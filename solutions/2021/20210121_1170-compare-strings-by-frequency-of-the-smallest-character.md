# #1170. 比较字符串的最小字符出现频率 / Compare Strings by Frequency of the Smallest Character

> 难度：中等 · 标签：Array、Hash Table、String、Binary Search、Sorting · [LeetCode 链接](https://leetcode.com/problems/compare-strings-by-frequency-of-the-smallest-character/)

---

## 题目（英文原版）

**Description**

Let the function f(s) be the frequency of the lexicographically smallest character in a non-empty string s. For example, if s = "dcce" then f(s) = 2 because the lexicographically smallest character is 'c', which has a frequency of 2.
You are given an array of strings words and another array of query strings queries. For each query queries[i], count the number of words in words such that f(queries[i]) < f(W) for each W in words.
Return an integer array answer, where each answer[i] is the answer to the ith query.

**Examples**

**Example 1:**

```
Input: queries = ["cbd"], words = ["zaaaz"]
Output: [1]
Explanation: On the first query we have f("cbd") = 1, f("zaaaz") = 3 so f("cbd") < f("zaaaz").
```

**Example 2:**

```
Input: queries = ["bbb","cc"], words = ["a","aa","aaa","aaaa"]
Output: [1,2]
Explanation: On the first query only f("bbb") < f("aaaa"). On the second query both f("aaa") and f("aaaa") are both > f("cc").
```

**Constraints**

- 1 <= queries.length <= 2000
- 1 <= words.length <= 2000
- 1 <= queries[i].length, words[i].length <= 10
- queries[i][j], words[i][j] consist of lowercase English letters.

---

## 题目（中文翻译）

**描述**  
设函数 `f(s)` 表示非空字符串 `s` 中字典序最小字符的出现频率。例如，若 `s = "dcce"`，则 `f(s) = 2`，因为字典序最小的字符是 `'c'`，其出现次数为 2。  
给定字符串数组 `words` 和查询字符串数组 `queries`。对于每个查询 `queries[i]`，统计 `words` 中满足 `f(queries[i]) < f(W)` 的字符串 `W` 的数量。  
返回一个整数数组 `answer`，其中 `answer[i]` 为第 `i` 个查询的答案。

**示例 1**  
```text
Input: queries = ["cbd"], words = ["zaaaz"]
Output: [1]
Explanation: 对第一个查询，f("cbd") = 1，f("zaaaz") = 3，满足 f("cbd") < f("zaaaz")。
```

**示例 2**  
```text
Input: queries = ["bbb","cc"], words = ["a","aa","aaa","aaaa"]
Output: [1,2]
Explanation: 对第一个查询，仅有 f("bbb") < f("aaaa") 成立。对第二个查询，f("aaa") 与 f("aaaa") 均大于 f("cc")。
```

**约束条件**  
- `1 <= queries.length <= 2000`  
- `1 <= words.length <= 2000`  
- `1 <= queries[i].length, words[i].length <= 10`  
- `queries[i][j]`、`words[i][j]` 只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每个字符串的 f(s) 直接算出来**，然后对每一个 query，逐个遍历 `words`，统计满足 `f(query) < f(word)` 的 word 数量。

- **计算 f(s) 的方法**  
  1. 找出字符串里字典序最小的字符（就像在字典里找最先出现的单词）。  
  2. 统计这个字符在字符串中出现了多少次（相当于查字典后，看到对应页码上有几次相同的词）。  

- **为什么正确**  
  对每一个 query，我们都完整地比较了它与 `words` 中每一个元素的 f 值，只要满足不等式就计数，显然得到的计数就是题目要求的答案。

- **时间/空间复杂度**  
  - 计算一次 f(s) 需要遍历字符串一次，长度 ≤ 10，记作 O(L)。  
  - 暴力遍历每个 query 与每个 word：`queries` 长度记为 `m`，`words` 长度记为 `n`。  
    总时间 = `m * n * O(L)` ≈ O(m·n)，因为 L 很小可以视作常数。  
  - 需要额外的空间存放每次计算的 f 值，最多只保存一个整数，空间 O(1)。

> **大白话解释**  
> O(m·n) 就像你要把 `m` 本书的每一页都和 `n` 本书的每一页对比一次，次数会随 `m`、`n` 的乘积快速增长。

#### 代码（Python）

```python
from typing import List

def f(s: str) -> int:
    """
    计算字符串 s 中字典序最小字符的出现次数
    """
    # 1. 找最小字符
    smallest = min(s)                 # min 相当于在字典里找最先的词
    # 2. 统计出现次数
    return s.count(smallest)          # count 类似查字典后数页码上出现几次

def num_smaller_by_frequency(queries: List[str], words: List[str]) -> List[int]:
    answer = []
    for q in queries:                  # 对每个 query
        cnt_q = f(q)                   # 计算它的 f 值
        # 暴力遍历所有 words，统计满足 f(q) < f(w) 的数量
        bigger = sum(1 for w in words if f(w) > cnt_q)
        answer.append(bigger)
    return answer

# ------------------- 测试 -------------------
if __name__ == "__main__":
    print(num_smaller_by_frequency(["cbd"], ["zaaaz"]))               # [1]
    print(num_smaller_by_frequency(["bbb","cc"], ["a","aa","aaa","aaaa"]))  # [1,2]
```

#### 复杂度

- **时间复杂度**：O(m·n)  
  - `m` 为 queries 长度，`n` 为 words 长度。每一次比较都需要 O(1)（因为字符串长度 ≤ 10），所以总体随两者乘积线性增长。
- **空间复杂度**：O(1)  
  - 只用了常数个额外变量来存储计数值。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次 query 都要遍历完整个 words 列表**。如果我们事先把 `words` 中所有的 f 值算好并排序，就可以**利用二分查找**在 O(log n) 时间内得到比某个数更大的元素个数。

**步骤拆解**  

1. **预处理 words**  
   - 对 `words` 中每个字符串计算 f 值，得到一个整数数组 `word_vals`。  
   - 将 `word_vals` 排序（从小到大）。排序相当于把字典里所有页码排好序，方便快速定位。

2. **处理每个 query**  
   - 计算 query 的 f 值记为 `p`。  
   - 在已经排好序的 `word_vals` 中，用 **二分查找** 找到第一个 **大于 p** 的位置 `idx`。  
   - 所有大于 p 的元素数量 = `len(word_vals) - idx`。  
   - 把这个数量加入答案数组。

**为什么有效**  
二分查找的原理是：在有序数组中，每次可以把搜索区间砍掉一半，最快在 `log₂ n` 步内定位目标位置。因为我们只关心 “大于 p 的第一个位置”，所以一次二分即可得到答案。

**核心数据结构解释**  

- **数组 + 排序**：把所有 f 值装进普通列表，然后使用 Python 内置的 `sort()`（底层是 Timsort，时间复杂度 O(n log n)）。  
- **二分查找**：类似在排好序的电话号码簿里找某个号码的插入位置，`bisect_right`（或自行实现）可以返回 “右侧插入点”，即第一个大于目标的下标。

#### 代码（Python）

```python
from typing import List
import bisect   # Python 标准库中的二分查找工具

def f(s: str) -> int:
    """返回字符串 s 中字典序最小字符的出现次数"""
    smallest = min(s)
    return s.count(smallest)

def num_smaller_by_frequency(queries: List[str], words: List[str]) -> List[int]:
    # 1️⃣ 预处理 words：计算 f 值并排序
    word_vals = [f(w) for w in words]   # 把每个 word 转成对应的整数
    word_vals.sort()                    # 从小到大排好序，后面二分会用到

    answer = []
    # 2️⃣ 对每个 query，二分寻找第一个 > p 的位置
    for q in queries:
        p = f(q)                         # query 的 f 值
        # bisect_right 返回的是 “插入点”，即第一个大于 p 的下标
        idx = bisect.bisect_right(word_vals, p)
        # 所有更大的元素在 idx 右侧
        bigger_cnt = len(word_vals) - idx
        answer.append(bigger_cnt)

    return answer

# ------------------- 测试 -------------------
if __name__ == "__main__":
    print(num_smaller_by_frequency(["cbd"], ["zaaaz"]))               # [1]
    print(num_smaller_by_frequency(["bbb","cc"], ["a","aa","aaa","aaaa"]))  # [1,2]
```

#### 复杂度

- **时间复杂度**：  
  - 计算 `words` 的 f 值：O(n)（n = len(words)），每次 O(L) 但 L ≤ 10。  
  - 排序 `word_vals`：O(n log n)。  
  - 对每个 query 进行二分查找：每次 O(log n)，共 m 次 → O(m log n)。  
  - 综合：**O(n log n + m log n)**，相比暴力的 O(m·n) 快很多，尤其当 n、m 接近上限 2000 时差距明显。

- **空间复杂度**：O(n)  
  - 需要额外存放 `word_vals`（长度为 n 的整数数组）。其余变量都是常数级。

---

## 心得

- **核心技巧**：先把可重复使用的信息（这里是 `words` 的 f 值）预处理并排序，然后利用二分查找快速统计“大于某值”的元素个数。  
- **适用的题型**  
  1. “查询数组中比给定数大的元素个数”——如 LeetCode 2385 *Find the Number of Good Subarrays*（思路类似）。  
  2. “每个查询要求统计满足某种不等式的元素”——如 2146 *K Highest Ranked Items Within a Price Range*（先排序再二分）。  
  3. “需要多次比较同一组数据的不同查询”——如 2405 *Optimal Partition of String*（先做一次前缀统计）。  
- **一句话总结**：**“先把静态数据整理好（排序），再用二分把每次动态查询变成对数时间”**。

---

## 反思

- **第一反应**：看到“对每个 query 统计满足 f(query) < f(word) 的 word 数量”，立刻想到两层循环直接比较——这就是暴力解。  
- **最容易踩的坑**  
  - **忘记取最小字符的出现次数**：直接统计全部字符的出现次数会得到错误结果。  
  - **边界条件**：当所有 `word` 的 f 值都不大于 query 时，二分返回的下标可能是 `len(word_vals)`，此时 `len - idx = 0` 必须返回 0。  
  - **排序方向**：如果误用 `bisect_left`（返回第一个 ≥ p 的位置）而不是 `bisect_right`，会把等于 p 的元素算进 “更大” 的集合，导致答案偏大。  
- **下次遇到同类题的第一步**：先思考“这组数据是否可以一次性预处理（排序、前缀和、哈希计数）”，如果可以，就把预处理做完，再用 **二分/前缀查找** 把每个查询的复杂度降到对数或常数级。