# #1685. 已排序数组的绝对差之和 / Sum of Absolute Differences in a Sorted Array

> 难度：中等 · 标签：Array、Math、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/sum-of-absolute-differences-in-a-sorted-array/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums sorted in non-decreasing order.
Build and return an integer array result with the same length as nums such that result[i] is equal to the summation of absolute differences between nums[i] and all the other elements in the array.
In other words, result[i] is equal to sum(|nums[i]-nums[j]|) where 0 <= j < nums.length and j != i (0-indexed).

**Examples**

**Example 1:**

```
Input: nums = [2,3,5]
Output: [4,3,5]
Explanation: Assuming the arrays are 0-indexed, then
result[0] = |2-2| + |2-3| + |2-5| = 0 + 1 + 3 = 4,
result[1] = |3-2| + |3-3| + |3-5| = 1 + 0 + 2 = 3,
result[2] = |5-2| + |5-3| + |5-5| = 3 + 2 + 0 = 5.
```

**Example 2:**

```
Input: nums = [1,4,6,8,10]
Output: [24,15,13,15,21]
```

**Constraints**

- 2 <= nums.length <= 105
- 1 <= nums[i] <= nums[i + 1] <= 104

---

## 题目（中文翻译）

给定一个按非递减顺序排序的整数数组 `nums`。  
构造并返回一个整数数组 `result`，其长度与 `nums` 相同，使得 `result[i]` 等于 `nums[i]` 与数组中所有其他元素的绝对差之和。  
换句话说，`result[i] = sum(|nums[i] - nums[j]|)`，其中 `0 <= j < nums.length` 且 `j != i`（0 索引）。

示例 1  
Input: `nums = [2,3,5]`  
Output: `[4,3,5]`  
**解释**：假设数组采用 0 索引，则  
`result[0] = |2-2| + |2-3| + |2-5| = 0 + 1 + 3 = 4`，  
`result[1] = |3-2| + |3-3| + |3-5| = 1 + 0 + 2 = 3`，  
`result[2] = |5-2| + |5-3| + |5-5| = 3 + 2 + 0 = 5`。

示例 2  
Input: `nums = [1,4,6,8,10]`  
Output: `[24,15,13,15,21]`  

约束条件  
- `2 <= nums.length <= 10^5`  
- `1 <= nums[i] <= nums[i + 1] <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是：**对每一个位置 `i`，遍历整个数组，累加 `|nums[i] - nums[j]|`**。  
因为题目已经说数组是 **非递减** 排序的，但在暴力解里我们暂时不利用这个信息，只是把它当作普通数组来处理。

- **使用的数据结构**：普通的 Python 列表（list）。我们只需要一次遍历得到每个 `i` 的答案，再把所有答案装进一个新列表返回。  
- **为什么正确**：公式 `|a - b|` 本身就是两个数的绝对差，无论数组是否有序，只要把所有 `j`（`j ≠ i`）的差值相加，就一定得到题目要求的答案。  
- **时间/空间复杂度**：  
  - 对每个 `i`（一共 `n` 次）都要遍历全部 `n` 个元素，**时间复杂度是 `O(n²)`**。  
    - 大白话：如果数组有 10,000 个数，暴力解要做大约 10000 × 10000 = 1 亿次加减运算，明显太慢。  
  - 只用了一个额外的结果数组，**空间复杂度是 `O(n)`**（存放答案），除此之外几乎不占额外空间。

#### 代码（Python）

```python
from typing import List

def get_sum_absolute_differences_bruteforce(nums: List[int]) -> List[int]:
    n = len(nums)
    result = [0] * n                     # 用来存放每个位置的答案
    for i in range(n):                   # 逐个位置 i
        total = 0
        for j in range(n):               # 再遍历所有位置 j
            total += abs(nums[i] - nums[j])   # 累加绝对差
        result[i] = total                # 把结果写入 result[i]
    return result
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 两层循环，每层都是 `n`，所以运算次数随 `n` 的平方增长。  
- **空间复杂度**：`O(n)` —— 只额外开辟了一个长度为 `n` 的数组来存放答案。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于每次都要遍历全部元素**。  
观察题目给出的 **提示**，我们可以利用数组已经排好序的特性，把求和拆成两部分：

对固定的 `i`，  
```
result[i] = (nums[i] - nums[0]) + (nums[i] - nums[1]) + … + (nums[i] - nums[i-1])
          + (nums[i+1] - nums[i]) + (nums[i+2] - nums[i]) + … + (nums[n-1] - nums[i])
```

左边都是 `nums[i]` **减去** 前面的元素，右边都是 **后面元素减去** `nums[i]`。  
把相同的东西提出来：

```
左侧部分 = i * nums[i] - (nums[0] + nums[1] + … + nums[i-1])
右侧部分 = (nums[i+1] + nums[i+2] + … + nums[n-1]) - (n-i-1) * nums[i]
```

于是只要**快速得到任意前缀（前面所有元素之和）和后缀（后面所有元素之和）**，就能在 **O(1)** 时间算出 `result[i]`。  
这正是**前缀和**（prefix sum）技巧的典型应用。

**前缀和**的概念：  
- 把数组的累计和保存下来，例如 `pre[k] = nums[0] + … + nums[k-1]`（注意 `pre[0] = 0`）。  
- 那么任意区间 `[l, r]`（左闭右开）的和就可以用 `pre[r] - pre[l]` 直接得到。  

对本题来说：

- `pre[i]` = 前 `i` 个数的和（不含 `nums[i]`），即 `nums[0] + … + nums[i-1]`。  
- 整个数组的总和 `total = pre[n]`。  
- 后缀和 `suffix_i = total - pre[i+1]`（不含 `nums[i]` 的右侧所有元素）。

把这些代入上面的公式，就能一次遍历得到所有答案，时间降到 **O(n)**。

#### 代码（Python）

```python
from typing import List

def get_sum_absolute_differences(nums: List[int]) -> List[int]:
    n = len(nums)
    # ---------- 1. 计算前缀和 ----------
    # pre[i] 表示前 i 个数的和（不含下标 i 的元素），长度为 n+1，方便直接使用下标
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] + nums[i]      # 累加得到前缀和

    total = pre[n]                         # 整个数组的和

    # ---------- 2. 根据公式计算每个位置的答案 ----------
    result = [0] * n
    for i in range(n):
        left_count = i                     # 左侧有 i 个元素
        right_count = n - i - 1            # 右侧有 n-i-1 个元素

        # 左侧部分：i * nums[i] - 前 i 个数的和
        left_sum = left_count * nums[i] - pre[i]

        # 右侧部分：(右侧所有元素的和) - (右侧元素个数 * nums[i])
        # 右侧所有元素的和 = total - pre[i+1]（去掉左侧+当前元素的和）
        right_sum = (total - pre[i + 1]) - right_count * nums[i]

        result[i] = left_sum + right_sum   # 两部分相加即为答案

    return result
```

> **关键点注释**  
> - `pre[i]` 的意义相当于“查字典”，`i` 是键，`pre[i]` 是对应的“页码”（前缀和）。  
> - `left_sum` 和 `right_sum` 分别对应公式的左侧、右侧，两者相加即为最终结果。  
> - 整个循环里只用了常数次加减乘除运算，真正实现了 **线性时间**。

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历两遍数组（一次建前缀和，一次计算答案），每一步都是 **常数时间**。  
  - 与暴力解的 `O(n²)` 对比：如果 `n = 10⁵`，最优解只需要约 `10⁵` 次运算，轻松跑在毫秒级，而暴力解根本不可接受。  
- **空间复杂度**：`O(n)` —— 额外使用了长度为 `n+1` 的前缀和数组 `pre`，以及返回的 `result`。如果不计返回值，额外空间仍是 `O(n)`。

---

## 心得

- **核心技巧**：利用数组已排序的特性，将绝对差拆分为 “左侧全部减去” 与 “右侧全部减去”，进而用前缀和快速求区间和。  
- **适用的题型**  
  1. “前缀和求区间和” 类题目，例如 “子数组和”等。  
  2. “基于排序的差值求和” 类题目，如 “数组的差值之和” / “所有配对的距离之和”。  
- **解题钥匙**：**把全局的 O(n²) 求和拆成两段局部的线性运算 + 前缀和**。

---

## 反思

- **第一反应**：看到“所有绝对差的和”，自然想到两层循环逐个相减。  
- **最容易踩的坑**  
  - **忘记排除 `i == j`**：虽然 `|a-a| = 0`，但在公式推导时要明确不计入自身。  
  - **前缀和下标错误**：`pre[i]` 表示前 `i` 个元素的和，容易写成 `pre[i-1]` 或 `pre[i+1]`，导致 off‑by‑one 错误。  
  - **整数溢出**：在某些语言里累计和可能超出 32 位整数范围，Python 自动大整数不成问题，但要保持警惕。  
- **下次遇到同类题**：**先检查是否可以把“全局”求和拆成左/右两块**，再考虑 **前缀和 / 后缀和** 或 **双指针** 等线性技巧。这样往往能从 O(n²) 直接跳到 O(n)。