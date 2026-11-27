"""Hourly counts for Suricata counters/events and Logstash JSON, with explicit time coverage."""
import io
import json
import re
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime,timezone
from functools import lru_cache
from zipfile import ZipFile
from inventory import ROOT,OUT,write_csv,clock_value

HEADER=re.compile(rb"^Date: (\d+)/(\d+)/(\d{4}) -- (\d\d):",re.M)
FIELDS={s:re.compile(rb'"'+k+rb'"\s*:\s*"(\d{4}-\d\d-\d\dT\d\d):\d\d:\d\d(?:\.\d+)?(Z|[+-]\d\d:?\d\d)"') for s,k in (("eve",b"timestamp"),("logstash",b"@timestamp"))}

@lru_cache(maxsize=32768)
def parse_hour(hour,zone):
    return int(datetime.fromisoformat((hour+b":00:00"+zone).decode()).timestamp())

def profile(ds):
    archive=next(r for r in json.loads((ROOT/"outputs/archive_manifest.json").read_text()) if r["dataset"]==ds)
    rows=[]
    coverage=[]
    start,end=[clock_value(archive["metadata"][k]) for k in ("start","end")]
    with ZipFile(ROOT/"data/archives"/archive["archive"]) as z:
        for entry in z.infolist():
            p=entry.filename
            parts=p.split("/")
            if entry.is_dir() or len(parts)<5 or parts[0]!="gather" or parts[2]!="logs":continue
            name="/".join(parts[3:])
            if name=="suricata/stats.log":source="stats"
            elif name=="suricata/eve.json":source="eve"
            elif name.startswith("logstash/") and name.endswith(".log"):source="logstash"
            else:continue
            host=parts[1]
            utc=any(archive["host_timezone_files"].get(f"gather/{host}/configs/{s}timezone") in ("UTC","Etc/UTC") for s in ("","etc/"))
            counts=Counter()
            last=None
            total=0
            with z.open(entry) as f:
                stream=io.BufferedReader(f,buffer_size=1<<20)
                while block:=stream.read(1<<20):
                    if not block.endswith(b"\n"):block+=stream.readline()
                    total+=block.count(b"\n")+int(not block.endswith(b"\n"))
                    if source=="stats":
                        i=0
                        for m in HEADER.finditer(block):
                            counts[last]+=block.count(b"\n",i,m.start())
                            mo,d,y,h=map(int,m.groups())
                            last=int(datetime(y,mo,d,h,tzinfo=timezone.utc).timestamp()) if utc else None
                            i=m.start()
                        counts[last]+=block.count(b"\n",i)+int(not block.endswith(b"\n"))
                    else:
                        # Select a single primary event timestamp on each physical line.
                        for line in block.split(b"\n"):
                            if m:=FIELDS[source].search(line):
                                counts[parse_hour(*m.groups())]+=1
            inside=sum(n for t,n in counts.items() if t is not None and start<=t<end)
            known=sum(n for t,n in counts.items() if t is not None)
            assert 0<=inside<=known<=total
            coverage.append(dict(dataset=ds,path=p,source=source,lines=total,inside=inside,outside=known-inside,unknown=total-known))
            rows.extend(dict(dataset=ds,host=host,source=source,hour_epoch=t,lines=n) for t,n in counts.items() if t is not None and start<=t<end and n)
    write_csv(OUT/ds/"extended_hours.csv",rows,["dataset","host","source","hour_epoch","lines"])
    write_csv(OUT/ds/"extended_quality.csv",coverage,["dataset","path","source","lines","inside","outside","unknown"])
    print(ds,flush=True)

if __name__=="__main__":
    with ProcessPoolExecutor(max_workers=4) as pool:
        list(pool.map(profile,[r["dataset"] for r in json.loads((ROOT/"outputs/archive_manifest.json").read_text())]))
