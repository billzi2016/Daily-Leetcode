# #1856. 最大子数组最小乘积 / Maximum Subarray Min-Product

> 难度：中等 · 标签：Array、Stack、Monotonic Stack、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/maximum-subarray-min-product/)

---

## 题目（英文原版）

**Description**

The min-product of an array is equal to the minimum value in the array multiplied by the array's sum.
Given an array of integers nums, return the maximum min-product of any non-empty subarray of nums. Since the answer may be large, return it modulo 109 + 7.
Note that the min-product should be maximized before performing the modulo operation. Testcases are generated such that the maximum min-product without modulo will fit in a 64-bit signed integer.
A subarray is a contiguous part of an array.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,2]
Output: 14
Explanation: The maximum min-product is achieved with the subarray [2,3,2] (minimum value is 2).
2 * (2+3+2) = 2 * 7 = 14.
```

**Example 2:**

```
Input: nums = [2,3,3,1,2]
Output: 18
Explanation: The maximum min-product is achieved with the subarray [3,3] (minimum value is 3).
3 * (3+3) = 3 * 6 = 18.
```

**Example 3:**

```
Input: nums = [3,1,5,6,4,2]
Output: 60
Explanation: The maximum min-product is achieved with the subarray [5,6,4] (minimum value is 4).
4 * (5+6+4) = 4 * 15 = 60.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 107

---

## 题目（中文翻译）

数组的最小乘积（min-product）定义为数组中的最小值乘以数组的所有元素之和。  
给定一个整数数组 `nums`，返回 `nums` 中任意 **非空** 子数组（subarray）的最大最小乘积（min-product）。由于答案可能很大，请返回其对 `10^9 + 7` 取模后的结果。  
**注意**：在进行模运算之前，需要先求出最大最小乘积（min-product）。题目保证在不取模的情况下，最大最小乘积（min-product）能够装入 64 位有符号整数。  
子数组（subarray）是数组中连续的一段。

## 示例

### 示例 1
> **输入**: `nums = [1,2,3,2]`  
> **输出**: `14`  
> **解释**: 最大最小乘积（min-product）由子数组 `[2,3,2]` 获得（最小值为 `2`）。  
> `2 * (2+3+2) = 2 * 7 = 14`.

### 示例 2
> **输入**: `nums = [2,3,3,1,2]`  
> **输出**: `18`  
> **解释**: 最大最小乘积（min-product）由子数组 `[3,3]` 获得（最小值为 `3`）。  
> `3 * (3+3) = 3 * 6 = 18`.

### 示例 3
> **输入**: `nums = [3,1,5,6,4,2]`  
> **输出**: `60`  
> **解释**: 最大最小乘积（min-product）由子数组 `[5,6,4]` 获得（最小值为 `4`）。  
> `4 * (5+6+4) = 4 * 15 = 60`.

## 约束条件

- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^7`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有可能的子数组都枚举一遍，求出它们的 **最小值** 与 **子数组之和**，再算出 `最小值 × 子数组之和`，取最大即可。

- **枚举子数组**：我们可以用两层循环，外层决定子数组的左端点 `l`，内层把右端点 `r` 从 `l` 向右移动，每次把新加入的元素累加到当前和 `sum`，并用 `min_val = min(min_val, nums[r])` 同时维护子数组的最小值。
- **为什么正确**：因为我们真的遍历了「所有」连续子段，任何合法的子数组都会在某一次 `(l, r)` 被检查到，算出的 `min_val * sum` 必然是该子数组的 min‑product。取最大自然得到答案。

> **类比**：想象你在一本字典里查每个词的出现位置。暴力解就像把字典的每一页都翻一遍，记录下每个词出现的所有页码——虽然能得到完整信息，但显然很慢。

#### 代码（Python）

```python
from typing import List

MOD = 10 ** 9 + 7

def maxMinProduct_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    ans = 0                     # 用来保存当前找到的最大 min‑product
    for left in range(n):       # 枚举子数组左端点
        cur_min = nums[left]    # 当前子数组的最小值
        cur_sum = 0             # 当前子数组的和
        for right in range(left, n):   # 扩展右端点
            cur_sum += nums[right]      # 累加新元素
            cur_min = min(cur_min, nums[right])  # 更新最小值
            ans = max(ans, cur_min * cur_sum)    # 取最大
    return ans % MOD
```

- 第 6 行的 `cur_min = nums[left]` 相当于把当前子数组的“最小值”先设为左端点的数，随后随右端点的移动不断取更小的值。
- 第 10 行的 `cur_sum += nums[right]` 就像在往购物车里继续加商品，求总价。
- 第 12 行 `cur_min * cur_sum` 正是题目要求的 **min‑product**。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  两层循环分别遍历 `n` 个左端点和最多 `n` 个右端点，最坏情况要检查约 `n·(n+1)/2` 个子数组。  
  用大白话说，若数组长度是 10⁴，暴力解大约要跑 10⁸ 次操作，已经超出常规 1 秒时限。

- **空间复杂度**：`O(1)`  
  只用了常数个额外变量（`cur_min`, `cur_sum`, `ans`），不随 `n` 增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **“每次都要重新遍历子数组来找最小值”**。如果我们能一次性知道，对于每个元素 `nums[i]`，它可以作为最小值的 **最长连续子数组** 是多少，那么只要算出这段子数组的和，就能直接得到 `nums[i] * (sum of that segment)`，不必再枚举所有子数组。

**关键观察**：  
- 对于固定的最小值 `x = nums[i]`，如果把子数组向左、右扩张，直到遇到比 `x` 更小的数为止，那么在这两个边界之间的所有子数组（只要包含 `i`）的最小值必然都是 `x`。因此，**以 `i` 为最小值的最大子数组** 就是：

```
左边界 = 最近的、在 i 左侧且 < nums[i] 的位置 + 1
右边界 = 最近的、在 i 右侧且 < nums[i] 的位置 - 1
```

- 这正是 **单调栈（Monotonic Stack）** 擅长的工作：一次遍历即可得到每个位置左右最近的更小元素。

**步骤概览**：

1. **前缀和** `pre[i]`（0‑based，`pre[0]=0`），用来在 O(1) 时间求任意区间 `[l, r]` 的和：`sum(l,r) = pre[r+1] - pre[l]`。前缀和相当于把每个位置之前所有数的“累计账本”，查询时只需两次查账本的差额。
2. **单调递增栈**（栈里保存数组下标，栈顶对应的数最小），从左到右遍历：
   - 当当前数 `nums[i]` **小于** 栈顶对应的数时，弹出栈顶 `mid`。弹出时，栈顶的左侧界限已经确定（栈中新的栈顶 `left`），右侧界限就是当前下标 `i`（因为 `i` 是第一个比 `mid` 小的数）。
   - 计算区间 `[left+1, i-1]` 的和，用 `pre` 快速得到，然后算 `nums[mid] * sum`，更新答案。
   - 继续弹出，直到栈顶不再大于 `nums[i]`。
   - 最后把 `i` 入栈。
3. **遍历结束后**，栈里剩下的元素右侧没有更小的数，右边界是数组末尾 `n-1`。再统一弹出一次完成剩余区间的计算。

> **类比**：把数组看成一排房子，房子的高度就是 `nums[i]`。我们要找每栋房子能“看到”多远（左/右），直到被更矮的房子挡住。单调栈就像一支“监视员”，按高度递增站队，遇到更矮的房子时，前面的监视员就可以确定自己的视野范围。

#### 代码（Python）

```python
from typing import List

MOD = 10 ** 9 + 7

def maxMinProduct(nums: List[int]) -> int:
    n = len(nums)

    # 1. 前缀和，pre[i] 表示 nums[0..i-1] 的累加和，pre[0] = 0
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] + nums[i]

    # 2. 单调递增栈，栈中只保存下标
    stack = []          # 保存「还没有找到右边界」的下标
    ans = 0

    for i, val in enumerate(nums):
        # 当当前值比栈顶对应的值小，说明栈顶的右边界找到了
        while stack and nums[stack[-1]] > val:
            mid = stack.pop()               # 以 mid 为最小值的子数组即将确定
            left = stack[-1] if stack else -1   # 左边界的下标（比 mid 小的最近的下标），若栈空则为 -1
            # 子数组区间是 (left, i) 之间，左闭右开 => [left+1, i-1]
            total = pre[i] - pre[left + 1]   # 区间和
            ans = max(ans, nums[mid] * total)
        stack.append(i)

    # 处理栈中剩余元素，它们的右边界是数组末尾 n-1
    while stack:
        mid = stack.pop()
        left = stack[-1] if stack else -1
        total = pre[n] - pre[left + 1]       # 区间和，右边界是 n-1
        ans = max(ans, nums[mid] * total)

    return ans % MOD
```

**关键行解释**：

- 第 7‑10 行构造前缀和：`pre[i+1]` 保存到当前位置为止的总和，类似“累计账本”。
- 第 14‑20 行的 `while` 循环是单调栈的核心：当出现更小的数时，弹出栈顶并立即算出以它为最小值的最大子数组的和与乘积。
- 第 17 行 `left = stack[-1] if stack else -1`：如果弹出后栈仍有元素，栈顶就是左边最近更小的下标；若栈空，说明左边没有更小的数，左边界设为 `-1`（即从最左侧开始）。
- 第 19 行 `total = pre[i] - pre[left + 1]`：利用前缀和快速得到子数组 `[left+1, i-1]` 的和。
- 第 24‑29 行处理残留在栈中的元素，它们的右边界是数组末尾 `n-1`。

#### 复杂度

- **时间复杂度**：`O(n)`  
  每个下标至多被压入栈一次、弹出一次，整个过程线性扫描 `nums`，前缀和的构造也是线性。相比暴力的 `O(n²)`，速度提升了 **n 倍**。

- **空间复杂度**：`O(n)`  
  需要额外的前缀和数组 `pre`（大小 `n+1`）和单调栈（最坏情况下会保存全部 `n` 个下标），都是线性空间。相对于输入规模，这已经是最优的。

---

## 心得

- **核心技巧**：**单调栈 + 前缀和**。单调栈帮助我们一次遍历找出每个元素左右最近的更小值，从而得到它能够支配的最长子数组；前缀和让区间求和降到 O(1)。
- **适用的题型**：
  1. **最大矩形面积**（LeetCode 84）——同样利用单调栈找左右更小柱子。
  2. **柱状图中最大的矩形**（LeetCode 1856）——与本题几乎等价，只是把 “最小值 × 和” 换成 “高度 × 宽度”。
  3. **子数组的最小值之和**（LeetCode 907）——同理，需要统计每个元素作为最小值出现的子数组个数。
- **一句话总结**：  
  *把每个元素当作“最小值”，用单调栈一次性确定它能“统治”的最大连续区间，再用前缀和算区间和，乘积最大即为答案。*

---

## 反思

- **第一反应**：直接枚举所有子数组（暴力）——想到最直接的完整搜索，却忽视了时间限制。
- **最容易踩的坑**：
  - **边界处理**：左边界为 `-1`、右边界为 `n` 时的前缀和差值容易写错，记得 `pre` 是 **左闭右开**。
  - **相等元素的处理**：栈里使用 “>” 而不是 “>=”，这样相等的元素会保持在栈中，防止重复计算区间，确保每个子数组只被计一次。
  - **取模时机**：题目要求先求最大值再取模，不能在中间每次都 `% MOD`，否则可能导致错误的比较。
- **下次类似题的第一步**：  
  “先思考：如果把某个位置的数固定为子数组的最小值，它能覆盖多大的连续区间？”——这一步往往直接指向单调栈的使用。