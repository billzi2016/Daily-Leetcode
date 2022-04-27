# #1757. 可回收且低脂的产品 / Recyclable and Low Fat Products

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/recyclable-and-low-fat-products/)

---

## 题目（英文原版）

**Description**

Table: Products
Write a solution to find the ids of products that are both low fat and recyclable.
Return the result table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| product_id  | int     |
| low_fats    | enum    |
| recyclable  | enum    |
+-------------+---------+
product_id is the primary key (column with unique values) for this table.
low_fats is an ENUM (category) of type ('Y', 'N') where 'Y' means this product is low fat and 'N' means it is not.
recyclable is an ENUM (category) of types ('Y', 'N') where 'Y' means this product is recyclable and 'N' means it is not.
```

**Example 2:**

```
Input: 
Products table:
+-------------+----------+------------+
| product_id  | low_fats | recyclable |
+-------------+----------+------------+
| 0           | Y        | N          |
| 1           | Y        | Y          |
| 2           | N        | Y          |
| 3           | Y        | Y          |
| 4           | N        | N          |
+-------------+----------+------------+
Output: 
+-------------+
| product_id  |
+-------------+
| 1           |
| 3           |
+-------------+
Explanation: Only products 1 and 3 are both low fat and recyclable.
```

---

## 题目（中文翻译）

**描述**  
表（Table）：`Products`  

编写一个查询，找出同时满足以下条件的产品 `id`：  
- `low_fats` 为 `'Y'`（表示该产品是低脂的）  
- `recyclable` 为 `'Y'`（表示该产品是可回收的）  

返回结果表，顺序不限。结果格式参照下例。

**示例 1**  

表结构：

| 列名（Column Name） | 类型（Type） |
|----------------------|--------------|
| `product_id`         | `int`        |
| `low_fats`           | `enum`（枚举）|
| `recyclable`         | `enum`（枚举）|

- `product_id` 为主键（primary key），即唯一值列。  
- `low_fats` 为枚举（`enum`）类型，取值为 `'Y'` 或 `'N'`，其中 `'Y'` 表示该产品是低脂的，`'N'` 表示不是。  
- `recyclable` 为枚举（`enum`）类型，取值为 `'Y'` 或 `'N'`，其中 `'Y'` 表示该产品是可回收的，`'N'` 表示不是。

**示例 2**  

**输入**  

`Products` 表：

```
+------------+----------+------------+
| product_id | low_fats | recyclable |
+------------+----------+------------+
| 0          | Y        | N          |
| 1          | Y        | Y          |
| 2          | N        | Y          |
| 3          | Y        | Y          |
| 4          | N        | N          |
+------------+----------+------------+
```

**输出**  

```
+------------+
| product_id |
+------------+
| 1          |
| 3          |
+------------+
```

**约束条件**  
无。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题本质上是 **在表中筛选满足两个条件的记录**。  
可以把 `Products` 表想象成一本 **商品目录**，每一行是一件商品的卡片，卡片上写着：

- `product_id`：商品的唯一编号（相当于身份证号）  
- `low_fats`：是否低脂，用 `'Y'`（Yes）或 `'N'`（No）表示  
- `recyclable`：是否可回收，同样用 `'Y'` / `'N'` 表示  

我们要找的商品，就是 **“低脂且可回收”** 的卡片。最直接的办法就是 **把所有卡片一张张翻看**，只要同时满足 `low_fats == 'Y'` **并且** `recyclable == 'Y'`，就把它的 `product_id` 收集起来。

在代码里，这种“一张张翻看”的过程可以用 **循环遍历**（`for`）实现；判断两个属性是否都是 `'Y'` 用 **逻辑与**（`and`）即可。  

> 为什么它一定对？  
> 因为我们检查了表中的每一行，凡是满足条件的必然被记录下来，凡是不满足的必然被过滤掉。没有遗漏，也没有误判。

**时间/空间复杂度的大白话解释**  

- **时间复杂度**：我们要看 **每一行**，如果表里有 `n` 条记录，就要做 `n` 次检查。我们把这种“看一遍表”的工作记作 **O(n)**，其中的 `n` 代表记录数。  
- **空间复杂度**：只需要一个列表来存放答案，最坏情况下所有商品都符合条件，列表里会有 `n` 个 `product_id`。所以空间也是 **O(n)**。如果只关心返回结果本身，这个空间是必须的。

#### 代码（Python）

```python
# 假设我们已经把 Products 表读取成一个 list of dict，
# 每条记录用 dict 表示，键就是列名
products = [
    {"product_id": 0, "low_fats": "Y", "recyclable": "N"},
    {"product_id": 1, "low_fats": "Y", "recyclable": "Y"},
    {"product_id": 2, "low_fats": "N", "recyclable": "Y"},
    {"product_id": 3, "low_fats": "Y", "recyclable": "Y"},
    {"product_id": 4, "low_fats": "N", "recyclable": "N"},
]

def low_fat_and_recyclable_bruteforce(products):
    """暴力遍历所有商品，挑出同时满足 low_fats='Y' 且 recyclable='Y' 的 product_id"""
    answer = []                       # 用来保存符合条件的 id
    for row in products:              # 逐行检查
        # 同时检查两个字段是否都是 'Y'
        if row["low_fats"] == "Y" and row["recyclable"] == "Y":
            answer.append(row["product_id"])   # 符合就加入答案
    return answer

# 运行示例
print(low_fat_and_recyclable_bruteforce(products))   # 输出: [1, 3]
```

#### 复杂度

- **时间复杂度**：`O(n)` — 需要遍历 `n` 条记录，每条记录做常数次比较。  
- **空间复杂度**：`O(k)` — `k` 为符合条件的商品数量，最坏 `k = n`，即 `O(n)`。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈其实不在时间**（已经是线性扫描，无法再快），而在 **代码的简洁度** 与 **可读性**。  
我们可以把“遍历 + 条件判断”这一步浓缩成 **列表推导式**（list comprehension），这是一种 Pythonic 的写法：一行代码完成遍历、判断和收集，逻辑更直观，且内部实现仍然是线性遍历。

核心技巧：**使用列表推导式过滤满足条件的元素**。  
类比：如果你在超市挑选水果，想要挑出所有“红色且甜的”，你可以一次性把所有水果摆在桌子上，然后用手指快速挑出符合的，这就是“一次遍历+条件筛选”。列表推导式正是把这个过程用代码表达出来。

#### 代码（Python）

```python
def low_fat_and_recyclable_optimal(products):
    """
    使用列表推导式一次性完成遍历、条件过滤和结果收集。
    返回所有 low_fats='Y' 且 recyclable='Y' 的 product_id。
    """
    return [
        row["product_id"]                # 需要保存的字段
        for row in products              # 对每一行进行遍历
        if row["low_fats"] == "Y" and row["recyclable"] == "Y"   # 同时满足两个条件
    ]

# 运行示例
print(low_fat_and_recyclable_optimal(products))   # 输出: [1, 3]
```

#### 复杂度

- **时间复杂度**：`O(n)` — 与暴力解相同，仍然只需要一次线性遍历。  
- **空间复杂度**：`O(k)` — 只存放符合条件的 `product_id`，最坏 `O(n)`。  
- **对比**：相较于显式的 `for` 循环，列表推导式在 **代码行数** 与 **可读性** 上更优，但算法本身的时间/空间界限没有改变，因为我们已经达到了理论上的最优（只能遍历一次）。

---

## 心得

- **核心技巧**：利用 **一次遍历 + 条件过滤**（列表推导式或 `filter`）快速得到满足多重条件的记录。  
- **适用的题型**  
  1. 从表/列表中筛选满足 **多个属性** 条件的元素（如“年龄大于 18 且城市是北京的用户”）。  
  2. 需要 **去重** 或 **统计** 符合条件的子集时（配合 `set`、`sum` 等）。  
- **一句话总结解题钥匙**：**“遍历一次，条件一起写，直接把符合的拿出来”。**

---

## 反思

- **第一反应**：看到“low_fats”和“recyclable”都是 `'Y'`/`'N'`，立刻想到 **过滤**，于是想用 `for` 循环逐行判断。  
- **最容易踩的坑**  
  - 把 `'Y'` / `'N'` 当成布尔值直接使用，导致逻辑错误（应显式比较字符串）。  
  - 忘记返回 `product_id` 而是返回整行记录，导致答案格式不对。  
  - 对空表或全部不符合条件的情况没有考虑，代码仍能正常返回空列表，需在解释时说明。  
- **下次遇到同类题**：第一步先 **确认过滤条件**（几个字段、取值是什么），然后 **决定用一次遍历**（`for` 循环或列表推导式）一次性筛选出来。这样既保证正确性，又能写出简洁的代码。