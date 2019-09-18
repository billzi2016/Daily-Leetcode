# #584. 查找客户推荐人 / Find Customer Referee

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/find-customer-referee/)

---

## 题目（英文原版）

**Description**

Table: Customer
Find the names of the customer that are either:
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
| referee_id  | int     |
+-------------+---------+
In SQL, id is the primary key column for this table.
Each row of this table indicates the id of a customer, their name, and the id of the customer who referred them.
```

**Example 2:**

```
Input: 
Customer table:
+----+------+------------+
| id | name | referee_id |
+----+------+------------+
| 1  | Will | null       |
| 2  | Jane | null       |
| 3  | Alex | 2          |
| 4  | Bill | null       |
| 5  | Zack | 1          |
| 6  | Mark | 2          |
+----+------+------------+
Output: 
+------+
| name |
+------+
| Will |
| Jane |
| Bill |
| Zack |
+------+
```

---

## 题目（中文翻译）

## 题目描述  

给定表 **Customer**（见下表），请找出满足以下任意一种情况的客户姓名（`name`）：

- 没有被任何其他客户推荐，即 `referee_id` 为 `NULL`；
- 没有推荐过任何其他客户，即该客户的 `id` 没有出现在 `referee_id` 列中。

返回的结果表可以任意顺序排列，列名仅为 `name`。

**表结构**  

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| name        | varchar |
| referee_id  | int     |
+-------------+---------+
```

在 SQL 中，`id` 为该表的主键。每一行记录了客户的唯一标识 `id`、姓名 `name`，以及推荐该客户的客户的 `id`（`referee_id`）。

## 示例  

**示例 1**

**输入**  

Customer 表：

```
+----+------+------------+
| id | name | referee_id |
+----+------+------------+
| 1  | Will | null       |
| 2  | Jane | null       |
| 3  | Alex | 2          |
| 4  | Bill | null       |
| 5  | Zack | 1          |
| 6  | Mark | 2          |
+----+------+------------+
```

**输出**  

```
+------+
| name |
+------+
| Will |
| Jane |
| Bill |
| Zack |
+------+
```

**解释**  

- `Will`、`Jane`、`Bill` 的 `referee_id` 为 `NULL`，满足“没有被推荐”的条件。  
- `Bill` 的 `id`（4）以及 `Zack` 的 `id`（5）均未出现在 `referee_id` 列中，满足“没有推荐其他客户”的条件。  

因此上述四位客户的姓名被返回。

## 约束  

- 表中数据量适中，无需考虑极端大数据的性能优化。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题要求找出 **满足任意一种情况** 的客户姓名：

1. **没有被任何人推荐**（`referee_id` 为 `NULL`）。  
2. **没有推荐过其他客户**（自己的 `id` 没有出现在别人的 `referee_id` 中）。

可以把表想象成一个“推荐网络”。  
- 每一行是一个人（`id`、`name`），还有一个指向推荐人的指针 `referee_id`。  
- “没有被推荐” 就像字典里找不到对应的释义，`referee_id` 这格子是空的。  
- “没有推荐别人” 就像我们在字典里找不到这个词的解释，说明没有人把它当作推荐人。

最直接的做法就是：

1. **遍历一遍**，把所有出现过的 `referee_id`（非 `NULL`）收集到一个集合 `referred_by_others`。这一步相当于把所有“被当作推荐人”的 id 记下来。  
2. 再**遍历第二遍**，对每一行判断：  
   - `referee_id` 为 `None` → “没有被推荐”。  
   - 或者 `id` 不在 `referred_by_others` 中 → “没有推荐别人”。  
   满足任意一个条件就把 `name` 加入答案。

> **为什么正确？**  
> - 第一步把所有 **被当作推荐人的 id** 完整地记录下来，后面只要判断 `id` 是否在这个集合里，就能精准地知道该客户是否曾经推荐过别人。  
> - 第二步的两个判定正好对应题目要求的两种情况，逻辑互不冲突，取 **或**（`or`）即可。

#### 代码（Python）

```python
from typing import List, Dict

def find_customer_referee(customers: List[Dict]) -> List[str]:
    """
    :param customers: 每条记录是一个字典，键包括 'id', 'name', 'referee_id'
    :return: 符合条件的客户姓名列表（顺序不要求）
    """
    # 1️⃣ 收集所有被当作推荐人的 id（排除 NULL）
    referred_by_others = set()
    for c in customers:
        if c['referee_id'] is not None:          # None 对应 SQL 里的 NULL
            referred_by_others.add(c['referee_id'])
    # 2️⃣ 再遍历一次，挑选满足「没有被推荐」或「没有推荐别人」的客户
    answer = []
    for c in customers:
        no_be_referred = c['referee_id'] is None          # 情况 1
        no_refer_others = c['id'] not in referred_by_others  # 情况 2
        if no_be_referred or no_refer_others:
            answer.append(c['name'])
    return answer
```

#### 复杂度

- **时间复杂度：** `O(n)`  
  - 第一次遍历收集 `referee_id` 用 `O(n)`，第二次遍历判断同样是 `O(n)`，总共线性增长。  
  - 这里的 `n` 就是表中行数，换句话说，遍历一次表只需要花 **和行数成正比** 的时间。

- **空间复杂度：** `O(m)`（`m ≤ n`）  
  - 额外使用的集合 `referred_by_others` 最多存放所有非 `NULL` 的 `referee_id`，数量不会超过表的行数。  
  - 其余的临时变量都是常数级别的空间开销。

---

### 2. 最优解

#### 思路  

在上面的“暴力解”里我们已经是 **线性** 的时间复杂度，没有多余的嵌套循环，已经是最优的时间表现。  
唯一还能改进的地方是 **一次遍历就完成**，不必分两次：

- 在遍历的同时，维护两个集合：  
  1. `null_set` – 保存所有 `referee_id` 为 `NULL` 的 `id`（即“没有被推荐”的人）。  
  2. `referee_set` – 保存所有出现过的 `referee_id`（即“被别人推荐过”的人）。  

- 再遍历一次（或者在同一次遍历的 **后半段** 再检查一次），只要 `id` 属于 `null_set` **或** 不在 `referee_set`，就符合条件。

因为我们已经在一次遍历里收集了所有必要的信息，第二遍只做 **O(1)** 的集合查询，整体仍是 `O(n)`，但只需要 **两次线性遍历**，代码更简洁，且只使用了常数级别的额外空间（两个集合的大小合计不超过 `n`）。

> **核心概念**：  
> - **集合（Set）** 在 Python 中的查找是 **常数时间**（`O(1)`），类似于生活中的“字典”，可以在几乎不花时间的情况下判断一个单词是否在词典里。  
> - **一次遍历 + 集合查询** 的组合，是处理“出现/不存在”这类关系的常见高效手段。

#### 代码（Python）

```python
def find_customer_referee_one_pass(customers: List[Dict]) -> List[str]:
    """
    只用两次遍历（一次收集信息，一次产生答案），保持 O(n) 时间、O(n) 空间。
    """
    # 第一次遍历：收集信息
    null_set = set()      # 存放没有被推荐的客户 id
    referee_set = set()   # 存放所有被当作推荐人的 id
    for c in customers:
        if c['referee_id'] is None:          # 没有被推荐
            null_set.add(c['id'])
        else:                                 # 被别人推荐，记录推荐人的 id
            referee_set.add(c['referee_id'])

    # 第二次遍历：生成答案
    answer = []
    for c in customers:
        if c['id'] in null_set or c['id'] not in referee_set:
            answer.append(c['name'])
    return answer
```

#### 复杂度

- **时间复杂度：** `O(n)`  
  - 两次线性遍历，都是对每行做 **常数时间** 的操作（集合的 `add` / `in`），总共仍是与行数成正比。

- **空间复杂度：** `O(n)`  
  - `null_set` 与 `referee_set` 合计最多存放 `n` 个 id，属于线性空间。

---

## 心得

- **核心技巧**：利用 **集合（Set）** 快速判断“出现 / 未出现”。  
- **适用场景**：  
  1. “找出表中没有关联到另一张表的记录”。  
  2. “找出数组中出现一次的元素（与出现多次的区别）”。  
  3. “找出未被引用的资源（如未被任何订单使用的商品）”。  
- **一句话总结**：**把“是否出现”转化为集合查找，就能把嵌套循环的 O(n²) 降到 O(n)。**

## 反思

- **第一反应**：直接遍历两次，先把所有 `referee_id` 收集起来，再判断每行是否满足条件。  
- **最容易踩的坑**：  
  - 忽略 `NULL`（在 Python 中对应 `None`）的处理，导致错误的集合内容。  
  - 在判断 “没有推荐别人” 时，误用了 `referee_id` 而不是检查自己的 `id` 是否出现在别人的 `referee_id` 中。  
- **下次类似题**：第一步先 **确定需要哪些“出现 / 不出现”的关系**，把这些关系用 **集合** 记录下来，再在第二遍直接查表得到答案。这样思路清晰、实现简洁。