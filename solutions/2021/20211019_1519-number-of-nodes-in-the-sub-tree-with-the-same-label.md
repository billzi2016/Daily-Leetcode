# #1519. **子树中标签相同的节点数** / Number of Nodes in the Sub-Tree With the Same Label

> 难度：中等 · 标签：Hash Table、Tree、Depth-First Search、Breadth-First Search、Counting · [LeetCode 链接](https://leetcode.com/problems/number-of-nodes-in-the-sub-tree-with-the-same-label/)

---

## 题目（英文原版）

**Description**

You are given a tree (i.e. a connected, undirected graph that has no cycles) consisting of n nodes numbered from 0 to n - 1 and exactly n - 1 edges. The root of the tree is the node 0, and each node of the tree has a label which is a lower-case character given in the string labels (i.e. The node with the number i has the label labels[i]).
The edges array is given on the form edges[i] = [ai, bi], which means there is an edge between nodes ai and bi in the tree.
Return an array of size n where ans[i] is the number of nodes in the subtree of the ith node which have the same label as node i.
A subtree of a tree T is the tree consisting of a node in T and all of its descendant nodes.

**Examples**

**Example 1:**

```
Input: n = 7, edges = [[0,1],[0,2],[1,4],[1,5],[2,3],[2,6]], labels = "abaedcd"
Output: [2,1,1,1,1,1,1]
Explanation: Node 0 has label 'a' and its sub-tree has node 2 with label 'a' as well, thus the answer is 2. Notice that any node is part of its sub-tree.
Node 1 has a label 'b'. The sub-tree of node 1 contains nodes 1,4 and 5, as nodes 4 and 5 have different labels than node 1, the answer is just 1 (the node itself).
```

**Example 2:**

```
Input: n = 4, edges = [[0,1],[1,2],[0,3]], labels = "bbbb"
Output: [4,2,1,1]
Explanation: The sub-tree of node 2 contains only node 2, so the answer is 1.
The sub-tree of node 3 contains only node 3, so the answer is 1.
The sub-tree of node 1 contains nodes 1 and 2, both have label 'b', thus the answer is 2.
The sub-tree of node 0 contains nodes 0, 1, 2 and 3, all with label 'b', thus the answer is 4.
```

**Example 3:**

```
Input: n = 5, edges = [[0,1],[0,2],[1,3],[0,4]], labels = "aabab"
Output: [3,2,1,1,1]
```

**Constraints**

- 1 <= n <= 105
- edges.length == n - 1
- edges[i].length == 2
- 0 <= ai, bi < n
- ai != bi
- labels.length == n
- labels is consisting of only of lowercase English letters.

---

## 题目（中文翻译）

给定一棵树（tree），即一个连通的无向图且不存在环，包含 `n` 个节点，编号为 `0` 到 `n‑1`，恰好有 `n‑1` 条边。树的根节点为 `0`，每个节点都有一个由小写字符组成的标签，标签字符串为 `labels`（即编号为 `i` 的节点的标签为 `labels[i]`）。  
`edges` 数组的形式为 `edges[i] = [a_i, b_i]`，表示在节点 `a_i` 与节点 `b_i` 之间存在一条边。  

返回长度为 `n` 的数组 `ans`，其中 `ans[i]` 表示以节点 `i` 为根的子树（subtree）中，标签与节点 `i` 相同的节点数量。  
子树指的是以某个节点为根，包含该节点及其所有后代节点的树结构。

---

### 示例

**示例 1**

```
Input: n = 7, edges = [[0,1],[0,2],[1,4],[1,5],[2,3],[2,6]], labels = "abaedcd"
Output: [2,1,1,1,1,1,1]
Explanation: 
节点 0 的标签为 'a'，其子树中还有节点 2 的标签也是 'a'，因此答案为 2。需要注意的是任意节点都算作其子树的一部分。  
节点 1 的标签为 'b'。节点 1 的子树包含节点 1、4、5，由于节点 4、5 的标签与节点 1 不同，答案为 1。  
其余节点的子树中与自身标签相同的节点仅有它们自己，答案均为 1。
```

**示例 2**

```
Input: n = 4, edges = [[0,1],[1,2],[0,3]], labels = "bbbb"
Output: [4,2,1,1]
Explanation: 
节点 2 的子树只有节点 2 本身，答案为 1。  
节点 3 的子树只有节点 3 本身，答案为 1。  
节点 1 的子树包含节点 1 和 2，两个节点的标签均为 'b'，答案为 2。  
节点 0 的子树包含节点 0、1、2、3，四个节点的标签全部为 'b'，答案为 4。
```

**示例 3**

```
Input: n = 5, edges = [[0,1],[0,2],[1,3],[0,4]], labels = "aabab"
Output: [3,2,1,1,1]
```

---

### 约束条件

- `1 <= n <= 10^5`
- `edges.length == n - 1`
- `edges[i].length == 2`
- `0 <= a_i, b_i < n`
- `a_i != b_i`
- `labels.length == n`
- `labels` 仅由小写英文字母组成

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：**对每一个节点 i，遍历它的整棵子树，统计与 `labels[i]` 相同的节点个数**。  
实现时可以把树先存成「邻接表」——把每条无向边 `[a,b]` 放进两个列表 `graph[a]` 与 `graph[b]` 中。  
随后对每个节点 i 进行一次深度优先搜索（DFS）或广度优先搜索（BFS），只要不回到已经走过的父节点，就一直往下走，直到把所有后代都访问完。  

- **邻接表** 就像一本「城市地图」：`graph[x]` 里列出所有和城市 `x` 直接相连的城市。  
- **DFS** 类似于「探险队」从根节点出发，沿着一条路一直走到底再回头，逐层深入。  

为什么这个方法一定能得到答案？因为我们 **完整遍历了** 每个节点的子树，统计了所有出现的标签，自然能够得到与自身标签相同的数量。  

但是，这种「每个节点都遍历一次子树」的做法会产生大量重复工作：  
- 当我们从根节点遍历整棵树时，已经算过了所有子树的节点；随后再从根的孩子再遍历一次时，根的孩子的子树又被重新遍历了一遍。  
- 在最坏情况下（树是一条链），第 1 个节点遍历 `n` 次，第 2 个遍历 `n-1` 次，…，第 `n` 个遍历 `1` 次，总共大约是 `n + (n-1) + … + 1 = n·(n+1)/2 ≈ O(n²)` 次访问。

**时间复杂度** 用大白话说就是「如果 n = 10,000，最坏情况下要做大约 100,000,000 次操作」——对电脑来说已经算是「很慢」了。  

**空间复杂度** 只需要存放邻接表（每条边存两次）和一次 DFS/BFS 的递归栈或队列，都是 `O(n)`。

#### 代码（Python）

```python
from collections import defaultdict, deque
from typing import List

def countSubTrees_brute(n: int, edges: List[List[int]], labels: str) -> List[int]:
    # 1️⃣ 建立邻接表（类似“城市地图”）
    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    # 2️⃣ 对每个节点都做一次 BFS，统计同标签节点数
    ans = [0] * n

    for start in range(n):
        target_label = labels[start]          # 我们要统计的字符
        cnt = 0
        visited = [False] * n
        q = deque([start])
        visited[start] = True

        while q:
            node = q.popleft()
            if labels[node] == target_label:
                cnt += 1                     # 找到相同标签，计数 +1
            for nxt in graph[node]:
                if not visited[nxt]:
                    visited[nxt] = True
                    q.append(nxt)           # 继续向下遍历

        ans[start] = cnt                      # 子树中同标签的数量

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 解释：每个节点都要遍历它的全部子树，最坏情况下会出现 `1 + 2 + … + n ≈ n²/2` 次访问。  
- **空间复杂度**：`O(n)`  
  - 解释：邻接表占 `O(n)`，每次 BFS 用到的 `visited` 与队列也都是 `O(n)`，但只在一次遍历时存在。

---

### 2. 最优解  

#### 思路  
从暴力解可以看到 **重复遍历** 是瓶颈。我们需要一种「一次遍历就把所有信息都算好」的办法。  

**关键观察**：  
- 在树形结构里，**子树的答案只依赖于它的子节点**，而不需要再去遍历整棵子树。  
- 如果我们能够让每个节点 **向父节点返回**「它的子树里每个字符出现的次数」，父节点只要把所有子节点的计数加起来，再加上自己本身的字符计数，就能得到完整的统计。  

这正好对应 **后序深度优先搜索**（DFS）——先递归处理所有子节点，再回到当前节点进行合并。  

**需要的工具**：  
- **邻接表**（同上），用来快速得到一个节点的所有相邻节点。  
- **计数数组**：长度为 26（因为只有小写英文字母），`cnt[c]` 表示子树中字符 `c` 出现的次数。可以把它想成「字典」——像查字典时先找到对应的页码再读取内容，这里直接用下标（`ord(c) - ord('a')`）定位。  
- **递归栈**：DFS 的递归本身会形成一个栈，深度最多 `n`，在 Python 中默认递归深度约 1000，针对 `n ≤ 10⁵` 需要手动把递归改成显式栈或使用 `sys.setrecursionlimit` 提高上限。这里为了简洁使用递归并提升上限。  

**算法步骤**  
1. 建立邻接表。  
2. 从根节点 `0` 开始 DFS。函数 `dfs(u, parent)` 返回一个长度为 26 的列表 `cnt_u`，表示以 `u` 为根的子树中每个字符的出现次数。  
3. 在 `dfs` 中：  
   - 初始化 `cnt_u` 为全 0。  
   - 对所有相邻节点 `v`（排除父节点防止回头），递归得到 `cnt_v`，把 `cnt_v` 加到 `cnt_u`（相当于把子树信息合并进来）。  
   - 最后把当前节点自己的字符计数 `cnt_u[ label[u] ] += 1`。  
   - `ans[u] = cnt_u[ label[u] ]` 即为答案。  
   - 返回 `cnt_u` 给父节点。  
4. DFS 完成后，`ans` 即为所求。  

**为什么是最优**：每条边只会被访问 **两次**（一次从父向子，一次从子向父），每个节点只会创建一次长度为 26 的计数数组并进行常数次的加法，整体时间是 **线性 O(n)**，空间也是 **O(n)**（邻接表 + 递归栈 + 计数数组总计 `n·26` ≈ `O(n)`）。

#### 代码（Python）

```python
import sys
from collections import defaultdict
from typing import List

def countSubTrees(n: int, edges: List[List[int]], labels: str) -> List[int]:
    # 为防止递归深度不足，适当调高上限（n ≤ 1e5）
    sys.setrecursionlimit(2 * 10**5)

    # 1️⃣ 建立邻接表
    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    ans = [0] * n                     # 最终答案数组

    # 2️⃣ 深度优先搜索，返回 26 长度的计数数组
    def dfs(u: int, parent: int) -> List[int]:
        # cnt_u[i] 表示子树中字符 (chr(i + ord('a'))) 的出现次数
        cnt_u = [0] * 26

        # 处理所有子节点
        for v in graph[u]:
            if v == parent:           # 防止回到父节点形成环
                continue
            cnt_child = dfs(v, u)     # 递归得到子节点的计数
            # 把子节点的计数累加到当前节点
            for i in range(26):
                cnt_u[i] += cnt_child[i]

        # 加上当前节点自己的标签
        idx = ord(labels[u]) - ord('a')
        cnt_u[idx] += 1

        # 当前节点的答案就是它标签对应的计数
        ans[u] = cnt_u[idx]

        return cnt_u

    # 从根节点 0 开始遍历
    dfs(0, -1)
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 解释：每条边只被遍历两次，每个节点只进行一次长度为 26 的数组合并，整体随节点数线性增长。相较于暴力的 `O(n²)`，大幅提升。  
- **空间复杂度**：`O(n)`  
  - 解释：邻接表占 `O(n)`，递归栈深度最多 `n`（在最坏的链形树里），每次递归返回的计数数组大小固定为 26，累计仍是线性 `O(n)`。

---

## 心得  

- **核心技巧**：后序深度优先搜索 + 计数数组（相当于「字典」），一次遍历即可把整棵子树的信息汇总给父节点。  
- **适用题型**  
  1. 「子树颜色/标签统计」类问题（如 LeetCode 1519 Number of Nodes in the Sub-Tree With the Same Label）。  
  2. 「子树信息合并」类问题，例如求每个节点子树中的最大值、最小值或出现次数。  
  3. 「树上 DP」的基础形态——子树向上合并局部信息再向下传递。  
- **一句话总结**：**把子树的局部统计“自底向上”累加，一遍遍历搞定全部答案**。

---

## 反思  

- **第一反应**：看到「子树」和「统计」二字，立刻想到「对每个节点都遍历一次子树」——这就是最直接的暴力思路。  
- **最容易踩的坑**  
  - **递归深度**：树可能是链状，递归层数达 `n`，需要 `sys.setrecursionlimit` 或改写成显式栈。  
  - **重复计数**：在合并子节点计数时一定要 **累加**（`+=`），而不是覆盖。  
  - **字符映射**：`ord(c) - ord('a')` 必须对应 0‑25，防止越界。  
  - **父子关系**：遍历邻接表时必须排除父节点，否则会在无向图中形成无限循环。  
- **下次遇到同类题**：第一步先思考「能否把子树信息自底向上汇总」——如果答案是「可以」，就直接写后序 DFS 并设计合适的状态（这里是 26 长度计数数组）。这样往往能把时间复杂度从 `O(n²)` 降到 `O(n)`。