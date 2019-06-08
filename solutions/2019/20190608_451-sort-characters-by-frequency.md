# #451. **按字符出现频率排序** / Sort Characters By Frequency

> 难度：中等 · 标签：Hash Table、String、Sorting、Heap (Priority Queue)、Bucket Sort、Counting · [LeetCode 链接](https://leetcode.com/problems/sort-characters-by-frequency/)

---

## 题目（英文原版）

**Description**

Given a string s, sort it in decreasing order based on the frequency of the characters. The frequency of a character is the number of times it appears in the string.
Return the sorted string. If there are multiple answers, return any of them.

**Examples**

**Example 1:**

```
Input: s = "tree"
Output: "eert"
Explanation: 'e' appears twice while 'r' and 't' both appear once.
So 'e' must appear before both 'r' and 't'. Therefore "eetr" is also a valid answer.
```

**Example 2:**

```
Input: s = "cccaaa"
Output: "aaaccc"
Explanation: Both 'c' and 'a' appear three times, so both "cccaaa" and "aaaccc" are valid answers.
Note that "cacaca" is incorrect, as the same characters must be together.
```

**Example 3:**

```
Input: s = "Aabb"
Output: "bbAa"
Explanation: "bbaA" is also a valid answer, but "Aabb" is incorrect.
Note that 'A' and 'a' are treated as two different characters.
```

**Constraints**

- 1 <= s.length <= 5 * 105
- s consists of uppercase and lowercase English letters and digits.

---

## 题目（中文翻译）

给定一个字符串 `s`，请根据字符出现的频率（frequency）对其进行降序排序。字符的频率指该字符在字符串中出现的次数。  
返回排序后的字符串。如果存在多个答案，返回任意一个即可。

**示例 1**  
**示例 2**  
**示例 3**  

**约束条件**

- `1 <= s.length <= 5 * 10^5`
- `s` 仅由大小写英文字母和数字组成。

**示例**

**示例 1**  
输入: `s = "tree"`  
输出: `"eert"`  
解释: `'e'` 出现了两次，而 `'r'` 和 `'t'` 各出现一次。因此 `'e'` 必须出现在 `'r'` 和 `'t'` 前面。`"eetr"` 也是一个有效答案。

**示例 2**  
输入: `s = "cccaaa"`  
输出: `"aaaccc"`  
解释: `'c'` 与 `'a'` 都出现了三次，所以 `"cccaaa"` 与 `"aaaccc"` 均为有效答案。需注意 `"cacaca"` 不符合要求，因为相同的字符必须相邻。

**示例 3**  
输入: `s = "Aabb"`  
输出: `"bbAa"`  
解释: `"bbaA"` 也是一个有效答案，但 `"Aabb"` 是错误的。需要注意大写字母 `'A'` 与小写字母 `'a'` 被视为不同的字符。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：

1. **统计每个字符出现的次数**。可以用 Python 的 `dict`（哈希表）来记录，键是字符，值是出现次数。哈希表就像一本字典，看到一个单词（字符）就能立刻查到它对应的页码（出现次数），查找时间非常快。  
2. **把所有字符按照出现次数从大到小排序**。把哈希表的 `items()`（键值对）取出来，交给 `sorted()`，并指定排序键为出现次数，倒序排列。  
3. **根据排好的顺序重新拼接字符串**。遍历排好序的 `(char, freq)`，把字符 `char` 重复 `freq` 次加入结果。

为什么正确？因为我们先把每个字符出现的次数完整记录下来，然后把字符按次数从高到低排好序，最后把字符按排好顺序一次性输出，就一定满足“出现次数多的字符在前”。  

**复杂度分析（大白话）**  
- 统计出现次数要遍历一遍字符串，长度记为 `n`，相当于走了 `n` 步。  
- 把哈希表的键值对排序，假设不同字符的种类数为 `m`（最多 62，26 大写+26 小写+10 数字），排序的时间大约是 `m log m`。因为 `m` 最多只有几百，这一步在实际数据里几乎可以忽略。  
- 最后拼接结果同样要走 `n` 步。

所以整体时间复杂度是 **O(n log m)**，在最坏情况下 `m≈n`（所有字符都不相同），就会退化为 **O(n log n)**。空间上我们用了一个哈希表存 `m` 条记录，还要一个额外的结果字符串，都是 **O(n)**（因为最终结果长度等于原字符串）。

#### 代码（Python）

```python
def frequency_sort_brute(s: str) -> str:
    # 1. 统计字符出现次数，使用字典（哈希表）
    freq = {}
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1   # get() 相当于查字典，找不到返回默认值 0

    # 2. 把 (字符, 次数) 按次数降序排好
    # sorted() 会返回一个新的列表，key 参数指定按次数排序，reverse=True 表示降序
    sorted_items = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    # 3. 根据排好的顺序拼接结果
    res = []
    for ch, cnt in sorted_items:
        res.append(ch * cnt)   # 把字符重复 cnt 次加入列表

    return ''.join(res)        # 把列表合并成最终字符串
```

#### 复杂度

- **时间复杂度**：`O(n log m)`，在最坏情况下 `m≈n`，即 `O(n log n)`。  
  *解释*：遍历字符串是线性 `n`，排序 `m` 条记录是 `m log m`，两者相加就是 `O(n log n)`（因为 `m≤n`）。  
- **空间复杂度**：`O(n)`。  
  *解释*：哈希表最多存 `m` 条记录，`m≤n`；结果字符串长度就是 `n`，因此总体是线性空间。

---  

### 2. 最优解

#### 思路  
暴力解的瓶颈在 **排序** 步骤。虽然字符种类 `m` 很小，但在最坏情况下 `m` 仍可能接近 `n`（比如全部不同的字符），排序的 `O(m log m)` 仍然不是线性的。我们可以利用 “频率范围是已知的” 这个特性把排序去掉，做到 **线性时间**。

关键观察：

- 每个字符的出现次数 `freq` 必然在区间 `[1, n]`（最少出现一次，最多出现 `n` 次）。
- 如果我们把 **出现次数相同的字符放进同一个桶**（bucket），那么只要把 **桶从高频到低频依次输出**，就能得到按频率降序的字符串，根本不需要比较大小。

这就是 **桶排序（Bucket Sort）** 的思想。实现步骤：

1. **计数**：和暴力解一样，用哈希表统计每个字符出现的次数。  
2. **建立桶**：创建一个长度为 `n+1` 的列表 `buckets`，下标 `i` 表示“出现次数恰好为 `i` 的字符集合”。因为出现次数最多不超过 `n`，所以 `buckets` 的大小只需要 `n+1`。  
3. **把字符放进对应的桶**：遍历哈希表的 `(ch, cnt)`，把字符 `ch` 加入 `buckets[cnt]`。这里每个桶可以是一个列表，存放所有出现次数相同的字符。  
4. **倒序遍历桶并拼接**：从 `n` 开始往下遍历 `buckets`，如果当前桶不为空，则把其中的每个字符重复 `cnt` 次加入结果。因为我们是从大到小遍历，所以自然满足频率递减。

这样就把 “排序” 这一步换成了 “线性遍历桶”，时间复杂度降到 **O(n)**。

如果想用 **优先队列（堆）** 也是一种思路：把每个字符和频率放进最大堆，每次弹出频率最高的字符。但堆的插入/弹出是 `O(log m)`，总体仍是 `O(n log m)`，不如桶排序快。这里我们重点展示桶排序的实现，因为它最能体现 “利用已知频率范围实现线性时间” 的技巧。

#### 代码（Python）

```python
def frequency_sort_opt(s: str) -> str:
    n = len(s)

    # 1. 统计每个字符的出现次数（哈希表）
    freq = {}
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1

    # 2. 建立长度为 n+1 的桶，每个桶是一个列表，存放出现次数相同的字符
    #    下标 i 表示“出现 i 次的字符”
    buckets = [[] for _ in range(n + 1)]

    # 3. 把字符放进对应的桶
    for ch, cnt in freq.items():
        buckets[cnt].append(ch)

    # 4. 从高频到低频遍历桶，拼接结果
    res = []
    for cnt in range(n, 0, -1):          # 从 n 倒着遍历到 1
        if not buckets[cnt]:
            continue                     # 空桶直接跳过
        for ch in buckets[cnt]:         # 同一频率的字符可以任意顺序
            res.append(ch * cnt)        # 把字符重复 cnt 次加入结果

    return ''.join(res)
```

#### 复杂度

- **时间复杂度**：`O(n)`。  
  *解释*：一次遍历统计频率 `O(n)`，创建桶的大小是 `n+1`（线性），把字符放进桶是 `O(m)`（`m≤n`），倒序遍历桶共计 `O(n)`（每个字符恰好被写入结果一次）。所有步骤都是线性相加。  
- **空间复杂度**：`O(n)`。  
  *解释*：哈希表占 `O(m)`，桶列表占 `O(n)`，结果字符串占 `O(n)`，总体仍是线性。

---

## 心得

- 这道题的核心技巧是 **利用出现次数的取值范围做桶排序**，把“排序”问题转化为线性遍历。  
- 该技巧适用于 **频率统计类、计数排序类** 的题目，例如  
  1. **Top K Frequent Elements**（前 K 个高频元素）  
  2. **Sort Colors**（颜色分类）  
  3. **Maximum Number of Words Found in a Dictionary**（单词出现次数统计）  
- 一句话总结解题钥匙：**“出现次数有上限 → 用下标直接映射 → 线性遍历即可”。**

## 反思

- 拿到题目第一反应往往是 “先统计频率，再排序”，这就是暴力思路。  
- 最容易踩的坑：  
  - 忽视字符种类可能很多，导致对 `sorted()` 的时间复杂度估计不足。  
  - 桶的大小一定要是 `n+1`（包括出现 `0` 次的下标），否则下标越界。  
  - 记得把同一频率的字符全部输出，不能交叉出现，否则会破坏“相同字符必须相邻”的要求。  
- 下次遇到同类题，第一步应想到 **“出现次数的范围已知吗？能否用桶/计数数组把频率直接映射？”**，这往往是把复杂度从 `O(n log n)` 降到 `O(n)` 的关键。