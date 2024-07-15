# #2780. 有效划分的最小索引 / Minimum Index of a Valid Split

> 难度：中等 · 标签：Array、Hash Table、Sorting · [LeetCode 链接](https://leetcode.com/problems/minimum-index-of-a-valid-split/)

---

## 题目（英文原版）

**Description**

An element x of an integer array arr of length m is dominant if more than half the elements of arr have a value of x.
You are given a 0-indexed integer array nums of length n with one dominant element.
You can split nums at an index i into two arrays nums[0, ..., i] and nums[i + 1, ..., n - 1], but the split is only valid if:
Here, nums[i, ..., j] denotes the subarray of nums starting at index i and ending at index j, both ends being inclusive. Particularly, if j < i then nums[i, ..., j] denotes an empty subarray.
Return the minimum index of a valid split. If no valid split exists, return -1.

**Examples**

**Example 1:**

```
Input: nums = [1,2,2,2]
Output: 2
Explanation: We can split the array at index 2 to obtain arrays [1,2,2] and [2]. 
In array [1,2,2], element 2 is dominant since it occurs twice in the array and 2 * 2 > 3. 
In array [2], element 2 is dominant since it occurs once in the array and 1 * 2 > 1.
Both [1,2,2] and [2] have the same dominant element as nums, so this is a valid split. 
It can be shown that index 2 is the minimum index of a valid split.
```

**Example 2:**

```
Input: nums = [2,1,3,1,1,1,7,1,2,1]
Output: 4
Explanation: We can split the array at index 4 to obtain arrays [2,1,3,1,1] and [1,7,1,2,1].
In array [2,1,3,1,1], element 1 is dominant since it occurs thrice in the array and 3 * 2 > 5.
In array [1,7,1,2,1], element 1 is dominant since it occurs thrice in the array and 3 * 2 > 5.
Both [2,1,3,1,1] and [1,7,1,2,1] have the same dominant element as nums, so this is a valid split.
It can be shown that index 4 is the minimum index of a valid split.
```

**Example 3:**

```
Input: nums = [3,3,3,3,7,2,2]
Output: -1
Explanation: It can be shown that there is no valid split.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 109
- nums has exactly one dominant element.

---

## 题目（中文翻译）

**描述**  
如果整数数组 `arr`（长度为 `m`）中有一个元素 `x`，使得 `arr` 中超过一半的元素的值等于 `x`，则称 `x` 为支配元素（dominant）。  
给定一个下标从 0 开始、长度为 `n` 的整数数组 `nums`，且其中恰好存在唯一的支配元素（dominant）。  
你可以在下标 `i` 处将 `nums` 划分为两个数组 `nums[0, ..., i]` 和 `nums[i + 1, ..., n - 1]`，但仅当满足以下条件时，该划分才是有效的：

> 这里，`nums[i, ..., j]` 表示从下标 `i` 到下标 `j`（两端均包含）的子数组（subarray）。特别地，如果 `j < i`，则 `nums[i, ..., j]` 表示空子数组。

返回满足条件的有效划分的最小下标 `i`。如果不存在有效划分，返回 `-1`。

---

### 示例

**示例 1**

```text
Input: nums = [1,2,2,2]
Output: 2
```

**解释**  
我们可以在下标 `2` 处划分数组，得到子数组 `[1,2,2]` 和 `[2]`。  
在子数组 `[1,2,2]` 中，元素 `2` 是支配元素，因为它出现了两次且 `2 * 2 > 3`。  
在子数组 `[2]` 中，元素 `2` 也是支配元素，因为它出现一次且 `1 * 2 > 1`。  
这两个子数组的支配元素与原数组 `nums` 的支配元素相同，因此该划分是有效的。  
可以证明 `2` 是满足条件的最小下标。

---

**示例 2**

```text
Input: nums = [2,1,3,1,1,1,7,1,2,1]
Output: 4
```

**解释**  
我们可以在下标 `4` 处划分数组，得到子数组 `[2,1,3,1,1]` 和 `[1,7,1,2,1]`。  
在子数组 `[2,1,3,1,1]` 中，元素 `1` 是支配元素，因为它出现了三次且 `3 * 2 > 5`。  
在子数组 `[1,7,1,2,1]` 中，元素 `1` 同样是支配元素，因为它出现了三次且 `3 * 2 > 5`。  
这两个子数组的支配元素均与原数组 `nums` 的支配元素相同，因此该划分是有效的。

---

**示例 3**

```text
Input: nums = [3,3,3,3,7,2,2]
Output: -1
```

**解释**  
可以证明不存在满足条件的有效划分。

---

### 约束

- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^9`
- `nums` 恰好只有一个支配元素（dominant）。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**枚举所有可能的切分点**，对每一个 `i`（`0 ≤ i ≤ n‑2`）都检查左子数组 `nums[0…i]` 和右子数组 `nums[i+1…n‑1]` 是否满足：

1. 两个子数组各自都有**支配元素**（出现次数 > 子数组长度 / 2）。  
2. 这个支配元素必须和原数组 `nums` 的唯一支配元素相同。  

实现时可以：

- 对每个切分点 `i`，遍历左子数组统计每个数出现的次数，用一个 **哈希表**（想象成一本“词典”，单词是数组的值，页码是出现次数）来找左子数组的支配元素。  
- 同理遍历右子数组统计次数，找右子数组的支配元素。  
- 两个子数组的支配元素相等且等于原数组的支配元素时，返回 `i`。  

因为我们要对每个切分点都 **完整遍历一次子数组**，所以时间复杂度是平方级的。  

#### 代码（Python）

```python
from collections import Counter
from typing import List

def dominant_split_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    # 先找出整体的支配元素 x（题目保证唯一）
    total_cnt = Counter(nums)
    x, f = max(total_cnt.items(), key=lambda kv: kv[1])   # 支配元素
    # 枚举切分点
    for i in range(n - 1):          # 只能切到倒数第二个位置
        # ---------- 左子数组 ----------
        left = nums[:i + 1]
        left_cnt = Counter(left)
        left_len = len(left)
        # 找左子数组的支配元素（如果有的话）
        left_dom = None
        for val, cnt in left_cnt.items():
            if cnt * 2 > left_len:     # 出现次数 > 长度/2
                left_dom = val
                break
        # ---------- 右子数组 ----------
        right = nums[i + 1:]
        right_cnt = Counter(right)
        right_len = len(right)
        right_dom = None
        for val, cnt in right_cnt.items():
            if cnt * 2 > right_len:
                right_dom = val
                break
        # 检查是否满足题目要求
        if left_dom == right_dom == x:
            return i
    return -1
```

> **关键行注释**  
> - `Counter`：像“查字典”，把每个数映射到它出现的次数。  
> - `cnt * 2 > length`：判断是否超过“一半”。把 “> 半” 用乘法写成整数比较，避免浮点数。  

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 对每个切分点（最多 `n` 个）我们都要遍历一次左子数组和一次右子数组，最坏情况是 `1 + 2 + … + (n‑1) ≈ n²/2`。  
  - 大白话：如果 `n = 10⁴`，大概要算 `10⁸` 次操作，明显会超时。  
- **空间复杂度**：`O(n)`（用于 `Counter` 的额外存储）  
  - 每次统计子数组时都要开辟一个哈希表，最坏会存放所有不同的数。  

---

### 2. 最优解  

#### 思路  

暴力解的**瓶颈**在于每次切分都要重新统计子数组的频率。  
观察可以发现：  

1. **支配元素是唯一的**，记为 `x`，它在整个数组出现了 `f` 次。  
2. 对于任意切分点 `i`，左子数组 `nums[0…i]` 中 `x` 的出现次数 `f1`，右子数组中 `x` 的出现次数自然是 `f2 = f - f1`。  
3. 判断 `x` 是否在左子数组支配，只需要检查 `f1 * 2 > (i + 1)`（左子数组长度是 `i+1`）。同理右侧判断 `f2 * 2 > (n - i - 1)`。  

所以，只要我们**一次遍历**数组，维护 `x` 的前缀出现次数 `f1`，即可在 `O(1)` 时间内判断当前切分点是否合法。  

实现步骤：

1. **找出支配元素 `x`**：一次遍历，用哈希表统计所有数的出现次数，取出现次数最大的那个。  
2. **遍历数组**，用变量 `pref` 累计到当前位置为止 `x` 的出现次数。  
   - 当 `i` 在 `[0, n-2]` 时（因为右侧至少要有一个元素），  
     - `left_len = i + 1`，`right_len = n - i - 1`  
     - `f1 = pref`，`f2 = total_f - pref`  
     - 检查 `f1 * 2 > left_len` 且 `f2 * 2 > right_len`，若都成立，返回 `i`。  
3. 若遍历结束仍未找到合法切分点，返回 `-1`。  

这就是**前缀计数**的典型应用，只需 `O(n)` 时间、`O(1)` 额外空间（哈希表用于第一次统计）。  

#### 代码（Python）

```python
from collections import Counter
from typing import List

def minimum_valid_split(nums: List[int]) -> int:
    n = len(nums)
    # ---------- 第一步：找到唯一的支配元素 ----------
    cnt = Counter(nums)               # 统计整体频率
    x, total_f = max(cnt.items(), key=lambda kv: kv[1])   # 支配元素 x 与它的总出现次数 f
    # ---------- 第二步：一次遍历，维护前缀出现次数 ----------
    pref = 0                          # 到当前下标 i 为止，x 出现的次数
    for i in range(n - 1):            # 只能切到倒数第二个位置
        if nums[i] == x:
            pref += 1                 # 更新前缀计数
        left_len = i + 1
        right_len = n - i - 1
        # 左子数组是否支配
        left_dom = pref * 2 > left_len
        # 右子数组是否支配（总出现次数减去左侧）
        right_dom = (total_f - pref) * 2 > right_len
        if left_dom and right_dom:
            return i                  # 找到最小的合法切分点
    return -1                         # 没有合法切分点
```

> **关键行注释**  
> - `cnt = Counter(nums)`：一次遍历得到所有数的出现次数，相当于“查字典”。  
> - `max(..., key=lambda kv: kv[1])`：取出现次数最多的键值对，即支配元素。  
> - `pref += 1`：类似“累计计数器”，记录到当前位置为止支配元素出现了多少次。  
> - `pref * 2 > left_len`：判断左子数组中支配元素出现次数是否超过“一半”。  

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 第一次遍历统计频率 `O(n)`，第二次遍历检查切分点 `O(n)`，总共线性增长。  
  - 与暴力解相比，从 “每次都重新数” 降到 “只数一次”，快了几个数量级。  
- **空间复杂度**：`O(k)`（`k` 为不同数的种类数）  
  - 用哈希表存储整体频率，最坏情况 `k = n`（所有数都不相同），仍然是 `O(n)`。  
  - 但在第二遍遍历中只用了常数级额外空间。  

---

## 心得  

- **核心技巧**：**前缀计数 + 只关心支配元素**。  
- 该技巧常用于**只需要判断某个特定值在子区间是否满足条件**的题目，例如：  
  1. *Find the Minimum Index of a Valid Split*（本题）。  
  2. *Maximum Frequency of a Subarray*（判断某元素出现次数是否超过阈值）。  
  3. *Find the First Position Where the Cumulative Sum Exceeds a Target*（累计和大于目标）。  
- **一句话总结**：  
  “既然支配元素唯一，只要一次遍历累计它的出现次数，就能在 O(1) 时间内判断每个切分点是否合法。”  

---

## 反思  

- **第一反应**：先想到“遍历所有切分点，分别统计左右子数组”。这是一种**直觉暴力**的思路。  
- **最容易踩的坑**：  
  - 忘记 **右子数组必须非空**，导致循环范围写成 `range(n)` 而产生错误的切分点。  
  - 判断支配条件时使用 `>` 而不是 `>=`（题目要求“超过一半”，不是“至少一半”）。  
  - 当支配元素出现次数正好是子数组长度的一半时不算支配，需要注意乘以 2 的比较方式。  
- **下次遇到类似题**，第一步应该：  
  1. **确认是否只有唯一的关键元素**（如支配元素、目标值）。  
  2. **把整个数组的统计信息预处理**（哈希表、前缀和），  
  3. 然后 **用一次线性遍历维护前缀计数**，在遍历过程中直接检查条件。