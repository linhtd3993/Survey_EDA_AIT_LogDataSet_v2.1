import sys, unittest
from pathlib import Path
from datetime import datetime, timezone
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from inventory import stamp
from profile_events import time_of
from extended_time import parse_hour

class TimeTests(unittest.TestCase):
    def test_explicit_offset(self):
        target=datetime(2022,1,24,3,1,tzinfo=timezone.utc).timestamp()
        self.assertEqual(time_of(b'- [24/Jan/2022:04:01:00 +0100]','apache2/access.log',2022,False),target)
        self.assertEqual(time_of(b'{"@timestamp":"2022-01-24T03:01:00.000Z"}','logstash/sample.log',2022,False),target)
        self.assertEqual(parse_hour(b'2022-01-24T04',b'+0100'),target-60)
    def test_ambiguous_clock(self):
        self.assertIsNone(stamp(b'Jan 24 03:01:00 sample','auth',2022,False))
        self.assertIsNone(stamp(b'Feb 30 00:00:00 sample','auth',2022,True))
        self.assertEqual(stamp(b'msg=audit(1642999060.603:1)','audit',2022,False),1642999060.603)
