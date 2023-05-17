# #2246. 不同相邻字符的最长路径 / Longest Path With Different Adjacent Characters

> 难度：困难 · 标签：Array、String、Tree、Depth-First Search、Graph、Topological Sort · [LeetCode 链接](https://leetcode.com/problems/longest-path-with-different-adjacent-characters/)

---

## 题目（英文原版）

**Description**

You are given a tree (i.e. a connected, undirected graph that has no cycles) rooted at node 0 consisting of n nodes numbered from 0 to n - 1. The tree is represented by a 0-indexed array parent of size n, where parent[i] is the parent of node i. Since node 0 is the root, parent[0] == -1.
You are also given a string s of length n, where s[i] is the character assigned to node i.
Return the length of the longest path in the tree such that no pair of adjacent nodes on the path have the same character assigned to them.

**Examples**

**Example 1:**

```
Input: parent = [-1,0,0,1,1,2], s = "abacbe"
Output: 3
Explanation: The longest path where each two adjacent nodes have different characters in the tree is the path: 0 -> 1 -> 3. The length of this path is 3, so 3 is returned.
It can be proven that there is no longer path that satisfies the conditions.
```

**Example 2:**

```
Input: parent = [-1,0,0,0], s = "aabc"
Output: 3
Explanation: The longest path where each two adjacent nodes have different characters is the path: 2 -> 0 -> 3. The length of this path is 3, so 3 is returned.
```

**Constraints**

- n == parent.length == s.length
- 1 <= n <= 105
- 0 <= parent[i] <= n - 1 for all i >= 1
- parent[0] == -1
- parent represents a valid tree.
- s consists of only lowercase English letters.

---

## 题目（中文翻译）

**题目描述**  
给定一棵以节点 0 为根的树（即一棵连通的、无环的无向图），共有 `n` 个节点，编号为 `0` 到 `n - 1`。树使用大小为 `n` 的 0 索引数组 `parent` 表示，其中 `parent[i]` 是节点 `i` 的父节点。由于节点 0 为根，`parent[0] == -1`。  
同时给定一个长度为 `n` 的字符串 `s`，其中 `s[i]` 是分配给节点 `i` 的字符。  
返回树中满足「路径上任意相邻节点的字符都不相同」的最长路径的长度。

**示例 1**  
``` 
Input: parent = [-1,0,0,1,1,2], s = "abacbe"
Output: 3
Explanation: 树中满足相邻节点字符均不同的最长路径是 0 -> 1 -> 3。该路径长度为 3，故返回 3。
可以证明不存在更长的满足条件的路径。
```

**示例 2**  
``` 
Input: parent = [-1,0,0,0], s = "aabc"
Output: 3
Explanation: 满足相邻节点字符均不同的最长路径是 2 -> 0 -> 3。该路径长度为 3，故返回 3。
```

**约束条件**  

- `n == parent.length == s.length`
- `1 <= n <= 10^5`
- 对所有 `i >= 1`，`0 <= parent[i] <= n - 1`
- `parent[0] == -1`
- `parent` 构成一棵合法的树
- `s` 仅由小写英文字母组成

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把“所有可能的路径”都枚举一遍，然后检查每条路径上相邻节点的字符是否不同，符合条件的就记录它的长度，最后取最大值。  
- **枚举路径**：在一棵树里，任意两点之间唯一唯一一条唯一的简单路径（不走回头）。于是我们可以把 **所有节点对 (i, j)** 当作路径的端点，利用 BFS/DFS 找出它们之间的路径。  
- **检查字符**：得到路径后，顺序遍历路径上的节点，比较相邻两个字符是否相同。如果有相同的，就把这条路径抛弃。  
- **记录最大长度**：把所有满足条件的路径长度取最大，即为答案。  

> **类比**：把树想象成一座城市的道路网，父子关系就像道路的指向。我们要做的就是把每两座建筑之间的所有可能路线都走一遍，就像旅游攻略里“从 A 城到 B 城的所有路线”。  

这种做法一定能得到正确答案，因为我们没有漏掉任何一条合法路径。唯一的缺点是 **效率太低**：  
- 对每一对节点 (i, j) 都要跑一次 BFS/DFS，时间是 **O(n²)**（n 为节点数）。  
- 同时需要存储路径，空间也会达到 **O(n)**（递归栈或队列），但这不是主要瓶颈。  

**为什么 O(n²) 看起来很大？**  
如果 n = 10⁵，n² 就是 10⁹，意味着要进行十亿次遍历，远远超出一秒能完成的计算量（一般 10⁸ 次左右是极限），所以会超时。

#### 代码（Python）  

```python
from collections import deque
from typing import List

def longestPath_bruteforce(parent: List[int], s: str) -> int:
    n = len(parent)
    # 1️⃣ 根据 parent 数组建邻接表（无向图）
    g = [[] for _ in range(n)]
    for i in range(1, n):
        p = parent[i]
        g[p].append(i)
        g[i].append(p)

    # 2️⃣ 求两点之间的路径（BFS 找父节点数组）
    def bfs_path(u: int, v: int) -> List[int]:
        # 记录每个节点的前驱，便于回溯出路径
        pre = [-1] * n
        q = deque([u])
        pre[u] = u
        while q:
            cur = q.popleft()
            if cur == v:
                break
            for nb in g[cur]:
                if pre[nb] == -1:
                    pre[nb] = cur
                    q.append(nb)
        # 回溯得到从 u 到 v 的路径
        path = []
        x = v
        while x != pre[x]:
            path.append(x)
            x = pre[x]
        path.append(u)
        path.reverse()
        return path

    ans = 1  # 至少包含根节点自身
    # 3️⃣ 枚举所有节点对
    for i in range(n):
        for j in range(i + 1, n):
            path = bfs_path(i, j)
            # 4️⃣ 检查相邻字符是否相同
            ok = True
            for k in range(1, len(path)):
                if s[path[k]] == s[path[k - 1]]:
                    ok = False
                    break
            if ok:
                ans = max(ans, len(path))
    return ans
```

> 代码说明：  
> - 第 1 步把父子关系转成 **无向邻接表**，这样可以从任意节点出发遍历。  
> - `bfs_path` 用 **广度优先搜索** 找到两点之间的唯一路径并返回。  
> - 主循环里两层 `for` 枚举所有节点对，时间复杂度正是 O(n²)。  

#### 复杂度  

- **时间复杂度**：`O(n² * (n + n)) ≈ O(n³)`，因为每对节点要跑一次 BFS，最坏情况下 BFS 需要遍历全部 `n` 条边。即使把 BFS 的复杂度记作 `O(n)`，整体仍是 **二次遍历** 的量级，远超题目限制。  
- **空间复杂度**：`O(n)`，用于存储邻接表和 BFS 时的 `pre` 数组。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈** 在于我们每次都从头遍历整棵树去找路径。实际上，树的结构让我们可以 **自底向上** 地聚合信息：  
- 对于每个节点，只需要知道 **从它向下延伸的最长合法链**（即不出现相同字符的最长向下路径长度）。  
- 当我们把子节点的这条最长链拼接到父节点时，只要父子字符不同，就可以把长度 +1 继续往上走。  

**核心概念——“向下最长合法链”**  
> 把每个节点想象成一根**伸向子树的棍子**，棍子的长度等于从该节点开始向下走、且相邻字符都不相同的最长路径长度（包括节点本身）。  

如果我们已经算出所有子节点的这条链的长度，那么在父节点处：
1. 只挑 **字符不同** 的子节点。  
2. 取出其中 **最长的两条**（因为最长路径可能经过父节点，分别来自左子树和右子树），把它们相加再加上父节点本身（+1），得到 **以父节点为“拐点”** 的最长路径长度。  
3. 同时，父节点向上的最长链只能取 **子节点中最长的那条**，再 +1。  

这样，只需要一次 **深度优先搜索（DFS）** 就能把所有信息收集完毕，时间线性 `O(n)`。  

**为什么只需要两条子链？**  
因为一条合法路径在树中最多只能经过一次父节点的“拐点”。如果我们把三条或更多子链都接在同一个父节点上，路径就会出现分叉，已不再是**简单路径**（路径不能回头或分叉），所以只需要最长的两条即可。  

**类比**：把树看成一座山脉，节点是山峰，向下的合法链是从山峰向下滑雪的最长滑道。我们想要找最长的滑道组合——要么是从某个山峰出发一直向下（向上返回的链），要么是两条滑道在同一个山峰汇合形成更长的路线。  

#### 代码（Python）  

```python
from typing import List
import sys
sys.setrecursionlimit(200000)   # 防止递归层数超过默认限制

def longestPath(parent: List[int], s: str) -> int:
    n = len(parent)
    # 1️⃣ 建立邻接表（子节点列表），因为是根树，只需要从父指向子
    children = [[] for _ in range(n)]
    for i in range(1, n):
        p = parent[i]
        children[p].append(i)

    ans = 1  # 全局答案，至少包含根节点自身

    # 2️⃣ 深度优先搜索，返回“从当前节点向下的最长合法链长度”
    def dfs(u: int) -> int:
        nonlocal ans
        # 记录当前节点的子链中最长的两条（初始为 0）
        max1, max2 = 0, 0

        # 遍历所有子节点
        for v in children[u]:
            child_len = dfs(v)                 # 子节点向下的最长链
            # 如果子节点字符和当前节点相同，不能接在一起
            if s[v] == s[u]:
                continue

            # 维护前两大长度
            if child_len > max1:
                max2 = max1
                max1 = child_len
            elif child_len > max2:
                max2 = child_len

        # 3️⃣ 以 u 为拐点的最长路径可能是：max1 + max2 + 1（自身）
        ans = max(ans, max1 + max2 + 1)

        # 4️⃣ 向上传递的只能是最长的那条 + 1（包括自身）
        return max1 + 1

    dfs(0)   # 从根节点 0 开始
    return ans
```

> 代码要点：  
> - 第 1 步把 `parent` 数组转成 **子节点列表**，这样 DFS 只向下遍历，避免重复访问。  
> - `dfs` 返回的是 **向下最长合法链**（包括当前节点本身）。  
> - `max1`、`max2` 用来保存子节点中 **前两大的合法链长度**，只在字符不同的情况下才考虑。  
> - `ans` 是全局变量，记录遍历过程中出现的 **最长路径长度**（可能不经过根节点）。  
> - 递归深度可能达到 `10⁵`，需要手动调大递归限制或改写为显式栈。  

#### 复杂度  

- **时间复杂度**：`O(n)`。每个节点只被访问一次，所有子链的比较、更新都是常数时间。相比暴力的 `O(n²)`，快了几个数量级。  
- **空间复杂度**：`O(n)`。邻接表占 `O(n)`，递归栈最坏情况下深度为树的高度（≤ n），同样是线性空间。  

---

## 心得  

- **核心技巧**：在树上使用 **后序 DFS + 动态规划**，把子树的“向下最长合法链”信息向上合并，利用两条最长子链得到可能的全局最长路径。  
- **适用的题型**：  
  1. “树上最长路径” 类问题（如 LeetCode 124. Binary Tree Maximum Path Sum）。  
  2. “子树信息合并” 类问题（如 LeetCode 543. Diameter of Binary Tree、LeetCode 1249. Minimum Remove to Make Valid Parentheses 的树形化变体）。  
- **一句话总结**：**把局部的“向下最长合法链”往上收，局部两条最佳链拼在一起即是全局答案。**  

---

## 反思  

- **第一反应**：看到“树”和“最长路径”，本能想到暴力枚举所有节点对或直接做 BFS/DFS，忽略了树的层次结构可以提供递归合并的机会。  
- **最容易踩的坑**：  
  - 忘记在子节点字符和父节点相同的情况下 **不能** 继续向上延伸，否则会错误计数。  
  - 只取单个子链的最大值，而忘记 **两条** 子链的组合，导致漏掉跨父节点的更长路径。  
  - 递归层数过深导致栈溢出，需要手动调大递归限制或改写为迭代。  
- **下次类似题目第一步**：先思考 **“对每个节点，我能从子树得到哪些信息？”**，把这些信息用 **后序 DFS** 合并，寻找局部最优能否拼成全局最优。这样往往能把指数级的暴力搜索压缩到线性时间。