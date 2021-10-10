# #1508. 已排序子数组和的区间和 / Range Sum of Sorted Subarray Sums

> 难度：中等 · 标签：Array、Two Pointers、Binary Search、Sorting、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/range-sum-of-sorted-subarray-sums/)

---

## 题目（英文原版）

**Description**

You are given the array nums consisting of n positive integers. You computed the sum of all non-empty continuous subarrays from the array and then sorted them in non-decreasing order, creating a new array of n * (n + 1) / 2 numbers.
Return the sum of the numbers from index left to index right (indexed from 1), inclusive, in the new array. Since the answer can be a huge number return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,4], n = 4, left = 1, right = 5
Output: 13 
Explanation: All subarray sums are 1, 3, 6, 10, 2, 5, 9, 3, 7, 4. After sorting them in non-decreasing order we have the new array [1, 2, 3, 3, 4, 5, 6, 7, 9, 10]. The sum of the numbers from index le = 1 to ri = 5 is 1 + 2 + 3 + 3 + 4 = 13.
```

**Example 2:**

```
Input: nums = [1,2,3,4], n = 4, left = 3, right = 4
Output: 6
Explanation: The given array is the same as example 1. We have the new array [1, 2, 3, 3, 4, 5, 6, 7, 9, 10]. The sum of the numbers from index le = 3 to ri = 4 is 3 + 3 = 6.
```

**Example 3:**

```
Input: nums = [1,2,3,4], n = 4, left = 1, right = 10
Output: 50
```

**Constraints**

- n == nums.length
- 1 <= nums.length <= 1000
- 1 <= nums[i] <= 100
- 1 <= left <= right <= n * (n + 1) / 2

---

## 题目（中文翻译）

**描述**  
给定一个由 `n` 个正整数构成的数组 `nums`。你需要计算该数组所有非空连续子数组的和，并将这些和按非递减顺序排序，形成一个新数组，长度为 `n * (n + 1) / 2`。返回新数组中下标从 `left` 到 `right`（下标从 1 开始，闭区间）的元素之和。由于答案可能非常大，请返回对 `10^9 + 7` 取模后的结果。

**示例**

**示例 1**  
```
Input: nums = [1,2,3,4], n = 4, left = 1, right = 5
Output: 13
```
**解释**：所有子数组的和为 `1, 3, 6, 10, 2, 5, 9, 3, 7, 4`。排序后得到新数组 `[1, 2, 3, 3, 4, 5, 6, 7, 9, 10]`。下标 `left = 1` 到 `right = 5` 的元素之和为 `1 + 2 + 3 + 3 + 4 = 13`。

**示例 2**  
```
Input: nums = [1,2,3,4], n = 4, left = 3, right = 4
Output: 6
```
**解释**：同示例 1，排序后的数组为 `[1, 2, 3, 3, 4, 5, 6, 7, 9, 10]`。下标 `left = 3` 到 `right = 4` 的元素之和为 `3 + 3 = 6`。

**示例 3**  
```
Input: nums = [1,2,3,4], n = 4, left = 1, right = 10
Output: 50
```
**解释**：排序后的完整数组为 `[1, 2, 3, 3, 4, 5, 6, 7, 9, 10]`，所有元素之和为 `50`。

**约束条件**  
- `n == nums.length`  
- `1 <= nums.length <= 1000`  
- `1 <= nums[i] <= 100`  
- `1 <= left <= right <= n * (n + 1) / 2`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有子数组的和全部算出来**，放进一个大列表，然后**把列表排序**，最后把第 `left`~`right` 位的数相加即可。

- **子数组**：数组的连续片段。比如 `[1,2,3]` 的子数组有 `[1]、[2]、[3]、[1,2]、[2,3]、[1,2,3]`。  
- **前缀和**（Prefix Sum）：把数组的前缀累计起来，`pre[i] = nums[0] + … + nums[i-1]`。有了前缀和，子数组 `[l, r]` 的和可以用 `pre[r+1] - pre[l]` O(1) 时间算出来，像查字典一样——“键”是下标，返回的就是对应的累计值。  
- **排序**：把所有子数组和放进列表后，用 Python 的 `list.sort()`（底层是快速排序/归并排序）把它们从小到大排好序。

**为什么这个方法一定对**  
因为我们没有遗漏任何非空连续子数组，也没有对它们的和做任何修改，直接按照题目要求的顺序（先算完再排序）得到的结果必然是正确的。

**时间/空间复杂度**（大白话解释）  

- **时间**：  
  1. 生成所有子数组和：外层遍历起点 `i`（`n` 次），内层遍历终点 `j`（平均约 `n/2` 次），总共大约 `n·(n+1)/2` ≈ `n²/2` 次计算，每次 O(1)。  
  2. 排序：要排 `k = n·(n+1)/2` 个数，排序的时间是 `k·log k`，这里的 `log` 是以 2 为底的对数，想象把 `k` 分成两半再两半……直到只剩一个。  
  所以整体时间是 **O(n² + k·log k)**，在最坏情况下约 **O(n²·log n)**（因为 `k` 与 `n²` 同阶）。  
- **空间**：我们需要把所有子数组和保存下来，需要 `k` 个整数，空间是 **O(k) = O(n²)**。  

> 用生活中的比喻：如果你把所有的水果（子数组和）装进一个大篮子（列表）再排序，那篮子本身的大小就是 `n²`，而把水果一个个挑出来放进篮子、再排队的过程就是 O(n²·log n)。

#### 代码（Python）

```python
from typing import List

MOD = 10**9 + 7

def rangeSum(nums: List[int], left: int, right: int) -> int:
    n = len(nums)

    # 1️⃣ 计算前缀和，方便 O(1) 求子数组和
    prefix = [0] * (n + 1)               # prefix[i] = 前 i 个数的和
    for i in range(n):
        prefix[i + 1] = prefix[i] + nums[i]

    # 2️⃣ 暴力枚举所有子数组，把它们的和放进 big 列表
    all_sums = []                        # 长度是 n*(n+1)//2
    for start in range(n):               # 子数组的左端点
        for end in range(start, n):      # 子数组的右端点（包含）
            s = prefix[end + 1] - prefix[start]   # 子数组和
            all_sums.append(s)

    # 3️⃣ 排序
    all_sums.sort()

    # 4️⃣ 累加第 left~right 位（下标从 1 开始，需要 -1 转成 Python 的 0 基）
    ans = sum(all_sums[left - 1: right]) % MOD
    return ans
```

> **关键行中文注释**  
> - `prefix[i + 1] = prefix[i] + nums[i]`  # 把第 i 个数加进去，得到前 i+1 个数的累计和  
> - `s = prefix[end + 1] - prefix[start]`  # 用前缀和算子数组 `[start, end]` 的和  
> - `all_sums.sort()`  # 把所有子数组和从小到大排好序  

#### 复杂度

- **时间复杂度**：`O(n²·log n)`  
  - `n²` 来自枚举所有子数组，`log n` 来自对约 `n²/2` 个数排序。  
- **空间复杂度**：`O(n²)`  
  - 需要保存所有子数组和的列表。

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于**把所有子数组和全部存下来再排序**。  
当 `n = 1000` 时，子数组个数约 500 000，虽然还能接受，但如果 `n` 更大，空间和时间都会暴涨。我们要 **只关心前 `right` 小的和**，不必真的把全部和列出来。

思路的核心是：

1. **二分答案**  
   - 把可能的子数组和范围当成一个搜索区间。  
   - 设 `mid` 为区间中点，统计**有多少子数组的和 ≤ mid**，以及这些子数组的**和的总和**。  
   - 如果数量 < `k`（我们想要前 `k` 小的和），说明 `mid` 太小，需要往更大的区间找；否则说明 `mid` 足够大，左边还能继续收紧。  
   - 通过二分，我们能找到**第 `k` 小的子数组和的阈值** `thresh(k)`，并且还能得到**所有 ≤ thresh(k) 的子数组和的总和** `sum_le(k)`。

2. **如何在 O(n) 内统计 “≤ mid 的子数组个数 & 总和”**  
   - 使用 **前缀和** `pre[i]`（同暴力解）。子数组 `[l, r]` 的和 = `pre[r+1] - pre[l]`。  
   - 对每个左端点 `l`，我们想找最大的右端点 `r` 使得 `pre[r+1] - pre[l] ≤ mid`。因为 `nums` 全是正数，`pre` 单调递增，**右端点只会向右移动**，可以用 **滑动窗口 / 双指针** 实现 O(n)。  
   - 设当前窗口是 `[l, r]`（右端点 `r` 为**可行的最大**），窗口内有 `cnt = r - l + 1` 个子数组以 `l` 为左端点且和 ≤ mid。  
   - 为了累加这些子数组的和，我们再利用 **前缀前缀和**（即 `pre2[i] = pre[0] + pre[1] + … + pre[i-1]`）。有了 `pre2`，窗口内所有子数组的和可以用下面的公式快速算出：

\[
\text{window\_sum} = \underbrace{(pre2[r+1] - pre2[l])}_{\text{所有前缀和的和}} \;-\; cnt \times pre[l]
\]

   - 解释：`pre2[r+1] - pre2[l]` 把 `pre[l] , pre[l+1] , … , pre[r]` 加起来；每个子数组和等于 `pre[t] - pre[l]`（`t` 从 `l+1` 到 `r+1`），所以把 `pre[l]` 重复减去 `cnt` 次即可。

3. **把 “前 k 小的子数组和的总和” 变成两次二分**  
   - 定义函数 `count_and_sum(limit)` 返回 `(cnt, total)`，即 **所有子数组和 ≤ limit 的个数和它们的和**。  
   - 先二分找 **第 `k` 小的子数组和的阈值** `val`，使得 `count_and_sum(val).cnt >= k` 且 `count_and_sum(val-1).cnt < k`。  
   - 设 `cnt, total = count_and_sum(val)`，此时 `total` 包含了 **所有 ≤ val** 的子数组和。因为可能多了 `cnt - k` 个恰好等于 `val` 的子数组，需要把它们的 `val` * (cnt - k) 再减掉，得到**恰好前 `k` 小的和的总和** `prefixSum(k)`。  

4. **最终答案**  
   - 需要 `[left, right]` 的和 → `prefixSum(right) - prefixSum(left-1)`（左闭右闭）。  
   - 最后对 `1e9+7` 取模。

**为什么这比暴力快**  
- 每次 `count_and_sum` 只遍历一次数组，时间 O(n)。  
- 二分的搜索区间是子数组和的最大可能值 `sum(nums)`（≤ 100 000），对数约 17 次。  
- 整体时间 **O(n log (maxSum))**，空间只要几段前缀数组，**O(n)**。

#### 代码（Python）

```python
from typing import List

MOD = 10**9 + 7

def rangeSum(nums: List[int], left: int, right: int) -> int:
    n = len(nums)

    # ---------- 1️⃣ 前缀和 & 前缀前缀和 ----------
    pre = [0] * (n + 1)          # pre[i] = nums[0] + … + nums[i-1]
    for i in range(n):
        pre[i + 1] = pre[i] + nums[i]

    pre2 = [0] * (n + 2)         # pre2[i] = pre[0] + … + pre[i-1]
    for i in range(1, n + 2):
        pre2[i] = pre2[i - 1] + pre[i - 1]

    # ---------- 2️⃣ 统计 ≤ limit 的子数组个数 & 和 ----------
    def count_and_sum(limit: int):
        """返回 (cnt, total)，cnt 为子数组和 ≤ limit 的个数，
           total 为这些子数组和的总和（不取模）"""
        cnt = 0
        total = 0
        r = 0                     # 右指针，表示当前窗口的最大右端点（含）
        for l in range(n):       # l 为左端点
            # 把 r 往右移动，只要子数组和仍 ≤ limit
            while r < n and pre[r + 1] - pre[l] <= limit:
                r += 1
            # 此时窗口 [l, r-1]（右端点是 r-1）全部合法
            cur_cnt = r - l       # 以 l 为左端点的合法子数组个数
            cnt += cur_cnt

            # 利用 pre2 计算这些子数组的和
            # 公式： (pre2[r] - pre2[l]) - cur_cnt * pre[l]
            cur_sum = (pre2[r] - pre2[l]) - cur_cnt * pre[l]
            total += cur_sum
        return cnt, total

    # ---------- 3️⃣ 前 k 小的子数组和的前缀和 ----------
    def prefixSum(k: int) -> int:
        """返回前 k 小的子数组和的总和（取模前）"""
        if k <= 0:
            return 0

        # 二分找到最小的阈值 val，使得 count(val) >= k
        lo, hi = 1, pre[-1]               # 子数组和最小是 1，最大是整个数组和
        while lo < hi:
            mid = (lo + hi) // 2
            cnt, _ = count_and_sum(mid)
            if cnt >= k:
                hi = mid
            else:
                lo = mid + 1
        val = lo                           # 这个 val 就是第 k 小的那个数

        cnt, total = count_and_sum(val)    # ≤ val 的所有子数组和
        # 可能有多余的等于 val 的子数组，需要去掉 (cnt - k) 个 val
        excess = cnt - k
        total -= excess * val
        return total % MOD

    # ---------- 4️⃣ 计算答案 ----------
    ans = (prefixSum(right) - prefixSum(left - 1)) % MOD
    return ans
```

> **代码要点中文注释**  
> - `pre[i + 1] = pre[i] + nums[i]`  # 前缀和，方便 O(1) 求子数组和  
> - `pre2[i] = pre2[i - 1] + pre[i - 1]`  # 前缀的前缀，用来快速求窗口内所有前缀和的和  
> - `while r < n and pre[r + 1] - pre[l] <= limit: r += 1`  # 双指针：右端点只会向右移动，保证子数组和 ≤ limit  
> - `cur_sum = (pre2[r] - pre2[l]) - cur_cnt * pre[l]`  # 通过公式一次性把窗口内所有子数组的和加进去  

#### 复杂度

- **时间复杂度**：`O(n·log(maxSum))`  
  - `count_and_sum` 线性遍历一次数组 → `O(n)`。  
  - 二分搜索的范围是子数组和的最大可能值 `maxSum = sum(nums) ≤ 100 000`，对数约 17。  
  - 所以整体约 `n * 17`，对 `n = 1000` 完全轻松。  

- **空间复杂度**：`O(n)`  
  - 只需要存前缀和 `pre`、前缀前缀和 `pre2`，以及少量常数变量。  

---

## 心得

- **核心技巧**：**前缀和 + 双指针 + 二分**，把“统计 ≤ 某阈值的子数组个数和总和”这件事压到 O(n) 里，然后通过二分把目标 “前 k 小的和” 找出来。  
- **适用的题型**  
  1. **子数组和排序相关**（如 “第 K 小的子数组和”）  
  2. **需要统计满足某个上界的子数组数量**（如 “子数组和不大于 target 的个数”）  
  3. **区间和的前缀求和**（如 “区间内子数组和的和”）  
- **一句话总结解题钥匙**：  
  > “把所有子数组和的排序问题转化为‘给定阈值，能得到多少个子数组’，再用二分定位阈值即可。”

---

## 反思

- **第一反应**：直接把所有子数组和列出来，然后排序——这就是暴力解。  
- **最容易踩的坑**  
  1. **整数溢出 / 取模**：累加的总和可能非常大，需要在最后一步统一取模（`10**9+7`），而不是每一步都取模，否则会破坏二分判断的正确性。  
  2. **双指针的边界**：右指针 `r` 在循环结束后指向的是 **第一个不合法的下标**，窗口实际是 `[l, r-1]`，要记得 `cur_cnt = r - l`。  
  3. **阈值二分的上下界**：最小可能的子数组和是数组中最小元素（这里是 1），最大是全部元素之和，若上下界取错会导致死循环。  
- **下次遇到同类题**：  
  1. **先问自己**：是否可以用“统计 ≤ X 的子数组”这种单调性质的判定函数？  
  2. **如果可以**，立刻构造 O(n) 的判定函数（前缀和 + 双指针），再用二分定位所需的阈值。  

这样就能把原本看似 O(n²·log n) 的暴力解，优化到 O(n·log maxSum) 的高效方案。祝你编码愉快！