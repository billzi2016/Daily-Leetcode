# #2432. 完成最长任务的员工 / The Employee That Worked on the Longest Task

> 难度：简单 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/the-employee-that-worked-on-the-longest-task/)

---

## 题目（英文原版）

**Description**

There are n employees, each with a unique id from 0 to n - 1.
You are given a 2D integer array logs where logs[i] = [idi, leaveTimei] where:
Note that the ith task starts the moment right after the (i - 1)th task ends, and the 0th task starts at time 0.
Return the id of the employee that worked the task with the longest time. If there is a tie between two or more employees, return the smallest id among them.

**Examples**

**Example 1:**

```
Input: n = 10, logs = [[0,3],[2,5],[0,9],[1,15]]
Output: 1
Explanation: 
Task 0 started at 0 and ended at 3 with 3 units of times.
Task 1 started at 3 and ended at 5 with 2 units of times.
Task 2 started at 5 and ended at 9 with 4 units of times.
Task 3 started at 9 and ended at 15 with 6 units of times.
The task with the longest time is task 3 and the employee with id 1 is the one that worked on it, so we return 1.
```

**Example 2:**

```
Input: n = 26, logs = [[1,1],[3,7],[2,12],[7,17]]
Output: 3
Explanation: 
Task 0 started at 0 and ended at 1 with 1 unit of times.
Task 1 started at 1 and ended at 7 with 6 units of times.
Task 2 started at 7 and ended at 12 with 5 units of times.
Task 3 started at 12 and ended at 17 with 5 units of times.
The tasks with the longest time is task 1. The employee that worked on it is 3, so we return 3.
```

**Example 3:**

```
Input: n = 2, logs = [[0,10],[1,20]]
Output: 0
Explanation: 
Task 0 started at 0 and ended at 10 with 10 units of times.
Task 1 started at 10 and ended at 20 with 10 units of times.
The tasks with the longest time are tasks 0 and 1. The employees that worked on them are 0 and 1, so we return the smallest id 0.
```

**Constraints**

- 2 <= n <= 500
- 1 <= logs.length <= 500
- logs[i].length == 2
- 0 <= idi <= n - 1
- 1 <= leaveTimei <= 500
- idi != idi+1
- leaveTimei are sorted in a strictly increasing order.

---

## 题目（中文翻译）

**题目描述**  
有 `n` 名员工，员工编号为 `0` 到 `n - 1`（唯一）。  
给定一个二维整数数组 `logs`，其中 `logs[i] = [idi, leaveTimei]`，表示第 `i` 个任务的结束信息：

- `idi` 为完成第 `i` 个任务的员工的编号  
- `leaveTimei` 为第 `i` 个任务结束的时间点  

注意，第 `i` 个任务在第 `i‑1` 个任务结束的瞬间立即开始，而第 `0` 个任务在时间 `0` 开始。

返回完成 **耗时最长** 任务的员工编号。如果有多个员工的任务耗时相同，返回编号最小的员工。

---

**示例 1**  
```
Input: n = 10, logs = [[0,3],[2,5],[0,9],[1,15]]
Output: 1
Explanation: 
Task 0 started at 0 and ended at 3 with 3 units of times.
Task 1 started at 3 and ended at 5 with 2 units of times.
Task 2 started at 5 and ended at 9 with 4 units of times.
Task 3 started at 9 and ended at 15 with 6 units of times.
The task with the longest time is task 3 and the employee with id 1 is the one that worked on it, so we return 1.
```

**示例 2**  
```
Input: n = 26, logs = [[1,1],[3,7],[2,12],[7,17]]
Output: 3
Explanation: 
Task 0 started at 0 and ended at 1 with 1 unit of times.
Task 1 started at 1 and ended at 7 with 6 units of times.
Task 2 started at 7 and ended at 12 with 5 units of times.
Task 3 started at 12 and ended at 17 with 5 units of times.
The task with the longest time is task 1. The employee that worked on it is 3, so we return 3.
```

**示例 3**  
```
Input: n = 2, logs = [[0,10],[1,20]]
Output: 0
Explanation: 
Task 0 started at 0 and ended at 10 with 10 units of times.
Task 1 started at 10 and ended at 20 with 10 units of times.
The tasks with the longest time are tasks 0 and 1. The employees that worked on them are 0 and 1, so we return the smallest id 0.
```

**约束条件**  

- `2 <= n <= 500`
- `1 <= logs.length <= 500`
- `logs[i].length == 2`
- `0 <= idi <= n - 1`
- `1 <= leaveTimei <= 500`
- `idi != idi+1`（相邻任务的员工编号不同）
- `leaveTimei` 严格递增（已按时间顺序排序）

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：  
1. **逐个任务计算耗时**。第 `i` 个任务的结束时间是 `logs[i][1]`，它的开始时间就是前一个任务的结束时间（第 0 个任务的开始时间是 0）。所以任务耗时 = `leaveTime[i] - leaveTime[i‑1]`（对第 0 个任务来说是 `leaveTime[0] - 0`）。  
2. **把每个员工的所有任务耗时都记下来**。可以用一个 **哈希表（字典）**，把 `employee_id` 当作键（key），对应的值（value）是该员工出现过的最大任务耗时。字典就像一本“查字典”，我们给它一个词（员工 id），它会告诉我们对应的页码（该员工的最长任务时间）。  
3. **遍历完所有任务后，找出最长的那段时间对应的员工**。如果有多个员工的最长任务时间相同，返回 id 最小的即可。  

为什么这个方法一定能得到正确答案？  
- 每个任务的耗时都被准确算出来，且没有遗漏。  
- 对每个员工我们只保留**最大**的那段耗时，这正是题目要求比较的对象。  
- 最后再一次遍历字典取最大值（若相等取最小 id），自然得到答案。  

**时间/空间复杂度的大白话解释**  
- `O(m)` 的时间复杂度（`m = logs.length`），意思是“我们要看一遍所有任务，一次遍历就够了”。  
- `O(k)` 的空间复杂度（`k = n`，员工数量），意思是“我们需要为每个员工准备一个小抽屉来放它的最长任务时间”。  

#### 代码（Python）

```python
def longestTask(n: int, logs: list[list[int]]) -> int:
    # 用字典记录每个员工的最长任务耗时
    # key: employee id, value: longest duration this employee has done
    longest = {}

    prev_leave = 0                     # 前一个任务的结束时间，初始为 0（第 0 件任务的开始时间）
    for emp_id, leave in logs:         # 逐个读取日志
        duration = leave - prev_leave  # 计算当前任务的耗时
        # 更新该员工的最长耗时（如果还没有记录，就直接写入）
        if emp_id not in longest or duration > longest[emp_id]:
            longest[emp_id] = duration
        prev_leave = leave              # 为下一次循环准备新的“前一个结束时间”

    # 在所有员工中找出最长的任务时间，若相等取 id 最小的
    answer_id = -1
    max_duration = -1
    for emp_id, dur in longest.items():
        if dur > max_duration or (dur == max_duration and emp_id < answer_id):
            max_duration = dur
            answer_id = emp_id

    return answer_id
```

#### 复杂度  

- **时间复杂度**：`O(m)`（`m` 为日志条数），只遍历一次日志，再遍历一次字典，都是线性时间。  
- **空间复杂度**：`O(k)`（`k` 为员工数），需要为每位出现过的员工保存一个整数。  

---  

### 2. 最优解  

#### 思路  

从暴力解出发，**慢点**其实只有两处：  
1. 使用字典保存每位员工的最长任务时间，随后还要再遍历一次字典找最大值。  
2. 对每个日志都要做一次 `if emp_id not in longest …` 的查找。  

其实我们可以在一次遍历 **同时** 完成这两件事：  
- 维护**全局的最长任务时间** `max_duration`，以及对应的员工 `ans_id`。  
- 当遍历到当前任务时，直接比较 `duration` 与 `max_duration`：  
  - 若更大，则更新 `max_duration` 并把 `ans_id` 设为当前 `emp_id`。  
  - 若相等且 `emp_id` 更小，也要更新 `ans_id`（因为题目要求最小 id）。  

这样就不需要额外的字典，也不需要第二遍遍历，**一次遍历即可得到答案**。  

核心技巧是**边遍历边维护最值**，这在很多“找最大/最小”类型的问题里都非常有用。可以把它想象成在跑步比赛时，裁判员站在赛道旁边，随时记录当前最快的选手，而不是等比赛结束后再去统计。  

#### 代码（Python）

```python
def longestTask(n: int, logs: list[list[int]]) -> int:
    max_duration = -1   # 记录目前发现的最长任务耗时
    ans_id = -1         # 记录对应的员工 id

    prev_leave = 0      # 前一个任务的结束时间，初始化为 0

    for emp_id, leave in logs:
        duration = leave - prev_leave   # 当前任务的耗时

        # 更新全局最长时间以及对应的员工 id
        if duration > max_duration or (duration == max_duration and emp_id < ans_id):
            max_duration = duration
            ans_id = emp_id

        prev_leave = leave              # 为下一次循环准备新的开始时间

    return ans_id
```

#### 复杂度  

- **时间复杂度**：`O(m)`，只遍历一次日志，**没有额外的遍历或查找**，和暴力解的时间复杂度相同，但常数更小。  
- **空间复杂度**：`O(1)`，只用了固定的几个变量（不随员工数量或日志长度增长），比暴力解省了字典的空间。  

---

## 心得  

- **核心技巧**：一次遍历时实时维护全局最值（最大/最小），并在冲突时使用题目要求的 tie‑break（这里是 id 最小）。  
- **适用的题型**：  
  1. “找出出现次数最多的元素”类（如 `696. Count Binary Substrings` 中的计数）  
  2. “在数组/日志中找最长/最短区间”类（如 `209. Minimum Size Subarray Sum`）  
  3. “遍历记录最值并处理平局”类（如 `1796. Second Largest Digit`）  
- **一句话总结解题钥匙**：**“遍历时把‘最大/最小’和‘平局规则’一起写进判断里”**。  

## 反思  

- **第一反应**：看到“每个任务都有开始结束时间，求最长”，立刻想到“算每段长度”，然后再比较。  
- **最容易踩的坑**：  
  - 忘记第 0 个任务的开始时间是 0，直接用 `logs[i][0]` 计算会错。  
  - 在平局时忘记取 **最小 id**，导致返回错误的员工。  
  - 把 `leaveTime` 当作任务时长，而不是结束时间，导致算错。  
- **下次遇到同类题的第一步**：先明确“每个元素的真正值”（这里是 `duration = curLeave - prevLeave`），再决定是只需要一次遍历记录全局最值，还是需要额外的数据结构。