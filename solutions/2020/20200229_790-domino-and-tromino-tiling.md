# #790. 多米诺骨牌与三连块平铺 / Domino and Tromino Tiling

> 难度：中等 · 标签：Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/domino-and-tromino-tiling/)

---

## 题目（英文原版）

**Description**

You have two types of tiles: a 2 x 1 domino shape and a tromino shape. You may rotate these shapes.
Given an integer n, return the number of ways to tile an 2 x n board. Since the answer may be very large, return it modulo 109 + 7.
In a tiling, every square must be covered by a tile. Two tilings are different if and only if there are two 4-directionally adjacent cells on the board such that exactly one of the tilings has both squares occupied by a tile.

**Examples**

**Example 1:**

```
Input: n = 3
Output: 5
Explanation: The five different ways are shown above.
```

**Example 2:**

```
Input: n = 1
Output: 1
```

**Constraints**

- 1 <= n <= 1000

---

## 题目（中文翻译）

你有两种形状的砖块：一种是 2 × 1 的多米诺骨牌（domino）形状，另一种是三连块（tromino）形状。你可以对这些形状进行旋转。  
给定整数 `n`，返回将一个 2 × n 的棋盘完全平铺的方案数。由于答案可能非常大，请返回 **模 10^9 + 7** 的结果。  

在一次平铺中，棋盘的每一个格子都必须被砖块覆盖。若且仅若存在两个在上下左右四个方向相邻的格子，使得在两个平铺方案中恰好有一个方案把这两个格子同时被同一块砖覆盖，则这两种平铺方案被认为是不同的。

**示例**

**示例 1**  
输入: `n = 3`  
输出: `5`  
解释: 如上图所示，共有五种不同的平铺方式。

**示例 2**  
输入: `n = 1`  
输出: `1`

**约束条件**

- `1 <= n <= 1000`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的摆放方式**，把棋盘从左到右、从上到下依次填满。  
- **使用的数据结构**：我们可以把 2×n 的棋盘抽象成一个长度为 `2*n` 的一维数组 `board`，每个位置保存 `0/1`（0 表示空，1 表示已被瓦片覆盖）。这类似于在纸上画格子，逐格检查是否已经被填好。  
- **搜索方式**：从左上角开始，找到第一个仍然是 `0` 的格子，尝试把四种合法的瓦片（两种方向的 domino、两种方向的 tromino）放进去，只要放得下且不与已经放好的瓦片重叠，就递归继续往后填。递归结束的条件是所有格子都被填满，此时计数 +1。  

这种做法一定能得到正确答案，因为它遍历了**所有可能的组合**，只要一种合法的组合能够完整覆盖棋盘，就会被计入。

> **为什么会慢**  
> 每放一块瓦片，后面的选择会指数级增加。比如在第 `i` 列时，可能有 2~4 种放法，而每一种放法又会产生新的分支。总体上相当于 **2 的 n 次方**（甚至更大）种情况。  

#### 代码（Python）

```python
MOD = 10**9 + 7

def numTilings_bruteforce(n: int) -> int:
    # 2 行 n 列的棋盘，用一维数组表示（行主序）
    board = [0] * (2 * n)          # 0 表示空，1 表示已被覆盖

    def index_to_pos(idx):
        """把一维下标转成 (row, col)"""
        return idx // n, idx % n   # row: 0 或 1

    def find_first_empty():
        """返回第一个为空的格子下标，若全部填满返回 -1"""
        for i, v in enumerate(board):
            if v == 0:
                return i
        return -1

    def set_cells(cells, val):
        """一次性把若干格子设为 val（0/1）"""
        for r, c in cells:
            board[r * n + c] = val

    def can_place(cells):
        """检查这些格子是否都在棋盘内部且当前未被占用"""
        for r, c in cells:
            if not (0 <= r < 2 and 0 <= c < n):
                return False
            if board[r * n + c] == 1:
                return False
        return True

    def dfs() -> int:
        pos = find_first_empty()
        if pos == -1:                 # 全部填满
            return 1
        r, c = index_to_pos(pos)

        total = 0

        # 1️⃣ 竖着放一个 2×1 domino
        cells = [(r, c), (1 - r, c)]          # 同一列的上下两个格子
        if can_place(cells):
            set_cells(cells, 1)
            total += dfs()
            set_cells(cells, 0)

        # 2️⃣ 横着放一个 2×1 domino（只能在上面一行或下面一行）
        cells = [(r, c), (r, c + 1)]
        if can_place(cells):
            set_cells(cells, 1)
            total += dfs()
            set_cells(cells, 0)

        # 3️⃣ 放一种 tromino：形状 “L”，左上、左下、右上
        cells = [(r, c), (1 - r, c), (r, c + 1)]
        if can_place(cells):
            set_cells(cells, 1)
            total += dfs()
            set_cells(cells, 0)

        # 4️⃣ 放另一种 tromino：形状 “Γ”，左上、右上、右下
        cells = [(r, c), (r, c + 1), (1 - r, c + 1)]
        if can_place(cells):
            set_cells(cells, 1)
            total += dfs()
            set_cells(cells, 0)

        return total % MOD

    return dfs()
```

> **代码说明**  
> - `board` 用一维数组保存 2×n 棋盘的占用状态，类似于一本词典里查找单词是否出现（下标是单词，值是是否已标记）。  
> - `dfs` 是深度优先搜索的递归函数，每一次尝试把一种合法的瓦片放到当前第一个空格子上，然后继续递归。  
> - 为了防止递归层数太深导致栈溢出，实际使用时 `n` 只能到 10 左右（因为时间已经爆炸）。

#### 复杂度  

- **时间复杂度**：约为 **O(2ⁿ)**（指数级），因为每一步都有常数个分支，深度为 `n`，总的搜索树大小呈指数增长。用大白话说，就是“随着 n 增大，所需的时间会像翻倍一样疯狂增长”。  
- **空间复杂度**：O(n)——递归栈的深度最多是 `n`，再加上 `board` 长度 `2n`，都是线性空间。

---

### 2. 最优解  

#### 思路  

从暴力解我们可以看到，**每次只关注最左侧未填的列**，这说明我们可以用**动态规划（DP）**把问题拆成子问题。  

> **瓶颈**：暴力解在每一步都要尝试所有瓦片并递归，导致大量重复计算。我们需要把“已经算好的”状态保存下来，避免重复。

---

#### 2.1 状态定义  

我们把棋盘从左到右划分为若干段，只关注**最右侧已经完全填好的列**。  
- `dp[i]`：**恰好填满**前 `i` 列（即 2×i 的区域）的合法摆放方式数。这里的 “完全填满” 指两行都没有缺口。  
- `p[i]`（或记作 `extra[i]`）：**恰好填满**前 `i` 列，但**多出**一个形如 “半列缺口” 的状态。具体来说，左上角已经被覆盖，而左下角还空着（或相反），这相当于在第 `i` 列留下了一个 “凹口”。  

> **类比**：想象你在铺地砖，`dp[i]` 表示前 `i` 米的地面已经铺得平整；`p[i]` 表示前 `i` 米已经铺好，但在第 `i` 米的右边留下了一个“小坑”，后面必须用特殊的砖块来填平。

---

#### 2.2 转移方程  

1. **完全填满的情况 `dp[i]`**  
   - **方式 A**：在第 `i‑1` 列已经完全填好 (`dp[i‑1]`)，再竖着放一个 domino → `dp[i‑1]` 种。  
   - **方式 B**：在第 `i‑2` 列已经完全填好 (`dp[i‑2]`)，再水平放两个 domino → `dp[i‑2]` 种。  
   - **方式 C**：在第 `i‑2` 列已经完全填好 (`dp[i‑2]`)，再放一个 tromino（两种方向），每种都会在第 `i‑1` 列留下一个凹口 → 2 × `dp[i‑2]` 种。  
   - **方式 D**：在第 `i‑1` 列已经出现凹口 (`p[i‑1]`)，再放一个特定的 tromino 把凹口填平 → `p[i‑1]` 种。  

   综合得到  
   \[
   dp[i] = dp[i-1] + dp[i-2] + 2\cdot dp[i-2] + p[i-1]
        = dp[i-1] + dp[i-2] + 2\cdot dp[i-2] + p[i-1]
   \]

2. **凹口状态 `p[i]`**（只留下左上或左下一个格子空）  
   - **方式 A**：在 `dp[i-1]` 完全填好的基础上，放一个 “L” 形的 tromino，使第 `i` 列留下凹口 → `dp[i-1]` 种。  
   - **方式 B**：在 `p[i-1]` 已经有凹口的基础上，再放一个竖着的 domino 把凹口向右延伸（相当于把凹口“移动”到第 `i` 列） → `p[i-1]` 种。  

   因此  
   \[
   p[i] = dp[i-1] + p[i-1]
   \]

把两式合并、消除 `p[i]`，可以得到更简洁的递推：

\[
\begin{aligned}
p[i] &= dp[i-1] + p[i-1] \\
dp[i] &= dp[i-1] + dp[i-2] + 2\cdot dp[i-2] + p[i-1] \\
      &= dp[i-1] + dp[i-2] + 2\cdot dp[i-2] + (p[i] - dp[i-1]) \\
      &= dp[i-1] + dp[i-2] + 2\cdot dp[i-2] + p[i] - dp[i-1] \\
      &= dp[i-2] + 2\cdot dp[i-2] + p[i] \\
      &= 2\cdot dp[i-1] + dp[i-3] \quad (\text{经过代数化简})
\end{aligned}
\]

最终得到 **最常用的单数组递推**（只需要 `dp`）：

\[
\boxed{dp[i] = (2\cdot dp[i-1] + dp[i-3]) \bmod M}\quad (i\ge 3)
\]

其中 `M = 10^9+7` 为取模常数。

> **为什么是 2·dp[i‑1] + dp[i‑3]**  
> - `2·dp[i‑1]`：在已经填满前 `i‑1` 列的基础上，**可以**（1）在第 `i‑1` 列竖着放一个 domino；（2）在第 `i‑1` 列放一个 tromino，使第 `i` 列留下凹口，然后再用另一块 tromino 把凹口填平——这两种情况共 `2·dp[i‑1]` 种。  
> - `dp[i‑3]`：前 `i‑3` 列完全填好后，**一次性**放三个 tromino（两种对称形）恰好覆盖第 `i‑2`、`i‑1`、`i` 三列，这里只剩下唯一的 “三块 L 形” 组合，故加上 `dp[i‑3]`。

---

#### 2.3 初始化  

- `dp[0] = 1`：空棋盘算一种合法方式。  
- `dp[1] = 1`：只能放一块竖着的 domino。  
- `dp[2] = 2`：两种方式：两个竖着的 domino 或两个水平的 domino。  

有了这三个基准，递推公式即可算到 `n`（最多 1000）。

---

#### 代码（Python）

```python
MOD = 10**9 + 7

def numTilings(n: int) -> int:
    """
    动态规划 O(n) 时间、O(1) 额外空间
    dp[i] = (2*dp[i-1] + dp[i-3]) % MOD   (i >= 3)
    """
    if n == 0:
        return 1
    if n == 1:
        return 1
    if n == 2:
        return 2

    # 只保留最近的三个状态，节省空间
    dp0, dp1, dp2 = 1, 1, 2   # 分别对应 dp[i-3], dp[i-2], dp[i-1]

    for i in range(3, n + 1):
        cur = (2 * dp2 + dp0) % MOD   # dp[i] = 2*dp[i-1] + dp[i-3]
        # 向前滚动窗口
        dp0, dp1, dp2 = dp1, dp2, cur

    return dp2
```

> **代码注释**  
> - `dp0, dp1, dp2` 分别保存 `dp[i-3]、dp[i-2]、dp[i-1]`，每次循环算出 `dp[i]` 后左移一次，相当于只用了 **常数** 的额外空间。  
> - `cur = (2 * dp2 + dp0) % MOD` 正是公式 `dp[i] = 2·dp[i‑1] + dp[i‑3]`，取模防止整数爆炸。  

---

#### 复杂度  

- **时间复杂度**：**O(n)**。我们只遍历一次 `1 … n`，每一步做常数次算术运算。相较于暴力的指数级，这就像“走直路”一样快。  
- **空间复杂度**：**O(1)**（常数）。只保存最近的三个 dp 值，不随 `n` 增长而增长。  

> 与暴力解相比，时间从“指数级”降到“线性级”，空间也从 `O(n)`（递归栈）降到 `O(1)`，在实际使用中可以轻松处理 `n = 1000` 甚至更大的输入。

---

## 心得  

- **核心技巧**：把“是否有缺口”抽象成状态（完全填满 vs. 留下一个凹口），利用**状态转移**把局部选择合并成全局计数。  
- **适用的题型**  
  1. **其他形状的平铺**（如 2×n 的 domino、Tromino 以及 L‑shaped tile 等）。  
  2. **斜坡/缺口 DP**（如 LeetCode 931 “Minimum Falling Path Sum” 中的“缺口”状态）。  
  3. **棋盘覆盖类递推**（如 LeetCode 322 “Coin Change” 的“可选/不可选”状态转移）。  
- **一句话总结解题钥匙**：**把“局部缺口”当作独立状态记下来，利用递推把所有可能的补齐方式一次性算完**。

---

## 反思  

- **第一反应**：看到 domino 与 tromino，立刻想到“递归枚举”。这在没有 DP 思路时是自然的。  
- **最容易踩的坑**  
  1. **忘记取模**：答案会非常大，必须在每一步 `% MOD`。  
  2. **边界条件**：`n < 3` 时递推公式不适用，需要手动返回 `dp[0]、dp[1]、dp[2]`。  
  3. **状态遗漏**：只考虑完全填满会导致错误；必须显式维护“凹口”状态（或等价的额外变量）。  
- **下次类似题的第一步**：先**画出前几列的所有合法铺法**，观察是否出现“缺口”或“剩余形状”，并把这些形状当作 DP 的状态来记录。这样可以快速从暴力到状态转移的桥梁。