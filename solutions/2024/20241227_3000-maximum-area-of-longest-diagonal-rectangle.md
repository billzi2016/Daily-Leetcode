# #3000. 最长对角线矩形的最大面积 / Maximum Area of Longest Diagonal Rectangle

> 难度：简单 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/maximum-area-of-longest-diagonal-rectangle/)

---

## 题目（英文原版）

**Description**

You are given a 2D 0-indexed integer array dimensions.
For all indices i, 0 <= i < dimensions.length, dimensions[i][0] represents the length and dimensions[i][1] represents the width of the rectangle i.
Return the area of the rectangle having the longest diagonal. If there are multiple rectangles with the longest diagonal, return the area of the rectangle having the maximum area.

**Examples**

**Example 1:**

```
Input: dimensions = [[9,3],[8,6]]
Output: 48
Explanation: 
For index = 0, length = 9 and width = 3. Diagonal length = sqrt(9 * 9 + 3 * 3) = sqrt(90) ≈ 9.487.
For index = 1, length = 8 and width = 6. Diagonal length = sqrt(8 * 8 + 6 * 6) = sqrt(100) = 10.
So, the rectangle at index 1 has a greater diagonal length therefore we return area = 8 * 6 = 48.
```

**Example 2:**

```
Input: dimensions = [[3,4],[4,3]]
Output: 12
Explanation: Length of diagonal is the same for both which is 5, so maximum area = 12.
```

**Constraints**

- 1 <= dimensions.length <= 100
- dimensions[i].length == 2
- 1 <= dimensions[i][0], dimensions[i][1] <= 100

---

## 题目（中文翻译）

**题目描述**  
给定一个二维 0 索引整数数组 `dimensions`。  
对于所有下标 `i`（`0 <= i < dimensions.length`），`dimensions[i][0]` 表示第 `i` 个矩形的长度，`dimensions[i][1]` 表示第 `i` 个矩形的宽度。  
返回对角线最长的矩形的面积。如果有多个矩形的对角线长度相同，则返回面积最大的矩形的面积。

**示例 1**  
```
Input: dimensions = [[9,3],[8,6]]
Output: 48
Explanation: 
对于下标 0，长度 = 9，宽度 = 3。对角线长度 = sqrt(9 * 9 + 3 * 3) = sqrt(90) ≈ 9.487。  
对于下标 1，长度 = 8，宽度 = 6。对角线长度 = sqrt(8 * 8 + 6 * 6) = sqrt(100) = 10。  
因此，下标为 1 的矩形拥有更大的对角线长度，返回其面积 = 8 * 6 = 48。
```

**示例 2**  
```
Input: dimensions = [[3,4],[4,3]]
Output: 12
Explanation: 两个矩形的对角线长度相同，均为 5，所以返回面积更大的矩形的面积，即 12。
```

**约束条件**  
- `1 <= dimensions.length <= 100`  
- `dimensions[i].length == 2`  
- `1 <= dimensions[i][0], dimensions[i][1] <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法就是把每个矩形的对角线长度算出来，和当前记录的最长对角线比较，若更长就更新答案；若相等则比较面积，取更大的面积。  

- **使用的数据结构**：只需要遍历一次 `dimensions`，用两个普通变量 `max_diag2`（对角线长度的平方）和 `max_area` 来保存目前找到的最佳值。这里的对角线平方相当于“查字典”，键是对角线长度，值是对应的面积，只是我们手动维护两个变量而已。  
- **为什么正确**：对角线长度是 `sqrt(l² + w²)`，平方根是单调递增函数，比较 `l² + w²` 与 `l'² + w'²` 的大小等价于比较对应的对角线长度大小。若出现相同的对角线平方，则题目要求取面积更大的矩形，直接比较 `l*w` 即可。  

#### 代码（Python）

```python
from typing import List

def maxAreaOfLongestDiagonal(dimensions: List[List[int]]) -> int:
    max_diag2 = -1          # 当前最大对角线长度的平方（初始化为-1保证第一个矩形会被更新）
    max_area = 0            # 对应的最大面积

    for idx, (l, w) in enumerate(dimensions):
        # 对角线长度的平方，避免使用 sqrt
        diag2 = l * l + w * w          # l² + w²
        area = l * w                    # 矩形面积

        # ① 对角线更长 → 直接更新
        # ② 对角线相等且面积更大 → 也更新
        if diag2 > max_diag2 or (diag2 == max_diag2 and area > max_area):
            # 打印调试信息（可选）
            # print(f"第 {idx} 个矩形更新: 长={l}, 宽={w}, 对角线²={diag2}, 面积={area}")
            max_diag2 = diag2
            max_area = area

    return max_area
```

#### 复杂度

- **时间复杂度**：`O(n)`，其中 `n = len(dimensions)`。我们只遍历一次数组，做常数次算术运算和比较。  
  - 大白话：如果有 100 个矩形，就需要看 100 次，每次花的时间几乎一样，所以总时间和矩形个数成正比。
- **空间复杂度**：`O(1)`，只用了固定的几个变量，不会随 `n` 增长而增加额外的内存。

---

### 2. 最优解

#### 思路  
从暴力解可以看到，真正的瓶颈不在遍历，而在**计算对角线时使用了 `sqrt`**。平方根运算在实际运行中稍慢，而且会产生浮点数，比较时可能出现精度误差。  
优化的关键是**用对角线的平方代替实际长度**：

1. 对每个矩形，计算 `l² + w²`（对角线的平方），这完全是整数运算。  
2. 用整数比较 `diag2` 的大小，等价于比较实际对角线长度。  
3. 当出现相同的 `diag2` 时，再比较面积 `l * w`，取更大的。

这样我们仍然只遍历一次，时间不变，但去掉了 `sqrt`，使常数因子更小，且避免了浮点数误差。  

> **类比**：想象你在比较两条绳子的长度，直接拉长测量会比较麻烦；如果你知道每条绳子对应的“能量”是长度的平方，那么比较能量大小就能直接判断哪条绳子更长，而不必真的去测量。

#### 代码（Python）

```python
from typing import List

def maxAreaOfLongestDiagonal(dimensions: List[List[int]]) -> int:
    # 初始化为最小可能值，保证第一个矩形一定会进入更新逻辑
    best_diag2 = -1   # 最长对角线的平方
    best_area = 0     # 对应的最大面积

    for l, w in dimensions:
        diag2 = l * l + w * w   # 对角线长度的平方（整数）
        area = l * w            # 矩形面积

        # 更新规则同上，只是这里已经没有 sqrt 了
        if diag2 > best_diag2 or (diag2 == best_diag2 and area > best_area):
            best_diag2 = diag2
            best_area = area

    return best_area
```

#### 复杂度

- **时间复杂度**：`O(n)`，与暴力解相同，只是去掉了 `sqrt`，实际运行更快。  
  - 与暴力解对比：理论上相同，但常数更小，尤其在 Python 这种解释型语言里，整数运算比浮点 `sqrt` 快很多。
- **空间复杂度**：`O(1)`，仍然只使用固定的几个变量。

---

## 心得

- **核心技巧**：把涉及平方根的比较转化为**比较平方**，利用单调性避免浮点数和额外的计算。  
- **适用的题型**：  
  1. “比较两点之间的距离大小”类（如求最近/最远点）  
  2. “判断圆与矩形、点与圆的相对位置”类（经常用 `dx²+dy²`）  
  3. “找最大/最小斜率、长度”等需要比较几何量的题目  
- **一句话总结**：**用整数的平方代替根号比较，既安全又高效。**

---

## 反思

- **第一反应**：直接把每个矩形的对角线算出来，用 `math.sqrt` 再比较，感觉最直观。  
- **最容易踩的坑**：  
  - 使用 `sqrt` 后比较浮点数，可能出现精度误差导致相等的对角线被误判为不相等。  
  - 忘记在对角线相等时仍需比较面积，导致答案不符合“面积最大”要求。  
- **下次类似题的第一步**：先思考是否可以把涉及根号或分数的比较转化为**整数比较**（如平方、通分），再决定是否需要真正计算根号或分数。这样既能避免精度问题，又能让代码更简洁高效。