# #1288. 移除被覆盖的区间 / Remove Covered Intervals

> 难度：中等 · 标签：Array、Sorting · [LeetCode 链接](https://leetcode.com/problems/remove-covered-intervals/)

---

## 题目（英文原版）

**Description**

Given an array intervals where intervals[i] = [li, ri] represent the interval [li, ri), remove all intervals that are covered by another interval in the list.
The interval [a, b) is covered by the interval [c, d) if and only if c <= a and b <= d.
Return the number of remaining intervals.

**Examples**

**Example 1:**

```
Input: intervals = [[1,4],[3,6],[2,8]]
Output: 2
Explanation: Interval [3,6] is covered by [2,8], therefore it is removed.
```

**Example 2:**

```
Input: intervals = [[1,4],[2,3]]
Output: 1
```

**Constraints**

- 1 <= intervals.length <= 1000
- intervals[i].length == 2
- 0 <= li < ri <= 105
- All the given intervals are unique.

---

## 题目（中文翻译）

给定一个数组 **intervals**，其中 `intervals[i] = [l_i, r_i]` 表示区间 `[l_i, r_i)`（左闭右开区间），请删除列表中所有被其他区间覆盖的区间。  
区间 `[a, b)` 当且仅当存在区间 `[c, d)` 使得 `c <= a` 且 `b <= d` 时，称其被 `[c, d)` **覆盖**（covered）。  
返回删除操作后剩余区间的数量。

**示例 1**  
**输入**: `intervals = [[1,4],[3,6],[2,8]]`  
**输出**: `2`  
**解释**: 区间 `[3,6)` 被 `[2,8)` 覆盖，故被移除。

**示例 2**  
**输入**: `intervals = [[1,4],[2,3]]`  
**输出**: `1`

**约束条件**  
- `1 <= intervals.length <= 1000`  
- `intervals[i].length == 2`  
- `0 <= l_i < r_i <= 10^5`  
- 所有给定的区间互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**两两比较**：把每一个区间 `i` 与列表中其余所有区间 `j`（`j ≠ i`）逐个比对，判断 `i` 是否被 `j` 完全覆盖。  
- **数据结构**：我们只需要把区间存进普通的 Python 列表 `intervals`，每个元素本身就是 `[l, r]`。可以把它想象成一本“时间表”，每一行记着一次活动的起止时间。  
- **覆盖的判定**：区间 `[a, b)` 被 `[c, d)` 覆盖，当且仅当 `c ≤ a` 并且 `b ≤ d`。这就像判断一本书的章节是否完全包含在另一章节里：起点不早，终点不晚。  
- **为什么正确**：只要我们把每个区间和**所有**其它区间比较一次，就一定能找到是否有某个区间把它完整包住。若找到了，就把它标记为“被覆盖”。遍历结束后，未被标记的区间就是剩下的区间。

#### 代码（Python）

```python
from typing import List

def remove_covered_intervals_bruteforce(intervals: List[List[int]]) -> int:
    n = len(intervals)
    # 用一个布尔数组记录每个区间是否被覆盖，初始都为 False
    covered = [False] * n

    # 两层循环，两两比较
    for i in range(n):
        if covered[i]:                     # 已经确认被覆盖，就可以跳过
            continue
        for j in range(n):
            if i == j:
                continue                  # 同一个区间不用比较
            # 判断 intervals[i] 是否被 intervals[j] 完全覆盖
            if intervals[j][0] <= intervals[i][0] and intervals[i][1] <= intervals[j][1]:
                covered[i] = True          # 标记 i 被覆盖
                break                      # 找到一个覆盖者即可停止内层循环

    # 统计没有被标记为 True 的区间数量
    return sum(not c for c in covered)
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  解释：我们用了两层循环，外层遍历 `n` 次，内层最坏情况下也要遍历 `n` 次，所以总操作次数大约是 `n × n`，即 `n²`。如果把 `n` 想象成 1000，那么 `n²` 大约是 1,000,000 次，计算机依然能接受，但当 `n` 变成 10⁵ 时就会变得非常慢。  
- **空间复杂度**：`O(n)`  
  解释：我们额外用了一个长度为 `n` 的布尔数组 `covered` 来记录状态，除此之外没有其它随 `n` 增长的额外空间。  

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**重复比较**：同样的区间会被比较很多次。我们可以通过**先排序**来把比较次数压到线性级别。

1. **排序**  
   - 首先把所有区间按左端点 `l` **升序**排列；左端点相同的情况下，按右端点 `r` **降序**排列。  
   - 这样排好以后，**左端点更小的区间一定在前面**，如果左端点相同，**右端点更大的（即更“宽”）会在前面**。这正好满足“宽的先出现，窄的后出现”的需求。

2. **一次遍历**  
   - 维护一个变量 `right_max`，表示目前遍历过的区间中**最大的右端点**。  
   - 依次遍历排好序的区间 `(l, r)`：  
     - 如果当前区间的右端点 `r` **小于等于** `right_max`，说明它被之前的某个区间（左端点更小且右端点更大）完全覆盖，直接忽略。  
     - 否则，它没有被覆盖，计数加一，同时更新 `right_max = r`，因为它的右端点是目前最大的。

3. **为什么有效**  
   - 由于左端点已经从小到大，任何后面的区间的左端点都 **不小于** 前面的左端点。  
   - 当出现左端点相同、右端点更大的区间在前面时，后面的区间一定会被前面的覆盖（右端点更小），因此只要检查右端点是否不超过 `right_max` 就足够了。  

4. **类比**  
   - 想象你在排队看电影，先把排片时间最早且放映时间最长的电影放在最前面。之后每来一部电影，如果它的结束时间早于或等于前面已经看过的最长结束时间，那它一定被前面的电影“覆盖”，不需要再计数。

#### 代码（Python）

```python
from typing import List

def remove_covered_intervals(intervals: List[List[int]]) -> int:
    # 1️⃣ 按左端点升序、右端点降序排序
    intervals.sort(key=lambda x: (x[0], -x[1]))
    # 2️⃣ 初始化计数和当前最大的右端点
    count = 0          # 记录未被覆盖的区间数量
    right_max = -1     # 因为所有 ri ≥ 0，-1 可以视作“还没有出现任何区间”

    # 3️⃣ 线性遍历
    for l, r in intervals:
        # 如果当前区间的右端点不大于已出现的最大右端点，说明被覆盖
        if r <= right_max:
            # 被覆盖，直接跳过
            continue
        # 否则，这个区间没有被覆盖，计数加一并更新 right_max
        count += 1
        right_max = r

    return count
```

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  解释：排序是这道题的主要耗时，排序算法（如 Timsort）在最坏情况下需要 `n log n` 次比较和交换。遍历一次的 `O(n)` 与排序相比可以忽略不计。对于 `n = 1000`，`log₂1000 ≈ 10`，所以总操作大约是 10,000 次，远快于暴力的 1,000,000 次。  
- **空间复杂度**：`O(1)`（不计排序时的递归栈）  
  解释：我们只用了常数个额外变量 `count`、`right_max`，并且 Python 的原地排序在大多数实现里只占 `O(1)` 额外空间（内部使用少量临时变量）。  

---

## 心得

- **核心技巧**：先排序再线性扫描，利用“左端点递增、右端点递减”的顺序把“覆盖”关系压缩成一次比较。  
- **适用的题型**  
  1. **合并区间**（Merge Intervals）——先排序后遍历合并重叠区间。  
  2. **最长递增子序列的区间版**（Maximum Length of Pair Chain）——同样需要按左端点升序、右端点降序排序。  
  3. **矩形面积并**（Rectangle Area II）——利用排序和扫描线思想处理覆盖关系。  
- **一句话总结**：**把宽的区间排在前面，右端点的最大值就能“一眼看出”后面的区间是否被覆盖。**

---

## 反思

- **第一反应**：直接想到两层循环把每个区间和所有其它区间比较，写出暴力实现。  
- **最容易踩的坑**  
  - **排序的细节**：左端点相同的区间必须把右端点大的放前面，否则会误把宽的区间当成被覆盖。  
  - **右端点相等的情况**：`r <= right_max` 包含等号是必须的，因为相等也算被覆盖（左端点更小或相同，右端点不大于）。  
  - **空列表或单元素**：虽然题目保证至少有一个区间，但写通用代码时仍需考虑 `right_max` 初始值的设定。  
- **下次遇到同类题**：第一步先**排序**（通常是左端点升序、右端点降序），然后**用一个变量记录已遍历区间的“最强”属性**（如最大右端点），再进行一次线性扫描即可。