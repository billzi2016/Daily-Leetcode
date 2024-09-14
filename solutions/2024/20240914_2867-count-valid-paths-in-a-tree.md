# #2867. 树中有效路径计数 / Count Valid Paths in a Tree

> 难度：困难 · 标签：Math、Dynamic Programming、Tree、Depth-First Search、Number Theory · [LeetCode 链接](https://leetcode.com/problems/count-valid-paths-in-a-tree/)

---

## 题目（英文原版）

**Description**

There is an undirected tree with n nodes labeled from 1 to n. You are given the integer n and a 2D integer array edges of length n - 1, where edges[i] = [ui, vi] indicates that there is an edge between nodes ui and vi in the tree.
Return the number of valid paths in the tree.
A path (a, b) is valid if there exists exactly one prime number among the node labels in the path from a to b.
Note that:

**Examples**

**Example 1:**

```
Input: n = 5, edges = [[1,2],[1,3],[2,4],[2,5]]
Output: 4
Explanation: The pairs with exactly one prime number on the path between them are: 
- (1, 2) since the path from 1 to 2 contains prime number 2. 
- (1, 3) since the path from 1 to 3 contains prime number 3.
- (1, 4) since the path from 1 to 4 contains prime number 2.
- (2, 4) since the path from 2 to 4 contains prime number 2.
It can be shown that there are only 4 valid paths.
```

**Example 2:**

```
Input: n = 6, edges = [[1,2],[1,3],[2,4],[3,5],[3,6]]
Output: 6
Explanation: The pairs with exactly one prime number on the path between them are: 
- (1, 2) since the path from 1 to 2 contains prime number 2.
- (1, 3) since the path from 1 to 3 contains prime number 3.
- (1, 4) since the path from 1 to 4 contains prime number 2.
- (1, 6) since the path from 1 to 6 contains prime number 3.
- (2, 4) since the path from 2 to 4 contains prime number 2.
- (3, 6) since the path from 3 to 6 contains prime number 3.
It can be shown that there are only 6 valid paths.
```

**Constraints**

- 1 <= n <= 105
- edges.length == n - 1
- edges[i].length == 2
- 1 <= ui, vi <= n
- The input is generated such that edges represent a valid tree.

---

## 题目（中文翻译）

给定一棵无向树，节点编号为 `1` 到 `n`。  
你会得到整数 `n` 和一个长度为 `n - 1` 的二维整数数组 `edges`，其中 `edges[i] = [ui, vi]` 表示树中存在一条连接节点 `ui` 和 `vi` 的边。

返回树中 **有效路径** 的数量。

**定义**  
一条路径 `(a, b)` 被称为有效的，当且仅当从节点 `a` 到节点 `b` 的路径上恰好出现 **一个质数（prime）** 的节点编号。

---

## 示例

### 示例 1
**输入**  
```
n = 5, edges = [[1,2],[1,3],[2,4],[2,5]]
```
**输出**  
```
4
```
**解释**  
恰好在路径上包含唯一质数的节点对有：

- `(1, 2)`：路径 `1 → 2` 中包含质数 `2`。  
- `(1, 3)`：路径 `1 → 3` 中包含质数 `3`。  
- `(1, 4)`：路径 `1 → 2 → 4` 中包含质数 `2`。  
- `(2, 4)`：路径 `2 → 4` 中包含质数 `2`。

---

### 示例 2
**输入**  
```
n = 6, edges = [[1,2],[1,3],[2,4],[3,5],[3,6]]
```
**输出**  
```
6
```
**解释**  
恰好在路径上包含唯一质数的节点对有：

- `(1, 2)`：路径 `1 → 2` 中包含质数 `2`。  
- `(1, 3)`：路径 `1 → 3` 中包含质数 `3`。  
- `(1, 4)`：路径 `1 → 2 → 4` 中包含质数 `2`。  
- `(1, 6)`：路径 `1 → 3 → 6` 中包含质数 `3`。  
- `(2, 4)`：路径 `2 → 4` 中包含质数 `2`。  
- `(3, 5)`：路径 `3 → 5` 中包含质数 `5`。

---

## 约束条件

- `1 <= n <= 10^5`
- `edges.length == n - 1`
- `edges[i].length == 2`
- `1 <= ui, vi <= n`
- 输入保证 `edges` 构成一棵有效的树。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有可能的**节点对**都枚举一遍，然后检查这条路径上素数的个数是否恰好为 1。  

- **数据结构**  
  - 用**邻接表**（`list[int][]`）存树，因为树的边数只有 `n‑1`，查相邻节点就像翻字典一样快：键是节点编号，值是它的邻居列表。  
  - 为了快速判断一个编号是否是素数，我们可以在每次查询时用**试除法**（从 2 到 √x）判断，这相当于在字典里一次性查找“这个数是不是素数”。  

- **为什么正确**  
  只要把每一对 `(a, b)` 的唯一路径找出来，统计其中的素数个数，恰好为 1 的就算是合法路径。因为树中任意两点之间只有唯一一条简单路径，这一步没有遗漏也不会重复计数。

- **时间/空间复杂度**  
  - 枚举所有 unordered pair 需要 `C(n,2) = n·(n‑1)/2` 次，大约 **O(n²)**。  
  - 对每一对我们都要跑一次 BFS/DFS 来找路径，最坏会遍历 `O(n)` 条边，所以整体时间是 **O(n³)**（在最坏情况下），但即使把路径查找改成 `O(log n)`（用 LCA）也仍然是 **O(n²)**。  
  - 空间上我们只保存邻接表和几个辅助数组，都是 `O(n)`。  

> **大白话**：  
> - `O(n²)` 就像把 `n` 张卡片两两配对，配对次数随 `n` 的平方增长。  
> - `O(n³)` 就是每配对再遍历一遍整棵树，工作量随 `n` 的立方增长，几千个节点就已经吃不消了。

#### 代码（Python）

```python
from collections import deque
import math

def is_prime(x: int) -> bool:
    """朴素判素数，适合小规模测试"""
    if x < 2:
        return False
    for d in range(2, int(math.isqrt(x)) + 1):
        if x % d == 0:
            return False
    return True

def bfs_path(u: int, v: int, adj: list[list[int]]) -> list[int]:
    """在树上找 u 到 v 的唯一路径，返回路径上的节点列表"""
    parent = [-1] * len(adj)
    q = deque([u])
    parent[u] = u
    while q:
        cur = q.popleft()
        if cur == v:
            break
        for nxt in adj[cur]:
            if parent[nxt] == -1:
                parent[nxt] = cur
                q.append(nxt)
    # 逆向回溯得到路径
    path = []
    node = v
    while node != u:
        path.append(node)
        node = parent[node]
    path.append(u)
    path.reverse()
    return path

def count_valid_bruteforce(n: int, edges: list[list[int]]) -> int:
    # 建邻接表（下标从 1 开始，方便与题目编号对应）
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)

    # 预先算出每个编号是否为素数
    prime = [False] * (n + 1)
    for i in range(1, n + 1):
        prime[i] = is_prime(i)

    ans = 0
    # 枚举所有 unordered pair (a, b)
    for a in range(1, n + 1):
        for b in range(a + 1, n + 1):
            path = bfs_path(a, b, adj)
            # 统计路径上素数的个数
            cnt = sum(1 for node in path if prime[node])
            if cnt == 1:
                ans += 1
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n³)`（每对节点 `O(n²)`，每次 BFS 最坏 `O(n)`）。  
- **空间复杂度**：`O(n)`，只需要邻接表、`prime` 数组和 BFS 用的 `parent` 数组。  

---

### 2. 最优解  

#### 思路  

暴力解慢的根本原因是**重复遍历同一条树枝**。在树上做 **一次深度优先遍历**，把每个子树的信息压缩成几个计数，就可以在 **线性时间** 内得到答案。  

关键点在于**“从某个节点往下走，路径中出现 0/1 个素数的节点数量”**。我们用两个 DP 值：

* `dp0[u]` – 以 `u` 为起点、向下走（只能往子树方向），且路径上**没有素数**的节点数。  
* `dp1[u]` – 以 `u` 为起点、向下走，且路径上**恰好有一个素数**的节点数。  

> **类比**：想象 `u` 是一座山的山脚，`dp0` 是从山脚往上爬而不碰到“危险岩石”（素数）的路线数，`dp1` 是恰好碰到一块岩石一次的路线数。

**状态转移**（对每个子节点 `v`）  

| `u` 是否为素数 | `dp0[u]` 计算方式 | `dp1[u]` 计算方式 |
|----------------|-------------------|-------------------|
| **非素数**      | `dp0[u] = 1 + Σ dp0[v]`（自己算作一条长度为 0 的合法路径）| `dp1[u] = Σ dp1[v]` |
| **素数**        | `dp0[u] = 0`（路径里已经出现素数，不能再算）| `dp1[u] = 1 + Σ dp0[v]`（自己算作一条只含自身素数的路径，或者子树里没有素数的路径） |

**计数合法路径**  
我们需要统计 **unordered** 节点对 `(a, b)`，且它们的最近公共祖先（LCA）为 `u`，路径上恰好出现 1 个素数。分两种情况：

1. **`u` 本身是素数**  
   - 这唯一的素数就在 LCA 上。两边都必须**没有**素数。  
   - 设 `cnt0 = Σ dp0[v]`（所有子树里不含素数的节点数）。  
   - 以 `u` 为端点的合法路径有 `cnt0` 条（`(u, x)`，`x` 来自子树且不含素数）。  
   - 两端都在子树里的合法路径有 `C(cnt0, 2) = cnt0·(cnt0‑1)/2` 条（任选两棵子树中的节点）。  
   - **贡献** = `cnt0 + C(cnt0, 2)`。

2. **`u` 不是素数**  
   - 素数一定在 **左侧** 或 **右侧** 的某一条子树路径上。  
   - 设 `cnt0 = Σ dp0[v]`、`cnt1 = Σ dp1[v]`。  
   - 以 `u` 为端点的合法路径是 `cnt1` 条（从 `u` 往下走恰好出现一次素数）。  
   - 两端都在子树里，且素数只在其中 **一侧**：我们需要把不同子树的 `dp0` 与 `dp1` 交叉配对。  
     - 具体做法：遍历子树，维护前缀和 `pre0`、`pre1`。对于当前子树 `(c0, c1)`，新增的跨子树合法对数为 `c0·pre1 + c1·pre0`。  
   - **贡献** = `cnt1 + Σ (c0·pre1 + c1·pre0)`。

在一次 DFS 中，我们既能得到 `dp0/ dp1`，也能把上述贡献累加到全局答案 `ans`。整个过程只遍历每条边一次，时间 **O(n)**，空间 **O(n)**（递归栈 + DP 数组）。

#### 代码（Python）

```python
import sys
sys.setrecursionlimit(2 * 10**5)

def sieve_primes(limit: int) -> list[bool]:
    """埃氏筛，返回 [0..limit] 是否为素数的布尔数组"""
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(limit ** 0.5) + 1):
        if is_prime[p]:
            step = p
            start = p * p
            for multiple in range(start, limit + 1, step):
                is_prime[multiple] = False
    return is_prime

def count_valid_paths(n: int, edges: list[list[int]]) -> int:
    # 1️⃣ 建图（下标从 1 开始）
    adj = [[] for _ in range(n + 1)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    # 2️⃣ 预处理素数表
    prime = sieve_primes(n)

    # 3️⃣ DP 数组 + 全局答案
    dp0 = [0] * (n + 1)   # 0 素数的垂直路径数量
    dp1 = [0] * (n + 1)   # 1 素数的垂直路径数量
    ans = 0               # 最终合法 unordered 对数

    def dfs(u: int, parent: int) -> None:
        nonlocal ans
        # 先遍历子树，收集子节点的 dp 值
        child_vals = []   # 保存每个子树的 (c0, c1) 方便后面合并
        for v in adj[u]:
            if v == parent:
                continue
            dfs(v, u)
            child_vals.append((dp0[v], dp1[v]))

        # ---------- 计算 dp0[u]、dp1[u] ----------
        if prime[u]:
            # u 本身是素数，路径里已经出现 1 个素数
            dp0[u] = 0
            dp1[u] = 1                     # 只含自身的长度 0 路径
            for c0, _ in child_vals:
                dp1[u] += c0               # 子树中不含素数的路径 + u 这颗素数
        else:
            # u 不是素数
            dp0[u] = 1                     # 长度 0 的路径（只含 u）
            dp1[u] = 0
            for c0, c1 in child_vals:
                dp0[u] += c0
                dp1[u] += c1

        # ---------- 统计以 u 为 LCA 的合法 unordered 对 ----------
        if prime[u]:
            # 素数在 LCA 上，只能两侧都不含素数
            cnt0 = sum(c0 for c0, _ in child_vals)   # 所有子树里不含素数的节点数
            # (u, x) 这种以 u 为端点的路径
            ans += cnt0
            # 两端都在子树里的路径：从不同子树各选一个
            ans += cnt0 * (cnt0 - 1) // 2
        else:
            # u 不是素数，素数必须出现于恰好一侧
            cnt0 = sum(c0 for c0, _ in child_vals)
            cnt1 = sum(c1 for _, c1 in child_vals)

            # 以 u 为端点的路径（必然走向含 1 素数的子树）
            ans += cnt1

            # 跨子树的路径：一侧 0 素数，另一侧 1 素数
            pre0 = pre1 = 0
            for c0, c1 in child_vals:
                ans += c0 * pre1 + c1 * pre0   # 与之前子树的配对
                pre0 += c0
                pre1 += c1

    # 任意选 1 号节点做根
    dfs(1, 0)
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 埃氏筛 `O(n log log n)`（在 10⁵ 范围内可以视作线性）。  
  - DFS 只遍历每条边一次，所有合并、计数都是常数时间操作。  
  - 与暴力的 `O(n²)` 相比，数量级下降了好几百倍，轻松跑满 `10⁵` 的数据。

- **空间复杂度**：`O(n)`  
  - 邻接表、`dp0/ dp1`、递归栈共 `n` 级别的存储。  
  - 与暴力的 `O(n)` 相同，但不需要额外的 `O(n²)` 辅助结构。

---

## 心得  

- **核心技巧**：在树上用**自底向上的 DP**统计“以节点为根的路径中素数出现次数”。  
- **适用场景**：  
  1. 计数满足某种“出现次数恰好 k 次”的路径，如 “恰好包含 1 条红色边的路径”。  
  2. “以 LCA 为中心，左右两侧属性满足特定组合”的计数问题，例如 “路径上奇数个节点”。  
- **一句话总结**：  
  > 把“路径上出现多少素数”压缩进每个子树的两类计数（0 个、1 个），再在父节点处交叉配对即可一次遍历得到所有合法路径。

---

## 反思  

- **第一反应**：直接枚举所有点对，跑 BFS 检查素数个数——因为这最符合直觉。  
- **最容易踩的坑**  
  1. **素数判断**：在大范围（10⁵）内频繁调用 `is_prime` 会导致超时，必须预处理一次。  
  2. **计数溢出**：答案可能超过 32 位整数，需要使用 Python 的大整数或 `long long`（在 C++ 中）。  
  3. **跨子树配对的重复计数**：若不使用前缀和技巧，会把同一对子树配对多算几次。  
- **下次思路**：  
  1. 先想 **能否把路径属性（素数出现次数）压缩成子树信息**。  
  2. 再考虑 **LCA 为中心的配对**——这往往能把 “全局配对” 转化为 “局部合并”。  

这样一步步从暴力到 DP，就能把原本 `O(n²)`（甚至 `O(n³)`）的暴力解，提升到 `O(n)` 的最优解。祝你玩转树上计数题目！