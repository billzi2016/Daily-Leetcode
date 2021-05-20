# #1335. 工作安排的最小难度 / Minimum Difficulty of a Job Schedule

> 难度：困难 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/minimum-difficulty-of-a-job-schedule/)

---

## 题目（英文原版）

**Description**

You want to schedule a list of jobs in d days. Jobs are dependent (i.e To work on the ith job, you have to finish all the jobs j where 0 <= j < i).
You have to finish at least one task every day. The difficulty of a job schedule is the sum of difficulties of each day of the d days. The difficulty of a day is the maximum difficulty of a job done on that day.
You are given an integer array jobDifficulty and an integer d. The difficulty of the ith job is jobDifficulty[i].
Return the minimum difficulty of a job schedule. If you cannot find a schedule for the jobs return -1.

**Examples**

**Example 1:**

```
Input: jobDifficulty = [6,5,4,3,2,1], d = 2
Output: 7
Explanation: First day you can finish the first 5 jobs, total difficulty = 6.
Second day you can finish the last job, total difficulty = 1.
The difficulty of the schedule = 6 + 1 = 7
```

**Example 2:**

```
Input: jobDifficulty = [9,9,9], d = 4
Output: -1
Explanation: If you finish a job per day you will still have a free day. you cannot find a schedule for the given jobs.
```

**Example 3:**

```
Input: jobDifficulty = [1,1,1], d = 3
Output: 3
Explanation: The schedule is one job per day. total difficulty will be 3.
```

**Constraints**

- 1 <= jobDifficulty.length <= 300
- 0 <= jobDifficulty[i] <= 1000
- 1 <= d <= 10

---

## 题目（中文翻译）

你需要在 **d 天** 内安排一系列工作。工作之间存在依赖关系（即：要完成第 *i* 项工作，必须先完成所有下标满足 `0 <= j < i` 的工作）。  
每天必须完成至少一项工作。**工作安排的难度** 定义为这 *d* 天中每一天难度的总和；一天的难度是该天完成的所有工作中 **难度的最大值**（job difficulty）。  

给定整数数组 `jobDifficulty` 和整数 `d`，其中 `jobDifficulty[i]` 表示第 *i* 项工作的难度。  
返回能够完成所有工作且难度最小的工作安排的总难度。如果不存在合法的安排，返回 `-1`。

## 示例

### 示例 1
**输入**  
`jobDifficulty = [6,5,4,3,2,1], d = 2`  

**输出**  
`7`  

**解释**  
第一天可以完成前 5 项工作，最大难度为 `6`。  
第二天完成最后一项工作，最大难度为 `1`。  
安排的总难度 = `6 + 1 = 7`。

### 示例 2
**输入**  
`jobDifficulty = [9,9,9], d = 4`  

**输出**  
`-1`  

**解释**  
即使每天只做一项工作，也会出现空闲的天数，无法在规定的天数内完成所有工作，故返回 `-1`。

### 示例 3
**输入**  
`jobDifficulty = [1,1,1], d = 3`  

**输出**  
`3`  

**解释**  
安排为每天完成一项工作，三天的最大难度分别为 `1、1、1`，总难度为 `3`。

## 约束条件
- `1 <= jobDifficulty.length <= 300`
- `0 <= jobDifficulty[i] <= 1000`
- `1 <= d <= 10`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有可能的「每天做哪些连续的工作」全部列举出来，然后计算每一种划分的总难度，取最小值。

- **数据结构**：我们只需要 **数组** 和 **递归**（或遍历所有切分点的循环）。  
  把 `jobDifficulty` 看成一本连续的章节册子，**每天**要读完若干连续的章节。我们可以把「每天的切分点」想象成在册子里插入 `d‑1` 根分割线，分割线左边的章节在前一天完成，右边的在后一天完成。  
- **为什么正确**：只要枚举了所有合法的切分方式（每一天至少有一项工作），我们就一定会看到最优的那一种。  
- **时间/空间复杂度**：  
  - 如果直接递归遍历所有切分方式，时间复杂度大约是 `O(n^{d})`（因为每一天都有 `O(n)` 种选法，重复 `d` 次）。  
  - 空间上只需要保存递归栈，最深 `d` 层，空间复杂度 `O(d)`。  
  用大白话说，`O(n^{d})` 就像「把 300 本书每本都可能在 10 天的某一天读完」的所有排列组合，根本不可算。

#### 代码（Python）

```python
from typing import List

def minDifficulty_bruteforce(jobDifficulty: List[int], d: int) -> int:
    n = len(jobDifficulty)
    # 如果工作总数小于天数，根本不可能安排完
    if n < d:
        return -1

    # 递归函数：从下标 start 开始，剩余 days 天要安排
    def dfs(start: int, days: int) -> int:
        # base case：只剩一天，必须把剩下的全部放在这一天
        if days == 1:
            return max(jobDifficulty[start:])   # 这一天的难度就是这段的最大值

        # 否则在 start..n-days 之间挑一个切分点（保证后面还有 enough jobs）
        best = float('inf')
        cur_max = 0
        # i 为本天最后一个工作的下标，必须留出 days-1 天给后面的工作
        for i in range(start, n - days + 1):
            cur_max = max(cur_max, jobDifficulty[i])   # 本天的最大难度
            # 递归求后面 days-1 天的最小难度
            next_part = dfs(i + 1, days - 1)
            best = min(best, cur_max + next_part)
        return best

    return dfs(0, d)
```

#### 复杂度  

- **时间复杂度**：`O(n^{d})`  
  - 直观解释：每一天都有 `≈ n` 种切法，重复 `d` 次，就像把 `n` 块糖果分到 `d` 只小猪的所有可能。  
- **空间复杂度**：`O(d)`  
  - 只用递归栈保存 `d` 层调用，和输入规模 `n` 无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**重复计算**同一段子数组的最大值以及子问题的最小难度。我们可以把「从左到右划分」的过程抽象成**动态规划（DP）**，把已经算好的子问题结果保存下来，避免重复。

**核心点**：

1. **状态定义**  
   - `dp[i][k]` 表示「把前 `i`（不含下标 `i`）个工作划分成 `k` 天的最小总难度」。  
   - 这里的 `i` 范围是 `0 … n`，`k` 范围是 `0 … d`。  
   - 初始时 `dp[0][0] = 0`（0 天完成 0 工作，难度为 0），其余为正无穷大（不可达）。

2. **状态转移**  
   - 对于第 `k` 天，我们需要决定这天到底做哪些连续的工作。设这天的最后一个工作是下标 `i-1`（即划分到 `i`），那么这天的工作范围是 `j … i-1`（`j` 为第 `k-1` 天结束后第一个工作的位置）。  
   - 那么 `dp[i][k] = min_{j < i} ( dp[j][k-1] + max(jobDifficulty[j:i]) )`  
   - `max(jobDifficulty[j:i])` 可以在遍历 `j` 的时候 **从右往左维护**，不必每次重新遍历整段。这样把「取段最大值」的成本降到 `O(1)`（摊还后）。

3. **遍历顺序**  
   - 外层循环天数 `k`（从 1 到 `d`），  
   - 中层循环当前位置 `i`（从 `k` 到 `n`，因为至少要 `k` 个工作才能分成 `k` 天），  
   - 内层逆向遍历 `j`（从 `i-1` 向前），同时更新 `cur_max` 为 `jobDifficulty[j]` 与之前的最大值的较大者。  

4. **为什么是最优**  
   - 动态规划把「把前 i 项划分成 k 天」的所有可能都考虑进来了，而每个子状态只计算一次，避免了暴力解的指数级重复。  
   - 由于我们始终使用 **连续子数组**（工作必须保持顺序），上述转移是完整且不遗漏的。

5. **时间复杂度分析**  
   - 三层循环的最坏次数约为 `d * n * n`（外层 `d ≤ 10`，中、内层 `n ≤ 300`），即 `O(d·n²)`。  
   - 对于本题的约束，这大约是 `10 * 300 * 300 = 900,000` 次运算，完全可以接受。  

6. **空间复杂度**  
   - 只需要 `dp` 二维数组 ` (n+1) × (d+1) `，即 `O(n·d)`。  

**类比**：把 `dp` 想成「记忆表」——就像我们在做十字绣时，把已经完成的格子颜色记录下来，下次再拼图时直接查表，不必重新绣一遍。

#### 代码（Python）

```python
from typing import List
import math

def minDifficulty(jobDifficulty: List[int], d: int) -> int:
    n = len(jobDifficulty)
    # 工作数不足天数，直接返回 -1
    if n < d:
        return -1

    # dp[i][k] = 前 i 项（0..i-1）划分成 k 天的最小总难度
    dp = [[math.inf] * (d + 1) for _ in range(n + 1)]
    dp[0][0] = 0                     # 0 天完成 0 工作，难度为 0

    # 枚举天数
    for k in range(1, d + 1):
        # 至少要 k 项工作才能划分成 k 天
        for i in range(k, n + 1):
            cur_max = 0
            # 逆向遍历，确定第 k 天的起始位置 j
            # j 为第 k-1 天结束后第一个工作的位置
            for j in range(i - 1, k - 2, -1):   # j >= k-1
                cur_max = max(cur_max, jobDifficulty[j])   # 更新第 k 天的最大难度
                # dp[j][k-1] 已经是前 j 项划分成 k-1 天的最优值
                dp[i][k] = min(dp[i][k], dp[j][k - 1] + cur_max)

    # 最终答案是前 n 项划分成 d 天的最小难度
    return dp[n][d] if dp[n][d] != math.inf else -1
```

#### 复杂度  

- **时间复杂度**：`O(d·n²)`  
  - 直观解释：我们有 `d` 天，每天遍历所有可能的「今天的起始位置」(`n`)，而每次又要在这段里往左扫 `n` 次，整体就是「天数 × 工作数的平方」。在本题约束下，这相当于「最多十次遍历三百本书的所有子段」，非常快。  
- **空间复杂度**：`O(d·n)`  
  - 只存 `dp` 表，大小为 `(n+1) × (d+1)`，随 `n`、`d` 线性增长。

---

## 心得

- **核心技巧**：**动态规划 + 前缀/逆向最大值维护**，把「切分数组」的所有可能用状态转移压缩到多项式时间。  
- **适用的题型**  
  1. 把数组划分成 `k` 段，使每段的某种代价（最大值、最小值、和等）之和最小/最大（如 “Divide Array into K Subarrays”）。  
  2. 需要在顺序约束下做「分组」或「分配」的 DP（如 “Maximum Sum of a Subarray After K Operations”）。  
- **一句话总结**：**把「每一天的工作」看成「一次切分」并用 DP 记忆「前 i 项划了 k 天的最优」即可快速求最小难度**。

---

## 反思

- **第一反应**：看到「必须保持顺序」且「每一天至少一项」立即想到「把数组切成 d 段」的模型，随后想到递归暴力。  
- **最容易踩的坑**  
  1. **工作数不足天数**：`len(jobDifficulty) < d` 必须直接返回 `-1`，否则 DP 会产生无效状态。  
  2. **边界下标**：在 DP 转移时，`j` 必须保证前 `k-1` 天至少有 `k-1` 项工作，所以循环范围要写对（`j >= k-1`）。  
  3. **最大值维护**：如果每次都重新遍历 `j..i-1` 计算最大值，时间会退化到 `O(d·n³)`，一定要在逆向遍历时实时更新 `cur_max`。  
- **下次类似题的第一步**：先明确「划分」的数量（`k`）和「顺序」约束，定义 `dp[i][k]` 为「前 i 项划成 k 组」的最优值，然后思考 **如何在 O(1) 维护当前组的代价**（如最大值、最小值、和），再写出转移公式。这样就能快速搭建出最优 DP。