# #2071. 可分配的最大任务数 / Maximum Number of Tasks You Can Assign

> 难度：困难 · 标签：Array、Two Pointers、Binary Search、Greedy、Queue、Sorting、Monotonic Queue · [LeetCode 链接](https://leetcode.com/problems/maximum-number-of-tasks-you-can-assign/)

---

## 题目（英文原版）

**Description**

You have n tasks and m workers. Each task has a strength requirement stored in a 0-indexed integer array tasks, with the ith task requiring tasks[i] strength to complete. The strength of each worker is stored in a 0-indexed integer array workers, with the jth worker having workers[j] strength. Each worker can only be assigned to a single task and must have a strength greater than or equal to the task's strength requirement (i.e., workers[j] >= tasks[i]).
Additionally, you have pills magical pills that will increase a worker's strength by strength. You can decide which workers receive the magical pills, however, you may only give each worker at most one magical pill.
Given the 0-indexed integer arrays tasks and workers and the integers pills and strength, return the maximum number of tasks that can be completed.

**Examples**

**Example 1:**

```
Input: tasks = [3,2,1], workers = [0,3,3], pills = 1, strength = 1
Output: 3
Explanation:
We can assign the magical pill and tasks as follows:
- Give the magical pill to worker 0.
- Assign worker 0 to task 2 (0 + 1 >= 1)
- Assign worker 1 to task 1 (3 >= 2)
- Assign worker 2 to task 0 (3 >= 3)
```

**Example 2:**

```
Input: tasks = [5,4], workers = [0,0,0], pills = 1, strength = 5
Output: 1
Explanation:
We can assign the magical pill and tasks as follows:
- Give the magical pill to worker 0.
- Assign worker 0 to task 0 (0 + 5 >= 5)
```

**Example 3:**

```
Input: tasks = [10,15,30], workers = [0,10,10,10,10], pills = 3, strength = 10
Output: 2
Explanation:
We can assign the magical pills and tasks as follows:
- Give the magical pill to worker 0 and worker 1.
- Assign worker 0 to task 0 (0 + 10 >= 10)
- Assign worker 1 to task 1 (10 + 10 >= 15)
The last pill is not given because it will not make any worker strong enough for the last task.
```

**Constraints**

- n == tasks.length
- m == workers.length
- 1 <= n, m <= 5 * 104
- 0 <= pills <= m
- 0 <= tasks[i], workers[j], strength <= 109

---

## 题目（中文翻译）

你有 `n` 项任务和 `m` 名工人。每个任务的强度要求存放在一个 **0 索引** 整数数组 `tasks` 中，第 `i` 项任务需要 `tasks[i]` 的强度才能完成。每名工人的强度存放在一个 **0 索引** 整数数组 `workers` 中，第 `j` 名工人的强度为 `workers[j]`。每名工人只能被分配到 **一个** 任务，并且必须拥有 **大于或等于** 该任务强度要求的强度（即 `workers[j] >= tasks[i]`）。

另外，你拥有 `pills` 颗魔法药丸（magical pills），每颗药丸可以让工人的强度提升 `strength`。你可以决定哪些工人服用魔法药丸，但每名工人至多只能服用 **一颗** 药丸。

给定整数数组 `tasks`、`workers`，以及整数 `pills` 和 `strength`，返回可以完成的 **最大任务数**。

---

### 示例

#### 示例 1
```
Input: tasks = [3,2,1], workers = [0,3,3], pills = 1, strength = 1
Output: 3
Explanation:
我们可以如下分配魔法药丸和任务：
- 将魔法药丸给工人 0。
- 将工人 0 分配给任务 2（0 + 1 >= 1）。
- 将工人 1 分配给任务 1（3 >= 2）。
- 将工人 2 分配给任务 0（3 >= 3）。
```

#### 示例 2
```
Input: tasks = [5,4], workers = [0,0,0], pills = 1, strength = 5
Output: 1
Explanation:
我们可以如下分配魔法药丸和任务：
- 将魔法药丸给工人 0。
- 将工人 0 分配给任务 0（0 + 5 >= 5）。
```

#### 示例 3
```
Input: tasks = [10,15,30], workers = [0,10,10,10,10], pills = 3, strength = 10
Output: 2
Explanation:
我们可以如下分配魔法药丸和任务：
- 将魔法药丸给工人 0 和工人 1。
- 将工人 0 分配给任务 0（0 + 10 >= 10）。
- 将工人 1 分配给任务 1（10 + 10 >= 15）。
最后一颗药丸不使用，因为它无法让任何工人强度足以完成剩余的任务。
```

---

### 约束条件

- `n == tasks.length`
- `m == workers.length`
- `1 <= n, m <= 5 * 10^4`
- `0 <= pills <= m`
- `0 <= tasks[i], workers[j], strength <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每个任务都逐一尝试找一个合适的工人**。  
我们可以遍历 `tasks`（任务强度数组），对每个任务：

1. 在 `workers` 中找一个未被使用且强度 `>=` 任务强度的工人，直接分配。  
2. 如果找不到，就再找一个未被使用且 `strength + workers[j] >=` 任务强度的工人，给他喝一颗药（pill），再分配。  
3. 如果连这样都做不到，就说明这条任务无法完成。

> **类比**：把 `workers` 看成一本字典，`workers[j]` 是词条的页码，任务强度是我们要查的“单词”。  
> - 不需要药的工人就像字典里已经有对应页码的词，直接翻到那页就行。  
> - 需要药的工人相当于词条少了几页（强度不足），我们可以在字典后面贴一张“补页”把它补足（喝药）。

因为我们要把 **每个任务都尝试一次**，而每次尝试都要在所有未使用的工人里线性搜索，所以时间会非常慢。

**正确性**：只要我们能够把所有任务都找到了满足条件的工人（可能加药），显然这就是一种合法的分配方式；如果找不到，就说明在当前的分配策略下该任务不可完成。暴力搜索遍历所有可能的配对，自然能得到答案（虽然效率低）。

**复杂度**  
- 对每个任务我们可能要遍历全部工人 → **时间复杂度** `O(n·m)`（`n` 为任务数，`m` 为工人数）。  
  用大白话说，就是如果有 10 000 个任务和 10 000 个工人，最坏情况下要比较 **一亿次**。  
- 只用了几个额外的数组/计数器 → **空间复杂度** `O(1)`（不计输入数组本身）。

显然，这个解法在 LeetCode 的数据规模（`n,m ≤ 5·10⁴`）下会超时。

---

### 2. 最优解

#### 思路  

**从暴力解的瓶颈出发**：  
- 暴力解每次都要在所有剩余工人里线性查找，导致 `O(n·m)`。  
- 关键是 **快速找到**：  
  1. **可以直接完成任务的最弱工人**（强度已足够）。  
  2. **需要药才能完成任务的最弱工人**（强度 + `strength` 已足够）。

这两类工人如果能在 **对数时间** 内取得，就可以把整体复杂度降到 `O((n+m)·log m)`，再配合二分搜索检查“是否能完成前 `k` 项任务”，整体复杂度会是 `O((n+m)·log m·log n)`，完全可以接受。

**核心思路**：  
1. **先排序**  
   - `tasks` 从小到大排序。  
   - `workers` 也从小到大排序。  
   排序后，**最容易完成的任务**对应最左侧的 `tasks`，**最强的工人**对应最右侧的 `workers`。  

2. **二分答案**  
   - 设 `k` 为我们想要检查能否完成的任务数（取最小的 `k` 个任务）。  
   - 通过二分搜索 `k` 的取值范围 `[0, min(n,m)]`，每次调用 **可行性检测函数** `can(k)`。  
   - 最后返回最大的 `k`。

3. **可行性检测 `can(k)`（贪心）**  
   - 只关注 `tasks[:k]`（最小的 `k` 个任务），因为如果最小的 `k` 项都做不到，任何别的 `k` 项更不可能完成。  
   - 按 **任务强度从大到小**（即从 `tasks[k-1]` 往左遍历）处理，这样每一步都在处理当前“最难的”任务，后面的任务只会更容易。  
   - 使用两个指针和一个 **最大堆**（`heapq` 的负数实现）来管理工人：
     - `right` 指向 `workers` 中尚未考虑的最强工人（从右向左移动）。  
     - **直接可用的工人**：`workers[right] >= cur_task` 时，直接把该工人分配给当前任务（不需要药），`right--`。  
     - **可能需要药的工人**：当 `workers[right] + strength >= cur_task`（即加药后足够）但 `workers[right] < cur_task` 时，把该工人的强度放入 **最大堆** `candidates`（存负数，使 `heapq` 成为最大堆）。随后 `right--`。  
   - 对当前任务 `cur_task`：
     1. **优先使用直接可用的工人**（因为不消耗药）。如果 `right` 仍指向满足 `workers[right] >= cur_task` 的工人，直接分配。  
     2. 否则 **尝试使用一颗药**：从 `candidates` 堆里弹出 **强度最大的**工人（即负数最小的），给他药，`pills--`。使用强度最大的原因是：这些工人本来最接近任务强度，使用药后浪费最少的“余量”，而把更弱的工人留给后面更容易的任务。  
     3. 如果既没有直接可用的工人，也没有可用的 `candidates`（或者药已经用完），则 `can(k)` 失败。  

   - 当所有 `k` 个任务都顺利分配完，`can(k)` 成功。

> **类比**：  
> - 把 `workers` 想成一排排的“砖块”，强度越大砖块越厚。  
> - 任务是需要一定厚度的“墙”。我们从最高的墙开始建（最大任务），先用最厚的砖（直接满足），如果厚度不够就给砖块粘上一层“胶水”（药）再用。  
> - 用胶水的砖块我们挑最接近墙高的那块，这样胶水浪费最少，后面更低的墙还能用更薄的砖。

**为什么二分 + 贪心能得到最优**：

- **二分**：因为如果我们可以完成 `k` 项任务，那么一定可以完成 `k-1` 项（把最难的那一项去掉即可），这是一种单调性，适合二分搜索。  
- **贪心**：在固定的 `k` 下，处理最难任务时使用**最弱**且足够的工人（直接或加药）是最安全的选择——因为留下的工人都更强或更易于加药，后面的任务更容易完成。若在某一步使用了更强的工人而导致后面任务失败，则必然存在更优的分配（换成更弱的工人），所以贪心不会错。

#### 代码（Python）

```python
import heapq
from typing import List

def maxTaskAssign(tasks: List[int], workers: List[int],
                  pills: int, strength: int) -> int:
    """
    返回能够完成的最大任务数
    """
    tasks.sort()                 # 任务从小到大
    workers.sort()               # 工人从小到大
    n, m = len(tasks), len(workers)

    # ---------- 可行性检测 ----------
    def can(k: int) -> bool:
        """能否完成 tasks 中最小的 k 项任务"""
        # 只看前 k 个最小任务
        need = tasks[:k]               # 已经是升序
        # 从大到小遍历（最难的任务先处理）
        need_idx = k - 1               # 当前任务在 need 中的下标
        right = m - 1                  # workers 中未使用的最强工人的指针
        cand = []                      # 最大堆（存负数），保存“需要药”的工人
        remain_pills = pills

        while need_idx >= 0:
            cur = need[need_idx]       # 当前最难的任务

            # 把所有强度 >= cur 的工人直接加入“直接可用”区间
            while right >= 0 and workers[right] >= cur:
                # 直接使用，不放入堆
                right -= 1
                # 直接匹配成功，跳过这次循环
                break
            else:
                # 没有直接可用的工人，先把所有“加药后足够”的工人放进堆
                while right >= 0 and workers[right] + strength >= cur:
                    # 负数实现最大堆
                    heapq.heappush(cand, -workers[right])
                    right -= 1

                # 现在尝试使用药
                if remain_pills > 0 and cand:
                    # 取出强度最大的工人（负数最小的）
                    heapq.heappop(cand)
                    remain_pills -= 1
                else:
                    # 既没有直接工人，也没有药可用，失败
                    return False
            # 当前任务已被安排
            need_idx -= 1
        return True

    # ---------- 二分搜索 ----------
    lo, hi = 0, min(n, m)
    while lo < hi:
        mid = (lo + hi + 1) // 2      # 取上半段防止死循环
        if can(mid):
            lo = mid                  # 能完成，尝试更多
        else:
            hi = mid - 1              # 不能完成，缩小范围
    return lo
```

**代码要点解释（每行中文注释）**

```python
tasks.sort()                 # 任务从小到大，方便取最小的 k 项
workers.sort()               # 工人从小到大，后面用指针从右侧取最强的工人
...
def can(k: int) -> bool:    # 检查能否完成前 k 项最小任务
    need = tasks[:k]        # 只关注这 k 项，已经是升序
    need_idx = k - 1        # 从最难的任务（右端）开始处理
    right = m - 1           # workers 中最右侧（最强）的工人指针
    cand = []               # 最大堆，存“加药后足够”的工人（负数实现最大堆）
    remain_pills = pills    # 复制一份药的数量，避免修改全局变量
...
while need_idx >= 0:        # 逐个处理任务
    cur = need[need_idx]    # 当前任务的强度
    # 1. 直接可以完成的工人（strength 已足够）放到直接区
    while right >= 0 and workers[right] >= cur:
        right -= 1          # 直接使用最弱的满足条件的工人
        break               # 任务已配好，进入下一个任务
    else:
        # 2. 把所有“加药后足够”的工人放进堆
        while right >= 0 and workers[right] + strength >= cur:
            heapq.heappush(cand, -workers[right])   # 负数 → 最大堆
            right -= 1
        # 3. 需要药且药还剩
        if remain_pills > 0 and cand:
            heapq.heappop(cand)     # 取出强度最大的工人使用药
            remain_pills -= 1
        else:
            return False            # 没有办法完成当前任务
    need_idx -= 1                 # 继续处理下一个（更容易）任务
...
# 二分搜索寻找最大可完成的任务数
while lo < hi:
    mid = (lo + hi + 1) // 2
    if can(mid):
        lo = mid
    else:
        hi = mid - 1
return lo
```

#### 复杂度

- **排序**：`O(n log n + m log m)`，一次性完成。  
- **二分搜索**：最多 `log(min(n,m))` 次检查。  
- **每次检查 `can(k)`**：  
  - 任务和工人指针各只遍历一次 → `O(k + m)`（`k ≤ n`），  
  - 堆的每次插入/弹出是 `O(log m)`，最多插入 `m` 次。  
  - 因此 `can(k)` 的时间复杂度是 `O((k + m)·log m)`，在最坏情况下约 `O((n+m)·log m)`。  
- **总体时间复杂度**：`O((n+m)·log m·log n)`。在 `n,m ≤ 5·10⁴` 的限制下完全可以在 1 秒左右跑完。  

- **空间复杂度**：  
  - 需要存放排序后的数组 `O(n + m)`（输入本身已经占用），  
  - 额外的堆最多保存 `m` 个工人 → `O(m)`。  
  - 其余变量都是常数级。  
  - **总体额外空间** `O(m)`，即线性空间。

---

## 心得

- **核心技巧**：**二分答案 + 贪心配对（双指针 + 最大堆）**。  
- **适用的题型**：  
  1. “能否在给定资源下完成前 `k` 项任务”——如 *Maximum Number of Darts Inside a Circle*（二分 + 检查）。  
  2. “在限制次数的加成/升级下，最大可完成的请求数”——如 *Maximum Number of Events That Can Be Attended II*（二分 + 贪心）。  
- **一句话总结解题钥匙**：**把任务从最难到最易排好序，用最弱且足够的工人（必要时加药）贪心配对，二分寻找最大可完成的任务数**。

---

## 反思

- **第一反应**：直接尝试每个任务配工人（暴力），但很快意识到会超时。  
- **最容易踩的坑**  
  - **边界条件**：`pills = 0` 或 `strength = 0` 时，不能忘记仍然需要正确处理“加药后足够”的判断。  
  - **堆的使用**：忘记把负数放进去会导致最小堆而非最大堆，导致错误的工人被选中。  
  - **二分取中点**：若使用 `(lo+hi)//2` 且不做上取整，可能陷入死循环（`lo` 永远不变）。  
- **下次类似题**：第一步先检查**单调性**（完成 `k` 能否推出完成 `k-1`），决定是否用二分；随后用**排序 + 双指针/堆**的贪心配对思路，确保每一步都使用“最弱足够的资源”。