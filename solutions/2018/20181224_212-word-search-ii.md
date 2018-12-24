# #212. 单词搜索 II / Word Search II

> 难度：困难 · 标签：Array、String、Backtracking、Trie、Matrix · [LeetCode 链接](https://leetcode.com/problems/word-search-ii/)

---

## 题目（英文原版）

**Description**

Given an m x n board of characters and a list of strings words, return all words on the board.
Each word must be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once in a word.

**Examples**

**Example 1:**

```
Input: board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]], words = ["oath","pea","eat","rain"]
Output: ["eat","oath"]
```

**Example 2:**

```
Input: board = [["a","b"],["c","d"]], words = ["abcb"]
Output: []
```

**Constraints**

- m == board.length
- n == board[i].length
- 1 <= m, n <= 12
- board[i][j] is a lowercase English letter.
- 1 <= words.length <= 3 * 104
- 1 <= words[i].length <= 10
- words[i] consists of lowercase English letters.
- All the strings of words are unique.

---

## 题目（中文翻译）

给定一个 **m × n** 棋盘（board）`board`，其中每个格子包含一个字符，以及一个单词列表（words）`words`，请返回所有能够在棋盘上找到的单词。

每个单词必须由**顺序相邻的单元格（adjacent cells）**中的字母组成，相邻单元格指水平或垂直相邻的格子。**同一个单元格（cell）**在构成同一个单词的过程中**不能被重复使用**。

---

### 示例

**示例 1**

```text
Input: board = [["o","a","a","n"],
                ["e","t","a","e"],
                ["i","h","k","r"],
                ["i","f","l","v"]],
       words = ["oath","pea","eat","rain"]
Output: ["eat","oath"]
```

**示例 2**

```text
Input: board = [["a","b"],
                ["c","d"]],
       words = ["abcb"]
Output: []
```

---

### 约束条件

- `m == board.length`
- `n == board[i].length`
- `1 <= m, n <= 12`
- `board[i][j]` 为小写英文字母
- `1 <= words.length <= 3 * 10^4`
- `1 <= words[i].length <= 10`
- `words[i]` 仅由小写英文字母组成
- `words` 中的所有字符串互不相同

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **每个单词** 当成一次独立的搜索任务：

1. 把单词的第一个字符在整个棋盘上找所有匹配的位置（就像在地图上找所有“起点”）。
2. 从每个起点开始，用 **回溯（DFS）** 按上下左右四个方向深度搜索，尝试把单词的后面的字符一个一个拼出来。  
   - 为了不走回头路，需要把已经走过的格子标记为“已访问”，搜索完后再恢复（就像走迷宫时在路线上贴临时的记号）。
3. 如果能把整个单词的字符全部走完，就把这个单词加入答案。

> **类比**：  
> - 哈希表（字典）可以想象成一本“词典”，key 是单词，value 是解释。这里我们不需要全局的词典，只是一次一次地检查单词是否存在，故不需要哈希表。  
> - 回溯就像在寻找一条从起点到终点的路径，走错了就“撤回”一步，继续尝试别的方向。

**为什么正确**：  
- 对每个单词我们穷举了所有可能的起点和所有可能的走法，只要有合法路径就一定会被找到。  
- 只要不违反“同一个格子只能使用一次”的规则，所有合法路径都会被遍历到。

#### 代码（Python）

```python
from typing import List

def findWords_bruteforce(board: List[List[str]], words: List[str]) -> List[str]:
    m, n = len(board), len(board[0])
    res = []

    # 四个方向：上、下、左、右
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # 深度优先搜索，检查 word[pos:] 是否能从 (i, j) 开始匹配
    def dfs(i: int, j: int, pos: int, word: str, visited: List[List[bool]]) -> bool:
        if pos == len(word):          # 已经匹配完所有字符
            return True
        # 越界或字符不匹配或已经访问过
        if i < 0 or i >= m or j < 0 or j >= n or visited[i][j] or board[i][j] != word[pos]:
            return False

        visited[i][j] = True          # 标记已访问
        # 继续向四个方向探索
        for di, dj in dirs:
            if dfs(i + di, j + dj, pos + 1, word, visited):
                visited[i][j] = False # 恢复现场，供后续搜索使用
                return True
        visited[i][j] = False         # 恢复现场
        return False

    for word in words:                 # 对每个单词单独搜索
        found = False
        visited = [[False] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if board[i][j] == word[0]:      # 只从匹配首字符的格子开始
                    if dfs(i, j, 0, word, visited):
                        res.append(word)
                        found = True
                        break
            if found:
                break

    return res
```

#### 复杂度

- **时间复杂度**：`O( W * m * n * 4^L )`  
  - `W` 为单词数，`m*n` 为棋盘格子数，`L` 为单词的最大长度。  
  - “`4^L`” 表示每走一步最多有 4 种选择，最坏情况下会尝试所有可能的走法。  
  - 用大白话说：如果有 1000 个单词，每个单词长度是 10，棋盘是 12×12，那么搜索次数会非常大，几乎是“指数级”增长，容易超时。

- **空间复杂度**：`O(m*n)`  
  - 主要是 `visited` 矩阵占用的空间，以及递归栈深度最多 `L`（ ≤ 10），这在本题是可以接受的。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **每个单词都要单独遍历整张棋盘**，而且搜索时没有任何提前剪枝。  
我们可以把所有单词 **一次性组织起来**，在搜索时 **同步检查多个单词的前缀**，只要当前路径已经不可能构成任何单词的前缀，就可以立刻停止搜索，这样可以大幅减少无效的搜索分支。

要实现 “前缀查询”，最合适的数据结构是 **Trie（前缀树）**：

- **Trie** 想象成一本“字典树”，每个节点代表一个字符，沿着根到某个节点的路径恰好是一组单词的公共前缀。  
- 插入一个单词的时间是字符数 `O(L)`，查询一个前缀是否存在同样是 `O(L)`。  
- 与哈希表不同，哈希表只能判断“完整的单词是否在集合中”，而不能高效地判断“某个前缀是否可能出现”。Trie 正好解决了这个需求。

**整体思路**：

1. **构建 Trie**：把 `words` 中的所有单词插入到同一棵 Trie 中，每个节点保存：
   - `children`：指向子节点的字典（字符 → 节点）。
   - `word`：若当前节点恰好对应某个完整单词，则把单词本身存进去（便于直接收集答案）。
2. **遍历棋盘**：对每个格子 `(i, j)`，尝试把它作为搜索的起点，执行 **回溯 DFS**，但在每一步：
   - 先检查当前字符是否在当前 Trie 节点的 `children` 中；若不存在，说明 **没有任何单词的前缀会走到这里**，直接返回（剪枝）。
   - 若存在，则进入对应的子节点继续搜索。
   - 当进入的子节点保存了 `word`（表示已经完整匹配了一个单词），把它加入答案并把 `word` 设为 `None`，防止同一个单词被重复加入。
3. **标记已访问**：同暴力解一样，用原地修改 `board[i][j] = '#'` 表示已访问，搜索完后再恢复原字符。
4. **返回答案**。

这样，**每个格子只会被访问一次**（因为一旦走到某条路径，若前缀不存在就立刻停止），总体时间复杂度大幅降低。

#### 代码（Python）

```python
from typing import List, Dict

class TrieNode:
    """Trie 的节点，children 用字典存放子字符，word 保存完整单词（用于收集答案）"""
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.word: str = None          # None 表示不是单词结束

def build_trie(words: List[str]) -> TrieNode:
    """把所有单词插入同一棵 Trie，返回根节点"""
    root = TrieNode()
    for w in words:
        node = root
        for ch in w:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.word = w                 # 标记完整单词
    return root

def findWords(board: List[List[str]], words: List[str]) -> List[str]:
    m, n = len(board), len(board[0])
    root = build_trie(words)
    res = []

    # 四个方向
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def dfs(i: int, j: int, node: TrieNode):
        ch = board[i][j]
        if ch == '#':                 # 已经被访问过
            return

        if ch not in node.children:   # 前缀不存在，直接剪枝
            return

        nxt = node.children[ch]       # 移动到子节点
        if nxt.word:                  # 找到一个完整单词
            res.append(nxt.word)
            nxt.word = None           # 防止重复加入

        # 标记为已访问，避免重复使用同一格子
        board[i][j] = '#'

        # 向四个方向继续搜索
        for di, dj in dirs:
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n:
                dfs(ni, nj, nxt)

        # 恢复现场，供其他路径使用
        board[i][j] = ch

        # 可选的优化：如果 nxt 的子树已经没有任何单词了，删除该分支
        if not nxt.children:
            del node.children[ch]

    for i in range(m):
        for j in range(n):
            dfs(i, j, root)

    return res
```

#### 复杂度

- **时间复杂度**：`O(m * n * L)`  
  - 每个格子最多进入一次 DFS，DFS 的深度受单词最大长度 `L`（≤10）限制。  
  - 虽然在最坏情况下仍可能遍历所有格子并尝试所有方向，但 **剪枝** 大幅降低了实际遍历次数。  
  - 与暴力解的 `O(W * m * n * 4^L)` 相比，指数级的 `4^L` 被降到了线性的 `L`，速度提升数百倍。

- **空间复杂度**：`O(T + m * n)`  
  - `T` 为 Trie 所占的节点总数，最多是所有单词字符数之和（ ≤ 3·10⁴ * 10 = 3·10⁵），在本题范围内完全可接受。  
  - 递归栈深度最多 `L`，加上原地标记的 `board`（不算额外空间），总体仍然是线性空间。

---

## 心得

- **核心技巧**：利用 Trie（前缀树）把所有单词组织在一起，在搜索时同步检查前缀，做到“边走边剪枝”。  
- **适用的题型**  
  1. **Word Search / Word Search II**（在网格中找单词）  
  2. **拼写检查**（给定大量单词，快速判断前缀是否存在）  
  3. **搜索引擎自动补全**（根据已输入的前缀返回可能的完整单词）  
- **一句话总结**：**把所有单词的公共前缀压进一棵 Trie，用它来提前判断“这条路还能走吗”。**  

---

## 反思

- **第一反应**：直接对每个单词做深度优先搜索，代码容易写，但会超时。  
- **最容易踩的坑**  
  - **重复加入同一个单词**：因为不同起点可能走到同一个完整单词，需要在 Trie 节点上把 `word` 置为 `None`，防止重复。  
  - **原地标记恢复错误**：忘记在回溯结束后把 `board[i][j]` 恢复成原字符，会导致后续搜索出错。  
  - **Trie 的删除优化**：如果不及时删除已经没有后续单词的分支，搜索时仍会遍历无用的路径，性能会受影响。  
- **下次遇到同类题**，第一步应该思考：“**是否可以把所有待匹配的目标一次性组织起来，用一种结构快速判断前缀**”。如果答案是**是**，那么就考虑构建 Trie 或者其他前缀查询结构，再结合回溯进行剪枝。