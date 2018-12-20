# #208. 实现 Trie（前缀树） / Implement Trie (Prefix Tree)

> 难度：中等 · 标签：Hash Table、String、Design、Trie · [LeetCode 链接](https://leetcode.com/problems/implement-trie-prefix-tree/)

---

## 题目（英文原版）

**Description**

A trie (pronounced as "try") or prefix tree is a tree data structure used to efficiently store and retrieve keys in a dataset of strings. There are various applications of this data structure, such as autocomplete and spellchecker.
Implement the Trie class:

**Examples**

**Example 1:**

```
Input
["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
[[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]
Output
[null, null, true, false, true, null, true]

Explanation
Trie trie = new Trie();
trie.insert("apple");
trie.search("apple");   // return True
trie.search("app");     // return False
trie.startsWith("app"); // return True
trie.insert("app");
trie.search("app");     // return True
```

**Constraints**

- 1 <= word.length, prefix.length <= 2000
- word and prefix consist only of lowercase English letters.
- At most 3 * 104 calls in total will be made to insert, search, and startsWith.

---

## 题目（中文翻译）

前缀树（Trie）是一种树形数据结构，能够在字符串集合中高效地存储和检索键。该数据结构在自动补全（autocomplete）和拼写检查器（spellchecker）等场景中有广泛应用。

**实现 Trie 类**  

---

**示例 1：**

```text
Input
["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
[[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]
Output
[null, null, true, false, true, null, true]
```

**解释**
```java
Trie trie = new Trie();
trie.insert("apple");          // 插入单词 "apple"
trie.search("apple");          // 返回 true
trie.search("app");            // 返回 false
trie.startsWith("app");        // 返回 true
trie.insert("app");            // 再插入单词 "app"
trie.search("app");            // 返回 true
```

---

**约束条件**

- `1 <= word.length, prefix.length <= 2000`
- `word` 和 `prefix` 仅由小写英文字母组成。
- `insert`、`search`、`startsWith` 的调用总次数不超过 `3 * 10^4`。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把所有插入的单词直接放进一个 **列表**（或集合）里。  

- **插入**：把单词 `word` 直接 `append` 到列表中。  
- **完整搜索** `search(word)`：遍历列表，看看列表里有没有完全等于 `word` 的元素。  
- **前缀搜索** `startsWith(prefix)`：同样遍历列表，只要找到一个单词的开头和 `prefix` 相同即可。  

> 类比：列表就像一本“词典”，我们每次都要从头到尾翻页查找，虽然能找到答案，但效率低。  

这个方法之所以 **正确**，是因为我们把所有出现过的单词全部保存下来，查询时只要把每个单词都比对一遍就一定能判断出是否存在。  

**时间/空间复杂度**（大白话版）  
- `insert`：把单词加到列表的尾巴，**O(1)**，几乎不花时间。  
- `search` / `startsWith`：要把列表里每个单词都检查一遍，最坏情况下要检查 **N**（已插入的单词数）个单词，每个单词的长度记为 **L**，所以是 **O(N·L)**。可以想象成“我们要找的词在第 N 本书的第 L 页”。  
- 空间：所有单词都要存下来，**O(N·L)**，即所有字符的总和。  

#### 代码（Python）  

```python
class Trie:
    def __init__(self):
        # 用一个列表保存所有插入的单词
        self.words = []                     # 相当于一本装满词的“词典”

    def insert(self, word: str) -> None:
        # 直接把单词放进去，时间几乎为常数
        self.words.append(word)             # 把 word 加到词典的最后一页

    def search(self, word: str) -> bool:
        # 线性遍历列表，逐个比较是否完全相同
        for w in self.words:                # 从第一页翻到最后一页
            if w == word:                   # 找到完全相同的单词
                return True
        return False                        # 没有找到

    def startsWith(self, prefix: str) -> bool:
        # 同样遍历列表，只要有一个单词的前缀匹配就行
        for w in self.words:                # 逐页检查
            if w.startswith(prefix):        # 检查是否以 prefix 开头
                return True
        return False                        # 没有任何单词以该前缀开头
```

#### 复杂度  

- **时间复杂度**  
  - `insert`：**O(1)**（常数时间）  
  - `search` / `startsWith`：**O(N·L)**，N 为已插入单词数，L 为单词平均长度。  
- **空间复杂度**  
  - **O(N·L)**，因为要把所有字符都保存下来。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈** 出在每次查询都要遍历全部单词。我们需要一种结构，让“查找”过程只跟**单词的长度**有关，而不受已有单词数量的影响。  

**Trie（前缀树）** 正是为此设计的。它把所有单词的公共前缀合并到同一个分支上，形成一棵多叉树：

- 每个节点对应一个字符（或空根节点），
- 从根到某个节点走过的路径恰好拼成一个前缀，
- 当某个单词结束时，在对应的节点上标记 `is_end = True`。  

这样：

- **插入**：从根节点依次检查每个字符是否已有子节点，若没有就创建。时间只和单词长度 **L** 成正比 → **O(L)**。  
- **完整搜索**：同样沿着字符路径往下走，走完后检查 `is_end` 标记 → **O(L)**。  
- **前缀搜索**：只需要走完前缀的路径，不需要检查 `is_end` → **O(L)**。  

> 类比：Trie 就像一本按照字母顺序折叠的“词典”。找单词时我们只需要沿着每一页的目录一步步往下翻，而不必把整本书都翻遍。  

**实现细节**  
- 每个节点的子节点可以用 **字典**（哈希表）保存，`key` 是字符，`value` 是对应的子节点对象。字典像查字典一样，给定字符可以在 **O(1)** 时间找到下一个节点。  
- 为了节省空间，也可以用长度为 26 的数组（对应 `'a'`~`'z'`），但在 Python 中使用 `dict` 更简洁且易读。  

#### 代码（Python）  

```python
class TrieNode:
    """Trie 的节点结构"""
    def __init__(self):
        # 用字典保存子节点，key 是字符，value 是对应的 TrieNode
        self.children = {}          # 相当于“查字典”，键是字母，值是下一个节点
        self.is_end = False         # 标记是否是一条完整单词的结束

class Trie:
    def __init__(self):
        # 根节点不对应任何字符，只是所有单词的起点
        self.root = TrieNode()      # 树的根，所有路径都从这里出发

    def insert(self, word: str) -> None:
        """把 word 放进 Trie"""
        node = self.root
        for ch in word:              # 逐字符遍历
            if ch not in node.children:
                # 没有该字符对应的子节点，就新建一个
                node.children[ch] = TrieNode()
            node = node.children[ch] # 移动到子节点继续插入
        node.is_end = True           # 最后一个字符所在的节点标记为单词结束

    def search(self, word: str) -> bool:
        """判断完整单词 word 是否在 Trie 中"""
        node = self._find_node(word)
        # 若找不到路径，返回 False；否则要检查该路径对应的节点是否是单词结束
        return node is not None and node.is_end

    def startsWith(self, prefix: str) -> bool:
        """判断是否有单词以 prefix 为前缀"""
        # 只要前缀对应的路径存在，就说明有单词以它开头
        return self._find_node(prefix) is not None

    def _find_node(self, s: str):
        """
        辅助函数：沿着字符串 s 在 Trie 中走到底，
        若途中缺少字符则返回 None（表示路径不存在）。
        """
        node = self.root
        for ch in s:
            if ch not in node.children:
                return None          # 路径中断，说明不存在
            node = node.children[ch]
        return node                 # 返回最后停留的节点
```

#### 复杂度  

- **时间复杂度**  
  - `insert`：**O(L)**，只遍历单词的每个字符一次。  
  - `search` / `startsWith`：**O(L)**，同样只跟单词（或前缀）的长度有关。  
  与暴力解相比，**不再随已插入单词数量 N 增长**，即使插入 30,000 次也依旧快。  

- **空间复杂度**  
  - 最坏情况下，每个字符都会新建一个节点，所有单词的字符总数记为 **S**，则 **O(S)**。  
  - 由于公共前缀会共享节点，实际占用的空间通常会比单纯保存所有字符串要少。  

---

## 心得  

- **核心技巧**：利用 Trie（前缀树）把公共前缀合并，查找仅与字符串长度相关。  
- **适用场景**：  
  1. 自动补全（Autocomplete）  
  2. 单词搜索 II（Word Search II）中的词典匹配  
  3. 拼写检查（Spell Checker）  
- **一句话总结**：**“把相同前缀的字符折叠进同一条枝干，查找路径即是答案。”**

## 反思  

- **第一反应**：直接用列表保存所有单词，遍历查找——最直观但不够高效。  
- **最容易踩的坑**：  
  - `search` 时忘记检查 `is_end`，导致把前缀误判为完整单词。  
  - `startsWith` 只需要判断路径是否存在，不要误用 `is_end`。  
  - 对空字符串的处理（根节点本身就是空前缀）。  
- **下次遇到同类题**：第一步先问自己“**查询是否必须遍历所有已存数据？**”，如果答案是“否”，就考虑使用 **Trie**、**前缀哈希** 或 **二分搜索树** 等结构来把查询成本降到与输入长度同阶。