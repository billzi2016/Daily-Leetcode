# #2877. 从列表创建 DataFrame / Create a DataFrame from List

> 难度：简单 · 标签： · [LeetCode 链接](https://leetcode.com/problems/create-a-dataframe-from-list/)

---

## 题目（英文原版）

**Description**

Write a solution to create a DataFrame from a 2D list called student_data. This 2D list contains the IDs and ages of some students.
The DataFrame should have two columns, student_id and age, and be in the same order as the original 2D list.
The result format is in the following example.

**Examples**

**Example 1:**

```
Input:
student_data:
[
  [1, 15],
  [2, 11],
  [3, 11],
  [4, 20]
]
Output:
+------------+-----+
| student_id | age |
+------------+-----+
| 1          | 15  |
| 2          | 11  |
| 3          | 11  |
| 4          | 20  |
+------------+-----+
Explanation:
A DataFrame was created on top of student_data, with two columns named student_id and age.
```

---

## 题目（中文翻译）

编写代码，将名为 `student_data` 的二维列表（2D list）转换为 DataFrame。该二维列表包含若干学生的 ID 和年龄。  
生成的 DataFrame 应包含两列：`student_id` 和 `age`，且行的顺序与原二维列表保持一致。  
结果格式请参考下面的示例。

**示例 1**

**输入**  
`student_data:`  
```text
[
  [1, 15],
  [2, 11],
  [3, 11],
  [4, 20]
]
```

**输出**  
```
+------------+-----+
| student_id | age |
+------------+-----+
| 1          | 15  |
| 2          | 11  |
| 3          | 11  |
| 4          | 20  |
+------------+-----+
```

**解释**  
在 `student_data` 的基础上创建了一个 DataFrame，包含两列，列名分别为 `student_id` 和 `age`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**先把列表里的每一行读取出来，再把它们一个一个放进 DataFrame**。  
可以把 `student_data` 看成一本学生名册，里面每一行都是“学生 ID + 年龄”。  
我们可以手动遍历这本名册，把每条记录放进一个空的表格（DataFrame）里，就像把每个人的资料一张张贴到白板上。

- **用到的数据结构**  
  - `list`：原始的二维列表，类似于一排排的纸条。  
  - `pandas.DataFrame`：表格容器，像 Excel 表格。我们先创建一个空的 DataFrame，再用 `df.loc[index] = [...]` 把每行数据写进去。

- **为什么正确**  
  只要我们按照原列表的顺序把每条记录逐行写入表格，最终得到的 DataFrame 就和列表的顺序完全一致，列名只要在创建时指定即可。

- **复杂度分析（大白话）**  
  - **时间**：我们需要遍历列表一次，列表有 `n` 条记录，所以大约要做 `n` 次“写入”操作，用数学语言记作 **O(n)**，意思是时间随记录数线性增长。  
  - **空间**：除了原列表本身，我们额外创建了一个大小为 `n` 的 DataFrame，空间也随 `n` 增长，记作 **O(n)**。

#### 代码（Python）

```python
import pandas as pd  # pandas 是 Python 里处理表格的工具，类似 Excel

# 题目给出的二维列表
student_data = [
    [1, 15],
    [2, 11],
    [3, 11],
    [4, 20]
]

# ① 先创建一个空的 DataFrame，指定列名
df = pd.DataFrame(columns=['student_id', 'age'])

# ② 用循环把每一行数据逐个写进去
for i, row in enumerate(student_data):
    # df.loc[i] 表示第 i 行（从 0 开始计数）
    # row[0] 是学生 ID，row[1] 是年龄
    df.loc[i] = [row[0], row[1]]   # 把 ID 和 age 放进对应列

print(df)
```

#### 复杂度

- **时间复杂度**：O(n) — 需要遍历 `student_data` 中的每一行一次。  
- **空间复杂度**：O(n) — 生成的 DataFrame 大小正好和列表一样大。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**逐行写入**，每写一行都要让 DataFrame 调整内部结构，实际运行时会有额外的开销。  
Pandas 已经提供了一个“一键”函数 `pd.DataFrame(data, columns=…)`，它可以一次性把整个二维列表转成表格，内部实现是一次性分配好所有行列的内存，效率更高。

优化思路：

1. **一次性构造**：直接把整个 `student_data` 交给 `pd.DataFrame`，让它一次性完成所有工作。  
2. **指定列名**：在创建时把 `columns=['student_id', 'age']` 传进去，这一步相当于在白板的最上面先写好标题。

> **类比**：如果你要把一堆纸条贴到白板上，暴力解相当于“一张一张”贴，最优解相当于一次性把所有纸条粘在一起，再一次性贴到白板上，省时又省力。

#### 代码（Python）

```python
import pandas as pd

student_data = [
    [1, 15],
    [2, 11],
    [3, 11],
    [4, 20]
]

# 直接一次性把列表转成 DataFrame，同时指定列名
df = pd.DataFrame(student_data, columns=['student_id', 'age'])

print(df)
```

#### 复杂度

- **时间复杂度**：O(n) — 仍然需要读取 `n` 条记录，但只遍历一次，没有额外的写入开销。相当于“跑得更快”。  
- **空间复杂度**：O(n) — 仍然需要存储 `n` 条记录的表格，只是内部实现更紧凑。

---

## 心得

- **核心技巧**：利用 Pandas 的构造函数一次性把二维列表转成 DataFrame，并在创建时指定列名。  
- **适用的题型**  
  1. 把 CSV、JSON、字典等结构化数据一次性转成 DataFrame。  
  2. 将嵌套列表（矩阵）转成表格进行后续分析。  
  3. 需要对已有列表快速加上列标题再做统计时。  
- **一句话总结**：**“一次性构造 + 明确列名” 是把列表变表格的钥匙。**

---

## 反思

- **第一反应**：看到“二维列表 → DataFrame”，马上想到用 `pd.DataFrame`，但有时会担心要手动循环才能指定列名。  
- **最容易踩的坑**  
  - 忘记在构造函数里写 `columns=`，导致列名是默认的 `0, 1`。  
  - 输入的列表不是二维的（比如空列表或内部元素长度不一致）会报错，需要提前检查。  
- **下次遇到同类题**：第一步就思考**是否有现成的“一键”函数**（如 `pd.DataFrame`、`np.array`），如果有，直接利用它可以省去手动循环的繁琐。