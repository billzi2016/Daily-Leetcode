# #3395. 唯一中位众数的子序列 I / Subsequences with a Unique Middle Mode I

> 难度：困难 · 标签：Array、Hash Table、Math、Combinatorics · [LeetCode 链接](https://leetcode.com/problems/subsequences-with-a-unique-middle-mode-i/)

---

## 题目（英文原版）

**Description**

Given an integer array nums, find the number of subsequences of size 5 of nums with a unique middle mode.
Since the answer may be very large, return it modulo 109 + 7.
A mode of a sequence of numbers is defined as the element that appears the maximum number of times in the sequence.
A sequence of numbers contains a unique mode if it has only one mode.
A sequence of numbers seq of size 5 contains a unique middle mode if the middle element (seq[2]) is a unique mode.

**Examples**

**Example 1:**

```
Input: nums = [1,1,1,1,1,1]
Output: 6
Explanation:
[1, 1, 1, 1, 1] is the only subsequence of size 5 that can be formed, and it has a unique middle mode of 1. This subsequence can be formed in 6 different ways, so the output is 6.
```

**Example 2:**

```
Input: nums = [1,2,2,3,3,4]
Output: 4
Explanation:
[1, 2, 2, 3, 4] and [1, 2, 3, 3, 4] each have a unique middle mode because the number at index 2 has the greatest frequency in the subsequence. [1, 2, 2, 3, 3] does not have a unique middle mode because 2 and 3 appear twice.
```

**Example 3:**

```
Input: nums = [0,1,2,3,4,5,6,7,8]
Output: 0
Explanation:
There is no subsequence of length 5 with a unique middle mode.
```

**Constraints**

- 5 <= nums.length <= 1000
- -109 <= nums[i] <= 109

---

## 题目（中文翻译）

给定一个整数数组 `nums`，求 `nums` 中所有长度为 5 的子序列（subsequence）中，满足 **唯一中位众数** 的子序列数量。由于答案可能非常大，请返回答案对 `10^9 + 7` 取模后的结果。  

**定义**  
- 一个序列的 **众数**（mode）指在该序列中出现次数最多的元素。  
- 若一个序列只有唯一的众数，则称该序列 **具有唯一众数**。  
- 长度为 5 的序列 `seq` 若其中的中间元素 `seq[2]` 是唯一众数，则称该序列 **具有唯一中位众数**。  

**示例**  

**示例 1**  
```
Input: nums = [1,1,1,1,1,1]
Output: 6
Explanation:
[1, 1, 1, 1, 1] 是唯一可以形成的长度为 5 的子序列，并且其中的中位元素 1 是唯一众数。该子序列可以通过 6 种不同的方式选取，因此输出 6。
```

**示例 2**  
```
Input: nums = [1,2,2,3,3,4]
Output: 4
Explanation:
[1, 2, 2, 3, 4] 和 [1, 2, 3, 3, 4] 均拥有唯一中位众数，因为下标为 2 的元素在子序列中出现次数最多。子序列 [1, 2, 2, 3, 3] 则没有唯一中位众数，因为 2 和 3 各出现两次。
```

**示例 3**  
```
Input: nums = [0,1,2,3,4,5,6,7,8]
Output: 0
Explanation:
不存在长度为 5 且具有唯一中位众数的子序列。
```

**约束条件**  

- `5 <= nums.length <= 1000`  
- `-10^9 <= nums[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把 **所有** 长度为 `5` 的下标组合枚举出来，检查每个子序列的中间元素 `seq[2]` 是否是唯一的众数（出现次数最多且只有一个）。  

- **枚举**：在长度为 `n` 的数组里，任选 `5` 个下标，要求严格递增 `i1 < i2 < i3 < i4 < i5`。  
- **检查**：统计这 5 个数里每个数出现了多少次，找出出现次数最大的那个。如果只有一个数的出现次数是最大值，而且它恰好位于下标 `i3`（即是中间元素），就算合法。  

> **类比**：把数组想象成一本书的每一页都有一个数字。暴力做法就是把所有可能的 5 页组合翻出来，逐页数数，看第 3 页的数字是不是这 5 页里出现次数最多且唯一的。

**为什么正确**  
因为我们把**所有**可能的子序列都遍历了一遍，只要符合题目定义的「唯一中间众数」就一定会被统计到，所以答案一定是完整的。

**复杂度**  
- 枚举所有 5‑元组的数量是 `C(n,5) ≈ n⁵ / 120`，在最坏情况下要检查约 `10¹⁵`（`n=1000`）个组合，根本不可行。  
- 时间复杂度记作 `O(n⁵)`，这里的 “⁵” 表示“每次都要遍历 5 层循环”。  
- 只用了常数级的额外空间，空间复杂度是 `O(1)`。

> **大白话**：`O(n⁵)` 就像让 1000 个人排成 5 行，每行选一个人——组合的数量天文级别，根本等不到答案。

---

### 2. 最优解

#### 思路  

因为子序列的长度 **固定为 5**，我们可以把注意力放在 **中间的那个位置** 上。  
设下标 `i` 为子序列的第三个元素（即中间元素），我们只需要统计：

> **有多少种办法**，在 `i` 左侧挑选 **2** 个下标，在 `i` 右侧挑选 **2** 个下标，使得  
> `nums[i]` 的出现次数严格大于其它任何数的出现次数。

把问题拆成两部分：

1. **左侧、右侧各选 2 个元素的组合数**（只关心是否等于 `nums[i]`，不管具体值是什么）。  
2. **满足“唯一中间众数” 的额外约束**。  
   - 当 `nums[i]` 在子序列里出现 **≥ 3 次** 时，其他数的出现次数最多为 2，必然不可能和 `nums[i]` 打平，约束自然满足。  
   - 当 `nums[i]` 只出现 **2 次**（即左/右各恰好出现一次或左侧出现一次右侧不出现，反之亦然）时，**其余的 3 个数必须互不相同**，否则会出现其他数出现 2 次与 `nums[i]` 打平，导致不是唯一众数。

下面一步步推导如何高效计数。

---

#### 2.1 统计左/右两侧「恰好 k 个等于中间值」的组合数  

设 `val = nums[i]`。  
- `L = i` 为 `i` 左侧元素个数，`R = n - i - 1` 为右侧元素个数。  
- `cntL =` 左侧等于 `val` 的个数，`cntR =` 右侧等于 `val` 的个数。  

从左侧挑选 2 个下标，使其中恰好有 `k`（`k = 0,1,2`）个等于 `val` 的方式数为  

\[
L_i[k] = \binom{cntL}{k}\times\binom{L-cntL}{2-k}
\]

右侧同理  

\[
R_i[k] = \binom{cntR}{k}\times\binom{R-cntR}{2-k}
\]

这里的组合数 `C(n, k)` 用 **预计算的阶乘+逆元** 在 `O(1)` 时间求得，模 `M = 10^9+7`。

---

#### 2.2 处理出现次数 ≥ 3 的情况  

只要 `kL + kR ≥ 2`（即 `val` 在子序列里出现 ≥ 3 次），**任意**挑选的其余元素都不会与 `val` 打平。  

贡献为  

\[
\text{ans}_{\ge 3} = \sum_{kL=0}^{2}\sum_{kR=0}^{2}
\mathbf{1}_{kL+kR\ge 2}\; L_i[kL]\times R_i[kR]
\]

---

#### 2.3 处理出现次数 = 2 的情况（关键难点）  

此时 `kL + kR = 1`，即 `val` 只出现一次在左侧或右侧。  
我们把两种对称的情形分别计数：

* **情形 A**：左侧出现一次 `val`（`kL=1, kR=0`）  
  - 左侧还需要再挑 **1** 个非 `val` 元素（记为 `x`）。  
  - 右侧需要挑 **2** 个非 `val` 元素（记为 `y, z`），且 `x, y, z` 必须 **三者互不相同**。  

* **情形 B**：右侧出现一次 `val`（`kL=0, kR=1`）  
  - 对称处理。

下面只说明情形 A，情形 B 同理。

**记号**  

- `L0 = L - cntL` 为左侧 **非 `val`** 的个数。  
- `R0 = R - cntR` 为右侧 **非 `val`** 的个数。  
- `freqL[w]` / `freqR[w]` 为左/右侧每个数 `w (≠ val)` 出现的次数。  

**步骤 1 – 选左侧的非 `val` 元素**  

我们遍历左侧所有不同的数 `w ≠ val`，  
- 选中 `w` 的方式有 `freqL[w]` 种（任选一个下标）。  

**步骤 2 – 在右侧挑选两个互不相同且都不等于 `w` 的元素**  

右侧所有非 `val` 元素的总数 `R0`，其中每个数 `u` 出现 `freqR[u]` 次。  
先算出右侧 **任意** 两个非 `val` 元素的 unordered pair 数：

\[
\text{totalPairs}_R = \binom{R0}{2}
\]

再算出 **相同数值的 pair**（会导致重复）：

\[
\text{samePairs}_R = \sum_{u\neq val}\binom{freqR[u]}{2}
\]

于是 **值互不相同的 pair** 为  

\[
\text{diffPairs}_R = \text{totalPairs}_R - \text{samePairs}_R
\]

但是我们还要 **排除** 那些包含数值 `w` 的 pair。  
包含 `w` 的 unordered pair 有两种：

* 两个都是 `w` → `\binom{freqR[w]}{2}`
* 一个是 `w`，另一个是其他数 → `freqR[w]\times(R0-freqR[w])`

两者之和正好是  

\[
\text{pairsWith}_w = freqR[w]\times(R0-freqR[w]) + \binom{freqR[w]}{2}
\]

所以 **右侧两数既互不相同又不等于 `w`** 的合法 pair 数为  

\[
\text{goodPairs}_R(w)=\text{diffPairs}_R-\text{pairsWith}_w
                =\text{totalPairs}_R-\text{samePairs}_R-freqR[w]\times(R0-freqR[w])
\]

（上式中已经把 `\binom{freqR[w]}{2}` 从 `samePairs_R` 中扣掉了）

**步骤 3 – 累加贡献**  

情形 A 的贡献为  

\[
\begin{aligned}
\text{ans}_A &= L_i[1]\times\Bigg(
    \sum_{w\neq val} freqL[w]\times\text{goodPairs}_R(w)
\Bigg)
\end{aligned}
\]

情形 B 类似，只需把「左」↔「右」对调。

**整体答案**  

\[
\text{ans}= \text{ans}_{\ge 3}+ \text{ans}_A + \text{ans}_B \pmod{M}
\]

---

#### 2.4 实现细节  

| 步骤 | 关键实现 |
|------|----------|
| **预计算组合数** | 用 `fact[i]`、`inv_fact[i]`（模逆）在 `O(n)` 预处理，`C(n,k)=fact[n]*inv_fact[k]*inv_fact[n-k] % M` |
| **遍历中间位置** | 从左到右维护两个哈希表 `left_cnt`、`right_cnt`（一开始 `right_cnt` 为全数组的频率） |
| **更新右侧计数** | 进入循环时先把 `nums[i]` 从 `right_cnt` 中减 1（因为它是中间元素，不属于右侧） |
| **得到 `cntL, cntR`** | `cntL = left_cnt.get(val,0)`，`cntR = right_cnt.get(val,0)` |
| **计算 `L_i[k]、R_i[k]`** | 直接套用组合数公式，若参数不合法返回 0 |
| **统计非 `val` 的频率** | `left_non = {k:v for k,v in left_cnt.items() if k!=val}`，同理 `right_non` |
| **求 `totalPairs`、`samePairs`** | `totalPairs = C(R0,2)`，`samePairs = sum(C(v,2) for v in right_non.values())`（左侧同理） |
| **遍历 `w` 累加** | 对每个 `w` 读取 `freqL[w]`、`freqR[w]`，用上面的公式算 `goodPairs_R(w)`，累加 `freqL[w]*goodPairs_R(w)`（情形 A） |
| **对称情形 B** | 同理，只是把「左」↔「右」换位 |
| **移动指针** | 循环结束后把 `nums[i]` 加入 `left_cnt`，准备下一个 `i` |

时间复杂度  
- 主循环 `i = 0 … n-1` → `O(n)`  
- 每次循环内部遍历一次 **左侧不同值**（或右侧），最坏 `O(n)`  
- 所以总时间 `O(n²)`，在 `n ≤ 1000` 时约 `10⁶` 次操作，轻松通过。

空间复杂度  
- 两个哈希表保存出现次数，最多存 `O(n)` 个不同数值 → `O(n)` 额外空间。

---

#### 代码（Python）

```python
MOD = 10 ** 9 + 7

# ---------- 组合数预处理 ----------
def prepare_combinations(N: int):
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (N + 1)
    inv_fact[N] = pow(fact[N], MOD - 2, MOD)          # Fermat 逆元
    for i in range(N, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD
    return fact, inv_fact

def C(n: int, k: int, fact, inv_fact) -> int:
    if k < 0 or k > n:
        return 0
    return fact[n] * inv_fact[k] % MOD * inv_fact[n - k] % MOD

# ---------- 主函数 ----------
def countUniqueMiddleMode(nums):
    n = len(nums)
    fact, inv_fact = prepare_combinations(n)

    # 右侧频率初始化为整个数组的计数
    from collections import Counter
    right_cnt = Counter(nums)
    left_cnt = Counter()

    ans = 0

    for i, val in enumerate(nums):
        # 1) 当前元素不算在右侧
        right_cnt[val] -= 1
        if right_cnt[val] == 0:
            del right_cnt[val]

        L = i                     # 左侧元素个数
        R = n - i - 1             # 右侧元素个数
        cntL = left_cnt.get(val, 0)
        cntR = right_cnt.get(val, 0)

        # ---------- 2) 计算 L_i[k] 与 R_i[k] ----------
        Li = [0, 0, 0]   # k = 0,1,2
        Ri = [0, 0, 0]
        for k in range(3):
            Li[k] = C(cntL, k, fact, inv_fact) * C(L - cntL, 2 - k, fact, inv_fact) % MOD
            Ri[k] = C(cntR, k, fact, inv_fact) * C(R - cntR, 2 - k, fact, inv_fact) % MOD

        # ---------- 3) 出现次数 >= 3 ----------
        for kL in range(3):
            for kR in range(3):
                if kL + kR >= 2:          # val 出现 3 次或以上
                    ans = (ans + Li[kL] * Ri[kR]) % MOD

        # ---------- 4) 出现次数 = 2 的两种情形 ----------
        # 先准备非 val 的频率表
        left_non = {k: v for k, v in left_cnt.items() if k != val}
        right_non = {k: v for k, v in right_cnt.items() if k != val}

        # ---- 辅助函数：右侧（或左侧）统计 ----
        def prepare_side(non_dict, total_non):
            """返回 totalPairs, samePairs, freq dict"""
            total_pairs = C(total_non, 2, fact, inv_fact)
            same_pairs = 0
            for c in non_dict.values():
                same_pairs = (same_pairs + C(c, 2, fact, inv_fact)) % MOD
            return total_pairs, same_pairs

        # ---- 情形 A：左侧出现一次 val (kL=1, kR=0) ----
        if Li[1] and R >= 2:          # 右侧至少需要两个位置
            total_pairs_R, same_pairs_R = prepare_side(right_non, R - cntR)
            # 对每个左侧不同值 w 计算贡献
            contrib_A = 0
            for w, cntLw in left_non.items():
                cntRw = right_non.get(w, 0)
                # goodPairs_R(w) = totalPairs_R - samePairs_R - cntRw * (R0 - cntRw)
                bad = cntRw * ((R - cntR) - cntRw) % MOD
                good = (total_pairs_R - same_pairs_R - bad) % MOD
                contrib_A = (contrib_A + cntLw * good) % MOD
            ans = (ans + Li[1] * contrib_A) % MOD

        # ---- 情形 B：右侧出现一次 val (kL=0, kR=1) ----
        if Ri[1] and L >= 2:
            total_pairs_L, same_pairs_L = prepare_side(left_non, L - cntL)
            contrib_B = 0
            for w, cntRw in right_non.items():
                cntLw = left_non.get(w, 0)
                bad = cntLw * ((L - cntL) - cntLw) % MOD
                good = (total_pairs_L - same_pairs_L - bad) % MOD
                contrib_B = (contrib_B + cntRw * good) % MOD
            ans = (ans + Ri[1] * contrib_B) % MOD

        # 5) 将当前元素加入左侧，进入下一个 i
        left_cnt[val] = left_cnt.get(val, 0) + 1

    return ans % MOD

# ---------- 示例 ----------
if __name__ == "__main__":
    print(countUniqueMiddleMode([1,1,1,1,1,1]))            # 6
    print(countUniqueMiddleMode([1,2,2,3,3,4]))          # 4
    print(countUniqueMiddleMode([0,1,2,3,4,5,6,7,8]))    # 0
```

> **代码要点说明**  
> - `prepare_combinations` 只需要算到 `n`（≤1000），所以非常快。  
> - `C(n,k)` 自动返回 0 当 `k` 超出范围，省去繁琐的边界判断。  
> - `left_non`、`right_non` 每次循环只复制一次哈希表的视图，复杂度仍是 `O(distinct)`。  
> - 所有乘法、加法都取模，防止整数溢出。

---

## 心得

- **核心技巧**：把固定长度子序列的“中间位置”固定下来，转化为左/右各挑 2 个元素的组合计数。  
- **适用题型**  
  1. “固定长度子序列 + 某个位置必须满足特殊计数”——如 “长度为 4，左侧元素必须全部不同”。  
  2. “出现次数比较” 类题，如 “找出出现次数最多且唯一的元素”。  
- **一句话总结**：**把问题拆成“中间元素出现次数”和“其余元素的相互关系”，分别用组合计数和排除重复的技巧解决**。

---

## 反思

- **第一反应**：直接枚举所有长度为 5 的子序列——虽然思路最直观，却忘记了 `n` 达到 1000 时组合数会爆炸。  
- **最容易踩的坑**  
  - **忽视 “唯一” 的要求**：只保证中间元素出现次数最多，却忘记排除出现次数相同的其他元素。  
  - **边界条件**：左侧或右侧不足 2 个位置时要直接返回 0，防止组合数负数。  
  - **模运算的负数**：在 `good = (total_pairs - same_pairs - bad) % MOD` 时一定要加上 `MOD` 再取模，防止 Python 的负数取模得到负值。  
- **下次类似题的第一步**：**先固定住“关键位置”（比如中间元素、最大值所在位置），把全局计数问题转化为两侧的独立计数，再检查是否有额外的唯一性或不相等约束**。这样往往能把指数级搜索压到多项式级。