# #3261. **计数满足 K 约束 II 的子串** / Count Substrings That Satisfy K-Constraint II

> 难度：困难 · 标签：Array、String、Binary Search、Sliding Window、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/count-substrings-that-satisfy-k-constraint-ii/)

---

## 题目（英文原版）

**Description**

You are given a binary string s and an integer k.
You are also given a 2D integer array queries, where queries[i] = [li, ri].
A binary string satisfies the k-constraint if either of the following conditions holds:
Return an integer array answer, where answer[i] is the number of substrings of s[li..ri] that satisfy the k-constraint.

**Examples**

**Example 1:**

```
Input: s = "0001111", k = 2, queries = [[0,6]]
Output: [26]
Explanation:
For the query [0, 6] , all substrings of s[0..6] = "0001111" satisfy the k-constraint except for the substrings s[0..5] = "000111" and s[0..6] = "0001111" .
```

**Example 2:**

```
Input: s = "010101", k = 1, queries = [[0,5],[1,4],[2,3]]
Output: [15,9,3]
Explanation:
The substrings of s with a length greater than 3 do not satisfy the k-constraint.
```

**Constraints**

- 1 <= s.length <= 105
- s[i] is either '0' or '1'.
- 1 <= k <= s.length
- 1 <= queries.length <= 105
- queries[i] == [li, ri]
- 0 <= li <= ri < s.length
- All queries are distinct.

---

## 题目（中文翻译）

你被给定一个二进制字符串 `s` 和一个整数 `k`。  
同时还给定一个二维整数数组 `queries`，其中 `queries[i] = [l_i, r_i]`。

如果一个二进制字符串满足 **k-约束**（k‑constraint），则必须满足以下两条条件中的任意一条：

（此处原题会列出具体的两条条件）

返回一个整数数组 `answer`，其中 `answer[i]` 是 `s[l_i..r_i]` 的所有满足 k‑约束的子串（substrings）的数量。

---

### 示例

**示例 1**

> **输入**  
> `s = "0001111", k = 2, queries = [[0,6]]`  
> **输出**  
> `[26]`  
> **解释**  
> 对于查询 `[0, 6]`，`s[0..6] = "0001111"` 的所有子串都满足 k‑约束，唯一例外的是子串 `s[0..5] = "000111"` 和 `s[0..6] = "0001111"`。

**示例 2**

> **输入**  
> `s = "010101", k = 1, queries = [[0,5],[1,4],[2,3]]`  
> **输出**  
> `[15,9,3]`  
> **解释**  
> 长度大于 3 的所有子串都不满足 k‑约束。

---

### 约束条件

- `1 <= s.length <= 10^5`
- `s[i]` 只能是 `'0'` 或 `'1'`
- `1 <= k <= s.length`
- `1 <= queries.length <= 10^5`
- `queries[i] == [l_i, r_i]`
- `0 <= l_i <= r_i < s.length`
- 所有查询互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

> **题目回顾**  
> 给定二进制字符串 `s`（只含 `'0'` 和 `'1'`）和整数 `k`。  
> 对于任意子串 `t`，只要下面两个条件之一成立，就说 `t` **满足 k‑constraint**：  

> 1. `t` 中 `'0'` 的个数 **≤ k**  
> 2. `t` 中 `'1'` 的个数 **≤ k**  

> 换句话说，只要子串里 **至少有一种字符出现不超过 k 次**，它就是合法的。  

> 对每个查询 `[l, r]`（子串 `s[l..r]`），要求统计该区间内所有满足 k‑constraint 的子串个数。

---

**最直接的做法**：枚举所有子串，统计 `'0'` 与 `'1'` 的个数，看是否满足上面的任意一个条件。

* **枚举子串**：两层循环，外层固定左端点 `i`，内层固定右端点 `j (i ≤ j ≤ r)`。  
* **计数**：在枚举过程中累计 `0`、`1` 的出现次数，或者每次查询时用 `prefix sum` 直接求出子串中 `0`、`1` 的个数。  

> **生活化类比**：  
> 想象你在一本字典里查词，字典的每一页上只能写 **至多 k** 个 “0”。只要你翻开的这页（子串）里 “0” 的数量不超过 k，或者 “1” 的数量不超过 k，你就可以说这页“符合规则”。暴力做法就相当于把每一页都拿出来仔细数数，看到底符合不符合。

**为什么一定对？**  
因为我们把所有可能的子串都检查了一遍，只要有一个满足条件就计数，所有合法子串必然被统计，非法的自然不计。

**时间/空间复杂度**  

| 步骤 | 复杂度 | 含义解释 |
|------|--------|----------|
| 枚举子串（两层循环） | **O(n²)**（`n = len(s)`）| 想象 n = 10⁵ 时，`n²` 就是 10⁰¹⁰，根本跑不完。 |
| 统计 `'0'`/`'1'`（前缀和） | O(1) 取值 | 这一步很快，但被外层的 `n²` 盖掉了。 |
| 额外空间 | **O(n)**（前缀和数组）| 只需要保存每个位置左侧 `'0'`、`'1'` 的累计数。 |

> **大白话**：`O(n²)` 就像让 10⁵ 个小朋友两两握手，次数会是 10⁵ × 10⁵ ≈ 10¹⁰，根本不可能在一秒内完成。

---

#### 代码（Python）

```python
def brute_count(s: str, k: int, queries):
    n = len(s)
    # 前缀和：pre0[i] = s[:i] 中 '0' 的个数，pre1 同理（i 从 0 开始，pre0[0]=0）
    pre0 = [0] * (n + 1)
    pre1 = [0] * (n + 1)
    for i, ch in enumerate(s, 1):
        pre0[i] = pre0[i - 1] + (ch == '0')
        pre1[i] = pre1[i - 1] + (ch == '1')

    ans = []
    for l, r in queries:                 # 对每个查询单独暴力枚举
        cnt = 0
        for i in range(l, r + 1):        # 子串左端点
            for j in range(i, r + 1):    # 子串右端点
                zeros = pre0[j + 1] - pre0[i]   # s[i..j] 中 '0' 的个数
                ones  = pre1[j + 1] - pre1[i]   # s[i..j] 中 '1' 的个数
                if zeros <= k or ones <= k:    # 满足任意一个条件即计数
                    cnt += 1
        ans.append(cnt)
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n² + q·n²)`（最坏情况下每个查询都遍历整个区间），在 `n ≤ 10⁵` 时不可接受。
- **空间复杂度**：`O(n)`（前缀和数组），额外的 `O(1)` 用于计数。

---

### 2. 最优解

#### 思路  

暴力解的核心瓶颈在于 **枚举所有子串**。  
观察条件：

> 对于子串 `s[i..j]`，只要 `cnt0 ≤ k` **或** `cnt1 ≤ k` 即合法。  

换句话说，**只要两种字符的出现次数同时 > k，子串就非法**。  
这让我们可以使用**滑动窗口**：  
- 维护一个左端点 `l`，右端点不断向右扩展 `r`。  
- 同时记录窗口 `[l, r]` 中 `'0'`、`'1'` 的个数 `c0, c1`。  
- 当 `c0 > k 且 c1 > k` 时，窗口已不合法，需要把左端点右移，直到合法为止。

> **关键结论**：  
> 对于每个固定的右端点 `r`，存在**唯一的最左合法位置** `L[r]`（记作 `left_bound[r]`），满足  
> `s[L[r]..r]` 合法且 `L[r]` 是满足此条件的最小下标。  
> 那么 **以 `r` 为右端点的所有合法子串** 正好是 `L[r] … r`，数量为 `r - L[r] + 1`。

所以我们只需要一次线性遍历求出 `L[r]`，再把它们转化为查询答案。

---

#### 2.1 预处理 `L[r]`

```text
c0, c1 = 0, 0
l = 0
for r in range(n):
    if s[r] == '0': c0 += 1 else: c1 += 1
    while c0 > k and c1 > k:          # 两者都超过 k，窗口非法
        if s[l] == '0': c0 -= 1 else: c1 -= 1
        l += 1
    L[r] = l          # 当前窗口已经是最左合法的
```

*时间复杂度*：每个字符最多进窗口一次、出窗口一次，**O(n)**。  
*空间复杂度*：保存 `L` 数组 **O(n)**。

---

#### 2.2 离线处理查询

对查询 `[ql, qr]`，我们要统计

```
ans = Σ_{i = ql..qr}  ( i - max(L[i], ql) + 1 )
```

解释：

- `i` 为子串的右端点。  
- `max(L[i], ql)` 是左端点的**实际下界**：  
  - 如果 `L[i] ≥ ql`，说明从 `L[i]` 起的所有子串合法，左端点只能取 `L[i]..i`。  
  - 如果 `L[i] < ql`，查询区间限制左端点不能小于 `ql`，于是左端点只能从 `ql` 开始。

于是贡献为 `i - max(L[i], ql) + 1`。

---

#### 2.3 通过 Fenwick 树（BIT）把公式转化为可快速求和的形式

把公式拆开：

```
i - max(L[i], ql) + 1
= (i + 1) - max(L[i], ql)
```

对区间 `[ql, qr]` 求和：

```
Σ (i + 1)  -  Σ max(L[i], ql)
```

第一部分 `Σ (i + 1)` 只和下标有关，可用前缀和 `pref_idx` 预处理得到 O(1) 查询。

第二部分需要 **区分两类**：

1. **L[i] < ql** → `max(L[i], ql) = ql`（统一为 `ql`）  
2. **L[i] ≥ ql** → `max(L[i], ql) = L[i]`

记  
- `cnt_big` = 区间内满足 `L[i] ≥ ql` 的位置数  
- `sum_big` = 这些位置对应的 `L[i]` 的总和  

则  

```
Σ max(L[i], ql) = cnt_big * ql + sum_big
```

所以答案为

```
total_idx = pref_idx[qr] - pref_idx[ql-1]      # Σ (i+1)
len_seg   = qr - ql + 1                       # 区间长度
cnt_small = len_seg - cnt_big                # L[i] < ql 的个数

ans = total_idx - (cnt_small * ql + sum_big)
```

**如何快速得到 `cnt_big` 与 `sum_big`？**  
把所有位置 `i` 按 `L[i]` 的大小**降序**加入 Fenwick 树：

- 树 `bit_cnt` 维护 **出现次数**（即 `1`），可以查询任意区间的元素个数。  
- 树 `bit_sum` 维护 **L[i] 的值**，可以查询区间内 `L` 的和。

我们把查询也按左端点 `ql` **降序**排列。  
遍历 `cur_left` 从 `n-1` 到 `0`：

```
while next_position has L[pos] >= cur_left:
    bit_cnt.add(pos, 1)
    bit_sum.add(pos, L[pos])
    move pointer
process all queries whose ql == cur_left:
    cnt_big = bit_cnt.range_sum(ql, qr)
    sum_big = bit_sum.range_sum(ql, qr)
    compute answer by上面的公式
```

因为每个位置只加入一次，每个查询只做两次树查询，整体复杂度 **O((n + q) log n)**。

---

#### 2.4 完整代码（Python）

```python
from typing import List, Tuple

class BIT:
    """Fenwick Tree（二叉索引树），1-indexed"""
    def __init__(self, n: int):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, idx: int, delta: int):
        """在 idx (0-based) 位置加 delta"""
        i = idx + 1
        while i <= self.n:
            self.bit[i] += delta
            i += i & -i

    def _sum(self, idx: int) -> int:
        """前缀和，包含 idx (0-based)"""
        i = idx + 1
        s = 0
        while i:
            s += self.bit[i]
            i -= i & -i
        return s

    def range_sum(self, l: int, r: int) -> int:
        """求区间 [l, r] 的和，l、r 为 0-based，且 l <= r"""
        if l > r:
            return 0
        return self._sum(r) - (self._sum(l - 1) if l else 0)


def count_substrings_k_constraint(s: str, k: int,
                                 queries: List[List[int]]) -> List[int]:
    n = len(s)

    # ---------- 1. 计算每个右端点的最左合法位置 L ----------
    L = [0] * n               # L[i] = 最小左端点，使得 s[L[i]..i] 合法
    cnt0 = cnt1 = 0
    left = 0
    for right, ch in enumerate(s):
        if ch == '0':
            cnt0 += 1
        else:
            cnt1 += 1
        # 当两种字符都超过 k 时，窗口非法，左指针右移
        while cnt0 > k and cnt1 > k:
            if s[left] == '0':
                cnt0 -= 1
            else:
                cnt1 -= 1
            left += 1
        L[right] = left

    # ---------- 2. 前缀和： Σ(i+1) ----------
    pref_idx = [0] * n          # pref_idx[i] = Σ_{j=0..i} (j+1)
    cur = 0
    for i in range(n):
        cur += i + 1
        pref_idx[i] = cur

    # ---------- 3. 离线处理查询 ----------
    # 把位置按 L 值降序排列，方便一次性加入 BIT
    pos_by_L = sorted([(L[i], i) for i in range(n)], key=lambda x: -x[0])

    # 把查询也按左端点降序排列，保存原始下标
    qs = [(l, r, idx) for idx, (l, r) in enumerate(queries)]
    qs.sort(key=lambda x: -x[0])

    bit_cnt = BIT(n)   # 记录出现的点的个数
    bit_sum = BIT(n)   # 记录对应的 L 值之和

    ans = [0] * len(queries)
    ptr = 0  # 指向 pos_by_L

    for ql, qr, qid in qs:
        # 把所有 L[pos] >= ql 的位置加入 BIT
        while ptr < n and pos_by_L[ptr][0] >= ql:
            _, pos = pos_by_L[ptr]
            bit_cnt.add(pos, 1)          # 计数 +1
            bit_sum.add(pos, L[pos])     # 累加 L[pos]
            ptr += 1

        # 区间长度
        length = qr - ql + 1

        # Σ (i+1) 在区间 [ql, qr] 的前缀和
        total_idx = pref_idx[qr] - (pref_idx[ql - 1] if ql else 0)

        # L[i] >= ql 的个数与 L 值之和
        cnt_big = bit_cnt.range_sum(ql, qr)
        sum_big = bit_sum.range_sum(ql, qr)

        # L[i] < ql 的个数 = length - cnt_big
        cnt_small = length - cnt_big

        # 公式： ans = total_idx - (cnt_small * ql + sum_big)
        ans[qid] = total_idx - (cnt_small * ql + sum_big)

    return ans
```

> **代码要点注释**  
> 1. `L` 的求法使用了经典的 **滑动窗口**，每次右移 `right`，如果窗口非法（`cnt0 > k 且 cnt1 > k`），就左移 `left` 直至合法。  
> 2. `BIT` 实现了 **区间求和**，在 `O(log n)` 时间内完成。  
> 3. 通过 **离线排序**（把查询和位置都按左端点降序），我们只需要一次遍历就把所有满足 `L[i] ≥ ql` 的位置加入树，避免了每个查询都重新扫描。  
> 4. 最后利用前缀和 `pref_idx` 把 `Σ (i+1)` 的部分直接算出，整体时间复杂度是 `O((n + q) log n)`，空间 `O(n)`。

#### 复杂度

| 步骤 | 时间复杂度 | 空间复杂度 | 说明 |
|------|------------|------------|------|
| 计算 `L`（滑动窗口） | **O(n)** | O(n) | 每个字符进出窗口各一次 |
| 前缀和 `pref_idx` | O(n) | O(n) | 只存一个长度为 `n` 的数组 |
| 排序 `pos_by_L`、`queries` | O(n log n + q log q) | O(n + q) | 标准排序 |
| Fenwick 树更新 & 查询 | **O((n + q) log n)** | O(n) | 两棵 BIT 各占 `n` 长度 |
| **总计** | **O((n + q) log n)** | **O(n + q)** | 对 `n, q ≤ 10⁵` 完全可接受 |

> 与暴力的 `O(n²)` 相比，`log n` 只相当于 17（因为 `2¹⁷ ≈ 1e5`），所以运行速度提升了 **数万倍**。

---

## 心得

- **核心技巧**：把“两个字符的计数同时大于 k”作为窗口失效的条件，用 **滑动窗口** 找到每个右端点的最左合法位置 `L[i]`。  
- **离线查询**：把所有查询按左端点排序，配合 **Fenwick 树**（或线段树）一次性维护满足 `L[i] ≥ current_left` 的位置，实现 `O(log n)` 区间求和。  
- **适用题型**  
  1. “子串满足某种 **双重** 条件，只要其中一种成立”——如本题的 `cnt0 ≤ k 或 cnt1 ≤ k`。  
  2. “需要在大量区间查询中统计满足窗口约束的子串数量”，典型例子还有 “子数组的最大值/最小值 ≤ K”。  
  3. “把每个右端点对应的左边界预处理，再利用前缀和/树结构快速求区间和”，如 “子数组和 ≤ K 的个数”。  

> **解题钥匙**：**把“合法子串”转化为“右端点对应的最左合法左端点”，再用离线+树结构批量求和**。

---

## 反思

- **第一反应**：看到“子串满足 k‑constraint”，自然想到枚举所有子串检查计数——这在面试里常是 **“先写出暴力”** 的步骤。  
- **最容易踩的坑**  
  1. **忘记“或”关系**：题目要求 **任意一种字符出现 ≤ k**，而不是两者都 ≤ k。容易把条件写成 `cnt0 ≤ k and cnt1 ≤ k`，导致答案完全错误。  
  2. **窗口失效条件写反**：合法窗口是 **至少有一种字符 ≤ k**，所以失效条件是 **两种字符都 > k**。如果写成 `cnt0 > k or cnt1 > k`，滑动窗口会不停收缩，导致 `L[i]` 计算错误。  
  3. **离线排序的方向**：必须 **从大到小** 处理左端点，否则加入 BIT 的时机会错位，导致 `cnt_big`、`sum_big` 统计不准确。  
  4. **前缀和下标错误**：`pref_idx[i]` 存的是 `Σ (j+1)`，取区间时要注意 `l = 0` 的特殊情况。  

- **下次类似题目**：  
  1. **先写出窗口失效的判定**（哪些计数同时超过阈值）。  
  2. **计算每个右端点对应的最左合法左端点**（滑动窗口一次遍历）。  
  3. **把查询离线化**，根据左端点排序，配合 BIT/线段树累计满足 `L[i] ≥ left` 的位置。  
  4. **利用前缀和把与下标相关的部分分离**，最终得到 `O((n+q) log n)` 的解法。  

这样就能把看似 “Hard” 的题目拆解成 **滑动窗口 + 离线 + 树结构** 三步走，条理清晰、代码易写。