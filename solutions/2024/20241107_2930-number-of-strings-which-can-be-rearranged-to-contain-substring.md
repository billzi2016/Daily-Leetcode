# #2930. 可重排后包含子串的字符串数量 / Number of Strings Which Can Be Rearranged to Contain Substring

> 难度：中等 · 标签：Math、Dynamic Programming、Combinatorics · [LeetCode 链接](https://leetcode.com/problems/number-of-strings-which-can-be-rearranged-to-contain-substring/)

---

## 题目（英文原版）

**Description**

You are given an integer n.
A string s is called good if it contains only lowercase English characters and it is possible to rearrange the characters of s such that the new string contains "leet" as a substring.
For example:
Return the total number of good strings of length n.
Since the answer may be large, return it modulo 109 + 7.
A substring is a contiguous sequence of characters within a string.

**Examples**

**Example 1:**

```
Input: n = 4
Output: 12
Explanation: The 12 strings which can be rearranged to have "leet" as a substring are: "eelt", "eetl", "elet", "elte", "etel", "etle", "leet", "lete", "ltee", "teel", "tele", and "tlee".
```

**Example 2:**

```
Input: n = 10
Output: 83943898
Explanation: The number of strings with length 10 which can be rearranged to have "leet" as a substring is 526083947580. Hence the answer is 526083947580 % (109 + 7) = 83943898.
```

**Constraints**

- 1 <= n <= 105

---

## 题目（中文翻译）

You are given an integer `n`.  
A string `s` is called **good** if it contains only lowercase English characters and it is possible to rearrange the characters of `s` such that the new string contains **"leet"** as a substring（子串）.  
Return the total number of good strings of length `n`.  
Since the answer may be large, return it modulo `10^9 + 7`.  
A substring（子串） is a contiguous sequence of characters within a string.

**Example 1:**  

**Example 2:**  

**Constraints:**  

- `1 <= n <= 10^5`

---

### 示例

#### 示例 1
**Input:** `n = 4`  
**Output:** `12`  
**Explanation:** 可以重排后得到包含 `"leet"` 这一子串的 12 个字符串分别是：`"eelt"`, `"eetl"`, `"elet"`, `"elte"`, `"etel"`, `"etle"`, `"leet"`, `"lete"`, `"ltee"`, `"teel"`, `"tele"` 和 `"tlee"`。

#### 示例 2
**Input:** `n = 10`  
**Output:** `83943898`  
**Explanation:** 长度为 10 的满足条件的字符串共有 `526083947580` 个。故答案为 `526083947580 % (10^9 + 7) = 83943898`。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有长度为 `n` 的小写字母串枚举出来，逐个检查它们能否 **重排** 成包含子串 `"leet"` 的字符串。  
- **枚举**：把 26 个字母看成 26 张不同的卡片，依次抽 `n` 张放在一排，所有可能的排列就是所有字符串。  
- **检查**：对每个字符串统计字母出现的次数，只要出现至少 `1` 个 `'l'`、至少 `1` 个 `'t'`、至少 `2` 个 `'e'`，就说明它可以通过重新排列得到 `"leet"`（把这几个必需的字母排成 `"leet"`，其余字母随意放在前后即可）。  

> **为什么这样判断对？**  
> 只要字符串里有足够的字母组成 `"leet"`，我们总可以把这四个字母挑出来，按顺序摆成 `"leet"`，剩下的字母随意放到前后或中间，这就是一次合法的重排。

**时间复杂度**  
- 枚举所有字符串的数量是 `26^n`（每个位置 26 种选择），  
- 对每个字符串我们还要遍历一次字符统计出现次数，耗时 `O(n)`。  
- 所以整体是 `O(n·26^n)`，在最坏情况下几乎是 **指数级** 的时间，`n` 只要大于 5 就已经不可接受。  

**空间复杂度**  
- 只需要保存当前枚举的字符串和计数数组，空间是 `O(1)`（不随 `n` 增长）。

> 大白话解释：  
> `O(26^n)` 就像说“把 26 张卡片排成一行，所有可能的排法”。当 `n=10` 时，这个数已经是 `141167095653376`，远远超过电脑能在一秒钟内遍历的次数。

#### 代码（Python）

```python
import itertools
from collections import Counter

MOD = 10**9 + 7

def brute_good_strings(n: int) -> int:
    """
    暴力枚举（仅用于教学或 n 很小的情况）。
    """
    alphabet = [chr(ord('a') + i) for i in range(26)]   # ['a', 'b', ... 'z']
    ans = 0

    # itertools.product 会生成所有长度为 n 的字母组合
    for tup in itertools.product(alphabet, repeat=n):
        s = ''.join(tup)               # 把元组拼成字符串
        cnt = Counter(s)               # 统计每个字符出现次数
        # 检查是否至少有 1 个 l、1 个 t、2 个 e
        if cnt['l'] >= 1 and cnt['t'] >= 1 and cnt['e'] >= 2:
            ans += 1
    return ans % MOD
```

> **注意**：上述函数在 `n=4` 时还能跑完（`26^4 = 456,976`），但 `n=10` 已经不可能在合理时间内得到答案。

#### 复杂度

- 时间复杂度：`O(n·26^n)` —— 指数级增长，`n` 稍大就会爆炸。  
- 空间复杂度：`O(1)` —— 只使用常数级额外空间。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，真正的难点不是 **如何枚举**，而是 **如何计数**。  
我们只关心字符出现的次数，而不是它们的具体排列顺序。于是可以把问题转化为：

> **有多少长度为 `n` 的字符串，其字母出现次数满足**  
> `cnt['l'] ≥ 1`、`cnt['t'] ≥ 1`、`cnt['e'] ≥ 2`？

这正好是一个 **容斥原理**（Inclusion–Exclusion）的问题。  
把“不满足条件”的三类情况列出来：

| 事件 | 含义 | 类比 |
|------|------|------|
| **A** | 没有 `'l'`（`cnt['l']=0`） | 把字典里 **l** 这页撕掉，所有单词都找不到 l |
| **B** | 没有 `'t'`（`cnt['t']=0`） | 同理，t 的页也撕掉 |
| **D** | `'e'` 的数量 ≤ 1（即 0 或 1 个） | “e” 这张卡片只能用 0 次或 1 次 |

我们要求的是 **既不属于 A，也不属于 B，也不属于 D** 的字符串数。  
根据容斥原理：

```
good = total
       - |A| - |B| - |D|
       + |A∩B| + |A∩D| + |B∩D|
       - |A∩B∩D|
```

下面逐个计算每一项的大小。**关键**是把每个约束转化为“可选的字母数”。  

1. **总数** `total = 26^n`（每位 26 种字母）  
2. **|A|**：没有 `'l'` → 只能用除 `'l'` 之外的 25 个字母 → `25^n`  
3. **|B|**：同理，`25^n`  
4. **|D|**：`e` 出现 **0 次** 或 **恰好 1 次**  
   - 0 次：`25^n`（排除 `'e'`）  
   - 1 次：选出放 `'e'` 的位置 `n` 种，其他位置任意 25 种 → `n·25^{n-1}`  
   - 合计：`25^n + n·25^{n-1}`  
5. **|A∩B|**：既没有 `'l'` 也没有 `'t'` → 只剩 24 种字母 → `24^n`  
6. **|A∩D|**：没有 `'l'`，且 `'e'` ≤ 1  
   - 先把 `'l'` 去掉，字母表剩 25（含 `'e'`）  
   - 0 个 `'e'`：`24^n`（排除 `'e'`）  
   - 1 个 `'e'`：`n·24^{n-1}`  
   - 合计：`24^n + n·24^{n-1}`  
   - **|B∩D|** 同理，结果相同。  
7. **|A∩B∩D|**：没有 `'l'`、没有 `'t'`，且 `'e'` ≤ 1  
   - 去掉 `'l'`、`'t'`，剩 24 种（含 `'e'`）  
   - 0 个 `'e'`：`23^n`（排除 `'e'`）  
   - 1 个 `'e'`：`n·23^{n-1}`  
   - 合计：`23^n + n·23^{n-1}`  

把这些代入容斥公式，整理后得到：

```
good = 26^n
       - 3·25^n - n·25^{n-1}
       + 3·24^n + 2·n·24^{n-1}
       - 23^n - n·23^{n-1}
```

所有指数运算都可以用 **快速幂**（Python 内置 `pow(base, exp, MOD)`）在 `O(log n)` 时间完成。  
因为 `n ≤ 10^5`，只需要常数级的乘法、加法和模运算，整个算法的时间复杂度是 **线性对数** `O(log n)`，空间 `O(1)`。

> **核心技巧**：把“能否重排成包含子串”转化为“字母出现次数的下界”，随后用容斥原理一次性计数。  
> 这一步的类比是：如果你想知道多少本书的目录里 **至少** 同时出现 “数学、物理、化学” 三章，你可以先算所有书的数量，然后减去缺少任意一章的书，再加回同时缺少两章的书，最后减去三章都缺的书——这正是容斥原理的思想。

#### 代码（Python）

```python
MOD = 10**9 + 7

def power(base: int, exp: int) -> int:
    """返回 base^exp (mod MOD) ，使用 Python 内置的快速幂"""
    return pow(base, exp, MOD)

def good_strings(n: int) -> int:
    """
    最优解：使用容斥原理 + 快速幂，时间 O(log n)，空间 O(1)。
    """
    if n < 4:                 # 长度不足以放下 "leet"
        return 0

    # 预先计算所有需要的幂
    p26 = power(26, n)
    p25 = power(25, n)
    p25_1 = power(25, n - 1)
    p24 = power(24, n)
    p24_1 = power(24, n - 1)
    p23 = power(23, n)
    p23_1 = power(23, n - 1)

    # 计算每一项（注意乘法要先取模，防止中间溢出）
    term1 = p26                                         # 26^n
    term2 = (3 * p25) % MOD                             # -3·25^n
    term3 = (n % MOD) * p25_1 % MOD                     # -n·25^{n-1}
    term4 = (3 * p24) % MOD                             # +3·24^n
    term5 = (2 * (n % MOD) % MOD) * p24_1 % MOD         # +2·n·24^{n-1}
    term6 = p23                                         # -23^n
    term7 = (n % MOD) * p23_1 % MOD                     # -n·23^{n-1}

    # 按容斥公式合并（先把所有正数加，再减去负数）
    ans = (term1
           - term2 - term3
           + term4 + term5
           - term6 - term7) % MOD

    # Python 的取模会把负数转成正数，这里再确保非负
    return ans if ans >= 0 else ans + MOD
```

> **代码说明（每行中文注释）**  
> - `if n < 4: return 0`：因为要至少有 1 个 `'l'`、1 个 `'t'`、2 个 `'e'`，最短长度是 4。  
> - `power` 使用内置 `pow`，它在底层已经实现了 **二进制快速幂**，时间 `O(log n)`。  
> - 所有 `termX` 都在 **取模** 后再做加减，防止中间乘积超出 Python 整数范围（虽然 Python 整数是大数，但取模可以保持数值小）。  
> - 最后 `ans % MOD` 保证答案落在 `[0, MOD-1]`。

#### 复杂度

- **时间复杂度**：`O(log n)`（只需要若干次快速幂），相较于暴力的 `O(n·26^n)` 提速几个数量级。  
- **空间复杂度**：`O(1)`（只用固定数量的变量），不随 `n` 增长。

> 与暴力解对比：  
> - 暴力解需要遍历 **所有** 可能的字符串，指数级时间，根本不可行。  
> - 最优解只关心**计数**，一次公式直接算出答案，几乎瞬间完成，即使 `n=10^5` 也毫无压力。

---

## 心得  

- **核心技巧**：把“能否重排得到特定子串”转化为“字母出现次数的下界”，随后使用 **容斥原理** 计数。  
- **适用场景**：  
  1. 统计满足若干“至少出现 k 次”类约束的字符串（如 `"abc"` 至少出现一次）。  
  2. 计数满足“缺少某些元素”或“元素出现上限”的组合问题（如密码强度检查）。  
  3. 任意需要 **同时满足多个独立约束** 的计数题目。  
- **一句话总结**：  
  “把‘能否重排’抽象成‘出现次数≥阈值’，再用容斥把‘不满足’的情况逐层剔除，答案瞬间得出。”

---

## 反思  

- **第一反应**：看到 “可以重排” 立即想到只要有足够的字符就行，于是把问题转化为“字母计数”。  
- **最容易踩的坑**：  
  - 忽略了 `'e'` 需要 **两个**，容易把它当成只要出现一次就行。  
  - 在容斥计算时忘记了“最多 1 个 e”实际上包含 **0 次** 与 **恰好 1 次** 两种情况。  
  - 对取模运算不慎，导致中间乘积溢出或负数取模错误。  
- **下次类似题的第一步**：  
  “先把‘能否重排成目标子串’转化为‘每个必需字符的出现下界’，再列出哪些约束被违背，用容斥原理计数”。  

祝你玩转算法，解锁更多思路！