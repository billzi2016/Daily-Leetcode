# #2080. **区间频率查询** / Range Frequency Queries

> 难度：中等 · 标签：Array、Hash Table、Binary Search、Design、Segment Tree · [LeetCode 链接](https://leetcode.com/problems/range-frequency-queries/)

---

## 题目（英文原版）

**Description**

Design a data structure to find the frequency of a given value in a given subarray.
The frequency of a value in a subarray is the number of occurrences of that value in the subarray.
Implement the RangeFreqQuery class:
A subarray is a contiguous sequence of elements within an array. arr[left...right] denotes the subarray that contains the elements of nums between indices left and right (inclusive).

**Examples**

**Example 1:**

```
Input
["RangeFreqQuery", "query", "query"]
[[[12, 33, 4, 56, 22, 2, 34, 33, 22, 12, 34, 56]], [1, 2, 4], [0, 11, 33]]
Output
[null, 1, 2]

Explanation
RangeFreqQuery rangeFreqQuery = new RangeFreqQuery([12, 33, 4, 56, 22, 2, 34, 33, 22, 12, 34, 56]);
rangeFreqQuery.query(1, 2, 4); // return 1. The value 4 occurs 1 time in the subarray [33, 4]
rangeFreqQuery.query(0, 11, 33); // return 2. The value 33 occurs 2 times in the whole array.
```

**Constraints**

- 1 <= arr.length <= 105
- 1 <= arr[i], value <= 104
- 0 <= left <= right < arr.length
- At most 105 calls will be made to query

---

## 题目（中文翻译）

设计一种数据结构，用于在给定的子数组（subarray）中查找指定值的出现次数（frequency）。  
子数组（subarray）是数组中连续的一段元素。`arr[left...right]` 表示下标 `left` 到 `right`（含）之间的所有元素构成的子数组。

实现 `RangeFreqQuery` 类：

```cpp
class RangeFreqQuery {
public:
    RangeFreqQuery(vector<int>& arr);          // 构造函数，初始化数据结构
    int query(int left, int right, int value); // 返回 value 在子数组 arr[left...right] 中出现的次数
};
```

**示例 1**

```text
输入
["RangeFreqQuery", "query", "query"]
[[[12, 33, 4, 56, 22, 2, 34, 33, 22, 12, 34, 56]], [1, 2, 4], [0, 11, 33]]
输出
[null, 1, 2]
```

**解释**
```text
RangeFreqQuery rangeFreqQuery = new RangeFreqQuery([12, 33, 4, 56, 22, 2, 34, 33, 22, 12, 34, 56]);
rangeFreqQuery.query(1, 2, 4); // 返回 1。值 4 在子数组 [33, 4] 中出现 1 次
rangeFreqQuery.query(0, 11, 33); // 返回 2。值 33 在子数组 [12, 33, 4, 56, 22, 2, 34, 33, 22, 12, 34, 56] 中出现 2 次
```

**约束条件**
- `1 <= arr.length <= 10^5`
- `1 <= arr[i], value <= 10^4`
- `0 <= left <= right < arr.length`
- 最多会有 `10^5` 次 `query` 调用

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**把子数组直接取出来，逐个数数**，看目标值出现了几次。  
- **数据结构**：只用 Python 的列表（`list`），因为我们只需要遍历子区间。  
- **生活化类比**：把数组想成一本笔记本，`left`、`right` 是要翻开的页码范围。我们把这几页的内容全部读一遍，手里记一个计数器，每看到一次目标数字就 +1，最后把计数器的值返回。  
- **正确性**：因为我们把子数组的每个元素都检查了一遍，所有出现的目标值必然都会被计数，答案必然正确。

#### 代码（Python）

```python
from typing import List

class RangeFreqQuery:
    def __init__(self, arr: List[int]):
        # 直接保存原数组
        self.arr = arr

    def query(self, left: int, right: int, value: int) -> int:
        """在子数组 arr[left..right] 中统计 value 出现的次数"""
        cnt = 0                     # 计数器
        for i in range(left, right + 1):   # 逐个遍历子区间（包括 right）
            if self.arr[i] == value:       # 遇到目标值就加一
                cnt += 1
        return cnt
```

#### 复杂度

- **时间复杂度**：`O(right - left + 1)`  
  这表示我们要检查子数组的每一个元素，最坏情况下（`left=0, right=n-1`）就是 `O(n)`。如果把 `O(n)` 想象成“和书里每一页都要读一遍”，显而易见会很慢，尤其是查询次数高达 10⁵ 次时。
- **空间复杂度**：`O(1)`（不计输入数组本身）  
  只用了一个计数器 `cnt`，不随 `n` 增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于每次查询都要 **线性遍历子数组**。  
我们可以把“每次都找目标值的位置”这件事 **提前准备**，让查询时只需要 **快速定位** 目标值出现的区间。

**核心思路**：

1. **预处理**：遍历一次完整数组，记录每个不同数值出现的所有下标。  
   - 用 **哈希表**（Python 的 `dict`）把数值映射到它出现的下标列表。  
   - 类比：这像是为每个单词在字典里建一个“页码表”，单词是 **key**，出现的页码（下标）是 **value**（一个有序的列表）。
2. **查询**：给定 `left, right, value`，我们只要在 `value` 对应的下标列表里找出 **落在 `[left, right]` 区间的下标个数**。  
   - 由于下标列表是 **递增有序** 的，使用 **二分搜索**（`bisect_left / bisect_right`）即可在 `O(log k)` 时间内定位区间端点。`k` 是该值出现的总次数，最坏也不超过 `n`。  
   - `bisect_left(list, left)` → 第一个 ≥ `left` 的位置。  
   - `bisect_right(list, right)` → 第一个 > `right` 的位置。两者之差就是落在 `[left, right]` 的元素数量。

**为什么快**：  
- 预处理只做一次 `O(n)`，之后每次查询只做两次二分搜索，时间是 `O(log k)`，对比暴力的 `O(length_of_subarray)` 大幅提升。  
- 空间上我们额外用了哈希表保存下标，总共 `O(n)`（每个元素的下标恰好存一次），是可以接受的。

#### 代码（Python）

```python
from bisect import bisect_left, bisect_right
from collections import defaultdict
from typing import List

class RangeFreqQuery:
    def __init__(self, arr: List[int]):
        """
        预处理：为每个不同的数值建立“出现下标列表”。
        这里用 defaultdict(list) 当作哈希表，key 是数值，value 是下标列表（递增）。
        """
        self.pos = defaultdict(list)   # 哈希表：value -> [indices...]
        for idx, num in enumerate(arr):
            self.pos[num].append(idx)   # 把当前下标加入对应数值的列表

    def query(self, left: int, right: int, value: int) -> int:
        """
        在子数组 arr[left..right] 中统计 value 的出现次数。
        思路：在 value 对应的下标列表中，用二分搜索找出
        第一个 >= left 的位置和第一个 > right 的位置，两者之差即为答案。
        """
        if value not in self.pos:           # 目标值根本不在数组里，直接返回 0
            return 0

        idx_list = self.pos[value]          # 取出该值的下标列表（有序）
        # 左边界：第一个下标 >= left
        left_idx = bisect_left(idx_list, left)
        # 右边界：第一个下标 > right
        right_idx = bisect_right(idx_list, right)

        # 两指针之间的元素数量就是落在区间 [left, right] 的次数
        return right_idx - left_idx
```

#### 复杂度

- **时间复杂度**  
  - **预处理**：`O(n)`，只遍历一次数组。  
  - **单次查询**：`O(log k)`，其中 `k` 是 `value` 在整个数组中出现的次数。  
    - 用大白话解释：二分搜索像是“在一本有序的电话号码簿里找某个号码的起止位置”，每次把搜索范围减半，最多需要查 `log₂(k)` 次（比如 `k=1024` 只需要 10 次比较），远比逐个遍历快。  
- **空间复杂度**：`O(n)`，因为每个元素的下标恰好存入一次，等价于复制了一遍原数组的下标信息。

与暴力解相比，查询时间从线性下降到对数级别，尤其在查询次数多（10⁵ 次）时优势显著。

---

## 心得

- **核心技巧**：**哈希表 + 有序下标列表 + 二分搜索**。把“出现位置”预先整理好，查询时只做两次二分定位。
- **适用题型**  
  1. **区间统计类**：如 “子数组中等于 target 的个数”、 “区间内小于等于 x 的元素个数”。  
  2. **离线查询 + 前缀和**：如 “区间和查询” 也可以用前缀和或类似的预处理技巧。  
  3. **频率查询**：如 “数组中某值出现的次数” 以及 “区间内出现次数最多的数” 的简化版（需要额外结构）。
- **一句话总结解题钥匙**：**把“查询”转化为“在已排好序的列表里二分定位”。**

---

## 反思

- **第一反应**：直接遍历子数组统计——最自然但不够高效。  
- **最容易踩的坑**  
  - 忘记对下标列表进行排序（虽然在遍历原数组时自然递增，但如果用其他方式构造要注意）。  
  - `bisect_left` 与 `bisect_right` 的区别：左闭右闭区间需要 `right_idx = bisect_right(..., right)`，否则会少算一个元素。  
  - 当 `value` 从未出现时，需要提前返回 `0`，否则会在空列表上二分导致错误。  
- **下次遇到同类题的第一步**：思考“能否把需要频繁查询的信息提前整理成有序结构”，如果可以，就先做一次 **预处理**，随后利用 **二分搜索**（或其他对数级查询）来快速回答。