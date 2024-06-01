# #2717. 半有序排列 / Semi-Ordered Permutation

> 难度：简单 · 标签：Array、Simulation · [LeetCode 链接](https://leetcode.com/problems/semi-ordered-permutation/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed permutation of n integers nums.
A permutation is called semi-ordered if the first number equals 1 and the last number equals n. You can perform the below operation as many times as you want until you make nums a semi-ordered permutation:
Return the minimum number of operations to make nums a semi-ordered permutation.
A permutation is a sequence of integers from 1 to n of length n containing each number exactly once.

**Examples**

**Example 1:**

```
Input: nums = [2,1,4,3]
Output: 2
Explanation: We can make the permutation semi-ordered using these sequence of operations: 
1 - swap i = 0 and j = 1. The permutation becomes [1,2,4,3].
2 - swap i = 2 and j = 3. The permutation becomes [1,2,3,4].
It can be proved that there is no sequence of less than two operations that make nums a semi-ordered permutation.
```

**Example 2:**

```
Input: nums = [2,4,1,3]
Output: 3
Explanation: We can make the permutation semi-ordered using these sequence of operations:
1 - swap i = 1 and j = 2. The permutation becomes [2,1,4,3].
2 - swap i = 0 and j = 1. The permutation becomes [1,2,4,3].
3 - swap i = 2 and j = 3. The permutation becomes [1,2,3,4].
It can be proved that there is no sequence of less than three operations that make nums a semi-ordered permutation.
```

**Example 3:**

```
Input: nums = [1,3,4,2,5]
Output: 0
Explanation: The permutation is already a semi-ordered permutation.
```

**Constraints**

- 2 <= nums.length == n <= 50
- 1 <= nums[i] <= 50
- nums is a permutation.

---

## 题目（中文翻译）

给定一个 **0-indexed** 的长度为 `n` 的排列 `nums`。  

如果排列的第一个元素等于 `1` 且最后一个元素等于 `n`，则称该排列为 **半有序（semi-ordered）**。  
你可以无限次执行以下操作，直到将 `nums` 变为半有序排列：

- 交换任意两个下标 `i` 和 `j`（`i ≠ j`）处的元素。

返回使 `nums` 成为半有序排列所需的 **最少操作次数**。

**排列（permutation）** 是由 `1` 到 `n` 的整数构成的长度为 `n` 的序列，且每个数字恰好出现一次。

### 示例

#### 示例 1
> **输入**: `nums = [2,1,4,3]`  
> **输出**: `2`  
> **解释**: 我们可以按如下顺序进行交换，使排列半有序：  
> 1. 交换 `i = 0` 与 `j = 1`，得到 `[1,2,4,3]`。  
> 2. 交换 `i = 2` 与 `j = 3`，得到 `[1,2,3,4]`。  
> 可以证明不存在少于两次操作即可使 `nums` 成为半有序排列的方案。

#### 示例 2
> **输入**: `nums = [2,4,1,3]`  
> **输出**: `3`  
> **解释**: 我们可以按如下顺序进行交换：  
> 1. 交换 `i = 1` 与 `j = 2`，得到 `[2,1,4,3]`。  
> 2. 交换 `i = 0` 与 `j = 1`，得到 `[1,2,4,3]`。  
> 3. 交换 `i = 2` 与 `j = 3`，得到 `[1,2,3,4]`。  
> 可以证明不存在少于三次操作即可使 `nums` 成为半有序排列的方案。

#### 示例 3
> **输入**: `nums = [1,3,4,2,5]`  
> **输出**: `0`  
> **解释**: 该排列已经是半有序排列，无需任何操作。

### 约束条件
- `2 <= nums.length == n <= 50`
- `1 <= nums[i] <= 50`
- `nums` 是一个 **排列（permutation）**。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把 1 直接搬到最前面，把 n 直接搬到最后面**，每一次搬运都用一次「任意两位置交换」的操作。  

- **数据结构**：我们只需要遍历一次数组，找到数字 `1` 和数字 `n` 的下标（位置）。可以把数组想象成一排座位，`1` 就像是想坐在最左边的朋友，`n` 想坐在最右边的朋友。  
- **为什么正确**：把 `1` 往左边交换一次，它的下标就会减 1，继续这样交换，最终一定能把 `1` 移到下标 `0`。同理，`n` 往右边交换一次，下标就会加 1，最终一定能到达下标 `n‑1`。只要把这两个过程都完整跑一遍，最终的数组必然是 `[1, … , n]`，即「半有序」的排列。  
- **时间/空间复杂度**：我们只遍历一次数组找到两个位置，然后在最坏情况下分别把 `1` 向左搬 `idx1` 步、把 `n` 向右搬 `(n-1-idxn)` 步。整个过程只用了常数级别的额外空间（几个整数），所以  

  - 时间复杂度：`O(n)`，其中 `n` 是数组长度。可以把 `O(n)` 想成「跟数组里每个元素都聊一次」的工作量。  
  - 空间复杂度：`O(1)`，只用了几根指针（整数），不随 `n` 增长。

> **注意**：这种「一步步搬」的写法其实已经是最优的实现，只是我们把「搬」的过程写得很直观，便于初学者理解。

#### 代码（Python）

```python
def minOperations_bruteforce(nums):
    """
    暴力模拟：把 1 往左搬到最前面，把 n 往右搬到最后面。
    只统计交换次数，不真的去改动数组（因为只需要计数）。
    """
    n = len(nums)
    # 找到 1 和 n 的下标
    idx_one = nums.index(1)          # 1 在第几位
    idx_n   = nums.index(n)          # n 在第几位

    # 把 1 往左搬到下标 0，需要 idx_one 次交换
    moves = idx_one

    # 把 n 往右搬到下标 n-1，需要 (n-1 - idx_n) 次交换
    moves += (n - 1 - idx_n)

    # 如果 1 本来在 n 的右边（idx_one > idx_n），
    # 那么在搬动的过程中会出现一次「多搬」的情况，
    # 实际只需要再减掉 1 次交换。
    if idx_one > idx_n:
        moves -= 1

    return moves
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历一次数组寻找两个位置。  
- **空间复杂度**：`O(1)` —— 只用几个整数变量。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正的瓶颈不在于时间**（已经是线性），而在于我们仍然「模拟」了搬运过程。实际上，只要知道 `1` 和 `n` 的位置，就能直接算出最少需要多少次交换，而不必真的去「搬」：

1. 记 `x` 为 `1` 的下标，`y` 为 `n` 的下标。  
2. 把 `1` 移到最左边需要 `x` 次交换（每次把它和左边的元素换位）。  
3. 把 `n` 移到最右边需要 `n‑1‑y` 次交换（每次把它和右边的元素换位）。  
4. 但如果 `1` 本来在 `n` 的右边（`x > y`），在把 `1` 搬到最左边的过程中，`n` 会被提前「挤」到左边一次，这时候我们实际上少了一次独立的交换。于是整体答案要 **减 1**。

把这几条写成公式就是：

```
if x < y:   answer = x + (n - 1 - y)
else:       answer = x + (n - 1 - y) - 1
```

这一步只用了常数时间，**无需遍历或模拟**，所以是最优的。

> **核心技巧**：把「把元素搬到目标位置」转化为「它距离目标有多远」的计数，再考虑两者搬运顺序产生的冲突（即 `x > y` 时的-1）。这类「距离+冲突」的思考方式在很多置换/排列题中都会出现。

#### 代码（Python）

```python
def minOperations(nums):
    """
    O(1) 直接算出答案，只需要找出 1 和 n 的位置。
    """
    n = len(nums)
    x = nums.index(1)   # 1 的下标
    y = nums.index(n)   # n 的下标

    # 基础距离之和
    ans = x + (n - 1 - y)

    # 如果 1 在 n 的右边，两次搬运会产生一次重复交换，抵消 1 次
    if x > y:
        ans -= 1
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)` 用于一次 `index` 查找（实际上是线性遍历），在本题的约束 `n ≤ 50` 下已经是最小可能。可以把它看成「只看两遍数组」的工作量。  
- **空间复杂度**：`O(1)` —— 只用常数个整数。

> 与暴力解相比，最优解去掉了「搬」的过程，直接用数学公式算出答案，思路更简洁，代码行数更少。

---

## 心得

- **核心技巧**：把「把指定元素放到指定位置」转化为「它离目标有多少格」，并考虑两个元素搬运顺序产生的冲突（`x > y` 时的 `-1`）。  
- **适用的题型**  
  1. *把 1 放到最左、把 n 放到最右* 类似的「半有序排列」题。  
  2. *把任意两个特定元素分别放到两端*（如把最小值放左、最大值放右）。  
  3. *只允许交换任意两位*，求最少交换次数的题目（如把数组变成升序的最少交换次数）。  
- **一句话总结**：**只要知道元素距离目标有多远，答案往往就是这些距离之和，冲突时记得减一次**。

---

## 反思

- **第一反应**：看到「任意两位交换」就想到「把 1 拿到最左，n 拿到最右」——先定位，再一步步搬。  
- **最容易踩的坑**  
  - 忘记当 `1` 在 `n` 右边时会产生一次重复交换，需要 `-1`。  
  - 把「交换次数」误认为是「移动距离」的和，而没有考虑冲突。  
  - 边界情况：如果数组已经是半有序的（`x==0` 且 `y==n-1`），答案应为 `0`。  
- **下次遇到同类题**：第一步先 **定位关键元素**（比如最小值、最大值），**算它们到目标位置的距离**，再检查 **搬运顺序是否会产生冲突**，必要时做一次「减一」的修正。