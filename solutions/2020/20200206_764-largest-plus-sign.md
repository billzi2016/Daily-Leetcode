# #764. **最大十字形** / Largest Plus Sign

> 难度：中等 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/largest-plus-sign/)

---

## 题目（英文原版）

**Description**

You are given an integer n. You have an n x n binary grid grid with all values initially 1's except for some indices given in the array mines. The ith element of the array mines is defined as mines[i] = [xi, yi] where grid[xi][yi] == 0.
Return the order of the largest axis-aligned plus sign of 1's contained in grid. If there is none, return 0.
An axis-aligned plus sign of 1's of order k has some center grid[r][c] == 1 along with four arms of length k - 1 going up, down, left, and right, and made of 1's. Note that there could be 0's or 1's beyond the arms of the plus sign, only the relevant area of the plus sign is checked for 1's.

**Examples**

**Example 1:**

```
Input: n = 5, mines = [[4,2]]
Output: 2
Explanation: In the above grid, the largest plus sign can only be of order 2. One of them is shown.
```

**Example 2:**

```
Input: n = 1, mines = [[0,0]]
Output: 0
Explanation: There is no plus sign, so return 0.
```

**Constraints**

- 1 <= n <= 500
- 1 <= mines.length <= 5000
- 0 <= xi, yi < n
- All the pairs (xi, yi) are unique.

---

## 题目（中文翻译）

你得到一个整数 `n`。构造一个 `n × n` 的二进制网格（binary grid） `grid`，初始时所有位置的值均为 `1`，但数组 `mines` 中给出的一些坐标会被设为 `0`。`mines[i] = [xi, yi]` 表示 `grid[xi][yi] == 0`。

返回网格中 **轴对齐的十字形（axis-aligned plus sign）** 所能达到的最大阶数（order）。如果不存在十字形，返回 `0`。

**定义**  
阶数为 `k` 的轴对齐十字形必须满足：
- 存在中心格子 `grid[r][c] == 1`；
- 以该中心向上、下、左、右各延伸 `k‑1` 个格子，且这些格子全部为 `1`，形成四条臂（arms）；
- 只需要检查十字形覆盖的这 `4·(k‑1) + 1` 个格子是否全为 `1`，十字形之外的格子可以是 `0` 也可以是 `1`。

---

### 示例

**示例 1**

```text
Input: n = 5, mines = [[4,2]]
Output: 2
Explanation: 如上图所示，网格中最大的十字形只能是阶数为 2。图中展示了其中一种情况。
```

**示例 2**

```text
Input: n = 1, mines = [[0,0]]
Output: 0
Explanation: 网格中不存在十字形，返回 0。
```

---

### 约束条件

- `1 <= n <= 500`
- `1 <= mines.length <= 5000`
- `0 <= xi, yi < n`
- 所有 `(xi, yi)` 均互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

把整个 `n × n` 的网格想象成一张棋盘，棋盘上大多数格子都是 `1`，只有 `mines` 给出的坐标是 `0`（相当于棋盘上被“挖掉”的格子）。  
我们要找的十字形（plus sign）可以这么理解：

- 选一个中心格子 `(r, c)`，它必须是 `1`。  
- 从中心往上、下、左、右各走相同的步数 `k‑1`，走过的每个格子也必须是 `1`。  
- 只要四条臂都满足，这个十字的 **阶数**（order）就是 `k`。

**最直接的办法**是：

1. 对每个可能的中心格子 `(r, c)`（遍历所有 `n²` 个格子）。  
2. 对每一种可能的阶数 `k`（从 `1` 开始，一直尝试到超出边界或碰到 `0` 为止）。  
3. 检查四个方向的 `k‑1` 步里有没有 `0`，如果有就停止；如果四条臂都全是 `1`，记录下当前的 `k`。  

这就像在棋盘上放大镜，一格格、一步步地验证“能否成十字”。  

- **为什么正确**：我们穷举了所有中心和所有可能的大小，只要有合法的十字形，就一定会在某一次遍历中被发现并记录。  
- **时间/空间复杂度**：  
  - 对每个格子我们最坏要检查 `O(n)` 步（因为十字最长也只能到达棋盘边缘），所以总时间是 `O(n³)`。  
  - 只用了原始的 `grid`，没有额外的存储，空间是 `O(1)`（不计输入本身）。

> **大白话解释**：  
> `O(n³)` 就像“立方体”一样增长。如果 `n = 100`，操作次数大约是 `100 × 100 × 100 = 1,000,000`，对电脑来说还能接受。但当 `n` 达到题目上限 `500` 时，就会是 `125,000,000` 次，明显会超时。

#### 代码（Python）

```python
def orderOfLargestPlusSign_bruteforce(n: int, mines: list[list[int]]) -> int:
    # 1. 先把所有 mines 标记为 0，其他格子默认是 1
    grid = [[1] * n for _ in range(n)]
    for x, y in mines:
        grid[x][y] = 0

    max_order = 0                     # 记录最大的阶数

    # 2. 枚举每一个可能的中心格子
    for r in range(n):
        for c in range(n):
            if grid[r][c] == 0:       # 中心必须是 1，若是 0 直接跳过
                continue

            # 3. 以当前中心尝试更大的 k（从 1 开始）
            cur_k = 1                  # k=1 表示只要中心本身是 1 就算合法
            while True:
                # 四个方向要检查的步数是 cur_k-1
                length = cur_k - 1
                ok = True

                # 上
                for d in range(1, length + 1):
                    if r - d < 0 or grid[r - d][c] == 0:
                        ok = False
                        break
                if not ok:
                    break

                # 下
                for d in range(1, length + 1):
                    if r + d >= n or grid[r + d][c] == 0:
                        ok = False
                        break
                if not ok:
                    break

                # 左
                for d in range(1, length + 1):
                    if c - d < 0 or grid[r][c - d] == 0:
                        ok = False
                        break
                if not ok:
                    break

                # 右
                for d in range(1, length + 1):
                    if c + d >= n or grid[r][c + d] == 0:
                        ok = False
                        break
                if not ok:
                    break

                # 四个方向都通过，说明当前 k 合法，尝试更大的 k
                cur_k += 1

            # while 循环结束时，cur_k 已经比合法的最大值大 1
            max_order = max(max_order, cur_k - 1)

    return max_order
```

#### 复杂度

- **时间复杂度**：`O(n³)`  
  - 解释：我们遍历了 `n²` 个中心，每个中心最坏要检查 `n` 步（四个方向的总和仍是线性），于是乘起来就是立方级别的操作量。
- **空间复杂度**：`O(1)`（不计输入 `grid` 本身）  
  - 只用了常数级的额外变量 `max_order、cur_k、ok` 等。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都要重新遍历四个方向**。实际上，**同一个方向上相邻格子的连续 `1` 数量是可以提前算好的**，这正是动态规划（DP）擅长的事。

我们把每个格子在四个方向（左、右、上、下）上能看到的连续 `1` 的长度预先算出来，记为：

- `left[r][c]`   – 从 `(r,c)` 往左（包括自己）连续的 `1` 的个数  
- `right[r][c]`  – 往右的连续 `1` 个数  
- `up[r][c]`     – 往上（向上）连续的 `1` 个数  
- `down[r][c]`   – 往下连续的 `1` 个数  

有了这四个表格，**十字形的阶数**在 `(r,c)` 处就可以直接得到：

```
order(r,c) = min(left[r][c], right[r][c], up[r][c], down[r][c])
```

因为十字的每条臂都不能超过最短的那一条。

**如何用 DP 求四个方向的连续长度？**  
以 `left` 为例：从左到右遍历每一行，若当前格子是 `1`，则  

```
left[r][c] = left[r][c-1] + 1
```

否则（是 `0`）则 `left[r][c] = 0`。  
右、上、下方向同理，只是遍历顺序不同（右从右往左，上从上往下，下从下往上）。

这样只需要 **四次线性遍历**（每次遍历 `n²` 个格子）就能得到全部信息，时间从 `O(n³)` 降到 `O(n²)`，空间也只需要四个 `n × n` 的整型数组（或在原地复用）——`O(n²)`。

> **类比**：  
> 想象你在一条直路上放置路灯，每根路灯的亮度取决于它左边最近的黑暗区距离。一次从左到右走过去，你就能把每个灯的左侧可视距离记录下来；再从右到左走一遍，就得到右侧的可视距离。十字形的中心格子只需要取四个方向中最短的那段可视距离，才能保证四臂等长。

#### 代码（Python）

```python
def orderOfLargestPlusSign(n: int, mines: list[list[int]]) -> int:
    # 1. 把所有格子初始化为 1，随后把 mines 标记为 0
    grid = [[1] * n for _ in range(n)]
    for x, y in mines:
        grid[x][y] = 0

    # 2. 创建四个 DP 表，全部初始化为 0
    left  = [[0] * n for _ in range(n)]
    right = [[0] * n for _ in range(n)]
    up    = [[0] * n for _ in range(n)]
    down  = [[0] * n for _ in range(n)]

    # 3. 从左到右、从上到下填充 left、up
    for r in range(n):
        for c in range(n):
            if grid[r][c] == 1:
                left[r][c] = (left[r][c - 1] if c > 0 else 0) + 1
                up[r][c]   = (up[r - 1][c]   if r > 0 else 0) + 1
            # 若是 0，保持 0（默认已是 0）

    # 4. 从右到左、从下到上填充 right、down
    for r in range(n - 1, -1, -1):
        for c in range(n - 1, -1, -1):
            if grid[r][c] == 1:
                right[r][c] = (right[r][c + 1] if c + 1 < n else 0) + 1
                down[r][c]  = (down[r + 1][c]   if r + 1 < n else 0) + 1

    # 5. 计算每个格子能构成的最大阶数，取最大值返回
    best = 0
    for r in range(n):
        for c in range(n):
            # 四个方向的最小值就是以 (r,c) 为中心的十字最大阶数
            cur = min(left[r][c], right[r][c], up[r][c], down[r][c])
            best = max(best, cur)

    return best
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 解释：我们只遍历了四遍 `n × n` 的矩阵，每次都是线性操作。相比暴力的 `O(n³)`，这里的运行时间随 `n` 的增长只会呈二次方增长，500 × 500 的情况也能轻松在毫秒级完成。
- **空间复杂度**：`O(n²)`  
  - 解释：需要存四个同样大小的 DP 表，合计约 `4 * n²` 个整数。对于 `n = 500`，大约占用 1 MB 左右的内存，完全在题目限制之内。

---

## 心得

- **核心技巧**：使用四个方向的“前缀连续 1 长度”动态规划，把每个格子在四个方向上的信息预处理好，再取最小值即得十字的最大阶数。
- **适用的题型**  
  1. **Largest X Sign**（类似的十字形、叉形等）  
  2. **Maximal Square**（求全 1 正方形的最大面积，亦使用四方向连续 1 长度）  
  3. **Binary Matrix Largest Sub‑rectangle with all 1**（利用上下连续长度做直方图求解）
- **一句话总结**：把“每个方向能伸多远”提前算好，十字的大小只需要一次 `min` 运算。

---

## 反思

- **第一反应**：看到“十字形”，自然想到暴力枚举中心并逐步扩展——直观但容易超时。
- **最容易踩的坑**  
  - **边界检查**：向左/右/上/下扩展时必须防止数组越界。  
  - **`0` 的位置**：如果 `mines` 中的坐标很多，直接在原始 `grid` 上标记 `0`，否则在 DP 中会错误地累计长度。  
  - **返回值**：如果整张表全是 `0`，`best` 应该是 `0`（而不是 `1`），因为没有合法的十字中心。
- **下次类似题目**：第一步先**思考能否把局部信息（如连续 1 的长度）用 DP 预处理**，再在中心位置做一次合并运算，往往能把指数级的暴力降到多项式级。