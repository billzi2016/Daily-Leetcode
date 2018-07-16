# #42. 接雨水 / Trapping Rain Water

> 难度：困难 · 标签：Array、Two Pointers、Dynamic Programming、Stack、Monotonic Stack · [LeetCode 链接](https://leetcode.com/problems/trapping-rain-water/)

---

## 题目（英文原版）

**Description**

Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

**Examples**

**Example 1:**

```
Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6
Explanation: The above elevation map (black section) is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. In this case, 6 units of rain water (blue section) are being trapped.
```

**Example 2:**

```
Input: height = [4,2,0,3,2,5]
Output: 9
```

**Constraints**

- n == height.length
- 1 <= n <= 2 * 104
- 0 <= height[i] <= 105

---

## 题目（中文翻译）

给定 **n** 个非负整数，表示一幅宽度为 1 的高程图（elevation map），计算下雨后能够接住多少单位的雨水。

## 示例

### 示例 1
**输入**  
```json
height = [0,1,0,2,1,0,1,3,2,1,2,1]
```
**输出**  
```json
6
```
**解释**  
上图中的高程图（黑色部分）由数组 `[0,1,0,2,1,0,1,3,2,1,2,1]` 表示。在这种情况下，能够接住 6 单位的雨水（蓝色部分）。

### 示例 2
**输入**  
```json
height = [4,2,0,3,2,5]
```
**输出**  
```json
9
```

## 约束条件
- `n == height.length`
- `1 <= n <= 2 * 10^4`
- `0 <= height[i] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**对每一个柱子**，分别看看它左边最高的柱子和右边最高的柱子各有多高。  
* 左边最高的柱子就像我们站在左侧往右看，能看到的最高“山峰”。  
* 右边最高的柱子就像站在右侧往左看，能看到的最高“山峰”。  

水只能装在**左、右两侧的最高柱子之间的空隙**里，水的高度等于两侧最高柱子中较低的那个减去当前柱子的高度（如果是负数则视为 0）。

> 类比：把每根柱子想成一排排的围墙，左边最高的墙像字典里查到的“左侧最高词”，右边最高的墙像“右侧最高词”。我们只要知道左右两边的最高墙，就能算出这根柱子上能盛多少水。

**为什么正确**：  
水面一定会被左侧最高的墙和右侧最高的墙卡住，水面高度只能是两者中较低的那个；如果当前柱子已经比这个高度高，水自然装不进去（负数取 0）。

**暴力实现**：  
对每个下标 `i`，分别遍历它左边（`0 … i-1`）找最高值 `left_max`，再遍历右边（`i+1 … n-1`）找最高值 `right_max`，然后按公式累计。

#### 代码（Python）

```python
from typing import List

def trap_brute(height: List[int]) -> int:
    n = len(height)
    total = 0                     # 最终答案
    for i in range(n):
        # 1️⃣ 找左侧最高柱子
        left_max = 0
        for j in range(i + 1):    # 包含自身，方便后面比较
            left_max = max(left_max, height[j])

        # 2️⃣ 找右侧最高柱子
        right_max = 0
        for j in range(i, n):    # 包含自身
            right_max = max(right_max, height[j])

        # 3️⃣ 计算当前位置能接的水量
        water = min(left_max, right_max) - height[i]
        if water > 0:             # 负数说明不能盛水
            total += water
    return total
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  对每个位置都要遍历左侧和右侧各一次，等价于把 `n` 次 `O(n)` 的循环套在一起。可以把它想象成“把每根柱子都请来一次大合照”，合照的时间随柱子数量的平方增长。  
- **空间复杂度**：`O(1)`  
  只用了几个额外的整型变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都要重新遍历左、右两边**，导致大量重复工作。我们可以把“左侧最高”和“右侧最高”这两个信息**提前算好**，这样每个位置只需要 O(1) 的时间去查表。

**两遍前缀/后缀最大数组**是最常见的做法：  

1. **左侧最高数组 `left_max[i]`**  
   `left_max[i]` 表示下标 `i` 左边（包括 `i` 本身）最高的柱子高度。  
   递推公式：`left_max[i] = max(left_max[i-1], height[i])`（从左往右扫）。  

2. **右侧最高数组 `right_max[i]`**  
   `right_max[i]` 表示下标 `i` 右边（包括 `i` 本身）最高的柱子高度。  
   递推公式：`right_max[i] = max(right_max[i+1], height[i])`（从右往左扫）。  

有了这两个数组，**每个位置的接水量**直接用公式  
`water[i] = min(left_max[i], right_max[i]) - height[i]`  
累计即可。

> 类比：把左侧最高的高度想成一本“左边最高词典”，右侧最高的高度想成一本“右边最高词典”。我们先把这两本词典全部写好，后面查词（算水量）就只需要 O(1) 的时间。

**进一步优化**：  
其实我们并不需要完整的两张表，只要同时维护**左指针、右指针**以及它们对应的最高值，就可以在一次遍历中完成计算，这就是**双指针**的思路。下面给出双指针实现，它的时间是 `O(n)`，空间只用 `O(1)`。

**双指针核心原理**：

- 设 `left`、`right` 分别指向数组的左端和右端，`left_max`、`right_max` 分别记录目前为止左侧和右侧看到的最高柱子。  
- 每一步比较 `height[left]` 与 `height[right]`：  
  - 如果 `height[left] < height[right]`，说明左侧的最高墙一定比右侧的最高墙低（因为右侧还有更高的墙），**左指针所在位置的水量只受左侧最高墙限制**，可以直接计算 `left_max - height[left]` 并左移。  
  - 否则（右侧更低或相等），右指针位置的水量只受右侧最高墙限制，计算 `right_max - height[right]` 并右移。  

这样每个柱子只会被访问一次，且不需要额外数组。

#### 代码（Python）

```python
from typing import List

def trap(height: List[int]) -> int:
    """
    双指针 + 动态维护左右最高柱子
    时间 O(n)  空间 O(1)
    """
    if not height:
        return 0

    left, right = 0, len(height) - 1          # 两端指针
    left_max, right_max = height[left], height[right]  # 当前看到的最高柱子
    ans = 0

    while left < right:
        if height[left] < height[right]:
            # 左侧较低，左指针位置的水量只受 left_max 限制
            left += 1
            left_max = max(left_max, height[left])   # 更新左侧最高
            ans += max(0, left_max - height[left])   # 累加水量（负数视为 0）
        else:
            # 右侧较低或相等，右指针位置的水量只受 right_max 限制
            right -= 1
            right_max = max(right_max, height[right]) # 更新右侧最高
            ans += max(0, right_max - height[right])   # 累加水量
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  只遍历了一遍数组，`n` 为柱子数量。可以想象成“一次性把所有柱子排队检查”，检查次数随柱子数量线性增长。  

- **空间复杂度**：`O(1)`  
  只用了常数个变量（指针、最高值、累计答案），不随 `n` 增长。

---

## 心得

- **核心技巧**：双指针配合“维护左/右最高柱子”思想。  
- **适用题型**：  
  1. “接雨水”系列（如 42. Trapping Rain Water）  
  2. “最长连续递增子数组”中需要左右边界的情况  
  3. “盛最多水的容器” (LeetCode 11) 也可以用双指针求最优解  
- **一句话总结**：**用双指针把左、右最高墙实时维护，水量自然可算**。

---

## 反思

- **第一反应**：先想到“对每根柱子左右各找最高”，于是写出暴力双循环。  
- **最容易踩的坑**：  
  - 忘记对负数取零，导致累计负值出现错误。  
  - 在双指针实现中，更新 `left_max` / `right_max` 的时机不对，会把当前柱子的高度算进去两次。  
  - 边界条件：空数组或只有一根柱子时直接返回 0。  
- **下次类似题的第一步**：先判断是否可以把“全局信息”（如左/右最高）预处理或动态维护，避免在每个位置重复遍历。这样往往能把 `O(n²)` 降到 `O(n)`。