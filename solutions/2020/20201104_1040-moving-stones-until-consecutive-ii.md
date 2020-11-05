# #1040. 移动石子直到连续 II / Moving Stones Until Consecutive II

> 难度：中等 · 标签：Array、Math、Sliding Window、Sorting · [LeetCode 链接](https://leetcode.com/problems/moving-stones-until-consecutive-ii/)

---

## 题目（英文原版）

**Description**

There are some stones in different positions on the X-axis. You are given an integer array stones, the positions of the stones.
Call a stone an endpoint stone if it has the smallest or largest position. In one move, you pick up an endpoint stone and move it to an unoccupied position so that it is no longer an endpoint stone.
The game ends when you cannot make any more moves (i.e., the stones are in three consecutive positions).
Return an integer array answer of length 2 where:

**Examples**

**Example 1:**

```
Input: stones = [7,4,9]
Output: [1,2]
Explanation: We can move 4 -> 8 for one move to finish the game.
Or, we can move 9 -> 5, 4 -> 6 for two moves to finish the game.
```

**Example 2:**

```
Input: stones = [6,5,4,3,10]
Output: [2,3]
Explanation: We can move 3 -> 8 then 10 -> 7 to finish the game.
Or, we can move 3 -> 7, 4 -> 8, 5 -> 9 to finish the game.
Notice we cannot move 10 -> 2 to finish the game, because that would be an illegal move.
```

**Constraints**

- 3 <= stones.length <= 104
- 1 <= stones[i] <= 109
- All the values of stones are unique.

---

## 题目（中文翻译）

给定一个整数数组 `stones`，表示若干颗石子在 X 轴上的不同位置。  
如果一颗石子位于所有石子中最小或最大的坐标，则称其为端点石子（endpoint stone）。  
在一次移动中，你可以挑选一颗端点石子，将其搬到一个未被占用的位置，并且搬动后它不再是端点石子。  
当无法再进行任何移动时（即所有石子恰好占据连续的三个位置），游戏结束。  

返回一个长度为 2 的整数数组 `answer`，其中  
- `answer[0]` 为使游戏结束所需的最小移动次数；  
- `answer[1]` 为使游戏结束所需的最大移动次数。

---

### 示例

**示例 1**  
输入: `stones = [7,4,9]`  
输出: `[1,2]`  
解释:  
- 我们可以将 4 移动到 8，完成一次移动后游戏结束。  
- 或者先将 9 移动到 5，再将 4 移动到 6，完成两次移动后游戏结束。

**示例 2**  
输入: `stones = [6,5,4,3,10]`  
输出: `[2,3]`  
解释:  
- 可以先将 3 移动到 8，然后将 10 移动到 7，完成两次移动后游戏结束。  
- 或者依次将 3→7、4→8、5→9，完成三次移动后游戏结束。  
- 注意，不能将 10 移动到 2，因为这不是合法的移动（搬动后仍会成为端点石子）。

---

### 约束条件

- `3 <= stones.length <= 10^4`
- `1 <= stones[i] <= 10^9`
- 所有 `stones[i]` 均唯一。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举每一步的所有合法移动**，一直搜索到所有石子占据三个连续位置为止。  

- **数据结构**：  
  - 把石子的位置放进 `set`（类似字典的查表，能在 O(1) 时间判断某个位置是否被占用）。  
  - 用 BFS（广度优先搜索）或 DFS（深度优先搜索）遍历状态树，每个状态就是当前石子的集合。  

- **合法移动**：取最左或最右的端点石子（最小或最大坐标），把它搬到任意**未被占用且不是新的端点**的位置。可以把“端点石子”想象成排队最前面或最后面的孩子，只有他们可以离开队伍；搬到的新位置必须不再是最前或最后一个孩子。  

- **结束条件**：石子已经是三个连续整数（比如 `[5,6,7]`），此时没有端点可以再搬动。  

- **正确性**：因为我们把**所有**可能的合法搬动都尝试了一遍，搜索到的最短路径一定是最少步数，所有能走到的终点状态也都会被遍历到，最大步数自然是遍历中出现的最长路径。  

- **时间/空间复杂度**：  
  - 每一步我们可能把端点搬到 `O(range)`（范围可能是 `10^9`）个位置，搜索树的深度最多是 `N`（石子数），所以最坏情况的时间复杂度是 **指数级**，记作 `O(2^N)`（类似每个石子有两种搬法）。  
  - 为了防止重复访问，需要把已经遍历过的状态放进 `visited` 集合，这会占用 **指数级** 的空间。  

> 用大白话说：这相当于把所有可能的走法都列出来，然后一条条检查，根本不可行。

#### 代码（Python）

```python
from collections import deque

def min_max_moves_bruteforce(stones):
    stones = tuple(sorted(stones))
    n = len(stones)
    target = tuple(range(stones[0], stones[0] + n))  # 任意三个连续位置的形式
    # 为了演示，这里只返回最小步数，最大步数的暴力实现非常耗时
    q = deque()
    q.append((stones, 0))          # (当前状态, 已走步数)
    visited = {stones}
    min_moves = None

    while q:
        cur, step = q.popleft()
        # 检查是否已经是连续的
        if all(cur[i] + 1 == cur[i + 1] for i in range(n - 1)):
            min_moves = step
            break

        left, right = cur[0], cur[-1]          # 端点石子
        # 把左端点搬到除左端点外的任意空位，但搬完后不能再是左端点
        for new_pos in range(left + 1, cur[-1]):   # 只枚举区间内的空位
            if new_pos in cur:
                continue
            # 搬完后新的最小值必须不是 new_pos
            if new_pos == min(cur[1], new_pos):
                continue
            new_state = tuple(sorted((new_pos,) + cur[1:]))
            if new_state not in visited:
                visited.add(new_state)
                q.append((new_state, step + 1))

        # 同理处理右端点
        for new_pos in range(cur[0] + 1, right):
            if new_pos in cur:
                continue
            if new_pos == max(cur[-2], new_pos):
                continue
            new_state = tuple(sorted(cur[:-1] + (new_pos,)))
            if new_state not in visited:
                visited.add(new_state)
                q.append((new_state, step + 1))

    # 暴力求最大步数的思路类似，只是要记录所有到达终点的 step 并取最大
    return [min_moves, None]   # 最大步数在暴力实现里不实际给出
```

> **注意**：上述代码仅用于说明思路，实际运行在 LeetCode 的数据规模（`n ≤ 10^4`）下会 **超时**，因此我们需要更高效的算法。

#### 复杂度  

- **时间复杂度**：`O(2^N)`（指数级），因为每一次搬动都有可能产生两条分支，且搜索深度与石子数量 N 成正比。  
- **空间复杂度**：`O(2^N)`，需要保存所有已经访问过的状态，以防止重复搜索。

---

### 2. 最优解  

#### 思路  

从暴力解可以看出，**瓶颈在于枚举所有搬动**。实际上，题目只要求返回 **最少步数** 与 **最多步数**，不需要真的去模拟每一步。我们可以用数学与滑动窗口的思路直接算出答案。

---

#### 2.1 最少步数  

把石子位置排序得到数组 `A`（长度为 `N`），记 `A[0]` 为最左，`A[N‑1]` 为最右。  
我们希望在 **一次搬动** 内把尽可能多的石子放进一个长度为 `N` 的连续区间（因为最终的目标区间恰好有 `N` 个位置）。  

- **滑动窗口**：窗口的左端点固定在 `A[l]`，右端点是 `A[l] + N - 1`（长度 N）。窗口内部的石子数就是 `cnt = r - l + 1`（`r` 为窗口最右侧石子在数组中的下标）。  
- 在所有 `l`（从 0 到 N‑1）中，取 `cnt` 的最大值 `max_inside`。  
- 那么最少搬动次数 = `N - max_inside`（把不在窗口里的石子搬进来）。

**特殊情况**：  
如果窗口已经几乎装满，只缺一个位置，而且缺的那个位置恰好在窗口的两端形成 “空位 + 两个连续石子”，例如 `[1,2,4]`（缺 3）或 `[1,3,4]`（缺 2），按照上面的公式会得到 `2` 步，但实际只需要 **2 步**（因为一次只能搬端点，且只能搬到不再是端点的位置）。  
更常见的特殊情形是 **`N-1`** 个石子已经连续，而剩下的一个石子恰好在最左或最右的空位，导致只能用两步收拢。判定方式：

```
if min_moves == N - 1 and (
        A[N-2] - A[0] == N - 2   # 左边缺一个
    or  A[N-1] - A[1] == N - 2   # 右边缺一个
):
    min_moves = 2
```

---

#### 2.2 最多步数  

想让步数尽可能多，就要 **每一步只搬走一个端点，且只把它搬到离当前端点最近的位置**，这样每一步只“缩小”最大的间隙 1。  

观察数组 `A`，最大的间隙只能出现在两端：

- 左端间隙：`A[1] - A[0] - 1`（左端点与第二个石子之间的空位数）  
- 右端间隙：`A[N-1] - A[N-2] - 1`（右端点与倒数第二个石子之间的空位数）  

我们可以把 **左端点** 一次次搬到右侧的空位，或者把 **右端点** 搬到左侧的空位。每搬一次，间隙会减 1，直到所有石子变成连续的 `N` 个位置。  

因此最多步数 = `max( A[N-1] - A[1] - (N - 2),  A[N-2] - A[0] - (N - 2) )`。  
这里的 `A[N-1] - A[1] - (N-2)` 表示 **把左端点一直搬到右边**，期间可以占用的空位数；同理右端点搬到左边。

---

#### 代码（Python）

```python
def numMovesStonesII(stones):
    """
    返回 [最少移动次数, 最多移动次数]
    思路：
    1) 先排序
    2) 用滑动窗口求最少步数，处理特殊情况
    3) 用两端间隙公式求最多步数
    """
    stones.sort()
    n = len(stones)

    # ---------- 最少步数 ----------
    # 滑动窗口：窗口长度为 n
    max_inside = 0          # 窗口里最多能装多少石子
    r = 0
    for l in range(n):
        # 把右指针尽量往右移动，使窗口仍然长度不超过 n
        while r + 1 < n and stones[r + 1] - stones[l] < n:
            r += 1
        # 窗口内石子数量
        inside = r - l + 1
        max_inside = max(max_inside, inside)

    min_moves = n - max_inside

    # 特殊情况：几乎全部连续，但缺的那个位置在窗口两端
    # 这时理论上只需要 2 步，而不是 n-1 步
    if min_moves == n - 1:
        # 检查左侧缺一个或右侧缺一个
        if stones[n - 2] - stones[0] == n - 2 or stones[n - 1] - stones[1] == n - 2:
            min_moves = 2

    # ---------- 最多步数 ----------
    # 两端间隙分别搬到另一端能产生的最大步数
    max_gap_left  = stones[-1] - stones[1] - (n - 2)   # 把左端点搬到右边
    max_gap_right = stones[-2] - stones[0] - (n - 2)   # 把右端点搬到左边
    max_moves = max(max_gap_left, max_gap_right)

    return [min_moves, max_moves]
```

#### 复杂度  

- **时间复杂度**：`O(N log N)`  
  - 排序 `O(N log N)`（`N ≤ 10⁴`），滑动窗口一次遍历 `O(N)`，其余计算均为 `O(1)`。  
  - 与暴力的指数级相比，几乎是线性的，能够轻松跑完最大测试数据。  

- **空间复杂度**：`O(1)`（不计输入数组本身的存储），只用了常数个额外变量。

---

## 心得  

- **核心技巧**：  
  1. **滑动窗口** 用来统计在长度为 `N` 的连续区间内已有多少石子，从而直接得到最少搬动次数。  
  2. **端点间隙公式**（`max(A[-1] - A[1], A[-2] - A[0]) - (N-2)`）求最多搬动次数，实质是把每一步的“收敛”幅度限制为 1。  

- **适用的题型**：  
  - “把元素搬到连续区间”类问题（如 **Moving Stones Until Consecutive I**）。  
  - “在固定窗口长度内统计元素个数”类问题（如 **Maximum Number of Points Inside a Circle**）。  
  - “利用两端间隙求最大步数”类的排列游戏（如 **Zigzag Conversion** 的类似思路）。  

- **一句话总结解题钥匙**：  
  “先把石子排好序，用窗口找出已经连续的最大子集，剩下的石子就是最少要搬的；最多步数则是把两端的空位一次一次填满。”

---

## 反思  

- **第一反应**：看到“端点石子只能搬动，目标是三个连续位置”，本能地想到**暴力搜索**所有搬动序列。  
- **最容易踩的坑**：  
  - **特殊情况**：`[a, a+1, a+2, …, a+N-2, a+N]`（缺一个中间位置），直接用 `N - max_inside` 会得到 `2`，但有的实现会误算成 `1`。必须额外判断 `min_moves == N-1` 并检查两端间距。  
  - **整数溢出**：位置范围 up to `10⁹`，在计算间隙时要使用 Python 的大整数即可，但在其他语言要注意 64 位。  
  - **窗口长度**：窗口的右边界是 `stones[l] + N - 1`（**长度 N**），而不是 `stones[l] + N`，容易写错导致 `inside` 统计错误。  

- **下次遇到同类题**，第一步应该：  
  1. **排序**，把问题转化为在数轴上的区间统计。  
  2. **思考窗口**：我们关心的是“在多少个连续位置上已经有石子”，而不是具体搬动步骤。  

这样即可快速从暴力思路跳到数学/滑动窗口的最优解。