# #1321. **餐厅增长** / Restaurant Growth

> 难度：中等 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/restaurant-growth/)

---

## 题目（英文原版）

**Description**

Table: Customer
You are the restaurant owner and you want to analyze a possible expansion (there will be at least one customer every day).
Compute the moving average of how much the customer paid in a seven days window (i.e., current day + 6 days before). average_amount should be rounded to two decimal places.
Return the result table ordered by visited_on in ascending order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| customer_id   | int     |
| name          | varchar |
| visited_on    | date    |
| amount        | int     |
+---------------+---------+
In SQL,(customer_id, visited_on) is the primary key for this table.
This table contains data about customer transactions in a restaurant.
visited_on is the date on which the customer with ID (customer_id) has visited the restaurant.
amount is the total paid by a customer.
```

**Example 2:**

```
Input: 
Customer table:
+-------------+--------------+--------------+-------------+
| customer_id | name         | visited_on   | amount      |
+-------------+--------------+--------------+-------------+
| 1           | Jhon         | 2019-01-01   | 100         |
| 2           | Daniel       | 2019-01-02   | 110         |
| 3           | Jade         | 2019-01-03   | 120         |
| 4           | Khaled       | 2019-01-04   | 130         |
| 5           | Winston      | 2019-01-05   | 110         | 
| 6           | Elvis        | 2019-01-06   | 140         | 
| 7           | Anna         | 2019-01-07   | 150         |
| 8           | Maria        | 2019-01-08   | 80          |
| 9           | Jaze         | 2019-01-09   | 110         | 
| 1           | Jhon         | 2019-01-10   | 130         | 
| 3           | Jade         | 2019-01-10   | 150         | 
+-------------+--------------+--------------+-------------+
Output: 
+--------------+--------------+----------------+
| visited_on   | amount       | average_amount |
+--------------+--------------+----------------+
| 2019-01-07   | 860          | 122.86         |
| 2019-01-08   | 840          | 120            |
| 2019-01-09   | 840          | 120            |
| 2019-01-10   | 1000         | 142.86         |
+--------------+--------------+----------------+
Explanation: 
1st moving average from 2019-01-01 to 2019-01-07 has an average_amount of (100 + 110 + 120 + 130 + 110 + 140 + 150)/7 = 122.86
2nd moving average from 2019-01-02 to 2019-01-08 has an average_amount of (110 + 120 + 130 + 110 + 140 + 150 + 80)/7 = 120
3rd moving average from 2019-01-03 to 2019-01-09 has an average_amount of (120 + 130 + 110 + 140 + 150 + 80 + 110)/7 = 120
4th moving average from 2019-01-04 to 2019-01-10 has an average_amount of (130 + 110 + 140 + 150 + 80 + 110 + 130 + 150)/7 = 142.86
```

---

## 题目（中文翻译）

表结构：`Customer`

你是餐厅的老板，想要分析可能的扩张情况（每天至少有一位顾客）。  
请计算每一天的 **移动平均**（moving average），即该天以及其前 6 天（共 7 天）顾客支付金额 `amount` 的平均值。`average_amount` 需要四舍五入保留两位小数。  
返回的结果表按 `visited_on` 升序排列，格式参见示例。

在 SQL 中，`(customer_id, visited_on)` 为该表的 **主键**（primary key）。  
该表记录了顾客在餐厅的交易信息，其中 `visited_on` 为顾客消费的日期。

---

### 示例 1

```sql
Customer 表结构
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| customer_id   | int     |
| name          | varchar |
| visited_on    | date    |
| amount        | int     |
+---------------+---------+
```

在 SQL 中，`(customer_id, visited_on)` 为主键（primary key）。  
该表包含餐厅的顾客交易数据。

**解释**  
对每个 `visited_on`，计算该日期以及其前 6 天（共 7 天）的 `amount` 总和，然后除以 7，得到 `average_amount`（保留两位小数）。例如，2019‑01‑07 的 7 天窗口是 2019‑01‑01 到 2019‑01‑07，所有 `amount` 求和后除以 7，即得到该日的平均消费额。

---

### 示例 2

**输入**

```text
Customer 表：
+-------------+--------------+--------------+--------+
| customer_id | name         | visited_on   | amount |
+-------------+--------------+--------------+--------+
| 1           | Jhon         | 2019-01-01   | 100    |
| 2           | Daniel       | 2019-01-02   | 110    |
| 3           | Jade         | 2019-01-03   | 120    |
| 4           | ...          | ...          | ...    |
+-------------+--------------+--------------+--------+
```

**输出**

（略）

**解释**  
同样对每一天计算其所在的 7 天窗口的平均消费额，并将结果按照 `visited_on` 升序返回。所有 `average_amount` 均四舍五入保留两位小数。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**把每一天当作“窗口的右端”，向左数 6 天（共 7 天）把这几天的消费额加起来再除以 7**。  

- **数据结构**：  
  - 用 **列表**（list）存放所有交易记录，每条记录是 `(visited_on, amount)`。  
  - `visited_on` 用 `datetime.date` 表示，方便比较大小。  
  - 为了快速找出“某一天之前的 6 天”，我们可以把所有记录先 **按日期升序排好**，相当于把时间轴排成一条直线。  

- **为什么正确**：  
  对于每一天 `d`，我们只需要找出日期在 `[d-6, d]` 区间的所有消费额并求平均。暴力做法把这一步逐条遍历检查：只要记录的日期在区间内，就累计它的 `amount`。因为题目保证每一天至少有一条记录，窗口里一定有数据，除以 7 就得到当天的 **七天移动平均**。  

- **时间/空间复杂度**：  
  - 假设总共有 `n` 条记录。对每一条记录（共 `n` 条）我们都要遍历一次完整的列表去找它前面的 6 天，这相当于 **`n × n` 次比较**，所以时间复杂度是 **O(n²)**。  
    - 大白话：如果有 100 条记录，程序会做大约 10,000 次“检查”。  
  - 只用了原始列表和几个临时变量，额外空间是 **O(1)**（常数级），不随 `n` 增长。

#### 代码（Python）  

```python
import datetime
from typing import List, Tuple

def moving_average_bruteforce(records: List[Tuple[int, str, str, int]]) -> List[Tuple[str, float]]:
    """
    暴力实现七天移动平均
    records: 每条记录为 (customer_id, name, visited_on_str, amount)
    返回: 按日期升序的 [(visited_on_str, average_amount), ...]
    """
    # 1. 把日期字符串转成 datetime.date，方便比较
    parsed = [(datetime.datetime.strptime(v, "%Y-%m-%d").date(), amt) for _, _, v, amt in records]

    # 2. 按日期升序排序（题目已保证唯一主键，但这里仍然排序）
    parsed.sort(key=lambda x: x[0])

    result = []
    for i, (cur_date, _) in enumerate(parsed):
        # 窗口左边界：当前日期往前数 6 天
        left = cur_date - datetime.timedelta(days=6)

        # 3. 暴力遍历所有记录，累计在窗口内的 amount
        total = 0
        cnt = 0               # 实际窗口内的天数（这里一定是 7，因为保证每天都有记录）
        for d, amt in parsed:
            if left <= d <= cur_date:   # 日期在窗口范围内
                total += amt
                cnt += 1

        avg = round(total / cnt, 2)   # 保留两位小数
        result.append((cur_date.strftime("%Y-%m-%d"), avg))

    return result
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 解释：外层遍历 `n` 次，内层每次又要检查 `n` 条记录，等价于“平方级”增长。  
- **空间复杂度**：`O(1)`（不计输入输出）  
  - 只用了几个常数级的临时变量和一个排序后的列表（排序本身是原地的），不随 `n` 增大而额外占用空间。

---

### 2. 最优解  

#### 思路  
暴力解的瓶颈在于 **每一天都要重新遍历所有记录**，导致重复工作。实际上，**相邻两天的窗口只有一天的差别**：  

- 当窗口从 `d-1` 移动到 `d` 时，左边界会向前多排除掉 `d-7` 那一天的记录，右边界会加入 `d` 那一天的记录。  

这正好可以用 **滑动窗口**（Sliding Window）或 **前缀和**（Prefix Sum）来优化：

1. **先把所有记录按日期升序排列**。  
2. 用两个指针 `left`、`right` 表示当前窗口的左右边界（左闭右闭），并维护 **窗口内金额的累计和 `window_sum`**。  
3. 随着 `right` 向右移动到新的一天：  
   - 把这一天的 `amount` 加入 `window_sum`。  
   - 如果窗口长度已经超过 7 天（即 `right - left + 1 > 7`），就把最左边那一天的 `amount` 从 `window_sum` 中减掉，并把 `left` 向右移动一格。  
4. 此时窗口恰好是最近的 7 天（或不足 7 天的情况，题目保证每天都有记录，所以一定是 7 天），直接用 `window_sum / 7` 即可得到平均值。  

**核心数据结构**：  
- **双指针**（two‑pointer）就像两只手在时间轴上滑动，一只负责“收进来”，另一只负责“丢出去”。  
- **整数累加** `window_sum` 相当于一个装钱的罐子，往里倒钱（新一天），也会把旧钱倒出来（超出 7 天的那一天），保证罐子里永远装的正好是最近 7 天的金额。

**为什么更快**：  
- 每条记录只会被 **加入一次**、**移除一次**，所以整个过程只遍历一次列表，时间复杂度降到 **O(n)**。  
- 只用了几个指针和一个整数，空间仍然是 **O(1)**。

#### 代码（Python）  

```python
import datetime
from typing import List, Tuple

def moving_average_optimal(records: List[Tuple[int, str, str, int]]) -> List[Tuple[str, float]]:
    """
    最优实现：滑动窗口 O(n) 时间、O(1) 额外空间
    """
    # 1. 解析日期并排序
    parsed = [(datetime.datetime.strptime(v, "%Y-%m-%d").date(), amt) for _, _, v, amt in records]
    parsed.sort(key=lambda x: x[0])

    n = len(parsed)
    left = 0               # 窗口左端指针
    window_sum = 0         # 窗口内金额总和
    result = []

    for right in range(n):
        cur_date, cur_amt = parsed[right]
        window_sum += cur_amt               # 把新一天加入窗口

        # 当窗口长度 > 7 时，左端需要收缩
        while right - left + 1 > 7:
            _, left_amt = parsed[left]
            window_sum -= left_amt           # 把最左边的金额移出
            left += 1                        # 左指针右移

        # 此时窗口长度恰好是 7（题目保证每天都有记录，前几天也会逐步满 7 天）
        avg = round(window_sum / (right - left + 1), 2)
        result.append((cur_date.strftime("%Y-%m-%d"), avg))

    return result
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 解释：`right` 指针遍历一次列表，`left` 指针最多也只会移动 `n` 次（每次移动都对应一次 “移除”），所以总操作次数和记录数成线性关系。相比暴力的 `O(n²)`，这就像把“十万次检查”压缩成“十万次简单加减”。  
- **空间复杂度**：`O(1)`（不计输入输出）  
  - 只用了常数个变量 (`left`, `right`, `window_sum`) 来维护窗口，额外内存不随 `n` 增长。

---

## 心得  

- **核心技巧**：**滑动窗口**（Two‑Pointer）配合 **累计求和**。  
- **适用题型**（类似思路）  
  1. 「求数组中长度为 `k` 的子数组最大/最小和」  
  2. 「统计字符串中满足某种条件的最长子串」  
  3. 「移动平均、移动中位数等滚动统计」  
- **一句话总结解题钥匙**：**让窗口只在两端“进出”，保持窗口大小不变，就能把重复遍历的成本降到 O(1) 每步**。

---

## 反思  

- **第一反应**：看到“七天窗口”，立刻想到 “把每一天往前数 6 天再算平均”，于是写了双层循环的暴力实现。  
- **最容易踩的坑**  
  - **日期跨度不连续**：如果某天没有记录，窗口长度会不足 7 天，需要自行判断除数。题目已保证每天都有客户，但在真实数据里要先填补缺失日期。  
  - **浮点数精度**：直接除法得到的结果可能有很多小数位，必须在最后 `round(..., 2)`，否则输出会多出不必要的尾数。  
  - **时间格式**：输入是字符串，需要先转成 `datetime.date` 再比较，否则字符串比较会出现错误（例如 `"2019-01-10"` 小于 `"2019-01-2"`）。  
- **下次遇到同类题**：**先确认窗口大小是否固定**，若是，立刻考虑 **滑动窗口**；若窗口大小可变，则思考 **前缀和** 或 **单调队列** 等技巧。这样可以第一时间把时间复杂度从平方级降到线性级。