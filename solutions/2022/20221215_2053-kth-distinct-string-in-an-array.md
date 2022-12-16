# #2053. 数组中第 k 个不同的字符串 / Kth Distinct String in an Array

> 难度：简单 · 标签：Array、Hash Table、String、Counting · [LeetCode 链接](https://leetcode.com/problems/kth-distinct-string-in-an-array/)

---

## 题目（英文原版）

**Description**

A distinct string is a string that is present only once in an array.
Given an array of strings arr, and an integer k, return the kth distinct string present in arr. If there are fewer than k distinct strings, return an empty string "".
Note that the strings are considered in the order in which they appear in the array.

**Examples**

**Example 1:**

```
Input: arr = ["d","b","c","b","c","a"], k = 2
Output: "a"
Explanation:
The only distinct strings in arr are "d" and "a".
"d" appears 1st, so it is the 1st distinct string.
"a" appears 2nd, so it is the 2nd distinct string.
Since k == 2, "a" is returned.
```

**Example 2:**

```
Input: arr = ["aaa","aa","a"], k = 1
Output: "aaa"
Explanation:
All strings in arr are distinct, so the 1st string "aaa" is returned.
```

**Example 3:**

```
Input: arr = ["a","b","a"], k = 3
Output: ""
Explanation:
The only distinct string is "b". Since there are fewer than 3 distinct strings, we return an empty string "".
```

**Constraints**

- 1 <= k <= arr.length <= 1000
- 1 <= arr[i].length <= 5
- arr[i] consists of lowercase English letters.

---

## 题目（中文翻译）

**描述**  
不同字符串（distinct string）指的是在数组中仅出现一次的字符串。  
给定字符串数组 `arr` 和整数 `k`，返回 `arr` 中第 `k` 个不同字符串。若不同字符串的数量少于 `k`，返回空字符串 `""`。  
注意，字符串的顺序按照它们在数组中出现的先后顺序来判断。

**示例 1**  
**输入**: `arr = ["d","b","c","b","c","a"], k = 2`  
**输出**: `"a"`  
**解释**:  
数组中唯一的不同字符串是 `"d"` 和 `"a"`。  
`"d"` 第一次出现，因此是第 1 个不同字符串。  
`"a"` 第二次出现，因此是第 2 个不同字符串。  
因为 `k == 2`，返回 `"a"`。

**示例 2**  
**输入**: `arr = ["aaa","aa","a"], k = 1`  
**输出**: `"aaa"`  
**解释**:  
数组中的所有字符串都是不同的，所以第 1 个字符串 `"aaa"` 被返回。

**示例 3**  
**输入**: `arr = ["a","b","a"], k = 3`  
**输出**: `""`  
**解释**:  
唯一的不同字符串是 `"b"`。由于不同字符串的数量少于 3，返回空字符串 `""`。

**约束条件**  
- `1 <= k <= arr.length <= 1000`  
- `1 <= arr[i].length <= 5`  
- `arr[i]` 仅由小写英文字母组成

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每个字符串都逐个检查一遍，看看它在数组里出现了几次**。  
如果只出现一次，就把它加入「候选」列表，最后取第 `k` 个即可。

- **使用的数据结构**：只需要一个普通的列表 `candidates` 来保存符合条件的字符串。  
- **生活化类比**：把数组想象成一本课堂点名册，点名时我们要找出只出现一次的同学名字。我们可以从头到尾一次一次地查看每个名字，在整个名单里数它出现的次数——这就像手里只有一本纸质名单，没法一次性查到全部次数，只能逐行数。

**为什么正确**：  
只要遍历完整个数组，对每个元素都统计它的出现次数，就一定能判断它是否“唯一”。把所有唯一的字符串按原顺序收集起来，第 `k` 个就是答案（如果不足 `k`，返回空串）。

#### 代码（Python）

```python
def kthDistinct_bruteforce(arr, k):
    """
    暴力解法：对每个字符串都遍历一次统计出现次数
    时间复杂度 O(n^2)，空间复杂度 O(1)（不计结果列表）
    """
    n = len(arr)
    distinct = []                     # 用来保存所有唯一字符串，保持原顺序

    for i in range(n):
        cnt = 0                       # 统计 arr[i] 在整个数组中出现的次数
        for j in range(n):
            if arr[j] == arr[i]:
                cnt += 1
        if cnt == 1:                  # 只出现一次的就是“distinct”
            distinct.append(arr[i])

    # 第 k 个（k 从 1 开始计数），如果不存在返回空串
    return distinct[k-1] if k <= len(distinct) else ""
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 这里的 `n` 是数组长度。外层循环 `n` 次，内层循环每次也要遍历 `n` 次，所以总共是 `n × n`。可以把它想象成“每个人都要检查全班同学的名字”，显然会很慢。
- **空间复杂度**：`O(1)`（不计返回的结果列表）  
  - 只用了常数级别的额外变量 `cnt`、`i`、`j`，不随 `n` 增长而增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每次都要遍历整个数组去统计出现次数**，导致 `O(n²)`。  
我们可以把“统计出现次数”这件事一次性完成，然后再一次遍历找第 `k` 个唯一字符串。

**一步步推导**：

1. **第一次遍历**：用一个 **哈希表（字典）** 记录每个字符串出现的次数。  
   - 哈希表类似于 **词典**，键（key）是字符串本身，值（value）是出现次数。查找、插入的时间都非常快，几乎是 `O(1)`。
2. **第二次遍历**：按原顺序再次扫描数组，遇到出现次数为 `1` 的字符串就把它计数。  
   - 当计数等于 `k` 时，直接返回该字符串。若遍历结束仍未找到，则返回空串。

这样只需要 **两次线性遍历**，总时间是 `O(n)`，空间额外使用一个哈希表，空间是 `O(n)`（最坏情况下每个字符串都不同，需要记录 `n` 条记录）。

#### 代码（Python）

```python
def kthDistinct(arr, k):
    """
    最优解：利用哈希表一次统计所有字符串的出现次数
    时间复杂度 O(n)，空间复杂度 O(n)
    """
    # 第一步：统计出现次数
    freq = {}                         # freq[字符串] = 出现次数
    for s in arr:                     # O(n) 次遍历
        freq[s] = freq.get(s, 0) + 1  # get(s,0) 相当于“查字典，若不存在返回 0”

    # 第二步：按原顺序寻找第 k 个只出现一次的字符串
    distinct_cnt = 0                  # 已找到的唯一字符串数量
    for s in arr:                     # 再遍历一次
        if freq[s] == 1:              # 只出现一次的就是 distinct
            distinct_cnt += 1
            if distinct_cnt == k:     # 第 k 个 distinct，直接返回
                return s
    # 没有足够的 distinct，返回空串
    return ""
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 两次线性遍历，每次都只访问数组一次。可以把它想象成“先把全班同学的点名次数记在一本小册子里（一次遍历），再按顺序查找第一次只出现一次的名字”（再一次遍历），总体就是线性时间。
- **空间复杂度**：`O(n)`  
  - 需要一个哈希表来保存每个不同字符串的计数。最坏情况下所有字符串都不相同，需要存 `n` 条记录。

---

## 心得

- **核心技巧**：**哈希表计数**（统计出现次数） + **两遍线性扫描**。  
- **适用的题型**：  
  1. “找数组中出现一次的元素”（如 LeetCode 136. Single Number）  
  2. “统计字符/单词出现频率后筛选”（如 词频前 K 大）  
  3. “判断数组中是否有重复元素”  
- **解题钥匙**：**先把信息一次性收集好（计数），再利用这些信息快速定位答案**。

---

## 反思

- **第一反应**：看到“distinct”，立刻想到要统计出现次数；于是想到用字典（哈希表）来做计数。
- **最容易踩的坑**：  
  - 忘记保持 **原始顺序**：只统计出现次数不代表顺序，必须在第二遍遍历时按原数组顺序检查。  
  - `k` 可能大于实际 distinct 的数量，需要返回空串 `""` 而不是 `None`。  
  - 字符串长度虽小，但仍需把整个字符串作为哈希表的键，避免手动实现比较函数。
- **下次第一步**：**先遍历一次，用哈希表统计每个元素出现的次数**，然后再根据题目要求（顺序、阈值等）进行第二遍扫描。这样可以把大多数“出现次数”相关的问题统一到同一套思路上。