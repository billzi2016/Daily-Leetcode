# #797. 所有从源点到目标点的路径 / All Paths From Source to Target

> 难度：中等 · 标签：Backtracking、Depth-First Search、Breadth-First Search、Graph · [LeetCode 链接](https://leetcode.com/problems/all-paths-from-source-to-target/)

---

## 题目（英文原版）

**Description**

Given a directed acyclic graph (DAG) of n nodes labeled from 0 to n - 1, find all possible paths from node 0 to node n - 1 and return them in any order.
The graph is given as follows: graph[i] is a list of all nodes you can visit from node i (i.e., there is a directed edge from node i to node graph[i][j]).

**Examples**

**Example 1:**

```
Input: graph = [[1,2],[3],[3],[]]
Output: [[0,1,3],[0,2,3]]
Explanation: There are two paths: 0 -> 1 -> 3 and 0 -> 2 -> 3.
```

**Example 2:**

```
Input: graph = [[4,3,1],[3,2,4],[3],[4],[]]
Output: [[0,4],[0,3,4],[0,1,3,4],[0,1,2,3,4],[0,1,4]]
```

**Constraints**

- n == graph.length
- 2 <= n <= 15
- 0 <= graph[i][j] < n
- graph[i][j] != i (i.e., there will be no self-loops).
- All the elements of graph[i] are unique.
- The input graph is guaranteed to be a DAG.

---

## 题目（中文翻译）

给定一个 **有向无环图**（directed acyclic graph，**DAG**），该图包含 `n` 个节点，编号为 `0` 到 `n - 1`。请找出所有从节点 `0`（源点）到节点 `n - 1`（目标点）的可能路径，并以任意顺序返回这些路径。

图的表示方式如下：`graph[i]` 是一个列表，列出所有可以从节点 `i` 前往的节点（即存在一条 **有向边**（directed edge）`i -> graph[i][j]`）。

**示例 1**  

**示例 2**  

**约束条件**  

- `n == graph.length`
- `2 <= n <= 15`
- `0 <= graph[i][j] < n`
- `graph[i][j] != i`（即不存在自环）
- `graph[i]` 中的所有元素互不相同
- 输入的图必定是 **有向无环图**（DAG）

**示例**  

**示例 1**  
```
Input: graph = [[1,2],[3],[3],[]]
Output: [[0,1,3],[0,2,3]]
Explanation: 有两条路径：0 -> 1 -> 3 和 0 -> 2 -> 3。
```

**示例 2**  
```
Input: graph = [[4,3,1],[3,2,4],[3],[4],[]]
Output: [[0,4],[0,3,4],[0,1,3,4],[0,1,2,3,4],[0,1,4]]
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题要求找出 **从 0 到 n‑1 的所有路径**，图是有向无环图（DAG）。  
最直接的想法是：**从起点 0 出发，沿着每一条可以走的边一直往前走，直到走到终点 n‑1 为止**。  
这正好对应 **深度优先搜索（DFS）** 的过程——我们把当前已经走过的节点记在一个列表 `path` 里，遍历当前节点的所有邻居，把邻居加入 `path` 再继续向下搜索；如果走到了终点，就把这条完整的 `path` 复制一份保存起来。  

> **类比**：把图想成一张城市地图，0 是家，n‑1 是公司。我们要把所有可能的 “从家出发 → 公司” 的路线记下来。DFS 就像是背着背包一路走，走到一个路口就把所有可能的下一条路都尝试一次，走不通就回头（回溯）再试别的路。

为什么它一定能得到所有路径？  
- 因为每次我们都**穷举**了当前节点的所有出边；  
- 递归的层层深入保证了每条可能的路线都会被完整走到终点；  
- 走到终点后立即记录，这样不会漏掉任何合法路径。  

**时间/空间分析（大白话）**  
- **时间**：我们必须把每一条合法路径都走一遍。设图中有 `p` 条合法路径，路径长度平均为 `L`，则大概要做 `p × L` 次“走一步”的操作。最坏情况下（图完全二叉树形状），路径数会指数级增长，记作 **O(2ⁿ)**（这里的 `n` 是节点数），所以时间复杂度用 **O(2ⁿ)** 表示。  
- **空间**：递归栈的深度最多等于图的最大路径长度 ≤ `n`，另外要存所有找到的路径，路径总数也是 `p`，所以 **O(p·L)**。如果只看递归栈本身，就是 **O(n)**。

#### 代码（Python）

```python
from typing import List

def allPathsSourceTarget(graph: List[List[int]]) -> List[List[int]]:
    """
    暴力 DFS（回溯）求所有 0 → n-1 路径
    """
    n = len(graph)                 # 节点总数
    target = n - 1                 # 终点编号
    res: List[List[int]] = []      # 用来存所有找到的路径
    path: List[int] = [0]          # 当前正在探索的路径，起点固定为 0

    def dfs(node: int) -> None:
        """从 node 开始继续向下搜索"""
        if node == target:                     # 到达终点
            res.append(path.copy())            # 复制一份当前路径加入答案
            return

        # 遍历 node 的所有邻居，逐个尝试
        for nxt in graph[node]:
            path.append(nxt)                    # 把 nxt 加入当前路径
            dfs(nxt)                            # 递归搜索 nxt
            path.pop()                          # 回溯：撤销刚才的选择

    dfs(0)                                      # 从起点 0 开始
    return res
```

#### 复杂度

- **时间复杂度**：`O(2ⁿ)`（指数级）  
  > 实际上取决于合法路径的数量，最坏情况下每个节点都有两条出边，导致路径数呈指数增长。  
- **空间复杂度**：`O(n + p·L)`，其中 `n` 为递归栈深度，`p·L` 为保存所有路径所需的空间。若只算递归栈，则是 `O(n)`。

---

### 2. 最优解

#### 思路  

暴力 DFS 已经能得到正确答案，但它在搜索过程中会**重复计算**同一个子问题。比如在示例 1 中，路径 `0 → 1 → 3` 和 `0 → 2 → 3` 都会在到达节点 `3` 前各自遍历一次 `3` 的后继（这里是空的），这并不浪费；但如果图更大、从某个中间节点出发能到达很多不同的终点路径，那么每次从该节点出发都要重新把所有后续路径重新枚举，效率会下降。

**优化思路**：  
- 把“从某个节点到终点的所有路径”当成一个子问题，用**记忆化搜索（Memoization）**或**动态规划（DP）**缓存起来。  
- 当我们第一次从节点 `i` 递归求解时，得到所有 `i → n-1` 的路径并保存在 `memo[i]` 中；以后若再需要从 `i` 开始的路径，只需要直接读取缓存，而不必再次遍历子图。  
- 这样每个节点的子路径只会被计算一次，整体时间下降到 **O(V + E + total_path_length)**，其中 `V`、`E` 分别是节点数和边数，`total_path_length` 是所有答案路径的总长度（不可避免，因为答案本身就这么大）。

**核心技术解释**：

- **记忆化搜索**：把递归函数的返回值保存下来（这里是“从该节点到终点的所有路径列表”），后面再需要时直接返回，省去重复工作。可以把它想成“把已经写好的章节放进一本手册”，以后查章节时直接翻手册，而不是重新写一遍。  
- **前缀路径拼接**：如果我们已经知道 `next` 节点的所有路径 `paths_from_next`（每条路径都是 `next → … → target`），那么从当前节点 `i` 出发的完整路径就可以写成 `[i] + path`，把 `i` 加到每条子路径的前面即可。

**步骤**：

1. 定义递归函数 `dfs(i)`，返回所有从 `i` 到 `target` 的路径（每条路径是列表）。  
2. 若 `i == target`，返回 `[[target]]`（只有一条空路径，起点就是终点）。  
3. 检查缓存 `memo[i]`，若已存在直接返回。  
4. 否则遍历 `graph[i]` 的每个邻居 `j`，递归得到 `dfs(j)`，把 `i` 加到每条子路径前面，收集到 `res`。  
5. 把 `res` 存入 `memo[i]` 并返回。  
6. 最后调用 `dfs(0)` 即可得到答案。

#### 代码（Python）

```python
from typing import List

def allPathsSourceTarget(graph: List[List[int]]) -> List[List[int]]:
    """
    记忆化 DFS（自底向上动态规划）求所有路径
    """
    n = len(graph)
    target = n - 1
    memo: dict[int, List[List[int]]] = {}   # 缓存：node -> 所有 node→target 的路径

    def dfs(node: int) -> List[List[int]]:
        """返回所有从 node 到 target 的路径（每条路径都是列表）"""
        if node == target:                     # 到达终点，只剩下自己这一个节点
            return [[target]]

        if node in memo:                       # 已经算过，直接返回缓存
            return memo[node]

        all_paths: List[List[int]] = []        # 用来收集从 node 出发的所有路径
        for nxt in graph[node]:                # 逐个邻居尝试
            for sub_path in dfs(nxt):          # 递归得到 nxt → target 的所有子路径
                # 把当前节点加到子路径前面形成完整路径
                all_paths.append([node] + sub_path)

        memo[node] = all_paths                  # 写入缓存
        return all_paths

    return dfs(0)                               # 从起点 0 开始
```

#### 复杂度

- **时间复杂度**：`O(V + E + total_path_length)`  
  > 每个节点只会进入递归一次，遍历它的出边一次（`V + E`），随后对每条子路径只做一次拼接，拼接的总工作量等于所有答案路径的总长度 `total_path_length`。相较于暴力解的指数级重复搜索，这里是线性（在答案规模之上的）增长。  
- **空间复杂度**：`O(V + total_path_length)`  
  > 缓存 `memo` 需要存每个节点对应的路径集合，大小同答案总长度；递归栈深度最多 `V`（即 `n`），所以整体是 `O(V + total_path_length)`。

---

## 心得

- **核心技巧**：**记忆化搜索（或自底向上的 DP）** 把“从某点到终点的所有路径”缓存，避免子问题的重复计算。  
- **适用场景**：  
  1. **所有路径枚举** 类题目（如 LeetCode 797、1066 等）。  
  2. **有向无环图的 DP**，如求最长路径、计数不同路径数等。  
  3. **递归子结构重复** 的组合类问题（子集、排列、划分等）。  
- **一句话总结**：**把每个节点到终点的所有子路径记下来，后面需要时直接取，用缓存把指数搜索压到线性**。

---

## 反思

- **第一反应**：看到“所有路径”，立刻想到“深度优先遍历 + 回溯”。这是一种最直接、最安全的思路。  
- **最容易踩的坑**：  
  - 忘记在记录路径时 **复制**（`path.copy()`），导致所有答案指向同一个列表。  
  - 对 DAG 的特性不加利用，仍然用纯暴力导致时间爆炸。  
  - 递归返回时忘记 **回溯**（`pop()`），会导致路径污染。  
- **下次类似题的第一步**：先判断图是否是 DAG，若是，则考虑**记忆化/DP**，把“从某节点到目标的子解”缓存，确保不重复遍历同一子图。这样既保持代码简洁，又能显著提升效率。