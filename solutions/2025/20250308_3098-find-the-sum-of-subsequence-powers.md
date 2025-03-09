# #3098. 子序列幂之和 / Find the Sum of Subsequence Powers

> 难度：困难 · 标签：Array、Dynamic Programming、Sorting · [LeetCode 链接](https://leetcode.com/problems/find-the-sum-of-subsequence-powers/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums of length n, and a positive integer k.
The power of a subsequence is defined as the minimum absolute difference between any two elements in the subsequence.
Return the sum of powers of all subsequences of nums which have length equal to k.
Since the answer may be large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,4], k = 3
Output: 4
Explanation:
There are 4 subsequences in nums which have length 3: [1,2,3] , [1,3,4] , [1,2,4] , and [2,3,4] . The sum of powers is |2 - 3| + |3 - 4| + |2 - 1| + |3 - 4| = 4 .
```

**Example 2:**

```
Input: nums = [2,2], k = 2
Output: 0
Explanation:
The only subsequence in nums which has length 2 is [2,2] . The sum of powers is |2 - 2| = 0 .
```

**Example 3:**

```
Input: nums = [4,3,-1], k = 2
Output: 10
Explanation:
There are 3 subsequences in nums which have length 2: [4,3] , [4,-1] , and [3,-1] . The sum of powers is |4 - 3| + |4 - (-1)| + |3 - (-1)| = 10 .
```

**Constraints**

- 2 <= n == nums.length <= 50
- -108 <= nums[i] <= 108
- 2 <= k <= n

---

## 题目（中文翻译）

给定一个长度为 `n` 的 **整数数组 (integer array)** `nums`，以及一个正整数 `k`。  
**子序列 (subsequence)** 的 **幂** 定义为该子序列中任意两元素之间的 **最小绝对差 (minimum absolute difference)**。  
返回 `nums` 中所有长度恰好为 `k` 的子序列的幂之和。  
由于答案可能很大，请返回 **取模 (modulo)** `10^9 + 7` 的结果。

## 示例

### 示例 1
**输入**  
`nums = [1,2,3,4], k = 3`  

**输出**  
`4`  

**解释**  
`nums` 中长度为 3 的子序列共有 4 个：`[1,2,3]`、`[1,3,4]`、`[1,2,4]`、`[2,3,4]`。  
它们的幂分别为 `|2 - 3|`、`|3 - 4|`、`|2 - 1|`、`|3 - 4|`，总和为 `4`。

### 示例 2
**输入**  
`nums = [2,2], k = 2`  

**输出**  
`0`  

**解释**  
唯一长度为 2 的子序列是 `[2,2]`，其幂为 `|2 - 2| = 0`。

### 示例 3
**输入**  
`nums = [4,3,-1], k = 2`  

**输出**  
`10`  

**解释**  
长度为 2 的子序列有 3 个：`[4,3]`、`[4,-1]`、`[3,-1]`。  
它们的幂分别为 `|4 - 3|`、`|4 - (-1)|`、`|3 - (-1)|`，总和为 `10`。

## 约束条件
- `2 <= n == nums.length <= 50`
- `-10^8 <= nums[i] <= 10^8`
- `2 <= k <= n`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有** 长度为 `k` 的子序列都枚举出来，  
对每个子序列计算它的 “力量” —— 即子序列中任意两数的绝对差的最小值，  
然后把这些最小值加起来。

- **数据结构**：  
  - `itertools.combinations` 可以一次性把数组中所有不重复的 `k` 元组挑出来，类似于在超市里一次性挑出所有可能的 `k` 件商品的组合。  
  - 计算子序列内部最小差值时，只需要一个双层循环遍历子序列内部的每一对元素，类似于在一张桌子上把所有水果两两比较重量。

- **为什么正确**：  
  只要把 **所有** 合法的子序列都算进来，且每个子序列的力量都算对了，最后求和自然就是题目要的答案。

- **复杂度**：  
  - 子序列的数量是组合数 `C(n, k)`（从 `n` 个元素里挑 `k` 个），这在数学上记作 “n 选 k”。  
  - 对每个子序列我们要检查它内部的所有两两差值，最多 `k·(k‑1)/2` 次比较。  
  - 所以总的时间是 `O( C(n,k) · k² )`。  
    - 当 `n = 50, k = 25` 时，`C(50,25) ≈ 1.26·10¹⁴`，根本不可能在电脑里跑完。  
  - 额外空间只用来保存当前枚举的子序列，`O(k)`，几乎可以忽略。

#### 代码（Python）

```python
import itertools

MOD = 10 ** 9 + 7

def sum_of_powers_bruteforce(nums, k):
    ans = 0
    # 1. 把所有长度为 k 的子序列枚举出来
    for comb in itertools.combinations(nums, k):
        # 2. 计算当前子序列的最小绝对差
        min_diff = float('inf')
        # 两层循环遍历子序列内部的每一对元素
        for i in range(k):
            for j in range(i + 1, k):
                diff = abs(comb[i] - comb[j])
                if diff < min_diff:
                    min_diff = diff
        # 3. 把最小差值加到答案里（取模防溢出）
        ans = (ans + min_diff) % MOD
    return ans
```

#### 复杂度  

- **时间复杂度**：`O( C(n, k) · k² )`  
  - “组合数 `C(n,k)`” 代表要枚举多少个子序列，`k²` 是每个子序列内部比较的次数。  
  - 对普通人来说，`C(50,25)` 已经是 **一百多万亿**，所以这段代码只能用于 **非常小** 的测试数据（比如 `n ≤ 15`）。  

- **空间复杂度**：`O(k)`  
  - 只保存当前枚举的子序列，最多 `k` 个整数。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **枚举所有子序列**。  
我们需要一种只 **计数** 而不真正列举子序列的方法。  

观察：

1. **先把数组排序**  
   排序后，子序列在原数组中的相对顺序不变，且子序列内部的最小绝对差一定是相邻两个元素的差（因为相邻的差最小）。  
   > 类比：把一串珠子按大小排好顺序后，最靠近的两颗珠子的距离一定是最小的。

2. **把“最小差”转化为“相邻差的阈值”**  
   对于一个固定的阈值 `d`（可能是 0、1、5…），我们可以问：  
   “有多少个长度为 `k` 的子序列，使得 **所有相邻元素的差** 都 **不小于** `d`？”  
   记这个计数为 `f(d)`。  

3. **利用包含‑排除**  
   - 如果 `d1 < d2`，显然 `f(d1) ≥ f(d2)`（阈值小，要求更宽松，子序列更多）。  
   - 对于恰好 **最小差等于** `d` 的子序列数量 = `f(d) - f(next_larger_d)`，其中 `next_larger_d` 是大于 `d` 的最小的那一个差值。  

4. **枚举所有可能的差值**  
   - 所有可能的相邻差只来自数组中任意两数的差，最多 `n·(n‑1)/2 ≤ 1225` 个。  
   - 把这些差值去重、排序（升序），得到差值列表 `diffs`。  

5. **动态规划计算 `f(d)`**  
   对于固定的阈值 `d`，我们在排好序的数组 `a`（长度 `n`）上做 DP：  

   - `dp[t][i]` = 选出 `t` 个元素，且第 `t` 个（最后一个）是 `a[i]`，**并且相邻差 ≥ d** 的方案数。  

   - 初始化：`dp[1][i] = 1`（单独一个元素本身就满足要求）。  

   - 转移：  
     ```
     dp[t][i] = Σ dp[t-1][j]   (j < i 且 a[i] - a[j] ≥ d)
     ```
     也就是说，若想把 `a[i]` 加到已经选好的 `t-1` 个元素的序列末尾，只要前一个元素 `a[j]` 与 `a[i]` 的差不小于 `d`，就可以。

   - 最终 `f(d) = Σ dp[k][i]`（把所有以不同结尾的合法序列加起来）。  

   这一步的时间复杂度是 `O(k · n²)`，因为我们要遍历所有 `t (≤k)`、所有 `i`，并在内部遍历所有合法的 `j`。  
   对于 `n ≤ 50, k ≤ 50`，这只要几千次操作，完全可以接受。

6. **把所有差值的贡献加起来**  

   按 **降序**（从大到小）遍历 `diffs`，  
   - 先算出当前阈值的 `f(d)`；  
   - 用 `cnt_exact = f(d) - f(prev_d)`（`prev_d` 是上一次遍历的、更大的阈值，对应的 `f` 已经算好）得到 **最小差恰好等于 `d` 的子序列数**；  
   - 累加 `ans += d * cnt_exact`（记得取模）。  

   当遍历完所有差值后，答案就得到啦！

#### 代码（Python）

```python
from bisect import bisect_left
MOD = 10 ** 9 + 7

def sum_of_powers(nums, k):
    n = len(nums)
    a = sorted(nums)                     # 1. 先排序
    # 2. 收集所有可能的差值（包括 0）
    diffs = {0}
    for i in range(n):
        for j in range(i + 1, n):
            diffs.add(a[j] - a[i])
    diffs = sorted(diffs)                # 升序

    # 3. 辅助函数：给定阈值 d，返回 f(d) —— 长度为 k、相邻差 ≥ d 的子序列数量
    def count_at_least(d):
        # dp[t][i] 只需要保留前一层 t-1，使用一维数组滚动即可
        dp_prev = [1] * n                # t = 1 时 dp[1][i] = 1
        for t in range(2, k + 1):
            dp_cur = [0] * n
            # 对每个 i，累计所有满足 a[i] - a[j] >= d 的 dp_prev[j]
            # 这里直接双层循环，n ≤ 50，足够快
            for i in range(n):
                s = 0
                for j in range(i):
                    if a[i] - a[j] >= d:
                        s += dp_prev[j]
                dp_cur[i] = s % MOD
            dp_prev = dp_cur
        # 最后一次循环得到的是 dp[k][*]
        return sum(dp_prev) % MOD

    # 4. 按差值从大到小累计贡献
    ans = 0
    prev_f = 0               # 对应更大的阈值的 f，初始为 0（因为 d 超过最大差时没有合法序列）
    for d in reversed(diffs):          # 降序遍历
        cur_f = count_at_least(d)      # f(d)
        cnt_exact = (cur_f - prev_f) % MOD   # 最小差恰好等于 d 的序列数
        ans = (ans + d * cnt_exact) % MOD
        prev_f = cur_f                  # 为下一次（更小的 d）准备

    return ans
```

> **代码要点注释**  
> - `sorted(nums)` 把数组排成从小到大的顺序，后面所有差值都是非负的，便于比较。  
> - `diffs` 用 `set` 去重，确保每个可能的差值只算一次。  
> - `count_at_least(d)` 中的双层循环 `i, j` 正是 “前一个元素与当前元素的差 ≥ d” 的判断。  
> - 采用滚动数组 (`dp_prev` → `dp_cur`) 省掉了 `O(k·n²)` 的额外空间，只用了 `O(n)`。  

#### 复杂度  

- **时间复杂度**：  
  - 产生所有差值：`O(n²)`（最多 1225 次）。  
  - 对每个差值 `d` 计算 `f(d)`：`O(k·n²)`。  
  - 差值个数 ≤ `n·(n‑1)/2 + 1`，记作 `m`。  
  - 总体时间 = `O( m · k · n² )` ≤ `O( (n²)·k·n² ) = O(k·n⁴)`。  
    - 对于本题的上限 `n = 50, k = 50`，约 `50·50⁴ ≈ 3·10⁶` 次基本运算，运行毫秒级。  
  - 与暴力解的 `C(n,k)·k²`（天文数字）相比，**相差几个数量级**，可以轻松通过所有测试。

- **空间复杂度**：`O(n)`  
  - DP 只保留上一层的 `n` 个计数，另外还有排序数组和差值列表，都是 `O(n)` 级别。  

---

## 心得  

- **核心技巧**：  
  - 将 “最小相邻差” 转化为 “相邻差的下界”，利用 **阈值计数 + 包含‑排除** 的思想。  
  - 对固定阈值使用 **动态规划** 计数长度为 `k`、相邻差 ≥ `d` 的子序列。  

- **适用的题型**（类似思路）  
  1. **子序列最小/最大差值之和**（如 LeetCode 1818 “Minimum Difference Between Target and Chosen Elements”）  
  2. **子序列满足相邻差 ≥ 给定值的计数**（如 “Number of Subsequence With Bounded Maximum Difference”）  
  3. **利用阈值 DP 计数的组合问题**（如 “Count the Number of Beautiful Subarrays”）  

- **一句话总结解题钥匙**：  
  “把‘最小差等于 d’拆成‘所有差 ≥ d’减去‘所有差 ≥ 下一更大值’，再用 DP 按阈值计数”。  

---

## 反思  

- **第一反应**：  
  “直接枚举所有子序列，逐个求最小差”。这在脑中是最自然的做法，却忽略了组合数的爆炸性。  

- **最容易踩的坑**  
  1. **忘记对数组先排序**，导致相邻差不一定是子序列的最小差。  
  2. **遗漏 0 差值**（当数组中有相同元素时），如果不把 0 加进 `diffs`，会把这类子序列的贡献算漏。  
  3. **模运算的负数**：`cnt_exact = (cur_f - prev_f) % MOD` 必须加取模，防止出现负数导致答案错误。  
  4. **边界条件**：`k = 2` 时 DP 只跑一次循环，仍然要保证代码能正常工作。  

- **下次遇到同类题的第一步**：  
  “先把问题抽象为‘满足某个阈值的子序列计数’，列出所有可能的阈值，再用 DP 或组合数学求每个阈值下的计数”。这样可以把“最小/最大”这类要求转化为“≥ / ≤”的计数，往往更容易构造高效算法。