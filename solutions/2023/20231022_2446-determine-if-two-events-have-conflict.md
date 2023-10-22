# #2446. 判断两个事件是否冲突 / Determine if Two Events Have Conflict

> 难度：简单 · 标签：Array、String · [LeetCode 链接](https://leetcode.com/problems/determine-if-two-events-have-conflict/)

---

## 题目（英文原版）

**Description**

You are given two arrays of strings that represent two inclusive events that happened on the same day, event1 and event2, where:
Event times are valid 24 hours format in the form of HH:MM.
A conflict happens when two events have some non-empty intersection (i.e., some moment is common to both events).
Return true if there is a conflict between two events. Otherwise, return false.

**Examples**

**Example 1:**

```
Input: event1 = ["01:15","02:00"], event2 = ["02:00","03:00"]
Output: true
Explanation: The two events intersect at time 2:00.
```

**Example 2:**

```
Input: event1 = ["01:00","02:00"], event2 = ["01:20","03:00"]
Output: true
Explanation: The two events intersect starting from 01:20 to 02:00.
```

**Example 3:**

```
Input: event1 = ["10:00","11:00"], event2 = ["14:00","15:00"]
Output: false
Explanation: The two events do not intersect.
```

**Constraints**

- event1.length == event2.length == 2
- event1[i].length == event2[i].length == 5
- startTime1 <= endTime1
- startTime2 <= endTime2
- All the event times follow the HH:MM format.

---

## 题目（中文翻译）

**描述**  
给定两个字符串数组 `event1` 和 `event2`，分别表示同一天内的两个**包含的事件（inclusive events）**，其中：

- 事件时间采用有效的 24 小时制，格式为 `HH:MM`。  
- 当两个事件存在非空交集（即有某个时刻同时属于两个事件）时，称它们发生**冲突（conflict）**。  

返回 `true` 表示两个事件之间存在冲突，否则返回 `false`。

**示例 1**  
**输入**: `event1 = ["01:15","02:00"], event2 = ["02:00","03:00"]`  
**输出**: `true`  
**解释**: 两个事件在 02:00 时刻相交。

**示例 2**  
**输入**: `event1 = ["01:00","02:00"], event2 = ["01:20","03:00"]`  
**输出**: `true`  
**解释**: 两个事件的交集为 01:20 到 02:00。

**示例 3**  
**输入**: `event1 = ["10:00","11:00"], event2 = ["14:00","15:00"]`  
**输出**: `false`  
**解释**: 两个事件没有交集。

**约束条件**  
- `event1.length == event2.length == 2`  
- `event1[i].length == event2[i].length == 5`  
- `startTime1 <= endTime1`  
- `startTime2 <= endTime2`  
- 所有事件时间均遵循 `HH:MM` 格式。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把两个时间段都展开成“一分钟一格”的序列，然后把两段的每一分钟都对比一次，只要出现同一分钟在两段里都出现，就说明有冲突。  

- **使用的数据结构**：把时间点转换成 **整数**（分钟数），再用 **集合（set）** 保存每一分钟出现的标记。集合可以类比成一本“字典”，把每个出现的分钟当成单词，出现与否就是在不在字典里。  
- **为什么正确**：如果两段时间在某一分钟都有出现，那么这分钟一定是它们的交集；遍历所有可能的分钟，必然能捕捉到任何交叉。  

#### 代码（Python）
```python
def haveConflict(event1, event2):
    # 把 "HH:MM" 转成从 00:00 开始的分钟数
    def to_min(t: str) -> int:
        h, m = map(int, t.split(':'))   # 把小时和分钟分别取出来
        return h * 60 + m               # 1 小时 = 60 分钟

    # 把第一个事件的每一分钟放进集合
    start1, end1 = map(to_min, event1)   # 例如 ["01:15","02:00"] -> (75, 120)
    minutes1 = set()
    for minute in range(start1, end1 + 1):   # +1 因为是闭区间
        minutes1.add(minute)                 # 把每一分钟加入集合

    # 把第二个事件的每一分钟逐个检查是否已经在集合里
    start2, end2 = map(to_min, event2)
    for minute in range(start2, end2 + 1):
        if minute in minutes1:               # 如果出现相同的分钟，说明冲突
            return True
    return False
```

#### 复杂度
- **时间复杂度**：`O(L1 + L2)`，其中 `L1`、`L2` 分别是两个事件的时长（分钟数）。如果把一天的 24 小时全展开，最坏是 `O(1440)`，也就是把每一分钟都检查一遍。  
- **空间复杂度**：`O(L1)`，需要用集合保存第一个事件的所有分钟数。

> **大白话解释**：我们把每一分钟都当作一块小砖瓦，逐块铺在集合里，再用另一段的砖瓦去碰撞检查。时间和空间都和砖瓦的数量成正比。

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在于**逐分钟展开**，实际上我们只需要比较两个时间段的起止点即可判断是否有交集。  

1. **把时间字符串转成整数**（同上），得到 `start1、end1、start2、end2` 四个数字，单位都是分钟。  
2. 两个闭区间 `[s1, e1]` 与 `[s2, e2]` 是否有交集，只需要判断它们**不相离**的条件：  
   - `s1` 在 `e2` 之后 → `s1 > e2`（没有交集）  
   - `s2` 在 `e1` 之后 → `s2 > e1`（没有交集）  
   只要上述两种情况都 **不成立**，就一定有交集。  
3. 用 `not (s1 > e2 or s2 > e1)` 即可直接得到答案。

> **类比**：想象两根木棍放在直线上，如果其中一根的左端点在另一根的右端点的右边，那它们肯定不相交；否则必有交点。

#### 代码（Python）
```python
def haveConflict(event1, event2):
    # 把 "HH:MM" 转成分钟数的函数
    def to_min(t: str) -> int:
        h, m = map(int, t.split(':'))
        return h * 60 + m

    start1, end1 = map(to_min, event1)   # 第一个事件的起止分钟
    start2, end2 = map(to_min, event2)   # 第二个事件的起止分钟

    # 若任意一方的开始时间在另一方结束时间之后，则不冲突
    # 否则一定有交集
    return not (start1 > end2 or start2 > end1)
```

#### 复杂度
- **时间复杂度**：`O(1)`，只做了常数次的字符串拆分、整数运算和比较。  
- **空间复杂度**：`O(1)`，只用了常数个变量来保存分钟数。

> 与暴力解相比，**时间从遍历每一分钟降到了常数时间**，空间也从集合降到只用几个整数，效率提升巨大。

---

## 心得

- **核心技巧**：**区间重叠判定**（只比较端点）。  
- **适用的题型**  
  1. 判断两个会议是否冲突（本题）。  
  2. 合并所有重叠区间（LeetCode 56 Merge Intervals）。  
  3. 给定多个活动，求最多可以参加多少个不冲突的活动（LeetCode 435 Non-overlapping Intervals）。  
- **一句话总结**：只要两段时间的起点不在对方的终点之后，它们就会相交。

---

## 反思

- **第一反应**：把时间拆成分钟，然后想“遍历每一分钟”。这虽然能得到正确答案，但显得笨拙。  
- **最容易踩的坑**  
  - 忽略了题目说明是 **闭区间**（包括起止时间），导致判断条件写成 `>=` 而不是 `>`，会把相邻但不重叠的情况误判为冲突。  
  - 没有处理跨午夜的情况（本题约束不出现），但如果出现，需要把时间映射到 0~1439 的环上。  
- **下次遇到同类题**：第一步先把时间或数值统一到同一种度量（如分钟），然后直接用**端点比较**判断是否相交，而不是逐个枚举。