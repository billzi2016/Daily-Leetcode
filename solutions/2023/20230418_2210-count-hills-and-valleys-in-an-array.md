# #2210. 数组中的山丘和谷地计数 / Count Hills and Valleys in an Array

> 难度：简单 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/count-hills-and-valleys-in-an-array/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums. An index i is part of a hill in nums if the closest non-equal neighbors of i are smaller than nums[i]. Similarly, an index i is part of a valley in nums if the closest non-equal neighbors of i are larger than nums[i]. Adjacent indices i and j are part of the same hill or valley if nums[i] == nums[j].
Note that for an index to be part of a hill or valley, it must have a non-equal neighbor on both the left and right of the index.
Return the number of hills and valleys in nums.

**Examples**

**Example 1:**

```
Input: nums = [2,4,1,1,6,5]
Output: 3
Explanation:
At index 0: There is no non-equal neighbor of 2 on the left, so index 0 is neither a hill nor a valley.
At index 1: The closest non-equal neighbors of 4 are 2 and 1. Since 4 > 2 and 4 > 1, index 1 is a hill. 
At index 2: The closest non-equal neighbors of 1 are 4 and 6. Since 1 < 4 and 1 < 6, index 2 is a valley.
At index 3: The closest non-equal neighbors of 1 are 4 and 6. Since 1 < 4 and 1 < 6, index 3 is a valley, but note that it is part of the same valley as index 2.
At index 4: The closest non-equal neighbors of 6 are 1 and 5. Since 6 > 1 and 6 > 5, index 4 is a hill.
At index 5: There is no non-equal neighbor of 5 on the right, so index 5 is neither a hill nor a valley. 
There are 3 hills and valleys so we return 3.
```

**Example 2:**

```
Input: nums = [6,6,5,5,4,1]
Output: 0
Explanation:
At index 0: There is no non-equal neighbor of 6 on the left, so index 0 is neither a hill nor a valley.
At index 1: There is no non-equal neighbor of 6 on the left, so index 1 is neither a hill nor a valley.
At index 2: The closest non-equal neighbors of 5 are 6 and 4. Since 5 < 6 and 5 > 4, index 2 is neither a hill nor a valley.
At index 3: The closest non-equal neighbors of 5 are 6 and 4. Since 5 < 6 and 5 > 4, index 3 is neither a hill nor a valley.
At index 4: The closest non-equal neighbors of 4 are 5 and 1. Since 4 < 5 and 4 > 1, index 4 is neither a hill nor a valley.
At index 5: There is no non-equal neighbor of 1 on the right, so index 5 is neither a hill nor a valley.
There are 0 hills and valleys so we return 0.
```

**Constraints**

- 3 <= nums.length <= 100
- 1 <= nums[i] <= 100

---

## 题目（中文翻译）

给定一个 **0-indexed**（从 0 开始索引）整数数组 `nums`。  
如果索引 `i` 的最近的非相等左邻居和右邻居的值都小于 `nums[i]`，则索引 `i` 属于山丘（hill）。  
同理，如果索引 `i` 的最近的非相等左邻居和右邻居的值都大于 `nums[i]`，则索引 `i` 属于谷地（valley）。  

当相邻的索引 `i` 与 `j` 满足 `nums[i] == nums[j]` 时，它们被视为同一个山丘或同一个谷地的一部分。  

注意：要使某个索引属于山丘或谷地，它在左侧和右侧都必须各至少存在一个 **非相等邻居**（即值不同的最近邻）。

返回数组 `nums` 中山丘和谷地的总数量。

## 示例

### 示例 1

```
Input: nums = [2,4,1,1,6,5]
Output: 3
Explanation:
At index 0: There is no non-equal neighbor of 2 on the left, so index 0 is neither a hill nor a valley.
At index 1: The closest non-equal neighbors of 4 are 2 and 1. Since 4 > 2 and 4 > 1, index 1 is a hill. 
At index 2: The closest non-equal neighbors of 1 are 4 and 6. Since 1 < 4 and 1 < 6, index 2 is a valley.
At index 3: The closest non-equal ...
```

（注：示例 1 的解释部分已截断）

### 示例 2

```
Input: nums = [6,6,5,5,4,1]
Output: 0
Explanation:
At index 0: There is no non-equal neighbor of 6 on the left, so index 0 is neither a hill nor a valley.
At index 1: There is no non-equal neighbor of 6 on the left, so index 1 is neither a hill nor a valley.
At index 2: The closest non-equal neighbors of 5 are 6 and 4. Since 5 < 6 and 5 > 4, index 2 is neither a hill nor a valley.
At index 3: The ...
```

（注：示例 2 的解释部分已截断）

## 约束条件

- `3 <= nums.length <= 100`
- `1 <= nums[i] <= 100`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

题目要求统计数组中“山”和“谷”的数量。  
- **山**：某个位置 `i` 左右最近的 **不相等** 元素都比 `nums[i]` 小。  
- **谷**：左右最近的 **不相等** 元素都比 `nums[i]` 大。  

最直接的想法是**对每个下标 `i` 都去向左、向右寻找最近的不同值**，得到 `left`、`right` 两个数后直接比较：

1. 从 `i-1` 向左遍历，直到找到 `nums[left] != nums[i]`（如果一直没有找到，说明左侧没有非相等邻居，`i` 不是山也不是谷）。  
2. 同理，从 `i+1` 向右遍历得到 `right`。  
3. 根据 `left`、`right` 的大小关系判断 `i` 是否是山或谷，计数。  

> **类比**：把数组想象成一条山路，站在第 `i` 坐标上，左边和右边的最近的“不同海拔标识牌”决定你所在的地形是山峰还是山谷。

**为什么正确**：题目定义正好是“左右最近的非相等邻居”，我们逐个检查每个位置，必然不遗漏也不会误判。

**时间/空间复杂度**：  
- 对每个 `i`，最坏情况要向左遍历 `O(n)`，向右遍历 `O(n)`，所以单个 `i` 需要 `O(n)`，整体是 `O(n²)`。  
- 只用了几个整数变量，额外空间是 `O(1)`。  

> **大白话**：`O(n²)` 就像在 100 人的队伍里，你让每个人都去检查前面和后面所有人一次，工作量会翻几倍，明显不够高效。

#### 代码（Python）  

```python
def countHillValley(nums):
    n = len(nums)
    ans = 0

    for i in range(n):
        # ① 找左侧最近的不同值
        left = i - 1
        while left >= 0 and nums[left] == nums[i]:
            left -= 1

        # ② 找右侧最近的不同值
        right = i + 1
        while right < n and nums[right] == nums[i]:
            right += 1

        # ③ 左右都有非相等邻居才可能是山或谷
        if left >= 0 and right < n:
            if nums[i] > nums[left] and nums[i] > nums[right]:
                ans += 1          # 山
            elif nums[i] < nums[left] and nums[i] < nums[right]:
                ans += 1          # 谷

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)` —— 每个位置最坏要遍历整条数组。  
- **空间复杂度**：`O(1)` —— 只用了常数个额外变量。  

---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**重复扫描相同的等值区间**。  
例如 `[2,4,1,1,6,5]` 中，索引 `2` 与 `3` 的值相同，左、右最近的不同值对它们来说完全一样，实际上它们属于同一个“山谷”。如果我们能**把相邻相等的元素先压缩成一个代表**，那么只需要在压缩后的序列上检查一次即可。

**关键步骤**：

1. **压缩数组**  
   - 用一个新列表 `compressed` 保存去掉连续相同元素后的序列。  
   - 示例：`[2,4,1,1,6,5] → [2,4,1,6,5]`。  
   - 这样，每个元素在压缩后一定两侧都有**不同**的邻居（除两端），不需要再在内部跳过相等的情况。

2. **遍历压缩后的序列**  
   - 对 `compressed[1] … compressed[-2]`（排除两端，因为两端缺少左/右邻居），检查：
     - 若 `compressed[i] > compressed[i-1]` 且 `compressed[i] > compressed[i+1]` → 山  
     - 若 `compressed[i] < compressed[i-1]` 且 `compressed[i] < compressed[i+1]` → 谷  
   - 每满足一次计数即可。

3. **为什么不重复计数**  
   - 在压缩前，所有相等的相邻元素被合并为一个代表，下标只出现一次，自然不会出现“同一个山/谷被算两次”的情况。

**核心算法**：**一次遍历 + 线性压缩**，属于**双指针/滑动窗口**的思路（一个指针遍历原数组，另一个指针负责写入压缩结果）。

**类比**：把一串连续相同颜色的珠子当成一颗“大珠子”，这样数山谷时只看“大珠子”之间的高低起伏。

#### 代码（Python）  

```python
def countHillValley(nums):
    """
    返回数组中山（hill）和谷（valley）的总数。
    思路：先压缩相邻相等的元素，再一次遍历判断高低。
    """
    # ① 线性压缩：去掉连续相同的元素
    compressed = []
    for x in nums:
        if not compressed or compressed[-1] != x:
            compressed.append(x)   # 只有当前元素和前一个不相等时才加入

    # ② 在压缩后的序列上统计山和谷
    ans = 0
    # 只遍历中间部分，两端必然缺少左/右非相等邻居
    for i in range(1, len(compressed) - 1):
        if compressed[i] > compressed[i - 1] and compressed[i] > compressed[i + 1]:
            ans += 1                # 山
        elif compressed[i] < compressed[i - 1] and compressed[i] < compressed[i + 1]:
            ans += 1                # 谷
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n)` ——  
  - 压缩一次遍历 `O(n)`；  
  - 再遍历压缩后序列最多 `n` 次（实际更少），总计线性。  
  - 与暴力解相比，从“每个位置都要找左右邻居”降到了“只看一次”。  

- **空间复杂度**：`O(n)`（最坏情况下压缩后仍然是原数组长度）——额外用了一个同等大小的列表。  
  - 由于 `n ≤ 100`，这个空间开销是完全可以接受的。  
  - 如果想进一步节约空间，也可以在原数组上就地压缩，只使用常数额外空间（这里为了代码可读性保留了 `compressed`）。

---  

## 心得  

- **核心技巧**：**相邻相等元素的合并（压缩）**，再进行一次线性检查。  
- **适用的题型**  
  1. “统计峰值/谷值” 类题目（如 LeetCode 2210 – Count Hills and Valleys in an Array）。  
  2. “删除连续重复元素后进行判断” 类题目（如 “删除数组中的重复项后求最长递增子序列”。）  
  3. “在压缩后数组上做单调性检查” 的题目（如 “删除重复后求峰值个数”。）  
- **一句话总结解题钥匙**：**先把连续相同的元素视为同一个点，再在这些点之间比较高低**。

## 反思  

- **第一反应**：直接对每个位置向左、向右搜最近的不同值——这就是暴力思路。  
- **最容易踩的坑**  
  - **边界条件**：数组两端没有左/右非相等邻居，必须排除。  
  - **重复计数**：相等的相邻元素如果不合并，会把同一个山/谷算多次。  
  - **压缩后长度为 1 或 2**：此时根本不存在山谷，需要返回 `0`（代码自然处理）。  
- **下次遇到同类题**：第一步先**把连续相同的元素压缩**，再在压缩后的序列上检查局部极值。这样既避免重复，又能做到线性时间。