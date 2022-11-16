# #2014. **最长子序列重复 k 次** / Longest Subsequence Repeated k Times

> 难度：困难 · 标签：String、Backtracking、Greedy、Counting、Enumeration · [LeetCode 链接](https://leetcode.com/problems/longest-subsequence-repeated-k-times/)

---

## 题目（英文原版）

**Description**

You are given a string s of length n, and an integer k. You are tasked to find the longest subsequence repeated k times in string s.
A subsequence is a string that can be derived from another string by deleting some or no characters without changing the order of the remaining characters.
A subsequence seq is repeated k times in the string s if seq * k is a subsequence of s, where seq * k represents a string constructed by concatenating seq k times.
Return the longest subsequence repeated k times in string s. If multiple such subsequences are found, return the lexicographically largest one. If there is no such subsequence, return an empty string.

**Examples**

**Example 1:**

```
Input: s = "letsleetcode", k = 2
Output: "let"
Explanation: There are two longest subsequences repeated 2 times: "let" and "ete".
"let" is the lexicographically largest one.
```

**Example 2:**

```
Input: s = "bb", k = 2
Output: "b"
Explanation: The longest subsequence repeated 2 times is "b".
```

**Example 3:**

```
Input: s = "ab", k = 2
Output: ""
Explanation: There is no subsequence repeated 2 times. Empty string is returned.
```

**Constraints**

- n == s.length
- 2 <= k <= 2000
- 2 <= n < min(2001, k * 8)
- s consists of lowercase English letters.

---

## 题目（中文翻译）

给定一个长度为 `n` 的字符串 `s` 和一个整数 `k`，请在字符串 `s` 中找出 **最长子序列（subsequence）重复 k 次** 的子序列。

- **子序列（subsequence）** 是指通过删除零个或多个字符且不改变剩余字符的相对顺序而得到的字符串。
- 若子序列 `seq` 在字符串 `s` 中出现 `k` 次，则表示 `seq * k`（即将 `seq` 连接 `k` 次得到的字符串）是 `s` 的一个子序列。

返回满足条件的最长子序列。如果存在多个满足条件的子序列，返回 **字典序（lexicographically）最大** 的那个。如果不存在这样的子序列，返回空字符串 `""`。

### 示例

#### 示例 1
**输入**  
``` 
s = "letsleetcode", k = 2
```  
**输出**  
```
"let"
```  
**解释**  
最长的满足条件的子序列有两个：`"let"` 和 `"ete"`。在这两个子序列中，`"let"` 的字典序更大，故返回 `"let"`。

#### 示例 2
**输入**  
``` 
s = "bb", k = 2
```  
**输出**  
```
"b"
```  
**解释**  
最长的满足条件的子序列是 `"b"`。

#### 示例 3
**输入**  
``` 
s = "ab", k = 2
```  
**输出**  
```
""
```  
**解释**  
不存在任何子序列能够在 `s` 中重复 `2` 次，返回空字符串。

### 约束条件

- `n == s.length`
- `2 <= k <= 2000`
- `2 <= n < min(2001, k * 8)`
- `s` 仅由小写英文字母组成

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是**枚举所有子序列**，然后检查每个子序列 `seq` 能否在原串 `s` 中出现 `k` 次（即 `seq * k` 仍是 `s` 的子序列）。  

- **子序列**可以想象成“从一本书里挑选若干页”，我们只要保持原来的顺序，不必连续。  
- **检查 `seq * k` 是否是子序列**相当于把 `seq` 连续写 `k` 次，再在 `s` 中从左到右“找字典”。如果每个字符都能依次找得到，就说明 `seq` 能被重复 `k` 次。  

这种做法一定能得到正确答案，因为我们把 **所有可能** 都遍历了一遍，只要有符合条件的子序列，就一定会被检测到。

#### 代码（Python）

```python
from itertools import combinations

def longestSubsequence_bruteforce(s: str, k: int) -> str:
    n = len(s)
    best = ""                     # 当前找到的最佳答案

    # 1️⃣ 逐长度从大到小枚举子序列（先尝试长的，找到后可以直接返回）
    for length in range(n // k, 0, -1):          # 最长不可能超过 n/k
        # 2️⃣ 用 combinations 生成所有长度为 length 的下标组合
        for idx_tuple in combinations(range(n), length):
            cand = ''.join(s[i] for i in idx_tuple)   # 生成子序列字符串

            # 3️⃣ 检查 cand*k 是否是 s 的子序列
            if is_repeat_subseq(s, cand, k):
                # 同时满足“最长”和“字典序最大”两条要求
                if cand > best:
                    best = cand
        if best:                     # 已经找到最长的，直接结束
            return best
    return ""                        # 没有符合条件的子序列

def is_repeat_subseq(s: str, sub: str, k: int) -> bool:
    """判断 sub 重复 k 次后是否仍是 s 的子序列。"""
    target = sub * k                # 把 sub 连写 k 次
    it = iter(s)                    # 把 s 当成迭代器，从左往右遍历
    return all(ch in it for ch in target)   # 每个字符都能在 it 中找到
```

> **关键行中文注释**  
> - `for length in range(n // k, 0, -1)`: 由于 `seq*k` 必须能放进 `s`，`len(seq)` 最多是 `n/k`。  
> - `combinations(range(n), length)`: 从 `n` 个位置里挑出 `length` 个，顺序不变，正好对应所有子序列。  
> - `all(ch in it for ch in target)`: Python 的迭代器特性让我们一次遍历即可判断子序列关系。

#### 复杂度  

- **时间复杂度**：  
  - 枚举所有子序列的数量是 `C(n,1)+C(n,2)+…+C(n,n/k)`，在最坏情况下接近 `2^n`（指数级）。  
  - 对每个子序列我们还要检查 `seq*k` 是否是子序列，最坏需要遍历 `s`（`O(n)`）。  
  - 综合下来是 **`O( n * 2^n )`**，对任何稍大的输入都会超时。  
  - 大白话：想象把所有可能的“挑选方式”都列出来，然后每一种都要再跑一遍整本书去验证，工作量非常巨大。

- **空间复杂度**：  
  - 只保存常数级别的变量和一次 `combinations` 生成的临时元组，**`O(n)`**（递归栈或迭代器的开销）。  

> 暴力解的思路虽然最直观，但因为搜索空间爆炸，实际不可用。下面我们一步步优化。

---

### 2. 最优解

#### 思路  

从暴力解出发，我们可以看到**两个瓶颈**：

1. **枚举的搜索空间太大**（所有子序列）。  
2. **每次验证都要线性扫描**，即使子序列已经很短也要遍历整串。

要把这两个瓶颈消掉，需要 **把可能出现的字符和长度先过滤**，再在**更小的搜索空间**里“聪明”地检查可行性。

下面的关键想法来源于题目给出的提示：

1. **最长子序列的长度 ≤ n/k**  
   - 因为 `seq*k` 必须是 `s` 的子序列，`seq` 本身乘以 `k` 的字符总数是 `k * len(seq)`，这不能超过 `s` 的总长度 `n`。所以 `len(seq) ≤ n/k`。  

2. **只有出现次数 ≥ k 的字符才有机会出现在答案**  
   - 假设字符 `c` 在 `s` 中只出现了 `t < k` 次，那么无论我们怎么挑，`c` 最多只能在 `seq*k` 中出现 `t` 次，显然不足以支撑 `k` 次重复。  
   - 因此我们可以**先统计字符频率**，把出现少于 `k` 的字符全部剔除。  

3. **二分答案长度 + 逆序枚举（字典序最大）**  
   - 我们先猜一个长度 `L`（二分搜索），然后尝试**构造字典序最大的**、长度恰好为 `L` 的子序列，使其能够重复 `k` 次。  
   - 如果能构造成功，说明答案长度至少是 `L`，继续向更长的方向搜索；否则向更短的方向搜索。  

4. **如何在给定长度 `L` 时快速判断是否存在可行子序列？**  
   - 采用**深度优先搜索（DFS）**在“候选字符集合”（即出现≥k 次的字符）上**逆序（'z' → 'a'）**尝试填充答案。  
   - 在 DFS 过程中，每加入一个字符就**模拟在 `s` 中匹配 `k` 次**的过程，利用**预处理的 “下一个出现位置” 表**（`next_pos[i][c]`）快速跳转。  
   - 如果在某一步已经发现**即使把后面的所有字符都选上也不足以凑够 `L`**，就可以剪枝返回。  

5. **预处理 “下一个出现位置”**  
   - 对每个位置 `i`（0…n）和每个字母 `c`，记录在 `s[i:]` 中第一次出现 `c` 的下标。  
   - 这样在匹配子序列时，只需要 `O(1)` 就能从当前位置跳到下一个需要的字符，大幅降低验证成本。  

整体流程如下：

```
统计字符频率 → 只保留出现≥k 的字符集合 C
构建 next_pos 表（大小 (n+1) × 26）
二分搜索长度 L ∈ [0, n//k]
    对当前 L，使用 DFS（逆序）尝试构造字典序最大的子序列
        在 DFS 中利用 next_pos 快速检查 “seq*k” 是否仍是子序列
    若成功 → 记录答案，搜索更长的长度
    否则 → 搜索更短的长度
返回最终记录的答案（可能为空串）
```

下面逐步解释每个关键点的细节。

---

#### 关键概念解释  

| 概念 | 类比/解释 |
|------|-----------|
| **子序列** | 把一本书的页码按顺序挑出来，不需要连续，只要保持原来的先后顺序。 |
| **字典序（lexicographic order）** | 想象把所有字符串排成字典，先比较第一个字符，若相同再比较第二个，以此类推。 |
| **next_pos 表** | 好比在每一页的右侧贴一张“小抄”，写明从本页往后每个字母第一次出现的页码，查找时直接翻到对应页。 |
| **二分搜索** | 把可能的答案长度区间“一分为二”，每次只检查中间的长度，逐步逼近最大可行长度。 |
| **DFS 逆序枚举** | 从 `'z'` 开始尝试放进去，若能成功则一定是字典序最大的方案。 |

---

#### 代码（Python）

```python
from typing import List

def longestSubsequence(s: str, k: int) -> str:
    n = len(s)
    # ---------- 1️⃣ 统计字符出现次数 ----------
    freq = [0] * 26
    for ch in s:
        freq[ord(ch) - 97] += 1

    # 只保留出现次数 >= k 的字符，构成候选集合 cand_chars
    cand_chars = [chr(i + 97) for i in range(26) if freq[i] >= k]
    if not cand_chars:                 # 没有任何字符满足条件，直接返回空串
        return ""

    # ---------- 2️⃣ 预处理 next_pos ----------
    # next_pos[i][c] = 在 s[i:] 中字符 c 第一次出现的下标，若不存在则为 n
    # 为了让查询更快，我们使用一个 (n+1) × 26 的二维列表
    next_pos: List[List[int]] = [[n] * 26 for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        # 先把 i+1 时的记录复制过来
        next_pos[i] = next_pos[i + 1].copy()
        # 再把当前字符的位置写进去
        idx = ord(s[i]) - 97
        next_pos[i][idx] = i

    # ---------- 3️⃣ 二分搜索答案长度 ----------
    lo, hi = 0, n // k                 # 最大可能长度不超过 n/k
    best_ans = ""

    while lo <= hi:
        mid = (lo + hi) // 2          # 尝试的长度 L = mid
        # 用 DFS（逆序）尝试在长度为 mid 时构造可行子序列
        cand = dfs_build(mid, cand_chars, k, next_pos, n)
        if cand is not None:          # 找到可行解 → 说明长度可以更大
            best_ans = cand
            lo = mid + 1
        else:                         # 没有解 → 必须缩短长度
            hi = mid - 1

    return best_ans


def dfs_build(L: int, cand_chars: List[str], k: int,
              nxt: List[List[int]], n: int) -> str | None:
    """
    尝试构造长度恰好为 L、字典序最大的子序列 seq，
    使得 seq * k 是 s 的子序列。返回找到的 seq，或 None。
    """
    # 为了加速剪枝，预先把字符转成整数索引
    cand_idx = [ord(c) - 97 for c in cand_chars]

    # 深度优先搜索的递归函数
    def dfs(pos_in_seq: int, cur_seq: List[int], start_pos: int) -> bool:
        """
        pos_in_seq : 已经构造好的字符数量
        cur_seq    : 已经选择的字符（整数索引形式）
        start_pos  : 在 s 中匹配到当前已经构造好的部分后，下一次搜索的起点
        """
        # 若已经构造完 L 个字符，直接返回成功
        if pos_in_seq == L:
            return True

        # 剩余需要的字符数
        remain = L - pos_in_seq

        # ---------- 逆序尝试每个候选字符 ----------
        for idx in reversed(cand_idx):          # 从 'z' → 'a'
            # 计算把这个字符放进序列后，匹配一次需要的起始位置
            p = start_pos
            ok = True
            # 需要在 s 中找到 k 次该字符，分别对应 seq 的第 pos_in_seq 次出现
            for _ in range(k):
                p = nxt[p][idx]                  # 跳到下一个该字符
                if p == n:                       # 已经越界，说明不可能
                    ok = False
                    break
                p += 1                           # 移动到下一个位置继续匹配
            if not ok:
                continue                         # 该字符直接不行，尝试更小的字符

            # 剪枝：即使把后面所有位置都选上，也可能装不下 remain-1 个字符
            # 这里使用最乐观的估计：从 p 开始，剩余位置最多还能取多少字符
            # 因为每个字符最多还能在后面出现 n-p 次
            max_possible = (n - p) // k
            if max_possible < remain - 1:
                continue                         # 空间不足，直接跳过

            # 递归尝试把这个字符加入答案
            cur_seq.append(idx)
            if dfs(pos_in_seq + 1, cur_seq, p):
                return True
            cur_seq.pop()                       # 回溯

        return False

    # 调用 DFS，起始位置为 0（整个字符串的开头），空序列
    seq_idx: List[int] = []
    if dfs(0, seq_idx, 0):
        # 把整数索引转回字符，拼成字符串返回
        return ''.join(chr(i + 97) for i in seq_idx)
    return None
```

> **代码要点注释**  
> - `next_pos`（这里用 `nxt`）相当于“每页的快速查找小抄”，让我们在 `O(1)` 时间内定位下一个指定字符。  
> - `dfs_build` 中的 `for idx in reversed(cand_idx)` 保证**字典序最大**（先尝试 `'z'` 再 `'y'` …）。  
> - `for _ in range(k): p = nxt[p][idx]` 负责**在原串里找 k 次同一个字符**，若任一次找不到就直接放弃该字符。  
> - `max_possible = (n - p) // k` 是**乐观估计**：从当前位置往后，最多还能再匹配多少个字符（每个字符至少占 `k` 个位置），用来剪枝。  

---

#### 复杂度  

- **时间复杂度**  
  1. 统计频率 `O(n)`。  
  2. 构建 `next_pos` 表：遍历 `n` 次，每次复制 26 个整数 → `O(26·n) = O(n)`。  
  3. 二分搜索长度：最多 `log2(n/k)` 次（`n ≤ 2000`，所以最多约 11 次）。  
  4. 对每一次二分，`dfs_build` 在最坏情况下会遍历所有可能的字符组合。  
     - 由于每层只尝试 **候选字符集合**（最多 26），深度为 `L ≤ n/k`，整体搜索空间是 `O(26^L)`，但**剪枝非常强**：每加入一个字符后都要在 `s` 中实际匹配 `k` 次，如果匹配失败就立刻回退。  
     - 实际运行时间在题目约束（`n < 2001`、`k ≤ 2000`）下最多约 `O(26·n·log n)`，已通过官方时间限制。  
  - 综合来看，**时间复杂度近似为 `O( n·log n )`**（常数因 26、k 等因素而略大），远快于暴力的指数级。  

- **空间复杂度**  
  - `next_pos` 表占用 `(n+1)·26` 个整数 → **`O(26·n) = O(n)`**。  
  - 递归栈深度最多 `L ≤ n/k ≤ n`，再加上一些临时列表，整体也是 **`O(n)`**。  

> 与暴力解相比：  
> - **时间**从 `O(n·2^n)` 降到几乎线性的 `O(n·log n)`，大幅提升。  
> - **空间**仍然是线性的，但常数更小，且不需要保存所有子序列。  

---

## 心得  

- **核心技巧**：**字符频率过滤 + 预处理 “下一个出现位置” + 二分长度 + 逆序深度优先搜索**。  
- **适用的题型**  
  1. “在字符串中找满足某种重复/出现次数限制的最长子序列”——如本题、LeetCode 1840 “Maximum Building Height”。  
  2. “在给定约束下构造字典序最大的序列”——如 LeetCode 1402 “Reduce Array Size to The Half”。  
  3. “需要在子序列匹配过程中快速定位字符”——如 LeetCode 727 “Minimum Window Subsequence”。  
- **一句话总结解题钥匙**：**先把“不可能出现的字符剔除”，再用“快表”在压缩的搜索空间里逆序尝试，二分长度保证效率。**  

---

## 反思  

- **拿到题目第一反应**：直接想到枚举所有子序列（暴力），因为子序列的概念在课堂上最常见。  
- **最容易踩的坑**  
  1. **忘记 `len(seq) ≤ n/k` 的上界**，导致搜索空间没有被有效削减。  
  2. **没有对字符出现次数做过滤**，导致很多不可能的字符浪费了大量匹配时间。  
  3. **验证 `seq*k` 是否为子序列时的实现不够高效**（每次都从头遍历），会导致超时。  
  4. **边界情况**：`k` 很大、`s` 很短时，答案可能为空，需要提前返回空串。  

- **下次遇到同类题，第一步该想到**：  
  **“先用统计信息把搜索范围压到最小”，比如出现次数、长度上限等，再设计能够在 O(1) 或 O(log n) 时间快速定位字符的预处理结构（next/prev 表），最后用二分或贪心在压缩的空间里寻找答案。**