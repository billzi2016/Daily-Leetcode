# #3065. 超过阈值的最小操作次数 I / Minimum Operations to Exceed Threshold Value I

> 难度：简单 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/minimum-operations-to-exceed-threshold-value-i/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums, and an integer k.
In one operation, you can remove one occurrence of the smallest element of nums.
Return the minimum number of operations needed so that all elements of the array are greater than or equal to k.

**Examples**

**Example 1:**

```
Input: nums = [2,11,10,1,3], k = 10
Output: 3
Explanation: After one operation, nums becomes equal to [2, 11, 10, 3].
After two operations, nums becomes equal to [11, 10, 3].
After three operations, nums becomes equal to [11, 10].
At this stage, all the elements of nums are greater than or equal to 10 so we can stop.
It can be shown that 3 is the minimum number of operations needed so that all elements of the array are greater than or equal to 10.
```

**Example 2:**

```
Input: nums = [1,1,2,4,9], k = 1
Output: 0
Explanation: All elements of the array are greater than or equal to 1 so we do not need to apply any operations on nums.
```

**Example 3:**

```
Input: nums = [1,1,2,4,9], k = 9
Output: 4
Explanation: only a single element of nums is greater than or equal to 9 so we need to apply the operations 4 times on nums.
```

**Constraints**

- 1 <= nums.length <= 50
- 1 <= nums[i] <= 109
- 1 <= k <= 109
- The input is generated such that there is at least one index i such that nums[i] >= k.

---

## 题目（中文翻译）

给定一个下标从 0 开始的整数数组 `nums`（integer array）和一个整数 `k`。  
一次操作可以删除 `nums` 中最小元素的一个出现位置。  
返回使数组中所有元素都大于等于 `k` 所需的最小操作次数。

**示例 1**  
```
Input: nums = [2,11,10,1,3], k = 10
Output: 3
Explanation: 在执行一次操作后，数组变为 [2,11,10,3]。
在执行两次操作后，数组变为 [11,10,3]。
在执行三次操作后，数组变为 [11,10]。
此时数组的所有元素均大于等于 10，过程结束。
可以证明，3 是使所有元素满足条件的最小操作次数。
```

**示例 2**  
```
Input: nums = [1,1,2,4,9], k = 1
Output: 0
Explanation: 数组的所有元素本身已经大于等于 1，无需进行任何操作。
```

**示例 3**  
```
Input: nums = [1,1,2,4,9], k = 9
Output: 4
Explanation: 只有一个元素（9）大于等于 9，需要对其余元素执行 4 次删除操作。
```

**约束条件**
- `1 <= nums.length <= 50`
- `1 <= nums[i] <= 10^9`
- `1 <= k <= 10^9`
- 输入保证至少存在一个下标 `i` 使得 `nums[i] >= k`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是 **一步步模拟题目描述的操作**：

1. 先把数组 `nums` 按从小到大排序（就像把一堆水果按重量从轻到重排好）。
2. 每次检查数组中最小的元素（排序后就是第一个），如果它已经 **≥ k**，说明所有元素都满足要求，停止。
3. 否则把这个最小元素删掉（相当于把最轻的水果挑走），计数器 `ops` 加 1，继续下一轮。

> **为什么这样会得到正确答案？**  
> 题目要求每一次只能删除 **当前最小的** 元素。如果我们每次都真的删掉当前最小的，那么在所有 **小于 k** 的元素全部被删掉之前，数组里一定还有至少一个 `< k` 的数。只要还有 `< k` 的数，就必须继续删除；只要没有 `< k` 的数，说明已经满足条件，操作可以停止。因此，模拟删除过程必然得到最少的操作次数。

#### 代码（Python）

```python
def min_operations_bruteforce(nums: list[int], k: int) -> int:
    # 1. 先把数组从小到大排好序
    nums.sort()                     # 排序好比把水果按重量从轻到重排好
    ops = 0                         # 记录已经做了多少次删除

    # 2. 循环检查最左侧（最小）的元素
    while nums and nums[0] < k:     # 只要最小的元素 < k，就必须继续删除
        nums.pop(0)                 # 删除最左侧的元素，相当于挑走最轻的水果
        ops += 1                    # 操作次数加一

    return ops
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  排序需要 `O(n log n)`，之后的删除循环最多 `n` 次，每次 `pop(0)` 在列表开头会把后面的元素整体左移，最坏是 `O(n)`，但因为 `n ≤ 50`，这里我们仍把整体复杂度记为 `O(n log n)`（排序是主要耗时）。
- **空间复杂度**：`O(1)`（不计输入本身）  
  只用了常数级别的额外变量 `ops`，没有额外的数组。

---

### 2. 最优解

#### 思路  
从暴力解可以看到，**真正决定操作次数的不是删除的顺序，而是有多少个元素小于 `k`**。因为：

- 每一次只能删最小的元素，但只要数组里还有 `< k` 的数，就必须继续删，最终一定要把所有 `< k` 的数全部清除。
- 删除顺序（先删最小的、再删次小的 …）并不影响需要删除的**数量**——只要把所有 `< k` 的数都删掉，条件就满足。

所以我们只要 **一次遍历数组，统计 `< k` 的元素个数**，这个计数就是答案。

> **类比**：想象一堆水果中有一些重量低于阈值 `k`，你只能一次只能挑走最轻的水果。无论挑走的顺序怎样，最终你必须把所有轻于 `k` 的水果全部挑走，挑走的次数恰好等于轻水果的数量。

#### 代码（Python）

```python
def min_operations(nums: list[int], k: int) -> int:
    # 直接统计有多少元素小于 k，即需要删除的次数
    count = 0
    for num in nums:                # 遍历数组的每一个元素
        if num < k:                 # 只要小于 k，就需要删除
            count += 1
    return count
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  只遍历一次数组，线性时间。对比暴力解的 `O(n log n)`，省去了排序这一步。
- **空间复杂度**：`O(1)`  
  只用了一个计数器 `count`，不占额外空间。

---

## 心得

- **核心技巧**：**一次遍历统计**——把“操作次数 = 不满足条件的元素个数”这一步抽象出来，避免不必要的排序或模拟。
- **适用的题型**  
  1. “删除最小/最大元素直至满足条件” 类似题目（如 “删除最小的字符直到字符串满足某个字典序”）。  
  2. “统计不符合阈值的元素数量” 的计数题（如 “数组中有多少元素大于等于目标值”。）
- **一句话总结**：**只要把所有“小于阈值”的元素数数出来，答案就出来了**。

---

## 反思

- **第一反应**：看到“每次只能删除最小的元素”，本能想到要先排序，然后一步步删，这就是暴力模拟的思路。
- **最容易踩的坑**  
  - 忽略了题目已经保证 **至少有一个元素 ≥ k**，所以不必考虑全部被删光的极端情况。  
  - 在实现暴力版时使用 `pop(0)` 会导致额外的 `O(n)` 移动，虽然题目规模小，但如果规模扩大会导致性能下降。  
- **下次遇到同类题的第一步**：先问自己 “到底要删除多少个元素？”——如果可以直接用**计数**得到答案，就不必真的去**模拟删除**。这一步常常能把时间复杂度从 `O(n log n)` 降到 `O(n)`。