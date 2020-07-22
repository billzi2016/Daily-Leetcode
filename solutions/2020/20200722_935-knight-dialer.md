# #935. 骑士拨号器 / Knight Dialer

> 难度：中等 · 标签：Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/knight-dialer/)

---

## 题目（英文原版）

**Description**

The chess knight has a unique movement, it may move two squares vertically and one square horizontally, or two squares horizontally and one square vertically (with both forming the shape of an L). The possible movements of chess knight are shown in this diagram:
A chess knight can move as indicated in the chess diagram below:
We have a chess knight and a phone pad as shown below, the knight can only stand on a numeric cell (i.e. blue cell).
Given an integer n, return how many distinct phone numbers of length n we can dial.
You are allowed to place the knight on any numeric cell initially and then you should perform n - 1 jumps to dial a number of length n. All jumps should be valid knight jumps.
As the answer may be very large, return the answer modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: n = 1
Output: 10
Explanation: We need to dial a number of length 1, so placing the knight over any numeric cell of the 10 cells is sufficient.
```

**Example 2:**

```
Input: n = 2
Output: 20
Explanation: All the valid number we can dial are [04, 06, 16, 18, 27, 29, 34, 38, 40, 43, 49, 60, 61, 67, 72, 76, 81, 83, 92, 94]
```

**Example 3:**

```
Input: n = 3131
Output: 136006598
Explanation: Please take care of the mod.
```

**Constraints**

- 1 <= n <= 5000

---

## 题目（中文翻译）

棋盘上的骑士（chess knight）有一种独特的走法：它可以垂直移动两格并水平移动一格，或水平移动两格并垂直移动一格（两者均形成 “L” 形）。骑士的所有可能移动如图所示：

我们将骑士放在下图中的手机键盘上，骑士只能站在数字格子（numeric cell）上（即蓝色格子）。

给定一个整数 `n`，返回可以拨出的长度为 `n` 的不同电话号码的数量。你可以将骑士最初放在任意数字格子上，然后进行 `n - 1` 次跳跃来组成长度为 `n` 的号码。所有跳跃必须是合法的骑士跳跃。

由于答案可能非常大，请返回答案对 `10^9 + 7` 取模后的结果。

**示例 1**  
**输入**: `n = 1`  
**输出**: `10`  
**解释**: 只需要拨出长度为 1 的号码，因此骑士可以放在 10 个数字格子中的任意一个。

**示例 2**  
**输入**: `n = 2`  
**输出**: `20`  
**解释**: 所有合法的两位号码为 `[04, 06, 16, 18, 27, 29, 34, 38, 40, 43, 49, 60, 61, 67, 72, 76, 81, 83, 92, 94]`。

**示例 3**  
**输入**: `n = 3131`  
**输出**: `136006598`  
**解释**: 注意对模数取余。

**约束条件**  
- `1 <= n <= 5000`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的跳法**。  
1. 把键盘想成一张 4 × 3 的格子（数字 0‑9），每个格子只放一个数字。  
2. 先把骑士放在任意一个数字格子上（相当于挑选第 1 位），然后按照骑士的 “L” 形走法（两格直走 + 一格横走）不停跳，跳 `n‑1` 次得到长度为 `n` 的电话号码。  

这相当于在一棵 **十叉树**（第一层有 10 个根）上深度优先搜索：  
- 每走一步，就把当前格子换成所有合法的下一格。  
- 当走到第 `n` 步时，就得到一条完整的电话号码。  

> **类比**：把电话号码看成“从一个城市出发，坐骑士专车一路跳转”，暴力解就是把所有可能的路线全部列出来。

只要把每一次合法跳法全部列举出来，答案一定是对的，因为我们没有遗漏也没有多算。

#### 代码（Python）

```python
MOD = 10 ** 9 + 7

# 骑士在键盘上可以跳到的格子（这里用字典模拟“查字典”）
# key 是当前数字，value 是一个列表，列出所有可以跳到的数字
moves = {
    0: [4, 6],
    1: [6, 8],
    2: [7, 9],
    3: [4, 8],
    4: [0, 3, 9],
    5: [],          # 5 没有合法的骑士跳
    6: [0, 1, 7],
    7: [2, 6],
    8: [1, 3],
    9: [2, 4],
}

def dfs(pos, steps):
    """从数字 pos 开始，已经跳了 steps 步，返回所有可能的电话号码数"""
    if steps == n:               # 已经走完 n 步（包括起点），计数 +1
        return 1
    total = 0
    for nxt in moves[pos]:       # 对每一个合法的下一格递归
        total += dfs(nxt, steps + 1)
    return total

def knightDialer_bruteforce(n):
    if n == 0:
        return 0
    ans = 0
    for start in range(10):      # 任意数字作为起点
        ans += dfs(start, 1)     # 已经用了第一位（steps = 1）
    return ans % MOD
```

> 关键点说明  
> - `moves` 把骑士的跳法抽象成“查字典”，`key` 是词（当前数字），`value` 是页码（可以去的数字）。  
> - 递归深度最多是 `n`（`n ≤ 5000`），但真实运行时会指数级爆炸。  

#### 复杂度  

- **时间复杂度**：`O(10 * 8^{n-1})`  
  - 每一步最多有 8 条分支（实际最多 4 条），所以总的搜索树节点数近似为 `10 * 8^{n-1}`，这就是所谓的 **指数时间**，当 `n` 稍大（比如 10）就已经不可接受。  
- **空间复杂度**：`O(n)`（递归栈的深度），因为只需要记录当前的跳数。  

> 大白话：如果把 `n` 想成 10，时间相当于 10 × 8⁹ ≈ 13 亿次运算，普通电脑根本跑不完。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到 **“每一步只和上一步的状态有关”**，这正是**动态规划（DP）**可以利用的地方。  
- **瓶颈**：暴力解每次都要重新遍历所有可能的路径，重复计算了很多子问题（比如“从 1 开始跳了 3 步”会在不同的递归枝中出现多次）。  
- **优化思路**：把“走到第 i 步、当前位置是哪个数字”这个信息记下来，下次再需要时直接查表，不必重新枚举。

**状态定义**  
`dp[i][d]` = 长度为 `i`、且第 `i` 位是数字 `d` 的合法电话号码数量。  

**状态转移**  
要得到 `dp[i][d]`，只需要把第 `i‑1` 步停在所有能够跳到 `d` 的前驱数字 `p` 的情况加起来：

```
dp[i][d] = Σ dp[i-1][p]   (p ∈ predecessors[d])
```

`predecessors[d]` 与前面的 `moves` 完全对应，只是把方向反过来（同样是字典）。

**初始状态**  
长度为 1 时，骑士可以直接站在任意数字上：

```
dp[1][d] = 1   (对所有 d = 0~9)
```

**答案**  
所有长度为 `n`、以任意数字结尾的计数之和：

```
answer = Σ dp[n][d]   (d = 0~9)
```

**空间优化**  
我们只需要前一步 (`i‑1`) 的数据来计算当前一步 (`i`)，因此可以把二维数组压缩成 **两个长度为 10 的一维数组**（滚动数组），把空间从 `O(n*10)` 降到 `O(10)`。

**取模**  
题目要求对 `10^9+7` 取模，所有加法都要在取模后保存，防止整数溢出。

> **类比**：把 DP 看成“记账本”。每一天（步数）我们只记下“今天手里有多少种可能的数字”，而不是把每一条具体的路径都写下来。

#### 代码（Python）

```python
MOD = 10 ** 9 + 7

# 前驱列表（哪个数字可以跳到当前数字）
pre = {
    0: [4, 6],
    1: [6, 8],
    2: [7, 9],
    3: [4, 8],
    4: [0, 3, 9],
    5: [],               # 5 没有前驱
    6: [0, 1, 7],
    7: [2, 6],
    8: [1, 3],
    9: [2, 4],
}

def knightDialer(n: int) -> int:
    if n == 1:                     # 长度为 1 时直接返回 10
        return 10

    # dp_prev[d] 表示长度为 i-1、以数字 d 结尾的计数
    dp_prev = [1] * 10            # i = 1 时每个数字都有 1 种

    for step in range(2, n + 1):   # 从第 2 步算到第 n 步
        dp_cur = [0] * 10
        for d in range(10):       # 计算每个目标数字 d 的新计数
            total = 0
            for p in pre[d]:      # 累加所有可以跳到 d 的前驱 p
                total += dp_prev[p]
            dp_cur[d] = total % MOD   # 取模防止溢出
        dp_prev = dp_cur          # 滚动数组：当前变成上一轮

    # 最终答案是所有以任意数字结尾的计数之和
    return sum(dp_prev) % MOD
```

> 关键行解释  
> - `pre` 把“可以跳到 d 的前一个格子”列出来，像查字典一样快速定位。  
> - `dp_prev` 和 `dp_cur` 只保存 10 个整数，空间恒定。  
> - `total % MOD` 确保每一步都不超过 10⁹+7。  

#### 复杂度  

- **时间复杂度**：`O(n * 10 * 8)` → 实际上是 `O(n)`，因为每一步只遍历常数个前驱（最多 4 条），所以随着 `n` 增长线性增长。  
  - 与暴力解的指数级 `O(8^{n})` 相比，快了天壤之别。  
- **空间复杂度**：`O(10)` → 常数级空间，只用了两个长度为 10 的数组。  

> 大白话：如果 `n = 5000`，我们只会进行约 `5000 * 10 * 4 ≈ 200k` 次加法，几乎瞬间就能算完。

---

## 心得  

- **核心技巧**：**状态转移的 DP + 滚动数组**（把“只依赖前一步”转化为 O(1) 空间）。  
- **适用的题型**  
  1. “棋子在格子上跳动”类问题（如 *Knight Shortest Path*、*Word Search* 中的跳格子）。  
  2. “固定步长的计数”问题（如 *爬楼梯*、*不同路径*）。  
  3. “带约束的序列计数”问题（如 *数字计数*、*斐波那契变形*）。  
- **一句话总结**：把“每一步只和上一步有关”抽象成 DP，记住前一步的结果，用滚动数组把空间压到常数。

---

## 反思  

- **第一反应**：直接写递归去枚举所有跳法，想到要用 DFS。  
- **最容易踩的坑**  
  - 忘记对 **`5`** 这个格子没有任何合法跳法，要在转移时把它的前驱设为空列表。  
  - 忘记在每一步 **取模**，导致整数溢出或答案不符合要求。  
  - 在滚动数组实现时不小心把 `dp_prev` 与 `dp_cur` 的引用搞混，导致结果被覆盖。  
- **下次类似题**：第一步先写出 **状态转移方程**（dp[i][...]=...），判断是否只依赖前一步，若是就直接使用 **滚动数组**；若需要更远的历史再考虑完整的二维 DP。