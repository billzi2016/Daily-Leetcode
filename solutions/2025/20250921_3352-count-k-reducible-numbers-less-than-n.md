# #3352. 统计小于 N 的 K 可约数 / Count K-Reducible Numbers Less Than N

> 难度：困难 · 标签：Math、String、Dynamic Programming、Combinatorics · [LeetCode 链接](https://leetcode.com/problems/count-k-reducible-numbers-less-than-n/)

---

## 题目（英文原版）

**Description**

You are given a binary string s representing a number n in its binary form.
You are also given an integer k.
An integer x is called k-reducible if performing the following operation at most k times reduces it to 1:
For example, the binary representation of 6 is "110". Applying the operation once reduces it to 2 (since "110" has two set bits). Applying the operation again to 2 (binary "10") reduces it to 1 (since "10" has one set bit).
Return an integer denoting the number of positive integers less than n that are k-reducible.
Since the answer may be too large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: s = "111", k = 1
Output: 3
Explanation:
n = 7 . The 1-reducible integers less than 7 are 1, 2, and 4.
```

**Example 2:**

```
Input: s = "1000", k = 2
Output: 6
Explanation:
n = 8 . The 2-reducible integers less than 8 are 1, 2, 3, 4, 5, and 6.
```

**Example 3:**

```
Input: s = "1", k = 3
Output: 0
Explanation:
There are no positive integers less than n = 1 , so the answer is 0.
```

**Constraints**

- 1 <= s.length <= 800
- s has no leading zeros.
- s consists only of the characters '0' and '1'.
- 1 <= k <= 5

---

## 题目（中文翻译）

给定一个二进制字符串（binary string） `s`，它表示整数 `n` 的二进制形式。  
同时给定一个整数 `k`。  

如果对一个整数 `x` 至多执行 `k` 次以下操作后能够得到 `1`，则称该整数是 **k‑可约数**（k‑reducible）：

- 将 `x` 的二进制表示中“1”的个数（即**置位**（set bits））记为 `cnt`，把 `x` 替换为 `cnt`。

例如，整数 `6` 的二进制为 `"110"`。第一次操作后得到 `2`（因为 `"110"` 中有两个置位）。再次对 `2`（二进制 `"10"`）操作得到 `1`（因为只有一个置位）。

返回小于 `n` 的正整数中 **k‑可约数** 的数量。由于答案可能非常大，请返回其对 `10^9 + 7` 取模后的结果。

**示例 1**  
**示例 2**  
**示例 3**  

**约束条件**  
- `1 <= s.length <= 800`  
- `s` 没有前导零  
- `s` 仅由字符 `'0'` 和 `'1'` 组成  
- `1 <= k <= 5`  

**示例**  

**示例 1:**  
```
Input: s = "111", k = 1
Output: 3
Explanation:
n = 7 。小于 7 的 1‑可约数为 1、2、4。
```

**示例 2:**  
```
Input: s = "1000", k = 2
Output: 6
Explanation:
n = 8 。小于 8 的 2‑可约数为 1、2、3、4、5、6。
```

**示例 3:**  
```
Input: s = "1", k = 3
Output: 0
Explanation:
不存在小于 n = 1 的正整数，所以答案为 0。
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把所有 **小于 n** 的正整数逐个枚举出来，检查它们能否在至多 `k` 次操作后变成 `1`。

- **枚举**：从 `1` 开始遍历到 `n-1`（`n` 用二进制字符串 `s` 表示），每遍历到一个数 `x`，就模拟题目给出的“取二进制中 `1` 的个数”这个操作。
- **模拟**：把 `x` 变成 `popcount(x)`（即二进制里 `1` 的个数），再对得到的结果继续做同样的操作，直到变成 `1` 或者已经用了 `k` 次。只要在 `k` 次之内成功变成 `1`，就把它计数。

> **类比**：把 `popcount` 想成“数数器”，每次把数字压缩成它的 `1` 的数量。对每个数字我们不停地把它塞进这个数数器，最多 `k` 次。

**为什么能得到正确答案**  
因为我们把 **所有** 小于 `n` 的正整数都检查了一遍，凡是满足题意的自然会被计数，凡是不满足的自然不会计数。

**时间/空间复杂度**  

- **时间**：对每个 `x`（最多 `n-1` 个），最多要做 `k ≤ 5` 次 `popcount`，每次 `popcount` 本身是 `O(log x)`（二进制位数）。所以总体是  
  \[
  O\big((n-1)\cdot k \cdot \log n\big)\approx O(n\log n)
  \]
  当 `n` 很大（题目里 `s` 长度可达 800，即 `n` 可能是 $2^{800}$）时，这根本不可行。

- **空间**：只用了常数个变量，`O(1)`。

> **大白话**：`O(n log n)` 就像让你把一整座城市的每栋楼都跑一遍马拉松，显然不可能在合理时间完成。

---

#### 代码（Python）

```python
def popcount(x: int) -> int:
    """返回 x 的二进制表示里 1 的个数"""
    return bin(x).count('1')


def steps_to_one(x: int, k: int) -> bool:
    """判断 x 是否能在至多 k 次 popcount 操作后变成 1"""
    cnt = 0
    while x != 1 and cnt < k:
        x = popcount(x)
        cnt += 1
    return x == 1


def brute(s: str, k: int) -> int:
    MOD = 10 ** 9 + 7
    n = int(s, 2)                 # 把二进制字符串转成整数
    ans = 0
    for x in range(1, n):         # 枚举 1 .. n-1
        if steps_to_one(x, k):
            ans = (ans + 1) % MOD
    return ans
```

> 这段代码在 `s` 长度很小（比如 ≤20）时能跑通，作为“暴力”参考即可。

#### 复杂度

- **时间复杂度**：`O(n log n)` —— `n` 可能是 $2^{800}$，根本不可接受。  
- **空间复杂度**：`O(1)` —— 只用了常数级别的临时变量。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **枚举所有数字**。我们需要一种方式 **不逐个遍历**，而是直接统计满足条件的数字个数。这里可以借助 **数位 DP（Digit DP）**：在遍历二进制位的过程中，动态记录已经出现了多少个 `1`，最后只要判断这个“出现的 `1` 的总数”是否满足 “k‑可约” 的条件即可。

关键观察如下：

1. **操作只依赖于 “1 的个数”**  
   对任意正整数 `x`，第一次操作把 `x` 变成 `popcount(x)`，之后的所有操作只和 `popcount(x)` 的 **1 的个数** 有关。换句话说，`x` 的具体二进制形状不重要，只要知道它的 **总 `1` 的数量** 就可以继续判断。

2. **递归计算 “从某个数到 1 需要的最少操作次数”**  
   定义 `g[t]` 为把数 `t`（`t ≥ 1`）化成 `1` 所需要的最少操作次数（不计入 `t` 本身）。  
   - `g[1] = 0`（已经是 1，不需要操作）  
   - 对其它 `t`，第一次操作把它变成 `popcount(t)`，于是  
     \[
     g[t] = 1 + g[\text{popcount}(t)]
     \]
   因为 `popcount(t) ≤ \log_2 t + 1`，递归深度非常小（`k ≤ 5`），我们可以 **预计算** 所有 `t` 在 `[1, 800]`（二进制位数上限）范围内的 `g[t]`。

3. **把 “k‑可约” 条件转换为 “popcount 在某个集合中”**  
   对于任意 `x > 1`，总操作次数 = `1 + g[popcount(x)]`。要让它 ≤ `k`，等价于  
   \[
   g[\text{popcount}(x)] \le k-1
   \]
   因此，只要 **`popcount(x)` 落在集合**  
   \[
   S = \{\, t \mid g[t] \le k-1 \,\}
   \]
   那么 `x` 就是 **k‑可约**。  
   `x = 1` 是特殊情况：它的操作次数是 `0`，自然满足所有 `k ≥ 0`，而 `popcount(1) = 1`，而 `g[1]=0`，同样在集合 `S` 中。

4. **数位 DP**  
   - **状态**：`dp[pos][cnt][tight]`  
     - `pos`：当前处理到的二进制位（从最高位到最低位），范围 `0 … L`（`L = len(s)`）。  
     - `cnt`：截至当前位已经出现的 `1` 的个数。最大不超过 `L`（≤800）。  
     - `tight`：前缀是否已经严格小于 `s` 的前缀。`tight = 1` 表示前面已经小于 `s`，后面的位可以随意取 `0/1`；`tight = 0` 表示前缀完全等于 `s`，当前位只能取不超过 `s[pos]`。  
   - **转移**：遍历当前位可以放 `0` 还是 `1`（受 `tight` 限制），更新 `cnt` 与 `tight`。  
   - **结束**：遍历完所有位后得到的 `cnt` 就是整数字的 `popcount`。如果 `cnt ∈ S` 且数字不为 `0`，就计入答案。  
   - **排除 0**：DP 会把全 0 的情况也算进去，需要在最后减去 1（因为 `0` 不是正整数），或者在转移时避免计数。

5. **取模**  
   题目要求对 $10^9+7$ 取模，所有加法都在模数下进行。

> **类比**：把二进制字符串看成一条走廊，`pos` 是你现在站在第几格，`cnt` 是你手里已经收集的 “钥匙”（`1` 的数量），`tight` 决定你是否已经走到比原始走廊更靠前的分支。走完整条走廊后，只要手里钥匙的数量在 “合格钥匙集合 `S`” 里，就算成功。

#### 代码（Python）

```python
MOD = 10 ** 9 + 7

def precompute_g(limit: int) -> list[int]:
    """
    计算 g[t]：把正整数 t 通过若干次 popcount 操作变成 1 所需的最少次数。
    limit 为我们需要的最大 t（这里等于二进制位数上限 800）。
    """
    g = [0] * (limit + 1)          # g[0] 暂时不使用
    g[1] = 0                       # 1 本身不需要操作
    for t in range(2, limit + 1):
        # 递归公式：先做一次 popcount，然后再看剩下的次数
        pc = bin(t).count('1')
        g[t] = 1 + g[pc]
    return g


def count_k_reducible(s: str, k: int) -> int:
    """
    主函数：返回二进制字符串 s 表示的 n 之下，k‑可约正整数的个数（模 1e9+7）。
    """
    L = len(s)                     # 二进制位数
    g = precompute_g(L)            # 只需要到 L，因为 popcount 最大不超过 L

    # 计算集合 S = { t | g[t] <= k-1 }
    # 注意：k >= 1，k-1 可能为 0，g[1] = 0 总是满足
    good = [False] * (L + 1)
    for t in range(1, L + 1):
        if g[t] <= k - 1:
            good[t] = True

    from functools import lru_cache

    @lru_cache(maxsize=None)
    def dp(pos: int, cnt: int, tight: int) -> int:
        """
        返回从第 pos 位（0 为最高位）开始往后，
        已经累计了 cnt 个 1，且 tight 标记当前前缀是否已经小于 s 的前缀，
        能得到的满足条件的数的个数（模 MOD）。
        """
        if pos == L:               # 已经走完所有位
            # cnt 是整数字的 popcount
            # 必须是正整数（即 cnt>0）且 cnt 落在 good 集合中
            return 1 if (cnt > 0 and good[cnt]) else 0

        limit_bit = int(s[pos]) if tight == 0 else 1   # 受 tight 限制的最大可放置的位
        total = 0
        for bit in (0, 1):
            if bit > limit_bit:
                continue
            new_tight = tight
            if tight == 0:
                if bit < limit_bit:
                    new_tight = 1          # 现在已经小于 s 的前缀
                else:
                    new_tight = 0          # 仍然和 s 前缀相等
            # 更新 1 的计数
            total += dp(pos + 1, cnt + bit, new_tight)
            if total >= MOD:
                total -= MOD
        return total

    # 从最高位开始，累计的 1 的数量为 0，tight = 0（尚未小于 s）
    ans = dp(0, 0, 0)

    # DP 中已经排除了全 0 的情况（cnt==0 时不算），所以不需要额外减去 0。
    return ans % MOD
```

**代码说明（关键行注释）**

| 行号（大致） | 解释 |
|--------------|------|
| `precompute_g` | 先把所有可能的 `popcount`（最多 `L`）对应的最少操作次数算出来。递归公式 `g[t] = 1 + g[popcount(t)]`。 |
| `good[t] = True` | 把满足 `g[t] ≤ k-1` 的 `t` 标记为 “好”，后面只要 `popcount` 落在这些 `t` 里就算 k‑可约。 |
| `dp(pos, cnt, tight)` | 典型的数位 DP：`pos` 是当前处理的位，`cnt` 累计的 `1` 的个数，`tight` 表示前缀是否已经小于 `s`。 |
| `if pos == L` | 所有位都决定完了，此时 `cnt` 就是整数字的 `popcount`，检查它是否在 `good` 集合且不是 0。 |
| `limit_bit = int(s[pos]) if tight == 0 else 1` | 当前位受 `tight` 约束时只能取 `0…limit_bit`。 |
| `new_tight = 1` / `0` | 根据本位选的 `bit` 与 `s[pos]` 的大小关系更新 `tight`。 |
| `total += dp(...)` | 把后续所有合法分支的计数加起来，记得取模。 |
| `ans = dp(0,0,0)` | 从最高位开始的入口。 |

#### 复杂度

- **时间复杂度**  
  DP 状态数为 `L * (L+1) * 2`，每个状态最多枚举两个 `bit`，所以  
  \[
  O(L^2) \quad (L \le 800) \approx 1.3 \times 10^{6}
  \]
  远远小于暴力的指数级。

- **空间复杂度**  
  记忆化缓存保存所有状态，同样是 `O(L^2)`（约几 MB），递归栈深度为 `L`。  

> 与暴力解相比，时间从 “遍历 $2^{800}$ 个数” 降到了 “几百万次简单循环”，完全可以在毫秒级完成。

---

## 心得

- **核心技巧**：**数位 DP + 预计算 “popcount 到 1 的步数”**。  
  把原本需要遍历所有数字的任务，转化为只在二进制位上做一次动态规划，再通过 “popcount 在合格集合里” 判断是否满足条件。

- **适用的题型**  
  1. **统计满足某种 “位计数” 条件的数**（如：二进制中 `1` 的个数是质数、是偶数等）。  
  2. **需要在数的“特征函数”上做限制**，而特征函数只和位的计数有关（如：数字根、奇偶性）。  
  3. **在限定范围内统计满足递归关系的数**（如：每次取数字和、每次取位数等）。

- **一句话总结解题钥匙**  
  “把‘多少次操作’抽象成‘popcount 的取值范围’，然后用数位 DP 直接计数”。  

---

## 反思

- **第一反应**：直接枚举所有小于 `n` 的数，逐个模拟操作。  
  这在思路上是对的，但忘记了 `n` 可能非常大（二进制长达 800 位），导致不可行。

- **最容易踩的坑**  
  1. **忘记排除 0**：DP 会把全 0 的情况算进去，需要手动排除。  
  2. **`k = 1` 时的边界**：此时我们需要 `g[popcount] ≤ 0`，只有 `popcount = 1` 合格，集合 `S` 只能是 `{1}`。  
  3. **递归深度**：`popcount` 的递归层数很小，但实现时要确保 `precompute_g` 覆盖到所有可能的 `t`（最大不超过二进制位数）。  
  4. **取模**：在 DP 累加时及时对 `MOD` 取模，防止整数溢出。

- **下次类似题的第一步**  
  看到“对数字做位级操作并计数”，立刻问自己：“这操作只和 `1` 的个数（或 `0` 的个数）有关吗？”如果答案是肯定的，就 **把问题转化为对 `popcount` 的约束**，随后考虑 **数位 DP** 来直接统计满足约束的数字。