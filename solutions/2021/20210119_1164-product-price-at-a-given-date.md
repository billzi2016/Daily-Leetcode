# #1164. **Product Price at a Given Date** / Product Price at a Given Date

> 难度：中等 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/product-price-at-a-given-date/)

---

## 题目（英文原版）

**Description**

Table: Products
Initially, all products have price 10.
Write a solution to find the prices of all products on the date 2019-08-16.
Return the result table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| product_id    | int     |
| new_price     | int     |
| change_date   | date    |
+---------------+---------+
(product_id, change_date) is the primary key (combination of columns with unique values) of this table.
Each row of this table indicates that the price of some product was changed to a new price at some date.
```

**Example 2:**

```
Input: 
Products table:
+------------+-----------+-------------+
| product_id | new_price | change_date |
+------------+-----------+-------------+
| 1          | 20        | 2019-08-14  |
| 2          | 50        | 2019-08-14  |
| 1          | 30        | 2019-08-15  |
| 1          | 35        | 2019-08-16  |
| 2          | 65        | 2019-08-17  |
| 3          | 20        | 2019-08-18  |
+------------+-----------+-------------+
Output: 
+------------+-------+
| product_id | price |
+------------+-------+
| 2          | 50    |
| 1          | 35    |
| 3          | 10    |
+------------+-------+
```

---

## 题目（中文翻译）

表：Products  
最初，所有商品的价格均为 10。  
请编写 SQL 查询，找出 **2019-08-16** 当天所有商品的价格。返回结果表可以任意顺序。结果的列名和示例保持一致。

**示例 1**  

| Column Name | Type |
|-------------|------|
| product_id  | int  |
| new_price   | int  |
| change_date | date |

`(product_id, change_date)` 为该表的主键（primary key），即由唯一值组成的列组合。  
表中的每一行表示某个商品的价格在某一天被改为 `new_price`。

**示例 2**  

Input:  
Products 表：

| product_id | new_price | change_date |
|------------|-----------|-------------|
| 1          | 20        | 2019-08-14  |
| 2          | 50        | 2019-08-14  |
| 1          | 30        | 2019-08-15  |
| 1          | 35        | 2019-08-16  |
| 2          | 65        | 2019-08-17  |
| 3          | 20        | 2019-08-18  |

**解释**  
- 商品 1 在 2019‑08‑16 前的最新价格记录是 35，故返回 35。  
- 商品 2 在 2019‑08‑16 前的最新价格记录是 50（因为 65 的记录在 2019‑08‑17），故返回 50。  
- 商品 3 在 2019‑08‑16 前没有价格变更记录，仍保持初始价格 10，故返回 10。  

**约束条件**  
- 表中数据量符合普通 SQL 查询的处理范围。  
- `change_date` 为标准的 `date` 类型。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题的本质是**在一段价格变动记录中，找出每个商品在指定日期（2019‑08‑16）当天的价格**。  
最直接的想法是：

1. 先把所有出现过的 `product_id` 收集起来（相当于把所有商品的名字装进一个背包）。  
2. 对于背包里的每一个商品，遍历整张 `Products` 表，找出**所有**在 `change_date ≤ 2019‑08‑16` 的记录。  
3. 在这些记录里挑出 **日期最新** 的那条，它的 `new_price` 就是该商品在目标日期的价格。  
4. 如果某个商品在目标日期之前根本没有任何记录，说明它一直保持初始价 **10**。

> **类比**：把 `Products` 表想象成一本“价格变动日志”。我们要为每本商品的“账本”翻到 2019‑08‑16 那一页，找最近的那条记录。如果日志里根本没有这本商品的记录，那它一直是默认的 10 元。

这种做法一定能得到正确答案，因为我们穷举了 **所有可能的记录**，并严格挑选了满足条件且最新的一条。

#### 代码（Python）

```python
from datetime import date
from typing import List, Tuple

# ------------------- 模拟输入 -------------------
# 每条记录是 (product_id, new_price, change_date)
records: List[Tuple[int, int, str]] = [
    (1, 20, "2019-08-14"),
    (2, 50, "2019-08-14"),
    (1, 30, "2019-08-15"),
    (1, 35, "2019-08-16"),
    (2, 65, "2019-08-17"),
    (3, 20, "2019-08-18"),
]
# ------------------------------------------------

TARGET = date(2019, 8, 16)          # 目标日期
DEFAULT_PRICE = 10                  # 初始价格

# 1️⃣ 收集所有出现过的商品编号
product_ids = {r[0] for r in records}

# 2️⃣ 对每个商品暴力遍历所有记录
result = []                         # 用来存放 (product_id, price) 的最终答案
for pid in product_ids:
    latest_date = None              # 记录满足条件的最新日期
    latest_price = DEFAULT_PRICE    # 默认价格

    for p, price, d_str in records:
        d = date.fromisoformat(d_str)
        if p == pid and d <= TARGET:          # 必须是同一商品且日期不晚于目标日
            if latest_date is None or d > latest_date:
                latest_date = d
                latest_price = price

    # 如果根本没有满足条件的记录，latest_price 仍然是默认的 10
    result.append((pid, latest_price))

# 打印结果（任意顺序均可）
for pid, price in result:
    print(pid, price)
```

#### 复杂度

- **时间复杂度**：`O(P × N)`  
  - `P` 为商品种类数，`N` 为表中记录总行数。  
  - 用大白话说，就是“**每个商品都要把整张表看一遍**”，如果表有 10 000 条、商品有 1 000 种，最坏情况下要做 10 000 000 次比较。

- **空间复杂度**：`O(P)`  
  - 只用了一个集合保存商品编号以及最终结果列表，和表本身的大小无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**重复遍历整张表**——同一条记录会被所有商品检查一次，导致时间呈乘积增长。  
我们可以把 **“找最新日期的记录”** 这件事一次性完成：

1. **过滤**：只保留 `change_date ≤ 2019‑08‑16` 的记录。之后的记录根本不可能影响目标日期的价格。  
2. **排序**（或直接遍历保持最新）：把过滤后的记录按 `product_id` 分组，并在每组内部按 `change_date` **升序** 排序。这样每个商品的记录会从最早到最晚依次出现。  
3. **遍历一次**：使用一个字典 `price_by_product` 保存“截至当前遍历位置的最新价格”。遍历排序后的记录时，字典会被不断覆盖，最后留下的就是每个商品在目标日期的最新价格。  
4. **补全默认价**：有些商品在过滤后根本没有任何记录，这时字典里没有对应的键，需要手动补上默认价格 `10`。

> **类比**：把所有符合日期要求的记录排成一条队列，**排队的顺序本身就是时间顺序**。我们只需要把每个人的最新票价记在手心，后面来的票价会把旧的盖掉，最后手心里留下的就是当天的实际票价。

这一步只遍历一次（或一次排序后遍历一次），大幅降低了时间消耗。

#### 代码（Python）

```python
from datetime import date
from typing import List, Tuple, Dict
from collections import defaultdict

# ------------------- 模拟输入 -------------------
records: List[Tuple[int, int, str]] = [
    (1, 20, "2019-08-14"),
    (2, 50, "2019-08-14"),
    (1, 30, "2019-08-15"),
    (1, 35, "2019-08-16"),
    (2, 65, "2019-08-17"),
    (3, 20, "2019-08-18"),
]
# ------------------------------------------------

TARGET = date(2019, 8, 16)
DEFAULT_PRICE = 10

# 1️⃣ 只保留在目标日期之前或当天的记录
filtered = [
    (pid, price, date.fromisoformat(d_str))
    for pid, price, d_str in records
    if date.fromisoformat(d_str) <= TARGET
]

# 2️⃣ 按 product_id、change_date 升序排序
filtered.sort(key=lambda x: (x[0], x[2]))

# 3️⃣ 一遍遍历，实时更新字典中的最新价格
price_by_product: Dict[int, int] = {}
for pid, price, _ in filtered:
    price_by_product[pid] = price          # 后面的同一商品会覆盖前面的

# 4️⃣ 把所有出现过的商品都列出来（包括没有任何变动的商品）
all_products = {pid for pid, _, _ in records}
# 这里如果有的商品根本没有任何记录（题目保证都有），也会被补全

result = []
for pid in all_products:
    price = price_by_product.get(pid, DEFAULT_PRICE)  # 没有记录则用默认价 10
    result.append((pid, price))

# 打印（顺序无要求）
for pid, price in result:
    print(pid, price)
```

#### 复杂度

- **时间复杂度**：`O(N log N)`（如果使用排序）或 `O(N)`（若直接使用哈希表 + 单次遍历）  
  - `N` 为记录总数。  
  - 用大白话说，就是“**只扫一遍表**”，再加上 **一次排序**（排序的代价是 `N log N`，在数据量不大时完全可接受）。

- **空间复杂度**：`O(P)`  
  - 只用了一个字典保存每个商品的最新价格，`P` 为商品种类数。额外的 `filtered` 列表在最坏情况下也是 `O(N)`，但可以原地过滤来进一步省空间。

---

## 心得

- **核心技巧**：**时间线上的最新值**。把“在某个时间点之前的最新记录”转化为“遍历一次并实时覆盖”。  
- **适用场景**：  
  1. **历史状态查询**（如用户余额、库存快照）。  
  2. **最近一次事件**（如最近登录时间、最近一次登录 IP）。  
  3. **累计最大/最小值**（如每一天的最高气温）。  
- **一句话总结**：**把所有满足日期限制的记录按时间顺序排好，一遍遍历，用字典把“最新的价格”记住即可。**

---

## 反思

- **第一反应**：直接把每个商品的所有记录全部遍历一遍，找出符合条件的最新一条。  
- **最容易踩的坑**：  
  - 忽略了 **默认价格 10**（当商品在目标日期前没有任何记录时）。  
  - 日期比较时把字符串直接比较会出错，必须先转换成 `date` 类型。  
  - 如果直接使用 `max` 函数而不先过滤日期，会把目标日期之后的更高价格误认为是当天价格。  
- **下次遇到同类题**：第一步先 **过滤** 掐头去尾（只保留在目标时间之前的记录），然后 **按时间排序或一次遍历更新**，把“最新值”保存在哈希表里。这样可以把时间复杂度从 “商品 × 记录” 降到 “记录一次”。