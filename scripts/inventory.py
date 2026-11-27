"""Inventory ZIP members, count text lines, resolve annotations and profile audit/auth time."""
import argparse
import csv
import hashlib
import io
import json
import re
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from zipfile import ZipFile
from log_reader import count_lines, check_labels, log_path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs/runs/ait-v21-01"
MONTHS = b"Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
EPOCH = re.compile(rb'\baudit\((\d+)(?:\.(\d+))?:')
SYS = re.compile(rb'^(\w{3})\s+(\d{1,2}) (\d\d):(\d\d):(\d\d)')
ACCOUNT = re.compile(rb'\bacct="([^"]+)"')
TYPE = re.compile(rb'^type=(\w+)')
BINARY = {".pdf",".xls",".xlsx",".doc",".docx",".odt",".jpg",".jpeg",".png",".zip",".gz",".journal",".journal~",".pcap",".pcapng"}

@lru_cache(maxsize=65536)
def sys_epoch(parts, year):
    month, day, hour, minute, second = parts
    return datetime(year,MONTHS.index(month)+1,int(day),int(hour),int(minute),int(second),tzinfo=timezone.utc).timestamp()

def stamp(raw, source, year, utc):
    if source=="audit":
        match=EPOCH.search(raw)
        if match:
            return int(match[1])+float(b"0."+(match[2] or b"0"))
    elif utc:
        match=SYS.match(raw)
        if match:
            try:
                return sys_epoch(match.groups(),year)
            except ValueError:
                pass
    return None

def clock_value(s):
    return datetime.fromisoformat(s).replace(tzinfo=timezone.utc).timestamp()

def write_csv(path, rows, fields):
    with path.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

def scan(dataset):
    directory=OUT/dataset
    directory.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((ROOT/"outputs/archive_manifest.json").read_text(encoding="utf-8"))
    info=next(r for r in manifest if r["dataset"]==dataset)
    with (ROOT/"configs/published_windows.csv").open(encoding="utf-8-sig") as f:
        attack=next(r for r in csv.DictReader(f) if r["dataset"]==dataset)
    start,end=[clock_value(info["metadata"][k]) for k in ("start","end")]
    begin,finish=[clock_value(attack[k]) for k in ("attack_start","attack_end")]
    year=datetime.fromtimestamp(start,timezone.utc).year
    inventory=[]
    index={}
    hours=Counter()
    phases=Counter()
    labelrows=[]
    labeltypes=[]
    events=defaultdict(list)
    coverage=Counter()
    with ZipFile(ROOT/"data/archives"/info["archive"]) as z:
        for member in z.infolist():
            path=member.filename
            parts=path.split("/")
            if member.is_dir() or len(parts)<4 or parts[0]!="gather" or parts[2]!="logs":
                continue
            host=parts[1]
            name="/".join(parts[3:])
            source=parts[3] if len(parts)>4 else re.sub(r"\.\d+$","",parts[3])
            family="audit" if re.fullmatch(r"audit/audit\.log(?:\.\d+)?",name) else "auth" if re.fullmatch(r"auth\.log(?:\.\d+)?",name) else ""
            utc=any(info["host_timezone_files"].get(f"gather/{host}/configs/{prefix}timezone") in ("Etc/UTC","UTC") for prefix in ("","etc/"))
            count=None
            inside=outside=unknown=blank=0
            lo=hi=None
            with z.open(member) as data:
                stream=io.BufferedReader(data,buffer_size=1<<20)
                if Path(name).suffix.lower() in BINARY or b"\x00" in stream.peek(2048)[:2048]:
                    status="binary"
                elif family:
                    status="timed"
                    count=0
                    for count,raw in enumerate(stream,1):
                        blank+=int(not raw.strip())
                        t=stamp(raw,family,year,utc)
                        if t is None:
                            unknown+=1
                            continue
                        lo=t if lo is None else min(lo,t)
                        hi=t if hi is None else max(hi,t)
                        if not start<=t<end:
                            outside+=1
                            continue
                        inside+=1
                        hours[host,family,int(t//3600)*3600]+=1
                        phases[family,"before" if t<begin else "during" if t<finish else "after"]+=1
                        if family=="audit":
                            account=ACCOUNT.search(raw)
                            kind=TYPE.match(raw)
                            if account and account[1] not in (b"?",b"",b"(unknown)") and kind:
                                coverage["audit_with_account"]+=1
                                events[host,account[1]].append((t,kind[1]))
                else:
                    status="text"
                    count=count_lines(stream)
            index[path]=count
            inventory.append(dict(dataset=dataset,host=host,path=path,source=source,bytes=member.file_size,status=status,lines=count,inside=inside,outside=outside,unknown_time=unknown,blank_timed=blank,first_epoch=lo,last_epoch=hi))
        for member in z.infolist():
            if member.is_dir() or not member.filename.startswith("labels/"):
                continue
            path=log_path(member.filename)
            with z.open(member) as stream:
                counts,types=check_labels(io.BufferedReader(stream),index.get(path))
            labelrows.append(dict(dataset=dataset,path=path,**counts))
            labeltypes.extend(dict(dataset=dataset,path=path,label=k,assignments=v) for k,v in types.items())
    sequences=Counter()
    for history in events.values():
        history.sort(key=lambda x:x[0])
        for (t,a),(u,b) in zip(history,history[1:]):
            if u>t:
                sequences[a.decode(),b.decode()]+=1
            else:
                coverage["tied_pairs"]+=1
    coverage["host_account_pairs"]=len(events)
    coverage["accounts"]=len({account for host,account in events})
    coverage["pairs_with_history"]=sum(len(h)>1 for h in events.values())
    write_csv(directory/"files.csv",inventory,list(inventory[0]))
    fields="annotation_rows matched unique_lines assignments repeated_ref out_of_bounds unresolved_file malformed multilabel_rows".split()
    write_csv(directory/"joins.csv",labelrows,["dataset","path"]+fields)
    write_csv(directory/"labels.csv",labeltypes,["dataset","path","label","assignments"])
    write_csv(directory/"hours.csv",(dict(dataset=dataset,host=h,source=s,hour_epoch=t,lines=n) for (h,s,t),n in hours.items()),["dataset","host","source","hour_epoch","lines"])
    write_csv(directory/"phases.csv",(dict(dataset=dataset,source=s,phase=k,lines=phases[s,k],seconds=d) for s in ("audit","auth") for k,d in zip(("before","during","after"),(begin-start,finish-begin,end-finish))),["dataset","source","phase","lines","seconds"])
    write_csv(directory/"sequences.csv",(dict(dataset=dataset,previous=a,following=b,pairs=v) for (a,b),v in sequences.items()),["dataset","previous","following","pairs"])
    (directory/"account.json").write_text(json.dumps(coverage),encoding="utf-8")
    print(dataset,len(inventory),sum(x["lines"] or 0 for x in inventory),flush=True)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("datasets",nargs="*")
    args=parser.parse_args()
    datasets=args.datasets or [r["dataset"] for r in json.loads((ROOT/"outputs/archive_manifest.json").read_text())]
    with ProcessPoolExecutor(max_workers=min(4,len(datasets))) as pool:
        list(pool.map(scan,datasets))
