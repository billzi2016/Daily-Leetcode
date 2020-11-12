# #1048. 最长字符串链 / Longest String Chain

> 难度：中等 · 标签：Array、Hash Table、Two Pointers、String、Dynamic Programming、Sorting · [LeetCode 链接](https://leetcode.com/problems/longest-string-chain/)

---

## 题目（英文原版）

**Description**

You are given an array of words where each word consists of lowercase English letters.
wordA is a predecessor of wordB if and only if we can insert exactly one letter anywhere in wordA without changing the order of the other characters to make it equal to wordB.
A word chain is a sequence of words [word1, word2, ..., wordk] with k >= 1, where word1 is a predecessor of word2, word2 is a predecessor of word3, and so on. A single word is trivially a word chain with k == 1.
Return the length of the longest possible word chain with words chosen from the given list of words.

**Examples**

**Example 1:**

```
Input: words = ["a","b","ba","bca","bda","bdca"]
Output: 4
Explanation: One of the longest word chains is ["a","ba","bda","bdca"].
```

**Example 2:**

```
Input: words = ["xbc","pcxbcf","xb","cxbc","pcxbc"]
Output: 5
Explanation: All the words can be put in a word chain ["xb", "xbc", "cxbc", "pcxbc", "pcxbcf"].
```

**Example 3:**

```
Input: words = ["abcd","dbqca"]
Output: 1
Explanation: The trivial word chain ["abcd"] is one of the longest word chains.
["abcd","dbqca"] is not a valid word chain because the ordering of the letters is changed.
```

**Constraints**

- 1 <= words.length <= 1000
- 1 <= words[i].length <= 16
- words[i] only consists of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串数组 `words`，其中每个单词仅由小写英文字母组成。  

`wordA` 是 `wordB` 的前驱（predecessor），当且仅当我们可以在 `wordA` 的任意位置插入恰好一个字母，且不改变其余字符的相对顺序，使得得到的字符串等于 `wordB`。  

单词链（word chain）是一系列单词 `[word1, word2, ..., wordk]`（k ≥ 1），满足 `word1` 是 `word2` 的前驱，`word2` 是 `word3` 的前驱，依此类推。单个单词本身也构成长度为 1 的单词链（k == 1）。  

返回从给定单词列表中选取的、可能的最长单词链的长度。

## 示例

### 示例 1
**Input:** `words = ["a","b","ba","bca","bda","bdca"]`  
**Output:** `4`  
**Explanation:** 其中一种最长的单词链是 `["a","ba","bda","bdca"]`。

### 示例 2
**Input:** `words = ["xbc","pcxbcf","xb","cxbc","pcxbc"]`  
**Output:** `5`  
**Explanation:** 所有单词都可以组成一个单词链 `["xb", "xbc", "cxbc", "pcxbc", "pcxbcf"]`。

### 示例 3
**Input:** `words = ["abcd","dbqca"]`  
**Output:** `1`  
**Explanation:** 平凡的单词链 `["abcd"]` 是最长单词链之一。`["abcd","dbqca"]` 不是有效的单词链，因为字母的顺序被改变了。

## 约束条件

- `1 <= words.length <= 1000`
- `1 <= words[i].length <= 16`
- `words[i]` 仅由小写英文字母组成。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有单词** 看成图中的节点，  
如果 `wordA` 能通过在任意位置插入 **恰好一个** 字母得到 `wordB`，  
就把一条有向边 `wordA → wordB` 画出来。  
这样，**最长的单词链** 就是这张有向图中最长的路径。

> **类比**：把每个单词想成一本字典里的词条，  
> 如果把 `wordA` 这本词条的某一页（字符）撕掉再加回去正好变成 `wordB`，  
> 那么 `wordA` 就是 `wordB` 的前驱。  

我们可以从每个单词出发，用深度优先搜索（DFS）把所有可能的后继都遍历一遍，  
记录遍历到的最大链长。

> **为什么正确**：DFS 会穷举 **所有** 合法的前驱‑后继关系，  
> 因此一定能找到最长的那条路径。

> **时间/空间分析（大白话）**：  
> - 对每个单词，我们都要尝试把它和 **其它所有单词** 比对一次，看看是否满足「插入一个字符」的条件，这一步本身是 `O(N²·L)`（`L` 为单词最长长度）。  
> - 再加上递归搜索的过程，最坏情况下会遍历所有排列组合，时间复杂度呈 **指数级**，记作 `O(N!)`（想象一下把 10 本书排成所有可能的顺序，需要 10! 种方式）。  
> - 递归栈最多会保存 `N` 层调用，空间复杂度是 `O(N)`。

> 对于 `N ≤ 1000` 的题目，这种指数级算法根本跑不动，只能用来帮助我们 **理解** 问题。

#### 代码（Python）

```python
from typing import List

def is_predecessor(a: str, b: str) -> bool:
    """判断 a 是否是 b 的前驱（在 a 任意位置插入一个字符得到 b）"""
    if len(b) - len(a) != 1:          # 长度必须差 1
        return False
    i = j = 0
    skipped = False                   # 是否已经跳过了 b 中多余的那个字符
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            i += 1
            j += 1
        elif not skipped:              # 第一次遇到不相等，就把 b 的这个字符“删掉”
            skipped = True
            j += 1
        else:                           # 已经删过一次，还不相等，说明不是前驱
            return False
    return True                         # 剩余的字符要么全匹配，要么正好是多余的那一个

def dfs(word: str, words: List[str], visited: dict) -> int:
    """从 word 出发，深度优先搜索能得到的最长链长（不带记忆化）"""
    max_len = 1                         # 至少包含自己
    for nxt in words:
        if is_predecessor(word, nxt):
            cur = 1 + dfs(nxt, words, visited)
            max_len = max(max_len, cur)
    return max_len

def longestStrChain_bruteforce(words: List[str]) -> int:
    """暴力版：对每个单词都做一次完整的 DFS"""
    n = len(words)
    ans = 1
    for w in words:
        ans = max(ans, dfs(w, words, {}))
    return ans
```

> 代码里没有使用记忆化（`visited` 没用），所以会产生大量重复计算，导致指数级时间。

#### 复杂度  

- **时间复杂度**：`O(N! )`（指数级）——因为每条可能的链都会被完整遍历。  
- **空间复杂度**：`O(N)`——递归栈最深为 `N`。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈** 在于：

1. **大量无效比较**：我们把每个单词和所有其它单词都比对，实际上只需要比较**长度相差 1** 的单词。  
2. **重复子问题**：同一个单词可能被多次递归求解，导致指数级时间。

**关键观察**：  
- 如果把「在 wordA 中插入一个字符得到 wordB」的过程**倒过来**思考，等价于「把 wordB 删除一个字符后得到 wordA」。  
- 删除字符比插入字符更容易实现：只要把 word 的每个位置的字符删掉一次，生成 `len(word)` 个“候选前驱”，检查它们是否在原数组中出现即可。

**一步步推导**：

1. **把单词按长度从短到长排序**。这样，当我们处理某个单词 `w` 时，所有可能的前驱（长度比 `w` 短 1 的单词）已经处理完毕，链长信息已经存下来。  
2. 用 **哈希表**（相当于查字典）记录每个单词对应的**最长链长度**。  
3. 对于当前单词 `w`，枚举 `len(w)` 种删除方式，得到 `prev`。如果 `prev` 在哈希表中出现，说明 `prev → w` 是合法的前驱‑后继关系，链长可以更新为 `max(dp[w], dp[prev] + 1)`。  
4. 最后遍历哈希表的最大值即为答案。

> **类比**：把每本词典（单词）看成一座楼层，楼层高度就是单词长度。我们从低层往高层搬砖（更新链长），每次只能往上搬一层（只能插入一个字符），于是只需要记住每层的最高砖数（最长链长），不必回头再搬。

#### 代码（Python）

```python
from typing import List

def longestStrChain(words: List[str]) -> int:
    # 1️⃣ 按长度升序排列，短的先处理
    words.sort(key=len)

    # 2️⃣ 哈希表：单词 -> 当前已知的最长链长度（至少为 1）
    dp = {}                     # 类似“查字典”，key 是单词，value 是最长链长

    ans = 1                     # 最少有一个单词，链长为 1
    for w in words:
        best = 1                # 默认只包含自己
        # 3️⃣ 枚举所有可能的前驱：删除 w 中的每一个字符
        for i in range(len(w)):
            prev = w[:i] + w[i+1:]          # 删除第 i 个字符得到的候选前驱
            if prev in dp:                  # 如果这个前驱真的在原数组里
                # 前驱的最长链 + 当前这个单词，形成新的链长
                best = max(best, dp[prev] + 1)

        dp[w] = best            # 把 w 的最长链长度写进字典
        ans = max(ans, best)    # 更新全局最大值

    return ans
```

> **关键行解释**  
> - `words.sort(key=len)`：把「短的先来」的原则变成代码，保证我们在处理 `w` 时，所有可能的 `prev` 已经有 `dp` 记录。  
> - `prev = w[:i] + w[i+1:]`：把第 `i` 位字符「删掉」形成候选前驱，等价于「在 prev 中插入一个字符」得到 `w`。  
> - `if prev in dp`：这里的 `dp` 就像一本「单词 → 链长」的字典，查找是否存在合法前驱。  
> - `best = max(best, dp[prev] + 1)`：如果 `prev` 能构成更长的链，就把它「接」到 `w` 上。

#### 复杂度  

- **时间复杂度**：`O(N·L²)`  
  - `N` 为单词数量（≤1000），`L` 为单词最大长度（≤16）。  
  - 对每个单词我们要枚举 `L` 次删除，每次生成的 `prev` 长度为 `L-1`，字符串切片操作本身是 `O(L)`，所以总共是 `N·L·L = N·L²`。  
  - 实际上因为 `L` 很小（最多 16），这段代码运行非常快。  

- **空间复杂度**：`O(N)`  
  - 哈希表 `dp` 需要存储每个单词对应的链长，大小正比于单词数量。  

> 与暴力解相比，时间从指数级降到了 **线性乘以一个很小的平方因子**，完全可以在 1000 条数据内毫秒级完成。

---

## 心得  

- **核心技巧**：把「插入一个字符」的关系**反向**为「删除一个字符」，并利用**哈希表 + 按长度排序的 DP**求解。  
- **适用的题型**（类似思路）  
  1. **单词接龙**（Word Ladder）——利用 BFS + 哈希表搜索相邻单词。  
  2. **最长递增子序列**（Longest Increasing Subsequence）——把「前驱」的定义改为「数值更小且下标在前」，同样用 DP + 哈希/二分优化。  
  3. **最长字母序列**（Longest String Chain 变形）——比如只允许「替换」一个字符，可采用类似的「枚举所有可能的前驱」思路。  
- **一句话总结**：**把正向的「插入」转成「删除」，配合长度排序和哈希记忆，动态规划即可一次遍历得到最长链**。

---

## 反思  

- **第一反应**：看到「前驱」的定义就想到「图」和「DFS」——想把所有可能的路径都枚举出来。  
- **最容易踩的坑**  
  1. **忽略长度差**：直接比较每两个单词的前后关系会导致 `O(N²·L)` 的不必要开销，甚至错过一些合法前驱。  
  2. **没有记忆化**：递归/DFS 时会重复计算同一个子问题，导致指数级时间。  
  3. **特殊情况**：单词集合中可能只有长度相同的单词，这时最长链只能是 `1`，需要初始化答案为 `1`。  
- **下次类似题的第一步**：**先把关系倒过来思考**（比如「插入」→「删除」），再检查「长度」或「数值」的单调性，决定是否可以用「按某个属性排序 + DP」的模板来一次遍历求解。