# #2088. 统计肥沃金字塔的数量 / Count Fertile Pyramids in a Land

> 难度：困难 · 标签：Array、Dynamic Programming、Matrix · [LeetCode 链接](https://leetcode.com/problems/count-fertile-pyramids-in-a-land/)

---

## 题目（英文原版）

**Description**

A farmer has a rectangular grid of land with m rows and n columns that can be divided into unit cells. Each cell is either fertile (represented by a 1) or barren (represented by a 0). All cells outside the grid are considered barren.
A pyramidal plot of land can be defined as a set of cells with the following criteria:
An inverse pyramidal plot of land can be defined as a set of cells with similar criteria:
Some examples of valid and invalid pyramidal (and inverse pyramidal) plots are shown below. Black cells indicate fertile cells.
Given a 0-indexed m x n binary matrix grid representing the farmland, return the total number of pyramidal and inverse pyramidal plots that can be found in grid.

**Examples**

**Example 1:**

```
Input: grid = [[0,1,1,0],[1,1,1,1]]
Output: 2
Explanation: The 2 possible pyramidal plots are shown in blue and red respectively.
There are no inverse pyramidal plots in this grid. 
Hence total number of pyramidal and inverse pyramidal plots is 2 + 0 = 2.
```

**Example 2:**

```
Input: grid = [[1,1,1],[1,1,1]]
Output: 2
Explanation: The pyramidal plot is shown in blue, and the inverse pyramidal plot is shown in red. 
Hence the total number of plots is 1 + 1 = 2.
```

**Example 3:**

```
Input: grid = [[1,1,1,1,0],[1,1,1,1,1],[1,1,1,1,1],[0,1,0,0,1]]
Output: 13
Explanation: There are 7 pyramidal plots, 3 of which are shown in the 2nd and 3rd figures.
There are 6 inverse pyramidal plots, 2 of which are shown in the last figure.
The total number of plots is 7 + 6 = 13.
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 1000
- 1 <= m * n <= 105
- grid[i][j] is either 0 or 1.

---

## 题目（中文翻译）

一个农夫拥有一块 **m 行 n 列** 的矩形网格土地，每个单元格（unit cell）可以划分为 1×1 的格子。每个格子要么肥沃（用 `1` 表示），要么贫瘠（用 `0` 表示）。网格之外的所有格子均视为贫瘠。

**金字塔形地块**（pyramidal plot）可以定义为满足如下条件的一组格子：

**倒置金字塔形地块**（inverse pyramidal plot）可以定义为满足类似条件的一组格子：

下面展示了一些有效和无效的金字塔（以及倒置金字塔）示例，黑色格子表示肥沃格子。

给定一个 **0 索引** 的 `m × n` 二进制矩阵 `grid` 表示这块农田，返回在 `grid` 中能够找到的 **金字塔形地块** 与 **倒置金字塔形地块** 的总数量。

---

### 示例

**示例 1**  
```text
Input: grid = [[0,1,1,0],[1,1,1,1]]
Output: 2
Explanation: 两个可能的金字塔形地块如图所示，分别用蓝色和红色标出。
该网格中不存在倒置金字塔形地块。
因此金字塔形地块与倒置金字塔形地块的总数为 2 + 0 = 2。
```

**示例 2**  
```text
Input: grid = [[1,1,1],[1,1,1]]
Output: 2
Explanation: 金字塔形地块如蓝色所示，倒置金字塔形地块如红色所示。
因此总地块数为 1 + 1 = 2。
```

**示例 3**  
```text
Input: grid = [[1,1,1,1,0],
               [1,1,1,1,1],
               [1,1,1,1,1],
               [0,1,0,0,1]]
Output: 13
Explanation: 共有 7 个金字塔形地块，其中 3 个在第 2、3 幅图中展示。
共有 6 个倒置金字塔形地块，其中 2 个在最后一幅图中展示。
总数为 7 + 6 = 13。
```

---

### 约束条件

- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 1000`
- `1 <= m * n <= 10^5`
- `grid[i][j]` 仅为 `0` 或 `1`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

把“金字塔”想象成 **一座倒置的三角形**，顶点在某个格子 `(r, c)`，往下每层宽度都比上一层多 2（左边、右边各扩展 1 格）。  

> **类比**：  
> - **哈希表** 就像字典，`key` 是单词，`value` 是页码。这里我们不需要哈希表，只需要遍历所有格子。  
> - **金字塔** 就像在地上画的等边三角形，只要每个格子都是 `1`（肥沃），就算合法。  

最直接的办法是 **枚举每一个可能的顶点**，然后**逐层向下检查**，看能否一直扩展成更高的金字塔。  
- 先把顶点 `(r, c)` 记为第 1 层（高度 = 1）。  
- 第 2 层要求 `(r+1, c-1) , (r+1, c) , (r+1, c+1)` 都是 `1`。  
- 第 3 层要求 `(r+2, c-2)…(r+2, c+2)` 全部是 `1`，依此类推。  
- 只要有一次检查不通过，就停止向下扩展。  

对 **倒金字塔**（顶点在底部）同理，只是方向相反：从底部往上检查。

> **为什么正确？**  
> 因为金字塔的定义本身就是“每层必须完整且全为 1”。我们逐层检查恰好对应了定义的每一条约束，所以只要检查通过，就一定是一座合法金字塔；检查不通过则说明这座金字塔不存在。

> **复杂度大概是怎样的？**  
> - 外层遍历所有格子：`m × n` 次。  
> - 对每个格子，最坏情况下需要检查 `min(m, n)` 层（因为金字塔的高度受行列数限制）。  
> - 每层检查的格子数随高度线性增长，总检查量是 `1 + 3 + 5 + … + (2·h-1) = h²`。  
> - 因此整体时间复杂度约为 **O(m·n·min(m,n)²)**，在最坏情况下相当于 **O(10⁸)**（因为 `m·n ≤ 10⁵`），会超时。  
> - 空间上只用了原始矩阵和几个临时变量，**O(1)**。

#### 代码（Python）

```python
def count_pyramids_bruteforce(grid):
    m, n = len(grid), len(grid[0])
    ans = 0

    # --------- 正金字塔（顶点在上） ----------
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 0:          # 顶点不是肥沃的，直接跳过
                continue
            height = 1                    # 当前已确认的高度（至少 1）
            while True:
                nr = r + height           # 下一层的行号
                if nr >= m:               # 超出矩阵下边界
                    break
                # 本层左、右边界列号
                left  = c - height
                right = c + height
                if left < 0 or right >= n:    # 超出左右边界
                    break
                # 检查本层所有格子是否都是 1
                ok = True
                for cc in range(left, right + 1):
                    if grid[nr][cc] == 0:
                        ok = False
                        break
                if not ok:
                    break
                height += 1                # 本层合法，尝试再高一层

            # 高度 >= 2 的金字塔才算有效，一座顶点可以构成 (height-1) 座金字塔
            ans += max(0, height - 1)

    # --------- 逆金字塔（顶点在下） ----------
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 0:
                continue
            height = 1
            while True:
                nr = r - height           # 往上找上一层
                if nr < 0:
                    break
                left  = c - height
                right = c + height
                if left < 0 or right >= n:
                    break
                ok = True
                for cc in range(left, right + 1):
                    if grid[nr][cc] == 0:
                        ok = False
                        break
                if not ok:
                    break
                height += 1
            ans += max(0, height - 1)

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(m·n·min(m,n)²)`  
  - “O” 代表算法的增长速度。这里的 `m·n` 是格子总数，`min(m,n)²` 是每个格子最坏情况下要检查的格子数的平方。换句话说，若矩阵是 1000×100，最坏需要检查约 `1000·100·100² = 10⁹` 次，远远超出可接受范围。  
- **空间复杂度**：`O(1)`  
  - 只用了常数级的额外变量（计数器、循环索引），不随输入规模增大而增长。

---

### 2. 最优解  

#### 思路  

暴力解的 **瓶颈** 在于“每个格子都要重新从头检查所有层”。  
如果我们已经知道 **下方（或上方）相邻格子的最大金字塔高度**，是否可以直接推导出当前格子的高度？答案是肯定的，这正是 **动态规划（DP）** 的核心思想——把大问题拆成子问题，子问题的答案已经算好，只需要 **一次查询**。

**关键观察**  

- 对于 **正金字塔**（顶点在上），设 `dp_up[r][c]` 为 **以 `(r,c)` 为顶点的最大金字塔高度**（高度至少为 1，只要该格子本身是 1）。  
- 要让高度大于 1，必须满足 **左下** 与 **右下** 两个格子各自能形成 **高度至少为 `h-1` 的金字塔**，因为第 `h` 层的最左、最右两个格子恰好是这两个位置。  
- 因此：

```
if grid[r][c] == 1:
    dp_up[r][c] = 1 + min(dp_up[r+1][c-1], dp_up[r+1][c+1])
else:
    dp_up[r][c] = 0
```

- 边界格子（超出矩阵）视为高度 0（相当于“外部都是荒地”），这样 `min` 操作自然会把它们排除。  

**逆金字塔** 同理，只是方向相反：

```
if grid[r][c] == 1:
    dp_down[r][c] = 1 + min(dp_down[r-1][c-1], dp_down[r-1][c+1])
else:
    dp_down[r][c] = 0
```

**如何把 DP 结果转成答案？**  

- 对于某个顶点，若 `dp = 4`，说明它可以是高度为 2、3、4 的金字塔的顶点，一共 **`dp-1`** 座金字塔（因为高度为 1 的“金字塔”不计数）。  
- 所以答案就是所有格子 `dp_up-1`（正金字塔）与 `dp_down-1`（逆金字塔）的正数之和。

**实现细节**  

1. **遍历顺序**：  
   - 计算 `dp_up` 时，需要先知道 **下一行** 的值，所以从 **底行向上** 逐行遍历。  
   - 计算 `dp_down` 时，需要先知道 **上一行** 的值，所以从 **顶行向下** 逐行遍历。  

2. **空间优化**：  
   - 只和上一行（或下一行）有关，完全可以只保留 **两行** 的 DP 数组，甚至用 **一维数组** 滚动更新，空间降到 `O(n)`。这里为了代码可读性保留完整的二维 DP，仍然是 `O(m·n)`，满足题目限制（`m·n ≤ 10⁵`）。

3. **边界处理**：  
   - 当访问 `c-1` 或 `c+1` 越界时，直接把对应的 DP 值当作 0（荒地），可以在代码里写 `if 0 <= nc < n else 0`。

> **为什么这一次是 O(m·n)？**  
> 每个格子只做 **一次** 常数时间的计算（取左右两个子问题的最小值），不再重复检查整层格子。因此总操作次数正好等于格子数 `m·n`，即线性时间。

#### 代码（Python）

```python
def countPyramids(grid):
    """
    返回矩阵中所有正金字塔和逆金字塔的数量（高度 >= 2）。
    """
    m, n = len(grid), len(grid[0])
    ans = 0

    # ---------- 正金字塔（顶点在上） ----------
    # dp_up[r][c] 表示以 (r,c) 为顶点的最大高度
    dp_up = [[0] * n for _ in range(m)]

    # 从底部往上遍历
    for r in range(m - 1, -1, -1):
        for c in range(n):
            if grid[r][c] == 0:          # 不是肥沃格子，无法构成金字塔
                dp_up[r][c] = 0
                continue

            # 底层默认高度 1（只要自己是 1）
            if r == m - 1:                # 已经是最底行，不能再往下扩展
                dp_up[r][c] = 1
            else:
                # 左下、右下的高度（越界视为 0）
                left  = dp_up[r + 1][c - 1] if c - 1 >= 0 else 0
                right = dp_up[r + 1][c + 1] if c + 1 < n else 0
                dp_up[r][c] = 1 + min(left, right)

            # 只要高度 >= 2，就能形成 (height-1) 座金字塔
            if dp_up[r][c] > 1:
                ans += dp_up[r][c] - 1

    # ---------- 逆金字塔（顶点在下） ----------
    # dp_down[r][c] 表示以 (r,c) 为底部（即逆金字塔的顶点）的最大高度
    dp_down = [[0] * n for _ in range(m)]

    # 从顶部往下遍历
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 0:
                dp_down[r][c] = 0
                continue

            if r == 0:                     # 已经是最顶行，无法再往上扩展
                dp_down[r][c] = 1
            else:
                left  = dp_down[r - 1][c - 1] if c - 1 >= 0 else 0
                right = dp_down[r - 1][c + 1] if c + 1 < n else 0
                dp_down[r][c] = 1 + min(left, right)

            if dp_down[r][c] > 1:
                ans += dp_down[r][c] - 1

    return ans
```

> **代码要点解释**（每行注释已在代码中给出）  
> - `dp_up[r][c] = 1 + min(left, right)`：  
>   - `1` 代表自己这层一定成立（因为 `grid[r][c] == 1`）。  
>   - `min(left, right)` 取左右下方能够继续向下扩展的最小高度，保证整层都为 `1`。  
> - `if dp_up[r][c] > 1: ans += dp_up[r][c] - 1`：  
>   - 高度为 1 的“金字塔”不计数，只有高度 ≥ 2 才算。  
>   - 例如 `dp = 4`，说明可以形成高度 2、3、4 的三座金字塔，`4-1 = 3` 正好是数量。  

#### 复杂度  

- **时间复杂度**：`O(m·n)`  
  - “O(m·n)” 表示算法的运行时间与矩阵中格子的数量成正比。只遍历了一遍矩阵（两次分别求正、逆金字塔），每个格子只做了常数次的加、减、取最小等操作。相比暴力的 `O(m·n·min(m,n)²)`，快了几个数量级。  
- **空间复杂度**：`O(m·n)`（如果使用滚动数组可降至 `O(n)`）  
  - 需要额外存两个 DP 表格，每个表格大小和原矩阵相同。因为 `m·n ≤ 10⁵`，最多只占几百 KB，完全在限制范围内。

---

## 心得  

- **核心技巧**：**利用相邻两格的 DP 值递推出当前格子的最大金字塔高度**（“左右下/上最小值 + 1”）。  
- **适用的题型**：  
  1. “最大正方形/矩形面积” 类的 DP（如 LeetCode 221、2212）。  
  2. “三角形/金字塔形状的计数” 类（如 “Count Submatrices With All Ones”）。  
- **一句话总结**：**把金字塔的“每层依赖左右相邻层”转化为 DP 递推，一遍遍历即可完成计数**。

---

## 反思  

- **第一反应**：看到“金字塔”就想到逐层检查，直接写暴力循环。  
- **最容易踩的坑**：  
  - 忘记 **高度必须 ≥ 2**，导致把单个格子也算进去了。  
  - 边界格子访问越界（`c-1`、`c+1`），需要额外判断或把越界视为 0。  
  - 逆金字塔的方向容易写反，记得把 DP 的遍历顺序调换（从上往下）。  
- **下次遇到类似题目**：**先问自己“当前格子能否由上下（左右）相邻格子的状态直接推出？”**，若答案是“能”，就立刻考虑 DP；若“不”，再考虑暴力或其他技巧。