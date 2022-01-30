# #1649. 创建有序数组 / Create Sorted Array through Instructions

> 难度：困难 · 标签：Array、Binary Search、Divide and Conquer、Binary Indexed Tree、Segment Tree、Merge Sort、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/create-sorted-array-through-instructions/)

---

## 题目（英文原版）

**Description**

Given an integer array instructions, you are asked to create a sorted array from the elements in instructions. You start with an empty container nums. For each element from left to right in instructions, insert it into nums. The cost of each insertion is the minimum of the following:
For example, if inserting element 3 into nums = [1,2,3,5], the cost of insertion is min(2, 1) (elements 1 and 2 are less than 3, element 5 is greater than 3) and nums will become [1,2,3,3,5].
Return the total cost to insert all elements from instructions into nums. Since the answer may be large, return it modulo 109 + 7

**Examples**

**Example 1:**

```
Input: instructions = [1,5,6,2]
Output: 1
Explanation: Begin with nums = [].
Insert 1 with cost min(0, 0) = 0, now nums = [1].
Insert 5 with cost min(1, 0) = 0, now nums = [1,5].
Insert 6 with cost min(2, 0) = 0, now nums = [1,5,6].
Insert 2 with cost min(1, 2) = 1, now nums = [1,2,5,6].
The total cost is 0 + 0 + 0 + 1 = 1.
```

**Example 2:**

```
Input: instructions = [1,2,3,6,5,4]
Output: 3
Explanation: Begin with nums = [].
Insert 1 with cost min(0, 0) = 0, now nums = [1].
Insert 2 with cost min(1, 0) = 0, now nums = [1,2].
Insert 3 with cost min(2, 0) = 0, now nums = [1,2,3].
Insert 6 with cost min(3, 0) = 0, now nums = [1,2,3,6].
Insert 5 with cost min(3, 1) = 1, now nums = [1,2,3,5,6].
Insert 4 with cost min(3, 2) = 2, now nums = [1,2,3,4,5,6].
The total cost is 0 + 0 + 0 + 0 + 1 + 2 = 3.
```

**Example 3:**

```
Input: instructions = [1,3,3,3,2,4,2,1,2]
Output: 4
Explanation: Begin with nums = [].
Insert 1 with cost min(0, 0) = 0, now nums = [1].
Insert 3 with cost min(1, 0) = 0, now nums = [1,3].
Insert 3 with cost min(1, 0) = 0, now nums = [1,3,3].
Insert 3 with cost min(1, 0) = 0, now nums = [1,3,3,3].
Insert 2 with cost min(1, 3) = 1, now nums = [1,2,3,3,3].
Insert 4 with cost min(5, 0) = 0, now nums = [1,2,3,3,3,4].
​​​​​​​Insert 2 with cost min(1, 4) = 1, now nums = [1,2,2,3,3,3,4].
​​​​​​​Insert 1 with cost min(0, 6) = 0, now nums = [1,1,2,2,3,3,3,4].
​​​​​​​Insert 2 with cost min(2, 4) = 2, now nums = [1,1,2,2,2,3,3,3,4].
The total cost is 0 + 0 + 0 + 0 + 1 + 0 + 1 + 0 + 2 = 4.
```

**Constraints**

- 1 <= instructions.length <= 105
- 1 <= instructions[i] <= 105

---

## 题目（中文翻译）

**题目描述**  
给定一个整数数组 `instructions`，要求按照 `instructions` 中元素的顺序依次将其插入到一个初始为空的容器 `nums` 中，使 `nums` 始终保持升序（sorted）。  
每次插入的代价定义为以下两者的最小值：

- `nums` 中严格小于当前插入元素的个数  
- `nums` 中严格大于当前插入元素的个数  

例如，将元素 `3` 插入到 `nums = [1,2,3,5]` 时，代价为 `min(2, 1)`（因为小于 `3` 的元素有 `1,2` 共 2 个，大于 `3` 的元素有 `5` 共 1 个），插入后 `nums` 变为 `[1,2,3,3,5]`。  

返回将 `instructions` 中所有元素插入完毕的总代价。由于答案可能很大，请返回 **`(10^9 + 7)`** 取模后的结果。

**示例 1**  
```text
Input: instructions = [1,5,6,2]
Output: 1
Explanation:
从空数组开始，nums = []。
- 插入 1，代价 min(0, 0) = 0，nums = [1]。
- 插入 5，代价 min(1, 0) = 0，nums = [1,5]。
- 插入 6，代价 min(2, 0) = 0，nums = [1,5,6]。
- 插入 2，代价 min(1, 2) = 1，nums = [1,2,5,6]。
总代价为 0 + 0 + 0 + 1 = 1。
```

**示例 2**  
```text
Input: instructions = [1,2,3,6,5,4]
Output: 3
Explanation:
从空数组开始，nums = []。
- 插入 1，代价 min(0, 0) = 0，nums = [1]。
- 插入 2，代价 min(1, 0) = 0，nums = [1,2]。
- 插入 3，代价 min(2, 0) = 0，nums = [1,2,3]。
- 插入 6，代价 min(3, 0) = 0，nums = [1,2,3,6]。
- 插入 5，代价 min(3, 1) = 1，nums = [1,2,3,5,6]。
- 插入 4，代价 min(3, 2) = 2，nums = [1,2,3,4,5,6]。
总代价为 0 + 0 + 0 + 0 + 1 + 2 = 3。
```

**示例 3**  
```text
Input: instructions = [1,3,3,3,2,4,2,1,2]
Output: 4
Explanation:
从空数组开始，nums = []。
- 插入 1，代价 min(0, 0) = 0，nums = [1]。
- 插入 3，代价 min(1, 0) = 0，nums = [1,3]。
- 插入 3，代价 min(1, 0) = 0，nums = [1,3,3]。
- 插入 3，代价 min(1, 0) = 0，nums = [1,3,3,3]。
- 插入 2，代价 min(1, 3) = 1，nums = [1,2,3,3,3]。
- 插入 4，代价 min(5, 0) = 0，nums = [1,2,3,3,3,4]。
- 插入 2，代价 min(1, 4) = 1，nums = [1,2,2,3,3,3,4]。
- 插入 1，代价 min(0, 6) = 0，nums = [1,1,2,2,3,3,3,4]。
- 插入 2，代价 min(2, 5) = 2，nums = [1,1,2,2,2,3,3,3,4]。
总代价为 0 + 0 + 0 + 0 + 1 + 0 + 1 + 0 + 2 = 4。
```

**约束条件**  
- `1 <= instructions.length <= 10^5`  
- `1 <= instructions[i] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每一次插入都当成一次“手动排队”。  
我们维护一个已经排好序的列表 `nums`（一开始为空），随后从左到右遍历 `instructions`：

1. **计数**：在把当前元素 `x` 插入 `nums` 之前，先统计 `nums` 中比 `x` 小的元素个数 `cntLess`，以及比 `x 大` 的元素个数 `cntGreater`。  
   - `cntLess` 就是 `x` 左边应该有多少人，`cntGreater` 是右边应该有多少人。  
   - 插入的费用就是 `min(cntLess, cntGreater)`。  

2. **插入**：把 `x` 按照升序插入到 `nums` 中（可以用 `bisect.insort`，它内部会做二分搜索定位插入位置，然后把后面的元素整体右移）。  

3. **累加费用**：把本次费用加入答案。

> **生活类比**：`nums` 像一本已经排好序的电话簿，插入新号码时要先找出它应该排在哪儿（左边有多少比它小，右边有多少比它大），然后把后面的页码整体往后搬，这一步的搬动工作量就是费用。

> **为什么正确**：费用定义本身就是“左边比它小的数”和“右边比它大的数”两者的较小值，暴力做法直接按照定义去统计，自然不会出错。

> **时间/空间复杂度**：  
> - 对每个元素我们都要遍历一次已有的 `nums` 来统计（最坏 O(n)），再把元素插入（最坏 O(n)）。  
> - 所以总时间是 `O(n²)`，其中 `n = len(instructions)`。  
> - 这里的 `O(n²)` 可以想象成“每插入一次，都要把后面的所有元素搬一次”。  
> - 额外空间只用了一个列表 `nums`，大小最多 `n`，即 `O(n)`。

#### 代码（Python）

```python
import bisect

MOD = 10**9 + 7

def createSortedArray_bruteforce(instructions):
    nums = []          # 已经排好序的数组
    total = 0          # 累计费用

    for x in instructions:
        # 统计比 x 小的元素个数（左边）
        # bisect_left 返回第一个 >= x 的位置，即左侧全部 < x
        cnt_less = bisect.bisect_left(nums, x)

        # 统计比 x 大的元素个数（右边）
        # bisect_right 返回第一个 > x 的位置，右侧全部 > x
        cnt_greater = len(nums) - bisect.bisect_right(nums, x)

        # 费用是两者的较小值
        total = (total + min(cnt_less, cnt_greater)) % MOD

        # 把 x 按升序插入 nums（内部会先二分定位，再整体右移）
        bisect.insort(nums, x)

    return total
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 直观理解：如果 `n = 10⁵`，相当于要搬动约 `10¹⁰` 次，显然会超时。  
- **空间复杂度**：`O(n)`  
  - 只需要存放已经插入的元素。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于每次都要 **线性遍历** 已有的数组来统计 `cntLess` 与 `cntGreater`，以及 **整体搬移** 插入元素。  
我们需要一种数据结构，能够在 **对数时间**（`O(log n)`)）内完成以下两件事：

1. **前缀计数**：统计当前已经出现过的、且 **小于** 某个值的元素个数。  
2. **后缀计数**：统计已经出现过的、且 **大于** 某个值的元素个数（可以用 `已插入总数 - 前缀计数 - 与当前值相等的计数`）。

这正好是 **树状数组（Binary Indexed Tree，简称 BIT）** 或 **线段树** 能做的事。  
BIT 维护一个长度为 `maxVal`（这里取 `10⁵`）的数组 `tree`，`tree[i]` 表示下标 `i` 对应的数出现的次数的前缀和。  

**核心操作**（均为 `O(log maxVal)`）：

| 操作 | 说明 |
|------|------|
| `update(i, delta)` | 把下标 `i` 的计数加 `delta`（这里 `delta = 1`），相当于插入一个新元素。 |
| `query(i)` | 返回区间 `[1, i]` 的累计次数，即 **小于等于 i** 的元素个数。 |

**如何求费用**：

- `cntLess = query(x - 1)` → 小于 `x` 的元素数。  
- `cntLessOrEqual = query(x)` → 小于等于 `x` 的元素数。  
- `cntGreater = inserted_sofar - cntLessOrEqual` → 已插入元素总数减去 `≤ x` 的个数，即大于 `x` 的元素数。  
- 费用 = `min(cntLess, cntGreater)`。

**步骤概览**：

1. 初始化 BIT，大小为 `max(instructions)`（不超过 `10⁵`）。  
2. 逐个遍历 `instructions`：  
   - 用 `query` 计算左侧小于当前值的数量。  
   - 用已插入的计数减去 `query(x)` 得到右侧更大的数量。  
   - 累加费用（取模）。  
   - 调用 `update(x, 1)` 把当前值的出现次数记入 BIT。  
3. 返回累计费用。

> **类比**：把 BIT 想象成一本“分层的统计册”。最底层是每个具体数字的出现次数，上层把相邻的几本合并成小册子，查询时只需要快速跳到相应的册子去累加，而不必一本一本翻。

#### 代码（Python）

```python
MOD = 10**9 + 7

class BIT:
    """树状数组（Fenwick Tree），支持前缀和查询和单点增量"""
    def __init__(self, size: int):
        self.n = size
        self.tree = [0] * (size + 1)   # 1-indexed

    def update(self, idx: int, delta: int = 1):
        """把位置 idx 的计数加 delta，时间 O(log n)"""
        while idx <= self.n:
            self.tree[idx] += delta
            idx += idx & -idx        # 低位取反，跳到下一个负责区间的节点

    def query(self, idx: int) -> int:
        """返回前缀和 sum[1..idx]，时间 O(log n)"""
        s = 0
        while idx > 0:
            s += self.tree[idx]
            idx -= idx & -idx        # 去掉最低位 1，向上走
        return s

def createSortedArray(instructions):
    if not instructions:
        return 0

    max_val = max(instructions)          # BIT 的大小，只需要到出现的最大数
    bit = BIT(max_val)

    total_cost = 0
    inserted = 0                         # 已经插入的元素个数

    for x in instructions:
        # 小于 x 的元素数量
        less_cnt = bit.query(x - 1)

        # 小于等于 x 的元素数量
        le_cnt = bit.query(x)

        # 大于 x 的元素数量 = 已插入 - 小于等于 x
        greater_cnt = inserted - le_cnt

        # 本次插入费用
        total_cost = (total_cost + min(less_cnt, greater_cnt)) % MOD

        # 把 x 计入 BIT
        bit.update(x, 1)
        inserted += 1

    return total_cost
```

#### 复杂度

- **时间复杂度**：`O(n log M)`，其中 `n = len(instructions)`，`M = max(instructions)`（≤ 10⁵）。  
  - 与暴力的 `O(n²)` 相比，`log M` 只在 17 左右（因为 `2^17 ≈ 1.3e5`），即使 `n = 10⁵` 也能在毫秒级完成。  
- **空间复杂度**：`O(M)`，即 BIT 数组的大小（最多 `10⁵ + 1`），比原来的 `O(n)` 更紧凑且固定。

---

## 心得

- **核心技巧**：利用树状数组（或线段树）实现**动态前缀计数**，把“统计比当前值小/大的元素个数”从线性降到对数。  
- **适用的题型**：  
  1. **逆序对计数**（LeetCode 493）——统计右侧比当前元素小的个数。  
  2. **数组的第 K 大/小查询**（使用有序集合或 BIT）  
  3. **区间求和 / 区间频次统计**（如 LeetCode 307 – 区间加法）  
- **一句话总结**：**把“每次遍历计数”换成“树状数组的前缀和查询”，即可在 O(log N) 内得到插入费用**。

---

## 反思

- **第一反应**：看到“插入有序数组，费用是左侧小/右侧大的较小值”，立刻想到要实时维护已出现元素的有序结构，暴力实现最自然。  
- **最容易踩的坑**：  
  - **下标越界**：BIT 是 1‑indexed，查询 `x-1` 时要确保 `x>1`，否则返回 0。  
  - **取模时机**：累计费用可能很大，需要在每次加法后 `mod`，防止整数溢出（在 Python 虽不会溢出，但保持一致性）。  
  - **最大值的选择**：如果直接把 BIT 大小设为 `10⁵+5`，可以避免因为指令中出现的最大值恰好是上限而导致的越界。  
- **下次遇到同类题**：第一步先问自己 “我需要快速统计**小于**或**大于**某个值的元素个数吗？” 如果答案是肯定的，就立刻考虑 **树状数组 / 线段树** 或 **有序集合**（如 `bisect`+`SortedList`）来做前缀计数。