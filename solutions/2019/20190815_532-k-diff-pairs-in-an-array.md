# #532. K 差数对 / K-diff Pairs in an Array

> 难度：中等 · 标签：Array、Hash Table、Two Pointers、Binary Search、Sorting · [LeetCode 链接](https://leetcode.com/problems/k-diff-pairs-in-an-array/)

---

## 题目（英文原版）

**Description**

Given an array of integers nums and an integer k, return the number of unique k-diff pairs in the array.
A k-diff pair is an integer pair (nums[i], nums[j]), where the following are true:
Notice that |val| denotes the absolute value of val.

**Examples**

**Example 1:**

```
Input: nums = [3,1,4,1,5], k = 2
Output: 2
Explanation: There are two 2-diff pairs in the array, (1, 3) and (3, 5).
Although we have two 1s in the input, we should only return the number of unique pairs.
```

**Example 2:**

```
Input: nums = [1,2,3,4,5], k = 1
Output: 4
Explanation: There are four 1-diff pairs in the array, (1, 2), (2, 3), (3, 4) and (4, 5).
```

**Example 3:**

```
Input: nums = [1,3,1,5,4], k = 0
Output: 1
Explanation: There is one 0-diff pair in the array, (1, 1).
```

**Constraints**

- 1 <= nums.length <= 104
- -107 <= nums[i] <= 107
- 0 <= k <= 107

---

## 题目（中文翻译）

给定一个整数数组（array）`nums` 和一个整数 `k`，返回数组中 **不同的** k‑diff 对（k-diff pair）的数量。  

k‑diff 对是满足以下条件的整数对 `(nums[i], nums[j])`：

- `i != j` 且 `|nums[i] - nums[j]| == k`（其中 `|val|` 表示 `val` 的绝对值（absolute value））。

---

### 示例

**示例 1**  
```text
Input: nums = [3,1,4,1,5], k = 2
Output: 2
Explanation: 数组中有两个 2‑diff 对，分别是 (1, 3) 和 (3, 5)。虽然输入中出现了两个 1，但只统计不同的对，所以结果为 2。
```

**示例 2**  
```text
Input: nums = [1,2,3,4,5], k = 1
Output: 4
Explanation: 数组中有四个 1‑diff 对，分别是 (1, 2)、(2, 3)、(3, 4) 和 (4, 5)。
```

**示例 3**  
```text
Input: nums = [1,3,1,5,4], k = 0
Output: 1
Explanation: 数组中只有一个 0‑diff 对，即 (1, 1)。
```

---

### 约束条件

- `1 <= nums.length <= 10^4`
- `-10^7 <= nums[i] <= 10^7`
- `0 <= k <= 10^7`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的两两组合都枚举一遍**，看它们的差的绝对值是否等于 `k`，如果相等就把这对数字记下来。  
- **遍历方式**：双层循环，外层选第一个元素 `nums[i]`，内层选后面的元素 `nums[j]`（`j > i`），这样可以避免把同一对 `(a,b)` 与 `(b,a)` 重复算两次。  
- **去重**：题目要求 **唯一** 的 `k‑diff` 对。我们可以把每一对已经排好序的数字 `(min, max)` 放进一个 `set`（集合）里，集合天然会去掉重复的键，就像查字典时只会出现每个单词一次一样。  

> **类比**：把数组想成一堆彩色球，暴力解就是把每两个球拎出来比一次颜色差，记下符合条件的组合，然后交给老师（`set`）检查有没有重复的组合。

**为什么正确**：遍历所有 `i < j` 的组合，必然会覆盖题目中所有可能的 `(nums[i], nums[j])`。只要我们把满足 `|nums[i] - nums[j]| == k` 的组合加入集合，最后集合的大小就是答案。

#### 代码（Python）

```python
from typing import List

def findPairs_bruteforce(nums: List[int], k: int) -> int:
    # 用集合保存唯一的 (小的, 大的) 对
    unique_pairs = set()

    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):                # 只看 i < j，防止重复
            if abs(nums[i] - nums[j]) == k:      # 判断差的绝对值是否等于 k
                # 把较小的放前面，保证 (a,b) 与 (b,a) 被视为同一对
                pair = (min(nums[i], nums[j]), max(nums[i], nums[j]))
                unique_pairs.add(pair)           # 集合会自动去重

    return len(unique_pairs)                     # 集合大小就是唯一对的数量
```

#### 复杂度

- **时间复杂度：`O(n²)`**  
  双层循环会检查每一对元素，`n` 是数组长度。`O(n²)` 可以想象成“把 `n` 个人两两握手”，如果 `n=1000`，大约会有 1,000,000 次比较，显然在大数据下会慢。

- **空间复杂度：`O(m)`（`m` 为答案的数量）**  
  只需要一个集合存放唯一的配对。最坏情况下 `m` 可能接近 `n²/2`（所有配对都合法），但实际受 `k` 限制，一般会远小于 `n²`。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每一对都要比较一次**。我们可以利用**哈希表（字典）**一次遍历就把所有信息统计好，从而把时间降到线性 `O(n)`。

关键点：

1. **先统计每个数字出现的次数**，这一步相当于“查字典”，键是数字，值是出现次数。  
   - 类比：把所有球的颜色记在一本小册子里，想知道某种颜色有多少球，只要翻一页就知道。

2. **根据 `k` 的取值分两种情况**  
   - **`k > 0`**：我们只需要检查 “当前数字 `x` 是否有 `x + k` 也在数组里”。如果两者都出现过，就能组成唯一的 `(x, x+k)` 配对。因为我们只看一次 `x`，所以不会产生重复。  
   - **`k == 0`**：此时要求两数相等，即配对必须是相同的数字。只有出现次数 **≥ 2** 的数字才算一对。  

这样只遍历一次哈希表，时间 `O(n)`，空间 `O(n)`（存放频率表）。

#### 代码（Python）

```python
from typing import List
from collections import Counter  # Counter 是专门用来统计出现次数的字典

def findPairs(nums: List[int], k: int) -> int:
    if k < 0:                     # 差的绝对值不可能是负数，直接返回 0
        return 0

    freq = Counter(nums)         # 第一步：统计每个数字出现的次数
    count = 0

    if k == 0:
        # 只要出现次数 >= 2 的数字，就能形成一个 (x, x) 配对
        for x, cnt in freq.items():
            if cnt > 1:
                count += 1
    else:
        # k > 0 的情况：只要 x+k 也在字典里，就能形成唯一配对 (x, x+k)
        for x in freq:
            if x + k in freq:
                count += 1

    return count
```

#### 复杂度

- **时间复杂度：`O(n)`**  
  只遍历一次数组构造频率表（`O(n)`），再遍历一次哈希表检查配对（`O(m)`，`m` ≤ `n`），合起来仍是线性时间。相当于“只需要把所有球一次性放进小册子”，不必再两两比较。

- **空间复杂度：`O(n)`**  
  需要一个哈希表保存每个不同数字的出现次数。最坏情况下所有数字都不相同，需要存 `n` 条记录。

---

## 心得

- **核心技巧**：利用哈希表把“是否存在某个数”这个查询从 `O(n)` 降到 `O(1)`，从而把整体复杂度从平方级别降到线性。  
- **适用的题型**  
  1. **两数之和**（判断是否存在一对数之和为目标值）  
  2. **数组中出现超过一次的元素**（统计出现次数）  
  3. **寻找满足特定差值的配对**（本题的变形）  
- **一句话总结解题钥匙**：**把“遍历+查找”分离，用哈希表一次完成所有查找**。

---

## 反思

- **第一反应**：直接想到双层循环枚举所有配对，因为这是最直观的“穷举”思路。  
- **最容易踩的坑**  
  - **`k` 为负数**：题目保证 `k ≥ 0`，但在实现时仍要防止负数导致错误的 `x - k` 判断。  
  - **去重**：如果只统计配对次数而不注意 `k > 0` 与 `k == 0` 的区别，容易把同一个数字的多次出现算成多对。  
  - **整数范围**：`nums[i]` 可能很大（±10⁷），但使用哈希表不会受范围限制。  
- **下次类似题的第一步**：**先思考是否可以用哈希表把“是否存在某个值”变成 O(1) 查询**，如果可以，就尝试基于频率或集合来直接计数，而不是枚举所有组合。