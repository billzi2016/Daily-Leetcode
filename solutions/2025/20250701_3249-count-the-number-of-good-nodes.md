# #3249. **统计好节点的数量** / Count the Number of Good Nodes

> 难度：中等 · 标签：Tree、Depth-First Search · [LeetCode 链接](https://leetcode.com/problems/count-the-number-of-good-nodes/)

---

## 题目（英文原版）

**Description**

There is an undirected tree with n nodes labeled from 0 to n - 1, and rooted at node 0. You are given a 2D integer array edges of length n - 1, where edges[i] = [ai, bi] indicates that there is an edge between nodes ai and bi in the tree.
A node is good if all the subtrees rooted at its children have the same size.
Return the number of good nodes in the given tree.
A subtree of treeName is a tree consisting of a node in treeName and all of its descendants.

**Examples**

**Example 1:**

```
Input: edges = [[0,1],[0,2],[1,3],[1,4],[2,5],[2,6]]
Output: 7
Explanation:
All of the nodes of the given tree are good.
```

**Example 2:**

```
Input: edges = [[0,1],[1,2],[2,3],[3,4],[0,5],[1,6],[2,7],[3,8]]
Output: 6
Explanation:
There are 6 good nodes in the given tree. They are colored in the image above.
Example 3:
Input: edges = [[0,1],[1,2],[1,3],[1,4],[0,5],[5,6],[6,7],[7,8],[0,9],[9,10],[9,12],[10,11]]
Output: 12
Explanation:
All nodes except node 9 are good.
```

**Example 3:**

```
Input: edges = [[0,1],[1,2],[1,3],[1,4],[0,5],[5,6],[6,7],[7,8],[0,9],[9,10],[9,12],[10,11]]
Output: 12
Explanation:
All nodes except node 9 are good.
```

**Constraints**

- 2 <= n <= 105
- edges.length == n - 1
- edges[i].length == 2
- 0 <= ai, bi < n
- The input is generated such that edges represents a valid tree.

---

## 题目（中文翻译）

给定一棵无向树（undirected tree），节点编号为 `0` 到 `n-1`，根节点为 `0`。你会得到一个长度为 `n-1` 的二维整数数组 `edges`，其中 `edges[i] = [a_i, b_i]` 表示节点 `a_i` 与节点 `b_i` 之间存在一条边。

如果一个节点的所有子节点（children）所对应的子树（subtree）的规模（size）都相同，则该节点被称为**好节点**（good node）。

返回这棵树中好节点的数量。

> **子树（subtree）** 是指以树中某个节点为根，并包含该节点的所有后代节点所构成的树。

### 示例

**示例 1**

```
Input: edges = [[0,1],[0,2],[1,3],[1,4],[2,5],[2,6]]
Output: 7
Explanation:
给定树的所有节点都是好节点。
```

**示例 2**

```
Input: edges = [[0,1],[1,2],[2,3],[3,4],[0,5],[1,6],[2,7],[3,8]]
Output: 6
Explanation:
该树中共有 6 个好节点，图中已用颜色标出这些节点。
```

**示例 3**

```
Input: edges = [[0,1],[1,2],[1,3],[1,4],[0,5],[5,6],[6,7],[7,8],[0,9],[9,10],[9,12],[10,11]]
Output: 12
Explanation:
除节点 9 之外，所有节点都是好节点。
```

### 约束条件

- `2 <= n <= 10^5`
- `edges.length == n - 1`
- `edges[i].length == 2`
- `0 <= a_i, b_i < n`
- 输入保证 `edges` 构成一棵有效的树。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**对每一个节点都单独去统计它的每个孩子子树的大小**，然后判断这些大小是否全部相同。  
实现思路可以拆成两步：

1. **遍历整棵树**，得到一棵**有向的父子关系**（因为原题给的是无向边，需要把根 `0` 定下来，随后把每条边朝向子节点）。  
2. 对每个节点 `v`，**再次深度优先搜索**（DFS）遍历它的子树，统计每个子树的节点数 `size(child)`。  
   - 把所有子树大小放进一个列表 `sizes`，如果 `sizes` 全部相等（或列表为空/只有一个元素），说明 `v` 是 “好节点”。  

这就是“暴力”做法——每次都重新走一遍子树，虽然思路很直观，但会产生大量重复计算。

> **类比**：把每棵子树的大小想象成一本书的页数，暴力解就像每次想比较几本书的页数时，都要重新把整本书从头读一遍，显然很慢。

**正确性**：  
- 对每个节点我们都完整地遍历了它的所有后代，得到了**真实的子树大小**。  
- 只要所有子树大小相等（或没有子树），按照题目定义，这个节点就是好节点。  
- 因此计数一定是准确的。

**复杂度分析**（大白话）：

- 对第 `i` 个节点，子树大小的统计需要遍历它的后代节点数 `size_i`。  
- 所有节点的遍历次数是 `size_0 + size_1 + … + size_{n-1}`，这相当于 **每条边会被走很多次**，最坏情况下是 `O(n²)`（比如一条链状树，根节点要遍历 `n` 次，第二个节点遍历 `n-1` 次，…）。  
- 空间方面我们只用了邻接表和递归栈，最多 `O(n)`（存图的空间）+ `O(h)`（递归深度），这里 `h ≤ n`，所以也是 `O(n)`。

#### 代码（Python）

```python
from collections import defaultdict
import sys
sys.setrecursionlimit(10**6)

def count_good_nodes_bruteforce(edges):
    n = len(edges) + 1
    # 1. 建立无向邻接表
    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    # 2. 把无向图转成有根的父子关系（根是 0）
    parent = [-1] * n
    children = [[] for _ in range(n)]

    def build(u, p):
        """DFS 把树定向，记录每个节点的子节点"""
        parent[u] = p
        for v in graph[u]:
            if v == p:          # 防止回到父节点形成环
                continue
            children[u].append(v)
            build(v, u)

    build(0, -1)

    # 3. 对每个节点单独统计子树大小（暴力）
    def subtree_size(u):
        """返回以 u 为根的子树节点数"""
        cnt = 1                     # 包含自己
        for v in children[u]:
            cnt += subtree_size(v)  # 递归累加子树大小
        return cnt

    good = 0
    for node in range(n):
        child_sizes = [subtree_size(ch) for ch in children[node]]
        # 叶子节点 child_sizes 为空，按题意也算好节点
        if len(child_sizes) <= 1 or all(s == child_sizes[0] for s in child_sizes):
            good += 1
    return good
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  解释：在最坏情况下（比如链式树），对每个节点都要遍历它下面的所有后代，累计的遍历次数约等于 `1 + 2 + … + n ≈ n²/2`，所以时间随节点数的平方增长。

- **空间复杂度**：`O(n)`  
  解释：我们需要存储邻接表、父子关系以及递归栈，最多和节点数同阶。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈在于重复遍历子树**。  
如果我们在一次 DFS 里 **同时得到每个节点的子树大小**，后面再判断好坏时就不需要再去遍历子树——只要检查已经计算好的子树大小即可。

**核心技巧**：**后序遍历（post‑order DFS）**  
- 在递归返回时，子节点的子树大小已经算好，父节点只需要把子节点返回的大小相加得到自己的子树大小。  
- 同时，父节点可以立刻检查自己所有子节点的大小是否相等，若相等就计数。

**步骤**：

1. **建图**：同暴力解，先把无向边转成邻接表。  
2. **一次 DFS**（从根 `0` 开始）  
   - 递归遍历子节点，得到每个子节点的子树大小 `sz_child`。  
   - 把所有 `sz_child` 收集进列表 `child_sizes`。  
   - 判断 `child_sizes` 是否全部相同（长度 0/1 直接算好）。  
   - 若满足条件，答案 `ans += 1`。  
   - 返回 `1 + sum(child_sizes)` 作为当前节点的子树大小。  
3. 最终 `ans` 即为好节点的数量。

> **类比**：把每棵子树的大小想象成一本书的页数，最优解相当于一次性把所有书的页数记录下来（在阅读的同时记下每本书的总页数），以后再比较时只要看记录，而不必重新阅读整本书。

**为什么是线性时间**：每条边只会被遍历 **一次**（从父到子），每个节点的计算工作也只做一次，整体是 `O(n)`。

#### 代码（Python）

```python
from collections import defaultdict
import sys
sys.setrecursionlimit(10**6)

def count_good_nodes(edges):
    """
    返回树中 “好节点” 的数量。
    思路：一次 DFS 同时得到子树大小并判断是否好节点。
    """
    n = len(edges) + 1
    # 1️⃣ 建立邻接表（无向）
    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    ans = 0  # 记录好节点的个数

    def dfs(u, parent):
        """
        后序遍历，返回以 u 为根的子树节点数。
        同时在返回前判断 u 是否是好节点并更新 ans。
        """
        nonlocal ans
        child_sizes = []          # 保存所有子节点的子树大小

        for v in graph[u]:
            if v == parent:       # 防止回到父节点
                continue
            sz = dfs(v, u)        # 递归得到子节点 v 的子树大小
            child_sizes.append(sz)

        # 判断 u 是否是好节点
        # 叶子节点 child_sizes 为空，或者只有一个子树，都是好节点
        if len(child_sizes) <= 1 or all(s == child_sizes[0] for s in child_sizes):
            ans += 1

        # 当前节点的子树大小 = 1（自己） + 所有子树大小之和
        return 1 + sum(child_sizes)

    dfs(0, -1)   # 从根节点 0 开始，父节点设为 -1（不存在）
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  解释：每条边只被遍历一次，所有节点的计算工作都是常数时间（收集子树大小、比较是否相等），所以运行时间随节点数线性增长。

- **空间复杂度**：`O(n)`  
  解释：邻接表需要 `O(n)` 的存储，递归栈深度最坏为树的高度，最坏情况下（链式树）为 `O(n)`，整体仍然是 `O(n)`。

---

## 心得

- **核心技巧**：一次后序 DFS 同时计算子树大小并判断 “好节点”。  
- **适用的题型**  
  1. 需要**子树信息**（大小、和、最大值等）并在父节点做判断的题目，如 “判断每个节点的子树是否满足某种属性”。  
  2. “树的均衡/对称/等价” 类问题，例如 “判断每个节点的左右子树大小是否相等”。  
  3. 需要**全局统计**但信息来源于局部子树的题目，如 “统计满足某种子树结构的节点”。  
- **一句话总结**：**一次 DFS 把所有子树信息“带回”给父节点，既省时又省力。**

---

## 反思

- **第一反应**：看到“所有子树大小相同”，立刻想到要先**求出每个子树的节点数**，于是想到遍历每个节点的子树——这就是暴力思路。  
- **最容易踩的坑**  
  1. **叶子节点的定义**：没有子节点时应直接算作好节点，别忘了把长度 `0/1` 的情况特殊处理。  
  2. **递归深度**：树可能很深（`n=10⁵`），需要 `sys.setrecursionlimit` 或改写为显式栈的迭代 DFS。  
  3. **父子方向**：原始边是无向的，DFS 时必须记录父节点防止回到已经遍历的节点，否则会陷入无限递归。  
- **下次遇到同类题**：第一步先**想“一次遍历把所有局部信息收集完”——也就是后序 DFS 或动态规划的“自底向上”思路。这样可以避免重复遍历，直接得到线性时间解。