# #2851. 字符串转换 / String Transformation

> 难度：困难 · 标签：Math、String、Dynamic Programming、String Matching · [LeetCode 链接](https://leetcode.com/problems/string-transformation/)

---

## 题目（英文原版）

**Description**

You are given two strings s and t of equal length n. You can perform the following operation on the string s:
You are also given an integer k. Return the number of ways in which s can be transformed into t in exactly k operations.
Since the answer can be large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: s = "abcd", t = "cdab", k = 2
Output: 2
Explanation: 
First way:
In first operation, choose suffix from index = 3, so resulting s = "dabc".
In second operation, choose suffix from index = 3, so resulting s = "cdab".

Second way:
In first operation, choose suffix from index = 1, so resulting s = "bcda".
In second operation, choose suffix from index = 1, so resulting s = "cdab".
```

**Example 2:**

```
Input: s = "ababab", t = "ababab", k = 1
Output: 2
Explanation: 
First way:
Choose suffix from index = 2, so resulting s = "ababab".

Second way:
Choose suffix from index = 4, so resulting s = "ababab".
```

**Constraints**

- 2 <= s.length <= 5 * 105
- 1 <= k <= 1015
- s.length == t.length
- s and t consist of only lowercase English alphabets.

---

## 题目（中文翻译）

给定两个长度相等为 `n` 的字符串 `s` 和 `t`。你可以对字符串 `s` 执行以下操作：

同时，给定一个整数 `k`。返回在恰好进行 `k` 次操作后，`s` 可以被转换成 `t` 的方式数量。由于答案可能很大，请返回答案对 `10^9 + 7` 取模的结果。

## 示例

### 示例 1

**输入**  
```
s = "abcd", t = "cdab", k = 2
```

**输出**  
```
2
```

**解释**  
第一种方式：  
- 第一次操作，选择下标为 `3` 的后缀，使得得到的 `s = "dabc"`。  
- 第二次操作，选择下标为 `3` 的后缀，使得得到的 `s = "cdab"`。

第二种方式：  
- 第一次操作，选择下标为 `1` 的后缀，使得得到的 `s = "bcda"`。  
- 第二次操作，选择下标为 `1` 的后缀，使得得到的 `s = "cdab"`。

### 示例 2

**输入**  
```
s = "ababab", t = "ababab", k = 1
```

**输出**  
```
2
```

**解释**  
第一种方式：  
- 选择下标为 `2` 的后缀，使得得到的 `s = "ababab"`。

第二种方式：  
- 选择下标为 `4` 的后缀，使得得到的 `s = "ababab"`。

## 约束条件

- `2 <= s.length <= 5 * 10^5`
- `1 <= k <= 10^15`
- `s.length == t.length`
- `s` 和 `t` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

把 **一次操作** 看成「把字符串左旋 `i` 位」：

- 选一个下标 `i (1 ≤ i ≤ n‑1)`（下标从 **1** 开始），
- 把前 `i` 个字符搬到字符串的末尾，剩下的字符保持顺序。  

举例说明：

```
s = "abcd"
i = 3 → 左旋 3 位 → "dabc"
i = 1 → 左旋 1 位 → "bcda"
```

> **类比**：左旋相当于把一本书的前 `i` 页翻到书的最后，书的内容顺序不变，只是起点变了。

**目标**：经过恰好 `k` 次左旋，使 `s` 变成 `t`。

如果把「左旋 `i` 位」抽象成「在当前位置的偏移量上加 `i`（模 `n`）」，那么整个过程就等价于：

- 初始偏移 `0`（即 `s` 本身）。
- 每一步在当前偏移上 **加** 一个数 `i ∈ {1,2,…,n‑1}`，结果取模 `n`。
- `k` 步后偏移必须恰好等于 `d`，其中 `d` 是 `t` 相对于 `s` 的旋转距离（如果 `t` 不是 `s` 的任意旋转，则根本不可能）。

于是我们把问题转化为：

> **在集合 `{1,…,n‑1}` 中选 `k` 个数，使它们的和模 `n` 等于 `d`，求选法数目**。

**为什么暴力可行**（仅作思路展示）：

- 枚举所有 `k` 步的选择，共有 `(n‑1)^k` 种可能；
- 对每一种可能，累加它们的和并取模 `n`，检查是否等于 `d`。

显然，这种「全枚举」的时间随 `k` 指数增长，根本不可用。但它帮助我们把原始的字符串操作抽象成「模数求和」的计数问题。

#### 代码（Python）

下面的代码实现了完整的暴力枚举（仅用于演示，**不适用于正式提交**）：

```python
MOD = 10**9 + 7

def brute_force(s: str, t: str, k: int) -> int:
    n = len(s)
    # 1）先判断 t 是否是 s 的某个旋转
    if t not in (s * 2):
        return 0

    # 2）求出目标偏移 d（左旋 d 位得到 t）
    d = (s + s).find(t)          # 第一次出现的位置就是旋转距离

    # 3）深度优先搜索所有 k 步的选择
    ans = 0
    def dfs(step: int, cur: int):
        nonlocal ans
        if step == k:
            if cur % n == d:
                ans = (ans + 1) % MOD
            return
        for add in range(1, n):   # i ∈ {1,…,n‑1}
            dfs(step + 1, cur + add)

    dfs(0, 0)
    return ans
```

> **代码解释**  
> - `if t not in (s * 2)`: 判断 `t` 是否为 `s` 的旋转（把 `s` 拼两遍，所有旋转都会出现）。  
> - `d = (s + s).find(t)`: 找到 `t` 第一次出现的位置，即左旋多少位得到 `t`。  
> - `dfs` 用递归枚举每一步的旋转长度 `add`，累计当前的偏移 `cur`。  
> - 当走完 `k` 步时检查 `cur % n == d`，若相等则找到一种合法方案。

#### 复杂度

- **时间复杂度**：`O((n‑1)^k)`  
  每一步有 `n‑1` 种选择，深度为 `k`，指数级增长。  
  用大白话说，就是「每走一步都要把所有可能的路径全部展开，走 `k` 步就会有 `n‑1` 的 `k` 次方条路」。

- **空间复杂度**：`O(k)`（递归栈的深度）  

> 对于本题的约束（`n ≤ 5·10^5，k ≤ 10^15`），暴力根本不可行，只能用下面的「最优解」来解决。

---

### 2. 最优解

#### 思路  

从暴力解我们已经把问题抽象为：

> **在集合 `A = {1,2,…,n‑1}` 中选 `k` 个数，使它们的和模 `n` 等于 `d`，求选法数目**。

这正是 **在环 `ℤ_n` 上的计数问题**，可以用 **线性递推 + 快速幂**（即矩阵快速幂）来求解。  
关键在于：

1. **状态**：当前的偏移量 `offset (0 … n‑1)`。  
2. **转移**：一次操作后，`offset → (offset + a) % n`，其中 `a ∈ A`。  
3. **转移矩阵** `M`：大小为 `n × n`，`M[i][j] = 1` 当且仅当存在 `a ∈ A` 使得 `j ≡ (i + a) mod n`。  
   换句话说，**每一行都有 `n‑1` 个 `1`，分别对应把 `i` 加上 `1…n‑1` 的结果**。

如果记 `dp_t[i]` 为经过 `t` 步后偏移为 `i` 的方案数，则  

```
dp_{t+1} = dp_t  ×  M
```

于是 `dp_k = dp_0 × M^k`，其中 `dp_0` 只有 `dp_0[0] = 1`（初始偏移为 0），其余为 0。  
答案就是 `dp_k[d]`。

**瓶颈**：直接构造并快速幂 `n × n` 矩阵的时间是 `O(n^3 log k)`，对 `n = 5·10^5` 完全不可行。

**关键观察——循环卷积**  

矩阵 `M` 是 **循环移位矩阵**（每一行都是前一行向右循环平移 1 位），它是 **循环卷积**（环形卷积）的矩阵表示。  
对循环卷积来说，有一个非常重要的性质：

> **循环卷积在离散傅里叶变换（DFT）下会变成点乘**。

因此我们可以把向量 `dp` 看成长度为 `n` 的多项式 `P(x)`（系数对应偏移），把一次操作对应的多项式 `Q(x) = x^1 + x^2 + … + x^{n‑1}`。  
一次左旋相当于把 `P(x)` 与 `Q(x)` **在环 `x^n = 1` 下做卷积**（即取模 `x^n‑1` 的乘积）。  
于是：

```
dp_k 对应的多项式 = (Q(x))^k   (mod x^n - 1)
```

求系数 `x^d` 即为答案。

**如何快速求 `(Q(x))^k (mod x^n‑1)`**  

1. **快速幂**：把多项式 `Q` 进行二进制幂，使用「乘法」＝「环形卷积」。
2. **环形卷积**：使用 **快速数论变换（NTT）**（模 `998244353`）或 **FFT**（浮点）在 `O(n log n)` 时间内完成一次卷积，再对指数 `n` 取模（把下标 ≥ n 的系数折回到 `[0, n-1]`）。
3. **模数转换**：题目要求模 `10^9+7`，而 NTT 常用的模是 `998244353`。我们可以 **在两套互质模数下分别做 NTT**（如 `998244353` 与 `1004535809`），随后用 **中国剩余定理（CRT）** 合并得到模 `10^9+7` 的结果。实现略繁琐，这里只给出 **单模**（`998244353`）的实现思路，读者可以自行扩展到 `10^9+7`。

**核心步骤概览**

| 步骤 | 作用 | 关键概念 |
|------|------|----------|
| 1. 判断可达性 | `t` 必须是 `s` 的旋转，否则答案 0 | 字符串匹配（KMP/Z） |
| 2. 求目标偏移 `d` | 计算 `t` 在 `s+s` 中第一次出现的位置 | 旋转距离 |
| 3. 构造基多项式 `Q(x)` | `Q(x) = x + x^2 + … + x^{n-1}` | 环形卷积的基元 |
| 4. 快速幂求 `Q(x)^k (mod x^n-1)` | 二进制幂 + 环形卷积 | 多项式快速幂、NTT |
| 5. 取系数 `x^d` 并模 `1e9+7` | 即为答案 | 取模、CRT（可选） |

#### 代码（Python）

下面的实现 **仅演示思路**，使用 `numpy.fft`（浮点）完成卷积，并在每次乘法后对系数取模 `MOD = 10**9+7`。在实际竞赛中请换成 NTT（整数）以避免精度误差。

```python
import sys
import math
from typing import List
import numpy as np

MOD = 10**9 + 7

def next_power_of_two(x: int) -> int:
    """返回不小于 x 的最小 2 的幂"""
    return 1 << (x - 1).bit_length()

def cyclic_convolve(a: List[int], b: List[int]) -> List[int]:
    """
    环形卷积 (a * b) mod (x^n - 1)，返回长度 n 的系数列表。
    这里使用浮点 FFT，实际使用 NTT 更安全。
    """
    n = len(a)
    size = next_power_of_two(2 * n)      # 为避免循环折叠，先做普通卷积再折回
    A = np.fft.rfft(a, size)
    B = np.fft.rfft(b, size)
    C = A * B
    conv = np.fft.irfft(C, size)
    conv = np.rint(conv).astype(np.int64) % MOD   # 四舍五入并取模

    # 折回到长度 n（环形）
    res = [0] * n
    for i in range(size):
        if i < n:
            res[i] = (res[i] + conv[i]) % MOD
        else:
            # 超出 n 的部分折回到 (i - n)
            res[i - n] = (res[i - n] + conv[i]) % MOD
    return res

def poly_pow(base: List[int], exp: int) -> List[int]:
    """二进制快速幂：返回 base^exp (mod x^n-1)"""
    n = len(base)
    # 单位多项式 1 -> 系数[1,0,0,...]
    result = [1] + [0] * (n - 1)
    while exp:
        if exp & 1:
            result = cyclic_convolve(result, base)
        base = cyclic_convolve(base, base)
        exp >>= 1
    return result

def kmp_lps(pattern: str) -> List[int]:
    """返回 KMP 的 lps（最长相等前后缀）数组，用于 O(n) 字符串匹配"""
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def find_rotation_distance(s: str, t: str) -> int:
    """如果 t 是 s 的旋转，返回左旋多少位得到 t；否则返回 -1"""
    if len(s) != len(t):
        return -1
    concat = s + s
    # 使用 KMP 在 concat 中找 t 的第一次出现位置
    pat = t
    txt = concat
    lps = kmp_lps(pat)
    i = j = 0
    while i < len(txt):
        if txt[i] == pat[j]:
            i += 1
            j += 1
            if j == len(pat):
                return i - j          # 第一次匹配的位置
        else:
            if j:
                j = lps[j - 1]
            else:
                i += 1
    return -1

def solve() -> None:
    import sys
    s = sys.stdin.readline().strip()
    t = sys.stdin.readline().strip()
    k = int(sys.stdin.readline().strip())

    n = len(s)

    # 1) 判断 t 是否可达
    d = find_rotation_distance(s, t)
    if d == -1:               # 不是旋转关系
        print(0)
        return

    # 2) 基多项式 Q(x) = x + x^2 + ... + x^{n-1}
    base = [0] * n
    for i in range(1, n):
        base[i] = 1          # 系数 x^i 为 1

    # 3) 计算 Q(x)^k (mod x^n-1)
    poly = poly_pow(base, k)

    # 4) 答案是系数 x^d
    ans = poly[d] % MOD
    print(ans)

if __name__ == "__main__":
    solve()
```

> **代码要点注释**  
> 1. `find_rotation_distance` 用 **KMP** 在 `s+s` 中找 `t`，时间 `O(n)`。  
> 2. `base` 对应一次操作的多项式：`x^i` 表示「左旋 i 位」。  
> 3. `cyclic_convolve` 先做普通卷积（FFT），再把下标 `≥ n` 的系数「折回」到 `[0, n‑1]`，实现「模 `x^n‑1`」的环形卷积。  
> 4. `poly_pow` 通过 **二进制快速幂**，每一步都调用 `cyclic_convolve`，总时间 `O(n log n log k)`。  
> 5. 最终答案 `poly[d]` 即为「恰好 `k` 步后偏移为 `d`」的方案数，记得对 `10^9+7` 取模。

> **实现提醒**：  
> - 在实际提交时请把 `numpy.fft` 换成 **NTT**（如 `mod = 998244353`）并使用 **CRT** 合并到 `10^9+7`，这样才能保证整数精度。  
> - 由于 `k` 可达 `10^15`，二进制幂的循环次数至多 `log2(10^15) ≈ 50`，完全可接受。

#### 复杂度

- **时间复杂度**：`O(n log n log k)`  
  - 每一次多项式乘法（环形卷积）需要 `O(n log n)`（FFT/NTT）。  
  - 快速幂的乘法次数是 `⌊log2 k⌋`，最多约 50 次。  
  - 整体对 `n = 5·10^5` 仍在几秒以内（实际使用高效 NTT 更快）。

- **空间复杂度**：`O(n)`  
  - 只保存若干长度为 `n` 的系数数组以及临时的 FFT/NTT 工作空间。

> 与暴力解相比，时间从指数级下降到 **准线性**（`n log n`），这就是本题的核心突破。

---

## 心得

- **核心技巧**：把「字符串左旋」抽象为「模 `n` 加法」，进而转化为 **环形卷积**（多项式乘法）的问题。  
- **适用场景**  
  1. 需要统计若干次「循环移位」或「环形加法」的组合数时。  
  2. 任意「在环上走步」的计数问题（如在圆桌上走步、密码轮盘等）。  
  3. 类似「给定集合的加法闭包」计数，常用多项式快速幂解决。  

> **解题钥匙**：**把离散操作映射到多项式乘法 → 用快速幂 + FFT/NTT**。

---

## 反思

- **第一反应**：看到「把后缀移动」立刻想到「旋转」或「循环移位」，于是把问题抽象为「偏移累加」。
- **最容易踩的坑**  
  1. **忽略 `i = n` 的禁止**：题目只允许 `1 … n‑1`，如果把 `0` 也算进去会导致答案偏大。  
  2. **`t` 不是 `s` 的旋转**：必须先判断可达性，否则直接返回 `0`。  
  3. **大数 `k`**：不能直接 DP，必须使用二进制快速幂。  
  4. **环形卷积的实现**：普通卷积后忘记把超出 `n` 的系数折回，会得到错误的模 `x^n‑1` 结果。  

- **下次思路**：  
  1. 先把「字符串操作」转成「数值模型」——这里是模 `n` 加法。  
  2. 判断是否可以用 **线性递推**（转移矩阵）描述。  
  3. 若矩阵是 **循环/卷积型**，立刻想到 **FFT/NTT + 快速幂**。  

这样就能在复杂度上把指数级的暴力直接压到 `n log n log k`，轻松应对大数据量。