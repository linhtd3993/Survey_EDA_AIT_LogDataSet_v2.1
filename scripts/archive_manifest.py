from pathlib import Path
import csv, json, hashlib, zipfile, yaml
from datetime import datetime

root = Path(__file__).resolve().parents[1]
windows = {row["dataset"]: row for row in csv.DictReader((root/"configs/published_windows.csv").open(encoding="utf-8-sig"))}
records = []
for item in csv.DictReader((root/'configs/archives.csv').open(encoding='utf-8-sig')):
    path = root/'data/archives'/item['key']
    with path.open('rb') as stream:
        digest = 'md5:' + hashlib.file_digest(stream,'md5').hexdigest()
    assert digest == item['checksum'] and path.stat().st_size == int(item['size'])
    with zipfile.ZipFile(path) as archive:
        members = archive.infolist()
        meta, = [e for e in members if e.filename.rsplit('/',1)[-1] in ('dataset.yml','dataset.yaml') and ('/' not in e.filename.strip('/') or e.filename.strip('/').count('/')==1)]
        metadata = yaml.safe_load(archive.read(meta))
        dataset = path.name.split("_")[0]
        window = windows[dataset]
        bounds_match = all(datetime.fromisoformat(str(metadata[key])) == datetime.fromisoformat(window["simulation_" + key]) for key in ("start","end"))
        zones = {entry.filename: archive.read(entry).decode().strip() for entry in members if entry.filename.startswith("gather/") and entry.filename.endswith("/timezone")}
        records.append(dict(dataset=dataset, archive=path.name, size=path.stat().st_size, checksum=digest, members=len(members), expanded_bytes=sum(e.file_size for e in members), metadata_path=meta.filename, metadata=metadata, published_window_matches=bounds_match, host_timezone_files=zones))

out = root/'outputs'
out.mkdir(exist_ok=True)
(out/'archive_manifest.json').write_text(json.dumps(records, indent=2, default=str), encoding='utf-8')
    print([(r['dataset'],r['members'],r['metadata_path']) for r in records])
