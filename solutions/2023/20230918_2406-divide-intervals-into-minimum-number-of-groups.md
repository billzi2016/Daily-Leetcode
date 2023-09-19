# #2406. 将区间划分为最少组数 / Divide Intervals Into Minimum Number of Groups

> 难度：中等 · 标签：Array、Two Pointers、Greedy、Sorting、Heap (Priority Queue)、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/divide-intervals-into-minimum-number-of-groups/)

---

## 题目（英文原版）

**Description**

You are given a 2D integer array intervals where intervals[i] = [lefti, righti] represents the inclusive interval [lefti, righti].
You have to divide the intervals into one or more groups such that each interval is in exactly one group, and no two intervals that are in the same group intersect each other.
Return the minimum number of groups you need to make.
Two intervals intersect if there is at least one common number between them. For example, the intervals [1, 5] and [5, 8] intersect.

**Examples**

**Example 1:**

```
Input: intervals = [[5,10],[6,8],[1,5],[2,3],[1,10]]
Output: 3
Explanation: We can divide the intervals into the following groups:
- Group 1: [1, 5], [6, 8].
- Group 2: [2, 3], [5, 10].
- Group 3: [1, 10].
It can be proven that it is not possible to divide the intervals into fewer than 3 groups.
```

**Example 2:**

```
Input: intervals = [[1,3],[5,6],[8,10],[11,13]]
Output: 1
Explanation: None of the intervals overlap, so we can put all of them in one group.
```

**Constraints**

- 1 <= intervals.length <= 105
- intervals[i].length == 2
- 1 <= lefti <= righti <= 106

---

## 题目（中文翻译）

你得到一个二维整数数组 `intervals`，其中 `intervals[i] = [left_i, right_i]` 表示闭区间 `[left_i, right_i]`。  
你需要将这些区间划分为一个或多个组，使得每个区间恰好属于一个组，并且同一组内的任意两个区间互不相交（intersect）。  
返回所需的最小组数。

两个区间相交，如果它们之间至少有一个公共的整数。例如区间 `[1, 5]` 与 `[5, 8]` 相交。

示例 1:  
Input: intervals = [[5,10],[6,8],[1,5],[2,3],[1,10]]  
Output: 3  
Explanation: 我们可以将区间划分为以下三组：  
- 组 1: `[1, 5]`, `[6, 8]`。  
- 组 2: `[2, 3]`, `[5, 10]`。  
- 组 3: `[1, 10]`。  
可以证明，无法用少于 3 组来划分这些区间。

示例 2:  
Input: intervals = [[1,3],[5,6],[8,10],[11,13]]  
Output: 1  
Explanation: 所有区间互不重叠，因而可以放在同一组中。

约束条件：  
- 1 ≤ `intervals.length` ≤ 10⁵  
- `intervals[i].length` == 2  
- 1 ≤ `left_i` ≤ `right_i` ≤ 10⁶

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是**枚举每一个时间点**，看有多少区间在这个点上“活着”。  
- 把每个区间 `[l, r]` 看成一本书的借阅记录，`l` 是借出日期，`r` 是归还日期。  
- 如果我们把所有日期从最小到最大逐个检查，统计在该日期仍在借阅的书本数目，那么**最高的借阅数量**就是我们最少需要多少个“书架”（即组）。  

实现上可以这样做：  
1. 对每个区间的左端点 `l` 加 `+1`，右端点 `r` 加 `-1`（注意题目里区间是闭区间，右端点要在 `r+1` 位置减）。  
2. 把所有的“增减”操作按时间顺序累加，得到每个时刻的当前重叠数。  
3. 取所有时刻的最大值，就是答案。  

> 这里用到的 **前缀和**（prefix sum）可以类比为“每天的净增人数”。  
> 把“左端点是借出，右端点+1 是归还”想象成每天进出的人数，累计起来就知道任何一天有多少人在场。

为什么这个方法一定正确？  
- 任意时刻的重叠数等价于 **同时进行的区间数**。  
- 把所有区间都放进最少的组，其实就是让每个组在同一时刻只容纳一个区间。因此需要的组数 **至少** 要和最高的同时重叠数一样多；同时我们可以把每个区间按照上述“进出”顺序安排到对应的组，恰好能达到这个上限，所以等号成立。

#### 代码（Python）  
```python
from typing import List

def min_groups_brute(intervals: List[List[int]]) -> int:
    # 记录每个时间点的增减变化，使用字典可以避免创建太大的数组
    diff = {}
    for l, r in intervals:
        diff[l] = diff.get(l, 0) + 1          # 左端点出现一次，重叠数 +1
        diff[r + 1] = diff.get(r + 1, 0) - 1  # 右端点的下一位出现一次，重叠数 -1

    # 把所有关键时间点排序，模拟前缀和的累加过程
    cur = 0          # 当前时刻的重叠数
    ans = 0          # 记录最大重叠数
    for point in sorted(diff):
        cur += diff[point]   # 累加增减值
        ans = max(ans, cur)  # 更新最大值

    return ans
```

#### 复杂度  
- **时间复杂度**：`O(n log n)`  
  - 我们遍历 `n` 个区间一次得到增减表 `O(n)`。  
  - 然后对所有关键点（至多 `2n` 个）排序，花费 `O(n log n)`。  
- **空间复杂度**：`O(n)`  
  - 需要存储每个左端点和右端点+1 的增减值，最坏情况有 `2n` 条记录。  

> **大白话**：  
> - `O(n log n)` 就像把 `n` 张卡片排成有序的队列，需要比较 `log n` 次才能把每张卡放好。  
> - `O(n)` 的空间相当于我们只需要跟踪 `n` 条信息，和原始输入规模是同级的。  

---

### 2. 最优解  

#### 思路  
暴力解的瓶颈在 **排序** 所有关键点后仍要遍历全部点，时间上已经是 `O(n log n)`，这已经是理论上最好的复杂度（因为至少要把区间按左端点排序才能判断冲突）。  
不过我们可以把实现写得更直观：**先把所有区间按左端点升序排好**，然后用一个**最小堆**（优先队列）维护当前每个组的“最早结束时间”。  

思路步骤如下：

1. **把区间左端点从小到大排序**。这相当于把所有任务按开始时间排好队，先到的先考虑。  
2. 维护一个**最小堆**，堆顶始终是**当前所有组中最早结束的那个区间的右端点**。  
   - 堆的意义类似“每个组最后一次使用的时间”。  
3. 依次遍历排序后的区间 `curr = [l, r]`：  
   - 如果 `curr.l` **大于** 堆顶的右端点（即 `curr` 开始时间在最早结束的组之后），说明可以把 `curr` 放进那个组，**弹出堆顶**（旧的结束时间不再需要），再把 `curr.r` **压入堆中**（更新该组的最新结束时间）。  
   - 否则，`curr` 与所有已有组都有冲突，需要 **新建一个组**，直接把 `curr.r` 放进堆里（堆的大小自然会增大）。  
4. 遍历结束后，**堆的大小**就是需要的最小组数。  

> 为什么最小堆能工作？  
> - 堆顶是“最早结束的组”，如果当前区间能放进去，它一定是**最安全的选择**（不会阻碍后面的区间），这是一种**贪心**策略。  
> - 这和我们在电影院安排放映厅的思路相同：先把最早结束的放映厅腾出来，再安排新的电影。

#### 代码（Python）  
```python
import heapq
from typing import List

def min_groups(intervals: List[List[int]]) -> int:
    # 1️⃣ 按左端点升序排列
    intervals.sort(key=lambda x: x[0])

    # 2️⃣ 用最小堆维护每个组的最新结束时间
    min_heap = []          # 堆中存放的是每个组当前的 right 边界

    for l, r in intervals:
        # 3️⃣ 如果当前区间的左端点 > 堆顶（最早结束的组），可以复用该组
        if min_heap and l > min_heap[0]:
            heapq.heappop(min_heap)   # 把旧的结束时间弹出，表示该组已被占用
        # 4️⃣ 把当前区间的右端点加入堆，代表这个组现在的最新结束时间
        heapq.heappush(min_heap, r)

    # 堆的大小就是需要的最少组数
    return len(min_heap)
```

#### 复杂度  
- **时间复杂度**：`O(n log n)`  
  - 排序 `O(n log n)`。  
  - 每个区间在堆中最多一次 `push`、一次 `pop`，每次操作都是 `O(log k)`，其中 `k` ≤ `n`，整体仍是 `O(n log n)`。  
- **空间复杂度**：`O(n)`（最坏情况所有区间都互相重叠，需要 `n` 个组，堆里会保存 `n` 个右端点）。

> 与暴力解相比，时间复杂度相同但实现更直观，且不需要额外的“差分表”。在实际面试中，**堆+贪心** 是最常见的思路，容易写出易懂的代码。

---

## 心得  

- **核心技巧**：把“最少组数”转化为“同一时刻最大重叠数”，用**扫描线 / 前缀和**或**最小堆贪心**求解。  
- **适用题型**  
  1. **会议室 II**（LeetCode 253）：需要最少会议室数。  
  2. **Maximum Number of Overlapping Intervals**：求最大同时进行的区间数。  
  3. **CPU Scheduling** 类似的资源分配问题。  
- **一句话总结**：**把每个区间看成“进/出”，最大同时在场的数量就是答案**。  

---

## 反思  

- **第一反应**：先想到“把所有时间点都列出来，逐点计数”。这就是差分表 + 前缀和的雏形。  
- **最容易踩的坑**  
  - 区间是**闭区间**，所以右端点的“离开”要在 `right + 1` 位置处理，否则 `[1,5]` 与 `[5,8]` 会被误判为不相交。  
  - 堆贪心里比较的条件必须是 **`l > heap[0]`**（严格大于），因为相等时仍然会有交点（题目说交点也算相交）。  
- **下次思路**：看到“把区间划分到不冲突的组”，立刻想到 **“最大重叠数 = 最少组数”**，第一步就尝试 **扫描线** 或 **堆**，而不是先暴力枚举所有点。