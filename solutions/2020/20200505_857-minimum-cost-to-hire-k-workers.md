# #857. 雇佣 K 名工人的最低成本 / Minimum Cost to Hire K Workers

> 难度：困难 · 标签：Array、Greedy、Sorting、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/minimum-cost-to-hire-k-workers/)

---

## 题目（英文原版）

**Description**

There are n workers. You are given two integer arrays quality and wage where quality[i] is the quality of the ith worker and wage[i] is the minimum wage expectation for the ith worker.
We want to hire exactly k workers to form a paid group. To hire a group of k workers, we must pay them according to the following rules:
Given the integer k, return the least amount of money needed to form a paid group satisfying the above conditions. Answers within 10-5 of the actual answer will be accepted.

**Examples**

**Example 1:**

```
Input: quality = [10,20,5], wage = [70,50,30], k = 2
Output: 105.00000
Explanation: We pay 70 to 0th worker and 35 to 2nd worker.
```

**Example 2:**

```
Input: quality = [3,1,10,10,1], wage = [4,8,2,2,7], k = 3
Output: 30.66667
Explanation: We pay 4 to 0th worker, 13.33333 to 2nd and 3rd workers separately.
```

**Constraints**

- n == quality.length == wage.length
- 1 <= k <= n <= 104
- 1 <= quality[i], wage[i] <= 104

---

## 题目（中文翻译）

有 **n** 名工人。给定两个整数数组 `quality` 与 `wage`，其中 `quality[i]` 表示第 **i** 名工人的质量（quality），`wage[i]` 表示第 **i** 名工人的最低工资期望（wage）。

我们需要恰好雇佣 **k** 名工人组成一个付费小组（paid group）。雇佣 **k** 名工人时，必须满足以下付费规则：

- 设付费比例为某个常数 `R`，则每位被雇佣工人的实际工资为 `quality[i] * R`。
- 对于每位被雇佣的工人，都必须满足 `quality[i] * R >= wage[i]`（即工资不低于其最低期望）。

给定整数 **k**，返回满足上述条件的付费小组所需的最小总费用。答案相对误差在 `10^-5` 以内均被视为正确。

**示例 1**  
**输入**: `quality = [10,20,5]`, `wage = [70,50,30]`, `k = 2`  
**输出**: `105.00000`  
**解释**: 我们给第 0 名工人支付 `70`，给第 2 名工人支付 `35`。

**示例 2**  
**输入**: `quality = [3,1,10,10,1]`, `wage = [4,8,2,2,7]`, `k = 3`  
**输出**: `30.66667`  
**解释**: 我们分别给第 0 名工人支付 `4`，给第 2、3 名工人各支付 `13.33333`。

**约束条件**  

- `n == quality.length == wage.length`
- `1 <= k <= n <= 10^4`
- `1 <= quality[i], wage[i] <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的 k 个人组合枚举一遍**，然后对每个组合计算出满足题目规则的最小付款。  

- **枚举组合**：把 `quality` 和 `wage` 看成两列对应的表格，任选 k 行（即 k 位工人）形成一个子集。  
- **计算最小工资**：  
  1. 对每位工人计算“性价比” `ratio = wage[i] / quality[i]`（每单位质量最少要付多少钱）。  
  2. 只要所有工人的工资都满足 “工资 = ratio × quality”，其中 `ratio` 必须不小于子集中每个人的 `ratio`，所以子集的 **最小可行 ratio** 就是子集中最大的 `ratio`。  
  3. 选定这个最大 ratio 后，总费用 = `max_ratio * (子集所有 quality 之和)`。  

因为我们已经遍历了所有子集，取最小的费用即为答案。  

> **为什么正确？**  
> 题目要求所有被雇佣的工人 **按同一比例**（即每单位质量的工资相同）付钱，且每个人的工资不能低于自己的最低期望 `wage[i]`。只要比例不小于子集中每个人的 `ratio`，所有约束都满足；而取最小的可能比例（即子集最大 `ratio`）显然能得到最小的总费用。

#### 代码（Python）

```python
import itertools
from typing import List

def mincost_bruteforce(quality: List[int], wage: List[int], k: int) -> float:
    n = len(quality)
    best = float('inf')

    # 1. 逐个枚举所有 k 人的组合（使用 itertools.combinations）
    for indices in itertools.combinations(range(n), k):
        # 2. 计算子集中的最大 ratio
        max_ratio = 0.0
        total_quality = 0
        for i in indices:
            ratio = wage[i] / quality[i]          # 每单位质量的最低工资
            max_ratio = max(max_ratio, ratio)      # 子集需要的最小统一比例
            total_quality += quality[i]            # 质量总和

        # 3. 用该比例算出总费用
        cost = max_ratio * total_quality
        best = min(best, cost)                     # 取最小值

    return best
```

> **关键行解释**  
> - `itertools.combinations(range(n), k)`：就像从 n 本书里挑出 k 本，列出所有可能的挑选方式。  
> - `wage[i] / quality[i]`：把工人的最低工资除以质量，得到“每质量要付多少钱”。  
> - `max(max_ratio, ratio)`：找出这 k 个人里最挑剔的那位（要求比例最高的），因为比例必须满足所有人。  

#### 复杂度  

- **时间复杂度**：  
  \[
  O\big(\binom{n}{k} \times k\big)
  \]  
  这里的 \(\binom{n}{k}\) 表示“从 n 个人里挑 k 个人有多少种方法”。例如 n=10，k=5 时约有 252 种组合，随着 n 增大组合数会呈指数级爆炸。  
- **空间复杂度**：  
  \[
  O(k)
  \]  
  只需要保存当前组合的质量和 ratio，总共不超过 k 个整数。

> **大白话**：暴力解相当于把所有可能的“人员名单”都写在纸上，一个个算费用，人数多了纸张就会炸掉，根本不可行。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**核心难点在于**：

1. **选出 k 个人**，而不是所有组合。  
2. **费用公式** = `max_ratio * sum_quality`，其中 `max_ratio` 必然是子集中 **最大的 ratio**（`wage/quality`）。

**观察**：如果我们把所有工人按照 `ratio = wage/quality` 从小到大排序，那么在遍历过程中：

- 当我们把第 `i` 个人（ratio 为 `r_i`）加入候选集合时，**所有已经遍历过的工人**的 ratio 都 **不大于** `r_i`。  
- 若把 `r_i` 设为当前组的 **最大 ratio**，则只要在已经遍历的工人里挑出 **质量最小的 k-1 位**（加上第 i 位共 k 人），就能得到 **最小的 sum_quality**，从而得到最小的费用 `r_i * sum_quality`。

**如何快速得到质量最小的 k-1 位？**  
使用一个**最大堆（max‑heap）**来维护当前已选的质量。堆里保存的是 **已挑选的质量值**，并且 **堆的大小不超过 k**。  
- 每次把新的质量 `q_i` 推入堆。  
- 若堆的大小超过 `k`，弹出堆中 **最大的质量**（因为我们想让质量总和尽可能小）。  
- 当堆的大小恰好等于 `k` 时，堆里保存的就是 **当前 ratio 为最大时，质量最小的 k 个人**。此时可以计算费用 `cost = r_i * sum_quality`，更新答案。

**整体步骤**：

1. 对每位工人计算 `ratio = wage[i] / quality[i]`，并把 `(ratio, quality[i])` 组成的元组放进列表。  
2. 按 `ratio` **升序**排序。  
3. 初始化一个 **最大堆**（在 Python 中用负数实现）和 `sum_quality = 0`。  
4. 依次遍历排好序的工人：
   - 把质量加入堆并累加到 `sum_quality`。  
   - 若堆大小 > k，弹出堆顶（最大质量），并相应地从 `sum_quality` 中减去。  
   - 当堆大小 == k 时，计算 `cost = ratio * sum_quality`，更新最小答案。  
5. 最后返回最小答案。

> **为什么这样是最优的？**  
> - 排序确保我们一次只考虑 **当前最大的 ratio**，不需要回溯。  
> - 堆保证在每个 ratio 下，**质量之和是最小的**（因为我们始终剔除最大的质量），从而得到全局最小费用。  
> - 整个过程只遍历一次列表，堆的每次插入/弹出是 `O(log k)`，整体时间 `O(n log n)`（排序）+ `O(n log k)`（堆），空间 `O(k)`。

#### 代码（Python）

```python
import heapq
from typing import List

def mincost_to_hire_k_workers(quality: List[int], wage: List[int], k: int) -> float:
    # 1. 计算每个人的 ratio = wage / quality，构成 (ratio, quality) 列表
    workers = [(w / q, q) for q, w in zip(quality, wage)]
    # 2. 按 ratio 从小到大排序
    workers.sort(key=lambda x: x[0])

    max_heap = []            # Python 没有 max‑heap，用负数模拟
    sum_quality = 0          # 当前堆中所有 quality 的和
    best = float('inf')      # 记录最小费用

    for ratio, q in workers:
        # 3. 把当前质量加入堆（负数实现 max‑heap）
        heapq.heappush(max_heap, -q)
        sum_quality += q

        # 4. 若堆里超过 k 人，弹出质量最大的那个人（即负数最小的元素）
        if len(max_heap) > k:
            removed = -heapq.heappop(max_heap)   # 取出真实的质量值
            sum_quality -= removed               # 更新质量总和

        # 5. 当堆正好有 k 人时，计算以当前 ratio 为最大比例的费用
        if len(max_heap) == k:
            cost = ratio * sum_quality
            best = min(best, cost)               # 取最小值

    return best
```

> **关键行解释**  
> - `workers = [(w / q, q) for q, w in zip(quality, wage)]`：把每位工人的“性价比”算出来，类似把每本书的“页数/重量”算好，方便后面排序。  
> - `heapq.heappush(max_heap, -q)`：把质量取负后放进最小堆，这样堆顶其实是 **最大的质量**（因为负数最小对应正数最大）。  
> - `if len(max_heap) > k: heapq.heappop(max_heap)`：当人数超过 k 时，把 **最贵的那位**（质量最大）踢出去，保持费用最小。  
> - `cost = ratio * sum_quality`：当前 ratio 已经是子集里最大的比例，乘以所有质量之和得到总工资。  

#### 复杂度  

- **时间复杂度**：  
  \[
  O\big(n \log n\big) \text{（排序)} + O\big(n \log k\big) \text{（堆操作)} = O\big(n \log n\big)
  \]  
  主要耗时在对 `n`（最多 10⁴）个工人排序，`log n` 大约是 14，完全可以接受。  
- **空间复杂度**：  
  \[
  O(k)
  \]  
  堆里最多保存 `k` 个质量值，`k ≤ n`，在最坏情况下是 O(n)，但一般只需要 O(k) 的额外空间。

> **对比暴力解**：暴力解的组合数随 `n` 指数增长，根本不可用；最优解只需一次排序和一个大小为 `k` 的堆，线性或对数级别的增长，能轻松跑完 10⁴ 条数据。

---

## 心得

- **核心技巧**：**把每位工人的最低工资转化为 “性价比 ratio = wage/quality”，然后利用排序 + 最大堆**，在每个可能的最大 ratio 下维护质量最小的 k 个人。  
- **适用场景**（类似题目）：
  1. “**最大化最小比率**”类问题，如 “Maximum Performance of a Team” (LeetCode 1383)。  
  2. “**在约束下选 k 项，求最小/最大代价**”的贪心 + 堆，如 “Find Minimum Number of Refueling Stops”。  
  3. “**按比例付费**”的变形，如 “Minimum Cost to Hire Workers with Different Skills”。  
- **一句话总结**：**把所有约束统一到一个比例上，排序后用堆挑最小质量，费用自然最小**。

---

## 反思

- **第一反应**：看到 “工资 ≥ wage[i]，且所有工资与质量成比例”，立刻想到 **每个人都有一个最小可接受的比例**，于是把问题转化为 “选 k 人，使 (最大比例) × (质量总和) 最小”。  
- **最容易踩的坑**：  
  1. **浮点精度**：`ratio` 是除法，需使用 `float`，最终答案要求误差 ≤ 1e‑5。  
  2. **堆的方向**：Python 只有最小堆，忘记取负数会导致 **保留最大质量** 而不是 **最小质量**。  
  3. **边界情况**：`k = 1` 时答案应是 `min(wage[i])`（因为比例 = wage/quality，费用 = ratio*quality = wage），代码仍然适用，只要堆大小恰好为 1。  
- **下次类似题的第一步**：  
  1. 把 “每个人的最小要求” 统一成 **单一指标**（如比例、单位成本等）。  
  2. 按该指标排序，**固定最大值**，再用 **堆/滑动窗口** 维护其余维度的最优子集。  

祝学习愉快，继续用“转化 + 排序 + 堆”这把钥匙打开更多算法大门！