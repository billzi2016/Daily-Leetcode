# #1338. 将数组大小减至一半 / Reduce Array Size to The Half

> 难度：中等 · 标签：Array、Hash Table、Greedy、Sorting、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/reduce-array-size-to-the-half/)

---

## 题目（英文原版）

**Description**

You are given an integer array arr. You can choose a set of integers and remove all the occurrences of these integers in the array.
Return the minimum size of the set so that at least half of the integers of the array are removed.

**Examples**

**Example 1:**

```
Input: arr = [3,3,3,3,5,5,5,2,2,7]
Output: 2
Explanation: Choosing {3,7} will make the new array [5,5,5,2,2] which has size 5 (i.e equal to half of the size of the old array).
Possible sets of size 2 are {3,5},{3,2},{5,2}.
Choosing set {2,7} is not possible as it will make the new array [3,3,3,3,5,5,5] which has a size greater than half of the size of the old array.
```

**Example 2:**

```
Input: arr = [7,7,7,7,7,7]
Output: 1
Explanation: The only possible set you can choose is {7}. This will make the new array empty.
```

**Constraints**

- 2 <= arr.length <= 105
- arr.length is even.
- 1 <= arr[i] <= 105

---

## 题目（中文翻译）

**题目描述**  
给定一个整数数组 `arr`。你可以选择一组整数，并删除数组中所有这些整数的出现次数。  
返回能够使数组中至少 **一半** 的整数被删除的最小集合大小。

**示例 1**  
```text
Input: arr = [3,3,3,3,5,5,5,2,2,7]
Output: 2
```
**解释**：选择集合 `{3,7}` 后，得到的新数组为 `[5,5,5,2,2]`，其长度为 5，正好是原数组长度的一半。  
可能的大小为 2 的集合还有 `{3,5}`、`{3,2}`、`{5,2}`。  
集合 `{2,7}` 不可行，因为会得到新数组 `[3,3,3,3,5,5,5]`，其长度大于原数组长度的一半。

**示例 2**  
```text
Input: arr = [7,7,7,7,7,7]
Output: 1
```
**解释**：唯一可以选择的集合是 `{7}`，删除后数组为空。

**约束条件**  
- `2 <= arr.length <= 10^5`  
- `arr.length` 为偶数  
- `1 <= arr[i] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可能的“要删掉的整数集合”都枚举一遍**，然后检查每个集合删掉后数组的长度是否 ≤ 原长度的一半，取满足条件的最小集合大小。  

- **数据结构**：我们可以把「要删掉的整数集合」用 Python 的 `set` 来表示，类似生活中把想要丢弃的物品放进一个篮子里。  
- **为什么正确**：因为我们枚举了**所有**可能的集合，只要其中有一个满足题目要求，就一定能找到最小的那个。  
- **时间/空间复杂度**：  
  - 枚举子集的个数是 `2^k`（`k` 为数组中不同整数的种类数），这在最坏情况下是指数级的。比如数组里有 20 种不同数字，子集就有 `2^20 ≈ 1,048,576` 种，已经远远超出 10⁵ 规模的时间限制。  
  - 对每个子集我们都要遍历整个数组统计被删掉的元素数，时间是 `O(n)`。于是整体时间是 `O(n * 2^k)`，在实际测试里会直接 TLE（超时）。  
  - 空间上只需要保存当前子集和计数，都是 `O(k)`，但因为时间已经不可接受，空间不是主要问题。  

> **大白话**：`O(n²)` 表示「如果 n 是 10，程序要跑 100 步」；而 `O(2^k)` 则是「如果 k 是 10，程序要跑 1024 步」，k 增加一点，步数就会翻倍，极快爆炸。

#### 代码（Python）

```python
from itertools import combinations
from collections import Counter
from typing import List

def min_set_bruteforce(arr: List[int]) -> int:
    n = len(arr)
    half = n // 2                     # 需要删除的最少元素个数
    freq = Counter(arr)               # 统计每个数出现的次数
    uniq = list(freq.keys())          # 不同的整数集合

    # 从 1 个元素的子集开始枚举，直到找到答案
    for size in range(1, len(uniq) + 1):
        # 组合库会返回所有 size 大小的子集
        for combo in combinations(uniq, size):
            removed = sum(freq[x] for x in combo)   # 这些数一共可以删除多少个元素
            if removed >= half:                     # 达到“至少删掉一半”
                return size                         # 第一次成功的 size 就是最小的
    return len(uniq)   # 理论上不会走到这里
```

> 这段代码可以跑通小规模的测试，但在 LeetCode 的数据范围（`arr.length` 可达 10⁵）下会直接超时。

#### 复杂度

- **时间复杂度**：`O(n * 2^k)`（指数级），其中 `k` 是不同整数的种类数。  
  - 实际上即使 `k` 只有 20，`2^k` 也已经是上万，乘以 `n`（最多 10⁵）更是天文数字。  
- **空间复杂度**：`O(k)`，用于存放不同整数及其出现次数的哈希表。  

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**枚举子集是最大的性能瓶颈**。我们需要一种办法，**直接挑选出最“能干”的整数**，而不是尝试所有组合。  

1. **统计频率**：先遍历一次数组，用哈希表（`dict` / `Counter`）统计每个整数出现的次数。  
   - 哈希表可以类比为「查字典」：键（key）是整数，值（value）是它在数组里出现的页码（次数）。查询、插入都是 `O(1)`，非常快。  
2. **把频率从大到小排序**（或使用最大堆）。因为**出现次数最多的整数**，一次就能删掉最多的元素，最有可能帮助我们快速达到“删掉一半”。  
   - 想象把所有整数的出现次数放进一个「装满糖果的盒子」里，糖果多的盒子（频率高）先吃，能最快把总糖果数减半。  
3. **贪心累计**：从频率最大的整数开始累计已经删除的元素个数，直到累计值 ≥ 原数组长度的一半。累计过程中使用的整数个数，就是答案。  
   - 这里的贪心是**安全的**：如果我们不先选出现次数最多的数，而是选一个次数更少的数，那么要达到同样的删除量，必然需要选更多的数，答案不会更小。  

**关键点**：  
- **为什么排序/堆能得到最优**？因为我们只关心“删掉多少”，而不是“具体删掉哪些”。最大频率的数一次就能贡献最多的删除量，贪心选择它们一定不会错。  
- **数据结构**：  
  - `Counter`（哈希表）统计频率。  
  - `sorted`（排序）或 `heapq`（最大堆）按频率从大到小取值。这里用排序更直观，时间复杂度相同且实现更简洁。  

#### 代码（Python）

```python
from collections import Counter
from typing import List

def min_set_optimal(arr: List[int]) -> int:
    n = len(arr)
    half = n // 2                     # 需要删除的最少元素个数

    # 1️⃣ 统计每个整数出现的次数（哈希表）
    freq = Counter(arr)               # 例如 {3:4, 5:3, 2:2, 7:1}

    # 2️⃣ 把出现次数取出来并从大到小排序
    counts = sorted(freq.values(), reverse=True)   # [4,3,2,1]

    # 3️⃣ 贪心累计删除的元素数量
    removed = 0        # 已经删除的元素总数
    ans = 0            # 选了多少种整数
    for c in counts:
        removed += c   # 加上当前整数的全部出现次数
        ans += 1       # 选了这个整数
        if removed >= half:   # 已经删掉至少一半
            break
    return ans
```

> 代码仅用了三行核心逻辑，关键行都加了中文注释，直接复制即可跑通 LeetCode。

#### 复杂度

- **时间复杂度**：`O(n + m log m)`  
  - `O(n)` 用于一次遍历统计频率（`n` 是数组长度）。  
  - `m` 是不同整数的种类数，`m ≤ n`。对频率数组 `counts` 排序的复杂度是 `O(m log m)`。在最坏情况下 `m = n = 10⁵`，`n log n` 仍然在 1 秒左右可以接受。  
  - 与暴力解的指数级 `O(n * 2^k)` 相比，**快了几个数量级**，在所有测试数据上都能顺利通过。  
- **空间复杂度**：`O(m)`  
  - 需要存放哈希表 `freq`（每种整数一条记录）和排好序的频率列表 `counts`。在最坏情况下 `m = n`，即最多占用约 10⁵ 个整数的空间，符合题目限制。

---

## 心得

- **核心技巧**：**统计频率 + 贪心挑选最大频率**。本题的关键在于把“删多少”转化为“选多少种数”，而最大频率的数最能“一举多得”。  
- **适用的题型**  
  1. *“移除数组中至少一半元素”*（本题）。  
  2. *“最少数量的字符使得字符串出现频率满足某条件”*（如 LeetCode 1796 “字符串中第一个出现两次的字符”）。  
  3. *“使用最少的硬币凑成目标金额”*（贪心在硬币面额满足特定条件时可行）。  
- **一句话总结**：**先把“价值”排好序，最大价值先拿——贪心永远不吃亏**。

---

## 反思

- **第一反应**：看到“删除一半”立刻想到“统计每个数出现次数”，因为只有出现次数决定了删多少。  
- **最容易踩的坑**  
  - **边界条件**：数组长度是偶数，但仍需使用 `half = n // 2`（整数除），否则可能少删一个导致答案错误。  
  - **频率相同的情况**：排序后顺序不影响答案，只要累计足够即可。  
  - **特殊情况**：全部元素相同时，只需要选 1 种数；全部元素都不相同时，需要选 `ceil(n/2)` 种数（因为每种只能删掉 1 个）。  
- **下次类似题的第一步**：**先把每个元素的“贡献值”（出现次数、权重等）统计出来并排序**，再根据目标（删多少、凑多少）进行贪心累计。这样往往能直接得到最优解。