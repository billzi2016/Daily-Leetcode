# #410. 拆分数组的最大子数组和 / Split Array Largest Sum

> 难度：困难 · 标签：Array、Binary Search、Dynamic Programming、Greedy、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/split-array-largest-sum/)

---

## 题目（英文原版）

**Description**

Given an integer array nums and an integer k, split nums into k non-empty subarrays such that the largest sum of any subarray is minimized.
Return the minimized largest sum of the split.
A subarray is a contiguous part of the array.

**Examples**

**Example 1:**

```
Input: nums = [7,2,5,10,8], k = 2
Output: 18
Explanation: There are four ways to split nums into two subarrays.
The best way is to split it into [7,2,5] and [10,8], where the largest sum among the two subarrays is only 18.
```

**Example 2:**

```
Input: nums = [1,2,3,4,5], k = 2
Output: 9
Explanation: There are four ways to split nums into two subarrays.
The best way is to split it into [1,2,3] and [4,5], where the largest sum among the two subarrays is only 9.
```

**Constraints**

- 1 <= nums.length <= 1000
- 0 <= nums[i] <= 106
- 1 <= k <= min(50, nums.length)

---

## 题目（中文翻译）

**题目描述**  
给定一个整数数组 `nums` 和一个整数 `k`，将 `nums` 拆分成 `k` 个非空子数组（subarray），要求所有子数组中和最大的那个子数组的和 **最小化**。返回拆分后能够得到的最小的最大子数组和。  
子数组是数组中连续的一段。

**示例 1**  
输入：`nums = [7,2,5,10,8]`, `k = 2`  
输出：`18`  
解释：将数组拆分成两个子数组共有四种方式，最佳的拆分方式是 `[7,2,5]` 与 `[10,8]`，此时两个子数组的和的最大值为 `18`。

**示例 2**  
输入：`nums = [1,2,3,4,5]`, `k = 2`  
输出：`9`  
解释：将数组拆分成两个子数组共有四种方式，最佳的拆分方式是 `[1,2,3]` 与 `[4,5]`，此时两个子数组的和的最大值为 `9`。

**约束条件**  
- `1 <= nums.length <= 1000`  
- `0 <= nums[i] <= 10^6`  
- `1 <= k <= min(50, nums.length)`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可能的切分方式都枚举出来**，然后把每种切法对应的「子数组最大和」算出来，取最小值。  
- **数据结构**：我们只需要用 Python 的 `list` 保存原数组，另外用一个临时的 `list` 保存每次切分后每段的和。可以把「把数组切成 k 段」想象成「给数组里挑 k‑1 条切线」，就像在一根绳子上随意打 k‑1 个结。  
- **为什么正确**：因为我们遍历了**所有**合法的切法，答案一定会出现在这些候选里。只要取最小的「子数组最大和」，就得到题目要求的最优值。  

> 暴力的核心难点是**枚举切法**。把 `n` 个元素切成 `k` 段等价于在 `n‑1` 条可能的切口中挑 `k‑1` 条。组合数为 `C(n‑1, k‑1)`，当 `n` 较大时会爆炸。

#### 代码（Python）

```python
from itertools import combinations
from typing import List

def splitArray_bruteforce(nums: List[int], k: int) -> int:
    n = len(nums)
    # 所有切口的下标（切口在 i 与 i+1 之间），范围是 0 ~ n-2
    cut_positions = list(range(n - 1))
    best = float('inf')                     # 记录全局最小的「最大子数组和」

    # 从 n-1 条切口里任选 k-1 条（即选出 k-1 个切点）
    for cuts in combinations(cut_positions, k - 1):
        cuts = (-1,) + cuts + (n - 1,)      # 加上左右边界，方便统一计算
        cur_max = 0                         # 当前切法的子数组最大和
        # 依次计算每段的和
        for i in range(len(cuts) - 1):
            left = cuts[i] + 1              # 本段左端点（含）
            right = cuts[i + 1] + 1         # 本段右端点（含），因为切口在 i 与 i+1 之间
            seg_sum = sum(nums[left:right]) # 直接求和（O(段长)）
            cur_max = max(cur_max, seg_sum)
        best = min(best, cur_max)           # 取最小的「最大子数组和」
    return best
```

> **关键行注释**  
> - `combinations(cut_positions, k - 1)`: 把所有切口两两组合，枚举每一种切法。  
> - `cuts = (-1,) + cuts + (n - 1,)`: 把左、右边界当作「隐形切口」加入，后面算子数组时就不需要特判首段和末段。  
> - `sum(nums[left:right])`: 直接遍历求和，虽然会重复计算，但保持代码最直观。

#### 复杂度  

- **时间复杂度**：`O(C(n‑1, k‑1) * n)`  
  - `C(n‑1, k‑1)` 是组合数，表示所有切法的数量。  
  - 对每一种切法我们要遍历整个数组求和，最坏情况是 `O(n)`。  
  - 当 `n=1000, k=50` 时，这个数字天文般大，根本跑不完。  
  - 用大白话说，就是「先把所有可能的切法写下来（可能上万亿），每写完一张都要再算一遍总和」，所以完全不可行。

- **空间复杂度**：`O(k)`  
  - 只保存当前切法的切点列表，最多 `k‑1` 个。其余都是常数级别的临时变量。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**枚举切法**。我们需要一种不枚举、直接「猜」答案的办法。  
观察题目可以发现：

1. **答案的取值范围是有界的**  
   - 最小可能的「最大子数组和」至少是数组中最大的那个元素 `max(nums)`（因为子数组不能拆分元素）。  
   - 最大可能的「最大子数组和」就是整个数组的和 `sum(nums)`（把所有元素放进同一个子数组）。  

2. **如果我们「猜」一个阈值 `mid`，可以快速判断是否能把数组划分成 ≤ k 段，使得每段的和都 ≤ mid**。  
   - 这一步只需要一次线性扫描：从左到右累计当前段的和，一旦加上下一个元素会超过 `mid`，就必须在这里**切断**，开启新段。  
   - 这种「尽量把元素塞进当前段」的策略是**贪心**的，因为只要不超过 `mid`，把更多元素放进当前段总是更有利于减少段数。  

3. **二分搜索**（Binary Search）  
   - 由于「能否划分」是**单调**的：阈值 `mid` 越大，越容易划分（段数不增），阈值越小，划分越困难。  
   - 因此我们可以在 `[max(nums), sum(nums)]` 这条数轴上做二分，找最小的 `mid` 使得「可以划分成 ≤ k 段」成立。  

下面把关键概念逐一解释：

- **前缀和**（Prefix Sum）  
  在本题的贪心判断里不需要额外的前缀和数组，只要用一个变量 `cur_sum` 累加即可。这里提前缀和只是为了让读者了解「把数组的累计和预先算好」的常见技巧。

- **贪心**（Greedy）  
  把「尽可能多装进当前子数组」想象成「装满背包」——只要不超重，就一直往里放，等到再放就会超重时才换新背包。这样得到的背包（子数组）数是最少的。

- **二分搜索**  
  把「找最小可行阈值」看作「在一条有序的数轴上找第一个满足条件的点」。我们每次取中点 `mid` 检查可行性，然后把搜索区间缩小到左半或右半。

#### 代码（Python）

```python
from typing import List

def splitArray(nums: List[int], k: int) -> int:
    """
    二分 + 贪心
    返回把数组分成 k 段后，所有段的最大和的最小可能值。
    """
    # 1. 确定搜索区间的左右端点
    left = max(nums)          # 任何合法划分的最大子数组和都不可能小于这个值
    right = sum(nums)         # 把所有元素放进同一个子数组时的和，是上界

    # 2. 二分搜索最小的可行阈值
    while left < right:       # 区间长度大于 1 时继续
        mid = (left + right) // 2   # 取中点，尝试作为「最大子数组和」的上限

        # 3. 贪心检查：能否在阈值 mid 下用不超过 k 段把数组划分完？
        needed = 1            # 至少需要 1 段（从第一个元素开始）
        cur_sum = 0           # 当前段的累计和
        for num in nums:
            # 若把 num 加进去会超出阈值，就必须另起一段
            if cur_sum + num > mid:
                needed += 1   # 开启新段
                cur_sum = num # 当前段重新计数，从 num 开始
            else:
                cur_sum += num

        # 4. 根据需要的段数决定搜索方向
        if needed <= k:       # 段数不超过 k，说明 mid 可能太大，左移收紧上界
            right = mid
        else:                 # 段数 > k，mid 太小，需要增大阈值
            left = mid + 1

    # 循环结束时 left == right，就是最小的可行阈值
    return left
```

> **关键行注释**  
> - `left = max(nums)`: 把「最大单个元素」当作最小可能答案，防止二分时出现不合法的阈值。  
> - `if cur_sum + num > mid:`: 这里实现了「装满背包」的贪心判断，一旦超过阈值就必须换新背包（新子数组）。  
> - `if needed <= k:`: 判断「是否可以在 k 段以内完成划分」，决定二分的收敛方向。  

#### 复杂度  

- **时间复杂度**：`O(n * log(S))`  
  - `n` 是数组长度（最多 1000），每一次二分都要遍历一次数组做贪心检查。  
  - `S = sum(nums) - max(nums)`（大概是答案搜索空间的大小），对数 `log(S)` 表示二分的轮数。  
  - 用大白话说，就是「先把可能的答案范围压缩到一条线段，再每次把线段砍一半，最多砍 log 次，每次砍完都要跑一遍数组」，整体运行很快，完全能在 1 秒内结束。

- **空间复杂度**：`O(1)`  
  - 只用了常数个额外变量 `left, right, mid, needed, cur_sum`，不随 `n` 增长。

---

## 心得

- **核心技巧**：**二分搜索 + 贪心判断**。  
  这是一种“**单调性 + 可行性检查**”的典型思路，常见于「把问题转化为在数轴上找最小满足条件的点」的题目。

- **适用的题型**  
  1. *Split Array Largest Sum*（本题）  
  2. *Capacity To Ship Packages Within D Days*（把包裹装进船，要求最小船容量）  
  3. *Find Minimum Time to Complete Trips*（在给定时间内完成若干任务的最小时间）  

- **一句话总结解题钥匙**：  
  > **把“最小化最大值”转化为“判断阈值是否可行”，再用二分快速定位最小可行阈值**。

---

## 反思

- **第一反应**：想到枚举所有切法，直接计算最大子数组和，没注意到搜索空间的单调性。  
- **最容易踩的坑**  
  1. **阈值下界写错**：如果直接把左端点设为 `0`，会导致贪心判断在 `mid` 小于数组最大元素时无限切段，甚至出现死循环。正确做法是 `left = max(nums)`。  
  2. **贪心计数遗漏最后一段**：在遍历结束后一定要把当前段计入（本实现通过 `needed` 初始为 1 并在超限时才 `+=1`，自然涵盖最后一段）。  
  3. **二分循环条件**：`while left < right` 而不是 `<=`，防止死循环；收敛时 `right = mid` 而不是 `mid - 1`（因为 `mid` 已经是可行的）。  

- **下次遇到同类题的第一步**：  
  > **先判断答案是否具有单调性（阈值越大越容易实现），如果有，就立刻想到二分 + 线性可行性检查**。这样可以迅速从暴力思路跳到高效解法。