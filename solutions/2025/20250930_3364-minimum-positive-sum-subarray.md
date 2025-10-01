# #3364. 最小正和子数组 / Minimum Positive Sum Subarray 

> 难度：简单 · 标签：Array、Sliding Window、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/minimum-positive-sum-subarray/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and two integers l and r. Your task is to find the minimum sum of a subarray whose size is between l and r (inclusive) and whose sum is greater than 0.
Return the minimum sum of such a subarray. If no such subarray exists, return -1.
A subarray is a contiguous non-empty sequence of elements within an array.

**Examples**

**Example 1:**

```
Input: nums = [3, -2, 1, 4], l = 2, r = 3
Output: 1
Explanation:
The subarrays of length between l = 2 and r = 3 where the sum is greater than 0 are:
Out of these, the subarray [3, -2] has a sum of 1, which is the smallest positive sum. Hence, the answer is 1.
```

**Example 2:**

```
Input: nums = [-2, 2, -3, 1], l = 2, r = 3
Output: -1
Explanation:
There is no subarray of length between l and r that has a sum greater than 0. So, the answer is -1.
```

**Example 3:**

```
Input: nums = [1, 2, 3, 4], l = 2, r = 4
Output: 3
Explanation:
The subarray [1, 2] has a length of 2 and the minimum sum greater than 0. So, the answer is 3.
```

**Constraints**

- 1 <= nums.length <= 100
- 1 <= l <= r <= nums.length
- -1000 <= nums[i] <= 1000

---

## 题目（中文翻译）

**描述**  
给定一个整数数组 `nums` 和两个整数 `l`、`r`。请找出长度在 `l` 到 `r`（含）之间且和大于 `0` 的子数组（subarray）中，和最小的那个。返回该子数组的最小正和。如果不存在满足条件的子数组，返回 `-1`。  
子数组是数组中连续的、非空的元素序列。

**示例 1**  
**输入**: `nums = [3, -2, 1, 4]`, `l = 2`, `r = 3`  
**输出**: `1`  
**解释**:  
长度在 `l = 2` 到 `r = 3` 之间且和大于 `0` 的子数组有：  
其中子数组 `[3, -2]` 的和为 `1`，是所有满足条件的子数组中最小的正和。因此答案为 `1`。

**示例 2**  
**输入**: `nums = [-2, 2, -3, 1]`, `l = 2`, `r = 3`  
**输出**: `-1`  
**解释**:  
不存在长度在 `l` 与 `r` 之间且和大于 `0` 的子数组，所以答案为 `-1`。

**示例 3**  
**输入**: `nums = [1, 2, 3, 4]`, `l = 2`, `r = 4`  
**输出**: `3`  
**解释**:  
子数组 `[1, 2]` 的长度为 `2`，且是所有满足条件的子数组中和最小的正数。因此答案为 `3`。

**约束条件**  
- `1 <= nums.length <= 100`  
- `1 <= l <= r <= nums.length`  
- `-1000 <= nums[i] <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的办法就是 **把所有可能的子数组都枚举一遍**，然后挑出满足条件的最小正和。  
- 子数组的长度必须在 `[l, r]` 之间。  
- 子数组的和要大于 `0`，我们只关心最小的那一个。  

> **数据结构类比**  
> 把数组看成一本书的章节，子数组就是连续的几页。我们只需要把所有符合页数范围的连续页数（即子数组）读一遍，记下它们的总字数（和），最后找出最小的正数。

**为什么正确**  
因为我们没有遗漏任何合法的子数组——遍历了所有起点 `i` 和所有合法的终点 `j`（`l ≤ j-i ≤ r`），只要把它们的和算出来并比较，就一定能得到答案。

**复杂度分析（大白话）**  
- **时间**：外层循环遍历起点 `i`（最多 `n` 次），内层循环遍历合法的终点 `j`（最多 `r-l+1 ≤ n` 次），每次都要把子数组的元素累加一次（最坏再遍历 `n` 次），所以时间是 **`O(n³)`**。在本题的约束 `n ≤ 100` 下仍然可以接受，但已经不是最优的了。  
- **空间**：只用了几个整数来保存临时和，**`O(1)`**。

#### 代码（Python）

```python
from typing import List

def min_positive_sum_bruteforce(nums: List[int], l: int, r: int) -> int:
    n = len(nums)
    ans = float('inf')                 # 记录当前找到的最小正和
    # i 为子数组的左端点（包含），0 ≤ i < n
    for i in range(n):
        # j 为子数组的右端点（不包含），长度为 j-i
        for length in range(l, r + 1):
            j = i + length
            if j > n:                   # 超出数组范围，直接跳过
                continue
            # 计算子数组 nums[i:j] 的和
            sub_sum = 0
            for k in range(i, j):
                sub_sum += nums[k]
            # 只关心和大于 0 的情况
            if sub_sum > 0:
                ans = min(ans, sub_sum)
    return -1 if ans == float('inf') else ans
```

> **代码要点**  
> - `ans` 初始为正无穷，表示还没有找到合法子数组。  
> - 三层循环分别负责起点、长度、求和，直观易懂。  
> - 最后如果 `ans` 没有被更新，说明不存在满足条件的子数组，返回 `-1`。

#### 复杂度

- **时间复杂度**：`O(n³)` —— 三层循环，最坏情况下每层都遍历 `n` 次。  
  - **含义**：如果 `n = 100`，大约会进行 `1,000,000` 次基本操作，在现代电脑上仍然可以在毫秒级完成，但随着 `n` 增大，这个算法会很快变慢。  
- **空间复杂度**：`O(1)` —— 只用了常数个额外变量。

---

### 2. 最优解

#### 思路  

暴力解的慢点主要在 **重复计算子数组的和**。  
如果我们事先把前缀和算好，子数组的和就可以 ** O(1) ** 直接求出来，枚举所有合法的 `(i, j)` 只需要两层循环，时间降到 `O(n²)`。  
但我们还能更进一步：  

- 设前缀和数组 `pre[0] = 0`，`pre[i] = nums[0] + … + nums[i-1]`。  
- 子数组 `nums[i:j]`（左闭右开）的和 = `pre[j] - pre[i]`，长度 = `j - i`。  
- 条件 `l ≤ j - i ≤ r` 等价于 `i ∈ [j - r, j - l]`。  

对每个右端点 `j`，我们只需要在 **窗口 `[j-r, j-l]`** 中找一个 `pre[i]`，使得：

1. `pre[j] - pre[i] > 0`（和为正）  
2. `pre[j] - pre[i]` 尽可能小（即 `pre[i]` 尽可能接近但小于 `pre[j]`）  

于是问题转化为：**在一个不断滑动的窗口里，快速找到小于当前值的最大前缀和**。  
这正好可以用 **有序容器 + 二分查找**（在 Python 中用 `bisect` 模块）实现：

1. 维护一个有序列表 `window`，它始终保存下标在 `[j-r, j-l]` 之间的前缀和。  
2. 当 `j` 向右移动时，**加入** `pre[j-l]`（左边界进入窗口），**删除** `pre[j-r-1]`（左边界已经超出窗口）。  
3. 用 `bisect_left` 在 `window` 中找到第一个 **不小于** `pre[j]` 的位置 `pos`，则 `pos-1` 位置的元素是 **小于** `pre[j]` 的最大前缀和。  
4. 若存在这样的前缀和，就计算差值并更新答案。  

> **数据结构类比**  
> 想象 `window` 是一本已经排好序的电话簿（前缀和），我们每次只关心“比我稍小一点的最大号码”。二分查找就像在电话簿里快速定位的过程，时间是 `O(log n)`。

这样整体复杂度是 **`O(n log n)`**，已经是本题在 `n ≤ 100` 时的最优方案（更大的数据规模下也能轻松应付）。

#### 代码（Python）

```python
from typing import List
import bisect

def min_positive_sum_opt(nums: List[int], l: int, r: int) -> int:
    n = len(nums)
    # 1. 计算前缀和
    pre = [0] * (n + 1)
    for i in range(1, n + 1):
        pre[i] = pre[i - 1] + nums[i - 1]

    ans = float('inf')          # 当前最小的正和
    window = []                 # 有序列表，存放下标在 [j-r, j-l] 之间的前缀和

    # 2. 从左到右枚举右端点 j（子数组右边界不包括 j 本身）
    for j in range(l, n + 1):   # j 最小要 >= l，这样才可能有长度 >= l 的子数组
        # ① 把新的左边界 pre[j-l] 加入窗口
        bisect.insort(window, pre[j - l])

        # ② 如果窗口已经超出长度 r，需要把最左边的 pre[j-r-1] 删除
        if j - r - 1 >= 0:
            # 在有序列表中找到要删除的值所在的位置并弹出
            idx = bisect.bisect_left(window, pre[j - r - 1])
            if idx < len(window) and window[idx] == pre[j - r - 1]:
                window.pop(idx)

        # ③ 在窗口里找 “小于 pre[j] 的最大前缀和”
        pos = bisect.bisect_left(window, pre[j])   # 第一个 >= pre[j] 的位置
        if pos > 0:                               # 说明存在小于 pre[j] 的元素
            best_pre = window[pos - 1]            # 最大的、但仍然 < pre[j]
            cur_sum = pre[j] - best_pre
            if cur_sum > 0:                       # 必须是正数
                ans = min(ans, cur_sum)

    return -1 if ans == float('inf') else ans
```

> **代码要点解释**  
> - `pre` 保存前缀和，求子数组和只需要两数相减。  
> - `window` 用 `bisect.insort` 保持有序，插入和删除的时间都是 `O(log n)`。  
> - `bisect_left(window, pre[j])` 返回第一个不小于 `pre[j]` 的位置，`pos-1` 就是我们要的“最大但仍小于 `pre[j]`”。  
> - 每次找到合法差值后更新 `ans`，最终如果 `ans` 没变则返回 `-1`。

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 每个右端点 `j` 只做常数次的二分插入、二分删除和一次二分查询，都是 `log` 级别的操作。相比暴力的 `O(n³)`，在 `n=100` 时从上万次降到几千次，规模更大时优势更明显。  
- **空间复杂度**：`O(n)`  
  - 主要是前缀和数组 `pre`（长度 `n+1`）和有序窗口 `window`（最多保存 `r-l+1 ≤ n` 个前缀和），都是线性空间。

---

## 心得

- **核心技巧**：**前缀和 + 有序窗口（二分查找）**，把“子数组求和”转化为“两个前缀和的差”，再利用有序结构快速定位满足条件的前缀和。  
- **适用的题型**  
  1. **区间长度有约束的最小/最大子数组和**（如本题）。  
  2. **在滑动窗口内找满足某种比较关系的元素**（如“窗口内最大/最小值”）。  
  3. **前缀和 + 单调/有序结构** 的变形题（如 “最长子数组和 ≤ K”、 “最小正子数组乘积”等）。  
- **一句话总结**：**把子数组和写成前缀差，再在长度窗口里用有序结构找“比我小一点的最大前缀”，差值就是最小的正和**。

---

## 反思

- **第一反应**：直接枚举所有子数组，写三层循环。因为题目规模小，这样能先得到正确答案。  
- **最容易踩的坑**  
  - **窗口边界**：忘记在 `j` 增长时同时加入 `pre[j-l]`、删除 `pre[j-r-1]`，导致窗口里包含了非法的前缀和。  
  - **二分查找的细节**：`bisect_left` 返回的是第一个 **不小于** 的位置，若要找“小于”的最大值，需要取 `pos-1` 并检查 `pos > 0`。  
  - **正数判定**：即使找到了前缀差，也要确保它大于 `0`，否则不符合题意。  
- **下次类似题的第一步**：先写出前缀和，把“子数组和”转成“前缀差”。随后思考“长度范围”对应的 **滑动窗口**，决定是否需要有序/单调结构来在窗口里快速查询满足条件的前缀。这样就能从暴力到 `O(n log n)` 的思路自然展开。