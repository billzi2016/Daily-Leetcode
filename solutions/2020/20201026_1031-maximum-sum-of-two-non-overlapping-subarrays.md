# #1031. 最大和的两个不重叠子数组 / Maximum Sum of Two Non-Overlapping Subarrays

> 难度：中等 · 标签：Array、Dynamic Programming、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/maximum-sum-of-two-non-overlapping-subarrays/)

---

## 题目（英文原版）

**Description**

Given an integer array nums and two integers firstLen and secondLen, return the maximum sum of elements in two non-overlapping subarrays with lengths firstLen and secondLen.
The array with length firstLen could occur before or after the array with length secondLen, but they have to be non-overlapping.
A subarray is a contiguous part of an array.

**Examples**

**Example 1:**

```
Input: nums = [0,6,5,2,2,5,1,9,4], firstLen = 1, secondLen = 2
Output: 20
Explanation: One choice of subarrays is [9] with length 1, and [6,5] with length 2.
```

**Example 2:**

```
Input: nums = [3,8,1,3,2,1,8,9,0], firstLen = 3, secondLen = 2
Output: 29
Explanation: One choice of subarrays is [3,8,1] with length 3, and [8,9] with length 2.
```

**Example 3:**

```
Input: nums = [2,1,5,6,0,9,5,0,3,8], firstLen = 4, secondLen = 3
Output: 31
Explanation: One choice of subarrays is [5,6,0,9] with length 4, and [0,3,8] with length 3.
```

**Constraints**

- 1 <= firstLen, secondLen <= 1000
- 2 <= firstLen + secondLen <= 1000
- firstLen + secondLen <= nums.length <= 1000
- 0 <= nums[i] <= 1000

---

## 题目（中文翻译）

给定一个整数数组 `nums` 和两个整数 `firstLen`、`secondLen`，返回长度分别为 `firstLen` 和 `secondLen` 的两个不重叠子数组（subarray）中的元素和的最大值。  
长度为 `firstLen` 的子数组可以出现在长度为 `secondLen` 的子数组之前，也可以出现在其之后，但二者必须不重叠。  
子数组（subarray）是数组中连续的一段。

**示例 1**  
**示例 2**  
**示例 3**

## 示例

### 示例 1
**输入**  
`nums = [0,6,5,2,2,5,1,9,4]`, `firstLen = 1`, `secondLen = 2`  
**输出**  
`20`  
**解释**  
一种选择是长度为 1 的子数组 `[9]`，以及长度为 2 的子数组 `[6,5]`，它们的和为 9 + 6 + 5 = 20，且不重叠。

### 示例 2
**输入**  
`nums = [3,8,1,3,2,1,8,9,0]`, `firstLen = 3`, `secondLen = 2`  
**输出**  
`29`  
**解释**  
一种选择是长度为 3 的子数组 `[3,8,1]`，以及长度为 2 的子数组 `[8,9]`，它们的和为 (3+8+1) + (8+9) = 29，且不重叠。

### 示例 3
**输入**  
`nums = [2,1,5,6,0,9,5,0,3,8]`, `firstLen = 4`, `secondLen = 3`  
**输出**  
`31`  
**解释**  
一种选择是长度为 4 的子数组 `[5,6,0,9]`，以及长度为 3 的子数组 `[0,3,8]`，它们的和为 (5+6+0+9) + (0+3+8) = 31，且不重叠。

## 约束条件
- `1 <= firstLen, secondLen <= 1000`
- `2 <= firstLen + secondLen <= 1000`
- `firstLen + secondLen <= nums.length <= 1000`
- `0 <= nums[i] <= 1000`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把所有可能的 **长度为 `firstLen` 的子数组** 与 **长度为 `secondLen` 的子数组** 都枚举一遍，挑出不重叠且和最大的那对。  

- **子数组**：在数组里连续的一段，就像把一根绳子直接截成两段，不能出现交叉。  
- **前缀和**：为了快速算任意子数组的和，我们先算一个“累计总和”数组 `pre`，`pre[i]` 表示 `nums[0..i-1]` 的和。这样任意子数组 `[l, r]`（左闭右闭）的和只需要 `pre[r+1] - pre[l]`，相当于在字典里查“从第 l 页到第 r 页的总字数”，时间 O(1)。  

暴力解的正确性很容易解释：我们把**所有合法组合**都检查了一遍，必然能找到最大和。  

**时间复杂度**：  
- 外层循环遍历 `firstLen` 子数组的起始位置，大约 `n` 次。  
- 内层循环遍历 `secondLen` 子数组的起始位置，同样是 `n` 次。  
- 每次检查只用 O(1)（前缀和），所以总共是 `O(n·n) = O(n²)`。  
  - “O(n²)” 可以想象成 **n 行 n 列的棋盘**，我们要遍历每一个格子。  

**空间复杂度**：  
- 需要存前缀和数组 `pre`，长度为 `n+1`，所以是 `O(n)`。  
- 其它变量都是常数，合计 `O(n)`。

#### 代码（Python）

```python
from typing import List

def maxSumTwoNoOverlap_bruteforce(nums: List[int], firstLen: int, secondLen: int) -> int:
    n = len(nums)

    # 1️⃣ 计算前缀和，pre[i] 为前 i 个元素的和（不含 nums[i] 本身）
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] + nums[i]          # 累计求和

    # 2️⃣ 暴力遍历所有合法的两段子数组
    ans = 0
    for i in range(n - firstLen + 1):          # 第一个子数组的左端点 i
        sum1 = pre[i + firstLen] - pre[i]      # 长度为 firstLen 的子数组和

        # 第二段子数组只能在 i 的左侧或右侧，且不能重叠
        # 右侧
        for j in range(i + firstLen, n - secondLen + 1):
            sum2 = pre[j + secondLen] - pre[j]
            ans = max(ans, sum1 + sum2)

        # 左侧
        for j in range(0, i - secondLen + 1):
            sum2 = pre[j + secondLen] - pre[j]
            ans = max(ans, sum1 + sum2)

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)` —— 需要两层循环遍历所有起点组合。  
- **空间复杂度**：`O(n)` —— 前缀和数组占用线性空间。

---

### 2. 最优解  

#### 思路  

暴力解慢的根源在于**重复计算**：我们在每一次内部循环里，都要重新遍历整个数组来找另一个子数组的最大和。其实，只要我们事先把“在某个位置左侧（或右侧）出现的最佳子数组和”记录下来，就可以 **一次遍历** 完成答案的计算。

核心技巧是 **前缀最大数组 + 滑动窗口**（等价于单调滑动窗口求固定长度子数组和）。下面分两步讲：

1. **固定长度子数组的和**  
   使用滑动窗口一次遍历得到所有长度为 `L`（`firstLen` 或 `secondLen`）的子数组和，时间 O(n)。  
   想象我们用一根长度为 `L` 的尺子在数组上滑动，每次尺子覆盖的元素和就是子数组和。

2. **左侧/右侧的最佳值**  
   - `left_max[i]`：在下标 `i`（包括 i）之前（左侧），长度为 `L` 的子数组的**最大和**。可以在一次遍历中实时更新。  
   - `right_max[i]`：在下标 `i`（包括 i）之后（右侧），长度为 `L` 的子数组的**最大和**。这需要从右向左遍历一次得到。  

有了这两个数组，我们就可以在一次遍历里尝试两种顺序：

- 先放 `firstLen`，后放 `secondLen`：`left_max_first[i] + right_max_second[i + 1]`
- 先放 `secondLen`，后放 `firstLen`：`left_max_second[i] + right_max_first[i + 1]`

取所有可能 `i` 的最大值即为答案。

> **类比**：把左侧的最佳子数组想象成“左边的最高山峰”，右侧的最佳子数组是“右边的最高山峰”。只要把两座山峰分别放在不相交的位置，峰值之和最大即可。

#### 代码（Python）

```python
from typing import List

def maxSumTwoNoOverlap(nums: List[int], firstLen: int, secondLen: int) -> int:
    n = len(nums)

    # ---------- 1️⃣ 计算所有长度为 L 的子数组和 ----------
    # 返回一个列表 sums，其中 sums[i] 表示以 i 为左端点、长度为 L 的子数组和
    def window_sums(L: int) -> List[int]:
        res = [0] * (n - L + 1)          # 可能的起点个数
        cur = sum(nums[:L])              # 第一个窗口的和
        res[0] = cur
        for i in range(1, n - L + 1):
            cur += nums[i + L - 1] - nums[i - 1]   # 滑动窗口：进来一个，踢走一个
            res[i] = cur
        return res

    sum_first = window_sums(firstLen)   # 长度 firstLen 的所有子数组和
    sum_second = window_sums(secondLen) # 长度 secondLen 的所有子数组和

    # ---------- 2️⃣ 计算左侧最大前缀 ----------
    # left_max_first[i] 表示在下标 i（含）之前，firstLen 子数组的最大和
    left_max_first = [0] * len(sum_first)
    cur_max = 0
    for i, v in enumerate(sum_first):
        cur_max = max(cur_max, v)
        left_max_first[i] = cur_max

    left_max_second = [0] * len(sum_second)
    cur_max = 0
    for i, v in enumerate(sum_second):
        cur_max = max(cur_max, v)
        left_max_second[i] = cur_max

    # ---------- 3️⃣ 计算右侧最大后缀 ----------
    # right_max_first[i] 表示在下标 i（含）之后，firstLen 子数组的最大和
    right_max_first = [0] * len(sum_first)
    cur_max = 0
    for i in range(len(sum_first) - 1, -1, -1):
        cur_max = max(cur_max, sum_first[i])
        right_max_first[i] = cur_max

    right_max_second = [0] * len(sum_second)
    cur_max = 0
    for i in range(len(sum_second) - 1, -1, -1):
        cur_max = max(cur_max, sum_second[i])
        right_max_second[i] = cur_max

    # ---------- 4️⃣ 组合两种排列，求最大 ----------
    ans = 0

    # 先放 firstLen，再放 secondLen
    # i 为 firstLen 子数组的左端点，必须保证 secondLen 子数组在它右侧不重叠
    for i in range(len(sum_first) - secondLen):
        # 第一个子数组结束位置是 i + firstLen - 1
        # 第二个子数组左端点最早是 i + firstLen
        best_second = right_max_second[i + firstLen]
        ans = max(ans, sum_first[i] + best_second)

    # 先放 secondLen，再放 firstLen
    for i in range(len(sum_second) - firstLen):
        best_first = right_max_first[i + secondLen]
        ans = max(ans, sum_second[i] + best_first)

    return ans
```

> **代码要点解释**  
> - `window_sums` 用滑动窗口一次遍历得到所有固定长度子数组的和，时间 O(n)。  
> - `left_max_*` 与 `right_max_*` 分别是前缀最大和后缀最大，类似“从左往右记最大值”和“从右往左记最大值”。  
> - 最后两段循环分别对应两种子数组出现的顺序，只要保证它们不相交（通过下标偏移），就能直接取对应的最大值相加。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 计算窗口和、前缀最大、后缀最大各一次遍历，都是线性时间。  
  - 与暴力解的 `O(n²)` 相比，省去了大量重复的内部循环。  
- **空间复杂度**：`O(n)`  
  - 需要保存四个长度约为 `n` 的辅助数组（窗口和、左/右最大），仍然是线性空间。

---

## 心得  

- **核心技巧**：固定长度子数组的滑动窗口 + 前缀/后缀最大值（相当于“一次遍历搞定左侧最优、右侧最优”）。  
- **适用题型**：  
  1. “Maximum Sum of Three Non‑Overlapping Subarrays”（三个不相交子数组）  
  2. “Maximum Profit in Job Scheduling”（区间调度中的最大收益）  
  3. “Best Time to Buy and Sell Stock III”（两笔不重叠的股票交易）  
- **一句话总结解题钥匙**：**把“在左边的最佳”和“在右边的最佳”预先算好，遍历一次即可得到全局最优**。

---

## 反思  

- **第一反应**：直接枚举所有可能的子数组组合，写出最笨的暴力代码。  
- **最容易踩的坑**：  
  - 忘记子数组之间必须 **不重叠**，导致在组合时出现交叉。  
  - 计算左/右最大时的下标偏移错误（比如 `i + firstLen` vs `i + firstLen - 1`），会让两段子数组相邻但仍算作重叠。  
  - 边界情况：当 `firstLen` 或 `secondLen` 等于数组长度的一半时，只有唯一的放置方式，需要确保循环条件不会越界。  
- **下次遇到同类题**：第一步先 **把固定长度子数组的和写出来**（滑动窗口），然后 **分别求左侧前缀最大和右侧后缀最大**，最后用这两个表格快速组合。这样就能立刻把时间从平方级降到线性级。