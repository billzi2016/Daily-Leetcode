# #1074. 子矩阵和为目标值的个数 / Number of Submatrices That Sum to Target

> 难度：困难 · 标签：Array、Hash Table、Matrix、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/number-of-submatrices-that-sum-to-target/)

---

## 题目（英文原版）

**Description**

Given a matrix and a target, return the number of non-empty submatrices that sum to target.
A submatrix x1, y1, x2, y2 is the set of all cells matrix[x][y] with x1 <= x <= x2 and y1 <= y <= y2.
Two submatrices (x1, y1, x2, y2) and (x1', y1', x2', y2') are different if they have some coordinate that is different: for example, if x1 != x1'.

**Examples**

**Example 1:**

```
Input: matrix = [[0,1,0],[1,1,1],[0,1,0]], target = 0
Output: 4
Explanation: The four 1x1 submatrices that only contain 0.
```

**Example 2:**

```
Input: matrix = [[1,-1],[-1,1]], target = 0
Output: 5
Explanation: The two 1x2 submatrices, plus the two 2x1 submatrices, plus the 2x2 submatrix.
```

**Example 3:**

```
Input: matrix = [[904]], target = 0
Output: 0
```

**Constraints**

- 1 <= matrix.length <= 100
- 1 <= matrix[0].length <= 100
- -1000 <= matrix[i][j] <= 1000
- -10^8 <= target <= 10^8

---

## 题目（中文翻译）

给定一个矩阵 `matrix` 和一个目标值 `target`，返回和等于 `target` 的 **非空子矩阵**（submatrix）的个数。  
子矩阵 `(x1, y1, x2, y2)` 指的是所有满足 `x1 ≤ x ≤ x2` 且 `y1 ≤ y ≤ y2` 的单元格 `matrix[x][y]` 的集合。  
如果两个子矩阵 `(x1, y1, x2, y2)` 与 `(x1', y1', x2', y2')` 在任意坐标上不同，则它们视为不同的子矩阵，例如 `x1 != x1'` 时即不同。

**示例 1**  
**输入**: `matrix = [[0,1,0],[1,1,1],[0,1,0]], target = 0`  
**输出**: `4`  
**解释**: 四个只包含 `0` 的 `1×1` 子矩阵。

**示例 2**  
**输入**: `matrix = [[1,-1],[-1,1]], target = 0`  
**输出**: `5`  
**解释**: 两个 `1×2` 子矩阵、两个 `2×1` 子矩阵以及整个 `2×2` 子矩阵的和均为 `0`。

**示例 3**  
**输入**: `matrix = [[904]], target = 0`  
**输出**: `0`

**约束条件**  
- `1 <= matrix.length <= 100`  
- `1 <= matrix[0].length <= 100`  
- `-1000 <= matrix[i][j] <= 1000`  
- `-10^8 <= target <= 10^8`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可能的子矩阵枚举出来，然后把每个子矩阵的元素相加，看看是否等于 `target`**。  

- **子矩阵的定义**：左上角坐标 `(x1, y1)`，右下角坐标 `(x2, y2)`，只要满足 `x1 ≤ x ≤ x2` 且 `y1 ≤ y ≤ y2` 的格子都属于这个子矩阵。  
- **遍历方式**：四层循环  
  1. 选左上角的行 `x1`（0 … m‑1）  
  2. 选左上角的列 `y1`（0 … n‑1）  
  3. 选右下角的行 `x2`（`x1` … m‑1）  
  4. 选右下角的列 `y2`（`y1` … n‑1）  
- 对每一组 `(x1, y1, x2, y2)`，再用两层循环把其中的所有元素加起来，得到子矩阵的和。

> **类比**：把矩阵想象成一本书的页码表，暴力枚举就像把每一页的每一种可能的左上角和右下角都写下来，然后逐字逐句读一遍，看看这段文字的总字数是不是正好等于目标值。

**为什么这个方法一定能得到答案**：因为我们把 **所有** 合法的子矩阵都遍历了一遍，凡是满足条件的自然会被计数。

#### 代码（Python）

```python
def num_submatrix_sum_target_brute(matrix, target):
    m, n = len(matrix), len(matrix[0])
    ans = 0

    # ① 枚举左上角 (x1, y1)
    for x1 in range(m):
        for y1 in range(n):
            # ② 枚举右下角 (x2, y2)
            for x2 in range(x1, m):
                for y2 in range(y1, n):
                    # ③ 计算该子矩阵的和
                    s = 0
                    for i in range(x1, x2 + 1):
                        for j in range(y1, y2 + 1):
                            s += matrix[i][j]          # 累加每个格子的值
                    if s == target:                  # 判断是否等于目标
                        ans += 1
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(m² * n²)`  
  - 四层循环产生约 `m² * n²` 种子矩阵，每种子矩阵内部又要遍历其内部格子，最坏情况下内部遍历的格子数也是 `O(m * n)`，于是整体是 `O(m³ * n³)`。  
  - 为了便于理解，我们常把它简化为 **四层遍历的组合数**，即 `m` 选两行、`n` 选两列，约等于 `O(m²·n²)`，已经是 **指数级** 的慢，100×100 的矩阵根本跑不完。  
- **空间复杂度**：`O(1)`  
  - 只用了常数个额外变量，没有额外的数据结构。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **每次都要重新遍历子矩阵内部的所有元素**。  
如果我们能够 **在 O(1) 时间内直接得到任意子矩阵的和**，就可以把“内部遍历”这一步省掉。  

这正是 **二维前缀和**（2‑D Prefix Sum）要解决的问题。  
- **前缀和的类比**：就像我们平时查字典，先记下每一页的累计字数，这样想要知道第 `a`~`b` 页的总字数，只需要 “第 `b` 页累计 - 第 `a‑1` 页累计”。二维前缀和把这种思想扩展到矩阵上。

**步骤 1：构建二维前缀和**  
`pre[i][j]` 表示矩阵左上角 `(0,0)` 到 `(i-1, j-1)`（不含 `i, j`）的所有元素之和。  
有递推式  
```
pre[i][j] = pre[i-1][j] + pre[i][j-1] - pre[i-1][j-1] + matrix[i-1][j-1]
```
这样我们可以在 **O(1)** 时间内算出任意子矩阵的和：
```
sum(x1,y1,x2,y2) = pre[x2+1][y2+1] - pre[x1][y2+1] - pre[x2+1][y1] + pre[x1][y1]
```

**步骤 2：把二维问题降维**  
固定上边界 `top` 和下边界 `bottom`（即选定一段连续的行），把这几行“压缩”成一维数组 `rowSum`，其中 `rowSum[col]` 表示在这几行之间，第 `col` 列的所有元素之和。  
此时，寻找 **子矩阵** 等价于在 `rowSum` 上寻找 **子数组**，使得子数组的和等于 `target`。  

**步骤 3：在一维数组上使用哈希表统计子数组和**  
- 用哈希表 `counter` 记录前缀和出现的次数。  
- 遍历 `rowSum`，维护当前前缀和 `cur`。  
- 若 `cur - target` 在哈希表里出现了 `k` 次，说明以当前右端点为结尾、和为 `target` 的子数组有 `k` 条，累计到答案。  
- 最后把当前前缀和 `cur` 加入哈希表。

**为什么这样快**：  
- 对每一对 `(top, bottom)`，我们只做一次 **线性扫描**（`O(n)`）就能统计所有满足条件的子矩阵。  
- `top`、`bottom` 各有 `m` 种取法，整体时间是 `O(m² * n)`，对 100×100 的矩阵来说大约只有 10⁶ 次操作，完全可接受。  

#### 代码（Python）

```python
from collections import defaultdict

def num_submatrix_sum_target(matrix, target):
    """
    返回子矩阵和恰好等于 target 的个数
    """
    m, n = len(matrix), len(matrix[0])
    ans = 0

    # ① 枚举上边界 top
    for top in range(m):
        # 用一个长度为 n 的数组累计从 top 行到当前 bottom 行每列的和
        col_sums = [0] * n

        # ② 枚举下边界 bottom（bottom >= top）
        for bottom in range(top, m):
            # 更新 col_sums：把第 bottom 行加进来
            for c in range(n):
                col_sums[c] += matrix[bottom][c]   # 这里相当于把矩阵压成一维

            # ③ 在一维数组 col_sums 上统计子数组和为 target 的个数
            counter = defaultdict(int)   # 哈希表：前缀和 -> 出现次数
            counter[0] = 1                # 空前缀和为 0，方便直接计数
            cur = 0                       # 当前前缀和

            for val in col_sums:
                cur += val                 # 累计到当前位置的前缀和
                # 若 cur - target 之前出现过，说明有若干子数组满足条件
                ans += counter[cur - target]
                # 记录当前前缀和出现次数，供后续使用
                counter[cur] += 1

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(m² * n)`  
  - 两层循环枚举 `top`、`bottom`（最多 `m * (m+1) / 2 ≈ m²/2` 次），内部对每列做一次线性扫描 `O(n)`，以及一次哈希表查询/更新（均摊为 O(1)）。  
  - 与暴力解的 `O(m²·n²)` 相比，少了一层 `n`，在最坏 100×100 的情况下从 10⁸ 降到约 10⁶，快上百倍。  

- **空间复杂度**：`O(n)`  
  - 主要是 `col_sums`（长度 n）和哈希表 `counter`（至多存储 n+1 个前缀和）。  
  - 与输入矩阵大小无关，只随列数线性增长。

---

## 心得

- **核心技巧**：**把二维子矩阵求和问题降维成一维子数组求和问题**，并配合 **前缀和 + 哈希表**（也叫「前缀和计数」）实现线性时间统计。  
- **适用场景**  
  1. “子数组/子矩阵求和等于 target” 系列题目（如 LeetCode 560、525、1074）。  
  2. 需要统计满足某种累计条件的区间数目时（比如求和为零的子数组、求和不超过 K 的子数组等）。  
- **一句话总结**：**先把多维度的累加压缩到一维，再用前缀和哈希表“一遍遍历”把所有答案找出来**。

---

## 反思

- **第一反应**：看到“子矩阵”和“target”，本能地想遍历所有子矩阵并逐个相加——这就是暴力思路。  
- **最容易踩的坑**  
  - **整数溢出**：在 Python 中整数无限大，但在其他语言要注意 `int` 范围。  
  - **负数**：子矩阵中可能出现负数，滑动窗口（只适用于全正）失效，必须使用前缀和 + 哈希表。  
  - **空前缀和的处理**：忘记把 `counter[0]=1` 放进去会导致漏掉从左边界直接等于 target 的子矩阵。  
- **下次类似题的第一步**：**先思考能否把多维度的求和问题压缩到一维**（固定上下边界或左右边界），随后考虑“一维前缀和 + 哈希表”或“滑动窗口”来快速统计。