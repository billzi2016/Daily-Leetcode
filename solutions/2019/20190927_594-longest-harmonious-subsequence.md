# #594. 最长和谐子序列 / Longest Harmonious Subsequence

> 难度：简单 · 标签：Array、Hash Table、Sliding Window、Sorting、Counting · [LeetCode 链接](https://leetcode.com/problems/longest-harmonious-subsequence/)

---

## 题目（英文原版）

**Description**

We define a harmonious array as an array where the difference between its maximum value and its minimum value is exactly 1.
Given an integer array nums, return the length of its longest harmonious subsequence among all its possible subsequences.

**Examples**

**Example 1:**

```
Input: nums = [1,3,2,2,5,2,3,7]
Output: 5
Explanation:
The longest harmonious subsequence is [3,2,2,2,3] .
```

**Example 2:**

```
Input: nums = [1,2,3,4]
Output: 2
Explanation:
The longest harmonious subsequences are [1,2] , [2,3] , and [3,4] , all of which have a length of 2.
```

**Example 3:**

```
Input: nums = [1,1,1,1]
Output: 0
Explanation:
No harmonic subsequence exists.
```

**Constraints**

- 1 <= nums.length <= 2 * 104
- -109 <= nums[i] <= 109

---

## 题目（中文翻译）

我们将和谐数组（harmonious array）定义为其最大值与最小值之差恰好为 **1** 的数组（array）。  
给定一个整数数组（integer array）`nums`，返回在所有可能的子序列（subsequence）中，最长和谐子序列的长度。

## 示例

### 示例 1
**输入**  
`nums = [1,3,2,2,5,2,3,7]`  

**输出**  
`5`  

**解释**  
最长的和谐子序列是 `[3,2,2,2,3]` 。

### 示例 2
**输入**  
`nums = [1,2,3,4]`  

**输出**  
`2`  

**解释**  
最长的和谐子序列有 `[1,2]`、`[2,3]`、`[3,4]`，它们的长度均为 **2**。

### 示例 3
**输入**  
`nums = [1,1,1,1]`  

**输出**  
`0`  

**解释**  
不存在和谐子序列。

## 约束条件
- `1 <= nums.length <= 2 * 10^4`
- `-10^9 <= nums[i] <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：**把所有子序列都列举出来，检查每个子序列的最大值与最小值之差是否恰好等于 1**。  
- **子序列**指的是在保持原来相对顺序的前提下，任选若干元素组成的新数组。  
- 为了判断“和谐”，我们需要知道子序列里的**最大值**和**最小值**。这可以用两个变量在遍历子序列时实时更新。  

把“最大值就像字典里查到的词条，最小值就像它对应的页码”。只要两个数相差 1，子序列就是和谐的。我们把所有满足条件的子序列长度取最大值即可。

为什么这个方法一定能得到答案？因为它穷举了**所有可能的子序列**，不放过任何一种组合，最好的自然会被记录下来。

不过，这种“全遍历”方式非常慢：  
- 对长度为 `n` 的数组，子序列的数量是 `2^n`（每个元素选或不选），根本不可行。  
- 为了稍微降低一点难度，我们可以只枚举**起点 i 和终点 j**（i ≤ j），把区间 `[i, j]` 当成子序列（这里把“子序列”简化成“连续子数组”，仍然能说明暴力思路的时间特征）。  
- 这样需要两层循环，时间复杂度是 `O(n²)`，空间几乎为 `O(1)`。

> **大白话**：  
> - `O(n²)` 就是“把每个元素和后面的每个元素都比一次”。如果 `n=10,000`，那大约要比 100 000 000 次，普通电脑跑几秒甚至几分钟都很正常。  

#### 代码（Python）  

```python
from typing import List

def findLHS_brute(nums: List[int]) -> int:
    n = len(nums)
    ans = 0                         # 记录目前找到的最长和谐子序列长度
    # 枚举所有可能的区间 [i, j]（这里用连续子数组来演示暴力思路）
    for i in range(n):
        cur_min = cur_max = nums[i] # 区间起点时，最大最小都是它自己
        for j in range(i, n):
            # 更新区间的最大值和最小值
            cur_min = min(cur_min, nums[j])
            cur_max = max(cur_max, nums[j])
            # 判断是否满足和谐条件
            if cur_max - cur_min == 1:
                ans = max(ans, j - i + 1)   # 区间长度 = j-i+1
    return ans
```

#### 复杂度  

- **时间复杂度：** `O(n²)`  
  - 两层循环，每层最多遍历 `n` 次。  
  - 大白话：把每个元素和它后面的所有元素都比一次。  

- **空间复杂度：** `O(1)`  
  - 只用了几个额外的变量来记录当前区间的最大、最小和值。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈**在于我们不断重复统计区间里的最大、最小值。实际上，**和谐子序列只关心两种数：`x` 和 `x+1`**（或者 `x-1`），而不需要关心它们在原数组中的相对位置，因为子序列可以随意挑选元素，只要保持顺序即可。  

**关键观察**  
- 如果一个数 `x` 出现了 `cnt[x]` 次，而数 `x+1` 出现了 `cnt[x+1]` 次，那么把这两种数全部挑出来，就得到一个长度为 `cnt[x] + cnt[x+1]` 的和谐子序列。  
- 只要 `cnt[x] > 0` 并且 `cnt[x+1] > 0`，这两个数就可以组成合法的子序列。  

于是我们只需要统计每个数出现的次数（**频率表**），再遍历一次所有键，检查相邻的 `x` 与 `x+1` 是否同时出现。  

**数据结构：哈希表（Python 中的 `dict`）**  
- 哈希表可以把“数字 → 出现次数”想象成一本**查字典**：词条是数字，页码是它出现的次数。查一次是 `O(1)`，所以统计整个数组只需要一次遍历。  

**步骤**  
1. **遍历数组**，把每个元素计数放进哈希表 `cnt`。  
2. **遍历哈希表的键**，对于每个键 `x`，如果 `x+1` 也在表里，则计算 `cnt[x] + cnt[x+1]`，更新答案。  

**为什么正确**  
- 任意合法的和谐子序列里，只会出现两种数且相差恰好 1（题目定义）。  
- 把这两种数全部取出来，得到的子序列一定更长或等长（因为我们没有删掉任何一个可以使用的元素）。  
- 因此，**最长的和谐子序列一定是“某个数 x 与 x+1 的全部出现次数之和”。**  

#### 代码（Python）  

```python
from typing import List
from collections import Counter   # Counter 本质上是一个 dict，专门用来计数

def findLHS(nums: List[int]) -> int:
    # 1️⃣ 统计每个数出现了多少次
    cnt = Counter(nums)          # 例如 [1,3,2,2] -> {1:1, 3:1, 2:2}
    
    ans = 0
    # 2️⃣ 检查每个数 x 是否和 x+1 同时出现
    for x in cnt:
        if x + 1 in cnt:         # x 与 x+1 都出现了
            # 把它们的出现次数相加，得到以这两种数构成的和谐子序列长度
            ans = max(ans, cnt[x] + cnt[x + 1])
    return ans
```

#### 复杂度  

- **时间复杂度：** `O(n)`  
  - 第一次遍历数组统计频率是 `O(n)`。  
  - 第二次遍历哈希表的键，键的数量最多等于不同元素的种类数 ≤ `n`，也是 `O(n)`。  
  - 大白话：我们只“走了一遍”原数组，后面再“翻了一遍”字典，都是线性时间。  

- **空间复杂度：** `O(m)`（`m` 为不同数字的种类数）  
  - 需要存放每个不同数字的计数。最坏情况下每个数字都不相同，`m = n`，所以是 `O(n)`。  
  - 这比暴力解的 `O(1)` 多一点空间，但换来了线性时间，通常是值得的。  

---  

## 心得  

- **核心技巧**：利用**哈希表计数**把“寻找相差为 1 的两类数”转化为 O(1) 查找。  
- **适用的题型**  
  1. “出现次数最多的子序列”类，如 **Longest Subarray with Absolute Diff ≤ 1**。  
  2. “两数之差为固定值”的计数问题，例如 **Pairs with Difference K**。  
  3. “相邻数出现次数相加”的统计类题，如 **Maximum Length of Pair Chain**（思路类似）。  
- **一句话总结**：  
  > 把“和谐”限制化成“只可能出现两种相邻的数”，用哈希表一次统计全部出现次数，配对相邻键即可得到最长长度。  

---  

## 反思  

- **第一反应**：看到“子序列”，本能想枚举所有组合（暴力），但立刻感到时间会爆炸。  
- **最容易踩的坑**  
  - 忽略 **空答案**：当数组里没有相差为 1 的两种数时，答案应为 `0`（如全部相同的 `[1,1,1]`）。  
  - 负数也能参与和谐子序列，需要哈希表能够处理负键（Python 的 dict 完全没问题）。  
  - 统计时使用 `Counter` 或手写 dict 时，要注意键不存在的情况，防止 `KeyError`。  
- **下次遇到同类题**，第一步应该想到：  
  > “这道题只关心数值之间的差距，能否把所有元素的出现次数先统计出来，然后在这份统计表上做配对？”  

这样就能快速从暴力想到哈希计数的最优解。