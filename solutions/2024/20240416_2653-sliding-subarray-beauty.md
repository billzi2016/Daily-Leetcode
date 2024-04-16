# #2653. 滑动子数组美感 / Sliding Subarray Beauty

> 难度：中等 · 标签：Array、Hash Table、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/sliding-subarray-beauty/)

---

## 题目（英文原版）

**Description**

Given an integer array nums containing n integers, find the beauty of each subarray of size k.
The beauty of a subarray is the xth smallest integer in the subarray if it is negative, or 0 if there are fewer than x negative integers.
Return an integer array containing n - k + 1 integers, which denote the beauty of the subarrays in order from the first index in the array.

**Examples**

**Example 1:**

```
Input: nums = [1,-1,-3,-2,3], k = 3, x = 2
Output: [-1,-2,-2]
Explanation: There are 3 subarrays with size k = 3. 
The first subarray is [1, -1, -3] and the 2nd smallest negative integer is -1. 
The second subarray is [-1, -3, -2] and the 2nd smallest negative integer is -2. 
The third subarray is [-3, -2, 3] and the 2nd smallest negative integer is -2.
```

**Example 2:**

```
Input: nums = [-1,-2,-3,-4,-5], k = 2, x = 2
Output: [-1,-2,-3,-4]
Explanation: There are 4 subarrays with size k = 2.
For [-1, -2], the 2nd smallest negative integer is -1.
For [-2, -3], the 2nd smallest negative integer is -2.
For [-3, -4], the 2nd smallest negative integer is -3.
For [-4, -5], the 2nd smallest negative integer is -4.
```

**Example 3:**

```
Input: nums = [-3,1,2,-3,0,-3], k = 2, x = 1
Output: [-3,0,-3,-3,-3]
Explanation: There are 5 subarrays with size k = 2.
For [-3, 1], the 1st smallest negative integer is -3.
For [1, 2], there is no negative integer so the beauty is 0.
For [2, -3], the 1st smallest negative integer is -3.
For [-3, 0], the 1st smallest negative integer is -3.
For [0, -3], the 1st smallest negative integer is -3.
```

**Constraints**

- n == nums.length
- 1 <= n <= 105
- 1 <= k <= n
- 1 <= x <= k
- -50 <= nums[i] <= 50

---

## 题目（中文翻译）

给定一个包含 **n** 个整数的整数数组（integer array）`nums`，求所有大小为 `k` 的子数组（subarray）的美感（beauty）。

子数组的美感定义为：如果子数组中负整数（negative integer）不少于 `x` 个，则美感为该子数组中第 `x` 小的负整数；否则美感为 `0`。

返回一个长度为 `n - k + 1` 的整数数组，依次记录从数组首位开始的每个长度为 `k` 的子数组的美感。

---

### 示例

**示例 1**

```text
Input: nums = [1,-1,-3,-2,3], k = 3, x = 2
Output: [-1,-2,-2]
Explanation: 共有 3 个大小为 k = 3 的子数组。
- 第一个子数组是 [1, -1, -3]，第 2 小的负整数是 -1。  
- 第二个子数组是 [-1, -3, -2]，第 2 小的负整数是 -2。  
- 第三个子数组是 [-3, -2, 3]，第 2 小的负整数是 -2。
```

**示例 2**

```text
Input: nums = [-1,-2,-3,-4,-5], k = 2, x = 2
Output: [-1,-2,-3,-4]
Explanation: 共有 4 个大小为 k = 2 的子数组。
- 对于 [-1, -2]，第 2 小的负整数是 -1。  
- 对于 [-2, -3]，第 2 小的负整数是 -2。  
- 对于 [-3, -4]，第 2 小的负整数是 -3。  
- 对于 [-4, -5]，第 2 小的负整数是 -4。
```

**示例 3**

```text
Input: nums = [-3,1,2,-3,0,-3], k = 2, x = 1
Output: [-3,0,-3,-3,-3]
Explanation: 共有 5 个大小为 k = 2 的子数组。
- 对于 [-3, 1]，第 1 小的负整数是 -3。  
- 对于 [1, 2]，不存在负整数，故美感为 0。  
- 对于 [2, -3]，第 1 小的负整数是 -3。  
- 对于 [-3, 0]，第 1 小的负整数是 -3。  
- 对于 [0, -3]，第 1 小的负整数是 -3。
```

### 约束

- `n == nums.length`
- `1 <= n <= 10^5`
- `1 <= k <= n`
- `1 <= x <= k`
- `-50 <= nums[i] <= 50`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **把每一个长度为 `k` 的子数组都完整地取出来，直接排序后找第 `x` 小的负数**（如果负数不足 `x` 个，就返回 `0`）。  

- **使用的数据结构**：  
  - `list`（列表）用来存放当前子数组的所有元素。  
  - `sorted()`（排序）相当于把这堆数字“排队”，最小的在最前面，像是把一堆书按照字母顺序摆好。  

- **为什么一定正确**：  
  1. 子数组的定义是连续的 `k` 个元素，枚举所有起始位置 `i`（`0 ≤ i ≤ n‑k`）即可遍历所有子数组。  
  2. 对每个子数组进行完整排序后，第 `x` 小的负数一定是答案，因为排序保证了“从小到大”的顺序。  

- **时间/空间复杂度**（大白话版）  
  - 对每一个子数组我们都要 **排序**，排序的代价大约是 `k log k`（想象把 `k` 本书排队，大概要花 `k log k` 步）。  
  - 子数组的数量是 `n‑k+1`，所以总时间是 ` (n‑k+1) * k log k`，最坏情况下可以写成 **O(n·k·log k)**。  
  - 只用了几个临时列表，空间最多是 `O(k)`（存放当前子数组），这在我们眼里叫 **O(k)**。

#### 代码（Python）

```python
def get_beauty_bruteforce(nums, k, x):
    n = len(nums)
    res = []                         # 用来保存每个窗口的答案
    for i in range(n - k + 1):       # 枚举所有窗口的左端点
        window = nums[i:i + k]       # 直接切片得到当前子数组
        # 只关心负数，先筛选出来再排序
        negatives = sorted([v for v in window if v < 0])
        if len(negatives) >= x:      # 负数够 x 个，取第 x 小
            res.append(negatives[x - 1])
        else:                        # 负数不足 x 个，答案是 0
            res.append(0)
    return res
```

#### 复杂度

- **时间复杂度**：`O(n·k·log k)`  
  - 想象有 `n` 本书，每本书要花 `k·log k` 的时间来排队，整体就是这么多步。  
- **空间复杂度**：`O(k)`  
  - 只存当前窗口的 `k` 个元素和若干负数，最多占用 `k` 大小的空间。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于每次都要把窗口里的数字重新排序，这在 `k` 很大的时候非常浪费。  
我们需要 **在窗口滑动时复用已有信息**，只对“进来”和“出去”的元素做少量更新。

观察题目约束：

- `nums[i]` 的取值范围很小：**-50 ≤ nums[i] ≤ 50**。  
- 只关心 **负数**，而且只需要找第 `x` 小的负数。

这两个点让我们可以使用 **计数数组（frequency array）** 来记录窗口里每个负数出现的次数。  
计数数组就像一本“字典”，下标是负数的数值（把 -50~ -1 映射到 0~49），对应的值是出现次数。

**滑动窗口 + 计数数组的核心步骤**

1. **初始化**：把前 `k` 个元素的负数计数填入 `cnt[0..49]`。  
2. **求第 x 小负数**：从最小的负数（-50）开始向右遍历计数数组，累加出现次数，第一次累计 ≥ `x` 时对应的负数就是答案。如果遍历结束仍未累计到 `x`，说明负数不足 `x` 个，答案是 `0`。  
3. **窗口右移**：  
   - 把窗口左端要移出的元素 `out` 的计数减 1（如果是负数）。  
   - 把窗口右端新进来的元素 `in` 的计数加 1（如果是负数）。  
   - 只改动这两个位置，时间是 **O(1)**。  

因为计数数组的长度固定为 **50**（负数的种类），求第 `x` 小负数的遍历最多 50 步，和 `k` 大小无关。整体时间就是 **O(n·50) = O(n)**。

#### 代码（Python）

```python
def get_beauty_optimal(nums, k, x):
    """
    sliding window + frequency array
    cnt[i] 记录数值 (i-50) 在窗口中出现的次数，i 取值 0~49 对应 -50~-1
    """
    n = len(nums)
    OFFSET = 50                     # 为了把负数映射到非负下标
    cnt = [0] * OFFSET               # 只需要 50 个格子

    # 1. 初始化前 k 个元素的计数
    for i in range(k):
        if nums[i] < 0:
            cnt[OFFSET + nums[i]] += 1   # 例如 nums[i] = -3 => cnt[47]++

    def kth_negative():
        """返回窗口内第 x 小的负数，若不足 x 个返回 0"""
        acc = 0                      # 累计出现的负数个数
        for idx in range(OFFSET):    # idx 0 对应 -50, idx 49 对应 -1
            acc += cnt[idx]
            if acc >= x:             # 第一次累计到 x，说明这里就是第 x 小
                return idx - OFFSET   # 把下标再映射回负数本身
        return 0                     # 负数不够 x 个

    ans = [kth_negative()]           # 第一个窗口的答案

    # 2. 窗口向右滑动
    for right in range(k, n):
        left = right - k              # 将要移出窗口的下标

        # 移出 left 位置的元素
        if nums[left] < 0:
            cnt[OFFSET + nums[left]] -= 1

        # 加入 right 位置的元素
        if nums[right] < 0:
            cnt[OFFSET + nums[right]] += 1

        # 计算当前窗口的第 x 小负数
        ans.append(kth_negative())

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 每个位置只进入一次、离开一次，计数更新是常数时间。  
  - 求第 `x` 小负数最多遍历 50 次（固定常数），所以整体线性。  
  - 与暴力解相比，**从 `n·k·log k` 降到 `n`**，在大数据量时快很多。

- **空间复杂度**：`O(1)`（常数空间）  
  - 只用了长度为 50 的计数数组和若干常数级别的变量，和输入规模 `n` 无关。

---

## 心得

- **核心技巧**：**利用数值范围小的特性，用固定大小的计数数组（相当于“哈希表”）配合滑动窗口**，实现 O(1) 更新和 O(常数) 查询。  
- **适用的题型**：  
  1. “滑动窗口求第 k 小/大元素”，但元素值域有限（如 `-1000~1000`）。  
  2. “窗口内出现次数超过阈值的元素”，可以用计数数组或哈希表快速判断。  
  3. “固定区间内的频率统计”，如 “求窗口内出现次数最多的数字”。  

> **解题钥匙**：**把“找第 x 小的负数”转化为“在 50 长的计数表里累计到第 x”，再配合滑动窗口让更新保持 O(1)。**

---

## 反思

- **第一反应**：直接想到遍历所有子数组、排序后取第 `x` 小——这是最自然的暴力思路。  
- **最容易踩的坑**：  
  - **负数映射**：忘记把 `-50~ -1` 映射到数组下标，会导致数组越界。  
  - **边界条件**：窗口里负数少于 `x` 时必须返回 `0`，不要忘记在 `kth_negative` 中处理。  
  - **计数数组的更新**：在滑动时一定要先减去离开的元素，再加上进来的元素，顺序不对会导致临时错误的计数。  

- **下次遇到同类题**，**第一步**就要检查**数值范围是否可以做离散化**（即把值映射到小数组），如果可以，就立刻考虑**计数数组 + 滑动窗口**的组合，而不是直接排序。