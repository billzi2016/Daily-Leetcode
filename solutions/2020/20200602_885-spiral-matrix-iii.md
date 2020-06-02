# #885. 螺旋矩阵 III / Spiral Matrix III

> 难度：中等 · 标签：Array、Matrix、Simulation · [LeetCode 链接](https://leetcode.com/problems/spiral-matrix-iii/)

---

## 题目（英文原版）

**Description**

You start at the cell (rStart, cStart) of an rows x cols grid facing east. The northwest corner is at the first row and column in the grid, and the southeast corner is at the last row and column.
You will walk in a clockwise spiral shape to visit every position in this grid. Whenever you move outside the grid's boundary, we continue our walk outside the grid (but may return to the grid boundary later.). Eventually, we reach all rows * cols spaces of the grid.
Return an array of coordinates representing the positions of the grid in the order you visited them.

**Examples**

**Example 1:**

```
Input: rows = 1, cols = 4, rStart = 0, cStart = 0
Output: [[0,0],[0,1],[0,2],[0,3]]
```

**Example 2:**

```
Input: rows = 5, cols = 6, rStart = 1, cStart = 4
Output: [[1,4],[1,5],[2,5],[2,4],[2,3],[1,3],[0,3],[0,4],[0,5],[3,5],[3,4],[3,3],[3,2],[2,2],[1,2],[0,2],[4,5],[4,4],[4,3],[4,2],[4,1],[3,1],[2,1],[1,1],[0,1],[4,0],[3,0],[2,0],[1,0],[0,0]]
```

**Constraints**

- 1 <= rows, cols <= 100
- 0 <= rStart < rows
- 0 <= cStart < cols

---

## 题目（中文翻译）

你从一个 `rows` 行 × `cols` 列的网格的单元格 `(rStart, cStart)` 开始，面向东。网格的左上角位于第一行第一列，右下角位于最后一行最后一列。  
你将以顺时针螺旋的形式行走，访问网格中的每个位置。每当移动到网格边界之外时，仍然继续行走（但随后可能会再次返回网格内部）。最终，你会访问网格中的所有 `rows * cols` 个单元格。  

返回一个坐标数组，按访问顺序记录网格中的位置。

**示例 1**  
输入: `rows = 1, cols = 4, rStart = 0, cStart = 0`  
输出: `[[0,0],[0,1],[0,2],[0,3]]`

**示例 2**  
输入: `rows = 5, cols = 6, rStart = 1, cStart = 4`  
输出: `[[1,4],[1,5],[2,5],[2,4],[2,3],[1,3],[0,3],[0,4],[0,5],[3,5],[3,4],[3,3],[3,2],[2,2],[1,2],[0,2],[4,5],[4,4],[4,3],[4,2],[4,1],[3,1],[2,1],[1,1],[0,1],[4,0],[3,0],[2,0],[1,0],[0,0]]`

**约束条件**  
- `1 <= rows, cols <= 100`  
- `0 <= rStart < rows`  
- `0 <= cStart < cols`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是“按题目说的那样走”。  
我们从起点 `(rStart, cStart)` 开始，先向东走一步，然后顺时针依次向 **南 → 西 → 北**，每转一次方向就把步数加一（因为螺旋每转一圈，边长会增长）。  
在走的过程中：

- 把每一次落在 **格子内部** 的坐标记下来（即 `0 ≤ r < rows` 且 `0 ≤ c < cols`），
- 只要记录的坐标数等于 `rows * cols`，说明所有格子都被访问过，结束。

这里用到的唯一数据结构是 **列表**（list），它就像装了很多小纸条的盒子，往里 `append`（添加）坐标就相当于往盒子里放纸条。

> **为什么正确？**  
> 螺旋的走法在数学上已经被证明能遍历整个平面（只要不停地向外扩展步长）。因为我们一直按照这个规律前进，并且只在坐标落在矩阵内部时才记录，所以最终一定会把矩阵里的每个格子都记下来。

> **时间/空间复杂度**  
> - **时间**：我们每走一步都要检查一次是否在矩阵内部，这一步的代价是 **O(1)**。要遍历完所有格子，最坏情况下需要走到矩阵外面再回来，步数大约是 `O(rows * cols)` 的常数倍（事实上最多走到外层的一个矩形框），所以整体时间是 **O(rows·cols)**。  
>   用大白话说，假设矩阵有 100×100=10 000 个格子，程序大概会走 10 000~12 000 步，步数随格子数线性增长。
> - **空间**：只用了一个结果列表来存放坐标，列表里恰好有 `rows·cols` 个元素，所以是 **O(rows·cols)** 的额外空间（不算输出本身）。

#### 代码（Python）

```python
def spiralMatrixIII(rows: int, cols: int, rStart: int, cStart: int):
    # 记录答案的列表
    ans = []
    # 已经记录的格子数量
    visited = 0
    # 当前坐标
    r, c = rStart, cStart

    # 四个方向：右、下、左、上（顺时针）
    # 每个方向对应的行、列增量
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # 第一次只走 1 步，随后每两次转向步数加 1
    step_len = 1          # 本次要走的格子数
    dir_idx = 0           # 当前方向在 dirs 中的下标

    # 只要还有格子没有被记录，就一直循环
    while visited < rows * cols:
        # 同一层螺旋要走两次“step_len”，比如右走 step_len， 下走 step_len，随后 step_len+1...
        for _ in range(2):
            dr, dc = dirs[dir_idx]          # 取出本次方向的增量
            for _ in range(step_len):
                # 把当前坐标记入答案（如果在矩阵内部）
                if 0 <= r < rows and 0 <= c < cols:
                    ans.append([r, c])
                    visited += 1
                    if visited == rows * cols:   # 已经全部记录完，直接返回
                        return ans
                # 向当前方向前进一步
                r += dr
                c += dc
            # 换下一个方向（顺时针）
            dir_idx = (dir_idx + 1) % 4
        # 完成两次转向后，步长加 1，进入下一层螺旋
        step_len += 1

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(rows·cols)` —— 每访问一个格子常数时间，整体随格子数线性增长。  
- **空间复杂度**：`O(rows·cols)` —— 结果列表需要存放所有格子的坐标。

---

### 2. 最优解

> 这里的“最优”指的仍然是 **O(rows·cols)** 时间，已经是不可再改进的下界。  
> 我们在思路上做的优化是：**不必每一步都检查四个方向是否需要转向**，而是直接按照“走 `step_len` 步 → 转向 → 再走 `step_len` 步 → 转向 → 步长+1” 的规律前进。这样代码更简洁，思路更清晰。

#### 思路  

从暴力解可以看到，**慢的地方**其实并不是时间，而是代码的可读性：我们每走一步都要写 `if` 判断，循环嵌套层数较多。  
要让思路更“一眼看懂”，可以把螺旋的“步长变化”抽象出来：

1. **方向顺序**：右 → 下 → 左 → 上，永远循环。把它们放进一个数组 `dirs`，用下标 `dir_idx` 取当前方向。
2. **步长**：第一次右走 1 步，随后 **每转两次方向**（即完成一次“外层”），步长就加 1。  
   - 用变量 `step_len` 记录当前需要走的格子数。  
   - 在外层 `while` 循环里，先走 `step_len` 步，再转向；再走 `step_len` 步，再转向；最后 `step_len += 1`，进入下一层。
3. **记录坐标**：只要当前坐标落在矩阵内部，就把它加入答案。  
   - 这里不需要额外的哈希表或访问标记，因为题目保证每个格子只会被访问一次。

> **类比**：想象你站在一个大圆形的舞池中心，手里拿着一根绳子。每转一次（顺时针），绳子会拉长一点点。你每走一步就把脚印留在地上，只有落在舞池内部的脚印才算数。等到所有格子都有脚印，舞会结束。

#### 代码（Python）

```python
def spiralMatrixIII(rows: int, cols: int, rStart: int, cStart: int):
    # 结果列表，预先分配容量可以稍微提升性能（非必需）
    ans = []
    # 记录已经收集到的格子数
    collected = 0

    # 四个方向，顺时针：右、下、左、上
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # 当前坐标
    r, c = rStart, cStart
    # 当前步长，初始为 1
    step_len = 1
    # 当前方向下标
    dir_idx = 0

    # 只要还有格子未被收集，就继续螺旋
    while collected < rows * cols:
        # 每层螺旋需要走两段相同长度的路（例如右 2 步、下 2 步）
        for _ in range(2):
            dr, dc = dirs[dir_idx]          # 取当前方向的增量
            for _ in range(step_len):
                # 若在矩阵内部，则保存坐标
                if 0 <= r < rows and 0 <= c < cols:
                    ans.append([r, c])
                    collected += 1
                    if collected == rows * cols:
                        return ans
                # 前进一步
                r += dr
                c += dc
            # 方向顺时针转一次
            dir_idx = (dir_idx + 1) % 4
        # 完成两次转向后，步长 +1，进入外层
        step_len += 1

    return ans
```

> **为什么这已经是最优？**  
> - **时间**：每个格子只检查一次 `O(1)`，整体 `O(rows·cols)`，不可能再更快，因为我们必须把每个格子都输出。  
> - **空间**：只用了输出列表本身，额外空间 `O(1)`（不计答案），已经是最小的额外开销。

#### 复杂度  

- **时间复杂度**：`O(rows·cols)` —— 每个格子恰好被访问一次。  
- **空间复杂度**：`O(rows·cols)` —— 结果列表占用的空间；除去答案本身，额外空间只有常数级变量 `O(1)`。

---

## 心得

- **核心技巧**：**螺旋遍历**（用步长递增的方式模拟顺时针螺旋）  
- **适用的题型**：  
  1. *Spiral Matrix*（把矩阵转成螺旋顺序）  
  2. *Zigzag Conversion*（虽然是斜向，但同样需要把方向和步长抽象）  
  3. *Robot Room Cleaner*（在未知区域按螺旋方式遍历）  
- **一句话总结解题钥匙**：**把“向外扩展的螺旋”拆解为“走 step_len 步 → 换方向 → 再走 step_len 步 → 步长+1”。**

---

## 反思

- **第一反应**：看到“顺时针螺旋”，立刻想到“模拟走一步一步”。  
- **最容易踩的坑**：  
  - 忘记在 **转向两次后** 再增加步长，导致路径不对。  
  - 边界判断写错（比如 `<= rows`），会把超出矩阵的坐标也加入答案。  
  - 当 `rows` 或 `cols` 为 1 时，螺旋会直接在同一直线上，需要保证循环仍能正常结束。  
- **下次遇到同类题**：第一步先**写出方向数组和步长递增的规律**，再在循环里判断“是否在矩阵内部”，这样可以避免大多数逻辑错误。