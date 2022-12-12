# #2048. 下一个更大的数值平衡数 / Next Greater Numerically Balanced Number

> 难度：中等 · 标签：Hash Table、Math、Backtracking、Counting、Enumeration · [LeetCode 链接](https://leetcode.com/problems/next-greater-numerically-balanced-number/)

---

## 题目（英文原版）

**Description**

An integer x is numerically balanced if for every digit d in the number x, there are exactly d occurrences of that digit in x.
Given an integer n, return the smallest numerically balanced number strictly greater than n.

**Examples**

**Example 1:**

```
Input: n = 1
Output: 22
Explanation: 
22 is numerically balanced since:
- The digit 2 occurs 2 times. 
It is also the smallest numerically balanced number strictly greater than 1.
```

**Example 2:**

```
Input: n = 1000
Output: 1333
Explanation: 
1333 is numerically balanced since:
- The digit 1 occurs 1 time.
- The digit 3 occurs 3 times. 
It is also the smallest numerically balanced number strictly greater than 1000.
Note that 1022 cannot be the answer because 0 appeared more than 0 times.
```

**Example 3:**

```
Input: n = 3000
Output: 3133
Explanation: 
3133 is numerically balanced since:
- The digit 1 occurs 1 time.
- The digit 3 occurs 3 times.
It is also the smallest numerically balanced number strictly greater than 3000.
```

**Constraints**

- 0 <= n <= 106

---

## 题目（中文翻译）

**题目描述**  
如果整数 `x` 的每个数字 `d` 在 `x` 中恰好出现 `d` 次，则称 `x` 为数值平衡数（numerically balanced）。  
给定整数 `n`，返回严格大于 `n` 的最小数值平衡数。

**示例**

示例 1  
Input: n = 1  
Output: 22  
Explanation:  
22 是数值平衡数，因为：  
- 数字 2 出现了 2 次。  
它也是严格大于 1 的最小数值平衡数。

示例 2  
Input: n = 1000  
Output: 1333  
Explanation:  
1333 是数值平衡数，因为：  
- 数字 1 出现了 1 次。  
- 数字 3 出现了 3 次。  
它也是严格大于 1000 的最小数值平衡数。  
注意，1022 不能作为答案，因为数字 0 出现的次数大于 0 次。

示例 3  
Input: n = 3000  
Output: 3133  
Explanation:  
3133 是数值平衡数，因为：  
- 数字 1 出现了 1 次。  
- 数字 3 出现了 3 次。  
它也是严格大于 3000 的最小数值平衡数。

**约束条件**  
- 0 ≤ n ≤ 10^6

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**从 n+1 开始一直往后找**，每检查一个整数就判断它是不是 “数值平衡”。  
判断一个整数是否平衡只需要统计它每个数字出现的次数：

* 把整数拆成字符（比如 `1333 → ['1','3','3','3']`），用 **哈希表** 记下每个字符出现了几次。  
  - 哈希表可以类比成一本词典，**key** 是“单词”（这里是数字字符），**value** 是“页码”（这里是出现次数）。
* 对于出现过的每个数字 `d`（注意 `d` 是字符，需要转成整数），检查它的出现次数是否恰好等于 `d` 本身。  
  - 例如出现了两次的字符 `'2'`，因为 `2 == 2`，满足条件；如果出现了两次的 `'3'`，则不满足。  
* 另外，**0 不能出现**，因为如果出现了，按照定义它应该出现 0 次，显然不可能。

只要找到第一个满足条件的数，就是答案。

> **为什么这个方法一定能找到答案？**  
> 题目保证答案一定存在（比如 `99…9`，即 9 出现 9 次的 9 位数），而我们是从 `n+1` 按顺序遍历，必然会在某一步遇到它。

#### 代码（Python）

```python
from collections import Counter

def is_balanced(x: int) -> bool:
    """判断整数 x 是否满足数值平衡的定义"""
    s = str(x)                     # 把整数转成字符串，方便逐位统计
    cnt = Counter(s)               # 哈希表：统计每个字符出现的次数
    for ch, times in cnt.items():
        d = int(ch)                 # 把字符转成对应的数字
        if d == 0:                  # 0 不能出现
            return False
        if times != d:              # 出现次数必须恰好等于数字本身
            return False
    return True                    # 所有出现的数字都满足条件

def next_greater_balanced(n: int) -> int:
    """暴力搜索：从 n+1 起一直往后找第一个数值平衡的整数"""
    x = n + 1
    while True:
        if is_balanced(x):
            return x
        x += 1                      # 继续检查下一个整数
```

> 关键行解释  
> - `cnt = Counter(s)`：相当于查字典，把每个数字当作“词”，出现次数当作“页码”。  
> - `if times != d:`：检查“出现多少次”是否等于“这个数字本身”。  

#### 复杂度

- **时间复杂度**：`O(Δ * L)`  
  - `Δ` 是从 `n+1` 到答案之间的整数个数（最坏情况约几百万），  
  - `L` 是每个整数的位数（≤ 9），所以整体大致是线性扫描。  
  - 用大白话说，就是“我们可能要检查几百万个数字，每检查一个只看几位”，在题目给的 `n ≤ 10⁶` 范围内完全可以接受。

- **空间复杂度**：`O(1)`（不计输出）  
  - 只用了常数级的计数器和几个局部变量。

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于**逐个尝试**，尤其当 `n` 很大而下一个平衡数相距较远时，会检查很多无用的整数。  
我们可以利用“数值平衡”本身的**结构特征**来直接生成所有可能的平衡数，然后在这些数中挑出最小的、严格大于 `n` 的那个。

**关键观察**  

1. 若数字 `d` 出现在平衡数中，它必须出现 **恰好 `d` 次**。  
   - 这意味着每个出现的数字对应一段固定长度的字符块（比如数字 3 必须出现 3 次 “333”）。  
2. 平衡数的总位数等于**所有出现数字的和**。  
   - 例如 `1333` → `1` 出现 1 次，`3` 出现 3 次，位数 `1+3 = 4`。  
3. 题目限制 `n ≤ 10⁶`，即答案的位数最多 **7 位**（因为 10⁶ 有 7 位）。  
   - 实际上，最大的可能平衡数是 `9` 出现 `9` 次的 `7777777`（7 位）或 `999999999`（9 位），但 9 位数已经远超 `10⁶`，所以我们只需考虑 **位数 ≤ 7**。

基于上述观察，我们可以**枚举**所有合法的数字集合：

- 选取一个子集 `S ⊆ {1,2,…,9}`（决定哪些数字会出现）。  
- 对每个选中的数字 `d ∈ S`，把它复制 `d` 次，得到一段字符块。  
- 把所有块拼在一起，得到一个长度为 `sum(S)` 的字符序列。  
- 对这个序列进行**全排列**（去重），每一种排列对应一个不同的整数。  

因为 `|S| ≤ 7`，总长度 ≤ 7，枚举的规模非常小（所有可能的平衡数不到几千个），可以一次性生成、排序，然后用 **二分查找** 找到第一个大于 `n` 的数。

**核心算法**：**回溯（Backtracking） + 全排列**  
- 回溯负责枚举子集 `S`（即决定是否把数字 `d` 加入结果）。  
- 对于已经确定的数字块集合，使用计数方式生成所有唯一排列（类似“全排列去重”），这里利用 Python 的 `itertools.permutations` 结合 `set` 去重即可，因规模极小。

#### 代码（Python）

```python
from itertools import permutations
from typing import List

def generate_balanced_numbers(max_len: int = 7) -> List[int]:
    """
    生成所有位数不超过 max_len（默认 7）的数值平衡整数，返回排好序的列表。
    """
    results = set()                     # 用集合自动去重

    # 递归枚举每个数字是否出现（出现则加入 d 次）
    def backtrack(d: int, cur: List[str]):
        """
        d   : 当前考虑的数字（1~9）
        cur : 已经选好的字符块列表（每个块是字符 d 重复 d 次，例如 '333'）
        """
        if d == 10:                     # 已经考察完 1~9
            if not cur:                 # 空集合不构成合法整数
                return
            # 把所有块拼成一个字符串，再生成所有唯一排列
            whole = ''.join(cur)        # 例如 ['1', '333'] → '1333'
            for perm in set(permutations(whole)):
                num = int(''.join(perm))
                if len(str(num)) <= max_len:   # 位数限制
                    results.add(num)
            return

        # 情况一：不选数字 d
        backtrack(d + 1, cur)

        # 情况二：选数字 d（必须出现 d 次）
        # 只有当加入后总长度不超过 max_len 时才继续
        if len(''.join(cur)) + d <= max_len:
            backtrack(d + 1, cur + [str(d) * d])

    backtrack(1, [])
    return sorted(results)              # 从小到大排列，方便二分查找

# 预先生成一次（只会执行一次，开销很小）
BALANCED_LIST = generate_balanced_numbers()

def next_greater_balanced_opt(n: int) -> int:
    """在预生成的有序列表中二分找出第一个 > n 的数"""
    # 二分查找左侧第一个满足 > n 的位置
    lo, hi = 0, len(BALANCED_LIST)
    while lo < hi:
        mid = (lo + hi) // 2
        if BALANCED_LIST[mid] <= n:
            lo = mid + 1
        else:
            hi = mid
    return BALANCED_LIST[lo]           # lo 必然在范围内，因为列表里有足够大的数
```

> 关键行解释  
> - `if len(''.join(cur)) + d <= max_len:`：相当于在“背包”里放入 `d` 个重量为 `1` 的物品，防止总长度超过我们关心的上限。  
> - `set(permutations(whole))`：把所有排列去重，得到每一种不同的数字顺序。因为长度 ≤ 7，最多 `7! = 5040` 种排列，算力几乎为零。  
> - 二分查找的 `while lo < hi:` 循环确保我们在 **对数时间**（大约 `log2(几千)`）内定位答案。

#### 复杂度

- **预处理（一次性）**  
  - 枚举子集的次数是 `2⁹ = 512`（每个数字选或不选），每种子集最多产生 `7! = 5040` 种排列。  
  - 因此 **时间复杂度**约为 `O(512 * 5040) ≈ 2.5×10⁶`，在 Python 中几毫秒即可完成。  
  - **空间复杂度**：存储所有平衡数，数量 < 4000，约几 KB。

- **查询单次**  
  - 二分查找 `O(log K)`，`K` 为平衡数的总个数（约 4000），几乎是常数时间。  
  - 额外空间 `O(1)`。

> 与暴力解对比：  
> - 暴力解最坏要检查几百万个整数，时间随 `n` 与答案距离线性增长。  
> - 最优解把所有可能的答案提前算好，只需要 **对数时间** 就能得到结果，极大提升效率。

---

## 心得

- **核心技巧**：利用**数值平衡的结构特性**（每个出现的数字必须出现固定次数）把问题转化为**枚举有限集合**，再用**二分查找**快速定位答案。  
- **适用的题型**  
  1. “满足某种计数约束的数字”类（如 **回文数、数字翻转后仍是平方数** 等）。  
  2. “位数受限、组合数目有限” 的搜索题（如 **数字组合求和、满足特定频率的字母序列**）。  
- **解题钥匙**：**先从题目本身的约束入手，找出可以枚举的“小空间”，把搜索范围压到常数级**。

---

## 反思

- **第一反应**：直接从 `n+1` 开始暴力检查，思路最简单。  
- **最容易踩的坑**  
  - **0 的处理**：0 不能出现，否则出现次数不等于 0。  
  - **位数上限**：需要明确答案最大可能的位数，否则枚举时会产生无用的长数字。  
  - **去重**：在生成排列时，同一数字块可能导致重复排列，必须去重，否则会产生冗余的结果。  
- **下次遇到类似题**，第一步应该问自己：  
  1. “题目对数字的出现次数有没有硬性限制？”  
  2. “这些限制能否把搜索空间压到可以直接枚举的规模？”  
  3. “枚举完后如何快速定位答案（排序 + 二分）？”  

这样就能从暴力搜索迅速升级到结构化枚举的高效解法。