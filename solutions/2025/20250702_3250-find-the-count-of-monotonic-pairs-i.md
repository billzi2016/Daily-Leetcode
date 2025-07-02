# #3250. **单调对计数 I** / Find the Count of Monotonic Pairs I

> 难度：困难 · 标签：Array、Math、Dynamic Programming、Combinatorics、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/find-the-count-of-monotonic-pairs-i/)

---

## 题目（英文原版）

**Description**

You are given an array of positive integers nums of length n.
We call a pair of non-negative integer arrays (arr1, arr2) monotonic if:
Return the count of monotonic pairs.
Since the answer may be very large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: nums = [2,3,2]
Output: 4
Explanation:
The good pairs are:
```

**Example 2:**

```
Input: nums = [5,5,5,5]
Output: 126
```

**Constraints**

- 1 <= n == nums.length <= 2000
- 1 <= nums[i] <= 50

---

## 题目（中文翻译）

给定一个长度为 `n` 的正整数数组 `nums`。

我们称一对非负整数数组 `(arr1, arr2)` 为 **单调的**，如果：

返回单调对的数量。由于答案可能非常大，请返回答案对 `10^9 + 7` 取模后的结果。

---

### 示例

#### 示例 1
> **输入**: `nums = [2,3,2]`  
> **输出**: `4`  
> **解释**: 满足条件的配对有：

#### 示例 2
> **输入**: `nums = [5,5,5,5]`  
> **输出**: `126`

---

### 约束条件
- `1 <= n == nums.length <= 2000`
- `1 <= nums[i] <= 50`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

题目要求我们把每个 `nums[i]` 拆成两部分  

```
arr1[i] + arr2[i] = nums[i] ,   arr1[i] ≥ 0 , arr2[i] ≥ 0
```  

并且 **arr1** 与 **arr2** 必须都是 **单调不下降**（即前一个元素不大于后一个元素）。  
最直接的想法是：把每个位置的所有合法拆分枚举出来，然后检查整个序列是否满足单调性，符合的就计数。  

> **类比**：想象我们在超市挑选两盒糖果，盒子 A 里放 `arr1[i]` 粒，盒子 B 里放 `arr2[i]` 粒，总数必须恰好等于 `nums[i]`。我们把每一种可能的分配方式写下来，再挑出 “两盒糖果的数量随天数不减少” 的方案。

**为什么会对**：  
- 对每个位置 `i`，我们列举了 **所有** 可能的 `(arr1[i], arr2[i])`。  
- 只要把这些位置的选择连起来，就能得到 **所有** 满足题目条件的 `(arr1, arr2)`。  
- 再逐一检查单调性，恰好过滤掉不合法的组合。

**复杂度**（大白话版）：  
- 每个 `i` 有 `nums[i] + 1` 种拆法（`0 … nums[i]`）。  
- 如果把所有位置的拆法相乘，就得到搜索空间的大小。最坏情况下 `nums[i] = 50, n = 2000`，于是搜索空间是 `51^2000`——比宇宙中原子数还要大！  
- 所以暴力的 **时间复杂度** 是指数级 `O(∏(nums[i]+1))`，**空间复杂度** 只需要递归栈 `O(n)`（但实际根本跑不完）。

下面给出可以运行的暴力代码，仅作概念展示，**不适用于大输入**。

#### 代码（Python）

```python
from typing import List

MOD = 10**9 + 7

def count_monotonic_pairs_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    ans = 0

    # 用深度优先搜索枚举每一位的拆分
    def dfs(i: int, prev_a: int, prev_b: int) -> None:
        """i : 当前处理的下标（0‑based）
           prev_a, prev_b : 前一个位置的 arr1、arr2 值，用来判断单调性
        """
        nonlocal ans
        if i == n:                     # 所有位置都已经填完
            ans = (ans + 1) % MOD
            return

        # 枚举当前位 arr1 的可能取值 s
        for s in range(nums[i] + 1):   # s = arr1[i]
            t = nums[i] - s            # t = arr2[i] 必须非负
            # 检查单调性：arr1 不降且 arr2 不降
            if s >= prev_a and t >= prev_b:
                dfs(i + 1, s, t)

    # 第 0 位没有前驱，先随意取一个合法拆法
    dfs(0, 0, 0)      # 这里把 prev_a、prev_b 设为 0，等价于把它们视作 “-∞”
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(∏ (nums[i] + 1))`（指数级），实际只能在 `n ≤ 10`、`nums[i]` 很小的情况下跑通。  
- **空间复杂度**：`O(n)`（递归栈深度），因为我们只保存当前递归路径上的信息。

---

### 2. 最优解  

#### 思路  

暴力解的 **瓶颈** 在于：我们每次都要遍历所有可能的前一个取值 `t`，导致指数级搜索。  
观察下面的约束可以帮助我们把搜索空间压缩到 **多项式**：

1. 对第 `i` 位，若我们已经决定 `arr1[i] = s`，则  
   `arr2[i] = nums[i] - s`（因为两者和必须等于 `nums[i]`）。  
   这一步把二维选择压成了一维：只需要关心 `s`（即 `arr1[i]`）即可。

2. 单调性要求  
   - `arr1[i-1] ≤ arr1[i]`   →   `t ≤ s`  
   - `arr2[i-1] ≤ arr2[i]`   →   `nums[i-1] - t ≤ nums[i] - s`  

   把第二个不等式整理一下：  

   ```
   nums[i-1] - t ≤ nums[i] - s
   ⇒ t ≥ nums[i-1] - (nums[i] - s)
   ⇒ t ≥ s + nums[i-1] - nums[i]
   ```

   所以合法的前一个 `t` 必须同时满足  

   ```
   max(0, s + nums[i-1] - nums[i]) ≤ t ≤ s
   ```

   （下界还要保证 `t ≥ 0`，因为 `arr1` 只能是非负整数）

3. 动态规划（DP）  
   定义  

   ```
   dp[i][s] = 前 i 个位置（0…i-1）已经填好，且 arr1[i-1] = s 时的合法方案数
   ```

   - 初始化 `i = 1`（只考虑第 0 位）：只要 `0 ≤ s ≤ nums[0]`，`dp[1][s] = 1`。  
   - 转移公式（i ≥ 2）：

   ```
   dp[i][s] = Σ dp[i-1][t]   （t 满足 max(0, s+nums[i-2]-nums[i-1]) ≤ t ≤ s）
   ```

   直接遍历所有 `t` 会导致 `O(maxVal^2)`，其中 `maxVal = max(nums) ≤ 50`。  
   但是 `maxVal` 很小，我们仍然可以 **利用前缀和** 把求和降到 `O(1)`：

   - 设 `pref[t] = Σ_{k=0}^{t} dp[i-1][k]`（前缀和）。
   - 那么区间求和 `Σ_{t = L}^{R} dp[i-1][t] = pref[R] - pref[L-1]`（`L` 可能为 0，需要特判）。

   这样每一次 `dp[i][s]` 的计算只需要 `O(1)`，整体时间 `O(n * maxVal)`。

4. 最终答案  

   所有长度为 `n` 的合法序列对应 `dp[n][s]`（`s` 为最后一个 `arr1` 的取值），所以答案是  

   ```
   ans = Σ_{s=0}^{nums[n-1]} dp[n][s]   (mod MOD)
   ```

**为什么快**：  
- 把二维枚举压成了一维（只决定 `arr1[i]`）。  
- 用前缀和把每一步的 “从前一个状态的合法区间求和” 从 `O(maxVal)` 降到 `O(1)`。  
- `maxVal ≤ 50`，`n ≤ 2000`，所以最多只做 `2000 * 51 ≈ 1e5` 次加法，轻松跑完。

#### 代码（Python）

```python
from typing import List

MOD = 10**9 + 7

def count_monotonic_pairs(nums: List[int]) -> int:
    """
    返回满足
        arr1[i] + arr2[i] = nums[i]  (arr1, arr2 为非负整数数组)
        arr1 单调不下降，arr2 单调不下降
    的 (arr1, arr2) 对数，模 1e9+7。
    """
    n = len(nums)
    max_val = max(nums)               # ≤ 50

    # dp[s] 表示当前处理到第 i 位时，arr1[i-1] = s 的方案数
    dp = [0] * (max_val + 1)

    # ---------- 初始化第 0 位 ----------
    for s in range(nums[0] + 1):      # arr1[0] 可以是 0 … nums[0]
        dp[s] = 1                     # arr2[0] = nums[0] - s 自动满足非负
    # ---------- 逐位递推 ----------
    for i in range(1, n):
        # 前缀和数组 pref[t] = Σ_{k=0}^{t} dp[k] (mod)
        pref = [0] * (max_val + 1)
        cur = 0
        for t in range(max_val + 1):
            cur = (cur + dp[t]) % MOD
            pref[t] = cur

        new_dp = [0] * (max_val + 1)

        for s in range(nums[i] + 1):          # arr1[i] 只能取到 nums[i]
            # 计算合法的前一个 arr1 值 t 的取值区间
            low = s + nums[i-1] - nums[i]     # 根据不等式推导得到的下界
            if low < 0:
                low = 0                       # t 必须非负
            high = s                         # t ≤ s

            # 区间可能为空（low > high），此时 new_dp[s] 仍为 0
            if low <= high:
                # 区间和 = pref[high] - pref[low-1]
                total = pref[high]
                if low > 0:
                    total = (total - pref[low - 1]) % MOD
                new_dp[s] = total

        dp = new_dp        # 进入下一轮

    # ---------- 汇总答案 ----------
    ans = sum(dp[s] for s in range(nums[-1] + 1)) % MOD
    return ans
```

**代码要点注释**：

- `dp` 只保留上一层的状态，空间从 `O(n*maxVal)` 降到 `O(maxVal)`。  
- `pref` 每轮重新计算，用来快速得到区间和。  
- `low = s + nums[i-1] - nums[i]` 是 **从单调性推导** 的核心公式。  
- `low` 可能为负，必须截到 `0`（因为 `arr1` 不能小于 0）。  
- 取模 `MOD` 保证结果不会溢出。

#### 复杂度  

- **时间复杂度**：`O(n * maxVal)`，这里 `maxVal ≤ 50`，所以实际约 `1e5` 次操作。  
  > 与暴力的指数级 `O(∏(nums[i]+1))` 相比，几乎是天壤之别。  

- **空间复杂度**：`O(maxVal)`，仅存两行 DP 和前缀和数组。  

---

## 心得  

- **核心技巧**：把 “两个数组的和固定” 转化为只决定一个数组的取值，再用 **单调性** 推导出前一个取值的合法区间，最后用 **前缀和** 优化区间求和。  
- **适用场景**：  
  1. “拆分数组并保持两条单调序列” 类问题（如 *Monotonic Pairs II*、*Split Array Into Two Monotonic Sequences*）。  
  2. 需要在 **状态转移中加入区间约束** 的 DP（如 “限制前后差值” 的序列计数）。  
- **一句话总结解题钥匙**：**把二元约束压成单变量，利用单调性得到一个连续区间，再用前缀和把区间求和降到 O(1)。**

---

## 反思  

- **第一反应**：看到 “arr1[i] + arr2[i] = nums[i]”，立刻想到枚举所有可能的拆分。  
- **最容易踩的坑**：  
  - 忘记检查 `arr2[i]` 的非负性（即 `s` 必须 ≤ `nums[i]`）。  
  - 计算区间下界时漏掉 `+ nums[i-1] - nums[i]` 的符号，导致区间错误。  
  - 前缀和取模时负数未加 `MOD`，在 Python 中会得到负数结果。  
- **下次思路**：遇到 “两个序列的和固定且都有单调性” 时，先 **固定其中一个序列**，把约束写成 **前后两个变量的区间关系**，再考虑 **前缀和/差分** 来加速 DP。这样可以立刻从指数级搜索跳到线性 DP。