# #992. 恰好包含 K 个不同整数的子数组 / Subarrays with K Different Integers

> 难度：困难 · 标签：Array、Hash Table、Sliding Window、Counting · [LeetCode 链接](https://leetcode.com/problems/subarrays-with-k-different-integers/)

---

## 题目（英文原版）

**Description**

Given an integer array nums and an integer k, return the number of good subarrays of nums.
A good array is an array where the number of different integers in that array is exactly k.
A subarray is a contiguous part of an array.

**Examples**

**Example 1:**

```
Input: nums = [1,2,1,2,3], k = 2
Output: 7
Explanation: Subarrays formed with exactly 2 different integers: [1,2], [2,1], [1,2], [2,3], [1,2,1], [2,1,2], [1,2,1,2]
```

**Example 2:**

```
Input: nums = [1,2,1,3,4], k = 3
Output: 3
Explanation: Subarrays formed with exactly 3 different integers: [1,2,1,3], [2,1,3], [1,3,4].
```

**Constraints**

- 1 <= nums.length <= 2 * 104
- 1 <= nums[i], k <= nums.length

---

## 题目（中文翻译）

给定一个整数数组（integer array）`nums` 和一个整数 `k`，返回 `nums` 中 **好子数组（good subarray）** 的数量。  
好子数组是指其中不同整数（different integers）的数量恰好等于 `k` 的子数组。  
子数组（subarray）是数组中连续的一个片段。

**示例 1**  

**示例 2**  

**约束条件**  

**示例**  

**示例 1**  
输入: `nums = [1,2,1,2,3]`, `k = 2`  
输出: `7`  
解释: 恰好包含 2 个不同整数的子数组有: `[1,2]`, `[2,1]`, `[1,2]`, `[2,3]`, `[1,2,1]`, `[2,1,2]`, `[1,2,1,2]`  

**示例 2**  
输入: `nums = [1,2,1,3,4]`, `k = 3`  
输出: `3`  
解释: 恰好包含 3 个不同整数的子数组有: `[1,2,1,3]`, `[2,1,3]`, `[1,3,4]`  

**约束条件**  
- `1 <= nums.length <= 2 * 10^4`  
- `1 <= nums[i], k <= nums.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有** 子数组枚举出来，然后逐个检查它们里面有多少种不同的整数。如果恰好等于 `k`，计数器就加一。

- **子数组**：数组的连续片段。可以用两个指针 `i`（左边界）和 `j`（右边界）来表示，`i ≤ j` 时子数组为 `nums[i…j]`。
- **不同整数的个数**：我们可以用 **哈希表**（在 Python 中是 `dict`）来记录当前子数组里每个数出现了多少次。哈希表就像一本“词典”，键（key）是数字，值（value）是出现次数。遍历子数组时，把每个数字的计数加一，最后哈希表的键的数量就是不同整数的种类数。

**为什么暴力解一定对**  
因为我们没有遗漏任何可能的子数组：所有 `i`、`j` 组合都遍历了一遍。只要对每个子数组正确统计不同元素的种类数，计数自然是准确的。

**复杂度分析（大白话）**  
- **时间**：外层循环 `i` 要跑 `n` 次，内层循环 `j` 也最多跑 `n` 次，所以大约是 `n × n = n²` 次操作。每次我们都要在哈希表里加/减计数，平均是 O(1)。所以总时间是 **O(n²)**。可以把它想象成“在一个 n×n 的格子里逐格检查”。
- **空间**：我们需要一个哈希表来存当前子数组的计数，最坏情况下子数组里所有元素都不相同，哈希表会装 `n` 个键。所以空间是 **O(n)**。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def subarraysWithKDistinct_brute(nums: List[int], k: int) -> int:
    n = len(nums)
    ans = 0

    # 枚举左边界 i
    for i in range(n):
        freq = defaultdict(int)   # 哈希表：数字 -> 出现次数
        distinct = 0               # 当前子数组不同数字的个数

        # 枚举右边界 j（从 i 开始向右扩展）
        for j in range(i, n):
            if freq[nums[j]] == 0:   # 这个数字以前没有出现过
                distinct += 1
            freq[nums[j]] += 1

            # 检查是否恰好有 k 种不同的数字
            if distinct == k:
                ans += 1
            # 如果已经超过 k，后面的子数组只会更多，直接 break
            elif distinct > k:
                break

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  解释：我们用两层循环遍历所有子数组，最坏情况下会检查约 `n²/2` 个子数组，算起来就是平方级别的工作量。
- **空间复杂度**：`O(n)`  
  解释：哈希表在最坏情况下会存 `n` 个不同的数字，随子数组长度线性增长。

---

### 2. 最优解

#### 思路  

暴力解慢的根源在于 **每次都重新统计子数组的不同元素**，这导致了 `O(n²)` 的时间。我们希望能够 **在遍历数组的过程中，动态维护子数组的状态**，这样就能把时间降到线性级别。

**关键观察**  
- 统计「恰好有 k 种不同数字」的子数组，等价于  
  `（至多有 k 种不同数字的子数组数） - （至多有 k‑1 种不同数字的子数组数）`。  
  因为「至多 k」 包含了「恰好 k」 和「更少」两部分，减去「至多 k‑1」后，剩下的就是「恰好 k」。
- 「至多 K 种不同数字」可以用 **滑动窗口 + 哈希表** 在 O(n) 时间内求得。  
  滑动窗口的思想是：用两个指针 `left`、`right` 表示当前窗口 `[left, right]`，我们把 `right` 逐步向右移动，把新元素加入窗口；如果窗口里不同数字的种类数超过 K，就把 `left` 向右收缩，直到种类数 ≤ K。

**滑动窗口的细节**  
1. 用 `cnt`（字典）记录窗口内每个数字出现的次数。  
2. 用 `unique` 记录当前窗口里不同数字的个数。  
3. 每次把 `right` 向右扩展时，更新 `cnt` 与 `unique`。  
4. 当 `unique > K` 时，循环收缩左边界 `left`，同时在 `cnt` 中减去对应数字的计数，若计数降到 0，则 `unique` 减 1。  
5. 此时窗口 `[left, right]` 是 **以 `right` 为右端点的所有满足「至多 K」的子数组**，数量为 `right - left + 1`（因为左边界可以在 `left … right` 任意位置）。把这个数量累加到答案中。

**整体算法**  
- 定义函数 `atMost(K)`，返回「至多 K 种不同数字」的子数组总数。  
- 结果 = `atMost(k) - atMost(k-1)`。

**为什么 O(n) 能做到**  
每个元素最多会被 `right` 指针加入窗口一次，又最多被 `left` 指针移出窗口一次。所有的加入、删除、计数更新操作都是 O(1)。所以整体遍历是线性时间。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def subarraysWithKDistinct(nums: List[int], k: int) -> int:
    """
    返回恰好包含 k 种不同整数的子数组个数。
    思路：利用「至多 K」-「至多 K-1」的差值。
    """
    def atMost(K: int) -> int:
        if K == 0:          # 至多 0 种不同数字的子数组只能是空的，计数为 0
            return 0
        cnt = defaultdict(int)   # 窗口内每个数字的出现次数
        left = 0
        unique = 0                # 窗口中不同数字的个数
        res = 0

        for right, x in enumerate(nums):
            # 把 nums[right] 加入窗口
            if cnt[x] == 0:       # 之前没有出现过，这里第一次出现
                unique += 1
            cnt[x] += 1

            # 若窗口里不同数字超过 K，就收缩左边界
            while unique > K:
                y = nums[left]
                cnt[y] -= 1
                if cnt[y] == 0:   # 这个数字完全离开窗口
                    unique -= 1
                left += 1

            # 此时窗口 [left, right] 满足「至多 K」,
            # 以 right 为右端点的合法子数组数 = 窗口长度
            res += right - left + 1

        return res

    # 恰好 k = 至多 k - 至多 (k-1)
    return atMost(k) - atMost(k - 1)
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  解释：`right` 指针遍历一次数组，`left` 指针最多也只会向右移动 `n` 步。所有哈希表的增删查都是常数时间，所以整体是线性时间。
- **空间复杂度**：`O(min(n, K))`（实际写作 `O(n)`）  
  解释：哈希表只会保存当前窗口里出现的数字。窗口最多包含 `K`（或 `K-1`）种不同数字，最坏情况下 `K` 可能等于 `n`，所以空间上限是 `O(n)`。

---

## 心得

- **核心技巧**：将「恰好 K」转化为「至多 K」减「至多 K‑1」的差值，再使用滑动窗口统计「至多 K」的子数组数。
- **适用场景**：  
  1. “子数组中至多/恰好 K 个不同元素” 类题目（如 LeetCode 340、992）。  
  2. “子数组满足某种计数上限” 的问题（如最长子数组满足和 ≤ K）。  
  3. “窗口内出现次数限制”的滑动窗口变形（如最长子串不含重复字符）。
- **一句话总结**：**把“恰好”拆成两次“至多”，再用滑动窗口一次遍历搞定。**

---

## 反思

- **第一反应**：立刻想到枚举所有子数组，写双层循环检查不同元素——这就是暴力解。
- **最容易踩的坑**  
  - 忘记在窗口收缩时把对应数字的计数减到 0 并同步更新 `unique`。  
  - `atMost(0)` 的边界要单独处理，否则会出现无限循环。  
  - 对于大输入，暴力解会超时，需要及时转向滑动窗口思路。
- **下次遇到同类题**：**先问自己“能否把‘恰好’转化为‘至多’的差值？”** 如果能，就立刻构造 `atMost` 的滑动窗口；如果不能，再考虑其他高级技巧（如前缀和、单调队列）。