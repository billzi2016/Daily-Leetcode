# #3365. 重排 K 段子串以形成目标字符串 / Rearrange K Substrings to Form Target String

> 难度：中等 · 标签：Hash Table、String、Sorting · [LeetCode 链接](https://leetcode.com/problems/rearrange-k-substrings-to-form-target-string/)

---

## 题目（英文原版）

**Description**

You are given two strings s and t, both of which are anagrams of each other, and an integer k.
Your task is to determine whether it is possible to split the string s into k equal-sized substrings, rearrange the substrings, and concatenate them in any order to create a new string that matches the given string t.
Return true if this is possible, otherwise, return false.
An anagram is a word or phrase formed by rearranging the letters of a different word or phrase, using all the original letters exactly once.
A substring is a contiguous non-empty sequence of characters within a string.

**Examples**

**Example 1:**

```
Input: s = "abcd", t = "cdab", k = 2
Output: true
Explanation:
```

**Example 2:**

```
Input: s = "aabbcc", t = "bbaacc", k = 3
Output: true
Explanation:
```

**Example 3:**

```
Input: s = "aabbcc", t = "bbaacc", k = 2
Output: false
Explanation:
```

**Constraints**

- 1 <= s.length == t.length <= 2 * 105
- 1 <= k <= s.length
- s.length is divisible by k.
- s and t consist only of lowercase English letters.
- The input is generated such that s and t are anagrams of each other.

---

## 题目（中文翻译）

给定两个字符串 `s` 和 `t`，它们互为字谜（anagram），以及一个整数 `k`。  
你的任务是判断是否可以将字符串 `s` 分割成 `k` 个等长的子串（substring），对这些子串进行任意顺序的重新排列，然后拼接得到的字符串恰好等于给定的字符串 `t`。  
如果可以实现，返回 `true`；否则返回 `false`。

**字谜（anagram）** 是指通过重新排列另一个单词或短语的字母而形成的单词或短语，且必须恰好使用所有原始字母一次。  
**子串（substring）** 是指字符串中连续的、非空的字符序列。

## 示例

### 示例 1
**输入:** `s = "abcd", t = "cdab", k = 2`  
**输出:** `true`  
**解释:**  
将 `s` 分成 `["ab", "cd"]`，重新排列为 `["cd", "ab"]`，拼接后得到 `t`。

### 示例 2
**输入:** `s = "aabbcc", t = "bbaacc", k = 3`  
**输出:** `true`  
**解释:**  
将 `s` 分成 `["aa", "bb", "cc"]`，重新排列为 `["bb", "aa", "cc"]`，拼接后得到 `t`。

### 示例 3
**输入:** `s = "aabbcc", t = "bbaacc", k = 2`  
**输出:** `false`  
**解释:**  
`k = 2` 时，必须将 `s` 分成长度为 `3` 的子串，例如 `["aab", "bcc"]`，无论如何重新排列都无法得到 `t`。

## 约束条件
- `1 <= s.length == t.length <= 2 * 10^5`
- `1 <= k <= s.length`
- `s.length` 能被 `k` 整除
- `s` 和 `t` 仅由小写英文字母组成
- 输入保证 `s` 与 `t` 是字谜（anagrams）关系

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：

1. 把 `s` 按照 `k` 等分切成 `k` 个子串，每个子串的长度为 `len(s) / k`（记作 `L`）。  
2. 产生 **所有** 可能的子串排列（即 `k!` 种），把每种排列拼接起来得到一个新字符串。  
3. 检查有没有一种排列恰好等于目标字符串 `t`，如果有就返回 `True`，否则返回 `False`。

> **类比**：把 `s` 看成一排装有 `k` 本书的书架，每本书的内容就是一个子串。暴力解相当于把书架上的书全部搬出来，尝试 **所有** 可能的摆放顺序（`k!` 种），看看能不能拼出 `t`。

**为什么正确**：  
只要我们遍历了所有子串的排列，就一定会碰到能够拼出 `t` 的那一种（如果存在的话），因此答案一定是正确的。

**时间/空间复杂度**：

- **时间**：需要遍历 `k!` 种排列，每种排列拼接 `k` 个长度为 `L` 的子串，时间大约是 `O(k! * n)`（`n = len(s)`）。  
  - `k!` 代表“阶乘”，即 `1·2·3·…·k`，当 `k` 稍大时（比如 10）就已经是天文数字，几乎不可能在实际运行时完成。  
- **空间**：需要保存 `k` 个子串以及递归/迭代产生排列时的临时状态，空间大约是 `O(k·L) = O(n)`。

显然，这种暴力方法在 `k` 较大时会超时，根本不可用。

#### 代码（Python）

```python
import itertools

def can_make_by_bruteforce(s: str, t: str, k: int) -> bool:
    n = len(s)
    L = n // k                     # 每个子串的长度
    # 1. 把 s 切成 k 段
    parts = [s[i*L:(i+1)*L] for i in range(k)]

    # 2. 枚举所有排列（k! 种），检查是否能得到 t
    for perm in itertools.permutations(parts):
        candidate = ''.join(perm)  # 把排列好的子串拼接成新字符串
        if candidate == t:
            return True
    return False
```

> **注意**：上述代码只能在 `k` 很小（如 `k ≤ 6`）的测试里跑通，用来说明“最直观、最笨”的思路，实际提交会因超时而失效。

#### 复杂度

- **时间复杂度**：`O(k! * n)` —— 阶乘增长极快，几乎不可能在 `k` 超过 10 时完成。
- **空间复杂度**：`O(n)` —— 用来保存原始的 `k` 个子串以及临时的排列。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正的难点**在于枚举所有排列。其实我们并不需要真的把所有排列列出来，只要比较两边的**子串多重集合**（multiset）是否相同即可。

- 把 `s` 按照等长切成 `k` 段，记为 `S = {s1, s2, …, sk}`（这里的集合是“带计数”的，两个相同子串会出现两次）。
- 同理，把 `t` 也切成 `k` 段，记为 `T = {t1, t2, …, tk}`。
- 只要 `S` 与 `T` 中每个子串出现的次数完全相同，就一定可以把 `S` 按某种顺序排列得到 `t`，因为我们可以把每个 `ti` 对应到 `S` 中同样的子串。

> **类比**：把 `s` 的 `k` 本书每本的内容写在一张卡片上，形成一副卡牌。`t` 的卡牌也是如此。只要两副卡牌的每张卡出现次数相同（即卡牌的多重集合相等），我们就可以把 `s` 那副卡牌洗牌成 `t` 那副卡牌。**不需要真的去洗**，只要数数看是否相同就行。

实现细节：

1. 计算每段子串的长度 `L = n / k`。  
2. 用哈希表（Python 的 `dict`）记录 `s` 的每段子串出现次数。  
   - 哈希表类似**查字典**：键是子串本身，值是出现的次数。  
3. 再遍历 `t` 的每段子串，在哈希表中把对应计数减一。  
   - 如果出现一个在 `s` 中不存在的子串（计数为 `0`），立刻返回 `False`。  
4. 最后检查哈希表中所有计数是否全部归零，若是则返回 `True`。

整个过程只需要一次线性扫描，时间 `O(n)`，空间 `O(k)`（最多保存 `k` 条不同子串的计数）。

#### 代码（Python）

```python
def can_make_by_hash(s: str, t: str, k: int) -> bool:
    """
    使用哈希表统计子串出现次数，判断两边的多重集合是否相同。
    """
    n = len(s)
    L = n // k                     # 每个子串的长度

    # 1. 统计 s 中每个子串的出现次数
    counter = {}
    for i in range(k):
        sub = s[i*L:(i+1)*L]       # 取第 i 段子串
        counter[sub] = counter.get(sub, 0) + 1   # 哈希表计数，类似查字典

    # 2. 遍历 t 的子串，逐一在哈希表中扣除计数
    for i in range(k):
        sub = t[i*L:(i+1)*L]
        if sub not in counter:    # t 中出现了 s 没有的子串
            return False
        counter[sub] -= 1
        if counter[sub] == 0:     # 计数降到 0 可以删除，节约空间（可选）
            del counter[sub]

    # 3. 若所有计数都已被消除，则两边多重集合相同
    return not counter            # 空字典 → True, 否则 False
```

> **关键行解释**  
> - `sub = s[i*L:(i+1)*L]`：利用切片一次取出第 `i` 段子串，时间复杂度是 **O(L)**，但整体只遍历一次字符串。  
> - `counter.get(sub, 0) + 1`：在字典里查找 `sub` 的当前计数，如果不存在返回 `0`（相当于查字典时没有找到对应的页码，就返回默认值）。  
> - `if sub not in counter`：相当于在字典里找不到这个词条，说明 `t` 包含了 `s` 没有的子串，直接返回 `False`。  

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历了两遍字符串（各 `k` 段），每次切片和哈希表操作都是常数时间。  
  - 与暴力解的 `O(k!·n)` 相比，线性时间几乎可以在任意输入规模下秒杀通过。  
- **空间复杂度**：`O(k)` —— 哈希表最多保存 `k` 条不同的子串及其计数（最坏情况每段子串都不相同），远小于 `n`。

---

## 心得

- **核心技巧**：把“能否重新排列子串”转化为**子串多重集合相等**的判定。  
- **适用的题型**  
  1. 把字符串切成若干块后，判断两串块集合是否相同（如本题）。  
  2. 判断两数组是否可以通过重新排列块得到（例如把数组分块后比较块的出现次数）。  
  3. 需要判断子序列或子串的“出现次数”是否匹配的场景（如“按字符块重排”类题）。  
- **一句话总结**：**只要把每块当成一个“字典的键”，统计出现次数，比较两侧计数是否完全相同，即可快速判断是否可通过块重排得到目标。**

---

## 反思

- **第一反应**：看到“把 s 分成 k 段，重新排列得到 t”，自然想到枚举所有排列（暴力）——这是一种直觉但不切实际的思路。  
- **最容易踩的坑**  
  1. **忘记长度必须整除**：题目保证 `len(s) % k == 0`，但实现时仍需自行计算每段长度 `L`。  
  2. **忽视子串相同但位置不同**：即使两个子串内容相同，它们在哈希表里应该计数两次，而不是只保留一次。  
  3. **边界条件**：`k = 1` 时，只能比较整体字符串是否相等；`k = n` 时，每段长度为 1，实际上是比较两个字符串的字符频率（这时答案一定为 `True` 因为已知是字母异位词）。  
- **下次遇到同类题的第一步**：**先把字符串切块，统计每块出现次数，再与目标字符串的块计数做比较**——这一步骤往往能在 O(n) 时间内直接给出答案，避免陷入指数级的枚举。