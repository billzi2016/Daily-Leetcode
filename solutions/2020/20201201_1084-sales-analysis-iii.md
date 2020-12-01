# #1084. 销售分析 III / Sales Analysis III

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/sales-analysis-iii/)

---

## 题目（英文原版）

**Description**

Table: Product
Table: Sales
Write a solution to report the products that were only sold in the first quarter of 2019. That is, between 2019-01-01 and 2019-03-31 inclusive.
Return the result table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| product_id   | int     |
| product_name | varchar |
| unit_price   | int     |
+--------------+---------+
product_id is the primary key (column with unique values) of this table.
Each row of this table indicates the name and the price of each product.
```

**Example 2:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| seller_id   | int     |
| product_id  | int     |
| buyer_id    | int     |
| sale_date   | date    |
| quantity    | int     |
| price       | int     |
+-------------+---------+
This table can have duplicate rows.
product_id is a foreign key (reference column) to the Product table.
Each row of this table contains some information about one sale.
```

**Example 3:**

```
Input: 
Product table:
+------------+--------------+------------+
| product_id | product_name | unit_price |
+------------+--------------+------------+
| 1          | S8           | 1000       |
| 2          | G4           | 800        |
| 3          | iPhone       | 1400       |
+------------+--------------+------------+
Sales table:
+-----------+------------+----------+------------+----------+-------+
| seller_id | product_id | buyer_id | sale_date  | quantity | price |
+-----------+------------+----------+------------+----------+-------+
| 1         | 1          | 1        | 2019-01-21 | 2        | 2000  |
| 1         | 2          | 2        | 2019-02-17 | 1        | 800   |
| 2         | 2          | 3        | 2019-06-02 | 1        | 800   |
| 3         | 3          | 4        | 2019-05-13 | 2        | 2800  |
+-----------+------------+----------+------------+----------+-------+
Output: 
+-------------+--------------+
| product_id  | product_name |
+-------------+--------------+
| 1           | S8           |
+-------------+--------------+
Explanation: 
The product with id 1 was only sold in the spring of 2019.
The product with id 2 was sold in the spring of 2019 but was also sold after the spring of 2019.
The product with id 3 was sold after spring 2019.
We return only product 1 as it is the product that was only sold in the spring of 2019.
```

---

## 题目（中文翻译）

**描述**  
表：`Product`  
表：`Sales`  

编写一个查询，报告仅在 2019 年第一季度（即 2019-01-01 到 2019-03-31，含）售出的商品。返回结果表的顺序不限。结果格式参见下例。

**示例 1**

**示例 1：**  

```
+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| product_id   | int     |
| product_name | varchar |
| unit_price   | int     |
+--------------+---------+
```

`product_id` 为该表的主键（primary key），即唯一值列。每行记录表示一种商品的名称和单价。

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| seller_id   | int     |
| product_id  | int     |
| buyer_id    | int     |
| sale_date   | date    |
| quantity    | int     |
| price       | int     |
+-------------+---------+
```

该表可能出现重复行。`product_id` 为外键（foreign key），引用 `Product` 表。每行记录包含一次销售的相关信息。

**示例 2**

**输入**  

`Product` 表：

```
+------------+--------------+------------+
| product_id | product_name | unit_price |
+------------+--------------+------------+
| 1          | S8           | 1000       |
| 2          | G4           | 800        |
| 3          | iPhone       | 1400       |
+------------+--------------+------------+
```

`Sales` 表：

```
+-----------+------------+----------+------------+----------+-------+
| seller_id | product_id | buyer_id | sale_date  | quantity | price |
+-----------+------------+----------+------------+----------+-------+
| 1         | 1          | 1        | 2019-01-21 | 2        | 2000  |
| 1         | 2          | 2        | 2019-02-17 | 1        | 800   |
| 2         | 2          | 3        | 2019-06-02 | 1        | 800   |
| 3         | 3          | 4        | 2019-05-13 | 2        | 2800  |
+-----------+------------+----------+------------+----------+-------+
```

**输出**  

```
+-------------+--------------+
| product_id  | product_name |
+-------------+--------------+
| 1           | S8           |
+-------------+--------------+
```

**解释**  
- 商品 ID 为 1 的产品仅在 2019 年第一季度售出。  
- 商品 ID 为 2 的产品虽然在第一季度有售出，但也在之后的月份（如 2019-06-02）出现销售记录。  
- 商品 ID 为 3 的产品仅在第一季度之后有销售。  

因此，只返回商品 ID 为 1 的记录，因为它是唯一 **仅在 2019 年第一季度**（spring of 2019）售出的商品。

**约束条件**  
无

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**逐个产品检查它的所有销售记录**，只要发现该产品在 2019‑01‑01 到 2019‑03‑31 之外还有一次销售，就把它排除。  

- **数据结构**：  
  - `products` 表可以想象成一本商品目录，每本书（行）里记着商品的 `product_id`、`product_name`、`unit_price`。  
  - `sales` 表则像一本销售日志，里面每一行记录一次交易，包括 `product_id`、`sale_date` 等。  
  - 为了快速找到某个商品的所有销售记录，我们可以把 `sales` 按 `product_id` 分组，类似于把日志按商品名字归档。这里用 `defaultdict(list)`（相当于“字典里的字典”，key 是商品编号，value 是该商品的所有销售记录列表），就像把每本商品的所有交易放进它自己的抽屉里。

- **为什么正确**：  
  - 对每个商品我们都检查了它的 **全部** 销售日期。如果没有一次日期落在 “第一季度之外”，说明它 **只** 在第一季度出现过，符合题意。  
  - 只要出现一次不符合的日期，就立刻把商品标记为“不合格”，因为题目要求“仅在第一季度出售”，一次违规就足够把它踢出结果。

- **时间/空间复杂度**（大白话版）  
  - `n` 为 `sales` 表的行数（交易次数），`m` 为 `products` 表的行数（商品种类）。  
  - **时间**：我们要遍历所有销售记录一次来建立分组（`O(n)`），随后对每个商品检查它的所有交易（总共仍是遍历所有交易一次），所以总体是 **线性** 的 `O(n + m)`，在最坏情况下可以近似为 `O(n)`（因为 `n` 通常远大于 `m`）。  
  - **空间**：我们额外用了一个字典把每笔交易按商品存进去，需要额外的 `O(n)` 空间来保存这些引用。

#### 代码（Python）

```python
from collections import defaultdict
from datetime import datetime
from typing import List, Dict, Any

# ------------------- 辅助函数 -------------------
def str_to_date(s: str) -> datetime:
    """把 'YYYY-MM-DD' 字符串转成 datetime，便于比较"""
    return datetime.strptime(s, "%Y-%m-%d")

# ------------------- 暴力解 -------------------
def sales_analysis_bruteforce(products: List[Dict[str, Any]],
                              sales: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    返回只在 2019 年第一季度（1 月 1 日 ~ 3 月 31 日）出现过销售的商品。
    这里的实现完全按照“逐个商品检查所有交易”来写。
    """
    # 1. 把所有销售记录按 product_id 收集到一个 dict 中
    #    key: 商品 id，value: 该商品的所有 sale_date 列表
    sales_by_product = defaultdict(list)
    for rec in sales:
        pid = rec["product_id"]
        sale_date = str_to_date(rec["sale_date"])
        sales_by_product[pid].append(sale_date)   # 把日期放进对应商品的抽屉

    # 2. 定义第一季度的起止日期（左闭右闭）
    q1_start = datetime(2019, 1, 1)
    q1_end   = datetime(2019, 3, 31)

    # 3. 逐个商品检查
    answer = []
    for prod in products:
        pid = prod["product_id"]
        # 如果该商品根本没有任何销售记录，也不算“只在第一季度出售”，直接跳过
        if pid not in sales_by_product:
            continue

        # 检查它的每一次销售日期
        only_q1 = True
        for d in sales_by_product[pid]:
            if d < q1_start or d > q1_end:   # 只要出现一次不在区间的日期
                only_q1 = False
                break                         # 可以提前结束循环
        if only_q1:                           # 全部都在第一季度
            answer.append({
                "product_id": pid,
                "product_name": prod["product_name"]
            })
    return answer
```

#### 复杂度

- **时间复杂度**：`O(n + m)`  
  - `n` 为 `sales` 行数，`m` 为 `products` 行数。遍历一次 `sales` 来分组，再遍历一次 `products`（每个商品内部最多遍历它的所有销售记录，总和仍是 `n`），所以整体线性。  
  - 用大白话说，就是“看一遍销售日志，一遍商品目录”，不会出现指数级的爆炸。

- **空间复杂度**：`O(n)`  
  - 额外的 `sales_by_product` 把每条销售记录的日期保存了一遍，最坏情况下需要和原始 `sales` 表同等大小的空间。

---

### 2. 最优解

#### 思路  

暴力解已经是 **线性** 时间 `O(n)`，在大多数情况下已经足够快。不过我们可以把代码写得更简洁、一次遍历就直接得到答案，省去对每个商品二次遍历的“检查”过程。

关键观察：

1. **只需要两类集合**  
   - `sold_in_q1`：在第一季度出现过的商品集合。  
   - `sold_out_q1`：在第一季度之外出现过的商品集合。  

   最终符合要求的商品 = `sold_in_q1 - sold_out_q1`（只在 Q1 出现，且没有在 Q1 之外出现）。

2. **一次遍历即可得到两个集合**  
   - 读取每条销售记录时，判断它的日期是否在 Q1 区间，随后把对应的 `product_id` 放进相应的集合。  
   - 这样我们不需要把销售记录按商品分组，也不需要后续的“逐个商品检查”。  

3. **只需要把商品目录（product 表）和 `product_id` 关联**  
   - 通过 `product_id` 能快速在字典 `id -> name` 中查到商品名称，构造最终结果。

#### 代码（Python）

```python
from datetime import datetime
from typing import List, Dict, Any

def sales_analysis_optimal(products: List[Dict[str, Any]],
                           sales: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    O(n) 一遍遍历即可求解，只用两个集合记录“出现过的商品”。
    """
    # 1️⃣ 把 product_id -> product_name 建成字典，方便后面快速查表
    id_to_name = {p["product_id"]: p["product_name"] for p in products}

    # 2️⃣ 定义第一季度的起止时间（左闭右闭）
    q1_start = datetime(2019, 1, 1)
    q1_end   = datetime(2019, 3, 31)

    # 3️⃣ 两个集合：只要出现一次就加入对应集合
    sold_in_q1   = set()   # 在 Q1 出现过的商品 id
    sold_out_q1  = set()   # 在 Q1 之外出现过的商品 id

    for rec in sales:
        pid = rec["product_id"]
        sale_date = datetime.strptime(rec["sale_date"], "%Y-%m-%d")
        if q1_start <= sale_date <= q1_end:
            sold_in_q1.add(pid)
        else:
            sold_out_q1.add(pid)

    # 4️⃣ 只在 Q1 出现的商品 = 在 Q1 出现且不在 Q1 之外出现的集合
    only_q1_ids = sold_in_q1 - sold_out_q1

    # 5️⃣ 把 id 转成题目要求的输出结构
    result = [
        {"product_id": pid, "product_name": id_to_name[pid]}
        for pid in only_q1_ids
        if pid in id_to_name          # 防止 sales 表出现了 product 表里没有的 id（题目里不会出现，但加个保险）
    ]
    return result
```

#### 复杂度

- **时间复杂度**：`O(n + m)`  
  - 只遍历一次 `sales`（`n` 条记录）来填两个集合，遍历一次 `products`（`m` 条记录）来建立 `id_to_name`，整体仍是线性。  
  - 与暴力解的时间复杂度相同，但 **只用了两次遍历**，而不是“遍历 + 再遍历每个商品的子列表”，在常数因子上更小，实际运行更快。

- **空间复杂度**：`O(k + m)`  
  - `k` 为出现过的不同商品数量（`k ≤ n`），对应两个集合的大小。  
  - 再加上 `id_to_name` 字典占 `O(m)` 空间。  
  - 与暴力解的 `O(n)` 相比，省掉了把每条销售记录完整保存的额外列表，只保留商品 id，空间更紧凑。

---

## 心得

- **核心技巧**：**集合运算（Set） + 一次遍历**  
  用两个集合分别记录“出现过的商品”与“出现过的异常商品”，再通过集合差得到答案。集合的 `add`、`in`、集合差 `-` 都是 **O(1)** 均摊时间操作，非常适合过滤类问题。

- **适用的题型**  
  1. “只在某段时间出现”或“只出现过一次”的过滤题（如 **Sales Analysis I / II**）。  
  2. “出现过但未出现过另一种状态”的对比题（如 “找出只在 2020 年出现的用户”）。  
  3. “某属性的唯一出现”类题目（如 “只买过一种颜色的商品的用户”）。

- **一句话总结解题钥匙**：  
  **把“满足条件的”与“违反条件的”分别收进两个集合，最后用集合差直接得到只满足条件的对象。**

---

## 反思

- **第一反应**：看到“只在第一季度售出”，立刻想到对每个商品检查所有销售记录的**逐个验证**方式——最直观但代码稍显冗长。

- **最容易踩的坑**  
  1. **日期比较**：忘记把字符串转成 `datetime`，直接比较字符串会得到错误的结果（比如 `'2019-10-01' < '2019-2-01'`）。  
  2. **没有销售记录的商品**：这类商品既不在 Q1，也不在 Q1 之外，应该被排除。  
  3. **重复记录**：同一商品同一天可能出现多条，集合会自动去重，避免重复计数。  

- **下次遇到同类题的第一步**：  
  **先把“满足 X 条件的 id” 与 “出现 Y 条件的 id” 分别收集进集合**，再用集合运算得到最终答案——这样思路明确，代码简洁。