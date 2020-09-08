# #983. 最小票价费用 / Minimum Cost For Tickets

> 难度：中等 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/minimum-cost-for-tickets/)

---

## 题目（英文原版）

**Description**

You have planned some train traveling one year in advance. The days of the year in which you will travel are given as an integer array days. Each day is an integer from 1 to 365.
Train tickets are sold in three different ways:
The passes allow that many days of consecutive travel.
Return the minimum number of dollars you need to travel every day in the given list of days.

**Examples**

**Example 1:**

```
Input: days = [1,4,6,7,8,20], costs = [2,7,15]
Output: 11
Explanation: For example, here is one way to buy passes that lets you travel your travel plan:
On day 1, you bought a 1-day pass for costs[0] = $2, which covered day 1.
On day 3, you bought a 7-day pass for costs[1] = $7, which covered days 3, 4, ..., 9.
On day 20, you bought a 1-day pass for costs[0] = $2, which covered day 20.
In total, you spent $11 and covered all the days of your travel.
```

**Example 2:**

```
Input: days = [1,2,3,4,5,6,7,8,9,10,30,31], costs = [2,7,15]
Output: 17
Explanation: For example, here is one way to buy passes that lets you travel your travel plan:
On day 1, you bought a 30-day pass for costs[2] = $15 which covered days 1, 2, ..., 30.
On day 31, you bought a 1-day pass for costs[0] = $2 which covered day 31.
In total, you spent $17 and covered all the days of your travel.
```

**Constraints**

- 1 <= days.length <= 365
- 1 <= days[i] <= 365
- days is in strictly increasing order.
- costs.length == 3
- 1 <= costs[i] <= 1000

---

## 题目（中文翻译）

你提前一年计划了若干次火车出行。需要出行的日期以整数数组（integer array）`days` 给出。`days` 中的每个元素是 1 到 365 之间的整数，表示一年中的第几天。

火车票有三种不同的购买方式（对应三种通行证）：

- `costs[0]` 对应的 1 天通行证，可覆盖购买当天以及随后 **1 天** 的连续旅行。
- `costs[1]` 对应的 7 天通行证，可覆盖购买当天以及随后 **7 天** 的连续旅行。
- `costs[2]` 对应的 30 天通行证，可覆盖购买当天以及随后 **30 天** 的连续旅行。

请返回在给定的 `days` 列表中，覆盖所有出行日期所需的最少美元数。

### 示例

#### 示例 1
**输入**  
`days = [1,4,6,7,8,20]`, `costs = [2,7,15]`  
**输出**  
`11`  
**解释**  
下面是一种购买通行证的方案，使得能够满足全部出行计划：

- 第 1 天，购买一张 1 天通行证，费用为 `costs[0] = $2`，覆盖第 1 天。  
- 第 3 天，购买一张 7 天通行证，费用为 `costs[1] = $7`，覆盖第 3、4、…、9 天。  
- 第 20 天，购买一张 1 天通行证，费用为 `costs[0] = $2`，覆盖第 20 天。

总共花费 `$11`，覆盖了所有出行日期。

#### 示例 2
**输入**  
`days = [1,2,3,4,5,6,7,8,9,10,30,31]`, `costs = [2,7,15]`  
**输出**  
`17`  
**解释**  
下面是一种购买通行证的方案，使得能够满足全部出行计划：

- 第 1 天，购买一张 30 天通行证，费用为 `costs[2] = $15`，覆盖第 1、2、…、30 天。  
- 第 31 天，购买一张 1 天通行证，费用为 `costs[0] = $2`，覆盖第 31 天。

总共花费 `$17`，覆盖了所有出行日期。

### 约束条件

- `1 <= days.length <= 365`
- `1 <= days[i] <= 365`
- `days` 严格递增。
- `costs.length == 3`
- `1 <= costs[i] <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**每到需要乘车的那一天，就枚举三种票的购买方式**（1 天、7 天、30 天），递归地把后面的所有天数全部算一遍，取最小花费。  

- **数据结构**：  
  - `days` 列表本身保存了所有要出行的日子。  
  - 为了判断“今天是否需要乘车”，可以把 `days` 放进 **哈希表**（在 Python 里用 `set`），这就像查字典一样，`key` 是日期，`value`（这里不需要）可以理解成对应的页码。  
- **为什么正确**：  
  - 递归的每一步都把「今天」要么买 1 天票，要么买 7 天票，要么买 30 天票，这三种选择覆盖了所有合法的购买方式。递归结束的条件是已经处理完所有出行日子，此时花费为 0。于是整个递归树遍历了所有可能的组合，取最小值自然就是答案。  
- **时间/空间复杂度（大白话）**：  
  - 设需要乘车的天数为 `n`（`n ≤ 365`）。每一天都有 3 种选择，递归树的深度最多是 `n`，所以最坏情况下会产生约 `3^n` 条路径，**时间复杂度是指数级**，在实际输入（最多 365 天）下根本跑不完。  
  - 递归调用会占用栈空间，最深 `n` 层，**空间复杂度是 O(n)**。  

#### 代码（Python）

```python
from functools import lru_cache

def mincostTickets_bruteforce(days, costs):
    """暴力递归解法，时间指数级，只用于理解思路"""

    day_set = set(days)                 # 把出行日子放进哈希表，查 O(1)
    last_day = days[-1]                 # 最后一个需要乘车的日子

    @lru_cache(maxsize=None)           # 记忆化，防止重复子问题（仍然指数级）
    def dfs(cur):
        """
        返回从 cur 天（包括 cur）到 last_day 所需的最少花费。
        cur 超过 last_day 时说明已经买完票，返回 0。
        """
        if cur > last_day:              # 已经处理完所有天
            return 0

        if cur not in day_set:          # 今天不需要乘车，直接看明天
            return dfs(cur + 1)

        # 三种买票方式，递归求后面的最小花费
        cost1 = costs[0] + dfs(cur + 1)          # 买 1 天票
        cost7 = costs[1] + dfs(cur + 7)          # 买 7 天票
        cost30 = costs[2] + dfs(cur + 30)        # 买 30 天票
        return min(cost1, cost7, cost30)

    return dfs(1)                        # 从第 1 天开始检查
```

#### 复杂度  

- **时间复杂度**：`O(3^n)`（指数级），因为每个需要乘车的日子都有 3 种分支。  
- **空间复杂度**：`O(n)`，递归栈的深度最多等于需要乘车的天数 `n`。  

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **“每一天只关心今天是否需要乘车”**，而且 **购买的票只会影响后面有限的几天**（最多 30 天）。这正好适合使用 **动态规划（DP）**：把“大问题”拆成“小问题”，把每一天的最小花费记下来，后面的天只需要查表，不必重新枚举所有组合。

1. **慢在哪里**  
   - 暴力解每次都要向后递归 `+7`、`+30` 天，导致大量重复计算。  
   - 同一天的子问题会被多次求解，浪费时间。

2. **优化思路**  
   - 用一个一维数组 `dp[i]` 表示 **到第 `i` 天为止（包括第 `i` 天）已经花的最少钱**。  
   - `i` 从 `1` 到 `365`（因为一年最多 365 天），如果 `i` 不是出行日子，则 `dp[i] = dp[i‑1]`（不需要买票，花费不变）。  
   - 如果 `i` 是出行日子，则有三种选择：  
     - 买 1 天票：`dp[i] = dp[i-1] + costs[0]`  
     - 买 7 天票：`dp[i] = dp[i-7] + costs[1]`（`i-7` 可能为负，取 `0`）  
     - 买 30 天票：`dp[i] = dp[i-30] + costs[2]`（同理）  
   - 取这三种情况的最小值，即为 `dp[i]`。  
   - 最终答案是 `dp[365]`（或者直接 `dp[last_day]`，因为后面不需要乘车，花费不再变化）。

3. **核心数据结构解释**  
   - **数组** `dp[0…365]`：想象成一本“记账本”，第 `i` 页记下到第 `i` 天为止的最少花费。我们每翻一页（i 增加 1），都把今天的费用算进去。  
   - **集合** `day_set`：像字典一样快速判断今天是否需要乘车，省去遍历 `days` 的时间。

4. **图示（文字版）**  
   - 假设 `days = [1,4,6,7,8,20]`，`costs = [2,7,15]`。  
   - 当我们算到第 8 天时，`dp[8]` 会考虑：  
     - 如果在第 8 天买 1 天票，则费用 = `dp[7] + 2`。  
     - 如果在第 2 天买了 7 天票（覆盖 2~8），费用 = `dp[1] + 7`（因为第 2 天之前已经花了 `dp[1]`）。  
     - 如果在第 -22 天买了 30 天票（相当于从第 1 天就买），费用 = `dp[0] + 15 = 15`。  
   - 取最小值得到 `dp[8] = 11`（对应题目示例的最优方案）。

#### 代码（Python）

```python
def mincostTickets(days, costs):
    """
    动态规划解法：时间 O(365) ≈ O(1)，空间 O(365)。
    dp[i] 表示到第 i 天（包括 i）为止的最小花费。
    """
    day_set = set(days)               # 哈希表，判断是否需要乘车，O(1) 查找
    last_day = days[-1]               # 最后一次出行的日期

    # dp[0] = 0，表示第 0 天（不真实存在）花费为 0
    dp = [0] * (last_day + 1)         # 只算到最后一次出行的那天即可

    for i in range(1, last_day + 1):
        if i not in day_set:          # 今天不需要乘车，费用和昨天一样
            dp[i] = dp[i - 1]
        else:
            # 购买 1 天票
            cost1 = dp[i - 1] + costs[0]

            # 购买 7 天票，i-7 可能为负，用 max 防止索引错误
            cost7 = dp[max(0, i - 7)] + costs[1]

            # 购买 30 天票，同理
            cost30 = dp[max(0, i - 30)] + costs[2]

            dp[i] = min(cost1, cost7, cost30)

    return dp[last_day]               # 最后一天的累计最小花费即答案
```

#### 复杂度  

- **时间复杂度**：`O(365)`，因为循环最多遍历 365 天，常数级别的操作。即使 `days` 长度只有 1，仍然最多跑 365 次，属于 **线性时间**，在实际数据范围内几乎可以视作 O(1)。  
- **空间复杂度**：`O(365)`，存放 DP 表的数组大小固定为一年天数（约 365），也可以说是 **常数级别的空间**。  

---

## 心得  

- **核心技巧**：**动态规划 + 前缀（累计）最小费用**。把“买票后覆盖的天数”转化为对过去若干天状态的转移，避免重复计算。  
- **适用的题型**：  
  1. “最小费用覆盖区间”类（如 **“买票”**、**“房屋租金最小化”**）。  
  2. “在有限时间窗口内选择最优操作”类（如 **“跳跃游戏 II”** 的 DP 版本）。  
  3. “有期限的优惠券/折扣”问题（如 **“打折券的最小消费”**）。  
- **一句话总结**：**把每一天的最小花费记下来，后面的决策只看过去的几天即可**——这就是 DP 的魔法。

---

## 反思  

- **第一反应**：看到“1 天、7 天、30 天的通票”，马上想到“枚举每一天的三种选择”。这就是暴力递归的想法。  
- **最容易踩的坑**：  
  - **边界处理**：`i-7`、`i-30` 可能小于 0，需要用 `max(0, …)` 防止数组越界。  
  - **只算到最后一次出行的天数**：如果直接建立长度 366 的 DP，虽然也对，但会多算无用的天数。  
  - **忘记把不出行的天数直接继承前一天的费用**，导致错误的额外费用。  
- **下次类似题目第一步**：**先把“状态”定义清楚**（这里是“到第 i 天的最小花费”），再思考**“从哪个或哪些以前的状态可以转移到现在”。这样往往能直接写出 DP 转移方程，避免盲目枚举。