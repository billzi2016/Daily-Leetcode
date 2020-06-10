# #892. 3D 形体的表面积 / Surface Area of 3D Shapes

> 难度：简单 · 标签：Array、Math、Geometry、Matrix · [LeetCode 链接](https://leetcode.com/problems/surface-area-of-3d-shapes/)

---

## 题目（英文原版）

**Description**

You are given an n x n grid where you have placed some 1 x 1 x 1 cubes. Each value v = grid[i][j] represents a tower of v cubes placed on top of cell (i, j).
After placing these cubes, you have decided to glue any directly adjacent cubes to each other, forming several irregular 3D shapes.
Return the total surface area of the resulting shapes.
Note: The bottom face of each shape counts toward its surface area.

**Examples**

**Example 1:**

```
Input: grid = [[1,2],[3,4]]
Output: 34
```

**Example 2:**

```
Input: grid = [[1,1,1],[1,0,1],[1,1,1]]
Output: 32
```

**Example 3:**

```
Input: grid = [[2,2,2],[2,1,2],[2,2,2]]
Output: 46
```

**Constraints**

- n == grid.length == grid[i].length
- 1 <= n <= 50
- 0 <= grid[i][j] <= 50

---

## 题目（中文翻译）

给定一个 $n \times n$ 网格（grid），其中在每个单元格 $(i, j)$ 上放置若干个 $1 \times 1 \times 1$ 立方体（cube）。网格中的数值 `v = grid[i][j]` 表示在单元格 $(i, j)$ 上堆叠的高度为 $v$ 的塔（tower），即该位置上有 $v$ 个立方体竖直堆叠。

在放置完所有立方体后，你会把所有**直接相邻**（directly adjacent）的立方体粘合在一起，形成若干不规则的三维形体（irregular 3D shapes）。

请返回这些形体的**总表面积**（surface area）。  
注意：每个形体的底面（bottom face）也计入表面积。

---

### 示例

**示例 1**

```
输入: grid = [[1,2],[3,4]]
输出: 34
```

**示例 2**

```
输入: grid = [[1,1,1],[1,0,1],[1,1,1]]
输出: 32
```

**示例 3**

```
输入: grid = [[2,2,2],[2,1,2],[2,2,2]]
输出: 46
```

---

### 约束条件

- $n == \text{grid}.length == \text{grid}[i].\text{length}$
- $1 \le n \le 50$
- $0 \le \text{grid}[i][j] \le 50$

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把每一个小立方体都拆开来看，先假设它是孤立的，那么它有 **6 个面**（上、下、左、右、前、后）都算在表面积里。  
接着检查它的 6 个相邻位置（上下左右以及上下层），如果相邻位置也有立方体，则这两块会粘在一起，这对面就不再算表面积。  

> **类比**：想象每个立方体是一张纸做的正方体模型，六个面都是可以看到的“纸”。当两块模型紧贴在一起时，贴合的两张纸会被“粘住”，从外观看不到了。  

把整个网格里所有立方体都这么处理，最后把每块立方体剩下的可见面数加起来，就是答案。  

**为什么正确**：  
- 每块立方体的 6 面是完整的基准。  
- 只要把所有与它相邻、实际接触的面全部剔除，剩下的就是外部可见的面。  
- 所有立方体的可见面求和，就是整个 3D 形状的总表面积（包括底面，因为题目要求底面计数）。

#### 代码（Python）  

```python
from typing import List

def surfaceArea_brute(grid: List[List[int]]) -> int:
    n = len(grid)                       # 网格的大小 n×n
    total = 0                           # 累计表面积

    # 方向向量：上、下、左、右、前、后
    dirs = [(0, 0, 1), (0, 0, -1),      # z 方向：上层、下层
            (0, 1, 0), (0, -1, 0),      # y 方向：前后
            (1, 0, 0), (-1, 0, 0)]      # x 方向：左右

    for i in range(n):
        for j in range(n):
            h = grid[i][j]              # 该格子的塔高
            for k in range(h):          # 把每一个小立方体都遍历一次
                # 每块立方体默认有 6 个面
                total += 6
                # 检查 6 个相邻位置是否也有立方体
                for di, dj, dk in dirs:
                    ni, nj, nk = i + di, j + dj, k + dk
                    # 只要相邻位置在网格范围内且高度大于等于 nk+1，就说明有立方体相邻
                    if 0 <= ni < n and 0 <= nj < n and nk >= 0 and nk < grid[ni][nj]:
                        # 相邻的面被粘在一起，需要减掉 2（本块和邻块各算了一次）
                        total -= 2
    return total
```

> **关键行注释**  
> - `total += 6`：每块立方体先算上全部 6 面。  
> - `if 0 <= ni < n and 0 <= nj < n and nk >= 0 and nk < grid[ni][nj]`：判断相邻位置是否真的有立方体。  
> - `total -= 2`：因为相邻的两块立方体各自都把这面对成“可见”，所以要减掉 2 次。

#### 复杂度  

- **时间复杂度**：`O(n³)`。  
  - 外层两层遍历网格是 `O(n²)`，内部再遍历每格子里的每个立方体（最高 50），最坏情况是 `n² * 50 ≈ O(n³)`。  
  - 大白话：如果把每个小立方体想象成一颗糖果，最多要检查 125,000 颗糖果的 6 个邻居，算起来会慢一点。  
- **空间复杂度**：`O(1)`（不计输入），只用了几个常数级的变量。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于逐个立方体遍历**，尤其是每块立方体都要检查 6 次邻居，导致 `O(n³)`。  
实际上，我们不需要把每个立方体拆开来算，只要从 **每个格子**（即每根塔）直接计算它对表面积的贡献即可。  

**关键观察**  

1. **顶部和底部**：只要格子里有立方体（高度 `h > 0`），顶部和底部各贡献 1，合计 2。  
2. **四个侧面**：  
   - 对于某个方向（例如向左），如果左边相邻格子的高度是 `h_left`，那么本格子在左侧“露出”的高度是 `max(h - h_left, 0)`。  
   - 如果左边没有格子（即在边界），把 `h_left` 当作 0，整个高度 `h` 都会露出。  
   - 四个方向分别计算，累加即可。  

**公式**（对每个格子 `grid[i][j] = h`）  

```
if h > 0:
    area += 2                         # 上下表面
    area += max(h - up,    0)         # 与上方格子比较
    area += max(h - down,  0)         # 与下方格子比较
    area += max(h - left,  0)         # 与左侧格子比较
    area += max(h - right, 0)         # 与右侧格子比较
```

这里的 `up/down/left/right` 是相邻格子的高度，若越界则视为 0。  

> **类比**：把每根塔想象成一座楼房，楼房的屋顶和地基一定能看到。四面墙只在比相邻楼房高的那部分才会外露，就像两栋楼之间的墙只露出高差的那段。  

#### 代码（Python）  

```python
from typing import List

def surfaceArea(grid: List[List[int]]) -> int:
    n = len(grid)
    area = 0

    for i in range(n):
        for j in range(n):
            h = grid[i][j]
            if h == 0:
                continue                 # 没有立方体直接跳过

            # 顶部 + 底部
            area += 2

            # 四个方向的相邻高度，越界当作 0
            up    = grid[i-1][j] if i > 0 else 0
            down  = grid[i+1][j] if i < n-1 else 0
            left  = grid[i][j-1] if j > 0 else 0
            right = grid[i][j+1] if j < n-1 else 0

            # 侧面只算比邻居高的那部分
            area += max(h - up, 0)
            area += max(h - down, 0)
            area += max(h - left, 0)
            area += max(h - right, 0)

    return area
```

> **关键行注释**  
> - `if h == 0: continue`：空格子直接跳过，省去不必要的计算。  
> - `up = grid[i-1][j] if i > 0 else 0`：边界处理，把外面的高度视作 0。  
> - `area += max(h - neighbor, 0)`：只把高于邻居的那段墙算进表面积。

#### 复杂度  

- **时间复杂度**：`O(n²)`。只遍历一次 `n × n` 的网格，每格子做常数次计算。  
  - 与暴力解相比，从 “每块小糖果检查 6 次” 降到了 “每根塔子检查 4 次”。  
- **空间复杂度**：`O(1)`（不计输入），只用了几个临时变量。  

---

## 心得  

- **核心技巧**：**从局部（每格子）直接求贡献**，而不是逐个立方体枚举。  
- **适用场景**：  
  1. 计算网格或矩阵中“表面积”“周长”等几何量时，常用 **邻格比较**（如 LeetCode 892. Surface Area of 3D Shapes）。  
  2. “岛屿周长” 类题目（LeetCode 463. Island Perimeter），同样是把每块土地的四条边与相邻土地比较。  
  3. “矩形相交面积” 或 “二维矩阵的外接矩形周长” 之类，需要 **局部贡献 + 边界处理** 的问题。  
- **一句话总结**：把每个单元的“可见面”看成 **自身高度减去相邻高度的正差**，再加上必露出的上下表面，即可线性求解表面积。  

---

## 反思  

- **第一反应**：把所有小立方体拆开逐个计数——直觉上最安全，但容易忽略时间复杂度。  
- **最容易踩的坑**：  
  - **边界条件**：格子在矩阵最外层时，没有相邻格子，需要把相邻高度视为 0。  
  - **高度为 0 的格子**：如果忘记跳过，会导致错误的 “上、下” 计数（0 仍会加 2）。  
  - **负数防护**：`max(h - neighbor, 0)` 必须防止出现负数，否则会把本不该减的面积抵消掉。  
- **下次类似题目**：第一步想到 **“每个单元的贡献 = 自己的属性（高度/面积） - 与相邻单元的重叠部分”**，然后逐格累加即可。