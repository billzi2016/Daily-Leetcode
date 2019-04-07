# #377. 组合总和 IV / Combination Sum IV

> 难度：中等 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/combination-sum-iv/)

---

## 题目（英文原版）

**Description**

Given an array of distinct integers nums and a target integer target, return the number of possible combinations that add up to target.
The test cases are generated so that the answer can fit in a 32-bit integer.
Follow up: What if negative numbers are allowed in the given array? How does it change the problem? What limitation we need to add to the question to allow negative numbers?

**Examples**

**Example 1:**

```
Input: nums = [1,2,3], target = 4
Output: 7
Explanation:
The possible combination ways are:
(1, 1, 1, 1)
(1, 1, 2)
(1, 2, 1)
(1, 3)
(2, 1, 1)
(2, 2)
(3, 1)
Note that different sequences are counted as different combinations.
```

**Example 2:**

```
Input: nums = [9], target = 3
Output: 0
```

**Constraints**

- 1 <= nums.length <= 200
- 1 <= nums[i] <= 1000
- All the elements of nums are unique.
- 1 <= target <= 1000

---

## 题目（中文翻译）

给定一个由 **不同整数** 组成的数组 `nums` 和一个目标整数 `target`，返回所有能够使元素之和等于 `target` 的 **组合方式**（combination）的数量。  
测试用例保证答案可以放入 32 位整数中。

**示例 1**  

**示例 2**  

**约束条件**  
- 1 ≤ `nums.length` ≤ 200  
- 1 ≤ `nums[i]` ≤ 1000  
- `nums` 中的所有元素互不相同。  
- 1 ≤ `target` ≤ 1000  

**进阶**：如果数组中允许出现负数，会对问题产生怎样的影响？需要在题目中加入哪些限制才能在允许负数的情况下仍然得到可解的答案？

---

### 示例

#### 示例 1
**输入**  
```
nums = [1,2,3], target = 4
```
**输出**  
```
7
```
**解释**  
可能的组合方式如下（不同的序列视为不同的组合）：
- (1, 1, 1, 1)
- (1, 1, 2)
- (1, 2, 1)
- (1, 3)
- (2, 1, 1)
- (2, 2)
- (3, 1)

#### 示例 2
**输入**  
```
nums = [9], target = 3
```
**输出**  
```
0
```

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**枚举所有可能的序列**，看哪些序列的元素之和恰好等于 `target`。  
可以把这个过程想象成“拼积木”：  
- `nums` 中的每个数字是一块不同颜色的积木。  
- 我们可以无限次使用每块积木（题目说可以重复使用），把它们一个接一个堆起来，直到总高度恰好等于 `target`。  
- 每一种堆积的顺序都算作一种不同的组合（因为序列不同算不同），所以 `(1,2,1)` 与 `(1,1,2)` 是两种不同的堆法。

实现上可以使用 **深度优先搜索（DFS）** 或者 **回溯**：  
1. 从 `target` 开始往下走，每走一步就尝试把 `nums` 中的每个数字 `num` 放到当前序列的末尾。  
2. 把 `target` 减去 `num`，得到新的剩余目标 `rest = target - num`。  
3. 如果 `rest == 0`，说明找到了一种合法组合，计数加一。  
4. 如果 `rest < 0`，说明已经超出目标，直接回溯（剪枝）。  

这种方法一定能找出所有合法组合，因为我们把每一种可能的放置顺序都尝试了一遍。  

**为什么正确？**  
- 递归的每一层都代表“已经选好了前面的若干个数”，剩下的目标 `rest` 必须由后面的数继续填满。  
- 当 `rest` 为 0 时，恰好找到了一个完整的序列；当 `rest` 为负时，说明这条路径不可能再回到 0，直接放弃即可。  
- 递归遍历了所有可能的放置顺序，所以不会漏掉任何合法组合。

**时间/空间复杂度**（大白话解释）  
- 时间复杂度：最坏情况下会尝试 **所有可能的序列**。如果 `target = 4`、`nums = [1,2,3]`，序列的长度最多是 `target / min(nums) = 4`，每一步都有 `len(nums)` 种选择，所以大致是 `O(k^target)`（指数级），这里的 `k = len(nums)`。用大写的 `O(n²)` 之类的多项式来描述并不合适，因为它是指数增长的，实际运行会非常慢。  
- 空间复杂度：递归栈的深度等于序列的最大长度，即 `target / min(nums)`，所以是 `O(target)` 的额外空间。

#### 代码（Python）

```python
from typing import List

def combinationSum4_bruteforce(nums: List[int], target: int) -> int:
    """暴力递归，枚举所有序列（会超时）"""
    count = 0                     # 用来统计合法组合的个数

    def dfs(rest: int) -> None:
        """尝试把剩余的 target（rest）用 nums 填满"""
        nonlocal count
        if rest == 0:            # 正好填满，找到一种组合
            count += 1
            return
        if rest < 0:             # 超出目标，直接回退
            return
        # 对每一个数字，都尝试放到序列的末尾
        for num in nums:
            dfs(rest - num)      # 递归处理剩余的部分

    dfs(target)                  # 从完整的 target 开始搜索
    return count
```

#### 复杂度  

- **时间复杂度**：`O(k^target)`（指数级），其中 `k = len(nums)`。意思是随着目标值 `target` 增大，搜索的树会呈指数倍增长，实际会很慢。  
- **空间复杂度**：`O(target)`，因为递归调用的最大深度等于序列的最长可能长度（最坏情况下全是最小的数字）。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**大量重复计算**。例如在 `nums = [1,2,3]`、`target = 4` 时，子问题 “凑成 `3` 的组合数” 会被多次求解（`1+2+?`、`2+1+?`、`3+?` 都会递归到同一个子问题）。  
这正好符合 **动态规划（Dynamic Programming）** 的使用场景：  
- **子问题**：`dp[i]` 表示“凑成目标 `i` 的组合数”。  
- **状态转移**：要得到 `dp[i]`，可以把最后一步选的数字记为 `num`，那么前面必须凑成 `i - num`。于是  

\[
dp[i] = \sum_{num \in nums,\; i \ge num} dp[i - num]
\]

- **初始状态**：`dp[0] = 1`，因为凑成 0 有一种“空序列”方式（不选任何数字）。  

这就是一个**自底向上的** DP（从小目标逐步构造到大目标），每个 `dp[i]` 只计算一次，避免了暴力解的重复递归。  

**类比**：把 `dp` 想成一本“查字典”。  
- `i` 就像字典里要查的“页码”。  
- `dp[i]` 是在第 `i` 页上写的答案。  
- 当我们想知道第 `i` 页的答案时，只需要看前面几页（`i - num`）的答案，然后把它们加起来。  

**为什么这比暴力快？**  
- 每个 `i`（从 1 到 `target`）只遍历一次 `nums`，时间是 `O(target * len(nums))`，是多项式级别的。  
- 不再有指数级的递归树，也不需要额外的递归栈，空间只需要 `O(target)` 的数组。  

#### 代码（Python）

```python
from typing import List

def combinationSum4_dp(nums: List[int], target: int) -> int:
    """
    动态规划：dp[i] 表示凑成 i 的组合数（顺序不同算不同）。
    时间复杂度 O(target * len(nums))，空间复杂度 O(target)。
    """
    dp = [0] * (target + 1)   # dp[0..target]，全部先设为 0
    dp[0] = 1                 # 空序列凑成 0，算 1 种方式

    # 从 1 填到 target
    for i in range(1, target + 1):
        # 枚举所有可能的最后一个数字
        for num in nums:
            if i >= num:      # 只有当 i >= num 时才有意义
                dp[i] += dp[i - num]   # 累加前缀子问题的答案
                # 这里不需要取模，因为题目保证答案在 32 位整数范围内

    return dp[target]
```

#### 复杂度  

- **时间复杂度**：`O(target * n)`，其中 `n = len(nums)`。  
  - 直白解释：我们要算 `target`（最多 1000）个小格子，每个格子里要遍历 `nums`（最多 200）次，所以最多算 200,000 次，算得快。  
- **空间复杂度**：`O(target)`，只需要一个长度为 `target+1` 的数组来保存中间结果。

---

## 心得  

- **核心技巧**：把“把目标分解成若干子目标”的过程抽象为**一维动态规划**，`dp[i]` 表示凑成 `i` 的组合数。  
- **适用的题型**（类似思路）  
  1. **完全背包（Unbounded Knapsack）**——比如 “Coin Change 组合数”。  
  2. **爬楼梯**——`dp[i] = dp[i-1] + dp[i-2]`（也是把最后一步拆开来想）。  
  3. **不同路径计数**——网格里只能向右或向下走时的路径数。  
- **一句话总结解题钥匙**：*把“最后一步”拆出来，用子问题的答案累加，即可从指数爆炸降到多项式。*

---

## 反思  

- **第一反应**：看到“不同序列算不同”，立刻想到递归/回溯去枚举所有排列。  
- **最容易踩的坑**  
  - **顺序计数**：有些组合数问题只关心“组合”（不计顺序），而本题计顺序，需要 **有序** 的 DP（即外层遍历 `i`，内层遍历 `num`）。  
  - **整数溢出**：若答案可能很大，需要取模或使用大整数；本题已说明答案在 32 位整数范围内。  
  - **初始化**：`dp[0] = 1` 必不可少，忘记会导致所有答案为 0。  
- **下次类似题的第一步**：先判断“是否可以把问题拆成‘最后一步+子问题’的形式”，如果可以，就立刻写出状态转移方程，构建 DP。