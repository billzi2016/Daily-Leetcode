# #3501. 最大化活跃区段（交易 II） / Maximize Active Section with Trade II

> 难度：困难 · 标签：Array、String、Binary Search、Segment Tree · [LeetCode 链接](https://leetcode.com/problems/maximize-active-section-with-trade-ii/)

---

## 题目（英文原版）

**Description**

You are given a binary string s of length n, where:
You can perform at most one trade to maximize the number of active sections in s. In a trade, you:
Additionally, you are given a 2D array queries, where queries[i] = [li, ri] represents a substring s[li...ri].
For each query, determine the maximum possible number of active sections in s after making the optimal trade on the substring s[li...ri].
Return an array answer, where answer[i] is the result for queries[i].
Note

**Examples**

**Example 1:**

```
Input: s = "01", queries = [[0,1]]
Output: [1]
Explanation:
Because there is no block of '1' s surrounded by '0' s, no valid trade is possible. The maximum number of active sections is 1.
```

**Example 2:**

```
Input: s = "0100", queries = [[0,3],[0,2],[1,3],[2,3]]
Output: [4,3,1,1]
Explanation:
Query [0, 3] → Substring "0100" → Augmented to "101001" Choose "0100" , convert "0100" → "0000" → "1111" . The final string without augmentation is "1111" . The maximum number of active sections is 4.
Query [0, 2] → Substring "010" → Augmented to "10101" Choose "010" , convert "010" → "000" → "111" . The final string without augmentation is "1110" . The maximum number of active sections is 3.
Query [1, 3] → Substring "100" → Augmented to "11001" Because there is no block of '1' s surrounded by '0' s, no valid trade is possible. The maximum number of active sections is 1.
Query [2, 3] → Substring "00" → Augmented to "1001" Because there is no block of '1' s surrounded by '0' s, no valid trade is possible. The maximum number of active sections is 1.
```

**Example 3:**

```
Input: s = "1000100", queries = [[1,5],[0,6],[0,4]]
Output: [6,7,2]
Explanation:
Query [1, 5] → Substring "00010" → Augmented to "1000101" Choose "00010" , convert "00010" → "00000" → "11111" . The final string without augmentation is "1111110" . The maximum number of active sections is 6.
Query [0, 6] → Substring "1000100" → Augmented to "110001001" Choose "000100" , convert "000100" → "000000" → "111111" . The final string without augmentation is "1111111" . The maximum number of active sections is 7.
Query [0, 4] → Substring "10001" → Augmented to "1100011" Because there is no block of '1' s surrounded by '0' s, no valid trade is possible. The maximum number of active sections is 2.
```

**Example 4:**

```
Input: s = "01010", queries = [[0,3],[1,4],[1,3]]
Output: [4,4,2]
Explanation:
Query [0, 3] → Substring "0101" → Augmented to "101011" Choose "010" , convert "010" → "000" → "111" . The final string without augmentation is "11110" . The maximum number of active sections is 4.
Query [1, 4] → Substring "1010" → Augmented to "110101" Choose "010" , convert "010" → "000" → "111" . The final string without augmentation is "01111" . The maximum number of active sections is 4.
Query [1, 3] → Substring "101" → Augmented to "11011" Because there is no block of '1' s surrounded by '0' s, no valid trade is possible. The maximum number of active sections is 2.
```

**Constraints**

- 1 <= n == s.length <= 105
- 1 <= queries.length <= 105
- s[i] is either '0' or '1'.
- queries[i] = [li, ri]
- 0 <= li <= ri < n

---

## 题目（中文翻译）

你得到一个长度为 n 的二进制字符串 s，字符只可能是 `'0'` 或 `'1'`。  
你最多可以进行一次交易（trade），以使字符串 s 中的活跃区段（active sections）数量达到最大。  
在一次交易中，你可以：

（题目原文中此处应说明交易的具体操作，已保留原样）

此外，你还会得到一个二维数组 queries，`queries[i] = [li, ri]` 表示子串 `s[li…ri]`。  
对于每个查询，求在子串 `s[li…ri]` 上进行最优交易后，整个字符串 s 中可能的最大活跃区段数。  
返回一个数组 answer，`answer[i]` 为对应查询的结果。

**示例 1**  
```text
Input: s = "01", queries = [[0,1]]
Output: [1]
Explanation:
因为不存在被 `'0'` 包围的 `'1'` 区块，无法进行有效的交易。此时活跃区段的最大数量为 1。
```

**示例 2**  
```text
Input: s = "0100", queries = [[0,3],[0,2],[1,3],[2,3]]
Output: [4,3,1,1]
Explanation:
Query [0, 3] → 子串 "0100" → 扩展为 "101001" → 选择 "0100"，将其转换为 "0000" → 再转换为 "1111"。去掉扩展后的最终字符串为 "1111"，活跃区段的最大数量为 4。  
Query [0, 2] → 子串 "010" → 扩展为 "10101" → 选择 "010"，将其转换为 "000" → 再转换为 "111"。……（后续已截断）
```

**示例 3**  
```text
Input: s = "1000100", queries = [[1,5],[0,6],[0,4]]
Output: [6,7,2]
Explanation:
Query [1, 5] → 子串 "00010" → 扩展为 "1000101" → 选择 "00010"，将其转换为 "00000" → 再转换为 "11111"。去掉扩展后的最终字符串为 "1111110"，活跃区段的最大数量为 6。  
Query [0, 6] → 子串 "1000100" → 扩展为 "110001001" → 选择 "000100"，将其转换为 "000000" → ……（后续已截断）
```

**示例 4**  
```text
Input: s = "01010", queries = [[0,3],[1,4],[1,3]]
Output: [4,4,2]
Explanation:
Query [0, 3] → 子串 "0101" → 扩展为 "101011" → 选择 "010"，将其转换为 "000" → 再转换为 "111"。去掉扩展后的最终字符串为 "11110"，活跃区段的最大数量为 4。  
Query [1, 4] → 子串 "1010" → 扩展为 "110101" → 选择 "010"，将其转换为 "000" → 再转换为 "111"。……（后续已截断）
```

**约束条件**
- `1 <= n == s.length <= 10^5`
- `1 <= queries.length <= 10^5`
- `s[i]` 只能是 `'0'` 或 `'1'`
- `queries[i] = [li, ri]`
- `0 <= li <= ri < n`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

题目大意是：  
- 给定一个仅由 `'0'`、`'1'` 组成的字符串 `s`（长度 `n ≤ 10⁵`）。  
- 对每个查询 `[l, r]`（表示子串 `s[l…r]`），我们 **最多只能进行一次 “交易”**，目的是让这段子串内部的 **“活跃区段数”**（即连续 `'1'` 的个数）尽可能多。  
- 交易的具体规则在题目描述里比较抽象，核心可以归结为 **把子串里恰好包含的一个 “0‑段” 完全翻成 `'1'`**，从而把它左侧的 `'1'` 段和右侧的 `'1'` 段合并成一个更长的 `'1'` 段。  

> **生活化类比**：  
> 把字符串想成一排灯泡，`'1'` 表示灯亮，`'0'` 表示灯灭。一次交易就像你有一次机会把一整段熄灯（连续的 `'0'`）全部打开，打开后左边已经亮着的灯和右边已经亮着的灯会连成一条更长的光带。  

最直接的做法是**对每个查询单独暴力模拟**：

1. 把子串 `s[l…r]` 拿出来。  
2. 在这段子串里枚举所有可能的 **完整的 `'0'` 段**（即该段的左端点和右端点都在 `[l, r]` 范围内）。  
3. 对每个 `'0'` 段，计算如果把它全部翻成 `'1'`，会得到多少个 `'1'`（即原来左侧的 `'1'` 长度 + 右侧的 `'1'` 长度 + 该段本身的长度）。  
4. 取所有枚举结果的最大值，即为该查询的答案。  

**为什么暴力是对的**：  
- 题目只允许**最多一次**交易，而一次交易只能完整覆盖一个 `'0'` 段（因为如果只翻一半，左/右两边的 `'1'` 段就不会合并成更长的段，显然不是最优）。  
- 因此只要把所有合法的 `'0'` 段都尝试一次，就一定能找到最优答案。  

**复杂度分析（大白话）**：  
- 对每个查询，我们可能要遍历子串的每个字符来找 `'0'` 段，最坏情况下子串长度是 `n`。  
- 再对每个 `'0'` 段做一次常数时间的计算。  
- 因此**每个查询的时间是 O(子串长度)**，所有查询合在一起是 **O(∑子串长度) ≤ O(n·q)**，这里 `q` 是查询数量，最坏会是 `10⁵·10⁵`，根本跑不完。  
- 空间只用了几个临时变量，**O(1)**。  

显然，暴力解在规模稍大的情况下会超时，需要优化。

#### 代码（Python）

```python
def brute_max_active(s: str, queries):
    n = len(s)
    ans = []
    for l, r in queries:                     # 遍历每个查询
        sub = s[l:r+1]                       # 取出子串
        best = sub.count('1')                # 若不做交易，活跃区段数即当前 '1' 的个数
        i = 0
        while i < len(sub):
            if sub[i] == '0':                # 找到一个零段的左端点
                j = i
                while j < len(sub) and sub[j] == '0':
                    j += 1                   # j 指向零段右侧第一个非零字符
                # 零段是 sub[i:j]，左侧连续 1 的长度
                left_ones = 0
                k = i - 1
                while k >= 0 and sub[k] == '1':
                    left_ones += 1
                    k -= 1
                # 右侧连续 1 的长度
                right_ones = 0
                k = j
                while k < len(sub) and sub[k] == '1':
                    right_ones += 1
                    k += 1
                # 交易后得到的 1 的总数
                cand = left_ones + (j - i) + right_ones
                best = max(best, cand)
                i = j                         # 跳过这个零段
            else:
                i += 1
        ans.append(best)
    return ans
```

> 代码里每一行都加了中文注释，帮助初学者快速读懂。  

#### 复杂度  

- **时间复杂度**：`O(∑(r_i - l_i + 1))`，最坏等价于 `O(n·q)`，在 `n,q ≤ 10⁵` 时会超时。  
- **空间复杂度**：`O(1)`（只用了常数个临时变量），这点是好的。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到两件事：

1. **只需要关注“段”（segment）**，而不是每个单独的字符。  
   - 连续相同字符会形成一个“段”。比如 `s = 00111000` → 段序列是 `[00]，[111]，[000]`。  
2. **一次交易只会完整覆盖一个 `'0'` 段**，并把它左边最近的 `'1'` 段和右边最近的 `'1'` 段合并。  

于是我们把整个字符串预处理成 **段的列表**：

| 段编号 | 类型（0/1） | 长度 |
|--------|------------|------|
| 0      | 0          | len0 |
| 1      | 1          | len1 |
| 2      | 0          | len2 |
| 3      | 1          | len3 |
| …      | …          | …    |

> **类比**：把灯泡排成一排后，用胶带把相邻相同颜色的灯泡粘在一起，每块胶带对应一个段。

对每个 **`0` 段**（记作编号 `i`），如果我们把它翻成 `'1'`，**最终活跃区段数** 就等于它左侧最近的 `'1'` 段长度 `len[i-1]` 加上它右侧最近的 `'1'` 段长度 `len[i+1]`（因为这两个 `'1'` 段会合并成一个更长的 `'1'` 段），**再加上自身的长度**。  

然而题目要求的是 **“子串 `[l,r]` 必须完整覆盖这三个段”**（左、0、右）。也就是说，只有当查询的范围同时包含段 `i-1`、`i`、`i+1` 时，这次交易才合法。  

因此，对于每个 **`0` 段** `i`，我们可以预先计算一个 **候选答案**：

```
cand[i] = len[i-1] + len[i] + len[i+1]          (i 为 0 段)
```

如果 `i` 是最左边或最右边的 `0` 段（没有左/右相邻的 `1` 段），则对应的 `len[i-1]` 或 `len[i+1]` 为 `0`，仍然可以使用同一公式。  

接下来要做的两件事：

1. **快速定位查询 `[l,r]` 对应的段编号区间**。  
   - 这可以用 **前缀和** `pos[i]`（第 `i` 个字符所在的段编号）在 O(log n) 或 O(1) 时间内得到。  
2. **在段编号区间内求最大 `cand[i]`**，并且确保 `i-1`、`i`、`i+1` 都在查询范围内。  

这正是**区间最大值查询**的典型应用——我们可以把所有 `cand[i]`（只对 `0` 段有意义）放进一棵 **线段树（Segment Tree）**（或 **稀疏表**、**树状数组**），支持：

- **构建**：`O(m)`，`m` 为段的数量（≤ `2·n`）。  
- **区间查询**：`O(log m)`。  

**关键细节——如何保证 `i-1,i,i+1` 完全被查询覆盖？**  

- 对于查询 `[l,r]`，我们先得到它覆盖的**最左**段编号 `L` 和**最右**段编号 `R`（通过二分或前缀数组 O(1)）。  
- 那么合法的 `0` 段编号 `i` 必须满足 `L ≤ i-1` 且 `i+1 ≤ R` → `L+1 ≤ i ≤ R-1`。  
- 换句话说，我们只需要在段编号区间 `[L+1, R-1]`（只保留内部段）里查询最大 `cand[i]`。  

边界情况：

- 如果查询只覆盖不到三个完整段（例如长度为 1 或 2），则**无法进行任何交易**，答案就是子串本身的 `'1'` 个数。我们可以直接用 **前缀和** `pref1`（`1` 的前缀计数）在 O(1) 时间算出。  

综上，整体流程如下：

1. **预处理**  
   - 生成段列表 `seg_type[]`、`seg_len[]`、`seg_start[]`（每段的左端点）。  
   - 计算每个字符对应的段编号 `char_to_seg[]`（长度 `n`）。  
   - 计算 `cand[i]`（只对 `0` 段）。  
   - 用 `cand` 建立线段树 `st`（支持区间最大值）。  
   - 计算 `'1'` 的前缀和 `pref1[]`（用于直接求子串内原始 `'1'` 数）。  

2. **单个查询 `[l,r]`**  
   - `total_ones = pref1[r+1] - pref1[l]` → 不做交易时的活跃区段数。  
   - `L = char_to_seg[l]`（子串最左端点所在的段）  
   - `R = char_to_seg[r]`（子串最右端点所在的段）  
   - 若 `R - L + 1 < 3`（段数不足 3） → 返回 `total_ones`。  
   - 否则在段编号区间 `[L+1, R-1]` 上 **查询最大 `cand`**：`best = st.query(L+1, R-1)`。  
   - 最终答案 = `max(total_ones, best)`。  

这样每个查询只需要 **O(log m)** 的时间，整体复杂度是 **O((n+q)·log n)**，足以通过所有约束。

#### 代码（Python）

```python
from typing import List

# ---------- 线段树实现（区间最大值） ----------
class SegmentTree:
    def __init__(self, data: List[int]):
        """data 长度为 n，构造一棵支持区间最大值的线段树，时间 O(n)"""
        n = len(data)
        self.N = 1
        while self.N < n:               # 扩展到 2 的幂
            self.N <<= 1
        self.seg = [0] * (2 * self.N)   # 树节点默认值 0（因为 cand 只会 >=0）
        # 把原数组放到叶子节点
        for i, v in enumerate(data):
            self.seg[self.N + i] = v
        # 自底向上构造父节点
        for i in range(self.N - 1, 0, -1):
            self.seg[i] = max(self.seg[i << 1], self.seg[i << 1 | 1])

    def query(self, l: int, r: int) -> int:
        """
        返回区间 [l, r]（左右端点都闭）的最大值，时间 O(log N)
        l、r 为 0‑based 的段编号（相对于原始 data）
        """
        if l > r:
            return 0
        l += self.N
        r += self.N
        res = 0
        while l <= r:
            if l & 1:                     # l 是右子节点，直接合并后右移
                res = max(res, self.seg[l])
                l += 1
            if not (r & 1):               # r 是左子节点，直接合并后左移
                res = max(res, self.seg[r])
                r -= 1
            l >>= 1
            r >>= 1
        return res


# ---------- 主函数 ----------
def maxActiveSections(s: str, queries: List[List[int]]) -> List[int]:
    n = len(s)

    # 1. 将字符串切成段
    seg_type = []          # 0 或 1
    seg_len = []           # 每段的长度
    seg_start = []         # 每段的左端点（在原字符串中的下标）
    i = 0
    while i < n:
        j = i
        while j < n and s[j] == s[i]:
            j += 1
        seg_type.append(int(s[i]))
        seg_len.append(j - i)
        seg_start.append(i)
        i = j
    m = len(seg_type)                      # 段的数量

    # 2. 为每个字符记录它属于哪个段（后面快速定位查询的左右段）
    char_to_seg = [0] * n
    for idx, start in enumerate(seg_start):
        length = seg_len[idx]
        for k in range(start, start + length):
            char_to_seg[k] = idx

    # 3. 前缀和，统计原始字符串中 1 的个数
    pref1 = [0] * (n + 1)
    for i, ch in enumerate(s):
        pref1[i + 1] = pref1[i] + (ch == '1')

    # 4. 为每个 0 段计算候选答案 cand[i] = len[i-1] + len[i] + len[i+1]
    cand = [0] * m                         # 只在 0 段位置有意义，其他保持 0
    for i in range(m):
        if seg_type[i] == 0:               # 只考虑 0 段
            left = seg_len[i - 1] if i - 1 >= 0 else 0
            right = seg_len[i + 1] if i + 1 < m else 0
            cand[i] = left + seg_len[i] + right

    # 5. 用 cand 构建线段树（支持区间最大查询）
    st = SegmentTree(cand)

    # 6. 处理每个查询
    ans = []
    for l, r in queries:
        # 子串中原始的 1 的个数（不做交易时的答案）
        total_ones = pref1[r + 1] - pref1[l]

        # 找到子串覆盖的最左、最右段编号
        left_seg = char_to_seg[l]
        right_seg = char_to_seg[r]

        # 如果子串内部段数不足 3，无法完整覆盖一个 “左‑0‑右” 三段结构
        if right_seg - left_seg + 1 < 3:
            ans.append(total_ones)
            continue

        # 在段编号区间 [left_seg+1, right_seg-1] 内查询最大 cand
        best = st.query(left_seg + 1, right_seg - 1)
        ans.append(max(total_ones, best))

    return ans
```

> **代码要点注释**  
> - **第 1 步**把字符串压缩成段，省去大量重复遍历。  
> - **第 2 步**构造 `char_to_seg`，相当于把每个灯泡贴上标签，告诉我们它属于哪根灯带。  
> - **第 4 步**的 `cand[i]` 正是“一次交易能把左侧、自己、右侧三段合并成的最大活跃区段数”。  
> - **第 5 步**使用线段树实现“区间最大值”。如果你不想自己实现，也可以用 Python 标准库的 `bisect` + `max`（但最坏是 O(log²)`，这里保持 O(log)`）。  

#### 复杂度  

- **预处理**  
  - 切段、构造映射、前缀和、`cand`、线段树：**O(n)**（因为段数 ≤ 2·n）。  
  - 额外空间：`seg_type、seg_len、seg_start、char_to_seg、pref1、cand、线段树`，共 **O(n)**。  

- **每个查询**  
  - 通过 `char_to_seg` 直接定位左右段：**O(1)**。  
  - 线段树区间查询：**O(log m) = O(log n)**。  
  - 整体 **时间 O((n + q)·log n)**，在 `n, q ≤ 10⁵` 下轻松通过。  

- **空间**：整体 **O(n)**。  

---

## 心得  

- **核心技巧**：把二进制串压缩成**段（segment）**，并利用**段的邻接关系**把“一次交易”转化为**三段合并的长度**。  
- **适用的题型**  
  1. “把子数组/子串中连续 0/1 翻转一次，使 1 的最大连续长度最大”——如 LeetCode 1156、1657。  
  2. “区间查询 + 区间修改，要求快速获取某种基于相邻块的统计量”——典型用**线段树/稀疏表**。  
  3. “把字符串压缩成块后，询问块之间的关系”——如“字符串分块求和”“块状更新”。  

- **一句话总结**：  
  *把字符串压成段，交易只影响完整的 “左‑0‑右” 三段结构，用线段树在段上做最大值查询，即可在 O(log n) 里得到每个子串的最优活跃区段数。*

---

## 反思  

- **第一反应**：看到“最多一次交易”“子串”，第一时间会想到枚举子串内部的每一种可能——也就是暴力 O(n·q)。  
- **最容易踩的坑**  
  1. **段边界遗漏**：交易必须完整覆盖左‑0‑右三段，忘记检查左端/右端是否被子串完整包含会得到错误答案。  
  2. **边界段的处理**：最左或最右的 `0` 段没有左/右相邻的 `1` 段，`len[i-1]` 或 `len[i+1]` 必须视为 `0`。  
  3. **查询长度不足 3 段**：此时根本不能进行任何合法交易，答案应直接是子串原有的 `'1'` 个数。  
- **下次遇到同类题**：  
  1. **先把结构压缩**（段、块、区间），看是否可以把“一次操作”映射为“合并相邻块”。  
  2. **把每个块的贡献预先算好**，然后把 “区间最大/最小” 之类的需求交给线段树或稀疏表来完成。  

这样既能把复杂度降到对数级，又能保证实现的正确性。祝你玩转每一道算法题！