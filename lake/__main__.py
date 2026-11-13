"""本地资料的既有读取入口。"""
import argparse,json,tempfile
from pathlib import Path
from .storage import Storage
from .elimination import inspect

def main():
    p=argparse.ArgumentParser(description='核对并读取资料仓原始资料');p.add_argument('--source',default='data/source.json');a=p.parse_args()
    data=json.loads(Path(a.source).read_text(encoding='utf-8'))
    with tempfile.TemporaryDirectory() as temporary:
        root=Path(temporary);store=Storage(root/'objects');result=inspect(data,store,root)
        print(json.dumps(result,ensure_ascii=False,sort_keys=True))
if __name__=='__main__':main()
