# #307. 区间求和查询 - 可变 / Range Sum Query - Mutable

> 难度：中等 · 标签：Array、Design、Binary Indexed Tree、Segment Tree · [LeetCode 链接](https://leetcode.com/problems/range-sum-query-mutable/)

---

## 题目（英文原版）

**Description**

Given an integer array nums, handle multiple queries of the following types:
Implement the NumArray class:

**Examples**

**Example 1:**

```
Input
["NumArray", "sumRange", "update", "sumRange"]
[[[1, 3, 5]], [0, 2], [1, 2], [0, 2]]
Output
[null, 9, null, 8]

Explanation
NumArray numArray = new NumArray([1, 3, 5]);
numArray.sumRange(0, 2); // return 1 + 3 + 5 = 9
numArray.update(1, 2);   // nums = [1, 2, 5]
numArray.sumRange(0, 2); // return 1 + 2 + 5 = 8
```

**Constraints**

- 1 <= nums.length <= 3 * 104
- -100 <= nums[i] <= 100
- 0 <= index < nums.length
- -100 <= val <= 100
- 0 <= left <= right < nums.length
- At most 3 * 104 calls will be made to update and sumRange.

---

## 题目（中文翻译）

给定一个整数数组 `nums`，需要处理多次以下类型的查询：

- `sumRange(left, right)`: 返回下标区间 `[left, right]`（闭区间）内元素的和。
- `update(index, val)`: 将 `nums[index]` 的值更新为 `val`。

请实现 `NumArray` 类，使其能够高效支持上述两种操作。

**示例 1**

```text
Input
["NumArray", "sumRange", "update", "sumRange"]
[[[1, 3, 5]], [0, 2], [1, 2], [0, 2]]
Output
[null, 9, null, 8]
```

**解释**
```java
NumArray numArray = new NumArray([1, 3, 5]);
numArray.sumRange(0, 2); // 返回 1 + 3 + 5 = 9
numArray.update(1, 2);   // 此时 nums = [1, 2, 5]
numArray.sumRange(0, 2); // 返回 1 + 2 + 5 = 8
```

**约束条件**

- `1 <= nums.length <= 3 * 10^4`
- `-100 <= nums[i] <= 100`
- `0 <= index < nums.length`
- `-100 <= val <= 100`
- `0 <= left <= right < nums.length`
- 调用 `update` 与 `sumRange` 的总次数不超过 `3 * 10^4`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把数组原封不动地保存下来，  
- **`update`**：把 `nums[index]` 直接改成新值 `val`，这一步只涉及一次赋值，时间几乎可以忽略。  
- **`sumRange`**：从 `left` 循环到 `right`，把每个元素累加起来得到区间和。  

这就像在超市里把所有商品逐个称重再相加——虽然能得到正确答案，但如果要称很多次就会很慢。  

> **数据结构**：这里只用到了普通的 Python 列表 (`list`)。可以把列表想象成一本“账本”，每一页（下标）记录一个数值，查询时要把对应的页翻出来逐个相加。

**为什么正确**：我们每次都直接读取最新的数组元素并做加法，显然符合题目对「区间求和」的定义。

**时间/空间复杂度**（用大白话解释）  
- `update` 只改一个位置，时间几乎是 **常数级**（O(1)），意思是无论数组多大，这一步的耗时基本不变。  
- `sumRange` 要遍历 `right-left+1` 个元素，最坏情况下遍历整个数组，时间是 **线性级**（O(n)），也就是如果数组有 30 000 个元素，就要走 30 000 步。  
- 额外空间几乎不需要，只用了几个临时变量，算作 **常数级**（O(1)）。

#### 代码（Python）

```python
class NumArray:
    def __init__(self, nums):
        """
        :type nums: List[int]
        """
        # 直接保存一份原始数组
        self.nums = nums

    def update(self, index, val):
        """
        将 nums[index] 的值改为 val
        :type index: int
        :type val: int
        :rtype: None
        """
        self.nums[index] = val          # 直接赋值，时间几乎为 O(1)

    def sumRange(self, left, right):
        """
        返回闭区间 [left, right] 的元素和
        :type left: int
        :type right: int
        :rtype: int
        """
        total = 0
        # 从 left 循环到 right，逐个累加
        for i in range(left, right + 1):
            total += self.nums[i]       # 每一步都是一次读取 + 加法
        return total
```

#### 复杂度

- **时间复杂度**  
  - `update`：O(1) —— 只改一个数，耗时几乎不变。  
  - `sumRange`：O(n) —— 需要遍历区间内的每个元素，最坏情况是遍历整个数组。  

- **空间复杂度**  
  - O(1) —— 除了保存原数组外，只用了常数个临时变量。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在 `sumRange`：每次查询都要线性遍历。  
我们希望在 **不遍历整个区间** 的情况下，仍然能得到区间和，同时还能快速处理 `update`。  
这正是「**点更新 + 区间求和**」的经典需求，常用的两种数据结构是：

1. **线段树（Segment Tree）**  
2. **树状数组 / 二叉索引树（Binary Indexed Tree，简称 BIT）**

对初学者来说，BIT 更容易实现且代码更简洁，下面用它来做最优解。  

---

##### 什么是 BIT？

想象一本 **“累计账本”**，每一页记录的不是单个数，而是 **从某个位置往前累计的和**。  
比如第 8 页记录的是第 1~8 的总和，第 4 页记录的是第 1~4 的总和，...  
当我们要查询任意区间 `[l, r]` 的和时，只需要：

```
前缀和(r) - 前缀和(l-1)
```

因为前缀和已经提前累计好，只要快速拿到两个前缀和即可。

**为什么更新只改动 O(log n) 个页？**  
在 BIT 中，每个下标 `i` 负责的区间长度由二进制最低位决定（lowbit）。  
更新一个位置 `i` 时，只需要把 `i` 所在的所有「负责该位置」的页的累计值都加上差值 `delta`，这些页的下标正好是 `i, i+lowbit(i), i+lowbit(i+lowbit(i)), …`，数量与数组长度的二进制位数成正比，最多是 `log₂ n`（约 15~16 次，n ≤ 3·10⁴）。

**类比**：把数组想象成一棵**层层递进的金字塔**，每层只记录自己负责的那块区域的总和。改动一个小砖块，只需要把它所在的几层金字塔重新加上差值，层数很少（log n），查询时把对应的几层金字塔相加减即可得到区间和。

---

##### 关键操作

- **lowbit(x)**：`x & (-x)`，得到二进制最低位的 1 所代表的数值。它告诉我们「当前下标负责的区间大小」。
- **add(i, delta)**：把 `delta` 加到 BIT 中下标 `i` 负责的所有区间。循环 `i += lowbit(i)`。
- **prefix_sum(i)**：求 `[1, i]` 的累计和。循环 `i -= lowbit(i)`，把所有负责的区间相加。

**注意**：BIT 采用 **1‑基索引**（下标从 1 开始），所以在实现时要把原数组的下标 `0`~`n-1` 映射到 `1`~`n`。

---

#### 代码（Python）

```python
class NumArray:
    def __init__(self, nums):
        """
        初始化 BIT（树状数组）并构建初始前缀信息
        :type nums: List[int]
        """
        self.n = len(nums)
        # BIT 用 1 基索引，长度需要多一个位置
        self.bit = [0] * (self.n + 1)   # 存放累计信息
        self.nums = nums[:]             # 复制一份原数组，方便后面计算差值

        # 把每个元素的值逐个加入 BIT，构造过程也是 O(n log n)
        for i, val in enumerate(nums):
            self._add(i + 1, val)       # i+1 转成 BIT 的下标

    def _lowbit(self, x):
        """返回 x 的最低位 1 所对应的值，例如 lowbit(6)=2"""
        return x & -x

    def _add(self, idx, delta):
        """
        在 BIT 中把 delta 加到位置 idx 以及它负责的上层节点
        :param idx: 1 基下标
        :param delta: 要增加的数值（可以是负数）
        """
        while idx <= self.n:
            self.bit[idx] += delta      # 累计到当前节点
            idx += self._lowbit(idx)    # 跳到下一个负责的节点

    def _prefix_sum(self, idx):
        """
        求前缀和 sum[0..idx]（idx 为 0 基下标），内部使用 1 基 BIT
        """
        res = 0
        idx += 1                         # 转成 1 基下标
        while idx > 0:
            res += self.bit[idx]        # 把负责的区间累计进来
            idx -= self._lowbit(idx)    # 向左跳到更小的区间
        return res

    def update(self, index, val):
        """
        将 nums[index] 改为 val
        :type index: int
        :type val: int
        """
        # 计算差值：新值 - 旧值
        delta = val - self.nums[index]
        self.nums[index] = val           # 同时更新原数组的副本
        self._add(index + 1, delta)      # 在 BIT 中同步更新

    def sumRange(self, left, right):
        """
        返回闭区间 [left, right] 的元素和
        :type left: int
        :type right: int
        :rtype: int
        """
        # 前缀和公式：sum[left..right] = prefix(right) - prefix(left-1)
        return self._prefix_sum(right) - self._prefix_sum(left - 1)
```

> **代码要点注释**  
> - `self.bit` 用来存放累计信息，长度比原数组多 1（因为 1 基索引）。  
> - `_add` 与 `_prefix_sum` 都是 **循环**，每次跳步大小由 `lowbit` 决定，跳的次数最多等于二进制位数，即 `log₂ n`。  
> - `update` 只需要把差值 `delta` 加进 BIT，而不必重新遍历整个数组。  
> - `sumRange` 只做两次前缀和查询，时间同样是 `O(log n)`。

#### 复杂度

- **时间复杂度**  
  - `update`：O(log n) —— 只在 BIT 中更新 `log n` 个节点。  
  - `sumRange`：O(log n) —— 需要计算两次前缀和，每次遍历 `log n` 个节点。  
  相比暴力解的 O(n)，对 30 000 次查询/更新的上限来说，速度提升巨大。

- **空间复杂度**  
  - O(n) —— 额外的 BIT 数组占用与原数组同等的线性空间（约 30 000 个整数），属于合理的线性额外空间。

---

## 心得

- **核心技巧**：**树状数组（Binary Indexed Tree）** 能在 `log n` 时间内完成「点更新」和「前缀和」两类操作，是「可变区间求和」的标准工具。  
- **适用的类似题目**  
  1. *Range Sum Query - Immutable*（只查询不更新）——可以直接用前缀和。  
  2. *Range Sum Query 2D - Mutable*（二维可变区间求和）——使用二维 BIT 或二维线段树。  
  3. *Range Minimum Query*（区间最小值）——可以用线段树实现类似的点更新 + 区间查询。  
- **一句话总结**：把数组的局部累计提前存进树形结构，更新只改动 log n 个节点，查询只读取 log n 个累计值。

---

## 反思

- **拿到题目时的第一反应**：直接用循环遍历区间求和，觉得最直观。  
- **最容易踩的坑**  
  - **索引偏移**：BIT 使用 1 基索引，容易把原数组的 0 基下标忘记加 1。  
  - **负数和差值**：`delta` 可能为负数，需要在 `_add` 时正确累加（加负数相当于减）。  
  - **边界条件**：`sumRange(left, left)`（单元素区间）以及 `left = 0` 时，需要保证 `prefix_sum(-1)` 正确返回 0。  
- **下次遇到同类题，第一步该想到**：**是否需要同时支持“单点修改”和“区间查询”。**如果是，就立刻考虑 BIT 或线段树，而不是先写暴力遍历。这样可以把时间复杂度从 O(n) 降到 O(log n)。