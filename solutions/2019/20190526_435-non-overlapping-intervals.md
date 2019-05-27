# #435. 无重叠区间 / Non-overlapping Intervals

> 难度：中等 · 标签：Array、Dynamic Programming、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/non-overlapping-intervals/)

---

## 题目（英文原版）

**Description**

Given an array of intervals intervals where intervals[i] = [starti, endi], return the minimum number of intervals you need to remove to make the rest of the intervals non-overlapping.
Note that intervals which only touch at a point are non-overlapping. For example, [1, 2] and [2, 3] are non-overlapping.

**Examples**

**Example 1:**

```
Input: intervals = [[1,2],[2,3],[3,4],[1,3]]
Output: 1
Explanation: [1,3] can be removed and the rest of the intervals are non-overlapping.
```

**Example 2:**

```
Input: intervals = [[1,2],[1,2],[1,2]]
Output: 2
Explanation: You need to remove two [1,2] to make the rest of the intervals non-overlapping.
```

**Example 3:**

```
Input: intervals = [[1,2],[2,3]]
Output: 0
Explanation: You don't need to remove any of the intervals since they're already non-overlapping.
```

**Constraints**

- 1 <= intervals.length <= 105
- intervals[i].length == 2
- -5 * 104 <= starti < endi <= 5 * 104

---

## 题目（中文翻译）

给定一个区间（interval）数组 `intervals`，其中 `intervals[i] = [starti, endi]`，返回需要删除的最少区间（interval）数，使剩余的区间（interval）全部不重叠。  
注意，端点相接但不产生交叉的区间视为不重叠。例如 `[1, 2]` 与 `[2, 3]` 是不重叠的。

**示例 1：**  
输入: `intervals = [[1,2],[2,3],[3,4],[1,3]]`  
输出: `1`  
解释: 可以删除 `[1,3]`，其余区间均不重叠。

**示例 2：**  
输入: `intervals = [[1,2],[1,2],[1,2]]`  
输出: `2`  
解释: 需要删除两个 `[1,2]`，才能使剩余区间不重叠。

**示例 3：**  
输入: `intervals = [[1,2],[2,3]]`  
输出: `0`  
解释: 已经不重叠，不需要删除任何区间。

**约束条件**  
- `1 <= intervals.length <= 10^5`  
- `intervals[i].length == 2`  
- `-5 * 10^4 <= starti < endi <= 5 * 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每一种可能的删除方式都试一遍**，找出能够让剩下的区间互不重叠且删除次数最少的方案。  
这相当于在原数组里挑选一个子集，使得子集中的所有区间互不重叠，然后把其余的区间全部删除。  

实现思路可以用**回溯（DFS）**或**枚举子集**：

1. 逐个遍历区间，决定「保留」还是「删除」  
2. 当我们决定「保留」时，需要检查它是否和已经保留下来的区间有交叉（交叉判断：`new_start < old_end` 且 `old_start < new_end`），如果冲突则这条路径不合法。  
3. 递归结束时统计已经删除的个数，取最小值。

> **类比**：把每个区间想象成一本书，书桌上只能摆放互不重叠的书。我们要把书桌上最多的书挑出来，剩下的书全都收进抽屉。暴力解就是把每本书都尝试放进或收进抽屉，看看哪种放法能让书桌上的书最多。

> **为什么正确**：因为我们遍历了所有合法的保留方案，最小的删除数一定出现在这些方案中。

> **时间/空间复杂度**：  
> - 每本书（区间）都有两种选择（保留或删除），所以递归树的节点数是 `2^n`，时间复杂度是 **指数级**，记作 `O(2^n)`。  
> - 为了记录已经保留下来的区间，需要一个列表，最坏情况下保存全部 `n` 个区间，空间复杂度是 `O(n)`。  

在 `n ≤ 20` 左右时还能接受，但题目给出的 `n` 可达 `10^5`，显然不可行。

#### 代码（Python）

```python
from typing import List

def eraseOverlapIntervals_bruteforce(intervals: List[List[int]]) -> int:
    n = len(intervals)
    # 为了方便比较，先把区间按起点排序（不影响正确性，只是让递归顺序固定）
    intervals.sort(key=lambda x: x[0])

    best = n  # 最少需要删除的区间数，初始设为最大可能值

    def dfs(idx: int, kept: List[List[int]], removed: int) -> None:
        """递归遍历第 idx 个区间的保留/删除选择"""
        nonlocal best
        # 剪枝：已经比当前最优更差，直接返回
        if removed >= best:
            return
        # 所有区间都决定完毕，更新最优解
        if idx == n:
            best = removed
            return

        cur = intervals[idx]

        # 方案1：删除当前区间
        dfs(idx + 1, kept, removed + 1)

        # 方案2：尝试保留当前区间，先检查是否和已保留的区间冲突
        conflict = False
        for a, b in kept:
            # 两个区间重叠的条件（左闭右开），若仅在端点相接则不算重叠
            if not (cur[1] <= a or cur[0] >= b):
                conflict = True
                break
        if not conflict:
            kept.append(cur)          # 把当前区间加入已保留集合
            dfs(idx + 1, kept, removed)
            kept.pop()                # 回溯，撤销选择

    dfs(0, [], 0)
    return best
```

> 关键行中文注释已写在代码里，直接复制运行即可看到结果（但请在小规模数据上测试，防止爆栈）。

#### 复杂度

- **时间复杂度**：`O(2^n)` —— 每个区间都有「保留」或「删除」两种选择，整体是指数级增长。  
- **空间复杂度**：`O(n)` —— 递归栈最深 `n` 层，加上保存已保留区间的列表。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**枚举所有可能的删除组合**，这会导致指数级的时间。我们需要找到一种**贪心**的策略，只在一次遍历（或一次排序后遍历）中直接得到最少删除数。

**关键观察**：

- 如果我们已经选定了一系列互不重叠的区间，后面再加入一个新区间时，只需要关心它和**最近的已选区间的结束位置**是否冲突。  
- 为了让后面的区间有更大的“活动空间”，**应该尽量让已选区间的结束位置尽可能早**。因为结束早的区间留下的时间段更长，后面的区间更容易放进去。

这正是**“最早结束时间优先”**的思想。实现步骤：

1. **按区间的结束时间 `end` 从小到大排序**。  
   - 类比：在电影院排队买票，先买结束最早的电影票，这样后面还有更多时间可以去看别的电影。  
2. 维护一个变量 `prev_end`，表示**上一次选中的区间的结束位置**。初始设为负无穷（`-inf`），表示还没有选区间。  
3. 依次遍历排好序的区间：  
   - 若当前区间的起点 `start >= prev_end`（即不重叠），我们可以**保留**它，并把 `prev_end` 更新为当前区间的结束位置。  
   - 否则，当前区间与上一个已保留区间重叠，**必须删除**它（因为已经选的区间结束更早，保留它对后面的区间更有利），删除计数 `removed += 1`。  

这样遍历一次即可得到最少需要删除的区间数。

> **为什么正确**（直观证明）：  
> - 已排序的区间列表中，若两个相邻区间 `i`、`j`（`i` 在前）不重叠，则 `end_i ≤ start_j`。  
> - 当我们遇到冲突时，必然是 `start_j < end_i`。此时如果我们把 `i` 删除而保留 `j`，则 `j` 的结束时间一定 **不早于** `i`（因为排序是按结束时间升序），于是后面的可选区间范围不会比保留 `i` 更大。换句话说，保留结束更早的区间对后续的选择最有利。  
> - 通过归纳（每一步都做最优选择），整个过程得到的保留集合是最大的非重叠子集，删除的最少。

> **时间/空间复杂度**：  
> - 排序需要 `O(n log n)`，遍历一次是 `O(n)`，整体 `O(n log n)`。  
> - 只用了几个额外的整数变量，空间 `O(1)`（不计输入本身）。

#### 代码（Python）

```python
from typing import List

def eraseOverlapIntervals(intervals: List[List[int]]) -> int:
    """
    贪心：先把区间按结束位置排序，每次尽量保留结束最早且不与前一个已保留区间重叠的区间。
    返回最少需要删除的区间数。
    """
    if not intervals:
        return 0

    # 1. 按结束时间升序排列
    intervals.sort(key=lambda x: x[1])   # x[1] 是区间的 end

    removed = 0          # 记录删除的区间个数
    prev_end = float('-inf')   # 上一个被保留区间的结束位置

    for start, end in intervals:
        # 2. 若当前区间的起点不早于上一个保留区间的结束点，则可以保留
        if start >= prev_end:
            prev_end = end          # 更新最近的结束位置
        else:
            # 3. 与上一个保留区间重叠，只能删除当前区间
            removed += 1

    return removed
```

> 关键行解释：
> - `intervals.sort(key=lambda x: x[1])`：把区间像排队一样，先让结束最早的站前面。
> - `if start >= prev_end:`：只有当“新来的区间开始时间不早于前面那个已经站好的区间结束时间”时，才可以让它进队。
> - `removed += 1`：否则只能让它离开（删除），因为我们已经选了更有利的前面那个区间。

#### 复杂度

- **时间复杂度**：`O(n log n)` —— 主要来源于排序，`n` 为区间个数。相比暴力的指数级，这已经是可以接受的线性对数级别。  
- **空间复杂度**：`O(1)` —— 只用了常数个额外变量（排序本身如果使用原地排序则不计额外空间）。

---

## 心得

- **核心技巧**：**“最早结束时间优先的贪心”**（也叫 **区间调度问题** 的经典解法）。  
- **适用的题型**（类似思路可直接迁移）：  
  1. **LC 435** – Non-overlapping Intervals（本题）  
  2. **LC 452** – Minimum Number of Arrows to Burst Balloons（把气球视作区间）  
  3. **LC 1005** – Maximize Number of Non-Overlapping Subarrays（子数组视作区间）  
- **一句话总结解题钥匙**：**“让已选区间尽可能早结束，后面的区间才有最大自由度”。**

---

## 反思

- **第一反应**：看到“删除最少区间使剩余不重叠”，本能想到“保留最多不重叠的区间”。于是联想到“子集最大化”，于是想到枚举/动态规划。  
- **最容易踩的坑**：  
  - 忽视 **“只在端点相接算不重叠”** 的细节，导致冲突判断写成 `start < prev_end`（漏等号）而产生错误答案。  
  - 在贪心实现时，如果忘记先 **按结束时间排序**，直接按起点排序会得到错误的最小删除数。  
  - 大数据量时，递归/DP 可能导致栈溢出或超时，必须切换到 `O(n log n)` 的贪心。  
- **下次遇到同类题**，第一步应该：**“把区间按结束时间排序”，然后用一次遍历检查是否冲突并计数”。** 这一步往往能直接给出最优解。