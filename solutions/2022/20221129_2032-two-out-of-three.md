# #2032. 出现于至少两个数组的数字 / Two Out of Three

> 难度：简单 · 标签：Array、Hash Table、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/two-out-of-three/)

---

## 题目（英文原版）

**Description**



**Examples**

**Example 1:**

```
Input: nums1 = [1,1,3,2], nums2 = [2,3], nums3 = [3]
Output: [3,2]
Explanation: The values that are present in at least two arrays are:
- 3, in all three arrays.
- 2, in nums1 and nums2.
```

**Example 2:**

```
Input: nums1 = [3,1], nums2 = [2,3], nums3 = [1,2]
Output: [2,3,1]
Explanation: The values that are present in at least two arrays are:
- 2, in nums2 and nums3.
- 3, in nums1 and nums2.
- 1, in nums1 and nums3.
```

**Example 3:**

```
Input: nums1 = [1,2,2], nums2 = [4,3,3], nums3 = [5]
Output: []
Explanation: No value is present in at least two arrays.
```

**Constraints**

- 1 <= nums1.length, nums2.length, nums3.length <= 100
- 1 <= nums1[i], nums2[j], nums3[k] <= 100

---

## 题目（中文翻译）

给定三个整数数组 `nums1`、`nums2`、`nums3`，请返回所有 **至少出现在其中两个数组** 的不同整数。返回的数组可以按任意顺序排列。

**示例 1**  
Input: `nums1 = [1,1,3,2]`, `nums2 = [2,3]`, `nums3 = [3]`  
Output: `[3,2]`  
Explanation: 至少出现在两个数组中的数字为：  
- `3`，出现在所有三个数组中。  
- `2`，出现在 `nums1` 和 `nums2` 中。

**示例 2**  
Input: `nums1 = [3,1]`, `nums2 = [2,3]`, `nums3 = [1,2]`  
Output: `[2,3,1]`  
Explanation: 至少出现在两个数组中的数字为：  
- `2`，出现在 `nums2` 和 `nums3` 中。  
- `3`，出现在 `nums1` 和 `nums2` 中。  
- `1`，出现在 `nums1` 和 `nums3` 中。

**示例 3**  
Input: `nums1 = [1,2,2]`, `nums2 = [4,3,3]`, `nums3 = [5]`  
Output: `[]`  
Explanation: 没有任何数字出现在至少两个数组中。

**约束条件**  
- `1 <= nums1.length, nums2.length, nums3.length <= 100`  
- `1 <= nums1[i], nums2[j], nums3[k] <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把 **三个数组** 里出现的每一个数都拿出来，逐个去检查它到底在几条数组里出现过。  

- **数据结构**：我们可以用 **列表**（list）把所有元素串起来，再用 **两层循环** 去判断。  
- **生活化类比**：想象你有三本笔记本，里面记了若干名字。你把所有名字写在一张大纸上，然后对每个名字逐本翻阅，看看它出现了几次。  
- **为什么正确**：只要我们把每个可能的数字都检查一遍，并且准确统计它出现的数组个数，就一定能找出“出现至少两次”的数字。  

#### 代码（Python）

```python
def twoOutOfThree(nums1, nums2, nums3):
    # 把三个数组的所有元素都放进一个大列表（可能会有重复）
    all_vals = nums1 + nums2 + nums3
    
    result = []                 # 用来存放答案
    seen = set()                # 防止同一个数字被多次加入答案

    for v in all_vals:          # 逐个检查每个数字
        if v in seen:           # 已经加入答案的直接跳过
            continue

        cnt = 0                 # 记录 v 出现在几个不同的数组里
        if v in nums1: cnt += 1
        if v in nums2: cnt += 1
        if v in nums3: cnt += 1

        if cnt >= 2:            # 至少出现两次，就加入答案
            result.append(v)
            seen.add(v)         # 标记已经加入，避免重复

    return result
```

#### 复杂度  

- **时间复杂度**：`O(n1·n2·n3)` 近似为 `O(N²)`（这里 N≈100）。  
  - 外层遍历所有元素（最多 300 次），每次要在三个数组里各做一次 `in` 查找。  
  - `in` 操作在列表里是线性查找，最坏要遍历整个数组，所以整体是两层循环的乘积。  
  - 用大白话说，就是“每检查一个数字，都要把三本笔记本从头翻到尾”，所以会慢。  

- **空间复杂度**：`O(N)`  
  - 需要额外的列表 `all_vals`（最多 300 个元素）和集合 `seen` 来去重。  

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于每次都要在列表里线性查找 (`v in numsX`)。如果我们把每个数组的元素先 **去重** 并 **存进哈希表/集合**，查询就能做到 **O(1)**（常数时间）。  

**优化步骤**：

1. **把每个数组去重**  
   - 用 `set(nums1)`、`set(nums2)`、`set(nums3)`。  
   - 类比：把每本笔记本的名字先整理成“字典”，查找时直接看页码，而不用从头翻。  

2. **统计每个数字出现的数组个数**  
   - 用一个全局的 **计数哈希表**（`defaultdict(int)`），遍历三个集合，把每出现一次就 `+1`。  
   - 这里的 “出现一次” 指的是 **在不同的数组里出现一次**，因为集合已经去掉了同一数组内部的重复。  

3. **筛选计数 ≥ 2 的数字**  
   - 最后遍历计数表，把值 ≥ 2 的键收集起来返回。  

**核心技巧**：  
- **集合（Set）**：类似字典的查找表，能够在常数时间判断元素是否存在。  
- **哈希表计数**：把“出现几次”这件事交给字典来做，避免手动写嵌套循环。  

**位运算的另类写法**（可选）：因为数值范围 ≤ 100，只需要 7 位二进制即可。我们可以用一个整数的第 `i` 位来记录第 `i` 个数出现在哪些数组里。但这里为了易懂，仍以集合+哈希表的方式实现。

#### 代码（Python）

```python
from collections import defaultdict

def twoOutOfThree(nums1, nums2, nums3):
    # 1️⃣ 把每个数组去重，放进集合
    set1, set2, set3 = set(nums1), set(nums2), set(nums3)

    # 2️⃣ 用哈希表统计每个数字出现的数组个数
    cnt = defaultdict(int)          # 默认值 0

    for v in set1: cnt[v] += 1      # 出现在 nums1 的集合里，计数 +1
    for v in set2: cnt[v] += 1
    for v in set3: cnt[v] += 1

    # 3️⃣ 选出计数 >= 2 的数字
    result = [v for v, c in cnt.items() if c >= 2]

    return result
```

#### 复杂度  

- **时间复杂度**：`O(N)`  
  - 每个数组最多 100 个元素，去重、遍历集合、更新计数表都是线性操作。  
  - 用大白话说，就是“一次性把三本笔记本的名字全部整理好，再快速检查每个名字出现了几本”。  

- **空间复杂度**：`O(N)`  
  - 需要存放三个集合（每个最多 100）和计数哈希表（最多 300 条记录），都是线性空间。  

---

## 心得

- **核心技巧**：集合去重 + 哈希表计数（或位运算）  
- **适用的题型**：  
  1. “出现至少 K 次的元素” 类题（如 *Intersection of Two Arrays II*）  
  2. “找出出现次数相同/不同的数字” （如 *Find All Duplicates in an Array*）  
  3. “多集合交集/并集” 相关的题目  

> **一句话总结**：先把每个数组整理成“查字典”，再用一个计数表“一遍遍历”即可快速找出出现至少两次的数字。

---

## 反思

- **第一反应**：直接遍历所有数字并用 `in` 检查——这就是暴力解。  
- **最容易踩的坑**：  
  - **重复元素**：同一数组里出现多次不应算多次计数，需要先去重。  
  - **返回顺序**：题目对顺序没有要求，只要包含正确元素即可。  
- **下次遇到同类题**：第一步想到 **把每个集合去重并放进哈希表**，利用 O(1) 查找和计数来避免嵌套循环。