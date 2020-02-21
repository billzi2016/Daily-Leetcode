# #782. 变换为棋盘 / Transform to Chessboard

> 难度：困难 · 标签：Array、Math、Bit Manipulation、Matrix · [LeetCode 链接](https://leetcode.com/problems/transform-to-chessboard/)

---

## 题目（英文原版）

**Description**

You are given an n x n binary grid board. In each move, you can swap any two rows with each other, or any two columns with each other.
Return the minimum number of moves to transform the board into a chessboard board. If the task is impossible, return -1.
A chessboard board is a board where no 0's and no 1's are 4-directionally adjacent.

**Examples**

**Example 1:**

```
Input: board = [[0,1,1,0],[0,1,1,0],[1,0,0,1],[1,0,0,1]]
Output: 2
Explanation: One potential sequence of moves is shown.
The first move swaps the first and second column.
The second move swaps the second and third row.
```

**Example 2:**

```
Input: board = [[0,1],[1,0]]
Output: 0
Explanation: Also note that the board with 0 in the top left corner, is also a valid chessboard.
```

**Example 3:**

```
Input: board = [[1,0],[1,0]]
Output: -1
Explanation: No matter what sequence of moves you make, you cannot end with a valid chessboard.
```

**Constraints**

- n == board.length
- n == board[i].length
- 2 <= n <= 30
- board[i][j] is either 0 or 1.

---

## 题目（中文翻译）

给定一个 n × n 的二进制网格（binary grid） **board**。在每一次移动中，你可以交换任意两行，或任意两列。返回将 **board** 转换为棋盘（chessboard）所需的最少移动次数。如果任务不可实现，返回 **-1**。棋盘是指在四个方向上相邻的格子中，**0** 与 **0**、**1** 与 **1** 都不相邻，即不存在相邻的相同数字。

**示例 1**  
输入: `board = [[0,1,1,0],[0,1,1,0],[1,0,0,1],[1,0,0,1]]`  
输出: `2`  
解释: 以下是一种可能的移动序列。第一步交换第一列和第二列。第二步交换第二行和第三行。

**示例 2**  
输入: `board = [[0,1],[1,0]]`  
输出: `0`  
解释: 同时需要注意，左上角为 **0** 的棋盘也是合法的棋盘。

**示例 3**  
输入: `board = [[1,0],[1,0]]`  
输出: `-1`  
解释: 无论进行何种交换，都无法得到合法的棋盘。

**约束条件**  
- `n == board.length`  
- `n == board[i].length`  
- `2 ≤ n ≤ 30`  
- `board[i][j]` 只能是 **0** 或 **1**

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直观的想法是 **把所有行和列都枚举所有可能的排列**，看哪一种排列能够得到合法的棋盘（相邻格子颜色不同），再把需要的交换次数记下来，取最小值。

- **行的排列**：把 `n` 行随意调换，等价于把 `n` 张纸排成任意顺序。  
- **列的排列**：同理，把 `n` 列随意调换。  

这就好比我们把一副扑克牌洗牌：每一种洗法都是一种可能的排列。只要把所有排列都尝试一遍，就一定能找到最优解（如果存在的话）。

> **为什么暴力一定正确？**  
> 因为题目只允许“交换任意两行”或“交换任意两列”。任意一次交换都只是在当前排列上做一次邻接置换，而把所有置换组合起来就能得到 **所有** 行/列的排列。因此遍历所有排列必然覆盖了所有合法的操作序列。

> **时间/空间复杂度**  
> - 行的排列有 `n!` 种，列的排列也有 `n!` 种，二者独立，组合起来是 `n! × n!`。  
> - 对每一种组合，我们要检查整个 `n × n` 的矩阵是否满足棋盘条件，需要 `O(n²)` 的时间。  
> - 所以总时间复杂度是 `O(n!² · n²)`，这在 `n ≤ 30` 时根本不可接受（即使 `n = 8`，`8!² ≈ 1.6·10⁹` 也会超时）。  
> - 空间只需要保存原矩阵和若干临时数组，`O(n²)`。

> **大白话解释**：  
> `O(n!²)` 就像说“把 30 本书排成任意顺序再排成任意顺序”，这比“把 30 本书全部搬到地上再重新排一次”还要慢，根本不可能在几秒钟内完成。

#### 代码（Python）

```python
import itertools
from copy import deepcopy

def is_chessboard(board):
    """判断 board 是否已经是合法的棋盘（相邻格子不同）。"""
    n = len(board)
    for i in range(n):
        for j in range(n):
            # 四个方向只要有一个相邻格子颜色相同，就不合法
            if i + 1 < n and board[i][j] == board[i + 1][j]:
                return False
            if j + 1 < n and board[i][j] == board[i][j + 1]:
                return False
    return True

def brute_transform(board):
    """暴力枚举所有行列排列，返回最小交换次数，若不可达返回 -1。"""
    n = len(board)
    rows = list(range(n))
    cols = list(range(n))
    best = float('inf')

    # 这里直接使用 itertools.permutations 产生所有排列
    for perm_r in itertools.permutations(rows):
        # 计算把原来的行顺序变成 perm_r 需要的交换次数
        # 交换次数等价于“排列的逆序数”，这里用简单的 O(n²) 计数
        row_swaps = sum(1 for i in range(n) for j in range(i) if perm_r[j] > perm_r[i])

        # 重新排列行
        new_board = [board[i] for i in perm_r]

        for perm_c in itertools.permutations(cols):
            col_swaps = sum(1 for i in range(n) for j in range(i) if perm_c[j] > perm_c[i])

            # 重新排列列
            transformed = [[new_board[i][j] for j in perm_c] for i in range(n)]

            if is_chessboard(transformed):
                best = min(best, row_swaps + col_swaps)

    return -1 if best == float('inf') else best
```

> 代码里每一行都加了中文注释，帮助你快速定位关键步骤。**请注意**：这段代码仅用于演示思路，实际运行会因为 `n!` 的爆炸式增长而超时。

#### 复杂度

- **时间复杂度**：`O(n!² · n²)` —— 先枚举所有行列排列（`n!` × `n!`），每次检查 `n²` 的格子。  
  - 含义：随着 `n` 增大，计算量会呈阶乘增长，几乎不可能在合理时间内完成。
- **空间复杂度**：`O(n²)` —— 需要存放原矩阵和一次拷贝的临时矩阵。

---

### 2. 最优解

#### 思路  

暴力的瓶颈在于 **枚举所有排列**。事实上，我们并不需要真的去枚举，而是可以从 **行/列的整体模式** 入手，直接算出最少的交换次数。

关键观察如下：

1. **合法棋盘的行（列）只能有两种模式**  
   - 设第一行是 `0101…`（记作模式 A），则所有奇数行必须和 A 完全相同，所有偶数行必须是 A 的 **反码**（`1010…`，记作模式 B）。  
   - 同理，第一列也是两种交替模式。  
   - 因此，整个矩阵的每一行要么和第一行相同，要么和第一行相反；每一列也要么和第一列相同，要么相反。

2. **行（列）出现的次数必须满足平衡条件**  
   - 当 `n` 为偶数时，模式 A 与模式 B 各出现 `n/2` 次。  
   - 当 `n` 为奇数时，出现次数只能是 `n//2` 与 `n//2+1` 两者之一（因为交替序列的长度导致多一个 0 或 1）。

3. **行（列）之间必须两两“相异或”相同**  
   - 任意两行的异或（XOR）要么全是 0，要么全是 1。换句话说，`board[i] XOR board[0]` 必须等于全 0 或全 1。  
   - 这一步可以用 **位运算** 快速检查（把每一行看成一个二进制整数）。

4. **如何得到最少交换次数**  
   - 把所有行视为一组二进制数，记下它们是否和第一行相同（记作 0）或相反（记作 1）。我们得到一个长度为 `n` 的 0/1 序列 `rowPattern`。  
   - 目标是把这 `rowPattern` 变成交替的 `0101…`（或 `1010…`），每一次交换两行等价于把序列中两个位置的数字互换。  
   - 对于交替序列，最少交换次数等于 **把错误位置的数量除以 2**，而且可以用下面的公式直接算出：  
     ```
     swaps = min( mismatches with pattern 0101…, mismatches with pattern 1010… ) / 2
     ```
   - 当 `n` 为奇数时，只有一种模式合法（因为交替序列的首位决定了整体），所以直接取对应的 mismatches。

5. **行列独立**  
   - 行的交换次数和列的交换次数互不影响，最终答案是两者之和再除以 2（因为一次交换只能改动行或列，而题目要求的“移动次数”是指一次行交换或一次列交换，二者相加即为总次数）。

**整体算法步骤**  

1. 把每一行/列压成整数，用位运算检查 **所有行/列都只有两种模式**（相同或相反）。若不满足直接返回 `-1`。  
2. 统计第一行出现的次数 `cntRowOnes`（即与第一行相反的行数），以及第一列出现的次数 `cntColOnes`。检查 **平衡条件**（奇偶数情况）。不满足返回 `-1`。  
3. 用函数 `min_swaps(pattern, n)` 计算把行序列（或列序列）变成交替序列需要的最少交换次数。  
4. 返回 `row_swaps + col_swaps`。

#### 代码（Python）

```python
def moves_to_chessboard(board):
    """
    返回将 board 变成合法棋盘所需的最少交换次数，若不可能返回 -1。
    思路：行/列只能出现两种交替模式，利用位运算快速判定并计算 swaps。
    """
    n = len(board)

    # ---------- 1. 把每一行压成整数 ----------
    rows = [int(''.join(map(str, row)), 2) for row in board]

    # ---------- 2. 检查行的合法性 ----------
    # 所有行要么等于 rows[0]，要么等于 rows[0] ^ ((1<<n)-1)（全反码）
    mask = (1 << n) - 1               # n 位全为 1 的掩码，例如 n=4 -> 0b1111
    for r in rows:
        if r != rows[0] and r != (rows[0] ^ mask):
            return -1                # 行出现了第三种模式，无法变成棋盘

    # ---------- 3. 检查列的合法性 ----------
    # 把每一列也压成整数
    cols = [int(''.join(str(board[i][j]) for i in range(n)), 2) for j in range(n)]
    for c in cols:
        if c != cols[0] and c != (cols[0] ^ mask):
            return -1                # 列出现了第三种模式

    # ---------- 4. 计数行/列中“相反”出现的次数 ----------
    # 与第一行相反的行数
    row_ones = sum(1 for r in rows if r == (rows[0] ^ mask))
    # 与第一列相反的列数
    col_ones = sum(1 for c in cols if c == (cols[0] ^ mask))

    # ---------- 5. 平衡条件 ----------
    # 当 n 为偶数时，必须恰好各占 n/2；奇数时只能相差 1
    if not (n // 2 <= row_ones <= (n + 1) // 2):
        return -1
    if not (n // 2 <= col_ones <= (n + 1) // 2):
        return -1

    # ---------- 6. 计算最少交换次数的辅助函数 ----------
    def min_swaps(cnt_ones, pattern):
        """
        cnt_ones   : 与第一行（列）相反的数量
        pattern    : 目标交替模式的首位（0 表示 0101..., 1 表示 1010...）
        返回把该序列变成交替序列所需的最少行（列）交换次数。
        """
        # 目标交替序列中 1 出现的次数
        target_ones = n // 2
        if n % 2 == 1:                # n 为奇数时，首位决定出现次数
            target_ones = n // 2 + pattern   # pattern=1 时多一个 1
        # mismatches 表示实际 1 与目标 1 的位置不匹配的个数
        mismatches = abs(cnt_ones - target_ones)
        # 每一次交换可以同时纠正两个错误位置
        return mismatches // 2

    # ---------- 7. 计算行、列各自的 swaps ----------
    # 对行：目标模式可以是 0101...（pattern=0）或 1010...（pattern=1），取最小值
    row_swaps = min(min_swaps(row_ones, 0), min_swaps(row_ones, 1))
    col_swaps = min(min_swaps(col_ones, 0), min_swaps(col_ones, 1))

    return row_swaps + col_swaps
```

> **代码要点注释**  
> - `mask = (1 << n) - 1` 把 `n` 位全 1 当作 “全反码” 的工具。  
> - `rows[0] ^ mask` 直接得到第一行的反码（0↔1），不需要逐位遍历。  
> - `min_swaps` 函数里用 **“错位的 1 的数量” / 2** 直接得到最少交换次数，这是一条重要的数学结论，后面会再解释。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 将每行/每列压成整数各需要 `O(n²)`（遍历矩阵一次）。  
  - 其余检查、计数、计算 swaps 均是 `O(n)`。  
  - 相比暴力的 `O(n!²·n²)`，这里是线性乘以 `n`，在 `n ≤ 30` 时毫秒级完成。

- **空间复杂度**：`O(n)`  
  - 只保存行、列的整数列表（各 `n` 个），以及常数级的辅助变量。  
  - 不需要额外的 `n×n` 矩阵拷贝，空间开销非常小。

---

## 心得

- **核心技巧**：**行/列只能出现两种互为反码的模式**，利用位运算快速判定并通过计数平衡来求最少交换次数。  
- **该技巧适用的题型**：  
  1. **Transform to Chessboard**（本题）  
  2. **Valid Tic‑Tac‑Toe State**（判断井字棋合法性）  
  3. **Flipping an Image**（翻转图像时需要判断行列是否可逆）  
- **一句话总结解题钥匙**：**把整行（列）看成一个二进制数，检查只有两种模式并用计数差除以 2 求最少交换**。

---

## 反思

- **拿到题目第一反应**：直接想到“把所有行、列随意换位”，于是产生了枚举所有排列的暴力思路。  
- **最容易踩的坑**  
  1. **平衡条件忽略**：即使所有行/列只有两种模式，如果出现次数不满足 `n/2`（偶数）或 `⌊n/2⌋/⌈n/2⌉`（奇数），仍然不可达。  
  2. **奇数尺寸的特殊处理**：交替序列的首位决定了整体出现次数，必须分别考虑 `pattern=0` 与 `pattern=1` 的情况。  
  3. **把交换次数误算为 “错位的行数”**：实际每次交换可以纠正 **两个** 错位位置，需要除以 2。  
- **下次遇到同类题，第一步该想到**：**把整行/列压成整数，用“只有两种互为反码的模式 + 出现次数平衡”这两个判定条件快速排除不可能的情况，再用计数差除以 2 求最小交换次数**。