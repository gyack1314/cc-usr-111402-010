"""规范对象的内容寻址和完整性校验。"""
import hashlib,json,os,tempfile
from pathlib import Path

def canonical(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')

class Storage:
    def __init__(self,root):self.root=Path(root);self.root.mkdir(parents=True,exist_ok=True)
    def write(self,value):
        raw=canonical(value);digest=hashlib.sha256(raw).hexdigest();target=self.root/digest
        if target.exists():
            self.read(digest);return digest
        fd,temporary=tempfile.mkstemp(prefix='.new-',dir=self.root)
        try:
            with os.fdopen(fd,'wb') as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
            os.replace(temporary,target)
        finally:
            if os.path.exists(temporary):os.unlink(temporary)
        return digest
    def read(self,digest):
        if len(digest)!=64 or any(c not in '0123456789abcdef' for c in digest):raise ValueError('对象摘要非法')
        raw=(self.root/digest).read_bytes()
        if hashlib.sha256(raw).hexdigest()!=digest:raise ValueError('对象正文校验失败')
        return json.loads(raw)
