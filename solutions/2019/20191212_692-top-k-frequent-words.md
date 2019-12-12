# #692. 前 K 高频单词 / Top K Frequent Words

> 难度：中等 · 标签：Array、Hash Table、String、Trie、Sorting、Heap (Priority Queue)、Bucket Sort、Counting · [LeetCode 链接](https://leetcode.com/problems/top-k-frequent-words/)

---

## 题目（英文原版）

**Description**

Given an array of strings words and an integer k, return the k most frequent strings.
Return the answer sorted by the frequency from highest to lowest. Sort the words with the same frequency by their lexicographical order.
Follow-up: Could you solve it in O(n log(k)) time and O(n) extra space?

**Examples**

**Example 1:**

```
Input: words = ["i","love","leetcode","i","love","coding"], k = 2
Output: ["i","love"]
Explanation: "i" and "love" are the two most frequent words.
Note that "i" comes before "love" due to a lower alphabetical order.
```

**Example 2:**

```
Input: words = ["the","day","is","sunny","the","the","the","sunny","is","is"], k = 4
Output: ["the","is","sunny","day"]
Explanation: "the", "is", "sunny" and "day" are the four most frequent words, with the number of occurrence being 4, 3, 2 and 1 respectively.
```

**Constraints**

- 1 <= words.length <= 500
- 1 <= words[i].length <= 10
- words[i] consists of lowercase English letters.
- k is in the range [1, The number of unique words[i]]

---

## 题目（中文翻译）

给定一个字符串数组（array）`words` 和一个整数（integer）`k`，返回出现频率最高的 `k` 个字符串。返回的答案需要按频率从高到低排序。频率相同的单词按字典序（lexicographical order）排序。

**示例 1**  
**输入**: `words = ["i","love","leetcode","i","love","coding"], k = 2`  
**输出**: `["i","love"]`  
**解释**: `"i"` 和 `"love"` 是出现频率最高的两个单词。由于 `"i"` 的字母序更小，排在 `"love"` 前面。

**示例 2**  
**输入**: `words = ["the","day","is","sunny","the","the","the","sunny","is","is"], k = 4`  
**输出**: `["the","is","sunny","day"]`  
**解释**: `"the"、"is"、"sunny"、"day"` 是出现频率最高的四个单词，出现次数分别为 4、3、2、1。

**约束条件**  
- `1 <= words.length <= 500`  
- `1 <= words[i].length <= 10`  
- `words[i]` 只包含小写英文字母。  
- `k` 的取值范围为 `[1, 不同单词的数量]`。

**进阶**: 你能否在 `O(n log(k))` 时间复杂度和 `O(n)` 额外空间复杂度下完成此题？

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**先把每个单词出现的次数统计出来**，再**把所有单词按照出现次数从高到低排序**，相同次数的单词再按字典序（字母顺序）排序，最后取前 `k` 个即可。

- **统计次数**：使用哈希表（Python 中的 `dict`），把单词当作 **key**，出现次数当作 **value**。哈希表就像一本词典，查找单词对应的页码是 O(1) 的。
- **排序**：把哈希表的 `items()`（即 `(word, freq)`）放进列表，用 `sorted` 并自定义排序规则：先按频率降序（`-freq`），再按单词的字典序升序（`word`）。
- **取前 k**：排序完成后，直接切片 `[:k]` 即可得到答案。

这个方法**一定正确**，因为我们把所有单词的出现次数都算清楚了，然后严格按照题目要求的顺序排好序，前 `k` 项自然就是我们要的结果。

**复杂度分析（大白话）**  
- 统计次数遍历一次数组，**时间是 O(n)**，`n` 是单词总数。  
- 排序要把 `m`（不同单词的数量）个元素排个序，排序的时间复杂度是 **O(m log m)**。在最坏情况下 `m` 可能和 `n` 差不多（每个单词都不相同），所以可以把它写成 **O(n log n)**。  
- 空间上我们需要保存哈希表和排序列表，最坏需要存 `m` 条记录，**空间是 O(m) ≈ O(n)**。

> **O(n log n)** 的意思是：如果你有 1000 条数据，排序大概要做 1000 × log₂1000 ≈ 1000 × 10 = 1 万次比较；如果是 1 万条数据，则是 1 万 × log₂1万 ≈ 1 万 × 14 = 14 万次比较。随着数据规模增大，比较次数会比线性增长（O(n)）快很多。

#### 代码（Python）

```python
from typing import List
from collections import defaultdict

def topKFrequent(words: List[str], k: int) -> List[str]:
    # 1️⃣ 统计每个单词出现的次数
    freq = defaultdict(int)               # 哈希表：key=单词，value=出现次数
    for w in words:                        # 遍历一次数组
        freq[w] += 1

    # 2️⃣ 把 (单词, 次数) 放进列表并排序
    #    排序规则：次数多的在前；次数相同则字典序小的在前
    sorted_items = sorted(
        freq.items(),
        key=lambda x: (-x[1], x[0])        # -x[1] 实现次数降序，x[0] 实现字典序升序
    )

    # 3️⃣ 取前 k 个单词的 word 部分返回
    return [word for word, _ in sorted_items[:k]]
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 统计次数 O(n)  
  - 排序 O(m log m) ≈ O(n log n)（因为 m ≤ n）  
  - 取前 k O(k)（k 很小，可忽略）

- **空间复杂度**：`O(n)`  
  - 哈希表保存每个不同单词及其计数，最坏需要 O(n) 的空间  
  - 排序时会额外创建一个大小为 m 的列表，也在同数量级  

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **完整排序**——我们把所有不同单词都排了一遍序，但题目只要求前 `k` 个。**如果能只维护前 `k` 个最频繁的单词，就不必对全部进行排序**，这样时间可以降到 `O(n log k)`。

实现思路：

1. **同样先用哈希表统计出现次数**（这一步无法省略，仍是 O(n)）。
2. **使用最小堆（优先队列）** 保存当前「最有可能进入答案」的 `k` 个单词。  
   - 堆顶是 **频率最小、且在频率相同的情况下字典序最大的**，这样当我们遇到更「好」的单词时，堆顶的「最差」单词就会被弹出。
   - Python 的 `heapq` 默认是 **小根堆**，我们只要把「频率」取负数或自行设计比较键即可。
3. **遍历哈希表的每个 (word, freq)**，把 `(freq, word)` 推入堆中。  
   - 若堆的大小超过 `k`，就弹出堆顶（最差的），保证堆里始终只保留 `k` 条「最好的」记录。
4. **堆中剩下的 `k` 条记录正好是答案**，但它们是按「最差在前」的顺序存放的，需要再 **弹出并倒序**（或直接排序）得到「频率高到低、字典序小到大」的最终顺序。

**为什么最小堆能工作？**  
- 堆的大小始终是 `k`，每次插入或弹出操作的时间是 `O(log k)`。  
- 我们只对每个不同单词（最多 `m` 条）进行一次「入堆」操作，整体时间是 `O(m log k)`，而 `m ≤ n`，所以是 `O(n log k)`。  
- 空间只需要保存哈希表（`O(m)`) 和大小为 `k` 的堆（`O(k)`），总体 `O(n)`。

> **O(n log k)** 的含义：如果 `k` 很小（比如 10），即使 `n` 达到几万，`log k` 只约等于 3~4，整体运算次数几乎和线性 `O(n)` 差不多。

#### 代码（Python）

```python
from typing import List
from collections import defaultdict
import heapq

def topKFrequent(words: List[str], k: int) -> List[str]:
    # 1️⃣ 统计出现次数（同暴力解）
    freq = defaultdict(int)
    for w in words:
        freq[w] += 1

    # 2️⃣ 最小堆，保存当前最好的 k 条记录
    #    堆里存 (freq, word)；Python 小根堆会把 freq 最小的放在堆顶
    #    为了在 freq 相同的情况下让字典序大的单词先弹出，
    #    我们把 word 取负的字典序（即直接使用 word 本身，因为堆会比较第一个元素后比较第二个元素）
    heap = []

    for word, f in freq.items():
        # 推入堆中
        heapq.heappush(heap, (f, word))
        # 若堆大小超过 k，弹出最小的（频率最少或字典序最大的）
        if len(heap) > k:
            heapq.heappop(heap)

    # 3️⃣ 堆里剩下的就是答案，但顺序是「最差在前」
    #    弹出所有元素并逆序即可得到「频率高→低、字典序小→大」
    res = []
    while heap:
        f, w = heapq.heappop(heap)   # 弹出最小的
        res.append(w)                # 先放到列表尾部
    return res[::-1]                 # 逆序返回
```

> **代码关键点注释**  
- `heapq.heappush` 与 `heapq.heappop` 的时间复杂度都是 `O(log k)`。  
- 堆的比较规则默认先比较第一个元素（频率），相同再比较第二个元素（单词），正好满足「频率相同按字典序」的需求。  
- 最后 `res[::-1]` 是把「最差→最好」的列表倒过来，变成「最好→最差」。

#### 复杂度

- **时间复杂度**：`O(n log k)`  
  - 统计次数 O(n)  
  - 对每个不同单词进行一次堆操作 O(m log k) ≤ O(n log k)  
  - 最后把堆弹出 O(k log k)（k ≤ n，已被前面的 O(n log k) 包含）

- **空间复杂度**：`O(n)`  
  - 哈希表占 O(m) ≤ O(n)  
  - 堆占 O(k)（k ≤ m），总体仍是 O(n)

---

## 心得

- **核心技巧**：**最小堆（优先队列）** 用来维护「前 k 大」的元素，避免对全部数据做完整排序。  
- **适用题型**（类似技巧）  
  1. *Top K Frequent Elements*（数字版）  
  2. *Find K Closest Points to Origin*（几何版）  
  3. *Kth Largest Element in an Array*（第 K 大元素）  
- **一句话总结**：**只保留 k 条“最优”，用堆把“最差”踢出去**，即可在 O(n log k) 完成 Top‑K 任务。

---

## 反思

- **第一反应**：先把所有单词计数，然后全部排序，直接把前 k 取出来——这就是暴力解。  
- **最容易踩的坑**  
  - **字典序的处理**：在频率相同的情况下，必须保证字典序小的排在前面。堆的比较键要写对，`(freq, word)` 正好满足要求；如果把 `freq` 取负或写成 `(-freq, word)`，记得对应地改堆的性质。  
  - **堆大小的控制**：忘记在堆超过 k 时弹出，会导致空间和时间都退化回 O(n log n)。  
  - **结果顺序**：堆弹出的顺序是从「最差」到「最好」，需要逆序或再排序，否则输出会是倒着的。  
- **下次类似题的第一步**：**先思考是否真的需要对全部数据排序**，如果只要前 K，立刻考虑「堆」或「快速选择」这类只保留 K 条记录的技巧。这样可以把时间从 `O(n log n)` 降到 `O(n log k)`，效率大幅提升。