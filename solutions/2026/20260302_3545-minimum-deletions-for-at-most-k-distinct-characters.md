# #3545. 至多 K 种不同字符的最少删除次数 / Minimum Deletions for At Most K Distinct Characters

> 难度：简单 · 标签：Hash Table、String、Greedy、Sorting、Counting · [LeetCode 链接](https://leetcode.com/problems/minimum-deletions-for-at-most-k-distinct-characters/)

---

## 题目（英文原版）

**Description**

You are given a string s consisting of lowercase English letters, and an integer k.
Your task is to delete some (possibly none) of the characters in the string so that the number of distinct characters in the resulting string is at most k.
Return the minimum number of deletions required to achieve this.

**Examples**

**Example 1:**

```
Input: s = "abc", k = 2
Output: 1
Explanation:
```

**Example 2:**

```
Input: s = "aabb", k = 2
Output: 0
Explanation:
```

**Example 3:**

```
Input: s = "yyyzz", k = 1
Output: 2
Explanation:
```

**Constraints**

- 1 <= s.length <= 16
- 1 <= k <= 16
- s consists only of lowercase English letters.

---

## 题目（中文翻译）

给定一个仅包含小写英文字母的字符串 **s**，以及一个整数 **k**。  
你的任务是删除字符串中的若干字符（可以不删），使得得到的字符串中不同字符的种类数至多为 **k**。  
返回为实现该目标所需的最少删除次数。

**示例 1**  
输入: `s = "abc", k = 2`  
输出: `1`  
解释：

**示例 2**  
输入: `s = "aabb", k = 2`  
输出: `0`  
解释：

**示例 3**  
输入: `s = "yyyzz", k = 1`  
输出: `2`  
解释：

**约束条件**  
- `1 <= s.length <= 16`  
- `1 <= k <= 16`  
- `s` 仅由小写英文字母组成

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每一种可能的删除方式都穷举一遍**，然后找出满足「不同字符数 ≤ k」且删除字符最少的情况。

- **把字符串看成一排小盒子**，每个盒子里装着一个字符。我们可以决定每个盒子是「保留」还是「删除」。
- 所有可能的决定组合等价于 **2ⁿ**（n 为字符串长度）种情况，就像二进制数从 0 到 2ⁿ‑1 每一位代表「删」或「不删」。
- 对每一种组合，我们统计保留下来的字符有哪些、出现了多少种。如果种类 ≤ k，就把这次删除的字符数记下来，取最小值。

**为什么一定能得到正确答案？**  
因为我们没有遗漏任何一种删除方式，答案一定出现在所有组合的遍历中。

**时间/空间复杂度**  
- 时间复杂度：`O(2^n * n)`  
  - 解释：有 `2^n` 种子集，每种子集我们要遍历一次字符串（长度 n）来判断是否符合要求。  
  - 用大白话说，就是「如果字符串有 16 个字符，最多要检查 2^16 ≈ 65536 种情况，每种情况再看 16 次」，这在电脑里还是能跑完的（因为 n ≤ 16）。
- 空间复杂度：`O(1)`（只用常数级的计数器和几个临时变量）  

#### 代码（Python）

```python
from itertools import product

def min_deletions_brute(s: str, k: int) -> int:
    n = len(s)
    best = n                     # 最差情况：全部删光

    # 用 product 产生 0/1 序列，0 表示删除，1 表示保留
    for mask in product([0, 1], repeat=n):
        # 统计保留下来的字符出现次数
        freq = {}
        deletions = 0
        for i, keep in enumerate(mask):
            if keep:                       # 保留
                ch = s[i]
                freq[ch] = freq.get(ch, 0) + 1
            else:                          # 删除
                deletions += 1

        # 若不同字符种类 ≤ k，更新最小删除数
        if len(freq) <= k:
            best = min(best, deletions)

    return best
```

#### 复杂度

- **时间复杂度**：`O(2^n * n)`  
  - 这里的 `2^n` 表示所有可能的「删/不删」组合，`n` 是每次遍历字符串的代价。  
- **空间复杂度**：`O(1)`  
  - 只用了几个计数变量和一个小字典，大小不随 `n` 增长。

---

### 2. 最优解

#### 思路  

从暴力解出发，我们发现 **瓶颈在于枚举所有子集**，这随字符串长度呈指数增长。其实我们并不需要知道**具体删哪些字符**，只要知道**删多少字符**即可。

观察：

1. 只关心每个字符出现的次数（频率），而不关心它们在字符串中的位置。  
   - 这相当于把字符种类看成“商品”，出现次数看成“库存”。我们只需要决定保留哪些商品，库存多的保留，库存少的删除，能让种类数 ≤ k 并且删除的总数最少。

2. 若当前不同字符的种类数 `d` 已经 ≤ k，直接返回 0。  
   - 就像盒子里已经不超过 k 种商品，不用动。

3. 当 `d > k` 时，需要删除 `d - k` 种字符。  
   - 为了让删除的字符数最少，显然应该 **先删除出现次数最少的字符**（把最不值钱的商品清掉），因为每删掉一种字符就会把它全部的出现次数都删掉。

基于上述直觉，算法步骤如下：

1. **统计频率**：遍历一次字符串，记录每个字符出现了多少次。可以用 Python 的 `collections.Counter`（相当于“查字典”，key 是字符，value 是出现次数）。
2. **提取频率列表并升序排序**：把所有出现次数放进一个数组 `counts`，从小到大排列。排序好比把商品按“价值”从低到高排好队。
3. **计算需要删除的种类数** `need = distinct - k`。如果 `need ≤ 0`，直接返回 0。
4. **累加最小的 `need` 个频率**：把排在最前面的 `need` 个次数相加，就是最少需要删除的字符总数。

**为什么这样一定最优？**  
因为我们每一次删除的都是当前剩余字符中**出现次数最少**的那一种。假设有更优的方案不删除某个最少出现的字符，而是删除了出现次数更多的字符，那么我们可以把这两者调换——把少的删掉、把多的留下，删除总数会更小，矛盾。因此上述贪心策略必然得到最小删除数。

#### 代码（Python）

```python
from collections import Counter

def min_deletions_optimal(s: str, k: int) -> int:
    # 1. 统计每个字符的出现次数
    freq = Counter(s)                     # 哈希表：字符 → 次数
    distinct = len(freq)                  # 现有不同字符的种类数

    # 2. 已经满足要求，直接返回 0
    if distinct <= k:
        return 0

    # 3. 把出现次数取出来并升序排序（从少到多）
    counts = sorted(freq.values())        # 例如 [1,2,4,5]

    # 4. 需要删除的字符种类数
    need = distinct - k                   

    # 5. 累加最少的 need 个次数，即为最少删除的字符总数
    deletions = sum(counts[:need])
    return deletions
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - `O(n)` 用于一次遍历统计频率，`n` 为字符串长度（≤ 16）。  
  - `O(m log m)` 用于对出现次数列表排序，`m` 是不同字符的种类数，最多 26，故 `log m` 很小。整体上可以看作 `O(n log n)`，在本题的规模里几乎是线性时间。
- **空间复杂度**：`O(m)`  
  - 需要存放每个字符的计数，`m` 最多 26（小写字母），属于常数级空间。

---

## 心得

- **核心技巧**：**频率统计 + 贪心删除最少出现的字符**。  
  只要先把每种字符出现多少次算出来，再把次数最小的几种直接删掉，就能保证删除数最少。

- **适用的题型**  
  1. “删除字符使字符串满足某种约束”——如 *删除字符使字符串中不超过 k 种不同字符*。  
  2. “保留出现次数最多的 k 种元素”——如 *出现次数最多的 k 个字母*。  
  3. “最小化删除/添加使出现次数满足某个阈值”——如 *删除最少字符使所有字符出现次数 ≤ limit*。

- **一句话总结**：**先算频率，删掉最不值钱的字符种类，最少删除即是答案。**

---

## 反思

- **第一反应**：看到「删除」和「不同字符数 ≤ k」就想到「统计每种字符出现多少次」；如果直接想暴力，会想到枚举子集，但会意识到指数级太慢（虽然本题 n 很小）。
- **最容易踩的坑**  
  1. **忘记先判断 `distinct <= k`**，直接去排序会导致 `need` 为负数，引发错误。  
  2. **误把字符的总出现次数相加**（比如把所有次数都相加）而不是只取最少的 `need` 种。  
  3. **边界条件**：`k = 0`（需要把所有字符都删掉）以及 `k >= distinct`（不需要删）都要正确处理。

- **下次遇到同类题**，第一步应该想到 **“先统计频率，再用贪心挑选要删/保留的种类”**，这往往能把指数级的搜索压缩到 `O(n log n)` 或更低。