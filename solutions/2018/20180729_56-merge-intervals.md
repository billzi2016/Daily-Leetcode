# #56. 合并区间 / Merge Intervals

> 难度：中等 · 标签：Array、Sorting · [LeetCode 链接](https://leetcode.com/problems/merge-intervals/)

---

## 题目（英文原版）

**Description**

Given an array of intervals where intervals[i] = [starti, endi], merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.

**Examples**

**Example 1:**

```
Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
Output: [[1,6],[8,10],[15,18]]
Explanation: Since intervals [1,3] and [2,6] overlap, merge them into [1,6].
```

**Example 2:**

```
Input: intervals = [[1,4],[4,5]]
Output: [[1,5]]
Explanation: Intervals [1,4] and [4,5] are considered overlapping.
```

**Constraints**

- 1 <= intervals.length <= 104
- intervals[i].length == 2
- 0 <= starti <= endi <= 104

---

## 题目（中文翻译）

**描述**  
给定一个区间数组（intervals），其中 `intervals[i] = [starti, endi]`，请合并所有重叠的区间，并返回一个不重叠的区间数组，使其能够覆盖输入中的所有区间。

**示例 1**  
**输入**：`intervals = [[1,3],[2,6],[8,10],[15,18]]`  
**输出**：`[[1,6],[8,10],[15,18]]`  
**解释**：区间 `[1,3]` 与 `[2,6]` 重叠，合并后得到 `[1,6]`。

**示例 2**  
**输入**：`intervals = [[1,4],[4,5]]`  
**输出**：`[[1,5]]`  
**解释**：区间 `[1,4]` 与 `[4,5]` 被视为重叠区间。

**约束条件**  
- `1 <= intervals.length <= 10^4`  
- `intervals[i].length == 2`  
- `0 <= starti <= endi <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把每一个区间都和其它所有区间两两比较，看看是否有重叠。如果有，就把它们合并成一个更大的区间；合并后再继续和剩余的区间比较，直到没有任何可以合并的为止。  

- **用到的数据结构**：  
  - `list`（列表）保存所有区间。可以把它想象成一张纸上的若干条线段。  
  - `while` 循环不断遍历列表，就像我们把纸上的线段一根根搬来搬去，检查是否可以粘在一起。  

- **为什么正确**：  
  只要遍历到每一对区间，都检查并在有交集时立即合并，最终得到的区间必然是所有原始区间的并集。因为我们没有遗漏任何可能的重叠关系，合并操作是可传递的（A 与 B 重叠，B 与 C 重叠，则 A 与 C 也会在后面的循环中被合并），所以最后的结果一定是“互不重叠且覆盖全部原始区间”的集合。

- **时间/空间复杂度**：  
  - 每次遍历要比较 `n` 个区间中的 `n-1` 对，最坏情况下要进行 `n` 次完整遍历才能没有可合并的区间。于是时间复杂度约为 **O(n²)**，这里的 `n²` 可以理解为“如果有 1000 个区间，最坏情况要比较大约 1000×1000=100 万次”。  
  - 只使用了原始列表和少量临时变量，额外空间为 **O(1)**（不计返回结果的空间）。

#### 代码（Python）

```python
from typing import List

def merge_bruteforce(intervals: List[List[int]]) -> List[List[int]]:
    # 先把区间复制一份，防止在遍历时直接修改原列表导致索引错误
    merged = [interval[:] for interval in intervals]

    i = 0
    while i < len(merged):
        has_merged = False                 # 记录本轮是否发生合并
        j = i + 1
        while j < len(merged):
            a_start, a_end = merged[i]
            b_start, b_end = merged[j]

            # 判断两区间是否重叠（或相邻，题目把相邻算作重叠）
            if not (a_end < b_start or b_end < a_start):
                # 合并成更大的区间
                new_interval = [min(a_start, b_start), max(a_end, b_end)]
                # 用新区间替换 i 位置的区间
                merged[i] = new_interval
                # 删除 j 位置的旧区间，因为已经被合并进去了
                merged.pop(j)
                has_merged = True
                # 合并后，i 位置的区间可能还能和后面的区间重叠，
                # 所以保持 i 不变，继续检查
                continue
            else:
                j += 1                     # 没重叠，检查下一个区间

        if not has_merged:                  # 本轮没有任何合并，说明 i 已经是最终区间
            i += 1
    return merged
```

#### 复杂度

- **时间复杂度**：O(n²) — “平方级”，因为每个区间可能要和其他所有区间比较多次。  
- **空间复杂度**：O(1) — 只用了常数个额外变量（不算返回的结果）。  

---  

### 2. 最优解

#### 思路  
暴力解的瓶颈在于**不停地两两比较**，导致大量重复检查。其实如果把所有区间按照左端点（`start`）从小到大排好序，重叠的区间必然会**相邻出现**。这样我们只需要一次线性扫描，就能把相邻且重叠的区间合并，时间会从 O(n²) 降到 O(n log n)（排序的代价）：

1. **排序**：把 `intervals` 按 `start` 升序排列。可以把它想象成把所有线段先摆成从左到右的顺序，方便“一眼就看出哪些相邻”。  
2. **遍历合并**：维护一个 `merged` 列表，始终保存已经处理好的、互不重叠的区间。遍历排序后的每个区间 `cur`：  
   - 如果 `merged` 为空或 `cur` 的左端点大于 `merged[-1]`（上一个已合并区间）的右端点，说明两者不重叠，直接把 `cur` 加入 `merged`。  
   - 否则，两者重叠（或相邻），只需要把上一个区间的右端点扩展到 `max(merged[-1][1], cur[1])` 即可。  

**核心算法**：**排序 + 线性合并**。  
- **排序**使用的是快速排序/归并排序等 O(n log n) 的比较排序（Python 内置 `list.sort()`），相当于把“字典”里所有词按照字母顺序排好。  
- **线性合并**则像把已经排好序的线段顺序贴在一起，遇到可以粘在一起的就直接粘，遇不到就另起一段。

#### 代码（Python）

```python
from typing import List

def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
    if not intervals:
        return []

    # 1️⃣ 按 start 从小到大排序
    intervals.sort(key=lambda x: x[0])   # lambda 就是“小工具”，告诉 sort 按第 0 个元素比较

    merged: List[List[int]] = []         # 用来存放最终的合并结果

    for cur in intervals:
        # 2️⃣ 如果 merged 为空或当前区间和上一个已合并区间不相交
        if not merged or cur[0] > merged[-1][1]:
            merged.append(cur[:])        # 直接加入新区间（拷贝一份防止后面修改影响原数据）
        else:
            # 3️⃣ 有重叠 → 把上一个区间的右端点往右伸展到更大的那个
            merged[-1][1] = max(merged[-1][1], cur[1])

    return merged
```

#### 复杂度

- **时间复杂度**：O(n log n) — 主要耗时在排序阶段，`log n` 可以理解为“把 1 万个区间排好序只需要大约 14 次比较层次”，远比平方级快。遍历合并是线性的 O(n)。  
- **空间复杂度**：O(log n)（排序的递归栈）或 O(n)（如果使用额外的临时数组），在 Python 的原地排序里实际额外空间很小，基本可以认为是 **O(1)** 额外空间（不计返回结果）。

---

## 心得

- **核心技巧**：先排序再线性扫描合并，是处理「区间重叠」这类问题的通用套路。  
- **适用的题型**：  
  1. **合并区间**（本题）  
  2. **求区间交集**（两个区间集合的公共部分）  
  3. **区间覆盖问题**（如「最小区间覆盖」）  
- **一句话总结**：把区间排好顺序，重叠的自然相邻，一遍扫描即可完成合并——排序是钥匙。

---

## 反思

- **第一反应**：看到“合并所有重叠区间”，立刻想到两两比较，写出暴力解。  
- **最容易踩的坑**：  
  - 忘记把 **相邻** 区间（如 `[1,4]` 与 `[4,5]`）也算重叠，需要使用 `>=` 或 `>` 的判断方式。  
  - 处理空输入或只有一个区间的边界情况。  
  - 在合并时直接修改原列表导致后续遍历出错，最好使用拷贝或维护一个新列表。  
- **下次类似题目第一步**：先思考能否通过**排序**把“可能相互影响的元素”放在一起，再决定是使用“双指针”“线性扫描”等线性算法，而不是直接暴力比较。