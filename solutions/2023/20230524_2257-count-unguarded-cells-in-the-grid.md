# #2257. 统计网格中未受守卫的单元格 / Count Unguarded Cells in the Grid

> 难度：中等 · 标签：Array、Matrix、Simulation · [LeetCode 链接](https://leetcode.com/problems/count-unguarded-cells-in-the-grid/)

---

## 题目（英文原版）

**Description**

You are given two integers m and n representing a 0-indexed m x n grid. You are also given two 2D integer arrays guards and walls where guards[i] = [rowi, coli] and walls[j] = [rowj, colj] represent the positions of the ith guard and jth wall respectively.
A guard can see every cell in the four cardinal directions (north, east, south, or west) starting from their position unless obstructed by a wall or another guard. A cell is guarded if there is at least one guard that can see it.
Return the number of unoccupied cells that are not guarded.

**Examples**

**Example 1:**

```
Input: m = 4, n = 6, guards = [[0,0],[1,1],[2,3]], walls = [[0,1],[2,2],[1,4]]
Output: 7
Explanation: The guarded and unguarded cells are shown in red and green respectively in the above diagram.
There are a total of 7 unguarded cells, so we return 7.
```

**Example 2:**

```
Input: m = 3, n = 3, guards = [[1,1]], walls = [[0,1],[1,0],[2,1],[1,2]]
Output: 4
Explanation: The unguarded cells are shown in green in the above diagram.
There are a total of 4 unguarded cells, so we return 4.
```

**Constraints**

- 1 <= m, n <= 105
- 2 <= m * n <= 105
- 1 <= guards.length, walls.length <= 5 * 104
- 2 <= guards.length + walls.length <= m * n
- guards[i].length == walls[j].length == 2
- 0 <= rowi, rowj < m
- 0 <= coli, colj < n
- All the positions in guards and walls are unique.

---

## 题目（中文翻译）

给定两个整数 `m` 和 `n`，表示一个 **0 索引（0-indexed）** 的 `m × n` **网格（grid）**。同时提供两个二维整数数组 `guards` 和 `walls`，其中 `guards[i] = [row_i, col_i]` 表示第 `i` 位 **守卫（guard）** 的位置，`walls[j] = [row_j, col_j]` 表示第 `j` 面 **墙（wall）** 的位置。

每个守卫可以沿四个基准方向（**北（north）**、**东（east）**、**南（south）**、**西（west）**）看到其所在位置起的所有单元格，除非视线被墙或其他守卫阻挡。只要至少有一名守卫能够看到某个单元格，该单元格即被视为 **受守卫（guarded）**。

返回网格中 **未被占用且未受守卫** 的单元格数量。

### 示例 1  
**输入**  
```text
m = 4, n = 6, guards = [[0,0],[1,1],[2,3]], walls = [[0,1],[2,2],[1,4]]
```  
**输出**  
```text
7
```  
**解释**：图中用红色标记的为受守卫的单元格，绿色标记的为未受守卫的单元格。未受守卫的单元格总数为 7，故返回 7。

### 示例 2  
**输入**  
```text
m = 3, n = 3, guards = [[1,1]], walls = [[0,1],[1,0],[2,1],[1,2]]
```  
**输出**  
```text
4
```  
**解释**：图中用绿色标记的为未受守卫的单元格。未受守卫的单元格总数为 4，故返回 4。

### 约束条件
- `1 ≤ m, n ≤ 10^5`
- `2 ≤ m × n ≤ 10^5`
- `1 ≤ guards.length, walls.length ≤ 5 × 10^4`
- `2 ≤ guards.length + walls.length ≤ m × n`
- `guards[i].length == walls[j].length == 2`
- `0 ≤ row_i, row_j < m`
- `0 ≤ col_i, col_j < n`
- `guards` 和 `walls` 中的所有位置互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：

1. 先把整个 `m × n` 的网格建立成一个二维数组 `grid`，  
   - `0` 表示空格，  
   - `1` 表示守卫（guard），  
   - `2` 表示墙（wall），  
   - `3` 表示已经被守卫看到的格子（guarded）。

2. 对每一个守卫，沿着 **上下左右** 四个方向一步一步往前走，  
   - 只要没有碰到墙或另一名守卫，就把路过的格子标记为 `3`（受守卫保护）。  
   - 碰到墙或守卫就停下来，因为视线被阻断。

3. 最后遍历整个网格，统计既不是守卫也不是墙、也没有被标记为 `3` 的格子数量——这就是“未受保护的空格”。

> **类比**：把网格想象成一张大地图，守卫就像灯塔，灯光沿四个方向直射，墙壁相当于挡光的山。只要灯光到达的地方，就算被照亮（受保护）。

> **为什么正确**：守卫的视线只能在四个正交方向上直线延伸，且只能被墙或另一守卫阻断。我们按照这条规则逐格扫描，所有能够被看到的格子必然会被标记，未被标记的格子自然就是不受守卫视线覆盖的。

#### 代码（Python）

```python
def countUnguarded(m: int, n: int, guards: list[list[int]], walls: list[list[int]]) -> int:
    # 0：空格，1：守卫，2：墙，3：已被守卫看到
    grid = [[0] * n for _ in range(m)]

    # 放置守卫
    for r, c in guards:
        grid[r][c] = 1
    # 放置墙
    for r, c in walls:
        grid[r][c] = 2

    # 四个方向的移动向量
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for r, c in guards:                     # 对每一个守卫
        for dr, dc in dirs:                 # 四个方向依次遍历
            nr, nc = r + dr, c + dc
            # 一直往前走，直到遇到墙或守卫或出界
            while 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 0:
                grid[nr][nc] = 3            # 标记为“受保护”
                nr += dr
                nc += dc

    # 统计未受保护的空格
    ans = 0
    for row in grid:
        for val in row:
            if val == 0:                     # 仍然是空格，说明没有被守卫看到
                ans += 1
    return ans
```

> **关键行解释**  
> - `grid = [[0] * n for _ in range(m)]`：创建一个 `m 行 n 列` 的二维列表，全部初始化为 `0`（空格）。  
> - `while 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 0:`：只要坐标合法且当前格子是空的，就可以继续向前；一旦碰到墙 (`2`) 或守卫 (`1`)，循环立即结束。  
> - `grid[nr][nc] = 3`：把这个格子标记为“被守卫看到”。  

#### 复杂度

- **时间复杂度**：`O(g * (m + n))`，其中 `g` 为守卫数量。  
  - 对每个守卫我们最多向四个方向各走 `max(m, n)` 步（最坏情况整行或整列都是空的），所以每个守卫的工作量是 `O(m + n)`。  
  - 对于初学者来说，可以把 `O(g * (m + n))` 想成“守卫数 × 网格的最长边”。在本题的约束下（`m·n ≤ 10⁵`），这仍然能跑完。

- **空间复杂度**：`O(m·n)`，需要一个和原网格同大小的二维数组来记录状态。  
  - 这相当于“把每个格子都装进一个小盒子里”，占用的内存正好和网格本身一样多。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每个守卫都要独立遍历它能看到的每一格**，当守卫很多、网格宽/高很大时会出现重复遍历（同一行/列的空格会被多次标记）。  
我们可以把视线的传播过程 **合并**，一次性完成整行或整列的标记，思路如下：

1. **准备工作**：同样创建 `grid`，把守卫记为 `1`、墙记为 `2`，其余保持 `0`。  
2. **行扫描**（左右两遍）  
   - **左→右**：遍历每一行的每个格子，维护一个布尔变量 `has_guard`。  
     - 当遇到守卫时，`has_guard = True`（后面的格子都可能被看到）。  
     - 当遇到墙时，`has_guard = False`（视线被阻断，后面的格子不再受左侧守卫影响）。  
     - 当 `has_guard` 为真且当前格子是空的 (`0`) 时，把它标记为受保护 (`3`)。  
   - **右→左**：同理，只是方向相反，处理右侧守卫的视线。  
3. **列扫描**（上下两遍）  
   - **上→下**：对每一列做类似的遍历，用 `has_guard` 记录“从上方看到的守卫”。  
   - **下→上**：相反方向。  
4. 最后遍历 `grid`，统计仍为 `0` 的格子数量——这些格子既不是守卫、也不是墙、也没有被任何方向的守卫看到。

> **核心概念——前缀扫描**  
> 把“从左往右是否已经遇到守卫且未被墙挡住”抽象成一个**状态**，随着遍历不断更新。这样每行只遍历一次（两遍），而不是对每个守卫都遍历一次。  

> **类比**：想象在一条直路上装了摄像头（守卫）和遮挡物（墙），摄像头拍摄的画面会一直往前延伸，直到被遮挡物阻断。我们只需要记录“当前这段路上是否有摄像头在拍摄”，不必每次都从摄像头重新走一遍。

#### 代码（Python）

```python
def countUnguarded(m: int, n: int, guards: list[list[int]], walls: list[list[int]]) -> int:
    # 0：空格，1：守卫，2：墙，3：受保护
    grid = [[0] * n for _ in range(m)]

    for r, c in guards:
        grid[r][c] = 1
    for r, c in walls:
        grid[r][c] = 2

    # ---------- 行方向扫描 ----------
    # 左 → 右
    for r in range(m):
        has_guard = False               # 本行左侧是否已经有守卫（且未被墙挡住）
        for c in range(n):
            if grid[r][c] == 1:         # 碰到守卫，后面的格子都可能被看到
                has_guard = True
            elif grid[r][c] == 2:       # 碰到墙，视线被阻断
                has_guard = False
            elif has_guard:             # 当前位置是空格且左侧有未被阻断的守卫
                grid[r][c] = 3

    # 右 → 左
    for r in range(m):
        has_guard = False
        for c in range(n - 1, -1, -1):
            if grid[r][c] == 1:
                has_guard = True
            elif grid[r][c] == 2:
                has_guard = False
            elif has_guard:
                grid[r][c] = 3

    # ---------- 列方向扫描 ----------
    # 上 → 下
    for c in range(n):
        has_guard = False
        for r in range(m):
            if grid[r][c] == 1:
                has_guard = True
            elif grid[r][c] == 2:
                has_guard = False
            elif has_guard:
                grid[r][c] = 3

    # 下 → 上
    for c in range(n):
        has_guard = False
        for r in range(m - 1, -1, -1):
            if grid[r][c] == 1:
                has_guard = True
            elif grid[r][c] == 2:
                has_guard = False
            elif has_guard:
                grid[r][c] = 3

    # 统计未受保护的空格
    ans = sum(1 for r in range(m) for c in range(n) if grid[r][c] == 0)
    return ans
```

> **关键行解释**  
> - `has_guard = False`：在每条新行（列）开始时，默认“左/上方没有守卫”。  
> - `if grid[r][c] == 1:`：遇到守卫，打开“灯”。  
> - `elif grid[r][c] == 2:`：遇到墙，关闭灯并且后面的格子不再受当前方向守卫影响。  
> - `elif has_guard:`：当前格子是空的且“灯是开的”，于是标记为 `3`（受保护）。  

#### 复杂度

- **时间复杂度**：`O(m·n)`  
  - 我们只对网格进行 **四次线性遍历**（左→右、右→左、上→下、下→上），每次都是 `m·n` 步。相比暴力解的 `O(g·(m+n))`，这里不再受守卫数量影响，始终线性随网格大小增长。  
  - 对于本题的限制 `m·n ≤ 10⁵`，这几乎是最快的。

- **空间复杂度**：`O(m·n)`  
  - 仍然需要一个同尺寸的二维数组来记录状态。  
  - 额外的变量只有几个布尔值 `has_guard`，可以视为 **O(1)** 额外空间。

---

## 心得

- **核心技巧**：**四向扫描 + 状态维护**（前缀/后缀扫描），把“每个守卫向四个方向延伸”的过程合并为对每行/列的两次线性遍历。  
- **适用的题型**  
  1. “矩阵中受光照/攻击影响的格子” 类似题目（例如 LeetCode 1461. Check If a String Contains All Binary Codes 里的滑动窗口思路）  
  2. “在二维网格中统计受阻挡的可达区域” 如 “Walls and Gates”  
  3. “行/列方向的最近特殊元素” 如 “Matrix Block Sum”  
- **一句话总结解题钥匙**：**把守卫的视线看成“打开的灯”，用一次遍历记录灯是否打开，就能一次性标记整行/整列的受保护格子**。

---

## 反思

- **第一反应**：直接把每个守卫的视线逐格展开，写成四个 `while` 循环——这就是暴力解。  
- **最容易踩的坑**  
  - **边界条件**：遍历时一定要检查 `0 ≤ nr < m`、`0 ≤ nc < n`，否则会数组越界。  
  - **墙和守卫的阻断顺序**：墙与守卫同样会阻止视线，不能只判断守卫。  
  - **重复标记**：在暴力解里，同一个格子可能被多个守卫多次标记，虽不影响正确性，但会浪费时间。  
- **下次遇到同类题**：第一步先思考**“是否可以把多次相似的遍历合并成一次线性扫描”**，尤其是涉及“方向传播”或“最近特殊元素”的问题时，尝试使用**前缀/后缀扫描**或**双指针**的思路。