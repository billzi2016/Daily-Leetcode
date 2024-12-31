# #3005. 统计出现次数最高的元素个数 / Count Elements With Maximum Frequency

> 难度：简单 · 标签：Array、Hash Table、Counting · [LeetCode 链接](https://leetcode.com/problems/count-elements-with-maximum-frequency/)

---

## 题目（英文原版）

**Description**

You are given an array nums consisting of positive integers.
Return the total frequencies of elements in nums such that those elements all have the maximum frequency.
The frequency of an element is the number of occurrences of that element in the array.

**Examples**

**Example 1:**

```
Input: nums = [1,2,2,3,1,4]
Output: 4
Explanation: The elements 1 and 2 have a frequency of 2 which is the maximum frequency in the array.
So the number of elements in the array with maximum frequency is 4.
```

**Example 2:**

```
Input: nums = [1,2,3,4,5]
Output: 5
Explanation: All elements of the array have a frequency of 1 which is the maximum.
So the number of elements in the array with maximum frequency is 5.
```

**Constraints**

- 1 <= nums.length <= 100
- 1 <= nums[i] <= 100

---

## 题目（中文翻译）

你得到一个只包含正整数的数组 `nums`。  
返回数组中所有出现次数（frequency）达到最大值的元素的**总出现次数**。  
元素的出现次数是指该元素在数组中出现的次数。

**示例 1**  
**示例 2**  
**约束条件**：

**示例**  

**示例 1:**  
输入: `nums = [1,2,2,3,1,4]`  
输出: `4`  
解释: 元素 `1` 和 `2` 的出现次数都是 `2`，这是数组中的最大出现次数。  
因此，数组中出现次数为最大值的元素总共出现了 `4` 次。

**示例 2:**  
输入: `nums = [1,2,3,4,5]`  
输出: `5`  
解释: 数组中的所有元素出现次数都是 `1`，这就是最大出现次数。  
所以，数组中出现次数为最大值的元素总共出现了 `5` 次。

**约束条件**  
- `1 <= nums.length <= 100`  
- `1 <= nums[i] <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是「把每个数都和其它所有数比一遍」，统计它出现了多少次。  
可以把数组想象成一排坐着的小朋友，我们要逐个询问「这位小朋友和后面的每一位小朋友是否同名」，把同名的次数累加起来，就得到了该小朋友的出现次数。  

具体步骤：

1. 对数组中的每一个位置 `i`，遍历整个数组统计 `nums[i]` 出现了多少次（用一个计数器 `cnt`）。
2. 把所有得到的出现次数放进一个列表 `freqs`，同时记录当前的最大出现次数 `max_freq`。
3. 再遍历一次 `freqs`，把等于 `max_freq` 的次数全部加起来，得到答案。

为什么正确？  
因为我们对每个元素都完整地统计了它在数组中出现的次数，随后只挑选出出现次数等于全体最大值的那些元素的出现次数相加，正好符合题意「所有出现次数为最大频率的元素在数组中的总出现次数」。

**时间/空间复杂度分析（大白话）**  

- 时间复杂度：外层遍历 `n` 次，内层每次又要遍历 `n` 次，总代价大约是 `n × n`，记作 **O(n²)**。把它想象成「把 n 张卡片两两配对检查」的工作量，随着 n 增大，工作量会以 **平方** 的速度增长。  
- 空间复杂度：我们只用了几个整数变量和一个长度为 `n` 的 `freqs` 列表，额外空间随 `n` 成正比，记作 **O(n)**。

#### 代码（Python）

```python
def maxFrequencyElements_bruteforce(nums):
    n = len(nums)
    # 第一次遍历：统计每个元素的出现次数
    freqs = []          # 用来保存每个位置对应的出现次数
    max_freq = 0        # 当前看到的最大出现次数

    for i in range(n):
        cnt = 0
        for j in range(n):
            if nums[j] == nums[i]:   # 把 nums[i] 和所有位置的数都比一遍
                cnt += 1
        freqs.append(cnt)            # 保存 nums[i] 的出现次数
        if cnt > max_freq:           # 同时维护最大出现次数
            max_freq = cnt

    # 第二次遍历：把所有等于 max_freq 的次数相加
    ans = 0
    for f in freqs:
        if f == max_freq:
            ans += f                 # 累加这些元素在数组中的总出现次数
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)` — 需要两层循环，像「把每个人都和所有人握手」一样，次数随 `n` 的平方增长。  
- **空间复杂度**：`O(n)` — 额外用了一个长度为 `n` 的列表来存每个位置的频率。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **「每个数都要遍历整条数组」**，这导致了 `n²` 的时间。  
观察题目，我们只需要 **每种不同的数出现了多少次**，而不必对每个位置都重复计数。  

**关键点**：  
- 用「哈希表」(Python 中的 `dict`) 来记录「数 → 出现次数」。哈希表可以把「查字典」的过程想象成「把单词翻到对应的页码」——只需要一次操作就能得到对应的值。  
- 统计完所有次数后，遍历哈希表找出最大的出现次数 `max_freq`。  
- 再遍历一次哈希表，把所有出现次数等于 `max_freq` 的 **频次**（即该数出现了多少次）相加，得到答案。

整个过程只需要 **两次线性遍历**，时间从 `O(n²)` 降到了 `O(n)`，空间仍然是 `O(k)`（`k` 为不同数字的种类数），在本题的约束下最多是 `100`，可以看作 `O(n)`。

**从零解释哈希表**  
哈希表是一种「键-值」映射的数据结构。把它想象成一本「电话簿」：你输入一个人的名字（键），立刻能得到他的电话号码（值），不需要从头到尾翻找。这里键是数组中的数字，值是该数字出现的次数。

#### 代码（Python）

```python
def maxFrequencyElements_optimal(nums):
    # 1️⃣ 统计每个数字的出现次数，使用 dict（哈希表）
    freq = {}                     # key: 数字，value: 出现次数
    for x in nums:
        freq[x] = freq.get(x, 0) + 1   # 若键不存在返回 0，再加 1

    # 2️⃣ 找到最大的出现次数
    max_freq = max(freq.values())      # 直接取所有次数的最大值

    # 3️⃣ 把所有出现次数等于 max_freq 的次数相加
    ans = 0
    for count in freq.values():
        if count == max_freq:
            ans += count               # 这里的 count 本身就是该数字在数组中的出现次数
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历数组一次（统计），再遍历哈希表两次（找最大、累计），整体随 `n` 成线性增长。相比暴力的 `n²`，大幅提升。  
- **空间复杂度**：`O(k)`，其中 `k` 为不同数字的种类数，最坏情况下 `k ≤ n`，所以也可以写成 `O(n)`。需要额外的字典来保存每个数字的计数。

---

## 心得

- **核心技巧**：使用哈希表（字典）完成「计数」任务。  
- **适用题型**：  
  1. 「出现次数最多的元素」系列（如 LeetCode 1697. 检查子数组是否存在最大公因数为 1）。  
  2. 「找出出现次数恰好为 k 的元素」类（如 347. 前 K 个高频元素）。  
  3. 「统计字符出现次数」类（如 383. 赎金信）。  
- **一句话总结**：**把「每个元素出现多少次」这件事交给哈希表，让它一次遍历帮你搞定**。

## 反思

- **第一反应**：先想到「遍历两次」——一次统计，一次找最大，感觉最直接。  
- **最容易踩的坑**：  
  - 忘记把「出现次数等于最大频率的所有次数」相加，而误以为只需要返回有多少种元素。  
  - 对空数组没有考虑（本题已保证长度 ≥ 1）。  
- **下次类似题的第一步**：**先问自己「这道题是否在找『出现次数』」**，如果是，立刻打开「哈希表计数」这把钥匙。