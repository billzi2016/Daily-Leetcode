# #986. 区间列表交集 / Interval List Intersections

> 难度：中等 · 标签：Array、Two Pointers、Line Sweep · [LeetCode 链接](https://leetcode.com/problems/interval-list-intersections/)

---

## 题目（英文原版）

**Description**

You are given two lists of closed intervals, firstList and secondList, where firstList[i] = [starti, endi] and secondList[j] = [startj, endj]. Each list of intervals is pairwise disjoint and in sorted order.
Return the intersection of these two interval lists.
A closed interval [a, b] (with a <= b) denotes the set of real numbers x with a <= x <= b.
The intersection of two closed intervals is a set of real numbers that are either empty or represented as a closed interval. For example, the intersection of [1, 3] and [2, 4] is [2, 3].

**Examples**

**Example 1:**

```
Input: firstList = [[0,2],[5,10],[13,23],[24,25]], secondList = [[1,5],[8,12],[15,24],[25,26]]
Output: [[1,2],[5,5],[8,10],[15,23],[24,24],[25,25]]
```

**Example 2:**

```
Input: firstList = [[1,3],[5,9]], secondList = []
Output: []
```

**Constraints**

- 0 <= firstList.length, secondList.length <= 1000
- firstList.length + secondList.length >= 1
- 0 <= starti < endi <= 109
- endi < starti+1
- 0 <= startj < endj <= 109
- endj < startj+1

---

## 题目（中文翻译）

给定两个闭区间（closed interval）列表 `firstList` 和 `secondList`，其中 `firstList[i] = [starti, endi]`，`secondList[j] = [startj, endj]`。每个列表内的区间两两不相交（pairwise disjoint）且已排序（sorted order）。

返回这两个区间列表的交集（intersection）。

闭区间 `[a, b]`（其中 `a <= b`）表示满足 `a <= x <= b` 的所有实数 `x` 的集合。

两个闭区间的交集是一个实数集合，要么为空，要么仍然可以表示为闭区间。例如，`[1, 3]` 与 `[2, 4]` 的交集为 `[2, 3]`。

示例 1:

示例 2:

约束条件：
- `0 <= firstList.length, secondList.length <= 1000`
- `firstList.length + secondList.length >= 1`
- `0 <= starti < endi <= 10^9`
- `endi < starti+1`
- `0 <= startj < endj <= 10^9`
- `endj < startj+1`

示例：
示例 1:
```
Input: firstList = [[0,2],[5,10],[13,23],[24,25]], secondList = [[1,5],[8,12],[15,24],[25,26]]
Output: [[1,2],[5,5],[8,10],[15,23],[24,24],[25,25]]
```

示例 2:
```
Input: firstList = [[1,3],[5,9]], secondList = []
Output: []
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把两条列表里所有的区间两两配对，检查每一对是否有交集。  
- **数据结构**：我们把每个区间看作一个小盒子，里面装着从 `start` 到 `end` 的所有实数。遍历时相当于把两个盒子逐个打开，看看有没有共同的数字。  
- **为什么正确**：只要把所有可能的配对都检查一遍，凡是有交集的配对都会被发现，所有交集区间自然就全收集进来了。  
- **复杂度分析**：设 `m = len(firstList)`, `n = len(secondList)`。我们要遍历 `m × n` 对区间，时间随这两个长度的乘积增长，用 **O(m·n)** 表示。  
  - 大白话：如果两条列表各有 1000 条区间，最坏情况下要比较 1 000 000 次，明显会慢。  
  - 空间上我们只需要保存答案和少量临时变量，空间复杂度是 **O(1)**（不计输出本身）。

#### 代码（Python）

```python
from typing import List

def interval_intersection_brute(firstList: List[List[int]],
                               secondList: List[List[int]]) -> List[List[int]]:
    """暴力解：枚举所有区间对，找交集"""
    res: List[List[int]] = []

    for a in firstList:                 # 遍历第一个列表的每个区间 a = [a_start, a_end]
        for b in secondList:            # 遍历第二个列表的每个区间 b = [b_start, b_end]
            # 交集的起点是两端点中较大的那个，终点是两端点中较小的那个
            start = max(a[0], b[0])
            end   = min(a[1], b[1])

            # 如果 start <= end，说明真的有交集
            if start <= end:
                res.append([start, end])   # 把交集加入答案

    return res
```

#### 复杂度

- **时间复杂度**：`O(m·n)` — 需要检查每一对区间，乘积级别的增长会让程序在数据稍大时变慢。  
- **空间复杂度**：`O(1)` — 只用常数级别的额外空间（不算返回的结果列表）。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**重复检查**：当我们已经比较过 `firstList[i]` 与 `secondList[j]`，如果两者没有交集，接下来仍然会把 `firstList[i]` 再和 `secondList[j+1]`（或 `firstList[i+1]`）比较，这其实是浪费的。  
因为两个列表本身已经 **按起点排序且内部不相交**，我们可以用 **双指针**（two‑pointers）一次遍历把所有交集找出来，时间只和两条列表的长度之和有关。

关键观察：

1. 两个区间 `[a_start, a_end]` 与 `[b_start, b_end]` 的交集只可能是  
   `max(a_start, b_start)` 到 `min(a_end, b_end)` 这段。  
2. 若 `a_end < b_end`，说明 `a` 这个区间已经“结束”了，它不可能再和后面的 `b` 产生交集，**指针 i 向前移动**（指向下一个 `a`）。反之若 `b_end < a_end`，则移动 `j`。  
3. 只要把指针一直往前推进，所有可能的交集都会被捕获，且每个区间最多被访问一次。

类比：把两条排好序的火车轨道想象成两列火车，指针是两列火车的司机。每当两列火车的车厢重叠（区间相交），就记录下来；随后让结束得更早的那列先离开站台（指针前进），再继续比较。

#### 代码（Python）

```python
from typing import List

def interval_intersection_opt(firstList: List[List[int]],
                              secondList: List[List[int]]) -> List[List[int]]:
    """最优解：双指针一次遍历"""
    i, j = 0, 0               # i 指向 firstList, j 指向 secondList
    res: List[List[int]] = []

    while i < len(firstList) and j < len(secondList):
        a_start, a_end = firstList[i]
        b_start, b_end = secondList[j]

        # 计算交集的左右端点
        start = max(a_start, b_start)
        end   = min(a_end, b_end)

        # 如果 start <= end，说明真的有交集，加入答案
        if start <= end:
            res.append([start, end])

        # 移动结束点更早的区间的指针
        if a_end < b_end:
            i += 1   # firstList 的当前区间已经用完，换下一个
        else:
            j += 1   # secondList 的当前区间已经用完，换下一个

    return res
```

#### 复杂度

- **时间复杂度**：`O(m + n)` — 每个指针最多前进 `len(firstList)` 或 `len(secondList)` 步，总步数不超过两者之和。相较于暴力的 `O(m·n)`，这在数据大时快了好几个数量级。  
- **空间复杂度**：`O(1)` — 只使用了常数级别的额外变量（不计返回列表）。

---

## 心得

- **核心技巧**：双指针（Two Pointers）在两个有序、互不重叠的序列上同步遍历，能够在一次线性扫描中找出所有交集。  
- **适用的题型**：  
  1. 合并两个有序数组（LeetCode 21 – Merge Two Sorted Lists）。  
  2. 找出两个有序区间列表的并集或差集（如 “Interval List Intersections” 的变形）。  
  3. 字符串或数组的滑动窗口交叉问题（如 “Minimum Window Substring” 的简化版）。  
- **一句话总结解题钥匙**：**让结束更早的区间先“退出舞台”，指针只前进不回头**。

---

## 反思

- **第一反应**：看到两个已经排好序且内部不相交的列表，立刻想到可以用“双指针”同步遍历，而不是盲目套用笨拙的双层循环。  
- **最容易踩的坑**：  
  - 忘记判断 `start <= end`（交集可能为空），直接把 `[start, end]` 加入会产生错误的 `[5,4]`。  
  - 错误地移动指针：必须比较两个区间的 **结束点**，而不是起点，否则会遗漏后面的交集。  
  - 边界情况：其中一个列表为空时直接返回空列表。  
- **下次遇到同类题的第一步**：先确认两组数据是否已排序且互不重叠，如果是，立刻考虑使用“双指针”从头到尾一次遍历。