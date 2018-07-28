# #54. 螺旋矩阵 / Spiral Matrix

> 难度：中等 · 标签：Array、Matrix、Simulation · [LeetCode 链接](https://leetcode.com/problems/spiral-matrix/)

---

## 题目（英文原版）

**Description**

Given an m x n matrix, return all elements of the matrix in spiral order.

**Examples**

**Example 1:**

```
Input: matrix = [[1,2,3],[4,5,6],[7,8,9]]
Output: [1,2,3,6,9,8,7,4,5]
```

**Example 2:**

```
Input: matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
Output: [1,2,3,4,8,12,11,10,9,5,6,7]
```

**Constraints**

- m == matrix.length
- n == matrix[i].length
- 1 <= m, n <= 10
- -100 <= matrix[i][j] <= 100

---

## 题目（中文翻译）

给定一个 **m × n 矩阵 (matrix)**，返回矩阵中所有元素按 **螺旋顺序 (spiral order)** 遍历得到的列表。

约束条件：
- m == matrix.length
- n == matrix[i].length
- 1 ≤ m, n ≤ 10
- -100 ≤ matrix[i][j] ≤ 100

示例：

示例 1  
Input: matrix = [[1,2,3],[4,5,6],[7,8,9]]  
Output: [1,2,3,6,9,8,7,4,5]

示例 2  
Input: matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]  
Output: [1,2,3,4,8,12,11,10,9,5,6,7]

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法就是“照着题目说的那样走”。  
我们把矩阵想成一张格子纸，手指从左上角开始，沿着**右 → 下 → 左 → 上**的顺时针方向走，一圈走完后再往里进一层，继续走，直到所有格子都被访问。

实现时可以：

1. 用 `visited` 集合（类似于字典的键）记录已经走过的格子，防止重复访问。  
   - **哈希表**就像一本词典，`key` 是格子坐标 `(i, j)`，`value` 可以随便，这里我们只需要判断“有没有”这本词典里有没有这个词。  
2. 用四个方向的增量 `[(0,1), (1,0), (0,-1), (-1,0)]` 表示右、下、左、上。  
3. 每一步尝试往当前方向前进一步，如果下一格已经越界或已经访问过，就**换方向**（顺时针转），继续前进。  
4. 当访问的元素数量等于矩阵总元素数时，停止。

这套办法完全按照“模拟螺旋行走”的过程来写，思路清晰，代码也不难。

#### 代码（Python）

```python
def spiralOrder(matrix):
    """
    :type matrix: List[List[int]]
    :rtype: List[int]
    """
    if not matrix:
        return []

    m, n = len(matrix), len(matrix[0])          # 行数、列数
    total = m * n                               # 需要访问的元素总数
    visited = set()                             # 已访问的坐标集合
    res = []                                     # 结果列表

    # 四个方向：右、下、左、上
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    dir_idx = 0                                  # 当前使用的方向下标

    # 起始位置在左上角
    i = j = 0

    while len(res) < total:
        res.append(matrix[i][j])                # 访问当前格子
        visited.add((i, j))                     # 标记为已访问

        # 计算下一步的坐标
        ni, nj = i + dirs[dir_idx][0], j + dirs[dir_idx][1]

        # 如果下一步超出矩阵范围或已经访问过，换方向
        if not (0 <= ni < m and 0 <= nj < n) or (ni, nj) in visited:
            dir_idx = (dir_idx + 1) % 4          # 顺时针转向
            ni, nj = i + dirs[dir_idx][0], j + dirs[dir_idx][1]

        i, j = ni, nj                            # 移动到下一格

    return res
```

#### 复杂度

- **时间复杂度**：`O(m·n)`  
  每个格子只会被访问一次，虽然在换方向时会多算一次坐标检查，但常数不影响整体规模。可以把 `O(m·n)` 想成“矩阵里有多少格子，就需要多少次操作”。

- **空间复杂度**：`O(m·n)`  
  需要一个 `visited` 集合来记录已经走过的格子，最坏情况下会存放所有格子的坐标。再加上返回的结果数组，同样是 `m·n` 大小。

---

### 2. 最优解

#### 思路  
暴力解已经是 O(m·n) 的最优时间复杂度，真正可以改进的地方是**空间**。  
我们不必用哈希表记住每个已经访问的格子，只要记录四条“边界”即可：

- `top`   ：当前未遍历的最上面一行的下标  
- `bottom`: 当前未遍历的最下面一行的下标  
- `left`  ：当前未遍历的最左边一列的下标  
- `right` ：当前未遍历的最右边一列的下标  

每遍历完一条边，就把对应的边界向内收缩 1。这样自然就避免了重复访问，也不需要额外的 `visited` 集合。

**步骤**：

1. 初始化四个边界：`top = 0, bottom = m-1, left = 0, right = n-1`。  
2. 按顺时针顺序遍历四条边：  
   - **左→右**：遍历 `top` 行的 `left … right` 列，遍历完后 `top += 1`（上边界下移）。  
   - **上→下**：遍历 `right` 列的 `top … bottom` 行，遍历完后 `right -= 1`（右边界左移）。  
   - **右←左**（如果还有未遍历的行）：遍历 `bottom` 行的 `right … left` 列，遍历完后 `bottom -= 1`（下边界上移）。  
   - **下↑上**（如果还有未遍历的列）：遍历 `left` 列的 `bottom … top` 行，遍历完后 `left += 1`（左边界右移）。  
3. 循环上述过程，直到 `top > bottom` 或 `left > right`，说明所有格子都已经走完。

这套做法只用了常数级别的额外空间（四个整数），而且逻辑上更贴近“按层收缩”的直觉。

#### 代码（Python）

```python
def spiralOrder(matrix):
    """
    :type matrix: List[List[int]]
    :rtype: List[int]
    """
    if not matrix:
        return []

    m, n = len(matrix), len(matrix[0])
    top, bottom = 0, m - 1          # 行的上、下边界
    left, right = 0, n - 1          # 列的左、右边界
    res = []                        # 结果列表

    while top <= bottom and left <= right:
        # 1️⃣ 左 → 右，遍历 top 行
        for col in range(left, right + 1):
            res.append(matrix[top][col])
        top += 1                    # 上边界下移

        # 2️⃣ 上 → 下，遍历 right 列
        for row in range(top, bottom + 1):
            res.append(matrix[row][right])
        right -= 1                  # 右边界左移

        # 3️⃣ 右 ← 左，遍历 bottom 行（注意可能已经没有行了）
        if top <= bottom:
            for col in range(right, left - 1, -1):
                res.append(matrix[bottom][col])
            bottom -= 1             # 下边界上移

        # 4️⃣ 下 ↑ 上，遍历 left 列（注意可能已经没有列了）
        if left <= right:
            for row in range(bottom, top - 1, -1):
                res.append(matrix[row][left])
            left += 1               # 左边界右移

    return res
```

#### 复杂度

- **时间复杂度**：`O(m·n)` — 每个元素恰好被访问一次，没有额外的检查或哈希操作，和暴力解一样快，只是常数更小。

- **空间复杂度**：`O(1)` — 只用了四个整数来保存边界（不计返回结果），相当于“常数级别的额外空间”。这比使用 `visited` 集合节省了大量内存，尤其在矩阵很大时优势明显。

---

## 心得

- **核心技巧**：**按层收缩的边界遍历**（四指针/边界指针）。  
- **适用题型**：  
  1. 螺旋矩阵（Spiral Matrix）  
  2. 逆时针螺旋遍历（Spiral Matrix II）  
  3. 矩阵的顺时针/逆时针层序遍历（如“矩阵旋转90度”等）  
- **一句话总结**：  
  “把矩阵看成一层层的围墙，沿着围墙走完后把围墙往里收，循环直到没有围墙为止。”

---

## 反思

- **第一反应**：直接把“顺时针螺旋”写成循环，遇到边界就换方向——也就是上面的暴力模拟。  
- **最容易踩的坑**：  
  - 单行或单列矩阵时，容易在收缩边界后继续访问已经遍历过的行/列，需要在遍历每条边之前检查对应的边界是否仍然有效（如 `if top <= bottom`、`if left <= right`）。  
  - 忘记在遍历完每条边后及时更新边界，导致无限循环。  
- **下次遇到同类题**，第一步应想到：**用四个指针记录当前未遍历的最外层边界，然后按顺时针（或逆时针）收缩边界**。这样既保证不越界，也能省去额外的 visited 结构。