# #2099. 长度为 K 的子序列最大和 / Find Subsequence of Length K With the Largest Sum

> 难度：简单 · 标签：Array、Hash Table、Sorting、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/find-subsequence-of-length-k-with-the-largest-sum/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and an integer k. You want to find a subsequence of nums of length k that has the largest sum.
Return any such subsequence as an integer array of length k.
A subsequence is an array that can be derived from another array by deleting some or no elements without changing the order of the remaining elements.

**Examples**

**Example 1:**

```
Input: nums = [2,1,3,3], k = 2
Output: [3,3]
Explanation:
The subsequence has the largest sum of 3 + 3 = 6.
```

**Example 2:**

```
Input: nums = [-1,-2,3,4], k = 3
Output: [-1,3,4]
Explanation: 
The subsequence has the largest sum of -1 + 3 + 4 = 6.
```

**Example 3:**

```
Input: nums = [3,4,3,3], k = 2
Output: [3,4]
Explanation:
The subsequence has the largest sum of 3 + 4 = 7. 
Another possible subsequence is [4, 3].
```

**Constraints**

- 1 <= nums.length <= 1000
- -105 <= nums[i] <= 105
- 1 <= k <= nums.length

---

## 题目（中文翻译）

给定一个整数数组 `nums` 和一个整数 `k`，要求找出 `nums` 中长度为 `k` 的子序列（subsequence），使其元素和最大。返回任意一个满足条件的子序列，以长度为 `k` 的整数数组形式返回。

**子序列（subsequence）** 是指可以通过从原数组中删除若干（也可以不删除）元素而得到的数组，且保留剩余元素的相对顺序不变。

## 示例

### 示例 1
**输入**: `nums = [2,1,3,3]`, `k = 2`  
**输出**: `[3,3]`  
**解释**:  
该子序列的和最大，为 `3 + 3 = 6`。

### 示例 2
**输入**: `nums = [-1,-2,3,4]`, `k = 3`  
**输出**: `[-1,3,4]`  
**解释**:  
该子序列的和为 `-1 + 3 + 4 = 6`，已达到最大。

### 示例 3
**输入**: `nums = [3,4,3,3]`, `k = 2`  
**输出**: `[3,4]`  
**解释**:  
该子序列的和为 `3 + 4 = 7`，是可能的最大和。另一种可行的子序列是 `[4,3]`（顺序不同但和相同）。

## 约束条件
- `1 <= nums.length <= 1000`
- `-10^5 <= nums[i] <= 10^5`
- `1 <= k <= nums.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把 **所有** 长度为 `k` 的子序列都列举出来，算出每个子序列的和，挑出最大的那个。  
- **子序列**：从原数组里挑出若干元素，保持原来的相对顺序，不需要是连续的。  
- **枚举**：可以把「挑出 `k` 个位置」看成「从 `n` 个位置里挑 `k` 个」的组合问题。  
- **数据结构类比**：枚举组合就像在一本电话本里挑出 `k` 个人的名字，遍历所有可能的选法。  

为什么这个方法一定能得到答案？因为我们把**所有合法的子序列**都检查了一遍，最大和的子序列必然在其中。  

**复杂度分析（大白话）**  
- 组合的数量是 “从 `n` 里挑 `k`”，记作 `C(n, k)`，比如 `n=10, k=5` 时有 252 种。  
- 对每一种组合，我们要把选中的 `k` 个数相加，花 `k` 步。  
- 所以总的时间大约是 `C(n, k) * k`，随 `n`、`k` 指数级增长，`n=1000` 时根本跑不完。  
- 只用了常数级的额外空间（存放当前组合和最大和），所以空间是 `O(k)`。

#### 代码（Python）

```python
from itertools import combinations
from typing import List

def max_subsequence_brute(nums: List[int], k: int) -> List[int]:
    # best_sum 保存当前找到的最大和，best_seq 保存对应的子序列
    best_sum = float('-inf')
    best_seq = []

    # enumerate 所有长度为 k 的位置组合（比如 (0,2,3) 表示取下标 0,2,3 的元素）
    for idx_tuple in combinations(range(len(nums)), k):
        # 根据下标取出子序列
        cur_seq = [nums[i] for i in idx_tuple]          # O(k)
        cur_sum = sum(cur_seq)                         # O(k)

        # 若当前和更大，就更新答案
        if cur_sum > best_sum:
            best_sum = cur_sum
            best_seq = cur_seq

    return best_seq
```

#### 复杂度

- **时间复杂度**：`O(C(n, k) * k)`  
  - 这里的 `C(n, k)` 是组合数，随 `n`、`k` 指数级增长。  
  - 用大白话说，就是「先把所有可能的挑选方法列出来，再把每种方法里的 `k` 个数相加」。
- **空间复杂度**：`O(k)`  
  - 只需要存放当前遍历的子序列和最大和的子序列，最多 `k` 个数。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到 **瓶颈** 在于「枚举所有组合」——这一步根本不需要做。  
实际上，要让子序列的和最大，只要把 **值最大的 `k` 个元素** 挑出来就行。  
但是挑出来后，还要保证它们在原数组中的相对顺序不变，才能构成合法的子序列。

**一步步推导**：

1. **挑最大的 `k` 个数**  
   - 把每个数和它的原始下标一起记下来，形成 `(value, index)` 的“带标签”数组。  
   - 按 `value` 降序排序，取前 `k` 个。  
   - 这一步相当于「在字典里查找最贵的 `k` 本书」，字典（这里是排序好的列表）让我们快速定位最大值。

2. **恢复原始顺序**  
   - 取出的 `k` 个元素已经记住了原来的下标。  
   - 把它们再按 **下标** 升序排一次，这样就得到一个合法的子序列，且仍然是最大和的。  

**核心算法 / 数据结构**  

- **排序（Sorting）**：把带下标的数组按照数值从大到小排，时间 `O(n log n)`。  
- **哈希表（Hash Table）** 类比：我们可以把「是否被选中」记在一个集合里，查询是 O(1)。这里直接用列表保存选中的 `(value, index)`，不需要额外的哈希表。  

**类比**：想象你在超市里挑选最贵的 `k` 件商品，先把所有商品按价格排序，挑前 `k` 件。挑完后，你发现这些商品在货架上的位置不一定连在一起，于是按照它们在货架上的顺序重新排一遍，最后得到的就是「不打乱原来顺序」的购物清单。

#### 代码（Python）

```python
from typing import List

def max_subsequence(nums: List[int], k: int) -> List[int]:
    # 1. 为每个元素记录下标，形成 (value, index) 的列表
    indexed = [(val, idx) for idx, val in enumerate(nums)]

    # 2. 按值降序排序，取前 k 大的元素
    #    sorted 返回的是新的列表，不会修改原数组
    top_k = sorted(indexed, key=lambda x: x[0], reverse=True)[:k]

    # 3. 根据下标升序重新排列，这样子序列保持原来的顺序
    top_k.sort(key=lambda x: x[1])   # 按 index 升序

    # 4. 只取出数值部分返回
    return [val for val, _ in top_k]
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - `sorted` 两次分别是 `O(n log n)`（第一次按值，第二次按下标），常数因子很小。  
  - 与暴力解的指数级时间相比，这就像把「穷举」换成了「一次快速排序」。
- **空间复杂度**：`O(n)`  
  - 需要额外的列表保存带下标的 `(value, index)` 对，大小和原数组相同。  
  - 这相当于在原数组旁边放了一个同等大小的“备份”，而不是指数级的组合空间。

---

## 心得

- **核心技巧**：**先挑最大的 k 个元素，再按原顺序恢复**。这是一种典型的「贪心 + 排序」思路。
- **适用的题型**  
  1. *Pick K Largest Elements*（如 LeetCode 347 前 K 个高频元素的变形）  
  2. *Maximum Sum of K Elements With Order Constraint*（如在数组中挑出 k 个数使和最大且保持顺序）  
  3. *Top K Frequent Words*（先统计频率再排序取前 K）  
- **一句话总结解题钥匙**：**“先用价值挑选，再用位置排队”。**

---

## 反思

- **第一反应**：直接想到「遍历所有组合」——最直观但不可行的暴力法。  
- **最容易踩的坑**  
  - 忘记 **保持原顺序**：只取最大的 `k` 个数会得到一个集合，但不一定是合法的子序列。  
  - 负数的处理：即使数组里有负数，仍然要取值最大的 `k` 个（负数也可能被挑选）。  
  - `k` 等于 `len(nums)` 时，直接返回原数组即可，不需要额外排序。  
- **下次类似题的第一步**：**把 “要最大化/最小化” 的目标转化为“挑选前 K 大/小的元素”，然后检查是否还有顺序或其他约束需要二次处理**。