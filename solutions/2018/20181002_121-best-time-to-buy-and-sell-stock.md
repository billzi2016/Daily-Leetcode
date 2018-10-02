# #121. 买卖股票的最佳时机 / Best Time to Buy and Sell Stock

> 难度：简单 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)

---

## 题目（英文原版）

**Description**

You are given an array prices where prices[i] is the price of a given stock on the ith day.
You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.
Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.

**Examples**

**Example 1:**

```
Input: prices = [7,1,5,3,6,4]
Output: 5
Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.
Note that buying on day 2 and selling on day 1 is not allowed because you must buy before you sell.
```

**Example 2:**

```
Input: prices = [7,6,4,3,1]
Output: 0
Explanation: In this case, no transactions are done and the max profit = 0.
```

**Constraints**

- 1 <= prices.length <= 105
- 0 <= prices[i] <= 104

---

## 题目（中文翻译）

你得到一个数组 **prices**，其中 `prices[i]` 表示第 *i* 天的股票价格。  
你希望通过选择**一天**买入一股股票，并在**未来的某一天**卖出该股票，以获得最大的利润。  
返回一次交易能够实现的**最大利润**。如果无法获得任何利润，返回 `0`。

**示例 1**  
**输入**: `prices = [7,1,5,3,6,4]`  
**输出**: `5`  
**解释**: 在第 2 天（价格 = 1）买入，第 5 天（价格 = 6）卖出，利润 = 6‑1 = 5。  
注意，不能在第 2 天买入后再在第 1 天卖出，因为必须先买后卖。

**示例 2**  
**输入**: `prices = [7,6,4,3,1]`  
**输出**: `0`  
**解释**: 在这种情况下不进行任何交易，最大利润为 0。

**约束条件**  
- `1 <= prices.length <= 10^5`  
- `0 <= prices[i] <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法就是把每一天当作**买入日**，然后把它之后的每一天都当作**卖出日**，算出这两天的利润，取所有可能利润的最大值。  
- **数据结构**：只需要用到原始的 `prices` 数组，和两个临时变量 `max_profit`、`profit` 来记录最大利润和当前利润。  
- **为什么正确**：因为题目要求「买入在前，卖出在后」的所有合法组合中利润最大，遍历所有合法组合自然能找到最优解。  
- **时间/空间复杂度**：我们会用两层循环，外层遍历 `i`（买入日），内层遍历 `j`（卖出日，`j > i`），所以总共要检查大约 `n·(n‑1)/2` 种组合，时间复杂度是 **O(n²)**。空间上只用了常数个额外变量，**O(1)**。

> **大白话解释**：  
> - `O(n²)` 可以想象成「如果有 100 天，要检查 100×99/2≈5,000 对买卖组合」，随着天数增多，检查的次数会像正方形一样快速增长。  
> - `O(1)` 表示不管天数多少，额外占用的记忆几乎不变，就像我们只准备了一支笔和一张纸来记下最大利润。

#### 代码（Python）

```python
def maxProfit_brute(prices):
    """
    暴力解法：遍历所有买入-卖出组合，找出最大利润
    """
    n = len(prices)
    max_profit = 0                     # 记录迄今为止的最大利润，初始为 0（不交易也可以）

    for i in range(n):                # i 为买入的那一天
        for j in range(i + 1, n):      # j 必须在 i 之后，才能卖出
            profit = prices[j] - prices[i]   # 当天卖出减去买入的差额
            if profit > max_profit:           # 只保留更大的利润
                max_profit = profit

    return max_profit
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 需要两层循环，检查所有 `i < j` 的组合。  
- **空间复杂度**：`O(1)` —— 只用了几个额外的整数变量。

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在于**重复比较**：当我们已经知道某天之前的最低买入价时，后面的每一天只需要和这个最低价比较一次，就能得到以当天为卖出日的最大利润。于是我们可以把「遍历所有买入日」这一步省掉，改为一次遍历，同时维护两个变量：

1. `min_price`：截至当前天（包括今天）为止，出现过的最低股价。相当于「到现在为止，最便宜的买入机会」。
2. `max_profit`：截至当前天，能够得到的最大利润。每天的潜在利润 = `prices[i] - min_price`，如果比 `max_profit` 大就更新。

这就是**一次遍历**（单指针）即可完成的思路，常被称为「动态规划的状态压缩」——我们只需要记录「到目前为止的最优子状态」即可。

> **类比**：把 `min_price` 想象成「水井里最深的水位」，每天的价格就是「水位的高度」。我们只关心「最深的井口」到底在哪儿，因为卖出时只要知道最低的买入价，就能算出最高的收益。

#### 代码（Python）

```python
def maxProfit(prices):
    """
    最优解：一次遍历，实时维护最低买入价和最大利润
    """
    min_price = float('inf')   # 初始设为正无穷，保证第一个价格一定会更新
    max_profit = 0             # 初始利润为 0（不交易也可以）

    for price in prices:       # 依次遍历每一天的股价
        # 如果当前价格更低，就更新最低买入价
        if price < min_price:
            min_price = price
        else:
            # 否则计算以今天卖出能得到的利润
            profit = price - min_price
            # 若利润更大，则更新最大利润
            if profit > max_profit:
                max_profit = profit

    return max_profit
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历一次数组，和天数呈线性关系。比 `O(n²)` 快很多，尤其当 `n` 达到 10⁵ 时，性能提升尤为明显。  
- **空间复杂度**：`O(1)` —— 只用了两个额外变量 `min_price`、`max_profit`，不随输入规模增长。

---

## 心得

- **核心技巧**：维护「截至当前位置的最优子状态」——这里是「最低买入价」和「最高利润」的实时更新。  
- **适用题型**：  
  1. 「最大子数组和」(Kadane 算法) – 维护当前子数组的最小前缀和。  
  2. 「买卖股票的最佳时机 II」 – 用类似的思路累计所有正的价格差。  
  3. 「最长递增子序列的长度」的 O(n) 版（使用单调栈）— 也是维护局部最优。  
- **一句话总结解题钥匙**：**把全局最优拆成「当前最小」+「当前最大」的组合，边遍历边更新**。

---

## 反思

- **第一反应**：直接想到「两层循环」把每一天的买入和卖出都枚举一遍。  
- **最容易踩的坑**：  
  - 忘记「只能在买入之后卖出」导致错误的 `i > j` 组合。  
  - 对全是下降的价格序列没有返回 `0`（题目要求利润为负时返回 0）。  
  - 在最优解中，如果先比较 `price < min_price` 再计算利润，可能会漏掉当天即为最低价且后面仍有更高价的情况，需要使用 `else` 或者先算利润再更新最小价。  
- **下次思考类似题**：第一步先问自己「有没有可以在一次遍历中维护的‘历史最值’（最小/最大）”，如果有，就尝试把暴力的双循环压缩成单指针的线性扫描。