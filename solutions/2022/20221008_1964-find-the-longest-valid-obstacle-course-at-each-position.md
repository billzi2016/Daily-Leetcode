# #1964. 找到每个位置的最长有效障碍赛道 / Find the Longest Valid Obstacle Course at Each Position

> 难度：困难 · 标签：Array、Binary Search、Binary Indexed Tree · [LeetCode 链接](https://leetcode.com/problems/find-the-longest-valid-obstacle-course-at-each-position/)

---

## 题目（英文原版）

**Description**

You want to build some obstacle courses. You are given a 0-indexed integer array obstacles of length n, where obstacles[i] describes the height of the ith obstacle.
For every index i between 0 and n - 1 (inclusive), find the length of the longest obstacle course in obstacles such that:
Return an array ans of length n, where ans[i] is the length of the longest obstacle course for index i as described above.

**Examples**

**Example 1:**

```
Input: obstacles = [1,2,3,2]
Output: [1,2,3,3]
Explanation: The longest valid obstacle course at each position is:
- i = 0: [1], [1] has length 1.
- i = 1: [1,2], [1,2] has length 2.
- i = 2: [1,2,3], [1,2,3] has length 3.
- i = 3: [1,2,3,2], [1,2,2] has length 3.
```

**Example 2:**

```
Input: obstacles = [2,2,1]
Output: [1,2,1]
Explanation: The longest valid obstacle course at each position is:
- i = 0: [2], [2] has length 1.
- i = 1: [2,2], [2,2] has length 2.
- i = 2: [2,2,1], [1] has length 1.
```

**Example 3:**

```
Input: obstacles = [3,1,5,6,4,2]
Output: [1,1,2,3,2,2]
Explanation: The longest valid obstacle course at each position is:
- i = 0: [3], [3] has length 1.
- i = 1: [3,1], [1] has length 1.
- i = 2: [3,1,5], [3,5] has length 2. [1,5] is also valid.
- i = 3: [3,1,5,6], [3,5,6] has length 3. [1,5,6] is also valid.
- i = 4: [3,1,5,6,4], [3,4] has length 2. [1,4] is also valid.
- i = 5: [3,1,5,6,4,2], [1,2] has length 2.
```

**Constraints**

- n == obstacles.length
- 1 <= n <= 105
- 1 <= obstacles[i] <= 107

---

## 题目（中文翻译）

给定一个下标从 **0** 开始的整数数组 `obstacles`，长度为 `n`，其中 `obstacles[i]` 表示第 `i` 个障碍的高度。  
对于每个下标 `i`（`0 ≤ i ≤ n‑1`），求满足以下条件的 **障碍赛道（obstacle course）** 的最长长度：

- 赛道由若干个下标严格递增的障碍组成，且这些障碍的高度 **不下降**（即每个后续障碍的高度 **≥** 前一个障碍的高度）；
- 赛道的最后一个障碍必须是下标 `i` 处的障碍。

返回一个长度为 `n` 的数组 `ans`，其中 `ans[i]` 为上述条件下以下标 `i` 为结尾的最长障碍赛道的长度。

## 示例

### 示例 1
> **输入**：`obstacles = [1,2,3,2]`  
> **输出**：`[1,2,3,3]`  
> **解释**：每个位置的最长有效障碍赛道为  
> - `i = 0`：`[1]`，长度为 `1`。  
> - `i = 1`：`[1,2]`，长度为 `2`。  
> - `i = 2`：`[1,2,3]`，长度为 `3`。  
> - `i = 3`：`[1,2,2]`（从 `[1,2,3,2]` 中去掉 `3`），长度为 `3`。

### 示例 2
> **输入**：`obstacles = [2,2,1]`  
> **输出**：`[1,2,1]`  
> **解释**：每个位置的最长有效障碍赛道为  
> - `i = 0`：`[2]`，长度为 `1`。  
> - `i = 1`：`[2,2]`，长度为 `2`。  
> - `i = 2`：`[1]`（只能取自身），长度为 `1`。

### 示例 3
> **输入**：`obstacles = [3,1,5,6,4,2]`  
> **输出**：`[1,1,2,3,2,2]`  
> **解释**：每个位置的最长有效障碍赛道为  
> - `i = 0`：`[3]`，长度为 `1`。  
> - `i = 1`：`[1]`，长度为 `1`。  
> - `i = 2`：`[3,5]` 或 `[1,5]`，长度为 `2`。  
> - `i = 3`：`[3,5,6]` 或 `[1,5,6]`，长度为 `3`。  
> - `i = 4`：`[3,4]` 或 `[1,4]`，长度为 `2`。  
> - `i = 5`：`[1,2]` 或 `[3,2]`（取 `[1,2]` 为合法），长度为 `2`。

## 约束条件

- `n == obstacles.length`
- `1 ≤ n ≤ 10^5`
- `1 ≤ obstacles[i] ≤ 10^7`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**对每一个位置 `i`，把它左边所有可以接在前面的障碍都枚举一遍**，找出最长的合法序列长度。

- **数据结构**：只需要一个一维数组 `dp`，`dp[i]` 保存以 `obstacles[i]` 结尾的最长障碍课程的长度。可以把它想象成“每个人手里记的最高成绩”，我们只要把所有比自己低（或相等）的成绩挑出来，取最大再加一。
- **为什么正确**：如果某条合法序列的最后一个障碍是 `i`，那么它的倒数第二个障碍一定在 `i` 左边且高度 `≤ obstacles[i]`（题目要求非递减）。于是把左边所有满足 `obstacles[j] ≤ obstacles[i]` 的 `dp[j]` 取最大，再加上 `obstacles[i]` 本身，就得到以 `i` 结尾的最长序列。遍历完所有 `i`，每个 `dp[i]` 就是答案。
- **时间/空间复杂度**：  
  - 对每个 `i` 我们都要检查 `0 … i‑1`，最坏情况要检查 `1 + 2 + … + (n‑1) = n·(n‑1)/2` 次，**时间复杂度是 O(n²)**。  
  - 只用了 `dp` 一个长度为 `n` 的数组，**空间复杂度是 O(n)**。  
  > 大白话：`O(n²)` 就像把 `n` 本书两两对比一次，工作量会随 `n` 的平方快速增长，`n=10⁵` 时根本跑不完。

#### 代码（Python）

```python
from typing import List

def longest_obstacle_course_bruteforce(obstacles: List[int]) -> List[int]:
    n = len(obstacles)
    dp = [1] * n                     # 每个位置至少可以自己形成长度为 1 的序列
    for i in range(n):
        # 检查 i 左边所有可以接在前面的障碍
        for j in range(i):
            if obstacles[j] <= obstacles[i]:   # 非递减要求
                # 把左边的最长长度加到当前
                dp[i] = max(dp[i], dp[j] + 1)
    return dp
```

#### 复杂度

- **时间复杂度**：`O(n²)` — 需要两层循环，外层 `n` 次，内层平均约 `n/2` 次，整体随 `n` 的平方增长。  
- **空间复杂度**：`O(n)` — 只用了一个长度为 `n` 的 `dp` 数组来存放结果。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于每次都要**遍历左边所有元素**。我们注意到，只关心“**在左边能接的序列中，长度最大的那一个**”。如果能够**快速知道**对于任意长度 `len`，**最小的可能结尾高度**是多少，就能直接定位当前障碍能接到的最长长度。

这正是**“Patience Sorting（纸牌游戏）”**思想的核心：  
- 维护一个数组 `tails`（有时叫 `d`），其中 `tails[l]` 表示**长度为 `l+1` 的合法序列的最小可能结尾高度**。  
- `tails` 是递增的（因为更长的序列一定要比更短的序列的最小结尾更大或相等），所以我们可以用**二分查找**在 `tails` 中定位**第一个大于等于当前障碍的下标**（这里用 “右侧等于” 的原因是序列允许相等）。  
- 设二分得到的位置是 `pos`（`0`‑based），则当前障碍可以接在长度为 `pos` 的序列后面，得到长度 `pos+1`，并且我们要把 `tails[pos]` 更新为 `obstacles[i]`（因为我们找到了一条同样长度但结尾更小的序列，后面可能更有利）。

把这个过程对每个 `i` 从左到右执行，就能在 **`O(log n)`** 时间内得到 `ans[i]`，整体是 **`O(n log n)`**。

> **类比**：想象每一种长度的“最轻背包”。`tails[l]` 就是装下 `l+1` 件物品时，**最轻的背包重量**。当一个新物品（障碍）出现时，我们把它放进**能够装下它的最小背包**，这样以后装更重的东西时，背包仍然是尽可能轻的。

**关键点**  

| 步骤 | 说明 |
|------|------|
| 1. 维护 `tails` | `tails[k]` = 当前已知的、长度为 `k+1` 的合法序列的最小结尾高度 |
| 2. 二分定位 | 使用 `bisect_right(tails, obstacles[i])` 找到第一个 **>** `obstacles[i]` 的位置，等价于找最长可以接的序列长度 |
| 3. 更新 `tails` | 把 `tails[pos] = obstacles[i]`（若 `pos` 已经存在），否则在末尾追加 |
| 4. 记录答案 | `ans[i] = pos + 1`（因为长度是下标 + 1） |

#### 代码（Python）

```python
from bisect import bisect_right
from typing import List

def longest_obstacle_course(obstacles: List[int]) -> List[int]:
    """
    O(n log n) 解法
    tails[k] 表示长度为 k+1 的合法序列的最小结尾高度
    """
    tails: List[int] = []          # 空的 tails
    ans: List[int] = []            # 最终答案

    for h in obstacles:            # 从左到右遍历每个障碍
        # bisect_right 在 tails 中找第一个 > h 的位置
        # 这样得到的下标 pos 正好是可以接上的最长序列的长度（0‑based）
        pos = bisect_right(tails, h)

        if pos == len(tails):
            # 没有比 h 更大的，说明可以把它接在最长序列后面，直接扩展
            tails.append(h)
        else:
            # 用更小的结尾高度替换，保持 tails 的“最小结尾”性质
            tails[pos] = h

        # 当前障碍的最长合法序列长度就是 pos+1
        ans.append(pos + 1)

    return ans
```

> **代码要点注释**  
- `bisect_right(tails, h)`：在递增数组 `tails` 中找 **最右侧** 可以插入 `h` 的位置，相当于“第一个严格大于 `h` 的下标”。因为序列允许相等，使用 `right` 可以把相等的元素放在更长的序列里。  
- `if pos == len(tails)`：说明 `h` 大于等于所有已有的最小结尾，可以把它接在最长序列后面，`tails` 长度加一。  
- `tails[pos] = h`：即使 `h` 不能延长序列，也可能让同长度的序列结尾更小，为以后更高的障碍提供更大的“容错空间”。  

#### 复杂度

- **时间复杂度**：`O(n log n)` — 对每个 `obstacles[i]` 只做一次二分查找（`log n`），遍历 `n` 次。相比暴力的 `O(n²)`，即使 `n=10⁵` 也能轻松跑完。  
- **空间复杂度**：`O(n)` — 最坏情况下 `tails` 长度会等于 `n`（完全递增），再加上返回的答案数组，同样是线性空间。

---

## 心得

- **核心技巧**：维护「每个长度对应的最小可能结尾」并用二分查找快速定位，这其实是 **非递减版最长递增子序列（LIS）** 的标准做法。  
- **适用的题型**  
  1. **最长递增子序列**（LeetCode 300）——只是不允许相等。  
  2. **最长非递减子序列**（LeetCode 274）——本题的变体，只求整体最长而不是每个位置。  
  3. **在序列中插入/查询最小/最大值的离线问题**，常用 **Binary Indexed Tree / Segment Tree + 坐标压缩**（同样思路）。  
- **一句话总结**：**把“最长长度”转化为“最小结尾”，用二分把查询压到对数级**。

---

## 反思

- **第一反应**：看到“每个位置都要输出长度”，自然想到 DP，遍历左边所有元素求最大，结果就是 O(n²)。  
- **最容易踩的坑**  
  - **相等的处理**：序列允许 `obstacle[j] == obstacle[i]`，所以在二分时必须使用 `bisect_right`（右侧插入），否则会把相等的元素误认为只能形成更短序列。  
  - **边界条件**：空 `tails` 时 `pos == 0`，要记得先 `append` 再记录答案。  
  - **大数范围**：`obstacles[i]` 最大到 `10⁷`，不影响二分，但如果使用 BIT 需要坐标压缩。  
- **下次遇到同类题**：第一步先问自己「**我只关心长度，还是也需要具体的序列**？」如果只关长度，立刻想到「**最小结尾 + 二分**」或「**BIT + 前缀最大**」的思路。这样就能直接跳到 O(n log n) 的方案，避免 O(n²) 的陷阱。