# #1157. 在线子数组多数元素 / Online Majority Element In Subarray

> 难度：困难 · 标签：Array、Binary Search、Design、Binary Indexed Tree、Segment Tree · [LeetCode 链接](https://leetcode.com/problems/online-majority-element-in-subarray/)

---

## 题目（英文原版）

**Description**

Design a data structure that efficiently finds the majority element of a given subarray.
The majority element of a subarray is an element that occurs threshold times or more in the subarray.
Implementing the MajorityChecker class:

**Examples**

**Example 1:**

```
Input
["MajorityChecker", "query", "query", "query"]
[[[1, 1, 2, 2, 1, 1]], [0, 5, 4], [0, 3, 3], [2, 3, 2]]
Output
[null, 1, -1, 2]

Explanation
MajorityChecker majorityChecker = new MajorityChecker([1, 1, 2, 2, 1, 1]);
majorityChecker.query(0, 5, 4); // return 1
majorityChecker.query(0, 3, 3); // return -1
majorityChecker.query(2, 3, 2); // return 2
```

**Constraints**

- 1 <= arr.length <= 2 * 104
- 1 <= arr[i] <= 2 * 104
- 0 <= left <= right < arr.length
- threshold <= right - left + 1
- 2 * threshold > right - left + 1
- At most 104 calls will be made to query.

---

## 题目（中文翻译）

设计一个数据结构，能够高效地查询给定子数组（subarray）的多数元素（majority element）。  
子数组的多数元素是指在该子数组中出现次数不少于 **threshold** 次的元素。

实现 `MajorityChecker` 类，使其支持如下操作：

```java
MajorityChecker(int[] arr)   // 构造函数，传入初始数组
int query(int left, int right, int threshold) // 查询区间 [left, right]（含）内是否存在出现次数 ≥ threshold 的元素，若存在返回该元素，否则返回 -1
```

**示例 1**

```text
输入
["MajorityChecker", "query", "query", "query"]
[[[1, 1, 2, 2, 1, 1]], [0, 5, 4], [0, 3, 3], [2, 3, 2]]

输出
[null, 1, -1, 2]

解释
MajorityChecker majorityChecker = new MajorityChecker([1, 1, 2, 2, 1, 1]);
majorityChecker.query(0, 5, 4); // 返回 1，因为元素 1 在下标 0~5 的子数组中出现 4 次
majorityChecker.query(0, 3, 3); // 返回 -1，因为在子数组 [1, 1, 2, 2] 中不存在出现 ≥3 次的元素
majorityChecker.query(2, 3, 2); // 返回 2，因为元素 2 在子数组 [2, 2] 中出现 2 次
```

**约束条件**

- `1 <= arr.length <= 2 * 10^4`
- `1 <= arr[i] <= 2 * 10^4`
- `0 <= left <= right < arr.length`
- `threshold <= right - left + 1`
- `2 * threshold > right - left + 1`（即阈值大于子数组长度的一半）
- 最多会调用 `query` 方法 `10^4` 次。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**把子数组完整遍历一遍**，统计每个数出现了多少次，然后看看有没有哪个数的出现次数 ≥ `threshold`。  

- **使用的数据结构**：  
  - `defaultdict(int)`（相当于我们平时用的“记事本”，键是数字，值是出现的次数）。  
  - 用 **列表** 保存子数组里的所有元素，就像把一段文字全部抄下来再去数字一样。

- **为什么正确**：  
  我们把子数组里每个位置的数字都记下来，统计它们的出现次数。只要有一个数字的次数满足题目要求，我们就一定能找出来。  

- **时间/空间复杂度**：  
  - **时间**：对每一次查询，都要把 `[left, right]` 区间的所有元素遍历一遍。区间长度记作 `m = right‑left+1`，所以时间是 **O(m)**。如果把 `m` 看成 `n`（数组最大长度），就是 **O(n)**。  
  - **空间**：额外的哈希表最多保存 `m` 种不同的数字，最坏情况下每个数字都不相同，所以是 **O(m)**，即 **O(n)**。  

> 大白话：  
> - **O(n)** 就像说“和数组里每个元素都聊一次”，如果数组有 10 000 个元素，你得花 10 000 步。  
> - **O(1)** 则是“一步就搞定”，和这里的暴力解完全不一样。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

class MajorityChecker:
    def __init__(self, arr: List[int]):
        self.arr = arr                      # 把数组原封不动保存下来

    def query(self, left: int, right: int, threshold: int) -> int:
        cnt = defaultdict(int)              # 记事本：记录每个数出现的次数
        # 把子数组全部抄下来并统计
        for i in range(left, right + 1):
            num = self.arr[i]
            cnt[num] += 1
            if cnt[num] >= threshold:       # 只要一次达到阈值就可以返回
                return num
        return -1                            # 没有满足条件的数
```

#### 复杂度

- **时间复杂度**：`O(right - left + 1)` → 最坏 `O(n)`。  
  > 意味着每次查询都要“走一遍”子数组的所有元素。

- **空间复杂度**：`O(right - left + 1)` → 最坏 `O(n)`。  
  > 需要额外的哈希表来存放子数组里出现的不同数字。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次查询都要遍历完整的子数组**。我们需要把查询时间压到 **对数级别**，甚至 **常数级**（不计入常数因子）。  

观察题目给出的 **两条重要限制**：

1. `2 * threshold > right - left + 1`  
   → 只要有“多数元素”，它出现的次数 **严格超过子数组长度的一半**。  
2. `threshold ≤ right - left + 1`（显然）  

这正好对应 **“多数元素”** 的定义：出现次数 > 子数组长度 / 2。  
**多数元素的特殊性**：如果我们随机挑选子数组里的一个位置，它恰好是多数元素的概率 > 50%。  

**核心思路**：  
- **预处理**：把每个数字出现的所有下标收集起来，存到哈希表 `pos_map` 中。下标列表是 **有序的**，可以用二分查找快速统计某个数字在 `[left, right]` 区间出现了多少次（相当于在一本字典里查“页码”）。  
- **查询时随机抽样**：在 `[left, right]` 区间随机挑选若干个下标（经验上 20 次已经足够把“未命中概率”压到几乎 0），每次取出对应的数字 `candidate`，再用二分查找在 `pos_map[candidate]` 中统计它出现的次数。如果次数 ≥ `threshold`，直接返回 `candidate`。如果全部抽样都没有满足，则返回 `-1`。  

> **为什么随机抽样可以保证正确性？**  
> - 假设子数组里真的存在多数元素 `M`，它占了 > 50% 的位置。  
> - 随机抽一次命中 `M` 的概率 > 0.5。  
> - 抽 `k` 次都不命中的概率是 `(1 - p)^k ≤ (0.5)^k`。取 `k = 20`，概率约为 `1/1,048,576`，几乎可以忽略不计。  

**数据结构细节**  

| 数据结构 | 类比 | 作用 |
|----------|------|------|
| `defaultdict(list) pos_map` | **字典**：词典里查“词”，这里查“数字”。每个词对应的**页码列表**就是该数字出现的下标集合。 | 快速定位某个数字的所有出现位置，支持二分查找。 |
| `bisect_left / bisect_right`（二分搜索） | **在有序的页码表里找范围**：像在排好序的书签里找某一段页码。 | 在 `pos_map[x]` 中统计 `x` 在 `[left, right]` 之间出现了几次，时间 `O(log n)`。 |

#### 代码（Python）

```python
import random
import bisect
from collections import defaultdict
from typing import List

class MajorityChecker:
    def __init__(self, arr: List[int]):
        self.arr = arr
        # 预处理：把每个数字出现的下标全部收集起来，保持有序
        self.pos_map = defaultdict(list)          # key: 数字，value: 该数字出现的下标列表（升序）
        for idx, num in enumerate(arr):
            self.pos_map[num].append(idx)

    def _count_in_range(self, num: int, left: int, right: int) -> int:
        """利用二分查找统计 num 在 [left, right] 之间出现的次数"""
        pos_list = self.pos_map[num]              # 已经排好序的下标列表
        # 左边界：第一个 >= left 的位置
        l = bisect.bisect_left(pos_list, left)
        # 右边界：第一个 > right 的位置
        r = bisect.bisect_right(pos_list, right)
        return r - l                               # 区间内元素个数

    def query(self, left: int, right: int, threshold: int) -> int:
        # 随机抽样的次数（经验值 20 足够把错误概率压到几乎 0）
        for _ in range(20):
            # 随机选一个下标，范围必须在 [left, right] 之内
            rand_idx = random.randint(left, right)
            candidate = self.arr[rand_idx]         # 这个下标对应的数字是候选者

            # 统计 candidate 在子数组中的出现次数（二分搜索，O(log n)）
            occ = self._count_in_range(candidate, left, right)
            if occ >= threshold:                  # 满足阈值直接返回
                return candidate

        # 经过多次抽样仍未找到，说明不存在多数元素
        return -1
```

**代码要点解释**  

1. `self.pos_map` 的构建只做一次，时间 `O(n)`，空间 `O(n)`（每个下标都要存）。  
2. `_count_in_range` 用 **二分** 找左、右边界，时间 `O(log k)`，其中 `k` 是该数字出现的次数（最坏 `O(log n)`）。  
3. `query` 循环 20 次，每次随机挑选下标 → **期望时间** `20 * O(log n)` → 实际上是 **O(log n)**。  

#### 复杂度

- **时间复杂度**：  
  - 预处理一次 `O(n)`（建哈希表）。  
  - 每次查询 `O(20·log n) = O(log n)`。  
    > 与暴力解的 `O(n)` 相比，查询速度快了 **数十倍**（对数 vs 线性）。  

- **空间复杂度**：`O(n)`。  
  - 需要保存每个元素的下标列表，总共 `n` 个下标，和原数组大小相同级别。  

> 与暴力解对比：  
> - 暴力解每次查询都要 `O(n)` 时间且 `O(n)` 额外空间。  
> - 最优解把查询时间降到 `O(log n)`，只在初始化时花 `O(n)` 空间和时间，后续查询极快。

---

## 心得

- **核心技巧**：**随机抽样 + 位置哈希表 + 二分计数**。  
- **适用的题型**（类似思路）  
  1. **“子数组中出现次数超过阈值的元素”**（如 LeetCode 1157 – Online Majority Element In Subarray）。  
  2. **“区间中出现次数最多的元素”**（使用莫尔投票 + 线段树做候选）。  
  3. **“区间随机抽样求近似答案”**（如随机选点估计中位数、众数等）。  

- **一句话总结解题钥匙**：  
  > **“多数元素占据 > 50% → 随机一次命中概率 > 0.5，配合快速计数即可在对数时间内确定答案。”**

---

## 反思

- **第一反应**：直接遍历子数组、统计频次——最直观但最慢。  
- **最容易踩的坑**  
  - **随机数范围**：一定要在 `[left, right]` 之间，否则抽到无关位置会导致错误计数。  
  - **二分计数边界**：`bisect_left` 找的是 “≥ left”，`bisect_right` 找的是 “> right”，两者相减才是出现次数。忘记 `right` 要用 `> right` 会少算一次。  
  - **阈值验证**：即使抽到多数元素，也必须再次 **确认** 它的出现次数 ≥ `threshold`，因为题目只要求 “出现至少 threshold 次”，而非严格多数。  

- **下次遇到同类题**，第一步应该想到：  
  > **“有没有利用元素出现频率的统计特性（如 > ½）来做概率抽样或投票？”**  
  如果能把“出现次数”转化为“位置列表 + 二分”，再配合随机抽样，就往最优解的方向迈进了。