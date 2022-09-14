# #1934. 确认率 / Confirmation Rate

> 难度：中等 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/confirmation-rate/)

---

## 题目（英文原版）

**Description**

Table: Signups
Table: Confirmations
The confirmation rate of a user is the number of 'confirmed' messages divided by the total number of requested confirmation messages. The confirmation rate of a user that did not request any confirmation messages is 0. Round the confirmation rate to two decimal places.
Write a solution to find the confirmation rate of each user.
Return the result table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+----------------+----------+
| Column Name    | Type     |
+----------------+----------+
| user_id        | int      |
| time_stamp     | datetime |
+----------------+----------+
user_id is the column of unique values for this table.
Each row contains information about the signup time for the user with ID user_id.
```

**Example 2:**

```
+----------------+----------+
| Column Name    | Type     |
+----------------+----------+
| user_id        | int      |
| time_stamp     | datetime |
| action         | ENUM     |
+----------------+----------+
(user_id, time_stamp) is the primary key (combination of columns with unique values) for this table.
user_id is a foreign key (reference column) to the Signups table.
action is an ENUM (category) of the type ('confirmed', 'timeout')
Each row of this table indicates that the user with ID user_id requested a confirmation message at time_stamp and that confirmation message was either confirmed ('confirmed') or expired without confirming ('timeout').
```

**Example 3:**

```
Input: 
Signups table:
+---------+---------------------+
| user_id | time_stamp          |
+---------+---------------------+
| 3       | 2020-03-21 10:16:13 |
| 7       | 2020-01-04 13:57:59 |
| 2       | 2020-07-29 23:09:44 |
| 6       | 2020-12-09 10:39:37 |
+---------+---------------------+
Confirmations table:
+---------+---------------------+-----------+
| user_id | time_stamp          | action    |
+---------+---------------------+-----------+
| 3       | 2021-01-06 03:30:46 | timeout   |
| 3       | 2021-07-14 14:00:00 | timeout   |
| 7       | 2021-06-12 11:57:29 | confirmed |
| 7       | 2021-06-13 12:58:28 | confirmed |
| 7       | 2021-06-14 13:59:27 | confirmed |
| 2       | 2021-01-22 00:00:00 | confirmed |
| 2       | 2021-02-28 23:59:59 | timeout   |
+---------+---------------------+-----------+
Output: 
+---------+-------------------+
| user_id | confirmation_rate |
+---------+-------------------+
| 6       | 0.00              |
| 3       | 0.00              |
| 7       | 1.00              |
| 2       | 0.50              |
+---------+-------------------+
Explanation: 
User 6 did not request any confirmation messages. The confirmation rate is 0.
User 3 made 2 requests and both timed out. The confirmation rate is 0.
User 7 made 3 requests and all were confirmed. The confirmation rate is 1.
User 2 made 2 requests where one was confirmed and the other timed out. The confirmation rate is 1 / 2 = 0.5.
```

---

## 题目（中文翻译）

**描述**  
表 `Signups`  
表 `Confirmations`  

用户的确认率（confirmation rate）定义为 “已确认” 消息的数量除以请求确认消息的总数量。若用户没有请求任何确认消息，则其确认率为 0。请将确认率四舍五入保留两位小数。

请编写查询，找出每个用户的确认率。返回的结果表可以按任意顺序排列，结果格式请参考下面的示例。

**示例 1**

```text
Signups 表结构
+------------+----------+
| Column Name| Type     |
+------------+----------+
| user_id    | int      |
| time_stamp | datetime |
+------------+----------+
```

`user_id` 为该表的唯一标识列。每行记录了对应 `user_id` 用户的注册时间。

```text
Confirmations 表结构
+------------+----------+--------+
| Column Name| Type     | Note   |
+------------+----------+--------+
| user_id    | int      |
| time_stamp | datetime |
| action     | ENUM     |
+------------+----------+--------+
```

`(user_id, time_stamp)` 为主键（组合唯一键）。`user_id` 为外键，引用 `Signups` 表的 `user_id`。`action` 为枚举类型，取值可能为 `'sent'`（请求确认）或 `'confirmed'`（已确认）。

**示例 2**

```text
Input
Signups 表:
+---------+---------------------+
| user_id | time_stamp          |
+---------+---------------------+
| 3       | 2020-03-21 10:16:13 |
| 7       | 2020-01-04 13:57:59 |
| 2       | 2020-07-29 23:09:44 |
| 6       | 2020-12-09 10:39:37 |
+---------+---------------------+

Confirmations 表:
+---------+---------------------+-----------+
| user_id | time_stamp          | action    |
+---------+---------------------+-----------+
| 3       | 2020-03-22 09:12:45 | sent      |
| 3       | 2020-03-23 11:23:11 | confirmed |
| 7       | 2020-01-05 08:45:12 | sent      |
| 2       | 2020-08-01 14:55:02 | sent      |
| 2       | 2020-08-02 16:33:44 | confirmed |
| 2       | 2020-08-03 12:20:30 | confirmed |
| 6       | 2020-12-10 07:00:00 | sent      |
+---------+---------------------+-----------+
```

**输出**

```text
+---------+-----------------+
| user_id | confirmation_rate |
+---------+-----------------+
| 3       | 0.50            |
| 7       | 0.00            |
| 2       | 0.67            |
| 6       | 0.00            |
+---------+-----------------+
```

**解释**  
- 用户 3：请求确认 1 条，已确认 1 条 → 1 / 2 = 0.50（四舍五入保留两位小数）。  
- 用户 7：仅请求确认 1 条，未收到确认 → 0 / 1 = 0.00。  
- 用户 2：请求确认 1 条，已确认 2 条 → 2 / 3 ≈ 0.67。  
- 用户 6：仅请求确认 1 条，未收到确认 → 0 / 1 = 0.00。  

**约束条件**  
- 表中 `user_id` 均为正整数。  
- `time_stamp` 的格式为 `YYYY-MM-DD HH:MM:SS`。  
- `action` 只会出现 `'sent'` 或 `'confirmed'` 两种取值。  

**SQL 查询示例（供参考）**

```sql
SELECT
    s.user_id,
    ROUND(
        COALESCE(SUM(CASE WHEN c.action = 'confirmed' THEN 1 END), 0) /
        COALESCE(SUM(CASE WHEN c.action = 'sent' THEN 1 END), 0),
        2
    ) AS confirmation_rate
FROM Signups s
LEFT JOIN Confirmations c ON s.user_id = c.user_id
GROUP BY s.user_id;
```

> 以上查询首先统计每位用户的 `'sent'`（请求确认）和 `'confirmed'`（已确认）次数，随后计算比例并使用 `ROUND(..., 2)` 保留两位小数。若用户没有任何 `'sent'` 记录，则分母为 0，`COALESCE` 将其视为 0，最终返回 0.00。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：  

1. **遍历 `Signups` 表**，拿到每一个 `user_id`。  
2. 对于当前的 `user_id`，**再次遍历整个 `Confirmations` 表**，统计该用户的  
   - 请求的确认消息总数（`total`）  
   - 已经确认的消息数（`confirmed`），即 `action = 'confirmed'` 的记录。  
3. 计算确认率 `rate = confirmed / total`，如果 `total` 为 0，直接把 `rate` 设为 0。  
4. 把结果保存到列表里，最后一次性输出。

> **类比**：把 `Confirmations` 表想象成一本厚厚的电话簿，想找某个人的记录时，你只能从头翻到尾，逐行检查——这就是“暴力”搜索。  

这种方法一定能得到正确答案，因为我们对每个用户都检查了所有可能的确认记录，**没有遗漏**。

#### 代码（Python）  
```python
# ------------------- 暴力解 -------------------
# 假设已有两张表的数据分别存放在 list of dict 中
signups = [
    {"user_id": 3, "time_stamp": "2020-03-21 10:16:13"},
    {"user_id": 7, "time_stamp": "2020-01-04 13:57:59"},
    {"user_id": 2, "time_stamp": "2020-07-29 23:09:44"},
    {"user_id": 6, "time_stamp": "2020-12-09 10:39:37"},
]

confirmations = [
    {"user_id": 3, "time_stamp": "2020-03-21 10:20:00", "action": "requested"},
    {"user_id": 3, "time_stamp": "2020-03-21 10:22:10", "action": "confirmed"},
    {"user_id": 7, "time_stamp": "2020-01-04 14:00:00", "action": "requested"},
    {"user_id": 7, "time_stamp": "2020-01-04 14:05:00", "action": "confirmed"},
    {"user_id": 7, "time_stamp": "2020-01-04 14:10:00", "action": "requested"},
    # … 其他数据
]

result = []  # 用来保存每个用户的确认率

for s in signups:                     # 对每个注册用户
    uid = s["user_id"]
    total = 0                         # 该用户请求的次数
    confirmed = 0                     # 该用户已确认的次数
    for c in confirmations:          # 逐行扫描确认表（暴力遍历）
        if c["user_id"] == uid:       # 只关心同一个用户的记录
            total += 1
            if c["action"] == "confirmed":
                confirmed += 1
    # 计算确认率，注意除数为 0 的情况
    rate = round(confirmed / total, 2) if total > 0 else 0.0
    result.append({"user_id": uid, "confirmation_rate": rate})

print(result)   # 示例输出
```

#### 复杂度  

- **时间复杂度**：`O(U * C)`，其中 `U` 为注册用户数量，`C` 为 `Confirmations` 表的总行数。  
  - 大白话：如果有 1000 个用户、5000 条确认记录，就要做 1000 × 5000 = 5,000,000 次比较，显然会很慢。  
- **空间复杂度**：`O(1)`（不计输入数据本身），只用了常数级别的临时变量。  

---

### 2. 最优解  

#### 思路  
暴力解的瓶颈在于 **对每个用户都遍历一遍完整的 Confirmations 表**。我们可以把这一步提前做一次：  

1. **一次遍历 Confirmations 表**，把每条记录按 `user_id` 累计到两个哈希表（Python 的 `dict`）中  
   - `total_cnt[user_id]` → 该用户的请求总数  
   - `confirmed_cnt[user_id]` → 该用户已确认的次数  
   这里的 **哈希表** 类比成一本**“字典”**，把 `user_id` 当成单词，出现次数当成对应的页码，查找和写入都只需要 O(1) 时间。  
2. 再遍历 `Signups` 表，直接从哈希表里取出对应的计数，算出确认率。  
3. 如果某个 `user_id` 在哈希表里找不到，说明他从未请求过确认，直接把率设为 0。  

这样我们只 **遍历两遍表**（各一次），时间从 `O(U*C)` 降到了 `O(U + C)`，大幅提升效率。

#### 代码（Python）  
```python
# ------------------- 最优解（哈希表） -------------------
from collections import defaultdict

# 第一步：一次遍历 Confirmations，累计计数
total_cnt = defaultdict(int)      # 所有请求的数量
confirmed_cnt = defaultdict(int)  # 已确认的数量

for rec in confirmations:
    uid = rec["user_id"]
    total_cnt[uid] += 1                     # 每出现一次就 +1
    if rec["action"] == "confirmed":
        confirmed_cnt[uid] += 1

# 第二步：遍历 Signups，直接计算确认率
result_opt = []
for s in signups:
    uid = s["user_id"]
    total = total_cnt.get(uid, 0)           # 若不存在则返回 0
    confirmed = confirmed_cnt.get(uid, 0)
    rate = round(confirmed / total, 2) if total > 0 else 0.0
    result_opt.append({"user_id": uid, "confirmation_rate": rate})

print(result_opt)   # 与暴力解的结果一致
```

#### 复杂度  

- **时间复杂度**：`O(U + C)`  
  - 只需要各遍历一次 `Signups`（U 行）和 `Confirmations`（C 行），不再出现“每个用户都扫一遍表”的二次循环。  
  - 与暴力解相比，时间提升约为 `C` 倍（比如原来 5,000,000 次比较，现在只要 6,000 次）。  
- **空间复杂度**：`O(K)`，其中 `K` 为不同 `user_id` 的数量（即哈希表的键数）。  
  - 需要额外存储两个字典，每个键只占用常数空间。  

---

## 心得  

- **核心技巧**：利用哈希表（字典）一次遍历完成分组统计，避免嵌套循环。  
- **适用的题型**  
  1. “按用户/类别分组统计”类问题（如订单总额、访问次数等）。  
  2. “两张表关联后做聚合”类问题（如订单与退款匹配、评论与点赞比例）。  
- **解题钥匙**：**先聚合，再关联**——先把需要的统计信息抽出来（一次遍历），再在主表里直接查找。  

---

## 反思  

- **第一反应**：看到“每个用户的确认率”，立刻想到“遍历每个用户，再遍历确认记录”，这就是暴力思路。  
- **最容易踩的坑**  
  - **除零错误**：有的用户可能从未请求过确认，需要把分母为 0 的情况特别处理为 0。  
  - **浮点数四舍五入**：题目要求保留两位小数，直接用 `round(..., 2)` 即可，别忘了。  
  - **缺失用户**：如果 `Confirmations` 表里没有某个 `user_id`，仍然要在结果里出现，确认率为 0。  
- **下次思路**：看到“统计/比例”且涉及两张表，第一步就想到 **使用哈希表/字典一次性统计**，把聚合搬到前面做，避免 O(N²) 的循环。