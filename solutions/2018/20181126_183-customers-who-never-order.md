# #183. 从未下单的客户 / Customers Who Never Order

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/customers-who-never-order/)

---

## 题目（英文原版）

**Description**

Table: Customers
Table: Orders
Write a solution to find all customers who never order anything.
Return the result table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| name        | varchar |
+-------------+---------+
id is the primary key (column with unique values) for this table.
Each row of this table indicates the ID and name of a customer.
```

**Example 2:**

```
+-------------+------+
| Column Name | Type |
+-------------+------+
| id          | int  |
| customerId  | int  |
+-------------+------+
id is the primary key (column with unique values) for this table.
customerId is a foreign key (reference columns) of the ID from the Customers table.
Each row of this table indicates the ID of an order and the ID of the customer who ordered it.
```

**Example 3:**

```
Input: 
Customers table:
+----+-------+
| id | name  |
+----+-------+
| 1  | Joe   |
| 2  | Henry |
| 3  | Sam   |
| 4  | Max   |
+----+-------+
Orders table:
+----+------------+
| id | customerId |
+----+------------+
| 1  | 3          |
| 2  | 1          |
+----+------------+
Output: 
+-----------+
| Customers |
+-----------+
| Henry     |
| Max       |
+-----------+
```

---

## 题目（中文翻译）

**描述**  
表：Customers  
表：Orders  

编写一个查询，找出所有 **从未下单的客户**（never order anything）。返回结果表，顺序任意。结果格式见下例。

**示例 1**  

**Customers 表结构**  

| Column Name | Type    |
|-------------|---------|
| id          | int     |
| name        | varchar |

- `id` 为 **主键（primary key）**（唯一值列）。  
- 每行记录表示一个客户的 ID 和姓名。

**Orders 表结构**  

| Column Name | Type |
|-------------|------|
| id          | int  |
| customerId  | int  |

- `id` 为 **主键（primary key）**。  
- `customerId` 为 **外键（foreign key）**，引用 **Customers** 表的 `id`。  
- 每行记录表示一个订单的 ID 以及下单客户的 ID。

**示例 3**  

输入  

Customers 表：

| id | name  |
|----|-------|
| 1  | Joe   |
| 2  | Henry |
| 3  | Sam   |
| 4  | Max   |

Orders 表：

| id | customerId |
|----|------------|
| 1  | 3          |
| 2  | 1          |

输出  

| Customers |
|-----------|
| Henry     |
| Max       |

**约束条件**  
无

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：**遍历每一个顾客**，再 **遍历一次订单表** 看看这位顾客的 `id` 是否出现在 `Orders.customerId` 里。  
- **数据结构**：这里我们把两张表都看成 Python 中的 `list[dict]`（列表里的字典），比如  
  ```python
  customers = [{'id':1,'name':'Joe'}, ...]
  orders    = [{'id':1,'customerId':3}, ...]
  ```  
  `list` 就像一本装满卡片的抽屉，`dict` 就像每张卡片上写的内容。  
- **为什么正确**：如果在遍历完所有订单后，仍然没有发现该顾客的 `id`，说明这位顾客从未下过单，应该把他的名字加入答案。  

#### 代码（Python）  

```python
def customers_never_order_brute(customers, orders):
    """
    暴力解：双层循环检查每个顾客是否出现在订单表中
    :param customers: List[Dict]，每个元素形如 {'id': int, 'name': str}
    :param orders:    List[Dict]，每个元素形如 {'id': int, 'customerId': int}
    :return: List[str]，所有从未下单的顾客姓名
    """
    result = []                     # 用来存放答案
    for cust in customers:          # 外层遍历每个顾客
        has_order = False           # 标记该顾客是否有订单
        for o in orders:            # 内层遍历所有订单
            if o['customerId'] == cust['id']:
                has_order = True    # 发现一次匹配，就说明有订单
                break               # 不必再继续检查这位顾客的其他订单
        if not has_order:           # 没有任何匹配，说明从未下单
            result.append(cust['name'])
    return result
```

#### 复杂度  

- **时间复杂度**：`O(N * M)`（N 为顾客数，M 为订单数）。  
  - 这里的 `O(N * M)` 可以想象成 **两层循环**，每层都要遍历一次列表，最坏情况下要把 N 张卡片都和 M 张卡片比较一次。  
- **空间复杂度**：`O(1)`（不计答案列表的额外空间）。  
  - 只用了几个额外的变量 `has_order`、`result`，和输入规模无关。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈在于每次都要遍历完整个订单表**。  
如果我们事先把所有出现过的 `customerId` 记录下来，后面只需要 **一次查找** 就能判断顾客是否下过单。  

- **核心数据结构**：**集合（set）**，它底层使用哈希表实现，查找时间是 **常数级 O(1)**，就像在一本**查字典**：把单词（这里是 `customerId`）当作键，字典会直接给出对应的页码（是否存在）。  
- 步骤  
  1. 遍历 `Orders`，把每条记录的 `customerId` 放进集合 `ordered_set`。  
  2. 再遍历 `Customers`，如果某个顾客的 `id` **不在** `ordered_set` 中，就说明他从未下单，加入答案。  

这样每张表只遍历一次，时间从 `O(N*M)` 降到 `O(N+M)`，空间多用了一个集合 `O(M)`。

#### 代码（Python）  

```python
def customers_never_order_optimal(customers, orders):
    """
    最优解：使用集合（哈希表）记录出现过的 customerId，随后一次遍历判断
    :param customers: List[Dict]，同上
    :param orders:    List[Dict]，同上
    :return: List[str]，所有从未下单的顾客姓名
    """
    # 第一步：把所有下单过的顾客 id 收集到集合中
    ordered_set = {o['customerId'] for o in orders}   # 集合推导式，时间 O(M)

    # 第二步：遍历顾客表，挑选不在集合里的顾客
    result = [c['name'] for c in customers if c['id'] not in ordered_set]  # 时间 O(N)

    return result
```

#### 复杂度  

- **时间复杂度**：`O(N + M)`  
  - `N` 是顾客数，`M` 是订单数。我们只各遍历一次列表，集合的插入和查询都是常数时间。相比暴力的 `O(N*M)`，大幅降低了运算量。  
- **空间复杂度**：`O(M)`（集合 `ordered_set` 需要存放所有出现过的 `customerId`）。  
  - 这相当于在“查字典”时需要额外准备一本只记录出现过的单词的词表，大小随订单数线性增长。

---

## 心得  

- **核心技巧**：**利用哈希集合（set）进行一次性去重/快速查找**。  
- **适用的题型**  
  1. “找出没有匹配的元素”类问题，例如 `Employees` 与 `Departments` 的左连接查询。  
  2. “数组/列表去重后求交集/差集”，如找出只在 A 中出现而不在 B 中出现的元素。  
  3. “频次统计”类问题，先把出现过的键放进集合或字典，再做判断。  
- **一句话总结解题钥匙**：**先把“常用的查询”预处理成 O(1) 的哈希结构，再遍历主表做一次判定**。

---

## 反思  

- **第一反应**：看到两张表，想到 **左连接** 或 **子查询**，于是自然会写出双层循环的暴力实现。  
- **最容易踩的坑**  
  - **空表**：如果 `Orders` 为空，集合会是空集合，代码仍然能正常工作。  
  - **重复订单**：同一个 `customerId` 可能出现多次，集合会自动去重，避免重复计数。  
  - **字段命名不统一**：务必确认 `customerId` 与 `Customers.id` 对应，否则会出现键不匹配的错误。  
- **下次遇到同类题**：第一步先思考 **“我需要快速判断某个元素是否出现过吗？”**，如果答案是 **是**，立刻构造 **集合 / 哈希表**，再进行一次线性遍历。