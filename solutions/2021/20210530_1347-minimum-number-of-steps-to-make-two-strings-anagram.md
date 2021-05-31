# #1347. **使两个字符串成为字谜的最少操作次数** / Minimum Number of Steps to Make Two Strings Anagram

> 难度：中等 · 标签：Hash Table、String、Counting · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-steps-to-make-two-strings-anagram/)

---

## 题目（英文原版）

**Description**

You are given two strings of the same length s and t. In one step you can choose any character of t and replace it with another character.
Return the minimum number of steps to make t an anagram of s.
An Anagram of a string is a string that contains the same characters with a different (or the same) ordering.

**Examples**

**Example 1:**

```
Input: s = "bab", t = "aba"
Output: 1
Explanation: Replace the first 'a' in t with b, t = "bba" which is anagram of s.
```

**Example 2:**

```
Input: s = "leetcode", t = "practice"
Output: 5
Explanation: Replace 'p', 'r', 'a', 'i' and 'c' from t with proper characters to make t anagram of s.
```

**Example 3:**

```
Input: s = "anagram", t = "mangaar"
Output: 0
Explanation: "anagram" and "mangaar" are anagrams.
```

**Constraints**

- 1 <= s.length <= 5 * 104
- s.length == t.length
- s and t consist of lowercase English letters only.

---

## 题目（中文翻译）

给定两个等长的字符串 `s` 和 `t`。在一次操作中，你可以选择 `t` 中的任意字符并将其替换为另一个字符。返回使 `t` 成为 `s` 的字谜（anagram）的最少操作次数。

字谜（anagram）是指一个字符串包含与另一个字符串相同的字符，只是顺序可能不同（也可能相同）。

**示例 1：**  
**输入：** `s = "bab", t = "aba"`  
**输出：** `1`  
**解释：** 将 `t` 中的第一个 `'a'` 替换为 `'b'`，得到 `t = "bba"`，此时 `t` 与 `s` 是字谜。

**示例 2：**  
**输入：** `s = "leetcode", t = "practice"`  
**输出：** `5`  
**解释：** 将 `t` 中的 `'p'、'r'、'a'、'i'、'c'` 替换为适当的字符，使得 `t` 成为 `s` 的字谜。

**示例 3：**  
**输入：** `s = "anagram", t = "mangaar"`  
**输出：** `0`  
**解释：** `"anagram"` 与 `"mangaar"` 已经是字谜。

**约束条件：**  
- `1 <= s.length <= 5 * 10^4`  
- `s.length == t.length`  
- `s` 和 `t` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**逐个字符去匹配**。  
我们从左到右遍历字符串 `s`，对每个字符 `c` 在 `t` 中寻找一个相同的 `c`：

1. 如果在 `t` 中找到了，就把这两个位置标记为「已经配对」；
2. 如果找不到，就说明 `t` 中缺少这个字符，需要把 `t` 的某个位置的字符改成 `c`，步骤数 +1。

这里可以把 `t` 看成一本「字典」，我们每次都在字典里「查找」是否有对应的词（字符）。如果没有，就「改写」字典里任意一个词，使其变成我们想要的。

这种做法一定能得到答案，因为每次我们都确保 `s` 的字符在 `t` 中出现（要么本来就有，要么通过一次替换得到），最后 `t` 的字符集合必然和 `s` 完全相同，也就是它们是 anagram。

**为什么会慢？**  
在最坏情况下，`t` 中没有任何与 `s` 匹配的字符。此时我们要对 `s` 的每个字符在 `t` 中遍历全部字符来判断「有没有」。这相当于两层循环，时间复杂度是 **O(n²)**（n 为字符串长度）。对于长度可达 5·10⁴ 的数据，这会超时。

#### 代码（Python）

```python
def minSteps_brute(s: str, t: str) -> int:
    n = len(s)
    # 用一个列表标记 t 中哪些位置已经被配对
    used = [False] * n
    steps = 0

    for i, ch in enumerate(s):               # 遍历 s 的每个字符
        found = False
        # 在 t 中找一个未被使用且字符相同的位置
        for j in range(n):
            if not used[j] and t[j] == ch:
                used[j] = True               # 标记为已配对
                found = True
                break
        # 如果找不到，说明需要一次替换
        if not found:
            # 随便找一个未使用的位置进行「替换」即可
            for j in range(n):
                if not used[j]:
                    used[j] = True
                    break
            steps += 1                         # 替换一次，步数加一
    return steps
```

> **关键行中文注释**已经写在代码里，方便对每一步的意义进行快速定位。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  直观理解：我们对 `s` 的每个字符，都要在 `t` 里遍历一次（最坏情况是全部遍历），于是出现了「平方」级的工作量。  
- **空间复杂度**：`O(n)`  
  需要一个长度为 `n` 的 `used` 数组来记录 `t` 中哪些字符已经被配对，额外使用的空间随输入规模线性增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**真正耗时的地方在于不断在 `t` 中寻找匹配字符**。  
如果我们把「每个字符出现多少次」这件事提前统计好，就不需要再遍历去找了——只要比较两个统计结果，就能直接得到需要替换的次数。

**核心技巧：字符计数（哈希表 / 固定大小数组）**  

- 把 `s` 中每个字符出现的次数记在一个长度为 26 的数组 `cnt_s`（下标 0 对应 `'a'`，1 对应 `'b'` ……）。
- 同理，把 `t` 中每个字符出现的次数记在 `cnt_t`。
- 对于某个字符 `c`，如果 `cnt_t[c]` **小于** `cnt_s[c]`，说明 `t` 缺少 `cnt_s[c] - cnt_t[c]` 个 `c`，必须把别的字符替换成 `c`。把所有字符的缺口加起来，就是最少的替换步数。

这一步只需要 **一次遍历**（O(n)）来统计频次，再 **一次遍历**（O(26)）来计算缺口，总体仍是线性时间。

> **类比**：把 `s` 看成一本「需求清单」，`t` 看成「仓库库存」。我们只要把需求清单上缺少的数量全部补齐，就完成了「配货」——不必去一件件比对，只要看数量差。

#### 代码（Python）

```python
def minSteps(s: str, t: str) -> int:
    # 26 个小写字母的计数数组，初始全部为 0
    cnt_s = [0] * 26
    cnt_t = [0] * 26

    # 统计 s 中每个字符的出现次数
    for ch in s:
        idx = ord(ch) - ord('a')   # 将字符映射到 0~25 的下标
        cnt_s[idx] += 1

    # 统计 t 中每个字符的出现次数
    for ch in t:
        idx = ord(ch) - ord('a')
        cnt_t[idx] += 1

    steps = 0
    # 只要 t 中的数量不足，就需要补齐
    for i in range(26):
        if cnt_t[i] < cnt_s[i]:
            steps += cnt_s[i] - cnt_t[i]   # 缺少的个数累计到答案

    return steps
```

> 代码中每一行都配有中文注释，帮助初学者快速了解「为什么」要这么写。

#### 复杂度

- **时间复杂度**：`O(n)`  
  只遍历了两遍字符串（各 O(n)），以及一次固定长度（26）的循环。可以把「O(n)」想象成「随输入长度线性增长的工作量」，远远快于 O(n²)。
- **空间复杂度**：`O(1)`（常数空间）  
  虽然用了两个长度为 26 的数组，但它们的大小与输入规模无关，始终是固定的 26×2 个整数，所以称为常数空间。

---

## 心得

- **核心技巧**：**字符计数（哈希表/数组）** 用来比较两个字符串的字符构成，是处理「anagram」或「字符差异」类问题的万能钥匙。
- **适用题型**  
  1. *2420. Find All Good Indices*（需要统计窗口内字符出现次数）  
  2. *383. Ransom Note*（判断能否用一段文字拼出另一段文字）  
  3. *448. Find All Numbers Disappeared in an Array*（利用计数或标记技巧）
- **一句话总结**：先把「有多少」算清楚，再比较「缺了多少」——不必逐个匹配，直接用计数差得到最少步数。

## 反思

- **第一反应**：看到「把 t 变成 s 的 anagram」就想到「逐字符替换」或「把 t 中多余的字符删掉再补上」。
- **最容易踩的坑**  
  - **只算多余的字符**：如果只统计 `t` 中多余的字符，而不考虑 `s` 中缺少的，会得到错误答案。正确做法是只看 `t` **不足** 的部分。  
  - **字符范围假设错误**：题目保证都是小写字母，才能用长度为 26 的数组；若忽视这一点，直接使用 Python 的 `dict` 也可以但会稍慢。  
  - **忘记返回 0**：当两个字符串已经是 anagram 时，计数差全为 0，答案应为 0，别因为循环逻辑写成了 `steps = max(steps, 0)` 之类的多余判断。
- **下次类似题的第一步**：先问自己「这道题需要比较两个集合的组成吗？」如果答案是「是」，立刻想到「计数/哈希表」——这一步往往能把时间复杂度从 O(n²) 降到 O(n)。