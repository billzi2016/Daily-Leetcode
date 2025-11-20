# #3428. 最大且最小子序列和（至多 K 个元素） / Maximum and Minimum Sums of at Most Size K Subsequences

> 难度：中等 · 标签：Array、Math、Dynamic Programming、Sorting、Combinatorics · [LeetCode 链接](https://leetcode.com/problems/maximum-and-minimum-sums-of-at-most-size-k-subsequences/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and a positive integer k. Return the sum of the maximum and minimum elements of all subsequences of nums with at most k elements.
Since the answer may be very large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3], k = 2
Output: 24
Explanation:
The subsequences of nums with at most 2 elements are:
The output would be 24.
```

**Example 2:**

```
Input: nums = [5,0,6], k = 1
Output: 2 2
Explanation:
For subsequences with exactly 1 element, the minimum and maximum values are the element itself. Therefore, the total is 5 + 5 + 0 + 0 + 6 + 6 = 22 .
```

**Example 3:**

```
Input: nums = [1,1,1], k = 2
Output: 12
Explanation:
The subsequences [1, 1] and [1] each appear 3 times. For all of them, the minimum and maximum are both 1. Thus, the total is 12.
```

**Constraints**

- 1 <= nums.length <= 105
- 0 <= nums[i] <= 109
- 1 <= k <= min(70, nums.length)

---

## 题目（中文翻译）

给定一个整数数组 `nums` 和一个正整数 `k`。返回所有长度至多 `k` 的子序列（subsequence）中，最大元素与最小元素之和的总和。由于答案可能非常大，请返回 `10^9 + 7` 取模后的结果。

### 示例

#### 示例 1
**输入**  
```json
nums = [1,2,3], k = 2
```
**输出**  
```
24
```
**解释**  
长度至多为 2 的子序列有：
（此处列出所有子序列并计算每个子序列的最大值与最小值之和，最终累计得到 24）

#### 示例 2
**输入**  
```json
nums = [5,0,6], k = 1
```
**输出**  
```
22
```
**解释**  
当子序列恰好包含 1 个元素时，最小值与最大值均为该元素本身。因此总和为  
`5 + 5 + 0 + 0 + 6 + 6 = 22`。

#### 示例 3
**输入**  
```json
nums = [1,1,1], k = 2
```
**输出**  
```
12
```
**解释**  
子序列 `[1, 1]` 与 `[1]` 各出现 3 次。对于所有这些子序列，最小值与最大值均为 1。故总和为 `12`。

### 约束条件
- `1 <= nums.length <= 10^5`
- `0 <= nums[i] <= 10^9`
- `1 <= k <= min(70, nums.length)`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法就是 **枚举所有合法的子序列**（subsequence），把每个子序列的最大值 `max` 与最小值 `min` 相加，再把这些和累加起来。  

- **枚举子序列**：可以把数组的每个元素看成“要不要放进子序列”，于是一共有 `2ⁿ` 种取法。  
- **过滤大小**：只保留长度 `≤ k` 的子序列。  
- **统计**：对每个保留下来的子序列，求 `max + min`，累加到答案中。  

> **类比**：想象你有 `n` 本书，每本书可以选也可以不选，所有可能的阅读清单就是 `2ⁿ` 种。如果你只能阅读不超过 `k` 本书，就要把超出 `k` 本的清单丢掉。  

这个办法一定能得到正确答案，因为我们把**所有**合法的子序列都遍历了一遍，自然不会漏掉也不会多算。  

#### 代码（Python）  

```python
from itertools import combinations

MOD = 10 ** 9 + 7

def brute(nums, k):
    n = len(nums)
    ans = 0
    # 枚举子序列的长度 1~k
    for sz in range(1, k + 1):
        # 组合得到所有长度为 sz 的子序列（顺序保持不变）
        for idxs in combinations(range(n), sz):
            subseq = [nums[i] for i in idxs]
            ans = (ans + max(subseq) + min(subseq)) % MOD
    return ans
```

> 这里的 `combinations` 会自动保持原数组的相对顺序，等价于子序列的定义。  

#### 复杂度  

- **时间复杂度**：`O( Σ_{sz=1}^{k} C(n, sz) )`  
  - 在最坏情况下（比如 `k = n`）相当于遍历所有 `2ⁿ` 种子集，指数级别的时间，几乎不可能在 `n ≤ 10⁵` 时跑完。  
- **空间复杂度**：`O(k)`（递归栈或 `combinations` 的临时存储），和输入规模无关。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **枚举子序列** 本身。我们要把“遍历所有子序列”这一步去掉，直接算出每个元素会在多少个子序列里贡献一次 `max`，以及会在多少个子序列里贡献一次 `min`，然后乘以该元素的值相加即可。  

**关键观察**  

1. 把数组 **从小到大排序**。  
2. 对于排好序的数组 `a[0] ≤ a[1] ≤ … ≤ a[n‑1]`：  
   - 若一个子序列的 **最大值** 是 `a[i]`，那么子序列里只能包含 **它左边**（下标 `< i`）的元素，且这些左边元素的选取方式不影响 `a[i]` 是最大值。  
   - 同理，若一个子序列的 **最小值** 是 `a[i]`，只能包含 **它右边**（下标 `> i`）的元素。  

因此，**每个元素 `a[i]` 作为最大值出现的次数** = “从它左边的 `i` 个元素中任选 `0~k‑1` 个（因为子序列最多 `k` 个，最大值本身已经占 1 位）” 的组合数之和。  

记  
\[
C_{i}^{(t)} = \binom{i}{t}
\]  
则  
\[
\text{cnt\_max}[i] = \sum_{t=0}^{k-1} \binom{i}{t}
\]  

同理，**每个元素作为最小值出现的次数** = “从它右边的 `n‑1‑i` 个元素中任选 `0~k‑1` 个”。  

\[
\text{cnt\_min}[i] = \sum_{t=0}^{k-1} \binom{n-1-i}{t}
\]  

**答案公式**  

\[
\text{ans} = \sum_{i=0}^{n-1} a[i]\;(\text{cnt\_max}[i] + \text{cnt\_min}[i]) \pmod{M}
\]  

其中 `M = 10⁹ + 7` 为题目要求的模数。  

**如何高效计算组合数**  

- 题目给出 `k ≤ 70`（远小于 `n ≤ 10⁵`），所以只需要 **预计算** `C(n, r)`，其中 `0 ≤ r ≤ k-1`。  
- 使用 **动态规划**（帕斯卡三角）递推：  
  \[
  \binom{n}{r} = \binom{n-1}{r} + \binom{n-1}{r-1} \pmod{M}
  \]  
- 只保留到第 `k-1` 列即可，空间复杂度 `O(k)`，时间复杂度 `O(n·k)`（约 `10⁵·70 = 7·10⁶`，完全可以接受）。  

**一步步的实现思路**  

1. **排序** `nums` → `a`（升序）。  
2. **预计算组合数** `C[n][r]`（`0 ≤ n ≤ len(a)`，`0 ≤ r ≤ k-1`）。  
3. **预计算前缀求和** `pref[i] = Σ_{t=0}^{k-1} C[i][t]`，同理 `suf[i] = Σ_{t=0}^{k-1} C[n-1-i][t]`（可以直接在遍历时用 `C` 查表）。  
4. **遍历数组**，累计 `a[i] * (pref[i] + suf[i])`，取模。  

这样我们把指数级别的枚举压缩成了 **线性**（`O(n·k)`）的计算。  

#### 代码（Python）  

```python
MOD = 10 ** 9 + 7

def max_min_sum(nums, k):
    """
    返回所有长度 ≤ k 的子序列中 max+min 的和，取模 1e9+7
    """
    n = len(nums)
    a = sorted(nums)                     # 1️⃣ 排序，方便区分「左边」和「右边」
    
    # 2️⃣ 预计算组合数 C[n][r]（只到 r = k-1）
    # C[i][r] = C(i, r) % MOD
    C = [[0] * k for _ in range(n + 1)]
    for i in range(n + 1):
        C[i][0] = 1                       # C(i,0) = 1
        # 只需要计算到 min(i, k-1)
        up = min(i, k - 1)
        for r in range(1, up + 1):
            C[i][r] = (C[i - 1][r] + C[i - 1][r - 1]) % MOD
    
    # 3️⃣ 计算前缀/后缀的「≤k-1 个元素的组合数之和」
    # prefix[i] = Σ_{t=0}^{k-1} C(i, t)
    prefix = [0] * n
    suffix = [0] * n
    for i in range(n):
        # 左边有 i 个元素（下标 < i）
        s = 0
        for t in range(k):               # t 从 0 到 k-1
            if t <= i:                    # 组合数定义域
                s = (s + C[i][t]) % MOD
        prefix[i] = s

        # 右边有 n-1-i 个元素（下标 > i）
        right = n - 1 - i
        s = 0
        for t in range(k):
            if t <= right:
                s = (s + C[right][t]) % MOD
        suffix[i] = s

    # 4️⃣ 累加答案
    ans = 0
    for i in range(n):
        coeff = (prefix[i] + suffix[i]) % MOD   # 出现次数 = 作为 max + 作为 min
        ans = (ans + a[i] * coeff) % MOD

    return ans
```

**代码要点说明**  

- `C` 的大小是 `(n+1) × k`，因为我们只关心 `0…k-1` 列，省掉了大量无用空间。  
- `prefix[i]` 表示 “从左侧 `i` 个元素中任选 `0~k‑1` 个”的组合数之和，恰好等于 `cnt_max[i]`。  
- `suffix[i]` 表示 “从右侧 `n‑1‑i` 个元素中任选 `0~k‑1` 个”的组合数之和，等于 `cnt_min[i]`。  
- 最后 `a[i] * (prefix[i] + suffix[i])` 就是该元素在所有子序列里贡献的 `max+min` 总和。  

#### 复杂度  

- **时间复杂度**：`O(n·k)`  
  - 预计算组合数：`n·k`  
  - 计算 `prefix / suffix`：每个位置遍历 `k` 次，同样 `n·k`  
  - 其余都是线性 `O(n)`。  
  - 对比暴力的 `O(2ⁿ)`，大幅下降到线性（乘以常数 `k ≤ 70`）。  
- **空间复杂度**：`O(n·k)` 用于存放组合数表（约 `7·10⁶` 个整数，约 56 MB，仍在多数平台可接受范围）。如果进一步优化，可以只保留上一行的值，把空间压到 `O(k)`，但对可读性不太友好，这里保持简单直观。  

---

## 心得  

- **核心技巧**：把 “每个子序列的 max+min” 拆解为 “每个元素作为 max 出现的次数 + 作为 min 出现的次数”。  
- **适用题型**：  
  1. “求所有子集（或子序列）中某种统计量的加权和”，如 “所有子集的最大值之和”。  
  2. “固定长度 ≤ k 的组合计数”，常见于 combinatorial + DP 题目。  
  3. “对每个元素计数它在满足某种约束的子集中的出现次数”。  
- **一句话总结**：**把子集遍历的工作交给组合数，元素本身只要乘以它在“左侧/右侧”能选的组合数之和即可。**  

---

## 反思  

- **第一反应**：直接枚举所有子序列，写出暴力代码，检查样例是否能跑通。  
- **最容易踩的坑**：  
  - 忘记对 **长度为 1** 的子序列计数（此时 max = min，应该算两次）。  
  - 组合数取模时溢出，必须在每一步 `% MOD`。  
  - `k` 可能大于 `n`，但题目已限制 `k ≤ n`，实现时仍要防止 `t > i` 的非法访问。  
- **下次类似题目**：第一步先思考 **“每个元素在满足约束的子集里出现多少次？”**，把求和转化为 “元素 × 出现次数”。这样往往可以用组合数或前缀/后缀计数把指数级枚举压到多项式时间。