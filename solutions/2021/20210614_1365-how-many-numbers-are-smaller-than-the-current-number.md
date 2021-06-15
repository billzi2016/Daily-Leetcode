# #1365. 有多少数字小于当前数字 / How Many Numbers Are Smaller Than the Current Number

> 难度：简单 · 标签：Array、Hash Table、Sorting、Counting Sort · [LeetCode 链接](https://leetcode.com/problems/how-many-numbers-are-smaller-than-the-current-number/)

---

## 题目（英文原版）

**Description**

Given the array nums, for each nums[i] find out how many numbers in the array are smaller than it. That is, for each nums[i] you have to count the number of valid j's such that j != i and nums[j] < nums[i].
Return the answer in an array.

**Examples**

**Example 1:**

```
Input: nums = [8,1,2,2,3]
Output: [4,0,1,1,3]
Explanation: 
For nums[0]=8 there exist four smaller numbers than it (1, 2, 2 and 3). 
For nums[1]=1 does not exist any smaller number than it.
For nums[2]=2 there exist one smaller number than it (1). 
For nums[3]=2 there exist one smaller number than it (1). 
For nums[4]=3 there exist three smaller numbers than it (1, 2 and 2).
```

**Example 2:**

```
Input: nums = [6,5,4,8]
Output: [2,1,0,3]
```

**Example 3:**

```
Input: nums = [7,7,7,7]
Output: [0,0,0,0]
```

**Constraints**

- 2 <= nums.length <= 500
- 0 <= nums[i] <= 100

---

## 题目（中文翻译）

给定一个数组 **nums**，对于每个 `nums[i]`，找出数组中有多少个数字比它小。也就是说，对于每个 `nums[i]`，需要统计满足 `j != i` 且 `nums[j] < nums[i]` 的下标 **j** 的个数。  
返回一个数组，其中第 `i` 个元素即为对应的计数结果。

**示例 1**  
**输入**: `nums = [8,1,2,2,3]`  
**输出**: `[4,0,1,1,3]`  
**解释**:  
- 对于 `nums[0]=8`，存在四个比它小的数字 (1, 2, 2, 3)。  
- 对于 `nums[1]=1`，不存在比它小的数字。  
- 对于 `nums[2]=2`，存在一个比它小的数字 (1)。  
- 对于 `nums[3]=2`，同样存在一个比它小的数字 (1)。  
- 对于 `nums[4]=3`，存在三个比它小的数字 (1, 2, 2)。

**示例 2**  
**输入**: `nums = [6,5,4,8]`  
**输出**: `[2,1,0,3]`

**示例 3**  
**输入**: `nums = [7,7,7,7]`  
**输出**: `[0,0,0,0]`

**约束条件**  
- `2 <= nums.length <= 500`  
- `0 <= nums[i] <= 100`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**对每一个位置 `i`，遍历整条数组，统计有多少个元素 `j` 满足 `nums[j] < nums[i]`**。  
这相当于让每个学生都去检查全班同学的成绩，看看有多少人比自己低。  

- **使用的数据结构**：仅仅是原数组 `nums` 本身和一个用来存放结果的列表 `ans`。不需要额外的高级结构。  
- **为什么正确**：因为我们逐个比较了所有可能的 `j`（包括自己），只要满足 “`j != i` 并且 `nums[j] < nums[i]`”，就计数一次，正好对应题目要求的“比当前数更小的数的个数”。  

#### 代码（Python）  

```python
def smallerNumbersThanCurrent(nums):
    n = len(nums)                     # 数组长度
    ans = [0] * n                      # 先准备好全 0 的答案列表

    for i in range(n):                # 外层遍历每个位置 i
        count = 0                      # 统计当前 i 前面有多少更小的数
        for j in range(n):            # 内层遍历所有位置 j
            if nums[j] < nums[i]:     # 如果 j 位置的数比 i 小
                count += 1            # 计数加一
        ans[i] = count                 # 把统计结果写入答案

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 这里的 `n` 是数组长度。外层循环 `n` 次，内层循环也要遍历 `n` 次，所以总共是 `n × n` 次比较。  
  - 用大白话说，就是如果数组有 100 条数据，程序要做大约 **1 万次** 的比较。  

- **空间复杂度**：`O(1)`（不计答案数组）  
  - 除了存放答案的列表外，只用了常数个额外变量 `count、i、j`，不随 `n` 增长而增长。  

---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**每次都要遍历整个数组**，导致 `O(n²)`。我们可以利用题目给出的两个重要信息来优化：

1. **数组长度最多 500，元素值在 0~100 之间**  
   - 这意味着数值范围很小（只有 101 种可能），可以用「计数」来快速得到每个数前面有多少更小的数。  

2. **我们只需要知道「比当前数更小」的数量，而不关心具体是哪几个**  
   - 只要知道每个数出现的次数，就可以累计得到「比它小的所有数的总和」。  

基于上述观察，有两种常用的优化思路：

- **排序 + 哈希**：先把数组排序，然后记录每个不同数第一次出现的下标（即有多少数比它小），最后把这个信息映射回原位置。  
- **计数排序（Counting Sort）**：因为数值范围固定，用一个长度为 101 的计数数组 `cnt[x]` 记录每个数 `x` 出现了多少次。随后把计数数组做前缀和 `pre[x] = cnt[0] + … + cnt[x-1]`，`pre[x]` 正好是「比 `x` 小的数的总个数」。  

这里采用 **计数排序**，因为实现最简洁且时间上是线性的 `O(n + m)`（`m = 101`），空间上只需要额外的 101 个整数。

**类比**：想象你在超市排队买饮料，饮料有 0~100 号共 101 种。你先统计每种饮料的库存（计数），再把库存累加起来得到「比某种饮料编号更小的所有饮料总数」，这样每次只看一次表就能直接回答「比我编号小的有多少」的问题。

#### 代码（Python）  

```python
def smallerNumbersThanCurrent(nums):
    # 1. 统计每个数出现的次数，cnt[i] 表示数字 i 在数组中出现了多少次
    cnt = [0] * 101                     # 因为 0 <= nums[i] <= 100
    for v in nums:                      # 遍历一次数组，计数
        cnt[v] += 1

    # 2. 计算前缀和：pre[i] = 所有小于 i 的数的出现次数总和
    pre = [0] * 101
    running = 0                         # 累计到当前 i-1 为止的总和
    for i in range(101):
        pre[i] = running                # 把累计值写入 pre[i]
        running += cnt[i]               # 再把 cnt[i] 加进去，为下一个 i 做准备

    # 3. 根据 pre 数组直接得到答案
    ans = [pre[v] for v in nums]        # 对原数组的每个元素 v，答案就是 pre[v]

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n + m)`，其中 `n = len(nums)`，`m = 101`（数值范围大小）。  
  - 实际上是一次遍历数组计数 `O(n)`，一次遍历长度为 101 的计数数组做前缀和 `O(m)`，以及一次生成答案的遍历 `O(n)`。  
  - 对于本题的约束，等价于 **线性时间**，远快于 `O(n²)` 的暴力解。  

- **空间复杂度**：`O(m)`，即额外使用了长度为 101 的两个数组 `cnt`、`pre`（常数级别的空间）。  
  - 与 `n` 无关，属于 **常数额外空间**。  

---  

## 心得  

- **核心技巧**：利用**计数排序**（或「值域有限」的前缀和）把“比某个数小的元素个数”一次性算好，再直接查表。  
- **适用的题型**：  
  1. “数组中有多少元素小于/大于某个值”——如 *Number of Smaller Elements After Self*（需要离线处理）  
  2. “统计每个数出现的次数并做累计”——如 *Relative Sort Array*、*Maximum Population Year*（时间范围有限）  
- **解题钥匙**：**先看数值范围**，如果范围小到可以直接计数，就用计数数组 + 前缀和，一次遍历即可搞定。  

---  

## 反思  

- **第一反应**：直接写双层循环，逐个比较。  
- **最容易踩的坑**：  
  - 忘记排除 `j == i` 的情况（计数时会把自己算进去）。  
  - 对于全相同的数组，要确保答案全是 0，计数法天然满足。  
- **下次遇到同类题**：第一步先检查“数值范围是否足够小”，如果是，就立刻考虑 **计数 + 前缀和** 的思路，而不是盲目排序或双指针。