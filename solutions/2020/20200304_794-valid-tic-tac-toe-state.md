# #794. **有效的井字棋局面** / Valid Tic-Tac-Toe State

> 难度：中等 · 标签：Array、Matrix · [LeetCode 链接](https://leetcode.com/problems/valid-tic-tac-toe-state/)

---

## 题目（英文原版）

**Description**

Given a Tic-Tac-Toe board as a string array board, return true if and only if it is possible to reach this board position during the course of a valid tic-tac-toe game.
The board is a 3 x 3 array that consists of characters ' ', 'X', and 'O'. The ' ' character represents an empty square.
Here are the rules of Tic-Tac-Toe:

**Examples**

**Example 1:**

```
Input: board = ["O  ","   ","   "]
Output: false
Explanation: The first player always plays "X".
```

**Example 2:**

```
Input: board = ["XOX"," X ","   "]
Output: false
Explanation: Players take turns making moves.
```

**Example 3:**

```
Input: board = ["XOX","O O","XOX"]
Output: true
```

**Constraints**

- board.length == 3
- board[i].length == 3
- board[i][j] is either 'X', 'O', or ' '.

---

## 题目（中文翻译）

给定一个表示井字棋 (Tic‑Tac‑Toe) 盘面的字符串数组 `board`，仅当该盘面能够在一次合法的井字棋游戏过程中出现时，返回 `true`，否则返回 `false`。

棋盘是一个 3×3 的二维数组，由字符 `' '`、`'X'` 和 `'O'` 组成。字符 `' '` 表示该格子为空。

**井字棋的规则**  
1. 游戏由两名玩家交替进行，先手玩家只能下 `'X'`，后手玩家只能下 `'O'`。  
2. 每一次落子只能放在空格 `' '` 上。  
3. 当某一玩家在任意一行、任意一列或两条对角线上形成连续的三个相同符号时，该玩家获胜，游戏立即结束。  
4. 若棋盘全部填满且没有玩家获胜，则为平局，游戏结束。  
5. 游戏结束后不再继续落子。

---

### 示例

**示例 1**  
```text
Input: board = ["O  ","   ","   "]
Output: false
Explanation: 先手玩家必须下 "X"，因此该局面不可能出现。
```

**示例 2**  
```text
Input: board = ["XOX"," X ","   "]
Output: false
Explanation: 玩家必须轮流落子，当前盘面出现了两次连续的 "X" 落子而没有对应的 "O" 落子，违反了轮流规则。
```

**示例 3**  
```text
Input: board = ["XOX","O O","XOX"]
Output: true
Explanation: 该盘面符合所有规则，可在合法的游戏过程中得到。
```

---

### 约束条件

- `board.length == 3`
- `board[i].length == 3`
- `board[i][j]` 只能是 `'X'`、`'O'` 或 `' '`。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把井字棋的**所有合法走法**全部枚举出来，然后看看目标棋盘 `board` 是否出现在这些合法走法之中。  

- **数据结构**：我们把棋盘当成一个 3×3 的二维数组（列表的列表），每一步都把一个空格 `' '` 换成当前玩家的棋子 `'X'` 或 `'O'`。  
- **类比**：把枚举过程想象成“遍历字典”，字典的 **key** 是一种走法（即每一步的棋子放置位置），**value** 是对应的棋盘状态。只要在这本“字典”里能找到和 `board` 完全相同的一页，就说明这局面是合法的。  
- **为什么正确**：因为我们把**所有**可能的合法走法（包括每一步的先后顺序）都列举出来了，只要 `board` 能在其中出现，就必然是一次合法游戏的结果。反之，如果没有出现，则说明该局面不可能出现。  

**实现方式**：使用深度优先搜索（DFS）或回溯法，递归地把空格填上 `'X'` 或 `'O'`，并在每一步检查是否已经有人赢了——如果已经有胜者，则不再继续往下走（因为游戏一旦结束就不再继续下子）。  

#### 代码（Python）  

```python
from typing import List

def validTicTacToe_bruteforce(board: List[str]) -> bool:
    # 把输入的字符串数组转成二维列表，方便修改
    target = [list(row) for row in board]

    # 统计所有合法局面的集合（使用字符串形式存储，方便比较）
    reachable = set()

    def win(b, player):
        """检查 player 是否已经形成了三子连线"""
        lines = [
            # 行
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            # 列
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            # 对角线
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)],
        ]
        return any(all(b[x][y] == player for x, y in line) for line in lines)

    def dfs(b, turn):
        """
        b   : 当前棋盘（二维列表）
        turn: 当前轮到的玩家，'X' 或 'O'
        """
        # 把当前局面记下来（转成字符串，方便放进 set）
        reachable.add(''.join(''.join(row) for row in b))

        # 如果已经有人赢了，就不要继续走子
        if win(b, 'X') or win(b, 'O'):
            return

        # 遍历所有空格，尝试落子
        for i in range(3):
            for j in range(3):
                if b[i][j] == ' ':
                    b[i][j] = turn               # 落子
                    dfs(b, 'O' if turn == 'X' else 'X')  # 换手继续搜索
                    b[i][j] = ' '               # 恢复现场（回溯）

    # 从空棋盘开始搜索，先手一定是 X
    empty_board = [[' ']*3 for _ in range(3)]
    dfs(empty_board, 'X')

    # 把目标棋盘转成同样的字符串形式，检查是否在 reachable 集合里
    target_str = ''.join(''.join(row) for row in target)
    return target_str in reachable
```

> 关键点注释已写在代码里，直接运行即可得到结果。  

#### 复杂度  

- **时间复杂度**：  
  - 井字棋最多 9 步，所有合法走法的数量上限是 `9! = 362880`（每一步都可以在剩下的格子里随意落子）。在每个递归节点我们只做 O(1) 的检查（是否有人赢），所以整体时间复杂度是 **O(9!)**，即 **大约 36 万次操作**。对电脑来说仍然可以接受，但显然不是最优的。  
- **空间复杂度**：  
  - 递归深度最多 9 层，另外要保存所有已经遍历过的局面（最坏情况下也不超过 9!），因此空间复杂度是 **O(9!)**（主要是 `reachable` 集合的大小）。  

> 用大白话说，暴力解相当于把所有可能的游戏录像都录下来，再在录像库里找一遍——虽然能找，但浪费很多磁盘和时间。  

---  

### 2. 最优解  

#### 思路  

从暴力解我们可以看到，**真正需要检查的只有局面的合法性，而不必枚举所有走法**。我们只要依据井字棋的规则，用数学关系直接判断即可。  

1. **先手一定是 X**，所以 X 的落子数要么等于 O 的落子数，要么比 O 多 1。  
2. **如果已经有玩家获胜**，游戏应该立即结束，后面的子不再出现。  
   - 若 X 赢了，则 X 必须比 O 多一步（因为 X 必须是最后落子的那一步）。  
   - 若 O 赢了，则 X 与 O 的落子数必须相等（因为 O 是最后落子的那一步）。  
3. **不可能同时出现 X 和 O 都赢的情况**，因为游戏一旦有人赢就会立即停止。  

只要这三条判断全部通过，局面就是合法的。  

**核心概念：**  
- **计数**（Count）：统计棋盘上 X 与 O 的数量。  
- **胜利检测**（Win Check）：检查每一行、每一列、两条对角线是否全部由同一个玩家占据。可以把每条线看成“一组钥匙”，如果同一玩家拥有整组钥匙，就算赢了。  

#### 代码（Python）  

```python
from typing import List

def validTicTacToe(board: List[str]) -> bool:
    """
    判断给定的 3x3 井字棋局面是否可能在一次合法游戏中出现。
    """
    # 1️⃣ 统计 X 和 O 的个数
    x_cnt = sum(row.count('X') for row in board)
    o_cnt = sum(row.count('O') for row in board)

    # 2️⃣ 先手必须是 X，且 X 不能比 O 多超过 1
    if not (x_cnt == o_cnt or x_cnt == o_cnt + 1):
        return False

    # 3️⃣ 定义一个函数，用来判断 player 是否已经赢了
    def win(player: str) -> bool:
        lines = [
            # 行
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            # 列
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            # 对角线
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)],
        ]
        # 只要有一条线全部是 player，就算赢了
        return any(all(board[x][y] == player for x, y in line) for line in lines)

    x_win = win('X')
    o_win = win('O')

    # 4️⃣ 同时出现 X 赢和 O 赢的情况不合法
    if x_win and o_win:
        return False

    # 5️⃣ 若 X 赢了，必须是 X 多一步（因为 X 最后落子）
    if x_win and x_cnt != o_cnt + 1:
        return False

    # 6️⃣ 若 O 赢了，必须是 X 与 O 落子数相等（因为 O 最后落子）
    if o_win and x_cnt != o_cnt:
        return False

    # 通过所有检测，说明局面合法
    return True
```

> 代码中每一步都配有中文注释，帮助你快速对应到思路的每个要点。  

#### 复杂度  

- **时间复杂度**：  
  - 统计字符数量遍历一次棋盘：O(9) → 实际上是常数时间。  
  - 检查八条可能的赢法，每条最多检查 3 格，同样是 O(1)。  
  - 所以整体时间复杂度是 **O(1)**，即“常数时间”，与棋盘大小无关。  
- **空间复杂度**：  
  - 只用了几个整数和布尔变量，空间占用不随输入变化，故为 **O(1)**。  

> 与暴力解相比，最优解把“遍历全部录像”变成了“一眼看穿局面的合法性”，快得多、占内存也少得多。  

---  

## 心得  

- **核心技巧**：**计数 + 胜利检测**。通过对 X、O 的落子数做约束，再结合谁先赢的规则，就能在常数时间内判断合法性。  
- **适用的题型**：  
  1. 任何需要判断棋类游戏合法性的题目（如 4×4 井字棋、五子棋的合法状态）。  
  2. 类似 “检查数独是否可能” 这类 **约束满足**（Constraint Satisfaction）问题。  
  3. “判断字符串是否可以通过合法的括号匹配得到”等 **计数 + 状态** 的判断题。  
- **一句话总结解题钥匙**：**先用计数把“谁该先走、谁该后走”锁定，再用胜负规则验证是否符合先后顺序**。  

---  

## 反思  

- **第一反应**：看到“是否可能出现”，本能想到“枚举所有可能的走法”。这在思考上是直观的，但显然不够高效。  
- **最容易踩的坑**：  
  - 忽略 **两个玩家同时赢** 的非法情况。  
  - 把 **X 必须先手** 的规则忘记，只检查了子数差。  
  - 对空格 `' '` 的处理不当，导致计数错误。  
- **下次遇到同类题**，第一步应该先 **列出游戏的基本规则（先后手、胜负结束条件）**，再 **用数学关系（计数、约束）把规则转化为代码判断**，而不是直接尝试枚举。