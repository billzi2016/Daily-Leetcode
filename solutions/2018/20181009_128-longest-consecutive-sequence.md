# #128. **最长连续序列** / Longest Consecutive Sequence

> 难度：中等 · 标签：Array、Hash Table、Union Find · [LeetCode 链接](https://leetcode.com/problems/longest-consecutive-sequence/)

---

## 题目（英文原版）

**Description**

Given an unsorted array of integers nums, return the length of the longest consecutive elements sequence.
You must write an algorithm that runs in O(n) time.

**Examples**

**Example 1:**

```
Input: nums = [100,4,200,1,3,2]
Output: 4
Explanation: The longest consecutive elements sequence is [1, 2, 3, 4]. Therefore its length is 4.
```

**Example 2:**

```
Input: nums = [0,3,7,2,5,8,4,6,0,1]
Output: 9
```

**Example 3:**

```
Input: nums = [1,0,1,2]
Output: 3
```

**Constraints**

- 0 <= nums.length <= 105
- -109 <= nums[i] <= 109

---

## 题目（中文翻译）

给定一个无序整数数组（array）`nums`，返回其中最长连续元素序列（consecutive elements sequence）的长度。  
要求设计的算法时间复杂度为 **O(n)**。

**示例 1**

```text
Input: nums = [100,4,200,1,3,2]
Output: 4
Explanation: 最长的连续元素序列是 [1, 2, 3, 4]，因此其长度为 4。
```

**示例 2**

```text
Input: nums = [0,3,7,2,5,8,4,6,0,1]
Output: 9
```

**示例 3**

```text
Input: nums = [1,0,1,2]
Output: 3
```

**约束条件**

- `0 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**对数组里的每一个元素，都去找它能组成的最长连续序列**。  
具体做法：

1. 任选数组中的一个数 `x` 作为序列的起点。  
2. 从 `x+1`、`x+2` ……一直往后检查，看看这些数字是否也在数组里出现。  
3. 一旦找不到下一个数字，就算出这条序列的长度。  
4. 对所有元素都重复以上过程，取最大的长度即为答案。

> **类比**：想象你在一本无序的电话号码本里找“连续的号码”。你先挑一个号码，然后往后一个一个找，看到不连续的就停下来。对每个号码都这么做，最后最长的那段就是答案。

**为什么正确**：  
如果我们对每个数都尝试向后延伸，必然会遍历到所有可能的连续序列。最长的那条自然会被记录下来。

**时间/空间复杂度**  
- 对每个元素都可能向后遍历 `O(n)` 次，最坏情况是数组里所有数都是连续的，此时总共会进行 `n + (n‑1) + … + 1 = O(n²)` 次比较。  
- 只用了常数级的额外空间 `O(1)`（仅仅是几个计数器）。

> **大白话解释**：`O(n²)` 就像你在课堂上让每位同学和全班的每个人握手，人数多了，手握的次数会呈“平方”增长，花的时间会非常久。

#### 代码（Python）

```python
def longestConsecutive(nums):
    n = len(nums)
    if n == 0:
        return 0

    longest = 1                     # 记录目前找到的最长长度
    for i in range(n):
        cur = nums[i]                # 以 nums[i] 为序列起点
        length = 1

        # 暴力检查后续的连续数字是否在数组里
        while cur + length in nums:  # “在数组里”用线性搜索，最差 O(n)
            length += 1

        longest = max(longest, length)

    return longest
```

> **关键行中文注释**  
> - `while cur + length in nums:` 这一步每次都要遍历整个列表去判断某个数是否存在，正是导致 `O(n²)` 的原因。

#### 复杂度

- **时间复杂度**：`O(n²)` —— 对每个元素都可能遍历整个数组。  
- **空间复杂度**：`O(1)` —— 只用了几个整型变量，没有额外的数据结构。

---

### 2. 最优解

#### 思路  
从暴力解可以看到，**“在数组里找某个数是否存在”** 是瓶颈所在。  
如果我们能把“是否存在”的查询从 **线性搜索**（`O(n)`）提升到 **常数时间**（`O(1)`），整个算法就会快很多。

**哈希表（Python 中的 `set`）** 正好提供了 `O(1)` 的查找能力。我们把所有数字放进一个集合 `S`，随后对每个数字 `x`：

1. **只在 `x` 是序列起点时才开始向后扩展**。  
   - `x` 是起点的充要条件是：`x-1` 不在集合中。这样我们就不会对同一条序列重复计数。  
   - 类比：如果你在街上寻找连续的门牌号，只在看到“前面没有门牌号”的地方才开始往后数，这样每条街只会被数一次。

2. 从 `x` 开始，检查 `x+1, x+2, …` 是否在集合中，一直往后走，直到找不到为止。记录走了多少步，就是这条序列的长度。

3. 对所有数字执行上述步骤，取最大长度。

**为什么是 `O(n)`**：  
- 把所有数字放进集合是一次遍历，`O(n)`。  
- 每个数字最多只会被访问两次：一次检查它是否是序列起点（`x-1 in S`），一次在它所在的序列里被向后遍历。所有遍历的次数加起来仍然是 `O(n)`。

#### 代码（Python）

```python
def longestConsecutive(nums):
    """
    使用哈希集合（set）实现 O(n) 的解法
    """
    num_set = set(nums)          # 把所有数字放进集合，查找 O(1)
    longest = 0

    for x in num_set:
        # 只有当 x-1 不在集合中时，x 才是一个序列的起点
        if x - 1 not in num_set:
            cur = x
            length = 1

            # 向后检查连续数字是否存在
            while cur + 1 in num_set:
                cur += 1
                length += 1

            longest = max(longest, length)

    return longest
```

> **关键行中文注释**  
> - `num_set = set(nums)`：把列表变成“字典”，查找像查字典一样快。  
> - `if x - 1 not in num_set:`：只有前一个数不存在，才说明 `x` 是序列的第一个。  
> - `while cur + 1 in num_set:`：不断往后找，直到找不到为止。

#### 复杂度

- **时间复杂度**：`O(n)` —— 每个元素常数次操作。  
  - 与暴力解对比：从“每个数都要遍历整个数组”降到了“每个数只会被遍历一次”，大幅提升效率。  
- **空间复杂度**：`O(n)` —— 需要额外的哈希集合来存储所有数字。

---

## 心得

- **核心技巧**：利用哈希集合把“是否出现”的查询降到 `O(1)`，并且只在序列起点才展开搜索，避免重复计数。  
- **适用的题型**：  
  1. “找数组中满足某种条件的子集合”，如 **Two Sum**（使用哈希表找 complement）。  
  2. “判断是否存在某种结构”，如 **Valid Sudoku**（行、列、宫格的唯一性检查）。  
  3. “需要快速去重或判断存在性”，如 **Longest Substring Without Repeating Characters**（滑动窗口+哈希表）。  
- **一句话总结解题钥匙**：**把“在数组里找某个数是否存在”变成常数时间的查找，并只在必要的起点展开遍历**。

---

## 反思

- **第一反应**：直接对数组排序后遍历，得到 `O(n log n)`，但题目要求 `O(n)`，于是思考如何在不排序的情况下快速判断连续性。  
- **最容易踩的坑**：  
  - 忘记只在序列起点才开始计数，导致每条序列会被重复遍历，时间复杂度退化到 `O(n²)`。  
  - 忽视空数组或只有一个元素的边界情况，需要返回 `0` 或 `1`。  
- **下次类似题的第一步**：先问自己“我需要频繁判断‘某个值是否已经出现/是否在集合中’吗？”如果答案是“Yes”，就立刻考虑使用哈希集合（`set`/`dict`）来把查询时间压到 `O(1)`。