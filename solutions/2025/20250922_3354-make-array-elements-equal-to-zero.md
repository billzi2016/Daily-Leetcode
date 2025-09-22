# #3354. 使数组元素全部变为零 / Make Array Elements Equal to Zero

> 难度：简单 · 标签：Array、Simulation、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/make-array-elements-equal-to-zero/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums.
Start by selecting a starting position curr such that nums[curr] == 0, and choose a movement direction of either left or right.
After that, you repeat the following process:
A selection of the initial position curr and movement direction is considered valid if every element in nums becomes 0 by the end of the process.
Return the number of possible valid selections.

**Examples**

**Example 1:**

```
Input: nums = [1,0,2,0,3]
Output: 2
Explanation:
The only possible valid selections are the following:
```

**Example 2:**

```
Input: nums = [2,3,4,0,4,1,0]
Output: 0
Explanation:
There are no possible valid selections.
```

**Constraints**

- 1 <= nums.length <= 100
- 0 <= nums[i] <= 100
- There is at least one element i where nums[i] == 0.

---

## 题目（中文翻译）

给定一个 **整数数组 (integer array)** `nums`。

首先选择一个起始位置 `curr`，要求满足 `nums[curr] == 0`，并且选择一个移动方向，**左** 或 **右**。  
随后，你需要重复以下过程：

> （题目原文未给出具体的操作步骤，这里保留原结构）

如果在过程结束时，`nums` 中的所有元素全部变为 `0`，则该 **起始位置 `curr` 与移动方向的组合** 被视为 **有效选择 (valid selection)**。  
返回所有可能的 **有效选择** 的数量。

## 示例

### 示例 1
**输入**: `nums = [1,0,2,0,3]`  
**输出**: `2`  
**解释**:  
唯一可能的有效选择如下：

（此处原题仅给出“以下”但未列出具体步骤，保持原样）

### 示例 2
**输入**: `nums = [2,3,4,0,4,1,0]`  
**输出**: `0`  
**解释**:  
不存在任何有效选择。

## 约束条件
- `1 <= nums.length <= 100`
- `0 <= nums[i] <= 100`
- 至少存在一个下标 `i` 使得 `nums[i] == 0`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目把 **“从一个值为 0 的位置出发，选定一个方向，最终所有元素都变成 0”** 这件事描述得很抽象。  
把它想象成 **“把左边的水全部倒到右边的水桶里，或者把右边的水全部倒到左边的水桶里”**。  
- 这里的 **水的体积** 就是数组中元素的数值（因为每次只能把 1 单位的值向前/向后移动）。
- 零点（`nums[i] == 0`）相当于 **一个可以放水的空桶**，我们只能把水往它的左边或右边倾倒。

如果我们把所有水都倒向左边的空桶，那么左边的总水量必须和右边的总水量 **相等**，否则不可能把右边的水全部搬进左边的空桶里；同理，倒向右边的空桶也需要左右两侧的水量相等。  

于是，**一个“起始位置 + 方向” 能让数组全部归零的充分必要条件** 就是：

> 该位置左侧所有数的和 与 右侧所有数的和 相等。

所以我们只要遍历数组，找到所有 `nums[i] == 0`，检查它左边的前缀和是否等于右边的后缀和即可。  
如果相等，则 **左、右两个方向** 都合法，贡献 `2` 种可行的选取方式。

> **为什么这样就对了？**  
> 把数组看成一条线段，移动的过程只能把“单位值”从一个位置搬到相邻位置，最终所有值都消失等价于把左侧的所有“单位值”全部搬到右侧（或相反）。只有两侧的总量相同，才能完全抵消。

#### 代码（Python）

```python
def countValidSelections(nums):
    """
    统计满足题意的 (起始位置, 方向) 组合数
    """
    n = len(nums)
    total = sum(nums)                 # 整个数组的总和
    prefix = [0] * n                  # 前缀和，prefix[i] = nums[0] + ... + nums[i]

    cur = 0
    for i, v in enumerate(nums):
        cur += v
        prefix[i] = cur

    ans = 0
    for i, v in enumerate(nums):
        if v != 0:                     # 只能从值为 0 的位置出发
            continue

        # 左侧和 = prefix[i-1]（i 为 0 时左侧和为 0）
        left_sum = prefix[i-1] if i > 0 else 0
        # 右侧和 = total - prefix[i]（去掉左侧和以及当前位置本身）
        right_sum = total - prefix[i]

        if left_sum == right_sum:      # 左右两侧水量相等
            ans += 2                   # 左、右两个方向都合法
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  只需要一次遍历计算前缀和，再遍历一次检查每个 `0` 的左右和是否相等。  
  “`O(n)`” 的含义是：如果数组长度翻倍，程序运行时间大约也会翻倍。

- **空间复杂度**：`O(n)`  
  需要额外的前缀和数组，大小和原数组成正比。  
  “`O(n)`” 表示占用的内存会随输入规模线性增长。

---

### 2. 最优解

#### 思路  

在上面的“暴力”思路里，我们已经使用了最直接、最省时的办法：  
- 只遍历两遍数组，**不需要枚举所有可能的移动步骤**（那会是指数级的爆炸）。
- 关键是把 “模拟搬运过程” 抽象为 **前缀和相等** 的判定。

因此 **已经是最优解**，不存在进一步的时间或空间提升空间。  
下面给出同样思路的稍微精简实现（不必额外保存完整的前缀数组，只用一个变量滚动前缀和）。

#### 代码（Python）

```python
def countValidSelections_opt(nums):
    """
    只用 O(1) 额外空间的实现。
    """
    total = sum(nums)          # 整体和
    left = 0                   # 当前下标左侧的前缀和（不包括当前元素）
    ans = 0

    for i, v in enumerate(nums):
        if v == 0:
            right = total - left - v   # 右侧和 = 整体和 - 左侧和 - 当前元素
            if left == right:
                ans += 2               # 左、右两个方向均合法
        left += v                      # 更新左侧前缀和，为下一轮做准备
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)` – 与上面的解法相同，只是常数因子更小。  
- **空间复杂度**：`O(1)` – 只用了几个整数变量，不随 `n` 增长。

---

## 心得

- **核心技巧**：利用前缀和把“把左边的数全部搬到右边”这一动态过程抽象为“左侧和等于右侧和”的静态判定。
- **适用场景**：  
  1. “平衡数组”类题目（如找分割点，使左右和相等）。  
  2. 需要把数组划分成两段且两段属性相同的题目（如分割数组成相同的子序列）。  
  3. 需要判断是否可以通过局部移动把全局状态归零的模拟题。
- **一句话总结**：  
  **“只要左右两侧的总量相等，零点两边的水（数值）就能相互抵消，所有方向都是合法的。”**

## 反思

- **第一反应**：看到“从 0 出发，选方向，最终全体归零”，第一想法是直接模拟搬运过程，结果会很复杂。
- **最容易踩的坑**：  
  - 忘记 **方向** 也算一种不同的选取，需要乘以 2。  
  - 没有注意到 **左侧或右侧为空** 时的特殊处理（前缀和为 0）。  
  - 把 “左侧和 == 右侧和” 当成 **唯一** 条件，却遗漏了必须 **起点为 0** 的限制。
- **下次思路**：  
  遇到类似“搬运/平衡”题目时，先尝试 **把动态过程抽象为累计量的等式**（前缀和 / 后缀和），再判断是否满足条件，这往往比逐步模拟更简洁高效。