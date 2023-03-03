# #2150. **数组中所有孤独数字** / Find All Lonely Numbers in the Array

> 难度：中等 · 标签：Array、Hash Table、Counting · [LeetCode 链接](https://leetcode.com/problems/find-all-lonely-numbers-in-the-array/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums. A number x is lonely when it appears only once, and no adjacent numbers (i.e. x + 1 and x - 1) appear in the array.
Return all lonely numbers in nums. You may return the answer in any order.

**Examples**

**Example 1:**

```
Input: nums = [10,6,5,8]
Output: [10,8]
Explanation: 
- 10 is a lonely number since it appears exactly once and 9 and 11 does not appear in nums.
- 8 is a lonely number since it appears exactly once and 7 and 9 does not appear in nums.
- 5 is not a lonely number since 6 appears in nums and vice versa.
Hence, the lonely numbers in nums are [10, 8].
Note that [8, 10] may also be returned.
```

**Example 2:**

```
Input: nums = [1,3,5,3]
Output: [1,5]
Explanation: 
- 1 is a lonely number since it appears exactly once and 0 and 2 does not appear in nums.
- 5 is a lonely number since it appears exactly once and 4 and 6 does not appear in nums.
- 3 is not a lonely number since it appears twice.
Hence, the lonely numbers in nums are [1, 5].
Note that [5, 1] may also be returned.
```

**Constraints**

- 1 <= nums.length <= 105
- 0 <= nums[i] <= 106

---

## 题目（中文翻译）

给定一个整数数组 `nums`。当一个数字 `x` 在数组中只出现一次，且它的相邻数字（即 `x + 1` 和 `x - 1`）都未出现在数组中时，称 `x` 为 **孤独数字**。  
返回 `nums` 中所有孤独数字。答案可以按任意顺序返回。

**示例 1**

```text
Input: nums = [10,6,5,8]
Output: [10,8]
Explanation: 
- 10 是孤独数字，因为它恰好出现一次，且 9 和 11 均未出现在 `nums` 中。  
- 8 是孤独数字，因为它恰好出现一次，且 7 和 9 均未出现在 `nums` 中。  
- 5 不是孤独数字，因为 6 出现在 `nums` 中，反之亦然。  

因此，`nums` 中的孤独数字为 [10, 8]。  
注意，返回 [8, 10] 也是可以的。
```

**示例 2**

```text
Input: nums = [1,3,5,3]
Output: [1,5]
Explanation: 
- 1 是孤独数字，因为它恰好出现一次，且 0 和 2 均未出现在 `nums` 中。  
- 5 是孤独数字，因为它恰好出现一次，且 4 和 6 均未出现在 `nums` 中。  
- 3 不是孤独数字，因为它出现了两次。  

因此，`nums` 中的孤独数字为 [1, 5]。  
注意，返回 [5, 1] 也是可以的。
```

**约束条件**

- `1 <= nums.length <= 10^5`
- `0 <= nums[i] <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**对数组里的每个数 x，都去遍历整个数组，看看**  

1. `x` 出现了几次（是否恰好一次）  
2. `x-1` 和 `x+1` 是否出现过  

如果这三个条件都满足，`x` 就是 “lonely”。  

- **用到的数据结构**：只需要原始的 `list nums`，不需要额外的容器。  
- **生活化类比**：把数组想成一本电话簿，想要判断某个人的电话号码是否“孤单”，我们要把整本电话簿从头到尾翻一遍，找出是否只有他一个人出现，而且他的前后邻居（号码 -1、+1）根本不存在。  

这个方法之所以 **正确**，是因为我们把题目要求的所有条件都一一检查了。只要遍历完整个数组，所有可能的相邻数字都会被看到。

#### 代码（Python）

```python
def findLonely(nums):
    res = []                               # 用来存放最终的孤独数字
    n = len(nums)
    for i in range(n):
        x = nums[i]
        # 统计 x 在数组中出现的次数（暴力遍历整个数组）
        cnt = 0
        for y in nums:
            if y == x:
                cnt += 1
        if cnt != 1:                        # 出现不止一次，直接跳过
            continue

        # 检查 x-1 是否出现
        has_left = False
        for y in nums:
            if y == x - 1:
                has_left = True
                break

        # 检查 x+1 是否出现
        has_right = False
        for y in nums:
            if y == x + 1:
                has_right = True
                break

        # 同时满足“只出现一次”且“左右都不存在”即为孤独数字
        if not has_left and not has_right:
            res.append(x)

    return res
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 解释：外层遍历 `n` 次，每次内部又要遍历整个数组（统计次数、检查左邻、检查右邻），所以大概是 `n × n` 次操作。可以把 `O(n²)` 想象成“如果你有 10,000 个数，需要做 100,000,000 次检查”，随 `n` 增大会非常慢。  
- **空间复杂度**：`O(1)`（不计返回结果的空间）  
  - 只用了常数级别的额外变量 `cnt、has_left、has_right`，不随输入规模增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于每次都要遍历整个数组去判断**  
- “x 出现了几次”  
- “x‑1、x+1 是否出现”  

只要我们能 **一次遍历就把这些信息全部记下来**，后面的查询就可以 **O(1)** 完成。这里就可以利用 **哈希表（字典）或集合**：

1. **统计出现次数**：用 `collections.Counter`（或普通 `dict`）把每个数字出现的次数统计出来。相当于把电话簿先做一次“索引”，以后想知道某个号码出现几次，只需要查表，时间是常数。  
2. **快速判断相邻数字是否存在**：把所有出现过的数字放进 `set(nums)`，集合的查找同样是 O(1)。  
3. **遍历唯一出现的数字**：只需要遍历 `counter` 的键（即所有不同的数字），检查  
   - `counter[x] == 1`（只出现一次）  
   - `x-1 not in num_set` 且 `x+1 not in num_set`（左右都不存在）  

这样 **只需要一次 O(n) 的遍历来建立哈希表和集合**，再一次 O(m)（m 为不同数字的个数，最多也是 O(n)）的遍历来挑选孤独数字，整体是线性时间。

- **核心数据结构**：  
  - **哈希表（Counter）**：像是“字典”，`key` 是数字，`value` 是出现次数。查找 `key` 的出现次数就像在字典里直接翻到对应的页码。  
  - **集合（set）**：只存数字本身，用来判断“某个数字是否在数组里”。相当于“是否有这本书”，检查非常快。  

- **类比**：想象你要在一座城市里找所有只住一户且左右邻居都空着的房子。先把全城所有房子的地址登记（一次遍历），然后只看登记表里出现一次的地址，并检查其左边和右边的地址是否也在登记表里。这样查找几乎瞬间完成。

#### 代码（Python）

```python
from collections import Counter

def findLonely(nums):
    # 1. 统计每个数字出现的次数
    cnt = Counter(nums)            # 哈希表：key->数字，value->出现次数
    # 2. 把所有出现过的数字放进集合，方便 O(1) 判断是否存在
    num_set = set(nums)

    res = []                        # 最终答案
    # 3. 只遍历一次哈希表的键（不同的数字）
    for x in cnt:
        if cnt[x] == 1:             # 只出现一次
            # 检查左右相邻数字是否不存在于集合中
            if (x - 1) not in num_set and (x + 1) not in num_set:
                res.append(x)       # 满足所有条件，加入答案

    return res
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 第一次遍历构建 `Counter` 与 `set` 各是 `O(n)`，第二次遍历不同数字的次数最多也是 `n`，所以整体随输入规模线性增长。可以把它想成“即使有 100,000 个数，也只需要大约 100,000 次简单操作”，非常快。  
- **空间复杂度**：`O(n)`  
  - 需要额外的哈希表和集合来存放每个数字的信息，最坏情况下每个数字都不相同，所以会占用和原数组同量级的额外空间。

---

## 心得

- **核心技巧**：利用 **哈希表/集合** 在一次遍历中完成计数和存在性查询，避免重复遍历。  
- **适用的题型**  
  1. “只出现一次的数字” 类题（如 LeetCode 169 Single Number）  
  2. “出现次数统计 + 条件筛选” 的数组题（如 统计出现次数大于 1 的数字、找出缺失的数字等）  
- **一句话总结**：**先把信息预处理进哈希表/集合，后面查询就能做到 O(1)。**  

---

## 反思

- **第一反应**：直接遍历每个元素并逐个检查左右邻居，写成三层循环。  
- **最容易踩的坑**  
  - 忘记判断 **出现次数恰好一次**，只检查了相邻数字会导致错误答案。  
  - 对于边界数字（如 0 或 10⁶），`x-1` 或 `x+1` 可能超出题目给出的范围，但因为我们使用集合判断是否存在，所以不需要额外的边界判断。  
- **下次遇到同类题**：第一步想到 **“先统计 + 用集合快速查询”**，把所有需要的属性一次性记录下来，再在这些记录上做筛选。这样可以把原本的 O(n²) 直接降到 O(n)。