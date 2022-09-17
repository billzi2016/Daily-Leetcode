# #1937. 带费用的最大点数 / Maximum Number of Points with Cost

> 难度：中等 · 标签：Array、Dynamic Programming、Matrix · [LeetCode 链接](https://leetcode.com/problems/maximum-number-of-points-with-cost/)

---

## 题目（英文原版）

**Description**

You are given an m x n integer matrix points (0-indexed). Starting with 0 points, you want to maximize the number of points you can get from the matrix.
To gain points, you must pick one cell in each row. Picking the cell at coordinates (r, c) will add points[r][c] to your score.
However, you will lose points if you pick a cell too far from the cell that you picked in the previous row. For every two adjacent rows r and r + 1 (where 0 <= r < m - 1), picking cells at coordinates (r, c1) and (r + 1, c2) will subtract abs(c1 - c2) from your score.
Return the maximum number of points you can achieve.
abs(x) is defined as:

**Examples**

**Example 1:**

```
Input: points = [[1,2,3],[1,5,1],[3,1,1]]
Output: 9
Explanation:
The blue cells denote the optimal cells to pick, which have coordinates (0, 2), (1, 1), and (2, 0).
You add 3 + 5 + 3 = 11 to your score.
However, you must subtract abs(2 - 1) + abs(1 - 0) = 2 from your score.
Your final score is 11 - 2 = 9.
```

**Example 2:**

```
Input: points = [[1,5],[2,3],[4,2]]
Output: 11
Explanation:
The blue cells denote the optimal cells to pick, which have coordinates (0, 1), (1, 1), and (2, 0).
You add 5 + 3 + 4 = 12 to your score.
However, you must subtract abs(1 - 1) + abs(1 - 0) = 1 from your score.
Your final score is 12 - 1 = 11.
```

**Constraints**

- m == points.length
- n == points[r].length
- 1 <= m, n <= 105
- 1 <= m * n <= 105
- 0 <= points[r][c] <= 105

---

## 题目（中文翻译）

你得到一个大小为 `m × n` 的整数矩阵 `points`（0 索引）。初始分数为 0，目标是从矩阵中获得的总分最大化。

**获取分数的规则**  
- 需要在每一行中选取恰好一个单元格。选取坐标为 `(r, c)` 的单元格会将 `points[r][c]` 加入你的得分。  
- 若相邻的两行 `r` 与 `r + 1`（其中 `0 ≤ r < m - 1`）中选取的单元格分别为 `(r, c1)` 和 `(r + 1, c2)`，则需要扣除 `abs(c1 - c2)`（`abs(x)` 表示绝对值）作为费用。

返回能够得到的最大总分。

**示例 1**  
**示例 2**  
（题目中给出的 `abs(x)` 定义略）

---

## 示例

### 示例 1
**输入**  
```text
points = [[1,2,3],[1,5,1],[3,1,1]]
```
**输出**  
```text
9
```
**解释**  
蓝色单元格表示最优的选取位置，坐标分别为 `(0, 2)`、`(1, 1)`、`(2, 0)`。  
加分部分：`3 + 5 + 3 = 11`。  
扣除费用：`abs(2 - 1) + abs(1 - 0) = 2`。  
最终得分为 `11 - 2 = 9`。

### 示例 2
**输入**  
```text
points = [[1,5],[2,3],[4,2]]
```
**输出**  
```text
11
```
**解释**  
蓝色单元格表示最优的选取位置，坐标分别为 `(0, 1)`、`(1, 1)`、`(2, 0)`。  
加分部分：`5 + 3 + 4 = 12`。  
扣除费用：`abs(1 - 1) + abs(1 - 0) = 1`。  
最终得分为 `12 - 1 = 11`。

---

## 约束条件

- `m == points.length`
- `n == points[r].length`
- `1 ≤ m, n ≤ 10^5`
- `1 ≤ m × n ≤ 10^5`
- `0 ≤ points[r][c] ≤ 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是**逐行枚举**我们在每一行选的列，然后把所有可能的组合都算一遍，取最大的总分。  

- **数据结构**：我们只需要一个二维数组 `points`（题目已经给出）以及一个一维数组 `dp` 来记录“到当前行、选了第 j 列时的最高得分”。可以把 `dp` 想象成 **记事本**，每一页（下标 j）记下“如果这时选第 j 列，最好的得分是多少”。  
- **为什么正确**：因为题目要求**每行恰好选一个格子**，而我们枚举了所有可能的选法（每行的列数从 0 到 n‑1），所以一定会包含最优解。  
- **时间/空间复杂度**：  
  - 对第 i 行的每个列 j，要检查前一行的所有列 k，计算 `dp_prev[k] - |j-k|`，这一步是 **O(n)**。  
  - 整体要遍历 m 行，每行 n 列，且每次都要遍历前一行的 n 列，所以时间复杂度是 **O(m·n²)**。如果把 m、n 都记成 N，时间就是 **O(N³)**，在最坏情况下会非常慢。  
  - 我们只需要保存前一行的 `dp`，所以空间是 **O(n)**（记事本只有一页的大小）。  

> **大白话解释**：  
> - O(n²) 就像你在找一对好朋友：你要把每个人（n）都和所有其他人（n）比较一次，比较次数是 n × n。  
> - O(m·n²) 则是把每一行都这么比较一次，工作量更大。

#### 代码（Python）  
```python
from typing import List

def maxPoints_bruteforce(points: List[List[int]]) -> int:
    m, n = len(points), len(points[0])
    # dp[j] 表示到当前行、选第 j 列时的最高得分
    dp = [0] * n

    # 第 0 行直接加上分数，因为没有前一行的惩罚
    for j in range(n):
        dp[j] = points[0][j]

    # 从第 1 行开始逐行处理
    for i in range(1, m):
        new_dp = [float('-inf')] * n   # 用 -inf 表示还没有算出答案
        for j in range(n):             # 当前行选第 j 列
            best = float('-inf')
            for k in range(n):         # 前一行选第 k 列
                # 前一行的得分 - 位置差距的惩罚
                cand = dp[k] - abs(j - k)
                if cand > best:
                    best = cand
            # 加上本格子的分数
            new_dp[j] = points[i][j] + best
        dp = new_dp                    # 把本行的结果当作下一行的前一行
    return max(dp)                     # 所有列中最大的就是答案
```

#### 复杂度  
- **时间复杂度**：`O(m·n²)` —— 每行的每个列都要和前一行的所有列比较一次。  
- **空间复杂度**：`O(n)` —— 只保存两行的 DP 数组，相当于一本只记录当前页的记事本。  

---

### 2. 最优解  

#### 思路  
从暴力解可以看到 **瓶颈** 出在内层的 `for k in range(n)`：我们每次都要遍历前一行的所有列来求 `dp_prev[k] - |j-k|` 的最大值。  
如果能够 **在 O(1) 时间内得到** `max_k (dp_prev[k] - |j-k|)`，整体复杂度就会降到 `O(m·n)`。  

**关键观察**  
`|j - k|` 可以拆成两种情况：  

|j - k| =  
- `j - k` 当 `k ≤ j`（前面的列）  
- `k - j` 当 `k ≥ j`（后面的列）

于是：

```
dp_prev[k] - |j-k|
= max( dp_prev[k] - (j-k) , dp_prev[k] - (k-j) )
= max( (dp_prev[k] + k) - j , (dp_prev[k] - k) + j )
```

对固定的 `j`，我们只需要知道：

- **左侧最大值** `L = max_{k ≤ j} (dp_prev[k] + k)`  
- **右侧最大值** `R = max_{k ≥ j} (dp_prev[k] - k)`

然后 `max_k (dp_prev[k] - |j-k|) = max(L - j, R + j)`。  

**如何在 O(n) 内得到 L、R**？  
- **左到右扫描**：维护一个变量 `best`，它始终保存 `dp_prev[k] + k` 的最大值（只考虑已经遍历过的 k，即 `k ≤ j`）。遍历时把 `best - j` 记在 `left[j]`。  
- **右到左扫描**：同理，维护 `best` 保存 `dp_prev[k] - k` 的最大值（只考虑 `k ≥ j`），遍历时把 `best + j` 记在 `right[j]`。  

这样，`left[j]` 与 `right[j]` 分别对应左侧、右侧的最佳贡献，取两者的最大值即可得到 `max_k (dp_prev[k] - |j-k|)`。  

**完整步骤**  

1. 初始化 `dp = points[0]`（第 0 行没有惩罚）。  
2. 对每一行 `i = 1 … m-1`：  
   - 先用两次线性扫描得到 `left`、`right`（每个都是长度 n 的数组）。  
   - 对每列 `j`，计算 `best_prev = max(left[j], right[j])`，再加上本格子的分数 `points[i][j]`，得到新一行的 `dp[j]`。  
3. 最后返回 `max(dp)`。  

**类比**：  
把 `dp_prev` 想成一排学生的成绩，`k` 是他们的座位号。老师想要选一个座位 `j`，并且想要把“成绩 - 距离”最大化。老师先从左往右记录“最高成绩 + 座位号”，再从右往左记录“最高成绩 - 座位号”，这样在任何座位 `j` 都能快速算出最佳值。  

#### 代码（Python）  
```python
from typing import List

def maxPoints(points: List[List[int]]) -> int:
    """
    动态规划 + 两次线性扫描（前缀最大 & 后缀最大）
    时间复杂度 O(m * n) ，空间复杂度 O(n)
    """
    m, n = len(points), len(points[0])
    # dp[j] 表示到当前行、选第 j 列时的最高得分
    dp = points[0][:]                     # 第 0 行直接复制

    for i in range(1, m):
        left = [0] * n
        right = [0] * n

        # -------- 左到右扫描，维护 max(dp[k] + k) ----------
        best = dp[0] + 0                  # k = 0 时的初始值
        left[0] = best - 0                # left[0] = best - j (j==0)
        for j in range(1, n):
            # 更新 best 为已遍历的 k 中的最大 (dp[k] + k)
            best = max(best, dp[j] + j)
            left[j] = best - j            # 对应公式 L - j

        # -------- 右到左扫描，维护 max(dp[k] - k) ----------
        best = dp[-1] - (n - 1)           # k = n-1 时的初始值
        right[-1] = best + (n - 1)        # right[-1] = best + j (j==n-1)
        for j in range(n - 2, -1, -1):
            best = max(best, dp[j] - j)
            right[j] = best + j           # 对应公式 R + j

        # 结合两侧的最优值，加上本行的分数，得到新一行的 dp
        new_dp = [0] * n
        for j in range(n):
            best_prev = max(left[j], right[j])   # 前一行的最佳贡献
            new_dp[j] = points[i][j] + best_prev
        dp = new_dp

    return max(dp)
```

#### 复杂度  
- **时间复杂度**：`O(m·n)` —— 每行只做两次线性扫描和一次遍历，所有操作都是 `O(1)` 的。相比暴力的 `O(m·n²)`，速度提升了 **n 倍**。  
- **空间复杂度**：`O(n)` —— 只保存当前行的 `dp`、`left`、`right` 三个长度为 n 的数组，相当于只需要一页记事本和两行临时笔记。  

---

## 心得  

- **核心技巧**：把带绝对值的转移式拆解为两部分，利用前缀最大/后缀最大（单调扫描）实现 **线性时间** 的 DP 优化。  
- **适用题型**：  
  1. “每行选一个，代价与列距有关” 如本题、LeetCode 1937 *Maximum Number of Points with Cost*。  
  2. “二维网格上移动，移动代价是 |x‑y|” 类似的路径最大化/最小化问题。  
  3. “一维数组 DP，转移式中出现 `|i-j|`” 的所有情况（如某些滑动窗口 DP）。  
- **一句话总结**：**把 `|j-k|` 拆成两种线性形式，分别维护左侧 `dp+k` 与右侧 `dp‑k` 的最大值，即可在 O(1) 内完成原本 O(n) 的转移。**  

---

## 反思  

- **第一反应**：看到“每行必须选一个，行间要扣列距”，立刻想到普通的 DP `dp[i][j] = points[i][j] + max_k(dp[i‑1][k] - |j‑k|)`，于是写出暴力实现。  
- **最容易踩的坑**：  
  - **边界**：左到右扫描时要先处理 `j=0`，右到左扫描时要先处理 `j=n-1`，否则会出现未初始化的值。  
  - **整数溢出**：虽然 Python 整数不溢出，但在其他语言需要使用足够大的类型（`long long`）。  
  - **空间**：若直接开二维 DP `dp[m][n]`，会超出 `1e5` 的限制；应只保留前一行。  
- **下次遇到同类题**：第一步就检查转移式里是否有形如 `- |i-j|`（或 `+ |i-j|`）的项，尝试把它拆成 `+/- i +/- j` 的形式，随后用前缀/后缀最大或单调队列等技巧把 `O(n²)` 降到 `O(n)`。