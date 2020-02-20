# #780. 到达终点 / Reaching Points

> 难度：困难 · 标签：Math · [LeetCode 链接](https://leetcode.com/problems/reaching-points/)

---

## 题目（英文原版）

**Description**

Given four integers sx, sy, tx, and ty, return true if it is possible to convert the point (sx, sy) to the point (tx, ty) through some operations, or false otherwise.
The allowed operation on some point (x, y) is to convert it to either (x, x + y) or (x + y, y).

**Examples**

**Example 1:**

```
Input: sx = 1, sy = 1, tx = 3, ty = 5
Output: true
Explanation:
One series of moves that transforms the starting point to the target is:
(1, 1) -> (1, 2)
(1, 2) -> (3, 2)
(3, 2) -> (3, 5)
```

**Example 2:**

```
Input: sx = 1, sy = 1, tx = 2, ty = 2
Output: false
```

**Example 3:**

```
Input: sx = 1, sy = 1, tx = 1, ty = 1
Output: true
```

**Constraints**

- 1 <= sx, sy, tx, ty <= 109

---

## 题目（中文翻译）

给定四个整数 `sx`、`sy`、`tx` 和 `ty`，如果可以通过若干次操作将点 `(sx, sy)` 转换为点 `(tx, ty)`，则返回 `true`；否则返回 `false`。  

对任意点 `(x, y)`，允许的操作有两种：将其转换为 `(x, x + y)` 或 `(x + y, y)`。

**示例 1**  
**示例 2**  
**示例 3**  

**约束条件**  

- `1 <= sx, sy, tx, ty <= 10^9`

---

### 示例

**示例 1**  
```text
Input: sx = 1, sy = 1, tx = 3, ty = 5
Output: true
```
**解释**：  
一种将起始点转化为目标点的操作序列如下：  
`(1, 1) -> (1, 2)`  
`(1, 2) -> (3, 2)`  
`(3, 2) -> (3, 5)`

**示例 2**  
```text
Input: sx = 1, sy = 1, tx = 2, ty = 2
Output: false
```

**示例 3**  
```text
Input: sx = 1, sy = 1, tx = 1, ty = 1
Output: true
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**从起点 (sx, sy) 按题目给出的两种操作一直往前搜索**，看能否恰好到达目标 (tx, ty)。  
- 每一次操作要么把 `x` 不变、把 `y` 加上 `x` → `(x, x+y)`；  
- 要么把 `y` 不变、把 `x` 加上 `y` → `(x+y, y)`。  

这相当于在一棵二叉树里做深度优先搜索（DFS）或广度优先搜索（BFS），树的根是起点，向下的每一层都是一次合法的移动。

> **类比**：想象你在一条只能往前走的楼梯，每走一步你可以把左脚（x）往前跨 y 步，或者把右脚（y）往前跨 x 步。要判断能否恰好站到目标台阶。

只要在搜索过程中出现了 `(tx, ty)`，说明可以到达；如果搜索的坐标已经超过目标的任意一维（比如 `x > tx` 或 `y > ty`），就可以剪枝，因为后面的操作只能让坐标继续增大，永远不可能再回到目标。

#### 代码（Python）

```python
def reachingPoints_brute(sx: int, sy: int, tx: int, ty: int) -> bool:
    # 使用栈模拟深度优先搜索
    stack = [(sx, sy)]
    visited = set()                 # 防止同一个点被重复访问

    while stack:
        x, y = stack.pop()
        # 若已经到达目标，返回 True
        if x == tx and y == ty:
            return True
        # 超过目标的点不再继续扩展（剪枝）
        if x > tx or y > ty:
            continue
        # 防止无限循环
        if (x, y) in visited:
            continue
        visited.add((x, y))

        # 两种合法的下一步
        stack.append((x + y, y))   # 把 x 加上 y
        stack.append((x, x + y))   # 把 y 加上 x
    return False
```

> **关键行解释**  
> - `if x > tx or y > ty:`：一旦坐标超过目标，就没有回头的操作，只会继续增大，直接丢弃。  
> - `visited` 集合：防止像 `(2,2)` 这样可以循环返回自身的情况导致死循环。

#### 复杂度

- **时间复杂度**：`O(2^{k})`（指数级），其中 `k` 是从起点到目标需要的步数。因为每一步都会产生两个分支，搜索树会指数增长。实际运行时会因为剪枝稍微好点，但最坏情况仍然是指数级。  
- **空间复杂度**：`O(2^{k})`，栈/队列里最多同时保存的节点数同样呈指数增长。

> **大白话**：想象你在森林里每走一步都要分两条路，走到第 20 步就会有 `2^20 ≈ 1,000,000` 条不同的路径需要检查，根本不可能在合理时间内完成。

---

### 2. 最优解

#### 思路  

暴力搜索太慢的根源在于**我们一直往前搜索**，每一步都产生两条分支，导致指数爆炸。  
观察题目可以发现，**每一次操作都是把较小的数加到较大的数上**，于是坐标始终保持 **非递减**（`x` 与 `y` 只会增大）。这暗示我们可以尝试 **从目标倒着走**，把大的数减去小的数，逐步回到起点。

> **关键观察**  
> - 若 `(x, y)` 能到达 `(tx, ty)`，则在逆向操作中，`tx` 与 `ty` 必须始终大于等于 `sx`、`sy`。  
> - 逆向唯一合法的操作是：  
>   - 如果 `tx > ty`，则上一步一定是 `(tx - ty, ty)`（因为正向只能把 `x` 加上 `y`），  
>   - 如果 `ty > tx`，则上一步一定是 `(tx, ty - tx)`。  
> - 当两数相差很大时，一次减去一次 `y`（或 `x`）会非常慢。**利用取模**：`tx % ty` 相当于一次性把 `tx` 减去若干个 `ty`，只要 `tx` 仍然大于 `sx`，我们就可以直接跳到 `tx % ty`。  

**倒推过程**：

1. 当 `tx == sx` 且 `ty >= sy` 时，只能让 `ty` 逐步减去 `sx`（即 `ty % sx`），如果最后恰好等于 `sy`，说明可达。  
2. 同理，当 `ty == sy` 且 `tx >= sx` 时，只能让 `tx` 逐步减去 `sy`，检查 `tx % sy == sx`。  
3. 其余情况循环：  
   - `if tx > ty:` `tx %= ty`（但要避免 `tx` 变成 0，若 `tx % ty == 0` 则设为 `ty`，因为只能减到 `ty` 以上的最小正数）。  
   - `else:` `ty %= tx`（同理处理 0 的情况）。  
4. 当 `tx < sx` 或 `ty < sy` 时，说明已经走不到起点，返回 `False`。

> **类比**：把两条路上的距离想象成两根绳子，正向是把短绳子挂在长绳子上让它更长；逆向就是把长绳子剪掉若干段短绳子的长度，一剪就相当于取模，省时又省力。

#### 代码（Python）

```python
def reachingPoints(sx: int, sy: int, tx: int, ty: int) -> bool:
    # 从目标倒着回到起点
    while tx >= sx and ty >= sy:
        # 已经到达起点的特殊情况
        if tx == sx and ty == sy:
            return True
        # 如果 x 与 y 相等，说明只能向前走，倒着走不到起点
        if tx == ty:
            break

        if tx > ty:
            # 当 tx 很大时，一次性减去多个 ty，等价于取模
            if ty > sy:                     # 还能继续取模
                tx %= ty
                if tx == 0:                 # 防止变成 0，保持正数
                    tx = ty
            else:                           # ty 已经等于起始的 sy，只能逐步减去 sx
                # 只能让 tx 逐步靠近 sx
                return (tx - sx) % ty == 0
        else:  # ty > tx
            if tx > sx:
                ty %= tx
                if ty == 0:
                    ty = tx
            else:
                return (ty - sy) % tx == 0

    return False
```

> **关键行解释**  
> - `while tx >= sx and ty >= sy:`：只要目标坐标仍不小于起点，就可能继续倒退。  
> - `tx %= ty` / `ty %= tx`：一次性把大数减去小数的若干倍，等价于多次 “减去” 操作。  
> - `if tx == 0: tx = ty`：取模可能得到 0，但实际操作中不能把坐标变成 0（坐标始终正整数），所以把它恢复为 `ty`，表示已经减到只剩一次加法的状态。  
> - 当 `ty == sy`（或 `tx == sx`）时，只剩下单向的减法，用 `(tx - sx) % ty == 0` 判断是否能正好回到起点。

#### 复杂度

- **时间复杂度**：`O(log max(tx, ty))`。每一次取模都把较大的数显著缩小，类似欧几里得算法求最大公约数的复杂度。即使在最坏情况下（比如 `tx` 与 `ty` 相差很小），循环次数也不会超过 `log` 级别。  
- **空间复杂度**：`O(1)`，只使用了常数个变量。

> **对比**：暴力解需要指数级的时间，而最优解只需要对数级的步数，瞬间从“根本不可行”变成“毫秒级可解”。

---

## 心得

- **核心技巧**：**逆向思考 + 取模**（把多次减法合并为一次取模）。  
- **适用的题型**：  
  1. **“从 A 到 B 的可达性”**，如 `Reaching Points`、`Can Transform String`（通过逆向操作判断）。  
  2. **涉及两个数的递增/递减关系**，如 `Escape a Large Maze`（利用取模跳过大量无效步骤）。  
  3. **求解某类 Diophantine 方程**，比如 `Extended Euclidean` 相关的整数线性组合问题。  
- **一句话总结**：**倒着走，用取模一次剪掉所有“无意义的加法”。**

---

## 反思

- **第一反应**：直接从起点进行 BFS/DFS，想把所有可能的路径枚举出来。  
- **最容易踩的坑**：  
  - 忘记在取模后检查 `0` 的情况，导致无限循环或错误的 `False`。  
  - 没有处理 `tx == ty` 的特殊情形，这时正向只能一步一步走，倒着无法继续。  
  - 边界条件 `sx == tx` 或 `sy == ty` 时，需要单独判断是否能通过一次加法到达。  
- **下次遇到同类题**：第一步立刻问自己 **“能否逆向回到起点？”**，如果可以，尝试 **取模** 或 **欧几里得算法** 把大量重复操作合并。这样往往能把指数级的搜索瞬间压缩到对数级。