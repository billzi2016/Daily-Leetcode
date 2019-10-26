# #636. **函数的独占时间** / Exclusive Time of Functions

> 难度：中等 · 标签：Array、Stack · [LeetCode 链接](https://leetcode.com/problems/exclusive-time-of-functions/)

---

## 题目（英文原版）

**Description**

On a single-threaded CPU, we execute a program containing n functions. Each function has a unique ID between 0 and n-1.
Function calls are stored in a call stack: when a function call starts, its ID is pushed onto the stack, and when a function call ends, its ID is popped off the stack. The function whose ID is at the top of the stack is the current function being executed. Each time a function starts or ends, we write a log with the ID, whether it started or ended, and the timestamp.
You are given a list logs, where logs[i] represents the ith log message formatted as a string "{function_id}:{"start" | "end"}:{timestamp}". For example, "0:start:3" means a function call with function ID 0 started at the beginning of timestamp 3, and "1:end:2" means a function call with function ID 1 ended at the end of timestamp 2. Note that a function can be called multiple times, possibly recursively.
A function's exclusive time is the sum of execution times for all function calls in the program. For example, if a function is called twice, one call executing for 2 time units and another call executing for 1 time unit, the exclusive time is 2 + 1 = 3.
Return the exclusive time of each function in an array, where the value at the ith index represents the exclusive time for the function with ID i.

**Examples**

**Example 1:**

```
Input: n = 2, logs = ["0:start:0","1:start:2","1:end:5","0:end:6"]
Output: [3,4]
Explanation:
Function 0 starts at the beginning of time 0, then it executes 2 for units of time and reaches the end of time 1.
Function 1 starts at the beginning of time 2, executes for 4 units of time, and ends at the end of time 5.
Function 0 resumes execution at the beginning of time 6 and executes for 1 unit of time.
So function 0 spends 2 + 1 = 3 units of total time executing, and function 1 spends 4 units of total time executing.
```

**Example 2:**

```
Input: n = 1, logs = ["0:start:0","0:start:2","0:end:5","0:start:6","0:end:6","0:end:7"]
Output: [8]
Explanation:
Function 0 starts at the beginning of time 0, executes for 2 units of time, and recursively calls itself.
Function 0 (recursive call) starts at the beginning of time 2 and executes for 4 units of time.
Function 0 (initial call) resumes execution then immediately calls itself again.
Function 0 (2nd recursive call) starts at the beginning of time 6 and executes for 1 unit of time.
Function 0 (initial call) resumes execution at the beginning of time 7 and executes for 1 unit of time.
So function 0 spends 2 + 4 + 1 + 1 = 8 units of total time executing.
```

**Example 3:**

```
Input: n = 2, logs = ["0:start:0","0:start:2","0:end:5","1:start:6","1:end:6","0:end:7"]
Output: [7,1]
Explanation:
Function 0 starts at the beginning of time 0, executes for 2 units of time, and recursively calls itself.
Function 0 (recursive call) starts at the beginning of time 2 and executes for 4 units of time.
Function 0 (initial call) resumes execution then immediately calls function 1.
Function 1 starts at the beginning of time 6, executes 1 unit of time, and ends at the end of time 6.
Function 0 resumes execution at the beginning of time 6 and executes for 2 units of time.
So function 0 spends 2 + 4 + 1 = 7 units of total time executing, and function 1 spends 1 unit of total time executing.
```

**Constraints**

- 1 <= n <= 100
- 2 <= logs.length <= 500
- 0 <= function_id < n
- 0 <= timestamp <= 109
- No two start events will happen at the same timestamp.
- No two end events will happen at the same timestamp.
- Each function has an "end" log for each "start" log.

---

## 题目（中文翻译）

在单线程 CPU 上执行一个包含 `n` 个函数的程序。每个函数的 ID 在 `0` 到 `n-1` 之间唯一。  
函数调用使用调用栈（call stack）记录：函数调用开始时，其 ID 被压入栈顶；函数调用结束时，其 ID 从栈顶弹出。栈顶的 ID 表示当前正在执行的函数。每当函数开始或结束时，都会记录一条日志，日志内容包括函数 ID、是开始还是结束以及时间戳。

给定一个字符串数组 `logs`，其中 `logs[i]` 表示第 `i` 条日志，格式为 `"{function_id}:{"start" | "end"}:{timestamp}"`。例如，`"0:start:3"` 表示函数 ID 为 `0` 的调用在时间戳 `3` 的起始时刻开始；`"1:end:2"` 表示函数 ID 为 `1` 的调用在时间戳 `2` 的结束时刻结束。注意，函数可以被多次调用，甚至递归调用。

函数的独占时间（exclusive time）是该函数所有调用的执行时间之和。例如，若一个函数被调用两次，第一次执行 2 个时间单位，第二次执行 1 个时间单位，则其独占时间为 `2 + 1 = 3`。

返回一个数组，其中第 `i` 个元素表示函数 ID 为 `i` 的独占时间。

---

### 示例

**示例 1**  
```text
Input: n = 2, logs = ["0:start:0","1:start:2","1:end:5","0:end:6"]
Output: [3,4]
Explanation:
函数 0 在时间 0 的起始时刻开始执行，随后执行 2 个时间单位，到达时间 1 的结束时刻。
函数 1 在时间 2 的起始时刻开始执行，执行 4 个时间单位，在时间 5 的结束时刻结束。
函数 0 在时间 6 的起始时刻恢复执行，执行 1 个时间单位。
因此函数 0 的总执行时间为 2 + 1 = 3，函数 1 的总执行时间为 4。
```

**示例 2**  
```text
Input: n = 1, logs = ["0:start:0","0:start:2","0:end:5","0:start:6","0:end:6","0:end:7"]
Output: [8]
Explanation:
函数 0 在时间 0 的起始时刻开始执行，执行 2 个时间单位后递归调用自身。
递归调用（函数 0）在时间 2 的起始时刻开始，执行 4 个时间单位。
初始调用在递归调用结束后恢复执行，随后立即再次调用自身。
第二次递归调用在时间 6 的起始时刻开始，执行 1 个时间单位。
初始调用在时间 7 的起始时刻恢复执行，执行 1 个时间单位。
所以函数 0 的总执行时间为 2 + 4 + 1 + 1 = 8。
```

**示例 3**  
```text
Input: n = 2, logs = ["0:start:0","0:start:2","0:end:5","1:start:6","1:end:6","0:end:7"]
Output: [7,1]
Explanation:
函数 0 在时间 0 的起始时刻开始执行，执行 2 个时间单位后递归调用自身。
递归调用（函数 0）在时间 2 的起始时刻开始，执行 4 个时间单位。
初始调用在递归调用结束后恢复执行，随后立即调用函数 1。
函数 1 在时间 6 的起始时刻开始，执行 1 个时间单位，在同一时间的结束时刻结束。
函数 0 在时间 6 的起始时刻恢复执行，执行 2 个时间单位。
因此函数 0 的总执行时间为 2 + 4 + 1 = 7，函数 1 的总执行时间为 1。
```

---

### 约束条件

- `1 <= n <= 100`
- `2 <= logs.length <= 500`
- `0 <= function_id < n`
- `0 <= timestamp <= 10^9`
- 不会有两个 **start** 事件发生在同一时间戳。
- 不会有两个 **end** 事件发生在同一时间戳。
- 每个 **start** 日志都有对应的 **end** 日志。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有日志顺序遍历一遍，记录每个函数的运行区间，然后把这些区间相互减去子函数的时间**。  
可以把每一次 `"start"` 当作一次“打开的盒子”，对应的 `"end"` 当作“关闭的盒子”。  
如果我们把每个函数的所有 **（开始时间，结束时间）** 区间收集起来，再对同一个函数的多个区间求和，就得到它的**总执行时间**。  
但是，这样会把**子函数占用的时间也算进去**，于是需要再把子函数的时间从父函数的区间里减掉——这一步如果用嵌套的循环去查找子区间，就会产生 **O(n²)** 的时间复杂度。

> **类比**：把日志想象成一本日记，里面写着“我（函数）什么时候开始工作，什么时候结束”。我们先把每个人的工作时段都列出来，然后再把“被别人抢走的时间”剔除掉。

#### 代码（Python）

```python
from typing import List

def exclusiveTime_bruteforce(n: int, logs: List[str]) -> List[int]:
    # 1. 把每条日志解析成 (id, type, timestamp)
    parsed = []
    for log in logs:
        fid, typ, ts = log.split(':')
        parsed.append((int(fid), typ, int(ts)))

    # 2. 用栈模拟调用关系，收集每一次函数的 (start, end) 区间
    intervals = [[] for _ in range(n)]          # intervals[i] 保存函数 i 的所有区间
    stack = []                                   # 栈中保存 (function_id, start_time)
    for fid, typ, ts in parsed:
        if typ == 'start':
            stack.append((fid, ts))              # 进入新函数
        else:  # 'end'
            last_fid, start_ts = stack.pop()     # 当前函数结束
            intervals[last_fid].append((start_ts, ts))

    # 3. 对每个函数，先把所有区间长度相加，再减去子函数占用的时间（暴力遍历）
    res = [0] * n
    for i in range(n):
        total = 0
        # 先把自己的所有区间长度相加
        for s, e in intervals[i]:
            total += e - s + 1    # 包含结束时刻本身

        # 再遍历所有其它函数的区间，找出完全被 i 包含的子区间并减去
        for j in range(n):
            if i == j:
                continue
            for s, e in intervals[j]:
                # 子区间必须完全在父区间内部
                # 这里用暴力检查所有可能的父区间
                for ps, pe in intervals[i]:
                    if ps <= s and e <= pe:
                        total -= e - s + 1
                        break
        res[i] = total
    return res
```

#### 复杂度  

- **时间复杂度**：`O(m * n²)`（`m` 为日志条数，`n` 为函数数量）。  
  解释：我们先遍历日志一次 O(m)；随后对每个函数的每个子函数区间都要去检查是否被父区间覆盖，最坏情况是 `n` 个函数各自有 `O(m)` 区间，导致两层循环产生二次方的检查。  
- **空间复杂度**：`O(m + n)`。  
  解释：需要存放解析后的日志（O(m)）以及每个函数的区间列表（最多 O(m)）和栈（深度不超过 `n`）。

> 虽然思路直观，但大量的嵌套循环在数据稍大时会明显卡顿，这就是我们要寻找更优解的动机。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于重复遍历子函数区间**。  
实际上，**调用栈本身已经帮我们把“父子关系”即时维护好了**，只要在遍历日志的同时把时间分配给当前栈顶的函数，就能直接得到每个函数的独占时间，根本不需要二次遍历。

关键点如下：

1. **使用栈**：栈顶始终是当前正在执行的函数。  
2. **记录上一次的时间戳**：`prev_time` 表示上一条日志处理完后 CPU 正在的时间点。  
3. **遇到 `start`**：  
   - 栈顶函数（如果有）在 `prev_time` 到 `cur_time-1` 这段时间里一直在执行，它的独占时间要加上 `cur_time - prev_time`。  
   - 将新的函数压入栈，更新 `prev_time = cur_time`。  
4. **遇到 `end`**：  
   - 栈顶函数在 `prev_time` 到 `cur_time`（包括结束时刻）这段时间里执行，独占时间加上 `cur_time - prev_time + 1`。  
   - 弹出栈顶函数，更新 `prev_time = cur_time + 1`（因为结束时刻已经被消耗，下一段时间从 `cur_time+1` 开始）。  

这样每条日志只处理一次，时间分配在 **O(1)** 的操作里完成，整体 **O(m)**。

> **类比**：把 CPU 想成一个厨房，**锅**（栈）里放的菜（函数）只能一个接一个地烹饪。每次有新菜要下锅（`start`），老菜先停一下，把已经烹饪的时间记下来；菜做好（`end`）后，把这段时间记给它，然后把锅里的老菜继续烹饪。

#### 代码（Python）

```python
from typing import List

def exclusiveTime(n: int, logs: List[str]) -> List[int]:
    """
    栈模拟函数调用，逐条日志分配独占时间
    """
    res = [0] * n               # 结果数组，保存每个函数的独占时间
    stack = []                  # 栈，保存正在执行的函数 id
    prev_time = 0               # 上一条日志处理完后 CPU 所在的时间点

    for log in logs:
        fid_str, typ, ts_str = log.split(':')
        fid = int(fid_str)
        cur_time = int(ts_str)

        if typ == 'start':
            # 如果栈不为空，栈顶函数在 prev_time ~ cur_time-1 这段时间里独占运行
            if stack:
                running = stack[-1]
                res[running] += cur_time - prev_time
            # 当前函数开始执行，压入栈
            stack.append(fid)
            prev_time = cur_time          # 下一个时间段从 cur_time 开始
        else:  # typ == 'end'
            # 栈顶函数结束，执行时间包括结束时刻本身
            running = stack.pop()
            res[running] += cur_time - prev_time + 1
            prev_time = cur_time + 1      # 下一段时间从 cur_time+1 开始

    return res
```

#### 复杂度  

- **时间复杂度**：`O(m)`，只遍历一次日志列表，且每次栈操作、时间计算都是常数时间。  
  与暴力解相比，时间从二次方降到线性，极大提升效率。  
- **空间复杂度**：`O(n)`，栈的最大深度不超过函数数量 `n`（递归最深时），结果数组本身也是 `O(n)`。

---

## 心得

- **核心技巧**：**利用栈模拟调用栈，配合前一次时间戳进行增量计时**。  
- **适用的题型**：  
  1. 需要在“嵌套/递归”结构中分配资源或时间的题目（如 **636. 函数的独占时间**、**225. 用队列实现栈** 的思路类似）。  
  2. 需要维护“最近的未完成事件”或“最近的开启状态”的场景（如 **20. 有效的括号**、**84. 柱状图中最大的矩形** 中的单调栈）。  
- **一句话总结**：**栈 + 前一个时间点 = 逐条日志的 O(1) 时间分配**。

## 反思

- **第一反应**：看到“调用栈”和“日志顺序”，立刻想到用栈来模拟函数的嵌套关系。  
- **最容易踩的坑**：  
  - **时间计数的闭区间/开区间**：`start` 事件的时间点是 **包括** 的，而 `end` 事件的时间点同样要算进函数的执行时间，需要在结束时加 `+1`。  
  - **更新 `prev_time` 的细节**：结束后要设为 `cur_time + 1`，否则下一个函数会把已经算过的时间重复计入。  
  - **空栈检查**：在 `start` 时若栈为空，别忘了直接压入新函数，不要尝试给“不存在的父函数”加时间。  
- **下次遇到同类题**：第一步先 **画出调用栈的变化**，确认每一次 `start`、`end` 对时间的增量贡献，然后决定是否可以用 **栈 + 前一个时间戳** 的方式一次遍历完成。