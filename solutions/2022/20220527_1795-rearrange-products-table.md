# #1795. 重新排列 Products 表 / Rearrange Products Table

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/rearrange-products-table/)

---

## 题目（英文原版）

**Description**

Table: Products
Write a solution to rearrange the Products table so that each row has (product_id, store, price). If a product is not available in a store, do not include a row with that product_id and store combination in the result table.
Return the result table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| product_id  | int     |
| store1      | int     |
| store2      | int     |
| store3      | int     |
+-------------+---------+
product_id is the primary key (column with unique values) for this table.
Each row in this table indicates the product's price in 3 different stores: store1, store2, and store3.
If the product is not available in a store, the price will be null in that store's column.
```

**Example 2:**

```
Input: 
Products table:
+------------+--------+--------+--------+
| product_id | store1 | store2 | store3 |
+------------+--------+--------+--------+
| 0          | 95     | 100    | 105    |
| 1          | 70     | null   | 80     |
+------------+--------+--------+--------+
Output: 
+------------+--------+-------+
| product_id | store  | price |
+------------+--------+-------+
| 0          | store1 | 95    |
| 0          | store2 | 100   |
| 0          | store3 | 105   |
| 1          | store1 | 70    |
| 1          | store3 | 80    |
+------------+--------+-------+
Explanation: 
Product 0 is available in all three stores with prices 95, 100, and 105 respectively.
Product 1 is available in store1 with price 70 and store3 with price 80. The product is not available in store2.
```

---

## 题目（中文翻译）

**描述**  
表：Products  

编写一个查询，将 **Products** 表重新排列，使每一行的形式为 **(product_id, store, price)**。如果某个商品在某家店铺没有对应的价格（即值为 `NULL`），则结果表中不应出现该 **product_id** 与 **store** 的组合。返回的结果表可以任意顺序。

**示例 1**

输入表 **Products**：

| product_id | store1 | store2 | store3 |
|------------|--------|--------|--------|
| 0          | 95     | 100    | 105    |
| 1          | 70     | NULL   | 80     |

输出表：

| product_id | store  | price |
|------------|--------|-------|
| 0          | store1 | 95    |
| 0          | store2 | 100   |
| 0          | store3 | 105   |
| 1          | store1 | 70    |
| 1          | store3 | 80    |

**解释**  
原表的每一行记录了商品在三个不同店铺（store1、store2、store3）的价格。查询需要将这些列“展开”为多行，每行只保留 **product_id**、店铺名称 **store**（列名对应的店铺）以及对应的 **price**。当某个店铺的价格为 `NULL` 时，表示该商品在该店铺不存在，故不应出现在结果中。

**约束条件**  
- 表中 `product_id` 为主键（primary key），即唯一且非空。  
- 表中可能出现 `NULL` 值，表示该商品在相应店铺没有价格。  
- 结果表的顺序不做要求。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

题目要求把原始的 **宽表**（每行有 `product_id`、`store1`、`store2`、`store3`）转换成 **长表**（每行只有 `product_id`、`store`、`price`），并且 **只保留有价格的记录**。  

可以把它想成把一张 **多列的价格清单** 拆成 **一条条的“商品‑店铺‑价格”**，就像把一本字典里每个词条的多个解释拆成“词‑解释‑编号”。  

最直接的做法是：

1. 按行遍历 `Products` 表（相当于逐行阅读字典的词条）。  
2. 对每一行，检查 `store1、store2、store3` 三个列的值。  
3. 只要某个列的值不是 `NULL`（在 Python 中对应 `None`），就把 `(product_id, store_name, price)` 加入结果。  

这样做 **一定正确**：我们没有遗漏任何非空的价格，也没有把空值误加入。

**时间复杂度**  
- 外层遍历每一行，设表有 `n` 行。  
- 内层检查 3 列（常数），所以总共是 `O(n)`。  
  - 大白话：如果表里有 1000 条商品记录，我们只会看 1000 次，每次看 3 次价格，时间随记录数线性增长。  

**空间复杂度**  
- 只需要存放输出结果，最坏情况下每行的 3 列全都有价格，结果行数会是 `3 * n`。因此空间是 `O(n)`（和输入规模同阶）。  

#### 代码（Python）

```python
from typing import List, Dict, Any

def rearrange_products_bruteforce(products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    暴力实现：把宽表转换为长表，只保留 price 非 None 的记录。
    参数:
        products: 每条记录是一个 dict，键包括 'product_id', 'store1', 'store2', 'store3'
    返回:
        长表记录的列表，每条记录包含 'product_id', 'store', 'price'
    """
    result = []                     # 用来保存最终的 (product_id, store, price) 三元组
    store_cols = ['store1', 'store2', 'store3']   # 需要展开的列名

    for row in products:            # 逐行遍历原始表
        pid = row['product_id']     # 商品编号
        for col in store_cols:      # 依次检查 store1、store2、store3
            price = row[col]        # 取出该列的价格
            if price is not None:   # 只保留非空的价格
                # 把列名（store1）转换成想要的 store 字段（store1 → store1）
                # 这里直接使用列名作为 store 的名字，实际题目中会是 'store1'、'store2'、'store3'
                result.append({
                    'product_id': pid,
                    'store': col,      # store 列名即为店铺标识
                    'price': price
                })
    return result
```

#### 复杂度  

- **时间复杂度**：`O(n)` — 随着商品数量线性增长，遍历一次表即可。  
- **空间复杂度**：`O(n)` — 最坏情况下会产生 `3n` 条结果记录，仍然是线性级别。  

---  

### 2. 最优解  

#### 思路  

在本题中，**暴力解已经是最优的**。  
瓶颈只会出现在**遍历所有行**的那一步，而这一步是必须的——没有看过的行我们根本不知道它的价格信息。  

唯一可以“优化”的，是**代码的可读性和可维护性**：把“列名列表”抽象出来，使用一次循环处理所有店铺列，避免手写三遍相同的逻辑。  

因此最优解和暴力解在时间、空间上是一样的，只是写法更简洁、更易于扩展（比如如果表里还有 `store4`、`store5`，只需要在 `store_cols` 中加上对应列名即可）。  

#### 代码（Python）

```python
def rearrange_products_optimal(products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    最优实现：核心思路与暴力相同，只是把店铺列抽象为列表，代码更简洁。
    """
    store_cols = [c for c in products[0].keys() if c.startswith('store')]  # 自动发现所有 store 列
    result = []

    for row in products:
        pid = row['product_id']
        for store in store_cols:
            price = row[store]
            if price is not None:
                result.append({
                    'product_id': pid,
                    'store': store,
                    'price': price
                })
    return result
```

> **关键点解释**  
> - `store_cols = [c for c in products[0].keys() if c.startswith('store')]`  
>   把所有以 `store` 开头的列名收集起来，等价于 `['store1','store2','store3']`，但如果以后表结构变了，这段代码仍然能自动适配。  
> - 其余逻辑与暴力解相同，保持 `O(n)` 时间、`O(n)` 空间。

#### 复杂度  

- **时间复杂度**：`O(n)` — 必须遍历每一行，且每行只检查常数个店铺列。  
- **空间复杂度**：`O(n)` — 结果列表的大小随输入线性增长。  

---

## 心得  

- **核心技巧**：**宽表转长表（Unpivot）**。在数据库里常用 `UNION ALL` 或 `CROSS APPLY` 实现，在编程语言里就是**遍历行 + 遍历列**。  
- **适用的题型**：  
  1. 将多列的属性（如 `score_math、score_english、score_science`）拆成 “学生‑科目‑分数”。  
  2. 将每个月的销售额列（`jan、feb、mar…`）转成 “月份‑销售额”。  
  3. 将用户的多电话号码列（`phone_home、phone_work、phone_mobile`）转成 “用户‑电话类型‑号码”。  
- **一句话总结解题钥匙**：**把每一列都当成一次独立的记录来收集，只保留非空的那几条**。

---

## 反思  

- **第一反应**：看到“把表重新排列成 (product_id, store, price)”，立刻想到 **遍历每行、遍历每个 store 列**，把非空的价格抽出来。  
- **最容易踩的坑**：  
  - 忘记过滤 `NULL`（Python 中的 `None`），会产生 `price` 为 `None` 的无效记录。  
  - 硬编码列名（只写 `store1、store2、store3`），导致表结构若有变化代码失效。  
  - 把列名直接当作数值使用，需要注意输出的 `store` 字段应该是列名本身（如 `'store1'`），而不是对应的价格。  
- **下次遇到同类题**：第一步就**确认需要“展开”哪些列**，把这些列收集进一个列表，然后**统一用双层循环**生成目标记录，同时**记得过滤空值**。这样既保证正确性，又容易扩展。