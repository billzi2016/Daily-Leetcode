# #1327. 列出期间下单的产品 / List the Products Ordered in a Period

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/list-the-products-ordered-in-a-period/)

---

## 题目（英文原版）

**Description**

Table: Products
Table: Orders
Write a solution to get the names of products that have at least 100 units ordered in February 2020 and their amount.
Return the result table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+------------------+---------+
| Column Name      | Type    |
+------------------+---------+
| product_id       | int     |
| product_name     | varchar |
| product_category | varchar |
+------------------+---------+
product_id is the primary key (column with unique values) for this table.
This table contains data about the company's products.
```

**Example 2:**

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| product_id    | int     |
| order_date    | date    |
| unit          | int     |
+---------------+---------+
This table may have duplicate rows.
product_id is a foreign key (reference column) to the Products table.
unit is the number of products ordered in order_date.
```

**Example 3:**

```
Input: 
Products table:
+-------------+-----------------------+------------------+
| product_id  | product_name          | product_category |
+-------------+-----------------------+------------------+
| 1           | Leetcode Solutions    | Book             |
| 2           | Jewels of Stringology | Book             |
| 3           | HP                    | Laptop           |
| 4           | Lenovo                | Laptop           |
| 5           | Leetcode Kit          | T-shirt          |
+-------------+-----------------------+------------------+
Orders table:
+--------------+--------------+----------+
| product_id   | order_date   | unit     |
+--------------+--------------+----------+
| 1            | 2020-02-05   | 60       |
| 1            | 2020-02-10   | 70       |
| 2            | 2020-01-18   | 30       |
| 2            | 2020-02-11   | 80       |
| 3            | 2020-02-17   | 2        |
| 3            | 2020-02-24   | 3        |
| 4            | 2020-03-01   | 20       |
| 4            | 2020-03-04   | 30       |
| 4            | 2020-03-04   | 60       |
| 5            | 2020-02-25   | 50       |
| 5            | 2020-02-27   | 50       |
| 5            | 2020-03-01   | 50       |
+--------------+--------------+----------+
Output: 
+--------------------+---------+
| product_name       | unit    |
+--------------------+---------+
| Leetcode Solutions | 130     |
| Leetcode Kit       | 100     |
+--------------------+---------+
Explanation: 
Products with product_id = 1 is ordered in February a total of (60 + 70) = 130.
Products with product_id = 2 is ordered in February a total of 80.
Products with product_id = 3 is ordered in February a total of (2 + 3) = 5.
Products with product_id = 4 was not ordered in February 2020.
Products with product_id = 5 is ordered in February a total of (50 + 50) = 100.
```

---

## 题目（中文翻译）

**描述**  
给定两张表 **Products** 与 **Orders**，编写 SQL 查询，找出在 2020 年 2 月（February 2020）累计下单数量至少为 100 单的产品名称（product_name）以及对应的下单数量（total_units）。返回的结果表顺序不限。

**表结构**

`Products` 表：

| 列名            | 类型    |
|-----------------|---------|
| product_id      | int     |
| product_name    | varchar |
| product_category| varchar |

- `product_id` 为主键（primary key），唯一标识每个产品。  
- 本表记录公司的产品信息。

`Orders` 表：

| 列名      | 类型 |
|-----------|------|
| product_id| int  |
| order_date| date |
| unit      | int  |

- `product_id` 为外键（foreign key），引用 `Products` 表的 `product_id`。  
- `unit` 表示在 `order_date` 当天下单的产品数量。  
- 本表可能出现重复行。

**返回结果**  
返回包含以下两列的结果表：

| product_name | total_units |
|--------------|-------------|

- `product_name` 为满足条件的产品名称。  
- `total_units` 为该产品在 2020 年 2 月的累计下单数量（≥ 100）。

**示例**

```text
Products 表:
+------------+----------------------+------------------+
| product_id | product_name         | product_category |
+------------+----------------------+------------------+
| 1          | Leetcode Solutions   | Book             |
| 2          | Jewels of Stringology| Book             |
| 3          | HP                   | Laptop           |
| 4          | Lenovo               | ...              |
| ...        | ...                  | ...              |
+------------+----------------------+------------------+

Orders 表:
+------------+------------+------+
| product_id | order_date | unit |
+------------+------------+------+
| 1          | 2020-02-01 | 30   |
| 1          | 2020-02-15 | 80   |
| 2          | 2020-02-10 | 50   |
| 2          | 2020-02-20 | 60   |
| 3          | 2020-02-05 | 20   |
| ...        | ...        | ...  |
+------------+------------+------+
```

**解释**  
- 产品 `Leetcode Solutions`（product_id = 1）在 2020‑02‑01 与 2020‑02‑15 两天的 `unit` 分别为 30 与 80，累计为 110 ≥ 100，满足条件。  
- 产品 `Jewels of Stringology`（product_id = 2）累计为 110，也满足条件。  
- 其他产品累计下单数量不足 100，不出现在结果中。

**可能的查询示例**：

```sql
SELECT
    p.product_name,
    SUM(o.unit) AS total_units
FROM Products p
JOIN Orders o
    ON p.product_id = o.product_id
WHERE o.order_date BETWEEN '2020-02-01' AND '2020-02-29'
GROUP BY p.product_name
HAVING SUM(o.unit) >= 100;
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：

1. **遍历** `Orders` 表里的每一条记录，找出日期在 **2020‑02‑01 ~ 2020‑02‑29** 之间的行。  
2. 对于每一条符合条件的订单，拿到它的 `product_id`，然后在 `Products` 表里 **逐个查找**（线性搜索）对应的 `product_name`。  
3. 用一个 **列表** 把同一个 `product_id` 的 `unit` 累加起来。  
4. 最后遍历这个累计列表，把累计值 **≥ 100** 的产品挑出来，输出 `product_name` 与累计的 `unit`。

> - **哈希表**（Python 中的 `dict`）可以看作是 **查字典**：键是 `product_id`，值是累计的 `unit`，查询和写入都是 O(1)。  
> - 这里的“暴力”指的是对 `Products` 表的 **线性搜索**（每次都从头遍历），这会导致 **时间复杂度平方级** 的增长。

**为什么正确**：我们把所有符合日期范围的订单都加到了对应的产品上，只要累计的数量达到 100，就一定满足题目要求。  

**时间/空间复杂度**（大白话）：

- **时间复杂度**：  
  - 遍历 `Orders` 表是一次 O(N)（N 为订单条数）。  
  - 对每条符合日期的订单，又要在 `Products` 表里 **逐行搜索**，最坏情况要遍历全部 M 条产品记录。  
  - 因此整体是 **O(N·M)**，如果 N≈M，则相当于 **O(N²)**，也就是“平方级”，随着数据量稍微大一点，执行时间会迅速飙升。  
- **空间复杂度**：  
  - 只用了一个 `dict` 保存每个 `product_id` 的累计 `unit`，最多占用 O(M)（每个产品一条记录）的额外空间。

#### 代码（Python）

```python
# 假设已把两张表读入 Python 的列表中
# products: List[Tuple[int, str, str]]
# orders:   List[Tuple[int, str, int]]   # (product_id, order_date, unit)

from typing import List, Tuple

def brute_force(products: List[Tuple[int, str, str]],
                orders: List[Tuple[int, str, int]]) -> List[Tuple[str, int]]:
    # 1️⃣ 统计 2020‑02 的订单量（使用字典累计）
    feb_total = {}                         # product_id -> 已累计的 unit
    for pid, order_date, unit in orders:
        # 只保留 2020‑02 的记录
        if order_date.startswith('2020-02'):   # 简单的字符串前缀判断
            # 2️⃣ 线性搜索对应的 product_name（暴力）
            product_name = None
            for p_id, name, _ in products:     # 逐行遍历 Products 表
                if p_id == pid:
                    product_name = name
                    break
            # 如果找不到（理论上不会），直接跳过
            if product_name is None:
                continue

            # 3️⃣ 累加 unit
            feb_total[pid] = feb_total.get(pid, 0) + unit

    # 4️⃣ 过滤累计 ≥100 的产品，返回 (product_name, total_units)
    result = []
    for pid, total in feb_total.items():
        if total >= 100:
            # 再次线性搜索一次获取 product_name（保持“暴力”特性）
            for p_id, name, _ in products:
                if p_id == pid:
                    result.append((name, total))
                    break
    return result
```

#### 复杂度

- **时间复杂度**：`O(N·M)`（最坏等价于 O(N²)），因为每条符合日期的订单都要在 `Products` 表里线性搜索一次。  
- **空间复杂度**：`O(M)`，只用了一个字典来保存每个产品的累计订单量。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 出在两次对 `Products` 表的线性搜索——每次都要遍历完整个产品列表，导致时间呈平方增长。  
要把它降下来，只需要把 **产品信息的查找** 从 O(M) 降到 O(1)。这正是**哈希表（字典）**的用武之地：

1. **预处理**：把 `Products` 表一次性放进字典 `id -> product_name`，相当于把“查字典”这一步提前做好。  
2. **遍历 Orders**：仍然只遍历一次 `Orders` 表，过滤出 2020‑02 的记录。  
3. **累计**：使用另一个字典 `product_id -> total_units` 累加符合日期的 `unit`。  
4. **筛选**：遍历累计字典，把 `total_units ≥ 100` 的产品挑出来，直接从第一步的字典里取 `product_name`。

整个过程只需要 **两次线性遍历**（一次 Products，一次 Orders），没有嵌套循环，时间降到 **线性 O(N+M)**。

> **哈希表类比**：把产品表想象成一本 **电话簿**，键是电话号码（product_id），值是联系人姓名（product_name）。查一次电话簿就能立刻得到姓名，省掉了翻遍整本书的时间。

#### 代码（Python）

```python
from typing import List, Tuple

def optimal_solution(products: List[Tuple[int, str, str]],
                     orders: List[Tuple[int, str, int]]) -> List[Tuple[str, int]]:
    """
    返回满足条件的 (product_name, total_units) 列表，顺序不要求。
    """

    # 1️⃣ 把 Products 放进哈希表，键是 product_id，值是 product_name
    prod_name_by_id = {pid: name for pid, name, _ in products}
    # 2️⃣ 用另一个字典累计 2020‑02 的订单量
    feb_total = {}

    for pid, order_date, unit in orders:
        # 只保留 2020‑02 的订单（字符串切片或 datetime 都可以）
        if order_date[:7] == '2020-02':          # '2020-02-15'[:7] -> '2020-02'
            feb_total[pid] = feb_total.get(pid, 0) + unit

    # 3️⃣ 筛选累计 ≥100 的产品，直接从 prod_name_by_id 取名字
    result = []
    for pid, total in feb_total.items():
        if total >= 100:
            # prod_name_by_id 中一定有对应的名字（外键约束保证）
            result.append((prod_name_by_id[pid], total))

    return result
```

#### 复杂度

- **时间复杂度**：`O(N + M)`  
  - `O(M)` 用来一次性把 `Products` 建成字典。  
  - `O(N)` 用来遍历 `Orders` 并累计。  
  两者相加仍然是线性增长，远快于平方级。  
- **空间复杂度**：`O(N + M)`（实际只需 `O(M)` 存 `product_id → name`，以及 `O(K)` 存满足日期的累计，其中 `K ≤ M`），相较于暴力解没有额外的嵌套结构。

---

## 心得

- **核心技巧**：**哈希表（字典）实现 O(1) 查找**，配合一次遍历完成聚合（相当于 SQL 的 `GROUP BY`）。  
- **适用的题型**：  
  1. “统计某段时间内每个用户/商品的总量” 类的聚合题（如 LeetCode 1752. Check if Array Is Sorted and Rotated）。  
  2. “找出出现次数 ≥ k 的元素” （如 LeetCode 229. Majority Element II）。  
  3. “关联两张表后进行条件筛选” 的 SQL‑to‑Python 转换题。  
- **一句话总结**：**把需要频繁查询的数据提前放进哈希表，避免重复遍历，时间自然降到线性。**

---

## 反思

- **第一反应**：直接写两个 `for` 循环，遍历 Orders 再遍历 Products，感觉最直观。  
- **最容易踩的坑**：  
  - 日期过滤不严谨（比如只判断月份而忽略年份会把 2021‑02 的记录算进去）。  
  - 忘记把 `Orders` 表中可能出现的 **重复行**（同一天同产品多条记录）也要累计。  
  - 如果使用 `int` 累计，数量极大时要注意 Python 整数不溢出，但在某些语言需要防止 overflow。  
- **下次遇到同类题**：第一步先 **把主表（如 Products）转成字典**，再一次遍历关联表（如 Orders）完成聚合与过滤。这样思路清晰，代码也自然高效。