# #1630. 等差子数组 / Arithmetic Subarrays

> 难度：中等 · 标签：Array、Hash Table、Sorting · [LeetCode 链接](https://leetcode.com/problems/arithmetic-subarrays/)

---

## 题目（英文原版）

**Description**

A sequence of numbers is called arithmetic if it consists of at least two elements, and the difference between every two consecutive elements is the same. More formally, a sequence s is arithmetic if and only if s[i+1] - s[i] == s[1] - s[0] for all valid i.
For example, these are arithmetic sequences:
The following sequence is not arithmetic:
You are given an array of n integers, nums, and two arrays of m integers each, l and r, representing the m range queries, where the ith query is the range [l[i], r[i]]. All the arrays are 0-indexed.
Return a list of boolean elements answer, where answer[i] is true if the subarray nums[l[i]], nums[l[i]+1], ... , nums[r[i]] can be rearranged to form an arithmetic sequence, and false otherwise.

**Examples**

**Example 1:**

```
1, 3, 5, 7, 9
7, 7, 7, 7
3, -1, -5, -9
```

**Example 2:**

```
1, 1, 2, 5, 7
```

**Example 3:**

```
Input: nums = [4,6,5,9,3,7], l = [0,0,2], r = [2,3,5]
Output: [true,false,true]
Explanation:
In the 0th query, the subarray is [4,6,5]. This can be rearranged as [6,5,4], which is an arithmetic sequence.
In the 1st query, the subarray is [4,6,5,9]. This cannot be rearranged as an arithmetic sequence.
In the 2nd query, the subarray is [5,9,3,7]. This can be rearranged as [3,5,7,9], which is an arithmetic sequence.
```

**Example 4:**

```
Input: nums = [-12,-9,-3,-12,-6,15,20,-25,-20,-15,-10], l = [0,1,6,4,8,7], r = [4,4,9,7,9,10]
Output: [false,true,false,false,true,true]
```

**Constraints**

- n == nums.length
- m == l.length
- m == r.length
- 2 <= n <= 500
- 1 <= m <= 500
- 0 <= l[i] < r[i] < n
- -105 <= nums[i] <= 105

---

## 题目（中文翻译）

**描述**  
如果一个数列至少包含两个元素，并且任意两个相邻元素之间的差值都相同，则称该数列为等差数列（arithmetic sequence）。更形式化地说，数列 `s` 为等差数列当且仅当对所有有效的 `i` 都满足 `s[i+1] - s[i] == s[1] - s[0]`。  

例如，以下数列都是等差数列：  
（此处省略具体示例）  

下面的数列不是等差数列：  
（此处省略具体示例）  

给定一个长度为 `n` 的整数数组 `nums`，以及两个长度为 `m` 的整数数组 `l` 和 `r`，它们表示 `m` 个区间查询，其中第 `i` 个查询的区间为 `[l[i], r[i]]`（所有数组均为 0‑索引）。  

返回一个布尔数组 `answer`，其中 `answer[i]` 为 `true` 当且仅当子数组 `nums[l[i]], nums[l[i]+1], ..., nums[r[i]]` **可以重新排列** 成等差数列，否则为 `false`。

---

**示例 1**  

等差数列示例：  
```
1, 3, 5, 7, 9
7, 7, 7, 7
3, -1, -5, -9
```

---

**示例 2**  

非等差数列示例：  
```
1, 1, 2, 5, 7
```

---

**示例 3**  

```text
Input: nums = [4,6,5,9,3,7], l = [0,0,2], r = [2,3,5]
Output: [true,false,true]
Explanation:
- 在第 0 个查询中，子数组为 [4,6,5]。将其重新排列为 [6,5,4] 后可以得到等差数列。
- 在第 1 个查询中，子数组为 [4,6,5,9]。无法重新排列成等差数列。
- 在第 2 个查询中，子数组为 [5,9,3,7]。将其重新排列为 [3,5,7,9] 后得到等差数列。
```

---

**示例 4**  

```text
Input: nums = [-12,-9,-3,-12,-6,15,20,-25,-20,-15,-10], l = [0,1,6,4,8,7], r = [4,4,9,7,9,10]
Output: [false,true,false,false,true,true]
```

---

**约束条件**  

- `n == nums.length`
- `m == l.length`
- `m == r.length`
- `2 <= n <= 500`
- `1 <= m <= 500`
- `0 <= l[i] < r[i] < n`
- `-10^5 <= nums[i] <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每一次查询的子数组取出来，排个序，再检查相邻差是否相等**。  

- **取子数组**：把 `nums[l[i] … r[i]]` 直接切片得到一个新的列表。  
- **排序**：把切出来的列表用 Python 的 `sorted` 排序。可以把排序想象成把一堆散乱的书按照高度从矮到高摆好，排好序后我们就能“一眼看出”相邻的差是否相同。  
- **检查等差**：遍历排好序的列表，计算相邻两个数的差，如果全部相同，则说明可以重新排列成等差数列（因为已经是最小‑最大排列）。  

> **为什么这样就对了？**  
> 如果一组数能够排列成等差数列，那么把它们从小到大排好后，必然也是等差的——等差数列的顺序唯一（只要固定首项和公差），所以只要排好序后相邻差相同，就一定可以得到原题要求的排列。  

**复杂度大概是怎样的？**  
- 对每个查询我们都要 **排序**，排序的时间是 `O(k log k)`（k 为子数组长度）。  
- 再遍历一次检查差值，时间是 `O(k)`，这在大 O 记号里被 `O(k log k)` 吞掉。  
- 空间上我们需要额外的列表保存排序后的子数组，大小是 `O(k)`。  

#### 代码（Python）

```python
from typing import List

def checkArithmeticSubarrays(nums: List[int],
                             l: List[int],
                             r: List[int]) -> List[bool]:
    ans = []
    for left, right in zip(l, r):
        # 1. 取出子数组
        sub = nums[left:right + 1]               # 包含右端点
        # 2. 排序
        sub.sort()                               # 原地排序，等价于 sorted(sub)
        # 3. 检查等差
        if len(sub) < 2:                         # 题目保证长度≥2，这里防御性写法
            ans.append(False)
            continue
        diff = sub[1] - sub[0]                   # 首个差值
        ok = True
        for i in range(2, len(sub)):
            if sub[i] - sub[i - 1] != diff:      # 只要有一个不等就不行
                ok = False
                break
        ans.append(ok)
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(m * k log k)`  
  - `m` 为查询次数，`k` 为每次子数组的长度（最坏情况是 `n`）。  
  - 用大白话说，就是“每一次查询都要先把那段数字排好序，排的过程比直接遍历慢一点”。  

- **空间复杂度**：`O(k)`（额外的排序数组）  
  - 只需要临时存放当前子数组，最多和原数组一样大。  

---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在**排序**——排序本身是 `O(k log k)`，而我们其实只需要判断**是否可以组成等差数列**，不一定要把它们排好序。  

观察等差数列的两个关键属性：

1. **最小值** 与 **最大值** 已知后，公差 `d` 必须满足  
   \[
   d = \frac{max - min}{len-1}
   \]  
   （因为等差数列的首项是 `min`，末项是 `max`，之间有 `len-1` 段相同的差）。  
2. **每个元素都唯一** 并且 **恰好落在等差格子上**：  
   对于任意元素 `x`，`(x - min) % d` 必须为 `0`，并且 `x` 只能出现一次（否则会冲突）。

因此我们可以 **在 O(k) 时间内** 完成检查：

- 先遍历一次子数组，得到 `min`、`max`、以及子数组的长度 `len`。  
- 计算公差 `d`，如果 `(max - min) % (len-1) != 0`，直接返回 `False`（因为差不是整数，根本不可能是等差）。  
- 再遍历一次子数组，用一个 **哈希表**（Python 的 `set`）记录已经出现的数。  
  - 对每个数 `x`，检查 `(x - min) % d == 0`，如果不满足，返回 `False`。  
  - 同时检查 `x` 是否已经出现过，出现两次也返回 `False`。  

> **类比**：哈希表就像一本词典，`key` 是单词（这里是数值），`value` 是是否已经出现过的标记。查找一个单词的页码（是否出现）只需要 O(1) 时间，就像我们在字典里快速查到答案。  

这样每个查询只需要 **两次线性遍历**，没有排序，时间降到了 `O(k)`，空间只需要一个 `set`，最坏 `O(k)`。

#### 代码（Python）

```python
from typing import List

def checkArithmeticSubarrays(nums: List[int],
                             l: List[int],
                             r: List[int]) -> List[bool]:
    ans = []
    for left, right in zip(l, r):
        sub = nums[left:right + 1]          # 取子数组
        length = len(sub)

        # 1️⃣ 找最小值、最大值
        mn = min(sub)
        mx = max(sub)

        # 2️⃣ 计算公差，先判断能否整除
        if (mx - mn) % (length - 1) != 0:   # 不能整除，必不是等差
            ans.append(False)
            continue
        d = (mx - mn) // (length - 1)       # 整数公差

        # 3️⃣ 用集合检查唯一性和“落在格子上”
        seen = set()
        ok = True
        for x in sub:
            # 必须能被公差整除到格子上
            if (x - mn) % d != 0:
                ok = False
                break
            # 不能出现两次
            if x in seen:
                ok = False
                break
            seen.add(x)
        ans.append(ok)
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(m * k)`  
  - 对每个查询只做两次线性扫描，没有 `log` 因子。  
  - 与暴力解相比，“排序的那段慢慢的”被完全去掉了。  

- **空间复杂度**：`O(k)`（哈希集合）  
  - 需要存放子数组里不重复的元素，最坏情况下与子数组大小相同。  

---  

## 心得  

- **核心技巧**：利用等差数列的 **最值 + 公差** 公式，配合 **哈希表** 检查唯一性和格子匹配。  
- **适用场景**：  
  1. 判断一组数能否重新排列成等差数列（本题）。  
  2. 判断一组数能否重新排列成等比数列（类似思路，用乘法和对数检查）。  
  3. 判断一组数能否形成等间距的排列（如“能否放在均匀的格子里”）。  
- **一句话总结**：  
  “只要知道最小值、最大值和元素个数，就能直接算出唯一的公差，随后用哈希表 O(1) 检查每个数是否落在等差格子上”。  

---  

## 反思  

- **第一反应**：直接把子数组排序再检查——最直观但不是最优。  
- **最容易踩的坑**：  
  - 公差为 `0`（所有数相同）时，除法会出现除以 `0` 的错误，需要单独处理。  
  - `(max - min)` 可能不是 `(len-1)` 的整数倍，这时必须提前返回 `False`，否则后面的模运算会出错。  
  - 负数和正数混合时，取模运算仍然适用，只要使用 Python 的 `%`（它返回非负余数）。  
- **下次遇到同类题**：第一步先**从数学公式出发**，看能否直接算出关键参数（如公差、比例），再决定是否需要排序或其他昂贵操作。