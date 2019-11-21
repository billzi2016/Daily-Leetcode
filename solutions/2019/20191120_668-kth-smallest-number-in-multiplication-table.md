# #668. 乘法表中的第 k 小数字 / Kth Smallest Number in Multiplication Table

> 难度：困难 · 标签：Math、Binary Search · [LeetCode 链接](https://leetcode.com/problems/kth-smallest-number-in-multiplication-table/)

---

## 题目（英文原版）

**Description**

Nearly everyone has used the Multiplication Table. The multiplication table of size m x n is an integer matrix mat where mat[i][j] == i * j (1-indexed).
Given three integers m, n, and k, return the kth smallest element in the m x n multiplication table.

**Examples**

**Example 1:**

```
Input: m = 3, n = 3, k = 5
Output: 3
Explanation: The 5th smallest number is 3.
```

**Example 2:**

```
Input: m = 2, n = 3, k = 6
Output: 6
Explanation: The 6th smallest number is 6.
```

**Constraints**

- 1 <= m, n <= 3 * 104
- 1 <= k <= m * n

---

## 题目（中文翻译）

几乎每个人都使用过乘法表（Multiplication Table）。大小为 m × n 的乘法表是一个整数矩阵（integer matrix）`mat`，其中 `mat[i][j] == i * j`（下标从 1 开始计数）。

给定三个整数 m、n 和 k，返回该 m × n 乘法表中第 k 小的元素（element）。

**示例 1**  
**示例 2**  
**约束条件**：

**示例**  
**示例 1:**  
```
Input: m = 3, n = 3, k = 5
Output: 3
```
**解释:** 第 5 小的数字是 3。

**示例 2:**  
```
Input: m = 2, n = 3, k = 6
Output: 6
```
**解释:** 第 6 小的数字是 6。

**约束条件**  
- `1 <= m, n <= 3 * 10^4`  
- `1 <= k <= m * n`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把整个乘法表的所有数字列出来，然后把它们从小到大排好序，取第 k 个就是答案。  

- **数据结构**：我们可以用一个普通的 Python 列表 `arr` 来存放所有的 `i * j`（`i` 从 1 到 `m`，`j` 从 1 到 `n`）。列表就像生活中的“收集盒”，把所有数字装进去。  
- **正确性**：因为乘法表里每个位置只出现一次，遍历完所有 `(i, j)` 就能得到完整的集合。对这个集合进行排序后，第 k 小的元素必然就是我们要的答案。  

#### 代码（Python）  

```python
def kthSmallest_bruteforce(m: int, n: int, k: int) -> int:
    # 1. 把所有 i*j 放进列表
    vals = []
    for i in range(1, m + 1):          # i 代表行号，像“第 i 行”
        for j in range(1, n + 1):      # j 代表列号，像“第 j 列”
            vals.append(i * j)         # 把乘积加入列表

    # 2. 对列表排序，Python 的 sort 用的就是 Timsort，平均 O(N log N)
    vals.sort()

    # 3. 第 k 小的元素下标是 k-1（因为下标从 0 开始）
    return vals[k - 1]
```

#### 复杂度  

- **时间复杂度**：`O(m * n log (m * n))`  
  - 生成所有 `m·n` 个数需要 `O(m·n)`，排序需要 `O(m·n log(m·n))`。  
  - 用大白话说，如果表有 10 000 个数字，排序大概是“先把它们一遍遍看一遍（10 000 次），再把它们按顺序排好（每次排的过程又要比较几次），整体比直接看一遍要慢很多”。  

- **空间复杂度**：`O(m * n)`  
  - 我们把所有数字都存进了列表，需要额外的内存与表的大小等价。  

---

### 2. 最优解  

#### 思路  
暴力解的瓶颈在 **生成并排序全部 `m·n` 个数**。当 `m`、`n` 都可能达到 3 × 10⁴ 时，`m·n` 最多会有 9 × 10⁸，根本装不下，也不可能在合理时间内排序。  
我们需要 **不显式生成全部数字**，而是利用乘法表的特殊结构来快速判断“某个数 X 在表里出现了多少次”。如果能在 `O(m log max)` 甚至 `O(m)` 的时间内算出 “≤ X 的元素个数”，就可以用 **二分查找**（binary search）在答案空间 `[1, m·n]` 上定位第 k 小的数。

**关键点 1：二分查找**  
二分查找像是“猜数字游戏”。我们先猜一个数 `mid`，然后检查表里有多少个元素 **不大于** `mid`。  
- 如果这个数量 **≥ k**，说明第 k 小的数一定 ≤ `mid`，于是把搜索区间右边界收紧到 `mid`。  
- 否则第 k 小的数在 `mid` 的右边，左边界移动到 `mid + 1`。  
不断逼近，最后左边界就是答案。

**关键点 2：如何快速统计 ≤ mid 的元素个数**  
观察第 `i` 行（`i` 从 1 到 `m`），这一行的数是 `i, 2i, 3i, …, n*i`。在这行里，**不大于 `mid` 的数的个数** 等价于 `mid // i`（整数除），但最多也只能有 `n` 个（因为一行只有 `n` 列）。于是：

```
cnt(mid) = sum_{i=1}^{m} min( n, mid // i )
```

这一步只需要遍历 `m` 行，时间 `O(m)`，不需要遍历 `n` 列。把它放进二分查找的判断里，就得到整体 `O(m log (m·n))` 的解法。

**类比**：把每一行想象成一本书，`i` 是这本书的“字数基准”。我们要统计“字数 ≤ mid 的页数”，只要除一下就知道了。

#### 代码（Python）  

```python
def kthSmallest(m: int, n: int, k: int) -> int:
    # 为了让循环次数更少，保证 m <= n
    if m > n:
        m, n = n, m

    # 二分搜索的左、右边界
    lo, hi = 1, m * n   # 最小可能是 1，最大可能是 m*n（左下角的最大乘积）

    while lo < hi:
        mid = (lo + hi) // 2          # 猜一个中间值

        # 统计乘法表里 ≤ mid 的元素个数
        cnt = 0
        for i in range(1, m + 1):
            # 第 i 行中 ≤ mid 的数有 min(n, mid // i) 个
            cnt += min(n, mid // i)

        # 根据 cnt 与 k 的关系收紧搜索区间
        if cnt >= k:                  # 足够多，答案在左侧（包括 mid）
            hi = mid
        else:                         # 不够多，答案在右侧
            lo = mid + 1

    # 循环结束时 lo == hi，即为第 k 小的数
    return lo
```

#### 复杂度  

- **时间复杂度**：`O(m log (m*n))`  
  - 二分查找的迭代次数是 `log₂(m*n)`（大约 30 次，因为 `m*n ≤ 9e8`），每次需要遍历 `m` 行做计数，所以整体是 `m` 乘以二分的次数。  
  - 用通俗的话说：我们只看每一行一次（而不是每个格子），再“猜-检”大约三十次，就找到了答案，比一次性列出所有格子快了几个数量级。  

- **空间复杂度**：`O(1)`  
  - 只用了常数个额外变量（`lo、hi、mid、cnt`），不随 `m、n` 增长。  

---

## 心得  

- **核心技巧**：**二分查找 + 计数函数**（在单调函数上搜索）。  
- **适用的题型**：  
  1. “第 K 小/大元素”类的矩阵或数列问题（如第 K 小的有序矩阵元素）。  
  2. “满足某条件的最小/最大值”类的优化问题（如在数组中找最小的满足子数组和 ≥ target 的长度）。  
- **一句话总结解题钥匙**：把“找第 k 小”转化为“在一个单调递增的计数函数上二分”，无需真的把所有元素列出来。  

---

## 反思  

- **第一反应**：直接把乘法表展开、排序——因为这一步最直观、最容易写出来。  
- **最容易踩的坑**：  
  - **时间超限**：`m·n` 可能非常大，不能真的生成整个表。  
  - **计数溢出**：在统计 `cnt` 时可能会超过 Python 的整数范围？（Python 整数自动大数化，一般不怕）但要注意 `mid // i` 可能大于 `n`，必须取 `min(n, …)`。  
  - **边界条件**：当 `k = 1` 或 `k = m*n` 时，答案分别是 `1` 与 `m*n`，二分搜索的区间必须包含这两个端点。  
- **下次类似题的第一步**：先思考“有没有单调的判定函数”，如果有，就立刻考虑二分查找，而不是直接构造完整数据。这样可以把时间复杂度从指数/平方级降到对数级。