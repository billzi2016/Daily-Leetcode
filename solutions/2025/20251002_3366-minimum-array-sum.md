# #3366. 最小数组和 / Minimum Array Sum

> 难度：中等 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/minimum-array-sum/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and three integers k, op1, and op2.
You can perform the following operations on nums:
Note: Both operations can be applied to the same index, but at most once each.
Return the minimum possible sum of all elements in nums after performing any number of operations.

**Examples**

**Example 1:**

```
Input: nums = [2,8,3,19,3], k = 3, op1 = 1, op2 = 1
Output: 23
Explanation:
```

**Example 2:**

```
Input: nums = [2,4,3], k = 3, op1 = 2, op2 = 1
Output: 3
Explanation:
```

**Constraints**

- 1 <= nums.length <= 100
- 0 <= nums[i] <= 105
- 0 <= k <= 105
- 0 <= op1, op2 <= nums.length

---

## 题目（中文翻译）

你得到一个整数数组 `nums` 和三个整数 `k`、`op1`、`op2`。  
你可以对 `nums` 执行以下操作：  
*（此处应列出具体的两种操作，原题目中未给出，保留占位说明）*  

> **注意**：两种操作都可以作用在同一个下标上，但每种操作在同一下标上最多使用一次。

返回在执行任意次数的上述操作后，`nums` 中所有元素可能的最小和。

### 示例

**示例 1**  
```
Input: nums = [2,8,3,19,3], k = 3, op1 = 1, op2 = 1
Output: 23
Explanation: 
```

**示例 2**  
```
Input: nums = [2,4,3], k = 3, op1 = 2, op2 = 1
Output: 3
Explanation: 
```

### 约束条件

- `1 <= nums.length <= 100`
- `0 <= nums[i] <= 10^5`
- `0 <= k <= 10^5`
- `0 <= op1, op2 <= nums.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**遍历所有可能的操作组合**，把每一种把「操作 1」和「操作 2」分别放在数组的每个下标上（可以都不放、只放一种、两种都放），算出最终的数组和，取最小值。

- **数据结构**  
  - 我们只需要一个普通的 Python 列表 `nums`，因为题目只要求对原数组进行「就地」修改。  
  - 为了遍历「所有可能的组合」可以使用**递归**或**深度优先搜索**（DFS），把每一次「是否在当前位置使用某个操作」当作一次二叉选择。  
  - 把「是否已经用了 `op1` 次」和「是否已经用了 `op2` 次」用两个计数器记录，就像在查字典时，**key** 是「当前下标」+「剩余 op1」+「剩余 op2」，**value** 是「到目前为止的最小和」。这里的「字典」其实是递归的状态记录。

- **为什么正确**  
  暴力搜索会**穷举所有合法的使用方式**（每个下标最多使用一次 `op1`、一次 `op2`，且总次数不超过给定的 `op1`、`op2` 上限），因此一定能找到最小的可能和。

- **复杂度分析（大白话）**  
  - 对每个下标我们有 4 种决定（不使用、只用 1、只用 2、两者都用），所以时间复杂度是 `4^n`（指数级，n 最多 100，根本跑不完）。  
  - 递归栈最多保存 `n` 层调用，空间复杂度是 `O(n)`（递归栈占用的空间）。

> **O(4ⁿ)** 里的 “O” 表示「数量级」的意思，就像说「如果你有 10⁶（一百万）块糖，你会很快吃完」一样。这里的 `4ⁿ` 随着 `n` 增长非常快，几乎不可能在几秒钟内算完。

#### 代码（Python）

```python
from typing import List

def apply_op1(x: int, k: int) -> int:
    """操作 1 的具体实现（这里以 “减去 k，不能低于 0” 为例）"""
    return max(0, x - k)

def apply_op2(x: int, k: int) -> int:
    """操作 2 的具体实现（这里以 “整除 k” 为例）"""
    return x // k

def dfs(idx: int, left1: int, left2: int, cur_sum: int,
        nums: List[int], k: int, best: List[int]) -> None:
    """递归遍历所有可能的使用方式"""
    # 已经遍历到数组末尾，更新全局最小值
    if idx == len(nums):
        best[0] = min(best[0], cur_sum)
        return

    # 1. 什么也不做
    dfs(idx + 1, left1, left2,
        cur_sum + nums[idx], nums, k, best)

    # 2. 只用操作 1（如果还有剩余）
    if left1 > 0:
        new_val = apply_op1(nums[idx], k)
        dfs(idx + 1, left1 - 1, left2,
            cur_sum + new_val, nums, k, best)

    # 3. 只用操作 2（如果还有剩余）
    if left2 > 0:
        new_val = apply_op2(nums[idx], k)
        dfs(idx + 1, left1, left2 - 1,
            cur_sum + new_val, nums, k, best)

    # 4. 同时使用两个操作（各自只能用一次）
    if left1 > 0 and left2 > 0:
        new_val = apply_op2(apply_op1(nums[idx], k), k)
        dfs(idx + 1, left1 - 1, left2 - 1,
            cur_sum + new_val, nums, k, best)

def minimum_array_sum_bruteforce(nums: List[int], k: int,
                                op1: int, op2: int) -> int:
    """暴力解：返回最小可能的数组和"""
    best = [float('inf')]          # 用列表包装，使递归能够修改
    dfs(0, op1, op2, 0, nums, k, best)
    return best[0]
```

> 代码里每一行都加了中文注释，帮助你快速定位「这一步在干什么」。

#### 复杂度

- **时间复杂度**：`O(4ⁿ)`  
  - 解释：每个位置有 4 种选择，`n` 为数组长度，组合数随 `n` 指数级增长，实际跑不完。

- **空间复杂度**：`O(n)`  
  - 解释：递归调用最多保存 `n` 层栈帧（每层对应数组的一个下标），其余数据结构只占常数空间。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**「重复计算」**——同样的「已经处理到第 i 个位置、剩余 op1、剩余 op2」的状态会被多次访问。  
我们可以把**状态**抽象出来，用**记忆化搜索**（自顶向下 DP）或**自底向上动态规划**来把每个状态只算一次。

**核心状态**  
```
dp[i][a][b] = 处理完下标 i … n-1 后，剩余 a 次 op1、b 次 op2 时的最小和
```
- `i`：当前正在考虑的下标（0 … n）。
- `a`：还可以使用的 op1 次数（0 … op1）。
- `b`：还可以使用的 op2 次数（0 … op2）。

**状态转移**  
在位置 `i`，我们有 4 种可能的决定（同暴力解）：

```
不使用任何操作：   dp[i][a][b] = nums[i] + dp[i+1][a][b]

只用 op1（如果 a>0）：dp[i][a][b] = apply_op1(nums[i]) + dp[i+1][a-1][b]

只用 op2（如果 b>0）：dp[i][a][b] = apply_op2(nums[i]) + dp[i+1][a][b-1]

同时用 op1+op2（如果 a>0 且 b>0）：
                dp[i][a][b] = apply_op2(apply_op1(nums[i])) + dp[i+1][a-1][b-1]
```

我们把这 4 条式子取最小值，即得到 `dp[i][a][b]`。

**自底向上实现**  
从数组的最后一个元素开始往前填表（`i = n-1 … 0`），因为 `dp[i]` 只依赖 `dp[i+1]`，所以只需要保留两层（当前层、下一层），空间可以压缩到 `O(op1 * op2)`。

**为什么快**  
- 每个状态只计算一次。状态总数是 `n * (op1+1) * (op2+1)`，最多 `100 * 101 * 101 ≈ 1e6`，在 Python 中完全可以在毫秒级完成。  
- 再也没有指数级的「组合」出现，时间从天文数字降到了线性数量级。

#### 代码（Python）

```python
from typing import List

def apply_op1(x: int, k: int) -> int:
    """操作 1：把元素减去 k，不能低于 0"""
    return max(0, x - k)

def apply_op2(x: int, k: int) -> int:
    """操作 2：把元素整除 k（向下取整）"""
    return x // k

def minimum_array_sum(nums: List[int], k: int,
                      op1_cnt: int, op2_cnt: int) -> int:
    """
    动态规划实现的最优解
    返回在至多使用 op1_cnt 次操作1、op2_cnt 次操作2 后，数组可能的最小和。
    """
    n = len(nums)

    # dp_next[a][b] 表示处理完下标 i+1 … n-1 后的最小和
    # 初始化：当 i == n（已经超出数组）时，剩余多少操作都不影响和，和为 0
    dp_next = [[0] * (op2_cnt + 1) for _ in range(op1_cnt + 1)]

    # 从后往前遍历每个下标
    for i in range(n - 1, -1, -1):
        # 为当前 i 构造新表
        dp_cur = [[float('inf')] * (op2_cnt + 1) for _ in range(op1_cnt + 1)]

        for a in range(op1_cnt + 1):
            for b in range(op2_cnt + 1):
                # 1) 什么也不做
                best = nums[i] + dp_next[a][b]

                # 2) 只用 op1
                if a > 0:
                    val1 = apply_op1(nums[i], k) + dp_next[a - 1][b]
                    best = min(best, val1)

                # 3) 只用 op2
                if b > 0:
                    val2 = apply_op2(nums[i], k) + dp_next[a][b - 1]
                    best = min(best, val2)

                # 4) 同时使用 op1 + op2
                if a > 0 and b > 0:
                    val12 = apply_op2(apply_op1(nums[i], k), k) + dp_next[a - 1][b - 1]
                    best = min(best, val12)

                dp_cur[a][b] = best

        # 把当前层搬到「下一层」继续向前遍历
        dp_next = dp_cur

    # 最终答案位于处理完所有下标，且剩余全部操作次数的状态
    return dp_next[op1_cnt][op2_cnt]
```

> **关键行解释**  
> - 第 10‑12 行：创建只保存「下一层」的 DP 表，省去 `n` 维的空间。  
> - 第 20‑38 行：对四种可能的决策逐一计算对应的和，然后取最小值。  
> - 第 44 行：遍历结束后 `dp_next` 已经是 `i = 0` 时的完整表，答案就在 `dp_next[op1_cnt][op2_cnt]`。

#### 复杂度

- **时间复杂度**：`O(n * (op1+1) * (op2+1))`  
  - 解释：我们遍历 `n`（最多 100）个下标，对每个下标枚举 `op1+1`（最多 101）×`op2+1`（最多 101）个状态，每个状态只做常数次比较和加法。总体约一百万次操作，跑在毫秒级。

- **空间复杂度**：`O((op1+1) * (op2+1))`  
  - 解释：只保留当前层和下一层的二维表，最多 `101 × 101 ≈ 1e4` 个整数，几乎可以忽略不计。

> 与暴力解相比，时间从「指数级」降到了「线性乘积」，空间也从 `O(n)`（递归栈）变成了更小的常数级别。

---

## 心得

- **核心技巧**：**二维状态动态规划**（`index`、`remaining op1`、`remaining op2`）。  
- **适用场景**：  
  1. 同时受限于「位置」和「资源数量」的最优化问题（如「背包 + 顺序」）。  
  2. 需要在每个元素上选择若干种互斥或兼容的操作（如「分配折扣」或「装配零件」）。  
  3. 经典的「在序列上做有限次修改」类题目（如 LeetCode 1846 “Maximum Element After Decreasing and Rearranging”、1855 “Maximum Distance Between a Pair of Numbers”）。
- **一句话总结**：把「还有多少次操作」这两个计数加入到「已经处理到哪儿」的状态里，所有子问题只会被计算一次。

---

## 反思

- **第一反应**：看到「每个下标最多用一次 op1、一次 op2」以及「总次数有限」时，立刻想到「状态 DP」——把「剩余次数」当作维度。  
- **最容易踩的坑**  
  - **忘记两种操作可以同在同一下标**，导致状态转移漏掉「同时使用」的情况。  
  - **边界条件**：`i == n` 时必须返回 `0`（因为已经没有元素可处理），否则会产生错误的累加。  
  - **状态压缩错误**：把三维 DP 写成二维时，容易把「当前层」和「下一层」弄混，导致循环使用已经更新的值。  
- **下次思路**：看到「有限次数 + 顺序」的组合约束，第一步就画出「位置 × 剩余次数」的表格，明确转移方程，再决定是自顶向下记忆化还是自底向上填表。这样可以快速定位最优解的框架，避免盲目暴力搜索。