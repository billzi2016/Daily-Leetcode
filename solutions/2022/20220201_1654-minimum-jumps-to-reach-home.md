# #1654. 到达家园的最小跳跃次数 / Minimum Jumps to Reach Home

> 难度：中等 · 标签：Array、Dynamic Programming、Breadth-First Search · [LeetCode 链接](https://leetcode.com/problems/minimum-jumps-to-reach-home/)

---

## 题目（英文原版）

**Description**

A certain bug's home is on the x-axis at position x. Help them get there from position 0.
The bug jumps according to the following rules:
The bug may jump forward beyond its home, but it cannot jump to positions numbered with negative integers.
Given an array of integers forbidden, where forbidden[i] means that the bug cannot jump to the position forbidden[i], and integers a, b, and x, return the minimum number of jumps needed for the bug to reach its home. If there is no possible sequence of jumps that lands the bug on position x, return -1.

**Examples**

**Example 1:**

```
Input: forbidden = [14,4,18,1,15], a = 3, b = 15, x = 9
Output: 3
Explanation: 3 jumps forward (0 -> 3 -> 6 -> 9) will get the bug home.
```

**Example 2:**

```
Input: forbidden = [8,3,16,6,12,20], a = 15, b = 13, x = 11
Output: -1
```

**Example 3:**

```
Input: forbidden = [1,6,2,14,5,17,4], a = 16, b = 9, x = 7
Output: 2
Explanation: One jump forward (0 -> 16) then one jump backward (16 -> 7) will get the bug home.
```

**Constraints**

- 1 <= forbidden.length <= 1000
- 1 <= a, b, forbidden[i] <= 2000
- 0 <= x <= 2000
- All the elements in forbidden are distinct.
- Position x is not forbidden.

---

## 题目（中文翻译）

某只虫子的家位于 x 轴的坐标 `x` 处。帮助它从位置 `0` 前往家。

虫子的跳跃规则如下：

- 每次可以向前跳 `a` 步，或向后跳 `b` 步。  
- 虫子可以向前跳超出家所在的位置，但**不能**跳到负整数坐标。  
- 给定整数数组 `forbidden`（forbidden），其中 `forbidden[i]` 表示虫子 **不能** 跳到的位置 `forbidden[i]`。  

给定整数 `a`、`b`、`x`，返回虫子到达家所需的最少跳跃次数。如果不存在任何跳跃序列能够让虫子恰好落在位置 `x`，返回 `-1`。

## 示例

### 示例 1
**输入**  
`forbidden = [14,4,18,1,15], a = 3, b = 15, x = 9`  
**输出**  
`3`  
**解释**  
向前跳三次 `0 -> 3 -> 6 -> 9` 即可到达家。

### 示例 2
**输入**  
`forbidden = [8,3,16,6,12,20], a = 15, b = 13, x = 11`  
**输出**  
`-1`

### 示例 3
**输入**  
`forbidden = [1,6,2,14,5,17,4], a = 16, b = 9, x = 7`  
**输出**  
`2`  
**解释**  
先向前跳一次 `0 -> 16`，再向后跳一次 `16 -> 7` 即可到达家。

## 约束条件

- `1 <= forbidden.length <= 1000`
- `1 <= a, b, forbidden[i] <= 2000`
- `0 <= x <= 2000`
- `forbidden` 中的所有元素互不相同
- 位置 `x` 不在 `forbidden` 中

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的跳跃序列**，找出能恰好落在目标位置 `x` 的最短序列。  
可以把这条数轴看成一张**无向图**：  
- 每个整数位置（非负）是一个节点。  
- 从节点 `p` 可以往前跳 `a` 步到 `p + a`，也可以往后跳 `b` 步到 `p - b`（前提是 `p - b ≥ 0`）。  
- 但如果某个位置在 `forbidden` 中，就把对应的节点删掉，不能进入。  

暴力做法就是**深度优先搜索（DFS）**所有可能的路径，记录最短的跳数。  
- 用递归或显式栈保存当前所在位置、已经跳了多少次、以及上一次是否是向后跳（因为题目要求**不能连续向后跳两次**）。  
- 每次尝试两种跳法：向前 `+a`、向后 `-b`（满足非负且不在 forbidden 中）。  
- 为了防止无限循环，需要用一个 `visited` 集合记住已经访问过的 `(位置, 上一次是否向后)` 状态。  

**为什么正确**  
DFS 会遍历所有合法的跳跃序列，只要序列能够到达 `x`，必定会在搜索过程中被发现。因为我们用 `visited` 防止重复访问，同一状态不会被无限重复进入，从而搜索是有限的。

**时间/空间复杂度（大白话）**  
- 设最大可能访问的状态数为 `N`（每个位置最多两种“上一次是否向后”状态），暴力 DFS 在最坏情况下会遍历所有状态。  
- 时间复杂度 **O(N)**，这里的 `N` 可能非常大（因为位置可以往前无限跳），在最坏情况下会接近指数级，实际会超时。  
- 空间复杂度 **O(N)**，主要是递归栈和 `visited` 集合的大小。  

> 大白话：如果把 `N` 想象成“可能出现的格子数量”，时间 O(N) 就是“要走遍每一个格子一次”。但这里的格子数可能是几千甚至几万，暴力遍历会非常慢。

#### 代码（Python）

```python
from typing import List, Set, Tuple

def minimum_jumps_bruteforce(forbidden: List[int], a: int, b: int, x: int) -> int:
    forbidden_set: Set[int] = set(forbidden)
    # (位置, 上一次是否向后跳) 组成的状态，用来防止重复访问
    visited: Set[Tuple[int, bool]] = set()
    best = float('inf')          # 记录找到的最小跳数

    def dfs(pos: int, steps: int, last_backward: bool) -> None:
        nonlocal best
        # 剪枝：已经比已知最优解更差，就不继续搜索
        if steps >= best:
            return
        # 到达目标
        if pos == x:
            best = steps
            return
        # 记录当前状态，防止以后再来
        if (pos, last_backward) in visited:
            return
        visited.add((pos, last_backward))

        # ---- 向前跳 ----
        nxt_forward = pos + a
        if nxt_forward not in forbidden_set:          # 不能是禁区
            dfs(nxt_forward, steps + 1, False)       # 向前跳后，标记上一次不是向后

        # ---- 向后跳（只能在上一次不是向后时）----
        if not last_backward:                         # 不能连续两次向后
            nxt_backward = pos - b
            if nxt_backward >= 0 and nxt_backward not in forbidden_set:
                dfs(nxt_backward, steps + 1, True)   # 向后跳后，标记上一次是向后

    dfs(0, 0, False)   # 从原点出发，步数 0，上一跳不是向后
    return -1 if best == float('inf') else best
```

#### 复杂度  

- **时间复杂度**：O(N)（N 为所有可能状态的数量），但因为 `N` 可能非常大，实际会超时。  
- **空间复杂度**：O(N) 用于保存 `visited` 集合和递归栈。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**搜索所有状态**是必须的，但我们可以用**更合适的遍历方式**来保证每个状态只访问一次，并且不必去递归深层次的路径。  
这正好对应**广度优先搜索（BFS）**的思路：  

1. **把每个合法的 (位置, 是否刚才向后) 当作图的节点**。  
2. **从起点 (0, False) 开始**，每一次扩展一次“层”，即一次跳。  
3. 当我们第一次把目标位置 `x` 出现在队列里时，当前层数就是**最少跳数**（BFS 的最短路特性）。  

**关键难点**  
- **不能连续向后跳**：我们需要在状态里记住“上一次是否向后”。因此每个位置会有两种可能的状态：`(pos, False)`（上一次是向前或是起点）和 `(pos, True)`（上一次是向后）。  
- **搜索范围的上界**：如果一直向前跳，理论上位置可以无限大。实际上，题目限制 `a, b, forbidden[i] ≤ 2000`，且 `x ≤ 2000`。  
  - 向前最多会超过 `x` 一段距离后再向后回来。已知最优路径不会超过 `max_limit = max(forbidden) + a + b + x`（一个安全上界），常取 `2000 + a + b` 或 `6000`。这里取 `limit = 6000`，足够覆盖所有可能的最优路径，又不会让搜索无限。  

**整体步骤**  

| 步骤 | 说明 |
|------|------|
| 初始化 | 用 `deque` 保存 BFS 队列，放入起点 `(0, False)`，步数 `0`。 |
| 访问标记 | `visited = set()`，存 `(pos, last_backward)`，防止重复入队。 |
| 循环 | 当队列不空时弹出当前状态，若 `pos == x` 返回当前步数。 |
| 扩展 | - **向前跳**：`next = pos + a`，如果 `next` 不在 forbidden 且 `next ≤ limit`，入队 `(next, False)`。<br>- **向后跳**：仅当 `last_backward == False`，计算 `next = pos - b`，若 `next ≥ 0` 且不在 forbidden，入队 `(next, True)`。 |
| 结束 | 若 BFS 完成仍未到达 `x`，返回 `-1`。 |

**为什么是最优**  
- BFS 按层遍历，先到达目标的路径必然是最少跳数。  
- 通过状态 `(pos, last_backward)` 完全捕获了“不能连续向后”的限制，保证搜索的合法性。  
- 使用 `visited` 防止同一状态重复入队，保证每个状态只被处理一次，时间线性于状态数。  

#### 代码（Python）

```python
from collections import deque
from typing import List, Set, Tuple

def minimum_jumps(forbidden: List[int], a: int, b: int, x: int) -> int:
    """
    BFS 解法
    :param forbidden: 禁止到达的整数位置列表
    :param a: 向前跳的步长
    :param b: 向后跳的步长
    :param x: 目标位置
    :return: 最少跳数，若不可达返回 -1
    """
    forbidden_set: Set[int] = set(forbidden)

    # 为防止无限向前，我们设一个合理的上界
    # 经验上取 6000 足以覆盖所有情况（2000 + a + b + x <= 6000）
    LIMIT = 6000

    # BFS 队列里保存 (当前位置, 上一次是否向后, 已跳次数)
    q: deque[Tuple[int, bool, int]] = deque()
    q.append((0, False, 0))

    visited: Set[Tuple[int, bool]] = set()
    visited.add((0, False))

    while q:
        pos, last_backward, steps = q.popleft()

        # 到达目标，直接返回步数
        if pos == x:
            return steps

        # ---------- 向前跳 ----------
        nxt_forward = pos + a
        if nxt_forward <= LIMIT and nxt_forward not in forbidden_set:
            state = (nxt_forward, False)          # 向前后，下一次可以向后
            if state not in visited:
                visited.add(state)
                q.append((nxt_forward, False, steps + 1))

        # ---------- 向后跳 ----------
        # 只能在上一次不是向后时才可以向后
        if not last_backward:
            nxt_backward = pos - b
            if nxt_backward >= 0 and nxt_backward not in forbidden_set:
                state = (nxt_backward, True)       # 向后后，下一次不能再向后
                if state not in visited:
                    visited.add(state)
                    q.append((nxt_backward, True, steps + 1))

    # BFS 结束仍未到达 x，说明不可达
    return -1
```

#### 复杂度  

- **时间复杂度**：`O(N)`，其中 `N` 为所有可能状态的数量。  
  - 位置的上界设为 `LIMIT ≈ 6000`，每个位置最多两种状态（是否刚向后），所以 `N ≤ 2 * LIMIT ≈ 12000`。  
  - 因此实际运行时间非常快，远低于暴力递归的指数级。  

- **空间复杂度**：`O(N)` 用于存 `visited` 集合和 BFS 队列，同样最多约 12000 条记录，完全可接受。  

> 与暴力解相比，BFS 只遍历一次每个合法状态，不会出现深度递归导致的栈溢出，也避免了大量重复搜索，速度提升几个数量级。

---

## 心得  

- **核心技巧**：把“一维跳跃问题”抽象成**带状态的图**，利用 **广度优先搜索（BFS)** 求最短路径。  
- **适用场景**：  
  1. 需要在有限状态空间中寻找最少操作次数的题目（如“打开锁”“最短变换序列”）。  
  2. 带有**额外约束**（如不能连续某类操作、只能向前/向后）时，需要在状态里记录约束信息。  
- **一句话总结**：**把每一步的“位置+上一步是否向后”当作节点，BFS 一层层展开，即可得到最少跳数**。

---

## 反思  

- **第一反应**：看到“跳”“禁止位置”“不能连续后跳”，立刻想到把问题建模成图，然后搜索最短路径。  
- **最容易踩的坑**：  
  - **无限向前**：若不设上界，BFS 可能会把队列推向无穷大导致内存爆炸。  
  - **状态重复**：只记录位置不记录“上一次是否向后”会导致非法的连续后跳被误认为合法，或者产生无限循环。  
  - **边界条件**：向后跳必须保证 `pos - b >= 0`，否则会进入负数位置。  
- **下次类似题的第一步**：先**明确状态定义**（哪些信息需要保存在节点上），再决定是 **BFS**（求最少步数）还是 **DFS/DP**（求最大/计数）。这样可以一次性把约束写进状态，避免后期纠错。