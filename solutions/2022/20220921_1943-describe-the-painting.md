# #1943. 描述绘画 / Describe the Painting

> 难度：中等 · 标签：Array、Hash Table、Sorting、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/describe-the-painting/)

---

## 题目（英文原版）

**Description**

There is a long and thin painting that can be represented by a number line. The painting was painted with multiple overlapping segments where each segment was painted with a unique color. You are given a 2D integer array segments, where segments[i] = [starti, endi, colori] represents the half-closed segment [starti, endi) with colori as the color.
The colors in the overlapping segments of the painting were mixed when it was painted. When two or more colors mix, they form a new color that can be represented as a set of mixed colors.
For the sake of simplicity, you should only output the sum of the elements in the set rather than the full set.
You want to describe the painting with the minimum number of non-overlapping half-closed segments of these mixed colors. These segments can be represented by the 2D array painting where painting[j] = [leftj, rightj, mixj] describes a half-closed segment [leftj, rightj) with the mixed color sum of mixj.
Return the 2D array painting describing the finished painting (excluding any parts that are not painted). You may return the segments in any order.
A half-closed segment [a, b) is the section of the number line between points a and b including point a and not including point b.

**Examples**

**Example 1:**

```
Input: segments = [[1,4,5],[4,7,7],[1,7,9]]
Output: [[1,4,14],[4,7,16]]
Explanation: The painting can be described as follows:
- [1,4) is colored {5,9} (with a sum of 14) from the first and third segments.
- [4,7) is colored {7,9} (with a sum of 16) from the second and third segments.
```

**Example 2:**

```
Input: segments = [[1,7,9],[6,8,15],[8,10,7]]
Output: [[1,6,9],[6,7,24],[7,8,15],[8,10,7]]
Explanation: The painting can be described as follows:
- [1,6) is colored 9 from the first segment.
- [6,7) is colored {9,15} (with a sum of 24) from the first and second segments.
- [7,8) is colored 15 from the second segment.
- [8,10) is colored 7 from the third segment.
```

**Example 3:**

```
Input: segments = [[1,4,5],[1,4,7],[4,7,1],[4,7,11]]
Output: [[1,4,12],[4,7,12]]
Explanation: The painting can be described as follows:
- [1,4) is colored {5,7} (with a sum of 12) from the first and second segments.
- [4,7) is colored {1,11} (with a sum of 12) from the third and fourth segments.
Note that returning a single segment [1,7) is incorrect because the mixed color sets are different.
```

**Constraints**

- 1 <= segments.length <= 2 * 104
- segments[i].length == 3
- 1 <= starti < endi <= 105
- 1 <= colori <= 109
- Each colori is distinct.

---

## 题目（中文翻译）

**描述**  
有一幅可以用数轴表示的细长画作。画作是由多段相互重叠的线段构成的，每段线段使用唯一的颜色进行绘制。给定一个二维整数数组 `segments`，其中 `segments[i] = [start_i, end_i, color_i]` 表示左闭右开线段 **[start_i, end_i)**，颜色为 `color_i`。  

在绘制过程中，重叠部分的颜色会混合。当两种或以上颜色混合时，会形成一个可以用混合颜色集合（set of mixed colors）表示的新颜色。为简化起见，只需要输出该集合中元素的**和**（sum），而不是完整的集合本身。  

你的任务是用**最少数量的**互不重叠的左闭右开线段来描述这幅画的混合颜色。这些线段可以用二维数组 `painting` 表示，其中 `painting[j] = [left_j, right_j, mix_j]` 描述左闭右开线段 **[left_j, right_j)**，其混合颜色的和为 `mix_j`。  

返回描述完整画作的二维数组 `painting`（不包括未被涂色的部分），返回的线段顺序任意即可。  

**左闭右开线段** **[a, b)** 表示数轴上从点 `a` 到点 `b` 的区间，包含点 `a` 而不包含点 `b`。

---

### 示例

**示例 1**  
```text
Input: segments = [[1,4,5],[4,7,7],[1,7,9]]
Output: [[1,4,14],[4,7,16]]
Explanation: 这幅画可以描述为：
- [1,4) 的颜色集合为 {5,9}，其和为 14（来源于第 1 段和第 3 段）。
- [4,7) 的颜色集合为 {7,9}，其和为 16（来源于第 2 段和第 3 段）。
```

**示例 2**  
```text
Input: segments = [[1,7,9],[6,8,15],[8,10,7]]
Output: [[1,6,9],[6,7,24],[7,8,15],[8,10,7]]
Explanation: 这幅画可以描述为：
- [1,6) 的颜色为 9，来源于第 1 段。
- [6,7) 的颜色集合为 {9,15}，其和为 24，来源于第 1、2 段。
- [7,8) 的颜色为 15，来源于第 2 段。
- [8,10) 的颜色为 7，来源于第 3 段。
```

**示例 3**  
```text
Input: segments = [[1,4,5],[1,4,7],[4,7,1],[4,7,11]]
Output: [[1,4,12],[4,7,12]]
Explanation: 这幅画可以描述为：
- [1,4) 的颜色集合为 {5,7}，其和为 12，来源于第 1、2 段。
- [4,7) 的颜色集合为 {1,11}，其和为 12，来源于第 3、4 段。
注意，返回单个线段 [1,7) 是错误的，因为两段的混合颜色集合不同。
```

---

### 约束条件
- `1 <= segments.length <= 2 * 10^4`
- `segments[i].length == 3`
- `1 <= start_i < end_i <= 10^5`
- `1 <= color_i <= 10^9`
- 每个 `color_i` 均不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每条线段拆成最小的“单位格子”，比如把坐标轴离散到每个整数点（或每个可能的坐标），然后逐格子统计有多少颜色覆盖，最后把相邻颜色和相同的格子合并成一个大区间。

- **数据结构**：我们可以用一个哈希表（在 Python 里就是 `dict`）来记每个坐标点对应的颜色和。哈希表就像一本**查字典**，键（key）是坐标，值（value）是该坐标上所有颜色的和。
- **为什么正确**：因为每个格子都被所有覆盖它的线段遍历一次，累加它们的颜色，最后得到的每个格子的颜色和一定等于题目要求的“混合颜色的和”。

**缺点**：如果坐标范围很大（题目中 `end` 最多到 `10^5`），我们需要遍历每一个整数点，时间会是 `O(range * n)`，在最坏情况下相当于 `O(10^5 * 2·10^4)`，根本跑不动。

#### 代码（Python）

```python
def describePainting_bruteforce(segments):
    # 用 dict 记录每个整数坐标点的颜色和
    color_sum = {}
    for l, r, c in segments:
        for x in range(l, r):          # 逐个整数格子遍历
            color_sum[x] = color_sum.get(x, 0) + c

    # 合并相邻坐标点，得到最小不重叠区间
    painting = []
    prev_x = None
    prev_sum = None
    for x in sorted(color_sum):
        cur_sum = color_sum[x]
        if prev_x is None:                 # 第一个点
            prev_x, prev_sum = x, cur_sum
        elif cur_sum != prev_sum:          # 颜色和变了，结束上一段
            painting.append([prev_x, x, prev_sum])
            prev_x, prev_sum = x, cur_sum
    # 记得把最后一段也加进去
    if prev_x is not None:
        painting.append([prev_x, max(color_sum)+1, prev_sum])
    return painting
```

> 关键行的中文注释已经写在代码里。

#### 复杂度  

- **时间复杂度**：`O(L * n)`，其中 `L` 是坐标轴的最大长度（最多 `10^5`），`n` 是线段数量。可以把 `O(L * n)` 想象成“每条线段都要走完整条路”，显然太慢了。  
- **空间复杂度**：`O(L)`，需要存储每个整数坐标的颜色和，同样随坐标范围线性增长。

---

### 2. 最优解

#### 思路  

暴力解慢的根源在于 **“逐格子遍历”**，我们其实不需要关心每一个单独的整数，只需要关心 **颜色和会改变的地方**——也就是所有线段的起点和终点。  

把所有起点、终点看成时间轴上的“事件”，每个事件会让当前的颜色和 **增加**（起点）或 **减少**（终点）。只要把这些事件按坐标从左到右排好序，顺序扫描一遍，就能实时维护「当前区间的颜色和」。  

- **核心算法**：**扫描线（Sweep Line）** + **前缀和**。  
- **数据结构**：我们仍然使用哈希表或列表来保存 **事件**，每个事件是 `(位置, 颜色增量)`。在 Python 中，用列表 `events = []`，随后 `events.sort()` 按位置排序。  
- **类比**：想象你在一条路上行走，路上有加油站（起点）会给你加油（颜色），也有出站口（终点）会把油倒掉。当你走到下一个站点时，你先记下从上一个站点到现在这段路上车里有多少油（颜色和），然后再根据站点的加减来更新车里的油量。这样走完整条路，就得到每段路上油量的变化区间。

**步骤细化**：

1. **收集事件**  
   对每个线段 `[l, r, c]`，在 `l` 位置放 `+c`，在 `r` 位置放 `-c`。  
2. **排序**  
   把所有事件按坐标升序排列。若同一坐标有多条事件，先把它们全部累加（因为在同一点上同时进入和离开不会产生长度为 0 的区间）。
3. **扫描**  
   - 用变量 `cur_sum` 保存当前颜色和，初始为 `0`。  
   - 用变量 `prev` 记录上一次处理完事件后的位置。  
   - 对每个事件坐标 `x`：  
     - 如果 `prev` 与 `x` 不同且 `cur_sum > 0`，说明区间 `[prev, x)` 被至少一条线段覆盖，颜色和就是 `cur_sum`，把它加入答案。  
     - 把所有在 `x` 位置的增量全部加到 `cur_sum`（即 `cur_sum += delta_sum_at_x`）。  
     - 更新 `prev = x`，继续下一个坐标。  
4. **返回答案**  
   结果已经是最小的不重叠区间，顺序可以随意。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def describePainting(segments: List[List[int]]) -> List[List[int]]:
    """
    扫描线 + 前缀和实现
    时间复杂度 O(n log n)   n 为线段数量
    空间复杂度 O(n)         只存事件列表
    """
    # 1. 收集所有事件：位置 -> 颜色增量（可能有多个事件在同一位置）
    events = defaultdict(int)          # 用 dict 累加同一坐标的增量
    for l, r, c in segments:
        events[l] += c                  # 起点，颜色加入
        events[r] -= c                  # 终点，颜色离开

    # 2. 把坐标排序
    sorted_pos = sorted(events.keys())

    cur_sum = 0          # 当前区间的颜色和
    prev = None          # 上一次处理完事件后的坐标
    ans = []

    for x in sorted_pos:
        # 3. 先把上一段（[prev, x)）的结果记下来
        if prev is not None and cur_sum > 0 and prev < x:
            ans.append([prev, x, cur_sum])

        # 4. 更新当前颜色和
        cur_sum += events[x]

        # 5. 移动 prev 指针
        prev = x

    return ans
```

> 关键行已用中文注释解释，直接复制即可运行。

#### 复杂度  

- **时间复杂度**：`O(n log n)`。  
  - 收集事件是线性 `O(n)`，  
  - 排序所有坐标需要 `O(m log m)`，其中 `m ≤ 2n`（每条线段产生两个事件），所以整体是 `O(n log n)`。  
  - 可以把 `O(n log n)` 想象成“把 n 条线段的端点排队”，这比逐格子遍历要快得多。  
- **空间复杂度**：`O(n)`。我们只保存 `2n` 个事件（起点和终点），以及答案列表。  

与暴力解相比，时间从可能的 `10^9` 级别降到几万级别，完全可以在限制内跑完。

---

## 心得

- **核心技巧**：**扫描线（Sweep Line）** + **前缀和**，把“区间覆盖”问题转化为“事件的增减”。  
- **适用的题型**  
  1. 区间求和或求交并（如 “Merge Intervals”, “Maximum Overlap of Intervals”）。  
  2. 统计某点被多少区间覆盖（如 “Count of Smaller Numbers After Self” 的离线版本）。  
  3. 颜色或权重叠加类题目（本题的“颜色混合”即是权重叠加）。  
- **一句话总结**：**只在端点上做加减，扫描一次即可得到所有不变区间**。

---

## 反思

- **第一反应**：看到“重叠的颜色要混合”，自然想到把每个小格子都算一遍——这就是暴力思路。  
- **最容易踩的坑**  
  - **同一坐标有多条事件**：如果不先把它们累加，就会错误地把长度为 0 的区间记录进答案。  
  - **空白区域**：`cur_sum == 0` 时说明没有任何颜色覆盖，必须跳过，否则会输出不该出现的区间。  
  - **返回顺序**：题目允许任意顺序，但如果在面试中需要有序输出，记得在最后 `ans.sort()`。  
- **下次类似题**：第一步先 **收集所有端点**，把它们排序，**在端点之间做前缀和**，这样就能把“区间变化”全部捕捉到。