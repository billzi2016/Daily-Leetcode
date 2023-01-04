# #2078. 不同颜色的最远两座房子 / Two Furthest Houses With Different Colors

> 难度：简单 · 标签：Array、Greedy · [LeetCode 链接](https://leetcode.com/problems/two-furthest-houses-with-different-colors/)

---

## 题目（英文原版）

**Description**

There are n houses evenly lined up on the street, and each house is beautifully painted. You are given a 0-indexed integer array colors of length n, where colors[i] represents the color of the ith house.
Return the maximum distance between two houses with different colors.
The distance between the ith and jth houses is abs(i - j), where abs(x) is the absolute value of x.

**Examples**

**Example 1:**

```
Input: colors = [1,1,1,6,1,1,1]
Output: 3
Explanation: In the above image, color 1 is blue, and color 6 is red.
The furthest two houses with different colors are house 0 and house 3.
House 0 has color 1, and house 3 has color 6. The distance between them is abs(0 - 3) = 3.
Note that houses 3 and 6 can also produce the optimal answer.
```

**Example 2:**

```
Input: colors = [1,8,3,8,3]
Output: 4
Explanation: In the above image, color 1 is blue, color 8 is yellow, and color 3 is green.
The furthest two houses with different colors are house 0 and house 4.
House 0 has color 1, and house 4 has color 3. The distance between them is abs(0 - 4) = 4.
```

**Example 3:**

```
Input: colors = [0,1]
Output: 1
Explanation: The furthest two houses with different colors are house 0 and house 1.
House 0 has color 0, and house 1 has color 1. The distance between them is abs(0 - 1) = 1.
```

**Constraints**

- n == colors.length
- 2 <= n <= 100
- 0 <= colors[i] <= 100
- Test data are generated such that at least two houses have different colors.

---

## 题目（中文翻译）

给定一条街道上 **n** 栋等间距排列的房子，每栋房子都被涂上了颜色。你得到一个下标从 **0** 开始的整数数组 **colors**（array），长度为 **n**，其中 **colors[i]** 表示第 **i** 栋房子的颜色。  
返回颜色不同的两栋房子之间的最大距离。  
第 **i** 栋和第 **j** 栋房子之间的距离定义为 `abs(i - j)`，其中 `abs(x)` 为 **x** 的绝对值（absolute value）。

**示例 1**  
```text
Input: colors = [1,1,1,6,1,1,1]
Output: 3
```
**解释**：如上图所示，颜色 `1` 为蓝色，颜色 `6` 为红色。颜色不同的最远两栋房子是第 `0` 栋和第 `3` 栋。第 `0` 栋的颜色是 `1`，第 `3` 栋的颜色是 `6`，它们之间的距离为 `abs(0 - 3) = 3`。  
注意，第 `3` 栋和第 `6` 栋同样可以得到最优答案。

**示例 2**  
```text
Input: colors = [1,8,3,8,3]
Output: 4
```
**解释**：如上图所示，颜色 `1` 为蓝色，颜色 `8` 为黄色，颜色 `3` 为绿色。颜色不同的最远两栋房子是第 `0` 栋和第 `4` 栋。第 `0` 栋的颜色是 `1`，第 `4` 栋的颜色是 `3`，它们之间的距离为 `abs(0 - 4) = 4`。

**示例 3**  
```text
Input: colors = [0,1]
Output: 1
```
**解释**：颜色不同的最远两栋房子是第 `0` 栋和第 `1` 栋。第 `0` 栋的颜色是 `0`，第 `1` 栋的颜色是 `1`，它们之间的距离为 `abs(0 - 1) = 1`。

**约束条件**
- `n == colors.length`
- `2 <= n <= 100`
- `0 <= colors[i] <= 100`
- 测试数据保证至少存在两栋颜色不同的房子。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把所有可能的房子对全部列举一遍，逐个检查它们的颜色是否不同，若不同就计算距离 `abs(i-j)`，把最大的距离记下来。

- **使用的数据结构**：只需要原始的 `colors` 列表和两个整数变量 `max_dist`（记录当前最大的距离）以及 `n`（房子数量）。  
  - `colors` 就像一本排好序的街道地图，索引 `i` 表示第 `i` 栋房子的位置，`colors[i]` 是它的颜色。  
  - 暴力遍历相当于把每一栋房子当作“左手”去和它右边的每一栋房子当作“右手”配对，就像把所有可能的两个人配对聊天，找出颜色不同且最远的那一对。

- **为什么正确**：我们遍历了所有 `i < j` 的组合，没有遗漏任何可能的房子对。只要有一对颜色不同且距离最大，就一定会在遍历过程中被发现。

- **复杂度分析**  
  - 时间：外层循环 `i` 走 `n` 次，内层循环 `j` 最多走 `n-1`、`n-2` … 次，总次数约为 `n*(n-1)/2`，用大写的 **O** 表示就是 **O(n²)**。  
    - 大白话：如果有 100 栋房子，暴力会检查大约 5,000 对（因为 100*99/2=4950），随 `n` 增大，检查次数会呈二次方增长。
  - 空间：只用了常数个额外变量，**O(1)**（不随 `n` 增长）。

#### 代码（Python）

```python
from typing import List

def maxDistance_bruteforce(colors: List[int]) -> int:
    n = len(colors)
    max_dist = 0                     # 记录当前找到的最大距离

    # i 为左侧房子的下标，j 为右侧房子的下标（i < j）
    for i in range(n):
        for j in range(i + 1, n):
            # 只关心颜色不同的情况
            if colors[i] != colors[j]:
                dist = j - i        # 因为 j > i，abs(i-j) == j-i
                if dist > max_dist:
                    max_dist = dist  # 更新最大距离
    return max_dist
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 需要检查所有两两组合，随着房子数量的增多，耗时会快速增长。  
- **空间复杂度**：`O(1)` —— 只用了几个整数变量，几乎不占额外内存。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到 **瓶颈** 在于两层循环遍历所有组合，实际上我们并不需要遍历全部。观察题目：

> 要求的是「最远」的两栋颜色不同的房子，而「最远」一定涉及到 **左端** 或 **右端** 的房子。

具体来说：

1. 若左边第 0 栋房子（最左）颜色和某栋右侧房子颜色不同，那么这对的距离就是 `j - 0 = j`，随 `j` 越大距离越大。于是我们只需要找离左端最远、颜色不同的房子即可。
2. 同理，若右边最后一栋房子（最右）颜色和某栋左侧房子颜色不同，那么这对的距离就是 `n-1 - i`，随 `i` 越小距离越大。于是我们只需要找离右端最左、颜色不同的房子即可。

因此，只需要 **两次线性扫描**：

- 从左向右扫描，寻找第一个与 `colors[0]` 不同的房子位置 `right_diff`，计算距离 `right_diff - 0`。
- 从右向左扫描，寻找第一个与 `colors[n-1]` 不同的房子位置 `left_diff`，计算距离 `n-1 - left_diff`。

答案即为这两个距离的最大值。

> **为什么这样就能得到全局最优？**  
> 假设最远的不同颜色房子对是 `(i, j)`，且 `i < j`。如果 `i` 不是最左端 `0`，那么把左端 `0` 换成 `i`，距离会变小；但如果 `colors[0] != colors[j]`，则 `(0, j)` 的距离更大或相等，同理右端也成立。于是最远的合法对必然和左端或右端之一构成。

- **使用的数据结构**：仍然是原始列表 `colors`，以及两个整数变量 `right_diff`、`left_diff` 用来记录第一次出现颜色不同的位置。  
  - 把列表想象成一条直线，左端的房子是“起点”，我们从起点往右跑，第一次看到不同颜色就停下来记录；右端同理。

- **复杂度**  
  - 时间：只需要遍历一次（最坏情况下两次遍历，但每次都是 O(n)），所以 **O(n)**。  
  - 空间：只用了常数个变量，**O(1)**。

#### 代码（Python）

```python
from typing import List

def maxDistance_optimal(colors: List[int]) -> int:
    n = len(colors)
    # 1. 从左边找第一个颜色不同的房子
    right_diff = 0                # 默认值，实际一定会被更新（题目保证有不同颜色的房子）
    for j in range(n):
        if colors[j] != colors[0]:
            right_diff = j
            break                 # 找到第一个不同的就可以停止

    # 2. 从右边找第一个颜色不同的房子
    left_diff = n - 1
    for i in range(n - 1, -1, -1):
        if colors[i] != colors[-1]:
            left_diff = i
            break

    # 3. 计算两种可能的最大距离，取较大者
    dist1 = right_diff               # = right_diff - 0
    dist2 = (n - 1) - left_diff      # = (n-1) - left_diff
    return max(dist1, dist2)
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 只进行两次线性扫描，房子数量增加时，耗时几乎呈线性增长。与暴力解相比，速度提升了 **n** 倍（例如 n=100 时从 5,000 次比较降到 200 次左右）。
- **空间复杂度**：`O(1)` —— 只用了几个整数变量，几乎不占额外内存。

---

## 心得

- **核心技巧**：**从两端贪心**——在寻找“最远”这种距离类问题时，往往可以把注意力集中在数组的两端，因为极端距离必然涉及到端点。
- **适用的题型**  
  1. “最大距离”或“最远两点”类问题（如 LeetCode 1493. Longest Subarray of 1s After Deleting One Element）。  
  2. “首尾不同”或“端点约束”类题目（如 1650. Lowest Common Ancestor of a Binary Tree III 的线性扫描思路）。  
  3. “从两端逼近” 的双指针问题（如 1679. Max Number of K-Sum Pairs）。
- **一句话总结解题钥匙**：**最远的合法配对一定和左端或右端之一相连，只要找出第一次颜色不同的位置即可。**

---

## 反思

- **第一反应**：看到“最大距离”立刻想到枚举所有对（暴力），因为这样最安全、最直观。
- **最容易踩的坑**  
  - 忘记题目保证至少有两种颜色，导致在极端情况下（全部相同）没有找到 `right_diff`/`left_diff`，代码会报错。实际实现时可以在循环结束后检查是否仍未更新（但本题不必）。  
  - 边界条件：当不同颜色恰好出现在最左或最右时，`right_diff` 或 `left_diff` 可能等于 0 或 `n-1`，仍然要正确计算距离。  
- **下次遇到同类题**：第一步先思考“最远/最大”是否必然与数组端点有关，如果是，就直接尝试从两端线性扫描；如果不确定，再考虑暴力验证后再寻找优化点。