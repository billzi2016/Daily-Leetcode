# #1158. 市场分析 I / Market Analysis I

> 难度：中等 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/market-analysis-i/)

---

## 题目（英文原版）

**Description**

Table: Users
Table: Orders
Table: Items
Write a solution to find for each user, the join date and the number of orders they made as a buyer in 2019.
Return the result table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+----------------+---------+
| Column Name    | Type    |
+----------------+---------+
| user_id        | int     |
| join_date      | date    |
| favorite_brand | varchar |
+----------------+---------+
user_id is the primary key (column with unique values) of this table.
This table has the info of the users of an online shopping website where users can sell and buy items.
```

**Example 2:**

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| order_id      | int     |
| order_date    | date    |
| item_id       | int     |
| buyer_id      | int     |
| seller_id     | int     |
+---------------+---------+
order_id is the primary key (column with unique values) of this table.
item_id is a foreign key (reference column) to the Items table.
buyer_id and seller_id are foreign keys to the Users table.
```

**Example 3:**

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| item_id       | int     |
| item_brand    | varchar |
+---------------+---------+
item_id is the primary key (column with unique values) of this table.
```

**Example 4:**

```
Input: 
Users table:
+---------+------------+----------------+
| user_id | join_date  | favorite_brand |
+---------+------------+----------------+
| 1       | 2018-01-01 | Lenovo         |
| 2       | 2018-02-09 | Samsung        |
| 3       | 2018-01-19 | LG             |
| 4       | 2018-05-21 | HP             |
+---------+------------+----------------+
Orders table:
+----------+------------+---------+----------+-----------+
| order_id | order_date | item_id | buyer_id | seller_id |
+----------+------------+---------+----------+-----------+
| 1        | 2019-08-01 | 4       | 1        | 2         |
| 2        | 2018-08-02 | 2       | 1        | 3         |
| 3        | 2019-08-03 | 3       | 2        | 3         |
| 4        | 2018-08-04 | 1       | 4        | 2         |
| 5        | 2018-08-04 | 1       | 3        | 4         |
| 6        | 2019-08-05 | 2       | 2        | 4         |
+----------+------------+---------+----------+-----------+
Items table:
+---------+------------+
| item_id | item_brand |
+---------+------------+
| 1       | Samsung    |
| 2       | Lenovo     |
| 3       | LG         |
| 4       | HP         |
+---------+------------+
Output: 
+-----------+------------+----------------+
| buyer_id  | join_date  | orders_in_2019 |
+-----------+------------+----------------+
| 1         | 2018-01-01 | 1              |
| 2         | 2018-02-09 | 2              |
| 3         | 2018-01-19 | 0              |
| 4         | 2018-05-21 | 0              |
+-----------+------------+----------------+
```

---

## 题目（中文翻译）

编写一个查询，统计每位用户的 **加入日期**（join date）以及他们在 **2019 年** 作为买家（buyer）下的订单数量。返回的结果表可以任意顺序排列，格式请参考示例。

**表结构**

**Users**  
```
+----------------+---------+
| Column Name    | Type    |
+----------------+---------+
| user_id        | int     |
| join_date      | date    |
| favorite_brand | varchar |
+----------------+---------+
```
- `user_id` 为主键（primary key），即唯一值列。  
- 该表记录了在线购物网站用户的信息，用户既可以出售也可以购买商品。

**Orders**  
```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| order_id      | int     |
| order_date    | date    |
| item_id       | int     |
| buyer_id      | int     |
| seller_id     | int     |
+---------------+---------+
```
- `order_id` 为主键（primary key）。  
- `item_id` 为外键（foreign key），引用 **Items** 表。  
- `buyer_id` 与 `seller_id` 分别表示买家和卖家的用户编号。

**Items**  
```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| item_id       | int     |
| item_brand    | varchar |
+---------------+---------+
```
- `item_id` 为主键（primary key）。

**示例**

**输入**  

Users 表：
```
+---------+------------+----------------+
| user_id | join_date  | favorite_brand |
+---------+------------+----------------+
| 1       | 2018-01-01 | Lenovo         |
| 2       | 2018-02-09 | Samsung        |
| 3       | 2018-01-19 | LG             |
| 4       | 2018-05-21 | HP             |
+---------+------------+----------------+
```

Orders 表：
```
+----------+------------+----...
```
（后续数据省略）

**输出**  
（依据题目要求返回每位用户的 `join_date` 与 2019 年的订单数，顺序不限）

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题本质上是 **把三张表（Users、Orders、Items）关联起来**，然后统计每个用户在 2019 年作为买家的订单数量。  
如果不使用任何技巧，只按照最直接的想法来做：

1. **遍历 Users 表**，取出每一行的 `user_id` 与 `join_date`。  
2. 对每一个 `user_id`，再 **遍历 Orders 表**，检查该行的 `buyer_id` 是否等于当前 `user_id`，并且 `order_date` 落在 2019‑01‑01 到 2019‑12‑31 之间。满足条件就计数。  
3. 把计数结果和 `join_date` 放进结果列表。

> **类比**：想象你在图书馆查某个人借了多少本书。先把所有人名单列出来（第一遍），再对每个人去“借书记录”里逐条检查（第二遍）。这就是最朴素的“双层循环”。

> **为什么正确**：我们把所有可能的组合都检查了一遍，只要符合题目条件就计数，天然满足“每个用户、每笔符合条件的订单”这一要求。

#### 代码（Python）

```python
# -------------------------------------------------
# 暴力实现：双层循环 + 线性扫描
# -------------------------------------------------
from datetime import datetime
from typing import List, Dict

def market_analysis_brute(
    users: List[Dict],
    orders: List[Dict],
) -> List[Dict]:
    """
    返回每个用户的 join_date 与 2019 年的买家订单数
    参数:
        users  : [{ "user_id": int, "join_date": "YYYY-MM-DD", ... }, ...]
        orders : [{ "order_id": int, "order_date": "YYYY-MM-DD",
                    "buyer_id": int, "seller_id": int, ... }, ...]
    """
    result = []
    # 先把 2019 年的起止日期转成 datetime，方便比较
    start_2019 = datetime.strptime("2019-01-01", "%Y-%m-%d")
    end_2019   = datetime.strptime("2019-12-31", "%Y-%m-%d")

    for u in users:                                 # 👈 第一次遍历 Users
        uid = u["user_id"]
        join = u["join_date"]
        cnt = 0                                      # 该用户 2019 年的订单计数

        for o in orders:                             # 👈 第二次遍历 Orders
            # 只关心 buyer_id 与当前用户相同，且日期在 2019 年
            if o["buyer_id"] == uid:
                od = datetime.strptime(o["order_date"], "%Y-%m-%d")
                if start_2019 <= od <= end_2019:
                    cnt += 1

        result.append({
            "user_id": uid,
            "join_date": join,
            "order_cnt": cnt
        })
    return result
```

#### 复杂度  

- **时间复杂度：** `O(U * O)`，其中 `U` 为用户数量，`O` 为订单数量。  
  > 大白话：如果用户有 1000 条，订单有 10 000 条，最坏情况下要检查 1000 × 10 000 = 1,000 万次。  
- **空间复杂度：** `O(U)`，只需要保存结果列表（每个用户一条记录）。  
  > 大白话：额外占用的内存跟用户数成正比，和订单数无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **对每个用户都要完整遍历一次订单表**，这导致 `U * O` 的乘法级别。  
我们可以把“遍历 Orders”这一步 **只做一次**，把订单按买家分组统计，这正是 **哈希表（字典）** 的强项。

优化步骤：

1. **先遍历 Orders 表**，只保留 2019 年的记录（一次过滤），并把每条记录的 `buyer_id` 作为键，计数作为值，存进 `buyer_cnt` 字典。  
   - 这相当于把“借书记录”先按照“借书人”归类好，像把图书馆的借书单按照人名排好序，后面查询就可以直接拿到。  
2. 再遍历 Users 表，直接从 `buyer_cnt` 中取出对应 `user_id` 的计数（若不存在则为 0），再拼装结果。  
3. 只需要 **两次线性遍历**，没有嵌套循环，时间复杂度降为 `O(U + O)`。

> **核心数据结构**：`dict`（在 Python 里实现哈希表）。  
> 类比：字典就像一本电话簿，**key** 是人的名字，**value** 是他的电话号码。我们把每个人的订单数量“写进电话簿”，以后查询只要一次查找（O(1)）即可。

#### 代码（Python）

```python
# -------------------------------------------------
# 最优实现：一次遍历 Orders + 哈希表统计
# -------------------------------------------------
from datetime import datetime
from typing import List, Dict

def market_analysis_optimal(
    users: List[Dict],
    orders: List[Dict],
) -> List[Dict]:
    """
    与暴力版等价，但时间复杂度降到 O(U + O)。
    """
    # 1️⃣ 统计 2019 年每个买家的订单数量
    buyer_cnt = {}                                 # {buyer_id: count}
    start_2019 = datetime.strptime("2019-01-01", "%Y-%m-%d")
    end_2019   = datetime.strptime("2019-12-31", "%Y-%m-%d")

    for o in orders:                               # 只遍历一次 Orders
        # 过滤掉非 2019 年的订单
        od = datetime.strptime(o["order_date"], "%Y-%m-%d")
        if not (start_2019 <= od <= end_2019):
            continue
        bid = o["buyer_id"]
        buyer_cnt[bid] = buyer_cnt.get(bid, 0) + 1   # 哈希表计数，等价于 ++

    # 2️⃣ 把统计结果和 Users 表拼起来
    result = []
    for u in users:                                # 再遍历一次 Users
        uid = u["user_id"]
        result.append({
            "user_id": uid,
            "join_date": u["join_date"],
            "order_cnt": buyer_cnt.get(uid, 0)      # 若没有记录，默认 0
        })
    return result
```

#### 复杂度  

- **时间复杂度：** `O(U + O)`。  
  > 大白话：先把订单表扫一遍（比如 10 000 条），再把用户表扫一遍（比如 1 000 条），总共约 11 000 次操作，远远小于 1 000 万次。  
- **空间复杂度：** `O(K)`，`K` 为不同买家的数量（即哈希表的键数），最坏情况等同于订单表的买家数，但仍远小于 `U * O`。  
  > 大白话：额外占用的内存只跟买家种类多少有关，和订单总量的乘积无关。

---

## 心得

- **核心技巧**：使用哈希表（字典）对数据进行一次性分组统计，避免嵌套循环。  
- **适用的题型**  
  1. “统计每个用户/商品/店铺在某个时间段的交易次数”  
  2. “按照类别统计出现次数” （如 LeetCode 统计出现频率的题目）  
  3. “求每个学生的成绩总分/平均分”  
- **一句话总结解题钥匙**：**先把大表一次遍历并聚合，再用哈希表直接查询，避免重复遍历**。

---

## 反思

- **第一反应**：直接写两层 `for` 循环，对每个用户遍历所有订单。  
- **最容易踩的坑**  
  - **日期过滤不严谨**：忘记把字符串转成 `datetime` 比较，导致 `'2019-12-31' > '2020-01-01'` 之类的错误。  
  - **遗漏没有订单的用户**：如果只返回出现过的 `buyer_id`，会把没有买过的用户漏掉。应当在遍历 `Users` 时默认计数为 `0`。  
  - **键名冲突**：如果把 `buyer_cnt` 与 `users` 合并时直接 `update`，可能会把 `join_date` 覆盖掉，需慎重命名字段。  
- **下次类似题的第一步**：**先思考能否一次遍历完成统计**（即“把计数搬到哈希表”），再决定是否需要额外的排序或连接操作。