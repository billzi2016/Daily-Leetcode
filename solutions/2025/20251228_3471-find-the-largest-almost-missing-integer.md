# #3471. 寻找最大的几乎缺失整数 / Find the Largest Almost Missing Integer

> 难度：简单 · 标签：Array、Hash Table · [LeetCode 链接](https://leetcode.com/problems/find-the-largest-almost-missing-integer/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and an integer k.
An integer x is almost missing from nums if x appears in exactly one subarray of size k within nums.
Return the largest almost missing integer from nums. If no such integer exists, return -1.

**Examples**

**Example 1:**

```
Input: nums = [3,9,2,1,7], k = 3
Output: 7
Explanation:
We return 7 since it is the largest integer that appears in exactly one subarray of size k .
```

**Example 2:**

```
Input: nums = [3,9,7,2,1,7], k = 4
Output: 3
Explanation:
We return 3 since it is the largest and only integer that appears in exactly one subarray of size k .
```

**Example 3:**

```
Input: nums = [0,0], k = 1
Output: -1
Explanation:
There is no integer that appears in only one subarray of size 1.
```

**Constraints**

- 1 <= nums.length <= 50
- 0 <= nums[i] <= 50
- 1 <= k <= nums.length

---

## 题目（中文翻译）

**描述**  
给定一个整数数组 `nums` 和一个整数 `k`。  
如果整数 `x` 恰好出现在 `nums` 中的 **一个子数组（subarray）** 且该子数组的大小为 `k`，则称 `x` 为 **几乎缺失（almost missing）**。  
返回 `nums` 中最大的几乎缺失整数。如果不存在满足条件的整数，返回 `-1`。

**示例**

> 示例 1  
> 输入: `nums = [3,9,2,1,7]`, `k = 3`  
> 输出: `7`  
> 解释:  
> 我们返回 `7`，因为它是唯一出现于大小为 `k` 的子数组且仅出现一次的最大整数。

> 示例 2  
> 输入: `nums = [3,9,7,2,1,7]`, `k = 4`  
> 输出: `3`  
> 解释:  
> 我们返回 `3`，因为它是唯一出现于大小为 `k` 的子数组且仅出现一次的最大整数。

> 示例 3  
> 输入: `nums = [0,0]`, `k = 1`  
> 输出: `-1`  
> 解释:  
> 没有整数仅出现在大小为 `1` 的子数组中。

**约束条件**  

- `1 <= nums.length <= 50`  
- `0 <= nums[i] <= 50`  
- `1 <= k <= nums.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有长度为 `k` 的子数组都列举出来**，然后逐个统计每个整数在这些子数组里出现了多少次。  
- **子数组**可以想象成连续的“窗口”，我们把窗口从左往右滑动，像在看一条跑道上的连续 `k` 个人。  
- 为了统计“出现次数”，我们可以使用 **哈希表**（在 Python 里是 `dict`），把整数当作 “词”，出现的子数组个数当作 “页码”。哈希表就像一本查字典的工具书，给定一个词（整数）可以立刻得到它对应的页码（出现次数）。  

具体步骤：
1. 枚举所有起始位置 `i`（`0 ≤ i ≤ n‑k`），得到子数组 `nums[i:i+k]`。  
2. 用 `set` 去重，得到该子数组里出现的**不同**整数。  
3. 把这些整数在哈希表中的计数加一。  
4. 完成所有窗口后，遍历哈希表，挑出计数恰好为 `1` 的整数，取其中最大的即为答案。  
5. 若没有计数为 `1` 的整数，返回 `-1`。

这种做法一定能得到正确答案，因为我们穷举了 **所有** 长度为 `k` 的子数组，并且对每个整数都精确记录了它出现的子数组数目。

#### 代码（Python）

```python
from typing import List

def largest_almost_missing_bruteforce(nums: List[int], k: int) -> int:
    n = len(nums)
    # cnt[x] 记录整数 x 出现在多少个长度为 k 的子数组中
    cnt = {}

    # 枚举每一个子数组的左端点
    for i in range(n - k + 1):
        # 当前子数组
        window = nums[i:i + k]
        # 用 set 去重，只统计不同的整数
        for x in set(window):
            cnt[x] = cnt.get(x, 0) + 1   # 哈希表计数 +1

    # 在所有出现次数恰好为 1 的整数中找最大值
    ans = -1
    for x, c in cnt.items():
        if c == 1 and x > ans:
            ans = x
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n * k)`  
  - 我们有 `n‑k+1`（≈ `n`）个窗口，每个窗口需要把 `k` 个元素放进 `set`，这一步是 `O(k)`。所以总体是 `O(n·k)`。  
  - 这里的 `O` 符号可以理解为“随输入规模线性增长”。如果 `n = 50, k = 25`，大约会执行 `1250` 次基本操作，仍然很快。

- **空间复杂度**：`O(m)`（`m` 为数组中不同整数的个数，最多 `51`）  
  - 主要是哈希表 `cnt` 和每次窗口的 `set`。因为题目限制 `0 ≤ nums[i] ≤ 50`，所以空间最多几百字节。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **重复遍历子数组**。实际上，题目可以用更精巧的观察一次性得到答案。

先把 `k` 分成三种情况：

| 情况 | 解释 |
|------|------|
| `k = 1` | 每个子数组只包含一个元素，等价于“数组中出现恰好一次的数”。 |
| `k = n`（`n` 为数组长度） | 整个数组本身是唯一的子数组，所有数都只出现一次子数组，答案就是数组的最大值。 |
| `1 < k < n` | 只要子数组长度既不是 `1` 也不是全部，那么 **只有数组的首元素 `nums[0]` 和尾元素 `nums[-1]`** 可能只出现在唯一的一个子数组。原因如下：<br>把窗口从左滑到右，窗口内部的元素（除首尾外）会被 **多次** 包含，因为它们既在左边的窗口里，又在右边的窗口里。只有最左边的元素只能被左端窗口覆盖，最右边的元素只能被右端窗口覆盖。于是“只出现一次子数组”的候选只能是这两个。 |

基于上述观察，最优解的步骤：

1. **统计整个数组中** `nums[0]` 和 `nums[-1]` 各出现了多少次（用哈希表或直接 `list.count`）。  
2. 根据出现次数决定答案：  
   - 若两个数都只出现一次，返回较大的那个。  
   - 若只有一个只出现一次，返回它。  
   - 若都出现多次，返回 `-1`。  
3. 对 `k = 1` 和 `k = n` 按表格中的特殊规则直接处理。

整个过程只需要一次遍历（或两次计数），不再枚举子数组，时间大幅下降。

#### 代码（Python）

```python
from typing import List

def largest_almost_missing(nums: List[int], k: int) -> int:
    n = len(nums)

    # 情形 1：k == 1
    if k == 1:
        # 统计每个数出现的次数，找只出现一次的最大值
        freq = {}
        for x in nums:
            freq[x] = freq.get(x, 0) + 1
        ans = -1
        for x, c in freq.items():
            if c == 1 and x > ans:
                ans = x
        return ans

    # 情形 2：k == n
    if k == n:
        # 整个数组是唯一子数组，直接返回最大元素
        return max(nums)

    # 情形 3：1 < k < n
    # 只可能是首元素或尾元素
    first, last = nums[0], nums[-1]

    # 统计这两个数在整个数组中的出现次数
    cnt_first = nums.count(first)
    cnt_last  = nums.count(last)

    # 根据出现次数挑选答案
    candidates = []
    if cnt_first == 1:
        candidates.append(first)
    if cnt_last == 1:
        candidates.append(last)

    if not candidates:          # 两个数都出现多次
        return -1
    return max(candidates)      # 取最大值
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 只需要一次（或两次）遍历数组统计出现次数。相比暴力的 `O(n·k)`，这里的“随数组长度线性增长”，即使 `n = 50` 也只会执行约 50 次基本操作。

- **空间复杂度**：`O(1)`（常数）  
  - 只用了几个整数变量来记录计数，没有额外随 `n` 增长的存储。

---

## 心得

- **核心技巧**：**利用窗口滑动的覆盖特性**，把问题转化为对首尾元素的简单计数。  
- **适用的题型**：  
  1. “只在唯一子数组出现” 类问题（如本题）。  
  2. “子数组覆盖次数” 统计类问题（如 `Count Number of Subarrays With Fixed Length`）。  
  3. “边界元素特殊性” 的题目（如只考虑数组首尾的最大/最小值）。  
- **一句话总结解题钥匙**：**先观察极端窗口（k=1、k=n）和窗口滑动的必然重复，再把注意力集中到可能唯一出现的边界元素上。**

---

## 反思

- **第一反应**：直接枚举所有子数组，写出完整的计数逻辑。  
- **最容易踩的坑**：  
  - 忽略 `k = 1` 时“子数组只含一个元素”，导致把所有出现一次的数都算进去（其实就是全局唯一数）。  
  - 在 `1 < k < n` 时误以为所有元素都可能只出现一次子数组，未注意到内部元素必被多个窗口覆盖。  
  - 边界条件 `k = n`（只有一个子数组）处理不当，直接返回 `-1`。  
- **下次类似题**：第一步先**思考窗口的覆盖范围**，找出“只能被唯一窗口覆盖的元素”，再**只统计这些候选**，而不是盲目遍历所有子数组。