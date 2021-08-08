# #1425. 受约束的子序列和 / Constrained Subsequence Sum

> 难度：困难 · 标签：Array、Dynamic Programming、Queue、Sliding Window、Heap (Priority Queue)、Monotonic Queue · [LeetCode 链接](https://leetcode.com/problems/constrained-subsequence-sum/)

---

## 题目（英文原版）

**Description**

Given an integer array nums and an integer k, return the maximum sum of a non-empty subsequence of that array such that for every two consecutive integers in the subsequence, nums[i] and nums[j], where i < j, the condition j - i <= k is satisfied.
A subsequence of an array is obtained by deleting some number of elements (can be zero) from the array, leaving the remaining elements in their original order.

**Examples**

**Example 1:**

```
Input: nums = [10,2,-10,5,20], k = 2
Output: 37
Explanation: The subsequence is [10, 2, 5, 20].
```

**Example 2:**

```
Input: nums = [-1,-2,-3], k = 1
Output: -1
Explanation: The subsequence must be non-empty, so we choose the largest number.
```

**Example 3:**

```
Input: nums = [10,-2,-10,-5,20], k = 2
Output: 23
Explanation: The subsequence is [10, -2, -5, 20].
```

**Constraints**

- 1 <= k <= nums.length <= 105
- -104 <= nums[i] <= 104

---

## 题目（中文翻译）

给定一个整数数组 `nums` 和一个整数 `k`，返回该数组中 **非空子序列（subsequence）** 的最大和，要求子序列中任意两个相邻元素 `nums[i]` 与 `nums[j]`（其中 `i < j`）满足 `j - i ≤ k`。

子序列是通过删除数组中的若干元素（可以为零）得到的，剩余元素保持原来的顺序。

### 示例

#### 示例 1
Input: `nums = [10,2,-10,5,20]`, `k = 2`  
Output: `37`  
Explanation: 子序列为 `[10, 2, 5, 20]`。

#### 示例 2
Input: `nums = [-1,-2,-3]`, `k = 1`  
Output: `-1`  
Explanation: 子序列必须非空，因此选择最大的那个数。

#### 示例 3
Input: `nums = [10,-2,-10,-5,20]`, `k = 2`  
Output: `23`  
Explanation: 子序列为 `[10, -2, -5, 20]`。

### 约束条件
- `1 ≤ k ≤ nums.length ≤ 10^5`
- `-10^4 ≤ nums[i] ≤ 10^4`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：**对每一个位置 i，枚举它前面至多 k 步的所有合法前驱 j，找出能得到的最大子序列和**。  

- **数据结构**：我们只需要一个一维数组 `dp`，`dp[i]` 表示“以 `nums[i]` 为结尾的合法子序列的最大和”。可以把 `dp` 想象成一本记账本，记下每个位置如果选上它，手里能拿到的最大钱。  
- **为什么正确**：  
  - 子序列的定义要求相邻两个选中的下标之差 ≤ k。  
  - 若我们已经知道所有 `j`（`i‑k ≤ j < i`）的 `dp[j]`，那么把 `nums[i]` 接在这些子序列后面仍然合法，和就是 `dp[j] + nums[i]`。  
  - 为了得到“最大”，只要在这些候选和里挑最大的，再和 `0` 比较（因为可以把 `nums[i]` 当成新序列的第一个元素），得到 `dp[i]` 的最优值。  

- **时间/空间复杂度**：  
  - 对每个 `i` 要检查至多 `k` 个前驱，最坏情况是 `k ≈ n`，于是时间复杂度是 **O(n·k)**，在最坏情况下等价于 **O(n²)**。  
  - `dp` 长度为 `n`，额外只用了常数级的临时变量，空间复杂度是 **O(n)**。  
  - **大白话**：`O(n²)` 就像你要把 10,000 本书两两配对检查，次数会是 100 百万次，显然太慢了。

#### 代码（Python）

```python
from typing import List

def constrained_subsequence_sum_bruteforce(nums: List[int], k: int) -> int:
    n = len(nums)
    # dp[i] 表示「以 i 为结尾的合法子序列的最大和」
    dp = [0] * n
    ans = -10**9                     # 题目要求非空，先设一个很小的初始值

    for i in range(n):
        # 先把自己单独拿出来（相当于前面没有合法前驱）
        best = nums[i]

        # 枚举 i 前面最多 k 步的所有前驱 j
        for j in range(max(0, i - k), i):
            # 如果 dp[j] 为负数，接在后面会更差，直接舍弃
            best = max(best, nums[i] + dp[j])

        dp[i] = best
        ans = max(ans, best)        # 维护全局最大

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n·k)`。如果 `k` 与 `n` 同阶，则相当于 `O(n²)`，即遍历每个元素时都要检查几乎所有前面的元素。  
- **空间复杂度**：`O(n)`。只用了 `dp` 一个长度为 `n` 的数组，额外常数空间。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于每次都要在 `[i‑k, i‑1]` 这段窗口里找最大的 `dp`**。如果我们能**在 O(1) 时间内得到窗口最大值**，整体就可以降到 O(n)。  

这正是 **单调队列（Monotonic Queue）** 能帮忙的地方。思路分三步：

1. **动态规划公式**  
   - 与暴力解相同，设 `dp[i] = nums[i] + max(0, max{dp[j] | i‑k ≤ j < i})`。  
   - 这里的 `max{dp[j]}` 就是窗口 `[i‑k, i‑1]` 的最大值。

2. **维护窗口最大值**  
   - 使用一个双端队列 `dq`，队首保存当前窗口的最大 `dp` 的下标。  
   - 当我们把新的 `dp[i]` 加入时，**把队尾所有小于 `dp[i]` 的下标弹出**，因为它们再也不可能成为以后窗口的最大值（`dp[i]` 更大且更靠右）。  
   - 同时，**如果队首的下标已经不在窗口范围（< i‑k）**，就把它弹出。这样队首永远是窗口内的最大值。

3. **计算答案**  
   - `dp[i] = nums[i] + max(0, dp[dq[0]])`（如果 `dq` 为空，说明窗口里没有正贡献，直接取 `0`）。  
   - 同时更新全局答案 `ans = max(ans, dp[i])`。

**类比**：想象你在排队买咖啡，每个人的咖啡价值是 `dp`。你只关心最近 `k` 个人中价值最高的那位。单调队列就像一个“只保留最高价值的窗口”，把价值低的“赶走”，让查询最高价值只需要看队首。

#### 代码（Python）

```python
from collections import deque
from typing import List

def constrained_subsequence_sum(nums: List[int], k: int) -> int:
    n = len(nums)
    dp = [0] * n                # dp[i] 同上
    dq = deque()                # 存放下标，dp 值单调递减
    ans = -10**9                # 全局最大答案

    for i in range(n):
        # 1）窗口左边界：i - k
        while dq and dq[0] < i - k:
            dq.popleft()        # 把已经离开窗口的下标踢出去

        # 2）当前窗口的最大 dp（如果 dq 为空说明没有正贡献）
        max_prev = dp[dq[0]] if dq else 0
        dp[i] = nums[i] + max(0, max_prev)

        # 3）更新答案
        ans = max(ans, dp[i])

        # 4）把 dp[i] 加入单调队列
        #   把队尾所有 dp 值 < dp[i] 的下标都弹出，保持递减
        while dq and dp[dq[-1]] <= dp[i]:
            dq.pop()
        dq.append(i)            # 把当前下标加入队尾

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n)`。每个下标至多进队一次、出队一次，所有操作累计是线性时间。相比暴力的 `O(n·k)`，快了几个数量级。  
- **空间复杂度**：`O(n)`（`dp` 数组）+ `O(k)`（队列最多保存 `k` 个元素），总体仍是线性空间。  

---  

## 心得  

- **核心技巧**：**在 DP 中用单调队列维护滑动窗口的最大值**。  
- **适用题型**：  
  1. “**滑动窗口最大值**” 类题（LeetCode 239）。  
  2. “**带限制的子序列和**” 或 “**带限制的递增子序列**”。  
  3. “**最大子数组和且长度受限**” 等需要在固定窗口内取极值的 DP。  
- **一句话总结**：**把 “找窗口最大值” 这一步交给单调队列，DP 就能跑到 O(n)。**  

## 反思  

- **第一反应**：看到 “相邻下标差 ≤ k”，立刻想到 “窗口”。于是写出 `dp[i] = nums[i] + max(dp[j])` 的递推式。  
- **最容易踩的坑**：  
  - **负数处理**：子序列必须非空，若所有数都是负的，答案是最大的单个元素，而不是 0。要在递推式里 `max(0, …)` 并在全局答案里保留负数。  
  - **窗口边界**：忘记在把新下标加入队列前先弹出已超出左边界的下标，会导致错误的最大值。  
  - **单调队列的“≤” vs “<”**：若使用 `<=` 把等值也弹出，可保持队列更短；但若只弹出 `<`，等值会保留，仍正确，只是可能占用更多空间。  
- **下次第一步**：看到 “在每个位置只和前面 k 个位置有关”，立刻想到 **滑动窗口 + 单调结构**（单调队列 / 堆）来把 “取最大/最小” 降到 O(1)。这样可以把大多数 O(n·k) 的 DP 优化到 O(n)。