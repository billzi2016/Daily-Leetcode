# #30. 串联所有单词的子串 / Substring with Concatenation of All Words

> 难度：困难 · 标签：Hash Table、String、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/substring-with-concatenation-of-all-words/)

---

## 题目（英文原版）

**Description**

You are given a string s and an array of strings words. All the strings of words are of the same length.
A concatenated string is a string that exactly contains all the strings of any permutation of words concatenated.
Return an array of the starting indices of all the concatenated substrings in s. You can return the answer in any order.

**Examples**

**Example 1:**

```
Input: s = "barfoothefoobarman", words = ["foo","bar"]
Output: [0,9]
Explanation:
The substring starting at 0 is "barfoo" . It is the concatenation of ["bar","foo"] which is a permutation of words . The substring starting at 9 is "foobar" . It is the concatenation of ["foo","bar"] which is a permutation of words .
```

**Example 2:**

```
Input: s = "wordgoodgoodgoodbestword", words = ["word","good","best","word"]
Output: []
Explanation:
There is no concatenated substring.
```

**Example 3:**

```
Input: s = "barfoofoobarthefoobarman", words = ["bar","foo","the"]
Output: [6,9,12]
Explanation:
The substring starting at 6 is "foobarthe" . It is the concatenation of ["foo","bar","the"] . The substring starting at 9 is "barthefoo" . It is the concatenation of ["bar","the","foo"] . The substring starting at 12 is "thefoobar" . It is the concatenation of ["the","foo","bar"] .
```

**Constraints**

- 1 <= s.length <= 104
- 1 <= words.length <= 5000
- 1 <= words[i].length <= 30
- s and words[i] consist of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串 `s` 和一个字符串数组 `words`。`words` 中所有字符串的长度相同。  
**串联字符串**（concatenated string）指恰好包含 `words` 中任意排列的所有字符串，且这些字符串依次相连得到的字符串。  
返回 `s` 中所有 **串联子串**（concatenated substring）的起始下标构成的数组。答案的顺序可以任意。

## 示例

### 示例 1
**输入**  
```text
s = "barfoothefoobarman", words = ["foo","bar"]
```
**输出**  
```text
[0,9]
```
**解释**  
起始下标为 `0` 的子串是 `"barfoo"`，它是 `["bar","foo"]` 的一种排列的串联结果。  
起始下标为 `9` 的子串是 `"foobar"`，它是 `["foo","bar"]` 的一种排列的串联结果。

### 示例 2
**输入**  
```text
s = "wordgoodgoodgoodbestword", words = ["word","good","best","word"]
```
**输出**  
```text
[]
```
**解释**  
不存在满足条件的串联子串。

### 示例 3
**输入**  
```text
s = "barfoofoobarthefoobarman", words = ["bar","foo","the"]
```
**输出**  
```text
[6,9,12]
```
**解释**  
- 起始下标为 `6` 的子串是 `"foobarthe"`，它是 `["foo","bar","the"]` 的一种排列的串联结果。  
- 起始下标为 `9` 的子串是 `"barthefoo"`，它是 `["bar","the","foo"]` 的一种排列的串联结果。  
- 起始下标为 `12` 的子串是 `"thefoobar"`，它是 `["the","foo","bar"]` 的一种排列的串联结果。

## 约束条件
- `1 <= s.length <= 10^4`
- `1 <= words.length <= 5000`
- `1 <= words[i].length <= 30`
- `s` 与 `words[i]` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：  
1. 先把 `words` 里所有单词的长度记为 `word_len`（题目保证它们相同），整个拼接后子串的长度就是 `total_len = word_len * len(words)`。  
2. 在原串 `s` 上从左到右尝试每一个可能的起始位置 `i`（`0 ≤ i ≤ len(s) - total_len`），取出长度为 `total_len` 的子串 `sub = s[i:i+total_len]`。  
3. 把 `sub` 再按照 `word_len` 切成若干块，每块看它是否正好对应 `words` 中的一个单词，且每个单词出现的次数要和 `words` 中一致。  

这一步可以用 **哈希表**（在 Python 里就是 `dict`）来记录 `words` 中每个单词出现的次数。哈希表就像一本“查词典”：给定单词（key），可以在 O(1) 时间内得到它出现了几次（value）。我们再用另一个临时哈希表统计 `sub` 中每个切块出现的次数，最后比较两个哈希表是否相同。

> 为什么这个方法一定能找出所有答案？  
因为我们枚举了所有可能的起始位置，并且对每个位置都完整检查了“是否恰好由这些单词组成”，只要有满足条件的子串，就一定会被记录下来。

#### 代码（Python）

```python
def findSubstring_bruteforce(s: str, words: list[str]) -> list[int]:
    if not s or not words:
        return []

    word_len = len(words[0])                     # 每个单词的长度
    total_len = word_len * len(words)            # 拼接后子串的总长度

    # 统计 words 中每个单词出现的次数，像查字典一样
    target_cnt = {}
    for w in words:
        target_cnt[w] = target_cnt.get(w, 0) + 1

    res = []
    # i 是可能的起始下标
    for i in range(len(s) - total_len + 1):
        # 取出长度为 total_len 的子串
        sub = s[i:i + total_len]

        # 把 sub 按照 word_len 切块并统计出现次数
        cur_cnt = {}
        valid = True
        for j in range(0, total_len, word_len):
            piece = sub[j:j + word_len]          # 取出第 j~j+word_len-1 的单词
            if piece not in target_cnt:          # 只要出现了不在 words 里的单词，就可以直接否定
                valid = False
                break
            cur_cnt[piece] = cur_cnt.get(piece, 0) + 1
            # 出现次数超过目标次数，同样可以提前结束
            if cur_cnt[piece] > target_cnt[piece]:
                valid = False
                break

        if valid and cur_cnt == target_cnt:      # 两个字典完全相同
            res.append(i)

    return res
```

#### 复杂度

- **时间复杂度**：`O(N * M * L)`  
  - `N = len(s)`（字符串长度）  
  - `M = len(words)`（单词数量）  
  - `L = len(words[0])`（每个单词的长度）  
  解释：我们要把每个可能的起始位置（最多 `N` 次）都检查一次，每次检查要切 `M` 块，每块的切取和哈希表操作是 `O(L)`（因为切片本身要复制 L 长度的子串），所以整体是 `N * M * L`。如果把 `L` 看成常数，这相当于 `O(N·M)`，在最坏情况下会非常慢。

- **空间复杂度**：`O(K)`  
  - `K` 为 `words` 中不同单词的数量（哈希表大小）。  
  解释：我们只用了两个字典来存放计数，最多占用与单词种类数相同的空间。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **重复遍历同一个子串的字符**。  
例如，`word_len = 3`，我们每次都把 `sub = s[i:i+total_len]` 完全重新切块，即使相邻的两个起始位置 `i` 与 `i+1` 只相差一个字符，几乎所有切块都是相同的，只是“窗口”整体向右平移了一位。

**滑动窗口**（Sliding Window）可以帮助我们复用已经算好的信息。核心想法：

1. 因为所有单词长度相同，我们可以把原串 `s` 按 `word_len` 的步长分成若干“行”。  
   - 例如 `word_len = 3`，我们分别从下标 `0,1,2` 这三个起点开始，每次向右跳 `3`，形成三条互不相交的序列。  
   - 这样每条序列内部的切块都是天然对齐的，方便我们一次只检查一个单词。

2. 对每一条序列使用 **固定大小的滑动窗口**：  
   - 窗口的大小是 `len(words)`（单词个数），窗口里维护一个哈希表 `window_cnt`，记录当前窗口内每个单词出现的次数。  
   - 当窗口右移一步（即加入一个新的单词 `right_word`），如果 `right_word` 在目标字典 `target_cnt` 中，我们就把它计数加一；如果出现次数超过目标次数，就要 **收缩左边界**（左指针向右移动）直到满足条件。  
   - 当窗口恰好包含 `len(words)` 个单词且计数全部匹配时，说明找到了一个合法的起始下标 `left`，把它加入答案。

3. 通过三条“行”分别遍历，能够覆盖所有可能的起始位置，且每个字符只会被加入或移出窗口 **一次**，从而把时间复杂度降到 `O(N * L)`，其中 `L = word_len`。

> **为什么滑动窗口可以做到 O(N)？**  
因为窗口的左指针和右指针只会单向前进，整个遍历过程每个字符最多被处理两次（一次加入窗口，一次移出窗口），没有重复的完整切块操作。

#### 代码（Python）

```python
def findSubstring(s: str, words: list[str]) -> list[int]:
    if not s or not words:
        return []

    word_len = len(words[0])                     # 每个单词的长度
    word_cnt = len(words)                        # 单词总数
    total_len = word_len * word_cnt              # 目标子串的长度
    n = len(s)

    # 目标哈希表：记录每个单词应该出现多少次
    target_cnt = {}
    for w in words:
        target_cnt[w] = target_cnt.get(w, 0) + 1

    res = []

    # 我们从 0,1,...,word_len-1 三个偏移量分别开始滑动窗口
    for offset in range(word_len):
        left = offset            # 窗口左边界
        right = offset           # 窗口右边界
        window_cnt = {}          # 当前窗口内单词计数

        # 右指针每次跨过一个完整单词
        while right + word_len <= n:
            word = s[right:right + word_len]   # 取出右侧的一个单词
            right += word_len

            # 如果这个单词根本不在目标集合里，窗口直接清空，左指针跳到 right 位置
            if word not in target_cnt:
                window_cnt.clear()
                left = right
                continue

            # 把 word 加入窗口计数
            window_cnt[word] = window_cnt.get(word, 0) + 1

            # 如果 word 出现次数超过目标次数，需要收缩左边界
            while window_cnt[word] > target_cnt[word]:
                left_word = s[left:left + word_len]
                window_cnt[left_word] -= 1
                left += word_len

            # 当窗口恰好包含 word_cnt 个单词时，说明找到了合法子串
            if right - left == total_len:
                res.append(left)

                # 为了继续向右搜索，先把最左侧的单词移出窗口
                left_word = s[left:left + word_len]
                window_cnt[left_word] -= 1
                left += word_len

    return res
```

#### 复杂度

- **时间复杂度**：`O(N * L)`  
  - `N = len(s)`，`L = word_len`。  
  - 解释：我们遍历了 `word_len` 条互不相交的序列，每条序列的长度至多 `N/L`，在每条序列里左指针和右指针各自最多前进 `N/L` 步，所以整体是 `O(N)`；乘上切片的代价 `O(L)`（取出一个单词要复制 `L` 长度的子串），得到 `O(N·L)`。在实际使用中 `L ≤ 30`，可以视作常数，几乎是线性时间。

- **空间复杂度**：`O(K)`  
  - `K` 为 `words` 中不同单词的种类数（哈希表大小）。  
  - 解释：我们只维护 `target_cnt`（固定）和 `window_cnt`（最多也只会存 K 种单词），不随 `s` 长度增长。

---

## 心得

- **核心技巧**：滑动窗口 + 哈希表计数  
  这两者组合可以高效地在字符串中寻找满足“固定长度、固定组成”的子串。

- **适用的题型**  
  1. “最长子串不含重复字符” 类似的窗口大小可变题目。  
  2. “找出所有异位词的起始下标” (LeetCode 438)——同样使用固定窗口、哈希表。  
  3. “最小覆盖子串” (LeetCode 76)——窗口大小可变，但同样依赖哈希表统计。

- **一句话总结解题钥匙**：**把问题转化为“窗口内的单词计数是否等于目标计数”，用滑动窗口一次遍历完成所有检查**。

---

## 反思

- **第一反应**：看到“所有单词长度相同”，自然想到把字符串切成等长块，然后枚举起始位置——这就是暴力思路。  
- **最容易踩的坑**  
  1. **边界条件**：`total_len` 可能超过 `len(s)`，此时直接返回空列表。  
  2. **单词不在字典里**：一旦出现不在 `words` 的单词，需要立刻清空窗口并把左指针跳到右指针后面，否则会产生错误的计数。  
  3. **计数超过目标**：窗口中某个单词出现次数超过 `words` 中的次数，需要循环收缩左边界，直到满足为止。  
- **下次遇到同类题**：第一步先判断是否可以 **按固定步长划分**（如单词长度相同），随后尝试 **滑动窗口 + 哈希计数** 的模板；如果步长不固定，再考虑使用 **前缀和** 或 **双指针** 的变体。