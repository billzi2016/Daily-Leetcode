# #2711. 对角线上不同值数量的差值 / Difference of Number of Distinct Values on Diagonals

> 难度：中等 · 标签：Array、Hash Table、Matrix · [LeetCode 链接](https://leetcode.com/problems/difference-of-number-of-distinct-values-on-diagonals/)

---

## 题目（英文原版）

**Description**

Given a 2D grid of size m x n, you should find the matrix answer of size m x n.
The cell answer[r][c] is calculated by looking at the diagonal values of the cell grid[r][c]:
A matrix diagonal is a diagonal line of cells starting from some cell in either the topmost row or leftmost column and going in the bottom-right direction until the end of the matrix is reached.
Return the matrix answer.

**Examples**

**Example 1:**

```
Input: grid = [[1,2,3],[3,1,5],[3,2,1]]
Output: Output: [[1,1,0],[1,0,1],[0,1,1]]
Explanation:
To calculate the answer cells:
```

**Example 2:**

```
Input: grid = [[1]]
Output: Output: [[0]]
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m, n, grid[i][j] <= 50

---

## 题目（中文翻译）

给定一个大小为 `m x n` 的二维网格 `grid`，请你计算并返回同样大小为 `m x n` 的矩阵 `answer`。  
`answer[r][c]` 的取值由单元格 `grid[r][c]` 所在对角线（diagonal）上的元素决定：

- **矩阵对角线** 是指从矩阵的最上面一行或最左面一列的某个单元格出发，沿右下方向（bottom‑right）一直延伸到矩阵边界的所有单元格构成的斜线。

对于每个位置 `(r, c)`：

1. 统计该单元格所在对角线上 **不同值的数量**（不包括 `grid[r][c]` 本身），记为 `distinctAbove`。  
2. 统计该单元格所在对角线上 **不同值的数量**（不包括 `grid[r][c]` 本身），但这次从该单元格向右上方向（top‑right）延伸的对角线，记为 `distinctBelow`。  
3. `answer[r][c] = |distinctAbove - distinctBelow|`（两者数量的绝对差）。

返回完整的 `answer` 矩阵。

---

### 示例

#### 示例 1
```text
Input: grid = [[1,2,3],[3,1,5],[3,2,1]]
Output: [[1,1,0],[1,0,1],[0,1,1]]
```
**解释：**  
计算每个单元格的答案时，需要分别统计其左上对角线和右上对角线（不包括自身）的不同值数量，然后取两者的差的绝对值。例如，`answer[0][0]` 的左上对角线为空，右上对角线也为空，故差值为 0；`answer[1][1]` 左上对角线包含值 `{1,2}`（不同值 2 个），右上对角线包含值 `{5}`（不同值 1 个），所以 `answer[1][1] = |2-1| = 1`，其余单元格同理。

#### 示例 2
```text
Input: grid = [[1]]
Output: [[0]]
```
**解释：**  
唯一的单元格没有任何对角线可供统计，故差值为 0。

---

### 约束条件

- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n, grid[i][j] <= 50`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的办法就是 **对每个格子单独遍历它的两条对角线**：

* 左上对角线：从当前格子一直往左上走，收集路过的所有数值，用 `set` 去重，得到不同值的个数 `cnt_up`。  
* 右下对角线：从当前格子一直往右下走，同样收集并去重，得到 `cnt_down`。  

答案格子 `answer[r][c] = |cnt_up - cnt_down|`（绝对值是因为题目要求“差的绝对值”，这样可以避免负数）。

> **类比**：  
> `set` 就像一本字典，里面只记录出现过的单词（这里是格子的数值），不管出现多少次，只记一次。查询有多少不同的单词，只需要看字典有多少页（`len(set)`）就行了。

**为什么正确**：  
对每个格子我们都完整地检查了它左上和右下方向上所有的格子，并且只统计不同的数值。因为题目定义的正是这两条对角线的不同值个数之差，暴力遍历自然能得到正确答案。

**时间/空间复杂度**  
* 对每个格子，我们最多要走 `min(m, n)` 步（左上或右下的长度），总共 `m·n` 个格子。  
  所以时间复杂度是 **O(m·n·max(m, n))**，在最坏情况下相当于 **O(m·n·(m+n))**。  
  > 大白话：如果矩阵是 50×50，最多要做 50 × 50 × 50 ≈ 125 000 次小操作，已经不算快了。  
* 只用了若干个 `set` 来存当前对角线的数值，最多 `max(m, n)` 个对角线，每条对角线的不同数值不超过 50（题目限制），所以 **空间复杂度是 O(m + n)**。

#### 代码（Python）

```python
from typing import List

def differenceOfDistinctValues(grid: List[List[int]]) -> List[List[int]]:
    m, n = len(grid), len(grid[0])
    ans = [[0] * n for _ in range(m)]

    for r in range(m):
        for c in range(n):
            # ---------- 左上对角线 ----------
            up_set = set()
            i, j = r - 1, c - 1          # 从左上方的第一个格子开始
            while i >= 0 and j >= 0:
                up_set.add(grid[i][j])  # 把数值放进集合，自动去重
                i -= 1
                j -= 1
            cnt_up = len(up_set)        # 不同数值的个数

            # ---------- 右下对角线 ----------
            down_set = set()
            i, j = r + 1, c + 1          # 从右下方的第一个格子开始
            while i < m and j < n:
                down_set.add(grid[i][j])
                i += 1
                j += 1
            cnt_down = len(down_set)

            # 取绝对差
            ans[r][c] = abs(cnt_up - cnt_down)

    return ans
```

#### 复杂度

- **时间复杂度**：`O(m * n * max(m, n))`  
  > 想象每个格子都要走一条最长的对角线，步数随矩阵尺寸线性增长，整体就是“格子数 × 对角线长度”。  
- **空间复杂度**：`O(m + n)`（存放若干 `set`）  
  > 每条对角线最多出现 50 种不同的数值，集合的大小受限于题目给出的数值范围。

---

### 2. 最优解

#### 思路  

暴力解的慢点在 **每个格子都重新遍历两条对角线**，导致大量重复工作。  
观察发现：

* 同一条对角线上的格子 **共享** 大部分信息。  
* 对角线可以用 `r - c`（行号减列号）唯一标识。比如所有 `r-c = 0` 的格子位于同一条左上→右下的对角线上。

利用这个特性，我们可以 **一次遍历就把每条对角线的去重信息记录下来**，然后在第二次遍历时直接读取。

具体步骤：

1. **第一次遍历（左上 → 右下）**  
   * 按行从上到下、列从左到右的顺序访问格子。  
   * 对每条对角线维护一个 `set seen_up[diag]`，记录已经遍历过的格子数值。  
   * 对格子 `(r, c)`，左上对角线中“在它之前出现的格子”正好是 `seen_up[diag]` 的大小。把这个大小记为 `up_cnt[r][c]`。  
   * 然后把当前格子的数值加入 `seen_up[diag]`，为后面的格子准备。

2. **第二次遍历（右下 → 左上）**  
   * 方向相反，从矩阵右下角往左上角走。  
   * 同理维护 `set seen_down[diag]`，记录已经遍历过的（即在右下方）的格子数值。  
   * 对格子 `(r, c)`，右下对角线中“在它之后出现的格子”大小就是 `seen_down[diag]`，记为 `down_cnt[r][c]`。  
   * 再把当前格子的数值加入 `seen_down[diag]`。

3. **合并**  
   `answer[r][c] = abs(up_cnt[r][c] - down_cnt[r][c])`。

> **核心技巧**：把对角线抽象成“斜率为 1 的直线”，用 `r - c` 作为键，利用 **哈希表 + 集合** 在 O(1) 时间内获取“已有多少不同的数”。  
> **类比**：想象每条对角线是一条生产线，工人（格子）依次上岗。第一次巡检时，记录下每位工人在他前面已经出现过多少种工具（数值），第二次巡检则记录他后面出现的工具种类。这样每位工人只需要被检查两次，效率大幅提升。

#### 代码（Python）

```python
from typing import List, Dict, Set

def differenceOfDistinctValues(grid: List[List[int]]) -> List[List[int]]:
    m, n = len(grid), len(grid[0])

    # 第一次遍历：左上 → 右下，记录左上对角线已有的不同值个数
    up_cnt = [[0] * n for _ in range(m)]
    seen_up: Dict[int, Set[int]] = {}            # key = r - c

    for r in range(m):
        for c in range(n):
            diag = r - c                         # 同一条对角线的标识
            if diag not in seen_up:
                seen_up[diag] = set()
            # 当前格子左上方已经出现的不同数值数量
            up_cnt[r][c] = len(seen_up[diag])
            # 把当前格子的数值加入集合，为后面的格子做准备
            seen_up[diag].add(grid[r][c])

    # 第二次遍历：右下 → 左上，记录右下对角线已有的不同值个数
    down_cnt = [[0] * n for _ in range(m)]
    seen_down: Dict[int, Set[int]] = {}

    for r in range(m - 1, -1, -1):
        for c in range(n - 1, -1, -1):
            diag = r - c
            if diag not in seen_down:
                seen_down[diag] = set()
            down_cnt[r][c] = len(seen_down[diag])
            seen_down[diag].add(grid[r][c])

    # 合并两次统计的结果
    ans = [[0] * n for _ in range(m)]
    for r in range(m):
        for c in range(n):
            ans[r][c] = abs(up_cnt[r][c] - down_cnt[r][c])

    return ans
```

#### 复杂度

- **时间复杂度**：`O(m * n)`  
  > 每个格子只被访问两次（一次左上遍历，一次右下遍历），所有哈希表和集合的操作均摊为 O(1)。所以整体是线性时间。相较于暴力的 `O(m·n·max(m,n))`，快了一个量级。

- **空间复杂度**：`O(m + n)`（哈希表里最多存 `m+n-1` 条对角线，每条对角线的集合最多 50 个元素）  
  > 只需要记录每条对角线已经出现的不同数值，不随矩阵大小指数增长。

---

## 心得

- **核心技巧**：利用 **对角线唯一标识 `r - c` + 哈希集合**，一次遍历就能统计左上/右下方向的不同值个数。  
- **适用场景**：  
  1. “在同一条对角线/同一行/同一列上统计去重信息” 类的问题（如 LeetCode 2670、矩阵中相同对角线元素计数等）。  
  2. 需要 **前缀/后缀去重计数** 的二维或一维序列问题。  
- **一句话总结**：把对角线抽象成“一条线”，用哈希表在遍历过程中“增量记录”去重计数，省掉重复遍历。

---

## 反思

- **第一反应**：直接对每个格子跑两次对角线遍历，写出最直观的暴力代码。  
- **最容易踩的坑**：  
  * 忘记 **排除当前格子本身**，导致计数多算一次。  
  * 边界条件：第一行/第一列的格子左上对角线为空，最后一行/最后一列的格子右下对角线为空。  
  * 集合的拷贝或误用导致时间复杂度失控。  
- **下次思路**：看到“同一条斜线/同一行/同一列”的统计需求时，立刻想 “用 `key = r - c`（或 `r + c`）把它们归类”，然后 **一次遍历 + 哈希集合** 完成前缀/后缀计数。这样可以把 O(N²) 的暴力压到 O(N)。