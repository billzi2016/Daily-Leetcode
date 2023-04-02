# #2190. 数组中键之后出现次数最多的数字 / Most Frequent Number Following Key In an Array

> 难度：简单 · 标签：Array、Hash Table、Counting · [LeetCode 链接](https://leetcode.com/problems/most-frequent-number-following-key-in-an-array/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums. You are also given an integer key, which is present in nums.
For every unique integer target in nums, count the number of times target immediately follows an occurrence of key in nums. In other words, count the number of indices i such that:
Return the target with the maximum count. The test cases will be generated such that the target with maximum count is unique.

**Examples**

**Example 1:**

```
Input: nums = [1,100,200,1,100], key = 1
Output: 100
Explanation: For target = 100, there are 2 occurrences at indices 1 and 4 which follow an occurrence of key.
No other integers follow an occurrence of key, so we return 100.
```

**Example 2:**

```
Input: nums = [2,2,2,2,3], key = 2
Output: 2
Explanation: For target = 2, there are 3 occurrences at indices 1, 2, and 3 which follow an occurrence of key.
For target = 3, there is only one occurrence at index 4 which follows an occurrence of key.
target = 2 has the maximum number of occurrences following an occurrence of key, so we return 2.
```

**Constraints**

- 2 <= nums.length <= 1000
- 1 <= nums[i] <= 1000
- The test cases will be generated such that the answer is unique.

---

## 题目（中文翻译）

给定一个下标从 **0** 开始的整数数组 `nums`，以及一个在 `nums` 中出现过的整数 `key`。  

对于 `nums` 中的每个不同的整数 `target`，统计 `target` 紧跟在 `key` 之后出现的次数。换句话说，统计满足以下条件的下标 `i` 的个数：

- `i > 0`
- `nums[i‑1] == key`
- `nums[i] == target`

返回出现次数最多的 `target`。题目保证出现次数最多的 `target` 是唯一的。

### 示例

#### 示例 1
```
Input: nums = [1,100,200,1,100], key = 1
Output: 100
Explanation: 对于 target = 100，存在 2 次出现在 key 之后，分别位于下标 1 和 4。没有其他整数出现在 key 之后，因此返回 100。
```

#### 示例 2
```
Input: nums = [2,2,2,2,3], key = 2
Output: 2
Explanation: 对于 target = 2，存在 3 次出现在 key 之后，分别位于下标 1、2、3。对于 target = 3，仅有一次出现在 key 之后（下标 4）。因此 target = 2 的出现次数最多，返回 2。
```

### 约束条件
- `2 <= nums.length <= 1000`
- `1 <= nums[i] <= 1000`
- 题目保证答案唯一。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：遍历数组里所有**不同的数字**（记作 `target`），然后再遍历一遍数组，统计 `target` 紧跟在 `key` 之后出现了多少次。  

- **数据结构**：我们只需要一个普通的整数计数器 `cnt`，因为每次只关心一种 `target`。如果把数组想象成一本日记，`key` 是某个特定的词语，`target` 就是紧跟在这个词后面的下一个词。我们把所有可能的下一个词一个一个拿出来检查它出现了几次。  
- **正确性**：对每个 `target`，我们都完整地遍历了一遍数组，检查所有满足 `nums[i‑1] == key && nums[i] == target` 的下标 `i`，计数自然就是它出现的次数。遍历完所有 `target` 后，选出计数最大的那个，就是答案。  

#### 代码（Python）

```python
def most_frequent(nums, key):
    # 先收集数组里出现过的所有不同数字（除去 key 本身也可以算进去）
    unique_vals = set(nums)

    best_target = None   # 最终答案
    best_cnt = -1        # 当前最大的计数

    # 对每一个可能的 target，逐个统计
    for target in unique_vals:
        cnt = 0
        # 暴力遍历整个数组，检查 target 是否紧跟在 key 之后
        for i in range(1, len(nums)):
            if nums[i - 1] == key and nums[i] == target:
                cnt += 1
        # 更新全局最大
        if cnt > best_cnt:
            best_cnt = cnt
            best_target = target

    return best_target
```

#### 复杂度

- **时间复杂度**：`O(m * n)`，其中 `n = len(nums)`，`m` 是不同数字的种类数。最坏情况下 `m ≈ n`，于是复杂度退化为 `O(n²)`。通俗地说，**把数组的长度 `n` 乘以自己一次**，所以运行时间会随数组长度的平方增长。  
- **空间复杂度**：`O(m)` 用来存放 `unique_vals` 集合，最坏 `O(n)`，但只和数字种类数有关，额外的存储很少。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**对每个 target 都要重新遍历一遍数组**。其实我们只需要一次遍历就能把所有目标的计数都收集起来：

1. **一次遍历**：从左到右看相邻的两个元素 `nums[i-1]` 与 `nums[i]`。  
2. 当 `nums[i-1] == key` 时，说明 `nums[i]` 是 **跟在 key 后面的** 数字。我们把它记进哈希表（Python 的 `dict`）里，`dict[value]` 表示该值作为 target 出现的次数。  
3. 遍历结束后，哈希表里已经包含了 **所有 target 的出现次数**，只要在表中找出计数最大的键，就是答案。

- **哈希表类比**：想象一本词典，**key** 是“前一个单词”，**value** 是“后一个单词”。我们每读到一次 “前一个单词 = key” 时，就在词典里给对应的 “后一个单词” 加一。最后，出现次数最多的“后一个单词”就是我们要找的答案。  
- **唯一答案保证**：题目说最大计数的 target 必定唯一，所以只要找出最大即可，不用考虑平局。

#### 代码（Python）

```python
def most_frequent(nums, key):
    # 用 dict 统计每个 target 紧跟在 key 后出现的次数
    cnt = {}          # cnt[target] = 出现次数

    # 从第二个元素开始检查前后关系
    for i in range(1, len(nums)):
        if nums[i - 1] == key:          # 前一个是 key
            target = nums[i]            # 当前元素就是 candidate
            cnt[target] = cnt.get(target, 0) + 1   # 计数加一

    # 找出计数最大的 target
    # 因为答案唯一，直接使用 max 并指定键为计数即可
    best_target = max(cnt, key=lambda t: cnt[t])
    return best_target
```

#### 复杂度

- **时间复杂度**：`O(n)`。只遍历一次数组，**线性**增长，数组长度翻倍，运行时间也只会翻倍。  
- **空间复杂度**：`O(m)`，`m` 为不同的 target 数量（即哈希表的键数），最坏 `O(n)`，但只存储出现过的后继数字，远小于暴力解的两层循环所产生的隐式额外空间。

---

## 心得

- **核心技巧**：利用哈希表一次遍历统计“后继元素”出现次数。  
- **适用的题型**  
  1. “统计某个元素后面出现的元素频次”——如 LeetCode 1150（`Check If a Number Is Majority Element in a Sorted Array`）的变形。  
  2. “相邻元素关系统计”——如找出出现次数最多的 **相邻对**（`Most Common Adjacent Pair`）。  
- **解题钥匙**：**把“遍历+计数”合二为一**，用哈希表一次搞定所有候选。

---

## 反思

- **第一反应**：看到“紧跟在 key 后面”，立刻想到遍历相邻元素并记录计数。  
- **最容易踩的坑**  
  - 忘记从下标 `1` 开始检查（因为要看前一个元素）。  
  - 没有处理 `key` 出现在最后一个位置的情况——此时没有后继元素，直接跳过即可。  
  - 误以为要统计 **所有出现的 target**（包括不跟在 key 后的），导致计数错误。  
- **下次第一步**：先问自己“是否可以在一次遍历中把所有需要的信息都收集起来？”如果答案是“可以”，就尝试用哈希表或计数数组一次完成统计。