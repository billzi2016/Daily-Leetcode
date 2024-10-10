# #2895. 最小处理时间 / Minimum Processing Time

> 难度：中等 · 标签：Array、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/minimum-processing-time/)

---

## 题目（英文原版）

**Description**

You have a certain number of processors, each having 4 cores. The number of tasks to be executed is four times the number of processors. Each task must be assigned to a unique core, and each core can only be used once.
You are given an array processorTime representing the time each processor becomes available and an array tasks representing how long each task takes to complete. Return the minimum time needed to complete all tasks.

**Examples**

**Example 1:**

```
Input: processorTime = [8,10], tasks = [2,2,3,1,8,7,4,5]
Output: 16
Explanation:
Assign the tasks at indices 4, 5, 6, 7 to the first processor which becomes available at time = 8 , and the tasks at indices 0, 1, 2, 3 to the second processor which becomes available at time = 10 .
The time taken by the first processor to finish the execution of all tasks is max(8 + 8, 8 + 7, 8 + 4, 8 + 5) = 16 .
The time taken by the second processor to finish the execution of all tasks is max(10 + 2, 10 + 2, 10 + 3, 10 + 1) = 13 .
```

**Example 2:**

```
Input: processorTime = [10,20], tasks = [2,3,1,2,5,8,4,3]
Output: 23
Explanation:
Assign the tasks at indices 1, 4, 5, 6 to the first processor and the others to the second processor.
The time taken by the first processor to finish the execution of all tasks is max(10 + 3, 10 + 5, 10 + 8, 10 + 4) = 18 .
The time taken by the second processor to finish the execution of all tasks is max(20 + 2, 20 + 1, 20 + 2, 20 + 3) = 23 .
```

**Constraints**

- 1 <= n == processorTime.length <= 25000
- 1 <= tasks.length <= 105
- 0 <= processorTime[i] <= 109
- 1 <= tasks[i] <= 109
- tasks.length == 4 * n

---

## 题目（中文翻译）

你拥有若干处理器（processor），每个处理器拥有 4 个核心（core）。要执行的任务数量是处理器数量的四倍。每个任务必须分配到唯一的核心，且每个核心只能使用一次。

给定一个数组 `processorTime`，表示每个处理器可用的时间，以及一个数组 `tasks`，表示每个任务的执行时长。返回完成所有任务所需的最小时间。

**示例 1**  
**输入**  
```text
processorTime = [8,10], tasks = [2,2,3,1,8,7,4,5]
```  
**输出**  
```text
16
```  
**解释**  
将下标为 4、5、6、7 的任务分配给第一个在时间 8 可用的处理器，将下标为 0、1、2、3 的任务分配给第二个在时间 10 可用的处理器。  
第一个处理器完成所有任务的时间为 `max(8 + 8, 8 + 7, 8 + 4, 8 + 5) = 16`。

**示例 2**  
**输入**  
```text
processorTime = [10,20], tasks = [2,3,1,2,5,8,4,3]
```  
**输出**  
```text
23
```  
**解释**  
将下标为 1、4、5、6 的任务分配给第一个处理器，其余任务分配给第二个处理器。  
第一个处理器完成所有任务的时间为 `max(10 + 3, 10 + 5, 10 + 8, 10 + 4) = 18`。  
第二个处理器完成所有任务的时间为 `max(20 + 2, 20 + 1, 20 + 2, 20 + 3) = 23`。  
最终的最小完成时间为两者的最大值，即 `23`。

**约束条件**
- `1 <= n == processorTime.length <= 25000`
- `1 <= tasks.length <= 10^5`
- `0 <= processorTime[i] <= 10^9`
- `1 <= tasks[i] <= 10^9`
- `tasks.length == 4 * n`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**不动脑子**，把任务按原来的顺序直接塞进处理器：  
- 先把前 4 个任务交给第 1 台处理器，  
- 接着把第 5~8 个任务交给第 2 台，以此类推。  

这里用到的唯一数据结构是**两个数组**（`processorTime` 与 `tasks`），它们本身就像一本“任务清单”。  
- `processorTime[i]` 相当于第 i 台机器的“开工时间”，就像你去超市结账的排队时间。  
- `tasks[j]` 就是第 j 项任务需要的“加工时长”，好比每件商品的结算时间。

把任务直接按顺序分配显然可以得到一个合法的完成时间，因为每台机器恰好拿到 4 项任务，满足题目要求。  
**为什么这个方法一定能得到答案？** 因为它满足所有约束，只是没有考虑如何让最慢的那台机器尽可能早点完成。  

#### 代码（Python）

```python
def minimumProcessingTime_brutal(processorTime, tasks):
    """
    暴力（其实是最朴素的）实现：
    按原顺序把 4 个任务分给第 i 台处理器。
    """
    n = len(processorTime)               # 处理器数量
    max_finish = 0                       # 记录所有处理器中最晚的完成时间

    for i in range(n):
        # 第 i 台处理器负责的 4 个任务在 tasks 中的下标范围
        start = i * 4
        end = start + 4
        # 计算这台机器的最晚完成时间：max(开工时间 + 任务时长)
        finish_i = max(processorTime[i] + t for t in tasks[start:end])
        max_finish = max(max_finish, finish_i)

    return max_finish
```

#### 复杂度  

- **时间复杂度**：`O(m)`（`m = 4 * n`），因为只遍历了一遍 `tasks`，每个任务恰好被取一次。  
  > 大白话：如果总共有 1000 项任务，算法大约要跑 1000 步，步数随任务数量线性增长。  
- **空间复杂度**：`O(1)`，只用了常数个额外变量（不计输入数组本身）。  

> 这种解法虽然快，但往往会得到一个 **很大的** 完成时间，因为没有利用“把长任务交给早到的机器”这个直觉。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 出在“哪个任务和哪个处理器配对”。  
- 如果把一个 **很长** 的任务交给 **晚到** 的处理器，`processorTime + task` 可能会非常大，拖慢整体。  
- 反之，如果把 **长任务** 分配给 **早到** 的处理器，虽然它本身会晚一点结束，但整体的最大值往往更小。

**关键观察**：  
> 处理器的开工时间越早，就应该负责越**长**的任务。  

于是我们可以把两组数据都排好序：

1. **处理器时间**从小到大排序（早到的在前）。  
2. **任务时长**从大到小排序（最长的在前）。  

然后按照顺序配对：第 `i` 台处理器（已排好序）负责当前剩余的 **4** 个最长任务。  
因为每台处理器必须恰好执行 4 项任务，这正好对应把任务数组切成长度为 4 的块。

**为什么这样是最优的？**  
- 设想有两台处理器 `A`（早）和 `B`（晚），以及两个任务 `x`（长）和 `y`（短），且 `x > y`。  
- 若把 `x` 给 `B`、`y` 给 `A`，最大完成时间为 `max(t_A + y, t_B + x)`。  
- 若把 `x` 给 `A`、`y` 给 `B`，最大完成时间为 `max(t_A + x, t_B + y)`。  
- 因为 `t_A ≤ t_B` 且 `x > y`，容易证明第二种配对的最大值 **不大于** 第一种。  
- 通过把任务按 **降序**、处理器按 **升序** 配对，所有类似的“交换”都会让最大值不增，故全局最优。

**类比**：把“早起的学生”安排做“最难的题”，把“晚起的学生”安排做“容易的题”，这样全班的最迟交卷时间会最短。

#### 代码（Python）

```python
def minimumProcessingTime(processorTime, tasks):
    """
    贪心 + 排序的最优实现。
    1. 处理器时间升序（早到的在前）
    2. 任务时长降序（最长的在前）
    3. 按顺序把每台处理器分配 4 个任务，记录最大完成时间
    """
    # 1. 排序
    processorTime.sort()               # 早到的在前
    tasks.sort(reverse=True)           # 最长的在前

    n = len(processorTime)              # 处理器数量
    max_finish = 0

    # 2. 逐台处理器配任务
    for i in range(n):
        # 这台处理器负责 tasks 中的第 i*4 ~ i*4+3 四个任务
        for j in range(4):
            task_idx = i * 4 + j
            finish_i = processorTime[i] + tasks[task_idx]
            # 更新全局最大完成时间
            if finish_i > max_finish:
                max_finish = finish_i

    return max_finish
```

> **代码要点注释**  
> - `processorTime.sort()`：把“谁先准备好”排好序，就像把排队的人按到达时间从早到晚排好。  
> - `tasks.sort(reverse=True)`：把“谁最耗时”排好序，像把作业难度从高到低排好。  
> - 循环里 `i * 4 + j` 正好取出当前处理器需要的四个最长剩余任务。  

#### 复杂度  

- **时间复杂度**：`O(m log m)`，其中 `m = 4n = len(tasks)`。  
  - 排序 `tasks` 需要 `O(m log m)`，排序 `processorTime` 只要 `O(n log n)`，`n ≤ m/4`，总体仍是 `O(m log m)`。  
  - 大白话：如果有 100,000 项任务，算法大约要进行 100,000 × log₂10⁵ ≈ 1.7 百万次比较，仍然很快。  
- **空间复杂度**：`O(1)`（不计输入数组本身的存储）。  
  - 只用了几个整数变量 `max_finish、i、j、task_idx`，没有额外的大数组。

> 与暴力解相比，时间复杂度从线性 `O(m)` 仍然是线性，但因为我们必须先排序，整体稍慢；然而暴力解根本不保证最小的最大完成时间。真正的提升在于 **结果质量**：贪心解得到的最大完成时间是**全局最小**的。

---

## 心得

- **核心技巧**：**贪心 + 排序**（把早的配长的），这是一种常见的“最大化‑最小化”思路。  
- **适用的题型**  
  1. “任务调度”类：如 LeetCode 1977 *Minimum Time to Finish the Race*（把最快的跑道配最慢的选手）。  
  2. “配对最大值最小化”类：如 2405 *Optimal Partition of String*（把大数配小数）。  
  3. “多机器分配”类：如 2185 *Maximum Number of Words You Can Type*（把常用字母配高频单词）。  
- **一句话总结**：让**最早准备好的机器**去做**最长的任务**，即可把整体最晚完成时间压到最低。

---

## 反思

- **第一反应**：看到“每台机器 4 核、任务数是 4 倍”，本能想到把任务平均分配，随后想到**排序配对**会更好。  
- **最容易踩的坑**  
  - 忘记 **每台机器必须恰好 4 项任务**，导致配对不完整。  
  - 忽视 **任务长度可能非常大**（`10⁹`），在计算时要使用 `int`（Python 自动大整数，C++ 需要 `long long`）。  
  - 边界条件：当 `processorTime` 含有相同值或 `tasks` 中有相同长度时，排序仍然有效，不需要额外处理。  
- **下次遇到同类题**：第一步想到 **把两组数据分别排序（一个升序，一个降序）**，再**按顺序配对**，这往往是最直接的最优贪心策略。