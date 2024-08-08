# #2817. **具有约束条件的元素最小绝对差** / Minimum Absolute Difference Between Elements With Constraint

> 难度：中等 · 标签：Array、Binary Search、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/minimum-absolute-difference-between-elements-with-constraint/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums and an integer x.
Find the minimum absolute difference between two elements in the array that are at least x indices apart.
In other words, find two indices i and j such that abs(i - j) >= x and abs(nums[i] - nums[j]) is minimized.
Return an integer denoting the minimum absolute difference between two elements that are at least x indices apart.

**Examples**

**Example 1:**

```
Input: nums = [4,3,2,4], x = 2
Output: 0
Explanation: We can select nums[0] = 4 and nums[3] = 4. 
They are at least 2 indices apart, and their absolute difference is the minimum, 0. 
It can be shown that 0 is the optimal answer.
```

**Example 2:**

```
Input: nums = [5,3,2,10,15], x = 1
Output: 1
Explanation: We can select nums[1] = 3 and nums[2] = 2.
They are at least 1 index apart, and their absolute difference is the minimum, 1.
It can be shown that 1 is the optimal answer.
```

**Example 3:**

```
Input: nums = [1,2,3,4], x = 3
Output: 3
Explanation: We can select nums[0] = 1 and nums[3] = 4.
They are at least 3 indices apart, and their absolute difference is the minimum, 3.
It can be shown that 3 is the optimal answer.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 109
- 0 <= x < nums.length

---

## 题目（中文翻译）

你得到一个下标从 0 开始的整数数组 `nums` 和一个整数 `x`。  
请找出数组中任意两个元素之间的最小绝对差（absolute difference），要求这两个元素的下标之差至少为 `x`。换句话说，寻找满足 `abs(i - j) >= x` 的下标 `i` 与 `j`，使得 `abs(nums[i] - nums[j])` 最小。  
返回满足上述条件的最小绝对差的整数值。

**示例**

**示例 1**  
```
输入: nums = [4,3,2,4], x = 2
输出: 0
解释: 我们可以选择 nums[0] = 4 与 nums[3] = 4。它们的下标相差至少为 2，且绝对差为最小值 0。可以证明 0 为最优答案。
```

**示例 2**  
```
输入: nums = [5,3,2,10,15], x = 1
输出: 1
解释: 我们可以选择 nums[1] = 3 与 nums[2] = 2。它们的下标相差至少为 1，且绝对差为最小值 1。可以证明 1 为最优答案。
```

**示例 3**  
```
输入: nums = [1,2,3,4], x = 3
输出: 3
解释: 我们可以选择 nums[0] = 1 与 nums[3] = 4。它们的下标相差至少为 3，且绝对差为最小值 3。可以证明 3 为最优答案。
```

**约束条件**

- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^9`
- `0 <= x < nums.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把所有满足距离要求的下标对全部枚举一遍，计算它们的绝对差，最后取最小值。

- **枚举方式**：双层循环，外层遍历 `i`（从 `0` 到 `len(nums)-1`），内层遍历 `j`（从 `i+x` 到 `len(nums)-1`），因为题目要求 `|i-j| >= x`，只要让 `j` 从 `i+x` 开始即可，避免重复计数。
- **使用的数据结构**：只需要一个整数变量 `ans` 保存当前的最小差值，**不需要额外的数据结构**。可以把它想象成我们手里唯一的一支笔，只用来记录最小值。

> **为什么这个方法一定对？**  
> 我们把所有合法的 `(i, j)` 都检查了一遍，最小的差值一定在这些检查中出现过，所以取遍历得到的最小值就是答案。

> **时间/空间复杂度大白话**  
> - 时间复杂度 `O(n²)`：如果数组有 `n` 个元素，外层循环跑 `n` 次，内层大约也跑 `n` 次（最坏情况），于是总共要做 `n × n` 次比较。把 `n` 想成 10 000，`n²` 就是 100 000 000，明显太慢了。  
> - 空间复杂度 `O(1)`：只用了常数个额外变量，不会随 `n` 增长。

#### 代码（Python）

```python
from typing import List

def min_absolute_diff_bruteforce(nums: List[int], x: int) -> int:
    n = len(nums)
    ans = float('inf')                 # 先设一个很大的初始值
    for i in range(n):
        # j 必须至少离 i x 个位置
        for j in range(i + x, n):
            diff = abs(nums[i] - nums[j])
            if diff < ans:              # 找到更小的就更新
                ans = diff
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)` — 需要检查所有合法的下标对，数量随 `n` 的平方增长。  
- **空间复杂度**：`O(1)` — 只用了常数个变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **“每次都要遍历所有已经出现的元素去找最接近的值”**，这一步是 `O(n)`，导致整体 `O(n²)`。

我们可以把 “在已经出现的元素中快速找最接近 `nums[j]` 的值” 这一步改成 `O(log n)`，只要使用一种 **有序容器**（如平衡二叉搜索树）即可。  
思路的演进如下：

1. **只考虑 i < j**（因为 `|i-j|` 对称），于是我们从左到右遍历数组，当前下标记作 `j`。
2. 对于每个 `j`，合法的 `i` 必须满足 `i ≤ j - x`。这意味着在处理 `j` 时，**左边已经出现且下标 ≤ j‑x 的元素** 都是候选集合。  
   - 当我们向右走一步（`j` 增加 1），只需要把 `nums[j-x]` 加入候选集合即可。  
   - 用 **有序集合**（在 Python 中可以用 `bisect` + 列表实现）保存这些候选值，集合内部始终保持从小到大排序。
3. 有了有序集合后，**在集合里找最接近 `nums[j]` 的值** 可以用二分查找（`bisect_left`）在 `O(log n)` 时间完成。  
   - `bisect_left` 返回第一个 **不小于** `nums[j]` 的位置。我们检查这个位置和它左边的那个位置（如果存在），因为这两个数分别是 **大于等于** 和 **小于** `nums[j]` 的最近邻，它们的差值中必有最小的。
4. 对每个 `j` 计算得到的差值取全局最小，即为答案。

> **核心数据结构——有序集合（Ordered Set）**  
> 想象一本《电话号码簿》，每次想找最接近的号码，只需要打开目录（已经排好序），用二分法快速定位。这里的“目录”就是我们用 `bisect` 维护的 **排好序的列表**，插入和查找都像在树上走一步，时间都是 `O(log n)`。

#### 代码（Python）

```python
from bisect import bisect_left, insort
from typing import List

def min_absolute_diff(nums: List[int], x: int) -> int:
    """
    使用有序集合（sorted list + 二分查找）实现 O(n log n) 的解法
    """
    n = len(nums)
    # 有序集合，保存已经可以配对的左侧元素值
    sorted_vals = []          # 初始为空
    ans = float('inf')

    for j in range(x, n):     # j 必须至少从 x 开始，这样 j-x 才合法
        # 把下标 i = j - x 对应的值加入有序集合
        # 这里使用 insort，等价于 “把元素插入到已经排好序的列表中”，时间 O(log n)
        insort(sorted_vals, nums[j - x])

        # 在有序集合里找最接近 nums[j] 的值
        pos = bisect_left(sorted_vals, nums[j])   # 第一个 >= nums[j] 的位置

        # 检查右侧（>=）的最近值
        if pos < len(sorted_vals):
            diff = abs(sorted_vals[pos] - nums[j])
            if diff < ans:
                ans = diff

        # 检查左侧（<）的最近值
        if pos > 0:
            diff = abs(sorted_vals[pos - 1] - nums[j])
            if diff < ans:
                ans = diff

    return ans
```

**代码要点解释**（每行中文注释已写在代码里）：

- `sorted_vals` 就像一本随时保持字母顺序的电话簿。  
- `insort(sorted_vals, nums[j - x])` 把新元素插进去，同时保持有序。  
- `bisect_left` 在有序列表里做二分查找，时间 `O(log n)`。  
- 只需要检查 **左边** 和 **右边** 两个最近的候选，因为它们距离 `nums[j]` 最近，其他更远的肯定不会更好。

#### 复杂度

- **时间复杂度**：`O(n log n)` — 循环 `n` 次，每次进行一次 `insort`（插入）和一次 `bisect_left`（查找），这两操作都是 `O(log n)`。相比暴力的 `O(n²)`，速度提升显著。  
- **空间复杂度**：`O(n)` — 最坏情况下有序集合会保存 `n-x` 个元素，随 `n` 成线性增长。

---

## 心得

- **核心技巧**：使用**有序集合**（平衡 BST / SortedList）实现“动态维护左侧候选并快速查询最近邻”。  
- **适用的题型**  
  1. “滑动窗口 + 最小差值” 类，如 **“Maximum Difference Between Two Elements With Constraint”**。  
  2. “区间查询最近值” 类，如 **“Find the K-th Smallest Pair Distance”**。  
  3. “实时维护有序数据并查询前驱/后继” 类，如 **“Contains Duplicate III”**。  
- **一句话总结解题钥匙**：*把左侧可以配对的元素放进一棵保持有序的树，随后对每个新元素只用二分查找最近的邻居即可。*

---

## 反思

- **第一反应**：看到 “至少相隔 x 个位置” 会立刻想到双指针或滑动窗口，于是尝试直接枚举所有合法对，得到暴力解。  
- **最容易踩的坑**  
  1. **忘记只加入 `j-x` 位置的元素**：如果每次都把所有左侧元素都加入集合，集合会包含不合法的配对，导致错误答案。  
  2. **边界条件**：当 `x = 0` 时，`j` 可以从 `0` 开始；当 `x = len(nums)-1` 时，只会有唯一一对，需要保证循环范围正确。  
  3. **处理左侧最近邻**：只检查 `pos`（≥）不够，还要检查 `pos-1`（<），否则在所有左侧值都比 `nums[j]` 大时会漏掉最小差。  
- **下次遇到同类题**：第一步先 **确定窗口/约束的左侧范围**，把这部分元素放进 **有序容器**，随后 **二分查找最近邻**，这样即可把 `O(n²)` 降到 `O(n log n)`。