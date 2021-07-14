# #1397. 找出所有好字符串 / Find All Good Strings

> 难度：困难 · 标签：String、Dynamic Programming、String Matching · [LeetCode 链接](https://leetcode.com/problems/find-all-good-strings/)

---

## 题目（英文原版）

**Description**

Given the strings s1 and s2 of size n and the string evil, return the number of good strings.
A good string has size n, it is alphabetically greater than or equal to s1, it is alphabetically smaller than or equal to s2, and it does not contain the string evil as a substring. Since the answer can be a huge number, return this modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: n = 2, s1 = "aa", s2 = "da", evil = "b"
Output: 51 
Explanation: There are 25 good strings starting with 'a': "aa","ac","ad",...,"az". Then there are 25 good strings starting with 'c': "ca","cc","cd",...,"cz" and finally there is one good string starting with 'd': "da".
```

**Example 2:**

```
Input: n = 8, s1 = "leetcode", s2 = "leetgoes", evil = "leet"
Output: 0 
Explanation: All strings greater than or equal to s1 and smaller than or equal to s2 start with the prefix "leet", therefore, there is not any good string.
```

**Example 3:**

```
Input: n = 2, s1 = "gx", s2 = "gz", evil = "x"
Output: 2
```

**Constraints**

- s1.length == n
- s2.length == n
- s1 <= s2
- 1 <= n <= 500
- 1 <= evil.length <= 50
- All strings consist of lowercase English letters.

---

## 题目（中文翻译）

给定长度为 `n` 的字符串 `s1` 和 `s2`，以及字符串 `evil`，返回 **好字符串**（good string）的数量。  
好字符串满足以下条件：

- 长度为 `n`；
- 在字典序上 **大于等于** `s1`；
- 在字典序上 **小于等于** `s2`；
- **不包含** `evil` 作为子串（substring）。

由于答案可能非常大，返回答案对 `10^9 + 7` 取模后的结果。

## 示例

### 示例 1
**输入**  
`n = 2, s1 = "aa", s2 = "da", evil = "b"`

**输出**  
`51`

**解释**  
以 `'a'` 开头的好字符串有 25 个：`"aa","ac","ad",...,"az"`。  
以 `'c'` 开头的好字符串也有 25 个：`"ca","cc","cd",...,"cz"`。  
最后仅有一个以 `'d'` 开头的好字符串：`"da"`。  
总计 `25 + 25 + 1 = 51`。

### 示例 2
**输入**  
`n = 8, s1 = "leetcode", s2 = "leetgoes", evil = "leet"`

**输出**  
`0`

**解释**  
所有满足 `s1 ≤ string ≤ s2` 的字符串都以前缀 `"leet"` 开头，而 `evil = "leet"` 正好是这个前缀，因此不存在好字符串。

### 示例 3
**输入**  
`n = 2, s1 = "gx", s2 = "gz", evil = "x"`

**输出**  
`2`

## 约束条件

- `s1.length == n`
- `s2.length == n`
- `s1 ≤ s2`
- `1 ≤ n ≤ 500`
- `1 ≤ evil.length ≤ 50`
- 所有字符串仅由小写英文字母组成

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有长度为 `n` 的小写字母串**，检查每一个串是否满足三个条件：

1. `s1 ≤ cur ≤ s2`（字典序在区间内）  
2. `cur` **不包含** 子串 `evil`  

这相当于把所有可能的字符串当成一本“字典”，然后一页页翻过去，挑出符合要求的页。  
- 用到的数据结构只有 **字符串** 本身和 **循环**（for 循环），不需要任何高级结构。  
- 判断字典序可以直接用 Python 的字符串比较（`<=`、`>=`），因为 Python 已经把字典序实现好了。  
- 判断是否包含 `evil` 用 `evil in cur`，相当于在一本书里找某个词。

**为什么正确**  
只要把**所有**可能的字符串都检查一遍，符合条件的自然就全部被统计了。

**时间/空间复杂度**  
- 字母表有 26 个字符，长度为 `n`，所以总共有 `26ⁿ` 种可能的字符串。  
- 对每一种我们都要做一次字典序比较（`O(n)`）和一次子串查找（最坏 `O(n·|evil|)`），但这里先把复杂度写成 **指数级**：  

```
时间复杂度 = O(26ⁿ)          # 规模随 n 指数增长，n=10 时已经 1.4e14，根本不可跑
空间复杂度 = O(n)           # 只需要存放当前枚举的字符串
```

大白话解释：`O(26ⁿ)` 就像把所有可能的密码都穷举出来尝试一次，随着密码长度每增加一位，尝试的次数就会 **翻 26 倍**，很快就会炸掉电脑。

#### 代码（Python）

```python
import itertools

MOD = 10**9 + 7

def count_good_bruteforce(n: int, s1: str, s2: str, evil: str) -> int:
    cnt = 0
    # itertools.product 会产生所有长度为 n 的字母组合，像是把 26 张卡片排成 n 行
    for chars in itertools.product('abcdefghijklmnopqrstuvwxyz', repeat=n):
        cur = ''.join(chars)                 # 把卡片拼成一个字符串
        # 先检查字典序是否在区间内
        if s1 <= cur <= s2:
            # 再检查是否出现了 evil
            if evil not in cur:
                cnt += 1
    return cnt % MOD
```

> 这段代码只能在 `n ≤ 4` 左右的小样例里跑通，真正的测评数据会导致超时。

#### 复杂度

- **时间复杂度**：`O(26ⁿ)` —— 随着 `n` 增大，枚举的次数呈指数增长，几乎不可能在 1 秒内完成。
- **空间复杂度**：`O(n)` —— 只保存当前枚举的字符串 `cur`，长度为 `n`。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **枚举所有 26ⁿ 种可能**。我们必须**不枚举**，而是**动态规划**（DP）直接算出符合条件的数量。

从暴力解出发，我们发现每一步只关心以下信息：

| 信息 | 含义 | 类比 |
|------|------|------|
| 已经决定了前 `pos` 位字符 | 当前构造到了第几位 | 像在拼单词，已经写好了前 `pos` 个字母 |
| 前缀是否仍然等于 `s1` | 如果一直等于 `s1`，第 `pos` 位的取值只能在 `s1[pos]` 与 `'z'` 之间 | 像是走在两条边界线上，左边界是 `s1`，右边界是 `s2` |
| 前缀是否仍然等于 `s2` | 同理，决定了右侧的上界 | |
| 已经匹配了 `evil` 的最长后缀长度 `k` | 当前字符串的后缀和 `evil` 的前缀最长匹配长度（类似 KMP 中的 `next`） | 把 `evil` 当成一本“禁忌词典”，我们要随时知道已经匹配了多少字，以防完整匹配出现 |

于是我们设计四维 DP：

```
dp[pos][k][tightLow][tightHigh] = 以当前已经构造好的前缀满足
    - 已经匹配的 evil 后缀长度为 k
    - 若 tightLow 为 1，则前缀仍等于 s1 的前 pos 位，否则已经大于 s1
    - 若 tightHigh 为 1，则前缀仍等于 s2 的前 pos 位，否则已经小于 s2
的合法字符串数量
```

**关键点 1：边界约束（tightLow / tightHigh）**  
- 当 `tightLow = 1` 时，第 `pos` 位的字符 `c` 必须 `c >= s1[pos]`，否则会小于下界。  
- 当 `tightHigh = 1` 时，`c <= s2[pos]`。  
- 选完 `c` 后，新的 `tightLow` 为 `tightLow and (c == s1[pos])`（仍然贴在下界上），同理更新 `tightHigh`。

**关键点 2：避免出现 `evil`**  
我们需要在每次添加新字符时，快速得到新的匹配长度 `k'`（即 `evil` 的最长前缀匹配当前后缀）。这正是 **KMP（Knuth–Morris–Pratt）** 的作用：  
- 先对 `evil` 计算 **失配表（failure function）** `fail[i]`，表示当已经匹配到 `evil[:i]`，再遇到不匹配字符时应该回退到哪儿。  
- 在 DP 转移时，用 `while k > 0 and evil[k] != c: k = fail[k-1]`，再检查 `evil[k] == c`，得到 `k' = k + 1`（如果匹配成功），否则 `k' = 0`。  
- 若 `k' == len(evil)`，说明刚刚把完整的 `evil` 放进来了，这条路径必须 **舍弃**（不计入答案）。

**关键点 3：记忆化递归**  
`n ≤ 500`，`|evil| ≤ 50`，状态总数为 `n * |evil| * 2 * 2 ≤ 500 * 50 * 4 = 100,000`，非常适合 **记忆化搜索**（自顶向下）或 **循环 DP**（自底向上）。这里使用递归 + `lru_cache`，代码更直观。

**整体思路**  
1. 预处理 `evil` 的 KMP 失配表 `fail`。  
2. 定义递归函数 `dfs(pos, k, low, high)`，返回从 `pos` 开始到结尾的合法字符串数。  
3. 在函数内部遍历当前位可以取的字符范围（受 `low`、`high` 限制），更新 `k'`、`low'`、`high'`，并把结果累加。  
4. 递归终止条件：`pos == n` 时说明已经构造完全部字符，只要没有触发 `evil`（即 `k < m`），计 1。  
5. 最终答案即 `dfs(0, 0, True, True) % MOD`。

#### 代码（Python）

```python
from functools import lru_cache

MOD = 10**9 + 7

def countGoodStrings(n: int, s1: str, s2: str, evil: str) -> int:
    m = len(evil)

    # ---------- 1. KMP 失配表 ----------
    # fail[i] = 当已经匹配了 evil[:i+1]，下一个字符不匹配时应回到的最长前缀长度
    fail = [0] * m
    for i in range(1, m):
        j = fail[i - 1]
        while j > 0 and evil[i] != evil[j]:
            j = fail[j - 1]
        if evil[i] == evil[j]:
            j += 1
        fail[i] = j

    # ---------- 2. 记忆化递归 ----------
    @lru_cache(None)
    def dfs(pos: int, k: int, low: bool, high: bool) -> int:
        """
        pos : 当前正在决定第 pos 位（0-index）
        k   : 当前已经匹配的 evil 前缀长度（相当于 KMP 中的状态）
        low : 已经严格大于 s1 前缀？如果 low=False，说明前缀仍等于 s1
        high: 已经严格小于 s2 前缀？如果 high=False，说明前缀仍等于 s2
        """
        if k == m:               # 已经完整匹配了 evil，非法路径
            return 0
        if pos == n:             # 已经构造完全部字符，合法
            return 1

        # 根据 low/high 决定本位字符的取值区间
        lo = s1[pos] if not low else 'a'
        hi = s2[pos] if not high else 'z'

        total = 0
        for ch in map(chr, range(ord(lo), ord(hi) + 1)):
            # ---- 更新 KMP 状态 k -> nk ----
            nk = k
            while nk > 0 and evil[nk] != ch:
                nk = fail[nk - 1]
            if evil[nk] == ch:
                nk += 1
            # 如果匹配到了完整的 evil，直接跳过这条分支
            if nk == m:
                continue

            # ---- 更新边界 tight 状态 ----
            nlow  = low or (ch > s1[pos])   # 只要已经大于下界，就保持 True
            nhigh = high or (ch < s2[pos])  # 只要已经小于上界，就保持 True

            total += dfs(pos + 1, nk, nlow, nhigh)
            if total >= MOD:  # 防止中间结果溢出
                total -= MOD

        return total % MOD

    return dfs(0, 0, False, False)
```

> **代码解读**  
> - `fail` 的构造相当于先把 `evil` 这本禁忌词典做“快速跳转表”。  
> - `dfs` 的四个参数完整描述了“当前站在第几位、已经匹配了多少禁忌、是否还贴在两条边界上”。  
> - `lo`、`hi` 把合法字符区间缩小到必须的范围，避免无效的遍历。  
> - 每一步的 `while` 循环是 KMP 的核心，用来在不匹配时回退到上一个可能的前缀。  

#### 复杂度

- **时间复杂度**：`O(n * m * 26)`  
  - 状态数 `n * m * 2 * 2`（约 `n·m`），每个状态遍历至多 26 个字符。  
  - 实际上因为 `low/high` 会限制取值范围，平均遍历的字符数更少。  
  - 大白话：把所有可能的“位置 × 已匹配长度”组合算一遍，每次最多尝试 26 种字母，整体是 **线性**（相对于 `n·m`）的。

- **空间复杂度**：`O(n * m * 2 * 2)` 用于缓存递归结果，大约 `100k` 条记录，约几百 KB。递归栈深度为 `n ≤ 500`，属于可接受范围。

---

## 心得

- **核心技巧**：**带边界的字符 DP + KMP 自动机**。  
  这套组合能够在“要在两个字典序边界之间生成字符串”且“要避免出现特定子串”时，快速统计合法个数。

- **适用的题型**  
  1. **字典序区间 + 禁忌子串**（本题）  
  2. **在给定范围内计数不包含某模式的数**（如“在 `[L,R]` 区间内计数不含 `13` 的整数”）  
  3. **带上/下界的字符串 DP**（如“在 `s1` 与 `s2` 之间，且不出现 `sub` 的回文数”）

- **一句话总结解题钥匙**：  
  “把 `evil` 看成 KMP 自动机，把上下界看成两把锁，用四维 DP 同时控制位置、匹配状态和两把锁的开闭”。  

---

## 反思

- **第一反应**：看到“区间 `[s1, s2]` + 不出现 `evil`”，立刻想到 **枚举 + 判断**，但很快意识到 `n` 可达 500，枚举根本不可行。  
- **最容易踩的坑**  
  1. **KMP 状态转移写错**：忘记在 `while` 循环后再检查 `evil[nk] == ch`，导致匹配长度错误。  
  2. **边界 tight 的更新**：`low` 与 `high` 必须分别在 “已经大于下界 / 已经小于上界” 时设为 `True`，否则会把合法的字符排除。  
  3. **模数运算**：递归返回值需要及时 `% MOD`，否则中间累加可能溢出 Python 的整数（虽然 Python 大整数不溢，但会拖慢速度）。  
- **下次遇到同类题的第一步**：  
  “先把禁忌子串做成 KMP 自动机，再写出 DP 状态：位置、匹配长度、是否仍贴在下界、是否仍贴在上界”。这样思路就已经完整，后面只要把转移写对即可。