# #665. 非递减数组 / Non-decreasing Array

> 难度：中等 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/non-decreasing-array/)

---

## 题目（英文原版）

**Description**

Given an array nums with n integers, your task is to check if it could become non-decreasing by modifying at most one element.
We define an array is non-decreasing if nums[i] <= nums[i + 1] holds for every i (0-based) such that (0 <= i <= n - 2).

**Examples**

**Example 1:**

```
Input: nums = [4,2,3]
Output: true
Explanation: You could modify the first 4 to 1 to get a non-decreasing array.
```

**Example 2:**

```
Input: nums = [4,2,1]
Output: false
Explanation: You cannot get a non-decreasing array by modifying at most one element.
```

**Constraints**

- n == nums.length
- 1 <= n <= 104
- -105 <= nums[i] <= 105

---

## 题目（中文翻译）

给定一个包含 **n** 个整数的数组（array）`nums`，请判断是否只通过修改至多 **一个** 元素就能使其成为 **非递减（non-decreasing）** 数组。  
我们定义，当对所有满足 `0 ≤ i ≤ n-2`（0 基）的索引 `i`，都有 `nums[i] ≤ nums[i+1]` 时，该数组为非递减数组。

### 示例

**示例 1**  
```
Input: nums = [4,2,3]
Output: true
Explanation: 你可以将第一个 4 修改为 1，使数组成为非递减数组。
```

**示例 2**  
```
Input: nums = [4,2,1]
Output: false
Explanation: 无法通过修改至多一个元素使数组变为非递减数组。
```

### 约束条件
- `n == nums.length`
- `1 <= n <= 10^4`
- `-10^5 <= nums[i] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举**哪一个元素被改动，然后检查改动后整个数组是否满足“非递减”。  
- 对每个下标 `i`（`0 ≤ i < n`），我们把 `nums[i]` 暂时改成一个“合理的值”。最简单的做法是把它改成左边的值 `nums[i‑1]`（如果有）或右边的值 `nums[i+1]`（如果有），因为只要把它拉到两侧之间，冲突往往会消失。  
- 改动完以后，遍历一遍数组，看是否每一对相邻元素都满足 `nums[j] ≤ nums[j+1]`。  
- 只要出现一次成功的改动，就返回 `True`；遍历完所有位置仍未成功，则返回 `False`。  

> **类比**：把数组想象成一条排队的队伍，只有一位同学可以调换座位（改动一次），我们尝试让每一位同学都去坐在左边或右边同学的座位上，然后再检查队伍是否已经排好序了。

这个方法一定能得到正确答案，因为我们把**所有可能的改动**都尝试了一遍（虽然实际改动的取值很多，但只要改成左/右相邻值就已经覆盖了所有能让冲突消失的情况）。

#### 代码（Python）

```python
from typing import List
import copy

def check_non_decreasing_bruteforce(nums: List[int]) -> bool:
    n = len(nums)
    # 先检查原数组是否已经非递减
    if all(nums[i] <= nums[i + 1] for i in range(n - 1)):
        return True

    # 枚举每一个可能被改动的下标 i
    for i in range(n):
        # 把原数组拷贝出来，防止改动影响后面的尝试
        arr = nums[:]

        # 试着把 nums[i] 改成左边的值（如果左边存在），或者右边的值（如果右边存在）
        # 这里尝试两种可能：改成左侧或改成右侧
        candidates = []
        if i - 1 >= 0:
            candidates.append(nums[i - 1])          # 拉低到左边的值
        if i + 1 < n:
            candidates.append(nums[i + 1])          # 抬高到右边的值

        for val in candidates:
            arr[i] = val
            # 检查改动后是否已经非递减
            if all(arr[j] <= arr[j + 1] for j in range(n - 1)):
                return True
    # 所有尝试都失败，说明不可能只改动一次就满足要求
    return False
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 外层遍历每个下标 `i`（`n` 次），  
  - 内层要遍历整个数组检查是否非递减（最坏 `n` 次），  
  - 所以总体大约是 `n × n = n²`。  
  - 用大白话说：如果数组有 10,000 个元素，最坏情况下需要检查 100,000,000 次——显然太慢了。

- **空间复杂度**：`O(n)`  
  - 每次改动我们都拷贝一份原数组，拷贝的大小和原数组一样。  
  - 除此之外只用了常数级别的额外变量。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都完整遍历数组**来验证。其实我们只需要一次线性遍历，就能判断是否可以通过一次改动解决。

关键观察：

1. **冲突点**  
   当出现 `nums[i] > nums[i+1]` 时，说明这两个位置违反了非递减的要求。我们把这种情况叫“冲突”。如果冲突出现 **两次或更多**，无论怎么改动一个元素，都无法一次性消除所有冲突，因为一次改动只能影响至多相邻的两段。  
   → 因此，冲突次数 > 1 时直接返回 `False`。

2. **只有一次冲突时如何处理**  
   设冲突出现在位置 `i`（即 `nums[i] > nums[i+1]`），我们可以有两种改动方案：

   - **把 `nums[i]` 降低**（让它不大于右边的 `nums[i+1]`），或者
   - **把 `nums[i+1]` 提高**（让它不小于左边的 `nums[i]`）。

   哪种方案更安全取决于 **冲突两侧的邻居**：

   - 如果 `i == 0`（冲突在最左边），我们只能把 `nums[i]` 降低，因为左边没有元素来限制。
   - 如果 `i+1 == n-1`（冲突在最右边），只能把 `nums[i+1]` 提高。
   - 否则，我们检查 `nums[i-1]` 与 `nums[i+1]` 的关系：  
     - 若 `nums[i-1] <= nums[i+1]`，把 `nums[i]` 降到 `nums[i-1]`（或者直接设为 `nums[i+1]`）是安全的，因为左侧已经不比右侧大。  
     - 若 `nums[i-1] > nums[i+1]`，则把 `nums[i]` 降低会导致 `nums[i-1] > nums[i]`，仍然是冲突。此时只能把 `nums[i+1]` 提高到 `nums[i]`，这样右侧的顺序会被修复。

   通过一次线性扫描，我们记录冲突次数，并在第一次冲突时**就直接在原数组上做一次“模拟改动”**（只需要改动一个数值即可），随后继续扫描确保没有第二次冲突。

> **类比**：想象一条河流中出现了一段倒流（`nums[i] > nums[i+1]`），我们只能在倒流处放一块石头改变水流方向。若河流中出现两段倒流，单块石头根本挡不住两处，问题无解。

#### 代码（Python）

```python
from typing import List

def check_non_decreasing(nums: List[int]) -> bool:
    """
    贪心一次遍历 O(n) 判断是否可以通过修改至多一个元素使数组非递减。
    """
    n = len(nums)
    cnt = 0                     # 记录冲突（nums[i] > nums[i+1]）出现的次数

    for i in range(n - 1):
        if nums[i] > nums[i + 1]:   # 发现一次冲突
            cnt += 1
            if cnt > 1:             # 超过一次冲突直接返回 False
                return False

            # ----- 决定如何“修改” -----
            # 情形 1：冲突在最左边，只能把 nums[i] 降低
            if i == 0:
                nums[i] = nums[i + 1]          # 让它等于右边的数
            # 情形 2：冲突在最右边，只能把 nums[i+1] 提高
            elif i + 1 == n - 1:
                nums[i + 1] = nums[i]          # 让它等于左边的数
            else:
                # 检查左侧邻居 nums[i-1] 与右侧邻居 nums[i+1] 的大小关系
                if nums[i - 1] <= nums[i + 1]:
                    # 可以安全地把 nums[i] 降低到 nums[i-1]（或直接设为 nums[i+1]）
                    nums[i] = nums[i - 1]
                else:
                    # 否则只能把 nums[i+1] 提高到 nums[i]
                    nums[i + 1] = nums[i]

    # 循环结束后冲突次数不超过 1，说明可以通过一次改动实现非递减
    return True
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历一次数组，检查相邻关系并在需要时做一次“模拟改动”。  
  - 用大白话说：如果数组有 10,000 个元素，只需要检查 9,999 次，比暴力的 100,000,000 次少了几个数量级，几乎是瞬间完成。

- **空间复杂度**：`O(1)`  
  - 只用了几个整数变量（`cnt`, `i` 等）和对原数组的原地修改，没有额外的与 `n` 成正比的存储。

---

## 心得

- **核心技巧**：**贪心 + 一次冲突计数**。在只能改动一次的限制下，冲突出现的次数直接决定答案的可行性。  
- **适用场景**：类似只能进行**一次局部修改**的题目，例如  
  1. LeetCode 665 – *Non-decreasing Array*（本题）  
  2. LeetCode 1909 – *Remove One Element to Make the Array Strictly Increasing*  
  3. LeetCode 1909 – *Maximum Subarray Sum After One Operation*（需要一次增/减）  
- **一句话总结**：**只要冲突不超过一次，就能通过一次“把高的降或把低的抬”把数组变成非递减**。

---

## 反思

- **第一反应**：看到“最多修改一个元素”，立刻想到**枚举每个位置的改动**，于是写出了暴力解。  
- **最容易踩的坑**  
  - **边界条件**：数组长度为 1 时天然满足；冲突出现在最左或最右时只能单向改动。  
  - **模拟改动的细节**：在冲突处如果直接把 `nums[i]` 设成 `nums[i+1]`，可能会破坏左侧已经满足的顺序，需要结合 `nums[i-1]` 的大小判断。  
  - **忘记计数**：如果只判断一次冲突而不记录次数，可能在出现两次冲突的情况下误判为 `True`。  
- **下次思路**：遇到“只能改动一次”这类限制时，**先找冲突点并统计次数**，再决定是否可以通过一次局部操作解决。这样往往能直接得到 O(n) 的贪心方案，避免先陷入枚举的暴力思路。