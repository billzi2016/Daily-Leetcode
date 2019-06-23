# #467. 环绕字符串中的唯一子串 / Unique Substrings in Wraparound String

> 难度：中等 · 标签：String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/unique-substrings-in-wraparound-string/)

---

## 题目（英文原版）

**Description**

We define the string base to be the infinite wraparound string of "abcdefghijklmnopqrstuvwxyz", so base will look like this:
Given a string s, return the number of unique non-empty substrings of s are present in base.

**Examples**

**Example 1:**

```
Input: s = "a"
Output: 1
Explanation: Only the substring "a" of s is in base.
```

**Example 2:**

```
Input: s = "cac"
Output: 2
Explanation: There are two substrings ("a", "c") of s in base.
```

**Example 3:**

```
Input: s = "zab"
Output: 6
Explanation: There are six substrings ("z", "a", "b", "za", "ab", and "zab") of s in base.
```

**Constraints**

- 1 <= s.length <= 105
- s consists of lowercase English letters.

---

## 题目（中文翻译）

我们定义字符串 **base** 为无限循环的字母表字符串 `"abcdefghijklmnopqrstuvwxyz"`，即 **base** 看起来像：

```
...abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz...
```

给定一个字符串 `s`，返回 `s` 中出现且属于 **base** 的 **唯一**（unique）**非空**（non‑empty）子串（substrings）的数量。

**示例 1**  

**示例 2**  

**示例 3**  

**约束条件**  

- `1 <= s.length <= 10^5`  
- `s` 仅由小写英文字母组成  

---

### 示例

**示例 1**  
**输入**: `s = "a"`  
**输出**: `1`  
**解释**: `s` 中唯一在 **base** 中的子串是 `"a"`。

**示例 2**  
**输入**: `s = "cac"`  
**输出**: `2`  
**解释**: 在 **base** 中出现的子串有两个，分别是 `"a"` 和 `"c"`。

**示例 3**  
**输入**: `s = "zab"`  
**输出**: `6`  
**解释**: 在 **base** 中出现的子串共有六个，分别是 `"z"`、`"a"`、`"b"`、`"za"`、`"ab"` 和 `"zab"`。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是**把所有子串都枚举出来**，然后逐个检查它们是否出现在无限循环的字母表 `"abcdefghijklmnopqrstuvwxyz"` 中。  

- **枚举子串**：把字符串 `s` 看成一本书的每一页，从第 `i` 页开始往后读 `j-i+1` 页，就得到一个子串。这里的“页码”就是下标 `i`、`j`。  
- **检查子串是否合法**：把子串的每两个相邻字符拿出来比较，要求它们在字母表里是相邻的（`'b'` 紧跟 `'a'`），并且最后一个字符 `'a'` 可以视作跟 `'z'` 相邻（因为是循环的）。如果整条子串都满足这个条件，就说明它出现在 **base** 中。  
- **去重**：用一个集合（`set`）把已经出现过的合法子串保存起来，最后集合的大小就是答案。  

> **为什么正确？**  
> 只要子串的字符顺序符合环形字母表的相邻关系，它必然是 **base** 的一段连续子序列。枚举所有子串并逐个验证，必然不会漏掉任何合法子串，也不会把不合法的计进去。

#### 代码（Python）  
```python
def findSubstringInWraproundString_bruteforce(s: str) -> int:
    n = len(s)
    seen = set()                     # 用来去重的集合

    # 枚举所有子串，左端点 i，右端点 j（包含）
    for i in range(n):
        for j in range(i, n):
            sub = s[i:j+1]           # 当前子串
            # 检查 sub 是否满足环形相邻关系
            ok = True
            for k in range(1, len(sub)):
                # 前后字符的 ASCII 码差值应该是 1，或者是 'a' - 'z'（即 -25）
                diff = ord(sub[k]) - ord(sub[k-1])
                if diff != 1 and diff != -25:   # -25 表示从 'z' 跳到 'a'
                    ok = False
                    break
            if ok:
                seen.add(sub)        # 合法子串加入集合

    return len(seen)
```

#### 复杂度  
- **时间复杂度**：`O(n³)`  
  - 外层两层循环枚举子串有 `O(n²)` 次，  
  - 对每个子串最坏要遍历它的全部字符检查相邻关系，平均长度约为 `O(n)`，于是总体是 `O(n³)`。  
  - 用大白话说，如果 `s` 长度是 1000，程序大概要跑 **十亿** 次小操作，明显太慢。  
- **空间复杂度**：`O(n²)`（最坏情况下所有子串都是合法的，需要存进集合）。  

---  

### 2. 最优解  

#### 思路  
暴力解的瓶颈在于**每个子串都要单独检查**，导致大量重复劳动。其实我们只需要关心**以每个字符结尾的最长合法子串长度**，因为：

- 任意一个合法子串 `X`，如果它以字符 `c` 结尾，那么 `X` 必然是以 `c` 结尾的某个更长合法子串的后缀。  
- 对于同一个结尾字符 `c`，只要知道最长的那条“连续环形”路径有多长 `L`，那么以 `c` 结尾的所有不同子串的数量就是 `L`（长度为 1、2、…、L 的子串）。  

于是我们可以用一个长度为 26 的数组 `dp`，`dp[i]` 记录**以字母 `'a'+i` 结尾的最长合法子串的长度**。遍历一次字符串 `s`：

1. 维护一个变量 `cur_len` 表示当前连续环形子串的长度。  
2. 对于当前位置 `j`，如果 `s[j]` 与前一个字符 `s[j-1]` 在环形字母表中相邻（`diff == 1` 或 `diff == -25`），则 `cur_len += 1`；否则 `cur_len = 1`（重新开始）。  
3. 用 `idx = ord(s[j]) - ord('a')` 把字符映射到数组下标，更新 `dp[idx] = max(dp[idx], cur_len)`。因为同一个字符可能在不同位置出现多次，我们只保留最长的那一次。  

遍历结束后，**所有不同合法子串的数量等于 `dp` 中所有元素的和**。  

> **为什么只需要 26 个数字就够了？**  
> 想象每个字母都是一座小塔，塔顶记录的是“以这个字母结尾的最长合法子串有多长”。所有合法子串都可以唯一映射到它们的结尾塔上，塔的高度累加起来就是答案。  

#### 代码（Python）  
```python
def findSubstringInWraproundString(s: str) -> int:
    """
    动态规划 O(n) 解法
    dp[i]：以字符 chr(ord('a') + i) 结尾的最长合法子串长度
    """
    dp = [0] * 26                 # 26 个字母对应的最长长度
    cur_len = 0                   # 当前以 s[j] 结尾的连续环形子串长度

    for j, ch in enumerate(s):
        if j > 0:
            # 判断 s[j] 与前一个字符是否相邻（环形）
            diff = ord(ch) - ord(s[j-1])
            if diff == 1 or diff == -25:   # -25 表示 'z' -> 'a'
                cur_len += 1
            else:
                cur_len = 1                # 重新开始计数
        else:
            cur_len = 1                    # 第一个字符单独算一个长度

        idx = ord(ch) - ord('a')          # 映射到 0~25
        dp[idx] = max(dp[idx], cur_len)   # 只保留最长的

    # 所有不同子串的数量 = 所有 dp 值的和
    return sum(dp)
```

#### 复杂度  
- **时间复杂度**：`O(n)`  
  - 只遍历一次字符串，每一步做常数时间的计算。  
  - 对比暴力的 `O(n³)`，这里的运行速度提升了 **指数级**，即使 `s` 长度是 10⁵ 也能轻松跑完。  
- **空间复杂度**：`O(1)`（固定的 26 个整数，不随 `n` 增长）。  

---  

## 心得  

- **核心技巧**：**以字符结尾的最长合法子串长度** + **数组（哈希表）统计**。  
- 这种“以结尾为索引” 的思路常用于**计数唯一子串**、**最长递增子序列的变形**等问题。  
- **相似题目**  
  1. *Longest Substring Without Repeating Characters*（统计无重复字符的最长子串）——用滑动窗口记录每个字符的最新位置。  
  2. *Number of Distinct Substrings in a String*（后缀数组或后缀自动机）——统计所有不同子串。  
  3. *Longest Continuous Subarray With Absolute Diff ≤ 1*（连续子数组的限制）——用类似的“当前长度”维护。  

> **一句话总结解题钥匙**：把“所有子串”压缩成“每个字符能作为结尾的最长合法长度”，然后把这些长度相加即可。

---  

## 反思  

- **第一反应**：看到题目立刻想到枚举所有子串，写出能跑通的小程序。  
- **最容易踩的坑**  
  - 忘记环形的特殊相邻关系 `'z' -> 'a'`（差值 -25），导致错误判断。  
  - 只统计最长长度而忘记 **取最大**（`max(dp[idx], cur_len)`），会把较短的重复计入。  
  - 边界条件：字符串长度为 1 时，`cur_len` 必须初始化为 1。  
- **下次类似题**：第一步先思考**是否可以把子串的属性（如是否满足某种连续关系）映射到“以某字符/位置结尾的状态”，如果可以，就尝试用 **DP + 哈希表** 把枚举的指数级复杂度压到线性。