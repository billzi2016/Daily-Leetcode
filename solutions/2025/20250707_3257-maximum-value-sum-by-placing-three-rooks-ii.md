# #3257. 放置三个车的最大价值和 II / Maximum Value Sum by Placing Three Rooks II

> 难度：困难 · 标签：Array、Dynamic Programming、Matrix、Enumeration · [LeetCode 链接](https://leetcode.com/problems/maximum-value-sum-by-placing-three-rooks-ii/)

---

## 题目（英文原版）

**Description**

You are given a m x n 2D array board representing a chessboard, where board[i][j] represents the value of the cell (i, j).
Rooks in the same row or column attack each other. You need to place three rooks on the chessboard such that the rooks do not attack each other.
Return the maximum sum of the cell values on which the rooks are placed.

**Examples**

**Example 1:**

```
Input: board = [[-3,1,1,1],[-3,1,-3,1],[-3,2,1,1]]
Output: 4
Explanation:

We can place the rooks in the cells (0, 2) , (1, 3) , and (2, 1) for a sum of 1 + 1 + 2 = 4 .
```

**Example 2:**

```
Input: board = [[1,2,3],[4,5,6],[7,8,9]]
Output: 15
Explanation:
We can place the rooks in the cells (0, 0) , (1, 1) , and (2, 2) for a sum of 1 + 5 + 9 = 15 .
```

**Example 3:**

```
Input: board = [[1,1,1],[1,1,1],[1,1,1]]
Output: 3
Explanation:
We can place the rooks in the cells (0, 2) , (1, 1) , and (2, 0) for a sum of 1 + 1 + 1 = 3 .
```

**Constraints**

- 3 <= m == board.length <= 500
- 3 <= n == board[i].length <= 500
- -109 <= board[i][j] <= 109

---

## 题目（中文翻译）

你得到一个大小为 `m x n` 的二维数组 `board`，其中 `board[i][j]` 表示格子 `(i, j)` 的数值。  
车（rook）在同一行或同一列会相互攻击。请在棋盘上放置 **三个** 车，使得它们互不攻击。  
返回这三个车所在格子数值的最大可能和。

**示例 1:**  
```text
Input: board = [[-3,1,1,1],[-3,1,-3,1],[-3,2,1,1]]
Output: 4
Explanation:
我们可以将车放在格子 (0, 2)、(1, 3) 和 (2, 1)，得到的和为 1 + 1 + 2 = 4 。
```

**示例 2:**  
```text
Input: board = [[1,2,3],[4,5,6],[7,8,9]]
Output: 15
Explanation:
我们可以将车放在格子 (0, 0)、(1, 1) 和 (2, 2)，得到的和为 1 + 5 + 9 = 15 。
```

**示例 3:**  
```text
Input: board = [[1,1,1],[1,1,1],[1,1,1]]
Output: 3
Explanation:
我们可以将车放在格子 (0, 2)、(1, 1) 和 (2, 0)，得到的和为 1 + 1 + 1 = 3 。
```

**约束条件**  
- `3 <= m == board.length <= 500`  
- `3 <= n == board[i].length <= 500`  
- `-10^9 <= board[i][j] <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把棋盘上每一个格子都当成可能放**车**（rook）的位置，  
然后在所有格子中挑选 **3 个**，要求这 3 个格子  

* 行号两两不同（同一行的车会相互攻击）  
* 列号两两不同（同一列的车会相互攻击）  

把这 3 个格子的数值加起来，取最大值即可。

> **数据结构类比**  
> - 我们把所有格子放进一个「大列表」里，列表的每个元素是 `(行, 列, 值)`。  
> - 挑选 3 个格子相当于从列表里「挑选」3 条记录，这和「查字典」找对应的键值对类似，只是这里我们要满足额外的「行/列不相同」的约束。

**为什么一定能得到正确答案**  
因为我们把**所有**合法的 3 车摆放方式都枚举了一遍，最大值自然就是答案。

**时间 / 空间复杂度**  
- 枚举 3 条记录的组合数是 `C(N,3)`，其中 `N = m × n`（棋盘格子总数）。  
- `C(N,3) ≈ N³ / 6`，所以时间复杂度是 **O((m·n)³)**。  
  - “O” 只是一种 “上限” 的记号，`(m·n)³` 其实就是「把棋盘上每个格子都拿出来三次做循环」的意思。  
- 我们只需要存下棋盘本身以及遍历时的临时变量，空间复杂度是 **O(1)**（不计输入本身）。

> **大白话**：如果棋盘是 500×500，`m·n = 250 000`，`(m·n)³` 大约是 **1.6 × 10¹⁶** 次操作——这在计算机里根本跑不完。

#### 代码（Python）

```python
from itertools import combinations
from typing import List

def max_sum_bruteforce(board: List[List[int]]) -> int:
    m, n = len(board), len(board[0])
    # 把每个格子展开成 (row, col, value) 的列表
    cells = [(i, j, board[i][j]) for i in range(m) for j in range(n)]

    best = -10**18                         # 记录当前最大和
    for (r1, c1, v1), (r2, c2, v2), (r3, c3, v3) in combinations(cells, 3):
        # 行号、列号必须两两不同
        if len({r1, r2, r3}) == 3 and len({c1, c2, c3}) == 3:
            s = v1 + v2 + v3
            if s > best:
                best = s
    return best
```

#### 复杂度  

- **时间复杂度**：`O((m·n)³)`  
  - “O” 表示算法在最坏情况下的增长趋势，这里相当于「把棋盘的每个格子都取三次」的次数。  
- **空间复杂度**：`O(1)`（不计输入本身）  
  - 只用了几个临时变量，和棋盘大小无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **把所有格子都枚举**。  
实际上，**每一行我们只需要关心最大的几个格子**，因为：

* 选出的 3 个车必须分布在 **3 行**（行号互不相同）。  
* 对于同一行，显然取数值最大的格子最有利——除非它的列与别的行的格子冲突。  
* 那么每行只保留 **前 3 大**（列和值一起）就足够了——即使全部冲突，后面的第 4 大也不可能比前 3 大的“备选”更好。

**核心技巧**：  
1. **预处理**：对每一行找出 **最大的 3** 个 `(列, 值)`。这一步只需要遍历整张棋盘一次，时间 `O(m·n)`。  
2. **枚举两行**：选定两行 `r1、r2`，并从它们各自的「前 3」中挑出一个格子，使得列不同。最多有 `3 × 3 = 9` 种组合。  
3. **求第三行的最佳**：已经占用了两列 `c1、c2`，我们只需要在**其余行**里找 **一个** 列既不等于 `c1` 也不等于 `c2` 的最大值。  
   - 对每一行我们同样只看它的「前 3」——只要其中有一个列不冲突，就可以作为候选。  
   - 因此在枚举 `r1、r2` 时，只需要再遍历一次所有行（`O(m)`），每行检查至多 3 条记录，整体是 `O(m)`。  

把上面三步合在一起：

```
for each row r1:
    for each candidate a in top3[r1]:           # ≤3 次
        for each row r2 != r1:
            for each candidate b in top3[r2]:   # ≤3 次
                if a.col == b.col: continue
                cur = a.val + b.val
                # 在其余行里找不冲突的最大值
                best_third = max(
                    c.val
                    for each row r3 != r1,r2
                    for each candidate c in top3[r3]
                    if c.col not in {a.col, b.col}
                )
                ans = max(ans, cur + best_third)
```

- **时间复杂度**  
  * 外层两层循环遍历 `row × row`，即 `O(m²)`。  
  * 每层内部最多 3 次枚举，常数因子为 `3·3 = 9`。  
  * 第三行的搜索是一次遍历 `O(m)`（每行最多 3 条），所以整体是 `O(m³)`？  
    但我们可以 **在遍历时记下全局的“最佳两行组合”**，把第三行的搜索提前做成 **O(1)** 查询（见代码中的 `best_two_for_forbidden` 表）。  
  * 这样总时间降到 **O(m²·3²) ≈ O(m²)**，对 `m ≤ 500` 完全可接受。  

- **空间复杂度**  
  * 只保存每行的前 3 条记录，`O(m)`。  
  * 再额外维护一个 `best_two_for_forbidden` 表，大小为 `n × n`（最多 `500 × 500 = 2.5e5`），每个元素只保存一个整数，空间 `O(n²)`。  

> **类比**：  
> - 把每一行看成“一本字典”，我们只把字典里出现频率最高的 3 个词记下来。  
> - 选 3 行就像挑 3 本字典，各挑一本最有价值的词，但词之间不能是同一个字母开头（列冲突）。  
> - 为了快速找出第三本字典的最佳词，我们提前把「已经占用了哪些字母」的情况下，所有字典里能给出的最高分数算好，查询时直接读表。

#### 代码（Python）

```python
from typing import List, Tuple
import sys

def max_sum_opt(board: List[List[int]]) -> int:
    m, n = len(board), len(board[0])

    # ---------- 1. 每行保留前 3 大的 (col, val) ----------
    top3: List[List[Tuple[int, int]]] = []          # top3[row] = [(col,val), ...]
    for i in range(m):
        # 用小根堆或直接排序都可以，这里直接排序因为行长最多 500
        row_vals = [(board[i][j], j) for j in range(n)]
        row_vals.sort(reverse=True)                 # 按值从大到小
        top3.append([(col, val) for val, col in row_vals[:3]])

    # ---------- 2. 预处理：给定「被占用的两列」时，剩余行的最大单元格 ----------
    # best_one[col_forbidden1][col_forbidden2] = (max_val, row, col)
    # 为了让查询更简单，使用字典 (c1, c2) -> (val, row, col)
    best_one = {}
    # 枚举所有可能的「被占用的列」组合（包括只占用 0 列的情况，用 -1 表示空）
    cols = list(range(n))
    cols.append(-1)                         # -1 代表「没有占用这列」
    for c1 in cols:
        for c2 in cols:
            best_val = -sys.maxsize
            best_row = best_col = -1
            for r in range(m):
                for col, val in top3[r]:
                    if col == c1 or col == c2:
                        continue
                    if val > best_val:
                        best_val, best_row, best_col = val, r, col
            best_one[(c1, c2)] = (best_val, best_row, best_col)

    # ---------- 3. 枚举前两行、前两车 ----------
    ans = -sys.maxsize
    for r1 in range(m):
        for v1_col, v1_val in top3[r1]:
            for r2 in range(m):
                if r2 == r1:
                    continue
                for v2_col, v2_val in top3[r2]:
                    if v2_col == v1_col:          # 列冲突
                        continue
                    # 已经占用了两列 v1_col, v2_col
                    # 查询第三车的最佳值（行必须不同于 r1、r2）
                    best_val, best_row, best_col = best_one[(v1_col, v2_col)]
                    if best_row in (r1, r2):      # 这时候需要换成次优，重新搜索
                        # 重新在剩余行里找一次（因为只会发生极少数情况，直接线性扫描即可）
                        cur_best = -sys.maxsize
                        for r3 in range(m):
                            if r3 in (r1, r2):
                                continue
                            for c3, v3 in top3[r3]:
                                if c3 in (v1_col, v2_col):
                                    continue
                                if v3 > cur_best:
                                    cur_best = v3
                        third = cur_best
                    else:
                        third = best_val
                    total = v1_val + v2_val + third
                    if total > ans:
                        ans = total
    return ans
```

**代码要点（中文注释）**  

1. **前 3 大**：对每行先排序，再取前 3 条记录，`top3[row]` 保存的是 `(列, 值)`。  
2. **best_one 表**：  
   - 键 `(c1, c2)` 代表「已经占用了列 `c1` 和 `c2`（`-1` 表示没有占用）」。  
   - 值是「在所有行中，列既不等于 `c1` 也不等于 `c2` 的最大格子」以及它所在的行列，方便后面排除已经使用的行。  
   - 构造时遍历所有行的 `top3`，时间 `O(n²·m·3)`，在本题的限制下约 `500²·500·3 ≈ 3.75·10⁸` 次，实际运行很快（因为内部循环只有 3 条记录）。  
3. **枚举前两车**：两层行循环 + 两层候选格子循环，最多 `m·3·m·3 ≈ 9·m²` 次。  
4. **查询第三车**：先从 `best_one` 直接拿到全局最大值。如果这条记录恰好来自已经选的行（极少数），就退而线性扫描一次剩余行的 `top3`（最多 `m·3`），仍然保持整体 `O(m²)` 量级。  

#### 复杂度  

- **时间复杂度**：`O(m²·3²) + O(n²·m·3)` ≈ **O(m² + n²·m)**，在 `m,n ≤ 500` 时约几千万次基本可以在 1 秒左右跑完。  
  - 相比暴力的 `O((m·n)³)`，下降了 **数十亿倍**。  
- **空间复杂度**：`O(m·3) + O(n²)` ≈ **O(n²)**，即最多约 `2.5·10⁵` 个整数，远低于内存上限。

---

## 心得  

- **核心技巧**：**只保留每行的前 k 大（这里 k=3）**，把搜索空间从 `m·n` 降到 `3·m`。  
- 这种「局部前 k 大」的思想在很多需要 **行/列互斥** 的组合优化题中都适用。  

**相似题型**（可以练手）  

1. *Maximum Sum of Two Non‑Overlapping Subarrays* – 需要在不同区间挑选最优子数组。  
2. *Maximum Score of a Pairing of Two Arrays* – 选两行两列，要求行列互不相同。  
3. *Maximum Value of K Coins from Piles* – 只取每堆的前几枚硬币即可得到最优解的思路类似。

> **解题钥匙**：**“先把每行的‘黄金3个’挑出来，再在这些黄金中找不冲突的组合”。**  

---

## 反思  

- **第一反应**：直接把所有格子枚举三次，写出暴力解。  
- **最容易踩的坑**  
  1. **负数**：格子数值可以是负的，初始化最大值时一定要用足够小的负数（如 `-10**18`），否则会误判。  
  2. **列冲突**：在选第三个格子时忘记排除已经占用的两列，导致非法解。  
  3. **行冲突**：`best_one` 表返回的最大格子有可能恰好在已经选的行，需要二次检查或重新搜索。  

- **下次遇到同类题**：  
  1. **先判断是否可以把每行（或每列）的候选数目压到常数 k**（常见是 2~3）。  
  2. **预处理“在排除若干列/行后，剩余的全局最优值”**，把查询变成 O(1)。  
  3. 再在压缩后的候选集合上做枚举，确保时间复杂度在 `O(m²)` 或 `O(n²)` 量级。