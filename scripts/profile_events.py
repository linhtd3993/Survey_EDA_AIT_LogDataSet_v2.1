"""Profile annotation-target files, with the release schedule used only retrospectively."""
import calendar
import csv
import io
import json
import re
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timezone
from functools import lru_cache
from zipfile import ZipFile
from inventory import ROOT, OUT, ACCOUNT, TYPE, MONTHS, stamp, clock_value, write_csv
from log_reader import log_path

ISO=re.compile(rb'(\d{4}-\d\d-\d\d[T ]\d\d:\d\d:\d\d)(?:\.\d+)?(Z|[+-]\d\d:?\d\d)?')
APACHE=re.compile(rb'\[(\d\d)/(\w{3})/(\d{4}):(\d\d:\d\d:\d\d) ([+-]\d{4})\]')
ERROR=re.compile(rb'^\[\w{3} (\w{3}) +(\d+) (\d\d:\d\d:\d\d)(?:\.\d+)? (\d{4})\]')
SESSION=re.compile(rb'\bses=(\d+)')
@lru_cache(maxsize=65536)
def seconds(value,offset):
    t=datetime.fromisoformat((value+offset).decode())
    return t.timestamp()

def time_of(raw,name,year,utc):
    if name.startswith("audit/"): return stamp(raw,"audit",year,utc)
    if name.startswith(("auth.log","dnsmasq")): return stamp(raw,"auth",year,utc)
    if name.startswith("logstash/"):
        m=re.search(rb'"@timestamp"\s*:\s*"([^"]+)"',raw)
        if not m:return None
        raw=m[1]
    if name.startswith("apache"):
        m=APACHE.search(raw)
        if m:
            d,mon,y,t,offset=m.groups()
            return seconds(b"%s-%02d-%sT%s"%(y,MONTHS.index(mon)+1,d,t),offset)
        m=ERROR.match(raw)
        if m and utc:
            mon,d,t,y=m.groups()
            return seconds(b"%s-%02d-%02dT%s"%(y,MONTHS.index(mon)+1,int(d),t),b"+00:00")
        return None
    m=ISO.match(raw)
    if m and (m[2] or utc):return seconds(m[1],m[2] or b"+00:00")
    return None

def profile(ds):
    info=next(r for r in json.loads((ROOT/"outputs/archive_manifest.json").read_text()) if r["dataset"]==ds)
    window=next(r for r in csv.DictReader((ROOT/"configs/published_windows.csv").open(encoding="utf-8-sig")) if r["dataset"]==ds)
    start,end=[clock_value(info["metadata"][k]) for k in ("start","end")]
    a,b=[clock_value(window[k]) for k in ("attack_start","attack_end")]
    year=datetime.fromtimestamp(start,timezone.utc).year
    output=[]
    history=defaultdict(list)
    session_counts=Counter()
    audit_accounts=0
    with ZipFile(ROOT/"data/archives"/info["archive"]) as z:
        labeled={log_path(p):p for p in z.namelist() if p.startswith("labels/") and not p.endswith("/")}
        paths=set(labeled)|{p for p in z.namelist() if re.fullmatch(r"gather/[^/]+/logs/audit/audit\.log(?:\.\d+)?",p)}
        for path in sorted(paths):
            ids=set()
            if path in labeled:
                with z.open(labeled[path]) as f:ids={json.loads(line)["line"] for line in f}
            host=path.split("/")[1]
            name=path.split("/logs/",1)[1]
            zones=info["host_timezone_files"]
            utc=any(zones.get(f"gather/{host}/configs/{s}timezone") in ("UTC","Etc/UTC") for s in ("","etc/"))
            counts=Counter()
            with z.open(path) as f:
                for n,raw in enumerate(io.BufferedReader(f),1):
                    try:t=time_of(raw,name,year,utc)
                    except (ValueError,OverflowError):t=None
                    phase="unknown" if t is None else "outside" if not start<=t<end else "before" if t<a else "during" if t<b else "after"
                    counts[phase,n in ids]+=1
                    if name.startswith("audit/") and phase in ("before","during","after"):
                        acct=ACCOUNT.search(raw)
                        kind=TYPE.match(raw)
                        if not acct or not kind or acct[1] in (b"?",b"",b"(unknown)"):continue
                        history[host,acct[1]].append((t,kind[1]))
                        audit_accounts+=1
                        session=SESSION.search(raw)
                        if session and session[1]!=b"4294967295":session_counts[host,session[1],acct[1]]+=1
            for (phase,linked),lines in counts.items():
                output.append(dict(dataset=ds,path=path,phase=phase,annotated=int(linked),lines=lines))
    new=den=0
    for values in history.values():
        previous=set()
        import itertools
        for _,batch in itertools.groupby(sorted(values),key=lambda v:v[0]):
            kinds=[kind for _,kind in batch]
            if previous:
                den+=len(kinds)
                new+=sum(k not in previous for k in kinds)
            previous.update(kinds)
    write_csv(OUT/ds/"label_windows.csv",output,["dataset","path","phase","annotated","lines"])
    account=dict(with_account=audit_accounts,with_session=sum(session_counts.values()),session_groups=len(session_counts),novel=new,eligible=den)
    (OUT/ds/"history.json").write_text(json.dumps(account),encoding="utf-8")
    print(ds,flush=True)

if __name__=="__main__":
    with ProcessPoolExecutor(max_workers=4) as pool:
        list(pool.map(profile,[r["dataset"] for r in json.loads((ROOT/"outputs/archive_manifest.json").read_text())]))
