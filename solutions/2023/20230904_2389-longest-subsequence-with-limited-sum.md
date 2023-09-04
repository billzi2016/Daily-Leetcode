# #2389. 受限总和的最长子序列 / Longest Subsequence With Limited Sum

> 难度：简单 · 标签：Array、Binary Search、Greedy、Sorting、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/longest-subsequence-with-limited-sum/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums of length n, and an integer array queries of length m.
Return an array answer of length m where answer[i] is the maximum size of a subsequence that you can take from nums such that the sum of its elements is less than or equal to queries[i].
A subsequence is an array that can be derived from another array by deleting some or no elements without changing the order of the remaining elements.

**Examples**

**Example 1:**

```
Input: nums = [4,5,2,1], queries = [3,10,21]
Output: [2,3,4]
Explanation: We answer the queries as follows:
- The subsequence [2,1] has a sum less than or equal to 3. It can be proven that 2 is the maximum size of such a subsequence, so answer[0] = 2.
- The subsequence [4,5,1] has a sum less than or equal to 10. It can be proven that 3 is the maximum size of such a subsequence, so answer[1] = 3.
- The subsequence [4,5,2,1] has a sum less than or equal to 21. It can be proven that 4 is the maximum size of such a subsequence, so answer[2] = 4.
```

**Example 2:**

```
Input: nums = [2,3,4,5], queries = [1]
Output: [0]
Explanation: The empty subsequence is the only subsequence that has a sum less than or equal to 1, so answer[0] = 0.
```

**Constraints**

- n == nums.length
- m == queries.length
- 1 <= n, m <= 1000
- 1 <= nums[i], queries[i] <= 106

---

## 题目（中文翻译）

给定一个长度为 `n` 的整数数组 `nums`，以及一个长度为 `m` 的整数数组 `queries`。  
返回一个长度为 `m` 的数组 `answer`，其中 `answer[i]` 表示从 `nums` 中挑选的**子序列（subsequence）**的最大可能大小，使得该子序列所有元素的和 **≤** `queries[i]`。  

**子序列（subsequence）** 是指可以通过删除原数组中的若干（或不删除）元素得到的数组，且剩余元素的相对顺序保持不变。

### 示例 1
**输入**  
```text
nums = [4,5,2,1], queries = [3,10,21]
```
**输出**  
```text
[2,3,4]
```
**解释**  
我们逐个回答查询：
- 子序列 `[2,1]` 的和 **≤** 3。可以证明，满足条件的子序列最大长度为 2，因此 `answer[0] = 2`。  
- 子序列 `[4,5,1]` 的和 **≤** 10。可以证明，满足条件的子序列最大长度为 3，因此 `answer[1] = 3`。  
- 子序列 `[4,5,2,1]` 的和 **≤** 21，长度为 4，所以 `answer[2] = 4`。

### 示例 2
**输入**  
```text
nums = [2,3,4,5], queries = [1]
```
**输出**  
```text
[0]
```
**解释**  
和 **≤** 1 的唯一子序列是空子序列，其长度为 0，故 `answer[0] = 0`。

### 约束条件
- `n == nums.length`
- `m == queries.length`
- `1 ≤ n, m ≤ 1000`
- `1 ≤ nums[i], queries[i] ≤ 10^6`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：**把所有可能的子序列都枚举出来**，然后检查每个子序列的元素和是否 ≤ `queries[i]`，符合条件的就记录它的长度，最后取最大的长度。  

- **子序列**可以看成“从原数组里挑选若干个位置，保持原来的顺序”。  
- **枚举所有子序列**相当于对每个位置决定“要不要选”。这和二进制的“0/1”选择一模一样：  
  - 位置 0 选 → 1， 不选 → 0  
  - 位置 1 选 → 1， 不选 → 0  
  - …  
  - 最后把所有 0/1 组合拼成二进制数，就得到一种子序列。  

因为我们要把 **每一种组合**（即每个二进制数）都尝试一遍，才能保证不漏掉最优解。  

**为什么这个方法一定对？**  
只要遍历了所有 2ⁿ 种可能，就一定能找到满足条件且长度最大的那个子序列。  

**时间/空间复杂度**  
- 对每个查询，我们要遍历 2ⁿ 种子序列，计算它们的和和长度 → **时间复杂度 O(2ⁿ)**（指数级，`n` 增大一点就会爆炸）。  
- 只需要几个变量保存当前的和、长度和最大长度 → **空间复杂度 O(1)**（常数级）。  

> **大白话**：  
> O(2ⁿ) 就像把所有可能的钥匙都试一遍才能打开锁，钥匙的数量会随着 `n` 的增加而指数增长，根本不可能在合理时间内完成。

#### 代码（Python）

```python
from itertools import combinations
from typing import List

def answer_bruteforce(nums: List[int], queries: List[int]) -> List[int]:
    n = len(nums)
    ans = []
    # 对每个查询单独处理
    for q in queries:
        best = 0                         # 记录当前查询的最大子序列长度
        # 枚举子序列长度 1~n
        for length in range(1, n + 1):
            # 取出所有长度为 length 的组合（保持顺序的子序列其实等价于组合，因为我们不关心位置）
            for idxs in combinations(range(n), length):
                s = sum(nums[i] for i in idxs)   # 计算这条子序列的和
                if s <= q:                       # 和不超过查询上限
                    best = max(best, length)    # 更新最大长度
        ans.append(best)               # 当前查询的答案
    return ans
```

> **代码要点**  
> - `combinations` 会把下标的所有取法枚举出来，相当于遍历所有子序列。  
> - 每次检查和是否 ≤ 查询值，符合就更新 `best`。  

#### 复杂度  

- **时间复杂度**：O(m·2ⁿ)  
  - `m` 是查询的个数，`2ⁿ` 是子序列的总数。  
  - 对于 `n=20` 已经是 `2⁰⁰ ≈ 1,048,576`，再乘上查询数会非常慢。  
- **空间复杂度**：O(1)（不计入输入数组本身）  

---

### 2. 最优解  

#### 思路  
从暴力解可以看到，**真正决定子序列能有多长的关键是“挑哪些元素”。**  
如果我们想让子序列尽可能长，显然应该挑 **尽可能小的元素**，因为小的元素更容易“装进”给定的和限制。  

**步骤拆解**  

1. **把 `nums` 排序**  
   - 排序后，前面的元素一定是最小的。  
   - 类比：在超市买东西想花最少的钱买最多的东西，就先挑最便宜的商品。

2. **前缀和**  
   - 计算排序后数组的前缀和 `pre[i]`：前 `i` 个最小元素的总和。  
   - 这样我们可以在 **O(1)** 时间内知道 “前 `k` 个最小元素的和”。  
   - 前缀和就像一本账本，记下每一步累计花了多少钱，后面查账只需要翻到对应页码。

3. **对每个查询使用二分查找**  
   - 我们要找最大的 `k`，满足 `pre[k] ≤ queries[i]`。  
   - 前缀和数组是单调递增的（因为每个新加的元素都是非负的），于是可以用 **二分查找** 在 `O(log n)` 时间内定位 `k`。  
   - 二分查找的思路：把可能的 `k` 范围不断二分，检查中间位置的前缀和是否 ≤ 查询值，决定向左还是向右继续搜索。

**为什么快？**  
- 只排序一次 `O(n log n)`，后面所有查询都只需要二分查找 `O(log n)`，不再枚举组合。  
- 这相当于把“挑最小元素”这一步提前做好准备，查询时直接查表。

#### 代码（Python）

```python
from bisect import bisect_right
from typing import List

def answer_optimal(nums: List[int], queries: List[int]) -> List[int]:
    # 1️⃣ 把 nums 从小到大排好序
    nums.sort()                         # O(n log n)

    # 2️⃣ 计算前缀和：pre[i] = 前 i 个最小元素的和，pre[0] = 0 方便二分
    pre = [0]                           # pre 长度为 n+1
    for x in nums:                     # O(n)
        pre.append(pre[-1] + x)

    # 3️⃣ 对每个查询使用二分查找
    ans = []
    for q in queries:
        # bisect_right 在 pre 中找到第一个 > q 的位置，下标 - 1 就是满足 ≤ q 的最大下标
        # 这里的下标恰好等于能取的元素个数
        k = bisect_right(pre, q) - 1   # O(log n)
        ans.append(k)
    return ans
```

> **代码要点**  
> - `nums.sort()`：把数组变成“从便宜到贵的商品列表”。  
> - `pre` 的第 `i` 项保存前 `i` 件商品的总价，`pre[0]=0` 代表“什么也不买”。  
> - `bisect_right(pre, q)` 相当于在账本里找第一个超过预算的那一页，前一页就是还能买的最大商品数。  

#### 复杂度  

- **时间复杂度**：  
  - 排序 `O(n log n)`  
  - 前缀和 `O(n)`  
  - 每个查询二分 `O(log n)`，共 `m` 次 → `O(m log n)`  
  - **总体** `O(n log n + m log n)`  
  - 与暴力的指数级 `O(m·2ⁿ)` 相比，几乎是 **秒杀**。  

- **空间复杂度**：`O(n)`  
  - 需要额外存储排好序的 `nums`（原地排序）和前缀和数组 `pre`，大小和原数组成正比。  
  - 相比暴力只用了常数空间，这里多用了线性空间，但仍然很小（`n ≤ 1000`）。

---

## 心得  

- **核心技巧**：**先把数组排序，再利用前缀和 + 二分查找**，把“挑最小元素”这一步预处理成查询能直接用的表。  
- **适用场景**：  
  1. “在预算内买最多物品” 类似的题目（如 LeetCode 1838. Frequency of the Most Frequent Element）。  
  2. “给定上限，求最长前缀满足条件” 的问题（如 LeetCode 1642. Furthest Building You Can Reach）。  
- **一句话总结**：**要让子序列最长，就从最小的数开始累加，用二分快速定位能取多少个。**

---

## 反思  

- **第一反应**：看到“子序列”和“最大长度”，立刻想到枚举所有子序列。  
- **最容易踩的坑**：  
  - 忘记子序列可以不保留原顺序的“相对位置”，其实在本题里只关心元素大小，排序不会破坏答案。  
  - 直接对每个查询都重新排序或重新计算前缀和，会导致不必要的重复工作。  
  - 二分查找的边界要处理好：使用 `bisect_right` 并减 1，才能得到 **≤** 查询值的最大下标。  
- **下次遇到同类题**：  
  1. 先思考 “要最大化个数，应该选什么样的元素？” → 通常是 **最小的**。  
  2. 看能否把“最小的若干个”预处理成前缀和或累计数组。  
  3. 对每个查询使用 **二分/滑动窗口** 快速定位答案。