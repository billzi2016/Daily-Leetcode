# #2428. 最大沙漏和 / Maximum Sum of an Hourglass

> 难度：中等 · 标签：Array、Matrix、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/maximum-sum-of-an-hourglass/)

---

## 题目（英文原版）

**Description**

You are given an m x n integer matrix grid.
We define an hourglass as a part of the matrix with the following form:
Return the maximum sum of the elements of an hourglass.
Note that an hourglass cannot be rotated and must be entirely contained within the matrix.

**Examples**

**Example 1:**

```
Input: grid = [[6,2,1,3],[4,2,1,5],[9,2,8,7],[4,1,2,9]]
Output: 30
Explanation: The cells shown above represent the hourglass with the maximum sum: 6 + 2 + 1 + 2 + 9 + 2 + 8 = 30.
```

**Example 2:**

```
Input: grid = [[1,2,3],[4,5,6],[7,8,9]]
Output: 35
Explanation: There is only one hourglass in the matrix, with the sum: 1 + 2 + 3 + 5 + 7 + 8 + 9 = 35.
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 3 <= m, n <= 150
- 0 <= grid[i][j] <= 106

---

## 题目（中文翻译）

给定一个 `m x n` 的整数矩阵 `grid`。  
我们将 **沙漏**（hourglass）定义为矩阵中的以下形状（不能旋转）：

```
a b c
  d
e f g
```

返回所有沙漏中元素之和的最大值。  
注意，沙漏必须完整地位于矩阵内部，不能超出边界。

**示例 1**

```
Input: grid = [[6,2,1,3],[4,2,1,5],[9,2,8,7],[4,1,2,9]]
Output: 30
Explanation: 上图中的沙漏拥有最大的和：6 + 2 + 1 + 2 + 9 + 2 + 8 = 30.
```

**示例 2**

```
Input: grid = [[1,2,3],[4,5,6],[7,8,9]]
Output: 35
Explanation: 矩阵中只有一个沙漏，其和为：1 + 2 + 3 + 5 + 7 + 8 + 9 = 35.
```

**约束条件**

- `m == grid.length`
- `n == grid[i].length`
- `3 <= m, n <= 150`
- `0 <= grid[i][j] <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有可能的**沙漏**（hourglass）一个个枚举出来，逐个把它包含的 7 个格子相加，取最大值即可。

- **沙漏的形状**  

```
a b c
  d
e f g
```

  只要左上角坐标是 `(i, j)`，则这 7 个格子分别是  
  `(i, j) , (i, j+1) , (i, j+2)`  
  `(i+1, j+1)`  
  `(i+2, j) , (i+2, j+1) , (i+2, j+2)`  

- **遍历方式**  

  沙漏的宽度和高度都是 3，所以左上角 `i` 的取值范围是 `0 … m‑3`，`j` 的取值范围是 `0 … n‑3`。  
  对每一对 `(i, j)`，把上面的 7 个格子相加，更新全局最大值。

- **为什么一定对**  

  题目说明“每个 3×3 子矩阵恰好对应唯一的沙漏”，我们把所有合法的左上角都遍历了一遍，必然不会漏掉任何一个沙漏，也不会多算不存在的形状，所以答案一定正确。

- **时间/空间复杂度的大白话**  

  - **时间复杂度**：外层有 `(m‑2)·(n‑2)` 次循环，每次只算 7 个数。  
    用大写的 `O` 记号写成 `O(m·n)`，意思是时间随矩阵大小线性增长。  
    想象你在一个 `150×150` 的格子里找沙漏，最多检查 `148·148≈2万` 次，这在电脑里几乎是瞬间完成的。  
  - **空间复杂度**：只用了几个临时变量（存最大值、当前和），不随输入规模增大而增长，记作 `O(1)`，即“常数级”空间。

#### 代码（Python）

```python
def max_hourglass_sum(grid):
    """
    暴力枚举每一个沙漏，求最大和
    :param grid: List[List[int]]，m 行 n 列的整数矩阵
    :return: int，最大的沙漏和
    """
    if not grid or not grid[0]:
        return 0

    m, n = len(grid), len(grid[0])
    max_sum = -float('inf')                     # 先设一个很小的值，后面会被更新

    # 左上角 (i, j) 能取到的最大范围是 m-3、n-3
    for i in range(m - 2):
        for j in range(n - 2):
            # 直接把 7 个格子相加
            cur = (
                grid[i][j] + grid[i][j + 1] + grid[i][j + 2] +   # 第一行 3 格
                grid[i + 1][j + 1] +                             # 中间 1 格
                grid[i + 2][j] + grid[i + 2][j + 1] + grid[i + 2][j + 2]  # 第三行 3 格
            )
            max_sum = max(max_sum, cur)        # 更新最大值

    return max_sum
```

#### 复杂度

- **时间复杂度**：`O(m·n)` —— 随矩阵行数 `m` 和列数 `n` 成正比增长。  
  大白话：矩阵越大，检查的次数就线性增多，但每次只算 7 个数，速度很快。

- **空间复杂度**：`O(1)` —— 只用了几个整数变量，不会随输入变大而占用更多内存。

---

### 2. 最优解

#### 思路  

虽然上面的暴力解已经是 `O(m·n)`，但它在每一次沙漏求和时仍然要访问 7 次数组。  
如果我们能够 **一次性得到一个 3×3 子矩阵的所有元素之和**，再减去四个角，就可以在 **常数时间**（只做几次加减）得到沙漏和。  

这正是**前缀和（Prefix Sum）**的用武之地。

- **前缀和矩阵**  

  对原矩阵 `grid` 构造一个同样大小的 `pre`，其中  

  ```
  pre[i][j] = grid[0][0] + ... + grid[i][j]   （左上到 (i, j) 的所有元素之和）
  ```

  计算 `pre` 的公式：

  ```
  pre[i][j] = grid[i][j] + pre[i-1][j] + pre[i][j-1] - pre[i-1][j-1]
  ```

  这一步只遍历一次矩阵，时间 `O(m·n)`，空间同样 `O(m·n)`。

- **利用前缀和求任意子矩阵和**  

  给定左上 `(r1, c1)`、右下 `(r2, c2)`，子矩阵和可以用四个前缀和快速算出：

  ```
  sum = pre[r2][c2] - pre[r1-1][c2] - pre[r2][c1-1] + pre[r1-1][c1-1]
  ```

  只需要 4 次加减，时间常数。

- **把它套到沙漏**  

  对于左上角 `(i, j)`，对应的 **3×3 子矩阵** 为 `(i, j)` → `(i+2, j+2)`。  
  先用前缀和算出这 9 个格子的总和 `total9`，再把四个不在沙漏里的角 (`grid[i][j]、grid[i][j+2]、grid[i+2][j]、grid[i+2][j+2]`) 减掉，得到沙漏和：

  ```
  hourglass = total9 - (grid[i][j] + grid[i][j+2] + grid[i+2][j] + grid[i+2][j+2])
  ```

  这样每个沙漏的求和只需要 **常数次**（几次加减），整体仍是 `O(m·n)`，但常数更小，且思路更通用（以后遇到需要求子矩阵和的题目可以直接复用前缀和）。

- **核心概念类比**  

  前缀和就像一本 **“累计账本”**：第 `i, j` 页记录了从左上角到这里的所有收入。要算任意区间的收入，只要把相应的页码相减即可，省去逐条相加的麻烦。

#### 代码（Python）

```python
def max_hourglass_sum_prefix(grid):
    """
    使用前缀和快速求每个沙漏的和，时间 O(m·n)，空间 O(m·n)
    """
    if not grid or not grid[0]:
        return 0

    m, n = len(grid), len(grid[0])

    # 1. 构造前缀和矩阵 pre，尺寸为 (m) x (n)
    pre = [[0] * n for _ in range(m)]
    for i in range(m):
        row_sum = 0                     # 当前行从左到右的累计和
        for j in range(n):
            row_sum += grid[i][j]       # 累加本行元素
            above = pre[i - 1][j] if i > 0 else 0   # 上面那行已经累计好的和
            pre[i][j] = row_sum + above # 组合得到左上到 (i, j) 的总和

    # 2. 遍历所有合法的左上角，利用前缀和算 3×3 子矩阵的总和
    max_sum = -float('inf')
    for i in range(m - 2):
        for j in range(n - 2):
            r1, c1 = i, j
            r2, c2 = i + 2, j + 2

            # 3×3 子矩阵的和（9 个格子）
            total9 = pre[r2][c2]
            if r1 > 0:
                total9 -= pre[r1 - 1][c2]
            if c1 > 0:
                total9 -= pre[r2][c1 - 1]
            if r1 > 0 and c1 > 0:
                total9 += pre[r1 - 1][c1 - 1]

            # 减去四个角，得到沙漏和
            corners = grid[i][j] + grid[i][j + 2] + grid[i + 2][j] + grid[i + 2][j + 2]
            hourglass = total9 - corners

            max_sum = max(max_sum, hourglass)

    return max_sum
```

#### 复杂度

- **时间复杂度**：`O(m·n)` ——  
  ① 构造前缀和遍历一次矩阵 `O(m·n)`；  
  ② 再遍历所有左上角，每次只做常数次加减，同样 `O(m·n)`。  
  与暴力解的时间级别相同，但常数更小，且代码可扩展到更复杂的子矩阵求和。

- **空间复杂度**：`O(m·n)` —— 需要额外存储同尺寸的前缀和矩阵 `pre`。  
  如果只在意空间，可以把前缀和压缩为一行滚动数组，进一步降到 `O(n)`，但这里保持最直观的写法。

---

## 心得

- **核心技巧**：前缀和（Prefix Sum）可以在 **O(1)** 时间内得到任意子矩阵的元素总和，是处理二维数组区间求和的“神器”。  
- **适用的题型**  
  1. **子矩阵求和**（如 LeetCode 304 – Range Sum Query 2D - Immutable）  
  2. **矩形内最大/最小和**（如 LeetCode 363 – Max Sum of Rectangle No Larger Than K）  
  3. **任意形状的求和**（只要能表示为若干子矩阵的并减，前缀和都能派上用场）  
- **一句话总结解题钥匙**：**把“每次都遍历”变成“只要一次预处理，再用常数时间查询”。**

---

## 反思

- **第一反应**：看到“3×3 子矩阵里有固定形状”，立刻想到枚举左上角、手动加 7 个格子。  
- **最容易踩的坑**  
  - **边界检查**：左上角的 `i`、`j` 只能取到 `m-3`、`n-3`，否则会越界。  
  - **负数或全零**：如果矩阵里全是 0，最大和仍然是 0，初始化 `max_sum` 时不能直接用 `0`，要用 `-inf` 防止误判。  
  - **前缀和的减法**：在计算子矩阵和时，需要仔细处理 `i‑1`、`j‑1` 为负的情况，否则会索引错误。  
- **下次类似题的第一步**：先判断**是否可以用前缀和把“区间求和”变为 O(1) 查询**；如果可以，就先做一次预处理，再在遍历过程中快速得到每个子结构的和值。