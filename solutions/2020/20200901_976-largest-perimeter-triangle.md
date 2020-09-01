# #976. 最大周长三角形 / Largest Perimeter Triangle

> 难度：简单 · 标签：Array、Math、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/largest-perimeter-triangle/)

---

## 题目（英文原版）

**Description**

Given an integer array nums, return the largest perimeter of a triangle with a non-zero area, formed from three of these lengths. If it is impossible to form any triangle of a non-zero area, return 0.

**Examples**

**Example 1:**

```
Input: nums = [2,1,2]
Output: 5
Explanation: You can form a triangle with three side lengths: 1, 2, and 2.
```

**Example 2:**

```
Input: nums = [1,2,1,10]
Output: 0
Explanation: 
You cannot use the side lengths 1, 1, and 2 to form a triangle.
You cannot use the side lengths 1, 1, and 10 to form a triangle.
You cannot use the side lengths 1, 2, and 10 to form a triangle.
As we cannot use any three side lengths to form a triangle of non-zero area, we return 0.
```

**Constraints**

- 3 <= nums.length <= 104
- 1 <= nums[i] <= 106

---

## 题目（中文翻译）

给定一个整数数组 `nums`，返回由其中任意三个长度组成、面积非零的三角形的最大周长。如果无法构成任何面积非零的三角形，返回 `0`。

## 示例

### 示例 1
**输入**  
`nums = [2,1,2]`  

**输出**  
`5`  

**解释**  
你可以使用边长为 `1、2、2` 的三条边构成一个三角形，其周长为 `5`。

### 示例 2
**输入**  
`nums = [1,2,1,10]`  

**输出**  
`0`  

**解释**  
- 使用边长 `1、1、2` 不能构成三角形。  
- 使用边长 `1、1、10` 不能构成三角形。  
- 使用边长 `1、2、10` 也不能构成三角形。  

由于任意三条边都无法组成面积非零的三角形，返回 `0`。

## 约束条件
- `3 <= nums.length <= 10^4`
- `1 <= nums[i] <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的三条边都枚举一遍**，判断它们能否构成三角形，能的话算出周长，取最大值。  
- **枚举**：用三层循环，分别选取下标 `i < j < k` 的三个元素，这相当于“从一堆棍子里挑三根”。  
- **三角形判定**：三条边 `a, b, c` 能组成面积大于 0 的三角形，需要满足 **任意两边之和大于第三边**，最常用的写法是把三条边先排序成 `a ≤ b ≤ c`，只要 `a + b > c` 即可（因为 `a + c > b`、`b + c > a` 必然成立）。  
- **记录最大周长**：如果能构成三角形，就计算 `a + b + c`，和当前的最大值比较，保存更大的。

> **类比**：把数组看成一本字典，想要找出“三个词能拼成一句有意义的话”。暴力做法就是把每三个词都拿出来尝试一次，肯定能找到答案，但时间会很长。

这种方法一定能得到正确答案，因为它**遍历了所有可能的组合**，不遗漏任何一种情况。

#### 代码（Python）

```python
from typing import List

def largestPerimeter_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    max_perimeter = 0                     # 记录目前找到的最大周长
    # 三层循环枚举所有 i < j < k
    for i in range(n - 2):
        for j in range(i + 1, n - 1):
            for k in range(j + 1, n):
                a, b, c = nums[i], nums[j], nums[k]
                # 为了方便判三角形，先把三条边从小到大排序
                x, y, z = sorted([a, b, c])
                # 判定：最短两边之和要大于最长边
                if x + y > z:
                    perimeter = x + y + z
                    if perimeter > max_perimeter:
                        max_perimeter = perimeter
    return max_perimeter
```

#### 复杂度

- **时间复杂度**：`O(n³)`  
  解释：三层循环分别遍历 `n`、`n-1`、`n-2` 次，数量级约等于 `n³`。如果 `n = 1000`，大约要执行 10⁹ 次操作，明显太慢。

- **空间复杂度**：`O(1)`  
  解释：只用了几个常数级的变量，不随 `n` 增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**重复检查大量不可能的组合**。实际上，只要把边长**从大到小排序**，就可以用**贪心**一次遍历找出答案。

**关键观察**  
- 若把数组降序排列为 `a₁ ≥ a₂ ≥ … ≥ a_n`，只要找到相邻的三条边 `a_i, a_{i+1}, a_{i+2}` 满足 `a_{i+1} + a_{i+2} > a_i`，这三个数就能组成三角形，并且它们的周长是**最大的**。  
- 为什么只看相邻三条？因为 `a_i` 是当前最大的边，若它已经大于后面两条之和（`a_{i+1}+a_{i+2}`），那么更小的 `a_{i+3}`、`a_{i+4}` … 与 `a_i` 组合肯定更不可能满足 `a_{j}+a_{k} > a_i`（因为后面的两条边只会更小），所以只需要继续往后移动窗口。

**算法步骤**  

1. **排序**：把 `nums` 按降序排列（大 → 小）。排序相当于把所有棍子从最长到最短排好队，方便一次检查。  
2. **遍历**：从头到倒数第三个位置，取 `i, i+1, i+2` 三根棍子。  
   - 判断 `nums[i+1] + nums[i+2] > nums[i]`。  
   - 若成立，直接返回这三条边的和 `nums[i] + nums[i+1] + nums[i+2]`，因为我们已经保证这是最大的可能周长。  
3. 若遍历结束仍未找到满足条件的三条边，说明 **任意三条都不能构成三角形**，返回 `0`。

> **类比**：把棍子排成从长到短的队列，先让最长的棍子和后面两根最接近它长度的棍子尝试配对。如果配对成功，已经是最好的组合了；如果不行，说明这根最长的棍子根本没法用，只好把它踢出队列，继续让第二长的棍子尝试。

#### 代码（Python）

```python
from typing import List

def largestPerimeter(nums: List[int]) -> int:
    # 1. 降序排序：最大边会排在最前面，后面的两条边尽可能大
    nums.sort(reverse=True)               # sort 相当于把字典里所有单词按字母倒序排好
    # 2. 只需要一次线性扫描
    for i in range(len(nums) - 2):
        a, b, c = nums[i], nums[i+1], nums[i+2]
        # 判定：两条较短的边之和要大于最长的边
        if b + c > a:
            return a + b + c               # 找到的就是最大周长，直接返回
    # 3. 没有任何合法三角形
    return 0
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  解释：排序是最耗时的步骤，时间为 `n log n`（比如 `n = 10⁴` 时大约几万次比较），遍历只需要 `O(n)`，整体受排序支配。相比暴力的 `O(n³)`，快了很多。

- **空间复杂度**：`O(1)`（如果使用原地排序）  
  解释：除了输入数组本身和少量临时变量，额外空间不随 `n` 增长。Python 的 `list.sort` 是原地排序。

---

## 心得

- **核心技巧**：**贪心 + 排序**。先把数据排好序，再利用“局部最优即全局最优”的性质一次遍历找答案。
- **适用的题型**  
  1. **三数之和最大且满足约束**（如本题、**Maximum Length of Pair Chain**）  
  2. **区间调度类贪心**（如 **Non-overlapping Intervals**）  
  3. **背包类的“先大后小”贪心**（如 **Boats to Save People**）
- **一句话总结解题钥匙**：**把问题转化为“在有序序列中找第一个满足条件的相邻窗口”。**

---

## 反思

- **第一反应**：看到“三条边要能组成三角形”，立刻想到“三角形不等式”，于是想到暴力枚举所有三元组。
- **最容易踩的坑**  
  - 忽视 **非零面积** 的要求，错误地接受 `a + b == c`（此时三点共线，面积为 0）。必须使用严格的大于号 `>`。  
  - 边界情况：数组长度恰好为 3，或者所有数都很小，导致没有合法三角形，需要返回 `0`。  
- **下次遇到同类题**：**先把数据排序**，思考“最大的元素能否和紧随其后的两个元素配合”，如果不行就把它丢掉，继续往后检查。这样可以在 `O(n log n)` 内得到最优解。