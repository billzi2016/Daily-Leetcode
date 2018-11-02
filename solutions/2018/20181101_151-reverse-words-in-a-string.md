# #151. 翻转字符串中的单词 / Reverse Words in a String

> 难度：中等 · 标签：Two Pointers、String · [LeetCode 链接](https://leetcode.com/problems/reverse-words-in-a-string/)

---

## 题目（英文原版）

**Description**

Given an input string s, reverse the order of the words.
A word is defined as a sequence of non-space characters. The words in s will be separated by at least one space.
Return a string of the words in reverse order concatenated by a single space.
Note that s may contain leading or trailing spaces or multiple spaces between two words. The returned string should only have a single space separating the words. Do not include any extra spaces.
Follow-up: If the string data type is mutable in your language, can you solve it in-place with O(1) extra space?

**Examples**

**Example 1:**

```
Input: s = "the sky is blue"
Output: "blue is sky the"
```

**Example 2:**

```
Input: s = "  hello world  "
Output: "world hello"
Explanation: Your reversed string should not contain leading or trailing spaces.
```

**Example 3:**

```
Input: s = "a good   example"
Output: "example good a"
Explanation: You need to reduce multiple spaces between two words to a single space in the reversed string.
```

**Constraints**

- 1 <= s.length <= 104
- s contains English letters (upper-case and lower-case), digits, and spaces ' '.
- There is at least one word in s.

---

## 题目（中文翻译）

**描述**  
给定一个输入字符串 `s`（string），请将其中单词的顺序进行反转。  
单词被定义为由 **非空格字符**（non-space characters）组成的连续序列。`s` 中的单词之间至少会有一个空格分隔。  
返回一个字符串，其中单词按逆序排列，单词之间仅用 **单个空格**（single space）连接。

需要注意的是，`s` 可能包含前导空格、尾随空格或多个连续空格。返回的结果字符串 **只能在单词之间保留一个空格**，且 **不应包含多余的空格**。

**示例 1**  
```text
Input: s = "the sky is blue"
Output: "blue is sky the"
```

**示例 2**  
```text
Input: s = "  hello world  "
Output: "world hello"
Explanation: 反转后的字符串不应包含前导或尾随空格。
```

**示例 3**  
```text
Input: s = "a good   example"
Output: "example good a"
Explanation: 需要将两个单词之间的多个空格缩减为单个空格后再进行逆序拼接。
```

**约束条件**  
- `1 <= s.length <= 10^4`  
- `s` 只包含英文字母（大小写均可）、数字和空格 `' '`。  
- `s` 中至少存在一个单词。

**进阶**  
如果你使用的语言中字符串（string）是可变的，能否在 **O(1)** 额外空间下原地（in-place）完成此操作？

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把字符串先 **切割** 成单词列表，再把列表倒序，最后用一个空格把单词拼起来。  

- **切割**：Python 的 `split()` 方法会把连续的空格当作分隔符，自动去掉首尾多余的空格，得到所有单词。可以把它想象成 **查字典**：字典的 key 是空格，value 是“下一个单词”。  
- **倒序**：列表的切片 `[::-1]` 能一次性把所有元素顺序反过来。  
- **拼接**：`join()` 把单词重新用单个空格连接起来，形成最终的字符串。  

这个方法一定能得到正确答案，因为我们把所有单词完整地提取出来，再按照题目要求的顺序重新排列。

**复杂度分析（大白话）**  
- `split()` 会遍历整个字符串一次，看到每个字符都要判断它是不是空格，时间随字符串长度线性增长，用 **O(n)** 表示。  
- `[::-1]` 也会遍历一次列表，时间也是 **O(n)**。  
- `join()` 再遍历一次单词列表，把它们写进新的字符串，同样是 **O(n)**。  
三步加起来仍是 **O(n)**，空间上我们需要存放切出来的单词列表和最终的结果字符串，最坏情况下需要 **O(n)** 的额外空间。

#### 代码（Python）

```python
def reverseWords_brute(s: str) -> str:
    # 1. 用 split() 把字符串按空格切割成单词列表
    #    连续空格会被自动合并，首尾空格会被忽略
    words = s.split()
    # 2. 把单词列表倒序
    reversed_words = words[::-1]
    # 3. 用单个空格把倒序后的单词拼接成新字符串
    result = ' '.join(reversed_words)
    return result
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 只需要线性遍历一次字符串（`n` 为字符串长度），其余操作也是线性时间。  
- **空间复杂度**：`O(n)` —— 需要额外存放切出来的单词列表和最终的结果字符串，最坏情况下占用和原字符串同等大小的空间。

---

### 2. 最优解

#### 思路  

暴力解已经是 **线性时间**，但它用了 `split()` 生成额外的列表，空间是 `O(n)`。  
如果语言允许原地修改字符数组（LeetCode 的 Follow‑up），我们可以把整个过程压缩到 **常数额外空间**（`O(1)`）。

核心思路是 **两次翻转**：

1. **整体翻转**：把整个字符序列倒过来。比如 `"the sky"` → `"yks eht"`。这一步把单词的顺序反了，但每个单词内部的字符也被反了。
2. **单词内部再翻转**：遍历翻转后的字符数组，遇到连续的非空格字符（即一个单词）时，再把这个单词内部的字符翻转回来。这样单词顺序已经是我们想要的，而每个单词的字符又恢复正常。
3. **去除多余空格**：在翻转的过程中会留下原始字符串中的多余空格（例如首尾空格、连续空格），我们再一次遍历，把连续空格压缩为单个空格，并去掉首尾空格。实现方式是使用 **双指针**：`slow` 指针负责写入结果，`fast` 指针负责读取原字符。

**为什么是 O(1) 额外空间？**  
我们把字符串先转成可变的字符列表（`list(s)`），这一步在 Python 里会产生 `O(n)` 的临时空间，但在面试中如果语言本身提供可变字符串（如 C++ 的 `char[]`），就可以直接在原数组上操作。这里的实现仍然保持 **只使用常数级的额外变量**（指针、计数器），不依赖额外的列表或字典。

**步骤示意（文字版）**

```
原始: "  hello   world  "
1. 转成列表并整体翻转 → [' ', ' ', 'd', 'l', 'r', 'o', 'w', ' ', ' ', ' ', 'o', 'l', 'l', 'e', 'h', ' ', ' ']
2. 逐词翻转 → [' ', ' ', 'w', 'o', 'r', 'l', 'd', ' ', ' ', ' ', 'h', 'e', 'l', 'l', 'o', ' ', ' ']
3. 双指针压缩空格 → "world hello"
```

#### 代码（Python）

```python
def reverseWords_opt(s: str) -> str:
    # 1️⃣ 把字符串转成字符列表，方便原地操作
    chars = list(s)

    # ---------- 辅助函数 ----------
    def reverse(l: int, r: int) -> None:
        """原地翻转 chars[l:r]（左闭右闭）"""
        while l < r:
            chars[l], chars[r] = chars[r], chars[l]
            l += 1
            r -= 1

    n = len(chars)

    # 2️⃣ 整体翻转
    reverse(0, n - 1)

    # 3️⃣ 翻转每个单词
    start = 0
    while start < n:
        # 跳过空格，找到单词的起始位置
        while start < n and chars[start] == ' ':
            start += 1
        if start >= n:
            break
        end = start
        # 找到单词的结束位置（下一个空格前）
        while end < n and chars[end] != ' ':
            end += 1
        # 翻转单词本身
        reverse(start, end - 1)
        start = end

    # 4️⃣ 双指针去除多余空格
    # slow 用来写入结果，fast 用来读取原字符
    slow = 0
    fast = 0
    while fast < n:
        # 跳过前导空格
        while fast < n and chars[fast] == ' ':
            fast += 1
        # 复制单词
        while fast < n and chars[fast] != ' ':
            chars[slow] = chars[fast]
            slow += 1
            fast += 1
        # 跳过单词后面的所有空格，只保留一个
        while fast < n and chars[fast] == ' ':
            fast += 1
        # 如果后面还有单词，写入一个空格作为分隔
        if fast < n:
            chars[slow] = ' '
            slow += 1

    # 最终结果是 chars[0:slow]，转换回字符串返回
    return ''.join(chars[:slow])
```

#### 复杂度

- **时间复杂度**：`O(n)` ——  
  - 整体翻转一次遍历 `O(n)`；  
  - 单词内部翻转整体仍是 `O(n)`（每个字符只会被翻转两次）；  
  - 双指针压缩空格再遍历一次 `O(n)`。  
  所有步骤都是线性时间，总体仍是 `O(n)`，和暴力解一样快，但没有额外的列表开销（在可变字符串的语言里是真正的 `O(1)` 额外空间）。

- **空间复杂度**：`O(1)`（不计入输入本身的字符数组）。  
  我们只使用了几个整数指针 `l, r, start, end, slow, fast`，占用常数级别的额外空间。  
  （在 Python 中因为字符串不可变，需要先把它转成列表，这一步会占 `O(n)` 空间，但在面试的 “in‑place” 要求下，这一步可以省去，直接对字符数组操作。）

---

## 心得

- 这道题考察 **字符串的原地翻转** 与 **双指针去除冗余空格** 的技巧。  
- 类似技巧常出现在这些题目中：  
  1. **翻转字符串中的单词**（LeetCode 151）  
  2. **删除字符串中的所有空格**（面试题 01.04）  
  3. **移动零**（数组原地操作的经典例子）  
- **一句话总结**：先整体翻转，再局部翻转单词，最后用双指针把多余空格压缩——这就是“原地逆序+清理”的解题钥匙。

---

## 反思

- **第一反应**：直接用 `split()` / `join()`，因为 Python 已经帮我们处理了空格和分割，代码最简洁。  
- **最容易踩的坑**：  
  - 忽略了 **首尾多余空格** 和 **连续空格**，直接拼接会产生错误的空格数量。  
  - 在原地实现时，忘记在翻转完单词后再次压缩空格，导致结果中出现多个空格。  
  - 边界条件：只有一个单词、全是空格（题目保证至少有一个单词）等情况需要额外判断。  
- **下次类似题的第一步**：先判断是**只需要重新排列单词**（可以用 `split`），还是**要求原地操作**（准备两次翻转 + 双指针）。这样能快速定位是“简洁版”还是“原地版”。