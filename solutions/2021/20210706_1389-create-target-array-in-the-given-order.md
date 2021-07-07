# #1389. 按给定顺序创建目标数组 / Create Target Array in the Given Order

> 难度：简单 · 标签：Array、Simulation · [LeetCode 链接](https://leetcode.com/problems/create-target-array-in-the-given-order/)

---

## 题目（英文原版）

**Description**

Given two arrays of integers nums and index. Your task is to create target array under the following rules:
Return the target array.
It is guaranteed that the insertion operations will be valid.

**Examples**

**Example 1:**

```
Input: nums = [0,1,2,3,4], index = [0,1,2,2,1]
Output: [0,4,1,3,2]
Explanation:
nums       index     target
0            0        [0]
1            1        [0,1]
2            2        [0,1,2]
3            2        [0,1,3,2]
4            1        [0,4,1,3,2]
```

**Example 2:**

```
Input: nums = [1,2,3,4,0], index = [0,1,2,3,0]
Output: [0,1,2,3,4]
Explanation:
nums       index     target
1            0        [1]
2            1        [1,2]
3            2        [1,2,3]
4            3        [1,2,3,4]
0            0        [0,1,2,3,4]
```

**Example 3:**

```
Input: nums = [1], index = [0]
Output: [1]
```

**Constraints**

- 1 <= nums.length, index.length <= 100
- nums.length == index.length
- 0 <= nums[i] <= 100
- 0 <= index[i] <= i

---

## 题目（中文翻译）

给定两个整数数组 `nums` 和 `index`。请按照以下规则创建目标数组 `target`：

- 从左到右遍历 `nums`，对于第 `i` 个元素 `nums[i]`，将其 **插入**（insert）到 `target` 的下标为 `index[i]` 的位置。
- 插入后，原本在该位置及其之后的元素向右移动一位。

返回最终得到的 `target` 数组。题目保证所有的插入操作都是合法的。

---

## 示例

### 示例 1  
**输入**: `nums = [0,1,2,3,4]`, `index = [0,1,2,2,1]`  
**输出**: `[0,4,1,3,2]`  
**解释**:

| nums | index | target  |
|------|-------|---------|
| 0    | 0     | [0] |
| 1    | 1     | [0,1] |
| 2    | 2     | [0,1,2] |
| 3    | 2     | [0,1,3,2] |
| 4    | 1     | [0,4,1,3,2] |

---

### 示例 2  
**输入**: `nums = [1,2,3,4,0]`, `index = [0,1,2,3,0]`  
**输出**: `[0,1,2,3,4]`  
**解释**:

| nums | index | target |
|------|-------|--------|
| 1    | 0     | [1] |
| 2    | 1     | [1,2] |
| 3    | 2     | [1,2,3] |
| 4    | 3     | [1,2,3,4] |
| 0    | 0     | [0,1,2,3,4] |

---

### 示例 3  
**输入**: `nums = [1]`, `index = [0]`  
**输出**: `[1]`

---

## 约束条件

- `1 <= nums.length, index.length <= 100`
- `nums.length == index.length`
- `0 <= nums[i] <= 100`
- `0 <= index[i] <= i`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直观的做法就是**模拟题目描述的插入过程**：

1. 从左到右遍历 `nums` 与 `index`。  
2. 把当前的 `nums[i]` 插入到结果数组 `target` 的第 `index[i]` 个位置。  

在 Python 中，列表的 `insert(pos, val)` 方法正好能完成“在第 `pos` 位插入”。  
可以把 `target` 想象成一张 **可伸缩的磁带**，每次把新磁带片（`nums[i]`）粘到指定的格子（`index[i]`）上，后面的磁带片会往后挪。

> **为什么正确**：题目保证每一次插入的下标都是合法的（`0 ≤ index[i] ≤ i`），所以按照给出的顺序逐步插入，最终得到的 `target` 必然就是题目要求的数组。

#### 代码（Python）

```python
def createTargetArray(nums, index):
    """
    暴力模拟插入过程
    :param nums: List[int]   原始数值数组
    :param index: List[int]  对应的插入位置
    :return: List[int]       最终得到的 target 数组
    """
    target = []                     # 初始化空的目标数组
    for i, (num, idx) in enumerate(zip(nums, index)):
        # 在 target 的第 idx 位插入 num
        # Python list 的 insert 方法会自动把后面的元素往后移动一格
        target.insert(idx, num)     # ← 关键操作
    return target
```

#### 复杂度  

- **时间复杂度：** `O(n²)`  
  - 插入操作 `list.insert` 最坏要把插入位置之后的所有元素向后搬移，平均搬移约 `n/2` 次。  
  - 对 `n` 次插入累计起来是 `1 + 2 + … + n ≈ n²/2`，所以是二次时间。  
  - 用大白话说，假设有 100 条数据，每条都要把后面的东西搬一次，搬的次数大约是 5 000 次。

- **空间复杂度：** `O(n)`  
  - 只用了一个额外的列表 `target` 来存放结果，长度正好是 `n`。  

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在于**每次插入都要搬移后面的元素**。如果我们能在 **O(log n)** 的时间内找到第 `k` 空位并填入，就可以把整体复杂度降到 `O(n log n)`。

这正是**树状数组（Fenwick Tree）**擅长的：  
- 树状数组可以在 `O(log n)` 时间内**求前缀和**或**修改单个位置的值**。  
- 这里我们把“空位”看成 1，已占用的位看成 0。  
- 对于第 `i` 次插入，需要在当前还有空位的数组中找到第 `index[i] + 1` 个空位（因为下标是从 0 开始），并把它设为已占用。

实现步骤：

1. 创建长度为 `n` 的树状数组 `bit`，初始时每个位置的值都是 1（表示“空位”。）  
2. 对每个 `i`：  
   - 用二分搜索（配合 `bit.prefix_sum`）在 `bit` 中定位第 `index[i] + 1` 个空位的真实下标 `pos`。  
   - 把 `nums[i]` 放到答案数组 `target[pos]`。  
   - 在 `bit` 中把 `pos` 位置的值从 1 改成 0（`update(pos, -1)`），表示该位已被占用。  

> **类比**：把 `bit` 当成一本**带有“是否已坐满”标记的座位表**。每次要坐第 `k` 位空座时，先在座位表里快速统计前面还有多少空位（前缀和），再二分定位真正的座位号。

#### 代码（Python）

```python
class BIT:
    """树状数组（Fenwick Tree），实现前缀和与单点更新"""
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)   # 1-indexed

    def update(self, idx, delta):
        """把 idx 位置的值加 delta（delta 可以为负）"""
        idx += 1                     # 转成 1-indexed
        while idx <= self.n:
            self.tree[idx] += delta
            idx += idx & -idx        # lowbit，向上遍历

    def query(self, idx):
        """返回区间 [0, idx] 的前缀和"""
        idx += 1                     # 1-indexed
        res = 0
        while idx > 0:
            res += self.tree[idx]
            idx -= idx & -idx
        return res

    def find_kth(self, k):
        """
        在当前数组中找到第 k 个 1 所在的下标（0-indexed）。
        这里的 k 是 1-indexed（第 1 个、 第 2 个 …），
        因为前缀和从 1 开始计数。
        """
        idx = 0
        bit_mask = 1 << (self.n.bit_length())  # 最高位的 2 的幂
        while bit_mask:
            nxt = idx + bit_mask
            if nxt <= self.n and self.tree[nxt] < k:
                k -= self.tree[nxt]
                idx = nxt
            bit_mask >>= 1
        return idx          # 仍是 0-indexed

def createTargetArray(nums, index):
    n = len(nums)
    bit = BIT(n)
    # 初始全部为 1（全部空位）
    for i in range(n):
        bit.update(i, 1)

    target = [0] * n
    for num, idx in zip(nums, index):
        # 需要找第 (idx+1) 个空位
        pos = bit.find_kth(idx + 1)
        target[pos] = num          # 填入答案
        bit.update(pos, -1)        # 该位从空变为已占用
    return target
```

#### 复杂度  

- **时间复杂度：** `O(n log n)`  
  - 每次插入都要在树状数组中 **二分定位第 k 个空位**，时间是 `O(log n)`。  
  - 对 `n` 次操作累计为 `n·log n`，远快于 `n²`。  
  - 用通俗的话说，假如有 100 条数据，普通做法要搬 5 000 次，而优化后只需要大约 `100·log₂100 ≈ 700` 次“查询/更新”。  

- **空间复杂度：** `O(n)`  
  - 除了结果数组 `target`，我们额外用了一个大小为 `n` 的树状数组 `bit`，同样是线性空间。  

---

## 心得

- **核心技巧**：使用 **树状数组（Fenwick Tree）** 实现“第 k 个空位”快速定位，从而把一次线性搬移压缩到对数时间。  
- **适用的题型**  
  1. “在数组中插入并保持顺序”类问题（如 LeetCode 1845、1850）。  
  2. “第 k 大/小元素”或“第 k 空位”查询（如 “数组中的第 K 大元素” 需要离线处理时）。  
- **一句话总结解题钥匙**：**把“找第 k 空位”转化为“前缀和查询”，用树状数组实现 O(log n) 的定位**。

---

## 反思

- **第一反应**：直接用 Python 的 `list.insert`，因为它把插入过程抽象成了一个函数，写起来最省事。  
- **最容易踩的坑**  
  - 忘记题目保证 `index[i] ≤ i`，若自行构造测试用例时违反此条件会导致 `insert` 报错。  
  - 在实现 BIT 时容易把 **1-indexed** 与 **0-indexed** 混淆，导致定位错误。  
- **下次遇到同类题**：第一步先判断 **是否真的需要 O(n²) 的搬移**，如果数据规模可能大，立刻想到使用 **树状数组 / 线段树** 来把“第 k 空位”查询变成对数时间的操作。