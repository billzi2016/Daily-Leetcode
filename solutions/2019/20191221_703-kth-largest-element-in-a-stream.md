# #703. 流中的第 K 大元素 / Kth Largest Element in a Stream

> 难度：简单 · 标签：Tree、Design、Binary Search Tree、Heap (Priority Queue)、Binary Tree、Data Stream · [LeetCode 链接](https://leetcode.com/problems/kth-largest-element-in-a-stream/)

---

## 题目（英文原版）

**Description**

You are part of a university admissions office and need to keep track of the kth highest test score from applicants in real-time. This helps to determine cut-off marks for interviews and admissions dynamically as new applicants submit their scores.
You are tasked to implement a class which, for a given integer k, maintains a stream of test scores and continuously returns the kth highest test score after a new score has been submitted. More specifically, we are looking for the kth highest score in the sorted list of all scores.
Implement the KthLargest class:

**Examples**

**Example 1:**

```
Input: ["KthLargest", "add", "add", "add", "add", "add"] [[3, [4, 5, 8, 2]], [3], [5], [10], [9], [4]]
Output: [null, 4, 5, 5, 8, 8]
Explanation:
KthLargest kthLargest = new KthLargest(3, [4, 5, 8, 2]); kthLargest.add(3); // return 4 kthLargest.add(5); // return 5 kthLargest.add(10); // return 5 kthLargest.add(9); // return 8 kthLargest.add(4); // return 8
```

**Example 2:**

```
Input: ["KthLargest", "add", "add", "add", "add"] [[4, [7, 7, 7, 7, 8, 3]], [2], [10], [9], [9]]
Output: [null, 7, 7, 7, 8]
Explanation:
```

**Constraints**

- 0 <= nums.length <= 104
- 1 <= k <= nums.length + 1
- -104 <= nums[i] <= 104
- -104 <= val <= 104
- At most 104 calls will be made to add.

---

## 题目（中文翻译）

你是大学招生办公室的一员，需要实时跟踪申请者的第 **k** 高分数，以便在新申请者提交成绩时动态确定面试和录取的分数线。  
请实现一个类，使其在给定整数 **k** 的情况下，维护一个成绩流（stream），并在每次加入新成绩后返回当前所有成绩中第 **k** 大的分数。更具体地说，需要在所有成绩的排序列表中找出第 **k** 大的元素。

实现 `KthLargest` 类：

```java
class KthLargest {
    public KthLargest(int k, int[] nums) { ... }
    public int add(int val) { ... }
}
```

- 构造函数 `KthLargest(int k, int[] nums)` 用 **k** 和初始成绩数组 `nums` 初始化对象。  
- 方法 `int add(int val)` 将新成绩 `val` 加入流中，并返回当前第 **k** 大的成绩。

**示例 1**  

**示例 2**  

**约束条件**  

- `0 <= nums.length <= 10^4`  
- `1 <= k <= nums.length + 1`  
- `-10^4 <= nums[i] <= 10^4`  
- `-10^4 <= val <= 10^4`  
- 最多会调用 `add` 方法 `10^4` 次  

**示例**

**示例 1：**  
```text
Input: ["KthLargest", "add", "add", "add", "add", "add"] 
       [[3, [4, 5, 8, 2]], [3], [5], [10], [9], [4]]
Output: [null, 4, 5, 5, 8, 8]
Explanation:
KthLargest kthLargest = new KthLargest(3, [4, 5, 8, 2]);
kthLargest.add(3); // 返回 4
kthLargest.add(5); // 返回 5
kthLargest.add(10); // 返回 5
kthLargest.add(9); // 返回 8
kthLargest.add(4); // 返回 8
```

**示例 2：**  
```text
Input: ["KthLargest", "add", "add", "add", "add"] 
       [[4, [7, 7, 7, 7, 8, 3]], [2], [10], [9], [9]]
Output: [null, 7, 7, 7, 8]
Explanation:
（此示例未提供额外解释）
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有出现过的分数全部保存到一个列表 `arr` 中，每次有新分数 `val` 来时：

1. 把 `val` 加到 `arr` 里。  
2. 把 `arr` 从大到小排序（`sorted(arr, reverse=True)`），这样第 `k` 大的分数就在下标 `k‑1` 处。  
3. 直接返回该下标的值。

> **类比**：把 `arr` 想象成一本“成绩册”，每次有新成绩要写进来，就把整本册子重新排个序，像老师每次都要把全班成绩从高到低重新排一次。  
> **为什么对**：只要把所有成绩都收集起来并排序，第 `k` 大的元素必然是排好序后的第 `k` 位，所以答案一定正确。

#### 代码（Python）

```python
class KthLargest:
    def __init__(self, k: int, nums: list[int]):
        """
        初始化：记录 k 的大小，保存已有成绩列表 nums
        """
        self.k = k
        self.arr = nums[:]               # 复制一份，防止外部修改

    def add(self, val: int) -> int:
        """
        添加新成绩 val 并返回当前第 k 大的成绩
        """
        self.arr.append(val)             # 把新成绩放进成绩册
        # 把成绩册从大到小排序，sorted 会返回一个新列表
        sorted_arr = sorted(self.arr, reverse=True)
        # 第 k 大的成绩在下标 k-1 处
        return sorted_arr[self.k - 1]
```

#### 复杂度  

- **时间复杂度**：`O(n log n)`（`n` 为当前成绩总数）  
  每次调用 `add` 都要对全部成绩排序，排序的代价是 `n log n`。  
  大白话：如果有 1000 条成绩，每次都要像把 1000 张卡片重新排队，花的时间会随卡片数的对数倍增长。

- **空间复杂度**：`O(n)`  
  需要保存所有出现过的成绩，随成绩数量线性增长。  

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**瓶颈**在于每次都要对全部数据重新排序。我们只关心第 `k` 大的元素，实际上只需要维护 **前 k 大的成绩**，其余的都不必排进去。

**核心技巧：最小堆（Min‑Heap）**  
- 堆是一种特殊的完全二叉树，最小堆的根节点（`heap[0]`）始终是堆中最小的元素。  
- Python 的 `heapq` 模块实现了最小堆。把 “前 k 大的成绩” 放进一个最小堆，堆顶恰好是这 k 条成绩中最小的，也就是第 `k` 大的成绩。

实现步骤：

1. **初始化**  
   - 把 `nums` 中的每个元素依次调用 `add`（或直接构造堆），让堆的大小不超过 `k`。  
   - 如果堆的元素超过 `k`，弹出堆顶（最小的），保持堆里只保留最大的 `k` 条成绩。

2. **添加新成绩 `val`**  
   - 将 `val` 推入堆 `heapq.heappush`。  
   - 若此时堆的大小超过 `k`，再弹出一次堆顶 `heapq.heappop`。  
   - 此时堆顶就是第 `k` 大的成绩，直接返回。

> **类比**：想象有一个只能装 `k` 本成绩册的抽屉，每次有新成绩时把它放进去，如果抽屉满了就把最差的那本（最小的成绩）扔掉。抽屉里剩下的就是目前最好的 `k` 本成绩，而抽屉最前面的那本（最小的）正好是第 `k` 大的成绩。

#### 代码（Python）

```python
import heapq
from typing import List

class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        """
        初始化时：
        - 记录 k 的大小
        - 用最小堆维护当前的前 k 大成绩
        """
        self.k = k
        self.heap = []                     # 小根堆，堆顶是最小的

        # 把初始数组中的每个元素交给 add 统一处理
        for num in nums:
            self.add(num)                  # 这里会自动保证堆的大小不超过 k

    def add(self, val: int) -> int:
        """
        向流中加入新成绩 val，并返回当前第 k 大的成绩
        """
        heapq.heappush(self.heap, val)     # 把新成绩放进小根堆
        # 如果堆里元素超过 k，弹出最小的（也就是第 k+1 大的成绩）
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)       # 弹出后堆中仍然是前 k 大的成绩

        # 堆顶就是第 k 大的成绩
        return self.heap[0]
```

#### 复杂度  

- **时间复杂度**：`O(log k)`  
  `heapq.heappush` 与 `heapq.heappop` 的代价都是把元素在堆中上浮或下沉，最多需要走树高 `log k` 步。  
  大白话：如果 `k = 3`，每次只需要比较几次（约 `log2(3) ≈ 1.6`）就能决定是否保留新成绩，和把全部成绩重新排队相比快得多。

- **空间复杂度**：`O(k)`  
  堆里最多只保存 `k` 条成绩，和 `k` 成正比。  

---

## 心得

- **核心技巧**：**最小堆（大小为 k）** 用来动态维护第 k 大元素。  
- **适用的题型**：  
  1. “第 K 大/小元素”系列（如数组中第 K 大元素、滑动窗口第 K 大元素）。  
  2. “流式数据”需要实时查询 Top‑K（如日志系统的热点查询）。  
- **解题钥匙**：**只保留必要的 K 条信息，用堆把它们组织起来**。

---

## 反思

- **第一反应**：看到 “实时返回第 k 大”，立刻想到要维护一个有序结构，最直接想到排序。  
- **最容易踩的坑**：  
  - **堆的大小**：忘记在 `add` 后检查并弹出多余元素，会导致堆里超过 `k`，返回的就不是第 k 大。  
  - **初始化**：`nums` 可能为空，需要先把堆建好再处理后续 `add`。  
  - **负数与重复值**：堆本身可以处理，别把它们当作特殊情况。  
- **下次第一步**：先问自己“我只需要前 k 大吗？”如果答案是肯定的，立刻想到 **大小为 k 的最小堆**，而不是全局排序。