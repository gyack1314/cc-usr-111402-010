"""资料与现有领域接口的核对。"""
import unittest,tempfile,json
from pathlib import Path
from lake.storage import Storage
from lake.elimination import inspect

class DomainTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.store=Storage(self.root/'objects')
        self.data=json.loads(Path('data/source.json').read_text(encoding='utf-8'))
    def test_existing_reader(self):
        self.assertTrue(inspect(self.data,self.store,self.root))

    def test_untrusted_and_stale_claim(self):
        from lake.elimination import validate_claim,bound
        d=self.data;good=validate_claim(d['tables']['carriers'],d['claims'][0]);bad=validate_claim(d['tables']['hubs'],d['claims'][1])
        self.assertTrue(good['validated']);self.assertFalse(bad['validated'])
        with self.assertRaises(ValueError):bound(bad,d['tables']['hubs'])
        with self.assertRaises(ValueError):bound(good,d['tables']['carriers']+[{'row_id':'c2','code':'c2'}])
