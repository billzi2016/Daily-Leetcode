# #839. 相似字符串分组 / Similar String Groups

> 难度：困难 · 标签：Array、Hash Table、String、Depth-First Search、Breadth-First Search、Union Find · [LeetCode 链接](https://leetcode.com/problems/similar-string-groups/)

---

## 题目（英文原版）

**Description**

Two strings, X and Y, are considered similar if either they are identical or we can make them equivalent by swapping at most two letters (in distinct positions) within the string X.
For example, "tars" and "rats" are similar (swapping at positions 0 and 2), and "rats" and "arts" are similar, but "star" is not similar to "tars", "rats", or "arts".
Together, these form two connected groups by similarity: {"tars", "rats", "arts"} and {"star"}.  Notice that "tars" and "arts" are in the same group even though they are not similar.  Formally, each group is such that a word is in the group if and only if it is similar to at least one other word in the group.
We are given a list strs of strings where every string in strs is an anagram of every other string in strs. How many groups are there?

**Examples**

**Example 1:**

```
Input: strs = ["tars","rats","arts","star"]
Output: 2
```

**Example 2:**

```
Input: strs = ["omv","ovm"]
Output: 1
```

**Constraints**

- 1 <= strs.length <= 300
- 1 <= strs[i].length <= 300
- strs[i] consists of lowercase letters only.
- All words in strs have the same length and are anagrams of each other.

---

## 题目（中文翻译）

**题目描述**  
如果两个字符串 **X** 和 **Y** 满足以下任意一种情况，则称它们相似（similar）：

1. 两者完全相同；  
2. 通过在 **X** 中至多交换两次字母（交换位置必须不同）即可得到 **Y**。

例如，"tars" 与 "rats" 相似（交换位置 0 和 2 的字符），"rats" 与 "arts" 也相似，但 "star" 与 "tars"、"rats"、"arts" 都不相似。

相似关系会形成若干连通分量（connected groups），即每个分组满足：分组内的任意单词，只要它与分组中 **至少一个** 其他单词相似，就属于该分组。注意，两个单词即使不直接相似，只要它们之间存在一条相似链，它们也会出现在同一个分组中。例如，"tars" 与 "arts" 虽然不直接相似，但因为都与 "rats" 相似，故同属一个分组。

给定字符串数组 `strs`，已知 `strs` 中的所有字符串都是彼此的字母异位词（anagram），请返回相似字符串的分组数。

**示例**

> 示例 1  
> 输入: `strs = ["tars","rats","arts","star"]`  
> 输出: `2`  

> 示例 2  
> 输入: `strs = ["omv","ovm"]`  
> 输出: `1`  

**约束条件**

- `1 <= strs.length <= 300`
- `1 <= strs[i].length <= 300`
- `strs[i]` 只包含小写字母。
- 所有字符串长度相同，且互为字母异位词（anagram）。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

1. **相似的定义**  
   两个等长字符串 `X`、`Y` 相似当且仅当  
   - 它们完全相同，或  
   - 只需要在 `X` 中交换 **恰好两** 个不同位置的字符，就能得到 `Y`。  
   换句话说，比较 `X`、`Y` 时，出现 **不相同的字符位置** 最多只能有 **2 个**，并且这两个位置的字符互相对应（即 `X[i]=Y[j]` 且 `X[j]=Y[i]`）。

2. **把所有字符串看成图的节点**  
   - 每个字符串是一个点。  
   - 如果两点对应的字符串相似，就连一条无向边。  
   - 题目要求的是 **连通分量的数量**（相似的点能相互走到，就是同一个组）。

3. **暴力构图**  
   - 对每一对字符串 `i < j`，检查它们是否相似（只要遍历一次字符，记录不相同的位置）。  
   - 如果相似，就把它们连在一起。  
   - 最后用 **DFS / BFS** 在这张图上遍历，统计连通分量数目。

4. **为什么一定对**  
   - 只要两字符串相似，就在图里连边；相似是 **可传递** 的（如果 `a~b` 且 `b~c`，则 `a`、`c` 在同一个连通分量）。  
   - 统计连通分量正好对应题目要求的“相似分组”。

5. **复杂度直观解释**  
   - `N = len(strs)`，`L = len(strs[0])`。  
   - 检查一对字符串相似需要遍历 `L` 个字符 → `O(L)`。  
   - 共有 `N*(N-1)/2 ≈ N²/2` 对，需要 `O(N²·L)` 次字符比较。  
   - 再做一次 DFS/BFS 只遍历 `N` 个点和已建好的边，时间几乎可以忽略。  
   - 空间上我们需要保存图的邻接表，最坏情况每对都相似，边数 `≈ N²`，即 `O(N²)`。

#### 代码（Python）

```python
from collections import defaultdict, deque
from typing import List

def are_similar(a: str, b: str) -> bool:
    """判断两个等长字符串是否相似（最多两处不同且互换对应）"""
    diff = []                     # 记录不同字符的位置
    for i, (ca, cb) in enumerate(zip(a, b)):
        if ca != cb:
            diff.append(i)
            if len(diff) > 2:    # 超过两处不同直接返回 False
                return False
    # 两种合法情况：全相同（diff 为空）或恰好两处且交叉相等
    return len(diff) == 0 or (len(diff) == 2 and
                              a[diff[0]] == b[diff[1]] and
                              a[diff[1]] == b[diff[0]])

def num_similar_groups_bruteforce(strs: List[str]) -> int:
    n = len(strs)
    # 1️⃣ 建图：邻接表
    graph = defaultdict(list)     # key: 节点编号，value: 相邻节点列表
    for i in range(n):
        for j in range(i + 1, n):
            if are_similar(strs[i], strs[j]):
                graph[i].append(j)
                graph[j].append(i)

    # 2️⃣ BFS/DFS 统计连通分量
    visited = [False] * n
    groups = 0

    for i in range(n):
        if not visited[i]:
            groups += 1               # 发现一个新组
            # 用 BFS 把同组的所有点都标记为已访问
            q = deque([i])
            visited[i] = True
            while q:
                cur = q.popleft()
                for nb in graph[cur]:
                    if not visited[nb]:
                        visited[nb] = True
                        q.append(nb)
    return groups
```

#### 复杂度  

- **时间复杂度**：`O(N²·L)`  
  - “N²” 表示我们要比较每一对字符串；“L” 是每次比较要遍历的字符数。  
  - 对于本题的最大数据量 `N ≤ 300, L ≤ 300`，约 `27 000 000` 次字符比较，仍在可接受范围。

- **空间复杂度**：`O(N²)`（最坏情况的邻接表）  
  - 如果每对字符串都相似，图里会有 `N(N-1)/2` 条边，需要存储这些边。  
  - 额外的 `visited` 数组只占 `O(N)`，相比之下可以忽略。

---

### 2. 最优解  

#### 思路  

暴力解的时间瓶颈在于 **全对比**：我们把所有 `N²/2` 对都检查一遍。  
实际上，**相似的字符串之间的差距非常小**（最多两个字符位置不同），这让我们可以采用 **并查集（Union‑Find）** 直接把相似的点合并，而不必显式保存完整的邻接表。  

**关键点**  

1. **并查集的作用**  
   - 把每个字符串看成一个集合的“代表”。  
   - 当发现两字符串相似时，把它们所在的集合合并（`union`）。  
   - 最终，不同集合的根（`find` 的返回值）数量就是相似分组的数量。  

2. **为什么还能省掉“全对比”**  
   - `N ≤ 300`，全对比已经够快，但我们仍然可以**提前剪枝**：  
     - 若两个字符串已经在同一个集合里，就不必再检查相似性（避免重复工作）。  
   - 这一步把 **最坏情况** 的时间仍保持在 `O(N²·L)`，但常数更小，代码更简洁。  

3. **并查集的实现**  
   - `parent[i]` 保存节点 `i` 的父节点，初始时每个节点是自己的父节点。  
   - `find(x)` 用路径压缩，使后续查询更快。  
   - `union(x, y)` 把两根合并，常用按秩（rank）或大小（size）优化。  

4. **整体流程**  

   ```
   for i in range(N):
       for j in range(i+1, N):
           if find(i) != find(j):          # 只在不同集合时才检查
               if are_similar(strs[i], strs[j]):
                   union(i, j)
   answer = number of distinct roots
   ```

5. **复杂度解释**  

   - **相似性检查** 仍是 `O(L)`，最多检查 `N(N-1)/2` 对 → `O(N²·L)`。  
   - **并查集操作**（`find`、`union`）几乎是 `O(α(N))`，α 为反 Ackermann 函数，几乎可以看作常数。  
   - 所以整体时间仍是 `O(N²·L)`，但空间只需要 `O(N)`（父指针数组），比邻接表省了 `O(N²)`。

#### 代码（Python）

```python
from typing import List

def are_similar(a: str, b: str) -> bool:
    """两字符串相似判定（最多两处不同且互换对应）"""
    diff = []
    for ca, cb in zip(a, b):
        if ca != cb:
            diff.append((ca, cb))
            if len(diff) > 2:        # 超过两处不同直接否定
                return False
    # diff 长度为 0（完全相同）或 2 且交叉相等
    return len(diff) == 0 or (len(diff) == 2 and
                              diff[0][0] == diff[1][1] and
                              diff[0][1] == diff[1][0])

class UnionFind:
    """并查集实现，带路径压缩和按秩合并"""
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank   = [0] * n          # 用于按秩合并

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])   # 路径压缩
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return
        # 按秩合并：高度低的挂到高度高的下面
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1

def num_similar_groups_unionfind(strs: List[str]) -> int:
    n = len(strs)
    uf = UnionFind(n)

    for i in range(n):
        for j in range(i + 1, n):
            # 只在不同集合时才进行相似性检查，避免无谓的比较
            if uf.find(i) != uf.find(j) and are_similar(strs[i], strs[j]):
                uf.union(i, j)

    # 统计不同根的数量，即为组数
    roots = {uf.find(i) for i in range(n)}
    return len(roots)
```

#### 复杂度  

- **时间复杂度**：`O(N²·L)`  
  - 与暴力解的时间量级相同，但 **并查集的 `find/union` 只占常数时间**，且我们在同集合内部会直接跳过相似性检查，实际运行更快。  

- **空间复杂度**：`O(N)`  
  - 只需要 `parent`、`rank` 两个长度为 `N` 的数组，省去了存图的 `O(N²)` 空间。  

---

## 心得  

- **核心技巧**：把“相似关系”抽象成图的连通性，然后使用 **并查集（Union‑Find）** 高效合并同一组的元素。  
- **适用的题型**  
  1. “相似字符串/单词分组” 类（本题、LeetCode 839 “Similar String Groups”）。  
  2. “好友关系、岛屿合并” 类（LeetCode 200 “Number of Islands”，LeetCode 547 “Friend Circles”）。  
  3. “等价关系” 的判定，如 “等价字符对” 之类的问题。  

- **一句话总结解题钥匙**：**把“相似”视作“可以连通的边”，用并查集把所有可达的节点合并，根的数量就是答案**。

---

## 反思  

- **第一反应**：直接把所有字符串两两比较，构图后做 DFS/BFS。  
- **最容易踩的坑**  
  - **相似判定**写错：必须确保只允许 **恰好两处不同且互换对应**，否则会把不相似的字符串误判进同一组。  
  - **重复合并**：若不检查 `find(i) != find(j)` 就直接比较，会导致大量不必要的相似性检查，尤其在 `N` 较大时会拖慢速度。  
  - **边界条件**：长度为 1 的字符串只有一种形式，所有字符串必然相同，答案为 1。  
- **下次遇到同类题**：  
  1. 先思考 “相似 / 等价” 能否抽象成 **图的连通分量**。  
  2. 再决定是 **显式建图 + DFS/BFS** 还是 **并查集**（一般并查集更省空间，代码更简洁）。  
  3. 最后仔细实现 **相似判定**，确保只在合法的 “最多两次交换” 条件下返回 `True`。