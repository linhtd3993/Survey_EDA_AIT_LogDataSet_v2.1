"""Fetch approved no-pcaps ZIPs using resumable, verified byte ranges."""
import csv
import hashlib
import http.client
import re
import shutil
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/archives"
BLOCK = 8 * 1024**2

def fetch(task):
    row, start, end, chunk = task
    length = end - start + 1
    if chunk.exists() and chunk.stat().st_size == length:
        return
    req = urllib.request.Request(row["url"], headers={"Range": f"bytes={start}-{end}"})
    expected = f"bytes {start}-{end}/{row['size']}"
    for attempt in range(12):
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                if response.headers.get("Content-Range") != expected:
                    raise OSError("Unexpected Content-Range")
                block = response.read(length)
            if len(block) != length:
                raise OSError("Incomplete range")
            temp = chunk.with_suffix(".tmp")
            temp.write_bytes(block)
            temp.replace(chunk)
            return
        except (OSError, http.client.HTTPException) as exc:
            if attempt == 11:
                raise
            print(row["key"], start, exc, flush=True)
            time.sleep(min(60, 2**attempt))

def main():
    rows = list(csv.DictReader((ROOT/"configs/archives.csv").open(encoding="utf-8-sig")))
    assert len(rows) == len({r["key"] for r in rows}) == 8
    RAW.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=12) as workers:
        for row in sorted(rows, key=lambda r: int(r["size"])):
            name = row["key"]
            assert re.fullmatch(r"[a-z]+_no-pcaps\.zip", name)
            final = RAW/name
            part = RAW/(name+".part")
            size = int(row["size"])
            if not final.exists():
                part.touch(exist_ok=True)
                chunks = RAW/(name+".chunks")
                chunks.mkdir(exist_ok=True)
                tasks = [(row, start, min(size, start + BLOCK)-1, chunks/str(start))
                         for start in range(part.stat().st_size, size, BLOCK)]
                list(workers.map(fetch, tasks))
                with part.open("ab") as out:
                    for _, start, _, chunk in tasks:
                        assert out.tell() == start
                        with chunk.open("rb") as stream:
                            shutil.copyfileobj(stream, out)
                candidate = part
            else:
                candidate = final
            assert candidate.stat().st_size == size
            with candidate.open("rb") as stream:
                assert "md5:" + hashlib.file_digest(stream, "md5").hexdigest() == row["checksum"], name
            with ZipFile(candidate) as archive:
                assert archive.infolist()
            if candidate == part:
                part.replace(final)
            print("verified", name, size, flush=True)

if __name__ == "__main__":
    main()
