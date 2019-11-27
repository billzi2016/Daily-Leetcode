# #675. 砍树以举办高尔夫活动 / Cut Off Trees for Golf Event

> 难度：困难 · 标签：Array、Breadth-First Search、Heap (Priority Queue)、Matrix · [LeetCode 链接](https://leetcode.com/problems/cut-off-trees-for-golf-event/)

---

## 题目（英文原版）

**Description**

You are asked to cut off all the trees in a forest for a golf event. The forest is represented as an m x n matrix. In this matrix:
In one step, you can walk in any of the four directions: north, east, south, and west. If you are standing in a cell with a tree, you can choose whether to cut it off.
You must cut off the trees in order from shortest to tallest. When you cut off a tree, the value at its cell becomes 1 (an empty cell).
Starting from the point (0, 0), return the minimum steps you need to walk to cut off all the trees. If you cannot cut off all the trees, return -1.
Note: The input is generated such that no two trees have the same height, and there is at least one tree needs to be cut off.

**Examples**

**Example 1:**

```
Input: forest = [[1,2,3],[0,0,4],[7,6,5]]
Output: 6
Explanation: Following the path above allows you to cut off the trees from shortest to tallest in 6 steps.
```

**Example 2:**

```
Input: forest = [[1,2,3],[0,0,0],[7,6,5]]
Output: -1
Explanation: The trees in the bottom row cannot be accessed as the middle row is blocked.
```

**Example 3:**

```
Input: forest = [[2,3,4],[0,0,5],[8,7,6]]
Output: 6
Explanation: You can follow the same path as Example 1 to cut off all the trees.
Note that you can cut off the first tree at (0, 0) before making any steps.
```

**Constraints**

- m == forest.length
- n == forest[i].length
- 1 <= m, n <= 50
- 0 <= forest[i][j] <= 109
- Heights of all trees are distinct.

---

## 题目（中文翻译）

**题目描述**  
给定一个由 `m × n` 矩阵（matrix）表示的森林（forest），矩阵中的每个单元格（cell）可能是：

- `0`：表示障碍物，不能通行。  
- `1`：表示空地，可以通行。  
- 大于 `1` 的整数：表示一棵树（tree），数值即为树的高度。

在一次移动中，你可以向四个方向中的任意一个移动：北（north）、东（east）、南（south）或西（west）。如果你站在一棵树所在的单元格上，可以选择将其砍倒。砍倒后，该单元格的数值会变为 `1`（空地）。

必须按照树的高度从低到高的顺序砍倒所有树。**起始位置为 `(0, 0)`**。返回完成所有砍树所需的最少步数（steps）。如果无法砍掉所有树，返回 `-1`。

> **说明**：输入保证不存在两棵树的高度相同，且至少有一棵树需要砍倒。

---

### 示例

**示例 1**  
```text
输入: forest = [[1,2,3],[0,0,4],[7,6,5]]
输出: 6
解释: 按照如下路径移动可以在 6 步内按高度从低到高砍倒所有树。
```

**示例 2**  
```text
输入: forest = [[1,2,3],[0,0,0],[7,6,5]]
输出: -1
解释: 中间一行全部为障碍物，导致无法到达底部一行的树，无法砍完所有树。
```

**示例 3**  
```text
输入: forest = [[2,3,4],[0,0,5],[8,7,6]]
输出: 6
解释: 可以沿着示例 1 中的同一路径砍掉所有树。
注意：可以先在起点 `(0, 0)` 处砍掉第一棵树，然后再开始移动。
```

---

### 约束条件
- `m == forest.length`
- `n == forest[i].length`
- `1 <= m, n <= 50`
- `0 <= forest[i][j] <= 10^9`
- 所有树的高度互不相同。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是**把所有可能的走法都列举出来**，看看哪一种能够按照树的高度从低到高依次砍掉所有树，最后取步数最少的那条路径。  

- **数据结构**  
  - **栈/递归**：用来保存“走到哪儿了、已经砍了哪些树”的状态，就像我们在玩迷宫游戏时把每一步的选择压进记事本。  
  - **二维数组**：森林本身就是一个 `m × n` 的矩阵，`forest[i][j]` 保存每个格子的高度或障碍（0 表示不能通行）。  

- **为什么正确**  
  只要把**所有合法的走法**都遍历一遍，就一定能找到一条满足“按高度顺序砍树”的路径（如果存在的话）。因为我们没有遗漏任何一步的可能性，答案一定在遍历的结果里。  

- **复杂度分析（大白话）**  
  - **时间**：每一步都有最多 4 种方向可以走，森林最多有 `m·n ≤ 2500` 个格子。要把所有走法枚举完，需要尝试的路径数是 `4^(m·n)`，这相当于 **指数级** 的增长，几乎不可能在电脑上跑完（就像把所有可能的密码都尝试一次）。我们用大写的 **O** 来表示这种“爆炸式”增长，记作 `O(4^{mn})`。  
  - **空间**：递归栈需要保存当前走到的路径，最深可能是走遍整个森林，即 `O(mn)` 的空间。  

> **提示**：虽然这种暴力搜索在理论上可以得到答案，但在实际编程面试中根本不可行，主要用来帮助我们发现“慢在哪里”。  

#### 代码（Python）  

```python
from typing import List

# 方向向量：上、下、左、右
DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def cutOffTree_bruteforce(forest: List[List[int]]) -> int:
    m, n = len(forest), len(forest[0])
    # 先把所有树的坐标和高度收集起来，方便判断是否已经全部砍完
    trees = [(i, j, forest[i][j]) for i in range(m) for j in range(n) if forest[i][j] > 1]
    trees.sort(key=lambda x: x[2])                     # 按高度升序

    # 用深度优先搜索穷举所有走法
    def dfs(x: int, y: int, idx: int, steps: int, visited) -> int:
        """
        x, y   当前所在坐标
        idx    正在准备砍第 idx 棵树（trees[idx]）
        steps  已经走的步数
        visited 已经走过的格子集合，防止原路回头形成死循环
        """
        # 所有树都砍完，返回已经走的步数
        if idx == len(trees):
            return steps

        # 目标树的位置
        tx, ty, _ = trees[idx]

        # 如果已经站在目标树上，直接砍掉，进入下一个目标
        if (x, y) == (tx, ty):
            forest[x][y] = 1          # 砍树后格子变成空地
            ans = dfs(x, y, idx + 1, steps, set())   # 重新开始记录 visited
            forest[x][y] = forest[x][y]  # 恢复现场（回溯）
            return ans

        best = float('inf')
        # 向四个方向尝试一步
        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < m and 0 <= ny < n and forest[nx][ny] != 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                cand = dfs(nx, ny, idx, steps + 1, visited)
                if cand != -1:
                    best = min(best, cand)
                visited.remove((nx, ny))

        return -1 if best == float('inf') else best

    # 从左上角 (0,0) 开始搜索
    return dfs(0, 0, 0, 0, {(0, 0)})
```

> 代码里每一行都有中文注释，帮助你快速对应思路与实现。请注意，这段代码只用于演示“暴力”思路，实际运行会因指数级时间而超时。

#### 复杂度  

- **时间复杂度**：`O(4^{m·n})` —— 每个格子都有 4 种走法，所有走法的组合数随格子数呈指数增长。  
- **空间复杂度**：`O(m·n)` —— 递归栈最深会遍历整个森林，另外需要保存已访问的格子集合。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**真正的瓶颈在于**我们把 **每一步的所有走法** 都枚举了。其实我们只需要关心 **“从当前位置走到下一个要砍的树的最短距离”**，而不必枚举所有可能的完整路径。  

思考过程如下：

1. **树的砍伐顺序是唯一的**  
   题目要求必须按照高度从低到高砍树，且所有树的高度互不相同。于是我们先把森林里所有树的 `(行, 列, 高度)` 收集起来并 **按照高度升序排序**。这一步可以用 **堆（优先队列）** 或直接排序实现，类似把所有树的“名字”写进一本按身高排列的电话簿。

2. **把“从 A 到 B 的最短步数”抽象成子问题**  
   当我们站在某个位置 `A`（起点或刚刚砍完的那棵树）时，只需要知道 **去下一个目标树 `B` 的最短路径长度**。这正好是 **最短路径** 的经典问题——在一个只有上下左右四条通路、障碍格子不可通行的网格中求最短步数。  
   对于这种 **无权图**（每走一步代价都是 1），**广度优先搜索（BFS）** 能在 **层层展开** 的过程中最先抵达目标，从而得到最短距离。

3. **把 BFS 当成“黑盒子”**  
   我们把 **“从当前点到目标点的最短步数”** 用一个函数 `bfs(start, target)` 实现。每次只要调用一次 BFS，就能得到从 `start` 到 `target` 的最短步数（如果不可达则返回 `-1`）。  
   这样整个算法的流程就是：  
   - 按高度排序所有树  
   - `cur = (0,0)`（起点）  
   - 对每棵树 `t`（从低到高）  
     - 用 BFS 计算 `cur → t` 的最短步数 `d`  
     - 如果 `d == -1`，说明这棵树根本到不了，直接返回 `-1`  
     - 否则累计答案 `ans += d`，并把 `cur` 更新为 `t`（因为已经站在这棵树的位置）  

4. **为什么是最优的**  
   - **每一次 BFS 只遍历一次整个森林**（最坏情况下遍历全部可通行格子），时间复杂度是 `O(m·n)`。  
   - **树的数量记作 `k`（`k ≤ m·n`）**，我们最多进行 `k` 次 BFS。整体时间复杂度是 `O(k·m·n)`，在本题的约束 `m,n ≤ 50` 下完全可以接受。  
   - 与暴力枚举所有路径的指数级时间相比，**我们只关心每两个关键点之间的最短距离**，省掉了大量冗余搜索，空间只需要保存 BFS 队列和 visited 数组，`O(m·n)`。

5. **关键概念解释**  
   - **广度优先搜索（BFS）**：想象你在一座城市里找最短路线，先走一步到所有相邻的街口，再走两步到所有相邻两层的街口……这样层层扩散，最先到达目的地的那条路径一定是最短的。实现时用 **队列**（先进先出）来记录“下一层要访问的格子”。  
   - **队列**就像排队买咖啡的人，最早进入队列的先被处理；**visited**数组则像是“已经去过的街口”，防止你在同一条路上来回转。  

#### 代码（Python）  

```python
from typing import List, Tuple
from collections import deque

# 四个方向：上、下、左、右
DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def bfs(forest: List[List[int]],
        start: Tuple[int, int],
        target: Tuple[int, int]) -> int:
    """
    在森林中从 start (sx,sy) 走到 target (tx,ty) 的最短步数。
    如果 target 不可达，返回 -1。
    """
    m, n = len(forest), len(forest[0])
    sx, sy = start
    tx, ty = target
    if start == target:
        return 0                     # 已经在目标位置，不需要走

    # visited 用来标记已经进入队列的格子，防止重复访问
    visited = [[False] * n for _ in range(m)]
    visited[sx][sy] = True

    q = deque()
    q.append((sx, sy, 0))            # (行, 列, 已走的步数)

    while q:
        x, y, d = q.popleft()
        # 向四个方向尝试一步
        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            # 合法且不是障碍且未访问过
            if 0 <= nx < m and 0 <= ny < n and not visited[nx][ny] and forest[nx][ny] != 0:
                if (nx, ny) == (tx, ty):
                    return d + 1      # 第一次碰到目标，就是最短路径
                visited[nx][ny] = True
                q.append((nx, ny, d + 1))
    # 队列空了还没找到，说明不可达
    return -1

def cutOffTree(forest: List[List[int]]) -> int:
    """
    主函数：返回从 (0,0) 出发，按树高从低到高砍完所有树的最少步数。
    如果有任意一棵树不可达，返回 -1。
    """
    m, n = len(forest), len(forest[0])

    # 1️⃣ 收集所有树并按高度升序排列
    trees = []
    for i in range(m):
        for j in range(n):
            h = forest[i][j]
            if h > 1:                # 1 表示空地，0 表示障碍
                trees.append((h, i, j))
    trees.sort()                    # 默认按第一个元素（高度）升序

    total_steps = 0
    cur_pos = (0, 0)                 # 起点

    # 2️⃣ 依次前往每棵树
    for _, tx, ty in trees:
        dist = bfs(forest, cur_pos, (tx, ty))
        if dist == -1:               # 途中出现不可达的树
            return -1
        total_steps += dist
        cur_pos = (tx, ty)           # 站到这棵树的位置，继续前进
        forest[tx][ty] = 1           # 砍掉后格子变成空地，后面走路可以经过

    return total_steps
```

> 代码每行都配有中文注释，帮助你把抽象的 BFS 与生活中的“找最短路”对应起来。只要把 `forest` 传进去即可直接运行得到答案。

#### 复杂度  

- **时间复杂度**：`O(k · m · n)`  
  - `k` 为森林中树的数量（最坏情况下 `k = m·n`），每一次 BFS 最多遍历整个矩阵 `m·n`。  
  - 与暴力解的指数级 `O(4^{mn})` 相比，**线性乘积**的增长在 50×50 的规模下几乎是瞬间完成的。  

- **空间复杂度**：`O(m·n)`  
  - 主要来自 BFS 的 `visited` 矩阵和队列，最多存储整个森林的格子。  
  - 与暴力解的递归栈相比，这个空间是 **可控且固定** 的。  

---

## 心得  

- **核心技巧**：**把“按顺序砍树”转化为一系列“最短路径”子问题**，使用 **广度优先搜索（BFS)** 逐对求解。  
- **该技巧适用的题型**：  
  1. “在网格中求最短步数”类（如 01 矩阵最短路径、最小岛屿桥）  
  2. “多个关键点需要依次访问”类（如 旅行商在小规模网格、机器人清扫房间）  
  3. “带顺序约束的最短路”类（如 按字典序遍历、按权值顺序访问）  
- **一句话总结解题钥匙**：  
  > “把全局的大搜索拆成若干个局部的最短路径，用 BFS 把每一步的距离算出来，再把这些距离累加。”  

---

## 反思  

- **第一反应**：看到“必须按树高从低到高砍”，立刻想到把树排个序；看到“只能上下左右走”，想到 BFS 求最短路。  
- **最容易踩的坑**  
  1. **忘记把砍掉的树格子恢复为 1**，导致后面的 BFS 误把已经砍掉的树当成障碍。  
  2. **起点本身可能就是一棵树**（高度 >1），需要先把它视作已砍，或者在排序后让它自然成为第一棵。  
  3. **边界条件**：`m` 或 `n` 为 1 时的单行/单列森林，仍然要保证四方向遍历不会越界。  
- **下次遇到同类题的第一步**：  
  > “先把所有‘必须按顺序访问的点’收集并排序，然后把‘从 A 到 B 的最短步数’抽象为 BFS（或其他最短路算法）来求解。”