# #1193. 每月交易 I / Monthly Transactions I

> 难度：中等 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/monthly-transactions-i/)

---

## 题目（英文原版）

**Description**

Table: Transactions
Write an SQL query to find for each month and country, the number of transactions and their total amount, the number of approved transactions and their total amount.
Return the result table in any order.
The query result format is in the following example.

**Examples**

**Example 1:**

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| id            | int     |
| country       | varchar |
| state         | enum    |
| amount        | int     |
| trans_date    | date    |
+---------------+---------+
id is the primary key of this table.
The table has information about incoming transactions.
The state column is an enum of type ["approved", "declined"].
```

**Example 2:**

```
Input: 
Transactions table:
+------+---------+----------+--------+------------+
| id   | country | state    | amount | trans_date |
+------+---------+----------+--------+------------+
| 121  | US      | approved | 1000   | 2018-12-18 |
| 122  | US      | declined | 2000   | 2018-12-19 |
| 123  | US      | approved | 2000   | 2019-01-01 |
| 124  | DE      | approved | 2000   | 2019-01-07 |
+------+---------+----------+--------+------------+
Output: 
+----------+---------+-------------+----------------+--------------------+-----------------------+
| month    | country | trans_count | approved_count | trans_total_amount | approved_total_amount |
+----------+---------+-------------+----------------+--------------------+-----------------------+
| 2018-12  | US      | 2           | 1              | 3000               | 1000                  |
| 2019-01  | US      | 1           | 1              | 2000               | 2000                  |
| 2019-01  | DE      | 1           | 1              | 2000               | 2000                  |
+----------+---------+-------------+----------------+--------------------+-----------------------+
```

---

## 题目（中文翻译）

**描述**  
表：Transactions  

编写一条 SQL 查询，统计每个月（`month`）和每个国家（`country`）的交易情况，包括：  
- 交易总数（`transaction_count`）以及交易金额总和（`total_amount`）  
- 状态为 “approved” 的交易数量（`approved_transaction_count`）以及这些已批准交易的金额总和（`approved_total_amount`）  

查询结果可以按任意顺序返回。  

查询结果的列名及含义如下（示例中已给出）：  

| 列名 | 含义 |
|------|------|
| month | 交易发生的月份（`MONTH(trans_date)`） |
| country | 国家 |
| transaction_count | 该月份该国家的交易总数 |
| total_amount | 该月份该国家的交易金额总和 |
| approved_transaction_count | 该月份该国家已批准（`approved`）的交易数量 |
| approved_total_amount | 该月份该国家已批准交易的金额总和 |

**示例**  

示例 1：  

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| id            | int     |
| country       | varchar |
| state         | enum    |
| amount        | int     |
| trans_date    | date    |
+---------------+---------+
```

`id` 为该表的主键。表中记录了每笔进入的交易信息。`state` 列的取值为 `"approved"` 或 `"declined"`（枚举类型）。  

示例 2：  

输入  
Transactions 表：

```
+------+---------+----------+--------+------------+
| id   | country | state    | amount | trans_date |
+------+---------+----------+--------+------------+
| 121  | US      | approved | 1000   | 2018-12-18 |
| 122  | US      | declined | 2000   | 2018-12-19 |
| 123  | US      | approved | 2000   | 2019-01-01 |
| 124  | DE      | approved | 2000   | 2019-01-07 |
+------+---------+----------+--------+------------+
```

**解释**  
- 2018 年 12 月，US 的交易总数为 2 笔，金额总和为 3000，已批准的交易为 1 笔，金额为 1000。  
- 2019 年 1 月，US 的交易总数为 1 笔，金额为 2000，已批准的交易也为 1 笔，金额为 2000。  
- 2019 年 1 月，DE 的交易总数为 1 笔，金额为 2000，已批准的交易为 1 笔，金额为 2000。  

**约束条件**  
无。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把表里的每一行都读出来，然后手动 **按月份 + 国家** 分组，分别统计：

1. **所有交易** 的笔数与金额总和  
2. **批准（approved）交易** 的笔数与金额总和  

这一步可以用 Python 的 `defaultdict`（类似于生活中的「收件箱」，往同一个邮箱里投信件）来实现：  
- `key = (year_month, country)` 把同一个月份、同一个国家的记录放在同一个「信箱」里。  
- 对每条记录，先更新「全部交易」的计数/金额；如果 `state == 'approved'` 再额外更新「批准交易」的计数/金额。

为什么能得到正确答案？因为我们没有遗漏任何一行，也没有重复计数，所有的统计都是在遍历一次原始数据后完成的。

**时间/空间复杂度**  
- **时间复杂度 O(n)**：`n` 为表的行数。我们只遍历一次，每条记录的处理都是 O(1)（字典的查找/写入是常数时间）。  
- **空间复杂度 O(k)**：`k` 为不同 `(year_month, country)` 组合的数量。最坏情况下每条记录的月份+国家都不相同，空间就是 O(n)，但一般远小于 n。

#### 代码（Python）

```python
import sqlite3
from collections import defaultdict
from datetime import datetime

# ---------- 下面的函数演示“暴力”解法 ----------
def monthly_transactions_bruteforce(db_path: str):
    """
    读取 Transactions 表，手动做分组聚合，返回结果列表。
    每一行是 (year_month, country,
               total_cnt, total_amount,
               approved_cnt, approved_amount)
    """
    # 1️⃣ 连接 SQLite 数据库（这里假设题目数据已经放进 SQLite）
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # 2️⃣ 把全部记录一次性取出来
    cur.execute("SELECT country, state, amount, trans_date FROM Transactions")
    rows = cur.fetchall()          # rows 是一个列表，每条是 (country, state, amount, trans_date)

    # 3️⃣ 用 defaultdict 来做分组聚合
    #   key = (year_month, country)
    agg = defaultdict(lambda: {
        "total_cnt": 0,
        "total_amount": 0,
        "approved_cnt": 0,
        "approved_amount": 0,
    })

    for country, state, amount, trans_date in rows:
        # 把日期转成 "YYYY-MM" 这种月份格式
        year_month = datetime.strptime(trans_date, "%Y-%m-%d").strftime("%Y-%m")
        key = (year_month, country)

        # ① 所有交易的统计
        agg[key]["total_cnt"] += 1
        agg[key]["total_amount"] += amount

        # ② 只有 state 为 approved 时才统计批准交易
        if state == "approved":
            agg[key]["approved_cnt"] += 1
            agg[key]["approved_amount"] += amount

    # 4️⃣ 把 defaultdict 转成普通列表，方便查看
    result = []
    for (year_month, country), stats in agg.items():
        result.append((
            year_month,
            country,
            stats["total_cnt"],
            stats["total_amount"],
            stats["approved_cnt"],
            stats["approved_amount"],
        ))

    conn.close()
    return result


# ---------- 示例运行 ----------
if __name__ == "__main__":
    # 假设本地已经有一个叫 test.db 的 SQLite 数据库，里面有 Transactions 表
    data = monthly_transactions_bruteforce("test.db")
    for line in data:
        print(line)
```

> **关键注释**  
> - `defaultdict` 类似「字典的字典」，每次访问不存在的键时会自动创建一个默认的统计容器。  
> - `datetime.strptime(...).strftime("%Y-%m")` 把完整日期压缩成「年-月」的字符串，便于按月份分组。

#### 复杂度

- **时间复杂度：O(n)** —— 只遍历一次表，`n` 为记录数。  
- **空间复杂度：O(k)** —— `k` 为不同 `(year_month, country)` 组合的数量，最坏 O(n)。  
  *大白话*：如果表里有 10 万条记录，而只有 100 种不同的月份‑国家组合，那么我们只需要保存 100 条统计信息，空间非常省。

---

### 2. 最优解

#### 思路  

在 **SQL** 里我们可以一次性完成所有聚合，而不必把数据拉到 Python 再手动循环。  
关键在于 **条件聚合（conditional aggregation）**：

| 需求 | 对应的 SQL 表达式 |
|------|-------------------|
| 所有交易的笔数 | `COUNT(*)` |
| 所有交易的金额总和 | `SUM(amount)` |
| 批准交易的笔数 | `SUM(CASE WHEN state='approved' THEN 1 ELSE 0 END)` |
| 批准交易的金额总和 | `SUM(CASE WHEN state='approved' THEN amount ELSE 0 END)` |

把这些表达式放在同一个 `SELECT` 里，再 **按月份 + 国家** (`GROUP BY`) 分组，就能一次算完。  
这一步的「瓶颈」在于我们不需要把数据搬出来再遍历，数据库内部已经用了高度优化的哈希聚合（类似于把所有信件先投进同一个邮箱再一次性数完），所以速度更快、代码更简洁。

**核心概念解释**  

- **`GROUP BY`**：把同一月份、同一国家的记录放进同一个「桶」里，后面的聚合函数会对每个桶分别计算。  
- **`CASE WHEN`**：相当于「如果…则…否则…」的判断，在聚合里相当于「只把符合条件的记录计入」——就像我们在手动统计时只在 `state=='approved'` 时才加一。  
- **`strftime('%Y-%m', trans_date)`**：把完整日期切成「年‑月」的字符串，作为分组的依据。

#### 代码（Python）

下面的函数展示了 **仅用一条 SQL** 完成需求。我们把 SQL 写成字符串，交给 SQLite（或其他关系型数据库）执行，最后把结果取出来。

```python
import sqlite3

def monthly_transactions_optimal(db_path: str):
    """
    使用单条 SQL 完成所有统计，返回同样的结果格式。
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    sql = """
    SELECT
        strftime('%Y-%m', trans_date) AS year_month,   -- 把日期压缩成 "2020-07" 这种月份标识
        country,
        COUNT(*)                                            AS total_cnt,          -- 所有交易笔数
        SUM(amount)                                         AS total_amount,       -- 所有交易金额
        SUM(CASE WHEN state = 'approved' THEN 1 ELSE 0 END) AS approved_cnt,       -- 批准交易笔数
        SUM(CASE WHEN state = 'approved' THEN amount ELSE 0 END) AS approved_amount -- 批准交易金额
    FROM Transactions
    GROUP BY year_month, country
    ORDER BY year_month, country;   -- 可选：让结果按时间、国家有序，方便阅读
    """
    cur.execute(sql)
    rows = cur.fetchall()   # 每行对应 (year_month, country, total_cnt, total_amount, approved_cnt, approved_amount)

    conn.close()
    return rows


# ---------- 示例运行 ----------
if __name__ == "__main__":
    data = monthly_transactions_optimal("test.db")
    for line in data:
        print(line)
```

> **关键注释**  
> - `strftime('%Y-%m', trans_date)` 在 SQLite 中把日期转成「年‑月」字符串，等价于 MySQL 的 `DATE_FORMAT(trans_date, '%Y-%m')`。  
> - `SUM(CASE WHEN … THEN 1 ELSE 0 END)` 把「符合条件」的行计为 1，不符合的计为 0，最终求和得到计数。  
> - 整条查询只需要一次 **全表扫描 + 哈希聚合**，在大多数数据库里是最优的执行计划。

#### 复杂度

- **时间复杂度：O(n)** —— 数据仍然要遍历一次，只是交给数据库的内部实现来做，实际常数更小。  
- **空间复杂度：O(k)** —— 只需要为每个 `(year_month, country)` 组合保存聚合结果，同样是 `k` 条记录。  

与暴力解相比，**时间常数更低**（因为不需要在 Python 层面进行大量的字典操作），代码也更简洁、易维护。

---

## 心得

- **核心技巧**：**条件聚合（Conditional Aggregation）** + **按月份分组**。  
- **适用场景**：  
  1. 同时统计“全部”和“满足某条件”的指标（如订单总额 vs. 已付款订单总额）。  
  2. 需要按时间窗口（年、月、日）进行多维度汇总。  
  3. 统计不同状态下的计数/金额（如用户活跃 vs. 注销）。  
- **一句话总结**：把“只算满足条件的那部分”写进 `CASE WHEN`，一次 `GROUP BY` 就能把所有想要的统计值一次性算出来。

---

## 反思

- **第一反应**：直接把所有记录拉出来，用 Python 循环手动分组统计。  
- **最容易踩的坑**：  
  - 日期的分组必须先把 `date` 转成 “年‑月” 的格式，否则同一年不同月份会被错误合并。  
  - `state` 的枚举值要和 SQL 中的字符串完全匹配（大小写、空格）。  
  - 若使用 MySQL、PostgreSQL 等不同数据库，日期函数的写法会略有区别（`DATE_FORMAT`、`TO_CHAR` 等）。  
- **下次类似题的第一步**：先在脑子里写出 **“所有指标 = 聚合函数 + 条件表达式”**，确认可以在一条 `SELECT` 里一次性完成，再去考虑具体的 SQL 语法。