# #2575. 找出字符串的可整除数组 / Find the Divisibility Array of a String

> 难度：中等 · 标签：Array、Math、String · [LeetCode 链接](https://leetcode.com/problems/find-the-divisibility-array-of-a-string/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed string word of length n consisting of digits, and a positive integer m.
The divisibility array div of word is an integer array of length n such that:
Return the divisibility array of word.

**Examples**

**Example 1:**

```
Input: word = "998244353", m = 3
Output: [1,1,0,0,0,1,1,0,0]
Explanation: There are only 4 prefixes that are divisible by 3: "9", "99", "998244", and "9982443".
```

**Example 2:**

```
Input: word = "1010", m = 10
Output: [0,1,0,1]
Explanation: There are only 2 prefixes that are divisible by 10: "10", and "1010".
```

**Constraints**

- 1 <= n <= 105
- word.length == n
- word consists of digits from 0 to 9
- 1 <= m <= 109

---

## 题目（中文翻译）

你得到一个下标从 **0** 开始的字符串 `word`（长度为 `n`），仅由数字字符组成，和一个正整数 `m`。  
**可整除数组**（divisibility array）`div` 是一个长度为 `n` 的整数数组，其中  

```
div[i] = 1   如果   word[0..i]（即前缀）对应的整数能够被 m 整除
div[i] = 0   否则
```

请返回字符串 `word` 的可整除数组 `div`。

---

### 示例

**示例 1**  

```
Input: word = "998244353", m = 3
Output: [1,1,0,0,0,1,1,0,0]
Explanation: 只有 4 个前缀能够被 3 整除，分别是 "9", "99", "998244" 和 "9982443"。
```

**示例 2**  

```
Input: word = "1010", m = 10
Output: [0,1,0,1]
Explanation: 只有 2 个前缀能够被 10 整除，分别是 "10" 和 "1010"。
```

---

### 约束条件

- `1 <= n <= 10^5`
- `word.length == n`
- `word` 仅由字符 `'0'` 到 `'9'` 组成
- `1 <= m <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每一个前缀都“读出来”变成整数，然后判断它能不能被 `m` 整除。  
可以把字符串想象成一本 **数字词典**，我们把从第 0 位到第 `i` 位的字符拼成一个“单词”，再把这个单词交给 **计算器**（`int()`）得到它对应的数值，最后用除法看余数是否为 0。

- **数据结构**：只需要普通的 Python 列表来存放答案，另外用 `int()` 把子串转成整数。  
- **正确性**：如果一个数能够被 `m` 整除，那么 `num % m == 0` 必然成立；我们对每一个前缀都这么检查，自然能得到全部符合要求的下标。  

**为什么会慢**：`int(word[:i+1])` 每次都要把前 `i+1` 个字符重新转成整数，转化过程本质上是把每一位都乘以相应的十的幂再相加，时间随前缀长度线性增长。对所有 `n` 个前缀累计起来就是 `1 + 2 + … + n = n·(n+1)/2`，即 **O(n²)**。

#### 代码（Python）

```python
def divisibilityArray_bruteforce(word: str, m: int) -> list[int]:
    n = len(word)
    ans = [0] * n                     # 用来存放答案的数组
    for i in range(n):
        # 把前 i+1 位字符拼成整数（相当于把字典里查到对应的“页码”）
        prefix_num = int(word[:i + 1])
        # 判断是否能被 m 整除，能则记 1，不能记 0
        ans[i] = 1 if prefix_num % m == 0 else 0
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 大白话：如果 `n` 是 10 000，算法大约要做 50 000 000 次“加减乘除”，会明显卡顿。  
- **空间复杂度**：`O(1)`（不计答案数组本身）  
  - 只用了几个临时变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于每次都重新把前缀转成完整的整数。其实我们不需要每次都重新计算整个数，只要保留上一次前缀的 **余数**（`mod`），就能利用十进制的进位规则快速得到新前缀的余数：

```
前缀 i-1 的数值 = X
前缀 i   的数值 = X * 10 + digit_i
```

对模 `m` 来说，有以下等式：

```
 (X * 10 + digit_i) % m
 = ( (X % m) * 10 + digit_i ) % m
```

这意味着只要知道 `X % m`（即上一次的余数），就能在 **O(1)** 时间内算出新的余数。于是我们只需要一次遍历，依次更新余数并判断是否为 0。

- **核心算法**：**前缀余数滚动**（也叫“前缀模”），它是一种 **动态规划** 思想的最简形式——当前状态只依赖于前一个状态。  
- **类比**：想象你在排队买票，每个人的票价都是 10 元，加上本人的票价（0‑9），而你只关心“排到这里总共付了多少元”除以 `m` 的余数。只要记住前面的人付了多少余数，你就能立刻算出自己付完后的余数，而不必重新数所有人的票价。

#### 代码（Python）

```python
def divisibilityArray(word: str, m: int) -> list[int]:
    """
    返回 word 的可除数组。时间 O(n)，空间 O(1)（不计输出）。
    """
    n = len(word)
    ans = [0] * n          # 结果数组
    cur_mod = 0            # 当前前缀的余数，初始为 0

    for i, ch in enumerate(word):
        digit = ord(ch) - ord('0')   # 把字符转成对应的整数 0~9
        # 根据 (prev_mod * 10 + digit) % m 更新余数
        cur_mod = (cur_mod * 10 + digit) % m
        # 余数为 0 表示前缀可被 m 整除
        ans[i] = 1 if cur_mod == 0 else 0

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 大白话：只需要一次遍历，每个字符做一次乘法、一次加法、一次取模，线性增长，`n` 再大也能在毫秒级完成。  
- **空间复杂度**：`O(1)`（不计输出）  
  - 只用了 `cur_mod`、`digit` 这几个常数级变量，和 `n` 没有关系。

---

## 心得

- **核心技巧**：利用前缀余数的递推公式，避免重复构造大整数。  
- **适用场景**：  
  1. “前缀可被 K 整除” 类题（如 LeetCode 1016 *子字符串计数*，只要把 `K` 换成 9）。  
  2. “求子数组/子串的模值” 这类需要快速判断可整除性的题目（如 “连续子数组的和能否被 K 整除”）。  
- **一句话总结**：**“只记余数，滚动更新”** 是解这类“前缀可除”问题的钥匙。

---

## 反思

- **第一反应**：直接把每个前缀转成整数再 `% m` 检查，觉得最直观。  
- **最容易踩的坑**：  
  - **大数溢出**：在某些语言里直接转成整数会超出 64 位范围；即使 Python 的大整数不溢，但时间会爆炸。  
  - **字符转整数**：忘记把字符 `'0'`~`'9'` 转成数字，导致字符串拼接错误。  
  - **取模顺序**：如果先把 `cur_mod * 10` 乘完再 `% m`，在语言整数上限低的情况下可能出现临时溢出。  
- **下次思路**：看到“前缀”“可整除”关键词时，第一步就想到 **“用滚动余数”**，从而把暴力的 O(n²) 降到 O(n)。