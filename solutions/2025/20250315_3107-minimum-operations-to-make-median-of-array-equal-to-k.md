# #3107. 使数组的中位数等于 K 的最少操作次数 / Minimum Operations to Make Median of Array Equal to K

> 难度：中等 · 标签：Array、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/minimum-operations-to-make-median-of-array-equal-to-k/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and a non-negative integer k. In one operation, you can increase or decrease any element by 1.
Return the minimum number of operations needed to make the median of nums equal to k.
The median of an array is defined as the middle element of the array when it is sorted in non-decreasing order. If there are two choices for a median, the larger of the two values is taken.

**Examples**

**Example 1:**

```
Input: nums = [2,5,6,8,5], k = 4
Output: 2
Explanation:
We can subtract one from nums[1] and nums[4] to obtain [2, 4, 6, 8, 4] . The median of the resulting array is equal to k .
```

**Example 2:**

```
Input: nums = [2,5,6,8,5], k = 7
Output: 3
Explanation:
We can add one to nums[1] twice and add one to nums[2] once to obtain [2, 7, 7, 8, 5] .
```

**Example 3:**

```
Input: nums = [1,2,3,4,5,6], k = 4
Output: 0
Explanation:
The median of the array is already equal to k .
```

**Constraints**

- 1 <= nums.length <= 2 * 105
- 1 <= nums[i] <= 109
- 1 <= k <= 109

---

## 题目（中文翻译）

给定一个整数数组 `nums` 和一个非负整数 `k`。一次 **操作**（operation）可以将任意元素增加或减少 `1`。  
返回使 `nums` 的 **中位数**（median）等于 `k` 所需的最少操作次数。  

**中位数** 的定义如下：将数组按**非递减顺序**（non-decreasing order）排序后，位于中间位置的元素即为中位数；如果数组长度为偶数，则取两个中间元素中较大的那个。  

### 示例

#### 示例 1
```
Input: nums = [2,5,6,8,5], k = 4
Output: 2
Explanation:
我们可以将 `nums[1]` 和 `nums[4]` 各减去 1，得到 [2, 4, 6, 8, 4]。此时数组的中位数等于 k。
```

#### 示例 2
```
Input: nums = [2,5,6,8,5], k = 7
Output: 3
Explanation:
我们可以把 `nums[1]` 加 1 两次，再把 `nums[2]` 加 1 一次，得到 [2, 7, 7, 8, 5]。
```

#### 示例 3
```
Input: nums = [1,2,3,4,5,6], k = 4
Output: 0
Explanation:
数组的中位数已经等于 k，无需任何操作。
```

### 约束条件
- `1 <= nums.length <= 2 * 10^5`
- `1 <= nums[i] <= 10^9`
- `1 <= k <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是 **把所有元素都改成 k**，这样数组的中位数一定是 k。  
实现上可以：

1. 对数组 `nums` 进行一次遍历。  
2. 对每个元素 `x`，计算把它改成 `k` 需要的步数 `abs(x - k)`（因为一次操作只能把数字加 1 或减 1）。  
3. 把所有步数加起来，就是一种可行的操作次数。

> **为什么这种方法一定能得到答案？**  
> 把每个数都改成 `k`，数组变成 `[k, k, …, k]`，显然中位数就是 `k`，所以一定满足题目要求。  

> **为什么它不是最优的？**  
> 实际上我们并不需要把 **所有** 元素都改成 `k`，只要保证 **左边的数 ≤ k**、**右边的数 ≥ k**，中位数就已经是 `k`。  
> 把不必要的元素也改成 `k` 会产生多余的操作次数。

> **复杂度大概是多大？**  
> 需要遍历 `n` 个元素，计算 `abs`，时间是 `O(n)`；  
> 但我们还要 **把数组排序**（因为题目要求的是“排序后中位数”），排序的代价是 `O(n log n)`。  
> 所以整体是 **`O(n log n)`**，空间只用了常数个额外变量 **`O(1)`**。  
> 这里的 `O(n log n)` 可以想象成“把 `n` 本书排好序，需要 `n` 本书的 `log n` 倍的时间”，比起 `O(n²)`（每本书和每本书都比较一次）要快很多，但仍然不是最省操作数的解法。

#### 代码（Python）

```python
def min_operations_bruteforce(nums, k):
    # 1. 先把数组排序，方便找中位数的位置
    nums.sort()                         # O(n log n)

    # 2. 把每个数都改成 k，累计操作次数
    ops = 0
    for x in nums:                      # O(n)
        ops += abs(x - k)                # 每次操作只能把数字 +-1，abs 表示需要的步数
    return ops
```

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - `n log n` 来自排序，遍历本身是线性的 `O(n)`。  
- **空间复杂度**：`O(1)`（不计排序使用的原地排序空间）  

---

### 2. 最优解  

#### 思路  

从暴力思路可以看到：**并不是所有元素都必须改成 k**，只要保证排序后中位数位置的数等于 k，且左侧所有数 **不大于** k、右侧所有数 **不小于** k，就已经满足条件。  

**找出瓶颈**  
- 暴力解把每个元素都改成 k，导致对已经满足条件的元素也浪费了操作。  
- 实际上，只需要处理 **“违背”** 条件的元素：  
  - **左半部分**（下标 `< mid`）如果出现 **大于 k** 的数，需要把它 **降到 k**。  
  - **右半部分**（下标 `≥ mid`）如果出现 **小于 k** 的数，需要把它 **升到 k**。  
- 中位数本身（下标 `mid`）如果不等于 k，只需要把它改到 k（这一步自然被上面的两段代码覆盖）。

**一步步推导**  

1. **排序**：先把数组升序排列，便于定位左/右半部分以及中位数。  
2. **确定中位数下标**：`mid = n // 2`（整数除法），因为题目规定“偶数长度取较大的那个”，恰好对应 Python 的下标。  
3. **遍历左半部分**：  
   - 对每个 `i < mid`，如果 `nums[i] > k`，说明它太大了，必须减小到 k。  
   - 所需操作次数是 `nums[i] - k`（因为只能一次减 1）。  
4. **遍历右半部分**：  
   - 对每个 `i ≥ mid`，如果 `nums[i] < k`，说明它太小了，必须增大到 k。  
   - 所需操作次数是 `k - nums[i]`。  
5. **累加所有必要的操作**，即得到最小的总步数。

> **为什么这样是最优的？**  
> - 我们只对 **真正违背中位数条件的元素** 做改动，任何不违背的元素如果再改动，只会增加不必要的步数。  
> - 每个违背的元素只能有唯一的最小改动方式（只能向 k 方向移动），所以我们得到的总和就是全局最小值。  

> **类比**：想象一排学生站成一条线，老师希望第 `mid` 位学生的身高恰好是 `k`，且左边的学生不比 `k` 高，右边的学生不比 `k` 矮。老师只需要让太高的左边学生“蹲下来”，太矮的右边学生“站起来”，不需要动已经符合要求的同学。  

#### 代码（Python）

```python
def min_operations(nums, k):
    """
    返回使数组中位数等于 k 所需的最少操作次数
    """
    nums.sort()                     # O(n log n) 先排序，便于定位左右两侧
    n = len(nums)
    mid = n // 2                    # 中位数下标（偶数长度取较大的那个）

    ops = 0

    # 左侧：下标 < mid，若元素大于 k，需要降到 k
    for i in range(mid):
        if nums[i] > k:
            ops += nums[i] - k      # 只能一次减 1，差值就是需要的步数

    # 右侧（包括中位数本身）：下标 >= mid，若元素小于 k，需要升到 k
    for i in range(mid, n):
        if nums[i] < k:
            ops += k - nums[i]      # 只能一次加 1，差值就是需要的步数

    return ops
```

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 排序占 `n log n`，两次线性遍历各是 `O(n)`，整体仍是 `O(n log n)`。  
  - 这里的 `n log n` 可以理解为“把 `n` 本书排好序需要的时间”，相比 `O(n²)`（每本书和每本书都比较一次）要快得多。  
- **空间复杂度**：`O(1)`（只使用常数级别的额外变量）  

---

## 心得  

- **核心技巧**：**只处理违背中位数条件的元素**，利用排序后左/右半部分的性质，分别向 `k` 收敛。  
- **适用的题型**：  
  1. “把数组的中位数/均值/众数调到指定值” 类的题目（如 *Minimum Operations to Make Array Median Equal to k*）。  
  2. “让所有元素满足某个阈值的最小代价” 题（如 *Minimize Operations to Make Array Elements Equal*）。  
  3. “在有序序列中，使某个位置的值达到目标，需要的最小增删步数”。  
- **一句话总结**：**把左边大于 k 的降到 k，右边小于 k 的升到 k，累计差值即最小操作数**。

---

## 反思  

- **第一反应**：直接把所有数改成 k，想到的实现很直接，但忽略了“只要中位数满足条件，其余可以保持原样”。  
- **最容易踩的坑**：  
  - 忘记 **包括中位数本身** 在右侧的处理（因为题目要求偶数长度取较大的中位数）。  
  - 忽视 **数组已经排序** 的前提，导致在未排序的情况下错误地判断左右半边。  
  - 边界条件：`n = 1` 时只有一个数，直接比较即可；`k` 超出所有元素范围时，只需要一次遍历累计差值。  
- **下次遇到同类题**，第一步应该想到：**先排序，然后只对“违背阈值”的元素进行单向移动**，这样可以立刻把搜索空间从 “所有可能的修改” 缩小到 “必须修改的那几位”。