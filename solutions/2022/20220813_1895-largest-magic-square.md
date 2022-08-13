# #1895. 最大魔方阵 / Largest Magic Square

> 难度：中等 · 标签：Array、Matrix、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/largest-magic-square/)

---

## 题目（英文原版）

**Description**

A k x k magic square is a k x k grid filled with integers such that every row sum, every column sum, and both diagonal sums are all equal. The integers in the magic square do not have to be distinct. Every 1 x 1 grid is trivially a magic square.
Given an m x n integer grid, return the size (i.e., the side length k) of the largest magic square that can be found within this grid.

**Examples**

**Example 1:**

```
Input: grid = [[7,1,4,5,6],[2,5,1,6,4],[1,5,4,3,2],[1,2,7,3,4]]
Output: 3
Explanation: The largest magic square has a size of 3.
Every row sum, column sum, and diagonal sum of this magic square is equal to 12.
- Row sums: 5+1+6 = 5+4+3 = 2+7+3 = 12
- Column sums: 5+5+2 = 1+4+7 = 6+3+3 = 12
- Diagonal sums: 5+4+3 = 6+4+2 = 12
```

**Example 2:**

```
Input: grid = [[5,1,3,1],[9,3,3,1],[1,3,3,8]]
Output: 2
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 50
- 1 <= grid[i][j] <= 106

---

## 题目（中文翻译）

一个 **k × k** 魔方阵（magic square）是一个 **k × k** 的整数网格（grid），其中每一行的行和（row sum）、每一列的列和（column sum）以及两条对角线的对角线和（diagonal sum）都相等。魔方阵中的整数不要求互不相同。任意 **1 × 1** 的网格显然是魔方阵。

给定一个 **m × n** 的整数网格（grid），返回可以在该网格中找到的最大魔方阵的大小（即其边长 **k**）。

---

### 示例

#### 示例 1
**Input:** `grid = [[7,1,4,5,6],[2,5,1,6,4],[1,5,4,3,2],[1,2,7,3,4]]`  
**Output:** `3`  
**Explanation:** 最大的魔方阵的边长为 **3**。该魔方阵的每一行和、每一列和以及两条对角线的和均为 **12**。  
- 行和：`5+1+6 = 5+4+3 = 2+7+3 = 12`  
- 列和：`5+5+2 = 1+4+7 = 6+3+3 = 12`  
- 对角线和：`5+4+3 = 6+4+2 = 12`

#### 示例 2
**Input:** `grid = [[5,1,3,1],[9,3,3,1],[1,3,3,8]]`  
**Output:** `2`

---

### 约束条件
- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 50`
- `1 <= grid[i][j] <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的子正方形都枚举出来，逐个检查它们是不是魔方阵**。  
具体步骤：

1. 枚举左上角 `(i, j)`（`0 ≤ i < m, 0 ≤ j < n`）。  
2. 再枚举正方形的边长 `k`（`1 ≤ k ≤ min(m-i, n-j)`）。  
3. 对这个 `k × k` 的子矩阵，逐行求和、逐列求和、两条对角线求和，判断它们是否相等。  

> **类比**：把 `k × k` 的子矩阵想成一块小地毯，逐行、逐列、两条斜线都要把地毯上的重量称一遍，看看是不是每次称的重量都相同。

为什么这个方法一定能得到答案？因为我们 **把所有可能的子正方形都检查了一遍**，只要有符合条件的，必然会被发现；如果没有，则答案只能是 `1`（每个 `1 × 1` 都是魔方阵）。

**时间复杂度**  
- 枚举左上角有 `m·n` 种。  
- 每个左上角最多可以尝试 `min(m, n)` 种边长。  
- 对每个具体的 `k × k`，要遍历 `k` 行、`k` 列、两条对角线，总共是 `O(k)`（因为行列的求和可以在一次遍历中完成）。  

于是总体复杂度是  

```
∑_{k=1}^{min(m,n)}  (m·n·k)  ≈ O(m·n·min(m,n)^2)
```

在最坏情况下（`m = n = 50`）大约是 `50·50·50² = 6.25·10⁶` 次基本操作，虽然还能跑完，但已经不是最优的做法了。

**空间复杂度**  
只用了常数级的额外变量，`O(1)`。

#### 代码（Python）

```python
def largestMagicSquare_bruteforce(grid):
    m, n = len(grid), len(grid[0])
    best = 1                     # 1×1 总是满足

    # 逐个左上角枚举
    for i in range(m):
        for j in range(n):
            # 枚举可能的边长（最多到矩阵边界）
            max_k = min(m - i, n - j)
            for k in range(2, max_k + 1):        # k=1 已经算在 best 里了
                # 计算第一行的和，作为“目标和”
                target = sum(grid[i][j:j + k])

                ok = True

                # 检查每一行的和
                for r in range(i, i + k):
                    if sum(grid[r][j:j + k]) != target:
                        ok = False
                        break
                if not ok:
                    continue

                # 检查每一列的和
                for c in range(j, j + k):
                    col_sum = sum(grid[r][c] for r in range(i, i + k))
                    if col_sum != target:
                        ok = False
                        break
                if not ok:
                    continue

                # 检查两条对角线的和
                diag1 = sum(grid[i + d][j + d] for d in range(k))
                diag2 = sum(grid[i + d][j + k - 1 - d] for d in range(k))
                if diag1 != target or diag2 != target:
                    ok = False

                if ok:
                    best = max(best, k)   # 记录最大的边长
    return best
```

> 代码里每一行前面的注释都是中文，帮助你快速定位关键操作。

#### 复杂度

- **时间复杂度**：`O(m·n·min(m,n)²)`  
  大白话：如果把矩阵看成 50×50 的棋盘，最坏情况下我们要检查每个起点的每一种可能大小，耗时大约是几百万次，虽然能跑通，但有更快的办法。

- **空间复杂度**：`O(1)`  
  只用了几个计数器和临时变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **每次检查子正方形都要重新遍历它的行、列、对角线**，导致时间随 `k` 的增大而线性增长。  
我们可以通过**前缀和**把“求区间和”这个操作降到 `O(1)`，从而把整体复杂度压到 `O(m·n·min(m,n))`。

**前缀和的类比**：想象你在一本账本里记下每一天累计的收入，想知道第 5 天到第 10 天的总收入，只需要 `累计到第10天 - 累计到第4天`，不必重新把这 6 天的每笔收入加一遍。矩阵的前缀和同理，只是把“天”换成了“格子”。

我们需要四种前缀和：

| 前缀和 | 含义 | 类比 |
|--------|------|------|
| `rowPref[i][j]` | 第 `i` 行前 `j` 列的累加和 | “第 i 行的账本” |
| `colPref[i][j]` | 第 `j` 列前 `i` 行的累加和 | “第 j 列的账本” |
| `diagPref[i][j]` | 主对角线（左上→右下）从左上角到 `(i,j)` 的累计和 | “左上→右下的斜线账本” |
| `antiPref[i][j]` | 副对角线（右上→左下）从右上角到 `(i,j)` 的累计和 | “右上→左下的斜线账本” |

有了这些表格，我们可以 **在常数时间** 内得到：

- 任意行的区间和：`rowPref[i][j+k] - rowPref[i][j]`
- 任意列的区间和：`colPref[i+k][j] - colPref[i][j]`
- 主对角线的区间和：`diagPref[i+k-1][j+k-1] - diagPref[i-1][j-1]`（注意边界）
- 副对角线的区间和：`antiPref[i+k-1][j] - antiPref[i-1][j+k]`

**整体算法**：

1. 先一次遍历矩阵，构造四个前缀和数组，时间 `O(m·n)`，空间同样 `O(m·n)`。  
2. 从最大的可能边长 `L = min(m,n)` 开始往下枚举（因为我们希望尽快找到最大值，找到后即可返回）。  
3. 对每个边长 `k`，遍历所有左上角 `(i, j)`（`0 ≤ i ≤ m-k, 0 ≤ j ≤ n-k`）。  
4. 取第一行的和作为目标值 `target`（用行前缀和得到）。  
5. 用前缀和检查 **所有 k 行、k 列、两条对角线** 是否等于 `target`。检查每行、每列都是 `O(1)`，所以一次子正方形的检查是 `O(k)`（因为要遍历 k 行/列），但不需要再遍历每个格子。  
6. 若找到合法的正方形，直接返回 `k`（因为我们是从大到小枚举的）。  

在最坏情况下我们仍会检查所有子正方形，但每次检查的代价已经从 `O(k²)` 降到 `O(k)`，整体时间变成 `O(m·n·min(m,n))`，在 50×50 的限制下几乎瞬间完成。

#### 代码（Python）

```python
def largestMagicSquare(grid):
    """
    返回 grid 中最大的魔方阵的边长
    """
    m, n = len(grid), len(grid[0])

    # ---------- 1. 预处理四类前缀和 ----------
    # 行前缀和：rowPref[i][j] = 第 i 行前 j 列的和（j 从 0 开始计数，rowPref[i][0] = 0）
    rowPref = [[0] * (n + 1) for _ in range(m)]
    # 列前缀和：colPref[i][j] = 第 j 列前 i 行的和（i 从 0 开始计数，colPref[0][j] = 0）
    colPref = [[0] * n for _ in range(m + 1)]
    # 主对角线前缀和：diagPref[i][j] 为左上角 (0,0) 到 (i,j) 主对角线的累计和
    diagPref = [[0] * n for _ in range(m)]
    # 副对角线前缀和：antiPref[i][j] 为右上角 (0,n-1) 到 (i,j) 副对角线的累计和
    antiPref = [[0] * n for _ in range(m)]

    for i in range(m):
        for j in range(n):
            # 行前缀
            rowPref[i][j + 1] = rowPref[i][j] + grid[i][j]
            # 列前缀
            colPref[i + 1][j] = colPref[i][j] + grid[i][j]
            # 主对角线前缀
            if i > 0 and j > 0:
                diagPref[i][j] = diagPref[i - 1][j - 1] + grid[i][j]
            else:
                diagPref[i][j] = grid[i][j]
            # 副对角线前缀（从右上往左下）
            if i > 0 and j + 1 < n:
                antiPref[i][j] = antiPref[i - 1][j + 1] + grid[i][j]
            else:
                antiPref[i][j] = grid[i][j]

    # ---------- 2. 从大到小尝试每一种边长 ----------
    max_len = min(m, n)
    for k in range(max_len, 0, -1):          # k 为正方形边长
        # 遍历所有左上角 (i, j) 使得 k×k 完全在矩阵内部
        for i in range(m - k + 1):
            for j in range(n - k + 1):
                # 目标和：取第一行的和
                target = rowPref[i][j + k] - rowPref[i][j]

                # ----- 检查每一行的和 -----
                ok = True
                for r in range(i, i + k):
                    cur = rowPref[r][j + k] - rowPref[r][j]
                    if cur != target:
                        ok = False
                        break
                if not ok:
                    continue

                # ----- 检查每一列的和 -----
                for c in range(j, j + k):
                    cur = colPref[i + k][c] - colPref[i][c]
                    if cur != target:
                        ok = False
                        break
                if not ok:
                    continue

                # ----- 检查两条对角线 -----
                # 主对角线 (i,j) → (i+k-1, j+k-1)
                d1 = diagPref[i + k - 1][j + k - 1]
                if i > 0 and j > 0:
                    d1 -= diagPref[i - 1][j - 1]

                # 副对角线 (i, j+k-1) → (i+k-1, j)
                d2 = antiPref[i + k - 1][j]
                if i > 0 and j + k < n:
                    d2 -= antiPref[i - 1][j + k]

                if d1 != target or d2 != target:
                    ok = False

                if ok:                     # 找到最大的正方形，直接返回
                    return k
    return 1   # 代码走不到这里，因为 1×1 必然满足
```

**代码要点解释**：

- `rowPref[i][j + k] - rowPref[i][j]`：**行区间和**，相当于“账本里第 i 行从第 j 列到第 j+k-1 列的累计”。  
- `colPref[i + k][c] - colPref[i][c]`：**列区间和**，同理。  
- 主对角线的前缀和需要减去左上方的累计，防止把不在正方形里的格子算进去。  
- 副对角线的处理方式类似，只是方向相反。  

#### 复杂度

- **时间复杂度**：`O(m·n·min(m,n))`  
  - 前缀和构造 `O(m·n)`。  
  - 主循环：对每个可能的边长 `k`（最多 `min(m,n)` 次），遍历所有左上角 `O(m·n)`，对每个正方形检查 `k` 行 + `k` 列（`O(k)`），整体上等价于 `∑_k (m·n·k) = O(m·n·min(m,n)²)`，但因为我们在检查行、列时直接用 **O(1)** 的前缀和，实际常数更小，且在最坏情况下 `k ≤ min(m,n)`，所以写作 `O(m·n·min(m,n))` 更能体现已优化的程度。对 50×50 的数据来说，最多约 `125,000` 次检查，几乎瞬间完成。

- **空间复杂度**：`O(m·n)`  
  四个前缀和矩阵各占 `m·n` 的空间，总共约四倍的原矩阵大小。对 50×50 的限制，最多几千个整数，完全在内存范围内。

---

## 心得

- **核心技巧**：**前缀和**（行、列、两条对角线）把“区间求和”从线性降到常数，让遍历更高效。  
- **适用的题型**（类似思路）  
  1. **子矩阵求和**（如 LeetCode 304、327）  
  2. **寻找满足某种和约束的子正方形/子矩形**（如 “Maximum Submatrix Sum”）  
  3. **二维前缀和**的变形，如 “Count Submatrices With All Ones”。  
- **一句话总结解题钥匙**：**用累计账本（前缀和）把重复的求和工作一次算完，再在此基础上快速验证每个候选正方形**。

---

## 反思

- **第一反应**：看到“每行、每列、两条对角线都相等”，自然想到**枚举所有子正方形**并逐行/列/对角线检查——这就是暴力解。  
- **最容易踩的坑**  
  1. **边界条件**：`k = 1` 时直接返回 1；在计算对角线前缀和时要注意不要越界（如 `i-1`、`j-1` 可能为负）。  
  2. **前缀和的减法**：忘记在左上/右上位置减去已经累计的部分，会导致对角线和错误。  
  3. **返回时机**：因为我们是从大到小枚举边长，一旦找到合法正方形就可以提前结束，否则会浪费时间。  
- **下次类似题的第一步**：**先思考能否用前缀和把“区间求和”常数化**，如果可以，就先构造前缀和，再在此基础上做枚举或滑动窗口等搜索。这样往往能把时间从“几秒”降到“毫秒”。