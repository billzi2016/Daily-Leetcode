# #890. 查找和替换模式 / Find and Replace Pattern

> 难度：中等 · 标签：Array、Hash Table、String · [LeetCode 链接](https://leetcode.com/problems/find-and-replace-pattern/)

---

## 题目（英文原版）

**Description**

Given a list of strings words and a string pattern, return a list of words[i] that match pattern. You may return the answer in any order.
A word matches the pattern if there exists a permutation of letters p so that after replacing every letter x in the pattern with p(x), we get the desired word.
Recall that a permutation of letters is a bijection from letters to letters: every letter maps to another letter, and no two letters map to the same letter.

**Examples**

**Example 1:**

```
Input: words = ["abc","deq","mee","aqq","dkd","ccc"], pattern = "abb"
Output: ["mee","aqq"]
Explanation: "mee" matches the pattern because there is a permutation {a -> m, b -> e, ...}. 
"ccc" does not match the pattern because {a -> c, b -> c, ...} is not a permutation, since a and b map to the same letter.
```

**Example 2:**

```
Input: words = ["a","b","c"], pattern = "a"
Output: ["a","b","c"]
```

**Constraints**

- 1 <= pattern.length <= 20
- 1 <= words.length <= 50
- words[i].length == pattern.length
- pattern and words[i] are lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串数组 `words` 和一个字符串 `pattern`，返回所有与 `pattern` 匹配的 `words[i]`，返回结果的顺序任意即可。  
如果存在一个字母的置换（permutation）`p`，使得将 `pattern` 中的每个字母 `x` 替换为 `p(x)` 后得到某个单词，则该单词匹配 `pattern`。  
回想一下，字母的置换（permutation）是一个从字母到字母的双射（bijection）：每个字母映射到另一个字母，且不存在两个不同的字母映射到同一个字母。

**Example 1:**  
**Example 2:**  
**Constraints:**

示例：

**示例 1:**  
Input: `words = ["abc","deq","mee","aqq","dkd","ccc"], pattern = "abb"`  
Output: `["mee","aqq"]`  
Explanation: `"mee"` 匹配该模式，因为存在置换 `{a -> m, b -> e, ...}`。  
`"ccc"` 不匹配该模式，因为置换 `{a -> c, b -> c, ...}` 不是一个合法的置换，`a` 和 `b` 被映射到了同一个字母。

**示例 2:**  
Input: `words = ["a","b","c"], pattern = "a"`  
Output: `["a","b","c"]`

约束条件：

- `1 <= pattern.length <= 20`
- `1 <= words.length <= 50`
- `words[i].length == pattern.length`
- `pattern` 和 `words[i]` 仅包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每个单词和 pattern 一一对应地去检查**，看能否把 pattern 的每个字母“换成”单词里的字母，使得整个映射是一一对应的（即没有两个 pattern 的字母映射到同一个单词的字母，也没有一个 pattern 的字母映射到两个不同的字母）。

这相当于在做“查字典”。  
- **哈希表（dict）** 就像一本词典，`key` 是 pattern 中的字母，`value` 是它映射到的单词字母。  
- 为了保证**双向唯一**，我们还需要另一个词典把单词字母映射回 pattern 字母（就像把词典翻面，检查每个词条的页码是否唯一）。

如果在遍历过程中出现以下任意一种情况，就说明当前单词 **不匹配** pattern：
1. 某个 pattern 字母已经映射过，但这次想映射到一个 **不同** 的单词字母；
2. 某个单词字母已经被别的 pattern 字母占用了（映射冲突）。

只要所有位置都检查通过，就说明这对 (pattern, word) 满足**双射**（bijection）的要求，保留下来。

#### 代码（Python）

```python
from typing import List

def matches(word: str, pattern: str) -> bool:
    """判断单个 word 是否能和 pattern 建立一一对应的映射"""
    p2w = {}          # pattern 字母 → word 字母
    w2p = {}          # word 字母 → pattern 字母（反向映射）

    for pc, wc in zip(pattern, word):
        # 正向映射冲突
        if pc in p2w and p2w[pc] != wc:
            return False
        # 反向映射冲突
        if wc in w2p and w2p[wc] != pc:
            return False
        # 建立映射（如果已经存在且相同，下面两行会覆盖但不影响结果）
        p2w[pc] = wc
        w2p[wc] = pc
    return True


def findAndReplacePattern(words: List[str], pattern: str) -> List[str]:
    """暴力遍历每个单词，挑选出匹配的"""
    ans = []
    for w in words:
        if matches(w, pattern):
            ans.append(w)
    return ans
```

#### 复杂度

- **时间复杂度**：`O(N * L)`  
  - `N` 是单词数量，`L` 是每个单词（以及 pattern）的长度。  
  - 对每个单词我们要逐字符比较一次，所需时间随 `N` 和 `L` 成正比。  
  - 用大白话说，就是“如果有 50 个单词，每个 20 个字母，最多检查 1000 次字符”。

- **空间复杂度**：`O(Σ)`（Σ 为字母表大小，这里最多 26）  
  - 只需要两张哈希表保存映射，最多存 26 对键值对，和输入规模无关。  

---

### 2. 最优解

#### 思路  

虽然上面的暴力解已经是 **线性**（相对于输入规模）的，但我们仍可以把「检查映射」这一步抽象成 **“把模式压缩成一种唯一的编号序列”**，然后直接比较压缩后的结果是否相同。

**核心观察**  
- 对于任意字符串（无论是 pattern 还是 word），只要把它每个字符第一次出现的位置记下来，后面再次出现时就写上第一次出现的编号，就能得到一个**标准化的编码**。  
- 例如 `"abb"` → `[0,1,1]`（`a` 第一次出现记 0，`b` 第一次出现记 1，第二个 `b` 复用 1）。  
- 两个字符串如果能够通过字母置换相互对应，它们的标准化编码必然相同；反之亦然。

**为什么这样能省去哈希表的双向检查？**  
- 编码过程天然保证了**一一对应**：同一个字符总是得到同一个编号，不同字符得到不同编号。  
- 只要两个字符串的编码序列相等，就已经说明存在一种 bijection 将一个映射到另一个。

**实现步骤**  

1. 编写一个 `encode(s)` 函数，把字符串 `s` 转换为它的编号序列（可以用列表或字符串表示）。  
2. 先对 `pattern` 计算一次编码，记为 `pat_code`。  
3. 对 `words` 中的每个单词 `w`，计算 `encode(w)`，如果等于 `pat_code`，说明匹配，加入答案。  

**类比**：把每个单词和 pattern 看成 **指纹**，指纹相同才是同类。指纹的生成过程就是 “第一次出现记号”。

#### 代码（Python）

```python
from typing import List

def encode(s: str) -> str:
    """
    将字符串 s 转换为标准化的编号序列，例如：
    "abb" -> "0,1,1"
    "mee" -> "0,1,1"
    使用字典记录每个字符第一次出现时的编号。
    """
    char_to_id = {}
    code = []
    nxt = 0                     # 下一个可用的编号

    for ch in s:
        if ch not in char_to_id:
            char_to_id[ch] = nxt
            nxt += 1
        code.append(str(char_to_id[ch]))
    # 用逗号拼接成唯一的字符串，便于直接比较
    return ','.join(code)


def findAndReplacePattern(words: List[str], pattern: str) -> List[str]:
    pat_code = encode(pattern)          # 只算一次
    ans = []
    for w in words:
        if encode(w) == pat_code:       # 编码相同即匹配
            ans.append(w)
    return ans
```

#### 复杂度

- **时间复杂度**：`O(N * L)`（与暴力解相同的量级）  
  - `encode` 对每个字符只遍历一次，`N` 个单词各自调用一次。  
  - 相比于使用两张哈希表的“冲突检查”，这里的操作更**轻量**（只写入一次映射），常数因子更小。

- **空间复杂度**：`O(Σ)`（同样只需保存 26 以下的映射）  
  - `encode` 中的 `char_to_id` 最多保存 26 条记录，和单词数量无关。  

相较于暴力解，最优解的 **核心优势** 在于代码更简洁、易于理解，也更容易在面试中快速写出。

---

## 心得

- **核心技巧**：把字符串映射关系抽象为“标准化编码”，利用 **哈希表**（字典）一次遍历完成。  
- **适用题型**：  
  1. **同构字符串**（LeetCode 205 – Isomorphic Strings）  
  2. **字母异位词分组**（LeetCode 49 – Group Anagrams）  
  3. **判断回文串是否可通过字符替换得到**（变形题目）  
- **一句话总结**：只要把「模式」和「单词」都压缩成「第一次出现的编号序列」，相等即说明可以通过字母置换相互匹配。

---

## 反思

- **第一反应**：看到“一一对应的置换”，立刻想到使用两张哈希表检查正向和反向映射是否冲突。  
- **最容易踩的坑**：  
  - 忘记检查 **双向唯一性**（只检查 pattern → word 的映射会漏掉 `a -> c, b -> c` 的错误）。  
  - 对长度不一致的单词直接返回错误（本题已保证等长，但实际面试时要自行判断）。  
  - 编码时忘记把不同字符映射到不同编号，导致 `"ab"` 与 `"aa"` 产生相同编码。  
- **下次思路**：遇到“是否存在某种置换使两串相等”时，第一步就考虑把两串 **归一化**（编码）后比较，这往往能把复杂的映射检查化简为 O(L) 的相等判断。