# #3386. **按键最长按压时间** / Button with Longest Push Time

> 难度：简单 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/button-with-longest-push-time/)

---

## 题目（英文原版）

**Description**

You are given a 2D array events which represents a sequence of events where a child pushes a series of buttons on a keyboard.
Each events[i] = [indexi, timei] indicates that the button at index indexi was pressed at time timei.
Return the index of the button that took the longest time to push. If multiple buttons have the same longest time, return the button with the smallest index.

**Examples**

**Example 1:**

```
Input: events = [[1,2],[2,5],[3,9],[1,15]]
Output: 1
Explanation:
```

**Example 2:**

```
Input: events = [[10,5],[1,7]]
Output: 10
Explanation:
```

**Constraints**

- 1 <= events.length <= 1000
- events[i] == [indexi, timei]
- 1 <= indexi, timei <= 105
- The input is generated such that events is sorted in increasing order of timei.

---

## 题目（中文翻译）

给定一个二维数组 `events`，它表示一系列事件，其中一个孩子在键盘上依次按下若干按钮。  
每个 `events[i] = [index_i, time_i]` 表示在时间 `time_i` 时，位于索引 `index_i` 的按钮被按下。  
返回按压时间最长的按钮的索引。如果有多个按钮的按压时间相同，返回索引最小的那个按钮。

**示例 1**

```text
Input: events = [[1,2],[2,5],[3,9],[1,15]]
Output: 1
解释：
```

**示例 2**

```text
Input: events = [[10,5],[1,7]]
Output: 10
解释：
```

**约束条件**

- `1 <= events.length <= 1000`
- `events[i] == [index_i, time_i]`
- `1 <= index_i, time_i <= 10^5`
- 输入保证 `events` 按 `time_i` 的递增顺序排序。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**对每一次按键事件，都去找它前面最近的那一次事件，算出时间差**，再在所有差值里挑出最大的那一次对应的按钮编号。  

- **用到的数据结构**：只需要把 `events` 这张二维表（相当于一张“记录表”，每行像字典里的一条 `key → value`）完整保存下来。这里不需要额外的哈希表、栈或队列，只用列表（list）就行。  
- **为什么正确**：题目保证 `events` 按时间递增排列，所以某一次按键的“持续时间”一定是它的 `time` 减去**紧挨在它前面的那一次**的 `time`（第一条记录的前面可以认为是时间 `0`）。只要我们把每一次的时间差算出来，最大值对应的按钮就是答案。  
- **时间/空间复杂度**：  
  - 为了算第 `i` 条记录的持续时间，我们要在 `i‑1 … 0` 的范围里**逐个检查**，找到最近的前一条记录，这一步在最坏情况下要遍历 `i` 次。对所有 `n` 条记录累加起来，就是 `1 + 2 + … + (n‑1) = O(n²)`。  
  - 只用了原始的 `events` 列表，没有额外的大空间，空间复杂度是 `O(1)`（不计输入本身）。

> **大白话**：`O(n²)` 可以想象成“在 1000 个人的队伍里，每个人都要跟前面所有人打招呼”，次数会爆炸式增长。

#### 代码（Python）

```python
def longestPushButton_bruteforce(events):
    """
    暴力解法：逐个向前查找前一条记录，计算持续时间
    :param events: List[List[int]]，每个子列表为 [index, time]
    :return: 持续时间最长的按钮下标
    """
    n = len(events)
    max_duration = 0          # 当前看到的最长持续时间
    answer = None             # 对应的按钮下标

    for i in range(n):
        # 第 i 条记录的时间
        cur_time = events[i][1]

        # 暴力查找它前面的最近一条记录（实际上就是 i-1 那条，因为已经排好序）
        # 这里写成循环只为演示“逐个检查”，实际可以直接取 i-1
        prev_time = 0         # 默认前一个时间是 0（第一条记录的情况）
        for j in range(i - 1, -1, -1):
            prev_time = events[j][1]
            break            # 找到最近的前一条记录后立即退出循环

        duration = cur_time - prev_time   # 本次按键的持续时间

        # 更新最大值：如果相同则取下标更小的按钮
        if duration > max_duration or (duration == max_duration and events[i][0] < answer):
            max_duration = duration
            answer = events[i][0]

    return answer
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 每条记录都要向前遍历一次，次数随 `n` 的平方增长。  
- **空间复杂度**：`O(1)` —— 只用了常数级的额外变量（不计输入本身）。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正的慢点在于每次都去向前遍历寻找前一条记录**。但题目已经保证 `events` 按时间递增，这意味着“前一条记录”**恰好就是当前记录的前一个元素**，不需要再搜索。

于是我们可以**一次遍历**整个数组，直接用 `events[i-1][1]`（上一次的时间）来计算当前的持续时间：

1. **初始化**：把第一条记录的持续时间视为 `time - 0`，并记录当前的最大时长和对应的按钮。  
2. **遍历**：从第二条记录开始，`duration = events[i][1] - events[i-1][1]`。  
3. **比较 & 更新**：如果 `duration` 更大，就更新答案；如果相等且按钮编号更小，同样更新（因为题目要求 “最小下标”。）  
4. **返回**：遍历结束后得到的 `answer` 即为所求。

核心算法其实是 **一次扫描（single pass）**，没有额外的数据结构，只用两个变量保存“当前最大时长”和“对应按钮”。  

> **类比**：想象你在看一本排好顺序的车票，想知道哪趟车的间隔最长，只需要把相邻两张票的时间差算一遍，不必把每张票都和所有前面的票比。

#### 代码（Python）

```python
def longestPushButton(events):
    """
    最优解：一次遍历即可求出最长持续时间对应的按钮
    :param events: List[List[int]]，已按 time 升序排序
    :return: 持续时间最长的按钮下标（若相同则返回下标最小的）
    """
    # 第一条记录的持续时间是 time - 0
    max_duration = events[0][1]          # 当前已知的最长时间
    answer = events[0][0]                # 对应的按钮下标

    # 从第二条记录开始逐个比较相邻时间差
    for i in range(1, len(events)):
        cur_index, cur_time = events[i]
        prev_time = events[i - 1][1]     # 正好是前一条记录的 time

        duration = cur_time - prev_time  # 本次按键的持续时间

        # 更新规则：更长 → 直接换；相等且下标更小 → 也换
        if duration > max_duration or (duration == max_duration and cur_index < answer):
            max_duration = duration
            answer = cur_index

    return answer
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历一次数组，次数随 `n` 线性增长。相比暴力的 `O(n²)` 快了很多。  
- **空间复杂度**：`O(1)` —— 只用了常数个额外变量（不计输入本身）。

---

## 心得

- **核心技巧**：利用**已排序的特性**，把“前一条记录”直接映射为相邻元素，从而实现一次扫描。  
- **适用的题型**：  
  1. “相邻元素差值最大”类（如 LeetCode 1672 `Maximum Time Gap`）。  
  2. “区间长度最长”类（如 LeetCode 2415 `Longest Subarray With Maximum Score` 的变形）。  
  3. “事件持续时间”类（如 LeetCode 2453 `Destroy the Monsters` 中的时间窗口）。  
- **一句话总结**：**排序+相邻差**是求“最长/最短间隔”问题的“万能钥匙”。

## 反思

- **第一反应**：看到“已排序的时间”，第一时间会想到只看相邻两条记录的差值，而不是遍历所有前面的记录。  
- **最容易踩的坑**：  
  - 忘记把第一条记录的起点当作时间 `0`，导致计算少了第一段的持续时间。  
  - 当出现多个按钮的最长时间相同，忘记返回 **下标最小** 的按钮。  
- **下次类似题的第一步**：检查输入是否已经**有序**或**可直接映射**到相邻元素，然后决定是“一次扫描”还是需要额外的数据结构（如哈希表、堆）来辅助。