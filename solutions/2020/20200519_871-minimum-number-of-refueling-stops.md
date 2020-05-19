# #871. 最少加油次数 / Minimum Number of Refueling Stops

> 难度：困难 · 标签：Array、Dynamic Programming、Greedy、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-refueling-stops/)

---

## 题目（英文原版）

**Description**

A car travels from a starting position to a destination which is target miles east of the starting position.
There are gas stations along the way. The gas stations are represented as an array stations where stations[i] = [positioni, fueli] indicates that the ith gas station is positioni miles east of the starting position and has fueli liters of gas.
The car starts with an infinite tank of gas, which initially has startFuel liters of fuel in it. It uses one liter of gas per one mile that it drives. When the car reaches a gas station, it may stop and refuel, transferring all the gas from the station into the car.
Return the minimum number of refueling stops the car must make in order to reach its destination. If it cannot reach the destination, return -1.
Note that if the car reaches a gas station with 0 fuel left, the car can still refuel there. If the car reaches the destination with 0 fuel left, it is still considered to have arrived.

**Examples**

**Example 1:**

```
Input: target = 1, startFuel = 1, stations = []
Output: 0
Explanation: We can reach the target without refueling.
```

**Example 2:**

```
Input: target = 100, startFuel = 1, stations = [[10,100]]
Output: -1
Explanation: We can not reach the target (or even the first gas station).
```

**Example 3:**

```
Input: target = 100, startFuel = 10, stations = [[10,60],[20,30],[30,30],[60,40]]
Output: 2
Explanation: We start with 10 liters of fuel.
We drive to position 10, expending 10 liters of fuel.  We refuel from 0 liters to 60 liters of gas.
Then, we drive from position 10 to position 60 (expending 50 liters of fuel),
and refuel from 10 liters to 50 liters of gas.  We then drive to and reach the target.
We made 2 refueling stops along the way, so we return 2.
```

**Constraints**

- 1 <= target, startFuel <= 109
- 0 <= stations.length <= 500
- 1 <= positioni < positioni+1 < target
- 1 <= fueli < 109

---

## 题目（中文翻译）

一辆汽车从起点出发，向东行驶至目标地点，目标地点距离起点 `target` 英里。途中有若干加油站（gas stations），用数组 `stations` 表示，其中 `stations[i] = [position_i, fuel_i]` 表示第 `i` 个加油站位于距起点 `position_i` 英里处，并且拥有 `fuel_i` 升汽油。  
汽车的油箱容量视为无限，初始时油箱内有 `startFuel` 升汽油。汽车每行驶一英里会消耗一升汽油。当汽车到达某个加油站时，可以选择停下来加油，将该站的所有汽油全部转入汽车油箱。  
返回汽车为到达目的地所需的最少加油次数（refueling stops）。如果无法到达目的地，返回 `-1`。  
注意：即使汽车在到达加油站时油量为 `0`，仍然可以在该站加油；若汽车在到达目的地时油量为 `0`，仍视为已成功到达。

**示例 1**  
**输入**: `target = 1, startFuel = 1, stations = []`  
**输出**: `0`  
**解释**: 我们可以在不加油的情况下直接到达目标。

**示例 2**  
**输入**: `target = 100, startFuel = 1, stations = [[10,100]]`  
**输出**: `-1`  
**解释**: 我们连第一个加油站都到达不了，因而也到达不了目标。

**示例 3**  
**输入**: `target = 100, startFuel = 10, stations = [[10,60],[20,30],[30,30],[60,40]]`  
**输出**: `2`  
**解释**:  
- 我们先有 10 升汽油，驱车行驶至位置 10，消耗 10 升，此时油箱为空。  
- 在位置 10 的加油站加满 60 升汽油。  
- 接着从位置 10 行驶到位置 60，消耗 50 升，油箱剩余 10 升。  
- 在位置 60 的加油站再加满 40 升，使油箱达到 50 升。  
- 最后直接驶向目标。  
途中共加油 2 次，返回 2。

**约束条件**  
- `1 <= target, startFuel <= 10^9`  
- `0 <= stations.length <= 500`  
- `1 <= position_i < position_{i+1} < target`  
- `1 <= fuel_i < 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的加油组合**，看看哪一种能够让汽车顺利到达终点并且加油次数最少。

- **数据结构**  
  - 用 `list` 保存所有加油站的信息 `stations[i] = [位置, 油量]`。可以把它想象成一条路上依次排好的加油站，位置越大就越靠前。  
  - 用 `int` 记录当前汽车的剩余油量。  
  - 为了枚举每一种“是否在某个加油站加油”的情况，我们可以用 **二进制位** 表示：第 `i` 位为 `1` 表示在第 `i` 个加油站停下来加满油，为 `0` 表示直接开过去不加油。这样一次遍历所有 `2^n` 种可能（`n` 为加油站数量）。

- **为什么正确**  
  暴力遍历把**所有**合法的加油方案都检查了一遍，只要有一种方案能让汽车到达 `target`，我们就能找到其中加油次数最少的那一个。因此答案一定不会错。

- **复杂度分析（大白话）**  
  - 时间复杂度：`O(2^n * n)`  
    - `2^n` 表示所有可能的加油组合（比如有 10 个加油站，就有 1024 种组合）。  
    - 对每一种组合我们需要模拟一次行驶过程，最多遍历 `n` 次加油站。  
    - 对初学者来说，`2^n` 就像把所有可能的钥匙都尝一遍，随着 `n` 增大，钥匙数会“爆炸”，很快就不可能在合理时间内完成。
  - 空间复杂度：`O(1)`（只用了几个整数来记录油量、位置等），不随 `n` 增长。

#### 代码（Python）

```python
from itertools import product
from typing import List

def minRefuelStops_bruteforce(target: int, startFuel: int,
                              stations: List[List[int]]) -> int:
    n = len(stations)
    # 所有加油站的“是否加油”二进制组合，0 表示不加，1 表示加
    # product([0, 1], repeat=n) 会产生 2^n 种元组
    best = float('inf')                     # 用来保存最小的加油次数
    for decisions in product([0, 1], repeat=n):
        fuel = startFuel                     # 当前油量
        prev = 0                             # 上一次停靠的地点（起点是 0）
        stops = 0                            # 本次方案的加油次数
        feasible = True

        for i, decide in enumerate(decisions):
            pos, add = stations[i]
            # 先开到当前加油站，需要消耗的油量是距离差
            need = pos - prev
            if fuel < need:                  # 油不够跑到这里
                feasible = False
                break
            fuel -= need                      # 开到这里后剩余油量
            if decide:                        # 决定在这里加油
                fuel += add
                stops += 1
            prev = pos                        # 更新当前位置

        # 最后检查能否从最后一个加油站（或起点）开到终点
        if feasible and fuel >= target - prev:
            best = min(best, stops)

    return -1 if best == float('inf') else best
```

#### 复杂度

- **时间复杂度**：`O(2^n * n)`  
  - `2^n` 表示所有可能的加油决策组合；每个组合要遍历最多 `n` 次加油站。  
  - 对初学者来说，这相当于“把每一种可能都尝一遍”，随着加油站数量稍微增多（比如 20），就会变得不可行。

- **空间复杂度**：`O(1)`  
  - 只用了常数个变量来记录油量、位置、加油次数等，和加油站数量无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**枚举所有加油方案**，而实际上我们只关心“在已经走过的路上，哪几个加油站的油最值得拿”。这可以用**贪心 + 最大堆**来实现，思路如下：

1. **把车子当作一直往前跑**，只要油还能支撑，就一直前进。  
2. 当车子**快要耗尽油**，而前面已经经过的加油站中还有剩余的油可以补充时，我们应该**先取油量最大的那个站**，因为它能让我们跑得更远，减少后续加油次数。  
3. 为了快速取出“已经过的、油量最大的加油站”，我们使用**最大堆（Priority Queue）**。在 Python 中 `heapq` 默认是最小堆，取负数即可模拟最大堆。  
4. 具体过程：  
   - 按位置顺序遍历所有加油站（包括终点 `target` 视作一个“没有油的站”），记 `prev` 为上一次到达的地点。  
   - `need = station_pos - prev` 为到达当前站点所需的油量。  
   - 如果当前油量 `fuel` **不足** `need`，就从最大堆里弹出油量最大的已经过站点，加到 `fuel` 中，同时计数 `stops += 1`。如果堆已经空了，说明再也没有可以加的油了，直接返回 `-1`。  
   - 当 `fuel` 足够时，开到当前站点，`fuel -= need`，把 **当前站点的油量**（如果不是终点）压入堆中，以备后面需要时使用。  
5. 当遍历完所有站点（包括终点）后，计数 `stops` 就是最少加油次数。

**为什么是最优的？**  
- 每一次“油不够继续前进”时，我们都选择**已经经过的、油量最大的站点**来加油。若改成加油量更小的站点，显然会让后面需要再次加油的次数不减反增。  
- 这种“取最大”的策略正是**贪心**的核心：局部最优（此时取最大）必能导向全局最优（最少加油次数）。  
- 证明可以通过**反证**：假设最优解在某一步没有取最大油量的站点，而是取了较小的，那我们把这一步换成取最大油量的站点，后面的路线不会变得更糟，反而可能更好，冲突于是不存在。

#### 代码（Python）

```python
import heapq
from typing import List

def minRefuelStops(target: int, startFuel: int,
                  stations: List[List[int]]) -> int:
    """
    贪心 + 最大堆
    :param target: 目的地距离起点的里程
    :param startFuel: 初始油量（每升油恰好能跑 1 英里）
    :param stations: [[位置, 油量], ...] 按位置升序给出
    :return: 最少加油次数，若无法到达返回 -1
    """
    # 把所有加油站位置 + 终点一起当成“站点”，终点的油量视作 0
    stations.append([target, 0])

    max_heap = []          # 用负数实现最大堆，存放已经路过的加油站的油量
    stops = 0              # 加油次数计数器
    prev = 0               # 上一次到达的地点（起点是 0）
    fuel = startFuel       # 当前剩余油量

    for pos, amount in stations:
        need = pos - prev           # 到达当前站点需要的油量

        # 如果油不够，就从已经路过的站点中取油（取最大的一次）
        while fuel < need:
            if not max_heap:        # 堆空了，说明再也没有油可以加
                return -1
            # 取出最大的油量（堆里存的是负数，需要取负号恢复正数）
            fuel += -heapq.heappop(max_heap)
            stops += 1              # 加油一次

        # 开到当前站点后剩余油量
        fuel -= need
        # 把当前站点的油量加入堆中，供以后需要时使用
        heapq.heappush(max_heap, -amount)
        prev = pos                  # 更新上一次到达的位置

    return stops
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - `n` 为加油站数量（`len(stations)`）。我们遍历一次所有站点。  
  - 每一次把油量加入堆或从堆中弹出，都需要 `log n` 的时间（堆的插入/删除是对数级的）。  
  - 与暴力解的 `2^n` 相比，`n log n` 随着 `n` 增长非常平缓，能够轻松处理题目给出的上限（`n ≤ 500`）。

- **空间复杂度**：`O(n)`  
  - 堆中最多会存放所有已经路过的站点的油量，最坏情况下是 `n` 个元素。  
  - 这比暴力解的 `O(1)` 多一点，但仍然在可接受范围内，而且换来了巨大的时间提升。

---

## 心得

- **核心技巧**：**贪心 + 最大堆**（在需要时取已路过站点中油量最大的那一个）。  
- **适用的题型**（类似思路）  
  1. “最大化利润”类问题：比如在股票买卖中，想要在每一次资金不足时尽可能取最大收益的交易。  
  2. “最少次数”类调度问题：如“跳跃游戏 II”（每次跳到最远的可以到达的位置）。  
  3. “资源分配”类问题：如“分配最少的机器完成所有任务”时，优先使用资源最大的机器。  
- **一句话总结解题钥匙**：**“当油不够前进时，先把已路过、油最多的站加进来”**。

---

## 反思

- **第一反应**：看到“最少加油次数”，立刻想到**动态规划**（dp[i] 表示到第 i 个站最少加油次数），于是写出 `O(n^2)` 的 DP 解。随后回忆到本题有更快的**贪心 + 堆**方案。  
- **最容易踩的坑**  
  - 忘记把终点 `target` 当作一个“站点”来处理，否则最后可能会少一次 `while fuel < need` 的检查。  
  - 处理 **起点油量已经足够直接到达终点** 的特殊情况：此时循环体根本不会执行，直接返回 `0`。  
  - 堆是最大堆，需要存负数或自行实现比较函数，容易写成最小堆导致逻辑相反。  
- **下次遇到同类题**：第一步先问自己 **“是否有‘资源不足’的时刻，需要从已收集的资源中挑选最大值？”**，若答案是，是就立刻考虑 **堆（优先队列）** + **贪心** 的组合。