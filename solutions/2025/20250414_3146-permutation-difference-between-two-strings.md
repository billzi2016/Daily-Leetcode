# #3146. 两字符串的排列差 / Permutation Difference between Two Strings

> 难度：简单 · 标签：Hash Table、String · [LeetCode 链接](https://leetcode.com/problems/permutation-difference-between-two-strings/)

---

## 题目（英文原版）

**Description**

You are given two strings s and t such that every character occurs at most once in s and t is a permutation of s.
The permutation difference between s and t is defined as the sum of the absolute difference between the index of the occurrence of each character in s and the index of the occurrence of the same character in t.
Return the permutation difference between s and t.

**Examples**

**Example 1:**

```
Input: s = "abc", t = "bac"
Output: 2
Explanation:
For s = "abc" and t = "bac" , the permutation difference of s and t is equal to the sum of:
That is, the permutation difference between s and t is equal to |0 - 1| + |1 - 0| + |2 - 2| = 2 .
```

**Example 2:**

```
Input: s = "abcde", t = "edbac"
Output: 12
Explanation: The permutation difference between s and t is equal to |0 - 3| + |1 - 2| + |2 - 4| + |3 - 1| + |4 - 0| = 12 .
```

**Constraints**

- 1 <= s.length <= 26
- Each character occurs at most once in s.
- t is a permutation of s.
- s consists only of lowercase English letters.

---

## 题目（中文翻译）

你得到两个字符串 `s` 和 `t`，其中 `s` 中的每个字符至多出现一次，且 `t` 是 `s` 的一个排列（permutation）。  
**排列差**（permutation difference）定义为：对每个字符，计算其在 `s` 中出现的下标与在 `t` 中出现的下标之间的绝对差（absolute difference），然后将所有这些差值求和。  
返回 `s` 与 `t` 之间的排列差。

示例 1  
输入: `s = "abc", t = "bac"`  
输出: `2`  
解释:  
对于 `s = "abc"` 与 `t = "bac"`，排列差等于  
\|0 - 1\| + \|1 - 0\| + \|2 - 2\| = 2  

示例 2  
输入: `s = "abcde", t = "edbac"`  
输出: `12`  
解释:  
排列差等于 \|0 - 3\| + \|1 - 2\| + \|2 - 4\| + \|3 - 1\| + \|4 - 0\| = 12  

**约束条件**  
- 1 ≤ `s.length` ≤ 26  
- `s` 中的每个字符至多出现一次  
- `t` 是 `s` 的一个排列（permutation）  
- `s` 只包含小写英文字母

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：对每个字符 `c`，在 `s` 中把它的下标记下来，再在 `t` 中把它的下标记下来，最后把两者的绝对差累加。  
因为 **每个字符在两串里都只出现一次**，我们只需要一次遍历就能得到下标。  

可以把“下标”想象成一本书的页码，字符 `c` 就是词条，找词条在 `s` 和 `t` 两本书里的页码，然后算页码差的绝对值，最后把所有词条的差值相加。

实现上，最笨的办法是：  
1. 对 `s` 的每个字符 `c`，在 `t` 中遍历寻找 `c` 的位置（这一步是 O(n)）。  
2. 把两边的下标相减取绝对值，加到答案里。  

因为我们对 `s` 中的每个字符都要在 `t` 中全遍历一次，时间复杂度是 **O(n²)**（n 是字符串长度）。  
空间上只用了常数级别的变量，**O(1)**。

#### 代码（Python）

```python
def permutationDifference_bruteforce(s: str, t: str) -> int:
    """
    暴力实现：对 s 中的每个字符，在 t 中线性搜索它的位置
    """
    total = 0                         # 用来累计答案
    n = len(s)

    for i in range(n):                # i 是字符在 s 中的下标
        ch = s[i]                     # 当前字符
        # 在 t 中寻找相同字符的下标（线性搜索）
        j = 0
        while j < n and t[j] != ch:   # 找不到就继续往后走
            j += 1
        # 此时 j 必然是字符在 t 中的下标（题目保证 t 是 s 的全排列）
        total += abs(i - j)           # 累加绝对差

    return total
```

#### 复杂度

- **时间复杂度：O(n²)**  
  这里的 `n²` 可以想象成「每个人都要和每个人握手」的情形。因为我们对 `s` 中的每个字符，都要在 `t` 中遍历一次。

- **空间复杂度：O(1)**  
  只用了几个整数变量，和输入大小无关，算作常数空间。

---

### 2. 最优解

#### 思路  

暴力解慢的地方在于 **在 `t` 中找字符的位置用了线性搜索**。  
我们可以把「在 `t` 中找字符的位置」这一步提前做好：先遍历一次 `t`，把每个字符所在的下标记录下来。  
这正好可以用 **哈希表（Python 中的 dict）** 来实现：

- 把 `t` 看成一本字典，**键（key）** 是字符，**值（value）** 是它在 `t` 中的下标。  
- 建好这张「字符 → 下标」的映射后，再遍历 `s`，直接用 `dict[字符]` 把对应的下标拿出来，时间是 O(1)。  

整个过程只需要 **两次线性遍历**，时间降到 **O(n)**，空间使用一个长度为 `n` 的字典，**O(n)**。

#### 代码（Python）

```python
def permutationDifference_optimal(s: str, t: str) -> int:
    """
    最优实现：先用哈希表把 t 中每个字符的下标记下来，再遍历 s 直接查询
    """
    # 第一步：构建字符 → 下标 的映射（相当于把 t 当成一本“查字典”）
    pos_in_t = {ch: idx for idx, ch in enumerate(t)}   # O(n) 时间，O(n) 空间

    total = 0
    # 第二步：遍历 s，直接在哈希表里查对应字符在 t 中的下标
    for idx_s, ch in enumerate(s):                     # O(n) 时间
        idx_t = pos_in_t[ch]                           # O(1) 查询
        total += abs(idx_s - idx_t)                    # 累加绝对差

    return total
```

#### 复杂度

- **时间复杂度：O(n)**  
  只做了两次线性遍历，想象成「所有人排队一次」的情形。相比暴力的「每个人都要和每个人握手」快了很多。

- **空间复杂度：O(n)**  
  用了一个字典保存 `t` 中每个字符的下标，大小正好是字符串长度 `n`。在本题中 `n ≤ 26`，几乎可以忽略不计。

---

## 心得

- **核心技巧**：利用哈希表把「在另一串中查找位置」的 O(n) 操作降到 O(1)。  
- **适用场景**：  
  1. 两个数组（或字符串）中相同元素位置的比较，如「最小交换次数」问题。  
  2. 需要快速定位元素位置的题目，例如「字符位置映射」或「数组重排后求差」。  
- **一句话总结**：把“查找”提前，用字典一次搞定，后面直接 O(1) 读取。

## 反思

- **第一反应**：看到「每个字符只出现一次」和「t 是 s 的全排列」就想到可以用「位置映射」来直接比较。  
- **最容易踩的坑**：  
  - 忘记把 `t` 的下标先保存，导致仍然在循环里做线性搜索。  
  - 对空字符串或长度不匹配的情况没有防御（本题已保证合法）。  
- **下次类似题的第一步**：先思考「是否可以把需要频繁查询的信息提前预处理（哈希表、数组等）」，把查询成本从 O(n) 降到 O(1)。