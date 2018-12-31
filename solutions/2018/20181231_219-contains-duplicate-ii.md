# #219. 包含重复元素 II / Contains Duplicate II

> 难度：简单 · 标签：Array、Hash Table、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/contains-duplicate-ii/)

---

## 题目（英文原版）

**Description**

Given an integer array nums and an integer k, return true if there are two distinct indices i and j in the array such that nums[i] == nums[j] and abs(i - j) <= k.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,1], k = 3
Output: true
```

**Example 2:**

```
Input: nums = [1,0,1,1], k = 1
Output: true
```

**Example 3:**

```
Input: nums = [1,2,3,1,2,3], k = 2
Output: false
```

**Constraints**

- 1 <= nums.length <= 105
- -109 <= nums[i] <= 109
- 0 <= k <= 105

---

## 题目（中文翻译）

给定一个整数数组 `nums` 和一个整数 `k`，如果存在两个不同的下标 `i` 和 `j` 满足 `nums[i] == nums[j]` 且 `abs(i - j) <= k`，则返回 `true`。

**示例 1**  
```text
Input: nums = [1,2,3,1], k = 3
Output: true
```

**示例 2**  
```text
Input: nums = [1,0,1,1], k = 1
Output: true
```

**示例 3**  
```text
Input: nums = [1,2,3,1,2,3], k = 2
Output: false
```

**约束条件**

- `1 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`
- `0 <= k <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把每一个元素都拿出来，和后面所有元素比较一次，只要出现相同的数且它们的下标差不超过 `k`，立刻返回 `True`。  
- **用到的数据结构**：普通的 Python 列表 `list`。我们直接遍历它，不需要额外的容器。可以把列表想象成一排排的信箱，信箱里装的是数字，我们逐个打开信箱，去看后面的每一个信箱里装的是什么。  
- **为什么正确**：因为我们枚举了所有可能的 `(i, j)` 配对（`i < j`），只要有一对满足题目条件，就一定会在遍历过程中被发现。  

#### 代码（Python）  

```python
def containsNearbyDuplicate_bruteforce(nums, k):
    n = len(nums)                     # 数组长度
    # i 从左到右遍历，每次都和后面的元素比较
    for i in range(n):
        # j 必须在 i 之后，并且距离不能超过 k
        for j in range(i + 1, min(i + k + 1, n)):
            # 如果发现相同的数，直接返回 True
            if nums[i] == nums[j]:
                return True
    # 循环结束仍未找到，说明不存在满足条件的下标对
    return False
```

#### 复杂度  
- **时间复杂度**：`O(n·k)`（最坏情况下接近 `O(n²)`）  
  - 大白话：我们最多会检查 `n` 次外层循环，每次最多检查 `k` 次内层循环。若 `k` 接近 `n`，就相当于要检查几乎所有的元素配对，工作量会呈平方级增长。  
- **空间复杂度**：`O(1)`  
  - 只用了常数个额外变量（`i、j、n`），不随输入规模增长。  

---  

### 2. 最优解  

#### 思路  
暴力解的瓶颈在于**重复检查**同一个数很多次。实际上，我们只需要关心“窗口”内最近的 `k` 个元素，因为题目要求两下标的距离不超过 `k`。  

**滑动窗口 + 哈希表**（这里用 Python 的 `set`）的核心思路如下：  

1. **维护一个大小不超过 `k` 的集合**，集合里存放当前窗口内的数值。可以把集合想象成一本“小字典”，键是数值，值是“这本字典里出现过”。  
2. 当遍历到第 `i` 个元素 `num = nums[i]` 时：  
   - 先检查 `num` 是否已经在集合中。若在，说明在窗口内已经出现过相同的数，且它们的下标差一定 ≤ `k`（因为窗口宽度正好是 `k`），直接返回 `True`。  
   - 若不在，就把 `num` 加入集合。  
3. 为了保证集合大小不超过 `k`，当窗口长度超过 `k` 时，需要**把最左侧的元素踢出集合**，即删除 `nums[i - k]`。这一步相当于窗口向右滑动一步。  

这样每个元素只会被 **加入一次、删除一次、查询一次**，整体线性时间完成。  

#### 代码（Python）  

```python
def containsNearbyDuplicate(nums, k):
    """
    使用滑动窗口 + 哈希集合判断是否存在满足条件的重复元素
    """
    window = set()                     # 当前窗口内的数值集合
    for i, num in enumerate(nums):
        # 1. 检查窗口里是否已经有相同的数
        if num in window:
            return True                # 找到满足条件的下标对，直接返回

        # 2. 把当前数加入窗口
        window.add(num)

        # 3. 保持窗口大小不超过 k
        #    当 i >= k 时，窗口左边界已经超出 k，移除最左侧的元素
        if i >= k:
            # nums[i - k] 是刚好在窗口左侧边界之外的那个元素
            window.remove(nums[i - k])

    # 循环结束仍未发现符合条件的重复数
    return False
```

#### 复杂度  
- **时间复杂度**：`O(n)`  
  - 大白话：我们只遍历了一遍数组，对每个元素做了常数次（最多三次）集合操作，工作量随元素个数线性增长。相比暴力的 `O(n·k)`，大幅提升。  
- **空间复杂度**：`O(k)`  
  - 集合里最多保存 `k` 个不同的数值（窗口大小），所以占用的额外空间与 `k` 成正比。若 `k` 很大（接近 `n`），最坏情况会是 `O(n)`，但仍比暴力的 `O(1)` 更有意义，因为我们换取了时间上的突破。  

---  

## 心得  

- **核心技巧**：**滑动窗口 + 哈希集合**，用于在“固定距离范围”内快速判断是否出现重复。  
- **适用的题型**：  
  1. *Contains Duplicate III*（判断距离与数值差都受限的重复）  
  2. *Longest Substring Without Repeating Characters*（最长不含重复字符的子串）  
  3. *Maximum Size Subarray Sum Equals k*（固定窗口求和）  
- **一句话总结解题钥匙**：**把“只关心最近 k 个元素”这件事用集合实现，窗口滑动时同步维护集合的大小**。  

---  

## 反思  

- **第一反应**：直接想到两层循环遍历所有配对，这是最自然的暴力实现。  
- **最容易踩的坑**：  
  - 忘记在窗口滑动时把左侧元素删掉，导致集合无限增长，进而出现错误的 `True`（因为同一个元素会被多次计入窗口）。  
  - `k = 0` 的特殊情况：窗口大小为 0，实际上不需要检查任何元素，直接返回 `False`（实现中自然会得到正确答案）。  
- **下次类似题目第一步**：**先确认“距离范围”或“窗口大小”，再思考如何在遍历时实时维护这个范围的状态**（通常用队列、集合或计数器实现）。