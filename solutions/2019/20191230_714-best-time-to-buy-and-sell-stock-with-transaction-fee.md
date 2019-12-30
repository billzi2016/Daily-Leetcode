# #714. 带交易费的买卖股票的最佳时机 / Best Time to Buy and Sell Stock with Transaction Fee

> 难度：中等 · 标签：Array、Dynamic Programming、Greedy · [LeetCode 链接](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/)

---

## 题目（英文原版）

**Description**

You are given an array prices where prices[i] is the price of a given stock on the ith day, and an integer fee representing a transaction fee.
Find the maximum profit you can achieve. You may complete as many transactions as you like, but you need to pay the transaction fee for each transaction.
Note:

**Examples**

**Example 1:**

```
Input: prices = [1,3,2,8,4,9], fee = 2
Output: 8
Explanation: The maximum profit can be achieved by:
- Buying at prices[0] = 1
- Selling at prices[3] = 8
- Buying at prices[4] = 4
- Selling at prices[5] = 9
The total profit is ((8 - 1) - 2) + ((9 - 4) - 2) = 8.
```

**Example 2:**

```
Input: prices = [1,3,7,5,10,3], fee = 3
Output: 6
```

**Constraints**

- 1 <= prices.length <= 5 * 104
- 1 <= prices[i] < 5 * 104
- 0 <= fee < 5 * 104

---

## 题目（中文翻译）

给定一个数组 **prices**，其中 `prices[i]` 表示第 *i* 天的股票价格，以及一个整数 **fee** 表示每笔交易的交易费 (transaction fee)。  
求你能够获得的最大利润。你可以进行任意次数的买入卖出操作，但每完成一次买入‑卖出（即一次完整的交易）都需要支付一次交易费。

**示例 1**  
Input: `prices = [1,3,2,8,4,9]`, `fee = 2`  
Output: `8`  
**解释**：可以通过以下操作获得最大利润  
- 在 `prices[0] = 1` 时买入  
- 在 `prices[3] = 8` 时卖出  
- 在 `prices[4] = 4` 时再次买入  
- 在 `prices[5] = 9` 时再次卖出  

总利润为 `((8 - 1) - 2) + ((9 - 4) - 2) = 8`。

**示例 2**  
Input: `prices = [1,3,7,5,10,3]`, `fee = 3`  
Output: `6`

**约束条件**  

- `1 <= prices.length <= 5 * 10^4`  
- `1 <= prices[i] < 5 * 10^4`  
- `0 <= fee < 5 * 10^4`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：**枚举每一次买入和卖出的时机**，把所有可能的交易组合都算一遍，挑出利润最大的那种。  
可以把它想成在一条街上挑选**买东西的摊位**和**卖东西的摊位**：  
- 先选一个摊位 `i`（买），再在它后面的任意摊位 `j`（卖）把手里的股票卖掉，利润是 `prices[j] - prices[i] - fee`（相当于在字典里查到“买价”和“卖价”之间的差，再扣掉手续费）。  
- 卖完以后，继续在 `j+1` 之后挑选下一对买卖。  

把上述过程递归下来，就可以得到 **所有可能的交易序列**，取最大值即为答案。  

> 为什么这个方法一定能得到正确答案？  
> 因为我们没有任何剪枝或贪心假设，所有合法的买卖顺序都被枚举到了，最大利润自然会被找到。  

> 时间/空间复杂度怎么解释？  
> - 每一次递归都要遍历后面的所有卖出日 `j`，而递归的层数最多是 `n`（每次至少买一次），于是时间复杂度大约是 `O(n²)`（实际上更接近 `O(2^n)`，但为了说明直观，这里用 `O(n²)` 来表示枚举所有买卖对的次数）。  
> - 递归栈最多保存 `n` 层调用，空间复杂度是 `O(n)`。  

#### 代码（Python）  

```python
from functools import lru_cache

def maxProfit_bruteforce(prices, fee):
    n = len(prices)

    # @lru_cache 把相同的子问题结果记下来，防止指数级重复计算
    @lru_cache(maxsize=None)
    def dfs(start):
        """
        从第 start 天开始，手里没有持股，能够得到的最大利润。
        """
        if start >= n:                     # 已经到了最后一天，不能再交易
            return 0

        best = 0                           # 不进行任何交易的情况
        # 枚举买入日 i
        for i in range(start, n):
            # 枚举卖出日 j（必须在 i 之后）
            for j in range(i + 1, n):
                profit = prices[j] - prices[i] - fee   # 卖出得到的净利润
                if profit > 0:                         # 只有盈利才值得做
                    # 在卖出后继续从 j+1 天开始寻找后面的交易
                    best = max(best, profit + dfs(j + 1))
        return best

    return dfs(0)


# ------------------- 测试 -------------------
if __name__ == "__main__":
    print(maxProfit_bruteforce([1, 3, 2, 8, 4, 9], 2))   # 8
    print(maxProfit_bruteforce([1, 3, 7, 5, 10, 3], 3)) # 6
```

- 关键点说明  
  - `@lru_cache` 相当于“记事本”，把已经算过的子问题（从第 `k` 天开始的最大利润）记下来，避免重复计算。  
  - `profit > 0` 相当于“如果这笔买卖会亏钱，就不要做”。  

#### 复杂度  

- **时间复杂度：** `O(n²)`（每个买入日遍历所有后面的卖出日），在最坏情况下仍然会遍历大约 `n·(n-1)/2` 对。  
  - 大白话：如果有 10,000 天的股价，大约要检查 5,0000,000（五千万）次，显然太慢。  
- **空间复杂度：** `O(n)`，主要是递归栈和缓存表占用的空间。  

---

### 2. 最优解  

#### 思路  

从暴力解我们可以看到 **瓶颈** 在于：每一天都要去回溯所有以后可能的卖出日，导致大量重复计算。  
实际上，在任意一天结束时，**我们只关心两种“状态”**：

1. **不持股**（手里没有股票），记为 `cash`，表示到目前为止手里剩下的最大现金。  
2. **持股**（手里有一支股票），记为 `hold`，表示到目前为止手里剩下的最大“净资产”（现金 + 持有的那支股票的成本）。  

这两个状态之间只会在 **买入** 或 **卖出** 时切换：

- **买入**：把一部分现金换成股票，`hold = max(hold, cash - prices[i])`  
  - 把 `cash` 减去当天的股价，得到买入后的“净资产”。  
- **卖出**：把手里的股票卖掉，同时支付手续费，`cash = max(cash, hold + prices[i] - fee)`  
  - 把 `hold` 加上当天的股价，再减去手续费，得到卖出后的现金。

这就是**动态规划**的核心：**每一步只保留最优的两种状态**，不必记录所有历史细节。  

> 为什么只需要两种状态就够了？  
> 想象你在路上行走，每走一步只能决定是“空手”还是“背着背包”。背包里装的东西价值只取决于**你上一次把东西放进去的时刻**（买入价），而不需要记住之前所有的走法。于是我们只需要记住“空手时最好的现金”和“背着背包时最好的净资产”。  

> 这套思路其实是一种**贪心 + DP**的混合。因为状态转移只依赖前一天的结果，时间上是线性的，空间上可以压缩到常数。  

#### 代码（Python）  

```python
def maxProfit_optimal(prices, fee):
    """
    使用状态机 DP（两状态）求最大利润。
    cash：到当前天为止，不持股时手里拥有的最大现金。
    hold：到当前天为止，持股时手里拥有的最大“净资产”（现金 - 买入成本）。
    初始时我们没有任何股票，cash 为 0，hold 为 -prices[0]（相当于买入第一天的股票）。
    """
    cash, hold = 0, -prices[0]          # 第 0 天结束时的两种状态

    for i in range(1, len(prices)):
        price = prices[i]

        # 先算卖出后可能得到的更大 cash（先用旧的 hold）
        new_cash = max(cash, hold + price - fee)
        # 再算买入后可能得到的更大 hold（先用旧的 cash）
        new_hold = max(hold, cash - price)

        cash, hold = new_cash, new_hold   # 更新为今天的状态

    # 最终我们必须“手里不持股”，因为持股的话要再卖掉才能变成真正的利润
    return cash


# ------------------- 测试 -------------------
if __name__ == "__main__":
    print(maxProfit_optimal([1, 3, 2, 8, 4, 9], 2))   # 8
    print(maxProfit_optimal([1, 3, 7, 5, 10, 3], 3)) # 6
```

- 关键行注释  
  - `cash = max(cash, hold + price - fee)`：**卖出**，如果今天卖出能得到比保持不动更多的现金，就更新。  
  - `hold = max(hold, cash - price)`：**买入**，如果今天买入能得到比已经持有的更大的净资产，就更新。  
  - 初始化 `hold = -prices[0]`：相当于在第 0 天买入一支股票，花掉 `prices[0]`，所以净资产是负数。  

#### 复杂度  

- **时间复杂度：** `O(n)`，只遍历一次价格数组。  
  - 大白话：如果有 50,000 天，只需要走 50,000 步，每一步做几次加减比较，几乎瞬间完成。  
- **空间复杂度：** `O(1)`，只用到 `cash`、`hold` 两个变量，和输入规模无关。  

---

## 心得  

- **核心技巧**：**状态机动态规划**（两个状态：持股 / 不持股） + **贪心式更新**。  
- **适用的题型**（类似思路）  
  1. *Best Time to Buy and Sell Stock*（无手续费）  
  2. *Best Time to Buy and Sell Stock II*（允许多次交易）  
  3. *Best Time to Buy and Sell Stock with Cooldown*（买卖后需要冷却一天）  
- **一句话总结解题钥匙**：**只维护“手里有股票”和“手里没有股票”两种最优收益，逐日递推即可**。  

---

## 反思  

- **拿到题目第一反应**：先想把所有买卖组合枚举出来，确保不遗漏任何可能的盈利点。  
- **最容易踩的坑**  
  - **手续费的处理**：卖出时要先把手续费扣掉，不能忘记在 `cash` 更新式里减 `fee`。  
  - **初始化**：`hold` 必须设为 `-prices[0]`（相当于第一天买入），否则后面的 `cash` 计算会偏高。  
  - **返回值**：最终答案一定是 `cash`（不持股），因为持股状态仍然有成本未结算。  
- **下次遇到同类题，第一步该想到**：**把问题抽象为“今天手里是有还是没有股票”，列出两种状态的转移方程，再用 O(n) 迭代求解**。