# #2087. 机器人在网格中的最小回家成本 / Minimum Cost Homecoming of a Robot in a Grid

> 难度：中等 · 标签：Array、Greedy · [LeetCode 链接](https://leetcode.com/problems/minimum-cost-homecoming-of-a-robot-in-a-grid/)

---

## 题目（英文原版）

**Description**

There is an m x n grid, where (0, 0) is the top-left cell and (m - 1, n - 1) is the bottom-right cell. You are given an integer array startPos where startPos = [startrow, startcol] indicates that initially, a robot is at the cell (startrow, startcol). You are also given an integer array homePos where homePos = [homerow, homecol] indicates that its home is at the cell (homerow, homecol).
The robot needs to go to its home. It can move one cell in four directions: left, right, up, or down, and it can not move outside the boundary. Every move incurs some cost. You are further given two 0-indexed integer arrays: rowCosts of length m and colCosts of length n.
Return the minimum total cost for this robot to return home.

**Examples**

**Example 1:**

```
Input: startPos = [1, 0], homePos = [2, 3], rowCosts = [5, 4, 3], colCosts = [8, 2, 6, 7]
Output: 18
Explanation: One optimal path is that:
Starting from (1, 0)
-> It goes down to (2, 0). This move costs rowCosts[2] = 3.
-> It goes right to (2, 1). This move costs colCosts[1] = 2.
-> It goes right to (2, 2). This move costs colCosts[2] = 6.
-> It goes right to (2, 3). This move costs colCosts[3] = 7.
The total cost is 3 + 2 + 6 + 7 = 18
```

**Example 2:**

```
Input: startPos = [0, 0], homePos = [0, 0], rowCosts = [5], colCosts = [26]
Output: 0
Explanation: The robot is already at its home. Since no moves occur, the total cost is 0.
```

**Constraints**

- m == rowCosts.length
- n == colCosts.length
- 1 <= m, n <= 105
- 0 <= rowCosts[r], colCosts[c] <= 104
- startPos.length == 2
- homePos.length == 2
- 0 <= startrow, homerow < m
- 0 <= startcol, homecol < n

---

## 题目（中文翻译）

给定一个 `m × n` 的网格，其中左上角单元格坐标为 `(0, 0)`，右下角单元格坐标为 `(m - 1, n - 1)`。数组 `startPos = [startrow, startcol]` 表示机器人最初位于单元格 `(startrow, startcol)`。数组 `homePos = [homerow, homecol]` 表示机器人的家在单元格 `(homerow, homecol)`。

机器人需要移动到家所在的单元格。它一次可以向左、向右、向上或向下移动一格，且不能越界。每一次移动都会产生一定的费用。另有两个 **0 索引** 的整数数组：`rowCosts`（行费用），长度为 `m`，以及 `colCosts`（列费用），长度为 `n`。

- 当机器人从行 `r` 移动到行 `r + 1`（向下）或 `r - 1`（向上）时，需要支付 `rowCosts[r]`（注意是离开的那一行的费用）。
- 当机器人从列 `c` 移动到列 `c + 1`（向右）或 `c - 1`（向左）时，需要支付 `colCosts[c]`（同样是离开的那一列的费用）。

返回机器人回家的 **最小总费用**。

---

### 示例

#### 示例 1
```text
Input: startPos = [1, 0], homePos = [2, 3], rowCosts = [5, 4, 3], colCosts = [8, 2, 6, 7]
Output: 18
Explanation: 一条最优路径如下：
- 从 (1, 0) 开始
- 向下移动到 (2, 0)，此移动费用为 rowCosts[2] = 3
- 向右移动到 (2, 1)，此移动费用为 colCosts[1] = 2
- 向右移动到 (2, 2)，此移动费用为 colCosts[2] = 6
- 向右移动到 (2, 3)，此移动费用为 colCosts[3] = 7
累计费用 3 + 2 + 6 + 7 = 18
```

#### 示例 2
```text
Input: startPos = [0, 0], homePos = [0, 0], rowCosts = [5], colCosts = [26]
Output: 0
Explanation: 机器人已经在家中。没有任何移动，累计费用为 0。
```

---

### 约束条件
- `m == rowCosts.length`
- `n == colCosts.length`
- `1 ≤ m, n ≤ 10^5`
- `0 ≤ rowCosts[r], colCosts[c] ≤ 10^4`
- `startPos.length == 2`
- `homePos.length == 2`
- `0 ≤ startrow, homerow < m`
- `0 ≤ startcol, homecol < n`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把机器人在网格里所有可能的走法都枚举一遍，找出费用最小的那条路径。  
可以把网格看成一张“棋盘”，每走一步就相当于在棋盘上向上、下、左、右跳一格。  
我们把每个格子当成 **节点**，四个方向的合法移动当成 **边**，每条边的费用就是对应的 `rowCosts`（向上下移动）或 `colCosts`（向左右移动）。  

> **类比**：这跟在城市里找最便宜的公交路线差不多——把每个站点当成节点，公交票价当成边权。  
> 暴力做法就是把所有可能的路线都列出来，然后挑最便宜的那条。

实现上可以用 **广度优先搜索（BFS）**：  
1. 把起点 `(startRow, startCol)` 放进队列，费用记为 `0`。  
2. 每次从队列弹出一个位置 `(r, c)`，尝试向四个方向走一步（如果没有越界）。  
3. 计算这一步的费用：向上/下走用 `rowCosts[newR]`，向左/右走用 `colCosts[newC]`。  
4. 如果到达的格子之前没有被访问过，或者这次到达的费用更小，就把它加入队列。  
5. 当弹出的是终点 `(homeRow, homeCol)` 时，当前费用就是最小费用。

**为什么正确？**  
BFS 按费用递增的顺序遍历（因为每条边的费用都是非负的），所以第一次碰到终点时，一定是最小费用路径。

**复杂度分析（大白话）**  
- 时间复杂度：我们最坏情况下会访问网格里的每一个格子一次，网格大小是 `m × n`，所以时间是 **O(m·n)**。可以把它想象成“遍历整个棋盘”。  
- 空间复杂度：需要一个 `visited` 数组保存每个格子的最小费用，同样是 **O(m·n)**，相当于“记住每个格子的花费”。  

> 对于本题的约束（`m,n` 最多 10⁵），`m·n` 可能会达到 10¹⁰，显然不可接受，说明暴力 BFS 不是实际可用的解法。

#### 代码（Python）

```python
from collections import deque
from math import inf

def minCostBrute(startPos, homePos, rowCosts, colCosts):
    m, n = len(rowCosts), len(colCosts)
    sr, sc = startPos
    hr, hc = homePos

    # 记录到每个格子的最小费用，初始为正无穷
    dist = [[inf] * n for _ in range(m)]
    dist[sr][sc] = 0

    q = deque()
    q.append((sr, sc))

    # 四个方向向量
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while q:
        r, c = q.popleft()
        if (r, c) == (hr, hc):
            return dist[r][c]          # 第一次到达终点就是最小费用

        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n:          # 不越界
                # 计算这一步的费用
                cost = rowCosts[nr] if dr != 0 else colCosts[nc]
                new_dist = dist[r][c] + cost
                if new_dist < dist[nr][nc]:
                    dist[nr][nc] = new_dist
                    q.append((nr, nc))

    return -1   # 按题意这里不会到达
```

#### 复杂度  

- **时间复杂度**：`O(m·n)` — 需要检查网格里的每一个格子，想象成“遍历整张地图”。  
- **空间复杂度**：`O(m·n)` — 需要保存每个格子的最小费用，同样是“把整张地图记在纸上”。  

---

### 2. 最优解  

#### 思路  

从暴力解我们已经知道：  
- 机器人只能在 **行** 方向上上下移动，或者 **列** 方向上左右移动。  
- **提示** 已经明确：不管机器人走哪条路径，它都必须经过 `startRow` 与 `homeRow` 之间的所有行、以及 `startCol` 与 `homeCol` 之间的所有列。  

这意味着**只要把机器人直接从起点走到终点，沿途经过的每一行/列都只会走一次**，再多走一步只会把费用再加一次，根本不可能更便宜。  

所以最小费用等于：  

```
所有需要跨过的行的 rowCosts 之和  +  所有需要跨过的列的 colCosts 之和
```

**如何求和？**  
1. 先比较起始行和目标行的大小。  
   - 如果 `startRow < homeRow`，机器人要向下走，遍历区间 `[startRow+1, homeRow]`（注意不包括起始行本身，因为站在起始行时并不产生费用）。  
   - 否则向上走，遍历区间 `[homeRow, startRow-1]`。  
2. 同理处理列的方向。  
3. 把对应的 `rowCosts`、`colCosts` 加起来即可。

> **类比**：把每一行的费用想象成“过山坡的坡度”，机器人必须爬过从起点到家的每一个坡，坡度相加就是总耗费的体力。我们只需要把这些坡度相加，而不必考虑“先爬左边的坡再爬右边的坡”，因为顺序不影响总和。

#### 代码（Python）

```python
def minCost(startPos, homePos, rowCosts, colCosts):
    """
    直接求需要跨过的行/列费用之和，时间 O(|Δrow| + |Δcol|)，空间 O(1)。
    """
    sr, sc = startPos
    hr, hc = homePos

    total = 0

    # 处理行方向（上下）
    if sr < hr:                      # 向下走
        for r in range(sr + 1, hr + 1):
            total += rowCosts[r]
    else:                            # 向上走
        for r in range(sr - 1, hr - 1, -1):
            total += rowCosts[r]

    # 处理列方向（左右）
    if sc < hc:                      # 向右走
        for c in range(sc + 1, hc + 1):
            total += colCosts[c]
    else:                            # 向左走
        for c in range(sc - 1, hc - 1, -1):
            total += colCosts[c]

    return total
```

> **一行写法（更 Pythonic）**  
> 如果你已经熟悉列表切片，可以把上面的循环压缩成两行求和，效果相同但更简洁：

```python
def minCost(startPos, homePos, rowCosts, colCosts):
    sr, sc = startPos
    hr, hc = homePos
    # 行费用
    row_sum = sum(rowCosts[min(sr, hr)+1 : max(sr, hr)+1])
    # 列费用
    col_sum = sum(colCosts[min(sc, hc)+1 : max(sc, hc)+1])
    return row_sum + col_sum
```

#### 复杂度  

- **时间复杂度**：`O(|hr - sr| + |hc - sc|)` — 只遍历机器人实际要跨过的行和列。  
  - 如果把这两个距离记作 `Δrow`、`Δcol`，则复杂度是 `O(Δrow + Δcol)`。在最坏情况下（起点在左上角，终点在右下角），`Δrow ≤ m`、`Δcol ≤ n`，所以仍是线性 `O(m + n)`，远远小于 `O(m·n)`。  
- **空间复杂度**：`O(1)` — 只用了几个整数变量，不会随输入规模增长。

---

## 心得  

- **核心技巧**：**只要把必须跨过的行/列费用相加**，不必考虑走哪条具体路径。  
- 该技巧适用的题型：  
  1. “最小费用从 A 到 B，费用只与经过的行/列有关”——如本题。  
  2. “在一维数组中从 i 移动到 j，每一步费用等于该位置的值”。  
  3. “在数轴上移动，移动成本只与经过的点的权值有关”。  
- **一句话总结**：*只要明确哪些行/列是必经的，答案就是这些必经行列费用的总和。*

---

## 反思  

- **第一反应**：先想到用 BFS/DFS 暴力搜索所有路径，想把每一步都算清楚。  
- **最容易踩的坑**：  
  - 忘记 **不计起始格子的费用**（因为站在起点时并没有移动）。  
  - 在向上/向左遍历时写错循环的边界，导致多加或少加了一个 `rowCosts`/`colCosts`。  
  - 对大输入忘记考虑时间复杂度，导致超时。  
- **下次类似题的第一步**：先问自己“是否每一步的费用只和**经过的行/列**有关”。如果答案是“是”，就可以直接把这些行/列的费用加起来，而不必做搜索。