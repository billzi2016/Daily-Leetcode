# #2369. 检查数组是否存在有效划分 / Check if There is a Valid Partition For The Array

> 难度：中等 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/check-if-there-is-a-valid-partition-for-the-array/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums. You have to partition the array into one or more contiguous subarrays.
We call a partition of the array valid if each of the obtained subarrays satisfies one of the following conditions:
Return true if the array has at least one valid partition. Otherwise, return false.

**Examples**

**Example 1:**

```
Input: nums = [4,4,4,5,6]
Output: true
Explanation: The array can be partitioned into the subarrays [4,4] and [4,5,6].
This partition is valid, so we return true.
```

**Example 2:**

```
Input: nums = [1,1,1,2]
Output: false
Explanation: There is no valid partition for this array.
```

**Constraints**

- 2 <= nums.length <= 105
- 1 <= nums[i] <= 106

---

## 题目（中文翻译）

给定一个 **0 索引** 的整数数组 `nums`。你需要将数组划分为一个或多个**连续子数组（contiguous subarray）**。  

我们称一次划分为**有效划分（valid partition）**，如果得到的每个子数组满足以下任意一种条件：

1. 子数组恰好由 **两个相等的元素** 组成，例如 `[x, x]`。  
2. 子数组恰好由 **三个相等的元素** 组成，例如 `[x, x, x]`。  
3. 子数组恰好由 **三个连续递增的元素** 组成，即 `nums[i] + 1 == nums[i+1] && nums[i+1] + 1 == nums[i+2]`，例如 `[x, x+1, x+2]`。  

如果数组至少存在一种满足上述条件的划分，返回 `true`；否则返回 `false`。

### 示例

**示例 1**  
输入：`nums = [4,4,4,5,6]`  
输出：`true`  
解释：数组可以划分为子数组 `[4,4]` 和 `[4,5,6]`。该划分满足条件 1 和条件 3，因此返回 `true`。

**示例 2**  
输入：`nums = [1,1,1,2]`  
输出：`false`  
解释：不存在满足条件的划分方式，返回 `false`。

### 约束条件

- `2 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的切分方式都枚举一遍**，只要找到一种切分使得每个子数组满足题目给出的三条合法规则，就返回 `True`，全部尝试完仍没有合法切分则返回 `False`。

- **数据结构**：我们只需要一个普通的 Python 列表 `nums`，以及一个递归函数 `dfs(i)` 表示“从下标 `i` 开始往后，剩下的部分是否可以被合法划分”。递归的过程类似于 **查字典**：把当前下标 `i` 当作“词”，我们在字典里查找是否有符合规则的“解释”（即合法子数组的长度 2 或 3），找到后继续查找下一个词 `i+len`，直到走到数组末尾。
- **为什么正确**：递归函数会尝试 **所有** 合法的子数组长度（2 或 3），只要其中一种选择能够把后面的子数组全部合法划分，`dfs(i)` 就会返回 `True`。因此只要存在至少一种合法划分，递归必定能找到并返回 `True`。
- **时间/空间复杂度**：  
  - 每个位置最多有 2（长度 2）+ 2（长度 3）= 4 种尝试（实际最多 2 种，因为长度 2 只能检查相等，长度 3 需要检查相等或递增）。在最坏情况下，这种递归会产生指数级的调用树，时间复杂度大约是 **O(2ⁿ)**，相当于“每走一步都有两条路可以走”。  
  - 递归栈的深度最坏是 `n`，所以空间复杂度是 **O(n)**（调用栈占用的空间）。

> **大白话**：如果你把每一步想象成“要不要在这里剪刀”，每个位置都有两种可能（剪或不剪），那么所有可能的组合就是 2 的 n 次方，随 n 增大会非常爆炸。

#### 代码（Python）

```python
from typing import List

def validPartition(nums: List[int]) -> bool:
    n = len(nums)

    # dfs(i) 表示从下标 i 开始的后缀是否可以合法划分
    def dfs(i: int) -> bool:
        # 到了数组末尾，说明所有子数组都已经合法划分
        if i == n:
            return True
        # 剩余元素不足 2 个，直接返回 False
        if i > n - 2:
            return False

        # ----- 尝试长度为 2 的子数组 -----
        # 条件：两个数相等
        if i + 1 < n and nums[i] == nums[i + 1]:
            if dfs(i + 2):          # 如果把这两个数切走后，后面的还能合法划分
                return True

        # ----- 尝试长度为 3 的子数组 -----
        if i + 2 < n:
            # 1) 全部相等
            if nums[i] == nums[i + 1] == nums[i + 2]:
                if dfs(i + 3):
                    return True
            # 2) 连续递增（比如 4,5,6）
            if nums[i] + 1 == nums[i + 1] and nums[i + 1] + 1 == nums[i + 2]:
                if dfs(i + 3):
                    return True

        # 所有尝试都失败，返回 False
        return False

    return dfs(0)
```

#### 复杂度

- **时间复杂度**：`O(2ⁿ)` —— 每一步都有两条“剪”或“不剪”的路，导致指数级的递归树。  
- **空间复杂度**：`O(n)` —— 最深的递归调用层数等于数组长度 `n`，即调用栈占用的空间。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**重复计算**是主要的性能瓶颈：相同的下标 `i` 会被递归多次访问。我们可以用 **记忆化（memo）** 或 **动态规划（DP）** 把已经算好的子问题结果保存下来，只计算一次。

**核心优化点**：

1. **状态定义**  
   用 `dp[i]` 表示“前 i（不含下标 i）个元素是否可以被合法划分”。`dp[0] = True`（空数组天然合法），目标是求 `dp[n]`。

2. **状态转移**  
   - 若 `i ≥ 2` 且 `nums[i‑2] == nums[i‑1]`（两个相等），且 `dp[i‑2]` 为真，则 `dp[i] = True`。  
   - 若 `i ≥ 3` 且 `nums[i‑3] == nums[i‑2] == nums[i‑1]`（三个相等），且 `dp[i‑3]` 为真，则 `dp[i] = True`。  
   - 若 `i ≥ 3` 且 `nums[i‑3] + 1 == nums[i‑2]` 且 `nums[i‑2] + 1 == nums[i‑1]`（递增连续），且 `dp[i‑3]` 为真，则 `dp[i] = True`。

   只要上述任意一种情况成立，就说明前 `i` 个元素可以合法划分。

3. **实现方式**  
   - **自底向上 DP**：从左到右依次填表，时间 `O(n)`，空间 `O(n)`。  
   - **滚动数组**：因为转移只依赖 `i‑2`、`i‑3`，我们可以只保留最近的几个状态，进一步把空间压到 `O(1)`。

**类比**：把 `dp[i]` 想成“从起点走到第 i 步是否有合法的路”。每一步我们只检查最近的 2 步或 3 步是否可以走过去，就像在走格子游戏，只要前面已经有合法的路径，后面就可以继续。

#### 代码（Python）

```python
from typing import List

def validPartition(nums: List[int]) -> bool:
    n = len(nums)
    # dp[i] 表示前 i 个元素（0 ~ i-1）是否可以合法划分
    dp = [False] * (n + 1)
    dp[0] = True                     # 空数组合法

    for i in range(2, n + 1):
        # ----- 长度为 2，两个相等 -----
        if nums[i - 2] == nums[i - 1] and dp[i - 2]:
            dp[i] = True

        # ----- 长度为 3，三种可能 -----
        if i >= 3:
            # 3 个相等
            if nums[i - 3] == nums[i - 2] == nums[i - 1] and dp[i - 3]:
                dp[i] = True
            # 递增连续
            if (nums[i - 3] + 1 == nums[i - 2] and
                nums[i - 2] + 1 == nums[i - 1] and
                dp[i - 3]):
                dp[i] = True

    return dp[n]
```

> **空间优化（可选）**：如果想把空间降到 `O(1)`，只需要保存最近三个布尔值 `dp[i-3]、dp[i-2]、dp[i-1]`，在循环里滚动更新即可。

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历一次数组，每个位置做常数次检查。与暴力解相比，从指数级降到了线性级，快了几个数量级。  
- **空间复杂度**：`O(n)`（若使用滚动数组则 `O(1)`）—— 只需要一个长度为 `n+1` 的布尔数组（或常数个布尔变量）来保存状态。

---

## 心得

- **核心技巧**：**动态规划**——把“大问题”拆成“子问题”，记录每一步是否可行，避免重复计算。  
- **适用题型**：  
  1. “能否把序列划分成满足某种局部规则的子段” （如 LeetCode 1235 `Maximum Profit in Job Scheduling` 的 DP 思路）。  
  2. “能否用若干块拼出整个序列” （如 LeetCode 139. `Word Break`）。  
  3. “是否存在合法路径/划分/配对” 的一维 DP（如 LeetCode 91. `Decode Ways`）。  
- **一句话总结**：**把“从头到尾是否可以划分”抽象为布尔 DP，逐步检查最近的 2/3 步即可**。

---

## 反思

- **第一反应**：看到“划分成若干连续子数组”，本能想到递归枚举所有切点，检查每段是否合法。  
- **最容易踩的坑**：  
  - **遗漏长度为 3 的递增情况**（题目允许 `[x, x+1, x+2]`）。  
  - **边界条件**：`dp` 的下标偏移容易写错，尤其是 `i-2`、`i-3` 的合法性检查。  
  - **空间泄漏**：如果直接用递归且没有记忆化，会导致栈溢出（`n` 可达 10⁵）。  
- **下次遇到同类题**：第一步先 **明确子数组的合法形式**，再 **定义 dp[i] 表示前 i 个元素是否可划分**，最后 **写出状态转移**（只看最近几步），这样思路更清晰、实现更稳妥。