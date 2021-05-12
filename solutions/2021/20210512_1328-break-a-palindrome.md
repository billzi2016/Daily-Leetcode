# #1328. 破坏回文 / Break a Palindrome

> 难度：中等 · 标签：String、Greedy · [LeetCode 链接](https://leetcode.com/problems/break-a-palindrome/)

---

## 题目（英文原版）

**Description**

Given a palindromic string of lowercase English letters palindrome, replace exactly one character with any lowercase English letter so that the resulting string is not a palindrome and that it is the lexicographically smallest one possible.
Return the resulting string. If there is no way to replace a character to make it not a palindrome, return an empty string.
A string a is lexicographically smaller than a string b (of the same length) if in the first position where a and b differ, a has a character strictly smaller than the corresponding character in b. For example, "abcc" is lexicographically smaller than "abcd" because the first position they differ is at the fourth character, and 'c' is smaller than 'd'.

**Examples**

**Example 1:**

```
Input: palindrome = "abccba"
Output: "aaccba"
Explanation: There are many ways to make "abccba" not a palindrome, such as "zbccba", "aaccba", and "abacba".
Of all the ways, "aaccba" is the lexicographically smallest.
```

**Example 2:**

```
Input: palindrome = "a"
Output: ""
Explanation: There is no way to replace a single character to make "a" not a palindrome, so return an empty string.
```

**Constraints**

- 1 <= palindrome.length <= 1000
- palindrome consists of only lowercase English letters.

---

## 题目（中文翻译）

给定一个仅包含小写英文字母（lowercase English letters）的回文字符串（palindrome），请恰好替换其中的一个字符为任意小写英文字母，使得得到的字符串不再是回文且在所有可能的结果中字典序最小（lexicographically smallest）。  
返回得到的字符串。如果不存在通过替换一个字符即可使其不再是回文的情况，返回空字符串。

字符串 a 的字典序小于字符串 b（两者长度相同）当且仅当在 a 与 b 第一次出现不同的字符位置上，a 的字符严格小于 b 的对应字符。例如，"abcc" 的字典序小于 "abcd"，因为它们在第四个字符处不同，'c' 小于 'd'。

**示例 1**

```text
Input: palindrome = "abccba"
Output: "aaccba"
Explanation: 将 "abccba" 变为非回文的方式有很多，例如 "zbccba"、"aaccba"、"abacba"。在所有可能的结果中，"aaccba" 的字典序最小。
```

**示例 2**

```text
Input: palindrome = "a"
Output: ""
Explanation: 无法通过替换单个字符使 "a" 变为非回文，因此返回空字符串。
```

**约束条件**

- 1 ≤ palindrome.length ≤ 1000
- palindrome 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的改动**，然后挑出符合要求且字典序最小的结果。

1. **遍历每一个下标** `i`（从 `0` 到 `len-1`）。  
2. 对于每个下标，尝试把原字符换成 **任意** 小写字母 `c`（`'a'`~`'z'`），但要保证 `c` 与原字符不同，因为题目要求「恰好替换一个字符」。
3. 把改动后的字符串记为 `new_s`，检查它是否仍是回文：  
   - 回文的检测可以把字符串正着读和反着读比较是否相等，类似把一本书正着读和倒着读是否是同一本。  
4. 如果 `new_s` 不是回文，就把它和当前找到的最小答案进行字典序比较，保留更小的那个。  
   - 字典序的比较就像在字典里查词，先比较第一个不同的字符，哪个字母更靠前，哪个字符串就更小。

只要遍历完所有下标和所有可能的字母，就一定能得到**字典序最小的合法改动**（如果有的话）。如果遍历结束仍没有合法字符串，说明根本没有办法改动——这只会在长度为 `1` 的情况出现。

**为什么这个方法一定对？**  
因为我们把「所有可能的」改动都枚举了一遍，必然不会漏掉最佳解。

**时间/空间复杂度**  
- 外层遍历 `n`（字符串长度）个位置。  
- 内层遍历 26 个字母。  
- 每次检查回文需要再遍历一次 `n`。  
- 所以总共是 `O(n * 26 * n) = O(26·n²)`，常数 26 可以忽略，记作 **O(n²)**。  
- 只用了几个临时字符串，额外空间是 **O(n)**（存放新生成的字符串），如果直接在原字符串上改动再恢复，空间可以降到 **O(1)**。

> **大白话**：如果字符串长度是 1000，暴力解大概要做 1000 × 1000 ≈ 100 万次比较，虽然在机器上还能跑完，但不是最优雅的办法。

#### 代码（Python）

```python
def breakPalindrome_bruteforce(palindrome: str) -> str:
    n = len(palindrome)
    # 长度为 1 时根本改不掉，直接返回空串
    if n == 1:
        return ""

    best = None                       # 用来保存当前找到的最小合法字符串
    for i in range(n):                # 枚举要改动的下标
        original = palindrome[i]
        for c in map(chr, range(ord('a'), ord('z') + 1)):  # 枚举所有小写字母
            if c == original:         # 必须真的改动，不能和原字符相同
                continue
            # 生成改动后的新字符串
            new_s = palindrome[:i] + c + palindrome[i + 1:]

            # 检查 new_s 是否是回文（正读和倒读相同）
            if new_s != new_s[::-1]:  # 这里用切片把字符串倒过来
                # 如果是第一次找到合法答案，直接保存
                if best is None or new_s < best:  # 字典序比较
                    best = new_s
    # 如果遍历结束仍没有合法答案，返回空串（实际上只会在 n==1 时出现）
    return best if best is not None else ""
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 两层遍历（位置 × 字母）加上每次回文检测的 `O(n)`。  
  大意是：随着字符串长度增长，运行时间会呈二次方增长。
- **空间复杂度**：`O(n)` —— 需要临时保存生成的新字符串 `new_s`（长度为 `n`）。如果改动后立即比较并恢复，空间可以降到 `O(1)`。

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于我们把所有可能的改动都尝试了一遍，而实际上我们只需要一次**贪心**的决定就能得到答案。

观察题目要求：

1. **必须恰好改动一个字符**，且改动后**不再是回文**。  
2. 我们希望**字典序最小**。字典序越小，意味着在**最左侧**出现的字符越小。

基于这两点，思考如何“尽可能左侧改动且让字符尽可能小”。

- 若字符串左半边（不包括中间字符）出现了一个不是 `'a'` 的字符，**把它改成 `'a'`** 就可以：
  - 改动后左半边的字符更小，整体字典序更小。  
  - 同时，因为我们把左边的字符改成 `'a'`，对应的右边字符保持不变，二者不再相等（原本不是 `'a'`），所以整体不再是回文。  

- 若左半边所有字符都是 `'a'`，说明整个字符串形如 `"aaaa...aa"`（全部都是 `'a'`），这时把左边任何字符改成更小的字母是不可能的（已经是最小的 `'a'`）。唯一的办法是**把最右边的字符改成 `'b'`**：
  - 把最右边的 `'a'` 换成 `'b'`，仍然只改动一个字符，且一定破坏回文（左边仍是 `'a'`，右边变成 `'b'`）。  
  - 改动位置尽可能靠右，是因为我们希望**左侧尽量保持不变**，从而让整体字典序保持最小。

- 唯一不可行的情况是字符串长度为 `1`，因为改动后只能得到单字符，必然仍是回文，返回空串。

**核心算法**：一次线性扫描（`O(n)`），找左半边第一个不是 `'a'` 的位置；若找不到，则把最后一个字符改成 `'b'`。

#### 代码（Python）

```python
def breakPalindrome(palindrome: str) -> str:
    n = len(palindrome)

    # 长度为 1 时无论怎么改都还是回文，返回空串
    if n == 1:
        return ""

    # 将字符串转成列表，方便原地修改（列表修改 O(1)）
    s = list(palindrome)

    # 只需要检查前半段（不包括中间字符），因为回文的对称性
    for i in range(n // 2):
        if s[i] != 'a':                     # 找到第一个不是 'a' 的位置
            s[i] = 'a'                       # 贪心：改成最小的字符 'a'
            return "".join(s)               # 立即返回，已经是字典序最小

    # 如果前半段全是 'a'，说明字符串形如 "aaaa...aa"
    # 把最后一个字符改成 'b'（最小的可以让它变大的字符）
    s[-1] = 'b'
    return "".join(s)
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历了一遍左半边（最多 `n/2` 次），每次操作都是常数时间。  
  与暴力解的 `O(n²)` 相比，时间提升了 **n 倍**，即长度 1000 时只需几千次操作。
- **空间复杂度**：`O(n)` —— 需要把字符串转成列表（长度为 `n`），但不需要额外的 `O(n²)` 辅助空间。若要求原地修改且返回新字符串，可以直接在原字符串上用切片构造，仍是 `O(n)`。

---

## 心得

- **核心技巧**：**贪心 + 对称性**。  
  通过观察“左侧越小越好”和“回文的对称结构”，我们只需要一次线性扫描就能确定唯一最优改动位置。

- **适用的题型**  
  1. 需要在满足某种“对称”或“平衡”约束的情况下，使字符串字典序最小（如 “Make String Palindrome” 的逆向思路）。  
  2. 只允许**恰好一次**改动，且要最小化某种代价（如 “Lexicographically Smallest String After One Swap”）。  
  3. 需要在**局部**（左半边）进行优化，而右半边可以利用对称性推断结果的题目。

- **一句话总结解题钥匙**：  
  **“把左侧第一个非最小字符改成最小字符；若左侧全是最小字符，则把最右侧字符稍微增大一点。”**

---

## 反思

- **第一反应**：看到“回文”和“字典序最小”，自然想到“把左边的字符尽量改成 `a`”。于是立刻想到遍历左半边寻找第一个不是 `a` 的位置。

- **最容易踩的坑**  
  1. **忘记长度为 1 的特殊情况**，会错误地返回 `'b'` 或其他字符。  
  2. **只改动左半边**而不考虑中间字符：当长度为奇数且中间字符不是 `a` 时，改动中间字符仍能破坏回文，但会导致字典序不如左侧改动小。  
  3. **把整个字符串都改成 `a`**（比如全是 `a`）而忘记最后要改成 `b`，导致仍是回文。

- **下次遇到同类题的第一步**：  
  **先判断是否可以在“左侧最早位置”进行最小化改动**，如果左侧已经达到最小值，再考虑“右侧最小的必要改动”。这一步往往可以把问题的搜索空间直接压到 `O(n)`。