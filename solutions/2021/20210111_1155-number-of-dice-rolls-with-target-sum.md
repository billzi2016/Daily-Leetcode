# #1155. 目标和的掷骰子方法数 / Number of Dice Rolls With Target Sum

> 难度：中等 · 标签：Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/number-of-dice-rolls-with-target-sum/)

---

## 题目（英文原版）

**Description**

You have n dice, and each dice has k faces numbered from 1 to k.
Given three integers n, k, and target, return the number of possible ways (out of the kn total ways) to roll the dice, so the sum of the face-up numbers equals target. Since the answer may be too large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: n = 1, k = 6, target = 3
Output: 1
Explanation: You throw one die with 6 faces.
There is only one way to get a sum of 3.
```

**Example 2:**

```
Input: n = 2, k = 6, target = 7
Output: 6
Explanation: You throw two dice, each with 6 faces.
There are 6 ways to get a sum of 7: 1+6, 2+5, 3+4, 4+3, 5+2, 6+1.
```

**Example 3:**

```
Input: n = 30, k = 30, target = 500
Output: 222616187
Explanation: The answer must be returned modulo 109 + 7.
```

**Constraints**

- 1 <= n, k <= 30
- 1 <= target <= 1000

---

## 题目（中文翻译）

你有 `n` 个骰子（dice），每个骰子有 `k` 个面，编号为 `1` 到 `k`。  
给定整数 `n`、`k` 和 `target`，返回在所有 `k^n` 种可能的掷骰子结果中，使得正面数字之和等于 `target` 的方法数。由于答案可能非常大，请返回对 `10^9 + 7` 取模后的结果。

## 示例

### 示例 1
**输入**: `n = 1, k = 6, target = 3`  
**输出**: `1`  
**解释**: 你掷一个有 6 面的骰子。只有一种方式可以得到和为 3。

### 示例 2
**输入**: `n = 2, k = 6, target = 7`  
**输出**: `6`  
**解释**: 你掷两个各有 6 面的骰子。得到和为 7 的方式有 6 种: `1+6`, `2+5`, `3+4`, `4+3`, `5+2`, `6+1`。

### 示例 3
**输入**: `n = 30, k = 30, target = 500`  
**输出**: `222616187`  
**解释**: 需要对 `10^9 + 7` 取模后返回答案。

## 约束条件
- `1 <= n, k <= 30`
- `1 <= target <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的投掷结果**，然后统计其中和等于 `target` 的情况。  
- 对于每个骰子，它有 `k` 种可能的面（1~k），我们可以把每一次投掷看成一次“选数字”。  
- 把 `n` 次投掷的结果放进一个长度为 `n` 的数组里，例如 `[2,5,1,…]`。  
- 把数组里所有数字相加，看看是否等于 `target`，如果是就计数。

这里用到的唯一数据结构是**列表（list）**，它类似于我们平时记事本上的一行行记录，按顺序保存每一次掷出的点数。

为什么能得到正确答案？因为我们把 **所有** 可能的 `k^n` 种组合都遍历了一遍，漏掉的情况不存在，自然统计的结果就是正确的。

> **时间/空间复杂度直观解释**  
> - `k^n` 表示“每个骰子有 `k` 种选择，`n` 个骰子相乘”。如果 `k=6, n=2`，就是 `6*6=36` 种可能。  
> - 当 `n`、`k` 稍大时，这个数会爆炸式增长（比如 `k=30, n=30`，结果是 30 的 30 次方，天文数字），所以这套办法在实际中会超时。  
> - 空间上我们只需要保存当前的一个组合（长度 `n`），所以空间是 `O(n)`。

#### 代码（Python）

```python
import itertools

MOD = 10**9 + 7

def numRollsToTarget_bruteforce(n: int, k: int, target: int) -> int:
    """
    暴力枚举所有可能的投掷结果
    """
    count = 0                     # 统计符合条件的方案数
    # itertools.product 会生成 k^n 种元组，每个元组对应一次完整的投掷
    for rolls in itertools.product(range(1, k + 1), repeat=n):
        if sum(rolls) == target:  # 检查当前组合的和是否等于 target
            count += 1
    return count % MOD            # 题目要求对 1e9+7 取模
```

#### 复杂度  

- **时间复杂度**：`O(k^n)`  
  - 意思是：我们要尝试 `k` 种面 **乘** `n` 次，也就是指数级增长，随着 `n` 或 `k` 增大，耗时会非常久。
- **空间复杂度**：`O(n)`  
  - 只需要保存一次投掷的结果（长度为 `n` 的元组），所以占用的内存随 `n` 线性增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**反复枚举相同的子问题**。例如在 `n=3` 时，前两颗骰子的所有可能和已经算过很多次，只是后面再加一个骰子而已。我们可以把“已经算好的子结果”记下来，下次需要时直接取，用 **动态规划（Dynamic Programming，简称 DP）**。

**核心想法**：  
- 用 `dp[i][s]` 表示「投掷 **i** 颗骰子，点数和恰好为 **s**」的方案数。  
- 初始状态：`dp[0][0] = 1`（0 颗骰子，和为 0 的唯一方式是“不投掷”）。其他 `dp[0][s] = 0`（没有骰子不可能得到正数和）。  
- 状态转移：要得到 `i` 颗骰子和为 `s`，我们可以把第 `i` 颗骰子的点数设为 `face`（1~k），那么前 `i-1` 颗骰子必须凑成 `s-face`。于是：

```
dp[i][s] = Σ dp[i-1][s - face]   (face 从 1 到 k，且 s-face ≥ 0)
```

- 最终答案是 `dp[n][target]`（投完所有骰子，和恰好为 target 的方案数）。

**如何把它实现得更省空间？**  
- 注意到计算 `dp[i][*]` 只依赖 `dp[i-1][*]`，所以我们可以只保留两行，一行代表上一层，一行代表当前层，交替更新。这样空间从 `O(n·target)` 降到 `O(target)`。

**类比**：把 `dp` 想成一本“记账本”，每一行记录“用前 i 颗骰子能凑出多少种不同的总分”。我们每次只需要翻看上一行（前 i‑1 颗），算出本行，然后把上一行的纸张收起来，继续往下写。

#### 代码（Python）

```python
MOD = 10**9 + 7

def numRollsToTarget_dp(n: int, k: int, target: int) -> int:
    """
    动态规划解法
    dp[t] 表示「已经投掷了若干颗骰子，当前和为 t」的方案数
    只保留一维数组，遍历每颗骰子时再更新一次
    """
    # dp_prev 保存上一步的状态，初始只有 dp[0] = 1
    dp_prev = [0] * (target + 1)
    dp_prev[0] = 1

    # 遍历每一颗骰子
    for dice in range(1, n + 1):
        dp_cur = [0] * (target + 1)          # 当前层的空表
        # 当前和 s 必须至少是 dice（每颗最小贡献 1），最多是 target
        for s in range(dice, min(target, dice * k) + 1):
            # 枚举本颗骰子的点数 face
            for face in range(1, k + 1):
                if s - face < 0:              # 前面的和不可能为负，直接跳过
                    break
                dp_cur[s] = (dp_cur[s] + dp_prev[s - face]) % MOD
        dp_prev = dp_cur                      # 进入下一轮时，当前层变成上一层
    return dp_prev[target]                    # 最后 n 颗骰子对应的方案数
```

#### 复杂度  

- **时间复杂度**：`O(n * target * k)`  
  - 直白解释：我们要循环 `n` 次（每颗骰子），每次遍历所有可能的和 `target`，在每个和里再尝试 `k` 种点数。因此总的操作次数约等于 `n × target × k`。在最坏情况下（`n=30, k=30, target=1000`），约为 30 × 1000 × 30 = 900 000 次，完全可以在一秒内完成。  
- **空间复杂度**：`O(target)`  
  - 只用了一个长度为 `target+1` 的数组来保存上一步的结果，和 `n` 没有关系，内存占用很小（最多 1001 个整数）。

---

## 心得

- **核心技巧**：**动态规划**——把“大问题”拆成“子问题”，用表格记住每一步的结果，避免重复计算。  
- **适用的题型**（类似思路）：
  1. **背包问题**（如 `0/1 背包`、`完全背包`）——也需要用 `dp[i][weight]` 之类的状态。  
  2. **子序列计数**（如 “不同子序列的个数”）——状态往往是 “前 i 个字符，组成长度 j 的子序列数”。  
  3. **路径计数**（如 “网格路径数”）——`dp[i][j]` 表示到达坐标 (i,j) 的路径数。  
- **一句话总结解题钥匙**：**把每一次掷骰子看成一次“增量”，用 DP 累计所有可能的增量组合**。

---

## 反思

- **第一反应**：看到 “n 个骰子、k 面、目标和”，立刻想到“枚举所有组合”。这虽然直观，但会超时。  
- **最容易踩的坑**：  
  - **边界**：`target` 可能比 `n`（最小和）小，或比 `n*k`（最大和）大，此时答案应为 0，需要提前返回或在循环里自然得到 0。  
  - **取模**：每一次累加都要对 `10^9+7` 取模，防止整数溢出。忘记取模会导致 Python 运行慢甚至答案错误。  
  - **循环范围**：在 DP 中，`s` 的下界可以从 `dice` 开始，上界可以限制为 `min(target, dice*k)`，这样可以省掉很多无效的计算。  
- **下次遇到同类题**：**先思考“状态”到底是什么**（这里是“已投掷多少颗骰子 + 当前和”），再写出状态转移方程，最后考虑如何压缩空间。这样可以快速从暴力想到 DP，避免无效的枚举。