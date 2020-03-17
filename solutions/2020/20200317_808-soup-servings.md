# #808. 汤的分配 / Soup Servings

> 难度：中等 · 标签：Math、Dynamic Programming、Probability and Statistics · [LeetCode 链接](https://leetcode.com/problems/soup-servings/)

---

## 题目（英文原版）

**Description**

You have two soups, A and B, each starting with n mL. On every turn, one of the following four serving operations is chosen at random, each with probability 0.25 independent of all previous turns:
Note:
The process stops immediately after any turn in which one of the soups is used up.
Return the probability that A is used up before B, plus half the probability that both soups are used up in the same turn. Answers within 10-5 of the actual answer will be accepted.

**Examples**

**Example 1:**

```
Input: n = 50
Output: 0.62500
Explanation: 
If we perform either of the first two serving operations, soup A will become empty first.
If we perform the third operation, A and B will become empty at the same time.
If we perform the fourth operation, B will become empty first.
So the total probability of A becoming empty first plus half the probability that A and B become empty at the same time, is 0.25 * (1 + 1 + 0.5 + 0) = 0.625.
```

**Example 2:**

```
Input: n = 100
Output: 0.71875
Explanation: 
If we perform the first serving operation, soup A will become empty first.
If we perform the second serving operations, A will become empty on performing operation [1, 2, 3], and both A and B become empty on performing operation 4.
If we perform the third operation, A will become empty on performing operation [1, 2], and both A and B become empty on performing operation 3.
If we perform the fourth operation, A will become empty on performing operation 1, and both A and B become empty on performing operation 2.
So the total probability of A becoming empty first plus half the probability that A and B become empty at the same time, is 0.71875.
```

**Constraints**

- 0 <= n <= 109

---

## 题目（中文翻译）

你有两种汤，A 汤和 B 汤，每种初始容量均为 `n` mL。每一回合，随机选择以下四种供应操作中的一种，四种操作的选择概率均为 `0.25`，且相互独立：

1. 从 A 汤中供应 `100` mL，B 汤供应 `0` mL。  
2. 从 A 汤中供应 `75` mL，B 汤供应 `25` mL。  
3. 从 A 汤中供应 `50` mL，B 汤供应 `50` mL。  
4. 从 A 汤中供应 `25` mL，B 汤供应 `75` mL。  

如果某种汤的剩余量小于该操作要求的供应量，则只供应该汤剩余的全部量（即供应量取剩余量与要求量的最小值）。**只要任意一次回合结束时有一种汤的容量为 `0`，整个过程立即停止**。

返回 **A 汤先用完的概率** 加上 **两种汤在同一回合同时用完的概率的一半**。答案在 `10⁻⁵` 以内的误差均被视为正确。

---

## 示例

### 示例 1  
**输入**  
```text
n = 50
```  

**输出**  
```text
0.62500
```  

**解释**  
- 若执行前两种操作中的任意一种，A 汤会先变为空。  
- 若执行第三种操作，A 与 B 汤会在同一次回合同时变为空。  
- 若执行第四种操作，B 汤会先变为空。  

因此，A 先变为空的概率加上两者同回合变空概率的一半为  
`0.25 × (1 + 1 + 0.5 + 0) = 0.625`。

### 示例 2  
**输入**  
```text
n = 100
```  

**输出**  
```text
0.71875
```  

**解释**  
- 执行第一种操作，A 汤会先变为空。  
- 执行第二种操作时，A 汤会在执行第 `[1, 2, 3]` 步时先变空，第 `4` 步时两者同时变空。  
- 执行第三种操作时，A 汤会在执行第 `[1, 2]` 步时先变空，第 `3` 步时两者同时变空。  
- 执行第四种操作时，A 汤会在执行第 `1` 步时先变空，第 `2` 步时两者同时变空。  

综上，A 先变空的概率加上两者同回合变空概率的一半为 `0.71875`。

---

## 约束条件

- `0 ≤ n ≤ 10⁹`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法就是**把所有可能的倒汤顺序枚举出来**，每一种顺序都有 0.25 的概率被选中。  
我们可以把每一次的“倒汤操作”看成一次**随机抽签**，四种操作分别是  

| 操作 | A 递减 | B 递减 |
|------|--------|--------|
| 1    | 100 mL |   0 mL |
| 2    |  75 mL |  25 mL |
| 3    |  50 mL |  50 mL |
| 4    |  25 mL |  75 mL |

从初始的 `(n, n)` 开始，递归地对每一种操作做一次**深度优先搜索**（DFS），直到 **A** 或 **B** 先倒空，或两者同一回合倒空。  

- **正确性**：递归遍历了**所有可能的操作序列**，每条序列的概率正好是 `0.25^k`（k 为这条序列的长度），所以把每条序列对应的结果累加起来，得到的就是题目要求的概率。  
- **为什么会慢**：每一步都有 4 种选择，深度为 `k` 时会产生 `4^k` 条分支。`k` 大约是 `n/25`（因为每次至少倒 25 mL），当 `n` 甚至只有 100 时，`k≈4`，分支数已经是 `4^4=256`；`n=500` 时，`k≈20`，分支数会爆炸到 `4^20≈10^12`，根本算不完。  

#### 代码（Python）

```python
def soupServings_bruteforce(n: int) -> float:
    """
    暴力递归：枚举所有可能的倒汤序列。
    仅用于演示，实际 n 较大时会超时。
    """
    # 四种操作对应的 (A减量, B减量)
    ops = [(100, 0), (75, 25), (50, 50), (25, 75)]

    def dfs(a: int, b: int) -> float:
        # a、b 为当前剩余的毫升数
        if a <= 0 and b <= 0:          # 同时倒空
            return 0.5                # 只算一半概率
        if a <= 0:                     # A 先倒空
            return 1.0
        if b <= 0:                     # B 先倒空
            return 0.0

        prob = 0.0
        for da, db in ops:
            prob += 0.25 * dfs(a - da, b - db)   # 每条分支的概率是 0.25
        return prob

    return dfs(n, n)
```

> **代码注释**  
> - `ops` 就像一本“小字典”，把“操作编号”映射到“倒掉多少毫升”。  
> - `dfs` 函数递归地把当前的汤量 `(a, b)` **拆解** 成四个更小的子问题。  
> - 递归的终止条件对应“汤已经倒完”的三种情况。  

#### 复杂度  

- **时间复杂度**：`O(4^k)`，其中 `k ≈ n / 25`。举例来说，`n = 200` 时大约需要遍历 `4^8 = 65536` 条路径，`n = 500` 时已经是 `4^20 ≈ 10^12`，几乎不可能在合理时间内算完。  
- **空间复杂度**：`O(k)`，递归栈的最大深度等于倒汤的次数 `k`（最多约 `n/25`），每层只保存常数个局部变量。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈** 在于大量的重复计算：不同的递归路径会得到相同的 `(a, b)` 状态，譬如 `(150, 75)` 可能由多条不同的操作序列得到。  
只要把已经算过的状态记下来，下次再遇到相同的 `(a, b)` 就直接使用保存的结果，这就是 **记忆化搜索（Memoization）**，也叫 **动态规划**（DP） 的递归写法。  

进一步观察：

1. **量化单位**  
   四种操作的递减量都是 25 的整数倍（100、75、50、25）。所以我们可以把毫升数 **除以 25 并向上取整**，把问题从 “毫升” 缩小到 “块”。  
   ```text
   n' = ceil(n / 25)
   ```
   此时每次操作对应的减量变成 `(4,0) , (3,1) , (2,2) , (1,3)`，整数更好处理。

2. **状态上限**  
   当 `n'` 很大时，`A` 先倒空的概率几乎是 1。LeetCode 的官方解法给出了经验阈值 `n' >= 200`（即原始 `n >= 200*25 = 5000`）时直接返回 1.0，误差仍在 `1e-5` 以内。这样我们只需要在 `n' ≤ 200` 的范围内做 DP。

3. **递推公式**  
   记 `dp[i][j]` 为当 A 剩 `i` 块、B 剩 `j` 块时 “A 先倒空或同时倒空的概率”。  
   - 终止条件  
     - `i <= 0 and j <= 0` → `dp = 0.5`（两者同一回合倒空，只算一半）  
     - `i <= 0` → `dp = 1.0`（A 先倒空）  
     - `j <= 0` → `dp = 0.0`（B 先倒空）  
   - 递推  
     ```text
     dp[i][j] = 0.25 * ( dp[i-4][j]   +
                        dp[i-3][j-1] +
                        dp[i-2][j-2] +
                        dp[i-1][j-3] )
     ```
     这里的下标如果小于 0，就直接使用上面的终止条件（因为已经倒空）。

4. **实现方式**  
   - **记忆化递归**：用字典 `@lru_cache` 保存已经算过的 `(i, j)`。代码简洁，易于理解。  
   - **自底向上 DP**（可选）：用二维数组填表，时间与记忆化递归相同。这里我们使用记忆化递归，因为它更直观且代码行数少。

#### 代码（Python）

```python
import math
from functools import lru_cache

def soupServings(n: int) -> float:
    """
    动态规划 + 规模缩放
    1. 把毫升数除以 25 并向上取整，得到整数规模 n_。
    2. 当 n_ >= 200 时直接返回 1.0（误差在 1e-5 以内）。
    3. 否则使用记忆化递归求 dp(i, j)。
    """
    # 1）规模缩放
    n_ = math.ceil(n / 25.0)

    # 2）大数直接返回 1.0
    if n_ >= 200:                     # 经验阈值，足够大时几乎必然 A 先倒空
        return 1.0

    # 3）记忆化递归
    @lru_cache(maxsize=None)
    def dp(i: int, j: int) -> float:
        """
        返回当 A 还有 i 块、B 还有 j 块时，
        “A 先倒空 + 0.5 * 同时倒空” 的概率。
        """
        # 终止条件
        if i <= 0 and j <= 0:          # 同时倒空
            return 0.5
        if i <= 0:                     # A 先倒空
            return 1.0
        if j <= 0:                     # B 先倒空
            return 0.0

        # 递推：四种可能的倒汤操作，每种概率 0.25
        return 0.25 * (dp(i - 4, j) +      # 操作 1
                       dp(i - 3, j - 1) +  # 操作 2
                       dp(i - 2, j - 2) +  # 操作 3
                       dp(i - 1, j - 3))   # 操作 4

    return dp(n_, n_)
```

> **关键行解释**  
> - `math.ceil(n / 25.0)`：把原始毫升数压缩成“块”，相当于把每 25 mL 当作 1 个“单位”。  
> - `if n_ >= 200: return 1.0`：把大规模的输入直接归约为几乎必然的答案，省掉后面的递归。  
> - `@lru_cache`：相当于给递归函数装上了“查字典”的功能，遇到已经算过的 `(i, j)` 直接返回缓存值，避免指数级重复计算。  
> - `dp(i - 4, j)` 等四行：把四种倒汤方式翻译成 **状态转移**，每条路径的概率都是 `0.25`，于是把它们加权求和得到当前状态的答案。

#### 复杂度  

- **时间复杂度**：`O(n_^2)`，其中 `n_ = ceil(n/25)` 且 `n_ ≤ 200`（因为更大的直接返回 1）。在最坏情况下约为 `200 * 200 = 40,000` 次递归调用，极其轻松。  
- **空间复杂度**：`O(n_^2)` 用于缓存所有子状态（最多 40,000 条），递归栈深度最多 `n_`（≤200），整体仍在几百 KB 级别。

相比暴力解，时间从指数级 `4^k` 降到了多项式级 `n_^2`，速度提升数万倍以上。

---

## 心得  

- **核心技巧**：把连续的“倒汤”过程抽象为**带概率的状态转移**，使用**动态规划（记忆化搜索）**求解。  
- **技巧适用的题型**  
  1. 需要在每一步随机选择若干固定操作的概率问题（如 “Two Egg Drop” 的期望步数）。  
  2. “棋盘上走子”类的概率 DP（如 “Knight Probability in Chessboard”）。  
  3. “资源消耗”类的递归概率（如 “Stone Game VII” 的期望值变体）。  
- **一句话总结解题钥匙**：**把每一次随机选择视作状态转移，记忆化所有出现过的状态，利用整数缩放把搜索空间压到可接受范围**。

---

## 反思  

- **第一反应**：直接写递归把四种操作全部展开，想“一遍遍模拟”。这会导致指数级爆炸。  
- **最容易踩的坑**  
  - **规模转换**：忘记除以 25 并向上取整，会导致 DP 表太大甚至超内存。  
  - **边界条件**：`i <= 0 and j <= 0` 必须返回 `0.5`（而不是 1），因为“同时倒空”只算半权重。  
  - **大数截断**：没有设阈值直接递归会导致栈溢出或超时。  
- **下次遇到同类题的第一步**：**检查是否存在固定的递减量或固定的转移模式**，如果有，先把数值尺度化（除公因数），再考虑 DP/记忆化搜索，必要时设一个合理的“足够大即为极限”的阈值。