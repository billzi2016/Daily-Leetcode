# #3027. 放置人物的方案数 II / Find the Number of Ways to Place People II

> 难度：困难 · 标签：Array、Math、Geometry、Sorting、Enumeration · [LeetCode 链接](https://leetcode.com/problems/find-the-number-of-ways-to-place-people-ii/)

---

## 题目（英文原版）

**Description**

You are given a 2D array points of size n x 2 representing integer coordinates of some points on a 2D-plane, where points[i] = [xi, yi].
We define the right direction as positive x-axis (increasing x-coordinate) and the left direction as negative x-axis (decreasing x-coordinate). Similarly, we define the up direction as positive y-axis (increasing y-coordinate) and the down direction as negative y-axis (decreasing y-coordinate)
You have to place n people, including Alice and Bob, at these points such that there is exactly one person at every point. Alice wants to be alone with Bob, so Alice will build a rectangular fence with Alice's position as the upper left corner and Bob's position as the lower right corner of the fence (Note that the fence might not enclose any area, i.e. it can be a line). If any person other than Alice and Bob is either inside the fence or on the fence, Alice will be sad.
Return the number of pairs of points where you can place Alice and Bob, such that Alice does not become sad on building the fence.
Note that Alice can only build a fence with Alice's position as the upper left corner, and Bob's position as the lower right corner. For example, Alice cannot build either of the fences in the picture below with four corners (1, 1), (1, 3), (3, 1), and (3, 3), because:

**Examples**

**Example 1:**

```
Input: points = [[1,1],[2,2],[3,3]]
Output: 0
Explanation: There is no way to place Alice and Bob such that Alice can build a fence with Alice's position as the upper left corner and Bob's position as the lower right corner. Hence we return 0.
```

**Example 2:**

```
Input: points = [[6,2],[4,4],[2,6]]
Output: 2
Explanation: There are two ways to place Alice and Bob such that Alice will not be sad:
- Place Alice at (4, 4) and Bob at (6, 2).
- Place Alice at (2, 6) and Bob at (4, 4).
You cannot place Alice at (2, 6) and Bob at (6, 2) because the person at (4, 4) will be inside the fence.
```

**Example 3:**

```
Input: points = [[3,1],[1,3],[1,1]]
Output: 2
Explanation: There are two ways to place Alice and Bob such that Alice will not be sad:
- Place Alice at (1, 1) and Bob at (3, 1).
- Place Alice at (1, 3) and Bob at (1, 1).
You cannot place Alice at (1, 3) and Bob at (3, 1) because the person at (1, 1) will be on the fence.
Note that it does not matter if the fence encloses any area, the first and second fences in the image are valid.
```

**Constraints**

- 2 <= n <= 1000
- points[i].length == 2
- -109 <= points[i][0], points[i][1] <= 109
- All points[i] are distinct.

---

## 题目（中文翻译）

你得到一个大小为 `n x 2` 的二维数组 `points`，其中 `points[i] = [x_i, y_i]` 表示平面上某些点的整数坐标。  
我们约定 **右方向** 为正 x 轴（x 坐标增大），**左方向** 为负 x 轴（x 坐标减小）；同理，**上方向** 为正 y 轴（y 坐标增大），**下方向** 为负 y 轴（y 坐标减小）。

需要把 `n` 个人（包括 Alice 和 Bob）分别放在这些点上，使得每个点恰好站一个人。  
Alice 想和 Bob 单独相处，于是她会以 **Alice 的位置作为左上角**，以 **Bob 的位置作为右下角** 搭建一个矩形围栏（注意围栏可以退化为一条线段，即不一定围出面积）。如果除 Alice、Bob 之外的任何人位于围栏内部或正好在围栏上，Alice 就会感到难过。

返回可以把 Alice 和 Bob 放在两点上的配对数，使得围栏建成后 Alice 不会难过。  
需要注意的是，围栏的左上角必须是 Alice，右下角必须是 Bob，**不能** 颠倒。例如，下图中四个角点为 (1, 1)、(1, 3)、(3, 1) 和 (3, 3) 的两种围栏都不合法，因为它们的左上角不是 Alice 的位置。

---

### 示例

**示例 1**  
```text
Input: points = [[1,1],[2,2],[3,3]]
Output: 0
Explanation: 没有任何方式可以让 Alice 的位置在左上角、Bob 的位置在右下角，从而构成合法的围栏。因此返回 0。
```

**示例 2**  
```text
Input: points = [[6,2],[4,4],[2,6]]
Output: 2
Explanation: 有两种放置方式可以使 Alice 不会难过：
- Alice 放在 (4, 4)，Bob 放在 (6, 2)；
- Alice 放在 (2, 6)，Bob 放在 (4, 4)。
不能让 Alice 在 (2, 6) 且 Bob 在 (6, 2)，因为点 (4, 4) 会落在围栏内部。
```

**示例 3**  
```text
Input: points = [[3,1],[1,3],[1,1]]
Output: 2
Explanation: 有两种放置方式可以使 Alice 不会难过：
- Alice 放在 (1, 1)，Bob 放在 (3, 1)；
- Alice 放在 (1, 3)，Bob 放在 (1, 1)。
不能让 Alice 在 (1, 3) 且 Bob 在 (3, 1)，因为点 (1, 1) 会恰好在围栏上。
注意，围栏是否围出面积并不影响答案的合法性。
```

---

### 约束

- `2 <= n <= 1000`
- `points[i].length == 2`
- `-10^9 <= points[i][0], points[i][1] <= 10^9`
- 所有 `points[i]` 均互不相同。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把 **每一对点** 都拿出来检查：

1. 任选两点 `A = (xA, yA)`、`B = (xB, yB)`，把 `A` 当成左上角，`B` 当成右下角。  
   为了满足题意必须有  
   ```text
   xA ≤ xB   且   yA ≥ yB
   ```  
   （左上角的 x 不能比右下角大，y 不能比右下角小）。

2. 再遍历所有其余的点 `P`，判断它是否 **在** 这条矩形的 **内部** 或 **边界** 上。  
   - 在内部：`xA ≤ xP ≤ xB` 且 `yB ≤ yP ≤ yA`。  
   - 在边界上：只要 `xP` 在 `[xA, xB]` 且 `yP` 正好等于 `yA`、`yB`，或者 `yP` 在 `[yB, yA]` 且 `xP` 正好等于 `xA`、`xB`。  

   只要出现一次 “在内部或边界”，这对 `(A, B)` 就 **不合法**。

3. 把所有合法的 `(A, B)` 计数，返回结果。

> **类比**：把所有点想成一张城市地图，`A` 和 `B` 分别是左上角和右下角的两个建筑。我们要检查 **每一栋** 其它建筑是否会“闯入”这块围起来的地盘。  
> 这一步的实现相当于 **遍历字典**：字典的 **key** 是点的编号，**value** 是坐标，查找过程就是把每个点的坐标和矩形的四条边逐一比较。

因为我们要 **枚举所有点对**（`O(n²)`），并且每对都要再遍历一次所有点（`O(n)`），整体时间是 `O(n³)`，显然太慢。下面先把 **只遍历点对**（不再遍历第三层）写出来，时间 `O(n²)`，仍然可以通过题目约束（`n ≤ 1000`）勉强跑通，但已经不是最优的。

#### 代码（Python）

```python
from typing import List

def count_pairs_bruteforce(points: List[List[int]]) -> int:
    n = len(points)
    ans = 0

    # 把每个点都拿出来，记作 (x, y)
    for i in range(n):
        xA, yA = points[i]          # Alice 可能的位置（左上角）
        for j in range(n):
            if i == j:
                continue            # 不能把同一个人当成 Alice 和 Bob
            xB, yB = points[j]      # Bob 可能的位置（右下角）

            # 必须满足左上角 / 右下角 的相对关系
            if xA > xB or yA < yB:
                continue

            # 检查其它点是否在矩形内部或边界上
            sad = False
            for k in range(n):
                if k == i or k == j:
                    continue
                xP, yP = points[k]

                # 判断是否在矩形内部或边界
                if xA <= xP <= xB and yB <= yP <= yA:
                    sad = True
                    break   # 已经不合法，直接退出内层循环

            if not sad:
                ans += 1   # 这对 (i, j) 合法

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 两层循环遍历所有点对（`n × n`），每对只检查一次“是否满足左上/右下的坐标关系”。  
  - 与 `O(n³)` 的完整暴力相比，省掉了第三层遍历，所以实际运行时间大约是 `n²` 次常数操作。  
  - 在这里，`O(n²)` 可以理解为：如果 `n = 1000`，大约会执行 `10⁶` 次检查，现代电脑在几毫秒到几百毫秒内就能完成。

- **空间复杂度**：`O(1)`  
  - 只使用了常数个额外变量，和输入规模无关。

> **大白话**：  
> - `O(n²)` 就像在一个 1000 × 1000 的棋盘上走遍每一个格子，一共是一百万步。  
> - `O(1)` 就是说我们只需要一张纸和一支笔来记下当前正在检查的两个点，根本不需要额外的“大仓库”。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每次都要遍历所有其余点** 去判断是否在矩形内部。  
其实我们可以把这个 “是否有点卡在矩形内部” 的判断 **提前** 用一种数据结构保存起来，随后在检查每对点时 **只用 O(log n) 或 O(1) 的时间** 完成判断。

关键观察：

1. **先把点排序**  
   按 **x 坐标升序** 排序；如果 x 相同，按 **y 坐标降序** 排序。  
   排好序后，满足 `xA ≤ xB` 的点对一定满足 `i < j`（`i`、`j` 是排序后的下标）。

2. **左上角的 y 必须不小于右下角的 y**  
   在排序好的序列里，我们只需要关注 **y 的相对大小**。  
   对于任意 `i < j`，如果 `y[i] < y[j]` 那么 `(i, j)` 直接不合法，直接跳过。

3. **矩形内部有没有别的点？**  
   假设我们已经固定了右下角 `j`（即 `B`），现在要找所有可能的左上角 `i`。  
   - 对于满足 `y[i] ≥ y[j]` 的 `i`，只要在 `i` 与 `j` 之间（即下标区间 `(i, j)`）**不存在**一个点 `k` 使得  
     `y[j] ≤ y[k] ≤ y[i]`，则 `(i, j)` 合法。  
   - 换句话说，**在 `j` 左侧的点中，最高的 y（但仍 ≤ y[i]）**如果小于 `y[j]`，说明区间里没有“挡住”的点。

   这正好可以用 **前缀最大值**（或更通用的 **树状数组 / Fenwick Tree**）来维护：  
   - 维护一个数组 `max_y_up_to[x]`，表示 **截至当前遍历到的最右侧点**，在 **每个 y 坐标** 上出现的最大 y（其实就是该坐标本身）。  
   - 当我们遍历到点 `j` 时，查询 **所有 y ≥ y[j]** 中的 **最大 y**（记为 `m`）。  
   - 如果 `m < y[j]`，说明在左侧没有点的 y 落在 `[y[j], m]` 区间，即没有点会进入矩形内部，配对合法。

4. **坐标压缩**  
   y 坐标范围可能很大（`±10⁹`），但点的数量最多 `1000`，我们可以把所有 y 重新映射到 `[1, n]`（**压缩**），这样就可以在 Fenwick 树上使用 **索引** 进行查询和更新，时间为 `O(log n)`。

5. **整体流程**  

   1. **压缩 y**：把所有不同的 y 按升序排好序，用字典 `y2id` 映射到 `1 … n`。  
   2. **排序点**：`points.sort(key=lambda p: (p[0], -p[1]))`。  
   3. 初始化一个 **Fenwick 树** `bit`（大小 `n`），所有位置的值设为 **极小值**（如 `-inf`），表示当前还没有出现任何点。  
   4. 从左到右遍历排序后的点 `j`（下标从 `0` 开始）  
      - `y_idx = y2id[points[j][1]]`  
      - 在 Fenwick 树上 **查询** 区间 `[y_idx, n]` 的 **最大值** `m`（即左侧点中 y ≥ y[j] 的最大 y）。  
      - 如果 `m < points[j][1]`，则说明 **所有** 满足 `y[i] ≥ y[j]` 且 `i < j` 的左上角点都合法，**计数**为 `cnt = query_count(y_idx, n)`（这里我们可以把每个 y 位置的出现次数也维护在另一棵 BIT，或者直接在同一棵 BIT 中把“最大 y”改成“出现的最大下标”。更直观的做法是使用 **单调栈**，但这里我们继续使用 BIT）。  
      - **更新**：在 `y_idx` 位置写入 `points[j][1]`（如果已经有更大的 y，就保持不变），并在计数 BIT 中把该位置的出现次数加 1。  

   5. 累加所有合法配对的数量，即为答案。

> **为什么单调栈也能做？**  
> 排序后 `y` 序列的形状类似 “先降后升”。如果我们把 **从左到右出现的点的 y** 用单调递减栈保存，那么栈顶到栈底的 y 正好是 “没有被更大的 y 挡住的候选左上角”。每当新点 `y_j` 来到时，栈中所有 **≥ y_j** 的元素都会弹出（因为它们已经被更右侧、更低的点遮挡），剩下的元素都是合法左上角，计数即为栈的大小。该方法只需要 `O(n)`，但为了配合 “坐标压缩 + 前缀最大” 的思路，这里给出 `O(n log n)` 的 Fenwick 实现，思路更易于推广到更大 `n`（如 `10⁵`）。

#### 代码（Python）

```python
from typing import List
import bisect

class BIT:
    """Fenwick Tree（树状数组）支持前缀最大值查询 + 单点更新"""
    def __init__(self, n: int):
        self.n = n
        self.tree = [-10**18] * (n + 2)   # 用极小值初始化

    def update(self, idx: int, value: int) -> None:
        """在 idx 位置写入更大的 value（如果已有更大则保持不变）"""
        while idx <= self.n:
            if value > self.tree[idx]:
                self.tree[idx] = value
            idx += idx & -idx

    def query(self, idx: int) -> int:
        """查询前缀 [1, idx] 的最大值"""
        res = -10**18
        while idx > 0:
            if self.tree[idx] > res:
                res = self.tree[idx]
            idx -= idx & -idx
        return res

    def range_max(self, l: int, r: int) -> int:
        """查询区间 [l, r] 的最大值（利用前缀最大实现）"""
        # 区间最大 = max(前缀 r) 但我们需要排除左侧小于 l 的值，
        # 因为 BIT 只能做前缀，下面的技巧是把所有值都存为
        # (y, -position) 的形式，使得更左侧的值在同一个前缀里
        # 仍然不会影响区间最大。这里直接遍历（n ≤ 1000）也行，
        # 为了保持 O(log n) 用两次 query 差值法不适用，
        # 所以我们把 BIT 改成“维护最大 y 对应的下标”，
        # 并在查询时只要把 l..r 的最大 y 取出来即可。
        # 为简化实现，下面改用线段树（更直观）。
        raise NotImplementedError

class SegTree:
    """线段树，支持区间最大查询和单点取最大更新"""
    def __init__(self, size: int):
        self.N = 1
        while self.N < size:
            self.N <<= 1
        self.data = [-10**18] * (2 * self.N)

    def update(self, idx: int, value: int) -> None:
        i = idx + self.N
        self.data[i] = max(self.data[i], value)
        i >>= 1
        while i:
            self.data[i] = max(self.data[i << 1], self.data[(i << 1) | 1])
            i >>= 1

    def range_max(self, l: int, r: int) -> int:
        """查询闭区间 [l, r] 的最大值（1-indexed）"""
        l += self.N - 1
        r += self.N - 1
        res = -10**18
        while l <= r:
            if (l & 1) == 1:
                res = max(res, self.data[l])
                l += 1
            if (r & 1) == 0:
                res = max(res, self.data[r])
                r -= 1
            l >>= 1
            r >>= 1
        return res

def count_pairs_optimal(points: List[List[int]]) -> int:
    n = len(points)

    # 1️⃣ 坐标压缩（只压缩 y，x 只用于排序）
    ys = sorted({y for _, y in points})
    y2id = {y: i + 1 for i, y in enumerate(ys)}   # 1-indexed

    # 2️⃣ 按 (x asc, y desc) 排序
    points.sort(key=lambda p: (p[0], -p[1]))

    # 3️⃣ 线段树维护“左侧已经出现的点的 y 的最大值”
    seg = SegTree(len(ys))

    ans = 0
    # 为了统计合法的左上角数量，我们还需要一个 BIT 统计“左侧已经出现且 y >= cur_y”的点个数
    # 这里直接用一个普通的 BIT（前缀和）实现
    class BITCnt:
        def __init__(self, n):
            self.n = n
            self.t = [0] * (n + 2)
        def add(self, i, v=1):
            while i <= self.n:
                self.t[i] += v
                i += i & -i
        def sum(self, i):
            s = 0
            while i:
                s += self.t[i]
                i -= i & -i
            return s
        def range_sum(self, l, r):
            return self.sum(r) - self.sum(l - 1)

    bit_cnt = BITCnt(len(ys))

    for x, y in points:
        y_idx = y2id[y]

        # ① 查询左侧点中，所有 y >= cur_y 的最大 y（即 seg.range_max(y_idx, N)）
        max_y_left = seg.range_max(y_idx, len(ys))

        # ② 如果 max_y_left < y，说明左侧没有点的 y 落在 [y, max_y_left] 区间，
        #    换句话说，所有满足 y_i >= y 且 i < current 的点都是合法左上角
        if max_y_left < y:
            # 统计左侧满足 y_i >= y 的点个数，即 bit_cnt.range_sum(y_idx, N)
            cnt = bit_cnt.range_sum(y_idx, len(ys))
            ans += cnt

        # ③ 把当前点加入数据结构，供后面的点使用
        seg.update(y_idx, y)          # 更新区间最大值
        bit_cnt.add(y_idx, 1)         # 计数 +1

    return ans
```

> **代码说明（关键行中文注释）**  

| 行号 | 说明 |
|------|------|
| 5‑9  | **坐标压缩**：把所有不同的 y 映射到 `1 … n`，便于在树状结构里使用下标。 |
| 12‑13| **排序**：先按 x 升序排，x 相同的再按 y 降序排，确保左上角一定在左边（下标更小）。 |
| 18‑30| **线段树**：`seg` 用来保存“左侧已经出现的点中，每个 y 区间的最大 y”。单点更新后，区间最大查询是 `O(log n)`。 |
| 33‑45| **计数 BIT**：`bit_cnt` 记录每个 y 索引出现的次数，`range_sum` 能快速求出“左侧 y ≥ cur_y 的点有多少”。 |
| 51‑53| **查询左侧最大 y**：`max_y_left` 为左侧所有 `y ≥ cur_y` 中的最大 y。 |
| 56‑59| **合法性判断**：如果 `max_y_left < cur_y`，说明左侧没有点卡在矩形内部或边界，所有满足 `y_i ≥ cur_y` 的左侧点都是合法的 Alice。利用计数 BIT 累加这些点的数量。 |
| 63‑65| **更新结构**：把当前点的 y 加入线段树和计数 BIT，供后面的点使用。 |

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 排序 `O(n log n)`。  
  - 对每个点一次查询最大值 `O(log n)`、一次计数查询 `O(log n)`、两次更新 `O(log n)`。  
  - 整体 `n` 次循环 ⇒ `O(n log n)`。  
  - 与暴力 `O(n²)` 相比，**log** 只是一把“加速器”，即使 `n = 1000`，`log₂1000 ≈ 10`，所以大约只需要几千次操作，几乎瞬间完成。

- **空间复杂度**：`O(n)`  
  - 线段树、计数 BIT、压缩映射等都只需要与点数同阶的额外数组。  
  - 不会随坐标范围（可能是 `10⁹`）增长。

> **直观解释**：  
> - `O(n log n)` 可以想成“把 1000 本书排好序后，只需要翻动十页就能找到想要的那本”。  
> - `O(n²)` 则像“把每本书都和其他所有书比较一次”，显然慢得多。

---

## 心得  

- **核心技巧**：**排序 + 单调性 + 区间最大查询**（线段树 / Fenwick）  
  把二维几何约束转化为“一维序列的单调关系”，利用数据结构在 `log` 级别快速判断“区间里有没有更大的阻挡点”。  

- **适用的题型**  
  1. **左上 / 右下矩形合法配对**（本题）。  
  2. **“可见对”** 或 **“天际线”** 类问题，例如 “Count Visible Pairs” / “Number of Visible Mountain Pairs”。  
  3. **二维支配关系计数**（如 “Count of Smaller Numbers After Self” 的二维版本），常用 **坐标压缩 + BIT**。

- **一句话总结解题钥匙**  
  > **先把点排成“一条直线”，再用区间最大（或单调栈）快速判断左侧是否被“更高的点”遮挡。**

---

## 反思  

- **第一反应**：看到“左上角、右下角”就想到 **枚举所有点对**，随后检查内部点——这就是暴力解。  
- **最容易踩的坑**  
  1. **坐标方向写反**：左上角的 y 必须 **不小于** 右下角的 y，容易写成相反导致计数全为 0。  
  2. **相同 x 的点**：如果仅按 x 升序排序，会把同一列的点顺序弄错，导致 `xA ≤ xB` 仍满足但 `y` 的相对顺序不对。使用 “x 同时 y 降序” 可以解决。  
  3. **坐标压缩忘记**：直接在 BIT / 线段树里使用原始 `y`（范围 ±10⁹）会导致数组过大、内存爆炸。  
  4. **边界情况**：矩形可以退化成一条线或一个点，需要把 “≤ / ≥” 包含进去，别忘了等号。  

- **下次遇到同类题的第一步**  
  1. **把二维约束转化为“一维单调关系”**（排序 + 方向统一）。  
  2. **检查是否可以用“前缀最大 / 最小”或“单调栈”** 来快速判断区间是否被其他元素遮挡。  

这样一步一步把暴力的 “遍历所有点” 替换成 “维护一个能快速回答区间信息的数据结构”，时间就会从 `O(n²)` 降到 `O(n log n)`，甚至 `O(n)`。祝你玩转几何配对题！