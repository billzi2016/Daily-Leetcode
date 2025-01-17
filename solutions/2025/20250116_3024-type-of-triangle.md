# #3024. 三角形类型 / Type of Triangle

> 难度：简单 · 标签：Array、Math、Sorting · [LeetCode 链接](https://leetcode.com/problems/type-of-triangle/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums of size 3 which can form the sides of a triangle.
Return a string representing the type of triangle that can be formed or "none" if it cannot form a triangle.

**Examples**

**Example 1:**

```
Input: nums = [3,3,3]
Output: "equilateral"
Explanation: Since all the sides are of equal length, therefore, it will form an equilateral triangle.
```

**Example 2:**

```
Input: nums = [3,4,5]
Output: "scalene"
Explanation: 
nums[0] + nums[1] = 3 + 4 = 7, which is greater than nums[2] = 5.
nums[0] + nums[2] = 3 + 5 = 8, which is greater than nums[1] = 4.
nums[1] + nums[2] = 4 + 5 = 9, which is greater than nums[0] = 3. 
Since the sum of the two sides is greater than the third side for all three cases, therefore, it can form a triangle.
As all the sides are of different lengths, it will form a scalene triangle.
```

**Constraints**

- nums.length == 3
- 1 <= nums[i] <= 100

---

## 题目（中文翻译）

你将得到一个下标从 **0** 开始、长度为 **3** 的整数数组 `nums`，其中的三个整数可以视为三角形的三条边。返回一个字符串，表示能够形成的三角形类型；如果这三条边 **无法构成三角形**，则返回 `"none"`。

**示例 1**  
```
Input: nums = [3,3,3]
Output: "equilateral"
Explanation: 所有三条边长度相等，构成等边三角形（equilateral）。
```

**示例 2**  
```
Input: nums = [3,4,5]
Output: "scalene"
Explanation: 
nums[0] + nums[1] = 3 + 4 = 7 > nums[2] = 5  
nums[0] + nums[2] = 3 + 5 = 8 > nums[1] = 4  
nums[1] + nums[2] = 4 + 5 = 9 > nums[0] = 3  
三条不等式均成立，说明可以构成三角形。且三条边长度各不相同，构成不等边三角形（scalene）。
```

**约束条件**
- `nums.length == 3`
- `1 <= nums[i] <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题的要求非常直观：

1. **先判断能否组成三角形**。  
   三角形的“成立条件”是：任意两条边的长度之和必须**严格大于**第三条边。可以把这条规则想象成“两个小木棒拼在一起，要比第三根木棒长”。我们只需要检查三次：

   - `a + b > c`
   - `a + c > b`
   - `b + c > a`

2. **如果可以组成三角形，再判断是哪种类型**。  
   - **等边三角形**：三条边长度全部相同。  
   - **等腰三角形**：恰好有两条边相等（但不是全部相等）。  
   - **不等边三角形**（即**锐角三角形**在这里叫 `scalene`）：三条边全不相等。

   判断方式可以用**集合（set）**来实现：把三条边放进集合，集合的大小就是不同长度的个数。  
   - 大小为 `1` → 等边  
   - 大小为 `2` → 等腰  
   - 大小为 `3` → 不等边  

   集合就像一本**字典**，每个不同的单词只出现一次，帮助我们快速统计不同的“词”。  

这就是最直接的做法：一步一步把题目要求的每条规则都写出来。

#### 代码（Python）

```python
from typing import List

def triangleType(nums: List[int]) -> str:
    a, b, c = nums          # 把三个边的长度分别取出来，方便后面写条件

    # 1. 判断是否能组成三角形
    if not (a + b > c and a + c > b and b + c > a):
        return "none"       # 任意一条不满足，都不是三角形

    # 2. 统计不同的边长数量（集合会自动去重）
    uniq = len(set(nums))   # set(nums) 把相同的边长合并，只剩下不同的

    if uniq == 1:
        return "equilateral"   # 全部相等 → 等边
    if uniq == 2:
        return "isosceles"      # 恰好两条相等 → 等腰
    return "scalene"            # 全部不相等 → 不等边
```

#### 复杂度

- **时间复杂度**：`O(1)`  
  只做了常数次的加法、比较和集合创建，和数组长度（固定为 3）无关。  
  用大白话说，就是“不管输入多大，跑的时间基本不变”。

- **空间复杂度**：`O(1)`  
  只用了几个整数变量和一个最多装 3 个元素的集合，所占空间是常数级别的。

---

### 2. 最优解

#### 思路  

暴力解已经是 **最优** 的时间复杂度（`O(1)`），但我们可以把代码写得更简洁、更易读，尤其是利用**排序**来统一判断“三角形成立条件”。

1. **先把三条边从小到大排好序**。  
   排序后，记最短的两条边为 `x`、`y`，最长的为 `z`。此时只需要检查 **`x + y > z`** 一条不等式就足够了，因为如果最短两条的和已经大于最长的，其他两条（`x + z`、`y + z`）自然也会更大。  

   排序的过程类似于把“三根木棒”按长度排队，最短的站前面，最长的站后面，检查前两根的长度之和是否能“跨过”最后一根。

2. **判断三角形类型**  
   排序后，边长的相等关系仍然可以用集合的大小来判断，或者直接比较相邻元素：

   - `x == y == z` → 等边  
   - `x == y` 或 `y == z` → 等腰（注意排除全部相等的情况）  
   - 否则 → 不等边  

   这里不必再用集合，直接比较更省一点空间。

#### 代码（Python）

```python
from typing import List

def triangleType(nums: List[int]) -> str:
    # 1. 把三条边从小到大排好序
    a, b, c = sorted(nums)   # sorted 返回新的列表，a <= b <= c

    # 2. 判断是否能组成三角形：只需检查最短两边之和是否大于最长边
    if a + b <= c:            # 如果不大于，就不可能是三角形
        return "none"

    # 3. 根据相等情况返回对应的类型
    if a == c:                # a == b == c，因为已经排好序，a==c 即全相等
        return "equilateral"
    if a == b or b == c:      # 有两条相等（但不全相等），就是等腰
        return "isosceles"
    return "scalene"          # 没有任何相等的边，就是不等边
```

#### 复杂度

- **时间复杂度**：`O(1)`（严格来说是 `O(3 log 3)`，但因为数组只有 3 个元素，排序的代价可以视作常数）  
  与暴力解相比，唯一的额外工作是一次排序，但对 3 个数来说几乎可以忽略不计。

- **空间复杂度**：`O(1)`  
  只用了几个变量，`sorted` 会生成一个长度为 3 的新列表，仍然是常数大小。

---

## 心得

- **核心技巧**：  
  1. **三角形判定** – 只要任意两边之和大于第三边。  
  2. **利用集合或排序** 来快速统计不同的边长数量，进而判断等边、等腰或不等边。

- **适用的题型**（类似思路）  
  - 判断四边形是否为矩形/正方形（先检查对角线相等，再判断边长相等）。  
  - 判断数列是否为等差/等比数列（排序后检查相邻差值/比值是否相同）。  
  - “合法的三角形”系列的变体，如 LeetCode 1799（最大数对的三角形数目）等。

- **一句话总结解题钥匙**：  
  **“先把条件化简到最少的几条判断，再用去重/比较快速定位不同的情况”。**

---

## 反思

- **第一反应**：  
  看到“能否组成三角形”和“哪种类型”，立刻想到“三角形不等式”和“比较边长是否相等”。于是直接写出三个不等式检查和集合计数的代码。

- **最容易踩的坑**：  
  - **忘记“严格大于”**：如果写成 `>=`，会把退化的线段误判为三角形。  
  - **边界值**：题目保证每条边至少为 1，故不必担心 0 或负数导致的特殊情况。  
  - **等腰的判定**：等腰必须排除等边的情况，否则会把等边误报为等腰。

- **下次遇到同类题的第一步**：  
  **先把所有“必须同时满足”的约束条件写出来，找出可以合并或简化的部分（如排序后只剩一条不等式），再考虑如何用最少的比较或去重手段区分不同的结果。**