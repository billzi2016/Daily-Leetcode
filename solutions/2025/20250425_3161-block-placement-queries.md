# #3161. 方块放置查询 / Block Placement Queries

> 难度：困难 · 标签：Array、Binary Search、Binary Indexed Tree、Segment Tree · [LeetCode 链接](https://leetcode.com/problems/block-placement-queries/)

---

## 题目（英文原版）

**Description**

There exists an infinite number line, with its origin at 0 and extending towards the positive x-axis.
You are given a 2D array queries, which contains two types of queries:
Return a boolean array results, where results[i] is true if you can place the block specified in the ith query of type 2, and false otherwise.

**Examples**

**Example 1:**

```
Input: queries = [[1,2],[2,3,3],[2,3,1],[2,2,2]]
Output: [false,true,true]
Explanation:

For query 0, place an obstacle at x = 2 . A block of size at most 2 can be placed before x = 3 .
```

**Example 2:**

```
Input: queries = [[1,7],[2,7,6],[1,2],[2,7,5],[2,7,6]]
Output: [true,true,false]
Explanation:
```

**Constraints**

- 1 <= queries.length <= 15 * 104
- 2 <= queries[i].length <= 3
- 1 <= queries[i][0] <= 2
- 1 <= x, sz <= min(5 * 104, 3 * queries.length)
- The input is generated such that for queries of type 1, no obstacle exists at distance x when the query is asked.
- The input is generated such that there is at least one query of type 2.

---

## 题目（中文翻译）

存在一条无限的数轴，原点在 `0`，向正 `x` 轴方向无限延伸。  
给定一个二维数组 `queries`，其中每个子数组表示一种查询，查询类型如下：

* **类型 1**：`[1, x]` —— 在位置 `x` 处放置一个障碍物（obstacle）。  
  题目保证在执行该查询时，位置 `x` 上不存在障碍物。

* **类型 2**：`[2, x, sz]` —— 判断是否能够放置一个长度**至多**为 `sz` 的方块（block），使得该方块的右端点不超过 `x`，且不与已放置的任何障碍物相交。  
  如果可以放置，则对应的结果为 `true`；否则为 `false`。

返回一个布尔数组 `results`，其中 `results[i]` 表示第 `i` 个 **类型 2** 查询的答案（`true` 表示可以放置，`false` 表示不能放置）。

---

### 示例

**示例 1**

```text
Input: queries = [[1,2],[2,3,3],[2,3,1],[2,2,2]]
Output: [false,true,true]
Explanation:
对于查询 0，在 x = 2 处放置一个障碍物。此时长度至多为 2 的方块可以放在 x = 3 之前。
查询 1 检查是否能在右端点 ≤ 3、长度 ≤ 3 的条件下放置方块，答案为 false（因为障碍物阻挡）。
查询 2 检查长度 ≤ 1 的方块，答案为 true。
查询 3 检查长度 ≤ 2、右端点 ≤ 2 的方块，答案为 true。
```

**示例 2**

```text
Input: queries = [[1,7],[2,7,6],[1,2],[2,7,5],[2,7,6]]
Output: [true,true,false]
Explanation:
- 第 0 条查询在 x = 7 放置障碍物。
- 第 1 条查询询问能否在右端点 ≤ 7、长度 ≤ 6 的条件下放置方块，答案为 true。
- 第 2 条查询在 x = 2 放置障碍物。
- 第 3 条查询检查长度 ≤ 5 的方块，答案为 true。
- 第 4 条查询检查长度 ≤ 6 的方块，答案为 false（已被两个障碍物限制）。
```

---

### 约束条件

- `1 <= queries.length <= 15 * 10^4`
- `2 <= queries[i].length <= 3`
- `1 <= queries[i][0] <= 2`
- `1 <= x, sz <= min(5 * 10^4, 3 * queries.length)`
- 输入保证对于所有类型 1 的查询，在执行时位置 `x` 上没有障碍物。
- 输入保证至少存在一条类型 2 的查询。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

- **数据结构**：我们直接用一个 Python `set` 来记下已经放好的障碍物位置。  
  - `set` 可以类比成**字典**，就像查字典时把“单词”当作 `key`，对应的“解释”当作 `value`，这里 `key` 是障碍物的坐标，`value`（这里不需要）可以想成“在这儿有障碍”。  
- **做法**：  
  1. 遇到类型 `1` 的查询，只要把坐标 `x` 加进 `set` 即可。  
  2. 遇到类型 `2` 的查询 `(x, sz)`，我们要判断 **是否存在** 一个左端点 `l`（`0 ≤ l ≤ x‑sz`），使得区间 `[l, l+sz]` 内没有任何障碍物。  
     - 最直接的办法是把所有可能的 `l` 从 `0` 枚举到 `x‑sz`，每枚举一次就检查区间 `[l, l+sz]` 是否和 `set` 有交集。  
     - 检查交集的方式是把 `l … l+sz` 里每一个坐标都在 `set` 中查找一次，只要发现一个在 `set` 里的坐标就说明这条线段被阻塞，继续下一个 `l`。  
- **为什么正确**：我们把**所有**可能的起始位置都遍历了一遍，只要有一条合法的线段就会返回 `True`，没有就返回 `False`。遍历完整个搜索空间自然是正确的。

#### 代码（Python）

```python
def blockPlacement(queries):
    obstacles = set()          # 记录已经放好的障碍物
    ans = []                   # type‑2 查询的返回结果

    for q in queries:
        if q[0] == 1:          # 类型 1：放障碍物
            _, x = q
            obstacles.add(x)   # 把坐标加入集合
        else:                  # 类型 2：能否放块
            _, x, sz = q
            can = False
            # 枚举所有可能的左端点 l
            for l in range(0, x - sz + 1):
                # 检查区间 [l, l+sz] 是否被障碍物占用
                blocked = False
                for p in range(l, l + sz + 1):
                    if p in obstacles:   # “查字典”，O(1) 时间
                        blocked = True
                        break           # 这条线段不行，直接尝试下一个 l
                if not blocked:           # 找到一条完全没有障碍的线段
                    can = True
                    break
            ans.append(can)

    return ans
```

> **关键行注释**  
> - `obstacles = set()`  # 像查字典一样，`in` 操作是 O(1)  
> - `for l in range(0, x - sz + 1):` # 暴力枚举所有左端点  
> - `if p in obstacles:` # 判断该坐标是否已经有障碍  

#### 复杂度

- **时间复杂度**：  
  - 类型 1 查询是 O(1)。  
  - 类型 2 查询最坏要遍历 `x‑sz+1` 个左端点，每个左端点再检查 `sz+1` 个坐标。于是单次查询的时间是 **O((x‑sz)·sz)**，在最坏情况下（`x≈5·10⁴`、`sz≈x/2`）会接近 **O(10⁹)**，远远超过题目限制。  
  - 用大白话说，`O(n²)` 就像“把 1000 张纸两两对比”，会产生 **100 万** 次比较，明显太慢。

- **空间复杂度**：  
  - 只用了一个 `set` 来保存障碍物，最多会存 `queries` 中所有类型 1 的坐标，大小为 **O(n)**（`n` 为查询数），即线性空间。

> 暴力解虽然最直观，但在数据量达到 10⁵ ~ 10⁶ 级别时会“卡死”，所以我们需要更聪明的办法。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于我们每次都要遍历所有可能的左端点 `l` 并检查每个坐标是否有障碍。  
实际上我们只关心每个位置 `i` 到**下一个障碍物**的距离：

```
d[i] = (最近的障碍物坐标) - i
```

- 如果 `d[i] > sz`，说明从 `i` 开始往右走 `sz` 步仍然没有碰到障碍，`[i, i+sz]` 可以放块。  
- 对于查询 `(x, sz)`，只要在区间 `[0, x‑sz]` 里存在 **一个** `d[i] > sz`，答案就是 `True`。

所以我们只需要：

1. **维护数组 `d`**，支持两种操作  
   - **更新**：当在位置 `p` 放置障碍物时，所有左侧位置 `i`（直到前一个障碍物）到下一个障碍的距离会变小，具体来说 `d[i] = min(d[i], p‑i)`。这是一种 **区间取最小**（`chmin`）操作。  
   - **查询**：对区间 `[0, x‑sz]` 求 **最大值** `max(d[i])`，判断它是否大于 `sz`。  

2. **数据结构**：我们需要一种能同时处理 “区间取最小” 与 “区间最大查询” 的结构。  
   - 这正是 **Segment Tree Beats**（线段树的高级技巧）能做到的：  
     - 每个节点维护区间的 **最大值**、**第二大值**、**最大值出现的次数**，以及 **懒标记** 用来做 `chmin`。  
     - 当我们对某个区间执行 `chmin(v)` 时，只要该区间的当前最大值已经 ≤ v，就不需要再往下传递；否则把超过 `v` 的部分降到 `v`，并更新节点信息。  
   - 这样每次更新和查询的 **摊销时间** 都是 `O(log N)`，`N` 为坐标上限（题目给出 `5·10⁴`），足够快。

下面用更直白的方式把 **Segment Tree Beats** 的核心思想解释给初学者：

- **普通线段树** 能把区间分成若干段，每段保存 **一个聚合信息**（比如最大值），查询时把对应的段合并即可。  
- **懒标记** 就像在段上贴了张 “以后再处理” 的便签，等真正需要时一次性下推，避免重复工作。  
- **区间取最小（chmin）** 其实是 “把这段里的所有数，和一个阈值 `v` 比较，超过 `v` 的全部变成 `v`”。  
  - 想象你有一排盒子里装了不同高度的水，`chmin(v)` 就是把所有高于 `v` 的盒子里的水倒掉，只剩 `v` 高。  
- 为了快速判断哪些盒子需要倒水，我们在每个节点记录 **最大高度**（`mx`）和 **第二大高度**（`se`）。如果 `mx ≤ v`，说明这段里没有水高于 `v`，直接跳过；如果 `se < v < mx`，说明只有最大值需要被降到 `v`，我们只改 `mx`，不必继续向下递归。这样就把原本可能遍历所有叶子的操作压缩到了 `log` 级别。

**步骤概览**

| 步骤 | 说明 |
|------|------|
| 初始化 | 把 `d[i]` 设为一个非常大的数（比如 `INF`），因为一开始没有障碍物，距离是无限远。 |
| 类型 1 查询 `(1, p)` | 1️⃣ 把位置 `p` 本身的 `d[p] = 0`（障碍物到自身的距离为 0）。<br>2️⃣ 对左侧区间 `[prev+1, p-1]`（`prev` 为 `p` 左边最近的障碍）执行 `chmin(p‑i)`，即 `range_chmin(prev+1, p, p)`。 |
| 类型 2 查询 `(2, x, sz)` | 计算 `right = x - sz`（左端点最大能取到的位置）。<br>在区间 `[0, right]` 取 **最大值** `mx = range_max(0, right)`。<br>如果 `mx > sz` → `True`，否则 `False`。 |

> **为什么只需要维护 `d` 而不必记录每个障碍的具体位置？**  
> 因为 `d[i]` 已经蕴含了“从 `i` 往右第一个障碍在哪里”。当我们在 `p` 处新增障碍时，只需要把左侧所有点的距离更新为更小的值即可，原来的障碍信息会自然被覆盖。

#### 代码（Python）

```python
import sys
sys.setrecursionlimit(1 << 25)

INF = 10 ** 9          # 足够大的“无限远”

class SegTree:
    """线段树（Segment Tree Beats）支持区间 chmin 与区间 max 查询"""
    def __init__(self, n):
        self.n = n
        size = 4 * n
        self.mx = [INF] * size      # 区间最大值
        self.se = [-INF] * size     # 区间第二大值
        self.cnt = [0] * size       # 最大值出现次数
        self.tag = [INF] * size     # 懒标记：用于 chmin，初始为 INF（表示“不做任何限制”）
        self._build(1, 0, n - 1)

    def _build(self, o, l, r):
        """初始化，每个叶子对应一个位置的 d[i] = INF"""
        if l == r:
            self.mx[o] = INF
            self.se[o] = -INF
            self.cnt[o] = 1
            return
        m = (l + r) // 2
        self._build(o << 1, l, m)
        self._build(o << 1 | 1, m + 1, r)
        self._push_up(o)

    # ---------- 合并信息 ----------
    def _push_up(self, o):
        left, right = o << 1, o << 1 | 1
        # 最大值
        if self.mx[left] == self.mx[right]:
            self.mx[o] = self.mx[left]
            self.cnt[o] = self.cnt[left] + self.cnt[right]
            self.se[o] = max(self.se[left], self.se[right])
        else:
            if self.mx[left] > self.mx[right]:
                self.mx[o] = self.mx[left]
                self.cnt[o] = self.cnt[left]
                self.se[o] = max(self.se[left], self.mx[right])
            else:
                self.mx[o] = self.mx[right]
                self.cnt[o] = self.cnt[right]
                self.se[o] = max(self.mx[left], self.se[right])

    # ---------- 懒标记 ----------
    def _apply_chmin(self, o, v):
        """把节点 o 的最大值降到 v（v < mx）"""
        if self.mx[o] <= v:
            return
        self.mx[o] = v
        self.tag[o] = min(self.tag[o], v)   # 只保留最小的限制

    def _push_down(self, o):
        if self.tag[o] == INF:    # 没有需要下发的限制
            return
        v = self.tag[o]
        self._apply_chmin(o << 1, v)
        self._apply_chmin(o << 1 | 1, v)
        self.tag[o] = INF

    # ---------- 区间 chmin ----------
    def range_chmin(self, L, R, v):
        """把区间 [L,R] 的值取最小：a[i] = min(a[i], v)"""
        self._chmin(1, 0, self.n - 1, L, R, v)

    def _chmin(self, o, l, r, L, R, v):
        if L <= l and r <= R and self.mx[o] <= v:
            return                     # 本段已经全部 ≤ v，无需操作
        if L <= l and r <= R and self.se[o] < v < self.mx[o]:
            self._apply_chmin(o, v)    # 只把最大值降到 v
            return
        self._push_down(o)
        m = (l + r) // 2
        if L <= m:
            self._chmin(o << 1, l, m, L, R, v)
        if R > m:
            self._chmin(o << 1 | 1, m + 1, r, L, R, v)
        self._push_up(o)

    # ---------- 区间最大值 ----------
    def range_max(self, L, R):
        return self._query_max(1, 0, self.n - 1, L, R)

    def _query_max(self, o, l, r, L, R):
        if L <= l and r <= R:
            return self.mx[o]
        self._push_down(o)
        m = (l + r) // 2
        ans = -INF
        if L <= m:
            ans = max(ans, self._query_max(o << 1, l, m, L, R))
        if R > m:
            ans = max(ans, self._query_max(o << 1 | 1, m + 1, r, L, R))
        return ans

    # ---------- 单点赋值（把 d[pos] 设为 0） ----------
    def point_set_zero(self, pos):
        self._set_zero(1, 0, self.n - 1, pos)

    def _set_zero(self, o, l, r, pos):
        if l == r:
            self.mx[o] = 0
            self.se[o] = -INF
            self.cnt[o] = 1
            self.tag[o] = INF
            return
        self._push_down(o)
        m = (l + r) // 2
        if pos <= m:
            self._set_zero(o << 1, l, m, pos)
        else:
            self._set_zero(o << 1 | 1, m + 1, r, pos)
        self._push_up(o)


def blockPlacement(queries):
    """返回所有 type‑2 查询的布尔答案"""
    # 题目保证所有坐标不超过 5*10⁴，取一个稍大的上界
    MAX_X = 50000 + 5
    seg = SegTree(MAX_X)

    # 为了在更新时知道左侧最近的障碍位置，需要一棵有序集合
    # 这里用 Python 的 built‑in `bisect` + list 来模拟平衡 BST（足够快）
    import bisect
    obstacles = []          # 已经放好的障碍，始终保持有序

    ans = []
    for q in queries:
        if q[0] == 1:                     # 放障碍
            _, x = q
            # 1. 单点设为 0（自己到最近障碍的距离是 0）
            seg.point_set_zero(x)

            # 2. 找到左边最近的障碍，决定需要 chmin 的左区间
            idx = bisect.bisect_left(obstacles, x)
            left = obstacles[idx - 1] if idx > 0 else -1   # -1 表示“原点左侧没有障碍”，我们只关心非负坐标
            # 对区间 (left, x) 执行 d[i] = min(d[i], x - i)
            if left + 1 <= x - 1:
                seg.range_chmin(left + 1, x - 1, x)   # 这里的 v 用坐标 x，实际含义是 “距离不能超过 x - i”

            # 把新障碍加入有序集合
            obstacles.insert(idx, x)

        else:                               # 类型 2：能否放块
            _, x, sz = q
            right = x - sz
            if right < 0:          # 左端点根本不可能出现
                ans.append(False)
                continue
            max_dist = seg.range_max(0, right)
            ans.append(max_dist > sz)

    return ans
```

**代码要点解释（中文注释已写在代码里）**：

- `SegTree` 的每个节点维护 `mx`（最大距离）、`se`（第二大距离）和 `cnt`（最大值出现次数），这正是 **Segment Tree Beats** 所需的三件套。  
- `range_chmin` 把区间里**超过阈值**的值全部降到阈值。通过比较 `mx` 与阈值 `v`、以及 `se` 与 `v`，我们可以在 **不向下递归** 的情况下直接在节点上完成更新，从而保证 `O(log N)` 的摊销复杂度。  
- `range_max` 只需要把对应区间的 `mx` 合并即可。  
- 为了快速找到左侧最近的障碍，我们使用了一个有序列表 `obstacles` 并配合 `bisect`（二分查找）得到 `left`，这一步同样是 `O(log N)`。  

#### 复杂度

- **时间复杂度**  
  - 每一次 **类型 1** 更新：  
    - `bisect` 查找左侧障碍 → `O(log N)`  
    - `point_set_zero`（单点赋值） → `O(log N)`  
    - `range_chmin`（区间取最小） → 摊销 `O(log N)`  
    - 合计 `O(log N)`。  
  - 每一次 **类型 2** 查询：  
    - `range_max` → `O(log N)`  
    - 合计 `O(log N)`。  
  - 整体 `O(Q·log N)`，其中 `Q = len(queries) ≤ 1.5·10⁵`，`N ≈ 5·10⁴`。  
  - 用大白话说，这相当于“每次只需要检查大约 17~18 次（因为 2¹⁷≈1e5）”，非常快。

- **空间复杂度**  
  - 线段树数组大小 `4·N`，每个节点保存若干整数 → **O(N)**。  
  - 有序障碍列表最多存 `Q` 个坐标 → **O(Q)**。  
  - 总体仍是线性空间，约几百 KB，完全可以接受。

> 与暴力解相比，时间从 “遍历所有可能起点” 的 **平方级** 降到了 **对数级**，性能提升几个数量级，完全满足题目要求。

---

## 心得

- **核心技巧**：**维护每个位置到最近障碍的距离 `d[i]`，并用支持区间 `chmin` 与区间 `max` 的线段树（Segment Tree Beats）快速更新与查询。**  
- **适用的题型**  
  1. “区间最小化 / 区间最大化” 这类需要 **区间取最小后再查询最大** 的问题（如 LeetCode 307、2391 等）。  
  2. “动态障碍 / 动态区间可达性” 类题目，常见于游戏地图、排队系统等。  
- **一句话总结**：**把“能否放块”转化为“在左端点集合中是否存在一个距离大于块长的点”，用线段树 Beats 把“距离的下降”和“最大距离的查询”合二为一。**

---

## 反思

- **第一反应**：看到“无限坐标轴”和“放障碍”就想把所有坐标都记下来，随后对每个查询枚举所有起点——这就是暴力思路。  
- **最容易踩的坑**  
  1. **坐标上限**：虽然题目说是“无限”，实际约束把 `x` 限在 `5·10⁴`，必须利用这个上界才能开数组。  
  2. **左端点合法性**：当 `x - sz < 0` 时直接返回 `False`，否则会出现负区间导致数组越界。  
  3. **懒标记的正确下发**：在 Segment Tree Beats 中忘记在递归前 `push_down`，会导致后续查询得到错误的最大值。  
- **下次遇到同类题**：第一步先**抽象出一个单点属性**（这里是 “到下一个障碍的距离”），看看它在“插入障碍”时如何单调变化，再寻找**支持该单调变化的区间数据结构**（如区间 `chmin` + `max`），从而把原本的 O(N²) 暴力转化为 O(log N)。