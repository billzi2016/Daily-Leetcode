# #1581. 未进行任何交易的访客 / Customer Who Visited but Did Not Make Any Transactions

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/customer-who-visited-but-did-not-make-any-transactions/)

---

## 题目（英文原版）

**Description**

Table: Visits
Table: Transactions
Write a solution to find the IDs of the users who visited without making any transactions and the number of times they made these types of visits.
Return the result table sorted in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| visit_id    | int     |
| customer_id | int     |
+-------------+---------+
visit_id is the column with unique values for this table.
This table contains information about the customers who visited the mall.
```

**Example 2:**

```
+----------------+---------+
| Column Name    | Type    |
+----------------+---------+
| transaction_id | int     |
| visit_id       | int     |
| amount         | int     |
+----------------+---------+
transaction_id is column with unique values for this table.
This table contains information about the transactions made during the visit_id.
```

**Example 3:**

```
Input: 
Visits
+----------+-------------+
| visit_id | customer_id |
+----------+-------------+
| 1        | 23          |
| 2        | 9           |
| 4        | 30          |
| 5        | 54          |
| 6        | 96          |
| 7        | 54          |
| 8        | 54          |
+----------+-------------+
Transactions
+----------------+----------+--------+
| transaction_id | visit_id | amount |
+----------------+----------+--------+
| 2              | 5        | 310    |
| 3              | 5        | 300    |
| 9              | 5        | 200    |
| 12             | 1        | 910    |
| 13             | 2        | 970    |
+----------------+----------+--------+
Output: 
+-------------+----------------+
| customer_id | count_no_trans |
+-------------+----------------+
| 54          | 2              |
| 30          | 1              |
| 96          | 1              |
+-------------+----------------+
Explanation: 
Customer with id = 23 visited the mall once and made one transaction during the visit with id = 12.
Customer with id = 9 visited the mall once and made one transaction during the visit with id = 13.
Customer with id = 30 visited the mall once and did not make any transactions.
Customer with id = 54 visited the mall three times. During 2 visits they did not make any transactions, and during one visit they made 3 transactions.
Customer with id = 96 visited the mall once and did not make any transactions.
As we can see, users with IDs 30 and 96 visited the mall one time without making any transactions. Also, user 54 visited the mall twice and did not make any transactions.
```

---

## 题目（中文翻译）

**描述**  
表 `Visits`  
表 `Transactions`  

编写一个查询，找出 **访问了但没有产生任何交易的客户（customer）** 的 `customer_id`，以及他们出现此类访问的次数。返回结果表，顺序任意即可。结果格式参考下方示例。

**示例 1**

**表结构**  

`Visits`  

| 列名          | 类型 |
|---------------|------|
| visit_id      | int  |
| customer_id   | int  |

`visit_id` 为该表唯一标识列，记录了到访商城的客户信息。

`Transactions`  

| 列名            | 类型 |
|-----------------|------|
| transaction_id  | int  |
| visit_id        | int  |
| amount          | int  |

`transaction_id` 为该表唯一标识列，记录了对应 `visit_id` 的交易信息。

**示例输入**  

```
Visits
+----------+-------------+
| visit_id | customer_id |
+----------+-------------+
| 1        | 23          |
| 2        | 9           |
| 4        | 30          |
| 5        | 54          |
| 6        | 96          |
| 7        | 54          |
| 8        | 54          |
+----------+-------------+

Transactions
+----------------+----------+--------+
| transaction_id | visit_id | amount |
+----------------+----------+--------+
| ... (已截断)   |
+----------------+----------+--------+
```

**约束条件**  
无

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每一次访问都和所有交易记录逐一比对**，看这次 `visit_id` 在 `Transactions` 表里有没有出现过：

1. 读取 `Visits` 表的每一行 `(visit_id, customer_id)`。  
2. 再遍历一遍 `Transactions` 表的每一行，检查 `transaction.visit_id == visit.visit_id`。  
3. 如果一次遍历完所有交易都没有找到匹配，说明这一次访问没有任何交易，于是把对应的 `customer_id` 的计数加 1。  

> **数据结构类比**：  
> - `Visits` 就像一张 **来客登记表**，每行记录一次来访的“身份证”。  
> - `Transactions` 像 **收银机的收据本**，每张收据里会写下对应的 `visit_id`。  
> - 暴力遍历就相当于每次来客登记完，都把 **收据本从头到尾翻一遍**，寻找匹配的收据。

**为什么正确**：只要我们把每一次访问和所有交易都比对一次，就一定能判断出该访问是否产生了交易。只要统计所有“没有匹配”的访问，就得到答案。

**复杂度分析（大白话）**：

- 假设 `Visits` 表有 `n` 条记录，`Transactions` 表有 `m` 条记录。  
- 对每一条访问（`n` 次）我们都要遍历所有交易（`m` 次），所以总共要做 `n × m` 次比较。  
- 这就是 **O(n·m)**，如果 `n`、`m` 都是几千甚至几万，计算量会很大。  
- 空间上我们只用到常量级的额外变量（计数器），所以是 **O(1)**。

#### 代码（Python）

```python
# ---------- 暴力解 ----------
# 输入：两张表分别用 list[dict] 表示
visits = [
    {"visit_id": 1, "customer_id": 23},
    {"visit_id": 2, "customer_id": 9},
    {"visit_id": 4, "customer_id": 30},
    {"visit_id": 5, "customer_id": 54},
    {"visit_id": 6, "customer_id": 96},
    {"visit_id": 7, "customer_id": 54},
    {"visit_id": 8, "customer_id": 54},
]

transactions = [
    {"transaction_id": 101, "visit_id": 1, "amount": 20},
    {"transaction_id": 102, "visit_id": 4, "amount": 15},
    {"transaction_id": 103, "visit_id": 5, "amount": 30},
    {"transaction_id": 104, "visit_id": 5, "amount": 40},
    {"transaction_id": 105, "visit_id": 7, "amount": 10},
]

def brute_force(visits, transactions):
    # 用 dict 保存每个 customer_id 的“无交易访问次数”
    result = {}
    for v in visits:                         # 对每一次访问
        has_tx = False                       # 标记该访问是否有交易
        for t in transactions:               # 暴力遍历所有交易
            if t["visit_id"] == v["visit_id"]:
                has_tx = True                # 找到匹配，说明有交易
                break
        if not has_tx:                       # 没有任何交易
            cid = v["customer_id"]
            result[cid] = result.get(cid, 0) + 1   # 计数 +1

    # 把 dict 转成列表，方便查看（顺序不要求）
    return [{"customer_id": k, "no_tx_visits": v} for k, v in result.items()]

print(brute_force(visits, transactions))
```

**运行结果示例**（可能的输出顺序）：

```text
[{'customer_id': 9, 'no_tx_visits': 1},
 {'customer_id': 30, 'no_tx_visits': 1},
 {'customer_id': 96, 'no_tx_visits': 1},
 {'customer_id': 54, 'no_tx_visits': 1}]
```

#### 复杂度

- **时间复杂度**：`O(n·m)` —— 每条访问都要遍历所有交易。  
  > *大白话*：如果 Visits 有 1000 条，Transactions 也有 1000 条，就要比较 1,000,000 次。
- **空间复杂度**：`O(k)`，`k` 为出现“无交易访问”的不同顾客数。  
  > 这里的额外空间只用来存放计数，和原始数据规模无关，算作 **O(1)**（常数级）。


---

### 2. 最优解

#### 思路  

从暴力解我们可以看到 **瓶颈** 出在 **每一次访问都要遍历所有交易**。  
如果我们能够**把交易表事先整理成一个可以快速查找的结构**，那么每次检查访问时只需要 **O(1)** 的时间。

**优化步骤**：

1. **把所有已发生交易的 `visit_id` 放进一个集合（hash set）**。  
   - 集合在 Python 中是 `set`，底层实现是哈希表，查找元素的时间几乎是 **常数时间**（O(1)），就像在字典里查词一样快。  
2. 再遍历 `Visits` 表：
   - 如果当前 `visit_id` 不在上面得到的集合里，说明这次访问没有任何交易，直接把对应 `customer_id` 的计数加 1。  
3. 最后把计数结果输出即可。

> **数据结构类比**：  
> - 把所有“有交易的来客编号”放进一本 **速查手册**（集合），查询是否在手册里就像在字典里找单词，立刻就能得到答案。  
> - 这样我们只需要 **一次遍历** 交易表（把手册写好），再 **一次遍历** 访问表（用手册快速检查），总共只是 `n + m` 次操作。

**复杂度分析**：

- 先遍历 `Transactions`，把 `visit_id` 放进集合，耗时 `O(m)`。  
- 再遍历 `Visits`，每次检查集合的时间是 `O(1)`，共 `O(n)`。  
- 总时间 = `O(n + m)`，线性增长，远快于 `O(n·m)`。  
- 额外空间需要保存集合和计数字典，最多是 `O(m + k)`，其中 `k` 为不同的顾客数。  

#### 代码（Python）

```python
# ---------- 最优解 ----------
def optimal_solution(visits, transactions):
    # 1️⃣ 把所有出现过交易的 visit_id 收集到集合里
    visited_with_tx = {t["visit_id"] for t in transactions}
    # 这里用 set 推导式，一行代码就完成，类似把所有单词装进字典

    # 2️⃣ 再遍历 Visits，统计那些不在集合里的访问
    counter = {}                         # customer_id -> 无交易访问次数
    for v in visits:
        if v["visit_id"] not in visited_with_tx:   # O(1) 查找
            cid = v["customer_id"]
            counter[cid] = counter.get(cid, 0) + 1

    # 3️⃣ 把结果转成列表返回（可以按任意顺序，这里按 customer_id 排序更好读）
    result = [
        {"customer_id": cid, "no_tx_visits": cnt}
        for cid, cnt in sorted(counter.items())
    ]
    return result

print(optimal_solution(visits, transactions))
```

**运行结果示例**（排序后）：

```text
[{'customer_id': 9, 'no_tx_visits': 1},
 {'customer_id': 30, 'no_tx_visits': 1},
 {'customer_id': 54, 'no_tx_visits': 1},
 {'customer_id': 96, 'no_tx_visits': 1}]
```

#### 复杂度

- **时间复杂度**：`O(n + m)`  
  > *大白话*：如果 Visits 有 1000 条，Transactions 也有 1000 条，只需要大约 2000 次操作，比 1,000,000 次快很多。  
- **空间复杂度**：`O(m + k)`（`m` 为交易数，`k` 为不同顾客数）  
  > 这里的额外空间是我们新建的集合和计数字典，都是线性规模的。

---

## 心得

- **核心技巧**：利用 **哈希表 / 集合** 实现「一次遍历+常数时间查询」的思想。  
- **适用的题型**  
  1. “找出在 A 表出现但在 B 表未出现的记录”  
  2. “统计只在一张表中出现的元素”  
  3. “快速判断某个键是否存在于另一集合中”  
- **解题钥匙**：**先把能快速查询的数据预处理成哈希结构，再遍历主表**。

---

## 反思

- **第一反应**：直接套用两层循环，逐行比对——这就是暴力解。  
- **最容易踩的坑**  
  - 忘记把 `visit_id` 唯一性考虑进去，导致同一次访问多次计数。  
  - 忽视 `customer_id` 可能出现多次，需要累计计数而不是覆盖。  
  - 边界情况：如果 `Transactions` 为空，所有访问都算“无交易”，代码仍需正确处理。  
- **下次遇到同类题**：第一步先 **思考是否可以把其中一张表转成集合/字典**，利用 O(1) 查找把时间复杂度从 `O(n·m)` 降到 `O(n+m)`。