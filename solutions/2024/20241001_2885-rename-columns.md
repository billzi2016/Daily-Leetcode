# #2885. 列重命名 / Rename Columns

> 难度：简单 · 标签： · [LeetCode 链接](https://leetcode.com/problems/rename-columns/)

---

## 题目（英文原版）

**Description**

Write a solution to rename the columns as follows:
The result format is in the following example.

**Examples**

**Example 1:**

```
DataFrame students
+-------------+--------+
| Column Name | Type   |
+-------------+--------+
| id          | int    |
| first       | object |
| last        | object |
| age         | int    |
+-------------+--------+
```

**Example 2:**

```
Example 1:
Input:
+----+---------+----------+-----+
| id | first   | last     | age |
+----+---------+----------+-----+
| 1  | Mason   | King     | 6   |
| 2  | Ava     | Wright   | 7   |
| 3  | Taylor  | Hall     | 16  |
| 4  | Georgia | Thompson | 18  |
| 5  | Thomas  | Moore    | 10  |
+----+---------+----------+-----+
Output:
+------------+------------+-----------+--------------+
| student_id | first_name | last_name | age_in_years |
+------------+------------+-----------+--------------+
| 1          | Mason      | King      | 6            |
| 2          | Ava        | Wright    | 7            |
| 3          | Taylor     | Hall      | 16           |
| 4          | Georgia    | Thompson  | 18           |
| 5          | Thomas     | Moore     | 10           |
+------------+------------+-----------+--------------+
Explanation: 
The column names are changed accordingly.
```

---

## 题目（中文翻译）

编写一个解决方案，对 DataFrame 的列进行如下重命名。结果的格式请参考下面的示例。

**示例 1**  

DataFrame `students`

```
+-------------+--------+
| Column Name | Type   |
+-------------+--------+
| id          | int    |
| first       | object |
| last        | object |
| age         | int    |
+-------------+--------+
```

**示例 2**  

```
Input:
+----+---------+----------+-----+
| id | first   | last     | age |
+----+---------+----------+-----+
| 1  | Mason   | King     | 6   |
| 2  | Ava     | Wright   | 7   |
| 3  | Taylor  | Hall     | 16  |
| 4  | Georgia | Thompson | 18  |
| 5  | Thomas  | Moore    | 10  |
+----+---------+----------+-----+

Output:
+------------+------------+-----------+--------------+
| student_id | first_name | last_name | student_age |
+------------+------------+-----------+--------------+
| 1          | Mason      | King      | 6           |
| 2          | Ava        | Wright    | 7           |
| 3          | Taylor     | Hall      | 16          |
| 4          | Georgia    | Thompson  | 18          |
| 5          | Thomas     | Moore     | 10          |
+------------+------------+-----------+--------------+
```

**约束条件**  
无

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的办法就是**逐列遍历**，把每个旧列名换成我们想要的新列名。可以把 DataFrame 看成一张 Excel 表，列名就像表头的文字。我们把每个旧表头手动改成新表头，这和手动在 Excel 中点两次“重命名”是一样的。

实现思路：

1. 先准备一个 **旧列名 → 新列名** 的映射表（字典），相当于一本“小字典”，左边是旧名字，右边是新名字。  
2. 用 `for` 循环遍历 DataFrame 的 `columns`（所有列名），把每个列名在字典里查找对应的新名字，拼成一个新的列名列表。  
3. 把这个新列表直接赋值给 `df.columns`，DataFrame 的列名就全部改好了。

> **为什么正确**  
> 因为我们没有改动数据本身，只是把列名换成字典里对应的名字。只要字典里每个旧列名都有对应的新列名，最终的表头一定是我们想要的。

> **复杂度分析（大白话）**  
> - **时间**：我们只遍历了一遍列名，列的数量记作 *n*，所以时间是 **O(n)**，意思是列越多，花的时间线性增长。  
> - **空间**：只用了一个新列表保存 *n* 个名字，额外空间也是 **O(n)**，这在列数很少（一般几列）时几乎可以忽略不计。

#### 代码（Python）

```python
import pandas as pd

def rename_columns_brute(df: pd.DataFrame) -> pd.DataFrame:
    """
    暴力遍历每一列并重新命名
    """
    # 1）准备旧列名 → 新列名的映射表（就像查字典）
    rename_map = {
        "id": "student_id",
        "first": "first_name",
        "last": "last_name",
        "age": "student_age"
    }

    # 2）遍历原来的列名，逐个找对应的新名字
    new_columns = []                     # 用来装新的列名
    for col in df.columns:               # 对每一列
        # 如果在映射表里找得到，就换成新名字；否则保持原名
        new_columns.append(rename_map.get(col, col))

    # 3）把新列名列表直接赋值回 DataFrame
    df.columns = new_columns

    return df
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历了一遍列名，列越多耗时越多，但是线性关系。  
- **空间复杂度**：`O(n)` —— 需要一个和列数等长的新列表来存放新列名。

---

### 2. 最优解

#### 思路  

从暴力解来看，**遍历列名并手动拼列表** 这一步其实可以交给 Pandas 自己来完成。Pandas 的 `rename` 方法本质上已经实现了“把旧名字换成新名字”的功能，只需要把映射字典传进去即可。

**瓶颈**  
- 暴力解里我们自己写了一个循环，这在列数很多时仍然是 **O(n)** 的遍历。虽然已经是线性时间，但我们可以把这段“遍历 + 替换”的工作交给底层实现，让代码更简洁、更易读。

**核心工具**：`DataFrame.rename`  
- 这个函数接受一个 `columns` 参数，值是 **旧列名 → 新列名** 的字典。内部会一次性完成所有列名的替换。可以把它想象成一次性把一本书的目录（旧章节名）全部改成新目录（新章节名），不需要逐页手动改。

**实现步骤**：

1. 构造同样的映射字典 `rename_map`。  
2. 调用 `df.rename(columns=rename_map, inplace=False)`（`inplace=False` 表示返回一个新 DataFrame，保持函数式编程的习惯）。  
3. 直接返回结果即可。

**复杂度**：`rename` 本质上仍然是遍历列名一次，所以时间仍是 **O(n)**，但不需要我们自己额外维护列表，空间开销也只有 **O(1)**（只用一个字典）。

#### 代码（Python）

```python
import pandas as pd

def rename_columns_optimal(df: pd.DataFrame) -> pd.DataFrame:
    """
    使用 pandas 自带的 rename 方法一次性完成列重命名
    """
    # 1）映射表：旧列名 -> 新列名（类似查字典）
    rename_map = {
        "id": "student_id",
        "first": "first_name",
        "last": "last_name",
        "age": "student_age"
    }

    # 2）调用 pandas 的 rename，返回一个新的 DataFrame
    #    inplace=False 表示不在原地修改，而是返回新对象
    new_df = df.rename(columns=rename_map, inplace=False)

    return new_df
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 仍然是遍历列名一次，只是交给了 Pandas 内部实现。  
- **空间复杂度**：`O(1)` —— 只用了映射字典，未额外创建与列数等长的列表。

> 与暴力解相比，最优解的 **代码行数更少、可读性更好**，而且避免了手动维护新列名列表的错误风险。

---

## 心得

- **核心技巧**：利用 Pandas 的 `rename` 方法配合字典一次性完成列名的批量替换。  
- **适用场景**：  
  1. **列重命名**（如把数据库字段映射到业务模型字段）。  
  2. **批量修改列前缀/后缀**（如 `df.rename(lambda x: f"new_{x}")`）。  
  3. **对齐不同数据源的列名**（如合并多个 CSV 时统一列名）。  
- **一句话总结**：**“用字典配合 pandas.rename，列名批量改，一行搞定”。**

---

## 反思

- **第一反应**：看到“重命名列”，立刻想到遍历 `df.columns` 手动改。  
- **最容易踩的坑**：  
  - **忘记返回新 DataFrame**（如果使用 `inplace=False`）导致外部变量没有变化。  
  - **映射字典缺少某些旧列名**，会导致这些列保持原名，需确认字典完整。  
  - **列名大小写或空格差异**，字典键必须和原列名完全一致。  
- **下次类似题目第一步**：先在脑中构建 **“旧名 → 新名”的映射字典**，再寻找 Pandas 中是否有直接接受该字典的函数（如 `rename`、`rename_axis` 等），优先使用库函数而不是自己写循环。