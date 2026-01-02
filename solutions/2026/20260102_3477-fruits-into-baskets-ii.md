# #3477. 水果装入篮子 II / Fruits Into Baskets II

> 难度：简单 · 标签：Array、Binary Search、Segment Tree、Simulation、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/fruits-into-baskets-ii/)

---

## 题目（英文原版）

**Description**

You are given two arrays of integers, fruits and baskets, each of length n, where fruits[i] represents the quantity of the ith type of fruit, and baskets[j] represents the capacity of the jth basket.
From left to right, place the fruits according to these rules:
Return the number of fruit types that remain unplaced after all possible allocations are made.

**Examples**

**Example 1:**

```
Input: fruits = [4,2,5], baskets = [3,5,4]
Output: 1
Explanation:
Since one fruit type remains unplaced, we return 1.
```

**Example 2:**

```
Input: fruits = [3,6,1], baskets = [6,4,7]
Output: 0
Explanation:
Since all fruits are successfully placed, we return 0.
```

**Constraints**

- n == fruits.length == baskets.length
- 1 <= n <= 100
- 1 <= fruits[i], baskets[i] <= 1000

---

## 题目（中文翻译）

你得到两个长度均为 n 的整数数组 `fruits` 和 `baskets`，其中 `fruits[i]` 表示第 i 类水果的数量，`baskets[j]` 表示第 j 个篮子的容量。  
从左到右依次放置水果，遵循题目给出的规则（规则在原题中已描述）。  
在完成所有可能的分配后，返回仍未被放置的水果种类数量。

**示例 1**  
输入: `fruits = [4,2,5]`, `baskets = [3,5,4]`  
输出: `1`  
解释:  
由于还有一种水果未能放入篮子，返回 1。

**示例 2**  
输入: `fruits = [3,6,1]`, `baskets = [6,4,7]`  
输出: `0`  
解释:  
所有水果均成功放入篮子，返回 0。

**约束条件**  
- `n == fruits.length == baskets.length`  
- `1 <= n <= 100`  
- `1 <= fruits[i], baskets[i] <= 1000`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

我们把 **水果种类** 看成从左到右排好的小盒子，**篮子** 也是从左到右排好的容器。  
规则是：

1. 先处理第 0 种水果，尽可能把它装进第 0 个篮子、再装进第 1 个篮子 …，一直往右装，直到水果全部装完或所有篮子都已经没有空位。  
2. 然后处理第 1 种水果，仍然只能往右（从第 1 个篮子开始）找还能装的篮子，依次填充。  
3. … 依次处理所有水果种类。  

如果某一种水果在走到最右边的篮子后仍有剩余，说明**这类水果根本放不进去**，我们要把它计数。  

> **哈希表类比**：如果你把每个篮子的剩余容量记在 `basket_remain[i]` 里，这相当于在查字典：键是篮子编号，值是还能放多少。  

暴力模拟的核心就是把每个水果种类的数量 `fruits[i]` 按顺序“倒进”后面的篮子里，边倒边把对应篮子的剩余容量减掉。

**为什么一定能得到正确答案？**  
因为我们严格遵守了题目给出的“从左到右、只能往后找篮子”这条规则，且每一次都把能放的尽量放进去——这就是题目要求的“尽可能多地分配”。所以最终剩下的水果种类数必然是唯一的。

#### 代码（Python）

```python
def countUnplacedFruits(fruits, baskets):
    """
    暴力模拟
    :param fruits: List[int]  第 i 种水果的数量
    :param baskets: List[int] 第 j 个篮子的容量
    :return: int 未能全部放入的水果种类数
    """
    n = len(fruits)
    # 用一个数组记录每个篮子还剩多少空间
    remain = baskets[:]          # 复制一份，防止修改原始输入
    unplaced = 0                 # 计数器

    # 按顺序处理每一种水果
    for i in range(n):
        need = fruits[i]         # 该种水果还有多少没有放进篮子

        # 从当前对应的篮子 i 开始，向右寻找还能装的篮子
        for j in range(i, n):
            if need == 0:        # 已经全部装完，直接退出内层循环
                break
            # 能装进去的量是剩余空间和需要量的最小值
            take = min(need, remain[j])
            remain[j] -= take    # 更新篮子的剩余空间
            need -= take         # 更新该种水果还需要装的量

        # 循环结束后，如果还有剩余，说明这类水果根本装不进去
        if need > 0:
            unplaced += 1

    return unplaced
```

> 关键行解释  
> - `remain = baskets[:]`：把篮子的容量复制到 `remain`，后面会不断减去已经放进去的水果。  
> - `take = min(need, remain[j])`：每次只能放进篮子还能容纳的量，或者把水果全部放完，两者取小的。  

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 外层遍历 `n` 种水果，内层最坏情况下要遍历从 `i` 到 `n-1` 的所有篮子，形成一个等差数列求和，约等于 `n·(n+1)/2`，即二次方级别。  
  - 用大白话说，就是如果 `n = 100`，最多要做 5 000 次“装水果”的操作，仍然可以接受。  

- **空间复杂度**：`O(1)`（不计输入数组）  
  - 只用了一个长度为 `n` 的 `remain` 数组来记录篮子剩余容量，大小与输入相同，属于原地修改的常数级额外空间。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在 **每次都要线性扫描右边的所有篮子**。  
如果我们能 **快速定位** 第一个仍有剩余空间的篮子，就能把扫描次数从 `O(n)` 降到 `O(log n)`。  

这正是**线段树（Segment Tree）**或**树状数组（Fenwick Tree）**擅长的事情——它们可以在对数组做“区间最大值”或“区间和”查询时，像二分一样在 `log n` 步内找到满足条件的下标。

**核心想法**  

1. 把每个篮子的剩余容量视为数组 `remain[]`。  
2. 构建一棵线段树，树节点保存**区间的最大剩余容量**。  
   - 若某个区间的最大值为 `0`，说明这段篮子已经全部装满，后面再查也没有意义。  
3. 对于第 `i` 种水果：  
   - 先用线段树在区间 `[i, n‑1]` 中查找**最左侧**仍有剩余空间的篮子（即最大值 > 0 的最小下标）。  
   - 把水果尽可能装进去：`take = min(need, remain[pos])`。  
   - 更新 `remain[pos]` 并在树上 **点更新**（把该位置的最大值改成新的剩余量）。  
   - 如果还有剩余，继续在 `[pos+1, n‑1]` 区间再次查找。  
   - 当找不到（返回 `-1`）且仍有 `need > 0` 时，这种水果算未能全部放进。  

这样，每一次**寻找**都是 `O(log n)`，每一次**更新**也是 `O(log n)`，而一次水果可能需要遍历的篮子数最多等于它实际占用的篮子数（每个篮子最多被更新一次），整体时间复杂度为 `O(n log n)`。

> **单调栈/前缀和类比**：如果把剩余容量看成一条山脉，线段树帮我们快速找到“第一个还能爬上去的山坡”。  

#### 代码（Python）

```python
class SegmentTree:
    """线段树：维护区间最大值，并支持寻找最左侧大于 0 的位置"""
    def __init__(self, data):
        self.n = len(data)
        # 树的大小一般取 4 * n 够用
        self.tree = [0] * (4 * self.n)
        self._build(1, 0, self.n - 1, data)

    def _build(self, node, l, r, data):
        if l == r:
            self.tree[node] = data[l]
            return
        mid = (l + r) // 2
        self._build(node * 2, l, mid, data)
        self._build(node * 2 + 1, mid + 1, r, data)
        self.tree[node] = max(self.tree[node * 2], self.tree[node * 2 + 1])

    def update(self, idx, value):
        """把下标 idx 的值改成 value（value 为新的剩余容量）"""
        self._update(1, 0, self.n - 1, idx, value)

    def _update(self, node, l, r, idx, value):
        if l == r:
            self.tree[node] = value
            return
        mid = (l + r) // 2
        if idx <= mid:
            self._update(node * 2, l, mid, idx, value)
        else:
            self._update(node * 2 + 1, mid + 1, r, idx, value)
        self.tree[node] = max(self.tree[node * 2], self.tree[node * 2 + 1])

    def query_first_positive(self, ql, qr):
        """在区间 [ql, qr] 中返回最左侧剩余容量 > 0 的下标，若不存在返回 -1"""
        return self._query(1, 0, self.n - 1, ql, qr)

    def _query(self, node, l, r, ql, qr):
        if r < ql or l > qr or self.tree[node] == 0:
            return -1                     # 这段区间没有正数
        if l == r:                       # 叶子结点且 >0
            return l
        mid = (l + r) // 2
        # 先查左子树，保证返回最左侧的下标
        left_res = self._query(node * 2, l, mid, ql, qr)
        if left_res != -1:
            return left_res
        return self._query(node * 2 + 1, mid + 1, r, ql, qr)


def countUnplacedFruits_opt(fruits, baskets):
    """
    使用线段树的 O(n log n) 解法
    """
    n = len(fruits)
    remain = baskets[:]                # 当前剩余容量
    seg = SegmentTree(remain)          # 构建线段树

    unplaced = 0

    for i in range(n):
        need = fruits[i]               # 该种水果还需要多少

        # 在 [i, n-1] 区间不断寻找还能装的篮子
        pos = seg.query_first_positive(i, n - 1)
        while need > 0 and pos != -1:
            take = min(need, remain[pos])
            remain[pos] -= take
            seg.update(pos, remain[pos])   # 更新线段树对应节点
            need -= take

            if remain[pos] == 0:           # 该篮子已满，继续向右找
                pos = seg.query_first_positive(pos + 1, n - 1)
            else:                           # 本篮子还有余量，仍然是最左侧可用的
                # 这里不需要再次查询，直接继续使用同一个 pos
                pass

        if need > 0:                       # 走到最右仍有剩余
            unplaced += 1

    return unplaced
```

> 关键行解释  
> - `self.tree[node] = max(...)`：每个节点保存它负责的区间里**最大**的剩余容量，方便判断该区间是否还有空位。  
> - `query_first_positive`：利用“最大值为 0”可以直接剪枝，快速定位最左侧还能装的篮子。  
> - `while need > 0 and pos != -1`：只要还有水果且还能找到篮子，就继续装；找不到（`pos==-1`）说明后面已经全满。  

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 对每种水果，最多进行若干次 “查找第一个可用篮子” + “更新篮子剩余量”。  
  - 每一次查询或更新都是 `log n`，而一次水果最多会遍历它实际占用的篮子数，所有水果共计至多遍历 `n` 次（每个篮子只会被清空一次），于是总体是 `n·log n`。  
  - 与暴力解的 `O(n²)` 相比，**当 n 较大时**（比如 10⁵）会快很多。  

- **空间复杂度**：`O(n)`  
  - 线段树本身需要约 `4·n` 的额外存储，加上 `remain` 数组，总体是线性的。  

---

## 心得  

- **核心技巧**：**使用线段树快速定位区间内第一个仍有剩余容量的篮子**。  
- **适用的题型**  
  1. “在区间里找第一个满足条件的元素”，如 **“把石子装进盒子”**、**“把任务安排到机器”** 等。  
  2. “动态维护数组的最大/最小/和”，典型的 **区间查询 + 点更新** 场景。  
  3. “模拟过程需要频繁跳过已满/已空的区段”，如 **“电影院座位分配”**。  
- **一句话总结解题钥匙**：**“把‘还能装吗’抽象成区间最大值，用线段树二分定位”，从而把线性扫描压缩到对数级。**  

---

## 反思  

- **第一反应**：直接写双层循环模拟——对小数据能跑通，但没想到会有更高效的结构。  
- **最容易踩的坑**  
  1. **下标范围**：水果只能从对应的篮子 `i` 开始往右找，忘记限制左边界会得到错误答案。  
  2. **更新后忘记同步线段树**：只改了 `remain[pos]` 而没有 `seg.update`，导致后续查询仍然看到旧的容量。  
  3. **边界条件**：当所有篮子都已满时，`query_first_positive` 必须返回 `-1`，否则会陷入死循环。  
- **下次类似题的第一步**：**先把“是否还有空位”抽象成一个可查询的数据结构（最大值/和），再考虑用二分/线段树定位**，这样能在一开始就避免 O(n²) 的暴力遍历。