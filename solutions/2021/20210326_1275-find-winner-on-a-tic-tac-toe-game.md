# #1275. 判断井字棋游戏的胜者 / Find Winner on a Tic Tac Toe Game

> 难度：简单 · 标签：Array、Hash Table、Matrix、Simulation · [LeetCode 链接](https://leetcode.com/problems/find-winner-on-a-tic-tac-toe-game/)

---

## 题目（英文原版）

**Description**

Tic-tac-toe is played by two players A and B on a 3 x 3 grid. The rules of Tic-Tac-Toe are:
Given a 2D integer array moves where moves[i] = [rowi, coli] indicates that the ith move will be played on grid[rowi][coli]. return the winner of the game if it exists (A or B). In case the game ends in a draw return "Draw". If there are still movements to play return "Pending".
You can assume that moves is valid (i.e., it follows the rules of Tic-Tac-Toe), the grid is initially empty, and A will play first.

**Examples**

**Example 1:**

```
Input: moves = [[0,0],[2,0],[1,1],[2,1],[2,2]]
Output: "A"
Explanation: A wins, they always play first.
```

**Example 2:**

```
Input: moves = [[0,0],[1,1],[0,1],[0,2],[1,0],[2,0]]
Output: "B"
Explanation: B wins.
```

**Example 3:**

```
Input: moves = [[0,0],[1,1],[2,0],[1,0],[1,2],[2,1],[0,1],[0,2],[2,2]]
Output: "Draw"
Explanation: The game ends in a draw since there are no moves to make.
```

**Constraints**

- 1 <= moves.length <= 9
- moves[i].length == 2
- 0 <= rowi, coli <= 2
- There are no repeated elements on moves.
- moves follow the rules of tic tac toe.

---

## 题目（中文翻译）

Tic‑Tac‑Toe（井字棋）在一个 3 × 3 的棋盘上由玩家 A 与玩家 B 进行对弈。游戏规则如下：

给定一个二维整数数组 `moves`，其中 `moves[i] = [row_i, col_i]` 表示第 `i` 步棋会落在 `grid[row_i][col_i]` 位置。返回游戏的胜者（如果存在），即返回 `"A"` 或 `"B"`。若游戏以平局结束则返回 `"Draw"`，若还有未落子的格子且游戏尚未结束则返回 `"Pending"`。

可以假设 `moves` 合法（即符合井字棋的规则），棋盘初始为空，且玩家 A 先手。

**示例 1**

```text
Input: moves = [[0,0],[2,0],[1,1],[2,1],[2,2]]
Output: "A"
Explanation: A 获胜，因为 A 先手并成功形成一条连线。
```

**示例 2**

```text
Input: moves = [[0,0],[1,1],[0,1],[0,2],[1,0],[2,0]]
Output: "B"
Explanation: B 获胜。
```

**示例 3**

```text
Input: moves = [[0,0],[1,1],[2,0],[1,0],[1,2],[2,1],[0,1],[0,2],[2,2]]
Output: "Draw"
Explanation: 棋盘已填满且没有玩家形成连线，游戏以平局结束。
```

**约束条件**

- `1 <= moves.length <= 9`
- `moves[i].length == 2`
- `0 <= row_i, col_i <= 2`
- `moves` 中不存在重复的坐标
- `moves` 符合井字棋的规则

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法就是**把整个 3×3 棋盘保存下来**，每走一步就把对应格子标记为 A 或 B（可以用 `1` 表示 A，`-1` 表示 B，`0` 表示空）。  
随后在每次落子后**遍历所有可能的获胜线路**（3 行、3 列、2 条对角线），检查这条线上的三个格子是否全部相同且非空。  

> **类比**：把棋盘想象成一本小笔记本，`row` 就是第几页，`col` 就是第几行。我们每落子就在对应页的对应行写上自己的名字。要判断是否赢了，就像翻开笔记本，检查每一页的每一行是否全是同一个人的名字。  

这种方法一定能得到正确答案，因为它把**所有可能的赢法都检查了一遍**。只要有一条线满足“同玩家占满三格”，就返回该玩家；如果检查完仍未发现胜者，则根据落子数判断是平局还是未结束。  

#### 代码（Python）  

```python
def tictactoe(moves):
    # 1. 建立 3x3 的棋盘，初始全为 0（空）
    board = [[0] * 3 for _ in range(3)]

    # 2. 依次落子，奇数手（0、2、4…）是 A，用 1 表示；偶数手是 B，用 -1 表示
    for i, (r, c) in enumerate(moves):
        board[r][c] = 1 if i % 2 == 0 else -1   # A 用 1，B 用 -1

    # 3. 定义一个检查函数，判断是否有玩家已经占满一条线
    def win(player):
        target = player * 3          # 3 个 1 或 -1 的和恰好是 3 或 -3
        # 检查每一行
        for row in board:
            if sum(row) == target:
                return True
        # 检查每一列
        for col in range(3):
            if board[0][col] + board[1][col] + board[2][col] == target:
                return True
        # 检查两条对角线
        if board[0][0] + board[1][1] + board[2][2] == target:
            return True
        if board[0][2] + board[1][1] + board[2][0] == target:
            return True
        return False

    # 4. 先判断 A 再判断 B（因为 A 先走，如果 A 已经赢了，B 不会再落子）
    if win(1):
        return "A"
    if win(-1):
        return "B"

    # 5. 若没有人赢，判断棋盘是否已满
    return "Draw" if len(moves) == 9 else "Pending"
```

#### 复杂度  

- **时间复杂度**：`O(9)`（常数级别）  
  - 我们最多检查 8 条线（3 行 + 3 列 + 2 对角线），每条线只算 3 个格子，总共不超过 24 次加法，和棋盘大小 3×3 成正比。  
  - 用大白话说，就是不管怎么走，这段代码的运行时间几乎是**固定不变**的，和输入规模（最多 9 步）线性相关。  

- **空间复杂度**：`O(9)` → `O(1)`  
  - 只用了一个 3×3 的二维数组，占用的空间是常数，不会随 `moves` 长度增长而增长。  

---  

### 2. 最优解  

#### 思路  
暴力解已经很快了，但我们仍然可以**把每一步的判断压到 O(1)**，不必遍历整张棋盘。  
关键在于**把每行、每列、两条对角线的占用情况用计数器保存下来**：

- `rows[i]`：第 `i` 行上 A 的落子数减去 B 的落子数。  
- `cols[j]`：第 `j` 列上 A 的落子数减去 B 的落子数。  
- `diag`：左上→右下对角线的计数（同上）。  
- `anti`：右上→左下对角线的计数。  

当某个计数的绝对值等于 3 时，说明同一个玩家在该行/列/对角线上占满了 3 格，游戏结束。  

> **类比**：把每一行、每一列想象成一本记事本的“分数表”。每当 A 落子，就在对应的行、列、对角线上加 **+1**；每当 B 落子，就减 **1**。一旦某个分数达到 **+3**（全是 A）或 **-3**（全是 B），就可以立刻宣布胜者，而不必再翻查整个棋盘。  

整个过程只需要一次遍历 `moves`，每一步的更新和检查都是 **常数时间**。  

#### 代码（Python）  

```python
def tictactoe(moves):
    # 计数器，长度为 3，分别对应 3 行和 3 列
    rows = [0] * 3
    cols = [0] * 3
    diag = 0          # 主对角线（左上->右下）
    anti = 0          # 副对角线（右上->左下）

    for i, (r, c) in enumerate(moves):
        player = 1 if i % 2 == 0 else -1   # A 用 +1，B 用 -1

        rows[r] += player          # 第 r 行计数
        cols[c] += player          # 第 c 列计数
        if r == c:                 # 落在主对角线
            diag += player
        if r + c == 2:             # 落在副对角线（因为 0+2,1+1,2+0 都等于 2）
            anti += player

        # 检查是否出现绝对值为 3 的计数
        if abs(rows[r]) == 3 or abs(cols[c]) == 3 or abs(diag) == 3 or abs(anti) == 3:
            return "A" if player == 1 else "B"

    # 循环结束仍未分出胜负
    return "Draw" if len(moves) == 9 else "Pending"
```

#### 复杂度  

- **时间复杂度**：`O(n)`，其中 `n = len(moves) ≤ 9`  
  - 每一步只做了几次整数加减和几次绝对值比较，**不随棋盘大小增长**。相较于暴力解遍历整张棋盘的做法，这里把每一步的判断压到了 **常数时间**，整体仍是线性。  

- **空间复杂度**：`O(1)`  
  - 只用了 4 个计数器（`rows`, `cols`, `diag`, `anti`），占用的空间固定不变。  

---  

## 心得  

- **核心技巧**：使用“计数器”来**增量维护行/列/对角线的状态**，从而在 O(1) 时间内判断胜负。  
- **适用的题型**：  
  1. **N×N 井字棋**（LeetCode 1275）  
  2. **矩阵行列求和/差**（如判断是否所有行列和相等）  
  3. **滑动窗口计数**（统计窗口内某类元素的出现次数）  
- **解题钥匙**：**把“检查所有可能”转化为“每一步只更新少量状态”**，用增量维护代替全局扫描。  

---  

## 反思  

- **第一反应**：看到棋盘只有 3×3，直接想把整个棋盘画出来、逐行检查。  
- **最容易踩的坑**：  
  - **对角线的判断**：要记得两条对角线的坐标条件，主对角线是 `row == col`，副对角线是 `row + col == 2`（因为索引从 0 开始）。  
  - **玩家标记**：如果使用 `1`、`-1` 记分，忘记在判断胜负时取绝对值会导致错误。  
  - **返回值顺序**：在有玩家已经赢的情况下，仍然要继续遍历剩余的步数会覆盖结果，正确做法是**一旦发现胜者立刻返回**。  
- **下次遇到同类题**：第一步先**思考是否可以用计数器或哈希表增量记录状态**，而不是每次都全盘扫描。这样往往能把时间从 “遍历所有组合” 降到 “每一步 O(1)”。