# #2947. **统计美丽子串 I** / Count Beautiful Substrings I

> 难度：中等 · 标签：Hash Table、Math、String、Enumeration、Number Theory、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/count-beautiful-substrings-i/)

---

## 题目（英文原版）

**Description**

You are given a string s and a positive integer k.
Let vowels and consonants be the number of vowels and consonants in a string.
A string is beautiful if:
Return the number of non-empty beautiful substrings in the given string s.
A substring is a contiguous sequence of characters in a string.
Vowel letters in English are 'a', 'e', 'i', 'o', and 'u'.
Consonant letters in English are every letter except vowels.

**Examples**

**Example 1:**

```
Input: s = "baeyh", k = 2
Output: 2
Explanation: There are 2 beautiful substrings in the given string.
- Substring "baeyh", vowels = 2 (["a",e"]), consonants = 2 (["y","h"]).
You can see that string "aeyh" is beautiful as vowels == consonants and vowels * consonants % k == 0.
- Substring "baeyh", vowels = 2 (["a",e"]), consonants = 2 (["b","y"]). 
You can see that string "baey" is beautiful as vowels == consonants and vowels * consonants % k == 0.
It can be shown that there are only 2 beautiful substrings in the given string.
```

**Example 2:**

```
Input: s = "abba", k = 1
Output: 3
Explanation: There are 3 beautiful substrings in the given string.
- Substring "abba", vowels = 1 (["a"]), consonants = 1 (["b"]). 
- Substring "abba", vowels = 1 (["a"]), consonants = 1 (["b"]).
- Substring "abba", vowels = 2 (["a","a"]), consonants = 2 (["b","b"]).
It can be shown that there are only 3 beautiful substrings in the given string.
```

**Example 3:**

```
Input: s = "bcdf", k = 1
Output: 0
Explanation: There are no beautiful substrings in the given string.
```

**Constraints**

- 1 <= s.length <= 1000
- 1 <= k <= 1000
- s consists of only English lowercase letters.

---

## 题目（中文翻译）

给定一个仅由小写英文字母组成的字符串 `s` 和一个正整数 `k`。  
设 **vowels** 为字符串中元音字母的个数，**consonants** 为辅音字母的个数。  

若一个字符串同时满足以下条件，则称其为 **美丽**（beautiful）：

- `vowels == consonants`  
- `vowels * consonants % k == 0`

返回字符串 `s` 中 **非空** 美丽子串（substring）的数量。  
子串是字符串中连续的一段字符序列。

英文字母中的元音字母为 `'a'`, `'e'`, `'i'`, `'o'`, `'u'`。  
英文字母中的辅音字母是除元音之外的所有字母。

---

### 示例

#### 示例 1
```text
Input: s = "baeyh", k = 2
Output: 2
Explanation: 共有 2 个美丽子串。
- 子串 "aeyh"，vowels = 2 (["a","e"])，consonants = 2 (["y","h"])。满足 vowels == consonants 且 2*2 % 2 == 0。
- 子串 "baey"，vowels = 2 (["a","e"])，consonants = 2 (["b","y"])。满足 vowels == consonants 且 2*2 % 2 == 0。
```

#### 示例 2
```text
Input: s = "abba", k = 1
Output: 3
Explanation: 共有 3 个美丽子串。
- 子串 "ab"，vowels = 1 (["a"])，consonants = 1 (["b"])。
- 子串 "ba"，vowels = 1 (["a"])，consonants = 1 (["b"])。
- 子串 "abba"，vowels = 2 (["a","a"])，consonants = 2 (["b","b"])。
```

#### 示例 3
```text
Input: s = "bcdf", k = 1
Output: 0
Explanation: 没有美丽子串。
```

---

### 约束

- `1 <= s.length <= 1000`
- `1 <= k <= 1000`
- `s` 仅由英文小写字母组成。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有可能的子串都枚举出来，逐个检查它们是否满足“美丽”的条件。  

- **枚举子串**：对左端点 `l`（0 ≤ l < n），再对右端点 `r`（l+1 ≤ r ≤ n）遍历，子串就是 `s[l:r]`（左闭右开）。这相当于在生活中把一根绳子从每一个可能的起点剪开，再从每一个后面的点剪断，得到所有连续的“小段”。  
- **统计元音/辅音**：遍历子串的每个字符，用一个集合 `{'a','e','i','o','u'}` 判断它是元音还是辅音，分别累加计数 `vowels`、`cons`.  
- **判断美丽**：子串满足  
  1. `vowels == cons`（元音数等于辅音数）  
  2. `vowels * cons % k == 0`（元音数与辅音数的乘积能被 `k` 整除）  

只要这两个条件都成立，就把答案加一。

> **为什么暴力法一定是对的？**  
> 因为我们把**所有**可能的子串都检查了一遍，任何满足条件的子串都会被计数，任何不满足的子串都不会计数，所以答案必然是正确的。

#### 代码（Python）

```python
def count_beautiful_substrings_bruteforce(s: str, k: int) -> int:
    vowels_set = {'a', 'e', 'i', 'o', 'u'}      # 元音集合，像查字典一样判断
    n = len(s)
    ans = 0

    # 枚举左端点 l
    for l in range(n):
        vowels = 0          # 当前子串的元音计数
        cons = 0            # 当前子串的辅音计数

        # 枚举右端点 r（右端点是开区间，所以从 l 开始往右扩展）
        for r in range(l, n):
            if s[r] in vowels_set:   # 判断字符是元音还是辅音
                vowels += 1
            else:
                cons += 1

            # 只要子串非空，就检查美丽条件
            if vowels == cons and (vowels * cons) % k == 0:
                ans += 1

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 解释：外层遍历 `n` 次，内层最坏也要遍历 `n` 次，合在一起就是大约 `n·n/2` 次操作。`O(n²)` 可以理解为“如果 `n` 是 1000，最多要做 1,000,000 次”。  
- **空间复杂度**：`O(1)`  
  - 只用了常数个计数变量，不会随 `n` 增长而占用更多内存。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于每次子串扩展都重新遍历字符来统计元音/辅音，导致二次循环。我们需要把“统计”这件事搬到 **前缀** 上，只在 **一次** 遍历中完成。

---

#### 2.1 把条件用前缀表达  

设  

- `prefV[i]` = 前 `i` 个字符（下标 `[0,i)`）里元音的个数。  
- `prefC[i]` = 前 `i` 个字符里辅音的个数。  

则任意子串 `s[l:r]`（`0 ≤ l < r ≤ n`）的元音数和辅音数分别是  

```
v = prefV[r] - prefV[l]
c = prefC[r] - prefC[l]
```

**条件 1**：`v == c`  
⇔ ` (prefV[r] - prefV[l]) - (prefC[r] - prefC[l]) == 0`  
⇔ `(prefV[r] - prefC[r]) == (prefV[l] - prefC[l])`  

把 `diff[i] = prefV[i] - prefC[i]` 记作“元音与辅音的差”。  
于是 **条件 1** 要求子串两端的 `diff` 相等——这正像“在数轴上走了一段后回到原点”。  

**条件 2**：`v * c % k == 0`  
因为 `v == c`，记 `t = v = c`，则 `t*t % k == 0`，即 `t²` 能被 `k` 整除。

> **数学小技巧**：要让 `t²` 能被 `k` 整除，只要 `t` 本身是 `k` 的 **平方根的倍数**（但不一定是整数根）。更精确地，若  
> `k = Π p_i^{e_i}`（质因数分解），则 `t` 必须包含每个质因子 `p_i` 至少 `ceil(e_i / 2)` 次。  
> 把这些最小次数乘起来得到一个数 `need`，满足 `need² % k == 0` 且 `need` 最小。于是 **条件 2** 等价于 `t % need == 0`。

> **类比**：把 `need` 想成“一把钥匙”。只有当元音数（也是辅音数）是这把钥匙的整数倍时，才可以打开“乘积被 k 整除”的锁。

---

#### 2.2 归纳为“同 diff 且同模”

子串美丽 ⇔  

1. `diff[l] == diff[r]`（两端差相同）  
2. `t = prefV[r] - prefV[l]` 能被 `need` 整除，即 `prefV[r] % need == prefV[l] % need`

于是我们只需要在一次遍历中，记录 **每个 `diff` 下，各个 `prefV % need` 出现的次数**。  

- 当遍历到位置 `i`（对应前缀 `s[0:i]`）时，已知当前 `diff_i` 与 `mod_i = prefV[i] % need`。  
- 之前出现过相同 `(diff, mod)` 的前缀数量，就是以当前 `i` 为右端点的美丽子串数。  
- 然后把当前 `(diff, mod)` 加入统计，继续向后走。

这相当于在“同一条河流（diff）上”，我们只关心“河里每块石头的颜色（mod）”。每当我们踩到同颜色的石头，就能找到一段闭合的区间。

---

#### 2.3 计算 `need`

```python
def minimal_need(k: int) -> int:
    need = 1
    d = k
    p = 2
    while p * p <= d:
        if d % p == 0:
            e = 0
            while d % p == 0:
                d //= p
                e += 1
            need *= p ** ((e + 1) // 2)   # ceil(e/2)
        p += 1
    if d > 1:            # 剩下的质因子是一个大于 sqrt(k) 的素数
        need *= d        # e == 1 => ceil(1/2) = 1
    return need
```

时间复杂度 `O(√k)`，因为 `k ≤ 1000`，这几乎可以忽略不计。

---

#### 代码（Python）

```python
def count_beautiful_substrings(s: str, k: int) -> int:
    # ---------- 1. 计算 need ----------
    def minimal_need(k: int) -> int:
        need = 1
        d = k
        p = 2
        while p * p <= d:
            if d % p == 0:
                e = 0
                while d % p == 0:
                    d //= p
                    e += 1
                need *= p ** ((e + 1) // 2)   # ceil(e/2)
            p += 1
        if d > 1:            # 余下的质因子
            need *= d
        return need

    need = minimal_need(k)                     # 需要的最小倍数

    # ---------- 2. 前缀遍历 ----------
    vowels = {'a', 'e', 'i', 'o', 'u'}          # 判断元音的“字典”
    diff = 0                                    # 当前前缀的 diff = #vowel - #cons
    pref_vowel = 0                              # 当前前缀的元音数
    ans = 0

    # map: diff -> {mod值: 出现次数}
    from collections import defaultdict
    cnt = defaultdict(lambda: defaultdict(int))
    cnt[0][0] = 1                               # 空前缀：diff=0, prefV%need=0

    for ch in s:
        if ch in vowels:
            pref_vowel += 1
            diff += 1          # 元音多了，diff 加 1
        else:
            diff -= 1          # 辅音多了，diff 减 1

        mod = pref_vowel % need

        # 统计以当前位置为右端点的美丽子串数
        ans += cnt[diff][mod]

        # 把当前前缀加入统计，供后面的右端点使用
        cnt[diff][mod] += 1

    return ans
```

> **代码注释**  
> - 第 1 部分把数学结论转化为一个函数 `minimal_need`，相当于先把“钥匙”锻造好。  
> - 第 2 部分一次遍历字符串，实时维护 `diff` 与 `pref_vowel`，并用两层哈希表 `cnt` 记录出现次数。每来到新位置，就把已经出现的相同 `(diff, mod)` 加到答案中——这一步相当于“在同一条河上找到同颜色的石头”。  

---

#### 复杂度  

- **时间复杂度**：`O(n + √k)`  
  - `O(n)` 来自一次线性遍历字符串。  
  - `O(√k)` 来自计算 `need`（`k ≤ 1000`，几乎可以忽略）。  
  - 与暴力的 `O(n²)` 相比，**从“每两两比较”降到“一次走完”**，即使 `n` 达到 10⁵ 也能轻松应付。  

- **空间复杂度**：`O(n)`（最坏情况）  
  - 我们在 `cnt` 中存储每个不同的 `diff` 与对应的 `mod` 出现次数。`diff` 的取值范围是 `[-n, n]`，`mod` 的取值范围是 `[0, need-1]`，两者的组合最多 `O(n)` 条目。  
  - 只用了若干整数变量和哈希表，符合题目 1000 长度的限制。

---

## 心得  

- **核心技巧**：把“元音数等于辅音数”转化为前缀差相等；把 “乘积能被 k 整除” 用质因数分解转化为 “元音数能被一个固定的 `need` 整除”。  
- **适用场景**：  
  1. **相等计数类子串**（如“子串中 0 与 1 数相等”）——常用前缀差 + 哈希表。  
  2. **乘积/和满足模条件的子串**——把乘积/和的约束化为前缀值的同余或可除性。  
  3. **需要额外数值约束的相等计数**——先把额外约束抽象为“前缀值的同余”。  
- **一句话总结解题钥匙**：`diff` 相同保证“元音=辅音”，`prefV % need` 相同保证“元音数能被 need 整除”。两者同时满足即是美丽子串。

---

## 反思  

- **第一反应**：看到“元音数 = 辅音数”，立刻想到前缀差的技巧；但最开始会忽视乘积可除的约束，导致只能暴力。  
- **最容易踩的坑**：  
  1. **`need` 计算错误**——忘记对每个质因子的指数取上取整 `(e+1)//2`。  
  2. **模运算时 `need = 1`**——当 `need = 1` 时，`prefV % need` 恒为 0，仍需正常计数，代码不能因为除以 0 报错。  
  3. **空前缀的初始化**——忘记把 `(diff=0, mod=0)` 计数为 1，会少算以开头为左端点的子串。  
- **下次类似题目第一步**：先写出 **前缀差**（或前缀和）把“等号”条件转化为 “前缀值相等”，再检查是否还有乘积/模之类的二次约束，思考能否把它也写成 **前缀值的同余** 或 **可整除** 条件。这样往往可以把二次循环压到一次遍历。