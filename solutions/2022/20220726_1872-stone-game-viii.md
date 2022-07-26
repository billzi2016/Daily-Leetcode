# #1872. 石子游戏 VIII / Stone Game VIII

> 难度：困难 · 标签：Array、Math、Dynamic Programming、Prefix Sum、Game Theory · [LeetCode 链接](https://leetcode.com/problems/stone-game-viii/)

---

## 题目（英文原版）

**Description**

Alice and Bob take turns playing a game, with Alice starting first.
There are n stones arranged in a row. On each player's turn, while the number of stones is more than one, they will do the following:
The game stops when only one stone is left in the row.
The score difference between Alice and Bob is (Alice's score - Bob's score). Alice's goal is to maximize the score difference, and Bob's goal is the minimize the score difference.
Given an integer array stones of length n where stones[i] represents the value of the ith stone from the left, return the score difference between Alice and Bob if they both play optimally.

**Examples**

**Example 1:**

```
Input: stones = [-1,2,-3,4,-5]
Output: 5
Explanation:
- Alice removes the first 4 stones, adds (-1) + 2 + (-3) + 4 = 2 to her score, and places a stone of
  value 2 on the left. stones = [2,-5].
- Bob removes the first 2 stones, adds 2 + (-5) = -3 to his score, and places a stone of value -3 on
  the left. stones = [-3].
The difference between their scores is 2 - (-3) = 5.
```

**Example 2:**

```
Input: stones = [7,-6,5,10,5,-2,-6]
Output: 13
Explanation:
- Alice removes all stones, adds 7 + (-6) + 5 + 10 + 5 + (-2) + (-6) = 13 to her score, and places a
  stone of value 13 on the left. stones = [13].
The difference between their scores is 13 - 0 = 13.
```

**Example 3:**

```
Input: stones = [-10,-12]
Output: -22
Explanation:
- Alice can only make one move, which is to remove both stones. She adds (-10) + (-12) = -22 to her
  score and places a stone of value -22 on the left. stones = [-22].
The difference between their scores is (-22) - 0 = -22.
```

**Constraints**

- n == stones.length
- 2 <= n <= 105
- -104 <= stones[i] <= 104

---

## 题目（中文翻译）

Alice 和 Bob 交替进行游戏，Alice 先手。  
有 `n` 颗石子（stones）排成一行。每当轮到某个玩家且当前剩余的石子数大于 1 时，他（她）将执行以下操作：

1. 选择左侧的任意连续子数组（subarray），将这些石子全部移除，并将它们的价值之和加入自己的得分。  
2. 将一个价值等于上述和的新石子放回行首。

当只剩下一颗石子时游戏结束。

**分数差（score difference）** 定义为 **Alice 的得分 - Bob 的得分**。Alice 的目标是使分数差最大化，Bob 的目标是使分数差最小化。  
给定整数数组 `stones`（长度为 `n`，其中 `stones[i]` 表示从左起第 `i` 颗石子的价值），返回在双方都采取最优策略（optimal）下的分数差。

## 示例

### 示例 1
**输入**  
```json
stones = [-1,2,-3,4,-5]
```
**输出**  
```
5
```
**解释**  
- Alice 移除前 4 颗石子，得到 `(-1) + 2 + (-3) + 4 = 2`，将 2 加入自己的得分，并在左侧放置价值为 2 的石子。此时 `stones = [2,-5]`。  
- Bob 移除前 2 颗石子，得到 `2 + (-5) = -3`，将 -3 加入自己的得分，并在左侧放置价值为 -3 的石子。此时 `stones = [-3]`。  
- 两人的得分差为 `2 - (-3) = 5`。

### 示例 2
**输入**  
```json
stones = [7,-6,5,10,5,-2,-6]
```
**输出**  
```
13
```
**解释**  
- Alice 移除所有石子，得到 `7 + (-6) + 5 + 10 + 5 + (-2) + (-6) = 13`，将 13 加入自己的得分，并在左侧放置价值为 13 的石子。此时 `stones = [13]`。  
- 两人的得分差为 `13 - 0 = 13`。

### 示例 3
**输入**  
```json
stones = [-10,-12]
```
**输出**  
```
-22
```
**解释**  
- Alice 只能进行一次操作，移除全部两颗石子，得到 `(-10) + (-12) = -22`，将 -22 加入自己的得分，并在左侧放置价值为 -22 的石子。此时 `stones = [-22]`。  
- 两人的得分差为 `(-22) - 0 = -22`。

## 约束条件
- `n == stones.length`
- `2 <= n <= 10^5`
- `-10^4 <= stones[i] <= 10^4`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是**递归枚举所有可能的操作**。  
- 当前局面是一串石头 `stones[l:]`（左边已经被“压缩”为一个新石头，实际只需要关注剩余的右侧）。  
- 玩家可以一次性移除 **至少两块** 的左侧石头，记为 `stones[l..r]`（`r ≥ l+1`），得到的分数是这段石头的和 `sum(l, r)`。  
- 移除后，游戏会在剩下的石头 `stones[r+1:]` 上继续进行，而左边会出现一个新石头，其数值等于 `sum(l, r)`，相当于把 `sum(l, r)` 放在最左边。  
- 因为 Alice 想让 **(Alice 分数 – Bob 分数)** 最大，Bob 想让它最小，这正是**零和博弈**的典型情形。  

我们可以用一个递归函数 `dfs(i)` 表示**从第 i 块石头开始，当前玩家（假设是先手）相对对手能够取得的最大分差**。  
```
dfs(i) = max_{j ≥ i+1} ( prefixSum[j] - dfs(j+1) )
```
- `prefixSum[j]` 是从第 0 块到第 j 块的前缀和，即一次性移除前 `j+1` 块石头的得分。  
- 移除后，轮到对手从 `j+1` 开始继续游戏，`dfs(j+1)` 表示对手相对当前玩家的最大分差，**所以要取负号**（相当于“我得到的分差 = 我这一步得分 – 对手以后能拿的分差”）。  

这就是暴力递归的完整思路。  

**为什么正确？**  
- 递归穷举了所有合法的“移除长度”，没有遗漏。  
- 每一步都考虑了对手随后会以最优方式回应（因为 `dfs` 本身已经是最优），于是递归的返回值正好是“在当前局面下，先手能够保证的最大分差”。  

**复杂度分析（大白话）**  
- 对每个起始位置 `i`，我们都要尝试 `O(n)` 移除长度；而递归的深度最多是 `n`，所以总共会出现 **指数级** 的调用次数（大约 `2^n`），这在 `n ≤ 10^5` 时根本跑不完。  
- 空间方面，递归栈最深 `n`，所以是 `O(n)` 的额外空间。  

#### 代码（Python）  
```python
from typing import List
import sys
sys.setrecursionlimit(10**6)

def stoneGameVIII_bruteforce(stones: List[int]) -> int:
    n = len(stones)

    # 计算前缀和，prefix[i] = stones[0] + ... + stones[i]
    prefix = [0] * n
    cur = 0
    for i, v in enumerate(stones):
        cur += v
        prefix[i] = cur

    from functools import lru_cache

    @lru_cache(None)               # 记忆化，避免重复计算（仍然指数级）
    def dfs(i: int) -> int:
        """从下标 i 开始，先手能取得的最大分差"""
        if i >= n - 1:              # 只剩一块石头，游戏结束，分差为 0
            return 0
        best = -10**18
        # 必须至少移除两块石头，即 j ≥ i+1
        for j in range(i + 1, n):
            # 取前缀和作为本轮得分
            cur_score = prefix[j]
            # 对手从 j+1 开始的最优分差是 dfs(j+1)
            # 本轮分差 = 本轮得分 - 对手以后能取得的分差
            best = max(best, cur_score - dfs(j + 1))
        return best

    return dfs(0)
```

#### 复杂度  
- **时间复杂度**：`O(2^n)`（指数级）——因为每一步都有 `O(n)` 分支，递归深度 `n`。  
- **空间复杂度**：`O(n)`——递归栈和前缀数组占用线性空间。  

> **大白话**：指数级相当于“每增加一个石头，可能的走法就像翻倍”，所以几分钟能算完的只适合 `n ≤ 15` 左右，远远不够本题的规模。

---  

### 2. 最优解  

#### 思路  
从暴力解我们已经得到 **状态转移方程**：  

\[
dp[i] = \max_{j \ge i+1} \bigl( \text{pref}[j] - dp[j+1] \bigr)
\]

- `dp[i]` 表示**从第 i 块石头开始，先手（此时轮到谁都可以视作先手）能够得到的最大分差**。  
- `pref[j]` 是前 `j+1` 块石头的和，即一次性移除到 `j` 的得分。  

**瓶颈在哪里？**  
- 暴力里我们对每个 `i` 都遍历所有 `j`，导致 `O(n^2)`（甚至指数级）时间。  
- 实际上，**`dp[i]` 只依赖于 `dp[i+1]`**，因为 `pref` 是递增的前缀和。  

把方程改写一下，注意 `j` 必须至少是 `i+1`，于是：

\[
dp[i] = \max\bigl( \underbrace{\text{pref}[i+1] - dp[i+2]}_{\text{取最小合法 j=i+1}},
                 \underbrace{\text{pref}[i+2] - dp[i+3}}_{\text{取 j=i+2}},\dots\bigl)
\]

如果从右向左计算 `dp`，**`dp[i]` 的最优取值一定是 `pref[i+1] - dp[i+2]` 与 `dp[i+1]` 中的较大者**。  
为什么？因为：

\[
dp[i+1] = \max_{k \ge i+2} \bigl( \text{pref}[k] - dp[k+1] \bigr)
\]

而 `dp[i]` 的候选集合比 `dp[i+1]` 多了一个选项 `j = i+1`（对应 `pref[i+1] - dp[i+2]`），其余的 `j ≥ i+2` 正好对应 `dp[i+1]` 中的所有选项。于是：

\[
dp[i] = \max\bigl( \text{pref}[i+1] - dp[i+2],\; dp[i+1] \bigr)
\]

这条递推式只需要 **常数时间** 就能得到 `dp[i]`，于是整体可以线性 `O(n)` 求解。

**核心技巧**  
- **前缀和**：把“把左边若干石头的和”一次性算出来，后面直接取值。  
- **从右往左的 DP**：把“以后会怎样”先算好，当前只看两种可能（立即停在 `i+1`，或交给后面的最优策略）。  
- **零和博弈**的“先手得分 - 对手最优得分”形式，转化为上面的递推。

**类比**：想象你在玩“取石子”游戏，每次可以取 **至少两块**，取的总和记为你的得分，然后把这总和重新放回左端，等价于“把剩下的游戏压缩为一个新局面”。从后往前算，就像把一列多米诺倒下，从最右边的最后一步往前推，知道每一步的最佳选择。

#### 代码（Python）  
```python
from typing import List

def stoneGameVIII(stones: List[int]) -> int:
    """
    返回在双方都最优的情况下，Alice 的分数减去 Bob 的分数。
    思路：前缀和 + 从右往左的 DP，时间 O(n)，空间 O(1)（除前缀外）。
    """
    n = len(stones)

    # 1️⃣ 计算前缀和，pref[i] = stones[0] + ... + stones[i]
    pref = [0] * n
    cur = 0
    for i, v in enumerate(stones):
        cur += v
        pref[i] = cur

    # 2️⃣ dp[i] 表示从第 i 块开始，先手能够获得的最大分差
    # 只需要保留 dp[i+1] 和 dp[i+2] 两个后继状态，空间可以 O(1)
    dp_next = 0          # 对应 dp[n] = 0（不存在的下标，游戏已经结束）
    dp_next_next = 0     # 对应 dp[n+1] = 0，统一写法

    # 从倒数第二个位置开始往左遍历（因为必须至少保留两块才能继续）
    for i in range(n - 2, -1, -1):
        # 选取 j = i+1 的情况：得分是 pref[i+1]，随后对手的最佳分差是 dp[i+2]
        take_one_more = pref[i + 1] - dp_next_next
        # 交给后面的最优策略（相当于不立刻取 i+1，而让后面的玩家先决定）
        # 这正是 dp[i+1]，我们已经保存在 dp_next 中
        dp_i = max(take_one_more, dp_next)

        # 更新滚动变量，准备计算更左边的 dp
        dp_next_next = dp_next
        dp_next = dp_i

    # 最终答案就是 dp[0]，即从最左边开始的最大分差
    return dp_next
```

#### 复杂度  
- **时间复杂度**：`O(n)`。我们只遍历一次数组，前缀和和 DP 各一次线性扫描。  
  - 大白话：如果有 `100,000` 块石头，只会做大约 `200,000` 次简单加减，比暴力的指数级快得多，几毫秒就能算完。  
- **空间复杂度**：`O(n)` 用于存前缀和（也可以在原数组上就地累加，进一步压缩到 `O(1)`），额外的 DP 只用了常数个变量。  

---

## 心得  

- **核心技巧**：**前缀和 + 从右往左的动态规划**，把“以后怎么走”提前算好，只在当前考虑两种可能（立刻取最短合法段或交给后面的最优策略）。  
- **适用的题型**：  
  1. **Stone Game 系列**（如 Stone Game VII、Stone Game IX）——经常需要前缀和 + DP。  
  2. **取子游戏**（如 “Removal Game”）——类似的“先手得分 - 后手最优得分”递推。  
  3. **区间 DP** 中“每一步都把左端压缩为一个值” 的情形。  
- **一句话总结解题钥匙**：**把“以后会怎样”先算好，只比较“立刻结束这一步”和“让对手先决定”两种选择**。

---

## 反思  

- **第一反应**：看到“把左边若干石头的和放回左端”，立刻想到**前缀和**，因为每次得分都是一个连续前缀的和。  
- **最容易踩的坑**：  
  - 忘记**至少要移除两块**，导致在 DP 边界条件上出错（如 `i = n-1` 时不应继续）。  
  - 前缀和的下标容易写错：`pref[i]` 表示前 `i+1` 块的和，取 `pref[i+1]` 才对应“移除到第 i+1 块”。  
  - DP 初始值：在数组右侧不存在的状态应该设为 `0`，否则会产生负的虚假分差。  
- **下次遇到同类题**：第一步先 **写出前缀和**，再 **从右往左写递推**，检查是否可以把 `max` 的范围压缩到常数个候选值。这样往往能直接得到 `O(n)` 解。