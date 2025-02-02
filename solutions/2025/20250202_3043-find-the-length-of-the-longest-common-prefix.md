# #3043. 寻找最长公共前缀的长度 / Find the Length of the Longest Common Prefix

> 难度：中等 · 标签：Array、Hash Table、String、Trie · [LeetCode 链接](https://leetcode.com/problems/find-the-length-of-the-longest-common-prefix/)

---

## 题目（英文原版）

**Description**

You are given two arrays with positive integers arr1 and arr2.
A prefix of a positive integer is an integer formed by one or more of its digits, starting from its leftmost digit. For example, 123 is a prefix of the integer 12345, while 234 is not.
A common prefix of two integers a and b is an integer c, such that c is a prefix of both a and b. For example, 5655359 and 56554 have common prefixes 565 and 5655 while 1223 and 43456 do not have a common prefix.
You need to find the length of the longest common prefix between all pairs of integers (x, y) such that x belongs to arr1 and y belongs to arr2.
Return the length of the longest common prefix among all pairs. If no common prefix exists among them, return 0.

**Examples**

**Example 1:**

```
Input: arr1 = [1,10,100], arr2 = [1000]
Output: 3
Explanation: There are 3 pairs (arr1[i], arr2[j]):
- The longest common prefix of (1, 1000) is 1.
- The longest common prefix of (10, 1000) is 10.
- The longest common prefix of (100, 1000) is 100.
The longest common prefix is 100 with a length of 3.
```

**Example 2:**

```
Input: arr1 = [1,2,3], arr2 = [4,4,4]
Output: 0
Explanation: There exists no common prefix for any pair (arr1[i], arr2[j]), hence we return 0.
Note that common prefixes between elements of the same array do not count.
```

**Constraints**

- 1 <= arr1.length, arr2.length <= 5 * 104
- 1 <= arr1[i], arr2[i] <= 108

---

## 题目（中文翻译）

给定两个正整数（positive integer）数组 `arr1` 和 `arr2`。  

正整数的 **前缀（prefix）** 是由其左侧一个或多个连续数字组成的整数。例如，`123` 是整数 `12345` 的前缀，而 `234` 不是。  

两个整数 `a` 与 `b` 的 **公共前缀（common prefix）** 是一个整数 `c`，使得 `c` 同时是 `a` 和 `b` 的前缀。例如，`5655359` 与 `56554` 的公共前缀有 `565` 和 `5655`，而 `1223` 与 `43456` 没有公共前缀。  

请在所有满足 `x ∈ arr1`、`y ∈ arr2` 的整数对 `(x, y)` 中，找到 **最长公共前缀（longest common prefix）** 的长度。返回所有对中最长公共前缀的长度；如果不存在任何公共前缀，则返回 `0`。  

> **注意**：同一数组内部元素之间的公共前缀不计入考察范围。

## 示例

### 示例 1
**输入**  
`arr1 = [1,10,100]`  
`arr2 = [1000]`

**输出**  
`3`

**解释**  
共有 3 对 `(arr1[i], arr2[j])`：
- `(1, 1000)` 的最长公共前缀是 `1`，长度为 1。  
- `(10, 1000)` 的最长公共前缀是 `10`，长度为 2。  
- `(100, 1000)` 的最长公共前缀是 `100`，长度为 3。  

最长的公共前缀是 `100`，其长度为 **3**。

### 示例 2
**输入**  
`arr1 = [1,2,3]`  
`arr2 = [4,4,4]`

**输出**  
`0`

**解释**  
任意 `(arr1[i], arr2[j])` 均不存在公共前缀，故返回 `0`。  

> 同一数组内部元素之间的公共前缀不计入本题。

## 约束条件
- `1 <= arr1.length, arr2.length <= 5 * 10^4`
- `1 <= arr1[i], arr2[i] <= 10^8`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **每一个** `arr1` 的元素和 **每一个** `arr2` 的元素配对，求出它们的公共前缀长度，最后取最大值。

- **配对**：把两个数组的下标分别遍历一遍，形成所有可能的 `(x, y)` 对。
- **求公共前缀**：把整数转成字符串（把数字想成“一串字母”），从左往右比较字符，遇到不同的字符就停下来，比较的字符数就是前缀长度。  
  > 把哈希表比作字典，字符串就像一本书的文字，逐字比对就像在找相同的开头句子。

只要遍历完所有配对，就一定能得到答案，因为我们穷举了所有可能。

#### 代码（Python）

```python
def longest_common_prefix_bruteforce(arr1, arr2):
    """
    暴力解：两层循环枚举所有配对，逐字符比较前缀。
    """
    max_len = 0                     # 记录目前找到的最长前缀长度
    for a in arr1:                  # 外层遍历 arr1
        sa = str(a)                 # 把整数转换成字符串，方便逐字符比较
        for b in arr2:              # 内层遍历 arr2
            sb = str(b)
            # 同时遍历两串的字符，直到有一个串结束或字符不相等
            i = 0
            while i < len(sa) and i < len(sb) and sa[i] == sb[i]:
                i += 1
            # i 此时就是当前配对的公共前缀长度
            if i > max_len:
                max_len = i
    return max_len
```

#### 复杂度  

- **时间复杂度**：`O(|arr1| * |arr2| * L)`  
  - `|arr1| * |arr2|` 是配对的总数（最坏情况 5·10⁴ × 5·10⁴），  
  - `L` 是两数最长的位数，最多 9（因为 1 ≤ 数 ≤ 10⁸）。  
  - 用大白话说，就是“把每一对都检查一遍，检查的工作量跟数字的位数成正比”。  
- **空间复杂度**：`O(1)`（只用了常数个临时变量），不随输入规模增长。

> 这种解法在数据规模很小的时候还能接受，但一旦数组长度达到上限，就会因为配对数量太大而超时。

---

### 2. 最优解

#### 思路  

从暴力解可以看出 **瓶颈** 在于「两层循环」——我们不需要真的把所有配对都枚举，只要知道 **是否存在** 某个前缀在两个数组中都出现过，就能得到答案。

**关键观察**：

- 任意整数的所有前缀只有 `len(num)` 种（最多 9 种），例如 `1234` 的前缀是 `1、12、123、1234`。
- 如果把 **`arr1` 中出现的所有前缀** 放进一个集合（HashSet），以后想判断某个前缀是否在 `arr1` 中出现，只要查询集合即可，时间是 **O(1)**。

基于上述观察，解题步骤如下：

1. **遍历 `arr1`**，把每个数的所有前缀插入哈希集合 `prefix_set`。  
   - 把整数不断除以 10（相当于“去掉最右边一位”），每一步得到的值就是一个前缀。  
   - 这一步的时间是 `O(|arr1| * D)`，`D` 为最大位数（≤9），几乎可以忽略不计。

2. **遍历 `arr2`**，同样生成它的前缀。  
   - 对每个前缀，从 **最长** 开始检查（先检查完整数字，再除以 10），只要在 `prefix_set` 中找到了，就说明这条前缀在两个数组里都出现过，更新答案并**直接跳到下一个 `arr2` 元素**（因为已经找到了该元素能得到的最长前缀）。  
   - 这样每个 `arr2` 元素最多检查 `D` 次。

3. 最终返回记录的最大前缀长度即可。

> **类比**：把 `arr1` 的所有前缀想成“一本图书馆的目录”，我们先把目录全部写进一本小册子（HashSet）。随后去另一本图书馆（`arr2`）寻找书名的前缀，只要在小册子里能查到，就说明两馆都有这本书的相同开头。

#### 代码（Python）

```python
def longest_common_prefix_opt(arr1, arr2):
    """
    最优解：利用 HashSet 存储 arr1 所有前缀，随后遍历 arr2 检查最长匹配前缀。
    """
    # 1️⃣ 把 arr1 的所有前缀放进集合
    prefix_set = set()                     # 哈希集合，相当于“字典”
    for num in arr1:
        x = num
        while x > 0:                       # 不断去掉最右边一位，得到所有前缀
            prefix_set.add(x)              # 把当前前缀加入集合
            x //= 10                       # 整除 10，相当于删除最右边一位

    # 2️⃣ 在 arr2 中寻找最长的公共前缀
    max_len = 0
    for num in arr2:
        x = num
        # 从完整数字开始向短的前缀检查，一旦找到就在此元素上结束
        while x > 0:
            if x in prefix_set:            # O(1) 哈希查询
                # 前缀长度 = 该整数的位数 = log10(x) + 1，直接用字符串长度更直观
                cur_len = len(str(x))
                if cur_len > max_len:
                    max_len = cur_len
                break                      # 已经是该 arr2 元素能得到的最长前缀
            x //= 10                       # 继续检查更短的前缀
    return max_len
```

#### 复杂度  

- **时间复杂度**：`O((|arr1| + |arr2|) * D)`  
  - `D ≤ 9`（整数最大位数），所以实际运行时间约等于 `O(|arr1| + |arr2|)`。  
  - 与暴力解的 `O(|arr1| * |arr2| * D)` 相比，**把平方级别降到了线性级别**，在 5·10⁴ 规模的数据下毫无压力。

- **空间复杂度**：`O(|arr1| * D)`  
  - 最坏情况下每个 `arr1` 的数都会产生 `D` 条不同前缀，存入集合。  
  - 由于 `D` 很小（≤9），空间大约是 `9 * 5·10⁴ ≈ 4.5×10⁵` 个整数，完全可以接受。

---

## 心得

- **核心技巧**：利用 **哈希集合（HashSet）存储所有前缀**，把“是否出现过”的判断从 **O(n)** 降到 **O(1)**。
- **适用场景**：  
  1. “找两个集合中公共的子串/子序列/前缀”等**集合交集**类问题。  
  2. “判断某个属性是否在已有集合中出现过”，如 “单词是否在词典里”。  
  3. “最长公共前缀/后缀”等需要**快速查重**的字符串/数字题目（如 LeetCode 14、720）。
- **一句话总结**：把所有可能的前缀先装进“字典”，再去另一边快速查找——**先收集、后查询**。

---

## 反思

- **第一反应**：直接两层循环枚举配对，逐字符比较。对初学者来说最自然，却忽略了规模限制。
- **最容易踩的坑**：  
  - 忘记把整数的前缀都加入集合，导致漏掉短前缀。  
  - 对 `0` 的处理：题目保证正整数，所以不必担心 `0` 的前缀。  
  - 在遍历 `arr2` 时如果从短前缀开始检查，可能会错过更长的匹配，必须**从长到短**检查。
- **下次遇到类似题**：第一步先问自己“能否把一侧的所有可能答案预处理成集合或哈希表”，如果答案是“可以”，那么后面的查询几乎都是 **O(1)**，问题往往能从 **暴力** 直接跃升到 **线性**。