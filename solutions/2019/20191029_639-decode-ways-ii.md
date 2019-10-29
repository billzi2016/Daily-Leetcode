# #639. 解码方法 II / Decode Ways II

> 难度：困难 · 标签：String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/decode-ways-ii/)

---

## 题目（英文原版）

**Description**

A message containing letters from A-Z can be encoded into numbers using the following mapping:
To decode an encoded message, all the digits must be grouped then mapped back into letters using the reverse of the mapping above (there may be multiple ways). For example, "11106" can be mapped into:
Note that the grouping (1 11 06) is invalid because "06" cannot be mapped into 'F' since "6" is different from "06".
In addition to the mapping above, an encoded message may contain the '*' character, which can represent any digit from '1' to '9' ('0' is excluded). For example, the encoded message "1*" may represent any of the encoded messages "11", "12", "13", "14", "15", "16", "17", "18", or "19". Decoding "1*" is equivalent to decoding any of the encoded messages it can represent.
Given a string s consisting of digits and '*' characters, return the number of ways to decode it.
Since the answer may be very large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
'A' -> "1"
'B' -> "2"
...
'Z' -> "26"
```

**Example 2:**

```
Input: s = "*"
Output: 9
Explanation: The encoded message can represent any of the encoded messages "1", "2", "3", "4", "5", "6", "7", "8", or "9".
Each of these can be decoded to the strings "A", "B", "C", "D", "E", "F", "G", "H", and "I" respectively.
Hence, there are a total of 9 ways to decode "*".
```

**Example 3:**

```
Input: s = "1*"
Output: 18
Explanation: The encoded message can represent any of the encoded messages "11", "12", "13", "14", "15", "16", "17", "18", or "19".
Each of these encoded messages have 2 ways to be decoded (e.g. "11" can be decoded to "AA" or "K").
Hence, there are a total of 9 * 2 = 18 ways to decode "1*".
```

**Example 4:**

```
Input: s = "2*"
Output: 15
Explanation: The encoded message can represent any of the encoded messages "21", "22", "23", "24", "25", "26", "27", "28", or "29".
"21", "22", "23", "24", "25", and "26" have 2 ways of being decoded, but "27", "28", and "29" only have 1 way.
Hence, there are a total of (6 * 2) + (3 * 1) = 12 + 3 = 15 ways to decode "2*".
```

**Constraints**

- 1 <= s.length <= 105
- s[i] is a digit or '*'.

---

## 题目（中文翻译）

一个只包含字符 **A‑Z** 的信息可以使用以下映射（mapping）编码为数字：

```
'A' -> "1"
'B' -> "2"
...
'Z' -> "26"
```

要解码一条已编码的信息，需要把所有数字进行分组（grouping），然后使用上述映射的逆过程将每个分组映射回字母（可能有多种分组方式）。例如，字符串 `"11106"` 可以有以下合法的映射方式：

* `"1 1 10 6"` → `"AAJF"`
* `"11 10 6"`   → `"KJF"`

注意分组 `"1 11 06"` 是非法的，因为 `"06"` 不能映射为 `'F'`（只能使用 `"6"` 而不是 `"06"`）。

除了上述映射之外，已编码的信息中还可能出现字符 `'*'`，它可以代表任意数字字符 `'1'` 到 `'9'`（不包括 `'0'`）。例如，已编码信息 `"1*"` 可以表示以下 9 条不同的编码：

```
"11", "12", "13", "14", "15", "16", "17", "18", "19"
```

对 `"1*"` 的解码等价于对它能表示的每一条编码分别进行解码。

给定仅由数字字符和 `'*'` 组成的字符串 `s`，返回对它进行解码的方案数。由于答案可能非常大，请返回 **10⁹ + 7** 取模后的结果。

---

### 示例

#### 示例 1
> 输入：`s = "*"`  
> 输出：`9`  
> 解释：`"*"` 可以表示任意一个 `"1"`~`"9"`，对应的字母分别是 `A`~`I`，因此共有 **9** 种解码方式。

#### 示例 2
> 输入：`s = "1*"`  
> 输出：`18`  
> 解释：`"1*"` 可以表示 `"11"`~`"19"` 共 9 条编码。每条编码都有 2 种解码方式（例如 `"11"` 可以解码为 `"AA"` 或 `"K"`），所以总方案数为 `9 × 2 = 18`。

#### 示例 3
> 输入：`s = "2*"`  
> 输出：`15`  
> 解释：`"2*"` 可以表示 `"21"`~`"29"` 共 9 条编码。`"21"`~`"26"` 每条都有 2 种解码方式，`"27"`、`"28"`、`"29"` 只能解码为单个字母，所以方案数为 `(6 × 2) + (3 × 1) = 12 + 3 = 15`。

---

### 约束

- `1 <= s.length <= 10⁵`
- `s[i]` 为数字字符或 `'*'`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把字符串 `s` 所有可能的 `*` 替换成真实的数字（`1~9`），得到 **所有** 的具体编码，然后对每一种具体编码用普通的「Decode Ways」（只含数字）求解，最后把所有结果加起来。

- **数据结构**：我们把 `*` 当成一个「占位符」，就像在字典里查单词时，`*` 相当于「任意一个字母」的空格。把它展开就是把「占位符」换成真实的「字母」。
- **正确性**：每一种把 `*` 替换成数字的方式都对应着一种合法的原始编码，而每一种原始编码的解码方式已经在「Decode Ways」的算法里被完整枚举，所以把所有替换方式的解码数相加，必然得到所有可能的解码总数。
- **时间/空间复杂度**：  
  - 假设 `k` 为字符串中 `*` 的个数，每个 `*` 有 9 种可能，所有组合数是 `9^k`。  
  - 对每一种组合我们都要跑一次 O(n) 的 DP（n 为字符串长度），所以总时间是 **O(n·9^k)**，这在 `k` 甚至只有 10 时就已经天文数字。  
  - 空间上只需要 O(n) 的 DP 表，额外的组合生成需要 O(k) 的递归栈。  

> **大白话**：  
> O(9^k) 就像是每次掷骰子，骰子有 9 面，掷 k 次所有可能的排列数。掷得越多，可能的排列就会指数级增长，根本算不过来。

#### 代码（Python）

```python
MOD = 10**9 + 7

def decode_ways_bruteforce(s: str) -> int:
    """暴力枚举所有 * 的可能，然后对每个具体数字串做普通 DP"""
    # 1. 把所有 * 的位置收集起来
    star_pos = [i for i, ch in enumerate(s) if ch == '*']
    k = len(star_pos)

    # 2. 递归枚举每个 * 替换成 1~9
    def helper(idx: int, cur: list):
        """把第 idx 个 * 替换完毕后，cur 保存已经确定的字符列表"""
        if idx == k:                     # 所有 * 都已经确定
            num_str = ''.join(cur)
            return decode_ways_numeric(num_str)   # 普通 DP
        total = 0
        for d in '123456789':            # * 只能是 1~9
            cur[star_pos[idx]] = d
            total = (total + helper(idx + 1, cur)) % MOD
        return total

    # 初始时把原字符串拷贝为列表，方便原地修改
    cur = list(s)
    return helper(0, cur)


def decode_ways_numeric(t: str) -> int:
    """只含数字的普通解码 DP（LeetCode 91）"""
    n = len(t)
    dp = [0] * (n + 1)
    dp[0] = 1                       # 空串有 1 种解法
    dp[1] = 0 if t[0] == '0' else 1

    for i in range(2, n + 1):
        # 单独一个字符
        if t[i - 1] != '0':
            dp[i] += dp[i - 1]
        # 两个字符一起看
        two = int(t[i - 2:i])
        if 10 <= two <= 26:
            dp[i] += dp[i - 2]
        dp[i] %= MOD
    return dp[n]
```

> 这段代码能够跑通很小的样例（比如 `s="*"`），但在 `s` 长度 100、`*` 多于 5 时就会超时。

#### 复杂度

- **时间复杂度**：`O(n·9^k)`，`k` 为 `*` 的个数。指数级的 9 的幂让它在实际数据里根本不可行。  
- **空间复杂度**：`O(n + k)`，`n` 用于 DP，`k` 用于递归栈保存星号位置。

---

### 2. 最优解

#### 思路  

从暴力解可以看到两大瓶颈：

1. **枚举所有 `*` 的可能**：这一步把时间从线性直接炸成指数。  
2. **每次都重新跑一次普通 DP**：即使我们把 `*` 展开，也没有利用之前已经算过的子问题。

要把这两步都省掉，需要 **在一次遍历中** 同时考虑单字符和双字符的所有合法组合。  
这正是 **动态规划（Dynamic Programming）** 的精髓：把大问题拆成「前 i-1 位的解法数」和「前 i-2 位的解法数」两块，利用它们快速算出第 i 位的答案。

关键点在于**如何计算每一步的「贡献」**：

- **单字符**：如果 `s[i]` 是数字，则只有当它不是 `'0'` 时才能单独解码；如果是 `'*'`，它可以是 `1~9`，贡献 `9` 种。  
- **双字符**：要看 `s[i-1]` 与 `s[i]` 两个位置组合成的两位数是否落在 `[10,26]`。因为 `*` 可能代表多种数字，这里会出现多种情况，需要逐一统计：

| 前一位 | 当前位 | 合法组合数 |
|--------|--------|-----------|
| `'1'`  | `'*'`  | 9 (`11~19`) |
| `'2'`  | `'*'`  | 6 (`21~26`) |
| `'*'`  | `'0'`  | 2 (`10` 与 `20`) |
| `'*'`  | `'1'~'6'` | 2 (`11~16`、`21~26`) |
| `'*'`  | `'7'~'9'` | 1 (`17~19`) |
| `'1'`  | `'0'~'9'`| 1（只要不是 `'0'`） |
| `'2'`  | `'0'~'6'`| 1（只要 ≤`6`） |
| 其它   | 其它   | 0 |

把这些统计公式写成代码即可。我们只需要两个变量 `dp0`（`dp[i-2]`）和 `dp1`（`dp[i-1]`）滚动更新，空间即可降到 **O(1)**。

#### 代码（Python）

```python
MOD = 10**9 + 7

def num_decodings(s: str) -> int:
    """
    动态规划，一次遍历完成所有可能的计数。
    dp[i] 表示前 i 个字符的解码方法数（i 从 0 开始计数）。
    为了节省空间，只保留 dp[i-2] (prev2) 和 dp[i-1] (prev1)。
    """
    n = len(s)
    # dp[0] = 1：空串只有 1 种解法
    prev2 = 1
    # dp[1] 取决于第一个字符
    first = s[0]
    if first == '*':
        prev1 = 9                      # * 可以是 1~9
    elif first == '0':
        prev1 = 0                      # 0 不能单独解码
    else:
        prev1 = 1                      # 其他数字只能对应一个字母

    for i in range(1, n):
        cur = 0
        cur_ch = s[i]
        prev_ch = s[i - 1]

        # -------- 单字符贡献 ----------
        if cur_ch == '*':
            cur += 9 * prev1               # * 可以是 1~9
        elif cur_ch != '0':
            cur += prev1                   # 非 0 的数字只能对应 1 种

        # -------- 双字符贡献 ----------
        # 情形1：前一位是 '*'
        if prev_ch == '*':
            if cur_ch == '*':
                # ** 可以是 11~19（9 种）或 21~26（6 种） 共 15 种
                cur += 15 * prev2
            elif '0' <= cur_ch <= '6':
                # *0~*6：可以是 10/20、11~16/21~26 => 2 种
                cur += 2 * prev2
            else:  # cur_ch 为 '7'~'9'
                # *7~*9 只能是 17~19 => 1 种
                cur += 1 * prev2
        # 情形2：前一位是确定的数字
        else:
            if prev_ch == '1':
                if cur_ch == '*':
                    cur += 9 * prev2       # 1* => 11~19
                else:
                    cur += prev2           # 10~19 都合法
            elif prev_ch == '2':
                if cur_ch == '*':
                    cur += 6 * prev2       # 2* => 21~26
                elif '0' <= cur_ch <= '6':
                    cur += prev2           # 20~26 合法
                # 27~29 不合法，什么都不加

        # 取模防止溢出
        cur %= MOD
        # 滚动更新 dp 状态
        prev2, prev1 = prev1, cur

    return prev1 % MOD
```

> 关键注释已经用中文写在每一行旁边，帮助初学者一步步跟踪状态变化。

#### 复杂度

- **时间复杂度**：`O(n)`，只遍历一次字符串。  
  - 与暴力解的 `O(n·9^k)` 相比，指数级的 `9^k` 被消掉了，线性时间在 10⁵ 长度下也能轻松跑完。  
- **空间复杂度**：`O(1)`，只用常数个整数保存前两个 DP 状态，不随输入长度增长。

---

## 心得

- **核心技巧**：在出现 `*` 时，用**枚举所有合法组合的计数**代替实际展开；利用**滚动 DP**只保留最近两项，省空间。  
- **适用的题型**：  
  1. 带有通配符的解码/计数类问题（如「Decode Ways I」的进阶版）。  
  2. 类似「不同路径」带障碍物或多种移动方式的动态规划题。  
  3. 任意需要**统计所有合法子串组合数**的字符串 DP（如「正则表达式匹配」的计数版）。  
- **一句话总结**：**把 `*` 的所有可能直接转化为加权系数，在 DP 转移时累加这些系数**，即可一次遍历完成计数。

---

## 反思

- **第一反应**：把 `*` 全部展开成 `1~9`，再套用普通的解码 DP。  
- **最容易踩的坑**：  
  - 忽略 `'0'` 只能和前一位组成 `10` 或 `20`，导致错误计数。  
  - `*` 与数字组合时的边界判断（比如 `2*` 只能取 `21~26`，而 `*7` 只能取 `17`）。  
  - 大数取模时忘记在每一步都 `% MOD`，会导致 Python 整数过大而慢。  
- **下次类似题的第一步**：先**把通配符的取值范围写成表格**，明确每种相邻字符组合对应的合法数量，再在 DP 转移公式里直接使用这些数量。这样既避免遗漏，也能快速写出 O(n) 的解法。