# #518. 零钱兑换 II / Coin Change II

> 难度：中等 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/coin-change-ii/)

---

## 题目（英文原版）

**Description**

You are given an integer array coins representing coins of different denominations and an integer amount representing a total amount of money.
Return the number of combinations that make up that amount. If that amount of money cannot be made up by any combination of the coins, return 0.
You may assume that you have an infinite number of each kind of coin.
The answer is guaranteed to fit into a signed 32-bit integer.

**Examples**

**Example 1:**

```
Input: amount = 5, coins = [1,2,5]
Output: 4
Explanation: there are four ways to make up the amount:
5=5
5=2+2+1
5=2+1+1+1
5=1+1+1+1+1
```

**Example 2:**

```
Input: amount = 3, coins = [2]
Output: 0
Explanation: the amount of 3 cannot be made up just with coins of 2.
```

**Example 3:**

```
Input: amount = 10, coins = [10]
Output: 1
```

**Constraints**

- 1 <= coins.length <= 300
- 1 <= coins[i] <= 5000
- All the values of coins are unique.
- 0 <= amount <= 5000

---

## 题目（中文翻译）

给定一个整数数组 `coins`（integer array），其中每个元素表示一种不同面额的硬币，以及一个整数 `amount`，表示需要凑成的总金额。  
返回恰好凑出该金额的组合数。如果无法通过任意组合得到该金额，返回 `0`。  
你可以假设每种硬币的数量是无限的。  
答案保证能够放入有符号 32 位整数中。

**示例 1**  
**输入**: `amount = 5, coins = [1,2,5]`  
**输出**: `4`  
**解释**: 有四种方式可以凑成目标金额：  
- `5 = 5`  
- `5 = 2 + 2 + 1`  
- `5 = 2 + 1 + 1 + 1`  
- `5 = 1 + 1 + 1 + 1 + 1`

**示例 2**  
**输入**: `amount = 3, coins = [2]`  
**输出**: `0`  
**解释**: 只能使用面额为 `2` 的硬币，无法凑出金额 `3`。

**示例 3**  
**输入**: `amount = 10, coins = [10]`  
**输出**: `1`  

**约束条件**  
- `1 <= coins.length <= 300`  
- `1 <= coins[i] <= 5000`  
- `coins` 中的所有值互不相同。  
- `0 <= amount <= 5000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的硬币组合**，看哪些组合的总和恰好等于 `amount`，把符合条件的组合计数。  
可以把每一种硬币看成一种“字母”，把组合看成“一串字母”。我们要找所有长度不固定、字母可以重复使用且字母对应的数值之和等于 `amount` 的字符串。

实现上常用 **回溯（深度优先搜索）**：

1. 从第一种硬币开始尝试  
2. 每次可以**选择**当前硬币（把它加入当前组合），或**跳过**当前硬币直接尝试下一种硬币  
3. 当累计的金额正好等于 `amount` 时，找到一种合法组合，计数 +1  
4. 累计金额超过 `amount` 或遍历完所有硬币则结束当前分支

> **为什么正确？**  
> 回溯会遍历所有可能的选取方式（包括每种硬币出现 0、1、2 … 次的情况），只要一种选取方式的总和等于目标金额，就算作一种合法组合。没有遗漏，也没有重复计数。

> **时间/空间复杂度**  
> - 每个硬币可以出现 `0~amount/coin` 次，搜索树的分支数随 `amount` 指数级增长。最坏情况下时间复杂度约为 `O(2^n)`（`n` 为硬币种类数）或者更粗糙地说 **指数级**。  
> - 递归调用栈的深度最多为 `amount`（全部用最小面值的硬币），所以空间复杂度是 `O(amount)`。

> **大白话解释**  
> `O(2^n)` 就像翻硬币的每一种“要不要拿”，每个硬币都有两种决定，全部决定下来就有 `2` 的 `n` 次方种可能。`O(amount)` 的空间相当于你在纸上记下最多 `amount` 张纸币的堆叠深度。

#### 代码（Python）

```python
from typing import List

def change_bruteforce(amount: int, coins: List[int]) -> int:
    """
    暴力回溯求组合数
    """
    # 为了避免计数时出现顺序不同却是同一种组合的情况，
    # 我们在递归时只允许使用「当前及之后」的硬币。
    n = len(coins)

    def dfs(idx: int, cur_sum: int) -> int:
        # idx: 正在考虑的硬币在 coins 中的下标
        # cur_sum: 已经凑好的金额
        if cur_sum == amount:          # 正好凑满，算作一种合法组合
            return 1
        if cur_sum > amount or idx == n:  # 超额或没有硬币可选，结束本分支
            return 0

        # 方式一：使用当前硬币（可以多次使用，所以仍然是 idx）
        use_it = dfs(idx, cur_sum + coins[idx])
        # 方式二：跳过当前硬币，尝试下一种硬币
        skip_it = dfs(idx + 1, cur_sum)

        return use_it + skip_it

    return dfs(0, 0)
```

#### 复杂度

- **时间复杂度**：`O(2^n)`（指数级），因为每个硬币都有“取/不取”两种选择，搜索树的节点数随硬币种类数呈指数增长。  
- **空间复杂度**：`O(amount)`，递归栈的最大深度等于最多可以放入的最小硬币的数量（最坏情况下是 `amount / min(coins)`，这里用 `amount` 作上界）。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**“重复子问题”** 是导致指数时间的根本原因：  
例如在上面的递归里，`dfs(idx, cur_sum)` 可能被多次调用（不同的路径到达相同的状态），导致大量重复计算。

**动态规划（Dynamic Programming，DP）** 正是用来“记住”已经算过的子问题的技术。  
这里的子问题可以定义为：

> `dp[i][j]` = 使用前 `i` 种硬币（即 `coins[:i]`），凑成金额 `j` 的组合数。

递推公式：

- **不使用第 i 种硬币**：`dp[i-1][j]`（只用前 `i-1` 种硬币凑 `j`）  
- **使用第 i 种硬币**：如果 `j >= coins[i-1]`，则可以在已经凑出 `j - coins[i-1]` 的基础上再加一个第 i 种硬币，组合数是 `dp[i][j - coins[i-1]]`（注意这里仍然是 `i`，因为同一种硬币可以无限次使用）

于是：

```
dp[i][j] = dp[i-1][j] + dp[i][j - coins[i-1]]   (j >= coins[i-1])
dp[i][j] = dp[i-1][j]                          (j <  coins[i-1])
```

**初始条件**：

- `dp[0][0] = 1`：0 种硬币凑成金额 0，只有一种空组合。  
- `dp[0][j>0] = 0`：0 种硬币不可能凑出正数金额。

**空间优化**  
观察公式只依赖 **当前行** (`dp[i][*]`) 和 **上一行** (`dp[i-1][*]`)。如果把行的遍历顺序改为 **硬币外层、金额内层**，并且使用一维数组 `dp[j]` 表示 “使用已遍历过的硬币凑成金额 j 的组合数”，则：

```
for coin in coins:
    for j from coin to amount:
        dp[j] += dp[j - coin]
```

这里 `dp[j]` 原本已经保存了 “不使用当前硬币” 的情况，`dp[j - coin]` 保存了 “使用当前硬币一次后，其余金额的组合数”。这样只需要 `O(amount)` 的额外空间。

> **类比**：把 `dp` 想象成一本“零钱账本”。每当我们拿到一种新硬币，就在账本里从左到右更新：把 “把这枚硬币加入之前能凑到的金额” 的记录累加进去，账本最终的第 `amount` 行就是答案。

#### 代码（Python）

```python
from typing import List

def change_dp(amount: int, coins: List[int]) -> int:
    """
    动态规划（空间优化为一维数组）求组合数
    """
    # dp[j] 表示「使用已经遍历过的硬币」凑成金额 j 的方案数
    dp = [0] * (amount + 1)
    dp[0] = 1                      # 凑成 0 元只有一种方式：不选硬币

    for coin in coins:             # 逐个硬币“放进账本”
        # 从 coin 开始向右遍历，保证每次使用的都是“已经包含当前硬币”的状态
        for j in range(coin, amount + 1):
            dp[j] += dp[j - coin]  # 把「把当前硬币加入」的方案数加进来

    return dp[amount]
```

#### 复杂度

- **时间复杂度**：`O(N * amount)`，其中 `N = len(coins)`。我们遍历每枚硬币一次，并对每枚硬币遍历一次 `0~amount` 的金额区间。  
  > 与暴力的指数级相比，这里是 **线性乘积**，实际运行非常快（最多约 `300 * 5000 = 1.5e6` 次循环）。

- **空间复杂度**：`O(amount)`，只用一个长度为 `amount + 1` 的一维数组。  
  > 与二维 DP `O(N * amount)` 的空间相比，省去了 `N` 倍的开销。

---

## 心得

- 这道题的核心技巧是 **“背包型动态规划 + 空间压缩”**（即“完全背包”问题）。  
- 该技巧常用于**计数类背包**题目，例如  
  1. **组合总和（Combination Sum）**  
  2. **分割整数（Integer Break）** 中的计数变体  
  3. **不同路径 II（Unique Paths II）** 的计数版本（把障碍视为不可使用的硬币）  

- **一句话总结解题钥匙**：把“每种硬币可以无限次使用”转化为 **“对每枚硬币遍历一次，内部从小额到大额累加方案数”**。

---

## 反思

- **第一反应**：直接写递归/回溯去枚举所有组合，觉得能写出来就能通过。  
- **最容易踩的坑**  
  1. **重复计数**：如果在回溯时不限制硬币的使用顺序（比如先取 2 再取 1），会把同一种组合算多次。  
  2. **边界条件**：`amount = 0` 时答案应该是 1（空组合），而不是 0。  
  3. **整数溢出**：虽然题目保证 32 位整数足够，但在某些语言里需要使用更大的类型防止溢出。  
- **下次遇到同类题的第一步**：先判断“是否是背包计数问题”，如果是，立刻写出状态 `dp[i][j]`（或一维压缩）并推导转移方程，而不是直接写暴力递归。这样可以把搜索空间从指数级压缩到多项式级。