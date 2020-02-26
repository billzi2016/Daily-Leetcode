# #786. **第 K 小的素数分数** / K-th Smallest Prime Fraction

> 难度：中等 · 标签：Array、Two Pointers、Binary Search、Sorting、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/k-th-smallest-prime-fraction/)

---

## 题目（英文原版）

**Description**

You are given a sorted integer array arr containing 1 and prime numbers, where all the integers of arr are unique. You are also given an integer k.
For every i and j where 0 <= i < j < arr.length, we consider the fraction arr[i] / arr[j].
Return the kth smallest fraction considered. Return your answer as an array of integers of size 2, where answer[0] == arr[i] and answer[1] == arr[j].

**Examples**

**Example 1:**

```
Input: arr = [1,2,3,5], k = 3
Output: [2,5]
Explanation: The fractions to be considered in sorted order are:
1/5, 1/3, 2/5, 1/2, 3/5, and 2/3.
The third fraction is 2/5.
```

**Example 2:**

```
Input: arr = [1,7], k = 1
Output: [1,7]
```

**Constraints**

- 2 <= arr.length <= 1000
- 1 <= arr[i] <= 3 * 104
- arr[0] == 1
- arr[i] is a prime number for i > 0.
- All the numbers of arr are unique and sorted in strictly increasing order.
- 1 <= k <= arr.length * (arr.length - 1) / 2

---

## 题目（中文翻译）

给定一个已排序的整数数组 `arr`，其中包含 `1` 和若干素数，且数组中的所有整数互不相同。再给定一个整数 `k`。  

对于所有满足 `0 <= i < j < arr.length` 的下标对 `(i, j)`，我们考虑分数 `arr[i] / arr[j]`（分子 / 分母）。  

返回第 `k` 小的分数。答案以长度为 `2` 的整数数组返回，其中 `answer[0] == arr[i]`、`answer[1] == arr[j]`。

---

### 示例

#### 示例 1
**输入**  
`arr = [1,2,3,5], k = 3`  

**输出**  
`[2,5]`  

**解释**  
按升序排列需考虑的分数为：  
`1/5, 1/3, 2/5, 1/2, 3/5, 2/3`。  
第三小的分数是 `2/5`。

#### 示例 2
**输入**  
`arr = [1,7], k = 1`  

**输出**  
`[1,7]`  

---

### 约束条件

- `2 <= arr.length <= 1000`
- `1 <= arr[i] <= 3 * 10^4`
- `arr[0] == 1`
- 对于 `i > 0`，`arr[i]` 为素数（prime）
- `arr` 中的所有数字唯一且严格递增排序
- `1 <= k <= arr.length * (arr.length - 1) / 2`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把 **所有合法的分数** 都枚举出来，放进一个列表，然后把列表从小到大排序，最后取第 `k` 小的那个。  

- **数据结构**：我们用一个普通的 Python 列表 `fractions` 来存放 `(分子, 分母, 值)` 三元组。  
  - 把分数的值存成 `float`（或者 `Fraction`），相当于把分数“翻译成小数”，这样 Python 的 `sort` 能直接比较大小。  
  - 把分子和分母一起保存是因为答案要求返回原数组中的两个数，而不是小数结果。  

> **类比**：把 `fractions` 想象成一本“分数字典”，每一页记录了一个分数和它对应的大小。我们把这本字典按页码（分数大小）排序，然后翻到第 `k` 页即可。

- **正确性**：因为我们遍历了所有满足 `0 ≤ i < j < n` 的 `(i, j)`，所以没有漏掉任何可能的分数。排序后第 `k` 小的必然是答案。

- **复杂度分析**：  
  - 枚举阶段需要两层循环，外层 `i` 从 `0` 到 `n-2`，内层 `j` 从 `i+1` 到 `n-1`，总共产生 `n·(n-1)/2` 个分数。时间复杂度是 **O(n²)**。  
  - 把所有分数放进列表需要同样的空间，也就是 **O(n²)**（因为最坏情况下要存 `≈ n²/2` 条记录）。  
  - 排序 `O(m log m)`，这里 `m = n·(n-1)/2`，仍然是 **O(n² log n)**，在 `n ≤ 1000` 时还能接受，但在更大的数据下会超时。

> **大白话**：`O(n²)` 就像让你在 1000 张卡片里找两张配对的组合，需要检查大约 500 000 次；`O(n² log n)` 还要把这些组合排个序，像在 500 000 本书里排号，工作量更大。

#### 代码（Python）

```python
from typing import List

def kth_smallest_prime_fraction_bruteforce(arr: List[int], k: int) -> List[int]:
    # 1. 枚举所有分数
    fractions = []                       # 用来存放 (分子, 分母, 分数值) 三元组
    n = len(arr)
    for i in range(n - 1):               # i 为分子下标
        for j in range(i + 1, n):        # j 为分母下标，保证 i < j
            fractions.append((arr[i], arr[j], arr[i] / arr[j]))
            # 这里 arr[i] / arr[j] 直接得到浮点数，方便后面比较大小

    # 2. 按分数值从小到大排序
    fractions.sort(key=lambda x: x[2])   # 只比较第 3 个元素（分数值）

    # 3. 第 k 小的分数对应的分子、分母即为答案
    numerator, denominator, _ = fractions[k - 1]   # k 是从 1 开始计数的
    return [numerator, denominator]
```

#### 复杂度

- **时间复杂度**：`O(n² log n)`  
  - 枚举产生 `≈ n²/2` 条分数 → `O(n²)`  
  - 排序这些分数 → `O(n² log n)`，这一步是主要耗时。

- **空间复杂度**：`O(n²)`  
  - 需要把所有分数都存进列表，最坏情况下要占用约 `n²/2` 条记录的空间。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **枚举所有分数并排序**，这一步产生了 `O(n²)` 的空间和 `O(n² log n)` 的时间。我们可以 **不显式列出所有分数**，而是利用数组已排序的特性，结合 **二分查找 + 双指针**（或 **堆**）来直接定位第 `k` 小的分数。

下面用 **二分查找 + 双指针计数** 的方案，思路如下：

1. **把分数的大小映射到一个实数区间**  
   所有合法分数的值介于 `0`（最小）和 `1`（最大，因为分子 < 分母）之间。我们可以在 `[0, 1]` 区间上二分，猜一个中间值 `mid`，然后统计 **有多少分数 ≤ mid**。

2. **如何在 `O(n)` 时间内统计 ≤ mid 的分数数目？**  
   - 因为 `arr` 已经升序，固定分母 `arr[j]`，分子 `arr[i]` 越大分数越大。  
   - 对每个分母 `j`（从右往左遍历），我们用一个指针 `i`（从左往右）保持 `arr[i] / arr[j] ≤ mid`。  
   - 当 `arr[i] / arr[j] ≤ mid` 成立时，**所有更小的分子 `arr[0..i]`** 与当前分母 `arr[j]` 组合的分数也都 ≤ mid。于是我们可以一次性把 `i+1` 条分数计入统计。  
   - 这个过程只需要一次线性扫描，时间 `O(n)`。

3. **二分的终止条件**  
   - 当 `low` 与 `high` 的差距足够小（如 `1e-9`）时，二分结束。此时 `low`（或 `high`）就是第 `k` 小分数的近似值。  
   - 为了得到**精确的分子分母**，在每一次二分统计的同时，记录下当前 **最大的** `≤ mid` 的分数对应的 `(i, j)`。二分结束后，这个记录就是答案。

4. **核心算法**：  
   - **二分查找**（Binary Search）在实数区间上搜索目标值。  
   - **双指针**（Two Pointers）在有序数组中一次遍历完成计数。  
   - 这两者配合可以把时间从 `O(n² log n)` 降到 **`O(n log precision)`**，空间降到 **`O(1)`**。

> **类比**：想象你在一条长河上寻找第 `k` 小的石子。暴力解是把河里的每块石子捡起来排队；最优解是站在河岸，用望远镜一次看一段河段（即二分），并且用手指快速滑过石子（即双指针），在看完所有段后，你已经知道第 `k` 小的石子在哪里，而不需要把所有石子都搬走。

#### 代码（Python）

```python
from typing import List

def kth_smallest_prime_fraction(arr: List[int], k: int) -> List[int]:
    n = len(arr)
    # 二分的上下界，所有分数都在 (0, 1) 之间
    low, high = 0.0, 1.0
    # 记录当前找到的最接近 low 的分数对应的分子、分母
    best_num, best_den = 0, 1

    # 精度控制：循环 40~50 次即可得到足够精确的结果（2^-40 ≈ 1e-12）
    for _ in range(40):
        mid = (low + high) / 2.0   # 试探的中间值
        # 下面的双指针统计 ≤ mid 的分数个数，同时找出最大的 ≤ mid 的分数
        count = 0                  # ≤ mid 的分数总数
        i = -1                     # 分子指针，初始化为 -1 表示还未找到合法 i
        # 遍历所有可能的分母，从左到右（也可以从右到左，只要保持一致）
        for j in range(1, n):
            # 移动分子指针 i，使得 arr[i] / arr[j] ≤ mid
            # 因为 arr 单调递增，i 只会向右移动
            while i + 1 < j and arr[i + 1] / arr[j] <= mid:
                i += 1
            # 此时 i 为满足条件的最大下标（如果 i == -1，说明没有分子满足 ≤ mid）
            count += i + 1       # i+1 条分数 ≤ mid（下标 0..i）

            # 同时记录当前最大的 ≤ mid 的分数，用于最终返回答案
            if i >= 0:
                # 因为 j 正在增大，当前的分数 arr[i]/arr[j] 可能是所有 ≤mid 中最大的
                if best_num * arr[j] < arr[i] * best_den:   # 比较 a/b 与 c/d，交叉相乘避免浮点误差
                    best_num, best_den = arr[i], arr[j]

        # 根据统计结果决定二分的方向
        if count < k:               # ≤mid 的分数太少，第 k 小在更大的区间
            low = mid
        else:                       # ≥k 条分数已经在 ≤mid 区间，说明答案不大于 mid
            high = mid

    return [best_num, best_den]
```

> **代码说明**  
> - `while i + 1 < j and arr[i + 1] / arr[j] <= mid:`：保证分子下标始终小于分母下标。  
> - `best_num * arr[j] < arr[i] * best_den`：用交叉相乘比较两个分数大小，避免浮点精度问题。  
> - 循环 40 次足以让 `high - low` 小于 `1e-12`，这在整数范围内已经可以唯一确定答案。

#### 复杂度

- **时间复杂度**：`O(n log precision)`  
  - 每一次二分迭代里，双指针遍历数组一次，时间 `O(n)`。  
  - 二分的迭代次数与要求的精度有关（这里取固定 40 次），视作常数。  
  - 与暴力解的 `O(n² log n)` 相比，省去了大量的枚举和排序。

- **空间复杂度**：`O(1)`  
  - 只使用了若干个额外的变量，没有额外的数组或列表，空间开销几乎为常数。

---

## 心得

- **核心技巧**：二分查找实数区间 + 双指针计数（也称 “基于有序数组的计数二分”）。  
- **适用的题型**：  
  1. “第 K 小的配对和/积” 之类的需要在有序数组中统计 ≤ 某阈值的配对数量。  
  2. “K-th Smallest Pair Distance”（LeetCode 719）——同样用二分 + 双指针统计距离。  
  3. “Find K-th Smallest Fraction” 这类分数或比值排序的题目。  
- **一句话总结解题钥匙**：**把“找第 K 小”转化为“判断有多少 ≤ X”，再在 X 上二分**。

---

## 反思

- **第一反应**：看到“所有 i < j 的分数”，自然想到枚举全部组合后排序。  
- **最容易踩的坑**：  
  - **精度问题**：直接比较浮点数容易出现误差，使用交叉相乘或 `Fraction` 能保证正确性。  
  - **指针边界**：分子指针 `i` 必须始终小于分母下标 `j`，否则会产生非法分数。  
  - **计数溢出**：`count` 可能达到 `n·(n-1)/2`，使用 Python 的大整数不会溢出，但在其他语言需要用 64 位整数。  
- **下次遇到同类题**：**先问自己**：是否可以把“第 K 小”转化为“阈值 X 下的计数”。如果可以，立刻尝试二分 + 有序结构的计数技巧。