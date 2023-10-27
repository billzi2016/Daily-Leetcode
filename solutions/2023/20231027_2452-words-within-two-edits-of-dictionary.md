# #2452. **字典中两次编辑以内的单词** / Words Within Two Edits of Dictionary

> 难度：中等 · 标签：Array、String、Trie · [LeetCode 链接](https://leetcode.com/problems/words-within-two-edits-of-dictionary/)

---

## 题目（英文原版）

**Description**

You are given two string arrays, queries and dictionary. All words in each array comprise of lowercase English letters and have the same length.
In one edit you can take a word from queries, and change any letter in it to any other letter. Find all words from queries that, after a maximum of two edits, equal some word from dictionary.
Return a list of all words from queries, that match with some word from dictionary after a maximum of two edits. Return the words in the same order they appear in queries.

**Examples**

**Example 1:**

```
Input: queries = ["word","note","ants","wood"], dictionary = ["wood","joke","moat"]
Output: ["word","note","wood"]
Explanation:
- Changing the 'r' in "word" to 'o' allows it to equal the dictionary word "wood".
- Changing the 'n' to 'j' and the 't' to 'k' in "note" changes it to "joke".
- It would take more than 2 edits for "ants" to equal a dictionary word.
- "wood" can remain unchanged (0 edits) and match the corresponding dictionary word.
Thus, we return ["word","note","wood"].
```

**Example 2:**

```
Input: queries = ["yes"], dictionary = ["not"]
Output: []
Explanation:
Applying any two edits to "yes" cannot make it equal to "not". Thus, we return an empty array.
```

**Constraints**

- 1 <= queries.length, dictionary.length <= 100
- n == queries[i].length == dictionary[j].length
- 1 <= n <= 100
- All queries[i] and dictionary[j] are composed of lowercase English letters.

---

## 题目（中文翻译）

给定两个字符串数组 `queries` 和 `dictionary`。两个数组中的所有单词均只包含小写英文字母，并且长度相同。  
在一次编辑（edit）中，你可以从 `queries` 中取出一个单词，将其中任意一个字母替换为任意其他字母。求出所有在最多 **两次编辑**（最多 two edits）后能够等于 `dictionary` 中某个单词的 `queries` 单词。

返回一个数组，包含所有满足条件的 `queries` 单词，顺序与它们在 `queries` 中出现的顺序保持一致。

---

### 示例 1

```text
Input: queries = ["word","note","ants","wood"], dictionary = ["wood","joke","moat"]
Output: ["word","note","wood"]
Explanation:
- 将 "word" 中的字符 'r' 改为 'o' 后即可得到字典中的单词 "wood"。
- 将 "note" 中的字符 'n' 改为 'j'、't' 改为 'k' 后得到 "joke"。
- 将 "ants" 变为字典中的任意单词至少需要超过 2 次编辑，因此不满足条件。
- "wood" 本身无需修改（0 次编辑），即可匹配字典中的 "wood"。
```

### 示例 2

```text
Input: queries = ["yes"], dictionary = ["not"]
Output: []
Explanation:
对 "yes" 进行任意两次编辑都无法得到字典中的单词 "not"，因此返回空数组。
```

---

### 约束条件

- `1 <= queries.length, dictionary.length <= 100`
- `n == queries[i].length == dictionary[j].length`
- `1 <= n <= 100`
- 所有 `queries[i]` 和 `dictionary[j]` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**把每个查询词 `q` 和字典里的每个单词 `d` 逐个比较**，看它们之间相差多少个字符。如果相差的字符数（即编辑距离）不超过 2，则 `q` 能通过最多两次“改字母”变成 `d`，于是把 `q` 加入答案。

- **用到的数据结构**：  
  - 两个普通的 Python 列表 `queries`、`dictionary`，它们就像两排装好单词的抽屉。  
  - 在比较两个单词时，只需要遍历它们的字符，这里相当于把两个单词的每个字母对应起来，一一检查。  
  - **哈希表**在这个暴力解里其实不需要，用到的只有**计数器**（一个整数）来记录不相同的字符个数。可以把它想成“错误标记灯”，每发现一个不同的字母，就点亮一次灯。

- **为什么正确**：  
  因为题目只要求“最多两次改字母”，这正好等价于“两个单词之间不相同的字符数 ≤ 2”。只要我们把所有可能的配对都检查一遍，必然不会漏掉任何符合条件的查询词。

- **时间/空间复杂度**（大白话解释）  
  - **时间**：我们要遍历 `len(queries)` 次外层循环，内部再遍历 `len(dictionary)` 次，每次比较 `n`（单词长度）个字符。于是总共要做 `queries × dictionary × n` 次字符比较。  
    用 **O(queries·dictionary·n)** 来表示，读作“数量级是 queries 乘以 dictionary 再乘以 n”。如果把它想象成一次跑步比赛，`queries` 是跑步的次数，`dictionary` 是每次跑步要跑的段数，`n` 是每段路的长度，三者相乘就是总的路程。  
  - **空间**：只用了几个计数器和返回的结果列表，和输入规模无关，属于 **O(1)**（常数级）额外空间。

#### 代码（Python）

```python
def within_two_edits_bruteforce(queries, dictionary):
    """
    暴力解：逐对比较，统计不同字符的个数
    """
    ans = []                                 # 用来保存符合条件的查询词
    for q in queries:                        # 遍历每个查询词
        for d in dictionary:                 # 与字典里的每个单词比较
            diff = 0                         # 记录不同字符的数量
            # 同时遍历两个单词的字符
            for ch_q, ch_d in zip(q, d):
                if ch_q != ch_d:            # 只要字符不相同，就计数
                    diff += 1
                if diff > 2:                # 超过两次编辑就可以提前结束本次比较
                    break
            if diff <= 2:                    # 不超过两次编辑，q 能匹配
                ans.append(q)
                break                         # 已经找到匹配的字典词，q 不需要再继续检查
    return ans
```

#### 复杂度

- **时间复杂度**：`O(queries·dictionary·n)`  
  - 举例：如果 `queries = 100`、`dictionary = 100`、`n = 100`，最坏情况下需要比较 `100×100×100 = 1,000,000` 次字符，这在现代电脑上毫秒级即可完成。
- **空间复杂度**：`O(1)`（不计答案列表）  
  - 只用了几个整数变量 `diff`、循环索引等，和输入规模无关。

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于每次比较都要遍历完整个单词，即使已经发现两个不同字符后仍然继续遍历（虽然我们加了 `break`，但仍然要对每一对单词做一次完整的 `O(n)` 检查）。当 `queries`、`dictionary`、`n` 都比较大时，这种“全遍历”会变得不够高效。

**优化目标**：把“比较所有字典单词”这一步做得更快。我们可以把字典构建成一棵 **Trie（前缀树）**，然后在 Trie 上进行 **深度优先搜索（DFS）**，在搜索过程中实时记录已经出现的不同字符数，一旦超过 2 就立刻剪枝（不再继续往下走）。这样：

- 对于每个查询词，只需要一次 DFS，就能在整个字典中找到所有**编辑距离 ≤ 2**的单词。  
- 由于 Trie 按公共前缀合并了相同的字符，搜索时会复用已经比较过的前缀，避免了大量重复比较。

下面一步步解释核心概念：

1. **Trie（前缀树）**  
   想象把所有字典单词放进一本“字典树”。树的根节点是空的，每往下一层就对应单词的下一个字符。相同前缀的单词会共享同一路径。这样，查询词的前缀相同的字典单词只会被检查一次。

2. **DFS + 剪枝**  
   - 从根节点开始，逐字符向下走。  
   - 维护一个计数器 `diff`，表示已经修改了多少字符（即当前字符不匹配的次数）。  
   - 当 `diff` 已经大于 2 时，说明无论后面怎么走，都不可能满足 “最多两次编辑”，于是**直接返回**，不再继续递归（这就是剪枝）。  
   - 当走到某个节点且该节点标记为单词结束 (`is_word=True`) 且 `diff ≤ 2`，说明我们已经找到一个匹配的字典单词，于是可以把查询词加入答案。

3. **复杂度直观解释**  
   - 每条搜索路径最多只能出现 2 次“不匹配”。因此在最坏情况下，搜索树的分支数是 `C(n,0)+C(n,1)+C(n,2) = 1 + n + n·(n-1)/2`，大约是 `O(n²)`。  
   - 但是实际运行时，大部分分支会因为提前剪枝而停止，尤其是字母表只有 26 个字符，分支的实际数量远小于 `26ⁿ`。  
   - 所以整体时间复杂度是 **`O(queries·(n² + total_nodes))`**，其中 `total_nodes` 是 Trie 中节点的总数（≤ dictionary·n），在本题约为 `10⁴` 级别，远小于暴力解的 `10⁶`。

#### 代码（Python）

```python
from typing import List, Dict

class TrieNode:
    """Trie 的节点，只需要记录子节点和是否是单词结束"""
    __slots__ = ("children", "is_word")
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}   # 类似字典，key 是字符，value 是下一个节点
        self.is_word: bool = False                # 标记从根到这里构成了字典里的完整单词

class Trie:
    """封装 Trie 的构建和搜索功能"""
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """把一个单词插入 Trie"""
        node = self.root
        for ch in word:
            if ch not in node.children:           # 没有对应的子节点就新建
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_word = True                       # 单词结束

    def can_match_within_two_edits(self, word: str) -> bool:
        """
        在 Trie 中查找是否存在一个单词，使得
        与 `word` 的不同字符数 ≤ 2
        """
        n = len(word)

        def dfs(idx: int, node: TrieNode, diff: int) -> bool:
            """
            idx   : 当前正在比较的字符在 `word` 中的下标
            node  : 当前 Trie 节点
            diff  : 已经累计的不同字符数
            """
            if diff > 2:                 # 已经超过两次编辑，剪枝
                return False
            if idx == n:                 # 已经遍历完所有字符
                return node.is_word     # 若此时正好是字典单词结束，则匹配成功

            ch = word[idx]               # 当前字符
            # 1）尝试走匹配的字符分支（不增加 diff）
            if ch in node.children:
                if dfs(idx + 1, node.children[ch], diff):
                    return True

            # 2）尝试走“修改”后的所有其他字符分支（diff + 1）
            for alt, child in node.children.items():
                if alt == ch:            # 已经在上面匹配过的分支，这里跳过
                    continue
                if dfs(idx + 1, child, diff + 1):
                    return True
            return False

        return dfs(0, self.root, 0)

def within_two_edits_optimal(queries: List[str], dictionary: List[str]) -> List[str]:
    """
    最优解：使用 Trie + 剪枝的 DFS
    """
    trie = Trie()
    for w in dictionary:          # 把字典全部插入 Trie
        trie.insert(w)

    ans = []
    for q in queries:
        if trie.can_match_within_two_edits(q):
            ans.append(q)         # 找到匹配就加入答案
    return ans
```

#### 复杂度

- **时间复杂度**：`O(queries · (n² + total_nodes))`  
  - `total_nodes ≤ dictionary·n`（每个单词最多贡献 `n` 个新节点）。  
  - `n²` 来自于“最多两次不匹配”在最坏情况下会产生的组合数。相比暴力解的 `O(queries·dictionary·n)`，这里去掉了 `dictionary` 的线性因子，尤其当字典很大时优势明显。  
  - 简单理解：我们把所有字典单词压缩进一棵树，只在需要“改字母”的时候分支，极大地减少了重复比较。

- **空间复杂度**：`O(total_nodes)`  
  - 用来存放 Trie，最多 `dictionary·n` 个节点。每个节点只保存 26 条可能的指针（实际只会创建出现过的字符），因此在本题约为几千到一万左右的内存，完全可接受。

---

## 心得

- **核心技巧**：利用 **Trie（前缀树）** 结合 **DFS + 剪枝** 在大量相似单词中快速定位编辑距离 ≤ 2 的匹配。  
- **适用的题型**（类似思路）  
  1. “单词搜索 II”（Word Search II）——在二维网格中找出字典里所有单词，需要 Trie + 回溯。  
  2. “拼写检查器”（Spell Checker）——判断一个单词是否在字典里或只差一个字符，同样可以用 Trie + 限制编辑次数的搜索。  
  3. “最长公共前缀”系列——需要对大量单词做前缀统计，Trie 是天然的数据结构。  
- **一句话总结解题钥匙**：**把所有字典单词压进一棵前缀树，用“最多两次不匹配”限制的深度优先搜索一次性搞定所有匹配**。

---

## 反思

- **第一反应**：直接两层循环逐字符比较——这是最自然的暴力思路。  
- **最容易踩的坑**  
  - **漏掉“0 次编辑”**：有的查询词本身已经在字典里，需要记得 `diff = 0` 也算合法。  
  - **提前剪枝**：在暴力解里忘记在发现 `diff > 2` 时立刻 `break`，会导致不必要的遍历。  
  - **Trie 的实现细节**：节点的 `children` 必须使用字典或固定大小的数组，否则会出现 `KeyError`。  
  - **边界条件**：所有单词长度相同，但仍要检查空字符串的情况（本题约束 `n ≥ 1`，但写代码时最好防御性检查）。  
- **下次类似题的第一步**：**先判断是否可以把所有候选集合压缩成 Trie**，再思考“编辑次数限制”如何在搜索过程中进行剪枝。这样往往能把 `O(m·k·n)`（暴力）降到 `O(m·(n²+total_nodes))`，大幅提升效率。