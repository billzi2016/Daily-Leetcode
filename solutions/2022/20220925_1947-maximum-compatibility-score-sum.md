# #1947. 最大兼容度得分和 / Maximum Compatibility Score Sum

> 难度：中等 · 标签：Array、Dynamic Programming、Backtracking、Bit Manipulation、Bitmask · [LeetCode 链接](https://leetcode.com/problems/maximum-compatibility-score-sum/)

---

## 题目（英文原版）

**Description**

There is a survey that consists of n questions where each question's answer is either 0 (no) or 1 (yes).
The survey was given to m students numbered from 0 to m - 1 and m mentors numbered from 0 to m - 1. The answers of the students are represented by a 2D integer array students where students[i] is an integer array that contains the answers of the ith student (0-indexed). The answers of the mentors are represented by a 2D integer array mentors where mentors[j] is an integer array that contains the answers of the jth mentor (0-indexed).
Each student will be assigned to one mentor, and each mentor will have one student assigned to them. The compatibility score of a student-mentor pair is the number of answers that are the same for both the student and the mentor.
You are tasked with finding the optimal student-mentor pairings to maximize the sum of the compatibility scores.
Given students and mentors, return the maximum compatibility score sum that can be achieved.

**Examples**

**Example 1:**

```
Input: students = [[1,1,0],[1,0,1],[0,0,1]], mentors = [[1,0,0],[0,0,1],[1,1,0]]
Output: 8
Explanation: We assign students to mentors in the following way:
- student 0 to mentor 2 with a compatibility score of 3.
- student 1 to mentor 0 with a compatibility score of 2.
- student 2 to mentor 1 with a compatibility score of 3.
The compatibility score sum is 3 + 2 + 3 = 8.
```

**Example 2:**

```
Input: students = [[0,0],[0,0],[0,0]], mentors = [[1,1],[1,1],[1,1]]
Output: 0
Explanation: The compatibility score of any student-mentor pair is 0.
```

**Constraints**

- m == students.length == mentors.length
- n == students[i].length == mentors[j].length
- 1 <= m, n <= 8
- students[i][k] is either 0 or 1.
- mentors[j][k] is either 0 or 1.

---

## 题目（中文翻译）

有一个包含 **n** 个问题的调查问卷，每个问题的答案只能是 0（否）或 1（是）。  
该调查分别发给编号为 `0 … m‑1` 的 **m** 名学生和编号为 `0 … m‑1` 的 **m** 名导师。学生的答案用二维整数数组 **students** 表示，其中 `students[i]` 是第 `i` 位学生（0‑索引）的答案数组。导师的答案用二维整数数组 **mentors** 表示，其中 `mentors[j]` 是第 `j` 位导师（0‑索引）的答案数组。

每位学生必须分配给恰好一位导师，每位导师也只能分配到恰好一名学生。  
**学生‑导师配对（student‑mentor pair）** 的 **兼容度得分（compatibility score）** 定义为学生和导师在相同位置上答案相同的数量。

任务是寻找一种学生与导师的配对方式，使所有配对的兼容度得分之和最大。  
给定 **students** 和 **mentors**，返回可以得到的最大兼容度得分和。

**示例 1**  
**输入**  
``` 
students = [[1,1,0],[1,0,1],[0,0,1]], 
mentors = [[1,0,0],[0,0,1],[1,1,0]]
```  
**输出**  
```
8
```  
**解释**  
我们可以按如下方式分配学生与导师：  
- 学生 0 分配给导师 2，兼容度得分为 3。  
- 学生 1 分配给导师 0，兼容度得分为 2。  
- 学生 2 分配给导师 1，兼容度得分为 3。  
总兼容度得分为 `3 + 2 + 3 = 8`。

**示例 2**  
**输入**  
``` 
students = [[0,0],[0,0],[0,0]], 
mentors = [[1,1],[1,1],[1,1]]
```  
**输出**  
```
0
```  
**解释**  
任意学生‑导师配对的兼容度得分均为 0。

**约束条件**  

- `m == students.length == mentors.length`  
- `n == students[i].length == mentors[j].length`  
- `1 <= m, n <= 8`  
- `students[i][k]` 只能是 0 或 1  
- `mentors[j][k]` 只能是 0 或 1

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：把所有学生和导师的配对方式全部列举一遍，算出每种配对的兼容度之和，取最大值。  

- **数据结构**  
  - **数组**：`students[i]`、` mentors[j]` 本身就是二维数组，直接用来存放每个人的答案。  
  - **排列（Permutation）**：把 `0 … m-1` 这 `m` 个学生的下标排成一个序列，序列的第 `k` 位表示第 `k` 位导师（下标 `k`）要配给哪个学生。排列就像把一堆书按不同顺序摆放，所有可能的摆法就是所有排列。  

- **为什么正确**  
  每一种排列对应一种合法的“一对一”配对方式，遍历 **所有** 排列就一定会覆盖最优的那一种。只要我们对每个配对计算出兼容度（相同答案的个数），把它们加起来，就得到该排列的总分。最大值自然就是答案。  

- **复杂度分析（大白话）**  
  - 学生 `m` 最多是 8，排列的数量是 `m!`（m 的阶乘），比如 `8! = 40320`，这在电脑里跑几毫秒就好。  
  - 对每一种排列，我们要计算 `m` 对的兼容度，每对需要比较 `n` 个答案（`n ≤ 8`），所以一次排列的工作量是 `m * n`。  
  - **时间复杂度**：`O(m! * m * n)` → 这里的 `O` 只是一种“量级”，意思是随着 `m` 增大，运行时间会像阶乘一样快速增长，但因为 `m ≤ 8`，实际运行非常快。  
  - **空间复杂度**：只需要保存输入数组和几个临时变量，`O(1)`（常数级别）。  

#### 代码（Python）  

```python
from itertools import permutations
from typing import List

def maxCompatibilityScore(students: List[List[int]], mentors: List[List[int]]) -> int:
    m, n = len(students), len(students[0])

    # ---------- 计算两个人的兼容度 ----------
    def score(a: List[int], b: List[int]) -> int:
        # 把对应位置相同的次数加起来
        return sum(1 for i in range(n) if a[i] == b[i])

    # 预先算好所有 student‑mentor 的兼容度，后面查表更快
    # compat[i][j] 表示 student i 和 mentor j 的分数
    compat = [[score(students[i], mentors[j]) for j in range(m)] for i in range(m)]

    best = 0
    # permutations 会返回所有 (0,1,…,m-1) 的排列，例如 (2,0,1)
    for perm in permutations(range(m)):
        total = 0
        # 第 k 位导师 (下标 k) 配给学生 perm[k]
        for mentor_idx, student_idx in enumerate(perm):
            total += compat[student_idx][mentor_idx]
        best = max(best, total)   # 记录最大总分

    return best
```

> **关键行中文注释**  
> - `permutations(range(m))`：枚举所有学生的排列方式。  
> - `compat[student_idx][mentor_idx]`：直接查表得到这对的兼容度，省去重复比较。  

#### 复杂度  

- **时间复杂度**：`O(m! * m * n)`  
  - 这里的 `m!` 表示所有排列的数量，`m*n` 是每个排列里要累加的分数。对 `m ≤ 8` 来说，最多约 `40320 * 8 * 8 ≈ 2.6×10⁶` 次基本操作，毫秒级完成。  
- **空间复杂度**：`O(m * n)`（存 `compat` 表）  
  - 只需要一个 `m×m` 的二维数组保存兼容度，规模很小。  

---  

### 2. 最优解  

#### 思路  

暴力解的 **瓶颈** 在于我们把所有排列一次性枚举出来，虽然 `m` 很小，但如果把 `m` 放大一点（比如 15），阶乘会爆炸。我们可以利用 **状态压缩 DP（动态规划）** 把搜索过程变成“逐步构造”，每次只决定一个学生配哪个导师，记住已经配好的导师，用 **位掩码（bitmask）** 表示。

**核心概念——位掩码**  
- 把一个整数的二进制位当作 “是否已经被使用” 的标记。  
- 例如 `mask = 0b0101`（二进制）表示第 0、2 位对应的导师已经被配走，其他未配。  
- 这种表示方式像是把 `m` 把钥匙挂在一排，每把钥匙的状态（上/下）告诉我们它是否已经被借走。

**DP 定义**  
- `dp[mask]`：当 **已经为前 `popcount(mask)` 位学生**（即已经决定了多少个学生）**配好了导师，且已使用的导师集合对应 `mask`** 时，能够得到的最大兼容度总和。  
- `popcount(mask)` 是 `mask` 二进制里 `1` 的个数，表示已经配对了多少位学生。  

**状态转移**  
- 当前我们要给第 `i = popcount(mask)` 位学生挑导师。遍历所有未被使用的导师 `j`（即 `mask` 第 `j` 位为 0），尝试把 `j` 分配给学生 `i`。  
- 新的掩码 `new_mask = mask | (1 << j)` 表示把导师 `j` 标记为已用。  
- 更新 `dp[new_mask] = max(dp[new_mask], dp[mask] + compat[i][j])`。  

**起始与结束**  
- `dp[0] = 0`（什么都没配，分数为 0）。  
- 最终答案是 `dp[(1 << m) - 1]`，即所有导师都已配完的状态。  

**为什么快**  
- 总状态数是 `2^m`（每位导师要么已配要么未配），对 `m = 8` 来说只有 256。  
- 对每个状态我们最多遍历 `m` 个导师，整体时间 `O(m * 2^m)`，远远小于 `m!`。  

#### 代码（Python）  

```python
from typing import List

def maxCompatibilityScore(students: List[List[int]], mentors: List[List[int]]) -> int:
    m, n = len(students), len(students[0])

    # ---------- 预计算兼容度矩阵 ----------
    def score(a: List[int], b: List[int]) -> int:
        return sum(1 for k in range(n) if a[k] == b[k])

    compat = [[score(students[i], mentors[j]) for j in range(m)] for i in range(m)]

    # ---------- DP + 位掩码 ----------
    total_states = 1 << m               # 2^m 种可能的 mask
    dp = [-1] * total_states            # -1 表示“未访问”
    dp[0] = 0                           # 初始状态：没有配对，得分 0

    for mask in range(total_states):
        # 已经配了多少个学生（也就是要配下一个的学生下标）
        i = bin(mask).count('1')        # popcount，Python 里可以用 mask.bit_count()（3.8+）
        if i >= m:                      # 全部配完了，后面不需要继续
            continue
        for j in range(m):
            if not (mask >> j) & 1:     # 第 j 位是 0，表示导师 j 还没被用
                new_mask = mask | (1 << j)
                # 更新新状态的最大得分
                dp[new_mask] = max(dp[new_mask],
                                   dp[mask] + compat[i][j])

    # 所有导师都配完的 mask 为 (1<<m)-1
    return dp[total_states - 1]
```

> **关键行中文注释**  
> - `mask >> j & 1`：检查第 `j` 位是否已经被占用。  
> - `dp[mask] + compat[i][j]`：把第 `i` 位学生配给第 `j` 位导师后得到的总分。  
> - `dp[new_mask] = max(...)`：保留所有可能配法中最好的那一个。  

#### 复杂度  

- **时间复杂度**：`O(m * 2^m)`  
  - 解释：`2^m` 是所有掩码的数量（最多 256），每个掩码我们最多尝试 `m` 次配对（最多 8 次），所以总操作不到 2000 次，几乎瞬间完成。相比暴力的 `m!`（40320）要快很多。  
- **空间复杂度**：`O(2^m + m^2)`  
  - `2^m` 用来存 `dp` 表，`m^2` 用来存兼容度矩阵。规模仍然很小（几百个整数）。  

---  

## 心得  

- **核心技巧**：**位掩码动态规划**（Bitmask DP）  
  - 把“哪些导师已经被配走”压缩到一个整数的二进制位中，利用 DP 按步递进求最大值。  
- **适用题型**（类似思路）  
  1. **分配类**：`Maximum Score from Performing Multiplication`, `Assign Cookies`（需要选/不选）  
  2. **旅行商问题**的简化版：`Shortest Path Visiting All Nodes`（LeetCode 847）  
  3. **子集枚举**：`Partition to K Equal Sum Subsets`、`Count Number of Nice Subarrays`（使用位掩码或子集 DP）  
- **一句话总结解题钥匙**：  
  “把‘已经用过的对象’用二进制位记录下来，逐步扩展状态，利用 DP 保存每一步的最优解”。  

---  

## 反思  

- **拿到题目第一反应**：  
  “这不就是把学生和导师全排列后算分吗？”于是立刻想到暴力枚举。  
- **最容易踩的坑**  
  1. **忘记把 `mask` 的位数对应到导师下标**，导致配对顺序错位。  
  2. **没有预先计算兼容度矩阵**，在 DP 里每次都重新比较，会把时间从 `O(m*2^m)` 拉回到 `O(m^2*2^m)`，仍然可以接受但不够优雅。  
  3. **边界条件**：当 `m = 0`（题目不允许）或 `mask` 已经是全 1 时，不要再继续循环。  
- **下次遇到同类题的第一步**：  
  “先判断是否可以用位掩码把‘已选/未选’状态压缩”，如果可以，就直接转向位掩码 DP；如果 `m` 太大而不可行，再考虑搜索+剪枝或其他近似方法。