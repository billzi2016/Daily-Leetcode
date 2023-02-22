# #2139. **达到目标分数的最少操作次数** / Minimum Moves to Reach Target Score

> 难度：中等 · 标签：Math、Greedy · [LeetCode 链接](https://leetcode.com/problems/minimum-moves-to-reach-target-score/)

---

## 题目（英文原版）

**Description**

You are playing a game with integers. You start with the integer 1 and you want to reach the integer target.
In one move, you can either:
You can use the increment operation any number of times, however, you can only use the double operation at most maxDoubles times.
Given the two integers target and maxDoubles, return the minimum number of moves needed to reach target starting with 1.

**Examples**

**Example 1:**

```
Input: target = 5, maxDoubles = 0
Output: 4
Explanation: Keep incrementing by 1 until you reach target.
```

**Example 2:**

```
Input: target = 19, maxDoubles = 2
Output: 7
Explanation: Initially, x = 1
Increment 3 times so x = 4
Double once so x = 8
Increment once so x = 9
Double again so x = 18
Increment once so x = 19
```

**Example 3:**

```
Input: target = 10, maxDoubles = 4
Output: 4
Explanation: Initially, x = 1
Increment once so x = 2
Double once so x = 4
Increment once so x = 5
Double again so x = 10
```

**Constraints**

- 1 <= target <= 109
- 0 <= maxDoubles <= 100

---

## 题目（中文翻译）

你正在玩一个整数游戏。初始时你拥有整数 `1`，目标是得到整数 `target`。  
在一次操作中，你可以执行以下两种之一：

- **增量操作**（increment operation）：将当前整数加 `1`。
- **翻倍操作**（double operation）：将当前整数乘以 `2`。

你可以任意次数使用增量操作，但翻倍操作至多只能使用 `maxDoubles` 次。

给定整数 `target` 和 `maxDoubles`，返回从 `1` 开始达到 `target` 所需的最少操作次数。

---

### 示例

**示例 1**  
```
Input: target = 5, maxDoubles = 0
Output: 4
Explanation: 只使用增量操作，将 1 依次加到 5。
```

**示例 2**  
```
Input: target = 19, maxDoubles = 2
Output: 7
Explanation:
初始时 x = 1
增量 3 次 → x = 4
翻倍 1 次 → x = 8
增量 1 次 → x = 9
再次翻倍 → x = 18
增量 1 次 → x = 19
```

**示例 3**  
```
Input: target = 10, maxDoubles = 4
Output: 4
Explanation:
初始时 x = 1
增量 1 次 → x = 2
翻倍 1 次 → x = 4
增量 1 次 → x = 5
再次翻倍 → x = 10
```

---

### 约束条件

- `1 <= target <= 10^9`
- `0 <= maxDoubles <= 100`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**从 1 开始**，把每一步的所有可能都枚举出来，直到达到 `target` 为止。  
- 每一步我们有两种选择：  
  1. **加一**（`x = x + 1`），可以无限次使用。  
  2. **翻倍**（`x = x * 2`），但只能使用至多 `maxDoubles` 次。  
- 这其实就是在一棵**树**中搜索：根节点是 `1`，每个节点向下有两条边（加一、翻倍），叶子是所有能达到的数。  
- 为了找到最少步数，只要在这棵树里做**广度优先搜索（BFS）**，第一个遇到 `target` 的层数就是答案。  

> **类比**：想象你在城市里走路，每走一步可以向前走 1 米，或者坐公交车一次走两倍的距离（但公交车票有限）。要最快到达终点，就要层层展开所有可能的路线，最先到达终点的那条路线就是最短的。

这种方法一定是 **正确** 的，因为 BFS 会按照步数递增的顺序遍历所有状态，第一个出现 `target` 的一定是最少步数。

#### 代码（Python）

```python
from collections import deque

def minMoves_bruteforce(target: int, maxDoubles: int) -> int:
    # BFS 队列里存 (当前值, 已使用的翻倍次数, 已走的步数)
    q = deque()
    q.append((1, 0, 0))
    # 用 set 防止重复访问同一个状态
    visited = {(1, 0)}

    while q:
        x, used, steps = q.popleft()
        # 到达目标直接返回步数
        if x == target:
            return steps

        # 1️⃣ 加一
        nxt = x + 1
        if nxt <= target and (nxt, used) not in visited:
            visited.add((nxt, used))
            q.append((nxt, used, steps + 1))

        # 2️⃣ 翻倍（只能在还有剩余次数时使用）
        if used < maxDoubles:
            nxt = x * 2
            if nxt <= target and (nxt, used + 1) not in visited:
                visited.add((nxt, used + 1))
                q.append((nxt, used + 1, steps + 1))

    # 按题意一定能到达，这行理论上不会被执行
    return -1
```

#### 复杂度  

- **时间复杂度**：`O(2^{maxDoubles})`（每一次翻倍都会把搜索树的宽度翻倍），在最坏情况下会非常大，实际受 `target ≤ 10^9` 限制，但仍然不可接受。  
  - 用大白话说，就是“如果你只能翻倍 30 次，搜索的分支数可能会接近十亿”，会超时。  
- **空间复杂度**：同样是 `O(2^{maxDoubles})`，因为要把所有已经访问的状态放进集合。  

> 结论：暴力 BFS 虽然思路简单，但在本题的约束下（`target` 可达 `10^9`，`maxDoubles` 可达 100）根本跑不完，需要更聪明的办法。

---

### 2. 最优解  

#### 思路  

从**正向**（从 1 开始）思考时，翻倍看起来是“把数字变大”，但**翻倍的次数有限**，我们很难判断什么时候该翻倍、什么时候该加一。  
一个常用的技巧是**把问题反过来**：  

> **从 `target` 往回走，想办法最少步数回到 1。**  

反向操作正好是原来的逆操作：

| 正向操作 | 逆向操作 |
|----------|----------|
| `x = x + 1`（加一） | `x = x - 1`（减一） |
| `x = x * 2`（翻倍） | `x = x / 2`（除以 2），前提是 `x` 为偶数且我们还有剩余的翻倍次数 |

逆向思考的好处：

1. **减一** 永远可以做，且代价是 1 步。  
2. **除以 2** 能一次性把数字减半，比连续减一快得多。  
3. 当 `target` 为 **偶数** 且还有翻倍次数时，**优先除以 2**，因为这一步相当于在正向用了一个翻倍，省掉了很多加一的步数。  

因此贪心策略如下：

- 只要还有可用的翻倍次数 **并且** 当前 `target` 为偶数，就执行 `target //= 2`（一次除以二），计一步并把剩余的翻倍次数减 1。  
- 否则只能执行 `target -= 1`（减一），计一步。  
- 重复上述过程，直到 `target` 变成 1 为止。  

因为每一步都让 `target` **严格变小**，循环最多进行 `log₂(target)` 次除以二，加上一些减一操作，整体是 **线性于二进制位数** 的。

> **类比**：想象你在下楼梯，楼梯可以一次走两级（相当于除以 2），但你只能使用这个“大跨步”若干次。每当楼梯级数是偶数且还有“大跨步”机会时，你就先用它，这样能最快到达底层。

#### 代码（Python）

```python
def minMoves(target: int, maxDoubles: int) -> int:
    moves = 0                # 记录总步数
    doubles_left = maxDoubles

    while target > 1:
        # 情形 1：还能翻倍 且 当前是偶数 → 逆向用除以 2
        if doubles_left > 0 and target % 2 == 0:
            target //= 2
            doubles_left -= 1
            moves += 1
        else:
            # 情形 2：只能减一（正向是加一）
            # 为了加速，直接一次性减去目标的最低位 1 的数量
            # 但这里写成最直观的循环，每次减一也可以通过位运算一次性处理
            target -= 1
            moves += 1

    return moves
```

> **小技巧**：如果想进一步加速，可以一次性把连续的奇数减到最近的偶数：`moves += target & 1; target -= target & 1`，但对初学者保持最直接的 `target -= 1` 更易理解。

#### 复杂度  

- **时间复杂度**：`O(log target)`  
  - 每次除以 2 至少把数字减半，最多出现 `log₂(target)` 次。减一操作最多出现 `maxDoubles` 次之外的其余步数，整体仍然是对数级别。  
  - 用大白话说，就是“即使目标是十亿，也只需要大约 30 次除以二的机会，加上一点点减一，总步数在几百以内”。  

- **空间复杂度**：`O(1)`  
  - 只使用了常数个变量，不随输入规模增长。

---

## 心得  

- **核心技巧**：**逆向贪心**——从目标倒着做操作，优先使用“除以 2”来快速缩小规模。  
- **适用的题型**（类似思路）：  
  1. *Minimum Operations to Reduce X to Y*（从 `X` 通过加 1、乘 2 等操作变成 `Y`）  
  2. *Broken Calculator*（LeetCode 991）  
  3. *Integer Replacement*（LeetCode 397）  
- **一句话总结解题钥匙**：**把“大跨步”（翻倍）倒着想成“除以二”，只要还能除且是偶数就先除，剩下的只能一步步减**。

---

## 反思  

- **第一反应**：直接写 BFS，枚举所有可能。因为对搜索熟悉，想到“最短路”自然想到 BFS。  
- **最容易踩的坑**：  
  1. **忘记限制翻倍次数**：在逆向时必须同步把 `maxDoubles` 计数递减，否则会误把可以无限除以二的情况当作合法。  
  2. **边界条件**：`target = 1` 时直接返回 0；`maxDoubles = 0` 时只能全靠加一，需要保证循环不会进入除以二的分支。  
  3. **大数溢出**：在正向模拟时可能出现 `x*2` 超过 Python 整数范围（虽然 Python 自动扩展），但在实际面试中要注意语言的整数上限。  
- **下次遇到同类题**，第一步应该**先考虑逆向**：把“增大”操作翻转为“缩小”操作，寻找可以一次性大幅度缩小的贪心机会（如除以 2、除以 3、减半等），再再决定是否需要 BFS 或 DP。