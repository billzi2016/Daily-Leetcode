# #1068. **产品销售分析 I** / Product Sales Analysis I

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/product-sales-analysis-i/)

---

## 题目（英文原版）

**Description**

Table: Sales
Table: Product
Write a solution to report the product_name, year, and price for each sale_id in the Sales table.
Return the resulting table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+-------------+-------+
| Column Name | Type  |
+-------------+-------+
| sale_id     | int   |
| product_id  | int   |
| year        | int   |
| quantity    | int   |
| price       | int   |
+-------------+-------+
(sale_id, year) is the primary key (combination of columns with unique values) of this table.
product_id is a foreign key (reference column) to Product table.
Each row of this table shows a sale on the product product_id in a certain year.
Note that the price is per unit.
```

**Example 2:**

```
+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| product_id   | int     |
| product_name | varchar |
+--------------+---------+
product_id is the primary key (column with unique values) of this table.
Each row of this table indicates the product name of each product.
```

**Example 3:**

```
Input: 
Sales table:
+---------+------------+------+----------+-------+
| sale_id | product_id | year | quantity | price |
+---------+------------+------+----------+-------+ 
| 1       | 100        | 2008 | 10       | 5000  |
| 2       | 100        | 2009 | 12       | 5000  |
| 7       | 200        | 2011 | 15       | 9000  |
+---------+------------+------+----------+-------+
Product table:
+------------+--------------+
| product_id | product_name |
+------------+--------------+
| 100        | Nokia        |
| 200        | Apple        |
| 300        | Samsung      |
+------------+--------------+
Output: 
+--------------+-------+-------+
| product_name | year  | price |
+--------------+-------+-------+
| Nokia        | 2008  | 5000  |
| Nokia        | 2009  | 5000  |
| Apple        | 2011  | 9000  |
+--------------+-------+-------+
Explanation: 
From sale_id = 1, we can conclude that Nokia was sold for 5000 in the year 2008.
From sale_id = 2, we can conclude that Nokia was sold for 5000 in the year 2009.
From sale_id = 7, we can conclude that Apple was sold for 9000 in the year 2011.
```

---

## 题目（中文翻译）

编写一个查询，报告 `Sales` 表中每个 `sale_id` 对应的 `product_name`、`year` 和 `price`。返回的结果表顺序任意。结果格式参见下面的示例。

**示例 1：**

**表结构**

```text
+-------------+-------+
| Column Name | Type  |
+-------------+-------+
| sale_id     | int   |
| product_id  | int   |
| year        | int   |
| quantity    | int   |
| price       | int   |
+-------------+-------+
```

- `(sale_id, year)` 为该表的主键（primary key，唯一值的列组合）。  
- `product_id` 为外键（foreign key，引用列），指向 `Product` 表。  
- 每一行记录了某一年对 `product_id` 对应的产品的销售情况。  
- 注意，`price` 为单件价格。

```text
+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| product_id   | int     |
| product_name | varchar |
+--------------+---------+
```

- `product_id` 为该表的主键（primary key，唯一值的列）。  
- 每一行记录了每个产品对应的名称。

**示例 3：**

```text
Input: 
Sales table:
+---------+------------+------+----------+-------+
| sale_id | product_id | year | quantity | price |
+---------+------------+------+----------+-------+ 
| 1       | 100        | 2008 | 10       | 5000  |
| 2       | 100        | 2009 | 12       | 5000  |
| 7       | 200        | 2011 | 15       | 9000  |
+---------+------------+------+----------+-------+

Product table:
+------------+--------------+
| product_id | product_name |
+------------+--------------+
| 100        | Nokia        |
| 200        | Apple        |
| 300        | Samsung      |
+------------+--------------+
```

**输出：**

```text
+--------------+-------+-------+
| product_name | year  | price |
+--------------+-------+-------+
| Nokia        | 2008  | 5000  |
| Nokia        | 2009  | 5000  |
| Apple        | 2011  | 9000  |
+--------------+-------+-------+
```

**解释：**  
- 从 `sale_id = 1` 可知 Nokia 在 2008 年的单件售价为 5000。  
- 从 `sale_id = 2` 可知 Nokia 在 2009 年的单件售价为 5000。  
- 从 `sale_id = 7` 可知 Apple 在 2011 年的单件售价为 9000。  

**约束条件**  
无。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

题目要求把 **Sales** 表和 **Product** 表按照 `product_id` 关联起来，得到每一笔销售对应的 `product_name、year、price`。  
最直接的想法就是：

1. **遍历 Sales 表的每一行**（把每一次 sale 当成一次“查询”）。  
2. **在 Product 表里逐行寻找相同的 `product_id`**，找到后取出对应的 `product_name`。  
3. 把 `product_name、year、price` 组成结果行。

这里用到的 **数据结构** 就是 **列表**（或数组），因为 LeetCode 的示例数据通常用表格形式展示，我们可以把每一行当成一个字典放进列表里。  

- **列表** 好比一本 **电话簿**，每本子页（元素）记录了一条信息。  
- **遍历** 就像我们一个个翻开电话簿的页码去找对应的名字。  

这种方法 **一定能得到正确答案**，因为我们对每一条销售记录都完整地检查了所有商品信息，保证不会漏掉任何匹配。

**时间/空间复杂度**（大白话）：

- 时间复杂度：`O(m * n)`，其中 `m` 是 Sales 表的行数，`n` 是 Product 表的行数。想象我们要把 **m 本电话簿** 的每一页都 **逐页** 对照 **n 本电话簿**，所以时间会呈乘积增长。  
- 空间复杂度：`O(1)`（不计输入输出），只用了常数级的临时变量。

#### 代码（Python）

```python
# 假设已经把两张表读取成列表，每行是一个字典
sales = [
    {"sale_id": 1, "product_id": 100, "year": 2008, "quantity": 10, "price": 5000},
    {"sale_id": 2, "product_id": 100, "year": 2009, "quantity": 12, "price": 5000},
    {"sale_id": 7, "product_id": 200, "year": 2011, "quantity": 15, "price": 9000},
]

products = [
    {"product_id": 100, "product_name": "Nokia"},
    {"product_id": 200, "product_name": "Apple"},
    {"product_id": 300, "product_name": "Samsung"},
]

def brute_force_join(sales, products):
    result = []                         # 用来存放最终答案
    for s in sales:                     # 对每一笔销售记录
        for p in products:              # 在商品表里逐行查找
            if s["product_id"] == p["product_id"]:   # 找到相同的 product_id
                # 取出需要的字段组成结果行
                result.append({
                    "product_name": p["product_name"],
                    "year": s["year"],
                    "price": s["price"]
                })
                break                    # 找到后立刻退出内层循环，避免多余比较
    return result

# 运行查看
for row in brute_force_join(sales, products):
    print(row)
```

**运行结果**（顺序不固定）  

```
{'product_name': 'Nokia', 'year': 2008, 'price': 5000}
{'product_name': 'Nokia', 'year': 2009, 'price': 5000}
{'product_name': 'Apple', 'year': 2011, 'price': 9000}
```

#### 复杂度  

- **时间复杂度**：`O(m * n)` — 如果 Sales 有 10 万行、Product 有 1 万行，最坏情况要比较 10^9 次，速度会很慢。  
- **空间复杂度**：`O(1)`（不计返回结果的存储） — 只用了几个临时变量。

---

### 2. 最优解  

#### 思路  

从暴力解可以看出，**瓶颈在于每次遍历 Sales 时，都要在 Product 表里重新遍历一次**。  
如果我们事先把 `product_id → product_name` 的映射保存下来（一次性遍历 Product 表），后面再查询时就可以 **直接用哈希表（字典）在 O(1) 时间拿到对应的名字**，不必再遍历。

核心步骤：

1. **构建哈希表**（Python 中的 `dict`），键是 `product_id`，值是 `product_name`。这一步相当于把商品表做成一本“**查字典**”，只要知道单词（product_id），马上能拿到页码（product_name）。  
2. **遍历 Sales 表**，对每一行直接在哈希表里找对应的 `product_name`，然后把 `product_name、year、price` 加入结果。  
3. 返回结果。

这样我们只遍历两遍表，时间从 `O(m * n)` 降到了 `O(m + n)`，在数据量大时会快很多。

#### 代码（Python）

```python
def optimal_join(sales, products):
    # 1️⃣ 把 product_id → product_name 建成哈希表
    prod_map = {p["product_id"]: p["product_name"] for p in products}
    # 这里使用字典推导式，一行代码完成，等价于：
    # prod_map = {}
    # for p in products:
    #     prod_map[p["product_id"]] = p["product_name"]

    result = []
    # 2️⃣ 只遍历一次 Sales 表
    for s in sales:
        # 在哈希表里 O(1) 时间拿到对应的商品名字
        name = prod_map.get(s["product_id"])
        # 如果题目保证外键完整性，这里一定能找到 name
        result.append({
            "product_name": name,
            "year": s["year"],
            "price": s["price"]
        })
    return result

# 运行示例
for row in optimal_join(sales, products):
    print(row)
```

**运行结果**（顺序同上）  

```
{'product_name': 'Nokia', 'year': 2008, 'price': 5000}
{'product_name': 'Nokia', 'year': 2009, 'price': 5000}
{'product_name': 'Apple', 'year': 2011, 'price': 9000}
```

#### 复杂度  

- **时间复杂度**：`O(m + n)` — 先遍历一次商品表（n），再遍历一次销售表（m），每次查询都是常数时间。相比暴力解快了很多。  
- **空间复杂度**：`O(n)` — 需要额外的哈希表来保存所有商品的映射，大小与商品表的行数成正比。

---

## 心得  

- **核心技巧**：使用 **哈希表（字典）** 把关联字段的映射提前准备好，实现 **一次遍历完成关联**（相当于 SQL 中的 `JOIN`）。  
- **适用场景**：  
  1. 两张表通过外键关联，需要把一个表的信息“贴”到另一张表上。  
  2. 需要在大数据量下频繁查询“键 → 值”关系，如用户 ID → 用户名、商品 ID → 商品信息。  
  3. 统计类题目里常用的 “计数/去重” 也可以通过哈希表实现。  
- **一句话总结**：**把关联键的映射预先存进字典，查询时直接 O(1) 取值，省去嵌套遍历**。

---

## 反思  

- **第一反应**：直接写 SQL `SELECT ... FROM Sales JOIN Product ON Sales.product_id = Product.product_id`，但因为要用 Python 实现，只好手动模拟 JOIN。  
- **最容易踩的坑**：  
  - 忘记处理外键不存在的情况（`dict.get` 可以返回 `None`，防止 KeyError）。  
  - 把结果顺序写死；题目说明返回顺序任意，代码不必强制排序。  
  - 在暴力实现里没有 `break`，导致同一个 `product_id` 被多次匹配，产生重复行。  
- **下次遇到同类题**：第一步先思考 **“能否把关联键预先做成哈希表？”**，如果能，就直接走 O(m+n) 的解法；如果关联条件更复杂，再考虑其他数据结构（如分组、双指针等）。