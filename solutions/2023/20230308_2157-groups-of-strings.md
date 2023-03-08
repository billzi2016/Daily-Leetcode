# #2157. **字符串分组** / Groups of Strings

> 难度：困难 · 标签：String、Bit Manipulation、Union Find · [LeetCode 链接](https://leetcode.com/problems/groups-of-strings/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array of strings words. Each string consists of lowercase English letters only. No letter occurs more than once in any string of words.
Two strings s1 and s2 are said to be connected if the set of letters of s2 can be obtained from the set of letters of s1 by any one of the following operations:
The array words can be divided into one or more non-intersecting groups. A string belongs to a group if any one of the following is true:
Note that the strings in words should be grouped in such a manner that a string belonging to a group cannot be connected to a string present in any other group. It can be proved that such an arrangement is always unique.
Return an array ans of size 2 where:

**Examples**

**Example 1:**

```
Input: words = ["a","b","ab","cde"]
Output: [2,3]
Explanation:
- words[0] can be used to obtain words[1] (by replacing 'a' with 'b'), and words[2] (by adding 'b'). So words[0] is connected to words[1] and words[2].
- words[1] can be used to obtain words[0] (by replacing 'b' with 'a'), and words[2] (by adding 'a'). So words[1] is connected to words[0] and words[2].
- words[2] can be used to obtain words[0] (by deleting 'b'), and words[1] (by deleting 'a'). So words[2] is connected to words[0] and words[1].
- words[3] is not connected to any string in words.
Thus, words can be divided into 2 groups ["a","b","ab"] and ["cde"]. The size of the largest group is 3.
```

**Example 2:**

```
Input: words = ["a","ab","abc"]
Output: [1,3]
Explanation:
- words[0] is connected to words[1].
- words[1] is connected to words[0] and words[2].
- words[2] is connected to words[1].
Since all strings are connected to each other, they should be grouped together.
Thus, the size of the largest group is 3.
```

**Constraints**

- 1 <= words.length <= 2 * 104
- 1 <= words[i].length <= 26
- words[i] consists of lowercase English letters only.
- No letter occurs more than once in words[i].

---

## 题目（中文翻译）

给定一个下标从 0 开始的字符串数组 `words`。每个字符串仅由小写英文字母组成，且同一字符串中不存在重复字母。

如果可以通过以下任意一种操作，使得字符串 `s2` 的字母集合由字符串 `s1` 的字母集合得到，则称 `s1` 与 `s2` **相连**（connected）：

- **添加**（add）：在 `s1` 的字母集合中加入一个新字母得到 `s2`；
- **删除**（delete）：从 `s1` 的字母集合中去掉一个字母得到 `s2`；
- **替换**（replace）：先从 `s1` 的字母集合中删除一个字母，再加入另一个不同的字母得到 `s2`。

`words` 可以被划分为一个或多个互不相交的 **组**（group）。若满足以下任意条件，则一个字符串属于同一组：

- 它与组内的其他字符串直接相连；
- 它可以通过若干条相连的链路（每条链路均满足上述任一操作）间接相连到组内的其他字符串。

需要保证不同组之间的任意两字符串都不相连。可以证明，这样的划分唯一。

返回一个大小为 2 的整数数组 `ans`，其中  

- `ans[0]` 为组的数量，  
- `ans[1]` 为最大组的大小。

---

### 示例

**示例 1**

```json
Input: words = ["a","b","ab","cde"]
Output: [2,3]
Explanation:
- words[0] 可以通过**替换**'a' 为 'b' 得到 words[1]，也可以通过**添加**'b' 得到 words[2]，因此 words[0] 与 words[1]、words[2] 相连。
- words[1] 可以通过**替换**'b' 为 'a' 得到 words[0]，也可以通过**添加**'a' 得到 words[2]，因此 words[1] 与 words[0]、words[2] 相连。
- words[2] 可以通过**删除**'b' 得到 words[0]，也可以通过**删除**'a' 得到 words[1]，因此它与前两者相连。
- words[3] 与其他任何字符串都不相连。

于是形成两个组：`["a","b","ab"]`（大小为 3）和 `["cde"]`（大小为 1），返回 `[2,3]`。

**示例 2**

```json
Input: words = ["a","ab","abc"]
Output: [1,3]
Explanation:
- words[0] 与 words[1] 相连（通过添加 'b'）。
- words[1] 与 words[0]、words[2] 相连（分别通过删除 'b'、添加 'c'）。
- words[2] 与 words[1] 相连（通过删除 'c'）。

所有字符串互相连通，只有一个组，大小为 3，返回 `[1,3]`。

---

### 约束条件

- `1 <= words.length <= 2 * 10^4`
- `1 <= words[i].length <= 26`
- `words[i]` 仅由小写英文字母组成
- 同一字符串中不存在重复字母

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每个字符串看成图中的一个节点，如果两个字符串 **满足“相连”**（即只需要一次「添加 / 删除 / 替换」操作就能相互得到），就在它们之间连一条无向边。  
于是问题就变成：

> 在这张无向图里，有多少个连通块（group）？最大的连通块有多少个节点？

> **数据结构类比**：  
> - **图** 好比城市之间的道路网络，城市 = 字符串，路 = 「相连」关系。  
> - **连通块** 就像互相能到达的城市集合，想象把每个块的城市全部涂成同一种颜色。

暴力实现的关键是 **判断两条字符串是否相连**。因为每条字符串长度至多 26（英文字母不重复），我们可以直接把它们的字符集合取出来，比较三种可能的变化：

1. **添加**：`len(s2) = len(s1) + 1` 且 `s1` 的字符集合是 `s2` 的子集。  
2. **删除**：`len(s2) = len(s1) - 1` 且 `s2` 的字符集合是 `s1` 的子集。  
3. **替换**：`len(s2) = len(s1)`，且两集合只相差 **恰好两个字符**（一个在 `s1` 里没有，在 `s2` 里有，反之亦然）。

只要满足其中一种，就在它们之间连边。

#### 代码（Python）

```python
from collections import defaultdict, deque
from typing import List

def are_connected(a: str, b: str) -> bool:
    """判断 a、b 是否只差一步（添加/删除/替换）"""
    set_a, set_b = set(a), set(b)
    if len(a) == len(b):
        # 替换：两集合相差恰好两个字符
        diff = set_a ^ set_b          # 对称差
        return len(diff) == 2
    elif len(a) + 1 == len(b):
        # a -> b 只需要添加一个字符
        return set_a.issubset(set_b)
    elif len(a) - 1 == len(b):
        # a -> b 只需要删除一个字符
        return set_b.issubset(set_a)
    return False

def groups_of_strings_bruteforce(words: List[str]) -> List[int]:
    n = len(words)
    # 建图（邻接表）
    graph = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if are_connected(words[i], words[j]):
                graph[i].append(j)
                graph[j].append(i)

    # BFS/DFS 统计连通块
    visited = [False] * n
    groups = 0
    max_size = 0
    for i in range(n):
        if not visited[i]:
            groups += 1
            q = deque([i])
            visited[i] = True
            size = 0
            while q:
                cur = q.popleft()
                size += 1
                for nb in graph[cur]:
                    if not visited[nb]:
                        visited[nb] = True
                        q.append(nb)
            max_size = max(max_size, size)
    return [groups, max_size]
```

#### 复杂度  

- **时间复杂度**：`O(n² * L)`  
  - `n` 为单词数量（最多 2·10⁴），`L ≤ 26` 为单词长度。  
  - 暴力要两两比较（`n²/2` 次），每次比较需要把字符转集合并做几次集合运算，成本与 `L` 成正比。  
  - 用“大白话”说，就是“如果有 10 000 条线索，要两两检查，那要检查几千万次”，所以在最坏情况下会超时。

- **空间复杂度**：`O(n + E)`  
  - `E` 为图中实际的边数，最坏情况下几乎是 `n²`，因此空间也会很大。  
  - 另外还有 `visited`、`queue` 等额外 O(n) 辅助空间。

---

### 2. 最优解

#### 思路  

暴力解慢的根源在 **“两两比较”**。我们需要一种方式，**只遍历每个单词一次**，就能把所有可能相连的单词找出来。

**关键观察**：

- 每个单词只含 **不重复的 26 个小写字母**，可以用 **26 位二进制掩码** 完全表示。  
  - 例如 `"ac"` → `0010…001`（第 0 位对应 `'a'`，第 2 位对应 `'c'`）。  
  - **掩码就像字典的页码**：把字母集合映射成唯一的整数，查询时只要看这个整数是否出现过。

- 对于一个掩码 `mask`，**一次合法操作能得到的所有可能掩码** 只有几百种（而不是 `n` 种）：

  1. **添加**：把任意一个缺失的字母位设为 1。  
     - `mask | (1 << k)`（`k` 为缺失字母的下标），最多 26 种。

  2. **删除**：把任意一个已有的字母位清 0。  
     - `mask ^ (1 << k)`（`k` 为已有字母的下标），最多 26 种。

  3. **替换**：先删掉一个已有字母，再加上一个缺失字母。  
     - `mask ^ (1 << i) | (1 << j)`，其中 `i` 是已有字母，`j` 是缺失字母。  
     - 组合数为 `|mask| * (26 - |mask|)`，最坏约 `13 * 13 = 169`（因为长度最多 26）。

  因此 **每个单词只会产生 O(26²) ≈ 676 条“候选”掩码**，这远小于 `n`。

- 把 **相同掩码的单词视为同一个节点**（它们本身已经相连），我们只需要 **把不同掩码之间的连通关系合并**。  
  这正是 **并查集（Union‑Find）** 的用武之地：每次发现两个掩码应该在同一组时，就把它们的根合并。

**整体步骤**：

1. **把每个单词转成掩码**，并记录 `mask → 第一个出现的下标`（用于并查集的初始化）。  
2. 初始化并查集 `parent`、`size`（每个根的组大小）。  
3. 对每个单词的掩码 `mask`，遍历上面列出的所有**候选掩码** `cand`。  
   - 如果 `cand` 在映射表中出现过，则把当前下标 `i` 与 `cand` 对应的下标 `j` 合并。  
4. 最后遍历所有根，统计 **连通块的数量**（不同根的个数）以及 **最大的组大小**（`size[root]` 的最大值）。

**类比解释**：

- **掩码** → **字典的页码**，每本书（单词）都有唯一的页码。  
- **候选掩码** → **把页码上的一页改成别的页码**（加/删/换），只有几百种可能的改动。  
- **并查集** → **把可以互相到达的书堆放在同一个书架**，每次发现两本书可以直接搬到同一个书架，就把它们的书架合并。

#### 代码（Python）

```python
from typing import List

class UnionFind:
    """并查集实现，带路径压缩和按大小合并"""
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.sz = [1] * n          # 每个根的组大小

    def find(self, x: int) -> int:
        # 递归写法，路径压缩：把访问过的节点直接挂到根上
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        # 按大小合并，小根挂到大根下面
        if self.sz[ra] < self.sz[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.sz[ra] += self.sz[rb]

def groups_of_strings(words: List[str]) -> List[int]:
    n = len(words)
    masks = []
    mask_to_index = {}            # 第一次出现的下标，后面统一用它做 union

    # 1️⃣ 把每个单词转成 26 位掩码
    for idx, w in enumerate(words):
        mask = 0
        for ch in w:
            mask |= 1 << (ord(ch) - ord('a'))
        masks.append(mask)
        # 同一个掩码的单词天然相连，只保留第一个下标
        if mask not in mask_to_index:
            mask_to_index[mask] = idx

    uf = UnionFind(n)

    # 2️⃣ 对每个单词的掩码，枚举所有一次操作能得到的候选掩码
    for i, mask in enumerate(masks):
        # a. 添加一个缺失的字母
        for b in range(26):
            if not (mask >> b) & 1:                # b 号位当前是 0 → 缺失
                cand = mask | (1 << b)            # 加上它
                if cand in mask_to_index:
                    uf.union(i, mask_to_index[cand])

        # b. 删除一个已有的字母
        for b in range(26):
            if (mask >> b) & 1:                    # b 号位是 1 → 有这个字母
                cand = mask ^ (1 << b)            # 把它清掉
                if cand in mask_to_index:
                    uf.union(i, mask_to_index[cand])

        # c. 替换：删掉一个已有字母，再加上一个缺失字母
        for del_b in range(26):
            if not (mask >> del_b) & 1:
                continue                          # 只能删已有的
            mask_without = mask ^ (1 << del_b)   # 先删
            for add_b in range(26):
                if (mask_without >> add_b) & 1:
                    continue                      # 只能加缺失的
                cand = mask_without | (1 << add_b)
                if cand in mask_to_index:
                    uf.union(i, mask_to_index[cand])

    # 3️⃣ 统计连通块数量和最大块大小
    root_set = set()
    max_group = 0
    for i in range(n):
        r = uf.find(i)
        root_set.add(r)
        max_group = max(max_group, uf.sz[r])

    return [len(root_set), max_group]
```

> **代码要点说明**  
> 1. `mask |= 1 << (ord(ch)-ord('a'))` 把字符对应的位设为 1，形成唯一的二进制标识。  
> 2. `mask_to_index` 只保存第一次出现的下标，因为同掩码的单词已经在同一组，后面只需要把其它掩码指向这个代表即可。  
> 3. 并查集的 `sz` 数组在 `union` 时同步更新，这样最后只要看根的 `sz` 就能得到每个组的大小。  
> 4. 替换操作的双层循环在最坏情况下是 `|mask| * (26 - |mask|) ≤ 13 * 13 = 169`，属于常数级别。

#### 复杂度  

- **时间复杂度**：`O(n * 26²)` ≈ `O(n)`  
  - 对每个单词，我们最多枚举 `26（添加） + 26（删除） + 169（替换） ≈ 221` 种候选掩码。  
  - 每次检查哈希表 `cand in mask_to_index` 是 O(1) 平均时间。  
  - 因此整体随 `n` 线性增长，能轻松处理 2·10⁴ 条记录。

- **空间复杂度**：`O(n)`  
  - `masks`、`mask_to_index`、并查集的 `parent`、`sz` 都是长度为 `n` 的数组。  
  - 只用了常数级别的额外空间（几个 26 位的整数），远小于暴力解的 `O(n²)` 边表。

---

## 心得

- **核心技巧**：**位掩码 + 并查集**。  
  - 位掩码把「字符集合」压缩成整数，极大降低了「相连」判定的搜索空间。  
  - 并查集高效管理「同属一组」的关系，只需要几次 `union`/`find` 就能得到连通块信息。

- **该技巧适用的题型**  
  1. **字符串/集合的相似度判定**（如 LeetCode 839 “Similar String Groups”）  
  2. **字母/数字的子集/超集关系**（如 LeetCode 1261 “Find Elements in a Contaminated Binary Tree” 中的位运算变形）  
  3. **需要快速合并集合的图论问题**（如「岛屿的数量」类问题配合 DSU）

- **一句话总结**：  
  *把每个单词压成 26 位的“指纹”，用指纹的有限邻域直接在并查集中合并，就是最快的分组方法。*

---

## 反思

- **第一反应**：看到“可以添加、删除、替换一个字符”，自然想到**图的连通块**，于是先写了两两比较的暴力实现。  
- **最容易踩的坑**  
  1. **字符不重复**：题目保证每个单词内部字母不重复，否则位掩码会失效。  
  2. **边界情况**：长度为 1 或 26 的单词，添加/删除/替换的候选集合要做好「不存在的位」过滤。  
  3. **同一掩码的多条单词**：必须在并查集里先把它们视为同一组，否则会重复计数。  
- **下次遇到同类题**：第一步先思考 **“能否把对象映射成整数/位掩码”**，再利用 **有限的邻域枚举 + DSU** 把相邻的对象快速合并。这样既避免 O(n²) 的全量比较，又能保证代码简洁易懂。