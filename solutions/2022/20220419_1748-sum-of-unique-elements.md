# #1748. 唯一元素之和 / Sum of Unique Elements

> 难度：简单 · 标签：Array、Hash Table、Counting · [LeetCode 链接](https://leetcode.com/problems/sum-of-unique-elements/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums. The unique elements of an array are the elements that appear exactly once in the array.
Return the sum of all the unique elements of nums.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,2]
Output: 4
Explanation: The unique elements are [1,3], and the sum is 4.
```

**Example 2:**

```
Input: nums = [1,1,1,1,1]
Output: 0
Explanation: There are no unique elements, and the sum is 0.
```

**Example 3:**

```
Input: nums = [1,2,3,4,5]
Output: 15
Explanation: The unique elements are [1,2,3,4,5], and the sum is 15.
```

**Constraints**

- 1 <= nums.length <= 100
- 1 <= nums[i] <= 100

---

## 题目（中文翻译）

**描述**  
给定一个整数数组 `nums`。数组的唯一元素（unique elements）是指在数组中恰好出现一次的元素。返回 `nums` 中所有唯一元素的和。

**示例 1**  
**输入**: `nums = [1,2,3,2]`  
**输出**: `4`  
**解释**: 唯一元素为 `[1,3]`，它们的和为 `4`。

**示例 2**  
**输入**: `nums = [1,1,1,1,1]`  
**输出**: `0`  
**解释**: 没有唯一元素，和为 `0`。

**示例 3**  
**输入**: `nums = [1,2,3,4,5]`  
**输出**: `15`  
**解释**: 唯一元素为 `[1,2,3,4,5]`，它们的和为 `15`。

**约束条件**  

- `1 <= nums.length <= 100`
- `1 <= nums[i] <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**对每一个元素，遍历整个数组看看它出现了几次**。如果恰好出现一次，就把它加到答案里。  
- 用到的数据结构只有最基本的 **列表**（array）。我们不需要额外的容器，直接在原数组上循环即可。  
- 把它想象成在超市里挑商品：我们要检查每件商品是否只出现一次，就像把每件商品拿出来，再把整个超市里所有商品都比一遍，看看有没有相同的。  
- 只要所有元素都检查完，这个方法一定能得到正确答案，因为我们把“出现次数 = 1”这一条件完整地验证了。

#### 代码（Python）

```python
def sum_of_unique(nums):
    total = 0                     # 最终答案
    n = len(nums)

    # 对每一个位置 i 的元素，遍历整个数组计数
    for i in range(n):
        cnt = 0                   # 记录 nums[i] 出现的次数
        for j in range(n):
            if nums[j] == nums[i]:
                cnt += 1
        # 如果恰好出现一次，就累加到答案
        if cnt == 1:
            total += nums[i]

    return total
```

#### 复杂度  

- **时间复杂度：O(n²)**  
  解释：外层循环遍历 `n` 次，内层又要遍历 `n` 次，整体是 “n 乘 n”，也就是二次方。把它想象成“每个人都要和所有人握手”，手握次数会成平方增长。  
- **空间复杂度：O(1)**  
  只用了常数个额外变量（`total、cnt、i、j`），不随输入规模增长而增加。

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在 **每次都要遍历整个数组去计数**，导致二次方时间。  
我们可以把“每个数出现了几次”这件事 **提前算好**，这样后面只需要 **一次遍历** 就能判断是否唯一。  

实现思路：

1. **一次遍历** 把每个数字出现的次数记录下来。  
   - 这里使用 **字典（Hash Table）**，它的查找/写入都是 O(1) 的。可以把字典想象成 **查字典**：词（key）是数字，页码（value）是出现次数。  
2. 再 **一次遍历** 字典的键值对，把出现次数恰好为 1 的数字加到答案中。

这样我们把原来的 “每个数都要遍历整个数组” 的工作，拆成了两次 **线性** 的遍历，时间大幅下降。

#### 代码（Python）

```python
def sum_of_unique(nums):
    # 第一步：统计每个数字出现的次数
    freq = {}                     # freq 相当于“查字典”，key 是数字，value 是出现次数
    for num in nums:
        freq[num] = freq.get(num, 0) + 1   # 如果 num 已经在字典里，就在原有次数上加 1；否则默认 0 再加 1

    # 第二步：累加出现一次的数字
    total = 0
    for num, cnt in freq.items():          # items() 同时返回键和值
        if cnt == 1:                        # 只出现一次的就是唯一元素
            total += num

    return total
```

#### 复杂度  

- **时间复杂度：O(n)**  
  解释：我们只做了两次线性遍历，`n` 是数组长度。把它想象成“只需要一次排队检查所有商品”，检查次数随商品数量线性增长。相比暴力解的 O(n²)，提升非常明显。  
- **空间复杂度：O(k)**  
  解释：`k` 是不同数字的种类数。最坏情况下每个数字都不相同，`k = n`，因此额外使用的字典空间最多和输入规模相同。因为题目限制 `nums[i] ≤ 100`，实际最多只会有 100 个键，空间是常数级别的。

---

## 心得

- **核心技巧**：利用哈希表（字典）统计频次，然后一次遍历求和。  
- **适用的题型**  
  1. “找出只出现一次的数字”（如 LeetCode 136 Single Number）  
  2. “统计出现次数最多的元素”（如 LeetCode 1690 Majority Element）  
  3. “按出现次数排序数组”（如 LeetCode 1636 Sort Array by Increasing Frequency）  
- **解题钥匙**：**先把“出现次数”这件事提前算好，再根据次数直接得出答案**。

---

## 反思

- **第一反应**：直接用两层循环去计数，想到“遍历整个数组看每个数出现了几次”。  
- **最容易踩的坑**  
  - 忘记统计完后再遍历字典，直接在原数组里累计，导致重复计入非唯一元素。  
  - 边界情况：全部元素相同（答案应为 0）或全部不同（答案应为所有元素之和）。  
- **下次遇到同类题**：第一步就问自己“**我需要每个元素出现多少次**？”如果答案涉及次数，立刻想到使用 **字典/哈希表** 来统计频次。