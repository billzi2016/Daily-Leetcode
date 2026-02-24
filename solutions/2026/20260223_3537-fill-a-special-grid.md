# #3537. 填充特殊网格 / Fill a Special Grid

> 难度：中等 · 标签：Array、Divide and Conquer、Matrix · [LeetCode 链接](https://leetcode.com/problems/fill-a-special-grid/)

---

## 题目（英文原版）

**Description**

You are given a non-negative integer n representing a 2n x 2n grid. You must fill the grid with integers from 0 to 22n - 1 to make it special. A grid is special if it satisfies all the following conditions:
Return the special 2n x 2n grid.
Note: Any 1x1 grid is special.

**Examples**

**Example 1:**

```
Input: n = 0
Output: [[0]]
Explanation:
The only number that can be placed is 0, and there is only one possible position in the grid.
```

**Example 2:**

```
Input: n = 1
Output: [[3,0],[2,1]]
Explanation:
The numbers in each quadrant are:
Since 0 < 1 < 2 < 3 , this satisfies the given constraints.
```

**Example 3:**

```
Input: n = 2
Output: [[15,12,3,0],[14,13,2,1],[11,8,7,4],[10,9,6,5]]
Explanation:

The numbers in each quadrant are:
This satisfies the first three requirements. Additionally, each quadrant is also a special grid. Thus, this is a special grid.
```

**Constraints**

- 0 <= n <= 10

---

## 题目（中文翻译）

给定一个非负整数 `n`，表示一个大小为 `2^n × 2^n` 的网格。请使用整数 `0` 到 `2^{2n} - 1`（共 `2^{2n}` 个数）填满整个网格，使其成为 **特殊网格**（special grid）。

**特殊网格的定义**（必须同时满足以下全部条件）：

1. 网格被划分为左上、右上、左下、右下四个象限（quadrant），每个象限的大小为 `2^{n-1} × 2^{n-1}`（当 `n = 0` 时，网格即为 `1 × 1` 的特殊网格）。
2. 四个象限中的元素满足严格的大小顺序：  
   - 右上象限的所有元素 < 右下象限的所有元素  
   - 右下象限的所有元素 < 左下象限的所有元素  
   - 左下象限的所有元素 < 左上象限的所有元素
3. 每个象限本身也必须是一个特殊网格（递归定义）。  
   - 注：任意 `1 × 1` 的网格天然满足特殊网格的条件。

返回满足上述要求的 `2^n × 2^n` 特殊网格。

> **提示**：当 `n = 0` 时，唯一可能的网格是 `[[0]]`，它显然满足所有条件。

---

## 示例

### 示例 1
```text
输入: n = 0
输出: [[0]]
解释:
唯一能放置的数字是 0，网格只有一个位置，显然满足要求。
```

### 示例 2
```text
输入: n = 1
输出: [[3,0],[2,1]]
解释:
四个象限分别为
- 右上象限: 0
- 右下象限: 1
- 左下象限: 2
- 左上象限: 3  

因为 0 < 1 < 2 < 3，满足上述大小顺序，且每个象限都是 1×1 的特殊网格。
```

### 示例 3
```text
输入: n = 2
输出: [[15,12,3,0],
       [14,13,2,1],
       [11,8,7,4],
       [10,9,6,5]]
解释:
四个 2×2 的象限分别为
- 右上象限: [[3,0],[2,1]]
- 右下象限: [[7,4],[6,5]]
- 左下象限: [[11,8],[10,9]]
- 左上象限: [[15,12],[14,13]]

右上象限的所有元素 < 右下象限的所有元素 < 左下象限的所有元素 < 左上象限的所有元素，满足大小顺序。  
此外，每个 2×2 的象限本身也符合特殊网格的定义（递归），因此整个 4×4 网格是特殊的。
```

---

## 约束条件
- `0 ≤ n ≤ 10`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是 **递归地构造** 小尺寸的特殊网格，再把它们拼成大尺寸的网格。  
把 2ⁿ × 2ⁿ 的格子分成四个等大的子格子（每个是 2ⁿ⁻¹ × 2ⁿ⁻¹），这四个子格子本身也必须是“特殊的”。  
如果我们已经会得到 `n‑1` 时的特殊网格 `sub`，只要给四个子格子分别加上不同的偏移量，就可以得到 `n` 时的答案。

> **类比**：把一个大的拼图分成四块，每块都是同样的图案，只是颜色（数值）整体向上提升了几档。  
> - **哈希表** 像字典，`key` 是格子坐标，`value` 是格子里放的数字。这里我们不需要真正的哈希表，只是把「坐标」和「数值」对应起来。  
> - **偏移量** 就像词典里每个单词的页码，只是这里的页码是 **统一加** 的常数。  

**为什么正确**  
- 题目要求每个 2ⁿ⁻¹ × 2ⁿ⁻¹ 的子格子本身必须是特殊的。递归保证了这点。  
- 题目还要求四个子格子之间的数值满足 “左上 > 左下 > 右下 > 右上”。我们通过给左上、左下、右下、右上分别加上 `3·size²、2·size²、1·size²、0`（`size = 2ⁿ⁻¹`）实现了这一顺序。  

**时间/空间复杂度**  
- 我们必须把每个格子都写上一个数字，最少要访问 `4ⁿ`（即 `2ⁿ·2ⁿ`）次，所以时间下界是 **O(4ⁿ)**，即 **O(N²)**（N = 2ⁿ）。  
- 暴力递归会在每一层都复制子矩阵，导致额外的临时列表开销，空间也会是 **O(N²)**（存放最终答案）加上递归栈深度 **O(n)**。  

#### 代码（Python）  

```python
def construct_grid_brutal(n: int):
    """
    递归构造特殊网格的“暴力”写法。
    只要能跑通就行，代码里每一步都有中文注释帮助理解。
    """
    # 基础情况：1×1 的网格只能放 0
    if n == 0:
        return [[0]]

    # 先递归得到规模更小的特殊网格（size = 2^(n-1)）
    smaller = construct_grid_brutal(n - 1)          # 这一步是核心的递归

    m = len(smaller)                # m = 2^(n-1)
    size_sq = m * m                 # size_sq = 4^(n-1)，后面用来计算偏移量

    # 四个子块分别需要加的偏移量
    #   左上  +3*size_sq
    #   左下  +2*size_sq
    #   右下  +1*size_sq
    #   右上  +0
    top_left  = [[x + 3 * size_sq for x in row] for row in smaller]
    top_right = [[x + 0 * size_sq for x in row] for row in smaller]
    bottom_left = [[x + 2 * size_sq for x in row] for row in smaller]
    bottom_right = [[x + 1 * size_sq for x in row] for row in smaller]

    # 把四块拼成大的 2^n × 2^n 矩阵
    new_grid = []
    for i in range(m):
        # 上半部分：左上 + 右上
        new_grid.append(top_left[i] + top_right[i])
    for i in range(m):
        # 下半部分：左下 + 右下
        new_grid.append(bottom_left[i] + bottom_right[i])

    return new_grid
```

#### 复杂度  

- **时间复杂度**：`O(N²)`（N = 2ⁿ）。我们必须遍历每个格子一次来写入数字。  
- **空间复杂度**：`O(N²)` 用于存放返回的二维列表，外加递归深度 `O(n)`（n ≤ 10，几乎可以忽略不计）。

---

### 2. 最优解  

#### 思路  

暴力解已经是 **线性时间**（相对于格子数）了，无法再快，因为每个格子必须写一个数字。  
所谓“最优”，指的是 **不产生额外的中间复制**，直接在同一块内存上填值。  
实现思路：

1. 先创建一个全 0 的 `2ⁿ × 2ⁿ` 空矩阵 `grid`。  
2. 用一次递归函数 `fill(k, r, c, base)`：  
   - `k` 表示当前子矩阵的层数（`k = 0` 时是 1×1）。  
   - `(r, c)` 是子矩阵左上角的坐标。  
   - `base` 是当前子矩阵中最小数字的起始值。  
3. 当 `k == 0` 时，把 `grid[r][c] = base`（因为只剩一个格子）。  
4. 否则，子矩阵大小为 `size = 2^{k-1}`，把四个象限分别递归：
   - **左上**：`fill(k-1, r, c, base + 3·size²)`  
   - **左下**：`fill(k-1, r+size, c, base + 2·size²)`  
   - **右下**：`fill(k-1, r+size, c+size, base + 1·size²)`  
   - **右上**：`fill(k-1, r, c+size, base + 0·size²)`  

> **类比**：把整个格子想成一本厚厚的相册，最左上角的页面（左上象限）放的是最新的、编号最大的照片；右上角放最旧的。我们每进入下一层，就把“相册的章节号”往后推 `size²`（因为每个子章节有 `size²` 张照片）。

这样只遍历一次格子，时间 `O(N²)`，空间只需要保存答案矩阵和递归栈 `O(N² + n)`，是最省内存的做法。

#### 代码（Python）  

```python
def construct_grid_optimal(n: int):
    """
    直接在同一块二维数组上填值的最优实现。
    时间 O(N²)，空间 O(N²)（仅存放答案）。
    """
    N = 1 << n                     # 2^n
    grid = [[0] * N for _ in range(N)]

    def fill(k: int, r: int, c: int, base: int):
        """
        递归填充子矩阵
        k    : 当前子矩阵的层数（k=0 时为 1×1）
        r,c  : 子矩阵左上角坐标
        base : 子矩阵中最小数字的起始值
        """
        if k == 0:                 # 只能放一个数
            grid[r][c] = base
            return

        size = 1 << (k - 1)        # 2^{k-1}
        block = size * size        # size² = 4^{k-1}

        # 按题目要求的顺序递归四个象限
        # 1️⃣ 左上  (最大的一段)
        fill(k - 1, r, c, base + 3 * block)
        # 2️⃣ 左下
        fill(k - 1, r + size, c, base + 2 * block)
        # 3️⃣ 右下
        fill(k - 1, r + size, c + size, base + 1 * block)
        # 4️⃣ 右上 (最小的一段)
        fill(k - 1, r, c + size, base + 0 * block)

    fill(n, 0, 0, 0)               # 从整体开始填
    return grid
```

#### 复杂度  

- **时间复杂度**：`O(N²)`，因为递归恰好访问每个格子一次，没有额外的复制操作。  
- **空间复杂度**：`O(N²)` 用于存放返回的矩阵，加上递归调用栈深度 `O(n)`（n ≤ 10），整体仍是线性于格子数。

---

## 心得  

- **核心技巧**：**分治（Divide and Conquer）** —— 把大问题拆成四个同构的子问题，分别加上不同的常数偏移后合并。  
- **适用题型**：  
  1. “把二维数组按象限递归填值” 类似题，如 *“Z‑order matrix”*、*“Gray code matrix”*。  
  2. 需要把一个整体划分为同构子结构并在子结构上做统一变换的题，例如 *“递归构造 Hilbert 曲线”*。  
  3. 任何要求 **每个子块满足相同性质** 的矩阵题。  

- **一句话总结解题钥匙**：**把大格子看成四块相同的“小格子”，先递归解决小格子，再统一加上对应的偏移量拼回去**。

---

## 反思  

- **第一反应**：看到“2ⁿ × 2ⁿ”以及“每个子格子也是特殊的”，立刻想到 **递归** 和 **分治**。  
- **最容易踩的坑**：  
  - **偏移量算错**：每个象限的基准应该是 `k·size²`，而不是 `k·size`，因为每个象限包含 `size²` 个数字。  
  - **坐标写反**：左上、左下、右下、右上的顺序一定要对应题目要求的 “左上 > 左下 > 右下 > 右上”。  
  - **溢出**：在 Python 中整数不溢出，但若用其他语言要注意 `int` 范围（这里 `n ≤ 10`，最大数字是 `2^{2·10}‑1 = 2^{20}‑1 ≈ 10⁶`，安全）。  
- **下次遇到同类题**：第一步就 **画出 n=1、n=2 的示例**，找出四块之间的数值关系，再用 **递归 + 常数偏移** 的思路实现。