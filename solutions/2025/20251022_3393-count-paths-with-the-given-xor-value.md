# #3393. 计数满足给定异或值的路径数 / Count Paths With the Given XOR Value

> 难度：中等 · 标签：Array、Dynamic Programming、Bit Manipulation、Matrix · [LeetCode 链接](https://leetcode.com/problems/count-paths-with-the-given-xor-value/)

---

## 题目（英文原版）

**Description**

You are given a 2D integer array grid with size m x n. You are also given an integer k.
Your task is to calculate the number of paths you can take from the top-left cell (0, 0) to the bottom-right cell (m - 1, n - 1) satisfying the following constraints:
Return the total number of such paths.
Since the answer can be very large, return the result modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: grid = [[2, 1, 5], [7, 10, 0], [12, 6, 4]], k = 11
Output: 3
Explanation:
The 3 paths are:
```

**Example 2:**

```
Input: grid = [[1, 3, 3, 3], [0, 3, 3, 2], [3, 0, 1, 1]], k = 2
Output: 5
Explanation:
The 5 paths are:
```

**Example 3:**

```
Input: grid = [[1, 1, 1, 2], [3, 0, 3, 2], [3, 0, 2, 2]], k = 10
Output: 0
```

**Constraints**

- 1 <= m == grid.length <= 300
- 1 <= n == grid[r].length <= 300
- 0 <= grid[r][c] < 16
- 0 <= k < 16

---

## 题目（中文翻译）

给定一个大小为 `m × n` 的二维整数数组（2D integer array）`grid`，以及一个整数 `k`。  
请计算从左上角单元格 `(0, 0)` 移动到右下角单元格 `(m - 1, n - 1)` 的路径数，使得路径上所有经过的单元格的值进行异或（XOR）运算的结果恰好等于 `k`。  
返回满足条件的路径总数。由于答案可能非常大，请返回结果对 `10^9 + 7` 取模后的值。

**示例 1**  
**输入**  
``` 
grid = [[2, 1, 5], [7, 10, 0], [12, 6, 4]], k = 11
```  
**输出**  
```
3
```  
**解释**  
满足条件的 3 条路径分别是：

**示例 2**  
**输入**  
``` 
grid = [[1, 3, 3, 3], [0, 3, 3, 2], [3, 0, 1, 1]], k = 2
```  
**输出**  
```
5
```  
**解释**  
满足条件的 5 条路径分别是：

**示例 3**  
**输入**  
``` 
grid = [[1, 1, 1, 2], [3, 0, 3, 2], [3, 0, 2, 2]], k = 10
```  
**输出**  
```
0
```  

**约束条件**  
- `1 ≤ m == grid.length ≤ 300`  
- `1 ≤ n == grid[r].length ≤ 300`  
- `0 ≤ grid[r][c] < 16`  
- `0 ≤ k < 16`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有可能的路径枚举出来，逐条检查它们的 **XOR** 是否等于 `k`。  
在一个 `m × n` 的网格里，我们只能向 **右** 或 **下** 移动（和题目默认的走法保持一致），于是从左上走到右下恰好要走 `m‑1` 步向下、`n‑1` 步向右，总共 `m+n‑2` 步。  
把这 `m+n‑2` 步的顺序全部排列组合，就得到所有路径。  

- **数据结构**：我们只需要一个 `list` 保存当前走过的格子值，然后用递归（深度优先搜索）把它们的 XOR 累计起来。  
- **为什么正确**：递归会遍历每一种合法的走法，遍历结束后检查 XOR 是否等于 `k`，只要统计一次符合条件的路径即可。  

**时间复杂度**  
每一步都有两种选择（右或下），所以路径数是 `C(m+n‑2, m‑1)`，这在最坏情况下约等于 `2^{m+n}`。也就是说时间复杂度是 **指数级**，写成 `O(2^{m+n})`。  
对初学者来说可以把 `2^{10}` 想成「十次抛硬币的所有可能」，随步数增长会非常快。

**空间复杂度**  
递归栈的深度是 `m+n‑1`，再加上保存路径的临时数组，整体是 **线性** 的 `O(m+n)`。

#### 代码（Python）

```python
MOD = 10**9 + 7

def countPaths_bruteforce(grid, k):
    m, n = len(grid), len(grid[0])
    ans = 0                       # 记录符合条件的路径数

    def dfs(r, c, cur_xor):
        """从 (r,c) 开始向右/下走，cur_xor 为目前的异或值"""
        nonlocal ans
        cur_xor ^= grid[r][c]      # 把当前格子的数加入异或

        # 到达右下角，检查是否等于 k
        if r == m - 1 and c == n - 1:
            if cur_xor == k:
                ans = (ans + 1) % MOD
            return

        # 向右走
        if c + 1 < n:
            dfs(r, c + 1, cur_xor)
        # 向下走
        if r + 1 < m:
            dfs(r + 1, c, cur_xor)

    dfs(0, 0, 0)
    return ans
```

#### 复杂度

- **时间复杂度**：`O(2^{m+n})` —— 随着网格稍大，路径数会呈指数增长，实际不可用。  
- **空间复杂度**：`O(m+n)` —— 递归栈深度等于走的步数。  

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于每条路径都被完整遍历一次。我们需要 **复用** 已经算好的子路径信息。  
这正是 **动态规划（DP）** 的思路：  
- 把从左上到某个格子 `(i, j)` 的所有路径的 XOR 结果以及对应的出现次数记下来。  
- 当我们要计算格子 `(i, j)` 的信息时，只需看它的左边 `(i, j-1)` 和上边 `(i-1, j)`，把它们的 XOR 再与当前格子值 `grid[i][j]` 做一次异或即可得到新的 XOR。  

因为 `grid[i][j]` 与 `k` 的范围都只有 **0~15**（4 位二进制），所有可能的 XOR 结果也只会在 `0~15` 之间。  
所以在每个格子我们只需要维护一个长度为 16 的数组（或字典）：

```
dp[i][j][x] = 从 (0,0) 到 (i,j) 的路径数，使得路径上所有数的 XOR = x
```

转移公式：

```
for each x in 0..15:
    # 来自左边
    dp[i][j][x ^ grid[i][j]] += dp[i][j-1][x]
    # 来自上边
    dp[i][j][x ^ grid[i][j]] += dp[i-1][j][x]
```

起始状态：`dp[0][0][grid[0][0]] = 1`（只有一条路径，就是站在左上格子本身）。

最终答案就是 `dp[m-1][n-1][k]`（模 `1e9+7`）。

**为什么只需要 0~15**  
XOR 运算的结果位数不会超过参与运算数的最大位数。题目保证每个格子数 < 16，即最多 4 位二进制，所以 XOR 结果也只能在 0~15 之间。把范围限制在 16，可以把“原本可能是 O(2^{m+n}) 的状态”压缩到 `m * n * 16`，线性可接受。

**空间优化**  
我们其实只需要上一行和当前行的状态即可，用滚动数组把空间降到 `O(n * 16)`。

#### 代码（Python）

```python
MOD = 10**9 + 7
MAX_XOR = 16               # 0 ~ 15

def countPaths(grid, k):
    m, n = len(grid), len(grid[0])

    # dp[col][xor] 表示当前处理行的第 col 列的状态
    dp = [[0] * MAX_XOR for _ in range(n)]

    # 初始化左上角
    dp[0][grid[0][0]] = 1

    # 先处理第一行（只能从左往右）
    for j in range(1, n):
        for x in range(MAX_XOR):
            if dp[j-1][x]:
                new_xor = x ^ grid[0][j]
                dp[j][new_xor] = (dp[j][new_xor] + dp[j-1][x]) % MOD

    # 从第二行开始遍历
    for i in range(1, m):
        # 新建一行的 dp，先处理第一列（只能从上往下）
        new_row = [[0] * MAX_XOR for _ in range(n)]
        for x in range(MAX_XOR):
            if dp[0][x]:
                new_xor = x ^ grid[i][0]
                new_row[0][new_xor] = (new_row[0][new_xor] + dp[0][x]) % MOD

        # 处理其余列，既可以来自左边也可以来自上边
        for j in range(1, n):
            for x in range(MAX_XOR):
                cnt = dp[j][x]               # 来自上方
                if cnt:
                    new_row[j][x ^ grid[i][j]] = (new_row[j][x ^ grid[i][j]] + cnt) % MOD
                cnt = new_row[j-1][x]        # 来自左方（注意这里已经是本行的新状态）
                if cnt:
                    new_row[j][x ^ grid[i][j]] = (new_row[j][x ^ grid[i][j]] + cnt) % MOD

        dp = new_row  # 换成当前行的状态，进入下一轮

    # 最后 dp[n-1][k] 即为答案
    return dp[n-1][k] % MOD
```

> **代码说明**  
> 1. `dp` 只保留上一行的状态。  
> 2. `new_row` 用来存放当前行的结果，遍历列时左侧的状态已经在 `new_row` 中可以直接使用。  
> 3. 每次更新都取模 `MOD`，防止整数溢出。  

#### 复杂度

- **时间复杂度**：`O(m * n * 16)` → 简写为 `O(m·n)`，因为 16 是常数。  
  与暴力的指数级相比，线性时间在 300×300 的上限下也只需要约 `1.44 × 10⁶` 次基本操作，轻松跑完。  
- **空间复杂度**：`O(n * 16)` → 只用了两行滚动数组，最多约 `300 * 16 = 4800` 个整数，几乎可以忽略不计。

---

## 心得

- **核心技巧**：利用 **XOR 的取值范围有限**（0~15）把原本指数级的路径枚举压缩为 **状态压缩 DP**。  
- **适用场景**  
  1. **路径计数 + 位运算限制**（如 “XOR 为 k” / “按位与为 0” 等）  
  2. **网格 DP** 中需要记录 **额外属性**（例如路径和、路径最大值）且属性取值范围小。  
  3. **分割点 DP**：把大问题拆成两半，各自保留属性分布，再合并（如本题的左/上合并）。  
- **一句话总结**：**“把所有可能的 XOR 结果压进 16 桶，用 DP 把每一步的桶合并”**。

---

## 反思

- **第一反应**：直接写递归/DFS，想把所有路径都列举出来检查 XOR。  
- **最容易踩的坑**  
  1. **忘记取模**：答案可能非常大，必须在每次累加时取 `% 1e9+7`。  
  2. **状态遗漏**：只记路径数而不记录对应的 XOR，会导致无法判断后续合并是否满足条件。  
  3. **边界处理**：第一行只能从左边来，第一列只能从上边来，容易写成 “同时取左上” 导致索引越界。  
- **下次类似题目第一步**：先判断**属性取值范围是否小**（比如 0~15、0~255），如果是，就考虑**状态压缩 DP**；否则再思考其他技巧（如前缀和、单调栈等）。