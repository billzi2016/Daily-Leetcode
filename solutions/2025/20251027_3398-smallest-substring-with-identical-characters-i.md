# #3398. 最小相同字符子串 I / Smallest Substring With Identical Characters I

> 难度：困难 · 标签：Array、Binary Search、Enumeration · [LeetCode 链接](https://leetcode.com/problems/smallest-substring-with-identical-characters-i/)

---

## 题目（英文原版）

**Description**

You are given a binary string s of length n and an integer numOps.
You are allowed to perform the following operation on s at most numOps times:
You need to minimize the length of the longest substring of s such that all the characters in the substring are identical.
Return the minimum length after the operations.

**Examples**

**Example 1:**

```
Input: s = "000001", numOps = 1
Output: 2
Explanation:
By changing s[2] to '1' , s becomes "001001" . The longest substrings with identical characters are s[0..1] and s[3..4] .
```

**Example 2:**

```
Input: s = "0000", numOps = 2
Output: 1
Explanation:
By changing s[0] and s[2] to '1' , s becomes "1010" .
```

**Example 3:**

```
Input: s = "0101", numOps = 0
Output: 1
```

**Constraints**

- 1 <= n == s.length <= 1000
- s consists only of '0' and '1'.
- 0 <= numOps <= n

---

## 题目（中文翻译）

**题目描述**  
给定一个二进制字符串（binary string）`s`，其长度为 `n`，以及一个整数 `numOps`。  
你最多可以对 `s` 执行 `numOps` 次以下操作：  
- 任选一个字符并将其从 `'0'` 改为 `'1'`，或从 `'1'` 改为 `'0'`。

在完成至多 `numOps` 次操作后，需要 **最小化** `s` 中 **最长子串（substring）** 的长度，使得该子串内的所有字符都相同。  
返回在最优操作方案下可以得到的最小长度。

**示例**  

**示例 1**  
输入: `s = "000001", numOps = 1`  
输出: `2`  
解释:  
将 `s[2]` 改为 `'1'`，得到 `"001001"`。此时最长的相同字符子串为 `s[0..1]` 和 `s[3..4]`，长度均为 `2`。

**示例 2**  
输入: `s = "0000", numOps = 2`  
输出: `1`  
解释:  
将 `s[0]` 和 `s[2]` 改为 `'1'`，得到 `"1010"`。此时所有相同字符子串的长度均为 `1`。

**示例 3**  
输入: `s = "0101", numOps = 0`  
输出: `1`  

**约束条件**  
- `1 <= n == s.length <= 1000`  
- `s` 仅由字符 `'0'` 和 `'1'` 组成。  
- `0 <= numOps <= n`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **“最多可以改 numOps 次”** 当成“可以任选 numOps 个位置把 0↔1”。  
于是：

1. 从字符串的每一个位置出发，枚举所有 **不超过 numOps** 的改动组合（相当于从 `n` 个位置里挑出 `0…numOps` 个）。
2. 对每一种改动后得到的新字符串，遍历一遍计算**最长的相同字符子串长度**（比如 “00011100” 的最长相同子串是长度 3）。
3. 把所有可能的答案取最小值，即为最终答案。

> **生活化类比**：把字符串想成一本只有两种字母的“词典”。我们手里有 `numOps` 支笔，可以把任意几页的字母改成另一种。暴力做法就是把每一种可能的改页方式都尝试一次，再去看看哪本改完后“最长的同字页”最短。

**为什么正确**：因为我们穷举了**所有**合法的改动方案，答案一定会在其中出现。

#### 代码（Python）

```python
from itertools import combinations
from typing import List

def longest_same_substring(t: str) -> int:
    """返回字符串 t 中最长的全相同字符子串长度"""
    max_len = 1
    cur = 1
    for i in range(1, len(t)):
        if t[i] == t[i-1]:
            cur += 1
            max_len = max(max_len, cur)
        else:
            cur = 1
    return max_len

def brute_force(s: str, numOps: int) -> int:
    n = len(s)
    ans = n                               # 最坏情况：全都是相同字符
    # 枚举改动次数 0 ~ numOps
    for k in range(numOps + 1):
        # 从 n 个位置里任选 k 个位置进行翻转
        for idxs in combinations(range(n), k):
            lst = list(s)
            for i in idxs:                # 把选中的位置翻转
                lst[i] = '1' if lst[i] == '0' else '0'
            cur_len = longest_same_substring(''.join(lst))
            ans = min(ans, cur_len)       # 取最小的最大子串长度
    return ans
```

> **关键行中文注释** 已写在代码里。  
> 这段代码在 `n ≤ 10` 时还能跑完，`n = 1000` 时就会“卡死”。

#### 复杂度  

- **时间复杂度**：  
  \[
  O\Big(\sum_{k=0}^{\text{numOps}} \binom{n}{k} \cdot n\Big)
  \]  
  直观解释就是：先挑出所有可能的改动组合（组合数会指数级增长），每种组合再遍历一次字符串求最长相同子串。  
  当 `numOps` 接近 `n` 时，这个式子相当于 `O(2^n * n)`，几乎不可能在 1 秒内算完。

- **空间复杂度**：  
  只用了常数级别的额外空间（`O(1)`），除了递归/循环中保存的临时字符串。

> 暴力解帮助我们弄清楚**问题的本质**：每一次翻转都是在把一段“太长的相同字符块”切成更小的块。接下来我们要想办法**快速判断**在给定的最大块长度 `L` 下，需要多少次翻转才能实现。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正的难点是判断**：在限制 `numOps` 次翻转的情况下，**最长相同字符子串能否被压到不超过 L**？  
如果我们能在 **O(n)** 时间内回答这个“判定问题”，再配合 **二分搜索**（Binary Search）在 `[1, n]` 区间上找最小的可行 `L`，整体复杂度就会是 `O(n log n)`，完全可以接受。

---

##### 2.1 先定位瓶颈  

暴力解的慢点在于 **枚举所有翻转组合**。  
实际上，翻转只会出现在 **原本的相同字符块（run）内部**，因为把不同字符之间的空隙翻转不会帮助缩短最长块。  
所以我们只需要考虑 **每个连续块的长度**。

---

##### 2.2 关键观察  

设原字符串中有一段连续的相同字符，长度为 `len`。  
如果我们要求 **最终每段相同字符的长度 ≤ L**，这段 `len` 必须被 **切割** 成若干段，每段长度 ≤ L。

- 要切成 `ceil(len / L)` 段，需要在内部插入 `ceil(len / L) - 1` 个翻转（把某个位置的字符改成相反的），这样就把原来的长块“砍断”了。

因此，对于整个字符串：

```
需要的最少翻转次数 = Σ ( ceil(len_i / L) - 1 )
                      对每个原始块 i
```

只要这个总数 ≤ `numOps`，就说明 **“可以把最长块压到 L 以下”**。

> **类比**：把每段长块想成一根绳子，目标是让每根绳子长度 ≤ L。每剪一次绳子就相当于一次翻转。我们只需要算出把所有绳子都剪到合格长度最少要几刀，判断这几刀是否在我们手头的刀数 `numOps` 之内。

---

##### 2.3 判定函数 `can(L)`

实现思路：

1. **遍历一次字符串**，统计连续相同字符的长度 `len`（用两个指针或计数器）。
2. 对每个 `len`，累计 `ops += (len - 1) // L`。  
   解释：`ceil(len / L) - 1` 等价于 `(len - 1) // L`（整数除法更直接）。
3. 如果遍历结束后 `ops ≤ numOps`，返回 `True`，否则 `False`。

整个过程只用一次线性扫描，时间 **O(n)**，空间 **O(1)**。

---

##### 2.4 二分搜索找最小 L  

- 左边界 `lo = 1`（最小可能的最长块长度）。  
- 右边界 `hi = n`（原字符串全相同时的上限）。  
- 每次取中点 `mid = (lo + hi) // 2`，调用 `can(mid)`：
  - 若 `True` → 说明可以把最长块压到 `mid`，于是尝试更小的值：`hi = mid - 1`，并记录答案 `ans = mid`。
  - 若 `False` → 说明 `mid` 太小，需要更大的上限：`lo = mid + 1`。

二分结束后 `ans` 即为**最小可能的最长相同子串长度**。

---

#### 代码（Python）

```python
def smallestLongestSubstring(s: str, numOps: int) -> int:
    """
    返回在至多 numOps 次翻转后，最长相同字符子串的最小可能长度。
    思路：二分搜索 + O(n) 判定函数。
    """

    n = len(s)

    # ---------- 判定函数 ----------
    def can(L: int) -> bool:
        """
        判断是否能把所有相同字符块的长度压到 ≤ L
        只需要统计每段原始块的长度，累加所需翻转次数。
        """
        ops_needed = 0          # 累计需要的翻转次数
        i = 0
        while i < n:
            j = i
            # 找出以 i 为起点的相同字符块 [i, j)
            while j < n and s[j] == s[i]:
                j += 1
            length = j - i       # 当前块的长度
            # 把长度为 length 的块切成每段 ≤ L 需要的最少翻转次数
            # 等价于 ceil(length / L) - 1，使用整数除法写法更简洁
            ops_needed += (length - 1) // L
            if ops_needed > numOps:   # 早停，省去后面的无用遍历
                return False
            i = j                # 开始下一个块
        return ops_needed <= numOps

    # ---------- 二分搜索 ----------
    lo, hi = 1, n
    ans = n                      # 最坏情况：全相同，答案就是 n
    while lo <= hi:
        mid = (lo + hi) // 2
        if can(mid):             # 可以做到，尝试更小的 L
            ans = mid
            hi = mid - 1
        else:                    # 做不到，需要更大的 L
            lo = mid + 1
    return ans
```

> **关键行中文注释** 已在代码中标明。  
> 这段代码在 `n = 1000`、`numOps = 500` 的极端情况下也能在毫秒级完成。

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 二分搜索最多进行 `log₂ n`（约 10 次）迭代。  
  - 每次迭代的判定函数只遍历一次字符串 `O(n)`。  
  - 与暴力解的指数级时间相比，`n = 1000` 时仅需几千次基本操作，几乎是瞬间完成。

- **空间复杂度**：`O(1)`  
  - 只用了几个整数变量，没有额外的数组或递归栈。

> 与暴力解相比，**时间从指数级降到了线性乘对数级**，是本题的关键突破。

---

## 心得

- **核心技巧**：把“最长相同字符子串 ≤ L”转化为“每段原始块需要切多少刀”，再用**二分搜索**在答案空间 `[1, n]` 上寻找最小可行值。
- **此技巧的适用场景**  
  1. “在有限次数的操作下，使某个数值不超过阈值”——如 `Maximum Frequency`（把数组中元素增至最多出现次数）  
  2. “把区间长度限制在某个值内”——如 `Split Array Largest Sum`（把数组划分成子数组，使最大子数组和最小）  
  3. “在限定次数的修改后，使序列满足单调/相等”等约束的二分判定类题目。

- **一句话总结解题钥匙**：**把全局最坏指标转化为局部“切割次数”，二分答案空间即可快速验证。**

---

## 反思

- **第一反应**：直接枚举所有翻转组合，想把每种可能都算一遍——这在思路上是对的，只是没有意识到搜索空间太大。
- **最容易踩的坑**  
  - **漏算边界**：块的长度正好是 `L` 时不需要翻转，公式 `(len-1)//L` 正好处理了这种情况。  
  - **提前退出**：在判定函数里，一旦累计的翻转次数已经超过 `numOps`，应立即返回 `False`，否则会不必要地遍历剩余字符导致时间稍微增大。  
  - **二分的闭区间写法**：要注意 `hi = mid - 1` 与 `lo = mid + 1` 的边界更新，否则会出现死循环。

- **下次遇到同类题**：第一步先思考 **“如果我们已经知道目标值 L，如何在 O(n) 检查是否可行？”**；如果能写出单调判定函数（可行 → 所有更大的 L 也必定可行），再使用二分搜索找最优答案。这样可以把“指数搜索”直接压缩到 “对数搜索”。