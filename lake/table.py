"""不可变关系版本及带旧版本条件的目录更新。"""
import os,json,tempfile
from pathlib import Path
from .storage import canonical
from .relations import validate

class Table:
    def __init__(self,storage,root):
        self.storage=storage;self.root=Path(root);self.root.mkdir(parents=True,exist_ok=True);self.refs=self.root/'heads.json'
    def heads(self):return json.loads(self.refs.read_bytes()) if self.refs.exists() else {}
    def snapshot(self,digest):
        meta=self.storage.read(digest);rows=self.storage.read(meta['rows']);validate(rows)
        if len(rows)!=meta['count']:raise ValueError('关系目录行数错误')
        return rows
    def stage(self,rows,schema):
        validate(rows);return self.storage.write({'rows':self.storage.write(rows),'schema':schema,'count':len(rows)})
    def publish(self,name,expected,digest):
        self.snapshot(digest);lock=self.root/'.writing'
        fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
        try:
            refs=self.heads()
            if refs.get(name)!=expected:raise ValueError('表版本已变化')
            refs[name]=digest;tempfd,temp=tempfile.mkstemp(dir=self.root)
            try:
                with os.fdopen(tempfd,'wb') as stream:stream.write(canonical(refs));stream.flush();os.fsync(stream.fileno())
                os.replace(temp,self.refs)
            finally:
                if os.path.exists(temp):os.unlink(temp)
        finally:
            os.close(fd);lock.unlink()
        return digest
