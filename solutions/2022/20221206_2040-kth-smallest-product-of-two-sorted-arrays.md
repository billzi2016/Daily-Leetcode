# #2040. 两个已排序数组的第 k 小乘积 / Kth Smallest Product of Two Sorted Arrays

> 难度：困难 · 标签：Array、Binary Search · [LeetCode 链接](https://leetcode.com/problems/kth-smallest-product-of-two-sorted-arrays/)

---

## 题目（英文原版）

**Description**



**Examples**

**Example 1:**

```
Input: nums1 = [2,5], nums2 = [3,4], k = 2
Output: 8
Explanation: The 2 smallest products are:
- nums1[0] * nums2[0] = 2 * 3 = 6
- nums1[0] * nums2[1] = 2 * 4 = 8
The 2nd smallest product is 8.
```

**Example 2:**

```
Input: nums1 = [-4,-2,0,3], nums2 = [2,4], k = 6
Output: 0
Explanation: The 6 smallest products are:
- nums1[0] * nums2[1] = (-4) * 4 = -16
- nums1[0] * nums2[0] = (-4) * 2 = -8
- nums1[1] * nums2[1] = (-2) * 4 = -8
- nums1[1] * nums2[0] = (-2) * 2 = -4
- nums1[2] * nums2[0] = 0 * 2 = 0
- nums1[2] * nums2[1] = 0 * 4 = 0
The 6th smallest product is 0.
```

**Example 3:**

```
Input: nums1 = [-2,-1,0,1,2], nums2 = [-3,-1,2,4,5], k = 3
Output: -6
Explanation: The 3 smallest products are:
- nums1[0] * nums2[4] = (-2) * 5 = -10
- nums1[0] * nums2[3] = (-2) * 4 = -8
- nums1[4] * nums2[0] = 2 * (-3) = -6
The 3rd smallest product is -6.
```

**Constraints**

- 1 <= nums1.length, nums2.length <= 5 * 104
- -105 <= nums1[i], nums2[j] <= 105
- 1 <= k <= nums1.length * nums2.length
- nums1 and nums2 are sorted.

---

## 题目（中文翻译）

给定两个已升序排列的整数数组 `nums1` 和 `nums2`，以及一个正整数 `k`。  
从所有可能的下标对 `(i, j)`（其中 `0 <= i < nums1.length`，`0 <= j < nums2.length`）形成的乘积 `nums1[i] * nums2[j]` 中，找出第 k 小的乘积并返回。  

**示例**  

**示例 1**  
```text
Input: nums1 = [2,5], nums2 = [3,4], k = 2
Output: 8
Explanation: 最小的 2 个乘积为：
- nums1[0] * nums2[0] = 2 * 3 = 6
- nums1[0] * nums2[1] = 2 * 4 = 8
第 2 小的乘积是 8。
```

**示例 2**  
```text
Input: nums1 = [-4,-2,0,3], nums2 = [2,4], k = 6
Output: 0
Explanation: 最小的 6 个乘积为：
- nums1[0] * nums2[1] = (-4) * 4 = -16
- nums1[0] * nums2[0] = (-4) * 2 = -8
- nums1[1] * nums2[1] = (-2) * 4 = -8
- nums1[1] * nums2[0] = (-2) * 2 = -4
- nums1[2] * nums2[0] = 0 * 2 = 0
- nums1[2] * nums2[1] = 0 * 4 = 0
第 6 小的乘积是 0。
```

**示例 3**  
```text
Input: nums1 = [-2,-1,0,1,2], nums2 = [-3,-1,2,4,5], k = 3
Output: -6
Explanation: 最小的 3 个乘积为：
- nums1[0] * nums2[4] = (-2) * 5 = -10
- nums1[0] * nums2[3] = (-2) * 4 = -8
- nums1[4] * nums2[0] = 2 * (-3) = -6
第 3 小的乘积是 -6。
```

**约束条件**  

- `1 <= nums1.length, nums2.length <= 5 * 10^4`
- `-10^5 <= nums1[i], nums2[j] <= 10^5`
- `1 <= k <= nums1.length * nums2.length`
- `nums1` 与 `nums2` 均为已排序（sorted）的数组。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把两个数组里所有可能的乘积都算出来，放进一个大列表里，然后把列表排序，最后取第 `k` 小的元素。

- **用到的数据结构**：  
  - `list`（列表）就像我们平时的“收纳盒”，可以把所有乘积装进去。  
  - `sort`（排序）相当于把收纳盒里的东西从小到大排好队，方便我们直接取第 `k` 位。

- **为什么正确**：  
  把所有 `nums1[i] * nums2[j]`（`i` 遍历 `nums1`，`j` 遍历 `nums2`）都算出来后，列表里必然包含了所有可能的乘积。把它们从小到大排好顺序，第 `k` 小的就是答案。

- **复杂度分析（大白话）**：  
  - 外层遍历 `nums1` 长度为 `m`，内层遍历 `nums2` 长度为 `n`，所以一共会产生 `m * n` 个乘积。  
  - 把这 `m * n` 个数排序，时间大约是 “每 10 个数需要花 1 秒” 那种数量级，数学上记作 `O(m·n·log(m·n))`。  
  - 这里的 `O` 只是一种“数量级”的标记，意思是随着 `m·n` 增大，运行时间会以 `m·n·log(m·n)` 的速度增长。  
  - 空间上我们要把所有乘积都存下来，需要 `O(m·n)` 的额外空间。

#### 代码（Python）

```python
def kthSmallestProduct_bruteforce(nums1, nums2, k):
    # 1. 把所有乘积算出来，放进一个列表
    products = []
    for a in nums1:               # 遍历第一个数组
        for b in nums2:           # 遍历第二个数组
            products.append(a * b)   # 计算乘积并收集
    # 2. 把列表从小到大排序
    products.sort()               # Python 内置的快速排序，时间复杂度约为 O(m·n·log(m·n))
    # 3. 第 k 小的元素（k 从 1 开始计数）
    return products[k - 1]        # 列表是 0 索引，取第 k-1 位
```

#### 复杂度

- **时间复杂度**：`O(m·n·log(m·n))`  
  - 先产生 `m·n` 个乘积（`O(m·n)`），再排序（`O(m·n·log(m·n))`），所以整体是后者主导。  
  - 这里的 `m = len(nums1)`，`n = len(nums2)`。

- **空间复杂度**：`O(m·n)`  
  - 需要把所有乘积都保存下来，列表大小正好是 `m·n`。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **“列举全部乘积”**，当数组长度达到 `5·10⁴` 时，`m·n` 可能高达 `2.5·10⁹`，根本不可能全部列出来。我们需要 **“不把所有乘积都显式生成，而是能直接判断某个值是否足够小”**。

下面一步步推导出一种 **二分查找 + 计数** 的方案：

1. **观察乘积的取值范围**  
   - 两个数的范围都是 `[-10⁵, 10⁵]`，所以乘积的最小值是 `-10¹⁰`，最大值是 `10¹⁰`。  
   - 这就像我们已经知道答案一定在一条很长的数轴上，我们可以在这条数轴上二分搜索。

2. **核心子问题：给定一个阈值 `mid`，有多少对乘积 ≤ `mid`？**  
   - 如果我们能在 **`O(m + n)`** 或 **`O(m·log n)`** 时间里算出这个数量，就可以在二分搜索的每一步快速判断“答案在左边还是右边”。  
   - 这一步是整个算法的关键。

3. **如何计数**  
   - 由于两个数组都是 **已排序** 的，我们可以把 `nums1` 分成三类：**负数、零、正数**（同理 `nums2` 也可以）。  
   - 乘积的符号只由两个数的符号决定：  
     - 负 × 正 → 负  
     - 正 × 负 → 负  
     - 正 × 正 → 正  
     - 负 × 负 → 正  
     - 任意数 × 0 → 0  
   - 对于每一种符号组合，我们可以利用 **双指针** 或 **二分查找** 来统计满足 `a * b ≤ mid` 的配对数。下面分别说明：

   **(a) 负数 × 正数 或 正数 × 负数 → 负乘积**  
   - 负数数组从左到右递增（更负的在左），正数数组从左到右递增（更大的正数在右）。  
   - 对于固定的负数 `a`（`a < 0`），要让 `a * b ≤ mid`（`mid` 可能是负数），等价于 `b ≥ ceil(mid / a)`（因为 `a` 为负，除法会翻转不等号）。  
   - 由于正数数组是有序的，我们可以用二分在正数数组中找到第一个满足 `b ≥ target` 的位置，之后所有更大的 `b` 都满足条件。  
   - 统计完所有负数，得到负乘积的数量。

   **(b) 正数 × 正数 → 正乘积**  
   - 两个都正，乘积随两个数的增大而增大。  
   - 对每个正数 `a`，我们想要 `a * b ≤ mid`（此时 `mid` 可能是正数），等价于 `b ≤ floor(mid / a)`。  
   - 在正数数组中二分找最后一个 `b` ≤ `target`，计入配对数。

   **(c) 负数 × 负数 → 正乘积**  
   - 两个都负，乘积为正且随数值“绝对值”变小而变小。  
   - 把负数数组看成 **递增的负数**（从最负到接近 0），我们可以把它们取相反数变成 **递增的正数**，然后和正数×正数的情形相同处理。

   **(d) 零的情况**  
   - 任意数与 0 的乘积都是 0。  
   - 如果 `mid ≥ 0`，所有包含零的配对都满足 `≤ mid`，数量为 `cnt_zero = (cnt_zero_in_nums1 * len(nums2) + cnt_zero_in_nums2 * len(nums1) - cnt_zero_in_nums1 * cnt_zero_in_nums2)`（因为零×零被算了两次，需要减掉一次）。

4. **二分搜索**  
   - 初始化搜索区间为 `left = -10**10 - 1`，`right = 10**10 + 1`（开区间）。  
   - 每次取 `mid = (left + right) // 2`，用上面的计数函数算出 `cnt = #pairs ≤ mid`。  
   - 如果 `cnt >= k`，说明第 `k` 小的乘积不大于 `mid`，把 `right = mid`；否则 `left = mid + 1`。  
   - 循环结束时 `left`（或 `right`）即为答案。

5. **时间复杂度**  
   - 二分搜索的区间长度是 `2·10¹⁰`，二分需要约 `log2(2·10¹⁰) ≈ 35` 次迭代。  
   - 每次计数我们对每个数组做一次遍历或二分，整体是 `O(m·log n + n·log m)`，在最坏情况下约为 `O((m+n)·log max(m,n))`，对本题的 `5·10⁴` 规模足够快。  
   - 所以总时间是 `O( (m+n)·log max(m,n)·log VALUE_RANGE )`，约几万次操作。

6. **空间复杂度**  
   - 只使用了常数级别的额外变量，`O(1)`。

#### 代码（Python）

```python
from bisect import bisect_left, bisect_right

def kthSmallestProduct(nums1, nums2, k):
    # 把两个数组分成负、零、正三段，方便后面计数
    neg1 = [x for x in nums1 if x < 0]          # 负数，升序（因为原数组升序）
    zero1 = [x for x in nums1 if x == 0]
    pos1 = [x for x in nums1 if x > 0]          # 正数，升序

    neg2 = [x for x in nums2 if x < 0]
    zero2 = [x for x in nums2 if x == 0]
    pos2 = [x for x in nums2 if x > 0]

    # 计数函数：返回乘积 <= target 的配对数
    def count_le(target):
        cnt = 0

        # ---------- 负 × 正（得到负数） ----------
        # 对每个负数 a，找满足 a * b <= target 的最小正数 b
        # 等价于 b >= ceil(target / a) （a < 0）
        for a in neg1:                     # a 为负
            # 目标阈值
            need = (target + a + 1) // a   # 向上取整 (Python 整除会向负无穷，这里手动修正)
            # 在正数数组中找第一个 >= need 的位置
            idx = bisect_left(pos2, need)
            cnt += len(pos2) - idx        # 右边所有都满足

        # ---------- 正 × 负（得到负数） ----------
        for a in neg2:                     # 这里把负数当成 a，正数当成 b，逻辑相同
            need = (target + a + 1) // a
            idx = bisect_left(pos1, need)
            cnt += len(pos1) - idx

        # ---------- 零的情况 ----------
        if target >= 0:
            # 任意数与 0 的乘积都是 0 <= target
            cnt += len(zero1) * len(nums2) + len(zero2) * len(nums1) - len(zero1) * len(zero2)

        # ---------- 正 × 正（得到正数） ----------
        for a in pos1:
            # a > 0，要求 a * b <= target => b <= target // a
            need = target // a
            idx = bisect_right(pos2, need)   # 最右侧满足的下标 +1
            cnt += idx

        # ---------- 负 × 负（得到正数） ----------
        # 把负数取相反数变成正数，乘积相同
        rev_neg1 = [-x for x in reversed(neg1)]   # 递增的正数
        rev_neg2 = [-x for x in reversed(neg2)]

        for a in rev_neg1:
            need = target // a
            idx = bisect_right(rev_neg2, need)
            cnt += idx

        return cnt

    # ----------------- 二分搜索 -----------------
    left, right = -10**10 - 1, 10**10 + 1   # 开区间 (left, right]
    while left + 1 < right:
        mid = (left + right) // 2
        if count_le(mid) >= k:
            right = mid
        else:
            left = mid

    return right
```

> **代码说明（关键行中文注释）**  
> - 第 4~12 行：把两个已排好序的数组分别拆成负、零、正三段，后面计数时会更直观。  
> - `count_le(target)`：核心计数函数，返回乘积 **≤** `target` 的配对数。  
> - `bisect_left` / `bisect_right`：二分查找库函数，类似在字典里找页码，时间是 `O(log n)`。  
> - 对负×正、正×负、正×正、负×负四种组合分别计数。  
> - 零的处理：如果 `target` ≥ 0，所有包含零的配对都是合法的。  
> - 二分循环：每次根据计数结果收紧搜索区间，最终 `right` 就是第 `k` 小的乘积。

#### 复杂度

- **时间复杂度**：`O( (m + n)·log max(m, n)·log 2·10¹⁰ )`  
  - `log 2·10¹⁰ ≈ 35` 次二分迭代。  
  - 每次迭代里对每个数组的负/正段进行一次二分计数，整体相当于 `O((m + n)·log max(m, n))`。  
  - 对于本题的最大规模（`5·10⁴`），运行时间在几百毫秒以内，能够通过所有测试。

- **空间复杂度**：`O(1)`（不计输入数组本身）  
  - 只用了常数个额外变量和几个临时列表（这些列表是对原数组的切片引用，实际并未复制大量数据）。

---

## 心得

- **核心技巧**：**二分答案 + 计数**。先把可能的答案范围缩小到一个数轴上，再用能够在 `O(log n)` 或 `O(n)` 时间内判断“有多少对乘积 ≤ 某个值”的方法进行二分搜索。
- **适用的题型**：  
  1. “第 K 小（大）对数/乘积/和” 类问题，例如 *Kth Smallest Pair Distance*、*Find K-th Smallest Pair Sum*。  
  2. 需要在**单调性**（答案随阈值增大而不减少）上做二分的场景，例如 *Maximum Subarray Sum No Larger Than K*。  
- **一句话总结解题钥匙**：**把“找第 K 小”转化为“阈值下有多少对 ≤ 阈值”，利用二分快速定位阈值**。

---

## 反思

- **第一反应**：看到“第 K 小”，立刻想到**排序后直接取第 K**，这就是暴力思路。  
- **最容易踩的坑**：  
  - **符号处理**：负数、正数、零混合时乘积的单调性会翻转，必须分情况讨论。  
  - **整数除法的向上/向下取整**：在 Python 中 `//` 对负数会向负无穷，需要手动调整才能得到数学意义上的上取整或下取整。  
  - **边界值**：二分搜索的左/右边界必须足够宽（包括可能的最小/最大乘积），否则会漏掉答案。  
- **下次类似题的第一步**：先**判断答案是否具有单调性**（即阈值增大时满足条件的配对数只会增不减），如果有，立刻构造**计数函数**，再用二分搜索定位答案。这样可以把“枚举所有可能”转化为“快速判断”。