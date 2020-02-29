# #789. 逃离幽灵 / Escape The Ghosts

> 难度：中等 · 标签：Array、Math · [LeetCode 链接](https://leetcode.com/problems/escape-the-ghosts/)

---

## 题目（英文原版）

**Description**

You are playing a simplified PAC-MAN game on an infinite 2-D grid. You start at the point [0, 0], and you are given a destination point target = [xtarget, ytarget] that you are trying to get to. There are several ghosts on the map with their starting positions given as a 2D array ghosts, where ghosts[i] = [xi, yi] represents the starting position of the ith ghost. All inputs are integral coordinates.
Each turn, you and all the ghosts may independently choose to either move 1 unit in any of the four cardinal directions: north, east, south, or west, or stay still. All actions happen simultaneously.
You escape if and only if you can reach the target before any ghost reaches you. If you reach any square (including the target) at the same time as a ghost, it does not count as an escape.
Return true if it is possible to escape regardless of how the ghosts move, otherwise return false.

**Examples**

**Example 1:**

```
Input: ghosts = [[1,0],[0,3]], target = [0,1]
Output: true
Explanation: You can reach the destination (0, 1) after 1 turn, while the ghosts located at (1, 0) and (0, 3) cannot catch up with you.
```

**Example 2:**

```
Input: ghosts = [[1,0]], target = [2,0]
Output: false
Explanation: You need to reach the destination (2, 0), but the ghost at (1, 0) lies between you and the destination.
```

**Example 3:**

```
Input: ghosts = [[2,0]], target = [1,0]
Output: false
Explanation: The ghost can reach the target at the same time as you.
```

**Constraints**

- 1 <= ghosts.length <= 100
- ghosts[i].length == 2
- -104 <= xi, yi <= 104
- There can be multiple ghosts in the same location.
- target.length == 2
- -104 <= xtarget, ytarget <= 104

---

## 题目（中文翻译）

**描述**  
你在一个无限的二维网格（grid）上玩一个简化版的吃豆人（PAC‑MAN）游戏。你从点 `[0, 0]` 开始，目标点为 `target = [x_target, y_target]`，需要尽快到达该位置。地图上有若干幽灵（ghosts），它们的起始位置由二维数组 `ghosts` 给出，其中 `ghosts[i] = [x_i, y_i]` 表示第 `i` 个幽灵的起始坐标。所有输入都是整数坐标。

每回合（turn），你和所有幽灵可以独立选择向四个基准方向中的任意一个移动 1 单位——北（north）、东（east）、南（south）或西（west）——或者原地不动。所有动作 **同步**（simultaneously）发生。

只有当你能够在任何幽灵到达你之前抵达目标点时，才算成功逃离（escape）。如果你与幽灵在同一回合到达同一个格子（包括目标格子），则不算逃脱。

返回 `true` 当且仅当不论幽灵如何移动，你都能确保逃离；否则返回 `false`。

**示例**

**示例 1**  
```text
Input: ghosts = [[1,0],[0,3]], target = [0,1]
Output: true
Explanation: 你可以在 1 回合后到达目的地 (0, 1)，而位于 (1, 0) 和 (0, 3) 的两只幽灵无法追上你。
```

**示例 2**  
```text
Input: ghosts = [[1,0]], target = [2,0]
Output: false
Explanation: 你需要到达目的地 (2, 0)，但幽灵位于 (1, 0) 正好在你和目的地之间。
```

**示例 3**  
```text
Input: ghosts = [[2,0]], target = [1,0]
Output: false
Explanation: 幽灵可以在同一回合到达目标点，你们同时到达，算作未逃脱。
```

**约束条件**

- `1 <= ghosts.length <= 100`
- `ghosts[i].length == 2`
- `-10^4 <= x_i, y_i <= 10^4`
- 同一位置上可能出现多只幽灵。
- `target.length == 2`
- `-10^4 <= x_target, y_target <= 10^4`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把**所有人（我们）和所有幽灵**的每一步移动都枚举出来，看看有没有一种走法能够让我们在幽灵到达我们所在格子之前先到达目标点。  

- **数据结构**：  
  - 使用 **队列**（queue）实现**广度优先搜索（BFS）**，把每一回合所有可能的位置都展开。  
  - 用 **集合（set）** 保存已经访问过的坐标，防止同一个格子被重复遍历（相当于查字典，key 是坐标，value 是是否已访问）。  

- **为什么正确**：  
  BFS 会按照回合数从小到大层层展开；当我们第一次在第 `t` 回合到达目标时，意味着在 **所有可能的第 ≤t 回合的走法** 中，没有任何幽灵能在第 `t` 回合或更早的回合占据同一个格子（因为我们在展开时同步检查幽灵的位置）。如果这种情况出现，就说明**一定可以逃脱**。  

- **时间/空间复杂度的大白话**：  
  - 设我们到达目标的最短步数为 `D`（即曼哈顿距离），每一步我们可以向四个方向或原地不动，最多有 `5` 种选择。于是第 `t` 步会产生 `5^t` 种可能的路径。把所有 `t = 0 … D` 的路径都枚举出来，时间复杂度大概是 `O(5^D)`，这在 `D` 稍大时就会爆炸（比如 `D=10` 时已经超过 9.7 百万次）。  
  - 同理，需要把每只幽灵的所有可能位置也展开，空间会随之指数增长。  

  用大白话说，这种方法相当于“把所有可能的走法都列出来，然后一个个检查”，在实际数据范围（坐标可达 ±10⁴）下根本不可行。

#### 代码（Python）  

```python
from collections import deque
from typing import List, Tuple, Set

def can_escape_bruteforce(ghosts: List[List[int]], target: List[int]) -> bool:
    # ---------- 辅助函数 ----------
    def manhattan(p: Tuple[int, int]) -> int:
        return abs(p[0]) + abs(p[1])

    # ---------- 初始化 ----------
    start = (0, 0)
    tgt = tuple(target)

    # 我们的 BFS 队列：每个元素是 (x, y, steps)
    q = deque([(start[0], start[1], 0)])
    visited_me: Set[Tuple[int, int, int]] = set()
    visited_me.add((start[0], start[1], 0))

    # 预先把每只幽灵的所有可能位置在每一步算出来（这里同样是暴力展开）
    # ghost_positions[t] = set of positions ghosts could occupy at step t
    ghost_positions: List[Set[Tuple[int, int]]] = [{tuple(g) for g in ghosts}]

    # ---------- BFS ----------
    while q:
        x, y, step = q.popleft()

        # 如果我们已经到达目标，检查第 step 步时有没有幽灵也在同一格子
        if (x, y) == tgt:
            # 若第 step 步的幽灵集合中不包含目标，则成功逃脱
            if tgt not in ghost_positions[step]:
                return True
            # 否则同步到达，算作失败，继续搜索别的路径
        # 生成下一步所有可能的移动（上下左右或不动）
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1), (0,0)]:
            nx, ny = x + dx, y + dy
            nstep = step + 1

            # 防止无限扩展：如果已经超过我们到目标的最短距离，就不必继续
            if nstep > manhattan(tgt):
                continue

            if (nx, ny, nstep) in visited_me:
                continue
            visited_me.add((nx, ny, nstep))
            q.append((nx, ny, nstep))

        # 同步扩展幽灵的可能位置到 step+1
        # 只保留到当前 step+1 为止的集合，后面会在判断时使用
        if len(ghost_positions) <= step + 1:
            next_set: Set[Tuple[int, int]] = set()
            for gx, gy in ghost_positions[step]:
                for dx, dy in [(1,0), (-1,0), (0,1), (0,-1), (0,0)]:
                    next_set.add((gx + dx, gy + dy))
            ghost_positions.append(next_set)

    # 所有可能路径都搜索完仍未找到安全到达的方式
    return False
```

> **关键行中文注释**  
> - `deque` 用来实现**层层推进**的 BFS，类似排队等候的队列。  
> - `ghost_positions[t]` 保存第 `t` 回合所有幽灵可能出现的格子，像一本“每回合的地图”。  
> - `if nstep > manhattan(tgt): continue` 把搜索深度限制在我们**最短**能到达目标的步数内，避免无意义的无限扩展。  

#### 复杂度  

- **时间复杂度**：`O(5^D * G)`（`D` 为我们到目标的曼哈顿距离，`G` 为幽灵数量）。这里的 `5^D` 来自每一步 5 种移动选择的指数增长，`G` 是因为每只幽灵的所有可能位置都要展开。  
  - 大白话：如果目标离我们 10 步远，可能的路径数已经接近 10 百万，计算机会吃不消。  
- **空间复杂度**：`O(5^D + D * G)`。我们需要保存每一步的所有可能位置以及每只幽灵的可能坐标集合，同样是指数级的。  

---

### 2. 最优解  

#### 思路  

从暴力解出发，**慢的地方**在于我们把每一步的所有可能路径都枚举了。事实上，**在 Manhattan（曼哈顿）距离** 的意义下，**我们每走一步，离目标的距离必然至少减少 1**（因为只能向四个方向走）。同理，幽灵也遵循同样的规则：它们也只能每回合把自己和我们的距离（或目标的距离）缩短最多 1。  

**关键观察**：  
- 我们从原点 `(0,0)` 到目标 `(xt, yt)` 的 **最短步数** 正好是 `|xt| + |yt|`（横向走 `|xt|` 步，纵向走 `|yt|` 步），这叫 **曼哈顿距离**。  
- 对于任意幽灵 `gi = (xi, yi)`，它从起点走到同一个目标点的最短步数是 `|xi - xt| + |yi - yt|`。  
- 因为所有玩家（我们和幽灵）在每回合可以 **同步移动**，**如果有任何幽灵的最短步数 ≤ 我们的最短步数**，那么这只幽灵至少可以在我们到达目标的同一回合（甚至更早）抢先占据目标或拦截我们。题目要求“**必须在幽灵到达我们之前**”才能逃脱，**同步到达不算逃脱**。  

因此，只要把我们和每只幽灵的曼哈顿距离算出来，**比较大小**，即可在 **O(n)**（`n` 为幽灵数量）时间内得到答案。  

**类比**：  
想象你在一条直线的起点，目标在终点。你和每个对手只能一次前进一步。谁的起点离终点更近，谁就能先到。这里的“直线”换成二维的“曼哈顿网格”，但原则完全相同。  

#### 代码（Python）  

```python
from typing import List

def escapeGhosts(ghosts: List[List[int]], target: List[int]) -> bool:
    """
    判断是否一定可以在所有幽灵之前到达 target。
    思路：比较曼哈顿距离——只要有任意幽灵的距离 <= 我们的距离，就无法逃脱。
    """
    # 我们从原点到目标的最短步数（曼哈顿距离）
    my_dist = abs(target[0]) + abs(target[1])

    # 遍历每只幽灵，计算它到目标的最短步数
    for gx, gy in ghosts:
        ghost_dist = abs(gx - target[0]) + abs(gy - target[1])
        # 若幽灵的距离不大于我们的距离，说明它能在我们之前或同一回合到达
        if ghost_dist <= my_dist:
            return False          # 逃脱失败

    # 所有幽灵的距离都严格大于我们，必然可以先到达
    return True
```

> **关键行中文注释**  
> - `my_dist`：把“我离终点有多远”用 **曼哈顿距离** 表示。  
> - `ghost_dist`：同理，算每只幽灵离终点的最近步数。  
> - `if ghost_dist <= my_dist: return False`：只要有一只幽灵 **不慢于** 我们，就说明它有办法在我们到达前（或同一回合）拦截，逃脱不成立。  

#### 复杂度  

- **时间复杂度**：`O(g)`，其中 `g = len(ghosts)`。我们只遍历一次幽灵数组，算一次曼哈顿距离，**不随坐标大小变化**。  
  - 与暴力解 `O(5^D)` 相比，**线性** 的时间几乎是瞬间完成的。  
- **空间复杂度**：`O(1)`，只用了常数级别的额外变量（两个整数）。  

---

## 心得  

- **核心技巧**：**曼哈顿距离**（Manhattan distance）比较。  
- **适用的题型**（类似思路）  
  1. *“Can you reach the destination before the enemy?”*（如 LeetCode 1312 Escape The Ghosts）  
  2. *“最短路径在网格中只允许上下左右移动”* 的问题（如 0‑1 BFS 里只关心距离大小）  
  3. *“两个点的相对先后到达”* 类的几何/坐标题目（如判断骑士、国王是否先到）  
- **一句话总结解题钥匙**：**只要比较出发点到目标的曼哈顿距离，谁的距离更小谁就先到**，不需要真正模拟移动过程。  

---

## 反思  

- **第一反应**：看到“每回合都可以向四个方向移动”，本能想把所有可能的走法枚举（即暴力搜索）。  
- **最容易踩的坑**  
  - **同步到达不算逃脱**：必须使用 `<=` 而不是 `<` 来比较距离。  
  - **负坐标**：曼哈顿距离使用绝对值，忽略正负号，否则会出现错误。  
  - **多只幽灵**：只要有一只幽灵满足条件就直接返回 `False`，不需要所有都比较完再判断。  
- **下次遇到同类题**：第一步就思考“有没有一种**距离度量**（曼哈顿、欧氏、Chebyshev）能直接把移动次数转化为数值”，把问题从“如何走”转化为“谁的数值更小”。这样往往能立刻得到 **O(n)** 的最优解。