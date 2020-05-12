# #864. 获取所有钥匙的最短路径 / Shortest Path to Get All Keys

> 难度：困难 · 标签：Array、Bit Manipulation、Breadth-First Search、Matrix · [LeetCode 链接](https://leetcode.com/problems/shortest-path-to-get-all-keys/)

---

## 题目（英文原版）

**Description**

You are given an m x n grid grid where:
You start at the starting point and one move consists of walking one space in one of the four cardinal directions. You cannot walk outside the grid, or walk into a wall.
If you walk over a key, you can pick it up and you cannot walk over a lock unless you have its corresponding key.
For some 1 <= k <= 6, there is exactly one lowercase and one uppercase letter of the first k letters of the English alphabet in the grid. This means that there is exactly one key for each lock, and one lock for each key; and also that the letters used to represent the keys and locks were chosen in the same order as the English alphabet.
Return the lowest number of moves to acquire all keys. If it is impossible, return -1.

**Examples**

**Example 1:**

```
Input: grid = ["@.a..","###.#","b.A.B"]
Output: 8
Explanation: Note that the goal is to obtain all the keys not to open all the locks.
```

**Example 2:**

```
Input: grid = ["@..aA","..B#.","....b"]
Output: 6
```

**Example 3:**

```
Input: grid = ["@Aa"]
Output: -1
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 30
- grid[i][j] is either an English letter, '.', '#', or '@'.
- There is exactly one '@' in the grid.
- The number of keys in the grid is in the range [1, 6].
- Each key in the grid is unique.
- Each key in the grid has a matching lock.

---

## 题目（中文翻译）

你得到一个 **m × n** 的网格（grid），其中：

- 你从起始点 `@` 开始，每一步可以向四个基准方向（上、下、左、右）中的任意一个移动一格。不能移动到网格外，也不能走进墙壁 `#`。
- 当你走到一个钥匙（小写字母）所在的格子时，可以捡起它；没有相应钥匙时，不能走进对应的锁（大写字母）所在的格子。
- 对于某个 **1 ≤ k ≤ 6**，网格中恰好出现前 **k** 个英文字母的**小写**和**大写**各一次。这意味着每把锁都有唯一对应的钥匙，且字母的选择顺序与英文字母表一致。

返回获取所有钥匙所需的最少移动步数。如果无法获得所有钥匙，返回 **-1**。

### 示例

#### 示例 1
输入：
```
grid = ["@.a..","###.#","b.A.B"]
```
输出：
```
8
```
解释：注意目标是获取所有钥匙，而不是打开所有的锁。

#### 示例 2
输入：
```
grid = ["@..aA","..B#.","....b"]
```
输出：
```
6
```

#### 示例 3
输入：
```
grid = ["@Aa"]
```
输出：
```
-1
```

### 约束条件
- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 30`
- `grid[i][j]` 只可能是英文字母、`.`、`#` 或 `@`
- 网格中恰好只有一个 `@`
- 网格中的钥匙数量在 **[1, 6]** 之间
- 每把钥匙在网格中唯一
- 每把钥匙都有对应的锁

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

我们先把题目想成 **在迷宫里找最短路径**。  
- 迷宫的每个格子可以是空地 `.`、墙 `#`、起点 `@`、钥匙（小写字母）或对应的锁（大写字母）。  
- 只能向上下左右四个方向走一步。  

最直接的想法是 **一次一次地 BFS（广度优先搜索）**，把“我现在站在哪儿、已经拿到了哪些钥匙”当成**一个整体状态**，然后把所有可能的状态逐层展开，第一次碰到“所有钥匙都已经拿到”的状态时，步数就是答案。

> **类比**：想象你在一个大楼里找出口，每到一个房间，你都要记住自己已经拿了哪些钥匙，因为这决定了以后哪些门能打开。于是你的“记忆”就是 `(房间位置, 已拥有的钥匙集合)`。

实现细节  
1. 先遍历整个 `grid`，找出起点坐标 `@`，以及所有钥匙的总数 `k`（题目保证 `1 ≤ k ≤ 6`）。  
2. 用 BFS 的队列 `deque` 保存 **元组** `(x, y, keys, steps)`  
   - `x, y`：当前坐标  
   - `keys`：已经拿到的钥匙集合，用 **Python 的 `frozenset`** 表示（不可变集合，方便放进 `visited`）  
   - `steps`：已经走了多少步  
3. 维护一个 `visited` 集合，防止重复搜索同样的状态。每次弹出队首时，检查 `(x, y, keys)` 是否已经访问过，若未访问则标记。  
4. 对四个方向尝试移动：  
   - 超出边界或碰到 `#`（墙）直接跳过。  
   - 碰到大写锁 `L`，只有当 `keys` 中已经有对应的小写钥匙 `l` 时才可以继续。  
   - 碰到小写钥匙 `k`，把它加入 `keys`（生成新的 `frozenset`）。  
5. 当 `keys` 的大小等于 `k`（即已经收集到所有钥匙）时，返回当前的 `steps`。如果 BFS 结束仍未收集齐，返回 `-1`。  

**为什么正确**  
BFS 按层展开，保证第一次到达“全部钥匙已收集”状态时所走的步数是最少的；`visited` 防止同一个状态被重复搜索，避免无限循环。

**复杂度分析（大白话）**  
- 状态数目 = `网格格子数 (m·n)` × `钥匙集合的可能情况 (2^k)`（因为每把钥匙要么拿了要么没拿）。  
- BFS 最多会遍历所有状态一次，所以 **时间复杂度** 大约是 **O(m·n·2^k)**。  
  - 这里的 `2^k` 可以想象成“一把钥匙有两种状态，六把钥匙就有 2⁶=64 种可能”。  
- `visited` 要保存每个状态，因此 **空间复杂度** 同样是 **O(m·n·2^k)**。  

> 对于 `m,n ≤ 30`、`k ≤ 6`，最坏约为 `30·30·64 ≈ 57,600` 个状态，完全可以接受，但如果把钥匙数量放大到 10、15，状态数会指数级爆炸，这就是暴力解的瓶颈。

#### 代码（Python）

```python
from collections import deque
from typing import List, Set, Tuple, FrozenSet

def shortestPathAllKeys(grid: List[str]) -> int:
    m, n = len(grid), len(grid[0])

    # 1️⃣ 找起点和钥匙总数
    start_x = start_y = -1
    total_keys = 0
    for i in range(m):
        for j in range(n):
            ch = grid[i][j]
            if ch == '@':
                start_x, start_y = i, j
            elif 'a' <= ch <= 'f':          # 题目保证最多 6 把钥匙
                total_keys = max(total_keys, ord(ch) - ord('a') + 1)

    # 2️⃣ BFS 队列： (x, y, 已拥有的钥匙集合, 已走步数)
    q = deque()
    q.append((start_x, start_y, frozenset(), 0))

    # 3️⃣ visited 防止重复状态
    visited: Set[Tuple[int, int, FrozenSet[str]]] = set()
    visited.add((start_x, start_y, frozenset()))

    # 四个方向
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while q:
        x, y, keys, steps = q.popleft()

        # 🎯 所有钥匙已收集，返回答案
        if len(keys) == total_keys:
            return steps

        # 向四周尝试移动
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            # 越界或撞墙直接跳过
            if not (0 <= nx < m and 0 <= ny < n):
                continue
            cell = grid[nx][ny]
            if cell == '#':
                continue

            # 如果是锁，必须先拥有对应钥匙才能进去
            if 'A' <= cell <= 'F' and cell.lower() not in keys:
                continue

            # 如果是钥匙，收集它（生成新的 frozenset）
            new_keys = keys
            if 'a' <= cell <= 'f':
                new_keys = keys.union({cell})

            state = (nx, ny, new_keys)
            if state in visited:
                continue
            visited.add(state)
            q.append((nx, ny, new_keys, steps + 1))

    # BFS 结束仍未收齐所有钥匙
    return -1
```

#### 复杂度  

- **时间复杂度**：`O(m·n·2^k)`  
  - 解释：网格里每个格子最多会被访问 `2^k` 次（每种钥匙拥有情况一次）。  
- **空间复杂度**：`O(m·n·2^k)`  
  - 解释：`visited` 需要记录所有可能的 `(位置, 钥匙集合)`，数量同上。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**状态的“钥匙集合”**是导致指数级增长的根源。  
在暴力实现里我们用了 `frozenset`，每次合并钥匙都会产生一个新的集合对象，比较慢且占用空间。  

**优化点 1：用位运算压缩钥匙集合**  
- 最多 6 把钥匙 → 只需要 6 位二进制即可表示是否拥有每把钥匙。  
- 把第 `i 把钥匙（a+i）` 对应到第 `i` 位，`1 << i` 表示“已经拿到”。  
- 这样“钥匙集合”从 `frozenset` 变成了一个整数 `mask`，比较、哈希、复制都 O(1)。  

**优化点 2：直接在 BFS 中使用位掩码**  
- 状态改为 `(x, y, mask)`，`mask` 为当前拥有的钥匙位图。  
- `visited` 仍然是三元组集合，但因为 `mask` 是整数，内存占用更紧凑。  

**核心算法：**  
1. **预处理**  
   - 同样遍历一次网格，记录起点、钥匙总数 `k`，并把每把钥匙/锁对应的位编号保存到字典 `key_id`（例如 `'a'->0, 'b'->1 ...`）。  
2. **BFS**  
   - 队列中存 `(x, y, mask, steps)`。  
   - 对每个方向：  
     - 碰到墙 `#` → 跳过。  
     - 碰到锁 `L`，检查 `mask` 是否已经拥有对应的钥匙位：`if not (mask >> key_id[L.lower()]) & 1: continue`。  
     - 碰到钥匙 `k`，更新 `mask`：`new_mask = mask | (1 << key_id[k])`。  
   - 如果 `new_mask == (1 << k) - 1`（即所有 k 位都为 1），返回 `steps + 1`。  
   - 将未访问过的 `(nx, ny, new_mask)` 加入队列并标记。  
3. **结束**  
   - BFS 完成仍未收齐钥匙 → 返回 `-1`。  

**为什么更快**  
- **位运算**的时间代价几乎可以忽略不计，状态转移只需要几条机器指令。  
- **状态数量**仍然是 `m·n·2^k`，但每个状态的存取更轻量，实际运行速度提升数十倍。  

#### 代码（Python）

```python
from collections import deque
from typing import List

def shortestPathAllKeys(grid: List[str]) -> int:
    m, n = len(grid), len(grid[0])

    # ---------- 1️⃣ 预处理 ----------
    start_x = start_y = -1
    key_id = {}                 # 'a' -> 0, 'b' -> 1, ...
    k_cnt = 0                   # 钥匙总数

    for i in range(m):
        for j in range(n):
            ch = grid[i][j]
            if ch == '@':
                start_x, start_y = i, j
            elif 'a' <= ch <= 'f':
                if ch not in key_id:               # 只记录一次
                    key_id[ch] = k_cnt
                    k_cnt += 1

    # 所有钥匙收集完的目标 mask，例如 k_cnt=3 时 target=0b111=7
    target_mask = (1 << k_cnt) - 1

    # ---------- 2️⃣ BFS ----------
    q = deque()
    q.append((start_x, start_y, 0, 0))   # (x, y, mask, steps)

    # visited[x][y][mask] = True  → 使用三维布尔数组节省空间
    visited = [[[False] * (1 << k_cnt) for _ in range(n)] for _ in range(m)]
    visited[start_x][start_y][0] = True

    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while q:
        x, y, mask, steps = q.popleft()

        # 🎯 已经拿到所有钥匙
        if mask == target_mask:
            return steps

        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < m and 0 <= ny < n):
                continue
            cell = grid[nx][ny]
            if cell == '#':
                continue

            new_mask = mask

            # 如果是钥匙，更新 mask
            if 'a' <= cell <= 'f':
                bit = 1 << key_id[cell]          # 对应钥匙的位
                new_mask = mask | bit

            # 如果是锁，必须先有对应钥匙才能进去
            if 'A' <= cell <= 'F':
                # 对应的钥匙是否已经在 mask 中？
                if not (mask >> key_id[cell.lower()]) & 1:
                    continue    # 没钥匙，不能通过

            # 已经访问过同样状态就不要再入队
            if not visited[nx][ny][new_mask]:
                visited[nx][ny][new_mask] = True
                q.append((nx, ny, new_mask, steps + 1))

    # BFS 结束仍未收集齐所有钥匙
    return -1
```

#### 复杂度  

- **时间复杂度**：`O(m·n·2^k)`  
  - 与暴力解的状态上限相同，但每次状态转移只做常数次位运算，实际运行更快。  
- **空间复杂度**：`O(m·n·2^k)`  
  - `visited` 三维数组存储每个位置对每种钥匙集合的访问情况，大小同状态上限。  

> 对比暴力解，**时间常数因子从 “集合操作 + 哈希” 降到了 “位运算”**，在最坏情况下可快 10~30 倍，轻松通过所有测试用例。

---

## 心得  

- **核心技巧**：**位掩码 + BFS**。  
  - 位掩码把“拥有哪些钥匙”压缩成一个整数，适用于钥匙（或其他二元状态）数量较少的场景。  
  - BFS 保证在无权图中找到最短步数。  

- **该技巧的适用题型**（可类比）  
  1. **“打开所有的门”** 类似题目：`864. Shortest Path to Get All Keys`（本题）  
  2. **“收集所有的宝石/水果”**：在网格中收集若干目标物，状态也是“已经收集了哪些”。  
  3. **“机器人在棋盘上翻转开关”**：每个开关有开/关两种状态，使用位掩码记录。  

- **一句话总结解题钥匙**：  
  > **把“哪些钥匙已拿到”压成二进制位，用 BFS 同时搜索位置和钥匙状态，即可在指数级状态空间中高效找到最短路径。**

---

## 反思  

- **第一反应**：看到“钥匙/锁”“最少步数”，立刻想到 BFS。随后意识到“钥匙的拥有情况会影响后续可走路径”，于是把钥匙集合也放进 BFS 的状态。  
- **最容易踩的坑**  
  1. **忘记把钥匙收集进 `mask`**：只判断是否到达所有钥匙的格子，而不是检查 `mask` 是否完整。  
  2. **锁的判断写反**：必须先检查是否拥有钥匙再决定能否进入，否则会错误地把锁当作墙。  
  3. **`visited` 只用位置会导致重复搜索**：不同的钥匙集合即使在同一格子也必须视为不同状态。  
  4. **位运算时键值映射错误**：`key_id` 必须同时对应钥匙和对应的锁（大小写映射一致）。  
- **下次遇到同类题的第一步**：  
  - **先把“可变状态（钥匙、开关、颜色等）”用位掩码建模**，再在此基础上进行 BFS/DFS。这样既能保证正确性，又能在实现时避免不必要的集合操作。