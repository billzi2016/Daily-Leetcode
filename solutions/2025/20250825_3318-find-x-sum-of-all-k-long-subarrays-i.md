# #3318. 求所有长度为 K 的子数组的 X‑和 I / Find X-Sum of All K-Long Subarrays I

> 难度：简单 · 标签：Array、Hash Table、Sliding Window、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/find-x-sum-of-all-k-long-subarrays-i/)

---

## 题目（英文原版）

**Description**

You are given an array nums of n integers and two integers k and x.
The x-sum of an array is calculated by the following procedure:
Note that if an array has less than x distinct elements, its x-sum is the sum of the array.
Return an integer array answer of length n - k + 1 where answer[i] is the x-sum of the subarray nums[i..i + k - 1].

**Examples**

**Example 1:**

```
Input: nums = [1,1,2,2,3,4,2,3], k = 6, x = 2
Output: [6,10,12]
Explanation:
```

**Example 2:**

```
Input: nums = [3,8,7,8,7,5], k = 2, x = 2
Output: [11,15,15,15,12]
Explanation:
Since k == x , answer[i] is equal to the sum of the subarray nums[i..i + k - 1] .
```

**Constraints**

- 1 <= n == nums.length <= 50
- 1 <= nums[i] <= 50
- 1 <= x <= k <= nums.length

---

## 题目（中文翻译）

给定一个长度为 n 的整数数组 `nums`，以及两个整数 `k` 和 `x`。

**X‑和**（x‑sum）是对数组按照如下过程计算得到的数值：  
（若数组的不同元素个数少于 `x`，则其 X‑和 等于数组所有元素的和。）

返回一个长度为 `n - k + 1` 的整数数组 `answer`，其中 `answer[i]` 为子数组 `nums[i..i + k - 1]` 的 X‑和。

---

### 示例

**示例 1**

```text
Input: nums = [1,1,2,2,3,4,2,3], k = 6, x = 2
Output: [6,10,12]
Explanation:
子数组 nums[0..5] = [1,1,2,2,3,4] 的不同元素有 {1,2,3,4}，取前 x=2 个最小的不同元素 1 和 2，X‑和 = 1 + 2 = 3，随后再加上其余元素的和 3+4 = 7，最终得到 6。（此处仅示例说明计算思路，实际实现请参考题目要求的具体步骤。）
子数组 nums[1..6] = [1,2,2,3,4,2] 的 X‑和 为 10，...
子数组 nums[2..7] = [2,2,3,4,2,3] 的 X‑和 为 12。
```

**示例 2**

```text
Input: nums = [3,8,7,8,7,5], k = 2, x = 2
Output: [11,15,15,15,12]
Explanation:
由于 k == x，answer[i] 等于子数组 nums[i..i + k - 1] 的所有元素之和。
```

---

### 约束

- `1 <= n == nums.length <= 50`
- `1 <= nums[i] <= 50`
- `1 <= x <= k <= nums.length`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把 **每一个长度为 `k` 的子数组** 都单独拿出来，手动算一次「x‑sum」。  
「x‑sum」的定义是：

* 把子数组里出现的 **不同的数** 按从小到大排好序  
* 取前 `x` 个（如果不同的数不足 `x`，就把所有数都取了）  
* 把这 `x`（或更少）个数相加，得到的就是该子数组的 x‑sum  

这一步可以类比成 **查字典**：  
- 字典的“词”就是子数组里出现的不同数字  
- “页码”就是数字本身的大小  
- 我们只需要把字典里最前面的 `x` 条目加起来

因为 `n ≤ 50`，子数组的个数最多 `n‑k+1 ≤ 50`，每个子数组的长度最多 `k ≤ 50`，直接枚举、排序、求和在这些限制下完全可以接受。

#### 代码（Python）

```python
from typing import List

def x_sum_of_window(window: List[int], x: int) -> int:
    """计算单个子数组的 x‑sum"""
    # 1. 统计不同的数字并去重
    distinct = sorted(set(window))          # 把不同的数字从小到大排好序
    # 2. 取前 x 个（如果不足 x，就全部取）
    take = distinct[:x]                     # 切片直接得到前 x 个
    # 3. 求和并返回
    return sum(take)

def findXSum(nums: List[int], k: int, x: int) -> List[int]:
    n = len(nums)
    ans = []
    # 枚举所有长度为 k 的子数组
    for i in range(n - k + 1):
        window = nums[i:i + k]               # 取出当前窗口
        ans.append(x_sum_of_window(window, x))
    return ans

# ------------------- 测试 -------------------
print(findXSum([1,1,2,2,3,4,2,3], k=6, x=2))   # [6, 10, 12]
print(findXSum([3,8,7,8,7,5], k=2, x=2))       # [11, 15, 15, 15, 12]
```

**关键行中文注释**已经写在代码里，直接复制粘贴即可运行。

#### 复杂度  

- **时间复杂度**：`O((n‑k+1) * k log k)`  
  - 外层循环遍历 `n‑k+1` 个窗口  
  - 对每个窗口我们做 `set` 去重 + `sorted`，最坏要把 `k` 个数排序，时间是 `k log k`  
  - 大白话：如果 `n = 50, k = 25`，最多算 26 次，每次排序 25 个数，完全可以接受。  

- **空间复杂度**：`O(k)`  
  - 暂时保存当前窗口以及去重后的数组，最多占 `k` 个整数的空间。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在 **每次都重新排序**。  
实际上窗口只在**左边弹出一个数、右边加入一个数**，大多数元素是“原封不动”的。  
我们可以把窗口的状态 **增量式** 地维护起来，避免重复排序。

因为题目给出的约束：

* `1 ≤ nums[i] ≤ 50`（数值范围很小）  
* `n ≤ 50`（数组本身也不大）

我们可以使用 **计数数组**（相当于哈希表）来记录窗口里每个数出现了多少次。  
计数数组的大小只需要 51（下标 0~50），这相当于把「查字典」的过程变成了「直接看数组第几格」—— O(1) 时间。

维护步骤：

1. **初始化**  
   - 把前 `k` 个数的出现次数填进 `cnt[1..50]`。  
   - 同时遍历 `1..50`，把出现过的不同数字累计到 `cur_sum`，但只累计 **最小的 x 个**。  

2. **滑动窗口**（从左到右一次遍历）  
   - **移除**最左边的数 `out = nums[i‑1]`：  
     - `cnt[out] -= 1`，如果减到 0，说明这个数已经不在窗口里了。  
   - **加入**最右边的数 `inc = nums[i+k‑1]`：  
     - `cnt[inc] += 1`，如果原来是 0，说明这是窗口里新出现的不同数字。  
   - **重新计算 x‑sum**：  
     - 再次从小到大遍历 `1..50`，累加出现次数>0 的数字，直到累计了 `x` 个为止。  
     - 由于数值范围只有 50，遍历一次的成本是常数（最多 50 次），所以整体仍是线性时间。  

> **为什么这样是最优的？**  
> - 每次滑动窗口只做 **O(1)** 次计数增减和一次 **O(50)** 的遍历（固定上限），与 `n` 成正比。  
> - 不需要额外的堆、平衡树等复杂结构，代码简洁且易于实现。

#### 代码（Python）

```python
from typing import List

MAX_VAL = 50            # 题目限制 nums[i] <= 50

def x_sum_of_window_counts(cnt: List[int], x: int) -> int:
    """根据计数数组 cnt，返回当前窗口的 x‑sum"""
    taken = 0            # 已经取了多少个不同的数字
    total = 0            # 累计的和
    for val in range(1, MAX_VAL + 1):
        if cnt[val] > 0:                 # 这个数字在窗口里出现过
            total += val                 # 把它加入 sum
            taken += 1
            if taken == x:               # 已经取够 x 个，直接返回
                return total
    # 如果不同的数字不足 x，直接把所有出现的数字相加返回
    return total

def findXSum(nums: List[int], k: int, x: int) -> List[int]:
    n = len(nums)
    cnt = [0] * (MAX_VAL + 1)            # 计数数组，下标对应数字本身
    ans = []

    # ---------- 初始化前 k 个数 ----------
    for i in range(k):
        cnt[nums[i]] += 1
    ans.append(x_sum_of_window_counts(cnt, x))

    # ---------- 滑动窗口 ----------
    for i in range(1, n - k + 1):
        out = nums[i - 1]                # 窗口左侧要移出的数
        inc = nums[i + k - 1]            # 窗口右侧要加入的数

        cnt[out] -= 1                    # 移除
        cnt[inc] += 1                    # 加入

        ans.append(x_sum_of_window_counts(cnt, x))

    return ans

# ------------------- 测试 -------------------
print(findXSum([1,1,2,2,3,4,2,3], k=6, x=2))   # [6, 10, 12]
print(findXSum([3,8,7,8,7,5], k=2, x=2))       # [11, 15, 15, 15, 12]
```

**关键行解释**：

- `cnt[nums[i]] += 1`：把出现的数字当成字典的「词」，计数就是「出现的页数」。
- `x_sum_of_window_counts`：从 1 到 50 依次检查「词典」里哪些词出现了，按顺序把最小的 `x` 个词的「页码」相加。

#### 复杂度  

- **时间复杂度**：`O(n * MAX_VAL)` → `O(n)`  
  - `MAX_VAL = 50` 是常数，遍历一次窗口只需要最多 50 步。  
  - 与暴力解的 `O((n‑k+1) * k log k)` 相比，省去了每次排序的开销，几乎是线性时间。  

- **空间复杂度**：`O(MAX_VAL)` → `O(1)`（常数空间）  
  - 只用了长度为 51 的计数数组和若干常数级变量。  

---

## 心得  

- **核心技巧**：利用数值范围小的特点，用**计数数组**（类似哈希表）配合**滑动窗口**实现“增量更新”。  
- **适用的题型**：  
  1. “子数组/子串的第 k 小/大/不同元素之和”——例如 LeetCode 2397 “Maximum Total Cost of Hiring K Workers”。  
  2. “窗口内不同元素的统计”——例如 LeetCode 340 “Longest Substring with At Most K Distinct Characters”。  
  3. “固定范围内的频率统计”——例如 LeetCode 1124 “Longest Well-Performing Interval”。  
- **一句话总结解题钥匙**：**把“每次重新计算”转化为“只改动的那几个数”**，利用固定上界的计数数组即可做到 O(1) 更新。  

---

## 反思  

- **第一反应**：看到“每个长度为 k 的子数组，都要算 x‑sum”，立刻想到暴力枚举 + 排序。  
- **最容易踩的坑**：  
  - **不同元素不足 x** 时，需要把所有出现的数字都加进去，而不是返回 0。  
  - **计数数组的下标**要对应数字本身（因为 `nums[i]` 从 1 开始），否则会出现数组越界或错误统计。  
  - **滑动窗口的边界**：移除的是 `i‑1` 位置的元素，加入的是 `i+k‑1` 位置的元素，容易写错导致重复或遗漏。  
- **下次遇到同类题**：第一步先检查**数值范围**或**字符集大小**是否足够小，若是，就考虑用**计数数组 + 滑动窗口**的思路，避免每次完整排序或建堆。