# #3609. **网格中到达目标的最少移动次数** / Minimum Moves to Reach Target in Grid

> 难度：困难 · 标签：Math · [LeetCode 链接](https://leetcode.com/problems/minimum-moves-to-reach-target-in-grid/)

---

## 题目（英文原版）

**Description**

You are given four integers sx, sy, tx, and ty, representing two points (sx, sy) and (tx, ty) on an infinitely large 2D grid.
You start at (sx, sy).
At any point (x, y), define m = max(x, y). You can either:
Return the minimum number of moves required to reach (tx, ty). If it is impossible to reach the target, return -1.

**Examples**

**Example 1:**

```
Input: sx = 1, sy = 2, tx = 5, ty = 4
Output: 2
Explanation:
The optimal path is:
Thus, the minimum number of moves to reach (5, 4) is 2.
```

**Example 2:**

```
Input: sx = 0, sy = 1, tx = 2, ty = 3
Output: 3
Explanation:
The optimal path is:
Thus, the minimum number of moves to reach (2, 3) is 3.
```

**Example 3:**

```
Input: sx = 1, sy = 1, tx = 2, ty = 2
Output: -1
Explanation:
```

**Constraints**

- 0 <= sx <= tx <= 109
- 0 <= sy <= ty <= 109

---

## 题目（中文翻译）

给定四个整数 `sx`、`sy`、`tx` 和 `ty`，它们分别表示二维无限网格上的两个点 `(sx, sy)` 和 `(tx, ty)`。  
你从点 `(sx, sy)` 开始。  

在任意点 `(x, y)` 处，定义 `m = max(x, y)`。此时你可以执行以下操作之一：

（题目原文中此处应列出具体的移动规则，保持原样不变）

返回到达 `(tx, ty)` 所需的最少移动次数。如果无法到达目标，返回 `-1`。

---

### 示例

**示例 1**  
```
Input: sx = 1, sy = 2, tx = 5, ty = 4
Output: 2
```
**解释**：  
最佳路径为：  
（此处原题会给出具体的路径步骤，保持原样）  
因此，达到 `(5, 4)` 的最少移动次数为 2。

**示例 2**  
```
Input: sx = 0, sy = 1, tx = 2, ty = 3
Output: 3
```
**解释**：  
最佳路径为：  
（此处原题会给出具体的路径步骤，保持原样）  
因此，达到 `(2, 3)` 的最少移动次数为 3。

**示例 3**  
```
Input: sx = 1, sy = 1, tx = 2, ty = 2
Output: -1
```
**解释**：  
（此处原题会说明为什么无法到达目标，保持原样）

---

### 约束条件

- `0 <= sx <= tx <= 10^9`
- `0 <= sy <= ty <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

- **问题复述**：  
  给定起点 `(sx, sy)` 和目标点 `(tx, ty)`（均在左下角，坐标不递减），在任意位置 `(x, y)` 定义 `m = max(x, y)`。一次合法的移动可以把 **较小的坐标** 加上 `m`，即  
  ```
  (x, y) → (x + m, y)   或   (x, y) → (x, y + m)
  ```  
  求最少的移动次数，若不可达返回 `-1`。

- **最直接的想法**：  
  从起点不停尝试所有可能的移动，直到达到目标。可以用 **广度优先搜索 (BFS)** 把每一种坐标看成图的一个节点，边就是一次合法移动。  
  - **数据结构**：  
    - 队列（queue）存放待扩展的坐标，类似查字典时把“单词”放进队列逐层展开。  
    - 哈希集合（set）记录已经访问过的坐标，防止重复搜索——就像字典的“已经查过的页码”。  

- **为什么一定能得到答案**：  
  BFS 按层遍历，第一次碰到目标点时走的路径必然是最短的，因为所有路径都是等权重的。

- **复杂度分析（大白话）**：  
  - 每次移动都会把一个坐标 **变大**（因为 `m ≥ 当前坐标`），所以搜索空间在最坏情况下会像树一样指数增长。若目标坐标很大（上限 `10⁹`），搜索的节点数可能接近 `O((tx‑sx)·(ty‑sy))`，也就是 **平方级**。  
  - 时间复杂度：`O(N²)`（N 代表坐标范围），直观上相当于“把整个二维平面都扫一遍”。  
  - 空间复杂度：同样是 `O(N²)`，因为要把已经走过的点都记下来。

> **结论**：暴力 BFS 能保证正确，却会在大数情况下彻底超时，必须寻找更聪明的办法。

#### 代码（Python）

```python
from collections import deque

def min_moves_bruteforce(sx: int, sy: int, tx: int, ty: int) -> int:
    # 特殊情况：起点已经是终点
    if (sx, sy) == (tx, ty):
        return 0

    q = deque()
    q.append((sx, sy, 0))          # (x, y, 已经用了多少步)
    visited = {(sx, sy)}          # 已经访问过的坐标，防止循环

    while q:
        x, y, step = q.popleft()
        m = max(x, y)

        # 两种合法的下一步
        nxt = [(x + m, y), (x, y + m)]
        for nx, ny in nxt:
            # 越界剪枝：坐标只会增大，超过目标就没有必要继续搜索
            if nx > tx or ny > ty:
                continue
            if (nx, ny) == (tx, ty):
                return step + 1          # 第一次到达即最短
            if (nx, ny) not in visited:
                visited.add((nx, ny))
                q.append((nx, ny, step + 1))

    # BFS 结束仍未找到，说明不可达
    return -1
```

#### 复杂度

- **时间复杂度**：`O(N²)`，其中 `N = max(tx‑sx, ty‑sy)`。直观上相当于在一个 `N × N` 的方格里遍历每一个格子。  
- **空间复杂度**：`O(N²)`，需要把已经访问的格子全部记下来，最坏情况下几乎占满整个方格。  

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **“正向搜索”**——我们一直在把坐标往更大的方向扩张，导致搜索树爆炸。  
关键观察：**每一步的操作都是可逆的**，只要我们从目标点倒着走，往回“撤销”一步，就能快速逼近起点。

**逆向撤销的规则**（从 `(x, y)` 回到它的前一个状态）：

1. 设 `a = max(x, y)`（较大的坐标），`b = min(x, y)`（较小的坐标）。  
2. 如果 `a` **至少是** `2·b`，说明前一步一定是把 `b` 加到了 `a` 上，使 `a` 变成 `2·b`、`3·b`…  
   - 此时我们可以直接把 `a` **除以 2**（或者更一般地 `a //= b`）来“撤销”。  
   - 为了计数，需要把除以的次数累加到答案里。  
3. 否则，`a` 与 `b` 的差距不够大，只能是 **一次** `a = a - b`（因为前一步只能把 `b` 加一次）。  
   - 于是我们执行 `a -= b`，计数+1。  

这就是 **“欧几里得算法”**（求最大公约数）在坐标上的变形：每次都把大的数减去小的数，或者把大的数对小的数取模。  
因为每一步都会让较大的坐标 **明显变小**，循环的次数最多是 `log(max(tx, ty))` 级别，极其高效。

**完整的逆向过程**：

```
moves = 0
while tx > sx and ty > sy:
    if tx > ty:
        # 大坐标是 tx
        if tx >= 2*ty:          # 可以一次性“除以”
            moves += tx // ty   # 撤销了多少次
            tx %= ty
            if tx == 0:         # 防止出现 0，恢复为 ty
                tx = ty
        else:
            tx -= ty
            moves += 1
    else:
        # 大坐标是 ty
        if ty >= 2*tx:
            moves += ty // tx
            ty %= tx
            if ty == 0:
                ty = tx
        else:
            ty -= tx
            moves += 1
```

循环结束后，必然出现以下三种情形之一：

1. **恰好回到起点** `(tx, ty) == (sx, sy)` → 直接返回 `moves`。  
2. **只剩下同一行或同一列**（比如 `tx == sx`，`ty >= sy`），这时只能继续把较小坐标（`sy` 或 `sx`）一次次加上固定的 **max**（即 `sx` 或 `sy`），判断是否能整除并累加步数。  
3. **无法继续**（坐标已经小于起点或无法整除）→ 返回 `-1`。

**特殊情况**：`sx` 或 `sy` 为 `0` 时，`max` 可能为另一个坐标，需要单独判断除零错误。

> **核心技巧**：把正向“加”转化为逆向“减/模”，利用 **欧几里得算法的快速收敛**，把原本指数级的搜索压到对数级。

#### 代码（Python）

```python
def min_moves(sx: int, sy: int, tx: int, ty: int) -> int:
    # 起点即终点
    if (sx, sy) == (tx, ty):
        return 0

    # 如果起点的某个坐标已经大于目标，直接不可能
    if sx > tx or sy > ty:
        return -1

    moves = 0

    # 主循环：同时把两个坐标都大于起点时才继续
    while tx > sx and ty > sy:
        if tx > ty:
            # 大坐标是 tx
            if tx >= 2 * ty:
                # 可以一次性撤销多步
                q, r = divmod(tx, ty)
                moves += q
                tx = r
                if tx == 0:          # 防止出现 0，恢复为 ty
                    tx = ty
            else:
                tx -= ty
                moves += 1
        else:
            # 大坐标是 ty
            if ty >= 2 * tx:
                q, r = divmod(ty, tx)
                moves += q
                ty = r
                if ty == 0:
                    ty = tx
            else:
                ty -= tx
                moves += 1

    # 循环结束后，只剩下同一行或同一列的情况
    if tx == sx and ty >= sy:
        # 只能把 y 增长，每次加上 sx（此时 sx == tx）
        if sx == 0:                     # 只能在 y 方向前进，且无法改变
            return -1 if ty != sy else moves
        if (ty - sy) % sx == 0:
            moves += (ty - sy) // sx
            return moves
        return -1

    if ty == sy and tx >= sx:
        # 只能把 x 增长，每次加上 sy（此时 sy == ty）
        if sy == 0:
            return -1 if tx != sx else moves
        if (tx - sx) % sy == 0:
            moves += (tx - sx) // sy
            return moves
        return -1

    # 其他情况说明已经“跳过”起点，无法到达
    return -1
```

> **代码要点说明**  
> - `divmod(a, b)` 同时返回商 `q`（一步可以撤销多少次）和余数 `r`，避免写两行代码。  
> - 当余数为 `0` 时，说明大坐标恰好是小坐标的整数倍，此时我们把它恢复为小坐标，以免后面出现除零错误。  
> - 最后两段分别处理“只能沿 X 轴/只能沿 Y 轴前进”的特例，利用 **整除判断** 检查是否真的可以到达。

#### 复杂度

- **时间复杂度**：`O(log max(tx, ty))`。每一次循环至少把较大的坐标除以 `2`（或者更大），类似欧几里得求最大公约数的复杂度。相对于暴力的 `O(N²)`，这几乎是瞬间完成。  
- **空间复杂度**：`O(1)`，只使用了常数个整数变量。

---

## 心得

- **核心技巧**：把“正向加法”转化为“逆向减法/取模”，利用欧几里得算法的快速收敛来倒推路径。  
- **适用场景**：  
  1. “从 (a,b) 只能把较大数加到较小数上” 这类只增不减的移动问题。  
  2. “只能把一个数乘以 2 或者加上另一个数” 的变形（如 LeetCode 780、LeetCode 1547）。  
  3. 任何可以 **逆向思考、一步撤销多次** 的数论/坐标题。  
- **一句话总结**：**逆向思考 + 欧几里得取模 = 最短路径**。

---

## 反思

- **第一反应**：看到坐标只会增大，就想用 BFS 暴力搜索全部可能路径。  
- **最容易踩的坑**：  
  - 忘记处理起点或目标坐标为 `0` 的特殊情况，会导致除零错误。  
  - 在逆向循环里只减一次 `a‑b`，会让算法退化成线性时间；应当利用 “大于两倍” 的条件一次性除以。  
  - 循环结束后忘记检查同一行/列的整除条件，错误返回 `-1`。  
- **下次类似题目第一步**：**先思考是否可以逆向操作**，如果可以，把“加”变成“减/模”，再看是否能一次性批量撤销。这样往往能把指数级搜索直接压到对数级。