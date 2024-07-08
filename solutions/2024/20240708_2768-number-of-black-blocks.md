# #2768. 黑块数量 / Number of Black Blocks

> 难度：中等 · 标签：Array、Hash Table、Enumeration · [LeetCode 链接](https://leetcode.com/problems/number-of-black-blocks/)

---

## 题目（英文原版）

**Description**

You are given two integers m and n representing the dimensions of a 0-indexed m x n grid.
You are also given a 0-indexed 2D integer matrix coordinates, where coordinates[i] = [x, y] indicates that the cell with coordinates [x, y] is colored black. All cells in the grid that do not appear in coordinates are white.
A block is defined as a 2 x 2 submatrix of the grid. More formally, a block with cell [x, y] as its top-left corner where 0 <= x < m - 1 and 0 <= y < n - 1 contains the coordinates [x, y], [x + 1, y], [x, y + 1], and [x + 1, y + 1].
Return a 0-indexed integer array arr of size 5 such that arr[i] is the number of blocks that contains exactly i black cells.

**Examples**

**Example 1:**

```
Input: m = 3, n = 3, coordinates = [[0,0]]
Output: [3,1,0,0,0]
Explanation: The grid looks like this:

There is only 1 block with one black cell, and it is the block starting with cell [0,0].
The other 3 blocks start with cells [0,1], [1,0] and [1,1]. They all have zero black cells. 
Thus, we return [3,1,0,0,0].
```

**Example 2:**

```
Input: m = 3, n = 3, coordinates = [[0,0],[1,1],[0,2]]
Output: [0,2,2,0,0]
Explanation: The grid looks like this:

There are 2 blocks with two black cells (the ones starting with cell coordinates [0,0] and [0,1]).
The other 2 blocks have starting cell coordinates of [1,0] and [1,1]. They both have 1 black cell.
Therefore, we return [0,2,2,0,0].
```

**Constraints**

- 2 <= m <= 105
- 2 <= n <= 105
- 0 <= coordinates.length <= 104
- coordinates[i].length == 2
- 0 <= coordinates[i][0] < m
- 0 <= coordinates[i][1] < n
- It is guaranteed that coordinates contains pairwise distinct coordinates.

---

## 题目（中文翻译）

**题目描述**

给定两个整数 `m` 和 `n`，表示一个 **0 索引** 的 `m x n` 网格的尺寸。  
同时给定一个 **0 索引** 的二维整数矩阵 `coordinates`，其中 `coordinates[i] = [x, y]` 表示坐标为 `[x, y]` 的单元格被涂成黑色。网格中未出现在 `coordinates` 的单元格均为白色。

一个 **块（block）** 被定义为网格中的 `2 x 2` 子矩阵。更正式地说，左上角为单元格 `[x, y]`（满足 `0 <= x < m - 1` 且 `0 <= y < n - 1`）的块包含坐标 `[x, y]`、`[x + 1, y]`、`[x, y + 1]` 和 `[x + 1, y + 1]`。

返回一个 **0 索引** 的整数数组 `arr`（长度为 5），其中 `arr[i]` 表示恰好包含 `i` 个黑色单元格的块的数量。

---

**示例**

*示例 1*

```
Input: m = 3, n = 3, coordinates = [[0,0]]
Output: [3,1,0,0,0]
Explanation: 网格如下：

```
（此处省略网格图示）

只有 1 个块含有 1 个黑色单元格，它的左上角是单元格 `[0,0]`。  
其余 3 个块的左上角分别是 `[0,1]`、`[1,0]` 和 `[1,1]`，它们都不含黑色单元格。  
因此返回 `[3,1,0,0,0]`。

*示例 2*

```
Input: m = 3, n = 3, coordinates = [[0,0],[1,1],[0,2]]
Output: [0,2,2,0,0]
Explanation: 网格如下：

```
（此处省略网格图示）

有 2 个块包含 2 个黑色单元格（左上角分别为 `[0,0]` 和 `[0,1]`）。  
另外 2 个块的左上角为 `[1,0]` 和 `[1,1]`，它们各含 1 个黑色单元格。  
因此返回 `[0,2,2,0,0]`。

---

**约束条件**

- `2 <= m <= 10^5`
- `2 <= n <= 10^5`
- `0 <= coordinates.length <= 10^4`
- `coordinates[i].length == 2`
- `0 <= coordinates[i][0] < m`
- `0 <= coordinates[i][1] < n`
- 保证 `coordinates` 中的坐标两两不同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把整个 **m × n** 的网格全部画出来，遍历每一个可能的 2×2 小块（左上角坐标 `[x, y]` 满足 `0 ≤ x < m-1`、`0 ≤ y < n-1`），统计这个小块里有多少个黑格子，然后把结果累加到 `arr[0]~arr[4]` 中。

- **数据结构**：  
  - 网格本身可以用二维列表 `grid[m][n]` 表示，`grid[i][j] = 1` 表示黑格子，`0` 表示白格子。  
  - `arr` 是长度为 5 的列表，用来记录恰好出现 `0、1、2、3、4` 个黑格子的 2×2 小块数量。  

> **类比**：把网格想象成一张棋盘，`grid[i][j]` 就像棋盘上的格子里是否放了棋子（黑格子），我们要检查每个 2×2 的“小宫格”里放了几颗棋子。

- **正确性**：  
  对每一个合法的左上角 `[x, y]`，我们都完整检查了它对应的四个格子，统计到的黑格子数必然是该块的真实黑格子数。把它计入对应的 `arr`，所有块都遍历完后，`arr` 的统计自然就是题目要求的答案。

- **时间/空间复杂度**：  
  - **时间**：我们需要遍历所有可能的 2×2 小块，数量是 `(m-1)*(n-1)`，每块检查 4 格子 → 大约 `4·(m-1)*(n-1)` 次操作，记作 **O(m·n)**。  
    对于 `m,n` 可达 `10⁵` 的情况，这个数量会达到 `10¹⁰` 级别，根本跑不完。  
  - **空间**：存整个网格需要 `m·n` 的空间，即 **O(m·n)**，同样在极限数据下会爆内存。

> **大白话**：  
> - `O(m·n)` 就是说，随着网格行数和列数的乘积增长，程序的运行时间会线性增长。想象你要把一整块地铺满砖，每块砖都要检查一次，地越大，时间就越久。  
> - `O(1)` 表示不随输入大小变化的常数空间，而 `O(m·n)` 表示需要跟网格大小等比例的内存。

#### 代码（Python）

```python
def countBlackBlocks_bruteforce(m: int, n: int, coordinates):
    # 1. 把所有黑格子标记在二维数组里
    grid = [[0] * n for _ in range(m)]          # 0 表示白格子
    for x, y in coordinates:
        grid[x][y] = 1                          # 1 表示黑格子

    # 2. 统计每个 2×2 小块里黑格子的数量
    ans = [0] * 5                               # ans[i] = 有 i 个黑格子的块数
    for x in range(m - 1):
        for y in range(n - 1):
            # 四个格子分别是 (x,y) (x+1,y) (x,y+1) (x+1,y+1)
            black_cnt = (grid[x][y] + grid[x + 1][y] +
                         grid[x][y + 1] + grid[x + 1][y + 1])
            ans[black_cnt] += 1                 # 把计数加到对应的桶里

    return ans
```

#### 复杂度

- **时间复杂度**：`O(m·n)`  
  意味着需要检查网格中每一个可能的 2×2 小块，随着网格面积增大，耗时线性增长。  
- **空间复杂度**：`O(m·n)`  
  需要存储整张网格，对大尺寸的输入会导致内存不足。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **遍历所有块**，而实际上 **黑格子本身的数量**（记作 `k = len(coordinates)`) 远远小于块的总数。  
我们只需要关注**被黑格子影响到的块**，其数量最多是 `4·k`（每个黑格子最多属于左上、左下、右上、右下四个块），这在最坏情况下仍然是 `O(k)`，而 `k ≤ 10⁴`，完全可接受。

**关键观察**：

1. 给定一个黑格子 `[x, y]`，它会出现在哪些 2×2 块里？  
   - 只要该块的左上角在 `[x-1, y-1]、[x-1, y]、[x, y-1]、[x, y]` 中（前提是左上角合法，即 `0 ≤ x' < m-1` 且 `0 ≤ y' < n-1`），该块就会包含这个黑格子。  
2. 因此，我们可以遍历每个黑格子，枚举它所在的最多 4 个块的左上角坐标，然后在一个哈希表（Python 的 `dict`）里记录该块已经出现了多少个黑格子。  
   - 哈希表的键是块的左上角坐标 `(x', y')`，值是当前块中黑格子的计数（1~4）。  
3. 最后遍历哈希表，把每个块的计数累加到 `ans[cnt]` 中。  
   - 还需要把 **没有任何黑格子的块** 计入 `ans[0]`。这类块的数量等于 **所有块的总数** 减去 **哈希表中出现的块数**。  
   - 所有块的总数是 `(m-1)*(n-1)`。

**为什么哈希表可以胜任？**  
- 哈希表像一本“字典”，可以用“左上角坐标”快速查找对应块的黑格子计数，时间是 **O(1)**（均摊），不需要遍历整个网格。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def countBlackBlocks(m: int, n: int, coordinates: List[List[int]]) -> List[int]:
    """
    最优解：只统计受到黑格子影响的块
    """
    # cnt_blocks[(x, y)] = 该块中黑格子的数量（1~4）
    cnt_blocks = defaultdict(int)

    for x, y in coordinates:
        # 枚举四个可能的左上角坐标
        for dx in (-1, 0):
            for dy in (-1, 0):
                nx, ny = x + dx, y + dy          # 可能的左上角
                # 必须保证左上角在合法范围内
                if 0 <= nx < m - 1 and 0 <= ny < n - 1:
                    cnt_blocks[(nx, ny)] += 1   # 该块黑格子数加一

    # ans[i] = 恰好有 i 个黑格子的块数，i 范围 0~4
    ans = [0] * 5

    # 先把出现过的块计入 ans
    for black_cnt in cnt_blocks.values():
        ans[black_cnt] += 1          # black_cnt 必然在 1~4 之间

    # 再算没有任何黑格子的块数量
    total_blocks = (m - 1) * (n - 1)          # 所有可能的 2×2 块总数
    blocks_with_black = len(cnt_blocks)      # 哈希表里记录的块数
    ans[0] = total_blocks - blocks_with_black

    return ans
```

#### 复杂度

- **时间复杂度**：`O(k)`（`k = len(coordinates)`）  
  - 对每个黑格子只检查最多 4 次，哈希表的增删查都是 `O(1)`，所以整体是线性与黑格子数量成正比。  
  - 与 `m·n`（可能高达 `10¹⁰`）相比，`k ≤ 10⁴`，速度提升数万倍。

- **空间复杂度**：`O(k)`  
  - 哈希表最多存储 `4·k` 条记录（每个黑格子最多影响 4 块），因此空间随黑格子数线性增长，远小于存整张网格的 `O(m·n)`。

> **对比**：暴力解需要遍历所有块（`O(m·n)`），最优解只遍历受影响的块（`O(k)`），这正是“只关心有信息的地方”的思路。

---

## 心得

- **核心技巧**：**只统计受黑格子影响的局部子结构**，利用哈希表（字典）对稀疏信息进行计数。  
- **适用场景**：  
  1. **稀疏矩阵统计**（如 “Number of Islands” 中只遍历陆地）  
  2. **子矩阵计数**（如 “Maximum Submatrix Sum” 中只关心含有特定元素的子矩阵）  
  3. **局部影响传播**（如 “Maximum Area of a Piece of Cake After Horizontal and Vertical Cuts”）  
- **一句话总结**：  
  > “当整体规模太大而有效元素少时，用哈希表记录每个有效元素能影响的局部结构，避免全局遍历。”

---

## 反思

- **拿到题目第一反应**：直接把网格画出来，暴力枚举每个 2×2 小块。  
- **最容易踩的坑**：  
  - 忘记检查左上角坐标的合法性，导致访问越界。  
  - 统计 `ans[0]` 时忘记减去已经计入哈希表的块数。  
  - 对坐标的偏移方向弄混（`dx, dy` 的取值必须是 `-1` 或 `0`，而不是 `+1`）。  
- **下次遇到同类题**：第一步先估算 **有效元素的数量** 与 **整体搜索空间** 的比例，若前者远小于后者，就立刻考虑 **基于稀疏信息的局部统计**（哈希表、集合等）来削减时间复杂度。