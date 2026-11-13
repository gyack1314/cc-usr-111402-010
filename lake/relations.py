"""关系行、袋身份以及简单三值谓词。"""
from .storage import canonical

def validate(rows):
    ids=[]
    for row in rows:
        if not isinstance(row,dict) or not isinstance(row.get('row_id'),str):raise ValueError('关系行缺少身份')
        ids.append(row['row_id'])
    if len(set(ids))!=len(ids):raise ValueError('关系行身份重复')
    return rows

def compare(left,op,right=None):
    if op=='is_null':return left is None
    if left is None or right is None:return None
    if op=='eq':return type(left) is type(right) and left==right
    if op=='ne':return not compare(left,'eq',right)
    if op=='gt':return left>right
    raise ValueError('比较操作不支持')

def predicate(row,expr):
    if 'and' in expr:
        values=[predicate(row,e) for e in expr['and']]
        return False if False in values else None if None in values else True
    return compare(row[expr['column']],expr['op'],expr.get('value'))

def bag(rows):
    result={}
    for row in rows:
        key=canonical(row).decode();result[key]=result.get(key,0)+1
    return result
