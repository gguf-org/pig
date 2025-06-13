## pig
[<img src="https://raw.githubusercontent.com/gguf-org/pig/master/pig.gif" width="128" height="128">](https://github.com/gguf-org/pig)

install pig via pip/pip3:
```
pip install gguf-py
```

update pig (if previous version installed) by:
```
pip install gguf-py --upgrade
```

check current version by:
```
pig -v
```

check user manual by:
```
pig -h
```

### assembler
```
pig a
```
assemble a gguf by selecting a master file

### brush
```
pig b
```
brush/erase a selected tensor

### checker
```
pig c
```
check tensor info for a selected gguf

### decomposer
```
pig d
```
decompose a selected gguf by tensor dimensions (dim)

### extractor
```
pig e
```
extract a selected tensor

### fixer
```
pig f
```
fix/rename a selected tensor
