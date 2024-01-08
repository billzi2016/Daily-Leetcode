# #2542. 最大子序列得分 / Maximum Subsequence Score

> 难度：中等 · 标签：Array、Greedy、Sorting、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/maximum-subsequence-score/)

---

## 题目（英文原版）

**Description**

You are given two 0-indexed integer arrays nums1 and nums2 of equal length n and a positive integer k. You must choose a subsequence of indices from nums1 of length k.
For chosen indices i0, i1, ..., ik - 1, your score is defined as:
Return the maximum possible score.
A subsequence of indices of an array is a set that can be derived from the set {0, 1, ..., n-1} by deleting some or no elements.

**Examples**

**Example 1:**

```
Input: nums1 = [1,3,3,2], nums2 = [2,1,3,4], k = 3
Output: 12
Explanation: 
The four possible subsequence scores are:
- We choose the indices 0, 1, and 2 with score = (1+3+3) * min(2,1,3) = 7.
- We choose the indices 0, 1, and 3 with score = (1+3+2) * min(2,1,4) = 6. 
- We choose the indices 0, 2, and 3 with score = (1+3+2) * min(2,3,4) = 12. 
- We choose the indices 1, 2, and 3 with score = (3+3+2) * min(1,3,4) = 8.
Therefore, we return the max score, which is 12.
```

**Example 2:**

```
Input: nums1 = [4,2,3,1,1], nums2 = [7,5,10,9,6], k = 1
Output: 30
Explanation: 
Choosing index 2 is optimal: nums1[2] * nums2[2] = 3 * 10 = 30 is the maximum possible score.
```

**Constraints**

- n == nums1.length == nums2.length
- 1 <= n <= 105
- 0 <= nums1[i], nums2[j] <= 105
- 1 <= k <= n

---

## 题目（中文翻译）

给定两个等长的、下标从 0 开始的整数数组 `nums1` 和 `nums2`（长度为 `n`），以及一个正整数 `k`。你需要从 `nums1` 中选择恰好 `k` 个下标构成一个子序列（subsequence）。  
设选中的下标为 `i₀, i₁, …, i_{k-1}`，则该子序列的得分定义为  

\[
\left( \sum_{j=0}^{k-1} \text{nums1}[i_j] \right) \times \min\bigl(\text{nums2}[i_0], \text{nums2}[i_1], \dots, \text{nums2}[i_{k-1}]\bigr)
\]

返回可能的最大得分。

**子序列（subsequence）** 是指从集合 `{0, 1, …, n-1}` 中删除任意（也可以不删除）若干元素后得到的下标集合。

---

## 示例

### 示例 1  
**输入**  
```text
nums1 = [1,3,3,2], nums2 = [2,1,3,4], k = 3
```  
**输出**  
```text
12
```  
**解释**  
四种可能的子序列得分如下：

- 选择下标 `0, 1, 2`，得分 = \((1+3+3) \times \min(2,1,3) = 7\)  
- 选择下标 `0, 1, 3`，得分 = \((1+3+2) \times \min(2,1,4) = 6\)  
- 选择下标 `0, 2, 3`，得分 = \((1+3+2) \times \min(2,3,4) = 12\)  
- 选择下标 `1, 2, 3`，得分 = \((3+3+2) \times \min(1,3,4) = ...\)（已截断）

最大得分为 **12**。

### 示例 2  
**输入**  
```text
nums1 = [4,2,3,1,1], nums2 = [7,5,10,9,6], k = 1
```  
**输出**  
```text
30
```  
**解释**  
选择下标 `2` 最优：`nums1[2] * nums2[2] = 3 * 10 = 30`，这是可能的最大得分。

---

## 约束条件

- `n == nums1.length == nums2.length`
- `1 <= n <= 10^5`
- `0 <= nums1[i], nums2[i] <= 10^5`
- `1 <= k <= n`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是**把所有可能的长度为 `k` 的下标子序列都枚举出来**，然后按照题目给的公式计算分数，取最大的那一个。  

- **用到的数据结构**：  
  - `list`（列表）保存当前枚举的下标集合。  
  - `for` 循环配合 `itertools.combinations`（组合）可以一次性生成所有 “从 `0…n-1` 中挑 `k` 个下标”的组合。  
  - 计算分数时需要求 **和**（`sum(nums1[i] for i in comb)`）和 **最小值**（`min(nums2[i] for i in comb)`），这就像在超市里挑选若干件商品后，先把价钱加起来，再找出最便宜的那件商品的价格。

- **为什么这个方法一定能得到正确答案**：  
  因为我们穷举了**所有**合法的下标子序列，真正的最优解必定在这些组合里出现，遍历完后取最大值自然就是答案。

- **时间/空间复杂度的大白话解释**：  
  - 设数组长度为 `n`，我们要从 `n` 个位置中挑 `k` 个，组合数是 `C(n,k) = n! / (k!·(n‑k)!)`，这在最坏情况下几乎等同于 `n^k`（指数级增长），也就是说**随数组变大，运行时间会像火箭一样飞快增长**，在 `n=10^5` 时根本不可行。  
  - 额外的空间只需要保存当前枚举的 `k` 个下标和几个临时变量，**大约是 `O(k)`**，相对来说很小。

#### 代码（Python）

```python
from itertools import combinations

def max_score_bruteforce(nums1, nums2, k):
    n = len(nums1)
    best = 0                      # 用来保存目前找到的最大分数
    # enumerate all ways to pick k indices
    for comb in combinations(range(n), k):
        # 计算选中下标对应的 nums1 的和
        s = sum(nums1[i] for i in comb)
        # 计算选中下标对应的 nums2 的最小值
        mn = min(nums2[i] for i in comb)
        best = max(best, s * mn)  # 更新最大分数
    return best
```

> **注意**：这段代码只能在 `n` 很小（比如 `n ≤ 20`）时跑得下，真正提交时会超时。

#### 复杂度

- **时间复杂度**：`O(C(n, k) * k)`  
  - 解释：我们要遍历 `C(n,k)` 种组合，每种组合里要遍历 `k` 次求和/求最小值，所以整体是指数级的，随着 `n` 增大几乎是“天文数字”。
- **空间复杂度**：`O(k)`  
  - 只保存当前组合的 `k` 个下标以及若干临时变量。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈在于枚举所有组合**。  
观察公式  

```
score = (sum of chosen nums1) * (min of chosen nums2)
```

- `min(nums2)` 只和 **最小的那个 nums2 元素** 有关。  
- 如果我们已经确定了「这 `k` 个下标里最小的 `nums2` 是哪一个」，那么 **只需要在它左边（包括它本身）挑出 `k‑1` 个 nums1 最大的元素**，再加上它对应的 `nums1`，就能得到在该最小值下的最佳分数。

于是可以把问题转化为：

> 按 **`nums2` 从大到小** 排序后，遍历每个元素把它当成「当前子序列的最小值」。在遍历的过程中，维护一个**能够随时得到 `k‑1`（或 `k`）个最大 `nums1` 值**的数据结构。

**关键数据结构 – 最小堆（priority queue）**  

- 堆就像一个“随时能看到最小元素的盒子”。  
- 我们在遍历时把已经看过的 `nums1` 放进 **最小堆**，堆里只保留 **最大的 `k` 个** `nums1`。  
  - 当堆的大小超过 `k` 时，弹出最小的那个（因为它不可能进入最终的最大 `k` 集合）。  
  - 这样堆顶（最小的）恰好是当前 `k` 个最大 `nums1` 中的最小值，堆中所有元素的和就是这 `k` 个最大 `nums1` 的总和。

**步骤概览**  

1. **把两个数组“绑在一起”**：`pairs = [(nums2[i], nums1[i]) for i in range(n)]`。  
   - 这里把 `nums2` 放在前面是为了后面**按 `nums2` 降序**排序，类似把商品的“折扣力度”放在前面，先看折扣大的商品。  

2. **按照 `nums2` 降序排列**。  
   - 排好序后，遍历时第一次出现的 `nums2` 最大，随后的 `nums2` 只会变小，保证当前遍历的元素可以被当作子序列的**最小值**（因为后面再加入的 `nums2` 都不比它大）。  

3. **遍历排序后的数组**，逐个把对应的 `nums1` 放进最小堆，并维护堆的大小 ≤ `k`。  
   - 同时维护 `cur_sum`：堆中所有元素的和。  

4. **当堆的大小恰好等于 `k` 时**，说明已经挑选了 `k` 个最大的 `nums1`（包括当前的那个）。此时的分数可以计算为 `cur_sum * current_nums2`（因为当前的 `nums2` 是这 `k` 个下标里最小的）。  
   - 用 `ans = max(ans, cur_sum * current_nums2)` 保存全局最大。  

5. 遍历结束后 `ans` 即为答案。

**类比**：  
想象你在挑选 `k` 件礼物，每件礼物都有两项属性：价值 `nums1` 和“保质期” `nums2`。你的得分是“所有礼物价值之和”乘以“最短保质期”。如果把礼物按保质期从长到短排好，你每次把价值最高的 `k` 件放进购物车（堆），当你把第 `i` 件礼物（保质期最短的那件）加入购物车后，立刻可以算出此时的得分，因为这件的保质期就是当前所有礼物的最短保质期。

#### 代码（Python）

```python
import heapq
from typing import List

def maxScore(nums1: List[int], nums2: List[int], k: int) -> int:
    # 1. 把两个数组对应的元素打包成 (nums2, nums1) 的元组
    pairs = list(zip(nums2, nums1))          # [(nums2[i], nums1[i]), ...]
    # 2. 按 nums2 降序排列
    pairs.sort(reverse=True)                 # 大的 nums2 先来

    max_heap = []            # 用最小堆（heapq 默认是最小堆）保存最大的 k 个 nums1
    cur_sum = 0              # 堆中所有元素的和
    ans = 0

    for cur_nums2, cur_nums1 in pairs:
        # 3. 把当前的 nums1 放进堆
        heapq.heappush(max_heap, cur_nums1)
        cur_sum += cur_nums1                # 更新当前和

        # 4. 如果堆的大小超过 k，弹出最小的那个（因为我们只想保留最大的 k 个）
        if len(max_heap) > k:
            removed = heapq.heappop(max_heap)   # 弹出最小的 nums1
            cur_sum -= removed                  # 对应地减去它的贡献

        # 5. 当堆正好有 k 个元素时，计算可能的最大分数
        if len(max_heap) == k:
            # 此时 cur_nums2 是这 k 个下标里最小的 nums2
            ans = max(ans, cur_sum * cur_nums2)

    return ans
```

> **关键行中文注释**：  
> - `heapq.heappush(max_heap, cur_nums1)` → 把当前的 `nums1` 加进“装价值的盒子”。  
> - `heapq.heappop(max_heap)` → 把盒子里价值最小的那件商品踢出去，只保留价值最高的 `k` 件。  
> - `cur_sum * cur_nums2` → “价值总和” × “当前最短保质期”。

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 排序需要 `O(n log n)`。  
  - 遍历时每次对堆的插入/弹出都是 `O(log k)`，`k ≤ n`，所以整体仍是 `O(n log n)`。  
  - 与暴力解的指数级时间相比，这个速度在 `n = 10^5` 时也能在毫秒级完成。

- **空间复杂度**：`O(n)`（主要是存放排序后的 `pairs`）  
  - 堆最多保存 `k` 个元素，`k ≤ n`，所以额外的堆空间是 `O(k)`，在最坏情况下也是 `O(n)`。  
  - 与暴力解的 `O(k)` 相比，多了一点排序数组的空间，但仍然线性可接受。

---

## 心得

- **核心技巧**：**先按 `nums2` 降序固定最小值，再用最小堆维护最大的 `k` 个 `nums1`**。  
- **适用的题型**（类似思路）：  
  1. **Maximum Score From Performing Multiplication Operations**（先排序后堆）  
  2. **Maximum Sum of Min-Product of Two Subarrays**（固定最小值，挑最大和）  
  3. **Maximum Performance of a Team**（同样是“固定最小的 `speed`，挑最大 `efficiency`”）  
- **一句话总结解题钥匙**：*把“最小的 `nums2`”先锁定，再用堆快速取出对应的 `k` 个最大 `nums1`*。

---

## 反思

- **第一反应**：直接想到枚举所有子序列，随后意识到会超时。  
- **最容易踩的坑**：  
  - **忘记在堆大小超过 `k` 时弹出**，导致 `cur_sum` 包含了多余的元素，得分计算会错误。  
  - **排序方向写反**：如果把 `nums2` 按升序排，当前遍历的 `nums2` 不是子序列的最小值，公式不成立。  
  - **整数溢出**（在某些语言里）需要使用 64 位整数；Python 自带大整数不需要额外处理。  
- **下次遇到同类题**：第一步先**思考哪个量会成为“瓶颈”（最小值或最大值），尝试**把它固定**（通常通过排序），再用**堆/单调结构**快速维护其余需要最大化/最小化的量。这样往往能把指数级搜索降到 `O(n log n)`。