# #1045. 购买所有产品的客户 / Customers Who Bought All Products

> 难度：中等 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/customers-who-bought-all-products/)

---

## 题目（英文原版）

**Description**

Table: Customer
Table: Product
Write a solution to report the customer ids from the Customer table that bought all the products in the Product table.
Return the result table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| customer_id | int     |
| product_key | int     |
+-------------+---------+
This table may contain duplicates rows. 
customer_id is not NULL.
product_key is a foreign key (reference column) to Product table.
```

**Example 2:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| product_key | int     |
+-------------+---------+
product_key is the primary key (column with unique values) for this table.
```

**Example 3:**

```
Input: 
Customer table:
+-------------+-------------+
| customer_id | product_key |
+-------------+-------------+
| 1           | 5           |
| 2           | 6           |
| 3           | 5           |
| 3           | 6           |
| 1           | 6           |
+-------------+-------------+
Product table:
+-------------+
| product_key |
+-------------+
| 5           |
| 6           |
+-------------+
Output: 
+-------------+
| customer_id |
+-------------+
| 1           |
| 3           |
+-------------+
Explanation: 
The customers who bought all the products (5 and 6) are customers with IDs 1 and 3.
```

---

## 题目（中文翻译）

**描述**  
表（Table）：Customer  
表（Table）：Product  

编写一个查询，返回 Customer 表中购买了 Product 表中**所有**产品的 `customer_id`。结果可以任意顺序返回。返回结果的格式请参见下方示例。

**示例 1**  

示例表结构：

| Column Name | Type |
|-------------|------|
| customer_id | int |
| product_key | int |

此表可能包含**重复行（duplicate rows）**。`customer_id` 不为空。`product_key` 是指向 Product 表的**外键（foreign key）**。

| Column Name | Type |
|-------------|------|
| product_key | int |

`product_key` 为该表的**主键（primary key）**（唯一值列）。

**示例 3**  

输入：  
Customer 表：

| customer_id | product_key |
|-------------|-------------|
| 1           | 5           |
| 2           | 6           |
| 3           | 5           |
| 3           | 6           |
| 1           | 6           |

Product 表：

| product_key |
|-------------|
| 5           |
| 6           |

输出：

| customer_id |
|-------------|
| 1           |
| 3           |

**解释**  
购买了所有产品（5 和 6）的客户是 ID 为 1 和 3 的客户。

**约束条件**  
无

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把 **所有商品** 看成一个集合 `all_products`，然后遍历每一个顾客 `customer_id`，把他买过的商品也放进集合 `bought`，最后检查 `bought` 是否 **恰好包含** `all_products`（即两者相等）。  

- **数据结构**  
  - `set`（集合）就像生活中的“装了所有不同物品的盒子”。往里放东西会自动去重，判断两个盒子是否装的是同样的东西只要 `set1 == set2`。  
  - `dict`（字典）可以把每个 `customer_id` 对应到他买过的商品集合，类似于 **查字典**：键是顾客，值是这个顾客的商品盒子。  

- **为什么正确**  
  如果一个顾客的商品集合正好等于所有商品的集合，说明他买过 **每一种** 商品（可能有重复购买，但集合已经去掉了重复）。反之，如果集合不相等，必然缺少至少一种商品。  

- **复杂度分析（大白话）**  
  - **时间**：我们要遍历两张表一次来构造集合，再遍历所有顾客一次来比较。设 `N` 为 `Customer` 表的行数，`M` 为 `Product` 表的行数，时间复杂度是 `O(N + M)`。  
  - **空间**：需要存下所有商品集合 `O(M)`，以及每个顾客对应的商品集合，最坏情况下每个顾客都买了所有商品，需要 `O(K * M)`（`K` 为顾客数量）。  

#### 代码（Python）  

```python
from collections import defaultdict
from typing import List, Tuple, Set

def customers_who_bought_all_bruteforce(
    customer: List[Tuple[int, int]],   # (customer_id, product_key)
    product: List[int]                 # product_key
) -> List[int]:
    """
    暴力实现：逐个顾客比集合
    """
    # 1️⃣ 把所有商品放进一个集合，像装满了所有商品的盒子
    all_products: Set[int] = set(product)          # O(M)

    # 2️⃣ 为每个顾客准备一个“商品盒子”，用 defaultdict 自动创建空集合
    bought_by: defaultdict[int, Set[int]] = defaultdict(set)   # O(1)

    # 3️⃣ 遍历 Customer 表，把每条记录的商品放进对应顾客的盒子里
    for cust_id, prod_key in customer:            # O(N)
        bought_by[cust_id].add(prod_key)          # 自动去重

    # 4️⃣ 检查每个顾客的盒子是否装满了所有商品
    result: List[int] = []
    for cust_id, bought_set in bought_by.items():  # O(K)
        if bought_set == all_products:              # 两个集合相等即买全了
            result.append(cust_id)

    return result
```

#### 复杂度  

- **时间复杂度**：`O(N + M + K)`  
  - `N`：`Customer` 表的行数（遍历一次）  
  - `M`：`Product` 表的行数（构造全商品集合）  
  - `K`：不同顾客的数量（遍历比较一次）  
  这在大多数情况下已经够快了，但如果顾客很多、商品很多，集合比较的开销仍然不容忽视。  

- **空间复杂度**：`O(M + K·M)`（最坏情况）  
  - `M` 用于存全商品集合  
  - 每个顾客可能都买了全部商品，需要 `K` 个集合，每个集合大小最多 `M`  

---

### 2. 最优解  

#### 思路  
暴力解的瓶颈在于 **为每个顾客保存完整的商品集合**，这会占用较多内存。实际上，我们只需要知道每个顾客买了多少种不同商品，**不需要记住具体是哪几种**。  

关键观察：

1. 先算出商品表里有多少种商品，记为 `total_cnt`。  
2. 再对 `Customer` 表 **按顾客分组**，统计每个顾客买到的 **不同商品** 数量 `cnt_distinct`。  
3. 当且仅当 `cnt_distinct == total_cnt` 时，这位顾客买到了所有商品。  

这一步只需要一次 **分组统计**，不需要存每个顾客的商品集合，空间可以降到 `O(K)`（只保存计数），时间仍是 `O(N + M)`。

在 SQL 中，这相当于：

```sql
SELECT c.customer_id
FROM Customer c
GROUP BY c.customer_id
HAVING COUNT(DISTINCT c.product_key) = (SELECT COUNT(*) FROM Product);
```

下面给出纯 Python 实现，利用 `defaultdict` 只保存计数。

#### 代码（Python）  

```python
from collections import defaultdict
from typing import List, Tuple, Set

def customers_who_bought_all_optimal(
    customer: List[Tuple[int, int]],   # (customer_id, product_key)
    product: List[int]                 # product_key
) -> List[int]:
    """
    最优实现：只统计每个顾客买到的不同商品种类数
    """
    # 1️⃣ 商品总种类数
    total_cnt: int = len(set(product))   # O(M)

    # 2️⃣ 用字典统计每个顾客买到的不同商品数
    #    key: customer_id, value: set of distinct product_keys
    #    这里仍然使用 set 来去重，但每个集合只在计数后就可以丢弃
    distinct_per_customer: defaultdict[int, Set[int]] = defaultdict(set)

    for cust_id, prod_key in customer:          # O(N)
        distinct_per_customer[cust_id].add(prod_key)

    # 3️⃣ 只保留计数等于 total_cnt 的顾客
    result: List[int] = []
    for cust_id, prod_set in distinct_per_customer.items():   # O(K)
        if len(prod_set) == total_cnt:        # 计数相等即买全了
            result.append(cust_id)

    return result
```

> **小技巧**：如果真的想把空间降到只保存计数（不保存集合），可以在遍历 `Customer` 表时使用 `defaultdict[int, set]` 来去重，然后在计数后把集合 `clear()`，或者改用 `defaultdict[int, int]` 并配合 **位图 / 位运算**（商品数量不大时）实现更省空间的计数。这里保持代码可读性，仍使用集合。

#### 复杂度  

- **时间复杂度**：`O(N + M)`  
  - 与暴力解相同，因为我们仍然需要遍历两张表一次。唯一的额外开销是对每个顾客集合求长度，仍是常数时间。  

- **空间复杂度**：`O(K + M)`（`K` 为不同顾客数量）  
  - `M` 用于存全商品集合（不可避免），  
  - `K` 用于存每个顾客的 **去重后的商品集合**（或计数），但每个集合的大小最多等于 `total_cnt`，整体空间远小于暴力解的 `O(K·M)`。  

与暴力解相比，**空间下降显著**，而时间保持不变，是更实用的方案。

---

## 心得  

- **核心技巧**：利用 **集合去重 + 分组计数** 判断“是否包含全部”。  
- **适用场景**  
  1. “找出购买了所有商品的用户”类问题（本题）。  
  2. “找出拥有所有技能的员工”或 “拥有所有标签的文章”。  
  3. “检查每个学生是否完成了所有课程”这类全覆盖判断。  
- **一句话总结**：**把“全部”转化为“种类计数相等”，用分组统计即可轻松解决**。

---

## 反思  

- **第一反应**：直接想把每个顾客的商品集合和全部商品集合做比较——这就是暴力思路。  
- **最容易踩的坑**  
  - **重复记录**：`Customer` 表可能出现同一顾客同一商品的多行，需要去重（用 `set` 或 `COUNT(DISTINCT ...)`）。  
  - **空表**：如果 `Product` 表为空，所有顾客都应被视为“买了全部商品”。实现时 `total_cnt = 0`，计数为 0 的顾客自然符合条件。  
  - **数据量极大**：直接保存每个顾客的完整商品集合会导致内存爆炸，需改为计数或位图。  
- **下次第一步**：先思考“全覆盖”是否可以用 **计数相等** 替代 **集合比较**，然后决定是用 SQL 的 `HAVING COUNT(DISTINCT ...)` 还是在代码里做分组计数。这样可以立刻定位最省空间的实现路径。