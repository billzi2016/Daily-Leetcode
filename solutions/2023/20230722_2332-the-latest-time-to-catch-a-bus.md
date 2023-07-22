# #2332. 搭乘公交的最晚时间 / The Latest Time to Catch a Bus

> 难度：中等 · 标签：Array、Two Pointers、Binary Search、Sorting · [LeetCode 链接](https://leetcode.com/problems/the-latest-time-to-catch-a-bus/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array buses of length n, where buses[i] represents the departure time of the ith bus. You are also given a 0-indexed integer array passengers of length m, where passengers[j] represents the arrival time of the jth passenger. All bus departure times are unique. All passenger arrival times are unique.
You are given an integer capacity, which represents the maximum number of passengers that can get on each bus.
When a passenger arrives, they will wait in line for the next available bus. You can get on a bus that departs at x minutes if you arrive at y minutes where y <= x, and the bus is not full. Passengers with the earliest arrival times get on the bus first.
More formally when a bus arrives, either:
Return the latest time you may arrive at the bus station to catch a bus. You cannot arrive at the same time as another passenger.
Note: The arrays buses and passengers are not necessarily sorted.

**Examples**

**Example 1:**

```
Input: buses = [10,20], passengers = [2,17,18,19], capacity = 2
Output: 16
Explanation: Suppose you arrive at time 16.
At time 10, the first bus departs with the 0th passenger. 
At time 20, the second bus departs with you and the 1st passenger.
Note that you may not arrive at the same time as another passenger, which is why you must arrive before the 1st passenger to catch the bus.
```

**Example 2:**

```
Input: buses = [20,30,10], passengers = [19,13,26,4,25,11,21], capacity = 2
Output: 20
Explanation: Suppose you arrive at time 20.
At time 10, the first bus departs with the 3rd passenger. 
At time 20, the second bus departs with the 5th and 1st passengers.
At time 30, the third bus departs with the 0th passenger and you.
Notice if you had arrived any later, then the 6th passenger would have taken your seat on the third bus.
```

**Constraints**

- n == buses.length
- m == passengers.length
- 1 <= n, m, capacity <= 105
- 2 <= buses[i], passengers[i] <= 109
- Each element in buses is unique.
- Each element in passengers is unique.

---

## 题目（中文翻译）

给定一个长度为 `n` 的 0 起始索引整数数组 `buses`，其中 `buses[i]` 表示第 `i` 辆公交的出发时间。再给定一个长度为 `m` 的 0 起始索引整数数组 `passengers`，其中 `passengers[j]` 表示第 `j` 位乘客的到达时间。所有公交的出发时间互不相同，所有乘客的到达时间也互不相同。

另有一个整数 `capacity`，表示每辆公交最多可以容纳的乘客数量。

当乘客到达时，会排队等待下一辆可乘坐的公交。若公交在 `x` 分钟出发，而你在 `y` 分钟到达且 `y ≤ x`，且该公交未满员，你即可上车。到达时间更早的乘客会优先上车。

更形式化地，当一辆公交到达时，会出现以下两种情况之一（省略具体细节）：

返回你可以到达公交站的**最晚时间**，以确保能够搭乘到一辆公交。**你不能与其他乘客在同一时刻到达**。

> 注意：数组 `buses` 和 `passengers` 未必是已排序的。

---

## 示例

### 示例 1

**输入**  
`buses = [10,20]`  
`passengers = [2,17,18,19]`  
`capacity = 2`

**输出**  
`16`

**解释**  
假设你在时间 `16` 到达。  
- 时间 `10` 时，第一辆公交出发，搭载第 `0` 位乘客。  
- 时间 `20` 时，第二辆公交出发，搭载你和第 `1` 位乘客。  

因为不能与其他乘客在同一时刻到达，你必须在第 `1` 位乘客之前到达才能上车。

---

### 示例 2

**输入**  
`buses = [20,30,10]`  
`passengers = [19,13,26,4,25,11,21]`  
`capacity = 2`

**输出**  
`20`

**解释**  
假设你在时间 `20` 到达。  
- 时间 `10` 时，第一辆公交出发，搭载第 `3` 位乘客。  
- 时间 `20` 时，第二辆公交出发，搭载第 `5` 位和第 `1` 位乘客。  
- 时间 `30` 时，第三辆公交出发，搭载第 `0` 位乘客和你。  

如果你稍晚一点到达，第 `6` 位乘客就会先上车，从而导致你无法搭乘。

---

## 约束条件

- `n == buses.length`
- `m == passengers.length`
- `1 ≤ n, m, capacity ≤ 10^5`
- `2 ≤ buses[i], passengers[i] ≤ 10^9`
- `buses` 中的每个元素互不相同
- `passengers` 中的每个元素互不相同

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**枚举**你可能到达的每一分钟 `t`（从 1 到最大的公交车发车时间），把 `t` 当成“你”这个乘客的到达时间，和题目给出的其他乘客一起模拟上车过程，看你能否上车。  

- **数据结构**：我们只需要两个**有序列表**（数组）  
  - `buses`：公交车的发车时间，想象成排好队的公交车，时间早的先到站。  
  - `passengers`：所有已知乘客的到达时间，想象成排队等车的乘客，时间早的先排在前面。  

  把这两个列表都 **排序**（就像把乱糟糟的字典排好顺序，查找时更方便）。  

- **模拟过程**：从最早的公交车开始，依次让排在前面的乘客（包括我们假设的 `t`）上车，直到公交车坐满或没有更多乘客能在该车发车前到达。  

- **为什么正确**：如果在所有可能的 `t` 中，有至少一个 `t` 能让我们上车，那么枚举一定会找到它；如果没有 `t` 能上车，枚举也会全部失败。  

- **时间/空间复杂度**：  
  - 枚举的次数是 **最大发车时间**，在最坏情况下可能是 `10^9`，每次模拟又要遍历所有公交车和乘客（`O(n+m)`）。所以时间复杂度是 **`O(maxTime * (n+m))`**，这在实际数据下根本不可接受。  
  - 只需要保存排序后的两个数组，空间是 **`O(n+m)`**。  

> **大白话**：`O(maxTime * (n+m))` 就好比让你把一条很长的路（比如 10⁹ 米）走一遍，每走一步都要重新检查所有的公交车和乘客，显然会超时。  

#### 代码（Python）  

```python
def latestTimeCatchTheBus_bruteforce(buses, passengers, capacity):
    # 1. 排序，方便模拟
    buses = sorted(buses)
    passengers = sorted(passengers)

    # 2. 可能的最大时间是最后一辆公交车的发车时间
    max_time = buses[-1]

    # 3. 枚举每一个可能的到达时间 t
    for t in range(1, max_time + 1):
        # t 不能和已有乘客的到达时间相同
        if t in passengers:
            continue

        # 把 t 当成“你”这位乘客加入队列，保持有序
        all_pass = sorted(passengers + [t])

        p_idx = 0               # 乘客指针
        success = False        # 是否成功上车

        for bus in buses:
            cnt = 0            # 当前公交车已上乘客数
            # 让所有到达时间 ≤ bus 且未上满的乘客上车
            while p_idx < len(all_pass) and all_pass[p_idx] <= bus and cnt < capacity:
                # 如果这位是我们自己（t），标记成功
                if all_pass[p_idx] == t:
                    success = True
                p_idx += 1
                cnt += 1
            # 若已成功上车，可以直接返回当前 t（因为我们是从小到大枚举的，后面的 t 更晚）
            if success:
                return t
        # 本次 t 没能上车，继续尝试更大的 t
    return -1   # 按题意不会出现这种情况
```

> **注意**：这段代码只用于说明暴力思路，实际运行会因为 `t in passengers` 的线性查找和大量的排序而超时。

#### 复杂度  

- **时间复杂度**：`O(maxTime * (n + m))`  
  - `maxTime` 可能高达 `10^9`，即使 `n,m` 只有 `10^5`，也会非常慢。  
- **空间复杂度**：`O(n + m)`  
  - 只需要存储排好序的两个数组以及一次临时的合并数组。  

---

### 2. 最优解  

#### 思路  

暴力解慢的根本原因是 **枚举所有可能的时间**，而实际上我们只需要关心两类时间点：

1. **公交车的发车时间**（因为如果你在发车时间以后到达，肯定坐不上该车）。  
2. **已有乘客的到达时间的前一秒**（因为题目禁止与你的到达时间相同，所以你只能在他们之前一秒到达）。  

因此，答案一定是 **某个乘客时间 - 1**，或者 **某辆公交车的发车时间**（如果该车还有空位且该时间没有被占用）。  

**核心思路**：  
- 先把 `buses`、`passengers` 排序。  
- 用两个指针模拟“乘客排队上车”。  
  - `i` 指向当前公交车（按时间从早到晚）。  
  - `j` 指向当前乘客（同样从早到晚）。  
- 对每辆公交车，最多让 `capacity` 位**已到达且未上车**的乘客上车。  
- 记录每辆车上了哪些乘客的到达时间。  

**得到答案的关键**在最后一辆公交车：  

- **若该车还有空位**  
  - 你可以直接在该车的发车时间 `bus_time` 到达（只要没有人已经在同一时刻）。  
- **若该车已满**  
  - 最后一个上车的乘客的到达时间记作 `last_passenger`。  
  - 你只能在 `last_passenger - 1` 时到达（确保比所有已上车的乘客更早且不与其他乘客同时间）。  

因为我们已经在模拟过程中把所有乘客的时间都排好序，只要检查 `last_passenger - 1` 是否已经被其他乘客占用（不会，因为乘客时间都是唯一的），答案即为该值。  

**为什么是最优的**：  
- 只遍历一次 `buses`（`n` 次）和一次 `passengers`（`m` 次），时间复杂度 `O(n log n + m log m)` 只来源于排序，模拟本身是线性的 `O(n + m)`。  
- 空间只用了排序后的数组和若干指针，`O(1)` 额外空间。  

#### 代码（Python）  

```python
def latestTimeCatchTheBus(buses, passengers, capacity):
    """
    返回你最迟可以到达的时间，使得能够成功上车。
    思路：先排序，然后用双指针模拟上车过程，只关心最后一辆车的情况。
    """
    # 1. 排序（O(n log n + m log m)）
    buses.sort()
    passengers.sort()

    p_idx = 0               # 乘客指针，指向下一个还未上车的乘客
    last_boarded = -1       # 记录最后一位成功上车乘客的到达时间

    # 2. 按时间顺序遍历每一辆公交车
    for bus_time in buses:
        cnt = 0             # 当前公交车已上乘客数

        # 把所有在 bus_time 之前（包括等于）且未上满的乘客让上车
        while p_idx < len(passengers) and passengers[p_idx] <= bus_time and cnt < capacity:
            last_boarded = passengers[p_idx]   # 更新最后上车的乘客时间
            p_idx += 1
            cnt += 1

        # 若这辆车已经坐满，直接进入下一辆；否则继续装载
        #（这里不需要额外处理，while 循环已经完成装载）

    # 3. 处理最后一辆公交车的结果
    #    - 如果最后一辆车还有空位（即 cnt < capacity），我们可以在该车的发车时间上车
    #    - 否则只能在 last_boarded 前的那一秒上车
    # 注意：因为所有乘客时间都是唯一的，last_boarded - 1 不会与已有乘客冲突
    # 但是仍需保证它不大于对应的公交车发车时间
    # 为了统一处理，我们再次遍历一次找出最后一辆车的装载情况

    # 重新模拟，只记录最后一辆车的装载信息
    p_idx = 0
    for i, bus_time in enumerate(buses):
        cnt = 0
        while p_idx < len(passengers) and passengers[p_idx] <= bus_time and cnt < capacity:
            last_boarded = passengers[p_idx]
            p_idx += 1
            cnt += 1
        # 当遍历到最后一辆车时，退出循环后 cnt、bus_time、last_boarded 都是我们需要的
        if i == len(buses) - 1:
            last_cnt = cnt
            last_bus = bus_time
            break

    if last_cnt < capacity:                     # 还有空位
        # 直接在公交车发车时间上车，但要确保这个时间没有被乘客占用
        # 乘客时间唯一且都 ≤ bus_time，若 bus_time 本身已经是乘客的到达时间，
        # 那么我们只能提前一秒。这里用集合判断更直观（O(1) 查找）。
        passenger_set = set(passengers)
        if last_bus not in passenger_set:
            return last_bus
        else:
            # bus_time 已被乘客占用，只能在 bus_time-1
            return last_bus - 1
    else:                                        # 已坐满
        # 必须在最后一个上车乘客的前一秒到达
        return last_boarded - 1
```

> **代码解释（关键行）**  
- `buses.sort()`、`passengers.sort()`：把乱序的时间排好顺序，后面只需要线性扫描。  
- `while ...` 循环：模拟“在当前公交车发车前，最早到达的乘客依次上车”。  
- `last_boarded`：始终保存**最新一次成功上车的乘客时间**，用于最后的答案计算。  
- 最后一次遍历是为了**确定最后一辆公交车的实际装载情况**（是否坐满），因为前面的循环已经把指针跑到末尾，直接用保存的变量会混淆。  

#### 复杂度  

- **时间复杂度**：`O(n log n + m log m)`  
  - 主要花在对 `buses`、`passengers` 的排序（`log` 代表“对数”，相当于把 100 000 条数据从无序变成有序，只需要几次比较）。  
  - 排序后只进行一次线性遍历（`O(n + m)`），相比暴力的 `O(maxTime·(n+m))` 快了几百倍。  
- **空间复杂度**：`O(1)`（不计输入数组本身）  
  - 只用了若干指针和局部变量，未额外申请与 `n、m` 成正比的存储空间。  

---

## 心得  

- **核心技巧**：先排序再用双指针模拟“先到先上”。  
- **适用的题型**：  
  1. “排队上车/排队登船”类（例如 LeetCode 1654. *Maximum Number of Eaten Apples* 中的贪心模拟）。  
  2. “在限定资源下的最晚/最早时间”类（例如 1095. *Find Smallest Integer Divisible by K* 中的二分+模拟）。  
- **一句话总结解题钥匙**：**把所有时间排好序，然后只在“关键时间点”（乘客到达或公交发车）上做一次线性模拟**。  

---

## 反思  

- **第一反应**：看到“最大时间”“不能和乘客同时间”，立刻想到要**枚举所有可能的时间**。这会导致超时。  
- **最容易踩的坑**：  
  - 忘记 **去重**：答案不能和任何乘客的到达时间相同，需要在返回前检查。  
  - 边界情况：最后一辆公交车还有空位且该时间正好被乘客占用，需要回退一秒。  
  - 大数范围：时间值可达 `10^9`，不能用数组下标直接映射，需要用集合或二分搜索。  
- **下次遇到同类题**：第一步先 **排序 + 找出关键时间点**（乘客或资源的时间），再用 **双指针/贪心** 线性模拟，而不是盲目枚举。