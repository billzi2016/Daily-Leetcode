# #2373. 矩阵中的最大局部值 / Largest Local Values in a Matrix

> 难度：简单 · 标签：Array、Matrix · [LeetCode 链接](https://leetcode.com/problems/largest-local-values-in-a-matrix/)

---

## 题目（英文原版）

**Description**

You are given an n x n integer matrix grid.
Generate an integer matrix maxLocal of size (n - 2) x (n - 2) such that:
In other words, we want to find the largest value in every contiguous 3 x 3 matrix in grid.
Return the generated matrix.

**Examples**

**Example 1:**

```
Input: grid = [[9,9,8,1],[5,6,2,6],[8,2,6,4],[6,2,2,2]]
Output: [[9,9],[8,6]]
Explanation: The diagram above shows the original matrix and the generated matrix.
Notice that each value in the generated matrix corresponds to the largest value of a contiguous 3 x 3 matrix in grid.
```

**Example 2:**

```
Input: grid = [[1,1,1,1,1],[1,1,1,1,1],[1,1,2,1,1],[1,1,1,1,1],[1,1,1,1,1]]
Output: [[2,2,2],[2,2,2],[2,2,2]]
Explanation: Notice that the 2 is contained within every contiguous 3 x 3 matrix in grid.
```

**Constraints**

- n == grid.length == grid[i].length
- 3 <= n <= 100
- 1 <= grid[i][j] <= 100

---

## 题目（中文翻译）

给定一个 `n × n` 的整数矩阵 `grid`。

生成一个大小为 `(n - 2) × (n - 2)` 的整数矩阵 `maxLocal`，使得 `maxLocal[i][j]` 为 `grid` 中以左上角坐标 `(i, j)` 为起点的 **连续的 3×3 子矩阵（submatrix）** 的最大值。

返回生成的矩阵 `maxLocal`。

## 示例

### 示例 1

**输入**  
```text
grid = [[9,9,8,1],
        [5,6,2,6],
        [8,2,6,4],
        [6,2,2,2]]
```

**输出**  
```text
[[9,9],
 [8,6]]
```

**解释**  
上图展示了原始矩阵和生成的矩阵。可以看到，生成矩阵中的每个值对应于原矩阵中相应的连续的 3×3 子矩阵的最大值。

### 示例 2

**输入**  
```text
grid = [[1,1,1,1,1],
        [1,1,1,1,1],
        [1,1,2,1,1],
        [1,1,1,1,1],
        [1,1,1,1,1]]
```

**输出**  
```text
[[2,2,2],
 [2,2,2],
 [2,2,2]]
```

**解释**  
可以看到，数值 `2` 出现在原矩阵的每一个连续的 3×3 子矩阵中，因此生成矩阵的所有位置都为 `2`。

## 约束条件

- `n == grid.length == grid[i].length`
- `3 ≤ n ≤ 100`
- `1 ≤ grid[i][j] ≤ 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：  
1. 先把左上角的 `3×3` 小方块找出来，遍历这 9 个格子，记下最大值。  
2. 然后把小方块向右、向下依次“滑动”，每到一个新位置，都再遍历一次它内部的 9 个格子取最大值。  

> **数据结构**：这里只用到最基础的 **二维列表**（`list of list`），相当于我们在纸上画的格子表。  
> **类比**：把每个 `3×3` 小窗口想象成一块小厨房的操作台，厨师要在这块台面上找出最辣的辣椒（最大值），于是他把台面上的每个辣椒都尝一遍，记下最辣的那个。  

为什么这个方法一定对？因为题目要求“每个连续的 `3×3` 矩阵的最大值”，只要我们把所有可能的 `3×3` 矩阵都枚举一次，并在每个矩阵内部找出最大值，就能得到答案。

#### 代码（Python）

```python
from typing import List

def largestLocal(grid: List[List[int]]) -> List[List[int]]:
    n = len(grid)                     # 矩阵的行数（也是列数）
    ans = [[0] * (n - 2) for _ in range(n - 2)]   # 用来装结果的 (n-2)×(n-2) 矩阵

    # i, j 分别是 3×3 小窗口左上角的坐标
    for i in range(n - 2):
        for j in range(n - 2):
            cur_max = 0               # 用来记录当前窗口的最大值
            # 遍历窗口内部的 3 行 3 列
            for x in range(i, i + 3):
                for y in range(j, j + 3):
                    if grid[x][y] > cur_max:
                        cur_max = grid[x][y]   # 更新最大值
            ans[i][j] = cur_max        # 把最大值写进答案矩阵
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n³)`  
  - 外层两层循环遍历所有左上角位置，共 `(n‑2)² ≈ n²` 次。  
  - 内层再遍历 9 (=3×3) 个格子，所以总操作数大约是 `9·n² ≈ O(n³)`。  
  - 用大白话说，就是如果 `n=100`，我们大概要检查 `100·100·9 = 90,000` 次，这在电脑眼里仍然是很快的。

- **空间复杂度**：`O(n²)`  
  - 额外开辟了一个大小为 `(n‑2)×(n‑2)` 的答案矩阵，需要 `≈ n²` 的空间。  
  - 除此之外，只用了常数级的临时变量（`cur_max` 等），所以不再额外占用空间。

---

### 2. 最优解

#### 思路  

暴力解的“慢点”在于：**每次窗口移动时都要把 9 个格子重新遍历一遍**。  
我们可以把这 9 次遍历的工作“搬运”到前面一次性完成，然后在窗口滑动时复用已经算好的信息。

**一步步的优化思路**：

1. **先在每一行上做一次滑动窗口**  
   - 对每一行，求出所有长度为 3 的子数组的最大值。  
   - 这一步可以用 **单调双端队列（deque）** 完成，时间是 `O(n)`。  
   - 结果是一个新的矩阵 `row_max`，它的大小是 `n × (n‑2)`，`row_max[i][j]` 表示第 `i` 行、从第 `j` 列开始的 3 个数的最大值。

2. **再在列方向上做一次滑动窗口**  
   - 把 `row_max` 看成若干列，对每一列再做一次长度为 3 的滑动最大值。  
   - 同样用单调队列，得到最终的 `maxLocal`，大小为 `(n‑2) × (n‑2)`。  

这样，每个元素只会被“加入”和“弹出”队列各一次，总共 `O(n²)` 次操作，显著快于 `O(n³)`。

> **单调队列是什么？**  
> 想象一条只能在两端进出的人排队（deque），但我们要求队列里保存的数值从大到小递减。  
> - 当我们加入一个新数时，把队尾所有 **小于** 新数的元素踢出去，因为它们永远不可能成为后面窗口的最大值。  
> - 当窗口左边界离开时，如果队首正好是要离开的那个数，就把它弹出。  
> 这样，队首永远是当前窗口的最大值，取值 O(1) 。

#### 代码（Python）

```python
from collections import deque
from typing import List

def largestLocal(grid: List[List[int]]) -> List[List[int]]:
    n = len(grid)

    # ---------- 第一步：行方向的滑动最大值 ----------
    # row_max[i][j] 表示第 i 行、列区间 [j, j+2] 的最大值
    row_max = [[0] * (n - 2) for _ in range(n)]

    for i in range(n):
        dq = deque()                     # 存放列索引，保证对应的值单调递减
        for j in range(n):
            # 1) 把比当前值小的元素踢出队尾
            while dq and grid[i][dq[-1]] <= grid[i][j]:
                dq.pop()
            dq.append(j)

            # 2) 确保队首在窗口内（窗口宽度是 3）
            if dq[0] <= j - 3:
                dq.popleft()

            # 3) 当窗口形成（j >= 2）时，记录最大值
            if j >= 2:
                row_max[i][j - 2] = grid[i][dq[0]]

    # ---------- 第二步：列方向的滑动最大值 ----------
    # 最终答案 max_local 的大小是 (n-2) × (n-2)
    max_local = [[0] * (n - 2) for _ in range(n - 2)]

    for j in range(n - 2):               # 对每一列（已经是行滑动后的结果）
        dq = deque()                     # 存放行索引，保证对应的值单调递减
        for i in range(n):
            # 1) 把比当前值小的元素踢出队尾
            while dq and row_max[dq[-1]][j] <= row_max[i][j]:
                dq.pop()
            dq.append(i)

            # 2) 保证队首仍在窗口内（窗口高度是 3）
            if dq[0] <= i - 3:
                dq.popleft()

            # 3) 当窗口形成（i >= 2）时，写入答案
            if i >= 2:
                max_local[i - 2][j] = row_max[dq[0]][j]

    return max_local
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 行滑动最大值遍历每个元素一次，列滑动最大值同理，总共 `2·n²` 次操作。  
  - 用大白话说，`n=100` 时只需要大约 `20,000` 次基本操作，比暴力的 `90,000` 次少了近 4 倍，且随着 `n` 增大差距会更明显。

- **空间复杂度**：`O(n²)`  
  - 额外用了两块同样大小的矩阵 `row_max` 和 `max_local`（分别是 `n×(n‑2)` 与 `(n‑2)×(n‑2)`），加上几个队列，都是线性级别的空间。  
  - 与暴力解相比，空间并没有增加太多（仍然是同阶的 `n²`），但时间更快。

---

## 心得

- **核心技巧**：**二维滑动窗口 + 单调队列**。把大窗口的最大值拆成先行后列的两次“一维”滑动，利用单调队列把每一次“一维”滑动的复杂度降到线性。
- **适用题型**  
  1. “矩阵中每个 k×k 子矩阵的最大/最小值”  
  2. “二维数组的滑动窗口求和/异或”等可以先把行/列的部分结果预处理的题目  
  3. “图像处理中的局部滤波” 这类需要在局部区域快速聚合信息的场景
- **一句话总结**：把二维窗口拆成两次一维窗口，配合单调队列即可在 `O(n²)` 时间搞定。

---

## 反思

- **第一反应**：直接用两层循环枚举左上角，再用三层循环遍历 3×3，写出暴力代码。因为这最符合直觉，且实现最简单。
- **最容易踩的坑**  
  - **边界**：窗口左上角的坐标只能到 `n‑3`，否则会超出矩阵范围。  
  - **队列维护**：忘记在滑动时把已经离开窗口的索引弹出，会导致队首不是当前窗口的最大值。  
  - **初始化**：`row_max` 和 `max_local` 的尺寸一定要是 `(n-2)`，否则会出现 IndexError。
- **下次遇到同类题**：第一步先思考“是否可以把二维问题拆成两次一维问题”，如果可以，就立刻考虑 **单调队列**（或 **前缀和**）来做一维滑动优化。这样往往能把 `O(n³)` 降到 `O(n²)`，甚至更低。