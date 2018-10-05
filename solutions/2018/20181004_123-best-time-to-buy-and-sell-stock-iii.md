# #123. 买卖股票的最佳时机 III / Best Time to Buy and Sell Stock III

> 难度：困难 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/)

---

## 题目（英文原版）

**Description**

You are given an array prices where prices[i] is the price of a given stock on the ith day.
Find the maximum profit you can achieve. You may complete at most two transactions.
Note: You may not engage in multiple transactions simultaneously (i.e., you must sell the stock before you buy again).

**Examples**

**Example 1:**

```
Input: prices = [3,3,5,0,0,3,1,4]
Output: 6
Explanation: Buy on day 4 (price = 0) and sell on day 6 (price = 3), profit = 3-0 = 3.
Then buy on day 7 (price = 1) and sell on day 8 (price = 4), profit = 4-1 = 3.
```

**Example 2:**

```
Input: prices = [1,2,3,4,5]
Output: 4
Explanation: Buy on day 1 (price = 1) and sell on day 5 (price = 5), profit = 5-1 = 4.
Note that you cannot buy on day 1, buy on day 2 and sell them later, as you are engaging multiple transactions at the same time. You must sell before buying again.
```

**Example 3:**

```
Input: prices = [7,6,4,3,1]
Output: 0
Explanation: In this case, no transaction is done, i.e. max profit = 0.
```

**Constraints**

- 1 <= prices.length <= 105
- 0 <= prices[i] <= 105

---

## 题目（中文翻译）

你得到一个数组 `prices`，其中 `prices[i]` 表示第 `i` 天的股票价格。  
求在最多完成 **两笔交易**（transaction）的前提下，你能够获得的最大利润。  
注意：不能同时进行多笔交易（即必须在再次买入前先卖出持有的股票）。

**示例 1**  
**示例 2**  
**示例 3**  
**约束条件**：

### 示例

#### 示例 1
**输入**: `prices = [3,3,5,0,0,3,1,4]`  
**输出**: `6`  
**解释**: 第 4 天买入（价格 = 0），第 6 天卖出（价格 = 3），利润 = 3‑0 = 3。  
随后第 7 天买入（价格 = 1），第 8 天卖出（价格 = 4），利润 = 4‑1 = 3。

#### 示例 2
**输入**: `prices = [1,2,3,4,5]`  
**输出**: `4`  
**解释**: 第 1 天买入（价格 = 1），第 5 天卖出（价格 = 5），利润 = 5‑1 = 4。  
注意，不能在第 1 天买入后又在第 2 天再次买入再一起卖出，因为这会导致同时持有多笔交易。必须先卖出后才能再次买入。

#### 示例 3
**输入**: `prices = [7,6,4,3,1]`  
**输出**: `0`  
**解释**: 这种情况下不进行任何交易，最大利润为 0。

### 约束条件
- `1 <= prices.length <= 10^5`
- `0 <= prices[i] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把「至多两笔交易」全部列举出来，算出每一种可能的收益，然后取最大值。  
我们可以把一次买卖看成「在第 `i` 天买入，在第 `j` 天卖出」(`i < j`)。  
于是两笔交易就变成四个下标 `i < j < k < l`，分别对应「第一次买、第一次卖、第二次买、第二次卖」。

> **类比**：把每一天的价格想成一本词典的页码，买入就像在某页写下「我要买」的记号，卖出就是在后面的页码写下「我要卖」的记号。暴力解就是把所有可能的「买-卖-买-卖」组合都写下来，再挑出收益最高的那一条。

只要遍历所有合法的四元组，就能得到答案。由于我们只用了 Python 的列表 `prices` 来存放价格，其他都只需要几个循环变量，所以不需要额外的数据结构。

**为什么正确**：  
每一种合法的买卖顺序都会在枚举过程中出现，遍历完所有组合后，最大收益一定被找到了。

**时间/空间分析**（大白话）  
- 外层有四层循环，每层最坏情况下都要遍历 `n`（`prices` 的长度）次。于是总的执行次数大约是 `n × n × n × n = n⁴`，也就是 **O(n⁴)**。如果 `n=10⁵`，这根本跑不完，跟在超市里排 10⁴ 条队一样慢。  
- 只用了常数个额外变量（`max_profit`、循环下标），所以 **空间复杂度是 O(1)**，即只占很少的内存。

#### 代码（Python）

```python
def maxProfit_bruteforce(prices):
    """
    暴力枚举四个下标 i < j < k < l，分别表示
    第一次买、第一次卖、第二次买、第二次卖
    """
    n = len(prices)
    max_profit = 0                         # 记录目前找到的最大收益

    # 第一次买的下标 i
    for i in range(n):
        # 第一次卖的下标 j，必须在 i 之后
        for j in range(i + 1, n):
            profit1 = prices[j] - prices[i]   # 第一次交易的收益（可能为负）
            # 第二次买的下标 k，必须在 j 之后
            for k in range(j + 1, n):
                # 第二次卖的下标 l，必须在 k 之后
                for l in range(k + 1, n):
                    profit2 = prices[l] - prices[k]   # 第二次交易的收益
                    total = max(0, profit1) + max(0, profit2)  # 只算正收益
                    if total > max_profit:
                        max_profit = total

    return max_profit
```

#### 复杂度

- **时间复杂度**：`O(n⁴)` —— 四层循环，每层最坏遍历 `n` 次，计算次数随 `n` 的四次方增长。  
- **空间复杂度**：`O(1)` —— 只用了常数个额外变量，和输入规模无关。

---

### 2. 最优解

#### 思路  
暴力解太慢，瓶颈在于我们把所有四个下标都枚举了一遍。  
观察可以发现：**一次交易的最大收益只和「买的最低价」和「卖的最高价」有关**。如果我们能在一次遍历中把「从左到右的最佳一次交易」和「从右到左的最佳一次交易」都算出来，就能把两笔交易的组合时间压到线性。

有两种常见的线性解法，这里选取「状态机 DP」的写法，它只需要四个变量：

| 变量 | 含义 |
|------|------|
| `hold1` | 手上持有第一笔股票后的最大「净收益」（相当于「已经花了钱买进」的负数） |
| `cash1` | 完成第一笔交易后手上持有的最大「净收益」 |
| `hold2` | 在完成第一笔交易后，又买入第二笔股票后的最大「净收益」 |
| `cash2` | 完成两笔交易后手上持有的最大「净收益」——这就是答案 |

我们把「买」看成「把当前收益减去价格」；「卖」看成「把当前收益加上价格」。遍历每一天的价格时，依次更新这四个状态：

```
hold1 = max(hold1, -price)          # 第一次买：要么保持原来的买入，要么今天买入
cash1 = max(cash1, hold1 + price)   # 第一次卖：要么保持原来的收益，要么今天卖出
hold2 = max(hold2, cash1 - price)   # 第二次买：基于第一次卖后的收益再买入
cash2 = max(cash2, hold2 + price)   # 第二次卖：基于第二次买后的收益再卖出
```

每一步都只比较两种可能，取更大的那个。遍历完所有天数后，`cash2` 就是「至多两笔交易」能得到的最大利润。

> **类比**：把这四个变量想成四位小老板。  
> - 小老板 1（`hold1`）正在算「第一次买了多少钱」的负数。  
> - 小老板 2（`cash1`）算「第一次卖完手里还有多少钱」。  
> - 小老板 3（`hold2`）在第一次卖完后又买进一次，算「第二次买了多少钱」的负数。  
> - 小老板 4（`cash2`）算「两次买卖全部结束后手里剩多少钱」。  
> 每天的价格到来时，四位老板都会「重新评估」是否该买或该卖，始终保持「手里最多钱」的状态。

**时间/空间分析**（大白话）  
- 只需要一次遍历 `prices`，每个元素做常数次算术和比较，执行次数随 `n` 成线性关系，**O(n)**。  
- 只用了四个整型变量，**O(1)** 的额外空间。

#### 代码（Python）

```python
def maxProfit(prices):
    """
    DP（状态机）解法，时间 O(n)，空间 O(1)
    """
    if not prices:
        return 0

    # 初始化：买入前手里没有钱，等价于负无穷（这里用一个很小的数）
    INF_NEG = -10**9
    hold1 = INF_NEG   # 第一次买入后手里剩下的净收益（实际是负数）
    cash1 = 0         # 完成第一次交易后手里最多有多少钱
    hold2 = INF_NEG   # 第二次买入后手里剩下的净收益
    cash2 = 0         # 完成两次交易后手里最多有多少钱（答案）

    for price in prices:
        # 第一次买：要么保持之前的买入，要么今天买（-price）
        hold1 = max(hold1, -price)
        # 第一次卖：要么保持之前的收益，要么今天卖（hold1 + price）
        cash1 = max(cash1, hold1 + price)
        # 第二次买：基于第一次卖后的收益再买入
        hold2 = max(hold2, cash1 - price)
        # 第二次卖：基于第二次买后的收益再卖出
        cash2 = max(cash2, hold2 + price)

    return cash2
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历一次数组，`n` 为价格天数。比暴力的 `n⁴` 快了好几数量级。  
- **空间复杂度**：`O(1)` —— 只用了四个额外整数变量，和 `n` 无关。

---

## 心得

- **核心技巧**：把「至多 K 笔交易」抽象为「买入/卖出」的状态转移，用 DP（或状态机）一次遍历完成。  
- **适用的题型**：  
  1. *Best Time to Buy and Sell Stock*（只允许一次交易）  
  2. *Best Time to Buy and Sell Stock II*（无限次交易）  
  3. *Best Time to Buy and Sell Stock IV*（最多 K 笔交易）  
- **解题钥匙**：把每一次「买」看成「把利润减去当前价格」，每一次「卖」看成「把利润加上当前价格」，用「最大」来维护最优状态。

---

## 反思

- **第一反应**：想到枚举所有买卖区间，却没意识到枚举的次数会爆炸。  
- **最容易踩的坑**：  
  - 忘记「可以不进行任何交易」的情况，需要初始化收益为 `0` 而不是负数。  
  - 在实现状态机时，更新顺序必须严格按照 `hold1 → cash1 → hold2 → cash2`，否则会把同一天的价格用两次，导致错误。  
- **下次思路**：看到「至多两笔交易」这类限制时，第一步想到「把问题拆成左侧一次交易 + 右侧一次交易」或「用固定状态数的 DP」来压缩时间。这样可以迅速从暴力到线性转变。