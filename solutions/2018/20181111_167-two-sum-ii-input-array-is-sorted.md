# #167. 两数之和 II - 输入数组已排序 / Two Sum II - Input Array Is Sorted

> 难度：中等 · 标签：Array、Two Pointers、Binary Search · [LeetCode 链接](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)

---

## 题目（英文原版）

**Description**

Given a 1-indexed array of integers numbers that is already sorted in non-decreasing order, find two numbers such that they add up to a specific target number. Let these two numbers be numbers[index1] and numbers[index2] where 1 <= index1 < index2 <= numbers.length.
Return the indices of the two numbers, index1 and index2, added by one as an integer array [index1, index2] of length 2.
The tests are generated such that there is exactly one solution. You may not use the same element twice.
Your solution must use only constant extra space.

**Examples**

**Example 1:**

```
Input: numbers = [2,7,11,15], target = 9
Output: [1,2]
Explanation: The sum of 2 and 7 is 9. Therefore, index1 = 1, index2 = 2. We return [1, 2].
```

**Example 2:**

```
Input: numbers = [2,3,4], target = 6
Output: [1,3]
Explanation: The sum of 2 and 4 is 6. Therefore index1 = 1, index2 = 3. We return [1, 3].
```

**Example 3:**

```
Input: numbers = [-1,0], target = -1
Output: [1,2]
Explanation: The sum of -1 and 0 is -1. Therefore index1 = 1, index2 = 2. We return [1, 2].
```

**Constraints**

- 2 <= numbers.length <= 3 * 104
- -1000 <= numbers[i] <= 1000
- numbers is sorted in non-decreasing order.
- -1000 <= target <= 1000
- The tests are generated such that there is exactly one solution.

---

## 题目（中文翻译）

给定一个 **1 索引数组（1-indexed array）** `numbers`，该数组已按 **非递减顺序（non-decreasing order）** 排序，找出两个数使其和等于给定的目标值 `target`。设这两个数分别为 `numbers[index1]` 和 `numbers[index2]`，满足 `1 <= index1 < index2 <= numbers.length`。  
返回这两个数的索引 `[index1, index2]`，索引需 **加一**（即仍为 1 索引），返回形式为长度为 2 的 **整数数组（integer array）**。  

测试数据保证恰好只有唯一解。不能使用同一个元素两次。  
你的解法必须使用 **常数额外空间（constant extra space）**。

**示例 1**  
**输入**: `numbers = [2,7,11,15]`, `target = 9`  
**输出**: `[1,2]`  
**解释**: 2 与 7 的和为 9，因此 `index1 = 1`, `index2 = 2`。返回 `[1, 2]`。

**示例 2**  
**输入**: `numbers = [2,3,4]`, `target = 6`  
**输出**: `[1,3]`  
**解释**: 2 与 4 的和为 6，因此 `index1 = 1`, `index2 = 3`。返回 `[1, 3]`。

**示例 3**  
**输入**: `numbers = [-1,0]`, `target = -1`  
**输出**: `[1,2]`  
**解释**: -1 与 0 的和为 -1，因此 `index1 = 1`, `index2 = 2`。返回 `[1, 2]`。

**约束条件**

- `2 <= numbers.length <= 3 * 10^4`
- `-1000 <= numbers[i] <= 1000`
- `numbers` 按 **非递减顺序（non-decreasing order）** 排列
- `-1000 <= target <= 1000`
- 测试数据保证恰好只有唯一解

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每一对数字都尝试一次**，看它们的和是否等于目标值 `target`。  
这相当于在“找对象”——我们把数组里的每个人都和后面的人逐个约会，直到找到那对恰好凑成 `target` 的情侣。

- **用到的数据结构**：只需要原始的列表 `numbers`，不需要额外的容器。  
- **为什么正确**：题目保证数组中恰好有唯一的一组满足条件的下标。遍历所有可能的两两组合（`i < j`），必然能碰到这唯一的那一对，于是返回它的下标（记得要加 1，题目要求 1‑indexed）。  
- **时间/空间复杂度**：  
  - 时间上我们要检查 `C(n,2) = n·(n‑1)/2` 对，其中 `n` 是数组长度。用大白话说，就是 **大约 n 的平方** 次比较，记作 **O(n²)**。  
  - 空间上我们只用了常数级的变量（循环计数器、返回值），所以是 **O(1)**。

#### 代码（Python）

```python
def two_sum_bruteforce(numbers, target):
    """
    暴力解：枚举所有 i < j 的组合，找出满足 numbers[i] + numbers[j] == target 的那一对。
    """
    n = len(numbers)
    # 外层遍历左指针 i
    for i in range(n - 1):
        # 内层遍历右指针 j，始终保证 j > i
        for j in range(i + 1, n):
            # 如果两数之和等于目标值，就返回 1-indexed 的下标
            if numbers[i] + numbers[j] == target:
                # 题目要求返回的是列表 [index1, index2]
                return [i + 1, j + 1]   # 加 1 把 0-index 转成 1-index
    # 由于题目保证一定有解，这行理论上不会执行
    return []
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 解释：如果 `n = 10,000`，暴力解大约要检查 50,000,000 对，显然在实际运行时会很慢。  
- **空间复杂度**：`O(1)`  
  - 解释：只用了几个整型变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

从暴力解出发，我们发现 **瓶颈在于重复检查很多不可能的组合**。  
因为数组已经 **按非递减顺序排好**，我们可以利用这个顺序来“剪枝”，只保留有希望的组合。

**核心思想：双指针（Two Pointers）**  
- 把一个指针放在最左边（`left`），另一个放在最右边（`right`）。  
- 计算 `numbers[left] + numbers[right]` 与 `target` 的关系：
  - 如果和正好等于 `target`，任务完成，返回下标。  
  - 如果和 **小于** `target`，说明左边的数太小（因为数组递增），只能把左指针向右移，让和增大。  
  - 如果和 **大于** `target`，说明右边的数太大，必须把右指针向左移，让和减小。  
- 这样每一步都能把搜索空间 **缩小一半**，最多只需要遍历 `n` 次。

**类比**：想象两个孩子站在一条长凳的两端，凳子上放着不同重量的石头。老师要他们把手中的石头重量加起来恰好等于 `target`。如果两人手中的石头太轻，左边的孩子（轻的）要往中间走；如果太重，右边的孩子（重的）要往中间走。最终他们必然在某个位置相遇，即找到答案。

**为什么只需要常数空间**：我们只用了两个整数 `left`、`right`，不依赖额外的数据结构。

#### 代码（Python）

```python
def two_sum_two_pointers(numbers, target):
    """
    双指针解法：利用已排序的特性，只用 O(1) 额外空间，在 O(n) 时间内找到答案。
    """
    left = 0                 # 左指针，从最左侧开始（0-index）
    right = len(numbers) - 1 # 右指针，从最右侧开始

    while left < right:      # 当左指针未超过右指针时继续
        cur_sum = numbers[left] + numbers[right]  # 当前两数之和

        if cur_sum == target:
            # 找到目标，返回 1-indexed 的下标
            return [left + 1, right + 1]

        if cur_sum < target:
            # 和太小，左边的数不够大，左指针右移
            left += 1
        else:
            # 和太大，右边的数太大，右指针左移
            right -= 1

    # 题目保证必有唯一解，理论上不会走到这里
    return []
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 解释：每一次循环要么左指针右移，要么右指针左移，两个指针最多各移动 `n` 步，所以最多检查 `n` 次。相比暴力的 `n²`，速度提升了 **平方级**。  
- **空间复杂度**：`O(1)`  
  - 解释：只用了两个整数变量 `left`、`right`，与输入规模无关，满足题目“常数额外空间”的要求。

---

## 心得

- **核心技巧**：**双指针**（Two‑Pointer）——在有序数组中寻找满足某种关系的元素对时的常用武器。  
- **适用的题型**：  
  1. “Two Sum II – Input array is sorted”（本题）。  
  2. “3Sum” 中的内部两数求和（先排序后使用双指针）。  
  3. “Remove Duplicates from Sorted Array” 通过前后指针压缩数组。  
- **一句话总结**：**利用有序性让左、右两端“相向而行”，每一步都排除无效区间，线性时间搞定两数之和**。

---

## 反思

- **第一反应**：看到“已排序”，立刻想到二分查找或双指针，而不是直接枚举。  
- **最容易踩的坑**：  
  - **下标偏移**：题目要求返回 1‑indexed 的下标，忘记加 1 会导致答案错误。  
  - **指针移动条件写反**：把 “和小于 target 时左指针右移” 写成左指针左移，会陷入死循环。  
  - **边界情况**：数组最短只有两个元素时，循环条件 `left < right` 仍然成立，需要确保代码能直接返回。  
- **下次遇到同类题**：**第一步先检查数组是否已排序**，若已排序立刻考虑双指针；若未排序再考虑哈希表或先排序后再用双指针。这样能迅速锁定最优解的方向。