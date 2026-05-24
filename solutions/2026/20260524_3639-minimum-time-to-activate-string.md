# #3639. 激活字符串的最小时间 / Minimum Time to Activate String

> 难度：中等 · 标签： · [LeetCode 链接](https://leetcode.com/problems/minimum-time-to-activate-string/)

---

## 题目（英文原版）

**Description**

You are given a string s of length n and an integer array order, where order is a permutation of the numbers in the range [0, n - 1].
Starting from time t = 0, replace the character at index order[t] in s with '*' at each time step.
A substring is valid if it contains at least one '*'.
A string is active if the total number of valid substrings is greater than or equal to k.
Return the minimum time t at which the string s becomes active. If it is impossible, return -1.

**Examples**

**Example 1:**

```
Input: s = "abc", order = [1,0,2], k = 2
Output: 0
Explanation:
The string s becomes active at t = 0 . Thus, the answer is 0.
```

**Example 2:**

```
Input: s = "cat", order = [0,2,1], k = 6
Output: 2
Explanation:
The string s becomes active at t = 2 . Thus, the answer is 2.
```

**Example 3:**

```
Input: s = "xy", order = [0,1], k = 4
Output: -1
Explanation:
Even after all replacements, it is impossible to obtain k = 4 valid substrings. Thus, the answer is -1.
```

**Constraints**

- 1 <= n == s.length <= 105
- order.length == n
- 0 <= order[i] <= n - 1
- s consists of lowercase English letters.
- order is a permutation of integers from 0 to n - 1.
- 1 <= k <= 109

---

## 题目（中文翻译）

给定一个长度为 **n** 的字符串 `s` 和一个整数数组 `order`，其中 `order` 是区间 **[0, n‑1]** 内数字的一个排列。

从时间 **t = 0** 开始，在每个时间步将 `s` 中下标为 `order[t]` 的字符替换为 `'*'`。

如果一个子串（substring）至少包含一个 `'*'`，则称该子串为**有效**的。

如果字符串中所有有效子串的总数大于等于 **k**，则称该字符串为**活跃**的。

返回字符串 `s` 变为活跃状态的最小时间 **t**。如果无法实现，返回 **-1**。

---

### 示例

**示例 1**

```
Input: s = "abc", order = [1,0,2], k = 2
Output: 0
```
**解释**：  
在 **t = 0** 时，字符串已经满足活跃条件，因此答案为 **0**。

**示例 2**

```
Input: s = "cat", order = [0,2,1], k = 6
Output: 2
```
**解释**：  
当 **t = 2** 时，字符串变为活跃，所以答案为 **2**。

**示例 3**

```
Input: s = "xy", order = [0,1], k = 4
Output: -1
```
**解释**：  
即使全部字符都被替换为 `'*'`，仍然无法得到 **k = 4** 个有效子串。因此答案为 **-1**。

---

### 约束条件

- `1 <= n == s.length <= 10^5`
- `order.length == n`
- `0 <= order[i] <= n - 1`
- `s` 只包含小写英文字母。
- `order` 是从 `0` 到 `n‑1` 的一个排列。
- `1 <= k <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**模拟**题目给出的过程：

1. 从 `t = 0` 开始，依次把 `order[t]` 位置的字符改成 `'*'`。  
2. 每次改完以后，遍历整条字符串，统计**包含至少一个 `'*'` 的子串**有多少个。  
3. 判断统计值是否已经 `≥ k`，如果是，就返回当前的 `t`；否则继续下一步。

> **用到的数据结构**  
> - **数组** `order` 本身就像一本“换位手册”，告诉我们每一分钟要去哪个下标换成 `'*'`。  
> - **遍历字符串** 时我们只需要一个普通的 **循环变量**，不需要额外的数据结构。  
> - 为了判断子串是否包含 `'*'`，可以把每个位置的字符直接和 `'*'` 做比较，就像在日常生活中“看这块地有没有标记”。

**为什么正确**  
因为我们严格按照题目描述一步步执行：每一次都把恰好一个位置变成 `'*'`，并且在每一步都完整地检查所有子串是否满足条件。只要在某一步满足 `valid_substrings ≥ k`，那一步的 `t` 必然是答案（因为我们是从 `t = 0` 按顺序递增的）。

**时间/空间复杂度**  
- 对每一个 `t`（最多 `n` 次）我们都要遍历 **所有** 子串来计数。子串的数量是 `n·(n+1)/2`（等差数列求和），所以每一步的时间是 `O(n²)`。整体时间就是 `O(n³)`，在最坏情况下会 **超时**（`n` 可达 10⁵）。  
- 只用了原始的字符串和 `order`，空间是 `O(1)`（不计输入本身）。

> **大白话解释**：  
> - `O(n³)` 可以想象成“把一座有 `n` 层的塔每层都拆成 `n` 块，再把每块拆成 `n` 小块”。当 `n` 只有几百时还能接受，`n=10⁵` 时根本不可能在一分钟内完成。

#### 代码（Python）

```python
def minTime_bruteforce(s: str, order: list[int], k: int) -> int:
    n = len(s)
    # 把字符串转成列表，方便原地修改为 '*'
    arr = list(s)

    # 一次遍历所有可能的 t（0~n-1）
    for t in range(n):
        # 把第 t 步对应的下标换成 '*'
        idx = order[t]
        arr[idx] = '*'

        # 统计包含 '*' 的子串数量（暴力 O(n^2)）
        cnt = 0
        for i in range(n):               # 子串左端点
            has_star = False
            for j in range(i, n):        # 子串右端点
                if arr[j] == '*':
                    has_star = True
                if has_star:             # 只要出现过 '*', 这条子串就算有效
                    cnt += 1

        if cnt >= k:                     # 第一次满足条件即返回
            return t

    return -1   # 全部换完仍不够
```

#### 复杂度

- **时间复杂度**：`O(n³)`  
  - `n` 次循环（每个时间点） × 每次遍历 `n²` 条子串 → 总共 `n³` 次基本操作。  
- **空间复杂度**：`O(1)`（不计输入）  
  - 只用了常数个额外变量。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每一步都要重新遍历所有子串**。我们需要一种办法，**快速判断在第 `t` 步时，整个字符串有多少有效子串**，而不是逐个枚举。

观察可以发现：

- 一个子串 **不** 包含 `'*'` 的唯一可能是它完全位于一段连续的、**没有被替换** 的字符区间（我们称之为 “纯段”）。  
- 如果我们知道所有纯段的长度 `L₁, L₂, …`，那么不含 `'*'` 的子串总数就是每段内部子串的和：  

\[
\text{invalid} = \sum_{i} \frac{L_i (L_i + 1)}{2}
\]

- 整条字符串的所有子串数是固定的 `n·(n+1)/2`（把每个起点和终点配对的组合数），所以  

\[
\text{valid} = \frac{n(n+1)}{2} - \text{invalid}
\]

因此，只要**快速得到所有纯段的长度**，我们就能在 `O(n)` 时间内算出 `valid`，进而判断是否 `≥ k`。

> **关键点**：  
> - 随着时间 `t` 增大，`'*'` 的位置只会**增多**，纯段只会**被切分得更小**，不会合并。  
> - 这正好适合二分搜索：**如果在某个 `t` 时已经满足 `valid ≥ k`，那么所有更大的 `t` 也一定满足**（因为把更多位置变成 `'*'` 只能让有效子串数不减）。  
> - 所以我们可以对答案 `t` 进行 **二分**，每一次二分检查都在 `O(n)` 完成。

**如何在一次检查中得到所有纯段的长度？**  

1. 先把前 `t+1` 个要被替换的下标标记为 `'*'`（用一个布尔数组 `is_star`）。  
2. 再从左到右扫描字符串，累计连续的非 `'*'` 长度 `cur_len`。  
   - 当遇到 `'*'` 或扫描结束时，把 `cur_len` 对应的子串数 `cur_len·(cur_len+1)//2` 累加到 `invalid`，然后把 `cur_len` 归零。  
3. 循环结束后，用公式 `total - invalid` 得到 `valid`。

**二分搜索的范围**  
- 最小可能的时间是 `0`（一开始就可能满足）。  
- 最大可能的时间是 `n-1`（全部字符都被换成 `'*'`）。  
- 若即使在 `t = n-1` 时仍不满足，则答案是 `-1`。

> **类比**：  
> 想象一条长长的路（字符串），路上有若干盲点（`'*'`）。我们要统计 **至少经过一个盲点的路径** 有多少条。把所有盲点标记出来后，只需要统计 **没有盲点的连续路段** 的路径数，然后用总路径数减去它们，就得到答案。

#### 代码（Python）

```python
def minTime(s: str, order: list[int], k: int) -> int:
    n = len(s)
    total_sub = n * (n + 1) // 2          # 所有子串的总数（不管有没有 '*')
    
    # 检查在给定的 t（0-indexed）时，是否已经有足够的有效子串
    def enough(t: int) -> bool:
        # 标记前 t+1 个位置为 '*'
        is_star = [False] * n
        for i in range(t + 1):
            is_star[order[i]] = True

        invalid = 0          # 不含 '*' 的子串数
        cur_len = 0          # 当前连续非 '*' 段的长度

        for i in range(n):
            if is_star[i]:               # 遇到 '*', 结束当前段
                if cur_len:
                    invalid += cur_len * (cur_len + 1) // 2
                    cur_len = 0
            else:                        # 仍在纯段中
                cur_len += 1

        # 最后可能还有一个未结束的段
        if cur_len:
            invalid += cur_len * (cur_len + 1) // 2

        valid = total_sub - invalid
        return valid >= k

    # 二分搜索答案
    left, right = 0, n - 1
    ans = -1
    while left <= right:
        mid = (left + right) // 2
        if enough(mid):            # 如果 mid 已经够了，尝试更小的 t
            ans = mid
            right = mid - 1
        else:                      # 不够，必须往后走
            left = mid + 1
    return ans
```

> **关键行中文注释**  
> - `is_star[order[i]] = True` 把第 `i` 步要换的位置记为 `'*'`（相当于在字典里写下“这里已经打了标记”）。  
> - `invalid += cur_len * (cur_len + 1) // 2` 把一段纯净区间里所有不含 `'*'` 的子串数一次性算出来，避免逐个子串枚举。  
> - `valid = total_sub - invalid` 总子串数减去无效子串，即为满足条件的子串数。

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 二分搜索最多 `log₂ n` 次（约 17 次，`n ≤ 10⁵`）。  
  - 每一次检查 `enough(t)` 需要一次线性扫描 `O(n)`。  
  - 所以总体是 `O(n log n)`，能够轻松跑完最大数据规模。  
- **空间复杂度**：`O(n)`（布尔数组 `is_star`）  
  - 只用了与字符串等长的额外数组，常数级的其他变量不计入。  

> 与暴力解相比：时间从 `O(n³)` 降到了 `O(n log n)`，几乎快了 **上万倍**；空间略增，但仍在可接受范围。

---

## 心得

- **核心技巧**：利用“总数减去不合法数” 的思路把子串计数转化为 **连续段长度的组合数**，并配合 **二分搜索** 判断最小满足时间。  
- **适用的题型**  
  1. “把若干位置标记后，统计满足某种条件的子数组/子串数”——如 **Maximum Number of Subarrays With Bounded Sum**。  
  2. “随着阈值增大，满足条件的区间数量单调变化”，需要 **二分 + 前缀/区间统计**——如 **Find Minimum Time to Complete All Jobs**。  
  3. “统计不包含特定字符的子串”，可以用 **段长度公式**——如 **Number of Substrings Containing All Three Characters**（变形）。  
- **一句话总结解题钥匙**：  
  “把‘至少出现一次星号’的子串转化为‘总子串数减去所有纯段子串数’，再用二分快速定位最早满足的时间。”

---

## 反思

- **第一反应**：直接模拟并逐个枚举子串，想到“暴力遍历”。这在概念上最直观，但忽视了数据规模导致不可行。  
- **最容易踩的坑**  
  - **单调性误判**：必须确认随着 `t` 增大，**有效子串数不会下降**。因为我们只会把更多字符变成 `'*'`，不可能让已有的 `'*'` 消失。  
  - **边界条件**：`t = 0` 时要先检查（有可能一开始就满足），以及 `t = n-1` 仍不满足时返回 `-1`。  
  - **大数溢出**：`n·(n+1)/2` 可能超过 32 位整数，使用 Python 的大整数即可，但在其他语言要用 64 位。  
- **下次遇到同类题**：第一步先思考“**是否可以把要统计的对象转化为‘总量 - 不满足的量’**”，并判断单调性是否成立，随后考虑二分或滑动窗口等**单调搜索**技巧。这样往往能把指数级暴力直接压缩到对数级。