# #803. 砖块被击中后掉落 / Bricks Falling When Hit

> 难度：困难 · 标签：Array、Union Find、Matrix · [LeetCode 链接](https://leetcode.com/problems/bricks-falling-when-hit/)

---

## 题目（英文原版）

**Description**

You are given an m x n binary grid, where each 1 represents a brick and 0 represents an empty space. A brick is stable if:
You are also given an array hits, which is a sequence of erasures we want to apply. Each time we want to erase the brick at the location hits[i] = (rowi, coli). The brick on that location (if it exists) will disappear. Some other bricks may no longer be stable because of that erasure and will fall. Once a brick falls, it is immediately erased from the grid (i.e., it does not land on other stable bricks).
Return an array result, where each result[i] is the number of bricks that will fall after the ith erasure is applied.
Note that an erasure may refer to a location with no brick, and if it does, no bricks drop.

**Examples**

**Example 1:**

```
Input: grid = [[1,0,0,0],[1,1,1,0]], hits = [[1,0]]
Output: [2]
Explanation: Starting with the grid:
[[1,0,0,0],
 [1,1,1,0]]
We erase the underlined brick at (1,0), resulting in the grid:
[[1,0,0,0],
 [0,1,1,0]]
The two underlined bricks are no longer stable as they are no longer connected to the top nor adjacent to another stable brick, so they will fall. The resulting grid is:
[[1,0,0,0],
 [0,0,0,0]]
Hence the result is [2].
```

**Example 2:**

```
Input: grid = [[1,0,0,0],[1,1,0,0]], hits = [[1,1],[1,0]]
Output: [0,0]
Explanation: Starting with the grid:
[[1,0,0,0],
 [1,1,0,0]]
We erase the underlined brick at (1,1), resulting in the grid:
[[1,0,0,0],
 [1,0,0,0]]
All remaining bricks are still stable, so no bricks fall. The grid remains the same:
[[1,0,0,0],
 [1,0,0,0]]
Next, we erase the underlined brick at (1,0), resulting in the grid:
[[1,0,0,0],
 [0,0,0,0]]
Once again, all remaining bricks are still stable, so no bricks fall.
Hence the result is [0,0].
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 200
- grid[i][j] is 0 or 1.
- 1 <= hits.length <= 4 * 104
- hits[i].length == 2
- 0 <= xi <= m - 1
- 0 <= yi <= n - 1
- All (xi, yi) are unique.

---

## 题目（中文翻译）

给定一个 `m × n` 的二进制网格 `grid`，其中 `1` 表示一块砖块，`0` 表示空位。  
一块砖块 **稳定**（stable）当且仅当它与第一行的任意砖块相连（通过上下左右相邻的砖块形成的路径），或者它本身就在第一行。

同时给定一个数组 `hits`，其中每个元素 `hits[i] = (row_i, col_i)` 表示一次擦除操作。每次操作我们会把位于 `(row_i, col_i)` 的砖块（若存在）移除。由于这块砖的消失，可能会导致其他砖块失去稳定性，从而 **掉落**（fall）。一旦砖块掉落，它会立刻从网格中消失（即不会落到其他稳定的砖块上）。

返回一个数组 `result`，其中 `result[i]` 表示在第 `i` 次擦除操作之后会掉落的砖块数量。  
需要注意的是，擦除操作可能指向一个本来就没有砖块的位置，此时不会有砖块掉落。

**示例 1**  
**输入**  
```text
grid = [[1,0,0,0],
        [1,1,1,0]]
hits = [[1,0]]
```
**输出**  
```text
[2]
```
**解释**  
初始网格为：

```
[[1,0,0,0],
 [1,1,1,0]]
```

我们擦除坐标为 `(1,0)` 的砖块（下划线标记），得到：

```
[[1,0,0,0],
 [0,1,1,0]]
```

此时右侧的两块砖（下划线标记）不再与顶部相连，也没有相邻的稳定砖块，它们会掉落。掉落后网格变为：

```
[[1,0,0,0],
 [0,0,0,0]]
```

因此结果为 `[2]`。

**示例 2**  
**输入**  
```text
grid = [[1,0,0,0],
        [1,1,0,0]]
hits = [[1,1],[1,0]]
```
**输出**  
```text
[0,0]
```
**解释**  
初始网格为：

```
[[1,0,0,0],
 [1,1,0,0]]
```

1. 第一次擦除 `(1,1)`（下划线标记），得到：

```
[[1,0,0,0],
 [1,0,0,0]]
```

剩余的所有砖块仍然稳定，未掉落。网格保持不变。

2. 第二次擦除 `(1,0)`（下划线标记），得到：

```
[[1,0,0,0],
 [0,0,0,0]]
```

此时仍然没有砖块掉落。

所以最终结果为 `[0,0]`。

**约束条件**

- `m == grid.length`
- `n == grid[i].length`
- `1 ≤ m, n ≤ 200`
- `grid[i][j]` 仅为 `0` 或 `1`
- `1 ≤ hits.length ≤ 4 × 10⁴`
- `hits[i].length == 2`
- `0 ≤ xi ≤ m - 1`
- `0 ≤ yi ≤ n - 1`
- 所有 `(xi, yi)` 坐标互不相同

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**每次击打后**，把对应位置的砖块设为 0（如果本来就是 0 则什么也不做），然后遍历整张网格，判断哪些砖块仍然“稳固”。  
- **稳固的定义**：砖块位于第一行（直接接触天花板）或与至少一个已经稳固的砖块相邻（上下左右四个方向）。  
- 为了判断稳固性，可以从第一行的所有砖块出发，使用 **BFS/DFS**（深度优先搜索）把所有能够“连通天花板”的砖块标记为稳固。  
- 再遍历一遍网格，未被标记的 1 就是会掉落的砖块，把它们全部置为 0，计数即为本次击打的答案。

> **类比**：把网格想象成一张纸，上面贴了很多小方块（砖）。我们把第一行的方块看成“根”，从根出发，顺着相邻的方块向下爬，爬到的所有方块都是“不掉”。其余的方块就会“掉下来”。

**为什么正确**  
- 只要砖块能通过相邻的砖块一路向上到达第一行，就一定不会掉落（题目定义的稳固条件）。  
- BFS/DFS 正好能把所有满足这个条件的砖块找出来。  

**时间/空间复杂度**  
- 对每一次击打，我们都要 **遍历整个网格一次**（`O(m·n)`）来做 BFS，又要再遍历一次统计掉落砖块，整体是 `O(m·n)`。  
- 如果击打次数为 `k`，总时间是 `O(k·m·n)`。在最坏情况下，`k` 可达 `4·10⁴`，`m·n` 最多 `200·200=4·10⁴`，导致时间爆炸（约 `1.6·10⁹` 步，远超时限）。  
- BFS 使用的队列和标记数组大小为 `O(m·n)`，即 **空间 `O(m·n)`**。

#### 代码（Python）

```python
from collections import deque
from copy import deepcopy
from typing import List

def hit_bricks_bruteforce(grid: List[List[int]], hits: List[List[int]]) -> List[int]:
    m, n = len(grid), len(grid[0])
    # 为了不改动原始数据，拷贝一份
    board = deepcopy(grid)

    def bfs_stable() -> List[List[bool]]:
        """从第一行出发，用 BFS 标记所有稳固的砖块"""
        stable = [[False] * n for _ in range(m)]
        q = deque()
        # 所有第一行的砖块都是稳固的起点
        for col in range(n):
            if board[0][col] == 1:
                stable[0][col] = True
                q.append((0, col))

        while q:
            r, c = q.popleft()
            for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and board[nr][nc] == 1 and not stable[nr][nc]:
                    stable[nr][nc] = True
                    q.append((nr, nc))
        return stable

    ans = []
    for hit_r, hit_c in hits:
        # 1. 删除击中的砖块（如果本来就是 0 则不动）
        if board[hit_r][hit_c] == 1:
            board[hit_r][hit_c] = 0
        # 2. 找出所有稳固的砖块
        stable = bfs_stable()
        # 3. 统计并删除不稳固的砖块
        fallen = 0
        for i in range(m):
            for j in range(n):
                if board[i][j] == 1 and not stable[i][j]:
                    board[i][j] = 0
                    fallen += 1
        ans.append(fallen)
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(k·m·n)`  
  > 这里的 `k` 是击打次数，`m·n` 是网格大小。意思是每次都要遍历整张网格一次，随 `k` 成线性增长。  

- **空间复杂度**：`O(m·n)`  
  > 需要额外的 `stable` 布尔矩阵和 BFS 队列，规模与网格相同。  

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都重新遍历整张网格**。我们需要一种能够“记住”之前已经稳定的结构，只在局部做更新。  
关键观察：

1. **逆向思考**：如果我们把所有击打一次性全部执行（把对应位置的砖块都先删掉），得到一个“最终状态”。  
2. 从这个最终状态开始，**逆向回放**每一次击打：把被删除的砖块“恢复”回来。恢复后，只需要检查这块砖块以及它的相邻砖块是否会因为这次恢复而变得稳固。  
3. 只要我们能快速判断两块砖块是否在同一个“稳固集合”中，就能在恢复时快速合并集合，进而得到本次击打导致掉落的砖块数量。  

这正好对应 **并查集（Union‑Find）** 的能力：

- 每个砖块视为一个节点。  
- 两块相邻且都是砖的节点合并到同一个集合，表示它们互相支撑。  
- 为了判断是否“稳固”，额外再设一个 **虚拟节点**（编号 `top`），与所有第一行的砖块相连。只要一个砖块所在的集合和 `top` 在同一个集合里，它就稳固。

**逆向过程**：

1. **预处理**：把 `hits` 中的所有位置的砖块先标记为 “被打掉”。得到 `grid_after_hits`。  
2. **建立并查集**：遍历 `grid_after_hits`，把相邻的砖块合并；把第一行的砖块与 `top` 合并。此时并查集记录了“最终状态”下的所有稳固关系。  
3. **逆序回放 hits**：从最后一次击打开始向前处理。  
   - 把被打掉的砖块 **恢复**（如果原本就是 0，则直接记 0）。  
   - 把它与四个方向上已有的砖块（如果有）合并。  
   - 如果恢复的砖块在第一行，则把它也合并到 `top`。  
   - 恢复前后，**`top` 所在集合的大小**会变化。`size_before` 为恢复前 `top` 所在集合的砖块数量（不包括 `top` 本身），`size_after` 为恢复后。  
   - 本次击打导致掉落的砖块数 = `size_after - size_before - 1`（减 1 是因为恢复的那块砖本身不算掉落）。  
4. 把每一步的结果存入答案数组，最后逆序返回即可。

> **类比**：把每个砖块看成城市，城市之间有道路（相邻关系）。`top` 是首都。只要一个城市能通过道路到达首都，它就不会被抛弃。我们先把所有被炸掉的城市从地图上删掉，得到“残缺的地图”。再把城市一个个“复建”，每复建一次，就检查首都能到达多少城市，变化的部分就是这次炸弹的“影响”。  

**并查集的实现细节**：

- `parent[x]`：节点 `x` 的父节点。  
- `size[x]`：以 `x` 为根的集合中包含的砖块数量（不算 `top`，但我们可以把 `top` 也算进去，后面只要减去它）。  
- `find(x)`：路径压缩，使后续查询更快。  
- `union(a,b)`：把两个集合合并，根节点较大的集合保留为新根，`size` 也相应相加。

#### 代码（Python）

```python
from typing import List

class UnionFind:
    def __init__(self, n: int):
        # 每个节点的父节点初始化为自己
        self.parent = list(range(n))
        # size 记录每个根节点对应集合的砖块数量（不包括虚拟节点）
        self.size = [1] * n

    def find(self, x: int) -> int:
        # 递归找根并路径压缩
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        # 小集合挂到大集合下面，保持树的平衡
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]

    def get_size(self, x: int) -> int:
        """返回根节点所在集合的大小"""
        return self.size[self.find(x)]

def hit_bricks(grid: List[List[int]], hits: List[List[int]]) -> List[int]:
    m, n = len(grid), len(grid[0])
    total = m * n
    top = total                     # 虚拟节点的编号，放在最后
    uf = UnionFind(total + 1)       # 包含虚拟节点的并查集

    # 1️⃣ 把所有要击中的砖块先标记为 0（相当于提前“打掉”）
    # 使用 copy，避免修改原始输入
    after = [row[:] for row in grid]
    for r, c in hits:
        after[r][c] = 0

    # 2️⃣ 建立并查集：把相邻的砖块合并，第一行的砖块与 top 合并
    def idx(r: int, c: int) -> int:
        return r * n + c

    for r in range(m):
        for c in range(n):
            if after[r][c] != 1:
                continue
            # 如果在第一行，直接和 top 相连
            if r == 0:
                uf.union(idx(r, c), top)
            # 向左、向上检查相邻砖块（只需要检查两个方向避免重复）
            for dr, dc in [(-1, 0), (0, -1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and after[nr][nc] == 1:
                    uf.union(idx(r, c), idx(nr, nc))

    # 3️⃣ 逆序处理 hits
    ans = [0] * len(hits)
    for i in range(len(hits) - 1, -1, -1):
        r, c = hits[i]
        # 如果原来本来就是空的，直接记 0
        if grid[r][c] == 0:
            ans[i] = 0
            continue

        # 记录恢复前，top 所在集合的大小（不包括虚拟节点本身）
        pre_top_size = uf.get_size(top)

        # 恢复这块砖
        after[r][c] = 1
        cur_idx = idx(r, c)

        # 如果在第一行，直接连到 top
        if r == 0:
            uf.union(cur_idx, top)

        # 与四个方向的已有砖块合并
        for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and after[nr][nc] == 1:
                uf.union(cur_idx, idx(nr, nc))

        # 恢复后，top 所在集合的大小
        post_top_size = uf.get_size(top)

        # 掉落的砖块数 = 新加入到 top 的砖块数量 - 1（恢复的这块砖不算）
        fallen = max(0, post_top_size - pre_top_size - 1)
        ans[i] = fallen

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(m·n + k·α(m·n))`  
  - `m·n` 用于一次性遍历网格并构建并查集。  
  - `k` 为击打次数，每次逆向恢复只做常数次 `union`/`find`，其时间近似 `α(N)`（反Ackermann 函数），在实际中可以视作常数。  
  - 与暴力解的 `O(k·m·n)` 相比，**只和网格大小线性相关**，大幅降低。  

- **空间复杂度**：`O(m·n)`  
  - 并查集的 `parent`、`size` 数组各占 `m·n + 1`，以及一个复制的 `after` 网格，同样是网格规模的线性空间。  

---

## 心得

- **核心技巧**：**逆向思考 + 并查集**。先把所有击打一次性执行，再逆向“恢复”可以把每一步的影响局部化，只需要维护连通性。  
- **适用的题型**  
  1. “删除后查询连通块” 类问题，如 **LeetCode 200**（岛屿数量） 的离线版本。  
  2. “动态连通性” 场景，例如 **LeetCode 1557**（可以到达的最远节点） 的逆向 Union‑Find 解法。  
  3. “矩阵中的连通块” 需要频繁删除或添加的题目，如 **LeetCode 695**（岛屿的最大面积） 的离线并查集思路。  

> **一句话总结**：把“打砖块”倒着来看——先把所有砖块踢掉，再逐个放回去，用并查集快速维护“能连到天花板的砖块集合”，掉落的砖块数就等于每次放回去后新加入集合的大小。

---

## 反思

- **第一反应**：直接模拟每次击打后重新 BFS，想到“遍历整张网格”。这是一种自然的暴力思路，却忽视了题目中击打次数可能非常大。  
- **最容易踩的坑**  
  1. **边界条件**：击打位置本来就是 0，需要返回 0，且不能把 `size` 减 1 出错。  
  2. **并查集的大小计数**：`size` 包含虚拟节点时需要特别处理，答案中要减去恢复的那块砖本身。  
  3. **逆序恢复时的相邻合并**：只能合并已经“存在”的砖块，`after` 必须及时更新，否则会错误地把空位当砖块。  
- **下次类似题目**：  
  1. **先判断是否可以离线**：如果所有修改都是“删除”，考虑先全部删除再逆向恢复。  
  2. **寻找一个全局不变的“根”**（本题的天花板），把它抽象成虚拟节点，用并查集维护与根的连通性。  
  3. **把每一步的增量变化转化为集合大小的差值**，这样就能 O(1) 直接得到答案。