# #2607. 使 K 子数组之和相等 / Make K-Subarray Sums Equal

> 难度：中等 · 标签：Array、Math、Greedy、Sorting、Number Theory · [LeetCode 链接](https://leetcode.com/problems/make-k-subarray-sums-equal/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array arr and an integer k. The array arr is circular. In other words, the first element of the array is the next element of the last element, and the last element of the array is the previous element of the first element.
You can do the following operation any number of times:
Return the minimum number of operations such that the sum of each subarray of length k is equal.
A subarray is a contiguous part of the array.

**Examples**

**Example 1:**

```
Input: arr = [1,4,1,3], k = 2
Output: 1
Explanation: we can do one operation on index 1 to make its value equal to 3.
The array after the operation is [1,3,1,3]
- Subarray starts at index 0 is [1, 3], and its sum is 4 
- Subarray starts at index 1 is [3, 1], and its sum is 4 
- Subarray starts at index 2 is [1, 3], and its sum is 4 
- Subarray starts at index 3 is [3, 1], and its sum is 4
```

**Example 2:**

```
Input: arr = [2,5,5,7], k = 3
Output: 5
Explanation: we can do three operations on index 0 to make its value equal to 5 and two operations on index 3 to make its value equal to 5.
The array after the operations is [5,5,5,5]
- Subarray starts at index 0 is [5, 5, 5], and its sum is 15
- Subarray starts at index 1 is [5, 5, 5], and its sum is 15
- Subarray starts at index 2 is [5, 5, 5], and its sum is 15
- Subarray starts at index 3 is [5, 5, 5], and its sum is 15
```

**Constraints**

- 1 <= k <= arr.length <= 105
- 1 <= arr[i] <= 109

---

## 题目（中文翻译）

**描述**  
给定一个下标从 0 开始的整数数组 `arr` 与一个整数 `k`。数组 `arr` 是循环的，也就是说数组的第一个元素是最后一个元素的下一个元素，最后一个元素是第一个元素的前一个元素。  

你可以任意次数执行以下操作：  

返回使所有长度为 `k` 的子数组（subarray）的和相等所需的最少操作次数。子数组是数组中连续的片段。

**示例**

*示例 1*  
```
Input: arr = [1,4,1,3], k = 2
Output: 1
```
**解释**：我们可以在下标 `1` 处进行一次操作，使其值变为 `3`。操作后的数组为 `[1,3,1,3]`。  

- 以下标 `0` 开始的子数组是 `[1, 3]`，其和为 `4`  
- 以下标 `1` 开始的子数组是 `[3, 1]`，其和为 `4`  
- 以下标 `2` 开始的子数组是 `[1, 3]`，其和为 `4`  
- 以下标 `3` 开始的子数组是 `[3, 1]`，其和为 `4`

*示例 2*  
```
Input: arr = [2,5,5,7], k = 3
Output: 5
```
**解释**：我们可以在下标 `0` 处进行三次操作，使其值变为 `5`，并在下标 `3` 处进行两次操作，使其值也变为 `5`。操作后的数组为 `[5,5,5,5]`。  

- 以下标 `0` 开始的子数组是 `[5, 5, 5]`，其和为 `15`  
- 以下标 `1` 开始的子数组是 `[5, 5, 5]`，其和为 `15`  
- 以下标 `2` 开始的子数组是 `[5, 5, 5]`，其和为 `15`  
- 以下标 `3` 开始的子数组是 `[5, 5, 5]`，其和为 `15`

**约束条件**  
- `1 <= k <= arr.length <= 10^5`  
- `1 <= arr[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**先把每个长度为 `k` 的子数组的和算出来**，记为 `s0, s1, …, s_{n-1}`（因为数组是环形的，子数组可以从任意位置开始）。如果所有子数组的和必须相等，那么它们的目标值只能是这 `n` 个和的**某个公共数**。  

我们可以把目标和 **假设** 为 `T`，然后遍历整个数组，**逐个修改元素**，让每个子数组的和都变成 `T`。因为一次操作只能把某个元素加 1 或减 1，修改第 `i` 个元素 `x` 次就需要 `|x|` 次操作。于是：

1. 选一个可能的目标和 `T`（比如遍历所有 `s_i`，或遍历 `[min(s), max(s)]` 的每一个整数）。
2. 按顺序处理子数组：当处理到以 `i` 为起点的子数组时，计算它当前的和 `cur` 与 `T` 的差 `diff = cur - T`。把 `diff` 分摊到子数组里的每个元素上（例如把 `diff` 全部加到子数组最左边的元素），这相当于对该元素做 `|diff|` 次增减操作。
3. 累计所有元素的操作次数，得到一种“把所有子数组和调到 `T`”的代价。

因为我们要 **尝试所有可能的 `T`**，并且每次都要遍历整个数组去“分摊差值”，时间复杂度会非常高。

- **为什么它是正确的？**  
  只要我们把每个子数组的和都调到同一个数 `T`，显然所有子数组的和就相等了。遍历所有 `T` 能保证找到最小的代价（虽然代价计算本身是暴力的）。
- **时间/空间复杂度**  
  *时间*：假设数组长度为 `n`，我们枚举 `O(n)` 个可能的 `T`，每次遍历 `n` 个元素并在每个子数组里做 `k` 次“分摊”，总共是 `O(n * n * k)`，最坏情况下约为 `O(n³)`。  
  *空间*：只需要常数级额外空间 `O(1)`（存几个计数器），不需要额外数组。

> **大白话**：`O(n³)` 就像把 1000 块砖头每块都搬来搬去 1000 次再搬回去——在实际中根本跑不完。

#### 代码（Python）

```python
def brute_force(arr, k):
    n = len(arr)
    # 计算所有长度为 k 的子数组和（环形）
    sums = []
    cur = sum(arr[i] for i in range(k))
    sums.append(cur)
    for i in range(1, n):
        cur += arr[(i + k - 1) % n] - arr[i - 1]
        sums.append(cur)

    best = float('inf')
    # 枚举每一个可能的目标和 T
    for T in sums:                     # 这里仅枚举出现过的子数组和，仍然是暴力
        ops = 0
        a = arr[:]                     # 复制一份，防止修改原数组
        # 逐个子数组“调平”
        for start in range(n):
            # 计算当前子数组的和
            cur = sum(a[(start + offset) % n] for offset in range(k))
            diff = cur - T
            # 把差值全部加到子数组最左边的元素上
            idx = start
            a[idx] -= diff
            ops += abs(diff)            # 需要的操作次数就是 |diff|
        best = min(best, ops)
    return best
```

> 这段代码可以直接跑，但对于 `n` 达到几千甚至上万时会 **超时**，因为它的时间复杂度太高。

#### 复杂度

- **时间复杂度**：`O(n³)` —— 这里的 `n³` 代表“遍历所有可能目标值 + 对每个目标值遍历所有子数组 + 对每个子数组遍历 `k` 个元素”。在实际中，这相当于“把每个砖头搬来搬去很多次”，几乎不可接受。
- **空间复杂度**：`O(1)` —— 只用了几个临时变量，额外空间几乎为零。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正的瓶颈在于我们对每个子数组都反复遍历**。如果能直接找出哪些位置的元素 **必须相等**，就可以把问题转化为“把同一组里的数改成相同值”，而不必每次都滑动窗口。

**关键观察 1：子数组和相等 ⇒ 相邻窗口的差为 0**  

设 `S_i` 为以 `i` 为起点的长度为 `k` 的子数组和（环形），要求所有 `S_i` 相等。  
两个相邻窗口的和差：

```
S_i - S_{i+1}
 = (arr[i] + arr[i+1] + … + arr[i+k-1])
   - (arr[i+1] + … + arr[i+k])
 = arr[i] - arr[i+k]          (下标取模 n)
```

如果所有 `S_i` 都相等，那么上式必须为 0，即  

```
arr[i] = arr[i+k]   (对所有 i)
```

**关键观察 2：这条等式会形成若干“循环组”**  

把数组看成环，步长为 `k`，从任意位置出发不断向前跳 `k` 步，最终会回到起点。  
这正是 **模 `n` 加法群** 中的 **循环子群**，其大小为 `n / gcd(n, k)`，而**不同的起点会产生 `g = gcd(n, k)` 条不相交的循环**。  

换句话说，**所有下标满足 `i % g == r`（`r` 为 0~g‑1） 的元素会在同一个循环里**，它们之间必须相等。  

**关键观察 3：在同一组里，最省操作的目标值是“中位数”**  

假设某组的原始数为 `[x1, x2, …, xm]`，我们要把它们全部改成同一个整数 `t`，操作次数是  

```
cost(t) = Σ |xi - t|
```

这个函数在 **中位数**（排序后第 `m//2` 位）取得最小值——这是“绝对值求和最小化”的经典结论（可以用“把数往中间推，左边的往右，右边的往左”来直观理解）。

因此，**每个循环组独立求中位数，然后把组内所有数改成该中位数**，总操作次数即为各组的 `cost` 之和。

**完整步骤**  

1. 计算 `g = gcd(n, k)`。  
2. 按 `i % g` 把下标划分成 `g` 组。  
3. 对每组  
   - 把组内的数取出来放进列表 `group`。  
   - 对 `group` 排序，找到中位数 `mid = group[len(group)//2]`。  
   - 累加 `abs(x - mid)` 到答案。  
4. 返回答案即为最少操作次数。

**为什么是最优的？**  

- 通过等式 `arr[i] = arr[i+k]` 我们已经 **必然** 要让同一循环里的数相等，任何合法的最终数组都满足这点。  
- 在每个循环内部，选择中位数是 **局部最优**（最小化该组的操作次数），而不同循环之间互不影响，局部最优即整体最优。  

#### 代码（Python）

```python
import math
from typing import List

def min_operations(arr: List[int], k: int) -> int:
    """
    返回最少的 +1/-1 操作次数，使得每个长度为 k 的子数组和相等。
    思路：
    1. 依据 gcd(n, k) 把下标划分为若干循环组；
    2. 每组内部把元素改成该组的中位数；
    3. 累加所有绝对差即为答案。
    """
    n = len(arr)
    g = math.gcd(n, k)          # 循环组的数量

    ans = 0
    # 对每一个余数 r (0 ~ g-1) 形成一组
    for r in range(g):
        group = []
        # 收集所有下标 i 满足 i % g == r 的元素
        i = r
        while i < n:
            group.append(arr[i])
            i += g               # 跳 g 步，恰好遍历同一循环
        # 排序后取中位数
        group.sort()
        median = group[len(group) // 2]   # 中位数（左中位或右中位都可）
        # 计算把该组全部变成 median 所需的操作次数
        for x in group:
            ans += abs(x - median)

    return ans
```

> **代码要点注释**  
- `math.gcd` 就像“找两根绳子共同的最短结”，返回它们的最大公约数 `g`。  
- `i += g` 相当于“在圆环上每次跳 `g` 步”，正好遍历同一个循环组。  
- `group.sort()` 把这组数字排好序，**中位数**就是排在中间的那一个，类似把一堆书排好后挑出最中间那本。  
- `abs(x - median)` 是“把 `x` 改成 `median` 需要的 +1/-1 次数”，所有这些加起来就是答案。

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 对每个循环组我们都要排序，所有组里元素总数恰好是 `n`，所以总的排序时间是 `O(n log n)`。  
  - 其余遍历、求中位数、累计差值都是线性 `O(n)`，不影响整体复杂度。  
  - 与暴力解的 `O(n³)` 相比，**从“几千次搬砖”降到“几千次快速排序”，快了几个数量级**。

- **空间复杂度**：`O(n)`（最坏情况下需要把所有元素存进 `group` 列表）  
  - 如果想进一步节省空间，可以在遍历时就把每组元素直接放进一个临时数组，处理完后释放；但 `n ≤ 10⁵` 的规模下 `O(n)` 完全可以接受。

---

## 心得

- **核心技巧**：**利用 `gcd(n, k)` 把环形数组划分为若干相互独立的循环组**，每组内部取中位数最小化绝对差。  
- **适用的题型**  
  1. “把环形/循环数组中若干位置的数统一”类问题（如 *Make All Elements Equal*、*Circular Array Equality*）。  
  2. “在同一约束下让若干子序列的和相等”类问题（如 *Equal Subarray Sums*、*Make Subarray Sums Equal*）。  
- **一句话总结解题钥匙**：**“相邻窗口相等 ⇒ 位置等式 ⇒ 通过 gcd 把位置划分 → 每组取中位数最省操作”。**

---

## 反思

- **第一反应**：看到“每个长度为 k 的子数组和相等”，立刻想到“滑动窗口差”会产生 `arr[i] - arr[i+k] = 0`，于是想到 **相邻元素必须相等**。  
- **最容易踩的坑**  
  - 忽略环形特性：下标需要取模 `n`，否则 `i+k` 会越界。  
  - 只考虑 `k` 本身而不取 `gcd(n, k)`，会把同一循环组拆成多个错误的子组，导致答案偏大。  
  - 中位数的选取：若组大小为偶数，左中位或右中位都可以，只要取 **任意一个** 中间的数即可。  
- **下次遇到同类题**，第一步应该问自己：**“相邻窗口的差是什么？”** 这往往会暴露出必须相等的下标关系，进而使用 **gcd** 把问题分解为独立的“小组”。这样就能从“枚举”直接跳到“分组+中位数”这种高效思路。