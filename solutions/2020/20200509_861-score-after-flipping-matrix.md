# #861. **翻转矩阵后的得分** / Score After Flipping Matrix

> 难度：中等 · 标签：Array、Greedy、Bit Manipulation、Matrix · [LeetCode 链接](https://leetcode.com/problems/score-after-flipping-matrix/)

---

## 题目（英文原版）

**Description**

You are given an m x n binary matrix grid.
A move consists of choosing any row or column and toggling each value in that row or column (i.e., changing all 0's to 1's, and all 1's to 0's).
Every row of the matrix is interpreted as a binary number, and the score of the matrix is the sum of these numbers.
Return the highest possible score after making any number of moves (including zero moves).

**Examples**

**Example 1:**

```
Input: grid = [[0,0,1,1],[1,0,1,0],[1,1,0,0]]
Output: 39
Explanation: 0b1111 + 0b1001 + 0b1111 = 15 + 9 + 15 = 39
```

**Example 2:**

```
Input: grid = [[0]]
Output: 1
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 20
- grid[i][j] is either 0 or 1.

---

## 题目（中文翻译）

你得到一个 `m x n` 的二进制矩阵 `grid`。  
一次操作可以选择任意一行或一列，将该行或该列中的每个值取反（即把所有 `0` 变成 `1`，所有 `1` 变成 `0`）。  

矩阵的每一行被视作一个二进制数，矩阵的 **得分（score）** 定义为这些二进制数的和。  
返回在进行任意次数的操作（可以为零次）后可能得到的最高得分。

**示例 1**  
```text
输入: grid = [[0,0,1,1],[1,0,1,0],[1,1,0,0]]
输出: 39
解释: 0b1111 + 0b1001 + 0b1111 = 15 + 9 + 15 = 39
```

**示例 2**  
```text
输入: grid = [[0]]
输出: 1
```

**约束条件**  
- `m == grid.length`  
- `n == grid[i].length`  
- `1 <= m, n <= 20`  
- `grid[i][j]` 只能是 `0` 或 `1`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的翻转操作都枚举一遍**，然后计算每种情况下矩阵的得分，取最大的那个。  
- **翻转行/列**：一次翻转相当于把选中的那一行（或列）里的每个 `0` 变成 `1`，每个 `1` 变成 `0`。这就像把一串开关全部拨到相反的位置。  
- **全部枚举**：我们可以把每一行是否翻转记成一个布尔值（`0` 表示不翻，`1` 表示翻），同理每一列也记成一个布尔值。于是总共有 `2^(m) * 2^(n) = 2^(m+n)` 种不同的翻转组合。  
- **计算得分**：翻转完以后，把每一行当成二进制数（左边是最高位），把所有行的数值相加，就是矩阵的得分。  

> **为什么正确**  
> 因为我们穷举了**所有**可能的翻转方式，最高得分一定出现在这其中的某一种组合里。只要遍历完全部组合并记录最大值，就一定能得到答案。

#### 代码（Python）

```python
from itertools import product
from copy import deepcopy

def matrix_score_bruteforce(grid):
    """
    暴力枚举所有行、列的翻转方式，返回最大得分
    """
    m, n = len(grid), len(grid[0])
    best = 0

    # row_flip[i] = 0/1 表示第 i 行是否翻转，col_flip[j] 同理
    for row_flip in product([0, 1], repeat=m):
        for col_flip in product([0, 1], repeat=n):
            # 深拷贝一份原矩阵，避免修改原数据
            g = deepcopy(grid)

            # 翻转行
            for i in range(m):
                if row_flip[i]:
                    for j in range(n):
                        g[i][j] ^= 1          # 0->1, 1->0，使用异或更简洁

            # 翻转列
            for j in range(n):
                if col_flip[j]:
                    for i in range(m):
                        g[i][j] ^= 1

            # 计算当前矩阵的得分
            total = 0
            for i in range(m):
                # 把第 i 行当作二进制数转成十进制
                row_val = 0
                for j in range(n):
                    row_val = (row_val << 1) | g[i][j]   # 左移一位后加当前位
                total += row_val

            best = max(best, total)   # 记录最大得分

    return best
```

#### 复杂度

- **时间复杂度**：`O(2^(m+n) * m * n)`  
  解释：我们要遍历 `2^(m+n)` 种翻转组合，每种组合里要对矩阵的每个元素（`m*n`）做翻转或读取操作，最后再把每行的二进制转十进制（同样是 `m*n`），所以整体是指数级的。对于 `m,n ≤ 20`，最坏情况是 `2^40`，根本不可算。

- **空间复杂度**：`O(m * n)`  
  解释：主要是存放一份拷贝的矩阵 `g`，大小和原矩阵一样。其余的辅助空间（比如 `row_flip`、`col_flip`）都是常数级的。

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于“枚举所有翻转组合”。我们可以观察到，矩阵得分只与每一列中出现的 `1` 的数量有关，而不是具体是哪一行翻了。利用这一点可以 **贪心** 地一步步构造最优的翻转方案，而不必尝试所有组合。

1. **最高位一定要是 1**  
   二进制数的左边是最高位，权值最大（`2^(n-1)`）。如果某行的最高位是 `0`，把整行翻转一次就能把它变成 `1`，而且不会影响其他列的相对比例。  
   → **操作**：遍历所有行，如果 `grid[i][0] == 0` 就翻转整行。此时第一列全变成 `1`，为后面的优化奠定基础。

2. **列独立决策**  
   在第一列固定为 `1` 之后，其他列的翻不翻只会影响该列中 `1` 的数量。因为每列的权值是固定的（第 `j` 列的权值是 `2^(n-1-j)`），我们希望该列的 `1` 越多越好。  
   - 统计第 `j` 列当前有多少个 `1`（记为 `cnt1`）。  
   - 如果把整列翻转，`1` 的数量会变成 `m - cnt1`。  
   - 取两者的最大值 `max(cnt1, m - cnt1)`，就是这列在最优情况下能够贡献的 `1` 的个数。  
   → **操作**：对每一列（从第 1 列到第 n‑1 列），计算 `cnt1`，决定是否“假装”翻转列，使 `1` 的数量最大。

3. **直接累计得分**  
   既然我们已经知道每列最终会有多少个 `1`，就可以直接把它们乘以对应的二进制权值累加，得到最大可能的总分。无需真的去翻转列，只要把 “翻不翻” 的决定转化为计数即可。

> **为什么贪心有效**  
> - 第一步把最高位全部变成 `1` 是必然的，因为最高位的权值是所有其他位之和的 **至少两倍**，不把它们变成 `1` 就永远不可能是最优。  
> - 第二步每列的决策互不影响：翻一列只会把该列的 `0`/`1` 互换，不会改变别的列的 `0`/`1` 分布，也不影响已经固定好的最高位。于是每列可以独立地选择“让 `1` 多一点”，这正是贪心的本质。

#### 代码（Python）

```python
def matrix_score(grid):
    """
    贪心算法：先保证第一列全为 1，再对每列独立决定是否翻转，使 1 的数量最大。
    返回翻转后可能得到的最高得分。
    """
    m, n = len(grid), len(grid[0])

    # 1️⃣ 把所有第一列为 0 的行翻转，使第一列全变成 1
    for i in range(m):
        if grid[i][0] == 0:               # 需要翻转整行
            for j in range(n):
                grid[i][j] ^= 1           # 行翻转：0<->1

    # 2️⃣ 逐列计算最大贡献
    total_score = 0
    for j in range(n):
        cnt1 = 0
        for i in range(m):
            cnt1 += grid[i][j]            # 统计第 j 列当前有多少个 1

        # 如果翻列，1 的数量会变成 m - cnt1，取两者较大者
        max_ones = max(cnt1, m - cnt1)

        # 第 j 列的二进制权值是 2^(n-1-j)（左边是高位）
        col_value = max_ones * (1 << (n - 1 - j))
        total_score += col_value

    return total_score
```

#### 复杂度

- **时间复杂度**：`O(m * n)`  
  解释：  
  - 第一次遍历所有行并可能翻转每行，最多访问 `m * n` 次元素。  
  - 第二次遍历每列统计 `1` 的数量，同样是 `m * n` 次访问。  
  整体是线性时间，对 `m,n ≤ 20` 完全轻松。

- **空间复杂度**：`O(1)`（不计输入矩阵本身）  
  解释：只用了若干个整数计数器和一个返回值，没有额外的与 `m,n` 成正比的存储。

---

## 心得

- **核心技巧**：先把最高位全部变成 `1`（贪心的必然步骤），随后对每列独立决定是否翻转，使 `1` 的数量最大。  
- **适用场景**：  
  1. “把矩阵的每行视作二进制数求和” 类似题目，如 **LeetCode 861. Score After Flipping Matrix**（本题）。  
  2. 需要对行/列独立做最优决策的题目，例如 **LeetCode 1005. Maximize Sum Of Array After K Negations**（单向贪心）。  
  3. “把二进制位的权值最大化” 的变体，如 **LeetCode 1690. Stone Game VII**（虽然是游戏，但也涉及局部最优决定）。  
- **一句话总结解题钥匙**：**最高位先抢占，后面每列只争取最多的 1**。

---

## 反思

- **第一反应**：想到“枚举所有翻转方式”，这在没有任何约束时是最自然的暴力思路。  
- **最容易踩的坑**：  
  - 忘记先把第一列全部变成 `1`，导致后面的列计数不准确。  
  - 直接在计数后再去真的翻列，可能会破坏已经处理好的前面列，必须保证列的决策是独立的。  
  - 对二进制权值的计算出错（左移的位数写反），导致最终得分偏小。  
- **下次类似题的第一步**：**先找出权值最大的维度（通常是最高位）并强制把它最大化**，随后再考虑其他维度的局部最优。这样往往可以把搜索空间从指数级压到线性级。