# #1704. 判断字符串两半是否相似 / Determine if String Halves Are Alike

> 难度：简单 · 标签：String、Counting · [LeetCode 链接](https://leetcode.com/problems/determine-if-string-halves-are-alike/)

---

## 题目（英文原版）

**Description**

You are given a string s of even length. Split this string into two halves of equal lengths, and let a be the first half and b be the second half.
Two strings are alike if they have the same number of vowels ('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'). Notice that s contains uppercase and lowercase letters.
Return true if a and b are alike. Otherwise, return false.

**Examples**

**Example 1:**

```
Input: s = "book"
Output: true
Explanation: a = "bo" and b = "ok". a has 1 vowel and b has 1 vowel. Therefore, they are alike.
```

**Example 2:**

```
Input: s = "textbook"
Output: false
Explanation: a = "text" and b = "book". a has 1 vowel whereas b has 2. Therefore, they are not alike.
Notice that the vowel o is counted twice.
```

**Constraints**

- 2 <= s.length <= 1000
- s.length is even.
- s consists of uppercase and lowercase letters.

---

## 题目（中文翻译）

给定一个长度为偶数的字符串 `s`。将该字符串等分为两段长度相等的子串，记前半段为 `a`，后半段为 `b`。  
如果两个字符串中元音字母的数量相同，则称它们**相似**（alike）。元音字母包括 `'a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'`。注意 `s` 可能包含大小写字母。  

返回 `true` 表示 `a` 与 `b` 相似，否则返回 `false`。

## 示例

### 示例 1
**输入**  
```
s = "book"
```
**输出**  
```
true
```
**解释**  
`a = "bo"`，`b = "ok"`。`a` 含有 1 个元音，`b` 也含有 1 个元音。因此它们相似。

### 示例 2
**输入**  
```
s = "textbook"
```
**输出**  
```
false
```
**解释**  
`a = "text"`，`b = "book"`。`a` 含有 1 个元音，而 `b` 含有 2 个元音。因此它们不相似。注意元音 `o` 被计数了两次。

## 约束条件
- `2 <= s.length <= 1000`
- `s.length` 为偶数
- `s` 仅由大小写英文字母组成

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：先把字符串 `s` 按长度均分成左半段 `a` 和右半段 `b`，然后分别统计两个半段里元音字母的个数，最后比较这两个计数是否相等即可。  

- **数据结构**：我们只需要遍历字符，用一个整数变量累计计数。这里可以把“元音字母”想象成字典里的“关键词”，判断一个字符是不是元音，就像在字典里查找某个词是否存在一样。  
- **正确性**：题目要求两段的元音数量相同，只要我们完整、准确地数出每段的元音个数，比较结果自然就能判断是否相等。  
- **复杂度**：  
  - 时间：我们要遍历整个字符串两次（一次遍历左半段，一次遍历右半段），总共看 `n` 个字符，时间复杂度记作 **O(n)**。这里的 `O(n)` 可以理解为“随着字符串长度增长，耗时大概会线性增长”。  
  - 空间：只用了常数个计数器，不会随 `n` 增长，空间复杂度是 **O(1)**（常数级别的内存）。

#### 代码（Python）

```python
def halvesAreAlike(s: str) -> bool:
    # 1. 建立一个集合，存放所有大小写元音，查找速度快（O(1)）
    vowels = set('aeiouAEIOU')

    n = len(s)
    half = n // 2               # 因为长度一定是偶数，正好平分

    # 2. 统计左半段的元音数
    left_cnt = 0
    for ch in s[:half]:         # s[:half] 是左半段的子串
        if ch in vowels:        # 判断是否是元音
            left_cnt += 1

    # 3. 统计右半段的元音数
    right_cnt = 0
    for ch in s[half:]:         # s[half:] 是右半段的子串
        if ch in vowels:
            right_cnt += 1

    # 4. 两段元音数相等则返回 True，否则 False
    return left_cnt == right_cnt
```

#### 复杂度  

- **时间复杂度**：O(n) — 需要遍历全部 `n` 个字符一次（左半段 + 右半段），所以耗时随字符数线性增长。  
- **空间复杂度**：O(1) — 只用了固定大小的集合 `vowels`（大小为 10）和几个计数变量，和 `n` 无关。

---  

### 2. 最优解  

#### 思路  
暴力解已经是 **线性时间、常数空间** 的解法，已经达到了题目的最优复杂度。不过我们可以把「遍历两次」进一步合并成「一次遍历」来写得更简洁——在一次循环中同时统计左半段和右半段的元音数。  

- **瓶颈**：原方法把左、右两段分别遍历，虽然总体仍是 O(n)，但代码里出现了两段相似的循环，阅读时会有重复。  
- **优化**：使用双指针（或单指针配合下标判断）一次遍历整个字符串。左指针从 `0` 开始向右走，右指针从 `n-1` 向左走。每次检查对应的字符是否是元音，分别累计左半段和右半段的计数。遍历结束后比较计数是否相等。  
- **核心概念——双指针**：把字符串想象成一条走廊，左指针从左门进，右指针从右门进，两个指针一起走完整条走廊，既不遗漏也不重复。  

#### 代码（Python）

```python
def halvesAreAlike(s: str) -> bool:
    vowels = set('aeiouAEIOU')
    n = len(s)
    half = n // 2

    left_cnt = right_cnt = 0   # 同时声明两个计数

    # 同时遍历左半段和右半段，只需要一次循环
    for i in range(half):
        # i 是左半段的下标，n-1-i 是右半段的下标
        if s[i] in vowels:          # 检查左半段的字符
            left_cnt += 1
        if s[n - 1 - i] in vowels:  # 检查右半段的字符
            right_cnt += 1

    return left_cnt == right_cnt
```

#### 复杂度  

- **时间复杂度**：O(n) — 只遍历了 `half` 次（实际检查了 `n` 个字符），仍是线性时间，但只用了 **一次** 循环。  
- **空间复杂度**：O(1) — 只用了集合 `vowels`（常数大小）和几个计数变量，和字符串长度无关。

---

## 心得  

- **核心技巧**：统计字符出现次数 → 使用集合快速判断元音 → 双指针一次遍历。  
- **适用题型**：  
  1. “判断字符串前后是否相同/相似” 类题（如 `Valid Palindrome`）。  
  2. “分段统计” 类题（如 `Number of Vowels in Substrings`）。  
  3. “双指针同步遍历” 类题（如 `Array Partition`）。  
- **解题钥匙**：**一次遍历+集合快速查表**。

---

## 反思  

- **第一反应**：把字符串直接切成两半，各自计数——最自然的暴力思路。  
- **最容易踩的坑**：  
  - 忘记大小写元音，需要把 `'A'`、`'E'` 等也算进去。  
  - 边界条件：字符串长度一定是偶数，但仍要确保 `half = len(s)//2` 正确。  
  - 使用 `set` 而不是列表可以把“是否是元音”的判断降到 O(1)。  
- **下次类似题的第一步**：**明确要比较的两个子集合（或子区间）是什么**，然后**想办法在一次遍历中同时收集信息**，避免重复扫描。