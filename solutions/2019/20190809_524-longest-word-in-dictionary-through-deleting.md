# #524. 字典中通过删除得到的最长单词 / Longest Word in Dictionary through Deleting

> 难度：中等 · 标签：Array、Two Pointers、String、Sorting · [LeetCode 链接](https://leetcode.com/problems/longest-word-in-dictionary-through-deleting/)

---

## 题目（英文原版）

**Description**

Given a string s and a string array dictionary, return the longest string in the dictionary that can be formed by deleting some of the given string characters. If there is more than one possible result, return the longest word with the smallest lexicographical order. If there is no possible result, return the empty string.

**Examples**

**Example 1:**

```
Input: s = "abpcplea", dictionary = ["ale","apple","monkey","plea"]
Output: "apple"
```

**Example 2:**

```
Input: s = "abpcplea", dictionary = ["a","b","c"]
Output: "a"
```

**Constraints**

- 1 <= s.length <= 1000
- 1 <= dictionary.length <= 1000
- 1 <= dictionary[i].length <= 1000
- s and dictionary[i] consist of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串 `s` 和一个字符串数组 `dictionary`，返回 `dictionary` 中能够通过删除 `s` 中若干字符而形成的最长单词。如果存在多个满足条件的单词，返回字典序（lexicographical order）最小的那个。如果不存在符合条件的单词，返回空字符串 `""`。

**示例 1**  
**输入**: `s = "abpcplea"`, `dictionary = ["ale","apple","monkey","plea"]`  
**输出**: `"apple"`

**示例 2**  
**输入**: `s = "abpcplea"`, `dictionary = ["a","b","c"]`  
**输出**: `"a"`

**约束条件**

- `1 <= s.length <= 1000`
- `1 <= dictionary.length <= 1000`
- `1 <= dictionary[i].length <= 1000`
- `s` 和 `dictionary[i]` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：遍历 `dictionary` 中的每一个单词，逐个检查它是否能通过**删除** `s` 中的若干字符得到。  
检查的过程可以把两个字符串当成两条跑道上的指针：

1. 指针 `i` 指向 `s`，指针 `j` 指向当前单词 `word`。  
2. 从左到右扫描 `s`，如果 `s[i] == word[j]`，说明找到了 `word` 中的下一个字符，`j` 前进一格。  
3. 最终如果 `j` 能走到 `word` 的末尾，说明 `word` 是 `s` 的子序列（即可以通过删除得到）。

如果 `word` 能匹配，就把它和当前的“最佳答案”比较：

- 长度更长 → 替换答案。  
- 长度相同但字典序更小 → 也替换答案。

**为什么正确**  
子序列的定义恰好是“可以在不改变相对顺序的前提下，通过删除若干字符得到”。上述双指针扫描正是逐字符验证这一点，所以只要遍历完所有单词，就一定能找出所有可行的答案，进而选出满足题目要求的最优解。

**复杂度分析（大白话）**  
- 对每个单词 `word`，我们最多要遍历一次 `s`（最坏情况 `s` 全部遍历完才决定是否匹配），时间是 `O(|s|)`。  
- `dictionary` 中有 `n` 个单词，所以总时间是 `O(n * |s|)`。  
- 这里的 `|s|` 和 `|word|` 最多是 1000，`n` 也最多 1000，最坏会是 10⁶ 次比较，仍在可接受范围。  

空间上我们只用了几个指针和一个保存答案的变量，**不依赖额外的数组或哈希表**，所以是 `O(1)`（常数级）空间。

#### 代码（Python）

```python
def longestWord(s: str, dictionary: list[str]) -> str:
    # 用来保存当前最好的答案
    best = ""

    # 遍历字典里的每个单词
    for word in dictionary:
        # 双指针：i遍历s，j遍历word
        i = j = 0
        while i < len(s) and j < len(word):
            if s[i] == word[j]:          # 找到匹配字符，word指针前进
                j += 1
            i += 1                         # s指针总是前进

        # 循环结束后，如果j走完了word，说明word是子序列
        if j == len(word):
            # 先比较长度，长度相同再比较字典序
            if len(word) > len(best) or (len(word) == len(best) and word < best):
                best = word

    return best
```

#### 复杂度

- **时间复杂度**：`O(n * |s|)`  
  - `n` 是字典的大小，`|s|` 是字符串 `s` 的长度。  
  - 大白话：如果 `s` 长 1000，字典有 1000 条，每条都要检查一次，最多做 1,000,000 次字符比较。

- **空间复杂度**：`O(1)`  
  - 只用了常数个额外变量（指针、答案字符串），不随输入规模增长。

---

### 2. 最优解

#### 思路  

从暴力解来看，**瓶颈在于每次检查子序列都要遍历完整个 `s`**。如果 `s` 很长，而字典里有很多短单词，这会产生很多不必要的重复遍历。

可以把这一步“检查子序列”改成**预处理**，一次性把 `s` 中每个字符出现的位置记录下来，这样后续检查任意单词时就能 **跳跃式** 前进，而不必逐字符扫描 `s`。实现思路如下：

1. **构建位置表**  
   - 创建一个长度为 26（英文字母个数）的列表 `pos`，每个元素是一个 `list`，存放该字母在 `s` 中出现的所有下标，且下标从小到大排列。  
   - 这一步只遍历一次 `s`，时间 `O(|s|)`。

2. **利用二分查找判断子序列**  
   - 对于待检查的单词 `word`，我们从左到右依次找每个字符在 `s` 中出现的 **下一个** 位置，必须严格大于前一个字符所在的位置。  
   - 由于 `pos[char]` 已经是有序的下标列表，我们可以在其中使用 **二分查找**（Python 的 `bisect` 模块）快速定位“大于等于 target”的最左边位置，时间 `O(log k)`（`k` 为该字符出现次数）。  
   - 如果在任意一步找不到合适的位置，则 `word` 不是子序列。

3. **排序字典**（可选但更直观）  
   - 为了直接得到“最长且字典序最小”的答案，可以先把 `dictionary` 按**长度降序、字典序升序**排序。遍历时第一个符合子序列条件的单词即是答案，后面就不必继续检查。

**为什么正确**  
- 位置表保证了我们只在 `s` 中出现的字符集合里查找，二分查找确保每一步找到的是**最靠左**且满足顺序的下标，这正是子序列的定义。  
- 排序后，先检查最长的单词，若出现同长度的情况，字典序更小的会排在前面，符合题目要求。

**复杂度分析（大白话）**  
- 构建位置表：只遍历一次 `s`，`O(|s|)`，相当于 1000 次操作。  
- 对每个单词 `word`：  
  - 长度为 `m`，每个字符一次二分查找，时间 `O(m·log |s|)`（因为每个列表长度最多是 `|s|`）。  
- 整体时间：`O(|s| + Σ m_i·log |s|)`，其中 `m_i` 是第 `i` 个单词的长度。  
  - 最坏情况下 `Σ m_i` ≤ `n·|s|`（每个单词都可能长到 `|s|`），所以仍然在 `O(n·|s|·log |s|)`，比直接遍历 `s` 的暴力解快一个 `log` 级别。  
- 空间：额外的 26 个列表共存储 `|s|` 个下标，`O(|s|)`。

#### 代码（Python）

```python
from bisect import bisect_right
from collections import defaultdict

def longestWord(s: str, dictionary: list[str]) -> str:
    # 1️⃣ 预处理：记录 s 中每个字母出现的位置
    pos = defaultdict(list)          # key:字符，value:该字符在 s 中的下标列表（升序）
    for idx, ch in enumerate(s):
        pos[ch].append(idx)

    # 2️⃣ 按「长度降序、字典序升序」排序，保证先检查最长且字典序最小的候选
    dictionary.sort(key=lambda w: (-len(w), w))

    # 3️⃣ 检查每个单词是否为子序列
    for word in dictionary:
        cur_idx = -1                 # 当前匹配到 s 中的下标，初始为 -1（表示在最左侧之前）
        found = True                 # 标记是否成功匹配整个 word

        for ch in word:
            if ch not in pos:        # s 中根本没有这个字符
                found = False
                break

            # 在 pos[ch] 中找第一个 > cur_idx 的位置（二分查找）
            i = bisect_right(pos[ch], cur_idx)
            if i == len(pos[ch]):    # 已经没有更大的下标了，匹配失败
                found = False
                break

            cur_idx = pos[ch][i]     # 更新为匹配到的下标，继续匹配下一个字符

        if found:                    # 第一个成功的就是答案
            return word

    # 没有任何单词匹配
    return ""
```

#### 复杂度

- **时间复杂度**：`O(|s| + Σ m_i·log |s|)`  
  - `|s|` 用于一次性遍历建立位置表。  
  - 对每个字典单词 `word`（长度 `m_i`），二分查找每个字符的时间是 `log |s|`，所以总共是 `m_i·log |s|`。  
  - 与暴力解相比，多了一个对数因子 `log |s|`（大约 10），在大规模数据时更快。

- **空间复杂度**：`O(|s|)`  
  - 位置表保存了 `s` 中每个字符的下标，总数正好等于 `|s|`。  
  - 额外的排序使用的空间也是 `O(n)`（字典本身），不算在额外空间里。

---

## 心得

- **核心技巧**：把“在字符串中找子序列”转化为“在已排序的下标列表中二分查找”。这是一种**预处理 + 二分**的思路，能够把线性扫描压缩为对数时间。
- **适用场景**  
  1. 判断大量查询词是否为同一长字符串的子序列（如 LeetCode 920 `Number of Music Playlists` 的子序列判断变体）。  
  2. 多次查询“给定模式是否是文本的子序列”，如自动补全系统中快速匹配。  
  3. “最短子序列覆盖”类问题，需要快速定位字符位置。
- **一句话总结**：**把字符串的每个字符位置预先记录，用二分查找跳过不必要的遍历**，就是解这类子序列匹配题的钥匙。

---

## 反思

- **第一反应**：直接遍历 `dictionary`、对每个单词用双指针检查子序列——最直观但不够高效。
- **最容易踩的坑**  
  - 忽视 **字典序** 的比较，导致在长度相同的情况下返回错误答案。  
  - 边界条件：当 `s` 中根本没有某个字符时，需要立即判定失败，防止 `bisect` 越界。  
  - 记得把 `cur_idx` 初始化为 `-1`，否则第一字符的二分查找会错误地从下标 `0` 开始。
- **下次思路**：面对“子序列+多查询”这类题目，第一步就想到 **预处理字符位置**，再配合 **二分查找** 或 **指针跳跃**，可以把每次检查的时间从 `O(|s|)` 降到 `O(log |s|)`。这样既能保证正确，又能在规模稍大的情况下保持效率。