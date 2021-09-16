# #1477. 找到两个互不重叠的子数组，使其和等于目标值 / Find Two Non-overlapping Sub-arrays Each With Target Sum

> 难度：中等 · 标签：Array、Hash Table、Binary Search、Dynamic Programming、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/find-two-non-overlapping-sub-arrays-each-with-target-sum/)

---

## 题目（英文原版）

**Description**

You are given an array of integers arr and an integer target.
You have to find two non-overlapping sub-arrays of arr each with a sum equal target. There can be multiple answers so you have to find an answer where the sum of the lengths of the two sub-arrays is minimum.
Return the minimum sum of the lengths of the two required sub-arrays, or return -1 if you cannot find such two sub-arrays.

**Examples**

**Example 1:**

```
Input: arr = [3,2,2,4,3], target = 3
Output: 2
Explanation: Only two sub-arrays have sum = 3 ([3] and [3]). The sum of their lengths is 2.
```

**Example 2:**

```
Input: arr = [7,3,4,7], target = 7
Output: 2
Explanation: Although we have three non-overlapping sub-arrays of sum = 7 ([7], [3,4] and [7]), but we will choose the first and third sub-arrays as the sum of their lengths is 2.
```

**Example 3:**

```
Input: arr = [4,3,2,6,2,3,4], target = 6
Output: -1
Explanation: We have only one sub-array of sum = 6.
```

**Constraints**

- 1 <= arr.length <= 105
- 1 <= arr[i] <= 1000
- 1 <= target <= 108

---

## 题目（中文翻译）

**描述**  
给定一个整数数组 `arr` 和一个整数 `target`。  
要求在 `arr` 中找到两个互不重叠的子数组（subarray），使每个子数组的元素和恰好等于 `target`。可能存在多种满足条件的组合，你需要返回长度之和最小的那一对子数组的长度之和。如果不存在这样两条子数组，返回 `-1`。

**示例**

**示例 1**  
```
Input: arr = [3,2,2,4,3], target = 3
Output: 2
Explanation: 只有两个子数组的和等于 3（[3] 和 [3]），它们的长度之和为 2。
```

**示例 2**  
```
Input: arr = [7,3,4,7], target = 7
Output: 2
Explanation: 虽然存在三组互不重叠的子数组和为 7（[7]、[3,4]、[7]），但选择第一个和第三个子数组即可，使长度之和为 2。
```

**示例 3**  
```
Input: arr = [4,3,2,6,2,3,4], target = 6
Output: -1
Explanation: 只存在唯一一个和为 6 的子数组，无法构成两条互不重叠的子数组。
```

**约束条件**  
- `1 <= arr.length <= 10^5`  
- `1 <= arr[i] <= 1000`  
- `1 <= target <= 10^8`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把 **所有** 满足 `sum == target` 的子数组都列举出来，然后在这些子数组中挑选两两不重叠的组合，求出长度之和的最小值。  

- **枚举子数组**：使用两层循环，外层固定左端点 `i`，内层把右端点 `j` 从 `i` 往后推，实时累加得到 `arr[i..j]` 的和。只要和等于 `target`，就把 `(i, j, length=j-i+1)` 这条记录保存下来。  
- **两两配对**：遍历保存的子数组列表，任选两条记录 `(l1, r1, len1)`、`(l2, r2, len2)`，检查它们是否不重叠（`r1 < l2` 或 `r2 < l1`），如果不重叠就更新答案 `len1 + len2` 的最小值。  

> **类比**：把数组想象成一排房间，`target` 是需要恰好装满的客容量。暴力解相当于先把所有能恰好装满的客房区间找出来（可能很多），再让两个不相邻的客房区间去比谁的面积（长度）加起来更小。  

这种方法 **一定能得到正确答案**，因为我们穷举了所有可能的子数组和所有合法的配对。  

#### 代码（Python）

```python
from typing import List

def minSumOfLengths_bruteforce(arr: List[int], target: int) -> int:
    n = len(arr)
    sub = []                       # 用来存所有和为 target 的子数组信息
    # 1. 枚举所有子数组
    for i in range(n):
        cur = 0
        for j in range(i, n):
            cur += arr[j]           # 累加得到 arr[i..j] 的和
            if cur == target:
                sub.append((i, j, j - i + 1))   # 记录左、右端点和长度
            elif cur > target:
                break               # 因为 arr 元素均为正数，后面只会更大，直接剪枝

    INF = float('inf')
    ans = INF

    # 2. 两两配对，找不重叠且长度和最小的组合
    m = len(sub)
    for a in range(m):
        l1, r1, len1 = sub[a]
        for b in range(a + 1, m):
            l2, r2, len2 = sub[b]
            # 检查是否不重叠
            if r1 < l2 or r2 < l1:
                ans = min(ans, len1 + len2)

    return -1 if ans == INF else ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 外层遍历 `i`，内层最多遍历到数组尾，最坏情况下要检查所有 `(i, j)` 对，约为 `n*(n+1)/2` 次。  
  - 配对阶段最坏也会检查 `C(m,2)`（`m` 为满足条件的子数组数），在最坏情况下 `m` 仍然是 `O(n²)`，所以整体仍是二次级别。  
  - **大白话**：如果数组长度是 10 000，暴力解大概要跑 100 000 000 次循环，计算机会明显卡住。  

- **空间复杂度**：`O(n²)`（存所有满足条件的子数组）  
  - 最坏情况下每个左端点都能找到一个满足 `target` 的右端点，数量仍然是二次级别。  

> 暴力解虽然概念最简单，但在 `n ≤ 10⁵` 的约束下根本不可用，需要进一步优化。  

---

### 2. 最优解  

#### 思路  

暴力解慢的根本原因是 **重复计算子数组的和**，以及 **大量不必要的配对**。  
观察题目约束：`arr[i]` 均为正整数，这意味着 **滑动窗口**（two‑pointer）可以在一次线性遍历中找到所有和为 `target` 的子数组。  

思路分三步：

1. **一次左→右遍历**，利用滑动窗口找出每个右端点 `i` 之前（包括 `i`）**最短**的满足 `sum == target` 的子数组长度，记为 `left_min[i]`。如果在 `i` 之前根本没有这样子数组，则记为 `∞`。  
   - 维护左指针 `l`、右指针 `r`、当前窗口和 `cur`。  
   - 当 `cur > target` 时左指针右移缩小窗口（因为所有数都正，只有这样才能让和变小）。  
   - 当 `cur == target` 时得到一个合法子数组 `[l, r]`，长度 `len = r - l + 1`。  
   - `left_min[r] = min(left_min[r-1], len)`：把当前找到的长度和之前的最小值取最小，保证 `left_min[i]` 始终是 **截至 i 为止** 的最短合法子数组。  

2. **一次右→左遍历**，同理得到 `right_min[i]`：从位置 `i` 开始（包括 `i`）向右的最短合法子数组长度。实现方式是把数组倒着遍历，或者直接在正序里用另一套滑动窗口（这里用倒序更直观）。  

3. **合并答案**：遍历所有可能的分割点 `i`（`0 ≤ i < n-1`），把左边的最短子数组 `left_min[i]` 与右边的最短子数组 `right_min[i+1]` 相加，取最小值。  
   - 如果某个位置左/右侧没有合法子数组（值为 `∞`），则该分割点不可行。  

> **类比**：把数组看成一条河，两岸各有若干座桥（子数组）恰好能承受 `target` 的重量。我们先在左岸记录离河左端最近的最短桥（`left_min`），再在右岸记录离河右端最近的最短桥（`right_min`），最后挑一处河流的分界点，让左桥和右桥不相交且总长度最小。  

#### 代码（Python）

```python
from typing import List

def minSumOfLengths(arr: List[int], target: int) -> int:
    n = len(arr)
    INF = 10 ** 9                     # 足够大的“无解”标记

    # ---------- 1. left_min ----------
    left_min = [INF] * n               # left_min[i] = 右端点 ≤ i 的最短合法子数组长度
    cur = 0
    l = 0
    best = INF                         # 维护到当前位置的最小长度

    for r in range(n):
        cur += arr[r]                  # 把右指针扩进窗口
        # 缩小窗口直到和不超过 target
        while cur > target:
            cur -= arr[l]
            l += 1
        # 若恰好等于 target，更新 best
        if cur == target:
            length = r - l + 1
            best = min(best, length)
        left_min[r] = best             # 把当前的 best 写入数组

    # ---------- 2. right_min ----------
    right_min = [INF] * n              # right_min[i] = 左端点 ≥ i 的最短合法子数组长度
    cur = 0
    r = n - 1
    best = INF

    for l in range(n - 1, -1, -1):
        cur += arr[l]                  # 把左指针往左扩进窗口
        while cur > target:
            cur -= arr[r]
            r -= 1
        if cur == target:
            length = r - l + 1
            best = min(best, length)
        right_min[l] = best            # 把当前的 best 写入数组

    # ---------- 3. 合并求最小 ----------
    ans = INF
    for i in range(n - 1):
        if left_min[i] < INF and right_min[i + 1] < INF:
            ans = min(ans, left_min[i] + right_min[i + 1])

    return -1 if ans == INF else ans
```

> **关键注释**  
> - `while cur > target:` 这一步是滑动窗口的核心，利用所有数为正的特性保证可以安全地左移指针。  
> - `best = min(best, length)` 用来持续保存 **截至当前** 的最短合法子数组长度。  
> - `left_min[r] = best` 与 `right_min[l] = best` 实现了“前缀最小”和“后缀最小”的概念。  

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 左→右遍历一次、右→左遍历一次、最后一次线性合并，都是线性次数。  
  - **大白话**：即使数组长达 100 000，代码只会跑大约 300 000 次循环，几乎瞬间得到答案。  

- **空间复杂度**：`O(n)`  
  - 需要两个长度为 `n` 的辅助数组 `left_min`、`right_min`。  
  - 这在 `n = 10⁵` 时只占几百 KB，完全可以接受。  

> 与暴力解相比，时间从 **平方级** 降到了 **线性级**，大幅提升了可行性。  

---

## 心得  

- **核心技巧**：利用 **正数数组的滑动窗口** 快速找到所有和为 `target` 的子数组，再结合 **前缀最小 / 后缀最小** 的思想把两段子数组的最短长度合并。  
- **适用场景**：  
  1. “在数组中找满足某个和的子数组”，且数组元素全为非负数（如 LeetCode 560、713）。  
  2. “两段不相交区间满足条件，求最小/最大总长度/价值”，典型做法是先算左侧最优、右侧最优再合并（如 1477. Find Two Non-overlapping Sub-arrays Each With Target Sum）。  
- **一句话总结**：**先用滑动窗口把所有合法子数组的最短长度压缩到前缀/后缀数组里，再在分界点上把左右最短长度相加，即可得到全局最优**。  

---

## 反思  

- **第一反应**：看到“两个不重叠子数组”和“最小长度和”，立刻想到**枚举所有子数组**，但这在大数据规模下不可行。  
- **最容易踩的坑**：  
  - 忘记数组里只能出现正数，导致尝试使用前缀和 + 哈希表的 O(n²) 方案而不利用滑动窗口的优势。  
  - 在合并 `left_min` 与 `right_min` 时，没有注意到两段必须**严格不相交**，错误地使用了同一个下标导致重叠。  
  - 边界情况：数组长度只有 1 或者根本找不到两段合法子数组，需要返回 `-1`。  
- **下次第一步**：确认数组元素的符号（正/负），如果全为正数，就先考虑 **滑动窗口** 来线性找所有满足目标和的子数组，再思考如何把这些信息合并（前缀/后缀最小、动态规划等）。