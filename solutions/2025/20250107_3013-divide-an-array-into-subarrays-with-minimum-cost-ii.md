# #3013. 将数组划分为子数组的最小成本 II / Divide an Array Into Subarrays With Minimum Cost II

> 难度：困难 · 标签：Array、Hash Table、Sliding Window、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/divide-an-array-into-subarrays-with-minimum-cost-ii/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array of integers nums of length n, and two positive integers k and dist.
The cost of an array is the value of its first element. For example, the cost of [1,2,3] is 1 while the cost of [3,4,1] is 3.
You need to divide nums into k disjoint contiguous subarrays, such that the difference between the starting index of the second subarray and the starting index of the kth subarray should be less than or equal to dist. In other words, if you divide nums into the subarrays nums[0..(i1 - 1)], nums[i1..(i2 - 1)], ..., nums[ik-1..(n - 1)], then ik-1 - i1 <= dist.
Return the minimum possible sum of the cost of these subarrays.

**Examples**

**Example 1:**

```
Input: nums = [1,3,2,6,4,2], k = 3, dist = 3
Output: 5
Explanation: The best possible way to divide nums into 3 subarrays is: [1,3], [2,6,4], and [2]. This choice is valid because ik-1 - i1 is 5 - 2 = 3 which is equal to dist. The total cost is nums[0] + nums[2] + nums[5] which is 1 + 2 + 2 = 5.
It can be shown that there is no possible way to divide nums into 3 subarrays at a cost lower than 5.
```

**Example 2:**

```
Input: nums = [10,1,2,2,2,1], k = 4, dist = 3
Output: 15
Explanation: The best possible way to divide nums into 4 subarrays is: [10], [1], [2], and [2,2,1]. This choice is valid because ik-1 - i1 is 3 - 1 = 2 which is less than dist. The total cost is nums[0] + nums[1] + nums[2] + nums[3] which is 10 + 1 + 2 + 2 = 15.
The division [10], [1], [2,2,2], and [1] is not valid, because the difference between ik-1 and i1 is 5 - 1 = 4, which is greater than dist.
It can be shown that there is no possible way to divide nums into 4 subarrays at a cost lower than 15.
```

**Example 3:**

```
Input: nums = [10,8,18,9], k = 3, dist = 1
Output: 36
Explanation: The best possible way to divide nums into 4 subarrays is: [10], [8], and [18,9]. This choice is valid because ik-1 - i1 is 2 - 1 = 1 which is equal to dist.The total cost is nums[0] + nums[1] + nums[2] which is 10 + 8 + 18 = 36.
The division [10], [8,18], and [9] is not valid, because the difference between ik-1 and i1 is 3 - 1 = 2, which is greater than dist.
It can be shown that there is no possible way to divide nums into 3 subarrays at a cost lower than 36.
```

**Constraints**

- 3 <= n <= 105
- 1 <= nums[i] <= 109
- 3 <= k <= n
- k - 2 <= dist <= n - 2

---

## 题目（中文翻译）

给定一个 **0 索引** 的整数 **数组（array）** `nums`，长度为 `n`，以及两个正整数 `k` 和 `dist`。  
**子数组（subarray）** 的 **代价（cost）** 定义为其首元素的值。例如，`[1,2,3]` 的代价为 `1`，`[3,4,1]` 的代价为 `3`。  

需要将 `nums` 划分为 `k` 个 **不相交的连续子数组（disjoint contiguous subarrays）**，要求第 **2** 个子数组的起始下标与第 **k** 个子数组的起始下标之差不超过 `dist`。换句话说，若划分为  

```
nums[0 .. (i1‑1)], nums[i1 .. (i2‑1)], … , nums[ik‑1 .. (n‑1)]
```  

则必须满足 `ik‑1 - i1 <= dist`。  

返回这些子数组的代价之和的 **最小可能值**。

---

### 示例

**示例 1**  
``` 
Input: nums = [1,3,2,6,4,2], k = 3, dist = 3
Output: 5
Explanation: 将数组划分为 3 个子数组的最佳方案是 [1,3], [2,6,4] 和 [2]。此划分满足 ik‑1 - i1 = 5 - 2 = 3，等于 dist。总代价为 nums[0] + nums[2] + nums[5] = 1 + 2 + 2 = 5。可以证明不存在代价低于 5 的合法划分。
```

**示例 2**  
``` 
Input: nums = [10,1,2,2,2,1], k = 4, dist = 3
Output: 15
Explanation: 将数组划分为 4 个子数组的最佳方案是 [10], [1], [2], [2,2,1]。此划分满足 ik‑1 - i1 = 3 - 1 = 2 < dist。总代价为 nums[0] + nums[1] + nums[2] + nums[3] = 10 + 1 + 2 + 2 = 15。划分为 [10], [1], [2,2,2], [1] 不合法，因为其 ik‑1 与 i1 的差超过了 dist。
```

**示例 3**  
``` 
Input: nums = [10,8,18,9], k = 3, dist = 1
Output: 36
Explanation: 将数组划分为 3 个子数组的最佳方案是 [10], [8], [18,9]。此划分满足 ik‑1 - i1 = 2 - 1 = 1，等于 dist。总代价为 nums[0] + nums[1] + nums[2] = 10 + 8 + 18 = 36。划分为 [10], [8,18], [9] 不合法，因为 ik‑1 与 i1 的差为 3 - 1 = 2，超过了 dist。
```

---

### 约束

- `3 <= n <= 10^5`
- `1 <= nums[i] <= 10^9`
- `3 <= k <= n`
- `k - 2 <= dist <= n - 2`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法就是**把所有合法的划分枚举一遍**，然后求出每种划分的费用之和，取最小值。  

- **划分的表示**：把数组 `nums` 按下标切成 `k` 段，需要挑选 `k‑1` 个切分点  
  \[
  i_1,i_2,\dots,i_{k-1}
  \]
  其中 `i_1` 是第二段的起始下标，`i_{k-1}` 是第 `k` 段的起始下标。  
- **合法性**：必须满足  
  \[
  i_{k-1}-i_1 \le \text{dist}
  \]
  也就是说，第二段的起点和倒数第二段的起点之间的距离不能超过 `dist`。  
- **费用**：每段子数组的费用等于它的第一个元素，所以一次划分的总费用是  
  \[
  \text{cost}=nums[0]+nums[i_1]+nums[i_2]+\dots+nums[i_{k-1}]
  \]

把所有满足 `i_{k-1}-i_1 ≤ dist` 的 `(i_1,…,i_{k-1})` 组合都遍历一遍，就能得到答案。

> **生活化类比**：想象你在超市挑选 `k‑1` 件商品（每件商品对应一个子数组的起点），必须保证第一件和最后一件之间的货架距离不超过 `dist`，然后把所有商品的价格相加，找出最便宜的组合。

**为什么正确**：因为我们把**所有可能**的合法划分都考虑到了，最小的费用必然出现在这些枚举中。

**时间/空间分析**：  
- 枚举 `k‑1` 个切分点相当于在长度为 `n` 的数组里挑选 `k‑1` 个位置，组合数是 \(\binom{n}{k-1}\)。  
- 对每一种组合我们要计算一次费用，时间复杂度就是 **O( C(n,k‑1) )**，在最坏情况下接近 **O(n^{k-1})**（指数级）。  
- 只需要常数级的额外空间来保存当前的切分点，空间复杂度 **O(1)**。  

显然，这种暴力办法在 `n` 最高可达 `10^5`、`k` 也可能很大时根本不可行，只能作为思考的起点。

#### 代码（Python）

```python
from itertools import combinations
from typing import List

def minCost_bruteforce(nums: List[int], k: int, dist: int) -> int:
    n = len(nums)
    best = float('inf')
    # i1 ... i_{k-1} 必须是递增的切分点
    for cuts in combinations(range(1, n), k - 1):      # 0 号位置固定是第一段起点
        i1, *mid, ik_1 = cuts
        # 合法性检查
        if ik_1 - i1 > dist:
            continue
        # 费用 = 第一个元素 + 所有切分点对应的元素
        cur = nums[0] + sum(nums[pos] for pos in cuts)
        best = min(best, cur)
    return best
```

> 代码里用 `itertools.combinations` 把所有切分点枚举出来，实际运行只能通过极小的测试数据。

#### 复杂度  

- **时间复杂度**：`O( C(n, k-1) )` ≈ `O(n^{k-1})`（指数级），在大输入下会超时。  
- **空间复杂度**：`O(1)`（只用常数级的临时变量），不随 `n` 增长。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**费用只和每段的第一个元素有关**。  
我们把 `nums[0]` 固定为第一段的费用，剩下的 `k‑1` 个费用只取自数组中除 `0` 之外的若干位置。  

把第二段的起点记作 `i`（即 `i = i1`），则后面还要再选 `k‑2` 个起点，这 `k‑2` 个位置必须全部落在区间  

\[
[i+1,\; \min(i+{\text{dist}},\; n-1)]
\]

因为 `i_{k-1}`（倒数第二段的起点）必须在 `i+dist` 之内，才能满足 `i_{k-1}-i ≤ dist`。  

> **关键观察**：  
> 对于固定的 `i`，我们只需要在上述窗口里挑 **最小的 `k‑2` 个 `nums` 值**，把它们加到 `nums[0] + nums[i]` 上即可得到该 `i` 对应的最小费用。  
> 因此答案是  
> \[
> \min_{i\in[1,n-1]} \bigl( nums[0] + nums[i] + \text{(窗口中最小 $k-2$ 元素之和)} \bigr)
> \]

于是问题转化为：**在一个滑动窗口上，动态维护“窗口中最小的 `m = k-2` 个数的和”**，并且窗口大小随 `i` 右移而变化（左端是 `i+1`，右端是 `i+dist`）。

#### 如何维护窗口的最小 `m` 个数  

常用的技巧是 **两堆（双堆）**：

1. **max‑heap `small`**（在 Python 中用负数实现）  
   - 保存当前窗口里 **最小的 `m` 个数**。  
   - 因为是最大堆，堆顶是这 `m` 个数里最大的，也就是“第 `m` 小”的那个数。  
   - 同时维护 `small_sum`，记录 `small` 中所有数的总和。

2. **min‑heap `large`**  
   - 保存窗口里 **其余的数**（比 `small` 中的数都大）。  
   - 堆顶是窗口里最小的“大数”，方便在 `small` 不够 `m` 时补进去。

**插入新元素** `x`：  
- 先把 `x` 放进 `small`，`small_sum += x`。  
- 如果 `small` 的大小超过 `m`，把堆顶（最大值）弹出，放进 `large`，并相应地从 `small_sum` 减去弹出的值。  

**删除离开窗口的元素** `x`：  
- 直接从对应的堆里标记为“已删除”。因为 Python 堆不支持任意删除，我们用一个字典 `del_cnt` 记录待删除的值出现次数，随后在弹出堆顶时“懒惰”清除。  
- 若 `x` 本来在 `small` 中，需要把 `small_sum` 减去 `x`，并让 `small` 的大小变小 1；随后如果 `small` 的大小小于 `m`，就把 `large` 的堆顶弹出放进 `small`，补齐 `m` 并更新 `small_sum`。  

**平衡两堆**：  
- 只要 `small` 的大小大于 `m`，就把多余的最大值搬到 `large`。  
- 只要 `small` 的大小小于 `m`，就把 `large` 的最小值搬进 `small`。  
- 这两个步骤每次最多 O(log size) 时间。

通过上述操作，**每次窗口滑动只需要 O(log k) 的代价**，而我们只要遍历一次 `i`（即第二段起点），即可得到答案。

#### 步骤概览  

1. 预处理：`m = k-2`（若 `m == 0`，直接返回 `nums[0] + min(nums[1:])`）。  
2. 初始化窗口为 `[2, min(dist+1, n-1)]`（对应 `i = 1` 时的窗口），把这些元素全部加入双堆，并保持 `small` 的大小不超过 `m`。  
3. 对每个可能的 `i`（从 `1` 到 `n-1`）  
   - 计算当前费用 `cur = nums[0] + nums[i] + small_sum`（如果 `m>0`），更新全局最小答案。  
   - 将窗口右端向右移动一位（如果仍在数组范围内），把新元素加入双堆。  
   - 将窗口左端（`i+1`）对应的元素移出窗口（如果左端已经在窗口里），在双堆中标记删除并平衡。  
4. 最后返回记录的最小费用。

> **类比**：把 `small` 想成“装最便宜商品的购物篮”，容量恰好是 `m`。`large` 是“仓库”，放着剩下的商品。每次超市上新商品（窗口右端）进来时，我们先把它放进篮子；如果篮子满了，就把最贵的商品搬到仓库。每次有商品下架（窗口左端）时，如果它在篮子里，我们把它从篮子里拿走，空出位置再从仓库挑最便宜的补进篮子。这样，篮子里始终保持当前窗口里最便宜的 `m` 件商品。

#### 代码（Python）

```python
import heapq
from collections import defaultdict
from typing import List

def minCost(nums: List[int], k: int, dist: int) -> int:
    """
    返回把 nums 分成 k 段，使得
    i_{k-1} - i_1 <= dist 时费用的最小可能和。
    费用 = 每段的首元素之和。
    """
    n = len(nums)
    m = k - 2                      # 需要在窗口中挑选的最小元素个数

    # 特殊情况：如果 m == 0，说明只需要两段——第一段固定起点 0，第二段任意起点即可
    if m == 0:
        # 第二段起点只能是 i (1 <= i < n)，而没有其它约束
        return nums[0] + min(nums[1:])

    # ---------- 双堆结构 ----------
    small = []                     # max‑heap（存负数），保存最小的 m 个数
    large = []                     # min‑heap，保存其余数
    del_cnt = defaultdict(int)    # 懒删除计数
    small_sum = 0                  # small 中所有数的和

    def push(val: int):
        """把 val 放进双堆并保持 small 的大小不超过 m"""
        nonlocal small_sum
        heapq.heappush(small, -val)   # max‑heap 用负数实现
        small_sum += val
        # 若 small 超出容量，搬走最大值到 large
        if len(small) > m:
            max_small = -heapq.heappop(small)
            small_sum -= max_small
            heapq.heappush(large, max_small)

    def erase(val: int):
        """标记窗口中要删除的 val"""
        nonlocal small_sum
        del_cnt[val] += 1
        # 判断它原本在 small 还是 large（通过比较堆顶实现）
        if small and val <= -small[0]:
            # 在 small 中
            small_sum -= val
        # 否则在 large 中，直接懒删即可

    def clean(heap):
        """弹出堆顶的已删除元素，返回有效的堆顶值（不弹出）"""
        while heap:
            top = -heap[0] if heap is small else heap[0]
            if del_cnt[top]:
                # 该元素已经在窗口外，真正删除
                heapq.heappop(heap)
                del_cnt[top] -= 1
                if del_cnt[top] == 0:
                    del_cnt.pop(top)
            else:
                break

    def balance():
        """保证 small 的大小恰好是 m（如果窗口内元素不足 m，则全部放在 small）"""
        nonlocal small_sum
        # 先把两堆的已删除元素清理干净
        clean(small)
        clean(large)

        # small 可能太小，需要从 large 补充
        while len(small) < m and large:
            # 把 large 中最小的搬到 small
            val = heapq.heappop(large)
            heapq.heappush(small, -val)
            small_sum += val

        # small 可能太大，需要搬出最大值到 large
        while len(small) > m:
            val = -heapq.heappop(small)
            small_sum -= val
            heapq.heappush(large, val)

    # ---------- 初始化窗口 ----------
    # i = 1 时窗口是 [2, min(1+dist, n-1)]
    left = 2
    right = min(1 + dist, n - 1)
    for idx in range(left, right + 1):
        push(nums[idx])

    ans = float('inf')
    # ---------- 主循环：遍历第二段的起点 i ----------
    for i in range(1, n):
        # 当前窗口已经对应于 i 的合法范围
        if len(small) < m:          # 窗口元素不足 m，说明此 i 不可能构成合法划分
            # 仍需移动窗口，但不更新答案
            pass
        else:
            cur = nums[0] + nums[i] + small_sum
            ans = min(ans, cur)

        # ----- 移动窗口到下一个 i+1 -----
        # 1) 右端向右扩展（如果还能扩展的话）
        new_right = i + dist + 1
        if new_right < n:
            push(nums[new_right])

        # 2) 左端收缩：左端原来是 i+1，下一轮左端应该是 (i+1)+1 = i+2
        old_left = i + 1
        if old_left <= n - 1:
            erase(nums[old_left])

        # 3) 重新平衡两堆
        balance()

    return ans
```

> **代码要点解释**  
> * `push`：把新进窗口的数加入 `small`，如果 `small` 超容量就把最大值搬到 `large`。  
> * `erase`：使用 `del_cnt` 做**懒删除**，因为 Python 堆不支持直接删任意元素。  
> * `clean`：在每次需要读取堆顶时，先把已经标记删除的元素真正弹出。  
> * `balance`：确保 `small` 恰好保留窗口中最小的 `m` 个数，并维护 `small_sum`。  
> * 主循环中先计算答案（前提是窗口里已经有足够的元素），再更新窗口（右移一位、左移一位），最后平衡堆。

#### 复杂度  

- **时间复杂度**：  
  - 主循环遍历 `i` 一共 `n` 次。  
  - 每次插入、删除、平衡堆的操作都是 `O(log k)`（堆的大小至多 `dist+1 ≤ n`，但实际只会保留 `m = k-2` 个在 `small`，其余在 `large`），所以整体 **O(n log k)**。  
  - 对比暴力的指数级，这已经是可以接受的。

- **空间复杂度**：  
  - 两个堆最多各保存 `O(dist)` 个元素，`dist ≤ n`，但实际只会占用 `O(k)`（因为 `small` 只需要 `k-2`，`large` 只剩下窗口其余的）。  
  - 再加上 `del_cnt` 字典，整体 **O(k + dist)**，在最坏情况下为 **O(n)**，但仍远小于暴力的记忆需求。

---

## 心得  

- **核心技巧**：在滑动窗口里维护“**最小的 m 个数的和**”，使用**双堆 + 懒删除**实现。  
- **适用的题型**：  
  1. “在区间/窗口内求前 `m` 小/大的元素之和”——如 LeetCode 2391 “Maximum Sum of Subsequence With Minimum Cost”。  
  2. “窗口内动态维护 Top‑K 元素”——如 “Sliding Window Median”。  
  3. “需要在约束范围内挑选若干最小（大）值”——如 “Divide an Array Into Subarrays With Minimum Cost I/II”。  
- **一句话总结**：**把“挑最小的 k 个数”转化为双堆结构，配合滑动窗口的增删，即可在 O(n log k) 内得到最优解。**

---

## 反思  

- **第一反应**：看到“费用是子数组的第一个元素”，立刻想到只要选好每段的起点即可，随后把约束转化为“在一个固定长度的窗口里挑最小的 `k‑2` 个数”。  
- **最容易踩的坑**：  
  - **窗口边界**：`i+dist` 可能超过数组末尾，需要 `min` 处理。  
  - **`k‑2 = 0` 的特殊情况**：此时不需要双堆，直接取最小的第二段起点即可。  
  - **堆的删除**：直接 `heap.remove` 会导致 `O(n)`，必须使用懒删除配合字典。  
  - **平衡后堆可能为空**：在窗口元素不足 `k‑2` 时要跳过答案更新。  
- **下次类似题**：第一步先**抽象出“只关心起点的值”，看能否把约束转化为“在某个滑动区间内挑最小（大）`m` 个”。如果可以，立刻考虑 **双堆+懒删** 或 **有序容器** 来高效维护。