# #3409. 相邻差递减的最长子序列 / Longest Subsequence With Decreasing Adjacent Difference

> 难度：中等 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/longest-subsequence-with-decreasing-adjacent-difference/)

---

## 题目（英文原版）

**Description**

You are given an array of integers nums.
Your task is to find the length of the longest subsequence seq of nums, such that the absolute differences between consecutive elements form a non-increasing sequence of integers. In other words, for a subsequence seq0, seq1, seq2, ..., seqm of nums, |seq1 - seq0| >= |seq2 - seq1| >= ... >= |seqm - seqm - 1|.
Return the length of such a subsequence.

**Examples**

**Example 1:**

```
Input: nums = [16,6,3]
Output: 3
Explanation:
The longest subsequence is [16, 6, 3] with the absolute adjacent differences [10, 3] .
```

**Example 2:**

```
Input: nums = [6,5,3,4,2,1]
Output: 4
Explanation:
The longest subsequence is [6, 4, 2, 1] with the absolute adjacent differences [2, 2, 1] .
```

**Example 3:**

```
Input: nums = [10,20,10,19,10,20]
Output: 5
Explanation:
The longest subsequence is [10, 20, 10, 19, 10] with the absolute adjacent differences [10, 10, 9, 9] .
```

**Constraints**

- 2 <= nums.length <= 104
- 1 <= nums[i] <= 300

---

## 题目（中文翻译）

给定一个整数数组 `nums`。  
你的任务是找到 `nums` 中最长的子序列（subsequence）`seq`，使得相邻元素的绝对差（absolute differences）构成一个非递增的整数序列。换句话说，对于子序列 `seq0, seq1, seq2, ..., seqm`，满足  

\[
|seq_1 - seq_0| \ge |seq_2 - seq_1| \ge \dots \ge |seq_m - seq_{m-1}|
\]

返回满足条件的子序列的长度。

---

### 示例

**示例 1**

```
Input: nums = [16,6,3]
Output: 3
```
**解释**：最长的子序列是 `[16, 6, 3]`，其相邻绝对差为 `[10, 3]`。

**示例 2**

```
Input: nums = [6,5,3,4,2,1]
Output: 4
```
**解释**：最长的子序列是 `[6, 4, 2, 1]`，其相邻绝对差为 `[2, 2, 1]`。

**示例 3**

```
Input: nums = [10,20,10,19,10,20]
Output: 5
```
**解释**：最长的子序列是 `[10, 20, 10, 19, 10]`，其相邻绝对差为 `[10, 10, 9, 9]`。

---

### 约束条件

- `2 <= nums.length <= 10^4`
- `1 <= nums[i] <= 300`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的子序列**，检查每个子序列的相邻差的绝对值是否满足  
`|a₁-a₀| ≥ |a₂-a₁| ≥ …`，然后取最长的那一个。

- **数据结构**：我们可以把数组的下标当成“节点”，把两两之间的差值当成“边”。遍历所有子序列相当于在这张完全图里搜索所有路径。  
  - 哈希表（字典）在这里可以看成“记事本”，把每条已经检查过的子序列长度记下来，防止重复计算。  
- **正确性**：因为我们遍历了**所有**合法子序列，必然能找到最长的那条。  
- **复杂度**：  
  - 子序列的个数是指数级的，最坏情况下是 `2ⁿ`（每个元素要么选要么不选），所以时间复杂度是 **指数级**，记作 `O(2ⁿ)`。  
  - 只需要保存当前递归栈和临时变量，空间是 `O(n)`。

> **大白话**：`O(2ⁿ)` 就像把所有可能的排队方式都列出来，人数多了根本算不过来。

#### 代码（Python）

```python
def longest_subseq_bruteforce(nums):
    n = len(nums)
    best = 1                     # 至少可以选一个元素

    # 递归枚举子序列
    def dfs(idx, last_val, last_diff, length):
        nonlocal best
        # 更新答案
        best = max(best, length)

        # 继续往后挑选
        for i in range(idx, n):
            cur_diff = abs(nums[i] - last_val) if length > 0 else 0
            # 如果已经有前驱，则检查非递增约束
            if length == 0 or cur_diff <= last_diff:
                dfs(i + 1, nums[i], cur_diff, length + 1)

    dfs(0, 0, float('inf'), 0)
    return best
```

> **提示**：这段代码只能用于极小规模的输入，主要是帮助大家理解“枚举”思路。

#### 复杂度

- 时间复杂度：`O(2ⁿ)` —— 随着元素个数呈指数增长，几乎不可能在 `n=10⁴` 时跑完。  
- 空间复杂度：`O(n)` —— 递归栈的深度最多 `n`。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**枚举所有子序列**。我们要把问题转化为“局部最优可以合并成全局最优”。  
观察条件：

```
|seq₁ - seq₀| ≥ |seq₂ - seq₁| ≥ … ≥ |seqₘ - seqₘ₋₁|
```

只要知道**当前结尾元素的值**以及**上一次的差值**，后面还能接什么元素就确定了。于是可以使用**动态规划**（DP）：

- 状态 `dp[v][d]`：以值 `v` 结尾，且最近一次相邻差的绝对值恰好是 `d` 的最长子序列长度。  
  - `v` 的取值范围是题目给出的 `1 … 300`（因为 `nums[i] ≤ 300`）。  
  - `d` 的取值范围是 `0 … 300`（最大差值不超过 `300-1`）。  
- 转移：遍历数组中的每个元素 `x`，尝试把它接在已经得到的任意状态后面。  
  - 若前一个元素的值是 `v`，则新差 `diff = |x - v|`。  
  - 为了满足“非递增”，前一个状态的差 `prev_d` 必须 **大于等于** `diff`。  
  - 因此我们需要 **在同一个 `v` 上，查询所有 `prev_d ≥ diff` 的最大 `dp[v][prev_d]`**。  

为了让查询 `max_{prev_d ≥ diff}` 快速完成，我们为每个 `v` 维护一个 **前缀最大数组**（其实是后缀最大，因为差值越大越靠左）：

```
pref[v][d] = max{ dp[v][d'], d' ≥ d }
```

这样查询只需 `O(1)`。

**整体流程**（伪代码）：

```
初始化 dp[1..300][0..300] = 0
初始化 pref 同样全 0
ans = 1

遍历 nums 中的每个数 x:
    cur_best = 1                     # 只选自己
    for v = 1 .. 300:
        diff = abs(x - v)
        # 取前缀最大得到可以接在 v 之后的最长长度
        cand = pref[v][diff] + 1
        cur_best = max(cur_best, cand)

        # 更新以 x 结尾、差为 diff 的状态
        dp[x][diff] = max(dp[x][diff], cand)

    # 重新计算 pref[x]（仅对 x 受影响的那一行重新扫一遍）
    max_sofar = 0
    for d from 300 down to 0:
        max_sofar = max(max_sofar, dp[x][d])
        pref[x][d] = max_sofar

    ans = max(ans, cur_best)

返回 ans
```

**为什么正确？**  
- **子问题完整**：`dp[v][d]` 已经记录了所有以 `v` 结尾、上一次差为 `d` 的最长子序列。  
- **状态转移合法**：若我们把新元素 `x` 接在某个已有子序列后面，唯一的限制是新的差 `diff` 必须不大于之前的差 `prev_d`。`pref[v][diff]` 正好给出了满足此限制的最长长度。  
- **最优子结构**：任何合法的最长子序列的倒数第二个元素一定是某个 `v`，且它的上一次差一定是某个 `prev_d ≥ diff`。因此我们的转移一定能得到这条子序列的长度。  
- **全局最优**：遍历所有 `x` 时，我们始终维护答案 `ans` 为所有状态的最大值，必然是整个数组的最长合法子序列。

**复杂度分析**  
- 外层遍历 `n`（≤ 10⁴）次。  
- 每次遍历 **所有可能的前驱值** `v`（1 ~ 300），常数时间完成查询和更新。  
- 重新计算 `pref[x]` 需要遍历差值范围 `0 ~ 300`。  
- 总时间 = `O(n * (V + D))`，其中 `V = D = 300`，约 `6·10⁶` 次操作，完全可以在 Python 里跑完。  
- 空间：`dp`、`pref` 各是 `301 × 301` 的二维数组，约 `9·10⁴` 整数，`O(V·D)` ≈ `O(10⁵)`，非常小。

> **类比**：把每个可能的数值想成“城市”，差值想成“道路宽度”。我们想在城市之间走，要求走的道路宽度逐渐变窄。`dp` 记录“到达某城市、刚走完宽度为 d 的路的最长路径”，`pref` 就是“从这里出发，宽度不小于 d 的所有道路中最好的那条”。这样每次只看一次表，就能决定是否继续前进。

#### 代码（Python）

```python
def longestSubsequence(nums):
    """
    返回满足相邻差绝对值非递增的最长子序列长度。
    思路：动态规划 + 前缀最大（后缀最大）表
    """
    MAX_VAL = 300          # 题目限制 nums[i] ≤ 300
    MAX_DIFF = 300         # 最大可能的差值

    # dp[v][d] : 以值 v 结尾，最近一次差恰好是 d 的最长子序列长度
    dp = [[0] * (MAX_DIFF + 1) for _ in range(MAX_VAL + 1)]
    # pref[v][d] : max{ dp[v][d'] }，其中 d' ≥ d
    pref = [[0] * (MAX_DIFF + 1) for _ in range(MAX_VAL + 1)]

    ans = 1                # 至少可以选一个元素

    for x in nums:
        cur_best = 1       # 只选自己时的长度

        # 枚举所有可能的前驱值 v
        for v in range(1, MAX_VAL + 1):
            diff = abs(x - v)                # 新增的相邻差
            # 在 v 上，查询差 >= diff 的最长长度（pref 已经是后缀最大）
            cand = pref[v][diff] + 1         # 加上当前元素 x
            if cand > cur_best:
                cur_best = cand

            # 更新以 x 结尾、差为 diff 的状态
            if cand > dp[x][diff]:
                dp[x][diff] = cand

        # 重新计算 pref[x]（仅这一行受影响）
        max_sofar = 0
        for d in range(MAX_DIFF, -1, -1):    # 从大到小遍历，构造后缀最大
            if dp[x][d] > max_sofar:
                max_sofar = dp[x][d]
            pref[x][d] = max_sofar

        # 更新全局答案
        if cur_best > ans:
            ans = cur_best

    return ans
```

**代码要点注释**  

| 行号 | 关键代码 | 中文解释 |
|------|----------|----------|
| 4‑5  | `MAX_VAL = 300`、`MAX_DIFF = 300` | 题目给的上限，用来固定 DP 表大小 |
| 9‑10 | `dp = [[0] * (MAX_DIFF + 1) for _ in range(MAX_VAL + 1)]` | 建立二维数组，所有状态初始为 0 |
| 11‑12| `pref = [[0] * (MAX_DIFF + 1) for _ in range(MAX_VAL + 1)]` | 前缀最大表，和 `dp` 同维度 |
| 16‑27| `for x in nums:` 循环遍历每个元素 | 对每个新加入的数 `x`，尝试把它接到已有子序列后面 |
| 20‑23| `diff = abs(x - v)`、`cand = pref[v][diff] + 1` | 计算新差值，利用 `pref` 快速得到能够接上去的最长长度 |
| 25‑26| `if cand > dp[x][diff]: dp[x][diff] = cand` | 更新状态表，使得以 `x` 结尾、差为 `diff` 的记录保持最长 |
| 29‑33| 重新计算 `pref[x]`（后缀最大） | 只需要在 `x` 这行重新扫一遍，时间 O(MAX_DIFF) |
| 36   | `ans = max(ans, cur_best)` | 维护全局最大答案 |

#### 复杂度

- **时间复杂度**：`O(n * (V + D)) = O(n * 600)`，其中 `n ≤ 10⁴`，约 `6·10⁶` 次基本操作，远低于暴力的指数级。  
  - 与暴力解相比，时间从 **指数** 降到了 **线性**（对 `n` 成比例），几乎可以瞬间算完最大输入。
- **空间复杂度**：`O(V * D) = O(300 * 300) ≈ 9·10⁴`，即几万个整数，远小于 `n`，是常数级别的额外空间。

---

## 心得

- **核心技巧**：把“相邻差的非递增”转化为“状态 = (当前值, 上一次差)”，并使用 **动态规划 + 后缀最大** 进行快速转移。  
- **适用场景**：  
  1. **限制在差值/距离上递增或递减** 的序列问题（如“相邻差的递增子序列”）。  
  2. **值域小且差值范围有限** 时，需要在“值 × 差”二维空间上做 DP。  
  3. 需要在**某个维度上取最大且满足单调约束**的场景（如 “最长递增子序列的长度按值分段统计”）。
- **一句话总结解题钥匙**：**把单调约束抽象成“上一次差值”，用二维 DP 保存 (值, 差) 并用后缀最大实现 O(1) 单调查询**。

---

## 反思

- **第一反应**：看到“相邻差的非递增”，本能想到“枚举所有子序列”或“把差值序列直接做 LIS”。这两条路都太慢。  
- **最容易踩的坑**：  
  - 忽略了 **差值为 0** 的情况（相等的数也合法）。  
  - 没有维护 **后缀最大**，导致每次查询 `prev_d ≥ diff` 需要遍历所有差值，时间会回到 `O(n·V·D)`。  
  - 边界条件：`dp` 初始化为 0，`pref` 也要同步更新，否则第一次使用时会得到错误的 `+1`。  
- **下次类似题目第一步**：先问自己“要不要记录上一条信息（这里是上一次的差值）”，若需要，则把它加入 DP 的维度；随后思考“单调约束如何快速查询”，常用技巧是 **前缀/后缀最大** 或 **单调队列**。