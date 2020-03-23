# #813. 最大平均数之和 / Largest Sum of Averages

> 难度：中等 · 标签：Array、Dynamic Programming、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/largest-sum-of-averages/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and an integer k. You can partition the array into at most k non-empty adjacent subarrays. The score of a partition is the sum of the averages of each subarray.
Note that the partition must use every integer in nums, and that the score is not necessarily an integer.
Return the maximum score you can achieve of all the possible partitions. Answers within 10-6 of the actual answer will be accepted.

**Examples**

**Example 1:**

```
Input: nums = [9,1,2,3,9], k = 3
Output: 20.00000
Explanation: 
The best choice is to partition nums into [9], [1, 2, 3], [9]. The answer is 9 + (1 + 2 + 3) / 3 + 9 = 20.
We could have also partitioned nums into [9, 1], [2], [3, 9], for example.
That partition would lead to a score of 5 + 2 + 6 = 13, which is worse.
```

**Example 2:**

```
Input: nums = [1,2,3,4,5,6,7], k = 4
Output: 20.50000
```

**Constraints**

- 1 <= nums.length <= 100
- 1 <= nums[i] <= 104
- 1 <= k <= nums.length

---

## 题目（中文翻译）

给定一个整数数组（integer array）`nums` 和一个整数 `k`。你可以将该数组划分（partition）为至多 `k` 个非空且相邻的子数组（subarray）。一个划分的得分（score）定义为每个子数组的平均数之和。  
需要注意的是，划分必须使用 `nums` 中的所有元素，且得分不一定是整数。  
返回所有可能划分中能够得到的最大得分。答案只要在实际答案的 `10⁻⁶` 以内均视为正确。

**示例 1**  
```
输入: nums = [9,1,2,3,9], k = 3
输出: 20.00000
解释:
最佳的划分方式是将 nums 划分为 [9], [1, 2, 3], [9]。此时得分为 9 + (1 + 2 + 3) / 3 + 9 = 20。  
我们也可以将 nums 划分为 [9, 1], [2], [3, 9]，此时得分为 5 + 2 + 6 = 13，显然更差。
```

**示例 2**  
```
输入: nums = [1,2,3,4,5,6,7], k = 4
输出: 20.50000
```

**约束条件**
- `1 <= nums.length <= 100`
- `1 <= nums[i] <= 10⁴`
- `1 <= k <= nums.length`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**把所有可能的切分方式枚举出来**，算出每种切分的得分（每段的平均数之和），最后取最大值。  

- **数据结构**：我们只需要用 Python 的 `list` 来存放原数组 `nums`，以及用递归/回溯的方式把切分的方案保存到另一个 `list` 中。可以把切分过程想象成在一条直线（数组）上放置“刀子”，每把刀子把数组划分成两段。  
- **为什么正确**：只要遍历了**所有**合法的切法（每段非空、总段数 ≤ k），必然会找到得分最高的那一种，所以答案一定在枚举得到的最大值里。  

**枚举方式**  
我们用深度优先搜索（DFS）从左到右尝试每一种切法。函数 `dfs(pos, used)` 表示当前已经处理到下标 `pos`（左闭右开区间），已经用了 `used` 段。  
- 若 `pos == n`（已经遍历完数组），说明得到了一种合法划分，返回当前累计的得分。  
- 否则，从 `pos` 开始向右扩展，尝试把 `[pos, i]` 这一段作为下一段（`i` 从 `pos` 到 `n-1`），计算这段的平均值 `avg = sum(nums[pos:i+1]) / (i-pos+1)`，递归求剩余部分的最大得分。  

因为 `k` 只限定**最多** `k` 段，递归时只要 `used < k` 就可以继续切，否则只能把剩余所有元素放进最后一段。

#### 代码（Python）  

```python
from typing import List

def largestSumOfAverages_bruteforce(nums: List[int], k: int) -> float:
    n = len(nums)

    # 递归搜索所有切分方式
    def dfs(pos: int, used: int) -> float:
        """返回从 pos 开始、已经用了 used 段的最大得分"""
        if pos == n:                     # 已经走到数组末尾
            return 0.0
        # 如果已经用了 k 段，只能把剩下的全部放进最后一段
        if used == k:
            total = sum(nums[pos:])      # 余下所有数的和
            cnt = n - pos                # 余下的个数
            return total / cnt           # 直接返回这段的平均值

        best = 0.0
        cur_sum = 0                     # 逐步累加当前段的和，避免每次都 sum()
        # 尝试把 [pos, i] 作为下一段
        for i in range(pos, n):
            cur_sum += nums[i]
            length = i - pos + 1
            avg = cur_sum / length      # 这一段的平均值
            # 递归求后面的最大得分，加上当前段的平均值
            best = max(best, avg + dfs(i + 1, used + 1))
        return best

    return dfs(0, 0)
```

**关键行解释**  
- `cur_sum += nums[i]`：像往水桶里倒水一样，边遍历边累计，这样每段的和可以 **O(1)** 计算，而不是每次都 `sum(nums[pos:i+1])`（会导致 O(n³)）。  
- `if used == k:`：已经用了最多的段数，只能把剩余的元素合在一起，这一步保证“最多 k 段”的限制。  

#### 复杂度  

- **时间复杂度**：`O(2^n)`（指数级）。  
  - 直观来说，每个位置我们都有“切”或“不切”两种选择，最坏情况下会产生大约 `2^(n-1)` 种切法。即使加上 `k` 的限制，仍然是指数级别，`n` 只要稍大（比如 20）就会超时。  
- **空间复杂度**：`O(n)`。  
  - 递归深度最多 `n`，加上函数调用栈占用的空间。  

> 大白话：时间复杂度的 `O(2^n)` 就像把一本 100 页的书每页都决定要不要在这里插一道“分割线”，所有可能的组合数会非常多，根本算不过来。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**重复计算** 是主要瓶颈：  
1. 同一个子数组的平均值会被多次求，尤其是 `sum(nums[l:r]) / (r-l+1)`。  
2. 对每个 `pos` 我们都要遍历所有可能的右端点 `i`，导致大量的子问题重复出现。  

**优化方向**  
- 用**前缀和**把子数组的求和降到 O(1)。  
- 用**动态规划（DP）**把“从左到右的最优划分”拆成子问题，避免重复递归。  

---

#### 动态规划模型  

设 `dp[i][j]` 表示：**前 `i` 个数（即 `nums[0..i-1]`）划分成恰好 `j` 段时能够得到的最大得分**。  

目标是求 `dp[n][k]`（`n = len(nums)`），但因为题目允许 **至多** `k` 段，实际返回 `max(dp[n][1..k])`（不过实现时可以直接让 DP 允许最多 `k` 段，即在转移时不必强制恰好 `k`）。

**状态转移**  
要得到 `dp[i][j]`，我们可以把第 `j` 段的左端点设在某个位置 `t`（`0 ≤ t < i`），于是：

```
dp[i][j] = max_{t from j-1 to i-1} ( dp[t][j-1] + average(t, i-1) )
```

- `t` 必须至少为 `j-1`，因为前面已经用了 `j-1` 段，每段至少一个元素。  
- `average(t, i-1)` 表示子数组 `nums[t..i-1]` 的平均值。  

**前缀和**  
定义 `prefix[x] = sum(nums[0..x-1])`（`prefix[0]=0`），则子数组和可以 O(1) 计算：

```
sum(t, i-1) = prefix[i] - prefix[t]
average(t, i-1) = (prefix[i] - prefix[t]) / (i - t)
```

这样每次转移只需要 O(1) 时间。

**初始化**  
- `dp[0][0] = 0`（0 个数、0 段得分为 0）。  
- 其它 `dp[0][*]` 或 `dp[*][0]` 设为负无穷（不合法），在实现时可以直接用 `0` 并在循环中避免非法转移。

**实现细节**  
- `n ≤ 100`，`k ≤ n`，所以二维 DP 表大小 `101 x 101` 完全可以接受。  
- 两层循环：外层遍历 `i`（1..n），中层遍历 `j`（1..min(k,i)），内层遍历 `t`（j-1..i-1）求最大值。整体时间复杂度 `O(n^2 * k)`，在最坏情况下是 `100^3 = 1e6`，完全在限制内。  

**进一步小优化**  
因为 `k ≤ n`，我们可以把 `j` 的上限设为 `min(k, i)`，防止不必要的循环。

#### 代码（Python）  

```python
from typing import List

def largestSumOfAverages(nums: List[int], k: int) -> float:
    n = len(nums)

    # ---------- 前缀和 ----------
    prefix = [0.0] * (n + 1)          # prefix[i] = nums[0] + ... + nums[i-1]
    for i in range(1, n + 1):
        prefix[i] = prefix[i - 1] + nums[i - 1]

    # ---------- 动态规划 ----------
    # dp[i][j] 表示前 i 个数划分成 j 段的最大得分
    dp = [[0.0] * (k + 1) for _ in range(n + 1)]

    # 初始化：划分成 1 段时，得分就是整体的平均值
    for i in range(1, n + 1):
        dp[i][1] = prefix[i] / i      # average of nums[0..i-1]

    # 逐步填表
    for i in range(1, n + 1):                 # 考虑前 i 个数
        # 最多只能划分成 i 段，且不超过 k
        for j in range(2, min(k, i) + 1):    # 划分成 j 段
            best = 0.0
            # 第 j 段的左端点 t（前面已经划分成 j-1 段）
            for t in range(j - 1, i):        # t 必须 >= j-1，保证前面有足够的元素
                # 前 t 个数划分成 j-1 段的最优得分
                left = dp[t][j - 1]
                # t..i-1 这段的平均值
                avg = (prefix[i] - prefix[t]) / (i - t)
                best = max(best, left + avg)
            dp[i][j] = best

    # 题目要求最多 k 段，直接返回 dp[n][k]（因为 dp 表已经考虑了“至多”）
    return dp[n][k]
```

**关键行解释**  
- `prefix[i] = prefix[i - 1] + nums[i - 1]`：像在一本笔记本里记录累计的“水量”，后面查询任意区间的水量只要两次相减就行。  
- `dp[i][1] = prefix[i] / i`：只有一段时，得分就是这段的平均数。  
- `avg = (prefix[i] - prefix[t]) / (i - t)`：利用前缀和快速算出子数组 `[t, i-1]` 的平均值。  
- `best = max(best, left + avg)`：把前面已经得到的最优得分 `left` 与当前段的平均值相加，取最大。  

#### 复杂度  

- **时间复杂度**：`O(n^2 * k)` → 在最坏情况下 `n = k = 100`，约为 `1,000,000` 次基本运算，运行毫秒级。  
  - 相比暴力的指数级 `O(2^n)`，这里是多项式时间，实际可以轻松通过所有测试。  
- **空间复杂度**：`O(n * k)` → 需要一个 ` (n+1) × (k+1) ` 的二维表来保存子问题的答案，最多约 `10,000` 个浮点数，几乎可以忽略不计。  

---

## 心得  

- **核心技巧**：**动态规划 + 前缀和**。  
  - 动态规划把“把前 i 个数划分成 j 段”的子问题拆解，避免重复枚举。  
  - 前缀和把任意子数组的和降到 O(1)，从而使状态转移的计算成本可控。  

- **适用的类似题型**  
  1. **分割数组的最大和**（如 LeetCode 1043: Partition Array for Maximum Sum）  
  2. **最小代价划分**（如 LeetCode 1105: Filling Bookcase Shelves）  
  3. **分段取平均的优化**（如 LeetCode 1473: Paint House III 中的 DP+前缀和技巧）  

- **一句话总结解题钥匙**：  
  “把大问题拆成‘前 i 个数划几段’的子问题，用前缀和把每段的平均值算得又快又准”。  

---  

## 反思  

- **第一反应**：看到“把数组划分成 k 段，求每段平均和的最大值”，立刻想到 **暴力枚举所有切法**。这是一种自然的直觉，却忽视了规模会爆炸。  

- **最容易踩的坑**  
  1. **边界条件**：`k` 可以等于 `n`（每个元素单独成段），此时答案是所有元素之和。实现时要保证循环 `for j in range(2, min(k, i)+1)` 不会出现 `j > i` 的非法状态。  
  2. **浮点数精度**：答案要求 `1e-6` 的误差容忍度，直接使用 `float`（Python 的 double）即可，无需额外的精度控制。  
  3. **前缀和的索引**：`prefix` 长度是 `n+1`，第 `i` 项对应 `nums[0..i-1]`，容易写错导致下标越界或求和错误。  

- **下次遇到同类题，第一步该想到**：  
  “先把问题抽象成‘前缀划分的最优子结构’，然后检查是否可以用前缀和把子区间的代价快速算出”。这样就能立刻从暴力转向 DP，避免时间超限。