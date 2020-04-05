# #827. 构造最大岛屿 / Making A Large Island

> 难度：困难 · 标签：Array、Depth-First Search、Breadth-First Search、Union Find、Matrix · [LeetCode 链接](https://leetcode.com/problems/making-a-large-island/)

---

## 题目（英文原版）

**Description**

You are given an n x n binary matrix grid. You are allowed to change at most one 0 to be 1.
Return the size of the largest island in grid after applying this operation.
An island is a 4-directionally connected group of 1s.

**Examples**

**Example 1:**

```
Input: grid = [[1,0],[0,1]]
Output: 3
Explanation: Change one 0 to 1 and connect two 1s, then we get an island with area = 3.
```

**Example 2:**

```
Input: grid = [[1,1],[1,0]]
Output: 4
Explanation: Change the 0 to 1 and make the island bigger, only one island with area = 4.
```

**Example 3:**

```
Input: grid = [[1,1],[1,1]]
Output: 4
Explanation: Can't change any 0 to 1, only one island with area = 4.
```

**Constraints**

- n == grid.length
- n == grid[i].length
- 1 <= n <= 500
- grid[i][j] is either 0 or 1.

---

## 题目（中文翻译）

给定一个 **n × n 的二进制矩阵** `grid`。你最多可以将一个 `0` 改为 `1`。返回在执行此操作后，矩阵中**最大岛屿**的面积。

> **岛屿**：由值为 `1` 的单元格组成，且相邻单元格必须是**四向相连（4-directionally connected）**的。

## 示例

### 示例 1
**输入**  
```text
grid = [[1,0],[0,1]]
```
**输出**  
```text
3
```
**解释**  
将一个 `0` 改成 `1`，使两个 `1` 相连，得到面积为 `3` 的岛屿。

### 示例 2
**输入**  
```text
grid = [[1,1],[1,0]]
```
**输出**  
```text
4
```
**解释**  
将唯一的 `0` 改为 `1`，岛屿面积扩大为 `4`。

### 示例 3
**输入**  
```text
grid = [[1,1],[1,1]]
```
**输出**  
```text
4
```
**解释**  
矩阵中不存在 `0` 可以翻转，唯一的岛屿面积为 `4`。

## 约束条件

- `n == grid.length`
- `n == grid[i].length`
- `1 <= n <= 500`
- `grid[i][j]` 只能是 `0` 或 `1`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是「把每一个 0 都尝试改成 1，然后重新统计整张图上最大的岛屿面积」。  
具体步骤：

1. **遍历所有格子**，找到值为 0 的位置。  
2. **把这个 0 暂时改成 1**（相当于我们在这块“海”上建了一座桥）。  
3. **从头到尾扫描整张矩阵**，用 **DFS（深度优先搜索）** 或 **BFS（广度优先搜索）** 把相连的 1 标记为同一个岛屿，并统计该岛屿的面积。  
4. 记录本次尝试得到的最大面积。  
5. **恢复原来的 0**，继续尝试下一个位置。  

> **数据结构类比**  
> - **栈 / 队列**：DFS 用栈（递归实现时是系统调用栈），BFS 用队列。想象你在迷宫里走，栈是「回头路」的记忆，队列是「先来后到」的排队。  
> - **矩阵**：就像一张城市地图，格子里是「陆地」(1) 或「海水」(0)。  

**为什么正确**  
因为我们穷举了所有可能的「改一个 0 为 1」的情况，并且每次都完整地计算了改动后的岛屿面积。只要遍历到所有零，最大值一定会被找出来。

**时间/空间复杂度**  

- **时间**：设矩阵大小为 `n × n`，零的个数最坏是 `n²`。每次把一个零改成 1 后，需要一次完整的 DFS/BFS，遍历所有格子，时间是 `O(n²)`。所以总时间是 `O(n² × n²) = O(n⁴)`。  
  - **大白话**：如果 `n = 100`，那最坏情况下要跑 `100⁴ = 100,000,000` 次基本操作，明显会超时。  

- **空间**：DFS 递归栈（或 BFS 队列）最深会到整个矩阵的格子数 `O(n²)`，其余只用常数级别的变量。  

#### 代码（Python）

```python
from collections import deque
from copy import deepcopy
from typing import List

def max_island_bruteforce(grid: List[List[int]]) -> int:
    n = len(grid)
    # 四个方向：上、下、左、右
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # -------------------------------------------------
    # 计算当前矩阵中所有岛屿的最大面积（不改动任何格子）
    # -------------------------------------------------
    def bfs(r: int, c: int, g: List[List[int]]) -> int:
        """从 (r,c) 开始 BFS，返回该岛屿的面积"""
        q = deque()
        q.append((r, c))
        g[r][c] = -1               # -1 表示已经访问过
        area = 1
        while q:
            x, y = q.popleft()
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < n and g[nx][ny] == 1:
                    g[nx][ny] = -1
                    q.append((nx, ny))
                    area += 1
        return area

    # -------------------------------------------------
    # 主循环：尝试把每一个 0 改成 1
    # -------------------------------------------------
    best = 0
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 0:                     # 只对 0 进行尝试
                # 复制一份矩阵，防止把原始数据弄坏
                tmp = deepcopy(grid)
                tmp[i][j] = 1                       # 把当前的 0 变成 1

                # 统计这张新矩阵的最大岛屿面积
                cur_max = 0
                for x in range(n):
                    for y in range(n):
                        if tmp[x][y] == 1:         # 发现未访问的陆地
                            cur_max = max(cur_max, bfs(x, y, tmp))
                best = max(best, cur_max)

    # 如果整个矩阵本来就全是 1，根本没有 0 可改，直接返回原始最大面积
    if best == 0:               # 没有任何 0 被尝试过
        # 只需要一次遍历算一次面积
        tmp = deepcopy(grid)
        for i in range(n):
            for j in range(n):
                if tmp[i][j] == 1:
                    best = max(best, bfs(i, j, tmp))
    return best
```

#### 复杂度  

- **时间复杂度**：`O(n⁴)`  
  - 解释：每个 0（最坏 `n²` 个）都要跑一次遍历整个矩阵的 DFS/BFS（`O(n²)`），两者相乘就是 `O(n⁴)`。  
- **空间复杂度**：`O(n²)`  
  - 解释：复制矩阵需要 `n²` 的额外空间，DFS/BFS 的递归栈或队列同样最多存 `n²` 个坐标。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在 **「每次都要重新遍历整张矩阵」**。  
我们可以把这一步提前完成：**先把所有已有的岛屿编号并记录每个岛屿的面积**，这样在后面只需要 **查看相邻的几个岛屿**，就能快速算出把某个 0 变成 1 后得到的总面积。

关键步骤如下：

1. **一次遍历，把所有岛屿「贴标签」**  
   - 用 **DFS/BFS** 把相连的 1 标记为同一个编号（从 2 开始，避免和原始的 0/1 冲突）。  
   - 同时把 **编号 → 面积** 的映射存进哈希表 `area[id]`。  
   - 类比：把城市地图上的每块连在一起的陆地「贴上邮编」并记下这个邮编对应的「土地面积」。  

2. **遍历所有 0，尝试把它变成 1**  
   - 看它四个方向上有哪些不同的岛屿编号（使用 `set` 去重，防止同一个岛屿被算两次）。  
   - 把这些相邻岛屿的面积相加，再加上自己这块新土地的 1，得到 **该位置改为 1 后的岛屿面积**。  
   - 记录所有位置中的最大值。  

3. **特殊情况**  
   - 如果原始矩阵全是 1，说明根本没有 0 可改，答案就是 `n*n`（整个矩阵本身就是最大岛屿）。  

> **数据结构解释**  
> - **哈希表（dict）**：就像一本「邮编手册」，key 是岛屿的编号，value 是对应的面积。查找时间几乎是 **O(1)**，也就是“一眼就能看到”。  
> - **集合（set）**：用于存放相邻的岛屿编号，自动去重，防止同一个岛屿被多次计入面积。  

**为什么更快**  
- **标记阶段只遍历一次**：把所有岛屿的面积算好，后面不需要再遍历整张矩阵。  
- **每个 0 只看最多 4 个邻居**：所以每个 0 的计算是 **O(1)**，整个过程是 **O(n²)**。  

#### 代码（Python）

```python
from collections import deque
from typing import List

def largestIsland(grid: List[List[int]]) -> int:
    n = len(grid)
    # 四个方向：上、下、左、右
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # ---------- 第一步：给每个岛屿编号并记录面积 ----------
    island_id = 2               # 从 2 开始，避免和 0/1 冲突
    area = {}                   # key: island_id, value: 面积

    def bfs(r: int, c: int, idx: int) -> int:
        """把以 (r,c) 为起点的岛屿标记为 idx，返回该岛屿面积"""
        q = deque()
        q.append((r, c))
        grid[r][c] = idx
        cnt = 1
        while q:
            x, y = q.popleft()
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] == 1:
                    grid[nx][ny] = idx
                    q.append((nx, ny))
                    cnt += 1
        return cnt

    for i in range(n):
        for j in range(n):
            if grid[i][j] == 1:               # 发现未标记的陆地
                cur_area = bfs(i, j, island_id)
                area[island_id] = cur_area
                island_id += 1

    # ---------- 第二步：尝试把每个 0 变成 1 ----------
    ans = max(area.values(), default=0)   # 可能原来就已经有最大的岛屿

    for i in range(n):
        for j in range(n):
            if grid[i][j] == 0:
                neighbor_ids = set()
                for dx, dy in dirs:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < n and 0 <= nj < n and grid[ni][nj] > 1:
                        neighbor_ids.add(grid[ni][nj])
                # 把相邻岛屿面积相加，再加上自己这块土地
                new_area = 1 + sum(area[idx] for idx in neighbor_ids)
                ans = max(ans, new_area)

    # ---------- 第三步：全是 1 的特殊情况 ----------
    # 如果没有 0，ans 已经是所有岛屿的最大面积（即 n*n）
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 解释：  
    1. 第一次遍历（标记岛屿）每个格子最多被访问一次 → `O(n²)`。  
    2. 第二次遍历（检查 0 的邻居）每个格子也只看常数个方向 → `O(n²)`。  
    两次遍历相加仍是 `O(n²)`，远快于暴力的 `O(n⁴)`。  

- **空间复杂度**：`O(n²)`（用于存放 `grid` 本身的标记） + `O(k)`（`k` 为岛屿数量，最坏 `k ≤ n²/2`），整体仍是 `O(n²)`。  
  - 解释：我们使用了一个额外的哈希表 `area`（最多存 `n²` 条记录）和 BFS 队列，最大空间和矩阵本身同阶。  

---

## 心得  

- **核心技巧**：先把所有已有的连通块（岛屿）**预处理**（编号 + 记录面积），再利用**局部信息**（相邻岛屿编号）快速计算「改一个格子」的结果。  
- **适用的题型**（类似思路）  
  1. **“岛屿的最大面积”**（只统计已有岛屿，不改格子）  
  2. **“最多可以连接多少块土地”**（把若干 0 同时变成 1）  
  3. **“最小岛屿翻转次数”**（把 0 变成 1 使所有 1 连通）  

- **一句话总结解题钥匙**：**“先把原有结构全部弄清楚，再只看改动点的局部影响”。**  

---

## 反思  

- **第一反应**：把每个 0 都改成 1，然后全图重新搜索最大岛屿——这就是暴力思路。  
- **最容易踩的坑**  
  1. **重复计数**：一个 0 周围可能有多个相同岛屿的格子，若不去重会把同一个岛屿面积算多次。使用 `set` 去重是关键。  
  2. **全 1 的矩阵**：没有 0 可改时，需要直接返回 `n*n`（或已有最大面积），否则会错误返回 1。  
  3. **编号冲突**：如果直接把岛屿标记为 1，会把原始的 1 和新标记混在一起。把编号从 2 开始可以避免冲突。  

- **下次遇到同类题的第一步**：**“先把原图的连通块信息全部收集（编号 + 属性）”，再在此基础上局部尝试改动”。**这样可以把原本的 `O(n⁴)` 暴力压到 `O(n²)`，大幅提升效率。