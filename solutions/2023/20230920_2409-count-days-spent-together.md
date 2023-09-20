# #2409. **共同逗留天数** / Count Days Spent Together

> 难度：简单 · 标签：Math、String · [LeetCode 链接](https://leetcode.com/problems/count-days-spent-together/)

---

## 题目（英文原版）

**Description**

Alice and Bob are traveling to Rome for separate business meetings.
You are given 4 strings arriveAlice, leaveAlice, arriveBob, and leaveBob. Alice will be in the city from the dates arriveAlice to leaveAlice (inclusive), while Bob will be in the city from the dates arriveBob to leaveBob (inclusive). Each will be a 5-character string in the format "MM-DD", corresponding to the month and day of the date.
Return the total number of days that Alice and Bob are in Rome together.
You can assume that all dates occur in the same calendar year, which is not a leap year. Note that the number of days per month can be represented as: [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31].

**Examples**

**Example 1:**

```
Input: arriveAlice = "08-15", leaveAlice = "08-18", arriveBob = "08-16", leaveBob = "08-19"
Output: 3
Explanation: Alice will be in Rome from August 15 to August 18. Bob will be in Rome from August 16 to August 19. They are both in Rome together on August 16th, 17th, and 18th, so the answer is 3.
```

**Example 2:**

```
Input: arriveAlice = "10-01", leaveAlice = "10-31", arriveBob = "11-01", leaveBob = "12-31"
Output: 0
Explanation: There is no day when Alice and Bob are in Rome together, so we return 0.
```

**Constraints**

- All dates are provided in the format "MM-DD".
- Alice and Bob's arrival dates are earlier than or equal to their leaving dates.
- The given dates are valid dates of a non-leap year.

---

## 题目（中文翻译）

Alice 和 Bob 分别因商务会议前往罗马。  
给定四个字符串 `arriveAlice`、`leaveAlice`、`arriveBob`、`leaveBob`。Alice 在城市的逗留时间为 `arriveAlice` 到 `leaveAlice`（**inclusive**，即包含起止日期），Bob 的逗留时间为 `arriveBob` 到 `leaveBob`（**inclusive**）。每个字符串都是长度为 5 的 `"MM-DD"` 形式，表示月份和日期。  

返回 Alice 与 Bob 同时在罗马的天数总和。  

可以假设所有日期都在同一日历年，且该年不是闰年（**leap year**）。每个月的天数如下（**month days**）：`[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]`。

---

### 示例

**示例 1**  
```text
Input: arriveAlice = "08-15", leaveAlice = "08-18", arriveBob = "08-16", leaveBob = "08-19"
Output: 3
Explanation: Alice 的逗留时间为 8 月 15 日到 8 月 18 日，Bob 的逗留时间为 8 月 16 日到 8 月 19 日。他们共同在 8 月 16、17、18 日在罗马，所以答案为 3。
```

**示例 2**  
```text
Input: arriveAlice = "10-01", leaveAlice = "10-31", arriveBob = "11-01", leaveBob = "12-31"
Output: 0
Explanation: 没有任何一天是 Alice 与 Bob 同时在罗马的，因此返回 0。
```

---

### 约束条件

- 所有日期均采用 `"MM-DD"` 格式。
- Alice 与 Bob 的到达日期不晚于各自的离开日期。
- 给出的日期均为非闰年中的有效日期。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把一年 365 天全部列出来，逐天检查 Alice 和 Bob 是否都在罗马。  
- **把日期转成「第几天」**：比如 01-01 是第 1 天，02-01 是第 32 天（因为 1 月有 31 天），以此类推。这里可以把月份和每个月的天数想成一本“日历字典”，键是月份，值是该月之前累计的天数。  
- **遍历 1~365**：对每一天 `d`，判断 `d` 是否在 Alice 的区间 `[arriveAlice, leaveAlice]` 且在 Bob 的区间 `[arriveBob, leaveBob]`，如果同时满足，就把答案加 1。  

这种做法之所以一定能得到正确答案，是因为我们把所有可能的日期都枚举了一遍，绝不会遗漏交集的任何一天。

#### 代码（Python）  

```python
def countDaysTogether(arriveAlice: str, leaveAlice: str,
                      arriveBob: str,   leaveBob: str) -> int:
    # 每个月的天数（非闰年）
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # 辅助函数：把 "MM-DD" 转成一年中的第几天
    def to_day_of_year(date: str) -> int:
        month = int(date[:2])          # 取前两位月份
        day   = int(date[3:])          # 取后两位日期
        # 累加前面几个月的天数，再加上当前月份的 day
        return sum(month_days[:month-1]) + day

    # 把四个日期都转成「第几天」
    a_start = to_day_of_year(arriveAlice)
    a_end   = to_day_of_year(leaveAlice)
    b_start = to_day_of_year(arriveBob)
    b_end   = to_day_of_year(leaveBob)

    # 暴力遍历 1~365，统计两人都在的天数
    together = 0
    for d in range(1, 366):                 # 365 天，Python 区间左闭右开
        if a_start <= d <= a_end and b_start <= d <= b_end:
            together += 1
    return together
```

#### 复杂度  

- **时间复杂度：** `O(365)` ≈ `O(1)`。虽然我们遍历了 365 天，但这是一条常数长度的循环，和输入规模无关。可以把它想成“最多检查 365 次”，即使在最差情况下也只需要这么多步。  
- **空间复杂度：** `O(1)`。只用了几个整数变量，额外占用的内存不随输入大小变化。

---

### 2. 最优解  

#### 思路  

暴力解的“慢”在于我们把所有 365 天都检查了一遍，实际上只需要关心两个时间区间的交集。  
**关键观察**：  
- Alice 在 `[a_start, a_end]` 之间，Bob 在 `[b_start, b_end]` 之间。  
- 两人的共同天数就是这两个区间的交集长度。  

于是我们可以把日期直接转成“一年中的第几天”，然后用公式求交集：

```
overlap_start = max(a_start, b_start)   # 交集左端点
overlap_end   = min(a_end,   b_end)     # 交集右端点
如果 overlap_start > overlap_end → 没有交集，答案 0
否则答案 = overlap_end - overlap_start + 1   # +1 因为两端都算在内
```

这里唯一需要的工具仍是 **日期 → 天数** 的映射。我们把月份累计天数的数组想成一本“日历字典”，查找非常快（只需一次求和），相当于 **哈希表**（key 是月份，value 是该月之前的天数），但这里用列表更直接。

#### 代码（Python）  

```python
def countDaysTogether(arriveAlice: str, leaveAlice: str,
                      arriveBob: str,   leaveBob: str) -> int:
    # 每个月的天数（非闰年），下标 0 代表 1 月
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # 把 "MM-DD" 转成一年中的第几天
    def to_day_of_year(date: str) -> int:
        month = int(date[:2])          # 例 "08-15" → month = 8
        day   = int(date[3:])          # 例 "08-15" → day   = 15
        # 前 (month-1) 个月的天数之和 + 当前月的 day
        return sum(month_days[:month-1]) + day

    a_start = to_day_of_year(arriveAlice)
    a_end   = to_day_of_year(leaveAlice)
    b_start = to_day_of_year(arriveBob)
    b_end   = to_day_of_year(leaveBob)

    # 交集的左端点是两个人开始时间的较大者
    overlap_start = max(a_start, b_start)
    # 交集的右端点是两个人结束时间的较小者
    overlap_end   = min(a_end,   b_end)

    # 若左端点大于右端点，说明没有重叠天数
    if overlap_start > overlap_end:
        return 0
    # 两端都算在内，所以要 +1
    return overlap_end - overlap_start + 1
```

#### 复杂度  

- **时间复杂度：** `O(1)`。只做了常数次的整数运算和一次列表切片求和（列表长度最多 12），与输入大小无关。相比暴力的 365 次循环，这里几乎瞬间完成。  
- **空间复杂度：** `O(1)`。同样只用了几个整数变量和一个固定长度的列表。

---

## 心得  

- **核心技巧**：把日期统一转成「一年中的第几天」后，用区间交集公式直接求答案。  
- **适用的题型**：  
  1. 两个或多个时间段的重叠天数（如会议室预约冲突）。  
  2. 计算两个日期范围的交集长度（如租房合同重叠天数）。  
- **解题钥匙**：**把日期映射到线性坐标，再用区间交集**。

---

## 反思  

- **第一反应**：看到“统计共同天数”，立刻想到“遍历每一天”。这在不考虑规模时是自然的想法。  
- **最容易踩的坑**：  
  - 忽略了日期是 **包含** 两端的，需要在交集长度上加 `+1`。  
  - 把闰年和非闰年搞混，导致二月份天数错误。  
  - 处理月份前导零（如 `"01-05"`）时直接转整数即可，避免字符串拼接错误。  
- **下次遇到同类题**：第一步先把所有日期转成“一年中的第几天”，再在 **数轴** 上做区间运算——这样往往能直接得到 `O(1)` 的最优解。