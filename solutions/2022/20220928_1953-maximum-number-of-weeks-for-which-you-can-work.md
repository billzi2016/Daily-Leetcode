# #1953. 可以工作的最长周数 / Maximum Number of Weeks for Which You Can Work

> 难度：中等 · 标签：Array、Greedy · [LeetCode 链接](https://leetcode.com/problems/maximum-number-of-weeks-for-which-you-can-work/)

---

## 题目（英文原版）

**Description**

There are n projects numbered from 0 to n - 1. You are given an integer array milestones where each milestones[i] denotes the number of milestones the ith project has.
You can work on the projects following these two rules:
Once all the milestones of all the projects are finished, or if the only milestones that you can work on will cause you to violate the above rules, you will stop working. Note that you may not be able to finish every project's milestones due to these constraints.
Return the maximum number of weeks you would be able to work on the projects without violating the rules mentioned above.

**Examples**

**Example 1:**

```
Input: milestones = [1,2,3]
Output: 6
Explanation: One possible scenario is:
​​​​- During the 1st week, you will work on a milestone of project 0.
- During the 2nd week, you will work on a milestone of project 2.
- During the 3rd week, you will work on a milestone of project 1.
- During the 4th week, you will work on a milestone of project 2.
- During the 5th week, you will work on a milestone of project 1.
- During the 6th week, you will work on a milestone of project 2.
The total number of weeks is 6.
```

**Example 2:**

```
Input: milestones = [5,2,1]
Output: 7
Explanation: One possible scenario is:
- During the 1st week, you will work on a milestone of project 0.
- During the 2nd week, you will work on a milestone of project 1.
- During the 3rd week, you will work on a milestone of project 0.
- During the 4th week, you will work on a milestone of project 1.
- During the 5th week, you will work on a milestone of project 0.
- During the 6th week, you will work on a milestone of project 2.
- During the 7th week, you will work on a milestone of project 0.
The total number of weeks is 7.
Note that you cannot work on the last milestone of project 0 on 8th week because it would violate the rules.
Thus, one milestone in project 0 will remain unfinished.
```

**Constraints**

- n == milestones.length
- 1 <= n <= 105
- 1 <= milestones[i] <= 109

---

## 题目（中文翻译）

**题目描述**  
有 `n` 个项目，编号从 `0` 到 `n - 1`。给定一个整数数组 `milestones`，其中 `milestones[i]` 表示第 `i` 个项目拥有的里程碑（milestone）数量。你每周只能完成 **恰好一个** 项目的一个里程碑，并且必须遵守以下两条规则：

1. **同一周只能完成一个里程碑**。  
2. **连续两周不能在同一个项目上工作**。

当所有项目的里程碑全部完成，或是此时唯一还能完成的里程碑会导致违反上述规则时，你必须停止工作。注意，受这些约束的影响，可能并不能完成所有项目的里程碑。

返回在不违反规则的前提下，你最多可以工作多少周。

---

### 示例

**示例 1**  
```text
Input: milestones = [1,2,3]
Output: 6
Explanation: 一种可能的安排如下：
- 第 1 周，完成项目 0 的一个里程碑。
- 第 2 周，完成项目 2 的一个里程碑。
- 第 3 周，完成项目 1 的一个里程碑。
- 第 4 周，完成项目 2 的一个里程碑。
- 第 5 周，完成项目 1 的一个里程碑。
- 第 6 周，完成项目 2 的一个里程碑。
```

**示例 2**  
```text
Input: milestones = [5,2,1]
Output: 7
Explanation: 一种可能的安排如下：
- 第 1 周，完成项目 0 的一个里程碑。
- 第 2 周，完成项目 1 的一个里程碑。
- 第 3 周，完成项目 0 的一个里程碑。
- 第 4 周，完成项目 1 的一个里程碑。
- 第 5 周，完成项目 0 的一个里程碑。
- 第 6 周，完成项目 2 的一个里程碑。
- 第 7 周，完成项目 0 的一个里程碑。
```

---

### 约束条件
- `n == milestones.length`
- `1 <= n <= 10^5`
- `1 <= milestones[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**模拟每一周的工作**：

1. 记录每个项目还剩多少里程碑（milestone）。
2. 每一周挑选一个**不是上周刚刚做过的项目**且里程碑数最多的项目来工作（因为里程碑多的项目更容易“卡住”，先把它们消耗掉更安全）。
3. 完成后把该项目的里程碑数减 1，继续下一周，直到找不到合法的项目为止。

> **类比**：把每个项目想成一本字典，`milestones[i]` 就是这本字典的页数。我们每周只能翻一本字典的下一页，而且**不能连续两周翻同一本字典**。于是我们每次都挑“页数最多”的字典翻（就像在查字典时先查词条多的那本），这样能让所有字典的页数尽量均匀减少。

**为什么正确**  
只要每一步都遵守“不连续同项目”的规则，模拟的过程就是合法的工作序列。遍历完所有可能的周数后得到的长度，就是题目要求的“最多能工作多少周”。

**时间/空间复杂度**  
- **时间**：每工作一周要从所有项目中找出里程碑最多的（可以用最大堆），这一步是 `O(log n)`。如果总里程碑数为 `S = sum(milestones)`，最坏情况下要工作 `S` 周，所以时间复杂度是 `O(S·log n)`。  
  - 直观理解：`S` 就是所有项目的“总工作量”。如果每个里程碑都要单独处理，就相当于遍历 `S` 次，每次都要在 `n` 本“字典”里挑出最大的一本（用堆实现的挑选代价是 `log n`）。
- **空间**：需要保存每个项目剩余的里程碑数以及堆结构，都是 `O(n)` 的额外空间。

> 当 `milestones[i]` 可能高达 `10^9` 时，`S` 也会非常大，`O(S·log n)` 直接不可接受，这也是我们后面要优化的原因。

#### 代码（Python）

```python
import heapq
from typing import List

def maxWeeks_bruteforce(milestones: List[int]) -> int:
    # ---------- 构造最大堆（Python 的 heapq 是最小堆，取负数实现最大堆） ----------
    max_heap = [(-x, i) for i, x in enumerate(milestones) if x > 0]
    heapq.heapify(max_heap)          # O(n)

    prev_idx = -1                     # 上一周工作的项目编号，-1 表示“还没有”
    weeks = 0

    while max_heap:
        # 取出里程碑最多的项目
        cnt1, idx1 = heapq.heappop(max_heap)
        cnt1 = -cnt1                   # 还原为正数

        # 如果恰好是上周的项目，只能尝试第二多的项目
        if idx1 == prev_idx:
            if not max_heap:           # 堆里已经没有别的项目，只能停下来
                break
            cnt2, idx2 = heapq.heappop(max_heap)
            cnt2 = -cnt2

            # 这周工作 idx2 项目
            weeks += 1
            prev_idx = idx2
            cnt2 -= 1                   # 完成一个里程碑

            # 把可能还有剩余的项目重新放回堆
            if cnt2 > 0:
                heapq.heappush(max_heap, (-cnt2, idx2))
            # 把之前弹出的 idx1 重新放回堆，等待以后再用
            heapq.heappush(max_heap, (-cnt1, idx1))
        else:
            # 这周工作 idx1 项目
            weeks += 1
            prev_idx = idx1
            cnt1 -= 1                   # 完成一个里程碑
            if cnt1 > 0:
                heapq.heappush(max_heap, (-cnt1, idx1))

    return weeks
```

#### 复杂度

- **时间复杂度**：`O(S·log n)`，其中 `S = sum(milestones)`，`log n` 来自堆的插入/弹出操作。  
  - 大白话：如果你要处理 1000 条任务，每次都要在 10 本字典里找最大的一本，找的代价大概是 “找一本最快的书要花大约 3（log₂10≈3）步”。于是总耗时约为 `1000 × 3 = 3000 步`。
- **空间复杂度**：`O(n)`，只存储每个项目的剩余里程碑数和堆的结构。

---

### 2. 最优解

#### 思路  

从暴力解可以看到**瓶颈**在于每周都要做一次“挑最大”的操作，导致时间随总里程碑数 `S` 线性增长。而其实我们只需要**判断是否能把所有里程碑排成不相邻的序列**，不必真的去排。

**关键观察**  

- 把所有里程碑看成 **颜色**，每个项目对应一种颜色。题目要求相邻两周的颜色不能相同，即 **不出现相同颜色的相邻元素**。
- 设 `total = sum(milestones)` 为所有里程碑的总数，`mx = max(milestones)` 为最多的那一个项目的里程碑数。  
- 其余项目的里程碑总和为 `rest = total - mx`。

现在有两种可能：

1. **mx 不“太多”**  
   当 `mx <= rest + 1` 时，最“多”的项目的里程碑可以被其他项目的里程碑充分“穿插”。想象把最多项目的里程碑排成 `mx` 个格子：

   ```
   A _ A _ A _ ... A   （A 代表最多项目）
   ```

   只要其他项目的总数 `rest` 至少能填满这些下划线 `_`（即 `rest >= mx-1`），我们就能把所有里程碑全部安排完。此时 **答案等于 total**（所有里程碑都能工作）。

2. **mx “太多”**  
   当 `mx > rest + 1` 时，即使把所有其他项目的里程碑都穿进去，仍然会剩下多个连续的 `A`，这会导致规则被违反。此时我们只能交替使用 `A` 与其他项目，最多能安排的周数是：

   ```
   A B A B A B ... A   （B 表示任意其他项目）
   ```

   交替的次数受 `rest` 的限制，最多能出现 `rest` 对 `A-B`，再加上最前面的一个 `A`，于是 **可工作周数 = 2 * rest + 1**。

综合两种情况：

```
answer = min(total, 2 * rest + 1)
```

这就是 **O(n)** 时间、**O(1)** 额外空间的最优解。

> **类比**：想象你有若干根彩色线段，要把它们排成一条“不能相邻同色”的绳子。最长的那根线段如果比其他所有线段加起来还长 1，说明它会“孤零零”卡住，绳子只能做到 `2 * (其余总长) + 1` 长度；否则所有线段都能完整拼完。

#### 代码（Python）

```python
from typing import List

def maxWeeks(milestones: List[int]) -> int:
    total = sum(milestones)                 # 所有里程碑的总数
    mx = max(milestones)                    # 最多的那个项目的里程碑数
    rest = total - mx                       # 其他项目的里程碑总和

    # 如果最多的项目不至于“压垮”其余项目，直接返回 total
    # 否则只能交替使用，最多工作 2*rest + 1 周
    return min(total, 2 * rest + 1)
```

#### 复杂度

- **时间复杂度**：`O(n)`，只遍历一次数组求和和最大值。  
  - 与暴力解相比，**不再随里程碑总数 `S` 增长**，即使 `milestones[i]` 达到 `10^9`，运行时间仍在毫秒级。
- **空间复杂度**：`O(1)`，只用了常数个额外变量（`total`, `mx`, `rest`）。

---

## 心得

- **核心技巧**：把“相邻两周不能同项目”转化为“最大数量的项目能否被其他项目完全穿插”。这是一种 **极值比较**（max 与 sum‑max 的关系） 的思路。
- **适用的题型**  
  1. “重新排列字符，使相同字符不相邻” 类似的字符串题（如 LeetCode 358、767）。  
  2. “任务调度” 中要求同类任务之间有冷却时间的题目（如 LeetCode 621）。
- **一句话总结**：**只要比较最大里程碑数和其余里程碑之和，就能直接算出能工作的最长周数**。

---

## 反思

- **第一反应**：直接想到“每周挑最多的项目”，于是写出基于堆的模拟代码。  
- **最容易踩的坑**  
  - **边界条件**：只有一个项目时，答案只能是 `1`（因为第二周就会连续同项目），公式 `min(total, 2*rest+1)` 正好给出 `1`（`rest=0`）。  
  - **大数溢出**：`milestones[i]` 最高 `10^9`，`total` 可能达到 `10^14`，在某些语言需要 64 位整数；Python 的 `int` 自动大数，不会溢出。  
  - **误把 `rest + 1` 当作 `rest`**：判断是否可以全部完成时的阈值是 `mx <= rest + 1`，容易忘记加的那个 `1`（因为首尾可以各放一个最多项目的里程碑）。
- **下次遇到同类题**：第一步先 **比较最大元素与其余元素之和**，看是否能形成 “交替” 或 “完全覆盖” 的结构，再决定是直接返回总和还是用 `2*rest+1` 公式。这样可以快速定位最优解的方向，避免不必要的模拟。