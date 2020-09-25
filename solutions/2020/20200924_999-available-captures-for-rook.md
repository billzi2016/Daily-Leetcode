# #999. 车的可用捕获 / Available Captures for Rook

> 难度：简单 · 标签：Array、Matrix、Simulation · [LeetCode 链接](https://leetcode.com/problems/available-captures-for-rook/)

---

## 题目（英文原版）

**Description**

You are given an 8 x 8 matrix representing a chessboard. There is exactly one white rook represented by 'R', some number of white bishops 'B', and some number of black pawns 'p'. Empty squares are represented by '.'.
A rook can move any number of squares horizontally or vertically (up, down, left, right) until it reaches another piece or the edge of the board. A rook is attacking a pawn if it can move to the pawn's square in one move.
Note: A rook cannot move through other pieces, such as bishops or pawns. This means a rook cannot attack a pawn if there is another piece blocking the path.
Return the number of pawns the white rook is attacking.

**Examples**

**Example 1:**

```
Input: board = [[".",".",".",".",".",".",".","."],[".",".",".","p",".",".",".","."],[".",".",".","R",".",".",".","p"],[".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".","."],[".",".",".","p",".",".",".","."],[".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".","."]]
Output: 3
Explanation:
In this example, the rook is attacking all the pawns.
```

**Example 2:**

```
Input: board = [[".",".",".",".",".",".","."],[".","p","p","p","p","p",".","."],[".","p","p","B","p","p",".","."],[".","p","B","R","B","p",".","."],[".","p","p","B","p","p",".","."],[".","p","p","p","p","p",".","."],[".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".","."]]
Output: 0
Explanation:
The bishops are blocking the rook from attacking any of the pawns.
```

**Example 3:**

```
Input: board = [[".",".",".",".",".",".",".","."],[".",".",".","p",".",".",".","."],[".",".",".","p",".",".",".","."],["p","p",".","R",".","p","B","."],[".",".",".",".",".",".",".","."],[".",".",".","B",".",".",".","."],[".",".",".","p",".",".",".","."],[".",".",".",".",".",".",".","."]]
Output: 3
Explanation:
The rook is attacking the pawns at positions b5, d6, and f5.
```

**Constraints**

- board.length == 8
- board[i].length == 8
- board[i][j] is either 'R', '.', 'B', or 'p'
- There is exactly one cell with board[i][j] == 'R'

---

## 题目（中文翻译）

你得到一个 **8 × 8** 矩阵（**board**）表示的国际象棋棋盘。棋盘上恰好有一个白车，用字符 `'R'` 表示；若干个白象，用字符 `'B'` 表示；若干个黑兵，用字符 `'p'` 表示。空格用字符 `'.'` 表示。

- 车可以在水平方向或垂直方向（上、下、左、右）移动任意格，直到遇到另一枚棋子或棋盘边缘为止。
- 若车能够在一次移动中到达某个黑兵所在的格子，则称该车 **正在攻击**（attacking）该兵。
- 车不能越过其他棋子（例如象或兵），因此如果路径上有其他棋子阻挡，则车无法攻击该兵。

**返回** 白车能够攻击的黑兵的数量。

---

### 示例

**示例 1**

```
Input: board = [[".",".",".",".",".",".",".","."],
                [".",".",".","p",".",".",".","."],
                [".",".",".","R",".",".",".","p"],
                [".",".",".",".",".",".",".","."],
                [".",".",".",".",".",".",".","."],
                [".",".",".","p",".",".",".","."],
                [".",".",".",".",".",".",".","."],
                [".",".",".",".",".",".",".","."]]
Output: 3
Explanation:
在这个例子中，车可以直接吃掉所有的兵。
```

**示例 2**

```
Input: board = [[".",".",".",".",".",".",".","."],
                [".","p","p","p","p","p",".","."],
                [".","p","p","B","p","p",".","."],
                [".","p","B","R","B","p",".","."],
                [".","p","p","B","p","p",".","."],
                [".","p","p","p","p","p",".","."],
                [".",".",".",".",".",".",".","."],
                [".",".",".",".",".",".",".","."]]
Output: 0
Explanation:
象阻挡了车与所有兵之间的路径，车无法捕获任何兵。
```

**示例 3**

```
Input: board = [[".",".",".",".",".",".",".","."],
                [".",".",".","p",".",".",".","."],
                [".",".",".","p",".",".",".","."],
                ["p","p",".","R",".","p","B","."],
                [".",".",".",".",".",".",".","."],
                [".",".",".","B",".",".",".","."],
                [".",".",".","p",".",".",".","."],
                [".",".",".",".",".",".",".","."]]
Output: 3
Explanation:
车正在攻击位于 b5、d6 和 f5 的三枚兵。
```

---

### 约束条件

- `board.length == 8`
- `board[i].length == 8`
- `board[i][j]` 仅可能是 `'R'`、`'.'`、`'B'` 或 `'p'`
- 棋盘中恰好只有一个位置满足 `board[i][j] == 'R'`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是**先把所有黑兵（'p'）找出来**，再判断每个黑兵能否被车（'R'）吃掉。  
判断的依据有两点：

1. **同一行或同一列**：只有在同一行或同一列时，车才有可能直线攻击到兵。  
2. **中间没有其他棋子阻挡**：从车到兵的直线路径上不能出现白象（'B'）或其他黑兵（'p'），否则车走不过去。

这就像我们在一条直路上观察两辆车能否相遇：如果它们在同一条直路上，而且中间没有其他车辆挡道，它们就能“碰面”。

实现步骤：

1. 遍历整个 8×8 棋盘，记录车的位置 `(rx, ry)`，以及所有黑兵的位置列表 `pawns`。  
2. 对每个黑兵 `(px, py)`：  
   - 若 `px == rx`（同一行），检查 `ry` 与 `py` 之间的所有格子是否全是 `'.'`（空格），如果是则这颗兵可以被吃。  
   - 若 `py == ry`（同一列），同理检查 `rx` 与 `px` 之间的格子。  
3. 计数即可。

**为什么这个方法一定正确？**  
因为我们穷举了每一颗黑兵，并且严格按照棋子的走法（只能横竖直线）以及阻挡规则来判断。只要满足上述两点，车一定能在一次移动内吃到该兵；不满足则一定吃不到。

**复杂度分析（大白话）**  

- 时间复杂度：我们先遍历一遍棋盘找车和所有兵，**O(64)**（常数），随后对每颗兵再检查最多 7 格（因为同一行/列最多 7 格），最坏情况是 8 颗兵，所以检查的次数约为 `8 × 7 = 56`，仍然是常数级。整体可以写成 **O(n²)**（这里 n=8），意思是随棋盘尺寸的平方增长。但因为尺寸固定为 8，实际运行非常快。  
- 空间复杂度：只用了几个变量存坐标和一个列表保存最多 8 颗兵的位置，**O(1)**（常数空间），意思是占用的内存不会随输入大小增长。

#### 代码（Python）

```python
from typing import List

def numRookCaptures(board: List[List[str]]) -> int:
    # 1️⃣ 找到车的位置以及所有黑兵的位置
    rook_x = rook_y = -1
    pawns = []                     # 用来存每颗黑兵的坐标
    for i in range(8):
        for j in range(8):
            if board[i][j] == 'R':
                rook_x, rook_y = i, j
            elif board[i][j] == 'p':
                pawns.append((i, j))

    # 2️⃣ 逐个判断黑兵能否被吃
    captures = 0
    for px, py in pawns:
        # 同一行：横向检查
        if px == rook_x:
            # 计算两个列号之间的最小、最大值（不包括两端）
            left, right = sorted([rook_y, py])
            blocked = False
            for y in range(left + 1, right):
                if board[px][y] != '.':   # 遇到任何非空格都算阻挡
                    blocked = True
                    break
            if not blocked:               # 没有阻挡，车可以吃掉这颗兵
                captures += 1
                continue                 # 已经算过了，直接看下一颗

        # 同一列：纵向检查
        if py == rook_y:
            top, bottom = sorted([rook_x, px])
            blocked = False
            for x in range(top + 1, bottom):
                if board[x][py] != '.':
                    blocked = True
                    break
            if not blocked:
                captures += 1

    return captures
```

#### 复杂度

- **时间复杂度**：`O(n²)`（这里 n=8），因为我们遍历了棋盘的每一个格子两次（一次找位置，一次检查），大白话就是“即使棋盘再大，时间也会随格子数量的平方增长”。  
- **空间复杂度**：`O(1)`，只用了常数个变量来保存坐标和计数。

---

### 2. 最优解

#### 思路  
从暴力解可以看出，**真正的耗时在于对每颗兵都要重新遍历路径**。其实我们只需要**从车出发，沿四个方向一直往前走**，遇到第一颗黑兵就计数，遇到白象就停止该方向的搜索。这样只遍历棋盘一次，而且每个方向最多走 7 步，时间更明确为 `O(8)`，即 **O(1)**。

优化的关键点：

1. **只从车的位置出发**，而不是遍历所有兵。  
2. **四个方向分别使用循环**（上、下、左、右），每次移动一步，检查当前格子：
   - 如果是空格 `'.'` → 继续前进。  
   - 如果是白象 `'B'` → 该方向被阻挡，直接停止。  
   - 如果是黑兵 `'p'` → 可以吃，计数后同样停止（因为车只能吃掉最近的那颗兵，后面的兵被阻挡）。  

这就像站在十字路口的警察，只需要看四条直路上有没有违规车辆，看到第一辆违规车就记一次，后面的车因为已经被第一辆拦住了自然不需要再看。

#### 代码（Python）

```python
from typing import List

def numRookCaptures(board: List[List[str]]) -> int:
    # 1️⃣ 找到车的位置（只需要一次遍历）
    for i in range(8):
        for j in range(8):
            if board[i][j] == 'R':
                rook_x, rook_y = i, j
                break

    captures = 0
    # 四个方向的向量：上、下、左、右
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dx, dy in directions:
        x, y = rook_x + dx, rook_y + dy
        # 继续往该方向走，直到出界或被阻挡
        while 0 <= x < 8 and 0 <= y < 8:
            cell = board[x][y]
            if cell == 'B':          # 遇到白象，方向结束
                break
            if cell == 'p':          # 遇到黑兵，计数后也结束
                captures += 1
                break
            # 为空格，继续前进
            x += dx
            y += dy

    return captures
```

#### 复杂度

- **时间复杂度**：`O(1)`（常数时间）。我们最多检查车所在行列的 4 条直线，每条最多 7 步，总共不超过 28 次访问。大白话就是“无论棋盘多大，这段代码的运行次数都是一个固定的小数字”。  
- **空间复杂度**：`O(1)`，只用了几个整数来保存坐标和计数，额外空间不随输入变化。

---

## 心得

- **核心技巧**：**从关键点（车）出发的四向扫描**。只要明确“从哪儿开始”和“哪些格子会阻止继续”，就能把遍历范围压到最小。  
- **适用的题型**：  
  1. “棋盘上某个棋子可以攻击多少目标”类（如 **LeetCode 463. Island Perimeter** 中的四向遍历）。  
  2. “寻找最近的障碍物”类（如 **LeetCode 2178. Maximum Split of Positive Even Integers** 中的线性扫描）。  
  3. “从某一点向四个方向扩散”类（如 **LeetCode 2120. Execution of All Sales Orders** 中的 BFS/DFS 简化版）。  
- **一句话总结解题钥匙**：**“定位起点 → 按方向一步步前进 → 碰到阻挡或目标即停”。**

---

## 反思

- **第一反应**：看到“车只能横竖走”，立刻想到遍历四个方向；但最初会想把所有兵列出来再逐个判断，导致不必要的重复检查。  
- **最容易踩的坑**：  
  - **边界检查**：忘记判断 `x, y` 是否仍在 0~7 范围内，容易出现 IndexError。  
  - **阻挡判断**：只要遇到白象就必须立刻停止，否则会错误计数后面的兵。  
  - **计数一次后仍继续**：每个方向只能计数最近的那颗兵，计数后一定要 `break`。  
- **下次遇到同类题**，第一步应该想：“**从关键点出发，沿可移动的方向直线搜索，遇阻或得分立即停止**”。这样往往能直接得到最优的线性/常数时间解。