# #373. 寻找和最小的 K 对数 / Find K Pairs with Smallest Sums

> 难度：中等 · 标签：Array、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/find-k-pairs-with-smallest-sums/)

---

## 题目（英文原版）

**Description**

You are given two integer arrays nums1 and nums2 sorted in non-decreasing order and an integer k.
Define a pair (u, v) which consists of one element from the first array and one element from the second array.
Return the k pairs (u1, v1), (u2, v2), ..., (uk, vk) with the smallest sums.

**Examples**

**Example 1:**

```
Input: nums1 = [1,7,11], nums2 = [2,4,6], k = 3
Output: [[1,2],[1,4],[1,6]]
Explanation: The first 3 pairs are returned from the sequence: [1,2],[1,4],[1,6],[7,2],[7,4],[11,2],[7,6],[11,4],[11,6]
```

**Example 2:**

```
Input: nums1 = [1,1,2], nums2 = [1,2,3], k = 2
Output: [[1,1],[1,1]]
Explanation: The first 2 pairs are returned from the sequence: [1,1],[1,1],[1,2],[2,1],[1,2],[2,2],[1,3],[1,3],[2,3]
```

**Constraints**

- 1 <= nums1.length, nums2.length <= 105
- -109 <= nums1[i], nums2[i] <= 109
- nums1 and nums2 both are sorted in non-decreasing order.
- 1 <= k <= 104
- k <= nums1.length * nums2.length

---

## 题目（中文翻译）

给定两个按非递减顺序排序的整数数组 `nums1` 和 `nums2`，以及一个整数 `k`。  
定义一个数对 (pair) `(u, v)`，其中 `u` 来自第一个数组，`v` 来自第二个数组。  
返回和最小的 `k` 个数对 `(u₁, v₁)`, `(u₂, v₂)`, …, `(u_k, v_k)`。

**示例 1**  
输入: `nums1 = [1,7,11]`, `nums2 = [2,4,6]`, `k = 3`  
输出: `[[1,2],[1,4],[1,6]]`  
解释: 前 3 个数对来自以下序列: `[1,2]`, `[1,4]`, `[1,6]`, `[7,2]`, `[7,4]`, `[11,2]`, `[7,6]`, `[11,4]`, `[11,6]`

**示例 2**  
输入: `nums1 = [1,1,2]`, `nums2 = [1,2,3]`, `k = 2`  
输出: `[[1,1],[1,1]]`  
解释: 前 2 个数对来自以下序列: `[1,1]`, `[1,1]`, `[1,2]`, `[2,1]`, `[1,2]`, `[2,2]`, `[1,3]`, `[1,3]`, `[2,3]`

**约束条件**
- `1 <= nums1.length, nums2.length <= 10⁵`
- `-10⁹ <= nums1[i], nums2[i] <= 10⁹`
- `nums1` 和 `nums2` 均按非递减顺序排序
- `1 <= k <= 10⁴`
- `k <= nums1.length * nums2.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把两张表 **全部** 配对，算出每一对的和，再挑出最小的 `k` 对。  

- **数据结构**：我们可以用 **列表**（list）把所有 `(u, v)` 配对存下来，随后把它们按照“和”排序。  
  - 把 `list` 想象成一本笔记本，里面一页一页记录每对数的“和”。  
- **正确性**：因为我们把 **所有可能** 的配对都列出来了，排序后取前 `k` 项，自然就是最小的 `k` 对。  
- **复杂度**：  
  - **时间**：要生成 `len(nums1) * len(nums2)` 对，每生成一对花 `O(1)`，再对 `m`（即所有配对数）个元素排序要 `O(m log m)`。所以总体是 `O(m log m)`，这里 `m = n1 * n2`。如果 `n1`、`n2` 都是 `10⁵`，`m` 会达到 `10¹⁰`，根本不可行。  
  - **空间**：我们需要把所有配对存下来，空间是 `O(m)`，同样会爆掉内存。

> **大白话**：  
> - `O(n²)` 并不是说“平方”本身有多神奇，而是说**工作量会随输入规模的平方增长**，比如 `n=1000` 时要做 1 000 000 次操作，`n=10 000` 时要做 100 000 000 次操作，量级激增。

#### 代码（Python）

```python
from typing import List

def k_smallest_pairs_bruteforce(nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
    # 1. 列举所有配对
    all_pairs = []
    for a in nums1:                # 第一个数组的每个元素
        for b in nums2:            # 第二个数组的每个元素
            all_pairs.append([a, b, a + b])   # 记录 (u, v, 和) 方便后面排序

    # 2. 按照和从小到大排序
    all_pairs.sort(key=lambda x: x[2])   # lambda x: x[2] 取 “和” 这一列

    # 3. 取前 k 项并去掉和的字段
    result = [[a, b] for a, b, _ in all_pairs[:k]]
    return result
```

#### 复杂度

- **时间复杂度**：`O(n1 * n2 log (n1 * n2))`  
  - 生成配对是 `O(n1 * n2)`，排序是 `O(m log m)`，`m = n1 * n2`。  
- **空间复杂度**：`O(n1 * n2)`  
  - 必须把所有配对存下来。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**一次性产生所有配对**，而我们只需要前 `k` 小的配对。  
观察题目给出的两个数组都是 **非递减**（从小到大）排序的，这给了我们极大的优化空间。

**关键观察**  

1. 对于固定的 `nums1[i]`，如果把 `nums2` 按顺序配对，和会 **递增**：  
   - `(nums1[i], nums2[0])` 的和是最小的，  
   - `(nums1[i], nums2[1])` 的和稍大，依此类推。  

2. 同理，对于固定的 `nums2[j]`，`(nums1[0], nums2[j])` 是最小的，以后配对会递增。  

因此我们可以把 “候选的下一个最小配对” 放进一个 **小根堆（最小优先队列）**，每次弹出堆顶（当前最小的和），并把它的“后继配对”加入堆中。  

**具体步骤**  

- **初始化**：只把 `nums1` 前 `min(k, len(nums1))` 个元素和 `nums2[0]` 配对放进堆。原因是 `k` 不会超过答案的数量，若 `nums1` 很长，只需要前 `k` 个最小的 `nums1` 参与配对。  
  - 堆里每个元素保存 `(sum, i, j)`，其中 `i`、`j` 是对应数组的下标。  
- **循环**：弹出堆顶 `(sum, i, j)`，把配对 `[nums1[i], nums2[j]]` 加入答案。  
  - 若 `j + 1 < len(nums2)`，说明 `nums2` 还有下一个元素可以和同一个 `nums1[i]` 配对，产生的新配对是 `(nums1[i], nums2[j+1])`，把它推入堆。  
- **结束**：当答案长度达到 `k` 或堆空时结束。

**为什么正确**  

- 堆始终保持“当前未输出的配对中，和最小的那个在堆顶”。  
- 每次弹出后，只把 **同一行**（即同一个 `i`）的下一个配对加入堆，保证不会遗漏任何可能比已输出配对更小的组合。  
- 由于数组已排序，这种“逐行推进”的方式正好覆盖了所有可能的最小 `k` 对。

**类比**：想象有若干条排好队的公交车（每条对应 `nums1[i]`），每辆车上有座位（对应 `nums2` 的元素），车票价等于 `nums1[i] + nums2[j]`，我们每次买最便宜的票，并把同一辆车的下一位乘客的票价加入候选名单，这样就能一次买到最便宜的 `k` 张票。

#### 代码（Python）

```python
import heapq
from typing import List

def k_smallest_pairs(nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
    """
    使用最小堆（优先队列）实现 O(k log min(k, len(nums1))) 的解法
    """
    if not nums1 or not nums2 or k == 0:
        return []

    # 1️⃣ 初始化堆：把 nums1 前 min(k, len(nums1)) 个元素和 nums2[0] 配对
    heap = []                                   # 小根堆，元素形如 (sum, i, j)
    m = min(k, len(nums1))                      # 只需要这么多行
    for i in range(m):
        # sum = nums1[i] + nums2[0]，i 为行索引，j 为列索引（当前是第 0 列）
        heapq.heappush(heap, (nums1[i] + nums2[0], i, 0))

    # 2️⃣ 逐个弹出最小和，收集答案，并把同一行的下一个配对加入堆
    ans = []
    while heap and len(ans) < k:
        cur_sum, i, j = heapq.heappop(heap)     # 弹出当前最小的和
        ans.append([nums1[i], nums2[j]])        # 保存配对

        # 若当前列 j 还能往右移动（还有更大的 nums2），把右边的配对加入堆
        if j + 1 < len(nums2):
            next_sum = nums1[i] + nums2[j + 1]
            heapq.heappush(heap, (next_sum, i, j + 1))

    return ans
```

#### 复杂度

- **时间复杂度**：`O(k log min(k, n1))`  
  - 堆的大小最多为 `min(k, n1)`（因为我们只会把每一行的下一个配对放进去），每次弹出或插入的代价是 `log` 堆大小。循环最多执行 `k` 次，所以是 `k * log(min(k, n1))`。  
  - 与暴力解相比，大幅降低了时间开销，尤其当 `k` 远小于 `n1 * n2` 时效果尤为明显。

- **空间复杂度**：`O(min(k, n1))`  
  - 堆里最多存 `min(k, n1)` 条记录，答案列表需要 `O(k)` 空间（输出本身必须占用），总体是线性于 `k`（或 `n1`）而不是乘积。

---

## 心得

- **核心技巧**：利用 **有序数组 + 最小堆**（又叫“多路归并”）一次获取最小的 `k` 项。  
- **适用场景**：  
  1. 两个或多个已排序序列的 **前 k 小元素**（如合并 `k` 条有序链表的前 `k` 节点）。  
  2. “**矩阵中前 k 小**” 这类题目，矩阵每行/每列单调递增。  
  3. 需要在 **大搜索空间** 中逐步扩展的情形（如 Dijkstra 最短路、A* 搜索）。  
- **一句话总结**：**把“下一个可能的最小配对”放进最小堆，弹出即是答案**。

---

## 反思

- **第一反应**：直接把所有配对列出来再排序，想到“暴力”。  
- **最容易踩的坑**：  
  - 忘记对 `k` 与数组长度的取最小值做限制，导致堆的大小可能会超过 `k`，浪费空间。  
  - 当 `nums1` 或 `nums2` 为空或 `k = 0` 时要提前返回空列表，防止索引越界。  
  - 注意 `heapq` 在 Python 中默认是 **最小堆**，直接使用 `(sum, i, j)` 即可，无需额外取负。  
- **下次类似题的第一步**：先检查输入是否 **有序**，如果是，就考虑 **使用堆/指针逐步扩展**，而不是一次性全部枚举。