# #2886. 更改数据类型 / Change Data Type

> 难度：简单 · 标签： · [LeetCode 链接](https://leetcode.com/problems/change-data-type/)

---

## 题目（英文原版）

**Description**

Write a solution to correct the errors:
The grade column is stored as floats, convert it to integers.
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
| grade       | float  |
+-------------+--------+
```

**Example 2:**

```
Example 1:
Input:
DataFrame students:
+------------+------+-----+-------+
| student_id | name | age | grade |
+------------+------+-----+-------+
| 1          | Ava  | 6   | 73.0  |
| 2          | Kate | 15  | 87.0  |
+------------+------+-----+-------+
Output:
+------------+------+-----+-------+
| student_id | name | age | grade |
+------------+------+-----+-------+
| 1          | Ava  | 6   | 73    |
| 2          | Kate | 15  | 87    |
+------------+------+-----+-------+
Explanation: 
The data types of the column grade is converted to int.
```

---

## 题目（中文翻译）

编写一个解决方案来纠正错误：`grade` 列目前以浮点数（float）存储，请将其转换为整数（int）。结果的格式参见下面的示例。

示例  
示例 1:  
DataFrame students  

| Column Name | Type   |
|-------------|--------|
| student_id  | int    |
| name        | object |
| age         | int    |
| grade       | float  |

示例 2:  
Example 1:  

**Input:**  
DataFrame students:  

| student_id | name | age | grade |
|------------|------|-----|-------|
| 1          | Ava  | 6   | 73.0  |
| 2          | Kate | 15  | 87.0  |

**Output:**  

| student_id | name | age | grade |
|------------|------|-----|-------|
| 1          | Ava  | 6   | 73    |
| 2          | Kate | 15  | 87    |
| ... (已截断) |

约束条件：  
无

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**逐行遍历** DataFrame，把 `grade` 列的每一个 `float` 值手动转成 `int`，再把转换后的结果放回去。  
可以把这个过程类比成：

- **字典**：就像我们把一本词典里的每个词（key）对应的页码（value）一个一个改成新的页码。  
- **遍历**：把学生名单从头到尾翻一遍，看到 73.0 就把它改成 73。

这种做法一定能得到正确的结果，因为我们把每个元素都按照题目要求转了类型。

#### 代码（Python）

```python
import pandas as pd

def change_grade_bruteforce(students: pd.DataFrame) -> pd.DataFrame:
    """
    暴力实现：逐行遍历，将 grade 列的 float 转成 int
    """
    # 复制一份，防止在原 DataFrame 上直接修改产生副作用
    df = students.copy()

    # 通过 iterrows() 逐行访问 (index, Series) 对
    for idx, row in df.iterrows():
        # row['grade'] 是当前行的成绩，类型是 float
        # int() 可以把 float 转成整数（会直接截断小数部分）
        df.at[idx, 'grade'] = int(row['grade'])   # ←关键行：手动转换

    return df
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  这里的 `n` 是 DataFrame 的行数。我们需要遍历每一行一次，才能把对应的 `grade` 改成整数。  
  “O(n)” 可以理解为“随数据规模线性增长”，数据越多，耗时几乎成正比。

- **空间复杂度**：`O(1)`（不计返回的结果）  
  只用了常数级别的额外变量（`idx`, `row`），没有随 `n` 增长的额外数据结构。  
  （如果把复制的 DataFrame 计入空间，则是 `O(n)`，因为复制本身占用了同样大小的内存。）

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于逐行遍历——每访问一行都要进行 Python 层面的循环，速度相对慢。  
Pandas 本身是基于 **向量化** 操作的，它在内部使用 C/NumPy 加速，对整列进行一次性操作要快很多。

优化的关键在于：

1. **一次性指定列的目标类型**：`DataFrame.astype()` 可以把整列一次性转换成目标 dtype（数据类型），底层是批量操作。  
2. **使用字典映射**：`astype({'grade': 'int'})` 把 `grade` 列指定为 `int`，其他列保持不变。  
   - 这里的字典可以类比成“批量改页码的指令表”，一次性告诉系统哪些列要改成什么类型。

这样我们不需要写循环，直接交给 Pandas 完成转换，代码更简洁，运行更快。

#### 代码（Python）

```python
import pandas as pd

def change_grade_optimal(students: pd.DataFrame) -> pd.DataFrame:
    """
    最优实现：利用 pandas 的 astype() 批量转换列类型
    """
    # 复制一份防止修改原始数据
    df = students.copy()

    # 使用字典一次性把 'grade' 列转成整数类型
    # astype 会在内部使用高效的向量化运算，速度远快于 Python 循环
    df = df.astype({'grade': 'int'})

    return df
```

#### 复杂度

- **时间复杂度**：`O(n)`（但常数更小）  
  虽然仍然需要遍历所有元素（因为每个数都要改类型），但底层是 **向量化** 的 C 实现，实际运行时间明显快于逐行 Python 循环。  
  “O(n)” 仍然表示“随行数线性增长”，只是每一步的工作更轻。

- **空间复杂度**：`O(1)`（不计返回的结果）  
  `astype` 会在内部创建一个新的列对象，但不需要额外的 Python 级别临时变量。若算上返回的 DataFrame，则是 `O(n)`（因为必须保存全部数据），这在任何解法中都是不可避免的。

---

## 心得

- **核心技巧**：使用 Pandas 的向量化操作（如 `astype`）一次性批量处理列的数据类型。  
- **适用题型**：
  1. **列类型统一**：如把日期字符串列转换成 `datetime` 类型。  
  2. **数值归一化**：把多个数值列一次性除以最大值或转成 `float64`。  
  3. **类别编码**：把若干 `object`（字符串）列一次性转成 `category`。  
- **解题钥匙**：**“先想有没有现成的 Pandas 函数可以一次搞定”**，不要急着写循环。

---

## 反思

- **第一反应**：看到“把 float 变成 int”，下意识想用 `for` 循环逐行 `int()`，因为这和平时处理普通列表的方式一样。  
- **最容易踩的坑**：
  - **忘记复制 DataFrame**：直接在原始 `students` 上修改会导致副作用，后面的测试用例可能受影响。  
  - **数据丢失**：`int()` 会直接截断小数，若题目要求四舍五入，需要使用 `round()` 再转 `int`。  
  - **列名写错**：字典的键必须完全匹配列名，否则 `astype` 会报错。  
- **下次第一步**：先在 **Pandas 文档或常用 API 列表** 中搜索 “convert column dtype”，找出能一次性完成的函数，再决定是否需要手动遍历。