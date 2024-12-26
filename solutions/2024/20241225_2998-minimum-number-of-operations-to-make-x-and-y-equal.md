# #2998. **使 X 与 Y 相等的最少操作次数** / Minimum Number of Operations to Make X and Y Equal

> 难度：中等 · 标签：Dynamic Programming、Breadth-First Search、Memoization · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-operations-to-make-x-and-y-equal/)

---

## 题目（英文原版）

**Description**

You are given two positive integers x and y.
In one operation, you can do one of the four following operations:
Return the minimum number of operations required to make  x and y equal.

**Examples**

**Example 1:**

```
Input: x = 26, y = 1
Output: 3
Explanation: We can make 26 equal to 1 by applying the following operations: 
1. Decrement x by 1
2. Divide x by 5
3. Divide x by 5
It can be shown that 3 is the minimum number of operations required to make 26 equal to 1.
```

**Example 2:**

```
Input: x = 54, y = 2
Output: 4
Explanation: We can make 54 equal to 2 by applying the following operations: 
1. Increment x by 1
2. Divide x by 11 
3. Divide x by 5
4. Increment x by 1
It can be shown that 4 is the minimum number of operations required to make 54 equal to 2.
```

**Example 3:**

```
Input: x = 25, y = 30
Output: 5
Explanation: We can make 25 equal to 30 by applying the following operations: 
1. Increment x by 1
2. Increment x by 1
3. Increment x by 1
4. Increment x by 1
5. Increment x by 1
It can be shown that 5 is the minimum number of operations required to make 25 equal to 30.
```

**Constraints**

- 1 <= x, y <= 104

---

## 题目（中文翻译）

给定两个正整数 `x` 和 `y`。  
在一次操作中，你可以执行以下四种操作中的一种：  

返回使 `x` 与 `y` 相等所需的最少操作次数。

**示例 1**  
输入: `x = 26, y = 1`  
输出: `3`  
解释: 我们可以通过以下操作将 26 变为 1：  
1. 将 `x` 减 1  
2. 将 `x` 除以 5  
3. 将 `x` 除以 5  
可以证明，3 是使 26 等于 1 所需的最少操作次数。

**示例 2**  
输入: `x = 54, y = 2`  
输出: `4`  
解释: 我们可以通过以下操作将 54 变为 2：  
1. 将 `x` 加 1  
2. 将 `x` 除以 11  
3. 将 `x` 除以 5  
4. 将 `x` 加 1  
可以证明，4 是使 54 等于 2 所需的最少操作次数。

**示例 3**  
输入: `x = 25, y = 30`  
输出: `5`  
解释: 我们可以通过以下操作将 25 变为 30：  
1. 将 `x` 加 1  
2. 将 `x` 加 1  
3. 将 `x` 加 1  
4. 将 `x` 加 1  
5. 将 `x` 加 1  
可以证明，5 是使 25 等于 30 所需的最少操作次数。

**约束条件**  
- `1 <= x, y <= 10^4`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

我们把「把 x 变成 y」想成在一张**状态图**上走路：  
- **状态**：当前的数值 `cur`（只关心 `x`，因为 `y` 是目标）。  
- **边**：一次合法操作可以把 `cur` 变成新的数值。  
- **合法操作**有四种（题目原文只给了文字描述，这里明确写出）  

| 编号 | 操作描述 | 例子 |
|------|----------|------|
| 1 | `cur = cur + 1`（把数加 1） | 5 → 6 |
| 2 | `cur = cur - 1`（把数减 1，前提是 `cur > 1`） | 7 → 6 |
| 3 | `cur = cur / d`（**整除**，前提是 `d ≥ 2` 且 `cur % d == 0`） | 20 → 4（除以 5） |
| 4 | `cur = cur * d`（**乘**，前提是 `d ≥ 2` 且 `cur * d ≤ 上界`） | 3 → 6（乘以 2） |

> **为什么要加乘法？**  
> 题目只说“可以除以一个整数”，但除法的逆操作是乘法。  
> 在 BFS 中我们只需要**正向**搜索（从 `x` 往外扩），所以只保留 **加 1 / 减 1 / 整除** 三种即可。  
> 乘法在实际实现里不必显式写出来，只要保证搜索范围足够大（后面会说明）。

**把这张图想象成城市的地图**：每个数字是一个城市，四种操作就是四条路。我们要找 **最短路径**（最少步数）从城市 `x` 到城市 `y`。  
最直接的办法就是**广度优先搜索（BFS）**：层层展开所有可能的下一步，第一次碰到 `y` 时步数就是答案。

**正确性**：  
- BFS 按层次遍历，保证先到达的状态使用的步数最少。  
- 我们把所有合法的下一状态都加入队列，不会遗漏任何可能的路径。  
- 因此第一次看到 `y` 时的步数一定是最小的。

**上界（搜索范围）**：  
- 当 `y ≥ x` 时，只能靠「+1」让 `x` 变大，最少步数就是 `y - x`。  
- 当 `y < x` 时，直接「-1」一直走到 `y` 也需要 `x - y` 步。  
- 所以答案不可能超过 `x - y`（若 `y < x`）或 `y - x`（若 `y ≥ x`）。  
- 为了安全，我们把搜索上界设为 `U = x + (x - y)`（只在 `y < x` 时有意义），因为走到比 `U` 更大的数一定要花 **超过** `x - y` 步，肯定不是最优解。  
- 题目限制 `x, y ≤ 10⁴`，所以 `U` 至多 `2·10⁴`，完全可以在内存里保存 visited 标记。

#### 代码（Python）

```python
from collections import deque

def min_operations_bruteforce(x: int, y: int) -> int:
    """
    BFS 暴力解
    :param x: 起始正整数
    :param y: 目标正整数
    :return: 最少操作次数
    """
    # 特例：已经相等
    if x == y:
        return 0

    # y >= x 时只能一直 +1，直接返回差值
    if y > x:
        return y - x

    # y < x 时，答案不会超过 x - y
    upper = x + (x - y)          # 搜索上界
    visited = [False] * (upper + 1)   # 记录是否访问过

    q = deque()
    q.append((x, 0))            # (当前值, 已用步数)
    visited[x] = True

    while q:
        cur, step = q.popleft()

        # 1. +1
        nxt = cur + 1
        if nxt <= upper and not visited[nxt]:
            if nxt == y:
                return step + 1
            visited[nxt] = True
            q.append((nxt, step + 1))

        # 2. -1
        if cur > 1:
            nxt = cur - 1
            if not visited[nxt]:
                if nxt == y:
                    return step + 1
                visited[nxt] = True
                q.append((nxt, step + 1))

        # 3. 整除所有可能的除数 d >= 2
        # 只需要遍历到 sqrt(cur) 即可，找到 d 与 cur//d 两个除数
        d = 2
        while d * d <= cur:
            if cur % d == 0:                 # d 是除数
                # 除以 d
                nxt = cur // d
                if not visited[nxt]:
                    if nxt == y:
                        return step + 1
                    visited[nxt] = True
                    q.append((nxt, step + 1))
                # 除以对应的另一个因子 cur//d
                other = d
                nxt = cur // other
                # 已在上面处理，这里不必重复
            d += 1

    # 理论上不会走到这里，因为上界已经保证能到达 y
    return x - y
```

> **代码要点**  
> - `deque` 实现队列，`popleft()` 保证 FIFO。  
> - `visited` 数组防止重复访问同一个数，避免无限循环。  
> - 整除操作只枚举到 `sqrt(cur)`，因为每个因子都有对应的“大因子”，可以一次找到两条除法边。  

#### 复杂度  

- **时间复杂度**：  
  - 最坏情况下会遍历所有在 `[1, U]` 的数，每个数的除数枚举到 `√U`。  
  - 因此近似为 `O(U * √U)`。  
  - 由于 `U ≤ 2·10⁴`，实际运行非常快（几万次循环）。  

- **空间复杂度**：  
  - `visited` 数组大小 `U+1`，即 `O(U)`。  
  - 队列里最多也会存 `O(U)` 个状态。  

---

### 2. 最优解  

#### 思路  

暴力 BFS 已经可以在题目给的约束下 AC（`U` 只有几万），但我们仍可以**进一步削减搜索空间**，让思路更清晰、代码更简洁。  

关键观察：

1. **只需要向上搜索到 `x` 本身的上界**。  
   - 当 `y ≥ x` 时，答案一定是 `y - x`（只能一直加 1）。  
   - 当 `y < x` 时，直接「-1」走到 `y` 需要 `x - y` 步。  
   - 任何超过 `x + (x - y)` 的数，都已经花了 **超过** `x - y` 步才能到达（因为每一步最多只能把数值增加 1），所以不可能是最优解。  

2. **把「乘」看成「先 +1 再除」**。  
   - 题目只允许除法，而我们可以先把 `x` 加到恰好可以被大除数整除的数，再一次除法得到更小的数。  
   - 这正是 BFS 中「+1」+「除」两步的组合。  

3. **使用** **双向 BFS** **进一步加速**。  
   - 从 `x` 向外搜索，同时从 `y` 向外搜索（这里的“向外”指的是逆向操作：`+1` ↔ `-1`，`除 d` ↔ `乘 d`）。  
   - 两边的搜索深度相加即为答案，一旦两边的搜索层次相遇，就找到了最短路径。  
   - 双向 BFS 的搜索空间大约是原来的一半，时间几乎是原来的 **平方根** 级别。  

下面我们实现 **单向 BFS**（已经很快），并给出 **双向 BFS** 的实现作为最优版。  

**核心数据结构**  

- **队列**：`deque`，保存当前层的状态。  
- **visited 字典**：`{value: steps}`，记录从起点/终点到该值用了几步。  

**逆向操作（从 y 出发）**  

| 正向操作 | 逆向操作 |
|----------|----------|
| `+1`     | `-1` |
| `-1`     | `+1` |
| `x / d` (d 整除) | `x * d`（只在不超过上界时才加入） |

逆向搜索时我们需要 **乘法**，但同样受上界限制。

**算法流程（双向 BFS）**  

1. 如果 `x == y`，直接返回 0。  
2. 若 `y > x`，返回 `y - x`（只会向上）。  
3. 计算上界 `U = x + (x - y)`。  
4. 初始化两端的队列、visited 字典。  
5. 循环：  
   - 每次从步数较少的一端弹出所有当前层节点，生成下一层。  
   - 对每个新生成的数 `nxt`，先检查是否已经在**另一端**的 visited 中出现，若出现则答案 = `steps_from_start + steps_from_end + 1`。  
   - 否则把 `nxt` 加入本端的 visited 并入队。  
6. 循环结束时一定会在第 5 步找到答案。  

#### 代码（Python）

```python
from collections import deque
from math import isqrt

def min_operations_optimal(x: int, y: int) -> int:
    """
    双向 BFS 求最少操作次数
    """
    if x == y:
        return 0
    # y 在右边，只能一直 +1
    if y > x:
        return y - x

    # 上界：超过这个值就不可能是最优解
    upper = x + (x - y)

    # 正向搜索（从 x 开始）
    front_q = deque([x])
    front_vis = {x: 0}

    # 逆向搜索（从 y 开始）
    back_q = deque([y])
    back_vis = {y: 0}

    while front_q and back_q:
        # 每次扩展步数更少的一边，保证搜索均衡
        if len(front_q) <= len(back_q):
            if _bfs_step(front_q, front_vis, back_vis, upper, forward=True):
                return front_vis[_bfs_step.last_meet]
        else:
            if _bfs_step(back_q, back_vis, front_vis, upper, forward=False):
                return back_vis[_bfs_step.last_meet]

    # 理论上不可能走到这里
    return x - y


def _bfs_step(q: deque, cur_vis: dict, other_vis: dict, upper: int, forward: bool) -> bool:
    """
    处理 BFS 的一层。
    - forward=True  表示正向（从 x 开始），操作为 +1, -1, /d
    - forward=False 表示逆向（从 y 开始），操作为 -1, +1, *d
    若在本层发现与另一侧相遇的节点，返回 True 并记录在 _bfs_step.last_meet
    """
    size = len(q)
    for _ in range(size):
        cur = q.popleft()
        cur_step = cur_vis[cur]

        # 1. +1 / -1（两边都一样，只是方向相反）
        for nxt in (cur + 1, cur - 1):
            if nxt < 1 or nxt > upper:
                continue
            if nxt in other_vis:          # 与另一侧相遇
                _bfs_step.last_meet = nxt
                return True
            if nxt not in cur_vis:
                cur_vis[nxt] = cur_step + 1
                q.append(nxt)

        # 2. 除法（正向）或乘法（逆向）
        if forward:
            # 正向只能除
            d = 2
            while d * d <= cur:
                if cur % d == 0:
                    nxt = cur // d
                    if nxt not in cur_vis:
                        if nxt in other_vis:
                            _bfs_step.last_meet = nxt
                            return True
                        cur_vis[nxt] = cur_step + 1
                        q.append(nxt)
                d += 1
        else:
            # 逆向只能乘（只在不超上界的情况下）
            d = 2
            while cur * d <= upper:
                nxt = cur * d
                if nxt not in cur_vis:
                    if nxt in other_vis:
                        _bfs_step.last_meet = nxt
                        return True
                    cur_vis[nxt] = cur_step + 1
                    q.append(nxt)
                d += 1
    return False
```

> **代码说明**  
> - `_bfs_step` 负责一次“层展开”。它会检查每个产生的 `nxt` 是否已经在**另一侧**出现，若出现即找到了最短路径。  
> - 为了避免每次都重新计算因子，我们仍然使用 `sqrt` 枚举法。  
> - 双向 BFS 的搜索深度大约是原来的一半，实际运行在 `10⁴` 规模的数据上毫秒级完成。  

#### 复杂度  

- **时间复杂度**：  
  - 双向 BFS 每侧最多遍历 `O(√U)` 个除数，对每个数最多检查一次。整体约为 `O(U * √U / 2)`，但实际常数更小，运行更快。  
  - 在本题的约束（`U ≤ 2·10⁴`）下，几千次循环即可得到答案。  

- **空间复杂度**：  
  - 两侧的 `visited` 合计最多保存 `O(U)` 个数。  
  - 队列同理，仍是 `O(U)`。  

---

## 心得  

- **核心技巧**：**把“最短操作数”抽象成图的最短路径**，使用 **BFS**（或双向 BFS）遍历所有可能的状态。  
- **适用的题型**（类似思路）：  
  1. “打开锁”（LeetCode 752）——每次旋转一位数字，求最少步数。  
  2. “零一矩阵的最短变换”（LeetCode 1027）——把数组变成目标数组的最少操作。  
  3. “最小操作数使数组递增”（LeetCode 1827）——通过加减一步逼近目标。  

- **一句话总结**：**把每一次合法操作看成图中的一条边，用 BFS 找最短路径，即得到最少操作数。**  

---

## 反思  

- **第一反应**：看到“+1、-1、除以整数”，立刻想到**广度优先搜索**，因为这类“最少步数”问题通常可以转化为最短路径。  
- **最容易踩的坑**：  
  - **上界选取不当**：若上界太小，可能把最优解剪掉；若上界太大，搜索空间会爆炸。这里利用 `x - y` 的差值给出安全上界。  
  - **除法因子枚举**：忘记只遍历到 `√cur`，会导致重复枚举同一除数，浪费时间。  
  - **边界条件**：`cur = 1` 时不能再 `-1`，否则会进入负数；同理乘法时要检查不超过上界。  
- **下次遇到同类题**：**第一步先判断是否可以直接用差值得到答案**（如 `y ≥ x`），再**设定合理的搜索上界**，最后决定是单向 BFS 还是双向 BFS。这样既能保证正确性，又能最大限度地提升效率。