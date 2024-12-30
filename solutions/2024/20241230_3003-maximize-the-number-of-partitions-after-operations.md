# #3003. **最大化操作后的分割数量** / Maximize the Number of Partitions After Operations

> 难度：困难 · 标签：String、Dynamic Programming、Bit Manipulation、Bitmask · [LeetCode 链接](https://leetcode.com/problems/maximize-the-number-of-partitions-after-operations/)

---

## 题目（英文原版）

**Description**

You are given a string s and an integer k.
First, you are allowed to change at most one index in s to another lowercase English letter.
After that, do the following partitioning operation until s is empty:
Return an integer denoting the maximum number of resulting partitions after the operations by optimally choosing at most one index to change.

**Examples**

**Example 1:**

```
Input: s = "accca", k = 2
Output: 3
Explanation:
The optimal way is to change s[2] to something other than a and c, for example, b. then it becomes "acbca" .
Then we perform the operations:
Doing the operations, the string is divided into 3 partitions, so the answer is 3.
```

**Example 2:**

```
Input: s = "aabaab", k = 3
Output: 1
Explanation:
Initially s contains 2 distinct characters, so whichever character we change, it will contain at most 3 distinct characters, so the longest prefix with at most 3 distinct characters would always be all of it, therefore the answer is 1.
```

**Example 3:**

```
Input: s = "xxyz", k = 1
Output: 4
Explanation:
The optimal way is to change s[0] or s[1] to something other than characters in s , for example, to change s[0] to w .
Then s becomes "wxyz" , which consists of 4 distinct characters, so as k is 1, it will divide into 4 partitions.
```

**Constraints**

- 1 <= s.length <= 104
- s consists only of lowercase English letters.
- 1 <= k <= 26

---

## 题目（中文翻译）

给定一个字符串 `s` 和一个整数 `k`。  
首先，你最多可以将 `s` 中的 **一个** 下标的字符改成另一个小写英文字母（lowercase English letter）。  
随后，重复执行下面的 **分割（partition）** 操作，直至 `s` 为空：  

> **分割操作**：从字符串的左端开始，取最长的前缀，使其包含的 **不同字符（distinct characters）** 不超过 `k`。将该前缀从 `s` 中移除，形成一个分割。  

返回一个整数，表示在上述过程中通过**最优**选择（至多一次字符修改）后能够得到的 **分割（partition）** 的最大数量。

---

### 示例

**示例 1**  
```text
Input: s = "accca", k = 2
Output: 3
Explanation:
最优的做法是把 s[2] 改成除 'a'、'c' 之外的字符，例如 'b'，此时字符串变为 "acbca"。  
随后执行分割操作：
- 第一次取前缀 "ac"，包含的不同字符 ≤ 2，移除后剩余 "bca"；
- 第二次取前缀 "b"，移除后剩余 "ca"；
- 第三次取前缀 "ca"，移除后为空。  
共得到 3 个分割，答案为 3。
```

**示例 2**  
```text
Input: s = "aabaab", k = 3
Output: 1
Explanation:
原字符串仅含 2 种不同字符。无论把哪个字符改成其他字符，整个字符串最多只会出现 3 种不同字符。  
因此，满足 “不同字符 ≤ 3” 的最长前缀始终是整个字符串本身，只有 1 个分割，答案为 1。
```

**示例 3**  
```text
Input: s = "xxyz", k = 1
Output: 4
Explanation:
最优的做法是把 s[0] 或 s[1] 改成字符串中不存在的字符，例如把 s[0] 改为 'w'。  
此时字符串变为 "wxyz"，包含 4 种不同字符。由于 k=1，分割操作每次只能取长度为 1 的前缀，最终会得到 4 个分割，答案为 4。
```

---

### 约束条件

- $1 \leq \text{s.length} \leq 10^4$
- `s` 仅由小写英文字母组成
- $1 \leq k \leq 26$

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把“改一位字符”这件事全部枚举出来，然后把 **“把字符串不断切掉满足条件的最长前缀”** 这一步也完整模拟。  

1. **枚举要改的下标**  
   - 可以不改（相当于把下标设为 `-1`），也可以把下标 `i (0 ≤ i < n)` 换成除原字符外的 25 个小写字母中的任意一个。  
   - 这一步相当于在字典里查找所有可能的“新单词”，把下标当成“词条”，把 25 种新字母当成“解释”。  

2. **模拟切割过程**  
   - 从字符串的左端开始，用一个滑动窗口记录当前窗口里出现了多少种不同的字符（`distinct`）。  
   - 当 `distinct ≤ k` 时，窗口可以继续往右扩；一旦超过 `k`，说明上一个窗口已经是 **“满足条件的最长前缀”**，把它切掉，计数加一，然后从切掉的位置重新开始。  
   - 直到整个字符串被切完，得到的计数就是这次改动得到的分区数。  

因为我们把所有可能的改动都跑一遍，必然能得到最大值，所以这个方法是 **正确** 的。  

**时间/空间复杂度**（大白话）  
- 枚举下标：`n` 次（最多 10⁴）  
- 每个下标枚举 25 种新字母（相当于把每本书的每一页都改成 25 种不同的颜色）  
- 对每一种改动，都要 **从头到尾** 扫描一次字符串来模拟切割，最坏情况要遍历 `n` 个字符。  

于是总体时间是 `O(n * 25 * n) = O(n²)`，在最坏的 10⁴ 长度下会是 10⁸ 次操作，明显会超时。  
空间只用了几个计数器和一个字符数组，`O(1)`（常数级）。


#### 代码（Python）

```python
def maxPartitions_bruteforce(s: str, k: int) -> int:
    n = len(s)
    alphabet = [chr(ord('a') + i) for i in range(26)]

    # ---------- 计算一次完整切割得到的分区数 ----------
    def partitions(t: str) -> int:
        i = 0          # 当前处理到的下标
        cnt = 0        # 已得到的分区数
        while i < len(t):
            # 用 sliding window 找最长前缀
            distinct = set()
            j = i
            while j < len(t) and (len(distinct) + (t[j] not in distinct)) <= k:
                distinct.add(t[j])
                j += 1
            cnt += 1          # 把 [i, j) 切掉
            i = j             # 从 j 继续
        return cnt

    best = partitions(s)           # 不改字符的情况

    # ---------- 枚举一次改动 ----------
    s_list = list(s)
    for idx in range(n):
        original = s_list[idx]
        for ch in alphabet:
            if ch == original:      # 只能改成别的字母
                continue
            s_list[idx] = ch
            best = max(best, partitions(''.join(s_list)))
        s_list[idx] = original      # 恢复原字符

    return best
```

> 关键行的中文注释已经写在代码里，直接运行即可验证思路是否正确（仅用于小样例调试，**大数据会超时**）。

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 解释：`n`（枚举位置） × `25`（每位置的候选字母） × `O(n)`（每次完整模拟切割）。  
  - 在这里 `O(n²)` 可以想象成“把一个 10⁴×10⁴ 的格子全填满”，显然太慢。  

- **空间复杂度**：`O(1)`  
  - 只用了常数个额外变量（集合、指针等），不随 `n` 增长。

---

### 2. 最优解  

#### 思路  

暴力解的 **瓶颈** 在于每次改动后都要 **重新从头扫描** 整个字符串。  
如果我们能够 **预先算好** 在 **不改字符** 的情况下每一次切割会把字符串分成怎样的区间，那么在尝试一次改动时，只需要 **局部修正** 这些区间，而不必重新遍历全局。

下面一步步推导出这种“预处理 + 局部修正”的思路：

1. **把切割过程抽象成跳转**  
   - 对于原字符串 `s`（不改字符），从下标 `i` 开始的最长合法前缀的右端点记作 `end[i]`（闭区间 `[i, end[i]]`）。  
   - `end[i]` 可以用 **滑动窗口** 一次遍历得到：左指针 `i` 右移时，右指针 `r` 只会向右移动，总体 `O(n)`。  

2. **利用 `end` 构造前缀/后缀分区计数**  
   - `pref[i]` = 在区间 `[0, i]`（包括 `i`）里，按照上述跳转能得到的分区数。  
   - `suff[i]` = 在区间 `[i, n-1]` 里，能够得到的分区数（从左往右切割）。  
   - 这两个数组同样可以在 `O(n)` 内一次遍历得到。  

3. **记录每个位置所在的原始分区起点**  
   - `part_start[i]` = 包含下标 `i` 的分区在原字符串中的左端点。  
   - 只要遍历一次 `end`，随时把区间的左端点写进去即可。  

4. **枚举改动，只修正受影响的那一段**  
   - 设我们把下标 `i` 改成字符 `c`（`c != s[i]`）。  
   - 只会影响 **包含 `i` 的那个原始分区**（左端点为 `L = part_start[i]`），以及它右边的若干分区。  
   - 关键是找到 **在改动后**，从 `L` 开始，**还能继续往右扩到哪儿**（仍满足 ≤ k 种不同字符）。记这个最右端点为 `r`。  

5. **如何快速得到 `r`**  
   - 我们把每个字符视作 26 位的 **位掩码**（bitmask），比如 `'a'` → `1<<0`，`'b'` → `1<<1` ……  
   - 用 **前缀异或**（或前缀或）可以在 `O(1)` 时间得到任意子串的字符集合的位掩码。  
   - 于是我们可以对右端点二分搜索：在 `[L, n-1]` 中找最大的 `r` 使得子串 `[L, r]` 的不同字符数 ≤ k。  
   - 统计不同字符数只需要 `popcount(mask)`（即二进制中 1 的个数），Python 的 `int.bit_count()` 完成。  

6. **两种情况**  
   - **情况 A**：`r ≥ i`  
     - 改动后，`[L, r]` 能合并成 **一个** 分区。其余左侧已固定（`pref[L-1]`），右侧从 `r+1` 开始仍按原规则切（`suff[r+1]`）。  
     - 总分区数 = `1 + pref[L-1] + suff[r+1]`。  

   - **情况 B**：`r < i`（改动导致左侧的原分区仍不能覆盖到 `i`）  
     - 那么改动后会产生 **两个** 分区：  
       1. 原分区 `[L, r]`（仍合法）  
       2. 以 `i` 为起点的新的分区，需要再次向右找最远合法右端点 `r2`（二分搜索同理）。  
     - 总分区数 = `2 + pref[L-1] + suff[r2+1]`。  

7. **遍历所有 `i`、所有 25 个候选字符**，取最大值即为答案。  
   - 预处理 `end、pref、suff、part_start` 只需 `O(n)`。  
   - 对每个 `i`，二分搜索的时间是 `O(log n)`，但我们会对每个候选字符都做一次，所以整体是 `O(n * 25 * log n)`，在 `n ≤ 10⁴` 的限制下完全可接受。  

#### 代码（Python）

```python
from typing import List

def maxPartitions(s: str, k: int) -> int:
    n = len(s)
    a2i = lambda ch: ord(ch) - ord('a')          # 字符 → 0~25

    # ---------- 1. 预处理：end[i] ----------
    # end[i] = 从 i 开始的最长合法前缀的右端点（闭区间）
    end: List[int] = [0] * n
    freq = [0] * 26          # 当前窗口里每个字符的出现次数
    distinct = 0             # 窗口里不同字符的种数
    r = 0
    for l in range(n):
        while r < n:
            idx = a2i(s[r])
            if freq[idx] == 0 and distinct == k:   # 再加入会超限
                break
            if freq[idx] == 0:
                distinct += 1
            freq[idx] += 1
            r += 1
        end[l] = r - 1        # r 超出了合法范围，所以右端点是 r-1
        # 移除左端点 l，准备下一轮 l+1
        left_idx = a2i(s[l])
        freq[left_idx] -= 1
        if freq[left_idx] == 0:
            distinct -= 1

    # ---------- 2. 前缀/后缀分区计数 ----------
    pref = [0] * n          # pref[i] = 区间 [0, i] 的分区数
    i = 0
    cnt = 0
    while i < n:
        cnt += 1
        nxt = end[i] + 1
        for j in range(i, nxt):
            pref[j] = cnt
        i = nxt

    suff = [0] * (n + 1)    # suff[i] = 区间 [i, n-1] 的分区数，suff[n]=0 方便写
    i = n - 1
    cnt = 0
    while i >= 0:
        cnt += 1
        # 从 i 向左找它对应的左端点
        # 这里利用 end 的逆向特性：如果 end[l] >= i，则 l 属于同一个分区
        # 为简化直接向左遍历直到不在同一区间
        j = i
        while j >= 0 and end[j] >= i:
            j -= 1
        # 区间 [j+1, i] 为一个分区
        for pos in range(j + 1, i + 1):
            suff[pos] = cnt
        i = j

    # ---------- 3. 记录每个位置所在的原始分区起点 ----------
    part_start = [0] * n
    i = 0
    while i < n:
        L = i
        R = end[i]
        for pos in range(L, R + 1):
            part_start[pos] = L
        i = R + 1

    # ---------- 4. 前缀位掩码（帮助 O(1) 统计子串不同字符数） ----------
    pref_mask = [0] * (n + 1)      # pref_mask[i] = s[0:i] 的字符集合（位掩码）
    for i, ch in enumerate(s):
        pref_mask[i + 1] = pref_mask[i] | (1 << a2i(ch))

    def distinct_cnt(l: int, r: int) -> int:
        """返回子串 s[l:r]（左闭右开）不同字符的种数"""
        mask = pref_mask[r] ^ pref_mask[l]   # 只保留 l~r-1 的位
        return mask.bit_count()

    # ---------- 5. 枚举改动 ----------
    best = pref[-1]          # 不改字符的情况已经在 pref 中算好
    alphabet = [chr(ord('a') + i) for i in range(26)]

    for i in range(n):
        orig = s[i]
        L = part_start[i]          # 原分区左端点
        left_pref = pref[L - 1] if L > 0 else 0

        for ch in alphabet:
            if ch == orig:
                continue

            # ---------- 计算改动后从 L 开始能走多远 ----------
            # 二分搜索右端点 r，使得 [L, r] 的不同字符数 ≤ k
            lo, hi = L, n - 1
            r = L - 1
            while lo <= hi:
                mid = (lo + hi) // 2
                if distinct_cnt(L, mid + 1) <= k:
                    r = mid
                    lo = mid + 1
                else:
                    hi = mid - 1

            if r >= i:        # 情况 A：改动的字符被包含在新的合并区间里
                right_suff = suff[r + 1] if r + 1 <= n else 0
                best = max(best, 1 + left_pref + right_suff)
            else:             # 情况 B：改动的字符在左侧区间之外，需要再分一次
                # 再找一次从 i 开始的最远合法右端点 r2
                lo, hi = i, n - 1
                r2 = i - 1
                while lo <= hi:
                    mid = (lo + hi) // 2
                    if distinct_cnt(i, mid + 1) <= k:
                        r2 = mid
                        lo = mid + 1
                    else:
                        hi = mid - 1
                right_suff = suff[r2 + 1] if r2 + 1 <= n else 0
                best = max(best, 2 + left_pref + right_suff)

    return best
```

**代码要点说明（中文注释已在代码中）**  

- `end` 用一次滑动窗口求出每个起点的最远合法右端点。  
- `pref` / `suff` 分别是左侧/右侧已经确定的分区数，帮助我们在局部修改后快速拼接整体答案。  
- `part_start` 记录原始分区的左端点，定位受影响的区间。  
- `pref_mask` + `distinct_cnt` 通过 **位掩码 + popcount** 在 `O(1)` 内得到任意子串的不同字符数，随后用 **二分搜索** 找到最右合法位置。  
- 最终遍历所有位置和 25 种可能的字符，取最大分区数即为答案。

#### 复杂度  

- **时间复杂度**：`O(n + n·25·log n)` ≈ `O(n log n)`  
  - 预处理 `end、pref、suff、part_start、pref_mask` 只要 `O(n)`。  
  - 对每个位置 `i`（`n` 次），遍历 25 种新字符，每种字符需要两次二分搜索（各 `O(log n)`），所以整体是 `n·25·log n`。  
  - 对于 `n ≤ 10⁴`，这大约是几万次运算，毫秒级即可完成。  

- **空间复杂度**：`O(n)`  
  - 需要存 `end、pref、suff、part_start、pref_mask` 等线性数组，都是长度 `n`（或 `n+1`）的整数列表。  
  - 相比暴力的 `O(1)` 多了线性空间，但仍然是可以接受的。

---

## 心得  

- **核心技巧**：  
  1. **滑动窗口 + 前缀位掩码** 快速判断任意子串的不同字符数。  
  2. **预计算分区跳转**（`end`、`pref`、`suff`）把全局切割过程抽象成若干跳跃，使得局部改动只需要局部修正。  

- **适用的题型**（类似思路）  
  - “在字符串上做最多一次修改，使得满足某种窗口约束的最大/最小值”  
  - “分割字符串，使每段满足字符种类/频率限制”  
  - “利用位掩码统计子串特性（如不同字母数、奇偶性）并配合二分/滑窗”  

- **一句话总结**：  
  **“先把不变情况下的切割结构全部算好，再在此基础上用位掩码 + 二分只修正受改动影响的那一段。”**

---

## 反思  

- **第一反应**：直接把“改一位”全部枚举，再把整个切割过程重新跑一遍。  
- **最容易踩的坑**  
  1. **统计子串不同字符数** 不能每次遍历整个子串，否则会把 `O(n²)` 再乘回来。位掩码或前缀计数是关键。  
  2. **边界条件**：`L = 0` 时 `pref[L-1]` 需要特殊处理；`r = n-1` 时 `suff[r+1]` 也要防止越界。  
  3. **二分搜索的闭区间/开区间** 容易写错，记得 `distinct_cnt(l, r+1)` 中的 `r+1` 表示右开区间。  

- **下次遇到同类题**，第一步应该：  
  1. **用滑动窗口一次遍历得到“最长合法前缀”**（或后缀），把问题抽象成“从左到右的跳转”。  
  2. **把全局结构预处理好**（前缀/后缀计数），再在此基础上考虑“局部修改”。  

这样既能避免重复全局遍历，又能把复杂度压到 `O(n log n)`，轻松通过 Hard 级别的限制。