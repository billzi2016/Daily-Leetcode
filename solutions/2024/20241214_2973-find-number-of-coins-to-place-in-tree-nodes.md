# #2973. 求树节点上放置硬币的数量 / Find Number of Coins to Place in Tree Nodes

> 难度：困难 · 标签：Dynamic Programming、Tree、Depth-First Search、Sorting、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/find-number-of-coins-to-place-in-tree-nodes/)

---

## 题目（英文原版）

**Description**

You are given an undirected tree with n nodes labeled from 0 to n - 1, and rooted at node 0. You are given a 2D integer array edges of length n - 1, where edges[i] = [ai, bi] indicates that there is an edge between nodes ai and bi in the tree.
You are also given a 0-indexed integer array cost of length n, where cost[i] is the cost assigned to the ith node.
You need to place some coins on every node of the tree. The number of coins to be placed at node i can be calculated as:
Return an array coin of size n such that coin[i] is the number of coins placed at node i.

**Examples**

**Example 1:**

```
Input: edges = [[0,1],[0,2],[0,3],[0,4],[0,5]], cost = [1,2,3,4,5,6]
Output: [120,1,1,1,1,1]
Explanation: For node 0 place 6 * 5 * 4 = 120 coins. All other nodes are leaves with subtree of size 1, place 1 coin on each of them.
```

**Example 2:**

```
Input: edges = [[0,1],[0,2],[1,3],[1,4],[1,5],[2,6],[2,7],[2,8]], cost = [1,4,2,3,5,7,8,-4,2]
Output: [280,140,32,1,1,1,1,1,1]
Explanation: The coins placed on each node are:
- Place 8 * 7 * 5 = 280 coins on node 0.
- Place 7 * 5 * 4 = 140 coins on node 1.
- Place 8 * 2 * 2 = 32 coins on node 2.
- All other nodes are leaves with subtree of size 1, place 1 coin on each of them.
```

**Example 3:**

```
Input: edges = [[0,1],[0,2]], cost = [1,2,-2]
Output: [0,1,1]
Explanation: Node 1 and 2 are leaves with subtree of size 1, place 1 coin on each of them. For node 0 the only possible product of cost is 2 * 1 * -2 = -4. Hence place 0 coins on node 0.
```

**Constraints**

- 2 <= n <= 2 * 104
- edges.length == n - 1
- edges[i].length == 2
- 0 <= ai, bi < n
- cost.length == n
- 1 <= |cost[i]| <= 104
- The input is generated such that edges represents a valid tree.

---

## 题目（中文翻译）

你得到一棵 **无向树（undirected tree）**，有 n 个节点，编号为 0 到 n - 1，根节点为 0。给定长度为 n - 1 的二维整数数组 edges，`edges[i] = [ai, bi]` 表示节点 ai 和节点 bi 之间有一条边。  

同时给定一个长度为 n 的 0 索引整数数组 cost，`cost[i]` 是第 i 个节点的代价（cost）。  

需要在树的每个节点上放置一定数量的硬币（coins）。节点 i 上放置的硬币数量可通过题目给出的公式计算（公式在原题中省略，此处保留描述）。  

返回一个长度为 n 的数组 coin，`coin[i]` 为放置在节点 i 上的硬币数量。

---

### 示例

**示例 1**  
输入:  
```
edges = [[0,1],[0,2],[0,3],[0,4],[0,5]], 
cost = [1,2,3,4,5,6]
```  
输出: `[120,1,1,1,1,1]`  
解释: 对于根节点 0，放置 6 × 5 × 4 = 120 枚硬币。其余节点都是叶子节点，子树（subtree）大小为 1，分别放置 1 枚硬币。

**示例 2**  
输入:  
```
edges = [[0,1],[0,2],[1,3],[1,4],[1,5],[2,6],[2,7],[2,8]], 
cost = [1,4,2,3,5,7,8,-4,2]
```  
输出: `[280,140,32,1,1,1,1,1,1]`  
解释: 各节点放置的硬币数量为:  
- 节点 0: 8 × 7 × 5 = 280 枚  
- 节点 1: 7 × 5 × 4 = 140 枚  
- 节点 2: 8 × 2 × 2 = 32 枚  
- 其余节点均为叶子，子树大小为 1，放置 1 枚硬币。

**示例 3**  
输入:  
```
edges = [[0,1],[0,2]], 
cost = [1,2,-2]
```  
输出: `[0,1,1]`  
解释: 节点 1 和 2 是叶子节点，子树大小为 1，分别放置 1 枚硬币。对于根节点 0，唯一可能的代价乘积为 2 × 1 × (-2) = -4，故放置 0 枚硬币。

---

### 约束条件

- 2 ≤ n ≤ 2 × 10⁴  
- `edges.length == n - 1`  
- `edges[i].length == 2`  
- 0 ≤ ai, bi < n  
- `cost.length == n`  
- 1 ≤ |cost[i]| ≤ 10⁴  
- 输入保证 `edges` 构成一棵合法的树。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**对每一个节点**，先把它所在子树的所有节点找出来（可以用一次 DFS），把这些节点的 `cost` 收集到一个数组里，然后在数组里穷举所有可能的三个数的组合，算出最大的乘积。  

- **数据结构**：  
  - `list`（列表）相当于我们生活中的“装东西的箱子”，把子树里所有 `cost` 都装进去。  
  - “穷举三个数的组合”可以想象成从箱子里挑出 **三件商品**，把它们的价格相乘，找出最大的那一次。  

- **为什么正确**：  
  - 我们把子树里所有可能的三元组都算了一遍，最大值自然就是答案。  

- **复杂度分析（大白话版）**：  
  - 对每个节点，我们都要遍历一次它的子树。根节点的子树大小是 `n`，第二层的子树大约是 `n/2`，如此往下。总体上相当于 **把每条边看了很多次**，最坏情况是 `O(n²)`（比如链状树，每次都要遍历几乎全部节点）。  
  - 空间上我们只需要保存一次遍历的临时数组，最多 `O(n)`（最坏是根节点的子树）。  

#### 代码（Python）  

```python
from itertools import combinations
from collections import defaultdict
import sys
sys.setrecursionlimit(10**6)

def brute_force(edges, cost):
    n = len(cost)
    # 建图，邻接表
    g = defaultdict(list)
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)

    # 把子树里所有节点的 cost 收集起来
    def collect(node, parent):
        vals = [cost[node]]                 # 先把自己的 cost 放进来
        for nb in g[node]:
            if nb == parent:                # 防止回到父节点
                continue
            vals.extend(collect(nb, node)) # 递归收集子树
        return vals

    ans = [0] * n
    for i in range(n):
        sub_vals = collect(i, -1)           # 收集 i 为根的子树
        if len(sub_vals) < 3:               # 子树节点不足 3 个
            ans[i] = 1
            continue
        # 穷举所有三个数的组合，取最大乘积
        best = -10**18
        for a, b, c in combinations(sub_vals, 3):
            prod = a * b * c
            if prod > best:
                best = prod
        ans[i] = 0 if best < 0 else best    # 负数要置 0
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 解释：对每个节点都要遍历它的整个子树，最坏情况下会出现 `1 + 2 + … + n ≈ n²/2` 次访问。  
- **空间复杂度**：`O(n)`  
  - 解释：递归栈最深 `O(n)`，以及临时保存子树节点的列表最多 `O(n)`（根节点时）。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈** 出在每次都要把整棵子树的所有 `cost` 收集出来并排序。我们只需要 **极端的几个数**（最大三个正数、最小三个负数），因为乘积的最大值必然由这些极端值构成。  

**关键观察**：  
- 任意三个数的乘积，要么是「三个最大的数」相乘，要么是「两个最小的负数」乘上「最大的正数」。  
- 因此，只要知道子树里 **前 3 大** 与 **前 3 小**（绝对值最小的负数）就能算出答案。  

**如何在 DFS 中合并子树信息**：  
1. 对每个节点做一次后序 DFS（先处理子节点，再处理自己）。  
2. 每个子节点返回给父节点 **最多 6 个数**：  
   - 前 3 大的正数（或整体最大的数）  
   - 前 3 小的负数（或整体最小的数）  
3. 父节点把自己的 `cost` 加进去，再把所有子节点返回的数合并，**只保留**整体的前 3 大和前 3 小（其余的都可以丢掉）。  
4. 用这 6 个数（最多）计算当前节点的答案：  
   - 若子树节点数 `< 3` → 直接 `1`。  
   - 否则取 `max( smallest[0] * smallest[1] * largest[-1] , largest[-1] * largest[-2] * largest[-3] )`。  
   - 若最大乘积为负 → 结果改成 `0`。  

**为什么只保留 6 个数仍然能得到正确答案**：  
- 任意三个数的乘积只会涉及到 **极端的三正或两负一正**，这三正一定在「最大的 3 个」里，两负一定在「最小的 3 个」里。其余的数不可能在最大乘积中出现。  

**类比**：  
- 把每个子树看作一本小字典，里面只记最常用的 3 个词（最大）和最少用的 3 个词（最小）。当两本字典合并时，只需要把这 6 个词再挑出最常用的 3 和最少用的 3，其他词直接丢掉，既省空间又不影响查询。  

#### 代码（Python）  

```python
from collections import defaultdict
import sys
sys.setrecursionlimit(10**6)

def maxProductCoins(edges, cost):
    n = len(cost)
    g = defaultdict(list)
    for a, b in edges:               # 建立无向树的邻接表
        g[a].append(b)
        g[b].append(a)

    ans = [0] * n                     # 最终答案

    # -------------------------------------------------
    # dfs 返回两件事：
    # 1) subtree size（子树节点数），用于判断是否 <3
    # 2) 一个列表，最多 6 个数：前 3 大 + 前 3 小
    # -------------------------------------------------
    def dfs(node, parent):
        size = 1                      # 自己算一个节点
        # 先把自己的 cost 放进临时列表
        vals = [cost[node]]

        for nb in g[node]:
            if nb == parent:         # 不回到父节点
                continue
            child_size, child_vals = dfs(nb, node)
            size += child_size
            vals.extend(child_vals)   # 合并子树的极值

        # ------------------- 计算当前节点的答案 -------------------
        if size < 3:                  # 子树节点不足 3 个
            ans[node] = 1
        else:
            # 把收集到的数排序一次，取极值
            vals.sort()
            # 三个最大的数
            cand1 = vals[-1] * vals[-2] * vals[-3]
            # 两个最小（可能是负数） + 最大
            cand2 = vals[0] * vals[1] * vals[-1]
            best = max(cand1, cand2)
            ans[node] = 0 if best < 0 else best

        # ------------------- 为父节点准备返回值 -------------------
        # 只保留整体的前 3 大和前 3 小（最多 6 个数）
        vals.sort()
        # 最小的三个
        smallest = vals[:3]
        # 最大的三个
        largest = vals[-3:] if len(vals) >= 3 else vals
        # 合并后返回，仍然最多 6 个
        return size, smallest + largest

    dfs(0, -1)          # 树的根节点是 0
    return ans
```

> **代码要点解释（每行中文注释已在代码中给出）**  
- `g` 用邻接表存图，类似“城市之间的道路”。  
- `dfs` 采用后序遍历，先把子树的信息收集完再处理当前节点。  
- `vals` 暂时保存所有极端数，随后通过 `sort` 取前 3 /后 3。  
- `ans[node]` 的计算只看两种可能的乘积，省去了枚举所有三元组。  
- 最后返回的 `smallest + largest` 保证父节点仍然只拿到最多 6 个数，保持整体 **线性** 时间。  

#### 复杂度  

- **时间复杂度**：`O(n log d)`（`d` 为节点度数），在最坏的星形树中 `d = n-1`，仍是 `O(n log n)`。  
  - 解释：每个节点只对 **自己和子节点返回的至多 6 个数** 做一次排序，排序长度至多 `6·deg(node)+1`，整体累计在 `O(n log n)` 以内。相比暴力的 `O(n²)` 快了好几倍。  
- **空间复杂度**：`O(n)`  
  - 解释：邻接表占 `O(n)`，递归栈最深 `O(n)`，每次返回的极值列表最多 6 个，常数级空间。  

---

## 心得  

- **核心技巧**：在需要求「子树中任意三数乘积最大」时，只需维护 **子树的前 3 大与前 3 小**，不必保存全部节点。  
- **适用场景**：  
  1. 求子树（或子数组）中「最大/最小 k 个元素」或「最大 k 项乘积」等极值问题。  
  2. 树形 DP 中需要合并子树信息，但信息量可以被「常数上界」压缩的情况。  
- **一句话总结解题钥匙**：**「只保留极端」**——最大乘积只会由极大或极小的若干数决定，省去全部数据的冗余。  

---

## 反思  

- **拿到题目第一反应**：先想到「遍历子树收集所有值」——这就是暴力解。  
- **最容易踩的坑**：  
  - 忘记子树节点数小于 3 时答案应为 `1`（不是 `0`）。  
  - 只考虑「三个最大」而忽略「两个最小（负）× 最大」的情况，导致负数情况下答案错误。  
  - 合并子树时如果直接拼接全部列表，会导致 `O(n²)` 的时间爆炸。  
- **下次类似题的第一步**：先**思考答案只会依赖哪些“极端”元素**，确认可以用常数大小的状态来表示子树信息，再设计 DP/DFS 合并过程。