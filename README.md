# 仓库键约束证明驱动资料库

Python 3.11 资料仓基础项目。领域接口在 lake/elimination.py，合成原始资料保存在 data/source.json，字段和当前接口约定见 docs/contracts.md。现有读取入口只展示源码已经支持的基础行为；更高层的查询、管理和协调能力不在当前接口内。

内容存储与关系目录分离：lake/storage.py通过摘要验证不可变对象，lake/table.py通过期望旧版本发布新关系，lake/relations.py定义行身份、袋计量及三值谓词。运行入口使用临时工作目录，不改变原始资料。

开发检查与读取：

```sh
python -m unittest discover -s tests -v
python -m compileall -q lake tests
python -m lake
```
