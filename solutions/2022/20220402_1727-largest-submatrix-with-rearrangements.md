# #1727. 可重排列的最大全 1 子矩阵 / Largest Submatrix With Rearrangements

> 难度：中等 · 标签：Array、Greedy、Sorting、Matrix · [LeetCode 链接](https://leetcode.com/problems/largest-submatrix-with-rearrangements/)

---

## 题目（英文原版）

**Description**

You are given a binary matrix matrix of size m x n, and you are allowed to rearrange the columns of the matrix in any order.
Return the area of the largest submatrix within matrix where every element of the submatrix is 1 after reordering the columns optimally.

**Examples**

**Example 1:**

```
Input: matrix = [[0,0,1],[1,1,1],[1,0,1]]
Output: 4
Explanation: You can rearrange the columns as shown above.
The largest submatrix of 1s, in bold, has an area of 4.
```

**Example 2:**

```
Input: matrix = [[1,0,1,0,1]]
Output: 3
Explanation: You can rearrange the columns as shown above.
The largest submatrix of 1s, in bold, has an area of 3.
```

**Example 3:**

```
Input: matrix = [[1,1,0],[1,0,1]]
Output: 2
Explanation: Notice that you must rearrange entire columns, and there is no way to make a submatrix of 1s larger than an area of 2.
```

**Constraints**

- m == matrix.length
- n == matrix[i].length
- 1 <= m * n <= 105
- matrix[i][j] is either 0 or 1.

---

## 题目（中文翻译）

**描述**  
给定一个大小为 `m x n` 的二进制矩阵 `matrix`，你可以任意重新排列矩阵的列顺序。  
返回在对列进行最优重排后，矩阵中所有元素均为 `1` 的最大子矩阵（submatrix）的面积。

**示例**  

**示例 1**  
输入：`matrix = [[0,0,1],[1,1,1],[1,0,1]]`  
输出：`4`  
解释：如上图所示，你可以对列进行重排。粗体标出的全 `1` 子矩阵面积为 `4`。

**示例 2**  
输入：`matrix = [[1,0,1,0,1]]`  
输出：`3`  
解释：如上图所示，你可以对列进行重排。粗体标出的全 `1` 子矩阵面积为 `3`。

**示例 3**  
输入：`matrix = [[1,1,0],[1,0,1]]`  
输出：`2`  
解释：需要注意只能整体重排列，无法得到面积大于 `2` 的全 `1` 子矩阵。

**约束条件**  
- `m == matrix.length`  
- `n == matrix[i].length`  
- `1 <= m * n <= 10^5`  
- `matrix[i][j]` 仅为 `0` 或 `1`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有列的排列都枚举一遍**，每一种排列都得到一个新的矩阵，然后在这个矩阵里找最大的全 `1` 子矩阵。  

- **枚举排列**：把 `n` 列当成 `n` 张卡片，随意排成一行。  
- **寻找子矩阵**：对每一种排好序的矩阵，用两层循环遍历左上角 `(r1, c1)` 与右下角 `(r2, c2)`，检查这个矩形里是否全是 `1`，如果是就更新最大面积。

> **为什么会对**  
> 因为我们把「所有可能的列顺序」都穷举了，必然会包含最优的那一种；随后对每一种顺序都检查了所有矩形，自然会找到最大的全 `1` 子矩阵。

> **时间/空间分析（大白话）**  
> - 枚举所有列的排列是 `n!`（n 的阶乘），比如 `n=5` 时要尝试 `120` 种；`n` 再大这个数会疯狂增长，根本不可能跑完。  
> - 对每一种排列，再用四重循环检查每个矩形，时间复杂度是 `O(m²·n²)`。  
> - 所以整体时间是 `O(n!·m²·n²)`，这在实际数据（`m·n ≤ 10⁵`）下根本不可接受。  
> - 空间上只需要存原矩阵和几个循环变量，`O(1)`（不计输入矩阵本身）。

#### 代码（Python）

```python
import itertools

def largestSubmatrix_bruteforce(matrix):
    """
    暴力解：枚举所有列的排列，逐个检查所有子矩阵是否全为 1。
    仅用于演示思路，实际会超时。
    """
    m, n = len(matrix), len(matrix[0])
    best = 0

    # 1）遍历所有列的排列（n! 种）
    for perm in itertools.permutations(range(n)):
        # 2）根据当前排列生成新的矩阵
        new_mat = [[row[col] for col in perm] for row in matrix]

        # 3）四重循环枚举所有子矩阵
        for r1 in range(m):
            for r2 in range(r1, m):
                for c1 in range(n):
                    for c2 in range(c1, n):
                        # 检查子矩阵 (r1..r2, c1..c2) 是否全为 1
                        all_one = True
                        for i in range(r1, r2 + 1):
                            for j in range(c1, c2 + 1):
                                if new_mat[i][j] == 0:
                                    all_one = False
                                    break
                            if not all_one:
                                break
                        if all_one:
                            area = (r2 - r1 + 1) * (c2 - c1 + 1)
                            best = max(best, area)
    return best
```

#### 复杂度

- **时间复杂度**：`O(n!·m²·n²)` —— 首先要遍历 `n!` 种列排列，随后每种排列又要检查 `m²·n²` 个子矩形，显然不可接受。  
- **空间复杂度**：`O(1)`（不计输入矩阵本身）—— 只用了常数级的额外变量。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**枚举列的顺序是最大的瓶颈**。我们需要一种方法，在不真的去排列列的情况下，直接得到「把列排好后」能够形成的最大全 `1` 子矩阵。

**关键观察 1**：  
对于任意一行 `i`，我们只关心 **在这行往上**（包括自己）每一列连续 `1` 的数量。记为 `height[i][j]`，即以 `(i, j)` 为底的垂直柱子高度。  

- 计算方式很像「柱状图」的高度：  
  - 如果 `matrix[i][j] == 1`，则 `height[i][j] = height[i-1][j] + 1`（上一行同列的高度加一）。  
  - 否则为 `0`（因为出现了 `0`，柱子被截断）。

**关键观察 2**：  
列的顺序可以随意调换。**对于同一行**，我们只需要把这行的所有 `height` 按 **从大到小** 排序，然后把最大的 `k` 个高度「并排」放在一起，形成宽度为 `k`、高度为第 `k` 大的柱子。这样得到的矩形面积是 `height_sorted[k-1] * k`。  

- 为什么这样合法？因为我们可以把列重新排列，使得这 `k` 列恰好是高度最大的 `k` 列，形成一个宽度为 `k`、高度为最小的那根柱子的矩形（所有柱子都不低于它），所以整个矩形全为 `1`。  

**步骤概括**  

1. **计算每个格子的垂直累计 `1` 数**（即 `height`）。这只需要一次遍历，时间 `O(m·n)`。  
2. 对每一行的 `height` 数组进行 **降序排序**（`O(n log n)`），得到 `sorted_heights`。  
3. 对排好序的数组，遍历 `k = 1 .. n`，计算面积 `sorted_heights[k-1] * k`，更新全局最大值。  

**复杂度分析（大白话）**  

- 第一步是线性扫描，和看完矩阵一次一样快。  
- 第二步对每行排序，最坏情况是 `m` 行每行 `n` 列，时间是 `m·(n log n)`，仍然能接受（`10⁵` 规模下约几百万次操作）。  
- 第三步是线性遍历每行的排序结果，`O(m·n)`。  

总体时间 `O(m·n log n)`，空间只需要额外的 `height`（`m·n`）和每行的临时排序数组（`O(n)`），符合题目限制。

#### 代码（Python）

```python
def largestSubmatrix(matrix):
    """
    最优解：利用每列的连续 1 高度 + 行内降序排序，求最大全 1 子矩阵面积。
    时间复杂度 O(m * n log n)，空间复杂度 O(m * n)（可以再优化到 O(n)）。
    """
    if not matrix:
        return 0

    m, n = len(matrix), len(matrix[0])

    # 1）计算每个位置往上的连续 1 的高度
    # height[i][j] 表示以 (i, j) 为底向上连续 1 的个数
    height = [[0] * n for _ in range(m)]
    for j in range(n):
        cnt = 0
        for i in range(m):
            if matrix[i][j] == 1:
                cnt += 1
                height[i][j] = cnt
            else:
                cnt = 0          # 碰到 0，累计高度清零
                height[i][j] = 0

    ans = 0

    # 2）对每一行的高度数组做降序排序，尝试所有可能的宽度
    for i in range(m):
        # 把第 i 行的高度取出来并排序（从大到小）
        sorted_heights = sorted(height[i], reverse=True)

        # 3）遍历宽度 k（从 1 到 n），计算对应面积
        for k in range(1, n + 1):
            # 第 k 大的高度是 sorted_heights[k-1]，宽度是 k
            area = sorted_heights[k - 1] * k
            if area > ans:
                ans = area

    return ans
```

> **代码要点注释**  
> - `cnt` 用来累计同一列的连续 `1`，相当于在看“柱子”往上有多高。  
> - `sorted(height[i], reverse=True)` 把第 `i` 行所有柱子的高度从高到低排好，这一步相当于“把列重新排列”。  
> - `area = sorted_heights[k-1] * k` 表示取前 `k` 根最高的柱子，最矮的那根决定矩形的高度，宽度自然是 `k`。

#### 复杂度

- **时间复杂度**：`O(m·n log n)`  
  - 计算累计高度：`O(m·n)`（线性扫描）。  
  - 每行排序：`O(m·n log n)`（最耗时的步骤）。  
  - 计算面积：`O(m·n)`（遍历每行的排序结果）。  
  与暴力解相比，省掉了 `n!` 的枚举，快得多。

- **空间复杂度**：`O(m·n)`（存 `height`），如果想进一步压缩到 `O(n)`，可以只保留上一行的累计高度并在遍历时直接排序，思路相同，这里为了清晰保留二维数组。

---

## 心得

- **核心技巧**：把每列的连续 `1` 高度看成柱子，用 **行内降序排序** 代替真实的列排列，从而在 `O(n log n)` 内找出最佳宽度‑高度组合。  
- **适用场景**：  
  1. “可以对列/行自由排序” 的矩阵题目（如 *Maximum Submatrix With Rearrangements*）。  
  2. “把二维问题转化为柱状图” 的最大矩形类问题（如 *Largest Rectangle in Histogram*、*Maximal Rectangle*）。  
- **一句话总结**：**把列的顺序交给排序，让最高的柱子靠在一起，宽度越大高度越小，枚举宽度即可得到最优面积。**

## 反思

- **第一反应**：直接枚举所有列的排列，然后暴力检查子矩阵——这在脑中是最自然的“全枚举”思路，却忽视了规模限制。  
- **最容易踩的坑**：  
  - 忽略了 `m·n ≤ 10⁵` 时 `n!` 完全不可接受；  
  - 在实现累计高度时忘记在遇到 `0` 时把计数清零，导致高度错误；  
  - 排序后忘记遍历所有可能的宽度，只取了最大高度，漏掉了中等宽度的更大面积。  
- **下次类似题的第一步**：先**把问题抽象成“每列的特征值”（如高度、前缀和）**，再思考**能否通过排序或单调结构一次性把所有列/行“安排好”，而不是直接枚举排列。这样往往能把指数级的搜索降到多项式级。