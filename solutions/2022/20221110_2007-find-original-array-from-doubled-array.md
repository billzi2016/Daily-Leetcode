# #2007. **从倍增数组中恢复原数组** / Find Original Array From Doubled Array

> 难度：中等 · 标签：Array、Hash Table、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/find-original-array-from-doubled-array/)

---

## 题目（英文原版）

**Description**

An integer array original is transformed into a doubled array changed by appending twice the value of every element in original, and then randomly shuffling the resulting array.
Given an array changed, return original if changed is a doubled array. If changed is not a doubled array, return an empty array. The elements in original may be returned in any order.

**Examples**

**Example 1:**

```
Input: changed = [1,3,4,2,6,8]
Output: [1,3,4]
Explanation: One possible original array could be [1,3,4]:
- Twice the value of 1 is 1 * 2 = 2.
- Twice the value of 3 is 3 * 2 = 6.
- Twice the value of 4 is 4 * 2 = 8.
Other original arrays could be [4,3,1] or [3,1,4].
```

**Example 2:**

```
Input: changed = [6,3,0,1]
Output: []
Explanation: changed is not a doubled array.
```

**Example 3:**

```
Input: changed = [1]
Output: []
Explanation: changed is not a doubled array.
```

**Constraints**

- 1 <= changed.length <= 105
- 0 <= changed[i] <= 105

---

## 题目（中文翻译）

一个整数数组 `original` 通过以下方式被转换为倍增数组 `changed`：先将 `original` 中每个元素的两倍值追加到数组中，然后对得到的数组进行随机洗牌（shuffle）。  
给定数组 `changed`，如果它是一个合法的倍增数组，则返回对应的 `original`；否则返回空数组 `[]`。`original` 中元素的返回顺序可以任意。

**示例 1**  
**输入**: `changed = [1,3,4,2,6,8]`  
**输出**: `[1,3,4]`  
**解释**: 一种可能的 `original` 为 `[1,3,4]`：  
- `1` 的两倍是 `1 * 2 = 2`。  
- `3` 的两倍是 `3 * 2 = 6`。  
- `4` 的两倍是 `4 * 2 = 8`。  
其他合法的 `original` 如 `[4,3,1]` 或 `[3,1,4]` 也都可以。

**示例 2**  
**输入**: `changed = [6,3,0,1]`  
**输出**: `[]`  
**解释**: `changed` 不是一个合法的倍增数组。

**示例 3**  
**输入**: `changed = [1]`  
**输出**: `[]`  
**解释**: `changed` 不是一个合法的倍增数组。

**约束条件**  
- `1 <= changed.length <= 10^5`  
- `0 <= changed[i] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：  
1. 把 `changed` 看成一个“乱序的原数组 + 其两倍”。  
2. 从中挑出若干个数，设它们是原数组的元素，然后检查这批数的两倍是否全部也出现在 `changed` 中。  
3. 如果能一次性把所有数配对成功，就得到一个合法的 `original`；否则说明 `changed` 不是合法的 doubled array。

**用到的数据结构**  
- **列表**：保存当前挑选的原数组元素。  
- **集合/列表的 `remove` 操作**：模拟把已配对的元素从 `changed` 中删掉。可以把 `remove` 想象成在字典里查到某个词后把对应的页码撕掉——每删一次，就相当于把这个词（数）从书里除去。

**为什么它是正确的**  
只要我们能把 `changed` 中的每个数都找到对应的「原数」或「两倍」关系，并且配对后全部消除，就说明原数组真的存在。暴力遍历所有可能的挑选方式，必然能够覆盖所有合法情况。

**时间/空间复杂度**  
- 对每个元素都要尝试找它的两倍，最坏情况下需要遍历剩余的所有元素寻找匹配，时间复杂度约为 **O(n²)**（n 是数组长度）。  
  - 大白话：如果数组有 10,000 个数，程序大概要做 10,000 × 10,000 = 100,000,000 次比较，显然会很慢。  
- 需要额外的列表保存已经配对的元素，空间复杂度是 **O(n)**。

#### 代码（Python）

```python
from typing import List

def findOriginal_bruteforce(changed: List[int]) -> List[int]:
    n = len(changed)
    # 长度必须是偶数，否则不可能是“原数组 + 两倍”
    if n % 2: 
        return []

    # 复制一份，后面会在这份上做删减
    nums = changed[:]
    # 结果列表
    original = []

    # 暴力尝试每一个数作为原数组的候选
    for i in range(n):
        if not nums:          # 已经全部配对完
            break
        x = nums[0]           # 取当前最左边的数当作候选
        # 在剩余的列表里寻找它的两倍
        try:
            idx = nums.index(2 * x, 1)   # 从位置1开始找，避免匹配到自己
        except ValueError:              # 没找到两倍，说明配对失败
            return []
        # 成功配对：把 x 与 2*x 从列表中删掉
        original.append(x)
        nums.pop(idx)        # 先删两倍，防止下标错位
        nums.pop(0)          # 再删掉 x 本身

    # 最终如果所有数都配对成功，original 就是答案
    return original if not nums else []
```

> **注意**：上述实现仅为演示暴力思路，实际运行会因为 `list.index` 与 `pop` 的线性时间导致整体 O(n²)。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 每次配对都要在剩余的列表里线性搜索两倍的位置，最坏会遍历 `n/2 + n/2-1 + … + 1 ≈ n²/4` 次。  
- **空间复杂度**：`O(n)`  
  - 复制了一份 `changed`（长度 n）以及存放原数组的列表。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**瓶颈在于频繁的线性查找和删除**。如果我们能够**一次性知道每个数出现了多少次**，就可以直接判断配对是否可能，而不必逐个遍历。

关键观察：

1. **最小的数一定不是别的数的两倍**。因为如果它是某个数的两倍，那么那个数会更小，和「最小」矛盾。  
2. 对于 **0**，它是自己的两倍，需要成对出现（出现次数必须为偶数）。  
3. 按 **从小到大** 的顺序处理，保证每次配对的「原数」一定已经是当前最小的、尚未配对的数。

基于上述观察，我们可以：

- 先对 `changed` 进行排序（或使用计数排序），得到有序序列。  
- 用 **哈希表（Python 的 `collections.Counter`）** 记录每个数的出现次数。哈希表就像一本“词典”，键是数值，值是该数出现的次数。  
- 依次遍历排序后的数值 `x`：  
  - 若 `cnt[x] == 0`，说明这个数已经全部配对完，直接跳过。  
  - 否则，检查 `cnt[2*x]` 是否足够（必须 ≥ `cnt[x]`）。如果不够，说明配对失败，直接返回空数组。  
  - 把 `cnt[2*x]` 减去 `cnt[x]`（配对成功），并把 `cnt[x]` 次数加入答案 `original` 中。  
- 最后返回 `original`。

**为什么是最优的**  
- 只遍历一次排序后的数组，配对过程全在 O(1) 的哈希表查找与更新中完成。  
- 排序的代价是 `O(n log n)`，这是已知的下界（因为我们必须至少检查所有元素的相对大小）。  
- 整体时间复杂度 `O(n log n)`，空间复杂度 `O(n)`（哈希表存放计数）。

#### 代码（Python）

```python
from typing import List
from collections import Counter

def findOriginal(changed: List[int]) -> List[int]:
    n = len(changed)
    # 长度必须为偶数，否则不可能由原数组 + 两倍构成
    if n % 2:
        return []

    changed.sort()                     # O(n log n) 的排序
    cnt = Counter(changed)             # 统计每个数出现的次数
    original = []

    for x in changed:
        if cnt[x] == 0:                # 已经全部配对完，直接跳过
            continue

        # 处理 0 的特殊情况：0 的两倍仍是 0，需要成对出现
        if x == 0:
            if cnt[x] % 2:             # 0 的出现次数是奇数，配不成对
                return []
            # 把所有 0 配对完，加入一半的 0 到原数组
            original.extend([0] * (cnt[x] // 2))
            cnt[x] = 0
            continue

        double = x * 2
        if cnt[double] < cnt[x]:       # 两倍不够配对，直接失败
            return []

        # 配对成功：把 x 的出现次数加入答案
        original.extend([x] * cnt[x])
        cnt[double] -= cnt[x]          # 把对应的两倍数量扣掉
        cnt[x] = 0                     # x 已经全部配对完

    return original
```

> **代码要点注释**  
> - `changed.sort()`：把乱序的数组排成从小到大的顺序，类似把散乱的水果按大小排好，方便后面“一只找另一只”。  
> - `Counter`：相当于“查字典”，快速得到每个数出现了几次。  
> - `if x == 0`：因为 0 的两倍还是 0，需要成对出现。  
> - `original.extend([x] * cnt[x])`：把当前数出现的次数全部加入答案。  

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 排序占 `n log n`，遍历和哈希表操作都是线性 `O(n)`。相比暴力的 `O(n²)`，速度提升显著。  
- **空间复杂度**：`O(n)`  
  - 需要额外的计数哈希表以及答案列表，均与输入规模成正比。  

---

## 心得

- **核心技巧**：**排序 + 哈希计数 + 从小到大配对**。  
- **适用的题型**：  
  1. “数组中找配对数” 类题（如 *Array of Doubled Pairs*、*Find All Numbers Disappeared in an Array* 的变形）。  
  2. “原数组 + 派生数组” 的逆向推断（如 *Recover Original Array From Prefix Sums*）。  
  3. “出现次数必须满足特定关系” 的题目（如 *Array of Even Length with Same Average*）。  
- **一句话总结**：**把最小的数视为原数组的成员，逐步配对它的两倍，利用计数表一次性完成配对**。

---

## 反思

- **第一反应**：看到“原数组 + 两倍”立刻想到把数组拆成两半、配对，但是忘记了顺序混乱会导致配对困难。  
- **最容易踩的坑**：  
  - 忽视 `0` 的特殊性（0 的两倍仍是 0，需要成对出现）。  
  - 只检查出现次数而不考虑数值大小，可能导致把大的数误当成原数组成员。  
  - 当 `changed` 长度为奇数时直接返回空数组，否则会在配对阶段卡死。  
- **下次类似题的第一步**：先 **排序** 并 **统计出现次数**，找出必然是“原数”的最小元素，然后**从小到大**逐步配对其两倍。这样可以把“随意配对”的暴力搜索转化为线性的、可证明正确的过程。