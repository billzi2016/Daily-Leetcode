# #1251. **Average Selling Price** / Average Selling Price

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/average-selling-price/)

---

## 题目（英文原版）

**Description**

Table: Prices
Table: UnitsSold
Write a solution to find the average selling price for each product. average_price should be rounded to 2 decimal places. If a product does not have any sold units, its average selling price is assumed to be 0.
Return the result table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| product_id    | int     |
| start_date    | date    |
| end_date      | date    |
| price         | int     |
+---------------+---------+
(product_id, start_date, end_date) is the primary key (combination of columns with unique values) for this table.
Each row of this table indicates the price of the product_id in the period from start_date to end_date.
For each product_id there will be no two overlapping periods. That means there will be no two intersecting periods for the same product_id.
```

**Example 2:**

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| product_id    | int     |
| purchase_date | date    |
| units         | int     |
+---------------+---------+
This table may contain duplicate rows.
Each row of this table indicates the date, units, and product_id of each product sold.
```

**Example 3:**

```
Input: 
Prices table:
+------------+------------+------------+--------+
| product_id | start_date | end_date   | price  |
+------------+------------+------------+--------+
| 1          | 2019-02-17 | 2019-02-28 | 5      |
| 1          | 2019-03-01 | 2019-03-22 | 20     |
| 2          | 2019-02-01 | 2019-02-20 | 15     |
| 2          | 2019-02-21 | 2019-03-31 | 30     |
+------------+------------+------------+--------+
UnitsSold table:
+------------+---------------+-------+
| product_id | purchase_date | units |
+------------+---------------+-------+
| 1          | 2019-02-25    | 100   |
| 1          | 2019-03-01    | 15    |
| 2          | 2019-02-10    | 200   |
| 2          | 2019-03-22    | 30    |
+------------+---------------+-------+
Output: 
+------------+---------------+
| product_id | average_price |
+------------+---------------+
| 1          | 6.96          |
| 2          | 16.96         |
+------------+---------------+
Explanation: 
Average selling price = Total Price of Product / Number of products sold.
Average selling price for product 1 = ((100 * 5) + (15 * 20)) / 115 = 6.96
Average selling price for product 2 = ((200 * 15) + (30 * 30)) / 230 = 16.96
```

---

## 题目（中文翻译）

编写查询，求出每个产品的平均售出价格（average_price），并保留两位小数。若某个产品没有任何已售出单位，则其平均售出价格视为 0。返回的结果表顺序不限，结果格式参照示例。

**表结构**

`Prices` 表  

| 列名          | 类型   |
|---------------|--------|
| product_id    | int    |
| start_date    | date   |
| end_date      | date   |
| price         | int    |

`(product_id, start_date, end_date)` 为主键（primary key），即唯一组合键。每一行记录了对应 `product_id` 在 `start_date` 到 `end_date` 期间的价格。

`UnitsSold` 表  

| 列名          | 类型   |
|---------------|--------|
| product_id    | int    |
| purchase_date | date   |
| units         | int    |

该表可能出现重复行。每一行记录了某一天某产品的售出单位数。

**返回结果示例**

```
product_id | average_price
-----------|---------------
1          | 12.34
2          | 0.00
...
```

（示例的输入/输出表格保持原样，仅对说明文字进行翻译。）

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题的核心是把 **每一次销售**（`UnitsSold` 表中的一行）对应到它发生时的 **商品单价**（`Prices` 表中满足日期区间的那一行），再算出「总收入 / 总销量」得到平均售价。

> **类比**：想象你在超市买东西，每件商品都有「价签」标明价格，价签会在一定时间段有效。你手里有一张购物小票，记录了买了多少件、哪天买的。要算出这段时间的平均花费，你得把每件商品的买入日期对应到当时的价签，然后把所有「单价 × 数量」加起来，再除以总数量。

最直接的做法就是：

1. 对 `UnitsSold` 表的每一行，遍历 `Prices` 表的所有行，找出满足  
   `product_id` 相同 且 `start_date ≤ purchase_date ≤ end_date` 的记录。  
   这一步相当于「把每件商品的买入日期在价签表里逐个找」。
2. 用找到的 `price` 乘以 `units`，累加到该商品的 `total_revenue` 中；同样累加 `units` 到 `total_units`。
3. 最后对每个 `product_id`，若 `total_units > 0`，平均价 = `total_revenue / total_units`，否则为 `0`（题目要求没有销量的商品平均价为 0）。
4. 使用 `round(..., 2)` 把结果保留两位小数。

> **为什么正确**  
> 每一次销售只能对应唯一一个有效的价签（因为价签的时间区间在同一商品下不重叠），所以遍历找到了的 `price` 正是这笔销售的实际成交价。把所有成交价乘以对应销量相加得到的就是 **总收入**，除以 **总销量** 就是 **平均售价**。

#### 代码（Python）

```python
from typing import List, Tuple
from collections import defaultdict
from datetime import datetime

# ------------------------------------------------------------------
# 辅助函数：把字符串日期转成 datetime，方便比较
def to_date(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%d")
# ------------------------------------------------------------------

def average_selling_price_bruteforce(
    prices: List[Tuple[int, str, str, int]],
    units_sold: List[Tuple[int, str, int]]
) -> List[Tuple[int, float]]:
    """
    暴力实现：对每一笔销售遍历所有价签，时间复杂度 O(N * M)
    参数
    ----
    prices: [(product_id, start_date, end_date, price), ...]
    units_sold: [(product_id, purchase_date, units), ...]
    返回值
    ----
    [(product_id, average_price), ...]，average_price 已经 round 到 2 位
    """

    # 统计每个商品的总收入和总销量
    revenue = defaultdict(int)   # product_id -> 总收入（price * units 的累计）
    sold_cnt = defaultdict(int)  # product_id -> 总销量

    # 暴力匹配
    for p_id, purchase_date, units in units_sold:
        purchase_dt = to_date(purchase_date)

        # 在价格表里找对应的价签
        matched_price = 0
        for pid, start, end, price in prices:
            if pid != p_id:
                continue
            if to_date(start) <= purchase_dt <= to_date(end):
                matched_price = price
                break   # 题目保证同一商品同一天只有唯一价签

        # 累加
        revenue[p_id] += matched_price * units
        sold_cnt[p_id] += units

    # 计算平均价，所有出现过的 product_id 都要返回
    all_products = {pid for pid, *_ in prices} | {pid for pid, *_ in units_sold}
    result = []
    for pid in all_products:
        if sold_cnt[pid] == 0:
            avg = 0.0
        else:
            avg = round(revenue[pid] / sold_cnt[pid] + 1e-9, 2)   # +1e-9 防止 0.005 四舍五入误差
        result.append((pid, avg))

    return result
```

#### 复杂度

- **时间复杂度**：`O(N * M)`  
  - `N` 为 `UnitsSold` 表的行数，`M` 为 `Prices` 表的行数。  
  - 可以把它想成「每卖出一件商品，要去全表里翻一遍价签」，如果两张表都有几千行，计算量会非常大。

- **空间复杂度**：`O(K)`  
  - `K` 为不同商品的数量（存放 `revenue`、`sold_cnt`、`result` 用到的空间）。  
  - 这相当于「只需要记住每个商品的累计数据」。


---  

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **对每一笔销售都要遍历所有价签**。其实价签本身已经按时间顺序组织好了（虽然原表没有保证顺序，但我们可以自行排序），而且同一商品的价签区间互不重叠。利用这一点，我们可以把搜索过程从线性扫描改成 **二分查找**，把时间复杂度降到 `O(N log M)`。

优化步骤：

1. **按商品分组并排序**  
   - 把 `Prices` 按 `product_id` 分组，每组内部再按 `start_date` 升序排列。  
   - 对每个商品，构造两个并行的列表：`starts = [start_date_i]`、`prices = [price_i]`。因为价签区间不重叠，只要找到了满足 `start_date ≤ purchase_date` 的最后一个 `start_date`，它对应的 `price` 就是正确的。

2. **二分查找对应价签**  
   - 对于一笔销售，先定位到对应商品的 `starts` 列表。  
   - 使用 `bisect_right(starts, purchase_date) - 1` 得到 **最近的、且不晚于购买日期的价签索引**。  
   - 再检查 `purchase_date` 是否 ≤ 对应的 `end_date`（如果不满足，说明该日期没有价签，题目假设不会出现这种情况），得到 `price`。

3. **累计收入和销量**  
   - 与暴力解相同，只是找 `price` 的过程更快。

4. **返回结果**  
   - 同样对所有出现过的 `product_id` 计算 `average_price`，若销量为 0 则返回 `0.0`。

> **为什么更快**  
> 二分查找的时间是 `log M`（对数级），相当于「把价签表折半查找」，每次只需要检查几次，而不是全部遍历。对大量数据（比如上万条记录）时，性能提升非常明显。

#### 代码（Python）

```python
from typing import List, Tuple
from collections import defaultdict
from datetime import datetime
import bisect

def to_date(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%d")

def average_selling_price_optimal(
    prices: List[Tuple[int, str, str, int]],
    units_sold: List[Tuple[int, str, int]]
) -> List[Tuple[int, float]]:
    """
    最优实现：利用二分查找，将时间复杂度降到 O(N log M)
    """
    # 1️⃣ 按商品分组并排序
    price_map = defaultdict(list)          # product_id -> [(start_dt, end_dt, price), ...] 已排序
    for pid, start, end, price in prices:
        price_map[pid].append((to_date(start), to_date(end), price))

    # 对每个商品的价签列表按 start_date 排序（保证二分的前提）
    start_dict = {}   # product_id -> [start_dt, ...]（仅保存 start，便于二分）
    interval_dict = {}# product_id -> [(start_dt, end_dt, price), ...]（与 start 同序）
    for pid, lst in price_map.items():
        lst.sort(key=lambda x: x[0])               # 按 start 升序
        starts = [s for s, _, _ in lst]
        start_dict[pid] = starts
        interval_dict[pid] = lst

    # 2️⃣ 累计收入和销量
    revenue = defaultdict(int)
    sold_cnt = defaultdict(int)

    for pid, purchase_date, units in units_sold:
        purchase_dt = to_date(purchase_date)

        # 若该商品在 price 表中根本没有价签，直接视为 price = 0（题目不太会出现）
        if pid not in start_dict:
            price = 0
        else:
            starts = start_dict[pid]
            intervals = interval_dict[pid]

            # 二分找最近的 start ≤ purchase_dt
            idx = bisect.bisect_right(starts, purchase_dt) - 1
            if idx < 0:
                price = 0   # 购买日期早于所有价签的起始日期
            else:
                s, e, price = intervals[idx]
                # 保险检查：若购买日期超过该价签的 end_date，则说明没有匹配的价签
                if purchase_dt > e:
                    price = 0

        revenue[pid] += price * units
        sold_cnt[pid] += units

    # 3️⃣ 计算平均价
    all_products = set(start_dict.keys()) | {pid for pid, *_ in units_sold}
    result = []
    for pid in all_products:
        if sold_cnt[pid] == 0:
            avg = 0.0
        else:
            avg = round(revenue[pid] / sold_cnt[pid] + 1e-9, 2)
        result.append((pid, avg))

    return result
```

#### 复杂度

- **时间复杂度**：`O(N log M + M log M)`  
  - `M log M` 来自对每个商品的价签进行一次排序（只需要一次）。  
  - 对每笔销售的二分查找是 `O(log M_i)`，累计为 `O(N log M)`（`M_i` 为对应商品的价签数量，最坏情况 `log M`）。  
  - 与暴力解的 `O(N * M)` 相比，**对数级的提升**就像把「走全程」变成「坐地铁」——速度快得多。

- **空间复杂度**：`O(M + K)`  
  - 需要存储分组后的价签列表（`O(M)`）以及累计的 `revenue`、`sold_cnt`（`O(K)`，`K` 为商品种类数）。


---

## 心得

- **核心技巧**：**对有序区间进行二分查找**（也可以称作「离散化 + 前缀」的思路）。  
- **适用的题型**  
  1. 给定时间区间的价格/费率，求某日期对应的值（如“股票历史分红”）。  
  2. 多段函数求值（如“阶梯函数求和”）或区间覆盖查询。  
- **解题钥匙**：先把**区间表**按 `product_id` 分组并排序，让“寻找对应区间”可以用二分或指针一次完成。

---

## 反思

- **第一反应**：看到两个表，立刻想到“把它们 **JOIN** 在一起”。如果是 SQL 直接写 `JOIN` + `GROUP BY`，思路很自然；转成 Python 时，往往会忘记先把价签按时间排序，导致只能用暴力遍历。
- **最容易踩的坑**  
  - **日期比较**：字符串直接比较在 `YYYY-MM-DD` 格式下是可以的，但为避免潜在错误，最好转成 `datetime` 对象。  
  - **区间不存在**：购买日期可能在所有价签之前或之后，需要处理 `idx < 0` 或 `purchase_dt > end_date` 的情况，否则会抛异常。  
  - **除零**：没有销量的商品要返回 `0.0`，否则会出现除以零的错误。  
- **下次类似题**：第一步先 **“把区间表整理成有序结构（排序、分组）”**，再决定是用 **二分** 还是 **双指针** 来匹配日期/数值。这样可以把 O(N·M) 的暴力遍历直接降到 O(N log M) 或更低。