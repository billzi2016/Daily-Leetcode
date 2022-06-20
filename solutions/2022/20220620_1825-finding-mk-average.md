# #1825. **寻找 MK 平均值** / Finding MK Average

> 难度：困难 · 标签：Design、Queue、Heap (Priority Queue)、Data Stream、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/finding-mk-average/)

---

## 题目（英文原版）

**Description**

You are given two integers, m and k, and a stream of integers. You are tasked to implement a data structure that calculates the MKAverage for the stream.
The MKAverage can be calculated using these steps:
Implement the MKAverage class:

**Examples**

**Example 1:**

```
Input
["MKAverage", "addElement", "addElement", "calculateMKAverage", "addElement", "calculateMKAverage", "addElement", "addElement", "addElement", "calculateMKAverage"]
[[3, 1], [3], [1], [], [10], [], [5], [5], [5], []]
Output
[null, null, null, -1, null, 3, null, null, null, 5]

Explanation
MKAverage obj = new MKAverage(3, 1); 
obj.addElement(3);        // current elements are [3]
obj.addElement(1);        // current elements are [3,1]
obj.calculateMKAverage(); // return -1, because m = 3 and only 2 elements exist.
obj.addElement(10);       // current elements are [3,1,10]
obj.calculateMKAverage(); // The last 3 elements are [3,1,10].
                          // After removing smallest and largest 1 element the container will be [3].
                          // The average of [3] equals 3/1 = 3, return 3
obj.addElement(5);        // current elements are [3,1,10,5]
obj.addElement(5);        // current elements are [3,1,10,5,5]
obj.addElement(5);        // current elements are [3,1,10,5,5,5]
obj.calculateMKAverage(); // The last 3 elements are [5,5,5].
                          // After removing smallest and largest 1 element the container will be [5].
                          // The average of [5] equals 5/1 = 5, return 5
```

**Constraints**

- 3 <= m <= 105
- 1 < k*2 < m
- 1 <= num <= 105
- At most 105 calls will be made to addElement and calculateMKAverage.

---

## 题目（中文翻译）

给定两个整数 `m` 和 `k`，以及一个整数数据流（stream of integers）。请实现一个数据结构，用于计算该数据流的 **MKAverage**。

**MKAverage** 的计算步骤如下：

1. 只考虑最近加入的 `m` 个元素（如果不足 `m` 个，则返回 `-1`）。  
2. 在这 `m` 个元素中，剔除最小的 `k` 个元素和最大的 `k` 个元素。  
3. 对剩余的 `m - 2k` 个元素求平均值，向下取整（即整数除法）。

实现 `MKAverage` 类，需要提供以下接口：

- `MKAverage(int m, int k)`: 构造函数，初始化参数 `m` 与 `k`。  
- `void addElement(int num)`: 向数据流中加入一个新整数 `num`。  
- `int calculateMKAverage()`: 返回当前数据流的 **MKAverage**，如果数据流中元素少于 `m` 个，则返回 `-1`。

---

**示例**

```json
Input
["MKAverage", "addElement", "addElement", "calculateMKAverage", "addElement", "calculateMKAverage", "addElement", "addElement", "addElement", "calculateMKAverage"]
[[3, 1], [3], [1], [], [10], [], [5], [5], [5], []]
Output
[null, null, null, -1, null, 3, null, null, null, 5]
```

**解释**
```java
MKAverage obj = new MKAverage(3, 1); 
obj.addElement(3);        // 当前元素为 [3]
obj.addElement(1);        // 当前元素为 [3, 1]
obj.calculateMKAverage(); // 元素不足 3 个，返回 -1
obj.addElement(10);       // 当前元素为 [3, 1, 10]
obj.calculateMKAverage(); // 去掉最小的 1 和最大的 10，剩下 [3]，平均值为 3
obj.addElement(5);        // 当前元素为 [1, 10, 5]（只保留最近的 3 个）
obj.addElement(5);        // 当前元素为 [10, 5, 5]
obj.addElement(5);        // 当前元素为 [5, 5, 5]
obj.calculateMKAverage(); // 去掉最小的 5 和最大的 5，剩下 [5]，平均值为 5
```

---

**约束条件**

- `3 <= m <= 10^5`
- `1 < 2k < m`
- `1 <= num <= 10^5`
- 最多会调用 `addElement` 与 `calculateMKAverage` 共计 `10^5` 次。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把 **最近的 `m` 个数** 全部保存下来，  
每次要计算 `MKAverage` 时：

1. 把这 `m` 个数 **排序**（就像把一堆零散的卡片摆成从小到大的顺序）。  
2. 去掉最左边的 `k` 张卡片（最小的 `k` 个），再去掉最右边的 `k` 张卡片（最大的 `k` 个）。  
3. 把剩下的 `m‑2k` 张卡片的数值相加，再除以 `m‑2k`，得到答案。

> **数据结构**：  
> - 用一个普通的 **队列**（`collections.deque`）记录元素的出现顺序，方便在窗口大小超过 `m` 时把最早的元素弹出。  
> - 用一个 **列表**保存这 `m` 个数，计算时对它进行排序。  
> - 类比：**哈希表**像字典，`key` 是单词，`value` 是页码；这里的 **队列** 像排队的顾客，最先来的最先离开。

**为什么能得到正确答案**  
- 只要我们始终只看最近的 `m` 条数据，按题意去掉最小/最大的 `k` 条，剩下的就是要平均的那 `m‑2k` 条。  
- 排序后直接切片取中间部分，数学上等价于题目描述的“先删最小 `k`，再删最大 `k`”。

**时间/空间复杂度**（大白话）  
- **时间**：  
  - 每次 `addElement` 只往队列里加一个数，时间是 **O(1)**。  
  - 每次 `calculateMKAverage` 要把最多 `m`（最多 10⁵）个数 **排序**，排序的代价大约是 “`m` 乘以 `log m`”，记作 **O(m log m)**。  
  - 如果我们每次都要算一次，最坏情况下会是 `10⁵` 次查询 → **O(10⁵·m log m)**，这在实际运行中会超时。  
- **空间**：我们只保存最近的 `m` 条数据，最多需要 **O(m)** 的额外内存。

#### 代码（Python）

```python
from collections import deque
from typing import List

class MKAverage:
    def __init__(self, m: int, k: int):
        self.m, self.k = m, k
        self.q = deque()          # 用来记住元素的顺序，最左边的是最早进入的
        self.window: List[int] = []   # 保存最近的 m 个数

    def addElement(self, num: int) -> None:
        self.q.append(num)        # 新元素进入队列
        self.window.append(num)   # 同时放进窗口列表
        # 如果窗口已经超过 m，就把最早的元素踢掉
        if len(self.q) > self.m:
            old = self.q.popleft()
            self.window.pop(0)    # 把对应的数从列表中删掉（这里是 O(m)）

    def calculateMKAverage(self) -> int:
        if len(self.q) < self.m:          # 还不到 m 条数据，返回 -1
            return -1
        # 把窗口里的数排序，得到从小到大的序列
        sorted_win = sorted(self.window)   # O(m log m)
        # 切掉最小的 k 和最大的 k，剩下的就是要平均的那部分
        middle = sorted_win[self.k: self.m - self.k]
        # 计算平均值（向下取整）
        return sum(middle) // (self.m - 2 * self.k)
```

> **注意**：这里的 `self.window.pop(0)` 实际是 **O(m)**，所以整体复杂度会更差，但代码足够直观，适合作为“最笨的解法”示例。

#### 复杂度

- **时间复杂度**：  
  - `addElement`：O(1)（理论上），但实际实现中删除最左元素用了 `pop(0)`，是 O(m)。  
  - `calculateMKAverage`：O(m log m)（因为要排序）。  
  - 用大白话解释：如果 `m = 100000`，一次查询要比把一整本书的页码全部重新排一遍还慢。  
- **空间复杂度**：O(m)——只存最近的 `m` 条数据。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **两大瓶颈**：

1. **排序** 整个窗口 `m` 次，每次都要 `O(m log m)`。  
2. **删除最左元素** 时要在列表里找位置并删掉，最坏是 `O(m)`。

要把这两个瓶颈都压到 **对数级别**（`O(log m)`），我们需要一种 **可以快速**：

- **插入** 一个数  
- **删除** 任意（这里是最早加入的）数  
- **查询** 前 `k` 小 / 后 `k` 大 的 **累计和**  

这正好可以用 **树状数组（Fenwick Tree）**（也叫 **Binary Indexed Tree，BIT**）来实现。  
BIT 的核心思想可以类比为 **一本带有累计信息的书签**：

- 书签上记录了「前面有多少本书」以及「前面这些书的总页数」。
- 只要我们把书放进去或拿走，更新书签的几条线段（`O(log N)`）就能让累计信息保持正确。
- 以后想要「前 `k` 本书的总页数」时，只要顺着书签往上跳，就能在 `O(log N)` 内算出来。

**为什么 BIT 能解决本题**  

- 题目中 `num` 的取值范围是 `1 ≤ num ≤ 10⁵`，这给了我们一个**固定的坐标轴**（大小为 `MAX = 10⁵`），可以把每个数看成在这条坐标轴上的一个点。  
- 我们维护两棵 BIT：  
  1. **cnt BIT**：记录每个数出现的次数（相当于「这本书有几章」）。  
  2. **sum BIT**：记录数值的累计和（相当于「这几章的总页数」）。  
- 这样我们可以在 **`O(log MAX)`** 内得到：  
  - 前 `k` 小的数的 **累计和**（通过二分查找 BIT 找到第 `k` 小所在的数值，再用 `sum BIT` 求和）。  
  - 前 `k` 大的数的 **累计和**（把「大」转化为「总数 - 前 (m‑k) 小」），同样 `O(log MAX)`。  
- 只要我们知道 **窗口总和** `total_sum`，再减去「最小 `k` 的和」和「最大 `k` 的和」，就得到 **中间部分的和**。  
- 最后 `MKAverage = middle_sum // (m - 2k)`。

**步骤概览**  

1. 用 `deque` 保存**出现顺序**，当窗口长度超过 `m` 时弹出最左边的数 `old`。  
2. 对 `old`：在两棵 BIT 中 **减 1 次出现次数**，并把它的值从 `sum BIT` 中减去，同时把 `total_sum` 减掉 `old`。  
3. 对新加入的 `num`：在两棵 BIT 中 **加 1 次出现次数**，把它的值加到 `sum BIT`，`total_sum` 加上 `num`。  
4. `calculateMKAverage`：  
   - 若窗口未满 `m`，返回 `-1`。  
   - 用 `cnt BIT` 找到第 `k` 小的数值 `left_val`，并用 `sum BIT` 计算 **小于等于 `left_val` 的累计和** → `left_sum`。  
   - 同理，找到第 `k` 大的数值对应的 **右侧阈值** `right_val`（其实是第 `m‑k` 小的数），计算 **大于等于 `right_val` 的累计和** → `right_sum`。  
   - `middle_sum = total_sum - left_sum - right_sum`。  
   - 返回 `middle_sum // (m - 2*k)`。

**关键点解释**  

- **二分查找 BIT 找第 k 小**：  
  BIT 本身只能快速求「前缀和」，但我们可以在 `log MAX` 的时间里「在树状结构上走」，相当于在「累计计数」的坐标轴上做二分，定位到第 `k` 个出现的数。  
- **删除最左元素**：因为我们有 `deque` 记录顺序，弹出时只需要在 BIT 中把对应的计数减一，**不需要遍历整个窗口**。  

#### 代码（Python）

```python
from collections import deque
from typing import List

MAX_VAL = 10 ** 5 + 2          # BIT 的大小，稍微大一点防止越界

class BIT:
    """树状数组（Fenwick Tree），支持单点更新 + 前缀和查询"""
    def __init__(self, size: int):
        self.n = size
        self.tree = [0] * (self.n + 1)

    def add(self, idx: int, delta: int) -> None:
        """在位置 idx（1-indexed）上加 delta"""
        while idx <= self.n:
            self.tree[idx] += delta
            idx += idx & -idx      # lowbit，向上跳到父节点

    def prefix_sum(self, idx: int) -> int:
        """求前缀和 sum[1..idx]"""
        s = 0
        while idx > 0:
            s += self.tree[idx]
            idx -= idx & -idx      # lowbit，向下跳到子节点
        return s

    def kth(self, k: int) -> int:
        """
        在累计计数中找到第 k 小的数值（返回对应的 idx），
        前提是整体计数 >= k。
        """
        idx = 0
        bit_mask = 1 << (self.n.bit_length() - 1)   # 最大的 2^p <= n
        while bit_mask:
            nxt = idx + bit_mask
            if nxt <= self.n and self.tree[nxt] < k:
                k -= self.tree[nxt]
                idx = nxt
            bit_mask >>= 1
        return idx + 1   # 因为 idx 仍然是「小于目标」的最大位置

class MKAverage:
    def __init__(self, m: int, k: int):
        self.m, self.k = m, k
        self.window = deque()          # 记录出现顺序
        self.cnt = BIT(MAX_VAL)        # 统计每个数出现的次数
        self.sum = BIT(MAX_VAL)        # 统计每个数的累计和
        self.total = 0                 # 窗口所有数的总和

    def _add(self, num: int) -> None:
        """向结构里插入一个数（内部使用）"""
        self.cnt.add(num, 1)           # 次数 +1
        self.sum.add(num, num)         # 累计和 +num
        self.total += num

    def _remove(self, num: int) -> None:
        """从结构里删除一个数（内部使用）"""
        self.cnt.add(num, -1)          # 次数 -1
        self.sum.add(num, -num)        # 累计和 -num
        self.total -= num

    def addElement(self, num: int) -> None:
        self.window.append(num)
        self._add(num)

        if len(self.window) > self.m:          # 窗口已满，需要踢掉最老的数
            old = self.window.popleft()
            self._remove(old)

    def calculateMKAverage(self) -> int:
        if len(self.window) < self.m:          # 还没有满 m 条
            return -1

        # 1️⃣ 取最小的 k 个数的累计和
        left_val = self.cnt.kth(self.k)        # 第 k 小的「数值」在坐标轴上的位置
        left_sum = self.sum.prefix_sum(left_val)

        # 2️⃣ 取最大的 k 个数的累计和
        #   等价于：在整体中去掉前 (m - k) 小的数，剩下的就是最大的 k 个
        right_k = self.m - self.k               # 第 (m-k) 小的数的位置
        right_val = self.cnt.kth(right_k)
        # 右侧的累计和 = 总和 - 前 (right_val-1) 的累计和
        right_sum = self.total - self.sum.prefix_sum(right_val - 1)

        # 3️⃣ 中间部分的和
        middle_sum = self.total - left_sum - right_sum

        return middle_sum // (self.m - 2 * self.k)
```

> **代码说明（关键行中文注释）**  
> - `BIT.add` / `BIT.prefix_sum`：在树上“顺着 low‑bit”向上/向下走，完成 **O(log N)** 的更新或查询。  
> - `BIT.kth`：在累计计数的“楼梯”上跳来跳去，找到第 `k` 小的数，仍是 **O(log N)**。  
> - `_add` / `_remove`：把新数或旧数同步写进两棵 BIT，并维护窗口的总和 `self.total`。  
> - `calculateMKAverage`：先找最小 `k` 的阈值，再找最大 `k` 的阈值，用 **前缀和** 把这两块的总和算出来，最后用总和减去这两块，即得到中间部分的和。

#### 复杂度

- **时间复杂度**  
  - `addElement`：每次插入（或删除）都要在两棵 BIT 上做一次 `add`，每次 `O(log MAX_VAL)`，即 **O(log 10⁵)**，约等于 **O(log m)**。  
  - `calculateMKAverage`：两次 `kth` 查找 + 两次前缀和查询，同样都是 **O(log MAX_VAL)**。  
  - 用大白话说：不管窗口有多大（最多 10⁵），每一次操作只需要「爬树」几层（大约 17 层），几乎是瞬间完成的。  
- **空间复杂度**  
  - 两棵 BIT 各占 `MAX_VAL` 的整数数组，约 **2 × 10⁵** 的空间 → **O(MAX_VAL)**，常数很小。  
  - 另外还有 `deque` 保存最近的 `m` 条数据 → **O(m)**。  
  - 综合来看是 **O(m + MAX_VAL)**，在本题的约束下完全可以接受。

---

## 心得

- **核心技巧**：使用 **树状数组（Fenwick Tree）** 维护**出现次数**和**数值前缀和**，配合 **滑动窗口 + 队列** 实现 **O(log N)** 的插入、删除和前 `k` 小/大累计求和。  
- **适用的题型**（类似思路）  
  1. **滑动窗口求中位数**（LeetCode 480 Sliding Window Median）  
  2. **数据流中的第 K 大元素**（LeetCode 703 Kth Largest Element in a Stream）  
  3. **区间动态统计**（比如「区间内第 K 小」）  
- **一句话总结解题钥匙**：**把「取最小 k、最大 k」的操作转化为「前缀计数/前缀和」的查询，用 BIT 把它们压到对数时间**。

---

## 反思

- **第一反应**：看到 “最近的 m 条数据，去掉最小 k、最大 k 再求平均”，立刻想到 “直接排序”。这就是最笨的暴力思路。  
- **最容易踩的坑**  
  - **删除最左元素**时忘记在统计结构里同步减掉，导致计数不一致。  
  - **二分查找 BIT**时下标容易越界（BIT 是 1‑indexed），需要把 `kth` 返回的结果加 1。  
  - **边界情况**：窗口未满 `m` 时直接返回 `-1`，否则会在 `kth` 中找不到足够的元素报错。  
- **下次遇到同类题**：  
  1. 判断是否可以把「取前/后若干个」转化为「前缀计数」或「前缀和」的查询。  
  2. 若数值范围有限（如 ≤ 10⁵），立刻考虑 **树状数组 / 线段树** 来维护出现次数和累计和。  
  3. 用 **队列** 记录顺序，保证「滑动窗口」的删除操作可以 O(log N) 完成。