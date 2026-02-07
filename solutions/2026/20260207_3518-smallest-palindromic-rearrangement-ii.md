# #3518. 最小回文重排 II / Smallest Palindromic Rearrangement II

> 难度：困难 · 标签：Hash Table、Math、String、Combinatorics、Counting · [LeetCode 链接](https://leetcode.com/problems/smallest-palindromic-rearrangement-ii/)

---

## 题目（英文原版）

**Description**

You are given a palindromic string s and an integer k.
Return the k-th lexicographically smallest palindromic permutation of s. If there are fewer than k distinct palindromic permutations, return an empty string.
Note: Different rearrangements that yield the same palindromic string are considered identical and are counted once.

**Examples**

**Example 1:**

```
Input: s = "abba", k = 2
Output: "baab"
Explanation:
```

**Example 2:**

```
Input: s = "aa", k = 2
Output: ""
Explanation:
```

**Example 3:**

```
Input: s = "bacab", k = 1
Output: "abcba"
Explanation:
```

**Constraints**

- 1 <= s.length <= 104
- s consists of lowercase English letters.
- s is guaranteed to be palindromic.
- 1 <= k <= 106

---

## 题目（中文翻译）

给定一个回文字符串 `s` 和一个整数 `k`。  
返回 `s` 的第 `k` 小（按字典序）回文排列（palindromic permutation）。如果不同的回文排列（distinct palindromic permutations）少于 `k` 个，返回空字符串。  
**注意**：产生相同回文字符串的不同重排被视为相同，只计数一次。

### 示例

#### 示例 1
**输入**: `s = "abba", k = 2`  
**输出**: `"baab"`  
**解释**:  

#### 示例 2
**输入**: `s = "aa", k = 2`  
**输出**: `""`  
**解释**:  

#### 示例 3
**输入**: `s = "bacab", k = 1`  
**输出**: `"abcba"`  
**解释**:  

### 约束条件
- `1 <= s.length <= 10^4`
- `s` 只包含小写英文字母。
- `s` 保证是回文的。
- `1 <= k <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：

1. **统计字符出现次数**。因为原串 `s` 已经是回文，除最多一个字符外，所有字符的出现次数都是偶数。  
2. **把每个字符的次数除以 2**，得到左半边需要放的字符（右半边完全由左半边镜像得到）。  
3. **把左半边的字符全排列**，每一种排列拼成完整的回文字符串。  
4. 把所有得到的回文字符串去重、排序，取第 `k` 小（下标 `k‑1`）。

> **类比**：把左半边的字符想象成一盒子里的彩色球，每种颜色的球数量已经固定。我们要把这些球全部排成一行（全排列），再把这行镜像到右边，就得到完整的回文。

这种做法一定能得到所有合法的回文排列，因为我们遍历了左半边的所有可能顺序。  

**为什么正确**  
- 回文的左半边决定了整个字符串，右半边只能是左半边的倒序（如果中心有单独的字符，则直接放在中间）。  
- 对左半边的每一种不同排列，必然得到一种不同的完整回文（不同的左半边必然导致不同的整体），所以遍历左半边的全排列即可得到所有答案。

**时间/空间分析（大白话）**  
- 假设左半边长度为 `m = n // 2`，字符种类数为 `c ≤ 26`。全排列的数量是  
  `m! / (cnt1! * cnt2! * … * cntc!)`，这正是我们需要枚举的组合数。  
- 暴力遍历每一种排列的时间就是 **“排列的总数 × 每次拼接字符串的时间”**，最坏情况下相当于 `O(m!)`（阶乘增长），即使 `m` 只有 10，`10! = 3,628,800`，已经很大了。  
- 空间上我们需要保存所有回文字符串再排序，最坏会占 **`O(排列数 × n)`** 的内存，容易爆掉。

> 简单来说，暴力解的时间复杂度是 **指数级**，在 `s` 长度达到 20 以上就已经不可行。

#### 代码（Python）

```python
import itertools
from collections import Counter

def kth_palindrome_bruteforce(s: str, k: int) -> str:
    # 1️⃣ 统计每个字符出现的次数
    freq = Counter(s)

    # 2️⃣ 计算左半边需要的字符次数（除以 2）
    half_cnt = {ch: v // 2 for ch, v in freq.items()}

    # 3️⃣ 把左半边的字符展开成列表，方便全排列
    half_chars = []
    for ch, cnt in half_cnt.items():
        half_chars.extend([ch] * cnt)          # 把每个字符复制 cnt 次

    # 4️⃣ 用 set 去重（因为有重复字符会产生相同排列）
    uniq_perms = set(itertools.permutations(half_chars))

    # 5️⃣ 把每个排列拼成完整回文，收集到列表
    palins = []
    mid = ''                                    # 中间字符（若有奇数个）
    for ch, cnt in freq.items():
        if cnt % 2 == 1:
            mid = ch
            break

    for left in uniq_perms:
        left_str = ''.join(left)
        pal = left_str + mid + left_str[::-1]   # 镜像右半边
        palins.append(pal)

    # 6️⃣ 排序后取第 k 小
    palins.sort()
    return palins[k - 1] if k <= len(palins) else ''
```

> **关键行注释**  
> - `half_cnt = {ch: v // 2 ...}`：把每个字符的次数除以 2，得到左半边需要的数量。  
> - `itertools.permutations` 会产生所有排列，`set` 用来去掉因为相同字符导致的重复排列。  
> - `left_str[::-1]` 是 Python 的切片技巧，直接得到左半边的倒序，构成右半边。

#### 复杂度

- **时间复杂度**：`O(m! )`（阶乘级），因为我们要遍历左半边的全部排列。  
  - `m = n // 2`，即使 `n = 20`，`m! = 10! ≈ 3.6e6`，已经非常慢。  
- **空间复杂度**：`O(m! * n)`，要把所有回文字符串存起来再排序，最坏会占用巨大的内存。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **“枚举所有排列”**，我们不需要真的把所有排列写出来，只要能够 **跳过** 已经统计好的整块排列数，就能直接定位第 `k` 小的那一个。

**核心思路**：**在构造左半边的过程中，按字典序逐位尝试每个可能的字符**，并**用组合计数**（多重排列的公式）算出**如果把这个字符放在当前位置，剩下的字符还能产生多少种合法排列**。  

- **如果这一次的计数 ≥ k**，说明第 `k` 小的答案一定以这个字符开头，我们就把它固定下来，继续往后构造。  
- **如果计数 < k**，说明所有以该字符开头的排列都不够第 `k` 小，需要**把计数从 k 中减去**，再尝试下一个更大的字符。

如此反复，最终会得到完整的左半边，随后把它镜像得到回文字符串。

**为什么可行**  
- 左半边的每一种排列对应唯一的完整回文，字典序比较时只需要比较左半边（因为右半边是镜像的，顺序相同）。  
- 多重排列的计数公式  

\[
\text{cnt} = \frac{(remaining)!}{\prod_i (freq_i)!}
\]

恰好给出了**“剩余字符可以排列出多少种不同序列”**。我们只要把它算出来，就能知道以当前字符为前缀的排列有多少。

**关键工具**  

| 工具 | 类比 | 作用 |
|------|------|------|
| **阶乘**（factorial） | 把 n 件不同的东西排成一行的方式数 | 计算总排列数 |
| **多重排列公式** | 把若干相同的东西放进去后，重复的排列要除去 | 统计带有重复字符的排列数 |
| **前缀计数** | 类似在字典里查找第 k 条词，先看第一个字母，再看第二个 | 在每一步决定是否“跳过”整块排列 |

**实现细节**  

1. **预计算阶乘**：`n ≤ 10^4`，`m = n // 2 ≤ 5000`，我们只需要到 `m` 的阶乘。使用 Python 的大整数即可，且每次计数时可能会非常大（超过 `10^6`），但只要大于 `k` 就可以直接截断，防止整数爆炸。  
2. **计数函数** `perm_count(rem_counts, total)`：  
   - `total` 为剩余字符的总数（左半边还要填的位数）。  
   - 公式 `total! / prod(cnt_i!)`，在除法前先把分子分母约简，或直接使用 `math.comb` 的乘除来防止溢出。这里采用**逐步相除**的方式，并在途中若结果已经 > k，就直接返回 `k+1`（相当于“够大了”）。  
3. **逐位构造**：循环 `pos` 从 `0` 到 `m-1`，对每个字符 `'a'..'z'`（如果它还有剩余的半数计数）尝试：  
   - 暂时把它的计数减 1，算出 `cnt = perm_count(...)`。  
   - 根据 `cnt` 与 `k` 的比较决定是否固定。  
4. **拼接**：左半边构造完后，加入可能的中间字符（出现奇数次的字符），再加左半边的逆序得到答案。  
5. **如果所有计数加起来仍然小于 k**，说明合法的回文排列不足 `k` 个，直接返回空串。

#### 代码（Python）

```python
import math
from collections import Counter

def kth_palindrome(s: str, k: int) -> str:
    n = len(s)
    freq = Counter(s)

    # ---------- 1. 检查是否有合法的回文 ----------
    odd_cnt = sum(v % 2 for v in freq.values())
    if odd_cnt > 1:                 # 题目保证 s 本身是回文，这里其实不需要，但保险起见
        return ""

    # ---------- 2. 准备左半边的字符计数 ----------
    half_cnt = {ch: v // 2 for ch, v in freq.items()}
    half_len = n // 2               # 需要填的左半边长度

    # ---------- 3. 预计算阶乘（到 half_len） ----------
    fact = [1] * (half_len + 1)
    for i in range(1, half_len + 1):
        fact[i] = fact[i - 1] * i

    # ---------- 4. 计算多重排列数的辅助函数 ----------
    def perm_count(rem_counts, total):
        """返回 total! / prod(cnt_i!)，若结果 > k 则直接返回 k+1"""
        if total == 0:
            return 1
        res = fact[total]
        for c in rem_counts.values():
            if c > 0:
                res //= fact[c]
            # 若已经超过 k，就可以提前结束
            if res > k:
                return k + 1
        return res

    # ---------- 5. 按字典序逐位构造左半边 ----------
    left = []
    for pos in range(half_len):
        # 按字母顺序尝试放哪个字符
        for ch in map(chr, range(ord('a'), ord('z') + 1)):
            if half_cnt.get(ch, 0) == 0:        # 该字符已经用完
                continue

            # 暂时使用一个 ch
            half_cnt[ch] -= 1
            remaining = half_len - pos - 1       # 还需要填的位数
            cnt = perm_count(half_cnt, remaining)

            if cnt >= k:                         # 第 k 小的答案就在这里
                left.append(ch)
                # 这一次的选择已经确定，不需要再恢复计数
                break
            else:
                # 所有以 ch 为前缀的排列都不够，跳过它
                k -= cnt
                half_cnt[ch] += 1                # 恢复计数，尝试下一个字符
        else:
            # 循环结束仍未 break，说明 k 超出了所有可能
            return ""

    # ---------- 6. 组装完整的回文 ----------
    # 中间字符（如果有奇数个的话）
    middle = ''
    for ch, v in freq.items():
        if v % 2 == 1:
            middle = ch
            break

    right = ''.join(reversed(left))
    return ''.join(left) + middle + right
```

> **代码要点注释**  
> - `fact[i]` 保存 `i!`，避免每次递归里重复计算阶乘。  
> - `perm_count` 在除法后若已经大于 `k`，立即返回 `k+1`，这样可以把计数限制在 `k` 的量级，防止大整数运算过慢。  
> - 主循环里 `for ch in ...` 按字母顺序遍历，保证**字典序**的正确性。  
> - 当 `cnt >= k` 时，我们确定本位应该放 `ch`，随后进入下一位；否则把 `cnt` 从 `k` 中减掉，表示“跳过这些排列”，继续尝试更大的字符。

#### 复杂度

- **时间复杂度**：`O(26 * m)`  
  - `m = n // 2 ≤ 5000`，每个位置最多遍历 26 个字母，内部的 `perm_count` 只做常数次的除法（因为字符种类 ≤ 26），所以整体是线性级别。  
  - 与暴力的 `O(m!)` 相比，提升了 **指数级**（从天文数字降到几万次运算）。

- **空间复杂度**：`O(26 + m)`  
  - 主要是存放字符计数（最多 26）和预计算的阶乘数组（长度 `m+1`）。  
  - 与暴力需要保存所有排列的 `O(m! * n)` 相比，几乎可以忽略不计。

---

## 心得

- **核心技巧**：利用**多重排列计数**（组合数学）在构造字符串时**跳过**整块不需要的排列，从而直接定位第 `k` 小的答案。  
- **适用题型**  
  1. “第 k 小的字典序排列”类问题（如 LeetCode 1722、面试题 “第 K 大的字母序列”）。  
  2. 需要在**有重复元素**的情况下统计排列数的题目（如“不同字符的全排列计数”）。  
  3. 任何**回文重排**或**对称结构**的枚举问题（如 “Palindromic Permutations” 系列）。  
- **一句话总结**：**“先算出剩余字符还能排多少种，再用 k 把不需要的整块跳过去”**，这就是找第 k 小回文排列的钥匙。

---

## 反思

- **第一反应**：看到“回文”和“第 k 小”，我立刻想到只需要处理左半边，因为右半边是镜像的。于是想到先把左半边全排列再排序——这就是暴力思路。  
- **最容易踩的坑**  
  1. **计数溢出**：阶乘会非常大，需要在计数时做“超过 k 就直接返回” 的截断。  
  2. **奇数字符的处理**：如果有字符出现奇数次，它只能放在中间，忘记处理会导致答案错误。  
  3. **去重**：左半边有重复字符时，直接使用 `itertools.permutations` 会产生大量重复，需要用集合或计数公式去重。  
- **下次类似题的第一步**：先**把问题简化**——找出“自由度最小的部分”（这里是左半边），再**用组合计数**评估每一步的选择会产生多少种完整解，利用 k 值进行“跳过”。这样可以避免暴力枚举，直接得到答案。