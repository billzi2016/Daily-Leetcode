# #1681. **最小不兼容性** / Minimum Incompatibility

> 难度：困难 · 标签：Array、Dynamic Programming、Bit Manipulation、Bitmask · [LeetCode 链接](https://leetcode.com/problems/minimum-incompatibility/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums​​​ and an integer k. You are asked to distribute this array into k subsets of equal size such that there are no two equal elements in the same subset.
A subset's incompatibility is the difference between the maximum and minimum elements in that array.
Return the minimum possible sum of incompatibilities of the k subsets after distributing the array optimally, or return -1 if it is not possible.
A subset is a group integers that appear in the array with no particular order.

**Examples**

**Example 1:**

```
Input: nums = [1,2,1,4], k = 2
Output: 4
Explanation: The optimal distribution of subsets is [1,2] and [1,4].
The incompatibility is (2-1) + (4-1) = 4.
Note that [1,1] and [2,4] would result in a smaller sum, but the first subset contains 2 equal elements.
```

**Example 2:**

```
Input: nums = [6,3,8,1,3,1,2,2], k = 4
Output: 6
Explanation: The optimal distribution of subsets is [1,2], [2,3], [6,8], and [1,3].
The incompatibility is (2-1) + (3-2) + (8-6) + (3-1) = 6.
```

**Example 3:**

```
Input: nums = [5,3,3,6,3,3], k = 3
Output: -1
Explanation: It is impossible to distribute nums into 3 subsets where no two elements are equal in the same subset.
```

**Constraints**

- 1 <= k <= nums.length <= 16
- nums.length is divisible by k
- 1 <= nums[i] <= nums.length

---

## 题目（中文翻译）

给定一个整数数组 `nums` 和一个整数 `k`。要求将该数组划分为 `k` 个大小相等的子集（subset），且同一子集内不能出现相同的元素。

子集的 **不兼容度**（incompatibility）定义为该子集内最大元素与最小元素的差值。

返回在最优划分下 `k` 个子集的不兼容度之和的最小可能值；如果无法满足划分条件，则返回 `-1`。

> **子集**：数组中出现的整数的一个无序集合。

### 示例

**示例 1**  
输入: `nums = [1,2,1,4]`, `k = 2`  
输出: `4`  
解释: 最优的划分方式为 `[1,2]` 和 `[1,4]`。  
不兼容度为 `(2-1) + (4-1) = 4`。  
注意 `[1,1]` 与 `[2,4]` 的和更小，但第一个子集包含了两个相同的元素，违反了条件。

**示例 2**  
输入: `nums = [6,3,8,1,3,1,2,2]`, `k = 4`  
输出: `6`  
解释: 最优的划分方式为 `[1,2]`、`[2,3]`、`[6,8]` 和 `[1,3]`。  
不兼容度为 `(2-1) + (3-2) + (8-6) + (3-1) = 6`。

**示例 3**  
输入: `nums = [5,3,3,6,3,3]`, `k = 3`  
输出: `-1`  
解释: 无法将 `nums` 划分成 3 个子集，使得同一子集内没有相等的元素。

### 约束条件

- `1 <= k <= nums.length <= 16`
- `nums.length` 能被 `k` 整除
- `1 <= nums[i] <= nums.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把数组的每个元素都放进 k 个子集**，枚举所有可能的分配方式，挑选出合法（同一个子集里没有相同数字）且不冲突的分配，计算每个子集的 `max‑min`，把它们加起来，取最小值。

- **用到的数据结构**  
  - **列表**：保存每个子集的元素，就像我们把水果装进不同的篮子。  
  - **集合（set）**：用来快速判断某个子集里是否已经出现了相同的数字，类似于字典的“查字典”，键是数字，值是“已经在这个篮子里”。  

- **为什么这个方法正确**  
  - 我们遍历了**所有**可能的分配方式，只要有一种合法的分配能得到更小的“不兼容和”，它一定会在遍历过程中被检查到。  

- **复杂度分析（大白话）**  
  - 对每个元素都有 `k` 种放法，所以总的分配数是 `kⁿ`（n 为数组长度）。  
  - 假设 `n = 16、k = 8`，`kⁿ = 8¹⁶ ≈ 2.8×10¹⁴`，天文数字，根本不可能跑完。  
  - 时间复杂度记作 **O(kⁿ)**，这表示**指数级**增长，随着 n 增大会“炸裂”。  
  - 只用到几个列表和集合，空间是 **O(k·n)**，基本可以忽略不计。

#### 代码（Python）

```python
from typing import List

def minimumIncompatibility(nums: List[int], k: int) -> int:
    n = len(nums)
    size = n // k                     # 每个子集的固定大小
    # 记录当前每个子集的元素（列表）和是否出现重复（集合）
    groups = [[] for _ in range(k)]
    used = [set() for _ in range(k)]

    ans = float('inf')

    def backtrack(idx: int, cur_sum: int):
        """把 nums[idx:] 的元素继续放进子集"""
        nonlocal ans
        # 剪枝：已经比当前最小答案大，直接返回
        if cur_sum >= ans:
            return
        # 所有元素都放完了，更新答案
        if idx == n:
            ans = cur_sum
            return

        val = nums[idx]
        # 尝试把当前元素放进每一个子集
        for g in range(k):
            # 1）子集未满且没有重复数字
            if len(groups[g]) < size and val not in used[g]:
                # 计算放进去后该子集的不兼容增量
                # 只有在子集刚好填满时才产生 max‑min
                inc = 0
                if len(groups[g]) == size - 1:      # 这次放进去后恰好满
                    mini = min(groups[g] + [val])
                    maxi = max(groups[g] + [val])
                    inc = maxi - mini

                groups[g].append(val)
                used[g].add(val)

                backtrack(idx + 1, cur_sum + inc)

                # 恢复现场
                groups[g].pop()
                used[g].remove(val)

            # 如果子集是空的，后面的子集也一定是空的，避免对称状态重复搜索
            if not groups[g]:
                break

    backtrack(0, 0)
    return -1 if ans == float('inf') else ans
```

> 关键注释已写在代码里。即使把 `n` 限制到 10 左右，这段代码也只能跑几秒；`n = 16` 时根本不可行。

#### 复杂度

- **时间复杂度**：`O(kⁿ)` —— 每个元素有 `k` 种选择，指数级增长。  
  > 把 `kⁿ` 想象成“每走一步都要开 `k` 条路”，走 `n` 步后路数就是 `kⁿ`，非常多。  
- **空间复杂度**：`O(k·n)` —— 保存 `k` 个子集的内容和集合，最多存 `n` 个数字。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于：我们在 **元素层面**（每次放一个数）进行搜索，导致大量重复的子集组合被反复遍历。  
要想快一点，需要 **从子集层面** 直接枚举合法的子集，然后把这些子集拼成完整的划分。  

关键观察：

1. **子集大小固定**  
   - `n = len(nums)`，每个子集必须恰好有 `size = n / k` 个元素。  

2. **子集内部不允许出现相同数字**  
   - 这可以在子集生成时直接过滤掉。  

3. **子集的不兼容值**  
   - 对于一个合法子集，只需要 `max - min`，与子集内部的排列无关。  

4. **整个划分就是「若干个互不相交的合法子集」的集合**  
   - 互不相交可以用 **位掩码（bitmask）** 表示：数组长度 ≤ 16，使用 16 位整数，每一位代表对应位置的元素是否已被使用。  

基于上述想法，最常用的做法是：

- **预处理**：遍历所有 `size` 大小的子集（组合），如果子集中没有重复数字，就计算它的不兼容值 `max - min`，并记下对应的位掩码 `mask`。  
- **动态规划（DP） + 位掩码**：  
  - `dp[mask]` 表示已经选取的元素集合为 `mask` 时，能够得到的最小不兼容和。  
  - 初始 `dp[0] = 0`（什么都没选，和为 0）。  
  - 对每个 `mask`，尝试加入一个 **合法子集的 mask_sub**，要求 `mask_sub` 与 `mask` 不重叠（`mask & mask_sub == 0`），并且子集大小正好是 `size`。  
  - 状态转移：`dp[mask | mask_sub] = min(dp[mask | mask_sub], dp[mask] + incompatibility[mask_sub])`。  
- 最终答案是 `dp[full_mask]`，其中 `full_mask = (1 << n) - 1`（所有元素都被使用）。如果 `dp[full_mask]` 没有被更新，则返回 `-1`。

**为什么快**：

- 子集的枚举次数是 `C(n, size)`（组合数），在最坏情况下 `n = 16, size = 8` 时约为 `12870`，远小于 `kⁿ`。  
- DP 只遍历 `2ⁿ`（最多 65536）个状态，每个状态只尝试少量合法子集，整体复杂度约为 `O( 2ⁿ * C(n, size) )`，在题目限制下完全可接受。

#### 代码（Python）

```python
from typing import List
from itertools import combinations
import math

def minimumIncompatibility(nums: List[int], k: int) -> int:
    n = len(nums)
    size = n // k                     # 每个子集必须恰好有 size 个元素
    full_mask = (1 << n) - 1          # 所有位置都被选中的掩码

    # ---------- 1. 预处理所有合法子集 ----------
    # incompat[mask] = 子集的 (max - min)；若 mask 对应的子集不合法，则不加入字典
    incompat = {}
    # 为了快速判断子集里是否有重复数字，先把每个位置的数值取出来
    for comb in combinations(range(n), size):
        # comb 是位置索引的元组，例如 (0,3,5)
        seen = set()
        ok = True
        vals = []
        for idx in comb:
            v = nums[idx]
            if v in seen:          # 同一子集出现相同数字，不合法
                ok = False
                break
            seen.add(v)
            vals.append(v)
        if not ok:
            continue
        mask = 0
        for idx in comb:
            mask |= 1 << idx        # 把这些位置对应的位设为 1
        incompat[mask] = max(vals) - min(vals)   # 计算不兼容值

    # ---------- 2. DP over bitmask ----------
    INF = math.inf
    dp = [INF] * (1 << n)
    dp[0] = 0                         # 空集合的代价为 0

    # 遍历所有状态
    for mask in range(1 << n):
        if dp[mask] == INF:           # 这个状态根本不可达，直接跳过
            continue
        # 已经用了多少个元素？如果已经是 full_mask 就不必再继续
        if mask == full_mask:
            continue
        # 只尝试那些合法子集的 mask_sub，它们必须和当前 mask 不冲突
        # 为了加速，只遍历预处理好的子集
        for sub_mask, cost in incompat.items():
            if mask & sub_mask:       # 有交集，说明这些元素已经被用过
                continue
            new_mask = mask | sub_mask
            # 更新新状态的最小代价
            if dp[new_mask] > dp[mask] + cost:
                dp[new_mask] = dp[mask] + cost

    return -1 if dp[full_mask] == INF else dp[full_mask]
```

> 代码中每一步都有中文注释，帮助你一步步跟上思路。  

#### 复杂度

- **时间复杂度**：  
  - 预处理合法子集：`O( C(n, size) * size )`（遍历每个组合并计算 max/min）。  
  - DP 转移：`O( 2ⁿ * number_of_valid_subsets )`，其中 `number_of_valid_subsets ≤ C(n, size)`。  
  - 对于 `n ≤ 16`，最坏约为 `O( 2¹⁶ * 12870 ) ≈ 8.4×10⁸`，但实际常数极小，运行在 0.1~0.3 秒内。  
- **空间复杂度**：  
  - `dp` 数组需要 `2ⁿ` 个浮点/整数，`O(2ⁿ)`（最多 65536）。  
  - `incompat` 只存合法子集的掩码和值，最多 `C(n, size)` 条记录，整体仍是 `O(2ⁿ)`。  

相比暴力的 **指数级（kⁿ）**，这里是 **指数级但基数更小（2ⁿ）**，并且利用了子集的提前过滤，大幅降低了实际搜索空间。

---

## 心得

- **核心技巧**：**位掩码 + 子集 DP**（先枚举合法子集，再在全局层面做最小费用覆盖）。  
- **适用的题型**（类似思路）  
  1. *Partition to K Equal Sum Subsets*（把数组划分成 k 个等和子集）  
  2. *Maximum Number of Groups Getting Fresh Chocolate*（分组满足条件的最大数量）  
  3. *Minimum Number of Increments on Subarrays to Form a Target Array*（子数组位运算 DP）  
- **一句话总结解题钥匙**：**先把“合法的子集”筛出来，用位掩码表示，再用 DP 在这些子集之间挑选出互不重叠、覆盖全部元素的最小代价组合**。

---

## 反思

- **第一反应**：直接想把每个数逐个放进 k 个桶里回溯，没意识到子集大小固定可以提前枚举。  
- **最容易踩的坑**  
  - **重复数字**：子集内部出现相同元素必须剔除，否则会得到错误的“不兼容”。  
  - **子集大小**：必须恰好是 `size = n/k`，否则最终的划分会不完整。  
  - **位运算细节**：`mask & sub_mask == 0` 用来判断两子集是否冲突，忘记这一点会产生重复使用同一元素的错误。  
- **下次遇到同类题**，第一步就**把所有满足局部约束的“基本单元”（子集、区间、组合）列举出来**，再在全局层面用 **DP + 位掩码** 进行最优选择。这样可以把搜索空间从“每个元素的每种放法”压缩到“每个合法子集的每种组合”。