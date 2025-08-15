# #3305. **包含所有元音且恰好有 K 个辅音的子字符串计数 I** / Count of Substrings Containing Every Vowel and K Consonants I

> 难度：中等 · 标签：Hash Table、String、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/count-of-substrings-containing-every-vowel-and-k-consonants-i/)

---

## 题目（英文原版）

**Description**

You are given a string word and a non-negative integer k.
Return the total number of substrings of word that contain every vowel ('a', 'e', 'i', 'o', and 'u') at least once and exactly k consonants.

**Examples**

**Example 1:**

```
Input: word = "aeioqq", k = 1
Output: 0
Explanation:
There is no substring with every vowel.
```

**Example 2:**

```
Input: word = "aeiou", k = 0
Output: 1
Explanation:
The only substring with every vowel and zero consonants is word[0..4] , which is "aeiou" .
```

**Example 3:**

```
Input: word = " ieaouqqieaouqq ", k = 1
Output: 3
Explanation:
The substrings with every vowel and one consonant are:
```

**Constraints**

- 5 <= word.length <= 250
- word consists only of lowercase English letters.
- 0 <= k <= word.length - 5

---

## 题目（中文翻译）

给定一个字符串 `word` 和一个非负整数 `k`。  
返回 `word` 中满足以下条件的子字符串（substrings）总数：

- 至少包含每个元音字母 `'a'`, `'e'`, `'i'`, `'o'`, `'u'` 各一次；
- 恰好包含 `k` 个辅音（consonants）。

**示例 1**  
**输入**: `word = "aeioqq", k = 1`  
**输出**: `0`  
**解释**: 没有子字符串同时包含所有元音。

**示例 2**  
**输入**: `word = "aeiou", k = 0`  
**输出**: `1`  
**解释**: 唯一满足条件的子字符串是 `word[0..4]`，即 `"aeiou"`，它包含所有元音且没有辅音。

**示例 3**  
**输入**: `word = "ieaouqqieaouqq", k = 1`  
**输出**: `3`  
**解释**: 符合条件的子字符串有：

（此处列出具体子字符串，原题略）

**约束条件**  
- `5 <= word.length <= 250`  
- `word` 仅由小写英文字母组成。  
- `0 <= k <= word.length - 5`   (因为至少需要 5 个字符来容纳所有元音)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有** 子串都枚举出来，逐个检查它们是否满足：

1. 包含 `'a','e','i','o','u'` 五个元音 **至少** 出现一次。  
2. 恰好有 `k` 个辅音（即不是元音的字母）。

> **数据结构类比**：  
> - 把字符串看成一本书的连续页面。枚举子串就像把每一段连续的页面都翻一遍。  
> - 检查元音出现情况可以用 **哈希表**（在 Python 中用 `dict` 或 `set`）来实现，哈希表就像一本“查字典”，`key` 是字母，`value` 记录它出现的次数。

**为什么一定对？**  
只要遍历了所有可能的起止位置 `(l, r)`，就不可能漏掉任何满足条件的子串；对每个子串的检查也完全覆盖了题目要求的两条规则。

**复杂度分析（大白话）**  

- 枚举子串的起点有 `n` 种，终点也有 `n` 种（`n = len(word)`），所以总共要检查大约 `n·n/2` 个子串，时间复杂度记作 **O(n²)**。  
  > 举例：如果 `n = 100`，大约要检查 5,000 条子串，算得上“很多”，但对本题的 `n ≤ 250` 完全可以接受。  
- 检查一个子串时，只需要遍历它本身的字符（最坏情况下是 `O(n)`），但因为子串长度在整个枚举过程中已经被累计进 `n²`，这里不再额外计入。  
- 额外使用的哈希表最多保存 5 个元音以及若干辅音计数，空间最多是 **O(1)**（常数级），不随 `n` 增长。

#### 代码（Python）

```python
def count_substrings_brute(word: str, k: int) -> int:
    vowels = {'a', 'e', 'i', 'o', 'u'}          # 元音集合，像字典的“查找表”
    n = len(word)
    ans = 0

    # 枚举所有左端点 l
    for l in range(n):
        vowel_cnt = {ch: 0 for ch in vowels}   # 记录五个元音出现次数
        cons_cnt = 0                           # 记录辅音个数

        # 右端点 r 从 l 开始向右扩展
        for r in range(l, n):
            ch = word[r]
            if ch in vowels:                   # 元音 → 在哈希表里计数
                vowel_cnt[ch] += 1
            else:                              # 辅音 → 直接计数
                cons_cnt += 1

            # 检查当前子串是否满足条件
            if cons_cnt == k and all(vowel_cnt[v] > 0 for v in vowels):
                ans += 1

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)` — “平方级”，因为我们把所有 `(左, 右)` 组合都遍历了一遍。  
- **空间复杂度**：`O(1)` — 只用了常数个变量（哈希表大小固定为 5）。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **重复遍历同一个字符**：当左端点 `l` 向右移动时，右端点 `r` 仍然会从 `l` 开始重新扫描，这导致了二次甚至多次遍历同一段子串。

我们可以利用 **滑动窗口（双指针）** 的思想，把左端点 `left` 和右端点 `right` 维护成一个“活动窗口”。窗口只会向右移动，左指针只会向右收缩，一旦窗口满足条件，就可以直接统计以 `right` 为结尾、满足要求的子串数量，而不必再枚举所有左端点。

关键点：

1. **窗口状态**  
   - `cnt_vowel[ch]`：记录窗口中每个元音出现的次数（5 个计数器）。  
   - `cnt_cons`：窗口中辅音的个数。  
   - `full_vowel`：一个布尔值，表示五个元音是否全部出现（`cnt_vowel` 中每个计数都 > 0）。

2. **移动右指针**  
   把 `right` 向右推进，把新字符加入窗口，更新相应计数。

3. **收缩左指针**  
   当窗口的辅音数 **超过** `k` 时，必须把左端点右移，直到 `cnt_cons ≤ k`。这一步保证窗口里 **恰好**（或不超过）`k` 个辅音。

4. **计数**  
   - 当窗口已经包含所有元音且恰好有 `k` 个辅音时，**以当前 `right` 为右端点的所有合法子串**的左端点必然位于 `left` 到 `right` 之间的某个位置。  
   - 为了避免遗漏，我们记录 **最左** 能让窗口满足条件的左指针 `valid_left`。从 `valid_left` 到 `right`（含）之间的每一个左端点，都对应一个合法子串。于是本轮可以直接把 `right - valid_left + 1` 加到答案中。

5. **为什么只需要记录一个 `valid_left`**  
   - 当我们继续把右指针往右移动时，窗口只会 **扩大**，元音的出现情况只能从 “不全” 变成 “全”，不会再回到 “不全”。  
   - 同时，收缩左指针只会让辅音数 **减小**，所以一旦窗口在某个位置满足 “全元音 + 恰好 k 辅音”，再往右走时只会产生更多满足条件的子串（左端点可以保持不变或进一步右移），不需要重新遍历所有左端点。

> **类比**：想象有一条装满水果的传送带，左指针是“取水果的起点”，右指针是“当前看到的水果”。只要传送带上出现了所有五种水果且恰好有 `k` 个非水果（辅音），那么从起点到当前位置的每一种取法都是合法的。

#### 代码（Python）

```python
def count_substrings_opt(word: str, k: int) -> int:
    vowels = {'a', 'e', 'i', 'o', 'u'}
    # 统计窗口中每个元音出现次数
    cnt_vowel = {v: 0 for v in vowels}
    cnt_cons = 0                # 辅音计数
    left = 0                    # 窗口左端
    valid_left = 0              # 第一个能够让窗口满足“全元音 + k 辅音”的左端
    ans = 0
    n = len(word)

    for right in range(n):
        ch = word[right]
        if ch in vowels:
            cnt_vowel[ch] += 1
        else:
            cnt_cons += 1

        # 1）如果辅音数超过 k，需要收缩左指针直到 ≤ k
        while cnt_cons > k:
            ch_left = word[left]
            if ch_left in vowels:
                cnt_vowel[ch_left] -= 1
            else:
                cnt_cons -= 1
            left += 1
            # 收缩后，valid_left 也必须同步右移，因为左端已经不在窗口内了
            if valid_left < left:
                valid_left = left

        # 2）检查窗口是否已经拥有所有元音
        while (all(cnt_vowel[v] > 0 for v in vowels)      # 全元音
               and cnt_cons == k                         # 正好 k 辅音
               and valid_left < left):                   # valid_left 还在窗口左侧
            # 若 valid_left 落在 left 之前，说明左端已经被收缩，需同步
            valid_left = left

        # 3）如果当前窗口满足条件，统计以 right 为右端的子串数量
        if all(cnt_vowel[v] > 0 for v in vowels) and cnt_cons == k:
            # 从 valid_left 到 right（包含）都是合法左端
            ans += (right - valid_left + 1)

    return ans
```

> **代码解释（关键行中文注释）**

```python
for right in range(n):                     # 右指针一步步往右走
    ch = word[right]
    if ch in vowels:                       # 元音出现，计数加一
        cnt_vowel[ch] += 1
    else:                                  # 辅音出现，计数加一
        cnt_cons += 1

    while cnt_cons > k:                     # 辅音超过 k，左指针收缩
        ch_left = word[left]
        if ch_left in vowels:
            cnt_vowel[ch_left] -= 1
        else:
            cnt_cons -= 1
        left += 1
        if valid_left < left:               # valid_left 不能落在窗口外
            valid_left = left

    # 此时窗口内辅音 ≤ k，检查是否已经拥有全部元音且恰好 k 个辅音
    if all(cnt_vowel[v] > 0 for v in vowels) and cnt_cons == k:
        ans += (right - valid_left + 1)     # 以 right 为右端的合法子串数
```

#### 复杂度

- **时间复杂度**：`O(n)` — 每个字符最多被右指针“进入”一次、左指针“移出”一次，所有计数和检查都是 **常数时间** 操作。相较于暴力的 `O(n²)`，这里的运行速度提升了数量级。  
- **空间复杂度**：`O(1)` — 只用了 5 个元音计数器、一个辅音计数器以及若干指针，全部是常数大小。

---

## 心得

- **核心技巧**：滑动窗口（双指针）结合**计数器**和**全覆盖判定**（五个元音全部出现）。  
- **适用的题型**（可迁移的思路）  
  1. “包含全部字符集合且满足长度/计数限制”的子串统计（如 **包含所有字母的最短子串**）。  
  2. “恰好 k 个特定字符”的子串计数（如 **恰好 k 个数字的子数组**）。  
  3. “窗口内满足多重条件”的计数问题（如 **最多 K 个不同字符的子串**）。
- **一句话总结**：**把窗口不断往右推进，同时用左指针把多余的字符剔除，只要窗口满足所有条件，就能一次性算出以当前右端为止的全部合法子串**。

---

## 反思

- **第一反应**：直接把所有子串枚举一遍检查——最安全也最容易想到的办法。  
- **最容易踩的坑**  
  - **边界条件**：`k = 0` 时只能接受全元音的子串，需要确保左指针收缩不会误删元音。  
  - **辅音计数**：忘记在左指针移动时把辅音计数减一，会导致窗口永远“超额”。  
  - **全元音判定**：使用 `all(cnt_vowel[v] > 0 for v in vowels)` 必须每次都检查，否则可能把缺少某个元音的窗口算进去。  
- **下次遇到同类题**：第一步先问自己“是否可以用滑动窗口把‘多余’的字符（这里是超出 k 的辅音）逐出？”如果答案是“可以”，就立刻搭建双指针框架，再在窗口内部维护需要的计数/标记即可。