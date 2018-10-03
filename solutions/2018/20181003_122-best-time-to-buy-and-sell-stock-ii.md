# #122. 买卖股票的最佳时机 II / Best Time to Buy and Sell Stock II

> 难度：中等 · 标签：Array、Dynamic Programming、Greedy · [LeetCode 链接](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/)

---

## 题目（英文原版）

**Description**

You are given an integer array prices where prices[i] is the price of a given stock on the ith day.
On each day, you may decide to buy and/or sell the stock. You can only hold at most one share of the stock at any time. However, you can buy it then immediately sell it on the same day.
Find and return the maximum profit you can achieve.

**Examples**

**Example 1:**

```
Input: prices = [7,1,5,3,6,4]
Output: 7
Explanation: Buy on day 2 (price = 1) and sell on day 3 (price = 5), profit = 5-1 = 4.
Then buy on day 4 (price = 3) and sell on day 5 (price = 6), profit = 6-3 = 3.
Total profit is 4 + 3 = 7.
```

**Example 2:**

```
Input: prices = [1,2,3,4,5]
Output: 4
Explanation: Buy on day 1 (price = 1) and sell on day 5 (price = 5), profit = 5-1 = 4.
Total profit is 4.
```

**Example 3:**

```
Input: prices = [7,6,4,3,1]
Output: 0
Explanation: There is no way to make a positive profit, so we never buy the stock to achieve the maximum profit of 0.
```

**Constraints**

- 1 <= prices.length <= 3 * 104
- 0 <= prices[i] <= 104

---

## 题目（中文翻译）

给定一个整数数组 (integer array) **prices**，其中 `prices[i]` 表示第 *i* 天的股票价格。  
在每一天，你可以决定 **买入** 和/或 **卖出** 股票。任意时刻你最多只能持有一股股票，但可以在同一天先买入后立即卖出。  
求你能够获得的最大利润并返回。

**示例 1**  
**输入**: `prices = [7,1,5,3,6,4]`  
**输出**: `7`  
**解释**:  
- 第 2 天买入（价格 = 1），第 3 天卖出（价格 = 5），利润 = 5‑1 = 4。  
- 第 4 天买入（价格 = 3），第 5 天卖出（价格 = 6），利润 = 6‑3 = 3。  
- 总利润 = 4 + 3 = 7。  

**示例 2**  
**输入**: `prices = [1,2,3,4,5]`  
**输出**: `4`  
**解释**:  
- 第 1 天买入（价格 = 1），第 5 天卖出（价格 = 5），利润 = 5‑1 = 4。  
- 总利润 = 4。  

**示例 3**  
**输入**: `prices = [7,6,4,3,1]`  
**输出**: `0`  
**解释**:  
- 没有任何交易能够获得正利润，因此不进行买卖，最大利润为 0。  

**约束条件**  
- `1 <= prices.length <= 3 * 10^4`  
- `0 <= prices[i] <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把所有可能的买卖组合都枚举一遍，挑出利润最大的那种。  
- **数据结构**：我们只需要一个普通的 Python 列表 `prices`，它就像一本记录每天股价的日记。  
- **暴力做法**：对每一天 `i`，假设在这一天买入，然后在后面的每一天 `j (j>i)` 卖出，计算 `prices[j] - prices[i]` 的利润。把所有利润相加（因为题目允许多次买卖，只要不同时持有两只股票），取最大值。  
- **为什么正确**：我们遍历了所有合法的买卖时机组合，最大利润一定会出现在这些组合之中。  

> 这里的“暴力”相当于把所有可能的交易路径都列出来，就像在超市里把每一种可能的购物路线都走一遍再挑最省钱的那条。

#### 代码（Python）
```python
def maxProfit_bruteforce(prices):
    n = len(prices)
    # profit[i] 表示在第 i 天结束时（手上可以没有股票）能够得到的最大利润
    profit = [0] * n
    for i in range(1, n):
        max_today = profit[i - 1]          # 不在第 i 天做任何事
        # 枚举所有可能的买入日 k（k < i），在第 i 天卖出
        for k in range(i):
            # profit[k] 是在第 k 天结束时的最大利润，
            # 再加上当天卖出的收益 prices[i] - prices[k]
            max_today = max(max_today, profit[k] + prices[i] - prices[k])
        profit[i] = max_today
    return profit[-1]
```
> 关键点解释  
> - `profit` 列表相当于一个记事本，记录每一天结束时的“最高可能钱”。  
> - 内层循环 `for k in range(i)` 就是把所有可能的买入日都尝试一次。

#### 复杂度
- **时间复杂度**：`O(n²)` —— 对每一天 `i` 都要遍历它之前的所有天数 `k`，相当于做了 `n` 次 `n/2` 次操作。用大白话说，就是“如果天数是 1000，循环大约要跑 500,000 次”。  
- **空间复杂度**：`O(n)` —— 需要一个和天数等长的数组 `profit` 来保存中间结果。

---

### 2. 最优解

#### 思路  
从暴力解可以看到，**瓶颈**在于每一天都要遍历所有之前的买入日，导致二次方的时间。其实这道题有一个更简单的贪心（Greedy）性质：

- 如果第 `i` 天的股价比第 `i-1` 天高，**把这段上涨的差价全部拿来赚**。因为我们可以在第 `i-1` 天买入，在第 `i` 天卖出，收益正好是 `prices[i] - prices[i-1]`。  
- 只要把所有正的相邻差价加起来，就等价于把每一段上升区间的最低点买入、最高点卖出。  

**为什么这样做一定是最优的？**  
想象一条山坡：从谷底爬到山顶，中间可能会有起伏。如果我们在每一次上坡的开始买入、在每一次下坡的开始卖出，累计的利润恰好等于从谷底直接买到山顶的利润。把所有小的“买-卖”拼起来，利润不变，甚至更灵活（可以在同一天买卖）。因此，**只要把所有正的相邻差价相加，就是最大可能利润**。

> 类比：这就像在超市里买东西，只要每次看到价格比前一次低，就立刻买进；每次价格比前一次高，就立刻卖出，累计的省钱（或赚钱）就是最优的。

#### 代码（Python）
```python
def maxProfit(prices):
    """
    贪心解：把所有相邻正差值累加
    """
    profit = 0
    for i in range(1, len(prices)):
        diff = prices[i] - prices[i - 1]   # 当天和前一天的价差
        if diff > 0:                       # 只在上涨时赚钱
            profit += diff                 # 累加到总利润
    return profit
```
> 关键行解释  
> - `diff = prices[i] - prices[i - 1]`：相当于“今天的价格和昨天的价格相比，涨了多少”。  
> - `if diff > 0: profit += diff`：只有在涨的情况下才把这部分利润记下来。

#### 复杂度
- **时间复杂度**：`O(n)` —— 只遍历一次数组，线性增长。比如 30,000 天只需要跑 30,000 次操作，几乎瞬间完成。  
- **空间复杂度**：`O(1)` —— 只用了几个额外的变量（`profit`、`diff`），不随输入规模增加。

---

## 心得

- **核心技巧**：**贪心**——在每一次局部最优（只在价格上升时买卖）累加，即得到全局最优。  
- **适用的题型**  
  1. “Best Time to Buy and Sell Stock I/II/III” 系列（只要可以多次买卖且没有额外限制）。  
  2. “Maximum Subarray” 类似的累计求和问题。  
  3. “Gas Station” 这类只需要局部判断能否前进的题目。  
- **一句话总结解题钥匙**：**只要价格出现上涨，就立刻抓住这段利润；所有上涨段的利润相加即是最大收益**。

---

## 反思

- **第一反应**：看到“可以多次买卖”，立刻想到“把所有上涨的区间都利用”，但如果不熟悉贪心，往往会先写出复杂的 DP 或递归。  
- **最容易踩的坑**  
  - 忘记“可以在同一天买卖”，导致在等价的 `prices[i] == prices[i+1]` 时误认为必须持股。  
  - 忽视全为下降的情况，需要返回 `0` 而不是负数。  
- **下次遇到同类题，第一步该想到**：**“局部最优是否等价于全局最优？”** 如果答案是“是”，就尝试贪心；如果不是，再考虑 DP 或单调栈等更高级的技巧。