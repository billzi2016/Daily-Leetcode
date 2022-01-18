# #1633. 参加比赛的用户比例 / Percentage of Users Attended a Contest

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/percentage-of-users-attended-a-contest/)

---

## 题目（英文原版）

**Description**

Table: Users
Table: Register
Write a solution to find the percentage of the users registered in each contest rounded to two decimals.
Return the result table ordered by percentage in descending order. In case of a tie, order it by contest_id in ascending order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| user_id     | int     |
| user_name   | varchar |
+-------------+---------+
user_id is the primary key (column with unique values) for this table.
Each row of this table contains the name and the id of a user.
```

**Example 2:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| contest_id  | int     |
| user_id     | int     |
+-------------+---------+
(contest_id, user_id) is the primary key (combination of columns with unique values) for this table.
Each row of this table contains the id of a user and the contest they registered into.
```

**Example 3:**

```
Input: 
Users table:
+---------+-----------+
| user_id | user_name |
+---------+-----------+
| 6       | Alice     |
| 2       | Bob       |
| 7       | Alex      |
+---------+-----------+
Register table:
+------------+---------+
| contest_id | user_id |
+------------+---------+
| 215        | 6       |
| 209        | 2       |
| 208        | 2       |
| 210        | 6       |
| 208        | 6       |
| 209        | 7       |
| 209        | 6       |
| 215        | 7       |
| 208        | 7       |
| 210        | 2       |
| 207        | 2       |
| 210        | 7       |
+------------+---------+
Output: 
+------------+------------+
| contest_id | percentage |
+------------+------------+
| 208        | 100.0      |
| 209        | 100.0      |
| 210        | 100.0      |
| 215        | 66.67      |
| 207        | 33.33      |
+------------+------------+
Explanation: 
All the users registered in contests 208, 209, and 210. The percentage is 100% and we sort them in the answer table by contest_id in ascending order.
Alice and Alex registered in contest 215 and the percentage is ((2/3) * 100) = 66.67%
Bob registered in contest 207 and the percentage is ((1/3) * 100) = 33.33%
```

---

## 题目（中文翻译）

**描述**  
表 `Users`  
| 列名 | 类型 |
|------|------|
| user_id | int |
| user_name | varchar |

`user_id` 为主键（primary key），即唯一值列。每行记录一个用户的 ID 与姓名。

表 `Register`  
| 列名 | 类型 |
|------|------|
| contest_id | int |
| user_id | int |

`(contest_id, user_id)` 为主键（primary key），即唯一值组合列。每行记录一个用户参加的比赛 ID。

编写查询，计算每场比赛的 **百分比（percentage）** —— 参赛用户数占全部用户数的比例，结果保留两位小数（四舍五入）。返回结果表按 **百分比（percentage）** 降序排列；若出现相同的百分比，则按 `contest_id` 升序排列。结果格式参照下例。

**示例 1**

`Users` 表：

```
+---------+-----------+
| user_id | user_name |
+---------+-----------+
| 6       | Alice     |
| 2       | Bob       |
| 7       | Alex      |
+---------+-----------+
```

`Register` 表：

```
+------------+---------+
| contest_id | user_id |
+------------+---------+
| 215        | 6       |
| 209        | 2       |
| 208        | 2       |
| 210        | 6       |
| 208        | 6       |
... (已截断)
```

**约束条件**  
- 表中数据量均在合理范围内，保证查询能够在合理时间内完成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：

1. 先把 **Users** 表的所有用户 `user_id` 放进一个列表 `all_users`，这相当于把所有“人”都记下来。  
2. 再把 **Register** 表的每一条记录（`contest_id, user_id`）拿出来，遍历所有比赛 `contest_id`，对每个比赛逐个检查 **所有用户** 是否在该比赛里出现过。  
   - 这一步可以想象成“老师点名”。老师要点名每一场比赛的每一个学生，看看他是不是已经报名了。  
3. 把每场比赛的报名人数除以总用户数，再乘以 100，得到百分比并保留两位小数。

> **为什么这个方法能得到正确答案？**  
> 因为我们没有遗漏任何用户，也没有遗漏任何比赛的报名记录，逐一计数自然得到准确的比例。

> **时间/空间复杂度**  
> - 时间复杂度：`O(C * U)`，其中 `C` 是比赛的种类数，`U` 是用户总数。  
>   - 用大白话解释，就是“如果有 10 场比赛，1000 个用户，就要做 10 × 1000 = 1 万次检查”。  
> - 空间复杂度：`O(U + R)`，`R` 为报名记录数。我们需要把用户列表和报名表都放进内存，除此之外不需要额外的结构。

#### 代码（Python）

```python
from typing import List, Tuple
from collections import defaultdict

# ------------------- 模拟数据 -------------------
# Users 表：[(user_id, user_name), ...]
users: List[Tuple[int, str]] = [
    (6, "Alice"),
    (2, "Bob"),
    (7, "Alex"),
]

# Register 表：[(contest_id, user_id), ...]
registers: List[Tuple[int, int]] = [
    (215, 6),
    (209, 2),
    (208, 2),
    (210, 6),
    (208, 6),
    # ... 这里可能还有更多记录
]
# ------------------------------------------------

def brute_force_percentage(users, registers):
    """
    暴力解：对每个比赛遍历所有用户，统计该比赛的报名人数。
    返回 [(contest_id, percentage_str), ...]，percentage_str 已经保留两位小数。
    """
    total_users = len(users)                     # 用户总数
    # 把所有的 contest_id 收集起来（去重）
    contests = {c for c, _ in registers}

    result = []
    for contest_id in contests:                  # 对每场比赛
        cnt = 0                                   # 该场比赛的报名人数
        for _, user_id in registers:            # 遍历所有报名记录
            if user_id == _ and contest_id == contest_id:
                # 这里的 if 永远为 True，写法仅为演示遍历所有用户的思想
                pass
        # 正式做法：遍历所有用户，检查该用户是否在该比赛的报名记录里
        for user_id, _ in users:
            # 用一个生成式判断 (contest_id, user_id) 是否出现在 registers 中
            if any(c == contest_id and u == user_id for c, u in registers):
                cnt += 1

        # 计算百分比，保留两位小数
        percent = round(cnt * 100 / total_users + 1e-9, 2)  # +1e-9 防止四舍五入误差
        result.append((contest_id, f"{percent:.2f}"))
    # 按要求排序：先按百分比降序，再按 contest_id 升序
    result.sort(key=lambda x: (-float(x[1]), x[0]))
    return result

# 示例运行
print(brute_force_percentage(users, registers))
```

> **关键行中文注释**  
> - `total_users = len(users)`：统计总用户数，相当于“全班有多少人”。  
> - `contests = {c for c, _ in registers}`：把所有出现过的比赛编号收集到集合里，去掉重复。  
> - `if any(c == contest_id and u == user_id for c, u in registers):`：检查当前用户是否在当前比赛的报名表里。  
> - `round(..., 2)`：四舍五入保留两位小数。  
> - `result.sort(key=lambda x: (-float(x[1]), x[0]))`：先让百分比大的排前面，若相同再让 `contest_id` 小的排前面。

#### 复杂度

- **时间复杂度**：`O(C * U * R)`（最坏情况下 `any` 需要遍历全部报名记录），在实际数据量不大时还能接受，但随着用户数、比赛数、报名记录数的增长会非常慢。  
- **空间复杂度**：`O(C + U + R)`，主要是保存原始表和结果列表。

---

### 2. 最优解

#### 思路  

从暴力解出发，我们可以看到 **瓶颈** 出在：

- 对每个 `(contest, user)` 组合都要遍历一次完整的报名表，导致重复的检查非常多。

**优化思路**：

1. **一次遍历 Register 表**，统计每个 `contest_id` 的报名人数。  
   - 这相当于“老师只点名一次，把每个学生的报名信息记录下来”。  
   - 使用 **字典（哈希表）**：`cnt[contest_id] = 已报名人数`。字典查找的时间复杂度是 **O(1)**，就像在字典里查单词，瞬间就能找到对应的页码。  
2. **总用户数** 只需要在 Users 表里数一次 `len(users)`。  
3. 计算百分比：`percentage = cnt / total_users * 100`，并用 `round(..., 2)` 保留两位小数。  
4. 最后按照题目要求的顺序排序：  
   - 先按百分比降序  
   - 再按 `contest_id` 升序（如果百分比相同）

整个过程只遍历两张表一次，时间大幅降低到 **线性**。

#### 代码（Python）

```python
from typing import List, Tuple
from collections import defaultdict

# ------------------- 模拟数据（同上） -------------------
users: List[Tuple[int, str]] = [
    (6, "Alice"),
    (2, "Bob"),
    (7, "Alex"),
]

registers: List[Tuple[int, int]] = [
    (215, 6),
    (209, 2),
    (208, 2),
    (210, 6),
    (208, 6),
    # ... 可能还有更多
]
# --------------------------------------------------------

def optimal_percentage(users: List[Tuple[int, str]],
                       registers: List[Tuple[int, int]]) -> List[Tuple[int, str]]:
    """
    最优解：一次遍历 Register 表统计每场比赛的报名人数。
    返回 [(contest_id, percentage_str), ...]，已按要求排序。
    """
    total_users = len(users)                     # 1️⃣ 统计总用户数
    contest_cnt = defaultdict(int)              # 2️⃣ 用字典统计每场比赛的报名人数

    # 只遍历一次 Register 表
    for contest_id, _ in registers:
        contest_cnt[contest_id] += 1             # 哈希表的写入是 O(1)

    # 计算百分比并转成字符串，保留两位小数
    result = []
    for contest_id, cnt in contest_cnt.items():
        percent = round(cnt * 100 / total_users + 1e-9, 2)
        result.append((contest_id, f"{percent:.2f}"))

    # 3️⃣ 排序：先按百分比降序，再按 contest_id 升序
    result.sort(key=lambda x: (-float(x[1]), x[0]))
    return result

# 示例运行
print(optimal_percentage(users, registers))
```

> **关键行中文注释**  
> - `contest_cnt = defaultdict(int)`：创建一个默认值为 0 的字典，相当于“每场比赛的报名人数从 0 开始”。  
> - `contest_cnt[contest_id] += 1`：遍历一次报名表，就把对应比赛的计数加一。  
> - `round(cnt * 100 / total_users + 1e-9, 2)`：先算出比例（`cnt / total_users`），乘 100 再保留两位小数。  
> - `result.sort(key=lambda x: (-float(x[1]), x[0]))`：负号让大比例排前面，`float(x[1])` 把字符串转回数值比较。

#### 复杂度

- **时间复杂度**：`O(U + R + C log C)`  
  - `U` 为 Users 表的行数（只用来算总数），`R` 为 Register 表的行数（一次遍历），`C` 为不同比赛的数量（最后的排序需要 `C log C`）。  
  - 与暴力解的 `O(C * U * R)` 相比，提升巨大，几乎是线性时间。  
- **空间复杂度**：`O(C)`  
  - 只需要保存每场比赛的计数，和最终的结果列表。  

---

## 心得

- **核心技巧**：**哈希表（字典）一次遍历计数**，再结合 **排序** 完成统计。  
- **适用的题型**  
  1. “每个部门的员工比例” 类似的 **分组计数** 题。  
  2. “每个商品的销量占比” 等 **聚合统计** 场景。  
  3. “每个城市的用户活跃度” 等 **分组后求比例** 的查询。  
- **一句话总结解题钥匙**：**“把所有需要统计的对象一次性放进哈希表，省掉重复遍历的代价”。**

---

## 反思

- **第一反应**：看到“每个比赛的用户百分比”，立刻想到 **SQL 的 GROUP BY**，但因为要用 Python，就把思路转化为 “遍历一次表，使用字典计数”。  
- **最容易踩的坑**  
  - **除以零**：如果 Users 表为空，需要先判断 `total_users > 0`，否则会出现除零错误。  
  - **四舍五入误差**：直接使用 `round` 可能出现 `0.005` 被向下取整的情况，加入极小的 `1e-9` 可以避免大多数误差。  
  - **排序时的类型**：百分比先转成 `float` 再取负号，否则字符串比较会得到错误的顺序。  
- **下次遇到同类题**，第一步应该想到 **“先统计每个分组的计数，用哈希表一次遍历”**，再在此基础上做比例或其他衍生计算。