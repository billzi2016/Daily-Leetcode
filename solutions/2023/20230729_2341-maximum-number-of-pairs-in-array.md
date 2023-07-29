# #2341. 数组中最大配对数 / Maximum Number of Pairs in Array

> 难度：简单 · 标签：Array、Hash Table、Counting · [LeetCode 链接](https://leetcode.com/problems/maximum-number-of-pairs-in-array/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums. In one operation, you may do the following:
The operation is done on nums as many times as possible.
Return a 0-indexed integer array answer of size 2 where answer[0] is the number of pairs that are formed and answer[1] is the number of leftover integers in nums after doing the operation as many times as possible.

**Examples**

**Example 1:**

```
Input: nums = [1,3,2,1,3,2,2]
Output: [3,1]
Explanation:
Form a pair with nums[0] and nums[3] and remove them from nums. Now, nums = [3,2,3,2,2].
Form a pair with nums[0] and nums[2] and remove them from nums. Now, nums = [2,2,2].
Form a pair with nums[0] and nums[1] and remove them from nums. Now, nums = [2].
No more pairs can be formed. A total of 3 pairs have been formed, and there is 1 number leftover in nums.
```

**Example 2:**

```
Input: nums = [1,1]
Output: [1,0]
Explanation: Form a pair with nums[0] and nums[1] and remove them from nums. Now, nums = [].
No more pairs can be formed. A total of 1 pair has been formed, and there are 0 numbers leftover in nums.
```

**Example 3:**

```
Input: nums = [0]
Output: [0,1]
Explanation: No pairs can be formed, and there is 1 number leftover in nums.
```

**Constraints**

- 1 <= nums.length <= 100
- 0 <= nums[i] <= 100

---

## 题目（中文翻译）

给定一个下标从 **0** 开始的整数数组 `nums`。一次操作可以执行以下步骤：

- 在 `nums` 中选取任意两个数值相同的元素，将它们配对并从数组中移除。

对 `nums` 重复执行上述操作，直到无法再形成新的配对为止。

返回一个下标从 **0** 开始、长度为 **2** 的整数数组 `answer`，其中 `answer[0]` 为形成的配对数，`answer[1]` 为在尽可能多次执行操作后 `nums` 中剩余的整数个数。

---

### 示例

**示例 1**

```
Input: nums = [1,3,2,1,3,2,2]
Output: [3,1]
Explanation:
- 将 `nums[0]` 与 `nums[3]` 配对并移除，它们的值都是 1。此时 nums = [3,2,3,2,2]。
- 将 `nums[0]` 与 `nums[2]` 配对并移除，它们的值都是 3。此时 nums = [2,2,2]。
- 将 `nums[0]` 与 `nums[1]` 配对并移除，它们的值都是 2。此时 nums = [2]。
- 已无法再形成配对。共形成了 3 对，剩余 1 个整数。
```

**示例 2**

```
Input: nums = [1,1]
Output: [1,0]
Explanation:
- 将 `nums[0]` 与 `nums[1]` 配对并移除，它们的值都是 1。此时 nums = []。
- 已无法再形成配对。共形成了 1 对，剩余 0 个整数。
```

**示例 3**

```
Input: nums = [0]
Output: [0,1]
Explanation:
- 无法形成配对，剩余 1 个整数。
```

---

### 约束

- `1 <= nums.length <= 100`
- `0 <= nums[i] <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**一次遍历数组，找到任意两个相同的数就把它们配成一对并删除**，然后把剩下的数组继续这么做，直到找不到相同的数为止。  
可以把数组想象成一堆零散的“水果”，我们每次从中挑出两颗相同品种的水果配对，拿走后剩下的水果继续挑。  

实现上可以使用两层循环：

1. 外层遍历每个元素 `i`（只要它还在数组里）。  
2. 内层从 `i+1` 开始找第一个和 `nums[i]` 相等的元素 `j`。  
3. 找到后，把这两个元素标记为“已配对”（比如把它们设为 `None`），计数器 `pairs += 1`。  
4. 继续外层的下一个未被标记的元素。  

因为每配成一对就把两个元素从数组中“删除”，所以最终未被标记的元素就是剩余的数字。

> **为什么这种方法一定能得到最大配对数？**  
> 只要有两个相同的数，就一定可以配成一对。我们每次都把能配的先配掉，后面再也不会出现因为先配错而导致配对数量减少的情况——配对的顺序并不影响总数，只要配对次数最多即可。

#### 代码（Python）

```python
from typing import List

def find_pairs_bruteforce(nums: List[int]) -> List[int]:
    # 用 None 表示已经被配对并“删除”的位置
    n = len(nums)
    used = [False] * n          # 标记每个位置是否已配对
    pairs = 0

    for i in range(n):
        if used[i]:                 # 已经配对过，直接跳过
            continue
        # 在 i 之后寻找第一个相同且未配对的元素
        for j in range(i + 1, n):
            if not used[j] and nums[i] == nums[j]:
                used[i] = used[j] = True   # 标记为已配对
                pairs += 1
                break                       # 找到一对后结束内层循环
    # 剩余未配对的元素即为 leftover
    leftover = sum(1 for flag in used if not flag)
    return [pairs, leftover]
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  两层循环最坏情况下要遍历 `n` × `n` 次。用大白话说，就是如果数组里几乎没有相同的数，我们几乎要把每个数都和后面的每个数比较一次，工作量会随 `n` 的平方增长。  
- **空间复杂度**：`O(n)`  
  额外用了一个和数组等长的布尔数组 `used` 来记录是否已配对，和原数组大小成正比。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**不停地在数组里找相同的数**，这一步用了 `O(n²)` 的时间。  
其实我们只需要知道每个整数出现了多少次，就能直接算出可以配多少对：  

- 如果某个数出现了 `cnt` 次，最多能配成 `cnt // 2` 对（整数除法），剩下 `cnt % 2` 个就是“剩余”。  
- 把所有数的配对数相加，就是答案的第一项；把所有数的剩余相加，就是答案的第二项。

要快速得到每个数的出现次数，**哈希表**（在 Python 中用 `dict` 或 `collections.Counter`）是最合适的工具。可以把它想象成一本“词典”，**key** 是数字本身，**value** 是它在数组里出现的次数。查一次字典的时间几乎是常数 `O(1)`，所以遍历一次数组就能把所有频率统计完。

**步骤**：

1. **统计频率**：遍历 `nums`，用哈希表 `freq` 记录每个数出现的次数。  
2. **累计结果**：遍历 `freq` 的每个 `(num, cnt)`，  
   - `pairs += cnt // 2`  
   - `leftover += cnt % 2`  
3. 返回 `[pairs, leftover]`。

这样只需要 **两次线性遍历**（一次算频率，一次算结果），时间复杂度降到 `O(n)`，空间只用来存哈希表，最多保存 `100`（因为 `0 ≤ nums[i] ≤ 100`）个键，仍是 `O(n)`（严格来说是 `O(k)`，`k` 为不同数字的种类数）。

#### 代码（Python）

```python
from typing import List
from collections import Counter

def find_pairs_optimal(nums: List[int]) -> List[int]:
    # 第一步：统计每个整数出现的次数（哈希表）
    freq = Counter(nums)          # Counter 相当于一个自动统计的词典

    pairs = 0      # 能组成的最大配对数
    leftover = 0   # 剩余未配对的数字个数

    # 第二步：根据每个频率直接算配对数和剩余数
    for cnt in freq.values():
        pairs += cnt // 2          # 每两个相同的数能组成一对
        leftover += cnt % 2        # 余数 1 表示还有一个单独留下

    return [pairs, leftover]
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  只遍历了数组一次（统计频率）和哈希表一次（累计结果），工作量随元素个数线性增长。用大白话说，就是元素多多少，时间就多多少，**没有平方级的爆炸**。  
- **空间复杂度**：`O(k)`（`k ≤ 101`），即 `O(n)` 的上界  
  只额外用了哈希表来存每种数字的计数，最坏情况下每个数字都不同，需要 `n` 个键。因为题目限制数字范围在 `0~100`，实际最多只会有 `101` 个键。

---

## 心得

- **核心技巧**：**利用哈希表统计频率**，再用整数除法 `//` 与取模 `%` 直接得到配对数和剩余数。  
- **适用的题型**  
  1. “找出可以组成多少对”类（如 **Array Partition**、**Maximum Number of K‑Divisible Elements**）。  
  2. “统计出现次数后进行分组/配对”类（如 **Longest Substring with At Most Two Distinct Characters**、**Minimum Operations to Reduce X to Zero** 中的计数思路）。  
- **解题钥匙**：**先把“需要的信息”（出现次数）弄清楚，再用数学公式直接算答案**。

---

## 反思

- **第一反应**：看到“配对”“删除”关键词，立刻想到两层循环去找相同元素。  
- **最容易踩的坑**  
  - 忘记把配对后剩下的单个元素计入 `leftover`，导致答案少了。  
  - 直接在原数组上 `pop` 会导致下标错位，使用标记或哈希表更安全。  
- **下次类似题**：**第一步先问自己“我需要哪些统计信息？”**，如果答案是“每个值出现几次”，就立刻想到哈希表或计数数组，从而把时间复杂度从 `O(n²)` 降到 `O(n)`。