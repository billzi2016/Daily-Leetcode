# #632. 最小覆盖 K 个列表元素的区间 / Smallest Range Covering Elements from K Lists

> 难度：困难 · 标签：Array、Hash Table、Greedy、Sliding Window、Sorting、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/smallest-range-covering-elements-from-k-lists/)

---

## 题目（英文原版）

**Description**

You have k lists of sorted integers in non-decreasing order. Find the smallest range that includes at least one number from each of the k lists.
We define the range [a, b] is smaller than range [c, d] if b - a < d - c or a < c if b - a == d - c.

**Examples**

**Example 1:**

```
Input: nums = [[4,10,15,24,26],[0,9,12,20],[5,18,22,30]]
Output: [20,24]
Explanation: 
List 1: [4, 10, 15, 24,26], 24 is in range [20,24].
List 2: [0, 9, 12, 20], 20 is in range [20,24].
List 3: [5, 18, 22, 30], 22 is in range [20,24].
```

**Example 2:**

```
Input: nums = [[1,2,3],[1,2,3],[1,2,3]]
Output: [1,1]
```

**Constraints**

- nums.length == k
- 1 <= k <= 3500
- 1 <= nums[i].length <= 50
- -105 <= nums[i][j] <= 105
- nums[i] is sorted in non-decreasing order.

---

## 题目（中文翻译）

你有 **k** 个已按非递减顺序（non‑decreasing order）排序的整数列表。请找出包含每个列表中至少一个数字的最小区间（range）。

我们定义区间 \[a, b\] 小于区间 \[c, d\] 当且仅当满足以下任一条件：

- b - a < d - c  
- b - a == d - c 且 a < c  

---

### 示例

#### 示例 1  
**输入**  
```text
nums = [[4,10,15,24,26],[0,9,12,20],[5,18,22,30]]
```  

**输出**  
```text
[20,24]
```  

**解释**  
- 列表 1: [4, 10, 15, 24, 26]，其中 24 落在区间 \[20,24\] 内。  
- 列表 2: [0, 9, 12, 20]，其中 20 落在区间 \[20,24\] 内。  
- 列表 3: [5, 18, 22, 30]，其中 22 落在区间 \[20,24\] 内。  

#### 示例 2  
**输入**  
```text
nums = [[1,2,3],[1,2,3],[1,2,3]]
```  

**输出**  
```text
[1,1]
```  

---

### 约束条件

- `nums.length == k`
- `1 <= k <= 3500`
- `1 <= nums[i].length <= 50`
- `-10^5 <= nums[i][j] <= 10^5`
- `nums[i]` 已按非递减顺序（non‑decreasing order）排序。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每个列表都选出一个数**，然后看这 `k` 个数的最大值与最小值之差，就是一个可能的区间。把所有可能的选法枚举一遍，取区间最短的那一个即可。

- **数据结构**  
  - `列表`：把每个列表想成一个装有若干“水果”的筐，我们要从每个筐里挑一个水果。  
  - `笛卡尔积`（`itertools.product`）：把所有筐的挑选方式全部列出来，就像把每种挑选方式写成一行表格。  
  - `min / max`：把挑出来的 `k` 个数分别找出最小和最大，就像在一堆水果里找出最小的重量和最大的重量。

- **为什么正确**  
  只要遍历了**所有**可能的挑选方式，就一定能找到包含每个列表至少一个元素且长度最小的区间。因为没有任何挑选被遗漏，最优解一定在枚举的结果里。

- **时间/空间复杂度**  
  - 假设第 `i` 个列表的长度为 `n_i`，总的组合数是 `N = n_1 * n_2 * … * n_k`。  
  - 对每一种组合我们都要遍历 `k` 个数求最小、最大，时间是 `O(k)`。  
  - 因此 **时间复杂度** 为 `O(N * k)`，在最坏情况下会呈指数级增长（比如 `k=5`、每个列表长度为 `50`，组合数就已经是 `50⁵` 了）。  
  - **空间复杂度** 只需要存放一次组合的 `k` 个数以及递归/迭代的栈，约为 `O(k)`。

> **大白话**：  
> `O(N * k)` 就像说“我们得把所有可能的选法全部试一遍”，如果选法很多（指数级），这件事几乎不可能在电脑里跑完。

#### 代码（Python）

```python
import itertools
from typing import List

def smallestRange_bruteforce(nums: List[List[int]]) -> List[int]:
    """
    暴力枚举每个列表的一个元素，返回最小覆盖区间。
    只适用于非常小的输入（比如 k<=3, 每个列表长度<=5）。
    """
    k = len(nums)
    best_range = [-10**6, 10**6]          # 初始一个很大的区间
    best_len = best_range[1] - best_range[0]

    # itertools.product 会产生所有可能的 (a1, a2, ..., ak) 组合
    for combo in itertools.product(*nums):
        cur_min = min(combo)              # 这 k 个数的最小值
        cur_max = max(combo)              # 这 k 个数的最大值
        cur_len = cur_max - cur_min

        # 如果当前区间更短，或者长度相等但左端点更小，就更新答案
        if cur_len < best_len or (cur_len == best_len and cur_min < best_range[0]):
            best_range = [cur_min, cur_max]
            best_len = cur_len

    return best_range
```

#### 复杂度

- **时间复杂度**：`O(N * k)`，其中 `N = Π len(nums[i])` 为所有组合数。  
  > 也就是说，随着列表数量或每个列表长度的增加，运行时间会指数级爆炸。
- **空间复杂度**：`O(k)`，仅存放一次组合的 `k` 个数和常数级辅助变量。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于枚举所有组合**。实际上我们不需要把所有挑选方式都列出来，只要**一次遍历**就能找出最小区间。关键观察有两点：

1. **每个列表本身是有序的**（非递减）。这意味着如果我们已经选了某个列表的第 `i` 个元素，那么下一个更大的选择只能是第 `i+1` 个元素。  
2. **区间长度只由当前选中的最小值和最大值决定**。如果我们把所有列表的当前选中元素放进一个最小堆（heap），堆顶就是当前最小值，堆里所有元素的最大值我们可以用一个变量 `current_max` 维护。

基于上述观察，我们可以采用**“滑动窗口 + 最小堆”**的思路：

- **初始化**：把每个列表的第一个元素放进最小堆，同时记录这 `k` 个数的最大值 `current_max`。此时堆里有 `k` 个元素，分别来自不同的列表。
- **循环**  
  1. 取出堆顶（最小值）`min_val`，此时区间 `[min_val, current_max]` 包含了每个列表至少一个数。更新最优答案（如果更短或左端点更小）。  
  2. 为了尝试让区间更窄，我们必须**把最小的那个数换成它所在列表的下一个更大的数**。如果该列表已经没有更多元素，说明所有可能的区间都已经遍历完，结束循环。  
  3. 把新的元素插入堆中，同时更新 `current_max = max(current_max, new_val)`。这样堆始终保持 `k` 个元素，且每个列表恰好贡献一个数。

- **结束**：当任意一个列表的元素被耗尽时，已经没有办法再得到覆盖所有列表的区间，循环结束，返回记录的最优区间。

**核心数据结构解释**  

- **最小堆（Priority Queue）**：想象成一个“最小值自动排在最前面的排队系统”。每次我们只需要 O(log k) 的时间取出最小值并插入新值。  
- **滑动窗口**：这里的窗口指的是当前堆里 `k` 个数对应的数轴区间。窗口的左端是堆顶（最小值），右端是 `current_max`（最大值），我们不断“滑动”左端来尝试更小的区间。

**为什么它是最优的**  

- 每次循环只做 **O(log k)** 的堆操作，整个过程遍历的元素总数是所有列表的元素总和 `N = Σ len(nums[i])`，所以时间是 `O(N log k)`。  
- 只使用了一个堆和几个整数变量，空间是 `O(k)`（堆里恰好存 `k` 条记录），远小于暴力解的指数级空间。

#### 代码（Python）

```python
import heapq
from typing import List, Tuple

def smallestRange(nums: List[List[int]]) -> List[int]:
    """
    使用最小堆 + 滑动窗口，时间 O(N log k)，空间 O(k)。
    N = 所有列表元素的总数，k = 列表个数。
    """
    k = len(nums)
    # 每个堆元素为 (值, 所属列表编号, 在该列表中的下标)
    min_heap: List[Tuple[int, int, int]] = []
    current_max = -10**6  # 记录堆中所有元素的最大值

    # 1️⃣ 初始化：把每个列表的第一个元素放进堆
    for i, lst in enumerate(nums):
        val = lst[0]
        heapq.heappush(min_heap, (val, i, 0))
        current_max = max(current_max, val)

    # 记录最好的区间，初始区间设为一个很大的范围
    best_left, best_right = -10**6, 10**6

    while True:
        # 2️⃣ 取出当前最小值（堆顶），这就是窗口左端
        current_min, list_id, idx_in_list = heapq.heappop(min_heap)

        # 3️⃣ 检查并更新最优答案
        if current_max - current_min < best_right - best_left or \
           (current_max - current_min == best_right - best_left and current_min < best_left):
            best_left, best_right = current_min, current_max

        # 4️⃣ 把该列表的下一个元素加入堆中
        if idx_in_list + 1 == len(nums[list_id]):   # 已经到该列表的末尾，结束
            break
        next_val = nums[list_id][idx_in_list + 1]
        heapq.heappush(min_heap, (next_val, list_id, idx_in_list + 1))
        # 更新窗口右端
        current_max = max(current_max, next_val)

    return [best_left, best_right]
```

#### 复杂度

- **时间复杂度**：`O(N log k)`  
  - `N = Σ len(nums[i])` 是所有数的总数。每个数只会被插入堆一次、弹出一次，堆操作的代价是 `log k`（因为堆里始终只有 `k` 条记录）。  
  - 与暴力解的指数级 `O(N * k)` 相比，这个复杂度在输入规模稍大的情况下也能在毫秒级完成。

- **空间复杂度**：`O(k)`  
  - 堆里恰好保存 `k` 条记录（每个列表一个），再加几个整数变量，整体空间随 `k` 线性增长。  
  - 对比暴力解需要记住所有组合，节省了巨量的内存。

---

## 心得

- **核心技巧**：**最小堆 + 滑动窗口**（也叫 “k路归并”），利用每个列表有序的特性，只保留每个列表当前的候选元素。
- **适用的题型**  
  1. “合并 k 个有序链表” / “找第 K 小的数”——同样用最小堆一次取最小。  
  2. “最小区间包含 K 类元素”——类似本题，只是元素来源不同。  
  3. “最长连续子数组满足条件”——使用滑动窗口的思想，只是这里的窗口是基于堆的。
- **一句话总结解题钥匙**：  
  *“把每个列表的当前最小候选放进最小堆，始终维护窗口的最大值，弹出最小值并向前推进该列表，即可在一次遍历中找到最小覆盖区间。”*

---

## 反思

- **第一反应**：看到“k 个已排序数组”，自然想到“归并”或“堆”这种可以一次遍历全部元素的技巧，而不是直接枚举所有组合。
- **最容易踩的坑**  
  - **忘记更新 `current_max`**：只看堆顶会导致区间宽度计算错误。  
  - **边界条件**：当某个列表已经没有后继元素时必须立即结束循环，否则会尝试访问越界。  
  - **相等区间长度的比较**：题目要求长度相同则左端点更小的区间更好，需要在代码里显式处理。
- **下次遇到同类题的第一步**：  
  *先把每个集合（列表、链表、字符集等）的“当前代表元素”放进最小堆，维护一个全局的最大值，然后在弹出最小值后推进对应集合的指针。*   This “堆 + 窗口”的框架几乎可以直接套用。