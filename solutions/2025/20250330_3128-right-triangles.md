# #3128. 直角三角形 / Right Triangles

> 难度：中等 · 标签：Array、Hash Table、Math、Combinatorics、Counting · [LeetCode 链接](https://leetcode.com/problems/right-triangles/)

---

## 题目（英文原版）

**Description**

You are given a 2D boolean matrix grid.
A collection of 3 elements of grid is a right triangle if one of its elements is in the same row with another element and in the same column with the third element. The 3 elements may not be next to each other.
Return an integer that is the number of right triangles that can be made with 3 elements of grid such that all of them have a value of 1.

**Examples**

**Example 1:**

```
Input: grid = [[0,1,0],[0,1,1],[0,1,0]]
Output: 2
Explanation:
There are two right triangles with elements of the value 1. Notice that the blue ones do not form a right triangle because the 3 elements are in the same column.
```

**Example 2:**

```
Input: grid = [[1,0,0,0],[0,1,0,1],[1,0,0,0]]
Output: 0
Explanation:
There are no right triangles with elements of the value 1.  Notice that the blue ones do not form a right triangle.
```

**Example 3:**

```
Input: grid = [[1,0,1],[1,0,0],[1,0,0]]
Output: 2
Explanation:
There are two right triangles with elements of the value 1.
```

**Constraints**

- 1 <= grid.length <= 1000
- 1 <= grid[i].length <= 1000
- 0 <= grid[i][j] <= 1

---

## 题目（中文翻译）

**描述**  
给定一个二维布尔矩阵（2D boolean matrix）`grid`。  
如果 `grid` 中的 3 个元素满足：其中一个元素与另一个元素位于同一行（row），并且与第三个元素位于同一列（column），则这 3 个元素构成一个**直角三角形（right triangle）**。这 3 个元素不要求相邻。  

返回能够由值为 `1` 的 3 个元素组成的直角三角形的数量。

**示例**  

*示例 1*  
```text
Input: grid = [[0,1,0],[0,1,1],[0,1,0]]
Output: 2
Explanation:
有两个直角三角形的三个元素的值均为 1。需要注意，蓝色标记的三个元素不构成直角三角形，因为它们全部在同一列。
```

*示例 2*  
```text
Input: grid = [[1,0,0,0],[0,1,0,1],[1,0,0,0]]
Output: 0
Explanation:
不存在值为 1 的直角三角形。蓝色标记的三个元素同样不构成直角三角形。
```

*示例 3*  
```text
Input: grid = [[1,0,1],[1,0,0],[1,0,0]]
Output: 2
Explanation:
有两个直角三角形的三个元素的值均为 1。
```

**约束条件**  
- `1 <= grid.length <= 1000`  
- `1 <= grid[i].length <= 1000`  
- `0 <= grid[i][j] <= 1`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的办法就是把所有可能的 3 个格子枚举一遍，检查它们是否满足“直角三角形”的条件。  
- **枚举**：遍历矩阵的每一个格子，把它记为 `A`；再从 `A` 之后的格子中挑两个记为 `B、C`，一共会产生 `C(n,3)` 种组合（`n = 行数 × 列数`）。  
- **判定**：对这三个坐标 `(x1,y1) , (x2,y2) , (x3,y3)`，只要有一个点的行与另一个点相同、列与第三个点相同，就构成直角三角形。  
- **生活类比**：想象一张城市地图，格子就是街区。暴力解相当于把所有街区的三两配对都列出来，然后问“这三个街区能不能组成一个‘L’形路口？”  

这种方法一定能得到正确答案，因为我们把**所有**可能的三元组都检查了一遍，只要有符合条件的必然会被计数。  

#### 代码（Python）  
```python
def countRightTriangles_bruteforce(grid):
    m, n = len(grid), len(grid[0])
    ans = 0

    # 把所有格子展平成一个列表，方便取组合
    cells = [(i, j) for i in range(m) for j in range(n) if grid[i][j] == 1]

    # 三层循环枚举所有不同的三元组
    for a in range(len(cells)):
        x1, y1 = cells[a]
        for b in range(a + 1, len(cells)):
            x2, y2 = cells[b]
            for c in range(b + 1, len(cells)):
                x3, y3 = cells[c]

                # 判断是否形成“直角”——
                # 任意挑一个点作为直角点，检查它的行是否与另一点相同，列是否与剩下那点相同
                if (x1 == x2 and y1 == y3) or (x1 == x3 and y1 == y2) \
                or (x2 == x1 and y2 == y3) or (x2 == x3 and y2 == y1) \
                or (x3 == x1 and y3 == y2) or (x3 == x2 and y3 == y1):
                    ans += 1
    return ans
```

#### 复杂度  
- **时间复杂度**：`O(k³)`，其中 `k` 是矩阵中 `1` 的个数。最坏情况下 `k = m·n`，所以可以粗略写成 **O((m·n)³)**。这相当于“把所有可能的三个人组合都检查一遍”，所以在大矩阵上会非常慢。  
- **空间复杂度**：`O(k)` 用来存放所有 `1` 的坐标列表。除了这点额外空间，算法本身是原地的。

---

### 2. 最优解  

#### 思路  
暴力解的瓶颈在于**三重循环**——我们把每一组三元组都枚举，导致时间呈立方增长。  
观察题目提示：  
> 如果 `grid[x][y] = 1`，只要在同一行还有其他 `1`，同一列还有其他 `1`，它就可以和这些点分别组成直角三角形。

换句话说，**每个 `1` 本身就是直角的“顶点”。**  
- 设第 `x` 行里有 `row[x]` 个 `1`，第 `y` 列里有 `col[y]` 个 `1`。  
- 把当前格子 `(x, y)` 当作直角点时，需要从同一行挑 **一个** 其他的 `1`（有 `row[x]‑1` 种选择），从同一列挑 **一个** 其他的 `1`（有 `col[y]‑1` 种选择）。  
- 两者独立选择，所以该点能贡献的直角三角形数目是 `(row[x]‑1) * (col[y]‑1)`。  

于是我们只需要两遍遍历：  
1. **统计**每行、每列的 `1` 的个数。  
2. 再遍历一次矩阵，对每个值为 `1` 的格子，用上面的公式累计答案。  

这就把原来的 **立方** 时间降到了 **线性**（只和格子总数成正比）。  

**类比**：把每行看作一本字典，记录这本字典里有多少页（`1`），每列也是一本字典。要找一个“L”形，只需要知道两本字典各有多少页，再把它们相乘即可——不必把所有页码一一列举。  

#### 代码（Python）  
```python
def countRightTriangles(grid):
    m, n = len(grid), len(grid[0])

    # 1. 统计每行、每列的 1 的个数
    row_cnt = [0] * m          # row_cnt[i] = 第 i 行里 1 的数量
    col_cnt = [0] * n          # col_cnt[j] = 第 j 列里 1 的数量

    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                row_cnt[i] += 1
                col_cnt[j] += 1

    # 2. 再遍历一次，用公式累加答案
    ans = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                # (row_cnt[i] - 1) 表示除掉自身外同一行的 1 的数量
                # (col_cnt[j] - 1) 表示除掉自身外同一列的 1 的数量
                ans += (row_cnt[i] - 1) * (col_cnt[j] - 1)

    return ans
```

#### 复杂度  
- **时间复杂度**：`O(m·n)`。我们只遍历矩阵两遍，每次都是常数时间操作。相比暴力的立方级别，快得多。  
- **空间复杂度**：`O(m + n)`。需要两个一维数组分别保存每行、每列的计数，额外空间随行列数线性增长。

---

## 心得  

- **核心技巧**：把“每个点都是直角顶点”这层抽象抽出来，用**行计数 + 列计数**的乘积直接求解。  
- **适用题型**：  
  1. “在矩阵中统计满足某种行/列组合的子结构”，如 *Number of Submatrices With All Ones*（行列前缀计数）。  
  2. “以某个格子为中心，向四个方向延伸计数”，如 *Count Submatrices With All Ones* 的变体。  
  3. “点的配对问题”，如 *Number of Pairs of Points with Manhattan Distance K*（先统计行/列出现次数）。  
- **一句话总结**：**把局部的“行/列出现次数”预处理出来，再用乘法组合计数，能把指数级枚举降到线性。**

---

## 反思  

- **第一反应**：看到“同一行、同一列”就想到把每行每列的 `1` 数统计下来，随后再组合。  
- **最容易踩的坑**：  
  - 忘记在公式中减去自身的 `1`（即 `row[x]-1`、`col[y]-1`），导致把不合法的“同一点两次”算进去了。  
  - 边界情况：如果某行或某列只有一个 `1`，则 `(cnt-1)` 为 `0`，这行/列不会贡献任何三角形，代码必须正确处理。  
- **下次第一步**：先**统计**行/列/行列交叉的出现次数，判断是否可以用“乘积”或“组合”公式直接求解，避免直接枚举。