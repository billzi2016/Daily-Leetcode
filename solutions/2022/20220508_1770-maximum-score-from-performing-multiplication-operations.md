# #1770. 执行乘法操作获得的最大分数 / Maximum Score from Performing Multiplication Operations

> 难度：困难 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/maximum-score-from-performing-multiplication-operations/)

---

## 题目（英文原版）

**Description**

You are given two 0-indexed integer arrays nums and multipliers of size n and m respectively, where n >= m.
You begin with a score of 0. You want to perform exactly m operations. On the ith operation (0-indexed) you will:
Return the maximum score after performing m operations.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3], multipliers = [3,2,1]
Output: 14
Explanation: An optimal solution is as follows:
- Choose from the end, [1,2,3], adding 3 * 3 = 9 to the score.
- Choose from the end, [1,2], adding 2 * 2 = 4 to the score.
- Choose from the end, [1], adding 1 * 1 = 1 to the score.
The total score is 9 + 4 + 1 = 14.
```

**Example 2:**

```
Input: nums = [-5,-3,-3,-2,7,1], multipliers = [-10,-5,3,4,6]
Output: 102
Explanation: An optimal solution is as follows:
- Choose from the start, [-5,-3,-3,-2,7,1], adding -5 * -10 = 50 to the score.
- Choose from the start, [-3,-3,-2,7,1], adding -3 * -5 = 15 to the score.
- Choose from the start, [-3,-2,7,1], adding -3 * 3 = -9 to the score.
- Choose from the end, [-2,7,1], adding 1 * 4 = 4 to the score.
- Choose from the end, [-2,7], adding 7 * 6 = 42 to the score. 
The total score is 50 + 15 - 9 + 4 + 42 = 102.
```

**Constraints**

- n == nums.length
- m == multipliers.length
- 1 <= m <= 300
- m <= n <= 105
- -1000 <= nums[i], multipliers[i] <= 1000

---

## 题目（中文翻译）

**题目描述**

给定两个下标从 **0** 开始的整数数组 `nums` 和 `multipliers`，长度分别为 `n` 和 `m`，且满足 `n >= m`。初始分数为 **0**，你需要恰好执行 `m` 次操作。第 `i` 次操作（`0`‑索引）时，你可以：

- 选择 `nums` 的最左侧元素或最右侧元素，记为 `x`；
- 将 `x` 与 `multipliers[i]` 相乘，得到的乘积加到当前分数上；
- 将选中的元素从 `nums` 中移除。

在完成全部 `m` 次操作后，返回可能得到的 **最大分数**。

**示例**

> 示例 1  
> 输入: `nums = [1,2,3]`, `multipliers = [3,2,1]`  
> 输出: `14`  
> 解释: 最优的操作序列如下:  
> - 第一次从末尾取 `3`，得分 `3 * 3 = 9` → 总分 `9`  
> - 第二次从末尾取 `2`，得分 `2 * 2 = 4` → 总分 `13`  
> - 第三次从末尾取 `1`，得分 `1 * 1 = 1` → 总分 `14`  

> 示例 2  
> 输入: `nums = [-5,-3,-3,-2,7,1]`, `multipliers = [-10,-5,3,4,6]`  
> 输出: `102`  
> 解释: 最优的操作序列如下:  
> - 第一次从开头取 `-5`，得分 `-5 * -10 = 50` → 总分 `50`  
> - 第二次从开头取 `-3`，得分 `-3 * -5 = 15` → 总分 `65`  
> - 第三次从开头取 `-3`，得分 `-3 * 3 = -9` → 总分 `56`  
> - 第四次从末尾取 `1`，得分 `1 * 4 = 4` → 总分 `60`  
> - 第五次从末尾取 `7`，得分 `7 * 6 = 42` → 总分 `102`  

**约束条件**

- `n == nums.length`
- `m == multipliers.length`
- `1 <= m <= 300`
- `m <= n <= 10^5`
- `-1000 <= nums[i], multipliers[i] <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题的本质是 **每一步可以从数组两端挑一个数**，乘上当前的 multiplier 加到得分里。  
最直接的想法就是把所有可能的挑选顺序全部列举出来，算出每种情况的总得分，最后取最大值。

- **数据结构**：只需要用原始的 `nums` 列表和 `multipliers` 列表。  
  - 这里不需要额外的数据结构，递归调用时用 **函数的参数** 记录已经从左边取了多少、从右边取了多少。  
  - 可以把「从左边取」想象成「从书架左端抽一本书」，「从右边取」就是「从右端抽一本书」——每次只能抽最外面的那本。

- **为什么正确**：因为我们把 **所有** 合法的挑选序列（左/右的组合）都遍历了一遍，必然会找到最优的那一个。

- **复杂度分析**：  
  - 每一步都有 2 种选择（左或右），共要进行 `m` 步，所以总的组合数是 `2^m`。  
  - 递归调用的层数最多为 `m`，所以空间（递归栈）是 `O(m)`。  
  - 用大白话说，`2^m` 就像把 1 翻 `m` 次硬币，结果会指数级增长。比如 `m=20` 时已经有 **约 1,000,000** 种可能，`m=30` 时就超过 **10 亿**，显然不可接受。

#### 代码（Python）

```python
from typing import List

def maximumScore_bruteforce(nums: List[int], multipliers: List[int]) -> int:
    n, m = len(nums), len(multipliers)

    # 递归函数：i 表示已经完成了 i 次乘法操作
    # left 表示已经从左边取走了多少个元素
    def dfs(i: int, left: int) -> int:
        # 已经完成全部 m 步，得分为 0（递归的基准）
        if i == m:
            return 0

        # 右边已经被取走的元素数目可以通过公式算出来
        right = n - 1 - (i - left)   # 已取的总数 i，左边取了 left，剩下的就是右边取的

        # 选左边
        take_left = nums[left] * multipliers[i] + dfs(i + 1, left + 1)

        # 选右边
        take_right = nums[right] * multipliers[i] + dfs(i + 1, left)

        # 返回两种选择的最大值
        return max(take_left, take_right)

    return dfs(0, 0)
```

> **注意**：这段代码只能在 `m` 很小（比如 `m ≤ 15`）时跑得动，主要用来说明最原始的思路。

#### 复杂度

- **时间复杂度**：`O(2^m)`  
  - 每一步分成左/右两条路，深度是 `m`，所以总的递归节点数是 `2^m`。  
  - 用生活中的比喻：如果每一步都要挑“左”或“右”，相当于一次一次掷硬币，硬币掷 `m` 次会出现 `2^m` 种不同的正反面序列。

- **空间复杂度**：`O(m)`  
  - 递归栈的深度最多 `m`，每层只保存常数个变量。  

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈在于大量的重复计算**。  
例如，在不同的递归路径上，可能会出现相同的「已经取了多少左边」的状态，这时后面的子问题完全相同，却被重复求解了。

**关键优化**：把「已经完成了 i 步且左边取了 left 个」这个状态记下来，下次再遇到相同的 `(i, left)` 时直接复用答案——这就是**记忆化搜索**（自顶向下 DP）或**动态规划**（自底向上）。

- **状态定义**  
  - `dp[i][left]`：在已经完成前 `i` 步（`0 ≤ i ≤ m`），并且从左边取了 `left` 个元素时，能够得到的最大得分。  
  - 从左边取了 `left`，说明从右边已经取了 `i - left` 个。右端当前可取的元素下标是 `right = n - 1 - (i - left)`。

- **状态转移**  
  - 这一步使用第 `i` 个 multiplier（下标从 0 开始）。有两种选择：
    1. **取左**：得分 `nums[left] * multipliers[i]` 加上后续的最优子得分 `dp[i+1][left+1]`。  
    2. **取右**：得分 `nums[right] * multipliers[i]` 加上后续的最优子得分 `dp[i+1][left]`（左边取的数量不变）。  
  - 取最大值：
    ```
    dp[i][left] = max(
        nums[left] * multipliers[i] + dp[i+1][left+1],
        nums[right] * multipliers[i] + dp[i+1][left]
    )
    ```

- **起始条件**  
  - 当 `i == m`（已经用了所有 multiplier）时，得分为 0。相当于 `dp[m][*] = 0`。

- **实现方式**  
  - **自顶向下**：用 `functools.lru_cache` 把递归的 `(i, left)` 结果缓存。代码简洁，易于理解。  
  - **自底向上**：从 `i = m-1` 往 `0` 填表。因为 `dp[i]` 只依赖 `dp[i+1]`，可以把二维表压缩成一维，空间降到 `O(m)`。

- **为什么快**  
  - 状态总数是 `m * (m+1) / 2 = O(m^2)`（因为 `left` 只能在 `0..i` 之间），每个状态只计算一次，时间从指数级降到多项式级。

#### 代码（Python）

下面给出 **自顶向下 + 记忆化** 的实现，配有中文注释，直接可以运行：

```python
from functools import lru_cache
from typing import List

def maximumScore(nums: List[int], multipliers: List[int]) -> int:
    n, m = len(nums), len(multipliers)

    @lru_cache(maxsize=None)               # 自动记住每个 (i, left) 的返回值
    def dfs(i: int, left: int) -> int:
        """
        i    : 已经使用了前 i 个 multiplier（0 <= i <= m）
        left : 已经从左边取走了 left 个元素
        返回：从当前状态开始，能够得到的最大剩余得分
        """
        if i == m:                          # 用完了所有 multiplier
            return 0

        # 右边当前可取的元素下标
        right = n - 1 - (i - left)          # 已取 i 次，左边取 left 次，剩下的都是右边取的

        # 选左边
        take_left = nums[left] * multipliers[i] + dfs(i + 1, left + 1)

        # 选右边
        take_right = nums[right] * multipliers[i] + dfs(i + 1, left)

        # 返回两种选择的最大值
        return max(take_left, take_right)

    return dfs(0, 0)                         # 从第 0 步、左边还没取开始
```

**自底向上（空间压缩）实现**（供参考）：

```python
def maximumScore_bottomup(nums: List[int], multipliers: List[int]) -> int:
    n, m = len(nums), len(multipliers)
    # dp[left] 表示在已经完成 i 步且左边取了 left 个时的最大得分
    dp = [0] * (m + 1)        # 初始化为第 m 步的状态，全为 0

    # 从倒数第一步往前算
    for i in range(m - 1, -1, -1):
        # left 的取值范围是 0 .. i（因为最多只能取 i 次左边）
        new_dp = dp[:]       # 复制上一层的 dp，防止覆盖
        for left in range(i + 1):
            right = n - 1 - (i - left)
            take_left = nums[left] * multipliers[i] + dp[left + 1]
            take_right = nums[right] * multipliers[i] + dp[left]
            new_dp[left] = max(take_left, take_right)
        dp = new_dp
    return dp[0]
```

#### 复杂度

- **时间复杂度**：`O(m²)`  
  - 状态数是 `i`（0~m）×`left`（0~i），大约是 `m·(m+1)/2`，每个状态只做常数次计算。  
  - 与暴力解的 `2^m` 相比，`m²` 增长非常慢，即使 `m = 300` 也只有约 **90,000** 次操作，完全可以接受。

- **空间复杂度**：`O(m²)`（记忆化版）或 `O(m)`（滚动数组版）  
  - 记忆化递归需要把所有状态保存下来，最坏情况是 `≈ m²`。  
  - 使用自底向上压缩到一维时，只保留两层 DP，空间降到 `O(m)`，约 300 个整数，几乎可以忽略不计。

---

## 心得

- **核心技巧**：**记忆化搜索 / 动态规划**，把“已经取了多少左边”作为状态，避免重复子问题。  
- **适用的题型**  
  1. “从数组两端取数”类问题（如 LeetCode 1463. 摘樱桃、LeetCode 1055. 形成最大的数）  
  2. 需要在固定步数内做选择、且选择只影响两端的情况（如 “石子游戏” 系列）  
- **一句话总结解题钥匙**：**把“左取次数”抽象成 DP 的维度，利用子问题重叠进行记忆化**。

---

## 反思

- **第一反应**：看到“可以从左或右取”就想直接模拟所有可能的组合，结果指数爆炸。  
- **最容易踩的坑**  
  - **下标计算错误**：右端下标 `right = n - 1 - (i - left)` 必须同时考虑已经取了多少左边和右边。  
  - **递归深度**：`m` 最多 300，递归层数不会太深，但如果改成循环实现，需要注意数组越界。  
  - **负数乘积**：乘数和数组里都有负数，不能把“取最大数”当成贪心。  
- **下次遇到同类题**：第一步先**确定状态**（例如已用步数、左端取的个数），再**判断是否有子问题重叠**，如果有就立刻考虑 DP/记忆化。这样可以把暴力的指数时间立刻降到多项式。