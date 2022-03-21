# #1712. 将数组划分为三个子数组的方法数 / Ways to Split Array Into Three Subarrays

> 难度：中等 · 标签：Array、Two Pointers、Binary Search、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/ways-to-split-array-into-three-subarrays/)

---

## 题目（英文原版）

**Description**

A split of an integer array is good if:
Given nums, an array of non-negative integers, return the number of good ways to split nums. As the number may be too large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: nums = [1,1,1]
Output: 1
Explanation: The only good way to split nums is [1] [1] [1].
```

**Example 2:**

```
Input: nums = [1,2,2,2,5,0]
Output: 3
Explanation: There are three good ways of splitting nums:
[1] [2] [2,2,5,0]
[1] [2,2] [2,5,0]
[1,2] [2,2] [5,0]
```

**Example 3:**

```
Input: nums = [3,2,1]
Output: 0
Explanation: There is no good way to split nums.
```

**Constraints**

- 3 <= nums.length <= 105
- 0 <= nums[i] <= 104

---

## 题目（中文翻译）

一个整数数组的划分如果满足以下条件则称为「好」的划分（good split）：

- 将数组 `nums` 划分为连续的左子数组 `left`、中子数组 `mid` 和右子数组 `right`，即 `nums = left + mid + right`（`+` 表示拼接）。
- 满足 `sum(left) ≤ sum(mid) ≤ sum(right)`，其中 `sum` 表示子数组的元素和。

给定一个非负整数数组 `nums`，返回 **好** 的划分方式的数量。由于答案可能非常大，请返回答案对 `10^9 + 7` 取模后的结果。

**示例 1**  
**输入**: `nums = [1,1,1]`  
**输出**: `1`  
**解释**: 唯一的好划分方式是 `[1] [1] [1]`。

**示例 2**  
**输入**: `nums = [1,2,2,2,5,0]`  
**输出**: `3`  
**解释**: 有三种好划分方式：
- `[1] [2] [2,2,5,0]`
- `[1] [2,2] [2,5,0]`
- `[1,2] [2,2] [5,0]`

**示例 3**  
**输入**: `nums = [3,2,1]`  
**输出**: `0`  
**解释**: 没有任何好划分方式。

**约束条件**  
- `3 <= nums.length <= 10^5`  
- `0 <= nums[i] <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把数组的两个“分割线”枚举出来。  
- 把数组 `nums` 看成一根绳子，要在绳子上戳两个洞，把绳子分成 **左 / 中 / 右** 三段。  
- 第一个洞（左墙）的位置记作 `i`，第二个洞（右墙）的位置记作 `j`，要求 `0 ≤ i < j < n-1`（因为每段都必须非空）。  
- 用前缀和 `pre[k] = nums[0] + … + nums[k-1]`（下标 0 的前缀和是 0）可以 **O(1)** 求出任意子数组的和：  
  - 左段和 `left = pre[i+1]`  
  - 中段和 `mid  = pre[j+1] - pre[i+1]`  
  - 右段和 `right = pre[n] - pre[j+1]`  

只要遍历所有合法的 `(i, j)`，检查 `left ≤ mid ≤ right` 是否成立，计数即可。

> **哈希表的类比**：前缀和就像一本“累计和字典”，键是下标，值是从数组开头到该下标前的总和，查一次就能得到子数组的和，和查字典找页码的速度一样快（O(1)）。

这个方法**一定能得到正确答案**，因为它穷举了所有可能的切分方式。

#### 代码（Python）

```python
from typing import List

MOD = 10 ** 9 + 7

def waysToSplit(nums: List[int]) -> int:
    n = len(nums)
    # 1️⃣ 计算前缀和数组，pre[k] 表示 nums[0..k-1] 的累计和
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] + nums[i]

    ans = 0
    # 2️⃣ 双层循环枚举左墙 i 与右墙 j
    for i in range(1, n - 1):          # i 为左段的最后一个元素的下标
        left = pre[i]                  # 左段和
        for j in range(i + 1, n):      # j 为中段的最后一个元素的下标
            mid = pre[j + 1] - pre[i]  # 中段和
            right = pre[n] - pre[j + 1]# 右段和
            if left <= mid <= right:   # 满足题目要求
                ans = (ans + 1) % MOD   # 计数并取模
    return ans
```

#### 复杂度

- **时间复杂度：** `O(n²)`  
  两层循环分别遍历 `i`（≈ n 次）和 `j`（≈ n 次），最坏情况要检查 `≈ n·n/2` 种切法。  
  大白话：如果数组有 10 000 个元素，暴力解要跑大约 100 000 000 次循环，明显太慢。

- **空间复杂度：** `O(n)`  
  只用了一个长度为 `n+1` 的前缀和数组。除此之外只用了常数级别的变量。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 出在对每个 `i` 再遍历所有 `j`，导致二次循环。  
观察条件  

```
left  = sum[0..i]           (i 为左墙)
mid   = sum[i+1..j]         (j 为右墙)
right = sum[j+1..n-1]
要求： left ≤ mid ≤ right
```

把等式改写成前缀和的形式（记 `pre[k]` 为前 `k` 个数的累计和）：

```
left  = pre[i+1]
mid   = pre[j+1] - pre[i+1]
right = pre[n] - pre[j+1]
```

对固定的右墙 `j`，我们想知道 **左墙 `i` 能取哪些位置**，使得上式成立。  
把不等式整理得到：

```
pre[i+1] ≤ pre[j+1] - pre[i+1]      →  2·pre[i+1] ≤ pre[j+1]          (1)
pre[j+1] - pre[i+1] ≤ pre[n] - pre[j+1] → pre[i+1] ≥ 2·pre[j+1] - pre[n] (2)
```

记 `L = 2·pre[j+1] - pre[n]`（下界），`R = pre[j+1] // 2`（上界，注意是整数除法向下取整）。  
则合法的 `i` 必须满足 `L ≤ pre[i+1] ≤ R`，并且 `i < j`（左墙在右墙左侧）。

关键点：

1. 前缀和数组 `pre` **单调递增**（因为 `nums` 非负），所以 `pre[i+1]` 随 `i` 增大而不下降。  
2. 对每个 `j`，我们只需要在 `pre` 中找到 **左边界**（第一个满足 `pre[i+1] ≥ L` 的位置）和 **右边界**（最后一个满足 `pre[i+1] ≤ R` 的位置）。  
3. 这两个位置可以用 **二分查找** 在 `pre[1..j]` 中快速定位，时间 `O(log n)`。  
4. 当左边界 ≤ 右边界时，合法的 `i` 个数就是 `rightIdx - leftIdx + 1`。

于是整体时间 `O(n log n)`（遍历 `j`，每次二分），空间仍是 `O(n)`。

> **双指针的类比**：想象在一条直线（前缀和）上有两只手指，左手指不断向右移动寻找第一个够大的位置，右手指寻找最后一个不超出的地方。因为数组是递增的，手指只会向前走，不会回头。

#### 代码（Python）

```python
from typing import List
import bisect

MOD = 10 ** 9 + 7

def waysToSplit(nums: List[int]) -> int:
    n = len(nums)
    # 1️⃣ 前缀和，长度 n+1，pre[0]=0，pre[i] 为前 i 个数的和
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] + nums[i]

    total = pre[n]          # 整个数组的和
    ans = 0

    # 2️⃣ 右墙 j 从左到右移动（j 为中段最后一个元素的下标）
    #    只需要遍历到 n-2，保证右段至少有一个元素
    for j in range(1, n - 1):
        # (1) 计算右墙对应的前缀和值
        right_sum = total - pre[j + 1]          # right = sum[j+1..n-1]
        # (2) 根据推导得到的上下界
        #    L = 2*pre[j+1] - total   （左段前缀和的下限）
        #    R = pre[j+1] // 2        （左段前缀和的上限）
        L = 2 * pre[j + 1] - total
        R = pre[j + 1] // 2

        # 前缀和数组是递增的，只在区间 pre[1..j]（左墙必须在 j 左侧）里找
        # 左边界：第一个 >= L 的位置
        left_idx = bisect.bisect_left(pre, L, 1, j + 1)
        # 右边界：最后一个 <= R 的位置
        right_idx = bisect.bisect_right(pre, R, 1, j + 1) - 1

        # 若找到的区间合法，则把区间长度加入答案
        if left_idx <= right_idx:
            ans = (ans + (right_idx - left_idx + 1)) % MOD

    return ans
```

> **代码要点注释**  
- `bisect_left(arr, target, lo, hi)` 在 `[lo, hi)` 区间内返回第一个 **不小于** `target` 的下标。  
- `bisect_right` 返回第一个 **大于** `target` 的下标，减 1 就是最后一个 ≤ `target` 的位置。  
- `lo = 1` 是因为左墙对应的前缀和至少要包括第一个元素（`pre[0]` 代表空段，不算在内）。

#### 复杂度

- **时间复杂度：** `O(n log n)`  
  主循环遍历 `j`（`n` 次），每次进行两次二分查找（`log n`），所以总体是 `n·log n`。  
  与暴力的 `n²` 相比，数量级从 “平方” 降到了 “对数”，即使 `n=10⁵` 也能在毫秒级完成。

- **空间复杂度：** `O(n)`  
  只额外用了前缀和数组 `pre`，大小为 `n+1`。其他变量都是常数级别。

---

## 心得

- **核心技巧**：利用数组非负导致的前缀和单调性，配合二分查找（或双指针）在有序序列中快速定位满足区间约束的下标范围。  
- **适用题型**  
  1. “把数组分成 k 段，要求每段的和满足某些不等式”——如 *Number of Ways to Split Array*（本题）  
  2. “在有序前缀和中找满足区间的子数组数量”——如 *Subarray Sum Equals K*（可转化为前缀和 + 哈希表）  
  3. “分割点满足左侧 ≤ 右侧”——如 *Maximum Subarray Sum After Partitioning*（需要二分或双指针）  

- **一句话总结**：**利用前缀和的单调性，用二分/双指针把 “遍历所有左墙” 的成本从线性降到对数**。

---

## 反思

- **第一反应**：直接写两层循环枚举所有分割点，随后发现会超时。  
- **最容易踩的坑**  
  - 忘记 `i < j` 的限制，导致计数错误。  
  - 当 `L` 为负数时，二分搜索仍能正常工作，因为前缀和最小是 0。  
  - `R` 需要向下取整（整数除法），否则会产生不合法的左墙位置。  
- **下次遇到同类题**：先检查数组是否单调（或是否可以转化为单调），再考虑 **“把不等式转化为前缀和区间”**，随后用二分或双指针定位合法区间。这样可以迅速从暴力到最优的思路跳跃。