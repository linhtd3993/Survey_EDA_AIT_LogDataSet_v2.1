"""Reconcile ZIP member inventory and separately counted recording units."""
from pathlib import Path
import hashlib
import json
import platform
from zipfile import ZipFile
import pandas as pd
from inventory import OUT, ROOT

def verify():
    inputs=json.loads((ROOT/"outputs/archive_manifest.json").read_text())
    totals=[]
    for meta in inputs:
        ds=meta["dataset"]
        d=OUT/ds
        f=pd.read_csv(d/"files.csv")
        j=pd.read_csv(d/"joins.csv").fillna(0)
        labels=pd.read_csv(d/"labels.csv")
        hours=pd.read_csv(d/"hours.csv")
        phase=pd.read_csv(d/"phases.csv")
        with ZipFile(ROOT/"data/archives"/meta["archive"]) as z:
            paths={p for p in z.namelist() if not p.endswith("/") and p.startswith("gather/") and p.split("/")[2:3]==["logs"]}
            annotation_paths={p.replace("labels/","gather/",1) for p in z.namelist() if p.startswith("labels/") and not p.endswith("/")}
        assert set(f.path)==paths and f.path.is_unique
        assert set(j.path)==annotation_paths and j.path.is_unique
        assert (j.annotation_rows==j.matched+j.malformed+j.out_of_bounds+j.unresolved_file).all()
        assert (j.unique_lines+j.repeated_ref==j.matched).all()
        assert j.assignments.sum()==labels.assignments.sum()
        timed=f[f.status=="timed"]
        assert (timed.lines==timed.inside+timed.outside+timed.unknown_time).all()
        assert timed.inside.sum()==hours.lines.sum()==phase.lines.sum()
        totals.append(dict(dataset=ds,files=len(f),hosts=f.host.nunique(),binary=sum(f.status=="binary"),text_files=f.lines.notna().sum(),lines=int(f.lines.sum()),timed_lines=int(timed.lines.sum()),inside=int(timed.inside.sum()),outside=int(timed.outside.sum()),unknown=int(timed.unknown_time.sum()),**{k:int(j[k].sum()) for k in j.columns if k not in ("dataset","path")}))
    frame=pd.DataFrame(totals)
    frame.to_csv(OUT/"totals.csv",index=False)
    assets=[*ROOT.glob("scripts/*.py"),*ROOT.glob("configs/*.*"),*ROOT.glob("tests/*.py")]
    assets=[p for p in assets if p.name!=".gitkeep"]
    manifest=dict(run_id=OUT.name,python=platform.python_version(),archive_checksums={r["dataset"]:r["checksum"] for r in inputs},file_sha256={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in assets},totals=totals)
    (OUT/"manifest.json").write_text(json.dumps(manifest,default=int,indent=2),encoding="utf-8")
    print(frame.to_string(index=False))
if __name__=="__main__":
    verify()
