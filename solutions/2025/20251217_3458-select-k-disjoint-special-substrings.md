# #3458. 选择 K 个互不相交的特殊子串 / Select K Disjoint Special Substrings

> 难度：中等 · 标签：Hash Table、String、Dynamic Programming、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/select-k-disjoint-special-substrings/)

---

## 题目（英文原版）

**Description**

Given a string s of length n and an integer k, determine whether it is possible to select k disjoint special substrings.
A special substring is a substring where:
Note that all k substrings must be disjoint, meaning they cannot overlap.
Return true if it is possible to select k such disjoint special substrings; otherwise, return false.

**Examples**

**Example 1:**

```
Input: s = "abcdbaefab", k = 2
Output: true
Explanation:
```

**Example 2:**

```
Input: s = "cdefdc", k = 3
Output: false
Explanation:
There can be at most 2 disjoint special substrings: "e" and "f" . Since k = 3 , the output is false .
```

**Example 3:**

```
Input: s = "abeabe", k = 0
Output: true
```

**Constraints**

- 2 <= n == s.length <= 5 * 104
- 0 <= k <= 26
- s consists only of lowercase English letters.

---

## 题目（中文翻译）

给定一个长度为 **n** 的字符串 `s` 和一个整数 `k`，判断是否可以选取 **k** 个互不相交的特殊子串（special substring）。
**特殊子串** 是满足特定条件的子串（substring），题目中会给出该条件的具体定义。
需要注意的是，所有 **k** 个子串必须互不相交，即它们之间不能有重叠。
如果可以选取 **k** 个这样的互不相交的特殊子串，返回 `true`；否则返回 `false`。

### 示例

#### 示例 1
**输入**  
`s = "abcdbaefab", k = 2`  
**输出**  
`true`  
**解释**  

（此处填写示例 1 的解释）

#### 示例 2
**输入**  
`s = "cdefdc", k = 3`  
**输出**  
`false`  
**解释**  
最多只能得到 2 个互不相交的特殊子串，分别是 `"e"` 和 `"f"`。因为 `k = 3`，所以返回 `false`。

#### 示例 3
**输入**  
`s = "abeabe", k = 0`  
**输出**  
`true`  
**解释**  

（此处填写示例 3 的解释）

### 约束条件
- `2 <= n == s.length <= 5 * 10^4`
- `0 <= k <= 26`
- `s` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：

1. **枚举所有子串**  
   对每一个左端点 `l`（`0 ≤ l < n`），把右端点 `r` 从 `l` 向右逐个扩展，得到子串 `s[l..r]`。

2. **判断子串是否 “special”**  
   对当前子串里的每个字符 `c`，检查它在整个字符串 `s` 中的出现位置。  
   - 如果 `c` 在子串外还有出现（即 `c` 的最左出现位置 `< l` 或最右出现位置 `> r`），则这个子串 **不是** special。  
   - 只有当子串里出现的所有字符的 **全部** 出现都被包含在 `[l, r]` 里时，子串才算 special。

3. **在所有 special 子串中挑选 k 个互不重叠的**  
   把所有满足 special 条件的子串记为区间 `[l, r]`，随后在这些区间里尝试挑选 `k` 个两两不相交的区间。  
   这一步可以用回溯（深度优先搜索）暴力尝试：  
   - 按左端点升序遍历区间，  
   - 对每个区间决定「选」或「不选」，选了以后后面的区间必须左端点 `≥` 当前区间的右端点 `+1`，  
   - 只要找到一种选法使得选中的区间数达到 `k`，就返回 `True`。

> **生活化类比**：  
> 把字符串想象成一本书的全部页码。每个字母是一本只在特定几页出现的“小册子”。  
> **special 子串** 就是一次“借阅”，必须把包含该字母所有页码的那几页一次性全部借走，不能只借走其中一页。  
> 我们要在整本书里找 `k` 次不重叠的完整借阅。

**为什么正确**：  
- 只要遍历了所有可能的左、右端点，就不会漏掉任何子串。  
- 只要把所有满足 special 条件的子串都列出来，再在这些子串里找 `k` 个互不相交的组合，必然能够判断是否存在合法方案。

**时间/空间复杂度**（大白话版）：

| 步骤 | 复杂度 | 大白话解释 |
|------|--------|------------|
| 枚举所有子串 | `O(n²)`（`n`≈5·10⁴，最坏会有 2.5 × 10⁹ 次）| 每个左端点要和每个右端点配对，像把 5 万本书的每一页和后面的每一页都配对一次。 |
| 判断 special | `O(26)`（最多 26 个字母）| 检查每个字母的最左/最右出现位置，最多 26 次。 |
| 回溯挑选 k 个 | 最坏 `O(2^m)`，`m` 为 special 子串数（在最坏情况下 `≈ n²`）| 组合爆炸，类似把所有子串的“选/不选”全排列跑一遍。 |
| **总计** | **指数级**（几乎不可接受）| 对 5 万长度的字符串根本跑不完。 |
| 空间 | `O(n²)`（存所有子串）| 需要把每个子串的左、右坐标都保存下来。 |

显然，这种暴力方法只能在 **超小** 的测试数据上玩玩，根本不适合正式提交。

---

#### 代码（Python）

```python
from typing import List

def is_special(s: str, l: int, r: int,
               first: List[int], last: List[int]) -> bool:
    """检查子串 s[l..r] 是否为 special。"""
    seen = set()
    for i in range(l, r + 1):
        c = s[i]
        if c in seen:
            continue
        seen.add(c)
        # 若该字符在子串外还有出现，则不是 special
        if first[ord(c) - 97] < l or last[ord(c) - 97] > r:
            return False
    return True

def brute_force(s: str, k: int) -> bool:
    n = len(s)
    if k == 0:
        return True

    # 预处理每个字母的最左、最右出现位置
    first = [n] * 26
    last  = [-1] * 26
    for i, ch in enumerate(s):
        idx = ord(ch) - 97
        first[idx] = min(first[idx], i)
        last[idx]  = max(last[idx], i)

    # 1️⃣ 收集所有 special 子串（区间）
    intervals = []                     # (左, 右)
    for l in range(n):
        for r in range(l, n):
            if is_special(s, l, r, first, last):
                intervals.append((l, r))

    # 2️⃣ 深度优先搜索挑选 k 个不相交区间
    intervals.sort()                    # 按左端点升序，便于剪枝

    def dfs(idx: int, chosen: int, prev_end: int) -> bool:
        # 已经选够 k 个，成功
        if chosen == k:
            return True
        # 已经遍历完所有区间，仍未够 k 个，失败
        if idx == len(intervals):
            return False
        # 剪枝：剩余区间数不足以凑齐 k
        if chosen + (len(intervals) - idx) < k:
            return False

        l, r = intervals[idx]
        # 选当前区间（前提是不与上一个冲突）
        if l > prev_end:
            if dfs(idx + 1, chosen + 1, r):
                return True
        # 不选当前区间，尝试下一个
        return dfs(idx + 1, chosen, prev_end)

    return dfs(0, 0, -1)
```

> **注释**：  
> - `first` / `last` 就像“字典”，记录每个字母第一次和最后一次出现的页码。  
> - `is_special` 用这些字典快速判断子串是否完整包含了它出现的所有字母。  
> - `dfs` 是“选/不选”暴力搜索，`prev_end` 记录上一次选中的子串右端点，保证不重叠。

---

#### 复杂度

- **时间复杂度**：`O(n² * 26 + 2^m)`，其中 `m` 为所有 special 子串的数量。整体呈指数级，无法接受。  
- **空间复杂度**：`O(n²)` 用于存储所有子串的区间。

---

### 2. 最优解

#### 思路  

暴力解慢的根本原因在于 **枚举所有子串**（`O(n²)`）以及 **组合搜索**（指数级）。  
观察题目提示可以得到关键的 **结构性信息**：

1. **每个字母的出现区间**  
   对字母 `c`，记 `L[c]` 为它第一次出现的位置，`R[c]` 为它最后一次出现的位置。  
   这两个位置就像 **“这本书里这本小册子的起止页码”**，最多只有 26 本小册子（因为只有 26 个小写字母）。

2. **从任意字符出发，构造最小的 special 区间**  
   设起点 `i` 为某个字符 `c` 的**第一次**出现（因为如果 `i` 不是第一次出现，它必定已经被前面的区间覆盖，没必要再从这里开始）。  
   - 初始右端点 `right = R[c]`（要把 `c` 的全部出现都装进去）。  
   - 接下来在 `[i, right]` 区间里检查每个字符 `x`，如果 `R[x] > right`，说明 `x` 的出现超出了当前右端点，需要把区间扩展到 `R[x]`。  
   - 继续循环，直到区间不再扩展。  
   这一步相当于 **“把所有涉及的字母的页码都拉到最右”**，得到的 `[i, right]` 就是包含 `i` 的**最小** special 区间。

   由于我们只从 **每个字母的第一次出现** 开始构造，这一步最多进行 26 次，得到的区间数量 `m ≤ 26`。

3. **在得到的区间集合中挑选 k 个互不重叠的区间**  
   现在问题转化为：**在至多 26 条区间里，能否选出至少 k 条不相交的区间？**  
   这正是经典的「**区间调度（Interval Scheduling）**」问题。  
   - 先把所有区间按 **右端点** 从小到大排序。  
   - 用 **动态规划 + 二分查找** 计算到第 `i` 条区间为止最多能选多少条：  

     ```
     dp[i] = max(dp[i-1], dp[p] + 1)
     ```
     其中 `p` 是在排序后**右端点 < left_i** 的最大下标（即与第 i 条区间不重叠的最近的区间），可以用二分搜索快速得到。

   - 最终 `dp[m]`（或 `dp[-1]`）即为最多可以挑选的 disjoint special 子串数。只要 `dp[m] ≥ k`，答案为 `True`。

4. **特殊情况**  
   - `k = 0`：不需要任何子串，直接返回 `True`。  
   - `k > 26`：因为最多只能得到 26 条区间，直接返回 `False`（但题目已保证 `k ≤ 26`）。

**核心算法**：  
- **构造最小 special 区间**（一次线性扫描 + 26 次循环）  
- **区间调度的 DP**（排序 + 二分）  

这两个步骤的时间复杂度都是 **线性或对数级**，远远快于暴力 `O(n²)`。

---

#### 代码（Python）

```python
from bisect import bisect_right
from typing import List, Tuple

def can_select_k_special(s: str, k: int) -> bool:
    """返回是否可以选出 k 个两两不相交的 special 子串"""
    n = len(s)
    if k == 0:                 # 不选也行
        return True

    # ---------- 1. 预处理每个字母的最左、最右出现位置 ----------
    INF = n
    first = [INF] * 26         # L[c]
    last  = [-1]  * 26         # R[c]
    for i, ch in enumerate(s):
        idx = ord(ch) - 97
        first[idx] = min(first[idx], i)
        last[idx]  = max(last[idx], i)

    # ---------- 2. 只从每个字母的第一次出现出发，构造最小 special 区间 ----------
    intervals: List[Tuple[int, int]] = []   # (左, 右)
    for c in range(26):
        if first[c] == INF:          # 该字母根本没出现
            continue
        l = first[c]                 # 起点一定是该字母的第一次出现
        r = last[c]                  # 初始右端点覆盖该字母所有出现
        # 扩展区间，使之包含所有在区间内字符的全部出现
        j = l
        while j <= r:                # 线性扫描区间内的字符
            idx = ord(s[j]) - 97
            r = max(r, last[idx])    # 若有字符的最右出现更靠右，拉伸右端点
            j += 1
        intervals.append((l, r))

    # ---------- 3. 区间调度：在这些区间中挑选最多的不相交区间 ----------
    intervals.sort(key=lambda x: x[1])          # 按右端点升序

    # 为二分准备右端点数组
    ends = [r for (_, r) in intervals]

    m = len(intervals)
    dp = [0] * (m + 1)          # dp[i] = 前 i 条区间（0..i-1）能选的最多数量
    for i in range(1, m + 1):
        l_i, r_i = intervals[i - 1]

        # 找到最近的、右端点 < l_i 的区间下标 p（在 dp 中对应 p+1）
        # bisect_right 返回第一个 > l_i-1 的位置
        p = bisect_right(ends, l_i - 1, 0, i - 1)   # 只在前 i-1 条里搜索
        # dp 转移：不选第 i 条 或 选第 i 条 + 前面不冲突的最优解
        dp[i] = max(dp[i - 1], dp[p] + 1)

    # dp[m] 即为最多能选出的 disjoint special 子串数
    return dp[m] >= k
```

> **代码解读**  
> - `first / last` 类似 **“字典”**，把每本小册子的起止页码记下来。  
> - 构造最小区间时，用 **“把区间里出现的所有字母的右端点都拉到最右”** 的方式一次性完成，时间复杂度仅 `O(n)`。  
> - `bisect_right` 实现 **二分查找**，快速定位与当前区间不重叠的最近前驱区间，保证 DP 的每一步是 `O(log m)`（这里 `m ≤ 26`，几乎是常数）。  

---

#### 复杂度

| 步骤 | 时间复杂度 | 空间复杂度 | 解释 |
|------|------------|------------|------|
| 预处理 `first / last` | `O(n)` | `O(26)` | 只遍历一次字符串，记录每个字母的最左/最右位置。 |
| 构造最小 special 区间 | `O(n)`（每个字符最多被扫描一次） | `O(m)` (`m ≤ 26`) | 只从 26 个起点出发，区间扩展过程线性遍历。 |
| 区间排序 | `O(m log m)`，实际 ≤ `O(26 log 26)` | `O(m)` | 排序方便后续 DP。 |
| DP + 二分 | `O(m log m)`（同上） | `O(m)` | `dp` 数组保存子问题答案。 |
| **总计** | **`O(n) + O(26 log 26)` ≈ `O(n)`** | **`O(n)`**（主要是存 `first/last`，其余常数） | 对于 `n ≤ 5·10⁴` 完全可接受。 |

与暴力解相比，时间从 **指数级** 降到了 **线性**，空间也从 `O(n²)` 降到 `O(n)`，实现了巨大的性能提升。

---

## 心得

- **核心技巧**：利用字母出现的 **最左/最右位置** 把问题压缩到至多 26 条区间，再用 **区间调度（DP + 二分）** 求最大不相交子集。  
- **适用场景**：  
  1. **“分割标签”**（LeetCode 763）——把字符串划分为每个字母只出现一次的最小块。  
  2. **“最少区间覆盖”**（把若干区间合并成最少数量的非重叠区间）。  
  3. **“挑选最多不重叠区间”**（经典的活动安排问题）。  
- **一句话总结解题钥匙**：**把所有可能的 special 子串压缩到字母的出现区间，再用贪心/DP 选最多的不相交区间**。

---

## 反思

- **第一反应**：直接暴力枚举所有子串并尝试组合，忽视了字符串中只有 26 种字符这一关键限制。  
- **最容易踩的坑**：  
  - **判断 special** 时忘记检查 **左端点** 是否也满足 `first[c] ≥ l`，导致错误的子串被当作 special。  
  - **区间不相交的定义**：右端点等于下一个左端点时是可以的（即 `r_i < l_j`），实现二分时要注意使用 `l_i - 1`。  
  - **k = 0** 的特殊情况必须提前返回，否则 DP 会误判。  
- **下次遇到同类题**，第一步应先 **提炼出全局唯一的“约束点”（如字符的首尾位置）**，看看是否能把搜索空间压到常数级，然后再使用 **区间调度** 或 **贪心** 求最大不冲突子集。