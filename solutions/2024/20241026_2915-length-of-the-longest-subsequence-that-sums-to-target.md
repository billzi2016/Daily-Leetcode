# #2915. 和为目标值的最长子序列长度 / Length of the Longest Subsequence That Sums to Target

> 难度：中等 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/length-of-the-longest-subsequence-that-sums-to-target/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array of integers nums, and an integer target.
Return the length of the longest subsequence of nums that sums up to target. If no such subsequence exists, return -1.
A subsequence is an array that can be derived from another array by deleting some or no elements without changing the order of the remaining elements.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,4,5], target = 9
Output: 3
Explanation: There are 3 subsequences with a sum equal to 9: [4,5], [1,3,5], and [2,3,4]. The longest subsequences are [1,3,5], and [2,3,4]. Hence, the answer is 3.
```

**Example 2:**

```
Input: nums = [4,1,3,2,1,5], target = 7
Output: 4
Explanation: There are 5 subsequences with a sum equal to 7: [4,3], [4,1,2], [4,2,1], [1,1,5], and [1,3,2,1]. The longest subsequence is [1,3,2,1]. Hence, the answer is 4.
```

**Example 3:**

```
Input: nums = [1,1,5,4,5], target = 3
Output: -1
Explanation: It can be shown that nums has no subsequence that sums up to 3.
```

**Constraints**

- 1 <= nums.length <= 1000
- 1 <= nums[i] <= 1000
- 1 <= target <= 1000

---

## 题目（中文翻译）

给定一个下标从 **0** 开始的整数数组 **nums（array）**，以及一个整数 **target（target）**。  
返回 **nums** 中和等于 **target** 的最长子序列（subsequence）的长度。如果不存在满足条件的子序列，返回 **-1**。

**子序列（subsequence）** 是指可以通过删除原数组中的若干（也可以不删除）元素而得到的数组，要求剩余元素的相对顺序保持不变。

### 示例

**示例 1**  
输入: `nums = [1,2,3,4,5], target = 9`  
输出: `3`  
解释: 和为 9 的子序列共有 3 种: `[4,5]`、`[1,3,5]`、`[2,3,4]`。最长的子序列是 `[1,3,5]` 与 `[2,3,4]`，长度为 **3**。

**示例 2**  
输入: `nums = [4,1,3,2,1,5], target = 7`  
输出: `4`  
解释: 和为 7 的子序列共有 5 种: `[4,3]`、`[4,1,2]`、`[4,2,1]`、`[1,1,5]`、`[1,3,2,1]`。最长的子序列是 `[1,3,2,1]`，长度为 **4**。

**示例 3**  
输入: `nums = [1,1,5,4,5], target = 3`  
输出: `-1`  
解释: 可以证明 **nums** 中不存在和为 3 的子序列。

### 约束条件

- `1 <= nums.length <= 1000`
- `1 <= nums[i] <= 1000`
- `1 <= target <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把数组里每一个元素**保留**或**删除**，把所有可能的组合都枚举出来，检查它们的和是否等于 `target`，如果相等就记录下它的长度，最后取最长的那个。

- **用到的数据结构**：  
  - **列表**（list）保存当前正在尝试的子序列。  
  - **递归栈**（可以把它想象成厨房里一层层的盘子，每次往里面放一个新盘子代表我们把一个元素加入子序列，回溯时再把盘子拿出来）。  
  - **全局变量**记录目前找到的最长长度。

- **为什么正确**：  
  只要把「保留」和「删除」这两种选择都尝试一次，所有可能的子序列就一定会被遍历到。只要在遍历过程中把满足 `sum == target` 的子序列的长度与当前答案比较，就一定能得到最长的那一个。

- **时间/空间复杂度**（大白话版）：  
  - 对于长度为 `n` 的数组，每个位置有「保留」或「删除」两种决定，一共会产生 `2ⁿ` 种组合。想象一下如果 `n=20`，组合数已经是 `1,048,576`，`n=30` 就已经是 **十亿** 级别，根本跑不完。  
  - 所以时间复杂度是 **O(2ⁿ)**，也就是说随着数组变长，耗时会呈指数级增长，几乎不可能在 1 秒内算完。  
  - 递归过程中最多会保存 `n` 层调用栈，空间复杂度是 **O(n)**。

#### 代码（Python）

```python
def longest_subseq_bruteforce(nums, target):
    """
    暴力枚举所有子序列，返回最长的满足和为 target 的子序列长度。
    如果不存在返回 -1。
    """
    n = len(nums)
    best = -1                     # 记录当前找到的最长长度

    def dfs(idx, cur_sum, cur_len):
        """
        深度优先搜索（递归）:
        idx      - 正在考虑的下标
        cur_sum  - 已经选的元素之和
        cur_len  - 已经选的元素个数
        """
        nonlocal best
        # 已经遍历完所有元素
        if idx == n:
            if cur_sum == target:                 # 和正好等于 target
                best = max(best, cur_len)         # 更新最长长度
            return

        # ① 选当前元素
        dfs(idx + 1, cur_sum + nums[idx], cur_len + 1)

        # ② 不选当前元素
        dfs(idx + 1, cur_sum, cur_len)

    dfs(0, 0, 0)
    return best
```

#### 复杂度

- **时间复杂度**：`O(2ⁿ)`  
  解释：每个元素都有「选」或「不选」两条路，全部遍历下来就是指数级的组合数。

- **空间复杂度**：`O(n)`  
  解释：递归深度最多等于数组长度 `n`，栈空间随之增长。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到**瓶颈**在于「枚举所有子序列」——这一步把时间推到了指数级。  
观察题目条件：

- `nums.length ≤ 1000`，`target ≤ 1000`，两者都不大。  
- 所求的是「长度」的最大值，而不是「具体的子序列」。  

这提示我们可以把**和**作为状态，用**动态规划（DP）**来逐步构造答案。  

---

**核心想法**：  
设 `dp[j]` 为**已经遍历过的前缀**（即若干个元素）中，**和恰好等于 `j` 的子序列的最大长度**。如果没有办法凑出 `j`，我们记 `dp[j] = -inf`（负无穷，表示不可达）。

遍历数组时，对每个元素 `num`，我们有两种选择：

1. **不使用** `num` → `dp[j]` 保持不变。  
2. **使用** `num` → 如果之前可以凑出 `j - num`，则现在可以凑出 `j`，长度加 1。  
   更新式子：`dp[j] = max(dp[j], dp[j - num] + 1)`。

**为什么要倒序遍历 `j`（从 target 到 num）**？  
因为我们在同一次循环里不希望把已经“本轮使用”过的 `num` 再次算进来。倒序遍历相当于先使用旧的 `dp` 值（不含本轮的 `num`），再把结果写回，保证每个元素只能被取一次——这正好对应**子序列**的定义（只能使用一次且保持顺序）。

**初始化**：  
- `dp[0] = 0`（和为 0 的空子序列长度是 0）。  
- 其它 `dp[j] = -inf`（不可达）。

遍历结束后，`dp[target]` 就是答案。如果仍是 `-inf`，说明不存在满足条件的子序列，返回 `-1`。

**空间优化**：  
上面的公式只依赖上一轮的 `dp`，所以只需要一个一维数组 `dp[0..target]`，空间从 `O(n·target)` 降到 `O(target)`。

#### 代码（Python）

```python
def longest_subseq_dp(nums, target):
    """
    动态规划求最长子序列长度，使其和等于 target。
    如果不存在返回 -1。
    """
    INF_NEG = -10**9                 # 代表「不可达」的负无穷
    dp = [INF_NEG] * (target + 1)    # dp[j] = 最大长度，使和为 j
    dp[0] = 0                        # 空子序列，和为 0，长度 0

    for num in nums:                 # 逐个处理数组中的元素
        # 必须倒序遍历，防止同一个元素在同一次循环中被使用多次
        for s in range(target, num - 1, -1):
            if dp[s - num] != INF_NEG:          # 只有之前能凑出 s-num 才有意义
                dp[s] = max(dp[s], dp[s - num] + 1)

    return dp[target] if dp[target] != INF_NEG else -1
```

#### 复杂度

- **时间复杂度**：`O(n · target)`  
  解释：外层遍历 `n`（最多 1000）个元素，内层遍历 `target`（最多 1000）个可能的和，总共大约一百万次操作，完全可以在毫秒级完成。相比暴力的指数级，这就是“快了好几百倍”。

- **空间复杂度**：`O(target)`  
  解释：只用了一个长度为 `target+1` 的一维数组，大约 1001 个整数，几乎可以忽略不计。

---

## 心得

- **核心技巧**：**背包型动态规划**（把「和」当作背包容量，把「长度」当作价值），在「子序列」而非「子数组」的情况下，仍然可以使用同样的思路，只要注意遍历顺序保证元素只能使用一次。
- **适用题型**（类似思路）：
  1. **“恰好装满背包”**：`Combination Sum IV`（求组合数），或 “是否可以恰好凑出目标和” (`Target Sum`)。  
  2. **“在限定和的情况下，最大化/最小化其他属性”**：如 “背包容量固定，价值最大化” (`0/1 Knapsack`)。  
  3. **“最长/最短子序列满足某种和的限制”**：如 “最长子序列和不超过 K”。
- **一句话总结**：  
  **把“和”当作状态，用 DP 记录每个和对应的最长长度，倒序遍历确保每个元素只用一次。**

---

## 反思

- **第一反应**：看到「最长」+「子序列」+「和等于 target」立刻想到「枚举」或「回溯」——这是最自然的暴力思路。  
- **最容易踩的坑**：  
  1. **忘记倒序遍历**，导致同一个元素被重复计入，得到的长度会不符合子序列的定义。  
  2. **初始化错误**：把 `dp[0]` 设成 `1`（长度 1）会把空子序列算成有元素，导致结果偏大。  
  3. **没有处理不可达情况**，直接返回 `dp[target]` 会得到负数，需要显式转成 `-1`。  
- **下次类似题的第一步**：  
  **先判断约束是否足够小（如 target ≤ 1000），如果是，就考虑用「和」作为 DP 状态；否则再思考其他技巧（如哈希表、双指针）。**