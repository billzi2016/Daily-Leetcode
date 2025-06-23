# #3239. 二进制网格回文化的最少翻转次数 I / Minimum Number of Flips to Make Binary Grid Palindromic I

> 难度：中等 · 标签：Array、Two Pointers、Matrix · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-flips-to-make-binary-grid-palindromic-i/)

---

## 题目（英文原版）

**Description**

You are given an m x n binary matrix grid.
A row or column is considered palindromic if its values read the same forward and backward.
You can flip any number of cells in grid from 0 to 1, or from 1 to 0.
Return the minimum number of cells that need to be flipped to make either all rows palindromic or all columns palindromic.

**Examples**

**Example 1:**

```
Input: grid = [[1,0,0],[0,0,0],[0,0,1]]
Output: 2
Explanation:

Flipping the highlighted cells makes all the rows palindromic.
```

**Example 2:**

```
Input: grid = [[0,1],[0,1],[0,0]]
Output: 1
Explanation:

Flipping the highlighted cell makes all the columns palindromic.
```

**Example 3:**

```
Input: grid = [[1],[0]]
Output: 0
Explanation:
All rows are already palindromic.
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m * n <= 2 * 105
- 0 <= grid[i][j] <= 1

---

## 题目（中文翻译）

给定一个大小为 `m x n` 的二进制矩阵 `grid`。  
如果一行或一列的值正读和反读相同，则称其为回文的（palindromic）。  
你可以将任意数量的单元格的值从 `0` 翻转为 `1`，或从 `1` 翻转为 `0`。  
返回使 **所有行** 回文或 **所有列** 回文所需翻转的最少单元格数。

#### 示例  

**示例 1**  
```
Input: grid = [[1,0,0],[0,0,0],[0,0,1]]
Output: 2
Explanation:
翻转标记的单元格后，所有行都成为回文。
```

**示例 2**  
```
Input: grid = [[0,1],[0,1],[0,0]]
Output: 1
Explanation:
翻转标记的单元格后，所有列都成为回文。
```

**示例 3**  
```
Input: grid = [[1],[0]]
Output: 0
Explanation:
所有行已经是回文，无需翻转。
```

#### 约束条件
- `m == grid.length`
- `n == grid[i].length`
- `1 <= m * n <= 2 * 10^5`
- `0 <= grid[i][j] <= 1`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直观的想法是**把每一行（或每一列）都当成一个独立的回文检查**，  
一旦发现某一对位置的数字不相同，就**随意翻转左边或右边的格子**，  
把所有可能的翻转组合都枚举一遍，挑出翻转次数最少的那一种。

> **类比**：把每一行想成一本书的两页，左页和右页的文字必须相同。  
> 当左页写错了（0 与 1 不同），我们可以把左页改成右页的内容，也可以把右页改成左页的内容。  
> 只要把所有可能的改法都列出来，挑出改动最少的方案，就是答案。

这种做法 **一定能得到正确答案**，因为我们把所有合法的翻转方式都尝试了一遍。  
但是它的搜索空间非常大：

- 每出现一次「不相等」的两格，就有 **两种选择**（翻左或翻右）。  
- 如果整张矩阵里出现了 `k` 对不相等的格子，枚举所有可能需要检查 `2^k` 种情况。

当矩阵稍大一点（比如 `m·n = 20`）时，`k` 可能已经达到 10 以上，`2^k` 就已经是几千甚至几万次遍历，  
更大的输入（本题最高 `2·10⁵` 个格子）根本不可能在合理时间内完成。

#### 代码（Python）

```python
from copy import deepcopy
from typing import List

def min_flips_bruteforce(grid: List[List[int]]) -> int:
    """
    暴力递归枚举所有翻转方案（仅作概念展示，实际会超时）。
    """
    m, n = len(grid), len(grid[0])
    ans = float('inf')

    # ---------- 检查所有行是否回文 ----------
    def rows_palindrome(g: List[List[int]]) -> bool:
        for row in g:
            if row != row[::-1]:          # 直接比较正序和逆序
                return False
        return True

    # ---------- 检查所有列是否回文 ----------
    def cols_palindrome(g: List[List[int]]) -> bool:
        for c in range(n):
            col = [g[r][c] for r in range(m)]
            if col != col[::-1]:
                return False
        return True

    # ---------- 递归尝试每一个格子的翻转 ----------
    def dfs(i: int, j: int, flips: int, cur: List[List[int]]):
        nonlocal ans
        # 剪枝：已经超过当前最小答案，直接返回
        if flips >= ans:
            return
        # 到达矩阵末尾，检查是否满足条件
        if i == m:
            if rows_palindrome(cur) or cols_palindrome(cur):
                ans = min(ans, flips)
            return
        # 计算下一个格子的位置
        ni, nj = (i, j + 1) if j + 1 < n else (i + 1, 0)

        # 1) 不翻转当前格子
        dfs(ni, nj, flips, cur)

        # 2) 翻转当前格子（0↔1）
        cur[i][j] ^= 1          # 位运算取反
        dfs(ni, nj, flips + 1, cur)
        cur[i][j] ^= 1          # 恢复原状，回溯

    dfs(0, 0, 0, deepcopy(grid))
    return ans
```

> **关键行中文注释**  
> - `row != row[::-1]`：判断一行是否是回文，`[::-1]` 是列表的逆序。  
> - `cur[i][j] ^= 1`：把 `0` 变成 `1`，`1` 变成 `0`（异或 1）。  
> - `if flips >= ans: return`：如果已经翻得比当前最小答案多，直接剪枝，省掉后面的递归。

#### 复杂度  

- **时间复杂度**：`O(2^k)`，其中 `k` 是矩阵中「不相等」的格子对数。  
  这相当于「指数级」增长，`k` 增加 1，计算量就会翻倍。  
- **空间复杂度**：`O(m·n)` 用于递归栈和拷贝矩阵，最坏情况下等同于矩阵本身的大小。

> **大白话**：暴力解的时间像是「翻硬币」——每次遇到不匹配就要再抛一次硬币决定翻哪一边，次数会很快爆炸，根本不适合大数据。

---

### 2. 最优解

#### 思路  

从暴力解可以看出 **瓶颈** 在于 **每一对不相等的格子我们都要枚举两种翻法**。  
其实这两种翻法的代价是一样的：  
- 若 `grid[i][j] != grid[i][n-1-j]`，无论把左边翻成右边，还是把右边翻成左边，**都只需要一次翻转**。  
- 所以我们根本不需要去「决定」翻哪一格，只要统计「有多少对不相等」就行了。

**核心观察**：

1. **行回文**  
   - 对每一列对 `(j, n-1-j)`（左‑右配对），遍历所有行 `i`。  
   - 若 `grid[i][j] != grid[i][n-1-j]`，这行在这两个位置上必须翻一次。  
   - 所有行的翻转次数累加，即得到把 **所有行** 变成回文所需的最少翻转数。

2. **列回文**  
   - 同理，对每一行对 `(i, m-1-i)`（上‑下配对），遍历所有列 `j`。  
   - 若 `grid[i][j] != grid[m-1-i][j]`，这列在这两个位置上必须翻一次。  
   - 累加得到把 **所有列** 变成回文的最少翻转数。

3. **取最小**  
   - 题目要求「行全回文」或「列全回文」任意一种即可，取两者的最小值即为答案。

> **类比**：把矩阵想成一块棋盘，行回文就像要求每一行的左右两侧镜像相同；  
> 列回文则是要求上下两侧镜像相同。我们只需要数出每一对「不对称」的格子有多少对，  
> 因为每对只需要「调和」一次，就能让对应的行（或列）满足镜像条件。

#### 代码（Python）

```python
from typing import List

def minFlips(grid: List[List[int]]) -> int:
    """
    统计使所有行回文或所有列回文所需的最少翻转次数。
    时间 O(m * n) ，空间 O(1)。
    """
    m, n = len(grid), len(grid[0])

    # ---------- 计算让所有行成为回文的翻转次数 ----------
    flips_rows = 0
    # 只需要遍历左半边的列 (j, n-1-j)
    for j in range(n // 2):
        opposite = n - 1 - j
        for i in range(m):
            if grid[i][j] != grid[i][opposite]:
                flips_rows += 1          # 这行在这两个位置必须翻一次

    # ---------- 计算让所有列成为回文的翻转次数 ----------
    flips_cols = 0
    # 只需要遍历上半边的行 (i, m-1-i)
    for i in range(m // 2):
        opposite = m - 1 - i
        for j in range(n):
            if grid[i][j] != grid[opposite][j]:
                flips_cols += 1          # 这列在这两个位置必须翻一次

    # ---------- 取最小 ----------
    return min(flips_rows, flips_cols)
```

**关键行中文注释**  

- `for j in range(n // 2):`：只遍历左半边列，右半边是它的镜像。  
- `if grid[i][j] != grid[i][opposite]:`：判断同一行的左右对应格子是否相同。  
- `flips_rows += 1`：不相等就必须翻一次，具体翻哪格不影响总次数。  
- 同理，`for i in range(m // 2):` 只遍历上半边行，检查上下对应格子。  

#### 复杂度  

- **时间复杂度**：`O(m·n)`  
  - 我们只遍历矩阵两次（一次按列配对，一次按行配对），每个格子最多被检查一次。  
  - 与矩阵大小线性相关，能够轻松处理题目给出的 `2·10⁵` 上限。  

- **空间复杂度**：`O(1)`  
  - 只使用了几个整数计数器，不会随输入规模增长而增加额外的数组或递归栈。

> **对比**：暴力解是指数级 `2^k`，最优解只需线性 `m·n`，相当于把「每对不匹配」的两种选择压缩成「只算一次」，效率提升了 **天文数字**。

---

## 心得

- **核心技巧**：**配对统计**（把矩阵的左右或上下对应格子配对，只统计不相等的对数）。  
- **适用的题型**：  
  1. **“使所有行/列回文”** 类似题目（如 *Minimum Number of Flips to Make Binary Grid Palindromic II*）。  
  2. **“矩阵对称”** 检查与最小修改（如 *Make Matrix Symmetric*）。  
  3. **“镜像匹配”** 的一维/二维字符串或数组问题（如 *Minimum Deletions to Make a String Palindrome*）。  
- **一句话总结**：**每对不相等只需一次翻转，直接计数即得最优解。**

---

## 反思

- **第一反应**：想到要把每行（或每列）逐个检查回文，结果是要遍历所有格子。  
- **最容易踩的坑**：  
  - 忘记 **只遍历一半**（左半边列或上半边行），导致重复计数，使答案翻倍。  
  - 处理奇数维度时忘记中间那一列（或行）不需要配对。  
  - 把行回文和列回文的计数混在一起，忘记分别取最小值。  
- **下次类似题的第一步**：**先确定配对规则**（左‑右或上‑下），把配对后不相等的数量统计出来，答案往往就是这数量的最小值。