# #2187. 完成所有行程的最少时间 / Minimum Time to Complete Trips

> 难度：中等 · 标签：Array、Binary Search · [LeetCode 链接](https://leetcode.com/problems/minimum-time-to-complete-trips/)

---

## 题目（英文原版）

**Description**

You are given an array time where time[i] denotes the time taken by the ith bus to complete one trip.
Each bus can make multiple trips successively; that is, the next trip can start immediately after completing the current trip. Also, each bus operates independently; that is, the trips of one bus do not influence the trips of any other bus.
You are also given an integer totalTrips, which denotes the number of trips all buses should make in total. Return the minimum time required for all buses to complete at least totalTrips trips.

**Examples**

**Example 1:**

```
Input: time = [1,2,3], totalTrips = 5
Output: 3
Explanation:
- At time t = 1, the number of trips completed by each bus are [1,0,0]. 
  The total number of trips completed is 1 + 0 + 0 = 1.
- At time t = 2, the number of trips completed by each bus are [2,1,0]. 
  The total number of trips completed is 2 + 1 + 0 = 3.
- At time t = 3, the number of trips completed by each bus are [3,1,1]. 
  The total number of trips completed is 3 + 1 + 1 = 5.
So the minimum time needed for all buses to complete at least 5 trips is 3.
```

**Example 2:**

```
Input: time = [2], totalTrips = 1
Output: 2
Explanation:
There is only one bus, and it will complete its first trip at t = 2.
So the minimum time needed to complete 1 trip is 2.
```

**Constraints**

- 1 <= time.length <= 105
- 1 <= time[i], totalTrips <= 107

---

## 题目（中文翻译）

给定一个数组 `time`，其中 `time[i]` 表示第 `i` 辆公交车完成一次行程（trip）所需的时间。  
每辆公交车可以连续完成多次行程，也就是说，在当前行程结束后，它可以立即开始下一次行程。并且每辆公交车相互独立，某辆公交车的行程安排不会影响其他公交车。

同时给定一个整数 `totalTrips`，表示所有公交车需要完成的行程总数。返回所有公交车至少完成 `totalTrips` 次行程所需的最小时间。

**示例 1**  
``` 
Input: time = [1,2,3], totalTrips = 5
Output: 3
Explanation:
- 在 t = 1 时，各公交车已完成的行程数为 [1,0,0]，总行程数为 1 + 0 + 0 = 1。
- 在 t = 2 时，各公交车已完成的行程数为 [2,1,0]，总行程数为 2 + 1 + 0 = 3。
- 在 t = 3 时，各公交车已完成的行程数为 [3,1,1]，总行程数为 3 + 1 + 1 = 5，已达到或超过 totalTrips。
因此最小时间为 3。
```

**示例 2**  
``` 
Input: time = [2], totalTrips = 1
Output: 2
Explanation:
只有一辆公交车，它将在 t = 2 完成第一次行程。  
所以完成 1 次行程的最小时间是 2。
```

**约束条件**  
- `1 <= time.length <= 10^5`  
- `1 <= time[i], totalTrips <= 10^7`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**模拟时间的流逝**：从 `t = 1` 开始，一秒一秒往后走，统计每一时刻每辆公交车已经完成了多少趟旅行，累计所有公交车的总趟数，直到总趟数 `≥ totalTrips` 为止。  

- **用到的数据结构**：只需要一个普通的 Python 列表 `time`（相当于一排排排好的公交车），以及几个整数变量来保存“已经过去的时间”和“累计的旅行次数”。  
- **生活化类比**：把每辆公交车想象成**流水线上的工人**，每个工人完成一件产品需要 `time[i]` 秒。我们把时间轴划分成一格格的秒钟，站在旁边的监督员每秒记录一次每个工人完成的产品数量，直到所有工人合计生产的产品数达到目标。  

**为什么这个方法正确**  
因为我们逐秒检查“在这段时间里所有公交车一共能跑多少趟”，只要找到了第一次满足 `≥ totalTrips` 的时刻，那就是最小的可行时间。没有遗漏，也没有提前。

**时间/空间复杂度**  
- **时间复杂度**：设答案是 `T`，我们需要循环 `T` 次，每一次循环里遍历全部 `n = len(time)` 辆公交车，做一次除法 `t // time[i]` 来得到该公交车已经跑的趟数。所以整体是 `O(T * n)`。在最坏情况下 `T` 可能非常大（比如所有公交车都很慢，而 `totalTrips` 很大），这会导致超时。  
- **空间复杂度**：只用了常数级额外空间 `O(1)`（除了原始输入列表外），因为我们只保存几个计数器。

> **大白话解释**：`O(T * n)` 就像说“如果我们要跑 10 000 秒，每秒要检查 100 辆车”，工作量就是 1 000 000 次基本操作。`O(1)` 则是指“我们只需要几块纸记下数字”，不随输入规模增长。

#### 代码（Python）

```python
def minimumTime_bruteforce(time, totalTrips):
    # 从第 1 秒开始逐秒检查
    t = 1
    while True:
        trips = 0                     # 当下累计的总趟数
        for tm in time:               # 遍历每辆公交车
            trips += t // tm          # 该车在 t 秒内能跑的趟数
        if trips >= totalTrips:      # 已经满足要求，返回当前时间
            return t
        t += 1                        # 否则继续下一秒
```

#### 复杂度

- **时间复杂度**：`O(T * n)` —— `T` 为答案的时间大小，`n` 为公交车数量。实际意义是：答案越大、公交车越多，运行越慢。  
- **空间复杂度**：`O(1)` —— 只用了常数个额外变量。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**核心问题是**：在给定的时间 `mid`（比如 10 秒）时，所有公交车一共能完成多少趟？如果这个数 ≥ `totalTrips`，说明 `mid` 可能是一个可行解；如果 < `totalTrips`，说明时间太短，需要更大的 `mid`。

这正好符合 **二分查找** 的使用场景：  
- **单调性**：当时间 `t` 增大时，能完成的总趟数只会**不减**（永远不会出现已经满足要求的时间再变不满足）。  
- **目标**：找最小的满足条件的 `t`。

**步骤**  

1. **确定搜索区间**  
   - 最小可能时间显然是 `1`（最快的公交车在第 1 秒就可能完成一次）。  
   - 最大可能时间可以设为 `max(time) * totalTrips`：最慢的公交车单独完成所有旅行所需要的时间，上界足够大，二分不会越界。  

2. **二分过程**  
   - 取中点 `mid = (left + right) // 2`。  
   - 计算 `mid` 秒内所有公交车能完成的总趟数：`sum(mid // tm for tm in time)`。这里的 `//` 是整除，表示“在 `mid` 秒里这辆车完整跑了几趟”。  
   - 若总趟数 `≥ totalTrips`，说明 `mid` 可行，收紧右边界 `right = mid`（因为我们想要最小的可行时间）。  
   - 否则 `mid` 不够大，收紧左边界 `left = mid + 1`。  

3. **结束条件**  
   当左边界与右边界相遇时（`left == right`），即找到了最小的可行时间。

**关键数据结构解释**  

- **列表 `time`**：相当于一本**字典**，`key` 是公交车编号，`value` 是它跑一次需要的秒数。我们只用它来遍历、取值。  
- **二分变量 `left, right, mid`**：把可能的时间范围像**尺子**一样不断折半，快速定位答案。

**类比**：想象你在找一把**最轻的钥匙**，但你只能用“重量是否≥某个阈值”来判断。于是你先试一个中等重量的钥匙，如果太重，就把范围往轻的方向收缩；如果太轻，就往重的方向收缩。每次都把范围砍掉一半，最后恰好锁住最轻合格的钥匙。

#### 代码（Python）

```python
def minimumTime(time, totalTrips):
    """
    二分查找最小的时间，使得所有公交车在该时间内完成的总趟数 >= totalTrips
    """
    # 1. 初始化左右边界
    left = 1                                 # 最小可能时间
    right = max(time) * totalTrips           # 足够大的上界

    # 2. 二分循环
    while left < right:
        mid = (left + right) // 2            # 取中点

        # 计算 mid 秒内所有公交车可以完成的趟数
        trips = 0
        for tm in time:                      # 遍历每辆车
            trips += mid // tm               # 整除得到该车完成的趟数
        # 3. 根据单调性收缩区间
        if trips >= totalTrips:              # mid 已经足够
            right = mid                       # 往左找更小的可行解
        else:                                 # 还不够，需要更大的时间
            left = mid + 1

    # 4. 循环结束时 left == right，即为答案
    return left
```

> **代码要点注释**  
> - `mid // tm`：在 `mid` 秒里，这辆车完整跑了多少趟（比如 `mid=7, tm=3` → `7//3 = 2`，表示跑了两趟，剩下 1 秒不足以再完成一次）。  
> - `while left < right`：当区间只剩一个数时停止，避免无限循环。  

#### 复杂度

- **时间复杂度**：`O(n * log(max(time) * totalTrips))`  
  - `log` 部分来自二分查找，每次把时间范围折半，最多进行 `log2(右边界)` 次迭代。  
  - 每次迭代我们遍历所有 `n` 辆公交车，计算 `mid // tm`，所以乘以 `n`。  
  - **大白话**：如果有 100 辆公交车，右边界是 10⁸，二分大约只需要 27 次循环（因为 2²⁷ ≈ 1.34e8），总操作约为 2700 次，远比暴力的几亿次要快。

- **空间复杂度**：`O(1)`  
  - 只使用了几个整数变量 `left, right, mid, trips`，不随输入规模增长。

---

## 心得

- **核心技巧**：利用**单调性 + 二分搜索**把“在多少时间内完成足够任务”转化为一个判定问题，从而在对数时间内找到最小可行解。  
- **适用的题型**：  
  1. **分配资源的最小时间**（例如 “Koko 吃香蕉”）  
  2. **容量/预算的最小阈值**（例如 “在限定天数内完成所有工作”）  
  3. **最小最大化问题**（例如 “把木板分割成 k 段的最小最大长度”）  
- **一句话总结解题钥匙**：**把“求最小满足条件的值”转化为“判断某个值是否可行”，再用二分快速定位**。

---

## 反思

- **第一反应**：看到“每辆公交车可以连续跑多趟”，自然会想到**累加每辆车跑的次数**，于是想到直接模拟。  
- **最容易踩的坑**：  
  - **右边界设得不够大**：如果上界太小，二分可能在答案之前就提前结束。安全的上界是 `max(time) * totalTrips`（最慢的车单独完成所有任务的时间）。  
  - **整除的细节**：使用 `mid // tm` 而不是 `mid / tm`，否则会得到浮点数导致错误计数。  
  - **循环退出条件**：必须写 `while left < right` 并在内部用 `right = mid`（不减 1）和 `left = mid + 1`，否则可能陷入死循环。  
- **下次遇到同类题**：第一步先**确认是否存在单调性**（时间增大→完成任务数不减），然后**写出判定函数**（给定时间能完成多少），最后**二分搜索最小满足判定的时间**。这样思路一步到位，代码自然清晰。