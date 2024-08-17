# #2831. 寻找最长相等子数组 / Find the Longest Equal Subarray

> 难度：中等 · 标签：Array、Hash Table、Binary Search、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/find-the-longest-equal-subarray/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums and an integer k.
A subarray is called equal if all of its elements are equal. Note that the empty subarray is an equal subarray.
Return the length of the longest possible equal subarray after deleting at most k elements from nums.
A subarray is a contiguous, possibly empty sequence of elements within an array.

**Examples**

**Example 1:**

```
Input: nums = [1,3,2,3,1,3], k = 3
Output: 3
Explanation: It's optimal to delete the elements at index 2 and index 4.
After deleting them, nums becomes equal to [1, 3, 3, 3].
The longest equal subarray starts at i = 1 and ends at j = 3 with length equal to 3.
It can be proven that no longer equal subarrays can be created.
```

**Example 2:**

```
Input: nums = [1,1,2,2,1,1], k = 2
Output: 4
Explanation: It's optimal to delete the elements at index 2 and index 3.
After deleting them, nums becomes equal to [1, 1, 1, 1].
The array itself is an equal subarray, so the answer is 4.
It can be proven that no longer equal subarrays can be created.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= nums.length
- 0 <= k <= nums.length

---

## 题目（中文翻译）

**题目描述**  
给定一个 0 索引整数数组 `nums` 和一个整数 `k`。  
如果一个子数组（subarray）中所有元素相等，则称其为相等子数组。需要注意，空子数组也是相等子数组。  
在最多删除 `k` 个元素后，返回可能的最长相等子数组的长度。  
子数组是数组中连续（可以为空）的元素序列。

**示例 1**  
```
Input: nums = [1,3,2,3,1,3], k = 3
Output: 3
Explanation: 最优的做法是删除下标为 2 和 4 的元素。  
删除后，`nums` 变为 [1, 3, 3, 3]。  
最长的相等子数组起始于 i = 1，结束于 j = 3，长度为 3。  
可以证明不存在更长的相等子数组。
```

**示例 2**  
```
Input: nums = [1,1,2,2,1,1], k = 2
Output: 4
Explanation: 最优的做法是删除下标为 2 和 3 的元素。  
删除后，`nums` 变为 [1, 1, 1, 1]。  
整个数组本身就是相等子数组，因此答案为 4。  
可以证明不存在更长的相等子数组。
```

**约束条件**  
- `1 <= nums.length <= 10^5`  
- `1 <= nums[i] <= nums.length`  
- `0 <= k <= nums.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**枚举所有可能的子数组**，然后看看删掉不超过 `k` 个元素后，子数组里剩下的元素能否全部相等。  
具体步骤可以这样描述：

1. 先枚举子数组的左端点 `l`（`0 ≤ l ≤ n-1`），再枚举右端点 `r`（`l ≤ r ≤ n-1`），子数组就是 `nums[l … r]`。  
2. 对这个子数组，统计每个数字出现的次数（用哈希表 `cnt`，把它想象成一本“字典”，单词是数字，页码是出现次数）。  
3. 设出现次数最多的数字出现了 `max_freq` 次，那么要把子数组变成全部相同，只需要把其它数字删掉，删掉的个数就是 `len(subarray) - max_freq`。  
4. 如果 `len(subarray) - max_freq ≤ k`，说明在允许的删除次数内可以把它变成等值子数组，更新答案 `ans = max(ans, max_freq)`（因为最终的等值子数组长度等于保留下来的最多的那个数字的个数）。

**为什么正确**  
只要我们把子数组中出现次数最多的数字留下，其余的全部删掉，子数组必然变成全相等。只要删掉的数量不超过 `k`，这种做法就是合法的。遍历所有子数组就一定能找到最优的那一个。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def longestEqualSubarray_bruteforce(nums: List[int], k: int) -> int:
    n = len(nums)
    ans = 0                     # 最长等值子数组的长度
    # 枚举左端点
    for l in range(n):
        cnt = defaultdict(int) # 哈希表：数字 -> 出现次数
        # 枚举右端点
        for r in range(l, n):
            cnt[nums[r]] += 1   # 把新加入的元素计数
            # 当前子数组长度
            length = r - l + 1
            # 出现次数最多的数字有多少个
            max_freq = max(cnt.values())
            # 需要删除的元素数 = 子数组长度 - 保留下来的最多的那个数字的个数
            deletions = length - max_freq
            if deletions <= k:   # 删除不超过 k 个，合法
                ans = max(ans, max_freq)   # 更新答案
    return ans
```

#### 复杂度

- **时间复杂度：** `O(n³)`（外层两层循环是 `O(n²)`，内部 `max(cnt.values())` 需要遍历哈希表，最坏情况下哈希表大小是 `O(n)`，所以总体是 `O(n³)`）  
  用大白话说，就是如果数组有 10 000 个元素，程序会做 **上千亿** 次操作，显然跑不动。

- **空间复杂度：** `O(n)`（哈希表最多会存放 `n` 种不同的数字）  
  这相当于在纸上写下所有不同数字的出现次数。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**枚举所有子数组**，导致时间呈二次甚至三次方增长。  
观察题目可以发现：

- 等值子数组的“目标数字”一定是原数组里出现的某个数字 `x`。  
- 对于固定的 `x`，我们只关心它出现的**位置**（索引），而不必关心其它数字的具体值。  

**关键想法：**  
把每个数字 `x` 出现的所有索引收集起来，得到一个递增的序列 `indices_x`。  
在这个序列上使用**滑动窗口**（双指针）来寻找最长的「可接受」区间。  

窗口 `[i, j]` 表示我们挑选了 `indices_x[i] … indices_x[j]` 这几次出现的 `x`。  
如果把这几次 `x` 之间的所有非 `x` 元素删掉，那么窗口对应的子数组就会全部变成 `x`。  
需要删除的非 `x` 元素数可以这样算：

```
total_len = indices_x[j] - indices_x[i] + 1          # 这段在原数组中的总长度（包含了 x 和非 x）
num_x     = j - i + 1                               # 窗口里有多少个 x
deletions = total_len - num_x                       # 其余的都是非 x，需要删掉
```

条件 `deletions ≤ k` 表示在允许的删除次数内可以把这段变成全 `x`。  
我们在每个 `indices_x` 上用 **双指针** 维持这个不超过 `k` 的窗口，尝试让窗口尽可能宽（即 `num_x` 最大），这正是我们要的答案。

**为什么滑动窗口能做到 O(n)？**  
指针 `left` 只会向右移动，`right` 也只会向右移动，每次移动都做 **常数** 次计算，所以每个 `indices_x` 只遍历一次。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def longestEqualSubarray(nums: List[int], k: int) -> int:
    """
    对每个不同的数字 x，收集它出现的下标列表 indices_x，
    然后在该列表上使用滑动窗口求最长满足
        (indices_x[j] - indices_x[i] + 1) - (j - i + 1) <= k
    的窗口大小 j-i+1。
    """
    # 1. 把每个数字的出现位置收集起来
    pos = defaultdict(list)          # 哈希表：数字 -> 该数字出现的所有下标（升序）
    for idx, val in enumerate(nums):
        pos[val].append(idx)

    answer = 0

    # 2. 对每个数字的下标列表做滑动窗口
    for val, indices in pos.items():
        left = 0                      # 窗口左指针
        # 右指针遍历整个列表
        for right in range(len(indices)):
            # 计算窗口对应的原数组长度
            total_len = indices[right] - indices[left] + 1
            # 窗口里已有的该数字的个数
            num_val = right - left + 1
            # 需要删除的非该数字的数量
            deletions = total_len - num_val

            # 如果删除次数超过 k，左指针右移收缩窗口
            while deletions > k:
                left += 1
                total_len = indices[right] - indices[left] + 1
                num_val = right - left + 1
                deletions = total_len - num_val

            # 此时窗口合法，更新答案
            answer = max(answer, num_val)

    return answer
```

#### 复杂度

- **时间复杂度：** `O(n)`  
  - 收集下标的过程遍历一次数组：`O(n)`。  
  - 对每个不同的数字，其下标列表长度之和仍是 `n`，滑动窗口在每个列表上只移动指针两遍，整体仍是 `O(n)`。  
  相比暴力解，从 **指数级** 降到 **线性级**，即使是 10⁵ 长的数组也能在毫秒级跑完。

- **空间复杂度：** `O(n)`  
  - 需要存放所有下标，总数等于数组长度 `n`。  
  用纸记下每个数字出现的位置，也需要 `n` 行。

---

## 心得

- **核心技巧**：**对每个候选值单独建索引 + 滑动窗口**。  
- **适用的题型**：  
  1. “最长子数组/子串满足删掉 ≤ k 个元素后全部相同” 类（本题）。  
  2. “最长子数组满足出现次数 ≤ k” 之类的频次限制题（如 LeetCode 1004 “最长相同子数组”）。  
  3. “最长子数组满足两端差值 ≤ limit” 的滑动窗口变体（如 1438 “最长连续子数组”）。

- **一句话总结解题钥匙**：  
  “把问题转化为‘在同一数字的出现位置上，找最长的间隙不超过 k 的连续段’，用双指针一次扫完。”

---

## 反思

- **第一反应**：直接想到枚举子数组并统计最多出现次数的数字，没意识到可以把“目标数字”提前固定下来。  
- **最容易踩的坑**：  
  - **下标计算错误**：`total_len` 要加 `+1`，因为下标是闭区间；忘记这个会导致删除次数少算一。  
  - **窗口收缩条件**：一定要在 `while deletions > k` 循环里更新所有相关变量，否则可能出现无限循环。  
  - **空子数组**：题目说空子数组也算等值子数组，但答案显然不会是 0（因为至少可以保留一个元素），实现时不需要额外处理。  

- **下次遇到同类题**，第一步应想到：  
  “先把**目标元素**的所有位置列出来”，再在这些位置上**滑动窗口**检查“删掉多少非目标元素”。这样可以把原本的 O(n²) 或 O(n³) 的搜索压到 O(n)。