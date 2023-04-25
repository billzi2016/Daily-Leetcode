# #2218. 从堆中选择 K 枚硬币的最大价值 / Maximum Value of K Coins From Piles

> 难度：困难 · 标签：Array、Dynamic Programming、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/maximum-value-of-k-coins-from-piles/)

---

## 题目（英文原版）

**Description**

There are n piles of coins on a table. Each pile consists of a positive number of coins of assorted denominations.
In one move, you can choose any coin on top of any pile, remove it, and add it to your wallet.
Given a list piles, where piles[i] is a list of integers denoting the composition of the ith pile from top to bottom, and a positive integer k, return the maximum total value of coins you can have in your wallet if you choose exactly k coins optimally.

**Examples**

**Example 1:**

```
Input: piles = [[1,100,3],[7,8,9]], k = 2
Output: 101
Explanation:
The above diagram shows the different ways we can choose k coins.
The maximum total we can obtain is 101.
```

**Example 2:**

```
Input: piles = [[100],[100],[100],[100],[100],[100],[1,1,1,1,1,1,700]], k = 7
Output: 706
Explanation:
The maximum total can be obtained if we choose all coins from the last pile.
```

**Constraints**

- n == piles.length
- 1 <= n <= 1000
- 1 <= piles[i][j] <= 105
- 1 <= k <= sum(piles[i].length) <= 2000

---

## 题目（中文翻译）

给定桌面上有 `n` 堆硬币。每一堆包含若干枚正面值不同的硬币（positive number of coins of assorted denominations）。  
一次操作中，你可以从任意一堆的顶部取走一枚硬币（choose any coin on top of any pile），将其放入你的钱包（wallet）。  

给定数组 `piles`，其中 `piles[i]` 是一个整数列表，表示第 `i` 堆从顶部到底部的硬币面值；再给定正整数 `k`，请返回恰好取走 `k` 枚硬币后，你的钱包中可以得到的 **最大总价值**（maximum total value）。

**示例 1**  
**示例 2**  
**约束条件**  

### 示例

#### 示例 1
```
Input: piles = [[1,100,3],[7,8,9]], k = 2
Output: 101
Explanation:
上述图示展示了选择 k 枚硬币的不同方式。
我们能够得到的最大总价值为 101。
```

#### 示例 2
```
Input: piles = [[100],[100],[100],[100],[100],[100],[1,1,1,1,1,1,700]], k = 7
Output: 706
Explanation:
如果我们从最后一堆取走全部硬币，则可以获得最大总价值。
```

### 约束条件
- `n == piles.length`
- `1 <= n <= 1000`
- `1 <= piles[i][j] <= 10^5`
- `1 <= k <= sum(piles[i].length) <= 2000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举**所有可能的取法：  
- 对每一堆 `i`，我们可以取 `0、1、2 … len(piles[i])` 个硬币（只能从顶部依次取）。  
- 把每堆取的个数记作 `take[i]`，要求 `take[0] + take[1] + … + take[n‑1] = k`。  
- 对于满足这个等式的每一种组合，计算对应的价值总和，取最大值。

可以把这件事想象成**挑选不同口味的糖果**：每个口味的糖果装在一列，只能从最上面吃，吃多少就决定了拿走的价值。我们要把所有口味的吃法凑成恰好 `k` 颗糖，找出价值最高的那种。

**为什么正确**：因为我们遍历了“所有合法的取法”，其中必然包含最优的那一种，所以最大值一定会被找到。

**时间/空间复杂度**  
- 这是一种 **指数级** 的搜索。设 `m_i = len(piles[i])`，则每堆都有 `m_i+1` 种取法，总的组合数是 `∏ (m_i+1)`，在最坏情况下接近 `2^k`（因为 `k ≤ Σ m_i`），随 `k` 指数增长。  
- 空间上只需要保存递归栈深度 `O(n)`。

> **大白话**：如果把 `O(2^k)` 想象成“每增加一次取硬币的机会，就要把答案表翻一倍”，当 `k=20` 时已经要翻 **一百万** 次，根本不可行。

#### 代码（Python）

```python
from typing import List

def maxValueOfCoins_bruteforce(piles: List[List[int]], k: int) -> int:
    n = len(piles)
    # 预先算好每堆取前 j 枚硬币的前缀和，方便后面求价值
    prefix = []
    for pile in piles:
        cur = [0]                     # prefix[0] = 0，表示不取
        s = 0
        for coin in pile:
            s += coin
            cur.append(s)            # cur[j] = 前 j 枚硬币的价值总和
        prefix.append(cur)

    best = 0

    def dfs(idx: int, remain: int, cur_sum: int):
        """遍历第 idx 堆之后的所有取法"""
        nonlocal best
        if idx == n:                  # 所有堆都决定完了
            best = max(best, cur_sum)
            return
        # 这堆最多只能取 min(len(pile), remain) 枚
        max_take = min(len(piles[idx]), remain)
        for t in range(max_take + 1):  # t = 0 … max_take
            # 前缀和直接给出取 t 枚的价值
            dfs(idx + 1, remain - t, cur_sum + prefix[idx][t])

    dfs(0, k, 0)
    return best
```

#### 复杂度

- **时间复杂度**：`O(∏ (m_i+1))`，在最坏情况下约等于 `O(2^k)`，指数级增长，实际会因为 `k ≤ 2000` 而完全不可运行。
- **空间复杂度**：`O(n + Σ m_i)` 用于存前缀和 + 递归栈 `O(n)`，总体是线性空间。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到**两个瓶颈**：

1. **重复计算**：不同的取法会产生很多相同的子问题，例如“前 3 堆已经取了 5 枚硬币，后面的选择完全相同”。  
2. **组合枚举**：直接枚举所有合法的 `take[i]` 组合导致指数级。

这正好适合**动态规划（Dynamic Programming，DP）**——把大问题拆成**子问题**，记录每个子问题的最优解，避免重复计算。

---

##### 2.1 子问题定义

设 `dp[i][c]` 为**只考虑前 `i` 堆（0 … i‑1）并恰好取 `c` 枚硬币时的最大价值**。  
答案即为 `dp[n][k]`（全部堆、恰好取 `k` 枚）。

---

##### 2.2 状态转移

对第 `i` 堆（下标从 `0` 开始）我们可以取 `t` 枚硬币，`t` 的取值范围是 `0 … min(len(piles[i]), c)`。  
取了 `t` 枚后，剩下的 `c‑t` 枚必须由前 `i` 堆完成：

```
dp[i+1][c] = max_{0 ≤ t ≤ min(len(pile_i), c)} ( dp[i][c-t] + prefix_i[t] )
```

- `dp[i][c-t]`：前 i 堆已经取了 `c‑t` 枚的最优价值。  
- `prefix_i[t]`：第 i 堆取前 `t` 枚硬币的价值总和（使用前缀和一次算好）。

这一步的核心是**把每堆的取法视作一次“背包”选择**：我们在已有的价值上“加”上当前堆的某个取法。

---

##### 2.3 初始化

- `dp[0][0] = 0`：不取任何堆、取 0 枚价值为 0。  
- 其它 `dp[0][c] = -∞`（不可达），在实现中可以直接用 `0` 并在转移时只考虑合法的 `c`。

---

##### 2.4 实现细节

1. **前缀和**：和暴力解一样，先把每堆的前缀和值算出来，`prefix_i[t]` 能在 `O(1)` 取到。  
2. **空间压缩**：`dp[i+1][*]` 只和 `dp[i][*]` 有关，可以只保留两行，甚至用一维数组倒序更新。这里采用 **一维 DP**：遍历每堆时，从 `k` 倒着遍历到 `0`，防止本轮更新的值被后面的 `t` 再使用。  
3. **时间界限**：`n ≤ 1000`，`k ≤ 2000`，每堆的大小总和 ≤ 2000。双层循环的复杂度是 `O(n * k * avg_len)`，最坏约 `O(n * k²)`，即 `2000 * 2000 = 4·10⁶`，在 Python 中毫秒级可接受。

---

##### 2.5 类比帮助理解

把每堆看成**一段可选的菜肴**，每道菜有不同的“口味价值”。我们要在总共只能点 `k` 道菜的限制下，挑选出价值最高的组合。动态规划就像 **把点菜的过程分成多轮**：先决定前几道菜怎么点（`dp[i][*]`），再在第 `i+1` 道菜上做选择，最后得到完整的点菜方案。

#### 代码（Python）

```python
from typing import List

def maxValueOfCoins(piles: List[List[int]], k: int) -> int:
    """
    动态规划解法
    dp[c] 表示当前已经处理完若干堆后，恰好取 c 枚硬币的最大价值
    """
    # 1️⃣ 计算每堆的前缀和，prefix[i][t] = 前 t 枚硬币的价值总和
    prefix = []
    for pile in piles:
        cur = [0]               # 0 枚时价值为 0
        s = 0
        for coin in pile:
            s += coin
            cur.append(s)       # 累加得到前缀和
        prefix.append(cur)

    # 2️⃣ 初始化 DP，一维数组，长度为 k+1，全部为 0（取 0 枚价值为 0）
    dp = [0] * (k + 1)

    # 3️⃣ 逐堆遍历
    for i, pre in enumerate(prefix):
        m = len(pre) - 1          # 这堆最多可以取多少枚
        # 必须倒序遍历 c，防止本轮更新的 dp 被同一堆的后续 t 使用
        for c in range(k, -1, -1):
            # 对当前堆尝试取 t 枚，t 不能超过 c，也不能超过堆的大小
            max_take = min(m, c)
            best = dp[c]          # 先把「不取」的情况记下来
            for t in range(1, max_take + 1):
                # dp[c-t] 是之前堆取了 c-t 枚的最优价值
                # pre[t] 是本堆取 t 枚的价值
                cand = dp[c - t] + pre[t]
                if cand > best:
                    best = cand
            dp[c] = best          # 更新 dp[c] 为本堆处理完后的最优

    return dp[k]
```

> **代码要点注释**  
> - `pre[t]` 的意义相当于“查字典”：`t` 是钥匙，返回的是对应的价值（前缀和）。  
> - `for c in range(k, -1, -1)` 是“倒着装箱”，防止同一堆的取法相互影响。  
> - `best = dp[c]` 先保留“不取本堆”的情况，随后尝试所有合法的 `t`。

#### 复杂度

- **时间复杂度**：`O(n * k * avg_len)`，在最坏情况下 `avg_len` 接近 `k`，即 `O(n * k²)`。对本题的约束（`n ≤ 1000, k ≤ 2000`）约等于 `4·10⁶` 次运算，运行毫秒级。  
  > 与暴力的指数级 `O(2^k)` 相比，这里是**多项式**时间，真正可行。

- **空间复杂度**：`O(k)` 用于一维 DP，再加上前缀和的 `O(Σ len(piles)) ≤ 2000`，整体是线性空间。

---

## 心得

- **核心技巧**：**动态规划 + 前缀和**。先把每堆取前 `j` 枚的价值预先算好（前缀和），再用 DP 把各堆的取法“装箱”。  
- **适用场景**  
  1. 多个**序列**（堆、数组、行）中只能从前面取若干元素，且总取数有上限。  
  2. “背包”类问题的**分组背包**（每组只能选 0~size 个，且选的顺序固定）。  
  3. 类似 **“分配 K 项资源到 N 项任务”** 的最优化问题，如 LeetCode 2140 *"Solving Questions With Brainpower"*（分组背包）等。  
- **一句话总结**：把每堆的“取前 j 枚价值”先算好，再用 **DP 把各堆的取法像装箱一样逐层合并**，就能在多项式时间内得到最优解。

---

## 反思

- **第一反应**：看到“每堆只能从顶部取”，立刻想到**前缀和**；看到“恰好取 k 枚”，想到**背包**。于是脑中浮现“分组背包 + 前缀和” 的画面。  
- **最容易踩的坑**  
  1. **边界**：`k` 可能大于某些堆的长度，需要 `min(len(pile), remain)`；  
  2. **倒序更新**：如果正序遍历 `c`，本轮的 `dp[c]` 会被同一堆的后续 `t` 覆盖，导致错误答案；  
  3. **前缀和的长度**：记得在 `prefix[i]` 开头放一个 `0`，方便表示“取 0 枚”。  
- **下次类似题的第一步**：  
  1. 判断是否可以**把每个子结构的“前缀价值”预处理**；  
  2. 把“恰好取固定数量”转化为**分组背包**的状态转移框架。  

祝你玩得开心，算法之路越走越顺！