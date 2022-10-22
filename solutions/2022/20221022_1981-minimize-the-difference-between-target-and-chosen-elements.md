# #1981. 最小化目标值与所选元素之差 / Minimize the Difference Between Target and Chosen Elements

> 难度：中等 · 标签：Array、Dynamic Programming、Matrix · [LeetCode 链接](https://leetcode.com/problems/minimize-the-difference-between-target-and-chosen-elements/)

---

## 题目（英文原版）

**Description**

You are given an m x n integer matrix mat and an integer target.
Choose one integer from each row in the matrix such that the absolute difference between target and the sum of the chosen elements is minimized.
Return the minimum absolute difference.
The absolute difference between two numbers a and b is the absolute value of a - b.

**Examples**

**Example 1:**

```
Input: mat = [[1,2,3],[4,5,6],[7,8,9]], target = 13
Output: 0
Explanation: One possible choice is to:
- Choose 1 from the first row.
- Choose 5 from the second row.
- Choose 7 from the third row.
The sum of the chosen elements is 13, which equals the target, so the absolute difference is 0.
```

**Example 2:**

```
Input: mat = [[1],[2],[3]], target = 100
Output: 94
Explanation: The best possible choice is to:
- Choose 1 from the first row.
- Choose 2 from the second row.
- Choose 3 from the third row.
The sum of the chosen elements is 6, and the absolute difference is 94.
```

**Example 3:**

```
Input: mat = [[1,2,9,8,7]], target = 6
Output: 1
Explanation: The best choice is to choose 7 from the first row.
The absolute difference is 1.
```

**Constraints**

- m == mat.length
- n == mat[i].length
- 1 <= m, n <= 70
- 1 <= mat[i][j] <= 70
- 1 <= target <= 800

---

## 题目（中文翻译）

**题目描述**  
给定一个 `m x n` 整数矩阵 `mat` 和一个整数 `target`。  
要求从矩阵的每一行中各选取一个整数，使得所选元素之和与 `target` 的绝对差（absolute difference）最小。  
返回能够得到的最小绝对差。  

**定义**  
两个数 `a` 与 `b` 的绝对差是 `|a - b|`（即 `a - b` 的绝对值）。

**示例**  

*示例 1*  
```
输入: mat = [[1,2,3],[4,5,6],[7,8,9]], target = 13
输出: 0
解释: 一种可能的选择是:
- 从第一行选取 1
- 从第二行选取 5
- 从第三行选取 7
所选元素的和为 13，恰好等于 target，故绝对差为 0。
```

*示例 2*  
```
输入: mat = [[1],[2],[3]], target = 100
输出: 94
解释: 最佳的选择是:
- 从第一行选取 1
- 从第二行选取 2
- 从第三行选取 3
所选元素的和为 6，|100 - 6| = 94。
```

*示例 3*  
```
输入: mat = [[1,2,9,8,7]], target = 6
输出: 1
解释: 最佳的选择是从唯一的一行中选取 7，|6 - 7| = 1。
```

**约束条件**  
- `m == mat.length`  
- `n == mat[i].length`  
- `1 <= m, n <= 70`  
- `1 <= mat[i][j] <= 70`  
- `1 <= target <= 800`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每一行都「挑一个」出来，然后把所有挑好的数相加，记为 `sum`，再算 `|target - sum|`，最后把所有可能的组合的差值取最小。  

- **用到的数据结构**：  
  - **递归/回溯**：把每一行看成一层树，树的深度就是行数 `m`，每层有 `n` 条分支（每个元素都是一种选择），遍历整棵树就能得到所有组合。  
  - **列表**：用一个 `path` 列表暂存当前已经选了哪些数，递归结束时把它们求和。  

- **为什么这个方法正确**：  
  - 递归会穷举 **每一种** 从每行挑一个元素的方式，保证不漏掉任何合法解。  
  - 对每一种解我们都计算真实的差值，取最小值自然就是答案。  

- **时间/空间复杂度**（大白话解释）：  
  - **时间**：每一行有 `n` 种选择，`m` 行就有 `nⁿ`（更准确地说是 `n^m`）种组合要尝试。想象有 5 行、每行 3 个数，就要检查 `3^5 = 243` 种情况；如果行数是 70、每行 70 个数，组合数会是天文数字 `70^70`，根本不可能跑完。  
  - **空间**：递归调用会用掉 `m` 层栈帧，最多 `O(m)` 的额外空间，另外保存当前路径也需要 `O(m)`。  

#### 代码（Python）

```python
def min_abs_difference_bruteforce(mat, target):
    m, n = len(mat), len(mat[0])
    best = float('inf')                     # 记录目前找到的最小差值

    def dfs(row, cur_sum):
        """尝试从第 row 行开始选，当前已经选的和是 cur_sum"""
        nonlocal best
        if row == m:                         # 所有行都选完了
            best = min(best, abs(target - cur_sum))
            return
        # 对当前行的每一个元素都尝试一次
        for val in mat[row]:
            # 剪枝：如果已经比当前 best 更差，就可以直接返回
            # （这里的剪枝非常弱，仅作示例）
            if abs(target - (cur_sum + val)) >= best:
                continue
            dfs(row + 1, cur_sum + val)

    dfs(0, 0)
    return best
```

> **关键行中文注释**  
> - `dfs(row, cur_sum)`: 递归函数，`row` 表示正在处理第几行，`cur_sum` 是已经选的数的和。  
> - `if row == m:`：所有行都已经选完，计算当前差值并更新全局最小 `best`。  
> - `for val in mat[row]:`：遍历当前行的每个候选数。  
> - `if abs(target - (cur_sum + val)) >= best:`：一个非常粗糙的剪枝，避免明显比已有答案更差的分支。  

#### 复杂度  

- **时间复杂度**：`O(n^m)` —— 每一行有 `n` 种选择，`m` 行要乘起来，组合数会爆炸。  
  - **含义解释**：如果 `n = 70, m = 70`，这相当于 70 的 70 次方，远远超过计算机能在一秒内完成的操作次数。  
- **空间复杂度**：`O(m)` —— 递归栈深度等于行数，最多保存 70 层调用。  

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **“枚举所有组合”** 是最大的瓶颈。我们需要一种 **“动态规划”**（DP）的方法，把 **“已经可能得到的和”** 用一个集合/布尔数组记录下来，随着遍历每一行逐步更新，而不是一次性枚举全部组合。

**关键观察**  

1. **所有元素都是正数**（`1 ≤ mat[i][j] ≤ 70`），所以累计的和只会增大，永远不会出现负数。  
2. `target ≤ 800`，而每行最多加 `70`，`m ≤ 70`，所以 **所有可能的总和上限** 为 `max_sum = m * 70 ≤ 4900`，这个范围不大，完全可以在内存里保存一个长度约 5k 的数组。  

**DP 的状态定义**  

- `dp[s] = True` 表示 **已经处理完前几行**，可以得到和为 `s` 的一种选择。  
- 初始时只可能得到和 `0`（什么都没选），所以 `dp[0] = True`。  

**状态转移**  

遍历每一行 `row`，把当前行的每个数 `x` 加到已有的所有和 `s` 上，形成新的和 `s + x`。我们用一个临时集合 `next_dp` 来保存本行结束后的所有可能和，然后把它赋值回 `dp`。  

**为什么只需要保留“可能的和”**  

因为我们只关心最终的 **和** 与 `target` 的差值，具体是哪个元素组合并不重要。只要知道某个和是可达的，就已经足够做后续比较。  

**如何得到答案**  

遍历完所有行后，`dp` 中的 `True` 位置就是所有可以得到的和。我们只要在这些和中找一个使 `|target - s|` 最小即可。  

**进一步的剪枝（可选）**  

- 因为所有数都是正的，若某个和已经大于 `target + max_extra`（`max_extra` 可以取 `70`），它离目标已经很远，继续加下去只会更远。实际实现中我们直接把上限设为 `max_sum`，已经足够小，不必额外剪枝。  

**类比**：  
把 `dp` 想象成一张「是否能到达」的地图，最开始只在坐标 0 有标记。每读完一行，就把这行的每个数字当作“步长”，把已有的标记向前移动相应的距离，产生新的标记。最后地图上所有有标记的点就是所有可能的总和。我们只需要在这张地图上找离 `target` 最近的点。  

#### 代码（Python）

```python
def minimize_the_difference(mat, target):
    """
    动态规划解法
    dp[s] == True  表示已经处理完若干行后，能够得到总和 s
    """
    m, n = len(mat), len(mat[0])
    max_sum = m * 70                     # 所有可能的最大总和（约 4900）
    dp = [False] * (max_sum + 1)
    dp[0] = True                         # 什么都不选时和为 0

    for row in mat:                      # 逐行处理
        next_dp = [False] * (max_sum + 1)
        for s in range(max_sum + 1):
            if not dp[s]:
                continue                # 当前和 s 不可达，跳过
            for val in row:             # 把本行的每个数加进去
                new_sum = s + val
                if new_sum <= max_sum:  # 防止越界
                    next_dp[new_sum] = True
        dp = next_dp                     # 用本行的结果覆盖旧的 dp

    # 所有可达的和已经记录在 dp 中，遍历找最接近 target 的那个
    ans = float('inf')
    for s in range(max_sum + 1):
        if dp[s]:
            ans = min(ans, abs(target - s))
    return ans
```

> **关键行中文注释**  
> - `max_sum = m * 70`：根据约束算出所有可能的最大和，数组长度只需要到这里。  
> - `dp[0] = True`：初始化，只选空集合时和为 0。  
> - `for row in mat:`：遍历每一行。  
> - `if not dp[s]: continue`：只对已经可以达到的和 `s` 进行扩展，省掉大量无用循环。  
> - `new_sum = s + val`：把本行的一个数加到已有的和上，得到新和。  
> - `if new_sum <= max_sum:`：防止数组越界。  
> - `ans = min(ans, abs(target - s))`：在所有可达的和中寻找最小的绝对差。  

#### 复杂度  

- **时间复杂度**：`O(m * n * max_sum)`  
  - 具体来说是 `m` 行 × 每行 `n` 个数 × 可能的和的上限 `max_sum (≈ 5 000)`。  
  - **含义解释**：对于本题，最坏情况约为 `70 * 70 * 4900 ≈ 24 000 000` 次基本操作，现代电脑在 1 秒内完全可以跑完。相比暴力的 `n^m`（天文级别），已经快得多。  

- **空间复杂度**：`O(max_sum)`  
  - 只需要两张长度约 5 000 的布尔数组（`dp` 与 `next_dp`），大约几千个布尔值，几 KB 的内存，几乎可以忽略不计。  

---

## 心得  

- **核心技巧**：把“每行挑一个数”转化为“所有可能的和的集合”，用 **动态规划（集合/布尔数组）** 逐行累加。  
- **适用的题型**（类似思路）：  
  1. *“从每个数组中选一个数，使总和最接近 target”*（如 LeetCode 2585 – `Number of Ways to Reach a Target Score`）。  
  2. *“背包容量不大，求能否恰好装满”*（经典 0/1 背包的布尔版）。  
  3. *“多维选择题”*（如从多行多列矩阵中选一个数，使行列和满足某条件）。  
- **一句话总结解题钥匙**：**把“组合”压缩成“可达的和”，用 DP 逐行扩展，最后在可达的和里找最近的那个**。  

---

## 反思  

- **第一反应**：看到“每行选一个数”，自然想到递归枚举所有组合——这在小规模数据下是最直观的。  
- **最容易踩的坑**：  
  - 忽略了 **上限** `max_sum`，直接用 `target` 作为数组大小会导致遗漏大于 `target` 的和，可能错过更接近的解。  
  - 在 DP 过程中忘记 **去重**（直接使用集合或布尔数组），会导致同一个和被重复计入，浪费时间。  
  - 边界条件：`target` 本身可能大于所有可能的和，需要在最终遍历时考虑所有 `dp[s] == True`，而不是只看 `s ≤ target`。  
- **下次类似题的第一步**：先估算**“所有可能结果的取值范围”**（比如最大和、最小和），决定用**布尔 DP / 位图**还是**集合**来记录可达状态，再逐步推进。