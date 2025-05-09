# #3179. 在 K 秒后求第 N 个值 / Find the N-th Value After K Seconds

> 难度：中等 · 标签：Array、Math、Simulation、Combinatorics、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/find-the-n-th-value-after-k-seconds/)

---

## 题目（英文原版）

**Description**

You are given two integers n and k.
Initially, you start with an array a of n integers where a[i] = 1 for all 0 <= i <= n - 1. After each second, you simultaneously update each element to be the sum of all its preceding elements plus the element itself. For example, after one second, a[0] remains the same, a[1] becomes a[0] + a[1], a[2] becomes a[0] + a[1] + a[2], and so on.
Return the value of a[n - 1] after k seconds.
Since the answer may be very large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: n = 4, k = 5
Output: 56
Explanation:
```

**Example 2:**

```
Input: n = 5, k = 3
Output: 35
Explanation:
```

**Constraints**

- 1 <= n, k <= 1000

---

## 题目（中文翻译）

**描述**  
给定两个整数 `n` 和 `k`。  
初始时，你有一个长度为 `n` 的数组 `a`，其中 `a[i] = 1`（`0 ≤ i ≤ n‑1`）。每经过一秒，所有元素同时更新为 **自身加上其所有前置元素之和**。例如，经过一秒后：

- `a[0]` 保持不变  
- `a[1]` 变为 `a[0] + a[1]`  
- `a[2]` 变为 `a[0] + a[1] + a[2]`  
- ……

返回 `k` 秒后 `a[n‑1]` 的值。由于答案可能非常大，返回其对 `10^9 + 7` 取模后的结果。

**示例**

**示例 1**  
```
Input: n = 4, k = 5
Output: 56
Explanation: 经过 5 秒后，数组演变为 [1, 5, 15, 56]，所以 a[3] = 56。
```

**示例 2**  
```
Input: n = 5, k = 3
Output: 35
Explanation: 经过 3 秒后，数组演变为 [1, 3, 6, 10, 35]，所以 a[4] = 35。
```

**约束条件**  
- `1 ≤ n, k ≤ 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**直接模拟**题目描述的过程：

1. 先建立一个长度为 `n` 的数组 `a`，所有元素都设为 `1`。  
2. 每过一秒，就把 `a` 同时更新为它的**前缀和**：  
   - `new_a[i] = a[0] + a[1] + … + a[i]`。  
   - 这里的“前缀和”可以想象成我们在一本字典里查词，查到第 `i` 个词时，需要把前面所有词的页码都加起来，得到一个累计的页码数。  
3. 重复第 2 步 `k` 次，最后返回 `a[n‑1]`。

为什么这个方法一定对？

- 题目说“**同时**更新每个元素”，这正好和我们一次性算出全部前缀和再整体覆盖原数组的过程一致。  
- 每一次的更新都完全遵循题目规则，所以 `k` 次后得到的 `a[n‑1]` 就是答案。

**复杂度分析**（大白话）：

- 每秒我们要遍历整个数组一次，计算前缀和，这相当于 **做 `n` 次加法**。  
- 要做 `k` 秒，就要 **做 `k` 轮**，所以总共要做 `n × k` 次加法。  
- 用 **大 O 记号** 写就是 `O(n·k)`，意思是时间会随 `n` 和 `k` 的乘积线性增长。  
- 我们只用到原数组和一个临时变量（保存当前前缀和），所以占用的额外空间是 **常数级**，记作 `O(1)`。

#### 代码（Python）

```python
MOD = 10**9 + 7

def nth_value_bruteforce(n: int, k: int) -> int:
    # 1. 初始化全 1 的数组
    a = [1] * n                     # a[i] = 1

    # 2. 重复 k 次前缀和更新
    for _ in range(k):
        prefix = 0                  # 用来累计前缀和
        for i in range(n):
            prefix = (prefix + a[i]) % MOD   # 加上当前元素并取模
            a[i] = prefix           # 同步写回 a[i]

    # 3. 返回最后一个元素
    return a[-1] % MOD
```

> **关键行注释**  
> - `prefix = (prefix + a[i]) % MOD`：相当于把字典里从第 0 页到第 `i` 页的页码全部加在一起，然后取模防止数字爆炸。  
> - `a[i] = prefix`：一次性把所有累计好的值写回原数组，保证“同步”更新。

#### 复杂度

- **时间复杂度**：`O(n·k)`  
  - 意味着如果 `n = 1000`、`k = 1000`，最多会执行约 `1,000,000` 次加法，完全可以在一秒内跑完。  
- **空间复杂度**：`O(1)`（不计输入数组本身）  
  - 只用了几个整数变量，和 `n、k` 的大小无关。

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于每秒都要遍历整个数组，虽然 `n·k ≤ 10⁶` 已经够快，但我们可以进一步把它压到 **只跟 `n` 或 `k` 中的较大者成线性**，甚至直接 `O(1)` 通过数学公式求解。

观察前几次的数组变化（`n = 5` 为例）：

| 秒数 | 数组 |
|------|------|
| 0    | `[1, 1, 1, 1, 1]` |
| 1    | `[1, 2, 3, 4, 5]` |
| 2    | `[1, 3, 6, 10, 15]` |
| 3    | `[1, 4, 10, 20, 35]` |

可以发现 **每个位置的数恰好是组合数**（二项式系数）：

\[
a_i^{(k)} = \binom{i+k}{k}
\]

- `i` 是下标（从 `0` 开始），`k` 是已经进行的秒数。  
- 组合数的意义：从 `i+k` 件物品里选 `k` 件的方式数，等价于 “把 `k` 次前缀和的累加过程展开后，每个原始的 `1` 被加了多少次”。  

**为什么会出现组合数？**  
把一次前缀和看成“把左边所有的 1 向右传播一次”。  
做 `k` 次前缀和，就相当于让每个原始的 `1` 向右传播 **恰好 `k` 步**，而要得到第 `i` 位的值，需要把所有能够到达 `i` 的传播路径计数。  
这正是 **“在 `i+k` 步中挑选 `k` 步向右走”** 的计数，亦即二项式系数。

所以我们只要**直接计算**：

\[
\text{answer} = \binom{n-1 + k}{k} \pmod{10^9+7}
\]

计算组合数的常用做法是 **阶乘 + 模逆**：

\[
\binom{N}{R} = \frac{N!}{R! (N-R)!}
\]

在模 `p = 10^9+7`（质数）下，除法可以用 **费马小定理**转化为乘以逆元：

\[
x^{-1} \equiv x^{p-2} \pmod{p}
\]

于是只需要预先算出 `0 … N` 的阶乘和阶乘的逆元，时间复杂度 `O(N)`，这里 `N = n + k`，最多 `2000`，几乎瞬间完成。

#### 代码（Python）

```python
MOD = 10**9 + 7

def mod_pow(a: int, e: int) -> int:
    """快速幂：计算 a^e % MOD，时间 O(log e)"""
    res = 1
    while e:
        if e & 1:
            res = (res * a) % MOD
        a = (a * a) % MOD
        e >>= 1
    return res

def prepare_factorials(limit: int):
    """预计算 0..limit 的阶乘和逆元阶乘"""
    fact = [1] * (limit + 1)
    for i in range(1, limit + 1):
        fact[i] = (fact[i-1] * i) % MOD

    inv_fact = [1] * (limit + 1)
    # inv_fact[limit] = (fact[limit])^(MOD-2) % MOD
    inv_fact[limit] = mod_pow(fact[limit], MOD - 2)
    for i in range(limit, 0, -1):
        inv_fact[i-1] = (inv_fact[i] * i) % MOD   # 逆推得到前一个

    return fact, inv_fact

def nth_value_optimal(n: int, k: int) -> int:
    # 需要的最大 N = n-1 + k
    N = n - 1 + k
    fact, inv_fact = prepare_factorials(N)

    # 组合数 C(N, k) = fact[N] * inv_fact[k] * inv_fact[N-k] % MOD
    ans = fact[N]
    ans = (ans * inv_fact[k]) % MOD
    ans = (ans * inv_fact[N - k]) % MOD
    return ans
```

> **关键行解释**  
> - `mod_pow`：相当于“快速乘法器”，把大幂次的乘法拆成二进制位的若干次乘，时间只有 `log e`。  
> - `prepare_factorials`：把“把 1·2·…·i”这一步提前算好，后面直接查表。逆元的倒推（`inv_fact[i-1] = inv_fact[i] * i`）就像把字典的页码倒着算，省去每次重新求逆的成本。  
> - `ans = fact[N] * inv_fact[k] * inv_fact[N-k] % MOD`：直接套用组合数公式，得到答案。

#### 复杂度

- **时间复杂度**：`O(n + k)`（实际上是 `O(N)`，`N = n + k`）  
  - 与暴力的 `O(n·k)` 相比，大幅降低。当 `n = k = 1000` 时，只有约 `2000` 次乘法和取模。  
- **空间复杂度**：`O(n + k)` 用于存放阶乘和逆元数组。  
  - 只需要 `2001` 个整数，几乎可以忽略不计。

---

## 心得

- **核心技巧**：**重复前缀和等价于二项式系数**。把“每秒把左边的所有数加到自己”视作“向右传播”，次数的组合即为组合数。  
- **适用的题型**  
  1. “多次前缀和 / 累计求和” 类问题（如 LeetCode 1484、1460）。  
  2. “把 1 通过若干次操作分配到不同位置” 的计数题（如分配硬币、递增序列计数）。  
  3. “在格子上向右/向下走 k 步后到达某点” 的组合计数（典型的路径计数）。  
- **一句话总结**：**把连续的前缀和转化为二项式系数，直接用组合数公式求解**。

---

## 反思

- **第一反应**：看到“每秒都把前缀和”，自然想到直接模拟（暴力）——最安全的起点。  
- **最容易踩的坑**  
  - **取模时的负数**：在 Python 中 `% MOD` 已经保证非负，但手写语言时要注意。  
  - **组合数的逆元**：如果忘记使用费马小定理或逆元预处理，直接除法会出错。  
  - **边界情况**：`k = 0` 时答案应是 `1`（因为数组全是 1），公式 `C(n-1,0)=1` 仍然成立；`n = 1` 时也是 `1`，同样符合公式。  
- **下次类似题的第一步**：**先判断是否可以把多次累计操作抽象为组合数或其他数学闭式**，如果可以，就直接用公式；否则再考虑 DP/模拟。