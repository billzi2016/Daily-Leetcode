# #442. 数组中所有出现两次的数字 / Find All Duplicates in an Array

> 难度：中等 · 标签：Array、Hash Table · [LeetCode 链接](https://leetcode.com/problems/find-all-duplicates-in-an-array/)

---

## 题目（英文原版）

**Description**

Given an integer array nums of length n where all the integers of nums are in the range [1, n] and each integer appears at most twice, return an array of all the integers that appears twice.
You must write an algorithm that runs in O(n) time and uses only constant auxiliary space, excluding the space needed to store the output

**Examples**

**Example 1:**

```
Input: nums = [4,3,2,7,8,2,3,1]
Output: [2,3]
```

**Example 2:**

```
Input: nums = [1,1,2]
Output: [1]
```

**Example 3:**

```
Input: nums = [1]
Output: []
```

**Constraints**

- n == nums.length
- 1 <= n <= 105
- 1 <= nums[i] <= n
- Each element in nums appears once or twice.

---

## 题目（中文翻译）

给定一个长度为 **n** 的整数数组（integer array）`nums`，其中所有整数均在区间 **[1, n]** 内，并且每个整数最多出现两次，返回所有出现两次的整数构成的数组。  
你必须设计一个时间复杂度为 **O(n)**、额外空间复杂度为 **O(1)**（不计输出结果所需空间）的算法。

**示例 1**  
**输入:** `nums = [4,3,2,7,8,2,3,1]`  
**输出:** `[2,3]`

**示例 2**  
**输入:** `nums = [1,1,2]`  
**输出:** `[1]`

**示例 3**  
**输入:** `nums = [1]`  
**输出:** `[]`

**约束条件**
- `n == nums.length`
- `1 <= n <= 10^5`
- `1 <= nums[i] <= n`
- 每个元素在 `nums` 中出现一次或两次。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的办法就是把数组里每个数都跟其它所有数比对一次，看看它出现了几次。  
- **使用的数据结构**：只需要遍历原数组，不需要额外的数据结构。可以把「出现次数」想象成在课堂点名：老师把每个学生的名字从名单里找一遍，数数这个名字出现了几次。  
- **为什么正确**：只要把每个元素和所有其他元素全部比较，就一定能统计出每个数出现的次数，出现两次的自然就能被找出来。  
- **时间/空间复杂度**：  
  - 时间复杂度是 **O(n²)**，因为外层循环遍历 n 次，内层又要遍历 n 次（实际上是 n‑1、n‑2…，但量级仍然是 n²）。可以把它想象成在一张 10000×10000 的表格里逐格检查，规模会非常大。  
  - 空间复杂度是 **O(1)**（不计输出），只用了常数个临时变量。  

#### 代码（Python）  

```python
def findDuplicates_brute(nums):
    """
    暴力解：两层循环统计出现次数
    :param nums: List[int]，满足 1 ≤ nums[i] ≤ n 且每个数出现 1 次或 2 次
    :return: List[int]，所有出现两次的数
    """
    n = len(nums)
    res = []                     # 用来保存答案
    for i in range(n):           # 外层遍历每个元素
        cnt = 0                   # 统计 nums[i] 出现了几次
        for j in range(n):       # 内层遍历所有元素与 nums[i] 比较
            if nums[j] == nums[i]:
                cnt += 1
        # 如果出现次数恰好是 2，说明是我们要找的重复数
        if cnt == 2 and nums[i] not in res:   # 防止把同一个数加入多次
            res.append(nums[i])
    return res
```

#### 复杂度  

- **时间复杂度**：`O(n²)` —— “平方”意思是如果数组有 10 000 个元素，算法大概要跑 10 000 × 10 000 = 1 亿次比较，明显太慢。  
- **空间复杂度**：`O(1)` —— 只用了常数个额外变量（`cnt`, `res` 列表的大小不算在“辅助空间”里，因为它是最终输出的一部分）。

---

### 2. 最优解  

#### 思路  

从暴力解可以看出，**瓶颈在于每个元素都要去遍历整个数组**。  
我们需要把“查找”这一步从 `O(n)` 降到 `O(1)`，而且仍然只能使用 **常数额外空间**。  

题目给了两个关键限制：  

1. **数值范围**：所有元素都在 `[1, n]` 之间，恰好对应数组的下标（下标是 `0~n-1`，数值是 `1~n`）。  
2. **出现次数**：每个数最多出现两次。  

利用 **下标** 这个“天然哈希表”可以在原数组上做标记。具体做法：  

- 对数组中的每个数 `x`，把它对应的下标 `abs(x) - 1` 位置的元素取负（如果它还没被取负）。  
- 再次遍历时，如果发现某个位置已经是负数，说明对应的数已经出现过一次，这一次就是第二次出现，直接把它加入答案。  

为什么负号可以当“标记”？  
想象我们有一排盒子（数组），盒子编号 1~n。第一次把编号为 `x` 的盒子里的东西翻个面（取负），第二次再来时看到它已经是翻面的（是负数），就知道 `x` 出现了两次。  

整个过程只在原数组上做原地修改，使用的额外变量只有常数个，满足 **O(1) 额外空间** 的要求。  

#### 代码（Python）  

```python
def findDuplicates(nums):
    """
    最优解：利用数组下标做原地哈希标记
    :param nums: List[int]，满足 1 ≤ nums[i] ≤ n 且每个数出现 1 次或 2 次
    :return: List[int]，所有出现两次的数
    """
    res = []                     # 用来保存答案
    for num in nums:
        idx = abs(num) - 1       # 取绝对值后转成下标（因为可能已经被取负）
        if nums[idx] < 0:        # 已经是负数，说明对应的数之前出现过一次
            res.append(idx + 1)  # 加 1 把下标恢复成原来的数值
        else:
            nums[idx] = -nums[idx]   # 第一次出现，标记为负
    # （可选）如果后面还要使用原数组，可再把负数恢复正数
    # for i in range(len(nums)):
    #     nums[i] = abs(nums[i])
    return res
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 只遍历了两次数组，每个元素的操作都是 **常数时间**。相当于把原本的“千百次”比较压缩成“一次”检查。  
- **空间复杂度**：`O(1)` —— 只用了 `res`（输出）和几个临时变量 `idx`、`num`，不计入额外空间。  

与暴力解相比，时间从 **平方级** 降到了 **线性级**，大幅提升效率。

---

## 心得  

- **核心技巧**：利用**数组下标作为哈希表**，通过把对应位置的数取负来做“是否出现过”的标记。  
- **适用的题型**：  
  1. **找出数组中出现一次的数**（类似 448. Find All Numbers Disappeared in an Array）  
  2. **原地置零/原地排列**（如 287. Find the Duplicate Number）  
  3. **数组中缺失的数字**（如 41. First Missing Positive）  
- **一句话总结解题钥匙**：**“数值范围正好对应下标，利用负号原地做标记”**。

---

## 反思  

- **第一反应**：看到“每个数最多出现两次”，马上想到计数或哈希表，但受限于 **O(1) 额外空间**，只能在原数组上做标记。  
- **最容易踩的坑**：  
  - 忘记对 `num` 取绝对值，导致已经被取负的数再取负会出现错误的下标。  
  - 直接在 `if nums[idx] == 0` 判断，会因为原数组中可能出现 `0`（虽然本题不会出现）而出错，使用负号更安全。  
  - 题目要求 **不修改输出以外的空间**，如果后面还要使用原数组，需要在结束时把负数恢复成正数。  
- **下次第一步**：检查**数值范围与下标的对应关系**，如果可以把下标当作哈希表，就尝试**原地标记**（取负、加 n、置位等）来达到 O(1) 空间。