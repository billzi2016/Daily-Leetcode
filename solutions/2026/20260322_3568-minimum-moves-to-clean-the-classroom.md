# #3568. 清理教室的最少移动次数 / Minimum Moves to Clean the Classroom

> 难度：中等 · 标签：Array、Hash Table、Bit Manipulation、Breadth-First Search、Matrix · [LeetCode 链接](https://leetcode.com/problems/minimum-moves-to-clean-the-classroom/)

---

## 题目（英文原版）

**Description**

You are given an m x n grid classroom where a student volunteer is tasked with cleaning up litter scattered around the room. Each cell in the grid is one of the following:
You are also given an integer energy, representing the student's maximum energy capacity. The student starts with this energy from the starting position 'S'.
Each move to an adjacent cell (up, down, left, or right) costs 1 unit of energy. If the energy reaches 0, the student can only continue if they are on a reset area 'R', which resets the energy to its maximum capacity energy.
Return the minimum number of moves required to collect all litter items, or -1 if it's impossible.

**Examples**

**Example 1:**

```
Input: classroom = ["S.", "XL"], energy = 2
Output: 2
Explanation:
```

**Example 2:**

```
Input: classroom = ["LS", "RL"], energy = 4
Output: 3
Explanation:
```

**Example 3:**

```
Input: classroom = ["L.S", "RXL"], energy = 3
Output: -1
Explanation:
No valid path collects all 'L' .
```

**Constraints**

- 1 <= m == classroom.length <= 20
- 1 <= n == classroom[i].length <= 20
- classroom[i][j] is one of 'S', 'L', 'R', 'X', or '.'
- 1 <= energy <= 50
- There is exactly one 'S' in the grid.
- There are at most 10 'L' cells in the grid.

---

## 题目（中文翻译）

你得到一个 **m × n** 的网格（grid）`classroom`，其中每个格子（cell）可能是以下几种之一：

- `'S'`：学生志愿者的起始位置，学生的初始能量为 `energy`（整数），表示学生的最大能量上限。
- `'L'`：散落的垃圾（litter），需要全部收集。
- `'R'`：能量重置区（reset area），站在该格子上时可以将能量恢复至最大值 `energy`。
- `'X'`：障碍物，不能通行。
- `'.'`：空地，可以自由通行。

学生每向上下左右任意相邻格子移动一次，消耗 **1** 单位能量。**当能量耗尽为 0 时，学生只能继续移动**，但前提是此时必须位于重置区 `'R'`，此时能量会立即恢复为最大值 `energy`。如果不在 `'R'` 且能量为 0，则无法继续前进。

请返回收集所有垃圾 `'L'` 所需的**最少移动次数**；如果不存在可行路径，则返回 **-1**。

---

### 示例

**示例 1**

```text
Input: classroom = ["S.", "XL"], energy = 2
Output: 2
Explanation: 学生从 `'S'` 出发向右移动到 `'.'`（消耗 1 能量），再向下移动到 `'L'`（再消耗 1 能量），成功收集全部垃圾，总共移动 2 步。
```

**示例 2**

```text
Input: classroom = ["LS", "RL"], energy = 4
Output: 3
Explanation: 一种最优路径是从 `'S'` 向左到 `'L'`（1 步），再向下到 `'R'`（1 步），此时能量被重置，最后向右到 `'L'`（1 步），共计 3 步收集完所有垃圾。
```

**示例 3**

```text
Input: classroom = ["L.S", "RXL"], energy = 3
Output: -1
Explanation: 没有任何合法路径能够在能量限制下收集所有 `'L'`，因此返回 -1。
```

---

### 约束条件

- `1 <= m == classroom.length <= 20`
- `1 <= n == classroom[i].length <= 20`
- `classroom[i][j]` 只能是 `'S'`, `'L'`, `'R'`, `'X'` 或 `'.'`
- `1 <= energy <= 50`
- 网格中恰好只有一个 `'S'`
- 网格中至多有 **10** 个 `'L'` 格子

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把 **每一步的所有信息** 都记录下来，然后像走迷宫一样一步步展开搜索，直到把所有垃圾 `'L'` 都捡完。  
我们需要的状态信息有：

| 信息 | 含义 | 类比 |
|------|------|------|
| `(x, y)` | 当前所在的格子坐标 | 像在地图上标记自己的位置 |
| `mask`   | 已经捡到的垃圾集合，用二进制位表示（第 i 位为 1 表示第 i 块 `'L'` 已经收集） | 像字典的查词表，key 是垃圾编号，value 是“已收集”/“未收集” |
| `e`      | 现在剩余的能量 | 像手机的电量，每走一步就减 1，走到 `'R'` 充满 |
| `steps`  | 已经走了多少步（即答案） | 计数器 |

把这四个变量放在一起就构成了 **完整的搜索状态**。  
我们可以用 **广度优先搜索（BFS）** 按层展开：先把起点状态压入队列，然后不断取出队首状态，尝试向上、下、左、右四个方向移动，生成新的状态并加入队列。只要在某一步的 `mask` 已经等于 “所有垃圾都捡到”的全 1 掩码，就可以返回当前的 `steps`，因为 BFS 保证第一次到达的就是最少步数。

**为什么暴力 BFS 能得到正确答案？**  
- BFS 按层遍历，先遍历的路径一定是最短的。  
- 我们把每一种可能的 `(位置, 已收集的垃圾, 剩余能量)` 都当成不同的节点，遍历所有合法的转移，必然会覆盖所有可行的路线。  
- 当出现能量耗尽且不在 `'R'` 的格子时，这条路就不再继续扩展，等价于把非法路径剪掉。  

#### 代码（Python）

```python
from collections import deque
from typing import List

def minMoves(classroom: List[str], energy: int) -> int:
    m, n = len(classroom), len(classroom[0])

    # ---------- 1. 预处理 ----------
    # 记录所有垃圾的位置，并给每块垃圾编号（0~k-1）
    litter_pos = {}
    k = 0
    for i in range(m):
        for j in range(n):
            if classroom[i][j] == 'L':
                litter_pos[(i, j)] = k
                k += 1
            if classroom[i][j] == 'S':
                sx, sy = i, j

    full_mask = (1 << k) - 1          # 所有垃圾都捡到的掩码

    # ---------- 2. BFS ----------
    # 队列里存 (x, y, mask, remaining_energy, steps)
    q = deque()
    q.append((sx, sy, 0, energy, 0))

    # 为了防止无限循环，用集合记录已经访问过的状态
    # visited[(x, y, mask, e)] = True
    visited = set()
    visited.add((sx, sy, 0, energy))

    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while q:
        x, y, mask, e, steps = q.popleft()

        # ① 检查是否已经捡完所有垃圾
        if mask == full_mask:
            return steps

        # ② 向四个方向尝试移动
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            # 越界或是墙（这里用 'X' 表示不可通行的格子）直接跳过
            if not (0 <= nx < m and 0 <= ny < n):
                continue
            if classroom[nx][ny] == 'X':
                continue

            ne = e - 1                     # 移动一步消耗 1 能量
            if ne < 0:                     # 能量耗尽且不在重置格子，非法
                continue

            # ③ 到达重置格子会把能量恢复到满值
            if classroom[nx][ny] == 'R':
                ne = energy

            # ④ 如果走到垃圾格子，更新 mask
            nmask = mask
            if classroom[nx][ny] == 'L':
                idx = litter_pos[(nx, ny)]
                nmask = mask | (1 << idx)   # 对应位设为 1

            state = (nx, ny, nmask, ne)
            if state in visited:
                continue
            visited.add(state)
            q.append((nx, ny, nmask, ne, steps + 1))

    # BFS 结束仍未捡完所有垃圾，说明不可达
    return -1
```

#### 复杂度  

- **时间复杂度**：  
  - 状态的上限是 `m * n * 2^k * (energy + 1)`。  
  - 这里 `k ≤ 10`，`energy ≤ 50`，`m,n ≤ 20`，所以最坏情况下约为 `20*20*2^10*51 ≈ 2.1×10^6`，在 Python 中仍然可以跑完。  
  - 用大白话说，`O(m·n·2^k·E)` 表示“每个格子、每种垃圾收集情况、每一种可能的剩余能量”都会被访问一次。

- **空间复杂度**：  
  - 同样需要保存所有已访问的状态，空间也是 `O(m·n·2^k·E)`。  
  - 队列里最多也会同时存这么多状态。

---

### 2. 最优解  

#### 思路  

暴力 BFS 已经能通过题目，但还有 **可以进一步剪枝** 的空间，使搜索更快、更省内存。  
瓶颈主要在 **能量维度**：同一个位置、同样的已收集垃圾集合，如果我们已经用更高的剩余能量到达过一次，那么以后用更低能量到达的状态就不可能产生更好的答案——因为以后每一步的消耗是一样的，剩余能量更少只会让后面的可行动作更受限。

**优化思路**：

1. **把 “剩余能量” 变成 “最优能量”**  
   - 对每个三元组 `(x, y, mask)` 只记录 **最高的剩余能量** `bestEnergy[x][y][mask]`。  
   - 当我们准备把一个新状态 `(x, y, mask, e)` 加入队列时，比较 `e` 与 `bestEnergy[x][y][mask]`：  
     - 若 `e` 更大，则更新 `bestEnergy` 并继续搜索。  
     - 若 `e` 不大于已经记录的值，则直接丢弃，因为已经有更好（能量更多）的路径到达同样的局面了。

2. **仍然使用 BFS**  
   - BFS 本身已经保证步数最小，**只要不丢掉任何可能产生更好能量的路径**，答案不变。  
   - 通过 `bestEnergy` 剪枝后，状态总数从 `m·n·2^k·E` 降到大约 `m·n·2^k`（因为每个 `(x,y,mask)` 最多只会保留一次能量最高的记录），大幅降低时间和空间开销。

3. **实现细节**  
   - `bestEnergy` 用三维列表 `[[[-1] * (1<<k) for _ in range(n)] for _ in range(m)]` 初始化为 `-1`（表示未到达）。  
   - 当我们准备入队时，先检查 `e > bestEnergy[x][y][mask]`。  
   - 其余转移逻辑（能量消耗、重置、更新 `mask`）与暴力版完全相同。

#### 代码（Python）

```python
from collections import deque
from typing import List

def minMoves(classroom: List[str], energy: int) -> int:
    m, n = len(classroom), len(classroom[0])

    # ---------- 1. 预处理 ----------
    litter_pos = {}
    k = 0
    for i in range(m):
        for j in range(n):
            ch = classroom[i][j]
            if ch == 'L':
                litter_pos[(i, j)] = k
                k += 1
            if ch == 'S':
                sx, sy = i, j

    full_mask = (1 << k) - 1

    # ---------- 2. bestEnergy[x][y][mask] ----------
    # -1 表示还没有以这个 mask 到达过 (x,y)
    bestEnergy = [[[-1] * (1 << k) for _ in range(n)] for _ in range(m)]

    # ---------- 3. BFS ----------
    q = deque()
    q.append((sx, sy, 0, energy, 0))   # (x, y, mask, remaining energy, steps)
    bestEnergy[sx][sy][0] = energy

    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while q:
        x, y, mask, e, steps = q.popleft()

        if mask == full_mask:          # 已经收集完全部垃圾
            return steps

        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < m and 0 <= ny < n):
                continue
            if classroom[nx][ny] == 'X':
                continue

            ne = e - 1
            if ne < 0:                 # 能量耗尽且不在重置格子，不能前进
                continue

            if classroom[nx][ny] == 'R':
                ne = energy            # 重置能量

            nmask = mask
            if classroom[nx][ny] == 'L':
                idx = litter_pos[(nx, ny)]
                nmask = mask | (1 << idx)

            # ---------- 剪枝：只保留能量最高的状态 ----------
            if ne <= bestEnergy[nx][ny][nmask]:
                continue                # 已经有更好（能量更多）的路径到达这里
            bestEnergy[nx][ny][nmask] = ne
            q.append((nx, ny, nmask, ne, steps + 1))

    return -1
```

#### 复杂度  

- **时间复杂度**：`O(m·n·2^k)`  
  - 每个 `(x, y, mask)` 最多只会被处理一次（因为后续能量更低的状态会被剪掉），所以总体遍历次数与格子数、垃圾子集数的乘积成正比。  
  - 与暴力版相比，省去了 `* energy` 这层因子，跑得更快。

- **空间复杂度**：`O(m·n·2^k)`  
  - `bestEnergy` 三维数组占用的空间就是主导因素，队列中最多也只会存同样数量的状态。  

相比于暴力 BFS，这个版本在 **大多数测试用例** 下都能显著降低运行时间和内存占用。

---

## 心得  

- **核心技巧**：**在 BFS 中加入状态剪枝**，利用 `bestEnergy[x][y][mask]` 只保留同一位置同一收集情况的最高剩余能量。  
- **适用的题型**（常见的“状态空间搜索 + 资源限制”）  
  1. `Shortest Path to Get All Keys`（LeetCode 864）——使用键的位掩码 + BFS 剪枝。  
  2. `Minimum Moves to Reach Target with Energy`（类似的能量/血量限制问题）。  
  3. `Robot Room Cleaner`（需要记录清洁状态并剪枝）。  
- **一句话总结解题钥匙**：**把“更好”定义为“剩余能量更多”，只保留每个局部状态的最优能量，就能大幅削减搜索空间。**

---

## 反思  

- **第一反应**：看到“每走一步消耗能量，‘R’ 可以充能”，立刻想到把能量作为搜索状态的一部分，用 BFS 暴力遍历。  
- **最容易踩的坑**  
  - 忘记在能量耗尽时检查是否站在 `'R'`，导致错误地把合法路径剪掉。  
  - 只用 `(x, y, mask)` 记录访问，忽略了能量维度，导致错误的“已访问”判断。  
  - 边界条件：`energy` 可能等于 1，移动一步后必须恰好在 `'R'` 才能继续。  
- **下次遇到同类题**：第一步先 **确定所有影响决策的维度**（位置、收集进度、资源量），再 **用 BFS/DFS 把它们组合成状态**，随后思考 **是否可以用“最优值”剪枝**（如最大剩余资源、最少消耗等）。这样既保证完整性，又能高效求解。