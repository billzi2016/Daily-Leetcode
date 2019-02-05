# #279. 完全平方数 / Perfect Squares

> 难度：中等 · 标签：Math、Dynamic Programming、Breadth-First Search · [LeetCode 链接](https://leetcode.com/problems/perfect-squares/)

---

## 题目（英文原版）

**Description**

Given an integer n, return the least number of perfect square numbers that sum to n.
A perfect square is an integer that is the square of an integer; in other words, it is the product of some integer with itself. For example, 1, 4, 9, and 16 are perfect squares while 3 and 11 are not.

**Examples**

**Example 1:**

```
Input: n = 12
Output: 3
Explanation: 12 = 4 + 4 + 4.
```

**Example 2:**

```
Input: n = 13
Output: 2
Explanation: 13 = 4 + 9.
```

**Constraints**

- 1 <= n <= 104

---

## 题目（中文翻译）

给定一个整数 `n`，返回能够表示为若干完全平方数（perfect square）之和的最少个数。  
完全平方数是某个整数的平方；换句话说，它是一个整数与其自身相乘的结果。例如，1、4、9、16 是完全平方数，而 3、11 不是。

**Example 1:**  
**Example 2:**  

**Constraints:**  

- `1 <= n <= 10^4`

**示例：**  

**示例 1:**  
Input: n = 12  
Output: 3  
Explanation: 12 = 4 + 4 + 4.

**示例 2:**  
Input: n = 13  
Output: 2  
Explanation: 13 = 4 + 9.

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是「把 n 拆成若干个完全平方数」——  
我们把所有可能的完全平方数（1、4、9、16 …）都列出来，然后尝试所有拆法，找出使用最少个数的那一种。

> **类比**：想象你有若干种面额的硬币（1、4、9、16…），要凑出总额 *n*，你可以随意挑选硬币组合。暴力解就像把所有可能的挑法都写下来，然后挑出硬币最少的那种。

实现上可以使用递归（深度优先搜索）：

1. 先算出 `sqrt(n)`，得到所有不超过 `n` 的完全平方数 `sq = i*i`（`i = 1 … sqrt(n)`）。  
2. 对每个 `sq`，递归求解「剩余 `n - sq` 需要多少个完全平方数」  
3. 把当前使用的一个 `sq` 加进去，取所有递归分支的最小值。

只要递归能走到 `n = 0`（此时不需要任何数），就可以返回答案。  
因为我们尝试了 **所有** 可能的拆法，这个方法一定能得到正确答案——只不过会非常慢。

#### 代码（Python）

```python
import math
from functools import lru_cache  # 用来记忆已经算过的子问题

def numSquares_bruteforce(n: int) -> int:
    """
    暴力递归求最少完全平方数个数
    """
    # 记忆化递归，避免重复计算相同的子问题
    @lru_cache(maxsize=None)
    def dfs(remaining: int) -> int:
        if remaining == 0:                # 正好凑齐，不需要再加数
            return 0
        # 最差情况是全用 1（因为 1 是完全平方数），上限设为 remaining
        best = remaining
        # 枚举所有可能的完全平方数
        limit = int(math.isqrt(remaining))   # sqrt(remaining) 的整数部分
        for i in range(1, limit + 1):
            sq = i * i
            # 递归求解剩余部分的最小个数，加上当前选的 1 个
            best = min(best, 1 + dfs(remaining - sq))
        return best

    return dfs(n)
```

> **关键行解释**  
> - `math.isqrt(remaining)`：返回 `remaining` 的整数平方根，等价于 `int(math.sqrt(...))`，但更安全。  
> - `@lru_cache`：把已经算好的 `remaining` 对应的答案存下来，后面再出现同样的 `remaining` 时直接返回，省去重复递归。

#### 复杂度

- **时间复杂度**：`O(k^n)`（指数级），这里的 `k` 约等于 `√n`，因为每一步我们都要尝试 `√remaining` 种选择，而且递归深度最坏可达 `n`（全用 `1`）。直观上可以把它想象成「每走一步都有 `√n` 条路可走」，所以会非常慢。  
- **空间复杂度**：`O(n)`，递归栈最深可能到 `n`（全用 `1`），再加上记忆化表最多存 `n` 个子问题。

> **大白话**：如果 `n = 100`，暴力解相当于要尝试上千上万次不同的拆法，根本跑不完。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 出在「重复计算」和「大量不必要的搜索」：

- **重复计算**：不同的路径会得到相同的「剩余值」，比如 `12 = 4 + 4 + 4` 与 `12 = 9 + 1 + 1 + 1` 都会在递归中多次求 `dfs(4)`、`dfs(3)` 等。  
- **不必要的搜索**：我们从大到小枚举每一种平方数，但很多组合根本不可能是最优解。

**优化思路**：把「子问题」的答案保存下来，**自底向上**逐步构造答案——这正是**动态规划（Dynamic Programming，DP）**的核心思想。  

我们定义：

> `dp[i]` = 把整数 `i` 表示成若干完全平方数的最少个数  

显然 `dp[0] = 0`（凑成 0 不需要任何数）。  
对于任意 `i (1 ≤ i ≤ n)`，我们可以尝试把 `i` 的最后一个完全平方数设为 `j*j`（`j` 从 `1` 到 `√i`），那么：

```
dp[i] = min( dp[i - j*j] + 1 )   （遍历所有可能的 j）
```

- `dp[i - j*j]` 表示「剩余部分」已经最少用了多少个平方数。  
- `+1` 表示我们又加上了一个 `j*j`。

这样，只要我们已经算出了所有小于 `i` 的 `dp`，就可以在 **O(√i)** 的时间内求出 `dp[i]`。把 `i` 从 `1` 递增到 `n`，最终 `dp[n]` 就是答案。

> **类比**：这好比在玩「找零」游戏，你已经知道「凑出 1、2、3 …」各需要最少几枚硬币，现在要凑出 `i`，只要把「`i` 减去一种硬币面额」后剩下的最优解加上这枚硬币，就是 `i` 的最优解。

#### 代码（Python）

```python
import math

def numSquares_dp(n: int) -> int:
    """
    动态规划求最少完全平方数个数
    dp[i] 表示凑成 i 所需的最少完全平方数个数
    """
    # 初始化 dp 数组，大小为 n+1，全部设为一个“大数”，这里用 n+1 因为最坏情况全用 1
    dp = [n + 1] * (n + 1)
    dp[0] = 0  # base case

    # 自底向上计算 dp[1] … dp[n]
    for i in range(1, n + 1):
        # 枚举所有可能的完全平方数 j*j（j <= sqrt(i)）
        limit = int(math.isqrt(i))
        for j in range(1, limit + 1):
            sq = j * j
            # dp[i] = min(dp[i], dp[i - sq] + 1)
            dp[i] = min(dp[i], dp[i - sq] + 1)

    return dp[n]
```

> **关键行解释**  
> - `dp = [n + 1] * (n + 1)`：先把每个位置设为「不可能的最大值」，这样后面 `min` 时不会误选。  
> - `limit = int(math.isqrt(i))`：只需要枚举到 `√i`，因为更大的数的平方已经超过 `i`，不可能作为最后一项。  
> - `dp[i - sq] + 1`：`dp[i - sq]` 已经是「剩余部分」的最优解，`+1` 表示再加上这枚 `sq`。

#### 复杂度

- **时间复杂度**：`O(n * √n)`。外层循环跑 `n` 次，内层最多遍历 `√i ≤ √n` 次。可以把它想象成「对每个数，你最多检查 √n 种可能的平方数」。
- **空间复杂度**：`O(n)`。我们需要一个长度为 `n+1` 的数组 `dp` 来存放所有子问题的答案。

> 与暴力解相比，时间从指数级降到了多项式级（几千次运算即可解决 `n = 10⁴`），在实际运行中几乎是瞬间完成。

---

## 心得

- **核心技巧**：把「把 n 拆成若干完全平方数」转化为「子问题的最优子结构」并使用**动态规划**自底向上求解。  
- **适用的题型**  
  1. **最少硬币找零**（LeetCode 322）——同样是「用最少数量的硬币凑出目标金额」。  
  2. **剪绳子**（LeetCode 343）——把绳子切成若干段，使乘积最大，也可以用 DP。  
  3. **背包问题的 0‑1 版**（LeetCode 416）——决定是否使用某个物品来达到最优价值。  
- **一句话总结**：把「整体」拆成「子问题」后，只要把「子问题的最优解」记下来，就能一步步构造出「整体的最优解」。

---

## 反思

- **第一反应**：看到「最少」两个字，就想到「遍历所有组合」——这就是暴力递归的冲动。  
- **最容易踩的坑**  
  - 忘记把 `dp[0]` 初始化为 `0`，导致递推时基准不对。  
  - 在枚举平方数时没有限制 `j ≤ √i`，会产生不必要的循环甚至数组越界。  
  - 对 `n` 较大时仍使用递归，导致栈溢出或运行超时。  
- **下次第一步**：先判断「是否有子问题的最优子结构」——如果有，立刻考虑 **动态规划**（或 BFS）而不是直接暴力搜索。这样可以把时间从天文数字降到可接受的范围。