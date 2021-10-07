# #1504. 全为 1 的子矩阵计数 / Count Submatrices With All Ones

> 难度：中等 · 标签：Array、Dynamic Programming、Stack、Matrix、Monotonic Stack · [LeetCode 链接](https://leetcode.com/problems/count-submatrices-with-all-ones/)

---

## 题目（英文原版）

**Description**

Given an m x n binary matrix mat, return the number of submatrices that have all ones.

**Examples**

**Example 1:**

```
Input: mat = [[1,0,1],[1,1,0],[1,1,0]]
Output: 13
Explanation: 
There are 6 rectangles of side 1x1.
There are 2 rectangles of side 1x2.
There are 3 rectangles of side 2x1.
There is 1 rectangle of side 2x2. 
There is 1 rectangle of side 3x1.
Total number of rectangles = 6 + 2 + 3 + 1 + 1 = 13.
```

**Example 2:**

```
Input: mat = [[0,1,1,0],[0,1,1,1],[1,1,1,0]]
Output: 24
Explanation: 
There are 8 rectangles of side 1x1.
There are 5 rectangles of side 1x2.
There are 2 rectangles of side 1x3. 
There are 4 rectangles of side 2x1.
There are 2 rectangles of side 2x2. 
There are 2 rectangles of side 3x1. 
There is 1 rectangle of side 3x2. 
Total number of rectangles = 8 + 5 + 2 + 4 + 2 + 2 + 1 = 24.
```

**Constraints**

- 1 <= m, n <= 150
- mat[i][j] is either 0 or 1.

---

## 题目（中文翻译）

给定一个 `m x n` 的二进制矩阵（binary matrix）`mat`，返回所有元素全为 `1` 的子矩阵（submatrix）的数量。

**示例 1**  
**输入**: `mat = [[1,0,1],[1,1,0],[1,1,0]]`  
**输出**: `13`  
**解释**:  
- 有 6 个尺寸为 `1x1` 的矩形。  
- 有 2 个尺寸为 `1x2` 的矩形。  
- 有 3 个尺寸为 `2x1` 的矩形。  
- 有 1 个尺寸为 `2x2` 的矩形。  
- 有 1 个尺寸为 `3x1` 的矩形。  

总矩形数 = `6 + 2 + 3 + 1 + 1 = 13`。

**示例 2**  
**输入**: `mat = [[0,1,1,0],[0,1,1,1],[1,1,1,0]]`  
**输出**: `24`  
**解释**:  
- 有 8 个尺寸为 `1x1` 的矩形。  
- 有 5 个尺寸为 `1x2` 的矩形。  
- 有 2 个尺寸为 `1x3` 的矩形。  
- 有 4 个尺寸为 `2x1` 的矩形。  
- 有 2 个尺寸为 `2x2` 的矩形。  
- 有 2 个尺寸为 `3x1` 的矩形。  
- 有 1 个尺寸为 `3x2` 的矩形。  

总矩形数 = `8 + 5 + 2 + 4 + 2 + 2 + 1 = 24`。

**约束条件**  
- `1 <= m, n <= 150`  
- `mat[i][j]` 只能是 `0` 或 `1`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **枚举所有可能的子矩阵**，然后检查它们是否全部由 `1` 组成。  
子矩阵由左上角 `(r1, c1)` 与右下角 `(r2, c2)` 唯一确定，只要 `r1 ≤ r2`、`c1 ≤ c2` 就是合法的。

- **数据结构**：我们只需要遍历二维数组本身，**不需要额外的数据结构**。如果把矩阵看成一本“表格”，枚举左上角就像在表格里挑一个起点，枚举右下角就是在这个起点的右下方向“画框”。  
- **正确性**：因为我们把**每一种可能的矩形**都检查了一遍，只要矩形里没有 `0`，就计数一次；所有合法的矩形都被统计，答案自然正确。  

#### 代码（Python）

```python
from typing import List

def numSubmatrices_bruteforce(mat: List[List[int]]) -> int:
    m, n = len(mat), len(mat[0])
    ans = 0

    # 枚举左上角 (r1, c1)
    for r1 in range(m):
        for c1 in range(n):
            # 枚举右下角 (r2, c2)
            for r2 in range(r1, m):
                for c2 in range(c1, n):
                    # 检查子矩阵是否全为 1
                    all_one = True
                    for i in range(r1, r2 + 1):
                        for j in range(c1, c2 + 1):
                            if mat[i][j] == 0:      # 只要出现 0 就不是合法矩形
                                all_one = False
                                break
                        if not all_one:
                            break
                    if all_one:
                        ans += 1
    return ans
```

> **关键行解释**  
> - 第 8‑11 行：四层循环枚举左上角和右下角，遍历所有子矩阵。  
> - 第 13‑21 行：再用两层循环检查子矩阵内部是否全是 `1`。一旦发现 `0` 就立刻退出（`break`），避免不必要的比较。

#### 复杂度

- **时间复杂度**：`O(m² · n² · (m·n))` → 简化为 **`O(m³·n³)`**，因为最坏情况下要检查每个子矩阵内部的每个元素。  
  - 用大白话说，就是“先挑起点再挑终点”，每挑一次都要把矩形里所有格子翻一遍，次数非常多。  
- **空间复杂度**：`O(1)`，只用了常数个额外变量。

> 由于 `m, n ≤ 150`，暴力解在最坏情况下会有约 `150⁶ ≈ 11·10¹⁰` 次操作，根本跑不完。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到 **瓶颈在于反复检查子矩阵内部**。如果能在 **遍历过程中** 直接知道有多少合法矩形，就能省掉那层“内部检查”。  
下面一步步推导出高效的做法：

1. **把问题转化为“以每一行作为底边的矩形”。**  
   对于第 `i` 行，我们只关心 **以第 `i` 行结尾**（即底部在第 `i` 行）的所有全 `1` 子矩阵。把所有行的贡献加起来，就是答案。

2. **用 `height[j]` 记录第 `j` 列向上连续的 `1` 的数量。**  
   - 当 `mat[i][j] == 1` 时，`height[j] = height[j] + 1`（向上延伸）。  
   - 当 `mat[i][j] == 0` 时，`height[j] = 0`（这列在当前行断了，后面就不能再组成全 `1` 的矩形了）。  
   这一步类似“把每一列看成一根柱子”，柱子的高度就是连续的 `1`。

3. **在每一行，统计以该行结尾的矩形数量。**  
   现在我们拥有一行 `height`，它相当于 **直方图**。我们要统计的是：**在这条直方图里，所有以当前行底部为下边界的矩形有多少**。  
   这正是**单调栈（Monotonic Stack）**的典型应用：  
   - 栈里保存 **柱子的下标**，并且保持 **对应的高度递增**。  
   - 当遍历到第 `j` 列时，若栈顶高度大于当前高度，就把栈顶弹出，因为它已经被当前更矮的柱子“限制”了宽度。  
   - 每弹出一次，就可以计算出 **以该柱子为最右侧、底部在当前行的矩形数量**。  

   具体公式：  
   - 设弹出的下标为 `k`，`h = height[k]`。  
   - `left = stack[-1]`（弹出后栈顶的下标），如果栈为空则 `left = -1`。  
   - 以 `k` 为最右边界、底部在当前行的矩形数量为 `h * (k - left)`，但这里要 **累计** 前面已经算过的更窄的矩形。  
   - 为了避免重复计数，我们维护一个 `cnt` 数组，`cnt[j]` 表示 **以第 `j` 列为最右边界的矩形数量**。  
   - 当弹出 `k` 时：`cnt[j] = cnt[left] + h * (j - left)`，其中 `j` 是当前遍历到的列（即右边界）。

4. **把每行的计数累加到答案**。  

整体流程：

```
for each row i:
    update height[]
    use monotonic stack on height to compute cnt[]
    ans += sum(cnt)
```

这样每个元素只会 **进栈一次、出栈一次**，整体是线性时间。

#### 代码（Python）

```python
from typing import List

def numSubmatrices_optimal(mat: List[List[int]]) -> int:
    """
    统计所有全 1 子矩阵的数量
    思路：以每一行作为底边，利用单调栈统计以该行结尾的矩形数目
    """
    m, n = len(mat), len(mat[0])
    height = [0] * n          # 每列向上的连续 1 的高度
    ans = 0

    for i in range(m):        # 逐行遍历
        # 1) 更新 height
        for j in range(n):
            if mat[i][j] == 1:
                height[j] += 1
            else:
                height[j] = 0

        # 2) 单调栈统计当前行结尾的矩形数量
        stack = []            # 栈中保存列下标，保证对应的 height 单调递增
        cnt = [0] * n         # cnt[j] = 以第 j 列为最右边界的合法矩形数

        for j in range(n):
            # 当栈顶高度 > 当前高度时弹出，意味着当前列把它的宽度限制住了
            while stack and height[stack[-1]] > height[j]:
                stack.pop()

            if stack:                     # 栈不空，左边最近比当前低的柱子下标是 stack[-1]
                left = stack[-1]
                # 以 j 为最右边界的矩形数 = 左边界的矩形数 + 当前柱子高度 * 宽度
                cnt[j] = cnt[left] + height[j] * (j - left)
            else:                         # 没有更低的柱子，左边界是 -1
                cnt[j] = height[j] * (j + 1)   # (j - (-1)) = j+1

            stack.append(j)               # 当前列进入栈，可能成为后面的左边界
            ans += cnt[j]                 # 累计答案

    return ans
```

> **关键行解释**  
> - 第 12‑16 行：把每列的 “向上连续 1 的高度” 更新好，等价于把矩阵转成直方图。  
> - 第 21‑30 行：维护 **单调递增栈**，当出现更矮的柱子时把高柱子弹出，保证栈顶永远是左侧最近的 **不高于当前** 的柱子。  
> - 第 24‑27 行：利用 **左侧最近更低柱子的位置** `left`，递推得到 `cnt[j]`（以 `j` 为右边界的矩形数量）。  
> - 第 32 行：把本行所有以 `j` 为右边界的矩形计入答案。

#### 复杂度

- **时间复杂度**：`O(m · n)`  
  - 每个元素只会 **进入栈一次、离开栈一次**，所以整行的处理是线性的。  
  - 用大白话说，就是“遍历矩阵一次就把答案算完”，比暴力的几百倍甚至上千倍快。

- **空间复杂度**：`O(n)`  
  - 只用了 `height`、`stack`、`cnt` 三个长度为 `n` 的数组。  
  - 与矩阵宽度成正比，远小于 `m·n`。

> 与暴力解相比，时间从 **指数级** 降到了 **线性级**，在最大输入 `150 × 150` 时几乎瞬间返回结果。

---

## 心得

- **核心技巧**：把二维子矩阵计数问题转化为 **每行的直方图计数**，并利用 **单调栈** 在 O(1) 时间内得到每列的贡献。  
- **适用题型**：  
  1. **统计全 1 子矩阵**（本题）。  
  2. **最大矩形面积**（LeetCode 85），同样使用单调栈求直方图的最大矩形。  
  3. **子数组最小值之和**（LeetCode 907），利用单调栈求每个元素作为最小值的贡献区间。  
- **一句话总结**：把“所有子矩形”拆成“每一行到底的矩形”，再用单调栈把每行的计数一次性算完，就是解题钥匙。

---

## 反思

- **第一反应**：直接枚举四个边界，检查每个子矩阵是否全为 `1`。这看起来最直观，却忽略了大量重复检查。  
- **最容易踩的坑**：  
  - **边界处理**：单调栈弹出后若栈为空，需要把左边界视作 `-1`，否则宽度计算会出错。  
  - **高度为 0 的列**：一旦出现 `0`，对应的 `height` 必须立刻归零，否则会把跨越 `0` 的矩形误计入。  
  - **累加方式**：`cnt[j]` 必须基于左侧最近更低柱子的 `cnt[left]` 累加，单独 `height[j] * (j-left)` 会漏掉左侧更宽的矩形。  
- **下次思路**：看到“子矩阵/子数组全为某个值”这类计数题，第一步就尝试把 **“以某一行（列）结束”** 的子结构抽出来，看能否用 **前缀、单调栈或 DP** 把重复工作合并。这样往往能把指数级暴力转化为线性或准线性解法。