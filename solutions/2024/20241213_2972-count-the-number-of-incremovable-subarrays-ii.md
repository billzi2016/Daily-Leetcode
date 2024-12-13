# #2972. 统计可移除后严格递增的子数组数量 II / Count the Number of Incremovable Subarrays II

> 难度：困难 · 标签：Array、Two Pointers、Binary Search · [LeetCode 链接](https://leetcode.com/problems/count-the-number-of-incremovable-subarrays-ii/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array of positive integers nums.
A subarray of nums is called incremovable if nums becomes strictly increasing on removing the subarray. For example, the subarray [3, 4] is an incremovable subarray of [5, 3, 4, 6, 7] because removing this subarray changes the array [5, 3, 4, 6, 7] to [5, 6, 7] which is strictly increasing.
Return the total number of incremovable subarrays of nums.
Note that an empty array is considered strictly increasing.
A subarray is a contiguous non-empty sequence of elements within an array.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,4]
Output: 10
Explanation: The 10 incremovable subarrays are: [1], [2], [3], [4], [1,2], [2,3], [3,4], [1,2,3], [2,3,4], and [1,2,3,4], because on removing any one of these subarrays nums becomes strictly increasing. Note that you cannot select an empty subarray.
```

**Example 2:**

```
Input: nums = [6,5,7,8]
Output: 7
Explanation: The 7 incremovable subarrays are: [5], [6], [5,7], [6,5], [5,7,8], [6,5,7] and [6,5,7,8].
It can be shown that there are only 7 incremovable subarrays in nums.
```

**Example 3:**

```
Input: nums = [8,7,6,6]
Output: 3
Explanation: The 3 incremovable subarrays are: [8,7,6], [7,6,6], and [8,7,6,6]. Note that [8,7] is not an incremovable subarray because after removing [8,7] nums becomes [6,6], which is sorted in ascending order but not strictly increasing.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 109

---

## 题目（中文翻译）

给定一个下标从 0 开始的正整数数组 `nums`。  
如果在删除某个子数组（subarray）后，剩余的数组严格递增（strictly increasing），则称该子数组为 **可移除子数组**（incremovable subarray）。例如，子数组 `[3, 4]` 是数组 `[5, 3, 4, 6, 7]` 的可移除子数组，因为删除它后数组变为 `[5, 6, 7]`，而 `[5, 6, 7]` 是严格递增的。  

返回 `nums` 中所有可移除子数组的总数。  
注意，空数组被视为严格递增。  
子数组是数组中连续的、非空的元素序列。

**示例 1**  
``` 
Input: nums = [1,2,3,4]
Output: 10
Explanation: 这 10 个可移除子数组分别是: 
[1], [2], [3], [4], 
[1,2], [2,3], [3,4], 
[1,2,3], [2,3,4], 以及 [1,2,3,4]。  
删除其中任意一个子数组后，`nums` 都会变成严格递增。  
注意不能选择空子数组。
```

**示例 2**  
``` 
Input: nums = [6,5,7,8]
Output: 7
Explanation: 这 7 个可移除子数组分别是: 
[5], [6], [5,7], [6,5], [5,7,8], [6,5,7] 和 [6,5,7,8]。  
可以证明 `nums` 中仅有这 7 个可移除子数组。
```

**示例 3**  
``` 
Input: nums = [8,7,6,6]
Output: 3
Explanation: 这 3 个可移除子数组分别是: 
[8,7,6], [7,6,6] 和 [8,7,6,6]。  
注意 `[8,7]` 不是可移除子数组，因为删除 `[8,7]` 后数组变为 `[6,6]`，虽然是升序排列，但并非严格递增。
```

**约束条件**  
- `1 <= nums.length <= 10^5`  
- `1 <= nums[i] <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**枚举所有可能的子数组**，把它们从原数组中删掉，然后检查剩下的数组是否严格递增。  

- **枚举子数组**：用两个循环 `l`、`r`（`0 ≤ l ≤ r < n`）表示要删除的子数组 `nums[l…r]`。  
- **检查剩余数组**：把左边的前缀 `nums[0…l‑1]` 和右边的后缀 `nums[r+1…n‑1]` 拼在一起，顺序遍历一次，判断每相邻的两个数是否满足 “前一个 < 后一个”。如果整个遍历都满足，则说明删除 `[l, r]` 后数组是严格递增的。  

> **类比**：把数组想成一本排好序的书的章节编号。我们要把连续的几页（子数组）撕掉，看看剩下的章节编号是否仍然从小到大。只要每相邻的章节号仍然递增，就算成功。

这个方法一定能得到正确答案，因为我们把**所有**合法的子数组都尝试了一遍，凡是满足条件的都会被计数。

#### 代码（Python）

```python
def count_incremovable_subarrays_bruteforce(nums):
    n = len(nums)
    ans = 0

    # 枚举所有非空子数组 [l, r]
    for l in range(n):
        for r in range(l, n):
            # 检查删除后是否严格递增
            ok = True
            prev = None                       # 用来记录上一个保留下来的元素

            # 先遍历左侧前缀
            for i in range(l):
                if prev is not None and prev >= nums[i]:
                    ok = False
                    break
                prev = nums[i]

            # 再遍历右侧后缀（如果左侧已经不满足，直接跳过）
            if ok:
                for i in range(r + 1, n):
                    if prev is not None and prev >= nums[i]:
                        ok = False
                        break
                    prev = nums[i]

            if ok:
                ans += 1

    return ans
```

> 关键行中文注释已经写在代码里，直接可以运行。  

#### 复杂度  

- **时间复杂度**：`O(n³)`  
  - 外层两层循环枚举子数组有 `O(n²)` 种可能。  
  - 对每一种子数组，我们要遍历最多 `n` 次来检查递增性，所以总共是 `n² × n = n³`。  
  - **大白话**：如果数组长度是 1000，程序大概要跑 1000³ = 10⁹ 次小操作，显然会超时。  

- **空间复杂度**：`O(1)`  
  - 只用了常数个额外变量（`prev`、`ok`），不随 `n` 增长。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**重复检查相同的前缀或后缀**。我们可以提前算好哪些前缀本身已经是严格递增的，哪些后缀本身已经是严格递增的，然后用**双指针**一次遍历就把所有合法子数组统计完。

1. **先找最长递增前缀**  
   - 从左往右扫描，记录下标 `x`，使得 `nums[0…x]` 已经严格递增，而 `x+1` 位置出现了下降或相等。  
   - 这相当于说：只要我们保留的左侧部分不超过 `x`，左侧一定是递增的。  

2. **再找最短递增后缀**  
   - 从右往左扫描，找到最小下标 `y`，使得 `nums[y…n‑1]` 已经严格递增。  
   - 只要我们保留的右侧部分从 `y` 开始或更靠右，右侧一定是递增的。  

3. **双指针遍历**  
   - 用指针 `i` 表示我们**保留的左侧的最后一个元素**的下标（`i = -1` 表示左侧为空）。`i` 的合法范围是 `-1 … x`。  
   - 用指针 `j` 表示我们**保留的右侧的第一个元素**的下标，初始设为 `y`。  
   - 对每个 `i`，我们要让 `nums[i] < nums[j]`（如果 `i = -1` 或 `j = n`，条件自动满足），因为左侧的最大值必须小于右侧的最小值，才能拼接成整体递增。  
   - 当 `i` 增大时，左侧的最大值只会变大，**`j` 只会向右移动**（不会左移），这正好符合双指针的“单调性”。  
   - 找到最小的满足条件的 `j` 后，**右侧可以任选一个起点** `k`，只要 `k ≥ j`（包括 `k = n`，即右侧全部删掉）。每一个 `k` 对应一种不同的被删除子数组。  
   - 因此，对于当前的 `i`，合法子数组的数量是 `n - j + 1`（从 `j` 到 `n` 共这么多选择）。把这些加起来就是答案。  

> **类比**：想象一条河，两边各有一段已经排好序的石子（左侧递增前缀、右侧递增后缀）。我们要在河中间挑选一段石子全部移走，使得左边的最后一块石子仍然小于右边的第一块石子。随着左边的石子逐渐增多（`i` 向右），右边的起始点只能往右移动（`j` 单调不减），于是只需要一次遍历就能算出所有可能的“移走的段”。  

#### 代码（Python）

```python
def count_incremovable_subarrays(nums):
    n = len(nums)

    # 1️⃣ 计算最长递增前缀的右端点 x
    x = 0
    while x + 1 < n and nums[x] < nums[x + 1]:
        x += 1          # 前缀仍然递增
    # 现在 nums[0..x] 是递增的，x 可能是 n-1（全数组递增）

    # 2️⃣ 计算最短递增后缀的左端点 y
    y = n - 1
    while y - 1 >= 0 and nums[y - 1] < nums[y]:
        y -= 1          # 后缀仍然递增
    # 现在 nums[y..n-1] 是递增的，y 可能是 0

    ans = 0
    j = y               # j 只会向右移动

    # 3️⃣ 双指针遍历 i（左侧保留的最后一个元素）
    # i = -1 表示左侧完全为空，这也是合法的起点
    for i in range(-1, x + 1):
        # 当 i != -1 且 j < n 时，确保左侧最大值 < 右侧最小值
        while j < n and i != -1 and nums[i] >= nums[j]:
            j += 1      # 右侧起点必须右移，才能满足递增

        # 此时 j 要么已经到 n（右侧全部删掉），要么满足 nums[i] < nums[j]
        # 右侧可以从 j 开始任意选择一个起点 k（k >= j），包括 k = n（空后缀）
        ans += n - j + 1   # 计数：从 j 到 n 共多少种选择

    return ans
```

> **关键行解释**  
> - `while x + 1 < n and nums[x] < nums[x + 1]: x += 1`：一步步扩展左侧递增前缀。  
> - `while y - 1 >= 0 and nums[y - 1] < nums[y]: y -= 1`：一步步收缩右侧递增后缀。  
> - `while j < n and i != -1 and nums[i] >= nums[j]: j += 1`：如果左侧最大值不小于右侧最小值，就把右侧起点往右推。  
> - `ans += n - j + 1`：右侧可以选 `j, j+1, …, n`（其中 `n` 表示空后缀），每一种对应一种被删子数组。  

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 前缀、后缀的扫描各一次 `O(n)`。  
  - 双指针循环里，`i` 最多走 `x+2 ≤ n+1` 步，`j` 只向右移动至 `n`，两者总共也最多走 `2n` 步。  
  - **大白话**：数组有多长，就只需要线性时间跑几遍，几乎瞬间就能得到答案。  

- **空间复杂度**：`O(1)`  
  - 只用了若干整数变量（`x, y, i, j, ans`），不随 `n` 增长。  

---

## 心得  

- **核心技巧**：利用**前缀/后缀的单调性 + 双指针**一次遍历统计所有满足 “左侧最大 < 右侧最小” 的区间。  
- **适用题型**  
  1. “删除一个子数组后，使剩余数组满足某种单调性” 类题（如 *Count the Number of Incremovable Subarrays I*）。  
  2. “在数组中找满足左边 ≤ 右边的分割点” 的双指针或前缀后缀题目（如 *Maximum Subarray Sum After One Deletion*）。  
- **一句话总结**：**把数组拆成“递增的左段 + 被删的中段 + 递增的右段”，左段的最大值必须小于右段的最小值，用单调双指针一次遍历即可把所有合法中段枚举完。**  

---

## 反思  

- **第一反应**：看到“删除子数组后剩下的要严格递增”，本能想到**枚举子数组**并逐个验证。  
- **最容易踩的坑**  
  - 忘记**空后缀**（即把右侧全部删掉）也是一种合法选择，需要在计数时把 `k = n` 包进去。  
  - 边界 `i = -1`（左侧为空）或 `j = n`（右侧为空）时的比较要特殊处理，否则会出现数组越界或错误的比较。  
  - 题目明确**子数组不能为空**，但**整个数组可以被全部删掉**，这两点要在计数时区分。  
- **下次遇到同类题**：第一步先**检查前缀和后缀的单调性**，把问题转化为“左最大 < 右最小”，然后考虑**双指针或二分搜索**把区间快速定位。这样可以立刻从 `O(n³)` 跳到 `O(n)`。