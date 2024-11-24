# #2949. 计数美丽子串 II / Count Beautiful Substrings II

> 难度：困难 · 标签：Hash Table、Math、String、Number Theory、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/count-beautiful-substrings-ii/)

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

- 1 <= s.length <= 5 * 104
- 1 <= k <= 1000
- s consists of only English lowercase letters.

---

## 题目（中文翻译）

给定一个字符串 `s` 和一个正整数 `k`。  
设一个字符串中的元音字母（vowels）数量为 `vowels`，辅音字母（consonants）数量为 `consonants`。若满足以下条件，则该字符串被称为 **美丽**（beautiful）：

- `vowels == consonants`
- `vowels * consonants % k == 0`

返回字符串 `s` 中 **非空美丽子串**（substring）的个数。  
子串是字符串中连续的字符序列。

英文元音字母为 `'a'`, `'e'`, `'i'`, `'o'`, `'u'`。  
英文辅音字母为除元音外的所有小写字母。

## 示例

### 示例 1
**输入**
``` 
s = "baeyh", k = 2
```
**输出**
```
2
```
**解释**  
在给定的字符串中共有 2 个美丽子串：

- 子串 `"baeyh"`，元音 = 2（`["a","e"]`），辅音 = 2（`["y","h"]`）。满足 `vowels == consonants` 且 `vowels * consonants % k == 0`，因此是美丽的。  
- 子串 `"baey"`，元音 = 2（`["a","e"]`），辅音 = 2（`["b","y"]`）。同样满足上述条件，也是美丽的。

### 示例 2
**输入**
``` 
s = "abba", k = 1
```
**输出**
```
3
```
**解释**  
该字符串中有 3 个美丽子串：

- 子串 `"ab"`，元音 = 1（`["a"]`），辅音 = 1（`["b"]`）。  
- 子串 `"ba"`，元音 = 1（`["a"]`），辅音 = 1（`["b"]`）。  
- 子串 `"abba"`，元音 = 2（`["a","a"]`），辅音 = 2（`["b","b"]`）。

可以验证这 3 个子串满足美丽的判定条件，且不存在其他美丽子串。

### 示例 3
**输入**
``` 
s = "bcdf", k = 1
```
**输出**
```
0
```
**解释**  
该字符串中没有美丽子串。

## 约束

- `1 <= s.length <= 5 * 10^4`
- `1 <= k <= 1000`
- `s` 仅由英文小写字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有子串**，逐个统计其中的元音个数 `v` 与辅音个数 `c`，然后检查是否满足  

```
v == c                     # 元音数和辅音数相等
(v * c) % k == 0           # 两者乘积能被 k 整除
```

> **数据结构类比**  
> - 把字符串看成一排盒子，每个盒子里放的是字母。枚举子串就像让小朋友依次把**左手**指向起点、**右手**指向终点，然后把这段盒子里的字母全数数一遍。  
> - 用到的计数（元音数、辅音数）类似于 **哈希表** 查字典：键是“元音/辅音”，值是出现的次数。

**为什么正确**  
遍历所有可能的起点 `i` 与终点 `j`（`i ≤ j`），一定会检查到题目要求的每一个非空子串，只要判断条件成立，就把答案加一，最终计数必然准确。

**复杂度分析**  

- 子串的数量是 `n·(n+1)/2`（`n` 为字符串长度），每个子串要遍历一次字符来统计 `v、c`。  
- **时间复杂度**：`O(n²)`，因为我们大约要做 `n²/2` 次字符统计。  
  - “`O(n²)`” 的含义可以想象成：如果 `n=10⁴`，则大约要执行 **一亿次**的循环，远超 1 秒的计算能力。  
- **空间复杂度**：`O(1)`，只用几个计数变量。

显然，这种暴力方法在 `n ≤ 5·10⁴` 时会超时，需要进一步优化。

---

### 2. 最优解

#### 思路  

从暴力解出发，**瓶颈**在于每次子串都要重新遍历内部字符。我们需要把“统计元音/辅音的过程” **前缀化**，让子串的统计可以 **O(1)** 完成。

---

#### 2.1 关键观察  

1. **元音 = 辅音**  
   设子串长度为 `L`，元音数为 `v`，辅音数为 `c`。  
   条件 `v == c` ⇒ `L = v + c = 2·v`，**子串长度一定是偶数**。  

2. **乘积可被 k 整除**  
   由于 `v == c`，`v·c = v²`，所以只要 `v² % k == 0` 即可。  
   换句话说，只要 `v` 是满足 `v²` 能被 `k` 整除的整数即可。

3. **把 `v² % k == 0` 用最小公倍数表示**  
   对 `k` 做质因数分解  

   ```
   k = p1^a1 * p2^a2 * ... * pt^at
   ```

   为了让 `v²` 包含每个 `pi` 的指数至少为 `ai`，  
   `v` 至少要包含 `pi^{ceil(ai/2)}`。  
   定义  

   ```
   M = product over i of pi^{ceil(ai/2)}
   ```

   那么 **所有满足 `v² % k == 0` 的 v 正好是 M 的整数倍**。  
   也就是说，子串满足条件 ⇔  

   - 元音数 = 辅音数 (= v)  
   - `v` 能被 `M` 整除（`v % M == 0`）

4. **前缀差值的等价转换**  

   用 `prefV[i]` 表示前 `i`（不含第 `i`）字符的元音个数。  
   对任意子串 `s[l … r]`（左闭右开），有  

   ```
   v = prefV[r] - prefV[l]
   length L = r - l
   ```

   条件 `v == L/2` 等价于  

   ```
   2·v - L = 0
   2·(prefV[r] - prefV[l]) - (r - l) = 0
   (2·prefV[r] - r)  ==  (2·prefV[l] - l)
   ```

   因此我们可以定义一个 **键值**  

   ```
   key[i] = 2·prefV[i] - i          (i 从 0 到 n)
   ```

   两个前缀 `i < j` 只要 `key[i] == key[j]`，对应的子串必然满足 `v == c`。

5. **把 “v 能被 M 整除” 也写成前缀的形式**  

   `v = prefV[j] - prefV[i]`，要求 `v % M == 0` ⇔  

   ```
   (prefV[j] - prefV[i]) % M == 0
   ⇔ prefV[j] % M == prefV[i] % M
   ```

   于是**只要**两个前缀满足：

   - `key` 相同（保证元音=辅音）
   - `prefV % M` 相同（保证 v 能被 M 整除）

   那么对应的子串一定是 **美丽子串**。

> **核心结论**  
> 把原问题转化为：在所有前缀 `0 … n` 中，统计 **同一组** `(key, prefV % M)` 出现的次数，任意两次出现之间对应的子串都是满足条件的。

---

#### 2.2 具体算法  

1. **求 M**  
   - 对 `k` 进行质因数分解（`k ≤ 1000`，直接试除即可）。  
   - 对每个质因数 `p^a`，把 `p^{ceil(a/2)}` 乘到 `M` 中。  
   - 特殊情况：`k == 1` 时 `M = 1`。

2. **遍历前缀**（包括空前缀 `i = 0`）  
   - `prefV` : 累计元音数。  
   - `key = 2 * prefV - i`。  
   - `mod = prefV % M`（当 `M == 1` 时 `mod` 恒为 0）。  
   - 使用一个两层哈希表 `cnt`：`cnt[key][mod]` 记录到目前为止出现过的 `(key, mod)` 的次数。  
   - 当前前缀可以与之前所有相同 `(key, mod)` 的前缀配对，贡献 `cnt[key][mod]` 条美丽子串。  
   - 然后把 `cnt[key][mod]` 加一，表示自己也加入到以后配对的候选中。

3. **答案即所有配对的累计和**。

---

#### 2.3 正确性证明  

我们要证明算法返回的计数等于题目要求的美丽子串数。

---

**Lemma 1**  
对于任意子串 `s[l … r-1]`（左闭右开），设  

```
v = #元音 in the substring
c = #辅音 in the substring
```

则 `v == c` 当且仅当 `key[l] == key[r]`，其中 `key[i] = 2·prefV[i] - i`。

*Proof.*  

```
v = prefV[r] - prefV[l]
c = (r - l) - v
```

`v == c` ⇔ `v = (r-l)/2` ⇔ `2·v = r - l` ⇔  

```
2·(prefV[r] - prefV[l]) = r - l
⇔ 2·prefV[r] - r = 2·prefV[l] - l
⇔ key[r] = key[l]
```

两式等价，证毕。 ∎



**Lemma 2**  
设 `M` 为满足 `v² % k == 0 ⇔ v % M == 0` 的最小正整数（算法第 1 步得到的值）。  
则对于任意整数 `v`，`v² % k == 0` 当且仅当 `v % M == 0`。

*Proof.*  

`M` 的构造保证 `M²` 能被 `k` 整除，并且对任意 `v`，若 `v` 能被 `M` 整除，则 `v = t·M`，  

```
v² = t²·M²  →  k | M²  →  k | v²
```

反之，若 `k | v²`，在每个质因数 `p` 的指数上，`v` 必须至少含有 `ceil(ai/2)` 次方，正好是 `M` 的因子，所以 `M | v`。 ∎



**Lemma 3**  
对于任意子串 `s[l … r-1]`，设 `v = #元音`。  
`v % M == 0` 当且仅当 `prefV[l] % M == prefV[r] % M`。

*Proof.*  

`v = prefV[r] - prefV[l]`，两边同余 `mod M`：

```
v ≡ prefV[r] - prefV[l] (mod M)
v % M == 0  ⇔  prefV[r] ≡ prefV[l] (mod M)
⇔  prefV[r] % M == prefV[l] % M
```

∎



**Lemma 4**  
子串 `s[l … r-1]` 是美丽子串（即 `v == c` 且 `v² % k == 0`）  
**当且仅当** 前缀 `l` 与前缀 `r` 满足  

```
key[l] == key[r]          (元音=辅音)
prefV[l] % M == prefV[r] % M   (v 能被 M 整除)
```

*Proof.*  
由 Lemma 1 获得 `v == c ⇔ key[l] == key[r]`。  
由 Lemma 2 与 Lemma 3，`v² % k == 0 ⇔ v % M == 0 ⇔ prefV[l] % M == prefV[r] % M`。  
两者同时成立即为美丽子串的定义。 ∎



**Lemma 5**  
遍历前缀时，每当我们在位置 `r` 看到已有的 `cnt[key][mod]`，把它加到答案中，恰好计数了所有以 `r` 为右端点的美丽子串。

*Proof.*  
固定右端点 `r`，所有满足美丽条件的左端点 `l` 必须满足 Lemma 4 中的两条等式。  
`key[l]` 与 `key[r]` 相同且 `prefV[l] % M` 与 `mod = prefV[r] % M` 相同。  
`cnt[key][mod]` 正好记录了在当前遍历之前出现过的前缀 `(key, mod)` 的数量，也就是所有合法的 `l`。  
因此把该数加入答案，即统计了所有以 `r` 为右端点的美丽子串。 ∎



**Theorem**  
算法的最终答案等于题目要求的 **非空美丽子串的个数**。

*Proof.*  
遍历所有前缀 `r = 0 … n`（其中 `r = 0` 代表空前缀），依据 Lemma 5 累加了每个右端点对应的合法左端点数。  
每一对满足条件的 `(l, r)` 对应唯一的非空子串 `s[l … r-1]`，且所有美丽子串都会在其右端点 `r` 时被计入一次。  
没有重复计数，也没有遗漏，故累计和即为答案。 ∎



#### 代码（Python）

```python
from collections import defaultdict
import sys

def smallest_M(k: int) -> int:
    """返回满足 v^2 % k == 0 当且仅当 v % M == 0 的最小正整数 M"""
    if k == 1:
        return 1
    M = 1
    x = k
    p = 2
    while p * p <= x:
        if x % p == 0:
            cnt = 0
            while x % p == 0:
                x //= p
                cnt += 1
            # 需要的指数是 ceil(cnt/2)
            need = (cnt + 1) // 2
            M *= p ** need
        p += 1
    # 处理剩下的一个质因数（如果有）
    if x > 1:
        # 只出现一次，cnt = 1，need = 1
        M *= x
    return M


def count_beautiful_substrings(s: str, k: int) -> int:
    """核心函数，返回美丽子串的数量"""
    M = smallest_M(k)                # 第一步：求 M
    # 两层哈希表：外层 key -> 内层 dict (mod -> 出现次数)
    cnt = defaultdict(lambda: defaultdict(int))

    pref_vowel = 0                    # 前缀元音数
    ans = 0

    # 先把空前缀 (i = 0) 放进去
    key = 0                           # 2*0 - 0
    mod = 0 % M
    cnt[key][mod] = 1

    vowels = set('aeiou')
    for i, ch in enumerate(s, 1):     # i 为前缀长度（从 1 开始）
        if ch in vowels:
            pref_vowel += 1

        key = 2 * pref_vowel - i      # 2*prefV - index
        mod = pref_vowel % M

        # 所有之前出现相同 (key, mod) 的前缀都可以和当前位置组成美丽子串
        ans += cnt[key][mod]

        # 把当前前缀计入哈希表，供后面的右端点使用
        cnt[key][mod] += 1

    return ans


# -------------------------------------------------------------
if __name__ == "__main__":
    # 读取示例或自测
    data = sys.stdin.read().strip().split()
    if not data:
        sys.exit(0)
    s = data[0]
    k = int(data[1])
    print(count_beautiful_substrings(s, k))
```

**代码要点解释（中文注释已在代码中）**  

- `smallest_M`：用 trial division（试除）把 `k` 分解成质因数，按 `ceil(exp/2)` 计算 `M`。  
- `cnt`：`defaultdict` 嵌套，`cnt[key][mod]` 记录到目前为止出现的前缀数量。  
- 遍历时维护 `pref_vowel`（累计元音数），实时计算 `key` 与 `mod`，利用哈希表直接得到可以配对的左端点数量。  
- 时间复杂度 `O(n)`，空间复杂度 `O(n)`（最坏情况每个前缀的 `(key, mod)` 都不相同）。

---

#### 复杂度

- **时间复杂度**：`O(n)`，只遍历一次字符串，所有哈希表操作均为均摊 `O(1)`。  
  - 与暴力解 `O(n²)` 相比，提升了 **数百倍**，即使 `n = 5·10⁴` 也能在毫秒级完成。

- **空间复杂度**：`O(n)`，需要存储每个前缀的 `(key, mod)` 计数。  
  - 实际上键的种类远小于 `n`（因为 `key` 与 `mod` 的取值受限），通常更接近 `O(n)` 的常数因子。

---

## 心得

- **核心技巧**：把“元音数 = 辅音数”用前缀差 `key = 2·prefV - index` 表示；把“`v²` 能被 `k` 整除”化为 “`v` 能被 `M` 整除”，进一步写成前缀模 `M` 相等。于是整个问题变成 **统计前缀的两维属性相同的配对**，可以用哈希表一次遍历完成。
- **适用场景**  
  1. 需要同时满足“**两个前缀属性相等**”的子串计数（如 “前缀和相等” 与 “前缀异或相等” 的组合）。  
  2. 条件可以拆解为 “**差值为 0**” 与 “**差值满足模数约束**” 的情形（例如 “子数组和为 0 且长度为偶数”）。
- **一句话总结**：把两个独立的约束都写成前缀的等式，利用哈希表把相同的前缀配对，即可在一次遍历中得到所有满足条件的子串。

---

## 反思

- **第一反应**：看到“元音数 * 辅音数 % k == 0”，立刻想到枚举子串、逐个计数，结果超时。  
- **最容易踩的坑**  
  1. 忽略了 `v == c` 已经暗含子串长度必须为偶数，直接统计奇数长度会导致错误答案。  
  2. 误以为 `v² % k == 0` 需要枚举所有 `v`，其实只要求出最小公倍数 `M`，条件即可化为模等式，大幅简化。  
  3. 处理 `k = 1` 时的特例：此时 `M = 1`，所有 `v` 都合法，算法仍能统一处理（因为 `mod` 恒为 0），但若忘记初始化空前缀，会少计一个子串。  
- **下次类似题的第一步**：先把“子串属性的等式”转化为 **前缀差的等式**，检查是否还能再加入 **模数约束**，然后思考是否可以用哈希表一次统计配对。这样往往可以把原本的 `O(n²)` 降到 `O(n)`。