# #953. **验证外星文字典** / Verifying an Alien Dictionary

> 难度：简单 · 标签：Array、Hash Table、String · [LeetCode 链接](https://leetcode.com/problems/verifying-an-alien-dictionary/)

---

## 题目（英文原版）

**Description**

In an alien language, surprisingly, they also use English lowercase letters, but possibly in a different order. The order of the alphabet is some permutation of lowercase letters.
Given a sequence of words written in the alien language, and the order of the alphabet, return true if and only if the given words are sorted lexicographically in this alien language.

**Examples**

**Example 1:**

```
Input: words = ["hello","leetcode"], order = "hlabcdefgijkmnopqrstuvwxyz"
Output: true
Explanation: As 'h' comes before 'l' in this language, then the sequence is sorted.
```

**Example 2:**

```
Input: words = ["word","world","row"], order = "worldabcefghijkmnpqstuvxyz"
Output: false
Explanation: As 'd' comes after 'l' in this language, then words[0] > words[1], hence the sequence is unsorted.
```

**Example 3:**

```
Input: words = ["apple","app"], order = "abcdefghijklmnopqrstuvwxyz"
Output: false
Explanation: The first three characters "app" match, and the second string is shorter (in size.) According to lexicographical rules "apple" > "app", because 'l' > '∅', where '∅' is defined as the blank character which is less than any other character (More info).
```

**Constraints**

- 1 <= words.length <= 100
- 1 <= words[i].length <= 20
- order.length == 26
- All characters in words[i] and order are English lowercase letters.

---

## 题目（中文翻译）

在一种外星语言中，出人意料地仍然使用英文小写字母，只是字母的顺序可能与我们不同。字母表的顺序是小写字母的某种排列。  
给定一系列用该外星语言书写的单词 `words`，以及字母表的顺序 `order`，如果且仅如果这些单词在该外星语言中是按字典序（lexicographically）排序的，则返回 `true`。

**示例 1**  
**输入**: `words = ["hello","leetcode"]`, `order = "hlabcdefgijkmnopqrstuvwxyz"`  
**输出**: `true`  
**解释**: 在该语言中字符 `'h'` 位于 `'l'` 前面，所以序列是有序的。

**示例 2**  
**输入**: `words = ["word","world","row"]`, `order = "worldabcefghijkmnpqstuvxyz"`  
**输出**: `false`  
**解释**: 在该语言中字符 `'d'` 位于 `'l'` 后面，导致 `words[0] > words[1]`，序列无序。

**示例 3**  
**输入**: `words = ["apple","app"]`, `order = "abcdefghijklmnopqrstuvwxyz"`  
**输出**: `false`  
**解释**: 前三个字符 `"app"` 相同，而第二个字符串更短（长度更小）。根据字典序规则，`"apple" > "app"`，因为 `'l'` > `'∅'`，其中 `'∅'` 表示空字符，空字符小于任何其他字符（更多信息请参考题目说明）。

**约束条件**  

- `1 <= words.length <= 100`  
- `1 <= words[i].length <= 20`  
- `order.length == 26`  
- `words[i]` 和 `order` 中的所有字符均为英文小写字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**逐对比较**相邻的两个单词，看它们在外星字典里的顺序是否符合要求。  
具体做法：

1. 取出 `order` 这条“外星字母表”。  
2. 当我们要比较两个字符 `c1`、`c2` 时，去 `order` 里找它们出现的下标（下标越小，字母越靠前），这就像在一本**字典**里查单词的页码：  
   * `order.find(c)` → 返回 `c` 在字母表中的位置。  
3. 按字符从左到右逐一比较：  
   * 第一个不同的字符决定两个单词的大小关系。  
   * 如果所有对应字符都相同，而其中一个单词更短，则短的那个更小（因为“空字符”比任何真实字符都小）。  

只要有一对相邻单词出现逆序，就可以直接返回 `False`；否则遍历完全部单词返回 `True`。

> **为什么正确？**  
> 字典序的定义正好是：**从左到右找第一个不同的字符**，比较它们在字母表中的先后顺序；若所有字符都相同，则长度短的更小。我们完全按照这个规则去逐对检查，自然能够判断整体是否已经排好序。

#### 代码（Python）

```python
def isAlienSorted(words, order):
    # 逐对检查相邻的两个单词
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        # 用两个指针遍历两个单词的字符
        j = 0
        while j < len(w1) and j < len(w2):
            c1, c2 = w1[j], w2[j]
            # 在 order 中线性查找字符的下标（相当于查字典的页码）
            idx1 = order.find(c1)   # O(26) = 常数时间
            idx2 = order.find(c2)
            if idx1 < idx2:          # w1 更小，顺序正确，结束本轮比较
                break
            if idx1 > idx2:          # w1 更大，出现逆序
                return False
            # 若相同继续比较下一个字符
            j += 1
        else:
            # 循环正常结束，说明前缀相同，检查长度
            if len(w1) > len(w2):   # 短的应该排在前面
                return False
    return True
```

> **关键行注释**  
> - `order.find(c)`：在外星字母表里线性查找字符位置，相当于在字典里找页码。  
> - `while j < len(w1) and j < len(w2)`: 同时遍历两个单词，避免越界。  
> - `else:` 块在 `while` 正常结束（没有 `break`）时执行，用来处理“前缀相同但长度不同”的情况。

#### 复杂度

- **时间复杂度**：`O(N * L * 26)`，其中  
  * `N = len(words)`（单词数），  
  * `L` 为单词的平均长度。  
  这里的 `26` 来自每次查找字符在 `order` 中的线性扫描。可以把它看成常数，所以整体仍是 **线性**，但常数比较大——就像在一本 **100 页的字典**里每次都要从头翻到对应页码。

- **空间复杂度**：`O(1)`，只使用了若干指针和临时变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于每次比较字符时都要在 `order` 中线性查找下标**。  
如果我们提前把每个字符对应的排名记下来，就能做到 **O(1) 时间取值**，进而把整体时间降到 `O(N * L)`，且只需要一次额外的 O(26) 空间。

优化步骤：

1. **预处理**：遍历一次 `order`，建立哈希表 `rank`（字典），键是字符，值是它在外星字母表中的位置。  
   * 类比：把 **字典**的“页码”一次性记在小本子上，之后查找就像直接翻到对应页码，不需要再翻整本书。  
2. **比较两个单词**：同样逐字符比较，但这次通过 `rank[c]` 直接得到字符的排名。  
3. **长度判断**：若前缀相同，仍然需要比较长度（短的排前）。

这样，**每个字符只被访问一次**，没有额外的线性查找，时间最优。

#### 代码（Python）

```python
def isAlienSorted(words, order):
    # 1. 预处理：构造字符 → 排名 的映射表（哈希表）
    rank = {ch: i for i, ch in enumerate(order)}   # O(26) 时间、O(26) 空间

    # 2. 定义一个比较函数，返回 True 当 w1 <= w2（符合外星字典序）
    def in_order(w1, w2):
        i = 0
        # 同时遍历两个单词的字符
        while i < len(w1) and i < len(w2):
            c1, c2 = w1[i], w2[i]
            if rank[c1] < rank[c2]:      # w1 更小
                return True
            if rank[c1] > rank[c2]:      # w1 更大，顺序错误
                return False
            i += 1                       # 相同字符继续比较下一个
        # 前缀相同，长度短的更小
        return len(w1) <= len(w2)

    # 3. 逐对检查所有相邻单词
    for i in range(len(words) - 1):
        if not in_order(words[i], words[i + 1]):
            return False
    return True
```

> **关键行注释**  
> - `rank = {ch: i for i, ch in enumerate(order)}`：一次遍历 `order`，把每个字母的“排名”存进字典，相当于把字典的页码写在小本子上。  
> - `rank[c1] < rank[c2]`：直接 O(1) 取值，避免了线性搜索。  
> - `return len(w1) <= len(w2)`：处理“前缀相同但长度不同”的特殊情况。

#### 复杂度

- **时间复杂度**：`O(N * L)`。  
  * 预处理 O(26) 可视为常数。  
  * 主循环每个字符只访问一次，等价于把所有单词的字符总数遍历一遍。  
  与暴力解相比，去掉了每次字符查找的 26 次线性扫描，真正达到了 **线性** 级别。

- **空间复杂度**：`O(26)`，即哈希表 `rank` 占用的空间。  
  只需记录 26 个字母的排名，和输入规模无关，几乎可以忽略不计。

---

## 心得

- **核心技巧**：利用哈希表把字符映射到自定义顺序，实现 **O(1) 取值**，从而把字典序比较的时间降到线性。  
- **适用场景**：  
  1. 任意需要**自定义字符顺序**的比较题（如 “字母异位词分组” 中的自定义排序）。  
  2. “**基于字符权值的排序**”题目，例如 “按字母顺序重新排列单词”。  
  3. “**字典序最小/最大**”类问题（如 “最小覆盖子串” 中的字符优先级比较）。  
- **一句话总结**：先把外星字母表“记在本子上”，后面比较单词时直接查表即可。

---

## 反思

- **第一反应**：看到“外星字母表”，自然想到把它转成一个查表（哈希表）来快速比较字符。  
- **最容易踩的坑**：  
  1. **前缀情况**：`"apple"` 与 `"app"`，前面相同但长度不同，需要把短的排在前面，否则会误判。  
  2. **字符不存在**：题目保证所有字符都在 `order` 中，但若自行改造测试数据，仍需防止 `KeyError`。  
  3. **空字符概念**：在字典序里，空字符（长度结束）被视为比任何真实字符都小，需要显式处理。  
- **下次思路**：遇到“自定义顺序”或“非标准比较”时，第一步就**建立映射表**（哈希表或数组），再用该映射完成后续比较。这样可以避免重复的线性查找，直接进入最优解的思考。