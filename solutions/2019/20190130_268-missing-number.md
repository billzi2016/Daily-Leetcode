# #268. 缺失数字 / Missing Number

> 难度：简单 · 标签：Array、Hash Table、Math、Binary Search、Bit Manipulation、Sorting · [LeetCode 链接](https://leetcode.com/problems/missing-number/)

---

## 题目（英文原版）

**Description**

Given an array nums containing n distinct numbers in the range [0, n], return the only number in the range that is missing from the array.
Follow up: Could you implement a solution using only O(1) extra space complexity and O(n) runtime complexity?

**Examples**

**Example 1:**

```
Input: nums = [3,0,1]
Output: 2
Explanation:
n = 3 since there are 3 numbers, so all numbers are in the range [0,3] . 2 is the missing number in the range since it does not appear in nums .
```

**Example 2:**

```
Input: nums = [0,1]
Output: 2
Explanation:
n = 2 since there are 2 numbers, so all numbers are in the range [0,2] . 2 is the missing number in the range since it does not appear in nums .
```

**Example 3:**

```
Input: nums = [9,6,4,2,3,5,7,0,1]
Output: 8
Explanation:
n = 9 since there are 9 numbers, so all numbers are in the range [0,9] . 8 is the missing number in the range since it does not appear in nums .
```

**Constraints**

- n == nums.length
- 1 <= n <= 104
- 0 <= nums[i] <= n
- All the numbers of nums are unique.

---

## 题目（中文翻译）

**题目描述**  
给定一个包含 `n` 个互不相同的整数的数组 `nums`，这些整数位于区间 `[0, n]` 中，返回该区间内唯一缺失的数字。

**示例 1**  
**示例 2**  
**示例 3**

**约束条件**  
- `n == nums.length`  
- `1 <= n <= 10⁴`  
- `0 <= nums[i] <= n`  
- `nums` 中的所有数字互不相同  

**进阶**  
能否只使用 **O(1)** 额外空间复杂度并在 **O(n)** 时间复杂度内实现？

---

### 示例

**示例 1**  
```
Input: nums = [3,0,1]
Output: 2
Explanation:
n = 3，因为数组中有 3 个数字，所以所有数字都在区间 [0,3] 中。2 是该区间内缺失的数字，因为它没有出现在 nums 中。
```

**示例 2**  
```
Input: nums = [0,1]
Output: 2
Explanation:
n = 2，因为数组中有 2 个数字，所以所有数字都在区间 [0,2] 中。2 是该区间内缺失的数字，因为它没有出现在 nums 中。
```

**示例 3**  
```
Input: nums = [9,6,4,2,3,5,7,0,1]
Output: 8
Explanation:
n = 9，因为数组中有 9 个数字，所以所有数字都在区间 [0,9] 中。8 是该区间内缺失的数字，因为它没有出现在 nums 中。
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把 **0 ~ n** 这 n+1 个数全部列出来，然后逐个检查它们是否出现在数组 `nums` 中。  
- **数据结构**：可以用一个集合（`set`）来存放数组里的所有元素。集合就像一本「词典」——把每个出现的数字记下来，之后查找某个数字是否在词典里，只需要 O(1) 的时间。  
- **正确性**：因为题目保证数组里没有重复且只缺少一个数，只要把所有出现的数记下来，再遍历 0~n 的完整区间，第一次发现「词典」里没有的数，就是缺失的那一个。  

#### 代码（Python）

```python
def missingNumber(nums):
    """
    暴力解：使用集合记录出现的数字，然后遍历 0~n 找出缺失的数字
    """
    # 把 nums 全部放进集合，查询会很快
    appeared = set(nums)                     # O(n) 时间，O(n) 额外空间

    n = len(nums)                            # n 是数组长度，也是缺失数所在区间的上界
    for number in range(n + 1):              # 检查 0~n 每个数
        if number not in appeared:           # 如果集合里没有，就找到了
            return number
    # 理论上不会走到这里，因为必有缺失数
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  解释：我们遍历数组一次把元素放进集合（O(n)），随后又遍历 0~n（最多 n+1 次），两段都是线性时间，所以总体是 O(n)。  
- **空间复杂度**：`O(n)`  
  解释：集合里要保存所有出现的数字，最坏情况要存 n 个元素，空间随输入规模线性增长。

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在于**额外的集合**占用了 O(n) 的空间。题目要求 **只使用 O(1) 额外空间**（常数级别的变量），因此我们要想办法在不额外存储所有元素的前提下，仍然能够得到缺失的数字。

一种常见且直观的技巧是利用 **等差数列求和公式**。  
- 区间 `[0, n]` 中所有数的和可以直接算出来：  

\[
S = 0 + 1 + 2 + \dots + n = \frac{n \times (n + 1)}{2}
\]

- 如果把数组里出现的数字全部加起来，记为 `sum_nums`，那么缺失的数字就是 `S - sum_nums`。  

这个思路只需要 **两个整数变量**（`S` 与 `sum_nums`），不依赖额外的数据结构，符合 O(1) 空间要求。

> **为什么等差求和公式成立？**  
> 想象把 `0` 与 `n`、`1` 与 `n-1` 配对，每对的和都是 `n`，总共有 `n/2` 对（若 `n` 为奇数，最中间的数字正好是 `n/2`，也恰好被算进公式里）。于是总和就是 `n * (n + 1) / 2`。

#### 代码（Python）

```python
def missingNumber(nums):
    """
    最优解：利用等差数列求和公式，只用常数级别的额外空间
    """
    n = len(nums)                           # 区间上界
    # 计算完整区间 0~n 的理论总和
    total_sum = n * (n + 1) // 2            # // 是整数除法，避免出现小数

    # 累加数组中出现的所有数字
    array_sum = 0
    for num in nums:                        # 只遍历一次数组
        array_sum += num

    # 缺失的数字就是理论总和减去实际出现的和
    return total_sum - array_sum
```

#### 复杂度  

- **时间复杂度**：`O(n)` — 只遍历一次数组，线性时间。与暴力解相比，时间相同，但没有额外的遍历集合步骤。  
- **空间复杂度**：`O(1)` — 只使用了几个整数变量（`n`、`total_sum`、`array_sum`），不随输入规模增长。

> **另一个同样满足 O(1) 空间的思路**：**异或（XOR）**。把 `0~n` 与数组里的数全部异或，结果就是缺失的数。原理类似，感兴趣的同学可以自行尝试实现。

---

## 心得

- **核心技巧**：把题目中的“缺失”转化为“总和差”或“异或差”。只要能一次遍历得到整体信息，就不必额外存储每个元素。  
- **适用题型**：  
  1. “Missing Number” 系列（如缺失的多个数、缺失的正数等）  
  2. “Find the Duplicate Number”——可以用求和或异或的变形思路  
  3. “Single Number”——经典的异或求唯一出现一次的数  

- **一句话总结解题钥匙**：**把“找哪个没有出现”转成“已知整体减去已出现”，用数学公式或位运算一次完成**。

---

## 反思

- **第一反应**：看到“缺失一个数”，立刻想到把所有可能的数列出来再检查——这就是暴力解。  
- **最容易踩的坑**：  
  - **整数溢出**：在某些语言（如 C++）中 `n*(n+1)` 可能超过 32 位整数范围，需要使用更宽的类型。Python 自动处理大整数，这里不必担心。  
  - **边界条件**：当缺失的是 `0` 或 `n` 时，仍然要能正确返回。使用等差求和公式可以天然覆盖这两种情况。  
- **下次遇到同类题**，第一步应该想到**“整体（和/异或） vs. 已出现的部分”**，用差值直接得到答案，而不是逐个搜索。这样既省空间又省时间。