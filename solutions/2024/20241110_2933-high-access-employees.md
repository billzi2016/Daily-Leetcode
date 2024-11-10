# #2933. 高访问员工 / High-Access Employees

> 难度：中等 · 标签：Array、Hash Table、String、Sorting · [LeetCode 链接](https://leetcode.com/problems/high-access-employees/)

---

## 题目（英文原版）

**Description**

You are given a 2D 0-indexed array of strings, access_times, with size n. For each i where 0 <= i <= n - 1, access_times[i][0] represents the name of an employee, and access_times[i][1] represents the access time of that employee. All entries in access_times are within the same day.
The access time is represented as four digits using a 24-hour time format, for example, "0800" or "2250".
An employee is said to be high-access if he has accessed the system three or more times within a one-hour period.
Times with exactly one hour of difference are not considered part of the same one-hour period. For example, "0815" and "0915" are not part of the same one-hour period.
Access times at the start and end of the day are not counted within the same one-hour period. For example, "0005" and "2350" are not part of the same one-hour period.
Return a list that contains the names of high-access employees with any order you want.

**Examples**

**Example 1:**

```
Input: access_times = [["a","0549"],["b","0457"],["a","0532"],["a","0621"],["b","0540"]]
Output: ["a"]
Explanation: "a" has three access times in the one-hour period of [05:32, 06:31] which are 05:32, 05:49, and 06:21.
But "b" does not have more than two access times at all.
So the answer is ["a"].
```

**Example 2:**

```
Input: access_times = [["d","0002"],["c","0808"],["c","0829"],["e","0215"],["d","1508"],["d","1444"],["d","1410"],["c","0809"]]
Output: ["c","d"]
Explanation: "c" has three access times in the one-hour period of [08:08, 09:07] which are 08:08, 08:09, and 08:29.
"d" has also three access times in the one-hour period of [14:10, 15:09] which are 14:10, 14:44, and 15:08.
However, "e" has just one access time, so it can not be in the answer and the final answer is ["c","d"].
```

**Example 3:**

```
Input: access_times = [["cd","1025"],["ab","1025"],["cd","1046"],["cd","1055"],["ab","1124"],["ab","1120"]]
Output: ["ab","cd"]
Explanation: "ab" has three access times in the one-hour period of [10:25, 11:24] which are 10:25, 11:20, and 11:24.
"cd" has also three access times in the one-hour period of [10:25, 11:24] which are 10:25, 10:46, and 10:55.
So the answer is ["ab","cd"].
```

**Constraints**

- 1 <= access_times.length <= 100
- access_times[i].length == 2
- 1 <= access_times[i][0].length <= 10
- access_times[i][0] consists only of English small letters.
- access_times[i][1].length == 4
- access_times[i][1] is in 24-hour time format.
- access_times[i][1] consists only of '0' to '9'.

---

## 题目（中文翻译）

**题目描述**  
给定一个下标从 **0** 开始的二维字符串数组 `access_times`，其大小为 `n`。对每个满足 `0 <= i <= n - 1` 的 `i`，`access_times[i][0]` 表示某位员工的姓名，`access_times[i][1]` 表示该员工的访问时间。所有记录均发生在同一天内。  
访问时间采用四位数的 24 小时制表示，例如 `"0800"` 或 `"2250"`。  

如果某位员工在 **一小时内**（**one-hour period**）的访问次数达到 **三次或以上**，则该员工被称为 **高访问（high-access）** 员工。  
- **恰好相差一小时的时间不算在同一个一小时内**。例如 `"0815"` 与 `"0915"` 不属于同一时间段。  
- **跨天的时间也不算在同一个一小时内**。例如 `"0005"` 与 `"2350"` 不属于同一时间段。  

返回一个字符串列表，包含所有高访问员工的姓名，顺序不限。

**示例 1**  
```text
Input: access_times = [["a","0549"],["b","0457"],["a","0532"],["a","0621"],["b","0540"]]
Output: ["a"]
Explanation: "a" 在时间段 [05:32, 06:31] 内有三次访问，分别是 05:32、05:49 和 06:21。  
但 "b" 的访问次数均不超过两次。  
因此答案为 ["a"]。
```

**示例 2**  
```text
Input: access_times = [["d","0002"],["c","0808"],["c","0829"],["e","0215"],["d","1508"],["d","1444"],["d","1410"],["c","0809"]]
Output: ["c","d"]
Explanation: "c" 在时间段 [08:08, 09:07] 内有三次访问，分别是 08:08、08:09 和 08:29。  
"d" 在时间段 [14:10, 15:09] 内也有三次访问，分别是 14:10、14:44 和 15:08。  
然而 "e" 只有一次访问，未达到高访问标准。  
因此答案为 ["c","d"]。
```

**示例 3**  
```text
Input: access_times = [["cd","1025"],["ab","1025"],["cd","1046"],["cd","1055"],["ab","1124"],["ab","1120"]]
Output: ["ab","cd"]
Explanation: "ab" 在时间段 [10:25, 11:24] 内有三次访问，分别是 10:25、11:20 和 11:24。  
"cd" 在同一时间段内也有三次访问，分别是 10:25、10:46 和 10:55。  
因此答案为 ["ab","cd"]。
```

**约束条件**  
- `1 <= access_times.length <= 100`  
- `access_times[i].length == 2`  
- `1 <= access_times[i][0].length <= 10`  
- `access_times[i][0]` 仅由英文字母小写组成  
- `access_times[i][1].length == 4`  
- `access_times[i][1]` 为 24 小时制时间格式  
- `access_times[i][1]` 仅包含字符 `'0'` 到 `'9'`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

1. **把同一个人的打卡记录挑出来**  
   用 **哈希表**（可以把它想象成一本“员工 → 打卡时间列表”的小字典，`key` 是员工姓名，`value` 是该员工所有的时间）把所有记录分组。

2. **枚举每个人的所有三次组合**  
   对于某个员工，假设他有 `m` 条记录。把这 `m` 条记录两两组合后再挑第三条，即 **三重循环** `i < j < k`，检查这三次打卡的最早时间和最晚时间相差是否 **严格小于 60 分钟**。如果有任意一组满足条件，这个人就是 “high‑access”。

3. **把满足条件的名字放进答案**  

> **为什么这种方法一定能得到正确答案？**  
> 我们把每个人所有可能的三次访问都穷举一遍，只要有一次满足“一小时内出现 3 次”，必然会被检测到。没有遗漏，也没有误判。

#### 代码（Python）

```python
from typing import List
from collections import defaultdict

def to_minutes(t: str) -> int:
    """把 'HHMM' 形式的字符串转成当天的分钟数，例如 '0815' -> 8*60+15"""
    hour = int(t[:2])
    minute = int(t[2:])
    return hour * 60 + minute

def high_access_employees_brute(access_times: List[List[str]]) -> List[str]:
    # 1️⃣ 用哈希表把同名的时间放在一起
    records = defaultdict(list)          # {name: [time_str, ...]}
    for name, tm in access_times:
        records[name].append(tm)

    high = []                             # 最终答案

    # 2️⃣ 对每个人的所有三元组进行暴力枚举
    for name, times in records.items():
        n = len(times)
        if n < 3:                         # 少于 3 条根本不可能满足条件
            continue
        # 把时间字符串全部转成分钟，方便比较
        minutes = [to_minutes(t) for t in times]

        # 三层循环枚举 i < j < k
        found = False
        for i in range(n - 2):
            for j in range(i + 1, n - 1):
                for k in range(j + 1, n):
                    # 最早与最晚的时间差
                    diff = max(minutes[i], minutes[j], minutes[k]) - \
                           min(minutes[i], minutes[j], minutes[k])
                    if diff < 60:          # 严格小于 60 分钟即满足
                        found = True
                        break
                if found:
                    break
            if found:
                break
        if found:
            high.append(name)

    return high
```

#### 复杂度  

- **时间复杂度**：`O(N * M³)`  
  - `N` 是员工人数（最坏情况下每个人只有 1 条记录，`N ≈ 100`），`M` 是单个员工的记录数。  
  - 对每个人我们用了三层循环，枚举所有三元组，最坏是 `C(M,3) ≈ M³/6`。  
  - 大白话：如果一个员工有 10 条记录，需要检查 120 组组合；如果有 20 条记录，需要检查 1,140 组……随着记录数的增加，检查次数会“爆炸”。

- **空间复杂度**：`O(N + total_records)`  
  - 哈希表保存了所有记录，额外的空间主要是存放时间的整数列表。  
  - 大白话：我们把原来的数据重新放进了一个字典里，大小跟原数据差不多。

> 由于题目规模只有 `≤ 100` 条记录，暴力解在实际运行时还能接受，但我们仍然可以做得更快。

---

### 2. 最优解

#### 思路  

从暴力解出发，**瓶颈** 在于我们对同一个员工的时间做了 **三重循环**，大量重复比较。  
观察下面两点可以帮助我们优化：

1. **同一个员工的时间顺序不影响“一小时内出现 3 次”**  
   只要把所有时间 **排序**（从早到晚），只需要关注相邻的几条记录就可以了。因为如果最早的时间和第 `i+2` 条时间之间已经超过 60 分钟，那么后面的记录更不可能在同一小时内出现 3 次。

2. **滑动窗口（双指针）**  
   把已排序的时间看成一条数轴，**左指针 `l`** 指向窗口最早的时间，**右指针 `r`** 向右扩张。每次把 `r` 往右移动一次，检查窗口大小 `r-l+1` 是否 ≥ 3 且 `times[r] - times[l] < 60`。如果窗口宽度已经 ≥ 60，就把左指针右移，缩小窗口。

   这个过程只遍历每个时间 **一次**，所以是 **线性** 的。

核心步骤如下：

1. 用哈希表把同名的时间收集起来（和暴力解一样）。
2. 把每个人的时间列表转成 **分钟整数** 并 **排序**。
3. 用 **双指针** 在排序后的列表里寻找满足条件的窗口；一旦找到，就把该员工加入答案并停止继续检查（因为只要出现一次即可）。
4. 最后返回所有满足条件的员工名字。

> **类比**：想象你在排队买票，前面的人离你不超过 1 小时（60 分钟）就算“同一批”。当队伍太长或时间差太大时，你就把队首的人“踢出”队列，这就是滑动窗口的思路。

#### 代码（Python）

```python
from typing import List
from collections import defaultdict

def to_minutes(t: str) -> int:
    """'HHMM' -> 当天第几分钟"""
    return int(t[:2]) * 60 + int(t[2:])

def high_access_employees_opt(access_times: List[List[str]]) -> List[str]:
    # 1️⃣ 收集每个人的时间（哈希表）
    records = defaultdict(list)          # {name: [time_str, ...]}
    for name, tm in access_times:
        records[name].append(tm)

    high = []                             # 最终答案

    # 2️⃣ 对每个人分别处理
    for name, times in records.items():
        if len(times) < 3:                # 记录不足 3 条直接跳过
            continue

        # 2️⃣① 转成分钟并排序
        minutes = sorted(to_minutes(t) for t in times)

        # 2️⃣② 双指针滑动窗口
        l = 0                              # 窗口左端
        for r in range(len(minutes)):      # 窗口右端依次右移
            # 当窗口宽度 >= 60 分钟时，左端右移收缩窗口
            while minutes[r] - minutes[l] >= 60:
                l += 1
            # 检查窗口里是否已经有 3 条或以上记录
            if r - l + 1 >= 3:            # r、l 是下标，+1 是元素个数
                high.append(name)
                break                     # 该员工已满足条件，无需继续检查

    return high
```

#### 复杂度  

- **时间复杂度**：`O(N log M)`（`N` 为总记录数，`M` 为单个员工的最大记录数）  
  - 哈希表收集 O(N)。  
  - 对每个人的时间列表做 **排序**，成本是 `O(M log M)`，所有人加起来不超过 `O(N log M)`（因为 `∑ M = N`）。  
  - 双指针遍历每个列表一次，线性 `O(M)`，同样累计为 `O(N)`。  
  - 综合下来，最耗时的步骤是排序，整体是 **对数级** 的提升。  
  - 大白话：相当于把每个人的打卡时间先排好序，然后只在排好序的队列里走一遍，不需要再去挑组合。

- **空间复杂度**：`O(N)`  
  - 需要额外存放每个人的时间列表（整数形式），和原始数据大小相同。  
  - 哈希表本身也占用相同数量的空间。

> 与暴力解相比，时间复杂度从 “指数级” 的 `M³` 降到了 “对数级” 的 `M log M`，在数据量稍大时会快很多。

---

## 心得

- **核心技巧**：  
  1️⃣ 使用哈希表把同一属性（员工姓名）对应的多条记录聚合起来。  
  2️⃣ 对每组数据先排序，再用 **滑动窗口（双指针）** 检查满足 “固定长度内的元素个数 ≥ k” 的条件。

- **适用的题型**（类似思路）  
  - “在一天内出现超过三次登录的用户”（LeetCode 1604）  
  - “找出数组中任意连续子数组长度 ≥ k 且和 ≤ target 的情况”（滑动窗口）  
  - “统计每个单词出现的次数并找出出现次数最多的前 K 个”（哈希表 + 排序）

- **一句话总结解题钥匙**：  
  **“先把同类数据聚合、排序，然后用窗口一次线性扫描，找出满足时间/距离约束的连续片段”。**

---

## 反思

- **第一反应**：看到“同一小时内出现 3 次”就想到要检查时间差，于是直接想把每个人的所有时间枚举三元组——这就是暴力思路。
- **最容易踩的坑**  
  - **时间格式**：`"0800"` 不是整数，需要自行拆分成小时和分钟再转成总分钟数。  
  - **边界条件**：差值必须 **严格小于 60**，等于 60 的情况不算。  
  - **跨天情况**：题目说明所有时间在同一天，故不需要考虑 `2350` 与 `0005` 的跨天窗口。  
  - **提前结束**：一旦某个员工已经满足条件，后面的检查可以直接跳过，避免不必要的计算。

- **下次遇到同类题**：  
  1️⃣ 先用 **哈希表** 把相同键的记录收集起来；  
  2️⃣ 判断是否需要 **排序**（大多数时间相关、数值相关的问题都需要）；  
  3️⃣ 想想 **窗口**（双指针）是否能一次线性遍历解决，而不是枚举组合。  

这样可以快速从 “暴力” 跳到 “最优”，写出既简洁又高效的代码。