# #1393. **资本收益/损失** / Capital Gain/Loss

> 难度：中等 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/capital-gainloss/)

---

## 题目（英文原版）

**Description**

Table: Stocks
Write a solution to report the Capital gain/loss for each stock.
The Capital gain/loss of a stock is the total gain or loss after buying and selling the stock one or many times.
Return the result table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| stock_name    | varchar |
| operation     | enum    |
| operation_day | int     |
| price         | int     |
+---------------+---------+
(stock_name, operation_day) is the primary key (combination of columns with unique values) for this table.
The operation column is an ENUM (category) of type ('Sell', 'Buy')
Each row of this table indicates that the stock which has stock_name had an operation on the day operation_day with the price.
It is guaranteed that each 'Sell' operation for a stock has a corresponding 'Buy' operation in a previous day. It is also guaranteed that each 'Buy' operation for a stock has a corresponding 'Sell' operation in an upcoming day.
```

**Example 2:**

```
Input: 
Stocks table:
+---------------+-----------+---------------+--------+
| stock_name    | operation | operation_day | price  |
+---------------+-----------+---------------+--------+
| Leetcode      | Buy       | 1             | 1000   |
| Corona Masks  | Buy       | 2             | 10     |
| Leetcode      | Sell      | 5             | 9000   |
| Handbags      | Buy       | 17            | 30000  |
| Corona Masks  | Sell      | 3             | 1010   |
| Corona Masks  | Buy       | 4             | 1000   |
| Corona Masks  | Sell      | 5             | 500    |
| Corona Masks  | Buy       | 6             | 1000   |
| Handbags      | Sell      | 29            | 7000   |
| Corona Masks  | Sell      | 10            | 10000  |
+---------------+-----------+---------------+--------+
Output: 
+---------------+-------------------+
| stock_name    | capital_gain_loss |
+---------------+-------------------+
| Corona Masks  | 9500              |
| Leetcode      | 8000              |
| Handbags      | -23000            |
+---------------+-------------------+
Explanation: 
Leetcode stock was bought at day 1 for 1000$ and was sold at day 5 for 9000$. Capital gain = 9000 - 1000 = 8000$.
Handbags stock was bought at day 17 for 30000$ and was sold at day 29 for 7000$. Capital loss = 7000 - 30000 = -23000$.
Corona Masks stock was bought at day 1 for 10$ and was sold at day 3 for 1010$. It was bought again at day 4 for 1000$ and was sold at day 5 for 500$. At last, it was bought at day 6 for 1000$ and was sold at day 10 for 10000$. Capital gain/loss is the sum of capital gains/losses for each ('Buy' --> 'Sell') operation = (1010 - 10) + (500 - 1000) + (10000 - 1000) = 1000 - 500 + 9000 = 9500$.
```

---

## 题目（中文翻译）

编写一个 SQL 查询，统计每只股票的资本收益（gain）或损失（loss）。  
一只股票的资本收益/损失是指在该股票被 **买入（Buy）** 并 **卖出（Sell）** 若干次后，所有卖出价格的总和减去所有买入价格的总和的结果。  
返回的结果表可以按任意顺序排列，格式参考下例。

**示例 1**

```sql
Stocks 表结构
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| stock_name    | varchar |
| operation     | enum    |
| operation_day | int     |
| price         | int     |
+---------------+---------+
```

- `(stock_name, operation_day)` 为主键（primary key），即这两列的组合在表中唯一。  
- `operation` 列是枚举（enum）类型，只包含 `'Sell'` 与 `'Buy'` 两个取值。

查询结果示例（可能的输出之一）：

```sql
+------------+-------------------+
| stock_name | capital_gain_loss |
+------------+-------------------+
| Leetcode  | 8000              |
| Corona Masks | -5              |
| Handbags  | 0                 |
+------------+-------------------+
```

**示例 2**

**输入**  
`Stocks` 表：

| stock_name   | operation | operation_day | price |
|--------------|-----------|---------------|-------|
| Leetcode     | Buy       | 1             | 1000 |
| Corona Masks | Buy       | 2             | 10   |
| Leetcode     | Sell      | 5             | 9000 |
| Handbags     | Buy       | 17            | 30   |
| … (数据被截断) |           |               |       |

**输出**  

| stock_name   | capital_gain_loss |
|--------------|-------------------|
| Leetcode     | 8000              |
| Corona Masks | -5                |
| Handbags     | 0                 |
| … (数据被截断) | …                 |

**说明**  
- 对每只股票，先把所有 `Buy` 记录的 `price` 求和，再把所有 `Sell` 记录的 `price` 求和，二者相减即为该股票的资本收益/损失。  
- 如果某只股票只出现 `Buy` 而没有对应的 `Sell`，则其收益为负值（即总买入成本的相反数）。  
- 同理，如果只出现 `Sell` 而没有 `Buy`，则其收益为正值（即总卖出收入）。

**约束条件**

- 表中数据量在合理范围内，能够在标准 SQL 引擎的执行时间限制内完成计算。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

我们手里有一张 `Stocks` 表，每一行记录一次 **买入** 或 **卖出** 操作，  
字段如下  

| 列名            | 含义                         |
|----------------|------------------------------|
| `stock_name`   | 股票名称（相当于字典的“键”） |
| `operation`    | `'Buy'` 或 `'Sell'`           |
| `operation_day`| 操作的时间顺序（越小越早）   |
| `price`        | 本次交易的价格                |

**目标**：对每只股票，算出所有买卖配对后的 **资本盈亏**（卖价 - 买价），并把每只股票的累计盈亏返回。  

最直接的想法是：

1. 把所有记录取出来，**按照 `stock_name` 分组**（就像把所有同一本字典的词条放在一起）。
2. 对每个分组，再**按照 `operation_day` 排序**，保证我们按时间顺序处理。
3. 逐条遍历该股票的操作序列：  
   - 遇到 `'Buy'`，把买入的价格记下来。  
   - 遇到 `'Sell'`，在已经记下的买入价格里**找一笔**对应的买入，然后用 `sell_price - buy_price` 累加到盈亏总和。  

最“笨”的地方在第 3 步的“找一笔对应的买入”。如果直接遍历已记录的买入列表去匹配，就会出现 **嵌套循环**——每一次卖出都要在之前所有的买入中搜索一次。  

> **为什么这种方法一定能得到正确答案？**  
> 因为题目保证每一次卖出都有对应的买入（买卖次数相等），只要我们把买入记录保存下来，随后出现的卖出必然可以在这些记录里找到匹配的买入。顺序匹配（先买先卖）符合常规的“先买后卖”逻辑，也满足题目要求的“买卖一次或多次”。  

**时间/空间复杂度**（大白话版）  

- **时间复杂度**：`O(n²)`  
  - `n` 是表中的记录总数。  
  - 对每一条卖出记录，我们都要遍历之前的所有买入记录（最坏情况下是 `n/2` 次），于是整体是 **平方级**，就像在找朋友时每次都要把所有朋友的名单翻一遍。  
- **空间复杂度**：`O(n)`  
  - 需要把每只股票的所有买入价格保存下来，最坏情况下要存 `n` 条记录。  

#### 代码（Python）  

```python
from collections import defaultdict
from typing import List, Dict, Tuple

# ------------------- 暴力实现 -------------------
def capital_gain_bruteforce(stocks: List[Dict]) -> List[Tuple[str, int]]:
    """
    stocks: 每条记录是一个 dict，键名和题目列名相同
    返回值: [(stock_name, total_gain), ...]，顺序不限
    """
    # 1. 按股票名称分组
    groups = defaultdict(list)          # stock_name -> list of records
    for rec in stocks:
        groups[rec["stock_name"]].append(rec)

    result = []

    # 2. 对每只股票分别处理
    for name, records in groups.items():
        # 按天数升序，保证时间顺序
        records.sort(key=lambda r: r["operation_day"])

        buys = []          # 已买入但未匹配的价格列表
        total_gain = 0

        # 3. 逐条遍历
        for r in records:
            if r["operation"] == "Buy":
                # 记录买入价格
                buys.append(r["price"])
            else:  # Sell
                # 暴力搜索对应的买入（这里直接取第一个未匹配的买入）
                # 实际上只要有买入就可以匹配，题目不要求特定的配对方式
                if buys:               # 防止空列表导致错误（理论上不会出现）
                    buy_price = buys.pop(0)   # 从列表头取出，模拟 FIFO
                    total_gain += r["price"] - buy_price
        result.append((name, total_gain))
    return result
```

#### 复杂度  

- **时间复杂度**：`O(n²)` —— 每一次卖出都要在 `buys` 列表里做线性搜索（`pop(0)` 本身也是 O(k)）。
- **空间复杂度**：`O(n)` —— 需要保存所有未匹配的买入价格。

---

### 2. 最优解  

#### 思路  

从暴力解我们可以看到 **瓶颈** 在于“找对应买入”这一步的线性搜索。  
如果我们能把买入价格的存取改成 **常数时间**，整个算法就会快很多。  

**关键观察**：  
- 买入和卖出是严格按照时间顺序出现的（`operation_day` 保证唯一且递增）。  
- 对于同一只股票，**最早买入的那笔** 必须先被卖出（先买先卖），这正好对应 **队列（FIFO）** 的特性。  

于是我们可以：

1. 仍然先把记录 **按股票分组并按天数排序**（这一步不可省，保证时间顺序）。
2. 对每只股票维护一个 **队列**（`collections.deque`），专门用来存放**尚未卖出的买入价格**。  
   - `Buy` → `queue.append(price)`（把买入价格放到队尾）  
   - `Sell` → `buy_price = queue.popleft()`（从队首取出最早的买入）  
   - 立即累加 `sell_price - buy_price` 到盈亏总和。  

因为 `append` 与 `popleft` 都是 **O(1)** 的操作，**不再需要遍历** 已有的买入列表，整体只遍历一次表格即可。

**时间/空间复杂度**（通俗解释）  

- **时间复杂度**：`O(n)`  
  - 每条记录只被处理一次，像一次“一刀切”检查，没有嵌套循环，速度随记录数线性增长。  
- **空间复杂度**：`O(m)`（`m` 为同一只股票的未匹配买入数，最坏情况仍然是 `O(n)`）  
  - 只需要保存当前尚未匹配的买入价格，数量最多等于表格的记录数。  

#### 代码（Python）  

```python
from collections import defaultdict, deque
from typing import List, Dict, Tuple

# ------------------- 最优实现 -------------------
def capital_gain_optimal(stocks: List[Dict]) -> List[Tuple[str, int]]:
    """
    与暴力版思路相同，只是把买入价格保存到 deque（双端队列），
    通过 O(1) 的 popleft 完成配对，整体线性时间。
    """
    # 1. 按股票名称分组
    groups = defaultdict(list)
    for rec in stocks:
        groups[rec["stock_name"]].append(rec)

    result = []

    # 2. 对每只股票分别处理
    for name, records in groups.items():
        # 按时间升序
        records.sort(key=lambda r: r["operation_day"])

        buy_queue = deque()   # FIFO 队列，存未匹配的买入价格
        total_gain = 0

        # 3. 单次遍历
        for r in records:
            if r["operation"] == "Buy":
                buy_queue.append(r["price"])          # 入队
            else:  # Sell
                # 队列不为空（题目保证买卖配对），取出最早的买入
                buy_price = buy_queue.popleft()       # 出队，O(1)
                total_gain += r["price"] - buy_price   # 累加盈亏

        result.append((name, total_gain))
    return result
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 每条记录只做一次 `append` 或 `popleft`，不再出现嵌套循环。  
- **空间复杂度**：`O(n)`（最坏情况下所有买入都未匹配），实际使用的空间随未成交买入的数量线性增长。

---

## 心得  

- **核心技巧**：**利用队列（FIFO）实现买卖配对**，把“寻找匹配买入”的线性搜索降为常数时间。  
- **适用场景**：  
  1. **交易类**问题，需要按时间顺序配对进出（如股票、商品、票务等）。  
  2. **括号匹配**、**水位线**等需要 **先进先出** 或 **先进后出** 的场景（后者使用栈）。  
  3. **日志处理**：按时间顺序把“开始”与“结束”事件配对。  
- **一句话总结**：  
  *“把时间顺序的配对任务抽象为队列，所有操作都能在 O(1) 内完成。”*

---

## 反思  

- **第一反应**：直接把所有买入价格存列表，卖出时遍历寻找匹配——这就是暴力思路。  
- **最容易踩的坑**：  
  - **忘记按 `operation_day` 排序**，导致配对顺序错误。  
  - **买入卖出不成对**（实际数据可能出现异常），此时 `popleft` 会报错，需要自行判断或抛异常。  
  - **使用 `list.pop(0)`** 会导致每次 O(k) 的搬移，实际效果和队列差不多慢。  
- **下次类似题**：第一步先 **思考“配对顺序是什么”**（FIFO、LIFO、或无序），再选合适的数据结构（队列、栈、哈希表）来实现 O(1) 的配对。这样就能快速从暴力到最优。