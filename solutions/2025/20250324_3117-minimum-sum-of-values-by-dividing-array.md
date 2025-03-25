# #3117. 划分数组后子数组值的最小和 / Minimum Sum of Values by Dividing Array

> 难度：困难 · 标签：Array、Binary Search、Dynamic Programming、Bit Manipulation、Segment Tree、Queue · [LeetCode 链接](https://leetcode.com/problems/minimum-sum-of-values-by-dividing-array/)

---

## 题目（英文原版）

**Description**

You are given two arrays nums and andValues of length n and m respectively.
The value of an array is equal to the last element of that array.
You have to divide nums into m disjoint contiguous subarrays such that for the ith subarray [li, ri], the bitwise AND of the subarray elements is equal to andValues[i], in other words, nums[li] & nums[li + 1] & ... & nums[ri] == andValues[i] for all 1 <= i <= m, where & represents the bitwise AND operator.
Return the minimum possible sum of the values of the m subarrays nums is divided into. If it is not possible to divide nums into m subarrays satisfying these conditions, return -1.

**Examples**

**Example 1:**

```
Input: nums = [1,4,3,3,2], andValues = [0,3,3,2]
Output: 12
Explanation:
The only possible way to divide nums is:
The sum of the values for these subarrays is 4 + 3 + 3 + 2 = 12 .
```

**Example 2:**

```
Input: nums = [2,3,5,7,7,7,5], andValues = [0,7,5]
Output: 17
Explanation:
There are three ways to divide nums :
The minimum possible sum of the values is 17 .
```

**Example 3:**

```
Input: nums = [1,2,3,4], andValues = [2]
Output: -1
Explanation:
The bitwise AND of the entire array nums is 0 . As there is no possible way to divide nums into a single subarray to have the bitwise AND of elements 2 , return -1 .
```

**Constraints**

- 1 <= n == nums.length <= 104
- 1 <= m == andValues.length <= min(n, 10)
- 1 <= nums[i] < 105
- 0 <= andValues[j] < 105

---

## 题目（中文翻译）

你得到两个数组 `nums` 与 `andValues`，长度分别为 `n` 和 `m`。  
数组的 **值** 定义为该数组的最后一个元素。  
你需要把 `nums` 划分为 `m` 个互不重叠的连续子数组，使得第 `i` 个子数组 `[l_i, r_i]` 的所有元素的按位与（bitwise AND）等于 `andValues[i]`，即  

```
nums[l_i] & nums[l_i + 1] & ... & nums[r_i] == andValues[i]   (1 ≤ i ≤ m)
```

其中 `&` 表示按位与运算符。  

返回划分后的 `m` 个子数组的 **值** 的最小可能和。如果不存在满足条件的划分方式，返回 `-1`。

---

### 示例

**示例 1**  
Input: `nums = [1,4,3,3,2]`, `andValues = [0,3,3,2]`  
Output: `12`  
Explanation:  
唯一可行的划分方式是  
```
[1,4] , [3] , [3] , [2]
```
对应的子数组值分别为 `4, 3, 3, 2`，总和为 `4 + 3 + 3 + 2 = 12`。

**示例 2**  
Input: `nums = [2,3,5,7,7,7,5]`, `andValues = [0,7,5]`  
Output: `17`  
Explanation:  
共有三种划分方式，其中最小的子数组值之和为 `17`。

**示例 3**  
Input: `nums = [1,2,3,4]`, `andValues = [2]`  
Output: `-1`  
Explanation:  
整个数组 `nums` 的按位与为 `0`，无法划分成仅一个子数组且其按位与等于 `2`，因此返回 `-1`。

---

### 约束条件

- `1 <= n == nums.length <= 10^4`
- `1 <= m == andValues.length <= min(n, 10)`
- `1 <= nums[i] < 10^5`
- `0 <= andValues[j] < 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法就是把 `nums` 的所有可能的 **连续划分** 都枚举一遍，然后检查每一段的 **按位与** 是否等于对应的 `andValues[i]`，若全部满足则把每段的 **最后一个元素** 加起来求和，取所有合法划分中的最小值。  

- **枚举划分**：把 `n` 个元素切成 `m` 段，就像把一根绳子在 `m‑1` 个位置剪断。  
- **按位与**：把一段里的所有数字逐位相“与”。可以把它想象成把每个数字写成二进制，然后同一位上只要有一个是 0，结果那一位就是 0。  
- **最后一个元素**：这段的“价值”就是这段最右边的数字。  

只要把所有切法全部列出来，逐个验证，就一定能得到答案（如果有的话）。  

#### 代码（Python）  
```python
from itertools import combinations
from typing import List

def brute(nums: List[int], and_vals: List[int]) -> int:
    n, m = len(nums), len(and_vals)
    if m > n:                     # 不可能把 n 个数分成更多段
        return -1

    best = float('inf')
    # 选取 m-1 个切点（下标），切点之间必须保持递增
    for cuts in combinations(range(1, n), m - 1):
        cuts = (0,) + cuts + (n,)          # 在两端各加上 0、n 方便切分
        ok = True
        cur_sum = 0
        for i in range(1, len(cuts)):
            l, r = cuts[i-1], cuts[i]      # 子数组是 nums[l:r]，左闭右开
            # 计算 AND
            cur_and = nums[l]
            for x in nums[l+1:r]:
                cur_and &= x
            if cur_and != and_vals[i-1]:
                ok = False
                break
            cur_sum += nums[r-1]           # 价值是子数组的最后一个元素
        if ok:
            best = min(best, cur_sum)

    return best if best != float('inf') else -1
```

> **关键行解释**  
> - `combinations(range(1, n), m - 1)`: 从 `1..n-1` 中挑出 `m-1` 个切点，等价于把绳子剪 `m-1` 次。  
> - `cur_and &= x`: “按位与”就像把两张纸叠在一起，只要有一张纸的对应位是洞（0），最终的洞就会出现。  
> - `cur_sum += nums[r-1]`: 取子数组的最右边元素作为价值。  

#### 复杂度  
- **时间复杂度**：`O(C(n-1, m-1) * n)`  
  - `C(n-1, m-1)` 是组合数，表示所有切法的数量，随着 `n` 的增大呈指数级增长。  
  - 对每一种切法我们还要遍历子数组求 AND，最坏要遍历全部 `n` 个元素。  
  - 用大白话讲，就是“几乎要把所有可能的划分都试一遍”，在 `n=10⁴` 时根本跑不完。  
- **空间复杂度**：`O(1)`（不计输入数组本身）  
  - 只用了常数级别的额外变量。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在 **枚举所有切点**，导致指数级时间。  
我们需要 **动态规划**（DP）把子问题的答案记下来，避免重复计算。  

---

**① 用 DP 表示子问题**  
设 `dp[i][j]` 为：  
> 前 `i`（即 `nums[0..i-1]`）个元素，已经划分成前 `j` 段（对应 `andValues[0..j-1]`）时，**价值和的最小可能值**。  

目标是 `dp[n][m]`（全部 `n` 个数、全部 `m` 段）。  

转移方程的核心是：  
```
dp[i][j] = min{ dp[k][j-1] + nums[i-1] }   (k < i 且 nums[k..i-1] 的 AND = andValues[j-1])
```
也就是说，第 `j` 段的右端一定是 `i-1`，左端可以是任意合法的 `k`（`k` 为这段的起始下标），只要这段的 **按位与** 等于 `andValues[j-1]`。  
`dp[k][j-1]` 已经是把前面 `k` 个元素划分好 `j-1` 段的最小价值和，**再加上第 `j` 段的价值**（它就是该段最右边的元素 `nums[i-1]`），就得到一种完整划分的价值和。我们在所有合法的 `k` 中取最小即可。

---

**② 如何快速得到合法的 `k` 区间？**  

把指针从左向右扫过数组，维护 **滑动窗口的 AND**：

- 当我们把窗口左端向左扩展时，`AND` 只会 **变小或保持不变**（因为更多的数字参与 “与”，只会把 1 位变成 0，永不把 0 变成 1）。  
- 这意味着对于固定的右端 `i-1`，**满足 `AND = target` 的左端** 形成一个 **连续区间** `[L, R]`（`L ≤ R`），其中  
  - `L` 是最左侧还能得到 `target` 的位置（**最长** 子数组），  
  - `R` 是最右侧还能得到 `target` 的位置（**最短** 子数组）。  

我们可以用 **双指针**（或二分）一次遍历算出每个 `i` 对应的 `[L,R]`。  
实现思路（双指针）：

```text
left = i-1
cur_and = nums[i-1]
while left >= 0 and (cur_and & nums[left]) == target:
    cur_and &= nums[left]
    left -= 1
# 此时 left+1 .. i-1 是最长满足 target 的子数组
# 再继续往左，只要 cur_and == target，就是更短的合法子数组
```

因为 `m ≤ 10`，我们可以对每个 `j`（即每个目标 `target = andValues[j-1]`）单独跑一次，这总共是 `O(n*m)`。

---

**③ 在 `[L,R]` 区间里取最小的 `dp[k][j-1]`**  

转移式需要 `min{ dp[k][j-1] } (k ∈ [L, R])`。  
这正是 **滑动窗口最小值** 问题：随着 `i` 从左到右移动，窗口 `[L,R]` 只会向右“滑动”。  

**单调队列（Monotonic Queue）** 可以在 **均摊 O(1)** 时间内维护窗口最小值：

- 队列里保存 **候选下标**，下标对应的 `dp` 值单调递增（队首始终是最小值）。  
- 当窗口右端 `i` 增大时，把 `dp[i][j-1]` 加入队列，同时弹出比它大的所有尾部元素（因为它们永远不会成为最小值）。  
- 当左端 `L` 超出窗口时，把队首的下标弹出。  

这样，在每一步我们都能 **O(1)** 取到 `min(dp[L..R][j-1])`，整体 DP 变成 `O(n*m)`。

---

**④ 完整流程**  

1. 初始化 `dp[0][0] = 0`，其余为正无穷。  
2. 对每个子数组目标 `t = andValues[j-1]`（`j = 1..m`）  
   - 用双指针/滑动窗口求出每个右端 `i` 对应的合法左端区间 `[L_i, R_i]`（若不存在则设为空）。  
   - 同时用单调队列维护 `dp[*][j-1]` 在当前窗口的最小值。  
   - 根据最小值更新 `dp[i][j] = min_in_window + nums[i-1]`。  
3. 最后返回 `dp[n][m]`，若仍是正无穷则返回 `-1`。  

因为 `m ≤ 10`，我们可以把 `dp` 作为二维列表 `dp = [[inf]*(m+1) for _ in range(n+1)]`，空间 `O(n*m)` 完全可接受。

---

#### 代码（Python）  

```python
from collections import deque
from typing import List

INF = 10**18          # 足够大的正数，代表“不可能”

def minimum_sum(nums: List[int], and_vals: List[int]) -> int:
    n, m = len(nums), len(and_vals)
    if m > n:                         # 子数组数大于元素数，直接不可能
        return -1

    # dp[i][j] : 前 i 个元素划分成前 j 段的最小价值和
    dp = [[INF] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 0

    # 对每一段的目标 AND 依次处理
    for j in range(1, m + 1):
        target = and_vals[j - 1]

        # 下面的两个数组记录每个右端 i（1-indexed）对应的合法左端区间 [L,R]
        L = [0] * (n + 1)   # 最左（最长子数组的左端）
        R = [0] * (n + 1)   # 最右（最短子数组的左端），若不存在则 L>R

        # -------- 计算 L[i] 与 R[i]（双指针） ----------
        left = 0            # 当前窗口左端（0-indexed）
        cur_and = (1 << 20) - 1   # 先设为全 1（因为 nums[i] < 1e5 < 2^17）
        for i in range(1, n + 1):   # i 为右端的 1-indexed 位置
            # 把新元素 nums[i-1] 加入窗口
            cur_and &= nums[i - 1]

            # 确保窗口 AND 不低于 target（因为 AND 只会下降）
            while left < i and (cur_and & target) != target:
                # 移出左端元素，重新计算窗口 AND
                cur_and |= ~nums[left]   # 把左端位恢复为 1（相当于撤销 &）
                left += 1

            # 此时 [left, i) 的 AND 已经 >= target
            # 再向左扩展，找到最左端还能保持恰好等于 target 的位置
            l = left
            cur = cur_and
            while l > 0:
                nxt = cur & nums[l - 1]
                if nxt != target:
                    break
                cur = nxt
                l -= 1
            L[i] = l                # 最左端（最长）

            # 再找最右端（最短），即从 i 向左最靠近 i 的位置仍等于 target
            r = i - 1
            cur = nums[i - 1]
            while r > left:
                nxt = cur & nums[r - 1]
                if nxt != target:
                    break
                cur = nxt
                r -= 1
            R[i] = r                # 最右端（最短）

        # -------- 用单调队列在窗口上取最小 dp --------
        mono = deque()               # 保存下标 k，dp[k][j-1] 单调递增
        # 先把 dp[0][j-1] 放进队列，方便处理 i=1 时的窗口
        mono.append(0)

        for i in range(1, n + 1):
            # 1. 把 dp[i-1][j-1] 加入单调队列（准备给后面的窗口使用）
            val = dp[i - 1][j - 1]
            while mono and dp[mono[-1]][j - 1] >= val:
                mono.pop()
            mono.append(i - 1)

            # 2. 窗口左端应该是 L[i]，右端是 R[i]
            #   移除所有下标 < L[i]（已经不在窗口）
            while mono and mono[0] < L[i]:
                mono.popleft()

            #   如果当前窗口合法（L <= R），取队首的最小值
            if L[i] <= R[i] and mono:
                best_prev = dp[mono[0]][j - 1]
                dp[i][j] = best_prev + nums[i - 1]   # 价值是子数组最后一个元素

    ans = dp[n][m]
    return ans if ans < INF else -1
```

> **代码要点注释**  
> - `cur_and &= nums[i - 1]`：把新来的元素加入窗口，按位与会只能让位数变小。  
> - `while left < i and (cur_and & target) != target:`：如果当前窗口的 AND 已经比目标更小，就把左端往右搬，恢复被 “与” 掉的 1 位（通过 `|= ~nums[left]` 实现）。这一步确保窗口的 AND **不低于** `target`。  
> - `L[i]` 与 `R[i]` 的求法本质是 **向左扩展**，因为 AND 只会下降，找到第一次下降到不等于 `target` 的位置。  
> - `mono`（单调队列）里始终保存 **从左到右 dp 值递增** 的下标，队首就是当前窗口的最小值。加入新元素时把比它大的都弹出，左端移出时把对应下标弹出。这样每次取最小值都是 `O(1)`。  

#### 复杂度  
- **时间复杂度**：`O(n * m)`  
  - 对每个 `j`（最多 10 次），我们遍历一遍 `nums`，每个元素的指针只左移或右移一次，单调队列的操作均摊为 `O(1)`。  
  - 与暴力的指数级相比，现在只需要线性乘以 `m`，在 `n ≤ 10⁴`、`m ≤ 10` 的限制下轻松跑完。  
- **空间复杂度**：`O(n * m)`  
  - DP 表占 ` (n+1) * (m+1) ` 个整数，`m` 最多 10，最多约 `10⁵` 个，完全可以接受。  
  - 额外的 `L,R`、单调队列只需要 `O(n)` 辅助空间。  

---

## 心得  

- **核心技巧**：**区间 DP + 单调队列**（滑动窗口最小值）。  
- **适用场景**  
  1. 需要把数组划分成若干段，每段满足某种“可递增/递减”约束（如 AND、OR、最大值 ≤ X 等），且每段的代价只与右端元素有关。  
  2. DP 转移式出现 **在一个连续区间里取最小/最大** 的情况，常用 **单调队列** 或 **线段树** 优化。  
- **一句话总结**：把“枚举所有切点”改成“在每个右端只看最近的合法左端区间”，并用单调队列把区间最小值压到 O(1)，即可把指数时间降到线性。  

---

## 反思  

- **第一反应**：看到“把数组划分成 m 段，要求每段的 AND 等于给定值”，本能想到 **枚举切点**（暴力）或者 **递归回溯**。这很直观，但很快会发现 `n` 最大 10⁴ 时根本不可行。  
- **最容易踩的坑**  
  1. **AND 的单调性**：忘记 AND 只会变小，导致区间寻找写成两端都要二分，代码复杂且容易出错。  
  2. **窗口左端的更新**：在维护 `cur_and` 时，需要把左端移出时“恢复”被 & 掉的位，否则会把 AND 错算得过小。  
  3. **单调队列的边界**：如果窗口为空却仍尝试取队首，会导致错误答案或索引越界。必须在 `L[i] <= R[i]` 且队列非空时才更新 `dp[i][j]`。  
- **下次遇到类似题**：  
  1. 先确认 **子数组属性的单调性**（AND、OR、最大值、最小值等），这决定是否可以用双指针/滑动窗口。  
  2. 写出 **区间 DP** 的转移式，看看是否需要在一个连续区间里取最值。  
  3. 若需要，立刻考虑 **单调队列**（线性）或 **线段树**（对数）来优化。这样就能从“枚举所有可能”直接跳到 “线性/对数时间”。