# #3351. 好子序列的和 / Sum of Good Subsequences

> 难度：困难 · 标签：Array、Hash Table、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/sum-of-good-subsequences/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums. A good subsequence is defined as a subsequence of nums where the absolute difference between any two consecutive elements in the subsequence is exactly 1.
Return the sum of all possible good subsequences of nums.
Since the answer may be very large, return it modulo 109 + 7.
Note that a subsequence of size 1 is considered good by definition.

**Examples**

**Example 1:**

```
Input: nums = [1,2,1]
Output: 14
Explanation:
```

**Example 2:**

```
Input: nums = [3,4,5]
Output: 40
Explanation:
```

**Constraints**

- 1 <= nums.length <= 105
- 0 <= nums[i] <= 105

---

## 题目（中文翻译）

给定一个整数数组 `nums`。若一个子序列（subsequence）中任意相邻两个元素的绝对差恰好等于 1，则称该子序列为**好子序列**（good subsequence）。

返回 `nums` 中所有可能的好子序列的元素和的总和。由于答案可能非常大，请返回 **模** `10^9 + 7` 后的结果。

> **提示**：长度为 1 的子序列默认被视为好子序列。

### 示例

**示例 1**

```
Input: nums = [1,2,1]
Output: 14
Explanation:
```

**示例 2**

```
Input: nums = [3,4,5]
Output: 40
Explanation:
```

### 约束条件

- `1 <= nums.length <= 10^5`
- `0 <= nums[i] <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的做法是 **枚举所有子序列**，检查它是否满足“相邻元素差恰好为 1”，如果满足就把该子序列里所有元素的和累加到答案中。  

- **枚举子序列**：把数组的每个元素看成 “要不要选”，于是可以用二进制的 0/1 组合来表示子序列。  
- **检查好序列**：遍历子序列内部，相邻两个数的绝对差是否为 1。  
- **累加贡献**：如果是好序列，就把子序列里所有数相加，再加到全局答案。

> **哈希表类比**：这里其实不需要哈希表，但如果把每一种子序列的“出现次数”记在一个字典里，它就像一本“查字典”，key 是子序列的具体取值，value 是出现次数。  

**为什么正确**：我们遍历了 **所有** 可能的子序列，凡是符合条件的都被计入，且没有遗漏或重复计数。

**时间/空间复杂度**  
- 子序列的总数是 2ⁿ（每个位置选或不选），所以时间复杂度是 **O(2ⁿ·n)**（每个子序列最多检查 n‑1 次相邻差）。  
- 只用了常数级别的额外空间（递归栈或临时数组），即 **O(n)**。

> **大白话**：  
> - “O(2ⁿ)” 就像把所有可能的选法都列出来，数量会在几秒钟内就炸掉（n=30 已经是 10⁹ 级别）。  
> - 对于本题的上限 n=10⁵，暴力根本不可行。

---

#### 代码（Python）

```python
from itertools import combinations

MOD = 10**9 + 7

def sum_good_subseq_bruteforce(nums):
    n = len(nums)
    ans = 0

    # 枚举子序列长度（从 1 到 n）
    for length in range(1, n + 1):
        # 组合出所有长度为 length 的下标集合
        for idxs in combinations(range(n), length):
            good = True
            cur_sum = 0
            # 检查相邻差是否为 1
            for i in range(length):
                cur_sum += nums[idxs[i]]
                if i > 0 and abs(nums[idxs[i]] - nums[idxs[i - 1]]) != 1:
                    good = False
                    break
            if good:
                ans = (ans + cur_sum) % MOD
    return ans
```

> 这段代码只能在 **极小规模**（如 n≤15）下跑通，用来帮助大家理解“全部枚举”到底是怎么做的。

#### 复杂度  

- **时间复杂度**：`O(2ⁿ · n)` —— 随着 n 增长会指数爆炸。  
- **空间复杂度**：`O(n)` —— 只保存临时的组合下标和累计和。

---

### 2. 最优解  

#### 思路  

暴力的瓶颈在于 **“枚举所有子序列”**。  
实际上我们并不需要把每一个子序列完整地列出来，只要知道 **每个数作为子序列最后一个元素时**，所有好子序列的数量和它们的总和即可。  

**关键观察**  

- 好子序列的相邻差只能是 `+1` 或 `-1`。  
- 当我们遍历数组 `nums` 时，当前元素 `x = nums[i]` 只能接在 **以 `x‑1` 或 `x+1` 结尾的子序列** 后面。  
- 因此只要维护两类信息：  
  1. `cnt[v]` – 以值 `v` 结尾的好子序列的 **个数**。  
  2. `sum[v]` – 这些子序列里所有元素的 **总和**（即把每个子序列的元素求和后再相加）。  

这两个数组（或字典）可以在 **一次遍历** 中动态更新——这正是 **动态规划** 的思路：  
> “状态” = “以某个数结尾的好子序列的统计信息”。  
> “转移” = “把当前数接到前一个状态上”。

**转移公式**（设 `x = nums[i]`）  

1. **新建单元素子序列**  
   - 个数：`1`  
   - 总和：`x`  

2. **把 `x` 接在以 `x‑1` 结尾的子序列后**  
   - 产生 `cnt[x‑1]` 条新子序列。  
   - 每条子序列的和在原来的基础上多加 `x`，所以贡献的总和是 `sum[x‑1] + cnt[x‑1] * x`。  

3. **把 `x` 接在以 `x+1` 结尾的子序列后**（同理）  
   - 新的个数：`cnt[x+1]`  
   - 新的总和：`sum[x+1] + cnt[x+1] * x`  

把三部分加起来得到 **本轮新增** 的统计：

```text
new_cnt = 1 + cnt[x-1] + cnt[x+1]
new_sum = x + (sum[x-1] + cnt[x-1]*x) + (sum[x+1] + cnt[x+1]*x)
```

随后把这些新增的统计 **累加到** `cnt[x]`、`sum[x]` 中，因为以后出现的元素仍然可以在它们的基础上继续扩展。  

**答案**：遍历过程中每一次产生的 `new_sum` 就是“以当前元素结尾的所有新好子序列的贡献”，把它们累加即可得到所有好子序列的总和。  

**为什么只需要 `x‑1` 与 `x+1`**：  
相邻差必须是 1，若前一个元素是 `y`，只有 `y = x-1` 或 `y = x+1` 才可能。其它值根本不可能接在一起，故不必考虑。

**数据结构**：  
`cnt`、`sum` 只会出现数组中出现过的数值，范围是 `0 … 10⁵`，使用 `defaultdict(int)`（哈希表）即可。  
哈希表就像一本“查字典”：键是数值，值是对应的统计信息，查找、插入、更新都是 **O(1)**。

**完整流程**  

1. 初始化 `cnt = {}`、`sum = {}`、`ans = 0`。  
2. 依次遍历 `nums` 中的每个 `x`：  
   - 读取 `cnt[x-1]、sum[x-1]、cnt[x+1]、sum[x+1]`（若不存在默认 0）。  
   - 计算 `new_cnt、new_sum`（记得对 `MOD` 取余）。  
   - `cnt[x] = (cnt[x] + new_cnt) % MOD`  
   - `sum[x] = (sum[x] + new_sum) % MOD`  
   - `ans = (ans + new_sum) % MOD`  
3. 返回 `ans`。  

**复杂度分析**  

- 每个元素只做常数次哈希表查询/写入，整体 **时间复杂度 O(n)**。  
- 哈希表最多存储出现过的不同数值，最坏情况是所有 `nums[i]` 不同，空间 **O(uniq)` ≤ O(n)**。  

---

#### 代码（Python）

```python
from collections import defaultdict

MOD = 10**9 + 7

def sum_good_subsequences(nums):
    """
    返回所有好子序列的元素和之和（模 1e9+7）
    """
    cnt = defaultdict(int)   # 以某个值结尾的好子序列个数
    sm  = defaultdict(int)   # 这些子序列的元素总和
    ans = 0

    for x in nums:
        # 读取相邻值的统计信息（若不存在则为 0）
        cnt_l = cnt[x - 1]
        sum_l = sm[x - 1]
        cnt_r = cnt[x + 1]
        sum_r = sm[x + 1]

        # ① 单元素子序列
        # ② 由 x-1 结尾的子序列扩展得到的新子序列
        # ③ 由 x+1 结尾的子序列扩展得到的新子序列
        new_cnt = (1 + cnt_l + cnt_r) % MOD
        new_sum = (
            x +                         # 单元素子序列的和
            (sum_l + cnt_l * x) +       # 扩展自 x-1
            (sum_r + cnt_r * x)         # 扩展自 x+1
        ) % MOD

        # 更新全局统计
        cnt[x] = (cnt[x] + new_cnt) % MOD
        sm[x]  = (sm[x]  + new_sum) % MOD
        ans = (ans + new_sum) % MOD

    return ans
```

**代码要点解释（中文注释）**

```python
cnt = defaultdict(int)   # 哈希表：键是数值，值是「以该数结尾的好子序列个数」
sm  = defaultdict(int)   # 哈希表：键是数值，值是「这些子序列的元素总和」

for x in nums:            # 从左到右遍历数组
    cnt_l = cnt[x - 1]     # 以 x-1 结尾的子序列个数（若不存在为 0）
    sum_l = sm[x - 1]      # 以 x-1 结尾的子序列的总和
    cnt_r = cnt[x + 1]     # 以 x+1 结尾的子序列个数
    sum_r = sm[x + 1]      # 以 x+1 结尾的子序列的总和

    # 计算「本轮」产生的子序列数量和它们的元素和
    new_cnt = (1 + cnt_l + cnt_r) % MOD          # 1 表示单独的 [x]
    new_sum = (x + (sum_l + cnt_l * x) + (sum_r + cnt_r * x)) % MOD

    # 把本轮新产生的统计信息加入到以 x 结尾的累计统计里
    cnt[x] = (cnt[x] + new_cnt) % MOD
    sm[x]  = (sm[x]  + new_sum) % MOD

    # 同时把本轮的贡献加入答案
    ans = (ans + new_sum) % MOD
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 只遍历一次数组，每次只做 O(1) 哈希表操作。相比暴力的指数级别，快得多。  
- **空间复杂度**：`O(m)`，其中 `m` 是数组中不同数值的个数，最坏 `m ≤ n`，即线性空间。  

---

## 心得  

- **核心技巧**：**以“最后一个元素”为状态的动态规划 + 哈希表统计**。  
- **适用题型**（类似思路）  
  1. “以某个数结尾的递增子序列计数”（LeetCode 673 – Number of Longest Increasing Subsequence）。  
  2. “相邻差为固定值的子序列求和/计数”（如差为 0 的相同元素子序列）。  
  3. “连续子数组/子序列的最大/最小值统计” 中常用的“前缀/后缀 + 哈希表”思路。  

- **一句话总结解题钥匙**：**把“所有子序列”压缩成“以某个值结尾的统计”，用 DP 一步步累计即可**。

---

## 反思  

- **第一反应**：直接想枚举、检查、累加——这在小数据时能跑通，却忽视了指数爆炸。  
- **最容易踩的坑**  
  - **忘记取模**：在乘法 `cnt * x` 以及累计时必须对 `MOD` 取余，否则会溢出。  
  - **边界值**：`x` 可能是 `0`，访问 `cnt[-1]` 时会产生负键，使用 `defaultdict(int)` 可自动返回 `0`，避免 `KeyError`。  
  - **重复计数**：每次更新 `cnt[x]`、`sm[x]` 时要 **累加**（`+=`），而不是直接赋值，否则后面的扩展会丢失之前的子序列。  

- **下次类似题目**：  
  1. **先定位状态**：以“最后一个元素”或“当前最大/最小值”等为 DP 状态。  
  2. **找转移**：看当前元素能接在哪些已有状态后面（本题是 `x‑1`、`x+1`）。  
  3. **设计统计**：如果要求“和”，除了计数外还要维护“总和”。  

这样一步步抽象，就能把看似指数级的组合问题，压缩成线性时间的动态规划。祝你玩转算法！