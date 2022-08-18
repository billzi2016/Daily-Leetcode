# #1900. 玩家相遇的最早和最晚轮次 / The Earliest and Latest Rounds Where Players Compete

> 难度：困难 · 标签：Dynamic Programming、Memoization · [LeetCode 链接](https://leetcode.com/problems/the-earliest-and-latest-rounds-where-players-compete/)

---

## 题目（英文原版）

**Description**

There is a tournament where n players are participating. The players are standing in a single row and are numbered from 1 to n based on their initial standing position (player 1 is the first player in the row, player 2 is the second player in the row, etc.).
The tournament consists of multiple rounds (starting from round number 1). In each round, the ith player from the front of the row competes against the ith player from the end of the row, and the winner advances to the next round. When the number of players is odd for the current round, the player in the middle automatically advances to the next round.
After each round is over, the winners are lined back up in the row based on the original ordering assigned to them initially (ascending order).
The players numbered firstPlayer and secondPlayer are the best in the tournament. They can win against any other player before they compete against each other. If any two other players compete against each other, either of them might win, and thus you may choose the outcome of this round.
Given the integers n, firstPlayer, and secondPlayer, return an integer array containing two values, the earliest possible round number and the latest possible round number in which these two players will compete against each other, respectively.

**Examples**

**Example 1:**

```
Input: n = 11, firstPlayer = 2, secondPlayer = 4
Output: [3,4]
Explanation:
One possible scenario which leads to the earliest round number:
First round: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
Second round: 2, 3, 4, 5, 6, 11
Third round: 2, 3, 4
One possible scenario which leads to the latest round number:
First round: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
Second round: 1, 2, 3, 4, 5, 6
Third round: 1, 2, 4
Fourth round: 2, 4
```

**Example 2:**

```
Input: n = 5, firstPlayer = 1, secondPlayer = 5
Output: [1,1]
Explanation: The players numbered 1 and 5 compete in the first round.
There is no way to make them compete in any other round.
```

**Constraints**

- 2 <= n <= 28
- 1 <= firstPlayer < secondPlayer <= n

---

## 题目（中文翻译）

**描述**  
有一个锦标赛，参与的玩家数量为 `n`。玩家站成一排，按照初始站位从左到右编号为 `1` 到 `n`（玩家 `1` 是最左侧的玩家，玩家 `2` 是第二个，依此类推）。  

锦标赛由多轮比赛组成，轮数从 `1` 开始。**第 `i` 轮** 中，排在前面的第 `i` 位玩家将与排在后面的第 `i` 位玩家对决，获胜者晋级进入下一轮。当本轮的玩家数量为奇数时，位于中间的玩家直接晋级。  

每轮结束后，晋级的玩家会按照他们最初的编号顺序（升序）重新排列成一排，进入下一轮的对决。  

编号为 `firstPlayer` 和 `secondPlayer` 的两位玩家是锦标赛中最强的选手。他们在相遇之前可以击败任意其他玩家。如果其他任意两位玩家相遇，胜负均可由我们自行决定。  

给定整数 `n`、`firstPlayer`、`secondPlayer`，返回一个长度为 `2` 的整数数组，其中第一个值是这两位玩家**最早**可能相遇的轮次，第二个值是**最晚**可能相遇的轮次。

**示例 1**  
```text
输入: n = 11, firstPlayer = 2, secondPlayer = 4
输出: [3,4]
解释:
最早相遇的情形之一:
第 1 轮: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
第 2 轮: 2, 3, 4, 5, 6, 11
第 3 轮: 2, 3, 4          // 第 2 位玩家 (2) 与第 4 位玩家 (4) 在第 3 轮相遇

最晚相遇的情形之一:
第 1 轮: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
第 2 轮: 1, 2, 3, 4, 5, 6
第 3 轮: 1, 2, 4          // 第 2 位玩家 (2) 与第 4 位玩家 (4) 在第 4 轮相遇
...（已截断）
```

**示例 2**  
```text
输入: n = 5, firstPlayer = 1, secondPlayer = 5
输出: [1,1]
解释: 编号为 1 和 5 的玩家在第一轮就相遇，无法让他们在其他轮次相遇。
```

**约束条件**  
- `2 <= n <= 28`  
- `1 <= firstPlayer < secondPlayer <= n`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **把所有可能的比赛过程全部枚举**，然后找出两位最强选手第一次相遇的轮数以及最后一次相遇的轮数。

- **数据结构**：我们可以用一个 **位掩码（bitmask）** 来表示每一轮留下的选手。  
  把 1 … n 编号的选手想象成一本字典，编号是“词”，而位掩码的第 *i* 位是 0 还是 1，就像字典里查不到或查到第 *i* 页一样，决定了第 *i* 位选手是否还在比赛中。

- **为什么这样一定能得到答案**：  
  只要把所有可能的胜负结果都穷举一遍，就没有遗漏的情况。遍历完以后，记录下每种情况下两位最强选手相遇的轮数，最小的就是**最早**的轮数，最大的就是**最晚**的轮数。

- **时间/空间复杂度**（大白话解释）  
  - 每一轮的比赛会把选手数减半（奇数时会多一个“自动晋级”），最多需要 `log₂ n` 轮（大约 5 ~ 6 轮，因为 n ≤ 28）。  
  - 但是每一轮的胜负组合是指数级的：第 1 轮有 `⌊n/2⌋` 场比赛，每场都有 2 种可能（谁赢），所以可能的组合数是 `2^{⌊n/2⌋}`。  
  - 把所有轮次的组合都列出来，时间复杂度大约是 `O(2^{n})`，空间也要保存每一种状态，都是 **爆炸性的**（比如 n=28 时，2⁸≈2.5×10⁸，根本跑不完）。

> **O(n²)**、**O(n³)** 之类的符号只是一种把“跑得快还是慢”量化的方式。这里的 **O(2ⁿ)** 表示“随着选手数量的增加，计算量会几乎翻倍”，对电脑来说是不可接受的。

#### 代码（Python）

```python
from functools import lru_cache
from itertools import product
from math import ceil

def brute_force(n: int, a: int, b: int):
    """仅用于演示，实际会超时。"""

    @lru_cache(None)
    def dfs(players: tuple) -> list:
        """返回所有可能的相遇轮数列表（从当前局面开始计）"""
        m = len(players)
        # 两位最强选手已经在同一局面里，直接返回空列表表示“已经相遇”
        if a not in players or b not in players:
            return []          # 说明已经被淘汰，理论上不会出现
        # 检查本轮是否相遇
        for i in range(m // 2):
            if {players[i], players[m - 1 - i]} == {a, b}:
                return [1]    # 本轮相遇，返回轮数 1
        # 处理奇数中间选手自动晋级的情况
        next_players = []
        # 为每一场比赛枚举两种可能的胜者
        outcomes = []
        for i in range(m // 2):
            left, right = players[i], players[m - 1 - i]
            outcomes.append((left, right))   # 只记录选手编号，后面会遍历取胜者

        # 所有比赛的胜负组合（笛卡尔积）
        all_cases = product(*[(o[0], o[1]) for o in outcomes])
        res = []
        for winners in all_cases:
            nxt = list(winners)
            if m % 2 == 1:                # 中间选手直接晋级
                nxt.append(players[m // 2])
            nxt.sort()                    # 按原始编号升序重新排队
            sub = dfs(tuple(nxt))
            if sub:                        # 如果后面还能相遇
                res.append(1 + sub[0])    # 当前轮数 + 之后的相遇轮数
        return res

    rounds = dfs(tuple(range(1, n + 1)))
    return [min(rounds), max(rounds)]
```

> **注意**：这段代码只用于说明“暴力枚举”的思路，实际运行会在 n=28 时直接卡死。

#### 复杂度

- **时间复杂度**：`O(2^n)` — 随着选手数量的增加，可能的胜负组合会指数级增长，几乎每多一个选手就把计算量翻一番，根本跑不完。
- **空间复杂度**：`O(2^n)` — 需要把每一种状态（选手的存活情况）保存下来以避免重复计算，同样是指数级的。

---

### 2. 最优解

#### 思路  

从暴力解可以看到：**真正需要搜索的不是每一场比赛的具体胜者，而是两位最强选手在每轮结束后会处在第几位**。只要知道他们的**排名**（在剩余选手中的顺序），就能判断他们是否相遇。

**关键观察 1：**  
在一轮结束后，所有留下的选手会按原始编号升序重新排队。  
假设当前还有 `n` 位选手，编号从左到右依次是 `1 … n`。第 `i` 位和第 `n+1-i` 位进行比赛。  
- 如果我们只关心某个选手的**位置** `pos`（而不在乎它到底赢了谁），那么它在下一轮的**可能位置**只能落在下面这个区间：

```
ceil(pos / 2)  ……  pos
```

解释：  
- `ceil(pos/2)` 是它所在的**左侧**配对的编号（如果它在左半边），此时它一定是左配对的胜者，排名不会变小于这个值。  
- `pos` 是它所在的**右侧**配对的编号（如果它在右半边），此时它可能是右配对的胜者，排名可以保持原来的值（因为左配对的选手可能全部被别的强者淘汰，导致它在剩下的选手中排得更靠前）。

**关键观察 2：**  
两位最强选手 **永远不会输**，所以只要它们没有在本轮相遇，它们一定会进入下一轮。  
因此我们只需要递归地 **枚举它们在下一轮可能出现的所有位置组合**，把每一步的轮数累加即可。

**递归定义**  
`dfs(a, b, n)` → 在还有 `n` 位选手、两位最强选手当前分别位于第 `a`、`b` 位（`a < b`）时，**从现在开始**最早和最晚相遇的轮数（包括当前这轮）。

递归过程：

1. **相遇判定**  
   - 若 `a + b == n + 1`，说明它们本轮正好配对，相遇轮数为 `1`（当前轮）。
2. **否则**  
   - 两位选手各自赢得自己的比赛，进入下一轮。  
   - 下一轮的选手总数是 `next_n = (n + 1) // 2`（向上取整，因为奇数会多一个自动晋级的选手）。  
   - 对于 `a`，它在下一轮可能的排名 `na` 在区间 `[ceil(a/2), a]`；同理 `b` 的可能排名 `nb` 在 `[ceil(b/2), b]`。  
   - 只保留满足 `na < nb` 的组合（因为 `a` 的编号比 `b` 小，排名也必须保持顺序）。  
   - 对每一种合法的 `(na, nb)`，递归求子问题 `dfs(na, nb, next_n)`，得到子问题的最早/最晚相遇轮数 `sub_min, sub_max`。  
   - 当前轮数需要再加 `1`（因为我们已经经历了一轮），于是更新全局的最早/最晚答案。

3. **记忆化**  
   - 同样的 `(a, b, n)` 可能会在不同的递归路径中出现多次，使用 `@lru_cache` 把结果缓存下来，避免重复计算。  
   - 由于 `n ≤ 28`，状态总数最多 `28 * 28 * 28 ≈ 2.2×10⁴`，非常小，递归加缓存即可在毫秒级完成。

**为什么这样是最优的**  
- 我们不再枚举每一场具体的胜负，而是只枚举两位选手可能的**排名**，每轮的枚举范围最多 `O(n)`，而递归深度最多 `log₂ n`，整体复杂度大约是 `O(n² log n)`，在本题的约束下完全可以接受。

#### 代码（Python）

```python
from functools import lru_cache
from math import ceil

def earliestAndLatest(n: int, firstPlayer: int, secondPlayer: int):
    """
    返回 [最早相遇的轮数, 最晚相遇的轮数]
    """

    @lru_cache(None)
    def dfs(a: int, b: int, m: int):
        """
        a, b : 当前轮次两位最强选手的排名（1-indexed，且 a < b）
        m   : 当前还有多少选手
        返回 (min_round, max_round) —— 从现在起（包括本轮）最早/最晚相遇的轮数
        """
        # 1. 本轮直接相遇
        if a + b == m + 1:
            return 1, 1   # 只需要本轮

        # 2. 否则进入下一轮
        next_m = (m + 1) // 2          # 向上取整，奇数会多一个自动晋级
        min_round = float('inf')
        max_round = -float('inf')

        # a 在下一轮可能的排名范围
        for na in range(ceil(a / 2), a + 1):
            # b 在下一轮可能的排名范围
            for nb in range(ceil(b / 2), b + 1):
                if na >= nb:          # 必须保持顺序 a 在前
                    continue
                sub_min, sub_max = dfs(na, nb, next_m)
                # 加上当前已经进行的这轮
                min_round = min(min_round, sub_min + 1)
                max_round = max(max_round, sub_max + 1)

        return min_round, max_round

    # 题目保证 firstPlayer < secondPlayer
    return list(dfs(firstPlayer, secondPlayer, n))
```

**代码要点解释（中文注释）**

| 行号 | 解释 |
|------|------|
| 4‑5 | `dfs` 用来递归求解，`@lru_cache` 负责记忆化，防止重复计算同一状态。 |
| 9‑11 | 若两位选手在本轮正好配对（位置之和等于 `m+1`），直接返回 1 轮。 |
| 14 | 计算下一轮的选手总数：向上取整，奇数时会多一个自动晋级的选手。 |
| 18‑21 | 枚举 `a` 在下一轮可能的排名范围 `na`。`ceil(a/2)` 是最左侧配对的编号，`a` 是最右侧配对的编号。 |
| 22‑26 | 同理枚举 `b` 的可能排名 `nb`，并确保 `na < nb`（保持原始顺序）。 |
| 27‑28 | 递归求子问题的最早/最晚相遇轮数。 |
| 30‑31 | 因为我们已经经历了一轮，所以子问题的答案要加 `1`。更新全局最小/最大值。 |
| 34 | 返回当前状态的最早/最晚相遇轮数。 |
| 38‑39 | 调用 `dfs` 并把结果转成列表返回。 |

#### 复杂度

- **时间复杂度**：`O(n² log n)`  
  - 每层递归最多枚举 `O(n)` 个 `na` 与 `O(n)` 个 `nb`，即 `O(n²)` 种组合。  
  - 递归深度不超过 `log₂ n`（因为每轮选手数至少减半），所以整体约为 `O(n² log n)`。  
  - 对于本题的最大 `n = 28`，计算量只有几千次，几乎瞬间完成。

- **空间复杂度**：`O(n³)`（记忆化表的大小）  
  - 状态由 `(a, b, m)` 三个整数决定，`a, b ≤ m ≤ n`，最多 `n³` 种状态。  
  - 递归栈深度 `O(log n)`，可以忽略不计。  

相比暴力的指数级时间，这个 DP 方案在所有合法输入下都能在毫秒级得到答案。

---

## 心得

- **核心技巧**：把“比赛过程”抽象为“两位选手的排名变化”，并用 **记忆化递归（DP）** 枚举所有合法的排名转移。
- **适用的题型**  
  1. 需要在 **多轮配对** 中寻找两元素相遇的最早/最晚时机（如本题）。  
  2. 类似的 “**淘汰赛**” 位置变化问题，如 “Find the Minimum and Maximum Rounds for Two Players to Meet”。  
  3. 需要 **状态压缩**（只关心少数关键元素）而不是完整枚举所有细节的组合问题。
- **一句话总结解题钥匙**：**只追踪关键选手的排名，而不是每一场比赛的胜负**，用 DP 把所有可能的排名转移枚举完即可。

---

## 反思

- **第一反应**：看到“最早”和“最晚”，第一想法就是**暴力枚举所有可能的比赛结果**，因为最直接能得到两者的上下界。
- **最容易踩的坑**  
  1. **忽略奇数轮的自动晋级**：当选手数为奇数时，中间的选手直接进入下一轮，必须在 `next_n = (n+1)//2` 中考虑进去。  
  2. **位置转移的范围写错**：`na`、`nb` 的取值区间是 `[ceil(pos/2), pos]`，不是单纯的 `pos//2` 或者 `pos`。写错会导致遗漏合法情况或产生不合法的状态。  
  3. **忘记记忆化**：没有缓存会导致大量重复子问题，时间会爆炸。  
- **下次类似题的第一步**：先**抽象出关键状态**（本题是两位选手的排名），判断状态转移的合法范围，然后决定是否需要记忆化或动态规划。这样可以把指数级的暴力搜索压缩到多项式时间。