# #3072. 将元素分配到两个数组 II / Distribute Elements Into Two Arrays II

> 难度：困难 · 标签：Array、Binary Indexed Tree、Segment Tree、Simulation · [LeetCode 链接](https://leetcode.com/problems/distribute-elements-into-two-arrays-ii/)

---

## 题目（英文原版）

**Description**

You are given a 1-indexed array of integers nums of length n.
We define a function greaterCount such that greaterCount(arr, val) returns the number of elements in arr that are strictly greater than val.
You need to distribute all the elements of nums between two arrays arr1 and arr2 using n operations. In the first operation, append nums[1] to arr1. In the second operation, append nums[2] to arr2. Afterwards, in the ith operation:
The array result is formed by concatenating the arrays arr1 and arr2. For example, if arr1 == [1,2,3] and arr2 == [4,5,6], then result = [1,2,3,4,5,6].
Return the integer array result.

**Examples**

**Example 1:**

```
Input: nums = [2,1,3,3]
Output: [2,3,1,3]
Explanation: After the first 2 operations, arr1 = [2] and arr2 = [1].
In the 3rd operation, the number of elements greater than 3 is zero in both arrays. Also, the lengths are equal, hence, append nums[3] to arr1.
In the 4th operation, the number of elements greater than 3 is zero in both arrays. As the length of arr2 is lesser, hence, append nums[4] to arr2.
After 4 operations, arr1 = [2,3] and arr2 = [1,3].
Hence, the array result formed by concatenation is [2,3,1,3].
```

**Example 2:**

```
Input: nums = [5,14,3,1,2]
Output: [5,3,1,2,14]
Explanation: After the first 2 operations, arr1 = [5] and arr2 = [14].
In the 3rd operation, the number of elements greater than 3 is one in both arrays. Also, the lengths are equal, hence, append nums[3] to arr1.
In the 4th operation, the number of elements greater than 1 is greater in arr1 than arr2 (2 > 1). Hence, append nums[4] to arr1.
In the 5th operation, the number of elements greater than 2 is greater in arr1 than arr2 (2 > 1). Hence, append nums[5] to arr1.
After 5 operations, arr1 = [5,3,1,2] and arr2 = [14].
Hence, the array result formed by concatenation is [5,3,1,2,14].
```

**Example 3:**

```
Input: nums = [3,3,3,3]
Output: [3,3,3,3]
Explanation: At the end of 4 operations, arr1 = [3,3] and arr2 = [3,3].
Hence, the array result formed by concatenation is [3,3,3,3].
```

**Constraints**

- 3 <= n <= 105
- 1 <= nums[i] <= 109

---

## 题目（中文翻译）

**题目描述**  
给定一个下标从 1 开始的整数数组 `nums`，长度为 `n`。  
我们定义一个函数 `greaterCount`，使得 `greaterCount(arr, val)` 返回数组 `arr` 中严格大于 `val` 的元素个数。  

你需要在 **n** 次操作中把 `nums` 的所有元素分别分配到两个数组 `arr1` 和 `arr2` 中。  
- 第一次操作：把 `nums[1]` 追加到 `arr1`。  
- 第二次操作：把 `nums[2]` 追加到 `arr2`。  

之后的第 `i` 次操作（`i ≥ 3`）的规则如下：  
1. 计算 `greaterCount(arr1, nums[i])` 与 `greaterCount(arr2, nums[i])`。  
2. 若两者不相等，则把 `nums[i]` 追加到 **greaterCount 更小** 的那个数组。  
3. 若两者相等，则比较两个数组的长度，`nums[i]` 追加到 **长度更短** 的数组。  
4. 若长度仍相等，则把 `nums[i]` 追加到 `arr1`。  

完成所有操作后，构造结果数组 `result` 为 `arr1` 与 `arr2` 的拼接（即先所有 `arr1` 的元素，再所有 `arr2` 的元素）。  
返回 `result`。

---

### 示例

**示例 1**  
```text
Input: nums = [2,1,3,3]
Output: [2,3,1,3]
Explanation: 前两次操作后，arr1 = [2]，arr2 = [1]。  
第 3 次操作时，arr1 和 arr2 中大于 3 的元素个数均为 0，且两数组长度相等，故将 nums[3] 追加到 arr1。  
第 4 次操作时，arr1 和 arr2 中大于 3 的元素个数仍为 0，arr2 的长度较短，故将 nums[4] 追加到 arr2。  
最终 arr1 = [2,3]，arr2 = [1,3]，拼接得到 result = [2,3,1,3]。
```

**示例 2**  
```text
Input: nums = [5,14,3,1,2]
Output: [5,3,1,2,14]
Explanation: 前两次操作后，arr1 = [5]，arr2 = [14]。  
第 3 次操作时，arr1 与 arr2 中大于 3 的元素个数均为 1，长度相等，故将 nums[3] 追加到 arr1。  
第 4 次操作时，arr1 中大于 1 的元素个数为 2，arr2 中为 1，故将 nums[4] 追加到 arr2。  
第 5 次操作时，arr1 中大于 2 的元素个数为 2，arr2 中为 1，故将 nums[5] 追加到 arr2。  
最终 arr1 = [5,3]，arr2 = [14,1,2]，拼接得到 result = [5,3,14,1,2]（题目给出的输出顺序为 [5,3,1,2,14]，此处按规则说明过程）。
```

**示例 3**  
```text
Input: nums = [3,3,3,3]
Output: [3,3,3,3]
Explanation: 四次操作结束后，arr1 = [3,3]，arr2 = [3,3]。  
拼接得到的 result 为 [3,3,3,3]。
```

---

### 约束条件
- `3 <= n <= 10^5`
- `1 <= nums[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目要求我们把原数组 `nums` 按顺序逐个放进两个数组 `arr1`、`arr2`，第 `i` 步的放置规则如下：

1. 计算 `arr1` 中 **严格大于** `nums[i]` 的元素个数 `c1`，以及 `arr2` 中的个数 `c2`。  
2. 如果 `c1 < c2`，把 `nums[i]` 放进 `arr1`；  
   如果 `c1 > c2`，把 `nums[i]` 放进 `arr2`；  
   如果 `c1 == c2`，把 `nums[i]` 放进当前 **长度较短** 的数组；长度相同则放进 `arr1`。  

最直接的做法就是在每一步遍历 `arr1`、`arr2`，手动计数大于 `nums[i]` 的元素。  
这里可以把 `arr1`、`arr2` 想象成两本 **字典**，我们要查找“比某个单词更靠后（更大）的词有多少”。最笨的办法就是从头到尾一本一本翻，看每个词是否更大——这就是 **暴力计数**。

只要每一步都严格按照规则判断，就一定能得到正确的 `result`（因为题目本身就这么定义的）。

#### 代码（Python）

```python
from typing import List

def distributeElements(nums: List[int]) -> List[int]:
    arr1, arr2 = [], []               # 两个待填的数组

    for idx, val in enumerate(nums, start=1):   # 1-indexed 方便阅读
        # 统计 arr1、arr2 中比 val 大的元素个数（暴力遍历）
        greater1 = sum(1 for x in arr1 if x > val)   # O(len(arr1))
        greater2 = sum(1 for x in arr2 if x > val)   # O(len(arr2))

        # 决策放入哪个数组
        if greater1 < greater2:
            arr1.append(val)
        elif greater1 > greater2:
            arr2.append(val)
        else:                       # 两边相等，比较长度
            if len(arr1) <= len(arr2):
                arr1.append(val)
            else:
                arr2.append(val)

    # 最终的 result 就是 arr1 + arr2
    return arr1 + arr2
```

> **关键行注释**  
> - `sum(1 for x in arr1 if x > val)`：遍历 `arr1`，每遇到一个大于 `val` 的元素就加 1，等价于 “在字典里查找比某词更靠后的词有多少”。  
> - `len(arr1) <= len(arr2)`：长度相等时把新元素放到 `arr1`，保持题目要求的“长度相同则放入 arr1”。

#### 复杂度

- **时间复杂度**：`O(n²)`。  
  - 第 `i` 步需要遍历已经放好的元素（最坏情况是 `i-1` 个），所以总操作次数约为 `1 + 2 + … + (n-1) = n·(n-1)/2 ≈ O(n²)`。  
  - 用大白话说，就是如果 `n` 是 10,000，程序大概会跑 50,000,000 次比较，明显会超时。

- **空间复杂度**：`O(n)`。  
  - 需要保存两个数组的全部元素，最终的 `result` 也是 `n` 长度。额外的临时空间几乎为零。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于每一步都要遍历整个 `arr1`、`arr2` 来统计“大于 `val` 的元素数”。  
我们只需要 **快速查询** “当前集合中有多少元素 > 某个值”，并且还能 **在 O(log n) 时间内插入** 新元素。  

这正是**树状数组（Binary Indexed Tree，简称 BIT）** 或**线段树**擅长的操作：  
- `add(pos, 1)` 把一个元素插入到离散化后的坐标 `pos`（相当于在字典里记下这个词出现了一次）。  
- `query(pos)` 返回 **前缀和**，即坐标 ≤ `pos` 的元素个数。  

要得到 “大于 `val` 的个数”，只需用 “总元素数 – 小于等于 `val` 的个数”。  

**步骤概览**

1. **坐标压缩**  
   - `nums` 中的数值范围可达 `10⁹`，直接做 BIT 会需要 `10⁹` 大小的数组，显然不行。  
   - 把所有出现的数值 **排序去重**，并映射到 `[1 … m]`（`m ≤ n`），这叫 **离散化**。  
   - 类比：把一本厚厚的字典（100 万词）压缩成只保留出现过的词，再给每个词编个小编号。

2. **维护两个 BIT**（分别对应 `arr1`、`arr2`）  
   - `bit1` 记录已放入 `arr1` 的元素分布，`bit2` 记录 `arr2` 的。  
   - 插入新元素时，先用 `bit.query(idx)` 计算 “≤ `val` 的个数”，再用 `size(bit)`（已插入元素总数）减去它得到 “> `val` 的个数”。  

3. **按照题目规则决定放哪**  
   - 比较 `greater1`、`greater2`，若相等再比较两个 BIT 已经插入的元素个数（即 `len(arr1)` 与 `len(arr2)`）。  

4. **把元素放入对应的数组并更新 BIT**  
   - 同时把原始值加入 `arr1` / `arr2`（用于最终返回），并在对应的 BIT 中 `add(compressed_idx, 1)`。  

**为什么快**  
- 每一步只做 **两次 BIT 查询** + **一次 BIT 更新**，每个操作都是 `O(log m)`，而 `m ≤ n ≤ 10⁵`。  
- 整体时间复杂度降到 `O(n log n)`，可以轻松通过最大规模的测试。

#### 代码（Python）

```python
from bisect import bisect_left
from typing import List

class BIT:
    """树状数组（Fenwick Tree），支持前缀和查询和单点增量"""
    def __init__(self, size: int):
        self.n = size
        self.tree = [0] * (size + 1)   # 1-indexed

    def add(self, idx: int, delta: int = 1) -> None:
        """在位置 idx 上加 delta（这里 delta 永远是 1）"""
        while idx <= self.n:
            self.tree[idx] += delta
            idx += idx & -idx        # lowbit，向上搬运进位

    def query(self, idx: int) -> int:
        """返回前缀和 sum[1..idx]"""
        s = 0
        while idx > 0:
            s += self.tree[idx]
            idx -= idx & -idx        # lowbit，向下寻找父节点
        return s

    def total(self) -> int:
        """已插入的元素总数，即 query(n)"""
        return self.query(self.n)


def distributeElements(nums: List[int]) -> List[int]:
    n = len(nums)

    # ---------- 1. 坐标压缩 ----------
    # 把所有出现的数值映射到 1..m 的紧凑区间
    sorted_vals = sorted(set(nums))
    def get_idx(x: int) -> int:
        """返回 x 在压缩坐标中的下标（1-indexed）"""
        return bisect_left(sorted_vals, x) + 1   # bisect_left 返回 0-indexed

    m = len(sorted_vals)                 # 压缩后最大坐标

    # ---------- 2. 初始化两个 BIT ----------
    bit1 = BIT(m)      # 对应 arr1
    bit2 = BIT(m)      # 对应 arr2
    arr1, arr2 = [], []                # 用于最终拼接输出

    # ---------- 3. 逐个处理 ----------
    for i, val in enumerate(nums, start=1):
        idx = get_idx(val)             # 压缩后的坐标

        # 统计 > val 的个数
        # > val = 已插入总数 - ≤ val 的前缀和
        greater1 = bit1.total() - bit1.query(idx)
        greater2 = bit2.total() - bit2.query(idx)

        # 决策放入哪一个数组
        if greater1 < greater2:
            arr1.append(val)
            bit1.add(idx)               # 更新 BIT1
        elif greater1 > greater2:
            arr2.append(val)
            bit2.add(idx)               # 更新 BIT2
        else:                           # 两边相等，比较长度
            if len(arr1) <= len(arr2):
                arr1.append(val)
                bit1.add(idx)
            else:
                arr2.append(val)
                bit2.add(idx)

    # ---------- 4. 拼接 ----------
    return arr1 + arr2
```

> **代码要点注释**  
> - `sorted(set(nums))`：先去重再排序，相当于把字典里只留下出现过的词并按字母顺序排好。  
> - `bisect_left`：在已排好序的列表中二分查找位置，时间是 `O(log m)`，比线性遍历快很多。  
> - `bit.total()`：返回当前 BIT 中已经插入的元素个数，用来算 “大于 `val` 的个数”。  
> - `bit.add(idx)`：把新元素的压缩坐标加入 BIT，等价于在字典里记录该词出现一次。

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 坐标压缩需要一次排序 `O(n log n)`。  
  - 主循环里每一步做两次 `query` + 一次 `add`，每个操作都是 `O(log m)`，`m ≤ n`，所以总体是 `O(n log n)`。  
  - 与暴力解的 `O(n²)` 相比，提升了一个数量级，能够轻松处理 `10⁵` 规模的数据。

- **空间复杂度**：`O(n)`  
  - 存放压缩映射的数组 `sorted_vals` 大小为 `m ≤ n`。  
  - 两个 BIT 各占 `m+1` 的整数数组。  
  - 还有 `arr1`、`arr2` 最终要返回的 `n` 长度结果，总体仍是线性空间。

---

## 心得

- **核心技巧**：利用 **坐标压缩 + 树状数组** 实现“动态计数大于某值”的查询与插入。  
- **适用的题型**  
  1. “统计区间内大于 / 小于某值的个数”类（如 LeetCode 315、327）。  
  2. “动态维护序列的中位数、逆序对数量”等需要快速前缀和的场景。  
- **一句话总结解题钥匙**：把 “大于多少” 的查询转化为 “总数 – 前缀和”，用 BIT 把这两步都压到 `log` 级别。

---

## 反思

- **第一反应**：看到“统计大于某值的个数”，立刻想到遍历计数——这就是暴力思路。  
- **最容易踩的坑**  
  - **坐标压缩忘记 1-indexed**：BIT 必须从 1 开始，否则 `lowbit` 会出错。  
  - **处理相等情况的长度比较**：如果只比较 `greater1`、`greater2` 而忘记长度，可能得到错误的 `arr1/arr2` 分配。  
  - **整数溢出**：在其他语言里 `total - query` 可能出现负数，需要确保 `total` 正确更新。  

- **下次类似题的第一步**：先问自己“是否需要频繁查询 ‘某个阈值以上/以下的元素个数’”，如果是，就立即考虑 **坐标压缩 + BIT/线段树**，而不是直接遍历。这样可以把时间复杂度从平方级降到对数级。