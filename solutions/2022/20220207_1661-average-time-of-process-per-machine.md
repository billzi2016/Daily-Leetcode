# #1661. 每台机器的平均进程时间 / Average Time of Process per Machine

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/average-time-of-process-per-machine/)

---

## 题目（英文原版）

**Description**

Table: Activity
There is a factory website that has several machines each running the same number of processes. Write a solution to find the average time each machine takes to complete a process.
The time to complete a process is the 'end' timestamp minus the 'start' timestamp. The average time is calculated by the total time to complete every process on the machine divided by the number of processes that were run.
The resulting table should have the machine_id along with the average time as processing_time, which should be rounded to 3 decimal places.
Return the result table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+----------------+---------+
| Column Name    | Type    |
+----------------+---------+
| machine_id     | int     |
| process_id     | int     |
| activity_type  | enum    |
| timestamp      | float   |
+----------------+---------+
The table shows the user activities for a factory website.
(machine_id, process_id, activity_type) is the primary key (combination of columns with unique values) of this table.
machine_id is the ID of a machine.
process_id is the ID of a process running on the machine with ID machine_id.
activity_type is an ENUM (category) of type ('start', 'end').
timestamp is a float representing the current time in seconds.
'start' means the machine starts the process at the given timestamp and 'end' means the machine ends the process at the given timestamp.
The 'start' timestamp will always be before the 'end' timestamp for every (machine_id, process_id) pair.
It is guaranteed that each (machine_id, process_id) pair has a 'start' and 'end' timestamp.
```

**Example 2:**

```
Input: 
Activity table:
+------------+------------+---------------+-----------+
| machine_id | process_id | activity_type | timestamp |
+------------+------------+---------------+-----------+
| 0          | 0          | start         | 0.712     |
| 0          | 0          | end           | 1.520     |
| 0          | 1          | start         | 3.140     |
| 0          | 1          | end           | 4.120     |
| 1          | 0          | start         | 0.550     |
| 1          | 0          | end           | 1.550     |
| 1          | 1          | start         | 0.430     |
| 1          | 1          | end           | 1.420     |
| 2          | 0          | start         | 4.100     |
| 2          | 0          | end           | 4.512     |
| 2          | 1          | start         | 2.500     |
| 2          | 1          | end           | 5.000     |
+------------+------------+---------------+-----------+
Output: 
+------------+-----------------+
| machine_id | processing_time |
+------------+-----------------+
| 0          | 0.894           |
| 1          | 0.995           |
| 2          | 1.456           |
+------------+-----------------+
Explanation: 
There are 3 machines running 2 processes each.
Machine 0's average time is ((1.520 - 0.712) + (4.120 - 3.140)) / 2 = 0.894
Machine 1's average time is ((1.550 - 0.550) + (1.420 - 0.430)) / 2 = 0.995
Machine 2's average time is ((4.512 - 4.100) + (5.000 - 2.500)) / 2 = 1.456
```

---

## 题目（中文翻译）

**描述**  
表：`Activity`  

工厂网站上有多台机器，每台机器运行相同数量的进程。编写 SQL 查询，找出每台机器完成单个进程的平均时间。  
单个进程的完成时间等于 `end` 时间戳（timestamp）减去 `start` 时间戳。平均时间的计算方式为：该机器上所有进程完成时间之和除以该机器运行的进程总数。  
查询结果应返回 `machine_id` 和平均时间，列名为 `processing_time`，并将结果四舍五入保留 3 位小数。  
返回的结果表顺序任意即可。  

**返回格式示例**  

```sql
-- 示例 1
SELECT machine_id, ROUND(AVG(end_timestamp - start_timestamp), 3) AS processing_time
FROM (
    SELECT machine_id, process_id,
           MAX(CASE WHEN activity_type = 'end'   THEN timestamp END) AS end_timestamp,
           MAX(CASE WHEN activity_type = 'start' THEN timestamp END) AS start_timestamp
    FROM Activity
    GROUP BY machine_id, process_id
) t
GROUP BY machine_id;
```

**示例**  

示例 1：

```
+------------+------------+---------------+-----------+
| machine_id | process_id | activity_type | timestamp |
+------------+------------+---------------+-----------+
| 0          | 0          | start         | 0.712     |
| 0          | 0          | end           | 1.520     |
| 0          | 1          | start         | 3.140     |
| 0          | 1          | end           | 4.001     |
| 1          | 0          | start         | 0.500     |
| 1          | 0          | end           | 1.000     |
| 1          | 1          | start         | 2.000     |
| 1          | 1          | end           | 2.800     |
+------------+------------+---------------+-----------+
```

输出：

```
+------------+-----------------+
| machine_id | processing_time |
+------------+-----------------+
| 0          | 0.834           |
| 1          | 0.650           |
+------------+-----------------+
```

**说明**  
- 对于机器 `0`，两个进程的耗时分别为 `1.520-0.712 = 0.808` 与 `4.001-3.140 = 0.861`，平均后四舍五入为 `0.834`。  
- 对于机器 `1`，两个进程的耗时分别为 `1.000-0.500 = 0.500` 与 `2.800-2.000 = 0.800`，平均后四舍五入为 `0.650`。  

约束条件  
- 表 `Activity` 中每对 `(machine_id, process_id, activity_type)` 组合唯一。  
- `activity_type` 只能取值 `'start'` 或 `'end'`。  
- `timestamp` 为浮点数，范围在 `[0, 10^9]`。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：  
1. 先把所有记录 **按机器 (machine_id) 分组**。  
2. 对每一台机器，再 **遍历它的每一个进程 (process_id)**，分别去找该进程的 `start` 时间和 `end` 时间。  
3. 用 `end - start` 得到该进程的耗时，所有进程耗时相加后除以进程数量，就得到机器的平均处理时间。

> **类比**：把 `Activity` 表想象成一本日志本。我们要为每本机器的日志本（按机器分组）找出每一条任务的“开始页”和“结束页”，再算出每条任务的页数差，最后求平均。

**为什么正确**  
- 每条记录都有明确的 `activity_type`（`start` 或 `end`），并且同一 `(machine_id, process_id)` 必定恰好出现一次 `start` 与一次 `end`（题目暗示）。
- 按照上述步骤逐条配对，必能得到每个进程的真实耗时，求平均自然得到答案。

**时间/空间复杂度**  
- 对每台机器的每个进程都要 **遍历一次完整的记录列表** 去找对应的 `start`、`end`，相当于两层循环。  
- 设表中记录条数为 `n`，则时间复杂度是 **O(n²)**（平方级别，意味着记录稍多就会慢）。  
- 只用到少量临时变量，空间复杂度是 **O(1)**（常数级别）。

#### 代码（Python）

```python
# 暴力解：两层循环逐个配对
def average_processing_time_brute(activity):
    """
    activity: List[Tuple[int, int, str, float]]
        每条记录 (machine_id, process_id, activity_type, timestamp)
    返回值: List[Tuple[int, float]]  (machine_id, 平均耗时，保留 3 位小数)
    """
    # 先找出所有机器的编号
    machines = set(row[0] for row in activity)

    result = []
    for m in machines:                     # 外层遍历每台机器
        # 收集该机器的所有进程号
        proc_ids = {row[1] for row in activity if row[0] == m}
        total_time = 0.0
        cnt = 0

        for p in proc_ids:                 # 内层遍历每个进程
            start = None
            end = None
            # 再次遍历整个表寻找对应的 start / end
            for row in activity:
                if row[0] == m and row[1] == p:
                    if row[2] == 'start':
                        start = row[3]
                    elif row[2] == 'end':
                        end = row[3]
            # 根据题意，start 与 end 必定都出现
            total_time += (end - start)
            cnt += 1

        avg = round(total_time / cnt, 3)   # 保留 3 位小数
        result.append((m, avg))

    return result
```

#### 复杂度  

- **时间复杂度：O(n²)**  
  *解释*：如果表里有 10,000 条记录，暴力解大约要做 10,000 × 10,000 = 100,000,000 次比较，明显太慢。  

- **空间复杂度：O(1)**  
  只用了几个临时变量（`set`、计数器），与输入规模无关。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈在于每次都要遍历整个表去找对应的 start / end**。  
只要我们 **一次遍历就把所有信息收集好**，后面的计算就可以在 O(1) 时间内完成。

**关键点**：使用 **哈希表（字典）** 来保存每个进程的 `start` 与 `end`，再根据机器编号累加。  
- 把 `(machine_id, process_id)` 这对键映射到一个小结构 `{'start': ?, 'end': ?}`，相当于给每个进程开一本“小账本”。  
- 同时维护另一个字典 `machine_sum` 记录每台机器的 **累计耗时**，以及 `machine_cnt` 记录 **进程数量**。  

这样只需要 **一次遍历**（O(n)）即可完成所有配对和求和。

> **类比**：把日志本一次性翻完，每翻到一页就把“开始时间”或“结束时间”写进对应任务的记事本里；记事本里信息完整后，再算每台机器的平均耗时。

#### 代码（Python）

```python
def average_processing_time_opt(activity):
    """
    使用哈希表一次遍历求平均时间
    :param activity: List[Tuple[int, int, str, float]]
    :return: List[Tuple[int, float]]
    """
    # step1：保存每个进程的 start / end 时间
    # key: (machine_id, process_id) -> {'start': float, 'end': float}
    proc_time = {}

    for machine_id, process_id, act_type, ts in activity:
        key = (machine_id, process_id)
        if key not in proc_time:
            proc_time[key] = {'start': None, 'end': None}
        proc_time[key][act_type] = ts          # 直接写入 start 或 end

    # step2：按机器累计总耗时和进程数
    machine_sum = {}   # machine_id -> total processing time
    machine_cnt = {}   # machine_id -> number of processes

    for (machine_id, _), times in proc_time.items():
        # 根据题意，start 与 end 都一定存在
        duration = times['end'] - times['start']
        machine_sum[machine_id] = machine_sum.get(machine_id, 0.0) + duration
        machine_cnt[machine_id] = machine_cnt.get(machine_id, 0) + 1

    # step3：计算平均值并保留 3 位小数
    result = []
    for m_id in machine_sum:
        avg = round(machine_sum[m_id] / machine_cnt[m_id], 3)
        result.append((m_id, avg))

    return result
```

#### 复杂度  

- **时间复杂度：O(n)**  
  只遍历一次 `activity` 表（n 条记录），每条记录的哈希操作均摊为 O(1)。  
  与暴力解的 O(n²) 相比，速度提升了 **指数级**（从平方级降到线性级）。

- **空间复杂度：O(n)**  
  需要保存每个进程的 start/end（最坏情况每条记录对应一个唯一的进程），因此使用的字典大小与输入规模线性相关。  
  对于本题的 “Easy” 规模，这完全可以接受。

---  

## 心得  

- **核心技巧**：一次遍历 + 哈希表（字典）配对。  
- **适用的题型**  
  1. “找出每对记录的差值并求聚合” —— 如 `Employee` 表的 `login` / `logout` 时间差。  
  2. “同一标识出现多次，需要配对后统计” —— 如 `Orders` 表的 `order` / `delivery` 时间。  
  3. “按键分组后计算平均/最大/最小” —— 如 `Sales` 表的每个商品的平均销量。  

- **一句话总结解题钥匙**：**把所有需要配对的信息先用字典收集好，后面只做 O(1) 的查找和累计**。

---  

## 反思  

- **第一反应**：看到 “start / end” 两种记录，就想先把它们分别放到两个列表再配对，结果是多余的遍历。  
- **最容易踩的坑**  
  - 忘记 `process_id` 只在同一台机器内部唯一，必须把 `(machine_id, process_id)` 共同作为键。  
  - 没有对 `timestamp` 做浮点数运算的精度控制，导致保留小数位时出现误差。  
  - 忽略了可能出现的 “只有 start 没有 end” 的异常情况（本题保证完整，但实际面试中要做好防御）。  
- **下次遇到同类题**：第一步先 **思考能否一次遍历把所有需要的信息收集进哈希表**，如果可以，就直接走最优路径；如果不行，再考虑多次遍历或排序等手段。