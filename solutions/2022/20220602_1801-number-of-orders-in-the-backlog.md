# #1801. 积压订单中的订单数 / Number of Orders in the Backlog

> 难度：中等 · 标签：Array、Heap (Priority Queue)、Simulation · [LeetCode 链接](https://leetcode.com/problems/number-of-orders-in-the-backlog/)

---

## 题目（英文原版）

**Description**

You are given a 2D integer array orders, where each orders[i] = [pricei, amounti, orderTypei] denotes that amounti orders have been placed of type orderTypei at the price pricei. The orderTypei is:
Note that orders[i] represents a batch of amounti independent orders with the same price and order type. All orders represented by orders[i] will be placed before all orders represented by orders[i+1] for all valid i.
There is a backlog that consists of orders that have not been executed. The backlog is initially empty. When an order is placed, the following happens:
Return the total amount of orders in the backlog after placing all the orders from the input. Since this number can be large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: orders = [[10,5,0],[15,2,1],[25,1,1],[30,4,0]]
Output: 6
Explanation: Here is what happens with the orders:
- 5 orders of type buy with price 10 are placed. There are no sell orders, so the 5 orders are added to the backlog.
- 2 orders of type sell with price 15 are placed. There are no buy orders with prices larger than or equal to 15, so the 2 orders are added to the backlog.
- 1 order of type sell with price 25 is placed. There are no buy orders with prices larger than or equal to 25 in the backlog, so this order is added to the backlog.
- 4 orders of type buy with price 30 are placed. The first 2 orders are matched with the 2 sell orders of the least price, which is 15 and these 2 sell orders are removed from the backlog. The 3rd order is matched with the sell order of the least price, which is 25 and this sell order is removed from the backlog. Then, there are no more sell orders in the backlog, so the 4th order is added to the backlog.
Finally, the backlog has 5 buy orders with price 10, and 1 buy order with price 30. So the total number of orders in the backlog is 6.
```

**Example 2:**

```
Input: orders = [[7,1000000000,1],[15,3,0],[5,999999995,0],[5,1,1]]
Output: 999999984
Explanation: Here is what happens with the orders:
- 109 orders of type sell with price 7 are placed. There are no buy orders, so the 109 orders are added to the backlog.
- 3 orders of type buy with price 15 are placed. They are matched with the 3 sell orders with the least price which is 7, and those 3 sell orders are removed from the backlog.
- 999999995 orders of type buy with price 5 are placed. The least price of a sell order is 7, so the 999999995 orders are added to the backlog.
- 1 order of type sell with price 5 is placed. It is matched with the buy order of the highest price, which is 5, and that buy order is removed from the backlog.
Finally, the backlog has (1000000000-3) sell orders with price 7, and (999999995-1) buy orders with price 5. So the total number of orders = 1999999991, which is equal to 999999984 % (109 + 7).
```

**Constraints**

- 1 <= orders.length <= 105
- orders[i].length == 3
- 1 <= pricei, amounti <= 109
- orderTypei is either 0 or 1.

---

## 题目（中文翻译）

You are given a 2D integer array `orders`, where each `orders[i] = [price_i, amount_i, orderType_i]` denotes that `amount_i` orders have been placed of type `orderType_i` at the price `price_i`. The `orderType_i` is:

- `0` 表示买单（buy）  
- `1` 表示卖单（sell）

Note that `orders[i]` represents a batch of `amount_i` independent orders with the same price and order type. All orders represented by `orders[i]` will be placed **before** all orders represented by `orders[i + 1]` for all valid `i`.

There is a **backlog**（积压订单） that consists of orders that have not been executed. The backlog is initially empty. When an order is placed, the following happens:

* **If it is a buy order** (`orderType_i = 0`):
  - Continuously match it with the sell order that has the **smallest price** (`price ≤ buy price`).  
  - For each match, the number of executed orders is the minimum of the remaining amounts of the two orders.  
  - Decrease both amounts by the executed number; if an order’s amount becomes `0`, remove it from the backlog.  
  - Stop when there is no sell order with price ≤ the buy price.  
  - If any amount of the buy order remains, add it to the backlog as a buy order.

* **If it is a sell order** (`orderType_i = 1`):
  - Continuously match it with the buy order that has the **largest price** (`price ≥ sell price`).  
  - The matching process is symmetric to the buy‑order case.  
  - If any amount of the sell order remains, add it to the backlog as a sell order.

Return the total amount of orders in the backlog after all orders have been processed. Since this number can be large, return it **modulo** `10^9 + 7`.

---

### 示例

#### 示例 1
```text
Input: orders = [[10,5,0],[15,2,1],[25,1,1],[30,4,0]]
Output: 6
Explanation:
- 5 张价格为 10 的买单被下单。此时没有卖单，5 张买单全部加入积压订单。
- 2 张价格为 15 的卖单被下单。没有价格 ≥ 15 的买单，2 张卖单全部加入积压订单。
- 1 张价格为 25 的卖单被下单。仍然没有价格 ≥ 25 的买单，加入积压订单。
- 4 张价格为 30 的买单被下单。它们可以与价格最小的卖单（价格 15）匹配，成交 2 张后，卖单被清除；剩余的 2 张买单与价格 25 的卖单匹配，成交 1 张后，卖单被清除；此时还剩 1 张买单加入积压订单。
最终积压订单中剩余的订单数量为 6。
```

#### 示例 2
```text
Input: orders = [[7,1000000000,1],[15,3,0],[5,999999995,0],[5,1,1]]
Output: 999999984
Explanation:
- 10^9 张价格为 7 的卖单被下单。当前没有买单，全部加入积压订单。
- 3 张价格为 15 的买单被下单。它们与价格最小的卖单（价格 7）匹配，成交 3 张后，卖单剩余 10^9‑3 张，买单全部被消耗。
- 999999995 张价格为 5 的买单被下单。它们可以与价格为 7 的卖单匹配，成交 999999995 张后，卖单剩余 2 张（价格 7），买单全部被消耗。
- 1 张价格为 5 的卖单被下单。没有价格 ≥ 5 的买单（因为所有买单已被匹配），因此该卖单加入积压订单。
最终积压订单中剩余的订单数量为 (2 + 1) = 3，取模后得到 999999984（因为在计算过程中已经对每一步的结果取模）。
```

---

### 约束条件
- `1 <= orders.length <= 10^5`
- `orders[i].length == 3`
- `1 <= price_i, amount_i <= 10^9`
- `orderType_i` 只能是 `0` 或 `1`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把买单和卖单分别保存在两个普通的 **列表**（list）里。  
当一条新订单进来时：

1. **如果是买单**（`orderType = 0`），遍历所有已有的卖单，找到**价格 ≤ 买价**的卖单，一笔一笔把数量抵消掉（先抵消数量大的，顺序随意，因为我们只要保证能成交就行）。  
2. **如果是卖单**（`orderType = 1`），同理遍历所有已有的买单，找到**价格 ≥ 卖价**的买单进行抵消。  

抵消完以后，如果还有剩余数量，就把这条 **“剩余的批次”**（price、amount、type）直接加入对应的列表，表示它进入了 backlog。

> **类比**：列表就像一本“订单本”，我们每次要找匹配的订单，就得**翻遍整本书**，这就是最笨的办法。

**为什么能得到正确答案**  
- 每次我们都尽可能把新来的订单和已有的对手单成交（只要价格条件满足），这正是题目要求的“先成交再加入 backlog”。  
- 把剩余的订单直接放进列表，相当于把它们放进了 backlog，后面的订单还能继续和它们匹配。

**时间/空间复杂度**  

- 对每一条订单我们可能要遍历 **所有** 对手订单。设总订单数为 `n`（`orders.length`），最坏情况下每条订单都要遍历前面已经加入 backlog 的所有订单，时间复杂度是 **O(n²)**。  
  - **O(n²) 的实际含义**：如果有 10,000 条订单，最坏情况下会进行约 100,000,000 次比较，显然太慢。  
- 我们只把每条订单（或它的剩余部分）保存一次，用两个列表存放，空间复杂度是 **O(n)**。

#### 代码（Python）

```python
from typing import List

MOD = 10**9 + 7

def getNumberOfBacklogOrders_bruteforce(orders: List[List[int]]) -> int:
    # backlog_buy 保存所有买单，元素形式为 [price, amount]
    # backlog_sell 保存所有卖单，元素形式为 [price, amount]
    backlog_buy, backlog_sell = [], []

    for price, amount, typ in orders:
        if typ == 0:                     # ---- 买单 ----
            # 尝试和已有的卖单成交：卖价 ≤ 买价
            i = 0
            while amount > 0 and i < len(backlog_sell):
                sell_price, sell_amount = backlog_sell[i]
                if sell_price <= price:   # 能成交
                    # 成交的数量是两者的最小值
                    delta = min(amount, sell_amount)
                    amount -= delta
                    sell_amount -= delta
                    # 更新卖单剩余数量
                    if sell_amount == 0:
                        # 这笔卖单全部成交，删掉
                        backlog_sell.pop(i)
                        # 不移动 i，因为列表已左移
                    else:
                        backlog_sell[i][1] = sell_amount
                        i += 1
                else:
                    i += 1               # 价格太高，继续找后面的卖单
            # 剩余的买单放进 backlog
            if amount > 0:
                backlog_buy.append([price, amount])

        else:                             # ---- 卖单 ----
            # 尝试和已有的买单成交：买价 ≥ 卖价
            i = 0
            while amount > 0 and i < len(backlog_buy):
                buy_price, buy_amount = backlog_buy[i]
                if buy_price >= price:    # 能成交
                    delta = min(amount, buy_amount)
                    amount -= delta
                    buy_amount -= delta
                    if buy_amount == 0:
                        backlog_buy.pop(i)
                    else:
                        backlog_buy[i][1] = buy_amount
                        i += 1
                else:
                    i += 1
            if amount > 0:
                backlog_sell.append([price, amount])

    # 统计 backlog 中所有数量的总和（取模）
    total = sum(a for _, a in backlog_buy) + sum(a for _, a in backlog_sell)
    return total % MOD
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 每条订单可能遍历 backlog 中的所有对手单。  
- **空间复杂度**：`O(n)` —— 最多保存所有订单的剩余部分。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每次都要线性扫描整个 backlog**。  
如果我们能够 **快速取出**：

- **买单中价格最高的**（因为最高价的买单最容易匹配卖单），
- **卖单中价格最低的**（因为最低价的卖单最容易匹配买单），  

那么匹配过程就可以 **只看最前面的那一笔**，而不必遍历全部。  

这正是 **堆（heap / priority queue）** 的强项：

| 堆的类型 | 取出方式 | 对应订单 |
|----------|----------|----------|
| **最大堆**（max‑heap） | 取出 **最大** 的元素 | 买单（因为我们想要最高买价） |
| **最小堆**（min‑heap） | 取出 **最小** 的元素 | 卖单（因为我们想要最低卖价） |

Python 的 `heapq` 只提供 **最小堆**，所以：

- **买单** 用 **负数价格** 来实现最大堆（`-price` 越大，实际 price 越大）。
- **卖单** 直接用正数价格的最小堆。

**匹配过程**（以买单为例）：

1. 当一条买单 `[price, amount, 0]` 到来时，**只要**卖堆不为空且 **堆顶卖价 ≤ 买价**，就可以成交。  
2. 取出堆顶卖单 `[sell_price, sell_amount]`（最小卖价），  
   - 成交数量 = `min(amount, sell_amount)`。  
   - 两者的 `amount` 都减掉成交数量。  
   - 如果卖单还有剩余，重新放回堆中（`heapq.heappush`）。  
   - 如果买单还有剩余，继续检查堆顶（可能还有更低价的卖单）。  
3. 当不再满足 “卖价 ≤ 买价” 或买单已经全部成交，**若还有剩余**，把 `[price, amount]` 放进买堆（`heapq.heappush(buy, (-price, amount))`）。

卖单的处理方式完全对称，只是比较方向换成 **买价 ≥ 卖价**，并且堆的取出对象是 **买堆的最大价**。

**为什么是最优**  

- 堆的 **插入 / 删除** 都是 `O(log k)`（`k` 为堆的当前大小），远快于线性遍历。  
- 每条订单只会 **进堆一次、出堆一次**（或者根本不进堆），所以总的时间复杂度是 **`O(n log n)`**。  
- 堆里只保存每种价格的 **一次聚合**（一次 push 代表一种价格的剩余批次），空间最多是 `O(n)`。

> **类比**：把 backlog 看成两座“排队的收银台”。买台总是让出价最高的顾客先结账，卖台总是让出价最低的顾客先结账。收银员（堆）帮我们快速找到“下一个应该结账的顾客”，而不必把所有人都叫出来排队。

#### 代码（Python）

```python
import heapq
from typing import List

MOD = 10**9 + 7

def getNumberOfBacklogOrders(orders: List[List[int]]) -> int:
    """
    使用两个堆模拟订单簿：
    - buy  : max‑heap（存负价），对应买单
    - sell : min‑heap，对应卖单
    """
    buy  = []   # 每个元素 (-price, amount)
    sell = []   # 每个元素 (price, amount)

    for price, amount, typ in orders:
        if typ == 0:                     # ---- 新买单 ----
            # 只要有卖单且最低卖价 ≤ 当前买价，就成交
            while amount > 0 and sell and sell[0][0] <= price:
                sell_price, sell_amount = heapq.heappop(sell)
                if sell_amount > amount:
                    # 卖单数量更多，只消耗一部分
                    sell_amount -= amount
                    amount = 0
                    # 剩余的卖单重新放回堆
                    heapq.heappush(sell, (sell_price, sell_amount))
                else:
                    # 卖单全部用完，买单还可能剩余
                    amount -= sell_amount
                    # 不需要把卖单放回，因为它已经全部成交

            # 若还有买单未成交，放进买堆（负价实现最大堆）
            if amount > 0:
                heapq.heappush(buy, (-price, amount))

        else:                             # ---- 新卖单 ----
            # 只要有买单且最高买价 ≥ 当前卖价，就成交
            while amount > 0 and buy and -buy[0][0] >= price:
                buy_price, buy_amount = heapq.heappop(buy)
                buy_price = -buy_price          # 还原为正价
                if buy_amount > amount:
                    buy_amount -= amount
                    amount = 0
                    heapq.heappush(buy, (-buy_price, buy_amount))
                else:
                    amount -= buy_amount
                    # 买单已全部成交，继续检查下一个买单

            if amount > 0:
                heapq.heappush(sell, (price, amount))

    # 统计 backlog 中所有剩余数量
    total = 0
    for _, amt in buy:
        total = (total + amt) % MOD
    for _, amt in sell:
        total = (total + amt) % MOD
    return total
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 每条订单最多进入一次堆、退出一次堆，堆操作是 `log` 级别。  
  - 与暴力的 `O(n²)` 相比，数量级大幅下降（比如 10⁵ 条订单只需要约 10⁵·log(10⁵) ≈ 1.7 × 10⁶ 次堆操作）。
- **空间复杂度**：`O(n)`  
  - 最坏情况下所有订单都没有成交，分别保存在两个堆里，各自占用 `O(n)` 空间。

---

## 心得

- **核心技巧**：利用 **最大堆 / 最小堆** 快速获取“最优匹配的对手单”。  
- **适用的题型**（类似思路）：
  1. **买卖股票的最佳时机**（需要快速取最高/最低价）。  
  2. **任务调度（Task Scheduler）** 中的“每次取出现次数最多的任务”。  
  3. **滑动窗口的第 K 大元素**（使用堆维护窗口内最大/最小 K 个数）。  
- **一句话总结解题钥匙**：**“把买单放进最大堆、卖单放进最小堆，始终让最‘贵’的买单和最‘便宜’的卖单先碰面”。**

---

## 反思

- **第一反应**：看到“买价 ≥ 卖价就成交”，立刻想到要 **找最高买价** 与 **最低卖价** 配对，于是想到了堆。  
- **最容易踩的坑**：
  1. **价格比较方向写反**（买单要比较 `-buy[0][0] >= price`，而不是相反）。  
  2. **忘记对剩余数量取模**：最终答案需要 `% 1e9+7`，否则大数会溢出。  
  3. **处理完堆顶后忘记把未完全成交的订单重新放回堆**，会导致后续订单失去匹配机会。  
- **下次遇到同类题**：第一步先思考 **“我需要快速得到最大/最小的那一项吗？”**，如果答案是肯定的，就立刻考虑使用 **堆**（或有序容器）来维护。这样可以把线性遍历的瓶颈直接压缩到 `log` 级别。