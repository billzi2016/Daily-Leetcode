# #1396. 设计地下系统 / Design Underground System

> 难度：中等 · 标签：Hash Table、String、Design · [LeetCode 链接](https://leetcode.com/problems/design-underground-system/)

---

## 题目（英文原版）

**Description**

An underground railway system is keeping track of customer travel times between different stations. They are using this data to calculate the average time it takes to travel from one station to another.
Implement the UndergroundSystem class:
You may assume all calls to the checkIn and checkOut methods are consistent. If a customer checks in at time t1 then checks out at time t2, then t1 < t2. All events happen in chronological order.

**Examples**

**Example 1:**

```
Input
["UndergroundSystem","checkIn","checkIn","checkIn","checkOut","checkOut","checkOut","getAverageTime","getAverageTime","checkIn","getAverageTime","checkOut","getAverageTime"]
[[],[45,"Leyton",3],[32,"Paradise",8],[27,"Leyton",10],[45,"Waterloo",15],[27,"Waterloo",20],[32,"Cambridge",22],["Paradise","Cambridge"],["Leyton","Waterloo"],[10,"Leyton",24],["Leyton","Waterloo"],[10,"Waterloo",38],["Leyton","Waterloo"]]

Output
[null,null,null,null,null,null,null,14.00000,11.00000,null,11.00000,null,12.00000]

Explanation
UndergroundSystem undergroundSystem = new UndergroundSystem();
undergroundSystem.checkIn(45, "Leyton", 3);
undergroundSystem.checkIn(32, "Paradise", 8);
undergroundSystem.checkIn(27, "Leyton", 10);
undergroundSystem.checkOut(45, "Waterloo", 15);  // Customer 45 "Leyton" -> "Waterloo" in 15-3 = 12
undergroundSystem.checkOut(27, "Waterloo", 20);  // Customer 27 "Leyton" -> "Waterloo" in 20-10 = 10
undergroundSystem.checkOut(32, "Cambridge", 22); // Customer 32 "Paradise" -> "Cambridge" in 22-8 = 14
undergroundSystem.getAverageTime("Paradise", "Cambridge"); // return 14.00000. One trip "Paradise" -> "Cambridge", (14) / 1 = 14
undergroundSystem.getAverageTime("Leyton", "Waterloo");    // return 11.00000. Two trips "Leyton" -> "Waterloo", (10 + 12) / 2 = 11
undergroundSystem.checkIn(10, "Leyton", 24);
undergroundSystem.getAverageTime("Leyton", "Waterloo");    // return 11.00000
undergroundSystem.checkOut(10, "Waterloo", 38);  // Customer 10 "Leyton" -> "Waterloo" in 38-24 = 14
undergroundSystem.getAverageTime("Leyton", "Waterloo");    // return 12.00000. Three trips "Leyton" -> "Waterloo", (10 + 12 + 14) / 3 = 12
```

**Example 2:**

```
Input
["UndergroundSystem","checkIn","checkOut","getAverageTime","checkIn","checkOut","getAverageTime","checkIn","checkOut","getAverageTime"]
[[],[10,"Leyton",3],[10,"Paradise",8],["Leyton","Paradise"],[5,"Leyton",10],[5,"Paradise",16],["Leyton","Paradise"],[2,"Leyton",21],[2,"Paradise",30],["Leyton","Paradise"]]

Output
[null,null,null,5.00000,null,null,5.50000,null,null,6.66667]

Explanation
UndergroundSystem undergroundSystem = new UndergroundSystem();
undergroundSystem.checkIn(10, "Leyton", 3);
undergroundSystem.checkOut(10, "Paradise", 8); // Customer 10 "Leyton" -> "Paradise" in 8-3 = 5
undergroundSystem.getAverageTime("Leyton", "Paradise"); // return 5.00000, (5) / 1 = 5
undergroundSystem.checkIn(5, "Leyton", 10);
undergroundSystem.checkOut(5, "Paradise", 16); // Customer 5 "Leyton" -> "Paradise" in 16-10 = 6
undergroundSystem.getAverageTime("Leyton", "Paradise"); // return 5.50000, (5 + 6) / 2 = 5.5
undergroundSystem.checkIn(2, "Leyton", 21);
undergroundSystem.checkOut(2, "Paradise", 30); // Customer 2 "Leyton" -> "Paradise" in 30-21 = 9
undergroundSystem.getAverageTime("Leyton", "Paradise"); // return 6.66667, (5 + 6 + 9) / 3 = 6.66667
```

**Constraints**

- 1 <= id, t <= 106
- 1 <= stationName.length, startStation.length, endStation.length <= 10
- All strings consist of uppercase and lowercase English letters and digits.
- There will be at most 2 * 104 calls in total to checkIn, checkOut, and getAverageTime.
- Answers within 10-5 of the actual value will be accepted.

---

## 题目（中文翻译）

一个地下铁路系统（Underground railway system）正在记录乘客在不同站点之间的旅行时间，并利用这些数据计算从某站点到另一站点的平均旅行时间。

实现 `UndergroundSystem` 类：

- `void checkIn(int id, string stationName, int t)`
  - 编号为 `id` 的乘客在时间 `t` 进入站点 `stationName`。
  - 同时只能有一个未完成的 check‑in。
- `void checkOut(int id, string stationName, int t)`
  - 编号为 `id` 的乘客在时间 `t` 从站点 `stationName` 出站。
- `double getAverageTime(string startStation, string endStation)`
  - 返回从 `startStation` 到 `endStation` 的平均旅行时间。
  - 平均时间 = 所有该路线的总旅行时间 / 该路线的出行次数。
  - 结果误差在 `10^-5` 之内即视为正确。

**说明**  
- 可以假设所有对 `checkIn` 和 `checkOut` 的调用都是一致的。如果乘客在时间 `t1` check‑in，则其对应的 `checkOut` 必在时间 `t2`，且 `t1 < t2`。所有事件按时间顺序发生。

### 示例 1

**输入**
```json
["UndergroundSystem","checkIn","checkIn","checkIn","checkOut","checkOut","checkOut","getAverageTime","getAverageTime","checkIn","getAverageTime","checkOut","getAverageTime"]
[[],[45,"Leyton",3],[32,"Paradise",8],[27,"Leyton",10],[45,"Waterloo",15],[27,"Waterloo",20],[32,"Cambridge",22],["Paradise","Cambridge"],["Leyton","Waterloo"],[10,"Leyton",24],["Leyton","Waterloo"],[10,"Waterloo",38],["Leyton","Waterloo"]]
```

**输出**
```json
[null,null,null,null,null,null,null,14.0,11.0,null,11.0,null,12.0]
```

**解释**
```
UndergroundSystem undergroundSystem = new UndergroundSystem();
undergroundSystem.checkIn(45, "Leyton", 3);
undergroundSystem.checkIn(32, "Paradise", 8);
undergroundSystem.checkIn(27, "Leyton", 10);
undergroundSystem.checkOut(45, "Waterloo", 15); // 乘客 45 的行程 "Leyton" -> "Waterloo"，耗时 15-3 = 12
undergroundSystem.checkOut(27, "Waterloo", 20); // 乘客 27 的行程 "Leyton" -> "Waterloo"，耗时 20-10 = 10
undergroundSystem.checkOut(32, "Cambridge", 22); // 乘客 32 的行程 "Paradise" -> "Cambridge"，耗时 22-8 = 14
undergroundSystem.getAverageTime("Paradise", "Cambridge"); // 返回 14.00000。仅有 1 次 "Paradise" -> "Cambridge" 行程，14 / 1 = 14
undergroundSystem.getAverageTime("Leyton", "Waterloo"); // 返回 11.00000。两次 "Leyton" -> "Waterloo" 行程，(12 + 10) / 2 = 11
undergroundSystem.checkIn(10, "Leyton", 24);
undergroundSystem.getAverageTime("Leyton", "Waterloo"); // 仍返回 11.00000（尚未产生新的出站记录）
undergroundSystem.checkOut(10, "Waterloo", 38); // 乘客 10 的行程 "Leyton" -> "Waterloo"，耗时 38-24 = 14
undergroundSystem.getAverageTime("Leyton", "Waterloo"); // 返回 12.00000。三次行程 (12 + 10 + 14) / 3 = 12
```

### 示例 2

**输入**
```json
["UndergroundSystem","checkIn","checkOut","getAverageTime","checkIn","checkOut","getAverageTime","checkIn","checkOut","getAverageTime"]
[[],[10,"Leyton",3],[10,"Paradise",8],["Leyton","Paradise"],[5,"Leyton",10],[5,"Paradise",16],["Leyton","Paradise"],[2,"Leyton",21],[2,"Paradise",30],["Leyton","Paradise"]]
```

**输出**
```json
[null,null,null,5.00000,null,null,5.50000,null,null,6.66667]
```

**解释**
```
UndergroundSystem undergroundSystem = new UndergroundSystem();
undergroundSystem.checkIn(10, "Leyton", 3);
undergroundSystem.checkOut(10, "Paradise", 8); // 行程耗时 5
undergroundSystem.getAverageTime("Leyton", "Paradise"); // 返回 5.00000

undergroundSystem.checkIn(5, "Leyton", 10);
undergroundSystem.checkOut(5, "Paradise", 16); // 行程耗时 6
undergroundSystem.getAverageTime("Leyton", "Paradise"); // 返回 (5 + 6) / 2 = 5.5

undergroundSystem.checkIn(2, "Leyton", 21);
undergroundSystem.checkOut(2, "Paradise", 30); // 行程耗时 9
undergroundSystem.getAverageTime("Leyton", "Paradise"); // 返回 (5 + 6 + 9) / 3 = 6.66667
```

### 约束条件

- `1 <= id, t <= 10^6`
- `1 <= stationName.length, startStation.length, endStation.length <= 10`
- 所有字符串仅由大小写英文字母和数字组成。
- `checkIn`、`checkOut`、`getAverageTime` 的调用总次数不超过 `2 * 10^4`。
- 结果误差在 `10^-5` 以内即被接受。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每一次 **check‑in → check‑out** 的完整记录全部保存下来，然后在 `getAverageTime(start,end)` 时遍历所有记录，挑出起点是 `start` 且终点是 `end` 的那几条，累加它们的旅行时间，再除以出现的次数得到平均值。

- **数据结构**  
  - 用一个列表 `trips` 保存所有已经完成的行程。每条记录可以是 `(id, startStation, endStation, travelTime)` 的元组。  
  - 列表就像一本“行程簿”，我们要在里面翻页找符合条件的记录。  

- **正确性**  
  - 因为每一次乘客的出行都会被完整记录下来，遍历全部记录就一定能找到所有符合 `(startStation, endStation)` 的行程，求和再除以次数自然得到准确的平均时间。

- **复杂度分析（大白话）**  
  - `checkIn`、`checkOut` 只是在字典里记下或取出一个时间，时间几乎可以忽略不计。  
  - `getAverageTime` 需要把所有行程翻一遍，就像在一本 10 000 页的书里找特定章节，需要 **O(N)** 的时间（N 是已经完成的出行次数）。如果出行次数很多，这一步会变得很慢。  
  - 额外空间：我们把每一条出行都保存下来，需要 **O(N)** 的空间。

#### 代码（Python）

```python
class UndergroundSystem:
    def __init__(self):
        # 正在乘车的乘客：id -> (stationName, checkInTime)
        self.check_in = {}
        # 已完成的所有行程，列表相当于“行程簿”
        self.trips = []          # [(id, start, end, travelTime), ...]

    # 乘客 id 在 stationName 检票，时间为 t
    def checkIn(self, id: int, stationName: str, t: int) -> None:
        self.check_in[id] = (stationName, t)          # 记下来，像把名字写进字典

    # 乘客 id 在 stationName 出站，时间为 t
    def checkOut(self, id: int, stationName: str, t: int) -> None:
        startStation, startTime = self.check_in.pop(id)   # 取出之前的记录
        travel = t - startTime                            # 计算花了多少分钟
        # 把这趟完整的行程放进“行程簿”
        self.trips.append((id, startStation, stationName, travel))

    # 求从 startStation 到 endStation 的平均旅行时间
    def getAverageTime(self, startStation: str, endStation: str) -> float:
        total = 0          # 累计所有符合条件的行程时间
        cnt = 0            # 计数符合条件的行程有多少条
        for _, s, e, time in self.trips:          # 把行程簿一页页翻
            if s == startStation and e == endStation:
                total += time
                cnt += 1
        return total / cnt if cnt != 0 else 0.0   # 防止除以 0
```

#### 复杂度

- **时间复杂度**  
  - `checkIn` / `checkOut` : **O(1)**（只做字典的增删）  
  - `getAverageTime` : **O(N)**，其中 N 是已完成的出行次数。相当于“把所有行程都翻一遍”，当调用很多次时会成为瓶颈。

- **空间复杂度**  
  - **O(N)**，因为我们把每一次完整的行程都存进列表，列表会随出行次数线性增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**慢点在 `getAverageTime`**：每次都要遍历全部历史记录。我们其实不需要每次都重新统计，只要在每一次 `checkOut` 时把“这趟行程的时间”直接累加到对应的 `(startStation, endStation)` 上，并记下这条路线已经出现了多少次。这样：

- `checkIn` / `checkOut` 仍然是 **O(1)** 的操作。  
- `getAverageTime` 只需要在哈希表里直接读取已经累计好的 **总时间** 与 **次数**，再除即可，时间同样是 **O(1)**。

实现细节：

1. **记录正在乘车的乘客**  
   - 用字典 `check_in` 保存 `id -> (stationName, time)`。这一步和暴力解一样，叫它“正在乘车表”。  
   - 想象成“地铁闸机的临时票据”，只在乘客离站时才会被取走。

2. **累计每条路线的统计信息**  
   - 用另一个字典 `route_stats`，键是 `(startStation, endStation)` 的元组，值是 `[totalTime, cnt]`（总时长、出现次数）。  
   - 这相当于“一本统计账本”，每次有人走完这条线路，就往对应的账目里加上这趟的时间并把次数加 1。

3. **查询平均时间**  
   - 直接取出 `totalTime / cnt`，就是答案。  
   - 因为题目保证所有查询的路线至少出现过一次，所以除以 0 的情况不会出现。

> **核心技巧：** 用哈希表把“动态累计”与“即时查询”解耦。每一次更新都是 **O(1)**，查询同样 **O(1)**，避免了遍历历史记录的成本。

#### 代码（Python）

```python
class UndergroundSystem:
    def __init__(self):
        # 正在乘车的乘客：id -> (stationName, checkInTime)
        self.check_in = {}                     # 类似闸机临时票据
        # 统计每条路线的累计信息： (start, end) -> [totalTime, count]
        self.route_stats = {}                  # 类似账本

    def checkIn(self, id: int, stationName: str, t: int) -> None:
        # 把乘客的起点和时间记下来，后面出站时会用到
        self.check_in[id] = (stationName, t)

    def checkOut(self, id: int, stationName: str, t: int) -> None:
        # 取出该乘客的起点和签到时间
        startStation, startTime = self.check_in.pop(id)
        travel = t - startTime                 # 本次旅行用了多少分钟

        # 用 (起点, 终点) 作为键，更新累计总时间和出现次数
        key = (startStation, stationName)
        if key not in self.route_stats:
            # 第一次出现这条路线，先创建记录
            self.route_stats[key] = [travel, 1]
        else:
            # 已有记录，累计时间并计数加一
            self.route_stats[key][0] += travel
            self.route_stats[key][1] += 1

    def getAverageTime(self, startStation: str, endStation: str) -> float:
        total, cnt = self.route_stats[(startStation, endStation)]
        # 直接算平均值，返回浮点数
        return total / cnt
```

#### 复杂度

- **时间复杂度**  
  - `checkIn` : **O(1)**（字典写入）  
  - `checkOut` : **O(1)**（字典读取、写入）  
  - `getAverageTime` : **O(1)**（字典读取一次并做除法）  
  与暴力解相比，查询不再随历史记录数增长，速度常数级。

- **空间复杂度**  
  - `check_in` 最多存放当前在车的乘客数，最多 **O(P)**，P ≤ 总调用数。  
  - `route_stats` 最多存放不同起终站组合的统计信息，最多 **O(R)**，R 为不同路线的数量（在最坏情况下也是 O(N)），但每条路线只保存两个数字，远小于保存所有行程的列表。总体仍是 **O(N)**，但常数更小，且不随查询次数增加。

---

## 心得

- **核心技巧**：使用哈希表把“每次出站的增量信息”直接累计到对应的路线统计上，实现 **增删改查皆 O(1)**。  
- **适用场景**：  
  1. **实时统计类**（例如：统计每个商品的平均购买时间、每个用户的平均在线时长）。  
  2. **频繁查询、少量更新的计数/求和问题（如 LeetCode 1356 `Station Connections`、1695 `Maximum Erasure Value` 的滑动窗口统计）**。  
  3. **设计题目**中常出现的“记录并求平均”“记录并求最大/最小”等需求。  
- **一句话总结**：**“把每次产生的增量立刻写进对应的统计表，查询时直接读取就行”。**

---

## 反思

- **拿到题目第一反应**：先用列表把所有出行记录下来，等查询时再遍历统计——这是一种最自然的“先记后算”思路。  
- **最容易踩的坑**  
  1. **忘记在 `checkOut` 时把乘客从 `check_in` 表中删除**，导致后续同一 `id` 再次 `checkIn` 时冲突。  
  2. **键的设计**：如果只用 `startStation` 或 `endStation` 作为键，会把不同路线混在一起，导致平均时间错误。必须用 `(start, end)` 元组唯一标识一条路线。  
  3. **除法精度**：返回值要求误差 ≤ 10⁻⁵，直接使用 Python 的浮点除法即可，无需额外处理。  
- **下次遇到同类题的第一步**：先问自己“是否可以在每一次事件发生时把需要的统计量即时累计？”如果答案是“可以”，就直接用哈希表实现 O(1) 的增量更新，而不是等到查询时再遍历全部历史。