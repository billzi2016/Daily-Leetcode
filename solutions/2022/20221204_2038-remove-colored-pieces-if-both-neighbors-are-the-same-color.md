# #2038. 如果两侧相邻颜色相同则移除彩色棋子 / Remove Colored Pieces if Both Neighbors are the Same Color

> 难度：中等 · 标签：Math、String、Greedy、Game Theory · [LeetCode 链接](https://leetcode.com/problems/remove-colored-pieces-if-both-neighbors-are-the-same-color/)

---

## 题目（英文原版）

**Description**

There are n pieces arranged in a line, and each piece is colored either by 'A' or by 'B'. You are given a string colors of length n where colors[i] is the color of the ith piece.
Alice and Bob are playing a game where they take alternating turns removing pieces from the line. In this game, Alice moves first.
Assuming Alice and Bob play optimally, return true if Alice wins, or return false if Bob wins.

**Examples**

**Example 1:**

```
Input: colors = "AAABABB"
Output: true
Explanation:
AAABABB -> AABABB
Alice moves first.
She removes the second 'A' from the left since that is the only 'A' whose neighbors are both 'A'.

Now it's Bob's turn.
Bob cannot make a move on his turn since there are no 'B's whose neighbors are both 'B'.
Thus, Alice wins, so return true.
```

**Example 2:**

```
Input: colors = "AA"
Output: false
Explanation:
Alice has her turn first.
There are only two 'A's and both are on the edge of the line, so she cannot move on her turn.
Thus, Bob wins, so return false.
```

**Example 3:**

```
Input: colors = "ABBBBBBBAAA"
Output: false
Explanation:
ABBBBBBBAAA -> ABBBBBBBAA
Alice moves first.
Her only option is to remove the second to last 'A' from the right.

ABBBBBBBAA -> ABBBBBBAA
Next is Bob's turn.
He has many options for which 'B' piece to remove. He can pick any.

On Alice's second turn, she has no more pieces that she can remove.
Thus, Bob wins, so return false.
```

**Constraints**

- 1 <= colors.length <= 105
- colors consists of only the letters 'A' and 'B'

---

## 题目（中文翻译）

**题目描述**  
有 `n` 个棋子按一条直线排列，每个棋子要么是颜色 `'A'`，要么是颜色 `'B'`。给定一个长度为 `n` 的字符串 `colors`，其中 `colors[i]` 表示第 `i` 块棋子的颜色。  

Alice 和 Bob 正在进行一场游戏，双方交替回合从棋子序列中移除棋子，Alice 先手。  
在一次合法的移动中，玩家只能移除一种颜色的棋子（`'A'` 或 `'B'`），且该棋子左右两侧的相邻棋子颜色必须与其相同。  

假设双方都采用最优策略，若 Alice 能获胜则返回 `true`，否则返回 `false`。

**示例**  

*示例 1*  
```text
Input: colors = "AAABABB"
Output: true
Explanation:
AAABABB -> AABABB
Alice 先手。她移除左侧第二个 `'A'`，因为它是唯一左右相邻均为 `'A'` 的 `'A'`。
接下来轮到 Bob。此时不存在左右相邻均为 `'B'` 的 `'B'`，Bob 无法移动。
因此 Alice 获胜，返回 true。
```

*示例 2*  
```text
Input: colors = "AA"
Output: false
Explanation:
Alice 先手。序列中只有两个 `'A'`，且都位于两端，没有任何 `'A'` 的左右相邻棋子都是 `'A'`，所以 Alice 不能移动。
于是 Bob 获胜，返回 false。
```

*示例 3*  
```text
Input: colors = "ABBBBBBBAAA"
Output: false
Explanation:
ABBBBBBBAAA -> ABBBBBBBAA
Alice 先手。她唯一的合法操作是移除倒数第二个 `'A'`（右侧的第二个 `'A'`）。
ABBBBBBAA -> ABBBBBBAA
轮到 Bob。Bob 有多种可以移除的 `'B'`，任选其一即可。
在 Alice 的第二轮，她已经没有可以移除的棋子。
因此 Bob 获胜，返回 false。
```

**约束条件**  

- `1 <= colors.length <= 10^5`
- `colors` 仅由字符 `'A'` 和 `'B'` 组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**模拟**游戏的每一步：

1. **遍历**当前字符串，找出所有可以被当前玩家删除的棋子。  
   - 对于 Alice 来说，可删的位置必须是 `'A'`，且左、右相邻的字符也都是 `'A'`。  
   - 对于 Bob 则相反，需要 `'B'` 两侧都是 `'B'`。  
2. 如果找到了至少一个合法位置，就**删除**其中的一个（随便挑一个都行，因为我们只想验证“是否存在必胜策略”），然后轮到对手继续上述过程。  
3. 当轮到某个玩家时，**没有合法位置**可删，则该玩家输，游戏结束。

这相当于把游戏当成**树形搜索**：每一次选择都会产生一个新的局面，接下来再继续搜索。  
如果把所有可能的选择都枚举下来，就能得到最终的胜负结果。

> **类比**：把每个局面想象成一本书的章节，找合法棋子就像在目录里查找可以打开的章节；删除后进入下一章节，直到找不到可打开的章节为止，游戏结束。

**为什么正确**：因为我们穷举了所有合法的走法，只要有一种走法能让 Alice 在对手无法行动时获胜，返回 `True`；否则返回 `False`。这正是“完全搜索”所保证的正确性。

#### 代码（Python）

```python
def can_win_bruteforce(colors: str) -> bool:
    # 递归模拟，两位玩家交替行动
    def helper(s: str, turn: int) -> bool:
        # turn = 0 代表 Alice, turn = 1 代表 Bob
        n = len(s)
        # 找到所有当前玩家可以删除的位置
        removable = []
        for i in range(1, n - 1):          # 只能检查非两端的棋子
            if turn == 0 and s[i] == 'A' and s[i-1] == s[i+1] == 'A':
                removable.append(i)
            if turn == 1 and s[i] == 'B' and s[i-1] == s[i+1] == 'B':
                removable.append(i)

        # 没有合法操作 → 当前玩家输 → 返回 False
        if not removable:
            return False

        # 只要有一种删除方式能让对手输，就返回 True
        for idx in removable:
            # 删除字符 idx，形成新局面
            new_s = s[:idx] + s[idx+1:]
            # 对手的回合（turn^1 表示 0↔1 交替）
            if not helper(new_s, turn ^ 1):
                return True   # 发现必胜路径

        # 所有选择都让对手有必胜策略 → 当前玩家必输
        return False

    return helper(colors, 0)   # Alice 先手
```

- `turn ^ 1` 利用位运算在 0 与 1 之间切换，模拟轮流。
- `removable` 收集所有可以删除的下标；若为空则直接判负。

#### 复杂度

- **时间复杂度**：`O(2^m)`（指数级），其中 `m` 是所有合法删除次数的总和。  
  因为每一步我们都要遍历整个字符串（`O(n)`），而递归树的深度最多是 `m`，分支数在最坏情况下接近 `2^m`，这在 `n` 甚至 `10⁵` 时根本不可接受。  
  用大白话说，就是“每一次都要把所有可能的棋子都尝试一次，次数会爆炸”。

- **空间复杂度**：`O(m)`，递归栈的深度最多等于删除次数 `m`。  

> 暴力解只能在 `n` 很小（比如 ≤10）的情况下跑通，用来帮助我们理解游戏的本质，但不适合作为正式答案。

---

### 2. 最优解

#### 思路  

从暴力解出发，**瓶颈**在于我们每一步都要遍历整条字符串并且递归搜索所有可能的走法。实际上，这个游戏的走法**相互独立**，不受对手具体怎么走的影响。我们可以从以下两点观察到这一点：

1. **只能在同色连续块内部删除**  
   - 只有当左、右相邻都是同色时，才可以删除该棋子。  
   - 换句话说，合法的删除只能发生在长度 `≥ 3` 的同色连续块（比如 `"AAA"`、`"BBBBB"`）的**内部**位置。块的两端永远不可删，因为缺少一个邻居。

2. **删除一个内部棋子只会把块长度减 1**  
   - 假设有一段长度为 `k` 的 `'A'` 块（`k ≥ 3`），我们可以把它内部的任意一个 `'A'` 删除。  
   - 删除后，块仍然是连续的 `'A'`，只不过长度变成 `k-1`。  
   - 于是 **该块还能再删 `k-2` 次**（因为最终块会缩到长度 2，无法再删除）。  

   因此，对于 Alice（只关心 `'A'`），她在整个游戏中最多能删的次数等于所有 `'A'` 块的 `(len - 2)` 之和。Bob 同理，只看 `'B'` 块。

3. **玩家的可用次数互不影响**  
   - Alice 删除 `'A'` 并不会影响任何 `'B'` 块的长度，同理 Bob 删除 `'B'` 也不会影响 `'A'` 块。  
   - 所以 **Alice 能删的次数**（记作 `cntA`）是固定的，**Bob 能删的次数**（记作 `cntB`）也是固定的，二者互不干扰。  

4. **谁先用完合法走法，谁就输**  
   - 两位玩家交替行动，若 `cntA > cntB`，说明 Alice 拥有更多的合法步数，Bob 会在自己的回合里先没有可删的棋子而输。  
   - 若 `cntA ≤ cntB`，Bob 至少可以跟上或超过 Alice 的步数，最终 Alice 会先无法行动而输。  

> **结论**：只需要比较两者的“潜在移动次数”。  
> - `cntA = Σ(max(0, lenA_i - 2))`（对每个 `'A'` 连续块）  
> - `cntB = Σ(max(0, lenB_i - 2))`（对每个 `'B'` 连续块）  
> - 返回 `cntA > cntB` 即可。

#### 代码（Python）

```python
def winner_of_game(colors: str) -> bool:
    """
    返回 True 表示 Alice（先手）必胜，False 表示 Bob 必胜。
    思路：统计所有连续块的可删除次数，比较两者大小。
    """
    cntA = cntB = 0          # Alice、Bob 各自的潜在移动次数
    i = 0
    n = len(colors)

    while i < n:
        j = i
        # 找到以 i 为起点的同色连续块的右边界（不含）
        while j < n and colors[j] == colors[i]:
            j += 1
        block_len = j - i    # 块的长度

        if colors[i] == 'A':
            # 只有长度 ≥3 的块才有可删位置，能删 (len-2) 次
            cntA += max(0, block_len - 2)
        else:  # colors[i] == 'B'
            cntB += max(0, block_len - 2)

        i = j                # 继续处理下一个块

    # Alice 先手，只有她的潜在步数更多才会赢
    return cntA > cntB
```

- `while i < n` 与内部的 `while j < n ...` 用来一次遍历找到所有连续块，时间 **只遍历一次**，所以是线性 `O(n)`。
- `max(0, block_len - 2)` 把长度小于 3 的块自动计为 0（因为没有合法删除）。

#### 复杂度

- **时间复杂度**：`O(n)`，只需要一次线性扫描字符串。  
  用大白话说，就是“把字符串看一遍，顺手把每段相同颜色的长度记下来”，不需要递归或多次遍历。

- **空间复杂度**：`O(1)`，只用常数个整数变量记录计数，不随 `n` 增长。

> 与暴力解相比，时间从指数级降到线性，空间也从递归栈的 `O(m)` 降到常数，完全可以应对 `10⁵` 规模的输入。

---

## 心得

- **核心技巧**：把游戏的“可行动次数”抽象为 **每个连续块的可删次数**，并利用**独立性**（A 块只影响 Alice，B 块只影响 Bob）把复杂的博弈简化为单纯的计数比较。  
- **适用的题型**  
  1. “移除相邻相同颜色的棋子” 系列（如 LeetCode 2038 `Remove Colored Pieces if Both Neighbors are the Same Color`）。  
  2. 只涉及 **同色块内部删除** 且两位玩家分别控制不同颜色的游戏。  
  3. 任何可以把**局面划分为互不干扰子局面**的博弈题（如 Nim 游戏的分块化思路）。  
- **一句话总结**：**比较两位玩家各自可以进行的最大移动次数，谁多谁赢**。

---

## 反思

- **第一反应**：看到“相邻相同颜色才能删除”，本能想到逐步模拟，每次找可删位置并删除。  
- **最容易踩的坑**  
  1. **忘记两端不可删**：只要左或右缺少一个邻居，就不能删除。  
  2. **误以为对手的走法会影响自己的次数**：实际上两种颜色的块互不干扰。  
  3. **边界情况**：长度为 1 或 2 的块根本没有合法删除，需要 `max(0, len-2)` 防止负数。  
- **下次遇到同类题**：第一步先**统计连续块的长度**，看能否把游戏转化为“每个块能提供多少次操作”，再比较双方的总次数是否决定胜负。这样就能立刻跳出暴力搜索的陷阱。