# #1407. **Top Travellers** / Top Travellers

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/top-travellers/)

---

## 题目（英文原版）

**Description**

Table: Users
Table: Rides
Write a solution to report the distance traveled by each user.
Return the result table ordered by travelled_distance in descending order, if two or more users traveled the same distance, order them by their name in ascending order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| id            | int     |
| name          | varchar |
+---------------+---------+
id is the column with unique values for this table.
name is the name of the user.
```

**Example 2:**

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| id            | int     |
| user_id       | int     |
| distance      | int     |
+---------------+---------+
id is the column with unique values for this table.
user_id is the id of the user who traveled the distance "distance".
```

**Example 3:**

```
Input: 
Users table:
+------+-----------+
| id   | name      |
+------+-----------+
| 1    | Alice     |
| 2    | Bob       |
| 3    | Alex      |
| 4    | Donald    |
| 7    | Lee       |
| 13   | Jonathan  |
| 19   | Elvis     |
+------+-----------+
Rides table:
+------+----------+----------+
| id   | user_id  | distance |
+------+----------+----------+
| 1    | 1        | 120      |
| 2    | 2        | 317      |
| 3    | 3        | 222      |
| 4    | 7        | 100      |
| 5    | 13       | 312      |
| 6    | 19       | 50       |
| 7    | 7        | 120      |
| 8    | 19       | 400      |
| 9    | 7        | 230      |
+------+----------+----------+
Output: 
+----------+--------------------+
| name     | travelled_distance |
+----------+--------------------+
| Elvis    | 450                |
| Lee      | 450                |
| Bob      | 317                |
| Jonathan | 312                |
| Alex     | 222                |
| Alice    | 120                |
| Donald   | 0                  |
+----------+--------------------+
Explanation: 
Elvis and Lee traveled 450 miles, Elvis is the top traveler as his name is alphabetically smaller than Lee.
Bob, Jonathan, Alex, and Alice have only one ride and we just order them by the total distances of the ride.
Donald did not have any rides, the distance traveled by him is 0.
```

---

## 题目（中文翻译）

描述  
给定两张表 **Users** 与 **Rides**，请编写查询语句统计每位用户累计旅行的距离。返回的结果表需要按照 **travelled_distance**（累计距离）降序排列；如果有多名用户的累计距离相同，则按 **name**（用户名）升序排列。

**表结构**

**Users** 表  
| Column Name | Type    |
|-------------|---------|
| id          | int     |
| name        | varchar |

- `id` 为唯一标识列。  
- `name` 为用户的姓名。

**Rides** 表  
| Column Name | Type |
|-------------|------|
| id          | int  |
| user_id     | int  |
| distance    | int  |

- `id` 为唯一标识列。  
- `user_id` 为进行该次旅行的用户的 `id`。  
- `distance` 为该次旅行的距离。

**示例**

输入  

Users 表：  
```
+------+-----------+
| id   | name      |
+------+-----------+
| 1    | Alice     |
| 2    | Bob       |
| 3    | Alex      |
| 4    | Donald    |
| 7    | Lee       |
| 13   | Jonathan  |
| 19   | Elvis     |
+------+-----------+
```

Rides 表：  
```
+------+----------+----------+
| id   | user_id  | distance |
+------+----------+----------+
| 1    | 1        | 120      |
| 2    | 2        | 200      |
| 3    | 3        | 80       |
| 4    | 4        | 400      |
| 5    | 7        | 150      |
| 6    | 13       | 200      |
| 7    | 1        | 80       |
| 8    | 2        | 150      |
| 9    | 3        | 150      |
|10    | 4        | 250      |
|11    | 7        | 150      |
|12    | 13       | 100      |
+------+----------+----------+
```

输出  
```
+-----------+-------------------+
| name      | travelled_distance|
+-----------+-------------------+
| Donald    | 650               |
| Bob       | 350               |
| Jonathan  | 300               |
| Lee       | 300               |
| Alice     | 200               |
| Alex      | 230               |
| Elvis     | 0                 |
+-----------+-------------------+
```

解释  
- Donald 的累计距离为 400 + 250 = 650。  
- Bob 的累计距离为 200 + 150 = 350。  
- Jonathan 的累计距离为 200 + 100 = 300。  
- Lee 的累计距离为 150 + 150 = 300（与 Jonathan 同距离，按姓名升序排在后面）。  
- Alice 的累计距离为 120 + 80 = 200。  
- Alex 的累计距离为 80 + 150 = 230。  
- Elvis 没有对应的行程记录，累计距离为 0。

约束条件  
- 无。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的做法是把 **Users** 表和 **Rides** 表先“一对多”地连接起来（相当于把每个人的所有乘坐记录都列出来），再把同一个用户的 `distance` 累加得到总里程。  

- **连接（JOIN）**：把两张表的 `id` 与 `user_id` 对上，就像把一本电话簿（Users）和一张出行日志（Rides）用“身份证号”这根绳子绑在一起。  
- **累计（SUM）**：把绑在一起的每个人的所有出行距离加起来，类似把同一个人多次旅行的里程写在同一张纸上。  

这个方法一定能得到正确答案，因为我们没有遗漏任何一条出行记录，也没有把不属于该用户的记录算进去。  

**时间复杂度**  
- 连接的过程需要把两张表的每一行都配对一次，最坏情况下是 `O(|Users| × |Rides|)`，即如果每个人都有对应的每条记录，就会出现笛卡尔积的情况。  
- 再遍历一次连接结果做求和，时间是 `O(N)`（N 为连接后的行数），总体仍然是 `O(|Users| × |Rides|)`。  
在大白话里，**O(n²)** 可以想象成“如果你有 n 本书，需要把每本书和每本书的每一页都比对一次”。  

**空间复杂度**  
- 需要额外保存连接后的所有行，最坏情况下也是 `O(|Users| × |Rides|)`。  

#### 代码（Python）  

```python
# 下面的实现使用 Python 的列表模拟数据库表
# Users 表：每条记录是 (id, name)
users = [
    (1, "Alice"),
    (2, "Bob"),
    (3, "Alex"),
    (4, "Donald"),
    (7, "Lee"),
    (13, "Jonathan"),
    (19, "Elvis")
]

# Rides 表：每条记录是 (id, user_id, distance)
rides = [
    (1, 1, 120),
    (2, 2,  50),
    (3, 1,  80),
    (4, 3,  40),
    (5, 7, 150),
    (6, 2,  70),
    (7, 7,  30),
    (8, 13, 200)
]

# ---------- 暴力解 ----------
# 1. 先把两张表“笛卡尔乘积”，只保留 user_id 与 id 相等的行
joined = []                              # 用来存放连接后的记录
for u_id, u_name in users:               # 遍历 Users 表
    for r_id, r_user_id, r_dist in rides:  # 遍历 Rides 表
        if u_id == r_user_id:            # 只保留匹配的行
            # 记录形式：(user_id, name, distance)
            joined.append((u_id, u_name, r_dist))

# 2. 对相同 user_id 的 distance 求和
# 这里用一个字典来累计，key 是 user_id，value 是 (name, total_distance)
totals = {}
for uid, name, dist in joined:
    if uid not in totals:
        totals[uid] = [name, 0]          # 初始化累计表
    totals[uid][1] += dist               # 累加里程

# 3. 把结果转成列表并排序
#   - 先按 travelled_distance 降序
#   - 再按 name 升序（当距离相同）
result = sorted(
    [(uid, info[0], info[1]) for uid, info in totals.items()],
    key=lambda x: (-x[2], x[1])
)

# 输出
print("user_id | name     | travelled_distance")
for uid, name, dist in result:
    print(f"{uid:<7} | {name:<8} | {dist}")
```

#### 复杂度  

- **时间复杂度**：`O(|Users| × |Rides|)`  
  → 想象把每个人的名字和每一条出行记录都去“配对”，最坏情况要做这么多次比较。  

- **空间复杂度**：`O(|Users| × |Rides|)`（用于存放 `joined` 列表）  
  → 需要把配对成功的所有行都保存下来。  

---  

### 2. 最优解  

#### 思路  
暴力解的瓶颈在 **连接** 步骤：我们把两张表的每一行都遍历了一遍，导致时间和空间都呈乘积增长。  
实际上，**Rides** 表已经用 `user_id` 标记了所属的用户，我们不需要把两张表做笛卡尔乘积，只要把 **Rides** 按 `user_id` 直接累计，再把累计结果和 **Users** 表左连接（左连接保证即使某个用户没有任何出行记录，也会出现在结果中，里程为 0）。  

核心思路如下：

1. **一次遍历 Rides**，用字典 `distance_sum[user_id]` 把同一用户的距离直接相加。  
   - 这一步相当于把所有出行记录先“归类”，类似把一堆快递按照收件人编号装进不同的箱子。  
2. **遍历 Users**，把每个用户的姓名与上一步得到的累计里程取出（如果没有则为 0），形成最终的结果列表。  
3. **排序**：先按里程降序，再按姓名升序。  

因为我们只遍历两次（一次 Rides，一次 Users），时间是线性的 `O(|Users| + |Rides|)`，空间只需要保存字典 `distance_sum`（大小最多等于用户数量），所以是最优的。

> **重要概念——字典（哈希表）**  
> 字典可以看作一本“查询手册”，把 `user_id` 当作单词，里程当作对应的页码。查找、插入的时间都是常数级别（几乎是 O(1)），因此非常高效。

#### 代码（Python）  

```python
# ---------- 最优解 ----------
from collections import defaultdict

# 1. 把每个用户的距离累计到字典里（O(|Rides|)）
distance_sum = defaultdict(int)          # 默认值 0
for _, user_id, dist in rides:            # 只关心 user_id 与 distance
    distance_sum[user_id] += dist

# 2. 构造结果列表：遍历 Users，拿到对应的累计距离（若不存在则为 0）
result = []
for uid, name in users:
    total = distance_sum.get(uid, 0)      # .get 防止 KeyError
    result.append((uid, name, total))

# 3. 排序：里程降序 → 姓名升序（O(|Users| log|Users|)）
result.sort(key=lambda x: (-x[2], x[1]))

# 4. 输出（保持与暴力解相同的格式）
print("user_id | name     | travelled_distance")
for uid, name, dist in result:
    print(f"{uid:<7} | {name:<8} | {dist}")
```

#### 复杂度  

- **时间复杂度**：`O(|Users| + |Rides| + |Users|·log|Users|)`  
  - `|Users| + |Rides|` 是两次线性遍历，`log|Users|` 来自最终的排序。  
  - 与暴力解相比，**省掉了乘积的那一步**，在数据量大时提升非常明显。  

- **空间复杂度**：`O(|Users|)`  
  - 只需要一个字典保存每个用户的累计距离，和最终结果列表（大小等于用户数）。  

---

## 心得  

- **核心技巧**：使用哈希表（字典）对关联数据进行**分组求和**，再用**左连接**把所有主表记录保留下来。  
- **适用场景**  
  1. “统计每个用户的消费总额” 类似的 **分组聚合**（GROUP BY）问题。  
  2. “计算每种商品的库存” 这类 **按键累计** 的需求。  
  3. “统计每个城市的天气记录数量” 等需要 **按类别计数** 的题目。  
- **一句话总结**：先把 **子表** 用字典累计，再和 **主表** 合并——避免笛卡尔乘积，时间线性。  

## 反思  

- **第一反应**：看到两张表就想到先 `JOIN` 再 `GROUP BY`，这在 SQL 里是最常见的写法。  
- **最容易踩的坑**  
  - 忘记对没有出行记录的用户补 0，导致结果缺失（左连接要记得保留全部 Users）。  
  - 在手写 Python 时，把 `distance` 累计到错误的键上（比如用了 `id` 而不是 `user_id`）。  
- **下次遇到同类题**：第一步先问自己——“子表是否已经按外键分组？” 如果答案是“是”，就直接 **字典累计**，再 **左连接** 主表。这样可以立刻把时间复杂度从乘积降到线性。