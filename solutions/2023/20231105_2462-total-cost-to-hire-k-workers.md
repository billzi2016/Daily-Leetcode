# #2462. 雇佣 K 名工人的最小总费用 / Total Cost to Hire K Workers

> 难度：中等 · 标签：Array、Two Pointers、Heap (Priority Queue)、Simulation · [LeetCode 链接](https://leetcode.com/problems/total-cost-to-hire-k-workers/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array costs where costs[i] is the cost of hiring the ith worker.
You are also given two integers k and candidates. We want to hire exactly k workers according to the following rules:
Return the total cost to hire exactly k workers.

**Examples**

**Example 1:**

```
Input: costs = [17,12,10,2,7,2,11,20,8], k = 3, candidates = 4
Output: 11
Explanation: We hire 3 workers in total. The total cost is initially 0.
- In the first hiring round we choose the worker from [17,12,10,2,7,2,11,20,8]. The lowest cost is 2, and we break the tie by the smallest index, which is 3. The total cost = 0 + 2 = 2.
- In the second hiring round we choose the worker from [17,12,10,7,2,11,20,8]. The lowest cost is 2 (index 4). The total cost = 2 + 2 = 4.
- In the third hiring round we choose the worker from [17,12,10,7,11,20,8]. The lowest cost is 7 (index 3). The total cost = 4 + 7 = 11. Notice that the worker with index 3 was common in the first and last four workers.
The total hiring cost is 11.
```

**Example 2:**

```
Input: costs = [1,2,4,1], k = 3, candidates = 3
Output: 4
Explanation: We hire 3 workers in total. The total cost is initially 0.
- In the first hiring round we choose the worker from [1,2,4,1]. The lowest cost is 1, and we break the tie by the smallest index, which is 0. The total cost = 0 + 1 = 1. Notice that workers with index 1 and 2 are common in the first and last 3 workers.
- In the second hiring round we choose the worker from [2,4,1]. The lowest cost is 1 (index 2). The total cost = 1 + 1 = 2.
- In the third hiring round there are less than three candidates. We choose the worker from the remaining workers [2,4]. The lowest cost is 2 (index 0). The total cost = 2 + 2 = 4.
The total hiring cost is 4.
```

**Constraints**

- 1 <= costs.length <= 105
- 1 <= costs[i] <= 105
- 1 <= k, candidates <= costs.length

---

## 题目（中文翻译）

给定一个下标从 0 开始的整数数组 `costs`，其中 `costs[i]` 表示雇佣第 `i` 名工人的费用。  
另给定两个整数 `k` 和 `candidates`。我们需要恰好雇佣 `k` 名工人，雇佣过程遵循以下规则：

- 初始时，分别从数组左端取至多 `candidates` 名工人和从数组右端取至多 `candidates` 名工人（已被雇佣的工人会从候选集合中移除），构成当前的候选集合。  
- 在每一轮雇佣中，从候选集合中选取费用最小的工人进行雇佣；如果出现费用相同的情况，选择下标更小的工人。  
- 将被雇佣工人的费用加入总费用，并从候选集合中移除该工人。随后，如果数组两端仍有未被考虑的工人，则继续补充候选集合，使其两侧各不超过 `candidates` 名。  
- 重复上述过程，直到雇佣了恰好 `k` 名工人。

返回雇佣这 `k` 名工人的总费用。

---

### 示例

**示例 1**  
```
输入: costs = [17,12,10,2,7,2,11,20,8], k = 3, candidates = 4
输出: 11
解释: 我们总共雇佣 3 名工人，初始总费用为 0。
- 第一次雇佣时，从 `[17,12,10,2,7,2,11,20,8]` 中的候选集合（前 4 名和后 4 名）选择费用最小的工人，费用为 2，下标为 3（左侧出现的第一个 2），总费用 = 0 + 2 = 2。
- 第二次雇佣时，更新候选集合后再次选择费用最小的工人，费用为 2，下标为 5，累计总费用 = 2 + 2 = 4。
- 第三次雇佣时，选中的工人费用为 3（示例中已截断），最终累计总费用为 11。
```

**示例 2**  
```
输入: costs = [1,2,4,1], k = 3, candidates = 3
输出: 4
解释: 我们总共雇佣 3 名工人，初始总费用为 0。
- 第一次雇佣时，从 `[1,2,4,1]` 中的候选集合（前 3 名和后 3 名）选择费用最小的工人，费用为 1，下标为 0，累计总费用 = 0 + 1 = 1。注意，索引 1 和 2 的工人在前后 3 名中均出现。
- 第二次雇佣时，...（示例已截断）
```

---

### 约束条件

- `1 <= costs.length <= 10^5`
- `1 <= costs[i] <= 10^5`
- `1 <= k, candidates <= costs.length`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**逐轮模拟**招聘过程：  

1. 每轮从数组 `costs` 的左侧 `candidates` 个人和右侧 `candidates` 个人（如果两端重叠则只算一次）中挑选**费用最小**的工人。  
2. 把选中的费用加到总花费中，然后把该工人从数组中“移除”。  
3. 重复第 1、2 步 `k` 次，得到最终的总费用。  

> **类比**：把 `costs` 看成一排排队的顾客，左边的 `candidates` 人和右边的 `candidates` 人各自排成一个小队。每次我们都从这两个小队里挑出“最便宜的顾客”让他买东西。  

**为什么正确**：题目本身就要求每一轮都只能在这两个窗口里挑选最小费用的工人，暴力模拟正好把每一步都完整执行了一遍，自然能得到正确答案。  

**时间/空间分析**：  
- 每轮我们要遍历至多 `2 * candidates`（左+右）个元素找最小值，最坏情况下 `candidates` 可能等于 `n`（数组长度），于是每轮的时间是 `O(n)`。  
- 需要进行 `k` 轮，整体时间是 `O(k·n)`，在最坏情况下 `k` 也可能接近 `n`，所以最坏时间复杂度是 **O(n²)**。  
- 只使用了常数级的额外变量（如计数器、临时最小值），空间复杂度是 **O(1)**。  

> **大白话**：`O(n²)` 就像把一本 10 000 页的书的每一页都和后面的每一页比较一次，明显会很慢。

#### 代码（Python）  

```python
from typing import List

def totalCost_bruteforce(costs: List[int], k: int, candidates: int) -> int:
    n = len(costs)
    total = 0                     # 累计已经花费的总费用
    left = 0                      # 当前左窗口的起始下标
    right = n - 1                 # 当前右窗口的结束下标

    for _ in range(k):            # 进行 k 轮招聘
        # 计算本轮左侧可选的下标集合
        left_end = min(left + candidates - 1, right)   # 防止左窗口越过右窗口
        right_start = max(right - candidates + 1, left)  # 防止右窗口越过左窗口

        # 在左窗口中找最小费用及其下标
        min_cost = float('inf')
        min_idx = -1
        for i in range(left, left_end + 1):
            if costs[i] < min_cost:
                min_cost, min_idx = costs[i], i

        # 在右窗口中找最小费用（若右窗口与左窗口有交集则会再次比较）
        for i in range(right_start, right + 1):
            if costs[i] < min_cost:
                min_cost, min_idx = costs[i], i

        # 累加费用
        total += min_cost

        # 将选中的工人“移除”，相当于把窗口向内收缩
        if min_idx <= left_end:           # 选的是左窗口的工人
            left = min_idx + 1
        else:                             # 选的是右窗口的工人
            right = min_idx - 1

    return total
```

#### 复杂度  

- **时间复杂度**：`O(k·n)`，最坏情况下相当于 `O(n²)`，因为每轮都要线性扫描整个数组。  
- **空间复杂度**：`O(1)`，只用了几个额外的整数变量。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**每轮都要线性扫描**，这会导致 `O(n²)`。我们需要一种能**快速得到当前窗口最小费用**的数据结构。  

**最小堆（Min‑Heap）**恰好可以在 `O(log size)` 时间内取出最小元素，并在 `O(log size)` 时间内插入新元素。  
因此思路是：

1. **准备两个最小堆**  
   - `leftHeap` 保存左侧窗口的前 `candidates` 个人的费用（以及对应下标）。  
   - `rightHeap` 保存右侧窗口的后 `candidates` 个人的费用。  
   两个堆的元素形如 `(cost, index)`，这样在费用相同的情况下可以通过 `index` 自动实现“下标更小的优先”。  

2. **维护指针**  
   - `l` 指向左侧窗口已经加入堆的下一个下标（初始为 `candidates`）。  
   - `r` 指向右侧窗口已经加入堆的下一个下标（初始为 `n‑candidates‑1`）。  
   这两个指针帮助我们在每轮“弹出”一个工人后，**从未加入堆的部分继续补充**，保证两个堆始终各自不超过 `candidates` 个元素。

3. **每轮选人**  
   - 看 `leftHeap[0]`（左堆最小）和 `rightHeap[0]`（右堆最小）哪个更小（费用相同则下标更小的堆会先弹出，因为我们在堆里把 `index` 也放进去作比较）。  
   - 弹出更小的那个，累加费用。  
   - 弹出后，根据弹出的是左堆还是右堆，从对应的未加入区间（`l` 或 `r`）**再加入一个新元素**，保持窗口大小。  
   - 当 `l > r` 时，说明所有人已经全部进入堆，此时只需要继续弹出已有堆中的元素即可。

4. **结束**  
   重复 `k` 次后，返回累计的费用。  

**为什么正确**：  
- 堆始终只保存当前可以被挑选的工人集合（左侧 `candidates` 与右侧 `candidates`），这正是题目规定的“窗口”。  
- 每次取堆顶即是当前窗口中费用最小且下标最小的工人，符合题目“最小费用、下标优先”规则。  
- 通过指针 `l`、`r` 按顺序把未进入堆的工人补进去，保证**没有遗漏**且**不重复**。  

**类比**：想象左侧和右侧各有一个小型的“最低价商品货架”，每次我们只从两个货架的最便宜商品里挑一个买走，买走后货架上会补上新的商品（如果还有未上架的）。这样我们不需要每次去遍历所有商品，只需要关注两个小货架的最便宜商品。

#### 代码（Python）  

```python
import heapq
from typing import List

def totalCost(costs: List[int], k: int, candidates: int) -> int:
    n = len(costs)
    total = 0                         # 累计总费用

    # 两个堆：元素为 (cost, index) 方便在费用相同的情况下比较下标
    left_heap = []                    # 左侧窗口堆
    right_heap = []                   # 右侧窗口堆

    # 初始化左侧堆：前 candidates 个人（如果数组不够则全部加入）
    for i in range(min(candidates, n)):
        heapq.heappush(left_heap, (costs[i], i))
    # 初始化右侧堆：后 candidates 个人（注意避免与左侧重复加入）
    for i in range(max(n - candidates, 0), n):
        # 只在下标不在左堆已加入范围内时才加入
        if i >= candidates:
            heapq.heappush(right_heap, (costs[i], i))

    # 指针 l、r 指向下一个未加入堆的下标
    l = candidates                     # 左侧已加入的下一个下标
    r = n - candidates - 1             # 右侧已加入的下一个下标（从右往左）

    for _ in range(k):
        # 取两堆的堆顶（如果某堆为空则用一个极大值占位）
        left_min = left_heap[0] if left_heap else (float('inf'), -1)
        right_min = right_heap[0] if right_heap else (float('inf'), -1)

        # 费用更小者获选；费用相同则下标更小者先出（因为元组比较会先比较第一个，再比较第二个）
        if left_min <= right_min:
            cost, idx = heapq.heappop(left_heap)
            total += cost
            # 从左侧未加入区间补充一个新元素（如果还有剩余）
            if l <= r:
                heapq.heappush(left_heap, (costs[l], l))
                l += 1
        else:
            cost, idx = heapq.heappop(right_heap)
            total += cost
            # 从右侧未加入区间补充一个新元素
            if l <= r:
                heapq.heappush(right_heap, (costs[r], r))
                r -= 1

    return total
```

> **代码要点注释**  
> - `heapq` 是 Python 标准库里的最小堆实现，`heappush` 插入，`heappop` 弹出堆顶。  
> - 堆里存 `(cost, index)`，元组在比较时会先比较 `cost`，若相等再比较 `index`，正好实现“费用相同取下标更小”。  
> - `l <= r` 用来判断还有未加入堆的工人；当两指针交叉后，所有人已经在堆中，只需继续弹出即可。

#### 复杂度  

- **时间复杂度**：`O(k log candidates)`  
  - 每轮弹出堆顶和（可能）插入新元素各需 `O(log candidates)`，共 `k` 轮。  
  - 与暴力解的 `O(k·n)` 相比，**对数级的提升**让大数据量（如 `n=10⁵`）也能轻松跑完。  

- **空间复杂度**：`O(candidates)`  
  - 两个堆最多各保存 `candidates` 个元素，总共不超过 `2·candidates`，即 `O(candidates)` 级别的额外空间。  

---

## 心得  

- **核心技巧**：**使用两个最小堆维护可选区间**，并配合双指针动态补充新元素。  
- **适用的题型**  
  1. “从两端各选一定数量的元素，逐轮取最小/最大”——如 **LeetCode 2462**（本题）。  
  2. “在滑动窗口/固定大小窗口中实时获取最小/最大值”——如 **滑动窗口最大值**（LC 239）。  
  3. “多路合并排序”——如合并 `k` 条有序链表（LC 23），也常用最小堆。  
- **一句话总结**：**把“每轮最小”转化为堆的“堆顶”，用指针把未进入堆的元素按顺序补进来，即可在对数时间完成全部招聘。**  

---

## 反思  

- **第一反应**：直接把每轮的左、右 `candidates` 人全部遍历找最小，代码好写但显然会超时。  
- **最容易踩的坑**  
  - **窗口重叠**：当 `candidates * 2 > n` 时，左、右窗口会有交叉，需要在初始化和补充时避免重复加入同一个下标。  
  - **下标优先**：费用相同要选下标更小的工人，若只比较费用会得到错误答案。使用 `(cost, index)` 元组可以天然解决。  
  - **指针边界**：补充新元素时必须判断 `l <= r`，否则会把已经加入堆的元素再次加入，导致堆中出现重复。  
- **下次思路**：看到“每轮只在两端固定数量的元素中挑最小”时，立刻想到 **双堆 + 双指针**，先把两端的候选集合装进堆，之后只在堆顶操作，避免全数组遍历。