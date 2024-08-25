# #2842. 统计具有最大美感的字符串的 K 子序列数量 / Count K-Subsequences of a String With Maximum Beauty

> 难度：困难 · 标签：Hash Table、Math、String、Greedy、Combinatorics · [LeetCode 链接](https://leetcode.com/problems/count-k-subsequences-of-a-string-with-maximum-beauty/)

---

## 题目（英文原版）

**Description**

You are given a string s and an integer k.
A k-subsequence is a subsequence of s, having length k, and all its characters are unique, i.e., every character occurs once.
Let f(c) denote the number of times the character c occurs in s.
The beauty of a k-subsequence is the sum of f(c) for every character c in the k-subsequence.
For example, consider s = "abbbdd" and k = 2:
Return an integer denoting the number of k-subsequences whose beauty is the maximum among all k-subsequences. Since the answer may be too large, return it modulo 109 + 7.
A subsequence of a string is a new string formed from the original string by deleting some (possibly none) of the characters without disturbing the relative positions of the remaining characters.
Notes

**Examples**

**Example 1:**

```
Input: s = "bcca", k = 2
Output: 4
Explanation: From s we have f('a') = 1, f('b') = 1, and f('c') = 2.
The k-subsequences of s are: 
bcca having a beauty of f('b') + f('c') = 3 
bcca having a beauty of f('b') + f('c') = 3 
bcca having a beauty of f('b') + f('a') = 2 
bcca having a beauty of f('c') + f('a') = 3
bcca having a beauty of f('c') + f('a') = 3 
There are 4 k-subsequences that have the maximum beauty, 3. 
Hence, the answer is 4.
```

**Example 2:**

```
Input: s = "abbcd", k = 4
Output: 2
Explanation: From s we have f('a') = 1, f('b') = 2, f('c') = 1, and f('d') = 1. 
The k-subsequences of s are: 
abbcd having a beauty of f('a') + f('b') + f('c') + f('d') = 5
abbcd having a beauty of f('a') + f('b') + f('c') + f('d') = 5 
There are 2 k-subsequences that have the maximum beauty, 5. 
Hence, the answer is 2.
```

**Constraints**

- 1 <= s.length <= 2 * 105
- 1 <= k <= s.length
- s consists only of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串 `s` 和一个整数 `k`。  
**k-子序列** 是指 `s` 的一个子序列（subsequence），其长度为 `k`，且其中的所有字符互不相同（即每个字符只出现一次）。  

设 `f(c)` 为字符 `c` 在 `s` 中出现的次数。  
**美感（beauty）** 定义为该 k-子序列中所有字符的 `f(c)` 之和。  

求所有 k-子序列中美感最大的子序列的数量，并返回该数量对 `10^9 + 7` 取模后的结果。  

> **子序列（subsequence）**：从原字符串中删除若干（可能为零）字符后，保留剩余字符的相对顺序而得到的新字符串。

### 示例

**示例 1**

```
Input: s = "bcca", k = 2
Output: 4
Explanation: 
从 s 中得到的字符出现次数为 f('a') = 1, f('b') = 1, f('c') = 2。
所有长度为 2 的 k-子序列及其美感如下：
- "bc" 的美感为 f('b') + f('c') = 3
- "bc" 的美感为 f('b') + f('c') = 3
- "ba" 的美感为 f('b') + f('a') = 2
- "ca" 的美感为 f('c') + f('a') = 3
- "ca" 的美感为 f('c') + f('a') = 3  
其中美感最大的值为 3，对应的 k-子序列有 4 种，因此答案为 4。
```

**示例 2**

```
Input: s = "abbcd", k = 4
Output: 2
Explanation: 
字符出现次数为 f('a') = 1, f('b') = 2, f('c') = 1, f('d') = 1。
所有长度为 4 的 k-子序列及其美感如下：
- "abbc" 的美感为 f('a') + f('b') + f('c') + f('d') = 5
- "abbd" 的美感为 f('a') + f('b') + f('c') + f('d') = 5  
美感最大值为 5，对应的 k-子序列有 2 种，所以答案为 2。
```

### 约束

- `1 <= s.length <= 2 * 10^5`
- `1 <= k <= s.length`
- `s` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有长度为 `k` 的子序列**，检查每个子序列的字符是否互不相同（即每个字符只出现一次），然后把这些字符在原串中的出现次数相加得到“美丽值”。把所有子序列的美丽值找出来，取最大的，再统计有多少个子序列恰好得到这个最大值。

- **数据结构**  
  - 用列表 `subseq` 暂存当前正在构造的子序列。可以把它想象成我们在做“挑水果”：每挑一个字符，就把它放进篮子（`subseq`）里。  
  - 用字典 `freq` 记录原字符串每个字符出现的次数，类似于查字典：键是字母，值是这本字典里该字母的页码（出现次数）。  

- **为什么正确**  
  枚举**所有**可能的子序列，肯定不会遗漏任何合法答案；随后比较美丽值并计数，自然能得到最大美丽值对应的子序列个数。

- **复杂度**  
  - 枚举所有子序列的数量是 `C(n, k)`（从 `n` 个位置中选 `k` 个），在最坏情况下 `k≈n/2` 时，这个数接近 `2^n`，指数级增长。  
  - 对每个子序列我们还要检查字符是否唯一、计算美丽值，这又要遍历 `k` 次。  
  - 因此 **时间复杂度** 大约是 `O(C(n, k) * k)`，在 `n=20` 以内还能接受，`n=2·10⁵` 时根本不可行。  
  - **空间复杂度** 只用来保存 `freq`（至多 26 个字母）和递归栈/临时列表，都是 `O(1)`（常数级）。


#### 代码（Python）

```python
from collections import Counter
from itertools import combinations

MOD = 10**9 + 7

def brute_count(s: str, k: int) -> int:
    n = len(s)
    if k > n:               # k 大于长度显然不可能
        return 0

    freq = Counter(s)      # 统计每个字符出现次数，类似查字典

    max_beauty = -1
    cnt_max = 0

    # 产生所有下标的组合，进而得到所有子序列
    for idxs in combinations(range(n), k):
        # 取出对应字符
        chars = [s[i] for i in idxs]

        # 检查是否全部不同（每个字符只出现一次）
        if len(set(chars)) != k:
            continue

        # 计算美丽值：把每个字符的出现次数相加
        beauty = sum(freq[c] for c in chars)

        if beauty > max_beauty:
            max_beauty = beauty
            cnt_max = 1
        elif beauty == max_beauty:
            cnt_max += 1

    return cnt_max % MOD
```

> 这段代码只能用来验证思路或在极小的数据上跑通，**在正式测试里会超时**。

#### 复杂度

- **时间复杂度**：`O(C(n, k) * k)`，指数级增长，`C(n, k)` 是组合数，代表“从 `n` 里挑 `k` 种方法的总数”。  
- **空间复杂度**：`O(1)`（只用了常数个额外变量），不随 `n` 增长。

---

### 2. 最优解

#### 思路  

暴力解慢的根源在于**枚举子序列本身**，而这一步其实是不需要的。题目只要求：

1. 选出 **k 个不同的字符**（不管它们在原串中的位置如何），使得这些字符的出现次数之和最大；
2. 统计 **有多少种选法** 能达到这个最大和。

换句话说，我们只需要在 **字符种类**（最多 26 种）上做选择，而不必关心具体的下标。于是可以把问题抽象为：

> 给定每个字符的出现次数 `f(c)`（即频率），从这些频率中挑选 `k` 项，使得和最大，并统计挑选方式的数量。

这一步的关键是**“挑最大的频率”**。如果我们把所有字符的频率从大到小排好序，只要取前 `k` 个频率，它们的和就是最大可能的美丽值。唯一的例外是：**出现次数相同的字符会产生多种等价的挑选方式**，我们需要计算这些等价方式的组合数。

下面一步步推导：

1. **统计频率**  
   用 `cnt[x]` 表示“出现次数恰好为 `x` 的字符有多少个”。这相当于把频率相同的字符分到同一个盒子里，盒子里有 `cnt[x]` 张卡片。  
   例如 `s = "abbbdd"` → 频率表 `{a:1, b:3, d:2}` → `cnt[1]=1, cnt[2]=1, cnt[3]=1`。

2. **从大到小遍历频率**  
   设 `need = k`（还需要挑多少个字符）。从最大的频率 `x_max` 开始：
   - 盒子里有 `cnt[x]` 张卡片（即 `cnt[x]` 个字符的频率都是 `x`）。  
   - 我们最多可以挑 `i = min(need, cnt[x])` 张卡片。挑 `i` 张的方式有 `C(cnt[x], i)` 种（组合数），因为从 `cnt[x]` 个相同频率的字符中挑 `i` 个。  
   - 这 `i` 个字符每个都贡献 `x` 次出现次数，所以美丽值会增加 `i * x`（我们其实只关心是否是最大值，直接挑最大的即可）。  
   - 把 `i` 从 `need` 中减去，继续向下一个更小的频率处理。

   当 `need` 变为 0 时，已经挑完 `k` 个字符，整个挑选过程结束。此时累计的组合数的乘积就是 **满足最大美丽值的 k‑子序列的种数**。

3. **为什么只挑最大的频率就一定得到最大美丽值**  
   假设我们挑了一个频率 `x1`，而还有更大的频率 `x2 > x1` 没被挑。把 `x1` 换成 `x2`，美丽值会增加 `x2 - x1 > 0`，所以原来的选择不可能是最大值。于是**最优解一定是把频率从大到小“贪心”取**。

4. **组合数的模运算**  
   由于答案需要对 `10⁹+7` 取模，我们必须在模数下计算组合数 `C(n, r) = n! / (r! (n-r)!)`。利用 **费马小定理**（`a^(p-1) ≡ 1 (mod p)`，`p` 为质数）可以把除法转化为乘法：  
   `C(n, r) ≡ n! * inv(r!) * inv((n-r)!) (mod p)`，其中 `inv(x) = x^(p-2) mod p`。  
   为了在 `O(1)` 时间内得到任意 `n!` 和其逆元，我们预先计算 **阶乘数组** `fac[i]` 和 **逆阶乘数组** `ifac[i]`（从 `0` 到最大可能的 `cnt[x]`，即 26）。

5. **实现细节**  
   - 先用 `Counter` 统计每个字符出现次数 → 得到频率列表 `freqs`。  
   - 再把频率计数到字典 `cnt`，并把所有出现的频率放进列表 `vals`，从大到小排序。  
   - 预先准备 `fac`、`ifac`（长度只需要到 26 即可）。  
   - 按上述贪心遍历 `vals`，累计答案 `ans = ans * C(cnt[x], i) % MOD`，并更新 `need -= i`。  
   - 当 `need` 为 0 时结束循环；若遍历完仍有 `need > 0`（说明不同字符的种类少于 `k`），答案为 0。

#### 代码（Python）

```python
MOD = 10**9 + 7
from collections import Counter

# ---------- 预处理：阶乘与逆阶乘 ----------
def prepare_fact(n: int):
    """返回长度为 n+1 的 fac 与 ifac 列表（模 MOD）"""
    fac = [1] * (n + 1)
    for i in range(1, n + 1):
        fac[i] = fac[i - 1] * i % MOD

    ifac = [1] * (n + 1)
    # 逆元使用 Fermat 小定理：a^(p-2) ≡ a^(-1) (mod p)
    ifac[n] = pow(fac[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        ifac[i - 1] = ifac[i] * i % MOD
    return fac, ifac

def comb(n: int, r: int, fac, ifac) -> int:
    """在模 MOD 下计算组合数 C(n, r)"""
    if r < 0 or r > n:
        return 0
    return fac[n] * ifac[r] % MOD * ifac[n - r] % MOD


# ---------- 主函数 ----------
def count_k_subseq_max_beauty(s: str, k: int) -> int:
    n = len(s)
    if k > n:                     # 长度不足，直接返回 0
        return 0

    # 1️⃣ 统计每个字符出现次数（频率）
    freq = Counter(s)             # {'a':3, 'b':2, ...}
    # 2️⃣ 统计频率出现的次数：cnt[x] = 有多少字符的频率恰为 x
    cnt = Counter(freq.values())  # 例如 {3:1, 2:2, 1:5}
    # 把所有出现过的频率取出来并从大到小排序
    values = sorted(cnt.keys(), reverse=True)

    # 3️⃣ 预处理组合数所需的阶乘（最多只需要到 26，因为字符种类不超过 26）
    fac, ifac = prepare_fact(26)

    need = k           # 还需要挑多少个字符
    ans = 1            # 累计答案（乘积）

    for v in values:          # 从最大频率开始贪心
        if need == 0:
            break
        total = cnt[v]        # 频率为 v 的字符总数
        take = min(need, total)   # 本轮我们能取多少个

        # 组合数 C(total, take) 乘到答案里
        ans = ans * comb(total, take, fac, ifac) % MOD
        need -= take

    # 如果遍历结束后 still need > 0，说明不同字符种类不足 k
    if need > 0:
        return 0
    return ans % MOD
```

**代码说明（关键行中文注释）**

| 行号 | 作用 | 说明 |
|------|------|------|
| `freq = Counter(s)` | 统计每个字符出现次数 | 类似查字典，键是字符，值是出现次数 |
| `cnt = Counter(freq.values())` | 统计相同频率的字符有多少个 | 把相同频率的字符放进同一个盒子 |
| `values = sorted(cnt.keys(), reverse=True)` | 把所有出现的频率从大到小排好 | 贪心要从“大盒子”往下挑 |
| `fac, ifac = prepare_fact(26)` | 预计算阶乘和逆阶乘 | 只需要到 26，因为字符种类最多 26 |
| `take = min(need, total)` | 本轮可以挑的数量 | 不能超过还需要的 `need`，也不能超过该频率的总数 |
| `ans = ans * comb(total, take, fac, ifac) % MOD` | 累计组合方式数 | `C(total, take)` 是从同频率的字符中挑 `take` 个的方式数 |
| `need -= take` | 更新还需挑的数量 | 继续挑下一个更小的频率 |
| `if need > 0: return 0` | 处理字符种类不足的情况 | 说明不同字符不够 `k` 个，答案为 0 |

#### 复杂度

- **时间复杂度**：  
  - 统计频率 `O(n)`（遍历字符串一次）。  
  - 统计频率出现次数、排序频率列表 `O(26 log 26)`，可以视作常数。  
  - 主循环最多遍历 26 种频率，亦为常数。  
  - **总体** 为 `O(n)`，线性时间，能够轻松处理 `n = 2·10⁵`。  

- **空间复杂度**：  
  - 需要存放字符频率的字典 `freq`（最多 26 项）和 `cnt`（最多 26 项），以及阶乘数组 `fac、ifac` 长度 27。  
  - 所有额外空间均为 `O(1)`（常数级），不随 `n` 增长。

---

## 心得

- **核心技巧**：先把问题抽象为“在字符频率上挑选 `k` 项”，再利用**贪心 + 组合数**求解。  
- **适用的题型**  
  1. “选出若干不同元素，使得某种权值和最大”——如 *Maximum Sum of K Distinct Elements*。  
  2. “统计满足某种最大/最小条件的组合数”——如 *Number of Ways to Reach a Target Score*（使用组合计数）。  
- **一句话总结解题钥匙**：**只在字符种类层面贪心取最大频率，并用组合数计数等价的挑选方式**。

---

## 反思

- **第一反应**：看到“子序列”和“唯一字符”，自然想到枚举子序列并检查唯一性，结果是暴力搜索。  
- **最容易踩的坑**  
  - **忽视字符种类的上限**：字符串只包含 26 种小写字母，利用这一点可以把问题从 `O(2ⁿ)` 降到 `O(n)`。  
  - **模运算细节**：组合数需要在模 `10⁹+7` 下计算，直接除法会出错，必须使用逆元（费马小定理）。  
  - **边界条件**：`k` 大于不同字符的数量时答案应为 0；`k` 等于 0 时答案是 1（空子序列），不过题目保证 `k ≥ 1`。  
- **下次类似题目第一步**：**先把原问题转换为“在某个统计量上挑选 k 项”**，检查是否可以只在统计层面解决，避免对原序列进行指数级枚举。