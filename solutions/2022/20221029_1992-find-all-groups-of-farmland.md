# #1992. 找出所有农田组 / Find All Groups of Farmland

> 难度：中等 · 标签：Array、Depth-First Search、Breadth-First Search、Matrix · [LeetCode 链接](https://leetcode.com/problems/find-all-groups-of-farmland/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed m x n binary matrix land where a 0 represents a hectare of forested land and a 1 represents a hectare of farmland.
To keep the land organized, there are designated rectangular areas of hectares that consist entirely of farmland. These rectangular areas are called groups. No two groups are adjacent, meaning farmland in one group is not four-directionally adjacent to another farmland in a different group.
land can be represented by a coordinate system where the top left corner of land is (0, 0) and the bottom right corner of land is (m-1, n-1). Find the coordinates of the top left and bottom right corner of each group of farmland. A group of farmland with a top left corner at (r1, c1) and a bottom right corner at (r2, c2) is represented by the 4-length array [r1, c1, r2, c2].
Return a 2D array containing the 4-length arrays described above for each group of farmland in land. If there are no groups of farmland, return an empty array. You may return the answer in any order.

**Examples**

**Example 1:**

```
Input: land = [[1,0,0],[0,1,1],[0,1,1]]
Output: [[0,0,0,0],[1,1,2,2]]
Explanation:
The first group has a top left corner at land[0][0] and a bottom right corner at land[0][0].
The second group has a top left corner at land[1][1] and a bottom right corner at land[2][2].
```

**Example 2:**

```
Input: land = [[1,1],[1,1]]
Output: [[0,0,1,1]]
Explanation:
The first group has a top left corner at land[0][0] and a bottom right corner at land[1][1].
```

**Example 3:**

```
Input: land = [[0]]
Output: []
Explanation:
There are no groups of farmland.
```

**Constraints**

- m == land.length
- n == land[i].length
- 1 <= m, n <= 300
- land consists of only 0's and 1's.
- Groups of farmland are rectangular in shape.

---

## 题目（中文翻译）

**描述**  
给定一个下标从 0 开始的 `m x n` 二元矩阵 `land`，其中 `0` 表示一公顷的森林土地，`1` 表示一公顷的农田。  
为了使土地有序，所有完全由农田组成的矩形区域被划分为若干 **组**（group）。任意两个组之间不相邻，即一个组中的农田在四个方向上不与另一个组的农田相邻。  

`land` 可以用坐标系表示，左上角坐标为 `(0, 0)`，右下角坐标为 `(m‑1, n‑1)`。请找出每个农田组的左上角坐标和右下角坐标。一个左上角为 `(r1, c1)`、右下角为 `(r2, c2)` 的农田组用长度为 4 的数组 `[r1, c1, r2, c2]` 表示。  

返回一个二维数组，其中每个子数组就是上述的 4 元组，表示 `land` 中的所有农田组。如果不存在农田组，返回空数组。答案的顺序不限。

**示例 1**  
**输入**  
```
land = [[1,0,0],
        [0,1,1],
        [0,1,1]]
```  
**输出**  
```
[[0,0,0,0],[1,1,2,2]]
```  
**解释**  
- 第一个组的左上角在 `land[0][0]`，右下角也在 `land[0][0]`。  
- 第二个组的左上角在 `land[1][1]`，右下角在 `land[2][2]`。

**示例 2**  
**输入**  
```
land = [[1,1],
        [1,1]]
```  
**输出**  
```
[[0,0,1,1]]
```  
**解释**  
唯一的组左上角在 `land[0][0]`，右下角在 `land[1][1]`。

**示例 3**  
**输入**  
```
land = [[0]]
```  
**输出**  
```
[]
```  
**解释**  
不存在农田组。

**约束条件**  
- `m == land.length`  
- `n == land[i].length`  
- `1 <= m, n <= 300`  
- `land` 仅由 `0` 和 `1` 构成。  
- 农田组均为矩形形状。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每一块 “农田” 当成一块需要 **遍历** 的区域：

1. **遍历整个矩阵**，每遇到一个 `1`（表示农田），说明我们发现了一个新“组”。  
2. 对这个 `1` 进行 **深度优先搜索（DFS）** 或 **广度优先搜索（BFS）**，把与它四向相连的所有 `1` 都访问到。遍历的过程中记录下行号和列号的 **最小值**（左上角）和 **最大值**（右下角）。  
3. 把得到的 `[min_row, min_col, max_row, max_col]` 加入答案。  
4. 为了避免重复遍历，同一个组里的所有 `1` 在搜索结束后都 **改成 `0`**（相当于“标记已访问”），后面再扫描时就不会再次进入这个组。

> **类比**：把矩阵想象成一张城市地图，`1` 是住宅区，`0` 是空地。我们把每栋住宅区当成“建筑块”，用 DFS 像消防员一样从入口（第一个发现的 `1`）走遍整栋楼的每个房间，记下楼的左上和右下坐标，然后把这栋楼标记为已灭火（改成 `0`），继续在地图上寻找下一栋未灭火的建筑。

**为什么正确**  
- DFS 能把 **四方向相连** 的所有 `1` 都找出来，题目保证同一个组内部必然相连（因为它本身是矩形），所以遍历完一次 DFS 就恰好得到完整的一个组。  
- 记录的最小/最大行列号正好对应矩形的左上和右下角，因为矩形的四个角一定是该组中行号/列号的极值。

**复杂度分析（大白话）**  
- **时间**：我们最多遍历每个格子一次（如果是 `1`，会被 DFS 再遍历一次），所以时间是 `O(m·n)`，这里的 `m·n` 就是矩阵里格子的总数。想象成“每个格子只看一眼”。  
- **空间**：DFS 用递归栈（或显式队列）最多保存一条矩形对角线的长度，最坏情况是 `O(m·n)`（全部格子都是 `1`），但我们可以把矩阵原地改成 `0`，不需要额外的 `visited` 数组，所以额外空间可以算作 **常数级** `O(1)`（递归栈除外）。

#### 代码（Python）

```python
from typing import List

def findFarmland(land: List[List[int]]) -> List[List[int]]:
    if not land:
        return []
    m, n = len(land), len(land[0])
    ans = []

    # 四个方向的移动向量
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def dfs(r: int, c: int,
            bounds: List[int]) -> None:
        """
        递归遍历以 (r,c) 为起点的连通块。
        bounds = [min_r, min_c, max_r, max_c]，实时更新矩形边界。
        """
        # 标记已访问
        land[r][c] = 0

        # 更新边界
        bounds[0] = min(bounds[0], r)   # min 行
        bounds[1] = min(bounds[1], c)   # min 列
        bounds[2] = max(bounds[2], r)   # max 行
        bounds[3] = max(bounds[3], c)   # max 列

        # 向四个方向继续扩散
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and land[nr][nc] == 1:
                dfs(nr, nc, bounds)

    # 主循环：遍历每一个格子
    for i in range(m):
        for j in range(n):
            if land[i][j] == 1:               # 发现未访问的农田
                # 初始边界就是当前格子本身
                cur_bounds = [i, j, i, j]
                dfs(i, j, cur_bounds)         # 深度优先遍历整块
                ans.append(cur_bounds)        # 保存结果

    return ans
```

#### 复杂度

- **时间复杂度**：`O(m·n)` —— 每个格子最多访问两次（一次在主循环，一次在 DFS），相当于“每格子只看一次”。  
- **空间复杂度**：`O(1)`（不计递归栈）——我们直接把原矩阵改成 `0` 来标记访问，不需要额外的 `visited` 数组。递归栈最坏深度为 `m·n`，在 Python 中可以改写为显式栈来避免递归深度限制。

---

### 2. 最优解

#### 思路  

虽然上面的 DFS 已经是 `O(m·n)`，但我们可以 **省掉递归/队列的开销**，只用一次线性扫描就能得到答案。这利用了题目给出的关键限制：

- **每个组都是完整的矩形**，且 **不同组之间不相邻**（四方向上不会相连）。  
- 因此，**左上角** 必然是 **上边界和左边界都是 `0`（或矩阵边界）** 的那个 `1`。换句话说，若 `(r,c)` 为 `1`，而 `land[r-1][c]`（上方）和 `land[r][c-1]`（左方）都是 `0`（或越界），那么它一定是某个矩形的左上角。

基于此，我们可以：

1. **遍历矩阵**，遇到满足 “左上角” 条件的 `1` 时，开始 **向右** 找到该行连续的 `1` 的最右端 `c2`，再 **向下** 找到该列连续的 `1` 的最下端 `r2`。因为整个组是矩形，这两个极值就确定了右下角。  
2. 将矩形坐标 `[r, c, r2, c2]` 加入答案。  
3. 为了不在后面的遍历中再次处理这块已经记录的矩形，我们 **把它内部的所有 `1` 改成 `0`**（同样是标记已访问），这样后面的循环会直接跳过。

> **类比**：把矩阵想成一张仓库平面图，`1` 是货架。左上角的货架左边和上边都是空地（`0`），于是我们从这里“一眼望去”往右看到这排货架的尽头，再往下看到这一列货架的底部，矩形区域一目了然。

**为什么更好**  
- 只需要 **一次线性扫描**，没有递归或队列的额外开销。  
- 每块矩形只会被 **一次** “找出右下角”，随后全部置零，保证总体仍是 `O(m·n)`，但常数更小，运行更快。

#### 代码（Python）

```python
from typing import List

def findFarmland(land: List[List[int]]) -> List[List[int]]:
    if not land:
        return []
    m, n = len(land), len(land[0])
    ans = []

    for r in range(m):
        for c in range(n):
            # 只在真正的左上角开始处理
            if land[r][c] == 1:
                # 判断上方和左方是否都是 0（或越界），若不是则说明已经属于之前的矩形
                if (r > 0 and land[r-1][c] == 1) or (c > 0 and land[r][c-1] == 1):
                    continue

                # 向右找到最右端
                c2 = c
                while c2 + 1 < n and land[r][c2 + 1] == 1:
                    c2 += 1

                # 向下找到最下端
                r2 = r
                while r2 + 1 < m and land[r2 + 1][c] == 1:
                    r2 += 1

                # 把整个矩形清零，防止后续重复遍历
                for i in range(r, r2 + 1):
                    for j in range(c, c2 + 1):
                        land[i][j] = 0

                ans.append([r, c, r2, c2])

    return ans
```

#### 复杂度

- **时间复杂度**：`O(m·n)` —— 每个格子至多被检查两次（一次在主循环，一次在清零内部的双层循环），整体仍是线性。  
- **空间复杂度**：`O(1)` —— 只在原矩阵上就地修改，不需要额外的辅助结构。

> 与暴力 DFS 相比，**时间常数更小**（没有递归栈、队列的入栈/出栈操作），在实际运行时会更快；空间上也同样是原地修改。

---

## 心得

- **核心技巧**：利用**矩形的几何特性**（左上角唯一、右下角唯一）以及**相邻组不相连**的约束，直接定位每个组的边界。  
- **适用场景**：  
  1. “找所有不相交的矩形/正方形”类题目（如 LeetCode 1992 `Find All Groups of Farmland`）。  
  2. “在二值矩阵中找最大/最小矩形”或 “统计矩形数量” 的变体。  
  3. 需要 **一次扫描** 完成定位的场景（如扫描仪图像处理中的连通块标记）。  
- **一句话总结**：**左上角是唯一的入口，向右/向下伸手即可一次性捕获整个矩形**。

---

## 反思

- **第一反应**：看到“矩形且不相邻”，立刻想到 **DFS/BFS** 来遍历连通块。  
- **最容易踩的坑**：  
  - 忘记判断 **左上角** 的条件，导致同一个矩形被多次识别。  
  - 在清零阶段遗漏了某些格子，使得后面遍历时把同一块矩形当成新块。  
  - 边界处理不当（如 `r-1`、`c-1` 越界）会抛异常。  
- **下次遇到同类题**：第一步先**思考是否可以用几何特性直接定位**（如左上角、右下角），而不是直接套用通用的搜索算法。这样往往能得到更简洁、更高效的解法。