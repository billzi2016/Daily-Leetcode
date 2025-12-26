# #3469. **找出移除数组元素的最小成本** / Find Minimum Cost to Remove Array Elements

> 难度：中等 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/find-minimum-cost-to-remove-array-elements/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums. Your task is to remove all elements from the array by performing one of the following operations at each step until nums is empty:
Return the minimum cost required to remove all the elements.

**Examples**

**Example 1:**

```
Input: nums = [6,2,8,4]
Output: 12
Explanation:
Initially, nums = [6, 2, 8, 4] .
The cost to remove all elements is 8 + 4 = 12 . This is the minimum cost to remove all elements in nums . Hence, the output is 12.
```

**Example 2:**

```
Input: nums = [2,1,3,3]
Output: 5
Explanation:
Initially, nums = [2, 1, 3, 3] .
The cost to remove all elements is 2 + 3 = 5 . This is the minimum cost to remove all elements in nums . Hence, the output is 5.
```

**Constraints**

- 1 <= nums.length <= 1000
- 1 <= nums[i] <= 106

---

## 题目（中文翻译）

给定一个整数数组 `nums`。你的任务是通过在每一步对 `nums` 执行以下操作之一，直至数组为空，来移除数组中的所有元素。返回移除所有元素所需的最小成本。

#### 示例 1
**输入:** `nums = [6,2,8,4]`  
**输出:** `12`  
**解释:**  
最初，`nums = [6, 2, 8, 4]`。  
移除所有元素的成本为 `8 + 4 = 12`。这是移除 `nums` 中所有元素的最小成本。因此，输出为 `12`。

#### 示例 2
**输入:** `nums = [2,1,3,3]`  
**输出:** `5`  
**解释:**  
最初，`nums = [2, 1, 3, 3]`。  
移除所有元素的成本为 `2 + 3 = 5`。这是移除 `nums` 中所有元素的最小成本。因此，输出为 `5`。

#### 约束条件
- `1 <= nums.length <= 1000`
- `1 <= nums[i] <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目可以这样理解：  
> **一次操作** = 取当前数组的**最左边的一个非空前缀**（比如 `[a₁, a₂, …, a_k]`），把它一次性删掉，**费用**等于这个前缀里最大的数 `max(a₁…a_k)`。  
> 之后数组只剩下后面的部分，继续上述操作，直到数组空为止。  

最直接的想法就是**枚举所有可能的切分方式**，计算每一种切分得到的总费用，取最小值。  

> 类比：把数组想成一本书，**一次阅读**可以一次性读完书的前几页，费用是这几页中最长的那句话的字数。我们想把整本书读完的总字数最少，于是把所有可能的“先读几页”方式全部尝试一遍。

因为每一次都可以选任意长度的前缀，切分方式的数量随数组长度呈指数增长（类似把 n 本书切成若干段的划分），所以这种**暴力递归**的时间会非常大，甚至会超出递归深度。

#### 代码（Python）

```python
from functools import lru_cache
from typing import List

def minCost_bruteforce(nums: List[int]) -> int:
    n = len(nums)

    @lru_cache(maxsize=None)          # 记忆化，避免重复计算相同子问题
    def dfs(start: int) -> int:
        """返回从 start 开始（包括 start）到数组末尾的最小费用"""
        if start == n:                 # 已经删除完全部元素
            return 0

        best = float('inf')
        cur_max = -float('inf')
        # 枚举当前可以删除的前缀长度（从 1 到剩余全部）
        for end in range(start, n):
            cur_max = max(cur_max, nums[end])   # 前缀的最大值
            cost = cur_max + dfs(end + 1)       # 本次费用 + 剩余部分的最优费用
            best = min(best, cost)              # 取最小
        return best

    return dfs(0)


# 示例
print(minCost_bruteforce([6, 2, 8, 4]))   # 12
print(minCost_bruteforce([2, 1, 3, 3]))   # 5
```

> 关键行解释  
> - `@lru_cache`：把已经算好的子问题记下来，避免指数级的重复计算。  
> - `cur_max = max(cur_max, nums[end])`：在遍历前缀的过程中实时维护该前缀的最大值，省去每次 `max(nums[start:end+1])` 的 O(k) 代价。  
> - `cost = cur_max + dfs(end + 1)`：本次删除前缀的费用 + 剩余数组的最小费用。

#### 复杂度  

- **时间复杂度**：`O(2^n)`（指数级）。虽然用了记忆化，状态数仍是 `n`（起始位置），但每个状态内部仍要遍历所有可能的前缀长度，导致最坏情况下的递归树仍然呈指数增长。  
- **空间复杂度**：`O(n)`，递归栈深度最多 `n`，加上记忆化表存 `n` 条记录。

---

### 2. 最优解

#### 思路  

暴力解慢的根本原因是**每一次都从当前位置枚举所有可能的前缀长度**，导致大量的重复计算。  
我们可以把「从位置 `i` 开始的最小费用」记下来，利用**动态规划**一次性算出所有状态。

设 `dp[i]` 表示**删除子数组 `nums[i:]`（从 i 到末尾）所需的最小费用**。  
显然 `dp[n] = 0`（空数组不需要费用）。  

从 `i` 开始，我们可以选择任意 `j (i ≤ j < n)` 作为本次删除的前缀的结束位置，费用为该前缀的最大值 `max(nums[i..j])`，随后剩余的部分是 `nums[j+1:]`，费用为 `dp[j+1]`。于是得到递推式：

```
dp[i] = min_{j ≥ i} ( max(nums[i..j]) + dp[j+1] )
```

这就是 **区间 DP** 的典型写法。我们只需要在计算 `dp[i]` 时，**从左往右维护当前前缀的最大值**，就能在 O(1) 时间得到 `max(nums[i..j])`，整体时间变为 `O(n^2)`，空间 `O(n)`。

> 类比：把书的章节排成一行，每次从左边挑出若干连续章节阅读，费用是这几章中最长的那句。我们把「从第 i 章节开始阅读」的最小费用记下来，往后推导，就能一次算完所有章节的最优方案。

> 对于本题的约束 `n ≤ 1000`，`O(n^2)` 完全可以接受（约 10⁶ 次运算），不需要更高级的单调栈优化。

#### 代码（Python）

```python
from typing import List

def minCost_dp(nums: List[int]) -> int:
    n = len(nums)
    dp = [0] * (n + 1)          # dp[n] = 0 已经在初始化时完成

    # 从后往前计算 dp[i]
    for i in range(n - 1, -1, -1):
        cur_max = -float('inf')
        best = float('inf')
        # 枚举本次删除的前缀结束位置 j
        for j in range(i, n):
            cur_max = max(cur_max, nums[j])   # 实时维护前缀最大值
            best = min(best, cur_max + dp[j + 1])
        dp[i] = best

    return dp[0]


# 示例
print(minCost_dp([6, 2, 8, 4]))   # 12
print(minCost_dp([2, 1, 3, 3]))   # 5
```

> 关键行解释  
> - `for i in range(n - 1, -1, -1)`: 从右往左填表，因为 `dp[i]` 需要用到 `dp[j+1] (j ≥ i)`。  
> - `cur_max = max(cur_max, nums[j])`: 在同一个 `i` 的内部循环里，随着 `j` 向右移动，前缀最大值只会增大或保持不变，直接更新即可。  
> - `best = min(best, cur_max + dp[j + 1])`: 取所有可能切分点中费用最小的那一个。

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 外层遍历 `i` 共 `n` 次，内层遍历 `j` 最多 `n-i` 次，累计约 `n·(n+1)/2 ≈ n²/2` 次操作。  
  - 用“大白话”说，就是如果 `n=1000`，大约要做 **50 万** 次比较和加法，电脑在毫秒级就能完成。

- **空间复杂度**：`O(n)`  
  - 只用了长度为 `n+1` 的一维数组 `dp`，再加几个临时变量，空间开销和输入规模成线性关系。

---

## 心得

- **核心技巧**：把“从左边取一个前缀”抽象成 **区间动态规划**，并在遍历时**实时维护区间最大值**，把 O(1) 的信息重复利用，避免每次重新扫描区间。  
- **适用场景**：  
  1. “一次操作只能处理左端连续子数组，费用取该子数组的某种聚合函数（最大值、最小值、和等）”。  
  2. “把数组划分成若干段，使每段的代价满足某种函数，求总代价最小”。  
  3. 类似的 LeetCode 题目：  
     - **1468. 计算器使用成本**（每次取前缀求和）  
     - **1359. 有效的数组分割**（分割后每段满足条件）  

- **一句话总结**：  
  > “把所有可能的前缀切分抽象成 DP 状态，利用一次遍历维护区间最大值，即可在 O(n²) 里得到最小删除成本。”

---

## 反思

- **第一反应**：看到“每次只能删除前缀，费用是前缀最大值”，我立刻想到“枚举所有切分”。这自然导向了暴力递归。  
- **最容易踩的坑**：  
  1. **忘记实时更新前缀最大值**，每次都用 `max(nums[i:j+1])` 会把时间复杂度提升到 O(n³)。  
  2. **边界处理**：`dp[n]` 必须设为 0，表示空数组不产生费用。  
  3. **整数范围**：`nums[i] ≤ 10⁶`，累计费用可能达到 `10⁹`，使用 Python 的 `int` 没问题，但在语言有限制的情况下要注意使用 64 位整数。  

- **下次类似题的第一步**：  
  > “先把‘一次操作的代价’抽象成对某个区间的聚合函数（最大/最小/和），然后问‘把整个数组划分成若干段，使每段代价相加最小’，这几乎总是 DP 的雏形，先写出 `dp[i]` 的递推式，再考虑如何在遍历中把区间信息（最大值）高效维护。”