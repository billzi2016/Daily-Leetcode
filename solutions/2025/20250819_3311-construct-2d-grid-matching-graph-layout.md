# #3311. 构造匹配图布局的二维网格 / Construct 2D Grid Matching Graph Layout

> 难度：困难 · 标签：Array、Hash Table、Graph、Matrix · [LeetCode 链接](https://leetcode.com/problems/construct-2d-grid-matching-graph-layout/)

---

## 题目（英文原版）

**Description**

You are given a 2D integer array edges representing an undirected graph having n nodes, where edges[i] = [ui, vi] denotes an edge between nodes ui and vi.
Construct a 2D grid that satisfies these conditions:
It is guaranteed that edges can form a 2D grid that satisfies the conditions.
Return a 2D integer array satisfying the conditions above. If there are multiple solutions, return any of them.

**Examples**

**Example 1:**

```
Input: n = 4, edges = [[0,1],[0,2],[1,3],[2,3]]
Output: [[3,1],[2,0]]
Explanation:
```

**Example 2:**

```
Input: n = 5, edges = [[0,1],[1,3],[2,3],[2,4]]
Output: [[4,2,3,1,0]]
Explanation:
```

**Example 3:**

```
Input: n = 9, edges = [[0,1],[0,4],[0,5],[1,7],[2,3],[2,4],[2,5],[3,6],[4,6],[4,7],[6,8],[7,8]]
Output: [[8,6,3],[7,4,2],[1,0,5]]
Explanation:
```

**Constraints**

- 2 <= n <= 5 * 104
- 1 <= edges.length <= 105
- edges[i] = [ui, vi]
- 0 <= ui < vi < n
- All the edges are distinct.
- The input is generated such that edges can form a 2D grid that satisfies the conditions.

---

## 题目（中文翻译）

你得到一个二维整数数组 `edges`，它表示一个拥有 `n` 个节点的无向图（undirected graph），其中 `edges[i] = [ui, vi]` 表示节点 `ui` 与节点 `vi` 之间存在一条边。

请构造一个满足下列条件的二维网格（2D grid）：

* 保证给出的 `edges` 能够形成满足条件的二维网格。
* 返回一个满足上述条件的二维整数数组。如果存在多个解，返回任意一个即可。

---

### 示例 1
**输入**  
`n = 4, edges = [[0,1],[0,2],[1,3],[2,3]]`

**输出**  
`[[3,1],[2,0]]`

**解释**：

（此处可自行补充解释）

---

### 示例 2
**输入**  
`n = 5, edges = [[0,1],[1,3],[2,3],[2,4]]`

**输出**  
`[[4,2,3,1,0]]`

**解释**：

（此处可自行补充解释）

---

### 示例 3
**输入**  
`n = 9, edges = [[0,1],[0,4],[0,5],[1,7],[2,3],[2,4],[2,5],[3,6],[4,6],[4,7],[6,8],[7,8]]`

**输出**  
`[[8,6,3],[7,4,2],[1,0,5]]`

**解释**：

（此处可自行补充解释）

---

## 约束条件
- `2 <= n <= 5 * 10^4`
- `1 <= edges.length <= 10^5`
- `edges[i] = [ui, vi]`
- `0 <= ui < vi < n`
- 所有的边均互不相同。
- 输入数据保证 `edges` 能形成满足条件的二维网格。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有节点都排进一个矩形的格子里**，然后把每一种可能的排法全部尝试一遍，看看哪一种能把题目给出的所有无向边都对应上。

- **数据结构**  
  - `grid`：二维列表，类似一张纸上的格子。把每个节点的编号写进格子里。  
  - `set(edges)`：把所有边放进集合，查询时就像查字典一样快，`(u,v)` 或 `(v,u)` 在集合里说明这条边存在。

- **为什么能得到答案**  
  如果真的存在一种合法的网格布局，那么遍历所有可能的布局时必定会碰到这一个。只要检查到它满足每条边的相邻格子恰好是题目给出的边，就可以返回。

- **时间/空间复杂度**  
  - 枚举所有排列的数量是 `n!`（n 的阶乘），每一种排列都要检查 `|edges|` 条边。  
  - **时间复杂度**：`O(n! * |edges|)`，在最坏情况下几乎是“永远跑不完”。  
  - **空间复杂度**：`O(n²)`（存放一个 `n × n` 的网格）+ `O(|edges|)`（存放所有边），这在本题的约束下也不算大。  

> **大白话**：`n!` 就像排队买饭的所有可能顺序，人数越多，排法就多到天文数字，根本不可能把它们全列出来。

#### 代码（Python）

```python
from itertools import permutations
from collections import defaultdict

def construct_grid_bruteforce(n, edges):
    # 把所有边放进集合，查找时像查字典一样 O(1)
    edge_set = {tuple(sorted(e)) for e in edges}

    # 先尝试所有可能的行数、列数（因为 n = rows * cols）
    for rows in range(1, n + 1):
        if n % rows:               # 只能整除的才可能是矩形
            continue
        cols = n // rows

        # 所有节点的全排列（每一种都是一种可能的排法）
        for perm in permutations(range(n)):
            # 把排列转成二维网格
            grid = [list(perm[i * cols:(i + 1) * cols]) for i in range(rows)]

            # 检查每条边是否恰好是相邻格子
            ok = True
            for u, v in edges:
                # 找到 u, v 在网格中的坐标
                found_u = found_v = False
                for i in range(rows):
                    for j in range(cols):
                        if grid[i][j] == u:
                            ui, uj = i, j
                            found_u = True
                        if grid[i][j] == v:
                            vi, vj = i, j
                            found_v = True
                # 两个点必须上下左右相邻（曼哈顿距离恰好为 1）
                if not (found_u and found_v) or abs(ui - vi) + abs(uj - vj) != 1:
                    ok = False
                    break
            if ok:
                return grid
    return []          # 题目保证一定有解，这行理论上不会执行
```

> 这段代码能够跑通小规模的例子（比如 `n ≤ 6`），但一旦 `n` 稍大就会卡死。

#### 复杂度  

- **时间复杂度**：`O(n! * |edges|)`——排列的数量指数级增长，实际不可用。  
- **空间复杂度**：`O(n²)`——存放二维网格；再加上 `O(|edges|)` 用来快速判断边是否存在。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**枚举所有排列**。  
实际上，题目已经保证输入的无向图 **恰好是一张矩形网格**（每个格子只和上下左右四个格子相连）。我们只需要**利用网格的结构特征**，直接把每个节点定位到它在矩形中的坐标。

网格图的**度（degree）**有很强的规律：

| 位置 | 结点度 |
|------|--------|
| 四个角   | 2      |
| 边（非角）| 3      |
| 内部      | 4      |

> **类比**：把每个节点想成一块拼图，角块只有两条“凸起”，边块有三条，内部块有四条。只要看每块的凸起数，就能知道它到底是角、边还是内部。

利用这个规律，我们可以一步步恢复出网格：

1. **找四个角**  
   - 统计每个节点的度（邻居数），度为 `2` 的恰好有四个，它们就是四个角。

2. **确定矩形的长宽**  
   - 任选一个角 `c0`（比如列表中的第一个），对它做一次 BFS，得到它到所有节点的最短距离 `dist0`（相当于在网格里走的步数）。  
   - 在四个角中，距离 `c0` 最远的那个必然是对角的角 `cOpp`。两角之间的距离 `D = dist0[cOpp]` 正好等于 `(rows‑1) + (cols‑1)`（从左上走到右下要走的格子数）。  
   - 由于 `rows * cols = n`（节点总数），我们只需要遍历 `n` 的所有因子 `(rows, cols)`，找出满足 `rows‑1 + cols‑1 = D` 的那一对。题目保证一定能找到。

3. **定位左上、右上两个角**  
   - 已知 `rows` 与 `cols`，在四个角里找出距离 `c0` 为 `cols‑1` 的角，它就是 **左上 → 右上** 的水平方向上的角，记为 `cTopRight`。  
   - 同理，距离 `c0` 为 `rows‑1` 的角是 **左上 → 左下** 的垂直方向上的角，记为 `cBottomLeft`。  

4. **用两次 BFS 同时确定行列坐标**  
   - 再对 `cTopRight` 做一次 BFS，得到 `distTR`（左上角到每个节点的水平+垂直距离）。  
   - 对于任意节点 `x`，设  
     - `d0 = dist0[x]`  = `row + col`（从左上走到 `x` 的曼哈顿距离）  
     - `d1 = distTR[x]` = `row + (cols‑1‑col)`（从右上走到 `x` 的曼哈顿距离）  
   - 两式相加消掉 `col`，得到行号  
     \[
     row = \frac{d0 + d1 - (cols-1)}{2}
     \]  
     再用 `col = d0 - row` 求出列号。  
   - 由于所有距离都是整数，上式的除以 2 必然整除。

5. **填表**  
   - 建立 `rows × cols` 的空矩阵 `ans`，把每个节点 `x` 放到 `ans[row][col]`。  
   - 最后返回 `ans` 即可。

整个过程只用了两次 BFS（线性时间），并且所有的计算都是整数运算，完全满足 `n ≤ 5·10⁴` 的规模。

#### 代码（Python）

```python
from collections import deque, defaultdict
from math import isqrt

def construct_grid(n, edges):
    # ---------- 1. 建图 & 统计度 ----------
    g = [[] for _ in range(n)]
    deg = [0] * n
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)
        deg[u] += 1
        deg[v] += 1

    # ---------- 2. 找四个角（度为 2 的点） ----------
    corners = [i for i, d in enumerate(deg) if d == 2]   # 必然有 4 个
    c0 = corners[0]                                     # 随便选一个作为左上角

    # ---------- 3. BFS 从左上角得到所有距离 ----------
    def bfs(start):
        dist = [-1] * n
        q = deque([start])
        dist[start] = 0
        while q:
            cur = q.popleft()
            for nb in g[cur]:
                if dist[nb] == -1:
                    dist[nb] = dist[cur] + 1
                    q.append(nb)
        return dist

    dist0 = bfs(c0)

    # ---------- 4. 确定对角角以及矩形的长宽 ----------
    # 对角角是距离最远的角
    cOpp = max(corners, key=lambda x: dist0[x])
    D = dist0[cOpp]                       # = (rows-1) + (cols-1)

    # 枚举 n 的因子找满足 D = (r-1)+(c-1) 的 (rows, cols)
    rows, cols = None, None
    for r in range(1, isqrt(n) + 1):
        if n % r:               # 不是因子
            continue
        c = n // r
        if (r - 1) + (c - 1) == D:
            rows, cols = r, c
            break
        if (c - 1) + (r - 1) == D:   # 交换也行
            rows, cols = c, r
            break
    # 题目保证一定能找到，下面的代码可以省去异常判断

    # ---------- 5. 确定左上 → 右上 的角 ----------
    # 距离为 cols-1 的角一定是同一行的右上角
    cTopRight = None
    for cor in corners:
        if cor != c0 and dist0[cor] == cols - 1:
            cTopRight = cor
            break

    # ---------- 6. 再做一次 BFS（从右上角） ----------
    distTR = bfs(cTopRight)

    # ---------- 7. 根据公式恢复 (row, col) ----------
    ans = [[-1] * cols for _ in range(rows)]
    for node in range(n):
        d0 = dist0[node]
        d1 = distTR[node]
        # 行号
        row = (d0 + d1 - (cols - 1)) // 2
        # 列号
        col = d0 - row
        ans[row][col] = node

    return ans
```

**代码要点说明（带中文注释）**

```python
def bfs(start):
    """从 start 出发的普通 BFS，返回每个节点到 start 的最短距离"""
    dist = [-1] * n               # -1 表示未访问
    q = deque([start])
    dist[start] = 0
    while q:
        cur = q.popleft()
        for nb in g[cur]:
            if dist[nb] == -1:    # 只访问一次，保证 O(N+M)
                dist[nb] = dist[cur] + 1
                q.append(nb)
    return dist
```

- **找角**：度为 2 的节点就像四个“只连两条路的拐角”。  
- **确定行列**：把 `n` 分解成因子，然后挑出满足“对角距离 = (行‑1)+(列‑1)”的那一对。  
- **坐标公式**：`row = (d0 + d1 - (cols-1)) / 2`，背后的原理是 **曼哈顿距离的加减消元**，把水平距离 `col` 消掉，只剩行号。  

#### 复杂度  

- **时间复杂度**：`O(n + m)`  
  - 两次 BFS 各遍历所有节点和边，`m = len(edges)`。  
  - 枚举因子最多 `O(√n)`，对本题规模来说可以忽略不计。  
  - 与暴力解的 `O(n! )` 相比，线性时间几乎瞬间完成。

- **空间复杂度**：`O(n + m)`  
  - `g`（邻接表）存储所有边，`dist0`、`distTR` 两个距离数组各 `O(n)`。  
  - 最终的答案矩阵 `rows × cols = n` 也在同一数量级。

---

## 心得  

- **核心技巧**：**利用网格图的度数特征（角 2、边 3、内部 4）定位四个角，再用两次 BFS 的曼哈顿距离求出每个节点的行列坐标。**  
- **适用的题型**  
  1. “给定无向图，恢复它是某种规则布局（如矩形、环形、树的层序）的问题”。  
  2. “根据度数或距离信息重建坐标系”的题目，例如 **恢复二维树的平面布局**。  
  3. “已知图是网格/棋盘，要求输出对应的矩阵” 的变体。  
- **一句话总结解题钥匙**：**先找角（度数最小），再用两次 BFS 把行列坐标通过距离公式算出来**。

---

## 反思  

- **第一反应**：看到“2‑D Grid”和“edges”，立刻想到把图画出来，检查每个节点的相邻数目——这提示它是网格。  
- **最容易踩的坑**  
  1. **忘记考虑矩形的长宽顺序**：`rows` 与 `cols` 可能互换，需要遍历所有因子。  
  2. **除法取整**：行号公式中的除以 2 必须是整数，若实现时使用浮点数会出现精度问题。  
  3. **特殊的 “细长” 矩形**（比如 1 × n），此时角的度数仍为 2，算法仍然适用，但要确保 BFS 距离匹配公式。  
- **下次遇到同类题**，第一步应该**统计每个节点的度数，寻找度数最小的点（角/端点）**，再**利用最短路径距离把坐标逐步恢复**。这样可以把搜索空间从指数级压到线性级。