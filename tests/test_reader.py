import io
import itertools
import json
import sys
import unittest
import zipfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from log_reader import count_lines, check_labels, log_path

class ReaderTests(unittest.TestCase):
    def test_physical_lines(self):
        for data, expected in [(b"",0),(b"\r\n\xff\n\nlast",4),(b"x\n",1),(b"x"*(2**20)+b"\n",1)]:
            self.assertEqual(count_lines(io.BytesIO(data)),expected)

    def test_join(self):
        rows=b'{"line":2,"labels":["a","b"]}\n{"line":2,"labels":["a"]}\n{"line":3,"labels":["a"]}\n?'
        stats, labels=check_labels(io.BytesIO(rows),2)
        self.assertEqual([stats[k] for k in ("matched","unique_lines","assignments","repeated_ref","out_of_bounds","malformed")],[2,1,3,1,1,1])
        self.assertEqual(check_labels(io.BytesIO(rows),None)[0]["unresolved_file"],3)
        for host in ("first","second"):
            self.assertEqual(log_path(f"labels/{host}/logs/auth.log.1"),f"gather/{host}/logs/auth.log.1")

    def test_author_example(self):
        path="labels/intranet_server/logs/audit/audit.log"
        with zipfile.ZipFile(ROOT/"data/archives/russellmitchell_no-pcaps.zip") as z:
            with z.open(path) as f:
                rows=[json.loads(x) for x in itertools.islice(f,4)]
            self.assertEqual([r["line"] for r in rows],list(range(1860,1864)))
            self.assertTrue(all(set(r["labels"])=={"attacker_change_user","escalate"} for r in rows))
            with z.open(log_path(path)) as f:
                events=[x.split()[0] for x in itertools.islice(f,1859,1863)]
            self.assertEqual(events,[b"type=USER_AUTH",b"type=USER_ACCT",b"type=CRED_ACQ",b"type=USER_START"])
