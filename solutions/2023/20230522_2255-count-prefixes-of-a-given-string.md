# #2255. 统计给定字符串的前缀数量 / Count Prefixes of a Given String

> 难度：简单 · 标签：Array、String · [LeetCode 链接](https://leetcode.com/problems/count-prefixes-of-a-given-string/)

---

## 题目（英文原版）

**Description**

You are given a string array words and a string s, where words[i] and s comprise only of lowercase English letters.
Return the number of strings in words that are a prefix of s.
A prefix of a string is a substring that occurs at the beginning of the string. A substring is a contiguous sequence of characters within a string.

**Examples**

**Example 1:**

```
Input: words = ["a","b","c","ab","bc","abc"], s = "abc"
Output: 3
Explanation:
The strings in words which are a prefix of s = "abc" are:
"a", "ab", and "abc".
Thus the number of strings in words which are a prefix of s is 3.
```

**Example 2:**

```
Input: words = ["a","a"], s = "aa"
Output: 2
Explanation:
Both of the strings are a prefix of s. 
Note that the same string can occur multiple times in words, and it should be counted each time.
```

**Constraints**

- 1 <= words.length <= 1000
- 1 <= words[i].length, s.length <= 10
- words[i] and s consist of lowercase English letters only.

---

## 题目（中文翻译）

给定一个字符串数组 `words` 和一个字符串 `s`，其中 `words[i]` 与 `s` 均只包含小写英文字母。  
返回 `words` 中有多少个字符串是 `s` 的前缀（prefix）。

前缀（prefix）是指出现在字符串开头的子串（substring），子串（substring）是字符串中连续的字符序列。

**示例 1**  

```text
Input: words = ["a","b","c","ab","bc","abc"], s = "abc"
Output: 3
Explanation:
在 s = "abc" 中，以下字符串是前缀（prefix）：
"a", "ab", "abc"。
因此，满足条件的字符串数量为 3。
```

**示例 2**  

```text
Input: words = ["a","a"], s = "aa"
Output: 2
Explanation:
两个字符串都是 s 的前缀（prefix）。  
注意，同一个字符串在 words 中可以出现多次，需分别计数。
```

**约束条件**

- `1 <= words.length <= 1000`
- `1 <= words[i].length, s.length <= 10`
- `words[i]` 和 `s` 只由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法就是把 `words` 里每一个字符串都和 `s` 对比，看它是不是 `s` 的前缀。  
- **数据结构**：这里仅需要遍历列表 `words`，不需要额外的数据结构。可以把「前缀」想象成「书的目录」——目录里每一项都是从书的开头开始的连续章节。如果我们手里有一本书 `s`，只要把目录项（即 `words[i]`）逐字比对，完全匹配就说明它是前缀。  
- **正确性**：如果 `words[i]` 完全等于 `s` 的前 `len(words[i])` 个字符，那么它必然是 `s` 的前缀；反之，如果有任意一个字符不相等，就不可能是前缀。遍历全部 `words`，把符合条件的计数相加，即得到答案。  

#### 代码（Python）

```python
from typing import List

def count_prefixes(words: List[str], s: str) -> int:
    ans = 0                         # 统计满足条件的数量
    for w in words:                 # 逐个检查 words 中的字符串
        # 如果 w 的长度超过 s，显然不可能是前缀，直接跳过
        if len(w) > len(s):
            continue
        # 判断 w 是否等于 s 的前 len(w) 个字符
        if s.startswith(w):        # str.startswith 相当于“把 w 按顺序放在 s 开头比对”
            ans += 1                # 符合条件，计数加一
    return ans
```

#### 复杂度

- **时间复杂度**：`O(N * L)`  
  - `N = len(words)`（最多 1000），`L = max(len(w), len(s))`（最多 10）。  
  - 直观理解：我们要检查每个单词（最多 N 次），每次检查最多看 `L` 个字符，所以总共大约要做 `N × L` 次字符比较。  
- **空间复杂度**：`O(1)`  
  - 只用了常数级别的额外变量 `ans`、`w`，不随输入规模增长而增加。

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在于：每次检查都要遍历 `w` 的所有字符，而 `s` 的长度非常短（≤10），我们可以把 **所有可能的前缀** 先算出来，放进一个集合（相当于「查字典」），后面只需要 O(1) 的时间判断 `w` 是否在集合中。

具体步骤：

1. **预处理 `s`**  
   - 从第一个字符开始，依次取出长度为 1、2、…、`len(s)` 的子串，全部放入集合 `prefixes`。  
   - 这一步类似把一本书的所有章节标题提前写好，后面查找时只要看标题是否在目录里即可。

2. **遍历 `words`**  
   - 对每个 `w`，只要判断 `w` 是否在 `prefixes` 中（集合的查找时间是常数 O(1)），如果是则计数加一。

这样我们把 **每个单词的字符比较** 换成了 **一次哈希查找**，整体时间从 `O(N·L)` 降到 `O(N + L)`，在本题约束下差别不大，但思路更具通用性（例如 `s` 很长时优势明显）。

#### 代码（Python）

```python
from typing import List

def count_prefixes_opt(words: List[str], s: str) -> int:
    # 1. 生成 s 的所有前缀，放入集合
    prefixes = set()
    for i in range(1, len(s) + 1):          # i 表示前缀的长度
        prefixes.add(s[:i])                # s[:i] 取前 i 个字符
        # 例如 s = "abc" 时，循环后 prefixes = {"a", "ab", "abc"}

    # 2. 统计在 words 中出现的前缀数量
    ans = 0
    for w in words:
        if w in prefixes:                  # 哈希表查找，时间常数
            ans += 1
    return ans
```

#### 复杂度

- **时间复杂度**：`O(N + L)`  
  - 生成前缀只遍历一次 `s`（`L` 步），随后遍历 `words`（`N` 步），每一步的操作都是常数时间。  
  - 与暴力解相比，去掉了每个单词内部的字符比较，整体更快，尤其当 `s` 很长时优势显著。

- **空间复杂度**：`O(L)`  
  - 需要保存 `s` 的所有前缀，最多 `len(s)`（≤10）个字符串，占用的额外空间与 `s` 长度成正比。

---

## 心得

- **核心技巧**：把“前缀是否匹配”转化为“集合成员查询”。  
- **适用场景**：  
  1. **前缀计数**：如本题、统计多少单词是给定句子的前缀。  
  2. **字典查询**：判断一个单词是否在已有词典里（使用集合或哈希表）。  
  3. **过滤重复**：需要快速去重或检查出现次数的场景。  
- **一句话总结**：把所有可能的答案提前准备好，用哈希表一次查找代替逐字符比较。

## 反思

- **第一反应**：直接遍历 `words`，用 `startswith` 检查前缀——最直观的暴力思路。  
- **最容易踩的坑**：  
  - 忽略 `words[i]` 长度大于 `s` 的情况，会导致 `startswith` 返回 `False`，但如果手写比较可能会出现索引越界。  
  - 统计时忘记考虑 `words` 中出现的重复字符串，需要每次都计数。  
- **下次第一步**：先思考能否把问题转化为“集合/哈希表查询”，如果可以，就先构造相应的数据结构，再进行线性遍历。这样常能把 O(N·L) 的暴力解降到 O(N+L)。