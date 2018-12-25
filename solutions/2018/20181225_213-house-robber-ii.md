# #213. **打家劫舍 II** / House Robber II

> 难度：中等 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/house-robber-ii/)

---

## 题目（英文原版）

**Description**

You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed. All houses at this place are arranged in a circle. That means the first house is the neighbor of the last one. Meanwhile, adjacent houses have a security system connected, and it will automatically contact the police if two adjacent houses were broken into on the same night.
Given an integer array nums representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.

**Examples**

**Example 1:**

```
Input: nums = [2,3,2]
Output: 3
Explanation: You cannot rob house 1 (money = 2) and then rob house 3 (money = 2), because they are adjacent houses.
```

**Example 2:**

```
Input: nums = [1,2,3,1]
Output: 4
Explanation: Rob house 1 (money = 1) and then rob house 3 (money = 3).
Total amount you can rob = 1 + 3 = 4.
```

**Example 3:**

```
Input: nums = [1,2,3]
Output: 3
```

**Constraints**

- 1 <= nums.length <= 100
- 0 <= nums[i] <= 1000

---

## 题目（中文翻译）

你是一名专业的抢劫犯，计划在一条街道上抢劫房屋。每栋房屋里都有一定数量的现金。所有房屋呈**环形**排列，也就是说第一栋房屋是最后一栋房屋的邻居。与此同时，**相邻房屋**之间装有联动的报警系统，如果同一夜里两栋相邻的房屋被闯入，系统会自动报警并联系警察。

给定一个整数数组 `nums`，其中 `nums[i]` 表示第 `i` 栋房屋中的现金金额，返回在不触发报警的前提下，你今晚能够抢劫到的最大现金总额。

**示例 1**  
**输入**: `nums = [2,3,2]`  
**输出**: `3`  
**解释**: 你不能先抢劫第 1 栋房屋（金额 = 2）再抢劫第 3 栋房屋（金额 = 2），因为它们是相邻的房屋。

**示例 2**  
**输入**: `nums = [1,2,3,1]`  
**输出**: `4`  
**解释**: 抢劫第 1 栋房屋（金额 = 1）后再抢劫第 3 栋房屋（金额 = 3），总金额为 `1 + 3 = 4`。

**示例 3**  
**输入**: `nums = [1,2,3]`  
**输出**: `3`

**约束条件**

- `1 <= nums.length <= 100`
- `0 <= nums[i] <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**枚举所有合法的偷窃方案**，找出金额最大的那一个。  
- “合法”指的是同一晚不能偷相邻的两栋房子，而且因为房子围成一个环，**第 1 栋和第 n 栋也是相邻的**。  
- 我们可以用**回溯（深度优先搜索）**把每栋房子分成「偷」或「不偷」两种选择。  
- 为了避免相邻偷，我们在决定偷第 i 栋时，需要检查第 i‑1 栋是否已经偷了；另外在递归结束后，还要检查第 1 栋和第 n 栋是否同时被偷。

> 类比：把每栋房子想象成一排灯，灯亮代表偷，灯灭代表不偷。相邻的灯不能同时亮，最左边和最右边的灯也不能一起亮。我们要找一种点灯方式，使亮灯的灯泡数值之和最大。

因为 `nums` 长度最多只有 100，暴力搜索在最坏情况下会遍历 2ⁿ 种可能，仍然可以在电脑上跑通，但显然不够高效。

#### 代码（Python）

```python
from typing import List

def rob_brute(nums: List[int]) -> int:
    n = len(nums)
    if n == 0:
        return 0
    best = 0                         # 记录全局最大金额

    def dfs(i: int, taken_prev: bool, first_taken: bool, cur_sum: int):
        """
        i: 当前考虑的房子下标（0‑based）
        taken_prev: 前一栋房子是否已经偷了
        first_taken: 第 0 栋房子是否已经偷了（用于最后检查环首尾）
        cur_sum: 目前累计的金额
        """
        nonlocal best
        if i == n:                    # 所有房子都遍历完
            # 环首尾不能同时被偷
            if not (first_taken and taken_prev):
                best = max(best, cur_sum)
            return

        # 方案 1：不偷第 i 栋
        dfs(i + 1, False, first_taken, cur_sum)

        # 方案 2：偷第 i 栋（前一栋必须没偷）
        if not taken_prev:
            dfs(i + 1, True,
                first_taken or i == 0,   # 记录是否偷了第 0 栋
                cur_sum + nums[i])

    dfs(0, False, False, 0)
    return best
```

#### 复杂度

- **时间复杂度**：`O(2^n)`  
  解释：每栋房子有「偷」或「不偷」两种选择，最坏会产生 2ⁿ 条递归路径。对于 `n = 100`，这个数量是天文数字，实际运行会非常慢。

- **空间复杂度**：`O(n)`  
  解释：递归调用栈的深度最多是 `n`，每层只保存常数个变量。

---

### 2. 最优解

#### 思路  

暴力解慢的根源在于**重复计算子问题**。如果我们把「偷到第 i 栋，且第 i‑1 栋不偷」这种状态记下来，就可以避免重复探索。  

这正是**动态规划（DP）**的核心思想：把大问题拆成子问题，只要把每个子问题的最优解保存下来，后面再用时直接查表。

#### 环形结构的拆解  

因为第 1 栋和第 n 栋相邻，**两者不能同时被偷**。于是我们可以把环拆成两条“直线”来分别求解：

1. **不偷第 1 栋** → 考虑房子 `[1 … n‑1]`（下标 1 到 n‑1）。  
2. **不偷第 n 栋** → 考虑房子 `[0 … n‑2]`（下标 0 到 n‑2）。

这两种情形各自都变成了**经典的 “House Robber”**（线性不相邻）问题。对每条线性区间求出最大偷金额，最后取两者的较大值即为答案。

#### 线性 House Robber 的 DP

设 `dp[i]` 为**考虑前 i 栋（下标 0 … i‑1）时能偷到的最大金额**。状态转移：

- 不偷第 i‑1 栋 → 金额仍是 `dp[i‑1]`  
- 偷第 i‑1 栋 → 前面最多只能偷到第 i‑3 栋，即 `dp[i‑2] + nums[i‑1]`

取两者最大：

```
dp[i] = max(dp[i‑1], dp[i‑2] + nums[i‑1])
```

初始条件：

- `dp[0] = 0`（不考虑任何房子）
- `dp[1] = nums[0]`（只考虑第一栋）

因为只需要前两项即可计算后续，**可以把数组压缩成两个变量**，进一步降低空间。

#### 代码（Python）

```python
from typing import List

def rob(nums: List[int]) -> int:
    """
    主函数，求环形街区的最大偷金额
    """
    n = len(nums)
    if n == 0:
        return 0
    if n == 1:                # 只有一栋房子，直接偷
        return nums[0]

    # 计算区间 nums[l:r]（左闭右开）的最大偷金额
    def rob_linear(l: int, r: int) -> int:
        prev2, prev1 = 0, 0   # prev2 = dp[i-2], prev1 = dp[i-1]
        for i in range(l, r):
            cur = max(prev1, prev2 + nums[i])  # dp[i] 的公式
            prev2, prev1 = prev1, cur          # 向前滚动窗口
        return prev1

    # 情形1：不偷第一栋 -> 考虑 [1, n)
    money1 = rob_linear(1, n)
    # 情形2：不偷最后一栋 -> 考虑 [0, n-1)
    money2 = rob_linear(0, n - 1)

    return max(money1, money2)   # 取两种情形的最大值
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  解释：我们分别遍历两段子数组，每段最多遍历 `n-1` 次，总共不超过 `2·(n-1)`，即线性时间。相比暴力的指数级，快了很多。

- **空间复杂度**：`O(1)`  
  解释：只用了常数个额外变量（`prev2, prev1, cur`），没有使用额外的数组，空间几乎不增长。

---

## 心得

- **核心技巧**：把环形问题转化为两次线性 DP，利用“相邻不能同偷”的约束将环拆成互斥的两条路径。  
- **适用的题型**：  
  1. **环形打家劫舍**（本题）  
  2. **环形最大独立集**（图论中把环形节点选成不相邻的最大权重子集）  
  3. **环形选择题**（例如“环形礼物分配”需要避免首尾冲突的 DP）  
- **一句话总结解题钥匙**：**“把环切开，分别在两条不相交的直线上做 DP，最后取最大”。**

---

## 反思

- **第一反应**：看到环形、相邻不能同偷，立刻想到“把环拆成两段”，因为环的首尾冲突只能让我们在某个端点做出取舍。  
- **最容易踩的坑**：  
  - 当数组长度为 `1` 时，直接返回唯一元素；如果忘记这一步会把区间 `[1, n)` 写成空导致错误。  
  - 当长度为 `2` 时，两段子数组会出现空区间，需要确保 `rob_linear` 能正确处理空区间（返回 0）。  
  - 在实现 DP 时，初始化 `prev2, prev1` 必须对应 `dp[0]` 与 `dp[1]` 的含义，否则会导致错位。  
- **下次遇到同类题**：第一步先**判断环的冲突点**，把问题拆成“固定不选”或“固定不偷”几种子情形，再在每个子情形上使用**线性 DP**或**滑动窗口**求最优。这样思路清晰，代码也容易写对。