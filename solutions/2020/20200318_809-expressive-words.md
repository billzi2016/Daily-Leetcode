# #809. 可扩展的单词 / Expressive Words

> 难度：中等 · 标签：Array、Two Pointers、String · [LeetCode 链接](https://leetcode.com/problems/expressive-words/)

---

## 题目（英文原版）

**Description**

Sometimes people repeat letters to represent extra feeling. For example:
In these strings like "heeellooo", we have groups of adjacent letters that are all the same: "h", "eee", "ll", "ooo".
You are given a string s and an array of query strings words. A query word is stretchy if it can be made to be equal to s by any number of applications of the following extension operation: choose a group consisting of characters c, and add some number of characters c to the group so that the size of the group is three or more.
Return the number of query strings that are stretchy.

**Examples**

**Example 1:**

```
Input: s = "heeellooo", words = ["hello", "hi", "helo"]
Output: 1
Explanation: 
We can extend "e" and "o" in the word "hello" to get "heeellooo".
We can't extend "helo" to get "heeellooo" because the group "ll" is not size 3 or more.
```

**Example 2:**

```
Input: s = "zzzzzyyyyy", words = ["zzyy","zy","zyy"]
Output: 3
```

**Constraints**

- 1 <= s.length, words.length <= 100
- 1 <= words[i].length <= 100
- s and words[i] consist of lowercase letters.

---

## 题目（中文翻译）

有时候人们会重复字母来表达额外的情感。例如，在字符串 `"heeellooo"` 中，我们可以看到相邻且相同的字母形成的 **group（组）**：`"h"`、`"eee"`、`"ll"`、`"ooo"`。

给定一个字符串 `s` 和一个查询字符串数组 `words`。如果一个查询单词可以通过任意次数的 **extension operation（扩展操作）** 变得与 `s` 相同，则称该查询单词为 **stretchy（可伸展的）**。扩展操作的定义如下：选择由字符 `c` 组成的一个 **group（组）**，向该组中添加若干个字符 `c`，使得该组的大小至少为 3。

请返回 **stretchy（可伸展的）** 查询字符串的数量。

示例 1  
示例 2  
约束条件：

示例  
示例 1:  
**输入**: `s = "heeellooo"`, `words = ["hello", "hi", "helo"]`  
**输出**: `1`  
**解释**:  
我们可以把单词 `"hello"` 中的 `"e"` 和 `"o"` 扩展成 `"heeellooo"`。  
而 `"helo"` 无法扩展成 `"heeellooo"`，因为其中的 `"ll"` 组的大小不到 3。

示例 2:  
**输入**: `s = "zzzzzyyyyy"`, `words = ["zzyy","zy","zyy"]`  
**输出**: `3`

约束条件：  
- `1 <= s.length, words.length <= 100`  
- `1 <= words[i].length <= 100`  
- `s` 和 `words[i]` 仅由小写字母组成。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：把 **s** 和每个 **word** 当成两串字符，**从左到右逐段比较**。  
- 两串字符都可以划分为「相邻相同字符」的**分组**（例如 `"heeellooo"` → `h / eee / ll / ooo`）。  
- 对于同一位置的两个分组，记它们的字符为 `c`，长度分别为 `lenS`、`lenW`。  
  - 如果 `lenS < 3`（即原串的该组长度不足 3），则只能**完全相等**，也就是 `lenS == lenW`。  
  - 如果 `lenS >= 3`，则可以**伸展**：`lenW` 可以小于 `lenS`，只要 `lenW ≤ lenS` 即可（因为我们可以在 `word` 的这组上“加字符”到 `lenS`）。  
- 只要所有对应的分组都满足上述规则，`word` 就是 **stretchy**。  

**为什么这个方法一定正确？**  
- 伸展操作只能在 **s** 的某个分组上增加字符，**不能**把两个不同字符的分组合并，也不能把字符顺序改变。  
- 因此，只要两串在每个字符块的**顺序**和**字符种类**一致，并且长度关系满足规则，必然可以通过若干次“加字符”把 `word` 变成 `s`。  

**时间/空间复杂度**  
- 对每个 `word`，我们都要把它和 `s` 同时遍历一次，最多遍历 `len(s) + len(word)` 次字符。  
- 若 `n = words.length`，`L = max(len(s), len(word_i))`，总体时间是 **O(n·L)**，在最坏情况下约为 `100·100 = 10⁴`，足够快。  
- 只使用了常数级的额外变量（指针、计数），空间是 **O(1)**。  

#### 代码（Python）  

```python
def expressiveWords(s, words):
    """
    :type s: str
    :type words: List[str]
    :rtype: int
    """
    def is_stretchy(word: str) -> bool:
        i = j = 0                     # i 指向 s，j 指向 word
        while i < len(s) and j < len(word):
            if s[i] != word[j]:       # 不同字符，直接失败
                return False

            # 统计 s 中当前字符的连续个数
            ch = s[i]
            cnt_s = 0
            while i < len(s) and s[i] == ch:
                i += 1
                cnt_s += 1

            # 统计 word 中当前字符的连续个数
            cnt_w = 0
            while j < len(word) and word[j] == ch:
                j += 1
                cnt_w += 1

            # 判断长度关系是否满足伸展规则
            if cnt_s < 3 and cnt_s != cnt_w:   # 组太短，必须完全相等
                return False
            if cnt_s >= 3 and cnt_w > cnt_s:   # word 的这组比 s 长，无法压缩
                return False
        # 两个指针必须同时走到字符串末尾
        return i == len(s) and j == len(word)

    # 统计满足条件的单词数量
    return sum(is_stretchy(w) for w in words)
```

#### 复杂度  

- **时间复杂度**：`O(n·L)`  
  - `n` 为单词数量，`L` 为 `s` 与每个单词的最大长度。  
  - 大白话：如果有 100 条单词，每条最多 100 个字母，最多要检查 10 000 次字符，算得很快。  
- **空间复杂度**：`O(1)`  
  - 只用了几个指针和计数器，和输入规模无关。  

---  

### 2. 最优解  

#### 思路  

暴力解已经是 **线性** 的了，真正的“优化点”在于**重复工作**：  
- 对每个 `word` 我们都要**重新遍历一次 `s`** 来统计每个字符块的长度。  
- 其实 `s` 的分组信息是固定的，可以**一次性预处理**，随后所有单词直接对比预处理好的结果，省去重复扫描。  

**优化步骤**  

1. **预处理 `s`**  
   - 把 `s` 转换成 `[(char1, cnt1), (char2, cnt2), ...]` 的列表，称为 `groups_s`。  
   - 这一步只做一次，时间 `O(len(s))`，空间 `O(len(s))`（最多 100，完全可接受）。  

2. **遍历每个 `word`**  
   - 同样把 `word` 按字符块划分得到 `groups_w`。  
   - 只要 `groups_s` 与 `groups_w` 的 **长度**（块数）不相等，直接不是 stretchy。  
   - 否则逐块比较：  
     - 字符必须相同。  
     - 若 `cnt_s < 3`，则必须 **完全相等** (`cnt_w == cnt_s`)。  
     - 若 `cnt_s >= 3`，则只要 `cnt_w ≤ cnt_s` 即可（因为可以伸展到 `cnt_s`）。  

3. **计数**  
   - 满足所有块规则的单词计入答案。  

**核心数据结构**：  
- **列表**（List）保存分组信息。把字符块视作“一个整体”，类似把一段文字当作一本书的章节。  
- **指针**（两个索引）遍历两个列表，像在两本章节目录中对应章节逐一比对。  

**为什么更好**：  
- 预处理把 `s` 的扫描次数从 `O(n·len(s))` 降到 **一次**，对每个单词只遍历它自己的字符，整体时间仍是 `O(n·L)`，但常数更小。  
- 代码结构更清晰，易于调试。  

#### 代码（Python）  

```python
def expressiveWords(s, words):
    """
    最优实现：先把 s 划分成 (字符, 连续个数) 的组，
    再对每个 word 与这些组逐一比对。
    """
    # ---------- 1. 预处理 s ----------
    def get_groups(string: str):
        """把字符串转成 [(char, count), ...] 的形式"""
        groups = []
        i = 0
        while i < len(string):
            ch = string[i]
            cnt = 0
            while i < len(string) and string[i] == ch:
                i += 1
                cnt += 1
            groups.append((ch, cnt))
        return groups

    groups_s = get_groups(s)          # 只做一次

    # ---------- 2. 判断单词 ----------
    def is_stretchy(word: str) -> bool:
        groups_w = get_groups(word)

        # 组数不相等，直接不可能相等
        if len(groups_w) != len(groups_s):
            return False

        # 逐组比较
        for (ch_s, cnt_s), (ch_w, cnt_w) in zip(groups_s, groups_w):
            if ch_s != ch_w:               # 不同字符，失败
                return False
            if cnt_s < 3:
                if cnt_s != cnt_w:         # 组太短，必须完全匹配
                    return False
            else:                           # cnt_s >= 3，允许伸展
                if cnt_w > cnt_s:          # word 的这组比 s 长，无法压缩
                    return False
        return True

    # ---------- 3. 统计 ----------
    return sum(is_stretchy(w) for w in words)
```

#### 复杂度  

- **时间复杂度**：`O(len(s) + Σ len(word_i))`  
  - 预处理 `s` 只用一次 `O(len(s))`。  
  - 对每个单词只遍历一次自身字符，累计长度为所有单词的总字符数。  
  - 与暴力解的渐进上界相同，但实际运行更快（少了对 `s` 的重复遍历）。  

- **空间复杂度**：`O(len(s))`  
  - 需要存放 `s` 的分组列表，最多 100 项，属于常数级别的额外空间。  

---  

## 心得  

- **核心技巧**：把字符串拆成「相同字符的连续块」进行**分组比较**。  
- **适用场景**：  
  1. **压缩/展开** 类问题（如 *String Compression*、*Compressed String Queries*）。  
  2. **模式匹配** 中需要比较字符出现次数的题目（如 *Repeated Substring Pattern*、*Valid Palindrome III* 中的计数版）。  
- **解题钥匙**：**先把结构化信息抽取出来（分组），再逐块比对**，这样可以把“字符顺序”和“出现次数”两个维度都清晰呈现。  

---  

## 反思  

- **第一反应**：看到“可以把字符组伸长到 3 或以上”，立刻想到**把两个字符串按字符块拆开**，逐块检查长度关系。  
- **最容易踩的坑**：  
  - 忘记**长度为 3 以上的组必须至少是 3**，否则会错误地把 `len_s = 2, len_w = 1` 当作可伸展。  
  - 忽视**组数不相等**的情况，会导致指针越界或误判。  
  - 对于 `word` 中的某组比 `s` 长的情况（`cnt_w > cnt_s`）要直接返回 `False`，因为我们只能**加字符**，不能删。  
- **下次遇到同类题**，第一步应该是**把所有涉及“连续相同字符”或“出现次数” 的信息抽取成列表**，再在这个更简洁的结构上进行比较或动态规划。