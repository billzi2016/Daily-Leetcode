# #1752. 检查数组是否已排序并旋转 / Check if Array Is Sorted and Rotated

> 难度：简单 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/check-if-array-is-sorted-and-rotated/)

---

## 题目（英文原版）

**Description**

Given an array nums, return true if the array was originally sorted in non-decreasing order, then rotated some number of positions (including zero). Otherwise, return false.
There may be duplicates in the original array.
Note: An array A rotated by x positions results in an array B of the same length such that B[i] == A[(i+x) % A.length] for every valid index i.

**Examples**

**Example 1:**

```
Input: nums = [3,4,5,1,2]
Output: true
Explanation: [1,2,3,4,5] is the original sorted array.
You can rotate the array by x = 3 positions to begin on the element of value 3: [3,4,5,1,2].
```

**Example 2:**

```
Input: nums = [2,1,3,4]
Output: false
Explanation: There is no sorted array once rotated that can make nums.
```

**Example 3:**

```
Input: nums = [1,2,3]
Output: true
Explanation: [1,2,3] is the original sorted array.
You can rotate the array by x = 0 positions (i.e. no rotation) to make nums.
```

**Constraints**

- 1 <= nums.length <= 100
- 1 <= nums[i] <= 100

---

## 题目（中文翻译）

给定一个数组 `nums`，如果该数组最初是按非递减顺序（non‑decreasing order）排序的，然后旋转（rotated）了若干位置（包括零位置），则返回 `true`；否则返回 `false`。  
原始数组中可能包含重复元素。  

**注意**：将数组 `A` 旋转 `x` 个位置后得到的数组 `B` 与 `A` 长度相同，满足 `B[i] == A[(i + x) % A.length]`，对所有有效索引 `i` 都成立。

### 示例

**示例 1**  
Input: `nums = [3,4,5,1,2]`  
Output: `true`  
Explanation: `[1,2,3,4,5]` 是原始的已排序数组。  
你可以将数组旋转 `x = 3` 个位置，使其以值为 `3` 的元素作为起始位置，得到 `[3,4,5,1,2]`。

**示例 2**  
Input: `nums = [2,1,3,4]`  
Output: `false`  
Explanation: 没有任何已排序的数组在旋转后能够得到 `nums`。

**示例 3**  
Input: `nums = [1,2,3]`  
Output: `true`  
Explanation: `[1,2,3]` 本身就是已排序的数组。  
你可以将数组旋转 `x = 0` 个位置（即不旋转）即可得到 `nums`。

### 约束条件

- `1 <= nums.length <= 100`
- `1 <= nums[i] <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：  
1. 先把原数组 **想象** 成一条环形的链（因为旋转本质上是把链头搬到别的位置）。  
2. 任选一个下标 `start` 作为“可能的旋转起点”。从 `start` 开始依次遍历整个环，如果能够得到 **非递减**（即不下降）的序列，则说明原数组是“先排好序再旋转”的；否则继续尝试下一个 `start`。  

这里用到的唯一数据结构是 **数组** 本身，遍历时需要用到 **模运算** `i % n` 来实现环形访问，类似于“在圆形跑道上跑 n 步”。  

为什么正确？  
- 如果数组真的来源于一次排序后再旋转，那么一定存在一个位置，使得从这里开始顺序阅读整个环会得到原始的有序序列。我们把所有可能的起点都尝试一遍，必然能找到这个位置（如果它真的存在）。

#### 代码（Python）

```python
def check_sorted_and_rotated_bruteforce(nums):
    n = len(nums)

    # 遍历每一个可能的起点
    for start in range(n):
        ok = True                     # 假设从 start 开始是有序的
        for i in range(1, n):
            # 前一个元素的真实下标
            prev_idx = (start + i - 1) % n
            # 当前元素的真实下标
            cur_idx  = (start + i) % n
            # 如果出现下降，则说明这个起点不行
            if nums[prev_idx] > nums[cur_idx]:
                ok = False
                break
        if ok:                         # 找到一个满足条件的起点
            return True
    return False                       # 所有起点都不行
```

#### 复杂度

- **时间复杂度：** `O(n²)`  
  解释：我们有 `n` 个起点，每个起点最多要遍历 `n` 次元素来检查是否有序。`n²` 就是“把 `n` 个人排成 `n` 行”这么多次比较，对 100 长度的数组来说还能接受，但不是最优的。  
- **空间复杂度：** `O(1)`  
  只用了常数个额外变量（`n、start、ok、prev_idx、cur_idx`），不随输入规模增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正的瓶颈**在于我们重复检查了很多相同的相邻关系。  
实际上，只要数一数数组中 **“下降点”**（即 `nums[i] > nums[i+1]`）出现的次数，就能判断是否为“先排好序再旋转”。原因如下：

1. **有序数组** 本身没有下降点（全是 `≤`），所以下降点数为 `0`。  
2. **旋转一次**（把后面的有序段搬到前面）只会在 **连接点** 产生一次下降：`... 最大值 , 最小值 ...`。  
3. **多次旋转** 仍然只会出现 **最多一次** 下降点，因为旋转本质上只是把整个有序序列的起点搬到别的位置，序列内部的相对顺序不变。  

因此，只要 **下降点的数量 ≤ 1**，就一定可以把数组视为一次排序后再旋转得到的；否则不可能。

要注意环形的最后一个元素和第一个元素之间也可能形成下降点，需要一起计数。

#### 代码（Python）

```python
def check_sorted_and_rotated(nums):
    """
    判断数组是否是「先非递减排序，再整体旋转」得到的。
    思路：统计相邻元素之间的下降次数，若不超过 1 次则返回 True。
    """
    n = len(nums)
    drop_cnt = 0                     # 记录下降点的数量

    for i in range(n):
        # 当前元素和下一个元素（环形处理，最后一个元素的下一个是第一个元素）
        nxt = (i + 1) % n
        if nums[i] > nums[nxt]:      # 发现下降
            drop_cnt += 1
            if drop_cnt > 1:         # 提前结束，已超过允许的阈值
                return False

    # drop_cnt 为 0 或 1 时均合法
    return True
```

#### 复杂度

- **时间复杂度：** `O(n)`  
  只遍历了一遍数组，比较次数是 `n`，即“只需要走一圈”。相比暴力的 `n²`，快了很多。  
- **空间复杂度：** `O(1)`  
  只用了几个计数器和下标变量，常数级空间。

---

## 心得

- **核心技巧**：**统计下降点（break points）**，利用环形特性把整个问题转化为一次线性扫描。  
- **适用场景**：  
  1. 判断数组是否为“已排序后旋转”类（如 LeetCode 1752 “Check if Array Is Sorted and Rotated”）。  
  2. 检查循环链表是否已经有序，只需要统计一次“逆序”。  
  3. 判断一段时间序列是否只出现一次峰值/谷值（单调转折点计数）。  
- **一句话总结**：**如果相邻下降的次数不超过一次，数组一定是有序后旋转得到的**。

---

## 反思

- **第一反应**：直接尝试所有可能的起点，写出暴力检查的代码。  
- **最容易踩的坑**：  
  - 忘记把最后一个元素和第一个元素也算进相邻比较，导致对 `[2,1]`、`[1,2]` 等边界 case 判错。  
  - 对于包含相同元素的数组（如 `[1,1,1]`），下降点数仍为 0，仍然应该返回 `True`，代码必须使用 `>` 而不是 `>=`。  
- **下次遇到同类题**：第一步先 **数一数“逆序/下降”出现了几次**，如果超过一次直接返回 `False`，否则返回 `True`。这样可以在 O(n) 时间内快速判断。