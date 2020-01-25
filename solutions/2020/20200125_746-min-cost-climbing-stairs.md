# #746. **最小花费爬楼梯** / Min Cost Climbing Stairs

> 难度：简单 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/min-cost-climbing-stairs/)

---

## 题目（英文原版）

**Description**

You are given an integer array cost where cost[i] is the cost of ith step on a staircase. Once you pay the cost, you can either climb one or two steps.
You can either start from the step with index 0, or the step with index 1.
Return the minimum cost to reach the top of the floor.

**Examples**

**Example 1:**

```
Input: cost = [10,15,20]
Output: 15
Explanation: You will start at index 1.
- Pay 15 and climb two steps to reach the top.
The total cost is 15.
```

**Example 2:**

```
Input: cost = [1,100,1,1,1,100,1,1,100,1]
Output: 6
Explanation: You will start at index 0.
- Pay 1 and climb two steps to reach index 2.
- Pay 1 and climb two steps to reach index 4.
- Pay 1 and climb two steps to reach index 6.
- Pay 1 and climb one step to reach index 7.
- Pay 1 and climb two steps to reach index 9.
- Pay 1 and climb one step to reach the top.
The total cost is 6.
```

**Constraints**

- 2 <= cost.length <= 1000
- 0 <= cost[i] <= 999

---

## 题目（中文翻译）

给定一个整数数组（array）`cost`，其中 `cost[i]` 表示楼梯第 *i* 步的花费。支付该费用后，你可以向上爬一步或两步。  
你可以从下标为 `0` 的步或下标为 `1` 的步开始。  
返回到达楼顶的最小花费。

**示例 1**  
```
Input: cost = [10,15,20]
Output: 15
```
**解释**：你将从下标 `1` 开始。  
- 支付 `15` 并爬两步直接到达楼顶。  
总花费为 `15`。

**示例 2**  
```
Input: cost = [1,100,1,1,1,100,1,1,100,1]
Output: 6
```
**解释**：你将从下标 `0` 开始。  
- 支付 `1` 并爬两步到达下标 `2`。  
- 支付 `1` 并爬两步到达下标 `4`。  
- 支付 `1` 并爬两步到达下标 `6`。  
- 支付 `1` 并爬一步到达下标 `7`。  
- 支付 `1` 并爬两步到达下标 `9`。  
- 支付 `1` 并爬一步到达楼顶。  
总花费为 `6`。

**约束条件**  
- `2 <= cost.length <= 1000`  
- `0 <= cost[i] <= 999`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把所有可能的上楼方式枚举出来，计算每条路径的花费，最后取最小值。  
- **数据结构**：我们可以用递归来模拟“从第 i 步出发，到达顶层的所有可能路径”。递归的调用栈类似于我们手里的一本“路线本”，每一次递归就相当于在本子上写下当前的选择（往上走 1 步还是 2 步）。  
- **正确性**：因为题目只允许一次走 1 步或 2 步，递归会把所有合法的走法都遍历一遍，所以必然能找到最小花费。  

#### 代码（Python）

```python
from functools import lru_cache

def minCostClimbingStairs_bruteforce(cost):
    n = len(cost)

    @lru_cache(maxsize=None)          # 记忆化，防止重复计算（纯暴力的话可以去掉）
    def dfs(i: int) -> int:
        """
        从第 i 步出发，爬到楼顶（下标 n）的最小花费。
        """
        # 已经到达或超过楼顶，说明不需要再付费
        if i >= n:
            return 0
        # 走一步或走两步，两种选择取费用更小的那条路
        cost_one = dfs(i + 1)
        cost_two = dfs(i + 2)
        return cost[i] + min(cost_one, cost_two)

    # 题目允许从第 0 步或第 1 步开始
    return min(dfs(0), dfs(1))
```

#### 复杂度  

- **时间复杂度**：`O(2^n)`（指数级）。因为每一步都有两种选择，递归树的节点数近似 `2^n`，所以会非常慢。  
- **空间复杂度**：`O(n)`，递归调用栈的最大深度等于楼梯的步数 `n`。

> **大白话**：如果楼梯有 30 步，`2^30 ≈ 10⁹`，相当于要算十亿次，电脑根本跑不完。  

---

### 2. 最优解

#### 思路  
从暴力解可以看到，**大量的重复计算是性能瓶颈**。  
- 例如，求 `dfs(0)` 时会计算 `dfs(2)`，而求 `dfs(1)` 时也会再次计算 `dfs(2)`，这是一种“子问题重复出现”的典型情况。  
- 动态规划（Dynamic Programming，简称 DP）正是用来 **把子问题的答案保存下来，后面再用时直接取**，从而把指数级的时间降到线性级。

**核心概念**：  
- **状态**：`dp[i]` 表示“从第 `i` 步出发，到达楼顶的最小花费”。  
- **状态转移**：从第 `i` 步只能往上走 1 步或 2 步，所以  
  \[
  dp[i] = cost[i] + \min(dp[i+1], dp[i+2])
  \]  
- **边界**：楼顶的下标是 `n`（长度），到达楼顶不需要再付费，设 `dp[n] = 0`，同理 `dp[n+1] = 0`（为了方便写 `i+2` 时不越界）。  
- **答案**：因为可以从第 0 步或第 1 步开始，最终答案是 `min(dp[0], dp[1])`。

**实现方式**  
- **自底向上**：从后往前填表，时间 `O(n)`，空间 `O(n)`。  
- **空间优化**：因为每次只用到 `dp[i+1]` 与 `dp[i+2]`，可以只保留两个变量，空间降到 `O(1)`。

下面先给出完整的 `O(n)` 表格版实现，再给出 `O(1)` 空间优化版。

#### 代码（Python）

```python
def minCostClimbingStairs_dp(cost):
    """
    动态规划（自底向上）求最小花费，时间 O(n)，空间 O(n)
    """
    n = len(cost)
    dp = [0] * (n + 1)          # dp[n] 已经是 0，表示到达顶层不再付费
    # 从倒数第二步开始往前算
    for i in range(n - 1, -1, -1):
        # dp[i] = 本步的费用 + 走一步或两步中花费更少的那条路
        dp[i] = cost[i] + min(dp[i + 1], dp[i + 2])
    # 题目允许从第 0 步或第 1 步开始
    return min(dp[0], dp[1])
```

```python
def minCostClimbingStairs_optimized(cost):
    """
    空间优化版，只用两个变量，时间 O(n)，空间 O(1)
    """
    n = len(cost)
    # next1 = dp[i+1]，next2 = dp[i+2]，初始化为 dp[n] 和 dp[n+1]，都等于 0
    next1, next2 = 0, 0
    # 逆序遍历
    for i in range(n - 1, -1, -1):
        cur = cost[i] + min(next1, next2)  # dp[i] 的值
        # 向前移动：原来的 next1 变成 next2，cur 成为新的 next1
        next2, next1 = next1, cur
    # 最后返回 min(dp[0], dp[1])，此时 next1 = dp[0]，next2 = dp[1]
    return min(next1, next2)
```

#### 复杂度  

- **时间复杂度**：`O(n)`——只遍历一次数组，线性时间。  
- **空间复杂度**：  
  - 表格版：`O(n)` 用来存 `dp` 数组。  
  - 优化版：`O(1)` 只用常数个变量。  

> 与暴力 `O(2^n)` 相比，`O(n)` 就像把“走遍所有可能的路线”改成“一步步记住最小的花费”，快得多。

---

## 心得

- **核心技巧**：**动态规划**——把“大问题”拆成“子问题”，并把子问题的答案缓存起来。  
- **适用的题型**  
  1. 爬楼梯类（如 *Climbing Stairs*、*Min Cost Climbing Stairs*）  
  2. 背包/路径最小费用类（如 *House Robber*、*Maximum Subarray*）  
  3. 计数类 DP（如 *Unique Paths*、*Decode Ways*）  
- **一句话总结解题钥匙**：**把每一步的最优解记录下来，后面的决定只需要看最近的几个记录**。

---

## 反思

- **第一反应**：看到“每一步可以走 1 或 2 步”，自然想到递归/回溯去穷举所有走法。  
- **最容易踩的坑**  
  - **越界**：在写 `dp[i+2]` 时，需要确保 `dp` 数组的长度至少是 `n+2`，或在代码里手动处理 `i+2` 超出范围的情况。  
  - **起点选择**：题目允许从第 0 步或第 1 步开始，答案是 `min(dp[0], dp[1])`，不要忘记取最小值。  
  - **空间优化的变量顺序**：更新 `next1`、`next2` 时顺序错误会导致使用了已经被覆盖的值。  
- **下次遇到同类题的第一步**：先判断“是否有重叠子问题”，如果有，就立刻考虑 **动态规划**（先写出状态 `dp[i]`，再写转移方程）。