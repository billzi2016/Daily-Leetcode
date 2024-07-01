# #2760. 阈值下的最长奇偶子数组 / Longest Even Odd Subarray With Threshold

> 难度：简单 · 标签：Array、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/longest-even-odd-subarray-with-threshold/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums and an integer threshold.
Find the length of the longest subarray of nums starting at index l and ending at index r (0 <= l <= r < nums.length) that satisfies the following conditions:
Return an integer denoting the length of the longest such subarray.
Note: A subarray is a contiguous non-empty sequence of elements within an array.

**Examples**

**Example 1:**

```
Input: nums = [3,2,5,4], threshold = 5
Output: 3
Explanation: In this example, we can select the subarray that starts at l = 1 and ends at r = 3 => [2,5,4]. This subarray satisfies the conditions.
Hence, the answer is the length of the subarray, 3. We can show that 3 is the maximum possible achievable length.
```

**Example 2:**

```
Input: nums = [1,2], threshold = 2
Output: 1
Explanation: In this example, we can select the subarray that starts at l = 1 and ends at r = 1 => [2]. 
It satisfies all the conditions and we can show that 1 is the maximum possible achievable length.
```

**Example 3:**

```
Input: nums = [2,3,4,5], threshold = 4
Output: 3
Explanation: In this example, we can select the subarray that starts at l = 0 and ends at r = 2 => [2,3,4]. 
It satisfies all the conditions.
Hence, the answer is the length of the subarray, 3. We can show that 3 is the maximum possible achievable length.
```

**Constraints**

- 1 <= nums.length <= 100
- 1 <= nums[i] <= 100
- 1 <= threshold <= 100

---

## 题目（中文翻译）

给定一个下标从 0 开始的整数数组 `nums` 和一个整数 `threshold`。  
找出满足以下条件的子数组（subarray）`nums[l..r]`（其中 `0 ≤ l ≤ r < nums.length`）的最长长度，并返回该长度。

> **注意**：子数组是数组中连续的、非空的元素序列。

---

### 示例

#### 示例 1
**输入**: `nums = [3,2,5,4]`, `threshold = 5`  
**输出**: `3`  
**解释**: 可以选择下标 `l = 1`、`r = 3` 的子数组 `[2,5,4]`。该子数组满足所有条件，长度为 3。可以证明 3 是能够得到的最大长度。

#### 示例 2
**输入**: `nums = [1,2]`, `threshold = 2`  
**输出**: `1`  
**解释**: 可以选择下标 `l = 1`、`r = 1` 的子数组 `[2]`。它满足所有条件，且长度 1 已经是最大可能值。

#### 示例 3
**输入**: `nums = [2,3,4,5]`, `threshold = 4`  
**输出**: `3`  
**解释**: 可以选择下标 `l = 0`、`r = 2` 的子数组 `[2,3,4]`。该子数组满足所有条件，长度为 3，且这是可达的最大长度。

---

### 约束条件
- `1 ≤ nums.length ≤ 100`
- `1 ≤ nums[i] ≤ 100`
- `1 ≤ threshold ≤ 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的办法就是把所有可能的**连续子数组**都枚举一遍，逐个检查它们是否满足题目要求：

1. **遍历所有左端点** `l`（从 `0` 到 `n‑1`）。  
2. 对每个左端点，再 **遍历所有右端点** `r`（从 `l` 到 `n‑1`），形成子数组 `nums[l … r]`。  
3. 在得到子数组后，**统计**  
   - 子数组中偶数的个数 `even_cnt`  
   - 子数组中奇数的个数 `odd_cnt`  
   - 奇数元素的 **和** `odd_sum`  
4. 判断是否满足两条条件  
   - `odd_sum ≤ threshold`（奇数之和不超过阈值）  
   - `even_cnt > odd_cnt`（偶数个数严格大于奇数个数）  
5. 若满足，就把当前子数组的长度 `r‑l+1` 与全局最大长度比较，取最大值。

> **类比**：把数组想象成一条街道，`l` 是街道的左门，`r` 是右门。我们把每一段可能的街道（子数组）都走一遍，记录下“偶数居民”和“奇数居民”的人数以及奇数居民的总财富（和），看哪段街道既满足财富不超标，又让偶数居民多于奇数居民，并且最长。

**为什么正确**  
因为我们把**所有**合法的子数组都检查了一遍，最大的合法长度自然会被找到。

**复杂度分析**  
- 外层遍历 `l` 有 `n` 次，内层遍历 `r` 最多也有 `n` 次，统计子数组信息需要 `O(r‑l+1)` 的时间。整体时间是  
  \[
  O\!\left(\sum_{l=0}^{n-1}\sum_{r=l}^{n-1} (r-l+1)\right)=O(n^3)
  \]  
  对于本题的约束（`n ≤ 100`），`n³` 仍然能跑完，但显得“笨拙”。  
- 只用了常数级的额外空间，`O(1)`。

> **大白话**：`O(n³)` 就像把 100 本书每本都翻 100 页，每页再读 100 行，虽然还能接受，但显然有更省力的办法。

#### 代码（Python）

```python
def longestEvenOddSubarray(nums, threshold):
    n = len(nums)
    best = 0                                 # 记录目前找到的最长合法长度

    # 枚举左端点 l
    for l in range(n):
        even_cnt = 0
        odd_cnt = 0
        odd_sum = 0

        # 枚举右端点 r，顺着右边扩展子数组
        for r in range(l, n):
            if nums[r] % 2 == 0:              # 偶数
                even_cnt += 1
            else:                             # 奇数
                odd_cnt += 1
                odd_sum += nums[r]

            # 检查当前子数组是否满足条件
            if odd_sum <= threshold and even_cnt > odd_cnt:
                best = max(best, r - l + 1)   # 更新最长长度

    return best
```

#### 复杂度

- **时间复杂度**：`O(n³)` —— 三层循环（左端点、右端点、统计子数组），在最坏情况下每次都要遍历子数组的所有元素。  
- **空间复杂度**：`O(1)` —— 只使用了常数个计数器。

---

### 2. 最优解

#### 思路  

暴力解的主要瓶颈在于**重复统计**同一个子数组的奇偶信息。  
当我们把右端点 `r` 向右移动一格时，只会新增一个元素 `nums[r]`，于是可以 **增量更新**：

- 如果 `nums[r]` 是偶数，`even_cnt += 1`  
- 如果是奇数，`odd_cnt += 1` 且 `odd_sum += nums[r]`

这让我们可以在 **O(1)** 的时间内得到新的窗口统计信息。于是我们可以使用 **滑动窗口（双指针）**：

1. 用两个指针 `left`、`right` 表示当前窗口 `[left, right]`。  
2. `right` 逐步向右扩张，每次把新元素的统计信息加入窗口。  
3. 若窗口 **不合法**（`odd_sum > threshold` **或** `even_cnt ≤ odd_cnt`），就把左指针 `left` 向右收缩，直到窗口恢复合法。收缩时要把离开的元素对应的计数/和减掉。  
4. 每次窗口合法后，用 `right - left + 1` 与答案比较，取最大值。

> **类比**：想象有一根可伸缩的绳子，两个人分别站在绳子的左右两端（`left` 与 `right`），我们让右边的人不断往前走（扩张），如果绳子太长或两边人数不符合要求，就让左边的人往前走（收缩）把绳子拉短。每次绳子合法时记录当前长度，最终得到最长合法长度。

**为什么正确**  
滑动窗口始终维护 **一个** 连续子数组的统计信息，且：

- 当窗口合法时，它必然是 **以 `right` 为右端点的所有合法子数组中最长的**（因为左端点已经尽可能左移了）。  
- 当窗口不合法时，左端点必然需要右移才能恢复合法，否则无论右端点再怎么向右，窗口的奇数和或偶数/奇数比例都不会改善。  

遍历完所有 `right`，所有以每个位置为右端点的合法子数组都被考虑过，最大长度自然被找出。

**复杂度分析**  
- 每个元素最多被 `right` 指针加入一次、被 `left` 指针移出一次，整体 **线性** `O(n)`。  
- 只需要保存四个计数器（`even_cnt, odd_cnt, odd_sum, best`），空间 `O(1)`。

#### 代码（Python）

```python
def longestEvenOddSubarray(nums, threshold):
    n = len(nums)
    left = 0               # 窗口左端点
    even_cnt = 0           # 窗口内偶数个数
    odd_cnt = 0            # 窗口内奇数个数
    odd_sum = 0            # 窗口内奇数元素的和
    best = 0               # 当前找到的最长合法长度

    # 右端点逐个右移
    for right in range(n):
        val = nums[right]
        if val % 2 == 0:           # 偶数
            even_cnt += 1
        else:                      # 奇数
            odd_cnt += 1
            odd_sum += val

        # 若窗口不合法，就收缩左端点，直到合法为止
        while odd_sum > threshold or even_cnt <= odd_cnt:
            left_val = nums[left]
            if left_val % 2 == 0:   # 移出的是偶数
                even_cnt -= 1
            else:                    # 移出的是奇数
                odd_cnt -= 1
                odd_sum -= left_val
            left += 1                # 左端点右移

        # 此时窗口合法，更新答案
        best = max(best, right - left + 1)

    return best
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 每个元素至多进入一次窗口、退出一次窗口。相当于只遍历了一遍数组。  
- **空间复杂度**：`O(1)` —— 只用了常数个额外变量。

---

## 心得

- **核心技巧**：**滑动窗口**（双指针）——在需要寻找满足“某些累计条件”的最长/最短子数组时，往往可以把窗口的左右端点当作两个指针，让右指针不断扩张、左指针在必要时收缩，从而实现线性时间。
- **适用的类似题型**  
  1. *最长子数组的和不超过 K*（LeetCode 862）  
  2. *最多包含 K 个不同字符的最长子串*（LeetCode 424）  
  3. *最长子数组中 1 的个数不超过 K*（LeetCode 1004）
- **一句话总结**：**只要能在 O(1) 时间内更新窗口统计信息，就可以用滑动窗口把暴力的 O(n³) 降到 O(n)。**

---

## 反思

- **第一反应**：看到“最长子数组”“阈值”“偶数/奇数”，立刻想到枚举所有子数组（暴力）——最直观但最慢的办法。  
- **最容易踩的坑**  
  - **边界条件**：窗口收缩时要正确地把离开的元素从计数/和中减掉，尤其是奇数的和 `odd_sum`。  
  - **条件顺序**：判断合法性的两个条件是“`odd_sum ≤ threshold`” **且** “`even_cnt > odd_cnt`”。忘记任意一个都会导致错误的答案。  
  - **空窗口**：在所有子数组都不合法的情况下，答案应该是 `0`（本题保证至少有一个合法子数组，但实现时仍需防止 `best` 初始值设错）。  
- **下次遇到同类题**：  
  1. 先明确“窗口内需要维护哪些累计信息”（计数、和、最大值等）。  
  2. 判断这些信息是否可以 **增量更新**（加入/移除一个元素的代价是否 O(1)）。  
  3. 若可以，就立刻尝试 **滑动窗口**；若不行，再考虑更高级的数据结构（单调队列、前缀和 + 哈希等）。