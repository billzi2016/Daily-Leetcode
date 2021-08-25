# #1450. 在指定时间做作业的学生人数 / Number of Students Doing Homework at a Given Time

> 难度：简单 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/number-of-students-doing-homework-at-a-given-time/)

---

## 题目（英文原版）

**Description**

Given two integer arrays startTime and endTime and given an integer queryTime.
The ith student started doing their homework at the time startTime[i] and finished it at time endTime[i].
Return the number of students doing their homework at time queryTime. More formally, return the number of students where queryTime lays in the interval [startTime[i], endTime[i]] inclusive.

**Examples**

**Example 1:**

```
Input: startTime = [1,2,3], endTime = [3,2,7], queryTime = 4
Output: 1
Explanation: We have 3 students where:
The first student started doing homework at time 1 and finished at time 3 and wasn't doing anything at time 4.
The second student started doing homework at time 2 and finished at time 2 and also wasn't doing anything at time 4.
The third student started doing homework at time 3 and finished at time 7 and was the only student doing homework at time 4.
```

**Example 2:**

```
Input: startTime = [4], endTime = [4], queryTime = 4
Output: 1
Explanation: The only student was doing their homework at the queryTime.
```

**Constraints**

- startTime.length == endTime.length
- 1 <= startTime.length <= 100
- 1 <= startTime[i] <= endTime[i] <= 1000
- 1 <= queryTime <= 1000

---

## 题目（中文翻译）

**描述**  
给定两个整数数组（integer arrays）`startTime` 和 `endTime`，以及一个整数 `queryTime`。第 `i` 位学生在时间 `startTime[i]` 开始做作业，在时间 `endTime[i]` 完成作业。返回在时间 `queryTime` 正在做作业的学生人数。更正式地说，返回满足 `queryTime` 位于区间 `[startTime[i], endTime[i]]`（包含端点）内的学生数量。

**示例**

**示例 1**  
```
Input: startTime = [1,2,3], endTime = [3,2,7], queryTime = 4
Output: 1
Explanation: 我们有 3 位学生：
- 第 1 位学生在时间 1 开始做作业，时间 3 完成，在时间 4 时不在做作业。
- 第 2 位学生在时间 2 开始并在时间 2 完成，同样在时间 4 时不在做作业。
- 第 3 位学生在时间 3 开始做作业，时间 7 完成，且在时间 4 时正在做作业。
```

**示例 2**  
```
Input: startTime = [4], endTime = [4], queryTime = 4
Output: 1
Explanation: 唯一的学生在 queryTime 时正在做作业。
```

**约束条件**
- `startTime.length == endTime.length`
- `1 <= startTime.length <= 100`
- `1 <= startTime[i] <= endTime[i] <= 1000`
- `1 <= queryTime <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把每个学生的学习时间段 `[startTime[i], endTime[i]]` 拿出来，逐个检查 **queryTime** 是否落在这个区间里。  
这和我们平时查字典的过程类似：  
- **哈希表** 就像一本字典，`key` 是单词，`value` 是对应的解释。  
- **这里的“字典”** 是「学生 → 他/她的学习时间段」。我们只需要遍历所有学生（相当于把字典的每一条目都翻一遍），看 **queryTime** 是否在该学生的时间段内。

只要遍历完所有学生，计数器加一的次数就是答案。

> **为什么正确**  
> 对每个学生，若 `startTime[i] ≤ queryTime ≤ endTime[i]` 成立，则说明此时此刻该学生正在做作业。把所有满足条件的学生都统计出来，自然就是答案。

#### 代码（Python）

```python
def busyStudent(startTime, endTime, queryTime):
    """
    :param startTime: List[int] 学生开始做作业的时间
    :param endTime:   List[int] 学生结束做作业的时间
    :param queryTime: int      要查询的时间点
    :return: int  在 queryTime 时正在做作业的学生人数
    """
    cnt = 0                     # 计数器，记录符合条件的学生数量
    for s, e in zip(startTime, endTime):   # 同时遍历 startTime 与 endTime
        # 判断 queryTime 是否落在 [s, e] 区间（两端都包括）
        if s <= queryTime <= e:
            cnt += 1            # 符合条件，计数器加一
    return cnt
```

#### 复杂度  

- **时间复杂度：** `O(n)`  
  这里的 `n` 是学生的数量（即数组长度）。我们只需要遍历一次数组，检查每个学生一次。  
  用大白话说，就是“**随着学生人数线性增长，程序跑的时间也线性增长**”。  

- **空间复杂度：** `O(1)`  
  只用了几个额外的变量（计数器 `cnt` 和循环临时变量），和学生人数无关，所占内存是常数级的。

---

### 2. 最优解

#### 思路  

从暴力解来看，**瓶颈** 并不在这里——已经是 `O(n)` 的线性遍历，已经是遍历所有学生的下界（因为每个学生的信息都必须看一遍才能判断）。  
但是如果**同一组 `startTime / endTime` 会被多次查询不同的 `queryTime`**，每次都 `O(n)` 就会显得“慢”。  
这时我们可以把所有时间段先“压平”到一条时间轴上，用**差分数组 + 前缀和**的技巧，只需一次预处理（`O(T)`，`T` 为时间轴的最大值），随后每个查询都能在 `O(1)` 时间内得到答案。

> **核心概念——差分数组**  
> 把区间 `[l, r]` 看作在时间 `l` 开始 +1，在时间 `r+1` 结束 -1。把所有学生的区间都这样标记后，对时间轴做前缀和，就得到“每个时刻有多少学生在做作业”。  
> 这就像我们在记录每日新增的感染人数（+1）和治愈人数（-1），随后累加得到当天的在院患者数。

#### 代码（Python）

```python
def busyStudent(startTime, endTime, queryTime):
    """
    当会有多次查询时，这种实现可以把每次查询的时间降到 O(1)。
    这里仍然返回单次 queryTime 的答案，保持接口一致。
    """
    # 1. 确定时间轴的长度（题目最大时间 ≤ 1000）
    max_time = max(max(startTime), max(endTime), queryTime) + 2   # +2 防止 r+1 越界

    diff = [0] * max_time          # 差分数组，初始化全为 0

    # 2. 把每个学生的区间转化为差分标记
    for s, e in zip(startTime, endTime):
        diff[s] += 1               # 在 s 时刻人数 +1
        diff[e + 1] -= 1           # 在 e+1 时刻人数 -1（区间是闭区间）

    # 3. 前缀和 → 每个时刻正在做作业的人数
    cur = 0
    for t in range(max_time):
        cur += diff[t]             # 累加差分得到当前时刻人数
        if t == queryTime:         # 一旦走到查询时间，直接返回
            return cur

    return 0   # 理论上不会走到这里，因为 queryTime 必在范围内
```

> **说明**  
> - 第 2 步的 `diff[e + 1] -= 1` 是关键，它确保在 `e` 时刻仍然算作在做作业，而在 `e+1` 时刻人数开始下降。  
> - 第 3 步遍历到 `queryTime` 时即得到答案，若有多个查询，只需继续遍历一次前缀和数组即可得到所有答案。

#### 复杂度  

- **时间复杂度：** `O(T + n)`（预处理） + `O(1)`（单次查询）  
  - `T` 为时间轴的最大长度（≤ 1000），`n` 为学生数量。  
  - 对比暴力解的 `O(n)`，如果查询次数 `q` 很大，整体时间会变成 `O(T + n + q·1)`，远快于 `O(q·n)`。

- **空间复杂度：** `O(T)`  
  需要一个长度为 `max_time` 的额外数组来存放差分信息。  
  对于本题的约束（`max_time ≤ 1000`），这也是非常小的开销。

---

## 心得

- **核心技巧**：区间计数 → 差分数组 + 前缀和  
- **适用题型**  
  1. “某时刻有多少人在工作/上课/观看视频” 类的区间统计题。  
  2. “给定若干时间段，求某时刻的最大重叠区间数” 类的题目（如会议室安排）。  
- **解题钥匙**：**把区间转化为“在起点 +1、在终点+1 处 -1”，再累加得到每个时刻的实际人数**。

---

## 反思

- **第一反应**：直接遍历每个学生，判断 `queryTime` 是否落在他的时间段内。  
- **最容易踩的坑**  
  - **闭区间**：题目说明区间是 `[start, end]`，所以判断条件要写成 `≤` 而不是 `<`。  
  - **数组越界**：在使用差分数组时，记得给 `end+1` 预留空间，否则会出现 IndexError。  
  - **特殊情况**：只有一个学生且 `start = end = queryTime`，仍然算作正在做作业。  
- **下次类似题**：第一步先判断是**只需要一次查询**（直接遍历）还是**多次查询**（考虑差分+前缀和），再决定采用哪种实现。