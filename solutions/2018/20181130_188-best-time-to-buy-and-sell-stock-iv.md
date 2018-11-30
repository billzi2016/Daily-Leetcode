# #188. 买卖股票的最佳时机 IV / Best Time to Buy and Sell Stock IV

> 难度：困难 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/)

---

## 题目（英文原版）

**Description**

You are given an integer array prices where prices[i] is the price of a given stock on the ith day, and an integer k.
Find the maximum profit you can achieve. You may complete at most k transactions: i.e. you may buy at most k times and sell at most k times.
Note: You may not engage in multiple transactions simultaneously (i.e., you must sell the stock before you buy again).

**Examples**

**Example 1:**

```
Input: k = 2, prices = [2,4,1]
Output: 2
Explanation: Buy on day 1 (price = 2) and sell on day 2 (price = 4), profit = 4-2 = 2.
```

**Example 2:**

```
Input: k = 2, prices = [3,2,6,5,0,3]
Output: 7
Explanation: Buy on day 2 (price = 2) and sell on day 3 (price = 6), profit = 6-2 = 4. Then buy on day 5 (price = 0) and sell on day 6 (price = 3), profit = 3-0 = 3.
```

**Constraints**

- 1 <= k <= 100
- 1 <= prices.length <= 1000
- 0 <= prices[i] <= 1000

---

## 题目（中文翻译）

你得到一个整数数组 `prices`，其中 `prices[i]` 表示第 `i` 天的股票价格，以及一个整数 `k`。  
求在最多进行 `k` 笔交易（即最多买入 `k` 次、卖出 `k` 次）的情况下，你能够获得的最大利润。  
注意：同一时间内不能进行多笔交易（即必须在再次买入前先卖出手中的股票）。

**示例 1**  
**输入**: `k = 2, prices = [2,4,1]`  
**输出**: `2`  
**解释**: 第 1 天买入（价格 = 2），第 2 天卖出（价格 = 4），利润 = 4 - 2 = 2。

**示例 2**  
**输入**: `k = 2, prices = [3,2,6,5,0,3]`  
**输出**: `7`  
**解释**: 第 2 天买入（价格 = 2），第 3 天卖出（价格 = 6），利润 = 6 - 2 = 4。随后第 5 天买入（价格 = 0），第 6 天卖出（价格 = 3），利润 = 3 - 0 = 3。总利润 = 4 + 3 = 7。

**约束条件**  
- `1 <= k <= 100`  
- `1 <= prices.length <= 1000`  
- `0 <= prices[i] <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**枚举所有可能的买卖时机**，只要不超过 `k` 笔交易，就计算它们的总利润，取最大值。  
可以把每一天想象成一本日记，**买** 相当于在某页写下“我买了”，**卖** 则是写下“我卖了”。  
暴力解就是把所有可能的“买–卖”配对组合全部列出来，像把所有可能的字典（key 为买的那天，value 为卖的那天）都写在纸上，然后挑出利润最高的那套。

实现上可以使用 **递归**（深度优先搜索）：

1. 从第 `start` 天开始，尝试在第 `i` 天买入（`i >= start`）。
2. 再从第 `i+1` 天开始，尝试在第 `j` 天卖出（`j > i`），得到一次交易的利润 `prices[j] - prices[i]`。
3. 递归求剩余天数内还能进行的最多 `k-1` 笔交易的最大利润。
4. 所有可能的 `(i, j)` 组合取最大值。

这个思路一定能得到正确答案，因为它穷举了**所有合法的交易序列**。只要我们不漏掉任何一种买卖配对，答案必然在其中。

> **为什么会对**  
> - 每一次递归都保证“买在卖之前”，符合题目“不允许同时持有多支股票”的限制。  
> - 递归层数不超过 `k`，所以最多只会进行 `k` 笔交易。  

#### 代码（Python）

```python
from typing import List
import sys

def maxProfit_bruteforce(k: int, prices: List[int]) -> int:
    n = len(prices)
    # 记忆化搜索，避免完全重复计算
    memo = {}

    def dfs(start: int, remaining: int) -> int:
        """
        从 start 位置开始，最多还能完成 remaining 笔交易，返回能得到的最大利润。
        """
        if remaining == 0 or start >= n:
            return 0
        if (start, remaining) in memo:
            return memo[(start, remaining)]

        max_profit = 0
        # 枚举买入的那一天 i
        for i in range(start, n):
            # 枚举卖出的那一天 j，必须在 i 之后
            for j in range(i + 1, n):
                # 这一次交易的利润
                profit = prices[j] - prices[i]
                if profit > 0:  # 只考虑赚钱的交易，亏损的直接跳过
                    # 递归求后面的利润
                    total = profit + dfs(j + 1, remaining - 1)
                    max_profit = max(max_profit, total)
        # 也可以选择不再交易，保持利润不变
        max_profit = max(max_profit, dfs(start + 1, remaining))
        memo[(start, remaining)] = max_profit
        return max_profit

    return dfs(0, k)

# ------------------- 测试 -------------------
if __name__ == "__main__":
    print(maxProfit_bruteforce(2, [2, 4, 1]))          # 2
    print(maxProfit_bruteforce(2, [3, 2, 6, 5, 0, 3]))# 7
```

#### 复杂度  

- **时间复杂度**：`O(n^(2k))`（指数级）  
  > 大白话：假设 `n = 5`，`k = 2`，我们需要把所有可能的买卖对（最多 `n*(n-1)/2` 种）组合起来，然后再在剩下的天数里继续挑选，这种“层层套娃”的过程会导致计算次数呈指数增长。实际运行时会很慢，甚至在 `n=1000, k=100` 时根本跑不完。

- **空间复杂度**：`O(n * k)` 用于记忆化表 `memo`，再加上递归栈深度 `O(k)`。  
  > 大白话：我们需要保存每个 `(start, remaining)` 的结果，最多 `n*k` 个格子，另外递归最多会调用 `k` 层函数。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**大量重复子问题**：同样的“从第 `i` 天开始、还能做 `t` 笔交易”会被不同的递归路径算好多次。我们可以把这些子问题整理成**动态规划（Dynamic Programming，DP）**的形式，只算一次。

---

#### 2.1 DP 状态定义  

设 `dp[t][i]` 表示**在第 `i` 天结束时，最多完成 `t` 笔交易能够得到的最大利润**。  
- `t` 的取值范围是 `0 … k`（0 笔交易利润必然是 0）。  
- `i` 的取值范围是 `0 … n-1`（第 `i` 天是数组下标）。

目标是求 `dp[k][n-1]`，即“在最后一天，最多 `k` 笔交易的最大利润”。

---

#### 2.2 状态转移  

考虑第 `i` 天的两种可能：

1. **不在第 `i` 天卖出**  
   那么利润和第 `i-1` 天相同：`dp[t][i-1]`。

2. **在第 `i` 天卖出**  
   必须在某个更早的天 `j (0 ≤ j < i)` 买入，形成第 `t` 笔交易的最后一次买卖。  
   那么利润为：  
   `prices[i] - prices[j] + dp[t-1][j-1]`  
   - `prices[i] - prices[j]` 是这一次交易的利润。  
   - `dp[t-1][j-1]` 是在第 `j-1` 天之前完成 `t-1` 笔交易的最大利润。

于是：

```
dp[t][i] = max( dp[t][i-1],
                max_{0 ≤ j < i} (prices[i] - prices[j] + dp[t-1][j-1]) )
```

直接套用会导致 **O(k * n²)** 的时间，因为对每个 `(t,i)` 都要遍历所有 `j`。

---

#### 2.3 优化：把内部的 max 提取出来  

观察内部表达式：

```
prices[i] - prices[j] + dp[t-1][j-1]
= (dp[t-1][j-1] - prices[j]) + prices[i]
```

对于固定的 `t`，`prices[i]` 是常数，只要维护 **`maxPrev = max_{0 ≤ j < i} (dp[t-1][j-1] - prices[j])`**，就能在 **O(1)** 时间得到上述最大值。

因此，遍历 `i` 时：

```
maxPrev = max(maxPrev, dp[t-1][i-1] - prices[i])
dp[t][i] = max(dp[t][i-1], prices[i] + maxPrev)
```

这样整体时间降为 **O(k * n)**。

---

#### 2.4 特殊情况：k 大于等于 n/2  

如果 `k` 大到可以在每一次上涨的机会都做交易（相当于“无限次交易”），我们可以直接使用 **贪心**：把所有正向的价差加起来即可。  
判断条件是 `k >= n // 2`（因为一次完整的买卖至少占两天），此时：

```
profit = sum( max(0, prices[i] - prices[i-1]) for i in 1..n-1 )
```

这一步的时间是 **O(n)**，空间 **O(1)**。

---

#### 代码（Python）

```python
from typing import List

def maxProfit(k: int, prices: List[int]) -> int:
    n = len(prices)
    if n == 0:
        return 0

    # ---- 1. 交易次数足够多，等价于无限次交易 ----
    if k >= n // 2:
        # 把所有上涨的差价直接加起来
        profit = 0
        for i in range(1, n):
            diff = prices[i] - prices[i - 1]
            if diff > 0:
                profit += diff
        return profit

    # ---- 2. 动态规划（O(k * n)）----
    # dp[t][i] 只需要前一天的值，使用两行滚动数组节省空间
    dp = [[0] * n for _ in range(k + 1)]

    for t in range(1, k + 1):
        # maxPrev 保存 max(dp[t-1][j-1] - prices[j])，初始化为第0天买入的情况
        maxPrev = -prices[0]  # dp[t-1][-1] 视作 0
        for i in range(1, n):
            # 第 t 笔交易在第 i 天结束的最大利润
            dp[t][i] = max(dp[t][i - 1], prices[i] + maxPrev)
            # 更新 maxPrev，供后面的 i 使用
            maxPrev = max(maxPrev, dp[t - 1][i] - prices[i])
    return dp[k][n - 1]

# ------------------- 测试 -------------------
if __name__ == "__main__":
    print(maxProfit(2, [2, 4, 1]))                # 2
    print(maxProfit(2, [3, 2, 6, 5, 0, 3]))      # 7
    # 额外测试：k 很大时等价于无限次交易
    print(maxProfit(100, [1, 2, 3, 4, 5]))       # 4
```

#### 复杂度  

- **时间复杂度**：`O(k * n)`  
  > 大白话：我们只用了两层循环——外层跑 `k` 次（最多 100），内层跑 `n` 次（最多 1000），所以最多算 `100 * 1000 = 100,000` 次，电脑在毫秒级就能完成。相比指数级的暴力解，这就是“快了一大截”。

- **空间复杂度**：`O(k * n)`（如果使用完整二维表）或 `O(n)`（使用滚动数组只保留上一行）。这里代码用了完整的二维表，空间最多 `101 * 1000 ≈ 1e5`，同样在可接受范围内。  

  与暴力解的 `O(n * k)` 记忆化表相比，额外的空间是线性的，不会出现指数级爆炸。

---

## 心得

- **核心技巧**：把“买入价 + 之前的利润”转化为一个可以在遍历中维护的最大值 `maxPrev`，从而把二重循环降为线性。  
- **适用的题型**  
  1. **股票系列**（Buy and Sell Stock I/II/III/IV）——均涉及买卖次数限制。  
  2. **带限制的区间 DP**（如 “分割数组的最大和”）——需要在遍历时维护历史最优值。  
  3. **背包类 DP** 中的“优化转移”技巧（如 “最大子序和” 的 Kadane 算法）。

- **一句话总结**：**把“买之前的最好状态”抽象为一个变量，遍历一次即可得到最优交易利润**。

---

## 反思

- **第一反应**：直接想到递归/回溯，尝试把所有买卖配对列举出来。  
- **最容易踩的坑**  
  - 忘记 **“买卖必须成对且不能重叠”**，导致状态转移错误。  
  - 当 `k` 很大时仍使用 `O(k·n²)` 的 DP，会超时，需要先判断 `k >= n/2` 并使用贪心。  
  - 边界条件：`prices` 为空或只有一天时，利润一定是 0。  
- **下次遇到同类题**：第一步先判断“交易次数是否可以视为无限”，如果不是，再写出 **`dp[t][i]`** 的定义，随后寻找 **“把内部循环的最值提前维护”** 的机会。这样能迅速把时间复杂度降到线性。