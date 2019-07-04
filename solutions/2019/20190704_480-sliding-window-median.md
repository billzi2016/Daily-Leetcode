# #480. 滑动窗口中位数 / Sliding Window Median

> 难度：困难 · 标签：Array、Hash Table、Sliding Window、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/sliding-window-median/)

---

## 题目（英文原版）

**Description**

The median is the middle value in an ordered integer list. If the size of the list is even, there is no middle value. So the median is the mean of the two middle values.
You are given an integer array nums and an integer k. There is a sliding window of size k which is moving from the very left of the array to the very right. You can only see the k numbers in the window. Each time the sliding window moves right by one position.
Return the median array for each window in the original array. Answers within 10-5 of the actual value will be accepted.

**Examples**

**Example 1:**

```
Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
Output: [1.00000,-1.00000,-1.00000,3.00000,5.00000,6.00000]
Explanation: 
Window position                Median
---------------                -----
[1  3  -1] -3  5  3  6  7        1
 1 [3  -1  -3] 5  3  6  7       -1
 1  3 [-1  -3  5] 3  6  7       -1
 1  3  -1 [-3  5  3] 6  7        3
 1  3  -1  -3 [5  3  6] 7        5
 1  3  -1  -3  5 [3  6  7]       6
```

**Example 2:**

```
Input: nums = [1,2,3,4,2,3,1,4,2], k = 3
Output: [2.00000,3.00000,3.00000,3.00000,2.00000,3.00000,2.00000]
```

**Constraints**

- 1 <= k <= nums.length <= 105
- -231 <= nums[i] <= 231 - 1

---

## 题目（中文翻译）

中位数 (median) 是有序整数列表中的中间值。如果列表长度为偶数，则不存在唯一的中间值，此时中位数是两个中间值的平均值。  
给定一个整数数组 (array) `nums` 和一个整数 `k`。存在一个大小为 `k` 的滑动窗口 (sliding window)，它从数组最左侧移动到最右侧。每次只能看到窗口内的 `k` 个数，窗口每次向右移动一位。  
返回原数组中每个窗口对应的中位数数组。答案只要在 `10^-5` 的误差范围内即被接受。

**示例 1**  
```text
Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
Output: [1.00000,-1.00000,-1.00000,3.00000,5.00000,6.00000]
Explanation: 
窗口位置                     中位数
---------------            -----
[1  3  -1] -3  5  3  6  7   1
 1 [3  -1  -3] 5  3  6  7  -1
 1  3 [-1  -3  5] 3  6  7  -1
 1  3  -1 [-3  5  3] 6  7   3
 1  3  -1  -3 [5  3  6] 7   5
 1  3  -1  -3  5 [3  6  7]  6
```

**示例 2**  
```text
Input: nums = [1,2,3,4,2,3,1,4,2], k = 3
Output: [2.00000,3.00000,3.00000,3.00000,2.00000,3.00000,2.00000]
```

**约束条件**
- `1 <= k <= nums.length <= 10^5`
- `-2^31 <= nums[i] <= 2^31 - 1`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**每次窗口滑动时把窗口里的 `k` 个数全部取出来，排序，然后直接取中位数**。  
- **取窗口里的数**：这一步相当于把窗口看成一只装有 `k` 个水果的篮子，随着篮子向右移动，我们每次把左边的水果丢掉、把右边的新水果放进去。  
- **排序**：把篮子里的水果从小到大排好序，就像把字典里的单词按字母顺序排好。  
- **取中位数**：如果 `k` 为奇数，直接取第 `k//2`（从 0 开始计数）个元素；如果 `k` 为偶数，取中间两个元素的平均值。  

这个方法一定能得到正确答案，因为**中位数的定义本身就要求先把所有数排好序**，只要我们不遗漏任何窗口里的数，计算就不会出错。

**为什么会慢？**  
- 对每一个窗口我们都要 **完整排序**，排序的时间是 `O(k log k)`。  
- 窗口一共会出现 `n - k + 1` 次（`n` 为数组长度），于是总时间是 `O((n - k + 1) * k log k)`，在最坏情况下接近 `O(n·k·log k)`。  
- 当 `n` 和 `k` 都接近 10⁵ 时，这个复杂度几乎不可接受。

#### 代码（Python）

```python
from typing import List

def median_sliding_window_bruteforce(nums: List[int], k: int) -> List[float]:
    """
    暴力解：每次取窗口、排序、求中位数
    """
    n = len(nums)
    res: List[float] = []

    for i in range(n - k + 1):               # 窗口左端点从 0 滑到 n-k
        window = nums[i:i + k]               # 取出当前窗口的 k 个数
        window.sort()                        # 排序，O(k log k)

        # 计算中位数
        if k % 2 == 1:                       # 奇数个数
            median = float(window[k // 2])
        else:                                # 偶数个数，取中间两个的平均值
            median = (window[k // 2 - 1] + window[k // 2]) / 2.0

        res.append(median)                   # 保存结果

    return res
```

#### 复杂度  

- **时间复杂度**：`O((n - k + 1) * k log k)` ≈ `O(n·k·log k)`  
  > 这相当于“每滑动一次窗口，就要花 k·log k 的时间来重新排队”。  
- **空间复杂度**：`O(k)`  
  > 只需要存放当前窗口的 `k` 个数（排序时会在原数组上进行），额外空间与窗口大小成正比。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**排序是瓶颈**。我们需要一种数据结构，能够：

1. **快速插入** 一个新元素（窗口右侧进入的数）  
2. **快速删除** 一个旧元素（窗口左侧离开的数）  
3. **在 O(1) 或 O(log k) 时间内取到中位数**  

这正好可以用 **两个堆**（优先队列）来实现：

- **大根堆 `low`**：保存窗口中较小的一半数（最大值在堆顶），相当于“左半边”。  
- **小根堆 `high`**：保存窗口中较大的一半数（最小值在堆顶），相当于“右半边”。  

我们让两堆的大小保持平衡（`len(low) == len(high)` 或 `len(low) == len(high) + 1`），这样：

- 当 `k` 为奇数时，`low` 多一个元素，堆顶就是中位数。  
- 当 `k` 为偶数时，`low` 与 `high` 各占一半，中位数是两堆堆顶的平均值。  

**插入**：把新数先放进 `low`（大根堆），再把 `low` 堆顶弹出放进 `high`（小根堆），保证所有在 `low` 的数都 ≤ `high` 的数。  
**删除**：直接删除对应堆中的元素比较困难，因为堆不支持 O(log k) 的任意位置删除。我们采用 **懒删除（lazy deletion）**：用一个哈希表 `del_map` 记录“该值已经被删除但仍在堆里”。在每次取堆顶或平衡堆时，检查堆顶是否已经在 `del_map` 中，如果是就把它弹出并在 `del_map` 中计数减一。这样实际删除的成本仍然是 `O(log k)`（弹出堆顶），而不需要遍历堆。

**平衡**：每次插入或删除后，可能导致两堆大小不平衡（差距大于 1），我们通过移动堆顶元素来恢复平衡。

整个过程每一步的复杂度都是 `O(log k)`，窗口总共移动 `n - k + 1` 次，整体时间 `O(n log k)`，空间 `O(k)`。

#### 代码（Python）

```python
import heapq
from collections import defaultdict
from typing import List

def median_sliding_window(nums: List[int], k: int) -> List[float]:
    """
    使用两个堆（大根堆 + 小根堆）和懒删除实现 O(n log k) 的解法
    """
    # Python 的 heapq 只有小根堆，利用负数实现大根堆
    low = []                     # max-heap (store as -value)
    high = []                    # min-heap
    delayed = defaultdict(int)  # 记录延迟删除的元素及其出现次数
    result: List[float] = []

    def prune(heap):
        """弹出堆顶已经标记为删除的元素"""
        while heap:
            num = -heap[0] if heap is low else heap[0]
            if delayed[num]:
                # 该元素在 delayed 中，真正删除
                heapq.heappop(heap)
                delayed[num] -= 1
                if delayed[num] == 0:
                    del delayed[num]
            else:
                break

    def balance():
        """保持 len(low) 与 len(high) 的平衡关系"""
        if len(low) > len(high) + 1:
            # low 过大，移动堆顶到 high
            heapq.heappush(high, -heapq.heappop(low))
            prune(low)
        elif len(low) < len(high):
            # high 过大，移动堆顶到 low
            heapq.heappush(low, -heapq.heappop(high))
            prune(high)

    def get_median() -> float:
        """根据当前堆的状态返回中位数"""
        if k % 2 == 1:  # 奇数窗口，low 多一个元素
            return float(-low[0])
        else:           # 偶数窗口，两堆堆顶取平均
            return (-low[0] + high[0]) / 2.0

    # 初始化前 k 个元素
    for i in range(k):
        heapq.heappush(low, -nums[i])
    # 把 low 中多余的元素搬到 high，使两堆平衡
    for _ in range(k // 2):
        heapq.heappush(high, -heapq.heappop(low))

    result.append(get_median())

    # 开始滑动窗口
    for i in range(k, len(nums)):
        out_num = nums[i - k]   # 窗口左侧要移出的数
        in_num = nums[i]        # 窗口右侧进来的数

        # 标记要删除的元素（懒删除）
        if out_num <= -low[0]:
            # out_num 在 low（左堆）里
            delayed[out_num] += 1
            if out_num == -low[0]:
                prune(low)      # 立即清理堆顶
        else:
            delayed[out_num] += 1
            if high and out_num == high[0]:
                prune(high)

        # 插入新元素
        if in_num <= -low[0]:
            heapq.heappush(low, -in_num)
        else:
            heapq.heappush(high, in_num)

        # 重新平衡两堆大小
        balance()
        # 再次平衡（因为删除可能导致大小再次失衡）
        balance()

        result.append(get_median())

    return result
```

#### 复杂度  

- **时间复杂度**：`O(n log k)`  
  > 每次窗口移动只做常数次堆的插入、弹出和“懒删除”，每个操作都是 `log k`，所以整体随 `n` 线性增长。相比暴力解的 `O(n·k·log k)`，大幅降低了乘数 `k`。  
- **空间复杂度**：`O(k)`  
  > 两个堆最多各保存约 `k/2` 个元素，加上 `delayed` 哈希表最多也只会记录窗口中已“标记删除”但尚未弹出的元素，整体与窗口大小成正比。

---

## 心得

- **核心技巧**：利用**两堆（大根堆 + 小根堆）保持有序分区**，并配合**懒删除**实现在滑动窗口中快速维护中位数。  
- **适用的题型**  
  1. “滑动窗口第 K 小/大元素”——同样可以用两堆或有序容器实现。  
  2. “动态数据流的中位数”——实时插入、查询中位数的典型场景。  
  3. “区间统计（如第 K 大）”——结合平衡二叉搜索树（TreeMap）或有序集合的思路。  
- **一句话总结**：**把窗口分成左小右大两堆，堆顶随时给你中位数**。

---

## 反思

- **第一反应**：直接把窗口里的数全部排序，然后取中位数——最自然但效率低下。  
- **最容易踩的坑**  
  - **删除元素的实现**：堆不支持任意位置删除，若不使用懒删除会导致 `O(k)` 的额外成本。  
  - **平衡堆的细节**：在奇偶窗口大小转换时，需要确保 `low` 可能比 `high` 多一个元素，否则中位数会算错。  
  - **负数实现大根堆**：忘记对取堆顶取负会导致错误的比较。  
- **下次类似题的第一步**：**先思考“如何在 O(log k) 内维护有序结构”**——如果能把数据分成两块并快速得到“中间位置”，大多数滑动窗口统计问题都能转化为堆或平衡树的操作。