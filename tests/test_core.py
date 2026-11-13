"""现有内容存储及关系目录的正确性。"""
import tempfile,unittest
from pathlib import Path
from lake.storage import Storage
from lake.table import Table
from lake.relations import compare,validate,bag

class CoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.store=Storage(self.root/'objects')
    def test_object_roundtrip(self):
        a=self.store.write({'值':None,'items':[1,2]});self.assertEqual(self.store.read(a),{'值':None,'items':[1,2]})
        self.assertEqual(a,self.store.write({'items':[1,2],'值':None}))
    def test_object_corruption(self):
        a=self.store.write([1]);(self.store.root/a).write_bytes(b'[2]')
        with self.assertRaises(ValueError):self.store.read(a)
    def test_identity_rejected(self):
        with self.assertRaises(ValueError):self.store.read('../secret')
    def test_frozen_table(self):
        t=Table(self.store,self.root/'refs');a=t.stage([{'row_id':'x','v':1}],{'v':'int'});t.publish('main',None,a)
        b=t.stage([{'row_id':'x','v':2}],{'v':'int'});t.publish('main',a,b)
        self.assertEqual(t.snapshot(a)[0]['v'],1)
        with self.assertRaises(ValueError):t.publish('main',a,b)
    def test_bag_and_identity(self):
        self.assertEqual(list(bag([{'v':1},{'v':1}]).values()),[2])
        with self.assertRaises(ValueError):validate([{'row_id':'x'},{'row_id':'x'}])
    def test_null_comparison(self):
        self.assertIsNone(compare(None,'eq',None));self.assertTrue(compare(None,'is_null'));self.assertFalse(compare(1,'eq',True))
