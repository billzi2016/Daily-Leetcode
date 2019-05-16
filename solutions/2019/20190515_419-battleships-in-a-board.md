# #419. 棋盘上的战舰 / Battleships in a Board

> 难度：中等 · 标签：Array、Depth-First Search、Matrix · [LeetCode 链接](https://leetcode.com/problems/battleships-in-a-board/)

---

## 题目（英文原版）

**Description**

Given an m x n matrix board where each cell is a battleship 'X' or empty '.', return the number of the battleships on board.
Battleships can only be placed horizontally or vertically on board. In other words, they can only be made of the shape 1 x k (1 row, k columns) or k x 1 (k rows, 1 column), where k can be of any size. At least one horizontal or vertical cell separates between two battleships (i.e., there are no adjacent battleships).
Follow up: Could you do it in one-pass, using only O(1) extra memory and without modifying the values board?

**Examples**

**Example 1:**

```
Input: board = [["X",".",".","X"],[".",".",".","X"],[".",".",".","X"]]
Output: 2
```

**Example 2:**

```
Input: board = [["."]]
Output: 0
```

**Constraints**

- m == board.length
- n == board[i].length
- 1 <= m, n <= 200
- board[i][j] is either '.' or 'X'.

---

## 题目（中文翻译）

给定一个 **m × n 矩阵 board**（board 为二维数组），其中每个单元格要么是战舰 `'X'`，要么是空格 `'.'`，返回棋盘上战舰的数量。

战舰只能水平或垂直放置。换句话说，战舰只能呈现 **1 × k**（1 行 k 列）或 **k × 1**（k 行 1 列）的形状，`k` 可以是任意正整数。任意两艘战舰之间必须至少有一个水平或垂直方向的空格相隔（即不存在相邻的战舰）。

**示例 1：**  
**示例 2：**  

**约束条件**  
- `m == board.length`  
- `n == board[i].length`  
- `1 <= m, n <= 200`  
- `board[i][j]` 只能是 `'.'` 或 `'X'`  

**进阶**：能否只遍历一次（one-pass），使用 **O(1)** 额外空间，并且不修改 `board` 的值？

---

**示例：**

**示例 1:**  
Input: board = [["X",".",".","X"],[".",".",".","X"],[".",".",".","X"]]  
Output: 2  

**示例 2:**  
Input: board = [["."]]  
Output: 0

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每一个 `'X'` 当成“未访问的舰体”，然后用 **深度优先搜索（DFS）** 把和它相连的同一艘战舰的所有格子全部遍历掉，遍历完一条连通块后计数器 `count` 加一。  
- **数据结构**：使用 **栈 / 递归** 来实现 DFS，类似于我们在地图上找连通的陆地（“岛屿”）时的做法。  
- **生活化类比**：想象你在一张纸上画了若干条直线（只能水平或垂直），每条线都是一艘战舰。现在要数有几条线，你可以从左上角逐格检查：一旦碰到线段的起点，就把这条线的所有格子都“擦掉”，这样后面再看到的 `'X'` 就一定是另一条新线的起点了。  
- **为什么正确**：DFS 会把所有与当前 `'X'` 直接相邻（上下左右）的 `'X'` 都访问到，而题目保证同一艘战舰只能是直线形状，所以 DFS 访问的恰好是一整条舰体。每遍历完一条舰体，就说明找到了 **一艘** 战舰。  

#### 代码（Python）

```python
from typing import List

def countBattleships_brute(board: List[List[str]]) -> int:
    """
    暴力解法：对每个未访问的 'X' 做深度优先搜索，把整条舰体标记为已访问，
    计数器加一。
    """
    if not board:
        return 0

    m, n = len(board), len(board[0])
    visited = [[False] * n for _ in range(m)]   # 记录哪些格子已经遍历

    def dfs(i: int, j: int) -> None:
        """递归地把与 (i, j) 相连的所有 'X' 标记为已访问"""
        # 越界或不是 'X' 或已经访问过，直接返回
        if i < 0 or i >= m or j < 0 or j >= n or board[i][j] != 'X' or visited[i][j]:
            return
        visited[i][j] = True                     # 标记为已访问
        # 四个方向继续搜索（这里其实只会走成一条直线）
        dfs(i + 1, j)   # 下
        dfs(i - 1, j)   # 上
        dfs(i, j + 1)   # 右
        dfs(i, j - 1)   # 左

    count = 0
    for i in range(m):
        for j in range(n):
            # 找到一个未访问的舰体起点，就 DFS 并计数
            if board[i][j] == 'X' and not visited[i][j]:
                dfs(i, j)
                count += 1
    return count
```

#### 复杂度

- **时间复杂度**：`O(m * n)`  
  每个格子最多被访问常数次（一次检查 + 最多一次 DFS 标记），所以整体是线性时间。  
  用大白话说，就是如果棋盘有 200×200=40,000 格子，最多跑 40,000 次“检查”。
- **空间复杂度**：`O(m * n)`  
  额外的 `visited` 二维数组需要和原棋盘等大的空间。递归栈最坏也会达到 `O(m * n)`（全是 `'X'` 时会递归遍历整条舰体）。

---

### 2. 最优解

#### 思路  

从暴力解出发，**瓶颈** 出现在额外的 `visited` 数组以及递归/栈的开销。实际上，题目已经给了我们 **“舰体之间至少有一个空格隔开”** 的强限制，这意味着我们可以 **只用一次遍历**，并且 **不需要额外的记忆** 来判断一格 `'X'` 是否已经属于某艘已经计数的战舰。

关键观察：

1. **左上角判定**  
   对于任意一个 `'X'`，如果它的上方 (`i-1, j`) 和左方 (`i, j-1`) 都不是 `'X'`，那么它一定是某艘战舰的 **起始格子**（左上角）。因为如果上面或左面有 `'X'`，那格子必然属于同一艘水平或垂直的舰体，而我们已经在更早的遍历位置统计过这艘舰体。

2. **一遍扫描即可**  
   按行从左到右、从上到下遍历棋盘，只要满足上面两点的 `'X'` 就计数。这样每艘舰体只会被计数一次。

3. **不需要修改 board**  
   只读取，不写入，满足 Follow‑up 的 “不修改 board” 要求。

类比：把棋盘想象成一篇文字，`'X'` 是单词的第一个字母，只有当它左边和上边不是字母时，它才是新单词的开头。我们只需要数这些开头的数量。

#### 代码（Python）

```python
from typing import List

def countBattleships(board: List[List[str]]) -> int:
    """
    最优解：一次遍历，统计每艘战舰左上角的 'X'，空间 O(1)。
    """
    if not board:
        return 0

    m, n = len(board), len(board[0])
    count = 0

    for i in range(m):
        for j in range(n):
            # 只关心 'X'，其余直接跳过
            if board[i][j] != 'X':
                continue

            # 若上方有 'X'，说明当前格子属于向下延伸的同一艘舰体，跳过
            if i > 0 and board[i - 1][j] == 'X':
                continue

            # 若左方有 'X'，说明当前格子属于向右延伸的同一艘舰体，跳过
            if j > 0 and board[i][j - 1] == 'X':
                continue

            # 同时满足上、左都不是 'X'，说明是新舰体的起点
            count += 1
    return count
```

#### 复杂度

- **时间复杂度**：`O(m * n)`  
  仍然是线性遍历，只是去掉了递归和额外标记的开销。和暴力解的时间相同，但常数更小，实际运行更快。

- **空间复杂度**：`O(1)`  
  只用了几个整数变量（`count、i、j`），不随棋盘大小增长。这里的 **O(1)** 意味着“常量级”，无论棋盘有多大，额外占用的内存都几乎不变。

---

## 心得

- **核心技巧**：利用题目给出的 “相邻战舰之间至少有一个空格” 的约束，把 **“计数左上角”** 这一几何特性抽象出来，从而实现 **一次遍历、O(1) 额外空间** 的解法。  
- **适用的题型**  
  1. **岛屿计数（LeetCode 200）** 的变形：若岛屿只能是矩形且相互不相邻，也可以用左上角计数。  
  2. **统计矩阵中不相交的直线段**（例如 “Number of Submatrices With All Ones” 中的特例）。  
  3. **棋盘类问题** 中的 “不相交的单元格集合” 计数，如 “Count Sub Islands”。  
- **一句话总结解题钥匙**：**只数每艘舰体的左上角**，其余格子自然被忽略。

---

## 反思

- **第一反应**：看到 “水平或垂直的 1×k / k×1” 形状，我首先想到用 DFS 把相连的 `'X'` 全部标记掉——这是最直观的“连通块计数”。  
- **最容易踩的坑**  
  1. **忘记相邻舰体的间隔**：如果不利用“至少有一个空格”，可能会在计数时把同一艘舰体计成多条。  
  2. **边界检查**：在最优解里判断 `i-1`、`j-1` 时，需要先确认 `i>0`、`j>0`，否则会越界。  
  3. **误以为可以在原地修改**：Follow‑up 要求 **不修改 board**，所以不能把已访问的 `'X'` 改成 `'.'`。  
- **下次遇到同类题**：第一步先检查“是否有额外的空间/相邻限制”。如果相邻的结构有明确的“间隔”或“只能水平/垂直”，往往可以 **从局部（左上角/起点）出发**，用一次遍历直接计数，省去 DFS/并查集等额外开销。