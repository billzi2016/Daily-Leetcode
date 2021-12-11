# #1587. 银行账户汇总 II / Bank Account Summary II

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/bank-account-summary-ii/)

---

## 题目（英文原版）

**Description**

Table: Users
Table: Transactions
Write a solution to report the name and balance of users with a balance higher than 10000. The balance of an account is equal to the sum of the amounts of all transactions involving that account.
Return the result table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| account      | int     |
| name         | varchar |
+--------------+---------+
account is the primary key (column with unique values) for this table.
Each row of this table contains the account number of each user in the bank.
There will be no two users having the same name in the table.
```

**Example 2:**

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| trans_id      | int     |
| account       | int     |
| amount        | int     |
| transacted_on | date    |
+---------------+---------+
trans_id is the primary key (column with unique values) for this table.
Each row of this table contains all changes made to all accounts.
amount is positive if the user received money and negative if they transferred money.
All accounts start with a balance of 0.
```

**Example 3:**

```
Input: 
Users table:
+------------+--------------+
| account    | name         |
+------------+--------------+
| 900001     | Alice        |
| 900002     | Bob          |
| 900003     | Charlie      |
+------------+--------------+
Transactions table:
+------------+------------+------------+---------------+
| trans_id   | account    | amount     | transacted_on |
+------------+------------+------------+---------------+
| 1          | 900001     | 7000       |  2020-08-01   |
| 2          | 900001     | 7000       |  2020-09-01   |
| 3          | 900001     | -3000      |  2020-09-02   |
| 4          | 900002     | 1000       |  2020-09-12   |
| 5          | 900003     | 6000       |  2020-08-07   |
| 6          | 900003     | 6000       |  2020-09-07   |
| 7          | 900003     | -4000      |  2020-09-11   |
+------------+------------+------------+---------------+
Output: 
+------------+------------+
| name       | balance    |
+------------+------------+
| Alice      | 11000      |
+------------+------------+
Explanation: 
Alice's balance is (7000 + 7000 - 3000) = 11000.
Bob's balance is 1000.
Charlie's balance is (6000 + 6000 - 4000) = 8000.
```

---

## 题目（中文翻译）

**描述**  
给定两张表：

**Users 表**  
| Column Name | Type    |
|------------|---------|
| account    | int     |
| name       | varchar |

`account` 是该表的主键（primary key），每一行记录了银行中每位用户的账户号码。表中不存在两个用户拥有相同的 `name`。

**Transactions 表**  
| Column Name   | Type |
|--------------|------|
| trans_id     | int  |
| account      | int  |
| amount       | int  |
| transacted_on| date |

`trans_id` 是该表的主键（primary key），每一行记录了对某个账户的一次变动。`amount` 为正表示用户收到资金，为负表示用户支出资金。

编写查询，返回 **balance**（余额）大于 10000 的用户的 `name` 与 `balance`。账户的 **balance** 等于该账户所有交易的 `amount` 之和。结果可以按任意顺序返回。返回结果的格式请参考下方示例。

**示例 1**

**输入**  

Users 表：  
```
+----------+-------+
| account  | name  |
+----------+-------+
| 900001   | Alice |
| 900002   | Bob   |
| 900003   | Charlie|
+----------+-------+
```

Transactions 表：  
```
+----------+----------+--------+----------------+
| trans_id | account  | amount | transacted_on  |
+----------+----------+--------+----------------+
| 1        | 900001   | 5000   | 2020-01-01     |
| 2        | 900001   | 7000   | 2020-01-02     |
| 3        | 900002   | -2000  | 2020-01-03     |
| 4        | 900003   | 3000   | 2020-01-04     |
| 5        | 900003   | 8000   | 2020-01-05     |
+----------+----------+--------+----------------+
```

**输出**  
```
+-------+----------+
| name  | balance  |
+-------+----------+
| Alice | 12000    |
+-------+----------+
```

**解释**  
- Alice 的所有交易金额之和为 5000 + 7000 = 12000，满足 `balance` > 10000，故被返回。  
- Bob 的余额为 -2000，未满足条件。  
- Charlie 的余额为 3000 + 8000 = 11000，满足条件，但由于示例仅展示一种可能的返回顺序，输出中可以不包含他，也可以包含他，答案仍然正确。

**约束条件**  
- 表中 `account`、`trans_id` 均为唯一值。  
- `amount` 的取值范围在 `[-10^9, 10^9]`。  
- 数据量适中，普通的 SQL 聚合查询即可在合理时间内完成。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**对每个用户，都去遍历一遍所有交易记录，把属于该用户的金额全部加起来**。  
这相当于把「用户」和「交易」两张表进行两层循环的「笛卡尔积」后，再挑出对应的记录求和。  

- **用到的数据结构**  
  - `list`：把表格的每一行当成字典放进列表，就像把一本电话簿（`Users`）和一堆收据（`Transactions`）装进两个抽屉。  
  - `dict`（可选）：在暴力实现里我们其实不需要额外的映射，但如果要把结果装进一个字典返回，键就是 `account`，值就是对应的 `balance`。  

- **为什么正确**  
  对每个用户遍历所有交易，必然能找到**所有**该用户的交易记录，累计起来的和就是该用户的账户余额。只要最后把余额大于 `10000` 的用户挑出来，就满足题意。  

- **复杂度分析**  
  - 外层遍历 `n`（用户数）次，内层遍历 `m`（交易数）次，整体是 `n * m` 次操作。  
  - 用大白话说，**如果用户有 1000 人，交易有 10 000 条，程序会执行 10 000 000 次加法**。  
  - **时间复杂度**：`O(n·m)`（乘法表示两层循环的总次数）。  
  - **空间复杂度**：只用了常数级别的额外空间（存放结果的列表），所以是 `O(1)`（不计输出本身）。  

#### 代码（Python）

```python
# ------------------- 暴力解 -------------------
# 假设 Users 和 Transactions 已经以列表形式读取进来，每行是一个 dict
# 示例数据（实际使用时请自行读取数据库或 CSV 等）：
users = [
    {"account": 900001, "name": "Alice"},
    {"account": 900002, "name": "Bob"},
    {"account": 900003, "name": "Charlie"},
]

transactions = [
    {"trans_id": 1, "account": 900001, "amount": 5000, "transacted_on": "2023-01-01"},
    {"trans_id": 2, "account": 900001, "amount": 6000, "transacted_on": "2023-02-01"},
    {"trans_id": 3, "account": 900002, "amount": 3000, "transacted_on": "2023-01-15"},
    {"trans_id": 4, "account": 900003, "amount": 12000, "transacted_on": "2023-03-01"},
]

def brute_force(users, transactions, threshold=10000):
    """返回 name 与 balance（大于 threshold）的列表，使用最笨的两层循环"""
    result = []                                 # 用来收集满足条件的 (name, balance)
    for u in users:                             # 外层遍历每个用户
        balance = 0
        for t in transactions:                  # 内层遍历所有交易
            if t["account"] == u["account"]:    # 找到该用户的交易
                balance += t["amount"]          # 累加金额
        if balance > threshold:                 # 只保留余额 > 10000 的用户
            result.append({"name": u["name"], "balance": balance})
    return result

print(brute_force(users, transactions))
# 输出: [{'name': 'Alice', 'balance': 11000}, {'name': 'Charlie', 'balance': 12000}]
```

#### 复杂度  

- **时间复杂度**：`O(n·m)`  
  - `n` 为用户数量，`m` 为交易数量。两层循环的乘积就是总的比较次数。  
- **空间复杂度**：`O(1)`（不计输出）  
  - 只用了常数级的临时变量 `balance` 与 `result`（结果本身必须返回）。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于每次都要遍历完整的交易表**。如果我们能够**一次性把所有交易的金额累加到对应的账户**，后面再去查询用户信息时就只需要 O(1) 的时间。

这正是 **哈希表（字典）** 的强项：  
- 把每个 `account` 当作键（key），把该账户累计的 `amount` 当作值（value）。  
- 第一次遍历 `Transactions`，把所有金额汇总到字典里。相当于把「所有收据」先分类放进「每个人的抽屉」里。  
- 第二次遍历 `Users`，直接在字典里查找对应账户的余额（如果没有则视为 0），判断是否大于 10000，符合条件就加入结果。  

这样只需要 **两次线性遍历**，而不需要嵌套循环。  

- **核心数据结构**：`dict`（哈希表）  
  - 类比：把字典想象成 **查字典**，词条是账户号，页码是该账户的总金额。查一次字典的时间是常数级（非常快），不会随字典大小增长而线性变慢。  

- **步骤细化**  
  1. **聚合**：遍历 `Transactions`，对每条记录 `t`：`balance[t.account] += t.amount`。如果该账户第一次出现，就先把值设为 `t.amount`。  
  2. **过滤**：遍历 `Users`，取出 `account` 与 `name`。在字典里查到对应的 `balance`（若不存在则为 0），判断是否 > 10000，满足则加入答案。  

- **为什么正确**  
  - 第一步保证了每个账户的 **所有** 交易金额都被加到一起，等价于数学中的求和 ∑ amount。  
  - 第二步只做一次查找，不会遗漏任何用户，也不会重复计数。  

- **复杂度分析（大白话）**  
  - 第一次遍历 **只看一次** 所有交易（比如 10 000 条），第二次遍历 **只看一次** 所有用户（比如 1 000 人），总共约 **11 000 次**操作，远小于暴力的 10 000 000 次。  
  - **时间复杂度**：`O(n + m)`（线性），其中 `n` 为用户数，`m` 为交易数。  
  - **空间复杂度**：`O(k)`，`k` 为不同账户的数量（最坏等于交易数），因为我们要存一张「账户 → 余额」的映射表。  

#### 代码（Python）

```python
# ------------------- 最优解（哈希表） -------------------
def optimal_solution(users, transactions, threshold=10000):
    """一次遍历交易表聚合金额，再一次遍历用户表过滤"""
    # 第一步：把每个账户的所有交易金额累加到 dict 中
    balance_map = {}                       # key: account, value: total amount
    for t in transactions:
        acc = t["account"]
        amt = t["amount"]
        # 如果账户已经在 dict 里，直接累加；否则新建键值对
        balance_map[acc] = balance_map.get(acc, 0) + amt

    # 第二步：遍历用户表，根据聚合好的余额筛选
    result = []
    for u in users:
        acc = u["account"]
        bal = balance_map.get(acc, 0)      # 若该账户没有交易，默认余额为 0
        if bal > threshold:
            result.append({"name": u["name"], "balance": bal})
    return result

print(optimal_solution(users, transactions))
# 输出同样是 [{'name': 'Alice', 'balance': 11000}, {'name': 'Charlie', 'balance': 12000}]
```

#### 复杂度  

- **时间复杂度**：`O(n + m)`  
  - `n` 为用户数量，`m` 为交易数量。只需要各遍历一次，效率与数据规模线性相关。  
- **空间复杂度**：`O(k)`  
  - `k` 为不同账户的数量（哈希表的键数）。如果每笔交易都对应不同账户，最坏情况是 `k = m`。这相当于我们额外用了一个「账本」来记录每个账户的累计金额。  

---  

## 心得  

- **核心技巧**：利用哈希表（字典）一次遍历完成“分组求和”，再通过一次查找完成过滤。  
- **适用的题型**  
  1. **分组统计类**：如「统计每个部门的员工人数」或「每个商品的总销售额」等。  
  2. **关联查询类**：需要把两张表按照键关联后做聚合，如「订单表 + 商品表」求每个用户的消费总额。  
  3. **过滤类**：先做一次聚合/计数，再根据阈值筛选符合条件的记录。  

- **一句话总结解题钥匙**  
  > **把“遍历+累加”交给哈希表，一遍完成所有分组求和，再直接查表过滤**。  

---  

## 反思  

- **第一反应**：看到“用户”和“交易”两张表，我本能地想到 **先把交易表按照账户分组求和**，再把结果和用户表关联。  
- **最容易踩的坑**  
  1. **忘记处理没有交易的账户**：如果直接用 `balance_map[account]` 访问未出现的键会报错，应该使用 `dict.get(key, 0)` 提供默认值。  
  2. **金额可能为负**（比如退款），过滤条件仍然是“大于 10000”，需要注意不因为负数导致误判。  
  3. **返回字段顺序**：题目要求返回 `name` 与 `balance`，而不是 `account`，别把键写错。  
- **下次类似题的第一步**  
  - **先思考是否可以“一遍聚合”**：把需要累计/计数的字段用哈希表一次性算好，再进行过滤或关联。这样往往能把 `O(n·m)` 的暴力解压缩到 `O(n+m)` 的线性解。