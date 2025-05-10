# #3180. 使用操作 I 的最大总奖励 / Maximum Total Reward Using Operations I

> 难度：中等 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/maximum-total-reward-using-operations-i/)

---

## 题目（英文原版）

**Description**

You are given an integer array rewardValues of length n, representing the values of rewards.
Initially, your total reward x is 0, and all indices are unmarked. You are allowed to perform the following operation any number of times:
Return an integer denoting the maximum total reward you can collect by performing the operations optimally.

**Examples**

**Example 1:**

```
Input: rewardValues = [1,1,3,3]
Output: 4
Explanation:
During the operations, we can choose to mark the indices 0 and 2 in order, and the total reward will be 4, which is the maximum.
```

**Example 2:**

```
Input: rewardValues = [1,6,4,3,2]
Output: 11
Explanation:
Mark the indices 0, 2, and 1 in order. The total reward will then be 11, which is the maximum.
```

**Constraints**

- 1 <= rewardValues.length <= 2000
- 1 <= rewardValues[i] <= 2000

---

## 题目（中文翻译）

你得到一个长度为 `n` 的整数数组（integer array）`rewardValues`，表示奖励的数值。  
最初，你的总奖励 `x` 为 0，且所有下标均为未标记（unmarked）。  
你可以任意次数地执行以下操作：  

请返回一个整数，表示在最优执行这些操作的情况下，你能够收集的最大总奖励（maximum total reward）。

**示例 1**  
Input: `rewardValues = [1,1,3,3]`  
Output: `4`  
Explanation:  
在操作过程中，我们可以按顺序标记下标 `0` 和 `2`，总奖励为 `4`，这是能够得到的最大值。

**示例 2**  
Input: `rewardValues = [1,6,4,3,2]`  
Output: `11`  
Explanation:  
按顺序标记下标 `0`、`2`、`1`，总奖励随后为 `11`，这是能够得到的最大值。

**约束条件**  
- `1 <= rewardValues.length <= 2000`  
- `1 <= rewardValues[i] <= 2000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题的核心规则是：

1. 初始总奖励 `x = 0`，所有下标均未标记。  
2. 任选一个未标记的下标 `i`，如果 **当前的总奖励 `x` 小于 `rewardValues[i]`**，就可以把它标记并把 `rewardValues[i]` 加到 `x` 上。  
3. 只要还有满足条件的下标，就可以继续操作，目标是让最终的 `x` 尽可能大。

> **生活化类比**：想象你在玩“先买后吃”的游戏。每件商品都有一个价钱 `rewardValues[i]`，你只能在手里拥有的钱 **少于** 商品价钱时才可以买它。买下后，你的现金会立刻增加商品的价钱（相当于把商品的价值拿来“卖”了）。想赚到最多的钱，就要挑选合适的购买顺序。

最直接的想法是 **枚举所有可能的操作顺序**，看哪一种能得到最大的总奖励。

- 先把数组 `rewardValues` 按任意顺序排列（不必排序），  
- 用深度优先搜索（DFS）模拟每一步的选择：  
  - 当前总奖励 `cur`。遍历所有未标记的下标 `i`，如果 `cur < rewardValues[i]`，就递归进入「标记 `i` 并把 `rewardValues[i]` 加到 `cur`」的状态。  
- 所有递归结束后，记录下出现的最大 `cur`。

**为什么这个方法一定能得到答案**：因为它尝试了 **所有** 合法的标记顺序，必然包含最优顺序。

**时间/空间复杂度**  
- 对 `n` 个元素，每一步都有至多 `n` 种选择，递归深度最多 `n`，因此最坏情况的时间复杂度是 **O(n!)**（阶乘级），随 `n` 的增长爆炸。  
- 递归栈最多保存 `n` 层状态，空间复杂度是 **O(n)**。

> 大白话解释：`O(n!)` 就像把 5 本书排成一排，有 `5! = 120` 种排法；当 `n=10` 时，排法已经是 `3,628,800`，几乎不可能在电脑上跑完。

#### 代码（Python）

```python
from typing import List

def maxReward_bruteforce(rewardValues: List[int]) -> int:
    n = len(rewardValues)
    used = [False] * n          # 标记哪些下标已经被取走
    ans = 0                     # 记录全局最大奖励

    def dfs(cur: int):
        """cur 为当前累计的奖励"""
        nonlocal ans
        ans = max(ans, cur)     # 更新答案

        for i in range(n):
            # 只有在当前奖励小于 rewardValues[i] 且 i 还未被使用时才能取
            if not used[i] and cur < rewardValues[i]:
                used[i] = True               # 标记 i
                dfs(cur + rewardValues[i])   # 递归进入新状态
                used[i] = False              # 回溯，恢复现场

    dfs(0)   # 从 0 开始尝试所有可能的操作顺序
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n!)` —— 需要遍历所有可能的取舍顺序，随着 `n` 增大非常慢。  
- **空间复杂度**：`O(n)` —— 递归栈深度最多 `n`，以及一个长度为 `n` 的布尔数组 `used`。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **枚举顺序**。仔细观察题目规则会发现：

1. **只要当前总奖励小于某个奖励值，就可以取它**。  
2. **取完后，总奖励会立刻变成更大的值**，这只会让后面的取值条件更宽松（因为 `cur` 只会增大）。  
3. 因此，如果我们把奖励数组 **从小到大排序**，**总是按照这个顺序来考虑是否取**，就不会错过任何最优解。  
   - 设 `a1 ≤ a2 ≤ … ≤ an` 为排序后的数组。若在某一步我们决定取 `ak`，那么之前的所有已取奖励之和必然 **小于 `ak`**（否则 `ak` 不满足取的条件）。这恰好是我们在 DP 中需要的约束。

基于排序后的顺序，我们可以把问题转化为 **“背包”**：  
- 每个奖励 `ai` 要么取，要么不取。  
- 取 `ai` 的前提是：**取之前的总和 `s` 必须小于 `ai`**。  
- 目标是让最终的总和 `s` 尽可能大。

这正好可以用 **状态压缩的布尔 DP** 来描述：

- `dp[j] = True` 表示 **在考虑前面若干个奖励后，能恰好得到总奖励 `j`**。  
- 初始时 `dp[0] = True`（什么都不取，奖励为 0）。

遍历排序后的每个奖励 `val`，我们尝试把它加入已有的可达和 `j` 中。要保证合法性，需要满足 `j < val`（因为在取 `val` 之前的总和 `j` 必须小于 `val`）。于是转移式为：

```
if dp[j] 为 True 且 j < val:
    dp[j + val] = True          # 把 val 加进去，得到新的和
```

注意：**从大到小遍历 `j`**，防止同一次循环中把同一个 `val` 用多次。

遍历完所有奖励后，最大的 `j` 且 `dp[j] == True` 就是答案。

**时间复杂度分析**  
- `val` 的最大可能值是 `2000`，`n ≤ 2000`，所以最大总和不超过 `2000 * 2000 = 4,000,000`。  
- 我们的 DP 只遍历一次 `val`，每次遍历所有可能的 `j`（最多到当前累计的最大和），总体时间是 `O(n * S)`，其中 `S` 为所有奖励的和。对于本题的约束，这大约是 `8×10^6` 次操作，完全可以接受。  
- 空间只需要一个长度为 `S+1` 的布尔数组，`O(S)`。

> 与暴力解对比：从 **指数级** 降到了 **线性乘以和**，速度提升了好几个数量级。

#### 代码（Python）

```python
from typing import List

def maxReward_dp(rewardValues: List[int]) -> int:
    # 1. 先排序，保证后面按顺序考虑时一定是从小到大
    rewardValues.sort()
    
    total_sum = sum(rewardValues)           # 所有奖励的和，决定 DP 数组的长度
    dp = [False] * (total_sum + 1)
    dp[0] = True                            # 0 总是可以达到（什么都不取）

    max_reach = 0                           # 当前已知的最大可达总和
    for val in rewardValues:                # 依次处理每个奖励
        # 必须从大到小遍历，防止在同一次循环中重复使用同一个 val
        for cur in range(max_reach, -1, -1):
            if dp[cur] and cur < val:       # 只有在 cur < val 时才能取当前奖励
                dp[cur + val] = True        # 把 val 加进去，得到新的总和
        max_reach += val                    # 更新已遍历的最大可能和

    # 找到最大的 j，使得 dp[j] 为 True
    for ans in range(total_sum, -1, -1):
        if dp[ans]:
            return ans
    return 0  # 理论上不会到这里
```

#### 复杂度

- **时间复杂度**：`O(n * S)`，其中 `S = sum(rewardValues)`（最坏约 4·10⁶），相当于“线性乘以总和”。比暴力的 `O(n!)` 快很多。  
- **空间复杂度**：`O(S)`，只需要一个布尔数组保存所有可能的总和。

---

## 心得

- **核心技巧**：**排序 + 受限的背包 DP**。先把奖励从小到大排列，利用“取之前的总和必须小于当前奖励”这一约束，在 DP 中只在满足 `j < val` 时才转移。  
- **适用的题型**：  
  1. “只能在满足某个阈值条件时才能选择元素” 的背包类问题（例如 LeetCode 2611 “Mice and Cheese” 的变体）。  
  2. “先手必须比后手小” 的序列选择题（比如 “Maximum Score From Performing Multiplication Operations”）。  
  3. “先挑小的再挑大的” 能保证最优的贪心+DP 组合（如 “Partition Array Into Two Subsets With Minimum Difference” 的特殊形式）。  
- **一句话总结解题钥匙**：**先排序，使约束只依赖于“当前总和 < 当前元素”，再用受限背包 DP 记录所有可达的总和**。

---

## 反思

- **第一反应**：看到“只能在当前奖励小于下一个奖励时才能取”，立刻想到“先把数组排好序，再按顺序挑选”。  
- **最容易踩的坑**：  
  - **忘记排序**：如果不排序，DP 的转移条件 `j < val` 可能不再成立，导致错误的可达状态。  
  - **DP 更新顺序错误**：必须从大到小遍历 `j`，否则同一次循环会把同一个奖励使用多次（相当于无限背包）。  
  - **边界条件**：`j = 0` 必须初始化为 `True`，否则无法开始取第一个奖励。  
- **下次类似题目第一步**：**先检查是否可以通过排序把约束“前后关系”固定下来**，如果可以，就把问题转化为“受限背包/子集和” 再做 DP。