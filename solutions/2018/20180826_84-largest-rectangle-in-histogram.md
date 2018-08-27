# #84. 柱状图中最大的矩形 / Largest Rectangle in Histogram

> 难度：困难 · 标签：Array、Stack、Monotonic Stack · [LeetCode 链接](https://leetcode.com/problems/largest-rectangle-in-histogram/)

---

## 题目（英文原版）

**Description**

Given an array of integers heights representing the histogram's bar height where the width of each bar is 1, return the area of the largest rectangle in the histogram.

**Examples**

**Example 1:**

```
Input: heights = [2,1,5,6,2,3]
Output: 10
Explanation: The above is a histogram where width of each bar is 1.
The largest rectangle is shown in the red area, which has an area = 10 units.
```

**Example 2:**

```
Input: heights = [2,4]
Output: 4
```

**Constraints**

- 1 <= heights.length <= 105
- 0 <= heights[i] <= 104

---

## 题目（中文翻译）

给定一个整数数组 `heights`，该数组表示直方图（histogram）中每根柱子（bar）的高度，且每根柱子的宽度均为 1，返回该直方图中最大矩形（largest rectangle）的面积。

### 约束条件
- $1 \leq \text{heights.length} \leq 10^5$
- $0 \leq \text{heights}[i] \leq 10^4$

### 示例

#### 示例 1
**输入**  
`heights = [2,1,5,6,2,3]`

**输出**  
`10`

**解释**  
上图是一个每根柱子宽度为 1 的直方图。红色区域即为面积最大的矩形，其面积为 10。

#### 示例 2
**输入**  
`heights = [2,4]`

**输出**  
`4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**枚举所有可能的矩形**，求出它们的面积，最后取最大值。  
直观地把直方图想象成一排小木块，每根木块的高度是 `heights[i]`，宽度都是 1。  
一个合法的矩形必须连续地覆盖若干根木块（比如第 2 根到第 5 根），它的高度只能取这几根木块中最矮的那根的高度，否则矩形会“漏掉”更高的那根。

实现上可以两层循环：

1. 外层循环 `i` 作为矩形左边界的起点。  
2. 内层循环 `j` 从 `i` 向右扩展，每次把当前高度 `heights[j]` 与已经记录的最小高度比较，取较小者作为这段区间的矩形高度。  
3. 用 `height * width` 计算面积，更新全局最大值。

**为什么正确**  
因为我们遍历了**所有**左、右边界的组合，并且每次都使用了这段区间内的最小高度作为矩形的高度，这恰好是构造合法矩形的唯一方式，所以一定能找到最大面积。

**复杂度分析**  
- 外层 `i` 有 `n` 次，内层 `j` 最多也会遍历 `n` 次，整体是 `n × n`，即 **O(n²)**。  
- 只用了常数个额外变量（最大面积、当前最小高度），空间是 **O(1)**。

> 大白话：如果 `n = 10,000`，暴力解要做大约 100,000,000 次“比较+乘法”，在电脑眼里已经是“慢得要命”。  

#### 代码（Python）

```python
def largestRectangleArea_bruteforce(heights):
    """
    暴力解：枚举所有左、右边界，计算最小高度乘宽度
    时间复杂度 O(n^2)，空间复杂度 O(1)
    """
    n = len(heights)
    max_area = 0                         # 保存当前最大的矩形面积

    for left in range(n):                # 左边界从 0 到 n-1
        min_h = heights[left]            # 区间 [left, right] 的最小高度，先设为 left 处的高度
        for right in range(left, n):     # 右边界从 left 向右扩展
            # 更新区间内的最小高度
            min_h = min(min_h, heights[right])
            width = right - left + 1      # 区间宽度 = 右边界 - 左边界 + 1（因为每根柱子宽度都是 1）
            area = min_h * width         # 矩形面积 = 最小高度 × 宽度
            max_area = max(max_area, area)   # 保持最大值

    return max_area
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 两层循环，最坏情况下要检查每一对左、右边界。  
- **空间复杂度**：`O(1)` —— 只用了几个整数变量，不随 `n` 增长。

---

### 2. 最优解

#### 思路  

暴力解慢的根本原因是**重复计算**了区间最小高度。  
例如，当我们把左边界从 `i` 移到 `i+1` 时，很多已经算好的最小值仍然可以直接使用，只需要“把左边的那根柱子剔除”即可。  
这类“只看一次、弹出一次”的需求非常适合 **栈（Stack）**，尤其是 **单调栈（Monotonic Stack）**。

**单调栈的核心思想**  
- 栈里保存柱子的下标，**从栈底到栈顶对应的高度是递增的**（即“单调递增栈”）。  
- 当遍历到第 `i` 根柱子时，若它的高度 **小于** 栈顶柱子的高度，说明栈顶柱子**已经找到了右边界**（因为它右边第一个比它低的柱子就是当前的 `i`），于是可以弹出栈顶并计算以它为**最小高度**的矩形面积。  
- 计算面积时，**左边界**是弹出后栈顶的下一个元素的下标+1（如果栈空则左边界是 0），**右边界**是当前柱子 `i-1`（因为 `i` 是第一个比它低的柱子）。  
- 通过一次遍历把每根柱子都“弹出”一次，所有可能的矩形都会被考虑到，且每根柱子只进栈、出栈各一次，时间线性。

**为什么要在末尾再加一个哨兵 0**  
为了让栈里残留的柱子也能被弹出并计算面积。把高度 0 的柱子视作“终点”，它会把所有剩余的柱子逐一弹出。

**步骤概览（伪代码）**  

```
push -1 onto stack   # -1 充当哨兵，帮助计算左边界
for i from 0 to n (inclusive):
    cur_height = heights[i] if i < n else 0   # 最后一次循环用 0 触发弹出
    while stack top != -1 and cur_height < heights[stack top]:
        h = heights[stack pop]                # 弹出的柱子高度
        left = stack top + 1                  # 弹出后栈顶就是左边界的下标
        width = i - left                      # 当前 i 是右边界的下一个位置
        area = h * width
        update max_area
    push i onto stack
return max_area
```

**类比**：把柱子想象成一排装有不同高度的盒子，单调栈就像一个只允许“递增高度”的托盘。每当出现更低的盒子时，托盘顶端的高盒子就“出货”，因为它已经不能再往右延伸了。

#### 代码（Python）

```python
def largestRectangleArea(heights):
    """
    单调递增栈解法：一次遍历 O(n) 时间，O(n) 空间（栈）
    """
    stack = [-1]               # 初始化栈，-1 作为哨兵，帮助计算左边界
    max_area = 0
    n = len(heights)

    for i in range(n + 1):     # 多跑一次 i=n，用高度 0 作为哨兵让所有柱子出栈
        # 当 i == n 时，cur_height 为 0；否则取真实高度
        cur_height = heights[i] if i < n else 0

        # 若当前高度小于栈顶柱子高度，说明栈顶柱子找到了右边界
        while stack[-1] != -1 and cur_height < heights[stack[-1]]:
            height = heights[stack.pop()]          # 被弹出的柱子高度
            left_index = stack[-1] + 1             # 新栈顶的下标+1 是左边界
            width = i - left_index                 # 右边界是 i-1，宽度 = i - left
            area = height * width
            max_area = max(max_area, area)         # 更新全局最大面积

        stack.append(i)        # 把当前柱子下标压入栈，保持栈中高度递增

    return max_area
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 每根柱子最多进栈一次、出栈一次，整体线性。相比暴力的 `O(n²)`，即使 `n=10⁵` 也能在毫秒级完成。  
- **空间复杂度**：`O(n)` —— 最坏情况下栈会保存所有柱子的下标（例如高度严格递增时），因此需要线性额外空间。

---

## 心得

- 这道题的核心技巧是 **单调栈**，它能够在一次遍历中找到每根柱子左、右最近的更低柱子，从而快速计算以该柱子为最小高度的最大矩形面积。  
- 类似需要“最近更小/更大元素” 的题目还有：
  1. **每日温度（Daily Temperatures）** – 找到右侧第一个更高温度。  
  2. **柱状图中最大的正方形（Largest Square in a Histogram）** – 也是用单调栈来定位边界。  
  3. **子数组最小值的和（Sum of Subarray Minimums）** – 需要左、右最近更小元素的贡献计数。  
- **一句话总结**：用单调递增栈一次遍历即可把“左/右最近更低柱子”这两个隐形信息显式化，进而得到最大矩形面积。

---

## 反思

- **第一反应**：直接想到枚举所有区间（暴力），因为这最容易写对。  
- **最容易踩的坑**：
  - 忘记在遍历结束后让栈中剩余的柱子全部弹出（使用高度 0 的哨兵）。  
  - 计算左边界时，如果栈空需要把左边界视作 0，常常会因为 `stack[-1]` 已经是哨兵 `-1` 而出错。  
  - 高度为 0 的柱子会导致面积为 0，别忘了把它当作“触发弹出”的手段，而不是普通柱子。  
- **下次类似题**：第一步先问自己“我需要知道每个元素左边最近更小/更大的位置吗？”如果答案是“是”，立刻把 **单调栈** 放进工具箱。