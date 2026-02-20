# #3533. 拼接可整除 / Concatenated Divisibility

> 难度：困难 · 标签：Array、Dynamic Programming、Bit Manipulation、Bitmask · [LeetCode 链接](https://leetcode.com/problems/concatenated-divisibility/)

---

## 题目（英文原版）

**Description**

You are given an array of positive integers nums and a positive integer k.
A permutation of nums is said to form a divisible concatenation if, when you concatenate the decimal representations of the numbers in the order specified by the permutation, the resulting number is divisible by k.
Return the lexicographically smallest permutation (when considered as a list of integers) that forms a divisible concatenation. If no such permutation exists, return an empty list.

**Examples**

**Example 1:**

```
Input: nums = [3,12,45], k = 5
Output: [3,12,45]
Explanation:
The lexicographically smallest permutation that forms a divisible concatenation is [3,12,45] .
```

**Example 2:**

```
Input: nums = [10,5], k = 10
Output: [5,10]
Explanation:
The lexicographically smallest permutation that forms a divisible concatenation is [5,10] .
```

**Example 3:**

```
Input: nums = [1,2,3], k = 5
Output: []
Explanation:
Since no permutation of nums forms a valid divisible concatenation, return an empty list.
```

**Constraints**

- 1 <= nums.length <= 13
- 1 <= nums[i] <= 105
- 1 <= k <= 100

---

## 题目（中文翻译）

你被给定一个正整数数组 `nums` 和一个正整数 `k`。  
如果对 `nums` 的一个排列（permutation），按照该排列的顺序把每个数字的十进制表示依次拼接成一个整数，且该整数能够被 `k` 整除，则称该排列形成了一个可整除的拼接（divisible concatenation）。

请返回字典序（lexicographically）最小的排列（视为整数列表），使其形成可整除的拼接。如果不存在满足条件的排列，返回空列表。

**示例 1**  
输入: `nums = [3,12,45]`, `k = 5`  
输出: `[3,12,45]`  
解释:  
字典序最小的能够形成可整除拼接的排列是 `[3,12,45]`。

**示例 2**  
输入: `nums = [10,5]`, `k = 10`  
输出: `[5,10]`  
解释:  
字典序最小的能够形成可整除拼接的排列是 `[5,10]`。

**示例 3**  
输入: `nums = [1,2,3]`, `k = 5`  
输出: `[]`  
解释:  
没有任何排列能够形成满足条件的可整除拼接，返回空列表。

**约束条件**  
- `1 <= nums.length <= 13`  
- `1 <= nums[i] <= 10^5`  
- `1 <= k <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**把所有可能的排列都列举出来**，逐个检查它们拼接成的整数是否能被 `k` 整除。  

- **数据结构**：  
  - `list`（列表）保存原始的 `nums`。  
  - `itertools.permutations` 相当于把所有排列装进一个“装配线”，每一次取出一条完整的排列。可以把它想象成 **字典**：键是排列的顺序，值是对应的数字，只不过这里我们一次性把所有键都列出来。  
- **正确性**：  
  - 任意一个合法的排列一定会出现在所有排列的集合中，遍历全部就不会漏掉。只要我们对每个排列都做“拼接 → 取模 → 判断是否为 0”的检查，就一定能找出所有可行的答案。  
- **时间/空间复杂度**：  
  - `nums` 长度记作 `n`（最多 13），所有排列的数量是 `n!`（阶乘），比如 `n=10` 时已经是 3,628,800 条。  
  - 对每条排列我们要把 `n` 个数拼接起来，拼接过程本身是线性的 `O(n)`，所以总体时间是 **O(n!·n)**，在最坏情况下会非常慢。  
  - 只需要保存当前枚举的一个排列和临时的拼接结果，额外空间是 **O(n)**（保存列表本身），不随排列数量增长。

> **大白话**：  
> `O(n!·n)` 可以理解为“先把所有可能的排队顺序都排好（这一步已经很耗时），然后再把每个顺序里的数字一个接一个写下来”。阶乘增长速度比线性、平方、立方都快得多，13! 已经是 6.2 × 10⁹，几乎不可能在一分钟内跑完。

#### 代码（Python）

```python
import itertools
from typing import List

def concatenated_number(nums: List[int], order: List[int]) -> int:
    """把按照 order 排列的 nums 拼接成一个整数"""
    res = 0
    for idx in order:
        x = nums[idx]
        # 计算 x 有多少位（10 的多少次方），然后把它左移到合适的位置
        d = 1
        while d <= x:
            d *= 10               # d 最终是 10 的位数次方
        res = res * d + x
    return res

def smallest_divisible_permutation(nums: List[int], k: int) -> List[int]:
    n = len(nums)
    # 所有下标的全排列，例如 n=3 时会得到 (0,1,2)、(0,2,1) ...
    for perm in itertools.permutations(range(n)):
        # 按当前排列拼接成的大数
        big = concatenated_number(nums, perm)
        if big % k == 0:                     # 能被 k 整除
            # 把下标转回真实的数字序列，即为答案
            return [nums[i] for i in perm]   # 这里已经是字典序最小的，因为 permutations 按字典序生成
    return []                                 # 没有合法排列
```

#### 复杂度

- **时间复杂度**：`O(n!·n)`  
  - `n!` 是所有排列的数量，`n` 是每条排列里需要拼接的数字个数。  
  - 对于 `n=13`，`13! ≈ 6.2×10⁹`，在实际运行时会超时。

- **空间复杂度**：`O(n)`  
  - 只存放当前遍历的一个排列和拼接过程中的临时整数。  

---

### 2. 最优解

#### 思路  

暴力解慢的根源在于 **“枚举所有排列”**，而我们只关心 **“是否能被 k 整除”**，这可以用 **模运算的性质** 来剪枝。  

关键观察：

1. **拼接的模运算可以拆分**  
   假设已有的拼接结果是 `cur`（已对 `k` 取模），接下来要拼接一个数 `x`，`x` 有 `len(x)` 位。  
   拼接后得到的数是 `cur * 10^{len(x)} + x`，对 `k` 取模后等价于  

   ```
   new_mod = (cur * (10^{len(x)} mod k) + x mod k) mod k
   ```

   因此只要知道 `cur mod k`，就可以在 **O(1)** 时间得到拼接后新的余数。

2. **状态可以用「已使用的元素集合」+「当前余数」描述**  
   - 已使用的集合可以用 **位掩码（bitmask）** 表示，`mask` 的第 `i` 位为 `1` 表示第 `i` 个数已经放进排列。  
   - `rem` 表示把已经选好的数拼接起来后对 `k` 的余数。  

   于是我们得到 **DP 状态** `dp[mask][rem]`：是否存在一种排列，使得使用的元素集合是 `mask`，且拼接后余数为 `rem`。  

3. **转移**  
   对于每个未使用的数 `i`（即 `mask` 第 `i` 位为 `0`），把它接到当前序列后得到新的余数 `new_rem`，并把状态转移到 `mask | (1<<i)`。  

4. **求最小字典序**  
   DP 只告诉“是否存在”。要得到 **字典序最小的排列**，我们在 **回溯** 时每一步都尝试下标从小到大的数字，只要该选择在 DP 表中是可行的，就把它加入答案。这样得到的就是字典序最小的排列。

5. **预处理**  
   - `len_i`：每个数的十进制位数。  
   - `pow10_mod[l] = 10^l mod k`（`l` 最大到 6，因为 `nums[i] ≤ 10^5`），可以一次性算好，后面查表 O(1)。  

**整体流程**  

- 预计算每个数的位数 `len_i` 与 `10^{len_i} mod k`。  
- 用 **位掩码 DP**（自底向上或记忆化递归）填表，时间复杂度 `O(n * 2^n * k)`，其中 `k ≤ 100`，所以常数很小。  
- 从 `mask = 0, rem = 0` 开始，按照下标从小到大尝试取数，只要对应的后继状态在 DP 表中为 `True`，就把它加入答案。  
- 若最终 `mask = (1<<n)-1` 时 `rem = 0` 不可达，返回空列表。

**为什么快**：  
- `2^n`（最多 8192）远小于 `n!`（上千亿），加上 `k` 只有 100，整体约 `13 * 8192 * 100 ≈ 1.1×10⁷` 次运算，轻松在毫秒级完成。

#### 代码（Python）

```python
from typing import List

def smallest_divisible_permutation(nums: List[int], k: int) -> List[int]:
    n = len(nums)

    # ---------- 1. 预处理 ----------
    # 每个数的十进制位数
    lens = []
    # 对应的 10^{len} mod k
    ten_pow_mod = []
    for x in nums:
        l = 0
        t = x
        while t:
            t //= 10
            l += 1
        lens.append(l)
        # 计算 10^l % k
        pow_mod = pow(10, l, k)   # Python 内置的快速幂取模
        ten_pow_mod.append(pow_mod)

    # ---------- 2. DP：mask × remainder ----------
    # dp[mask][rem] = True 表示「可以用 mask 表示的集合拼接后余数为 rem」
    size = 1 << n
    dp = [[False] * k for _ in range(size)]
    dp[0][0] = True               # 空集合，余数 0（因为没有数字时视作 0）

    for mask in range(size):
        for rem in range(k):
            if not dp[mask][rem]:
                continue
            # 尝试把一个还未使用的数 i 加到序列后面
            for i in range(n):
                if mask >> i & 1:   # 已经使用过
                    continue
                new_mask = mask | (1 << i)
                # 余数转移公式：new = (rem * 10^{len_i} + nums[i]) % k
                new_rem = (rem * ten_pow_mod[i] + nums[i] % k) % k
                dp[new_mask][new_rem] = True

    full_mask = (1 << n) - 1
    if not dp[full_mask][0]:      # 没有任何排列能让余数为 0
        return []

    # ---------- 3. 重建字典序最小的排列 ----------
    ans = []
    mask, rem = 0, 0
    while mask != full_mask:
        # 按下标从小到大尝试，保证字典序最小
        for i in range(n):
            if mask >> i & 1:
                continue
            new_mask = mask | (1 << i)
            new_rem = (rem * ten_pow_mod[i] + nums[i] % k) % k
            # 只有当后继状态可达时才选这个数
            if dp[new_mask][new_rem]:
                ans.append(nums[i])
                mask, rem = new_mask, new_rem
                break   # 选定后立刻跳到下一位
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n * 2^n * k)`  
  - `2^n` 是所有子集的数量（`n ≤ 13`），`n` 是遍历每个子集时尝试加入的候选数，`k ≤ 100` 是余数的取值范围。  
  - 与暴力的 `n!·n` 相比，指数级下降（`2^13 = 8192` vs `13! ≈ 6·10⁹`），实际运行非常快。

- **空间复杂度**：`O(2^n * k)`  
  - DP 表需要保存每个子集对应的 `k` 个余数的可达性。  
  - 对于最大规模：`8192 * 100 ≈ 8.2×10⁵` 个布尔值，约 0.8 MB，完全可接受。

---

## 心得

- **核心技巧**：利用 **模运算的可拆分性** 与 **位掩码 DP**（子集 DP）把“全排列”问题压缩到指数级别的状态空间。  
- **适用的题型**  
  1. “把数字拼接后满足某种模条件”——如 *LeetCode 1155*（`Number of Digits in a Concatenated Number`）的变体。  
  2. “在子集上做状态转移”——如 *LeetCode 1982*（`Find Array Given Subset Sums`）或旅行商问题的位掩码 DP。  
  3. “需要字典序最小/最大答案”——在 DP 完成后通过 **从小到大尝试** 重建路径即可。  

- **一句话总结**：  
  “把拼接余数拆成 `cur * 10^{len} + x`，用子集+余数的 DP 保存可行性，最后按字典序回溯得到最小排列。”

---

## 反思

- **第一反应**：直接枚举全部排列，写出判断函数，想“一次搞定”。  
- **最容易踩的坑**  
  1. **位数计算错误**：忘记对 `0` 也算作 1 位，或在 `while t` 循环里漏掉最后一次乘 10。  
  2. **模运算溢出**：拼接前的中间结果可能非常大，必须始终在模 `k` 的范围内计算（使用 `pow(10, l, k)`）。  
  3. **字典序恢复**：只检查 `dp[new_mask][new_rem]` 是否为 `True` 而不考虑顺序，会得到任意合法排列，而非最小的。  
- **下次类似题的第一步**：  
  “先把‘拼接后取模’写成递推公式，看看能否只用当前余数和一个数的属性来更新，然后考虑用 **子集+余数** 的 DP 把枚举空间压到 `2^n`”。