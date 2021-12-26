# #1605. 在已知行列和的情况下构造合法矩阵 / Find Valid Matrix Given Row and Column Sums

> 难度：中等 · 标签：Array、Greedy、Matrix · [LeetCode 链接](https://leetcode.com/problems/find-valid-matrix-given-row-and-column-sums/)

---

## 题目（英文原版）

**Description**

You are given two arrays rowSum and colSum of non-negative integers where rowSum[i] is the sum of the elements in the ith row and colSum[j] is the sum of the elements of the jth column of a 2D matrix. In other words, you do not know the elements of the matrix, but you do know the sums of each row and column.
Find any matrix of non-negative integers of size rowSum.length x colSum.length that satisfies the rowSum and colSum requirements.
Return a 2D array representing any matrix that fulfills the requirements. It's guaranteed that at least one matrix that fulfills the requirements exists.

**Examples**

**Example 1:**

```
Input: rowSum = [3,8], colSum = [4,7]
Output: [[3,0],
         [1,7]]
Explanation: 
0th row: 3 + 0 = 3 == rowSum[0]
1st row: 1 + 7 = 8 == rowSum[1]
0th column: 3 + 1 = 4 == colSum[0]
1st column: 0 + 7 = 7 == colSum[1]
The row and column sums match, and all matrix elements are non-negative.
Another possible matrix is: [[1,2],
                             [3,5]]
```

**Example 2:**

```
Input: rowSum = [5,7,10], colSum = [8,6,8]
Output: [[0,5,0],
         [6,1,0],
         [2,0,8]]
```

**Constraints**

- 1 <= rowSum.length, colSum.length <= 500
- 0 <= rowSum[i], colSum[i] <= 108
- sum(rowSum) == sum(colSum)

---

## 题目（中文翻译）

你得到两个非负整数数组 `rowSum` 和 `colSum`，其中 `rowSum[i]` 表示第 *i* 行的元素之和，`colSum[j]` 表示第 *j* 列的元素之和。换句话说，你不知道矩阵的具体元素，但已知每行和每列的和。

请构造任意一个大小为 `rowSum.length × colSum.length` 的、元素为非负整数（non‑negative integers）的矩阵，使其满足给定的行和列的约束。

返回一个二维数组，表示任意满足要求的矩阵。题目保证至少存在一个满足条件的矩阵。

**示例 1**  
**输入**: `rowSum = [3,8]`, `colSum = [4,7]`  
**输出**: 
```
[[3,0],
 [1,7]]
```  
**解释**:  
- 第 0 行: 3 + 0 = 3 == `rowSum[0]`  
- 第 1 行: 1 + 7 = 8 == `rowSum[1]`  
- 第 0 列: 3 + 1 = 4 == `colSum[0]`  
- 第 1 列: 0 + 7 = 7 == `colSum[1]`  

行列和均匹配，且所有矩阵元素均为非负数。另一种可能的矩阵为:
```
[[1,2],
 [3,5]]
```

**示例 2**  
**输入**: `rowSum = [5,7,10]`, `colSum = [8,6,8]`  
**输出**: 
```
[[0,5,0],
 [6,1,0],
 [2,0,8]]
```

**约束条件**  
- `1 <= rowSum.length, colSum.length <= 500`  
- `0 <= rowSum[i], colSum[i] <= 10^8`  
- `sum(rowSum) == sum(colSum)`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把矩阵的每一个格子都尝试填上所有可能的非负整数**，只要满足对应的行和列的要求就算成功。  
可以把它想象成**拼图**：我们有若干行和若干列，每条“边”上写着该行（列）需要的总和，我们要把每个小格子里的数字拼进去，使得每条边的数字恰好加到它要求的总和。  

实现上常用**回溯（Backtracking）**：

1. 按行、列顺序依次处理格子 `(i, j)`。  
2. 对当前格子，枚举所有合法的取值 `x`（`0 ≤ x ≤ min(剩余的 rowSum[i], colSum[j])`）。  
3. 把 `x` 放进去后，更新 `rowSum[i]`、`colSum[j]`（分别减去 `x`），递归处理下一个格子。  
4. 若递归返回成功，则整个矩阵已经找到；若所有 `x` 都尝试失败，则回溯，把格子恢复为 `0`，继续尝试别的分配。  

> **为什么它一定能找到答案？**  
> 题目保证至少有一种合法矩阵。回溯会遍历**所有**可能的填法，只要存在合法解，就一定会在某条搜索路径上走到最后。  

> **大白话的时间/空间解释**  
> - **时间复杂度**：每个格子最多有 `min(rowSum[i], colSum[j]) + 1` 种取值。最坏情况下行列和都很大，格子数是 `m·n`（`m = len(rowSum)`，`n = len(colSum)`），所以时间是指数级的，记作 **O( (maxSum)^{m·n} )**，也就是“非常、非常慢”。  
> - **空间复杂度**：递归深度最多是格子数 `m·n`，加上存放矩阵的空间，整体是 **O(m·n)**。

#### 代码（Python）

```python
def restoreMatrix_bruteforce(rowSum, colSum):
    """暴力回溯版，返回任意合法矩阵"""
    m, n = len(rowSum), len(colSum)
    # 用一个 m×n 的全 0 矩阵先占位
    matrix = [[0] * n for _ in range(m)]

    def dfs(i, j):
        """递归填第 i 行第 j 列"""
        # 若已经填完最后一个格子，说明成功
        if i == m:                     # i 超出行数，说明全部填完
            return True

        # 计算下一个格子的坐标
        ni, nj = (i, j + 1) if j + 1 < n else (i + 1, 0)

        # 当前格子最多能放多少：不能超过所在行或所在列剩余的和
        limit = min(rowSum[i], colSum[j])
        for x in range(limit + 1):     # 从 0 到 limit 逐个尝试
            # 把 x 放进去，更新行、列剩余和
            matrix[i][j] = x
            rowSum[i] -= x
            colSum[j] -= x

            # 递归处理下一个格子
            if dfs(ni, nj):
                return True          # 找到合法解，直接返回

            # 失败了，撤销修改（回溯）
            rowSum[i] += x
            colSum[j] += x
            matrix[i][j] = 0

        # 所有可能都不行，返回 False 让上层回溯
        return False

    dfs(0, 0)          # 从左上角开始搜索
    return matrix
```

> **关键行中文注释**已经写在代码里，帮助你一步步跟踪思路。

#### 复杂度

- **时间复杂度**：`O( (max(rowSum, colSum) + 1)^{m·n} )` —— 指数级，实际只能在极小规模（比如 `2×2`）下跑得完。  
- **空间复杂度**：`O(m·n)` —— 矩阵本身占的空间，加上递归栈的深度同样是格子数。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于每个格子都要枚举很多可能的数**，这让时间爆炸。实际上我们并不需要“尝遍所有”——只要保证每行、每列的剩余和始终被满足，就可以一次性决定每个格子的值。

**核心观察**：

- 对于格子 `(i, j)`，只要把 `rowSum[i]` 与 `colSum[j]` 中的**较小者**填进去，行和列的需求都会被“尽可能”满足，而不会导致以后出现负数。  
- 填完后，**对应的行或列**（或者两者）会变成 **0**（即已经满足），以后再也不需要在这行/列上继续分配。  
- 于是我们可以**一次遍历**所有格子，采用**贪心**：`matrix[i][j] = min(rowSum[i], colSum[j])`，然后把这两个剩余和都减去该值。  

这就是题目提示中的“找最小的 rowSum 或 colSum，放进去”。把矩阵想象成**水池**，`rowSum[i]` 是第 i 行的“水量”，`colSum[j]` 是第 j 列的“水量”。每次我们把两者的最小值倒进交叉的格子，水要么把整行灌满，要么把整列灌满，最后所有水都恰好倒完。

**实现细节**：

1. 初始化 `m = len(rowSum)`, `n = len(colSum)`，创建全 0 矩阵。  
2. 用两个指针 `i`（行）和 `j`（列）从左上角开始遍历。  
3. 对当前 `(i, j)`，取 `x = min(rowSum[i], colSum[j])`，填入矩阵并更新 `rowSum[i] -= x`, `colSum[j] -= x`。  
4. 若 `rowSum[i] == 0`，说明第 i 行已经满足，`i += 1` 移到下一行；若 `colSum[j] == 0`，说明第 j 列已经满足，`j += 1` 移到下一列。  
5. 循环直到所有行列指针都走完。  

因为每次至少让一行或一列的剩余和变为 0，最多进行 `m + n` 次指针移动，总体是 **线性** 的。

#### 代码（Python）

```python
def restoreMatrix(rowSum, colSum):
    """贪心构造任意合法矩阵，时间 O(m+n)，空间 O(m·n)"""
    m, n = len(rowSum), len(colSum)
    # 先准备一个全 0 的矩阵
    matrix = [[0] * n for _ in range(m)]

    i = j = 0               # i 指向当前行，j 指向当前列
    while i < m and j < n:
        # 取当前行、列剩余和的最小值作为填入的数
        x = min(rowSum[i], colSum[j])
        matrix[i][j] = x

        # 更新剩余需求
        rowSum[i] -= x
        colSum[j] -= x

        # 若该行已经填满，向下走到下一行
        if rowSum[i] == 0:
            i += 1
        # 若该列已经填满，向右走到下一列
        if colSum[j] == 0:
            j += 1

    return matrix
```

> **关键行解释**  
> - `x = min(rowSum[i], colSum[j])`：把两者中较小的“水量”倒进交叉格子。  
> - `if rowSum[i] == 0: i += 1`：这一行已经满足，后面不再需要在该行放数字。  
> - `if colSum[j] == 0: j += 1`：同理，列满足后直接右移。

#### 复杂度

- **时间复杂度**：`O(m + n)` —— 每次循环至少让一行或一列的剩余和归零，最多走完 `m` 行加 `n` 列。对比暴力的指数级，这就是“瞬间完成”。  
- **空间复杂度**：`O(m·n)` —— 用来存放返回的矩阵。除矩阵外，只用了常数级的额外变量（指针 `i, j`、临时 `x`）。

---

## 心得

- **核心技巧**：**贪心 + 双指针**。把行列剩余和视作资源，始终取最小的那部分一次性消耗。  
- **适用的题型**  
  1. **分配类**：如“分配糖果使总甜度相等”“配对两组数使每对差值最小”。  
  2. **矩阵构造**：比如 “构造满足行列和的矩阵” (本题)、“构造满足对角线和的矩阵”。  
  3. **资源调度**：如 “两台机器的任务分配”“流水线作业调度”。  
- **一句话总结解题钥匙**：**“每次把当前行或列最紧缺的需求一次性满足”**。

---

## 反思

- **第一反应**：看到行列和，我首先想到“遍历所有格子尝试所有组合”。这自然导致回溯的暴力思路。  
- **最容易踩的坑**  
  - 忘记 **`rowSum` 与 `colSum` 必须同步减**，导致后面出现负数或不匹配。  
  - 没有在填完后 **及时移动指针**，导致死循环（比如一直在同一个格子上循环）。  
  - 对 **边界情况**（只有一行或一列）没有特别处理，代码仍然能正常工作，但需要确认循环条件 `while i < m and j < n`。  
- **下次遇到同类题**：**先思考“有没有一次性把某个需求全部满足的办法”。** 若可以，用最小值或最大值一次性扣除，就能把问题从“指数”降到“线性”。