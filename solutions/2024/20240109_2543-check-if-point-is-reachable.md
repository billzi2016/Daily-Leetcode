# #2543. 判断点是否可达 / Check if Point Is Reachable

> 难度：困难 · 标签：Math、Number Theory · [LeetCode 链接](https://leetcode.com/problems/check-if-point-is-reachable/)

---

## 题目（英文原版）

**Description**

There exists an infinitely large grid. You are currently at point (1, 1), and you need to reach the point (targetX, targetY) using a finite number of steps.
In one step, you can move from point (x, y) to any one of the following points:
Given two integers targetX and targetY representing the X-coordinate and Y-coordinate of your final position, return true if you can reach the point from (1, 1) using some number of steps, and false otherwise.

**Examples**

**Example 1:**

```
Input: targetX = 6, targetY = 9
Output: false
Explanation: It is impossible to reach (6,9) from (1,1) using any sequence of moves, so false is returned.
```

**Example 2:**

```
Input: targetX = 4, targetY = 7
Output: true
Explanation: You can follow the path (1,1) -> (1,2) -> (1,4) -> (1,8) -> (1,7) -> (2,7) -> (4,7).
```

**Constraints**

- 1 <= targetX, targetY <= 109

---

## 题目（中文翻译）

存在一个无限大的网格。你当前位于点 (1, 1)，需要在有限步数内到达点 (targetX, targetY)。  
在一步操作中，你可以从点 (x, y) 移动到以下任意一个点：  
（题目原文中列出的可移动点，此处省略）

给定两个整数 targetX 和 targetY，分别表示最终位置的 X 坐标和 Y 坐标。如果可以通过若干步从 (1, 1) 到达该点，返回 `true`；否则返回 `false`。

**示例 1**  
输入: `targetX = 6, targetY = 9`  
输出: `false`  
解释: 无法通过任何移动序列从 (1,1) 到达 (6,9)，因此返回 `false`。

**示例 2**  
输入: `targetX = 4, targetY = 7`  
输出: `true`  
解释: 你可以按照以下路径到达: (1,1) → (1,2) → (1,4) → (1,8) → (1,7) → (2,7) → (4,7)。

**约束条件**  
- 1 ≤ targetX, targetY ≤ 10^9

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**正向模拟**：从起点 `(1, 1)` 出发，按照题目给出的四种合法移动不停地扩展所有可能到达的点，直到看到目标 `(targetX, targetY)` 为止，或者搜索空间已经太大、没有新点可以加入为止。

- **使用的数据结构**：  
  - **队列**（`collections.deque`）相当于排队买饭的队伍，先进入的点先被取出来扩展。  
  - **集合**（`set`）像是一本“已经去过的城市名单”，把已经访问过的坐标记下来，防止重复搜索（避免在地图上来回走）。

- **为什么它是正确的**：  
  只要我们把**所有**合法的下一步都枚举出来，并且不漏掉任何一步，那么搜索过程就会遍历**所有**能够从 `(1,1)` 到达的点。如果目标点真的可以到达，它一定会在搜索过程中出现。

- **时间/空间复杂度**（大白话）  
  - 每次从队列里取出一个点，都要产生 **4** 条新边（最多四种移动方式）。如果我们把搜索进行到第 `k` 步，就会产生大约 `4^k` 个点。  
  - 因此时间复杂度是 **指数级**，记作 `O(4^k)`，意思是“随步数呈指数增长”，即使 `k` 只有 20，点的数量也已经超过一千万，根本跑不完。  
  - 同时我们把所有已经访问过的点都存进集合，空间也会是 `O(4^k)`，同样会爆掉内存。

> **结论**：暴力正向搜索在本题根本不可行，只能用来帮助我们理解题目。

#### 代码（Python）

```python
from collections import deque

def reachable_bruteforce(targetX: int, targetY: int) -> bool:
    # BFS（广度优先搜索）模拟所有可能的移动
    q = deque()
    q.append((1, 1))
    visited = {(1, 1)}                # 已经去过的坐标集合

    while q:
        x, y = q.popleft()
        if (x, y) == (targetX, targetY):
            return True

        # 四种合法的前进方式
        nxt = [(x + y, y), (x, x + y), (x * 2, y), (x, 2 * y)]

        for nx, ny in nxt:
            # 为了防止搜索无限扩大，这里随意设一个上限（仅用于演示）
            if nx > 2 * targetX or ny > 2 * targetY:
                continue
            if (nx, ny) not in visited:
                visited.add((nx, ny))
                q.append((nx, ny))

    return False   # 队列空了，说明目标不可达
```

> **注意**：上面代码里我们人为加了 `nx > 2*targetX` 之类的剪枝，只是为了让演示跑得快；实际题目坐标可以高达 `10^9`，根本不可能完整搜索。

#### 复杂度  

- **时间复杂度**：`O(4^k)`（指数级），`k` 为搜索深度。  
  - 大意是：每走一步，分支会成指数增长，算力很快就跟不上。  
- **空间复杂度**：`O(4^k)`，因为要把所有已经遍历的点都存进集合。

---

### 2. 最优解

#### 思路  

**从后往前思考**——把题目倒着看：从目标 `(targetX, targetY)` 逐步“回退”到起点 `(1,1)`。  
这样每一步的逆操作就只有两类：

| 正向操作 | 逆向操作（从大坐标回到小坐标） |
| -------- | ---------------------------- |
| `(x, y) → (x + y, y)` | 如果 `x > y`，可以把 `x` 减掉 `y`：`(x, y) → (x - y, y)` |
| `(x, y) → (x, y + x)` | 同理，如果 `y > x`，可以把 `y` 减掉 `x` |
| `(x, y) → (2x, y)` | 如果 `x` 是偶数，可以除以 2：`(x, y) → (x/2, y)` |
| `(x, y) → (x, 2y)` | 如果 `y` 是偶数，可以除以 2：`(x, y) → (x, y/2)` |

**瓶颈**  
- 直接用 “减去” 的逆操作会导致 **一步一步** 只减掉一次，最坏情况下会出现 `O(max(x, y))` 步，仍然太慢（比如 `10^9`）。  
- 关键在于**一次性**把大的坐标减掉 **尽可能多** 次。这正是 **欧几里得算法**（求最大公约数 GCD）里用的“取模”技巧：`x = x % y` 能一次性去掉若干个 `y`。

**观察 GCD**  
- “加法”操作 `(x + y, y)` 或 `(x, x + y)` **不会改变** 两数的最大公约数。  
- “除以 2” 操作会把 **公约数乘以 2**（如果两个数本来都有因子 2），或者保持不变。  
- 因此，在任意一次合法移动后，`gcd(x, y)` 只会 **乘以 2 的若干次**，**永远不会出现奇数因子**的变化。

从 `(1,1)` 出发，初始 `gcd = 1`。经过任意次合法移动后，得到的坐标 `(x, y)` 必然满足：

```
gcd(x, y) = 2^k   （k ≥ 0，表示 1、2、4、8… 这些 2 的幂）
```

**逆向过程的判定**  
- 我们只需要检查目标点的 `gcd` 是否是 **2 的幂**。如果是，就一定能把它一步步“除掉”所有的 2（使用除以 2 的逆操作），再用 “取模” 把两个数化为 `(1, 1)`；如果不是，则无论怎么除以 2、取模，都不可能把公约数降到 1，说明不可达。

**如何快速判断 “是 2 的幂”**  
- 一个正整数 `n` 是 2 的幂，当且仅当 `n & (n - 1) == 0`（二进制表示只有一个 `1`）。

**完整逆向步骤（不必真的写循环）**  
1. 计算 `g = gcd(targetX, targetY)`。  
2. 判断 `g` 是否是 2 的幂：`g & (g - 1) == 0`。  
3. 若是，返回 `True`；否则返回 `False`。

> **为什么不需要真正做循环？**  
> 因为只要 `g` 是 2 的幂，**一定**存在一系列除以 2、取模的逆操作把点回到 `(1,1)`；若不是，则不可能。于是我们直接用数论结论得出答案，时间只花在一次 `gcd` 计算上。

#### 代码（Python）

```python
import math

def canReach(targetX: int, targetY: int) -> bool:
    """
    判断能否从 (1,1) 经过若干次合法移动到 (targetX, targetY)。
    思路：只要 gcd(targetX, targetY) 是 2 的幂，就一定可达。
    """
    g = math.gcd(targetX, targetY)          # 求两数的最大公约数
    # 判断 g 是否是 2 的幂（二进制里只有一个 1）
    return (g & (g - 1)) == 0                # True -> 可达, False -> 不可达
```

**代码解释（逐行中文注释）**

| 行号 | 代码 | 中文解释 |
|------|------|----------|
| 1    | `import math` | 引入标准库 `math`，我们只用它的 `gcd` 函数。 |
| 3-9  | `def canReach(...):` | 定义主函数，接受目标坐标。 |
| 6    | `g = math.gcd(targetX, targetY)` | 计算两坐标的最大公约数。 |
| 8    | `return (g & (g - 1)) == 0` | 用位运算判断 `g` 是否是 2 的幂，返回布尔值。 |

#### 复杂度  

- **时间复杂度**：`O(log min(targetX, targetY))`。  
  - 只做一次欧几里得求 GCD，欧几里得算法的复杂度是对数级，意思是即使坐标是 `10^9`，也只需要大约 30 次除法/取模运算。  
- **空间复杂度**：`O(1)`。  
  - 只用常数级的几个整数变量，不会随输入大小增长。

与暴力解相比，**时间从指数级下降到对数级**，**空间从指数级降到常数级**，这正是本题的关键突破。

---

## 心得

- **核心技巧**：**利用最大公约数 (GCD) 与 2 的幂的性质**，把看似复杂的路径问题转化为简单的数论判定。  
- **该技巧适用的题型**  
  1. “从 (a,b) 经过加法/倍数操作能否到达 (c,d)” 类的可达性题（如 LeetCode 780、1153）。  
  2. “只允许对数或除以 2 的操作，判断能否化为 1”的问题（如 “整数是否能化为 1”）。  
- **一句话总结解题钥匙**：**只要目标点的 GCD 是 2 的幂，就一定可达**。

---

## 反思

- **第一反应**：看到“无限网格”和“可以加、可以倍增”，我本能地想用 BFS 正向搜索。  
- **最容易踩的坑**  
  - 忽视 **指数爆炸**：直接模拟会在几步内产生海量点，导致超时或内存爆炸。  
  - 误以为只要坐标相等或相差不大就能到达，忘记 **公约数** 的限制。  
  - 边界条件：`targetX = targetY = 1`（显然可达），以及极大数值时的溢出（在 Python 中整数不会溢出，但语言差异需要注意）。  
- **下次遇到同类题的第一步**：先思考 **是否可以逆向回退**，并寻找 **不变式**（如 GCD、奇偶性），把搜索空间压缩到常数或对数级。这样往往能迅速发现隐藏的数论结构，从而得到最优解。