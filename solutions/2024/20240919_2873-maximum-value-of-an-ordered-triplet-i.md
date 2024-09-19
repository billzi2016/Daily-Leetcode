# #2873. **有序三元组的最大值 I** / Maximum Value of an Ordered Triplet I

> 难度：简单 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/maximum-value-of-an-ordered-triplet-i/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums.
Return the maximum value over all triplets of indices (i, j, k) such that i < j < k. If all such triplets have a negative value, return 0.
The value of a triplet of indices (i, j, k) is equal to (nums[i] - nums[j]) * nums[k].

**Examples**

**Example 1:**

```
Input: nums = [12,6,1,2,7]
Output: 77
Explanation: The value of the triplet (0, 2, 4) is (nums[0] - nums[2]) * nums[4] = 77.
It can be shown that there are no ordered triplets of indices with a value greater than 77.
```

**Example 2:**

```
Input: nums = [1,10,3,4,19]
Output: 133
Explanation: The value of the triplet (1, 2, 4) is (nums[1] - nums[2]) * nums[4] = 133.
It can be shown that there are no ordered triplets of indices with a value greater than 133.
```

**Example 3:**

```
Input: nums = [1,2,3]
Output: 0
Explanation: The only ordered triplet of indices (0, 1, 2) has a negative value of (nums[0] - nums[1]) * nums[2] = -3. Hence, the answer would be 0.
```

**Constraints**

- 3 <= nums.length <= 100
- 1 <= nums[i] <= 106

---

## 题目（中文翻译）

给定一个下标从 0 开始的整数数组 `nums`（integer array）。  
返回所有满足 `i < j < k` 的索引三元组 `(i, j, k)` 中的最大值。如果所有此类三元组的值均为负数，则返回 `0`。  

索引三元组 `(i, j, k)` 的值定义为  
\[
(nums[i] - nums[j]) \times nums[k]
\]

**示例 1**  
```
Input: nums = [12,6,1,2,7]
Output: 77
```
**解释**：三元组 `(0, 2, 4)` 的值为 `(nums[0] - nums[2]) * nums[4] = 77`。可以证明不存在值大于 77 的有序三元组。

**示例 2**  
```
Input: nums = [1,10,3,4,19]
Output: 133
```
**解释**：三元组 `(1, 2, 4)` 的值为 `(nums[1] - nums[2]) * nums[4] = 133`。可以证明不存在值大于 133 的有序三元组。

**示例 3**  
```
Input: nums = [1,2,3]
Output: 0
```
**解释**：唯一的有序三元组 `(0, 1, 2)` 的值为 `(nums[0] - nums[1]) * nums[2] = -3`，为负数。因此答案为 `0`。

**约束条件**  
- `3 <= nums.length <= 100`  
- `1 <= nums[i] <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有可能的三元组** 都枚举一遍，计算它们的价值 `(nums[i] - nums[j]) * nums[k]`，然后取最大值。  

- **数据结构**：只需要一个普通的 Python 列表 `nums`。  
- **生活化类比**：把数组想成一排排编号的盒子，暴力解相当于让小朋友把每个盒子当作起点 `i`，再往后挑一个盒子当作中点 `j`，再挑一个更后面的盒子当作终点 `k`，把这三个盒子里的数字套进公式里算一次。把所有算出来的结果放进“成绩单”，最后挑最高分。  

**为什么一定对**：题目要求所有满足 `i < j < k` 的三元组，枚举三层循环正好把这些组合全部遍历到了，所以不会漏掉任何可能的答案。

**时间/空间复杂度**：  
- **时间**：外层循环跑 `n` 次，第二层循环最多跑 `n` 次，最里层同理，整体是 `n × n × n = n³`，即 **O(n³)**。  
  大白话：如果数组长度是 10，暴力解大约要算 1 000 次；长度是 100，就要算 1 000 000 次，明显会慢。  
- **空间**：只用了常数个额外变量，**O(1)**。

#### 代码（Python）

```python
from typing import List

def maximumTripletValue_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    best = 0                         # 记录最大的正价值，默认 0
    # i 为最左边的下标
    for i in range(n - 2):           # 至少要留出两个位置给 j、k
        # j 为中间的下标
        for j in range(i + 1, n - 1):
            # k 为最右边的下标
            for k in range(j + 1, n):
                value = (nums[i] - nums[j]) * nums[k]
                if value > best:    # 只关心更大的正数
                    best = value
    return best
```

#### 复杂度  

- **时间复杂度**：O(n³) — 需要三层循环遍历所有三元组，随着 `n` 增大，运算次数呈立方增长。  
- **空间复杂度**：O(1) — 只用了几个整数变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

从暴力解出发，我们看到 **瓶颈** 在于三层循环，尤其是最里面的 `k` 循环，每一次都在重复已经算过的东西。  
要想加速，需要 **提前把可以重复使用的子结果保存下来**，这样在遍历 `k` 时就不必再枚举所有 `i、j`。

观察公式 `(nums[i] - nums[j]) * nums[k]`，对于固定的 `k`，只有 `(nums[i] - nums[j])` 的最大值会影响最终答案。  
而 `(nums[i] - nums[j])` 只涉及 `i` 和 `j`（且 `i < j`），我们可以把它拆成两步：

1. **左侧最大值** `max_left[i]`：在位置 `i` 之前（包括 `i` 本身）出现的最大元素 `max(nums[0..i])`。  
   - 类比：把数组看成一本字典，`max_left[i]` 就是“从第一页到第 `i` 页中，字母最大的那一页”。  
2. 对每个中间位置 `j`，**最好的差值** 为 `max_left[j-1] - nums[j]`（因为 `i` 必须在 `j` 左边）。  
   把这些差值在遍历时取最大，记作 `best_diff_up_to_j`。

接下来，只要把 `best_diff_up_to_j` 与后面的 `nums[k]` 相乘，就能得到以 `k` 为最右端的最佳价值。  

实现细节：

- 第一次遍历（从左到右）计算 `best_diff_up_to_j`，并把它存进数组 `diff[j]`。  
- 第二次遍历（从左到右）对每个 `k`，使用 `diff[k-1]`（即所有 `j < k` 的最佳差值）乘以 `nums[k]`，更新答案。  

整个过程只用了 **两次线性遍历**，时间是 **O(n)**，额外空间可以用一个长度为 `n` 的数组（也可以把 `best_diff` 和 `max_left` 合并成常数个变量实现 O(1) 空间）。

> **核心技巧**：**前缀最大 + 前缀最佳差值**，把三层循环压缩成两层甚至一层。

#### 代码（Python）

```python
from typing import List

def maximumTripletValue(nums: List[int]) -> int:
    n = len(nums)
    if n < 3:
        return 0

    # 第一步：计算到每个位置 j 为止，左侧最大值减去 nums[j] 的最大差值
    # diff[j] 表示在 i < j 的所有组合里，(nums[i] - nums[j]) 的最大值
    diff = [float('-inf')] * n          # 初始化为负无穷
    max_left = nums[0]                  # 到当前为止的最大元素
    for j in range(1, n - 1):           # j 只能到 n-2，因为后面还要留一个 k
        # 计算以当前 j 为中间点的差值，并与之前的最佳差值比较
        diff[j] = max(diff[j - 1], max_left - nums[j])
        # 更新左侧最大值，为后面的 j 做准备
        max_left = max(max_left, nums[j])

    # 第二步：遍历每个可能的 k，使用 diff[k-1]（所有 j < k 的最佳差值）计算价值
    ans = 0
    for k in range(2, n):
        if diff[k - 1] > 0:                     # 只有正的差值才可能让乘积变正
            ans = max(ans, diff[k - 1] * nums[k])

    return ans
```

> **代码注释** 已经用中文解释了每一行的作用，直接复制运行即可。

#### 复杂度  

- **时间复杂度**：O(n) — 只遍历了两遍数组，随着 `n` 增大，运算次数线性增长。相比暴力的 O(n³)，快了很多。  
- **空间复杂度**：O(n)（如果使用 `diff` 数组）或 O(1)（只保留一个变量 `best_diff`）。这里展示的实现是 O(n) 版，易于理解；如果要进一步压缩空间，只需要把 `diff` 换成一个滚动变量即可。

---

## 心得

- **核心技巧**：利用**前缀最大**和**前缀最佳差值**把三元组的枚举压缩到线性时间。  
- **适用场景**：  
  1. 需要在数组中找形如 `A[i] - B[j]`（`i < j`）的最大差值的题目（如 *Maximum Difference Between Two Elements*）。  
  2. 需要在三元组 `(i, j, k)` 中，左侧两项只涉及 `i、j`，右侧只涉及 `k` 的乘积/和类问题（如 *Maximum Value of an Ordered Triplet II*、*Maximum Profit of Stock Trading*）。  
- **一句话总结**：**把“左边的最好”提前算好，后面只要乘以右边的元素即可**。

---

## 反思

- **第一反应**：直接写三层循环暴力枚举，因为最直接、最不容易出错。  
- **最容易踩的坑**：  
  - 忘记 `i < j < k` 的顺序限制，导致使用了错误的前缀信息。  
  - 当 `max_left - nums[j]` 为负时仍然更新 `diff`，会把负差值当作候选，进而在乘以 `nums[k]` 时产生负的答案，需要在最终比较时只保留正的结果（或直接在更新 `ans` 前判断 `diff > 0`）。  
  - 边界条件：数组长度恰好为 3 时，只能算唯一的三元组，需要确保循环下标不越界。  
- **下次第一步**：先思考 **“能否把左侧的最优信息提前保存”**，如果可以，就把问题转化为前缀/后缀的动态更新，而不是直接枚举所有组合。这样往往能把指数级的暴力下降到线性或线性对数级。