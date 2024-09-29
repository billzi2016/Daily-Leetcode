# #2882. 删除重复行 / Drop Duplicate Rows

> 难度：简单 · 标签： · [LeetCode 链接](https://leetcode.com/problems/drop-duplicate-rows/)

---

## 题目（英文原版）

**Description**

There are some duplicate rows in the DataFrame based on the email column.
Write a solution to remove these duplicate rows and keep only the first occurrence.
The result format is in the following example.

**Examples**

**Example 1:**

```
DataFrame customers
+-------------+--------+
| Column Name | Type   |
+-------------+--------+
| customer_id | int    |
| name        | object |
| email       | object |
+-------------+--------+
```

**Example 2:**

```
Example 1:
Input:
+-------------+---------+---------------------+
| customer_id | name    | email               |
+-------------+---------+---------------------+
| 1           | Ella    | emily@example.com   |
| 2           | David   | michael@example.com |
| 3           | Zachary | sarah@example.com   |
| 4           | Alice   | john@example.com    |
| 5           | Finn    | john@example.com    |
| 6           | Violet  | alice@example.com   |
+-------------+---------+---------------------+
Output:  
+-------------+---------+---------------------+
| customer_id | name    | email               |
+-------------+---------+---------------------+
| 1           | Ella    | emily@example.com   |
| 2           | David   | michael@example.com |
| 3           | Zachary | sarah@example.com   |
| 4           | Alice   | john@example.com    |
| 6           | Violet  | alice@example.com   |
+-------------+---------+---------------------+
Explanation:
Alic (customer_id = 4) and Finn (customer_id = 5) both use john@example.com, so only the first occurrence of this email is retained.
```

---

## 题目（中文翻译）

有些行在 `email` 列上是重复的。  
请编写一个解决方案，删除这些重复行，只保留第一次出现的记录。  
结果格式请参考下面的示例。

**示例 1**  
DataFrame `customers`

| Column Name | Type   |
|-------------|--------|
| customer_id | int    |
| name        | object |
| email       | object |

**示例 2**  
Example 1:

**输入：**

| customer_id | name    | email               |
|-------------|---------|---------------------|
| 1           | Ella    | emily@example.com   |
| 2           | David   | michael@example.com |
| 3           | Zachary | sarah@example.com   |
| 4           | Alice   | john@example.com    |
| 5           | Finn    | john@example.com    |
| ...         | ...     | ...                 |

**约束条件**  
无

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **遍历整张表**，把已经出现过的 `email` 记下来，遇到相同的 `email` 就跳过。  
- **数据结构**：使用 `set`（集合）来保存已经出现的邮箱，集合就像一本“已经标记的字典”，查找是否已经存在的时间非常快（常数级 O(1)）。
- **为什么正确**：因为题目要求 **只保留第一次出现的那一行**，只要我们在遍历时按照顺序记录第一次出现的邮箱，并且在后面遇到相同邮箱时不再加入结果，就能得到正确的去重表。
- **时间/空间复杂度**：我们需要遍历所有行一次，所以时间是 **O(n)**（n 为行数），每遇到一个新邮箱就往集合里放一个元素，最坏情况下所有邮箱都不重复，需要额外的 **O(n)** 空间来存放集合和结果列表。  

> 大白话：如果有 1000 条记录，程序会看一遍这 1000 条（一次遍历），每次检查 “这邮箱之前出现过吗？” 只需要在集合里找一下，几乎不花时间。

#### 代码（Python）

```python
import pandas as pd

def drop_duplicate_rows_brute(df: pd.DataFrame) -> pd.DataFrame:
    """
    暴力实现：手动遍历 DataFrame，使用 set 记录已经出现的 email。
    只保留第一次出现的那一行。
    """
    seen_emails = set()          # 用来存放已经出现过的邮箱
    rows_to_keep = []            # 保存需要保留的行（以 dict 形式）

    # 按行遍历 DataFrame，df.itertuples() 的速度比 df.iterrows() 更快
    for row in df.itertuples(index=False, name=None):
        # row 的顺序和列的顺序保持一致，例如 (customer_id, name, email)
        email = row[2]            # 第三列是 email
        if email not in seen_emails:   # 只要这封邮件之前没出现过
            seen_emails.add(email)     # 记下来，防止后面再加入
            rows_to_keep.append(row)   # 这行保留下来

    # 用保留下来的数据重新创建一个 DataFrame，列名保持不变
    result = pd.DataFrame(rows_to_keep, columns=df.columns)
    return result
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  解释：程序只需要遍历一次所有行，每次检查集合里是否已经有该邮箱，集合的查找是常数时间，所以整体是线性时间。
- **空间复杂度**：`O(n)`  
  解释：最坏情况下所有邮箱都不重复，需要把每一行都存进 `rows_to_keep`，以及把每个邮箱放进 `seen_emails`，因此额外使用的空间与行数成正比。

---

### 2. 最优解

#### 思路  

Pandas 已经为我们实现了 **去重** 的高效函数 `drop_duplicates`，它内部已经做了很多底层优化（C 语言实现、向量化操作），速度远快于纯 Python 循环。  
- **瓶颈所在**：在暴力解中，我们用了 Python 循环逐行检查，这在大数据集上会非常慢，因为每次循环都要进入 Python 解释器。
- **优化思路**：直接交给 Pandas，让它一次性在 C 层面完成去重，只需要指定依据的列 `email`，并告诉它保留第一次出现的记录（`keep='first'`）。
- **核心函数**：`DataFrame.drop_duplicates(subset=['email'], keep='first')`  
  - `subset` 指定根据哪几列判断重复，这里只看 `email`。  
  - `keep='first'` 表示保留第一次出现的那一行，后面的重复行全部删除。  

> 类比：把整个表当作一本电话簿，`drop_duplicates` 就像一本“去重机”，一次性把所有重复的电话号码挑出来，省去了我们手动一行行检查的麻烦。

#### 代码（Python）

```python
import pandas as pd

def drop_duplicate_rows_optimal(df: pd.DataFrame) -> pd.DataFrame:
    """
    最优实现：直接使用 pandas 内置的 drop_duplicates 方法。
    参数说明：
        subset=['email']   → 只根据 email 列判断重复
        keep='first'       → 保留第一次出现的那一行
    返回值是一个已经去重后的 DataFrame（不改变原始 df）。
    """
    # pandas 的 drop_duplicates 在内部使用了高效的向量化运算
    result = df.drop_duplicates(subset=['email'], keep='first')
    return result
```

#### 复杂度

- **时间复杂度**：`O(n)`（在实现细节上更快）  
  解释：虽然理论上仍然需要查看每一行，但所有操作都是在底层 C 实现的向量化代码中完成，实际运行时间常数因子要远小于 Python 循环。  
- **空间复杂度**：`O(n)`（创建新表的开销）  
  解释：`drop_duplicates` 会返回一个新的 DataFrame，最坏情况下所有行都保留，需要额外的 O(n) 空间。但相比手动保存行的方式，它的内存布局更紧凑，且不需要额外的 Python 对象（如 `set`）。

---

## 心得

- **核心技巧**：利用 Pandas 的 **向量化去重函数** `drop_duplicates`，一次性完成基于指定列的去重。
- **适用题型**  
  1. “删除重复记录” 类的题目（例如根据用户名、手机号去重）。  
  2. “保留唯一键的第一条/最后一条记录” 场景（如日志文件中同一用户的首次登录记录）。  
  3. “基于多列组合键去重” （例如同时考虑 `city` 与 `date`）。
- **一句话总结解题钥匙**：**让库来做 heavy lifting**——当有现成的高效库函数时，直接调用而不是自己写循环。

## 反思

- **第一反应**：看到“去重”，立刻想到遍历+集合的朴素实现。  
- **最容易踩的坑**  
  - 忘记指定 `subset` 参数，导致整行都相同才会被认为是重复。  
  - 误以为 `drop_duplicates` 会在原地修改，需要注意它返回的是新对象（除非 `inplace=True`）。  
  - 对空 DataFrame 或全部行均相同的极端情况没有提前测试。  
- **下次类似题的第一步**：先检查语言/库是否提供 **专门的去重函数**，如果有，就直接使用；如果没有，再考虑手动遍历加哈希表的方案。