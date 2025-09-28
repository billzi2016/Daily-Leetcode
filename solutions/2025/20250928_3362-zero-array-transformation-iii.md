# #3362. 零数组转换 III / Zero Array Transformation III

> 难度：中等 · 标签：Array、Greedy、Sorting、Heap (Priority Queue)、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/zero-array-transformation-iii/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums of length n and a 2D array queries where queries[i] = [li, ri].
Each queries[i] represents the following action on nums:
A Zero Array is an array with all its elements equal to 0.
Return the maximum number of elements that can be removed from queries, such that nums can still be converted to a zero array using the remaining queries. If it is not possible to convert nums to a zero array, return -1.

**Examples**

**Example 1:**

```
Input: nums = [2,0,2], queries = [[0,2],[0,2],[1,1]]
Output: 1
Explanation:
After removing queries[2] , nums can still be converted to a zero array.
```

**Example 2:**

```
Input: nums = [1,1,1,1], queries = [[1,3],[0,2],[1,3],[1,2]]
Output: 2
Explanation:
We can remove queries[2] and queries[3] .
```

**Example 3:**

```
Input: nums = [1,2,3,4], queries = [[0,3]]
Output: -1
Explanation:
nums cannot be converted to a zero array even after using all the queries.
```

**Constraints**

- 1 <= nums.length <= 105
- 0 <= nums[i] <= 105
- 1 <= queries.length <= 105
- queries[i].length == 2
- 0 <= li <= ri < nums.length

---

## 题目（中文翻译）

给定一个长度为 `n` 的整数数组 `nums` 与一个二维数组 `queries`，其中 `queries[i] = [l_i, r_i]`。  
每个 `queries[i]` 表示对 `nums` 执行一次如下操作：

- **零数组**（Zero Array）是指所有元素均为 `0` 的数组。

返回可以从 `queries` 中删除的最大查询数目，使得在仅使用剩余的查询时仍能将 `nums` 转换为零数组。如果无论如何都无法将 `nums` 转换为零数组，返回 `-1`。

---

### 示例

#### 示例 1
```
输入: nums = [2,0,2], queries = [[0,2],[0,2],[1,1]]
输出: 1
解释:
删除 `queries[2]` 后，仍然可以通过剩余的查询将 `nums` 变为零数组。
```

#### 示例 2
```
输入: nums = [1,1,1,1], queries = [[1,3],[0,2],[1,3],[1,2]]
输出: 2
解释:
我们可以删除 `queries[2]` 和 `queries[3]`。
```

#### 示例 3
```
输入: nums = [1,2,3,4], queries = [[0,3]]
输出: -1
解释:
即使使用所有查询，也无法将 `nums` 转换为零数组。
```

---

### 约束条件
- `1 <= nums.length <= 10^5`
- `0 <= nums[i] <= 10^5`
- `1 <= queries.length <= 10^5`
- `queries[i].length == 2`
- `0 <= l_i <= r_i < nums.length`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每一个查询都看成可以使用或不使用的开关**。  
- 对于每一种“开/关”组合（即子集），我们把被选中的查询全部执行一次，看看最终数组是否全变成 0。  
- 如果可以，就统计这次删除了多少查询（总查询数 - 使用的查询数），取最大值。

**用到的数据结构**  
- **子集**：相当于把所有查询排成一本字典，`key` 是查询的下标，`value` 是“使用”还是“删除”。  
- **数组模拟**：把每一次查询对区间 `[l, r]` 的操作看成在数组上做 `+1`（因为每次操作会把区间里每个元素减 1，等价于在需求上加 1），最后检查每个位置的累计值是否恰好等于 `nums[i]`。  

**为什么这个方法正确**  
- 我们遍历了**所有可能的使用集合**，只要有一种方式能够满足每个位置的需求，就一定会被检测到。  

**时间/空间复杂度**  
- 假设有 `m = len(queries)` 个查询。子集的数量是 `2^m`，每个子集需要遍历整个数组（`n`）来累计区间增量。  
- **时间复杂度**：`O( 2^m * n )`，指数级增长。可以把 `2^m` 想象成“每增加一个查询，就把工作量翻一倍”，所以即使 `m=20`（约一百万种组合），也会非常慢。  
- **空间复杂度**：`O(n)` 用来保存临时的增量数组。  

> 这个暴力解只能用来验证思路或在 **极小规模**（比如 `n,m ≤ 10`）时跑通。真正的题目要求 `n,m ≤ 10^5`，必须找更快的办法。

#### 代码（Python）  

```python
from itertools import combinations
from copy import deepcopy

def brute_force(nums, queries):
    n, m = len(nums), len(queries)
    best_remove = -1                     # 最多可以删除的查询数
    # 枚举所有可能的“使用的查询”集合（子集）
    for k in range(m + 1):
        for used_idx in combinations(range(m), k):
            # 先把需求拷贝一份
            need = deepcopy(nums)
            # 对每个被使用的查询，在它的区间里把需求减 1
            for idx in used_idx:
                l, r = queries[idx]
                for i in range(l, r + 1):
                    need[i] -= 1
            # 检查是否全部变成 0（或更小，说明多余的操作也算合法）
            if all(v == 0 for v in need):
                # 删除的查询数 = 总数 - 使用的数量
                best_remove = max(best_remove, m - k)
    return best_remove
```

#### 复杂度  

- **时间复杂度**：`O(2^m * n)`，指数级，实际只能跑极小数据。  
- **空间复杂度**：`O(n)`，保存临时需求数组。  

---

### 2. 最优解  

#### 思路  

从暴力解出发，我们可以看到**“每个位置 i 必须被至少 `nums[i]` 次查询覆盖”**。  
如果把每一次查询想象成“一块能覆盖区间 `[l, r]` 的布”，我们的问题就变成：

> 用最少块布（查询）来覆盖每个位置的需求 `nums[i]`，每块布只能用一次。

**慢点在哪里**  
- 暴力遍历所有子集显然不可行。  
- 即使只想“尽可能少用查询”，我们仍然需要快速判断在遍历数组的过程中，**当前还能选哪些查询**。

**关键观察**  
1. 当我们处理位置 `i` 时，只会用到 **左端点 ≤ i** 的查询（因为左端点更大的查询根本不覆盖 `i`）。  
2. 为了让同一块查询尽可能帮助后面的很多位置，我们应该**优先挑选右端点最远的查询**。这样它在满足当前需求的同时，还能为后面的需求提供最大“余量”。  

这正是**贪心 + 优先队列（堆）**的典型思路：

- **按左端点升序**把所有查询排好序，准备逐个“放进”一个堆。  
- 维护一个 **最大堆（按右端点）**，堆里保存所有左端点已经 ≤ 当前位置 `i` 的查询。  
- 用一个 **差分数组 `diff`** 来记录已经选中的查询对后续位置的贡献。遍历数组时，用 `cur_cover` 累加 `diff`，得到 **已经被覆盖的次数**。  
- 当前位置 `i` 还缺多少次覆盖？`need = nums[i] - cur_cover`（若为负则取 0）。  
- 当 `need > 0` 时，**从堆中弹出右端点最大的查询**，把它标记为“已使用”，并在 `diff[l] += 1, diff[r+1] -= 1`（相当于给后面的 `cur_cover` 加 1）。弹出一次就满足一次需求，循环直到 `need == 0`。  
- 如果堆已经空了，说明没有任何可用查询能够覆盖当前位置，**题目无解，返回 -1**。

**为什么这个贪心是正确的**  

- **局部最优 → 全局最优**：在位置 `i` 必须补足 `need` 次时，任选 `need` 条查询只要它们的右端点 ≥ i 即可。若我们不选右端点最大的那条，而是选一条右端点更小的，那么这条小的查询在以后 **更早** 失效，可能导致后面的某个位置缺少必要的覆盖。换句话说，把“最远的布”留给以后，是对后面需求最安全的做法。  
- **交换论证**：设想最优解中在位置 `i` 使用了一条右端点为 `r1` 的查询，而我们贪心选了一条右端点为 `r2 (≥ r1)` 的查询。把这两条查询在解中互换位置，仍然能满足当前位置的需求，并且不会让后面的任何位置变得更差，因为 `r2` 能覆盖的范围不比 `r1` 小。于是可以把任意最优解改造成与贪心相同的形式，说明贪心得到的解也是最优的。  

**算法步骤（伪代码）**  

```
sort queries by left endpoint
heap = empty max‑heap (store (right, left))
diff = [0] * (n + 1)          # 差分数组
cur_cover = 0                # 当前 i 已经被覆盖的次数
used = 0                     # 选中的查询数量
ptr = 0                      # 指向排序后 queries 的指针

for i in 0 .. n-1:
    # 把左端点 ≤ i 的查询全部加入堆
    while ptr < m and queries[ptr].l <= i:
        push heap with (queries[ptr].r, queries[ptr].l)
        ptr += 1

    cur_cover += diff[i]      # 累计到当前位置的覆盖次数
    need = max(0, nums[i] - cur_cover)

    while need > 0:
        if heap empty: return -1          # 没法满足需求
        r, l = pop heap (rightmost interval)
        # 选这条查询
        used += 1
        diff[l] += 1
        diff[r + 1] -= 1
        cur_cover += 1          # 这条查询立刻对当前位置生效
        need -= 1
```

最后答案 = `len(queries) - used`（总查询数减去必须保留的最小数量）。

**核心技巧**  
- **差分数组**让我们在 **O(1)** 时间内把一次区间增量记下来，随后在遍历时累计得到每个位置的实际覆盖次数。  
- **最大堆**实现“取右端点最远的查询”这一贪心步骤，时间为 `O(log m)`。  

#### 代码（Python）  

```python
import heapq
from typing import List

def max_removed_queries(nums: List[int], queries: List[List[int]]) -> int:
    n = len(nums)
    m = len(queries)

    # 1) 按左端点升序排序，方便一次遍历加入堆
    queries_sorted = sorted(queries, key=lambda x: x[0])

    # 2) max‑heap：Python 的 heapq 是 min‑heap，取负数实现 max‑heap
    max_heap = []                     # 元素为 (-right, left)

    diff = [0] * (n + 1)              # 差分数组，记录已选查询的区间贡献
    cur_cover = 0                     # 当前 i 已经被覆盖的次数
    used = 0                          # 必须保留的查询数量
    ptr = 0                           # 指向排序后 queries 的指针

    for i in range(n):
        # 把所有左端点 <= i 的查询放进堆
        while ptr < m and queries_sorted[ptr][0] <= i:
            l, r = queries_sorted[ptr]
            heapq.heappush(max_heap, (-r, l))   # -r 让堆顶是右端点最大的
            ptr += 1

        # 累计差分得到当前位置已有的覆盖次数
        cur_cover += diff[i]

        # 仍然缺多少次覆盖？
        need = nums[i] - cur_cover
        if need < 0:
            need = 0

        # 贪心选取右端点最远的查询，直到需求满足
        while need > 0:
            if not max_heap:            # 没有可用查询，直接返回 -1
                return -1
            neg_r, l = heapq.heappop(max_heap)
            r = -neg_r
            # 选这条查询 → 在差分数组上做一次区间 +1
            diff[l] += 1
            if r + 1 <= n:
                diff[r + 1] -= 1
            used += 1
            cur_cover += 1               # 立刻对当前位置生效
            need -= 1

    # 所有位置需求都已满足
    return m - used                     # 可以删除的最多查询数
```

> **代码解释（中文注释）**已写在关键行旁，直接复制粘贴即可运行。

#### 复杂度  

- **时间复杂度**：`O( (n + m) * log m )`  
  - 每个查询只会被一次 `push`、一次 `pop`，每次操作 `log m`。  
  - 其余的遍历 `n` 次的累加和差分都是 `O(1)`。  
  - 与暴力解的指数级相比，这在 `10^5` 规模下完全可接受。  

- **空间复杂度**：`O(n + m)`  
  - `diff` 长度 `n+1`，堆里最多存 `m` 条查询。  
  - 相比 `O(n*m)` 的暴力存储，这只是线性空间。  

---

## 心得  

- **核心技巧**：把“每次查询覆盖区间”抽象为**区间增量**，用**差分数组**快速累计；再结合**最大堆**实现“右端点最远优先”的贪心。  
- **适用题型**  
  1. **区间覆盖最少集合**（如 “最少灯泡点亮全路段”）  
  2. **区间调度/资源分配**（如 “给每个时间段分配最少机器”）  
  3. **前缀和/差分+贪心** 的组合题目（如 “使数组全为 0 的最少操作”）  

> **一句话总结解题钥匙**：  
> “在满足当前位置需求时，始终选取能够覆盖最远右端点的查询”，配合差分数组即可在 **O((n+m)log m)** 完成全局最优。

---

## 反思  

- **第一反应**：看到“区间查询”就想到**前缀和**或**差分**，但最初会忽略“每个查询只能用一次”，导致把问题误当成“无限次使用”。  
- **最容易踩的坑**  
  1. **堆里弹出的查询右端点可能小于当前 i**：如果不检查，会产生负贡献。实现时只把左端点 ≤ i 的查询加入堆，右端点自然 ≥ i（因为左 ≤ i ≤ right），所以不需要额外检查。  
  2. **差分数组越界**：对 `diff[r+1]` 必须先判断 `r+1 ≤ n`，否则会访问越界。  
  3. **需求为 0 时仍然错误地弹出堆**：记得 `need = max(0, nums[i] - cur_cover)`，避免负数导致不必要的弹出。  

- **下次遇到同类题**：  
  1. **先把需求转化为“每个位置需要被覆盖多少次”。**  
  2. **把区间操作抽象为差分/前缀和**，这样可以在遍历时实时得到当前的覆盖次数。  
  3. **用贪心+堆**，在遍历位置时挑选“最远右端点”的区间，以保证后续需求尽可能被同一条区间覆盖。  

这样一步步拆解，既能保证正确性，又能写出高效的实现。祝你玩转区间贪心！