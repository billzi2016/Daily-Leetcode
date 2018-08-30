# #88. 合并两个有序数组 / Merge Sorted Array

> 难度：简单 · 标签：Array、Two Pointers、Sorting · [LeetCode 链接](https://leetcode.com/problems/merge-sorted-array/)

---

## 题目（英文原版）

**Description**

You are given two integer arrays nums1 and nums2, sorted in non-decreasing order, and two integers m and n, representing the number of elements in nums1 and nums2 respectively.
Merge nums1 and nums2 into a single array sorted in non-decreasing order.
The final sorted array should not be returned by the function, but instead be stored inside the array nums1. To accommodate this, nums1 has a length of m + n, where the first m elements denote the elements that should be merged, and the last n elements are set to 0 and should be ignored. nums2 has a length of n.
Follow up: Can you come up with an algorithm that runs in O(m + n) time?

**Examples**

**Example 1:**

```
Input: nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3
Output: [1,2,2,3,5,6]
Explanation: The arrays we are merging are [1,2,3] and [2,5,6].
The result of the merge is [1,2,2,3,5,6] with the underlined elements coming from nums1.
```

**Example 2:**

```
Input: nums1 = [1], m = 1, nums2 = [], n = 0
Output: [1]
Explanation: The arrays we are merging are [1] and [].
The result of the merge is [1].
```

**Example 3:**

```
Input: nums1 = [0], m = 0, nums2 = [1], n = 1
Output: [1]
Explanation: The arrays we are merging are [] and [1].
The result of the merge is [1].
Note that because m = 0, there are no elements in nums1. The 0 is only there to ensure the merge result can fit in nums1.
```

**Constraints**

- nums1.length == m + n
- nums2.length == n
- 0 <= m, n <= 200
- 1 <= m + n <= 200
- -109 <= nums1[i], nums2[j] <= 109

---

## 题目（中文翻译）

给定两个整数数组 `nums1` 和 `nums2`，它们分别以**非递减**（non-decreasing）顺序排序，并且给定两个整数 `m` 与 `n`，分别表示 `nums1` 和 `nums2` 中实际有效元素的个数。  
请将 `nums1` 和 `nums2` 合并成一个**非递减**（non-decreasing）有序数组。

合并后的有序数组 **不需要** 通过函数返回，而是直接存放在数组 `nums1` 中。为此，`nums1` 的长度为 `m + n`，其中前 `m` 个位置存放需要合并的元素，后 `n` 个位置预先填为 `0`，在合并过程中应当被覆盖。`nums2` 的长度为 `n`。

**示例 1**、**示例 2**、**示例 3** 均在下方给出。

---

### 示例

**示例 1**  
**输入**: `nums1 = [1,2,3,0,0,0]`, `m = 3`, `nums2 = [2,5,6]`, `n = 3`  
**输出**: `[1,2,2,3,5,6]`  
**解释**: 我们要合并的数组是 `[1,2,3]` 和 `[2,5,6]`。  
合并后的结果为 `[1,2,2,3,5,6]`，其中下划线标出的元素来自 `nums1`。

**示例 2**  
**输入**: `nums1 = [1]`, `m = 1`, `nums2 = []`, `n = 0`  
**输出**: `[1]`  
**解释**: 我们要合并的数组是 `[1]` 和 `[]`。  
合并后的结果为 `[1]`。

**示例 3**  
**输入**: `nums1 = [0]`, `m = 0`, `nums2 = [1]`, `n = 1`  
**输出**: `[1]`  
**解释**: 我们要合并的数组是 `[]` 和 `[1]`。  
合并后的结果为 `[1]`。需要注意的是，因为 `m = 0`，`nums1` 中实际上没有元素。这里的 `0` 仅用于保证合并结果能够放入 `nums1`。

---

### 约束条件

- `nums1.length == m + n`
- `nums2.length == n`
- `0 <= m, n <= 200`
- `1 <= m + n <= 200`
- `-10^9 <= nums1[i], nums2[j] <= 10^9`

---

### 进阶

你能否想出一个时间复杂度为 `O(m + n)` 的算法来完成合并？

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把两段已经排好序的子数组 **直接拼在一起**，再把整个数组重新排序。  
- **数据结构**：这里仅使用普通的 Python 列表（list），相当于我们生活中常见的“排好序的商品货架”。  
- **为什么正确**：把 `nums1[:m]`（原来的有效部分）和 `nums2[:n]` 合并成一个新列表后，整体排序后的顺序一定就是题目要求的非递减序列。  
- **复杂度分析**：  
  - 先把两个子数组拼在一起，需要遍历 `m + n` 个元素，时间是 `O(m+n)`。  
  - 再调用 Python 内置的 `sort()`，最坏情况会进行 `O((m+n)·log(m+n))` 次比较。  
  - 额外空间：我们新建了一个长度为 `m+n` 的列表，空间是 `O(m+n)`。  
  - 大白话：如果你有 100 本书，要先把它们全部放到桌子上（`O(100)`），再把它们重新排好顺序需要花大约 `100·log₂100 ≈ 664` 步（`O(100·log100)`）。

#### 代码（Python）

```python
def merge_brute(nums1, m, nums2, n):
    """
    暴力解：先把有效部分取出来拼在一起，再整体排序
    """
    # 1. 取出 nums1 前 m 个有效元素，和 nums2 前 n 个元素
    merged = nums1[:m] + nums2[:n]          # O(m+n) 的拼接
    # 2. 对合并后的列表进行排序
    merged.sort()                           # O((m+n)·log(m+n))
    # 3. 把排好序的结果写回 nums1（原地修改）
    for i in range(m + n):
        nums1[i] = merged[i]                # O(m+n) 的拷贝
```

#### 复杂度  

- **时间复杂度**：`O((m + n)·log(m + n))` —— 主要是排序的开销。  
- **空间复杂度**：`O(m + n)` —— 需要额外的临时列表 `merged` 来保存合并后的元素。  

---  

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **排序** 这一步。因为两个子数组本身已经是有序的，我们完全可以 **利用已有的顺序**，一次遍历就把它们合并好——这就是经典的“双指针”技巧。

1. **从后往后放**：`nums1` 的长度已经够容纳 `m+n` 个元素，后面的 `n` 个位置是空的（最开始是 0），我们可以从数组尾部开始填。这样就不会把还未比较的元素覆盖掉。  
2. **双指针**：设 `i = m-1` 指向 `nums1` 有效部分的最后一个元素，`j = n-1` 指向 `nums2` 的最后一个元素，`k = m+n-1` 指向 `nums1` 最后一个可写位置。每一步比较 `nums1[i]` 与 `nums2[j]`，把较大的放到 `nums1[k]`，对应的指针左移。  
3. **处理剩余**：如果 `nums2` 还有剩余（`j >= 0`），说明它们都比 `nums1` 的剩余元素小，直接复制到前面。若 `nums1` 还有剩余，则已经在正确位置，无需额外操作。  

**类比**：想象两条已经排好序的队伍从后门依次走进一个更大的房间，房间里最靠后的座位先给排在后面的队员坐，这样前面的座位永远不会被后进的队员抢占。

#### 代码（Python）

```python
def merge(nums1, m, nums2, n):
    """
    最优解：双指针从后往前放，时间 O(m+n)，空间 O(1)
    """
    # i 指向 nums1 有效部分的末尾，j 指向 nums2 的末尾，k 指向合并后数组的末尾
    i, j, k = m - 1, n - 1, m + n - 1

    # 当两个指针都还有元素时，比较大小放入 nums1[k]
    while i >= 0 and j >= 0:
        if nums1[i] > nums2[j]:
            nums1[k] = nums1[i]   # 把 nums1[i] 放到最右侧
            i -= 1                # 向左移动 nums1 的指针
        else:
            nums1[k] = nums2[j]   # 把 nums2[j] 放到最右侧
            j -= 1                # 向左移动 nums2 的指针
        k -= 1                    # 合并后的位置左移一格

    # 如果 nums2 还有剩余（说明全部都比 nums1 小），直接复制过去
    while j >= 0:
        nums1[k] = nums2[j]
        j -= 1
        k -= 1
    # 当 i >= 0 时，nums1 已经在正确位置，无需额外操作
```

#### 复杂度  

- **时间复杂度**：`O(m + n)` —— 只遍历两数组一次，没有额外的排序。  
  - 含义：如果 `m = 100`、`n = 50`，最多只需要比较 150 次，就能得到答案。  
- **空间复杂度**：`O(1)` —— 只用了几个额外的指针变量，所有操作都在原数组 `nums1` 上完成。  
  - 含义：不需要再申请额外的列表，内存占用几乎不变。  

---  

## 心得  

- **核心技巧**：**双指针（从后向前）** 结合“原地覆盖”。  
- **适用题型**：  
  1. 合并两个有序数组（本题）。  
  2. 合并两个有序链表（LeetCode 21）。  
  3. 删除有序数组中的重复元素，只保留唯一值（LeetCode 26）——也常用双指针。  
- **一句话总结**：把较大的元素先放到末尾，既保持顺序，又避免覆盖未比较的元素。  

## 反思  

- **第一反应**：看到两个已经排好序的数组，第一时间想到 “先拼在一起再排序”。  
- **最容易踩的坑**：  
  - 忘记从 **后往前** 放，导致已经放好的元素被后面的覆盖。  
  - 忽略 `m` 或 `n` 为 0 的边界情况，尤其是 `nums1` 完全为空时仍需要把 `nums2` 复制进去。  
- **下次第一步**：先问自己 “能不能利用已有的有序信息？”——如果能，立刻考虑 **双指针** 或 **滑动窗口** 之类的线性合并思路。