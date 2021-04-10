# #1292. 矩阵中和不超过阈值的最大正方形边长 / Maximum Side Length of a Square with Sum Less than or Equal to Threshold

> 难度：中等 · 标签：Array、Binary Search、Matrix、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/maximum-side-length-of-a-square-with-sum-less-than-or-equal-to-threshold/)

---

## 题目（英文原版）

**Description**

Given a m x n matrix mat and an integer threshold, return the maximum side-length of a square with a sum less than or equal to threshold or return 0 if there is no such square.

**Examples**

**Example 1:**

```
Input: mat = [[1,1,3,2,4,3,2],[1,1,3,2,4,3,2],[1,1,3,2,4,3,2]], threshold = 4
Output: 2
Explanation: The maximum side length of square with sum less than 4 is 2 as shown.
```

**Example 2:**

```
Input: mat = [[2,2,2,2,2],[2,2,2,2,2],[2,2,2,2,2],[2,2,2,2,2],[2,2,2,2,2]], threshold = 1
Output: 0
```

**Constraints**

- m == mat.length
- n == mat[i].length
- 1 <= m, n <= 300
- 0 <= mat[i][j] <= 104
- 0 <= threshold <= 105

---

## 题目（中文翻译）

**题目描述**  
给定一个 `m x n` 矩阵 `mat`（matrix）和一个整数 `threshold`（阈值），返回满足「正方形（square）中所有元素之和 ≤ `threshold`」的最大边长（side‑length），如果不存在这样的正方形则返回 `0`。

**示例**  

*示例 1*  
输入: `mat = [[1,1,3,2,4,3,2],[1,1,3,2,4,3,2],[1,1,3,2,4,3,2]], threshold = 4`  
输出: `2`  
解释: 和小于等于 `4` 的最大正方形的边长是 `2`，如图所示。

*示例 2*  
输入: `mat = [[2,2,2,2,2],[2,2,2,2,2],[2,2,2,2,2],[2,2,2,2,2],[2,2,2,2,2]], threshold = 1`  
输出: `0`

**约束条件**  

- `m == mat.length`  
- `n == mat[i].length`  
- `1 ≤ m, n ≤ 300`  
- `0 ≤ mat[i][j] ≤ 10^4`  
- `0 ≤ threshold ≤ 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可能的正方形都枚举一遍**，算出它们的元素和，看看哪些正方形的和 ≤ threshold，最后取最大的边长。

- **枚举正方形**  
  - 先决定正方形的左上角坐标 `(i, j)`，  
  - 再决定它的边长 `k`（`k` 从 1 开始递增，只要不超出矩阵边界）。  
- **求和**  
  - 对于每个 `(i, j, k)`，遍历正方形内部的 `k × k` 个格子，把它们的值加起来。  
  - 这一步就像在厨房里数一盘水果的总重量，需要一个一个称。

> **类比**：把矩阵想成一本书的每页都有若干字，正方形就是连续的几页。暴力做法就是把每一种可能的页数组合都读一遍，算字数。

- **为什么一定对**  
  - 我们检查了**所有**合法的正方形，只要有一个满足条件，就一定能找到最大的那一个（因为我们会记录最大边长）。

#### 代码（Python）

```python
from typing import List

def maxSideLength_bruteforce(mat: List[List[int]], threshold: int) -> int:
    m, n = len(mat), len(mat[0])
    best = 0                                 # 记录目前找到的最大边长

    # 枚举左上角坐标
    for i in range(m):
        for j in range(n):
            # 以 (i, j) 为左上角的正方形最大可能的边长
            max_len = min(m - i, n - j)
            # 逐个尝试每一种边长
            for k in range(1, max_len + 1):
                cur_sum = 0
                # 计算 k×k 正方形的元素和
                for x in range(i, i + k):
                    for y in range(j, j + k):
                        cur_sum += mat[x][y]
                # 若和不超过阈值，更新答案
                if cur_sum <= threshold:
                    best = max(best, k)
                else:
                    # 已经超过阈值，后面的更大正方形只会更大，直接跳出
                    break
    return best
```

> **关键行中文注释**  
> - `max_len = min(m - i, n - j)`：保证正方形不跑出矩阵边界。  
> - 两层 `for x / for y` 用来**逐格累加**，相当于把正方形里的每个数字都“装进篮子”。  
> - `if cur_sum <= threshold:`：只要满足条件，就把当前边长和历史最大值比较，保留更大的。

#### 复杂度

- **时间复杂度**：`O(m * n * min(m, n)^2)`  
  - 外层两层循环遍历每个左上角，最多 `m·n` 次。  
  - 对每个左上角，最坏情况要检查的边长是 `min(m, n)`，每次求和又要遍历 `k²` 格子。  
  - 用大白话讲，就是**“每次都把正方形里的每块砖都数一遍”**，所以会慢到几千万次（在最大约束 300×300 时会超时）。

- **空间复杂度**：`O(1)`（不计输入矩阵本身）  
  - 只用了几个整型变量，额外存储几乎为零。

---

### 2. 最优解

#### 思路  

暴力解慢的根本原因是**每次都要重新遍历正方形内部的格子**，导致大量重复计数。我们可以通过两步技巧把这部分工作压到 **`O(1)`**：

1. **前缀和（Prefix Sum）**  
   - 先把矩阵的每个左上角到 `(i, j)` 的子矩阵和算好，存进另一个矩阵 `pre`。  
   - 有了前缀和后，任何任意子矩形（包括正方形）的元素和都能 **常数时间** 通过四个数相减得到。  
   - 类比：把每本书的累计字数写在封面上，想知道第 `a`‑`b` 页的字数，只要用封面上的累计数相减即可，省去逐页数的麻烦。

2. **二分搜索（Binary Search）**  
   - 观察到：**如果边长 `k` 的正方形已经满足 “和 ≤ threshold”，那么所有更小的边长一定也满足**（因为更小的正方形包含的格子更少，和不会增大）。  
   - 这是一种**单调性**（从左到右：`True True … True False False …`），正好可以用二分搜索在 `[1, min(m, n)]` 区间快速定位最大的合法 `k`。  
   - 二分搜索的过程类似找钥匙：先猜一个长度 `mid`，检查是否可行；如果可行，就把左边界移到 `mid+1`（尝试更大），否则把右边界移到 `mid-1`（尝试更小），直到左右边界相遇。

**整体流程**：

1. 预处理前缀和 `pre`（`O(m·n)`）。  
2. 用二分搜索决定答案的范围（`log(min(m,n))` 次）。  
3. 每次二分检查时，遍历所有可能的左上角，利用前缀和在 **`O(1)`** 时间算出对应正方形的和，若发现任意一个 ≤ threshold，就说明该边长可行。

#### 代码（Python）

```python
from typing import List

def maxSideLength(mat: List[List[int]], threshold: int) -> int:
    m, n = len(mat), len(mat[0])

    # ---------- 1. 构造前缀和矩阵 ----------
    # pre[i][j] 表示左上角 (0,0) 到 (i-1, j-1) 的子矩阵和，大小为 (m+1)×(n+1)
    pre = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        row_sum = 0
        for j in range(n):
            row_sum += mat[i][j]                 # 当前行的累计和
            pre[i + 1][j + 1] = pre[i][j + 1] + row_sum
            # 解释：pre[i][j+1] 是上一行同列的累计，row_sum 把本行左侧的值加进去

    # ---------- 2. 二分搜索 ----------
    left, right = 1, min(m, n)   # 正方形的可能边长范围
    answer = 0

    # 判断长度为 k 的正方形是否存在满足条件的
    def possible(k: int) -> bool:
        # 遍历所有左上角 (i, j)，i 的范围是 [0, m-k]，j 的范围是 [0, n-k]
        for i in range(m - k + 1):
            for j in range(n - k + 1):
                # 使用前缀和快速求子矩阵和
                total = (pre[i + k][j + k] - pre[i][j + k]
                         - pre[i + k][j] + pre[i][j])
                if total <= threshold:
                    return True      # 只要找到一个即可
        return False

    while left <= right:
        mid = (left + right) // 2   # 试探的边长
        if possible(mid):
            answer = mid            # 记录下可行的最大值
            left = mid + 1          # 继续往更大的方向搜索
        else:
            right = mid - 1         # 缩小搜索区间

    return answer
```

> **关键行中文注释**  
> - `pre[i + 1][j + 1] = pre[i][j + 1] + row_sum`：把上一行的累计和加上当前行到 `(i,j)` 为止的和，得到左上到 `(i,j)` 的总和。  
> - `total = (pre[i + k][j + k] - pre[i][j + k] - pre[i + k][j] + pre[i][j])`：四角相减得到正方形内部的和，像是用四块拼图的面积求交集。  
> - `if possible(mid):`：如果当前 `mid` 边长可以找到满足条件的正方形，就把答案更新并尝试更大的 `mid`。

#### 复杂度

- **时间复杂度**：`O(m·n + log(min(m,n)) * m * n)`  
  - 前缀和预处理 `O(m·n)`。  
  - 二分搜索最多进行 `log(min(m,n))`（约 9 次，因为 `min ≤ 300`）轮检查。每轮检查遍历所有左上角，时间 `O(m·n)`，而每次查询正方形和是 `O(1)`（前缀和相减）。  
  - 用大白话说：**先花一次时间把“每页的累计字数”记下来，之后每次只需要几步算就能知道任意一段的总字数，整体只要几千次操作，瞬间跑完。**

- **空间复杂度**：`O(m·n)`  
  - 需要额外的前缀和矩阵 `pre`，大小比原矩阵多一行一列。  
  - 对于 `300×300` 的矩阵，这大约是 90,000 个整数，完全可以接受。

---

## 心得

- **核心技巧**：  
  1. **前缀和** —— 把二维累计和预先算好，子矩阵求和从 `O(k²)` 降到 `O(1)`。  
  2. **二分搜索** —— 利用“如果长度 k 可行，则更小的长度必定可行”的单调性，快速定位最大可行边长。

- **适用的题型**（类似技巧）  
  - “最大正方形 / 矩形满足某种约束” （如 LeetCode 1277）  
  - “在二维数组中寻找满足阈值的最小/最大子矩阵面积”  
  - “二维数组中查询子矩阵和” 相关的任何问题（如区域求和、子矩阵计数等）。

- **一句话总结**：  
  > 先把“每块地的累计肥料量”记下来（前缀和），再用“能否种植？”的二分法快速挑出最大可种植的正方形边长。

---

## 反思

- **第一反应**：  
  “把所有正方形都枚举，直接算和”——最自然的暴力思路，但会超时。

- **最容易踩的坑**  
  1. **边界检查**：正方形的左上角 `(i, j)` 必须保证 `i + k ≤ m` 且 `j + k ≤ n`，否则会越界。  
  2. **前缀和的坐标偏移**：因为 `pre` 多了一行一列，查询时要使用 `i+ k`、`j+ k` 等偏移，容易写错。  
  3. **二分搜索的终止条件**：`while left <= right` 与 `mid = (left + right)//2` 必须配合使用，否则会出现无限循环。

- **下次遇到同类题的第一步**：  
  先判断是否存在“单调性”——即某个属性（长度、面积、阈值）增大时可行性只会从 **True → False** 或 **False → True** 变化。如果有，立刻考虑二分搜索；随后检查是否可以用前缀和或其他预处理把**子结构查询**从线性降到常数。