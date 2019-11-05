# #648. 替换单词 / Replace Words

> 难度：中等 · 标签：Array、Hash Table、String、Trie · [LeetCode 链接](https://leetcode.com/problems/replace-words/)

---

## 题目（英文原版）

**Description**

In English, we have a concept called root, which can be followed by some other word to form another longer word - let's call this word derivative. For example, when the root "help" is followed by the word "ful", we can form a derivative "helpful".
Given a dictionary consisting of many roots and a sentence consisting of words separated by spaces, replace all the derivatives in the sentence with the root forming it. If a derivative can be replaced by more than one root, replace it with the root that has the shortest length.
Return the sentence after the replacement.

**Examples**

**Example 1:**

```
Input: dictionary = ["cat","bat","rat"], sentence = "the cattle was rattled by the battery"
Output: "the cat was rat by the bat"
```

**Example 2:**

```
Input: dictionary = ["a","b","c"], sentence = "aadsfasf absbs bbab cadsfafs"
Output: "a a b c"
```

**Constraints**

- 1 <= dictionary.length <= 1000
- 1 <= dictionary[i].length <= 100
- dictionary[i] consists of only lower-case letters.
- 1 <= sentence.length <= 106
- sentence consists of only lower-case letters and spaces.
- The number of words in sentence is in the range [1, 1000]
- The length of each word in sentence is in the range [1, 1000]
- Every two consecutive words in sentence will be separated by exactly one space.
- sentence does not have leading or trailing spaces.

---

## 题目（中文翻译）

在英文中，有一种叫做根（root）的概念，后面可以接其他单词形成更长的单词——我们称这种单词为派生词（derivative）。例如，当根 `"help"` 后接单词 `"ful"` 时，可以组成派生词 `"helpful"`。  
给定一个由多个根组成的字典 `dictionary` 和一个由空格分隔的句子 `sentence`，请将句子中的所有派生词替换为构成它的根。如果一个派生词可以被多个根替换，则使用长度最短的根进行替换。返回替换后的句子。

**示例 1**  
**输入**  
``` 
dictionary = ["cat","bat","rat"], sentence = "the cattle was rattled by the battery"
```  
**输出**  
```
the cat was rat by the bat
```

**示例 2**  
**输入**  
``` 
dictionary = ["a","b","c"], sentence = "aadsfasf absbs bbab cadsfafs"
```  
**输出**  
```
a a b c
```

**约束条件**

- `1 <= dictionary.length <= 1000`
- `1 <= dictionary[i].length <= 100`
- `dictionary[i]` 只包含小写字母。
- `1 <= sentence.length <= 10^6`
- `sentence` 只包含小写字母和空格。
- `sentence` 中的单词数在 `[1, 1000]` 范围内。
- `sentence` 中每个单词的长度在 `[1, 1000]` 范围内。
- 相邻的两个单词之间恰好只有一个空格。
- `sentence` 开头和结尾没有空格。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：  
1. 把 `dictionary`（根词表）存进一个 **哈希表**（Python 的 `set`），相当于把所有根词写进一本字典，查找时只需要看一眼就能知道有没有。  
2. 把句子按空格切成一个个单词。  
3. 对每个单词，从左到右逐字符尝试构造前缀：  
   - 取第 1 个字符组成的前缀，查哈希表；  
   - 再取前 2 个字符组成的前缀，继续查；  
   - …一直到整个单词。  
   - 一旦找到哈希表中存在的前缀，就把这个单词换成该前缀（因为我们是从短到长枚举的，第一个命中的一定是最短的根词），然后停止对该单词的检查。  
4. 把所有处理好的单词用空格重新拼起来，即得到答案。

> **类比**：哈希表就像一本“词汇手册”，我们只需要把想查的词（前缀）翻到对应的页码（哈希键），看手册里有没有记载。  

> **为什么正确**：  
> - 题目要求把单词替换成 **最短** 的根词。我们从短到长枚举前缀，第一次命中必然是最短的。  
> - 若整个单词都没有任何根词的前缀，则保持原样不变，这正好符合题目要求。

#### 代码（Python）

```python
def replaceWords(dictionary, sentence):
    # 把根词放进集合，查找 O(1)
    roots = set(dictionary)

    # 把句子切成单词列表
    words = sentence.split()

    for i, w in enumerate(words):
        # 逐字符构造前缀，长度从 1 到 len(w)
        for l in range(1, len(w) + 1):
            prefix = w[:l]               # 当前前缀
            if prefix in roots:          # 在根词集合里找到了
                words[i] = prefix        # 用根词替换
                break                    # 停止检查该单词
        # 如果没有任何前缀在集合里，保持原单词不变

    # 用空格把单词重新拼成句子
    return ' '.join(words)
```

#### 复杂度

- **时间复杂度**：`O(N * L)`  
  - `N` 是句子里单词的个数（≤1000），`L` 是单词的最大长度（≤1000）。  
  - 对每个单词我们最坏要检查它的每一个前缀，前缀检查是 O(1)（哈希查找），所以整体是 `N * L`。  
  - 用大白话说，就是“如果句子里有 1000 个单词，每个单词最多 1000 个字母，最坏情况下要检查 100 万次”。

- **空间复杂度**：`O(D)`  
  - `D` 为根词表的大小（≤1000），我们用一个 `set` 把它们全部存下来。  
  - 其余空间只用来存切好的单词列表，和输入长度同阶，不计入额外空间。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **“对每个单词逐字符枚举前缀”**。  
如果我们能一次性把所有根词组织起来，让“查找前缀”操作更快，就能把整体时间降下来。  
这里**Trie（前缀树）** 正好能满足需求。

**Trie** 可以把一组字符串压缩成一棵树：

- 每个节点代表一个字符。  
- 从根节点到某个节点的路径恰好对应一个前缀。  
- 当某条路径对应的字符串是完整的根词时，我们在该节点上打上“结束标记”。  

**查找过程**：

1. 把所有根词插入 Trie。插入时，如果某条路径已经存在，就直接走下去；否则创建新节点。  
2. 处理句子中的每个单词时，只需要从首字符开始，沿着 Trie 向下走：  
   - 遇到 **结束标记**，说明已经找到最短根词，立刻返回该根词。  
   - 若走到某个字符在 Trie 中不存在的分支，说明该单词没有任何根词的前缀，直接返回原单词。  
3. 其余步骤和暴力解相同：把替换后的单词重新拼成句子。

> **类比**：Trie 像一本**“按字母顺序排好目录的字典”**。查找一个单词的前缀时，只需要顺着目录一步步往下走，一旦碰到标记为“完整词条”的页面，就找到了最短匹配。

#### 代码（Python）

```python
class TrieNode:
    """Trie 的节点结构"""
    __slots__ = ('children', 'is_word')

    def __init__(self):
        self.children = {}      # key: 字符，value: 子节点
        self.is_word = False    # 是否到这里就构成一个完整的根词


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """把一个根词插入 Trie"""
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_word = True

    def shortest_prefix(self, word: str) -> str:
        """
        在 Trie 中寻找 word 的最短根词前缀。
        若不存在则返回原单词。
        """
        node = self.root
        prefix_chars = []        # 记录走过的字符，用来拼接前缀
        for ch in word:
            if ch not in node.children:      # 没有对应分支，说明没有根词匹配
                return word
            node = node.children[ch]
            prefix_chars.append(ch)
            if node.is_word:                 # 第一次遇到完整根词，就是最短的
                return ''.join(prefix_chars)
        # 整个单词走完仍未遇到根词
        return word


def replaceWords(dictionary, sentence):
    # 1. 建立 Trie 并把所有根词插入
    trie = Trie()
    for root in dictionary:
        trie.insert(root)

    # 2. 逐词查找最短前缀并替换
    result = []
    for w in sentence.split():
        result.append(trie.shortest_prefix(w))

    # 3. 合并成最终句子
    return ' '.join(result)
```

#### 复杂度

- **时间复杂度**：`O(T + S)`  
  - `T` 为所有根词字符总数（≤ 1000 * 100 = 1e5），用于一次性构建 Trie。  
  - `S` 为句子中所有字符的总数（≤ 1e6），因为每个字符最多只会在 Trie 中被访问一次（走到不存在的分支就停）。  
  - 相比暴力解的 `O(N * L)`，这里不再出现 “对每个单词重复遍历前缀” 的平方级开销，整体更快。  
  - 用通俗的话说：**我们只需要把所有根词一次性装进字典，然后把句子里每个字母“顺着路标”走一次**。

- **空间复杂度**：`O(T)`  
  - Trie 的节点数最多等于所有根词字符的总数（每个字符可能对应一个新节点），因此空间与根词字符总数线性相关。  
  - 额外的 `result` 列表占用的空间与句子单词数相同，算作输出空间。

---

## 心得

- **核心技巧**：**Trie（前缀树）** 用于高效的前缀查询。  
- **适用的题型**：  
  1. **单词搜索 II**（在矩阵中找多个单词）。  
  2. **最长单词串**（找出可以由字典中其他单词拼接成的最长单词）。  
  3. **字典序最小的单词替换**（本题的变形）。  
- **一句话总结**：把所有根词压缩进一棵前缀树，遍历句子时“顺着树走”，第一个到达的终止节点就是答案。

---

## 反思

- **第一反应**：看到“根词 + 前缀替换”，自然想到“把根词放进集合，逐字符枚举前缀”。这是一种**暴力思路**，可以直接写出可运行的代码。  
- **最容易踩的坑**：  
  - **忘记返回最短根词**：若直接把所有匹配的根词都列出来，可能会选到更长的根词，需要额外比较长度。  
  - **边界字符**：句子里单词可能恰好等于根词本身，或者根词本身是空字符串（题目保证不为空）。  
  - **空间泄漏**：在 Trie 实现中，如果不使用 `__slots__` 或者不及时释放节点，可能导致额外的内存开销（在 Python 里一般不影响答案）。  
- **下次遇到同类题**：第一步先**思考是否需要大量前缀查询**，如果是，就立即考虑构建 **Trie**；否则，直接用 **哈希表 + 前缀枚举** 也是可行的。