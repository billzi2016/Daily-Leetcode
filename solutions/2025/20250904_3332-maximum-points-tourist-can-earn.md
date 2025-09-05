# #3332. Maximum Points Tourist Can Earn / Maximum Points Tourist Can Earn

> 难度：中等 · 标签：Array、Dynamic Programming、Matrix · [LeetCode 链接](https://leetcode.com/problems/maximum-points-tourist-can-earn/)

---

## 题目（英文原版）

**Description**

You are given two integers, n and k, along with two 2D integer arrays, stayScore and travelScore.
A tourist is visiting a country with n cities, where each city is directly connected to every other city. The tourist's journey consists of exactly k 0-indexed days, and they can choose any city as their starting point.
Each day, the tourist has two choices:
Return the maximum possible points the tourist can earn.

**Examples**

**Example 1:**

```
Input: n = 2, k = 1, stayScore = [[2,3]], travelScore = [[0,2],[1,0]]
Output: 3
Explanation:
The tourist earns the maximum number of points by starting in city 1 and staying in that city.
```

**Example 2:**

```
Input: n = 3, k = 2, stayScore = [[3,4,2],[2,1,2]], travelScore = [[0,2,1],[2,0,4],[3,2,0]]
Output: 8
Explanation:
The tourist earns the maximum number of points by starting in city 1, staying in that city on day 0, and traveling to city 2 on day 1.
```

**Constraints**

- 1 <= n <= 200
- 1 <= k <= 200
- n == travelScore.length == travelScore[i].length == stayScore[i].length
- k == stayScore.length
- 1 <= stayScore[i][j] <= 100
- 0 <= travelScore[i][j] <= 100
- travelScore[i][i] == 0

---

## 题目（中文翻译）

你得到两个整数 `n` 和 `k`，以及两个二维整数数组 `stayScore` 和 `travelScore`。  

一位游客要在一个拥有 `n` 个城市的国家旅行，每个城市之间都直接相连。游客的旅程恰好包含 `k` 天（使用 **0‑index**），他可以任选一个城市作为出发点。  

每一天，游客有两种选择：

1. **停留（stay）** 在当前所在的城市 `c`，获得 `stayScore[d][c]` 分，其中 `d` 为当前的天数（`0 ≤ d < k`）。  
2. **前往** 另一个城市 `c'`（`c' ≠ c`），获得 `travelScore[c][c']` 分，随后当天结束后游客的所在城市变为 `c'`。  

求游客在 `k` 天结束后能够获得的 **最大可能得分**。

## 示例

### 示例 1  
**输入**  
```
n = 2, k = 1
stayScore = [[2,3]]
travelScore = [[0,2],[1,0]]
```
**输出**  
```
3
```
**解释**  
游客在第 0 天选择在城市 1（下标为 1）停留，获得 `stayScore[0][1] = 3` 分，这是可以得到的最大分数。

### 示例 2  
**输入**  
```
n = 3, k = 2
stayScore = [[3,4,2],[2,1,2]]
travelScore = [[0,2,1],[2,0,4],[3,2,0]]
```
**输出**  
```
8
```
**解释**  
游客在城市 1（下标为 1）开始旅行。  
- 第 0 天停留在城市 1，获得 `stayScore[0][1] = 4` 分。  
- 第 1 天前往城市 2（下标为 2），获得 `travelScore[1][2] = 4` 分。  

总得分 `4 + 4 = 8` 为最大可能得分。

## 约束条件
- `1 ≤ n ≤ 200`
- `1 ≤ k ≤ 200`
- `n == travelScore.length == travelScore[i].length == stayScore[i].length`
- `k == stayScore.length`
- `1 ≤ stayScore[i][j] ≤ 100`
- `0 ≤ travelScore[i][j] ≤ 100`
- `travelScore[i][i] == 0`   （停留在同一城市的旅行得分为 0）

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把每一天的「去哪儿」全部枚举出来，然后把所有可能的得分加起来，取最大值。  

- **数据结构**：我们可以用一个长度为 `k` 的列表 `path` 来保存当天所在的城市编号（`0 … n‑1`）。把 `path` 想象成旅行日记本，翻开每一页都写下当天的城市。  
- **为什么正确**：只要把所有合法的 `path`（每一天可以 stay 也可以 travel）都遍历一遍，必然会碰到最优的那条路线，取最大分数自然就是答案。  
- **复杂度分析**：  
  - 第 0 天可以选 `n` 个起点。  
  - 第 1 天可以 **stay**（只有 1 种）或 **travel** 到其它 `n‑1` 个城市 → 大约 `n` 种选择。  
  - 第 2 天同理……第 `k‑1` 天仍有 `n` 种选择。  
  - 总的枚举次数是 `n × n × … × n = n^k`（`k` 次乘法），即 **指数级**。  
  - 时间复杂度记作 **O(n^k)**，意思是如果 `n=200, k=200`，根本不可能在电脑上跑完。  
  - 空间上只需要保存 `path`（长度 `k`）和当前得分，都是 **O(k)**，几乎可以忽略。  

> **大白话**：把所有可能的旅行计划列成一本巨大的“旅行手册”，每翻一页就算一次分数。手册太厚，根本翻不完。

#### 代码（Python）  

```python
from typing import List

def maxPoints_bruteforce(n: int, k: int,
                         stayScore: List[List[int]],
                         travelScore: List[List[int]]) -> int:
    """暴力递归枚举所有可能的路线（仅作思路展示，实际会超时）"""
    best = 0                     # 全局最大分数

    def dfs(day: int, city: int, cur: int):
        """第 day 天结束后位于 city，已经得到 cur 分数"""
        nonlocal best
        if day == k:              # 已经走完 k 天（0‑index），更新答案
            best = max(best, cur)
            return

        # 1️⃣ 当天选择「stay」——分数加 stayScore[day][city]
        dfs(day + 1, city,
            cur + stayScore[day][city])

        # 2️⃣ 当天选择「travel」到其它城市
        for nxt in range(n):
            if nxt == city:       # 不能“旅行”到自己（那等价于 stay）
                continue
            dfs(day + 1, nxt,
                cur + travelScore[city][nxt])

    # 题目允许任意城市作为起点，第一天只能「stay」一次
    for start in range(n):
        dfs(1, start, stayScore[0][start])   # 第 0 天直接算 stay 分

    return best
```

> 关键行的中文注释已经写在代码里，直接跑会得到正确答案，只是 **会超时**。

#### 复杂度  

- **时间复杂度**：`O(n^k)` —— 每天都有 `n` 种选择，指数增长，实际不可接受。  
- **空间复杂度**：`O(k)` —— 递归栈的深度最多 `k`，以及保存当前分数的变量。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**每一天的决策只和前一天所在的城市有关**，而不需要记住更早的历史。  
这正好符合「动态规划」的思路：把「从第 0 天到第 i 天，最后停在城市 j 时的最高得分」记下来，后面的天数只在此基础上转移。

**慢在哪里？**  
- 暴力解每次都重新遍历所有可能的前一天城市，导致指数级的重复计算。  
- 实际上，同一天、同一城市的最高得分只会出现一次，后面可以直接复用。

**核心概念——状态 & 转移**  

| 名称 | 含义 | 类比 |
|------|------|------|
| `dp[i][j]` | 第 `i` 天（0‑index）结束时，游客位于城市 `j` 能获得的最大总分 | 想象成「第 i 天的城市排行榜」——第 `j` 名的分数 |
| 初始状态 | 第 0 天只能「stay」一次，`dp[0][j] = stayScore[0][j]` | 直接把第一天的日记本填好 |
| 转移方程 | 对第 `i (≥1)` 天的每个城市 `j`，有两种来源：<br>1. 前一天就在 `j`，选择「stay」<br>2. 前一天在其它城市 `p`，选择「travel」到 `j` | 把「昨天的最高分」带到今天：<br>· 继续呆在原地 → 加上当天的 stay 分<br>· 换城市 → 加上 travel 分 |
| 公式 | `dp[i][j] = max( dp[i-1][j] + stayScore[i][j] ,   max_{p≠j}( dp[i-1][p] + travelScore[p][j] ) )` | 把两条可能的路线得分算出来，取更大的那条 |
| 答案 | `max_j dp[k-1][j]`（第 `k-1` 天结束时的最高分） | 最后一天排行榜的最高分 |

**一步步推导**  

1. **第一天**：只可能「stay」，所以直接把 `stayScore[0][*]` 放进 `dp[0][*]`。  
2. **第二天**：要么继续待在同一城市（把前一天的分数加上当天的 stay），要么从其他城市飞过来（前一天的分数 + travel 分）。  
3. **后面的每一天**：同理，只需要看「昨天」的 `dp` 表，找出对每个城市的最佳来源。  

因为 `n, k ≤ 200`，我们可以直接用两层循环枚举 `p`，时间是 `O(k·n²)`，空间只需要保存 `k·n` 的表（或者滚动数组压到 `O(n)`）。

**类比帮助记忆**  
- 把 `dp[i][j]` 想成「第 i 天的城市 j 的最高分卡片」。每天结束后，我们把所有卡片更新一次：把「昨天卡片」的分数 +「今天的加分」写到新卡片上，取最大的写进去。

#### 代码（Python）  

```python
from typing import List

def maxPoints_dp(n: int, k: int,
                 stayScore: List[List[int]],
                 travelScore: List[List[int]]) -> int:
    """
    动态规划 O(k * n^2) 解法
    dp[i][j] 表示第 i 天（0-index）结束后，游客位于城市 j 时的最高总分。
    """
    # ---------- 初始化 ----------
    dp = [[0] * n for _ in range(k)]          # dp[i][j] 的二维表
    for city in range(n):
        dp[0][city] = stayScore[0][city]      # 第 0 天只能 stay

    # ---------- 状态转移 ----------
    for day in range(1, k):                    # 从第 1 天遍历到第 k-1 天
        for cur in range(n):                  # 目标城市 cur
            # 1) 昨天就在 cur，选择 stay
            best = dp[day - 1][cur] + stayScore[day][cur]

            # 2) 从其它城市 p 旅行到 cur
            for prev in range(n):
                if prev == cur:
                    continue                 # 已经在 cur，算 stay 已经处理
                cand = dp[day - 1][prev] + travelScore[prev][cur]
                if cand > best:
                    best = cand

            dp[day][cur] = best                # 保存当天结束时的最优分数

    # ---------- 结果 ----------
    return max(dp[k - 1])                      # 最后一天所有城市的最大值
```

**代码要点**  

- `dp[0][city] = stayScore[0][city]` 是基准情形（第一天只能停留）。  
- 双层循环 `for prev in range(n)` 实现 “从所有可能的前一天城市转移”。  
- `best` 先算 “stay” 再比较所有 “travel”，保证取最大。  
- 最后 `max(dp[k-1])` 把第 `k-1` 天（即第 `k` 天）的排行榜最高分取出来。  

#### 复杂度  

- **时间复杂度**：`O(k * n²)` ——  
  - `k` 天 × `n` 目标城市 × `n` 前一天城市的枚举。  
  - 与暴力的 `O(n^k)` 相比，指数下降到多项式，`200 * 200 * 200 = 8,000,000` 次运算，完全可以接受。  
- **空间复杂度**：`O(k * n)` —— 存放整个 `dp` 表（约 `40,000` 个整数）。如果进一步压缩，只保留前一天的数组，则可以降到 `O(n)`，但这里为了易读保持完整表。  

---

## 心得  

- **核心技巧**：把「每天的选择只和前一天所在城市有关」抽象为 **动态规划**，用 `dp[day][city]` 记录「到此为止的最高分」。  
- **适用题型**：  
  1. **路径最大值** 类问题，如「在网格/矩阵中移动获得最大分数」  
  2. **状态仅与上一步相关** 的 DP，例如「股票买卖的最大利润」  
  3. **多状态转移**（stay / move）的旅行类题目，如「旅行者的最大收益」  
- **一句话总结**：  
  > 把「每一天的最佳分数」装进表格，前一天的最优直接帮助计算后一天的最优——这就是 DP 的魔法。  

---

## 反思  

- **第一反应**：看到「每一天可以 stay 或 travel」立刻想到「枚举所有可能的路线」。  
- **最容易踩的坑**：  
  - 忘记 **第 0 天只能 stay**（因为没有前一天的城市可供 travel）。  
  - 在转移时把 `travelScore[i][i]`（等于 0）误当作一次合法的 travel，导致重复计分。  
  - 边界条件：`k = 1` 时只返回第一天的 stay 分数。  
- **下次类似题的第一步**：先问自己「状态只和上一步有关吗？」如果答案是「是」，立刻写出 `dp[day][state]` 的定义，再推导转移方程——这一步往往能把指数暴力直接压到多项式。