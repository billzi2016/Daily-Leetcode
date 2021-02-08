# #1200. 最小绝对差 / Minimum Absolute Difference

> 难度：简单 · 标签：Array、Sorting · [LeetCode 链接](https://leetcode.com/problems/minimum-absolute-difference/)

---

## 题目（英文原版）

**Description**

Given an array of distinct integers arr, find all pairs of elements with the minimum absolute difference of any two elements.
Return a list of pairs in ascending order(with respect to pairs), each pair [a, b] follows

**Examples**

**Example 1:**

```
Input: arr = [4,2,1,3]
Output: [[1,2],[2,3],[3,4]]
Explanation: The minimum absolute difference is 1. List all pairs with difference equal to 1 in ascending order.
```

**Example 2:**

```
Input: arr = [1,3,6,10,15]
Output: [[1,3]]
```

**Example 3:**

```
Input: arr = [3,8,-10,23,19,-4,-14,27]
Output: [[-14,-10],[19,23],[23,27]]
```

**Constraints**

- 2 <= arr.length <= 105
- -106 <= arr[i] <= 106

---

## 题目（中文翻译）

**题目描述**  
给定一个由互不相同的整数构成的数组（array）`arr`，找出所有元素对（pair），使得这两个元素之间的绝对差（absolute difference）是所有可能差值中的最小值。返回一个按升序排列的对列表（以对本身的升序为准），每个对以 `[a, b]` 的形式出现，其中 `a <= b`。

**示例 1**  
**输入**: `arr = [4,2,1,3]`  
**输出**: `[[1,2],[2,3],[3,4]]`  
**解释**: 最小绝对差为 `1`。将所有差值等于 `1` 的对按升序列出。

**示例 2**  
**输入**: `arr = [1,3,6,10,15]`  
**输出**: `[[1,3]]`  

**示例 3**  
**输入**: `arr = [3,8,-10,23,19,-4,-14,27]`  
**输出**: `[[-14,-10],[19,23],[23,27]]`  

**约束条件**  
- `2 <= arr.length <= 10^5`  
- `-10^6 <= arr[i] <= 10^6`   (数组中的每个整数 `arr[i]` 的取值范围)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把数组里每两个数都拿出来算一次绝对差（`abs(a-b)`），记下最小的那个差值，然后再把所有差值等于最小差的数对收集起来。  

- **用到的数据结构**：  
  - **列表（list）**：存放原始数组和最终答案。  
  - **双层循环**：遍历“所有可能的两两组合”。可以把它想象成在一张纸上画一个矩阵，行是第一个数，列是第二个数，遍历矩阵的每个格子就相当于检查每一对数。  
- **为什么正确**：因为我们把 **每一对** 都算了一遍，最小的差一定会被找到，随后把所有等于这个最小差的对全部输出，自然不会漏掉。  

- **时间/空间复杂度**（大白话解释）：  
  - **时间复杂度**是 `O(n²)`，这里的 `n` 是数组长度。可以把它想成“每个人和每个人都要握手”，如果有 100 个人，握手次数是 100×99/2≈5,000 次；如果人数翻倍到 200，握手次数会变成大约 20,000 次，增长速度是 **平方级** 的。  
  - **空间复杂度**是 `O(1)`（不算输出的空间），因为我们只用了常数个额外变量来保存最小差和临时的两个数。

#### 代码（Python）

```python
from typing import List

def minimumAbsDifference_bruteforce(arr: List[int]) -> List[List[int]]:
    n = len(arr)
    min_diff = float('inf')          # 当前找到的最小差，初始设为无限大
    pairs = []                       # 用来保存最终答案

    # 双层循环遍历所有两两组合
    for i in range(n):
        for j in range(i + 1, n):    # 只看 i < j，避免重复和自己和自己比较
            diff = abs(arr[i] - arr[j])   # 计算绝对差
            if diff < min_diff:           # 发现更小的差，就清空之前的答案
                min_diff = diff
                pairs = [[min(arr[i], arr[j]), max(arr[i], arr[j])]]
            elif diff == min_diff:        # 差等于当前最小差，直接加入答案
                pairs.append([min(arr[i], arr[j]), max(arr[i], arr[j])])

    # 为了满足“按对升序”要求，需要把每个小对排好序后，再整体排序
    pairs.sort()
    return pairs
```

#### 复杂度

- **时间复杂度**：`O(n²)` — 每个元素都要和后面的所有元素比较一次，数量随 `n` 的平方增长。  
- **空间复杂度**：`O(1)`（不计输出）— 只用了几个临时变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于“双层循环”。我们需要一种办法，**不必把每一对都算一遍**，就能直接找到最小的差。  

观察：  
- 若把数组 **从小到大排好序**，相邻的两个数之间的差一定是**所有可能差值中最小的候选**。  
- 为什么？因为如果有两个数 `a < b < c`，则 `c - a = (c - b) + (b - a)`，显然 `c - a` 大于等于 `b - a` 或 `c - b` 中的一个。换句话说，最小差一定出现在相邻的两个数之间。  

因此，**步骤**如下：

1. **排序**：把数组升序排列（`O(n log n)`）。  
2. **一次遍历**：只看相邻的两个数，计算它们的差，记录下最小差 `min_diff`。  
3. **再次遍历**（或者在第一次遍历时直接收集）：把所有差等于 `min_diff` 的相邻数对加入答案。  
4. 因为我们已经是按照升序遍历的，答案天然是“按对升序”，不需要额外排序。

核心算法/数据结构：

- **排序**（Sorting）：在 Python 中 `list.sort()` 使用的是 **Timsort**，时间复杂度 `O(n log n)`，空间复杂度 `O(1)`（原地排序）。可以把排序想象成把一堆乱放的书按照高度从低到高摆成一排。  
- **一次遍历**（Single Pass）：遍历一次数组，时间 `O(n)`，相当于“从左到右顺着排好序的书一本一本检查”。  

整体时间复杂度为 `O(n log n)`，主要花在排序上；空间复杂度为 `O(1)`（不计答案）。

#### 代码（Python）

```python
from typing import List

def minimumAbsDifference(arr: List[int]) -> List[List[int]]:
    # 1. 排序，O(n log n)
    arr.sort()                     # 原地排序，省掉额外空间

    # 2. 找到最小相邻差，O(n)
    min_diff = float('inf')
    for i in range(1, len(arr)):
        diff = arr[i] - arr[i - 1]     # 已经是升序，直接相减即可（不需要 abs）
        if diff < min_diff:
            min_diff = diff

    # 3. 收集所有等于 min_diff 的相邻对，O(n)
    result: List[List[int]] = []
    for i in range(1, len(arr)):
        if arr[i] - arr[i - 1] == min_diff:
            result.append([arr[i - 1], arr[i]])   # 已经是升序的对

    # 4. result 本身已经按对升序，无需再排序
    return result
```

#### 复杂度

- **时间复杂度**：`O(n log n)` — 排序是最耗时的步骤，后面的两次线性遍历各是 `O(n)`，整体 dominated by sorting。相比暴力的 `O(n²)`，当 `n` 很大时（如 10⁵）快了很多。  
- **空间复杂度**：`O(1)`（不计答案）— 只用了常数个额外变量；排序在原地进行，不额外占用大块内存。

---

## 心得

- **核心技巧**：先排序，再只比较相邻元素的差值。  
- **适用的题型**：  
  1. “寻找最小/最大差值” 类问题（如 **Maximum Gap**）。  
  2. “区间相邻关系” 类问题（如 **两数之和** 的变体，需要有序数组的双指针）。  
- **一句话总结解题钥匙**：**把乱序变有序，最小差一定藏在相邻位置**。

---

## 反思

- **拿到题目第一反应**：直接想遍历所有两两组合求差（暴力），因为最直观。  
- **最容易踩的坑**：  
  - 忘记先排序，导致比较非相邻元素产生错误的最小差。  
  - 结果顺序不符合要求，忘记对答案再排序（其实只要排序后遍历相邻即可自然有序）。  
  - 边界条件：数组最小长度为 2 时，只会有唯一一对答案，需要确保代码不出现索引越界。  
- **下次遇到同类题，第一步该想到**：**“先把数据排好序”，因为有序结构能把很多“所有组合”问题压缩成“相邻比较”。