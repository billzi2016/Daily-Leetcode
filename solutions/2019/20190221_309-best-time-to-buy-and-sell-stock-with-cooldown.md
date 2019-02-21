# #309. 最佳买卖股票时机（含冷却期） / Best Time to Buy and Sell Stock with Cooldown

> 难度：中等 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/)

---

## 题目（英文原版）

**Description**

You are given an array prices where prices[i] is the price of a given stock on the ith day.
Find the maximum profit you can achieve. You may complete as many transactions as you like (i.e., buy one and sell one share of the stock multiple times) with the following restrictions:
Note: You may not engage in multiple transactions simultaneously (i.e., you must sell the stock before you buy again).

**Examples**

**Example 1:**

```
Input: prices = [1,2,3,0,2]
Output: 3
Explanation: transactions = [buy, sell, cooldown, buy, sell]
```

**Example 2:**

```
Input: prices = [1]
Output: 0
```

**Constraints**

- 1 <= prices.length <= 5000
- 0 <= prices[i] <= 1000

---

## 题目（中文翻译）

给定一个数组（array）`prices`，其中 `prices[i]` 表示第 `i` 天的股票价格。求你能够获得的最大利润。你可以完成任意次数的交易（即多次买入并卖出一股股票），但需满足以下限制：

- 同一时间只能持有一股股票，必须先 **卖出**（sell）后才能再次 **买入**（buy），即不能同时进行多笔交易。
- 在卖出股票后的**冷却日**（cooldown），即下一天不能买入股票，必须等待一天后才能进行下一次买入。

**示例 1**

```
Input: prices = [1,2,3,0,2]
Output: 3
Explanation: 交易序列 = [buy, sell, cooldown, buy, sell]
```

**示例 2**

```
Input: prices = [1]
Output: 0
```

**约束条件**

- `1 <= prices.length <= 5000`
- `0 <= prices[i] <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的买卖序列**，把每一天当成“要不要交易”的决策点。  
- 对于第 `i` 天，我们可以选择 **不操作**，保持原来的状态。  
- 如果当天手里没有股票，可以 **买入**（前提是昨天不是“卖出后冷却”）。  
- 如果当天手里有股票，可以 **卖出**，卖完后第二天必须进入 **冷却**（即不能再买）。  

这相当于在每一天做一次“是/否”选择，所有可能的组合形成一棵二叉树，遍历整棵树就能得到所有合法的交易方案，取最大利润即为答案。  

> **类比**：把每一天想象成一本日记，写下“今天买了/卖了/啥也没做”。要写出所有合法的日记本，就必须把每一种可能的写法都列出来。

由于我们在递归的每一步都会尝试两种（或三种）选择，递归树的深度是 `n`（天数），分支数近似是 `2`，所以**总的可能性是指数级**，这就是暴力解的本质。

#### 代码（Python）

```python
def maxProfit_bruteforce(prices):
    n = len(prices)

    # 递归函数：第 i 天，手里是否持有股票 (hold)，以及昨天是否刚卖出进入冷却 (cool)
    def dfs(i, hold, cool):
        # 超出最后一天，利润为 0
        if i == n:
            return 0

        # 记忆化缓存，避免同一状态重复计算
        if (i, hold, cool) in memo:
            return memo[(i, hold, cool)]

        # 1. 什么都不做，进入下一天
        profit = dfs(i + 1, hold, False)

        if hold:
            # 2. 如果手里有股票，今天可以卖出，卖出后明天进入冷却
            profit = max(profit,
                         prices[i] + dfs(i + 1, False, True))
        else:
            # 3. 如果手里没有股票且昨天没有冷却，今天可以买入
            if not cool:
                profit = max(profit,
                             -prices[i] + dfs(i + 1, True, False))

        memo[(i, hold, cool)] = profit
        return profit

    memo = {}
    return dfs(0, False, False)
```

> 关键点注释（已在代码中）：  
> - `hold` 表示当前是否持有一支股票（类似背包里有没有物品）。  
> - `cool` 表示昨天是否刚卖出，需要“冷却一天”。  
> - 递归的三条分支对应 “不操作 / 卖出 / 买入”。  

#### 复杂度

- **时间复杂度**：`O(2^n)`（指数级），因为每一天都可能产生两条分支，最坏情况下会遍历所有可能的买卖序列。  
- **空间复杂度**：`O(n)`，递归栈的深度最多为 `n`，另外还有记忆化表 `memo`，最坏也会存 `O(n·2·2)` 条状态，仍然是线性空间。

> **大白话**：如果有 30 天，暴力解大概要尝试 `2^30 ≈ 10⁹` 种情况，显然在电脑里跑不完。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**重复计算相同的子问题**。观察可以发现，决定第 `i` 天的操作，只需要知道**前一天的三种可能状态**：

| 状态 | 含义 |
|------|------|
| `hold[i]`   | 第 `i` 天结束时，手里**持有**一支股票 |
| `sold[i]`   | 第 `i` 天结束时，**刚卖出**股票（此时进入冷却） |
| `rest[i]`   | 第 `i` 天结束时，**既没有持有也没有卖出**，即处于“休息”状态 |

这三个状态互相转移如下（`price = prices[i]`）：

1. **持有** (`hold[i]`)  
   - 昨天已经持有，今天什么都不做 → `hold[i-1]`  
   - 昨天是休息状态，今天买入 → `rest[i-1] - price`  
   - 取两者最大：`hold[i] = max(hold[i-1], rest[i-1] - price)`

2. **卖出** (`sold[i]`)  
   - 必须在昨天持有，今天卖出 → `hold[i-1] + price`  
   - 没有其他来源：`sold[i] = hold[i-1] + price`

3. **休息** (`rest[i]`)  
   - 昨天是休息，今天继续休息 → `rest[i-1]`  
   - 昨天刚卖出，今天进入冷却 → `sold[i-1]`  
   - 两者取最大：`rest[i] = max(rest[i-1], sold[i-1])`

**答案**是最后一天的最大利润，即 `max(sold[n-1], rest[n-1])`（因为持有股票意味着还没有把钱变成利润）。

> **类比**：把这三种状态想成三条道路，每天你只能站在其中一条上。根据前一天所在的道路，今天可以换到哪条道路都有明确的规则。我们只需要记录每条道路的“最高海拔”（最大利润），不必记住所有走过的细节。

**空间优化**：上面的转移只依赖 `i-1` 的状态，所以可以用 **滚动变量** 把空间压到 `O(1)`。

#### 代码（Python）

```python
def maxProfit(prices):
    """
    动态规划，时间 O(n)，空间 O(1)
    """
    if not prices:
        return 0

    n = len(prices)
    # 初始化第一天的三种状态
    hold = -prices[0]          # 第 0 天买入
    sold = 0                   # 不可能在第 0 天卖出
    rest = 0                   # 第 0 天什么也不做

    for i in range(1, n):
        price = prices[i]

        # 保存上一次的值，后面计算需要用到旧的 hold、sold、rest
        prev_hold, prev_sold, prev_rest = hold, sold, rest

        # 持有：昨天持有或昨天休息今天买入
        hold = max(prev_hold, prev_rest - price)

        # 卖出：昨天持有今天卖出
        sold = prev_hold + price

        # 休息：昨天休息或昨天卖出进入冷却
        rest = max(prev_rest, prev_sold)

    # 最终利润不能是持有状态，因为还没兑现
    return max(sold, rest)
```

> 关键行中文注释已在代码里，帮助你快速定位每一步的意义。

#### 复杂度

- **时间复杂度**：`O(n)`，只遍历一次数组，每天做常数次算术比较。  
- **空间复杂度**：`O(1)`，只用固定的 3~4 个变量保存前一天的状态。

> 与暴力解相比，时间从指数级下降到线性级，几乎可以在几毫秒内解决 `n = 5000` 的最大输入。

---

## 心得

- **核心技巧**：**状态机式动态规划**（将问题拆成若干互相转移的状态）。  
- **适用题型**：  
  1. “买卖股票”系列带有冷却、手续费或最多交易次数限制的题目。  
  2. “最长子序列”或“子数组最大和”中需要考虑前后状态转移的场景。  
  3. “爬楼梯”“跳棋”类需要记忆前几步状态的 DP。  
- **一句话总结**：把“买/卖/冷却”抽象成**三条状态线**，只记录每条线的最高收益即可。

---

## 反思

- **第一反应**：直接想枚举所有买卖组合，写递归或回溯。  
- **最容易踩的坑**：  
  - 忘记 **冷却** 的限制，导致出现相邻两天买卖的非法序列。  
  - 在 DP 中把“持有”状态写成 `max(hold[i-1], sold[i-1] - price)`，实际上只能从 **休息** 状态买入。  
  - 结果返回时误把 `hold[n-1]` 当作答案，导致多算了一把未卖出的股票价值。  
- **下次思路**：一看到“只能在卖出后休息一天”这类**状态约束**，立刻把问题抽象成**有限状态机**，列出所有合法状态并写出转移方程。这样往往能直接得到 O(n) 的 DP 解。