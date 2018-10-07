# #126. 单词接龙 II / Word Ladder II

> 难度：困难 · 标签：Hash Table、String、Backtracking、Breadth-First Search · [LeetCode 链接](https://leetcode.com/problems/word-ladder-ii/)

---

## 题目（英文原版）

**Description**

A transformation sequence from word beginWord to word endWord using a dictionary wordList is a sequence of words beginWord -> s1 -> s2 -> ... -> sk such that:
Given two words, beginWord and endWord, and a dictionary wordList, return all the shortest transformation sequences from beginWord to endWord, or an empty list if no such sequence exists. Each sequence should be returned as a list of the words [beginWord, s1, s2, ..., sk].

**Examples**

**Example 1:**

```
Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"]
Output: [["hit","hot","dot","dog","cog"],["hit","hot","lot","log","cog"]]
Explanation: There are 2 shortest transformation sequences:
"hit" -> "hot" -> "dot" -> "dog" -> "cog"
"hit" -> "hot" -> "lot" -> "log" -> "cog"
```

**Example 2:**

```
Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log"]
Output: []
Explanation: The endWord "cog" is not in wordList, therefore there is no valid transformation sequence.
```

**Constraints**

- 1 <= beginWord.length <= 5
- endWord.length == beginWord.length
- 1 <= wordList.length <= 500
- wordList[i].length == beginWord.length
- beginWord, endWord, and wordList[i] consist of lowercase English letters.
- beginWord != endWord
- All the words in wordList are unique.
- The sum of all shortest transformation sequences does not exceed 105.

---

## 题目（中文翻译）

从单词 `beginWord` 到单词 `endWord` 使用字典（dictionary）`wordList` 的转换序列是一个形如 `beginWord -> s1 -> s2 -> ... -> sk` 的单词序列，使得相邻两个单词仅相差一个字符。  

给定两个单词 `beginWord` 和 `endWord`，以及字典 `wordList`，返回所有 **最短** 的转换序列。如果不存在满足条件的序列，则返回空列表。每条序列应以列表形式返回，形如 `[beginWord, s1, s2, ..., sk]`。  

## 示例  

### 示例 1  
**输入**  
```
beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"]
```  
**输出**  
```
[["hit","hot","dot","dog","cog"],["hit","hot","lot","log","cog"]]
```  
**解释**  
存在两条最短的转换序列：  
- `"hit" -> "hot" -> "dot" -> "dog" -> "cog"`  
- `"hit" -> "hot" -> "lot" -> "log" -> "cog"`  

### 示例 2  
**输入**  
```
beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log"]
```  
**输出**  
```
[]
```  
**解释**  
`endWord` `"cog"` 不在 `wordList` 中，因此不存在有效的转换序列。  

## 约束条件  

- `1 <= beginWord.length <= 5`  
- `endWord.length == beginWord.length`  
- `1 <= wordList.length <= 500`  
- `wordList[i].length == beginWord.length`  
- `beginWord`、`endWord` 和 `wordList[i]` 均由小写英文字母组成。  
- `beginWord != endWord`  
- `wordList` 中的所有单词互不相同。  
- 所有最短转换序列的总数不超过 `10^5`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**穷举**所有可能的单词转换序列，然后挑出最短的那些。  
可以把每一步看成在一个**字典树**里走一步：  
- 当前单词 `cur` → 把它的每个字符换成 `'a'~'z'`，得到所有“相邻”单词。  
- 只要相邻单词在 `wordList`（相当于一本“查字典”），就可以继续往下走。  

于是我们可以用 **深度优先搜索（DFS）** 从 `beginWord` 一路递归到底 `endWord`，把走过的路径记录下来。  
只要在搜索过程中记录下当前路径的长度，一旦发现已经超过已知的最短长度，就可以提前剪枝（因为我们只想要最短的）。  

> **类比**：把 `wordList` 想成一本字典，`key` 是单词，`value` 是它的页码。DFS 就像在字典里一步步翻页，找出所有能从起点页跳到终点页的路径。

**为什么能得到正确答案**  
- DFS 会遍历 **所有** 合法的转换序列（只要不超出字典的限制），因此最短序列一定会被遍历到。  
- 通过记录最短长度并在后续搜索中剪枝，最终留下的就是所有最短的序列。

**时间/空间复杂度**  
- 最坏情况下，单词数 `n = len(wordList)`，每个单词有 `L`（≤5）个字符。每个字符可以换成 26 种可能，所以每个单词的“相邻”数最多是 `26 * L`。  
- 暴力 DFS 需要尝试所有可能的路径，路径长度最坏是 `n`，于是时间复杂度约为 **O( (26·L)ⁿ )**，指数级爆炸，实际会因为剪枝稍好，但仍然不可接受。  
- 空间上需要保存递归栈和当前路径，最坏 O(n)（递归深度）。

> **大白话**：时间复杂度的 `O( (26·L)ⁿ )` 就像说“每走一步都有 26·L 种选择，走 n 步就会产生 26·L 的 n 次方种可能”，这在实际里几乎不可能跑完。

#### 代码（Python）

```python
from typing import List

def findLadders_bruteforce(beginWord: str, endWord: str, wordList: List[str]) -> List[List[str]]:
    word_set = set(wordList)                 # 用集合查找单词，速度像查字典
    if endWord not in word_set:
        return []

    L = len(beginWord)                       # 单词长度（题目保证相同）
    res: List[List[str]] = []                # 保存所有最短路径
    shortest = float('inf')                  # 当前已知的最短长度

    def dfs(cur: str, path: List[str], visited: set):
        nonlocal shortest
        # 已经走得比已知最短的还长，直接返回，省掉后面的搜索
        if len(path) > shortest:
            return

        if cur == endWord:                    # 到达终点
            if len(path) < shortest:         # 发现更短的路径
                shortest = len(path)
                res.clear()                  # 以前的都不是最短，清空
            res.append(path.copy())          # 保存这条最短路径
            return

        # 枚举所有可能的相邻单词
        for i in range(L):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                if c == cur[i]:
                    continue
                nxt = cur[:i] + c + cur[i+1:]   # 把第 i 个字符换成 c
                if nxt in word_set and nxt not in visited:
                    visited.add(nxt)            # 标记为已访问，防止循环
                    path.append(nxt)
                    dfs(nxt, path, visited)
                    path.pop()                  # 回溯，撤销这一步
                    visited.remove(nxt)

    dfs(beginWord, [beginWord], {beginWord})
    return res
```

#### 复杂度

- **时间复杂度**：`O((26·L)^n)`（指数级），因为会尝试所有可能的单词序列。  
- **空间复杂度**：`O(n)`，递归栈深度最多等于单词数量。

> 实际上，这种暴力方法在 `wordList` 长度稍大时（如 > 10）就会超时，属于**不可行**的思路，只适合作为思考起点。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**搜索的瓶颈**在于我们把所有路径都枚举了一遍，而实际上只需要**最短层数**的路径。  
这就可以用 **广度优先搜索（BFS）** 来先找到最短层数，然后再在这层数范围内回溯所有合法路径。

**步骤一：BFS 构造层次图（邻接表）**  
- 从 `beginWord` 开始层层展开，每次只保留**本层**能到达的单词（因为同层的单词已经是最短距离）。  
- 为了在后面回溯时知道每个单词是从哪些前驱单词得到的，建立一个 **predecessor 列表** `parents[child] = [parent1, parent2, …]`。  
- 只要在 BFS 过程中遇到 `endWord`，说明已经找到了最短层数，后面的层可以不再继续（因为再往后会更长）。

**步骤二：DFS（或递归）从 `endWord` 逆向回溯到 `beginWord`**  
- 有了 `parents` 信息，我们可以从终点开始向前找所有可能的前驱，形成一棵倒置的搜索树。  
- 递归把路径拼接起来，直到回到 `beginWord`，再把路径反转得到正向序列。  
- 由于 `parents` 只记录最短层次的前驱，所有得到的路径必然是**最短的**。

**核心数据结构解释**  
- **集合（set）**：像字典的“查页码”，判断一个单词是否在 `wordList` 中是 O(1) 时间。  
- **队列（deque）**：实现 BFS 的“排队”。每次弹出队首，向外扩散。  
- **defaultdict(list)**：存前驱列表，类似每本书的“参考文献列表”。  
- **层集合（level_set）**：记录本层已经访问过的单词，防止同层重复加入队列导致冗余搜索。

**为什么最优**  
- BFS 只遍历一次所有单词，时间是 **O(N·L·26)**，其中 `N = len(wordList)`，`L` 是单词长度。  
- 只记录最短层次的前驱，回溯阶段的搜索空间大大缩小，整体仍保持线性级别。  

#### 代码（Python）

```python
from collections import defaultdict, deque
from typing import List

def findLadders(beginWord: str, endWord: str, wordList: List[str]) -> List[List[str]]:
    word_set = set(wordList)               # 快速判断单词是否存在
    if endWord not in word_set:
        return []

    L = len(beginWord)                     # 单词长度
    # ---------- 第一步：BFS 构造前驱图 ----------
    parents = defaultdict(list)            # child -> [all possible parents in shortest path]
    # 记录已经在更早层次访问过的单词，防止重复加入队列
    visited = set([beginWord])
    # 当前层的单词集合
    level_set = set([beginWord])

    found = False                           # 是否已经在某层遇到 endWord
    while level_set and not found:
        next_level = set()                  # 下一层的单词集合
        for word in level_set:
            # 枚举所有可能的相邻单词
            for i in range(L):
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    if c == word[i]:
                        continue
                    nxt = word[:i] + c + word[i+1:]
                    if nxt not in word_set:
                        continue
                    # 只要 nxt 在本层或更早层出现，就可以记录前驱关系
                    if nxt not in visited:
                        next_level.add(nxt)
                    # 不管 nxt 是否已经在 visited，只要它在本层或下一层，都把当前 word 记录为前驱
                    if nxt in next_level or nxt in visited:
                        parents[nxt].append(word)
                    if nxt == endWord:
                        found = True          # 已经找到最短层次

        # 将本层的单词加入 visited，防止以后层再次访问（保证 BFS 层序）
        visited.update(next_level)
        level_set = next_level

    if not found:                           # 没有任何路径到达 endWord
        return []

    # ---------- 第二步：DFS 逆向回溯 ----------
    res: List[List[str]] = []

    def backtrack(word: str, path: List[str]):
        """从 endWord 递归回到 beginWord，path 保存逆序路径"""
        if word == beginWord:
            # path 现在是 [end, ..., begin]，翻转后加入结果
            res.append(path[::-1])
            return
        for parent in parents[word]:
            backtrack(parent, path + [parent])   # 向前继续找前驱

    backtrack(endWord, [endWord])
    return res
```

#### 复杂度

- **时间复杂度**：`O(N * L * 26)`  
  - BFS：每个单词最多遍历 `L` 个位置，每个位置尝试 26 种字符 → `O(N·L·26)`。  
  - 回溯：只在最短层次的前驱图上递归，所有路径总数 ≤ `10⁵`（题目保证），因此仍是线性级别。  
  与暴力解的指数级时间相比，简直是天壤之别。

- **空间复杂度**：`O(N * L)`  
  - `parents` 存储每个单词的前驱列表，最坏每个单词都有 `O(N)` 前驱，但实际受限于层数，整体在 `O(N·L)` 量级。  
  - 队列、集合等临时结构也都是 `O(N)`。  

> **对比**：暴力解需要遍历所有可能的路径，时间爆炸；最优解先用 BFS 把搜索范围锁定在最短层次，再用有向无环图回溯，真正实现了 **线性时间**。

---

## 心得

- **核心技巧**：先用 **BFS** 找到最短层次（保证最短路径），再用 **逆向 DFS + 前驱图** 生成所有最短路径。  
- **适用的题型**  
  1. “求所有最短路径” 类问题（如 LeetCode 126 `Word Ladder II`、127 `Word Ladder` 的变体）。  
  2. 图中 **多源最短路径** 并需要列举所有路径的情况（如迷宫最短路径的全部解）。  
  3. 需要先**层次遍历**再**回溯**的组合题（如“最小基因变化” 433）。  
- **一句话总结**：**先用 BFS 把搜索范围压到最短层，再在这层构建前驱图逆向回溯，即可高效输出所有最短转换序列。**

---

## 反思

- **第一反应**：直接想把所有可能的转换序列枚举出来（DFS 暴力），这会导致时间爆炸。  
- **最容易踩的坑**  
  - **忘记在 BFS 中去重**：同一层的单词如果多次加入队列，会导致前驱记录重复，甚至出现环路。  
  - **剪枝不够**：只要在 BFS 发现 `endWord`，就应停止继续扩展更深的层，否则会把非最短路径也加入图中。  
  - **回溯顺序**：逆向回溯时一定要把路径翻转，否则返回的序列顺序会是 `end → … → begin`。  
  - **边界条件**：`endWord` 不在 `wordList`、`wordList` 为空、`beginWord` 与 `endWord` 长度不同等，都要提前判断。  
- **下次遇到同类题**：第一步先 **做一次 BFS 只求最短距离**，记录每层的前驱；第二步 **在这层的前驱图上做回溯**，即可得到所有最短解。这样既能保证正确性，又能避免指数级爆炸。