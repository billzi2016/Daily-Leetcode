# #2132. 在网格上盖章 / Stamping the Grid

> 难度：困难 · 标签：Array、Greedy、Matrix、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/stamping-the-grid/)

---

## 题目（英文原版）

**Description**

You are given an m x n binary matrix grid where each cell is either 0 (empty) or 1 (occupied).
You are then given stamps of size stampHeight x stampWidth. We want to fit the stamps such that they follow the given restrictions and requirements:
Return true if it is possible to fit the stamps while following the given restrictions and requirements. Otherwise, return false.

**Examples**

**Example 1:**

```
Input: grid = [[1,0,0,0],[1,0,0,0],[1,0,0,0],[1,0,0,0],[1,0,0,0]], stampHeight = 4, stampWidth = 3
Output: true
Explanation: We have two overlapping stamps (labeled 1 and 2 in the image) that are able to cover all the empty cells.
```

**Example 2:**

```
Input: grid = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]], stampHeight = 2, stampWidth = 2 
Output: false 
Explanation: There is no way to fit the stamps onto all the empty cells without the stamps going outside the grid.
```

**Constraints**

- m == grid.length
- n == grid[r].length
- 1 <= m, n <= 105
- 1 <= m * n <= 2 * 105
- grid[r][c] is either 0 or 1.
- 1 <= stampHeight, stampWidth <= 105

---

## 题目（中文翻译）

**题目描述**  
给定一个 `m x n` 的二进制矩阵（binary matrix）`grid`，矩阵中的每个单元格要么是 `0`（空），要么是 `1`（已占用）。  
同时给定印章的尺寸 `stampHeight x stampWidth`。我们需要在满足以下限制和要求的前提下放置印章：

- 每个印章必须完全位于矩阵内部，不能超出边界。  
- 只能在空单元格（值为 `0`）上进行盖章，已占用的单元格（值为 `1`）不能被覆盖。  
- 盖章可以相互重叠。  

如果能够在满足上述条件的情况下使所有空单元格都被盖住，返回 `true`；否则返回 `false`。

**示例**

*示例 1*  
```
Input: grid = [[1,0,0,0],
               [1,0,0,0],
               [1,0,0,0],
               [1,0,0,0],
               [1,0,0,0]], stampHeight = 4, stampWidth = 3
Output: true
Explanation: 如图所示，我们使用两个相互重叠的印章（图中标记为 1 和 2）即可覆盖所有空单元格。
```

*示例 2*  
```
Input: grid = [[1,0,0,0],
               [0,1,0,0],
               [0,0,1,0],
               [0,0,0,1]], stampHeight = 2, stampWidth = 2 
Output: false
Explanation: 无法在不超出网格边界的前提下，将印章放置到所有空单元格上。
```

**约束条件**
- `m == grid.length`
- `n == grid[r].length`
- `1 <= m, n <= 10^5`
- `1 <= m * n <= 2 * 10^5`
- `grid[r][c]` 只能是 `0` 或 `1`
- `1 <= stampHeight, stampWidth <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**枚举所有可能的盖章位置**，检查该位置对应的 `stampHeight × stampWidth` 小矩形里是否全是 `0`（空格）。如果可以，就把这块区域记为“已经被盖住”。最后遍历整个网格，确认每个原本为 `0` 的格子都被至少一次盖章覆盖。

> **类比**：把矩阵想象成一张格子纸，`1` 是已经被占用的格子，`0` 是需要贴标签的格子。我们手里有一张固定大小的标签纸（stamp），只能贴在全是空格的区域，且可以相互重叠。暴力做法就是把标签纸搬到每一个可能的位置，逐格检查下面的纸是否全是空的。

**为什么正确**：只要我们把所有合法的贴标签位置都尝试过，并把它们的覆盖范围记录下来，最后只要检查每个空格是否被记录到，答案就一定准确。  

**时间/空间复杂度**（大白话）  
- 对每个左上角 `(i, j)`（共 `m·n` 个），我们要检查一个大小为 `stampHeight × stampWidth` 的子矩阵，检查过程要看 `stampHeight·stampWidth` 个格子。于是总共要做 `m·n·stampHeight·stampWidth` 次格子检查。  
- 这在最坏情况下会是 **`O(m·n·stampHeight·stampWidth)`**，如果矩阵是 `1000×1000`、印章是 `500×500`，那就相当于 **10^12** 次操作，根本跑不完。  
- 需要的额外空间只有记录覆盖情况的矩阵，大小 `m·n`，即 **`O(m·n)`**。

#### 代码（Python）

```python
def possibleToStamp(grid, stampHeight, stampWidth):
    m, n = len(grid), len(grid[0])
    # 用来标记哪些格子已经被至少一块印章覆盖
    covered = [[0] * n for _ in range(m)]

    # 暴力遍历每一个可能的左上角
    for i in range(m - stampHeight + 1):
        for j in range(n - stampWidth + 1):
            # 检查 stampHeight × stampWidth 区域里是否全是 0
            ok = True
            for a in range(stampHeight):
                for b in range(stampWidth):
                    if grid[i + a][j + b] == 1:   # 遇到已占用格子，不能贴印章
                        ok = False
                        break
                if not ok:
                    break

            # 如果可以贴，就把这块区域全部标记为已覆盖
            if ok:
                for a in range(stampHeight):
                    for b in range(stampWidth):
                        covered[i + a][j + b] = 1

    # 最后检查所有原本为 0 的格子是否都被覆盖了
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 0 and covered[i][j] == 0:
                return False
    return True
```

#### 复杂度  

- **时间复杂度**：`O(m·n·stampHeight·stampWidth)`  
  - 这相当于“把每块印章的每个格子都检查一遍”。在数据规模大时会超时。  
- **空间复杂度**：`O(m·n)`  
  - 只需要一个同尺寸的矩阵记录覆盖情况。

---

### 2. 最优解  

#### 思路  

暴力解慢的根源在于**重复检查同一块子矩阵的内部格子**。例如相邻两个左上角只相差一列，但我们仍然把整块 `stampHeight × stampWidth` 的格子从头到尾遍历一遍，这导致大量冗余计算。

要把重复的检查去掉，可以**预处理出任意子矩阵中 `1` 的个数**，这样只需要 O(1) 时间就能判断某个位置的子矩阵是否全是 `0`。  
这正是**前缀和（二维）**的用武之地：

1. **二维前缀和** `pre[i+1][j+1]` 表示矩阵左上角 `(0,0)` 到 `(i,j)`（含）之间 `1` 的总数。  
   - 计算公式：`pre[i+1][j+1] = pre[i][j+1] + pre[i+1][j] - pre[i][j] + grid[i][j]`。  
   - 这样我们可以在 O(1) 时间内得到任意矩形 `[r1,r2] × [c1,c2]` 中 `1` 的数量：  
     `cnt = pre[r2+1][c2+1] - pre[r1][c2+1] - pre[r2+1][c1] + pre[r1][c1]`。

2. 用前缀和判断每个左上角 `(i,j)` 对应的 `stampHeight × stampWidth` 区域是否全是 `0`（即 `cnt == 0`），如果可以，就把这块区域的**覆盖信息**记录下来。  
   - 直接把每个合法位置的所有格子都标记为已覆盖仍然会是 O(m·n·stampHeight·stampWidth)。  
   - 为了做到 O(m·n)，我们采用**二维差分数组（Imos 方法）**：  
     - 对合法的左上角 `(i,j)`，在差分矩阵 `diff` 中四个角做增减操作，使得后续一次前缀和就能得到每个格子被多少块印章覆盖。  
     - 具体做法：  
       ```text
       diff[i][j]         += 1
       diff[i + stampHeight][j]         -= 1
       diff[i][j + stampWidth]          -= 1
       diff[i + stampHeight][j + stampWidth] += 1
       ```  
     - 最后对 `diff` 再做一次二维前缀和，得到 `cover[i][j]`（被覆盖的次数）。若 `cover[i][j] > 0` 则说明该格子被至少一块印章覆盖。

3. 最后遍历原矩阵：若某格子本来是 `0`，但对应的 `cover` 为 `0`，说明它根本没有被任何合法印章覆盖，直接返回 `False`。否则全部满足返回 `True`。

> **类比**：  
> - 前缀和就像是“累计的书页数”。只要知道前几页的总数，就能快速算出任意区间的页数。  
> - 差分数组则像是“在区间起点加一本书，在区间终点后减一本书”，最后把所有“加”与“减”累加起来，就得到每一页实际拥有的书本数。

#### 代码（Python）

```python
def possibleToStamp(grid, stampHeight, stampWidth):
    m, n = len(grid), len(grid[0])

    # ---------- 1. 计算二维前缀和（统计 1 的个数） ----------
    pre = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        row_sum = 0
        for j in range(n):
            row_sum += grid[i][j]          # 本行累计
            pre[i + 1][j + 1] = pre[i][j + 1] + row_sum

    # ---------- 2. 用差分数组记录所有合法印章的覆盖范围 ----------
    diff = [[0] * (n + 1) for _ in range(m + 1)]   # 多一行/列方便边界处理

    for i in range(m - stampHeight + 1):
        for j in range(n - stampWidth + 1):
            # 计算左上角 (i,j) 对应子矩阵中 1 的数量
            r1, c1 = i, j
            r2, c2 = i + stampHeight - 1, j + stampWidth - 1
            ones = (pre[r2 + 1][c2 + 1] - pre[r1][c2 + 1]
                    - pre[r2 + 1][c1] + pre[r1][c1])
            if ones == 0:            # 完全没有占用格子，合法
                diff[i][j] += 1
                diff[i + stampHeight][j] -= 1
                diff[i][j + stampWidth] -= 1
                diff[i + stampHeight][j + stampWidth] += 1

    # ---------- 3. 把差分数组恢复为实际覆盖次数 ----------
    cover = [[0] * n for _ in range(m)]
    for i in range(m):
        cur = 0
        for j in range(n):
            cur += diff[i][j]                 # 行内累计
            if i > 0:
                diff[i][j] += diff[i - 1][j]  # 加上上一行的累计
            cover[i][j] = diff[i][j]          # 这里的 diff 已经是最终覆盖次数

    # ---------- 4. 检查每个空格子是否被覆盖 ----------
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 0 and cover[i][j] == 0:
                return False
    return True
```

> **代码要点注释**  
> - 第 1 步的 `pre` 用来“一次性”得到任意子矩阵里 `1` 的数量。  
> - 第 2 步的四次增减是**二维差分**的核心：只在左上角加 1、右下角再加 1、右上角、左下角各减 1，后面一次前缀和即可恢复每格被覆盖的次数。  
> - 第 3 步直接在 `diff` 上做两次累计（先行后列），得到最终的 `cover`。  
> - 第 4 步只要发现有 `0` 没被覆盖，就可以立刻返回 `False`。

#### 复杂度  

- **时间复杂度**：`O(m·n)`  
  - 前缀和、差分累计、最终检查各只遍历一次矩阵。相当于“线性”时间，即使 `m·n` 达到 2×10⁵ 也能轻松跑完。  
  - 与暴力解的 `O(m·n·stampHeight·stampWidth)` 相比，省掉了所有重复的子矩阵检查。  
- **空间复杂度**：`O(m·n)`  
  - 需要额外的前缀和矩阵 `pre`（`(m+1)×(n+1)`）和差分/覆盖矩阵 `diff/cover`，总共同样是与原矩阵同量级的空间。

---

## 心得  

- **核心技巧**：二维前缀和 + 二维差分（Imos）  
- **适用题型**  
  1. “子矩阵全为 0/1 能否覆盖全部空格” 类似的 **矩阵覆盖** 问题。  
  2. “在矩阵上多次区间加/减后，查询每个位置的最终值” 典型的 **区间操作 + 前缀和**。  
  3. “判断每个子矩阵是否满足某种条件（如全部相同、全部 ≤ K）” 时常用 **前缀和** 快速求和。  
- **一句话总结解题钥匙**：**先用前缀和把“这块区域能否放印章”降到 O(1)，再用差分数组把所有合法印章的覆盖一次性累计**。

---

## 反思  

- **第一反应**：看到“stampHeight × stampWidth 的印章可以重叠，要求覆盖所有 0”，本能想到枚举所有左上角并逐格检查。  
- **最容易踩的坑**  
  1. **边界检查**：印章左上角只能放在 `i ≤ m‑stampHeight`、`j ≤ n‑stampWidth` 的位置，忘了会导致数组越界。  
  2. **覆盖计数的实现**：直接在 `cover` 矩阵上逐格加 1 会回到暴力时间，必须使用差分技巧。  
  3. **前缀和的索引**：二维前缀和通常多一行/列作哨兵，容易把 `pre[i][j]` 与原矩阵 `grid[i‑1][j‑1]` 搞混。  
- **下次类似题的第一步**：**先思考能否用前缀和把子矩阵属性（全 0、全 1、和 ≤ K）在 O(1) 内查询**，如果可以，再考虑如何在 O(1) 或 O(log) 时间内“批量更新”这些子矩阵的影响（差分、树状数组、线段树等）。这样就能把指数级的枚举压到线性或准线性。