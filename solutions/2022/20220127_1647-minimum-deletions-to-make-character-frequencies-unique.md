# #1647. 使字符频率唯一的最少删除次数 / Minimum Deletions to Make Character Frequencies Unique

> 难度：中等 · 标签：Hash Table、String、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/minimum-deletions-to-make-character-frequencies-unique/)

---

## 题目（英文原版）

**Description**

A string s is called good if there are no two different characters in s that have the same frequency.
Given a string s, return the minimum number of characters you need to delete to make s good.
The frequency of a character in a string is the number of times it appears in the string. For example, in the string "aab", the frequency of 'a' is 2, while the frequency of 'b' is 1.

**Examples**

**Example 1:**

```
Input: s = "aab"
Output: 0
Explanation: s is already good.
```

**Example 2:**

```
Input: s = "aaabbbcc"
Output: 2
Explanation: You can delete two 'b's resulting in the good string "aaabcc".
Another way it to delete one 'b' and one 'c' resulting in the good string "aaabbc".
```

**Example 3:**

```
Input: s = "ceabaacb"
Output: 2
Explanation: You can delete both 'c's resulting in the good string "eabaab".
Note that we only care about characters that are still in the string at the end (i.e. frequency of 0 is ignored).
```

**Constraints**

- 1 <= s.length <= 105
- s contains only lowercase English letters.

---

## 题目（中文翻译）

一个字符串（string）**s** 若不存在两种不同字符的出现频率相同，则称其为**好（good）**字符串。  
给定字符串 **s**，返回使 **s** 成为好字符串所需删除的最少字符数。

字符的频率（frequency）指该字符在字符串中出现的次数。例如，在字符串 `"aab"` 中，字符 `'a'` 的频率为 2，字符 `'b'` 的频率为 1。

**示例 1**

> **输入**: `s = "aab"`  
> **输出**: `0`  
> **解释**: `s` 已经是好字符串，无需删除任何字符。

**示例 2**

> **输入**: `s = "aaabbbcc"`  
> **输出**: `2`  
> **解释**: 可以删除两个 `'b'`，得到好字符串 `"aaabcc"`。  
> 另一种做法是删除一个 `'b'` 和一个 `'c'`，得到好字符串 `"aaabbc"`。

**示例 3**

> **输入**: `s = "ceabaacb"`  
> **输出**: `2`  
> **解释**: 删除两个 `'c'`，得到好字符串 `"eabaab"`。  
> 注意，只考虑最终字符串中仍然存在的字符（频率为 0 的字符不计入）。

**约束条件**

- `1 <= s.length <= 10^5`
- `s` 仅包含小写英文字母。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**穷举所有可能的删除方式**，看哪一种最省删字符。  
具体可以这样做：

1. 先统计每个字母出现的次数（相当于查字典：字母 → 次数）。  
2. 对于每个字母，我们可以把它的出现次数从原始值一直减到 0（即全部删掉），每种减法对应一种“删除方案”。  
3. 把所有字母的“减法”组合起来，就得到一种完整的删除方案。  
4. 检查该方案得到的字符串是否已经“好”（所有非零频率互不相同），如果是，就记录下删除的字符数。  
5. 最后在所有合法方案中取最小的删除数。

> **生活化类比**：想象你在超市里挑选水果，每种水果都有若干个，你可以把任意数量的水果丢掉。要找出**最少**需要丢掉多少水果才能让每种水果的剩余数量都不相同，就得把每种水果的可能丢掉的数量全部列出来，逐一尝试。

**为什么这个方法正确？**  
因为它遍历了**所有**可能的删除组合，必然会包含最优的那一种。只要检查每一种组合是否满足“频率唯一”，并记录最小的删除次数，就能得到答案。

**为什么不推荐这么做？**  
- 字母表只有 26 种，但每种字母的出现次数可以高达 `10^5`。如果把每种字母的所有可能删除次数都列出来，组合数会呈指数级增长，根本不可计算。  
- 想象把 10 的 5 次方个苹果的“丢掉数量”全部列出来，组合数会天文数字，程序根本跑不完。

#### 代码（Python）

下面给出一个**完整的暴力实现**（仅作概念演示，实际会超时）：

```python
from collections import Counter
import itertools

def min_deletions_bruteforce(s: str) -> int:
    # 统计每个字符的出现次数
    freq = Counter(s)                 # 类似查字典，key 是字符，value 是出现次数
    chars = list(freq.keys())
    counts = [freq[c] for c in chars]  # 各字符的频率列表

    best = len(s)  # 最多删掉所有字符

    # 对每个字符，枚举它可以被删到的次数（0~原始频率）
    # itertools.product 会产生所有组合，组合数 = ∏(freq_i + 1)，极其庞大
    for deletions in itertools.product(*[range(c + 1) for c in counts]):
        # 计算删除后每个字符的剩余频率
        remain = [c - d for c, d in zip(counts, deletions)]
        # 过滤掉已经被全部删掉的字符（频率 0 不计入唯一性判断）
        positive = [x for x in remain if x > 0]

        # 检查正频率是否全部唯一
        if len(positive) == len(set(positive)):
            # 合法方案，更新最小删除数
            total_del = sum(deletions)
            best = min(best, total_del)

    return best
```

> **关键行中文注释**已经写在代码里。  

#### 复杂度  

- **时间复杂度**：`O(∏ (freq_i + 1))`（所有字符的频率加 1 的乘积），等价于指数级。  
  - 用大白话说，就是“几乎不可能在合理时间内跑完”。  
- **空间复杂度**：`O(k)`，`k` 为不同字符的种类（最多 26），因为只需要保存频率表和临时变量。  

显然，这种暴力方法在 LeetCode 的数据范围（字符串长度可达 10⁵）下会 **超时**，所以我们需要更聪明的做法。

---  

### 2. 最优解  

#### 思路  

从暴力解出发，**瓶颈**在于我们一次次“尝试所有可能的删法”。实际上，**只要把冲突的频率往下调到一个未被占用的值**，就已经是最省删字符的方式了。  

关键观察：

1. **只需要关心出现次数**，而不是字符本身。字符之间是可以互换的，只要频率集合满足唯一性即可。  
2. **频率越大，越不容易往下调**（因为调到 0 也只能删掉这么多）。所以我们应该**先处理出现次数大的字符**，让它们“抢占”大的频率位。  
3. 当我们遍历频率（从大到小）时，**如果当前频率已经被使用**，就把它**不断减 1**，直到找到一个 **未被使用** 的正整数（或者减到 0，表示该字符全部删掉）。每次减 1 就相当于删除一个字符。  

这就是 **贪心 + 哈希表** 的思路：

- 用 **哈希表（set）** 记录已经“占用”的频率，就像字典里记录每个词对应的页码。  
- 按 **频率从大到小** 排序，保证“大频率先抢位”。  
- 对每个频率 `f`，不断 `f -= 1`（相当于删除字符），直到 `f == 0` 或者 `f` 不在已占用集合中。把最终的 `f` 加入集合，并累计删掉的字符数 `original_f - f`。  

> **类比**：想象你在排队买电影票，票价从高到低排好。每个人只能买一次且只能买未被占用的票价。若某个票价已经被买走，大家只能往后面更便宜的票价找，直到买到没有人买的票价（或者买不到，只好放弃，即删掉全部字符）。  

#### 代码（Python）

```python
from collections import Counter

def min_deletions(s: str) -> int:
    # 1. 统计每个字符的出现次数
    freq_counter = Counter(s)                 # 哈希表：字符 -> 次数
    frequencies = list(freq_counter.values()) # 只保留出现次数

    # 2. 按出现次数从大到小排序（贪心的关键）
    frequencies.sort(reverse=True)

    used = set()      # 已经占用的频率集合
    deletions = 0     # 累计删除的字符数

    for f in frequencies:
        # 只要当前频率已经被占用，就往下调
        while f > 0 and f in used:
            f -= 1          # 删除一个字符
            deletions += 1  # 记录一次删除操作
        # 调整完毕后，把这个频率加入占用集合（如果 f==0 则不加入，因为 0 表示字符全删掉）
        if f > 0:
            used.add(f)

    return deletions
```

**代码要点说明**（每行都有中文注释）：

- `Counter(s)`：把字符串看成一本字典，键是字符，值是它出现的次数。  
- `frequencies.sort(reverse=True)`：把出现次数从大到小排好，保证“大频率先抢位”。  
- `while f > 0 and f in used:`：只要当前频率已经被别的字符占用，就把它往下调（相当于删字符），直到找到一个空位或调到 0。  
- `used.add(f)`：把最终得到的、未被占用的频率记下来，防止后面的字符再次使用同样的频率。  

#### 复杂度  

- **时间复杂度**：`O(n log n)`，其中 `n` 为不同字符的种类（最多 26），  
  - 主要来源于对频率列表的排序 `O(k log k)`（`k ≤ 26`），  
  - 其余的遍历和集合查询都是 `O(k)`，几乎可以忽略。  
  - 用大白话说，就是“几乎瞬间完成”，即使字符串长度是 10⁵ 也不受影响，因为我们只处理 26 种字符。  

- **空间复杂度**：`O(k)`，即最多存储 26 个频率的集合和列表，几乎可以视作常数空间。  

相比暴力的指数级时间，这个贪心方案在所有合法输入下都能轻松跑完。

---  

## 心得  

- **核心技巧**：**贪心 + 哈希集合**（把已经占用的频率记下来，冲突时往下调）。  
- **适用的题型**：  
  1. “使数组/字符串的元素唯一”类问题（如 “让数组中的元素各不相同的最少修改次数”）。  
  2. “把数值压缩到不冲突”类问题（如 “最少移动使所有坐标不重合”）。  
  3. “频率/计数唯一化”类问题（本题）。  
- **一句话总结**：**先让大频率抢占高位，冲突就往下删——最省删字符的贪心法**。

---  

## 反思  

- **拿到题目第一反应**：想到先统计字符出现次数，然后想办法让这些次数互不相同。  
- **最容易踩的坑**：  
  - 忽略了 **频率为 0 的字符不计入唯一性**，导致把已经全部删掉的字符也算进冲突检查。  
  - 在调频率时忘记累计删除的次数，或者把 `while f > 0` 写成 `while f >= 0`，会导致无限循环。  
  - 没有对频率进行降序排序，导致小频率先占位，后面的大频率被迫删更多字符，结果不是最优。  
- **下次遇到同类题**：第一步就**统计频率并排序**，再用 **集合记录已占用的频率**，冲突时**向下调**，边调边累计删除次数。这样可以直接得到最优解。