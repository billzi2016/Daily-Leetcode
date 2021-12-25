# #1604. 一小时内同一员工使用钥匙卡三次或以上的警报 / Alert Using Same Key-Card Three or More Times in a One Hour Period

> 难度：中等 · 标签：Array、Hash Table、String、Sorting · [LeetCode 链接](https://leetcode.com/problems/alert-using-same-key-card-three-or-more-times-in-a-one-hour-period/)

---

## 题目（英文原版）

**Description**

LeetCode company workers use key-cards to unlock office doors. Each time a worker uses their key-card, the security system saves the worker's name and the time when it was used. The system emits an alert if any worker uses the key-card three or more times in a one-hour period.
You are given a list of strings keyName and keyTime where [keyName[i], keyTime[i]] corresponds to a person's name and the time when their key-card was used in a single day.
Access times are given in the 24-hour time format "HH:MM", such as "23:51" and "09:49".
Return a list of unique worker names who received an alert for frequent keycard use. Sort the names in ascending order alphabetically.
Notice that "10:00" - "11:00" is considered to be within a one-hour period, while "22:51" - "23:52" is not considered to be within a one-hour period.

**Examples**

**Example 1:**

```
Input: keyName = ["daniel","daniel","daniel","luis","luis","luis","luis"], keyTime = ["10:00","10:40","11:00","09:00","11:00","13:00","15:00"]
Output: ["daniel"]
Explanation: "daniel" used the keycard 3 times in a one-hour period ("10:00","10:40", "11:00").
```

**Example 2:**

```
Input: keyName = ["alice","alice","alice","bob","bob","bob","bob"], keyTime = ["12:01","12:00","18:00","21:00","21:20","21:30","23:00"]
Output: ["bob"]
Explanation: "bob" used the keycard 3 times in a one-hour period ("21:00","21:20", "21:30").
```

**Constraints**

- 1 <= keyName.length, keyTime.length <= 105
- keyName.length == keyTime.length
- keyTime[i] is in the format "HH:MM".
- [keyName[i], keyTime[i]] is unique.
- 1 <= keyName[i].length <= 10
- keyName[i] contains only lowercase English letters.

---

## 题目（中文翻译）

LeetCode 公司员工使用钥匙卡（key‑card）打开办公室的大门。每当员工使用钥匙卡时，安全系统会记录该员工的姓名以及使用的时间。如果同一员工在 **一小时内**（one‑hour period）使用钥匙卡 **三次或以上**，系统会触发警报（alert）。

给定两个等长字符串数组 `keyName` 和 `keyTime`，其中 `keyName[i]` 与 `keyTime[i]` 分别表示第 `i` 次刷卡的员工姓名和刷卡时间（同一天内）。刷卡时间采用 24 小时制，格式为 `"HH:MM"`，例如 `"23:51"`、`"09:49"`。

返回所有触发警报的 **唯一** 员工姓名列表，按字母升序排序。

> 注意，时间段 `"10:00"`‑`"11:00"` 被视为 **一小时内**，而 `"22:51"`‑`"23:52"` 则不算。

---

## 示例

### 示例 1

**输入**  
```text
keyName = ["daniel","daniel","daniel","luis","luis","luis","luis"]
keyTime = ["10:00","10:40","11:00","09:00","11:00","13:00","15:00"]
```

**输出**  
```text
["daniel"]
```

**解释**  
`"daniel"` 在一小时内使用了钥匙卡三次，时间分别为 `"10:00"`、`"10:40"`、`"11:00"`，因此触发警报。

### 示例 2

**输入**  
```text
keyName = ["alice","alice","alice","bob","bob","bob","bob"]
keyTime = ["12:01","12:00","18:00","21:00","21:20","21:30","23:00"]
```

**输出**  
```text
["bob"]
```

**解释**  
`"bob"` 在一小时内使用了钥匙卡三次，时间分别为 `"21:00"`、`"21:20"`、`"21:30"`，因此触发警报。

---

## 约束条件

- `1 <= keyName.length, keyTime.length <= 10^5`
- `keyName.length == keyTime.length`
- `keyTime[i]` 的格式为 `"HH:MM"`
- `[keyName[i], keyTime[i]]` 互不相同
- `1 <= keyName[i].length <= 10`
- `keyName[i]` 只包含小写英文字母

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是**对每个人的每一次刷卡记录都去找它后面的两次记录**，看这三次刷卡的时间差是否不超过 1 小时。  
- **数据结构**：我们把 `keyName[i]`、`keyTime[i]` 直接放进两个列表里，用下标 `i` 来关联姓名和时间。可以把每个人的所有记录看成一张“刷卡表”。  
- **为什么正确**：只要在表中找到任意三次刷卡的时间间隔 ≤ 60 分钟，就满足题目“在一小时内刷卡三次或以上”。遍历全部组合自然不会漏掉任何可能的情况。  
- **复杂度大白话**：  
  - 对每个人，设他一共刷了 `k` 次卡。要检查所有 **三元组**（即任意挑 3 次刷卡），组合数是 `C(k,3) = k·(k‑1)·(k‑2)/6`，这在最坏情况下接近 `k³`。  
  - 整体上相当于对 `n` 条记录做三层循环，时间复杂度是 **O(n³)**，这在 `n ≤ 10⁵` 时根本跑不完。  
  - 我们只用几个列表和几个整数，空间占用是 **O(n)**（保存原始输入）。

#### 代码（Python）

```python
from typing import List

def alertNames_bruteforce(keyName: List[str], keyTime: List[str]) -> List[str]:
    n = len(keyName)
    # 把时间字符串直接保留下来，后面会转成分钟再比较
    alert_set = set()                     # 用集合自动去重

    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                # 必须是同一个人
                if keyName[i] != keyName[j] or keyName[i] != keyName[k]:
                    continue
                # 把 "HH:MM" 转成分钟数，方便做差
                t1 = int(keyTime[i][:2]) * 60 + int(keyTime[i][3:])
                t2 = int(keyTime[j][:2]) * 60 + int(keyTime[j][3:])
                t3 = int(keyTime[k][:2]) * 60 + int(keyTime[k][3:])
                # 只要三次刷卡的最大时间 - 最小时间 ≤ 60，就满足
                if max(t1, t2, t3) - min(t1, t2, t3) <= 60:
                    alert_set.add(keyName[i])
    # 返回字典序排序的列表
    return sorted(alert_set)
```

#### 复杂度

- **时间复杂度**：`O(n³)`  
  - “³” 代表三层循环，实际意义是：如果有 10 万条记录，算法要检查约 `10^15` 次组合，根本不可行。
- **空间复杂度**：`O(n)`  
  - 只用了存放原始输入的列表和一个集合保存结果，额外开销与 `n` 成线性关系。

---

### 2. 最优解

#### 思路  
从暴力解可以看到，**瓶颈在于重复遍历同一个人的所有刷卡时间**。如果我们先把每个人的刷卡时间**排序**，那么只需要在有序序列里检查**相邻的三个时间**是否在 1 小时内即可。  
- **为什么排序后只检查相邻三次**？  
  - 排序后，时间从早到晚排列。若某三次刷卡 `t_a < t_b < t_c` 满足 `t_c - t_a ≤ 60`，那么这三次一定是**相邻的**（在它们之间不可能再有别的刷卡时间，否则那个时间会把窗口拉宽，使 `t_c - t_a` 更大）。因此只要在有序序列里滑动一个长度为 3 的窗口，就能捕捉所有满足条件的情况。  
- **核心技巧**：  
  1. **哈希表（字典）**：把同一个人的所有时间放进同一个列表里。哈希表就像“名字 → 时间列表”的字典，查找 O(1)。  
  2. **时间转整数**：把 `"HH:MM"` 统一转成 **分钟数**（`hour*60 + minute`），这样比较只用整数减法。  
  3. **排序**：对每个人的时间列表进行升序排序，复杂度 `O(k log k)`，`k` 是该人的刷卡次数。  
  4. **滑动窗口**：遍历排序后的列表，用下标 `i` 表示窗口左端，检查 `times[i+2] - times[i] ≤ 60`。如果成立，立刻把名字加入结果集合。  

- **类比**：把每个人的刷卡时间想象成一排排的**灯泡**，灯泡亮的时间点是分钟数。我们要找的是“连续三个灯泡亮的时间间隔不超过 60”。排序后，灯泡已经按时间排好，只要看相邻的三盏灯就行了。

#### 代码（Python）

```python
from typing import List, Dict

def alertNames(keyName: List[str], keyTime: List[str]) -> List[str]:
    # 1. 建立哈希表：name -> 所有刷卡的分钟数列表
    records: Dict[str, List[int]] = {}
    for name, t in zip(keyName, keyTime):
        minutes = int(t[:2]) * 60 + int(t[3:])   # "HH:MM" → 总分钟数
        records.setdefault(name, []).append(minutes)

    alert_set = set()   # 用集合自动去重

    # 2. 对每个人的时间列表排序 + 滑动窗口检查
    for name, times in records.items():
        times.sort()                     # 升序排列
        # 如果次数少于 3，直接跳过
        for i in range(len(times) - 2):
            # 检查窗口最左和最右的时间差是否 ≤ 60 分钟
            if times[i + 2] - times[i] <= 60:
                alert_set.add(name)
                break   # 已经满足条件，后面不必继续检查

    # 3. 返回字典序排序的结果
    return sorted(alert_set)
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - `n` 为总记录数。我们遍历一次把时间放进哈希表是 `O(n)`。  
  - 对每个人的时间列表排序，所有列表的长度之和仍是 `n`，所以整体排序成本是 `O(n log n)`（最坏情况所有记录都属于同一个人）。  
  - 滑动窗口的遍历是线性的 `O(n)`。  
  - 与暴力解的 `O(n³)` 相比，`log n` 只是一点点增长，几乎可以在 10⁵ 条数据下毫秒级完成。

- **空间复杂度**：`O(n)`  
  - 需要存储哈希表中每个人的所有时间（总共 `n` 个整数）以及结果集合，和输入规模同阶。

---

## 心得

- **核心技巧**：先**分组**（哈希表），再**排序**并用**滑动窗口**检查固定长度子序列的时间差。  
- **适用的题型**  
  1. “在固定窗口长度内出现 K 次” 类问题（例如“最近 K 次登录的时间差”）。  
  2. “子数组/子序列满足某种区间约束” 的滑动窗口题目（如 LeetCode 239. Sliding Window Maximum）。  
  3. “同一属性的多次出现频率” 检测（例如异常登录、频繁操作监控）。  
- **一句话总结解题钥匙**：**“先把同类数据聚在一起，排好序后只看相邻的窗口”**。

---

## 反思

- **第一反应**：看到“同一个人三次刷卡在一小时内”，立刻想到**枚举三元组**检查时间差。  
- **最容易踩的坑**  
  1. **时间跨天**：本题限定在同一天内，直接把 `"HH:MM"` 转成分钟即可；如果跨天需要额外处理。  
  2. **时间等于 60 分钟的边界**：`"10:00"` 与 `"11:00"` 视为合法，需要使用 `≤ 60` 而不是 `< 60`。  
  3. **重复记录**：题目保证 `[name, time]` 唯一，但如果出现重复，需要去重或使用集合。  
- **下次遇到同类题**：第一步先**把相同属性的记录收集到一起**（哈希表），**排序**后用**固定长度滑动窗口**判断是否满足时间/数值区间条件。这样可以把指数级暴力搜索直接降到 `O(n log n)`。