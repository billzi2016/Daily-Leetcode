# #1931. 用三种不同颜色涂色网格 / Painting a Grid With Three Different Colors

> 难度：困难 · 标签：Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/painting-a-grid-with-three-different-colors/)

---

## 题目（英文原版）

**Description**

You are given two integers m and n. Consider an m x n grid where each cell is initially white. You can paint each cell red, green, or blue. All cells must be painted.
Return the number of ways to color the grid with no two adjacent cells having the same color. Since the answer can be very large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: m = 1, n = 1
Output: 3
Explanation: The three possible colorings are shown in the image above.
```

**Example 2:**

```
Input: m = 1, n = 2
Output: 6
Explanation: The six possible colorings are shown in the image above.
```

**Example 3:**

```
Input: m = 5, n = 5
Output: 580986
```

**Constraints**

- 1 <= m <= 5
- 1 <= n <= 1000

---

## 题目（中文翻译）

给定两个整数 `m` 和 `n`。考虑一个 `m × n` 的网格（grid），其中每个格子（cell）最初为白色。你可以将每个格子涂成红色、绿色或蓝色，且所有格子必须被涂色。  
返回满足 **没有两个相邻格子（adjacent cells）颜色相同** 的涂色方案数。由于答案可能非常大，请返回答案对 `10^9 + 7` 取模（modulo）的结果。

### 示例

**示例 1**  
```text
Input: m = 1, n = 1
Output: 3
Explanation: 如上图所示，三种可能的涂色方式。
```

**示例 2**  
```text
Input: m = 1, n = 2
Output: 6
Explanation: 如上图所示，六种可能的涂色方式。
```

**示例 3**  
```text
Input: m = 5, n = 5
Output: 580986
```

### 约束条件

- `1 <= m <= 5`
- `1 <= n <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把整个 `m × n` 的格子一次性遍历完，每个格子都尝试三种颜色（红、绿、蓝），把所有可能的涂法枚举出来，然后把“不相邻格子颜色相同”的约束逐一检查，符合的计数加一。

- **用到的数据结构**：  
  - 一个二维列表 `grid` 保存当前格子的颜色。可以把它想象成一张纸，上面画了格子，`grid[i][j]` 就是第 `i` 行第 `j` 列的颜色。  
  - 递归函数 `dfs(pos)` 用来把格子“一个一个地涂”。这里的 `pos` 类似于在一本字典里查找单词的顺序编号，先涂第一个格子，再涂第二个，依次往后。

- **为什么正确**：  
  - 递归会遍历 **所有** 可能的颜色组合（每个格子 3 种颜色），所以不可能漏掉任何合法的涂法。  
  - 每次在递归结束（所有格子都涂完）时检查相邻格子是否冲突，只有全部满足约束的才计入答案。因此统计的就是题目要求的合法涂法数目。

- **复杂度分析（大白话版）**：  
  - **时间复杂度**：格子总数是 `m·n`，每个格子有 3 种选择，所以总的组合数是 `3^(m·n)`，递归会遍历全部这些组合。用大写的 **O** 表示就是 `O(3^{m·n})`。可以把它想象成“指数级别的增长”，即使 `m=5、n=5` 也会有 `3^25 ≈ 8.5×10^{11}` 种情况，根本不可能在电脑里跑完。  
  - **空间复杂度**：递归的深度等于格子数 `m·n`，每层递归要保存一个局部变量，所以空间是 `O(m·n)`（即格子数），再加上保存整个网格的 `O(m·n)`，总共也是线性。

#### 代码（Python）

```python
MOD = 10**9 + 7

def num_of_ways_bruteforce(m: int, n: int) -> int:
    """暴力枚举全部涂色方案，适用于极小的 m、n（仅作概念演示）。"""
    # 0、1、2 分别代表红、绿、蓝
    colors = [0, 1, 2]
    grid = [[-1] * n for _ in range(m)]   # -1 表示未上色
    total = 0

    def valid(i: int, j: int, c: int) -> bool:
        """检查把 (i,j) 涂成颜色 c 是否与已经上色的相邻格子冲突。"""
        # 上方格子
        if i > 0 and grid[i-1][j] == c:
            return False
        # 左方格子
        if j > 0 and grid[i][j-1] == c:
            return False
        return True

    def dfs(pos: int):
        """按顺序涂第 pos 个格子（从左上到右下）。"""
        nonlocal total
        if pos == m * n:          # 所有格子都涂完了
            total = (total + 1) % MOD
            return
        i, j = divmod(pos, n)     # 把一维索引转成二维坐标
        for c in colors:
            if valid(i, j, c):
                grid[i][j] = c    # 涂色
                dfs(pos + 1)      # 继续涂下一个格子
                grid[i][j] = -1   # 恢复现场（回溯）

    dfs(0)
    return total
```

#### 复杂度

- **时间复杂度**：`O(3^{m·n})` —— 每个格子都有 3 种选择，全部遍历。  
- **空间复杂度**：`O(m·n)` —— 保存网格以及递归栈的深度。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**把整张网格一次性枚举**，导致指数级的组合数。  
观察约束可以发现：

1. **相邻只在同一行或同一列**。因此如果我们一次只关注**一列**，只要保证：
   - 同一列内部的相邻格子颜色不同（竖向约束）；
   - 与左边那一列对应行的颜色不同（横向约束）；
   那么整张网格就一定合法。

2. **列的高度 `m` ≤ 5**，这意味着每列的所有可能涂法最多是 `3^5 = 243` 种，数量非常小。我们可以把每一种合法的列涂法抽象成一个 **状态码**（也叫“位掩码”），用一个整数来表示整列的颜色序列。  
   - 类比：把每列看成一本小字典，里面只有 243 条“单词”。我们把每条单词映射成一个编号，后面只在编号之间做比较，省掉了逐格比较的麻烦。

3. **状态转移**：设 `dp[col][s]` 为第 `col` 列涂成状态 `s` 的合法方案数。转移时，只要左侧列的状态 `t` 与当前状态 `s` 在每一行上颜色不同，就可以把 `dp[col-1][t]` 的方案数加到 `dp[col][s]`。这一步只涉及两列之间的比较，时间从 `3^{m·n}` 降到 `n * K^2`（`K` 为合法列状态数），对 `m ≤ 5` 来说是完全可以接受的。

4. **预处理**：  
   - 先枚举所有 `3^m` 种颜色组合，筛掉竖向相邻相同的，得到合法列集合 `valid_cols`（大小记作 `K`）。  
   - 再遍历 `valid_cols` 两两配对，记录哪些状态可以相邻（即横向不冲突），得到 `compat[s]` 列表。这样在 DP 时只需要遍历兼容的左侧状态，进一步降低常数。

5. **取模**：答案可能非常大，题目要求对 `10^9+7` 取模。所有加法都在取模后进行，防止整数溢出。

**关键概念解释**：

- **位掩码（mask）**：把每一行的颜色视作 2 位二进制（因为 3 种颜色可以用 0/1/2 编号），把整列的 `m` 行颜色依次左移并相加，形成唯一的整数。类似把一串颜色“压缩”进一个数字，像把一本厚厚的书压成一本小册子，便于快速比较和存储。

- **动态规划（DP）**：把大问题（整张网格的合法涂法）拆成若干子问题（每列的合法涂法），利用子问题的最优解递推得到整体答案。

#### 代码（Python）

```python
MOD = 10**9 + 7

def num_of_ways(m: int, n: int) -> int:
    """
    动态规划 + 位掩码
    时间复杂度：O(n * K^2) ，K <= 3^m (m <= 5)
    空间复杂度：O(K)      ，只保留当前列的 DP 表
    """
    # ---------- 1. 生成所有合法的列状态 ----------
    # 用 0、1、2 表示三种颜色
    total_states = 3 ** m                 # 所有可能的颜色组合数
    valid_cols = []                       # 只保留竖向相邻不同的列
    col_to_mask = []                      # 把颜色列表转成整数 mask，方便后面比较

    for num in range(total_states):
        colors = []                        # 这列的每一行颜色
        x = num
        ok = True
        for _ in range(m):
            colors.append(x % 3)           # 取低两位（0/1/2）作为颜色
            x //= 3
        # 检查竖向相邻格子是否冲突
        for i in range(1, m):
            if colors[i] == colors[i-1]:
                ok = False
                break
        if ok:
            # 把颜色序列压成一个整数（位掩码）
            mask = 0
            for i in range(m):
                mask = mask * 3 + colors[i]   # 类似把每个颜色当作 3 进制的一个位
            valid_cols.append(mask)

    K = len(valid_cols)                    # 合法列的数量，最多 3^5 = 243

    # ---------- 2. 预计算列之间的兼容性 ----------
    # compat[s] = [t1, t2, ...] 表示状态 s 可以紧跟在这些状态 t 之后
    compat = [[] for _ in range(K)]
    # 把 mask 分解回颜色列表的辅助函数
    def mask_to_colors(mask):
        arr = [0] * m
        for i in range(m-1, -1, -1):
            arr[i] = mask % 3
            mask //= 3
        return arr

    col_colors = [mask_to_colors(mask) for mask in valid_cols]

    for i in range(K):
        for j in range(K):
            # 检查横向相邻（同一行）是否冲突
            ok = True
            for row in range(m):
                if col_colors[i][row] == col_colors[j][row]:
                    ok = False
                    break
            if ok:
                compat[i].append(j)

    # ---------- 3. DP 迭代 ----------
    # dp[i] 表示第当前列涂成状态 i 的方案数
    dp = [1] * K          # 第 0 列（左侧第一列）任意合法状态都有 1 种方案
    for col in range(1, n):   # 从第 2 列开始向右推进
        new_dp = [0] * K
        for cur in range(K):
            total = 0
            for pre in compat[cur]:   # 只遍历兼容的左侧状态
                total += dp[pre]
            new_dp[cur] = total % MOD
        dp = new_dp

    # ---------- 4. 汇总答案 ----------
    return sum(dp) % MOD
```

#### 复杂度

- **时间复杂度**：`O(n * K^2)`，其中 `K` 是合法列状态数，`K ≤ 3^m ≤ 243`。因为 `n ≤ 1000`，实际运行时间大约在 `1000 * 243^2 ≈ 5.9×10^7` 次基本操作，完全能在一秒以内完成。  
  - 与暴力解的 `O(3^{m·n})` 相比，指数级的增长被压缩到了 **线性**（对 `n`）乘以一个常数（约 2‑3 百），差距天壤之别。

- **空间复杂度**：`O(K)`，只保存当前列的 DP 表和兼容列表。`K` 最多 243，几乎可以忽略不计。

---

## 心得

- **核心技巧**：把二维约束拆成“列状态 + 列间兼容” 的动态规划，利用 **位掩码** 将每列的颜色组合压缩成一个整数，从而实现快速比较与转移。  
- **适用的题型**（类似思路）：
  1. **染色棋盘**（每格 2 种颜色，行列相邻不同）  
  2. **放置瓷砖/状态压缩 DP**（如 `Domino tiling`、`Minesweeper` 之类的格子约束问题）  
  3. **LeetCode 1743. Restore the Array From Adjacent Pairs**（需要把局部信息拼接成全局）  
- **一句话总结解题钥匙**：**把大网格拆成“小列”，用状态压缩把每列的合法涂法编号，再用 DP 只在相邻列之间转移**。

---

## 反思

- **第一反应**：看到“相邻格子颜色不同”，立刻想到“逐格遍历，暴力检查”。这在小规模时很自然，但面对 `n ≤ 1000` 的规模，必须寻找更高效的结构。  
- **最容易踩的坑**：  
  - **竖向约束忘记**：在生成合法列状态时必须先确保同一列内部相邻格子不同，否则后面的 DP 会计入非法方案。  
  - **取模遗漏**：DP 过程中累计次数会很快超出 Python 整数范围，务必要在每一次加法后 `mod`。  
  - **状态编号混淆**：位掩码的构造顺序（从低位到高位或相反）一定要统一，否则比较时会产生错误的兼容关系。  
- **下次遇到同类题**：第一步就要思考“是否可以把二维约束压缩成一维状态”，尝试**状态压缩 DP**（列或行为单位），并预先枚举所有合法的局部状态。这样可以把指数级搜索降到多项式级别。