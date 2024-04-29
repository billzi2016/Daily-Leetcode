# #2670. 找出不同元素差数组 / Find the Distinct Difference Array

> 难度：简单 · 标签：Array、Hash Table · [LeetCode 链接](https://leetcode.com/problems/find-the-distinct-difference-array/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array nums of length n.
The distinct difference array of nums is an array diff of length n such that diff[i] is equal to the number of distinct elements in the suffix nums[i + 1, ..., n - 1] subtracted from the number of distinct elements in the prefix nums[0, ..., i].
Return the distinct difference array of nums.
Note that nums[i, ..., j] denotes the subarray of nums starting at index i and ending at index j inclusive. Particularly, if i > j then nums[i, ..., j] denotes an empty subarray.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,4,5]
Output: [-3,-1,1,3,5]
Explanation: For index i = 0, there is 1 element in the prefix and 4 distinct elements in the suffix. Thus, diff[0] = 1 - 4 = -3.
For index i = 1, there are 2 distinct elements in the prefix and 3 distinct elements in the suffix. Thus, diff[1] = 2 - 3 = -1.
For index i = 2, there are 3 distinct elements in the prefix and 2 distinct elements in the suffix. Thus, diff[2] = 3 - 2 = 1.
For index i = 3, there are 4 distinct elements in the prefix and 1 distinct element in the suffix. Thus, diff[3] = 4 - 1 = 3.
For index i = 4, there are 5 distinct elements in the prefix and no elements in the suffix. Thus, diff[4] = 5 - 0 = 5.
```

**Example 2:**

```
Input: nums = [3,2,3,4,2]
Output: [-2,-1,0,2,3]
Explanation: For index i = 0, there is 1 element in the prefix and 3 distinct elements in the suffix. Thus, diff[0] = 1 - 3 = -2.
For index i = 1, there are 2 distinct elements in the prefix and 3 distinct elements in the suffix. Thus, diff[1] = 2 - 3 = -1.
For index i = 2, there are 2 distinct elements in the prefix and 2 distinct elements in the suffix. Thus, diff[2] = 2 - 2 = 0.
For index i = 3, there are 3 distinct elements in the prefix and 1 distinct element in the suffix. Thus, diff[3] = 3 - 1 = 2.
For index i = 4, there are 3 distinct elements in the prefix and no elements in the suffix. Thus, diff[4] = 3 - 0 = 3.
```

**Constraints**

- 1 <= n == nums.length <= 50
- 1 <= nums[i] <= 50

---

## 题目（中文翻译）

给定一个下标从 **0** 开始、长度为 **n** 的数组 `nums`。  
`nums` 的 **distinct difference array（不同元素差数组）** 为长度为 **n** 的数组 `diff`，其中  

```
diff[i] = （前缀 nums[0, ..., i] 中不同元素的数量） - （后缀 nums[i + 1, ..., n - 1] 中不同元素的数量）
```

其中 `nums[i, ..., j]` 表示从下标 **i** 到 **j**（含） 的 **subarray（子数组）**。如果 **i > j**，则该子数组为空。  

请返回 `nums` 的不同元素差数组 `diff`。

---

### 示例

**示例 1**

```
输入: nums = [1,2,3,4,5]
输出: [-3,-1,1,3,5]
解释:
- i = 0 时，前缀 [1] 中有 1 个不同元素，后缀 [2,3,4,5] 中有 4 个不同元素，diff[0] = 1 - 4 = -3。
- i = 1 时，前缀 [1,2] 中有 2 个不同元素，后缀 [3,4,5] 中有 3 个不同元素，diff[1] = 2 - 3 = -1。
- i = 2 时，前缀 [1,2,3] 中有 3 个不同元素，后缀 [4,5] 中有 2 个不同元素，diff[2] = 3 - 2 = 1。
- i = 3 时，前缀 [1,2,3,4] 中有 4 个不同元素，后缀 [5] 中有 1 个不同元素，diff[3] = 4 - 1 = 3。
- i = 4 时，前缀 [1,2,3,4,5] 中有 5 个不同元素，后缀为空，0 个不同元素，diff[4] = 5 - 0 = 5。
```

**示例 2**

```
输入: nums = [3,2,3,4,2]
输出: [-2,-1,0,2,3]
解释:
- i = 0 时，前缀 [3] 中有 1 个不同元素，后缀 [2,3,4,2] 中有 3 个不同元素，diff[0] = 1 - 3 = -2。
- i = 1 时，前缀 [3,2] 中有 2 个不同元素，后缀 [3,4,2] 中有 3 个不同元素，diff[1] = 2 - 3 = -1。
- i = 2 时，前缀 [3,2,3] 中有 2 个不同元素（{2,3}），后缀 [4,2] 中有 2 个不同元素，diff[2] = 2 - 2 = 0。
- i = 3 时，前缀 [3,2,3,4] 中有 3 个不同元素（{2,3,4}），后缀 [2] 中有 1 个不同元素，diff[3] = 3 - 1 = 2。
- i = 4 时，前缀 [3,2,3,4,2] 中有 3 个不同元素，后缀为空，0 个不同元素，diff[4] = 3 - 0 = 3。
```

---

### 约束

- `1 <= n == nums.length <= 50`
- `1 <= nums[i] <= 50`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每一个下标 i 当成分界点**，分别统计  

* 前缀 `nums[0 … i]` 中有多少个不同的数字  
* 后缀 `nums[i+1 … n-1]` 中有多少个不同的数字  

然后用前缀的不同数目减去后缀的不同数目，得到 `diff[i]`。

> **数据结构**：这里需要一个能够快速判断“某个元素是否已经出现过”的容器。  
> Python 中的 `set` 正好满足需求。可以把它想象成一本“查字典”，每次把一个数字当作单词，字典里已经有的单词就说明它出现过了。

**为什么正确**：  
- 前缀和后缀分别遍历一次，把出现过的数字加入各自的 `set`，集合的大小 `len(set)` 正好等于不同元素的个数。  
- 按题意对每个 `i` 计算一次，得到的数组必然满足题目定义。

**时间/空间分析（大白话）**：  
- 对每个 `i`（一共有 `n` 个），我们都要遍历一次前缀和一次后缀，最坏情况下每次遍历的长度都是 `O(n)`，于是总共是 `O(n × n) = O(n²)`。  
- `set` 里最多装 `n` 个元素（因为数组长度是 `n`），所以额外空间是 `O(n)`。

#### 代码（Python）

```python
from typing import List

def distinct_difference_array_bruteforce(nums: List[int]) -> List[int]:
    n = len(nums)
    diff = [0] * n                     # 用来存放答案
    for i in range(n):                 # 把每个位置当作分界点
        # ---------- 统计前缀的不同元素 ----------
        prefix_set = set()
        for j in range(i + 1):         # 前缀是 0 … i
            prefix_set.add(nums[j])    # 把元素放进集合，相同的会自动去重
        prefix_cnt = len(prefix_set)   # 前缀不同元素的个数

        # ---------- 统计后缀的不同元素 ----------
        suffix_set = set()
        for j in range(i + 1, n):      # 后缀是 i+1 … n-1
            suffix_set.add(nums[j])
        suffix_cnt = len(suffix_set)   # 后缀不同元素的个数

        diff[i] = prefix_cnt - suffix_cnt   # 题目要求的差值
    return diff
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  > 想象有 `n` 个人排队，每个人都要检查前面和后面所有人的名字是否重复，检查次数随人数的平方增长。
- **空间复杂度**：`O(n)`  
  > 最多同时保存两个集合，每个集合最多装 `n` 个不同的数字。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**重复统计** 是性能瓶颈：  
- 当我们把分界点从左往右移动时，前缀只会**多加**一个元素，后缀只会**少去**一个元素。  
- 于是可以在一次遍历中，**累计** 前缀的不同数目；再一次逆向遍历，**累计** 后缀的不同数目。这样每个元素只会被“放进集合”一次，时间降到线性 `O(n)`。

具体步骤：

1. **左向右遍历**，用 `set` 记录已经见过的数字，得到 `pre[i] = 前缀 nums[0 … i] 的不同元素个数`。  
2. **右向左遍历**，同理得到 `suf[i] = 后缀 nums[i … n-1] 的不同元素个数`。注意我们真正需要的是 `i+1` 开始的后缀，所以在计算答案时使用 `suf[i+1]`（若 `i` 已是最后一个位置，则后缀为空，记为 0）。  
3. 最后遍历一次，`diff[i] = pre[i] - suf[i+1]`（`suf[n]` 设为 0）。

> **核心技巧**：前缀/后缀累计是一种“动态规划”思想的简化版，利用**一次遍历**把局部信息保存下来，后面再直接查询。  
> **类比**：想象在读一本书时，你从前往后记下每页出现的新单词数（前缀），再从后往前记下每页出现的新单词数（后缀），最后两者相减就能快速得到任意页的差值，而不必每次重新数一遍。

#### 代码（Python）

```python
from typing import List

def distinct_difference_array(nums: List[int]) -> List[int]:
    n = len(nums)

    # ---------- 前缀不同元素个数 ----------
    pre = [0] * n                # pre[i] = 前缀 0..i 的不同元素个数
    seen_pre = set()
    for i in range(n):
        seen_pre.add(nums[i])    # 加入集合，自动去重
        pre[i] = len(seen_pre)   # 当前集合大小即为不同元素个数

    # ---------- 后缀不同元素个数 ----------
    # 为了方便使用 suf[i+1]，我们额外准备一个长度为 n+1 的数组，最后一个位置对应空后缀
    suf = [0] * (n + 1)          # suf[i] = 后缀 i..n-1 的不同元素个数
    seen_suf = set()
    for i in range(n - 1, -1, -1):
        seen_suf.add(nums[i])
        suf[i] = len(seen_suf)   # 记录从 i 开始的后缀不同数目

    # ---------- 计算答案 ----------
    diff = [0] * n
    for i in range(n):
        diff[i] = pre[i] - suf[i + 1]   # 注意后缀是从 i+1 开始的
    return diff
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  > 每个元素只进 `set` 两次（一次正向一次逆向），所以整体是线性增长。相比暴力的 `O(n²)`，速度提升了好几个数量级。
- **空间复杂度**：`O(n)`  
  > 需要存 `pre`、`suf` 各 `n` 长的数组以及两个 `set`，总共也是线性空间。

---

## 心得

- **核心技巧**：前缀/后缀累计（一次遍历统计不同元素个数），配合哈希集合去重。  
- **适用题型**：  
  1. “前缀与后缀差值”类题目，如 “Maximum Difference Between Prefix and Suffix”。  
  2. 需要快速查询 **区间内不同元素个数** 的问题，例如 “Count Unique Elements in Subarrays”。  
  3. 任意需要**一次遍历得到每个位置左/右侧信息**的题目，如 “左侧最近更大元素”。
- **一句话总结**：**把重复统计改成一次累计，用集合记住已经出现的数字**，即可线性时间搞定。

## 反思

- **第一反应**：直接写两层循环去数前缀和后缀的不同元素——这就是暴力解。  
- **最容易踩的坑**：  
  - 处理最后一个位置的后缀时要记得它是空的，返回 0；否则会出现索引越界。  
  - `set` 只能去重，不能直接得到“出现次数”，但本题只需要是否出现，使用 `set` 完全足够。  
- **下次类似题的第一步**：先问自己“**前缀/后缀信息是否可以累计**”。如果答案是“Yes”，就立刻考虑一次遍历保存累计结果，而不是每次都重新遍历。