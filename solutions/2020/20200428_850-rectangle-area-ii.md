# #850. **矩形面积 II** / Rectangle Area II

> 难度：困难 · 标签：Array、Segment Tree、Line Sweep、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/rectangle-area-ii/)

---

## 题目（英文原版）

**Description**

You are given a 2D array of axis-aligned rectangles. Each rectangle[i] = [xi1, yi1, xi2, yi2] denotes the ith rectangle where (xi1, yi1) are the coordinates of the bottom-left corner, and (xi2, yi2) are the coordinates of the top-right corner.
Calculate the total area covered by all rectangles in the plane. Any area covered by two or more rectangles should only be counted once.
Return the total area. Since the answer may be too large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: rectangles = [[0,0,2,2],[1,0,2,3],[1,0,3,1]]
Output: 6
Explanation: A total area of 6 is covered by all three rectangles, as illustrated in the picture.
From (1,1) to (2,2), the green and red rectangles overlap.
From (1,0) to (2,3), all three rectangles overlap.
```

**Example 2:**

```
Input: rectangles = [[0,0,1000000000,1000000000]]
Output: 49
Explanation: The answer is 1018 modulo (109 + 7), which is 49.
```

**Constraints**

- 1 <= rectangles.length <= 200
- rectanges[i].length == 4
- 0 <= xi1, yi1, xi2, yi2 <= 109
- xi1 <= xi2
- yi1 <= yi2
- All rectangles have non zero area.

---

## 题目（中文翻译）

给定一个二维数组，其中每个元素表示一个轴对齐矩形。`rectangles[i] = [xi1, yi1, xi2, yi2]` 表示第 *i* 个矩形，其中 `(xi1, yi1)` 为左下角坐标，`(xi2, yi2)` 为右上角坐标。

计算平面上所有矩形覆盖的总面积。若同一面积被两个或多个矩形覆盖，只计一次。

返回总面积。由于答案可能非常大，返回结果对 **10^9 + 7** 取模。

**示例 1**

```text
Input: rectangles = [[0,0,2,2],[1,0,2,3],[1,0,3,1]]
Output: 6
Explanation: 三个矩形覆盖的总面积为 6，如图所示。
从 (1,1) 到 (2,2) 的区域，绿色矩形和红色矩形重叠。
从 (1,0) 到 (2,3) 的区域，三个矩形全部重叠。
```

**示例 2**

```text
Input: rectangles = [[0,0,1000000000,1000000000]]
Output: 49
Explanation: 答案为 10^18，对 (10^9 + 7) 取模后得到 49。
```

**约束条件**

- `1 <= rectangles.length <= 200`
- `rectangles[i].length == 4`
- `0 <= xi1, yi1, xi2, yi2 <= 10^9`
- `xi1 <= xi2`
- `yi1 <= yi2`
- 所有矩形的面积均非零。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把平面离散成很多“小格子”，然后把每个格子看成一个“像素”。只要有任意一个矩形覆盖了这个格子，就把它记为已占用，最后把所有已占用格子的面积加起来即可。

> **类比**：把坐标轴想象成一本笔记本的横竖线格子。我们把所有出现过的横坐标和纵坐标记下来，形成若干条竖线和若干条横线，这样就把平面划分成若干个“小矩形格子”。每个格子就像笔记本里的一格格子，判断它是否被涂色（被矩形覆盖）非常直观。

实现步骤：

1. 收集所有矩形的左、右 x 坐标以及下、上 y 坐标，去重并排序。设得到的横坐标序列为 `xs`，纵坐标序列为 `ys`。因为最多有 `200` 个矩形，每条坐标最多出现 `400` 次，所以 `len(xs) ≤ 400`，`len(ys) ≤ 400`。
2. 建立一个二维布尔数组 `covered[i][j]`，表示横坐标区间 `[xs[i], xs[i+1])` 与纵坐标区间 `[ys[j], ys[j+1])` 这块小矩形是否被至少一个输入矩形覆盖。
3. 对每个输入矩形 `[x1, y1, x2, y2]`，找出它在 `xs`、`ys` 中对应的下标范围，然后把对应的 `covered` 区块全部置为 `True`。
4. 最后遍历 `covered`，对每个被标记的格子累加面积  
   `area += (xs[i+1] - xs[i]) * (ys[j+1] - ys[j])`。

**为什么正确**：离散化后每个格子恰好对应原平面上的一个不相交的小矩形区域。若该格子被任意矩形覆盖，则它的全部面积都应该计入总和；若没有覆盖，则不计入。遍历所有格子即完成了对 **并集面积** 的统计。

**复杂度分析**  

- `xs`、`ys` 长度均 ≤ 400，二维数组大小约为 `400 × 400 = 1.6e5`。  
- 对每个矩形我们要遍历它对应的格子，最坏情况是遍历全部格子一次，时间复杂度约为 `O(N * M²)`，这里 `M ≤ 400`，所以实际运行时间在几万次量级，完全可以接受。  
- 空间上需要存放 `covered`，即 `O(M²)`，约几百 KB。

> **大白话解释**：  
> - `O(N·M²)` 中的 `N` 是矩形的个数，`M` 是离散后坐标的种类数（最多 400）。如果把 `N` 想成“有多少只小狗”，`M²` 想成“地上有多少块草地”，我们要把每只小狗跑过的每块草地都检查一遍，所以时间是“狗数 × 草地数”。  
> - `O(M²)` 的空间就相当于我们在地上铺了一层草垫，记录每块草地是否被踩过。

#### 代码（Python）

```python
MOD = 10**9 + 7

def rectangleArea(rectangles):
    # 1️⃣ 收集所有不同的 x、y 坐标并排序
    xs = sorted({x for r in rectangles for x in (r[0], r[2])})
    ys = sorted({y for r in rectangles for y in (r[1], r[3])})

    # 2️⃣ 建立坐标到下标的映射，方便后面快速定位区间
    x_id = {x: i for i, x in enumerate(xs)}
    y_id = {y: i for i, y in enumerate(ys)}

    # 3️⃣ 用二维布尔数组记录每个小格子是否被覆盖
    covered = [[False] * (len(ys) - 1) for _ in range(len(xs) - 1)]

    # 4️⃣ 把每个矩形对应的格子全部标记为 True
    for x1, y1, x2, y2 in rectangles:
        # 在离散化后的坐标轴上找出对应的下标范围
        for i in range(x_id[x1], x_id[x2]):          # 横向区间
            for j in range(y_id[y1], y_id[y2]):      # 纵向区间
                covered[i][j] = True

    # 5️⃣ 累加所有被标记格子的面积
    area = 0
    for i in range(len(xs) - 1):
        dx = xs[i + 1] - xs[i]          # 该列格子的宽度
        for j in range(len(ys) - 1):
            if covered[i][j]:
                dy = ys[j + 1] - ys[j]  # 该行格子的高度
                area = (area + dx * dy) % MOD

    return area
```

#### 复杂度

- **时间复杂度**：`O(N * M²)`，其中 `N ≤ 200` 为矩形个数，`M ≤ 400` 为离散坐标数。直观上相当于“对每只小狗检查每块草地”。
- **空间复杂度**：`O(M²)`，用来存储格子是否被覆盖的二维布尔表。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**对每个格子都要遍历一次**，当坐标范围很大（可达 `10⁹`）时即使离散化后格子数也会比较多，且实现上需要 `O(M²)` 的额外空间。我们可以把“遍历所有格子”这一步**合并到一次扫描中**，只在 **x 方向上** 按顺序扫过去，同时维护 **当前所有活跃矩形在 y 方向上的并集长度**。这样我们只在每个相邻的 x 之间计算一次面积，而不必逐格子累加。

这就是经典的 **线段树 + 扫描线（Line Sweep）** 思路，核心步骤如下：

1. **离散化 y 坐标**  
   与暴力解相同，只收集所有矩形的 `y1`、`y2`，排序去重得到 `ys`。离散化的目的是把连续的 y 区间映射到线段树的节点上，使得每个节点对应一个固定的长度 `ys[r+1] - ys[l]`。

2. **把矩形转化为事件**  
   对每个矩形 `[x1, y1, x2, y2]`，在 `x = x1` 处产生一个 **进入事件**（type = +1），在 `x = x2` 处产生一个 **离开事件**（type = -1）。事件结构为 `(x, type, y1, y2)`。把所有事件按 `x` 从小到大排序。

3. **线段树维护 y 方向的覆盖长度**  
   - 每个线段树节点保存两个信息：  
     * `count`：当前区间被多少个矩形完整覆盖（懒记数），即覆盖计数。  
     * `cover_len`：**实际被覆盖的长度**。如果 `count > 0`，说明整个区间被至少一个矩形覆盖，`cover_len = ys[r+1] - ys[l]`；否则 `cover_len = left_child.cover_len + right_child.cover_len`（即从子区间合并）。
   - 当处理一个事件时，对对应的 `[y1, y2)` 区间在树上执行 **区间加/减**（`type` 为 +1 或 -1），随后根节点的 `cover_len` 就是**当前所有活跃矩形在 y 方向的并集长度**。

4. **计算面积**  
   扫描完第 `i` 条事件后，记 `cur_x = events[i].x`，`next_x = events[i+1].x`（若已是最后一条事件则 `next_x = cur_x`）。在两条相邻事件之间，`x` 坐标保持不变，`y` 方向的覆盖长度为根节点的 `cover_len`。于是这段宽度为 `dx = next_x - cur_x` 的竖条面积为 `dx * cover_len`。把它累加到答案中。

5. **取模**  
   题目要求对 `10⁹+7` 取模，累计时随时 `% MOD` 即可。

**关键概念解释**  

- **扫描线**：把平面看成一条会从左到右（或从下到上）移动的“扫把”。每当扫到矩形的左边缘时把它加入“活跃集合”，扫到右边缘时把它移出。只要维护活跃集合在垂直方向的投影长度，就能算出每段水平位移对应的面积。  
- **线段树（Segment Tree）**：想象把 y 轴切成很多段，每段长度固定（由离散化得到）。线段树是一棵二叉树，树的每个节点负责一段连续的 y 区间。它可以在 **对数时间** 完成区间的“加1/减1”操作，并且快速返回整条轴上被覆盖的总长度。  
- **懒记数（Lazy Count）**：我们不需要在每一次加减时把整个区间的每个小格子都去更新，只要记录该区间被覆盖的次数（`count`），当 `count>0` 时整段都算作被覆盖，省下大量的递归。

#### 代码（Python）

```python
MOD = 10**9 + 7

class SegmentTree:
    """线段树，只维护区间覆盖计数和覆盖长度"""
    def __init__(self, ys):
        self.ys = ys                # 离散化后的 y 坐标列表
        self.n = len(ys) - 1        # 实际区间个数（相邻坐标构成的区间）
        # 下面的数组大小取 4*n 足够容纳完整的二叉树
        self.count = [0] * (4 * self.n)      # 区间被完整覆盖的次数
        self.cover_len = [0] * (4 * self.n)  # 区间实际被覆盖的长度

    def _update(self, node, l, r, ql, qr, val):
        """在区间 [ql,qr) 上加/减 val（+1 入，-1 出）"""
        if ql >= r or qr <= l:          # 完全不相交
            return
        if ql <= l and r <= qr:         # 完全覆盖
            self.count[node] += val
        else:                           # 部分覆盖，继续向下递归
            mid = (l + r) // 2
            self._update(node*2, l, mid, ql, qr, val)
            self._update(node*2+1, mid, r, ql, qr, val)

        # 根据 count 决定当前节点的 cover_len
        if self.count[node] > 0:
            # 只要计数大于 0，整段区间必被覆盖
            self.cover_len[node] = self.ys[r] - self.ys[l]
        else:
            # 否则从子节点合并（叶子节点时子节点不存在，长度为 0）
            if r - l == 1:   # 叶子区间
                self.cover_len[node] = 0
            else:
                self.cover_len[node] = self.cover_len[node*2] + self.cover_len[node*2+1]

    def update(self, y1, y2, val):
        """外部调用的简化接口，y1、y2 为原始坐标"""
        l = self._idx(y1)
        r = self._idx(y2)
        self._update(1, 0, self.n, l, r, val)

    def _idx(self, y):
        """把原始 y 坐标转换为离散化后的下标"""
        # 因为 ys 已经排好序，使用二分查找
        import bisect
        return bisect.bisect_left(self.ys, y)

    def query(self):
        """根节点的 cover_len 即为当前所有活跃矩形在 y 方向的并集长度"""
        return self.cover_len[1]

def rectangleArea(rectangles):
    # 1️⃣ 离散化所有 y 坐标
    ys = sorted({y for r in rectangles for y in (r[1], r[3])})
    st = SegmentTree(ys)

    # 2️⃣ 生成事件 (x, type, y1, y2)
    events = []
    for x1, y1, x2, y2 in rectangles:
        events.append((x1, 1, y1, y2))   # 矩形左边进入
        events.append((x2, -1, y1, y2))  # 矩形右边离开
    events.sort(key=lambda e: e[0])    # 按 x 坐标升序

    ans = 0
    prev_x = events[0][0]

    # 3️⃣ 扫描线遍历所有事件
    for x, typ, y1, y2 in events:
        dx = x - prev_x                     # 与上一次 x 的水平距离
        covered_y = st.query()              # 当前 y 方向被覆盖的总长度
        ans = (ans + dx * covered_y) % MOD   # 累加这段宽度对应的面积

        # 更新线段树，使得后面的区间能得到正确的 y 覆盖长度
        st.update(y1, y2, typ)

        prev_x = x

    return ans
```

> **代码要点注释**  
> - `ys` 是离散化后的 y 列表，`st.ys[r] - st.ys[l]` 正好是节点对应区间的真实长度。  
> - `update` 中的 `val` 为 `+1`（进入）或 `-1`（离开），通过 `count` 记录该区间被多少个矩形“套住”。  
> - `query` 直接返回根节点的 `cover_len`，即当前所有活跃矩形在 y 方向的并集长度。  

#### 复杂度

- **时间复杂度**：`O(N log N)`  
  - 生成并排序事件需要 `O(N log N)`（`N` 为矩形个数，最多 200）。  
  - 每个事件对应一次线段树的区间更新，更新的时间是 `O(log M)`，其中 `M` 为离散化后 y 坐标的数量（ ≤ 400），所以整体仍是 `O(N log N)`。相比暴力的 `O(N·M²)`，快了好几个数量级。  
  - 大白话：我们只在“左/右边缘”这 2N 次关键位置动手，而不是每块草地都检查一次。

- **空间复杂度**：`O(M)`  
  - 线段树只需要存储 `4·(M-1)` 个节点的计数和长度，`M ≤ 400`，所以几千个整数的空间即可。相较于暴力的 `O(M²)`（二维数组），省了大量内存。

---

## 心得

- **核心技巧**：**扫描线 + 线段树（或区间计数）**，用于求平面上大量轴对齐矩形的并集面积。  
- **适用场景**：  
  1. 多矩形/多线段求并集面积或周长（如 LeetCode 850、735）。  
  2. 计算平面上点的覆盖次数、求最大重叠区间（如会议室安排）。  
  3. 任何需要在二维平面上快速统计 **垂直投影长度** 的问题。  
- **一句话总结解题钥匙**：**把二维问题转化为“一维覆盖长度随 x 变化的积分”，用线段树在 O(log N) 内维护这条“一维长度”。**

---

## 反思

- **第一反应**：看到“求所有矩形并集面积”，自然想到“把平面切成小格子”——即离散化暴力法。  
- **最容易踩的坑**：  
  1. **坐标离散化的闭区间/开区间**：事件区间必须使用左闭右开 `[y1, y2)`，否则会出现重复计数。  
  2. **取模时的负数**：更新后 `ans` 可能出现负数，需要在最终返回前 `(ans + MOD) % MOD`。  
  3. **边界条件**：当所有矩形在同一条竖线或横线上时，`dx` 为 0，不能忘记仍要更新线段树，否则后续 `cover_len` 会错误。  
- **下次类似题的第一步**：**先把所有横向（或纵向）边界抽出来做事件排序**，明确“什么时候加入、什么时候移除”，再思考用哪种“一维结构”来维护当前的覆盖长度（线段树、树状数组、或有序集合）。这样就能快速从暴力想到最优解。