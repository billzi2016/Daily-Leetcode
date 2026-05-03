# #3615. 图中最长回文路径 / Longest Palindromic Path in Graph

> 难度：困难 · 标签：String、Dynamic Programming、Bit Manipulation、Graph、Bitmask · [LeetCode 链接](https://leetcode.com/problems/longest-palindromic-path-in-graph/)

---

## 题目（英文原版）

**Description**

You are given an integer n and an undirected graph with n nodes labeled from 0 to n - 1 and a 2D array edges, where edges[i] = [ui, vi] indicates an edge between nodes ui and vi.
You are also given a string label of length n, where label[i] is the character associated with node i.
You may start at any node and move to any adjacent node, visiting each node at most once.
Return the maximum possible length of a palindrome that can be formed by visiting a set of unique nodes along a valid path.

**Examples**

**Example 1:**

```
Input: n = 3, edges = [[0,1],[1,2]], label = "aba"
Output: 3
Exp lanation:
```

**Example 2:**

```
Input: n = 3, edges = [[0,1],[0,2]], label = "abc"
Output: 1
Explanation:
```

**Example 3:**

```
Input: n = 4, edges = [[0,2],[0,3],[3,1]], label = "bbac"
Output: 3
Explanation:
```

**Constraints**

- 1 <= n <= 14
- n - 1 <= edges.length <= n * (n - 1) / 2
- edges[i] == [ui, vi]
- 0 <= ui, vi <= n - 1
- ui != vi
- label.length == n
- label consists of lowercase English letters.
- There are no duplicate edges.

---

## 题目（中文翻译）

**描述**  
给定一个整数 `n` 和一个 **无向图（undirected graph）**，该图包含 `n` 个节点，节点编号为 `0` 到 `n‑1`，以及一个二维数组 `edges`，其中 `edges[i] = [ui, vi]` 表示节点 `ui` 与节点 `vi` 之间存在一条边。  
同时给定一个长度为 `n` 的字符串 `label`，其中 `label[i]` 是与节点 `i` 关联的字符。  

你可以从任意节点出发，沿着相邻节点移动，每个节点至多访问一次。返回在一条合法路径上访问的一组唯一节点所能形成的回文串的最大可能长度。

**示例 1**  
```
Input: n = 3, edges = [[0,1],[1,2]], label = "aba"
Output: 3
Explanation: 
```

**示例 2**  
```
Input: n = 3, edges = [[0,1],[0,2]], label = "abc"
Output: 1
Explanation: 
```

**示例 3**  
```
Input: n = 4, edges = [[0,2],[0,3],[3,1]], label = "bbac"
Output: 3
Explanation: 
```

**约束条件**  
- `1 <= n <= 14`  
- `n - 1 <= edges.length <= n * (n - 1) / 2`  
- `edges[i] == [ui, vi]`  
- `0 <= ui, vi <= n - 1`  
- `ui != vi`  
- `label.length == n`  
- `label` 仅由小写英文字母组成。  
- 不存在重复的边。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有可能的简单路径**（即每个节点至多走一次）都枚举一遍，然后把路径上经过的节点对应的字符拼成字符串，检查它是不是回文，记录最长的长度。

- **枚举路径**：可以用深度优先搜索（DFS）从每个起点出发，递归地走到相邻的未访问节点。递归的状态只需要记住  
  - 当前所在的节点 `u`  
  - 已经访问过的节点集合 `mask`（用二进制位表示，第 i 位是 1 表示节点 i 已经走过）  
  - 当前路径对应的字符序列 `path`（用 Python 的列表保存，最后再拼成字符串）。
- **回文检查**：把 `path` 拼成字符串 `s`，判断 `s == s[::-1]`（即正着读和反着读相同）。如果是回文，就用 `len(s)` 更新答案。

> **生活化类比**：  
> 想象你在一座城堡里走迷宫，城堡的每个房间都有一块字母石碑。你只能每个房间进一次，走完后把看到的字母排成一串，看看能不能正着读、反着读都一样。暴力解就是把所有可能的走法全部写下来，逐个检查。

**为什么这个方法一定能得到正确答案**  
因为我们枚举了**所有**合法的路径，且每条路径都严格满足「不重复访问」的限制。只要路径对应的字符序列是回文，就会被记录；最终的最大长度必然是所有合法回文路径长度的上界。

#### 代码（Python）

```python
from typing import List

def longestPalindromePath_bruteforce(n: int, edges: List[List[int]], label: str) -> int:
    # 建图：邻接表，方便遍历相邻节点
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)

    ans = 0                     # 当前找到的最长回文长度

    def dfs(u: int, mask: int, path: List[str]) -> None:
        """从节点 u 出发，mask 表示已访问节点，path 保存走过的字符"""
        nonlocal ans
        # 把当前路径拼成字符串，检查是否是回文
        s = ''.join(path)
        if s == s[::-1]:        # 回文判断
            ans = max(ans, len(s))

        # 继续向相邻且未访问的节点扩展
        for v in g[u]:
            if not (mask >> v) & 1:      # v 还没有被访问
                path.append(label[v])    # 记录字符
                dfs(v, mask | (1 << v), path)
                path.pop()                # 回溯，撤销字符

    # 从每个节点作为起点开始搜索
    for start in range(n):
        dfs(start, 1 << start, [label[start]])

    return ans
```

> **关键行注释**  
> - `mask | (1 << v)` 把第 v 位设为 1，表示「已经访问了节点 v」  
> - `path.append(label[v]) / path.pop()` 实现「走进」和「走出」一个节点的回溯

#### 复杂度

- **时间复杂度**：`O(n! )`（阶乘级）  
  在最坏情况下（图是完全图），从任意起点可以访问的顺序是 `n-1`、`n-2`、…、`1`，相当于全排列的数量。对每条路径我们还要做一次 `O(n)` 的回文判断，整体是指数级甚至阶乘级的增长。  
  用大白话说，就是**随节点数增长，跑得非常慢，几秒钟能跑完的 n 只能到 10 左右**。
- **空间复杂度**：`O(n)`（递归栈 + 当前路径）  
  递归深度最多 `n`，路径列表最多保存 `n` 个字符。

---

### 2. 最优解

#### 思路  

因为 **n ≤ 14**，我们可以把「已经访问的节点集合」用 **位掩码（bitmask）** 紧凑地表示，随后在**状态压缩动态规划**中枚举所有可能的子集。  

**核心观察**  
- 回文的两端字符必须相等。我们可以把构造过程想成「从两端向中间收敛」：  
  - 维护当前已经形成的回文的左端点 `l`、右端点 `r`（这两个节点一定已经在 `mask` 中）。  
  - 若想继续扩展，就需要找 **两个新的未使用的节点** `u`、`v`，满足  
    1. `u` 与 `l` 相邻，`v` 与 `r` 相邻（只能沿图的边走）  
    2. `label[u] == label[v]`（才能保持回文）  
    3. `u`、`v` 均不在 `mask` 中（不能重复访问）  
  - 把 `u`、`v` 加入集合，新的左、右端点分别变成 `u`、`v`，回文长度+2。

- 当左端点和右端点重合 (`l == r`) 时，说明回文长度是奇数；此时我们可以再尝试把一个未使用的节点 `c` 加到中间，只要它与当前端点相连且字符任意（因为单独一个字符总是回文），长度+1。

**状态定义**  
`dp[mask][l][r] = 当前已经使用的节点集合为 mask，左端点是 l，右端点是 r 时，能够得到的最大回文长度。`  
- `mask`：`0 … (1<<n)-1`（最多 2^14 = 16384 种）  
- `l, r`：`0 … n-1`（最多 14×14 = 196 种）  

**初始化**  
1. 单个节点本身就是长度为 1 的回文：`dp[1<<i][i][i] = 1`。  
2. 两个相邻且字符相同的节点可以直接构成长度为 2 的回文：如果 `i` 与 `j` 有边且 `label[i]==label[j]`，则 `dp[(1<<i)|(1<<j)][i][j] = 2`。

**转移**  
对每个已经有值的状态 `(mask, l, r)`，尝试把一对新端点加入：

```
for u in neighbors[l]:
    if (mask >> u) & 1: continue          # u 已经被使用
    for v in neighbors[r]:
        if (mask >> v) & 1: continue      # v 已经被使用
        if label[u] != label[v]: continue # 必须字符相同
        new_mask = mask | (1<<u) | (1<<v)
        dp[new_mask][u][v] = max(dp[new_mask][u][v], dp[mask][l][r] + 2)
```

**奇数长度的中心**（可选）  
如果 `l == r`（当前回文长度是奇数），我们还能把一个未使用的相邻节点 `c` 放在中间：

```
for c in neighbors[l]:
    if (mask >> c) & 1: continue
    new_mask = mask | (1<<c)
    dp[new_mask][c][c] = max(dp[new_mask][c][c], dp[mask][l][r] + 1)
```

**答案**  
遍历所有 `dp` 表中的值，取最大即可。

**为什么比暴力快**  
- **状态压缩**：每个子集只会被处理一次，而不是对每条路径都重新遍历。  
- **只在两端扩展**：我们不需要关心路径中间的顺序，只要左右两端匹配即可，大幅剪枝。  
- **位运算**检查「是否已访问」是 O(1) 的操作。  
- 整体状态数是 `2^n * n * n ≈ 16384 * 14 * 14 ≈ 3.2e6`，每个状态的转移最多遍历相邻节点（度 ≤ n），所以时间在几千万次级别，完全可以在毫秒级跑完。

#### 代码（Python）

```python
from typing import List

def longestPalindromePath(n: int, edges: List[List[int]], label: str) -> int:
    # 1. 建图（邻接表），方便快速遍历相邻节点
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)

    INF_NEG = -10**9                     # 表示「不可达」的初始值
    size = 1 << n                        # 所有可能的 mask 数量

    # dp[mask][l][r] 用三维列表存，初始化为不可达
    dp = [[[INF_NEG] * n for _ in range(n)] for _ in range(size)]

    # 2. 初始化：单个节点（长度 1）和相邻相同字符的两节点（长度 2）
    for i in range(n):
        dp[1 << i][i][i] = 1             # 单点回文
    for u in range(n):
        for v in g[u]:
            if u < v and label[u] == label[v]:   # 防止重复计数
                mask = (1 << u) | (1 << v)
                dp[mask][u][v] = dp[mask][v][u] = 2   # 两端相同字符的回文

    ans = 1                               # 至少有一个字符

    # 3. 状态转移
    for mask in range(size):
        for l in range(n):
            for r in range(n):
                cur = dp[mask][l][r]
                if cur < 0:                     # 这个状态不可达，直接跳过
                    continue
                # 更新全局答案
                ans = max(ans, cur)

                # ----- 尝试扩展成长度+2 的回文（从两端各加一个） -----
                for nl in g[l]:                # 左端点的候选新节点
                    if (mask >> nl) & 1:       # 已经用过
                        continue
                    for nr in g[r]:            # 右端点的候选新节点
                        if (mask >> nr) & 1:
                            continue
                        if label[nl] != label[nr]:
                            continue           # 必须字符相同
                        new_mask = mask | (1 << nl) | (1 << nr)
                        # 更新 dp[new_mask][nl][nr]
                        if dp[new_mask][nl][nr] < cur + 2:
                            dp[new_mask][nl][nr] = cur + 2

                # ----- 奇数长度的中心扩展（只在左==右 时需要） -----
                if l == r:                     # 当前是奇数长度回文
                    for nc in g[l]:           # 把一个新节点放在中间
                        if (mask >> nc) & 1:
                            continue
                        new_mask = mask | (1 << nc)
                        if dp[new_mask][nc][nc] < cur + 1:
                            dp[new_mask][nc][nc] = cur + 1

    return ans
```

> **代码要点解释**  
> - `mask >> v & 1` 用位运算判断节点 `v` 是否已经在当前集合里。  
> - `dp` 用 `-10**9` 代表「不可达」状态，防止误把 0 当作合法长度。  
> - 两层循环 `for nl in g[l]`、`for nr in g[r]` 正是在「左端点」和「右端点」各选一个相邻节点，确保路径仍然是合法的。  
> - 当 `l == r` 时，说明回文长度是奇数，我们可以再往中间塞一个节点，长度+1。

#### 复杂度

- **时间复杂度**：`O( 2^n * n^2 * deg^2 )`  
  - `2^n` 是所有可能的节点子集数量（最多 16384）。  
  - `n^2` 来自状态表的两端点组合（最多 196）。  
  - `deg` 是图中节点的最大度数，最坏情况下 `deg ≤ n`，于是整体约为 `O(2^n * n^4)`，但实际常数很小（n ≤ 14），运行在毫秒级。  
  - 与暴力解的 `O(n!)` 相比，**指数从阶乘降到了 2 的幂**，明显快得多。

- **空间复杂度**：`O(2^n * n^2)`  
  - 需要保存所有状态的 dp 表，约 `16384 * 14 * 14 ≈ 3.2e6` 个整数，约 12 MB（完全可以接受）。

---

## 心得

- **核心技巧**：**位掩码动态规划（Bitmask DP）** + **从两端扩展构造回文**。  
- **适用的题型**（类似思路）  
  1. “Hamiltonian Path / Cycle” 这类要求遍历每个节点一次的子集 DP（例如 LeetCode 847 “Shortest Path Visiting All Nodes”）。  
  2. “Maximum Palindrome Subsequence on a Graph” 或 “Palindrome Partitioning with Graph Constraints”。  
  3. “Travelling Salesman Problem” 的小规模（n ≤ 15）实现——本质上也是位掩码 DP。  
- **一句话总结解题钥匙**：**把回文的左右端点当作状态，用未使用的节点集合（mask）记忆已走过的点，只有左右两端相等时才能继续扩展**。

---

## 反思

- **第一反应**：看到“回文 + 图 + n ≤ 14”，立刻想到 **状态压缩 DP**，因为小规模的 n 适合用位运算枚举子集。  
- **最容易踩的坑**  
  1. **重复计数**：在初始化时，两节点回文要防止把同一条边算两遍（`u < v` 条件）。  
  2. **掩码检查**：忘记在转移前判断新节点是否已经在 `mask` 中，会导致非法的「重复访问」路径。  
  3. **奇数长度的中心**：如果只实现两端扩展，会漏掉只剩一个中心节点的情况，导致答案少 1。  
- **下次遇到同类题**：第一步先判断是否可以用 **位掩码** 来描述「已使用的元素集合」；若可以，就立刻设定 **状态 = (mask, 端点信息…)**，再寻找可以从当前状态**一步步扩展**的「转移规则」。这样思路就已经清晰了。