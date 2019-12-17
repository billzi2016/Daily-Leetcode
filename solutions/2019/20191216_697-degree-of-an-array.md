# #697. 数组的度 / Degree of an Array

> 难度：简单 · 标签：Array、Hash Table · [LeetCode 链接](https://leetcode.com/problems/degree-of-an-array/)

---

## 题目（英文原版）

**Description**

Given a non-empty array of non-negative integers nums, the degree of this array is defined as the maximum frequency of any one of its elements.
Your task is to find the smallest possible length of a (contiguous) subarray of nums, that has the same degree as nums.

**Examples**

**Example 1:**

```
Input: nums = [1,2,2,3,1]
Output: 2
Explanation: 
The input array has a degree of 2 because both elements 1 and 2 appear twice.
Of the subarrays that have the same degree:
[1, 2, 2, 3, 1], [1, 2, 2, 3], [2, 2, 3, 1], [1, 2, 2], [2, 2, 3], [2, 2]
The shortest length is 2. So return 2.
```

**Example 2:**

```
Input: nums = [1,2,2,3,1,4,2]
Output: 6
Explanation: 
The degree is 3 because the element 2 is repeated 3 times.
So [2,2,3,1,4,2] is the shortest subarray, therefore returning 6.
```

**Constraints**

- nums.length will be between 1 and 50,000.
- nums[i] will be an integer between 0 and 49,999.

---

## 题目（中文翻译）

给定一个非空的非负整数数组 `nums`，数组的 **度**（degree）定义为其中任意元素出现次数的最大值。  
你的任务是找出 `nums` 中满足 **度** 与原数组相同的 **连续子数组**（subarray）中，长度最小的可能值。

#### 示例 1

**输入**  
```json
nums = [1,2,2,3,1]
```

**输出**  
```
2
```

**解释**  
原数组的度为 2，因为元素 `1` 和 `2` 各出现了两次。  
具有相同度的子数组有：  
`[1, 2, 2, 3, 1]`、`[1, 2, 2, 3]`、`[2, 2, 3, 1]`、`[1, 2, 2]`、`[2, 2, 3]`、`[2, 2]`。  
最短的长度是 2，因此返回 2。

#### 示例 2

**输入**  
```json
nums = [1,2,2,3,1,4,2]
```

**输出**  
```
6
```

**解释**  
数组的度为 3，因为元素 `2` 出现了三次。  
`[2,2,3,1,4,2]` 是满足相同度的最短子数组，所以返回 6。

#### 约束

- `1 <= nums.length <= 50,000`
- `0 <= nums[i] <= 49,999`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**枚举所有可能的连续子数组**，统计子数组里每个数字出现的次数，得到子数组的“度”（出现次数的最大值），如果它和原数组的度相同，就把它的长度记下来，最后取最小的长度。

- **用到的数据结构**：  
  - **哈希表（Python 的 dict）**。可以把它想象成一本字典，**key** 是单词（这里是数组里的数字），**value** 是对应的页码（这里是出现次数）。查找、插入、更新都是 O(1) 时间，和在真实字典里查单词差不多快。

- **为什么正确**：  
  - 我们把所有可能的连续子数组都检查了一遍，凡是满足“度相同”的子数组一定会被发现，取最小长度自然就是答案。

- **复杂度分析（大白话）**：  
  - 外层遍历左端点 `i`，内层遍历右端点 `j`，两层循环一起会产生大约 `n·(n+1)/2 ≈ n²/2` 次子数组。  
  - 对每个子数组，我们要遍历一次它的元素来更新哈希表计数，这一步的时间和子数组长度成正比，最坏情况下是 O(n)。于是整体时间是 **O(n³)**（立方级），在 50 000 长度时根本不可接受。  
  - 空间上我们只需要存放当前子数组的计数表，最多也就是 O(n)（因为子数组里最多有 n 种不同的数字）。

#### 代码（Python）

```python
def findShortestSubArray_bruteforce(nums):
    n = len(nums)
    # 先算出原数组的度
    from collections import Counter
    overall_cnt = Counter(nums)
    degree = max(overall_cnt.values())

    best_len = n  # 先设为最大可能长度

    # 枚举所有子数组 [i, j]
    for i in range(n):
        sub_cnt = {}          # 当前子数组的计数哈希表
        sub_degree = 0        # 当前子数组的度
        for j in range(i, n):
            x = nums[j]
            sub_cnt[x] = sub_cnt.get(x, 0) + 1   # 哈希表里加 1
            sub_degree = max(sub_degree, sub_cnt[x])

            # 如果子数组的度已经等于整体度，就可以尝试更新答案
            if sub_degree == degree:
                best_len = min(best_len, j - i + 1)
                # 继续往右扩展也不可能更短了，直接 break 提速（可选）
                # break

    return best_len
```

#### 复杂度

- **时间复杂度**：**O(n³)**  
  - 解释：外层 i、内层 j 各 O(n)，内部遍历子数组再 O(n) → 立方级。对 n=50 000 来说几乎不可能跑完。

- **空间复杂度**：**O(n)**  
  - 解释：最坏情况下子数组里出现 n 个不同的数字，需要 O(n) 的哈希表来计数。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于我们重复统计同一个数字的出现位置。其实，只要知道每个数字 **第一次出现的位置、最后一次出现的位置以及出现次数**，就能直接算出它能贡献的最短子数组长度。

**一步步推导**：

1. **遍历一次数组**（线性时间），记录三个信息：  
   - `first[x]`：数字 `x` 第一次出现的下标。  
   - `last[x]`：数字 `x` 最后一次出现的下标。  
   - `count[x]`：数字 `x 的出现次数。  
   这三个信息可以用三个哈希表（或一个字典里存元组）来保存。  
   类比：想象我们在记录每本书的**起始页**、**结束页**以及**出现次数**，一次记录完毕后，所有信息都在手里。

2. **求整体的度**：遍历 `count`，取最大的出现次数 `degree`。

3. **求最短长度**：再次遍历 `count`，只看出现次数等于 `degree` 的数字。  
   对于这些“最频繁的”数字，子数组必须至少从它的第一次出现到最后一次出现才能包含它全部出现的次数，长度就是 `last[x] - first[x] + 1`。  
   取这些长度的最小值，就是答案。

**核心算法**：一次遍历 + 哈希表（字典） → **线性时间**。  
**为什么对了**：子数组必须是连续的，若想保留某个数字的全部出现次数，子数组的左端点不能早于它的第一次出现，右端点不能晚于它的最后一次出现。因此最短子数组的长度必然是上述公式给出的。

#### 代码（Python）

```python
def findShortestSubArray(nums):
    """
    返回拥有和原数组相同 degree 的最短连续子数组的长度。
    思路：一次遍历记录每个数字的首次位置、末次位置以及出现次数。
    """
    first = {}   # 第一次出现的下标
    last = {}    # 最后一次出现的下标
    count = {}   # 出现次数

    for i, x in enumerate(nums):
        if x not in first:               # 只记录第一次出现
            first[x] = i
        last[x] = i                      # 始终更新为最新的下标
        count[x] = count.get(x, 0) + 1   # 计数加一

    # 计算整体的 degree（最大出现次数）
    degree = max(count.values())

    # 在所有出现次数等于 degree 的数字中，找最小的子数组长度
    min_len = len(nums)   # 初始值设为整个数组长度
    for x in count:
        if count[x] == degree:
            cur_len = last[x] - first[x] + 1   # 公式：右端点 - 左端点 + 1
            min_len = min(min_len, cur_len)

    return min_len
```

#### 复杂度

- **时间复杂度**：**O(n)**  
  - 解释：只遍历了一遍数组（`n` 次），随后遍历哈希表（至多不同数字的个数 ≤ n）做常数时间的操作。相比暴力的 O(n³)，快了很多，几乎是线性的。

- **空间复杂度**：**O(k)**（`k` 为不同数字的个数，最坏 O(n)）  
  - 解释：我们保存了每个不同数字的三个整数（首次、末次、计数），占用的空间与不同数字的数量成正比。对于本题的约束，这完全可接受。

---

## 心得

- **核心技巧**：一次遍历收集**出现次数 + 首次/末次位置**，利用哈希表实现 O(1) 的查询和更新。  
- **适用的题型**：  
  1. **寻找数组子区间满足某种频率条件**（如 “最短子数组使出现次数达到给定阈值”）。  
  2. **统计字符/数字的出现区间**（如 “最长无重复子串”、 “最小覆盖子串”）。  
  3. **求数组的 “跨度”**（首次/末次位置差），比如 “找出出现次数最多的元素的最小区间”。  
- **一句话总结解题钥匙**：**把“出现次数最多的元素”对应的左、右边界记录下来，答案就是这些边界差的最小值**。

---

## 反思

- **第一反应**：看到“degree（度）”和“最短连续子数组”，立刻想到要**统计每个数字出现的次数**，于是想到暴力枚举所有子数组。  
- **最容易踩的坑**：  
  - **忽略连续性**：只统计出现次数而不考虑第一次/最后一次出现的位置，会得到错误的子数组长度。  
  - **边界条件**：数组只有一个元素时，`first`、`last`、`count` 都只有一个值，答案应为 1。  
  - **同频多元素**：可能有不止一个数字的出现次数等于整体 degree，需要在它们之间取最小长度。  
- **下次类似题的第一步**：**先用哈希表记录每个元素的出现次数以及出现的左右边界**，再根据题目要求在这些信息上做一次线性扫描。这样可以快速定位答案，避免暴力枚举的高时间消耗。