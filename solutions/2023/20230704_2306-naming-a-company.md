# #2306. 命名公司 / Naming a Company

> 难度：困难 · 标签：Array、Hash Table、String、Bit Manipulation、Enumeration · [LeetCode 链接](https://leetcode.com/problems/naming-a-company/)

---

## 题目（英文原版）

**Description**

You are given an array of strings ideas that represents a list of names to be used in the process of naming a company. The process of naming a company is as follows:
Return the number of distinct valid names for the company.

**Examples**

**Example 1:**

```
Input: ideas = ["coffee","donuts","time","toffee"]
Output: 6
Explanation: The following selections are valid:
- ("coffee", "donuts"): The company name created is "doffee conuts".
- ("donuts", "coffee"): The company name created is "conuts doffee".
- ("donuts", "time"): The company name created is "tonuts dime".
- ("donuts", "toffee"): The company name created is "tonuts doffee".
- ("time", "donuts"): The company name created is "dime tonuts".
- ("toffee", "donuts"): The company name created is "doffee tonuts".
Therefore, there are a total of 6 distinct company names.

The following are some examples of invalid selections:
- ("coffee", "time"): The name "toffee" formed after swapping already exists in the original array.
- ("time", "toffee"): Both names are still the same after swapping and exist in the original array.
- ("coffee", "toffee"): Both names formed after swapping already exist in the original array.
```

**Example 2:**

```
Input: ideas = ["lack","back"]
Output: 0
Explanation: There are no valid selections. Therefore, 0 is returned.
```

**Constraints**

- 2 <= ideas.length <= 5 * 104
- 1 <= ideas[i].length <= 10
- ideas[i] consists of lowercase English letters.
- All the strings in ideas are unique.

---

## 题目（中文翻译）

**描述**  
给定一个字符串数组 `ideas`，其中每个字符串代表在给公司命名过程中可能使用的名称。命名公司的过程如下：

- 选取两个不同的字符串 `a` 与 `b`（顺序不固定）。
- 交换它们的首字母，得到新的字符串 `a'` 与 `b'`。  
  例如，`a = "coffee"`、`b = "donuts"`，交换首字母后得到 `a' = "doffee"`、`b' = "conuts"`。
- 如果 **两个** 新字符串 `a'` 与 `b'` 都不在原数组 `ideas` 中，则这一次选取是 **有效的**，并且可以生成两种不同的公司名称（`a' b'` 与 `b' a'`）。

返回所有可能的 **不同的有效名称** 的数量。

---

**示例 1**  
```
Input: ideas = ["coffee","donuts","time","toffee"]
Output: 6
Explanation: 以下选取是有效的：
- ("coffee", "donuts"): 生成的公司名称是 "doffee conuts"。
- ("donuts", "coffee"): 生成的公司名称是 "conuts doffee"。
- ("donuts", "time"):   生成的公司名称是 "tonuts dime"。
- ("donuts", "toffee"): 生成的公司名称是 "tonuts doffee"。
- ("time", "donuts"):   生成的公司名称是 "dime tonuts"。
- ("toffee", "donuts"): 生成的公司名称是 "doffee tonuts"。
```

**示例 2**  
```
Input: ideas = ["lack","back"]
Output: 0
Explanation: 没有任何有效的选取，因此返回 0。
```

---

**约束条件**
- $2 \leq \text{ideas.length} \leq 5 \times 10^4$
- $1 \leq \text{ideas}[i].\text{length} \leq 10$
- `ideas[i]` 只包含小写英文字母。
- `ideas` 中的所有字符串互不相同。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是**枚举所有两两组合**，把每一对字符串的首字母互换后检查是否仍然不在原数组里。  

- **数据结构**：  
  - 用 `set` 把所有原始名字存起来，类似于查字典时的“词典”。`set` 的查询时间是 **O(1)**，相当于在字典里直接翻到对应页码。  
  - 用两层循环遍历所有有序对 `(i, j)`，即把每个字符串当作「左」和「右」各自尝试一次。  

- **为什么正确**：  
  - 只要遍历了所有可能的有序对，并且对每对都做了「换首字母」的检验，就不会漏掉任何合法的名字组合。  

- **复杂度大白话**：  
  - **时间**：外层循环 `n` 次，内层循环最多 `n‑1` 次，每次都要生成两个新字符串（长度最多 10）并在 `set` 中查找，时间大约是 `n × n = n²`。如果把 `n²` 用大白话解释，就是“如果有 10,000 个名字，需要检查大约一亿次”。  
  - **空间**：除了保存原始 `set`（需要 `n` 个字符串），不需要额外的大结构，空间是 **O(n)**。  

#### 代码（Python）  

```python
from typing import List

def distinctNames_brute(ideas: List[str]) -> int:
    # 把所有原始名字放进集合，查询相当于查字典
    idea_set = set(ideas)
    n = len(ideas)
    ans = 0

    # 两层循环遍历所有有序对 (i, j)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue          # 不能和自己配对

            a, b = ideas[i], ideas[j]
            # 交换首字母得到新名字
            new_a = b[0] + a[1:]
            new_b = a[0] + b[1:]

            # 两个新名字都不在原集合里，才算合法
            if new_a not in idea_set and new_b not in idea_set:
                ans += 1

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n² * L)`  
  - `n²` 是两层循环的次数，`L`（≤10）是生成新字符串的代价。  
  - 大白话：如果有 5 万个名字，暴力解根本跑不完。  

- **空间复杂度**：`O(n)`  
  - 只用了一个 `set` 来存原始名字。  

---  

### 2. 最优解  

#### 思路  

从暴力解出发，**瓶颈**在于「两层循环」导致的 `n²` 次检查。我们需要把**比较次数从 `n²` 降到接近 `n`**。  

关键观察：

1. **把名字按「除去首字母的其余部分」分组**  
   - 例如 `"coffee"` → 尾部 `"offee"`，`"toffee"` → 同样的尾部 `"offee"`。  
   - 同一组里的两个名字**换首字母后一定会产生冲突**（因为尾部相同），所以同组内部的配对全部**不合法**，可以直接忽略。  

2. **每组只关心出现了哪些首字母**  
   - 对于同一尾部 `"offee"`，可能出现的首字母有 `c、t、d …`。  
   - 把这 26 个可能的首字母用 **26 位二进制掩码**（bitmask）记录下来。  
   - 把掩码想象成「字典的页码表」，第 `k` 位是 1 表示第 `k` 个字母（`'a'+k`）在这个组里出现过。  

3. **跨组配对的合法性**  
   - 设有两组 `G1`、`G2`，对应的掩码分别为 `mask1、mask2`，大小分别为 `cnt1、cnt2`。  
   - 只有当 **首字母在另一组里没有出现** 时，换首字母才不会生成已经存在的名字。  
   - `mask1 & mask2` 表示两组都出现的首字母（公共位），这些字母导致的配对是**非法**的。  
   - 对于 `G1` 中的每个合法首字母（不在公共位），它可以和 `G2` 中所有 **不在公共位** 的首字母配对。  
   - 计数公式：`valid_pairs = (cnt1 - common) * (cnt2 - common) * 2`  
     - `common = popcount(mask1 & mask2)` 表示公共字母的数量。  
     - 乘以 `2` 是因为有序对 `(i, j)` 和 `(j, i)` 都算。  

4. **遍历所有组的组合**  
   - 组的数量最多是 `n`（每个名字尾部都不相同），但我们只需要两层遍历 **组**，而不是 **名字**。  
   - 组数远小于 `n`，而且每次计算只用了位运算和常数时间，整体复杂度 **接近 O(n·L)**。  

#### 代码（Python）  

```python
from typing import List
from collections import defaultdict

def distinctNames(ideas: List[str]) -> int:
    """
    统计所有合法的有序名字对数。
    思路：按去掉首字母的后缀分组，每组记录出现的首字母集合（用 26 位掩码）。
    再遍历组间组合，利用位运算快速统计合法配对。
    """
    # 1. 统计每个后缀对应的首字母掩码以及该组的大小
    suffix_mask = defaultdict(int)   # suffix -> 26 位掩码
    suffix_cnt  = defaultdict(int)   # suffix -> 组内元素个数

    for w in ideas:
        first = ord(w[0]) - ord('a')          # 0~25
        suffix = w[1:]                       # 去掉首字母的后缀
        suffix_mask[suffix] |= 1 << first    # 把对应位设为 1
        suffix_cnt[suffix] += 1

    # 把字典的键取出来，方便后面两层遍历
    suffixes = list(suffix_mask.keys())
    m = len(suffixes)

    ans = 0
    # 2. 两层遍历不同的后缀组（只需要遍历 i < j 的组合）
    for i in range(m):
        mask_i = suffix_mask[suffixes[i]]
        cnt_i  = suffix_cnt[suffixes[i]]
        for j in range(i + 1, m):
            mask_j = suffix_mask[suffixes[j]]
            cnt_j  = suffix_cnt[suffixes[j]]

            # 公共首字母的位数（即两组都出现的首字母）
            common = bin(mask_i & mask_j).count('1')   # popcount

            # 两组各自去掉这些公共字母后，剩余的合法配对数
            valid_i = cnt_i - common      # G1 中可以和 G2 配对的元素数
            valid_j = cnt_j - common      # G2 中可以和 G1 配对的元素数

            ans += valid_i * valid_j * 2   # 乘 2 计有序对

    return ans
```

> **代码要点解释**（中文注释已经写在代码里），这里再用生活化的比喻说明：  
> - **后缀组**就像把所有“同款衣服的剩余部分”放在一起，只看它们的“颜色标签”。  
> - **掩码**像一本“颜色手册”，每一页（第 `k` 位）记录是否出现过第 `k` 种颜色。  
> - 两本手册的交集（`mask_i & mask_j`）告诉我们“这两批衣服都有的颜色”，这些颜色的配对会产生冲突，必须排除。  

#### 复杂度  

- **时间复杂度**：`O(n·L + g²·26)`，其中  
  - `n·L` 是遍历所有名字并提取后缀的代价（`L ≤ 10`），几乎是线性。  
  - `g` 是不同后缀的数量，最坏情况下 `g = n`，但每次内部计算只用了 **位运算**（常数 26），所以整体仍是 **≈ O(n·L)**。  
  - 用大白话说：即使有 5 万个名字，也只会跑几百万次轻量的位操作，能够在一秒内结束。  

- **空间复杂度**：`O(g)`，存储每个后缀的掩码和计数。最坏 `g = n`，即 `O(n)`。  

---  

## 心得  

- **核心技巧**：把字符串的「公共部分」抽出来分组，再用 **位掩码**（bitmask）快速统计每组出现的首字母集合。  
- **适用的题型**  
  1. 按「去掉首字符」或「去掉某一固定位置」分组的字符串配对问题（如 “Maximum Matching of Prefix/Suffix”）。  
  2. 需要统计不同集合之间「没有交集」的配对数时（如 “Number of Good Pairs”）。  
- **一句话总结**：**把相同后缀的名字归为一组，用 26 位二进制记录出现的首字母，组间配对只需排除公共首字母即可**。  

---  

## 反思  

- **第一反应**：直接双循环暴力枚举，代码写得很快，但会超时。  
- **最容易踩的坑**  
  - 忽略了「有序对」的计数，需要乘以 2。  
  - 只考虑了不同后缀之间的配对，却忘记排除同组内部的配对（它们一定非法）。  
  - 位掩码要使用 `int` 并确保只保留 26 位，防止误用更大范围的位运算。  
- **下次遇到同类题**：第一步先 **看能否把元素按照不变的“公共子结构”分组**，再 **用集合或位掩码把变动的那一部分压缩**，这样就能把 `O(n²)` 的比较压缩到 `O(n)` 级别。