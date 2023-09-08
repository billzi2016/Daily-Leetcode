# #2395. 寻找和相等的子数组 / Find Subarrays With Equal Sum

> 难度：简单 · 标签：Array、Hash Table · [LeetCode 链接](https://leetcode.com/problems/find-subarrays-with-equal-sum/)

---

## 题目（英文原版）

**Description**

Given a 0-indexed integer array nums, determine whether there exist two subarrays of length 2 with equal sum. Note that the two subarrays must begin at different indices.
Return true if these subarrays exist, and false otherwise.
A subarray is a contiguous non-empty sequence of elements within an array.

**Examples**

**Example 1:**

```
Input: nums = [4,2,4]
Output: true
Explanation: The subarrays with elements [4,2] and [2,4] have the same sum of 6.
```

**Example 2:**

```
Input: nums = [1,2,3,4,5]
Output: false
Explanation: No two subarrays of size 2 have the same sum.
```

**Example 3:**

```
Input: nums = [0,0,0]
Output: true
Explanation: The subarrays [nums[0],nums[1]] and [nums[1],nums[2]] have the same sum of 0. 
Note that even though the subarrays have the same content, the two subarrays are considered different because they are in different positions in the original array.
```

**Constraints**

- 2 <= nums.length <= 1000
- -109 <= nums[i] <= 109

---

## 题目（中文翻译）

给定一个下标从 0 开始的整数数组 `nums`，判断是否存在 **两个长度为 2 的子数组（subarray）** 且它们的元素和相等。需要注意，这两个子数组的起始下标必须不同。  
如果存在满足条件的子数组，返回 `true`；否则返回 `false`。  

子数组（subarray）是数组中连续的、非空的元素序列。

**示例 1**  
**输入**: `nums = [4,2,4]`  
**输出**: `true`  
**解释**: 子数组 `[4,2]` 与 `[2,4]` 的和均为 `6`。

**示例 2**  
**输入**: `nums = [1,2,3,4,5]`  
**输出**: `false`  
**解释**: 没有任意两个长度为 2 的子数组具有相同的和。

**示例 3**  
**输入**: `nums = [0,0,0]`  
**输出**: `true`  
**解释**: 子数组 `[nums[0], nums[1]]` 与 `[nums[1], nums[2]]` 的和均为 `0`。虽然这两个子数组的内容相同，但它们位于原数组的不同位置，因而被视为不同的子数组。

**约束条件**  
- `2 <= nums.length <= 1000`  
- `-10^9 <= nums[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有长度为 `2` 的子数组的和全部算出来，然后两两比较，看有没有相同的。  

- **数据结构**：我们只需要一个普通的列表（array）来保存每个子数组的和。可以把它想象成「把每两本相邻的书的厚度加在一起，放进一本新笔记本」。
- **为什么正确**：题目要求“是否存在**两个**长度为 2 的子数组，它们的起始位置不同且和相等”。只要我们把 **所有** 可能的子数组的和列出来，随后检查是否出现重复，就一定能得到答案。
- **时间/空间复杂度**：  
  - 我们需要遍历数组的每一个相邻位置 `i`（`0 ≤ i < n‑1`），对每个位置再遍历后面的所有相邻位置 `j`（`i+1 ≤ j < n‑1`）进行比较，时间上是两层循环，形成 **O(n²)**（n 的平方）级别的计算。  
  - 这里的 **O(n²)** 可以理解为：如果数组长度是 100，程序大概会执行 100 × 100 ≈ 10 000 次核心操作。  
  - 需要额外的列表来保存所有子数组的和，最多有 `n‑1` 个子数组，空间复杂度是 **O(n)**。

#### 代码（Python）

```python
def findSubarrays_bruteforce(nums):
    """
    暴力解：枚举所有长度为 2 的子数组，逐个比较是否出现相同的和
    """
    n = len(nums)
    sums = []                     # 用来保存每个子数组的和
    # 第一个循环：遍历所有可能的起始位置 i
    for i in range(n - 1):
        cur_sum = nums[i] + nums[i + 1]   # 计算子数组 nums[i:i+2] 的和
        # 第二个循环：把当前和和之前出现过的每个和逐个比较
        for s in sums:
            if s == cur_sum:              # 只要出现一次相同，就可以返回 True
                return True
        sums.append(cur_sum)              # 把当前和加入列表，供后面的比较使用
    return False                           # 没有找到相同的和
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  两层循环导致操作次数随数组长度的平方增长。  
- **空间复杂度**：`O(n)`  
  需要一个长度为 `n‑1` 的列表来存放子数组的和。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于每次都要把当前的子数组和和之前所有的和逐个比较，这会产生大量重复工作。  
事实上，我们只需要知道「这个和之前出现过没有」即可，一旦出现过就可以立刻返回 `True`。这正好可以用 **哈希集合（set）** 来实现：  

- **哈希集合** 像一本「查字典」的工具书，**key** 是子数组的和，**value**（这里不需要）可以理解为「出现的页码」。查找一个 key 是否已经在集合里，时间是 **O(1)**（常数时间），几乎不随数据规模增长而变慢。  
- 遍历一次数组，计算每个相邻两数的和 `cur_sum`，立即检查 `cur_sum` 是否已经在集合 `seen` 中。  
  - 若在，说明之前已经出现过同样的和，返回 `True`。  
  - 若不在，就把 `cur_sum` 加入集合，继续往后走。  
- 只要遍历完整个数组仍未找到重复和，说明不存在满足条件的子数组，返回 `False`。

> **关键点**：集合的「**存在性检查**」比列表的「**遍历比较**」快得多，这就是从 `O(n²)` 降到 `O(n)` 的根本原因。

#### 代码（Python）

```python
def findSubarrays(nums):
    """
    最优解：使用哈希集合一次遍历完成检查
    """
    seen = set()                     # 用来存放已经出现过的子数组和
    for i in range(len(nums) - 1):   # 只需要遍历到倒数第二个元素
        cur_sum = nums[i] + nums[i + 1]   # 计算当前长度为 2 的子数组和
        if cur_sum in seen:               # O(1) 判断是否已经出现过
            return True                   # 找到相同的和，直接返回
        seen.add(cur_sum)                 # 把当前和加入集合，供后面比较
    return False                           # 遍历结束仍未发现相同的和
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  只需要一次线性遍历，每一步的「集合查找」和「集合插入」都是常数时间。相当于如果数组长度是 1000，最多只会执行大约 1000 次核心操作，远快于暴力解的 1 000 000 次。
- **空间复杂度**：`O(n)`  
  最坏情况下每个子数组的和都不相同，需要把 `n‑1` 个不同的和都放进集合中。

---

## 心得

- **核心技巧**：利用 **哈希集合（set）** 实现「是否出现过」的 O(1) 检查，从而把双重循环的暴力比较降到线性遍历。  
- **适用的题型**  
  1. 判断是否存在重复的子数组/子序列和（如「长度为 3 的子数组是否有相同和」）。  
  2. 判断数组中是否有两个元素之差为某个固定值（使用集合存已遍历元素）。  
  3. 判断是否存在两段区间的前缀和相等（前缀和 + 哈希集合）。  
- **一句话总结**：**「只要能把“出现过吗”转化为集合的 O(1) 查找，很多重复判断的题目都能一次遍历搞定」**。

---

## 反思

- **第一反应**：看到「两个子数组」立即想到「枚举所有组合」——这正是暴力解的思路。  
- **最容易踩的坑**  
  - **边界条件**：数组长度最小为 2，遍历时要确保 `i + 1` 不越界。  
  - **相同位置的子数组**：题目要求「起始位置不同」，所以只要两次出现相同的和，必然对应不同的起始下标（因为我们是顺序遍历的）。  
  - **负数和大数**：`nums[i]` 可能为负数或极大值，使用 Python 的整数不会溢出，但在其他语言需要注意整数范围。  
- **下次遇到同类题的第一步**：先问自己「这道题需要判断『是否出现过某个值』吗？」如果答案是「是」，立刻想到「哈希集合」或「哈希表」来实现 O(1) 判重。