# #3080. Mark Elements on Array by Performing Queries / Mark Elements on Array by Performing Queries

> 难度：中等 · 标签：Array、Hash Table、Sorting、Heap (Priority Queue)、Simulation · [LeetCode 链接](https://leetcode.com/problems/mark-elements-on-array-by-performing-queries/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array nums of size n consisting of positive integers.
You are also given a 2D array queries of size m where queries[i] = [indexi, ki].
Initially all elements of the array are unmarked.
You need to apply m queries on the array in order, where on the ith query you do the following:
Return an array answer of size m where answer[i] is the sum of unmarked elements in the array after the ith query.

**Examples**

**Example 1:**

```
Input: nums = [1,2,2,1,2,3,1], queries = [[1,2],[3,3],[4,2]]
Output: [8,3,0]
Explanation:
We do the following queries on the array:
```

**Example 2:**

```
Input: nums = [1,4,2,3], queries = [[0,1]]
Output: [7]
Explanation: We do one query which is mark the element at index 0 and mark the smallest element among unmarked elements. The marked elements will be nums = [ 1 ,4, 2 ,3] , and the sum of unmarked elements is 4 + 3 = 7 .
```

**Constraints**

- n == nums.length
- m == queries.length
- 1 <= m <= n <= 105
- 1 <= nums[i] <= 105
- queries[i].length == 2
- 0 <= indexi, ki <= n - 1

---

## 题目（中文翻译）

给定一个下标从 **0** 开始的数组 `nums`，长度为 `n`，其中所有元素为正整数。  
同时给定一个大小为 `m` 的二维数组 `queries`，其中 `queries[i] = [index_i, k_i]`。  
最初数组中的所有元素均 **未标记**。  

你需要按顺序对数组执行 `m` 次查询。在第 `i` 次查询中，依次执行以下操作：

1. 将下标为 `index_i` 的元素标记。  
2. 在剩余未标记的元素中，找到第 `k_i` 小的元素并标记（若有多个相同值，任选其一）。

返回一个大小为 `m` 的数组 `answer`，其中 `answer[i]` 为第 `i` 次查询后数组中 **未标记** 元素的和。

---

### 示例

#### 示例 1
**输入**  
```text
nums = [1,2,2,1,2,3,1], queries = [[1,2],[3,3],[4,2]]
```
**输出**  
```text
[8,3,0]
```
**解释**  
我们按顺序对数组执行上述查询：

* 第一次查询 `[1,2]`：标记下标 `1` 的元素 `2`，并标记未标记元素中的第 2 小的元素。  
* 第二次查询 `[3,3]`：标记下标 `3` 的元素 `1`，并标记未标记元素中的第 3 小的元素。  
* 第三次查询 `[4,2]`：标记下标 `4` 的元素 `2`，并标记未标记元素中的第 2 小的元素。  

每次查询后未标记元素的和分别为 `8、3、0`，因此 `answer = [8,3,0]`。

#### 示例 2
**输入**  
```text
nums = [1,4,2,3], queries = [[0,1]]
```
**输出**  
```text
[7]
```
**解释**  
我们执行唯一的一次查询：

* 标记下标 `0` 的元素 `1`。  
* 在剩余未标记的元素 `[4,2,3]` 中，标记第 1 小的元素（即最小的 `2`）。  

此时未标记的元素为 `[4,3]`，它们的和为 `4 + 3 = 7`，所以 `answer = [7]`。

---

### 约束条件
- `n == nums.length`
- `m == queries.length`
- `1 <= m <= n <= 10^5`
- `1 <= nums[i] <= 10^5`
- `queries[i].length == 2`
- `0 <= index_i, k_i <= n - 1`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **一次一次地模拟** 题目给出的操作：

1. 维护一个 `marked` 数组，`marked[i] = True` 表示 `nums[i]` 已经被标记。  
2. 对每个查询 `[idx, k]`  
   - 先把 `idx` 位置的元素标记（如果之前已经标记则不做任何事）。  
   - 再在 **所有仍未标记的元素** 中挑出数值最小的 `k` 个标记。  
   - 计算剩余（未标记）元素的总和，保存到答案数组中。

> **类比**：把 `marked` 看成一本字典，`key` 是下标，`value` 是“是否已经划线”。  
> 找最小的 `k` 个元素就像在字典里挑出最靠前的 `k` 条记录——最直白的办法是把所有未划线的记录拿出来排个序，然后取前 `k` 条。

> **为什么一定对**：我们完全按照题目描述的步骤去做，没有任何近似或偷懒，所有的标记和求和都是真实的，答案必然正确。

#### 代码（Python）

```python
def markElements(nums, queries):
    n = len(nums)
    marked = [False] * n                # 记录每个下标是否已被标记
    total = sum(nums)                    # 当前未标记元素的和
    ans = []

    for idx, k in queries:
        # 1) 标记查询给出的下标
        if not marked[idx]:
            marked[idx] = True
            total -= nums[idx]           # 从总和里减去被标记的值

        # 2) 找出当前未标记的最小 k 个元素并标记
        #   先把所有未标记的元素收集起来，按数值排序
        unmarked_vals = [(nums[i], i) for i in range(n) if not marked[i]]
        unmarked_vals.sort()             # 按数值从小到大

        # 取前 k 个（如果不足 k，则全部取）
        for _ in range(min(k, len(unmarked_vals))):
            val, i = unmarked_vals[_]
            marked[i] = True
            total -= val                 # 从总和里减去

        # 3) 记录本轮查询后的未标记元素之和
        ans.append(total)

    return ans
```

> 关键行中文注释已经写在代码里，直接复制运行即可。

#### 复杂度

- **时间复杂度**：`O(m * n log n)`  
  - 对每一次查询我们都要遍历整个数组收集未标记元素（`O(n)`），随后排序（`O(n log n)`）。  
  - 这里的 `m` 是查询次数，`n` 是数组长度。  
  - 用大白话说，就是 **每一次查询都像重新排一次队**，队里最多有 `n` 个人，排队要 `n log n` 步。

- **空间复杂度**：`O(n)`  
  - 需要额外的 `marked` 数组和一次临时的 `unmarked_vals` 列表，最多保存 `n` 个元素。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈出在 **每次查询都要把所有未标记元素重新排序**。  
实际上，每个元素只会被标记 **一次**，所以我们可以把“取最小的 k 个未标记元素”这一步 **全局只做一次**，而不是在每个查询里重复。

**核心技巧**：使用 **最小堆（优先队列）** 保存所有未标记元素，堆顶永远是当前未标记元素中数值最小的那个。  

思考过程：

1. **初始化**  
   - 把每个位置 `(nums[i], i)` 放进最小堆 `heap`。  
   - 维护 `marked` 数组和当前未标记元素的总和 `total = sum(nums)`。

2. **处理每个查询 `[idx, k]`**  
   - **标记 `idx`**：如果 `idx` 还未标记，就把它标记并从 `total` 中减去 `nums[idx]`。  
   - **标记 k 个最小元素**：循环 `k` 次（或者堆空为止）  
     - 从堆中弹出堆顶 `(val, i)`。  
     - 如果 `i` 已经标记（可能是之前的 `idx`），**跳过**，继续弹出下一个。  
     - 否则标记它、把 `val` 从 `total` 中减去。  
   - 循环结束后，把 `total` 加入答案数组。

3. **为什么整体是 `O((n+m) log n)`**  
   - 每个元素最多被弹出堆一次（标记后不再需要），所以所有 `pop` 操作的次数 ≤ `n`。  
   - 每次 `push` 只在初始化时进行，次数也是 `n`。  
   - 堆的每次 `pop`/`push` 都是 `log n`，于是总时间是 `O((n + total_k) log n)`，而 `total_k` ≤ `n`（因为标记后元素不再出现），故整体是 `O((n+m) log n)`。  
   - 用大白话说，就是 **每个元素只排一次队**（进堆一次、出堆一次），所以整个过程比“每次查询都排队”快很多。

> **类比**：堆就像一本随时可以查到“当前最小未划线的词”的字典，查一次是 `O(1)`（看堆顶），删一次是 `O(log n)`（把最后一个词搬到最前面再整理）。

#### 代码（Python）

```python
import heapq

def markElements(nums, queries):
    n = len(nums)
    # 1) 初始化最小堆，堆里存 (值, 下标)
    heap = [(nums[i], i) for i in range(n)]
    heapq.heapify(heap)                 # O(n)

    marked = [False] * n                 # 标记数组
    total = sum(nums)                    # 当前未标记元素之和
    ans = []

    for idx, k in queries:
        # ---------- 标记查询给出的下标 ----------
        if not marked[idx]:
            marked[idx] = True
            total -= nums[idx]           # 从总和里减去

        # ---------- 标记 k 个当前最小的未标记元素 ----------
        while k > 0 and heap:
            val, i = heapq.heappop(heap)   # 取堆顶的最小元素
            if marked[i]:                  # 已经标记过，直接跳过
                continue
            # 标记这个元素
            marked[i] = True
            total -= val
            k -= 1

        # ---------- 记录本轮查询后的未标记元素之和 ----------
        ans.append(total)

    return ans
```

**关键行中文注释**：

- `heap = [(nums[i], i) for i in range(n)]` # 把每个元素及其下标放进堆
- `heapq.heapify(heap)` # 把列表一次性变成最小堆，时间线性
- `if not marked[idx]: …` # 只在未标记时才扣除对应的值
- `while k > 0 and heap:` # 循环取最小的 k 个元素
- `if marked[i]: continue` # 弹出来的可能已经在前面被标记，直接丢掉
- `total -= val` # 把被标记的值从总和里减掉

#### 复杂度

- **时间复杂度**：`O((n + m) log n)`  
  - 初始化堆 `O(n)`，每次 `pop`/`push` 为 `log n`，总共至多 `n` 次有效弹出（每个元素只会被标记一次）。  
  - 与暴力解相比，**不再随查询次数线性增长**，大幅提升效率。  

- **空间复杂度**：`O(n)`  
  - 需要保存堆、`marked` 数组以及答案数组，均为线性规模。

---

## 心得

- **核心技巧**：**最小堆 + 只标记一次**。  
  通过堆我们能在 `O(log n)` 时间快速获得当前未标记的最小元素；因为每个元素只会被标记一次，所有弹出操作的次数总和是 `O(n)`，从而实现整体 `O((n+m) log n)`。

- **适用的题型**  
  1. “每次取当前最小/最大元素并删除”——如 **合并 K 条有序链表**、**找第 K 小的数**。  
  2. “动态维护一组元素的最小/最大”，如 **滑动窗口的最大值**（单调队列）或 **动态中位数**（两堆）。  
  3. “一次遍历中多次查询当前最小/最大”，如本题的“多次标记最小元素”。

- **一句话总结解题钥匙**：**把“每次都重新排序”变成“全局只排序一次”，利用堆让最小元素随时可取**。

---

## 反思

- **第一反应**：看到“标记最小的 k 个未标记元素”就想到每次都把未标记元素收集、排序——这就是暴力思路。  
- **最容易踩的坑**  
  1. **重复标记**：查询的 `index` 可能已经在之前被标记，需要先判断再扣除。  
  2. **堆中弹出的已标记元素**：因为 `index` 也会进入堆，在后面的 `k` 次标记里可能被弹出，需要跳过。  
  3. **k 大于剩余未标记元素数**：循环要以 `heap` 是否为空或 `k` 为 0 为结束条件，防止死循环。  

- **下次遇到同类题**：第一步想到 **“是否可以一次性准备一个能够快速取最小/最大的结构（堆、平衡树、单调队列）”，并且确认每个元素只会被操作一次”。** 这样往往能把看似 O(n·m) 的暴力转化为 O((n+m) log n) 的高效解。