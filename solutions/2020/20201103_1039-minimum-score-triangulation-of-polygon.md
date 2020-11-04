# #1039. 最小得分三角剖分 / Minimum Score Triangulation of Polygon

> 难度：中等 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/minimum-score-triangulation-of-polygon/)

---

## 题目（英文原版）

**Description**

You have a convex n-sided polygon where each vertex has an integer value. You are given an integer array values where values[i] is the value of the ith vertex in clockwise order.
Polygon triangulation is a process where you divide a polygon into a set of triangles and the vertices of each triangle must also be vertices of the original polygon. Note that no other shapes other than triangles are allowed in the division. This process will result in n - 2 triangles.
You will triangulate the polygon. For each triangle, the weight of that triangle is the product of the values at its vertices. The total score of the triangulation is the sum of these weights over all n - 2 triangles.
Return the minimum possible score that you can achieve with some triangulation of the polygon.

**Examples**

**Example 1:**

```
Input: values = [1,2,3]
Output: 6
Explanation: The polygon is already triangulated, and the score of the only triangle is 6.
```

**Example 2:**

```
Input: values = [3,7,4,5]
Output: 144
Explanation: There are two triangulations, with possible scores: 3*7*5 + 4*5*7 = 245, or 3*4*5 + 3*4*7 = 144. The minimum score is 144.
```

**Example 3:**

```
Input: values = [1,3,1,4,1,5]
Output: 13
Explanation: The minimum score triangulation is 1*1*3 + 1*1*4 + 1*1*5 + 1*1*1 = 13.
```

**Constraints**

- n == values.length
- 3 <= n <= 50
- 1 <= values[i] <= 100

---

## 题目（中文翻译）

给定一个凸 $n$ 边形，且每个顶点都有一个整数值。数组 `values` 中的 `values[i]` 表示按顺时针顺序第 $i$ 个顶点的值。

**多边形三角剖分（polygon triangulation）** 是指将多边形划分为若干个三角形的过程，且每个三角形的三个顶点必须都是原多边形的顶点，划分后不允许出现除三角形以外的其他形状。该过程会产生 $n - 2$ 个三角形。

现在你需要对该多边形进行三角剖分。对于每个三角形，其权重等于其三个顶点值的乘积。整个剖分的总得分是所有 $n - 2$ 个三角形权重的和。

返回在所有可能的三角剖分方式中能够得到的**最小总得分**。

## 示例

### 示例 1
**输入**  
```json
values = [1,2,3]
```
**输出**  
```
6
```
**解释**  
多边形已经只有一个三角形，唯一的三角形权重为 $1 \times 2 \times 3 = 6$。

### 示例 2
**输入**  
```json
values = [3,7,4,5]
```
**输出**  
```
144
```
**解释**  
存在两种不同的三角剖分方式，得到的得分分别为  
$3 \times 7 \times 5 + 4 \times 5 \times 7 = 245$，或  
$3 \times 4 \times 5 + 3 \times 4 \times 7 = 144$。  
最小得分为 **144**。

### 示例 3
**输入**  
```json
values = [1,3,1,4,1,5]
```
**输出**  
```
13
```
**解释**  
最小得分的剖分为  
$1 \times 1 \times 3 + 1 \times 1 \times 4 + 1 \times 1 \times 5 + 1 \times 1 \times 1 = 13$。

## 约束条件

- $n = \text{values.length}$
- $3 \le n \le 50$
- $1 \le \text{values}[i] \le 100$

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**枚举所有可能的三角形划分**，把每一种划分算出它的得分，最后取最小值。  
- **数据结构**：我们只需要一个列表 `values` 保存每个顶点的数值。  
- **生活化类比**：把多边形想成一块披萨，披萨上有 n 条切口（顶点），我们要把它切成 `n‑2` 块三角形披萨。暴力解相当于把每一种切法都尝试一次，再算出每块三角形披萨的“味道”（顶点数值的乘积），最后挑出味道最淡的切法。  
- **为什么正确**：只要遍历了**所有**合法的三角化方式，就一定能找到最小的总分。  

实现时可以使用递归：  
1. 选定一个“根三角形”，它一定包含顶点 `0`、`i`、`j`（`0 < i < j < n`），其中 `i` 与 `j` 分别是当前子多边形的两端。  
2. 该根三角形把多边形分成左侧子多边形 `[0 … i]` 和右侧子多边形 `[i … j]`（注意端点重叠），递归求它们的最小得分。  
3. 把根三角形的得分 `values[0] * values[i] * values[j]` 加上两侧子问题的最小得分，就是当前划分的总分。  
4. 对所有可能的 `i` 取最小值。

> **注意**：递归会产生大量重复计算（同一段子多边形会被求解很多次），所以这就是所谓的“暴力”。  

#### 代码（Python）

```python
from functools import lru_cache

def minScoreTriangulation_bruteforce(values):
    n = len(values)

    # 使用记忆化递归避免手动写 dp 表，但本质仍是暴力搜索
    @lru_cache(None)                     # 把已经算好的子问题记下来
    def dfs(l: int, r: int) -> int:
        """
        求解以 vertices[l] 为左端，vertices[r] 为右端的子多边形
        的最小三角化得分（不包括 l、r 本身所在的三角形）。
        当 r - l == 1 时，子多边形已经没有顶点可以再划分，得分为 0。
        """
        if r - l == 1:                    # 只剩两条边，无法形成三角形
            return 0

        best = float('inf')
        # 在 l 与 r 之间任选一个顶点 k 作为第三个点，构成三角形 (l, k, r)
        for k in range(l + 1, r):
            # 三角形本身的得分
            cur = values[l] * values[k] * values[r]
            # 加上左侧子多边形和右侧子多边形的最小得分
            total = cur + dfs(l, k) + dfs(k, r)
            best = min(best, total)       # 取最小

        return best

    # 整个多边形的左右端点是 0 与 n-1
    return dfs(0, n - 1)


# ---------- 示例 ----------
if __name__ == "__main__":
    print(minScoreTriangulation_bruteforce([1, 2, 3]))               # 6
    print(minScoreTriangulation_bruteforce([3, 7, 4, 5]))           # 144
    print(minScoreTriangulation_bruteforce([1, 3, 1, 4, 1, 5]))    # 13
```

> 代码里用了 `functools.lru_cache` 进行**记忆化**，这样可以把同一个子区间的结果复用，虽然仍然是指数级别的搜索，但对 `n ≤ 12` 这种极小规模已经够用了。真正的暴力（不记忆化）会更慢。

#### 复杂度

- **时间复杂度**：`O( n! )`（阶乘级）——因为每一次都要在 `l…r` 之间挑一个顶点，递归深度大约是 `n`，组合数呈阶乘增长。  
  > 大白话：想象把 `n` 条切口全都尝试一次，可能的切法会像排列组合一样爆炸，几乎不可能在电脑上跑完 `n=50` 的情况。  
- **空间复杂度**：`O(n)`——递归栈的深度最多 `n`，加上记忆化表（如果不使用 `lru_cache`）也只需要保存 `O(n²)` 个子区间的结果。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **“子区间划分”** 是核心：每一次都把一个多边形拆成左右两个更小的子多边形。  
**瓶颈** 在于：同样的子区间会被重复求解很多次。只要把“已经算好的子区间结果”保存下来，就能避免重复计算，这正是**动态规划（Dynamic Programming）**的思想。

**动态规划的状态定义**  
- `dp[l][r]`：表示顶点索引在 `[l, r]`（含）之间形成的**凸多边形**（注意 `r - l ≥ 2`）的最小三角化得分。  
- 当 `r - l == 2` 时，正好只能组成唯一的三角形，得分是 `values[l] * values[l+1] * values[r]`。  

**状态转移**  
对任意 `l < k < r`（`k` 为当前子多边形内部的第三个顶点），
```
dp[l][r] = min( dp[l][k] + dp[k][r] + values[l]*values[k]*values[r] )
```
- `dp[l][k]`：左侧子多边形的最小得分  
- `dp[k][r]`：右侧子多边形的最小得分  
- `values[l]*values[k]*values[r]`：当前根三角形的得分  

这正是把 **“根三角形 + 两侧子问题”** 的递归式写成表格形式。

**遍历顺序**  
因为 `dp[l][r]` 依赖于更小的区间 `dp[l][k]`、`dp[k][r]`，我们必须先算好**短区间**。  
常见做法是枚举区间长度 `len` 从 `3` 到 `n`，再枚举左端点 `l`，右端点 `r = l + len - 1`。

**类比**：把这个过程想成“拼图”。先把最小的两块拼好（长度为 3 的区间），再逐步拼更大的块，每次只需要看已经拼好的小块怎么组合。

#### 代码（Python）

```python
def minScoreTriangulation(values):
    """
    动态规划 O(n^3) 解法
    dp[l][r] 表示顶点 l~r 之间（含）形成的凸多边形的最小得分。
    """
    n = len(values)
    # 初始化二维 dp 表，全部设为正无穷（因为我们要取最小值）
    dp = [[float('inf')] * n for _ in range(n)]

    # 长度为 2（即只有两条边）时没有三角形，得分为 0
    for i in range(n):
        dp[i][i] = 0
        if i + 1 < n:
            dp[i][i + 1] = 0

    # 从最小的可以构成三角形的长度 3 开始枚举
    for length in range(3, n + 1):          # length = 子多边形的顶点数
        for l in range(0, n - length + 1):
            r = l + length - 1              # 子多边形的右端点
            # 枚举第三个顶点 k，把 (l, k, r) 当作根三角形
            for k in range(l + 1, r):
                # 当前三角形的得分 + 左子区间 + 右子区间
                cur = values[l] * values[k] * values[r] + dp[l][k] + dp[k][r]
                if cur < dp[l][r]:
                    dp[l][r] = cur          # 取最小

    # 整个多边形对应区间 [0, n-1]
    return dp[0][n - 1]


# ---------- 示例 ----------
if __name__ == "__main__":
    print(minScoreTriangulation([1, 2, 3]))               # 6
    print(minScoreTriangulation([3, 7, 4, 5]))           # 144
    print(minScoreTriangulation([1, 3, 1, 4, 1, 5]))    # 13
```

#### 复杂度

- **时间复杂度**：`O(n³)`  
  - 三层循环：外层遍历区间长度 `O(n)`，中层遍历左端点 `O(n)`，内层遍历分割点 `k` 也最多 `O(n)`。  
  - 大白话：想象我们把每一条可能的“切线”都尝试一次，最多会有 `50³ = 125,000` 次计算，电脑能在毫秒级完成。  
- **空间复杂度**：`O(n²)`  
  - 需要一个 `n × n` 的二维表来保存所有子区间的最小得分。对于 `n ≤ 50`，这只占几千个整数，几乎可以忽略不计。

---

## 心得

- **核心技巧**：**区间动态规划**——把大问题拆成左、右子区间的最优解，加上当前决定的代价。  
- **适用题型**（类似思路）  
  1. **矩阵链乘法**（LeetCode 312）  
  2. **戳气球**（LeetCode 312）  
  3. **最小删除回文**（LeetCode 1246）  
- **一句话总结解题钥匙**：**“把多边形看成一段连续的区间，枚举最后一个形成的三角形，利用子区间的最优解递推”。**

---

## 反思

- **第一反应**：看到“凸多边形”“三角化”就想到**递归枚举根三角形**，这自然导向了区间 DP。  
- **最容易踩的坑**  
  - 忘记对长度为 2（只有两条边）或长度为 3（恰好一个三角形）的区间进行初始化，导致 `dp` 中出现 `inf` 传播。  
  - 循环的边界写错：`k` 必须在 `(l, r)` 之间，不能取到 `l` 或 `r`。  
  - 题目要求 **凸** 多边形，保证任意选的三角形都是合法的；如果是非凸多边形，需要额外判断是否形成内部交叉。  
- **下次遇到同类题**：第一步立刻想到“**把整体看成区间，枚举最后一步（或最先做的那一步）**”，然后写出 DP 状态转移式，再确定遍历顺序。这样可以快速从暴力递归跳到 O(n³) 的高效解。