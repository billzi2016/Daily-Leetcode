# #347. 前 K 个高频元素 / Top K Frequent Elements

> 难度：中等 · 标签：Array、Hash Table、Divide and Conquer、Sorting、Heap (Priority Queue)、Bucket Sort、Counting、Quickselect · [LeetCode 链接](https://leetcode.com/problems/top-k-frequent-elements/)

---

## 题目（英文原版）

**Description**

Given an integer array nums and an integer k, return the k most frequent elements. You may return the answer in any order.
Follow up: Your algorithm's time complexity must be better than O(n log n), where n is the array's size.

**Examples**

**Example 1:**

```
Input: nums = [1,1,1,2,2,3], k = 2
Output: [1,2]
```

**Example 2:**

```
Input: nums = [1], k = 1
Output: [1]
```

**Constraints**

- 1 <= nums.length <= 105
- -104 <= nums[i] <= 104
- k is in the range [1, the number of unique elements in the array].
- It is guaranteed that the answer is unique.

---

## 题目（中文翻译）

给定一个整数数组 `nums` 和一个整数 `k`，返回出现频率最高的 `k` 个元素。你可以以任意顺序返回答案。

**示例 1**  
**示例 2**  

**约束条件**  
- 1 ≤ `nums.length` ≤ 10⁵  
- -10⁴ ≤ `nums[i]` ≤ 10⁴  
- `k` 的取值范围为 `[1, 数组中不同元素的个数]`  
- 题目保证答案唯一  

**进阶**：你的算法时间复杂度必须优于 O(n log n)，其中 n 为数组的大小。

**示例**

示例 1:  
```
Input: nums = [1,1,1,2,2,3], k = 2
Output: [1,2]
```

示例 2:  
```
Input: nums = [1], k = 1
Output: [1]
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

1. **统计每个数字出现的次数**  
   - 用 **哈希表**（在 Python 里就是 `dict`）来记录。把数字当作 **key**（词），出现的次数当作 **value**（页码）。这一步类似查字典：看到一个单词，就把它的出现次数记下来。  
2. **把所有 (数字, 次数) 放进列表**，然后**按照次数从大到小排序**。  
   - 排序相当于把所有单词按出现频率排好序，最常出现的排在前面。  
3. **取排好序的前 k 个数字**，就是答案。

> **为什么正确**  
> 统计得到每个数字的真实出现次数后，排序保证了次数大的排在前面，取前 k 个自然就是出现次数最高的 k 个。

#### 代码（Python）

```python
from collections import Counter  # Counter 是专门用来计数的“字典”

def topKFrequent(nums, k):
    # 1. 统计频率，key 是数字，value 是出现次数
    freq = Counter(nums)               # 例如 nums = [1,1,2] => {1:2, 2:1}
    
    # 2. 把 (数字, 次数) 变成列表并按次数降序排序
    #   sorted 会返回一个新列表，key=lambda x: x[1] 表示按元组的第二个元素（次数）比较
    sorted_items = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    #   sorted_items 形如 [(1, 3), (2, 2), (3, 1)]

    # 3. 取前 k 个数字（只要数字，不要次数）
    result = [num for num, _ in sorted_items[:k]]
    return result
```

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 统计频率是 `O(n)`（遍历一次数组）。  
  - 排序需要 `O(m log m)`，其中 `m` 是不同数字的个数，最坏 `m = n`，于是整体是 `O(n log n)`。  
  - 大白话：如果数组有 10 万个数，排序相当于把这 10 万个数字排好队，需要大约 `10万 × log2(10万) ≈ 10万 × 17` 次比较。

- **空间复杂度**：`O(m)`  
  - 需要一个哈希表存每个数字的计数，最坏情况每个数字都不相同，所以空间是 `O(n)`。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **排序**，因为排序本身是 `O(n log n)`。我们要把时间压到 **线性**（`O(n)`）或者 **接近线性**（`O(n log k)`）：

1. **仍然先统计频率**（这一步已经是线性的，不能再快了）。  
2. **利用「桶排序」**（Bucket Sort）把出现次数映射到「桶」里：  
   - 出现次数的范围是 `1 … n`（因为最多出现 n 次）。  
   - 创建一个长度为 `n+1` 的列表 `bucket`，下标 `i` 表示「出现了 i 次」的所有数字。  
   - 把每个数字放进对应的桶里，这一步同样是 `O(n)`。  
3. **从高频到低频遍历桶**，把数字收集到结果中，直到收集到 k 个为止。  
   - 因为我们是从「大桶」往「小桶」走，最先碰到的数字必然是最高频的，直接得到答案。  

> **为什么正确**  
> 统计得到每个数字的真实出现次数后，所有可能的出现次数只有 `0 ~ n`（线性范围），把相同次数的数字聚在同一个「桶」里，遍历桶时自然按照次数从大到小顺序检查，前 k 个数字就是出现次数最高的 k 个。

#### 代码（Python）

```python
from collections import Counter
from typing import List

def topKFrequent(nums: List[int], k: int) -> List[int]:
    # 1️⃣ 统计每个数字的出现次数
    freq = Counter(nums)                # {num: count}
    
    n = len(nums)
    # 2️⃣ 创建桶：下标 i 表示「出现了 i 次」的所有数字
    bucket = [[] for _ in range(n + 1)] # 长度 n+1 的空列表组成的列表
    
    # 把数字放进对应的桶里
    for num, cnt in freq.items():
        bucket[cnt].append(num)          # 例如 cnt=3 的数字会放进 bucket[3]
    
    # 3️⃣ 从高频到低频收集答案
    res = []
    # 从最大的可能出现次数 n 开始往下遍历
    for cnt in range(n, 0, -1):
        if bucket[cnt]:                  # 该桶不为空
            for num in bucket[cnt]:
                res.append(num)          # 取出数字加入结果
                if len(res) == k:        # 已经收集到 k 个，直接返回
                    return res
    return res  # 理论上永远不会走到这里，因为题目保证 k 合法
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 统计频率 `O(n)`。  
  - 把数字放进桶 `O(m)`，`m` ≤ `n`。  
  - 最终遍历桶最多也只会遍历 `n` 次（因为桶的下标最多到 `n`），所以整体是线性的。  
  - 大白话：如果有 10 万个数，整个过程只需要「走一遍」这 10 万个数，速度非常快。

- **空间复杂度**：`O(n)`  
  - 哈希表需要存每个不同数字的计数，最坏 `O(n)`。  
  - 桶的总大小是 `n+1`，每个数字只会出现在唯一的一个桶里，所以额外空间也是线性的。  

> 与暴力解对比：我们把原本需要 `log n` 次「比较」的排序，换成了「直接放进对应的箱子」的线性操作，从而把时间从 `O(n log n)` 降到了 `O(n)`。

---

## 心得

- **核心技巧**：**桶排序 + 哈希计数**。先把「出现次数」这个概念离散化为「箱子」，再按箱子顺序取值。
- **适用的题型**  
  1. “前 K 大/小” 且元素值范围可映射为有限的「频率」或「权重”。  
  2. “出现次数排序” 例如 **"Sort Characters By Frequency"**、**"Frequency of the Most Frequent Element"**。  
  3. “计数类”问题，如 **"Maximum Population Year"**（使用差分数组 + 前缀和）。
- **一句话总结**：把「出现次数」变成「下标」，用桶直接把相同次数的数字装进去，最高频的数字自然在最高的桶里。

---

## 反思

- **第一反应**：先用 `Counter` 计数，再 `sorted`，因为排序是最直观的「把东西排好顺序」的办法。  
- **最容易踩的坑**  
  - **桶的大小**：一定要是 `n+1`，因为出现次数最大可能是 `n`（全部相同），下标 `0` 不会用到但要占位。  
  - **返回顺序**：题目说答案可以是任意顺序，只要是前 k 高频即可，不必额外再排序。  
  - **k 等于唯一元素数量**：此时所有元素都要返回，遍历桶要确保能把所有桶都检查完。  
- **下次遇到同类题**：先问自己「出现次数的范围是否和数组长度同阶」，如果是，就考虑 **桶排序**；如果范围太大，则考虑 **堆**（`O(n log k)`）或 **Quickselect**（平均 `O(n)`）来取前 k。