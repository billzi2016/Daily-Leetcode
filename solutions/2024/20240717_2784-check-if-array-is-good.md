# #2784. 判断数组是否为好数组 / Check if Array is Good

> 难度：简单 · 标签：Array、Hash Table、Sorting · [LeetCode 链接](https://leetcode.com/problems/check-if-array-is-good/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums. We consider an array good if it is a permutation of an array base[n].
base[n] = [1, 2, ..., n - 1, n, n] (in other words, it is an array of length n + 1 which contains 1 to n - 1 exactly once, plus two occurrences of n). For example, base[1] = [1, 1] and base[3] = [1, 2, 3, 3].
Return true if the given array is good, otherwise return false.
Note: A permutation of integers represents an arrangement of these numbers.

**Examples**

**Example 1:**

```
Input: nums = [2, 1, 3]
Output: false
Explanation: Since the maximum element of the array is 3, the only candidate n for which this array could be a permutation of base[n], is n = 3. However, base[3] has four elements but array nums has three. Therefore, it can not be a permutation of base[3] = [1, 2, 3, 3]. So the answer is false.
```

**Example 2:**

```
Input: nums = [1, 3, 3, 2]
Output: true
Explanation: Since the maximum element of the array is 3, the only candidate n for which this array could be a permutation of base[n], is n = 3. It can be seen that nums is a permutation of base[3] = [1, 2, 3, 3] (by swapping the second and fourth elements in nums, we reach base[3]). Therefore, the answer is true.
```

**Example 3:**

```
Input: nums = [1, 1]
Output: true
Explanation: Since the maximum element of the array is 1, the only candidate n for which this array could be a permutation of base[n], is n = 1. It can be seen that nums is a permutation of base[1] = [1, 1]. Therefore, the answer is true.
```

**Example 4:**

```
Input: nums = [3, 4, 4, 1, 2, 1]
Output: false
Explanation: Since the maximum element of the array is 4, the only candidate n for which this array could be a permutation of base[n], is n = 4. However, base[4] has five elements but array nums has six. Therefore, it can not be a permutation of base[4] = [1, 2, 3, 4, 4]. So the answer is false.
```

**Constraints**

- 1 <= nums.length <= 100
- 1 <= num[i] <= 200

---

## 题目（中文翻译）

**描述**  
给定一个整数数组 `nums`。如果一个数组是 `base[n]` 的全排列（permutation），则我们称该数组为 **好数组**。  

`base[n] = [1, 2, ..., n‑1, n, n]`  
（即长度为 `n + 1` 的数组，其中 `1` 到 `n‑1` 各出现一次，`n` 出现两次）。例如 `base[1] = [1, 1]`，`base[3] = [1, 2, 3, 3]`。  

返回 `true` 表示给定数组是好数组，否则返回 `false`。  
注意：整数的全排列（permutation）指这些数字的任意排列顺序。

**示例**  

*示例 1*  
```
Input: nums = [2, 1, 3]
Output: false
Explanation: 由于数组的最大元素为 3，唯一可能的 n 为 3，此时 base[3] 共有 4 个元素，而 nums 只有 3 个，因此不可能是 base[3] = [1, 2, 3, 3] 的全排列，答案为 false。
```

*示例 2*  
```
Input: nums = [1, 3, 3, 2]
Output: true
Explanation: 最大元素为 3，唯一可能的 n 为 3。可以看到 nums 通过交换第二个和第四个元素后即可得到 base[3] = [1, 2, 3, 3]，因此答案为 true。
```

*示例 3*  
```
Input: nums = [1, 1]
Output: true
Explanation: 最大元素为 1，唯一可能的 n 为 1。显然 nums 就是 base[1] = [1, 1] 的全排列，答案为 true。
```

*示例 4*  
```
Input: nums = [3, 4, 4, 1, 2, 1]
Output: false
Explanation: 最大元素为 4，唯一可能的 n 为 4。此时 base[4] 只有 5 个元素，而 nums 有 6 个，无法成为 base[4] = [1, 2, 3, 4, 4] 的全排列，答案为 false。
```

**约束条件**  
- `1 <= nums.length <= 100`  
- `1 <= nums[i] <= 200`   (原题写作 `num[i]`，此处统一为 `nums[i]`)

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：  
1. 先找出数组 `nums` 的最大值 `n`（因为 `base[n]` 中最大的数就是 `n`）。  
2. 根据 `n` 生成 **理想的基准数组** `base[n] = [1, 2, …, n‑1, n, n]`。  
3. 把 `nums` 和 `base[n]` 都 **排序**（把元素按从小到大的顺序排好），这样如果两者是同一个集合的排列，它们排好序后应该**完全相同**。  

> 类比：把两个装满不同颜色弹珠的盒子里的弹珠倒出来，按颜色从浅到深排成一排。如果两排完全一致，说明盒子里的弹珠是同样的组合，只是顺序不同。

**为什么对？**  
- 排序后相同的多重集合会得到完全相同的序列。  
- 如果 `nums` 不是 `base[n]` 的排列，要么元素种类不对，要么某个数出现次数不对，排序后必然出现差异。  

#### 代码（Python）

```python
from typing import List

def is_good_bruteforce(nums: List[int]) -> bool:
    # 1. 找到最大值 n
    n = max(nums)                         # max() 一次遍历即可得到最大数

    # 2. 生成理论上的 base[n]
    base = list(range(1, n)) + [n, n]     # [1,2,...,n-1] + 两个 n

    # 3. 长度必须相同，否则不可能是排列
    if len(nums) != len(base):
        return False

    # 4. 把两个数组都排序后逐个比较
    nums_sorted = sorted(nums)            # O(k log k) 排序，k = len(nums)
    base_sorted = sorted(base)            # base 本身已经几乎有序，仍是 O(k log k)

    return nums_sorted == base_sorted      # 完全相同则是好数组
```

#### 复杂度  
- **时间复杂度：** `O(k log k)`（`k = len(nums)`）  
  - `max(nums)` 是 `O(k)`，但排序是 `O(k log k)`，是主要耗时。  
  - 大白话：如果数组有 100 个元素，排序大约要做 100 × log₂100 ≈ 665 次比较，远多于一次线性遍历。  
- **空间复杂度：** `O(k)`  
  - 需要额外的列表来保存排序后的 `nums`（以及 `base`），相当于再占用原数组大小的空间。  

---  

### 2. 最优解  

#### 思路  
暴力解的瓶颈在 **排序**，排序本身就会把时间从线性提升到 `log` 级别。  
其实我们只需要检查每个数字出现的次数，而不必把它们排好序。  

关键观察：  
- `base[n]` 的长度一定是 `n + 1`（因为有 `1 … n‑1` 各一次，加上两个 `n`）。  
- 对于 `1 … n‑1`，每个数字只能出现 **恰好一次**。  
- 对于最大值 `n`，必须出现 **恰好两次**。  

所以只要统计每个数出现的次数，就能在一次遍历中完成判定。  
这里使用 **哈希表**（在 Python 中是 `dict`，可以看成“查字典”），键是数字，值是出现次数。  

> 类比：把弹珠装进透明盒子，每种颜色的弹珠只记数，不需要把它们排成一行。只要数目符合要求，就说明盒子里装的弹珠是想要的组合。

#### 代码（Python）

```python
from typing import List
from collections import Counter   # Counter 本质是一个字典，专门统计出现次数

def is_good(nums: List[int]) -> bool:
    # 1. 最大元素 n
    n = max(nums)

    # 2. 长度必须是 n + 1，先排除明显不符合的情况
    if len(nums) != n + 1:
        return False

    # 3. 统计每个数字出现的次数
    cnt = Counter(nums)   # 一遍遍历，时间 O(k)，空间 O(k)

    # 4. 检查 1~n-1 是否各出现一次，n 是否出现两次
    for num in range(1, n):
        if cnt.get(num, 0) != 1:          # get 防止键不存在返回 0
            return False

    # 检查最大值 n
    if cnt.get(n, 0) != 2:
        return False

    # 5. 其余数字（比如出现了比 n 更大的数）直接返回 False
    # 只要遍历完 1~n，若还有其他键说明有非法数字
    if len(cnt) != n:   # 只应该有 n 个不同的键（1~n）
        return False

    return True
```

#### 复杂度  
- **时间复杂度：** `O(k)`（线性）  
  - 只需要一次遍历统计次数，然后遍历 `1 … n`（最多 `k` 次）检查。  
  - 与暴力解相比省去了 `log k` 的排序开销。  
- **空间复杂度：** `O(k)`（哈希表）  
  - 需要存放每个不同数字的计数，最坏情况下每个数字都不同，空间和输入大小同量级。  

---

## 心得  

- **核心技巧**：利用**计数哈希表**（或数组计数）直接判断每个元素出现的次数，而不是排序。  
- **适用的题型**  
  1. 判断数组是否为某种“出现次数固定”的排列（如只出现一次或出现固定次数的数组）。  
  2. “数组是否为有效的排列”类题目（如判断是否是 `[0,1,2,…,n-1]` 的排列）。  
  3. “找出缺失或多余元素”需要计数的场景。  
- **一句话总结**：**把“顺序”扔掉，只看“每个数字出现了几次”。**  

---

## 反思  

- **第一反应**：先找最大值，然后生成目标数组再比较，想到排序。  
- **最容易踩的坑**  
  - 忽视数组长度必须是 `max + 1` 的限制，导致出现 `max` 出现两次但长度不匹配的假阳性。  
  - 只检查 `1 … n‑1` 的出现次数，却忘了确认 **没有更大的数字** 出现。  
- **下次遇到同类题**：第一步先**统计出现次数**（哈希表/计数数组），再**根据题目给出的出现次数规则**逐一验证，而不是先排序或构造完整的目标序列。