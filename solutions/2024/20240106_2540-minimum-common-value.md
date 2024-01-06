# #2540. 最小公共值 / Minimum Common Value

> 难度：简单 · 标签：Array、Hash Table、Two Pointers、Binary Search · [LeetCode 链接](https://leetcode.com/problems/minimum-common-value/)

---

## 题目（英文原版）

**Description**

Given two integer arrays nums1 and nums2, sorted in non-decreasing order, return the minimum integer common to both arrays. If there is no common integer amongst nums1 and nums2, return -1.
Note that an integer is said to be common to nums1 and nums2 if both arrays have at least one occurrence of that integer.

**Examples**

**Example 1:**

```
Input: nums1 = [1,2,3], nums2 = [2,4]
Output: 2
Explanation: The smallest element common to both arrays is 2, so we return 2.
```

**Example 2:**

```
Input: nums1 = [1,2,3,6], nums2 = [2,3,4,5]
Output: 2
Explanation: There are two common elements in the array 2 and 3 out of which 2 is the smallest, so 2 is returned.
```

**Constraints**

- 1 <= nums1.length, nums2.length <= 105
- 1 <= nums1[i], nums2[j] <= 109
- Both nums1 and nums2 are sorted in non-decreasing order.

---

## 题目（中文翻译）

给定两个整数数组 `nums1` 和 `nums2`，它们均已按非递减顺序（non‑decreasing order）排序，返回两个数组中**公共的最小整数**。如果 `nums1` 和 `nums2` 中不存在公共整数，则返回 `-1`。  
注意，若某整数在两个数组中各至少出现一次，则称该整数为 **公共的**（common）。

**示例 1**  
**输入**: `nums1 = [1,2,3]`, `nums2 = [2,4]`  
**输出**: `2`  
**解释**: 两个数组中共同出现的最小元素是 `2`，因此返回 `2`。

**示例 2**  
**输入**: `nums1 = [1,2,3,6]`, `nums2 = [2,3,4,5]`  
**输出**: `2`  
**解释**: 公共元素有 `2` 和 `3`，其中最小的是 `2`，所以返回 `2`。

**约束条件**  

- `1 <= nums1.length, nums2.length <= 10^5`  
- `1 <= nums1[i], nums2[j] <= 10^9`  
- `nums1` 和 `nums2` 均已按非递减顺序排序。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把 **第一个数组的所有元素** 记下来，然后把 **第二个数组的每个元素** 挨个检查它是否已经出现过。  
- 这里可以使用 **哈希表（Python 的 `set`）** 来存放已经出现的数字。  
- 把 `set` 想象成一本“查字典”：你把单词（这里是数字）写进去，想要查某个单词是否在字典里，只要看一眼（O(1) 时间）就知道。  

步骤如下：  

1. 把 `nums1` 中的所有数放进一个 `set`（相当于把它们全部记下来）。  
2. 遍历 `nums2`，只要发现当前数字在 `set` 里，就说明它在两个数组中都出现过。  
3. 因为题目要求 **最小的公共整数**，我们在遍历 `nums2` 时可以同时记录所有公共数字的最小值，或者直接在遍历时把所有公共数字放进列表，最后取 `min`。  

这种方法一定能找到答案（如果有公共数字的话），因为我们把 **所有** 可能的匹配都检查了一遍。  

#### 代码（Python）  

```python
def findSmallestCommonElement(nums1, nums2):
    # 1️⃣ 把 nums1 的所有元素放进集合，查找时 O(1)
    seen = set(nums1)                     # {1,2,3,...}
    
    # 2️⃣ 用一个变量记录当前找到的最小公共数，初始设为正无穷大
    min_common = float('inf')
    
    # 3️⃣ 遍历 nums2，若在集合中则更新 min_common
    for num in nums2:
        if num in seen:                    # O(1) 判断
            if num < min_common:           # 只保留最小的那个
                min_common = num
    
    # 4️⃣ 如果没有找到公共元素，返回 -1
    return -1 if min_common == float('inf') else min_common
```

#### 复杂度  

- **时间复杂度**：`O(m + n)`  
  - 把 `nums1` 放进集合需要遍历一次，时间是 `O(m)`（`m = len(nums1)`）。  
  - 再遍历 `nums2` 检查是否在集合里，需要 `O(n)`（`n = len(nums2)`）。  
  - 合在一起就是 `O(m + n)`，即“线性时间”。  
- **空间复杂度**：`O(m)`  
  - 需要额外的集合来存 `nums1` 的所有元素，最坏情况下集合里会有 `m` 个数。  

> **大白话解释**：时间复杂度 `O(m + n)` 就是说，程序的运行时间大概和两个数组的长度之和成正比；如果两个数组各有 10 万个元素，程序大概会执行 20 万次基本操作。空间 `O(m)` 表示我们额外用了和第一个数组一样多的内存来记住它的元素。  

---  

### 2. 最优解  

#### 思路  
虽然上面的暴力解已经是 **线性时间**，但它用了额外的 `O(m)` 空间。  
因为题目已经保证两个数组 **都是非递减（已排序）**，我们可以利用这个特性，用 **双指针**（two‑pointers）在 **常数额外空间** 下完成同样的任务。  

**瓶颈**：暴力解的瓶颈不是时间，而是额外的集合占用的内存。如果数组很大（上限 10⁵），额外的 `set` 仍然是可以接受的，但在面试中，展示利用已有排序特性来省空间往往更受青睐。  

**双指针的核心思想**：  
- 想象有两根指针 `i`、`j`，分别指向 `nums1`、`nums2` 的开头。  
- 每一步比较 `nums1[i]` 与 `nums2[j]`：  
  - 若相等，说明找到了一个公共元素，直接返回它（因为我们从最小的开始遍历，第一次相等的就是最小公共数）。  
  - 若 `nums1[i] < nums2[j]`，说明 `nums1[i]` 太小，后面的 `nums2` 都不可能比它更小，只能把 `i` 向右移动，让 `nums1` 的指针追上更大的数。  
  - 若 `nums1[i] > nums2[j]`，同理把 `j` 向右移动。  
- 当任意一个指针跑到数组末尾时，说明已经没有公共元素，返回 `-1`。  

**类比**：把两个排好队的学生（数组）分别站在两条平行的走道上，两人只能向前走，谁的号码更小就让那个人先走，直到两个人的号码相同——那就是最先相遇的最小公共号码。  

#### 代码（Python）  

```python
def findSmallestCommonElement(nums1, nums2):
    i, j = 0, 0                     # 两个指针分别指向数组开头
    n1, n2 = len(nums1), len(nums2)

    while i < n1 and j < n2:        # 只要两边都还有元素就继续比较
        a, b = nums1[i], nums2[j]

        if a == b:                  # 找到相等的，就是最小公共数
            return a

        if a < b:                   # a 更小，i 右移让 a 变大
            i += 1
        else:                       # b 更小，j 右移让 b 变大
            j += 1

    # 循环结束仍未返回，说明没有公共元素
    return -1
```

#### 复杂度  

- **时间复杂度**：`O(m + n)`  
  - 每次循环至少会让其中一个指针前进一步，最多移动 `m + n` 步。  
  - 与暴力解的时间相同，但没有哈希表的额外开销。  

- **空间复杂度**：`O(1)`  
  - 只用了几个整数变量（指针），不随输入规模增长。  

> **对比**：时间上两种方法一样快（都是线性），但最优解省掉了 `set` 所占的内存，真正做到“原地”求解。  

---  

## 心得  

- **核心技巧**：**双指针**（Two‑Pointers）在已排序数组上寻找交集或最小公共元素。  
- **适用的类似题型**：  
  1. “Intersection of Two Sorted Arrays” —— 找出两个已排序数组的交集。  
  2. “Merge Two Sorted Lists” —— 合并两个有序链表（同样用双指针）。  
  3. “Find Common Elements in Two Sorted Matrices” —— 在二维有序矩阵中找公共元素。  
- **一句话总结**：  
  > “当两个序列都已经排好序时，用两根指针同步前进，第一次相遇的元素就是最小公共值。”  

---  

## 反思  

- **第一反应**：看到“两个已排序数组”，立刻想到“可以用双指针遍历”。  
- **最容易踩的坑**：  
  - 忘记在指针移动后检查是否已经越界，导致 `IndexError`。  
  - 误以为可以直接返回 `min(set(nums1) & set(nums2))` 而忽视了空间限制（虽然在本题也能通过，但不是最优）。  
  - 忽略了 **返回 -1** 的情况，需要在循环结束后专门处理。  
- **下次遇到同类题的第一步**：  
  - 先确认数组是否已排序；如果是，立刻考虑 **双指针**（或**归并**）方案；如果不是，考虑先排序或使用哈希表。