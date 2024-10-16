# #2902. 有界和的子多重集计数 / Count of Sub-Multisets With Bounded Sum

> 难度：困难 · 标签：Array、Hash Table、Dynamic Programming、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/count-of-sub-multisets-with-bounded-sum/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array nums of non-negative integers, and two integers l and r.
Return the count of sub-multisets within nums where the sum of elements in each subset falls within the inclusive range of [l, r].
Since the answer may be large, return it modulo 109 + 7.
A sub-multiset is an unordered collection of elements of the array in which a given value x can occur 0, 1, ..., occ[x] times, where occ[x] is the number of occurrences of x in the array.
Note that:

**Examples**

**Example 1:**

```
Input: nums = [1,2,2,3], l = 6, r = 6
Output: 1
Explanation: The only subset of nums that has a sum of 6 is {1, 2, 3}.
```

**Example 2:**

```
Input: nums = [2,1,4,2,7], l = 1, r = 5
Output: 7
Explanation: The subsets of nums that have a sum within the range [1, 5] are {1}, {2}, {4}, {2, 2}, {1, 2}, {1, 4}, and {1, 2, 2}.
```

**Example 3:**

```
Input: nums = [1,2,1,3,5,2], l = 3, r = 5
Output: 9
Explanation: The subsets of nums that have a sum within the range [3, 5] are {3}, {5}, {1, 2}, {1, 3}, {2, 2}, {2, 3}, {1, 1, 2}, {1, 1, 3}, and {1, 2, 2}.
```

**Constraints**

- 1 <= nums.length <= 2 * 104
- 0 <= nums[i] <= 2 * 104
- Sum of nums does not exceed 2 * 104.
- 0 <= l <= r <= 2 * 104

---

## 题目（中文翻译）

**题目描述**  
给定一个下标从 0 开始的整数数组 `nums`（元素为非负整数），以及两个整数 `l` 和 `r`。  
返回 `nums` 中所有子多重集（sub-multiset）的个数，使得每个子多重集的元素之和位于闭区间 `[l, r]` 内。  
由于答案可能很大，请返回答案对 `10^9 + 7` 取模后的结果。  

子多重集是指数组中元素的无序集合，其中某个取值 `x` 可以出现 `0, 1, …, occ[x]` 次，`occ[x]` 为 `x` 在数组中出现的次数。

**示例**  

> 示例 1  
> 输入: `nums = [1,2,2,3]`, `l = 6`, `r = 6`  
> 输出: `1`  
> 解释: 唯一满足条件的子多重集是 `{1, 2, 3}`，其和为 6。  

> 示例 2  
> 输入: `nums = [2,1,4,2,7]`, `l = 1`, `r = 5`  
> 输出: `7`  
> 解释: 和落在区间 `[1, 5]` 的子多重集有 `{1}`, `{2}`, `{4}`, `{2, 2}`, `{1, 2}`, `{1, 4}`, `{1, 2, 2}`。  

> 示例 3  
> 输入: `nums = [1,2,1,3,5,2]`, `l = 3`, `r = 5`  
> 输出: `9`  
> 解释: 和落在区间 `[3, 5]` 的子多重集有 `{3}`, `{5}`, `{1, 2}`, `{1, 3}`, `{2, 2}`, `{2, 3}`, `{1, 1, 2}`, `{1, 1, 3}`, `{1, 2, 2}`。  

**约束条件**  
- `1 <= nums.length <= 2 * 10^4`  
- `0 <= nums[i] <= 2 * 10^4`  
- `nums` 中所有元素之和不超过 `2 * 10^4`  
- `0 <= l <= r <= 2 * 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的子多集合都枚举出来**，然后统计它们的和是否落在 `[l, r]` 区间。

- **子多集合**：对数组中的每个不同数值 `x`，我们可以选 `0,1,…,occ[x]` 次（`occ[x]` 是 `x` 在数组里出现的次数）。  
  把它想象成**装满不同种类水果的篮子**，每种水果的数量上限就是它在原数组里的出现次数。我们要把篮子里装的水果种类和数量全部列举出来。

- **枚举方法**：先把数组中出现的不同数值收集起来（相当于“水果种类表”），然后对每种水果使用**回溯**（深度优先搜索）决定选多少个。递归结束时得到一种完整的子多集合，计算它的和，看是否在 `[l, r]`。

- **为什么一定对**：回溯遍历了**每一种合法的选法**，没有遗漏也没有重复（因为我们按种类顺序一次决定），所以答案一定完整。

- **时间/空间复杂度**  
  - 假设有 `m` 种不同的数值，每种数值的出现次数分别为 `c1, c2, …, cm`。  
  - 暴力需要遍历 `∏ (ci + 1)` 种组合，这个数在最坏情况下接近 `2^n`（`n = len(nums)`），所以 **时间复杂度是指数级**，记作 `O(2^n)`。  
  - 递归栈最多保存 `m` 层调用，额外空间 `O(m)`，在最坏情况下 `m ≤ n`，所以 **空间复杂度是 `O(n)`**。  

> **大白话**：如果把每一步的选择想象成“一次抉择”，要把所有抉择的枝干全部走完，就像在森林里把每条小路都走一遍，路数会随树的分叉指数增长，根本跑不完。

#### 代码（Python）

```python
from collections import Counter
from typing import List

MOD = 10 ** 9 + 7

def count_bruteforce(nums: List[int], l: int, r: int) -> int:
    # 统计每个数出现了多少次
    freq = Counter(nums)                 # 哈希表：键是数值，值是出现次数
    values = list(freq.items())          # [(数值, 次数), …]

    ans = 0

    def dfs(idx: int, cur_sum: int) -> None:
        """递归枚举第 idx 种数选多少个"""
        nonlocal ans
        if idx == len(values):           # 已经决定完所有种类
            if l <= cur_sum <= r:        # 检查和是否在区间内
                ans = (ans + 1) % MOD
            return

        val, cnt = values[idx]
        # 选 0~cnt 次当前数值
        for k in range(cnt + 1):
            dfs(idx + 1, cur_sum + k * val)

    dfs(0, 0)
    return ans
```

> 这段代码在 `nums` 长度稍大（>20）时就会失效，因为递归树太宽、太深，运行时间会爆炸。

#### 复杂度

- **时间复杂度**：`O(∏ (ci + 1))`，在最坏情况下约等于 `O(2^n)`，即指数级增长，几乎不可能在 2×10⁴ 的数据上跑完。  
- **空间复杂度**：`O(m)`（递归栈），最坏 `O(n)`，相对可接受。

---

### 2. 最优解

#### 思路  

暴力解慢的根本原因是**反复枚举相同的子问题**。我们注意到：

1. **只关心子多集合的“和”**，而不在乎具体选了哪些元素。  
2. **数组元素的总和 ≤ 20000**，这意味着所有可能的和都在 `0 … 20000` 之间，范围很小。  
3. 每种数值可以选若干次，这正好和 **“背包/找零”**（Coin Change）问题的**有界背包**相同。

于是我们可以用 **动态规划**（DP）来统计“能得到每个和的子多集合有多少种”。  
把 `dp[s]` 定义为：**使用已经处理过的数值，得到和为 `s` 的子多集合的数量**（包括空集合）。答案就是 `dp[l] + dp[l+1] + … + dp[r]`。

关键在于 **如何高效地把一种数值 `v`（出现 `cnt` 次）加入 DP**。  
直接的做法是：

```
for k = 0 .. cnt:
    ndp[s + k*v] += dp[s]
```

这相当于对每个 `s` 再遍历 `cnt+1` 次，时间是 `O(cnt * maxSum)`，在最坏情况下仍然太慢。

**优化思路——滑动窗口（Sliding Window）**  
把所有和按照 `v` 的余数分成若干“列”，每列的索引形如 `rem, rem+v, rem+2v, …`。在同一列里，转移公式只涉及 **相邻的 `cnt+1` 个旧状态**，于是可以用 **固定窗口的累计和** 来一次性算完整列，时间降到 `O(maxSum)`，而不是 `O(cnt*maxSum)`。

具体步骤：

```
dp[0] = 1
for each (value v, count cnt):
    ndp = [0] * (maxSum+1)
    for rem in 0 .. v-1:                     # 每个余数对应一列
        window = 0
        # 遍历该列的所有位置 s = rem + t*v
        for t, s in enumerate(range(rem, maxSum+1, v)):
            window += dp[s]                  # 把当前旧状态加入窗口
            if t > cnt:                      # 窗口太大，弹出最左边的旧状态
                window -= dp[s - (cnt+1)*v]
            ndp[s] = window % MOD            # 当前和 s 的新计数
    dp = ndp
```

- **为什么正确**：窗口里正好保存了 `dp[s] , dp[s‑v] , … , dp[s‑cnt*v]`（不越界的部分），这些正是构造新和 `s` 时可以使用的所有旧和。把它们相加得到 `ndp[s]`，恰好是“选 0~cnt 个 `v`”的所有可能。  
- **时间复杂度**：外层遍历不同数值的种类 `m ≤ 200`，内层每次遍历 `0 … maxSum`（`maxSum ≤ 20000`）一次，所以 **总时间 `O(m * maxSum) ≈ O(200 * 20000) = 4·10⁶`**，轻松跑完。  
- **空间复杂度**：只需要两个长度为 `maxSum+1` 的数组，**`O(maxSum)`**，即约 20001 个整数。

#### 代码（Python）

```python
from collections import Counter
from typing import List

MOD = 10 ** 9 + 7

def count_submultisets(nums: List[int], l: int, r: int) -> int:
    """
    使用有界背包（滑动窗口）统计所有子多集合的和的出现次数。
    返回满足 l <= sum <= r 的子多集合数量（模 1e9+7）。
    """
    # 1. 统计每个数值出现的次数
    freq = Counter(nums)                     # 哈希表：key=数值, value=出现次数
    max_sum = sum(nums)                      # 题目保证 ≤ 20000
    dp = [0] * (max_sum + 1)
    dp[0] = 1                                 # 空集合的和为 0，计数 1

    # 2. 对每种数值进行有界背包转移
    for v, cnt in freq.items():
        ndp = [0] * (max_sum + 1)             # 下一轮的 DP 表
        # 按余数把所有位置划分成若干列，每列之间相隔 v
        for rem in range(v):
            window = 0                        # 滑动窗口的累计和
            # 枚举该列的所有索引 s = rem + t*v
            for t, s in enumerate(range(rem, max_sum + 1, v)):
                # 把当前旧状态 dp[s] 加入窗口
                window = (window + dp[s]) % MOD
                # 如果窗口大小超过 cnt+1，弹出最左侧的旧状态
                if t > cnt:
                    left_idx = s - (cnt + 1) * v
                    window = (window - dp[left_idx]) % MOD
                # 当前和 s 的新计数就是窗口内所有可能的组合数
                ndp[s] = window
        dp = ndp                               # 更新为最新的 DP 表

    # 3. 累加区间 [l, r] 的计数即为答案
    ans = sum(dp[l:r + 1]) % MOD
    return ans
```

> 代码中的 **`% MOD`** 保证了每一步都不会出现整数溢出，同时符合题目“答案取模”的要求。

#### 复杂度

- **时间复杂度**：`O(m * maxSum)`，其中 `m` 为不同数值的种类数（≤ 200），`maxSum = sum(nums) ≤ 20000`。  
  实际上大约是 `4·10⁶` 次基本操作，远快于指数级的暴力解。  
- **空间复杂度**：`O(maxSum)`，只用两个长度为 `maxSum+1` 的一维数组（约 20001 个整数），非常节省内存。

> 与暴力解相比，时间从指数级降到了线性乘以种类数，**差距相当于把一座山搬到了平原**，在实际数据规模下可以轻松 AC。

---

## 心得

- **核心技巧**：**有界背包 + 滑动窗口**，把“每种数值最多使用 `cnt` 次”的约束转化为对同余类的窗口累计。  
- **适用的题型**  
  1. **计数型背包**：如 “统计和为 K 的子集个数（每个数只能用一次/多次）”。  
  2. **有限硬币找零**：给定若干硬币面值及每种硬币的最大使用次数，求凑成指定金额的方案数。  
  3. **受限组合计数**：比如 “在一串字符中，每个字符出现次数有限，统计满足长度或权值限制的子序列数量”。  

- **一句话总结解题钥匙**：  
  **把“可重复使用且次数受限”的选择，拆成同余类后用滑动窗口一次遍历完成 DP 转移。**

---

## 反思

- **第一反应**：看到“子多集合”和“出现次数限制”，立刻想到 **背包/找零** 的 DP，然而最初会尝试直接的三重循环（对每个数遍历每个和，再遍历每次使用次数），这仍然会超时。  
- **最容易踩的坑**  
  1. **忘记对空集合计数**：`dp[0]` 必须初始化为 1，否则所有结果都会少一条。  
  2. **窗口边界处理**：弹出旧状态时要保证索引不越界（使用 `t > cnt` 判断），否则会出现负索引错误。  
  3. **取模负数**：Python 的 `%` 对负数会得到正数，但在手动 `window -= dp[left]` 后最好再 `% MOD`，防止出现负数导致后续错误。  
- **下次类似题的第一步**：  
  **先检查“总和上限是否小”，如果是，则把问题转化为“在有限和范围内统计方案数”，并考虑使用**“**有界背包 + 滑动窗口**”** 或 **“前缀和/单调队列优化的 DP”** 来降低复杂度。