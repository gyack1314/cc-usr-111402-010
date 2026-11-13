"""表证书全文验证与来源绑定。"""
from .storage import canonical
import hashlib
from .relations import validate

def table_digest(rows):return hashlib.sha256(canonical(rows)).hexdigest()

def validate_claim(rows,claim):
    validate(rows);cols=claim['columns'];values=[tuple(r[c] for c in cols) for r in rows]
    if claim['kind']=='unique':
        nonnull=[v for v in values if all(x is not None for x in v)];valid=len(set(nonnull))==len(nonnull)
    elif claim['kind']=='not_null':valid=all(all(x is not None for x in v) for v in values)
    else:raise ValueError('现有证书类型不支持')
    return {'table_digest':table_digest(rows),'columns':cols,'kind':claim['kind'],'coverage':'full','validated':valid}

def bound(certificate,rows):
    if not certificate['validated'] or certificate['coverage']!='full' or certificate['table_digest']!=table_digest(rows):raise ValueError('约束证据不可用')
    return True

def inspect(data,storage,root):
    certificates=[dict(table=c['table'],**validate_claim(data['tables'][c['table']],c)) for c in data['claims']]
    return {'certificates':certificates,'tables':{n:table_digest(rows) for n,rows in data['tables'].items()}}
