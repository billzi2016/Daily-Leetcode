# #2596. 检查骑士巡游配置 / Check Knight Tour Configuration

> 难度：中等 · 标签：Array、Depth-First Search、Breadth-First Search、Matrix、Simulation · [LeetCode 链接](https://leetcode.com/problems/check-knight-tour-configuration/)

---

## 题目（英文原版）

**Description**

There is a knight on an n x n chessboard. In a valid configuration, the knight starts at the top-left cell of the board and visits every cell on the board exactly once.
You are given an n x n integer matrix grid consisting of distinct integers from the range [0, n * n - 1] where grid[row][col] indicates that the cell (row, col) is the grid[row][col]th cell that the knight visited. The moves are 0-indexed.
Return true if grid represents a valid configuration of the knight's movements or false otherwise.
Note that a valid knight move consists of moving two squares vertically and one square horizontally, or two squares horizontally and one square vertically. The figure below illustrates all the possible eight moves of a knight from some cell.

**Examples**

**Example 1:**

```
Input: grid = [[0,11,16,5,20],[17,4,19,10,15],[12,1,8,21,6],[3,18,23,14,9],[24,13,2,7,22]]
Output: true
Explanation: The above diagram represents the grid. It can be shown that it is a valid configuration.
```

**Example 2:**

```
Input: grid = [[0,3,6],[5,8,1],[2,7,4]]
Output: false
Explanation: The above diagram represents the grid. The 8th move of the knight is not valid considering its position after the 7th move.
```

**Constraints**

- n == grid.length == grid[i].length
- 3 <= n <= 7
- 0 <= grid[row][col] < n * n
- All integers in grid are unique.

---

## 题目（中文翻译）

在一个 n × n 的棋盘上有一只骑士（knight）。在**有效配置**（valid configuration）中，骑士从棋盘的左上角格子出发，恰好访问棋盘上的每一个格子一次。

给定一个 n × n 的整数矩阵 `grid`，其中 `grid[row][col]` 表示格子 `(row, col)` 是骑士访问的第 `grid[row][col]` 步（步数从 0 开始计数）。矩阵中的整数互不相同，且均在区间 `[0, n * n - 1]` 内。

如果 `grid` 表示一次合法的骑士移动序列，则返回 `true`；否则返回 `false`。

> 注意：合法的骑士移动指的是一次纵向移动两个格子并横向移动一个格子，或一次横向移动两个格子并纵向移动一个格子。下图展示了骑士从任意格子出发的八种可能移动方式。

### 示例

#### 示例 1
```text
输入: grid = [[0,11,16,5,20],
              [17,4,19,10,15],
              [12,1,8,21,6],
              [3,18,23,14,9],
              [24,13,2,7,22]]
输出: true
解释: 上图对应的 `grid` 可以构成一次有效的骑士巡游。
```

#### 示例 2
```text
输入: grid = [[0,3,6],
              [5,8,1],
              [2,7,4]]
输出: false
解释: 上图对应的 `grid` 中，第 8 步（即编号为 7 的格子）在第 7 步之后的位置不满足骑士的合法移动规则。
```

### 约束条件
- `n == grid.length == grid[i].length`
- `3 <= n <= 7`
- `0 <= grid[row][col] < n * n`
- `grid` 中的所有整数互不相同。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：  
1. **从 0 开始**，在整张棋盘里把 `0`、`1`、`2` … `n*n-1` 逐个找出来。  
2. 找到相邻的两个序号后，检查它们之间的相对位置是否符合骑士的走法（两格垂直 + 一格水平，或两格水平 + 一格垂直）。  

> **数据结构类比**：  
> - 这里我们只用到 **二维数组**（棋盘本身）和 **遍历**，不需要额外的“高级”结构。可以把遍历想象成在一本字典里逐页查找某个单词的页码——每次都要从头翻到尾。

**为什么这个方法一定正确？**  
因为题目要求 **每一步** 都必须是合法的骑士跳。只要我们把每一步的起点和终点都找出来并逐对检查，所有条件就被完整覆盖了。

**时间/空间复杂度的大白话**：  
- 时间复杂度 `O(n⁴)`：  
  - `n²` 是棋盘格子总数。我们要找 `0 … n²-1`，每找一个都要在 `n²` 个格子里遍历一次 → `n² × n² = n⁴`。  
  - 想象把一张 `7×7` 的棋盘看成 49 本小书，每本书里还有 49 页，要找 49 本书里每本的第几页——这显然会花很多时间。  
- 空间复杂度 `O(1)`：只用到常数个额外变量（坐标、计数器），不随 `n` 增长。

#### 代码（Python）  

```python
def checkValidGrid_bruteforce(grid):
    n = len(grid)

    # 骑士可以走的 8 种相对位移
    dirs = [(2, 1), (1, 2), (-1, 2), (-2, 1),
            (-2, -1), (-1, -2), (1, -2), (2, -1)]

    # 从 0 到 n*n-2，逐个检查相邻两步是否为合法跳
    for cur in range(n * n - 1):
        # 1️⃣ 在全棋盘里寻找 cur 的坐标
        cur_r = cur_c = -1
        for i in range(n):
            for j in range(n):
                if grid[i][j] == cur:
                    cur_r, cur_c = i, j
        # 2️⃣ 同理寻找 cur+1 的坐标
        nxt_r = nxt_c = -1
        for i in range(n):
            for j in range(n):
                if grid[i][j] == cur + 1:
                    nxt_r, nxt_c = i, j

        # 3️⃣ 检查两坐标是否满足骑士跳的任意一种
        valid = False
        for dr, dc in dirs:
            if cur_r + dr == nxt_r and cur_c + dc == nxt_c:
                valid = True
                break
        if not valid:          # 只要有一步不合法，直接返回 False
            return False
    return True
```

#### 复杂度  

- **时间复杂度**：`O(n⁴)` —— 需要 `n²` 次遍历，每次遍历整张 `n²` 大小的棋盘。  
- **空间复杂度**：`O(1)` —— 只用了常数个临时变量。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈**在于每次都要遍历整张棋盘去找当前步数的坐标。实际上，棋盘里每个数字只会出现一次，我们完全可以在一次遍历时把所有数字的坐标记下来，后面直接查表即可。

**优化步骤**  

1. **一次遍历构建映射**：使用 Python 的字典（相当于“查字典”）把每个数字 `val` 映射到它所在的坐标 `(row, col)`。  
   - 这一步的时间是 `O(n²)`，空间是 `O(n²)`（因为要保存每个格子的坐标）。  
2. **顺序检查**：从 `0` 到 `n²-2`，直接从字典里取出 `cur` 与 `cur+1` 的坐标，判断它们是否符合骑士的 8 种跳法。  
   - 只需要常数时间 `O(1)` 来比较一次，整个过程仍是 `O(n²)`。  

**核心算法/数据结构解释**  

- **字典（哈希表）**：想象你有一本字典，**key** 是单词（这里是格子里的数字），**value** 是页码（这里是坐标）。查找一个单词的页码只需要几秒钟，和翻遍整本书的时间相比快了很多。  
- **骑士的合法位移**：用一组固定的 `(dx, dy)` 表示八个方向，检查 `(r1+dx, c1+dy) == (r2, c2)` 即可。

**为什么是最优的？**  
- 每个格子必须至少看一次（否则无法保证没有遗漏），所以下界是 `Ω(n²)`。我们的做法正好达到这个下界，没有多余的遍历。  

#### 代码（Python）  

```python
def checkValidGrid(grid):
    """
    判断给定的 grid 是否是一次合法的骑士遍历
    """
    n = len(grid)

    # 1️⃣ 预先把每个数字的坐标存进哈希表
    pos = {}                     # key: 数字，value: (row, col)
    for i in range(n):
        for j in range(n):
            pos[grid[i][j]] = (i, j)

    # 2️⃣ 骑士的 8 种可能跳法（相对位移）
    moves = [(2, 1), (1, 2), (-1, 2), (-2, 1),
             (-2, -1), (-1, -2), (1, -2), (2, -1)]

    # 3️⃣ 按顺序检查每一步是否为合法跳
    for cur in range(n * n - 1):
        r1, c1 = pos[cur]        # 当前步的坐标
        r2, c2 = pos[cur + 1]    # 下一步的坐标

        # 判断 (r2, c2) 是否在 (r1, c1) 的八个合法位置之一
        if not any(r1 + dr == r2 and c1 + dc == c2 for dr, dc in moves):
            return False        # 只要有一步不合法，直接否定
    return True                 # 全部检查通过
```

#### 复杂度  

- **时间复杂度**：`O(n²)` —  
  - 第一次遍历把所有坐标放进字典需要 `n²` 次操作。  
  - 第二次遍历检查 `n²‑1` 条相邻关系，每条只做常数次比较。  
  - 用通俗的话说：如果棋盘是 7×7（共 49 格），我们最多只看 49 次，而不是 49×49 次。  
- **空间复杂度**：`O(n²)` — 需要保存每个数字的坐标，等价于再开一张同样大小的表格。  

---

## 心得  

- **核心技巧**：利用哈希表一次性把「数字 → 坐标」建立映射，随后只做常数时间的合法性检查。  
- **适用的题型**：  
  1. **验证路径合法性**（如验证机器人走迷宫的顺序）。  
  2. **序列到坐标的映射**（如 LeetCode 1971 “Find if Path Exists in Grid”).  
  3. **棋盘类的顺序验证**（如验证数独的填充顺序、验证滑动拼图的合法移动）。  
- **一句话总结**：**把所有信息一次性收集好，再用 O(1) 的查表方式逐步验证——避免重复遍历是关键。**

---

## 反思  

- **第一反应**：看到「每个格子都有唯一的序号」就想到「把序号对应到坐标」；随后想到直接遍历寻找相邻序号——这就是暴力解。  
- **最容易踩的坑**：  
  - 忘记检查 **起点必须是 0**（题目保证，但自行实现时要确认）。  
  - 只检查了 `0 → 1 → 2 …` 的顺序，却忘记验证 **所有格子都被访问**（若输入不完整会导致 KeyError）。  
  - 骑士的八种位移写错顺序或漏掉一种，导致误判。  
- **下次遇到同类题**：**第一步就把「位置映射」建好**，然后只用常数时间去验证每一步是否合法。这样可以立刻把时间复杂度从指数级或平方级降到线性级。