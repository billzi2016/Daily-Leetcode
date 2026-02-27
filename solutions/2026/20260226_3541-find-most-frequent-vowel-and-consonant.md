# #3541. 寻找出现次数最多的元音和辅音 / Find Most Frequent Vowel and Consonant

> 难度：简单 · 标签：Hash Table、String、Counting · [LeetCode 链接](https://leetcode.com/problems/find-most-frequent-vowel-and-consonant/)

---

## 题目（英文原版）

**Description**

You are given a string s consisting of lowercase English letters ('a' to 'z').
Your task is to:
Return the sum of the two frequencies.
Note: If multiple vowels or consonants have the same maximum frequency, you may choose any one of them. If there are no vowels or no consonants in the string, consider their frequency as 0.

**Examples**

**Example 1:**

```
Input: s = "successes"
Output: 6
Explanation:
```

**Example 2:**

```
Input: s = "aeiaeia"
Output: 3
Explanation:
```

**Constraints**

- 1 <= s.length <= 100
- s consists of lowercase English letters only.

---

## 题目（中文翻译）

给定一个仅包含小写英文字母（'a' 到 'z'）的字符串 `s`。  
你的任务是：

- 找出出现次数最多的元音（vowel）以及出现次数最多的辅音（consonant）；
- 返回这两个字符出现频率（frequency）的和。

> **说明**：如果有多个元音或多个辅音拥有相同的最大频率，你可以任意选择其中之一。  
> 如果字符串中不存在元音或不存在辅音，则对应的频率视为 `0`。

示例：

**示例 1**  
```
Input: s = "successes"
Output: 6
Explanation:
```

**示例 2**  
```
Input: s = "aeiaeia"
Output: 3
Explanation:
```

约束条件：

- `1 <= s.length <= 100`
- `s` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把字符串里每个字母出现的次数都统计出来**，然后再在元音集合 `{'a','e','i','o','u'}` 和其余字母（即辅音）中各找出出现次数最高的那个，最后把这两个最高次数相加即得答案。

- **用到的数据结构**：  
  - **哈希表（字典）**，可以把它想象成一本**查字典**：每个单词（这里是字母）是 **key**，对应的页码（这里是出现次数）是 **value**。查询、插入、更新的时间都很快（相当于在字典里直接翻到对应的页码）。

- **为什么这个方法正确**：  
  统计完每个字母出现的次数后，我们只需要比较两类字母（元音、辅音）各自的最大值。因为题目要求的就是“出现频率最高的元音 + 出现频率最高的辅音”。只要统计完整，取最大值自然就对了。

- **时间/空间复杂度的大白话**：  
  - 暴力实现可以用两层循环：外层遍历字母表的 26 个字母，内层遍历字符串 `s` 去计数。这相当于 **把每个字母都检查一遍**，所以时间是 `26 * n`，在算法表示里写成 **O(n²)**（因为 `n` 最多是 100，实际运行仍然很快）。  
  - 空间上只需要保存 26 个计数，用一个大小固定的数组或字典，**常数级别的空间**，记作 **O(1)**（不随输入长度增长）。

#### 代码（Python）

```python
def most_frequent_vowel_consonant_bruteforce(s: str) -> int:
    # 元音集合，像一本只收录元音的“小词典”
    vowels = set('aeiou')
    # 记录所有字母出现次数的字典：key 是字母，value 是出现次数
    freq = {}

    # 两层循环：外层遍历所有可能的字母，内层遍历字符串计数
    for ch in 'abcdefghijklmnopqrstuvwxyz':          # 只会遍历 26 次
        cnt = 0
        for c in s:                                   # 每次遍历整个字符串
            if c == ch:
                cnt += 1
        freq[ch] = cnt                                 # 把计数存进字典

    # 找出元音中出现次数最多的那个
    max_vowel = 0
    for v in vowels:
        max_vowel = max(max_vowel, freq[v])

    # 找出辅音中出现次数最多的那个
    max_consonant = 0
    for c in freq:
        if c not in vowels:                            # 只看辅音
            max_consonant = max(max_consonant, freq[c])

    # 两个最大次数相加即为答案
    return max_vowel + max_consonant
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 这里的 `n` 是字符串长度。因为我们用了两层遍历：外层固定 26 次，内层遍历 `n` 次，严格来说是 `26 * n`，但在大 O 表示法里仍写作 `O(n²)`，意思是“随着 `n` 增大，运行时间会呈二次增长”。  
- **空间复杂度**：`O(1)` —— 只用了一个长度为 26 的字典，所占空间不随 `n` 变化，始终是常数。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于我们对每个字母都遍历了一遍字符串**，其实这一步是完全可以省掉的。我们只需要 **一次遍历** 就能把每个字母的出现次数全部统计完。

优化思路如下：

1. **一次遍历**：从左到右扫描字符串 `s`，遇到一个字母就把它在哈希表中的计数加 1。相当于在“查字典”时直接把对应的页码加一，省掉了二次遍历的过程。  
2. **实时更新最大值**：在遍历的过程中，分别维护两个变量 `max_vowel`、`max_consonant`，当某个字母计数更新后，立刻检查它是否是当前类别（元音或辅音）的最大值。如果是，就直接更新对应的最大值。这样 **不需要再遍历哈希表一次** 去找最大值。  
3. **边界情况**：如果字符串里根本没有元音（或辅音），对应的最大值保持为 0，正好符合题目要求。

**核心算法**：**一次遍历 + 哈希表计数**。这在很多“统计出现次数”类题目中都是最常用、最高效的做法。

> 类比：想象你在超市统计每种商品的销量。暴力做法是每种商品都去看一遍全部收银记录（二次遍历），最优做法是每收到一张小票就立即把对应商品的销量加一（一次遍历），既省时又省力。

#### 代码（Python）

```python
def most_frequent_vowel_consonant(s: str) -> int:
    vowels = set('aeiou')          # 元音集合，查找是否为元音 O(1)
    freq = {}                      # 哈希表：key = 字母，value = 出现次数
    max_vowel = 0                  # 当前出现次数最高的元音
    max_consonant = 0              # 当前出现次数最高的辅音

    for ch in s:                   # 只遍历一次字符串
        # 更新哈希表计数
        freq[ch] = freq.get(ch, 0) + 1

        # 根据字母是元音还是辅音，更新对应的最大值
        if ch in vowels:
            # 如果这次计数超过之前的最大元音计数，就更新
            if freq[ch] > max_vowel:
                max_vowel = freq[ch]
        else:                       # 辅音
            if freq[ch] > max_consonant:
                max_consonant = freq[ch]

    # 两个最大值相加即为答案
    return max_vowel + max_consonant
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历一次字符串，`n` 是字符串长度。用“大白话”说，就是“随着字符数线性增长，运行时间也线性增长”。  
- **空间复杂度**：`O(1)` —— 哈希表最多存 26 个字母的计数，属于常数空间。即使不使用哈希表，只用两个计数数组（长度 26）也同样是常数空间。

> 与暴力解相比，时间从二次级别降到了线性级别，速度提升非常明显，尤其当 `n` 变大时差距会更加明显。

---

## 心得

- **核心技巧**：一次遍历统计频次 + 实时维护最大值（哈希表计数）。  
- **适用的题型**：  
  1. “找出现次数最多的字符”类（如 LeetCode 383 → 赎回最大字符）。  
  2. “统计字母/数字出现频率”类（如 统计字符串中每个字母出现次数）。  
  3. “找出现次数最高的子集”类（如 统计数组中出现最多的数）。  
- **一句话总结解题钥匙**：**“一次遍历，边走边记，最大值随时更新”。**

---

## 反思

- **第一反应**：先想到用字典把每个字符的出现次数都统计出来，然后再分别取元音、辅音的最大值。  
- **最容易踩的坑**：  
  - 忘记处理 **没有元音或没有辅音** 的情况，导致最大值未初始化而报错。  
  - 把元音集合写错（比如少了 `'u'`），会把真实的元音当成辅音计数。  
  - 对大小写不敏感的输入忘记统一转为小写（本题已保证全小写，其他题目要注意）。  
- **下次类似题的第一步**：**先确定需要统计的“类别”（如元音/辅音、奇数/偶数等），然后用一次遍历的哈希表/计数数组把每个类别的出现次数记录下来**。这样就能在遍历中同步更新所需的最大/最小值，避免二次循环。