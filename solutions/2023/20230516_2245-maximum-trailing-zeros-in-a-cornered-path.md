# #2245. 拐角路径的最大末尾零数 / Maximum Trailing Zeros in a Cornered Path

> 难度：中等 · 标签：Array、Matrix、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/maximum-trailing-zeros-in-a-cornered-path/)

---

## 题目（英文原版）

**Description**

You are given a 2D integer array grid of size m x n, where each cell contains a positive integer.
A cornered path is defined as a set of adjacent cells with at most one turn. More specifically, the path should exclusively move either horizontally or vertically up to the turn (if there is one), without returning to a previously visited cell. After the turn, the path will then move exclusively in the alternate direction: move vertically if it moved horizontally, and vice versa, also without returning to a previously visited cell.
The product of a path is defined as the product of all the values in the path.
Return the maximum number of trailing zeros in the product of a cornered path found in grid.
Note:

**Examples**

**Example 1:**

```
Input: grid = [[23,17,15,3,20],[8,1,20,27,11],[9,4,6,2,21],[40,9,1,10,6],[22,7,4,5,3]]
Output: 3
Explanation: The grid on the left shows a valid cornered path.
It has a product of 15 * 20 * 6 * 1 * 10 = 18000 which has 3 trailing zeros.
It can be shown that this is the maximum trailing zeros in the product of a cornered path.

The grid in the middle is not a cornered path as it has more than one turn.
The grid on the right is not a cornered path as it requires a return to a previously visited cell.
```

**Example 2:**

```
Input: grid = [[4,3,2],[7,6,1],[8,8,8]]
Output: 0
Explanation: The grid is shown in the figure above.
There are no cornered paths in the grid that result in a product with a trailing zero.
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 105
- 1 <= m * n <= 105
- 1 <= grid[i][j] <= 1000

---

## 题目（中文翻译）

给定一个大小为 `m × n` 的二维整数数组 `grid`，其中每个单元格包含一个正整数。  
**拐角路径 (cornered path)** 定义为至多包含一次转折 (turn) 的相邻单元格集合。具体来说，路径在转折之前只能沿水平方向或垂直方向移动，且不能回到已经访问过的单元格；转折之后，路径则只能沿另一方向（如果之前水平移动，则转为垂直移动，反之亦然），同样不能回到已访问的单元格。  

路径的 **乘积 (product)** 为路径上所有数值的乘积。  
返回 `grid` 中所有拐角路径的乘积所能拥有的最大 **末尾零数 (trailing zeros)**。

**示例 1**  
输入:  
```json
grid = [[23,17,15,3,20],
        [8,1,20,27,11],
        [9,4,6,2,21],
        [40,9,1,10,6],
        [22,7,4,5,3]]
```  
输出: `3`  
解释: 左侧的网格展示了一条合法的拐角路径。该路径的乘积为  
`15 * 20 * 6 * 1 * 10 = 18000`，其末尾有 `3` 个零。可以证明，这已经是所有拐角路径中乘积末尾零数的最大值。  

**示例 2**  
输入:  
```json
grid = [[4,3,2],
        [7,6,1],
        [8,8,8]]
```  
输出: `0`  
解释: 如上图所示的网格中，没有任何拐角路径的乘积能够产生末尾为零的情况。  

**约束条件**  
- `m == grid.length`  
- `n == grid[i].length`  
- `1 <= m, n <= 10^5`  
- `1 <= m * n <= 10^5`  
- `1 <= grid[i][j] <= 1000`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每一条可能的拐角路径都枚举出来，算出它们的乘积，再数乘积末尾有多少个 `0`，取最大值**。  
- **路径的形状**：从某个起点出发，只能向左/右/上/下走，最多转一次弯。也就是说路径形如 “─┐”、 “│─”、 “─│”、 “└─” 四种基本形（方向可以反向）。
- **枚举方式**：  
  1. 先枚举起点 `(r1, c1)`，再枚举终点 `(r2, c2)`。  
  2. 判断这两个点之间的最短 Manhattan 距离是否恰好等于 `|r1‑r2| + |c1‑c2|`（即只能走直线或只转一次）。  
  3. 若满足，就把路径上所有格子乘起来，计算 trailing zeros。  

> **哈希表的类比**：我们要统计每个格子里有多少个因子 `2` 和因子 `5`，就好像在查字典一样：键是格子坐标，值是 `(cnt2, cnt5)`。  

**为什么这个方法一定能得到正确答案？**  
因为我们把 **所有合法的拐角路径** 都遍历了一遍，最大值自然不会错过。

**时间/空间分析（大白话版）**  
- **时间**：  
  - 对每一对起点‑终点我们都要检查路径是否合法并遍历路径上的所有格子。  
  - 若网格有 `k = m·n` 个格子，起点‑终点组合大约是 `k²`，每条路径最坏遍历 `O(m+n)` 个格子。于是时间复杂度是 **`O(k³)`**，在最坏情况下相当于 **`O((10⁵)³)`**，根本跑不完。  
  - 用大白话说，就是“要把 100 万个格子两两配对，再把每条配对的路径全部算一遍”，这根本不可能在电脑上跑完。  

- **空间**：只需要存格子本身和临时计数，**`O(1)`**（不计输入本身）。

#### 代码（Python）

```python
from math import prod

def count_factor(x, p):
    """返回 x 中因子 p（2 或 5）的个数"""
    cnt = 0
    while x % p == 0:
        x //= p
        cnt += 1
    return cnt

def trailing_zeros_of_path(grid, cells):
    """cells 为路径上所有坐标的列表，返回该路径乘积的 trailing zeros"""
    total2, total5 = 0, 0
    for r, c in cells:
        total2 += count_factor(grid[r][c], 2)
        total5 += count_factor(grid[r][c], 5)
    return min(total2, total5)

def brute_force(grid):
    m, n = len(grid), len(grid[0])
    best = 0
    # 所有起点
    for r1 in range(m):
        for c1 in range(n):
            # 所有终点
            for r2 in range(m):
                for c2 in range(n):
                    # 必须是同一行或同一列，或只转一次
                    if r1 == r2 or c1 == c2:
                        # 直接走直线
                        cells = []
                        if r1 == r2:  # 同行
                            step = 1 if c2 > c1 else -1
                            for c in range(c1, c2 + step, step):
                                cells.append((r1, c))
                        else:          # 同列
                            step = 1 if r2 > r1 else -1
                            for r in range(r1, r2 + step, step):
                                cells.append((r, c1))
                        best = max(best, trailing_zeros_of_path(grid, cells))
                    else:
                        # 只能转一次拐角，两种走法都要尝试
                        # 先走横后走纵
                        cells = []
                        step = 1 if c2 > c1 else -1
                        for c in range(c1, c2 + step, step):
                            cells.append((r1, c))
                        step = 1 if r2 > r1 else -1
                        for r in range(r1 + step, r2 + step, step):
                            cells.append((r, c2))
                        best = max(best, trailing_zeros_of_path(grid, cells))

                        # 先走纵后走横
                        cells = []
                        step = 1 if r2 > r1 else -1
                        for r in range(r1, r2 + step, step):
                            cells.append((r, c1))
                        step = 1 if c2 > c1 else -1
                        for c in range(c1 + step, c2 + step, step):
                            cells.append((r2, c))
                        best = max(best, trailing_zeros_of_path(grid, cells))
    return best
```

> **注意**：以上代码仅为演示思路，实际运行会因为时间太长而超时。

#### 复杂度  

- **时间复杂度**：`O((m·n)³)`，相当于 `O(k³)`，在本题约等于 `O(10¹⁵)`，根本不可能完成。  
- **空间复杂度**：`O(1)`（不计输入本身），只用了常数级别的额外变量。

---

### 2. 最优解  

#### 思路  

暴力解的 **瓶颈** 在于：我们每次都要把路径上所有格子逐个遍历，导致指数级的时间。  
要把时间压到 **线性**（即 `O(m·n)`），必须 **把每条路径的 “因子 2 的总数” 与 “因子 5 的总数” 预先算好**，这样只要把几段前缀和相加，就能得到整条路径的统计。  

关键观察：

1. **Trailing zeros 只跟因子 2 与 5 的个数有关**  
   - 任意整数可以写成 `2^a * 5^b * other`（other 与 2、5 互质）。  
   - 乘积的因子 2 总数 = 所有格子里 `a` 的和，因子 5 总数 = 所有格子里 `b` 的和。  
   - 末尾的 `0` 的个数 = `min(total2, total5)`。  

2. **拐角路径的形状**  
   - 把拐角（转弯的格子）记作 **“肘部”**。  
   - 肘部左上、右上、左下、右下 四个方向的 **直线段** 必须是 **从肘部一直向外走**（不回头）。  
   - 因此，一条合法拐角路径可以拆成 **肘部 + 两条直线**（每条直线可能长度为 0，即不转弯的纯直线）。  

3. **前缀和**  
   - 对每一行，计算从左到右的累计因子 2、5；同理从右到左。  
   - 对每一列，计算从上到下、从下到上 的累计因子 2、5。  
   - 这相当于在 **每个方向** 上建立 “查字典”——给定起点和终点，**O(1)** 时间即可得到这段直线的因子和。  

4. **遍历所有肘部**  
   对每个格子 `(i, j)`，我们尝试四种拐角形状：  
   - 向上 + 向左  
   - 向上 + 向右  
   - 向下 + 向左  
   - 向下 + 向右  
   对每种形状，使用前缀和快速得到两段直线的 `(cnt2, cnt5)`，再 **加上肘部本身的因子**（因为肘部会被算两次，需要减一次）。  
   最后 `ans = max(ans, min(total2, total5))`。  

5. **为什么是 O(m·n)？**  
   - 前缀和的构建遍历每个格子一次 → `O(m·n)`。  
   - 再遍历每个格子作为肘部，四种方向的查询都是 **常数时间** → 仍是 `O(m·n)`。  

#### 详细步骤（带类比）  

| 步骤 | 类比 | 说明 |
|------|------|------|
| **统计因子** | 把每个数拆成 “有多少个 2” + “有多少个 5” | 用 `while` 循环除以 2、5，得到 `(cnt2, cnt5)`，相当于给每个格子贴上两张小标签。 |
| **行前缀** | 像在一本书的左边写下每页累计出现的某个词的次数 | `row_left[i][j]` = 从左到 `(i,j)` 的 `2` 的总数；同理 `row_left5`。右到左同理。 |
| **列前缀** | 类似把一本笔记本竖着翻，记录每页的累计次数 | `col_up[i][j]` = 从上到 `(i,j)` 的 `2` 总数；同理 `col_up5`，下到上亦如此。 |
| **查询直线段** | 像在字典里查找 “从第 a 页到第 b 页的总词数” | 例如 **左段** = `row_left[i][j] - row_left[i][k-1]`（k 为左端点），如果 k 为 0 则直接取 `row_left[i][j]`。 |
| **合并两段 + 肘部** | 把两条绳子系在同一个结上，结本身的重量只算一次 | `total2 = up2 + left2 + cell2 - cell2`（因为肘部已经在两段里都算了一次，需要减去一次）。 |
| **取最小** | 末尾的 `0` 受最少的那种因子限制 | `zeros = min(total2, total5)`。 |

#### 代码（Python）

```python
def count_factor(x, p):
    """返回 x 中因子 p（2 或 5）的个数"""
    cnt = 0
    while x % p == 0:
        x //= p
        cnt += 1
    return cnt

def maxTrailingZeros(grid):
    m, n = len(grid), len(grid[0])

    # 1) 预处理每个格子里 2 和 5 的个数
    twos  = [[0] * n for _ in range(m)]
    fives = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            twos[i][j]  = count_factor(grid[i][j], 2)
            fives[i][j] = count_factor(grid[i][j], 5)

    # 2) 四个方向的前缀和：左、右、上、下
    #    left[i][j] = (2的累计, 5的累计) 从行首到 (i,j)（含）
    left2  = [[0] * n for _ in range(m)]
    left5  = [[0] * n for _ in range(m)]
    right2 = [[0] * n for _ in range(m)]
    right5 = [[0] * n for _ in range(m)]
    up2    = [[0] * n for _ in range(m)]
    up5    = [[0] * n for _ in range(m)]
    down2  = [[0] * n for _ in range(m)]
    down5  = [[0] * n for _ in range(m)]

    # 行的左→右、右→左前缀
    for i in range(m):
        acc2 = acc5 = 0
        for j in range(n):
            acc2 += twos[i][j]
            acc5 += fives[i][j]
            left2[i][j] = acc2
            left5[i][j] = acc5
        acc2 = acc5 = 0
        for j in range(n - 1, -1, -1):
            acc2 += twos[i][j]
            acc5 += fives[i][j]
            right2[i][j] = acc2
            right5[i][j] = acc5

    # 列的上→下、下→上前缀
    for j in range(n):
        acc2 = acc5 = 0
        for i in range(m):
            acc2 += twos[i][j]
            acc5 += fives[i][j]
            up2[i][j] = acc2
            up5[i][j] = acc5
        acc2 = acc5 = 0
        for i in range(m - 1, -1, -1):
            acc2 += twos[i][j]
            acc5 += fives[i][j]
            down2[i][j] = acc2
            down5[i][j] = acc5

    # 3) 以每个格子为拐角，枚举四种 L 形
    ans = 0
    for i in range(m):
        for j in range(n):
            # 当前格子的因子（会在两段中重复出现，需要在最后减一次）
            cur2, cur5 = twos[i][j], fives[i][j]

            # (上, 左)
            up_seg2  = up2[i][j]   - (up2[i-1][j]   if i > 0 else 0)
            up_seg5  = up5[i][j]   - (up5[i-1][j]   if i > 0 else 0)
            left_seg2 = left2[i][j] - (left2[i][j-1] if j > 0 else 0)
            left_seg5 = left5[i][j] - (left5[i][j-1] if j > 0 else 0)
            total2 = up_seg2 + left_seg2 - cur2   # 减一次重复的肘部
            total5 = up_seg5 + left_seg5 - cur5
            ans = max(ans, min(total2, total5))

            # (上, 右)
            right_seg2 = right2[i][j] - (right2[i][j+1] if j + 1 < n else 0)
            right_seg5 = right5[i][j] - (right5[i][j+1] if j + 1 < n else 0)
            total2 = up_seg2 + right_seg2 - cur2
            total5 = up_seg5 + right_seg5 - cur5
            ans = max(ans, min(total2, total5))

            # (下, 左)
            down_seg2 = down2[i][j] - (down2[i+1][j] if i + 1 < m else 0)
            down_seg5 = down5[i][j] - (down5[i+1][j] if i + 1 < m else 0)
            total2 = down_seg2 + left_seg2 - cur2
            total5 = down_seg5 + left_seg5 - cur5
            ans = max(ans, min(total2, total5))

            # (下, 右)
            total2 = down_seg2 + right_seg2 - cur2
            total5 = down_seg5 + right_seg5 - cur5
            ans = max(ans, min(total2, total5))

    return ans
```

> **代码要点解释**  
> - `up_seg2` 等变量取得的是 **从当前格子往上（或左、右、下）一直到边缘** 的因子和。因为前缀和是从边缘累加的，直接相减即可得到这段。  
> - `- cur2`（或 `- cur5`）是因为肘部在两段里都被算进来了，实际乘积只需要它一次。  
> - 四种组合分别对应四个可能的 L 形（转弯方向），每次都更新全局最大 `ans`。

#### 复杂度  

- **时间复杂度**：`O(m·n)`  
  - 前缀和四遍遍历：`4·m·n`。  
  - 再遍历每个格子并做常数次查询：`O(m·n)`。  
  - 整体仍是线性，和网格大小成正比。  
- **空间复杂度**：`O(m·n)`  
  - 需要存四个方向的前缀和以及因子计数矩阵。  
  - 这在本题的限制 `m·n ≤ 10⁵` 内是完全可以接受的。  

---

## 心得  

- **核心技巧**：把 “末尾 0 的个数 = min(因子 2 的总数, 因子 5 的总数)” 这一本质转化为 **二维前缀和** 的求和问题。  
- **适用的题型**  
  1. 需要统计路径上某类累加信息（如素因子、出现次数）并且路径形状受限的题目。  
  2. “拐角路径” 或 “L 形路径” 之类的二维几何约束。  
  3. 类似 “Maximum Sum of 3 Non‑Overlapping Subarrays” 在二维上的变形，只是把求和换成求 **min(2,5)**。  
- **一句话总结解题钥匙**：**把乘积的 trailing zeros 转化为两个独立的前缀和（2 与 5），再以每个格子为拐点，利用前缀和快速合并两段直线**。

---

## 反思  

- **第一反应**：直接枚举所有路径，求乘积，再数零。  
- **最容易踩的坑**  
  1. **忘记肘部重复计数**：两段直线都包含拐角格子，需要在合并时减掉一次。  
  2. **边界处理**：在前缀和相减时，如果段的起点是边缘，需要特判防止访问负索引。  
  3. **只算 2 与 5**：很多人会误以为要算所有因子，实际只需关注 2 与 5。  
- **下次遇到同类题**：第一步先思考 **“这道题的答案到底由哪些可加的局部信息决定？”**，若是乘积的零、最大公约数、最小公倍数等，往往可以拆解成 **对每个元素的某种计数**，再用前缀和或动态规划把局部计数快速合并。