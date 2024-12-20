# #2981. 寻找出现三次的最长特殊子串 I / Find Longest Special Substring That Occurs Thrice I

> 难度：中等 · 标签：Hash Table、String、Binary Search、Sliding Window、Counting · [LeetCode 链接](https://leetcode.com/problems/find-longest-special-substring-that-occurs-thrice-i/)

---

## 题目（英文原版）

**Description**

You are given a string s that consists of lowercase English letters.
A string is called special if it is made up of only a single character. For example, the string "abc" is not special, whereas the strings "ddd", "zz", and "f" are special.
Return the length of the longest special substring of s which occurs at least thrice, or -1 if no special substring occurs at least thrice.
A substring is a contiguous non-empty sequence of characters within a string.

**Examples**

**Example 1:**

```
Input: s = "aaaa"
Output: 2
Explanation: The longest special substring which occurs thrice is "aa": substrings "aaaa", "aaaa", and "aaaa".
It can be shown that the maximum length achievable is 2.
```

**Example 2:**

```
Input: s = "abcdef"
Output: -1
Explanation: There exists no special substring which occurs at least thrice. Hence return -1.
```

**Example 3:**

```
Input: s = "abcaba"
Output: 1
Explanation: The longest special substring which occurs thrice is "a": substrings "abcaba", "abcaba", and "abcaba".
It can be shown that the maximum length achievable is 1.
```

**Constraints**

- 3 <= s.length <= 50
- s consists of only lowercase English letters.

---

## 题目（中文翻译）

给定一个仅包含小写英文字母的字符串 `s`。  
如果一个字符串只由同一个字符组成，则称其为 **特殊（special）** 字符串。例如 `"abc"` 不是特殊字符串，而 `"ddd"`、`"zz"`、`"f"` 都是特殊字符串。  

返回 `s` 中出现次数至少为三次的最长 **特殊（special）子串（substring）** 的长度；如果不存在出现至少三次的特殊子串，返回 `-1`。  

子串（substring）是指字符串中连续的、非空的字符序列。

### 示例

**示例 1**  
输入：`s = "aaaa"`  
输出：`2`  
**解释**：出现三次的最长特殊子串是 `"aa"`，对应的子串有 `"aaaa"`、`"aaaa"`、`"aaaa"`（在不同位置）。可以证明最大长度只能是 2。

**示例 2**  
输入：`s = "abcdef"`  
输出：`-1`  
**解释**：不存在出现至少三次的特殊子串，故返回 `-1`。

**示例 3**  
输入：`s = "abcaba"`  
输出：`1`  
**解释**：出现三次的最长特殊子串是 `"a"`，对应的子串有 `"abcaba"`、`"abcaba"`、`"abcaba"`（在不同位置）。可以证明最大长度只能是 1。

### 约束

- `3 <= s.length <= 50`
- `s` 只包含小写英文字母。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**把所有可能的子串都列举出来**，然后检查它们是否满足「只包含同一个字符」且「出现次数 ≥ 3」这两个条件。  

- **枚举子串**：长度为 `len`（1~n），起始位置为 `i`（0~n‑len），子串就是 `s[i:i+len]`。  
- **判断是否 special**：只要子串里所有字符相同即可。可以把子串的第一个字符记下来，然后遍历子串的其余字符，看到不同的就立刻判为不符合。  
- **计数出现次数**：把每个符合要求的子串放进哈希表（Python 的 `dict`），键是子串本身，值是出现次数。遍历完所有子串后，找出值 ≥ 3 的键中长度最大的那个。

> **类比**：哈希表就像一本“词典”，我们把每个子串当作“单词”，它对应的“页码”就是出现的次数。遍历完后，只要找出出现次数不少于 3 次的最长单词即可。

这个方法一定能得到正确答案，因为我们没有遗漏任何子串，也没有对出现次数做任何近似。

#### 代码（Python）

```python
def longest_special_substring_bruteforce(s: str) -> int:
    n = len(s)
    cnt = {}                     # 哈希表：子串 → 出现次数

    # 1. 枚举所有子串
    for length in range(1, n + 1):          # 子串长度
        for start in range(0, n - length + 1):   # 起始位置
            sub = s[start:start + length]

            # 2. 判断 sub 是否 special（全由同一字符组成）
            first_char = sub[0]
            is_special = True
            for ch in sub:
                if ch != first_char:        # 只要有一个字符不同，就不是 special
                    is_special = False
                    break
            if not is_special:
                continue                    # 直接跳到下一个子串

            # 3. 统计出现次数
            cnt[sub] = cnt.get(sub, 0) + 1

    # 4. 在所有出现 ≥3 次的 special 子串里找最长的长度
    ans = -1
    for sub, times in cnt.items():
        if times >= 3:
            ans = max(ans, len(sub))
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n³)`  
  - 外层两层循环枚举所有子串，共 `O(n²)` 次。  
  - 判断一个子串是否 special 需要遍历子串本身，最坏情况下是 `O(n)`，于是总体是 `O(n³)`。  
  - 这里的 `n` 只到 50，`50³ = 125000`，完全可以接受。  

- **空间复杂度**：`O(n²)`  
  - 最坏情况下每个子串都是 special（例如全是同一个字符），哈希表里会保存 `O(n²)` 条记录。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**对每个子串都逐字符检查**，导致 `O(n³)`。  
观察题目可以发现：

1. **特殊子串只能是由同一个字符组成**，因此我们只需要关注每个字符 `a~z` 各自的出现情况。  
2. 在字符串中，同一个字符会形成若干**连续块（run）**，比如 `"aaabbaa"` 中字符 `'a'` 的块长度分别是 `3,2,1`。  
3. 对于长度为 `L` 的 special 子串，只要在某个块里有 `k ≥ L`，就可以在这个块内部得到 `k‑L+1` 个长度为 `L` 的子串（可以重叠）。  
4. 所以，给定字符 `c` 和长度 `L`，**出现次数** = ` Σ max(0, run_len - L + 1) `（对所有该字符的块求和）。只要这个和 ≥ 3，就说明长度为 `L` 的 special 子串出现了至少三次。

基于上述结论，我们可以：

- 对每个字符 `c`，统计它在 `s` 中所有块的长度，得到一个整数列表 `runs_c`。  
- 在 `1 … max_run_len`（该字符最大块长度）之间**二分搜索**最长的 `L`，使得 ` Σ max(0, run‑L+1) ≥ 3`。  
- 最终答案是所有字符得到的最长 `L` 的最大值（若始终找不到满足条件的 `L`，返回 `-1`）。

二分搜索把检查过程的时间从 `O(n)` 降到了 `O(log n)`，而字符种类只有 26 种，总体复杂度是 `O(26 * (n + log n)) ≈ O(n)`，足够快。

> **类比**：把每个字符的连续块想象成“仓库”，块长度 `k` 表示仓库里有 `k` 件相同商品。我们想知道能否挑选出长度为 `L` 的商品（即连续 `L` 件）至少三次——每个仓库能提供 `k‑L+1` 份（如果 `k<L` 就提供 0 份），只要所有仓库加起来不少于 3 份，就满足要求。

#### 代码（Python）

```python
def longest_special_substring_opt(s: str) -> int:
    n = len(s)
    answer = -1

    # 逐字符统计该字符的所有连续块长度
    for ch in set(s):                     # 只遍历实际出现的字符
        runs = []                         # 该字符的块长度列表
        i = 0
        while i < n:
            if s[i] != ch:
                i += 1
                continue
            j = i
            while j < n and s[j] == ch:   # 找到一个块的右边界
                j += 1
            runs.append(j - i)            # 块长度
            i = j

        # 如果所有块总长度都不足以出现三次，直接跳过
        if sum(runs) < 3:
            continue

        # 二分搜索最长的 L
        lo, hi = 1, max(runs)              # L 的取值范围
        best = -1
        while lo <= hi:
            mid = (lo + hi) // 2           # 试探的子串长度 L
            # 计算所有块能贡献的 L 长度子串数量
            total = sum(max(0, run - mid + 1) for run in runs)

            if total >= 3:                 # 能满足出现 ≥3 次，尝试更长
                best = mid
                lo = mid + 1
            else:                          # 不够长，缩短 L
                hi = mid - 1

        answer = max(answer, best)

    return answer
```

#### 复杂度  

- **时间复杂度**：`O(26 * n * log n)` → 实际上是 `O(n log n)`  
  - 对每个出现的字符遍历一次字符串得到所有块，`O(n)`。  
  - 二分搜索的步数是 `log(max_run_len) ≤ log n`，每一步遍历 `runs`（块数 ≤ n），所以每个字符的二分过程是 `O(n log n)`。  
  - 乘以最多 26 种字符，整体仍然是线性对数级别。  

- **空间复杂度**：`O(n)`  
  - 只需要存放当前字符的块长度列表，最坏情况（全是同一字符）列表长度为 `n`。  

---

## 心得  

- **核心技巧**：把“只包含同一字符的子串”转化为**连续块的长度**，利用**块内部的子串计数公式** `run‑L+1`，再配合二分搜索找最大满足条件的长度。  
- **适用的题型**  
  1. “最长子串/子数组出现至少 K 次”且子串有特定结构（如全相同字符、全递增等）。  
  2. “给定字符，判断其连续出现次数是否满足某个阈值”——常用块计数 + 前缀和。  
  3. “在字符串中找满足某种计数约束的最长区间”，二分 + 前缀计数的思路类似。  
- **一句话总结**：把“特殊子串出现次数”拆解为“每个连续块能贡献多少”，用二分快速定位最长可行长度。

---

## 反思  

- **第一反应**：看到“特殊子串只能是同一字符”，立刻想到枚举所有子串检查是否全相同。  
- **最容易踩的坑**  
  - **重叠计数**：同一块内部的子串可以相互重叠，需要用公式 `run‑L+1` 而不是简单的 `run // L`。  
  - **块的统计**：忽略了字符在不同位置出现的多个块，必须把所有块都累加。  
  - **边界条件**：长度为 1 的子串总是 special，需要确保二分搜索的下界是 1。  
- **下次类似题的第一步**：先**把问题抽象成“在若干区间/块上统计满足某长度的子段数量”**，再决定是直接枚举还是二分/滑动窗口等优化手段。