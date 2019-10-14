# #620. 不无聊的电影 / Not Boring Movies

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/not-boring-movies/)

---

## 题目（英文原版）

**Description**

Table: Cinema
Write a solution to report the movies with an odd-numbered ID and a description that is not "boring".
Return the result table ordered by rating in descending order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+----------------+----------+
| Column Name    | Type     |
+----------------+----------+
| id             | int      |
| movie          | varchar  |
| description    | varchar  |
| rating         | float    |
+----------------+----------+
id is the primary key (column with unique values) for this table.
Each row contains information about the name of a movie, its genre, and its rating.
rating is a 2 decimal places float in the range [0, 10]
```

**Example 2:**

```
Input: 
Cinema table:
+----+------------+-------------+--------+
| id | movie      | description | rating |
+----+------------+-------------+--------+
| 1  | War        | great 3D    | 8.9    |
| 2  | Science    | fiction     | 8.5    |
| 3  | irish      | boring      | 6.2    |
| 4  | Ice song   | Fantacy     | 8.6    |
| 5  | House card | Interesting | 9.1    |
+----+------------+-------------+--------+
Output: 
+----+------------+-------------+--------+
| id | movie      | description | rating |
+----+------------+-------------+--------+
| 5  | House card | Interesting | 9.1    |
| 1  | War        | great 3D    | 8.9    |
+----+------------+-------------+--------+
Explanation: 
We have three movies with odd-numbered IDs: 1, 3, and 5. The movie with ID = 3 is boring so we do not include it in the answer.
```

---

## 题目（中文翻译）

**描述**  
表 (Table): `Cinema`  
编写一个查询，报告 ID 为奇数且描述 (description) 不为 `"boring"` 的电影。返回的结果表按 `rating` 降序排序。结果格式参考下方示例。

**示例 1**

表结构：

```
+----------------+----------+
| Column Name    | Type     |
+----------------+----------+
| id             | int      |
| movie          | varchar  |
| description    | varchar  |
| rating         | float    |
+----------------+----------+
```

- `id` 是该表的主键 (primary key)，具有唯一值。  
- 每行记录包含电影名称、描述以及评分。  
- `rating` 为保留两位小数的浮点数，取值范围为 `[0, 10]`。

**示例 2**

输入：

```
Cinema 表:
+----+------------+-------------+--------+
| id | movie      | description | rating |
+----+------------+-------------+--------+
| 1  | War        | great 3D    | 8.9    |
| 2  | Science    | fiction     | 8.5    |
| 3  | irish      | boring      | 6.2    |
| 4  | Ice song   | Fantacy     | 8.6    |
| 5  | House card | Interesting | 9.1    |
+----+------------+-------------+--------+
```

输出：

```
+----+------------+-------------+--------+
| id | movie      | description | rating |
+----+------------+-------------+--------+
| 5  | House card | Interesting | 9.1    |
| 1  | War        | great 3D    | 8.9    |
+----+------------+-------------+--------+
```

**解释**  
奇数 ID 的电影有 1、3、5 三部。ID 为 3 的电影描述为 `boring`，因此在答案中被排除。剩余的电影按 `rating` 降序排列，得到上述结果。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把整张 `Cinema` 表全部取出来，然后在 **Python** 里逐行检查：

1. **奇数 ID**：`id % 2 == 1`  
   - 把 `id` 除以 2，余数是 1 就是奇数。可以把它想象成“数门牌号时，只保留左边的奇数房子”。  
2. **描述不为 "boring"**：`description.lower() != "boring"`  
   - 把描述变成小写后和 `"boring"` 比较，类似于在字典里查词，若不是 “boring” 这本词条就保留下来。  
3. **按 rating 降序排列**：`sorted(..., key=lambda x: x['rating'], reverse=True)`  
   - 把符合条件的记录按照评分从高到低排，像把电影海报按照星级从高到低挂在墙上。

这种做法之所以 **正确**，是因为我们把所有可能的行都遍历了一遍，只要满足题目要求的就留下来，最后再排个序。

#### 代码（Python）  
下面的代码使用 `sqlite3` 直接在内存中创建示例表、插入数据，并用 Python 完成过滤和排序。关键行都有中文注释，复制运行即可看到结果。

```python
import sqlite3

# ------------------- 创建示例数据库（仅用于演示） -------------------
conn = sqlite3.connect(":memory:")          # 在内存中创建临时数据库
cur = conn.cursor()

# 创建 Cinema 表
cur.execute("""
CREATE TABLE Cinema (
    id INTEGER PRIMARY KEY,
    movie TEXT,
    description TEXT,
    rating REAL
)
""")

# 插入示例数据
sample_data = [
    (1, 'War',        'great 3D',    8.9),
    (2, 'Science',    'fiction',     8.5),
    (3, 'irish',      'boring',      6.2),
    (4, 'Ice song',   'Fantacy',     8.6),
    (5, 'House card', 'Interesting', 9.1)
]
cur.executemany("INSERT INTO Cinema VALUES (?,?,?,?)", sample_data)
conn.commit()

# ------------------- 暴力解（在 Python 里过滤） -------------------
# 1. 读取全部行
cur.execute("SELECT id, movie, description, rating FROM Cinema")
rows = cur.fetchall()                     # rows 是一个列表，每个元素是一个元组

# 2. 用 Python 逐行检查条件
filtered = []
for r in rows:
    id_, movie, desc, rating = r
    if id_ % 2 == 1 and desc.lower() != "boring":   # 奇数 ID 且描述不是 boring
        filtered.append({"id": id_, "movie": movie,
                         "description": desc, "rating": rating})

# 3. 按 rating 降序排序
filtered.sort(key=lambda x: x["rating"], reverse=True)

# 4. 打印结果（模拟 LeetCode 要求的输出表格）
print("| id | movie      | description | rating |")
print("|----|------------|-------------|--------|")
for rec in filtered:
    print(f"| {rec['id']}  | {rec['movie']:<10} | {rec['description']:<11} | {rec['rating']} |")
```

**运行结果**

```
| id | movie      | description | rating |
|----|------------|-------------|--------|
| 5  | House card | Interesting | 9.1 |
| 1  | War        | great 3D    | 8.9 |
```

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 读取全部行是 `O(n)`（遍历一次），过滤也是 `O(n)`，排序需要 `O(n log n)`，所以整体是 `O(n log n)`。  
  - “`n log n`” 可以想象成“把 `n` 本书先排好队（`n`），再每次把两本书合并（`log n` 次）”。  
- **空间复杂度**：`O(n)`  
  - 需要把所有符合条件的记录暂存到列表里，最坏情况下几乎所有行都满足条件，所以使用线性空间。

---

### 2. 最优解  

#### 思路  
从暴力解可以看到，**瓶颈** 出在我们把所有数据拉到 Python 里后才过滤、排序。实际上，**SQL 本身就擅长** 这些操作：  

1. **过滤**：`WHERE` 子句可以直接在数据库层面只返回满足条件的行。  
2. **奇数 ID**：`id % 2 = 1` 用取模运算筛选奇数，就像只挑选奇数号的门牌。  
3. **排除 “boring”**：`description <> 'boring'`（不等于），相当于在字典里直接把 “boring” 那一页撕掉。  
4. **排序**：`ORDER BY rating DESC` 让数据库一次性返回已经排好序的结果，省去 Python 再排序的成本。

因此，只需要一条 **SQL 查询语句** 就能一次性完成所有工作，时间复杂度降到 `O(m)`（`m` 为满足条件的记录数），空间几乎为 `O(1)`（只存返回的结果）。

下面把这条语句写在 Python 字符串里，交给 `sqlite3` 执行，展示最简洁的实现方式。

#### 代码（Python）  

```python
import sqlite3

# 假设已有名为 cinema.db 的数据库，里面已经有 Cinema 表
# 为演示，这里仍在内存中创建同样的表和数据（和上面相同）
conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.execute("""
CREATE TABLE Cinema (
    id INTEGER PRIMARY KEY,
    movie TEXT,
    description TEXT,
    rating REAL
)
""")
cur.executemany("INSERT INTO Cinema VALUES (?,?,?,?)", [
    (1, 'War',        'great 3D',    8.9),
    (2, 'Science',    'fiction',     8.5),
    (3, 'irish',      'boring',      6.2),
    (4, 'Ice song',   'Fantacy',     8.6),
    (5, 'House card', 'Interesting', 9.1)
])
conn.commit()

# ------------------- 最优解：直接用 SQL 完成所有工作 -------------------
sql = """
SELECT id, movie, description, rating
FROM Cinema
WHERE id % 2 = 1               -- 只保留奇数 ID
  AND description <> 'boring' -- 描述不是 boring
ORDER BY rating DESC;          -- 按评分降序排列
"""

cur.execute(sql)
rows = cur.fetchall()

# 打印结果（与题目要求的表格格式保持一致）
print("| id | movie      | description | rating |")
print("|----|------------|-------------|--------|")
for r in rows:
    print(f"| {r[0]}  | {r[1]:<10} | {r[2]:<11} | {r[3]} |")
```

**运行结果**

```
| id | movie      | description | rating |
|----|------------|-------------|--------|
| 5  | House card | Interesting | 9.1 |
| 1  | War        | great 3D    | 8.9 |
```

#### 复杂度  

- **时间复杂度**：`O(m)`（`m` 为满足条件的行数）  
  - 数据库只扫描一次表（`O(n)`），但只返回满足条件的 `m` 行，排序在内部使用高效的算法，整体比手动 `O(n log n)` 更快。  
- **空间复杂度**：`O(m)`（返回结果的大小）  
  - 只保留符合条件的记录，不需要额外的临时列表。

相较于暴力解，**我们把过滤和排序的工作交给了数据库**，省去了在 Python 中额外的遍历和排序步骤，运行更快、代码更简洁。

---

## 心得  

- **核心技巧**：利用 SQL 的 `WHERE`、`%`（取模）和 `ORDER BY` 完成过滤与排序。  
- **适用场景**：  
  1. 需要根据数值奇偶性筛选行（如 “奇数用户 ID”）。  
  2. 排除特定关键字的记录（如 “不含 'spam' 的邮件”。）  
  3. 按某列排序后直接返回结果的查询（如 “成绩最高的前 10 名”。）  
- **一句话总结**：**把“筛选+排序”交给数据库，一条 SQL 语句即可搞定。**  

---

## 反思  

- **第一反应**：直接把表全部取出来，用 Python 手动过滤、排序。  
- **最容易踩的坑**：  
  - 忘记把 `description` 与 `'boring'` 做不等比较，导致把 “boring” 也留下。  
  - 对奇数的判断写成 `id % 2 = 0`（其实是偶数），结果相反。  
  - 排序方向写成 `ASC`（升序），导致输出顺序不符合要求。  
- **下次类似题的第一步**：先在 **SQL** 中写出 `WHERE` 条件（奇偶、关键字过滤），再加 `ORDER BY`，确保所有筛选、排序都在数据库层完成。这样既省时又省力。