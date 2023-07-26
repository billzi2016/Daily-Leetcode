# #2336. 无限集合中的最小数字 / Smallest Number in Infinite Set

> 难度：中等 · 标签：Hash Table、Design、Heap (Priority Queue)、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/smallest-number-in-infinite-set/)

---

## 题目（英文原版）

**Description**

You have a set which contains all positive integers [1, 2, 3, 4, 5, ...].
Implement the SmallestInfiniteSet class:

**Examples**

**Example 1:**

```
Input
["SmallestInfiniteSet", "addBack", "popSmallest", "popSmallest", "popSmallest", "addBack", "popSmallest", "popSmallest", "popSmallest"]
[[], [2], [], [], [], [1], [], [], []]
Output
[null, null, 1, 2, 3, null, 1, 4, 5]

Explanation
SmallestInfiniteSet smallestInfiniteSet = new SmallestInfiniteSet();
smallestInfiniteSet.addBack(2);    // 2 is already in the set, so no change is made.
smallestInfiniteSet.popSmallest(); // return 1, since 1 is the smallest number, and remove it from the set.
smallestInfiniteSet.popSmallest(); // return 2, and remove it from the set.
smallestInfiniteSet.popSmallest(); // return 3, and remove it from the set.
smallestInfiniteSet.addBack(1);    // 1 is added back to the set.
smallestInfiniteSet.popSmallest(); // return 1, since 1 was added back to the set and
                                   // is the smallest number, and remove it from the set.
smallestInfiniteSet.popSmallest(); // return 4, and remove it from the set.
smallestInfiniteSet.popSmallest(); // return 5, and remove it from the set.
```

**Constraints**

- 1 <= num <= 1000
- At most 1000 calls will be made in total to popSmallest and addBack.

---

## 题目（中文翻译）

你有一个集合，初始时包含所有正整数 `[1, 2, 3, 4, 5, ...]`。  
请实现 `SmallestInfiniteSet` 类，使其支持以下操作：

- `popSmallest()`：返回集合中最小的整数，并将其从集合中移除。  
- `addBack(num)`：将整数 `num` 添加回集合中。如果 `num` 已经在集合中，则不做任何修改。

**示例 1：**

```text
Input
["SmallestInfiniteSet", "addBack", "popSmallest", "popSmallest", "popSmallest", "addBack", "popSmallest", "popSmallest", "popSmallest"]
[[], [2], [], [], [], [1], [], [], []]

Output
[null, null, 1, 2, 3, null, 1, 4, 5]
```

**解释**  
```java
SmallestInfiniteSet smallestInfiniteSet = new SmallestInfiniteSet();
smallestInfiniteSet.addBack(2);    // 2 已经在集合中，故不做任何改变。
smallestInfiniteSet.popSmallest(); // 返回 1，集合变为 [2,3,4,5,...]
smallestInfiniteSet.popSmallest(); // 返回 2，集合变为 [3,4,5,...]
smallestInfiniteSet.popSmallest(); // 返回 3，集合变为 [4,5,...]
smallestInfiniteSet.addBack(1);    // 将 1 加回集合，集合变为 [1,4,5,...]
smallestInfiniteSet.popSmallest(); // 返回 1，集合变为 [4,5,...]
smallestInfiniteSet.popSmallest(); // 返回 4，集合变为 [5,6,...]
smallestInfiniteSet.popSmallest(); // 返回 5，集合变为 [6,7,...]
```

**约束条件**

- `1 <= num <= 1000`
- `popSmallest` 与 `addBack` 的调用总次数不超过 `1000` 次。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把集合里 **目前存在哪些数字** 用一个容器记录下来，然后每次 `popSmallest` 时从头遍历找出最小的那个。  
这里可以把集合想象成一本 **词典**：

- **词典的页码** 就是正整数（1,2,3,…）。  
- **是否在集合里** 相当于“这页是否已经被撕掉”。  

如果我们用一个 **布尔数组**（或 Python 的 `set`）来记录每个页码是否仍在词典中，就可以随时判断某个数字是否可用。  

实现步骤：

1. 由于题目只会出现 `num ≤ 1000` 且最多 1000 次操作，我们可以把 **可能出现的最大数字** 设为一个稍大的上限（比如 2000），在数组里预先全部标记为 “在”。  
2. `popSmallest`：从 `1` 开始线性扫描，找到第一个标记为 “在” 的位置 `i`，把它标记为 “不在”，并返回 `i`。  
3. `addBack(num)`：如果 `num` 当前被标记为 “不在”，就把它改回 “在”。如果本来就在集合里（已经是 “在”），什么也不做。

> **为什么正确**  
> - 初始时所有正整数都在集合里，数组的每个位置都标记为 “在”。  
> - `popSmallest` 每次都返回当前最小的 “在” 位置，并把它改为 “不在”，相当于把最小的正整数从集合中删掉。  
> - `addBack` 只把已经被删掉的数重新标记为 “在”，不影响其它数字的状态。  

#### 代码（Python）

```python
class SmallestInfiniteSet:
    def __init__(self):
        # 这里把可能出现的最大数字设为 2000（足够大），全部标记为 True 表示“在集合里”
        self.MAX = 2000
        self.present = [True] * (self.MAX + 1)   # 下标 0 不使用，直接浪费一点空间

    def popSmallest(self) -> int:
        # 从 1 开始线性查找第一个仍在集合里的数字
        for i in range(1, self.MAX + 1):
            if self.present[i]:
                self.present[i] = False      # 把它弹出
                return i
        # 按题意这里不会到达，因为集合是无限的
        raise Exception("No element left")

    def addBack(self, num: int) -> None:
        # 只在被弹出后才需要恢复
        if 1 <= num <= self.MAX:
            self.present[num] = True
```

#### 复杂度  

- **时间复杂度**：  
  - `popSmallest` 最坏需要遍历整个数组，时间是 **O(N)**，这里的 `N` 可以理解为“当前已经弹出的最大数字”。  
  - `addBack` 只做一次下标访问，时间是 **O(1)**。  
  - 用大白话说，`O(N)` 就像你在一本厚厚的词典里从头翻到第 `N` 页，页数越大，找的时间越久。  

- **空间复杂度**：  
  - 使用了长度为 `MAX` 的布尔数组，**O(N)** 的额外空间（这里的 `N` ≈ 2000），相当于准备了一张记事本，记下每一页是否被撕掉。  

> 这套暴力解在 **题目数据量很小** 时可以跑通，但随着 `popSmallest` 被调用很多次，线性扫描会成为明显的瓶颈。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于每次 `popSmallest` 都要从头线性扫描**。我们需要一种 **随时能得到当前最小元素** 的数据结构，且插入、删除都要快。  

两种关键工具：

1. **指针 `cur`**：记录 **“下一个从未被弹出过的最小正整数”**。  
   - 初始时 `cur = 1`，表示 1 仍在集合里。  
   - 每次直接弹出 `cur` 后，`cur += 1`，因为未弹出的最小数一定是下一个整数。  
   - 这相当于把无限集合 **划分成两块**：  
     - 左边已经弹出（或者已经被 `addBack` 放回）的数字，用其他容器管理。  
     - 右边是从 `cur` 开始的连续自然数，永远保持有序，不需要额外存储。  

2. **最小堆（优先队列）**：专门保存 **“被弹出后又被 `addBack` 放回来的数字”**。  
   - 堆的特性是“**随时能在 O(log k) 时间取出最小元素**”，这里的 `k` 是堆中元素个数。  
   - 为了防止同一个数字被重复放回，我们再维护一个 **集合 `in_heap`**，记录堆里已经存在的数字。  

**弹出最小数 `popSmallest` 的过程**：

- 如果堆不为空且堆顶（最小的回退数字）小于 `cur`，说明有比 `cur` 更小的“已经回来的”数字，此时弹出堆顶。  
- 否则，弹出 `cur` 本身，并把 `cur` 向右移动一位（`cur += 1`），因为连续的自然数已经自动排好序了。  

**放回数字 `addBack(num)` 的过程**：

- 只有当 `num` **已经被弹出**（即 `num < cur`）且 **不在堆里** 时，才需要把它加入堆。  
- 把 `num` 推入堆 (`heapq.heappush`) 并在 `in_heap` 中登记。  

这样每次操作都只涉及 **堆的顶端** 或 **指针的移动**，不需要遍历整个集合，时间复杂度大幅下降。

> **类比**：  
> - 想象有一条 **无限长的流水线**，上面依次放着 1、2、3… 的商品。  
> - `cur` 代表 **流水线上当前未取走的最左边商品**。  
> - 当某个已经取走的商品被放回仓库时，我们把它放进 **小箱子（堆）**，箱子里总是保持最小的商品在最上面。  
> - 取商品时，先看箱子里有没有更小的，如果有就从箱子里拿；否则直接从流水线上取当前最左的商品。

#### 代码（Python）

```python
import heapq

class SmallestInfiniteSet:
    def __init__(self):
        # cur 指向「下一个从未弹出」的最小正整数，初始为 1
        self.cur = 1
        # min‑heap 保存被弹出后又 addBack 的数字
        self.heap = []                 # 实际存放的数值
        self.in_heap = set()           # 用 set 防止同一个数被重复放入堆

    def popSmallest(self) -> int:
        """
        返回集合中当前最小的正整数，并将其从集合中删除。
        """
        # 如果堆非空且堆顶小于 cur，说明有比 cur 更小的“回退”数字
        if self.heap and self.heap[0] < self.cur:
            smallest = heapq.heappop(self.heap)   # 弹出堆顶
            self.in_heap.remove(smallest)          # 同步移除记录
            return smallest
        else:
            # 否则直接返回 cur，并让 cur 向右移动一位
            smallest = self.cur
            self.cur += 1
            return smallest

    def addBack(self, num: int) -> None:
        """
        如果 num 已经被弹出且当前不在集合中，则把它放回集合。
        """
        # 只对已经弹出且未在堆中的数字进行添加
        if num < self.cur and num not in self.in_heap:
            heapq.heappush(self.heap, num)   # 加入最小堆
            self.in_heap.add(num)            # 记录在集合中，防止重复加入
```

#### 复杂度  

- **时间复杂度**：  
  - `popSmallest`：  
    - 堆非空且堆顶更小 → `heappop` 为 **O(log k)**（`k` 为堆中元素数）。  
    - 否则直接返回 `cur` 为 **O(1)**。  
  - `addBack`：如果需要加入堆，同样是 `heappush`，时间 **O(log k)**；否则是 **O(1)**。  
  - 用大白话讲，**log k** 就像在一棵层层递增的“抽屉”里找最小的东西，层数很少（最多约 10），所以几乎是瞬间完成。  

- **空间复杂度**：  
  - 只用了一个最小堆和一个集合来保存 **被 addBack 的数字**，最多不超过所有调用次数（≤ 1000），所以 **O(k)**，这里的 `k` ≤ 1000。  
  - 与暴力解的固定大数组相比，空间更“省”，只在需要时才占用。

> 与暴力解相比，**最优解把每次 `popSmallest` 从可能的 O(N) 降到 O(log k) 或 O(1)**，在大量操作时会快很多。

---

## 心得

- **核心技巧**：把「无限有序」的部分用指针 `cur` 表示，把「被弹出后又可能回来」的离散部分用 **最小堆 + 哈希集合** 管理。  
- **适用的题型**  
  1. **动态维护有序集合**（如 “实现一个支持 insert、delete、getMin 的数据结构”）。  
  2. **需要快速取最小/最大且元素会被重新加入**（如 “设计一个有序流的窗口”）。  
  3. **把无限序列拆分为“已知前缀 + 需要维护的碎片”** 的问题（比如 “无限流的第 K 小数”）。  
- **一句话总结**：**指针负责顺序递增，堆负责处理“乱序回归”，两者配合即可 O(log n) 完成最小值操作**。

---

## 反思

- **第一反应**：直接用数组或集合记录每个数字是否在，随后线性扫描找最小。  
- **最容易踩的坑**  
  - **无限集合的实现**：不能真的创建无限大的数组，需要用指针或懒加载的方式。  
  - **重复 `addBack`**：若不检查堆中是否已有该数字，会导致同一个数出现多次，进而 `popSmallest` 返回错误的结果。  
  - **边界条件**：当 `addBack` 的数大于等于 `cur` 时，实际上它已经在 “未弹出” 的连续区间里，不需要放进堆。  
- **下次类似题目第一步**：先思考 **“哪些元素是天然有序且可以用指针/计数表示”**，把剩余需要动态维护的离散元素交给 **堆/平衡树 + 哈希** 来管理。这样就能快速定位瓶颈并选出合适的数据结构。