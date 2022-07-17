# #1861. 旋转盒子 / Rotating the Box

> 难度：中等 · 标签：Array、Two Pointers、Matrix · [LeetCode 链接](https://leetcode.com/problems/rotating-the-box/)

---

## 题目（英文原版）

**Description**

You are given an m x n matrix of characters boxGrid representing a side-view of a box. Each cell of the box is one of the following:
The box is rotated 90 degrees clockwise, causing some of the stones to fall due to gravity. Each stone falls down until it lands on an obstacle, another stone, or the bottom of the box. Gravity does not affect the obstacles' positions, and the inertia from the box's rotation does not affect the stones' horizontal positions.
It is guaranteed that each stone in boxGrid rests on an obstacle, another stone, or the bottom of the box.
Return an n x m matrix representing the box after the rotation described above.

**Examples**

**Example 1:**

```
Input: boxGrid = [["#",".","#"]]
Output: [["."],
         ["#"],
         ["#"]]
```

**Example 2:**

```
Input: boxGrid = [["#",".","*","."],
              ["#","#","*","."]]
Output: [["#","."],
         ["#","#"],
         ["*","*"],
         [".","."]]
```

**Example 3:**

```
Input: boxGrid = [["#","#","*",".","*","."],
              ["#","#","#","*",".","."],
              ["#","#","#",".","#","."]]
Output: [[".","#","#"],
         [".","#","#"],
         ["#","#","*"],
         ["#","*","."],
         ["#",".","*"],
         ["#",".","."]]
```

**Constraints**

- m == boxGrid.length
- n == boxGrid[i].length
- 1 <= m, n <= 500
- boxGrid[i][j] is either '#', '*', or '.'.

---

## 题目（中文翻译）

给定一个 `m × n` 的字符矩阵 `boxGrid`，它表示一个盒子的侧视图。盒子中的每个单元格可能是以下三种之一：

- `#`：石头（stone）
- `*`：障碍物（obstacle）
- `.`：空格

将盒子顺时针旋转 **90 度**，此时部分石头会因重力而下落。每块石头会向下落到障碍物、另一块石头或盒子底部为止。重力不影响障碍物的位置，盒子旋转产生的惯性也不影响石头的水平位置。

题目保证 `boxGrid` 中的每块石头最初都已经停靠在障碍物、另一块石头或盒子底部。

返回一个 `n × m` 的矩阵，表示上述旋转并下落后的盒子状态。

---

## 示例

### 示例 1
**输入**
```text
boxGrid = [["#",".","#"]]
```
**输出**
```text
[["."],
 ["#"],
 ["#"]]
```

### 示例 2
**输入**
```text
boxGrid = [["#",".","*","."],
           ["#","#","*","."]]
```
**输出**
```text
[["#","."],
 ["#","#"],
 ["*","*"],
 [".","."]]
```

### 示例 3
**输入**
```text
boxGrid = [["#","#","*",".","*","."],
           ["#","#","#","*",".","."],
           ["#","#","#",".","#","."]]
```
**输出**
```text
[[".", "#", "#"],
 [".", "#", "#"],
 ["#", "#", "*"],
 ["#", "*", "."],
 ["#", ".", "*"],
 ["#", ".", "."]]
```

---

## 约束条件

- `m == boxGrid.length`
- `n == boxGrid[i].length`
- `1 ≤ m, n ≤ 500`
- `boxGrid[i][j]` 只会是 `'#'`、`'*'` 或 `'.'`。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
题目给出一个 `m × n` 的矩阵 `boxGrid`，其中  
- `'#'` 表示石头  
- `'*'` 表示障碍物  
- `'.'` 表示空格  

先把盒子顺时针旋转 90°，再让石头在 **重力** 作用下向“下”（即旋转后矩阵的下方）掉落，直到碰到障碍物、另一块石头或盒子底部。  

最直接的想法是：

1. **先旋转**：把原矩阵按照公式  
   `rotated[i][j] = boxGrid[m‑1‑j][i]`  
   直接生成一个 `n × m` 的新矩阵，这一步不涉及任何判断，只是把坐标搬过去。

2. **再掉落**：对旋转后的矩阵逐列（列对应原来的行）从下往上遍历。  
   - 对每一列，从最底部往上找空格 `'.'`。  
   - 当找到一个空格后，继续往上找最近的石头 `'#'`，且这两个位置之间不能有障碍物 `'*'`（如果有障碍物，石头会被阻挡，不能掉进去）。  
   - 找到后把石头搬到空格位置，原来的石头位置置为 `'.'`，继续向上搜索。  

这相当于“把所有可以掉落的石头都搬到最靠底部的空格”。  

> **类比**：想象你在玩“多米诺骨牌”。每一列的石头就像一排骨牌，障碍物是固定的墙，空格是可以让骨牌滑下去的坑。我们把每块石头从上往下“推”到最近的坑里。

**为什么正确**：  
- 旋转前后，障碍物 `'*'` 的位置是固定的（旋转后仍在相同的相对位置），而石头只能在没有障碍物的空格里下落。  
- 按列从下往上处理，保证每次移动的目标格子一定是该列当前最底部的空格，符合重力的自然顺序。  

**时间/空间复杂度的大白话**：  
- `O(m·n)` 表示我们要遍历矩阵里每一个格子一次，类似于把一张 `m` 行 `n` 列的表格每格都检查一遍。  
- `O(m·n)` 的空间意味着我们另外开辟了一张同样大小的表格来存放旋转后的结果，和原表格一样大。  

#### 代码（Python）  

```python
from typing import List

def rotate_the_box_brute(boxGrid: List[List[str]]) -> List[List[str]]:
    m, n = len(boxGrid), len(boxGrid[0])

    # 1️⃣ 先把盒子顺时针旋转 90 度，得到 n 行 m 列的矩阵
    rotated = [['' for _ in range(m)] for _ in range(n)]
    for i in range(n):                 # 新矩阵的行索引
        for j in range(m):             # 新矩阵的列索引
            rotated[i][j] = boxGrid[m - 1 - j][i]   # 坐标搬运

    # 2️⃣ 再让石头在旋转后的矩阵里“掉落”
    for col in range(m):               # 按列处理（每列对应原来的行）
        write_row = n - 1              # write_row 指向当前列最底部的空格位置
        row = n - 1
        while row >= 0:
            if rotated[row][col] == '*':          # 障碍物：下面再也不能放石头了
                write_row = row - 1                # 重置写指针到障碍物上面
                row -= 1
            elif rotated[row][col] == '#':        # 石头：尝试下落
                if write_row != row:               # 只在需要移动时才交换
                    rotated[write_row][col] = '#'
                    rotated[row][col] = '.'
                write_row -= 1                     # 下一个石头要放更上面
                row -= 1
            else:                                 # 空格 '.'，直接往上走
                row -= 1

    return rotated
```

#### 复杂度  

- **时间复杂度**：`O(m·n)`  
  - 旋转一步遍历所有格子一次，掉落一步同样遍历每列的每个格子一次。  
  - 用大白话说，就是“把整张表格看了一遍”。  

- **空间复杂度**：`O(m·n)`  
  - 需要额外的 `n × m` 矩阵来存放旋转后的结果。原始矩阵保持不变。  

---  

### 2. 最优解  

#### 思路  

暴力解已经是 **线性**（`O(m·n)`）的时间复杂度，已经非常快。  
唯一可以改进的地方是 **空间**：我们可以在 **原地** 完成旋转和掉落，只使用 `O(1)`（常数）额外空间（不计输出矩阵本身）。  

实现思路分两步：

1. **先把每一行的石头向右侧“滑动”**（等价于在原矩阵中模拟重力向下的效果）。  
   - 对每一行从右往左遍历，用两个指针 `write`（写指针）和 `read`（读指针）。  
   - `write` 指向当前行中可以放石头的最右侧空格；`read` 寻找左侧最近的石头。  
   - 遇到障碍物 `'*'` 时，`write` 必须重新定位到障碍物左侧，因为石头不能穿过障碍物。  
   - 这样每行的石头都会被“推到右边”，相当于在未旋转之前已经完成了“下落”。  

2. **再把矩阵顺时针旋转 90°**，**就可以直接原地写回**（因为已经没有空格会被石头再覆盖）。  
   - 旋转可以使用 **转置 + 行翻转** 的技巧：  
     - 先对 `m × n` 矩阵做转置，得到 `n × m`（需要新矩阵，因为行列数改变），  
     - 再把每一行（即原来的列）反转顺序。  
   - 这里仍然需要一个新的 `n × m` 矩阵来存放结果，但**不需要**再额外的 `O(m·n)` 辅助空间用于掉落。  

> **关键点**：把掉落的工作提前到旋转之前完成，这样在旋转时不必再遍历每列寻找石头和空格，直接把已经排好序的行写进去即可。

#### 代码（Python）  

```python
from typing import List

def rotate_the_box_opt(boxGrid: List[List[str]]) -> List[List[str]]:
    m, n = len(boxGrid), len(boxGrid[0])

    # ---------- 1️⃣ 先在每一行把石头往右推（模拟下落） ----------
    for r in range(m):
        write = n - 1                     # 写指针：当前行最右侧可以放石头的位置
        for c in range(n - 1, -1, -1):    # 从右往左遍历
            if boxGrid[r][c] == '*':      # 障碍物出现，写指针重新定位到左侧
                write = c - 1
            elif boxGrid[r][c] == '#':    # 找到石头
                if write != c:            # 需要移动
                    boxGrid[r][write] = '#'
                    boxGrid[r][c] = '.'
                write -= 1                # 下一个石头要放更左边
            # '.' 什么也不做，继续往左

    # ---------- 2️⃣ 再把矩阵顺时针旋转 90° ----------
    # 创建 n 行 m 列的结果矩阵
    rotated = [['' for _ in range(m)] for _ in range(n)]
    for r in range(m):
        for c in range(n):
            # 旋转公式：新矩阵的 (c, m-1-r) 位置对应原矩阵 (r, c)
            rotated[c][m - 1 - r] = boxGrid[r][c]

    return rotated
```

#### 复杂度  

- **时间复杂度**：`O(m·n)`  
  - 第一步遍历每行一次，第二步遍历每个格子一次，总共两遍矩阵。  
  - 与暴力解相同，但常数更小（没有在每列内部再找空格/石头的嵌套循环）。  

- **空间复杂度**：`O(m·n)`（输出矩阵）  
  - 额外的工作只用了 `O(1)` 的指针变量。  
  - 与暴力解相比，**不需要**再额外开辟一个同等大小的“掉落过程”临时矩阵，空间占用更紧凑。  

---  

## 心得  

- **核心技巧**：先在原矩阵内部完成“石头下落”操作（**双指针**在每行内滑动），再一次性旋转矩阵。  
- **适用的题型**：  
  1. “重力下落”类题目（如 **Gravity Flip**、**Falling Squares**）。  
  2. 需要在 **二维网格** 中做 **行/列的压缩**（如 **Move Zeroes in 2D**、**Shift Grid**）。  
  3. 需要 **矩阵旋转** 再处理的题目（如 **Rotate Image**、**Spiral Matrix**）。  
- **一句话总结解题钥匙**：**把“下落”提前到旋转前，用双指针把石头压到最右侧，再一次性旋转即可。**  

---  

## 反思  

- **第一反应**：看到“旋转 90° 并下落”，直接想到先旋转再逐列模拟下落，写出最直观的暴力实现。  
- **最容易踩的坑**：  
  - **障碍物阻挡**：在掉落时必须判断 `'*'`，否则石头会错误地穿过去。  
  - **写指针位置更新**：障碍物出现后要把 `write` 移到障碍物左侧（或上方），否则会把石头放到障碍物上面。  
  - **边界条件**：只有一行或一列时，循环仍需正常工作。  
- **下次类似题目第一步**：先思考是否可以把 **重力/压缩** 操作提前到 **原始坐标系** 中完成，用 **双指针** 在行或列里一次遍历把元素“压”到目标位置，再再做其它几何变换（旋转、翻转）。这样往往能把空间和时间都控制在最优。