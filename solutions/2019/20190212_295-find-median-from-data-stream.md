# #295. 数据流中的中位数 / Find Median from Data Stream

> 难度：困难 · 标签：Two Pointers、Design、Sorting、Heap (Priority Queue)、Data Stream · [LeetCode 链接](https://leetcode.com/problems/find-median-from-data-stream/)

---

## 题目（英文原版）

**Description**

The median is the middle value in an ordered integer list. If the size of the list is even, there is no middle value, and the median is the mean of the two middle values.
Implement the MedianFinder class:
Follow up:

**Examples**

**Example 1:**

```
Input
["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"]
[[], [1], [2], [], [3], []]
Output
[null, null, null, 1.5, null, 2.0]

Explanation
MedianFinder medianFinder = new MedianFinder();
medianFinder.addNum(1);    // arr = [1]
medianFinder.addNum(2);    // arr = [1, 2]
medianFinder.findMedian(); // return 1.5 (i.e., (1 + 2) / 2)
medianFinder.addNum(3);    // arr[1, 2, 3]
medianFinder.findMedian(); // return 2.0
```

**Constraints**

- -105 <= num <= 105
- There will be at least one element in the data structure before calling findMedian.
- At most 5 * 104 calls will be made to addNum and findMedian.

---

## 题目（中文翻译）

**描述**  
中位数（median）是有序整数序列中的中间值。如果序列长度为偶数，则不存在唯一的中间值，此时中位数定义为两个中间值的平均值（mean）。

请实现 **MedianFinder** 类，使其能够：

- `addNum(int num)`：向数据流中添加一个整数 `num`。  
- `findMedian()`：返回当前所有添加数字的中位数。

**示例 1**  

```json
Input
["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"]
[[], [1], [2], [], [3], []]

Output
[null, null, null, 1.5, null, 2.0]
```

**解释**  
```java
MedianFinder medianFinder = new MedianFinder();
medianFinder.addNum(1);    // arr = [1]
medianFinder.addNum(2);    // arr = [1, 2]
medianFinder.findMedian(); // 返回 1.5（即 (1 + 2) / 2）
medianFinder.addNum(3);    // arr = [1, 2, 3]
medianFinder.findMedian(); // 返回 2.0
```

**约束条件**  

- `-10^5 <= num <= 10^5`  
- 在调用 `findMedian` 之前，数据结构中至少已经存在一个元素。  
- `addNum` 和 `findMedian` 的调用次数总计不超过 `5 * 10^4` 次。

**进阶**  
（此处留空，原题目未给出具体内容）

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法就是把所有出现的数字都保存下来，每次要查询中位数时：

1. 把已有的数字 **全部排序**（从小到大）。  
2. 根据当前元素的个数 `n` 判断中位数的取法：  
   - `n` 为奇数时，取排好序后第 `n//2`（从 0 开始计数）的那个数。  
   - `n` 为偶数时，取第 `n//2‑1` 和第 `n//2` 两个数的平均值。  

> **数据结构类比**：把所有数字放进一个“可随时打开的抽屉”，要找中位数时先把抽屉里的东西排好队（排序），再挑中间的一个或两个。  

这个方法之所以 **正确**，是因为中位数的定义本身就是“排好序后正中间的数”。只要我们把数排好序，直接取就能得到答案。  

**为什么会慢**：  
- 每次 `findMedian` 都要重新对全部数据排序，排序的代价是 `O(n log n)`（`n` 为当前元素个数）。  
- 随着数据流的不断增长，这个代价会越来越大。  

#### 代码（Python）

```python
class MedianFinder:
    def __init__(self):
        # 用一个列表保存所有加入的数字
        self.nums = []          # 类似装东西的抽屉

    def addNum(self, num: int) -> None:
        # 直接把新数字放到列表尾部
        self.nums.append(num)   # O(1) 插入

    def findMedian(self) -> float:
        # 1. 先把所有数字排序，得到有序序列
        sorted_nums = sorted(self.nums)   # O(n log n)
        n = len(sorted_nums)

        # 2. 根据奇偶性返回中位数
        if n % 2 == 1:                     # 奇数个
            return float(sorted_nums[n // 2])
        else:                              # 偶数个，取中间两个数的平均值
            mid1 = sorted_nums[n // 2 - 1]
            mid2 = sorted_nums[n // 2]
            return (mid1 + mid2) / 2.0
```

#### 复杂度  

- **时间复杂度**：`O(n log n)`（`findMedian` 时需要排序，`n` 为当前元素数量）  
  - 大白话：如果有 10,000 条数据，要把它们排一次序，大约相当于把 10,000 张卡片两两比较、重新排队的过程，花的时间会随数据量的 **对数** 增长。  
- **空间复杂度**：`O(n)`（保存所有数字的列表）  
  - 大白话：我们把每个数字都装进抽屉，抽屉的大小正好和数字的个数一样。

---  

### 2. 最优解  

#### 思路  

**慢点在哪里？**  
- 暴力解每次 `findMedian` 都要**全局排序**，这一步是瓶颈。  
- 实际上，只要我们在 **插入** 的时候就保持一定的顺序信息，就可以在 **常数时间**（或对数时间）内得到中位数。

**核心思想：使用两个堆（优先队列）**  
- **最大堆**（`maxHeap`）保存**左半边**的所有数，堆顶是左半边的最大值。  
- **最小堆**（`minHeap`）保存**右半边**的所有数，堆顶是右半边的最小值。  

这样设计的好处：

1. 左边的数全部 **≤** 右边的数（因为左边最大 ≤ 右边最小）。  
2. 两个堆的大小始终保持平衡：  
   - 若总数为偶数，两个堆大小相同。  
   - 若总数为奇数，`maxHeap`（左边）比 `minHeap` 多 1。  
3. 只要保持上述平衡，**中位数**就可以直接从堆顶得到：  
   - 偶数时：`(maxHeap.top + minHeap.top) / 2`  
   - 奇数时：`maxHeap.top`（左边多的那个数）  

**实现细节**（一步步推导）  

1. **插入新数**  
   - 先把新数放进 `maxHeap`（左边），因为我们默认左边可以多一个。  
   - 为了保证左边的最大不大于右边的最小，需要把 `maxHeap` 的堆顶（最大）弹出，放进 `minHeap`。  
   - 此时右边可能比左边多 1，若是这样再把 `minHeap` 的堆顶（最小）弹回 `maxHeap`，恢复平衡。  

2. **查找中位数**  
   - 只看堆的大小和堆顶即可，**不需要遍历或排序**。  

> **数据结构类比**：想象有两座山坡，左边山坡的最高点（`maxHeap` 顶）和右边山坡的最低点（`minHeap` 顶）始终相邻。我们每次往左坡放石子，然后把左坡最高的石子搬到右坡，保持两座山的高度差不超过 1。中位数就是两座山坡最高/最低的交界点。  

#### 代码（Python）

```python
import heapq

class MedianFinder:
    def __init__(self):
        # maxHeap 用负数实现（Python 只有最小堆），保存左半边较小的数
        self.maxHeap = []   # 实际上是取负号后的小根堆
        # minHeap 正常使用，保存右半边较大的数
        self.minHeap = []   # 小根堆

    def addNum(self, num: int) -> None:
        """
        1. 先把 num 放进 maxHeap（左半边），因为左边可以多一个
        2. 把 maxHeap 的最大值（即负数堆顶的相反数）移到 minHeap，保证左边所有数 ≤ 右边所有数
        3. 如果 minHeap 变大（比 maxHeap 多 1），再把 minHeap 的最小值移回 maxHeap，恢复平衡
        """
        # step1：放进 maxHeap（注意取负号，使其成为最大堆）
        heapq.heappush(self.maxHeap, -num)               # O(log n)

        # step2：把左边最大的数搬到右边
        # 这里 pop 出来的是负数，取相反数得到真实值
        max_top = -heapq.heappop(self.maxHeap)           # O(log n)
        heapq.heappush(self.minHeap, max_top)            # O(log n)

        # step3：如果右边比左边多，就把右边最小的数搬回左边
        if len(self.minHeap) > len(self.maxHeap):
            min_top = heapq.heappop(self.minHeap)        # O(log n)
            heapq.heappush(self.maxHeap, -min_top)       # O(log n)

    def findMedian(self) -> float:
        """
        根据两个堆的大小返回中位数
        - 若总数为奇数，maxHeap 多一个，堆顶即中位数
        - 若总数为偶数，两堆大小相等，取两个堆顶的平均值
        """
        if len(self.maxHeap) > len(self.minHeap):        # 奇数个数
            return float(-self.maxHeap[0])
        else:                                            # 偶数个数
            return (-self.maxHeap[0] + self.minHeap[0]) / 2.0
```

#### 复杂度  

- **时间复杂度**：`O(log n)`（每次 `addNum` 需要在堆中插入/弹出，堆的高度是 `log n`）  
  - 大白话：像在排队的过程中只需要在 **对数层** 的位置插入或搬走一个元素，远比把所有人重新排队快。  
- **空间复杂度**：`O(n)`（所有数字都要存进两个堆，总数仍然是 `n`）  
  - 大白话：我们仍然要把每个数字记下来，只是把它们分到两座“山坡”上，整体占用的空间跟数据量是线性关系。

---  

## 心得  

- **核心技巧**：利用 **两个堆**（最大堆 + 最小堆）实现 **动态中位数**，保持左半边最大 ≤ 右半边最小，并让两堆大小相差不超过 1。  
- **适用的题型**  
  1. **滑动窗口中位数**（LeetCode 480）——在固定长度窗口内实时求中位数，同样用两堆或平衡树。  
  2. **Kth Largest Element in a Stream**（第 K 大元素）——维护一个大小为 K 的最小堆。  
  3. **数据流中的百分位数**——思路类似，使用多个堆或有序容器维护分位点。  
- **一句话总结解题钥匙**：**“把数据流划分为左小右大两部分，用堆维持局部有序，堆顶即为中位数”。**  

---  

## 反思  

- **第一反应**：看到“数据流”和“随时求中位数”，立刻想到“每次全部排序”。这符合直觉，却忽略了 **实时性** 的要求。  
- **最容易踩的坑**  
  1. **堆的平衡**：忘记在 `addNum` 后检查并恢复两堆大小的平衡，会导致堆顶不再对应中位数。  
  2. **最大堆的实现**：Python 只有最小堆，需要把数取负才能模拟最大堆，容易写错符号。  
  3. **奇偶判断**：在 `findMedian` 时要根据堆的大小判断是取单个堆顶还是取两个堆顶的平均值，遗漏会导致错误的结果。  
- **下次类似题的第一步**：**先划分数据的“左/右”两侧，选合适的有序容器（堆/平衡树）保持两侧大小平衡**，再思考如何从容器的“边界”直接得到答案。