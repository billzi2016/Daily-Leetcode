# #854. K 相似字符串 / K-Similar Strings

> 难度：困难 · 标签：Hash Table、String、Breadth-First Search · [LeetCode 链接](https://leetcode.com/problems/k-similar-strings/)

---

## 题目（英文原版）

**Description**

Strings s1 and s2 are k-similar (for some non-negative integer k) if we can swap the positions of two letters in s1 exactly k times so that the resulting string equals s2.
Given two anagrams s1 and s2, return the smallest k for which s1 and s2 are k-similar.

**Examples**

**Example 1:**

```
Input: s1 = "ab", s2 = "ba"
Output: 1
Explanation: The two string are 1-similar because we can use one swap to change s1 to s2: "ab" --> "ba".
```

**Example 2:**

```
Input: s1 = "abc", s2 = "bca"
Output: 2
Explanation: The two strings are 2-similar because we can use two swaps to change s1 to s2: "abc" --> "bac" --> "bca".
```

**Constraints**

- 1 <= s1.length <= 20
- s2.length == s1.length
- s1 and s2 contain only lowercase letters from the set {'a', 'b', 'c', 'd', 'e', 'f'}.
- s2 is an anagram of s1.

---

## 题目（中文翻译）

**描述**  
如果可以通过恰好 **k** 次交换（swap） s1 中两个字母的位置，使得得到的字符串等于 s2，则称字符串 s1 和 s2 为 **k**‑相似（k‑similar），其中 **k** 为非负整数。  
给定两个变位词（anagram） s1 和 s2，返回使 s1 与 s2 **k**‑相似的最小 **k**。

**示例**

**示例 1**  
输入: `s1 = "ab", s2 = "ba"`  
输出: `1`  
解释: 这两个字符串是 1‑相似的，因为只需一次交换即可将 s1 变为 s2：`"ab" --> "ba"`。

**示例 2**  
输入: `s1 = "abc", s2 = "bca"`  
输出: `2`  
解释: 这两个字符串是 2‑相似的，因为可以通过两次交换将 s1 变为 s2：`"abc" --> "bac" --> "bca"`。

**约束条件**  
- `1 <= s1.length <= 20`  
- `s2.length == s1.length`  
- `s1` 和 `s2` 仅包含集合 `{'a', 'b', 'c', 'd', 'e', 'f'}` 中的小写字母。  
- `s2` 是 `s1` 的变位词（anagram）。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **“把 s1 通过若干次任意两字符交换得到 s2”** 看成在状态空间里走路：  

- 每一个状态就是一种字符串（比如 `"abca"`）。  
- 从一个状态出发，任选两个位置 `i、j` 交换字符，就得到一个相邻的状态。  

于是我们可以把所有可能的字符串当成图的节点，用 **广度优先搜索（BFS）** 从 `s1` 开始，一层层展开所有可能的交换，第一次碰到 `s2` 时层数就是最少的交换次数 `k`。

> **类比**：把 `s1` 想成一本词典里的一页，想要翻到 `s2` 那页。每一次“翻页”就是把两个字母换位，所有能翻到的页组成一个大网格，BFS 就像从起点一步步向外扩散，最先到达目标页的层数就是答案。

**为什么正确**  
BFS 的核心特性是**层序遍历**：先遍历 0 步能到达的状态，再遍历 1 步能到达的状态……所以第一次遇到目标状态时，必然是最少步数。

**时间/空间分析（大白话）**  

- 对长度为 `n` 的字符串，任意一次交换有 `C(n,2)=n·(n-1)/2` 种可能。  
- 如果不做任何剪枝，搜索树的宽度是 `O(n²)`，深度最坏情况下是 `O(n)`（因为每次最多只能把一个位置纠正），于是时间复杂度约为 `O((n²)^{n})`，也就是 **指数级**，对 `n≤20` 来说几乎不可接受。  
- BFS 需要把已经访问过的字符串放进集合里防止重复，最坏情况下要保存全部状态，空间也是 **指数级**。

#### 代码（Python）

```python
from collections import deque

def kSimilarity_bruteforce(s1: str, s2: str) -> int:
    """暴力 BFS 求最小交换次数（仅作概念演示，实际会超时）"""
    if s1 == s2:
        return 0

    n = len(s1)
    # visited 用哈希表（字典）保存已经遍历过的字符串，类似查字典：key 是字符串，value 随便
    visited = {s1}
    q = deque([(s1, 0)])               # (当前字符串, 已经用了几次交换)

    while q:
        cur, step = q.popleft()
        # 产生所有可能的下一个状态
        cur_list = list(cur)
        for i in range(n):
            for j in range(i + 1, n):
                # 交换 i、j 位
                cur_list[i], cur_list[j] = cur_list[j], cur_list[i]
                nxt = ''.join(cur_list)
                if nxt == s2:          # 第一次碰到目标，就是最少步数
                    return step + 1
                if nxt not in visited:
                    visited.add(nxt)
                    q.append((nxt, step + 1))
                # 恢复原样，准备尝试下一个 (i, j)
                cur_list[i], cur_list[j] = cur_list[j], cur_list[i]

    return -1   # 题目保证一定能到达，这行理论上不会执行
```

#### 复杂度

- **时间复杂度**：`O((n²)^{n})`（指数级）  
  > 解释：每层最多有 `n·(n-1)/2 ≈ n²` 个分支，深度最坏是 `n`，于是时间呈指数增长。
- **空间复杂度**：`O((n²)^{n})`（指数级）  
  > 需要把所有已经遍历的字符串存下来，最坏情况下数量和时间一样多。

---

### 2. 最优解

#### 思路  

暴力解的“慢”点在于 **盲目枚举所有可能的交换**，很多分支根本不可能帮助我们更快地纠正错误位置。  
关键观察：

1. **只关注不匹配的位置**。如果 `cur[i] == target[i]`，这个位置已经正确了，后面再去换它只会把正确的字符弄坏，显然不是最优的做法。  
2. **每一步尽量让一个位置立刻对齐**。设 `i` 是当前字符串中最左侧的错误位置（`cur[i] != target[i]`），我们只尝试把 `cur[i]` 与那些能够把 `i` 位置纠正的字符交换——也就是在后面位置 `j>i` 且 `cur[j] == target[i]` 的字符。这样一次交换一定能让 `i` 正确，搜索树的分支数从 `O(n²)` 降到 **“错误字符的个数”**，大幅度削减。

基于上述两点，我们仍然使用 BFS（因为层序遍历天然给出最少步数），但 **每个状态只生成有限、且更有价值的子状态**。实现细节：

- 用 `deque` 维护 BFS 队列，`visited` 防止重复。
- 对每个弹出的字符串 `cur`，先找出最左侧的错误索引 `i`。
- 遍历 `j`（`i+1 … n-1`），如果 `cur[j] == target[i]` 且 `cur[j] != target[j]`（换掉的字符本身也是错的），则交换 `i`、`j`，得到新字符串 `nxt`，加入队列。
- 只要找到 `target`，返回当前层数 + 1。

> **类比**：想象你在整理一排错位的书。你总是先把最左边那本错误的书换到正确的位置——因为只要把这本书放好，左边以后再也不会出现错误。这样每一步都在“修正最左边的错误”，效率自然更高。

**为什么仍然正确**  
我们仍然遍历了所有 **合法** 的最优路径：任意最优解的第一步必然是把最左侧错误位置换成正确字符（否则该位置在后面才会被纠正，步数不可能更少），所以我们没有遗漏最优解。

**复杂度提升**  
- 分支数从 `O(n²)` 降到 `O(m)`，其中 `m` 是当前错误字符的数量（最多 `n`）。  
- 实际上对 `n≤20` 的约束，这种剪枝可以让 BFS 在几千到几万步内结束，完全可接受。

#### 代码（Python）

```python
from collections import deque

def kSimilarity(s1: str, s2: str) -> int:
    """BFS + 只交换最左侧错误位的优化版本，能在 20 长度内 AC"""
    if s1 == s2:
        return 0

    n = len(s1)
    target = s2
    visited = {s1}
    q = deque([(s1, 0)])   # (当前字符串, 已使用的交换次数)

    while q:
        cur, step = q.popleft()
        # 1️⃣ 找到最左侧仍然不匹配的位置 i
        i = 0
        while i < n and cur[i] == target[i]:
            i += 1
        if i == n:                     # 已经全部匹配（理论上不会进入这里，因为会在前一步返回）
            return step

        cur_list = list(cur)
        # 2️⃣ 只尝试把 i 位换成 target[i] 所在的错误位置 j
        for j in range(i + 1, n):
            # 只有当 cur[j] 正好是我们想要放到 i 位置的字符，且 j 位置本身也不对的时候才交换
            if cur_list[j] == target[i] and cur_list[j] != target[j]:
                # 交换 i、j
                cur_list[i], cur_list[j] = cur_list[j], cur_list[i]
                nxt = ''.join(cur_list)
                if nxt == target:
                    return step + 1          # 第一次到达目标，步数最少
                if nxt not in visited:
                    visited.add(nxt)
                    q.append((nxt, step + 1))
                # 恢复原样，准备尝试下一个 j
                cur_list[i], cur_list[j] = cur_list[j], cur_list[i]

    return -1   # 题目保证一定能到达
```

#### 复杂度

- **时间复杂度**：`O(b^d)`，其中  
  - `d` 是答案的最小交换次数（最多 `n`），  
  - `b` 是每层的分支数，**最坏约为错误字符的数量 ≤ n**。  
  在实际测试中，`b` 远小于 `n²`，所以整体表现接近 `O(n·b^d)`，对 `n≤20` 完全可以在毫秒级跑完。  
  > 大白话：每一步只换“能立刻把左边错误改正的字符”，所以搜索树非常瘦，几乎不需要遍历所有可能的交换。

- **空间复杂度**：`O(b^d)`（队列 + visited 集合），同样因为 `b` 很小，最多只会存几千到几万条状态，远低于指数级的暴力解。

---

## 心得

- **核心技巧**：在 BFS 中**只对最左侧错误位置进行有针对性的交换**（即“修正最左错误”），极大地削减分支。
- **适用的题型**  
  1. 需要最少操作次数且每次操作是“在字符串/数组上交换两个元素”的问题（如 *Minimum Swaps to Make Strings Equal*）。  
  2. 需要把一个排列变成另一个排列的最少交换次数（如 *K-Similar Strings*、*Shortest Sequence of Swaps*）。  
  3. 需要在状态空间搜索且可以利用**“只处理当前最迫切错误”**的启发式剪枝的题目（如某些排列游戏、拼图类问题）。
- **一句话总结解题钥匙**：*“每一步都让左边的错误立刻消失”，这样 BFS 只走最有价值的路，答案自然最短。*

---

## 反思

- **第一反应**：看到 “swap 两个字符” 立刻想到 **全排列 + BFS**，于是写出最笨的暴力搜索。  
- **最容易踩的坑**  
  - **重复状态**：不使用 `visited` 会导致指数级爆炸。  
  - **无意义的交换**：随意交换已经正确的位置会把正确的字符弄坏，导致搜索树膨胀。  
  - **边界情况**：当 `s1 == s2` 时应直接返回 `0`，否则会多走一步。  
  - **字符相同的冗余交换**：如果 `cur[j] == target[i]` 但 `cur[j]` 已经在正确位置（`cur[j] == target[j]`），交换后会把已正确的字符弄错，应该跳过。  
- **下次遇到同类题**：  
  1. 先定位**最左/最上**的错误位置。  
  2. 只尝试能**立刻纠正该错误**的操作（如交换成目标字符）。  
  3. 再决定用 BFS 还是双向 BFS、A* 等搜索策略。这样往往能把指数级问题压到可接受范围。