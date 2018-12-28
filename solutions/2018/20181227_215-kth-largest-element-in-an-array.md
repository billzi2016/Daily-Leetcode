# #215. 数组中的第 K 大元素 / Kth Largest Element in an Array

> 难度：中等 · 标签：Array、Divide and Conquer、Sorting、Heap (Priority Queue)、Quickselect · [LeetCode 链接](https://leetcode.com/problems/kth-largest-element-in-an-array/)

---

## 题目（英文原版）

**Description**

Given an integer array nums and an integer k, return the kth largest element in the array.
Note that it is the kth largest element in the sorted order, not the kth distinct element.
Can you solve it without sorting?

**Examples**

**Example 1:**

```
Input: nums = [3,2,1,5,6,4], k = 2
Output: 5
```

**Example 2:**

```
Input: nums = [3,2,3,1,2,4,5,5,6], k = 4
Output: 4
```

**Constraints**

- 1 <= k <= nums.length <= 105
- -104 <= nums[i] <= 104

---

## 题目（中文翻译）

给定一个整数数组 `nums` 和一个整数 `k`，返回数组中第 `k` 大的元素。  
注意这里指的是在排序后的顺序中的第 `k` 大元素，而 **不是** 第 `k` 个不同的元素。  
能否在不进行整体排序的情况下实现？

**示例 1**  
**示例 2**  
**约束条件**  

**示例**  
**示例 1:**  
```
Input: nums = [3,2,1,5,6,4], k = 2
Output: 5
```

**示例 2:**  
```
Input: nums = [3,2,3,1,2,4,5,5,6], k = 4
Output: 4
```

**约束条件**  
- `1 <= k <= nums.length <= 10^5`  
- `-10^4 <= nums[i] <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把数组全部排好序，然后直接取第 `k` 大的那个数。  
- **使用的数据结构**：Python 的列表（list）本身就像一本可以随时翻页的笔记本，`list.sort()` 就相当于把笔记本里的所有页码排成从小到大的顺序。  
- **为什么正确**：排好序后，第 `k` 大的元素就在固定位置——如果从小到大排好序，`len(nums) - k` 这个下标对应的就是第 `k` 大的数。  
- **复杂度分析**：  
  - 排序的时间大约是 `O(n log n)`，这里的 `n` 是数组长度。可以把 `log n` 想象成“每次把问题规模减半需要的步骤数”，所以整体时间是“每个元素都要参与一次比较，比较的次数随 `n` 的对数增长”。  
  - 额外的空间主要是排序时可能用到的临时数组，最坏情况下是 `O(n)`（如果使用额外的辅助空间），但 Python 原地排序一般是 `O(1)` 额外空间。

#### 代码（Python）

```python
def findKthLargest(nums, k):
    """
    暴力解法：先排序，再直接索引第 k 大的元素
    :param nums: List[int] 待查找的数组
    :param k: int 要找的第 k 大
    :return: int 第 k 大的数值
    """
    # 1. 对数组进行原地升序排序（小到大）
    nums.sort()                     # Python 内置的 Timsort，时间复杂度 O(n log n)

    # 2. 第 k 大的元素在排序后的位置是 len(nums) - k
    return nums[-k]                  # -k 表示倒数第 k 个，即第 k 大
```

#### 复杂度  

- **时间复杂度**：`O(n log n)` —— 排序是主要耗时，`log n` 代表每次把数据分成两半的过程。  
- **空间复杂度**：`O(1)`（若使用原地排序）或 `O(n)`（若排序实现需要额外数组），这里我们假设使用原地排序，所以额外空间几乎为常数。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**完整排序**，其实我们只需要第 `k` 大的那个数，而不必把所有元素都排好序。  
从暴力思路出发，可以逐步优化：

1. **使用最大堆 / 最小堆**  
   - 维护一个大小为 `k` 的 **最小堆**（最小堆的根是堆中最小的元素）。  
   - 当遍历数组时，把元素依次放进堆；如果堆的大小超过 `k`，就把最小的元素（根）弹出。  
   - 这样堆里始终保存 **当前最大的 k 个数**，遍历结束后堆顶就是第 `k` 大的数。  
   - 堆可以类比为“只保留最贵的 k 件商品的仓库”，每次有更贵的商品进来，就把最便宜的踢出去。

2. **快速选择（Quickselect）**  
   - 快速选择是基于 **快速排序** 的划分思想，只递归处理可能包含第 `k` 大元素的那一半。  
   - 具体做法：随机选一个枢轴（pivot），把数组分成左侧（<= 枢轴）和右侧（> 枢轴）两部分。  
   - 如果右侧的元素个数恰好是 `k-1`，则枢轴就是答案；如果右侧元素太少，就在左侧继续找第 `(k - right_len - 1)` 大的；如果右侧元素太多，就在右侧继续找第 `k` 大的。  
   - 这样每一步都把搜索空间 **至少减半**，平均时间是 `O(n)`，最坏情况（枢轴选得极端）会退化到 `O(n²)`，但我们通过随机化枢轴可以把最坏概率降到极低。

下面分别给出两种最优实现，读者可以根据实际需求选用。

#### 代码（Python）—— 最小堆实现

```python
import heapq

def findKthLargest(nums, k):
    """
    最小堆（大小为 k）实现第 k 大元素
    思路：维护一个只装 k 个最大数的堆，堆顶始终是第 k 大
    """
    # 1. 建立一个空的最小堆
    min_heap = []

    for num in nums:
        # 2. 把当前元素加入堆
        heapq.heappush(min_heap, num)   # O(log k) 的插入

        # 3. 若堆的大小超过 k，弹出最小的元素
        if len(min_heap) > k:
            heapq.heappop(min_heap)     # O(log k) 的删除

    # 4. 循环结束后，堆里恰好是最大的 k 个数，堆顶即第 k 大
    return min_heap[0]
```

#### 代码（Python）—— Quickselect 实现

```python
import random

def findKthLargest(nums, k):
    """
    Quickselect（快速选择）实现第 k 大元素
    通过随机划分把问题规模逐步减半，平均线性时间 O(n)
    """
    # 将第 k 大转化为第 (len(nums) - k) 小（因为快速选择默认找第 i 小）
    target = len(nums) - k

    def quickselect(left, right):
        """
        在 nums[left:right+1] 区间内寻找第 target 小的元素
        """
        # 1. 随机挑选枢轴并放到区间最右侧
        pivot_index = random.randint(left, right)
        nums[pivot_index], nums[right] = nums[right], nums[pivot_index]

        # 2. 把小于等于枢轴的放左边，大于枢轴的放右边
        pivot = nums[right]
        i = left          # i 指向下一个应放置“小于等于”区的下标
        for j in range(left, right):
            if nums[j] <= pivot:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
        # 把枢轴放到它最终的位置
        nums[i], nums[right] = nums[right], nums[i]

        # 3. 判断枢轴所在位置 i 是否就是目标下标
        if i == target:
            return nums[i]               # 找到第 target 小，即第 k 大
        elif i < target:
            # 目标在右侧区间
            return quickselect(i + 1, right)
        else:
            # 目标在左侧区间
            return quickselect(left, i - 1)

    return quickselect(0, len(nums) - 1)
```

#### 复杂度  

- **最小堆实现**  
  - 时间复杂度：`O(n log k)` —— 遍历 `n` 个元素，每次插入/弹出堆的代价是 `log k`（因为堆的大小最多是 `k`）。如果 `k` 远小于 `n`，这会比完整排序快很多。  
  - 空间复杂度：`O(k)` —— 只保存 `k` 个元素的堆。

- **Quickselect 实现**  
  - 时间复杂度：**平均** `O(n)` —— 每次划分都把问题规模大约减半，类似二分查找的思想。可以把 `O(n)` 想象成“只需要遍历一次数组”。  
  - 空间复杂度：`O(1)`（递归栈的深度平均是 `log n`，可以看作常数级别的额外空间）。  

与暴力解的 `O(n log n)` 相比，堆方案在 `k` 较小的情况下更快，Quickselect 在大多数随机输入下则是线性时间的最佳选择。

---

## 心得

- **核心技巧**：利用**堆**或**快速选择**在不完整排序的情况下定位第 `k` 大元素。  
- **适用的类似题型**：  
  1. “第 k 小的元素”（LeetCode 215 同题，只是顺序相反）  
  2. “前 K 大/小元素”（如 Top K Frequent Elements）  
  3. “滑动窗口最大值”（需要维护固定大小的最大堆或单调队列）  
- **一句话总结**：**把“只要第 k 大”转化为“只保留最有价值的 k 项”，用堆或快速选择即可高效实现。**

---

## 反思

- **第一反应**：直接把数组排序，然后取对应下标。  
- **最容易踩的坑**：  
  - 忘记把 “第 k 大” 转换为 “第 (n‑k) 小” 在 Quickselect 中使用；  
  - 堆实现时忘记在插入后检查堆的大小，导致堆会无限增长；  
  - 对极端输入（如全部相同的数）没有特殊处理，可能导致递归深度过大。  
- **下次遇到同类题**：第一步先思考“是否真的需要完整排序”，如果不需要，立刻联想到**堆**（保留前 K）或**快速选择**（划分递归）这两把钥匙。