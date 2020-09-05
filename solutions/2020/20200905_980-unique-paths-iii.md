# #980. 不同路径 III / Unique Paths III

> 难度：困难 · 标签：Array、Backtracking、Bit Manipulation、Matrix · [LeetCode 链接](https://leetcode.com/problems/unique-paths-iii/)

---

## 题目（英文原版）

**Description**

You are given an m x n integer array grid where grid[i][j] could be:
Return the number of 4-directional walks from the starting square to the ending square, that walk over every non-obstacle square exactly once.

**Examples**

**Example 1:**

```
Input: grid = [[1,0,0,0],[0,0,0,0],[0,0,2,-1]]
Output: 2
Explanation: We have the following two paths: 
1. (0,0),(0,1),(0,2),(0,3),(1,3),(1,2),(1,1),(1,0),(2,0),(2,1),(2,2)
2. (0,0),(1,0),(2,0),(2,1),(1,1),(0,1),(0,2),(0,3),(1,3),(1,2),(2,2)
```

**Example 2:**

```
Input: grid = [[1,0,0,0],[0,0,0,0],[0,0,0,2]]
Output: 4
Explanation: We have the following four paths: 
1. (0,0),(0,1),(0,2),(0,3),(1,3),(1,2),(1,1),(1,0),(2,0),(2,1),(2,2),(2,3)
2. (0,0),(0,1),(1,1),(1,0),(2,0),(2,1),(2,2),(1,2),(0,2),(0,3),(1,3),(2,3)
3. (0,0),(1,0),(2,0),(2,1),(2,2),(1,2),(1,1),(0,1),(0,2),(0,3),(1,3),(2,3)
4. (0,0),(1,0),(2,0),(2,1),(1,1),(0,1),(0,2),(0,3),(1,3),(1,2),(2,2),(2,3)
```

**Example 3:**

```
Input: grid = [[0,1],[2,0]]
Output: 0
Explanation: There is no path that walks over every empty square exactly once.
Note that the starting and ending square can be anywhere in the grid.
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 20
- 1 <= m * n <= 20
- -1 <= grid[i][j] <= 2
- There is exactly one starting cell and one ending cell.

---

## 题目（中文翻译）

你得到一个 `m × n` 的整数矩阵 `grid`，其中 `grid[i][j]` 的取值含义如下：

- `-1` 表示障碍格子（obstacle），不可踏入。  
- `0` 表示空格子（empty square），可以走。  
- `1` 表示起始格子（starting square），路径必须从这里出发。  
- `2` 表示结束格子（ending square），路径必须在这里结束。  

返回从起始格子走到结束格子的 **4 方向**（上下左右）路径的数量，要求路径恰好走遍所有非障碍格子一次且仅一次。

**示例 1**  
Input: `grid = [[1,0,0,0],[0,0,0,0],[0,0,2,-1]]`  
Output: `2`  
Explanation: 我们有以下两条路径：  
1. `(0,0),(0,1),(0,2),(0,3),(1,3),(1,2),(1,1),(1,0),(2,0),(2,1),(2,2)`  
2. `(0,0),(1,0),(2,0),(2,1),(1,1),(0,1),(0,2),(0,3),(1,3),(1,2),(2,2)`

**示例 2**  
Input: `grid = [[1,0,0,0],[0,0,0,0],[0,0,0,2]]`  
Output: `4`  
Explanation: 我们有以下四条路径：  
1. `(0,0),(0,1),(0,2),(0,3),(1,3),(1,2),(1,1),(1,0),(2,0),(2,1),(2,2),(2,3)`  
2. `(0,0),(0,1),(1,1),(1,0),(2,0),(2,1),(2,2),(1,2),(0,2),(0,3),(1,3),(2,3)`  
3. `(0,0),(1,0),(2,0),(2,1),(2,2),(1,2),(1,1),(0,1),(0,2),(0,3),(1,3),(2,3)`  
4. `(0,0),(1,0),(2,0),(2,1),(1,1),(0,1),(0,2),(0,3),(1,3),(1,2),(2,2),(2,3)`

**示例 3**  
Input: `grid = [[0,1],[2,0]]`  
Output: `0`  
Explanation: 没有任何路径能够恰好走遍所有空格子一次。

注意，起始格子和结束格子可以位于网格中的任意位置。

**约束条件**  
- `m == grid.length`  
- `n == grid[i].length`  
- `1 ≤ m, n ≤ 20`  
- `1 ≤ m × n ≤ 20`  
- `-1 ≤ grid[i][j] ≤ 2`  
- grid 中恰好只有一个起始格子和一个结束格子。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把题目当成「在网格里走路」的深度优先搜索（DFS）问题。  
- **网格**：想象成一张棋盘，每个格子可以是起点 `1`、终点 `2`、普通空格 `0` 或障碍 `-1`（相当于不能走的格子）。  
- **走法**：从起点出发，每次可以向上、下、左、右四个方向移动一步（就像走迷宫）。  
- **要求**：必须恰好走遍所有非障碍格子一次，且最后停在终点。

实现上我们把每个格子当作 **节点**，用递归的 DFS 去尝试所有可能的走法。  
在递归过程中：

1. 记录已经走过的格子数量 `visited_cnt`。  
2. 当前格子标记为已访问（可以把它改成 `-1`，相当于“临时障碍”，防止回头走）。  
3. 对四个方向尝试移动：如果新位置在棋盘内且不是障碍且未被访问，就继续递归。  
4. 当走到终点时检查 `visited_cnt` 是否等于 **所有可走格子总数**，若相等则找到一条合法路径，计数加一。  
5. 递归返回前，把当前格子恢复原状（撤销标记），继续尝试其它方向——这一步叫 **回溯**。

> **为什么正确**  
> DFS 会枚举所有可能的走法。我们只在满足「恰好走遍所有可走格子」的情况下计数，因此每条合法路径都被统计一次，且不会漏掉。

> **时间/空间复杂度**  
> - 每一步最多有 4 种选择，最坏情况下会遍历所有排列组合。设可走格子数为 `k`（`k ≤ 20`），则时间复杂度约为 `O(4^k)`，实际会因为边界和障碍而大幅剪枝。  
> - 递归深度最多为 `k`，需要额外的栈空间 `O(k)`，以及原始网格 `O(m·n)` 的存储。

#### 代码（Python）

```python
from typing import List

def uniquePathsIII(grid: List[List[int]]) -> int:
    m, n = len(grid), len(grid[0])

    # 统计可走格子（0、1、2）的数量，并找到起点坐标
    empty_cnt = 0
    start_x = start_y = -1
    for i in range(m):
        for j in range(n):
            if grid[i][j] != -1:          # 不是障碍
                empty_cnt += 1
            if grid[i][j] == 1:           # 起点
                start_x, start_y = i, j

    # 四个方向向量
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def dfs(x: int, y: int, visited: int) -> int:
        """从 (x, y) 出发，已经走过 visited 个格子，返回合法路径数量"""
        # 如果来到终点
        if grid[x][y] == 2:
            # 必须恰好走遍所有可走格子
            return 1 if visited == empty_cnt else 0

        # 把当前格子标记为已访问，防止再次进入
        tmp = grid[x][y]
        grid[x][y] = -1          # 相当于临时障碍

        total = 0
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            # 判断新坐标是否合法且不是障碍
            if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] != -1:
                total += dfs(nx, ny, visited + 1)

        # 回溯：恢复原来的格子值
        grid[x][y] = tmp
        return total

    # 起点已经算作第一个已访问格子
    return dfs(start_x, start_y, 1)
```

#### 复杂度  

- **时间复杂度**：`O(4^k)`（`k` 为可走格子数），大致意思是「每走一步最多有四条路要尝试，最坏情况下要尝遍所有可能的走法」。  
- **空间复杂度**：`O(k)`，递归栈的深度最多等于可走格子数（最多 20），加上原始网格本身的存储 `O(m·n)`。

---

### 2. 最优解

#### 思路  

暴力 DFS 已经能够在题目限制（`m·n ≤ 20`）下 AC，但我们仍可以通过**位运算**把「已经走过的格子」信息压缩到一个整数里，从而：

1. **快速判断是否已经访问过**：用位掩码 `mask`，第 `p` 位为 1 表示第 `p` 个格子已经走过。检查/设置只需要 O(1) 的位运算。  
2. **减少重复状态**：如果同一个位置、同样的访问掩码已经被遍历过，就不必再搜索（记忆化搜索）。这相当于在 DFS 基础上加了 **缓存**（`memo[(x, y, mask)]`），避免了指数级的重复计算。

**核心概念——位掩码**  
把网格展平成一维序列（比如行主序），每个格子对应一个编号 `idx = i * n + j`。  
- `1 << idx` 表示「第 idx 格子」对应的二进制位。  
- `mask & (1 << idx)` 用来判断该格子是否已被访问。  
- `mask | (1 << idx)` 用来把该格子标记为已访问。

**步骤概览**  

1. 预处理：统计可走格子数 `empty_cnt`，记录起点、终点的编号 `start_idx`、`end_idx`。  
2. 递归函数 `dfs(pos, mask)`：  
   - `pos` 是当前格子的一维编号。  
   - `mask` 是已经走过的格子的位掩码。  
   - 递归结束条件：若 `pos == end_idx`，只有当 `mask` 恰好包含所有可走格子（`mask == full_mask`）时才计为 1。  
   - 否则，对四个方向的相邻格子 `next_pos` 进行遍历：如果该格子不是障碍且在 `mask` 中未出现，就递归 `dfs(next_pos, mask | (1 << next_pos))`。  
3. 使用 `@lru_cache(None)`（或手写 dict）对 `(pos, mask)` 进行记忆化，避免重复子问题。  
4. 初始调用 `dfs(start_idx, 1 << start_idx)`，返回结果。

> **为什么更快**  
> - 位掩码把「已访问集合」压成一个整数，比较、更新都只需要常数时间。  
> - 记忆化把相同的子状态合并，只会计算一次，整体搜索树的规模从指数级下降到约 `O(k·2^k)`（`k ≤ 20`），在本题数据范围内极其快。

> **时间/空间解释**  
> - `2^k` 表示「所有可能的访问集合」的数量（因为每个格子要么走过要么没走）。乘以 `k`（当前位置的选择）得到总体状态数。  
> - 空间主要是缓存表的大小，也大约是 `k·2^k` 条记录，最多几百万条，完全可以放在内存里。

#### 代码（Python）

```python
from typing import List
from functools import lru_cache

def uniquePathsIII(grid: List[List[int]]) -> int:
    m, n = len(grid), len(grid[0])

    # 将二维坐标映射到一维编号：idx = i * n + j
    def idx(i: int, j: int) -> int:
        return i * n + j

    start = end = -1
    empty_cnt = 0

    for i in range(m):
        for j in range(n):
            if grid[i][j] != -1:                # 不是障碍，都算作可走格子
                empty_cnt += 1
            if grid[i][j] == 1:
                start = idx(i, j)
            elif grid[i][j] == 2:
                end = idx(i, j)

    # 所有可走格子都被访问时的掩码（全 1）
    full_mask = (1 << empty_cnt) - 1   # 这里我们只对可走格子编号，后面会映射

    # 为了让位掩码只关心可走格子，我们需要把每个可走格子映射到 [0, empty_cnt)
    # 创建映射表：原始 idx -> 压缩后的 bit 位
    compress = {}
    bit = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] != -1:
                orig = idx(i, j)
                compress[orig] = bit
                bit += 1

    start_bit = compress[start]
    end_bit   = compress[end]

    # 四个方向的移动向量（仍然用二维坐标计算）
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    @lru_cache(None)
    def dfs(pos: int, mask: int) -> int:
        """从压缩后位置 pos 出发，已走过的格子集合为 mask，返回合法路径数"""
        # 如果已经到达终点
        if pos == end_bit:
            # mask 必须恰好覆盖所有可走格子
            return 1 if mask == full_mask else 0

        total = 0
        # 将压缩后的位恢复成原始坐标，方便找相邻格子
        i, j = divmod(pos_to_orig[pos], n)   # pos_to_orig 下面会定义

        for dx, dy in dirs:
            ni, nj = i + dx, j + dy
            if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] != -1:
                nxt_orig = idx(ni, nj)
                nxt_bit = compress[nxt_orig]
                if not (mask >> nxt_bit) & 1:          # 该格子未被访问
                    total += dfs(nxt_bit, mask | (1 << nxt_bit))
        return total

    # 为了在 dfs 中把压缩位快速转回原始坐标，需要一个逆映射数组
    pos_to_orig = [0] * empty_cnt
    for orig, b in compress.items():
        pos_to_orig[b] = orig

    # 初始状态：只访问起点
    return dfs(start_bit, 1 << start_bit)
```

> **代码要点注释**  
> 1. `compress` 把每个 **实际格子** 编号映射到 **连续的位序号**（0~k‑1），这样 `full_mask` 就是 `k` 个 1。  
> 2. `@lru_cache(None)` 自动为函数 `dfs` 做记忆化，键是 `(pos, mask)`。  
> 3. `mask | (1 << nxt_bit)` 表示「把下一个格子标记为已走」。  
> 4. 当 `pos == end_bit` 时检查 `mask == full_mask`，确保所有可走格子都恰好走过一次。

#### 复杂度  

- **时间复杂度**：`O(k * 2^k)`，其中 `k` 为可走格子数（`k ≤ 20`）。解释为「每个格子可能是当前所在位置（k 种），每种位置对应的访问集合有 `2^k` 种」，而记忆化把每种状态只计算一次。相较于暴力的 `O(4^k)`，指数基数从 4 降到 2，速度提升显著。  
- **空间复杂度**：`O(k * 2^k)` 用于缓存表，加上递归栈深度 `O(k)`，总体仍在可接受范围（约几百万条记录，几百 MB 以下）。

---

## 心得  

- **核心技巧**：**回溯 + 位掩码 + 记忆化搜索**。  
- **适用的题型**：  
  1. “遍历所有格子一次”的路径类题目，如 *Unique Paths II*、*Hamiltonian Path*（在小图中）  
  2. 需要记录集合状态的搜索题，如 *Word Search II*（可以用位掩码记录已使用的单词）  
  3. “在小规模状态空间中求最优/计数”的 DP/搜索题，例如 *TSP（旅行商问题）* 的位 DP 形式。  
- **一句话总结**：**把“已经走过哪些格子”压成一个整数，用缓存防止重复搜索，既能保证走遍所有格子，又能大幅加速。**

---

## 反思  

- **第一反应**：直接写一个 DFS，记录已经走过的格子并在终点检查是否全部访问。  
- **最容易踩的坑**：  
  - **计数错误**：忘记把起点本身算进已访问格子，导致 `visited_cnt` 与实际格子数不匹配。  
  - **边界条件**：终点可能在四周被障碍包围，需要在递归里先判断是否已经到达终点再检查访问完整性。  
  - **状态重复**：没有记忆化会导致大量相同子树的重复计算，时间会爆炸。  
- **下次思路**：遇到“遍历全部格子一次”或“每个格子只能使用一次”的小规模网格/集合问题，第一步就想到 **位掩码 + 记忆化**，再决定是否需要回溯搜索。这样可以在保证正确性的同时，尽可能把时间控制在 `k·2^k` 量级。