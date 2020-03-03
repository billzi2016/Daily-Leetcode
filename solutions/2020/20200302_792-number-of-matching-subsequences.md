# #792. 匹配子序列的数量 / Number of Matching Subsequences

> 难度：中等 · 标签：Array、Hash Table、String、Binary Search、Dynamic Programming、Trie、Sorting · [LeetCode 链接](https://leetcode.com/problems/number-of-matching-subsequences/)

---

## 题目（英文原版）

**Description**

Given a string s and an array of strings words, return the number of words[i] that is a subsequence of s.
A subsequence of a string is a new string generated from the original string with some characters (can be none) deleted without changing the relative order of the remaining characters.

**Examples**

**Example 1:**

```
Input: s = "abcde", words = ["a","bb","acd","ace"]
Output: 3
Explanation: There are three strings in words that are a subsequence of s: "a", "acd", "ace".
```

**Example 2:**

```
Input: s = "dsahjpjauf", words = ["ahjpjau","ja","ahbwzgqnuk","tnmlanowax"]
Output: 2
```

**Constraints**

- 1 <= s.length <= 5 * 104
- 1 <= words.length <= 5000
- 1 <= words[i].length <= 50
- s and words[i] consist of only lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串 **s** 和一个字符串数组 **words**，返回 **words[i]** 中是 **s** 的子序列（subsequence）的字符串的数量。

子序列（subsequence）是指从原字符串中删除若干字符（可以不删），但不改变剩余字符相对顺序而得到的新字符串。

**示例 1**  
**输入**: `s = "abcde", words = ["a","bb","acd","ace"]`  
**输出**: `3`  
**解释**: 在 `words` 中有三个字符串是 `s` 的子序列: `"a"`, `"acd"`, `"ace"`。

**示例 2**  
**输入**: `s = "dsahjpjauf", words = ["ahjpjau","ja","ahbwzgqnuk","tnmlanowax"]`  
**输出**: `2`  
**解释**: 在 `words` 中有两个字符串是 `s` 的子序列: `"ahjpjau"` 和 `"ja"`。

**约束条件**  
- `1 <= s.length <= 5 * 10^4`  
- `1 <= words.length <= 5000`  
- `1 <= words[i].length <= 50`  
- `s` 和 `words[i]` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每个 `words[i]` 都单独拿出来，和 `s` 做一次“是否为子序列”的检查**。  
检查子序列可以用**双指针**来完成：

1. 把指针 `i` 放在 `s` 的开头，指针 `j` 放在当前单词 `w` 的开头。  
2. 从左到右遍历 `s`，如果 `s[i] == w[j]`，说明找到了 `w` 中的下一个字符，`j` 往右走一步。  
3. 当 `j` 走到 `w` 的末尾时，说明所有字符都已经匹配成功，`w` 是 `s` 的子序列。  
4. 如果遍历完 `s` 仍然没有把 `j` 移动到末尾，则 `w` 不是子序列。

> **类比**：把 `s` 想成一本长篇小说，`w` 是一本小册子。我们把小册子里的每一页（字符）依次在小说里找对应的句子（字符），只要顺序不乱，就算匹配成功。

因为每个单词都要遍历一次 `s`（最坏情况下全部字符都要比较），所以这个方法是**正确的**，只是效率不高。

#### 代码（Python）

```python
def is_subsequence(s: str, w: str) -> bool:
    """判断 w 是否是 s 的子序列，双指针实现"""
    i = j = 0
    while i < len(s) and j < len(w):
        if s[i] == w[j]:          # 找到匹配字符，w 向后走一步
            j += 1
        i += 1                    # s 必须一直往后走
    return j == len(w)           # j 能走到末尾说明全部匹配成功

def numMatchingSubseq_bruteforce(s: str, words: list[str]) -> int:
    cnt = 0
    for w in words:
        if is_subsequence(s, w):
            cnt += 1
    return cnt
```

#### 复杂度

- **时间复杂度**：`O(|s| * |words|)`  
  这里的 `|s|` 是字符串 `s` 的长度，`|words|` 是数组 `words` 的长度（即单词个数）。  
  直观上可以把它想成“每个单词都要走完整本小说一次”，如果 `s` 长 10⁴，`words` 有 5 000 个，最坏会有 5 000 × 10⁴ = 5 × 10⁷ 次字符比较，显得有点慢。

- **空间复杂度**：`O(1)`（不计输入占用的空间）  
  只用了几个指针变量，额外的内存几乎为零。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每遍历一次 `s` 都要重新检查所有单词**。  
我们可以把 **“所有单词的检查过程”** 与 **“遍历 `s` 的过程”** 合并，做到“一遍 `s`，一次性把所有单词推进”。  

核心思想是 **把每个单词按照它当前期待的字符分到 26 个“等待队列”里**（类似字典查询，`a`~`z` 各自对应一个列表），然后顺序读取 `s`，把对应字符的队列一次性取出并推进。

具体步骤如下：

1. **准备 26 个桶**（用列表或 `defaultdict(list)`），下标 `0~25` 分别代表字符 `'a'~'z'`。  
   每个桶里存放的是 **(word, pos)**，其中 `word` 是单词本身（或它的引用），`pos` 是当前已经匹配到的字符位置（即下一个要匹配的字符在 `word` 中的下标）。

2. **把所有单词放进对应的第一个字符桶**。  
   例如单词 `"acd"`，它的第一个字符是 `'a'`，于是把 `( "acd", 0 )` 放进 `'a'` 的桶。

3. **遍历主字符串 `s`**，对每个字符 `c`：
   - 取出 **当前字符对应桶**（比如 `c = 'd'` 就取出 `'d'` 的桶），这里的取出操作要一次性全部取走，因为这些单词已经“看到了”它们期待的字符。
   - 对取出的每个 `(word, pos)`：
     - `pos += 1` 表示已经匹配了一个字符，准备匹配下一个。
     - 如果 `pos == len(word)`，说明这个单词已经全部匹配成功，计数器 `ans` 加一。
     - 否则，把 `(word, pos)` 放进 **下一个期待字符** 的桶里（`word[pos]`）。

4. **遍历结束后，`ans` 就是答案**。

> **类比**：把 26 个桶想成 26 条不同颜色的“传送带”。每个单词最初站在它第一个字母对应的传送带上，等到 `s` 走到这个字母时，传送带上的所有单词一起“上车”，向前走一步，随后跳到它们下一个字母对应的传送带。所有单词在传送带上跑完，谁先跑完就算匹配成功。

这样每个字符在 `s` 中只被访问一次，每个单词的每个字符也只被“搬运”一次，**总工作量是 `O(|s| + Σ|words[i]|)`**，远远小于暴力的 `O(|s|·|words|)`。

#### 代码（Python）

```python
from collections import defaultdict, deque
from typing import List, Tuple

def numMatchingSubseq_optimal(s: str, words: List[str]) -> int:
    # 1. 26 条等待队列，用 deque 方便弹出左侧元素
    waiting = defaultdict(deque)          # key: 字符, value: deque[(word, pos)]

    # 2. 把所有单词放入它们第一个字符对应的队列
    for w in words:
        # 把 (word, 当前已经匹配到的位置) 放进去，初始位置是 0
        waiting[w[0]].append((w, 0))

    ans = 0  # 记录匹配成功的单词数

    # 3. 依次遍历主字符串 s
    for ch in s:
        # 取出当前字符对应的所有待匹配项（一次性取走，防止循环中再次加入导致无限循环）
        cur_queue = waiting[ch]
        waiting[ch] = deque()  # 清空原队列，后面的单词会重新加入其他桶

        # 逐个处理取出的 (word, pos)
        while cur_queue:
            word, pos = cur_queue.popleft()
            pos += 1                     # 已经匹配了一个字符，向后走一步

            if pos == len(word):        # 完全匹配成功
                ans += 1
            else:
                # 把单词放到下一个期待字符的队列里
                next_char = word[pos]
                waiting[next_char].append((word, pos))

    return ans
```

#### 复杂度

- **时间复杂度**：`O(|s| + Σ|words[i]|)`  
  - `|s|` 次遍历主串，每次只做 **常数** 操作（取出一个队列、把元素搬到下一个队列）。  
  - 每个单词的每个字符恰好被访问一次（从一个队列搬到下一个），所以加起来是所有单词长度的总和。  
  与暴力解相比，省掉了 `|words|` 倍的 `|s|` 乘法，速度提升显著。

- **空间复杂度**：`O(Σ|words[i]|)`（额外的等待队列）  
  - 所有 `(word, pos)` 对会一直保存在 26 个队列里，总数等于所有单词字符的总和。  
  - 这相当于把输入本身的字符拷贝一遍，属于合理的线性空间。

---

## 心得

- **核心技巧**：**“把所有子序列的匹配过程合并到一次遍历中”**，即 **等待队列（bucket）/多路同步**。  
- **适用场景**：  
  1. **多字符串匹配**（如 LeetCode 792 `Number of Matching Subsequences`）。  
  2. **一次扫描解决多个查询**（如“在字符串中查询多个模式是否出现”）。  
  3. **类似的“多指针同步”问题**（如 LeetCode 1032 `Stream of Characters` 的 Trie 版实现）。  
- **一句话总结**：把每个单词挂在它**当前需要的字符**上，随主串走，一次遍历全搞定。

---

## 反思

- **第一反应**：直接对每个单词做子序列检查，写出双指针代码。  
- **最容易踩的坑**：  
  - **桶的取出方式**：如果在遍历 `s` 时直接在原队列上 `pop`，而在循环内部又往同一个桶里 `append`，会导致无限循环。解决办法是先把当前桶内容全部取出（如 `cur_queue = waiting[ch]; waiting[ch] = []`），再处理。  
  - **单词为空或长度为 1**：要确保把空字符串视为子序列（本题中 `words[i]` 长度 ≥ 1，故不必额外处理）。  
  - **字符映射**：`defaultdict(deque)` 可以省去手动检查键是否存在的代码。  
- **下次遇到同类题**：第一步就思考 **“是否可以把所有查询合并到一次遍历”**，把每个查询的“等待状态”挂在对应的触发点上（字符、数值或位置），再随主序列一步步推进。这样往往能把指数级的复杂度降到线性。