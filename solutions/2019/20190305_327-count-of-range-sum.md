# #327. 区间和计数 / Count of Range Sum

> 难度：困难 · 标签：Array、Binary Search、Divide and Conquer、Binary Indexed Tree、Segment Tree、Merge Sort、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/count-of-range-sum/)

---

## 题目（英文原版）

**Description**

Given an integer array nums and two integers lower and upper, return the number of range sums that lie in [lower, upper] inclusive.
Range sum S(i, j) is defined as the sum of the elements in nums between indices i and j inclusive, where i <= j.

**Examples**

**Example 1:**

```
Input: nums = [-2,5,-1], lower = -2, upper = 2
Output: 3
Explanation: The three ranges are: [0,0], [2,2], and [0,2] and their respective sums are: -2, -1, 2.
```

**Example 2:**

```
Input: nums = [0], lower = 0, upper = 0
Output: 1
```

**Constraints**

- 1 <= nums.length <= 105
- -231 <= nums[i] <= 231 - 1
- -105 <= lower <= upper <= 105
- The answer is guaranteed to fit in a 32-bit integer.

---

## 题目（中文翻译）

给定一个整数数组（integer array）`nums`，以及两个整数 `lower` 和 `upper`，返回落在闭区间 `[lower, upper]` 之间的范围和（range sum）的个数。

范围和 `S(i, j)` 定义为 `nums` 中下标从 `i` 到 `j`（包含 `i`、`j`）的元素之和，其中 `i ≤ j`。

## 示例

### 示例 1

**输入**  
`nums = [-2,5,-1], lower = -2, upper = 2`

**输出**  
`3`

**解释**  
满足条件的三个区间分别是 `[0,0]`、`[2,2]` 和 `[0,2]`，它们对应的范围和为 `-2`、`-1`、`2`。

### 示例 2

**输入**  
`nums = [0], lower = 0, upper = 0`

**输出**  
`1`

## 约束条件

- `1 <= nums.length <= 10^5`
- `-2^31 <= nums[i] <= 2^31 - 1`
- `-10^5 <= lower <= upper <= 10^5`
- 答案保证能够放入 32 位整数。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把所有可能的子数组都枚举出来，逐个求和，再判断这个和是否落在 `[lower, upper]` 区间。  

- **枚举子数组**：我们可以用两个下标 `i`（子数组左端）和 `j`（右端），`i ≤ j`。  
- **求子数组和**：把 `nums[i] … nums[j]` 的元素加起来。  
- **检查范围**：如果和 `s` 满足 `lower ≤ s ≤ upper`，计数器加一。  

> **类比**：把数组想象成一排书，`i`、`j` 就是你要从第几本书开始读到第几本书结束，读完后把书页数相加，看是不是在老师给的 “页数范围” 里。

**为什么正确**：我们遍历了 **所有** 合法的 `(i, j)` 组合，任何满足条件的子数组都会被统计一次，所以答案一定完整。

#### 代码（Python）  

```python
def countRangeSum_brute(nums, lower, upper):
    n = len(nums)
    ans = 0                     # 计数器

    # 枚举左端点 i
    for i in range(n):
        cur_sum = 0              # 动态维护从 i 到 j 的累计和，避免每次都重新遍历
        # 枚举右端点 j（i ≤ j）
        for j in range(i, n):
            cur_sum += nums[j]   # 累加新的元素
            # 判断当前子数组和是否在区间内
            if lower <= cur_sum <= upper:
                ans += 1

    return ans
```

> **关键点注释**  
> - `cur_sum` 用来 **增量** 累加，而不是每次都 `sum(nums[i:j+1])`，这样可以省掉一次内部循环的开销。  
> - 两层 `for` 循环把所有 `(i, j)` 组合都遍历到了。

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 解释：外层循环 `n` 次，内层平均也要遍历约 `n/2` 次，所以大约是 `n × n/2 ≈ n²/2`，在大 O 记号里我们只写 `O(n²)`，意思是**随着数组长度增长，运行时间会以平方速度增长**。  
- **空间复杂度**：`O(1)`  
  - 解释：只用了常数个额外变量（计数器、累加和），不随 `n` 增大而增加。

---

### 2. 最优解  

#### 思路  

**瓶颈**：暴力解的两层循环导致 `n²` 次加法，`n` 可达 `10⁵` 时根本跑不完。我们需要把“求子数组和”这一步的代价降到 `O(log n)` 或 `O(1)`，并且避免枚举所有 `(i, j)`。

**核心技巧**：**前缀和 + 归并排序（分治计数）**。  

1. **前缀和**  
   - 定义 `pre[k] = nums[0] + nums[1] + … + nums[k‑1]`（`pre[0] = 0`）。  
   - 那么子数组 `[i, j]` 的和等于 `pre[j+1] – pre[i]`。  
   - 于是问题转化为：在前缀和数组中，找有多少对 `(i, j)`（`i < j`）满足 `lower ≤ pre[j] – pre[i] ≤ upper`。  

   > **类比**：把每本书的累计页数记下来（前缀和），子数组的页数就是“后一本的累计页数 减 去 前一本的累计页数”。我们只需要比较两本书的累计页数差是否在区间内。

2. **归并排序计数**  
   - 把前缀和数组 `pre` 按下标划分成左右两半，递归地分别排序并计数。  
   - 当左半段和右半段各自已经排好序时，**利用有序性** 可以在 `O(n)` 时间内统计跨段的合法对数：  
     - 对于左段的每个 `pre[i]`，在右段中寻找满足 `pre[i] + lower ≤ pre[j] ≤ pre[i] + upper` 的 `pre[j]`。  
     - 因为右段是有序的，只需要维护两个指针 `l`、`r`，它们只会向右移动，整体线性。  
   - 最后把左右两段合并成有序数组，返回计数。  

   归并排序本身的时间复杂度是 `O(n log n)`，而我们在合并阶段额外做了线性扫描，整体仍是 `O(n log n)`。

**为什么正确**：  
- 前缀和把原始子数组求和转化为两个前缀差，等价不变。  
- 归并排序的分治保证每一对 `(i, j)`（不论在左段、右段还是跨段）都会被恰好一次计数。  
- 归并过程的有序性确保我们能在一次线性扫描中找出所有满足区间的右端点。

#### 代码（Python）  

```python
from typing import List

def countRangeSum(nums: List[int], lower: int, upper: int) -> int:
    # 1. 计算前缀和数组，长度为 n+1，pre[0] = 0
    pre = [0]
    for x in nums:
        pre.append(pre[-1] + x)

    # 2. 归并排序 + 计数的递归函数
    def sort_count(lo: int, hi: int) -> int:
        """对 pre[lo:hi]（左闭右开）进行归并排序，并返回区间和的合法对数"""
        if hi - lo <= 1:          # 区间长度为 0 或 1，天然有序
            return 0

        mid = (lo + hi) // 2
        cnt = sort_count(lo, mid) + sort_count(mid, hi)   # 递归统计左右两段

        # 3. 统计跨段的合法对
        i = j = mid               # i、j 是右段的滑动窗口左边界
        for left in pre[lo:mid]:  # 左段已排好序，逐个遍历
            # 找到第一个满足 pre[right] >= left + lower 的位置
            while i < hi and pre[i] < left + lower:
                i += 1
            # 找到第一个不满足 pre[right] <= left + upper 的位置（即 > upper）
            while j < hi and pre[j] <= left + upper:
                j += 1
            cnt += j - i          # 右段中满足条件的元素个数

        # 4. 合并左右两段，使 pre[lo:hi] 有序
        # 使用 Python 自带的归并（手写也行，这里写得更直观）
        merged = sorted(pre[lo:hi])
        pre[lo:hi] = merged       # 覆盖原区间

        return cnt

    return sort_count(0, len(pre))
```

> **关键行中文注释**  
> - 第 4 行把原数组转成前缀和，`pre[k]` 表示前 `k` 个数的总和。  
> - `sort_count` 是典型的 **归并排序** 框架：先递归左右，再合并。  
> - `while i < hi and pre[i] < left + lower`：左指针 `i` 找到第一个 **不小于** `left+lower` 的位置。  
> - `while j < hi and pre[j] <= left + upper`：右指针 `j` 找到第一个 **大于** `left+upper` 的位置。  
> - `cnt += j - i`：区间 `[i, j)` 中的所有右端点都满足条件，直接计数。  
> - `merged = sorted(pre[lo:hi])`：把当前区间排序，保证后续递归使用的是有序数组。

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 解释：归并排序把数组不断二分，深度为 `log n`，每层合并都要遍历整个数组一次（`n`），所以总工作量是 `n × log n`。相比暴力的 `n²`，**随着 n 增大，运行时间只会增长对数级**，能够轻松处理 `10⁵` 规模的数据。  

- **空间复杂度**：`O(n)`  
  - 解释：我们额外使用了一个同样大小的数组 `merged`（或 `sorted` 产生的临时列表）来存放合并结果，空间随 `n` 成线性增长。递归调用栈的深度为 `log n`，相对于 `n` 可以忽略不计。

---

## 心得  

- **核心技巧**：**前缀和 + 归并排序（或分治计数）**。把“子数组和在区间内”转化为“两个前缀差在区间内”，再利用有序性在合并阶段线性计数。  
- **适用题型**  
  1. **区间和计数**：如本题、`Number of Subarrays with Sum ≤ K`（需要前缀和 + BIT）  
  2. **逆序对计数**：LeetCode 493 “Reverse Pairs” – 同样用归并排序统计满足 `i < j 且 nums[i] > 2*nums[j]` 的对数。  
  3. **区间中位数 / Kth 小**：使用归并或线段树维护有序前缀。  
- **一句话总结**：**把子数组求和转成前缀差，再用归并排序的有序性一次性统计所有满足区间的差值对**。

---

## 反思  

- **第一反应**：直接两层循环暴力枚举，想当然地把所有子数组都算一遍。  
- **最容易踩的坑**  
  1. **整数溢出**（在语言如 C++/Java 中），Python 免疫但要注意题目限制。  
  2. **边界条件**：前缀和数组需要额外的 `0`（表示空前缀），否则会漏掉以第一个元素开始的子数组。  
  3. **指针移动**：在归并计数时，`i`、`j` 必须只向右移动，不能回退，否则会导致 `O(n²)` 的退化。  
- **下次遇到同类题**：第一步先 **构造前缀和**，确认可以把“子数组属性”转化为“前缀差的属性”；随后判断是否能利用 **有序结构（排序、平衡树、BIT）** 在 `O(log n)` 或 `O(n)` 时间内统计满足区间的配对。