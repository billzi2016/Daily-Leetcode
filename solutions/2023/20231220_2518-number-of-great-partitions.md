# #2518. 优秀划分的数量 / Number of Great Partitions

> 难度：困难 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/number-of-great-partitions/)

---

## 题目（英文原版）

**Description**

You are given an array nums consisting of positive integers and an integer k.
Partition the array into two ordered groups such that each element is in exactly one group. A partition is called great if the sum of elements of each group is greater than or equal to k.
Return the number of distinct great partitions. Since the answer may be too large, return it modulo 109 + 7.
Two partitions are considered distinct if some element nums[i] is in different groups in the two partitions.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,4], k = 4
Output: 6
Explanation: The great partitions are: ([1,2,3], [4]), ([1,3], [2,4]), ([1,4], [2,3]), ([2,3], [1,4]), ([2,4], [1,3]) and ([4], [1,2,3]).
```

**Example 2:**

```
Input: nums = [3,3,3], k = 4
Output: 0
Explanation: There are no great partitions for this array.
```

**Example 3:**

```
Input: nums = [6,6], k = 2
Output: 2
Explanation: We can either put nums[0] in the first partition or in the second partition.
The great partitions will be ([6], [6]) and ([6], [6]).
```

**Constraints**

- 1 <= nums.length, k <= 1000
- 1 <= nums[i] <= 109

---

## 题目（中文翻译）

给定一个由正整数构成的数组 `nums` 和一个整数 `k`。  
将数组划分为两个有序的组，使得每个元素恰好属于其中一个组。若两个组的元素和均 **大于等于** `k`，则该划分称为 **优秀划分（great partition）**。  
返回不同的优秀划分的数量。由于答案可能非常大，请返回对 `10^9 + 7` 取模后的结果。  
如果在两个划分中存在某个元素 `nums[i]` 所在的组不同，则这两个划分被视为不同。

### 示例

#### 示例 1
**输入**  
`nums = [1,2,3,4], k = 4`

**输出**  
`6`

**解释**  
优秀划分有：  
`([1,2,3], [4])`、`([1,3], [2,4])`、`([1,4], [2,3])`、`([2,3], [1,4])`、`([2,4], [1,3])`、`([4], [1,2,3])`。

#### 示例 2
**输入**  
`nums = [3,3,3], k = 4`

**输出**  
`0`

**解释**  
该数组不存在满足条件的优秀划分。

#### 示例 3
**输入**  
`nums = [6,6], k = 2`

**输出**  
`2`

**解释**  
我们可以将 `nums[0]` 放在第一组或第二组，两种划分分别为 `([6], [6])` 和 `([6], [6])`，均满足条件。

### 约束条件
- `1 <= nums.length, k <= 1000`
- `1 <= nums[i] <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把每个元素都**决定**它到底进入第一个组还是第二个组。  
这和我们平时把物品装进两个盒子里是一样的——每件物品有两种选择。  
把所有决定写成一串 `0/1`（`0` 代表放进组 1，`1` 代表放进组 2），  
所有可能的决定总数就是 `2ⁿ`（`n` 为数组长度），这正是**全部分割**的数量。

暴力做法就是把这 `2ⁿ` 种决定全部枚举出来，  
每枚举一种，就算出两组的和，检查它们是否都 **≥ k**，符合条件就计数。  

> **类比**：把 `dp` 当成一本“查字典”。  
> - “单词” 是一种决定（比如 `0101…`）  
> - “页码” 是这决定对应的两组和  

只要把所有“单词”都翻一遍，就能知道有多少页码满足要求。

**为什么一定正确**  
因为我们没有遗漏任何一种可能，也没有多算重复的情况，  
所以只要遍历完全部 `2ⁿ` 种决定，计数的结果必然就是答案。

**时间/空间复杂度**  
- 枚举 `2ⁿ` 种决定，每种都要遍历 `n` 个数求和 → **时间 O( n·2ⁿ )**。  
  用大白话说，`2ⁿ` 是指数级增长，`n` 只是在每次枚举里多走几步，整体非常慢。  
- 只需要记录当前的两组和 → **空间 O(1)**（常数级）。

显然，当 `n` 超过 20 左右时，这种方法就不可用了。

#### 代码（Python）

```python
from itertools import product

MOD = 10**9 + 7

def great_partitions_bruteforce(nums, k):
    n = len(nums)
    ans = 0
    # product 会生成所有 0/1 的组合，长度为 n
    for mask in product([0, 1], repeat=n):
        sum_a = 0          # 组 A 的和
        sum_b = 0          # 组 B 的和
        for i, bit in enumerate(mask):
            if bit == 0:   # 放进组 A
                sum_a += nums[i]
            else:          # 放进组 B
                sum_b += nums[i]
        if sum_a >= k and sum_b >= k:
            ans = (ans + 1) % MOD
    return ans
```

#### 复杂度  

- 时间复杂度：**O(n·2ⁿ)** — 指数级，随着 `n` 增长会很快失去可用性。  
- 空间复杂度：**O(1)** — 只用几个整数保存当前的两组和。

---

### 2. 最优解  

#### 思路  

从暴力解出发，**瓶颈** 正是枚举所有 `2ⁿ` 种决定。  
我们需要一种只遍历 **一次**（或者 `O(n·k)`）就能得到答案的方法。

观察题目可以把它转换为**子集计数**的问题：

- 把数组划分为两个**有序**的组，其实只需要决定“哪一些元素进入组 1”，
  剩下的自然进入组 2。  
- 设总和 `S = sum(nums)`，如果我们记下组 1 的和为 `x`，  
  那么组 2 的和就是 `S - x`。  

> **条件**：`x ≥ k` 且 `S - x ≥ k`  
> ⇔ `k ≤ x ≤ S - k`

于是**答案**等于 **满足 `k ≤ x ≤ S - k` 的子集个数**（每个子集直接对应一种有序划分）。

#### 为什么可以只算 “和小于 k”  

直接统计 `x` 落在 `[k, S-k]` 的子集看起来需要遍历到 `S`（可能非常大）。  
但注意到：

- 若 `x < k`，显然不合法。  
- 若 `x > S - k`，等价于 `S - x < k`（组 2 不合法）。  

这两种“不合法”的子集是**互斥**的（只要 `S ≥ 2k`，两者不可能同时成立），
并且它们的数量是相等的：  
把一个“不合法”子集的元素全部取反（即取补集），就会得到另一个“不合法”子集。  

所以：

```
合法子集数量 = 所有子集数量 - 2 * (和 < k 的子集数量)
```

- **所有子集数量** 是 `2ⁿ`（每个元素要么在组 1，要么不在）。  
- **和 < k 的子集数量** 只需要统计到 `k‑1`，而 `k ≤ 1000`，这可以用 **背包 DP** 完成。

#### 动态规划（背包）求 “和 < k” 的子集数  

我们维护一个长度为 `k` 的数组 `dp[s]`，表示**和恰好等于 `s` 的子集个数**（模 `MOD`）。  

初始化：`dp[0] = 1`（空子集的和为 0）。  
遍历每个数 `num`，从大到小更新 `dp`：

```
for s from k-1 down to 0:
    if s + num < k:
        dp[s + num] = (dp[s + num] + dp[s]) % MOD
```

倒序遍历保证每个数只被使用一次，防止重复计数。

遍历完所有元素后，`cnt_lt_k = sum(dp[0:k]) % MOD` 即为 **和 < k** 的子集总数（包括空集）。

最后答案：

```
total = pow(2, n, MOD)                 # 2ⁿ (模 MOD)
ans   = (total - 2 * cnt_lt_k) % MOD   # 可能为负，取模后修正
```

如果 `S < 2*k`，根本不可能出现合法划分，直接返回 0。

#### 代码（Python）

```python
MOD = 10**9 + 7

def great_partitions(nums, k):
    n = len(nums)
    total_sum = sum(nums)

    # 1. 先判断不可行的情况
    if total_sum < 2 * k:          # 两组都要 ≥ k，整体和不够
        return 0

    # 2. DP 求和 < k 的子集数量
    dp = [0] * k          # dp[s] = 子集和恰好为 s 的方案数
    dp[0] = 1             # 空集

    for num in nums:
        # 只关心 sum < k，超出 k 的状态不需要保存
        for s in range(k - 1, -1, -1):
            nxt = s + num
            if nxt < k:
                dp[nxt] = (dp[nxt] + dp[s]) % MOD

    cnt_lt_k = sum(dp) % MOD          # 所有和 < k 的子集（包括空集）

    # 3. 计算答案
    total_subsets = pow(2, n, MOD)    # 2ⁿ（模 MOD）
    ans = (total_subsets - 2 * cnt_lt_k) % MOD
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n * k)`  
  - `n ≤ 1000`，`k ≤ 1000`，最多约 `10⁶` 次基本运算，轻松通过。  
  - 与暴力的指数级 `2ⁿ` 相比，快了好几个数量级。  
- **空间复杂度**：`O(k)`  
  - 只需要一个长度为 `k` 的一维数组，最多 `1000` 个整数。

---

## 心得  

- **核心技巧**：把“两个组都满足条件”转化为“子集的和落在一个区间”。  
- **关键点**：利用对称性把区间外的计数（`sum < k`）翻倍后从全部子集 `2ⁿ` 中减去，避免直接枚举大范围的和。  
- **适用场景**  
  1. “两组和都 ≥ 某阈值” 类的问题（如 **Number of Great Partitions**）。  
  2. “两组和的差不超过某值” 需要把条件转化为子集和区间的题目。  
  3. 任何可以用 **子集和 ≤ X** 计数的组合计数问题（背包 DP 常用）。

> **解题钥匙**：把复杂的“两个组”约束化简为“单个子集的和在区间”，再用 **背包 DP** 只统计区间的一侧。

---

## 反思  

- **第一反应**：直接枚举所有划分（暴力），因为对“分组”直觉最强。  
- **最容易踩的坑**  
  1. **总和不足**：如果 `sum(nums) < 2*k`，直接返回 0，忘记会导致 DP 仍然跑但答案错误。  
  2. **模运算负数**：`total - 2*cnt_lt_k` 可能为负，需要加上 `MOD` 再取模。  
  3. **DP 边界**：只更新 `s+num < k` 的状态，防止数组越界并保持 `O(k)` 空间。  
- **下次遇到同类题**，第一步应该：  
  1. 计算总和，检查是否满足基本的 “两组都 ≥ k” 条件。  
  2. 思考能否把两组约束转化为 **子集和的区间**，并利用对称性把区间外的计数简化。  
  3. 若区间上限太大，尝试只统计区间下限（`< k`）并用 `2ⁿ` 减法得到答案。