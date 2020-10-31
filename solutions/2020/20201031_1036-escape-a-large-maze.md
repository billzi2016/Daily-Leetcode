# #1036. 逃离大迷宫 / Escape a Large Maze

> 难度：困难 · 标签：Array、Hash Table、Depth-First Search、Breadth-First Search · [LeetCode 链接](https://leetcode.com/problems/escape-a-large-maze/)

---

## 题目（英文原版）

**Description**

There is a 1 million by 1 million grid on an XY-plane, and the coordinates of each grid square are (x, y).
We start at the source = [sx, sy] square and want to reach the target = [tx, ty] square. There is also an array of blocked squares, where each blocked[i] = [xi, yi] represents a blocked square with coordinates (xi, yi).
Each move, we can walk one square north, east, south, or west if the square is not in the array of blocked squares. We are also not allowed to walk outside of the grid.
Return true if and only if it is possible to reach the target square from the source square through a sequence of valid moves.

**Examples**

**Example 1:**

```
Input: blocked = [[0,1],[1,0]], source = [0,0], target = [0,2]
Output: false
Explanation: The target square is inaccessible starting from the source square because we cannot move.
We cannot move north or east because those squares are blocked.
We cannot move south or west because we cannot go outside of the grid.
```

**Example 2:**

```
Input: blocked = [], source = [0,0], target = [999999,999999]
Output: true
Explanation: Because there are no blocked cells, it is possible to reach the target square.
```

**Constraints**

- 0 <= blocked.length <= 200
- blocked[i].length == 2
- 0 <= xi, yi < 106
- source.length == target.length == 2
- 0 <= sx, sy, tx, ty < 106
- source != target
- It is guaranteed that source and target are not blocked.

---

## 题目（中文翻译）

**描述**  
在 XY 平面上有一个 $10^6 \times 10^6$ 的网格（grid），每个网格单元的坐标记为 $(x, y)$。  
我们从 **源点**（source）`[sx, sy]` 开始，目标是到达 **目标点**（target）`[tx, ty]`。另外给定一个阻塞单元数组 `blocked`，其中 `blocked[i] = [xi, yi]` 表示坐标为 $(xi, yi)$ 的单元被阻塞（blocked squares）。  

每一步可以向北（north）、东（east）、南（south）或西（west）移动一格，前提是该格子不在 `blocked` 中且不超出网格边界。  
若存在一系列合法移动，使得能够从源点到达目标点，则返回 `true`，否则返回 `false`。

**示例 1**  

**示例 2**  

**约束条件**  

- $0 \leq \text{blocked.length} \leq 200$
- $\text{blocked}[i].\text{length} = 2$
- $0 \leq xi, yi < 10^6$
- $\text{source}.\text{length} = \text{target}.\text{length} = 2$
- $0 \leq sx, sy, tx, ty < 10^6$
- $\text{source} \neq \text{target}$
- 已保证源点和目标点均未被阻塞

**示例**  

**示例 1:**  
```
Input: blocked = [[0,1],[1,0]], source = [0,0], target = [0,2]
Output: false
Explanation: 从源点出发无法到达目标点，因为所有可行的移动方向都被阻塞。  
我们无法向北或向东移动，因为相应的格子被阻塞。  
向南或向西移动也不可行，因为会超出网格范围。
```

**示例 2:**  
```
Input: blocked = [], source = [0,0], target = [999999,999999]
Output: true
Explanation: 由于没有阻塞单元，能够到达目标点。
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把整个 **1 000 000 × 1 000 000** 的网格想成一张巨大的棋盘，然后从 `source` 出发，用**深度优先搜索（DFS）**或**广度优先搜索（BFS）**把所有可以走到的格子都遍历一遍，最后看能否走到 `target`。

- **数据结构**  
  - **队列 / 栈**：保存待访问的格子，就像我们在玩迷宫游戏时，记下“下一步要往哪走”。  
  - **哈希表**（`set`）：记录已经访问过的格子，防止走回头路。哈希表可以类比成一本字典，`key` 是格子坐标，`value`（这里不需要）可以想象成词所在的页码。查询是否已经访问只需要一次“查字典”，时间很快。

- **为什么正确**  
  BFS/DFS 会把 **所有** 能够通过合法移动（上下左右且不在 blocked 中）到达的格子枚举出来，只要 `target` 在这些格子里，就一定能从 `source` 到达。

- **时间/空间复杂度**  
  - **时间复杂度**：在最坏情况下，我们可能要遍历整个网格的每一个格子。网格有 $10^6 \times 10^6 = 10^{12}$ 个格子，用大白话说就是 **一万亿**！于是时间复杂度是 $O(10^{12})$，在实际运行中根本不可接受。  
  - **空间复杂度**：同样需要保存访问过的格子，最坏也需要 $O(10^{12})$ 的空间，显然不可能在电脑里放得下。

> **结论**：暴力搜索虽然思路最简单，却因为网格太大而不可行。

#### 代码（Python）

```python
from collections import deque

def is_escape_bruteforce(blocked, source, target):
    # 把 blocked 转成 set，方便 O(1) 判断是否是障碍格子
    blocked_set = {tuple(p) for p in blocked}
    # 四个方向：上、右、下、左
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    q = deque([tuple(source)])      # BFS 队列
    visited = {tuple(source)}       # 已访问集合

    while q:
        x, y = q.popleft()
        if (x, y) == tuple(target):
            return True            # 找到终点

        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            # 越界检查（网格范围是 [0, 10^6)）
            if not (0 <= nx < 10**6 and 0 <= ny < 10**6):
                continue
            if (nx, ny) in blocked_set:
                continue
            if (nx, ny) in visited:
                continue
            visited.add((nx, ny))
            q.append((nx, ny))

    return False   # BFS 结束仍未到达 target，说明被围住
```

> 这段代码在理论上能得到正确答案，但在实际运行时会 **卡死**，因为要遍历的格子太多。

#### 复杂度

- **时间复杂度**：`O(10^12)` —— 相当于遍历一万亿个格子，远远超过普通电脑的计算能力。  
- **空间复杂度**：`O(10^12)` —— 需要存储一万亿个坐标，同样不可能实现。

---

### 2. 最优解

#### 思路  

**关键观察**  
- `blocked` 最多只有 **200** 个格子。即使这些格子把 `source`（或 `target`）完全围起来，能够围成的最大 “封闭区域” 也非常有限。  
- 若我们从 `source` 能够走出一个 **足够大的** 区域（比如走了超过一定步数仍未被卡住），那么说明 `source` 没有被围住，后面无论目标在多远，都一定可以到达（因为网格是连通的、没有其它障碍）。  
- 同理，对 `target` 也做同样的检查。只有当 **两端都被围住** 时，答案才是 `False`。

**围住的最大面积**  
- 设 `k = len(blocked)`。若用 `k` 个格子围成一个最紧凑的闭合环（类似于把格子排成一个正方形的外框），它能围住的格子数最多是 `k * (k - 1) / 2`（这其实是已知的上界，实际更小）。  
- LeetCode 官方给出的安全阈值是 `k * (k - 1) // 2`，约等于 **20000**（因为 `k ≤ 200`）。因此，只要我们从起点 BFS/DFS 访问的格子数 **超过 20000**，就可以确信起点不被围住。

**算法步骤**  

1. 把 `blocked` 放进 `set`（哈希表）以便 O(1) 判断。  
2. 定义一个 `limit = len(blocked) * (len(blocked) - 1) // 2`（如果 `blocked` 少于 2，直接取 0）。  
3. 从 `source` 做 **受限 BFS**：  
   - 每次弹出一个格子，向四个方向尝试移动。  
   - 若碰到 `target`，直接返回 `True`（说明直接可达）。  
   - 记录已访问格子数 `cnt`，若 `cnt > limit`，说明已经走出了所有可能的围墙，返回 `True`（因为此时一定能逃脱围墙）。  
   - 若 BFS 结束且未达到 `limit`，说明被围住，返回 `False`。  
4. 同样地，从 `target` 做一次受限 BFS（只检查是否能走出围墙，不需要再次判断是否到达 `source`）。  
5. 最终答案是 **source 能逃脱 且 target 能逃脱**。

**为什么正确**  

- **若 source 被围住**：围墙的面积 ≤ `limit`，受限 BFS 只能访问 ≤ `limit` 个格子，永远到不了 `target`，返回 `False`。  
- **若 source 没被围住**：受限 BFS 必然在访问格子数超过 `limit` 时提前返回 `True`，说明它可以走到“无限远”，进而可以到达任何不被障碍阻拦的点（包括 target）。  
- **对 target 同理**。只有两端都不被围住，才一定存在一条合法路径。

**核心技巧**：利用 **blocked 数量的上界** 把“巨大的网格搜索”转化为**常数级的局部搜索**，这就是所谓的 **“受限 BFS”** 或 **“可达区域上界”** 思想。

#### 代码（Python）

```python
from collections import deque
from typing import List, Set, Tuple

def is_escape_possible(blocked: List[List[int]],
                       source: List[int],
                       target: List[int]) -> bool:
    """
    受限 BFS：如果在访问了超过 limit 个格子仍未被卡住，就说明可以逃脱围墙。
    """
    # 1. 预处理
    blocked_set: Set[Tuple[int, int]] = {tuple(p) for p in blocked}
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # 2. 计算搜索上限
    k = len(blocked)
    # 经验上限：k * (k - 1) // 2，k <= 200 时最多约 20000
    limit = k * (k - 1) // 2

    # 3. 受限 BFS 的实现（返回是否能“逃脱围墙”或直接到达目标）
    def bfs(start: Tuple[int, int], finish: Tuple[int, int]) -> bool:
        q = deque([start])
        visited: Set[Tuple[int, int]] = {start}
        steps = 0

        while q:
            x, y = q.popleft()
            steps += 1
            # 已经走出了可能的围墙范围，直接返回 True
            if steps > limit:
                return True
            # 若恰好到达目标（只在 source->target 的搜索里会用到）
            if (x, y) == finish:
                return True

            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                # 越界检查
                if not (0 <= nx < 10**6 and 0 <= ny < 10**6):
                    continue
                # 障碍格子或已经访问过的格子直接跳过
                if (nx, ny) in blocked_set or (nx, ny) in visited:
                    continue
                visited.add((nx, ny))
                q.append((nx, ny))

        # BFS 结束仍未突破上限，说明被围住
        return False

    s = tuple(source)
    t = tuple(target)

    # 先检查从 source 能否逃脱（或直接到达 target）
    if not bfs(s, t):
        return False
    # 再检查从 target 能否逃脱（不需要再判断是否到达 source）
    if not bfs(t, s):
        return False

    return True
```

> 代码里每一步都有中文注释，直接复制运行即可。

#### 复杂度

- **时间复杂度**：`O(limit)`，其中 `limit = k * (k - 1) / 2 ≤ 20000`。也就是说最多只会遍历约两万格子，和整个 10⁶ × 10⁶ 的网格大小 **无关**，几乎是常数时间。  
- **空间复杂度**：`O(limit)`，因为 `visited` 最多存储这么多格子，同样约两万，远远低于一万亿的需求。

> 与暴力解相比，时间从 `10^12` 降到了 `2×10^4`，速度提升 **数万倍**，空间也同样大幅压缩。

---

## 心得

- **核心技巧**：利用阻塞格子数量的上界，将“大网格搜索”转化为“受限 BFS”。  
- **适用的题型**  
  1. **Escape a Large Maze**（本题）  
  2. **Number of Islands II**（动态添加障碍后判断连通性）  
  3. **Largest Island**（利用限定的障碍数量进行局部搜索）  
- **一句话总结**：**只要能走出 `blocked` 能围成的最大封闭区域，就一定能到达任意远的目标。**  

---

## 反思

- **第一反应**：直接把整个网格当成图，用 BFS/DFS 完全遍历。  
- **最容易踩的坑**  
  - 忘记 **网格边界**（坐标只能在 `[0, 10⁶)` 之间），导致数组越界。  
  - 没有利用 `blocked` 的数量上限，导致时间爆炸。  
  - 在 BFS 中没有设置 **访问上限**，会无限扩散直至内存耗尽。  
- **下次遇到类似题**：第一步先**思考障碍的数量能限制搜索范围多少**，如果可以得到一个 **常数级的上界**，就立刻采用 **受限 BFS/DFS** 而不是全局搜索。这样既保证正确性，又能在大规模输入下快速通过。