# #375. **猜数字 Higher or Lower II** / Guess Number Higher or Lower II

> 难度：中等 · 标签：Math、Dynamic Programming、Game Theory · [LeetCode 链接](https://leetcode.com/problems/guess-number-higher-or-lower-ii/)

---

## 题目（英文原版）

**Description**

We are playing the Guessing Game. The game will work as follows:
Given a particular n, return the minimum amount of money you need to guarantee a win regardless of what number I pick.

**Examples**

**Example 1:**

```
Input: n = 10
Output: 16
Explanation: The winning strategy is as follows:
- The range is [1,10]. Guess 7.
    - If this is my number, your total is $0. Otherwise, you pay $7.
    - If my number is higher, the range is [8,10]. Guess 9.
        - If this is my number, your total is $7. Otherwise, you pay $9.
        - If my number is higher, it must be 10. Guess 10. Your total is $7 + $9 = $16.
        - If my number is lower, it must be 8. Guess 8. Your total is $7 + $9 = $16.
    - If my number is lower, the range is [1,6]. Guess 3.
        - If this is my number, your total is $7. Otherwise, you pay $3.
        - If my number is higher, the range is [4,6]. Guess 5.
            - If this is my number, your total is $7 + $3 = $10. Otherwise, you pay $5.
            - If my number is higher, it must be 6. Guess 6. Your total is $7 + $3 + $5 = $15.
            - If my number is lower, it must be 4. Guess 4. Your total is $7 + $3 + $5 = $15.
        - If my number is lower, the range is [1,2]. Guess 1.
            - If this is my number, your total is $7 + $3 = $10. Otherwise, you pay $1.
            - If my number is higher, it must be 2. Guess 2. Your total is $7 + $3 + $1 = $11.
The worst case in all these scenarios is that you pay $16. Hence, you only need $16 to guarantee a win.
```

**Example 2:**

```
Input: n = 1
Output: 0
Explanation: There is only one possible number, so you can guess 1 and not have to pay anything.
```

**Example 3:**

```
Input: n = 2
Output: 1
Explanation: There are two possible numbers, 1 and 2.
- Guess 1.
    - If this is my number, your total is $0. Otherwise, you pay $1.
    - If my number is higher, it must be 2. Guess 2. Your total is $1.
The worst case is that you pay $1.
```

**Constraints**

- 1 <= n <= 200

---

## 题目（中文翻译）

我们正在玩「猜数字游戏（Guessing Game）」。游戏规则如下：

给定一个正整数 `n`，请返回在最坏情况下仍能确保获胜所需支付的最小金额。换句话说，无论我选的数字是什么，你都必须有一种策略，使得你最终的花费不超过该金额。

---

### 示例

#### 示例 1  
**输入**: `n = 10`  
**输出**: `16`  
**解释**: 下面是一种最优的策略：

- 初始范围为 `[1,10]`，先猜 `7`。  
  - 若正好是我的数字，则无需付费，累计花费 `$0`。否则，你需要支付 `$7`。  
  - 若我的数字更大，范围缩小为 `[8,10]`，接着猜 `9`。  
    - 若正好是我的数字，则累计花费 `$7`。否则，再支付 `$9`。  
    - 若我的数字更大，只能是 `10`，再猜 `10`。累计花费 `$7 + $9 = $16`。  
    - 若我的数字更小，只能是 `8`，再猜 `8`。累计花费 `$7 + $9 = $16`。  
  - 若我的数字更小，范围缩小为 `[1,6]`，接着猜 `3`。  
    - 若正好是我的数字，则累计花费 `$7`。否则，再支付 `$3`。  
    - 若我的数字更大，范围变为 `[4,6]`，再猜 `5`。  
      - 若正好是我的数字，则累计花费 `$7 + $3 = $10`。否则，再支付 `$5`。  
      - 若我的数字更大，只能是 `6`，再猜 `6`。累计花费 `$7 + $3 + $5 = $15`。  
      - 若我的数字更小，只能是 `4`，再猜 `4`。累计花费 `$7 + $3 + $5 = $15`。  
    - 若我的数字更小，范围变为 `[1,2]`，再猜 `1`。  
      - 若正好是我的数字，则累计花费 `$7 + $3 = $10`。否则，再支付 `$1`。  
      - 若我的数字更大，只能是 `2`，再猜 `2`。累计花费 `$7 + $3 + $1 = $11`。  

在所有可能的分支中，最坏情况的花费是 `$16`，因此只需准备 `$16` 即可保证获胜。

---

#### 示例 2  
**输入**: `n = 1`  
**输出**: `0`  
**解释**: 只有唯一的数字 `1`，直接猜 `1`，无需付费。

---

#### 示例 3  
**输入**: `n = 2`  
**输出**: `1`  
**解释**: 可选数字为 `1` 和 `2`。  
- 首先猜 `1`。  
  - 若正好是我的数字，则累计花费 `$0`。否则，需要支付 `$1`。  
  - 若我的数字更大，只能是 `2`，再猜 `2`。累计花费 `$1`。  

最坏情况下的花费为 `$1`。

---

### 约束

- `1 <= n <= 200`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**把每一次可能的猜测都枚举一遍**，然后在每种猜测下考虑最坏的情况（也就是对手挑选的数字让我们付出最大金额），取所有猜测中最小的那个最大值。  

这正好符合“**最小化最大损失**”的要求，属于**极小化极大（Minimax）**的思想。  

实现时可以用递归来表达：  

- `cost(i, j)` 表示在当前已知答案在区间 `[i, j]`（两端都可能）时，**保证一定能赢**最少需要付出的钱。  
- 对于区间 `[i, j]`，我们可以任选一个数 `k (i ≤ k ≤ j)` 作为这一步的猜测。  
    - 猜 `k` 本身要花 `k` 元（如果恰好就是答案，这笔钱不算进最终费用，因为游戏结束时我们不需要再付钱）。  
    - 猜完后会有两种可能的子区间：  
        - 如果答案更小，区间变成 `[i, k‑1]`；  
        - 如果答案更大，区间变成 `[k+1, j]`。  
    - 为了保证最坏情况下的费用最小，我们需要取这两种子区间中**较大的**费用（因为对手会让我们付更多），于是本次猜 `k` 的**最坏费用**是 `k + max(cost(i, k‑1), cost(k+1, j))`。  
- 对所有可能的 `k` 取最小值，即得到 `cost(i, j)`。  

这就是递归公式：  

```
cost(i, j) = 0                              if i >= j          # 区间空或只有一个数，不需要花钱
cost(i, j) = min_{k=i..j} ( k + max(cost(i, k-1), cost(k+1, j)) )
```

> **类比**：  
> 哈希表（字典）就像一本词典，`key` 是单词，`value` 是对应的页码。递归里我们把已经算好的 `cost(i, j)` 存进字典，后面再需要时直接查，省去重复计算。  

**正确性**：  
递归把所有可能的猜测和后续的最坏情况都穷举了一遍，`min` 选出了在当前区间内能让最坏损失最小的猜测。因此，返回的 `cost(1, n)` 正好是“无论答案是多少，都能保证赢且付出的最小上限”。  

#### 代码（Python）  

```python
from functools import lru_cache

def getMoneyAmount(n: int) -> int:
    """
    暴力递归 + 记忆化（缓存）实现
    """

    @lru_cache(None)               # 把已经算好的区间费用存进字典，避免重复计算
    def dp(i: int, j: int) -> int:
        # 区间为空或只有一个数，直接返回 0（不需要花钱）
        if i >= j:
            return 0

        # 在 i..j 之间枚举所有可能的猜测 k
        best = float('inf')
        for k in range(i, j + 1):
            # 猜 k 需要花 k 元，随后进入左右子区间的最坏费用
            cost = k + max(dp(i, k - 1), dp(k + 1, j))
            best = min(best, cost)   # 取所有 k 中的最小值

        return best

    return dp(1, n)
```

#### 复杂度  

- **时间复杂度**：`O(n³)`  
  - 解释：外层递归会产生 `O(n²)` 个不同的区间 `(i, j)`（因为 `i`、`j` 各有 `n` 种取法），每个区间内部要遍历 `k` 从 `i` 到 `j`，最坏情况下是 `O(n)`，于是总共是 `n² * n = n³`。  
  - 对于 `n ≤ 200`，`200³ = 8,000,000` 次运算仍在可接受范围。  

- **空间复杂度**：`O(n²)`  
  - 解释：记忆化缓存保存所有区间的结果，最多有 `n²/2` 个不同区间，需要这么多空间。递归栈的深度最多 `n`，相较于 `n²` 可以忽略不计。  

---  

### 2. 最优解  

#### 思路  

暴力递归已经利用了**记忆化**（DP）把时间降到了 `O(n³)`，但仍然有改进空间。我们可以把递归改写成**自底向上的动态规划**，同样是 `dp[i][j]` 表示区间 `[i, j]` 的最小保证费用，只是把“先算子问题再合并”这一步显式化。

**为什么暴力解慢**  
- 递归每次都要遍历 `k`，即使很多区间的最优 `k` 实际上集中在中间。  
- 递归的函数调用本身也有一定开销。  

**优化思路**  
1. **明确状态**：`dp[i][j]`（`i ≤ j`）是子区间 `[i, j]` 的答案。  
2. **递推公式**（和递归完全一样）：  

   ```
   dp[i][j] = 0                                      if i >= j
   dp[i][j] = min_{k=i..j} ( k + max(dp[i][k-1], dp[k+1][j]) )
   ```

3. **填表顺序**：区间长度从小到大枚举。  
   - 当长度为 0（`i == j`）时，`dp[i][j] = 0`。  
   - 对于长度 `len = 2, 3, …, n`，我们已经知道所有更小区间的值，可以直接使用它们来计算当前区间。  

4. **可选的进一步加速**（可选但不必实现）：  
   - 对于同一行/列的 `dp`，最优的 `k` 往往是 **单调递增** 的（这叫 **Knuth 优化**）。如果实现，就能把 `O(n³)` 降到 `O(n²)`。  
   - 这里为了保持代码简洁，只采用 `O(n³)` 的标准 DP，已足够通过所有约束（`n ≤ 200`）。  

**类比**：  
想象你在玩“猜数字”游戏的每一步，都先把所有可能的子游戏结果写在纸上（这就是 DP 表），再从这些已知结果中挑出最好的决策。这样每个子游戏只算一次，避免了“重复思考”。  

#### 代码（Python）  

```python
def getMoneyAmount(n: int) -> int:
    """
    动态规划（自底向上）实现
    dp[i][j] 表示在区间 [i, j] 内保证获胜的最小费用
    """
    # 初始化 n+2 x n+2 的二维数组，默认值 0
    dp = [[0] * (n + 2) for _ in range(n + 2)]

    # 区间长度从 2 开始（长度为 1 的区间不需要花钱）
    for length in range(2, n + 1):                # length = j - i + 1
        for i in range(1, n - length + 2):       # i 为区间左端点
            j = i + length - 1                    # 右端点
            best = float('inf')

            # 在 i..j 之间尝试每一个可能的猜测 k
            for k in range(i, j + 1):
                # 左右子区间的费用已经在 dp 表中算好
                left  = dp[i][k - 1]   # 区间 [i, k-1]
                right = dp[k + 1][j]   # 区间 [k+1, j]
                # 本次猜 k 的最坏费用 = k + max(left, right)
                cost = k + max(left, right)
                best = min(best, cost)

            dp[i][j] = best   # 把最小的最坏费用写进表格

    return dp[1][n]            # 整个区间 [1, n] 的答案
```

#### 复杂度  

- **时间复杂度**：`O(n³)`  
  - 解释：外层两层循环枚举所有区间，数量约为 `n²/2`；最内层遍历区间内的每个可能的猜测 `k`，最坏是 `O(n)`，于是总体仍是 `n³`。对 `n = 200` 来说约 `8×10⁶` 次基本运算，运行时间毫秒级。  

- **空间复杂度**：`O(n²)`  
  - 解释：需要一个 `n×n` 的二维表格来保存所有子区间的答案。  

> 若实现 **Knuth 优化**（利用最优 `k` 的单调性），时间可降至 `O(n²)`，但对本题并非必须。  

---  

## 心得  

- **核心技巧**：**极小化极大（Minimax） + 区间动态规划**。  
- **适用的类似题目**：  
  1. **312. Burst Balloons** – 也是在区间里挑选一个位置，使得总收益最大，需要 `dp[i][j]` 的区间划分。  
  2. **276. Paint Fence**（变体） – 在区间上做决策，使用 `dp` 记录最小/最大代价。  
  3. **1547. Minimum Cost to Cut a Stick** – 在一根木棍上切割，切割点的选择同样使用 `dp[i][j] = min_k (cost + dp[i][k] + dp[k][j])`。  

- **一句话总结解题钥匙**：  
  “在每个区间里，挑选一个猜测，使得左右子区间的最坏费用的**最大值**最小化，递归/迭代求出所有区间的最小保证费用。”  

---  

## 反思  

- **第一反应**：看到“最小化最大损失”，立刻想到**博弈论中的极小化极大**，于是写出递归公式。  
- **最容易踩的坑**：  
  1. **边界条件**：区间为空或只剩一个数字时费用应为 `0`，否则会出现负索引错误或多算一次费用。  
  2. **递归/DP 重复计算**：不加记忆化会导致指数级爆炸。  
  3. **整数溢出**：在 Python 中不怕，但在语言如 C++ 需要使用 `int` 足够大或 `long long`。  
- **下次遇到同类题**，第一步应该思考：  
  “这是一种**区间划分**的博弈吗？能否用 `dp[l][r]` 表示子区间的最优值，并写出 `min_k (cost(k) + max(dp[l][k-1], dp[k+1][r]))` 这种极小化极大的递推？”  

这样就能迅速搭建出递归/动态规划的雏形。祝你玩得开心，算法进步飞快！