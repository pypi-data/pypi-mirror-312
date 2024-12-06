# 项目用途

参考ailabx和qlib，优化了一些代码，将qlib因子计算独立出来使用。并简化使用方法。

# 用法设计

## 数据 
使用内置的下载数据工具或使用自有数据源


## 计算因子

将因子写在用户指定的csv中:
```
因子名，因子表达式
feature1,$close/Ref($close,20)-1
```
label设置：
```
label0,Ref($close, -5)/Ref($close, -1) - 1
```

读取csv文件，并对指定的数据开展这些表达式的计算。

## 因子分析

pip install alphalens