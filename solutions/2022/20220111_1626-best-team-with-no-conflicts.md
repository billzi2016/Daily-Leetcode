# #1626. 无冲突的最佳球队 / Best Team With No Conflicts

> 难度：中等 · 标签：Array、Dynamic Programming、Sorting · [LeetCode 链接](https://leetcode.com/problems/best-team-with-no-conflicts/)

---

## 题目（英文原版）

**Description**

You are the manager of a basketball team. For the upcoming tournament, you want to choose the team with the highest overall score. The score of the team is the sum of scores of all the players in the team.
However, the basketball team is not allowed to have conflicts. A conflict exists if a younger player has a strictly higher score than an older player. A conflict does not occur between players of the same age.
Given two lists, scores and ages, where each scores[i] and ages[i] represents the score and age of the ith player, respectively, return the highest overall score of all possible basketball teams.

**Examples**

**Example 1:**

```
Input: scores = [1,3,5,10,15], ages = [1,2,3,4,5]
Output: 34
Explanation: You can choose all the players.
```

**Example 2:**

```
Input: scores = [4,5,6,5], ages = [2,1,2,1]
Output: 16
Explanation: It is best to choose the last 3 players. Notice that you are allowed to choose multiple people of the same age.
```

**Example 3:**

```
Input: scores = [1,2,3,5], ages = [8,9,10,1]
Output: 6
Explanation: It is best to choose the first 3 players.
```

**Constraints**

- 1 <= scores.length, ages.length <= 1000
- scores.length == ages.length
- 1 <= scores[i] <= 106
- 1 <= ages[i] <= 1000

---

## 题目（中文翻译）

你是篮球队的经理。为了即将到来的锦标赛，你希望挑选出整体得分最高的球队。球队的得分是球队中所有球员得分（score）的总和。

然而，球队中不允许出现冲突（conflict）。如果年龄较小的球员的得分严格高于年龄较大的球员，则会产生冲突。相同年龄的球员之间不存在冲突。

给定两个数组 `scores` 和 `ages`，其中 `scores[i]` 和 `ages[i]` 分别表示第 `i` 位球员的得分和年龄，返回所有可能的球队中能够获得的最高整体得分。

### 示例

#### 示例 1
**输入:** `scores = [1,3,5,10,15]`, `ages = [1,2,3,4,5]`  
**输出:** `34`  
**解释:** 你可以选择所有球员。

#### 示例 2
**输入:** `scores = [4,5,6,5]`, `ages = [2,1,2,1]`  
**输出:** `16`  
**解释:** 最佳选择是最后 3 位球员。注意，同龄的球员可以同时被选入。

#### 示例 3
**输入:** `scores = [1,2,3,5]`, `ages = [8,9,10,1]`  
**输出:** `6`  
**解释:** 最佳选择是前 3 位球员。

### 约束条件
- `1 <= scores.length, ages.length <= 1000`
- `scores.length == ages.length`
- `1 <= scores[i] <= 10^6`
- `1 <= ages[i] <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可能的球员组合枚举一遍**，对每一种组合检查是否满足“没有冲突”，如果满足就把这支队伍的总分记下来，最后取最大的那个。

- **枚举组合**可以用二进制的“位掩码”来实现：  
  比如有 4 名球员，`0b1011` 表示我们选了第 0、1、3 名（最低位对应第 0 名）。  
- **检查冲突**：遍历选中的球员两两比较，如果出现「年龄更小但分数更高」的情况，就说明冲突，直接把这套组合抛弃。  
- **记录最大分数**：对每一个合法组合，累加它们的 `scores`，更新全局最大值。

> **类比**：把所有组合想成一本“可能的球队名单”，我们像翻书一样一页一页地检查，哪一页符合规矩，哪一页分数最高。

> **为什么正确**：我们把**所有**合法的球队都遍历了一遍，最大的分数自然不会遗漏。

#### 代码（Python）

```python
from typing import List

def bestTeamScore_bruteforce(scores: List[int], ages: List[int]) -> int:
    n = len(scores)
    best = 0                     # 记录当前找到的最高总分

    # 0 ~ (1<<n)-1 每一个整数的二进制位对应一种选人方式
    for mask in range(1 << n):
        total = 0                # 本次组合的分数和
        valid = True             # 是否满足“没有冲突”

        # 先把选中的球员收集起来，方便后面两两比较
        selected = []
        for i in range(n):
            if mask >> i & 1:    # 第 i 位为 1 表示选第 i 名球员
                selected.append(i)
                total += scores[i]

        # 两两检查冲突：年龄更小且分数更高即为冲突
        for i in range(len(selected)):
            for j in range(i + 1, len(selected)):
                a, b = selected[i], selected[j]
                if (ages[a] < ages[b] and scores[a] > scores[b]) or \
                   (ages[b] < ages[a] and scores[b] > scores[a]):
                    valid = False
                    break
            if not valid:
                break

        if valid:
            best = max(best, total)   # 更新最高分

    return best
```

#### 复杂度  

- **时间复杂度**：`O(2^n * n^2)`  
  - `2^n` 是所有子集的数量（因为每个人都有选或不选两种可能）。  
  - 对每个子集我们最多要遍历 `n` 次把选中的球员收集起来，再进行两两比较，最坏情况是 `O(n^2)`。  
  - **大白话**：如果有 20 个人，`2^20 ≈ 10⁶`，再乘以 `20² = 400`，已经是几亿次运算，根本跑不动。  

- **空间复杂度**：`O(n)`  
  - 只需要保存当前子集的选中列表和若干临时变量。  

> 暴力解虽然思路最简单，但在 `n` 达到 1000（题目上限）时根本不可行，只能作为“起点”。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**冲突的本质是年龄和分数的相对顺序**。如果我们能把球员排成一种“自然顺序”，那么只要保证分数不下降（或不升高），冲突就一定不会出现。

**关键观察**：

1. **先把球员按年龄升序排列**。年龄相同的球员之间不存在冲突，所以可以把他们的分数再按升序排在一起。  
   - 这样得到的序列满足：**左边的球员年龄 ≤ 右边的球员年龄**。  

2. 在上述顺序下，**只要选取的分数序列是非递减的（score[i] ≤ score[j]，i 在左 j 在右），冲突就一定不存在**。  
   - 因为年龄已经不小于左边，若左边分数也不高于右边，就不可能出现“更年轻却分数更高”的情况。  

3. 于是问题转化为：**在这个已排序的列表里，挑选一个分数非递减的子序列，使其分数之和最大**。  
   - 这正是“**带权的最长递增子序列（LIS）**”的变形，只是我们要求的是**最大总分**，而不是长度。  

4. **动态规划**：  
   - `dp[i]` 表示**以第 i 名球员结尾的合法队伍的最高总分**。  
   - 初始时 `dp[i] = scores[i]`（只选自己）。  
   - 转移方程：遍历所有 `j < i`，如果 `scores[j] <= scores[i]`（分数不下降），则可以把第 i 名球员接在第 j 名球员后面，得到更大的总分。  
     ```
     dp[i] = scores[i] + max(dp[j] for j < i and scores[j] <= scores[i])
     ```
   - 最终答案是 `max(dp)`。

5. **复杂度**：  
   - 外层遍历 `i`，内层遍历 `j`，时间 `O(n²)`。  
   - `n ≤ 1000`，`n² = 10⁶`，在 Python 中完全可以接受。  
   - 空间只需要保存 `dp` 数组，`O(n)`。

> 如果想进一步把时间降到 `O(n log n)`，可以使用**树状数组 / 线段树**对分数做离散化后做前缀最大查询。但对本题的限制来说，`O(n²)` 已经足够好。

#### 代码（Python）

```python
from typing import List

def bestTeamScore(scores: List[int], ages: List[int]) -> int:
    # 1️⃣ 把球员打包成 (age, score) 的元组，按年龄升序，年龄相同则按分数升序
    players = sorted(zip(ages, scores))          # 例：[(1,4), (1,5), (2,4), (2,6), ...]

    n = len(players)
    dp = [0] * n                                 # dp[i] = 以 players[i] 为队尾的最高总分
    ans = 0

    # 2️⃣ 动态规划
    for i in range(n):
        cur_score = players[i][1]                # 当前球员的分数
        dp[i] = cur_score                        # 至少可以只选自己

        # 考察所有在它左侧的球员 j，若分数不大于当前分数，就可以接在后面
        for j in range(i):
            if players[j][1] <= cur_score:       # 分数不下降
                dp[i] = max(dp[i], dp[j] + cur_score)

        ans = max(ans, dp[i])                    # 更新全局最大

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 两层循环遍历 `n`（最多 1000）次，约等于一百万次基本操作，跑得非常快。  
  - 与暴力的 `O(2ⁿ)` 相比，**从指数级降到多项式级**，速度提升是天壤之别。  

- **空间复杂度**：`O(n)`  
  - 只用了 `players`（排序后）和 `dp` 两个长度为 `n` 的列表。  

---

## 心得

- **核心技巧**：把“年龄‑分数冲突”转化为**排序 + 非递减分数子序列**的问题，再用**动态规划求最大加权递增子序列**。  
- **适用场景**：  
  1. **带权最长递增子序列**（如 “Maximum Sum Increasing Subsequence”）。  
  2. **需要先排序再做 DP 的配对/选择题**（如 “Maximum Profit in Job Scheduling”）。  
  3. **二维约束转化为单维约束**（如 “Russian Doll Envelopes”）。  
- **一句话总结**：先把约束变成“顺序”，再用 DP 选出“分数不降且总分最高”的子序列，就是解题钥匙。  

---

## 反思

- **第一反应**：看到“冲突”二字，我立刻想到枚举所有子集检查冲突——这就是暴力解的出发点。  
- **最容易踩的坑**：  
  - **排序时的 tie‑break**：年龄相同的球员必须再按分数升序排，否则会误把 `score[j] > score[i]` 的情况当成合法。  
  - **边界条件**：只有一名球员时直接返回他的分数，DP 初始化要保证 `dp[i] = scores[i]`。  
  - **整数溢出**：Python 整数不溢出，但在其他语言要注意使用 64 位。  
- **下次遇到同类题**：第一步先**找能把多维约束“一维化”**（通常是排序），随后考虑 **递增/递减子序列的 DP** 或 **贪心 + 二分**。这样思路更清晰，避免盲目暴力。