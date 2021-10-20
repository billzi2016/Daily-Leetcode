# #1520. 最大不重叠子字符串的数量 / Maximum Number of Non-Overlapping Substrings

> 难度：困难 · 标签：String、Greedy · [LeetCode 链接](https://leetcode.com/problems/maximum-number-of-non-overlapping-substrings/)

---

## 题目（英文原版）

**Description**

Given a string s of lowercase letters, you need to find the maximum number of non-empty substrings of s that meet the following conditions:
Find the maximum number of substrings that meet the above conditions. If there are multiple solutions with the same number of substrings, return the one with minimum total length. It can be shown that there exists a unique solution of minimum total length.
Notice that you can return the substrings in any order.

**Examples**

**Example 1:**

```
Input: s = "adefaddaccc"
Output: ["e","f","ccc"]
Explanation: The following are all the possible substrings that meet the conditions:
[
  "adefaddaccc"
  "adefadda",
  "ef",
  "e",
  "f",
  "ccc",
]
If we choose the first string, we cannot choose anything else and we'd get only 1. If we choose "adefadda", we are left with "ccc" which is the only one that doesn't overlap, thus obtaining 2 substrings. Notice also, that it's not optimal to choose "ef" since it can be split into two. Therefore, the optimal way is to choose ["e","f","ccc"] which gives us 3 substrings. No other solution of the same number of substrings exist.
```

**Example 2:**

```
Input: s = "abbaccd"
Output: ["d","bb","cc"]
Explanation: Notice that while the set of substrings ["d","abba","cc"] also has length 3, it's considered incorrect since it has larger total length.
```

**Constraints**

- 1 <= s.length <= 105
- s contains only lowercase English letters.

---

## 题目（中文翻译）

**描述**  
给定一个只包含小写字母的字符串 `s`，需要找到若干个**非空**子字符串（substring），使得这些子字符串两两**不重叠**（non‑overlapping），并且满足以下条件：

- 对于每个子字符串，若该子字符串中出现了某个字符 `c`，则 `s` 中所有出现的 `c` 都必须全部包含在该子字符串内部。  

在满足上述条件的前提下，求 **子字符串的最大数量**。如果存在多种方案得到相同的子字符串数量，则返回 **总长度最小** 的方案。可以证明，总长度最小的方案是唯一的。  

返回的子字符串可以以任意顺序输出。

---

**示例**  

示例 1  
```text
Input: s = "adefaddaccc"
Output: ["e","f","ccc"]
Explanation: 以下是所有满足条件的子字符串（部分列出）：
[
  "adefaddaccc",
  "adefadda",
  "ef",
  "e",
  "f",
  "ccc",
]
如果选第一个字符串，则无法再选其他子字符串，只得到 1 个；  
如果选 "adefadda"，剩下的 "ccc" 是唯一不与其重叠的子字符串，得到 2 个。  
最优解是选择 ["e","f","ccc]，共 3 个子字符串，且总长度最小。 
```

示例 2  
```text
Input: s = "abbaccd"
Output: ["d","bb","cc"]
Explanation: 虽然集合 ["d","abba","cc"] 也包含 3 个子字符串，但它的总长度更大，因而不是最优解。 
```

---

**约束**  
- `1 <= s.length <= 10^5`  
- `s` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有 **非空子串** 都枚举出来，逐个检查它们是否满足题目要求：

1. 对每个字符 `c`，子串里必须包含 `c` 在原串中出现的 **所有位置**（即左边界 ≤ 第一次出现的位置，右边界 ≥ 最后一次出现的位置）。
2. 选出满足条件的子串后，想办法挑选出 **最多**、且 **总长度最小** 的一组互不重叠的子串。

可以把这个过程类比成：

- **查字典**：要检查一个子串是否“合法”，就像在字典里查每个字母的所有页码，只有当子串覆盖了该字母所有的页码时才算合格。  
- **装箱**：把合法子串看成不同大小的盒子，要把盒子装进一条直线（原串）里，盒子之间不能重叠，目标是装进去的盒子最多且总占用空间最小。

**为什么暴力能得到正确答案**  
因为我们遍历了**所有可能的子串**，并且对每一种合法的子串组合都尝试了一遍（例如使用回溯或 DP 求最大不重叠子集），所以必然能找到最优解。

**时间/空间复杂度**  
- 枚举所有子串的数量是 `n*(n+1)/2 ≈ O(n²)`（`n` 为字符串长度）。  
- 对每个子串要检查 26 个字母的出现区间，最坏情况是 `O(26) = O(1)`，但因为要遍历子串内部的字符，实际是 `O(length_of_substring)`，累计下来仍是 `O(n³)`。  
- 再加上对合法子串集合进行“最大不重叠子集”搜索，最坏会是指数级（`2^k`，`k` 为合法子串数），因此整体时间复杂度约为 **指数级**，在 `n=10⁵` 时根本不可行。  
- 空间上需要保存所有子串的区间，最坏 `O(n²)`。

> **大白话**：  
> - `O(n²)` 就像你要把每一页纸和每一本书的每一行都配对一次，次数会随 `n` 的平方增长。  
> - `O(2^k)` 更糟，像是你每次都要考虑“要不要选这本书”，选或不选每本书都有一次决定，组合数会翻倍。

#### 代码（Python）

```python
from itertools import combinations
from typing import List

def max_non_overlapping_bruteforce(s: str) -> List[str]:
    n = len(s)

    # 统计每个字符的最左、最右出现位置
    left = {c: n for c in set(s)}
    right = {c: -1 for c in set(s)}
    for i, ch in enumerate(s):
        left[ch] = min(left[ch], i)
        right[ch] = max(right[ch], i)

    # 判断子串 s[l:r+1] 是否合法
    def valid(l: int, r: int) -> bool:
        for ch in set(s[l:r+1]):                # 只检查子串里出现的字符
            if left[ch] < l or right[ch] > r:   # 有字符的全局区间跨出子串
                return False
        return True

    # 收集所有合法子串的区间
    intervals = []
    for l in range(n):
        for r in range(l, n):
            if valid(l, r):
                intervals.append((l, r))

    # 暴力搜索最大不重叠子集（指数级）
    best = []
    m = len(intervals)
    for mask in range(1 << m):               # 每一种选取/不选的组合
        cur = []
        last_end = -1
        ok = True
        for i in range(m):
            if mask >> i & 1:
                l, r = intervals[i]
                if l <= last_end:           # 重叠，非法
                    ok = False
                    break
                cur.append((l, r))
                last_end = r
        if ok:
            # 先比较子串个数，再比较总长度
            if (len(cur) > len(best)) or (len(cur) == len(best) and
               sum(r - l + 1 for l, r in cur) < sum(r - l + 1 for l, r in best)):
                best = cur

    # 把区间转成字符串返回
    return [s[l:r+1] for l, r in best]
```

> **提示**：上述代码仅用于说明思路，实际运行会在 `n=20` 左右就超时。

#### 复杂度

- **时间复杂度**：`O(2^k * k)`（指数级），其中 `k` 为合法子串的数量。  
  解释：我们遍历了所有子集（`2^k`），每次检查是否冲突需要遍历子集里选中的区间（最多 `k`）。
- **空间复杂度**：`O(k)` 保存合法区间，最坏 `O(n²)`。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **“枚举所有子串”** 和 **“指数级挑选子集”**。  
观察题目可以发现：

1. **合法子串之间只能出现包含关系**  
   - 若两个合法子串相交却不完全包含，则必有某个字符的全部出现位置跨出了其中一个子串，违背合法性。  
   - 因此，真正可以一起选的子串 **一定是不相交**（不重叠），否则必有包含关系。

2. **每个字符只能出现在唯一的“最小合法子串”里**  
   - 对字符 `c`，它在原串的最左出现位置记为 `L[c]`，最右出现位置记为 `R[c]`。  
   - 若我们想让一个子串包含字符 `c` 的所有出现，那么子串的左端点 **不能小于** `L[c]`，右端点 **不能大于** `R[c]`。  
   - 于是，以字符 `c` 为“入口”，我们可以 **不断扩展** 区间 `[L[c], R[c]]`：  
     - 在当前区间内检查每个字符 `x`，如果 `L[x]` 在区间左侧之外或 `R[x]` 在右侧之外，就把区间扩大到覆盖 `L[x]` 与 `R[x]`。  
     - 重复上述过程，直到区间不再扩大。  
   - 这个 **最终得到的区间** 就是以字符 `c` 为起点的 **最小合法子串**（如果最终区间恰好等于 `[L[c], R[c]]`，则说明它本身已经合法；否则说明不存在以 `c` 为左端点的合法子串）。

3. **所有字符得到的最小合法子串** 形成一组候选区间。  
   - 这些区间已经是 “**最短** 的合法子串**”。  
   - 题目要求 “**最多子串** 且 “**总长度最小**”。  
   - 经典的**区间调度**（interval scheduling）问题告诉我们：**把区间按右端点升序排序，贪心地选不冲突的区间** 能得到**最大数量**的互不重叠区间。  
   - 因为我们已经把每个字符的区间压缩到了最短，所以在数量相同的情况下，贪心选右端点最早的区间自然会产生**最小的总长度**（这也是题目唯一最小总长度解的保证）。

**核心算法**  
- **预处理**：一次遍历得到每个字符的最左、最右出现位置 `L[c]`、`R[c]`。  
- **构造最小合法子串**：对每个字符 `c`，从 `L[c]` 开始向右扩展，直至区间不再变化。若最终区间的左端点仍是 `L[c]`，则该区间是合法的，保存下来。  
- **贪心挑选**：把所有合法区间按右端点升序排序，遍历时只要当前区间的左端点大于上一次选中的右端点，就把它加入答案。

下面用生活化的类比帮助理解：

- **左/右出现位置**：把每个字母想象成一种“邮递员”，`L[c]` 是他第一次送信的街道，`R[c]` 是最后一次送信的街道。要让一个快递盒子（子串）合法，就必须把这位邮递员所有的信件都装进去。
- **区间扩展**：我们先把盒子装到邮递员第一次和最后一次送信的街道之间。如果盒子里还有别的邮递员的信件没有全部装进去，就把盒子再往外扩，直到所有信件都在盒子里——这一步就是“**不断扩展**”。
- **贪心选盒子**：所有盒子大小已经最小，接下来我们把盒子排成一排，先挑最左边（右端点最早）的盒子装进仓库，然后再挑下一个不和已经装好的盒子重叠的盒子……这样装的盒子最多，也最省空间。

#### 代码（Python）

```python
from typing import List

def maxNumOfSubstrings(s: str) -> List[str]:
    n = len(s)

    # 1. 统计每个字符的最左、最右出现位置
    left = [n] * 26          # left[i] = 最左出现位置，i 对应字符 chr(ord('a')+i)
    right = [-1] * 26        # right[i] = 最右出现位置
    for i, ch in enumerate(s):
        idx = ord(ch) - ord('a')
        left[idx] = min(left[idx], i)
        right[idx] = max(right[idx], i)

    # 2. 以每个字符为起点，尝试构造「最小合法子串」
    intervals = []           # 保存所有合法区间 (l, r)
    for c in range(26):
        if right[c] == -1:           # 该字符根本不存在
            continue

        l, r = left[c], right[c]     # 初始区间：该字符的全部出现范围
        # 只要区间内部还有字符的出现范围超出当前区间，就把区间扩大
        expanded = True
        while expanded:
            expanded = False
            # 检查区间 [l, r] 内所有字符
            for j in range(l, r + 1):
                idx = ord(s[j]) - ord('a')
                if left[idx] < l:            # 出现更左，需要左边界左移
                    l = left[idx]
                    expanded = True
                if right[idx] > r:           # 出现更右，需要右边界右移
                    r = right[idx]
                    expanded = True
        # 扩展结束后，如果区间的左端点仍是字符 c 的最左位置，则说明
        # 这个区间是「以字符 c 为左端点的最小合法子串」。
        if l == left[c]:            # 只有左端点恰好等于该字符的最左位置才合法
            intervals.append((l, r))

    # 3. 贪心挑选不重叠区间：按右端点升序排序
    intervals.sort(key=lambda x: x[1])   # 先选右端点最早的

    ans = []
    prev_end = -1
    for l, r in intervals:
        if l > prev_end:           # 与已选区间不重叠
            ans.append(s[l:r+1])   # 把子串加入答案
            prev_end = r

    return ans
```

**代码要点解释**  

| 行号 | 关键代码 | 中文注释 |
|------|----------|----------|
| 5‑8 | `left = [n] * 26; right = [-1] * 26` | 初始化每个字母的最左/最右出现位置。`n` 表示「不存在」的左边界，`-1` 表示「不存在」的右边界。 |
| 9‑12 | `for i, ch in enumerate(s):` | 单次遍历字符串，更新每个字符的左、右边界。 |
| 18‑21 | `l, r = left[c], right[c]` | 以字符 `c` 为起点的初始区间。 |
| 23‑31 | `while expanded: …` | **循环扩展**：只要区间内部出现了更左或更右的字符，就把区间向外扩展。循环结束时区间已经“稳定”。 |
| 33‑34 | `if l == left[c]: intervals.append((l, r))` | 只有左端点恰好等于字符 `c` 的最左出现位置，才算是「以 `c` 为左端点的最小合法子串」。 |
| 38 | `intervals.sort(key=lambda x: x[1])` | 按右端点升序排序，为后续的 **区间调度** 做准备。 |
| 41‑45 | `if l > prev_end: …` | 贪心选取不重叠区间：只要左端点在上一个选中区间的右端点之后，就可以加入答案。 |

#### 复杂度

- **时间复杂度**：`O(26 * n) = O(n)`  
  - 统计左/右出现位置：一次遍历 `O(n)`。  
  - 对每个字符进行区间扩展：每次扩展时遍历的区间长度总和不超过 `n`（因为每个字符最多被访问几次），所以整体仍是线性。  
  - 排序合法区间，区间数量最多为 26（每个字符至多产生一个），排序成本可以忽略。  
  - 因此整体是 **线性**，在 `n = 10⁵` 时也能轻松跑完。

- **空间复杂度**：`O(26) = O(1)`（不计答案本身）  
  - 只用了常数个长度为 26 的数组保存左右边界，及若干区间列表（最多 26 条）。  

> 与暴力解相比：  
> - 暴力解需要 **指数级** 时间和 **平方级** 空间，根本不可用。  
> - 最优解只用 **一次线性扫描**，空间几乎不增长，效率提升了天壤之别。

---

## 心得

- **核心技巧**：**区间的最小合法化 + 区间调度的贪心**。  
  先把每个字符的出现区间“压缩”到最小合法子串，再用“右端点最早”的贪心挑选不重叠区间，既保证子串数量最多，也保证总长度最小。

- **该技巧适用的题型**  
  1. **“最大不重叠子集”** 类问题（如《会议室安排》《Maximum Number of Non-Overlapping Intervals》）。  
  2. **“区间扩展/合并”** 需要先把区间扩展到满足某些约束（如《Partition Labels》）。  
  3. **“字符全覆盖”** 的子串问题（如《Minimum Window Substring》中的变形）。

- **一句话总结解题钥匙**  
  > **把每个字符的出现区间“压到最小”，再用“右端点最早”的贪心挑区间**。

---

## 反思

- **第一反应**：看到“子串必须包含字符的全部出现”就想到**枚举所有子串**，随后陷入指数级搜索的泥潭。  
- **最容易踩的坑**  
  1. **区间扩展的终止条件**：忘记在循环中检查 **所有字符**（不仅是起点字符）会导致得到的区间仍不合法。  
  2. **左端点必须等于字符的最左出现位置**：如果不加这个判断，会产生一些“可行但不是最小”的区间，导致贪心选取时出现不唯一的最小总长度解，违背题目唯一性。  
  3. **边界情况**：全字符串只有一种字符时，最小合法子串就是整串，代码要能够正确返回。  

- **下次遇到同类题，第一步该想到**  
  1. **先定位每个元素的全局区间**（左/右出现位置）。  
  2. **尝试把区间向外扩展直至“闭合”，得到最小合法区间**。  
  3. **使用区间调度的贪心**（右端点最早）挑选不冲突的区间。  

这样即可在 **线性时间** 内得到最优解，避免暴力搜索的陷阱。