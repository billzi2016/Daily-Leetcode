# #3580. 查找持续改进的员工 / Find Consistently Improving Employees

> 难度：中等 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/find-consistently-improving-employees/)

---

## 题目（英文原版）

**Description**

Table: employees
Table: performance_reviews
Write a solution to find employees who have consistently improved their performance over their last three reviews.
Return the result table ordered by improvement score in descending order, then by name in ascending order.
The result format is in the following example.
Example:

**Examples**

**Example 1:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| employee_id | int     |
| name        | varchar |
+-------------+---------+
employee_id is the unique identifier for this table.
Each row contains information about an employee.
```

**Example 2:**

```
+-------------+------+
| Column Name | Type |
+-------------+------+
| review_id   | int  |
| employee_id | int  |
| review_date | date |
| rating      | int  |
+-------------+------+
review_id is the unique identifier for this table.
Each row represents a performance review for an employee. The rating is on a scale of 1-5 where 5 is excellent and 1 is poor.
```

**Example 3:**

```
+-------------+----------------+
| employee_id | name           |
+-------------+----------------+
| 1           | Alice Johnson  |
| 2           | Bob Smith      |
| 3           | Carol Davis    |
| 4           | David Wilson   |
| 5           | Emma Brown     |
+-------------+----------------+
```

**Example 4:**

```
+-----------+-------------+-------------+--------+
| review_id | employee_id | review_date | rating |
+-----------+-------------+-------------+--------+
| 1         | 1           | 2023-01-15  | 2      |
| 2         | 1           | 2023-04-15  | 3      |
| 3         | 1           | 2023-07-15  | 4      |
| 4         | 1           | 2023-10-15  | 5      |
| 5         | 2           | 2023-02-01  | 3      |
| 6         | 2           | 2023-05-01  | 2      |
| 7         | 2           | 2023-08-01  | 4      |
| 8         | 2           | 2023-11-01  | 5      |
| 9         | 3           | 2023-03-10  | 1      |
| 10        | 3           | 2023-06-10  | 2      |
| 11        | 3           | 2023-09-10  | 3      |
| 12        | 3           | 2023-12-10  | 4      |
| 13        | 4           | 2023-01-20  | 4      |
| 14        | 4           | 2023-04-20  | 4      |
| 15        | 4           | 2023-07-20  | 4      |
| 16        | 5           | 2023-02-15  | 3      |
| 17        | 5           | 2023-05-15  | 2      |
+-----------+-------------+-------------+--------+
```

**Example 5:**

```
+-------------+----------------+-------------------+
| employee_id | name           | improvement_score |
+-------------+----------------+-------------------+
| 2           | Bob Smith      | 3                 |
| 1           | Alice Johnson  | 2                 |
| 3           | Carol Davis    | 2                 |
+-------------+----------------+-------------------+
```

---

## 题目（中文翻译）

编写一个查询，找出在最近三次绩效评估（performance_reviews）中成绩持续提升的员工。  
返回的结果表按 **improvement_score**（改进分数）降序排列，若分数相同则按 **name**（姓名）升序排列。  
结果格式参照下例。

**示例 1：**  
```sql
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| employee_id | int     |
| name        | varchar |
+-------------+---------+
```
`employee_id` 为该表的唯一标识。每行记录一名员工的信息。

**示例 2：**  
```sql
+-------------+------+
| Column Name | Type |
+-------------+------+
| review_id   | int  |
| employee_id | int  |
| review_date | date |
| rating      | int  |
+-------------+------+
```
`review_id` 为该表的唯一标识。每行记录一次员工的绩效评估（performance review）。`rating` 的取值范围为 1‑5，5 表示优秀，1 表示差。

**示例 3：**  
```sql
+-------------+----------------+
| employee_id | name           |
+-------------+----------------+
| 1           | Alice Johnson  |
| 2           | Bob Smith      |
| 3           | Carol Davis    |
| 4           | David Wilson   |
| 5           | Emma Brown     |
+-------------+----------------+
```

**示例 4：**  
```sql
+-----------+-------------+-------------+--------+
| review_id | employee_id | review_date | rating |
+-----------+-------------+-------------+--------+
| 1         | 1           | 2023-01-15  | 2      |
| 2         | 1           | 2023-04-15  | 3      |
| 3         | 1           | 2023-07-15  | 4      |
| 4         | 1           | 2023-10-15  | 5      |
| 5         | 2           | 2023-02-01  | 3      |
... (已截断)
```

**示例 5（输出）：**  
```sql
+-------------+----------------+-------------------+
| employee_id | name           | improvement_score |
+-------------+----------------+-------------------+
| 2           | Bob Smith      | 3                 |
| 1           | Alice Johnson  | 2                 |
| 3           | Carol Davis    | 2                 |
+-------------+----------------+-------------------+
```

**约束条件：**  
- 无其他约束。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把两张表都读进来，然后**逐个员工**检查他的最近三次评估是否呈递增趋势。  
可以把 `performance_reviews` 看成一本“成绩册”，每一行是某位员工在某一天的分数。  
我们把这本册子先**按日期排序**（就像把成绩单按照时间顺序排好），再把同一个 `employee_id` 的记录放到一起（这一步类似于把同一本成绩册按学生姓名分组）。  

对每个员工的成绩序列：

1. 取最近的三条记录（即日期最大的三条）。  
2. 看这三条记录的 `rating` 是否满足 `r1 < r2 < r3`（从旧到新一直在提高）。  
3. 如果满足，就把该员工的 **提升分数**记为 `r3 - r1`（最新评分减去最早评分），随后把 `employee_id`、`name`、`improvement_score` 加入答案。  

> **为什么这个方法一定对？**  
> - 我们先把所有记录按日期排序，确保“最近的三条”一定是最新的三次评估。  
> - 只要这三次评分严格递增，说明员工在这段时间里一直在进步。  
> - 计算 `r3 - r1` 正好等于“提升了多少分”。  

**时间/空间复杂度**（大白话）  
- 假设总共有 `n` 条评估记录，`m` 位员工。  
- 先对全部记录**排序**需要 `O(n log n)`（把所有记录排成一本时间顺序的账本）。  
- 然后遍历一次把记录分组、检查每个员工的最近三条，整体是线性 `O(n)`。  
- 所以总时间是 `O(n log n)`，主要花在排序上。  
- 我们额外用几个字典来存放分组信息，最多保存所有记录一次，空间是 `O(n)`。  

#### 代码（Python）  

```python
# 假设已经从数据库中读取出两张表，分别放在 list of dict 中
employees = [
    # 示例数据
    {"employee_id": 1, "name": "Alice Johnson"},
    {"employee_id": 2, "name": "Bob Smith"},
    {"employee_id": 3, "name": "Carol Davis"},
    # ...
]

performance_reviews = [
    # 示例数据（review_id, employee_id, review_date, rating）
    {"review_id": 1, "employee_id": 1, "review_date": "2023-01-15", "rating": 2},
    {"review_id": 2, "employee_id": 1, "review_date": "2023-04-15", "rating": 3},
    {"review_id": 3, "employee_id": 1, "review_date": "2023-07-15", "rating": 4},
    {"review_id": 4, "employee_id": 1, "review_date": "2023-10-15", "rating": 5},
    {"review_id": 5, "employee_id": 2, "review_date": "2023-02-01", "rating": 1},
    {"review_id": 6, "employee_id": 2, "review_date": "2023-05-01", "rating": 2},
    {"review_id": 7, "employee_id": 2, "review_date": "2023-08-01", "rating": 4},
    # ...
]

# -------------------------------------------------------------
# 1️⃣ 把评估记录按日期升序排好（最早 → 最晚）
# -------------------------------------------------------------
performance_reviews.sort(key=lambda r: r["review_date"])

# 2️⃣ 建立 employee_id → name 的映射，方便后面查名字
id_to_name = {e["employee_id"]: e["name"] for e in employees}

# 3️⃣ 用字典把所有评估按员工分组，保存为一个有序列表（已经是时间顺序的）
from collections import defaultdict
grouped = defaultdict(list)          # employee_id -> list of (date, rating)

for rev in performance_reviews:
    grouped[rev["employee_id"]].append((rev["review_date"], rev["rating"]))

# 4️⃣ 遍历每个员工，检查最近三次是否递增
result = []   # 最终要返回的列表

for emp_id, records in grouped.items():
    if len(records) < 3:            # 记录不足三条，直接跳过
        continue

    # 取最近的三条（列表已经是时间顺序，取最后三条即可）
    last_three = records[-3:]       # [(date1, r1), (date2, r2), (date3, r3)]

    r1 = last_three[0][1]
    r2 = last_three[1][1]
    r3 = last_three[2][1]

    # 判断是否严格递增
    if r1 < r2 < r3:
        improvement = r3 - r1       # 提升分数
        result.append({
            "employee_id": emp_id,
            "name": id_to_name[emp_id],
            "improvement_score": improvement
        })

# 5️⃣ 按要求排序：提升分数降序 → 姓名升序
result.sort(key=lambda x: (-x["improvement_score"], x["name"]))

# 打印或返回结果
for row in result:
    print(row)
```

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 主要是对 `n` 条评估记录的排序（`log n` 是排序的“层数”，相当于把 1 万条记录排好顺序大约需要 14 次比较层）。  
- **空间复杂度**：`O(n)`  
  - 需要额外的字典保存所有记录的分组信息，最坏情况下要存一遍所有评估记录。

---

### 2. 最优解  

#### 思路  

在暴力解中，**瓶颈**在于我们先对全部记录整体排序，然后再遍历一次。  
如果数据量非常大（比如上千万条评估），一次全局排序会比较耗时。  

观察到：**我们只关心每个员工的最近三条记录**，不需要把所有员工的记录全部排好顺序，只要在插入新记录时能够快速得到该员工的最新三条就行。  

可以采用 **“滑动窗口 + 小根堆（或固定大小的列表）”** 的思路：

1. **按 `employee_id` 分组**（不必排序），对每个员工维护一个长度不超过 3 的列表 `last_three`，始终保存最近的三条评估。  
2. 在遍历 `performance_reviews` 时，先把记录按 `review_date` **升序**插入对应员工的列表（如果列表已经有 3 条，弹出最早的那条）。  
   - 这里我们不必一次性把所有记录排序，只要把原始记录 **一次遍历**并在插入时保持列表有序即可。  
   - 为了保证插入后仍然是按日期升序，可以使用 `bisect.insort`（二分插入），时间是 `O(log 3) = O(1)`，因为列表最多 3 长。  
3. 当遍历结束后，每个员工的 `last_three` 正好是 **最近的三条记录（已排好序）**。  
4. 再遍历这些列表，检查 `rating` 是否严格递增并计算提升分数。  

这样我们 **只遍历一次原始记录**（`O(n)`），不需要一次性对全部记录做 `O(n log n)` 的全局排序。  

> **核心数据结构解释**  
> - **字典（哈希表）**：像一本电话簿，`employee_id` 是名字，对应的值是这位员工的“最近三条评估”。查找和插入都非常快，平均是 `O(1)`。  
> - **固定长度列表 + 二分插入**：因为列表最多只有 3 条，插入、删除都可以看作常数时间操作。我们用 `bisect` 的二分搜索来保持日期顺序，类似于把新成绩放进已经排好序的成绩单中。

#### 代码（Python）  

```python
from collections import defaultdict
import bisect

# ------------------- 输入数据（同上） -------------------
employees = [
    {"employee_id": 1, "name": "Alice Johnson"},
    {"employee_id": 2, "name": "Bob Smith"},
    {"employee_id": 3, "name": "Carol Davis"},
    # ...
]

performance_reviews = [
    {"review_id": 1, "employee_id": 1, "review_date": "2023-01-15", "rating": 2},
    {"review_id": 2, "employee_id": 1, "review_date": "2023-04-15", "rating": 3},
    {"review_id": 3, "employee_id": 1, "review_date": "2023-07-15", "rating": 4},
    {"review_id": 4, "employee_id": 1, "review_date": "2023-10-15", "rating": 5},
    {"review_id": 5, "employee_id": 2, "review_date": "2023-02-01", "rating": 1},
    {"review_id": 6, "employee_id": 2, "review_date": "2023-05-01", "rating": 2},
    {"review_id": 7, "employee_id": 2, "review_date": "2023-08-01", "rating": 4},
    # ...
]

# -------------------------------------------------------------
# 1️⃣ 建立 employee_id → name 的映射
# -------------------------------------------------------------
id_to_name = {e["employee_id"]: e["name"] for e in employees}

# 2️⃣ 用字典保存每位员工的最近三条评估（列表里保存 (date, rating)）
last_three_map = defaultdict(list)   # employee_id -> [(date, rating), ...]

# 3️⃣ 遍历所有评估记录，实时维护「最近三条」窗口
for rev in performance_reviews:
    emp_id = rev["employee_id"]
    date = rev["review_date"]
    rating = rev["rating"]

    # 在已有的列表里二分插入，使列表保持日期升序
    # 因为列表长度 ≤ 3，时间可以视作 O(1)
    bisect.insort(last_three_map[emp_id], (date, rating))

    # 如果插入后列表超过 3 条，弹出最早的那条（列表第 0 位）
    if len(last_three_map[emp_id]) > 3:
        last_three_map[emp_id].pop(0)

# 4️⃣ 检查每位员工的窗口是否满足递增条件，并计算提升分数
result = []
for emp_id, records in last_three_map.items():
    if len(records) < 3:
        continue          # 记录不足三条，直接跳过

    r1 = records[0][1]   # 最早的 rating
    r2 = records[1][1]
    r3 = records[2][1]   # 最近的 rating

    if r1 < r2 < r3:     # 严格递增 → 持续改进
        improvement = r3 - r1
        result.append({
            "employee_id": emp_id,
            "name": id_to_name[emp_id],
            "improvement_score": improvement
        })

# 5️⃣ 按要求排序：提升分数降序 → 姓名升序
result.sort(key=lambda x: (-x["improvement_score"], x["name"]))

# 输出
for row in result:
    print(row)
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历一次 `performance_reviews`（`n` 条记录），每条记录的插入、弹出操作都是常数时间（列表长度永远 ≤ 3）。  
  - 最后再遍历每位员工一次，最多 `m` 次（`m ≤ n`），仍然是线性。  
  - 与暴力解相比，省去了 `O(n log n)` 的全局排序，速度提升明显。  

- **空间复杂度**：`O(m)`  
  - 我们只为每位员工保存最多 3 条记录，整体空间是员工数乘以常数 3，远小于保存全部记录的 `O(n)`。  

---

## 心得  

- **核心技巧**：对每个分组（员工）维护**固定长度的滑动窗口**，实时更新最近的 K 条数据。  
- **适用场景**：  
  1. “最近 N 条交易/日志/评价”类问题（如找出最近 5 笔订单的总金额）。  
  2. “连续 K 天/记录满足某条件”问题（如连续 3 天温度递增）。  
  3. “流式数据的实时 Top‑K”问题（如实时监控最近 10 条日志中的错误码分布）。  
- **一句话总结**：  
  *把“只关心最近几条”转化为每个键的长度为 3 的滑动窗口，既省时又省空间。*

---

## 反思  

- **第一反应**：直接把所有评估按日期排序，然后逐个员工检查——这就是暴力解。  
- **最容易踩的坑**：  
  - **日期排序方向**：一定要保证取的是“最近的三次”，否则会误判。  
  - **严格递增**：`<` 而不是 `<=`，否则相同分数会被误认为是提升。  
  - **员工记录不足三次**：要提前过滤，否则会出现索引错误。  
- **下次遇到同类题**：第一步先**确定窗口大小 K**（本题是 3），再想办法**在遍历过程中实时维护这 K 条最新记录**，而不是一次性全局排序。这样往往能把时间复杂度从 `O(n log n)` 降到 `O(n)`。