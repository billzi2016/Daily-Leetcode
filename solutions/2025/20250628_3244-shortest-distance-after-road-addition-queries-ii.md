# #3244. 道路新增查询后的最短距离 II / Shortest Distance After Road Addition Queries II

> 难度：困难 · 标签：Array、Greedy、Graph、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/shortest-distance-after-road-addition-queries-ii/)

---

## 题目（英文原版）

**Description**

You are given an integer n and a 2D integer array queries.
There are n cities numbered from 0 to n - 1. Initially, there is a unidirectional road from city i to city i + 1 for all 0 <= i < n - 1.
queries[i] = [ui, vi] represents the addition of a new unidirectional road from city ui to city vi. After each query, you need to find the length of the shortest path from city 0 to city n - 1.
There are no two queries such that queries[i][0] < queries[j][0] < queries[i][1] < queries[j][1].
Return an array answer where for each i in the range [0, queries.length - 1], answer[i] is the length of the shortest path from city 0 to city n - 1 after processing the first i + 1 queries.

**Examples**

**Example 1:**

```
Input: n = 5, queries = [[2,4],[0,2],[0,4]]
Output: [3,2,1]
Explanation:

After the addition of the road from 2 to 4, the length of the shortest path from 0 to 4 is 3.

After the addition of the road from 0 to 2, the length of the shortest path from 0 to 4 is 2.

After the addition of the road from 0 to 4, the length of the shortest path from 0 to 4 is 1.
```

**Example 2:**

```
Input: n = 4, queries = [[0,3],[0,2]]
Output: [1,1]
Explanation:

After the addition of the road from 0 to 3, the length of the shortest path from 0 to 3 is 1.

After the addition of the road from 0 to 2, the length of the shortest path remains 1.
```

**Constraints**

- 3 <= n <= 105
- 1 <= queries.length <= 105
- queries[i].length == 2
- 0 <= queries[i][0] < queries[i][1] < n
- 1 < queries[i][1] - queries[i][0]
- There are no repeated roads among the queries.
- There are no two queries such that i != j and queries[i][0] < queries[j][0] < queries[i][1] < queries[j][1].

---

## 题目（中文翻译）

你得到一个整数 `n` 和一个二维整数数组 `queries`。  
有 `n` 个城市，编号为 `0` 到 `n - 1`。最初，对于所有 `0 ≤ i < n - 1`，都存在一条 **单向道路（unidirectional road）** 从城市 `i` 指向城市 `i + 1`。  

`queries[i] = [u_i, v_i]` 表示新增一条 **单向道路（unidirectional road）** 从城市 `u_i` 到城市 `v_i`。在处理完每一次查询后，你需要求出从城市 `0` 到城市 `n - 1` 的最短路径长度。  

不存在两条查询满足 `queries[i][0] < queries[j][0] < queries[i][1] < queries[j][1]`。  

返回一个数组 `answer`，其中 `answer[i]` 为处理前 `i + 1` 条查询后，从城市 `0` 到城市 `n - 1` 的最短路径长度。

## 示例

### 示例 1

**输入**  
`n = 5, queries = [[2,4],[0,2],[0,4]]`

**输出**  
`[3,2,1]`

**解释**  

- 在新增从 `2` 到 `4` 的道路后，`0` 到 `4` 的最短路径长度为 `3`。  
- 在新增从 `0` 到 `2` 的道路后，`0` 到 `4` 的最短路径长度为 `2`。  
- 在新增从 `0` 到 `4` 的道路后，`0` 到 `4` 的最短路径长度为 `1`。

### 示例 2

**输入**  
`n = 4, queries = [[0,3],[0,2]]`

**输出**  
`[1,1]`

**解释**  

- 在新增从 `0` 到 `3` 的道路后，`0` 到 `3` 的最短路径长度为 `1`。  
- 在新增从 `0` 到 `2` 的道路后，最短路径长度仍保持为 `1`。

## 约束条件

- `3 ≤ n ≤ 10^5`
- `1 ≤ queries.length ≤ 10^5`
- `queries[i].length == 2`
- `0 ≤ queries[i][0] < queries[i][1] < n`
- `1 < queries[i][1] - queries[i][0]`
- 查询中不存在重复的道路。
- 不存在两个不同的查询 `i ≠ j` 满足 `queries[i][0] < queries[j][0] < queries[i][1] < queries[j][1]`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**每次新增一条单向道路后，重新跑一次最短路**。  
因为所有道路的权重都是 `1`，我们可以把图看成 **无权有向图**，于是 BFS（广度优先搜索）就可以求出从城市 `0` 到城市 `n-1` 的最短路径长度。

- **数据结构**  
  - **邻接表**：把每条道路保存到 `graph[u]` 中，类似于把每本书的章节目录写在一本字典里，`u` 是章节号，`graph[u]` 里存放所有可以直接跳到的章节（城市）。  
  - **队列**：BFS 用的“排队”结构，像排队买票一样，先进入的先出。

- **为什么正确**  
  BFS 从起点 `0` 按层次展开，每层恰好对应路径长度 `+1`，因此第一次到达终点 `n-1` 时的层数就是最短路径的长度。每次我们把新道路加入图中，再跑一次 BFS，得到的距离一定是当前所有道路构成的最短路径。

- **复杂度分析（大白话）**  
  - **时间复杂度**：一次 BFS 需要遍历所有城市和所有道路，最坏情况是 `O(n + m)`，其中 `m = (n-1) + #queries`（原来的链路 `n-1` 条，加上已经加入的查询）。因为我们要在每一条查询后都重新跑一次 BFS，整体是 `O(q·(n+q))`，在最坏情况下接近 `O(10^10)`，这对 10⁵ 规模的数据根本跑不完。  
  - **空间复杂度**：保存图需要 `O(n+q)` 的邻接表，队列最多装 `O(n)` 个城市，整体 `O(n+q)`。

> **简化记号**：  
> - `O(n²)` 并不是说真的要算 `n` 的平方次，而是说算法的运行次数会随 `n` 的增大 **呈二次增长**，比如 `n=10⁵` 时会有 10¹⁰ 次操作，远远超出计算机的承受范围。

#### 代码（Python）

```python
from collections import deque, defaultdict

def brute_force(n, queries):
    # 初始的单向链路 0->1->2->...->n-1
    graph = defaultdict(list)
    for i in range(n - 1):
        graph[i].append(i + 1)

    ans = []
    for u, v in queries:                     # 逐条处理查询
        graph[u].append(v)                    # 加入新道路

        # BFS 求最短路
        dist = [-1] * n
        q = deque([0])
        dist[0] = 0
        while q:
            cur = q.popleft()
            if cur == n - 1:                  # 已经到达终点，最短路找到了
                break
            for nxt in graph[cur]:
                if dist[nxt] == -1:           # 只访问一次，防止重复
                    dist[nxt] = dist[cur] + 1
                    q.append(nxt)

        ans.append(dist[n-1])                 # 记录当前答案
    return ans
```

#### 复杂度

- **时间复杂度**：`O(q·(n+q))`，每条查询都重新跑一次 BFS，几乎是二次甚至三次方级别的运算，实际会超时。  
- **空间复杂度**：`O(n+q)` 用来存图和 BFS 队列。  

> 暴力解帮助我们理解“每次都全局重新计算最短路”是行不通的，接下来要找出 **只改动受影响的部分**，从而把复杂度降到可接受的范围。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**每次加入的道路只会让距离变短**，而且所有道路都是 **只向前**（`u < v`），形成一个 **有向无环图 (DAG)**。  
我们要利用两个关键性质：

1. **距离只会单调递减**  
   初始距离 `dist[i] = i`（走链路一步一步走）。加入新道路后，某些城市的距离可能变小，但永远不会再增大。

2. **查询区间不交叉**  
   题目保证不存在 `u_i < u_j < v_i < v_j`（两条道路“交叉”）。这意味着所有新道路形成的区间集合是 **层叠（laminar）** 的：  
   - 要么相互不相交（完全左/右），  
   - 要么一个完全套在另一个内部。  
   想象一排书架，所有新放进去的书（区间）要么整本放在左边，要么整本放在右边，绝不会出现“左半边一本书，右半边另一本书交错” 的情况。

这两个性质让我们可以 **只在需要的地方更新距离**，而且每个城市的距离 **最多只会被更新一次**（因为一旦被更小的值覆盖，再也不可能再变大）。

---

#### 2.1 关键观察：距离的“线性”结构  

因为每条道路的权重都是 `1`，从城市 `v` 往后的所有城市如果沿着原来的链路继续走，距离会 **每走一步 +1**。  
换句话说，加入一条道路 `(u, v)` 会在位置 `v` 产生一条 **斜率为 1 的直线**，起点的高度是 `dist[u] + 1`（从 `0` 到 `u` 的最短距离，加上这条新道路）。  
之后的城市 `i (>= v)` 的候选距离就是：

```
candidate(i) = (dist[u] + 1) + (i - v)
```

这正好是 “起点高度 + 直线斜率(1) × 横坐标偏移”。  
如果 `candidate(i)` 小于当前的 `dist[i]`，我们就把 `dist[i]` 降下来。

**所有已加入的道路都会产生这样的一条斜率为 1 的直线**。  
在同一个位置 `i`，真实的最短距离是 **所有直线的最小值** 与原始链路距离 `i` 的最小值。

因为斜率相同，**只需要保留“最低的截距”**（即 `dist[u] + 1 - v`）即可。  
但这个截距本身依赖于 `dist[u]`，而 `dist[u]` 又可能已经被更早的直线压低。于是我们只能**逐点更新**，但可以保证每点只更新一次。

---

#### 2.2 用「未被压低的点」维护集合  

我们维护两个数组：

- `dist[i]`：当前已知的最短距离（会逐步下降）。
- `bad`（或叫 `unimproved`）：一个 **有序集合**，保存所有**尚未被任何直线压低**的城市编号。  
  初始时 `dist[i] = i`，所有城市都是“未被压低”，所以集合是 `{0, 1, 2, …, n‑1}`。

当处理查询 `(u, v)` 时：

1. 计算从起点到 `u` 的当前最短距离 `cur = dist[u] + 1`（再加上新道路本身）。
2. 在有序集合中找到第一个 **不小于 `v`** 的城市 `p`（二分搜索）。
3. 从 `p` 开始向右遍历，只要 `cur + (p - v) < dist[p]`，就说明这条新直线把城市 `p` 的距离压得更低。于是：
   - 把 `dist[p]` 更新为 `cur + (p - v)`；
   - 把 `p` 从集合中 **删除**（因为它已经不再等于原始的 `p`，以后不会再被检查）。
4. 当遇到某个城市 `p` 使得 `cur + (p - v) >= dist[p]`，说明这条直线已经“被更低的直线遮住”，后面的城市更不可能被压低，直接退出循环。

**为什么每个城市只会被删除一次？**  
一旦我们把城市 `p` 从集合中删掉，说明已经找到了一条更短的路径，使得 `dist[p] < p`。后面的任何新道路的起点 `u` 必须满足 `u ≤ p`（因为区间不交叉），而新的直线的截距 `dist[u] + 1 - v` **不会比已经得到的更大**，因此不可能再次让 `dist[p]` 变得更大，也不可能再出现 `cur + (p - v) < dist[p]` 的情况。于是 `p` 再也不会被重新检查。

因此：

- **每个城市最多被弹出集合一次** → 总的内部循环次数 `≤ n`。  
- 每次查询只做一次 `bisect_left`（`O(log n)`）和若干次弹出（累计 `O(n)`），整体时间 `O((n + q) log n)`，在 `10⁵` 规模下轻松通过。

---

#### 2.3 代码实现细节  

Python 没有内置的平衡树，但我们可以用 **`list` + `bisect`** 来模拟有序集合：

- `unimproved = list(range(n))` 保存有序的城市编号。  
- `bisect_left(unimproved, v)` 找到第一个 `≥ v` 的位置。  
- 删除时使用 `pop(i)`，因为每个元素只会被删除一次，累计的 `O(n)` 删除开销仍然是线性的。

这就完成了 **“只更新真正受影响的点”** 的高效实现。

---

#### 代码（Python）

```python
import bisect

def shortest_distance_after_road_addition(n: int, queries):
    """
    最优解：每条查询只在必要的城市上做一次更新。
    返回每次查询后的最短路径长度（从 0 到 n-1）。
    """
    # 初始距离：沿着原链路一步一步走
    dist = list(range(n))               # dist[i] = i
    # 保存“尚未被压低”的城市编号，保持有序
    unimproved = list(range(n))         # 0,1,2,...,n-1

    ans = []

    for u, v in queries:
        # 通过已知的 dist[u] 再走一条新路到 v
        cur = dist[u] + 1               # 新直线在位置 v 的起始高度

        # 在 unimproved 中找到第一个 >= v 的城市
        idx = bisect.bisect_left(unimproved, v)

        # 从该位置开始向右检查，直到新直线不再能压低为止
        while idx < len(unimproved):
            p = unimproved[idx]         # 当前城市编号
            # 通过新直线到达 p 的距离
            cand = cur + (p - v)

            if cand < dist[p]:          # 可以压低
                dist[p] = cand          # 更新距离
                # 该城市已不再等于原始的 p，删除它
                unimproved.pop(idx)    # 删除后，下一个元素会自动移动到 idx 位置
                # 不需要 ++idx，因为 pop 后 idx 指向的就是下一个元素
            else:
                # 直线已经被更低的路径遮住，后面的城市更不可能被压低
                break

        # 当前答案就是到终点 n-1 的距离
        ans.append(dist[n - 1])

    return ans
```

> **代码要点注释（中文）**  
> - `dist[u] + 1`：到达 `u` 的最短距离再加上这条新道路，得到在 `v` 位置的“起点高度”。  
> - `cand = cur + (p - v)`：从 `v` 走到 `p` 需要多走 `(p - v)` 步，每步代价 `1`，于是得到候选距离。  
> - `unimproved.pop(idx)`：一旦 `dist[p]` 被压低，`p` 再也不可能回到 “未被压低” 的状态，直接从集合中删掉，保证以后不再检查。  

#### 复杂度

- **时间复杂度**：`O((n + q)·log n)`  
  - 每次查询一次二分查找 `O(log n)`。  
  - 内层 `while` 循环累计至多弹出 `n` 次城市（每个城市只弹出一次），所以总体 `O(n)`。  
  - 综上，两部分相加得到 `O((n+q) log n)`，在 `n, q ≤ 10⁵` 时约几百万次操作，轻松通过。

- **空间复杂度**：`O(n)`  
  - `dist`、`unimproved` 各占 `O(n)`，额外的常数级别变量不影响量级。

> 与暴力解相比，时间从 **二次/三次方** 降到了 **准线性**（带一个对数因子），这是本题的关键突破。

---

## 心得

- **核心技巧**：利用 **单调递减 + 区间不交叉** 的特性，只在“被新直线真正压低”的点上更新距离，并把这些点从有序集合中剔除，保证每个点只被处理一次。  
- **适用场景**  
  1. **动态最短路**（边权统一且只往前）——如本题的“链路 + 单向快捷道路”。  
  2. **区间最小值/覆盖**——当所有更新都是 **斜率相同的线**（或等价的 “+1” 步长）时，可用类似的“删除已满足条件的点”技巧。  
  3. **层叠区间（laminar）结构**——任何保证“区间不交叉”的动态问题，都可以尝试用 **一次遍历 + 删除** 的思路把复杂度降到线性。
- **一句话总结**：**“只在真正被新道路压低的城市上更新，并一次性把它们踢出‘待检查集合’，这样每个城市只改一次，整体线性”。**

---

## 反思

- **第一反应**：直接每次跑 BFS，想把所有道路重新算一遍。  
- **最容易踩的坑**  
  - 忘记利用 **方向性**（所有道路都是从左往右），导致把图当成一般有向图，误以为需要全图最短路。  
  - 忽视 **区间不交叉** 的限制，以为需要处理任意区间交叉的情况，结果设计的结构过于复杂。  
  - 在实现有序集合时使用了 `set`（无序）或 `heap`（不支持定位删除），导致删除操作变成 `O(n)`，整体复杂度失控。  
- **下次类似题目**：  
  1. **先检查是否有单调/方向性**（比如只能向前、只能递增）。  
  2. **寻找“只会改变一次”的元素**（如本题的每个城市只会被压低一次），利用 **一次性删除** 的思想把整体复杂度压到线性。  
  3. **利用题目给出的结构限制**（如 laminar 区间）简化数据结构的设计。  

祝你在算法的道路上越走越顺 🚀