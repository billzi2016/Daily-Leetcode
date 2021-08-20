# #1444. 切披萨的方案数 / Number of Ways of Cutting a Pizza

> 难度：困难 · 标签：Array、Dynamic Programming、Memoization、Matrix、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/number-of-ways-of-cutting-a-pizza/)

---

## 题目（英文原版）

**Description**

Given a rectangular pizza represented as a rows x cols matrix containing the following characters: 'A' (an apple) and '.' (empty cell) and given the integer k. You have to cut the pizza into k pieces using k-1 cuts.
For each cut you choose the direction: vertical or horizontal, then you choose a cut position at the cell boundary and cut the pizza into two pieces. If you cut the pizza vertically, give the left part of the pizza to a person. If you cut the pizza horizontally, give the upper part of the pizza to a person. Give the last piece of pizza to the last person.
Return the number of ways of cutting the pizza such that each piece contains at least one apple. Since the answer can be a huge number, return this modulo 10^9 + 7.

**Examples**

**Example 1:**

```
Input: pizza = ["A..","AAA","..."], k = 3
Output: 3 
Explanation: The figure above shows the three ways to cut the pizza. Note that pieces must contain at least one apple.
```

**Example 2:**

```
Input: pizza = ["A..","AA.","..."], k = 3
Output: 1
```

**Example 3:**

```
Input: pizza = ["A..","A..","..."], k = 1
Output: 1
```

**Constraints**

- 1 <= rows, cols <= 50
- rows == pizza.length
- cols == pizza[i].length
- 1 <= k <= 10
- pizza consists of characters 'A' and '.' only.

---

## 题目（中文翻译）

给定一个由 `rows × cols` 矩阵表示的矩形披萨，其中每个格子包含字符 `'A'`（苹果）或 `'.'`（空格），以及一个整数 `k`。你需要通过 `k‑1` 次切割将披萨分成 `k` 块。

对于每一次切割，你可以选择切割方向：**垂直**（vertical）或 **水平**（horizontal），然后在单元格边界处选定切割位置，将披萨分成两块。如果进行垂直切割，则把左侧的部分分给一位顾客；如果进行水平切割，则把上侧的部分分给一位顾客。最后剩下的那块披萨分给最后一位顾客。

返回能够使每块披萨至少包含一个苹果的切割方案数。由于答案可能非常大，请返回结果对 `10^9 + 7` 取模后的值。

## 示例

### 示例 1
```
Input: pizza = ["A..","AAA","..."], k = 3
Output: 3
Explanation: 上图展示了三种满足条件的切割方式。注意，每块披萨都必须至少含有一个苹果。
```

### 示例 2
```
Input: pizza = ["A..","AA.","..."], k = 3
Output: 1
```

### 示例 3
```
Input: pizza = ["A..","A..","..."], k = 1
Output: 1
```

## 约束条件

- `1 <= rows, cols <= 50`
- `rows == pizza.length`
- `cols == pizza[i].length`
- `1 <= k <= 10`
- `pizza` 仅由字符 `'A'` 和 `'.'` 组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的切法**，只要切完后每块都含有至少一个苹果，就算一种合法方案。  
具体可以这么做：

1. 从左上角 `(0,0)` 开始，尝试在每一条水平或垂直的边界处切一次（总共有 `rows-1` 条水平线和 `cols-1` 条垂直线可以切）。  
2. 切完后把上面或左边的那块交给第一个人，剩下的部分继续递归切 `k-1` 次。  
3. 递归的终止条件是已经切完 `k-1` 次，此时只要剩下的整块 pizza 含有至少一个苹果，就算一种合法切法。

> **类比**：想象你在一张纸上画格子，每次都把纸折一次，折好的那块直接送给朋友，剩下的纸继续折。只要每块纸上都有苹果（标记），这次折纸方式就是合法的。

**为什么正确**：  
我们把**所有**可能的切法都遍历了一遍，只要满足题目要求（每块都有苹果），就计数。遍历完整个搜索树，得到的计数必然等于所有合法切法的数量。

**时间/空间分析**：  
- 每一次切都有 `O(rows + cols)` 种可能（所有水平线 + 所有垂直线）。  
- 递归深度最多 `k-1 ≤ 9`（因为 `k ≤ 10`），所以**最坏情况**的搜索树大小约为  
  \[
  (rows+cols)^{k-1}
  \]  
  对于最大限制 `rows = cols = 50`、`k = 10`，这会是天文数字，根本跑不完。  
- 递归栈的深度是 `k`，空间是 `O(k)`。

> **大白话解释**：`O(n²)` 就是说如果 `n` 是 100，运算量大约是 10000；而这里的 `(rows+cols)^{k-1}` 甚至比 `n⁶` 还大，几乎不可能在几秒内算完。

#### 代码（Python）

```python
MOD = 10**9 + 7

def has_apple(pizza, r1, c1, r2, c2):
    """检查子矩阵 (r1,c1)~(r2,c2) 是否至少有一个 'A'"""
    for i in range(r1, r2 + 1):
        for j in range(c1, c2 + 1):
            if pizza[i][j] == 'A':
                return True
    return False

def dfs(pizza, r, c, cuts):
    """
    从左上角 (r,c) 开始，剩余的子 pizza 为
    rows-1, cols-1 为右下角。cuts 表示还需要再切几次。
    """
    rows, cols = len(pizza), len(pizza[0])
    # 基础情况：已经没有切了，检查剩下的是否有苹果
    if cuts == 0:
        return 1 if has_apple(pizza, r, c, rows - 1, cols - 1) else 0

    total = 0
    # 尝试所有水平切线（切掉上面的部分）
    for nr in range(r, rows - 1):
        if has_apple(pizza, r, c, nr, cols - 1):          # 上面这块必须有苹果
            total += dfs(pizza, nr + 1, c, cuts - 1)      # 剩下的继续切
            total %= MOD

    # 尝试所有垂直切线（切掉左边的部分）
    for nc in range(c, cols - 1):
        if has_apple(pizza, r, c, rows - 1, nc):          # 左边这块必须有苹果
            total += dfs(pizza, r, nc + 1, cuts - 1)      # 剩下的继续切
            total %= MOD

    return total

def ways_bruteforce(pizza, k):
    return dfs(pizza, 0, 0, k - 1)
```

> **注**：`has_apple` 每次都要遍历整个子矩阵，导致整体时间复杂度更高。

#### 复杂度

- **时间复杂度**：`O((rows+cols)^{k-1} * rows * cols)`  
  解释：每一次递归都要遍历所有可能的切线（`rows+cols`），并且每次判断是否含苹果要遍历子矩阵（`rows*cols`），指数级增长，实际不可接受。
- **空间复杂度**：`O(k)`（递归栈深度），加上用于存放原始 pizza 的 `O(rows*cols)`。

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**有两个：

1. **大量重复的子矩阵检查**：同一个子矩阵会被多次调用 `has_apple`，导致 `O(rows*cols)` 的重复工作。  
2. **没有记忆化**：相同的状态 `(row, col, cuts)` 会被多次递归求解，导致指数级的重复计算。

我们可以通过**前缀和** + **记忆化搜索（或 DP）** 把这两个问题都解决掉。

---

##### 2.1 前缀和：快速判断子矩阵是否有苹果  

构造一个二维前缀和 `pre[i][j]`，表示从 `(i,j)` 到右下角 `(rows-1, cols-1)` 区域内苹果的数量。  
这样，任意子矩阵 `(r1,c1) ~ (r2,c2)`（这里我们只关心右下角固定在最右下）是否含苹果，只需要：

```python
apple_cnt = pre[r1][c1] - pre[r2+1][c1] - pre[r1][c2+1] + pre[r2+1][c2+1]
```

因为右下角总是 `(rows-1, cols-1)`，我们只需要查询 `(r,c)` 到右下的总数即可，写成更简洁的形式：

```python
has_apple = pre[r][c] > 0
```

> **类比**：前缀和就像一本图书的目录，告诉你从第几页到最后有多少章节，查找特定区间的章节数只需要看目录，不必逐页翻。

---

##### 2.2 DP 状态定义  

记 `dp[r][c][cuts]` 为：**从左上角坐标 `(r,c)` 开始，剩余的子 pizza（右下角固定在 `(rows-1,cols-1)`）在还需要 `cuts` 次切割时的合法切法数**。  

- **初始状态**：`cuts = 0` 时，只要子矩阵里还有苹果，就只有一种合法方式（不再切），即 `dp[r][c][0] = 1`；否则为 `0`。  
- **转移**：对于 `cuts > 0`，我们尝试所有合法的水平切和垂直切。  
  - **水平切**：在 `r'`（`r ≤ r' < rows-1`）处切，切掉上面的部分 `(r,c)~(r',cols-1)`。这块必须含苹果，即 `pre[r][c] - pre[r'+1][c] > 0`。如果合法，则剩下的部分从 `(r'+1, c)` 开始继续切 `cuts-1` 次，贡献 `dp[r'+1][c][cuts-1]` 种方式。  
  - **垂直切**：类似，在 `c'`（`c ≤ c' < cols-1`）处切，左边块必须含苹果，即 `pre[r][c] - pre[r][c'+1] > 0`，合法则加上 `dp[r][c'+1][cuts-1]`。

所有合法切法的和就是 `dp[r][c][cuts]`。

因为 `rows, cols ≤ 50`，`k ≤ 10`，状态总数是 `50 * 50 * 10 = 25000`，非常小，直接递归加记忆化或自底向上 DP 都可以。

---

##### 2.3 记忆化搜索（自顶向下）实现  

我们用一个三维数组 `memo` 保存已经算好的 `dp`，每次递归先检查是否已存在，若有直接返回，避免重复计算。

---

##### 2.4 代码（Python）

```python
MOD = 10**9 + 7

def ways_optimal(pizza, k):
    rows, cols = len(pizza), len(pizza[0])

    # ---------- 1. 构造右下角前缀和 ----------
    # pre[i][j] 表示从 (i,j) 到右下角的苹果总数
    pre = [[0] * (cols + 1) for _ in range(rows + 1)]
    for i in range(rows - 1, -1, -1):
        for j in range(cols - 1, -1, -1):
            pre[i][j] = (1 if pizza[i][j] == 'A' else 0) \
                        + pre[i + 1][j] + pre[i][j + 1] - pre[i + 1][j + 1]

    # ---------- 2. 记忆化搜索 ----------
    from functools import lru_cache

    @lru_cache(None)                         # 自动记忆化
    def dfs(r, c, cuts):
        """
        从左上角 (r,c) 开始，剩余的子 pizza 为右下角 (rows-1,cols-1)。
        还需要再切 cuts 次（即还要得到 cuts+1 块）。
        返回合法切法数。
        """
        # 若当前子矩阵没有苹果，直接返回 0
        if pre[r][c] == 0:
            return 0
        # 当不再需要切（cuts == 0）时，只要还有苹果就是一种合法方式
        if cuts == 0:
            return 1

        total = 0

        # -------- 水平切 --------
        # 尝试在每一条水平线 r' (r ≤ r' < rows-1) 处切
        for nr in range(r + 1, rows):
            # 上面那块 (r,c)~(nr-1,cols-1) 必须有苹果
            # 只要 pre[r][c] - pre[nr][c] > 0 即可
            if pre[r][c] - pre[nr][c] > 0:
                total += dfs(nr, c, cuts - 1)
                total %= MOD

        # -------- 垂直切 --------
        for nc in range(c + 1, cols):
            # 左边那块 (r,c)~(rows-1,nc-1) 必须有苹果
            if pre[r][c] - pre[r][nc] > 0:
                total += dfs(r, nc, cuts - 1)
                total %= MOD

        return total

    # 初始从 (0,0) 开始，需要切 k-1 次
    return dfs(0, 0, k - 1)
```

**关键行中文注释解释**：

- `pre[i][j] = ...`：从 `(i,j)` 到右下角累计苹果数，后面判断是否有苹果只看 `pre[i][j] > 0`。
- `@lru_cache(None)`：Python 的记忆化装饰器，自动把函数调用结果缓存，避免重复递归。
- `if pre[r][c] - pre[nr][c] > 0`：判断水平切上面的那块是否至少有一个苹果。
- `if pre[r][c] - pre[r][nc] > 0`：判断垂直切左边的那块是否至少有一个苹果。

#### 复杂度

- **时间复杂度**：`O(rows * cols * k)`  
  解释：状态数是 `rows * cols * k`（每个状态只遍历一次），每个状态内部遍历所有可能的切线，总共最多 `rows + cols ≤ 100`，所以整体仍然是常数级别乘以状态数，远小于暴力的指数级。  
  对于最大输入 `50 * 50 * 10 = 25000`，运行毫秒级。

- **空间复杂度**：`O(rows * cols * k)` 用于缓存 `dp`（记忆化表），加上前缀和的 `O(rows * cols)`，总体约 `O(rows * cols * k)`，约几万个整数，完全可以接受。

---

## 心得

- **核心技巧**：**二维前缀和 + 记忆化动态规划**。前缀和把“子矩阵是否含苹果”的判定降到 O(1)，记忆化 DP 把指数级的递归转化为多项式级别的状态转移。
- **适用题型**  
  1. **分割类 DP**：如 LeetCode 546. 移除盒子、1312. 让子数组和相等等，需要在区间上做多次切割。  
  2. **二维区间计数**：如 2242. 通过重复切分获得的最大利润、或者任意“在矩阵上切割满足条件”的题目。  
- **一句话总结解题钥匙**：  
  > **“先把‘这块里有苹果吗’变成 O(1) 查询，再用记忆化 DP 把所有可能的切法一次算完。”**

---

## 反思

- **第一反应**：看到“切 k 块，每块要有苹果”，本能想要**枚举所有切法**（暴力递归），这也是最自然的思路。  
- **最容易踩的坑**  
  1. **子矩阵判定重复**：每次切都遍历整块检查是否有苹果，会导致时间爆炸。  
  2. **边界条件**：切到最后一块时必须检查是否还有苹果；水平/垂直切线的循环要从 `r+1 / c+1` 开始，避免切到空的上/左块。  
  3. **模运算**：答案要求 `10⁹+7`，在每次累加时都要取模，否则会溢出。  
- **下次类似题的第一步**：  
  > **先构造前缀和（或其他 O(1) 区间查询结构）**，确认可以快速判断子区域是否满足约束，然后再决定使用记忆化 DP 还是自底向上 DP。这样可以把指数级的搜索直接压缩到多项式级别。