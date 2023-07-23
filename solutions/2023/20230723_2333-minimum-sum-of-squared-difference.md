# #2333. 最小平方差之和 / Minimum Sum of Squared Difference

> 难度：中等 · 标签：Array、Binary Search、Greedy、Sorting、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/minimum-sum-of-squared-difference/)

---

## 题目（英文原版）

**Description**

You are given two positive 0-indexed integer arrays nums1 and nums2, both of length n.
The sum of squared difference of arrays nums1 and nums2 is defined as the sum of (nums1[i] - nums2[i])2 for each 0 <= i < n.
You are also given two positive integers k1 and k2. You can modify any of the elements of nums1 by +1 or -1 at most k1 times. Similarly, you can modify any of the elements of nums2 by +1 or -1 at most k2 times.
Return the minimum sum of squared difference after modifying array nums1 at most k1 times and modifying array nums2 at most k2 times.
Note: You are allowed to modify the array elements to become negative integers.

**Examples**

**Example 1:**

```
Input: nums1 = [1,2,3,4], nums2 = [2,10,20,19], k1 = 0, k2 = 0
Output: 579
Explanation: The elements in nums1 and nums2 cannot be modified because k1 = 0 and k2 = 0. 
The sum of square difference will be: (1 - 2)2 + (2 - 10)2 + (3 - 20)2 + (4 - 19)2 = 579.
```

**Example 2:**

```
Input: nums1 = [1,4,10,12], nums2 = [5,8,6,9], k1 = 1, k2 = 1
Output: 43
Explanation: One way to obtain the minimum sum of square difference is: 
- Increase nums1[0] once.
- Increase nums2[2] once.
The minimum of the sum of square difference will be: 
(2 - 5)2 + (4 - 8)2 + (10 - 7)2 + (12 - 9)2 = 43.
Note that, there are other ways to obtain the minimum of the sum of square difference, but there is no way to obtain a sum smaller than 43.
```

**Constraints**

- n == nums1.length == nums2.length
- 1 <= n <= 105
- 0 <= nums1[i], nums2[i] <= 105
- 0 <= k1, k2 <= 109

---

## 题目（中文翻译）

给定两个正整数数组 `nums1` 和 `nums2`（均为 0 起始下标），长度均为 `n`。  
数组 `nums1` 与 `nums2` 的 **平方差之和**（sum of squared difference）定义为  
\[
\sum_{i=0}^{n-1} ( \text{nums1}[i] - \text{nums2}[i] )^2
\]  
再给定两个正整数 `k1` 和 `k2`。你可以对 `nums1` 中的任意元素执行 **加 1** 或 **减 1** 的操作，至多 `k1` 次；同理，`nums2` 中的任意元素可以执行加 1 或减 1 的操作，至多 `k2` 次。  
返回在最多对 `nums1` 进行 `k1` 次、对 `nums2` 进行 `k2` 次修改后能够得到的 **最小平方差之和**。  

> 注意：数组元素可以被修改为负整数。

### 示例

#### 示例 1
```text
Input: nums1 = [1,2,3,4], nums2 = [2,10,20,19], k1 = 0, k2 = 0
Output: 579
Explanation: 由于 k1 = 0 且 k2 = 0，数组中的元素无法被修改。  
平方差之和为：(1 - 2)² + (2 - 10)² + (3 - 20)² + (4 - 19)² = 579。
```

#### 示例 2
```text
Input: nums1 = [1,4,10,12], nums2 = [5,8,6,9], k1 = 1, k2 = 1
Output: 43
Explanation: 获得最小平方差之和的一种方式是：  
- 将 `nums1[0]` 增加 1；  
- 将 `nums2[2]` 增加 1。  

此时平方差之和为：(2 - 5)² + (4 - 8)² + (10 - 7)² + (12 - 9)² = 43。  
（还有其他操作方式也能得到相同的最小值。） 
```

### 约束条件
- `n == nums1.length == nums2.length`
- `1 <= n <= 10^5`
- `0 <= nums1[i], nums2[i] <= 10^5`
- `0 <= k1, k2 <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

我们先把两个数组对应位置的差值算出来，记作  

```
diff[i] = |nums1[i] - nums2[i]|      # 绝对值，表示差的大小
```

题目说每一次操作可以把 **任意** 一个元素加 1 或减 1（不管是 `nums1` 还是 `nums2`），其实等价于把某个 `diff[i]` **减 1**（因为把 `nums1[i]` 加 1 相当于把两者差距缩小 1，或者把 `nums2[i]` 减 1 也是同样的效果）。  

> **类比**：把 `diff` 看成一排装满糖果的盒子，盒子里糖果越多，代表这两个位置的差距越大。我们有 `k = k1 + k2` 次机会，每次可以从糖果最多的盒子里拿走一颗糖（让差距减 1），目标是让所有盒子里的糖尽可能少，最后求每个盒子糖数的平方和。

最直观的做法是：  
1. 计算所有 `diff[i]` 并放进一个普通列表。  
2. 重复 `k = k1 + k2` 次：  
   - 线性扫描整个列表，找出当前最大的 `diff`（最甜的盒子）。  
   - 把它减 1（如果已经是 0，就保持 0，因为再减会让差距变负，平方后仍然是正数，等价于把差距增大，显然不是最优）。  
3. 最后把所有 `diff[i]` 的平方求和返回。

**为什么这个方法一定能得到正确答案？**  
因为每一次我们都把「当前最大」的差距缩小 1。若把操作花在一个更小的差距上，最大差距仍然保持不变，整体的平方和会更大（平方函数是凸的，大数的平方增长更快），所以贪心地削减最大差距是合理的。

**时间 / 空间复杂度的大白话**  
- 时间复杂度：我们要遍历 `k` 次，每次都要在 `n` 个数里找最大值，所以是 `O(k·n)`。如果 `k` 很大（题目允许 `10^9`），这会非常慢。  
- 空间复杂度：只需要存放 `n` 个差值，`O(n)` 的额外空间。

#### 代码（Python）

```python
from typing import List

def min_squared_diff_bruteforce(nums1: List[int], nums2: List[int],
                               k1: int, k2: int) -> int:
    n = len(nums1)
    # 1. 计算初始差的绝对值
    diff = [abs(nums1[i] - nums2[i]) for i in range(n)]

    k = k1 + k2                     # 总操作次数

    # 2. 贪心地每次把最大的 diff 减 1
    for _ in range(k):
        # 线性扫描找最大值的下标
        max_idx = 0
        for i in range(1, n):
            if diff[i] > diff[max_idx]:
                max_idx = i
        # 把最大 diff 减 1，不能小于 0
        if diff[max_idx] > 0:
            diff[max_idx] -= 1

    # 3. 计算平方和
    return sum(d * d for d in diff)
```

> **关键行注释**  
> - `diff = [abs(...)]`：把“两个数的差”变成“差的大小”，因为我们只关心距离。  
> - `max_idx = ...` 循环：在所有差值里挑出最大的那个。  
> - `if diff[max_idx] > 0: diff[max_idx] -= 1`：已经是 0 了就不再减，避免出现负数（负数的绝对值同样是正的，减负数等价于增加差距，显然不想这么做）。

#### 复杂度  

- **时间复杂度**：`O(k·n)`  
  - 设 `k = k1 + k2`。每一次操作都要遍历一遍长度为 `n` 的数组找最大值，等价于“把 `k` 次循环和 `n` 次遍历乘在一起”。  
- **空间复杂度**：`O(n)`  
  - 只用了一个长度为 `n` 的 `diff` 列表来存放差值。

---

### 2. 最优解  

#### 思路  

**瓶颈在哪里？**  
在暴力解里，找最大差值的那一步用了 **线性扫描**，导致每次操作都要遍历 `n` 个元素。若 `k` 很大，这一步会成为死亡循环。

**优化思路——用“优先队列（堆）”把最大值找出来**  

- **堆的概念**：想象一堆石子，最大（或最小）的那颗总是放在最顶上，取出或放入新石子只需要少量搬动，而不必把所有石子都搬一遍。  
- 在 Python 中，`heapq` 实现的是 **最小堆**，我们可以把每个差值取负数（`-diff`），这样负数最小的其实对应原来最大的 `diff`。  

**完整的贪心+堆算法**  

1. 计算所有 `diff[i] = |nums1[i] - nums2[i]|`。  
2. 把每个 `diff[i]` 的负数压进最小堆 `heap`（相当于最大堆）。  
3. 总操作次数 `k = k1 + k2`。对每一次：  
   - 弹出堆顶（即当前最大的差值）`cur = -heapq.heappop(heap)`。  
   - 如果 `cur` 为 0，说明所有差距已经为 0，后面的操作再怎么也不会让平方和变小，直接退出循环。  
   - 否则把 `cur` 减 1（让差距更小），再把 `-cur` 放回堆中。  
4. 循环结束后，堆里剩下的都是最终的差值（取负后再取绝对值），把它们的平方求和返回。  

**为什么这一步是最优的？**  

- **贪心的正确性**：每一次我们都挑最大的差距来减 1。因为平方函数是凸的（大数的平方比小数的平方增长更快），把一次单位的“努力”放在最大的地方，能让整体平方和下降最多。  
- **堆的优势**：堆能在 `O(log n)` 时间内完成“取最大值”和“放回新值”两步，而不是 `O(n)`。于是总时间降为 `O(k log n)`，即使 `k` 达到 `10^9`，只要 `k` 大到超过 `max(diff) * n`（即所有差距都已经降到 0），我们会提前结束循环，实际操作次数不会真的这么大。

**另一种思路——二分答案 + 前缀计数**（这里不展开实现，只作提示）  
因为我们只关心每个差距最终会被削减到多少，实际上可以在 **[0, max(diff)]** 区间上二分寻找一个阈值 `mid`，使得把所有差距削减到不超过 `mid` 所需的操作数恰好不超过 `k`。这是一种 “把差距压到某个上限” 的思路，配合计数数组可以做到 `O(max(diff) + log max(diff))`。但对初学者来说，堆实现更直观。

#### 代码（Python）

```python
import heapq
from typing import List

def min_squared_diff(nums1: List[int], nums2: List[int],
                    k1: int, k2: int) -> int:
    """
    贪心 + 最大堆（用负数实现）求最小的平方差和
    """
    n = len(nums1)
    # 1. 计算初始差的绝对值
    diff = [abs(nums1[i] - nums2[i]) for i in range(n)]

    # 2. 把每个差值的负数放进最小堆，等价于最大堆
    #    heap[0] 永远是负数中最小的，也就是原差值中最大的
    heap = [-d for d in diff]
    heapq.heapify(heap)          # O(n) 建堆

    k = k1 + k2                   # 总操作次数

    # 3. 逐次把最大的 diff 减 1
    for _ in range(k):
        # 取出当前最大的差值（记得取负号恢复正数）
        cur = -heapq.heappop(heap)

        if cur == 0:              # 所有差距已经为 0，后面再操作也无效
            # 把 0 放回堆里，后面的循环直接 break
            heapq.heappush(heap, 0)
            break

        cur -= 1                  # 把最大的差值减 1
        heapq.heappush(heap, -cur)  # 再放回堆中（仍然用负数）

    # 4. 计算最终的平方和
    #    堆里存的是负数，取负号再平方即可
    return sum((-x) * (-x) for x in heap)
```

> **关键行注释**  
> - `heap = [-d for d in diff]`：把每个差值取负数，利用 Python 的 **最小堆** 来模拟 **最大堆**。  
> - `heapq.heapify(heap)`：一次性把列表变成堆，时间是 `O(n)`，比逐个 `heappush` 更快。  
> - `cur = -heapq.heappop(heap)`：弹出堆顶（最小的负数），再取负得到真正的最大差值。  
> - `if cur == 0: … break`：所有差距已经是 0，继续操作只能把 0 减成负数再取绝对值，平方和不变，直接退出可省时。  
> - `heapq.heappush(heap, -cur)`：把更新后的差值（仍然取负）放回堆，保持堆的性质。  

#### 复杂度  

- **时间复杂度**：`O(k log n)`（最坏情况），其中 `k = k1 + k2`。  
  - 堆的 `heappop` 与 `heappush` 各是 `O(log n)`，循环 `k` 次。  
  - 实际上，当所有差距被削减到 0 时会提前 `break`，所以真正的循环次数 ≤ `sum(diff)`，在题目约束下依然可接受。  
- **空间复杂度**：`O(n)`  
  - 需要存放 `diff`（或直接在堆里）共 `n` 个整数。  

与暴力解相比，时间从 `O(k·n)` 降到了 `O(k log n)`，对大规模数据提升巨大。

---

## 心得  

- **核心技巧**：**贪心 + 最大堆**（或等价的计数/二分）  
  - 每一次操作都针对当前“差距最大”的位置进行，能够最快降低整体的平方和。  
- **适用的题型**（类似思路可迁移）：  
  1. *Minimize the Maximum Difference*（把最大差距压到最小）  
  2. *Reduce Array Sum with Operations*（每次减 1/加 1，目标是最小化某个函数）  
  3. *Maximum Product after K Increments*（利用堆把最小值提升）  
- **一句话总结解题钥匙**：**把所有操作都用在“当前差距最大的下标”，用堆快速找最大即可**。

---

## 反思  

- **第一反应**：看到可以对两个数组的每个元素自由加减，立刻想到把差值 `|a-b|` 当作可直接操作的对象。  
- **最容易踩的坑**：  
  - 忽略了 `k` 可能远大于所有差距之和，导致无限循环。必须在 `cur == 0` 时提前退出。  
  - 只在 `nums1` 或 `nums2` 上做加减，而忘记两者等价，实际上可以把两者的操作次数合并成 `k = k1 + k2`。  
  - 计算平方和时忘记把负数恢复正数，导致错误的负数平方。  
- **下次类似题的第一步**：先把“可直接操作的量”（这里是绝对差）抽象出来，然后思考“每一次操作应该放在哪个位置”——往往是 **最大/最小** 那个，随后选用 **堆** 或 **计数** 来高效维护。