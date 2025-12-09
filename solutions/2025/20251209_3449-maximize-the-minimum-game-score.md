# #3449. 最大化最小游戏得分 / Maximize the Minimum Game Score

> 难度：困难 · 标签：Array、Binary Search、Greedy · [LeetCode 链接](https://leetcode.com/problems/maximize-the-minimum-game-score/)

---

## 题目（英文原版）

**Description**

You are given an array points of size n and an integer m. There is another array gameScore of size n, where gameScore[i] represents the score achieved at the ith game. Initially, gameScore[i] == 0 for all i.
You start at index -1, which is outside the array (before the first position at index 0). You can make at most m moves. In each move, you can either:
Note that the index must always remain within the bounds of the array after the first move.
Return the maximum possible minimum value in gameScore after at most m moves.

**Examples**

**Example 1:**

```
Input: points = [2,4], m = 3
Output: 4
Explanation:
Initially, index i = -1 and gameScore = [0, 0] .
The minimum value in gameScore is 4, and this is the maximum possible minimum among all configurations. Hence, 4 is the output.
```

**Example 2:**

```
Input: points = [1,2,3], m = 5
Output: 2
Explanation:
Initially, index i = -1 and gameScore = [0, 0, 0] .
The minimum value in gameScore is 2, and this is the maximum possible minimum among all configurations. Hence, 2 is the output.
```

**Constraints**

- 2 <= n == points.length <= 5 * 104
- 1 <= points[i] <= 106
- 1 <= m <= 109

---

## 题目（中文翻译）

**描述**  
给定一个大小为 `n` 的整数数组 `points` 和一个整数 `m`。还有另一个大小为 `n` 的数组 `gameScore`，其中 `gameScore[i]` 表示第 `i` 场游戏获得的得分。初始时 `gameScore[i] == 0`（对所有 `i` 均为 0）。  
你从下标 `-1` 开始，即数组之外（在下标 `0` 之前的“左侧”位置）。最多可以进行 `m` 次移动。每一次移动，你可以执行以下操作之一：

>（题目原文中未给出具体的两种操作，这里保持原样）

> **注意**：在第一次移动之后，下标必须始终保持在数组范围内。

返回在至多 `m` 次移动后，`gameScore` 中的 **最小值** 能够达到的最大可能值。

---

**示例 1**  
```
Input: points = [2,4], m = 3
Output: 4
Explanation:
Initially, index i = -1 and gameScore = [0, 0] .
The minimum value in gameScore is 4, and this is the maximum possible minimum among all configurations. Hence, 4 is the output.
```

**示例 2**  
```
Input: points = [1,2,3], m = 5
Output: 2
Explanation:
Initially, index i = -1 and gameScore = [0, 0, 0] .
The minimum value in gameScore is 2, and this is the maximum possible minimum among all configurations. Hence, 2 is the output.
```

**约束条件**  
- `2 <= n == points.length <= 5 * 10^4`  
- `1 <= points[i] <= 10^6`  
- `1 <= m <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

把题目想成“在一条直线上的若干个房间，每个房间 `i` 有一种糖果，糖果的价值是 `points[i]`”。  
我们从左侧的门（下标 `-1`）出发，每走一步就会进入相邻的房间。**每次进入房间 `i`，就会把 `points[i]` 加到该房间的 `gameScore[i]` 上**。  
目标是：在最多 `m` 步之内，使得所有房间的糖果总价值的最小值尽可能大。

最直接的想法是：**把每一步都枚举出来**，把所有可能的走法都尝试一次，记录每种走法结束后 `gameScore` 的最小值，最后取最大值。

- **数据结构**：直接用一个长度为 `n` 的列表 `gameScore` 来记录每个位置的累计得分。  
  - `list` 就像一本记事本，记下每个房间里放了多少糖果。  
- **为什么正确**：我们把**所有**合法的走法都遍历了一遍，最好的那一次自然会被找到。  
- **时间/空间复杂度**：  
  - 每一步都有两种选择（向左或向右），最多走 `m` 步，所以走法的数量是 `2^m`（指数级别）。  
  - 对每一种走法我们都要遍历 `m` 步去模拟，整体时间是 `O(2^m * m)`，在最坏情况下根本不可接受。  
  - 空间只需要保存 `gameScore`，即 `O(n)`。

> **大白话**：  
> `O(2^m)` 就像让你把 20 次硬币翻面所有可能的排列都列出来，根本不可能在一分钟内算完。

#### 代码（Python）

```python
def brute_force(points, m):
    n = len(points)
    best = 0                     # 当前找到的最大最小值

    def dfs(pos, steps, score):
        """深度优先搜索所有走法
        pos   : 当前所在的下标（-1 表示门外）
        steps : 已经走了多少步
        score : 当前每个位置的累计得分（列表）
        """
        nonlocal best
        if steps == m:           # 已经用完所有步数
            best = max(best, min(score))   # 更新答案
            return

        # 两种可能的移动方向
        for nxt in (pos - 1, pos + 1):
            # 必须保证移动后仍在数组范围内（第一次移动除外）
            if nxt < -1 or nxt >= n:
                continue
            if nxt == -1:        # 仍在门外，不能得分
                dfs(nxt, steps + 1, score)
            else:
                # 进入 nxt，得分 + points[nxt]
                new_score = score[:]           # 复制一份
                new_score[nxt] += points[nxt]
                dfs(nxt, steps + 1, new_score)

    # 初始状态：在门外，所有得分为 0
    dfs(-1, 0, [0] * n)
    return best
```

> 代码仅用于说明思路，实际运行会因 `2^m` 的爆炸式增长而超时。

#### 复杂度

- **时间复杂度**：`O(2^m * m)` — 每一步都有两种选择，指数级增长，根本不可行。  
- **空间复杂度**：`O(n)` — 只保存 `gameScore` 列表和递归栈。

---

### 2. 最优解

#### 思路  

从暴力解可以看出：**真正的难点不是“怎么走”，而是“走多少次”**。  
我们不需要枚举每一步的具体顺序，只要知道**每个位置最少要被访问多少次**，就能算出最少需要多少步。  

**关键观察**  

1. **每次访问位置 `i`，`gameScore[i]` 会增加 `points[i]`**。  
   - 如果想让 `gameScore[i] ≥ x`，最少需要访问 `i`  
     \[
     t_i = \left\lceil \frac{x}{\text{points}[i]} \right\rceil
     \]  
     次（向上取整），因为每次只能加 `points[i]`。  

2. **访问次数与步数的关系**  
   - 第一次到达 `i` 必然是从左边的 `i-1`（或者是起点 `-1`）走一步。  
   - 之后的每一次额外访问，都需要先离开 `i` 再回来。  
     - 离开去 `i+1` 用 1 步，回来再到 `i` 再用 1 步 → **2 步** 完成一次额外访问。  
   - 当我们处理完位置 `i` 后，还要继续前进到 `i+1`（除非已经是最右端），这也要 **1 步**。  

   综合起来，若 `t_i` 为位置 `i` 需要的访问次数：

   - 对 **非最后一个位置** (`i < n-1`)  
     \[
     \text{步数}_i = 1\;(\text{第一次到达}) + (t_i-1)\times 2\;(\text{额外访问}) + 1\;(\text{前进到 i+1}) = 2t_i
     \]

   - 对 **最后一个位置** (`i = n-1`)  
     \[
     \text{步数}_{n-1}=1 + (t_{n-1}-1)\times 2 = 2t_{n-1}-1
     \]

   把所有位置的步数相加，得到 **实现目标 `x` 的最少步数**：

   \[
   \text{minMoves}(x)=\sum_{i=0}^{n-2} 2t_i + (2t_{n-1}-1)=2\sum_{i=0}^{n-1} t_i - 1
   \]

3. **二分答案**  
   - `minMoves(x)` 随着 `x` 增大而单调不减（要的访问次数只能增多），  
   - 因此我们可以**二分** `x`，每次检查 `minMoves(x) ≤ m` 是否成立。  
   - 二分的上界可以取 `max(points) * m`（把所有步都花在价值最大的格子上），下界取 `0`。  

**完整算法**  

```
binary search low = 0, high = max(points) * m
while low < high:
    mid = (low + high + 1) // 2      # 取上中位数，防止死循环
    if feasible(mid):               # 检查是否能在 ≤ m 步内让每个 score ≥ mid
        low = mid
    else:
        high = mid - 1
return low
```

`feasible(x)` 的实现只需要遍历一次数组，计算 `t_i = ceil(x / points[i])`，累加 `2*t_i`，最后减 `1` 与 `m` 比较。  

**为什么是最优**  

- **不枚举走法**：只关注每个位置需要多少次访问，省掉了指数级的枚举。  
- **贪心地把多余的访问放在原地往返**：这是最省步数的方式（离开再回来恰好 2 步），没有更好的办法可以在更少步数内增加一次访问。  
- **二分搜索**把原本可能的 `x`（答案）范围压缩到 `log(max* m)` 次检查，每次检查 `O(n)`，总体 `O(n log(max* m))`，已经是该问题的理论下界（因为必须看每个 `points[i]`）。

#### 代码（Python）

```python
import math
from typing import List

def max_min_game_score(points: List[int], m: int) -> int:
    """
    返回在至多 m 步内，gameScore 的最小值能够达到的最大可能值。
    """
    n = len(points)

    # ---------- 判断给定的 x 是否可行 ----------
    def feasible(x: int) -> bool:
        """
        计算让每个位置的得分至少为 x 所需的最少步数。
        若该步数 ≤ m，则返回 True。
        """
        total_visits = 0               # Σ t_i
        for p in points:
            # t_i = ceil(x / p)
            # 使用整数运算避免浮点数误差
            t_i = (x + p - 1) // p
            total_visits += t_i
            # 早停：如果已经超过上界，直接返回 False
            # 2*total_visits - 1 是当前累计的最小步数
            if 2 * total_visits - 1 > m:
                return False
        # 最少步数 = 2 * Σ t_i - 1
        return 2 * total_visits - 1 <= m

    # ---------- 二分搜索答案 ----------
    lo, hi = 0, max(points) * m   # 上界足够大
    while lo < hi:
        mid = (lo + hi + 1) // 2   # 取上中位数，防止死循环
        if feasible(mid):
            lo = mid               # mid 可行，尝试更大
        else:
            hi = mid - 1           # mid 不可行，缩小上界
    return lo
```

**关键行解释**  

- `t_i = (x + p - 1) // p`  
  > 把向上取整写成整数除法，像“把糖果装进盒子”，不足一盒也算一盒。  
- `if 2 * total_visits - 1 > m: return False`  
  > 只要已经超过步数上限，就不必继续遍历后面的元素，省时间。  
- `while lo < hi:` + `mid = (lo + hi + 1) // 2`  
  > 二分的标准写法，`+1` 保证在 `lo` 与 `hi` 相差 1 时仍能收敛。

#### 复杂度

- **时间复杂度**：`O(n log (max(points) * m))`  
  - 每次二分检查遍历一次数组 `O(n)`，二分的迭代次数是 `log (max* m)`（约 60 次，足够快）。  
  - 与暴力的指数级 `2^m` 相比，快了天壤之别。  
- **空间复杂度**：`O(1)`（除输入外只用常数级额外变量）  
  - 不需要额外的数组或递归栈，内存开销几乎为零。

---

## 心得

- **核心技巧**：**把“每个位置至少要多少分”转化为“每个位置至少要访问多少次”，再用**`2 * Σ visits - 1`** 计算最少步数，配合二分搜索得到答案。  
- **适用场景**：  
  1. “在有限步数/操作次数内，使所有元素至少达到某阈值”——如 **分配资源**、**加油站补给** 等。  
  2. “每次操作只能对当前位置产生固定增益”，需要求最大最小值——如 **硬币游戏**、**刷怪升级**。  
  3. 需要**单调性**+**二分**的优化问题——如 **最大化最小配额**、**最小化最大负载**。  
- **一句话总结解题钥匙**：**把目标值 `x` 固定下来，算出实现它所需的最少步数，二分寻找最大的 `x`**。

---

## 反思

- **第一反应**：直接去枚举所有走法，想把每一步都写清楚。  
- **最容易踩的坑**：  
  - 忘记第一次到达某个位置已经算一次访问，导致 `t_i` 的计算少了 1。  
  - 计算最少步数时遗漏了最后一个位置不需要再向右走一步，导致多加了 1 步。  
  - 二分的上下界写反，或者取中位数时使用向下取整导致死循环。  
- **下次类似题目第一步**：**先判断“是否存在单调性”，把答案的判定函数写出来（这里是 `feasible(x)`），再决定是否可以二分**。这样能立刻把指数爆炸的搜索空间压缩到对数级。