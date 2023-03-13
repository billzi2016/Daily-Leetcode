# #2163. 删除 n 个元素后两部分和的最小差值 / Minimum Difference in Sums After Removal of Elements

> 难度：困难 · 标签：Array、Dynamic Programming、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/minimum-difference-in-sums-after-removal-of-elements/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums consisting of 3 * n elements.
You are allowed to remove any subsequence of elements of size exactly n from nums. The remaining 2 * n elements will be divided into two equal parts:
The difference in sums of the two parts is denoted as sumfirst - sumsecond.
Return the minimum difference possible between the sums of the two parts after the removal of n elements.

**Examples**

**Example 1:**

```
Input: nums = [3,1,2]
Output: -1
Explanation: Here, nums has 3 elements, so n = 1. 
Thus we have to remove 1 element from nums and divide the array into two equal parts.
- If we remove nums[0] = 3, the array will be [1,2]. The difference in sums of the two parts will be 1 - 2 = -1.
- If we remove nums[1] = 1, the array will be [3,2]. The difference in sums of the two parts will be 3 - 2 = 1.
- If we remove nums[2] = 2, the array will be [3,1]. The difference in sums of the two parts will be 3 - 1 = 2.
The minimum difference between sums of the two parts is min(-1,1,2) = -1.
```

**Example 2:**

```
Input: nums = [7,9,5,8,1,3]
Output: 1
Explanation: Here n = 2. So we must remove 2 elements and divide the remaining array into two parts containing two elements each.
If we remove nums[2] = 5 and nums[3] = 8, the resultant array will be [7,9,1,3]. The difference in sums will be (7+9) - (1+3) = 12.
To obtain the minimum difference, we should remove nums[1] = 9 and nums[4] = 1. The resultant array becomes [7,5,8,3]. The difference in sums of the two parts is (7+5) - (8+3) = 1.
It can be shown that it is not possible to obtain a difference smaller than 1.
```

**Constraints**

- nums.length == 3 * n
- 1 <= n <= 105
- 1 <= nums[i] <= 105

---

## 题目（中文翻译）

**题目描述**  
给定一个下标从 0 开始的整数数组 `nums`，其长度为 `3 * n`。  
你可以从 `nums` 中删除恰好 `n` 个元素（形成一个子序列（subsequence）），剩余的 `2 * n` 个元素随后会被分成两个等长的部分，每部分包含 `n` 个元素。  
设第一部分的元素和为 `sumfirst`，第二部分的元素和为 `sumsecond`，两部分和的差记为 `sumfirst - sumsecond`。  
返回在删除 `n` 个元素之后，使两部分和的差的 **最小可能值**。

**示例**

*示例 1*  
```
Input: nums = [3,1,2]
Output: -1
Explanation: 这里 nums 有 3 个元素，所以 n = 1。  
因此需要从 nums 中删除 1 个元素，然后将剩余数组分成两个等长的部分。  
- 删除 nums[0] = 3 后，数组变为 [1,2]，两部分和的差为 1 - 2 = -1。  
- 删除 nums[1] = 1 后，数组变为 [3,2]，两部分和的差为 3 - 2 = 1。  
- 删除 nums[2] = 2 后，数组变为 [3,1]，两部分和的差为 3 - 1 = 2。  
最小的差值为 -1。  
```

*示例 2*  
```
Input: nums = [7,9,5,8,1,3]
Output: 1
Explanation: 这里 n = 2，需要删除 2 个元素，剩余的 4 个元素再分成两部分，每部分 2 个元素。  
如果删除 nums[2] = 5 和 nums[3] = 8，得到的数组为 [7,9,1,3]，差值为 (7+9) - (1+3) = 12。  
为了得到最小差值，应删除 nums[1] = 9 和 nums[4] = 1，得到的数组为 [7,5,8,3]，差值为 (7+5) - (8+3) = 1。  
```

**约束条件**  
- `nums.length == 3 * n`  
- `1 <= n <= 10^5`  
- `1 <= nums[i] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的删除方案都枚举一遍**，然后对每一种方案再把剩下的 `2·n` 个数平分成前后两段，计算 `sum(first) - sum(second)`，取最小值。

- **枚举删除的子序列**：`nums` 长度为 `3·n`，要删除恰好 `n` 个元素。等价于从 `3·n` 个位置中挑选 `n` 个位置，这本质上是组合数 `C(3n, n)`，数量会随 `n` 指数级增长。  
- **划分剩余数组**：删除后剩下 `2·n` 个数，前 `n` 个算作左边，后 `n` 个算作右边，直接求两段的和即可。

> **类比**：把这道题想成“从一本 3n 页的书里抽掉 n 页，然后把剩下的书平均分成上下两册，比较两册的总页数”。如果你把每一种抽页方式都试一遍，显然要花掉非常多的时间。

**为什么正确**：因为我们遍历了**所有**合法的删除方式，必然能找到最小的差值。只不过这样做在计算上几乎是不可能完成的。

#### 代码（Python）

```python
import itertools

def minimumDifference_bruteforce(nums):
    n = len(nums) // 3
    best = float('inf')
    # 所有可能的删除下标组合（指数级）
    for remove_idx in itertools.combinations(range(3 * n), n):
        remove_set = set(remove_idx)
        # 剩余的元素按原顺序拼成新数组
        remain = [nums[i] for i in range(3 * n) if i not in remove_set]
        # 前 n 个算左边，后 n 个算右边
        left_sum  = sum(remain[:n])
        right_sum = sum(remain[n:])
        best = min(best, left_sum - right_sum)
    return best
```

> 这段代码在 `n` 大于 5 左右时就会失控（运行时间呈指数增长），只能当作理论上的“暴力解”。

#### 复杂度  

- **时间复杂度**：`O(C(3n, n) * n)` —— 组合数本身已经是指数级的，等价于 **O( (3n)! / (n!·(2n)!) )**，在实际中几乎不可接受。  
- **空间复杂度**：`O(3n)` 用来存放临时的 `remain` 数组，属于线性空间。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于枚举所有删除方案**。我们需要一种方式，只用一次遍历就能得到“左边最小和”和“右边最大和”。关键观察：

1. **删除 n 个元素后，剩下的 2n 个数的顺序仍然保持原来的相对顺序**。于是可以把问题等价为：在原数组中选出一个“分割点” `i`（`n‑1 ≤ i ≤ 2n‑1`），左侧（包括 `i`）至少保留 `n` 个数，右侧（不包括 `i`）至少保留 `n` 个数。我们要让左侧选出的 `n` 个数的和尽可能 **小**，右侧选出的 `n` 个数的和尽可能 **大**。

2. 对每个可能的分割点 `i`，我们需要知道：
   - **左侧最小 possible sum**：在下标 `0 … i` 中，挑选恰好 `n` 个数，使它们的和最小。记作 `left[i]`。
   - **右侧最大 possible sum**：在下标 `i+1 … 3n‑1` 中，挑选恰好 `n` 个数，使它们的和最大。记作 `right[i+1]`。

3. 有了 `left[i]` 与 `right[i+1]`，答案就是  
   `min_{i=n‑1 … 2n‑1} ( left[i] - right[i+1] )`。

#### 如何高效求 `left` 与 `right`

- **左侧最小 n 和**：从左到右遍历数组，用一个**最大堆**（Python 的 `heapq` 默认是最小堆，存负数即可）维护当前已选的 `n` 个最小元素的和。  
  - 初始把前 `n` 个数放进堆，求和 `cur_sum`（此时已经是左侧最小 n 和）。  
  - 向右移动一格时，把新出现的元素加入堆并累加到 `cur_sum`，随后弹出堆顶（即最大的那个），把它的值减去 `cur_sum`，保持堆大小始终为 `n`。这样堆里始终保存的是 **当前前缀中最小的 n 个数**，`cur_sum` 就是对应的最小和。把它写入 `left[i]`。

- **右侧最大 n 和**：从右到左遍历，用**最小堆**维护当前已选的 `n` 个最大元素的和（同理，弹出最小的保留最大的）。过程与左侧相反，只是方向和堆的类型不同。

> **类比**：  
> - 最大堆像是“装满 n 个最轻石头的背包”，每次有更轻的石头出现，就把最重的石头踢出去，背包里永远是当前最轻的 n 块石头。背包的总重量就是左侧的最小和。  
> - 最小堆则是“装满 n 块最重石头的背包”，每次有更重的石头出现，就把最轻的踢出去，背包重量就是右侧的最大和。

#### 代码（Python）

```python
import heapq
from typing import List

def minimumDifference(nums: List[int]) -> int:
    """
    计算在删除恰好 n 个元素后，使前 n 个数的和 - 后 n 个数的和 最小的值。
    思路：前缀最小 n 和 + 后缀最大 n 和 → 一次遍历得到答案
    """
    m = len(nums)                 # = 3 * n
    n = m // 3

    # ---------- 1. 计算 left[i]（0-indexed） ----------
    left = [0] * m                 # 只会用到 i in [n-1, 2n-1]
    max_heap = []                  # 存负数，实现最大堆
    cur_sum = 0

    # 先放前 n 个数
    for i in range(n):
        cur_sum += nums[i]
        heapq.heappush(max_heap, -nums[i])   # 负数 → 最大堆
    left[n - 1] = cur_sum

    # 向右滑动，维护“前缀中最小的 n 个数”
    for i in range(n, 2 * n):
        cur_sum += nums[i]
        heapq.heappush(max_heap, -nums[i])
        # 弹出当前最大的（即负数最小的），保证堆大小为 n
        removed = -heapq.heappop(max_heap)
        cur_sum -= removed
        left[i] = cur_sum

    # ---------- 2. 计算 right[i]（i 为分割点右侧的起始下标） ----------
    right = [0] * m                # 只会用到 i in [n, 2n]
    min_heap = []                  # 正常的最小堆
    cur_sum = 0

    # 先放后 n 个数（数组最右侧）
    for i in range(m - 1, m - n - 1, -1):
        cur_sum += nums[i]
        heapq.heappush(min_heap, nums[i])
    right[2 * n] = cur_sum          # 右侧第一个可用分割点是 2n

    # 向左滑动，维护“后缀中最大的 n 个数”
    for i in range(2 * n - 1, n - 1, -1):
        cur_sum += nums[i]
        heapq.heappush(min_heap, nums[i])
        # 弹出当前最小的，保持堆大小为 n
        removed = heapq.heappop(min_heap)
        cur_sum -= removed
        right[i] = cur_sum

    # ---------- 3. 在所有合法的分割点上取最小差值 ----------
    answer = float('inf')
    for i in range(n - 1, 2 * n):
        diff = left[i] - right[i + 1]
        if diff < answer:
            answer = diff
    return answer
```

**代码要点注释**（已在关键行写中文解释）：

- `max_heap` 使用负数实现最大堆，用来**实时保存前缀中最小的 n 个数**。  
- `min_heap` 正常使用，用来**实时保存后缀中最大的 n 个数**。  
- `left[i]` 表示 **下标 ≤ i** 的子数组里挑 `n` 个数的**最小可能和**。  
- `right[i]` 表示 **下标 ≥ i** 的子数组里挑 `n` 个数的**最大可能和**。  
- 最后遍历合法的分割点 `i`（左侧必须至少保留 `n`，右侧同理），计算 `left[i] - right[i+1]`，取最小。

#### 复杂度  

- **时间复杂度**：`O(3n log n) = O(n log n)`。  
  - 遍历一次数组，堆的插入与弹出均为 `O(log n)`，共执行约 `3n` 次。  
  - 相比暴力的指数级，这已经是**线性对数**的高效解。  
- **空间复杂度**：`O(n)`。  
  - 两个堆各最多保存 `n` 个元素，`left` 与 `right` 两个数组各长度 `3n`（但只用到 `O(n)` 的区间），整体仍然是线性空间。

---

## 心得

- **核心技巧**：**前缀最小 n 和 + 后缀最大 n 和**，配合 **堆（优先队列）** 实现“动态维护前 n 小/后 n 大”。  
- **适用的题型**：  
  1. “在数组中选取 k 个数使和最小/最大”——如 LeetCode 2092、2199。  
  2. “拆分数组后求两段和的差值最小”——如本题、或“分割数组的最小差”。  
  3. “删除若干元素后保持某种极值”——如 “删除子数组后最大子序和”。  
- **一句话总结**：**把问题转化为“左侧挑最小、右侧挑最大”，用堆一次遍历即可得到全局最优**。

---

## 反思

- **第一反应**：看到“删除 n 个元素后分成两段”，自然想到“枚举所有删除方式”，这导致了暴力思路。  
- **最容易踩的坑**：  
  - **分割点的取值范围**必须保证左、右各至少有 `n` 个元素，否则无法构成合法的两段。  
  - **堆的类型选错**：左侧需要 **最大堆**（保留最小的 n），右侧需要 **最小堆**（保留最大的 n），容易混淆。  
  - **整数溢出** 在 Python 中不成问题，但在其他语言要注意使用 64 位整数。  
- **下次遇到同类题**：第一步先**思考“在前缀/后缀中挑 k 个数的极值”能否用**堆**或**单调结构**实时维护，而不是直接枚举组合。这样往往能把指数级的搜索压缩到 `O(n log k)`。