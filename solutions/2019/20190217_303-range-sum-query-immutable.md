# #303. 区间和查询 - 不可变 / Range Sum Query - Immutable

> 难度：简单 · 标签：Array、Design、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/range-sum-query-immutable/)

---

## 题目（英文原版）

**Description**

Given an integer array nums, handle multiple queries of the following type:
Implement the NumArray class:

**Examples**

**Example 1:**

```
Input
["NumArray", "sumRange", "sumRange", "sumRange"]
[[[-2, 0, 3, -5, 2, -1]], [0, 2], [2, 5], [0, 5]]
Output
[null, 1, -1, -3]

Explanation
NumArray numArray = new NumArray([-2, 0, 3, -5, 2, -1]);
numArray.sumRange(0, 2); // return (-2) + 0 + 3 = 1
numArray.sumRange(2, 5); // return 3 + (-5) + 2 + (-1) = -1
numArray.sumRange(0, 5); // return (-2) + 0 + 3 + (-5) + 2 + (-1) = -3
```

**Constraints**

- 1 <= nums.length <= 104
- -105 <= nums[i] <= 105
- 0 <= left <= right < nums.length
- At most 104 calls will be made to sumRange.

---

## 题目（中文翻译）

**描述**  
给定一个整数数组 `nums`，需要处理多次区间求和查询。请实现 `NumArray` 类，使其能够在 **O(1)** 的时间复杂度内返回任意区间 `[left, right]`（左闭右闭）的元素和。

**实现要求**  
- `NumArray(int[] nums)`：构造函数，传入整数数组 `nums`。  
- `int sumRange(int left, int right)`：返回下标从 `left` 到 `right` 的子数组（subarray）之和。

**示例**  

```java
NumArray numArray = new NumArray([-2, 0, 3, -5, 2, -1]);
numArray.sumRange(0, 2); // 返回 (-2) + 0 + 3 = 1
numArray.sumRange(2, 5); // 返回 3 + (-5) + 2 + (-1) = -1
numArray.sumRange(0, 5); // 返回 (-2) + 0 + 3 + (-5) + 2 + (-1) = -3
```

**示例输入/输出**  

```
Input
["NumArray", "sumRange", "sumRange", "sumRange"]
[[[-2, 0, 3, -5, 2, -1]], [0, 2], [2, 5], [0, 5]]
Output
[null, 1, -1, -3]
```

**约束条件**  

- `1 <= nums.length <= 10^4`  
- `-10^5 <= nums[i] <= 10^5`  
- `0 <= left <= right < nums.length`  
- 最多会调用 `sumRange` `10^4` 次  

**说明**  
- 由于数组在初始化后不再修改，所有查询都可以基于前缀和（prefix sum）预处理，以实现常数时间查询。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：每次 `sumRange(left, right)` 被调用时，就把下标 `left` 到 `right` 之间的元素逐个加起来，得到答案后返回。  

- **用到的数据结构**：只需要原始的整数数组 `nums`。可以把数组想象成一本书的章节，`left`、`right` 就是要读的起止页码。我们每次都把对应页码的文字（数字）逐字读一遍并求和。  
- **为什么正确**：因为题目要求的就是「区间求和」，遍历一次区间内的所有数并相加，必然得到正确的和。  
- **时间/空间复杂度**：  
  - 时间复杂度：每次查询都要遍历 `right - left + 1` 个元素，最坏情况下相当于遍历整个数组，记作 **O(n)**（这里的 *n* 代表数组长度）。如果有 `q` 次查询，总时间就是 **O(q·n)**。  
  - 空间复杂度：只使用了原数组本身，不需要额外空间，记作 **O(1)**。

> 大白话解释：`O(n)` 就像说「如果你有 1000 本书，最差情况要把每本书的每一页都读一遍」，而 `O(1)` 就是「只需要一支笔，根本不占地方」。

#### 代码（Python）

```python
class NumArray:
    def __init__(self, nums):
        """
        初始化时直接保存原数组。
        """
        self.nums = nums                     # 原数组，像一本书的全部页码

    def sumRange(self, left: int, right: int) -> int:
        """
        暴力遍历 left~right，逐个相加。
        """
        total = 0
        for i in range(left, right + 1):     # 从左边页码一直到右边页码
            total += self.nums[i]            # 把当前页的数字加到总和
        return total
```

#### 复杂度

- **时间复杂度**：`O(n)`（单次查询遍历区间长度），如果有 `q` 次查询则是 `O(q·n)`。  
  > 意味着查询次数多时会变得很慢，就像每次都要重新读一遍同一本书的同一段文字。
- **空间复杂度**：`O(1)`，只用了常数级别的额外变量 `total`。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**重复遍历**是性能瓶颈。  
如果我们事先把 **从数组开头到每个位置的前缀和**算好，后面的查询只需要用「两次前缀和相减」就能得到区间和，时间从 `O(n)` 降到 `O(1)`。

> **前缀和**可以类比为「累计页码的总字数」：  
> - `pre[i]` 表示第 `0`~`i-1` 页的所有数字之和（不包括第 `i` 页）。  
> - 要得到第 `left`~`right` 页的总和，只需要 `pre[right+1] - pre[left]`，相当于「从左边起算到右边的总字数」减去「左边之前的总字数」。

**构造过程**（一次遍历）：

```
pre[0] = 0                                 # 0 页之前的和为 0
for i from 0 to n-1:
    pre[i+1] = pre[i] + nums[i]            # 累加当前页的数字
```

这样 `pre` 长度是 `n+1`，查询时只要做一次减法。

#### 代码（Python）

```python
class NumArray:
    def __init__(self, nums):
        """
        预处理前缀和，时间 O(n)，空间 O(n)。
        """
        self.prefix = [0]                    # prefix[0] = 0
        for num in nums:                     # 一次遍历累计
            self.prefix.append(self.prefix[-1] + num)
            # 这里的 -1 取的是前一个累计值，+ num 加上当前元素

    def sumRange(self, left: int, right: int) -> int:
        """
        通过前缀和求区间和，时间 O(1)。
        """
        # prefix[right+1] 包含了 0~right 的和，prefix[left] 包含了 0~left-1 的和
        return self.prefix[right + 1] - self.prefix[left]
```

#### 复杂度

- **时间复杂度**：  
  - 构造阶段 `O(n)`（只遍历一次数组）。  
  - 单次查询 `O(1)`（只做两次数组访问和一次减法）。  
  > 与暴力解相比，查询速度提升了 **n** 倍，尤其当查询次数很多（题目最多 10⁴ 次）时优势明显。

- **空间复杂度**：`O(n)`，我们额外存了一个长度为 `n+1` 的前缀和数组。  
  > 可以想象为在书的每一页后面都贴了一张小纸条，记录到该页为止的累计字数，省去每次重新阅读的时间。

---

## 心得

- **核心技巧**：前缀和（Prefix Sum）——一次预处理后，任意区间求和均可在常数时间完成。  
- **适用的题型**：  
  1. 「区间求和」系列（如 LeetCode 303、Range Sum Query 2D – Immutable）。  
  2. 「子数组和为 K」等需要快速获取子数组累计值的题目。  
  3. 「滑动窗口」里经常会用到前缀和来判断窗口内元素的和。  
- **一句话总结**：**把“把书一次读完”这一步提前做掉，后面每次只看目录就能知道任意章节的总字数。**

## 反思

- **第一反应**：直接遍历区间求和（暴力），因为这最符合直觉。  
- **最容易踩的坑**：  
  - 忘记在前缀和数组里额外留一个 `0`，导致下标错位。  
  - `left`、`right` 为 0 时的边界处理不当（`prefix[-1]` 会出错）。  
  - 题目要求 `left ≤ right`，但如果写成 `right+1` 越界，需要保证前缀数组长度为 `n+1`。  
- **下次类似题的第一步**：先问自己「是否可以把一次性遍历的结果保存下来？」如果答案是「可以」，就尝试用前缀和或类似的预处理技巧。