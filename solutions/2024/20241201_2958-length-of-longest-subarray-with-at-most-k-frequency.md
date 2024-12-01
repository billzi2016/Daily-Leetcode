# #2958. 最长子数组长度（每个元素出现频率至多为 K） / Length of Longest Subarray With at Most K Frequency

> 难度：中等 · 标签：Array、Hash Table、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/length-of-longest-subarray-with-at-most-k-frequency/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and an integer k.
The frequency of an element x is the number of times it occurs in an array.
An array is called good if the frequency of each element in this array is less than or equal to k.
Return the length of the longest good subarray of nums.
A subarray is a contiguous non-empty sequence of elements within an array.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,1,2,3,1,2], k = 2
Output: 6
Explanation: The longest possible good subarray is [1,2,3,1,2,3] since the values 1, 2, and 3 occur at most twice in this subarray. Note that the subarrays [2,3,1,2,3,1] and [3,1,2,3,1,2] are also good.
It can be shown that there are no good subarrays with length more than 6.
```

**Example 2:**

```
Input: nums = [1,2,1,2,1,2,1,2], k = 1
Output: 2
Explanation: The longest possible good subarray is [1,2] since the values 1 and 2 occur at most once in this subarray. Note that the subarray [2,1] is also good.
It can be shown that there are no good subarrays with length more than 2.
```

**Example 3:**

```
Input: nums = [5,5,5,5,5,5,5], k = 4
Output: 4
Explanation: The longest possible good subarray is [5,5,5,5] since the value 5 occurs 4 times in this subarray.
It can be shown that there are no good subarrays with length more than 4.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 109
- 1 <= k <= nums.length

---

## 题目（中文翻译）

给定一个整数数组 `nums` 和一个整数 `k`。  
元素 `x` 的频率（frequency）指的是它在数组中出现的次数。  
如果数组中每个元素的频率都小于等于 `k`，则该数组称为 **好数组**（good）。  
返回 `nums` 中最长的好子数组（subarray）的长度。  
子数组（subarray）是数组中连续且非空的元素序列。

**示例 1**  
**输入**: `nums = [1,2,3,1,2,3,1,2]`, `k = 2`  
**输出**: `6`  
**解释**: 最长的好子数组是 `[1,2,3,1,2,3]`，因为其中的值 `1、2、3` 的出现次数均不超过 `2`。同样，子数组 `[2,3,1,2,3,1]` 和 `[3,1,2,3,1,2]` 也满足条件。可以证明不存在长度大于 `6` 的好子数组。

**示例 2**  
**输入**: `nums = [1,2,1,2,1,2,1,2]`, `k = 1`  
**输出**: `2`  
**解释**: 最长的好子数组是 `[1,2]`，因为其中的值 `1` 和 `2` 各仅出现一次。子数组 `[2,1]` 也是好子数组。可以证明不存在长度大于 `2` 的好子数组。

**示例 3**  
**输入**: `nums = [5,5,5,5,5,5,5]`, `k = 4`  
**输出**: `4`  
**解释**: 最长的好子数组是 `[5,5,5,5]`，因为值 `5` 在该子数组中出现了 `4` 次，正好等于 `k`。可以证明不存在长度大于 `4` 的好子数组。

**约束条件**  
- `1 <= nums.length <= 10^5`  
- `1 <= nums[i] <= 10^9`  
- `1 <= k <= nums.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有子数组**，检查每个子数组里每个元素出现的次数是否 ≤ k，满足条件的就记录它的长度，最后取最大值。

- **枚举子数组**：用两个循环，外层 `i` 表示子数组左端点，内层 `j` 表示右端点，子数组即 `nums[i…j]`。  
- **统计频率**：对每个子数组，我们需要知道每个数出现了几次。这里可以用**哈希表**（在 Python 中就是 `dict`）来计数，哈希表就像一本**查字典**：单词是键（key），对应的页码是值（value），我们把数当成单词，把出现次数当成页码。  
- **判断是否满足**：遍历哈希表的所有键，只要有一个出现次数大于 `k`，这段子数组就不“好”。  

这种方法之所以**正确**，是因为我们把**所有可能的连续子序列**都检查了一遍，凡是满足题目条件的必然会被记录。

> **时间/空间复杂度**  
> - 两层循环 `i`、`j`，每一次都要重新遍历子数组里的元素统计频率，最坏情况是 `O(n³)`（`n` 为数组长度）。  
> - 哈希表最多保存子数组里所有不同的元素，最坏情况是 `O(n)`（子数组可能包含全部不同的数）。  

用大白话说，`O(n³)` 就像你让小朋友把 100 本书每本都翻三遍再数字，显然太慢了。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def longest_subarray_bruteforce(nums: List[int], k: int) -> int:
    n = len(nums)
    ans = 0                         # 记录最大长度

    # 枚举左端点 i
    for i in range(n):
        freq = defaultdict(int)     # 哈希表：统计从 i 开始的子数组频率
        # 枚举右端点 j
        for j in range(i, n):
            freq[nums[j]] += 1      # 把新加入的元素计数加一

            # 检查当前子数组是否仍然满足「每个元素出现次数 ≤ k」
            if all(cnt <= k for cnt in freq.values()):
                ans = max(ans, j - i + 1)   # 更新最大长度
            else:
                # 一旦出现次数超过 k，继续扩张只会更坏，直接跳出内层循环
                break

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n³)`  
  - 两层循环本身是 `O(n²)`，每次检查 `freq.values()` 需要遍历哈希表，最坏 `O(n)`，于是总体 `O(n³)`。  
  - 实际运行时会快一点，因为一旦频率超限我们会提前 `break`，但在最坏输入（如全部相同且 `k` 很大）仍然是立方级别。

- **空间复杂度**：`O(n)`  
  - 哈希表最多保存子数组里出现的所有不同元素，最坏情况是子数组长度等于 `n`，即需要 `O(n)` 的额外空间。

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于每次都重新统计子数组频率，导致大量重复工作。  
观察题目可以发现：我们只关心**“窗口”**（即当前考察的子数组）里每个数的出现次数是否超过 `k`。这正好符合**滑动窗口（Two‑Pointer）**的使用场景。

**核心想法**：

1. 用两个指针 `left`、`right` 维护一个**有效窗口** `nums[left … right]`，保证窗口内每个数的频率 ≤ k。  
2. `right` 每次向右扩展一格，加入新元素后更新哈希表的计数。  
3. 如果加入后出现次数 **超过 k**，说明窗口不再“好”。此时需要**收缩左边**（移动 `left`），把窗口左端的元素逐个移除并更新计数，直到所有频率再次 ≤ k。  
4. 每一次窗口合法时，用 `right - left + 1` 更新答案的最大值。  

这样每个元素**最多进窗口一次、出窗口一次**，整个过程是线性的。

> **为什么滑动窗口能工作？**  
> - 窗口的左端只会向右移动，永不回头；右端也只会向右前进。  
> - 当窗口非法（某个数出现次数 > k）时，唯一的办法是把左端往右推，让出现次数多的那个数离开窗口，直到合法为止。  
> - 这正是“**维护一个满足条件的连续子序列**”的典型做法。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def longest_subarray_sliding_window(nums: List[int], k: int) -> int:
    freq = defaultdict(int)   # 哈希表：记录窗口内每个数的出现次数
    left = 0                   # 窗口左端
    ans = 0

    # 右端指针逐步遍历整个数组
    for right, val in enumerate(nums):
        freq[val] += 1                         # 把新元素加入窗口并计数

        # 如果加入后出现次数超过 k，需要收缩左端
        while freq[val] > k:                   # 只要当前加入的这个数超限，就一直左移
            freq[nums[left]] -= 1              # 把左端元素的计数减一
            left += 1                          # 窗口左端右移一格

        # 此时窗口合法，更新最大长度
        ans = max(ans, right - left + 1)

    return ans
```

> **关键点说明**  
> - `while freq[val] > k` 只检查刚加入的 `val` 是否超限。因为窗口之前已经合法，只会因为这一次加入导致某个数（必是 `val`）次数超标。  
> - `freq[nums[left]] -= 1` 同时可能把别的数的计数降到 `k` 以下，使窗口重新合法。  
> - 整个循环中，每个元素最多被 `right` 访问一次、`left` 访问一次，时间是线性的。

#### 复杂度

- **时间复杂度**：`O(n)`  
  - `right` 指针遍历一次数组，`left` 指针同样最多遍历一次（因为只会右移），所以总操作次数与 `n` 成正比。  
  - 与暴力解的 `O(n³)` 相比，速度提升了 **指数级**，在 10⁵ 规模的数据下也能毫秒级完成。

- **空间复杂度**：`O(m)`，其中 `m` 是窗口内不同元素的个数，最坏 `O(n)`。  
  - 只需要哈希表保存当前窗口的计数，随着窗口左移，旧的键会被删减或计数归零。

---

## 心得

- **核心技巧**：**滑动窗口 + 哈希表计数**，用于在 **“连续子序列满足频率上限”** 这类约束下求最长/最短长度。  
- **适用的相似题型**  
  1. *Longest Substring Without Repeating Characters*（字符不重复的最长子串）  
  2. *Maximum Size Subarray Sum Equals k*（子数组和等于 k 的最长长度）  
  3. *Fruit Into Baskets*（最多两种水果的最长连续区间）  
- **一句话总结解题钥匙**：**把“合法性检查”放在窗口的右端加入元素时，若失效就立即左移收缩，保持窗口始终合法，记录最大长度**。

---

## 反思

- **拿到题目第一反应**：先想到枚举所有子数组检查频率，写出最直接的暴力实现。  
- **最容易踩的坑**  
  - **频率更新不完整**：收缩左端时忘记把对应元素的计数减一，导致哈希表里残留旧计数。  
  - **遗漏多种超限情况**：只检查新加入的元素是否超限是对的，但如果实现时不小心写成 `while any(cnt > k for cnt in freq.values())`，会导致每次遍历全部键，时间退化。  
  - **边界条件**：`k` 等于数组长度时，整个数组都是合法子数组，需要保证代码能够返回 `len(nums)`。  
- **下次遇到同类题**：第一步先思考“**能否用滑动窗口把合法区间维持在 O(1) 检查**”。如果答案是肯定的，就立刻构造左右指针、哈希计数的框架，再细化收缩条件。