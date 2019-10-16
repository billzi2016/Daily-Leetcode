# #621. 任务调度器 / Task Scheduler

> 难度：中等 · 标签：Array、Hash Table、Greedy、Sorting、Heap (Priority Queue)、Counting · [LeetCode 链接](https://leetcode.com/problems/task-scheduler/)

---

## 题目（英文原版）

**Description**

You are given an array of CPU tasks, each labeled with a letter from A to Z, and a number n. Each CPU interval can be idle or allow the completion of one task. Tasks can be completed in any order, but there's a constraint: there has to be a gap of at least n intervals between two tasks with the same label.
Return the minimum number of CPU intervals required to complete all tasks.

**Examples**

**Example 1:**

```
Input: tasks = ["A","A","A","B","B","B"], n = 2
Output: 8
Explanation: A possible sequence is: A -> B -> idle -> A -> B -> idle -> A -> B.
After completing task A, you must wait two intervals before doing A again. The same applies to task B. In the 3 rd interval, neither A nor B can be done, so you idle. By the 4 th interval, you can do A again as 2 intervals have passed.
```

**Example 2:**

```
Input: tasks = ["A","C","A","B","D","B"], n = 1
Output: 6
Explanation: A possible sequence is: A -> B -> C -> D -> A -> B.
With a cooling interval of 1, you can repeat a task after just one other task.
```

**Example 3:**

```
Input: tasks = ["A","A","A", "B","B","B"], n = 3
Output: 10
Explanation: A possible sequence is: A -> B -> idle -> idle -> A -> B -> idle -> idle -> A -> B.
There are only two types of tasks, A and B, which need to be separated by 3 intervals. This leads to idling twice between repetitions of these tasks.
```

**Constraints**

- 1 <= tasks.length <= 104
- tasks[i] is an uppercase English letter.
- 0 <= n <= 100

---

## 题目（中文翻译）

**描述**  
给定一个由字母 A 到 Z 标记的 CPU 任务（CPU tasks）数组 `tasks`，以及一个整数 `n`。CPU 的每个时间间隔（interval）可以执行一个任务或保持空闲（idle）。任务可以以任意顺序完成，但必须满足以下约束：同一标签的两次任务之间必须间隔至少 `n` 个时间间隔。返回完成所有任务所需的最少时间间隔数。

**示例**  

**示例 1**  
输入: `tasks = ["A","A","A","B","B","B"], n = 2`  
输出: `8`  
解释: 一种可能的执行序列为: `A -> B -> idle -> A -> B -> idle -> A -> B`。  
完成任务 A 后，需要等待两个时间间隔才能再次执行 A，任务 B 同理。在第 3 个时间间隔，既不能执行 A 也不能执行 B，只能空闲。到了第 4 个时间间隔，已经过去 2 个间隔，可以再次执行 A。

**示例 2**  
输入: `tasks = ["A","C","A","B","D","B"], n = 1`  
输出: `6`  
解释: 一种可能的执行序列为: `A -> B -> C -> D -> A -> B`。  
冷却时间间隔（cooling interval）为 1 时，只需在两个相同任务之间插入一个其他任务即可。

**示例 3**  
输入: `tasks = ["A","A","A","B","B","B"], n = 3`  
输出: `10`  
解释: 一种可能的执行序列为: `A -> B -> idle -> idle -> A -> B -> idle -> idle -> A -> B`。  
只有两类任务 A 和 B，需要相隔 3 个时间间隔，这导致在两次相同任务之间需要出现两次空闲。

**约束条件**  
- `1 <= tasks.length <= 10^4`  
- `tasks[i]` 为大写英文字母。  
- `0 <= n <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把所有任务的执行顺序全部列举出来，挑一个满足“相同字母之间至少间隔 `n` 个时间片”的排列，然后数一下需要多少个时间片（包括可能的 `idle` 空闲）。  

- **数据结构**：我们可以用一个列表 `order` 来存放当前尝试的执行顺序。  
- **生活化类比**：把任务看成排队买饭的顾客，`order` 就是排队的顺序。我们要检查的是，同一种顾客（同一字母）之间是否至少隔了 `n` 个人。  
- **正确性**：只要遍历到的每一种排列都满足间隔要求，那么它的长度（包括空闲）就是一种合法的调度方案。最短的合法长度就是答案。  

显然，这种“枚举所有排列”的做法在最坏情况下会尝试 `tasks.length!` 种可能，远远超出计算能力，但它帮助我们理清了问题：**关键在于如何尽量让任务紧凑地排在一起，避免产生多余的空闲**。

#### 代码（Python）

```python
import itertools

def leastInterval_bruteforce(tasks, n):
    # 统计所有可能的排列（会非常慢，仅作演示）
    min_time = float('inf')
    for perm in set(itertools.permutations(tasks)):
        time = 0               # 已经用了多少时间片
        last_pos = {}          # 记录每个字母上一次出现的时间片
        for t in perm:
            # 如果该任务上一次出现的时间片距离现在不足 n，就需要插入 idle
            if t in last_pos and time - last_pos[t] - 1 < n:
                # 需要的 idle 数 = n - (已经间隔的时间片数)
                idle = n - (time - last_pos[t] - 1)
                time += idle     # 插入 idle
            # 执行当前任务
            time += 1
            last_pos[t] = time - 1   # 更新该任务的最近执行时间片
        min_time = min(min_time, time)
    return min_time
```

> **注意**：上述代码仅用于说明思路，`itertools.permutations` 在 `tasks` 长度稍大时会爆炸，实际提交会 TLE（超时）。

#### 复杂度  

- **时间复杂度**：`O(k!)`（`k = len(tasks)`），因为要遍历所有排列。可以把 `O(k!)` 想象成“把所有书本的排法全都列出来”，即使只有 10 本书，也要检查 3,628,800 种排法，显然不可行。  
- **空间复杂度**：`O(k)`，只需要保存当前排列和几个辅助变量。

---

### 2. 最优解

#### 思路  

从暴力解我们知道：**关键是让“高频任务”尽可能均匀分布**，这样可以最小化 idle 的出现。下面一步步推导出一种贪心（greedy）策略：

1. **统计每种任务出现的次数**  
   把任务看成字典（哈希表），`key` 是任务字母，`value` 是出现次数。就像查字典时，词是 `key`，对应的页码是 `value`。

2. **找出出现次数最多的任务**  
   假设出现最多的任务出现了 `max_freq` 次。为了让这类任务之间的间隔达到 `n`，我们必须在它们之间插入 **其它任务或 idle**，形成若干“循环”。  
   每个循环的长度 = `n + 1`（因为一次执行任务后，需要 `n` 个空位才能再次执行同类任务）。  
   例如 `n = 2`，循环形如 `[A, _, _]`，这里的下划线可以放别的任务或 idle。

3. **计算最少需要的时间片**  
   - 如果 **只考虑最高频任务**，我们得到的基准长度是  
     `part_count = max_freq - 1`（循环的数量，最后一次不需要后面的空位）  
     `part_length = n + 1`（每个循环的长度）  
     `empty_slots = part_count * (part_length - 1)`（除去最高频任务本身外，需要填充的空位数）  
   - 把 **其余任务的数量** 填进这些空位。若任务数量足够填满所有空位，则不需要 idle，答案就是任务总数 `len(tasks)`。  
   - 否则，仍有空位未被占用，这些空位只能是 idle，答案就是 `len(tasks) + idle`，也可以写成  
     `max(len(tasks), (max_freq - 1) * (n + 1) + num_max)`  
     其中 `num_max` 是出现次数等于 `max_freq` 的任务种类数（可能有多个任务并列最高频）。

4. **为什么贪心是最优的？**  
   - 最高频任务决定了最紧凑的排列方式，因为它们最多、最难分散。  
   - 只要把其它任务尽可能填进最高频任务之间的空位，就不会产生多余的 idle。  
   - 任何把最高频任务放得更紧的安排都会违反间隔限制，任何把它们放得更松的安排只会增加 idle，所以上述计算得到的长度一定是最小的。

5. **实现细节**  
   - 计数可以用长度为 26 的数组（因为只涉及大写字母）或 `collections.Counter`。  
   - 找到 `max_freq` 与 `num_max` 只需要一次遍历。  

#### 代码（Python）

```python
from collections import Counter

def leastInterval(tasks, n):
    """
    返回完成所有任务所需的最少时间片数（包括 idle）。
    """
    if n == 0:                     # 没有冷却时间，直接按任务数返回
        return len(tasks)

    # 1. 统计每个任务出现的次数
    task_counts = Counter(tasks)   # 类似于查字典，key 是任务字母，value 是出现次数

    # 2. 找到出现次数的最大值以及有多少种任务达到这个最大值
    max_freq = max(task_counts.values())          # 最多出现的次数
    num_max = sum(1 for cnt in task_counts.values() if cnt == max_freq)  # 并列最高频的种类数

    # 3. 计算理论上的最小长度
    #    (max_freq - 1) 表示除了最后一次出现之外，需要多少个完整的“循环”
    part_count = max_freq - 1
    #    每个循环的长度是 n + 1（任务本身 + n 个间隔），但其中已经放了一个最高频任务
    part_length = n + 1
    #    空位总数 = 循环数 * (循环长度 - 1)（减去已经占用的最高频任务）
    empty_slots = part_count * (part_length - 1)
    #    其余任务的总数（不包括最高频任务本身）
    available_tasks = len(tasks) - max_freq * num_max
    #    需要的 idle = max(0, empty_slots - available_tasks)
    idle = max(0, empty_slots - available_tasks)

    # 4. 总时间片 = 任务数 + idle
    return len(tasks) + idle
```

> **代码解释**  
> - 第 1 行的 `if n == 0` 相当于说“如果不需要间隔，直接一个接一个执行即可”。  
> - `Counter` 把任务列表转成 “字典”，类似于查字典时把词对应到页码。  
> - `max_freq` 是“最高频任务的出现次数”，就像我们先挑出最常见的字母。  
> - `num_max` 统计有多少种字母的出现次数和 `max_freq` 相同（可能有并列）。  
> - `empty_slots` 代表“我们必须预留的空位”，如果其它任务填不满这些空位，就只能用 `idle`（空闲）来填。

#### 复杂度  

- **时间复杂度**：`O(m)`，其中 `m = len(tasks)`（最多 10⁴），因为只遍历一次任务列表并做常数次统计。相比暴力的 `O(m!)`，这就像把“把所有书排好再检查”简化成“只看每本书出现几次”。  
- **空间复杂度**：`O(1)`（常数空间），因为计数数组或 `Counter` 最多存 26 个字母的信息，和任务数量无关。

---

## 心得

- **核心技巧**：利用任务出现频率构造“循环”，把最高频任务决定的框架当作基准，再把其余任务填进去——这是一种典型的**贪心 + 计数**思路。  
- **适用的题型**：  
  1. **Task Scheduler**（本题）  
  2. **Rearrange String k Distance Apart**（要求相同字符间隔至少 k）  
  3. **Maximum Points You Can Obtain from Cards**（需要先统计出现次数再贪心取最大）  
- **一句话总结解题钥匙**：**先把最“难安放”的任务（最高频）铺成骨架，其余任务尽可能填进骨架的空位**。

---

## 反思

- **第一反应**：看到“相同任务间必须间隔 n”，自然想到“把相同字母的出现时间间隔拉开”，于是想到暴力枚举所有排列。  
- **最容易踩的坑**：  
  - 忽略 **并列最高频任务** 的情况，导致公式缺少 `num_max`，在出现多个最高频字母时会算错。  
  - `n = 0` 时直接返回任务数，否则会错误地加上多余的 idle。  
  - 计算空位时忘记减去已经放进的最高频任务本身。  
- **下次类似题的第一步**：先 **统计每种元素出现的次数**，找出出现最多的元素（或并列最多的），再围绕它们构造最紧凑的排列框架。这样就能快速定位问题的“瓶颈”，并据此设计贪心或数学公式求解。