# #1498. 满足给定和条件的子序列数量 / Number of Subsequences That Satisfy the Given Sum Condition

> 难度：中等 · 标签：Array、Two Pointers、Binary Search、Sorting · [LeetCode 链接](https://leetcode.com/problems/number-of-subsequences-that-satisfy-the-given-sum-condition/)

---

## 题目（英文原版）

**Description**

You are given an array of integers nums and an integer target.
Return the number of non-empty subsequences of nums such that the sum of the minimum and maximum element on it is less or equal to target. Since the answer may be too large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: nums = [3,5,6,7], target = 9
Output: 4
Explanation: There are 4 subsequences that satisfy the condition.
[3] -> Min value + max value <= target (3 + 3 <= 9)
[3,5] -> (3 + 5 <= 9)
[3,5,6] -> (3 + 6 <= 9)
[3,6] -> (3 + 6 <= 9)
```

**Example 2:**

```
Input: nums = [3,3,6,8], target = 10
Output: 6
Explanation: There are 6 subsequences that satisfy the condition. (nums can have repeated numbers).
[3] , [3] , [3,3], [3,6] , [3,6] , [3,3,6]
```

**Example 3:**

```
Input: nums = [2,3,3,4,6,7], target = 12
Output: 61
Explanation: There are 63 non-empty subsequences, two of them do not satisfy the condition ([6,7], [7]).
Number of valid subsequences (63 - 2 = 61).
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 106
- 1 <= target <= 106

---

## 题目（中文翻译）

给定一个整数数组（array）`nums` 和一个整数 `target`。  
返回 `nums` 中 **非空** 子序列（subsequence）的个数，使得该子序列的 **最小元素** 与 **最大元素** 之和 **小于等于** `target`。由于答案可能非常大，请返回 **模** `10^9 + 7` 的结果。

**示例 1**  
**输入**: `nums = [3,5,6,7]`, `target = 9`  
**输出**: `4`  
**解释**: 满足条件的子序列共有 4 个  
- `[3]` → 最小值 + 最大值 = `3 + 3 ≤ 9`  
- `[3,5]` → `3 + 5 ≤ 9`  
- `[3,5,6]` → `3 + 6 ≤ 9`  
- `[3,6]` → `3 + 6 ≤ 9`

**示例 2**  
**输入**: `nums = [3,3,6,8]`, `target = 10`  
**输出**: `6`  
**解释**: 满足条件的子序列有 6 个（数组中可以出现重复数字）  
`[3]`, `[3]`, `[3,3]`, `[3,6]`, `[3,6]`, `[3,3,6]`

**示例 3**  
**输入**: `nums = [2,3,3,4,6,7]`, `target = 12`  
**输出**: `61`  
**解释**: 所有非空子序列共 63 个，其中有 2 个不满足条件（`[6,7]`, `[7]`），因此有效子序列数为 `63 - 2 = 61`。

**约束条件**  
- `1 <= nums.length <= 10^5`  
- `1 <= nums[i] <= 10^6`  
- `1 <= target <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**枚举所有可能的子序列**，然后检查每个子序列的最小值与最大值之和是否 ≤ `target`。  
- **子序列**：在原数组中挑选若干个元素，保持原来的相对顺序。  
- **枚举子序列**可以看作对每个位置做“取”或“不取”的二进制选择，长度为 `n` 的数组一共有 `2ⁿ` 种取法（不算空集）。  

实现时可以使用递归或位运算来遍历所有子集。每遍历到一个子序列，就用 `min()`、`max()` 取出最小和最大元素，判断 `min+max ≤ target`，满足则计数。

> **为什么会对**  
> 因为我们把**所有**合法子序列都检查了一遍，必然不会漏掉任何一种可能，自然得到正确答案。

> **时间/空间复杂度**  
> - 时间复杂度：`O(2ⁿ * n)`。遍历 `2ⁿ` 个子序列，每个子序列要遍历一次（或调用 `min/max`），最坏要 `n` 步。  
> - 空间复杂度：`O(n)`（递归栈或临时保存子序列的列表）。  

> **大白话解释**：  
> 如果数组有 20 个元素，`2ⁿ` 已经是 1,048,576，已经接近一百万次循环；而题目允许 `n` 达到 10⁵，`2ⁿ` 完全不可想象——相当于宇宙里所有原子都在做加法，显然会超时。

#### 代码（Python）

```python
from typing import List

MOD = 10**9 + 7

def num_subseq_brute(nums: List[int], target: int) -> int:
    n = len(nums)
    ans = 0

    # 用二进制枚举所有非空子序列
    for mask in range(1, 1 << n):          # 1 << n 等价于 2ⁿ
        cur_min = float('inf')
        cur_max = -float('inf')
        # 遍历每一位，判断该位置的元素是否被选中
        for i in range(n):
            if mask >> i & 1:              # 第 i 位为 1，说明取了 nums[i]
                cur_min = min(cur_min, nums[i])
                cur_max = max(cur_max, nums[i])
        # 检查条件
        if cur_min + cur_max <= target:
            ans = (ans + 1) % MOD
    return ans
```

#### 复杂度

- **时间复杂度**：`O(2ⁿ * n)` —— 随着 `n` 增大呈指数级增长，几乎不可能在 `n = 10⁵` 时跑完。  
- **空间复杂度**：`O(1)`（只用了若干个整数变量），不计入输出本身的空间。

---

### 2. 最优解

#### 思路  

**暴力的瓶颈**在于每次都要遍历所有子序列，导致指数级时间。观察题目可以发现：

1. **只关心最小值和最大值**，中间的元素随意取或不取都不会影响条件 `min + max ≤ target`。  
2. **数组排序后**，如果固定左边的最小值 `nums[i]`，那么右边能选的最大值只能是满足 `nums[i] + nums[j] ≤ target` 的最右侧元素 `nums[j]`。  
3. 对于已经排序好的数组，**双指针**可以一次遍历完成所有合法组合：  
   - `left` 指向当前最小值（从左到右），  
   - `right` 初始指向最右端，向左收缩，保证 `nums[left] + nums[right] ≤ target`。  
   - 当条件满足时，**左指针 `left` 与右指针 `right` 之间的所有子序列**（只要最小值固定为 `nums[left]`，最大值可以是 `nums[left] … nums[right]` 中的任何一个）都是合法的。  
   - 具体计数方式：`2^{right-left}`，因为在区间 `(left, right]`（不含 left）里的每个元素都可以**自由选择**（取或不取），共 `right-left` 个位置。  

4. 为了快速求 `2^k mod MOD`，预先计算幂数组 `pow2[k] = 2^k % MOD`，这样每次计数只需一次数组查询。

**核心概念解释**  

- **排序**：把数字从小到大排成一行，像把书按照高度排好，找最小和最大就像找最左和最右的书。  
- **双指针**：想象有两只手从两端向中间走，左手负责挑最小的，右手负责挑最大的，只要两手拿的数字之和不超标，就可以“把中间的书随意挑”。  
- **幂模**：`2^{k}` 表示有 `k` 本书可以自由挑，每本书有两种状态（挑或不挑），所以总组合数是 `2` 的 `k` 次方。因为答案可能非常大，需要对 `10^9+7` 取余。

#### 代码（Python）

```python
from typing import List

MOD = 10**9 + 7

def num_subseq(nums: List[int], target: int) -> int:
    """
    最优解：排序 + 双指针 + 预计算 2^k
    """
    nums.sort()                     # 1. 先把数组从小到大排好
    n = len(nums)

    # 2. 预计算 2^k % MOD，k 从 0 到 n
    pow2 = [1] * (n + 1)            # pow2[0] = 1
    for i in range(1, n + 1):
        pow2[i] = (pow2[i - 1] * 2) % MOD   # 每次乘以 2 并取模

    left, right = 0, n - 1
    ans = 0

    # 3. 双指针遍历
    while left <= right:
        # 如果最小值 + 最大值仍然 ≤ target，说明 left 与 right 之间的任意子集都合法
        if nums[left] + nums[right] <= target:
            # 右侧可以自由取或不取，组合数 = 2^{right-left}
            ans = (ans + pow2[right - left]) % MOD
            left += 1                 # 左指针右移，尝试更大的最小值
        else:
            # 说明当前右端太大，必须左移右指针让最大值变小
            right -= 1

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 排序需要 `O(n log n)`。  
  - 双指针遍历每个元素最多移动一次，线性 `O(n)`。  
  - 预计算幂数组也是 `O(n)`。  
  综合来看，排序是主导，故整体是 `O(n log n)`。  
  与暴力的指数级相比，`n = 10⁵` 完全可以在毫秒级通过。

- **空间复杂度**：`O(n)`  
  - 需要额外的 `pow2` 数组保存 `n+1` 个整数。  
  - 其它变量都是常数级。  

  如果想进一步压缩空间，可以在遍历时直接使用快速幂计算 `2^{right-left}`，但会牺牲常数时间。

---

## 心得

- **核心技巧**：**排序 + 双指针** 把“最小值”和“最大值”的约束转化为区间问题；**预计算幂** 把指数计数变成 O(1) 查询。  
- **适用的题型**  
  1. “子序列/子数组的最小值+最大值 ≤ K” 类似问题（如 LeetCode 1498）  
  2. “两数之和 ≤ target” 的变种，需要统计满足条件的组合数（如 “Number of Pairs With Absolute Difference Less Than K”）  
  3. “在排序数组中统计满足某种区间约束的子集数量”，常见于组合计数类题目。  

- **一句话总结**：**把只关心两端的条件转化为左右指针的可行区间，利用 2 的幂计数所有自由选择的中间元素。**

---

## 反思

- **第一反应**：直接想遍历所有子序列，写递归或位运算实现——这在小数据上能跑通，但忽视了 `n` 可达 `10⁵` 的规模。  
- **最容易踩的坑**  
  - **忘记对答案取模**，导致整数溢出或运行时间变慢。  
  - **边界条件**：当 `left == right` 时仍需计数（单元素子序列），此时 `pow2[0] = 1` 正好对应。  
  - **排序后指针移动顺序**：若写成 `while left < right` 而忘记处理 `left == right`，会漏掉单元素子序列。  
- **下次思路**：看到“最小+最大”这种只与两端有关的约束，立刻想到 **先排序 → 用双指针**，并思考“中间元素是否自由选择”，从而决定是否需要 **幂计数**。这样可以快速从暴力思路跳到线性或对数级的最优解。