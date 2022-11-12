# #2009. **使数组连续的最少操作次数** / Minimum Number of Operations to Make Array Continuous

> 难度：困难 · 标签：Array、Hash Table、Binary Search、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-operations-to-make-array-continuous/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums. In one operation, you can replace any element in nums with any integer.
nums is considered continuous if both of the following conditions are fulfilled:
For example, nums = [4, 2, 5, 3] is continuous, but nums = [1, 2, 3, 5, 6] is not continuous.
Return the minimum number of operations to make nums continuous.

**Examples**

**Example 1:**

```
Input: nums = [4,2,5,3]
Output: 0
Explanation: nums is already continuous.
```

**Example 2:**

```
Input: nums = [1,2,3,5,6]
Output: 1
Explanation: One possible solution is to change the last element to 4.
The resulting array is [1,2,3,5,4], which is continuous.
```

**Example 3:**

```
Input: nums = [1,10,100,1000]
Output: 3
Explanation: One possible solution is to:
- Change the second element to 2.
- Change the third element to 3.
- Change the fourth element to 4.
The resulting array is [1,2,3,4], which is continuous.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 109

---

## 题目（中文翻译）

给定一个整数数组 `nums`。一次操作中，你可以将 `nums` 中的任意元素替换为任意整数。

如果数组满足以下两个条件，则称其为连续（continuous）：

1. 数组中所有元素互不相同；
2. 最大元素与最小元素之差恰好等于数组长度减一，即 `max(nums) - min(nums) + 1 = nums.length`（等价于排序后相邻元素之差均为 1）。

例如，`nums = [4, 2, 5, 3]` 是连续的，而 `nums = [1, 2, 3, 5, 6]` 则不是连续的。

返回使 `nums` 连续所需的最少操作次数。

---

**示例 1**

```
Input: nums = [4,2,5,3]
Output: 0
Explanation: nums 已经是连续的，无需任何操作。
```

**示例 2**

```
Input: nums = [1,2,3,5,6]
Output: 1
Explanation: 可以将最后一个元素改为 4，得到 [1,2,3,5,4]，此时数组连续。
```

**示例 3**

```
Input: nums = [1,10,100,1000]
Output: 3
Explanation: 可以按以下方式操作：
- 将第二个元素改为 2；
- 将第三个元素改为 3；
- 将第四个元素改为 4；
得到的数组为 [1,2,3,4]，已连续。
```

---

**约束条件**

- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把数组变成一个「连续」的序列**，比如长度为 `n` 的数组，只要把它改成 `[x, x+1, x+2, …, x+n-1]`（其中 `x` 是某个起始整数）就满足题意。  

于是我们可以枚举所有可能的起始值 `x`，然后统计原数组里已经落在区间 `[x, x+n-1]` 的元素有多少个，剩下的 `n‑cnt` 个就必须通过「一次操作」把它们改成缺少的数字。  

> **类比**：把数组看成一本词典里的单词，连续的数组就像字典里从第 `x` 页到第 `x+n-1` 页的连续页码。我们要找出已有多少单词已经正好在这段页码里，缺的页码就要「补齐」——每补一个页码就是一次操作。

**为什么正确**  
如果我们固定了起始值 `x`，那么唯一合法的目标数组就是 `[x, x+1, …, x+n-1]`（顺序不影响，因为可以随意替换成任何整数）。只要把不在这个区间的元素全部换成缺少的数，就一定能得到连续数组；而保留下来的元素数量最多时，操作次数自然最少。

**时间/空间分析（大白话）**  

- 枚举 `x` 的个数在最坏情况下可能是 `O(n)`（因为只要考虑 `nums` 中的每个元素作为左端点），每次统计区间内的元素又要遍历整个数组，**时间复杂度是 `O(n²)`**。  
  - `O(n²)` 可以想象成「十个人排队，每个人都要检查十遍」——随着人数的平方增长，计算量会很快炸掉。
- 只用了几个整数变量，**空间复杂度是 `O(1)`**（常数级别的内存）。

#### 代码（Python）

```python
from typing import List

def minOperations_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    ans = n                     # 最多需要 n 次操作（全部替换）

    # 为了避免枚举到无意义的起始值，我们只把每个 nums[i] 当成左端点
    for i in range(n):
        left = nums[i]          # 区间左边界 x
        right = left + n - 1    # 区间右边界 x+n-1

        # 统计有多少元素已经在 [left, right] 之间
        cnt = 0
        for v in nums:
            if left <= v <= right:
                cnt += 1

        # 需要替换的元素数 = 总长度 - 已经在区间内的数量
        ans = min(ans, n - cnt)

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)` — 每个左端点遍历整个数组，等价于「n 个人每人都要检查 n 次」。
- **空间复杂度**：`O(1)` — 只用了若干整数变量，没有额外的随 `n` 增长的存储。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **「每次统计都要遍历整条数组」**。我们需要把「统计区间内元素个数」的过程加速。

**关键观察 1：排序后区间变得有序**  
把数组从小到大排序（`O(n log n)`），那么任意区间 `[x, x+n-1]` 在排好序的数组里对应的 **连续子段**。于是我们只要在排好序的数组上找最长的子段，使得子段的最左元素和最右元素之差 ≤ `n-1`（即这段数已经可以组成连续序列，重复的数需要先去重）。

**关键观察 2：重复元素没有帮助**  
如果出现相同的数，连续序列里只能保留一个，其他的必须被替换。于是我们先 **去重**（使用 `set`），得到 **唯一值的有序列表** `uniq`。

**关键观察 3：滑动窗口（双指针）**  
在有序且去重的数组 `uniq` 上，用两个指针 `l`、`r` 维护一个窗口，要求窗口内的最大值 `uniq[r]` 与最小值 `uniq[l]` 的差 ≤ `n-1`。  
- 当窗口满足条件时，窗口长度 `r-l+1` 表示我们可以 **直接保留** 这么多不同的数，剩下的 `n - (r-l+1)` 个位置需要通过操作补齐。
- 当窗口不满足时，左指针 `l` 向右收缩，直到重新满足条件。

遍历一次 `uniq`（每个元素最多进出窗口一次），就能得到 **最大可保留的不同元素数** `max_keep`。答案即 `n - max_keep`。

> **类比**：把 `uniq` 想成一条排好队的学生，老师希望选出一段人数最多且身高（数值）相差不超过 `n-1` 的学生，这段学生可以直接留下，其他学生需要重新安排座位（相当于一次操作）。

**时间复杂度**  
- 排序 `O(n log n)`（`n` 为原数组长度）。  
- 去重 `O(n)`，滑动窗口 `O(m)`，其中 `m ≤ n`（去重后的长度）。  
- 总体 `O(n log n)`，远快于暴力的 `O(n²)`。

**空间复杂度**  
- 需要存储排好序的数组和去重后的列表，最多 `O(n)`。  

#### 代码（Python）

```python
from typing import List

def minOperations(nums: List[int]) -> int:
    n = len(nums)

    # 1. 排序 + 去重，得到唯一且有序的数组
    uniq = sorted(set(nums))          # set 像字典的“查词典”，把重复的词去掉
    m = len(uniq)

    max_keep = 0                      # 能直接保留下来的最大不同元素数
    l = 0                             # 左指针

    # 2. 滑动窗口：右指针 r 从左到右遍历 uniq
    for r in range(m):
        # 窗口太宽（最大值 - 最小值 > n-1）时，左指针右移收缩窗口
        while uniq[r] - uniq[l] > n - 1:
            l += 1

        # 当前窗口长度 = r - l + 1
        # 这段数已经可以在不改变的情况下组成连续序列（只要把缺的数补上）
        max_keep = max(max_keep, r - l + 1)

    # 3. 需要替换的最少次数 = 总长度 - 能保留的最大不同元素数
    return n - max_keep
```

#### 复杂度

- **时间复杂度**：`O(n log n)` — 主要花在排序上，`log n` 像「把书一本一本放进书架」的过程，远比暴力的「每个人都要检查每个人」快得多。
- **空间复杂度**：`O(n)` — 需要额外存放排好序的数组和去重后的列表。

---

## 心得

- **核心技巧**：**先排序再去重 + 滑动窗口**，把「找区间」的问题转化为「找最长满足差值限制的连续子段」。
- **适用的类似题型**  
  1. **最长子数组/子序列满足范围限制**（如 LeetCode 713 *Subarray Product Less Than K*）。  
  2. **最少替换使数组递增**（如 LeetCode 665 *Non-decreasing Array*）。  
  3. **把数组变成连续序列的最少操作**（本题本身的变体）。
- **一句话总结**：  
  *“把数组排好序、去掉重复，用滑动窗口找能直接保留的最长区间，剩下的全换掉。”*

---

## 反思

- **第一反应**：直接枚举所有可能的连续区间，统计已有的元素——这就是暴力解的出发点。  
- **最容易踩的坑**  
  - **重复元素**：忽略重复会导致窗口长度误算，需要先 `set` 去重。  
  - **窗口长度的判断**：区间长度应与原数组长度 `n` 对比，而不是去重后长度 `m`。  
  - **边界条件**：当数组本身已经连续（`max_keep == n`）时，答案应为 `0`，代码要能正确返回。  
- **下次类似题的第一步**：  
  *“先把数据排序并去重，看能否在有序结构上用双指针/滑动窗口一次遍历求出最大满足条件的子段。”*