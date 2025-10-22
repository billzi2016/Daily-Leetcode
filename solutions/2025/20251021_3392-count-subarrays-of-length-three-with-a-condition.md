# #3392. 计数满足条件的长度为三的子数组 / Count Subarrays of Length Three With a Condition

> 难度：简单 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/count-subarrays-of-length-three-with-a-condition/)

---

## 题目（英文原版）

**Description**

Given an integer array nums, return the number of subarrays of length 3 such that the sum of the first and third numbers equals exactly half of the second number.

**Examples**

**Example 1:**

```
Input: nums = [1,2,1,4,1]
Output: 1
Explanation:
Only the subarray [1,4,1] contains exactly 3 elements where the sum of the first and third numbers equals half the middle number.
```

**Example 2:**

```
Input: nums = [1,1,1]
Output: 0
Explanation:
[1,1,1] is the only subarray of length 3. However, its first and third numbers do not add to half the middle number.
```

**Constraints**

- 3 <= nums.length <= 100
- -100 <= nums[i] <= 100

---

## 题目（中文翻译）

**题目描述**  
给定一个整数数组 `nums`，返回满足以下条件的长度为 3 的子数组（subarray）数量：子数组中第一个元素与第三个元素的和恰好等于第二个元素的一半。

**示例 1**  
```
Input: nums = [1,2,1,4,1]
Output: 1
```
**解释**：  
唯一满足条件的子数组是 `[1,4,1]`，其中首尾两数之和 `1 + 1 = 2` 正好等于中间数 `4` 的一半 `4 / 2 = 2`。

**示例 2**  
```
Input: nums = [1,1,1]
Output: 0
```
**解释**：  
唯一的长度为 3 的子数组是 `[1,1,1]`，但其首尾两数之和 `1 + 1 = 2` 并不等于中间数 `1` 的一半 `1 / 2 = 0.5`，因此不计入。

**约束条件**  
- `3 <= nums.length <= 100`  
- `-100 <= nums[i] <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有长度为 3 的子数组都列举出来，逐个检查条件是否满足**。  
- **数据结构**：只需要用到普通的 Python 列表（list），因为我们只在原数组上取连续的三个元素。可以把「取子数组」想象成「在书里一次翻开三页」——只要把起始页码记下来，就能直接看到这三页的内容。  
- **正确性**：题目要求统计满足 `first + third = half of second` 的子数组。只要遍历到每一个可能的起始位置 `i`（`0 ≤ i ≤ len(nums)-3`），取出 `nums[i]、nums[i+1]、nums[i+2]`，检查 `2*(nums[i] + nums[i+2]) == nums[i+1]`（把「除以 2」移到等式左边避免浮点数），若成立就计数。遍历完所有起始位置后，计数即为答案。  
- **时间/空间复杂度**：  
  - **时间**：我们用两层循环来枚举子数组的起始位置和结束位置，最坏情况下会检查 `n*(n-1)/2` 次（这里 `n` 是数组长度），这在大 O 记号里写成 **O(n²)**。对初学者来说，`O(n²)` 可以理解为「如果数组有 10 000 个元素，操作次数大约是 10 000×10 000 = 1 亿次」，明显会慢。  
  - **空间**：只用了常数个额外变量（计数器、循环索引），所以是 **O(1)**，即“几乎不占额外内存”。

#### 代码（Python）

```python
def count_subarrays_bruteforce(nums):
    n = len(nums)
    ans = 0                         # 计数满足条件的子数组个数
    # i 为子数组的左端点，j 为右端点（这里 j = i+2，因为长度固定为 3）
    for i in range(n):
        for j in range(i + 2, n):
            # 只在长度恰好为 3 时检查条件
            if j - i + 1 == 3:
                first = nums[i]
                middle = nums[i + 1]
                third = nums[j]
                # 把 “等于一半” 移到左边：2 * (first + third) == middle
                if 2 * (first + third) == middle:
                    ans += 1
    return ans
```

#### 复杂度

- **时间复杂度**：**O(n²)** — 需要两层循环，随着数组长度的增长，操作次数呈二次方增长。  
- **空间复杂度**：**O(1)** — 只用了固定数量的变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**子数组的长度固定为 3**，所以其实不需要两层循环，只要一次遍历就能把所有可能的三元组枚举完。  
- **慢在哪里**：暴力解的第二层循环（`j`）其实每次只会取 `i+2`，所以大多数循环体是多余的，浪费了大量时间。  
- **优化步骤**：  
  1. 只保留外层循环 `i`，让 `i` 直接走到可以形成长度为 3 的子数组的最后一个起点 `len(nums)-3`。  
  2. 对每个 `i`，直接取 `nums[i]、nums[i+1]、nums[i+2]`，检查同样的等式 `2*(nums[i] + nums[i+2]) == nums[i+1]`。  
- **核心算法**：**一次线性扫描**（Linear Scan）。这是一种最基础的技巧：当题目只要求查看「相邻」或「固定窗口」的元素时，直接用滑动窗口或固定步长遍历即可。  
- **类比**：想象你在一条路上走，每走一步就顺手检查前后两块石头的颜色是否满足某种关系，走到终点即可，无需回头或多次遍历。

#### 代码（Python）

```python
def count_subarrays(nums):
    """
    返回满足 nums[i] + nums[i+2] = nums[i+1] / 2 的长度为 3 的子数组个数。
    这里把等式两边同乘 2，避免出现小数。
    """
    n = len(nums)
    ans = 0
    # i 只能取到 n-3，因为要保证 i、i+1、i+2 都在数组范围内
    for i in range(n - 2):
        first = nums[i]
        middle = nums[i + 1]
        third = nums[i + 2]
        # 检查 2 * (first + third) 是否恰好等于 middle
        if 2 * (first + third) == middle:
            ans += 1
    return ans
```

#### 复杂度

- **时间复杂度**：**O(n)** — 只遍历一次数组，操作次数随数组长度线性增长。相比暴力的 O(n²)，速度提升显著。  
- **空间复杂度**：**O(1)** — 仍然只使用常数个额外变量。

---

## 心得

- **核心技巧**：利用**固定窗口长度的线性扫描**（一次遍历所有长度为 3 的子数组）。  
- **适用题型**：  
  1. “判断相邻三数关系”类题，例如 `nums[i] + nums[i+2] == nums[i+1]`。  
  2. “滑动窗口计数”类题，例如统计满足 `sum(window) == k` 的固定长度子数组。  
  3. “固定间隔比较”类题，例如检查 `nums[i] == nums[i+2]`。  
- **一句话总结**：**只要子数组长度固定，直接用一次线性遍历即可把所有候选窗口枚举完**。

---

## 反思

- **第一反应**：看到 “长度为 3” 立刻想到枚举所有三元组，用三层循环实现。  
- **最容易踩的坑**：  
  - 忘记把 “除以 2” 移到左边，导致使用浮点数比较产生精度误差。  
  - 边界条件：数组长度恰好为 3 时仍需检查一次；若写成 `for i in range(len(nums))` 会产生索引越界。  
- **下次思路**：遇到 “固定窗口长度” 的计数题，第一步就想到 **滑动窗口 / 固定步长一次遍历**，而不是先写多重循环。这样可以直接得到最优的线性时间解。