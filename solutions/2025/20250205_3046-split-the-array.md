# #3046. 数组拆分 / Split the Array

> 难度：简单 · 标签：Array、Hash Table、Counting · [LeetCode 链接](https://leetcode.com/problems/split-the-array/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums of even length. You have to split the array into two parts nums1 and nums2 such that:
Return true if it is possible to split the array, and false otherwise.

**Examples**

**Example 1:**

```
Input: nums = [1,1,2,2,3,4]
Output: true
Explanation: One of the possible ways to split nums is nums1 = [1,2,3] and nums2 = [1,2,4].
```

**Example 2:**

```
Input: nums = [1,1,1,1]
Output: false
Explanation: The only possible way to split nums is nums1 = [1,1] and nums2 = [1,1]. Both nums1 and nums2 do not contain distinct elements. Therefore, we return false.
```

**Constraints**

- 1 <= nums.length <= 100
- nums.length % 2 == 0
- 1 <= nums[i] <= 100

---

## 题目（中文翻译）

给定一个长度为偶数的整数数组 `nums`。请将该数组划分为两个长度相等的子数组 `nums1` 和 `nums2`，并满足：

- `nums1` 中的所有元素互不相同（不存在重复元素），即 **distinct**（distinct）；
- `nums2` 中的所有元素也互不相同。

如果可以完成上述划分，则返回 `true`；否则返回 `false`。

## 示例

### 示例 1
**输入**  
`nums = [1,1,2,2,3,4]`

**输出**  
`true`

**解释**  
一种可行的划分方式是 `nums1 = [1,2,3]`，`nums2 = [1,2,4]`。两个子数组均不含重复元素。

### 示例 2
**输入**  
`nums = [1,1,1,1]`

**输出**  
`false`

**解释**  
唯一可能的划分是 `nums1 = [1,1]`，`nums2 = [1,1]`，但两个子数组都包含重复元素，故返回 `false`。

## 约束条件

- `1 <= nums.length <= 100`
- `nums.length` 为偶数，即 `nums.length % 2 == 0`
- `1 <= nums[i] <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**枚举所有可能的划分**。  
把数组 `nums` 按照下标分成两段 `nums1`、`nums2`，要求：

1. `len(nums1) = len(nums2) = n/2`（`n` 为 `nums` 长度，已知是偶数）。  
2. 每段内部的元素都互不相同（即没有重复的数）。  

枚举的做法可以用「组合」来实现：从 `n` 个位置里挑出 `n/2` 个放进 `nums1`，剩下的自然就是 `nums2`。随后检查两段是否都满足「元素不重复」的条件。

> **类比**：想象你有一盒彩色球，要把它们平均分到两只盒子里，且每只盒子里不能出现同色的两个球。暴力做法就是把所有可能的分配方式都列出来，逐一检验。

**为什么正确**：只要遍历了**所有**合法的分配方式，就一定会找到一种满足要求的划分（如果存在的话），因此必然不会漏掉答案。

**复杂度分析**：  
- 组合数为 `C(n, n/2)`，在最坏情况下会非常大（比如 `n=20` 时已经有 184,756 种），所以时间复杂度是指数级的，记作 **O(2ⁿ)**（这里用 `2ⁿ` 形象地说明随着 `n` 增大，运算量会呈指数增长）。  
- 需要保存当前的组合以及两个子数组，最多占用 **O(n)** 的额外空间。

> **大白话**：`O(2ⁿ)` 就像把所有可能的“分配方案”一次一次地试，人数越多，方案数就像翻倍一样迅速爆炸，根本跑不完。

#### 代码（Python）

```python
from itertools import combinations
from typing import List

def splitArray_bruteforce(nums: List[int]) -> bool:
    n = len(nums)
    half = n // 2

    # 所有下标的组合，挑出 half 个放进 nums1
    for idxs in combinations(range(n), half):
        nums1 = [nums[i] for i in idxs]                 # 选中的下标对应的元素
        nums2 = [nums[i] for i in range(n) if i not in idxs]

        # 检查两个子数组内部是否都有唯一元素
        if len(set(nums1)) == half and len(set(nums2)) == half:
            return True        # 找到一种合法划分
    return False               # 所有组合都不行
```

#### 复杂度

- **时间复杂度**：`O( C(n, n/2) * n ) ≈ O(2ⁿ)`  
  解释：组合数本身已经是指数级，遍历每个组合时还要把元素取出来检查唯一性，整体仍然是指数级的。

- **空间复杂度**：`O(n)`  
  解释：存放当前的 `nums1`、`nums2` 以及组合下标，需要的额外空间与输入规模线性相关。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于枚举所有可能的划分**。其实我们并不需要真的去划分，只要检查**每个数字出现的次数**即可。

观察题目要求：

1. 同一个数字如果出现在同一段里会导致重复。  
2. 为了避免重复，同一个数字最多只能出现两次（一次放进 `nums1`，一次放进 `nums2`）。  
3. 若某个数字出现 **三次或更多**，无论怎么划分，必然有一段里会出现两个相同的数，题目就没有解。

因此，只要遍历一遍数组，统计每个数出现的频率（哈希表），检查是否有频率 > 2 即可。

> **类比**：把数组看成一本字典，数字是“单词”，出现的次数是“页码”。我们只需要看每个单词的页码是否超过两页，如果有，就说明这本字典根本无法被平均分成两本且每本都不出现重复单词。

**为什么正确**：  
- 若所有数字出现次数 ≤ 2，则可以把每个出现两次的数字分别放进两段，出现一次的数字随意分配，使两段长度相等（因为总长度是偶数）。这样必然能得到合法划分。  
- 若存在出现次数 > 2 的数字，则必然在某段出现重复，违背题目条件。

**核心数据结构**：**哈希表（字典）**，用于 O(1) 时间统计频率。  

**复杂度分析**：  
- 只需要一次遍历，时间 **O(n)**（线性时间）。  
- 额外的哈希表最多保存 100 个不同的数字（受约束 `1 ≤ nums[i] ≤ 100`），空间 **O(1)**（常数级），因为它不随 `n` 增长而增长太多。

#### 代码（Python）

```python
from typing import List
from collections import Counter

def splitArray(nums: List[int]) -> bool:
    """
    判断是否可以把数组均分为两个子数组，使每个子数组内部元素互不相同。
    思路：若任意数字出现超过两次，则不可能。否则一定可以。
    """
    freq = Counter(nums)                # 统计每个数字出现的次数，类似“查字典”
    for val, cnt in freq.items():
        if cnt > 2:                     # 出现超过两次，必然导致同段重复
            return False
    return True                         # 所有数字出现次数 ≤ 2，必能划分
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历一次数组，`n` 是数组长度。  
  > 大白话：把数组里每个数字都看一遍，花的时间跟数组有多长成正比。

- **空间复杂度**：`O(1)`（实际上是 `O(k)`，`k ≤ 100` 为不同数字的种类数）  
  > 大白话：我们只用了一个小盒子（字典）来记每个数字出现几次，盒子里最多装 100 张卡片，和数组有多长没关系。

---

## 心得

- **核心技巧**：**频率统计**（哈希表）+ **次数上限判断**。  
- **适用题型**：
  1. “数组能否分成两组，使每组元素唯一” 类似题（如 LeetCode 2465 *Number of Distinct Subarrays*）。  
  2. “判断是否可以重新排列，使相邻元素不相同” （如 767 *Reorganize String*）。  
- **解题钥匙**：**先找瓶颈**——如果问题可以用“出现次数”直接判定，则不必进行复杂的组合或动态规划。

## 反思

- **第一反应**：看到“分成两段且每段内部不重复”，自然想到**枚举所有划分**，因为这最直观。  
- **最容易踩的坑**：
  - 忽略了 **数组长度为偶数** 的前提，导致在分配出现一次的数字时可能出现长度不平衡。  
  - 没有考虑 **数字出现次数上限**，从而多写了不必要的代码。  
- **下次遇到同类题**，第一步应该**检查元素的出现次数**，判断是否存在直接导致不可能的情况，再决定是否需要进一步的构造或搜索。