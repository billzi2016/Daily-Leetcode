# #416. 等和子集划分 / Partition Equal Subset Sum

> 难度：中等 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/partition-equal-subset-sum/)

---

## 题目（英文原版）

**Description**

Given an integer array nums, return true if you can partition the array into two subsets such that the sum of the elements in both subsets is equal or false otherwise.

**Examples**

**Example 1:**

```
Input: nums = [1,5,11,5]
Output: true
Explanation: The array can be partitioned as [1, 5, 5] and [11].
```

**Example 2:**

```
Input: nums = [1,2,3,5]
Output: false
Explanation: The array cannot be partitioned into equal sum subsets.
```

**Constraints**

- 1 <= nums.length <= 200
- 1 <= nums[i] <= 100

---

## 题目（中文翻译）

给定一个整数数组 `nums`，如果能够将数组划分为两个子集（subset），使得两个子集中的元素和相等，则返回 `true`；否则返回 `false`。

**示例**

示例 1  
输入: `nums = [1,5,11,5]`  
输出: `true`  
解释: 数组可以划分为 `[1, 5, 5]` 和 `[11]`，两个子集的和均为 11。

示例 2  
输入: `nums = [1,2,3,5]`  
输出: `false`  
解释: 无法将数组划分为和相等的两个子集。

**约束条件**

- `1 <= nums.length <= 200`
- `1 <= nums[i] <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**枚举所有可能的划分**，看有没有一种划分能够让两部分的和相等。  
可以把每个元素想象成「是」或「否」的选择——「是」表示放进子集 A，「否」表示放进子集 B。  
于是我们可以用 **回溯（深度优先搜索）** 把每个元素逐个决定放哪边，递归到底时检查两边的和是否相等。

- **用到的数据结构**：  
  - `list nums`：原始数组。  
  - 两个整数 `sum_a`、`sum_b` 分别记录当前子集 A、B 的累计和。  
  - 递归函数的调用栈相当于「记事本」，保存我们在每一步的选择。

- **为什么正确**：  
  - 回溯会遍历 **所有** 2ⁿ 种放法（每个元素有两种去向），因此只要存在合法划分，必然会被遍历到并返回 `True`。

- **复杂度分析**（大白话）  
  - **时间**：每个元素都有「放进 A」或「放进 B」两种可能，全部遍历下来要尝试 2ⁿ 种情况。这里的 `n` 是数组长度。2ⁿ 的增长速度非常快，像 10 → 1024，20 → 1,048,576，30 → 超过十亿。  
    - 用大写 O 表示：`O(2^n)`。  
  - **空间**：递归深度最多为 `n`，再加上少量额外变量，空间是 `O(n)`。

#### 代码（Python）

```python
def can_partition_bruteforce(nums):
    """暴力回溯版，直接枚举所有划分"""

    total = sum(nums)
    # 如果总和是奇数，根本不可能平分
    if total % 2 != 0:
        return False

    target = total // 2               # 只需要让其中一个子集的和等于 target

    def dfs(index, cur_sum):
        """
        index: 当前处理到的下标
        cur_sum: 已经放进子集 A 的元素和
        """
        # 已经凑到目标和，直接返回 True
        if cur_sum == target:
            return True
        # 超过目标或者遍历完所有元素，说明这条路不行
        if cur_sum > target or index == len(nums):
            return False

        # 选择把 nums[index] 放进子集 A
        if dfs(index + 1, cur_sum + nums[index]):
            return True
        # 或者不放（等价于放进子集 B），继续往下走
        return dfs(index + 1, cur_sum)

    return dfs(0, 0)
```

#### 复杂度

- **时间复杂度**：`O(2^n)` —— 需要尝试所有 2ⁿ 种放法，随元素个数指数增长。  
- **空间复杂度**：`O(n)` —— 递归栈的深度最多等于数组长度 `n`。

---

### 2. 最优解

#### 思路  

从暴力解我们看到 **瓶颈** 在于「枚举所有组合」导致指数级时间。  
实际上，这道题只要求判断是否能把数组划分成 **两部分和相等**，等价于：

> 是否能在数组中挑选出若干个数，使它们的和恰好等于 `total / 2`？

这正是经典的 **「0/1 背包」**（subset sum）问题：每个数要么选要么不选，容量是 `target = total/2`，每个数的「价值」与「重量」相同。

**动态规划（DP）** 可以把指数级搜索压缩到多项式时间。思路如下：

1. 先检查总和是否为偶数，若为奇数直接返回 `False`（不可能平分）。
2. 设 `target = total // 2`。我们要判断是否存在子集和为 `target`。
3. 定义布尔型 DP 数组 `dp[i]`，表示「是否能用若干个数凑出和为 i」。
   - 初始时 `dp[0] = True`（空集合的和为 0），其余 `False`。
4. 对每个数 `num`，遍历 `i` 从 `target` **倒序** 到 `num`：
   - `dp[i] = dp[i] or dp[i - num]`
   - 含义：如果以前能凑出 `i - num`，加上当前 `num` 就能凑出 `i`。
   - **倒序遍历** 很关键：保证每个数只使用一次（相当于「0/1」背包），不被同一个数多次累计。

当遍历完所有数后，`dp[target]` 为 `True` 表示可以恰好凑出目标和，从而可以把数组平分。

- **类比**：想象你在玩「拼图」游戏，`target` 是一块固定大小的拼图板，`num` 是不同形状的拼块。`dp[i]` 记录「有没有办法把板子恰好填满 i 的面积」。每放入一块拼块，你就检查「如果把这块拼块放进去，之前能填满的面积会不会变成新的面积」——这正是 DP 的核心思想。

#### 代码（Python）

```python
def can_partition(nums):
    """动态规划（01 背包）实现，时间 O(n * target)，空间 O(target)"""

    total = sum(nums)
    # 总和为奇数不可能平分
    if total % 2 != 0:
        return False

    target = total // 2
    # dp[i] 表示是否能凑出和为 i
    dp = [False] * (target + 1)
    dp[0] = True                     # 空集合可以凑出 0

    for num in nums:
        # 必须倒序遍历，防止同一个数被重复使用
        for i in range(target, num - 1, -1):
            # 如果之前能凑出 i-num，加上当前 num 就能凑出 i
            dp[i] = dp[i] or dp[i - num]
        # 提前结束：如果已经能凑出 target，直接返回 True
        if dp[target]:
            return True

    return dp[target]
```

#### 复杂度

- **时间复杂度**：`O(n * target)`  
  - `n` 是数组长度（最多 200），`target` 最多是 `sum(nums)/2`，而每个 `nums[i] ≤ 100`，所以 `target ≤ 200 * 100 / 2 = 10,000`。  
  - 用大白话说，就是「遍历每个数，再遍历一次从 0 到目标和的所有可能」，这在本题的约束下是完全可以接受的。

- **空间复杂度**：`O(target)`  
  - 只需要一个长度为 `target+1` 的布尔数组来保存「能否凑出该和」的信息。相比于二维 DP（`n * target`），我们把空间压缩到了仅仅目标和大小。

---

## 心得

- **核心技巧**：把「能否平分」转化为「是否存在子集和为总和的一半」的 **0/1 背包（子集和）** 问题，然后使用 **一维动态规划** 求解。
- **适用的题型**  
  1. *Subset Sum*（LeetCode 416、494）  
  2. *Knapsack Capacity*（背包容量恰好装满）  
  3. *Equal Sum Partition*（把数组划分成相等和的多组）  
- **一句话总结解题钥匙**：**把目标值固定为总和的一半，用 DP 记录「能否凑出每个可能的和」**。

---

## 反思

- **第一反应**：看到「把数组分成两部分和相等」就想到「找一个子集的和等于一半」，于是立刻联想到子集和（subset sum）问题。
- **最容易踩的坑**  
  1. **总和为奇数**：忘记提前返回 `False`，会导致 DP 仍然尝试无意义的目标值。  
  2. **正向遍历 DP**：如果正向遍历，会把同一个数重复使用，导致错误的答案。  
  3. **边界条件**：`dp[0]` 必须初始化为 `True`，否则即使没有任何数也无法得到和为 0 的状态。  
- **下次遇到同类题的第一步**：先计算总和，判断奇偶性；再把问题抽象为「是否能凑出某个固定目标」的子集和问题，准备使用 DP（或位运算）求解。