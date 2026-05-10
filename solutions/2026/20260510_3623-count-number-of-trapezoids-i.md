# #3623. 计数水平梯形的数量 I / Count Number of Trapezoids I

> 难度：中等 · 标签：Array、Hash Table、Math、Geometry · [LeetCode 链接](https://leetcode.com/problems/count-number-of-trapezoids-i/)

---

## 题目（英文原版）

**Description**

You are given a 2D integer array points, where points[i] = [xi, yi] represents the coordinates of the ith point on the Cartesian plane.
A horizontal trapezoid is a convex quadrilateral with at least one pair of horizontal sides (i.e. parallel to the x-axis). Two lines are parallel if and only if they have the same slope.
Return the  number of unique horizontal trapezoids that can be formed by choosing any four distinct points from points.
Since the answer may be very large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: points = [[1,0],[2,0],[3,0],[2,2],[3,2]]
Output: 3
Explanation:

There are three distinct ways to pick four points that form a horizontal trapezoid:
```

**Example 2:**

```
Input: points = [[0,0],[1,0],[0,1],[2,1]]
Output: 1
Explanation:

There is only one horizontal trapezoid that can be formed.
```

**Constraints**

- 4 <= points.length <= 105
- –108 <= xi, yi <= 108
- All points are pairwise distinct.

---

## 题目（中文翻译）

给定一个二维整数数组 `points`，其中 `points[i] = [xi, yi]` 表示第 *i* 个点在笛卡尔平面上的坐标。  
**水平梯形**（horizontal trapezoid）是指至少有一对水平边（即平行于 x 轴）的凸四边形（convex quadrilateral）。两条直线平行当且仅当它们的斜率（slope）相同。  

返回可以从 `points` 中任意选择四个互不相同的点组成的 **唯一**（unique）水平梯形的数量。由于答案可能非常大，请返回其对 `10^9 + 7` 取模后的结果。

---

### 示例

**示例 1**  
```text
Input: points = [[1,0],[2,0],[3,0],[2,2],[3,2]]
Output: 3
Explanation:
有三种不同的方式选取四个点，使它们构成水平梯形：
```

**示例 2**  
```text
Input: points = [[0,0],[1,0],[0,1],[2,1]]
Output: 1
Explanation:
只能构成一种水平梯形。
```

---

### 约束条件

- `4 <= points.length <= 10^5`
- `-10^8 <= xi, yi <= 10^8`
- 所有点两两不同。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有点的四元组都枚举一遍**，检查这四个点能否组成一条水平梯形。  

- **枚举四个不同的下标** `i, j, k, l`（`i < j < k < l`），得到四个点 `p[i]、p[j]、p[k]、p[l]`。  
- 判断这四个点是否满足「至少有一对水平边」且「四点构成凸四边形」的条件。  
- 如果满足，就计数 +1。  

> **类比**：把点想象成一盒糖果，暴力解就是把糖果一个一个拿出来，尝试所有四个糖果的组合，看能否拼出想要的形状。显然，这种「尝遍所有可能」的办法在点很多的时候会非常慢。

**为什么正确**  
只要遍历了**所有**可能的四点组合，就不可能漏掉任何合法的梯形；每一次检查都是对题目条件的完整验证，所以计数一定是准确的。

**复杂度分析（大白话）**  

- 枚举四个下标相当于「从 `n` 个点里挑 4 个」的组合数，记作 `C(n,4) = n·(n‑1)·(n‑2)·(n‑3)/24`。  
- 当 `n = 10⁵`（题目最大规模）时，这个数字天文级别，根本算不完。  
- 因此时间复杂度是 **O(n⁴)**，也可以说「每增加一个点，运算量会乘上大约 `n`」——这在实际运行中几乎是不可能完成的。  
- 只用了常数级的额外存储，空间是 **O(1)**。

#### 代码（Python）

```python
from itertools import combinations
from typing import List

MOD = 10**9 + 7

def is_horizontal_trapezoid(pts: List[List[int]]) -> bool:
    """
    判断四个点是否能组成水平梯形
    1. 至少有一对点 y 相同（水平边）
    2. 四点不共线，且凸四边形
    这里直接用几何公式判断凸性（叉积同号），
    代码仅用于演示暴力思路，实际不会通过大数据。
    """
    # 先检查是否有两点在同一条水平线上
    ys = [y for _, y in pts]
    if len(set(ys)) == 4:          # 没有任何相同的 y，直接否定
        return False

    # 按 x 排序后检查四边形是否自交（简单做法）
    pts_sorted = sorted(pts, key=lambda p: (p[0], p[1]))
    # 计算相邻向量的叉积符号是否一致
    cross_sign = None
    for i in range(4):
        x1, y1 = pts_sorted[i]
        x2, y2 = pts_sorted[(i + 1) % 4]
        x3, y3 = pts_sorted[(i + 2) % 4]
        # 向量 (p_i -> p_{i+1}) × (p_{i+1} -> p_{i+2})
        cross = (x2 - x1) * (y3 - y2) - (y2 - y1) * (x3 - x2)
        if cross == 0:          # 共线，退化
            return False
        if cross_sign is None:
            cross_sign = cross > 0
        elif (cross > 0) != cross_sign:
            return False        # 叉积符号不同，说明凹形或自交
    return True

def brute_count(points: List[List[int]]) -> int:
    ans = 0
    for quad in combinations(points, 4):          # 枚举所有四元组
        if is_horizontal_trapezoid(list(quad)):
            ans = (ans + 1) % MOD
    return ans
```

> **注意**：上述代码仅作“暴力思路示例”。在 `n = 10⁵` 时根本跑不完，真正解题时必须换更快的算法。

#### 复杂度  

- **时间复杂度**：`O(n⁴)` —— 每多一个点，组合数会乘以约 `n`，极其庞大。  
- **空间复杂度**：`O(1)` —— 只用了常数级的临时变量。

---

### 2. 最优解  

#### 思路  

从暴力解可以看出，**真正耗时的地方是枚举所有四点组合**。我们需要找到一种只遍历 **一次** 点集合，就能直接算出答案的办法。

**关键观察**  

1. **水平边的定义**  
   - 水平边必须位于同一条水平直线，即所有点的 `y` 坐标相同。  
   - 把所有点按照 `y` 分组（把同一水平线上的点放进同一个盒子），这一步相当于把「点」先按照「哪条水平线」进行分类。  

2. **梯形的构造**  
   - 一条梯形有 **两条水平边**，分别位于 **两条不同的水平线**（`y` 不同）。  
   - 只要在第一条线选出任意两个点（形成下底），在第二条线再选任意两个点（形成上底），这四点必然能拼成一个水平梯形（四点互不重合，且四边形必然凸）。  
   - 因此，**每条水平线提供的“水平边”数量** = 该线点数的两两组合数 `C(cnt, 2)`。  

3. **组合计数**  
   - 对于两条不同的水平线 `L1、L2`，梯形的数量 = `C(cnt1, 2) * C(cnt2, 2)`（下底的选法 × 上底的选法）。  
   - 把所有不同的 `y` 组合起来求和即可得到答案。  

4. **如何高效求和**  
   - 设 `h_i = C(cnt_i, 2)` 为第 `i` 条水平线能够形成的水平边数。  
   - 所有梯形的总数 = ` Σ_{i<j} h_i * h_j`。  
   - 直接两层循环会是 `O(m²)`（`m` 为不同 `y` 的数量），仍然可能太慢（最坏 `m ≈ n`）。  
   - 利用前缀累加：遍历每条线时，保持已经遍历过的 `h` 的累计和 `pre_sum`。当前线贡献 `h_i * pre_sum`，随后把 `h_i` 加入 `pre_sum`。这样只需要 **一次遍历**，时间 `O(m)`。  

5. **取模**  
   - 题目要求答案对 `10⁹+7` 取模，所有乘法和加法都要在取模后进行，防止整数溢出。  

**核心数据结构**  

- **哈希表（字典）**：把 `y` 作为键，点的个数 `cnt` 作为值。  
  - 类比：把「字典」想成一本电话簿，`y` 是人名，`cnt` 是这位「人」拥有的「电话号码」数量。我们只需要快速查到每个 `y` 有多少点。  
- **整数变量**：累计和 `pre_sum`、答案 `ans`，均在取模后更新。  

**整体步骤**  

1. 用哈希表统计每个 `y` 上的点数 `cnt_y`。  
2. 对每个 `cnt_y` 计算 `h = cnt_y * (cnt_y - 1) // 2`（即 `C(cnt_y, 2)`），并在遍历的过程中累计答案：`ans += h * pre_sum`。  
3. 把当前 `h` 加入 `pre_sum`，继续遍历下一条水平线。  
4. 最后返回 `ans % MOD`。  

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

MOD = 10**9 + 7

def countHorizontalTrapezoids(points: List[List[int]]) -> int:
    """
    最优解：O(n) 时间 + O(m) 空间（m 为不同 y 的数量，最多不超过 n）
    """
    # 1. 统计每条水平线上有多少点
    cnt_by_y = defaultdict(int)          # 哈希表：y -> 该行点数
    for x, y in points:
        cnt_by_y[y] += 1

    ans = 0          # 最终答案
    pre_sum = 0      # 已经遍历过的水平边数之和（Σ h_j，j 为已处理的行）

    # 2. 遍历每条水平线（顺序无所谓，只要遍历一次）
    for cnt in cnt_by_y.values():
        if cnt < 2:          # 少于两个点，根本不能形成水平边，直接跳过
            continue
        # 本行能形成的水平边数量 h = C(cnt, 2)
        h = cnt * (cnt - 1) // 2
        h %= MOD             # 取模防止后面乘法溢出

        # 3. 与之前所有行配对，形成梯形
        ans = (ans + h * pre_sum) % MOD

        # 4. 把本行的 h 加入前缀和，供后面的行使用
        pre_sum = (pre_sum + h) % MOD

    return ans
```

> **代码说明（中文注释）**  
> - 第 5‑7 行：使用 `defaultdict(int)` 把所有点按照 `y` 分组，统计每组的大小。  
> - 第 13‑15 行：如果某条水平线只有 0、1 个点，根本不可能成为梯形的上下底，直接跳过。  
> - 第 18 行：`h = cnt * (cnt-1) // 2` 正是组合数 `C(cnt, 2)`，即从该行挑选两点的方式数。  
> - 第 22 行：`ans += h * pre_sum` —— 把当前行与所有已经遍历过的行配对，累加梯形数量。  
> - 第 26 行：更新前缀和，让后面的行能够看到当前行的 `h`。  

#### 复杂度  

- **时间复杂度**：`O(n)`（一次遍历所有点统计 `y`，再一次遍历不同的 `y`，总量不超过 `n`）。  
  - 与暴力的 `O(n⁴)` 相比，**快了几乎 `n³` 次方**，即使 `n = 10⁵` 也能在毫秒级完成。  
- **空间复杂度**：`O(m)`，其中 `m` 为不同的 `y` 值数量（最坏情况 `m = n`），即哈希表存储每条水平线的计数。  
  - 这相当于只需要保存每条水平线的点数，远比保存所有四点组合要省内存。

---

## 心得  

- **核心技巧**：把「水平梯形」抽象为「两条不同水平线各取两个点」的组合问题，利用**分组计数 + 组合数学**快速求和。  
- **适用的题型**  
  1. **统计满足某种“同属性两两组合”再配对的结构**（如「平行四边形计数」）。  
  2. **需要先按某个属性分组，再在组间做配对」的题目（如「统计矩形数量」）。  
- **一句话总结**：**先把点按 y 分组，计算每组的两点组合数 `C(cnt,2)`，再用前缀和把所有组两两配对，答案即为这些组合数的两两乘积之和**。

---

## 反思  

- **第一反应**：看到「水平梯形」立刻想到「先找水平边」——这一步把几何约束转化为「相同 y」的等价条件。  
- **最容易踩的坑**  
  1. **忘记去重**：同一条水平线上的点必须两两不同，使用组合数 `C(cnt,2)` 自动处理。  
  2. **溢出**：`cnt` 可能很大，直接相乘会超出 64 位整数范围，必须在每一步都对 `10⁹+7` 取模。  
  3. **边界情况**：某条水平线点数少于 2 时不能贡献任何水平边，需提前过滤。  
- **下次遇到同类题**：第一步先 **“按关键属性（如坐标、颜色、数值）分组”，再在每组内部计数，最后把组间的计数用组合公式或前缀和快速配对**。这样可以把原本指数级的枚举压缩到线性时间。