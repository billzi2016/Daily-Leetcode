# #2261. **K 可整除元素子数组** / K Divisible Elements Subarrays

> 难度：中等 · 标签：Array、Hash Table、Trie、Rolling Hash、Hash Function、Enumeration · [LeetCode 链接](https://leetcode.com/problems/k-divisible-elements-subarrays/)

---

## 题目（英文原版）

**Description**

Given an integer array nums and two integers k and p, return the number of distinct subarrays, which have at most k elements that are divisible by p.
Two arrays nums1 and nums2 are said to be distinct if:
A subarray is defined as a non-empty contiguous sequence of elements in an array.
Follow up:
Can you solve this problem in O(n2) time complexity?

**Examples**

**Example 1:**

```
Input: nums = [2,3,3,2,2], k = 2, p = 2
Output: 11
Explanation:
The elements at indices 0, 3, and 4 are divisible by p = 2.
The 11 distinct subarrays which have at most k = 2 elements divisible by 2 are:
[2], [2,3], [2,3,3], [2,3,3,2], [3], [3,3], [3,3,2], [3,3,2,2], [3,2], [3,2,2], and [2,2].
Note that the subarrays [2] and [3] occur more than once in nums, but they should each be counted only once.
The subarray [2,3,3,2,2] should not be counted because it has 3 elements that are divisible by 2.
```

**Example 2:**

```
Input: nums = [1,2,3,4], k = 4, p = 1
Output: 10
Explanation:
All element of nums are divisible by p = 1.
Also, every subarray of nums will have at most 4 elements that are divisible by 1.
Since all subarrays are distinct, the total number of subarrays satisfying all the constraints is 10.
```

**Constraints**

- 1 <= nums.length <= 200
- 1 <= nums[i], p <= 200
- 1 <= k <= nums.length

---

## 题目（中文翻译）

给定一个整数数组 `nums` 与两个整数 `k`、`p`，返回满足「至多有 `k` 个元素能被 `p` 整除」的不同子数组（subarray）的数量。

两个数组 `nums1` 与 `nums2` 被认为是 **不同的**，当且仅当它们的元素序列不完全相同。  
子数组（subarray）被定义为数组中 **非空的连续** 元素序列。

---

### 示例 1
**输入**  
`nums = [2,3,3,2,2]`, `k = 2`, `p = 2`

**输出**  
`11`

**解释**  
下标 0、3、4 处的元素能够被 `p = 2` 整除。  
满足「至多有 `k = 2` 个元素能被 2 整除」的 11 个不同子数组如下：

```
[2], [2,3], [2,3,3], [2,3,3,2],
[3], [3,3], [3,3,2], [3,3,2,2],
[3,2], [3,2,2], [2,2]
```

注意，子数组 `[2]` 与 `[3]` 在原数组中出现了多次，但它们只算作 **一次**。

---

### 示例 2
**输入**  
`nums = [1,2,3,4]`, `k = 4`, `p = 1`

**输出**  
`10`

**解释**  
所有元素均能被 `p = 1` 整除。由于每个子数组中至多有 4 个可被 1 整除的元素，而数组长度本身就是 4，**所有子数组** 都满足条件。数组的所有子数组一共 10 个，且全部不同。

---

### 约束条件
- `1 <= nums.length <= 200`
- `1 <= nums[i], p <= 200`
- `1 <= k <= nums.length`

---

### 进阶
能否在 **O(n²)** 时间复杂度内解决本题？

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把 **所有** 子数组都枚举出来，然后逐个检查：

1. 子数组是连续的非空序列。  
   - 用两个指针 `i`（左端）和 `j`（右端）来表示子数组 `nums[i…j]`，就像我们在走路时左脚踩在位置 `i`，右脚踩在位置 `j`，两脚之间的路段就是子数组。  
2. 统计子数组里 **能被 `p` 整除的元素个数** 是否 ≤ `k`。  
   - 这一步相当于在子数组里找“特殊的石子”（能被 `p` 整除的数），数一数它们有多少颗。  
3. 为了避免重复计数，需要把已经出现过的子数组“记下来”。  
   - **哈希表**（Python 的 `set`）就像一本“字典”，`key` 是子数组的“内容”，`value` 只需要存在与否。这里我们把子数组直接转成 **元组** `(nums[i], nums[i+1], …, nums[j])`，元组可以直接作为字典的键，就像查字典时，用词（`key`）去找对应的页码（`value`）。

**为什么能得到正确答案**  
- 我们遍历了所有可能的 `[i, j]`，所以不会漏掉任何合法子数组。  
- 每次只在满足 “可被 `p` 整除的元素 ≤ `k`” 时才把子数组加入集合，确保计数的子数组全部符合要求。  
- 集合天然去重，重复出现的子数组只会留下一个拷贝。

**复杂度分析（大白话）**  

| 步骤 | 说明 | 复杂度 |
|------|------|--------|
| 枚举所有起点 `i` | `i` 从 `0` 到 `n‑1`，就像我们把左脚一步步往右移动 | `O(n)` |
| 对每个 `i` 枚举所有终点 `j` | 对每个左端，右端可以往右走到数组末尾，最多 `n` 步 | `O(n)`（每个 `i`） |
| 检查可整除元素个数 | 需要遍历子数组里的每个元素，最坏情况子数组长度是 `n` | `O(n)`（每个子数组） |
| 把子数组转成元组并加入集合 | 把子数组复制成新对象，长度同子数组长度 | `O(n)`（每个子数组） |

把它们乘起来就是 **`O(n³)`**。  
- `n` ≤ 200 时，`200³ = 8,000,000`，在 Python 里还能跑完，但已经不是我们想要的“优雅”解法。  
- 空间方面，集合最坏会保存所有不同子数组，数量上限是 `n·(n+1)/2`（所有子数组），即 `O(n²)`。

#### 代码（Python）

```python
from typing import List

def countDistinctSubarrays_bruteforce(nums: List[int], k: int, p: int) -> int:
    n = len(nums)
    seen = set()                     # 用来去重的哈希表
    for i in range(n):               # 左端 i
        for j in range(i, n):        # 右端 j
            # 统计子数组 nums[i..j] 中能被 p 整除的元素个数
            cnt = 0
            for t in range(i, j + 1):
                if nums[t] % p == 0:
                    cnt += 1
            if cnt <= k:              # 合法子数组
                # 把子数组转成元组，加入集合（自动去重）
                sub = tuple(nums[i:j + 1])
                seen.add(sub)
    return len(seen)
```

#### 复杂度

- **时间复杂度**：`O(n³)`  
  - “立方”意味着如果数组长度翻倍，运行时间会增加约 8 倍。对 200 长度的数组来说还能接受，但不是最优的。  
- **空间复杂度**：`O(n²)`  
  - 最坏情况下所有子数组都不同，需要把它们全部放进集合。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **重复遍历同一个子数组**（统计可整除元素、拷贝成元组）以及 **每次都要 O(长度) 的额外工作**。我们可以把这两件事“边走边算”，让每个子数组只 **被访问一次**，从而把时间降到 `O(n²)`。

优化思路分两步：

1. **滑动窗口计数**  
   - 当我们固定左端 `i`，右端 `j` 逐渐向右扩展时，子数组 `nums[i…j]` 只会比前一次多一个元素 `nums[j]`。  
   - 因此我们可以维护一个变量 `cntDiv`，记录当前窗口里可被 `p` 整除的元素个数。每次加入 `nums[j]` 时，只需检查它是否能被 `p` 整除，然后 `cntDiv += 1`（或保持不变）。  
   - 当 `cntDiv` 超过 `k` 时，说明再往右扩展已经不合法，直接 **break**，因为后面的子数组（更长）肯定也不合法。

2. **滚动哈希唯一标记子数组**  
   - 为了快速去重，我们不再把子数组复制成元组，而是用 **滚动哈希**（Rolling Hash）把子数组映射成一个整数。  
   - 把子数组看成一个“数字串”：`hash = (hash * base + nums[j]) % mod`，每加入一个新元素就像在左边加一位。  
   - 为防止不同子数组产生相同哈希（冲突），我们把 **哈希值 + 长度** 作为键放进集合。冲突概率极低，实际使用时可以再加一层双模数（这里用单个大质数已经足够）。  

这样，枚举所有 `(i, j)` 只需要 `O(1)` 的额外工作，整体时间降到 `O(n²)`，空间仍是 `O(n²)`（存所有不同哈希）。

**核心概念解释**  

- **双指针 / 滑动窗口**：想象你在跑步，左脚固定在起点，右脚一步步往前跑。每跑一步，就检查新踩到的石头（`nums[j]`）是否特殊（能被 `p` 整除），并更新计数。只要计数 ≤ `k`，就继续跑；一旦超过，就停下来，因为再往前跑只会让计数更大。  
- **滚动哈希**：把子数组看成一串字符，每个字符对应一个数字。把它们当作 **多项式**：`a0 * B^(len-1) + a1 * B^(len-2) + … + a_{len-1}`（`B` 是基数）。在模 `M`（大质数）下取余，得到一个“指纹”。每次在右端加一个新数字，只需要一次乘法和一次加法，就能得到新指纹，像在滚动的指纹机里不停盖上新印章。  

#### 代码（Python）

```python
from typing import List

def countDistinctSubarrays_opt(nums: List[int], k: int, p: int) -> int:
    n = len(nums)
    MOD = 10 ** 9 + 7          # 大质数，防止哈希冲突
    BASE = 911                 # 任意大于最大元素的数，这里随便选一个

    distinct = set()           # 存 (hash, length) 去重

    for i in range(n):         # 左端固定
        cnt_div = 0            # 当前窗口里能被 p 整除的个数
        cur_hash = 0           # 滚动哈希值
        length = 0             # 窗口长度，方便构造唯一键

        for j in range(i, n):  # 右端向右扩展
            if nums[j] % p == 0:
                cnt_div += 1
            if cnt_div > k:    # 已经不合法，后面的更长子数组也不合法
                break

            # 更新滚动哈希：hash = hash * BASE + nums[j] (mod MOD)
            cur_hash = (cur_hash * BASE + nums[j]) % MOD
            length += 1

            # 把 (hash, length) 放进集合，自动去重
            distinct.add((cur_hash, length))

    return len(distinct)
```

> **代码要点注释**  
> - `cnt_div` 只在 **O(1)** 时间内更新，避免了对每个子数组重新遍历计数。  
> - `cur_hash` 同样在 **O(1)** 时间内更新，实现“滚动”。  
> - `break` 把不合法的右端直接剪掉，省掉大量无用的遍历。  

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 两层循环最多遍历 `n·(n+1)/2` 次子数组，每次只做常数次运算（整除检查、哈希更新、集合插入）。  
  - 与暴力解相比，省掉了内部的 `O(length)` 计数与拷贝，速度提升约 `n` 倍（对 200 长度的数组，从约 8 百万次降到 20 千次左右）。  
- **空间复杂度**：`O(n²)`  
  - 最坏情况下所有子数组都不同，需要把它们的哈希+长度存进集合。每个键占用常数空间，整体仍是二次级别。  

---

## 心得

- **核心技巧**：**滑动窗口 + 滚动哈希**。  
  - 滑动窗口帮助我们在枚举子数组时 **实时维护** 约束（可被 `p` 整除的元素个数），把 `O(length)` 的检查降到 `O(1)`。  
  - 滚动哈希把子数组的“内容”压缩成一个整数，使 **去重** 只需 `O(1)` 插入集合，避免了复制整个子数组的高开销。  

- **适用的题型**（类似思路）  
  1. “子数组/子串满足某种计数约束” 如 **最长子数组/子串且至多 `k` 个不同字符**（LeetCode 340）。  
  2. “统计不同子数组/子串” 需要去重的题目，如 **Distinct Substrings of a String**、**Number of Different Subarrays**（LeetCode 2261）。  
  3. “子数组满足数值范围约束” 并需要快速唯一标记的，如 **Count Subarrays With Median K**（滑动窗口 + 前缀哈希）  

- **一句话总结解题钥匙**  
  > 用滑动窗口把“是否合法”检查变成常数时间，用滚动哈希把“子数组长得像不一样”压成指纹，这两者结合即可在 `O(n²)` 内完整统计。

---

## 反思

- **第一反应**：直接把所有子数组列举出来，用 `set` 去重。  
- **最容易踩的坑**  
  - **重复计数**：忘记去重会把同样的子数组算多次。  
  - **时间爆炸**：在每次检查子数组时重新遍历子数组本身，导致 `O(n³)`。  
  - **哈希冲突**：只用哈希值而不记录长度时，可能出现不同长度子数组产生相同哈希的极端情况（虽然概率低）。  
  - **边界条件**：`k` 可能等于数组长度，或者 `p = 1`（所有元素都可被整除），这时所有子数组都合法，需要确保循环不提前 `break`。  

- **下次遇到同类题**，第一步应该问自己：  
  1. “我能否在枚举子数组的过程中 **增量更新** 约束条件（计数、和、最大值等）？”  
  2. “是否需要 **快速唯一标记** 子数组/子串？如果需要，滚动哈希或前缀哈希是常用工具”。  

通过这两步思考，往往能立刻把 `O(n³)` 的暴力方案压到 `O(n²)`，甚至更低。