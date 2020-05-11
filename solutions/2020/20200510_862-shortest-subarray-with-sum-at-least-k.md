# #862. 和至少为 K 的最短子数组 / Shortest Subarray with Sum at Least K

> 难度：困难 · 标签：Array、Binary Search、Queue、Sliding Window、Heap (Priority Queue)、Prefix Sum、Monotonic Queue · [LeetCode 链接](https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/)

---

## 题目（英文原版）

**Description**

Given an integer array nums and an integer k, return the length of the shortest non-empty subarray of nums with a sum of at least k. If there is no such subarray, return -1.
A subarray is a contiguous part of an array.

**Examples**

**Example 1:**

```
Input: nums = [1], k = 1
Output: 1
```

**Example 2:**

```
Input: nums = [1,2], k = 4
Output: -1
```

**Example 3:**

```
Input: nums = [2,-1,2], k = 3
Output: 3
```

**Constraints**

- 1 <= nums.length <= 105
- -105 <= nums[i] <= 105
- 1 <= k <= 109

---

## 题目（中文翻译）

给定一个整数数组（integer array）`nums` 和一个整数 `k`，返回 `nums` 中 **和至少为 `k` 的最短非空子数组（subarray）** 的长度。如果不存在满足条件的子数组，返回 `-1`。  
子数组（subarray）是数组中连续的一段。

**Example 1:**  
**Example 2:**  
**Example 3:**  

约束条件：
- 1 ≤ `nums.length` ≤ 10⁵
- -10⁵ ≤ `nums[i]` ≤ 10⁵
- 1 ≤ `k` ≤ 10⁹

示例：
示例 1:  
Input: nums = [1], k = 1  
Output: 1  

示例 2:  
Input: nums = [1,2], k = 4  
Output: -1  

示例 3:  
Input: nums = [2,-1,2], k = 3  
Output: 3

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法就是把所有可能的 **连续子数组** 都枚举一遍，算出它们的和，看看哪一个满足「和 ≥ k」且长度最短。  

- **数据结构**：我们只需要一个普通的 Python 列表 `nums`，以及两个循环的计数器 `i`、`j`。  
- **生活化类比**：把数组想成一排排糖果，想找出最短的一段糖果，使得它们的甜度之和不小于 `k`。最笨的办法就是把每一段都尝一遍，记录满足条件的最短长度。  

这个方法必然能得到正确答案，因为它遍历了**所有**合法的子数组，肯定不会漏掉最优解。

#### 代码（Python）  

```python
def shortest_subarray_brute(nums, k):
    n = len(nums)
    ans = float('inf')               # 用正无穷表示目前还没有找到合法子数组
    for i in range(n):               # 子数组的左端点
        cur_sum = 0
        for j in range(i, n):        # 子数组的右端点（包括 i 本身）
            cur_sum += nums[j]       # 累加得到 i~j 的和
            if cur_sum >= k:         # 一旦满足条件，就更新答案
                ans = min(ans, j - i + 1)
                break                # 这条子数组已经够短了，继续往右只会更长
    return -1 if ans == float('inf') else ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)`。外层循环 `n` 次，内层最坏情况下也要遍历 `n` 次，两个 `for` 嵌套相当于 **平方级** 的工作量。可以把 `O(n²)` 想象成“如果 `n` 是 10，工作量大约是 100；如果 `n` 是 1000，工作量就变成 1 000 000”。  
- **空间复杂度**：`O(1)`。只用了常数级的额外变量（`cur_sum`、`ans`），不随输入规模增长。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**重复计算子数组的和** 是最大的性能瓶颈。我们可以用「前缀和」把每段子数组的和用一次减法就算出来：  

- **前缀和** `pre[i]` 表示 `nums[0] + … + nums[i‑1]`（注意下标偏移）。于是子数组 `nums[l … r‑1]` 的和等于 `pre[r] - pre[l]`。  

有了前缀和后，问题转化为：**在前缀和数组中找一对下标 `(l, r)`，使得 `pre[r] - pre[l] ≥ k 且 r - l 最小**。  

这看起来像「最短的满足差值条件的两点」，可以用 **单调队列（Monotonic Queue）** 高效求解。思路如下：

1. **单调递增的队列**  
   - 队列里存放前缀和的下标 `i`，且对应的前缀和值 `pre[i]` **严格递增**。  
   - 为什么要保持递增？因为如果 `pre[i] ≥ pre[j]` 且 `i < j`，那么 `j` 对任何后面的 `r` 都不会比 `i` 更好（`pre[r] - pre[j] ≤ pre[r] - pre[i]`），而且 `j` 的下标更大，导致子数组更长。于是可以直接把 `j` 弹出。

2. **遍历前缀和**  
   - 对每个新的前缀和 `pre[r]`（`r` 从 0 到 n），先检查队首是否满足 `pre[r] - pre[queue[0]] ≥ k`。如果满足，就说明以 `queue[0]` 为左端点的子数组已经够大，长度为 `r - queue[0]`，可以更新答案；随后弹出队首，因为它已经不可能再产生更短的子数组（更大的 `r` 只会让长度更长）。  
   - 接着，维护队列的单调性：如果 `pre[r] ≤ pre[queue[-1]]`，把队尾的下标弹出，直到队尾的前缀和比 `pre[r]` 小为止。然后把 `r` 加入队尾。  

整个过程只遍历一次前缀和数组，队列的每个元素最多进出一次，**时间是线性的**。

> **类比**：想象一条河流，两岸的水位分别是 `pre[l]`（左岸）和 `pre[r]`（右岸），我们要找最短的「桥」使得两岸水位差至少 `k`。我们把左岸的水位按升序排好，只保留「最有潜力」的点（更低的水位更容易满足差值），这样每次只看最左边的点就能快速决定是否可以建桥。

#### 代码（Python）  

```python
from collections import deque
from typing import List

def shortest_subarray(nums: List[int], k: int) -> int:
    n = len(nums)
    # 1. 计算前缀和，pre[0] = 0，pre[i] 表示前 i 个数的和
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] + nums[i]

    # 2. 单调队列，里面存放前缀和的下标
    dq = deque()
    ans = n + 1                     # 用一个不可能的最大值做初始答案

    for r in range(n + 1):
        # 2.1 先检查队首能否构成合法子数组
        while dq and pre[r] - pre[dq[0]] >= k:
            ans = min(ans, r - dq[0])   # 更新最短长度
            dq.popleft()                # 弹出，因为以后再也用不到它了

        # 2.2 维护队列的单调递增性（前缀和从小到大）
        while dq and pre[r] <= pre[dq[-1]]:
            dq.pop()                    # 更大的下标、较大的前缀和没有优势，删掉

        dq.append(r)                    # 把当前下标加入队尾

    return -1 if ans == n + 1 else ans
```

#### 复杂度  

- **时间复杂度**：`O(n)`。我们只遍历一次前缀和数组（`n+1` 次），队列中的每个下标最多进一次、出一次，所以整体操作次数与 `n` 成线性关系。相比暴力的 `O(n²)`，相当于把「一万倍」的工作量压缩到「几倍」。
- **空间复杂度**：`O(n)`。前缀和数组需要 `n+1` 个整数，队列最坏情况下也可能保存 `n+1` 个下标（但仍然是线性级别）。这在 10⁵ 的规模下是可以接受的。

---

## 心得  

- **核心技巧**：**前缀和 + 单调队列**（也叫单调递增双端队列）。  
- **适用的题型**（类似思路）  
  1. **Maximum Subarray Sum with Length Constraint**（限制长度的最大子数组和）  
  2. **Shortest Subarray with Sum at Least K**（本题）  
  3. **Longest Well-Performing Interval**（最长的「表现良好」区间）  
- **一句话总结解题钥匙**：把「子数组求和」转化为「前缀和差值」，再用单调队列只保留「最有潜力的左端点」即可线性求解。

---

## 反思  

- **第一反应**：看到「最短」+「和 ≥ k」马上想到枚举所有子数组（暴力），但很快意识到 `n` 高达 10⁵，暴力不可行。  
- **最容易踩的坑**  
  - 前缀和可能出现负数，导致不能直接用二分或滑动窗口（这些方法要求数组非负）。  
  - 维护单调队列时忘记先检查「能否直接得到答案」的 while 循环，导致答案不更新或超时。  
  - 边界条件：`pre[0] = 0` 必须加入队列，否则会漏掉以数组开头为左端点的合法子数组。  
- **下次遇到同类题**：第一步先写出前缀和，思考「是否可以把子数组条件转化为两个前缀的差值」，然后判断是否需要 **单调结构**（单调栈/队列）来快速找满足差值的最短/最长区间。