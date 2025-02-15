# #3071. 在网格上写字母 Y 的最少操作次数 / Minimum Operations to Write the Letter Y on a Grid

> 难度：中等 · 标签：Array、Hash Table、Matrix、Counting · [LeetCode 链接](https://leetcode.com/problems/minimum-operations-to-write-the-letter-y-on-a-grid/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed n x n grid where n is odd, and grid[r][c] is 0, 1, or 2.
We say that a cell belongs to the Letter Y if it belongs to one of the following:
The Letter Y is written on the grid if and only if:
Return the minimum number of operations needed to write the letter Y on the grid given that in one operation you can change the value at any cell to 0, 1, or 2.

**Examples**

**Example 1:**

```
Input: grid = [[1,2,2],[1,1,0],[0,1,0]]
Output: 3
Explanation: We can write Y on the grid by applying the changes highlighted in blue in the image above. After the operations, all cells that belong to Y, denoted in bold, have the same value of 1 while those that do not belong to Y are equal to 0.
It can be shown that 3 is the minimum number of operations needed to write Y on the grid.
```

**Example 2:**

```
Input: grid = [[0,1,0,1,0],[2,1,0,1,2],[2,2,2,0,1],[2,2,2,2,2],[2,1,2,2,2]]
Output: 12
Explanation: We can write Y on the grid by applying the changes highlighted in blue in the image above. After the operations, all cells that belong to Y, denoted in bold, have the same value of 0 while those that do not belong to Y are equal to 2. 
It can be shown that 12 is the minimum number of operations needed to write Y on the grid.
```

**Constraints**

- 3 <= n <= 49
- n == grid.length == grid[i].length
- 0 <= grid[i][j] <= 2
- n is odd.

---

## 题目（中文翻译）

**描述**  
给定一个下标从 0 开始的 $n \times n$ 网格 `grid`，其中 $n$ 为奇数，且 `grid[r][c]` 的取值只能是 0、1 或 2。  
我们称一个单元格属于字母 Y（Letter Y），如果它满足以下任意一种条件：  
（此处应列出具体的形状条件，原题目中已省略）

当且仅当网格中所有属于字母 Y 的单元格的值相同，且所有不属于字母 Y 的单元格的值相同（两者的值可以相等也可以不相等），我们认为字母 Y 已经写在网格上。  

返回在一次操作中可以将任意单元格的值改为 0、1 或 2 的前提下，使网格上写出字母 Y 所需的最少操作次数。

**示例**

**示例 1**  
```text
输入: grid = [[1,2,2],[1,1,0],[0,1,0]]
输出: 3
解释: 如上图所示，我们对标记为蓝色的单元格进行修改后即可得到字母 Y。修改后，所有属于 Y 的单元格（加粗部分）统一为 1，而不属于 Y 的单元格的值为 0。可以证明，3 是完成该操作的最小次数。
```

**示例 2**  
```text
输入: grid = [[0,1,0,1,0],[2,1,0,1,2],[2,2,2,0,1],[2,2,2,2,2],[2,1,2,2,2]]
输出: 12
解释: 如上图所示，我们对标记为蓝色的单元格进行修改后即可得到字母 Y。修改后，所有属于 Y 的单元格（加粗部分）统一为 0，而不属于 Y 的单元格统一为 2。可以证明，12 是完成该操作的最小次数。
```

**约束条件**  
- $3 \le n \le 49$
- $n = \text{grid.length} = \text{grid}[i].\text{length}$
- $0 \le \text{grid}[i][j] \le 2$
- $n$ 为奇数

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

先把「写好字母 Y」的形状在网格上画出来。  
因为 **n 为奇数**，我们可以把中心格记作 `(mid, mid)`，其中 `mid = n // 2`。  

- **上半部分**：从最上面一行开始，两条对称的斜线一直走到中心格。  
  - 左斜线的格子满足 `r == c`（左上到左下的对角线）  
  - 右斜线的格子满足 `r + c == n - 1`（右上到右下的对角线）  
  - 只取 `r ≤ mid` 的那些格子，因为斜线在到达中心后就不再继续。  

- **下半部分**：从中心格往下一直是一条竖直的线，所有格子满足 `c == mid` 且 `r ≥ mid`。  

把这两块格子合在一起，就是「属于字母 Y」的所有格子。  

> **类比**：把网格想象成一张纸，`mid` 行/列就是纸的中线。斜线就像两根笔画从左上、右上斜着走到中线的交点，然后再往下画一根直线。

题目要求：  
- 所有属于 Y 的格子必须 **统一成同一个数**（0、1 或 2）。  
- 其余格子也必须 **统一成同一个数**（同样是 0、1 或 2，可能和 Y 的数相同）。  

**最直接的办法**是：遍历所有可能的「Y 的数」`a`（3 种）和「非 Y 的数」`b`（同样 3 种），分别计算把每个格子改成对应数值需要几次操作，取最小值。

- 对每个格子，若它已经是目标数值，就不需要操作；否则就需要 1 次操作（把它改成目标值）。
- 统计「属于 Y」的格子数 `cntY`，以及「不属于 Y」的格子数 `cntN`（`cntN = n*n - cntY`），再分别统计这两块区域里每种数值出现的次数。

**为什么正确**  
因为我们枚举了所有合法的「Y 的数」和「非 Y 的数」组合，必然会覆盖最优解。对每一种组合，计算得到的操作次数就是把当前网格变成该组合所需要的最少操作数；取最小即得到全局最优。

**时间/空间分析（大白话）**  
- 我们要看每个格子一次，算它属于哪块（Y 还是非 Y），并把它的数值记下来。网格里最多有 `49*49 = 2401` 个格子，遍历一次就是 **O(n²)**，这里的 `n` 是网格的边长。  
- 枚举 3×3=9 种数值组合，这个常数很小，仍然是 O(n²)。  
- 只用几个计数器（每块 3 种数值的出现次数），占用的额外空间是 **O(1)**，即不随网格大小增长。

#### 代码（Python）

```python
def min_operations_to_write_y(grid):
    n = len(grid)
    mid = n // 2                     # 中心行/列的下标

    # 统计 Y 区域和非 Y 区域中 0/1/2 各出现了多少次
    # cntY[v] 表示 Y 区域里值为 v 的格子数，cntN 同理
    cntY = [0, 0, 0]
    cntN = [0, 0, 0]

    for r in range(n):
        for c in range(n):
            # 判断 (r, c) 是否在 Y 上
            in_y = False
            if r <= mid:                     # 上半部分：两条斜线
                if r == c or r + c == n - 1:
                    in_y = True
            else:                            # 下半部分：中间竖线
                if c == mid:
                    in_y = True

            val = grid[r][c]                # 0 / 1 / 2
            if in_y:
                cntY[val] += 1
            else:
                cntN[val] += 1

    total_y = sum(cntY)          # Y 区域的格子总数
    total_n = sum(cntN)          # 非 Y 区域的格子总数

    ans = float('inf')
    # 枚举 Y 的目标数 a (0/1/2) 和非 Y 的目标数 b (0/1/2)
    for a in range(3):
        for b in range(3):
            # 需要改动的格子数 = 区域总数 - 已经是目标数的格子数
            ops = (total_y - cntY[a]) + (total_n - cntN[b])
            ans = min(ans, ops)

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)` — 只遍历一次网格，`n` 是边长。  
  大白话：如果网格是 10×10，最多看 100 次格子；如果是 49×49，最多看 2401 次格子，都是线性增长的。  
- **空间复杂度**：`O(1)` — 只用了几个固定大小的计数器，和网格大小无关。

---

### 2. 最优解  

#### 思路  

暴力解已经是 **线性遍历 + 常数枚举**，时间已经是 `O(n²)`，这已经是该问题的下界，因为我们必须检查每个格子到底属于 Y 还是不属于 Y，才能统计出现次数。  

唯一可以改进的地方是 **代码可读性和实现细节**，让判断「是否在 Y 上」更加直观、避免重复判断。我们把「Y 的形状」抽象成两个集合：

1. **上半部的两个对角线**（只取到中心行）  
2. **中间竖线的下半部**（从中心行往下）

我们可以在一次遍历中直接根据行号 `r` 判断所属区域，而不必每次都写两层 `if`。另外，使用 **列表推导** 或 **数组** 来一次性保存所有 Y 坐标，也是一种思路，但空间会从 `O(1)` 变成 `O(n)`，对本题意义不大。

综上，**最优解** 与暴力解在时间复杂度上是等价的：`O(n²)`。下面给出稍微精简、易懂的实现。

#### 代码（Python）

```python
def min_operations_to_write_y(grid):
    n = len(grid)
    mid = n // 2

    # 统计 Y 区域与非 Y 区域中每种数值的出现次数
    cntY = [0, 0, 0]   # cntY[0]、cntY[1]、cntY[2]
    cntN = [0, 0, 0]

    for r in range(n):
        # 预先算出该行在 Y 中的列集合，避免每个格子都判断
        if r < mid:                     # 上半部：两条斜线
            cols_in_y = {r, n - 1 - r}  # 左斜线列 = r，右斜线列 = n-1-r
        elif r == mid:                  # 中心行：三格都属于 Y（两斜线交点 + 中间竖线）
            cols_in_y = {mid}
        else:                           # 下半部：只保留中间竖线
            cols_in_y = {mid}

        for c in range(n):
            val = grid[r][c]
            if c in cols_in_y:
                cntY[val] += 1
            else:
                cntN[val] += 1

    total_y = sum(cntY)
    total_n = sum(cntN)

    # 枚举 Y 的目标数 a 与非 Y 的目标数 b
    ans = min(
        (total_y - cntY[a]) + (total_n - cntN[b])
        for a in range(3) for b in range(3)
    )
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)` —— 只遍历一次网格。  
- **空间复杂度**：`O(1)` —— 只使用了几个固定大小的计数器。

---

## 心得  

- **核心技巧**：把网格划分为「属于 Y」和「不属于 Y」两块，分别统计每块中 0/1/2 的出现次数，然后枚举两块的目标数值即可得到最少改动次数。  
- **适用的题型**  
  1. **固定形状的统一颜色/数值问题**（例如把十字形、X 形、斜线形等统一成一种颜色）。  
  2. **把矩阵分成若干固定区域，要求每个区域内部数值相同**（如把棋盘分成黑白两块，各自统一颜色）。  
  3. **需要最少改动使得两个子集的数值分别相同**的计数类问题。  

- **一句话总结解题钥匙**：**先把网格划分成两类，统计每类中每种数值的出现次数，枚举目标数值求最小改动**。

---

## 反思  

- **第一反应**：看到「字母 Y」和「最少操作」就想到「把对应位置的数统一」，于是立刻想到统计出现次数。  
- **最容易踩的坑**  
  - **判断 Y 的格子**：容易忘记只取上半部的两条对角线（`r ≤ mid`），或者把中心行的两条斜线都算进去导致重复计数。  
  - **边界条件**：`n` 最小是 3，中心行恰好是 `mid`，此时中心格同时在两条斜线和竖线上，需要确保不重复计数。  
  - **目标数值可以相同**：如果忘记允许 Y 与非 Y 取相同的数，可能会错失更小的答案。  

- **下次遇到类似题**：**第一步**先明确“形状”对应的格子集合，用集合或数学条件把它们写出来；**第二步**分别统计每类中不同数值的频次；**第三步**枚举目标数值，计算最小改动。这样思路清晰，代码也自然简洁。