# #2887. 填充缺失数据 / Fill Missing Data

> 难度：简单 · 标签： · [LeetCode 链接](https://leetcode.com/problems/fill-missing-data/)

---

## 题目（英文原版）

**Description**

Write a solution to fill in the missing value as 0 in the quantity column.
The result format is in the following example.

**Examples**

**Example 1:**

```
DataFrame products
+-------------+--------+
| Column Name | Type   |
+-------------+--------+
| name        | object |
| quantity    | int    |
| price       | int    |
+-------------+--------+
```

**Example 2:**

```
Example 1:
Input:+-----------------+----------+-------+
| name            | quantity | price |
+-----------------+----------+-------+
| Wristwatch      | None     | 135   |
| WirelessEarbuds | None     | 821   |
| GolfClubs       | 779      | 9319  |
| Printer         | 849      | 3051  |
+-----------------+----------+-------+
Output:
+-----------------+----------+-------+
| name            | quantity | price |
+-----------------+----------+-------+
| Wristwatch      | 0        | 135   |
| WirelessEarbuds | 0        | 821   |
| GolfClubs       | 779      | 9319  |
| Printer         | 849      | 3051  |
+-----------------+----------+-------+
Explanation: 
The quantity for Wristwatch and WirelessEarbuds are filled by 0.
```

---

## 题目（中文翻译）

编写一个解决方案，将 `quantity` 列中的缺失值填充为 **0**。结果的格式请参考下面的示例。

**示例 1**  
DataFrame `products`

```
+-------------+--------+
| Column Name | Type   |
+-------------+--------+
| name        | object |
| quantity    | int    |
| price       | int    |
+-------------+--------+
```

**示例 2**  
Example 1:

```
Input:
+-----------------+----------+-------+
| name            | quantity | price |
+-----------------+----------+-------+
| Wristwatch      | None     | 135   |
| WirelessEarbuds | None     | 821   |
| GolfClubs       | 779      | 9319  |
| Printer         | 849      | 3051  |
+-----------------+----------+-------+

Output:
+-----------------+----------+-------+
| name            | quantity | price |
+-----------------+----------+-------+
| Wristwatch      | 0        | 135   |
| WirelessEarbuds | 0        | 821   |
| GolfClubs       | 779      | 9319  |
| Printer         | 849      | 3051  |
+-----------------+----------+-------+
```

约束条件：无

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
题目很直接：给定一个 `pandas` DataFrame，要求把 **quantity** 列中缺失的值（`None`、`NaN` 等）全部填成 **0**。  
可以把这个任务想象成在一张表格里，用 **橡皮擦** 把空白的格子擦掉，然后在同一个位置写上 **0**。  

实现上，只需要遍历 **quantity** 列的每一个单元格，检查它是不是缺失值（`isnull()`），如果是就把它改成 0。  
- **数据结构**：这里使用的是 `pandas.DataFrame`，它类似于 Excel 表格，行列都有标签，列本身是 `Series`（可以把它想成“一列数据的列表”）。  
- **为什么正确**：只要把所有缺失的单元格改成 0，题目要求的“把缺失值填为 0”就完成了。  

#### 代码（Python）  

```python
import pandas as pd

def fill_missing_brute(df: pd.DataFrame) -> pd.DataFrame:
    """
    暴力遍历每一行，对 quantity 列的缺失值填 0
    """
    # 复制一份，防止修改原始 DataFrame（好习惯）
    result = df.copy()

    # 遍历 quantity 列的索引
    for idx in result.index:
        # pd.isnull 用来判断当前单元格是否是缺失值（None / NaN）
        if pd.isnull(result.at[idx, "quantity"]):
            # 把缺失的单元格直接赋值为 0
            result.at[idx, "quantity"] = 0

    return result

# ------------------- 示例 -------------------
data = {
    "name": ["Wristwatch", "WirelessEarbuds", "GolfClubs", "Printer"],
    "quantity": [None, None, 779, 849],
    "price": [135, 821, 9319, 3051],
}
df = pd.DataFrame(data)
print("原始 DataFrame:")
print(df)

filled = fill_missing_brute(df)
print("\n填充后 DataFrame:")
print(filled)
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  这里的 `n` 是 DataFrame 行数。我们只遍历一次每一行，检查并可能赋值一次。  
  “`O(n)`” 可以理解为“随行数线性增长”，行数翻倍，时间大约也会翻倍。  

- **空间复杂度**：`O(1)`（不计返回的副本）  
  除了存放结果的那份副本（`copy()`），算法本身只用了常数级别的额外变量（`idx`、临时布尔值），所以额外空间不随 `n` 增长。  

---  

### 2. 最优解  

#### 思路  
上面的暴力解已经是 **O(n)**，在遍历一次的前提下已经达到了线性时间，几乎没有提升空间。  
不过 `pandas` 本身提供了专门处理缺失值的向量化函数 `fillna()`，它一次性对整列（甚至整张表）执行填充，内部实现使用 C 语言的底层循环，速度更快，代码更简洁。  

**瓶颈所在**：  
- 手动 `for` 循环在 Python 层面会有解释器开销，虽然复杂度相同，但实际运行时间会慢一点。  

**优化思路**：直接调用 `fillna()`，只对 `quantity` 这一列填 0。  

**核心函数解释**：  
- `Series.fillna(value)`：把 Series 中所有缺失值（`NaN`、`None`）换成 `value`。可以把它想成“一键清理工具”，一次性把所有空格填满。  

#### 代码（Python）  

```python
import pandas as pd

def fill_missing_optimal(df: pd.DataFrame) -> pd.DataFrame:
    """
    使用 pandas 的 fillna() 向量化操作，一行代码完成填充
    """
    # 复制一份防止修改原始数据
    result = df.copy()

    # 只对 quantity 列执行 fillna，缺失值直接变为 0
    result["quantity"] = result["quantity"].fillna(0)

    return result

# ------------------- 示例 -------------------
data = {
    "name": ["Wristwatch", "WirelessEarbuds", "GolfClubs", "Printer"],
    "quantity": [None, None, 779, 849],
    "price": [135, 821, 9319, 3051],
}
df = pd.DataFrame(data)
print("原始 DataFrame:")
print(df)

filled = fill_missing_optimal(df)
print("\n填充后 DataFrame（最优解）:")
print(filled)
```

#### 复杂度  

- **时间复杂度**：`O(n)`（但常数因子更小）  
  `fillna` 仍然需要查看每一个元素一次，所以是线性时间。不过它在底层用了 C 实现，跑得更快。可以把它理解为“同样的路程，只是用了更快的车”。  

- **空间复杂度**：`O(1)`（不计返回的副本）  
  与暴力解相同，只是内部实现不需要额外的 Python 循环变量。  

---  

## 心得  

- **核心技巧**：掌握 `pandas` 的向量化函数（如 `fillna`、`replace`）可以让数据清洗既简洁又高效。  
- **适用场景**：  
  1. 将缺失值填充为特定数值（0、均值、中位数等）。  
  2. 替换某列的特定字符或数值（`Series.replace`）。  
  3. 对多列一次性执行同样的缺失值填充（`DataFrame.fillna`）。  
- **一句话总结**：**“缺失值填充—向量化是最快的钥匙”。**  

---  

## 反思  

- **第一反应**：看到 “quantity 列有 None，需要变成 0”，立刻想到遍历每行检查并赋值。  
- **最容易踩的坑**：  
  - 忽略 `NaN`（`numpy.nan`）与 `None` 的区别，只有 `isnull` 或 `fillna` 能统一处理。  
  - 直接在原 DataFrame 上修改可能影响后续使用，建议先 `copy()`。  
- **下次遇到同类题**：第一步先想 **“有没有 pandas 的内置函数可以一次性完成？”**，如果有，就直接使用向量化操作；没有再考虑手动遍历。