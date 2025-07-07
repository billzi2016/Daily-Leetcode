# #3256. 放置三个车的最大价值和 I / Maximum Value Sum by Placing Three Rooks I

> 难度：困难 · 标签：Array、Dynamic Programming、Matrix、Enumeration · [LeetCode 链接](https://leetcode.com/problems/maximum-value-sum-by-placing-three-rooks-i/)

---

## 题目（英文原版）

**Description**

You are given a m x n 2D array board representing a chessboard, where board[i][j] represents the value of the cell (i, j).
Rooks in the same row or column attack each other. You need to place three rooks on the chessboard such that the rooks do not attack each other.
Return the maximum sum of the cell values on which the rooks are placed.

**Examples**

**Example 1:**

```
Input: board = [[-3,1,1,1],[-3,1,-3,1],[-3,2,1,1]]
Output: 4
Explanation:

We can place the rooks in the cells (0, 2) , (1, 3) , and (2, 1) for a sum of 1 + 1 + 2 = 4 .
```

**Example 2:**

```
Input: board = [[1,2,3],[4,5,6],[7,8,9]]
Output: 15
Explanation:
We can place the rooks in the cells (0, 0) , (1, 1) , and (2, 2) for a sum of 1 + 5 + 9 = 15 .
```

**Example 3:**

```
Input: board = [[1,1,1],[1,1,1],[1,1,1]]
Output: 3
Explanation:
We can place the rooks in the cells (0, 2) , (1, 1) , and (2, 0) for a sum of 1 + 1 + 1 = 3 .
```

**Constraints**

- 3 <= m == board.length <= 100
- 3 <= n == board[i].length <= 100
- -109 <= board[i][j] <= 109

---

## 题目（中文翻译）

给定一个 `m x n` 的二维数组 `board` 表示棋盘，其中 `board[i][j]` 表示单元格 `(i, j)` 的数值。  
车（rook）在同一行或同一列会相互攻击。你需要在棋盘上放置 **三个车**，使得它们互不攻击。  
返回这三个车所放置单元格数值的最大可能和。

**示例 1**  
**输入**: `board = [[-3,1,1,1],[-3,1,-3,1],[-3,2,1,1]]`  
**输出**: `4`  
**解释**:  
我们可以将车放在单元格 `(0, 2)`, `(1, 3)`, `(2, 1)`，得到的和为 `1 + 1 + 2 = 4`。

**示例 2**  
**输入**: `board = [[1,2,3],[4,5,6],[7,8,9]]`  
**输出**: `15`  
**解释**:  
我们可以将车放在单元格 `(0, 0)`, `(1, 1)`, `(2, 2)`，得到的和为 `1 + 5 + 9 = 15`。

**示例 3**  
**输入**: `board = [[1,1,1],[1,1,1],[1,1,1]]`  
**输出**: `3`  
**解释**:  
我们可以将车放在单元格 `(0, 2)`, `(1, 1)`, `(2, 0)`，得到的和为 `1 + 1 + 1 = 3`。

**约束条件**  
- `3 <= m == board.length <= 100`  
- `3 <= n == board[i].length <= 100`  
- `-10^9 <= board[i][j] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **每一颗车** 当成一次选择，枚举所有可能的放法，然后挑出满足“不同行、不同列”且价值和最大的那一种。

- **数据结构**：我们只需要遍历二维数组 `board`，可以把它想象成一张棋盘，`board[i][j]` 就是格子 `(i, j)` 上的分数。  
- **暴力枚举** 的步骤类似于“把所有格子都写在纸上，然后从中挑出 3 个不在同一行也不在同一列的格子”。这就像在字典里查单词：我们把所有单词列出来，再一个个尝试组合。

**为什么正确**  
只要我们把所有合法的三子组合都检查一遍，最大值必然会被找到——这就是“穷举法”。不管棋盘多大，只要遍历完所有组合，答案就一定在其中。

**复杂度分析**  

- 棋盘上有 `m·n`（最多 10 000）个格子。  
- 从中挑 3 个的组合数是 `C(m·n, 3) ≈ (m·n)^3 / 6`，在最坏情况下约为 `10⁴³ / 6 ≈ 1.6·10¹¹`，远远超出计算机的承受范围。  
- 空间上我们只需要保存原始数组，额外开销几乎为 `O(1)`。

> **大白话**：时间复杂度 `O((m·n)³)` 就像让 10 000 个人排队买票，每次都要让他们三两两地重新排队检查一次，根本不可能在几秒钟内完成。空间复杂度 `O(1)` 则是说我们几乎不需要额外的内存。

#### 代码（Python）

```python
# 下面的代码仅作“暴力思路演示”，在实际提交时会超时
def maxRookSum_bruteforce(board):
    m, n = len(board), len(board[0])
    best = -10**18
    cells = [(i, j) for i in range(m) for j in range(n)]

    for a in range(len(cells)):
        i1, j1 = cells[a]
        for b in range(a + 1, len(cells)):
            i2, j2 = cells[b]
            if i1 == i2 or j1 == j2:        # 同行或同列直接跳过
                continue
            for c in range(b + 1, len(cells)):
                i3, j3 = cells[c]
                if i3 in (i1, i2) or j3 in (j1, j2):
                    continue
                cur = board[i1][j1] + board[i2][j2] + board[i3][j3]
                best = max(best, cur)
    return best
```

#### 复杂度

- **时间复杂度**：`O((m·n)³)` —— 组合数非常大，实际不可接受。  
- **空间复杂度**：`O(1)` —— 只使用了常数级的额外空间。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于「枚举所有格子」的三重循环。  
我们需要 **限制枚举的维度**，而不失去完整性。  

观察到：

1. **行数 ≤ 100，列数 ≤ 100**，两者都不大。  
2. 只需要 **挑 3 列**（或 3 行），然后在这 3 列里挑出 3 行，使得每行只取一次。  

于是可以把问题转化为：

> 选定 3 列 `c1, c2, c3`，在所有行中挑出 3 行，使得每行只使用这 3 列中的 **恰好一个**，且价值和最大。

这正好是 **“在 3 列上做最大权匹配（size = 3）”**。  
因为列的数量只有 3，**状态压缩 DP（位掩码）** 能在 O(m·2³) 时间内完成一次匹配。

**步骤细化**

1. **枚举所有列三元组**  
   列数最多 100，`C(100,3) = 161,700`，可以轻松遍历。

2. **对固定的列三元组进行 DP**  
   - 用一个长度为 `8`（`2³`）的数组 `dp[mask]` 保存当前已经占用的列集合对应的最大价值和。  
   - 初始 `dp[0] = 0`，其余为负无穷（表示不可达）。  
   - 遍历每一行 `r`：  
        - 读取该行在这 3 列上的分数 `v[0], v[1], v[2]`。  
        - 对所有已有的 `mask`（0~7），尝试把第 `k` 列（`k` 对应位）加入（前提是该位在 `mask` 中未被占用），得到 `newMask = mask | (1 << k)`，更新 `dp[newMask] = max(dp[newMask], dp[mask] + v[k])`。  
        - 同时也可以“什么都不选”，即保持原 `dp[mask]`（这一步自然在代码里通过不修改实现）。  
   - 经过所有行后，`dp[7]`（二进制 `111`）即表示已经选满 3 列且行互不相同的最大和。

3. **取所有列三元组的最大值** 即为答案。

**为什么正确**  
- **列三元组遍历**：题目要求的 3 只车必须落在 3 列上，任意合法解对应唯一的列三元组。我们遍历所有列三元组，必然会覆盖真正的最优解所在的列集合。  
- **DP 保证行互不相同**：在 DP 过程中每次只能从当前行选 **至多** 一个列（因为我们只对 `mask` 加入一次位），因此同一行不可能被选两次，满足“行不冲突”。  
- **位掩码完整性**：`mask` 的每一位代表对应列是否已经被占用，遍历完所有行后 `mask = 111` 意味着 3 列都已被占用且对应的 3 行互不相同。  

**时间复杂度**  

- 列三元组数：`C(n,3) = O(n³)`（在本题 `n ≤ 100`，约 1.6×10⁵）。  
- 对每个三元组的 DP：遍历 `m` 行，每行对 `8` 个 `mask` 以及最多 `3` 种加入方式，时间 `O(m·2³·3) = O(m)`（常数因子很小）。  
- 综合：`O(C(n,3)·m) = O(n³·m)`，在最坏情况下约 `1.6·10⁷` 次基本操作，完全可以在 1 秒左右跑完。  

**空间复杂度**  

- 只需 `dp[8]` 这 8 个整数，外加常数级临时变量 → `O(1)`。

> **对比**：暴力解 `O((m·n)³)` 天文数字 → 最优解 `O(n³·m)` 只相当于几千万次运算，差距相当于把“跑马拉松”改成“快跑 100 米”。

#### 代码（Python）

```python
from itertools import combinations

def maxRookSum(board):
    """
    board: List[List[int]]
    返回在不同行、不同列放置 3 个车能够得到的最大价值和
    """
    m, n = len(board), len(board[0])
    INF_NEG = -10**18          # 代表 “不可达”
    answer = INF_NEG

    # 1) 枚举所有列的三元组 (c1, c2, c3)
    for c1, c2, c3 in combinations(range(n), 3):
        # dp[mask]：已经占用的列集合为 mask 时的最大和
        dp = [INF_NEG] * 8      # 2^3 = 8 种状态
        dp[0] = 0                # 什么都不选的初始状态

        # 2) 对每一行尝试选或不选
        for r in range(m):
            v1, v2, v3 = board[r][c1], board[r][c2], board[r][c3]
            vals = [v1, v2, v3]

            # 复制一份旧的 dp，防止本轮更新相互影响
            old = dp[:]

            # 枚举已有的 mask
            for mask in range(8):
                if old[mask] == INF_NEG:
                    continue      # 这个状态不可达，跳过

                # 尝试把当前行的第 k 列加入（如果该列尚未被占用）
                for k in range(3):
                    bit = 1 << k
                    if mask & bit:      # 该列已经被占，用不了
                        continue
                    new_mask = mask | bit
                    dp[new_mask] = max(dp[new_mask], old[mask] + vals[k])

        # dp[7] 对应 111，三列全部被占用
        answer = max(answer, dp[7])

    return answer
```

**代码说明（关键行中文注释）**

- `combinations(range(n), 3)`：把所有列的三元组列举出来，就像把所有可能的“列组合”写在纸上。
- `dp = [INF_NEG] * 8`：用 8 个格子保存 3 列的占用情况，`8 = 2³`。
- `old = dp[:]`：在处理同一行时，先把上一行的结果拷贝出来，防止本行的多次更新相互干扰（相当于“一次只改一行”）。
- `if mask & bit: continue`：如果这列已经被别的行占用了，就不能再选，保证“列不冲突”。
- `dp[new_mask] = max(dp[new_mask], old[mask] + vals[k])`：把当前行选第 `k` 列的价值加入，取更大的那个，确保“价值最大”。

#### 复杂度

- **时间复杂度**：`O(C(n,3) * m) = O(n³·m)`  
  - 对于最大输入（`m = n = 100`）约为 `1.6×10⁷` 次基本循环，运行在几百毫秒内。  
- **空间复杂度**：`O(1)`  
  - 只使用了常数级的 DP 表和几条临时变量。

---

## 心得

- **核心技巧**：**枚举列（或行）三元组 + 位掩码 DP**，把原本的“三维”搜索压缩到 “两维” 再用 DP 完成配对。  
- **适用题型**  
  1. “在矩阵中挑 k 个元素，要求行列互不相同”——如 *Maximum Value Sum by Placing K Rooks*（K 任意）。  
  2. “从若干组中各挑一个，且总数固定”——比如 “选择 3 条不相交的航线使收益最大”。  
  3. “小规模的二分匹配”——当左侧集合（列）规模很小，用位掩码 DP 求最大匹配。  
- **一句话总结**：**把列数固定下来，利用位掩码 DP 把“行不冲突”变成“状态转移”，即可在 O(n³·m) 内搞定三子匹配**。

---

## 反思

- **第一反应**：直接把所有格子组合枚举，想当然地认为电脑能跑完。  
- **最容易踩的坑**  
  - **时间爆炸**：忽视组合数的指数级增长，导致代码在最坏情况下根本跑不完。  
  - **忘记“行不冲突”**：只保证列不同而忘记同一行只能选一次，会得到非法解。  
  - **负数处理**：格子值可能为负，初始化 DP 时必须用足够小的负数（如 `-10**18`），否则会把 “不选” 当成 0 导致错误。  
- **下次类似题的第一步**：先 **固定规模更小的一侧**（列或行），再用 **位掩码 DP** 或 **匈牙利算法的简化版** 处理配对，避免直接三重枚举。这样思路清晰、实现简洁，也能保证通过所有测试。