# #2547. 最小划分数组成本 / Minimum Cost to Split an Array

> 难度：困难 · 标签：Array、Hash Table、Dynamic Programming、Counting · [LeetCode 链接](https://leetcode.com/problems/minimum-cost-to-split-an-array/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and an integer k.
Split the array into some number of non-empty subarrays. The cost of a split is the sum of the importance value of each subarray in the split.
Let trimmed(subarray) be the version of the subarray where all numbers which appear only once are removed.
The importance value of a subarray is k + trimmed(subarray).length.
Return the minimum possible cost of a split of nums.
A subarray is a contiguous non-empty sequence of elements within an array.

**Examples**

**Example 1:**

```
Input: nums = [1,2,1,2,1,3,3], k = 2
Output: 8
Explanation: We split nums to have two subarrays: [1,2], [1,2,1,3,3].
The importance value of [1,2] is 2 + (0) = 2.
The importance value of [1,2,1,3,3] is 2 + (2 + 2) = 6.
The cost of the split is 2 + 6 = 8. It can be shown that this is the minimum possible cost among all the possible splits.
```

**Example 2:**

```
Input: nums = [1,2,1,2,1], k = 2
Output: 6
Explanation: We split nums to have two subarrays: [1,2], [1,2,1].
The importance value of [1,2] is 2 + (0) = 2.
The importance value of [1,2,1] is 2 + (2) = 4.
The cost of the split is 2 + 4 = 6. It can be shown that this is the minimum possible cost among all the possible splits.
```

**Example 3:**

```
Input: nums = [1,2,1,2,1], k = 5
Output: 10
Explanation: We split nums to have one subarray: [1,2,1,2,1].
The importance value of [1,2,1,2,1] is 5 + (3 + 2) = 10.
The cost of the split is 10. It can be shown that this is the minimum possible cost among all the possible splits.
```

**Constraints**

- 1 <= nums.length <= 1000
- 0 <= nums[i] < nums.length
- 1 <= k <= 109

---

## 题目（中文翻译）

给定一个整数数组 `nums` 和一个整数 `k`。  
将数组划分为若干个非空子数组（subarray）。一次划分的 **成本**（cost）等于该划分中每个子数组的 **重要性值**（importance value）之和。

设 `trimmed(subarray)` 为子数组去除所有只出现一次的数字后的版本。  
子数组的 **重要性值** 为 `k + trimmed(subarray).length`。  

返回对 `nums` 的划分可能得到的最小成本。

> **子数组（subarray）** 是数组中连续的、非空的元素序列。

---

### 示例

#### 示例 1
**输入**  
`nums = [1,2,1,2,1,3,3], k = 2`

**输出**  
`8`

**解释**  
我们将 `nums` 划分为两个子数组：`[1,2]`、`[1,2,1,3,3]`。  
- 子数组 `[1,2]` 的重要性值为 `2 + (0) = 2`。  
- 子数组 `[1,2,1,3,3]` 的重要性值为 `2 + (2 + 2) = 6`（`trimmed` 后剩下两个 `1` 和两个 `3`）。  
划分的成本为 `2 + 6 = 8`。可以证明这已经是所有可能划分中的最小成本。

#### 示例 2
**输入**  
`nums = [1,2,1,2,1], k = 2`

**输出**  
`6`

**解释**  
我们将 `nums` 划分为两个子数组：`[1,2]`、`[1,2,1]`。  
- 子数组 `[1,2]` 的重要性值为 `2 + (0) = 2`。  
- 子数组 `[1,2,1]` 的重要性值为 `2 + (2) = 4`（`trimmed` 后剩下两个 `1`）。  
划分的成本为 `2 + 4 = 6`，已是最小可能成本。

#### 示例 3
**输入**  
`nums = [1,2,1,2,1], k = 5`

**输出**  
`10`

**解释**  
我们将 `nums` 整体作为一个子数组：`[1,2,1,2,1]`。  
- 该子数组的重要性值为 `5 + (3 + 2) = 10`（`trimmed` 后剩下三个 `1` 和两个 `2`）。  
划分的成本即为 `10`，也是最小可能成本。

---

### 约束条件

- `1 <= nums.length <= 1000`
- `0 <= nums[i] < nums.length`
- `1 <= k <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可能的切分方式都枚举一遍**，然后计算每一种切分的费用，取最小值。  
要实现这一点，我们可以：

1. 用两层循环枚举子数组的左端点 `l` 与右端点 `r`（`0 ≤ l ≤ r < n`），得到所有连续子数组 `nums[l..r]`。  
2. 再用一个外层循环把数组从左到右切成若干段，记录每段的费用之和，取最小。

**数据结构**  
- 为了求子数组的 “重要度”，我们需要统计每个数在子数组中出现的次数。最自然的方式是 **哈希表**（在 Python 中用 `defaultdict(int)`），它的作用类似于一本**查字典**：  
  - **key** 是数字本身，  
  - **value** 是这个数字在当前子数组里出现了几次。  

  当我们遍历子数组时，遇到一个新数字，就把它的计数加 1；如果计数从 1 变成 2，说明它从“只出现一次”变成了“出现两次”，这时它的出现次数要全部计入 **trimmed** 部分；如果计数已经 ≥2，再出现一次，只需要再加 1（因为 trimmed 部分已经把它的前两次算进来了）。

**正确性**  
枚举所有切分方式必然能覆盖最优解，因为没有任何剪枝或假设。只要我们对每个子数组正确计算 **importance = k + trimmed length**，累加所有子数组的费用即可得到该切分的总成本。

**复杂度**  
- 枚举所有子数组需要 `O(n^2)`（两个循环）。  
- 对每个子数组重新统计频率需要 `O(n)`（遍历子数组本身），于是总时间是 `O(n^3)`。  
  - **大白话**：如果 `n = 1000`，`n³ = 10⁹`，在电脑里跑几分钟甚至几小时都可能超时。  
- 额外使用的哈希表大小最多是子数组中不同数字的种类数，最多 `O(n)`，所以空间是 `O(n)`。

#### 代码（Python）

```python
from collections import defaultdict
from math import inf

def minCost_bruteforce(nums, k):
    n = len(nums)
    # dp[i] 表示划分前 i 个元素（0..i-1）的最小费用，dp[0]=0 表示空前缀
    dp = [inf] * (n + 1)
    dp[0] = 0

    # 枚举子数组的右端点 r（1-indexed 方便写 dp）
    for r in range(1, n + 1):
        freq = defaultdict(int)          # 统计 nums[l..r-1] 的频率
        trimmed_len = 0                   # 当前子数组的 trimmed 长度
        # 从右往左尝试所有可能的左端点 l
        for l in range(r - 1, -1, -1):
            x = nums[l]
            freq[x] += 1
            if freq[x] == 2:              # 第一次出现两次，之前的 1 次不计，后面 2 次全部计入 trimmed
                trimmed_len += 2
            elif freq[x] > 2:             # 已经出现 ≥2 次，再出现一次只多加 1
                trimmed_len += 1

            importance = k + trimmed_len
            dp[r] = min(dp[r], dp[l] + importance)   # dp[l] 为左侧已划分好的最小费用
    return dp[n]

# 示例
print(minCost_bruteforce([1,2,1,2,1,3,3], 2))   # 8
```

> 代码里每一行都有中文注释，帮助你快速定位关键操作。

#### 复杂度

- **时间复杂度**：`O(n³)`  
  - 解释：外层 `r` 循环 `n` 次，内层 `l` 循环最多 `n` 次，而每次更新 `freq`、`trimmed_len` 只花 `O(1)`，但我们在最外层还有一次 `dp` 的遍历（这里已经算进 `O(n²)`），整体是立方级别。
- **空间复杂度**：`O(n)`  
  - 解释：`dp` 数组长度为 `n+1`，哈希表最多保存 `n` 个不同的数字计数。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于每次计算子数组 `nums[l..r]` 的 `importance` 时，都要重新遍历子数组来统计频率。其实，当我们把左端点 `l` **从右向左**移动时，子数组只会 **加入一个新元素**，所以可以在 **常数时间**内更新 `importance`。

**关键观察**  
设 `imp(l, r)` 为子数组 `nums[l..r]` 的重要度（不含 `k`，即 trimmed 长度）。当我们把左端点从 `l` 向左扩展到 `l-1`，只会加入一个元素 `x = nums[l-1]`，此时 `imp(l-1, r)` 的变化只有三种可能：

| `x` 在 `nums[l..r]` 中的出现次数 `cnt` | 变化 |
|---|---|
| `cnt = 0`（之前根本没有） | `imp` **不变**（`x` 只出现一次，被 trimmed 删除） |
| `cnt = 1`（之前出现一次） | `imp` **+2**（现在出现两次，两个都算进 trimmed） |
| `cnt ≥ 2`（之前已经出现 ≥2 次） | `imp` **+1**（再多出现一次，只多算 1） |

只要我们在遍历 `l` 时维护一个 **频率表**（哈希表），并记录当前的 `trimmed_len`，就能 **O(1)** 更新 `imp`。这样，对每个右端点 `r`，我们只需要 **一次** `O(n)` 的循环就能得到所有左端点对应的 `importance`，而不是 `O(n²)`。

**动态规划**  
仍然使用 `dp[i]` 表示前 `i`（0…i‑1）个元素的最小划分费用。对每个右端点 `r`（1‑based），我们：

1. 初始化一个空频率表 `freq`、`trimmed = 0`。  
2. 从 `l = r-1` 向左遍历到 `0`，逐步把 `nums[l]` 加入子数组 `nums[l..r-1]`，实时更新 `trimmed`。  
3. 计算 `importance = k + trimmed`，并尝试转移 `dp[r] = min(dp[r], dp[l] + importance)`。

整体时间复杂度为 `O(n²)`（外层 `r` 循环 `n` 次，内层 `l` 循环最多 `n` 次），空间仍是 `O(n)`。

**为什么 O(n²) 已经足够？**  
题目限制 `n ≤ 1000`，`n² = 10⁶`，在 Python 中毫秒级即可完成，远低于时间限制。

#### 代码（Python）

```python
from collections import defaultdict
from math import inf

def minCost(nums, k):
    """
    dp[i] : 前 i 个元素（0 .. i-1）的最小划分费用
    """
    n = len(nums)
    dp = [inf] * (n + 1)
    dp[0] = 0                     # 空数组的费用为 0

    # 枚举子数组的右端点 r（1-indexed，方便对应 dp）
    for r in range(1, n + 1):
        freq = defaultdict(int)   # 记录当前子数组 nums[l..r-1] 中每个数字的出现次数
        trimmed = 0                # 当前子数组的 trimmed 长度（不含 k）

        # 从右向左尝试所有左端点 l
        for l in range(r - 1, -1, -1):
            x = nums[l]
            freq[x] += 1

            # 根据出现次数的不同，更新 trimmed
            if freq[x] == 2:          # 由 1 次变成 2 次，两个都计入 trimmed
                trimmed += 2
            elif freq[x] > 2:         # 已经 ≥2 次，再来一次只多加 1
                trimmed += 1
            # freq[x] == 1 时不做任何操作（只出现一次被 trimmed 删除）

            importance = k + trimmed          # 当前子数组的费用
            # dp[l] 已经是前 l 个元素的最优费用，尝试把它和当前子数组拼在一起
            dp[r] = min(dp[r], dp[l] + importance)

    return dp[n]

# ------------------- 测试 -------------------
print(minCost([1,2,1,2,1,3,3], 2))   # 8
print(minCost([1,2,1,2,1], 2))       # 6
print(minCost([1,2,1,2,1], 5))       # 10
```

> 代码中的每一步都有中文注释，帮助你跟踪 **频率表**、**trimmed 长度** 与 **dp 转移** 的关系。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 解释：外层遍历右端点 `r` `n` 次，内层遍历左端点 `l` 最多 `n` 次，每次只做 `O(1)` 的哈希表更新与 `dp` 取最小操作。相比暴力的 `O(n³)`，快了一个数量级，实际运行不到几毫秒。
- **空间复杂度**：`O(n)`  
  - 解释：`dp` 长度 `n+1`，以及每次循环中最多存 `n` 个不同数字的频率表。

---

## 心得

- **核心技巧**：**从右向左维护子数组的频率表，利用增量更新**（即“加入一个元素只改动常数步”）把原本需要 `O(n)` 重新统计的过程降到 `O(1)`。  
- **适用的题型**  
  1. **分割数组求最小/最大费用**（如 “分割数组的最大和”）。  
  2. **子数组代价依赖出现次数**（如 “最小代价划分，使每段内相同元素出现次数满足条件”。）  
  3. **需要在所有左端点上快速计算同类代价**（如 “划分数组使每段的不同元素个数最小化”。）  
- **一句话总结解题钥匙**：  
  > “把子数组的代价拆成增量形式，左端点往左移动时只更新一次哈希表，就能在 `O(1)` 内得到新的代价”。  

---

## 反思

- **第一反应**：看到“把数组切成若干子数组”立刻想到 **动态规划**，因为这类“划分最优”问题常用 `dp[i] = min(dp[j] + cost(j,i))`。  
- **最容易踩的坑**  
  1. **频率更新错误**：忘记在 `freq[x] == 2` 时加 `2`（因为两个元素都要计入 trimmed），导致结果偏小。  
  2. **边界条件**：`dp[0] = 0` 必须初始化，否则会出现“未划分前的费用为无穷”。  
  3. **整数溢出**：在其他语言里 `k` 可达 `10⁹`，累加时要使用足够大的类型（Python 自动大整数）。  
- **下次遇到同类题的第一步**：  
  > “先写出 DP 状态转移公式，然后思考：`cost(j,i)` 是否可以在 **滑动窗口**/**增量** 的方式下快速得到”。如果可以，就把 O(n³) 的暴力转化为 O(n²)（或更快）的实现。