# #2883. 删除缺失数据 / Drop Missing Data

> 难度：简单 · 标签： · [LeetCode 链接](https://leetcode.com/problems/drop-missing-data/)

---

## 题目（英文原版）

**Description**

There are some rows having missing values in the name column.
Write a solution to remove the rows with missing values.
The result format is in the following example.

**Examples**

**Example 1:**

```
DataFrame students
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
+------------+---------+-----+
| student_id | name    | age |
+------------+---------+-----+
| 32         | Piper   | 5   |
| 217        | None    | 19  |
| 779        | Georgia | 20  |
| 849        | Willow  | 14  |
+------------+---------+-----+
Output:
+------------+---------+-----+
| student_id | name    | age |
+------------+---------+-----+
| 32         | Piper   | 5   |
| 779        | Georgia | 20  | 
| 849        | Willow  | 14  | 
+------------+---------+-----+
Explanation: 
Student with id 217 havs empty value in the name column, so it will be removed.
```

---

## 题目（中文翻译）

有些行在 **name** 列中存在缺失值 (missing values)。  
请编写代码删除所有包含缺失值的行。结果的格式请参考下面的示例。

**示例 1**  

DataFrame (DataFrame) `students`

| Column Name | Type   |
|-------------|--------|
| student_id  | int    |
| name        | object |
| age         | int    |

**示例 2**  

**输入**：

| student_id | name    | age |
|------------|---------|-----|
| 32         | Piper   | 5   |
| 217        | None    | 19  |
| 779        | Georgia | 20  |
| 849        | Willow  | 14  |

**输出**：

| student_id | name    | age |
|------------|---------|-----|
| 32         | Piper   | 5   |
| 779        | Georgia | 20  |
| 849        | Willow  | 14  |

> 注：示例中已截断的部分请自行补全完整的表格。

**约束条件**  
无

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法就是 **一行一行** 看，看 `name` 这一列是否是缺失值（在 Python 中通常表现为 `None`、`np.nan` 或 `pd.NA`），如果是，就把这行“挑掉”。  

- **数据结构**：这里我们使用 **pandas 的 DataFrame**，可以把它想象成一张电子表格（Excel），每一行是一条记录，每一列是一个属性。  
- **查找缺失值**：`None` 就像字典里找不到对应的词条，`np.nan` 则像字典里写了“空”。我们只要逐行检查 `row['name']` 是否是这些“空”。  
- **为什么正确**：只要把所有 `name` 为缺失的行全部删掉，剩下的行必然都满足题目要求——没有缺失值。  

#### 代码（Python）  

```python
import pandas as pd
import numpy as np

# ---------- 示例数据 ----------
data = {
    "student_id": [32, 217, 779, 849],
    "name": ["Piper", None, "Georgia", "Willow"],   # None 表示缺失
    "age": [5, 19, 20, 14]
}
df = pd.DataFrame(data)

# ---------- 暴力实现 ----------
def drop_missing_bruteforce(df: pd.DataFrame) -> pd.DataFrame:
    # 用一个列表收集所有「不缺失」的行
    kept_rows = []
    for idx, row in df.iterrows():               # 逐行遍历，像一张纸上逐行检查
        # 判断 name 是否为缺失值（None、np.nan、pd.NA 都算缺失）
        if pd.notna(row["name"]):                # pd.notna 相当于「不是空」的检查
            kept_rows.append(row)                # 把这行保存下来
    # 把收集到的行重新拼成 DataFrame
    return pd.DataFrame(kept_rows).reset_index(drop=True)

result = drop_missing_bruteforce(df)
print(result)
```

**运行结果**

```
   student_id     name  age
0          32    Piper    5
1         779  Georgia   20
2         849   Willow   14
```

#### 复杂度  

- **时间复杂度**：`O(n)`，因为我们需要遍历 `n` 行一次。这里的 `O(n)` 可以理解为“随数据行数线性增长”。  
- **空间复杂度**：`O(k)`，其中 `k` 为保留下来的行数（最坏情况 `k = n`），因为我们要额外存一份不含缺失值的表格。

---

### 2. 最优解  

#### 思路  
虽然上面的暴力解已经是 `O(n)`，但我们手动遍历、逐行收集的过程在 **pandas** 里有更简洁、更高效的内置函数：`DataFrame.dropna`。  

- **瓶颈**：手动遍历会产生 Python 层的循环，速度比不上底层 C 实现的向量化操作。  
- **优化思路**：直接让 pandas 在内部用 C/NumPy 的向量化方式一次性筛选出缺失值所在的行，然后删除它们。  
- **核心函数**：`df.dropna(subset=['name'])`  
  - `subset=['name']` 表示只关注 `name` 这列是否缺失。  
  - `dropna` 相当于“把空格里的东西都扔掉”，一次性完成，不需要我们自己循环。  

> **类比**：如果把 DataFrame 当成一本电话簿，`dropna` 就像是一次性把所有没有姓名的页码撕掉，而不是一本一本翻过去检查。

#### 代码（Python）  

```python
import pandas as pd

# ---------- 示例数据 ----------
data = {
    "student_id": [32, 217, 779, 849],
    "name": ["Piper", None, "Georgia", "Willow"],   # None 表示缺失
    "age": [5, 19, 20, 14]
}
df = pd.DataFrame(data)

# ---------- 最优实现 ----------
def drop_missing_optimal(df: pd.DataFrame) -> pd.DataFrame:
    # 只检查 name 列，直接使用 pandas 的向量化函数 dropna
    # inplace=False 表示返回一个新 DataFrame，原 df 不变
    cleaned = df.dropna(subset=['name'])          # 把 name 为缺失的行全部删掉
    # 为了让索引从 0 开始、连续（可选），使用 reset_index
    return cleaned.reset_index(drop=True)

result = drop_missing_optimal(df)
print(result)
```

**运行结果**

```
   student_id     name  age
0          32    Piper    5
1         779  Georgia   20
2         849   Willow   14
```

#### 复杂度  

- **时间复杂度**：`O(n)`，但底层是 **向量化** 实现，实际运行速度比手写循环快很多。可以把它想成“一次性把整本书都扫描完”，而不是“一页页手动翻”。  
- **空间复杂度**：`O(k)`（`k` 为保留下来的行数），因为 `dropna` 会返回一个新 DataFrame，内部会复制需要保留的行。

---

## 心得  

- **核心技巧**：使用 pandas 的 `dropna`（或 `fillna`）进行缺失值处理。  
- **适用的题型**：  
  1. 删除/填充缺失值的预处理题（如“删除所有年龄为缺失的记录”）。  
  2. 基于特定列筛选数据的清洗题（如“只保留销量不为 NaN 的商品”）。  
- **解题钥匙**：**向量化函数**——把“逐行检查”交给 pandas，省时省力。

## 反思  

- **第一反应**：看到“缺失值”，自然想到遍历每一行判断 `None`，手动删掉。  
- **最容易踩的坑**：  
  - 只检查 `None` 而忽略 `np.nan`、`pd.NA`（它们在 pandas 里同样算缺失）。  
  - 删除后索引不连续，后续操作可能会因为旧索引而出错。  
- **下次类似题的第一步**：先思考是否有 **pandas 内置的向量化函数**（如 `dropna`、`fillna`、`replace`）可以一步完成，而不是自己写循环。