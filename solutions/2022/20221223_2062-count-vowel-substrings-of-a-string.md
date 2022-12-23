# #2062. 统计字符串中的元音子串 / Count Vowel Substrings of a String

> 难度：简单 · 标签：Hash Table、String · [LeetCode 链接](https://leetcode.com/problems/count-vowel-substrings-of-a-string/)

---

## 题目（英文原版）

**Description**

A substring is a contiguous (non-empty) sequence of characters within a string.
A vowel substring is a substring that only consists of vowels ('a', 'e', 'i', 'o', and 'u') and has all five vowels present in it.
Given a string word, return the number of vowel substrings in word.

**Examples**

**Example 1:**

```
Input: word = "aeiouu"
Output: 2
Explanation: The vowel substrings of word are as follows (underlined):
- "aeiouu"
- "aeiouu"
```

**Example 2:**

```
Input: word = "unicornarihan"
Output: 0
Explanation: Not all 5 vowels are present, so there are no vowel substrings.
```

**Example 3:**

```
Input: word = "cuaieuouac"
Output: 7
Explanation: The vowel substrings of word are as follows (underlined):
- "cuaieuouac"
- "cuaieuouac"
- "cuaieuouac"
- "cuaieuouac"
- "cuaieuouac"
- "cuaieuouac"
- "cuaieuouac"
```

**Constraints**

- 1 <= word.length <= 100
- word consists of lowercase English letters only.

---

## 题目（中文翻译）

一个子串（substring）是字符串中连续的（非空）字符序列。  
元音子串（vowel substring）是仅由元音字符（'a', 'e', 'i', 'o', 'u'）组成且在其中出现了全部五个元音的子串。  
给定字符串 `word`，返回 `word` 中元音子串的数量。

**示例 1**  
**示例 2**  
**示例 3**  

**约束条件**

- `1 <= word.length <= 100`
- `word` 仅由小写英文字母组成。

---

### 示例

#### 示例 1
**输入**  
``` 
word = "aeiouu"
```  
**输出**  
```
2
```  
**解释**  
`word` 的元音子串如下（下划线部分为子串）：
- “aeiouu”
- “aeiouu”

#### 示例 2
**输入**  
``` 
word = "unicornarihan"
```  
**输出**  
```
0
```  
**解释**  
并未出现全部 5 个元音，因此不存在元音子串。

#### 示例 3
**输入**  
``` 
word = "cuaieuouac"
```  
**输出**  
```
7
```  
**解释**  
`word` 的元音子串如下（下划线部分为子串）：
- “cuaieuouac”
- “cuaieuouac”
- “cuaieuouac”
- “cuaieuouac”
- “cuaieuouac”
- “cuaieuouac”
- “cuaieuouac”

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**把所有可能的子串都列举出来**，然后逐个检查：

1. 子串里出现的字符只能是元音（`a, e, i, o, u`）。  
   - 这里可以把元音集合想象成一本“小字典”，查某个字符是否在字典里，只要看它是不是字典的“键”。  
2. 这五个元音必须 **全部出现**，也就是说子串对应的“键集合”必须恰好是 `{a,e,i,o,u}`。  

只要同时满足这两点，就把计数器 `ans` 加一。

> **为什么这种方法一定能得到正确答案？**  
> 因为我们没有遗漏任何子串，也没有错误地把不符合条件的子串算进去。只要遍历完所有子串，答案自然完整。

**时间复杂度**  
- 枚举子串的过程是两层循环：外层选起始位置 `i`，内层选结束位置 `j`，共 `O(n²)` 次。  
- 对每个子串要检查它是否只含元音并且包含全部五个元音，这一步需要遍历子串本身，最坏情况长度是 `n`，所以是 `O(n)`。  
- 综合起来是 **`O(n³)`**。  
  - 大白话：如果字符串长 100，最坏要做 100³ = 1,000,000 次基本操作，虽然在本题数据范围还能跑完，但效率不佳。

**空间复杂度**  
- 只用了常数级别的额外空间（比如存元音集合、计数器），所以是 **`O(1)`**。

#### 代码（Python）

```python
def countVowelSubstrings_bruteforce(word: str) -> int:
    vowels = set('aeiou')                 # 哈希表（集合）像字典，查字符是否是元音 O(1)
    n = len(word)
    ans = 0

    # 枚举所有子串的起点 i
    for i in range(n):
        # 枚举所有子串的终点 j（包含 i，j）
        for j in range(i, n):
            sub = word[i:j+1]              # 当前子串
            # 检查子串是否只由元音组成
            if all(ch in vowels for ch in sub):
                # 检查是否出现了 5 种不同的元音
                if set(sub) == vowels:    # set(sub) 把子串里的字符去重
                    ans += 1
            else:
                # 一旦遇到辅音，后面的更长子串也一定不行，直接跳出内层循环
                break

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n³)` — 三层循环的含义可以想象成“遍历所有起点 → 遍历所有终点 → 再遍历子串内部”。  
- **空间复杂度**：`O(1)` — 只用了几个计数器和一个常量大小的集合。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**每次都要重新遍历子串的字符**。  
实际上我们只需要关注 **连续的元音片段**，因为一旦出现辅音，任何跨过它的子串都不可能是 “只含元音” 的。

**步骤**  

1. **把字符串划分成只含元音的连续块**。  
   - 想象把句子拆成几段 “只说元音的句子”。每段内部我们再去统计满足 “包含全部五个元音” 的子串。  
2. 对每一段使用 **滑动窗口（双指针）** 来统计。  
   - `left` 和 `right` 分别是窗口的左、右边界。窗口里记录每个元音出现的次数（用一个长度为 5 的数组或字典）。  
   - 当窗口已经包含了 5 种元音时，**左边界固定**，右边界再往右扩，所有更长的子串仍然满足条件。此时可以直接把 `len(segment) - right`（从当前 `right` 到段末的所有可能结束位置）加到答案中，然后左移 `left` 继续寻找下一个窗口。  
3. 整个过程只遍历一次字符串，时间是 **线性的**。  

**为什么滑动窗口能一次算完？**  
- 窗口右移时，只会新增一个字符，更新计数是 `O(1)`。  
- 当窗口已经满足“5 元音全出现”这个条件时，左边再收缩只会让情况更差（少了字符），所以左边一定要继续移动，直至窗口不再满足条件。这样每个字符最多被左指针和右指针各访问一次，整体是 `O(n)`。

#### 代码（Python）

```python
def countVowelSubstrings(word: str) -> int:
    vowels = set('aeiou')
    n = len(word)
    ans = 0
    i = 0

    while i < n:
        # 1️⃣ 找到下一个只含元音的连续片段
        if word[i] not in vowels:
            i += 1
            continue

        # 记录片段的起始位置
        start = i
        while i < n and word[i] in vowels:   # 片段一直到出现辅音为止
            i += 1
        end = i                               # 片段区间是 [start, end)

        # 2️⃣ 在该片段内部使用滑动窗口统计
        cnt = {v: 0 for v in vowels}          # 记录每个元音出现次数
        unique = 0                            # 已经出现的不同元音个数
        left = start

        for right in range(start, end):
            ch = word[right]
            if cnt[ch] == 0:                  # 这个元音是第一次出现
                unique += 1
            cnt[ch] += 1

            # 当窗口已经包含全部 5 种元音时
            while unique == 5:
                # 右边界 fixed，左边界 left，后面所有以 right 为左端点的子串
                # （一直扩展到片段末端）都满足条件
                ans += end - right            # end - right 为可选的结束位置数目
                # 收缩左边界，准备寻找下一个窗口
                left_ch = word[left]
                cnt[left_ch] -= 1
                if cnt[left_ch] == 0:
                    unique -= 1               # 少了一种元音
                left += 1

    return ans
```

> **代码要点注释**  
> - `while i < n and word[i] in vowels:` 把只含元音的片段一次性找出来。  
> - `cnt` 和 `unique` 用来实时判断窗口里是否已经出现了全部五种元音。  
> - `ans += end - right` 这一步是核心：只要窗口已经满足条件，**右边界往后再往右扩**（不需要检查），每一种扩展方式都对应一个合法子串。

#### 复杂度  

- **时间复杂度**：`O(n)` — 每个字符至多被左指针和右指针各访问一次。  
  - 与暴力解相比，从“遍历所有子串”降到了“只走一遍字符串”。  
- **空间复杂度**：`O(1)` — 只用了固定大小的哈希表（5 个键）和几个指针变量，和字符串长度无关。

---

## 心得  

- **核心技巧**：**滑动窗口 + 只保留元音的连续块**。  
- 该技巧常用于**“在满足某种条件的子数组/子串中计数”**的问题，例如：  
  1. **最长子串不含重复字符**（LeetCode 3）  
  2. **最小覆盖子串**（LeetCode 76）  
  3. **子数组和等于 K**（LeetCode 560）  
- **一句话总结解题钥匙**：  
  > “先把不可能的字符（辅音）剔除，只在纯元音的区间里，用窗口一次遍历求出所有满足‘五元音全出现’的子串”。  

---

## 反思  

- **第一反应**：把所有子串都列出来检查——这在写代码时最自然，但会导致超时。  
- **最容易踩的坑**：  
  1. **忘记在遍历子串时提前终止**：一旦遇到辅音，后面的更长子串已经不可能是“只含元音”，应立即 `break`。  
  2. **统计全部五个元音时只看出现次数，而不是种类**：必须确保每种元音至少出现一次，而不是出现总次数≥5。  
  3. **边界条件**：字符串全是辅音、或恰好只有 5 个元音且相邻，都要能正确返回 0 或 1。  
- **下次遇到同类题**，第一步应想到：  
  > “先把‘非法字符’切断，把问题限制在连续合法区间内，然后用滑动窗口一次遍历统计”。