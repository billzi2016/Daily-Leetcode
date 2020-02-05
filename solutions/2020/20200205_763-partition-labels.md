# #763. **分割标签** / Partition Labels

> 难度：中等 · 标签：Hash Table、Two Pointers、String、Greedy · [LeetCode 链接](https://leetcode.com/problems/partition-labels/)

---

## 题目（英文原版）

**Description**

You are given a string s. We want to partition the string into as many parts as possible so that each letter appears in at most one part. For example, the string "ababcc" can be partitioned into ["abab", "cc"], but partitions such as ["aba", "bcc"] or ["ab", "ab", "cc"] are invalid.
Note that the partition is done so that after concatenating all the parts in order, the resultant string should be s.
Return a list of integers representing the size of these parts.

**Examples**

**Example 1:**

```
Input: s = "ababcbacadefegdehijhklij"
Output: [9,7,8]
Explanation:
The partition is "ababcbaca", "defegde", "hijhklij".
This is a partition so that each letter appears in at most one part.
A partition like "ababcbacadefegde", "hijhklij" is incorrect, because it splits s into less parts.
```

**Example 2:**

```
Input: s = "eccbbbbdec"
Output: [10]
```

**Constraints**

- 1 <= s.length <= 500
- s consists of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串 `s`。我们希望尽可能多地将该字符串**分割**（partition）成若干部分，使得每个字母至多出现在一个部分中。例如，字符串 `"ababcc"` 可以分割为 `["abab", "cc"]`，但 `["aba", "bcc"]` 或 `["ab", "ab", "cc"]` 这样的分割是无效的。  
需要注意的是，分割后按顺序将所有部分连接起来得到的结果字符串应当等于原始字符串 `s`。  

返回一个整数列表，表示这些部分的大小。

**示例 1**

```
Input: s = "ababcbacadefegdehijhklij"
Output: [9,7,8]
Explanation:
划分得到的子串为 "ababcbaca", "defegde", "hijhklij"。
每个字母都出现在至多一个子串中，满足要求。
如果划分为 "ababcbacadefegde", "hijhklij"，虽然仍满足字母不重复的条件，但得到的子串数量更少，因此不是最大化的划分。
```

**示例 2**

```
Input: s = "eccbbbbdec"
Output: [10]
Explanation:
整个字符串只能划分为一个部分，长度为 10。
```

**约束条件**

- `1 <= s.length <= 500`
- `s` 只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的切分方式都列举出来**，然后逐个检查每个切分是否满足「每个字母只出现在一个区间」的要求。  

- **数据结构**  
  - `list` 用来保存当前的切分点（类似在一段文字里插入分隔符）。  
  - `set` 用来快速判断一个区间里出现的字母集合（把字母当成「字典」里的词，`set` 就是记录已经出现过的词）。  

- **正确性**  
  - 只要枚举了**所有**合法的切分方式，就不会漏掉答案。  
  - 对每一种切分，只要检查每个区间内部的字母集合是否与其它区间的集合相交（即出现重复），不相交则该切分合法。  

- **复杂度**  
  - 对长度为 `n` 的字符串，切分点有 `n-1` 个位置，每个位置可以「切」也可以「不切」，于是可能的切分方式是 `2^(n-1)` 种，呈指数级增长。  
  - 检查一个切分是否合法需要遍历整个字符串并使用 `set` 记录字母，时间是 `O(n)`，空间是 `O(1)`（因为字母表只有 26 个小写字母）。  
  - 综合下来，**时间复杂度是 O(n·2^(n-1))**，在最坏情况下几乎不可能在 500 长度的输入上跑完。  

#### 代码（Python）

```python
def partition_labels_bruteforce(s: str):
    n = len(s)
    ans = []

    # 递归枚举所有切分点，pos 表示当前处理到的字符位置，cuts 保存已经决定的切分位置
    def dfs(pos: int, cuts: list):
        if pos == n:                      # 已经走到字符串末尾，得到一种完整切分
            if is_valid(cuts):            # 检查是否合法
                # 根据切分点算出每段长度并加入答案
                sizes = []
                prev = 0
                for cut in cuts:
                    sizes.append(cut - prev + 1)
                    prev = cut + 1
                sizes.append(n - prev)    # 最后一段
                ans.append(sizes)
            return

        # 方案一：在 pos 处不切，继续往后走
        dfs(pos + 1, cuts)

        # 方案二：在 pos 处切（前提是 pos 不是最后一个字符）
        if pos < n - 1:
            dfs(pos + 1, cuts + [pos])

    # 判断一组切分点 cuts 是否满足「每个字母只在一个区间」的条件
    def is_valid(cuts: list) -> bool:
        intervals = []
        prev = 0
        for cut in cuts:
            intervals.append((prev, cut))
            prev = cut + 1
        intervals.append((prev, n - 1))

        # 对每个区间统计出现的字符
        seen = {}
        for idx, (l, r) in enumerate(intervals):
            cur_set = set()
            for i in range(l, r + 1):
                ch = s[i]
                if ch in cur_set:          # 同一区间内部出现重复不影响
                    continue
                if ch in seen:            # 已经在别的区间出现过，非法
                    return False
                cur_set.add(ch)
            for ch in cur_set:
                seen[ch] = idx
        return True

    dfs(0, [])
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n·2^(n-1))`  
  - 解释：`2^(n-1)` 是所有可能的切分方式数量，`n` 是每次检查是否合法需要遍历的字符数。  
- **空间复杂度**：`O(n)`（递归栈深度 + 保存切分点的列表）  

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于枚举所有切分方式**。实际上我们根本不需要尝试所有可能，只要**贪心地把每段扩展到足够大，使得其中出现的每个字母的所有出现位置都被包含**，就能得到唯一的最优划分。  

**关键观察**：

1. 对于任意一个字母 `c`，它在字符串中的**最左位置**和**最右位置**是固定的。  
2. 若我们决定从位置 `i` 开始一个新段，那么这个段的右边界一定要至少延伸到 `s[i]` 最后一次出现的位置 `last[s[i]]`。  
3. 当我们把右边界延伸到 `last[s[i]]` 后，段内可能出现其他字母 `x`，这些字母的最右出现位置可能更靠右，于是我们继续把右边界向右扩展到 `max(last[x])`，直到**遍历到的下标等于当前右边界**，说明这段已经囊括了所有涉及的字母，不能再往前截断。  

于是我们得到**两指针/贪心**的线性算法：

- 第一次遍历记录每个字母的**最后出现下标**（哈希表 `last`，类似查字典，字母是词，页码是最后出现位置）。  
- 第二次遍历用两个指针 `start`（本段起点）和 `end`（本段最右边界）：
  - 对每个字符 `c`，把 `end = max(end, last[c])`，即不断扩展右边界。  
  - 当遍历的下标 `i` 达到 `end` 时，说明当前段已经完整，记录段长 `end - start + 1`，然后把 `start = i + 1` 开启新段。  

**为什么贪心有效**？

- 如果在 `i == end` 时提前截断，那么必然会把某个字母的后续出现留到后面的段里，违背「每个字母只出现一次」的要求。  
- 只要等到 `i == end` 再截断，就已经把本段涉及的所有字母的出现全部覆盖，后面的字符与本段不再有交集，继续向后划分不会影响已经得到的段数。  

#### 代码（Python）

```python
def partition_labels(s: str):
    """
    贪心 + 哈希表（记录每个字符的最右出现位置） + 双指针
    返回每段的长度列表
    """
    # 1️⃣ 记录每个字符最后出现的下标
    #   哈希表就像一本字典，key 是字母，value 是它在书中出现的最后一页
    last = {ch: i for i, ch in enumerate(s)}   # O(n) 时间，O(Alphabet) 空间

    ans = []
    start = 0          # 当前段的起点
    end = 0            # 当前段能够扩展到的最右边界

    # 2️⃣ 再遍历一遍字符串，动态更新 end
    for i, ch in enumerate(s):
        # 把右边界延伸到该字符最后出现的位置
        end = max(end, last[ch])   # 如果后面还有相同字符，就把段拉长

        # 当遍历的下标恰好到达右边界，说明本段可以结束
        if i == end:
            ans.append(end - start + 1)   # 记录本段长度
            start = i + 1                 # 新段从下一个字符开始

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 第一次遍历建立 `last` 表是 `O(n)`，第二次遍历每个字符只做常数次操作，合计线性时间。  
  - 与暴力解的指数时间相比，几乎瞬间完成，即使 `n=500` 也毫无压力。  
- **空间复杂度**：`O(1)`（严格来说是 `O(Alphabet)`，字母表大小固定为 26）  
  - 只需要存放每个字母的最后位置以及少量指针变量，和输入规模无关。  

---

## 心得

- **核心技巧**：**记录每个字符的最右出现位置 + 贪心扩展区间**。  
- **适用的题型**  
  1. 需要把序列划分为满足某种“局部不冲突”条件的最大（或最小）分段，如 **“Maximum Number of Non‑Overlapping Substrings”**。  
  2. 需要一次遍历决定区间边界的题目，例如 **“Longest Substring with At Most K Distinct Characters”**（滑动窗口的思路类似）。  
- **解题钥匙**：**把“出现范围”当成区间，始终让区间扩展到能够覆盖所有出现的最远点，再在恰好到达右端时截断**。

---

## 反思

- **第一反应**：看到「每个字母只能出现在一个区间」就想到「记录每个字母出现的范围」以及「把区间合并」，于是自然联想到哈希表和区间合并的思路。  
- **最容易踩的坑**  
  - 忘记把 **所有**字符的最右位置都考虑进去，只用当前字符的最右位置会导致区间提前截断。  
  - 处理结束条件时写成 `if i == start:`（错误）而不是 `if i == end:`，导致永远不能形成正确的分段。  
  - 边界情况：字符串全由同一个字符组成时，`last` 的值等于最后下标，算法仍能返回 `[len(s)]`。  
- **下次遇到同类题**，第一步应该 **统计每个元素的出现区间**（最左、最右），再 **在遍历中动态合并区间**，用「区间合并」或「贪心截断」的视角来思考。