# #1033. 移动石子直至连续 / Moving Stones Until Consecutive

> 难度：中等 · 标签：Math、Brainteaser · [LeetCode 链接](https://leetcode.com/problems/moving-stones-until-consecutive/)

---

## 题目（英文原版）

**Description**

There are three stones in different positions on the X-axis. You are given three integers a, b, and c, the positions of the stones.
In one move, you pick up a stone at an endpoint (i.e., either the lowest or highest position stone), and move it to an unoccupied position between those endpoints. Formally, let's say the stones are currently at positions x, y, and z with x < y < z. You pick up the stone at either position x or position z, and move that stone to an integer position k, with x < k < z and k != y.
The game ends when you cannot make any more moves (i.e., the stones are in three consecutive positions).
Return an integer array answer of length 2 where:

**Examples**

**Example 1:**

```
Input: a = 1, b = 2, c = 5
Output: [1,2]
Explanation: Move the stone from 5 to 3, or move the stone from 5 to 4 to 3.
```

**Example 2:**

```
Input: a = 4, b = 3, c = 2
Output: [0,0]
Explanation: We cannot make any moves.
```

**Example 3:**

```
Input: a = 3, b = 5, c = 1
Output: [1,2]
Explanation: Move the stone from 1 to 4; or move the stone from 1 to 2 to 4.
```

**Constraints**

- 1 <= a, b, c <= 100
- a, b, and c have different values.

---

## 题目（中文翻译）

有三颗石子分别位于 X 轴的不同位置，给定三个整数 `a`, `b`, `c` 表示石子的初始坐标。  
在一次移动中，你只能挑选位于**端点 (endpoint)** 的石子（即当前位置最小或最大的石子），并将其移动到两个端点之间的一个未被占用的位置。形式化地，设当前石子的位置为 `x < y < z`，你可以把位于 `x` 或 `z` 的石子搬到某个整数位置 `k`，满足 `x < k < z` 且 `k ≠ y`。  
当无法再进行任何移动时（即三颗石子已经占据 **连续 (consecutive)** 的三个位置），游戏结束。

返回一个长度为 2 的整数数组 `answer`，其中：

- `answer[0]` 为使石子达到连续状态所需的**最小移动次数**；
- `answer[1]` 为在任意合法操作序列中可能出现的**最大移动次数**。

---

## 示例

**示例 1**  
```
Input: a = 1, b = 2, c = 5
Output: [1,2]
Explanation: 将石子从 5 移动到 3，或者先将石子从 5 移动到 4 再移动到 3。
```

**示例 2**  
```
Input: a = 4, b = 3, c = 2
Output: [0,0]
Explanation: 已经是连续的三个位置，无法进行任何移动。
```

**示例 3**  
```
Input: a = 3, b = 5, c = 1
Output: [1,2]
Explanation: 将石子从 1 移动到 4；或者将石子从 1 移动到 2 再移动到 4。
```

---

## 约束条件

- `1 <= a, b, c <= 100`
- `a`, `b`, `c` 互不相同。

---

## 解题过程  

下面我们一起攻克 LeetCode “Moving Stones Until Consecutive”。  
题目给出三颗石子在数轴上的不同坐标 `a, b, c`（`1 ≤ a,b,c ≤ 100`），每一步只能把最左或最右的石子搬到 **两个端点之间的空位**（必须是整数且不能放在已有石子的位置）。  
当三颗石子恰好占据 **连续的三个整数** 时游戏结束，要求返回一个长度为 2 的数组  

```
[minimumMoves, maximumMoves]
```

分别表示 **最少** 需要多少步能结束，以及 **最多** 还能走多少步（仍然在合法规则下）。

---

### 1. 直觉解（暴力）

#### 思路  

> **把问题想成 “在小范围里穷举所有合法搬动”**  
>  
> - **数据结构**：我们用一个 `tuple` `(x, y, z)`（已排好序 `x < y < z`）来记录三颗石子的当前位置。  
>   - 这个 tuple 像一本 **字典**，键是位置，值是“这格子里有石子”。  
> - **合法搬动**：每一步只能把左端点 `x` 或右端点 `z` 移到 `(x, z)` 之间的空位 `k`（`k ≠ y`），搬完后再把三颗石子重新排序。  
> - **暴力搜索**：从初始状态出发，用 BFS（广度优先搜索）遍历所有可能的状态，记录每个状态首次到达时的步数（这就是到达该状态的 **最少** 步数）。当我们首次碰到 “连续” 状态 `(t, t+1, t+2)` 时，当前步数就是 **最小移动数**。  
> - **最大移动数**：因为 BFS 会遍历所有 reachable 的状态，我们只要在遍历完后取 **最大** 的步数即可（只要还能继续搬动就一定不是终止状态）。  

> **为什么暴力是对的？**  
> - 题目约束很小：坐标最大 100，三颗石子只能占 3 个格子，状态空间最多是 `C(100,3) ≈ 161,700`，完全可以在毫秒级遍历完。  
> - BFS 保证第一次到达某个状态的步数是最短路径，这正好对应题目要求的“最少移动”。  
> - 同时遍历所有状态自然能得到最大的步数。  

> **时间/空间复杂度**  
> - **时间**：`O(number_of_states * possible_moves_per_state)`  
>   - 状态数上限约 `1.6e5`，每个状态最多有 `2 * (z - x - 1)` 种搬法（左端点或右端点各可以搬到中间的每个空位），最坏情况 `O(100)`。整体约 `O(1e7)`，在 Python 里仍然能跑完。  
>   - 用大白话说，就是“最多几百万次小循环”，电脑跑得很快。  
> - **空间**：`O(number_of_states)` 用于 `visited` 集合和 BFS 队列，大约几万到十几万条记录，几 MB 内存。  

#### 代码（Python）

```python
from collections import deque
from typing import List, Tuple

def movingStones_bruteforce(a: int, b: int, c: int) -> List[int]:
    # -------------------------------------------------
    # 1. 把三个坐标排好序，形成初始状态 (x, y, z)
    # -------------------------------------------------
    start = tuple(sorted((a, b, c)))          # 例如 (1,2,5)

    # -------------------------------------------------
    # 2. BFS 初始化
    # -------------------------------------------------
    q = deque()
    q.append((start, 0))                      # (状态, 已走步数)
    visited = {start}                         # 已经遍历过的状态

    min_moves = None
    max_moves = 0

    while q:
        (x, y, z), steps = q.popleft()

        # -------------------------------------------------
        # 3. 检查是否已经是连续的三个数
        # -------------------------------------------------
        if x + 1 == y and y + 1 == z:        # 形如 (t, t+1, t+2)
            if min_moves is None:            # 第一次遇到，必然是最少步数
                min_moves = steps
            # 仍然继续搜索，找出更大的 steps（因为还有其它路径可以更慢地收敛）
        else:
            # -------------------------------------------------
            # 4. 产生所有合法的搬动
            # -------------------------------------------------
            # 把左端点 x 搬到 (x, z) 之间的空位
            for k in range(x + 1, z):
                if k == y:                     # 不能搬到已有石子的位置
                    continue
                new_state = tuple(sorted((k, y, z)))
                if new_state not in visited:
                    visited.add(new_state)
                    q.append((new_state, steps + 1))

            # 把右端点 z 搬到 (x, z) 之间的空位
            for k in range(x + 1, z):
                if k == y:
                    continue
                new_state = tuple(sorted((x, y, k)))
                if new_state not in visited:
                    visited.add(new_state)
                    q.append((new_state, steps + 1))

        # -------------------------------------------------
        # 5. 更新最大步数（只要还能继续搬动，这一步就算合法）
        # -------------------------------------------------
        max_moves = max(max_moves, steps)

    # BFS 结束后 min_moves 必定被赋值（题目保证一定可以收敛）
    return [min_moves, max_moves]
```

> **关键行中文注释** 已在代码里标出，帮助你快速定位每一步的意义。

#### 复杂度  

- **时间复杂度**：`O(状态数 × 每状态的合法搬动数) ≈ O(1e7)`，即“几千万次基本操作”。  
- **空间复杂度**：`O(状态数) ≈ O(1.6e5)`，即“几百 KB~几 MB 的内存”。  

虽然能跑通，但我们仍然可以 **用数学观察** 把时间降到常数级，这就是下面的最优解。

---

### 2. 最优解  

#### 思路  

从暴力解我们已经知道：**游戏最多只需要 2 步就能结束**（因为每一步都把一个端点搬到另一个端点的“旁边”），而 **最大步数** 与两端点之间的距离有关。  
下面一步步把这两个结论推导出来。

---

##### 2.1 为什么最少步数最多是 2？

把三个位置排好序记为 `x < y < z`。  
- **若已经连续**（`x+1 == y` 且 `y+1 == z`），显然不需要搬动，最少步数 = 0。  
- **若两颗石子之间只差 2**（例如 `x, x+2, z` 或 `x, y, y+2`），只要把另一端点搬到中间的空位，就能一次形成连续三个数。  
  - 例子：`1,2,5` → 把 `5` 搬到 `3`（或者 `4` 再搬到 `3`），一步完成。  
- **其余情况**：两端点之间的间距至少是 3。此时我们可以先把左端点或右端点搬到 **另一个端点的旁边**（即形成 `x, x+1, z` 或 `x, z-1, z`），此时仍不是连续，但只剩下 **把中间的那颗石子搬到旁边**，再一步即可。  
  - 所以最多只需要 2 步。

> **结论**：最少步数只能是 0、1 或 2。  
> 判断规则：  
> - `0` 当且仅当 `x+1 == y` 且 `y+1 == z`。  
> - `1` 当且仅当 `y - x == 2` **或** `z - y == 2`。  
> - 其余情况返回 `2`。

---

##### 2.2 最大步数怎么算？

观察每一次合法搬动的 **效果**：  
- 只能搬动端点石子 `x` 或 `z`。  
- 搬动后，新的最左位置 **不会小于** 原来的 `x`，最右位置 **不会大于** 原来的 `z`。  
- 更重要的是：**最大位置与最小位置的差距一定会减小至少 1**。  
  - 设 `gap = z - x`。搬动左端点 `x` 到 `k (x<k<z)`，新的最左点是 `min(k, y)`，最右点仍是 `z`，于是新 `gap' = z - min(k, y) ≤ z - (x+1) = gap - 1`。右端点同理。  

因此，**每走一步，`gap` 至少缩小 1**。  
当最终形成连续三个数时，`gap = 2`（因为 `z - x = (t+2) - t = 2`）。  
所以 **最多可以走的步数** = `initial_gap - 2`。  

但我们还有一个细节：**如果两端之间的空位非常多，实际上每一步我们只能把端点搬到离另一端点最近的空位**，也就是每一步只能让 `gap` 减少 **恰好 1**（这已经是最慢的情况）。  
于是 **最大步数** = `max(y - x, z - y) - 1`。  
解释：  
- `y - x` 是左侧两个石子之间的距离，`z - y` 是右侧两个石子之间的距离。  
- 只要每次都把远端的石子搬到离中间石子 **最远的那一侧**（即每次只缩小较大的那段距离 1），最终的步数就是较大距离减 1。  

> **举例**：`1, 2, 5` → `gap = 4`，较大段是 `5-2 = 3`，最大步数 = `3-1 = 2`（走法：`5→4→3` 或 `5→3→4`）。  

---

##### 2.3 完整的最优算法  

1. 把 `a, b, c` 排序得到 `x, y, z`。  
2. **最小步数**  
   - 若 `x+1 == y` 且 `y+1 == z` → `min = 0`。  
   - 否若 `y - x == 2` 或 `z - y == 2` → `min = 1`。  
   - 否则 → `min = 2`。  
3. **最大步数**  
   - `max = max(y - x, z - y) - 1`。  

这套公式只用了几次整数运算，时间 **O(1)**，空间 **O(1)**。

---

#### 代码（Python）

```python
from typing import List

def movingStones(a: int, b: int, c: int) -> List[int]:
    """
    返回 [minimumMoves, maximumMoves]。
    思路来源于数学观察，时间、空间均为 O(1)。
    """
    # 1. 排序，得到 x < y < z
    x, y, z = sorted((a, b, c))

    # 2. 计算最小移动次数
    if x + 1 == y and y + 1 == z:          # 已经连续
        min_moves = 0
    elif y - x == 2 or z - y == 2:        # 有一段恰好间隔 2，直接一步完成
        min_moves = 1
    else:                                 # 其余情况最多两步
        min_moves = 2

    # 3. 计算最大移动次数
    # 两侧较大的间距决定我们可以“慢慢逼近”多少次
    max_moves = max(y - x, z - y) - 1

    return [min_moves, max_moves]
```

> **代码要点**  
> - `sorted` 像 **字典的索引**，把三颗石子按从左到右的顺序排好，后面只需要处理这三个数。  
> - `y - x == 2` / `z - y == 2` 表示 **中间有唯一的空位**，把远端石子直接搬进去即可一次结束。  
> - `max(y - x, z - y) - 1` 正是 “最宽的那段距离减去 1”，对应“每一步只把端点往里挪 1”。  

---

#### 复杂度  

- **时间复杂度**：`O(1)` —— 只做常数次比较、加减运算。  
  - 用大白话说，就是“无论输入多大，运行时间几乎不变”。  
- **空间复杂度**：`O(1)` —— 只用了几个整数变量。  

相比暴力搜索，时间从“几千万次循环”降到了“几次算术”，几乎瞬间完成。

---

## 心得  

- **核心技巧**：  
  1. **把三颗石子排序**，把问题抽象成「左端点、中心、右端点」的关系。  
  2. **观察每一步对端点距离的影响**，得到最小步数只能是 0/1/2 的结论。  
  3. **利用距离递减的单调性**，直接推导最大步数公式 `max(distance) - 1`。  

- **此技巧适用的题型**（类似思路）  
  1. **“把数组压缩成连续区间”**（如 `1005. K 次取反后使数组非递减` 中的区间移动）。  
  2. **“端点移动”** 类游戏（如 LeetCode 1040. Moving Stones Until Consecutive 的变体）。  
  3. **“距离递减/递增”** 的贪心题（如 `1657. Determine if Two Strings Are Close` 中的字符计数比较）。  

- **一句话总结解题钥匙**：  
  **“把问题化成端点距离的单调变化，利用极值（0、1、2）和最大间距的差值即可快速得出答案”。**  

---

## 反思  

- **第一反应**：看到“只能搬端点石子”，立刻想到“状态空间很小，直接 BFS”。这能得到正确答案，但不够高效。  
- **最容易踩的坑**  
  1. **忘记排序**：如果不把 `a,b,c` 排序，后续的 `x,y,z` 关系会乱掉。  
  2. **特判 `1 2 4`**：此时 `y-x=1`、`z-y=2`，最小步数是 1（因为右端点可以直接搬到 3），容易误判为 2。  
  3. **最大步数公式写反**：有些人会误写成 `z - x - 2`，但这在 `1,2,100` 时会得到 97 而非正确的 `max(1,98)-1 = 97`（恰好相同），但在其他不对称情况下会出错。  

- **下次遇到同类题**：  
  **第一步**先把所有关键元素（位置、长度、区间） **排序或标准化**，然后 **分析每一步对“极值”（最小/最大） 的影响**，看能否直接写出 O(1) 的数学公式。这样往往可以跳过暴力搜索，直接得到最优解。