# #2944. 购买水果的最少硬币数 / Minimum Number of Coins for Fruits

> 难度：中等 · 标签：Array、Dynamic Programming、Queue、Heap (Priority Queue)、Monotonic Queue · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-coins-for-fruits/)

---

## 题目（英文原版）

**Description**

You are given an 0-indexed integer array prices where prices[i] denotes the number of coins needed to purchase the (i + 1)th fruit.
The fruit market has the following reward for each fruit:
Note that even if you can take fruit j for free, you can still purchase it for prices[j - 1] coins to receive its reward.
Return the minimum number of coins needed to acquire all the fruits.

**Examples**

**Example 1:**

```
Input: prices = [3,1,2]
Output: 4
Explanation:
Note that even though you could take the 2 nd fruit for free as a reward of buying 1 st fruit, you purchase it to receive its reward, which is more optimal.
```

**Example 2:**

```
Input: prices = [1,10,1,1]
Output: 2
Explanation:
```

**Example 3:**

```
Input: prices = [26,18,6,12,49,7,45,45]
Output: 39
Explanation:
Note that even though you could take the 6 th fruit for free as a reward of buying 3 rd fruit, you purchase it to receive its reward, which is more optimal.
```

**Constraints**

- 1 <= prices.length <= 1000
- 1 <= prices[i] <= 105

---

## 题目（中文翻译）

你得到一个下标从 **0** 开始的整数数组 **prices**，其中 `prices[i]` 表示购买第 **i + 1** 个水果需要的硬币数。  
水果市场对每个水果都有以下奖励：  

> **注意**：即使你可以免费获得水果 `j`（作为购买水果 `i` 的奖励），你仍然可以支付 `prices[j‑1]` 枚硬币购买它，以获得它的奖励。

返回获取所有水果所需的最少硬币数。

## 示例

### 示例 1  
**输入**: `prices = [3,1,2]`  
**输出**: `4`  
**解释**:  
注意，虽然你可以把第 2 个水果作为购买第 1 个水果的奖励免费获得，但你仍然选择购买它以获得它的奖励，这样更优。

### 示例 2  
**输入**: `prices = [1,10,1,1]`  
**输出**: `2`  
**解释**:  

### 示例 3  
**输入**: `prices = [26,18,6,12,49,7,45,45]`  
**输出**: `39`  
**解释**:  
注意，虽然你可以把第 6 个水果作为购买第 3 个水果的奖励免费获得，但你仍然选择购买它以获得它的奖励，这样更优。

## 约束条件

- `1 <= prices.length <= 1000`
- `1 <= prices[i] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

把水果看成一条直线上的格子，编号 `0 … n‑1`（第 `i` 个水果对应 `prices[i]`）。  
当我们 **买下** 第 `i` 个水果时，需要付 `prices[i]` 枚硬币，同时可以 **免费获得** 紧随其后的至多 `i` 个水果（即可以直接跳到第 `i+1 … i+i+1` 中的任意一个格子继续购买）。  

> **类比**：想象你在玩跳格子游戏，每踩到一个格子要付费，但踩到后可以一次性跨过若干格子继续前进。我们的目标是用最少的费用，从格子 `0` 跳到格子 `n`（代表所有水果都已经得到）。

最直接的办法是枚举所有可能的跳法：  
- 从位置 `i` 出发，尝试跳到合法的每一个 `j`（`i+1 ≤ j ≤ i+1+i`），递归或遍历计算后面的最小花费。  
- 把所有子问题的答案取最小，就是从 `i` 开始的最优费用。

这相当于 **深度优先搜索 + 记忆化**（或直接写成两层循环的 DP），时间会非常慢。

#### 代码（Python）

```python
from functools import lru_cache
from typing import List

def minCoins_bruteforce(prices: List[int]) -> int:
    n = len(prices)

    @lru_cache(None)                 # 记忆化，避免重复计算
    def dfs(i: int) -> int:
        """返回从位置 i 开始获取所有水果的最小硬币数。
        i == n 表示已经到了数组末尾，费用为 0。"""
        if i >= n:                    # 已经买完所有水果
            return 0
        best = float('inf')
        # 购买第 i 个水果后，可直接跳到 [i+1, i+1+i] 中的任意位置
        max_jump = min(n, i + 1 + i)   # 防止越界
        for nxt in range(i + 1, max_jump + 1):
            cost = prices[i] + dfs(nxt)
            best = min(best, cost)
        return best

    return dfs(0)
```

> 关键行解释  
> - `@lru_cache(None)`：把函数调用的结果缓存起来，等价于把子问题的答案记下来，避免指数级重复计算。  
> - `max_jump = min(n, i + 1 + i)`：保证跳到的下标不超过数组末尾。  
> - `cost = prices[i] + dfs(nxt)`：买第 `i` 个水果花 `prices[i]`，随后从 `nxt` 继续最优。

#### 复杂度  

- **时间复杂度**：`O( n * average_jump )`，在最坏情况下每个位置会尝试 `O(i)` 次跳转，导致约 `O(n^2)`。  
  > 用大白话说，就是如果水果有 1000 个，最差情况大概要算 1 000 000 次，这在实际运行中会慢到让人等不及。  
- **空间复杂度**：`O(n)` 用于递归栈和记忆化表（缓存 `dp[i]`），相当于存一张长度为 `n` 的表。

---

### 2. 最优解

#### 思路  

暴力解慢的根源在于 **每次都要在 `[i+1, i+1+i]` 这个区间里找最小的 `dp` 值**，这段区间随 `i` 向左移动而不断变化，导致大量重复的最小值查询。

**关键观察**：

- 我们只关心「区间最小值」，不在乎区间里到底是哪一个 `j`。  
- 当我们从右往左遍历 `i = n‑1 … 0` 时，**窗口** `[i+1, i+1+i]` 也是从右向左“滑动”。  
- 维护一个**单调队列（Monotonic Queue）**，始终把当前窗口内的 `dp` 按升序保存，队首就是窗口最小值。

这样每次只需 **O(1)** 就能得到 `min(dp[j])`，整体时间降到 **线性 O(n)**。

**步骤**：

1. 定义 `dp[i]` 为「从位置 `i` 开始，获取所有水果的最小硬币数」。
2. 边界：`dp[n] = 0`（站在数组右边界，已经没有水果了）。我们把 `dp` 看成长度为 `n+1` 的数组。
3. 从右往左计算 `dp[i]`：  
   `dp[i] = prices[i] + min{ dp[j] | j ∈ [i+1, min(n, i+1+i)] }`  
   窗口右端随 `i` 变化：`right = min(n, i+1+i)`，左端始终是 `i+1`。
4. 使用单调队列 `dq` 保存 **候选下标**，并保持 `dp` 值递增：
   - 当我们把 `i` 向左移动时，需要 **加入** `dp[i+1]`（因为新窗口左端变成 `i+1`），并 **弹出** 超出右端的下标（`> right`）。
   - 维持队列单调：如果新加入的 `dp` 小于队尾对应的 `dp`，就把队尾弹出，因为它永远不可能成为最小值。
5. 计算完 `dp[i]` 后，把它放进队列，为后面的更左侧的 `i` 提供最小值。

#### 代码（Python）

```python
from collections import deque
from typing import List

def minCoins(prices: List[int]) -> int:
    """
    动态规划 + 单调队列（Monotonic Queue）
    返回购买所有水果的最少硬币数，等价于 dp[0]。
    """
    n = len(prices)
    # dp 数组多开一个位置，dp[n] = 0 表示已经买完
    dp = [0] * (n + 1)

    # 单调队列保存下标，队首对应的 dp 值始终是当前窗口的最小值
    dq = deque()
    # 初始时窗口为空，先把 dp[n] 放进去（后面会被弹出）
    dq.append(n)                     # dp[n] = 0

    # 从右往左遍历
    for i in range(n - 1, -1, -1):
        # 1️⃣ 计算当前窗口的右边界（不能超过 n）
        right = min(n, i + 1 + i)    # i+1+i = 2*i+1

        # 2️⃣ 把已经不在窗口里的下标弹出（下标 > right）
        while dq and dq[0] > right:
            dq.popleft()

        # 3️⃣ 当前窗口最小的 dp 值就在队首
        min_next = dp[dq[0]]

        # 4️⃣ 计算 dp[i]
        dp[i] = prices[i] + min_next

        # 5️⃣ 将 dp[i] 加入单调队列，为更左侧的 i 做准备
        #    先把比 dp[i] 大的下标全部弹出，保持 dp 值单调递增
        while dq and dp[dq[-1]] >= dp[i]:
            dq.pop()
        dq.append(i)

    # dp[0] 即为答案
    return dp[0]
```

> 关键行中文注释  
> 1. `right = min(n, i + 1 + i)` —— 计算当前可以跳到的最右位置。  
> 2. `while dq and dq[0] > right: dq.popleft()` —— 删除已经跑出窗口的下标。  
> 3. `min_next = dp[dq[0]]` —— 队首保存的就是窗口内的最小 `dp`。  
> 4. `while dq and dp[dq[-1]] >= dp[i]: dq.pop()` —— 单调队列的核心：把比新值大的旧值踢掉，保证队列从左到右 `dp` 单调递增。  

#### 复杂度  

- **时间复杂度**：`O(n)`。每个下标至多进出队列一次，所有循环的总工作量与 `n` 成线性关系。  
  > 与暴力的 `O(n²)` 相比，假设 `n = 1000`，我们只需要大约 1000 次操作，几乎是瞬间完成。  
- **空间复杂度**：`O(n)`。存 `dp` 表（`n+1`）和单调队列（最多 `n+1` 个下标），均为线性规模。

---

## 心得

- **核心技巧**：**单调队列**（Monotonic Queue）用于在滑动窗口内快速获取最小值。  
- **适用的题型**（类似思路）  
  1. 「跳跃游戏」类最小费用问题（如 LeetCode 1696 “Jump Game VI”）。  
  2. 「滑动窗口最小值」问题（LeetCode 239）。  
  3. 「区间 DP」需要快速查询区间最小值的场景。  
- **一句话总结解题钥匙**：把「从 i 能跳到的所有位置的最小费用」抽象为「窗口最小值」，用单调队列在 O(1) 内维护它。

---

## 反思

- **第一反应**：看到「买第 i 个水果后可以免费获得后面至多 i 个水果」就想到了「跳格子」或「区间覆盖」的模型，随即想到 DP。  
- **最容易踩的坑**  
  - **下标越界**：窗口右端 `i+1+i` 可能超过 `n`，必须 `min(n, …)`。  
  - **单调队列的弹出时机**：忘记在每次循环开始时把已经跑出窗口的元素弹出，会导致取到错误的最小值。  
  - **初始状态**：`dp[n] = 0` 必须放入队列，否则最左侧的 `i` 取不到合法的 `min_next`。  
- **下次类似题的第一步**：先把「从当前位置能到达的所有后继」写成区间，然后思考如何在 **滑动窗口** 中高效获取「区间最小（或最大）值」——单调队列、堆或线段树都是常用工具。