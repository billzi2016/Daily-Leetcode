# #2140. 用脑力解题 / Solving Questions With Brainpower

> 难度：中等 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/solving-questions-with-brainpower/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed 2D integer array questions where questions[i] = [pointsi, brainpoweri].
The array describes the questions of an exam, where you have to process the questions in order (i.e., starting from question 0) and make a decision whether to solve or skip each question. Solving question i will earn you pointsi points but you will be unable to solve each of the next brainpoweri questions. If you skip question i, you get to make the decision on the next question.
Return the maximum points you can earn for the exam.

**Examples**

**Example 1:**

```
Input: questions = [[3,2],[4,3],[4,4],[2,5]]
Output: 5
Explanation: The maximum points can be earned by solving questions 0 and 3.
- Solve question 0: Earn 3 points, will be unable to solve the next 2 questions
- Unable to solve questions 1 and 2
- Solve question 3: Earn 2 points
Total points earned: 3 + 2 = 5. There is no other way to earn 5 or more points.
```

**Example 2:**

```
Input: questions = [[1,1],[2,2],[3,3],[4,4],[5,5]]
Output: 7
Explanation: The maximum points can be earned by solving questions 1 and 4.
- Skip question 0
- Solve question 1: Earn 2 points, will be unable to solve the next 2 questions
- Unable to solve questions 2 and 3
- Solve question 4: Earn 5 points
Total points earned: 2 + 5 = 7. There is no other way to earn 7 or more points.
```

**Constraints**

- 1 <= questions.length <= 105
- questions[i].length == 2
- 1 <= pointsi, brainpoweri <= 105

---

## 题目（中文翻译）

你得到一个下标从 0 开始的二维整数数组（2D integer array）`questions`，其中 `questions[i] = [pointsi, brainpoweri]`。  
该数组描述了一场考试的题目序列，你必须按顺序（即从题目 0 开始）依次决定 **解答**（solve）或 **跳过**（skip）每一道题。  

- 解答第 i 题会获得 `pointsi` 分，但随后你将 **无法** 解答接下来的 `brainpoweri` 道题。  
- 跳过第 i 题则可以继续对第 i+1 题做出决策。

返回在整场考试中能够获得的 **最大分数**（maximum points）。

**示例 1**  
输入：`questions = [[3,2],[4,3],[4,4],[2,5]]`  
输出：`5`  
解释：最大分数可以通过解答第 0 题和第 3 题获得。  
- 解答第 0 题：获得 3 分，随后 **无法** 解答接下来的 2 道题  
- 第 1、2 题均被跳过（无法解答）  
- 解答第 3 题：获得 2 分  
总分：`3 + 2 = 5`。不存在其他方案能得到 5 分或更高。

**示例 2**  
输入：`questions = [[1,1],[2,2],[3,3],[4,4],[5,5]]`  
输出：`7`  
解释：最大分数可以通过解答第 1 题和第 4 题获得。  
- 跳过第 0 题  
- 解答第 1 题：获得 2 分，随后 **无法** 解答接下来的 2 道题  
- 第 2、3 题均被跳过（无法解答）  
- 解答第 4 题：获得 5 分  
总分：`2 + 5 = 7`。不存在其他方案能得到 7 分或更高。

**约束条件**  
- `1 <= questions.length <= 10^5`  
- `questions[i].length == 2`  
- `1 <= pointsi, brainpoweri <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每一道题都**尝试两种选择**：  
1. **解这道题** → 获得 `pointsi` 分，然后必须跳过接下来的 `brainpoweri` 道题。  
2. **跳过这道题** → 直接进入下一道题继续决定。

我们可以用**递归**把这两种选择写出来：  
```python
def dfs(i):
    if i >= n:                     # 已经超出题目范围，得 0 分
        return 0
    # 方案1：跳过第 i 题
    skip = dfs(i + 1)
    # 方案2：解第 i 题
    take = questions[i][0] + dfs(i + questions[i][1] + 1)
    return max(skip, take)
```
这里的 `i` 表示“当前正要决定的题号”。  
递归把所有可能的解/跳组合枚举一遍，取最大分数即为答案。

> **类比**：想象你在玩一条直线的“跳房子”。每次站在格子 `i`，你可以选择**停下来得分**，但随后必须跨过去若干格子；或者**直接跳到下一个格子**继续游戏。递归就是把所有可能的跳法都写出来。

该方法**一定能得到正确答案**，因为它穷举了所有合法的决策序列。

#### 代码（Python）

```python
from typing import List
import sys
sys.setrecursionlimit(10**6)   # 防止递归层数太深导致崩溃

def maxPoints_bruteforce(questions: List[List[int]]) -> int:
    n = len(questions)

    # 记忆化搜索（加上缓存可以避免大量重复计算，但仍然是指数级的）
    from functools import lru_cache

    @lru_cache(None)
    def dfs(i: int) -> int:
        if i >= n:                     # 超出数组范围，得 0 分
            return 0
        # 方案1：跳过第 i 题
        skip = dfs(i + 1)
        # 方案2：解第 i 题
        points, brain = questions[i]
        take = points + dfs(i + brain + 1)
        # 取两者的最大值
        return max(skip, take)

    return dfs(0)
```

#### 复杂度  

- **时间复杂度**：`O(2^n)`（指数级）  
  直觉上每道题都有“解”或“跳”两种选择，全部组合大约是 `2^n` 种。即使用了 `lru_cache` 记忆化，最坏情况下仍然会遍历每个状态一次，状态数是 `n`，但每次递归里会产生 `O(n)` 的跳转，整体仍然接近指数级，难以接受。

- **空间复杂度**：`O(n)`  
  递归栈的深度最多为 `n`（每次只往后走），再加上记忆化表的大小 `O(n)`。

> **大白话**：如果有 20 道题，暴力解大约要尝试 `2^20 ≈ 1,000,000` 种情况；若是 1000 道题，情况数会天文数字，根本跑不完。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**每一道题的决定只与后面的子问题有关**。这正是动态规划（DP）的典型特征：把大问题拆成若干**子问题**，自底向上或自顶向下求解。

我们从**后往前**遍历题目，维护一个数组 `dp[i]`，表示**从第 i 题开始（包括 i）能够获得的最大分数**。  
- 当我们站在第 `i` 题时，有两种选择：
  1. **跳过**：分数等于 `dp[i+1]`（从下一题继续）。
  2. **解题**：得到 `points_i`，随后要跳过 `brain_i` 道题，下一次可以考虑的题目是 `i + brain_i + 1`，因此分数为 `points_i + dp[i + brain_i + 1]`（如果越界则取 0）。

`dp[i] = max(dp[i+1], points_i + dp[i + brain_i + 1])`

因为我们是从后往前填表，`dp[i+1]`、`dp[i+brain_i+1]` 已经算好，直接取最大即可。

**关键点**：

- **单向遍历**：只需要一次从右到左的循环，时间线性。
- **额外空间**：需要一个长度为 `n+1` 的 DP 数组（多一个哨兵 `dp[n]=0`，方便越界时直接返回 0）。

> **类比**：想象你在跑步机上倒着走，每走到一个格子，你要决定是**停下来得分**还是**直接跳到前面**。因为你已经知道前面每个格子最好的得分（已经算好），只要比较这两种选择的总分，就能得到当前格子的最佳答案。

#### 代码（Python）

```python
from typing import List

def maxPoints_dp(questions: List[List[int]]) -> int:
    n = len(questions)
    # dp[i] 表示从第 i 题开始（包括 i）能够获得的最大分数
    dp = [0] * (n + 1)          # 多一个位置，dp[n] = 0 代表已超出题目

    # 从后往前遍历
    for i in range(n - 1, -1, -1):
        points, brain = questions[i]
        # 选项一：跳过第 i 题
        skip = dp[i + 1]
        # 选项二：解第 i 题
        #   - 下一个可以考虑的题目下标是 i + brain + 1
        #   - 若越界，则 dp[...] 自动为 0（因为 dp 数组已经填满 0）
        take = points + dp[min(n, i + brain + 1)]
        # 取两者的最大值
        dp[i] = max(skip, take)

    # 答案就是从第 0 题开始的最大分数
    return dp[0]
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  只遍历一次数组，每一步做常数时间的比较与加法。对比暴力的指数级，快得多。

- **空间复杂度**：`O(n)`  
  需要额外的 DP 数组存放 `n+1` 个整数。如果想进一步压缩空间，可以只保留后面若干个状态（因为 `dp[i]` 只依赖 `dp[i+1]` 和 `dp[i+brain_i+1]`），但在本题 `n ≤ 10^5` 时，`O(n)` 已经足够。

> **对比**：暴力解在 10^5 条数据上根本跑不完，而最优解只需要几毫秒。

---

## 心得

- **核心技巧**：把“是否解题”抽象成**二选一的状态转移**，使用**逆向动态规划**（从后往前）求解子问题的最优值。  
- **适用题型**：  
  1. “做或不做”且**决定后会跳过若干后续元素**的题目（如本题、LeetCode 1696 `Jump Game VI` 的变形）。  
  2. “在数组中挑选不相邻元素求最大和”类问题（如“打家劫舍”）。  
  3. “带冷却时间的任务调度”类问题（如 LeetCode 309 `Best Time to Buy and Sell Stock with Cooldown`）。
- **一句话总结**：**把每一步的两种选择写成递推公式，逆向遍历即可得到全局最优。**

---

## 反思

- **第一反应**：看到“解题后要跳过 `brainpower` 题”，立刻想到“递归枚举所有可能”。  
- **最容易踩的坑**：  
  1. **越界处理**：`i + brain_i + 1` 可能超过数组长度，需要安全返回 0。  
  2. **大数溢出**：在 Python 中不必担心，但在某些语言要使用 64 位整数。  
  3. **记忆化/DP 表的初始化**：忘记把 `dp[n]=0` 设置好会导致错误。  
- **下次类似题目**：第一步先**写出状态 `dp[i]` 表示从第 i 开始的最优解**，再**列出转移方程**（跳或不跳），最后决定是**自底向上**还是**自顶向下**实现。这样可以快速摆脱暴力的思维陷阱。