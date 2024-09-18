# #2872. K 可整除连通分量的最大数量 / Maximum Number of K-Divisible Components

> 难度：困难 · 标签：Tree、Depth-First Search · [LeetCode 链接](https://leetcode.com/problems/maximum-number-of-k-divisible-components/)

---

## 题目（英文原版）

**Description**

There is an undirected tree with n nodes labeled from 0 to n - 1. You are given the integer n and a 2D integer array edges of length n - 1, where edges[i] = [ai, bi] indicates that there is an edge between nodes ai and bi in the tree.
You are also given a 0-indexed integer array values of length n, where values[i] is the value associated with the ith node, and an integer k.
A valid split of the tree is obtained by removing any set of edges, possibly empty, from the tree such that the resulting components all have values that are divisible by k, where the value of a connected component is the sum of the values of its nodes.
Return the maximum number of components in any valid split.

**Examples**

**Example 1:**

```
Input: n = 5, edges = [[0,2],[1,2],[1,3],[2,4]], values = [1,8,1,4,4], k = 6
Output: 2
Explanation: We remove the edge connecting node 1 with 2. The resulting split is valid because:
- The value of the component containing nodes 1 and 3 is values[1] + values[3] = 12.
- The value of the component containing nodes 0, 2, and 4 is values[0] + values[2] + values[4] = 6.
It can be shown that no other valid split has more than 2 connected components.
```

**Example 2:**

```
Input: n = 7, edges = [[0,1],[0,2],[1,3],[1,4],[2,5],[2,6]], values = [3,0,6,1,5,2,1], k = 3
Output: 3
Explanation: We remove the edge connecting node 0 with 2, and the edge connecting node 0 with 1. The resulting split is valid because:
- The value of the component containing node 0 is values[0] = 3.
- The value of the component containing nodes 2, 5, and 6 is values[2] + values[5] + values[6] = 9.
- The value of the component containing nodes 1, 3, and 4 is values[1] + values[3] + values[4] = 6.
It can be shown that no other valid split has more than 3 connected components.
```

**Constraints**

- 1 <= n <= 3 * 104
- edges.length == n - 1
- edges[i].length == 2
- 0 <= ai, bi < n
- values.length == n
- 0 <= values[i] <= 109
- 1 <= k <= 109
- Sum of values is divisible by k.
- The input is generated such that edges represents a valid tree.

---

## 题目（中文翻译）

给定一棵 **无向树 (undirected tree)**，其有 `n` 个节点，编号为 `0` 到 `n‑1`。  
你会得到整数 `n` 和一个长度为 `n‑1` 的二维整数数组 `edges`，其中 `edges[i] = [a_i, b_i]` 表示节点 `a_i` 与节点 `b_i` 之间存在一条 **边 (edge)**。  

同时给定一个下标从 `0` 开始的整数数组 `values`（长度为 `n`），其中 `values[i]` 为第 `i` 个节点的 **值 (value)**，以及一个整数 `k`。

**有效的划分** 是指从树中删除任意（可以为空）集合的 **边**，使得得到的每个 **连通分量 (connected component)** 的 **值**（即该分量内所有节点的 `values` 之和）都能被 `k` 整除。  

返回任意有效划分中 **连通分量的最大数量**。

---

### 示例

#### 示例 1

```
Input: n = 5, edges = [[0,2],[1,2],[1,3],[2,4]], values = [1,8,1,4,4], k = 6
Output: 2
Explanation: 我们删除连接节点 1 与 2 的那条边。此时划分是有效的，因为：
- 包含节点 1 和 3 的连通分量的值为 values[1] + values[3] = 8 + 4 = 12，能够被 6 整除；
- 包含节点 0、2、4 的连通分量的值为 values[0] + values[2] + values[4] = 1 + 1 + 4 = 6，能够被 6 整除。

可以证明不存在其它划分能够得到更多的连通分量。
```

#### 示例 2

```
Input: n = 7, edges = [[0,1],[0,2],[1,3],[1,4],[2,5],[2,6]], values = [3,0,6,1,5,2,1], k = 3
Output: 3
Explanation: 我们删除连接节点 0 与 2 的边，以及连接节点 0 与 1 的边。此时划分是有效的，因为：
- 只包含节点 0 的连通分量的值为 values[0] = 3，能够被 3 整除；
- 包含节点 2、5、6 的连通分量的值为 values[2] + values[5] + values[6] = 6 + 2 + 1 = 9，能够被 3 整除；
- 包含节点 1、3、4 的连通分量的值为 values[1] + values[3] + values[4] = 0 + 1 + 5 = 6，能够被 3 整除。
```

---

### 约束条件

- `1 <= n <= 3 * 10^4`
- `edges.length == n - 1`
- `edges[i].length == 2`
- `0 <= a_i, b_i < n`
- `values.length == n`
- `0 <= values[i] <= 10^9`
- `1 <= k <= 10^9`
- 所有 `values` 之和能够被 `k` 整除。
- 输入保证 `edges` 构成一棵有效的树。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每条边都看成「要不要砍」的二选一**，枚举所有可能的切割方式，然后检查得到的每个连通块的节点值之和是否都是 `k` 的倍数。如果所有块都满足条件，这种切法就是「合法」的；在所有合法切法中取块数最多的那一个。

- **数据结构**：  
  - 树本身用邻接表（`list[ list[int] ]`）存储，类似于「每个人的朋友列表」；  
  - 为了枚举「砍不砍」的决定，可以用一个长度为 `n‑1` 的二进制数组 `mask`，把它想象成「每条路上是否修了围墙」的开关。  
  - 判断连通块时，需要**并查集（Union‑Find）**，它就像一本「同学册」——把同一组同学的名字写在同一页，`find` 就是查询某个人在第几页，`union` 就是把两页合并。

- **正确性**：  
  - 枚举的集合覆盖了 **所有** 可能的切割方式（因为每条边的状态都被考虑），因此如果存在合法切法，必然会被遍历到。  
  - 对每一种切法，用并查集把没有被切断的边连起来，得到的连通块正是切割后树的各个子树。随后检查每个块的节点值之和是否能被 `k` 整除，符合题意即为合法。

- **复杂度**：  
  - 枚举 `2^{n-1}` 种切法（每条边两种状态），相当于 **指数级**。  
  - 对每一种切法，需要遍历所有 `n-1` 条边并做并查集合并（几乎是 `O(n)`），再遍历 `n` 个节点求和，整体是 `O(n)`。  
  - 所以总时间复杂度是 `O( n * 2^{n-1} )`，在最坏情况下会爆炸。  
  - 空间方面主要是邻接表、并查集和递归栈，都是 `O(n)`。

> **大白话**：  
> 想象你有 30 条绳子，要把每根绳子都决定「剪」还是「不剪」——这相当于在脑子里列出十几亿种可能，根本不可能在一分钟内算完。

#### 代码（Python）

```python
from typing import List

class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))

    def find(self, x: int) -> int:
        # 查询所在的「页码」并路径压缩
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: int, b: int) -> None:
        # 把两页合并到同一页
        pa, pb = self.find(a), self.find(b)
        if pa != pb:
            self.parent[pa] = pb


def maxKDivisibleComponents_bruteforce(
    n: int, edges: List[List[int]], values: List[int], k: int
) -> int:
    m = n - 1                       # 边的数量
    best = 1                        # 至少整棵树是一个合法组件

    # 用 mask 表示每条边是否被切断，0 表示不切，1 表示切
    for mask in range(1 << m):      # 枚举 2^{n-1} 种情况
        uf = UnionFind(n)

        # 依据 mask 把未被切断的边连起来
        for i, (u, v) in enumerate(edges):
            if not (mask >> i) & 1:  # 第 i 条边不被切
                uf.union(u, v)

        # 统计每个连通块的节点和值
        comp_sum = {}
        for node in range(n):
            root = uf.find(node)
            comp_sum[root] = comp_sum.get(root, 0) + values[node]

        # 检查每个块的和是否能被 k 整除
        if all(s % k == 0 for s in comp_sum.values()):
            # 合法：组件数 = 边被切的数量 + 1
            best = max(best, bin(mask).count("1") + 1)

    return best
```

#### 复杂度

- **时间复杂度**：`O( n * 2^{n-1} )`  
  - `2^{n-1}` 是所有切法的数量，`n` 是每次遍历节点/边的开销。  
  - 对于 `n = 30` 已经是上百亿次操作，远远超出实际可接受范围。

- **空间复杂度**：`O(n)`  
  - 只用了邻接表（`O(n)`）和并查集（`O(n)`），以及常数级的临时变量。

---

### 2. 最优解

#### 思路  

从暴力解可以看出：**真正的难点在于「在哪儿切」**，而不是「枚举所有可能」。如果我们能够 **一次遍历就知道哪些子树可以独立成块**，就不必穷举。

关键观察：

1. **根树**  
   把树任选一个根（这里选 `0`），把每条边都看成「父 → 子」的方向。这样每条边只会被检查一次。

2. **子树的和模 k**  
   对于某个节点 `v`，设 `sub(v)` 为以 `v` 为根的子树里所有节点值的总和。  
   - 如果 `sub(v) % k == 0`，说明 **整个子树的和已经是 k 的倍数**，我们完全可以把这条边（`v` 与父节点的连线）**剪掉**，让子树独立成为一个合法组件。  
   - 否则，这个子树必须和父节点「合并」在一起，才能让父节点的子树总和继续向上累加。

3. **为什么这样切是最优的？**  
   - 每当我们发现一个子树的和能被 `k` 整除，就立即切掉它。这样做不会影响其他子树的可切性，因为子树之间本来就没有交叉（树的结构天然保证）。  
   - 只要父节点的子树总和最终也能被 `k` 整除（题目保证整棵树的和能被 `k` 整除），我们就能把所有满足条件的子树都切出来，得到 **最多** 的组件数。  
   - 任何不切的子树如果本身已经是 `k` 的倍数，留下来只会让组件数更少，显然不是最优。

4. **实现细节**  
   - 用 **深度优先搜索（DFS）** 从根向下遍历。DFS 返回的是「当前子树的和对 k 取模」`mod = sub(v) % k`。  
   - 对每个子节点 `c`：  
     - 递归得到 `child_mod`。  
     - 如果 `child_mod == 0`，说明子树 `c` 可以独立成块，**计数 +1**（相当于剪掉这条边）。  
     - 否则，把 `child_mod` 加到当前节点的累计和中（因为它们必须合在一起）。  
   - 最终根节点的累计和必为 `0`（题目保证），不需要再计数。

5. **答案**  
   - `ans` 记录了「可以剪掉的边」的数量。每剪掉一条边，组件数就增加 **1**。  
   - 整棵树本身也是一个组件，所以 **最大组件数 = ans + 1**，或者直接返回 `ans`（因为题目要求返回组件数），这里我们返回 `ans + 1`。

> **类比**：  
> 想象你在剪纸，每块纸的面积必须是 6 的倍数。先把大纸划分成小块，只要某块的面积已经是 6 的倍数，你立刻把它剪下来；剩下的部分继续拼凑，直到全部剪完。这样剪的次数就是最多的。

#### 代码（Python）

```python
from typing import List
import sys
sys.setrecursionlimit(10**6)   # 防止递归层数太深时崩溃

def maxKDivisibleComponents(n: int, edges: List[List[int]],
                            values: List[int], k: int) -> int:
    """
    返回在任意合法切割下，最多可以得到的连通块数量。
    思路：DFS 统计子树和 mod k，子树和为 0 时立即剪断。
    """

    # 1. 建立邻接表（把树看成无向图）
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)

    ans = 0                     # 记录可以剪断的边数

    def dfs(u: int, parent: int) -> int:
        """
        返回以 u 为根的子树的 sum % k
        同时在遍历过程中统计可以剪断的子树
        """
        nonlocal ans
        cur = values[u] % k    # 当前节点本身的值对 k 取模

        for v in g[u]:
            if v == parent:    # 不回到父节点，防止死循环
                continue
            child_mod = dfs(v, u)   # 递归得到子树的模
            if child_mod == 0:
                # 子树已经是 k 的倍数，可以独立成块，剪掉这条边
                ans += 1
                # 剪掉后，这条子树不再贡献给父节点的和
            else:
                # 必须和当前节点合并，累计模值（注意取模防止溢出）
                cur = (cur + child_mod) % k

        return cur   # 返回合并后的模值给父节点

    # 2. 从根节点 0 开始 DFS
    dfs(0, -1)

    # 3. 组件数 = 剪掉的边数 + 1（剩下的整棵树）
    return ans + 1
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 每个节点只被访问一次，遍历所有 `n‑1` 条边的总工作量正比于节点数。  
  - 与暴力解的指数级 `2^{n}` 相比，线性时间在 `n=3·10⁴` 的规模下轻松跑完。

- **空间复杂度**：`O(n)`  
  - 邻接表占 `O(n)`。  
  - 递归栈最坏深度为树的高度，最坏情况下可能是 `O(n)`（链状树），仍然在可接受范围。  
  - 额外变量 `ans`、`cur` 等都是常数级。

---

## 心得

- **核心技巧**：利用 **子树和的模 k** 来判断是否可以独立成块，配合一次 **DFS** 完成统计。  
- **适用的题型**（类似思路）  
  1. **删除边使每个连通块的权值和为偶数**（判断子树和是否为偶数）。  
  2. **树上划分，使每块的节点数恰好为某个固定值**（利用子树大小模目标值）。  
  3. **把树分成若干个和为 0（模某数）的子树**（如 LeetCode 1485 “Clone Binary Tree With Random Pointer” 的变形）。  
- **一句话总结解题钥匙**：  
  > **只要子树的累计和已经满足除数的要求，就立刻「剪」它；否则就继续向上合并。**  

---

## 反思

- **第一反应**：看到「把树切成若干块」立刻想到「枚举每条边是否切」的暴力搜索。  
- **最容易踩的坑**  
  1. **递归返回值的意义**：一定要返回 **子树和对 k 的余数**，而不是原始和，否则会出现整数溢出或错误的剪枝判断。  
  2. **根节点不计入剪切**：根没有父边，不能把整棵树当成可剪的子树，否则会多算一个组件。  
  3. **递归深度**：树可能呈链状，递归深度达 `3·10⁴`，需要手动提升递归上限或改写为显式栈。  
- **下次遇到同类题**：第一步先**把树根化**，然后**在一次 DFS 中统计子结构的「是否已满足条件」**，再决定是否剪断——把「搜索」转化为「局部判断」即可。