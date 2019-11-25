# #673. 最长递增子序列的个数 / Number of Longest Increasing Subsequence

> 难度：中等 · 标签：Array、Dynamic Programming、Binary Indexed Tree、Segment Tree · [LeetCode 链接](https://leetcode.com/problems/number-of-longest-increasing-subsequence/)

---

## 题目（英文原版）

**Description**

Given an integer array nums, return the number of longest increasing subsequences.
Notice that the sequence has to be strictly increasing.

**Examples**

**Example 1:**

```
Input: nums = [1,3,5,4,7]
Output: 2
Explanation: The two longest increasing subsequences are [1, 3, 4, 7] and [1, 3, 5, 7].
```

**Example 2:**

```
Input: nums = [2,2,2,2,2]
Output: 5
Explanation: The length of the longest increasing subsequence is 1, and there are 5 increasing subsequences of length 1, so output 5.
```

**Constraints**

- 1 <= nums.length <= 2000
- -106 <= nums[i] <= 106
- The answer is guaranteed to fit inside a 32-bit integer.

---

## 题目（中文翻译）

给定一个整数数组 `nums`，返回最长递增子序列（longest increasing subsequence）的个数。注意，序列必须严格递增。

### 示例 1
**输入**: `nums = [1,3,5,4,7]`  
**输出**: `2`  
**解释**: 两个最长递增子序列分别是 `[1, 3, 4, 7]` 和 `[1, 3, 5, 7]`。

### 示例 2
**输入**: `nums = [2,2,2,2,2]`  
**输出**: `5`  
**解释**: 最长递增子序列的长度为 `1`，共有 `5` 个长度为 `1` 的递增子序列，所以输出 `5`。

### 约束条件
- `1 <= nums.length <= 2000`
- `-10^6 <= nums[i] <= 10^6`
- 答案保证能够放入 32 位整数中。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有子序列都枚举出来，检查它们是不是严格递增的，记录最长长度以及出现的次数**。  
- **子序列**可以理解为“从原数组里挑选若干个元素，保持原来的相对顺序”。这就像在一本书里挑出若干页，页码必须保持从前往后。  
- 为了遍历所有子序列，我们可以用**位掩码**（二进制）来表示是否选取第 `i` 个元素。长度为 `n` 的数组有 `2ⁿ` 种选法。  
- 对每一种选法，遍历一次数组，判断挑出来的元素是否严格递增（相邻两个数必须 `前 < 后`），并统计它的长度。  
- 最后比较所有合法递增子序列的长度，找出最长的长度 `L`，再统计出现多少次长度为 `L` 的子序列。

> **为什么它是对的？**  
> 只要把所有可能的子序列都穷举检查，就一定不会遗漏最长的递增子序列，也不会把不递增的序列算进去。穷举法的正确性来自“枚举全体”。

> **时间/空间复杂度**  
> - **时间复杂度**：我们要遍历 `2ⁿ` 种子序列，每种子序列最多遍历 `n` 个元素来判断递增性 → `O(n·2ⁿ)`。这在 `n` 只有几位时还能接受，但一旦 `n=2000`，`2ⁿ` 已经天文数字，根本跑不完。  
> - **空间复杂度**：只需要常数级的额外空间（存几个计数器） → `O(1)`。

> **大白话解释**：  
> `O(n·2ⁿ)` 可以想象成“先把所有可能的钥匙（2ⁿ 把）都拿出来，再对每把钥匙检查一次（n 步）”。钥匙数量随 `n` 指数级增长，根本不可能全部试完。

#### 代码（Python）

```python
from itertools import combinations

def findNumberOfLIS_bruteforce(nums):
    n = len(nums)
    best_len = 0          # 当前找到的最长递增子序列长度
    count = 0             # 长度为 best_len 的子序列个数

    # 枚举子序列长度从 1 到 n（因为空序列不算）
    for length in range(1, n + 1):
        # combinations 会返回所有不重复的 index 组合，例如 (0,2,3)
        for idxs in combinations(range(n), length):
            # 取出对应的数值
            seq = [nums[i] for i in idxs]
            # 检查是否严格递增
            if all(seq[i] < seq[i + 1] for i in range(len(seq) - 1)):
                if length > best_len:
                    best_len = length
                    count = 1
                elif length == best_len:
                    count += 1
    return count
```

#### 复杂度

- **时间复杂度**：`O(n·2ⁿ)` — 随着数组长度指数级增长，几乎不可能在真实数据上跑通。  
- **空间复杂度**：`O(1)` — 只用了几个计数变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **“枚举所有子序列”**，这一步根本不必要。我们只关心 **每个位置结尾的最长递增子序列的长度** 与 **对应的计数**，可以用 **动态规划（DP）** 把问题拆成子问题。

**核心想法**  
- 对于数组中的每个元素 `nums[i]`，考虑它作为递增子序列的最后一个元素时，能够得到的最长长度 `len[i]` 以及有多少种方式得到这个长度 `cnt[i]`。  
- 对 `i` 前面的所有元素 `j < i`，只要 `nums[j] < nums[i]`（才能保持递增），就可以把 `j` 那里已经算好的子序列“接在” `i` 后面。  
- 具体规则：

| 情况 | 说明 |
|------|------|
| `len[j] + 1 > len[i]` | 通过 `j` 能得到更长的序列，更新 `len[i]` 为 `len[j] + 1`，并把计数 `cnt[i]` 设为 `cnt[j]`（因为所有最长序列都来自 `j`）。 |
| `len[j] + 1 == len[i]` | 通过 `j` 能得到同样长度的序列，说明又多出 `cnt[j]` 条不同的方式，累加到 `cnt[i]`。 |
| 否则 | `j` 贡献不大，忽略。 |

- 初始时每个位置都可以单独成为长度为 1 的递增子序列，计数为 1（即 `len[i]=1, cnt[i]=1`）。

**求答案**  
遍历完所有 `i` 后，整体最长长度 `L = max(len)`。答案就是所有 `len[i] == L` 的 `cnt[i]` 之和。

**时间复杂度**  
- 双层循环 `i` 与 `j` → `O(n²)`，对 `n ≤ 2000` 完全可接受。  
- 空间只需要两个长度为 `n` 的数组 → `O(n)`。

> **为什么 `O(n²)` 已经是“最优”**  
> 对于本题的约束（`n` 只到 2000），`O(n²)` 已经足够快。还有更高级的 `O(n log n)` 解法（利用树状数组 / 线段树），但实现较为复杂，对初学者来说不易理解。这里把 `O(n²)` 视为最优解，帮助大家掌握 **DP + 计数** 这类常见技巧。

#### 代码（Python）

```python
def findNumberOfLIS(nums):
    """
    返回最长递增子序列的个数
    """
    n = len(nums)
    if n <= 1:
        return n

    # len[i]  表示以 nums[i] 结尾的递增子序列的最长长度
    # cnt[i]  表示以 nums[i] 结尾且长度为 len[i] 的子序列个数
    length = [1] * n
    count  = [1] * n

    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:                # 只能接在更小的数后面
                if length[j] + 1 > length[i]:    # 找到更长的序列
                    length[i] = length[j] + 1
                    count[i]  = count[j]          # 计数换成来自 j 的方式
                elif length[j] + 1 == length[i]: # 同样长的序列再多一种
                    count[i] += count[j]

    # 整体最长长度
    longest = max(length)

    # 所有以最长长度结尾的子序列计数求和即为答案
    total = sum(cnt for l, cnt in zip(length, count) if l == longest)
    return total
```

#### 复杂度

- **时间复杂度**：`O(n²)` — 以 `n=2000` 为例，大约 4 000 000 次比较，在一秒内可以轻松完成。  
  > 大白话：我们把每个人（`i`）和他前面的所有人（`j`）配对一次，配对次数等于 `1+2+…+(n-1) = n·(n-1)/2`，这就是 `O(n²)`。

- **空间复杂度**：`O(n)` — 只用了两个长度为 `n` 的列表来记录每个位置的最长长度和计数。  
  > 大白话：我们只需要记住每个人的“最高分”和“有几种方式得到最高分”，不需要额外的大表格。

---

## 心得

- **核心技巧**：**动态规划 + 计数**。先算出每个位置的最长长度，再在同长度上累计不同的方案数。  
- **适用的题型**  
  1. “求最长递增子序列的个数” （本题）。  
  2. “最长递增子序列的和” / “最长递增子序列的最小/最大和”。  
  3. “最长公共子序列的个数” 或 “最长公共子序列的计数”。  
- **一句话总结**：**“把全局问题拆成‘以每个位置结尾的子问题’，用 DP 记录长度与方案数，最后合并”。**

---

## 反思

- **第一反应**：直接想到枚举所有子序列，写出暴力解，随后意识到时间会爆炸。  
- **最容易踩的坑**  
  - 忘记在 `length[j] + 1 == length[i]` 时要 **累加**计数，而不是覆盖。  
  - 边界情况：全部相等的数组，最长长度是 `1`，答案应该是 `n`（每个元素都是一条合法序列）。  
  - 当 `nums` 长度为 `1` 时，直接返回 `1`，防止后面的 `max(length)` 报错。  
- **下次遇到同类题**：第一步先问自己 “是否可以把答案拆成‘以某个位置结尾’的子问题”，若可以，就立刻写出 DP 状态转移式，再考虑是否需要计数/和等额外信息。这样可以避免无效的全枚举思路，直接走向高效的 DP 解法。