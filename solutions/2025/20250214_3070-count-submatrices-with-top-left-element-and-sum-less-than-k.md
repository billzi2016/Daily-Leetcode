# #3070. 计数包含左上角元素且和不超过 k 的子矩阵 / Count Submatrices with Top-Left Element and Sum Less Than k

> 难度：中等 · 标签：Array、Matrix、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/count-submatrices-with-top-left-element-and-sum-less-than-k/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer matrix grid and an integer k.
Return the number of submatrices that contain the top-left element of the grid, and have a sum less than or equal to k.

**Examples**

**Example 1:**

```
Input: grid = [[7,6,3],[6,6,1]], k = 18
Output: 4
Explanation: There are only 4 submatrices, shown in the image above, that contain the top-left element of grid, and have a sum less than or equal to 18.
```

**Example 2:**

```
Input: grid = [[7,2,9],[1,5,0],[2,6,6]], k = 20
Output: 6
Explanation: There are only 6 submatrices, shown in the image above, that contain the top-left element of grid, and have a sum less than or equal to 20.
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= n, m <= 1000
- 0 <= grid[i][j] <= 1000
- 1 <= k <= 109

---

## 题目（中文翻译）

**题目描述**  
给定一个下标从 0 开始的整数矩阵 `grid` 和一个整数 `k`。  
返回所有 **子矩阵（submatrix）** 中满足以下条件的数量：该子矩阵必须包含矩阵左上角元素 `grid[0][0]`，且其所有元素之和 **小于等于** `k`。

**示例**

*示例 1*  
```text
Input: grid = [[7,6,3],[6,6,1]], k = 18
Output: 4
Explanation: 仅有 4 个子矩阵（如上图所示）同时满足包含左上角元素且其元素和 ≤ 18。
```

*示例 2*  
```text
Input: grid = [[7,2,9],[1,5,0],[2,6,6]], k = 20
Output: 6
Explanation: 仅有 6 个子矩阵（如上图所示）同时满足包含左上角元素且其元素和 ≤ 20。
```

**约束条件**

- `m == grid.length`
- `n == grid[i].length`
- `1 <= n, m <= 1000`
- `0 <= grid[i][j] <= 1000`
- `1 <= k <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目要求统计 **所有** 包含左上角元素 `(0,0)` 的子矩阵，使得它们的元素和 ≤ `k`。  
最直接的想法就是：

1. 把右下角的坐标 `(i, j)`（`0 ≤ i < m, 0 ≤ j < n`）枚举出来。每一对坐标唯一决定一个子矩阵 `grid[0..i][0..j]`。
2. 对这个子矩阵里的每一个格子求和。  
   - 这里可以把子矩阵想象成一块 **矩形巧克力**，我们把它全部吃掉来算重量。  
3. 如果和 ≤ `k`，计数器 `ans` 加一。

> **为什么能得到正确答案**  
> 因为题目限定子矩阵必须包含左上角，所以左上角坐标永远是 `(0,0)`，右下角遍历所有可能即可覆盖所有合法子矩阵。只要把每个子矩阵的真实和算出来并比较，就不会漏掉也不会多算。

> **时间/空间分析（大白话）**  
> - **时间复杂度**：外层两层循环枚举右下角，共 `m·n` 种可能；  
>   对每一种可能，我们要遍历整个子矩阵的格子，最坏情况下是 `i·j ≈ m·n` 个格子。于是总的操作次数约为 `m·n·m·n = (m·n)²`，即 **O(m²·n²)**。  
>   用生活中的比喻，这相当于你要把每块巧克力都从头到尾数一遍重量，而巧克力的块数本身就已经是 `m·n`，于是整体工作量是“块数的平方”。
> - **空间复杂度**：只用了常数个额外变量（计数器、临时求和），不随输入规模增长，**O(1)**。

#### 代码（Python）

```python
def countSubmatrices_brute(grid, k):
    """
    暴力解：枚举右下角 (i, j)，逐格累加求和
    """
    m, n = len(grid), len(grid[0])
    ans = 0                         # 记录符合条件的子矩阵个数

    # 枚举右下角坐标
    for i in range(m):
        for j in range(n):
            cur_sum = 0             # 当前子矩阵的元素和
            # 累加左上角到 (i, j) 的所有格子
            for r in range(i + 1):         # 行 0..i
                for c in range(j + 1):     # 列 0..j
                    cur_sum += grid[r][c]  # 把每个格子的值加进去
            # 判断是否满足 ≤ k
            if cur_sum <= k:
                ans += 1

    return ans
```

> **代码要点注释**  
> - `for i in range(m)`、`for j in range(n)`：遍历所有可能的右下角。  
> - 两层内部循环 `for r in range(i+1)`、`for c in range(j+1)`：把子矩阵里的每个元素都加进 `cur_sum`。  
> - `if cur_sum <= k:`：只要和不超过 `k`，计数器加一。

#### 复杂度

- **时间复杂度**：`O(m²·n²)` — 需要遍历每个子矩阵的每个格子，工作量随矩阵面积的平方增长。  
- **空间复杂度**：`O(1)` — 只用常数级别的额外变量。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 出在「每次都把子矩阵的所有格子重新加一遍」。  
如果我们能在 **O(1)** 的时间内直接得到任意子矩阵的和，整体复杂度就会从 `O(m²·n²)` 降到 **枚举右下角的次数** `O(m·n)`。

这正是 **前缀和（Prefix Sum）** 的用武之地。  
- **二维前缀和** 可以把 “从左上角到任意位置的矩形和” 预先算好，存进一个同样大小的数组 `pref`。  
- 对于本题，子矩阵的左上角永远是 `(0,0)`，所以子矩阵 `grid[0..i][0..j]` 的和 **恰好等于** `pref[i][j]`（不需要减去其他区域）。

> **二维前缀和的类比**  
> 想象你在一本厚厚的字典里查词，字典的每一页都标记了从书首到该页的累计页数。查到任意页的累计页数，只要直接看那一页的标记即可，无需从头数起。这里的“累计页数”就是前缀和。

实现步骤：

1. **构建前缀和矩阵 `pref`**  
   - `pref[i][j] = grid[i][j] + pref[i-1][j] + pref[i][j-1] - pref[i-1][j-1]`（注意去掉左上重叠部分）。  
   - 边界上（`i==0` 或 `j==0`）单独处理，等价于把超出范围的值视为 `0`。
2. **遍历右下角** `(i, j)`，直接读取 `pref[i][j]`，判断是否 ≤ `k`，符合则计数。  
3. 返回计数。

整个过程只遍历两遍矩阵：一次构造前缀和，二次统计，时间是 `O(m·n)`，空间是存前缀和的 `O(m·n)`（也可以在原数组上原地改写，但为了思路清晰这里单独用一个数组）。

#### 代码（Python）

```python
def countSubmatrices_opt(grid, k):
    """
    最优解：利用二维前缀和在 O(1) 时间得到任意左上角为 (0,0) 的子矩阵和
    """
    m, n = len(grid), len(grid[0])

    # 第一步：构造前缀和矩阵 pref，pref[i][j] 表示左上角到 (i, j) 的和
    pref = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            # 当前格子的原始值
            cur = grid[i][j]

            # 上方累计、左方累计、左上角重复部分要减掉
            up = pref[i - 1][j] if i > 0 else 0
            left = pref[i][j - 1] if j > 0 else 0
            diag = pref[i - 1][j - 1] if i > 0 and j > 0 else 0

            # 前缀和公式
            pref[i][j] = cur + up + left - diag

    # 第二步：统计满足 sum ≤ k 的子矩阵
    ans = 0
    for i in range(m):
        for j in range(n):
            # 由于左上角固定为 (0,0)，子矩阵和就是 pref[i][j]
            if pref[i][j] <= k:
                ans += 1

    return ans
```

> **关键行解释**  
> - `up = pref[i-1][j] if i>0 else 0`：取上面一行的累计和，`i==0` 时没有上面，视作 `0`。  
> - `left = pref[i][j-1] if j>0 else 0`：取左边一列的累计和，同理。  
> - `diag = pref[i-1][j-1] if i>0 and j>0 else 0`：左上角的累计被上面和左边都加了一次，需要减掉一次。  
> - `pref[i][j] = cur + up + left - diag`：这就是二维前缀和的核心公式。  
> - `if pref[i][j] <= k:`：直接用前缀和判断，无需再遍历格子。

#### 复杂度

- **时间复杂度**：`O(m·n)` — 只遍历两遍矩阵，每格的操作都是常数时间。  
  > 与暴力解相比，工作量从“面积的平方”降到了“面积”，相当于把原本的 `O(10⁶)` 降到 `O(10³)`（当 `m=n=1000` 时）。
- **空间复杂度**：`O(m·n)` — 需要一个同等大小的前缀和矩阵来存累计值。  
  > 如果想进一步压缩空间，可以把前缀和直接写回原矩阵 `grid`，这样只需要 `O(1)` 额外空间，但概念上会稍微复杂一些。

---

## 心得

- **核心技巧**：二维前缀和（Prefix Sum）——一次预处理即可在 O(1) 时间得到任意左上角固定的子矩阵和。  
- **适用题型**  
  1. “求所有以 (0,0) 为左上角的子矩阵和” 系列，如本题。  
  2. “统计满足某种和约束的子矩阵”——比如 “子矩阵和 ≤ k” 或 “子矩阵和 = target”。  
  3. “求任意子矩阵的最大和 / 最小和”——常用前缀和结合单调队列或二分搜索。  
- **一句话总结**：**先把“累加”这件事一次性做好，后面查询就能瞬间得到**。

---

## 反思

- **第一反应**：直接枚举每个子矩阵并逐格相加，代码最容易写出来。  
- **最容易踩的坑**  
  - **边界处理**：在计算前缀和时，`i-1`、`j-1` 可能越界，需要用 `0` 填充。  
  - **整数溢出**：本题 `grid[i][j] ≤ 1000`，`m,n ≤ 1000`，最大和约为 `10⁹`，在 Python 中不会溢出，但在语言限制更严格的环境要注意使用 64 位整数。  
  - **误把左上角固定的前提忘记**：如果把一般的子矩阵求和公式直接套用，会出现额外的减法，导致错误。  
- **下次类似题的第一步**：判断是否可以 **预处理累计信息**（前缀和、前缀乘积、前缀最大值等），如果可以，就先把它算好，再在枚举阶段 O(1) 直接查询。