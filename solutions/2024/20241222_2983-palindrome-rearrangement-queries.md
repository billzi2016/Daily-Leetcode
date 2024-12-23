# #2983. 回文重排查询 / Palindrome Rearrangement Queries

> 难度：困难 · 标签：Hash Table、String、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/palindrome-rearrangement-queries/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed string s having an even length n.
You are also given a 0-indexed 2D integer array, queries, where queries[i] = [ai, bi, ci, di].
For each query i, you are allowed to perform the following operations:
For each query, your task is to determine whether it is possible to make s a palindrome by performing the operations.
Each query is answered independently of the others.
Return a 0-indexed array answer, where answer[i] == true if it is possible to make s a palindrome by performing operations specified by the ith query, and false otherwise.

**Examples**

**Example 1:**

```
Input: s = "abcabc", queries = [[1,1,3,5],[0,2,5,5]]
Output: [true,true]
Explanation: In this example, there are two queries:
In the first query:
- a0 = 1, b0 = 1, c0 = 3, d0 = 5.
- So, you are allowed to rearrange s[1:1] => abcabc and s[3:5] => abcabc.
- To make s a palindrome, s[3:5] can be rearranged to become => abccba.
- Now, s is a palindrome. So, answer[0] = true.
In the second query:
- a1 = 0, b1 = 2, c1 = 5, d1 = 5.
- So, you are allowed to rearrange s[0:2] => abcabc and s[5:5] => abcabc.
- To make s a palindrome, s[0:2] can be rearranged to become => cbaabc.
- Now, s is a palindrome. So, answer[1] = true.
```

**Example 2:**

```
Input: s = "abbcdecbba", queries = [[0,2,7,9]]
Output: [false]
Explanation: In this example, there is only one query.
a0 = 0, b0 = 2, c0 = 7, d0 = 9.
So, you are allowed to rearrange s[0:2] => abbcdecbba and s[7:9] => abbcdecbba.
It is not possible to make s a palindrome by rearranging these substrings because s[3:6] is not a palindrome.
So, answer[0] = false.
```

**Example 3:**

```
Input: s = "acbcab", queries = [[1,2,4,5]]
Output: [true]
Explanation: In this example, there is only one query.
a0 = 1, b0 = 2, c0 = 4, d0 = 5.
So, you are allowed to rearrange s[1:2] => acbcab and s[4:5] => acbcab.
To make s a palindrome s[1:2] can be rearranged to become abccab.
Then, s[4:5] can be rearranged to become abccba.
Now, s is a palindrome. So, answer[0] = true.
```

**Constraints**

- 2 <= n == s.length <= 105
- 1 <= queries.length <= 105
- queries[i].length == 4
- ai == queries[i][0], bi == queries[i][1]
- ci == queries[i][2], di == queries[i][3]
- 0 <= ai <= bi < n / 2
- n / 2 <= ci <= di < n
- n is even.
- s consists of only lowercase English letters.

---

## 题目（中文翻译）

你得到一个下标从 **0** 开始的字符串 `s`，其长度为偶数 `n`。  
同时给定一个下标从 **0** 开始的二维整数数组 `queries`，其中 `queries[i] = [a_i, b_i, c_i, d_i]`。

对于每个查询 `i`，你可以对以下两个子串分别进行任意次字符重新排列（rearrange）操作：

- 子串 `s[a_i … b_i]`
- 子串 `s[c_i … d_i]`

每个查询之间互相独立。  
你的任务是判断：是否存在一种重新排列方式，使得在完成该查询规定的两段子串的重新排列后，整个字符串 `s` 成为回文串（palindrome）。  

返回一个下标从 **0** 开始的布尔数组 `answer`，其中 `answer[i]` 为 `true` 表示可以使 `s` 成为回文，`false` 表示不行。

---

### 示例

#### 示例 1
```text
Input: s = "abcabc", queries = [[1,1,3,5],[0,2,5,5]]
Output: [true,true]
Explanation: 该示例包含两个查询。
- 第一个查询：
  - a₀ = 1, b₀ = 1, c₀ = 3, d₀ = 5。
  - 可以重新排列子串 s[1:1]（即 "b"）和子串 s[3:5]（即 "abc"）。
  - 为了使 `s` 成为回文，可以把 s[3:5] 重新排列成 "cba"，得到字符串 "abccba"。
  - 此时 `s` 为回文，所以 answer[0] = true。
- 第二个查询：
  - a₁ = 0, b₁ = 2, c₁ = 5, d₁ = 5。
  - 可以重新排列子串 s[0:2]（即 "abc"）和子串 s[5:5]（即 "c"）。
  - 将 s[0:2] 重新排列为 "cba"，得到字符串 "cbaabc"。
  - 再把 s[5:5] 保持不变，整个字符串即为回文 "cbaabc"（即 "cbaabc" 本身就是回文）。
  - 因此 answer[1] = true。
```

#### 示例 2
```text
Input: s = "abbcdecbba", queries = [[0,2,7,9]]
Output: [false]
Explanation: 该示例只有一个查询。
- a₀ = 0, b₀ = 2, c₀ = 7, d₀ = 9。
- 可以重新排列子串 s[0:2]（即 "abb"）和子串 s[7:9]（即 "bba"）。
- 即使对这两个子串进行任意重新排列，中心子串 s[3:6]（即 "cdec"）仍无法成为回文，导致整体字符串无法成为回文。
- 所以 answer[0] = false。
```

#### 示例 3
```text
Input: s = "acbcab", queries = [[1,2,4,5]]
Output: [true]
Explanation: 该示例只有一个查询。
- a₀ = 1, b₀ = 2, c₀ = 4, d₀ = 5。
- 可以重新排列子串 s[1:2]（即 "cb"）和子串 s[4:5]（即 "ab"）。
- 将 s[1:2] 重新排列为 "bc"，得到 "abccab"。
- 再将 s[4:5] 重新排列为 "ba"，得到 "abccba"，此时字符串为回文。
- 因此 answer[0] = true。
```

---

### 约束条件
- `2 <= n == s.length <= 10^5`
- `1 <= queries.length <= 10^5`
- `queries[i].length == 4`
- `a_i = queries[i][0]`, `b_i = queries[i][1]`
- `c_i = queries[i][2]`, `d_i = queries[i][3]`
- `0 <= a_i <= b_i < n / 2`
- `n / 2 <= c_i <= d_i < n`
- `n` 为偶数
- `s` 仅由小写英文字母组成

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

把题目想成“把左半边和右半边对应位置配对”。  
- **固定位置**：如果某个下标 `i` 不在左区间 `[a,b]`，而它的对称下标 `j = n‑1‑i` 也不在右区间 `[c,d]`，这两个字符是 **不能动** 的，必须原本就相同。  
- **单侧可动**：如果 `i` 在左区间而 `j` 不在右区间，说明我们只能在左区间里挑出一个字符来和右边的 `s[j]` 配对，同理右区间单侧可动的情况也一样。  
- **双侧可动**：如果 `i` 在左区间且 `j` 在右区间，两边都可以随意换位，只要左区间和右区间的字符种类与数量最终能够两两对应即可。

最直接的办法就是 **遍历整个字符串**，把左区间、右区间的字符统计出来（用 26 长的数组表示字母出现次数），再把“单侧可动”需要的字符从对应的统计里扣除，最后比较两侧剩余的字符计数是否相同。  

> **类比**：把左区间的字符想成一盒“左边的字母”，右区间是一盒“右边的字母”。  
> - 固定位置相当于已经贴好标签的配对，必须先检查是否已经匹配。  
> - 单侧可动相当于左盒子里必须拿出和右边固定字符相同的字母来贴标签。  
> - 双侧可动则只要求两盒子里剩下的字母能够一一对应（盒子里各有多少种、多少个就必须相同）。  

只要把这些规则逐一实现，就能得到答案。  

#### 代码（Python）

```python
from typing import List

def can_make_palindrome_bruteforce(s: str, queries: List[List[int]]) -> List[bool]:
    n = len(s)
    half = n // 2
    ans = []

    for a, b, c, d in queries:
        # 统计左区间、右区间的字符出现次数（26 个字母）
        left_cnt = [0] * 26
        right_cnt = [0] * 26
        for i in range(a, b + 1):
            left_cnt[ord(s[i]) - ord('a')] += 1
        for i in range(c, d + 1):
            right_cnt[ord(s[i]) - ord('a')] += 1

        possible = True

        # 1️⃣ 检查固定位置是否已经匹配
        for i in range(half):
            j = n - 1 - i
            in_left = a <= i <= b
            in_right = c <= j <= d
            if not in_left and not in_right:          # 双侧都不能动
                if s[i] != s[j]:
                    possible = False
                    break

        if not possible:
            ans.append(False)
            continue

        # 2️⃣ 单侧可动：左区间需要补齐右侧固定字符
        for i in range(half):
            j = n - 1 - i
            if a <= i <= b and not (c <= j <= d):      # 只左侧可动
                idx = ord(s[j]) - ord('a')
                left_cnt[idx] -= 1                     # 用掉左区间的一个该字符
                if left_cnt[idx] < 0:                  # 不够用，直接失败
                    possible = False
                    break

        if not possible:
            ans.append(False)
            continue

        # 3️⃣ 单侧可动：右区间需要补齐左侧固定字符
        for i in range(half):
            j = n - 1 - i
            if not (a <= i <= b) and (c <= j <= d):    # 只右侧可动
                idx = ord(s[i]) - ord('a')
                right_cnt[idx] -= 1
                if right_cnt[idx] < 0:
                    possible = False
                    break

        if not possible:
            ans.append(False)
            continue

        # 4️⃣ 双侧可动：两侧剩余字符计数必须完全相同
        if left_cnt != right_cnt:
            possible = False

        ans.append(possible)

    return ans
```

> **关键行注释**  
> - `left_cnt`、`right_cnt` 用 **哈希表**（这里用长度为 26 的数组）来记录每个字母出现次数，类似查字典的过程：`key` 是字母，`value` 是出现次数。  
> - `left_cnt[idx] -= 1` 表示“把左区间里已经用掉的那个字符从统计里减掉”。  

#### 复杂度  

- **时间复杂度**：`O(q * n)`（`q` 为查询数，`n` 为字符串长度）。  
  - 解释：对每个查询我们要遍历整条字符串（检查固定位置、单侧可动），最坏情况是 `n` 步操作。  
  - 对于 `n = 10⁵，q = 10⁵` 这种规模会导致 10¹⁰ 次操作，显然会超时。  
- **空间复杂度**：`O(1)`（只用了常数个长度为 26 的数组），不随 `n`、`q` 增长。

---

### 2. 最优解  

#### 思路  

暴力解的 **瓶颈** 在于每个查询都要 **遍历整条字符串**。  
要把它降到 `O(1)`（或 `O(26)`) 每查询，只需要把“区间内字符出现次数”的统计提前准备好，**一次预处理后**即可在常数时间内得到任意区间的计数。

这正是 **前缀和 + 哈希表**（这里仍然是 26 长数组）可以帮我们做到的：

1. **前缀计数**  
   对每个字母 `ch ∈ [a..z]`，建立一个长度为 `n+1` 的数组 `pref[ch][i]`，表示 `s[0:i]`（左闭右开）中字母 `ch` 出现的次数。  
   这样，任意区间 `[l, r]`（含左右端点）的出现次数可以用  
   `cnt(ch, l, r) = pref[ch][r+1] - pref[ch][l]`  
   在 **O(1)** 时间内得到。

2. **固定位置是否匹配**  
   只要检查左半边 `i` **既不在左区间 `[a,b]`，也不在右区间的镜像 `[n-1-d, n-1-c]`** 的位置是否已经相等。  
   为此我们预处理一个 **不匹配前缀和** `mis[i]`（`i` 只遍历左半边）：
   ```python
   mis[i] = 1 if s[i] != s[n-1-i] else 0
   prefMis[i+1] = prefMis[i] + mis[i]
   ```
   任意区间的“不匹配数”同样可以 O(1) 查询。  
   对当前查询，固定位置的集合是左半边去掉 `L = [a,b]` 与 `M = [n-1-d, n-1-c]` 两个区间的交集。  
   用前缀和可以快速算出 **这些位置的不匹配数是否为 0**。

3. **单侧可动需要的字符**  
   - 左侧需要补齐的字符正好是右半边 **镜像左区间** `J = [n-1-b, n-1-a]` 中、但不在右区间 `[c,d]` 的字符。  
   - 右侧需要补齐的字符是左半边 **镜像右区间** `I = [n-1-d, n-1-c]` 中、但不在左区间 `[a,b]` 的字符。  

   这两个集合都是 **连续区间**（可能与另一个区间有交集），所以它们的字符频率同样可以用前缀计数 O(1) 获得。  
   记  
   ```python
   needL = freq(J) - freq(J ∩ R)   # 左侧必须提供的字符
   needR = freq(I) - freq(I ∩ L)   # 右侧必须提供的字符
   ```

4. **双侧可动的剩余字符必须相等**  
   - 先得到左区间 `[a,b]`、右区间 `[c,d]` 的字符计数 `cntL`、`cntR`（同样用前缀计数）。  
   - 从 `cntL` 中减去 `needL`，从 `cntR` 中减去 `needR`。如果在减的过程中出现负数，说明对应的可动区间里没有足够的字符来匹配固定对侧字符，直接返回 `false`。  
   - 最后检查两侧剩余计数数组是否完全相同；相同即说明双侧可动的字符可以自由配对，答案为 `true`。

整个过程每个查询只涉及 **常数次区间计数查询**（26 个字母），时间复杂度是 `O(26) ≈ O(1)`，空间只需要 `26 * (n+1)` 的前缀数组。

> **类比**：  
> - 前缀计数就像一本“字典”，把整本书（字符串）每一页（下标）之前出现的单词（字母）数量都记录下来，之后想查任意章节（区间）出现多少次，只需要看两页的差值。  
> - “需要的字符”相当于从左盒子里挑出必须给右盒子固定伙伴的那几颗糖，先把这几颗糖算出来，再看剩下的糖能否两盒子完全配对。

#### 代码（Python）

```python
from typing import List

ALPH = 26  # 小写英文字母个数

def build_prefix_counts(s: str):
    """返回一个 26 x (n+1) 的前缀计数矩阵"""
    n = len(s)
    pref = [[0] * (n + 1) for _ in range(ALPH)]
    for i, ch in enumerate(s):
        idx = ord(ch) - ord('a')
        for c in range(ALPH):
            pref[c][i + 1] = pref[c][i] + (1 if c == idx else 0)
    return pref

def range_freq(pref, l: int, r: int):
    """返回区间 [l, r]（含）里每个字母的出现次数，长度 26 的列表"""
    res = [0] * ALPH
    for c in range(ALPH):
        res[c] = pref[c][r + 1] - pref[c][l]
    return res

def build_mismatch_prefix(s: str):
    """只遍历左半边，记录 s[i] 与其对称字符是否不相等的前缀和"""
    n = len(s)
    half = n // 2
    pref = [0] * (half + 1)
    for i in range(half):
        pref[i + 1] = pref[i] + (1 if s[i] != s[n - 1 - i] else 0)
    return pref

def mismatch_in_interval(pref_mis, l: int, r: int) -> int:
    """左半边区间 [l, r]（含）里不匹配的数量"""
    if l > r:
        return 0
    return pref_mis[r + 1] - pref_mis[l]

def interval_intersection(l1, r1, l2, r2):
    """返回两个闭区间的交集，若无交集返回 (0, -1)（空区间）"""
    l = max(l1, l2)
    r = min(r1, r2)
    if l > r:
        return (0, -1)
    return (l, r)

def can_make_palindrome_optimal(s: str, queries: List[List[int]]) -> List[bool]:
    n = len(s)
    half = n // 2

    # 1️⃣ 前缀计数（每个字母 26 列）
    pref = build_prefix_counts(s)

    # 2️⃣ 不匹配前缀和，仅在左半边建立
    pref_mis = build_mismatch_prefix(s)

    ans = []

    for a, b, c, d in queries:
        # ---------- ① 固定位置必须已经匹配 ----------
        # 左半边不在左区间且不在右区间的镜像区间
        # 镜像右区间 M = [n-1-d, n-1-c]（在左半边）
        m_l, m_r = n - 1 - d, n - 1 - c
        # 计算“左半边固定位置”的不匹配数量：
        # total_mis - (左区间 or 镜像右区间) 中的 mismatches
        total_mis = pref_mis[half]                     # 左半边所有不匹配的数量
        # 左区间 [a,b] 的不匹配数
        mis_left = mismatch_in_interval(pref_mis, a, b)
        # 镜像右区间 [m_l, m_r] 的不匹配数
        mis_mirror = mismatch_in_interval(pref_mis, m_l, m_r)
        # 两者交集的不匹配数（因为前面会被加两次，需要减一次）
        inter_l, inter_r = interval_intersection(a, b, m_l, m_r)
        mis_inter = mismatch_in_interval(pref_mis, inter_l, inter_r)
        # 只在固定位置的不匹配数
        fixed_mis = total_mis - (mis_left + mis_mirror - mis_inter)

        if fixed_mis != 0:          # 有固定位置不相等，直接否
            ans.append(False)
            continue

        # ---------- ② 统计区间字符频率 ----------
        cntL = range_freq(pref, a, b)        # 左区间
        cntR = range_freq(pref, c, d)        # 右区间

        # 镜像左区间 J = [n-1-b, n-1-a]（在右半边）
        j_l, j_r = n - 1 - b, n - 1 - a
        # 镜像右区间 I = [n-1-d, n-1-c]（在左半边）
        i_l, i_r = n - 1 - d, n - 1 - c

        # ---------- ③ 计算单侧可动需要的字符 ----------
        # 需要左侧提供的字符 = J 中不在右区间的字符
        freq_J = range_freq(pref, j_l, j_r)
        # J 与右区间的交集
        inter_J_R_l, inter_J_R_r = interval_intersection(j_l, j_r, c, d)
        freq_JR = range_freq(pref, inter_J_R_l, inter_J_R_r) if inter_J_R_l <= inter_J_R_r else [0]*ALPH
        needL = [freq_J[k] - freq_JR[k] for k in range(ALPH)]

        # 需要右侧提供的字符 = I 中不在左区间的字符
        freq_I = range_freq(pref, i_l, i_r)
        inter_I_L_l, inter_I_L_r = interval_intersection(i_l, i_r, a, b)
        freq_IL = range_freq(pref, inter_I_L_l, inter_I_L_r) if inter_I_L_l <= inter_I_L_r else [0]*ALPH
        needR = [freq_I[k] - freq_IL[k] for k in range(ALPH)]

        # ---------- ④ 从区间计数中扣除这些需求 ----------
        possible = True
        for k in range(ALPH):
            cntL[k] -= needL[k]
            cntR[k] -= needR[k]
            if cntL[k] < 0 or cntR[k] < 0:   # 需求超过了区间本身的供应
                possible = False
                break

        if not possible:
            ans.append(False)
            continue

        # ---------- ⑤ 双侧可动的剩余字符必须完全相同 ----------
        if cntL != cntR:
            possible = False

        ans.append(possible)

    return ans
```

> **代码要点说明**  
> 1. `build_prefix_counts` 把每个字符的前缀计数放在二维数组里，后面 **任意区间** 的字符频率只需要两次减法。  
> 2. `pref_mis` 用来快速判断“固定位置是否已经相等”。  
> 3. `interval_intersection` 负责求两个闭区间的交集，帮助我们把 “只在左区间但不在右区间” 这类集合转成 **连续区间**，便于使用前缀计数。  
> 4. 最后只比较两个长度为 26 的数组是否相同，时间常数非常小。

#### 复杂度  

- **时间复杂度**：`O(q * 26) = O(q)`，因为每个查询只做 26 次常数操作（遍历字母表）。  
  - 与暴力解 `O(q·n)` 相比，**把遍历字符串的代价降到了常数**。  
- **空间复杂度**：`O(26·n)` 用于前缀计数矩阵 + `O(n)` 用于不匹配前缀和，整体仍是线性 `O(n)`，在题目限制 `n ≤ 10⁵` 以内完全可接受。

---

## 心得  

- **核心技巧**：**前缀和 + 区间字符计数**。把“区间里有多少个 a、b、c …”预先算好，查询时只需要 O(1) 即可得到。  
- **适用的题型**  
  1. “区间能否重新排列成回文/同构” 类问题（如 LeetCode 1512、1657）。  
  2. “区间内字符出现次数是否满足某种约束” 的查询题（如 “字符串查询是否为回文”）。  
- **解题钥匙**：把所有**可动**的字符视为“资源池”，把**固定**的配对视为“需求”，只要资源池能恰好满足需求且剩余资源两侧相等，答案就为 `True`。

---

## 反思  

- **第一反应**：看到“可以任意重排子串”，立刻想到**统计字符出现次数**，因为重排不改变字符种类与数量。  
- **最容易踩的坑**  
  1. **忘记检查固定位置**：即两侧都不在可动区间时必须原本相等。  
  2. **需求超出供应**：单侧可动时，需要的字符可能在对应区间里根本没有，导致负数计数。  
  3. **区间交集的处理**：左侧需求要排除已经在右侧可动的那部分，否则会多扣一次。  
- **下次类似题**：第一步先**划分三类位置**（双侧固定、单侧可动、双侧可动），再**用前缀和把每类的字符计数快速取出**，最后比较资源与需求是否匹配。这样思路清晰，代码也容易写对。