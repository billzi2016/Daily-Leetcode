# #2888. 重塑数据：拼接 / Reshape Data: Concatenate

> 难度：简单 · 标签： · [LeetCode 链接](https://leetcode.com/problems/reshape-data-concatenate/)

---

## 题目（英文原版）

**Description**

Write a solution to concatenate these two DataFrames vertically into one DataFrame.
The result format is in the following example.

**Examples**

**Example 1:**

```
DataFrame df1
+-------------+--------+
| Column Name | Type   |
+-------------+--------+
| student_id  | int    |
| name        | object |
| age         | int    |
+-------------+--------+

DataFrame df2
+-------------+--------+
| Column Name | Type   |
+-------------+--------+
| student_id  | int    |
| name        | object |
| age         | int    |
+-------------+--------+
```

**Example 2:**

```
Input:
df1
+------------+---------+-----+
| student_id | name    | age |
+------------+---------+-----+
| 1          | Mason   | 8   |
| 2          | Ava     | 6   |
| 3          | Taylor  | 15  |
| 4          | Georgia | 17  |
+------------+---------+-----+
df2
+------------+------+-----+
| student_id | name | age |
+------------+------+-----+
| 5          | Leo  | 7   |
| 6          | Alex | 7   |
+------------+------+-----+
Output:
+------------+---------+-----+
| student_id | name    | age |
+------------+---------+-----+
| 1          | Mason   | 8   |
| 2          | Ava     | 6   |
| 3          | Taylor  | 15  |
| 4          | Georgia | 17  |
| 5          | Leo     | 7   |
| 6          | Alex    | 7   |
+------------+---------+-----+
Explanation:
The two DataFramess are stacked vertically, and their rows are combined.
```

---

## 题目（中文翻译）

编写一个解决方案，将这两个数据框（DataFrame）**垂直**（即在行方向上）拼接成一个数据框（DataFrame）。  
结果的格式请参考下方示例。

**示例 1：**

DataFrame df1  
```
+-------------+--------+
| Column Name | Type   |
+-------------+--------+
| student_id  | int    |
| name        | object |
| age         | int    |
+-------------+--------+
```

DataFrame df2  
```
+-------------+--------+
| Column Name | Type   |
+-------------+--------+
| student_id  | int    |
| name        | object |
| age         | int    |
+-------------+--------+
```

**示例 2：**  

**输入：**  

df1  
```
+------------+---------+-----+
| student_id | name    | age |
+------------+---------+-----+
| 1          | Mason   | 8   |
| 2          | Ava     | 6   |
| 3          | Taylor  | 15  |
| 4          | Georgia | 17  |
+------------+---------+-----+
```

df2  
```
+------------+------+-----+
| student_id | name | age |
+------------+------+-----+
| 5          | Leo  | 7   |
| 6          | Alex | 7   |
... (已截断)
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法就是把 `df2` 的每一行一个一个取出来，追加到 `df1` 的后面。  
可以把 DataFrame 想象成 Excel 表格，手动把第二张表格的每一行复制粘贴到第一张表格的最后一行。  
实现时我们可以：

1. 用 `df1.values.tolist()` 把 `df1` 转成普通的 Python 列表（每行是一个子列表）。  
2. 用 `df2.iterrows()` 逐行遍历 `df2`，把每行的值（也是列表）追加到上一步得到的列表中。  
3. 最后把这个列表重新包装成 DataFrame，列名保持不变。

这样做是 **一定能得到正确答案** 的，因为我们没有改变任何行的顺序，也没有丢失数据，只是把两张表“拼”在一起。

> **时间/空间复杂度解释**  
> - `O(m + n)`：如果 `df1` 有 `m` 行，`df2` 有 `n` 行，我们需要遍历每一行一次，所以时间随行数线性增长。  
> - `O(m + n)`：我们把所有行都放进一个新的列表里，需要额外的存储空间，同样是线性增长。  
> 在大白话里，这就像是把两堆苹果一次性搬到一个更大的箱子里，搬的次数和箱子的容量都和苹果总数成正比。

#### 代码（Python）

```python
import pandas as pd

def concat_bruteforce(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    """
    暴力实现：逐行遍历 df2 并把每行追加到 df1 的数据列表中
    """
    # 1. 把 df1 的数据取出来，变成普通的二维列表
    rows = df1.values.tolist()          # 每一行是一个子列表

    # 2. 用 iterrows() 按行遍历 df2
    for _, row in df2.iterrows():
        # row 是一个 Series，使用 .tolist() 把它转成普通列表
        rows.append(row.tolist())       # 把 df2 的当前行追加到 rows 里

    # 3. 用原来的列名重新创建 DataFrame
    result = pd.DataFrame(rows, columns=df1.columns)
    return result
```

#### 复杂度

- **时间复杂度**：`O(m + n)` — 需要遍历 `df1` 的每一行（转成列表）以及 `df2` 的每一行，行数越多耗时越多，呈线性关系。  
- **空间复杂度**：`O(m + n)` — 额外创建了一个包含所有行的列表，这个列表的大小随总行数线性增长。

---

### 2. 最优解

#### 思路  
从暴力解可以看到，真正的“慢点”并不在遍历本身，而是我们手动把数据搬来搬去、重新包装成列表再构造 DataFrame。  
`pandas` 本身已经提供了高度优化的 **拼接函数** `pd.concat`，它内部使用了底层的 C 语言实现，速度比纯 Python 循环快很多。

**核心技巧**：使用 `pd.concat([df1, df2], axis=0)`，其中 `axis=0` 表示 **纵向**（上下）拼接。  
可以把它想象成 Excel 中的 “合并工作表”，只需要点几下按钮，系统会自动把两张表合并。

**为什么它更好**：

- **一次性操作**：不需要先把数据转成列表再转回 DataFrame，省去中间的拷贝。  
- **内部向量化**：`pandas` 在内部使用了高效的数组操作，避免了 Python 循环的开销。  
- **代码更简洁**：一行代码即可完成任务，易读易维护。

#### 代码（Python）

```python
import pandas as pd

def concat_optimal(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    """
    最优实现：直接使用 pandas 的 concat 函数进行纵向拼接
    """
    # axis=0 表示按行拼接（上下合并），ignore_index=True 会重新生成 0,1,2,... 的索引
    result = pd.concat([df1, df2], axis=0, ignore_index=True)
    return result
```

#### 复杂度

- **时间复杂度**：`O(m + n)` — 与暴力解相同，仍然需要遍历所有行，但每行的处理在底层更高效，实际运行时间更短。  
- **空间复杂度**：`O(m + n)` — 仍然需要存放合并后的所有行，只是没有额外的 Python 列表拷贝，内存占用略低。

---

## 心得

- **核心技巧**：使用 `pd.concat`（或 `DataFrame.append`）进行 DataFrame 的纵向拼接。  
- **适用的题型**  
  1. 多个相同结构的表格需要合并（如每日日志表合并成月表）。  
  2. 把训练集和测试集合并后统一做特征工程。  
  3. 将分块读取的大文件（CSV/Excel）拼接成完整的数据集。  
- **一句话总结**：`pd.concat` 就是 pandas 里专门用来“一键拼接”表格的万能钥匙。

## 反思

- **第一反应**：看到“把两个 DataFrame 垂直拼接”，马上想到手动遍历每行然后拼接。  
- **最容易踩的坑**  
  - 忘记设置 `ignore_index=True`，导致合并后索引出现重复。  
  - 两个 DataFrame 列顺序不一致时，`concat` 会按列名对齐，可能出现 NaN，需要确保列名一致或使用 `ignore_index` 前先统一列顺序。  
- **下次第一步**：先检查 pandas 是否已有对应的 **一键函数**（如 `concat`、`merge`、`join`），如果有，就直接使用，避免自行实现低效的循环。