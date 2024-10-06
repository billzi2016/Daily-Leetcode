# #2890. 重塑数据：Melt / Reshape Data: Melt

> 难度：简单 · 标签： · [LeetCode 链接](https://leetcode.com/problems/reshape-data-melt/)

---

## 题目（英文原版）

**Description**

Write a solution to reshape the data so that each row represents sales data for a product in a specific quarter.
The result format is in the following example.

**Examples**

**Example 1:**

```
DataFrame report
+-------------+--------+
| Column Name | Type   |
+-------------+--------+
| product     | object |
| quarter_1   | int    |
| quarter_2   | int    |
| quarter_3   | int    |
| quarter_4   | int    |
+-------------+--------+
```

**Example 2:**

```
Input:
+-------------+-----------+-----------+-----------+-----------+
| product     | quarter_1 | quarter_2 | quarter_3 | quarter_4 |
+-------------+-----------+-----------+-----------+-----------+
| Umbrella    | 417       | 224       | 379       | 611       |
| SleepingBag | 800       | 936       | 93        | 875       |
+-------------+-----------+-----------+-----------+-----------+
Output:
+-------------+-----------+-------+
| product     | quarter   | sales |
+-------------+-----------+-------+
| Umbrella    | quarter_1 | 417   |
| SleepingBag | quarter_1 | 800   |
| Umbrella    | quarter_2 | 224   |
| SleepingBag | quarter_2 | 936   |
| Umbrella    | quarter_3 | 379   |
| SleepingBag | quarter_3 | 93    |
| Umbrella    | quarter_4 | 611   |
| SleepingBag | quarter_4 | 875   |
+-------------+-----------+-------+
Explanation:
The DataFrame is reshaped from wide to long format. Each row represents the sales of a product in a quarter.
```

---

## 题目（中文翻译）

编写一个解决方案，将数据重塑，使每一行表示某个产品在特定季度的销售数据。  
结果的格式请参考下面的示例。

**示例 1**

DataFrame report  

```
+-------------+--------+
| Column Name | Type   |
+-------------+--------+
| product     | object |
| quarter_1   | int    |
| quarter_2   | int    |
| quarter_3   | int    |
| quarter_4   | int    |
+-------------+--------+
```

**示例 2**

输入  

```
+-------------+-----------+-----------+-----------+-----------+
| product     | quarter_1 | quarter_2 | quarter_3 | quarter_4 |
+-------------+-----------+-----------+-----------+-----------+
| Umbrella    | 417       | 224       | 379       | 611       |
| SleepingBag | 800       | 936       | 93        | 875       |
+-------------+-----------+-----------+-----------+-----------+
```

输出  

```
...
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法就是 **手动遍历** 原始的 DataFrame，把每一行的 `product` 与四个季度的销量分别取出来，重新拼成 “长表格” 的形式：

| product | quarter | sales |
|--------|---------|-------|

- **遍历**：先遍历每一行（每个产品），再遍历四个季度列。  
- **构造新行**：把当前产品名、季度名称（`quarter_1` → `1`、`quarter_2` → `2`…）以及对应的销量放进一个临时的列表。  
- **汇总**：遍历结束后，用这个列表一次性创建新的 DataFrame。

> 类比：想象你有一本《季度销售报告》手册，里面每页列出一个产品四个季度的销量。要把它变成 “每页只写一个产品+季度+销量” 的小卡片，你只能一页页（行）翻过去，然后把每个季度的数字分别写到新的卡片上。

**为什么正确**  
因为我们没有改变任何数值，只是把原来宽表（每行有多个季度列）**拆分** 成了长表（每行只对应一个季度），信息是完整保留的。

#### 代码（Python）

```python
import pandas as pd

def melt_bruteforce(df: pd.DataFrame) -> pd.DataFrame:
    # 用来存放每一行新记录的临时列表
    records = []

    # 遍历每一行，row 是一个 Series，index 是列名
    for _, row in df.iterrows():
        product = row['product']               # 当前产品名
        # 四个季度列名固定为 quarter_1~quarter_4
        for q in range(1, 5):
            quarter_col = f'quarter_{q}'       # 如 'quarter_1'
            sales = row[quarter_col]           # 对应的销量
            # 把拆分后的信息加入列表
            records.append({
                'product': product,
                'quarter': q,                   # 用数字 1~4 表示季度
                'sales': sales
            })

    # 用收集好的字典列表一次性创建 DataFrame
    result = pd.DataFrame(records)
    # 为了和题目要求的列顺序保持一致，可再排序列
    result = result[['product', 'quarter', 'sales']]
    return result


# ---------- 示例运行 ----------
data = {
    'product': ['Umbrella', 'SleepingBag'],
    'quarter_1': [417, 800],
    'quarter_2': [224, 936],
    'quarter_3': [379, 93],
    'quarter_4': [611, 875]
}
df = pd.DataFrame(data)
print(melt_bruteforce(df))
```

#### 复杂度

- **时间复杂度**：`O(m * n)`  
  - 这里 `m` 是产品行数，`n` 是季度列数（固定为 4）。遍历每行的每个季度一次，所以总操作次数约为 `m × n`。  
  - 用大白话说，就是“产品多多少行，季度固定四个”，所以如果有 1000 行数据，就会执行约 4000 次“小操作”。  

- **空间复杂度**：`O(m * n)`  
  - 我们在 `records` 列表里保存了和原表同等数量的记录（每个原始单元格对应一条新记录），所以需要额外的存储空间与输出大小相同。  

---

### 2. 最优解

#### 思路  
虽然手动遍历可以得到正确结果，但 **代码冗长、可读性差**，而且每遍历一次都要在 Python 层面做很多小操作，效率不如底层实现。  
瓶颈就在 **“逐行、逐列的 Python 循环”**——循环本身在解释器里执行，速度相对慢。

**Pandas 提供的 `melt`** 正是为这种“宽表 → 长表”场景准备的 **专用函数**，内部实现已经用了向量化的 C / Cython 代码，速度快且语义清晰。

核心概念——**“堆叠（stack）”** 与 **“拆解（unpivot）”**：

- **堆叠**：把多列的数值“堆”到同一列，形成更长的表格。  
- `pd.melt(df, id_vars='product', var_name='quarter', value_name='sales')` 的含义是：  
  - `id_vars`：保持不变的列（这里是 `product`），相当于“主键”。  
  - `var_name`：原来列名（`quarter_1`…）会被搬到新列 `quarter` 中。  
  - `value_name`：对应的数值会搬到新列 `sales` 中。  

**一步到位**：只需要调用一次 `melt`，再把 `quarter` 列的字符串后缀去掉（`quarter_1` → `1`），即可得到目标结果。

#### 代码（Python）

```python
import pandas as pd

def melt_optimal(df: pd.DataFrame) -> pd.DataFrame:
    """
    使用 pandas 内置的 melt 完成宽表到长表的转换。
    """
    # 1. melt：把 quarter_1~quarter_4 四列“拆开”成两列
    melted = pd.melt(
        df,
        id_vars=['product'],          # product 列保持不变
        var_name='quarter',           # 原列名放进新列 quarter
        value_name='sales'            # 对应的数值放进新列 sales
    )
    # 2. 把 'quarter_1' 这种字符串只保留数字部分
    melted['quarter'] = melted['quarter'].str.replace('quarter_', '').astype(int)

    # 3. 按照题目要求的列顺序返回
    return melted[['product', 'quarter', 'sales']]


# ---------- 示例运行 ----------
data = {
    'product': ['Umbrella', 'SleepingBag'],
    'quarter_1': [417, 800],
    'quarter_2': [224, 936],
    'quarter_3': [379, 93],
    'quarter_4': [611, 875]
}
df = pd.DataFrame(data)
print(melt_optimal(df))
```

#### 复杂度

- **时间复杂度**：`O(m * n)`（与暴力解相同的量级）  
  - 只不过内部实现用了向量化操作，实际运行常数因子大幅下降。可以把它想象成“一次性把所有单元格搬家”，而不是“一个一个搬”。  

- **空间复杂度**：`O(m * n)`  
  - 仍需要存放与输出等量的数据，但不需要额外的 Python 列表对象，直接在 pandas 的内部结构里完成。

> 与暴力解对比：**代码行数从 20 多行降到 7 行**，**可读性提高**，**运行速度在大数据时往往快 5‑10 倍**（因为省掉了 Python 循环的开销）。

---

## 心得

- **核心技巧**：使用 `pandas.melt`（或 `DataFrame.stack`）进行宽表 → 长表的“拆解”。  
- **适用题型**  
  1. 将多个时间点的指标列合并为 “日期、指标值” 两列（如每日温度、每月收入）。  
  2. 把多种类别的计数列转为 “类别、计数” 两列（如商品种类的库存）。  
  3. 处理实验数据的“多变量宽表” → “变量、取值” 长表（常见于机器学习特征工程）。  
- **一句话总结解题钥匙**：**“用 pandas 的专用函数 melt，一次性把列‘摊平’成行”。**

---

## 反思

- **第一反应**：看到 “每行有四个 quarter 列”，立刻想到手动遍历把每列拆出来。  
- **最容易踩的坑**  
  - **列名处理**：`melt` 之后的 `quarter` 列仍是字符串（如 `quarter_1`），需要去掉前缀并转成整数，否则排序或后续计算会出错。  
  - **忘记指定 `id_vars`**：如果不告诉 `melt` 哪些列是“保持不变的键”，所有列都会被堆叠，导致 `product` 也被拆成两列。  
  - **数据类型**：`quarter` 需要是整数类型，以便后续按顺序排序或绘图。  
- **下次类似题的第一步**：先在脑中确认是 “宽表 → 长表” 的需求，然后直接搜索或回想 `pandas.melt`（或 `stack`）这类“一键”函数，避免手写循环。