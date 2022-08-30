# #1914. **循环旋转网格** / Cyclically Rotating a Grid

> 难度：中等 · 标签：Array、Matrix、Simulation · [LeetCode 链接](https://leetcode.com/problems/cyclically-rotating-a-grid/)

---

## 题目（英文原版）

**Description**

You are given an m x n integer matrix grid​​​, where m and n are both even integers, and an integer k.
The matrix is composed of several layers, which is shown in the below image, where each color is its own layer:
A cyclic rotation of the matrix is done by cyclically rotating each layer in the matrix. To cyclically rotate a layer once, each element in the layer will take the place of the adjacent element in the counter-clockwise direction. An example rotation is shown below:
Return the matrix after applying k cyclic rotations to it.

**Examples**

**Example 1:**

```
Input: grid = [[40,10],[30,20]], k = 1
Output: [[10,20],[40,30]]
Explanation: The figures above represent the grid at every state.
```

**Example 2:**

```
Input: grid = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]], k = 2
Output: [[3,4,8,12],[2,11,10,16],[1,7,6,15],[5,9,13,14]]
Explanation: The figures above represent the grid at every state.
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 2 <= m, n <= 50
- Both m and n are even integers.
- 1 <= grid[i][j] <= 5000
- 1 <= k <= 109

---

## 题目（中文翻译）

给定一个 *m* × *n* 的整数矩阵（matrix） `grid`，其中 *m* 和 *n* 都是偶数，以及一个整数 `k`。  
矩阵由若干层（layer）组成，如下图所示，每种颜色对应一个层：

对矩阵进行一次循环旋转（cyclic rotation），即对矩阵中的每一层都进行循环旋转。对某一层进行一次循环旋转时，层中的每个元素都会移动到其在逆时针方向（counter‑clockwise direction）相邻的位置。下面的示例展示了一次旋转的过程：

返回对矩阵执行 `k` 次循环旋转后的结果矩阵。

---

### 示例

**示例 1**

```text
Input: grid = [[40,10],[30,20]], k = 1
Output: [[10,20],[40,30]]
Explanation: 上图展示了每一步的网格状态。
```

**示例 2**

```text
Input: grid = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]], k = 2
Output: [[3,4,8,12],[2,11,10,16],[1,7,6,15],[5,9,13,14]]
Explanation: 上图展示了每一步的网格状态。
```

---

### 约束条件

- `m == grid.length`
- `n == grid[i].length`
- `2 <= m, n <= 50`
- `m` 和 `n` 均为偶数
- `1 <= grid[i][j] <= 5000`
- `1 <= k <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

把矩阵想象成一层层套在一起的“围栏”。最外层是矩形的四条边，往里一层又是一个更小的矩形……  
**暴力做法**就是：

1. **逐层取出**：把每一层的元素按顺时针（或逆时针）顺序搬到一个一维列表 `layer` 中。  
   - 这一步类似把一本字典里某一章节的所有词抄到一张纸上，`layer` 就是那张纸。  
2. **循环左移 k 步**：对 `layer` 做 `k % len(layer)` 次左移（逆时针方向）。左移相当于把纸上的词往左搬，超出左端的词再从右端补回来。  
3. **写回矩阵**：把搬好的 `layer` 再按同样的路径写回原来的位置。  

因为题目要求 **每层都要逆时针旋转**，只要把每层单独处理，互不影响。

**为什么正确**  
- 每层的元素在旋转后仍然只会出现在同一层的其它位置，层之间没有交叉。  
- 把层展开成一维列表后，循环左移恰好对应“每个元素向逆时针的相邻位置移动”。  

**时间/空间分析**  
- **时间**：我们遍历每个格子一次把它放进对应层的列表，又遍历一次把它写回去。总共 `O(m·n)`。  
- **空间**：需要额外的列表来存放每层的元素，最坏情况下（最外层）会有 `2·(m+n-2)` 个元素，仍然是 `O(m·n)`（与输入规模同阶）。  

> **大白话**：`O(m·n)` 就是说，矩阵有多少格子，就需要处理多少次，和格子数成正比；`O(m·n)` 的空间是说，最坏情况下我们可能把所有格子都搬到一张纸上再放回去。

#### 代码（Python）  

```python
def rotateGrid_bruteforce(grid, k):
    """
    暴力实现：逐层展开、左移 k 步、再写回矩阵
    """
    m, n = len(grid), len(grid[0])
    layers = min(m, n) // 2                 # 层数，外层算第 0 层

    for layer in range(layers):
        # ---------- 1. 把当前层的元素搬到一维列表 ----------
        elems = []

        # 上边（左→右），不包括右上角，因为会在右边再取到
        for col in range(layer, n - layer):
            elems.append(grid[layer][col])

        # 右边（上→下），不包括右下角
        for row in range(layer + 1, m - layer):
            elems.append(grid[row][n - 1 - layer])

        # 下边（右→左），不包括左下角
        for col in range(n - 2 - layer, layer - 1, -1):
            elems.append(grid[m - 1 - layer][col])

        # 左边（下→上），不包括左上角
        for row in range(m - 2 - layer, layer, -1):
            elems.append(grid[row][layer])

        # ---------- 2. 循环左移 ----------
        rot = k % len(elems)                # 只需要左移到余数步
        elems = elems[rot:] + elems[:rot]   # Python 切片实现左移

        # ---------- 3. 把旋转后的元素写回 ----------
        idx = 0

        for col in range(layer, n - layer):
            grid[layer][col] = elems[idx]; idx += 1
        for row in range(layer + 1, m - layer):
            grid[row][n - 1 - layer] = elems[idx]; idx += 1
        for col in range(n - 2 - layer, layer - 1, -1):
            grid[m - 1 - layer][col] = elems[idx]; idx += 1
        for row in range(m - 2 - layer, layer, -1):
            grid[row][layer] = elems[idx]; idx += 1

    return grid
```

#### 复杂度  

- **时间复杂度**：`O(m·n)`  
  - 解释：每个格子只会被读取一次、写回一次，和格子总数成线性关系。  
- **空间复杂度**：`O(m·n)`（最坏情况）  
  - 解释：我们用额外的列表存放一层的所有元素，最外层的长度接近矩阵周长 `2·(m+n-2)`，仍然是和格子数同阶。  

---  

### 2. 最优解  

#### 思路  

暴力解已经是 **线性时间**，已经无法再快（因为必须看所有格子）。  
真正的“最优”在于 **降低额外空间**：我们可以 **原地** 完成旋转，只使用 `O(1)` 额外空间（不计输出矩阵本身）。

思路步骤：

1. **把每层的元素视为一个环**，环的长度 `len = 2·(m + n - 4·layer) - 4`。  
2. 对每个环，我们只需要把它整体左移 `k % len` 步。左移可以通过**循环置换（cycle replacement）**一次完成，而不必额外建列表。  
   - 把环看成一个圆圈，先记住起点的值，然后沿着圆圈走 `step = k % len` 步，把前一个位置的值写到当前位，循环直到回到起点。  
   - 这类似把一串珠子顺时针移动，只需要手里拿一个珠子，沿路把珠子往前搬。  
3. 为了在环上“走”，我们需要一个**统一的坐标生成器**，把 `(row, col)` 按环的遍历顺序依次产生。  

这样我们只使用常数级的临时变量（如 `prev, cur, r, c`），空间降到 `O(1)`。

> **关键点**：  
> - 计算每层的实际旋转步数 `step = k % perimeter`，因为旋转 `perimeter` 步会回到原位。  
> - 循环置换必须确保每个位置只访问一次，否则会出现覆盖问题。  

#### 代码（Python）  

```python
def rotateGrid_optimal(grid, k):
    """
    最优实现：在原矩阵上原地完成每层的循环左移，只使用 O(1) 额外空间
    """
    m, n = len(grid), len(grid[0])
    layers = min(m, n) // 2

    for layer in range(layers):
        # ---------- 1. 计算当前层的周长 ----------
        top, left = layer, layer
        bottom, right = m - 1 - layer, n - 1 - layer
        perimeter = 2 * (bottom - top + right - left)   # 环的元素个数

        step = k % perimeter          # 实际需要移动的步数
        if step == 0:                 # 步数为 0，直接跳过本层
            continue

        # ---------- 2. 辅助函数：按照环的顺序遍历坐标 ----------
        def next_pos(r, c):
            """给定当前位置，返回环上顺时针的下一个位置"""
            if r == top and c < right:            # 在上边，往右走
                return r, c + 1
            if c == right and r < bottom:         # 在右边，往下走
                return r + 1, c
            if r == bottom and c > left:           # 在下边，往左走
                return r, c - 1
            # 否则在左边，往上走
            return r - 1, c

        # ---------- 3. 循环置换 ----------
        # 记录环上第一个位置的值，后面会放回起点
        r, c = top, left
        prev = grid[r][c]               # 起始元素暂存

        # 按照 step 步的距离循环遍历环，直到回到起点
        for _ in range(perimeter):
            # 计算下一个要写入的坐标
            nr, nc = next_pos(r, c)

            # 把 prev 写到下一个位置，同时拿到下一个位置原来的值
            cur = grid[nr][nc]          # 先取出后面的值，防止被覆盖
            grid[nr][nc] = prev         # 把前一个值搬进去
            prev = cur                  # 更新 prev 为刚才取出的值

            r, c = nr, nc               # 移动指针

            # 当我们刚好回到起点时，循环已经完成
            if (r, c) == (top, left):
                break

        # 注意：上面的循环已经把所有位置都正确填好，起点的值已在最后一次写回
    return grid
```

> **代码说明**  
> - `next_pos` 把环看成顺时针走的路线（上→右→下→左），返回下一个坐标。  
> - `prev` 保存当前要搬走的元素，`cur` 暂存下一个位置的旧值，防止覆盖。  
> - 循环 `perimeter` 次保证遍历完整个环，`step` 已经在 `k % perimeter` 中处理，实际移动的距离体现在“每次搬一步”。  

#### 复杂度  

- **时间复杂度**：`O(m·n)`  
  - 解释：每个格子仍然只会被访问一次（读取 + 写入），所以和矩阵大小成线性关系。  
- **空间复杂度**：`O(1)`（不计输入矩阵本身）  
  - 解释：只用了常数个临时变量 `prev, cur, r, c`，没有额外的与 `m·n` 成正比的存储。  

相比暴力解，时间相同但空间大幅降低，尤其在矩阵较大时更友好。

---  

## 心得  

- **核心技巧**：把二维矩阵的每一层抽象成“一维环”，再对环进行循环左移。  
- **适用的题型**  
  1. **矩阵层旋转**（如 LeetCode 1904 `The Number of Full Rounds You Have Played` 中的层次遍历）  
  2. **螺旋顺序遍历/填充**（如 54 `Spiral Matrix`、59 `Spiral Matrix II`）  
  3. **图像/矩阵的环形平移**（如 1690 `Stone Game VII` 中的环形操作）  
- **一句话总结解题钥匙**：**把层拆成环，环上左移 `k % length`，再写回**。

---  

## 反思  

- **第一反应**：看到“层”“循环旋转”，马上想到把每层拉成一维数组再左移。  
- **最容易踩的坑**  
  - **边界错误**：遍历每层时容易把四个角重复或遗漏，尤其右边和下边的终止条件要仔细写。  
  - **k 很大**：直接循环 `k` 次会超时，必须先取模 `k % perimeter`。  
  - **奇数维度**：题目保证 `m,n` 为偶数，若忘记会在计算层数时出现 `min(m,n)//2` 失误。  
- **下次类似题**：第一步先 **确定层数 & 把层展平成一维**，再 **计算有效步数（取模）**，最后 **原地写回或使用额外数组**。  

祝你玩转矩阵层旋转！ 🎉