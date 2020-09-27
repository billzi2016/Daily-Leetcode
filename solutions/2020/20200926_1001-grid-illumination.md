# #1001. 网格照明 / Grid Illumination

> 难度：困难 · 标签：Array、Hash Table · [LeetCode 链接](https://leetcode.com/problems/grid-illumination/)

---

## 题目（英文原版）

**Description**

There is a 2D grid of size n x n where each cell of this grid has a lamp that is initially turned off.
You are given a 2D array of lamp positions lamps, where lamps[i] = [rowi, coli] indicates that the lamp at grid[rowi][coli] is turned on. Even if the same lamp is listed more than once, it is turned on.
When a lamp is turned on, it illuminates its cell and all other cells in the same row, column, or diagonal.
You are also given another 2D array queries, where queries[j] = [rowj, colj]. For the jth query, determine whether grid[rowj][colj] is illuminated or not. After answering the jth query, turn off the lamp at grid[rowj][colj] and its 8 adjacent lamps if they exist. A lamp is adjacent if its cell shares either a side or corner with grid[rowj][colj].
Return an array of integers ans, where ans[j] should be 1 if the cell in the jth query was illuminated, or 0 if the lamp was not.

**Examples**

**Example 1:**

```
Input: n = 5, lamps = [[0,0],[4,4]], queries = [[1,1],[1,0]]
Output: [1,0]
Explanation: We have the initial grid with all lamps turned off. In the above picture we see the grid after turning on the lamp at grid[0][0] then turning on the lamp at grid[4][4].
The 0th query asks if the lamp at grid[1][1] is illuminated or not (the blue square). It is illuminated, so set ans[0] = 1. Then, we turn off all lamps in the red square.

The 1st query asks if the lamp at grid[1][0] is illuminated or not (the blue square). It is not illuminated, so set ans[1] = 0. Then, we turn off all lamps in the red rectangle.
```

**Example 2:**

```
Input: n = 5, lamps = [[0,0],[4,4]], queries = [[1,1],[1,1]]
Output: [1,1]
```

**Example 3:**

```
Input: n = 5, lamps = [[0,0],[0,4]], queries = [[0,4],[0,1],[1,4]]
Output: [1,1,0]
```

**Constraints**

- 1 <= n <= 109
- 0 <= lamps.length <= 20000
- 0 <= queries.length <= 20000
- lamps[i].length == 2
- 0 <= rowi, coli < n
- queries[j].length == 2
- 0 <= rowj, colj < n

---

## 题目（中文翻译）

有一个大小为 `n x n` 的二维网格（2D grid），网格中的每个单元格（cell）初始时都有一盏灯（lamp）是关闭的。  
给定二维数组 `lamps`，其中 `lamps[i] = [rowi, coli]` 表示位于 `grid[rowi][coli]` 的灯被打开。即使同一盏灯在数组中出现多次，它也视为打开。  
当一盏灯被点亮时，它会照亮它所在的单元格以及同一行（row）、同一列（column）或同一对角线（diagonal）上的所有单元格。  

同时给定另一个二维数组 `queries`，其中 `queries[j] = [rowj, colj]`。对于第 `j` 次查询，需要判断 `grid[rowj][colj]` 是否被照亮。回答完第 `j` 次查询后，需要关闭位于 `grid[rowj][colj]` 的灯以及它的 8 个相邻灯（adjacent lamp），即那些与 `grid[rowj][colj]` 同侧或同角相接的单元格中的灯（如果存在）。  

返回一个整数数组 `ans`，其中 `ans[j]` 为 `1` 表示第 `j` 次查询的单元格被照亮，`0` 表示未被照亮。

**示例 1**  
**示例 2**  
**示例 3**  

**约束条件**

- `1 <= n <= 10^9`
- `0 <= lamps.length <= 20000`
- `0 <= queries.length <= 20000`
- `lamps[i].length == 2`
- `0 <= rowi, coli < n`
- `queries[j].length == 2`
- `0 <= rowj, colj < n`

---

### 示例

#### 示例 1
**输入**  
```text
n = 5, lamps = [[0,0],[4,4]], queries = [[1,1],[1,0]]
```
**输出**  
```text
[1,0]
```
**解释**  
我们从所有灯均关闭的初始网格开始。上图展示了先点亮 `grid[0][0]` 再点亮 `grid[4][4]` 后的网格状态。  
第 0 次查询询问 `grid[1][1]`（蓝色方块）是否被照亮。它被照亮，因此 `ans[0] = 1`。随后，我们关闭红色方块内的所有灯。  

第 1 次查询询问 `grid[1][0]`（蓝色方块）是否被照亮。它未被照亮，因此 `ans[1] = 0`。随后，我们关闭红色矩形内的所有灯。

#### 示例 2
**输入**  
```text
n = 5, lamps = [[0,0],[4,4]], queries = [[1,1],[1,1]]
```
**输出**  
```text
[1,1]
```

#### 示例 3
**输入**  
```text
n = 5, lamps = [[0,0],[0,4]], queries = [[0,4],[0,1],[1,4]]
```
**输出**  
```text
[1,1,0]
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有灯的照亮情况都写到一个二维数组里**，然后对每个查询直接检查该格子是否被点亮。  

实现步骤：

1. **建立一个 `grid`（二维列表）**，大小为 `n × n`，初始全为 `0`（表示未点亮）。  
2. **遍历 `lamps`**，把每盏灯所在的行、列、两条对角线的所有格子都标记为 `1`（点亮）。  
   - 行：`grid[r][*]`  
   - 列：`grid[*][c]`  
   - 主对角线（左上↘右下）：所有满足 `r - c` 相同的格子  
   - 副对角线（左下↗右上）：所有满足 `r + c` 相同的格子  
3. **对每个查询**  
   - 直接读取 `grid[row][col]`，如果是 `1` 就把答案记为 `1`，否则记为 `0`。  
   - 然后把查询格子以及它的 8 个相邻格子（如果在矩阵内部）对应的灯全部关闭。关闭的方式是把 `grid` 中相应位置重新设为 `0`，并且把它们对所在行、列、对角线的照亮状态全部撤销。  

> **生活化类比**：  
> - `grid` 就像一本大地图，每个格子是地图上的一个小格子，标记 `1` 表示这里有灯光，标记 `0` 表示黑暗。  
> - 把灯点亮就像在地图上画光线，光线会沿着横向、纵向以及两条斜线一直延伸。  

**为什么这种方法是对的？**  
因为我们把每盏灯的照亮范围全部显式记录在 `grid` 中，查询时直接看 `grid` 的值就能得到正确答案。关闭灯后，同样把对应的光线从 `grid` 中擦掉，后面的查询就会基于最新的状态。

#### 代码（Python）

```python
def gridIllumination_bruteforce(n, lamps, queries):
    # ---------- 1. 建立 n×n 的网格 ----------
    grid = [[0] * n for _ in range(n)]

    # ---------- 2. 把每盏灯的照亮范围写进 grid ----------
    for r, c in lamps:
        # 行
        for y in range(n):
            grid[r][y] = 1
        # 列
        for x in range(n):
            grid[x][c] = 1
        # 主对角线（r - c 固定）
        d = r - c
        for x in range(n):
            y = x - d
            if 0 <= y < n:
                grid[x][y] = 1
        # 副对角线（r + c 固定）
        s = r + c
        for x in range(n):
            y = s - x
            if 0 <= y < n:
                grid[x][y] = 1

    ans = []
    # ---------- 3. 逐个处理查询 ----------
    for r, c in queries:
        # 直接查看当前格子是否被点亮
        ans.append(1 if grid[r][c] == 1 else 0)

        # 关闭 (r,c) 及其 8 邻近格子的灯
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 1:
                    # 把这盏灯本身对应的光线全部擦掉
                    # 行
                    for y in range(n):
                        grid[nr][y] = 0
                    # 列
                    for x in range(n):
                        grid[x][nc] = 0
                    # 主对角线
                    d = nr - nc
                    for x in range(n):
                        y = x - d
                        if 0 <= y < n:
                            grid[x][y] = 0
                    # 副对角线
                    s = nr + nc
                    for x in range(n):
                        y = s - x
                        if 0 <= y < n:
                            grid[x][y] = 0
    return ans
```

> **关键行解释**  
> - `grid = [[0] * n for _ in range(n)]`：创建一个 `n×n` 的全 0 矩阵。  
> - `for y in range(n): grid[r][y] = 1`：把灯所在行的所有格子设为点亮。  
> - `for dr in (-1,0,1): …`：遍历查询格子及其八个相邻格子。  

#### 复杂度

- **时间复杂度**：`O(n³)`（超慢）  
  - 为每盏灯遍历整行、整列、两条对角线，最坏情况下每条遍历 `n` 次；灯的数量最多 `20000`，但 `n` 可达 `10⁹`，所以这种做法根本不可行。  
  - 用大白话说，想象一张 1 000 000 000 × 1 000 000 000 的表格，遍历每一行、每一列就已经需要 **上千亿** 次操作，远远超过电脑能接受的范围。

- **空间复杂度**：`O(n²)`  
  - 需要存储整个网格，若 `n=10⁹`，连内存都装不下。  

> 综上，这种“把全部灯光画在纸上再查表”的暴力思路只能用来说明问题，实际求解时必须做更好的优化。  

---

### 2. 最优解

#### 思路  

**从暴力解出发**，我们发现两大瓶颈：

1. **完整记录每个格子的点亮状态**（`grid`），空间和时间都太大。  
2. **每次关闭灯时，都要遍历整行、整列、整条对角线**，导致时间爆炸。

**关键观察**  

- 判断一个格子是否被点亮，只需要知道 **该格子所在的行、列、两条对角线是否还有至少一盏灯**。不必关心具体是哪盏灯在照亮。  
- 行、列、对角线的编号可以用整数表示：
  - 行：`row` 本身  
  - 列：`col` 本身  
  - 主对角线：`row - col`（所有在同一条左上→右下的格子都有相同的差）  
  - 副对角线：`row + col`（所有在同一条左下→右上的格子都有相同的和）  

于是我们可以 **用四个哈希表（字典）** 来维护每条“光线”上还剩多少盏灯：

| 哈希表 | 键（key） | 含义 |
|--------|-----------|------|
| `row_cnt`   | 行号 `r` | 这行还有多少盏灯是打开的 |
| `col_cnt`   | 列号 `c` | 这列还有多少盏灯是打开的 |
| `diag_cnt`  | `r - c`  | 主对角线上还有多少盏灯 |
| `anti_cnt`  | `r + c`  | 副对角线上还有多少盏灯 |

**实现细节**

1. **初始化**  
   - 把每盏灯的坐标放进一个 `set`（或 `dict`）`lamp_set`，用 `(r, c)` 这对整数唯一标识。  
   - 同时把四个计数字典的对应键值加 1。  
   - 如果同一盏灯在输入里出现多次，只算一次（`set` 自动去重），这样计数也不会多加。

2. **查询**  
   - 对于 `(r, c)`，只要 `row_cnt[r] > 0 or col_cnt[c] > 0 or diag_cnt[r-c] > 0 or anti_cnt[r+c] > 0`，说明它被至少一盏灯照亮，答案记 `1`，否则记 `0`。  
   - 这一步是 **O(1)**，因为只看四个字典的值。

3. **关闭灯**  
   - 需要关闭 **查询格子自身以及 8 个相邻格子**（共 9 格）。遍历这 9 个坐标 `(nr, nc)`：  
     - 如果 `(nr, nc)` 在 `lamp_set` 中（说明这格子上还有灯），就把它从集合里删掉。  
     - 同时把对应的四个计数器减 1（如果计数减到 0，就可以把键删掉，省空间）。  
   - 这一步同样是 **O(1)**（最多遍历 9 次，每次 O(1) 操作）。

**为什么能跑得快？**  
- 我们不再维护每个格子的状态，只记录**光线的“活灯数量”**。  
- 每次查询和每次关闭最多只涉及常数次哈希表的查找/更新，时间是 **线性** 与灯的数量和查询数量成正比：`O(L + Q)`，其中 `L = len(lamps)`，`Q = len(queries)`。  
- 空间只用到四个哈希表和灯的集合，最坏情况是每盏灯各自位于不同行、不同列、不同对角线，空间是 `O(L)`，远远小于 `O(n²)`。

> **类比**：  
> 把每条光线想成一本字典（哈希表），键是行号/列号/对角线标识，值是这本字典里还有多少本书（灯）。查询时只要看这四本字典里有没有书就行，根本不必把每页纸都写出来。

#### 代码（Python）

```python
from collections import defaultdict

def gridIllumination(n, lamps, queries):
    """
    最优解：使用四个哈希表 + 一个集合记录灯的位置
    时间复杂度 O(L + Q)，空间复杂度 O(L)
    """
    # ---------- 1. 记录灯的位置（去重） ----------
    lamp_set = set()                # {(r, c), ...}
    row_cnt   = defaultdict(int)   # 行 -> 灯的数量
    col_cnt   = defaultdict(int)   # 列 -> 灯的数量
    diag_cnt  = defaultdict(int)   # 主对角线 (r - c) -> 灯的数量
    anti_cnt  = defaultdict(int)   # 副对角线 (r + c) -> 灯的数量

    for r, c in lamps:
        if (r, c) in lamp_set:     # 已经计数过的灯直接跳过
            continue
        lamp_set.add((r, c))
        row_cnt[r]   += 1
        col_cnt[c]   += 1
        diag_cnt[r - c] += 1
        anti_cnt[r + c] += 1

    # ---------- 2. 处理每个查询 ----------
    ans = []
    # 8 个方向（包括自身）用于关闭灯
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),  (0, 0),  (0, 1),
                  (1, -1),  (1, 0),  (1, 1)]

    for r, c in queries:
        # ----- 判断是否被照亮 -----
        if (row_cnt.get(r, 0) > 0 or
            col_cnt.get(c, 0) > 0 or
            diag_cnt.get(r - c, 0) > 0 or
            anti_cnt.get(r + c, 0) > 0):
            ans.append(1)
        else:
            ans.append(0)

        # ----- 关闭 (r,c) 以及相邻的灯 -----
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and (nr, nc) in lamp_set:
                # 从集合中移除
                lamp_set.remove((nr, nc))

                # 四个计数器各减一，若减到 0 则删掉键（可选，帮助节省空间）
                row_cnt[nr]   -= 1
                if row_cnt[nr] == 0:
                    del row_cnt[nr]

                col_cnt[nc]   -= 1
                if col_cnt[nc] == 0:
                    del col_cnt[nc]

                diag_cnt[nr - nc] -= 1
                if diag_cnt[nr - nc] == 0:
                    del diag_cnt[nr - nc]

                anti_cnt[nr + nc] -= 1
                if anti_cnt[nr + nc] == 0:
                    del anti_cnt[nr + nc]

    return ans
```

> **代码要点注释**  
> - `defaultdict(int)`：创建一个默认值为 `0` 的字典，省去每次查询是否存在的判断。  
> - `lamp_set`：集合的查找/删除都是 **O(1)**，用来判断某个格子上是否真的有灯。  
> - `directions`：列举了 9 个相对坐标，遍历一次即可完成“关闭自身及相邻灯”。  
> - `if 0 <= nr < n and 0 <= nc < n`：确保不越界（因为 `n` 可能非常大）。  

#### 复杂度

- **时间复杂度**：`O(L + Q)`  
  - 初始化遍历灯列表一次 `O(L)`。  
  - 每个查询做常数次哈希表查找 (`O(1)`) 并遍历至多 9 个相邻格子，合计 `O(Q)`。  
  - 与网格大小 `n` 完全无关，适用于 `n` 高达 `10⁹` 的情况。  
  - 用大白话说：如果有 2 万盏灯和 2 万次查询，最多执行约 **4 万次**的简单操作，几乎在一瞬间就能算完。

- **空间复杂度**：`O(L)`  
  - 需要存放灯的位置集合以及四个计数字典，最坏情况下每盏灯都占一个键值对。  
  - 与网格面积 `n²` 无关，极大节省内存。  

---

## 心得

- **核心技巧**：**用哈希表统计行、列、对角线的灯数量**，而不是显式维护每个格子的点亮状态。  
- **适用的题型**  
  1. “**棋盘上有棋子，查询是否在同一行/列/对角线**” 类似题目，如 LeetCode 199（Number of Islands）中的邻接检查。  
  2. “**二维平面上点的覆盖/冲突**”，比如 1461（Check If a String Contains All Binary Codes）中的滑动窗口计数思路。  
  3. “**动态添加/删除元素后快速判断属性**”，如 1723（Longest Substring of One Repeating Character）中的字符计数。  

- **一句话总结解题钥匙**：**把“是否被照亮”转化为“所在的四条线中是否还有活灯”，用哈希表把四条线的活灯数量实时维护**。

---

## 反思

- **第一反应**：直接把灯光画在大矩阵里，想把每个格子都标记出来。  
- **最容易踩的坑**  
  1. **空间爆炸**：`n` 可以高达 `10⁹`，根本不能开 `n×n` 的数组。  
  2. **重复灯的处理**：同一盏灯可能在输入中出现多次，需要去重，否则计数会多算。  
  3. **对角线编号**：主对角线用 `r - c`，副对角线用 `r + c`，容易写错或忘记负数的情况。  
  4. **关闭灯时的边界检查**：相邻格子可能超出矩阵，需要先判断 `0 ≤ nr < n`、`0 ≤ nc < n`。  

- **下次遇到同类题**，第一步应该先**思考能否用少量统计信息代替完整网格**（行/列/对角线计数、前缀和、滑动窗口等），再决定使用哈希表、数组或其他数据结构来维护这些统计信息。这样既能保证时间，又能控制空间。