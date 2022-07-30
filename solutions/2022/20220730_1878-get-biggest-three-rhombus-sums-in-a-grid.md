# #1878. 网格中最大的三个菱形和 / Get Biggest Three Rhombus Sums in a Grid

> 难度：中等 · 标签：Array、Math、Sorting、Heap (Priority Queue)、Matrix、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/get-biggest-three-rhombus-sums-in-a-grid/)

---

## 题目（英文原版）

**Description**

You are given an m x n integer matrix grid​​​.
A rhombus sum is the sum of the elements that form the border of a regular rhombus shape in grid​​​. The rhombus must have the shape of a square rotated 45 degrees with each of the corners centered in a grid cell. Below is an image of four valid rhombus shapes with the corresponding colored cells that should be included in each rhombus sum:
Note that the rhombus can have an area of 0, which is depicted by the purple rhombus in the bottom right corner.
Return the biggest three distinct rhombus sums in the grid in descending order. If there are less than three distinct values, return all of them.

**Examples**

**Example 1:**

```
Input: grid = [[3,4,5,1,3],[3,3,4,2,3],[20,30,200,40,10],[1,5,5,4,1],[4,3,2,2,5]]
Output: [228,216,211]
Explanation: The rhombus shapes for the three biggest distinct rhombus sums are depicted above.
- Blue: 20 + 3 + 200 + 5 = 228
- Red: 200 + 2 + 10 + 4 = 216
- Green: 5 + 200 + 4 + 2 = 211
```

**Example 2:**

```
Input: grid = [[1,2,3],[4,5,6],[7,8,9]]
Output: [20,9,8]
Explanation: The rhombus shapes for the three biggest distinct rhombus sums are depicted above.
- Blue: 4 + 2 + 6 + 8 = 20
- Red: 9 (area 0 rhombus in the bottom right corner)
- Green: 8 (area 0 rhombus in the bottom middle)
```

**Example 3:**

```
Input: grid = [[7,7,7]]
Output: [7]
Explanation: All three possible rhombus sums are the same, so return [7].
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 50
- 1 <= grid[i][j] <= 105

---

## 题目（中文翻译）

You are given an `m x n` integer matrix `grid`​.

A **rhombus sum**（菱形和） is the sum of the elements that form the border of a regular **rhombus**（菱形） shape in `grid`.  
The rhombus must have the shape of a square rotated 45 degrees with each of the corners centered in a grid cell. Below is an image of four valid rhombus shapes with the corresponding colored cells that should be included in each rhombus sum:

> Note: the rhombus can have an area of 0, which is depicted by the purple rhombus in the bottom right corner.

Return the biggest three **distinct**（不同的） rhombus sums in the grid in descending order. If there are less than three distinct values, return all of them.

### 示例

#### 示例 1
**Input:**  
```json
grid = [[3,4,5,1,3],
        [3,3,4,2,3],
        [20,30,200,40,10],
        [1,5,5,4,1],
        [4,3,2,2,5]]
```
**Output:** `[228,216,211]`  
**Explanation:** The rhombus shapes for the three biggest distinct rhombus sums are depicted above.  
- **Blue:** `20 + 3 + 200 + 5 = 228`  
- **Red:** `200 + 2 + 10 + 4 = 216`  
- **Green:** `5 + 200 + 4 + 2 = 211`

#### 示例 2
**Input:**  
```json
grid = [[1,2,3],
        [4,5,6],
        [7,8,9]]
```
**Output:** `[20,9,8]`  
**Explanation:** The rhombus shapes for the three biggest distinct rhombus sums are depicted above.  
- **Blue:** `4 + 2 + 6 + 8 = 20`  
- **Red:** `9` (area 0 rhombus in the bottom right corner)  
- **Green:** `8` (area 0 rhombus in the bottom middle)

#### 示例 3
**Input:**  
```json
grid = [[7,7,7]]
```
**Output:** `[7]`  
**Explanation:** All three possible rhombus sums are the same, so return `[7]`.

### 约束条件
- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 50`
- `1 <= grid[i][j] <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

把网格看成一张棋盘，每个格子里放着一个数字。  
“菱形”就是把一个正方形顺时针转 45°，四个顶点必须落在格子中心上。  
如果把菱形的左上、右上、右下、左下四个顶点分别记为  
`(r‑k, c) , (r, c+k) , (r+k, c) , (r, c‑k)`（`k` 为菱形的“半径”，即从中心到任意顶点的步数），  
那么它的四条边正好是 **四条对角线方向** 的连续格子。

最直接的做法就是：

1. **遍历所有可能的中心** `(r, c)`（`0 ≤ r < m, 0 ≤ c < n`）。  
2. **遍历所有合法的半径 `k`**。  
   - 必须保证四个顶点都在矩阵内部，即  
     `0 ≤ r‑k , r+k < m` 且 `0 ≤ c‑k , c+k < n`。  
3. **沿着四条边逐格累加**，得到该菱形的边界和。  
   - 走左上 → 右上：`(r‑i, c+i)`，`i = 0 … k`  
   - 走右上 → 右下：`(r+i, c+i)`，`i = 1 … k`（注意不要把右上的格子重复算两次）  
   - 走右下 → 左下：`(r+i, c‑i)`，`i = 1 … k`  
   - 走左下 → 左上：`(r‑i, c‑i)`，`i = 1 … k‑1`（最后一个点已经在左上点里算过）  

   这样就把菱形的 **边界**（不包括内部）全部加进来了。  
   当 `k = 0` 时，菱形退化成一个点，边界和就是该格子的数值，这也是合法的“面积为 0 的菱形”。  

4. 把每一次得到的和放进 **集合**（去重），最后把集合转成列表，降序排序，取前 3 个即可。

> **类比**：  
> - 哈希表（这里用 `set`）就像字典，`key` 是出现过的和，自动帮我们去掉重复的值。  
> - 四条边的遍历像是走路——先往右上走 `k` 步，再往右下走 `k` 步……每一步都把路过的格子值记下来。

**为什么一定正确**：  
- 我们穷举了所有合法的中心和半径，且每一种组合都完整地遍历了它的四条边（没有漏掉也没有重复计数），所以每一个可能的菱形都被计算到了它的真实边界和。

**复杂度分析（大白话）**：  
- 中心有 `m·n` 种可能。  
- 对每个中心，半径 `k` 最大只能到 `min(r, c, m‑1‑r, n‑1‑c)`，最坏情况下约为 `min(m,n)/2`，记作 `K`。  
- 对每个 `(center, k)`，我们要走 `4·k` 步来累加——也就是 **O(k)**。  

所以总体时间是  

```
∑_{所有中心} ∑_{k=1..K} O(k)  ≈  O(m·n·K²)
```

在最坏情况下 `K ≈ 25`（因为 `m,n ≤ 50`），时间大约是 `50·50·25² ≈ 1.5·10⁶`，在 Python 里还能跑完，但已经不是最优的。

空间上我们只用了一个 `set` 来保存不同的和，最多也不会超过所有菱形的数量，仍是 **O(m·n·K)**，实际远小于几千，算作 **O(1)** 额外空间。

#### 代码（Python）

```python
from typing import List

def get_biggest_three_bruteforce(grid: List[List[int]]) -> List[int]:
    m, n = len(grid), len(grid[0])
    sums = set()                     # 用 set 自动去重

    for r in range(m):
        for c in range(n):
            # k = 0 时，菱形退化为单个格子
            sums.add(grid[r][c])

            # 枚举可能的半径 k
            max_k = min(r, c, m - 1 - r, n - 1 - c)
            for k in range(1, max_k + 1):
                total = 0

                # 左上 -> 右上
                for i in range(k):
                    total += grid[r - i][c + i]

                # 右上 -> 右下（i 从 1 开始，避免重复右上点）
                for i in range(1, k + 1):
                    total += grid[r + i][c + i]

                # 右下 -> 左下（i 从 1 开始，避免重复右下点）
                for i in range(1, k + 1):
                    total += grid[r + i][c - i]

                # 左下 -> 左上（i 从 1 开始，避免重复左上点）
                for i in range(1, k):
                    total += grid[r - i][c - i]

                sums.add(total)

    # 把集合转成列表，降序取前 3
    ans = sorted(sums, reverse=True)[:3]
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(m·n·K²)`，其中 `K = min(m,n)/2`。  
  - 大白话：如果把矩阵看成 50×50，最坏需要大约一百六十万次“加法”，还能接受。  
- **空间复杂度**：`O(1)`（不计输出集合的大小），只用了常数级别的额外变量。

---

### 2. 最优解  

#### 思路  

**瓶颈在哪里？**  
暴力解的主要耗时在于每次计算菱形边界时，都要**逐格遍历**四条边。  
如果我们能让“求一条对角线的连续和”在 **常数时间** 内完成，那么每个菱形的求和就能从 `O(k)` 降到 `O(1)`，整体复杂度随之降到 `O(m·n·K)`。

**关键技巧——对角线前缀和**  
- 对普通数组我们常用“一维前缀和”快速求区间和。  
- 对于矩阵的 **左上→右下**（↘）方向和 **右上→左下**（↙）方向的对角线，也可以预先算好前缀和，称为 **对角线前缀和**。  

我们准备两张同尺寸的矩阵：

| 名称 | 含义 |
|------|------|
| `diag1` | `diag1[i][j]` = 从左上角 (0,0) 到 (i,j) 的 **↘** 对角线元素累计和。公式：`grid[i][j] + diag1[i-1][j-1]`（超出边界视为 0）。 |
| `diag2` | `diag2[i][j]` = 从右上角 (0,n-1) 到 (i,j) 的 **↙** 对角线元素累计和。公式：`grid[i][j] + diag2[i-1][j+1]`（超出边界视为 0）。 |

有了这两张表，**任意一段对角线的和** 可以在 O(1) 内算出。例如，想要得到从点 `(r1,c1)` 到 `(r2,c2)`（走 ↘）的和（假设 `r2 ≥ r1`）：

```
sum = diag1[r2][c2] - diag1[r1-1][c1-1]   (如果 r1>0 且 c1>0)
```

同理，↙ 方向用 `diag2`。

**如何利用它求菱形的四条边？**  
记中心 `(r,c)`，半径 `k`。

```
左上  (r-k, c)      → 右上 (r, c+k)   : 方向 ↙
右上  (r,   c+k)    → 右下 (r+k, c)   : 方向 ↘
右下  (r+k, c)      → 左下 (r,   c-k) : 方向 ↙
左下  (r,   c-k)    → 左上 (r-k, c)   : 方向 ↘
```

每条边的端点已经知道，使用对角线前缀和直接得到整条边的和。**注意**：四条边的四个端点会把四个顶点各算了两次（每条边的起点和终点都算一次），所以最后需要 **减去四个顶点的值**，只保留边界上的格子。

**整体流程**  

1. 预处理 `diag1`、`diag2`（两次遍历矩阵，时间 `O(m·n)`）。  
2. 同样遍历所有中心 `(r,c)` 与所有合法半径 `k`（最多 `K`）。  
3. 对每个 `(r,c,k)`：  
   - 用 `diag1/diag2` 计算四条边的和（每条 O(1)）。  
   - `total = sum1 + sum2 + sum3 + sum4 - 4 * grid[corner]`（四个角已经被多算了一次）。  
   - 把 `total` 加入集合。  
4. 最后对集合排序，取前 3。  

**复杂度对比**：  
- 暴力解：`O(m·n·K²)`（每个菱形要走 `k` 步）。  
- 优化后：`O(m·n·K)`（每个菱形只做常数次查表），大约比前者快 `K` 倍（最多 25 倍），在最坏情况下只有约 `6·10⁴` 次运算，几乎瞬间完成。

#### 代码（Python）

```python
from typing import List

def get_biggest_three(grid: List[List[int]]) -> List[int]:
    m, n = len(grid), len(grid[0])

    # ---------- 1. 预处理两条对角线的前缀和 ----------
    diag1 = [[0] * n for _ in range(m)]   # ↘ 方向
    diag2 = [[0] * n for _ in range(m)]   # ↙ 方向

    for i in range(m):
        for j in range(n):
            # ↘ 前缀和：来自左上角 (i-1, j-1)
            diag1[i][j] = grid[i][j]
            if i > 0 and j > 0:
                diag1[i][j] += diag1[i-1][j-1]

            # ↙ 前缀和：来自右上角 (i-1, j+1)
            diag2[i][j] = grid[i][j]
            if i > 0 and j + 1 < n:
                diag2[i][j] += diag2[i-1][j+1]

    # ---------- 2. 辅助函数：快速求对角线区间和 ----------
    def get_diag1_sum(r1, c1, r2, c2):
        """↘ 从 (r1,c1) 到 (r2,c2) 的和，保证 r2>=r1, c2>=c1"""
        res = diag1[r2][c2]
        if r1 > 0 and c1 > 0:
            res -= diag1[r1-1][c1-1]
        return res

    def get_diag2_sum(r1, c1, r2, c2):
        """↙ 从 (r1,c1) 到 (r2,c2) 的和，保证 r2>=r1, c2<=c1"""
        res = diag2[r2][c2]
        if r1 > 0 and c1 + 1 < n:
            res -= diag2[r1-1][c1+1]
        return res

    # ---------- 3. 枚举所有菱形 ----------
    sums = set()
    for r in range(m):
        for c in range(n):
            # 半径 0 的情况：单个格子
            sums.add(grid[r][c])

            max_k = min(r, c, m - 1 - r, n - 1 - c)
            for k in range(1, max_k + 1):
                # 四条边的端点
                # 左上 -> 右上 (↙)
                s1 = get_diag2_sum(r - k, c, r, c + k)
                # 右上 -> 右下 (↘)
                s2 = get_diag1_sum(r, c + k, r + k, c)
                # 右下 -> 左下 (↙)
                s3 = get_diag2_sum(r, c - k, r + k, c)
                # 左下 -> 左上 (↘)
                s4 = get_diag1_sum(r - k, c, r, c - k)

                # 四个顶点被算了两次，需要减掉一次
                total = s1 + s2 + s3 + s4 \
                        - grid[r - k][c] - grid[r][c + k] \
                        - grid[r + k][c] - grid[r][c - k]

                sums.add(total)

    # ---------- 4. 取最大三个 ----------
    return sorted(sums, reverse=True)[:3]
```

#### 复杂度  

- **时间复杂度**：`O(m·n·K)`，其中 `K = min(m,n)/2`。  
  - 大白话：在 50×50 的矩阵里最多只需要遍历大约 6 万次“求和”，每次只做几次数组下标访问，几乎是瞬间完成。  
- **空间复杂度**：`O(m·n)` 用来存放 `diag1`、`diag2` 两张前缀和矩阵；集合 `sums` 最多也只会有 `m·n·K` 条不同的和，整体仍是线性空间。

---

## 心得  

- **核心技巧**：**对角线前缀和**（把“走对角线求和”变成 O(1)）  
- **适用的题型**：  
  1. “求矩阵中任意斜线（对角线）区间和” 类题，例如 LeetCode 1460 *Make Two Arrays Equal by Reversing Subarrays*（需要斜对角前缀）  
  2. “菱形、斜线形状的子矩阵求和” 题，如 “Largest Submatrix With Rearrangements” 的变体  
  3. “在网格上按斜方向移动的路径最大和” 类 DP 题。  

> **解题钥匙**：把 **“遍历”** 的代价压到 **“查询”**，先预处理，再常数时间拿到所需信息。

---

## 反思  

- **第一反应**：看到“菱形”和“边界求和”，本能想把四条边一个格子一个格子遍历——这就是暴力思路。  
- **最容易踩的坑**：  
  1. **重复计数**：四条边的端点会被算两次，需要在最终结果中减掉四个角的值。  
  2. **边界检查**：半径 `k` 必须保证四个顶点都在矩阵内部，尤其在矩阵不是正方形时更容易出错。  
  3. **对角线前缀和的索引**：`diag2` 的递推方向是左上 → 右下，取值时要小心 `c+1` 越界。  

- **下次遇到类似题目**，第一步应该先问自己：  
  > “这类形状的求和是否可以转化为若干条**固定方向**的连续段？”  
  如果答案是“Yes”，就尝试**预处理对应方向的前缀和**，把遍历的时间压到常数。这样往往能从暴力 O(n³) 直接降到 O(n²) 甚至更低。