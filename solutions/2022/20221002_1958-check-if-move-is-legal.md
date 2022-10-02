# #1958. 检查移动是否合法 / Check if Move is Legal

> 难度：中等 · 标签：Array、Matrix、Enumeration · [LeetCode 链接](https://leetcode.com/problems/check-if-move-is-legal/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed 8 x 8 grid board, where board[r][c] represents the cell (r, c) on a game board. On the board, free cells are represented by '.', white cells are represented by 'W', and black cells are represented by 'B'.
Each move in this game consists of choosing a free cell and changing it to the color you are playing as (either white or black). However, a move is only legal if, after changing it, the cell becomes the endpoint of a good line (horizontal, vertical, or diagonal).
A good line is a line of three or more cells (including the endpoints) where the endpoints of the line are one color, and the remaining cells in the middle are the opposite color (no cells in the line are free). You can find examples for good lines in the figure below:
Given two integers rMove and cMove and a character color representing the color you are playing as (white or black), return true if changing cell (rMove, cMove) to color color is a legal move, or false if it is not legal.

**Examples**

**Example 1:**

```
Input: board = [[".",".",".","B",".",".",".","."],[".",".",".","W",".",".",".","."],[".",".",".","W",".",".",".","."],[".",".",".","W",".",".",".","."],["W","B","B",".","W","W","W","B"],[".",".",".","B",".",".",".","."],[".",".",".","B",".",".",".","."],[".",".",".","W",".",".",".","."]], rMove = 4, cMove = 3, color = "B"
Output: true
Explanation: '.', 'W', and 'B' are represented by the colors blue, white, and black respectively, and cell (rMove, cMove) is marked with an 'X'.
The two good lines with the chosen cell as an endpoint are annotated above with the red rectangles.
```

**Example 2:**

```
Input: board = [[".",".",".",".",".",".",".","."],[".","B",".",".","W",".",".","."],[".",".","W",".",".",".",".","."],[".",".",".","W","B",".",".","."],[".",".",".",".",".",".",".","."],[".",".",".",".","B","W",".","."],[".",".",".",".",".",".","W","."],[".",".",".",".",".",".",".","B"]], rMove = 4, cMove = 4, color = "W"
Output: false
Explanation: While there are good lines with the chosen cell as a middle cell, there are no good lines with the chosen cell as an endpoint.
```

**Constraints**

- board.length == board[r].length == 8
- 0 <= rMove, cMove < 8
- board[rMove][cMove] == '.'
- color is either 'B' or 'W'.

---

## 题目（中文翻译）

你得到一个下标从 0 开始的 8 × 8 网格 `board`，其中 `board[r][c]` 表示游戏棋盘上的单元格 `(r, c)`。棋盘上，空格用 `'.'` 表示，白子用 `'W'` 表示，黑子用 `'B'` 表示。  

每一步的操作是选择一个空格并将其改为你所执的颜色（白色或黑色）。只有当改动后，该单元格成为一条**好线（good line）**的端点时，这一步才合法。  

**好线（good line）** 是指由三格或以上单元格组成的一条直线（水平、垂直或对角），其中两端的单元格颜色相同，且中间的所有单元格颜色均为相反的颜色（整条线中不能出现空格）。下面的示意图中展示了若干好线的例子。  

给定整数 `rMove`、`cMove` 和字符 `color`（表示你所执的颜色，白色或黑色），若将单元格 `(rMove, cMove)` 改为 `color` 是一次合法的移动，则返回 `true`；否则返回 `false`。

## 示例

### 示例 1  
**输入**  
```json
board = [[".",".",".","B",".",".",".","."],
         [".",".",".","W",".",".",".","."],
         [".",".",".","W",".",".",".","."],
         [".",".",".","W",".",".",".","."],
         ["W","B","B",".","W","W","W","B"],
         [".",".",".","B",".",".",".","."],
         [".",".",".","B",".",".",".","."],
         [".",".",".","W",".",".",".","."]],
rMove = 4, cMove = 3, color = "B"
```
**输出**  
```
true
```
**解释**  
`'.'`、`'W'`、`'B'` 分别对应空格、白子和黑子。将位置 `(4, 3)` 的空格改为黑子后，它成为了一条好线的端点，因此这一步合法。

### 示例 2  
**输入**  
```json
board = [[".",".",".",".",".",".",".","."],
         [".","B",".",".","W",".",".","."],
         [".",".","W",".",".",".",".","."],
         [".",".",".","W","B",".",".","."],
         [".",".",".",".",".",".",".","."],
         [".",".",".",".","B","W",".","."],
         [".",".",".",".",".",".","W","."],
         [".",".",".",".",".",".",".","B"]],
rMove = 4, cMove = 4, color = "W"
```
**输出**  
```
false
```
**解释**  
虽然以选中的单元格为中心可以形成若干好线，但在改为白子后，仍然没有任何好线的端点位于该单元格，因此这一步不合法。

## 约束条件

- `board.length == board[r].length == 8`
- `0 <= rMove, cMove < 8`
- `board[rMove][cMove] == '.'`
- `color` 只能是 `'B'` 或 `'W'`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可能的直线都枚举一遍，看看有没有满足 “好线” 条件的**。  
这里的“直线”指的是八个方向（上下、左右、四条对角线）上的连续格子。

- **数据结构**：  
  - `board` 本身就是一个 8×8 的二维列表（相当于一个 8 行 8 列的表格），我们只需要**遍历它的坐标**。  
  - “方向”可以用一个二元组 `(dx, dy)` 表示，例如向右是 `(0, 1)`，向左上是 `(-1, -1)`。这有点像查字典时的“键”，键对应的值就是我们要走的步伐。

- **为什么正确**：  
  - 题目要求**新落子的格子必须是好线的一个端点**。如果我们把每个方向上可能的长度都检查一遍，就一定能发现所有满足条件的线。只要有一条满足，就说明这一步是合法的。

- **枚举细节**：  
  1. 先把目标格子 `(rMove, cMove)` 暂时改成 `color`（因为合法性是“改完之后”判断的）。  
  2. 对每个方向 `(dx, dy)`：  
     - 从新格子往该方向走，第一个格子必须是**对手颜色**（即 `opposite = 'B' if color=='W' else 'W'`），否则这条方向根本不可能构成好线。  
     - 再继续往同一方向走，只要一直是对手颜色就继续。  
     - 当第一次遇到**和自己颜色相同**的格子时（且已经走过至少两格），说明找到了一个端点——这条线的长度 ≥ 3，且中间全部是对手颜色，符合“好线”。  
     - 途中如果碰到 `'.'`（空格）或者走出棋盘，就直接终止这条方向的检查。  

- **复杂度分析（大白话版）**：  
  - 我们最多检查 **8 条方向**，每条方向最远走到棋盘边界（最多 7 步，因为已经站在一个格子上）。  
  - 所以最多检查 `8 × 7 = 56` 次格子，这在常数级别。用算法的语言写成 **O(8·8) ≈ O(1)**，意思是**不随输入规模增长而增长**（因为棋盘大小固定是 8×8）。  
  - 空间上只用了几个临时变量，**O(1)**，也就是几块小纸片的空间。

#### 代码（Python）

```python
def checkMove(board, rMove, cMove, color):
    # 1. 把目标格子改成自己的颜色（模拟落子）
    board[rMove][cMove] = color

    # 2. 对手的颜色
    opposite = 'B' if color == 'W' else 'W'

    # 8 个方向的向量：水平、垂直、两条对角线
    directions = [
        (0, 1),   # 右
        (0, -1),  # 左
        (1, 0),   # 下
        (-1, 0),  # 上
        (1, 1),   # 右下
        (1, -1),  # 左下
        (-1, 1),  # 右上
        (-1, -1)  # 左上
    ]

    for dx, dy in directions:
        x, y = rMove + dx, cMove + dy   # 第一步走向该方向
        cnt_opposite = 0                # 记录遇到的对手颜色格子数

        # 只要没有越界且格子不是空的，就一直往前走
        while 0 <= x < 8 and 0 <= y < 8 and board[x][y] != '.':
            if board[x][y] == opposite:
                cnt_opposite += 1       # 中间必须是对手颜色
            else:                       # 遇到和自己颜色相同的格子
                # 好线要求：端点颜色相同，且中间至少有 1 个对手颜色格子
                if cnt_opposite >= 1:
                    return True        # 找到合法的好线，直接返回 True
                break                 # 如果中间没有对手颜色，直接终止该方向

            # 往该方向继续前进
            x += dx
            y += dy

    # 所有方向都没有找到合法的好线
    return False
```

> **关键行中文注释**已经写在代码里，帮助你一步步跟踪思路。

#### 复杂度

- **时间复杂度**：`O(8·8) ≈ O(1)`  
  - 解释：我们最多检查 8 条方向，每条最多走 7 步，总共 56 次检查。对初学者来说，就是**几乎不花时间**，因为棋盘固定小。

- **空间复杂度**：`O(1)`  
  - 只用了常数个变量（方向数组、几个计数器），不随棋盘大小变化。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正的瓶颈并不是时间**（已经是常数），而是**代码的可读性和提前剪枝**。  
我们可以把思路再抽象一次，使得代码更简洁、更容易解释：

1. **只检查“端点在新格子” 的情况**。好线的两个端点必须颜色相同，而我们已经把新格子设成 `color`，所以只需要向外找 **第一个** 同颜色格子，且它们之间必须全是对手颜色。  
2. **在每个方向上一次遍历即可**：  
   - 第一步必须是对手颜色（如果不是，直接放弃该方向）。  
   - 接下来一直往前走，只要仍然是对手颜色就继续。  
   - 当遇到同颜色格子时，只要已经走过 **至少两格**（即中间出现了对手颜色），就成功。  
   - 一旦遇到空格或出界，就立刻终止该方向。  

这样做的好处是**不必在每个可能的长度都重新判断**，而是**一边走一边判断**，更像在找“第一条满足条件的线”。时间仍然是常数，但思路更贴近“从新格子往外搜索”，更容易在面试或实际编程中迁移到更大的棋盘。

下面给出更简洁的实现：

#### 代码（Python）

```python
def checkMove(board, rMove, cMove, color):
    # 把新格子改成自己的颜色（模拟落子）
    board[rMove][cMove] = color
    opposite = 'B' if color == 'W' else 'W'

    # 8 个方向
    dirs = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]

    for dx, dy in dirs:
        x, y = rMove + dx, cMove + dy

        # 必须先遇到对手颜色，才能继续往前找端点
        if not (0 <= x < 8 and 0 <= y < 8) or board[x][y] != opposite:
            continue          # 这条方向直接跳过

        # 已经确认第一个格子是对手颜色，继续往前
        while True:
            x += dx
            y += dy
            # 越界或遇到空格，说明这条方向不行
            if not (0 <= x < 8 and 0 <= y < 8) or board[x][y] == '.':
                break
            # 遇到同颜色格子，说明找到了另一端点
            if board[x][y] == color:
                return True   # 合法移动
            # 否则还是对手颜色，继续循环

    return False
```

> 代码里每一步都写了 **“先检查第一个格子是否为对手颜色”**，这一步相当于 **提前剪枝**，可以避免不必要的循环。

#### 复杂度

- **时间复杂度**：`O(8·8) ≈ O(1)`  
  - 与暴力解相同，但因为我们在每条方向上只遍历一次，实际运行的次数更少。可以理解为“最多检查 56 次格子”，在 8×8 的棋盘上几乎瞬间完成。

- **空间复杂度**：`O(1)`  
  - 只用了几个整型变量和方向列表，仍然是常数空间。

---

## 心得

- **核心技巧**：**沿八个方向一次遍历，寻找“先是对手颜色、后是同颜色端点” 的模式**。这是一种**方向搜索**（directional scan）的思路，常用于棋盘类、矩阵类题目。
- **适用的题型**（类似思路）  
  1. **Reversi（翻转棋）合法落子判定** – 需要在任意方向上找到相邻的对手颜色再到自己的颜色。  
  2. **五子棋/连珠判定** – 判断某一步是否形成连续五子，需要在四个方向上搜索相同颜色的连续块。  
  3. **单词搜索（Word Search）** – 在矩阵中沿八个方向查找连续字符序列。

- **一句话总结解题钥匙**：**“端点在新格子 → 必须先遇到对手 → 再遇到同色端点”**，把这句话翻译成代码就是方向遍历加条件判断。

---

## 反思

- **第一反应**：看到“好线”定义，立刻想到**枚举所有直线**，检查端点颜色和中间颜色的关系。  
- **最容易踩的坑**：  
  - 忘记 **新格子必须先变成自己的颜色** 再进行检查（否则会把空格当成端点）。  
  - 没有确保 **中间至少有一个对手颜色格子**（长度必须 ≥ 3）。  
  - 边界条件处理不当，导致访问 `board[-1][*]` 或 `board[8][*]` 抛异常。  
- **下次遇到同类题**：第一步就**确定要搜索的方向**，并**明确搜索顺序（先对手后同色）**，然后把这条“搜索路线”写成循环，边走边判断是否满足终止条件。这样可以快速定位合法性，避免冗余的遍历。