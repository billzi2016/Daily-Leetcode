# #406. 按身高重建队列 / Queue Reconstruction by Height

> 难度：中等 · 标签：Array、Binary Indexed Tree、Segment Tree、Sorting · [LeetCode 链接](https://leetcode.com/problems/queue-reconstruction-by-height/)

---

## 题目（英文原版）

**Description**

You are given an array of people, people, which are the attributes of some people in a queue (not necessarily in order). Each people[i] = [hi, ki] represents the ith person of height hi with exactly ki other people in front who have a height greater than or equal to hi.
Reconstruct and return the queue that is represented by the input array people. The returned queue should be formatted as an array queue, where queue[j] = [hj, kj] is the attributes of the jth person in the queue (queue[0] is the person at the front of the queue).

**Examples**

**Example 1:**

```
Input: people = [[7,0],[4,4],[7,1],[5,0],[6,1],[5,2]]
Output: [[5,0],[7,0],[5,2],[6,1],[4,4],[7,1]]
Explanation:
Person 0 has height 5 with no other people taller or the same height in front.
Person 1 has height 7 with no other people taller or the same height in front.
Person 2 has height 5 with two persons taller or the same height in front, which is person 0 and 1.
Person 3 has height 6 with one person taller or the same height in front, which is person 1.
Person 4 has height 4 with four people taller or the same height in front, which are people 0, 1, 2, and 3.
Person 5 has height 7 with one person taller or the same height in front, which is person 1.
Hence [[5,0],[7,0],[5,2],[6,1],[4,4],[7,1]] is the reconstructed queue.
```

**Example 2:**

```
Input: people = [[6,0],[5,0],[4,0],[3,2],[2,2],[1,4]]
Output: [[4,0],[5,0],[2,2],[3,2],[1,4],[6,0]]
```

**Constraints**

- 1 <= people.length <= 2000
- 0 <= hi <= 106
- 0 <= ki < people.length
- It is guaranteed that the queue can be reconstructed.

---

## 题目（中文翻译）

**描述**  
给定一个二维数组 `people`，其中 `people[i] = [h_i, k_i]` 表示第 *i* 个人的身高为 `h_i`，且在其前面恰好有 `k_i` 个人的身高 **大于等于** `h_i`。  
请根据 `people` 重建并返回该队列。返回的队列应当以二维数组 `queue` 的形式给出，其中 `queue[j] = [h_j, k_j]` 表示排在第 *j* 位（`queue[0]` 为队首）的人的属性。

**示例 1**  
```text
Input: people = [[7,0],[4,4],[7,1],[5,0],[6,1],[5,2]]
Output: [[5,0],[7,0],[5,2],[6,1],[4,4],[7,1]]
Explanation:
- Person 0 的身高为 5，前面没有身高大于或等于 5 的人。
- Person 1 的身高为 7，前面没有身高大于或等于 7 的人。
- Person 2 的身高为 5，前面有两个人的身高大于或等于 5，分别是 Person 0 和 Person 1。
- Person 3 的身高为 6，前面有一个人身高大于或等于 6，即 Person 1。
- Person 4 的身高为 4，前面有四个人的身高大于或等于 4，分别是 Person 0、1、2、3。
- Person 5 的身高为 7，前面有一个人身高大于或等于 7，即 Person 1。  
因此得到的重建队列为 `[[5,0],[7,0],[5,2],[6,1],[4,4],[7,1]]`。

**示例 2**  
```text
Input: people = [[6,0],[5,0],[4,0],[3,2],[2,2],[1,4]]
Output: [[4,0],[5,0],[2,2],[3,2],[1,4],[6,0]]
```

**约束条件**  
- `1 <= people.length <= 2000`  
- `0 <= h_i <= 10^6`  
- `0 <= k_i < people.length`  
- 题目保证一定可以重建出唯一的队列。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

把题目想成 “把每个人按要求放进队列”。  
最直接的想法是：  

1. **先把人按身高从低到高排好**（因为最矮的人的约束最容易满足）。  
2. 维护一个长度为 `n`（`n = len(people)`）的空位数组 `queue`，初始全是 `None`，相当于“一排空座位”。  
3. 依次取出排好序的每个人 `[h, k]`，从左往右数空位，找到第 **k+1** 个空位（因为 `k` 表示前面要有 `k` 个 **不低于** 他高度的人），把他坐进去。  

> **类比**：想象你在排队买票，先把最矮的孩子安排座位，他只在乎前面有多少个不低于他身高的人。等他坐好后，再让稍高一点的孩子找第 `k`+1 个空位坐…… 这样一步步填满所有座位。  

**为什么正确**  
- 当我们只看已经坐好的人时，所有已坐的人 **身高都不低于** 正在放置的人的身高（因为我们是从矮到高放的）。  
- 因此，在剩余的空位中，第 `k`+1 个空位恰好满足“前面有 `k` 个人不低于他”。  

**时间/空间分析**  
- 对每个人都要遍历一次队列去找第 `k`+1 个空位，最坏情况要遍历 `n` 次。于是总时间是 `n` 个人 × `n` 次遍历 = **O(n²)**。  
- 只用了一个长度为 `n` 的数组来记录队列，空间是 **O(n)**。  

> **大白话**：`O(n²)` 就像你在教室里找座位，每找一次要从头数到第 `k` 位，人数多了，数的次数会呈平方增长，几百人算下来就会明显慢。  

#### 代码（Python）  

```python
from typing import List

def reconstructQueue_bruteforce(people: List[List[int]]) -> List[List[int]]:
    """
    暴力实现：从矮到高依次放置，每次线性扫描找第 k+1 个空位
    """
    n = len(people)
    # 1️⃣ 按身高升序，如果身高相同则 k 也升序（任意顺序都行，只要先处理矮的）
    people.sort(key=lambda x: (x[0], x[1]))

    # 2️⃣ 用 None 表示空位
    queue = [None] * n

    for h, k in people:
        # 在 queue 中找第 k+1 个空位
        empty_cnt = 0          # 已经遍历到的空位数
        for i in range(n):
            if queue[i] is None:          # 当前位置空
                if empty_cnt == k:        # 正好是第 k+1 个空位
                    queue[i] = [h, k]     # 坐下
                    break
                empty_cnt += 1
    return queue
```

#### 复杂度  

- **时间复杂度**：`O(n²)` — 每个人要线性扫描一次队列，最坏会遍历 `n` 次。  
- **空间复杂度**：`O(n)` — 只用了一个长度为 `n` 的数组来存放结果。  

---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **每次都要线性扫描找空位**。  
如果我们能在 **对数时间** 内找到第 `k`+1 个空位，就能把整体复杂度降到 `O(n log n)`。  

这正是 **树状数组（Binary Indexed Tree, BIT）** 或 **线段树** 擅长的：  
- 它们可以维护一个数组 `bit[i]`，记录前缀 “空位数量”。  
- 支持两类操作  
  1. **更新**：把某个位置的空位标记为已占用（空位数减 1）。  
  2. **查询**：在 `O(log n)` 时间内找到第 `k` 个空位对应的真实下标（**二分查找** + 前缀和）。  

**步骤**  

1. **先把人按身高从高到低排**，如果身高相同则 `k` 小的在前。  
   - 这样，当我们把一个人插入队列时，已经插入的所有人 **都不比他矮**，不会影响后面人的 `k` 值。  
2. 初始化一个长度为 `n` 的 BIT，所有位置的值都设为 `1`（表示“空位”）。  
3. 按顺序遍历排序后的人 `[h, k]`：  
   - 在 BIT 中查找第 `k+1` 个空位的真实下标 `pos`（因为 `k` 表示前面有 `k` 个不低于他的已坐人）。  
   - 把 `[h, k]` 放到结果数组的 `pos` 位置。  
   - 在 BIT 中把 `pos` 位置的值更新为 `0`（占用），即 `add(pos, -1)`。  

> **类比**：想象有一排座位，每个座位上贴有一张 “还有几个人还能坐在我左边？” 的小卡片。  
> 我们用 BIT 把所有卡片的数字加在一起，快速算出第几张卡片对应的座位。每坐下一个人，就把那张卡片的数字减 1，表示这位已经被占用了。  

**为什么正确**  
- 先按 **高→低** 排序，保证已放入的人的身高 **≥** 正在放的人。  
- 对于当前人来说，`k` 正好等于 “已经占用的、且身高 ≥ 当前人的” 人数。  
- BIT 给出的第 `k+1` 个空位恰好是满足 “左边已有 `k` 个已占位（且身高不低）” 的位置。  

#### 代码（Python）  

```python
from typing import List

class BIT:
    """树状数组（Binary Indexed Tree），支持前缀和与单点增减"""
    def __init__(self, n: int):
        self.n = n
        self.tree = [0] * (n + 1)   # 1-indexed

    def add(self, idx: int, delta: int):
        """把 idx 位置的值加 delta（idx 采用 0-index，内部转成 1-index）"""
        i = idx + 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i

    def prefix_sum(self, idx: int) -> int:
        """返回 [0, idx] 的前缀和（idx 采用 0-index）"""
        i = idx + 1
        s = 0
        while i:
            s += self.tree[i]
            i -= i & -i
        return s

    def find_kth(self, k: int) -> int:
        """
        在当前数组中（每个位置要么 1 表示空位，要么 0 表示已占），
        找到第 k 个 1 的下标（k 从 1 开始计数）。
        这里使用二分 + 前缀和的思想，时间 O(log n)。
        """
        left, right = 0, self.n - 1
        while left < right:
            mid = (left + right) // 2
            if self.prefix_sum(mid) >= k:   # 前缀和已经 >= k，说明第 k 个 1 在左半边
                right = mid
            else:
                left = mid + 1
        return left

def reconstructQueue_optimal(people: List[List[int]]) -> List[List[int]]:
    """
    最优实现：利用树状数组在 O(log n) 内定位第 k+1 个空位
    """
    n = len(people)
    # 1️⃣ 按身高降序、k 升序排序
    people.sort(key=lambda x: (-x[0], x[1]))

    # 2️⃣ 初始化 BIT，所有位置都是空位（值 1）
    bit = BIT(n)
    for i in range(n):
        bit.add(i, 1)   # 把每个位置设为 1

    res = [None] * n   # 最终答案

    # 3️⃣ 依次把每个人放进队列
    for h, k in people:
        # 第 k+1 个空位的下标（因为 k 表示前面已经有 k 个不低于他的已坐人）
        pos = bit.find_kth(k + 1)
        res[pos] = [h, k]          # 坐下
        bit.add(pos, -1)           # 把该位置标记为已占用
    return res
```

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 排序 `O(n log n)`。  
  - 对每个人一次 `find_kth`（二分 + 前缀和）+ `add`，均为 `O(log n)`，共 `n` 次。  
  - 与暴力的 `O(n²)` 相比，数量级下降明显，`n=2000` 时几乎瞬间完成。  

- **空间复杂度**：`O(n)`  
  - 结果数组、BIT 树各占 `n` 大小。  

---  

## 心得  

- **核心技巧**：先按身高从高到低排序，然后利用 **树状数组（或线段树）** 快速定位第 `k`+1 个空位。  
- **适用的题型**  
  1. “第 k 小/第 k 大” 需要在动态集合中快速定位（如 “寻找第 k 个空位”）。  
  2. 需要在 **插入后保持顺序** 的问题，例如 “根据逆序对重建数组”。  
  3. 其他基于 “空位/可用位置” 的排队或排座位类题目。  
- **一句话总结**：把最高的先坐，用 BIT 把“空位”当成可查询的资源，插入即删，整个过程只要 `log` 级别的操作。  

---  

## 反思  

- **第一反应**：先想到把人从矮到高依次放，直接线性扫描找空位——这就是暴力思路。  
- **最容易踩的坑**  
  - **排序顺序**：如果把矮的先放，后面的高的人会影响已经满足的 `k`，导致错误。正确的顺序是 **高→低**（或使用 BIT 的矮→高 但要定位空位），要记住。  
  - **`k` 的解释**：`k` 表示前面 **不低于** 当前身高的人数，而不是严格大于，排序时要把同高的 `k` 小的先放。  
  - **BIT 的 `find_kth` 实现**：边界要处理好（`k` 从 1 开始），否则会找不到位置或越界。  
- **下次类似题的第一步**：先确定 **一个固定的全局顺序**（通常是“从大到小”或“从小到大”），然后思考如何在该顺序下用 **可快速查询/更新的数据结构**（BIT、线段树、平衡树）完成“第 k 个空位”或“第 k 大元素”的定位。