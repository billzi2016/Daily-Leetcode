# #1632. 矩阵的秩变换 / Rank Transform of a Matrix

> 难度：困难 · 标签：Array、Union Find、Graph、Topological Sort、Sorting、Matrix · [LeetCode 链接](https://leetcode.com/problems/rank-transform-of-a-matrix/)

---

## 题目（英文原版）

**Description**

Given an m x n matrix, return a new matrix answer where answer[row][col] is the rank of matrix[row][col].
The rank is an integer that represents how large an element is compared to other elements. It is calculated using the following rules:
The test cases are generated so that answer is unique under the given rules.

**Examples**

**Example 1:**

```
Input: matrix = [[1,2],[3,4]]
Output: [[1,2],[2,3]]
Explanation:
The rank of matrix[0][0] is 1 because it is the smallest integer in its row and column.
The rank of matrix[0][1] is 2 because matrix[0][1] > matrix[0][0] and matrix[0][0] is rank 1.
The rank of matrix[1][0] is 2 because matrix[1][0] > matrix[0][0] and matrix[0][0] is rank 1.
The rank of matrix[1][1] is 3 because matrix[1][1] > matrix[0][1], matrix[1][1] > matrix[1][0], and both matrix[0][1] and matrix[1][0] are rank 2.
```

**Example 2:**

```
Input: matrix = [[7,7],[7,7]]
Output: [[1,1],[1,1]]
```

**Example 3:**

```
Input: matrix = [[20,-21,14],[-19,4,19],[22,-47,24],[-19,4,19]]
Output: [[4,2,3],[1,3,4],[5,1,6],[1,3,4]]
```

**Constraints**

- m == matrix.length
- n == matrix[i].length
- 1 <= m, n <= 500
- -109 <= matrix[row][col] <= 109

---

## 题目（中文翻译）

给定一个 **m × n** 的矩阵 `matrix`，返回一个新矩阵 `answer`，其中 `answer[row][col]` 表示 `matrix[row][col]` 的 **秩**（rank）。  
**秩** 是一个整数，用来表示该元素相对于其他元素的大小。计算秩时需遵循以下规则：

1. 若两个元素位于同一行（row）或同一列（column），且数值相等，则它们的秩相同。  
2. 若元素 `a` 的数值小于元素 `b`，且 `a` 与 `b` 在同一行或同一列中，则 `a` 的秩严格小于 `b` 的秩。  
3. 对于任意元素，其秩等于 **1 +** 所有满足条件 2 的较小元素的最大秩。  
4. 题目保证在上述规则下，`answer` 唯一确定。

---

### 示例

**示例 1**  
```text
Input: matrix = [[1,2],[3,4]]
Output: [[1,2],[2,3]]
Explanation:
matrix[0][0] 的秩为 1，因为它是所在行和所在列中最小的整数。  
matrix[0][1] 的秩为 2，因为 matrix[0][1] > matrix[0][0]，且 matrix[0][0] 的秩为 1。  
matrix[1][0] 的秩为 2，因为 matrix[1][0] > matrix[0][0]，且 matrix[0][0] 的秩为 1。  
matrix[1][1] 的秩为 3，因为 matrix[1][1] > matrix[0][1]、matrix[1][0]，它们的秩分别为 2 和 2，故取最大值 2 加 1 得 3。
```

**示例 2**  
```text
Input: matrix = [[7,7],[7,7]]
Output: [[1,1],[1,1]]
```

**示例 3**  
```text
Input: matrix = [[20,-21,14],[-19,4,19],[22,-47,24],[-19,4,19]]
Output: [[4,2,3],[1,3,4],[5,1,6],[1,3,4]]
```

---

### 约束条件

- `m == matrix.length`
- `n == matrix[i].length`
- `1 <= m, n <= 500`
- `-10^9 <= matrix[row][col] <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**把每个格子都当成一次“排名比赛”，找出它所在行和所在列中已经确定好的最大排名，再把自己的排名设为 max+1**。  

实现步骤可以这样描述：

1. 按照数值从小到大遍历矩阵的每一个格子。  
2. 对于当前格子 `(r, c)`，查看它所在的第 `r` 行和第 `c` 列，找出已经被赋予的**最大**排名（如果该行/列还没有任何格子被处理，则默认最大排名是 0）。  
3. 把当前格子的排名设为 `max_rank + 1`，并把这个值记入答案矩阵 `answer`。  

这里用到的**数据结构**非常简单：

- `row_max[r]`：记录第 `r` 行已经出现的最大排名。可以把它想象成一本“行记录本”，每翻一页（行号）就能看到该行的最高排名。  
- `col_max[c]`：记录第 `c` 列的最大排名，类似“列记录本”。  

为什么这个办法能得到正确答案？  
因为我们是 **严格按照数值从小到大** 的顺序处理的，所有比当前格子小的格子已经提前得到排名，它们的排名一定不大于当前格子应该得到的排名。于是只要在同一行或同一列里取最大的已经确定的排名，加一，就是当前格子合法的最小排名。

**但是**，如果同一行/列里出现**相同数值**的格子，这种做法会把它们分别算成不同的排名，而题目要求相同数值在同一行/列中必须拥有相同的排名。为了处理相同数值，需要把它们看成一个整体（连通分量），这正是暴力解的瓶颈所在。  

#### 代码（Python）

```python
def matrixRankTransform_bruteforce(matrix):
    """
    暴力解：按数值升序逐个处理，每次只看所在行/列的最大 rank。
    只适合演示思路，未处理相同数值的连通性，时间会很慢。
    """
    m, n = len(matrix), len(matrix[0])
    # 把所有格子写成 (value, row, col) 的列表，方便排序
    cells = [(matrix[i][j], i, j) for i in range(m) for j in range(n)]
    cells.sort(key=lambda x: x[0])          # 按数值从小到大

    answer = [[0] * n for _ in range(m)]    # 最终答案矩阵
    row_max = [0] * m                       # 第 r 行的当前最大 rank
    col_max = [0] * n                       # 第 c 列的当前最大 rank

    for val, r, c in cells:
        # 当前格子所在行/列已经出现的最大 rank
        cur = max(row_max[r], col_max[c]) + 1
        answer[r][c] = cur
        # 更新行/列的最大 rank，后面的格子会看到它
        row_max[r] = max(row_max[r], cur)
        col_max[c] = max(col_max[c], cur)

    return answer
```

> **关键行中文注释**  
> - `cells.sort(...)`：把所有格子按数值排好队，像排队买票一样，先处理小的。  
> - `cur = max(row_max[r], col_max[c]) + 1`：找出同一行/列里最大的已知排名，加一得到自己的排名。  
> - `row_max[r] = max(row_max[r], cur)`：把自己“报到”，让后面的人知道这行已经有这么大的排名了。  

#### 复杂度  

- **时间复杂度**：`O(m·n·log(m·n))`  
  - 解释：先把所有格子收集到列表里，需要 `m·n` 次遍历。  
  - 再对列表进行排序，排序的代价是 `O(k·log k)`，其中 `k = m·n`。  
  - 最后遍历一次列表，时间是线性的 `O(k)`。  
  - 所以总体是 `O(k·log k)`，即 `O(m·n·log(m·n))`。  
  - 对于 `m,n ≤ 500`（最多 25 万格子），这已经算是**比较慢**的做法，尤其在 Python 中会接近超时。  

- **空间复杂度**：`O(m·n)`  
  - 需要一个长度为 `m·n` 的 `cells` 列表来保存所有格子的信息，还要 `O(m+n)` 的 `row_max/col_max`，合起来仍是线性空间。  

> **大白话**：  
> - `O(m·n·log(m·n))` 就像“先把 25 万个数字排个序，需要花费大约 25 万 × log₂25 万 ≈ 25 万 × 18 次比较”。  
> - `O(m·n)` 的空间意味着我们把矩阵里每个格子都记了一遍，花的内存和原矩阵差不多。  

---  

### 2. 最优解  

#### 思路  

暴力解的**慢点**主要有两个：  

1. **没有把相同数值的格子归为同一个整体**。如果同一行/列里出现相同的数，它们的排名必须相同，否则会破坏“唯一答案”这一前提。  
2. **每次只看行/列的最大 rank**，但在处理一批**相同数值**的格子时，这些格子之间可能相互影响（因为它们会形成连通块），如果不一次性统一处理，会导致后面的格子拿到错误的基准 rank。  

为了解决这两个问题，**官方思路**是：

1. **把所有格子按数值从小到大分批**。同一批里的格子数值相等。  
2. 在同一批内部，用 **并查集（Union‑Find）** 把相互“连通”的格子合并成一个**连通分量**。  
   - 两个格子如果在同一行或同一列且数值相等，就认为它们是“相连的”。  
   - 并查集就像一本“朋友关系簿”，每次合并相同数值的邻居，就把它们的根（代表）拉到一起。  
3. 对每个连通分量，**找出它所在的所有行和所有列的当前最大 rank**（这些行列只会受到比当前数值更小的格子影响）。  
4. 该分量的 **统一 rank** = `max(这些行/列的最大 rank) + 1`。  
5. 把这个统一 rank 写回该分量的所有格子，同时更新对应的 `row_max`、`col_max`（因为以后更大的数值会看到这些新的 rank）。  

这样做的好处：

- 同一批里相等的格子一定会得到相同的排名，因为它们被合并成同一个分量，统一分配 rank。  
- 只需要遍历每个分量一次即可得到 rank，避免了在同一批内部多次查询更新导致的重复工作。  
- 由于我们始终**按数值升序**处理，每一次查询的 `row_max / col_max` 都已经是**最终的**（不会再被更小的数改变），所以算法是正确且唯一的。  

下面我们把关键概念用生活化的类比解释一下：

| 概念 | 类比 |
|------|------|
| **格子** | 超市里的一件商品（有价格 `value`、位置 `(row, col)`） |
| **按数值排序** | 把所有商品按价格从低到高排队结账 |
| **同一批相同数值** | 同价商品一起结账 |
| **并查集** | “买一送一”卡：如果两件商品在同一排（行）或同一列且同价，就可以把它们视作“一套”，卡片会把它们绑定在一起 |
| **row_max / col_max** | 每条收银通道（行/列）已经累计的最高积分，后面的顾客只看这个积分来决定自己的积分 |

#### 代码（Python）

```python
from collections import defaultdict

class UnionFind:
    """并查集实现（路径压缩 + 按秩合并）"""
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [0] * size           # 用来平衡树的高度

    def find(self, x):
        # 递归寻找根节点，同时压缩路径
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        # 合并两个集合，根节点按 rank（高度）决定谁当根
        xr, yr = self.find(x), self.find(y)
        if xr == yr:
            return
        if self.rank[xr] < self.rank[yr]:
            self.parent[xr] = yr
        elif self.rank[xr] > self.rank[yr]:
            self.parent[yr] = xr
        else:
            self.parent[yr] = xr
            self.rank[xr] += 1


def matrixRankTransform(matrix):
    """
    最优解：按数值分批 + 并查集 + 行/列最大 rank 维护
    复杂度 O(m·n·α(m·n))，α 为 Ackermann 函数的反函数，几乎可以视作 O(1)。
    """
    m, n = len(matrix), len(matrix[0])
    # 1. 把所有格子写成 (value, row, col) 并按 value 排序
    cells = [(matrix[i][j], i, j) for i in range(m) for j in range(n)]
    cells.sort(key=lambda x: x[0])

    answer = [[0] * n for _ in range(m)]   # 最终答案
    row_max = [0] * m                      # 每行已知的最大 rank
    col_max = [0] * n                      # 每列已知的最大 rank

    i = 0
    while i < len(cells):
        # --------- 处理同一个数值的一个批次 ----------
        same_val = cells[i][0]            # 本批次的数值
        batch = []                         # 本批次所有格子 (row, col)
        while i < len(cells) and cells[i][0] == same_val:
            _, r, c = cells[i]
            batch.append((r, c))
            i += 1

        # 2. 用并查集合并同批次里“同行或同列”的格子
        uf = UnionFind(m * n)              # 每个格子都有唯一 id = r*n + c
        # 先把同一行的相同数值格子连起来
        rows = defaultdict(list)
        cols = defaultdict(list)
        for r, c in batch:
            rows[r].append(c)
            cols[c].append(r)

        for r, cols_in_row in rows.items():
            # 同一行里相同数值的格子两两 union
            for j in range(1, len(cols_in_row)):
                c1 = cols_in_row[j - 1]
                c2 = cols_in_row[j]
                uf.union(r * n + c1, r * n + c2)

        for c, rows_in_col in cols.items():
            # 同一列里相同数值的格子两两 union
            for j in range(1, len(rows_in_col)):
                r1 = rows_in_col[j - 1]
                r2 = rows_in_col[j]
                uf.union(r1 * n + c, r2 * n + c)

        # 3. 统计每个连通分量需要的 rank（基于行/列的当前最大 rank）
        #   comp_max[root] = 该连通块内部所有格子所在行/列的最大 rank
        comp_max = defaultdict(int)
        for r, c in batch:
            root = uf.find(r * n + c)
            # 该格子所在行和列目前的最大 rank
            cur = max(row_max[r], col_max[c])
            comp_max[root] = max(comp_max[root], cur)

        # 4. 把计算好的 rank 写回答案，并同步更新 row_max / col_max
        for r, c in batch:
            root = uf.find(r * n + c)
            rank = comp_max[root] + 1          # +1 才是当前格子的 rank
            answer[r][c] = rank
            row_max[r] = max(row_max[r], rank) # 更新该行的最大 rank
            col_max[c] = max(col_max[c], rank) # 更新该列的最大 rank

    return answer
```

> **代码要点中文注释**  
> - `cells.sort(...)`：把所有格子按数值排好队，先处理小的。  
> - `while i < len(cells) and cells[i][0] == same_val`：把数值相同的一整批取出来。  
> - `uf.union(...)`：把同一行或同一列里相同数值的格子“拉进同一个朋友圈”。  
> - `comp_max[root] = max(comp_max[root], cur)`：记录该朋友圈里所有格子所在行/列的最大已有 rank。  
> - `rank = comp_max[root] + 1`：统一给整个朋友圈一个 rank，保证相等数值的格子拥有相同排名。  
> - `row_max[r] = max(row_max[r], rank)`：把新 rank 记进行记录本，后面更大的格子会看到它。  

#### 复杂度  

- **时间复杂度**：`O(m·n·α(m·n))`  
  - `α` 是 **Ackermann 函数的反函数**，极其缓慢增长（对于所有实际数据，α ≤ 5），可以视作常数。  
  - 具体步骤：  
    1. **排序** `O(m·n·log(m·n))`（这是唯一的对数项）。  
    2. **遍历每个批次**：对每个格子只做几次 `find/union`，每次近似 `O(1)`。  
    3. **统计/写回** 同样是线性遍历。  
  - 所以整体是 `O(m·n·log(m·n))`，但相较于暴力解，**没有在每个格子内部再次遍历整行或整列**，所以实际运行快得多。  

- **空间复杂度**：`O(m·n)`  
  - 需要保存 `cells`（`m·n` 个三元组），并查集的 `parent`/`rank` 数组也各占 `m·n`。  
  - 额外的 `row_max`、`col_max`、`answer` 同样是线性大小。  

> **大白话**：  
> - 排序的代价仍然是“把 25 万个数字排一次”。  
> - 之后每个格子只“找一次朋友”和“更新一次积分”，几乎不再花额外的时间。  
> - 空间上我们把每个格子都记了一遍，和原矩阵大小相当。  

---  

## 心得  

- **核心技巧**：**按数值分批 + 并查集合并相同数值的连通块 + 维护行/列的最大 rank**。  
- 这种思路在**“需要在行/列之间保持某种相对顺序”**的题目里非常常见，尤其当**相同数值需要统一处理**时。  

**相似题目**（可自行练习）：

1. **LeetCode 1209. Remove All Adjacent Duplicates in String II**  
   - 需要用栈或并查集把相邻相同字符归为一块。  
2. **LeetCode 1632. Rank Transform of a Tree**  
   - 把树的节点按值分层，并用并查集合并相等值的连通块。  
3. **LeetCode 1691. Maximum Height by Stacking Cuboids**  
   - 需要先排序再用 DP，思路类似“先把小的处理完”。  

> **一句话总结解题钥匙**：  
> **“先把相同数值的格子连成一块，再统一给它们排位”**。  

---  

## 反思  

- **拿到题目第一反应**：  
  - “这不就是每行每列取最大，然后加一吗？”  
  - 随即想到要把所有格子按大小顺序处理，但忘记了相同数值的连通性会导致错误。  

- **最容易踩的坑**  
  1. **相同数值跨行跨列的连通**：只把同一行或同一列相同的格子 union，而忽略了通过多次 “桥接” 形成的大块，会导致同一块内部出现不同 rank。  
  2. **更新 row_max / col_max 的时机**：必须在**整个批次**处理完以后统一更新，否则同批次内部的格子会相互干扰，导致 rank 被错误提升。  
  3. **边界条件**：矩阵只有一行或一列时，仍然需要并查集的处理，否则会出现 `IndexError`。  

- **下次遇到同类题的第一步**：  
  - **“先把所有元素按值分层，确定同层内部的等价关系（并查集/DFS），再一次性给整层分配答案”。** 这一步把“相等要一起处理”这条原则写进了解题流程，避免遗漏。