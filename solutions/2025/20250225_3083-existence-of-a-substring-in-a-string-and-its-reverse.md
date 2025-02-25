# #3083. 字符串及其反转中子串的存在性 / Existence of a Substring in a String and Its Reverse

> 难度：简单 · 标签：Hash Table、String · [LeetCode 链接](https://leetcode.com/problems/existence-of-a-substring-in-a-string-and-its-reverse/)

---

## 题目（英文原版）

**Description**

Given a string s, find any substring of length 2 which is also present in the reverse of s.
Return true if such a substring exists, and false otherwise.

**Examples**

**Example 1:**

```
Input: s = "leetcode"
Output: true
Explanation: Substring "ee" is of length 2 which is also present in reverse(s) == "edocteel" .
```

**Example 2:**

```
Input: s = "abcba"
Output: true
Explanation: All of the substrings of length 2 "ab" , "bc" , "cb" , "ba" are also present in reverse(s) == "abcba" .
```

**Example 3:**

```
Input: s = "abcd"
Output: false
Explanation: There is no substring of length 2 in s , which is also present in the reverse of s .
```

**Constraints**

- 1 <= s.length <= 100
- s consists only of lowercase English letters.

---

## 题目（中文翻译）

**描述**  
给定一个字符串 `s`，寻找任意长度为 2 的子串（substring），该子串在 `s` 的反转（reverse）中也出现。若存在这样的子串返回 `true`，否则返回 `false`。

**示例 1**  
**输入**: `s = "leetcode"`  
**输出**: `true`  
**解释**: 子串 `"ee"` 长度为 2，且也出现在 `reverse(s) == "edocteel"` 中。

**示例 2**  
**输入**: `s = "abcba"`  
**输出**: `true`  
**解释**: 所有长度为 2 的子串 `"ab"、"bc"、"cb"、"ba"` 均出现在 `reverse(s) == "abcba"` 中。

**示例 3**  
**输入**: `s = "abcd"`  
**输出**: `false`  
**解释**: 在 `s` 中不存在任何长度为 2 的子串同时出现在 `s` 的反转中。

**约束条件**  
- `1 <= s.length <= 100`  
- `s` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把题目翻译成「把原字符串 `s` 反转得到 `t`，在 `s` 的所有长度为 2 的子串里找一找，哪一个也出现在 `t` 中」。  
实现步骤如下：

1. 用 Python 的切片 `s[::-1]` 生成反转字符串 `t`。这一步像在字典里查到「把整本书倒着读」的版本，`t[i]` 就是原来 `s` 最后第 `i+1` 个字符。  
2. 枚举 `s` 中所有长度为 2 的子串 `s[i:i+2]`（`i` 从 `0` 到 `len(s)-2`）。这相当于把「每两个相邻的字母」一个一个拿出来检查。  
3. 对每个子串，使用 Python 的 `in` 操作判断它是否是 `t` 的子串（即 `sub in t`）。如果找到了，就返回 `True`；遍历完都没有找到则返回 `False`。  

为什么会对？因为我们把「在原串里」和「在反转串里」这两个条件都逐一检查了，只要有一次同时满足，就说明答案是 `True`。

#### 代码（Python）

```python
def check_substring_bruteforce(s: str) -> bool:
    # 1. 先把 s 反转，得到 t
    t = s[::-1]                     # 例如 "leetcode" -> "edocteel"

    # 2. 枚举所有长度为 2 的子串
    n = len(s)
    for i in range(n - 1):          # i 最多到 n-2，保证 i+1 仍在范围内
        sub = s[i:i + 2]            # 取出相邻的两个字符，例如 "le"
        # 3. 检查 sub 是否出现在反转串 t 中
        if sub in t:                # Python 的子串判断，底层也是一次遍历比较
            return True

    # 没有任何子串满足条件
    return False
```

#### 复杂度

- **时间复杂度：** `O(n²)`  
  - 外层遍历 `n-1` 次，每一次 `sub in t` 最坏要扫描整个 `t`（长度 `n`），所以大约是 `n × n` 次比较。  
  - 用大白话说，就是「如果字符串有 100 个字符，最多要比较 10,000 次」。
- **空间复杂度：** `O(n)`  
  - 需要额外存放反转后的字符串 `t`，长度和原字符串相同。其它变量都是常数级别。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在第 3 步：每检查一个子串都要在整条反转串里找一次，导致 **二次遍历**。  
我们可以把“在反转串里找”这件事 **提前** 用一个哈希表（在 Python 里用 `set`）记下来，这样查询就可以做到 **常数时间**。

观察一下题目要求的等价条件：

- 子串 `s[i]s[i+1]` 出现在反转串 `t` 中  
  ↔ 在原串里出现 **相反顺序** 的子串 `s[i+1]s[i]`（因为 `t` 的每两个相邻字符正好是原串中相邻字符的倒序）。

因此，只要在遍历原串的过程中，看到一个长度为 2 的子串 `ab`，检查 **它的逆序 `ba`** 是否已经出现过即可。  
还有一种特殊情况：如果子串本身是回文（两个字符相同，如 `"aa"`），它的逆序和自己一样，只要出现一次就已经满足条件。

实现步骤：

1. 初始化一个空集合 `seen` 用来保存已经遍历过的子串（长度为 2）。集合的查询 `x in seen` 是 **O(1)**，类似于在字典里快速查找页码。  
2. 从左到右扫描 `s`，每次取当前的子串 `cur = s[i:i+2]`（`i` 从 `0` 到 `n-2`）。  
3. 检查 `cur[::-1]`（逆序子串）是否已经在 `seen` 中：  
   - 如果在，说明之前出现过它的逆序，直接返回 `True`。  
   - 否则，把 `cur` 加入 `seen`，继续往后走。  
4. 循环结束仍未找到，返回 `False`。

这样我们只遍历一次字符串，且每一步的查询/插入都是常数时间，整体是 **线性时间**。

#### 代码（Python）

```python
def check_substring_optimal(s: str) -> bool:
    seen = set()                     # 用来存放已经看到的长度为 2 的子串
    n = len(s)

    for i in range(n - 1):
        cur = s[i:i + 2]             # 当前子串，例如 "ab"
        rev = cur[::-1]              # 逆序子串，例如 "ba"

        # 如果逆序子串已经出现过，说明条件成立
        if rev in seen:
            return True

        # 否则把当前子串放进集合，供后面的子串去比较
        seen.add(cur)

    # 遍历完都没有匹配成功
    return False
```

#### 复杂度

- **时间复杂度：** `O(n)`  
  - 只遍历一次字符串，集合的查询/插入都是常数时间。  
  - 用大白话说，「如果有 100 个字符，只需要检查 99 次」。
- **空间复杂度：** `O(n)`  
  - 最坏情况下需要把所有长度为 2 的子串都存进集合，数量约为 `n-1`，即线性空间。

---

## 心得

- **核心技巧**：利用 **哈希表（集合）** 把“是否出现过”这类判断降到 `O(1)`，从而把原本的二次遍历压缩成一次遍历。  
- **适用的题型**  
  1. 判断两个数组/字符串是否有公共子序列（长度固定）  
  2. “找出是否存在两个数之和为目标值” → 使用哈希表存已遍历的数  
  3. “是否存在相同的字符对” → 类似的 “出现过的子串/字符对” 检查  

> **解题钥匙**：把“在另一条序列里找”转化为“在已遍历的集合里查”，利用集合的 O(1) 查询。

---

## 反思

- **第一反应**：直接把题目描述成「在原串和反转串里找公共子串」，于是想到暴力枚举。  
- **最容易踩的坑**  
  - 忘记考虑子串本身是回文（如 `"aa"`），导致误判。  
  - 边界条件：字符串长度小于 2 时没有长度为 2 的子串，直接返回 `False`。  
- **下次类似题的第一步**：先问自己「能否把‘在另一段数据里找’转化为‘在已经看到的东西里查’」；如果能，就立刻考虑哈希表/集合来实现 O(1) 查询。