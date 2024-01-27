# #2563. 统计公平数对的数量 / Count the Number of Fair Pairs

> 难度：中等 · 标签：Array、Two Pointers、Binary Search、Sorting · [LeetCode 链接](https://leetcode.com/problems/count-the-number-of-fair-pairs/)

---

## 题目（英文原版）

**Description**

Given a 0-indexed integer array nums of size n and two integers lower and upper, return the number of fair pairs.
A pair (i, j) is fair if:

**Examples**

**Example 1:**

```
Input: nums = [0,1,7,4,4,5], lower = 3, upper = 6
Output: 6
Explanation: There are 6 fair pairs: (0,3), (0,4), (0,5), (1,3), (1,4), and (1,5).
```

**Example 2:**

```
Input: nums = [1,7,9,2,5], lower = 11, upper = 11
Output: 1
Explanation: There is a single fair pair: (2,3).
```

**Constraints**

- 1 <= nums.length <= 105
- nums.length == n
- -109 <= nums[i] <= 109
- -109 <= lower <= upper <= 109

---

## 题目（中文翻译）

**题目描述**  
给定一个下标从 0 开始的整数数组（array）`nums`，其长度为 `n`，以及两个整数 `lower` 和 `upper`，请返回满足条件的公平数对（fair pair）的数量。

如果一对下标 `(i, j)`（其中 `0 <= i < j < n`）满足  
`lower <= nums[i] + nums[j] <= upper`，则称该数对为 **公平数对**。

---

**示例**

**示例 1**  
输入：`nums = [0,1,7,4,4,5]`, `lower = 3`, `upper = 6`  
输出：`6`  
解释：共有 6 对公平数对：`(0,3)`, `(0,4)`, `(0,5)`, `(1,3)`, `(1,4)`, `(1,5)`。

**示例 2**  
输入：`nums = [1,7,9,2,5]`, `lower = 11`, `upper = 11`  
输出：`1`  
解释：唯一的公平数对是 `(2,3)`。

---

**约束条件**  

- `1 <= nums.length <= 10^5`
- `nums.length == n`
- `-10^9 <= nums[i] <= 10^9`
- `-10^9 <= lower <= upper <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把所有可能的下标组合枚举一遍，逐个检查它们是否满足 “公平” 的条件。  
- **枚举方式**：双层循环，外层遍历 `i`（从 `0` 到 `n-2`），内层遍历 `j`（从 `i+1` 到 `n-1`），因为题目要求 `i < j`。  
- **判断条件**：计算 `nums[i] + nums[j]`，如果它落在区间 `[lower, upper]` 之间，就算是一对公平的配对，计数器 `cnt` 加一。  

**生活化类比**：把数组想象成一排小朋友，老师要挑出两个人站在一起，要求他们的身高和（即 `nums[i] + nums[j]`）在规定的区间里。老师会一个一个地把所有可能的两个人配对尝试，看是否符合要求，这就是暴力枚举的过程。

**为什么正确**：因为我们把所有合法的 `(i, j)` 都检查了一遍，凡是满足条件的必然被计数，凡是不满足的必然被排除，所以答案一定是完整且准确的。

#### 代码（Python）

```python
def countFairPairs_bruteforce(nums, lower, upper):
    n = len(nums)
    cnt = 0                     # 记录公平配对的数量
    # 双层循环枚举所有 i < j 的组合
    for i in range(n - 1):      # i 最多到倒数第二个元素
        for j in range(i + 1, n):
            s = nums[i] + nums[j]   # 两数之和
            # 判断是否在 [lower, upper] 区间内
            if lower <= s <= upper:
                cnt += 1            # 符合条件，计数器加一
    return cnt
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - “平方”表示如果数组长度是 `n`，我们大约要检查 `n*(n-1)/2` 对数（想象成一个 `n` 行 `n` 列的表格，只看上三角形），所以时间会随 `n` 的增大而 **非常快** 地增长。比如 `n=10⁵` 时，`n²` 已经是 `10¹⁰`，根本跑不完。  
- **空间复杂度**：`O(1)`  
  - 只用了几个额外的整数变量（计数器、循环下标），不随 `n` 增大而增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每一次都要遍历所有后面的元素**，导致 `O(n²)` 的时间。我们可以利用**排序 + 双指针**（或二分搜索）把检查的次数压到 `O(n log n)`。

1. **先把数组排序**（升序）。  
   排序后，若固定一个数 `nums[i]`，满足 `lower ≤ nums[i] + nums[j] ≤ upper` 的 `j` 必然在一个连续的区间 `[L, R]`（因为数组是单调递增的）。  
2. 对每个 `i`，我们需要找出：
   - 第一个 **不小于** `lower - nums[i]` 的下标 `left`（即 `nums[left]` 是能让和达到下限的最小数）。  
   - 最后一个 **不大于** `upper - nums[i]` 的下标 `right`（即 `nums[right]` 是还能让和不超上限的最大数）。  
3. 这两个下标可以用 **二分查找**（`bisect_left` / `bisect_right`）在已经排好序的数组里快速定位，时间是 `O(log n)`。  
4. 对于当前 `i`，满足条件的配对数就是 `right - left + 1`（注意只统计下标 **大于 i** 的元素）。  
5. 把所有 `i` 的结果累加，即得到答案。  

**核心技巧解释**  
- **二分查找**：想象在一本排好序的字典里找某个单词的位置。我们每次把搜索范围砍掉一半，快速逼近目标位置。Python 标准库的 `bisect` 模块已经帮我们实现了这一步。  
- **前缀区间**：因为数组是升序的，满足 `lower ≤ nums[i] + nums[j]` 的 `j` 必然在某个位置以后才开始满足；同理，满足 `nums[i] + nums[j] ≤ upper` 的 `j` 必然在某个位置以前就已经超出上限。于是这些 `j` 形成了一个连续区间，直接算长度就行了。

#### 代码（Python）

```python
from bisect import bisect_left, bisect_right

def countFairPairs(nums, lower, upper):
    nums.sort()                     # 1. 先升序排序
    n = len(nums)
    cnt = 0

    for i in range(n - 1):         # 只需要遍历到倒数第二个元素
        # 2. 计算当前 i 能配对的数值范围
        left_val  = lower - nums[i]   # 和要 >= lower 时，另一个数最小需要多少
        right_val = upper - nums[i]   # 和要 <= upper 时，另一个数最大能有多少

        # 3. 在排序好的数组里二分定位
        #   只在 i 右侧（i+1 .. n-1）搜索，所以把搜索区间限制为 (i+1, n)
        left  = bisect_left(nums, left_val, i + 1, n)   # 第一个 >= left_val 的位置
        right = bisect_right(nums, right_val, i + 1, n) - 1  # 最后一个 <= right_val 的位置

        # 4. 统计合法配对数
        if left <= right:           # 说明区间非空
            cnt += (right - left + 1)

    return cnt
```

**代码要点中文注释**  
- `bisect_left(a, x, lo, hi)` 在 `[lo, hi)` 区间内找到第一个 **不小于** `x` 的位置。  
- `bisect_right(a, x, lo, hi)` 在 `[lo, hi)` 区间内找到第一个 **大于** `x` 的位置，减一即得到最后一个 **不大于** `x` 的下标。  
- 我们把搜索范围限定在 `i+1` 之后，保证 `i < j`。

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 排序需要 `O(n log n)`。随后对每个 `i`（共 `n` 次）做两次二分查找，每次 `O(log n)`，合计也是 `O(n log n)`。相较于 `O(n²)`，当 `n=10⁵` 时，这个复杂度可以在毫秒级完成。  
- **空间复杂度**：`O(1)`（不计排序本身使用的 `O(n)` 额外空间）  
  - 只用了常数个额外变量 `cnt、left、right…`，没有额外的数据结构随 `n` 增长。

---

## 心得

- **核心技巧**：**排序 + 二分定位**（或对应的双指针）把“找区间”从线性遍历压到对数级别。  
- **适用的题型**：  
  1. 统计满足 `a[i] + a[j]` 在某个区间的配对数（本题）。  
  2. “两数之和”变体，如 “求和在区间内的最小/最大长度子数组”。  
  3. “计数满足不等式的元素对”类题目，例如 LeetCode 974 *子数组长度的最小和*（思路相似的滑动窗口/双指针）。  
- **一句话总结解题钥匙**：**先把数据排好序，再用二分/双指针一次性定位合法区间**。

---

## 反思

- **第一反应**：直接写双层循环枚举，想到“暴力”。  
- **最容易踩的坑**：  
  - 忘记限制 `j > i`，导致统计了重复或非法的配对。  
  - 二分搜索的左闭右开区间写错，导致 `left`、`right` 越界或漏掉边界元素。  
  - 当 `left_val` 大于所有后面的元素或 `right_val` 小于所有后面的元素时，需要判断区间是否为空（`left <= right`）。  
- **下次遇到同类题的第一步**：**先思考能否把 “范围条件” 转化为 “在排好序的数组里找区间”，如果可以，就立刻考虑排序 + 二分（或双指针）来实现**。