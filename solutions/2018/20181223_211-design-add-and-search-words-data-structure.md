# #211. 设计可添加和搜索单词的数据结构 / Design Add and Search Words Data Structure

> 难度：中等 · 标签：String、Depth-First Search、Design、Trie · [LeetCode 链接](https://leetcode.com/problems/design-add-and-search-words-data-structure/)

---

## 题目（英文原版）

**Description**

Design a data structure that supports adding new words and finding if a string matches any previously added string.
Implement the WordDictionary class:
Example:

**Examples**

**Example 1:**

```
Input
["WordDictionary","addWord","addWord","addWord","search","search","search","search"]
[[],["bad"],["dad"],["mad"],["pad"],["bad"],[".ad"],["b.."]]
Output
[null,null,null,null,false,true,true,true]

Explanation
WordDictionary wordDictionary = new WordDictionary();
wordDictionary.addWord("bad");
wordDictionary.addWord("dad");
wordDictionary.addWord("mad");
wordDictionary.search("pad"); // return False
wordDictionary.search("bad"); // return True
wordDictionary.search(".ad"); // return True
wordDictionary.search("b.."); // return True
```

**Constraints**

- 1 <= word.length <= 25
- word in addWord consists of lowercase English letters.
- word in search consist of '.' or lowercase English letters.
- There will be at most 2 dots in word for search queries.
- At most 104 calls will be made to addWord and search.

---

## 题目（中文翻译）

设计一种数据结构，支持添加新单词并判断给定字符串是否与任意已添加的单词匹配。

实现 `WordDictionary` 类：

```cpp
class WordDictionary {
public:
    WordDictionary();                 // 初始化对象
    void addWord(string word);        // 添加单词
    bool search(string word);         // 搜索单词，支持 '.' 通配符
};
```

**示例**  

```text
输入
["WordDictionary","addWord","addWord","addWord","search","search","search","search"]
[[],["bad"],["dad"],["mad"],["pad"],["bad"],[".ad"],["b.."]]
输出
[null,null,null,null,false,true,true,true]

解释
WordDictionary wordDictionary = new WordDictionary();
wordDictionary.addWord("bad");      // 添加单词 "bad"
wordDictionary.addWord("dad");      // 添加单词 "dad"
wordDictionary.addWord("mad");      // 添加单词 "mad"
wordDictionary.search("pad");       // 返回 false
wordDictionary.search("bad");       // 返回 true
wordDictionary.search(".ad");       // 返回 true，'.' 可以匹配任意单个字符
wordDictionary.search("b..");       // 返回 true，两个 '.' 各匹配一个字符
```

**约束条件**

- `1 <= word.length <= 25`
- `addWord` 中的 `word` 仅由小写英文字母组成。
- `search` 中的 `word` 只包含 `'.'` 或小写英文字母。
- 每个 `search` 查询的 `word` 中至多出现 2 个 `'.'`。
- 最多会有 `10^4` 次 `addWord` 与 `search` 调用。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有加入的单词都保存到一个 **列表**（list）里。  
- **添加**：把新单词 `word` 直接 `append` 到列表中，类似往纸条本里写下新词。
- **搜索**：给定一个查询字符串 `pattern`（可能包含 `.`），我们逐个取出列表里的单词，检查它们是否和 `pattern` 匹配。匹配过程可以把 `.` 当成“任意字符”，其它字母必须相同。

> **类比**：列表就像一本词典的“目录”，要找是否有符合条件的词，只能逐页翻（遍历），没有索引（哈希表）可以直接定位。

这种做法一定能得到正确答案，因为我们检查了所有已经加入的单词，只要有一个匹配就返回 `True`，否则返回 `False`。

#### 代码（Python）

```python
class WordDictionary:
    def __init__(self):
        # 用一个列表保存所有加入的单词
        self.words = []          # [] 相当于空的词典目录

    def addWord(self, word: str) -> None:
        # 直接把单词放进列表
        self.words.append(word)  # 添加新词

    def search(self, pattern: str) -> bool:
        # 逐个检查列表中的单词
        for w in self.words:
            if self._match(w, pattern):
                return True      # 找到匹配的就可以返回 True
        return False             # 没有任何匹配

    def _match(self, word: str, pattern: str) -> bool:
        """
        判断 word 是否匹配 pattern
        pattern 中的 '.' 可以匹配任意单个字符
        """
        if len(word) != len(pattern):
            return False        # 长度不等肯定不匹配

        for wc, pc in zip(word, pattern):
            if pc != '.' and wc != pc:
                return False    # 出现不相等且不是 '.' 的情况
        return True             # 全部字符都匹配
```

#### 复杂度

- **时间复杂度**：`O(N·L)`  
  - `N` 为已加入的单词数，`L` 为单词的平均长度。  
  - “O(N·L)” 的含义是：最坏情况下我们要遍历 `N` 个单词，每个单词都要比较 `L` 次字符。
- **空间复杂度**：`O(N·L)`  
  - 所有单词都原样保存在列表里，需要的空间正比于单词总字符数。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次搜索都要遍历所有单词**。如果单词很多，这会非常慢。我们需要一种**按字符逐层定位**的结构，让搜索只在可能匹配的路径上进行。

**Trie（字典树）** 正好满足这个需求。  
- **Trie 的结构**：每个节点代表一个字符，节点的子节点集合相当于“这个字符后面可能出现哪些字符”。根节点不对应任何字符，只是入口。  
- **添加单词**：从根节点开始，依次创建或复用子节点，最后在最后一个字符的节点上标记 `is_end = True` 表示一条完整单词结束。  
- **搜索**：  
  - 当当前字符是普通字母时，只能沿对应的子节点继续向下。  
  - 当字符是 `.`（通配符）时，需要**尝试所有子节点**（即“所有可能的字符”），只要有一条路径最终能匹配成功，就返回 `True`。这一步可以用 **深度优先搜索（DFS）** 实现。

因为题目说明 **搜索词中最多只有 2 个 `.`**，所以即使在最坏情况下我们也只会分叉最多两次，整体仍然很快。

> **类比**：Trie 像一本按字母顺序排列的“树形词典”。查找时可以像在目录树里一步步往下走，只有在遇到 `.` 时才需要“打开所有子目录”尝试。

#### 代码（Python）

```python
class TrieNode:
    """Trie 的节点结构"""
    def __init__(self):
        self.children = {}      # 用字典保存子节点，key 是字符，value 是 TrieNode
        self.is_end = False     # 标记是否是一条完整单词的结束

class WordDictionary:
    def __init__(self):
        self.root = TrieNode()  # 创建根节点

    def addWord(self, word: str) -> None:
        """把单词插入 Trie"""
        node = self.root
        for ch in word:
            # 如果当前字符对应的子节点不存在，就创建一个
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]          # 移动到子节点继续插入
        node.is_end = True                    # 最后一个字符所在节点标记为单词结束

    def search(self, pattern: str) -> bool:
        """在 Trie 中搜索匹配 pattern 的单词，支持 '.' 通配符"""
        return self._dfs(self.root, pattern, 0)

    def _dfs(self, node: TrieNode, pattern: str, idx: int) -> bool:
        """
        深度优先搜索
        node  : 当前所在的 Trie 节点
        pattern: 查询的模式字符串
        idx   : 正在匹配的字符下标
        """
        if idx == len(pattern):
            # 所有字符都匹配完，只有当恰好落在一个完整单词的结尾才算成功
            return node.is_end

        ch = pattern[idx]
        if ch == '.':
            # 通配符，需要尝试所有子节点
            for child in node.children.values():
                if self._dfs(child, pattern, idx + 1):
                    return True          # 任意一条路径成功即可返回 True
            return False                 # 所有子路径都不匹配
        else:
            # 普通字符，只能沿对应的子节点前进
            if ch not in node.children:
                return False            # 没有对应的子节点，匹配失败
            return self._dfs(node.children[ch], pattern, idx + 1)
```

#### 复杂度

- **时间复杂度**：  
  - `addWord`：`O(L)`，只需遍历单词的每个字符一次。  
  - `search`：最坏情况是遇到 `.` 时需要遍历所有子节点。因为题目限制搜索词至多有 2 个 `.`，所以搜索的时间大约是 `O(26^k · L)`（`k ≤ 2`），实际运行中几乎是 `O(L)`。  
  - 与暴力解相比，**不再随已加入单词的数量 `N` 增长**，只与单词长度相关。

- **空间复杂度**：`O(N·L)`  
  - 存储所有单词需要的节点数同样是所有字符的总和。额外的递归栈深度最多 `L`，可以视为常数级别的额外空间。

---

## 心得

- **核心技巧**：使用 Trie（字典树）配合深度优先搜索处理通配符 `.`。  
- **适用的题型**：  
  1. **实现前缀树**（LeetCode 208）  
  2. **单词搜索 II**（LeetCode 212），需要在二维网格中匹配单词集合  
  3. **最长单词串**（LeetCode 720），需要判断前缀是否都在词典中  
- **一句话总结**：**把所有单词组织成树形结构，只在需要“猜”字符时分支搜索**，即可高效完成带通配符的匹配。

---

## 反思

- **第一反应**：直接用列表保存单词，遍历检查——这就是暴力解。  
- **最容易踩的坑**：  
  - `search` 时忘记检查 **单词结束标记**，导致 `"a"` 能匹配 `"a."`（长度不一致）。  
  - `.` 的递归实现写成只检查第一个子节点，导致漏掉其他可能的匹配路径。  
  - 没有考虑空字符串或单字符单词的边界情况。  
- **下次遇到同类题**：第一步想到“是否可以把字符之间的关系用树/图结构表达”，若出现通配符或前缀查询，**Trie + DFS** 往往是首选思路。