# #2849. 判断在给定时间是否能到达指定单元格 / Determine if a Cell Is Reachable at a Given Time

> 难度：中等 · 标签：Math · [LeetCode 链接](https://leetcode.com/problems/determine-if-a-cell-is-reachable-at-a-given-time/)

---

## 题目（英文原版）

**Description**

You are given four integers sx, sy, fx, fy, and a non-negative integer t.
In an infinite 2D grid, you start at the cell (sx, sy). Each second, you must move to any of its adjacent cells.
Return true if you can reach cell (fx, fy) after exactly t seconds, or false otherwise.
A cell's adjacent cells are the 8 cells around it that share at least one corner with it. You can visit the same cell several times.

**Examples**

**Example 1:**

```
Input: sx = 2, sy = 4, fx = 7, fy = 7, t = 6
Output: true
Explanation: Starting at cell (2, 4), we can reach cell (7, 7) in exactly 6 seconds by going through the cells depicted in the picture above.
```

**Example 2:**

```
Input: sx = 3, sy = 1, fx = 7, fy = 3, t = 3
Output: false
Explanation: Starting at cell (3, 1), it takes at least 4 seconds to reach cell (7, 3) by going through the cells depicted in the picture above. Hence, we cannot reach cell (7, 3) at the third second.
```

**Constraints**

- 1 <= sx, sy, fx, fy <= 109
- 0 <= t <= 109

---

## 题目（中文翻译）

给定四个整数 `sx`、`sy`、`fx`、`fy`，以及一个非负整数 `t`。  
在一个无限的二维网格（grid）中，你从单元格 `(sx, sy)` 开始。每秒钟，你必须移动到它的任意一个相邻单元格（adjacent cells）。  

返回 `true` 当且仅当你能够在恰好 `t` 秒后到达单元格 `(fx, fy)`；否则返回 `false`。  
相邻单元格指的是与当前单元格共享至少一个角的 8 个单元格。你可以多次访问同一个单元格。

## 示例

### 示例 1
**输入**: `sx = 2, sy = 4, fx = 7, fy = 7, t = 6`  
**输出**: `true`  
**解释**: 从单元格 `(2, 4)` 出发，经过 6 秒后可以到达单元格 `(7, 7)`，路径如图所示。

### 示例 2
**输入**: `sx = 3, sy = 1, fx = 7, fy = 3, t = 3`  
**输出**: `false`  
**解释**: 从单元格 `(3, 1)` 出发，至少需要 4 秒才能到达单元格 `(7, 3)`，因此在第 3 秒时无法到达。

## 约束条件
- `1 <= sx, sy, fx, fy <= 10^9`
- `0 <= t <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的走法都枚举出来**，看看在第 `t` 秒有没有走到目标格子。  
我们可以把每一步看成在 **八个方向**（上、下、左、右以及四个对角）中的一次移动，就像在棋盘上随意走国王一样。

实现上常用 **广度优先搜索（BFS）**：

1. 把起点 `(sx, sy)` 放进队列，记下已经走了 0 步。  
2. 每次从队列里弹出一个位置 `(x, y, step)`，如果 `step == t` 并且 `(x, y) == (fx, fy)`，说明找到了答案。  
3. 否则把它的 8 个相邻格子 `(x+dx[i], y+dy[i])`（`dx, dy` 分别是 `[-1,0,1]` 的组合）连同 `step+1` 一起加入队列，继续搜索。  

> **类比**：想象你在城市的十字路口，每秒可以向任意相邻的 8 条街道走去。要判断第 `t` 秒能否恰好站在某个特定的十字路口，就要把所有可能的行走路线画出来，然后看有没有一条正好在第 `t` 步到达。

这种方法一定能得到正确答案，因为它把**所有**合法路径都遍历了一遍。

#### 代码（Python）

```python
from collections import deque

def reachable_bruteforce(sx: int, sy: int, fx: int, fy: int, t: int) -> bool:
    # 八个方向的偏移量
    dirs = [(-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)]

    # 队列里保存 (x, y, 已经走的步数)
    q = deque()
    q.append((sx, sy, 0))

    while q:
        x, y, step = q.popleft()
        # 已经走够 t 步，检查是否恰好在目标格子
        if step == t:
            if x == fx and y == fy:
                return True
            continue                # 已经走满 t 步但不在目标，剪枝

        # 仍有剩余步数，向 8 个相邻格子继续扩展
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            q.append((nx, ny, step + 1))

    # 队列耗尽仍未找到答案
    return False
```

> **注意**：这里没有做任何剪枝或记忆化，所有可能的走法都会被展开。

#### 复杂度  

- **时间复杂度**：`O(8^t)`  
  每一步都有 8 种选择，`t` 步后会产生 `8^t` 条路径。  
  用大白话说，就是如果 `t=5`，我们要检查 `8·8·8·8·8 = 32768` 条路线；`t` 再大一点，数量会天文增长。

- **空间复杂度**：`O(8^t)`（队列最坏情况下会同时保存同一层的所有节点）  

> 由于 `t` 最多可以到 `10^9`，显然暴力 BFS 完全不可行，只能作为**思考起点**。

---

### 2. 最优解

#### 思路  

从暴力解可以看到：**真正的难点不在于“怎么走”，而在于判断是否存在一种走法**。  
我们不需要真的走出来，只要了解**最少需要多少步**以及**多余的步数如何消耗**，就能直接判断。

**关键观察 1：最少步数 = Chebyshev 距离**  

在每秒可以向任意相邻格子（包括对角）移动的情况下，横向和纵向的距离可以同时缩短（走对角），所以从 `(sx, sy)` 到 `(fx, fy)` 的**最少步数**是  

```
minDist = max(|fx - sx|, |fy - sy|)
```

这叫 **Chebyshev 距离**，就像在国际象棋里国王走到另一格最少需要的步数。

**关键观察 2：多余的步数可以随意消耗**  

一旦到达目标格子，我们仍然可以“原地浪费”时间：

- 走一步离开目标，再走一步返回（两步消耗）。  
- 甚至可以用三步返回（如示例 `(0,0)->(1,0)->(1,1)->(0,0)`），所以**只要多余的步数 ≥ 2**，我们总能把它们“消耗掉”。  

唯一的例外是 **起点已经是目标且只剩 1 步**：  
- 这时必须走出再走回来，但只有 1 步根本不可能回到原点。  

**综合判断**  

1. 如果 `t < minDist` → 连最短路径都走不完，答案 `False`。  
2. 否则，只有一种特殊情况会失败：`(sx, sy) == (fx, fy)` 且 `t == 1`（只能走一步，必然离开起点）。  
3. 其余情况全部成立 → `True`。

这就是 **O(1)** 的判断方法。

#### 代码（Python）

```python
def reachable(sx: int, sy: int, fx: int, fy: int, t: int) -> bool:
    """
    判断是否能在恰好 t 秒后到达 (fx, fy)。
    思路：先算 Chebyshev 距离，再检查特殊情况。
    """
    # 1️⃣ 计算横纵坐标的绝对差
    dx = abs(fx - sx)
    dy = abs(fy - sy)

    # 2️⃣ 最少需要的步数 = 两者的最大值
    min_dist = max(dx, dy)

    # 3️⃣ 不能比最少步数更快到达
    if t < min_dist:
        return False

    # 4️⃣ 唯一的“卡死”情形：已经在目标格子，却只能走 1 步
    if sx == fx and sy == fy and t == 1:
        return False

    # 5️⃣ 其它全部可以通过往返或绕路消耗多余的时间
    return True
```

#### 复杂度  

- **时间复杂度**：`O(1)`  
  只做了几次整数运算和比较，和 `t` 的大小毫无关系。  
  相比暴力的指数级别，简直是“一瞬间算完”。

- **空间复杂度**：`O(1)`  
  只用了常数个变量，不会随输入规模增长。

---

## 心得

- **核心技巧**：把二维格子移动抽象成 **Chebyshev 距离**（国王步）+ **多余步数的消耗**。  
- **适用的题型**  
  1. 任意方向（含对角）移动的最短路径问题。  
  2. “恰好用 k 步到达” 类型的可达性判断（如“骑士在 k 步后是否能回到原点”）。  
  3. 需要判断 **是否可以在给定步数内完成** 的路径规划问题（常见在游戏或机器人移动中）。  
- **一句话总结**：只要目标距离 ≤ 时间，并且不是“已经在目标只能走一步”这唯一的特例，就一定能到达。

---

## 反思

- **第一反应**：先想到 BFS，想把所有走法枚举出来。  
- **最容易踩的坑**  
  - 忽略了对角线一次可以同时缩短横纵距离，导致错误地使用 Manhattan 距离。  
  - 没考虑 **t = 0** 的情况（起点即是终点时应返回 `True`）。  
  - 错误地以为多余的步数必须是偶数才行，实际上只要有 2 步以上的“往返”就能消耗任意多余步数。  
- **下次思路**：一看到“每秒可以向任意相邻格子移动”，第一步就想到 **Chebyshev 距离**，再判断 **时间是否足够**，最后检查 **是否有只能走一步的特殊情况**。这样可以直接得到 O(1) 的答案。