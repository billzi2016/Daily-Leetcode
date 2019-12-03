# #680. 验证回文 II / Valid Palindrome II

> 难度：简单 · 标签：Two Pointers、String、Greedy · [LeetCode 链接](https://leetcode.com/problems/valid-palindrome-ii/)

---

## 题目（英文原版）

**Description**

Given a string s, return true if the s can be palindrome after deleting at most one character from it.

**Examples**

**Example 1:**

```
Input: s = "aba"
Output: true
```

**Example 2:**

```
Input: s = "abca"
Output: true
Explanation: You could delete the character 'c'.
```

**Example 3:**

```
Input: s = "abc"
Output: false
```

**Constraints**

- 1 <= s.length <= 105
- s consists of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串 `s`，如果在至多删除一个字符（character）后，`s` 能成为回文（palindrome），则返回 `true`。

**示例 1**  
Input: `s = "aba"`  
Output: `true`

**示例 2**  
Input: `s = "abca"`  
Output: `true`  
Explanation: 你可以删除字符 `'c'`。

**示例 3**  
Input: `s = "abc"`  
Output: `false`

**约束条件**  
- `1 <= s.length <= 10^5`  
- `s` 只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**把每一个字符都尝试删掉一次**，看剩下的字符串能否成为回文。  
- 先写一个判断回文的函数 `is_palindrome(s)`，它从左到右、从右到左同时比较字符，就像我们平时把单词倒着读一样。  
- 对于原字符串 `s`，先检查不删任何字符的情况（因为“最多删一个”也包括“一个也不删”）。  
- 然后遍历下标 `i = 0 … len(s)-1`，把第 `i` 个字符删掉（即拼接 `s[:i] + s[i+1:]`），再用 `is_palindrome` 检查。  
- 只要有一次检查返回 `True`，说明可以通过至多一次删除得到回文，直接返回 `True`；全部尝试完仍未成功，返回 `False`。

> **类比**：把哈希表想象成一本字典，键（key）是单词，值（value）是页码。这里我们用的“删除字符”相当于把字典里的一页撕掉，然后再看剩下的内容是否还能前后对称。

这种做法一定能得到正确答案，因为它把**所有**可能的删法都穷举了。

#### 代码（Python）
```python
def validPalindrome_bruteforce(s: str) -> bool:
    """暴力解：枚举每一个可能的删除位置，检查是否为回文"""

    def is_palindrome(t: str) -> bool:
        """判断字符串 t 是否是回文（两端指针逐步逼近）"""
        left, right = 0, len(t) - 1
        while left < right:
            if t[left] != t[right]:
                return False
            left += 1
            right -= 1
        return True

    # 先检查不删字符的情况
    if is_palindrome(s):
        return True

    # 枚举删除第 i 个字符的可能
    for i in range(len(s)):
        # 构造删掉第 i 个字符后的新字符串
        candidate = s[:i] + s[i + 1:]
        if is_palindrome(candidate):
            return True

    # 所有尝试都失败，返回 False
    return False
```

#### 复杂度
- **时间复杂度**：`O(n²)`  
  解释：外层循环遍历 `n` 次，每次都要调用 `is_palindrome` 检查长度约为 `n` 的子串，最坏情况下需要比较 `n/2` 次字符，整体是 `n × n`，即 `n²`。  
- **空间复杂度**：`O(1)`（不计入返回的临时字符串）  
  解释：只使用了常数个指针变量和一个临时的切片（Python 切片会生成新对象，但在分析算法本身时我们只关注额外的 *额外* 空间）。

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在于**每次都重新构造并遍历整个子串**。我们可以利用回文本身的“对称”特性，**一次遍历就找出唯一的冲突点**，然后只尝试两种可能的删除方式。

1. **双指针**：设左指针 `l = 0`，右指针 `r = len(s)-1`，向中间逼近。  
2. 当 `s[l] == s[r]` 时，说明这对字符已经匹配，继续 `l += 1, r -= 1`。  
3. 当出现 **不匹配**（`s[l] != s[r]`）时，说明只能在 `l` 或 `r` 位置删掉一个字符。此时分两种情况检查：
   - **跳过左字符**：检查子串 `s[l+1 : r+1]` 是否是回文。  
   - **跳过右字符**：检查子串 `s[l : r]` 是否是回文。  
   只要其中一种成立，就可以通过至多一次删除得到回文。  
4. 若遍历完整个字符串都没有冲突，说明原字符串本身已经是回文，直接返回 `True`。

> **为什么只需要检查这两种情况？**  
> 因为我们已经确定冲突只发生在 `l` 与 `r` 这两个位置。若在 `l` 位置删字符后仍然不匹配，那么唯一的可能只能是删 `r` 位置的字符。再往外删别的字符已经不可能只删一次就恢复对称了。

> **类比**：把双指针想象成两个人站在走廊两端向中间走，遇到不一致的鞋子（左脚和右脚颜色不同），只能把左边或右边的鞋子换掉一次，看看剩下的鞋子能否全部匹配。

#### 代码（Python）
```python
def validPalindrome(s: str) -> bool:
    """最优解：双指针一次遍历，冲突点只尝试两种删除方式"""

    def is_palindrome_range(left: int, right: int) -> bool:
        """
        判断子串 s[left:right+1] 是否是回文。
        只使用指针，不生成新字符串，空间保持 O(1)。
        """
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True

    left, right = 0, len(s) - 1
    while left < right:
        if s[left] == s[right]:
            left += 1
            right -= 1
        else:
            # 第一次不匹配，尝试跳过左字符或右字符
            skip_left  = is_palindrome_range(left + 1, right)   # 删除 s[left]
            skip_right = is_palindrome_range(left, right - 1)   # 删除 s[right]
            return skip_left or skip_right   # 任意一种成功即返回 True
    # 完全匹配，原字符串已经是回文
    return True
```

#### 复杂度
- **时间复杂度**：`O(n)`  
  解释：指针只会从两端各移动一次，最多遍历整个字符串一次。即使在冲突点调用 `is_palindrome_range`，它只检查剩余的子串，最多也只遍历剩下的字符一次，整体仍是线性 `n`。  
- **空间复杂度**：`O(1)`  
  解释：只使用了若干整数指针 `left, right`，没有额外的数组或递归栈。

---

## 心得

- **核心技巧**：双指针 + 贪心（在第一次冲突处做一次“尝试性删除”）。  
- **适用的题型**：  
  1. **Valid Palindrome**（不允许删除）——只需要双指针判断。  
  2. **Longest Substring Without Repeating Characters**（需要滑动窗口）——也是指针类的贪心。  
  3. **Maximum Number of K‑Sorted Subarrays**（需要局部检查）——可以用类似的局部验证思路。  
- **一句话总结**：**只要找出第一个不匹配的位置，删左或删右，两次检查就能决定答案**。

---

## 反思

- **第一反应**：直接把每个字符都删掉尝试，想到要遍历所有可能。  
- **最容易踩的坑**：  
  - 忘记“最多一次删除”也包括“零次删除”，所以要先判断原字符串是否已是回文。  
  - 在冲突点检查子串时，必须使用 **闭区间**（`right` 包含在内），否则会漏掉最后一个字符的比较。  
  - 字符串长度可能达到 `10⁵`，若使用 `s[:i] + s[i+1:]` 会产生大量临时字符串，导致超时。  
- **下次遇到同类题**：第一步先用双指针找冲突点，若冲突则只考虑**局部的有限几种修正**（如删除、替换），避免全局暴力。