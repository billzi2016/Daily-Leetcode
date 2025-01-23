# #3031. 恢复单词至初始状态的最小时间 II / Minimum Time to Revert Word to Initial State II

> 难度：困难 · 标签：String、Rolling Hash、String Matching、Hash Function · [LeetCode 链接](https://leetcode.com/problems/minimum-time-to-revert-word-to-initial-state-ii/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed string word and an integer k.
At every second, you must perform the following operations:
Note that you do not necessarily need to add the same characters that you removed. However, you must perform both operations at every second.
Return the minimum time greater than zero required for word to revert to its initial state.

**Examples**

**Example 1:**

```
Input: word = "abacaba", k = 3
Output: 2
Explanation: At the 1st second, we remove characters "aba" from the prefix of word, and add characters "bac" to the end of word. Thus, word becomes equal to "cababac".
At the 2nd second, we remove characters "cab" from the prefix of word, and add "aba" to the end of word. Thus, word becomes equal to "abacaba" and reverts to its initial state.
It can be shown that 2 seconds is the minimum time greater than zero required for word to revert to its initial state.
```

**Example 2:**

```
Input: word = "abacaba", k = 4
Output: 1
Explanation: At the 1st second, we remove characters "abac" from the prefix of word, and add characters "caba" to the end of word. Thus, word becomes equal to "abacaba" and reverts to its initial state.
It can be shown that 1 second is the minimum time greater than zero required for word to revert to its initial state.
```

**Example 3:**

```
Input: word = "abcbabcd", k = 2
Output: 4
Explanation: At every second, we will remove the first 2 characters of word, and add the same characters to the end of word.
After 4 seconds, word becomes equal to "abcbabcd" and reverts to its initial state.
It can be shown that 4 seconds is the minimum time greater than zero required for word to revert to its initial state.
```

**Constraints**

- 1 <= word.length <= 106
- 1 <= k <= word.length
- word consists only of lowercase English letters.

---

## 题目（中文翻译）

**题目描述**  
给定一个下标从 0 开始的字符串 `word`（string）和一个整数 `k`（int）。  
每过一秒，你必须依次执行以下两项操作：

1. 从 `word` 的前缀（prefix）中移除恰好 `k` 个字符。  
2. 向 `word` 的末尾追加任意 `k` 个字符（这 `k` 个字符不必与被移除的相同，但每秒必须同时进行这两项操作）。

返回使 `word` 恢复到初始状态所需的最小正整数时间（即大于零的最少秒数）。

---

**示例**  

**示例 1**  
```
Input: word = "abacaba", k = 3
Output: 2
```
**解释**：  
第 1 秒，移除前缀中的字符 `"aba"`，在末尾添加字符 `"bac"`，此时 `word` 变为 `"cababac"`。  
第 2 秒，移除前缀中的字符 `"cab"`，在末尾添加字符 `"aba"`，此时 `word` 重新变为 `"abacaba"`，恢复到初始状态。  

**示例 2**  
```
Input: word = "abacaba", k = 4
Output: 1
```
**解释**：  
第 1 秒，移除前缀中的字符 `"abac"`，在末尾添加字符 `"caba"`，`word` 立即变为 `"abacaba"`，恢复到初始状态。可以证明 1 秒是大于零的最小时间。

**示例 3**  
```
Input: word = "abcbabcd", k = 2
Output: 4
```
**解释**：  
每秒都移除前缀的前 2 个字符，并将相同的 2 个字符追加到末尾。  
经过 4 秒后，`word` 再次等于 `"abcbabcd"`，恢复到初始状态。可以证明 4 秒是大于零的最小时间。

---

**约束条件**  

- `1 <= word.length <= 10^6`  
- `1 <= k <= word.length`  
- `word` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

我们把 **每一秒** 的两件事拆开来看：

1. 把字符串最前面的 `k` 个字符删掉（相当于把 `word[0:k]` 丢进垃圾桶）。  
2. 再在字符串的末尾随意加入 **任意** `k` 个字符（可以是任何小写字母，和删掉的字符不一定相同）。

设原字符串长度为 `n`，第 `t` 秒结束后已经删掉了 `t·k` 个字符，剩下的部分是  

```
word[t·k : n]          （如果 t·k > n，则已经没有原来的字符了）
```

要让第 `t` 秒结束时 **恰好** 回到最初的 `word`，只能靠我们在第二步“随意加入的字符”来填补缺失的前缀。  
这就要求：**剩下的那段原字符必须正好等于原字符串的前缀**，否则无论我们往后面加什么，都不可能拼成完整的 `word`。

换句话说，必须找到一个长度 `L`（`L = n - t·k`），满足  

```
word[0 : L] == word[n-L : n]      （前缀 = 后缀）
```

并且 `t·k = n - L` 必须能被 `k` 整除 → `n - L` 必须是 `k` 的整数倍。  

暴力做法就是：

1. 枚举 `t = 1, 2, …`（最多到 `n`，因为删掉 `n` 个字符后已经没有原字符了）。  
2. 计算 `L = n - t·k`，如果 `L < 0` 直接跳过。  
3. 检查 `word[0:L]` 是否等于 `word[n-L:n]`（直接切片比较）。  
4. 第一次满足条件的 `t` 就是答案。

> **生活化类比**：  
> 想象你有一根绳子，上面写着字符。每秒你剪掉左边 `k` 厘米，然后在右边随意粘上一段同样长的绳子（可以写任意字符）。要让绳子最终重新变成原来的模样，必须保证剩下的那段“老绳子”恰好是原绳子的开头，这样你再在后面粘上合适的“新绳子”就能完整复原。

#### 代码（Python）

```python
def minimumTime_bruteforce(word: str, k: int) -> int:
    n = len(word)
    # 最多只需要尝试 n 次，因为超过 n 次就没有原字符可以保留下来了
    for t in range(1, n + 1):
        removed = t * k               # 已经删掉的字符数
        if removed > n:               # 已经删光了，后面的比较没有意义
            break
        L = n - removed               # 剩余的原字符长度
        # 检查前缀和后缀是否相同
        if word[:L] == word[n - L:]:
            return t                  # 第一次满足即为最小时间
    # 如果循环结束仍未返回，说明只能等全部字符被删掉再重新拼
    # 此时 t = ceil(n / k) = (n + k - 1) // k
    return (n + k - 1) // k
```

> **关键行解释**  
> - `removed = t * k`：第 `t` 秒共删除了多少字符。  
> - `L = n - removed`：剩下的原字符长度。  
> - `word[:L] == word[n - L:]`：直接比较前缀与后缀是否相同。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  外层循环最多 `n` 次，内层比较前缀/后缀最坏需要遍历 `O(n)`（切片比较本质上是线性）。  
  用大白话说，就是“每秒都要把整根绳子重新检查一遍”，所以会很慢。

- **空间复杂度**：`O(1)`  
  只用了常数个变量，和输入长度无关。

---

### 2. 最优解

#### 思路  

暴力解慢的根源在于 **每次都要重新比较整个前缀和后缀**。  
我们只需要一次性把所有“前缀 = 后缀”的信息全部算出来，然后再挑选满足 `(n - L) % k == 0` 的最长 `L` 即可。

这正好是 **字符串的“border”**（即前缀同时也是后缀）的典型应用。  
常用的两种线性算法：

1. **KMP 的前缀函数**（`pi`）  
2. **Z‑函数**  

这里选用 **Z‑函数**，因为它直接给出每个位置开始的子串与整体前缀的最长公共前缀长度，非常适合判断 “从某个位置到结尾是否完整匹配前缀”。

**Z‑函数**定义：`Z[i]` 为字符串 `s` 从位置 `i` 开始的子串与 `s` 的前缀的最长公共前缀长度。  
如果 `i + Z[i] == n`，说明从 `i` 开始的子串恰好匹配了长度为 `n-i` 的前缀，也就是说 **`n-i` 是一个 border**。

步骤如下：

1. 计算 `word` 的 Z‑函数，时间 `O(n)`。  
2. 遍历所有 `i`（`1 ≤ i < n`），若 `i + Z[i] == n`，则 `L = n - i` 是一个合法的前缀‑后缀长度。  
3. 在这些 `L` 中挑选 **最大** 的满足 `(n - L) % k == 0`（即 `L` 与 `k` 的关系满足可以整除）。  
   - 记这个最大长度为 `bestL`（如果没有找到，默认 `bestL = 0`）。  
4. 答案即 `t = (n - bestL) // k`（因为每秒删 `k`，总共要删掉 `n - bestL` 个字符）。

> **类比**：  
> 把 `word` 想成一本书的全文。Z‑函数相当于一次性检查“从第几页开始往后读，能和书的开头读到多少相同”。只要找出所有能完整匹配到书末的起始页（即 `i + Z[i] == n`），我们就得到所有可能的“前后相同的段落”。随后挑最长、且长度差能被 `k` 整除的段落，就能算出最少需要多少次“剪掉前 `k` 页、再补上任意页”才能把书恢复原样。

#### 代码（Python）

```python
def minimumTime(word: str, k: int) -> int:
    """
    O(n) 解法：利用 Z 函数找最长满足条件的前后缀长度 L
    最终答案 = (n - L) // k
    """
    n = len(word)

    # ---------- 计算 Z 函数 ----------
    Z = [0] * n
    l, r = 0, 0               # 当前维护的 [l, r) 区间，使得区间内与前缀完全匹配
    for i in range(1, n):
        if i < r:
            Z[i] = min(r - i, Z[i - l])   # 复用已有信息
        # 暴力向右扩展
        while i + Z[i] < n and word[Z[i]] == word[i + Z[i]]:
            Z[i] += 1
        # 若扩展后超过当前区间，更新 l、r
        if i + Z[i] > r:
            l, r = i, i + Z[i]

    # ---------- 寻找满足条件的最长 border ----------
    bestL = 0                                   # 默认长度 0（总能满足）
    for i in range(1, n):
        if i + Z[i] == n:                       # 从 i 开始的子串恰好匹配到结尾
            L = n - i                           # 前缀/后缀长度
            if (n - L) % k == 0:                # 删除的字符数能被 k 整除
                if L > bestL:
                    bestL = L

    # ---------- 计算答案 ----------
    return (n - bestL) // k
```

> **关键行解释**  
> - `while i + Z[i] < n and word[Z[i]] == word[i + Z[i]]:`：在当前位置尽可能向右扩展匹配长度。  
> - `if i + Z[i] == n:`：说明从 `i` 开始的子串正好覆盖到字符串结尾，长度 `n-i` 是一个完整的 border。  
> - `(n - L) % k == 0`：确保要删掉的字符数（`n-L`）可以用整数秒的 `k` 来完成。  
> - `return (n - bestL) // k`：总共需要删掉 `n - bestL` 个字符，每秒删 `k`，自然得到最少秒数。

#### 复杂度

- **时间复杂度**：`O(n)`  
  只遍历一次字符串计算 Z‑函数，随后再一次线性遍历找 border。  
  与 `n` 成正比，哪怕 `n` 达到 `10⁶` 也能毫秒级完成。

- **空间复杂度**：`O(n)`  
  需要额外的数组 `Z` 长度为 `n`，其余只用常数空间。  
  相比暴力的 `O(1)`，这里多用了线性空间，但换来了线性时间，是值得的权衡。

---

## 心得

- **核心技巧**：利用 **前后缀相同（border）** 的性质，把“每秒删除 `k`、随意添加 `k`”的问题转化为“找最长满足 `(n - L) % k == 0` 的 border”。  
- **适用场景**：  
  1. **字符串循环复位** 类题（例如 “最小循环移位次数”）。  
  2. **需要找所有前后缀相同的长度**（如 “最短回文前缀”）。  
  3. **利用 Z‑函数或前缀函数做线性匹配**（如 “字符串分割是否可由相同子串组成”）。
- **一句话总结**：  
  “把‘每秒删 `k`’看成一次左移 `k`，只要找出能左移若干次后仍和原串前缀对齐的最长段落，答案就是删掉其余字符需要的秒数。”

---

## 反思

- **拿到题目第一反应**：先想“每秒把前 `k` 丢掉再补上”，于是想到 **模拟** 或 **暴力枚举**，检查每一步是否能复原。  
- **最容易踩的坑**  
  1. **忘记考虑 `L = 0`**：即全部字符都被删掉的极端情况，答案仍然是 `ceil(n/k)`。  
  2. **边界条件**：`n - L` 必须是 `k` 的整数倍，直接比较 `L` 而忽视这一点会得到错误答案。  
  3. **字符串长度非常大**（`10⁶`），若仍使用 `O(n²)` 的比较会超时。  
- **下次遇到同类题**：第一步先 **抽象成“左移+前后缀匹配”**，立刻想到使用 **Z‑函数 / 前缀函数** 把所有可能的匹配一次性算出来，再在这些候选中挑最优。这样可以避免毫无目标的暴力枚举，直接走向线性解法。