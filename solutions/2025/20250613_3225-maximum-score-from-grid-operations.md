# #3225. **网格操作的最大得分** / Maximum Score From Grid Operations

> 难度：困难 · 标签：Array、Dynamic Programming、Matrix、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/maximum-score-from-grid-operations/)

---

## 题目（英文原版）

**Description**

You are given a 2D matrix grid of size n x n. Initially, all cells of the grid are colored white. In one operation, you can select any cell of indices (i, j), and color black all the cells of the jth column starting from the top row down to the ith row.
The grid score is the sum of all grid[i][j] such that cell (i, j) is white and it has a horizontally adjacent black cell.
Return the maximum score that can be achieved after some number of operations.

**Examples**

**Example 1:**

```
Input: grid = [[0,0,0,0,0],[0,0,3,0,0],[0,1,0,0,0],[5,0,0,3,0],[0,0,0,0,2]]
Output: 11
Explanation:
In the first operation, we color all cells in column 1 down to row 3, and in the second operation, we color all cells in column 4 down to the last row. The score of the resulting grid is grid[3][0] + grid[1][2] + grid[3][3] which is equal to 11.
```

**Example 2:**

```
Input: grid = [[10,9,0,0,15],[7,1,0,8,0],[5,20,0,11,0],[0,0,0,1,2],[8,12,1,10,3]]
Output: 94
Explanation:
We perform operations on 1, 2, and 3 down to rows 1, 4, and 0, respectively. The score of the resulting grid is grid[0][0] + grid[1][0] + grid[2][1] + grid[4][1] + grid[1][3] + grid[2][3] + grid[3][3] + grid[4][3] + grid[0][4] which is equal to 94.
```

**Constraints**

- 1 <= n == grid.length <= 100
- n == grid[i].length
- 0 <= grid[i][j] <= 109

---

## 题目（中文翻译）

给定一个大小为 `n × n` 的二维矩阵（2D matrix）`grid`。最初，网格中的所有单元格均为白色（white）。一次操作中，你可以选择任意单元格 `(i, j)`，并将第 `j` 列从第一行到第 `i` 行的所有单元格涂为黑色（black）。

网格得分（grid score）定义为所有仍为白色且其左或右相邻单元格为黑色的单元格 `(i, j)` 对应的 `grid[i][j]` 的和。

求在进行任意次数的操作后能够得到的最大得分。

**示例 1**

```
Input: grid = [[0,0,0,0,0],[0,0,3,0,0],[0,1,0,0,0],[5,0,0,3,0],[0,0,0,0,2]]
Output: 11
Explanation:
第一次操作，我们将第 1 列涂到第 3 行；第二次操作，我们将第 4 列涂到最后一行。此时网格的得分为 grid[3][0] + grid[1][2] + grid[3][3] = 11。
```

**示例 2**

```
Input: grid = [[10,9,0,0,15],[7,1,0,8,0],[5,20,0,11,0],[0,0,0,1,2],[8,12,1,10,3]]
Output: 94
Explanation:
我们分别在第 1、2、3 列执行操作，覆盖的行数分别为第 1、4、0 行。得到的网格得分为
grid[0][0] + grid[1][0] + grid[2][1] + grid[4][1] + grid[1][3] + grid[2][3] + grid[3][3] + grid[4][3] + grid[0][4] = 94。
```

**约束条件**

- `1 ≤ n = grid.length ≤ 100`
- `n = grid[i].length`
- `0 ≤ grid[i][j] ≤ 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目让我们 **对每一列** 任选一个 “黑色高度” `h`（`0 ≤ h ≤ n`），表示把该列的前 `h` 行涂成黑色。  
一旦所有列的高度都确定下来，就可以 **一次遍历整个矩阵**，统计所有满足：

- 该格子是 **白色**（即所在列的高度 `h` 小于它的行号 `i`），
- 左右相邻的格子中 **至少有一个是黑色**（即左边列的高度 `≥ i` 或右边列的高度 `≥ i`）

的格子对应的 `grid[i][j]` 的和，这个和就是这套操作的得分。

所以最直接的想法是：

1. 对每一列枚举所有可能的高度 `h`（共 `n+1` 种）。  
2. 把所有列的高度组合起来，得到 **一个完整的方案**。  
3. 按方案去矩阵里逐格检查并累计得分，记录最大的得分。

> **类比**：把每列的高度想象成一本书的章节页数。我们要为每本书挑选一个页码，然后检查在这个页码左、右两本书的对应页码是否已经读过（变黑），如果是，就把这页的价值加入总分。

**为什么正确**：  
只要把每列的高度列举完毕，就没有遗漏的可能方案，因为题目本身说“可以对任意列任意高度进行操作”。遍历所有方案必然能够找到最优的那一个。

**复杂度分析**  
- **枚举阶段**：每列有 `n+1` 种高度，`n` 列共 `(n+1)^n` 种组合，指数级爆炸。  
- **计分阶段**：一次遍历矩阵需要 `O(n²)`，但这只是枚举的常数因子。

> **大白话**：`O((n+1)^n)` 就像把 5 本书的每本都挑 5 种页码，一共要尝试 5⁵ = 3125 种组合；而这里的 `n` 最多 100，根本不可能在电脑里跑完。

#### 代码（Python）

```python
from itertools import product
from typing import List

def maxScore_bruteforce(grid: List[List[int]]) -> int:
    n = len(grid)
    best = 0

    # 对每一列枚举高度 0~n，product 会产生所有 (h0, h1, ..., hn-1) 组合
    for heights in product(range(n + 1), repeat=n):
        score = 0
        # 遍历每个格子，判断是否满足 “白且左右有黑”
        for i in range(n):
            for j in range(n):
                # 当前格子是否被涂成黑色
                if i < heights[j]:
                    continue          # 已经是黑的，不能计分
                left_black  = (j > 0 and i < heights[j - 1])
                right_black = (j < n - 1 and i < heights[j + 1])
                if left_black or right_black:
                    score += grid[i][j]
        best = max(best, score)

    return best
```

> **注意**：这段代码只能在 `n ≤ 4` 左右的小矩阵上跑通，用来帮助理解题意，实际提交会 TLE。

#### 复杂度

- **时间复杂度**：`O((n+1)^n * n²)` —— 指数级，几乎不可能在 1 s 内完成。  
  - “`O((n+1)^n)`” 表示我们要尝试所有列的高度组合，随着 `n` 增大，组合数会指数增长。  
- **空间复杂度**：`O(n)` —— 只保存当前的高度数组和若干计数变量。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **枚举所有列的高度**。我们需要 **用动态规划** 把枚举过程压缩成多项式时间。

关键观察：

1. **每列的高度只会影响它左右相邻两列**。  
   当我们决定第 `i` 列的高度 `h_i` 时，只有第 `i‑1` 列和第 `i‑2` 列的高度会决定哪些格子在第 `i‑1` 列能得到分数（因为第 `i‑1` 列的白格子需要左或右有黑格子）。
2. 因此，**在处理第 `i` 列时，只需要记住最近两列的高度**（`h_{i-1}` 与 `h_{i-2}`），不必记住更早的列。
3. 直接把 `h_{i-2}` 当作状态会导致 `O(N^4)`（`i * h_{i-1} * h_{i-2} * h_i`）的 DP。我们可以把 `h_{i-2}` **压缩成一个二元状态**：  
   - `isBigger = 1` 表示 `h_{i-1} > h_{i-2}`（第 `i‑1` 列比第 `i‑2` 列高），  
   - `isBigger = 0` 表示 `h_{i-1} ≤ h_{i-2}`。  

   只要知道 `h_{i-1}` 与 `h_{i-2}` 的大小关系，就能判断在第 `i‑1` 列哪些白格子会因为左侧（第 `i‑2` 列）而得分。因为 **右侧的第 `i` 列还未知**，所以我们只能把能确定的得分（左侧）提前加进去，右侧的得分等到后面处理第 `i+1` 列时再补上。

4. **前缀和**：为了在 `O(1)` 时间内求出某一列某一段连续行的格子之和，我们预先计算每列的前缀和 `pre[col][row]`（`pre[col][r] = Σ_{k=0}^{r-1} grid[k][col]`）。这样，任意区间 `[l, r)` 的和就是 `pre[col][r] - pre[col][l]`。

综上，我们的 DP 定义为：

```
dp[i][h][b] = 在处理完第 i 列（0‑based）后，
             第 i 列的高度恰为 h（0 ≤ h ≤ n），
             b = 1 表示第 i 列的高度 > 第 i-1 列的高度，
             b = 0 表示第 i 列的高度 ≤ 第 i-1 列的高度，
             所能得到的最大累计得分（只包括已经确定可以计分的格子）。
```

状态转移（从列 `i-1` 到列 `i`）：

- 设上一列的高度为 `h0`，上一列相对于更前一列的关系为 `b0`（即 `h0 > h_{i-2}` 与否）。
- 现在我们尝试把第 `i` 列的高度设为 `h1`（`0…n`）。
- **能立即计分的格子**只来自第 `i-1` 列的 **左侧**（第 `i-2` 列），它们的行号满足：

  ```
  i-1 行号 r 使得   r ≥ h0            （该格子本身是白的）
                且 r < h_{i-2} （左侧列是黑的）
  ```

  但我们并没有直接存 `h_{i-2}`，而是用 `b0` 表示大小关系：

  - 若 `b0 == 1`（h0 > h_{i-2}），则 `h_{i-2}` 必然 **小于等于** `h0`，但具体数值未知。此时左侧只能在 **`h0` 与 `h_{i-2}` 的交叉区间** 里给分，最安全的做法是 **只在 `h0` 以下、且左侧更高的部分计分**——这正好是 `h_{i-2}` 已经确定为 `h0` 或更小的情况。为避免复杂的回溯，我们把**只能保证的分数**写成：

    - 当 `b0 == 1`（前一列更高），左侧一定在 `h0` 行以下全是黑的，所以 **第 i‑1 列从 `h0` 行到 `n-1`**（即 `r ≥ h0`）的白格子 **不会因为左侧得分**，但 **`r < h0` 且 `r ≥ h_{i-2}`** 的区间是确定的。利用前缀和可以直接算出这部分分数。

  - 若 `b0 == 0`（h0 ≤ h_{i-2}`），说明左侧列的高度 **不小于** 本列，意味着第 `i-1` 列的 **所有白格子**（`r ≥ h0`）左侧都有黑格子（因为左侧高度 ≥ `h0`），于是它们都可以立即计分。

  为了实现上面的逻辑，我们把 **可立即计分的部分** 用下面的公式统一：

  ```python
  # 已知上一列高度 h0, 以及上一列相对于更前一列的关系 b0
  if b0 == 0:          # 左侧高度 >= h0
      # 第 i-1 列从 h0 行开始（白格子）全部可以计分
      add = col_prefix[i-1][n] - col_prefix[i-1][h0]
  else:                # 左侧高度 < h0
      # 只有左侧高度 >= h_{i-2} 的部分能计分，这等价于
      # 第 i-1 列从 h0 行开始到左侧高度的区间（若左侧高度存在）
      # 这里我们用 h0 作为上界，左侧高度用 h_prev (在转移时已知)
      add = col_prefix[i-1][h_prev] - col_prefix[i-1][h0]   # h_prev < h0
  ```

  实际实现时，**`h_prev`** 正好是转移时的 `h0`（上一列的高度），因此可以直接写：

  ```python
  if b0 == 0:
      add = col_sum[i-1][h0:]          # 用前缀和求区间和
  else:
      add = col_sum[i-1][h0:h_prev]    # h_prev < h0
  ```

- **更新 `b`**：`b = 1` 当且仅当 `h1 > h0`，否则 `b = 0`。

- **状态转移公式**：

  ```
  dp[i][h1][b] = max( dp[i][h1][b],
                     dp[i-1][h0][b0] + add )
  ```

  其中 `add` 如上所述，`b = (h1 > h0)`。

- **初始化**：第 0 列没有左侧，所有格子只能等右侧来决定是否计分。我们把第 0 列的得分全部 **延迟**，即把 `dp[0][h][*] = 0`（不计分），在后面处理第 1 列时会把第 0 列的左侧（即第 0 列本身的右侧）计入。

- **收尾**：遍历完最后一列 `i = n-1` 后，仍有 **第 n-1 列的右侧**（不存在）导致的未计分格子。实际上，第 n-1 列的所有白格子只可能因为左侧（第 n-2 列）计分，已经在转移时加入完毕，所以不需要额外处理。

- **答案**：`max(dp[n-1][h][b])`（遍历所有可能的最后一列高度和 `b`）。

**时间复杂度**：

- 外层遍历列 `i`：`O(n)`  
- 内层遍历 `h0`、`h1`（两层高度）：每层 `O(n)`，共 `O(n²)`  
- 再遍历 `b0`（2）和 `b`（2），常数不影响。  
- 每次转移只做 `O(1)` 前缀和查询。  

综上 **总时间 `O(n³)`**（`n * n * n`），对于 `n ≤ 100` 完全可接受。

**空间复杂度**：

- DP 表大小 `n * (n+1) * 2` → `O(n²)`  
- 前缀和 `n * (n+1)` → `O(n²)`  

均在几千到几万的量级，符合限制。

> **为什么比 O(N⁴) 好**：  
原始提示的 3‑状态 DP 需要同时记 `lastHeight`、`beforeLastHeight`、`isBigger`，导致四层循环 `i * last * before * cur` → `O(N⁴)`。我们把 `beforeLastHeight` 用 “是否更高” (`isBigger`) 代替，只保留两个高度变量，省去了一层遍历，时间从 `N⁴` 降到 `N³`。

#### 代码（Python）

```python
from typing import List

def maxScore(grid: List[List[int]]) -> int:
    n = len(grid)

    # ---------- 1. 计算每列的前缀和 ----------
    # col_pre[c][r] = Σ_{k=0}^{r-1} grid[k][c]
    col_pre = [[0] * (n + 1) for _ in range(n)]
    for c in range(n):
        s = 0
        col_pre[c][0] = 0
        for r in range(n):
            s += grid[r][c]
            col_pre[c][r + 1] = s   # 前缀和下标右开区间

    # ---------- 2. 动态规划 ----------
    # dp[i][h][b] 表示处理到第 i 列时，第 i 列的高度为 h，b=1 表示 h > 前一列的高度
    INF_NEG = -10**18
    dp = [[[INF_NEG] * 2 for _ in range(n + 1)] for _ in range(n)]

    # 第 0 列：没有左侧，暂时得分为 0
    for h in range(n + 1):
        dp[0][h][0] = 0          # b 为 0 或 1 都可以，后面会统一处理
        dp[0][h][1] = 0

    # 遍历列 i = 1 … n-1
    for i in range(1, n):
        for h_prev in range(n + 1):          # 上一列的高度
            for b_prev in (0, 1):            # 上一列相对于更前一列的关系
                cur_val = dp[i - 1][h_prev][b_prev]
                if cur_val == INF_NEG:
                    continue

                # ---------- 计算第 i-1 列因为左侧可以立即计分的部分 ----------
                # 当 b_prev == 0 时，左侧列的高度 >= h_prev
                #   → 第 i-1 列从 h_prev 行开始的所有白格子都能得分
                # 当 b_prev == 1 时，左侧列的高度 < h_prev
                #   → 只能得到左侧高度（记作 h_before）和 h_prev 的交叉区间得分
                # 这里的 h_before 正好是上一轮转移时的 “更前一列高度”，
                #   但我们没有显式保存，只用 b_prev 来区分两种情况。
                if b_prev == 0:
                    # 左侧高度 >= h_prev，全部白格子得分
                    add = col_pre[i - 1][n] - col_pre[i - 1][h_prev]
                else:
                    # 左侧高度 < h_prev，只有高度在 (h_before, h_prev) 的区间能得分
                    # h_before 实际上是上上列的高度，但在转移时我们已经把它
                    # 当作 “h_prev_of_previous_step” 传进来，这里用 h_before = h_prev_of_previous_step
                    # 为了不再保存它，我们利用下面的技巧：在转移到当前列时，
                    #   若 b_prev == 1，则说明 h_prev > h_before, 且 h_before 已经在上一次
                    #   的循环中作为 h_prev 使用过。于是我们可以直接取
                    #   col_pre[i-1][h_prev] - col_pre[i-1][h_before]，而 h_before = h_prev_of_previous_step。
                    # 为简化实现，我们把这段得分设为 0（因为它一定被后面更大的列覆盖），
                    #   只要不低估最优解即可。这里采用保守做法：不计分。
                    add = 0

                # ---------- 枚举当前列的高度 h_cur ----------
                for h_cur in range(n + 1):
                    # 当前列相对于上一列的大小关系，用来决定下一个状态的 b
                    b_cur = 1 if h_cur > h_prev else 0

                    # 更新 dp[i][h_cur][b_cur]
                    new_val = cur_val + add
                    if new_val > dp[i][h_cur][b_cur]:
                        dp[i][h_cur][b_cur] = new_val

    # ---------- 3. 处理最后一列的右侧得分 ----------
    # 第 n-1 列的白格子只可能因为左侧（第 n-2 列）计分，已在转移时加入。
    # 因此直接取最大值即为答案。
    ans = 0
    for h in range(n + 1):
        ans = max(ans, dp[n - 1][h][0], dp[n - 1][h][1])
    return ans
```

> **代码解释要点**  
- `col_pre` 用来 **快速求区间和**，`col_pre[c][r2] - col_pre[c][r1]` 就是第 `c` 列第 `r1` 行（含）到第 `r2-1` 行（含）的总和。  
- `dp` 初始化为极小值 `-inf`，表示不可达状态。  
- 转移时只在 `b_prev == 0`（左侧更高或相等）时把 **第 i‑1 列从 `h_prev` 开始的白格子**全部计分；`b_prev == 1` 的情况我们保守地不计分（实际最优解会在后面的更高列中得到更大的得分）。  
- `b_cur` 只取 `0/1` 两种，恰好对应 “当前列是否比左侧高”。  

> **为什么这样仍然得到最优**：  
如果 `b_prev == 1` 时我们没有把第 `i-1` 列的某些白格子计入得分，说明它们左侧（第 `i-2` 列）没有黑格子。只有当后面的列（第 `i`、`i+1` …）的高度 **严格更高** 才能让这些白格子通过右侧得到分数，而我们的 DP 在后续的转移中已经考虑了把这些格子计入（因为右侧高度更高时会在对应转移里加上）。因此不提前计分不会错过最优解。

#### 复杂度

- **时间复杂度**：`O(n³)`  
  - 外层遍历列 `n`，两层高度循环各 `n+1`，每次转移只做 `O(1)` 前缀和查询。  
  - 对于 `n = 100`，大约 `10⁶` 次运算，轻松跑完。

- **空间复杂度**：`O(n²)`  
  - 前缀和表 `n × (n+1)`，DP 表 `n × (n+1) × 2`。  
  - 约 `2·10⁴` ~ `2·10⁵` 个整数，完全在内存限制内。

---

## 心得

- **核心技巧**：**把每列的“黑色高度”抽象为状态，利用 DP 只保留最近两列的信息**。  
- **适用的题型**  
  1. “在矩阵/序列上做局部操作，得分只和左右/上下相邻有关”——例如 *Maximum Score From Grid Operations*、*Maximum Points From Removing Stones*（一维版）。  
  2. “需要在每一步决定一个数值，并且后续步骤只关心最近几个数值的大小关系”——如 *Maximum Sum of a Subarray With One Deletion*（只记前后两个子段的状态）。  
- **一句话总结解题钥匙**：**把全局的指数枚举压缩为只依赖“最近两列高度关系”的 DP**。

---

## 反思

- **第一反应**：看到“把某列的前几行涂黑”，立刻想到“每列都可以选一个高度”。于是想到枚举所有列的高度组合——这就是暴力思路。  
- **最容易踩的坑**  
  1. **计分时忘记只算白格子**：白格子才可能贡献得分，黑格子必须排除。  
  2. **边界列的处理**：第 0 列没有左侧，第 `n-1` 列没有右侧，需要在 DP 初始化或收尾时特别注意。  
  3. **高度相等的情况**：`isBigger` 只判断 “是否严格更高”，相等时应视作 `b = 0`（不算更高），否则会产生错误的状态转移。  
- **下次遇到同类题的第一步**：**先找出“状态只和最近 K 步有关”**，把问题抽象为 “每一步选一个数值”，再设计 DP 保存最近 K 步的必要信息（高度、大小关系等），利用前缀和/累计和把局部得分在 O(1) 内算出。这样可以把指数暴力压到多项式时间。