# #1994. 好子集的数量 / The Number of Good Subsets

> 难度：困难 · 标签：Array、Hash Table、Math、Dynamic Programming、Bit Manipulation、Counting、Number Theory、Bitmask · [LeetCode 链接](https://leetcode.com/problems/the-number-of-good-subsets/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums. We call a subset of nums good if its product can be represented as a product of one or more distinct prime numbers.
Return the number of different good subsets in nums modulo 109 + 7.
A subset of nums is any array that can be obtained by deleting some (possibly none or all) elements from nums. Two subsets are different if and only if the chosen indices to delete are different.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,4]
Output: 6
Explanation: The good subsets are:
- [1,2]: product is 2, which is the product of distinct prime 2.
- [1,2,3]: product is 6, which is the product of distinct primes 2 and 3.
- [1,3]: product is 3, which is the product of distinct prime 3.
- [2]: product is 2, which is the product of distinct prime 2.
- [2,3]: product is 6, which is the product of distinct primes 2 and 3.
- [3]: product is 3, which is the product of distinct prime 3.
```

**Example 2:**

```
Input: nums = [4,2,3,15]
Output: 5
Explanation: The good subsets are:
- [2]: product is 2, which is the product of distinct prime 2.
- [2,3]: product is 6, which is the product of distinct primes 2 and 3.
- [2,15]: product is 30, which is the product of distinct primes 2, 3, and 5.
- [3]: product is 3, which is the product of distinct prime 3.
- [15]: product is 15, which is the product of distinct primes 3 and 5.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 30

---

## 题目（中文翻译）

你得到一个整数数组 `nums`。如果一个 `nums` 的子集（subset）的乘积（product）能够表示为一个或多个 **不同的**（distinct）质数（prime numbers）的乘积，则称该子集为 **好子集**（good subset）。  
返回 `nums` 中不同好子集的数量，对 `10^9 + 7` 取模（modulo）。

**子集**（subset）指可以通过删除 `nums` 中任意（可能为零或全部）元素得到的任意数组。只有当被删除的下标集合不同，两个子集才被视为不同。

---

### 示例

**示例 1**  
```text
Input: nums = [1,2,3,4]
Output: 6
Explanation: 好子集包括：
- [1,2]：乘积为 2，是不同质数 2 的乘积。
- [1,2,3]：乘积为 6，是不同质数 2 和 3 的乘积。
- [1,3]：乘积为 3，是不同质数 3 的乘积。
- [2]：乘积为 2，是不同质数 2 的乘积。
- [2,3]：乘积为 6，是不同质数 2 和 3 的乘积。
- [3]：乘积为 3，是不同质数 3 的乘积。
```

**示例 2**  
```text
Input: nums = [4,2,3,15]
Output: 5
Explanation: 好子集包括：
- [2]：乘积为 2，是不同质数 2 的乘积。
- [2,3]：乘积为 6，是不同质数 2 和 3 的乘积。
- [2,15]：乘积为 30，是不同质数 2、3 和 5 的乘积。
- [3]：乘积为 3，是不同质数 3 的乘积。
- [15]：乘积为 15，是不同质数 3 和 5 的乘积。
```

---

### 约束条件

- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 30`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **枚举所有子集**，把子集里的数相乘，判断这个乘积能否写成「若干个互不相同的质数」的乘积。

- **子集**：把数组 `nums` 看成一堆球，每个球可以**留下**也可以**丢掉**，所有留下/丢掉的方式就是子集。  
- **乘积检查**：把得到的乘积不断除以质数（2,3,5,…），如果最后只剩下 1，且除的每个质数只出现一次，则说明是“好子集”。  
- **哈希表**（字典）可以帮助我们快速记录每个质数出现的次数，就像查字典一样，`key` 是质数，`value` 是出现的次数。

**为什么正确**  
枚举把所有可能的子集都列出来，逐个验证。只要验证过程不出错，所有符合条件的子集都会被统计。

**时间/空间复杂度**  

- 枚举子集的数量是 `2^n`（每个元素有留下/丢掉两种选择），`n` 最多 10⁵，这已经是 **天文数字**，根本跑不完。  
- 对每个子集我们还要把所有元素相乘并做质因数分解，最坏情况下是 `O(n)`，所以整体时间是 `O(n * 2^n)`。  
- 空间只需要保存当前子集的乘积和质数计数，最多 `O(n)`（存放一个子集的所有元素），但因为时间已经不可能，这个解法只能当作“思考起点”。

> **大白话**：  
> `O(2^n)` 就好比让 30 个人每人选“是/否”，所有组合一共有 1 073 741 824 种，根本不可能手动列完。  

#### 代码（Python）

```python
from math import sqrt
from collections import Counter

MOD = 10**9 + 7
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]   # 30 以内的所有质数

def is_good(product: int) -> bool:
    """判断一个整数的质因数是否全互不相同（且只出现一次）。"""
    for p in primes:
        cnt = 0
        while product % p == 0:
            product //= p
            cnt += 1
        if cnt > 1:          # 同一个质数出现两次或以上，直接失败
            return False
    return product == 1    # 只剩 1，说明全部质因数都是互不相同的

def brute(nums):
    n = len(nums)
    ans = 0
    # 0~2^n-1 每一个二进制数对应一种子集的选/不选情况
    for mask in range(1, 1 << n):          # 空集不算
        prod = 1
        for i in range(n):
            if mask >> i & 1:              # 第 i 位为 1，说明选了 nums[i]
                prod *= nums[i]
        if is_good(prod):
            ans += 1
    return ans % MOD
```

> 这段代码 **只能在 n 很小（比如 ≤20）时跑得动**，用来帮助你理解最原始的思路。

#### 复杂度

- **时间复杂度**：`O(n * 2^n)` —— 每个子集都要遍历一次全部元素。  
- **空间复杂度**：`O(1)`（不计递归栈），因为只用常数个变量存放临时乘积。

---

### 2. 最优解

#### 思路  

暴力的瓶颈在于 **“枚举所有子集”**。我们要 **不枚举**，而是 **用状态压缩 + 动态规划** 把子集的计数直接算出来。

关键观察如下：

1. **元素范围很小**：`1 ≤ nums[i] ≤ 30`。所以所有可能的数只有 30 种，完全可以先统计每个数出现了多少次（哈希表），这一步类似“先把字典的词频做好”。  
2. **只能使用“无重复质因数”的数**  
   - 如果一个数本身含有 **平方因子**（如 4 = 2²、8 = 2³、9 = 3² …），那么它必然会把同一个质数出现两次，使得乘积不满足“互不相同”。  
   - 因此我们只保留 **square‑free**（无重复质因数）的数，其他直接丢弃。  
3. **用位掩码表示质数集合**  
   - 30 以内的质数有 10 个：`[2,3,5,7,11,13,17,19,23,29]`。  
   - 把每个数的质因数映射成 10 位的二进制掩码，`第 i 位为 1` 代表该数包含第 `i` 个质数。比如 `6 = 2·3` → `mask = 0b0000000011`。  
   - 这就像“每个质数是一个开关”，一个数对应的掩码告诉我们哪些开关被打开了。  
4. **动态规划的状态**  
   - `dp[mask]` 表示**选出若干个数后，已使用的质数集合恰好是 `mask` 的方案数。  
   - 初始时 `dp[0] = 1`（空集合的乘积为 1，暂不算进答案）。  
5. **转移**  
   - 对于每一个 **合法** 数 `x`（square‑free），记它的质数掩码为 `m`，出现次数为 `cnt[x]`。  
   - 选 `x` 的方式有 `cnt[x]` 种（任选它的哪一个下标），**但只能选一次**，因为再次选会导致同一质数出现两次。  
   - 为防止同一轮更新时重复使用 `x`，我们从大到小遍历已有的 `mask`，只在 `mask & m == 0`（不冲突）时进行转移：  
     ```
     new_mask = mask | m
     dp[new_mask] += dp[mask] * cnt[x]
     ```
6. **处理数字 1**  
   - `1` 本身不贡献任何质因数，乘以多少个 `1` 都不影响“互不相同”。  
   - 假设 `cnt1` 是 `1` 的出现次数，那么每个已经算好的好子集都可以再任选 `0~cnt1` 个 `1`，共计 `2^{cnt1}` 种扩展方式。  
   - 最后答案要乘以 `2^{cnt1}`（模运算下），再减去空集的计数。  
7. **求最终答案**  
   - 把所有 `mask != 0`（非空集合）的 `dp[mask]` 加起来，即得到不含 `1` 的好子集数。  
   - 再乘以 `2^{cnt1}`，得到包含任意个 `1` 的所有好子集。  

> **类比**：  
> 把每个质数想成一把钥匙，`mask` 表示已经用了哪些钥匙。我们要把钥匙装进盒子（子集），每次放入一个新数时，只能放进 **不冲突的钥匙**，否则盒子会“坏掉”。动态规划正是记录“已经装了哪些钥匙，有多少种装法”。

#### 代码（Python）

```python
from collections import Counter

MOD = 10**9 + 7

# 30 以内的所有质数，按顺序排好，后面会用下标来映射位
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
prime_to_bit = {p: i for i, p in enumerate(PRIMES)}   # 质数 → 位号

def prime_mask(x: int) -> int:
    """
    返回 x 的质因数掩码（仅在 x 为 square‑free 时使用）。
    若 x 含有重复质因数则返回 -1 表示“非法”。
    """
    mask = 0
    for p in PRIMES:
        if p * p > x:      # 已经超过 sqrt(x) 可以提前结束
            break
        cnt = 0
        while x % p == 0:
            x //= p
            cnt += 1
        if cnt > 1:        # 同一个质数出现两次，非法
            return -1
        if cnt == 1:       # 只出现一次，打开对应的位
            mask |= 1 << prime_to_bit[p]
    # 余下的 x 可能是 1 或者一个大于 sqrt(original) 的质数
    if x > 1:               # x 本身是质数
        # 仍然需要检查是否已经出现过（不可能，因为 x > sqrt(original)）
        mask |= 1 << prime_to_bit[x]
    return mask

def number_of_good_subsets(nums):
    cnt = Counter(nums)                 # 统计每个数出现的次数
    cnt1 = cnt.get(1, 0)                # 1 的出现次数

    # dp[mask]：已经使用的质数集合为 mask 的方案数（不含 1）
    dp = [0] * (1 << len(PRIMES))
    dp[0] = 1                           # 空集合的基准

    # 遍历所有可能的数字（除 1 之外），只处理 square‑free 的
    for num, freq in cnt.items():
        if num == 1:
            continue                    # 1 单独处理
        mask = prime_mask(num)
        if mask == -1:                  # 含有重复质因数，直接跳过
            continue

        # 为防止同一轮多次使用同一个数，从高到低遍历已有 mask
        for old_mask in range((1 << len(PRIMES)) - 1, -1, -1):
            if dp[old_mask] == 0:
                continue                # 没有这种状态，省略
            if old_mask & mask:        # 质数集合冲突，不能合并
                continue
            new_mask = old_mask | mask
            # 选取当前数字的任意一个下标，共有 freq 种方式
            dp[new_mask] = (dp[new_mask] + dp[old_mask] * freq) % MOD

    # 所有非空 mask 的方案数之和（此时不含 1）
    ans = sum(dp[mask] for mask in range(1, len(dp))) % MOD

    # 把 1 的任意组合加入进来（每个已有方案都可以乘以 2^{cnt1}）
    ans = ans * pow(2, cnt1, MOD) % MOD
    return ans

# ------------------- 示例 -------------------
if __name__ == "__main__":
    print(number_of_good_subsets([1,2,3,4]))          # 6
    print(number_of_good_subsets([4,2,3,15]))         # 5
```

**代码要点注释（中文）**  

- `prime_mask`：把一个数的质因数映射成位掩码；若出现平方因子返回 `-1`（表示该数永远不能出现在好子集）。  
- `dp[0] = 1`：空集合的计数为 1，后面会在求答案时排除它。  
- **倒序遍历** `old_mask`：确保同一次迭代里不会把同一个数字用两次（类似背包问题的“0/1”写法）。  
- `dp[old_mask] * freq`：从已有的方案里挑出一种，再从 `freq` 个相同数的下标里任选一个加入子集。  
- 最后乘 `2^{cnt1}`：每个好子集可以自由添加任意个 `1`（相当于把 `1` 当作“无影响的装饰品”）。

#### 复杂度

- **时间复杂度**：`O(N + 2^P * P)`  
  - `N` 是数组长度（最多 10⁵），用于统计出现次数。  
  - `P = 10` 是 30 以内的质数个数，`2^P = 1024`，遍历所有掩码的时间几乎可以忽略。整体约为线性 `O(N)`。  
- **空间复杂度**：`O(2^P)` ≈ 1024  
  - 只需要保存 `dp` 数组以及若干常数级的辅助结构。  

> 与暴力解相比，时间从指数级 (`2^n`) 降到了 **线性**，空间也从 `O(n)` 降到了常数级（1024），足以轻松通过所有测试。

---

## 心得

- **核心技巧**：**位掩码 + 子集动态规划**（又称“状态压缩 DP”）。  
- **适用题型**  
  1. 需要统计“互不冲突”元素子集的计数，如 **“不同的好子集”**、**“无重复质因数的子集”**。  
  2. **“选择若干个数，使得它们的某些属性不冲突”**，比如 **“最大不相交子集”**、**“按位或不重复的集合计数”**。  
- **一句话总结**：**把每个数的质因数看成一把钥匙，用位掩码记录已用的钥匙，DP 把“已经用了哪些钥匙”作为状态，一次遍历就能算出所有合法子集的数量。**

---

## 反思

- **第一反应**：看到“乘积可以表示为互不相同的质数的乘积”，立刻想到 **质因数分解**，于是想把每个数拆成质数后直接枚举子集。  
- **最容易踩的坑**  
  1. **平方因子**：忘记排除像 `4、8、9…` 这类含有重复质因数的数，会导致错误计数。  
  2. **1 的处理**：`1` 本身不贡献质因数，却可以任意加入子集，若不单独乘 `2^{cnt1}` 会少算很多方案。  
  3. **模运算**：在 DP 转移和最终乘 `2^{cnt1}` 时必须随时取模，否则中间乘积会溢出。  
- **下次类似题的第一步**：**先把元素映射成“是否冲突”的二进制状态**（位掩码），检查哪些元素是合法的（如 square‑free），再用 **状态压缩 DP** 统计符合条件的子集。这样可以把指数级的枚举压缩到仅与状态数（通常是 2^{质数个数}）成正比。