# #1358. 包含全部三种字符的子串个数 / Number of Substrings Containing All Three Characters

> 难度：中等 · 标签：Hash Table、String、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/number-of-substrings-containing-all-three-characters/)

---

## 题目（英文原版）

**Description**

Given a string s consisting only of characters a, b and c.
Return the number of substrings containing at least one occurrence of all these characters a, b and c.

**Examples**

**Example 1:**

```
Input: s = "abcabc"
Output: 10
Explanation: The substrings containing at least one occurrence of the characters a, b and c are "abc", "abca", "abcab", "abcabc", "bca", "bcab", "bcabc", "cab", "cabc" and "abc" (again).
```

**Example 2:**

```
Input: s = "aaacb"
Output: 3
Explanation: The substrings containing at least one occurrence of the characters a, b and c are "aaacb", "aacb" and "acb".
```

**Example 3:**

```
Input: s = "abc"
Output: 1
```

**Constraints**

- 3 <= s.length <= 5 x 10^4
- s only consists of a, b or c characters.

---

## 题目（中文翻译）

给定一个仅由字符 `a`、`b`、`c` 组成的字符串 `s`。返回包含至少一次字符 `a`、`b`、`c` 三者的子串（substring）个数。

## 示例

### 示例 1
**输入**  
``` 
s = "abcabc"
```  
**输出**  
```
10
```  
**解释**  
包含至少一次字符 `a`、`b`、`c` 的子串有 `"abc"`、`"abca"`、`"abcab"`、`"abcabc"`、`"bca"`、`"bcab"`、`"bcabc"`、`"cab"`、`"cabc"` 以及再次出现的 `"abc"`，共计 10 个。

### 示例 2
**输入**  
``` 
s = "aaacb"
```  
**输出**  
```
3
```  
**解释**  
包含至少一次字符 `a`、`b`、`c` 的子串有 `"aaacb"`、`"aacb"` 和 `"acb"`，共计 3 个。

### 示例 3
**输入**  
``` 
s = "abc"
```  
**输出**  
```
1
```  

## 约束条件
- `3 <= s.length <= 5 × 10^4`
- `s` 仅由字符 `a`、`b`、`c` 组成。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**枚举所有子串**，然后检查它是否同时包含字符 `a、b、c`。  
- 子串可以用两个指针 `i`（左边界）和 `j`（右边界）来表示，`i ≤ j`。  
- 检查子串是否满足条件时，只需要遍历一次子串，统计出现的 `a、b、c` 是否都有。  
- 这里用到的唯一数据结构是**计数器**（比如字典），它像一本字典：把字符当成“单词”，把出现次数当成“页码”。  

这种方法一定能得到正确答案，因为我们把所有可能的子串都检查了一遍，只要有满足条件的，就会被计数。  

#### 代码（Python）  

```python
def number_of_substrings_bruteforce(s: str) -> int:
    n = len(s)
    ans = 0

    # i 为子串左端点，j 为右端点（包含）
    for i in range(n):
        cnt = {'a': 0, 'b': 0, 'c': 0}   # 记录当前子串里 a,b,c 的出现次数
        for j in range(i, n):
            cnt[s[j]] += 1               # 把新加入的字符计数加一
            # 只要三个字符的计数都大于 0，就满足题意
            if cnt['a'] > 0 and cnt['b'] > 0 and cnt['c'] > 0:
                ans += 1                 # 统计一个合法子串
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)`。  
  - 外层循环 `i` 走 `n` 步，内层循环 `j` 最多也走 `n` 步，所以最坏情况大约是 `n × n` 次操作。  
  - 用大白话说，就是如果字符串长度是 10,000，算法要做大约 100,000,000 次检查，明显会很慢。  

- **空间复杂度**：`O(1)`。  
  - 只用了一个固定大小的字典来计数，和输入长度无关，所需额外空间可以视为常数。  



---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**重复遍历同一个字符**：当左指针 `i` 向右移动时，右指针 `j` 仍然要从 `i` 开始重新扫描，这导致大量冗余计算。  

我们可以把**滑动窗口**的思想引入进来：  
- 用两个指针 `left`、`right` 维护一个**窗口** `s[left : right+1]`，保证窗口里始终**包含所有三种字符**。  
- 当窗口已经满足条件时，**所有以 `left` 为左端点、右端点 ≥ `right` 的子串**都必然满足要求，因为往右扩展只会让字符种类更多。  
- 因此，对于固定的 `left`，只要找到最左侧的满足条件的 `right`，合法子串的数量就是 `len(s) - right`（从 `right` 到字符串末尾都可以作为右端点）。  

实现细节：  
1. 用一个哈希表 `freq`（字典）记录窗口中每个字符的出现次数。  
2. 不断移动右指针 `right`，把字符加入窗口并更新计数。  
3. 当 `freq` 中 `a、b、c` 的计数都 ≥ 1 时，说明窗口已经合法。此时把 `len(s) - right` 加到答案中。  
4. 然后收缩左指针 `left`，把左端字符计数减一，继续检查是否仍然合法。若仍合法，继续累加答案；若不合法，停止收缩，继续移动右指针。  

这样每个字符最多被左指针和右指针各访问一次，整体线性时间。  

#### 代码（Python）  

```python
def number_of_substrings(s: str) -> int:
    n = len(s)
    freq = {'a': 0, 'b': 0, 'c': 0}   # 窗口中字符出现次数
    left = 0
    ans = 0

    # right 逐个遍历字符串
    for right in range(n):
        freq[s[right]] += 1          # 把右端字符加入窗口

        # 当窗口已经包含 a、b、c 时，开始收缩左端
        while freq['a'] > 0 and freq['b'] > 0 and freq['c'] > 0:
            # 此时以 left 为左端，right 为最左满足条件的右端
            # 所有更右的右端 (right, right+1, …, n-1) 都合法
            ans += n - right

            # 收缩窗口：左指针左移一格，去掉 left 位置的字符
            freq[s[left]] -= 1
            left += 1

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n)`。  
  - `right` 只会向右走一次，`left` 也只会向右走最多 `n` 步。两个指针的总移动次数不超过 `2n`，所以整体是线性时间。  
  - 与暴力 `O(n²)` 相比，效率提升了数量级：即使 `n = 5×10⁴`，也只需要大约 `1e5` 次操作，轻松跑完。  

- **空间复杂度**：`O(1)`。  
  - 只用了固定大小的字典 `freq`，与字符串长度无关，属于常数级别的额外空间。  



## 心得  

- **核心技巧**：**滑动窗口 + 前缀计数**。通过维持一个满足条件的最小窗口，能够一次性统计所有以该左端点为起点的合法子串。  
- **适用的题型**：  
  1. “包含所有字符的最小子串”类（LeetCode 76 Minimum Window Substring）。  
  2. “子数组/子串满足某种计数条件”类（如统计子数组和≥K 的个数）。  
- **一句话总结解题钥匙**：**找到每个左端点对应的最左合法右端点，用 `n - right` 直接算出该左端点贡献的子串数**。  



## 反思  

- **第一反应**：看到“所有三种字符都出现”自然想到枚举子串检查，直觉是暴力遍历。  
- **最容易踩的坑**：  
  - 忘记在左指针收缩时更新计数，导致窗口仍被误认为合法。  
  - 边界条件：当字符串本身就不含全部三种字符时，答案应为 0，需要保证循环不会误加。  
- **下次遇到同类题**：第一步先思考**“对于固定的左端点，最早出现的满足条件的右端点是多少？”**，再用滑动窗口把这个过程线性化。