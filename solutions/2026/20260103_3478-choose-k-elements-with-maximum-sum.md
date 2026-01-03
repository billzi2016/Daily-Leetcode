# #3478. **选择 K 个元素的最大和** / Choose K Elements With Maximum Sum

> 难度：中等 · 标签：Array、Sorting、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/choose-k-elements-with-maximum-sum/)

---

## 题目（英文原版）

**Description**

You are given two integer arrays, nums1 and nums2, both of length n, along with a positive integer k.
For each index i from 0 to n - 1, perform the following:
Return an array answer of size n, where answer[i] represents the result for the corresponding index i.

**Examples**

**Example 1:**

```
Input: nums1 = [4,2,1,5,3], nums2 = [10,20,30,40,50], k = 2
Output: [80,30,0,80,50]
Explanation:
```

**Example 2:**

```
Input: nums1 = [2,2,2,2], nums2 = [3,1,2,3], k = 1
Output: [0,0,0,0]
Explanation:
Since all elements in nums1 are equal, no indices satisfy the condition nums1[j] < nums1[i] for any i , resulting in 0 for all positions.
```

**Constraints**

- n == nums1.length == nums2.length
- 1 <= n <= 105
- 1 <= nums1[i], nums2[i] <= 106
- 1 <= k <= n

---

## 题目（中文翻译）

给定两个整数数组 `nums1` 和 `nums2`（长度均为 `n`），以及一个正整数 `k`。  
对于每个下标 `i`（`0 <= i < n`），计算满足 `nums1[j] < nums1[i]` 的所有下标 `j` 中，`nums2[j]` 的最大 **k** 个元素之和。如果符合条件的下标少于 `k`，则将所有符合条件的 `nums2[j]` 相加。  
返回长度为 `n` 的数组 `answer`，其中 `answer[i]` 即对应下标 `i` 的计算结果。

**示例 1**

```
Input: nums1 = [4,2,1,5,3], nums2 = [10,20,30,40,50], k = 2
Output: [80,30,0,80,50]
Explanation:
- i = 0, nums1[0] = 4. 小于 4 的下标有 1、2、4，对应的 nums2 为 20、30、50，取最大 2 个得到 50 + 30 = 80。
- i = 1, nums1[1] = 2. 小于 2 的下标只有 2，对应的 nums2 为 30，只有一个元素，和为 30。
- i = 2, nums1[2] = 1. 没有下标满足 nums1[j] < 1，和为 0。
- i = 3, nums1[3] = 5. 小于 5 的下标有 0、1、2、4，对应的 nums2 为 10、20、30、50，取最大 2 个得到 50 + 30 = 80。
- i = 4, nums1[4] = 3. 小于 3 的下标有 1、2，对应的 nums2 为 20、30，取最大 2 个得到 20 + 30 = 50。
```

**示例 2**

```
Input: nums1 = [2,2,2,2], nums2 = [3,1,2,3], k = 1
Output: [0,0,0,0]
Explanation:
所有元素的 nums1 值相等，不存在下标满足 nums1[j] < nums1[i]，因此每个位置的和均为 0。
```

**约束条件**

- `n == nums1.length == nums2.length`
- `1 <= n <= 10^5`
- `1 <= nums1[i], nums2[i] <= 10^6`
- `1 <= k <= n`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**对每一个下标 `i`，把所有满足 `nums1[j] < nums1[i]` 的 `j` 找出来，把对应的 `nums2[j]` 收集到一个列表里，挑出最大的 `k` 个（如果不足 `k` 就全拿），求和得到 `answer[i]`**。  

- **使用的数据结构**：  
  - `list`（列表）用来暂存符合条件的 `nums2` 值。可以把它想象成“收集箱”，把所有满足条件的数字装进去。  
  - `sort`（排序）用来挑出最大的 `k` 个。把收集箱里的数字从大到小排好序，前 `k` 个就是我们要的。  

- **为什么一定能得到正确答案**：  
  只要把 **所有** 满足 `nums1[j] < nums1[i]` 的 `nums2[j]` 收集起来，再挑出 **最大的 k 个**，它们的和必然是满足条件的子集里最大的可能和——因为任何别的子集要么少取了一个更大的数，要么多取了一个更小的数，和都会不如我们挑出的这 `k` 个。

- **复杂度分析（大白话）**：  
  - 对每个 `i`（一共 `n` 次），我们都要遍历整个数组检查 `nums1[j] < nums1[i]`（`n` 次），这一步相当于“把每个人的所有邻居都找一遍”。  
  - 收集完以后要排序，最坏情况要排 `n` 个数，时间大约是 `n log n`。  
  - 综合下来时间是 **`O(n * (n + n log n)) ≈ O(n² log n)`**，但因为 `n` 已经在 10⁵ 量级，`n²` 已经远远超出接受范围。  
  - 空间上我们只需要一个临时列表，最坏情况下会装下 `n` 个数，**`O(n)`** 的额外空间。

#### 代码（Python）

```python
from typing import List

def max_sum_bruteforce(nums1: List[int], nums2: List[int], k: int) -> List[int]:
    n = len(nums1)
    ans = [0] * n                     # 最终答案数组
    for i in range(n):                # 对每个位置 i
        candidates = []               # 收集满足条件的 nums2
        for j in range(n):            # 暴力检查所有 j
            if nums1[j] < nums1[i]:   # 条件：nums1[j] 必须更小
                candidates.append(nums2[j])
        # 把收集到的 nums2 从大到小排
        candidates.sort(reverse=True)
        # 只取前 k 个（如果不足 k 就全部取）
        ans[i] = sum(candidates[:k])
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n² log n)` —— 每个 `i` 需要遍历 `n` 次并对收集的元素排序。  
- **空间复杂度**：`O(n)` —— 最坏情况下临时列表会装下全部 `n` 个 `nums2`。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每次都要重新遍历全部 `j`**，这导致 `O(n²)` 的时间。  
我们可以利用 **“从小到大一次遍历”** 的思想，避免重复工作：

1. **先把下标按照 `nums1` 的大小排序**。  
   - 想象把所有人排成一条队伍，身高（`nums1`）从矮到高。  
   - 当我们站在第 `i` 个人时，**他前面所有人** 的 `nums1` 必然都更小。  
2. **维护一个只保留最大 `k` 个 `nums2` 的最小堆**（优先队列）。  
   - 堆就像一个“小盒子”，里面始终保存当前看到的最大的 `k` 个 `nums2`。  
   - 堆顶（最小的那个）是我们随时可以踢出去的“最小的宝贝”。  
   - 这样，**在遍历到某个下标时，堆里恰好是所有 **左侧**（`nums1` 更小）位置的 `nums2` 中最大的 `k` 个**。  
3. **当前下标的答案 = 堆中所有元素的和**（如果堆里元素少于 `k`，直接把它们全部相加）。  
4. **把当前的 `nums2` 加入堆**，如果堆的大小超过 `k`，弹出最小的那个，保持堆大小不变。  
5. 继续遍历下一个下标。

因为我们只遍历一次（`O(n)`），每次堆的插入/弹出是 `O(log k)`，整体时间是 `O(n log k)`，远快于暴力。

> **核心数据结构解释**  
> - **最小堆（min‑heap）**：想象一堆石头，最轻的那块总是放在最上面，随时可以拿走。我们把 `nums2` 当石头，堆顶就是当前最大 `k` 里最小的那块，弹出它相当于“把不够大的石头扔掉”。  
> - **前缀和**：这里不需要额外的前缀和，只要维护一个变量 `heap_sum`，记录堆中所有元素的和，随时更新即可。

#### 代码（Python）

```python
import heapq
from typing import List

def max_sum_optimal(nums1: List[int], nums2: List[int], k: int) -> List[int]:
    n = len(nums1)

    # 1️⃣ 把下标按照 nums1 的大小升序排列
    #   idxs = [0, 1, 2, ...] 按 nums1 对应的值从小到大排好
    idxs = sorted(range(n), key=lambda i: nums1[i])

    # 2️⃣ 用最小堆保存目前看到的最大的 k 个 nums2
    min_heap = []          # 堆里存的是 nums2 的值
    heap_sum = 0           # 堆中所有元素的和，随时维护

    # 结果数组，先全部填 0
    answer = [0] * n

    # 3️⃣ 按照 nums1 从小到大依次处理
    for i in idxs:
        # 此时堆里恰好是所有 nums1 更小的下标对应的 nums2（最多 k 个最大值）
        answer[i] = heap_sum          # 直接把和写进答案

        # 把当前的 nums2 加入堆中，准备供后面的更大的 nums1 使用
        heapq.heappush(min_heap, nums2[i])
        heap_sum += nums2[i]

        # 如果堆的大小超过 k，弹出最小的那个，保持只保留最大的 k 个
        if len(min_heap) > k:
            smallest = heapq.heappop(min_heap)   # 弹出堆顶（最小值）
            heap_sum -= smallest                  # 同步更新和

    return answer
```

> **代码关键行中文注释**  
> - `sorted(..., key=lambda i: nums1[i])`：把下标按 `nums1` 的值排好序，像把人按身高排队。  
> - `heapq.heappush(min_heap, nums2[i])`：把当前的 `nums2` 放进“小盒子”。  
> - `if len(min_heap) > k: heapq.heappop(min_heap)`：盒子装满了（超过 `k`），把最轻的石头（最小的 `nums2`）扔掉，确保盒子里永远是最大的 `k` 块。  
> - `answer[i] = heap_sum`：盒子里石头的总重量，就是答案。

#### 复杂度

- **时间复杂度**：`O(n log k)`  
  - 排序一次 `O(n log n)`（但 `log n` 与 `log k` 同阶，整体仍为 `O(n log n)`，在 `k ≤ n` 时可写作 `O(n log k)`）。  
  - 每个元素一次插入堆 `O(log k)`，最多一次弹出 `O(log k)`。  
  - 与暴力的 `O(n²)` 相比，几乎是 **线性级** 的提升。

- **空间复杂度**：`O(k)`  
  - 只维护一个大小不超过 `k` 的堆和一个 `heap_sum` 变量，额外空间与 `k` 成正比。  
  - 结果数组 `answer` 本身是输出，需要 `O(n)`，但不计入额外空间。

---

## 心得

- **核心技巧**：**排序 + 最小堆（维护前 k 大）**。  
- **适用的题型**（类似思路）  
  1. “**在每个元素左侧找最大的 k 个值的和**” 例如 LeetCode 2381 *Maximum Sum of the Prefix of the Array*。  
  2. “**根据一个属性筛选，求另一属性的前 k 大和**” 如 “Maximum Sum of Selected Elements” 系列。  
  3. “**滑动窗口内前 k 大**” 的变体，例如 “Sliding Window Maximum”。  

- **一句话总结解题钥匙**：  
  *把数组按关键属性排序，利用最小堆实时维护“已出现的最大 k 个值”，即可在一次遍历中得到每个位置的答案。*

---

## 反思

- **第一反应**：看到“对于每个 i，找所有 nums1[j] < nums1[i] 的 nums2 并取最大 k 个”，第一时间会想到两层循环 → 暴力 `O(n²)`。  
- **最容易踩的坑**  
  1. **下标顺序混乱**：排序后需要把答案写回原始下标，否则输出顺序会错。  
  2. **堆的大小维护**：忘记在插入后检查并弹出，导致堆里可能超过 `k`，答案会错误。  
  3. **边界条件**：`k = 1` 或 `k = n`，以及某些 `i` 前面没有满足条件的元素，需要返回 `0`，不能出现未初始化的值。  
- **下次类似题的第一步**：  
  *先判断是否可以把“左侧/前缀”或“右侧/后缀”转化为一次线性遍历的形式，随后考虑用堆或单调结构维护前 k 大（或小）元素。*