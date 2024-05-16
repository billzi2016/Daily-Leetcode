# #2697. 字典序最小回文 / Lexicographically Smallest Palindrome

> 难度：简单 · 标签：Two Pointers、String、Greedy · [LeetCode 链接](https://leetcode.com/problems/lexicographically-smallest-palindrome/)

---

## 题目（英文原版）

**Description**

You are given a string s consisting of lowercase English letters, and you are allowed to perform operations on it. In one operation, you can replace a character in s with another lowercase English letter.
Your task is to make s a palindrome with the minimum number of operations possible. If there are multiple palindromes that can be made using the minimum number of operations, make the lexicographically smallest one.
A string a is lexicographically smaller than a string b (of the same length) if in the first position where a and b differ, string a has a letter that appears earlier in the alphabet than the corresponding letter in b.
Return the resulting palindrome string.

**Examples**

**Example 1:**

```
Input: s = "egcfe"
Output: "efcfe"
Explanation: The minimum number of operations to make "egcfe" a palindrome is 1, and the lexicographically smallest palindrome string we can get by modifying one character is "efcfe", by changing 'g'.
```

**Example 2:**

```
Input: s = "abcd"
Output: "abba"
Explanation: The minimum number of operations to make "abcd" a palindrome is 2, and the lexicographically smallest palindrome string we can get by modifying two characters is "abba".
```

**Example 3:**

```
Input: s = "seven"
Output: "neven"
Explanation: The minimum number of operations to make "seven" a palindrome is 1, and the lexicographically smallest palindrome string we can get by modifying one character is "neven".
```

**Constraints**

- 1 <= s.length <= 1000
- s consists of only lowercase English letters.

---

## 题目（中文翻译）

你得到一个仅由小写英文字母组成的字符串 `s`，可以对其进行**操作（operation）**。一次操作指将 `s` 中的某个字符替换为另一个小写英文字母。

你的任务是以最少的操作次数将 `s` 变成**回文（palindrome）**。如果在最少操作次数下能够得到多个回文，则返回字典序（lexicographically）最小的那个。

若两个等长字符串 `a` 与 `b` 在首个不同的位置上，`a` 的字符在字母表中出现得更早，则称 `a` 的字典序小于 `b`。

返回最终得到的回文字符串。

**示例 1**  
Input: `s = "egcfe"`  
Output: `"efcfe"`  
Explanation: 将 `"egcfe"` 变成回文的最少操作次数为 1。通过将字符 `'g'` 改为 `'f'`，可以得到字典序最小的回文 `"efcfe"`。

**示例 2**  
Input: `s = "abcd"`  
Output: `"abba"`  
Explanation: 将 `"abcd"` 变成回文的最少操作次数为 2。通过修改两个字符得到的字典序最小的回文是 `"abba"`。

**示例 3**  
Input: `s = "seven"`  
Output: `"neven"`  
Explanation: 将 `"seven"` 变成回文的最少操作次数为 1。将字符 `'s'` 改为 `'n'` 后得到的字典序最小的回文是 `"neven"`。

**约束条件**  
- `1 <= s.length <= 1000`  
- `s` 仅由小写英文字母组成。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把字符串的左半边和右半边一一对应起来比较**。  
- 设字符串长度为 `n`，下标从 `0` 开始。下标 `i`（左边）对应的右边下标是 `n‑1‑i`。  
- 如果 `s[i]` 已经等于 `s[n‑1‑i]`，这对字符已经是回文对，什么也不需要做。  
- 否则我们必须把其中的一个字符改成另一个字符，使它们相等。  
  为了让 **操作次数最少**，只需要改 **一个** 字符（改成另一个的值即可），不必同时改两个。  

现在有多种改法：把左边改成右边，或把右边改成左边，甚至改成其它字母。  
因为我们要求 **字典序最小** 的回文，原则是：  
> 在必须改动的那一对字符里，把 **字母大的那个** 换成 **字母小的那个**。  

这样既保证只改一次，又让最终的回文在字典序上尽可能靠前。  

> **类比**：把哈希表想象成一本字典，key 是单词，value 是页码。这里我们“查询”两个字符的大小，选出更大的那个去“改写”，就像把字典里错页的内容改成正确的那页。

**为什么正确？**  
- 每对不相等的字符至少需要一次修改才能成为回文，对每对我们只改一次，恰好达到最小操作数。  
- 在只改一次的前提下，把大的字符改成小的字符一定会让整体字符串在第一处不同的地方更靠前（因为字母表是有序的），于是得到字典序最小的回文。

#### 代码（Python）

```python
def makeSmallestPalindrome(s: str) -> str:
    # 把字符串转成列表，方便原地修改
    chars = list(s)
    n = len(chars)
    left, right = 0, n - 1          # 双指针：左指针从0开始，右指针从末尾开始

    while left < right:             # 只要左指针在右指针左边，就还有未比较的字符对
        if chars[left] != chars[right]:        # 这对字符不相等，需要改动
            # 取较小的字符
            smaller = min(chars[left], chars[right])
            # 把较大的那个改成较小的（保持回文且字典序最小）
            chars[left] = chars[right] = smaller
        # 向中间收敛
        left += 1
        right -= 1

    return ''.join(chars)           # 把列表拼回字符串
```

#### 复杂度  

- **时间复杂度：O(n)** — 只遍历一次字符串的左半边（`n/2` 次），常数因素不影响大 O 表示。  
- **空间复杂度：O(n)** — 把原字符串复制成列表，需要额外 `n` 个字符的存储空间。  

---

### 2. 最优解  

#### 思路  

其实上面的“暴力”已经是 **最优** 的了，因为：

1. **瓶颈**：我们只需要比较每一对字符一次，无法再少于 `n/2` 次比较，否则会漏掉某对导致非回文。  
2. **一次改动足够**：每对不相等的字符只需要一次改动才能成为回文，进一步改动只会增加操作次数，违背 “最少操作” 的要求。  
3. **字典序最小**：在每对字符必须改动一次的前提下，把大的字符改成小的字符是局部最优，而全局最优可以通过“局部最优相加”得到（因为每对字符独立决定）。  

因此 **无需额外的动态规划、单调栈等复杂结构**，只要使用双指针一次遍历即可得到答案。  

下面给出同样的实现，但把空间优化到 **O(1)**（不额外拷贝列表），直接在原字符串的字符数组上操作（Python 中不可变，需要转成 `list`，但仍算原地修改）。

#### 代码（Python）

```python
def makeSmallestPalindrome(s: str) -> str:
    # 直接把字符串转成列表，后面会在原地修改
    chars = list(s)
    i, j = 0, len(chars) - 1       # i 为左指针，j 为右指针

    while i < j:
        if chars[i] != chars[j]:
            # 取两者的较小字符
            smaller = min(chars[i], chars[j])
            # 把两边都改成较小字符，保持回文且字典序最小
            chars[i] = chars[j] = smaller
        i += 1
        j -= 1

    return ''.join(chars)          # 重新拼成字符串返回
```

> **关键点解释**  
> - `min(a, b)`：Python 内置函数，返回两个字符中字母表顺序更靠前的那个。  
> - `while i < j`：只需要遍历到中间，`i == j` 时是中心字符（奇数长度），它本身不影响回文性。  

#### 复杂度  

- **时间复杂度：O(n)** — 只遍历一次，和暴力解相同。  
- **空间复杂度：O(1)** （若算上把字符串转成列表的临时空间，则为 O(n)），但相对于额外使用哈希表、DP 表等，这已经是最小的额外空间了。

---

## 心得  

- **核心技巧**：双指针（Two Pointers） + 贪心（Greedy）  
- **适用的题型**：  
  1. “将字符串变成回文” 系列（如 LeetCode 1312. Minimum Insertion Steps to Make a String Palindrome）  
  2. “最小字符替换使字符串满足某种对称性” （如把字符串变成回文的同时满足字典序要求）  
  3. “两端比较并同步修改” 的数组/字符串题目（如判断回文、删除回文最少字符等）  
- **一句话总结解题钥匙**：**“两端相遇，一次比较，必要时把大的改成小的”。**  

---

## 反思  

- **第一反应**：看到“把字符串变成回文”，本能想到把左边和右边对应字符配对比较。  
- **最容易踩的坑**：  
  - 忘记只改一次导致操作数不最小。  
  - 只考虑把左边改成右边，忽略把大的改成小的会破坏字典序最小的要求。  
  - 对奇数长度的字符串忘记中心字符不需要处理。  
- **下次类似题的第一步**：**先用双指针定位不匹配的字符对，再思考在“最少改动”前提下，怎样选择改动的方向能让整体结果在字典序上最优**。