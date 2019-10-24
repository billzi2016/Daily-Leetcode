# #630. 课程表 III / Course Schedule III

> 难度：困难 · 标签：Array、Greedy、Sorting、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/course-schedule-iii/)

---

## 题目（英文原版）

**Description**

There are n different online courses numbered from 1 to n. You are given an array courses where courses[i] = [durationi, lastDayi] indicate that the ith course should be taken continuously for durationi days and must be finished before or on lastDayi.
You will start on the 1st day and you cannot take two or more courses simultaneously.
Return the maximum number of courses that you can take.

**Examples**

**Example 1:**

```
Input: courses = [[100,200],[200,1300],[1000,1250],[2000,3200]]
Output: 3
Explanation: 
There are totally 4 courses, but you can take 3 courses at most:
First, take the 1st course, it costs 100 days so you will finish it on the 100th day, and ready to take the next course on the 101st day.
Second, take the 3rd course, it costs 1000 days so you will finish it on the 1100th day, and ready to take the next course on the 1101st day. 
Third, take the 2nd course, it costs 200 days so you will finish it on the 1300th day. 
The 4th course cannot be taken now, since you will finish it on the 3300th day, which exceeds the closed date.
```

**Example 2:**

```
Input: courses = [[1,2]]
Output: 1
```

**Example 3:**

```
Input: courses = [[3,2],[4,3]]
Output: 0
```

**Constraints**

- 1 <= courses.length <= 104
- 1 <= durationi, lastDayi <= 104

---

## 题目（中文翻译）

有 `n` 门不同的在线课程（online courses），编号为 `1` 到 `n`。给定一个数组 `courses`，其中 `courses[i] = [duration_i, lastDay_i]` 表示第 `i` 门课程需要 **连续** 上 `duration_i` 天，并且必须在 `lastDay_i`（含）之前完成。  
你将在第 `1` 天开始学习，且不能同时学习两门或以上的课程。  
返回你能够选修的课程的 **最大数量**。

## 示例

### 示例 1  
**输入:** `courses = [[100,200],[200,1300],[1000,1250],[2000,3200]]`  
**输出:** `3`  
**解释:**  
总共有 4 门课程，但最多只能选修 3 门：  
1. 首先选第 1 门课程，耗时 100 天，完成于第 100 天，随后可以在第 101 天开始下一门课程。  
2. 接着选第 3 门课程，耗时 1000 天，完成于第 1100 天，随后可以在第 1101 天开始下一门课程。  
3. 再选第 2 门课程，耗时 200 天，完成于第 1300 天。  

第 4 门课程此时无法选修，因为完成时间会是第 3300 天，已超出其截止日期 `lastDay = 3200`。

### 示例 2  
**输入:** `courses = [[1,2]]`  
**输出:** `1`

### 示例 3  
**输入:** `courses = [[3,2],[4,3]]`  
**输出:** `0`

## 约束条件

- `1 <= courses.length <= 10^4`
- `1 <= duration_i, lastDay_i <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的选课方案**，然后挑出能够在规定的最后一天前完成的方案，取其中课程数量最多的那个。  
可以把它想成：

- **每门课程是一件要放进背包的物品**，背包的容量不是固定的，而是每件物品都有自己的“最迟放进去的时间”。  
- 我们要尝试所有把哪些物品放进去、以什么顺序放进去的可能性。

实现上常见的做法是**深度优先搜索（DFS）或回溯**，对每门课决定“选”或“不选”，并在递归里维护已经用掉的天数。如果当前累计天数已经超过了某门课的截止日，就把这条分支剪掉。

> 这里的“选/不选”相当于在**字典**里查找键值：键是“课程编号”，值是“是否选”。字典查找就像查字典，key 是词，value 是对应的解释，查找速度快（O(1)），但我们仍然要遍历所有键。

**为什么这个方法能得到正确答案**  
因为它穷举了所有合法的选课组合，必然会覆盖最优解。只要不漏掉任何一种可能性，答案就一定在其中。

**时间/空间复杂度**  
- **时间复杂度**：对 `n` 门课，每门课有“选”或“不选”两种决定，所有可能的组合数是 `2^n`，因此时间复杂度是 **O(2ⁿ)**。  
  - 大白话：如果有 20 门课，就要检查大约 1,048,576 种情况；如果是 30 门课，就要检查十亿级别的情况，根本跑不完。  
- **空间复杂度**：递归栈的深度最多是 `n`，再加上记录已选课程的集合，空间是 **O(n)**。

显然，这种暴力方案只能用于 `n` 很小（比如 `n ≤ 15`）的玩具数据，面对题目中 `n ≤ 10⁴` 的规模会直接 **超时**。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**枚举顺序是主要的性能瓶颈**。如果我们能够在遍历课程的过程中 **即时决定是否保留当前课程**，而不必回溯，就能把时间从指数级降到多项式级。

**关键观察 1：课程的截止日（lastDay）决定了我们处理的顺序**  
如果两门课的截止日分别是 5 天和 10 天，显然我们应该先考虑 5 天的课，因为它的时间窗口更紧。于是我们把所有课程**按 lastDay 从小到大排序**。这一步保证了“已经决定的课程”永远不会影响后面截止更早的课程的可行性。

**关键观察 2：在已决定的课程集合中，如果总耗时超出了当前课程的截止日，我们可以尝试“换课”**  
设 `total` 为已经选的课程累计天数，`duration` 为当前课程的时长。如果 `total + duration ≤ lastDay`，直接选它，`total += duration`。  
如果 `total + duration > lastDay`，说明现在的课程集合已经“超时”。我们想把 **耗时最长的那门课**换掉，因为：

- 换掉最长的课能最大程度地减小 `total`，从而更有可能让 `total` ≤ `lastDay`。
- 这相当于在已有课程中“挑出一个最重的背包物品”，把它扔掉，再装进当前这件更轻的物品。

要高效地找到已选课程中时长最长的那门课，我们使用 **最大堆（max‑heap）**（在 Python 的 `heapq` 中实现为负数的最小堆），它就像“一个可以随时弹出最大元素的字典”。堆的核心操作 `push`、`pop` 的时间都是 **O(log k)**（k 为堆中元素个数），远快于线性扫描。

**完整算法步骤**  

1. **排序**：把 `courses` 按 `lastDay` 升序排列。  
2. 初始化一个空最大堆 `maxHeap`（存放已选课程的时长，取负数以实现 max‑heap），以及累计天数 `total = 0`。  
3. **遍历** 排好序的每门课程 `(duration, lastDay)`：  
   - 如果 `total + duration ≤ lastDay`：  
     - 直接选课：`total += duration`，`heapq.heappush(maxHeap, -duration)`。  
   - 否则（超时）：  
     - 查看堆顶（即已选课程中时长最长的那门）`longest = -maxHeap[0]`。  
     - 如果 `longest > duration`：  
       - 用当前更短的课换掉最长的课：`total += duration - longest`（相当于 `total = total - longest + duration`），`heapq.heappop(maxHeap)`，`heapq.heappush(maxHeap, -duration)`。  
     - 否则，当前课太长，直接丢弃（不做任何操作）。  
4. 循环结束后，堆的大小即为能够选修的最多课程数。

**为什么这一步步推导是合法的**  

- **排序保证**：因为我们总是先处理截止更早的课程，任何后面出现的课程的 `lastDay` 都不小于当前的 `lastDay`。所以如果在处理某门课时已经满足 `total ≤ lastDay`，以后再加入更宽松的课程时，`total` 只会增大，不会影响已经完成的早期课程的截止。  
- **换课策略的最优性**：假设在超时情况下我们换掉的不是最长的课，而是另一门更短的课。换掉更短的课会让 `total` 减少得更少，仍然可能超时；而换掉最长的课能够让 `total` 最多减少，最有可能恢复可行。因此，**每一次换课都是局部最优且全局不受影响**。  

> 类比：把已经选的课程想象成一个装满石头的背包，背包的容量随时间增长而变小（deadline 越来越紧）。当背包超重时，你总是把最大、最重的石头扔掉，换成更轻的石头，这样背包最容易保持在容量限制内。

#### 代码（Python）

```python
import heapq
from typing import List

def scheduleCourse(courses: List[List[int]]) -> int:
    """
    返回最多可以选修的课程数
    """
    # 1. 按截止日期升序排列
    courses.sort(key=lambda x: x[1])          # x[1] 是 lastDay

    max_heap = []          # 用负数实现的最大堆，存放已选课程的 duration
    total_time = 0        # 已选课程累计耗时

    for duration, last_day in courses:
        # 2. 尝试把当前课程加入计划
        if total_time + duration <= last_day:
            # 还能按时完成，直接加入
            total_time += duration
            heapq.heappush(max_heap, -duration)   # 负号让最小堆变成最大堆
        else:
            # 3. 超时：看看能否换掉已经选的最长课程
            if max_heap and -max_heap[0] > duration:
                # 堆顶是最长课程的时长
                longest = -heapq.heappop(max_heap)   # 弹出最长课程
                total_time += duration - longest      # 用当前更短的课替换
                heapq.heappush(max_heap, -duration)   # 把当前课加入堆
                # 如果 longest <= duration，说明当前课更长，直接丢弃
            # 若没有可换的或换了也不更好，就不选当前课程

    # 堆的大小即为选修的课程数
    return len(max_heap)


# ---------- 简单测试 ----------
if __name__ == "__main__":
    examples = [
        ([[100,200],[200,1300],[1000,1250],[2000,3200]], 3),
        ([[1,2]], 1),
        ([[3,2],[4,3]], 0),
    ]
    for courses, ans in examples:
        res = scheduleCourse(courses)
        print(f"courses={courses} => {res} (expected {ans})")
```

> 关键行中文注释已标注，代码可直接运行。  
> - `heapq.heappush(max_heap, -duration)`：把时长取负后压入最小堆，等价于最大堆。  
> - `-max_heap[0]`：堆顶元素的相反数，就是当前已选课程中最长的时长。

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 排序需要 `O(n log n)`。  
  - 遍历每门课时，堆的 `push`/`pop` 均为 `O(log k)`（`k ≤ n`），整体也是 `O(n log n)`。  
  - 大白话：即使有 10,000 门课，也只会做大约 10,000 次“放进/弹出”堆的操作，每次只需要几百次基本比较，算得上“很快”。

- **空间复杂度**：`O(n)`  
  - 堆里最坏会存下所有被选的课程，最多不超过 `n`。  
  - 额外的 `total_time`、排序后的列表等只占常数级空间。

与暴力解相比，时间从指数级的 `2ⁿ` 降到了对数级的 `log n`，大幅提升了可行性。

---

## 心得

- **核心技巧**：**先按截止日排序 + 用最大堆维护已选课程的最长时长**，实现“贪心换课”。  
- **适用的题型**  
  1. **课程表类**（如 *Course Schedule II*）需要按时间窗口安排任务。  
  2. **任务调度**（如 *Maximum Number of Events That Can Be Attended*）中也会用到“按结束时间排序 + 堆”。  
  3. **背包的变形**（如 *Find the Maximum Number of Non‑Overlapping Intervals*）同样可以用“最长/最短替换”思路。  
- **一句话总结解题钥匙**：  
  > “把最紧迫的任务先排好序，遇到超时就把已选任务里最‘耗时’的踢掉，保证总耗时始终最小。”

---

## 反思

- **第一反应**：看到“每门课都有时长和截止日”，立刻想到**区间调度**或**背包**，于是尝试暴力枚举所有子集。  
- **最容易踩的坑**  
  - **忘记排序**：如果不按 `lastDay` 排序，后面换课可能会破坏已经满足的早期截止，导致错误。  
  - **堆的方向写错**：Python 默认是最小堆，需要取负数实现最大堆，写成正数会导致换掉最短的课，结果不对。  
  - **边界条件**：当 `max_heap` 为空或 `longest <= duration` 时，不能盲目 `pop`，否则会误删已经合法的课程。  
- **下次遇到同类题的第一步**：  
  - **先把所有任务按截止时间排序**，然后思考“如果累计时间超过当前截止，怎样在已选任务中‘最小化’累计时间”。这一步往往直接指向“最大堆换课”或“最小堆挑最早结束”。