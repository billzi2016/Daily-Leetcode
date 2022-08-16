# #1898. **可移除字符的最大数量** / Maximum Number of Removable Characters

> 难度：中等 · 标签：Array、Two Pointers、String、Binary Search · [LeetCode 链接](https://leetcode.com/problems/maximum-number-of-removable-characters/)

---

## 题目（英文原版）

**Description**

You are given two strings s and p where p is a subsequence of s. You are also given a distinct 0-indexed integer array removable containing a subset of indices of s (s is also 0-indexed).
You want to choose an integer k (0 <= k <= removable.length) such that, after removing k characters from s using the first k indices in removable, p is still a subsequence of s. More formally, you will mark the character at s[removable[i]] for each 0 <= i < k, then remove all marked characters and check if p is still a subsequence.
Return the maximum k you can choose such that p is still a subsequence of s after the removals.
A subsequence of a string is a new string generated from the original string with some characters (can be none) deleted without changing the relative order of the remaining characters.

**Examples**

**Example 1:**

```
Input: s = "abcacb", p = "ab", removable = [3,1,0]
Output: 2
Explanation: After removing the characters at indices 3 and 1, "abcacb" becomes "accb".
"ab" is a subsequence of "accb".
If we remove the characters at indices 3, 1, and 0, "abcacb" becomes "ccb", and "ab" is no longer a subsequence.
Hence, the maximum k is 2.
```

**Example 2:**

```
Input: s = "abcbddddd", p = "abcd", removable = [3,2,1,4,5,6]
Output: 1
Explanation: After removing the character at index 3, "abcbddddd" becomes "abcddddd".
"abcd" is a subsequence of "abcddddd".
```

**Example 3:**

```
Input: s = "abcab", p = "abc", removable = [0,1,2,3,4]
Output: 0
Explanation: If you remove the first index in the array removable, "abc" is no longer a subsequence.
```

**Constraints**

- 1 <= p.length <= s.length <= 105
- 0 <= removable.length < s.length
- 0 <= removable[i] < s.length
- p is a subsequence of s.
- s and p both consist of lowercase English letters.
- The elements in removable are distinct.

---

## 题目（中文翻译）

给定两个字符串 `s` 和 `p`，其中 `p` 是 `s` 的子序列（subsequence）。同时给定一个互不相同的 **0** 索引整数数组 `removable`，它包含 `s` 的一部分下标（`s` 也是 **0** 索引）。  

你需要选择一个整数 `k`（`0 ≤ k ≤ removable.length`），使得在使用 `removable` 前 `k` 个下标从 `s` 中删除字符后，`p` 仍然是 `s` 的子序列（subsequence）。更正式地说，对于所有 `0 ≤ i < k`，标记下标 `removable[i]` 对应的字符，然后删除所有被标记的字符，检查 `p` 是否仍为子序列（subsequence）。  

返回能够满足上述条件的最大 `k`。

> **子序列（subsequence）**：从原字符串中删除若干字符（可以为零）后得到的新字符串，要求保留剩余字符的相对顺序不变。

### 示例

#### 示例 1
```
Input: s = "abcacb", p = "ab", removable = [3,1,0]
Output: 2
Explanation: 删除下标 3 和 1 对应的字符后，"abcacb" 变成 "accb"。此时 "ab" 是 "accb" 的子序列（subsequence）。  
如果再删除下标 0，对应的字符，"abcacb" 变成 "ccb"，此时 "ab" 已不再是子序列（subsequence）。因此最大 k 为 2。
```

#### 示例 2
```
Input: s = "abcbddddd", p = "abcd", removable = [3,2,1,4,5,6]
Output: 1
Explanation: 删除下标 3 对应的字符后，"abcbddddd" 变成 "abcddddd"。"abcd" 仍是 "abcddddd" 的子序列（subsequence）。
```

#### 示例 3
```
Input: s = "abcab", p = "abc", removable = [0,1,2,3,4]
Output: 0
Explanation: 删除 `removable` 中的第一个下标后，"abc" 已不再是子序列（subsequence）。
```

### 约束条件

- `1 ≤ p.length ≤ s.length ≤ 10^5`
- `0 ≤ removable.length < s.length`
- `0 ≤ removable[i] < s.length`
- `p` 是 `s` 的子序列（subsequence）。
- `s` 和 `p` 均只包含小写英文字母。
- `removable` 中的元素互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**枚举**所有可能的 `k`（从 `0` 到 `removable.length`），把前 `k` 个要删除的下标对应的字符从 `s` 中删掉，然后判断 `p` 是否仍然是 `s` 的子序列。

- **数据结构**  
  - `set`（集合）就像一本“查字典”，把要删掉的下标放进去，查询是否需要删除只需要一次 O(1) 的查找。  
  - 判断子序列时，用两个指针 `i`（遍历 `s`）和 `j`（遍历 `p`），类似“指着看”。如果当前字符没有被删且等于 `p[j]`，就把 `j` 往后移动一位，最终看 `j` 能否走到 `p` 的末尾。

- **为什么正确**  
  只要我们把 **恰好** 前 `k` 个下标对应的字符删掉，随后检查 `p` 是否还能按顺序在剩余字符中出现，这就是题目要求的“是否仍是子序列”。遍历所有 `k` 并取最大满足条件的即可。

- **时间/空间复杂度**  
  - 对每个 `k`（最多 `removable.length` 次）我们都要构造一次集合并遍历 `s`（长度最多 `10⁵`），所以时间复杂度是  
    \[
    O\big(\text{len(removable)} \times |s|\big)
    \]  
    用大白话说，就是**每删一次都要重新检查一遍整条长字符串**，最坏情况会接近 `10⁵ × 10⁵`，会超时。  
  - 集合里最多存 `k`（≤ `|s|`）个下标，空间复杂度是 `O(|s|)`（实际通常远小于 `|s|`）。

#### 代码（Python）

```python
def max_removable_bruteforce(s: str, p: str, removable: list[int]) -> int:
    n = len(removable)
    best = 0                     # 记录最大的合法 k

    # 枚举所有可能的 k
    for k in range(1, n + 1):
        # 把前 k 个下标放进集合，方便 O(1) 判断是否被删
        removed = set(removable[:k])

        # 双指针检查 p 是否仍是子序列
        i, j = 0, 0               # i 遍历 s，j 遍历 p
        while i < len(s) and j < len(p):
            if i not in removed and s[i] == p[j]:
                j += 1            # 成功匹配一个字符
            i += 1                # s 总是往前走

        if j == len(p):           # p 全部匹配成功
            best = k               # 更新答案

    return best
```

#### 复杂度

- **时间复杂度**：`O(|removable| × |s|)`  
  直观理解：每尝试一次删除，都要把整条字符串走一遍，像是“每次都重新读一遍书”。
- **空间复杂度**：`O(|s|)`（用于存放 `removed` 集合）  
  实际上集合里最多放 `k` 个元素，`k ≤ |removable| < |s|`。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每次都完整遍历 `s`**。我们需要一种“**一次检查**”就能判断任意 `k` 是否可行的方法。观察到：

1. 给定一个 `k`，我们只关心 **哪些下标被删**（前 `k` 个 `removable`），其余字符保持不变。  
2. 检查子序列的过程只需要一次 **双指针**遍历 `s`（和暴力一样），只要我们能 **快速判断一个位置是否已被删除**，就不必每次重新构造集合。

于是可以把 “是否可行” 这个子问题抽象为：

> **给定一个整数 `k`，把 `removable[:k]` 标记为删除，判断 `p` 是否仍是 `s` 的子序列。**

这一步的实现仍是 `O(|s|)`，但我们可以 **二分搜索** `k` 的最大值，因为：

- 当 `k` 越大（删的字符越多），`p` 成为子序列的可能性 **只会降低**（单调递减）。  
- 因此，满足条件的 `k` 形成一个前缀区间 `[0 … ans]`，我们可以在 `[0 … len(removable)]` 上二分找到最大合法 `k`。

二分的核心步骤：

1. 取中点 `mid`。  
2. 用 `mid` 构造 “已删除” 标记（可以用布尔数组 `deleted`，长度为 `|s|`，下标对应字符是否被删）。  
3. 用双指针检查子序列。  
4. 如果 `mid` 合法 → 说明更大的 `k` 也可能合法，左边界移到 `mid + 1`；否则右边界移到 `mid - 1`。  
5. 最终右边界 `right`（或左边界 `left-1`）就是答案。

> **为什么二分能用？**  
> 想象把每次删除看成把“桥梁”拆掉，桥越少，连通 `p` 的路径越难。只要一次删掉的桥让路径断了，之后再删更多桥肯定也断。因此满足条件的 `k` 是 **连续的前缀**，符合二分的单调性。

**实现细节**  

- 为了让 “某位置是否已删除” 的查询是 O(1)，我们用一个长度为 `|s|` 的布尔数组 `deleted`（类似“标记本”，把要删除的页码划掉）。  
- 每次二分检查完后，需要把 `deleted` 复原（重新创建新数组或在检查结束后清空），因为不同的 `mid` 对应的删除集合不同。  
- 整体时间复杂度是 `O(|s| log |removable|)`，因为二分最多 `log₂(|removable|)` 次，每次遍历 `s` 一次。

#### 代码（Python）

```python
def max_removable(s: str, p: str, removable: list[int]) -> int:
    """
    二分搜索最大 k，使得在删除 removable[:k] 之后 p 仍是 s 的子序列。
    """
    n = len(removable)

    # ---------- 子函数：判断给定 k 是否可行 ----------
    def can(k: int) -> bool:
        """返回 True 表示删除 removable[:k] 后，p 仍是子序列。"""
        # 1. 标记被删除的字符（布尔数组）
        deleted = [False] * len(s)
        for i in range(k):
            deleted[removable[i]] = True

        # 2. 双指针遍历 s 与 p
        j = 0                     # p 的指针
        for i, ch in enumerate(s):
            if deleted[i]:        # 被删掉的字符直接跳过
                continue
            if j < len(p) and ch == p[j]:
                j += 1            # 成功匹配一个字符
            if j == len(p):       # 已经全部匹配完
                return True
        return False               # 遍历完 s 仍未匹配完 p

    # ---------- 二分搜索 ----------
    left, right = 0, n            # left 为可行下界，right 为可行上界（可能）
    ans = 0
    while left <= right:
        mid = (left + right) // 2
        if can(mid):              # mid 可行 → 试更大的 k
            ans = mid
            left = mid + 1
        else:                     # mid 不可行 → 必须缩小 k
            right = mid - 1
    return ans
```

#### 复杂度

- **时间复杂度**：`O(|s| · log |removable|)`  
  - 二分的层数约为 `log₂(|removable|)`（比如 `|removable| = 10⁵` 时约 17 次），每层遍历一次 `s`（最长 `10⁵`），整体约 `1.7 × 10⁶` 次操作，能够轻松跑完。  
  - 与暴力的 `O(|removable|·|s|)`（最坏 `10¹⁰`）相比，速度提升了 **指数级**。

- **空间复杂度**：`O(|s|)`（布尔数组 `deleted`）  
  - 只需要额外的一个长度为 `|s|` 的标记数组，常数级别的额外空间。

---

## 心得

- **核心技巧**：**单调性 + 二分搜索**，配合 **双指针检查子序列**。  
- **该技巧适用的题型**：  
  1. “在数组/字符串上删除/修改一定数量的元素后，某性质是否仍然成立”——如 *Maximum Number of Removable Characters*、*Maximum Rows Covered by Columns*（二分 + 检查）。  
  2. “给定阈值，判断是否可行，然后求最大/最小阈值”——如 *Capacity To Ship Packages Within D Days*、*Split Array Largest Sum*。  
- **一句话总结解题钥匙**：**把“能否”转化为单调判定函数，用二分快速定位极限**。

---

## 反思

- **第一反应**：看到“最大 k”，立刻想到“二分”。但如果不注意到“k 增大只会让 p 更难成为子序列”，单调性就会失效。  
- **最容易踩的坑**：  
  - 忘记 `removable` 中的下标是 **相对于原始 s** 的，删除后下标不再连续，必须使用标记数组或集合直接判断。  
  - 在二分的 `can(k)` 中误把 `deleted` 设为全局共享导致上一轮的标记残留，必须每次重新构造或清空。  
  - 边界条件：`k = 0`（不删）一定合法，`k = len(removable)` 可能不合法，需要二分区间写对。  
- **下次类似题的第一步**：先**判断是否存在单调性**（删除/增加/阈值）→如果有，立刻构造**判定函数** → 用**二分**寻找极值。这样可以把指数级的枚举压到对数级。