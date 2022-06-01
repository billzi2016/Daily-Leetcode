# #1800. 最大上升子数组和 / Maximum Ascending Subarray Sum

> 难度：简单 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/maximum-ascending-subarray-sum/)

---

## 题目（英文原版）

**Description**

Given an array of positive integers nums, return the maximum possible sum of an strictly increasing subarray in nums.
A subarray is defined as a contiguous sequence of numbers in an array.

**Examples**

**Example 1:**

```
Input: nums = [10,20,30,5,10,50]
Output: 65
Explanation: [5,10,50] is the ascending subarray with the maximum sum of 65.
```

**Example 2:**

```
Input: nums = [10,20,30,40,50]
Output: 150
Explanation: [10,20,30,40,50] is the ascending subarray with the maximum sum of 150.
```

**Example 3:**

```
Input: nums = [12,17,15,13,10,11,12]
Output: 33
Explanation: [10,11,12] is the ascending subarray with the maximum sum of 33.
```

**Constraints**

- 1 <= nums.length <= 100
- 1 <= nums[i] <= 100

---

## 题目（中文翻译）

给定一个由正整数构成的数组 `nums`，返回 `nums` 中严格递增子数组（subarray）的最大可能和。  
子数组（subarray）被定义为数组中连续的一段数字序列。

## 示例

### 示例 1
**输入**: `nums = [10,20,30,5,10,50]`  
**输出**: `65`  
**解释**: `[5,10,50]` 是和为 `65` 的最大上升子数组。

### 示例 2
**输入**: `nums = [10,20,30,40,50]`  
**输出**: `150`  
**解释**: `[10,20,30,40,50]` 是和为 `150` 的上升子数组。

### 示例 3
**输入**: `nums = [12,17,15,13,10,11,12]`  
**输出**: `33`  
**解释**: `[10,11,12]` 是和为 `33` 的上升子数组。

## 约束条件

- `1 <= nums.length <= 100`
- `1 <= nums[i] <= 100`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把 **所有可能的子数组** 都枚举一遍，判断它们是否严格递增，如果是就把子数组的元素求和，最后取最大值。  

- **子数组**：数组里连续的一段，就像我们在一串珠子里挑出相邻的几颗。  
- **严格递增**：后面的数必须比前面的数大，类似爬楼梯，每一步只能往更高的台阶走。  
- **数据结构**：只需要用普通的 Python 列表 `nums`，以及几个整数变量来记录当前的和、最大和等。  

这个方法一定能得到正确答案，因为我们没有漏掉任何可能的子数组，所有符合条件的子数组都会被检查到。  

**时间/空间复杂度**  
- 枚举子数组的两层循环，每层最多遍历 `n`（数组长度）次，最坏情况下是 `n·n = n²` 次操作。这里的 **O(n²)** 可以理解为“如果数组有 1000 个元素，程序大概要做 1000×1000 = 100 万次比较”。  
- 只使用了常数个额外变量，空间复杂度是 **O(1)**（不随 `n` 增长）。  

#### 代码（Python）  

```python
def maxAscendingSum_bruteforce(nums):
    """
    暴力枚举所有子数组，求严格递增子数组的最大和
    """
    n = len(nums)
    max_sum = 0                     # 记录全局最大和

    # i 为子数组的起始下标
    for i in range(n):
        cur_sum = 0                  # 当前子数组的和
        prev = -float('inf')         # 前一个元素的值，初始设为负无穷，保证第一个元素一定可以加入

        # j 为子数组的结束下标（包含）
        for j in range(i, n):
            if nums[j] > prev:       # 严格递增才可以继续累加
                cur_sum += nums[j]
                prev = nums[j]
                # 更新全局最大和
                if cur_sum > max_sum:
                    max_sum = cur_sum
            else:
                # 一旦不递增，后面的元素就不可能再属于同一个递增子数组
                break

    return max_sum
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 解释：外层循环 `n` 次，内层最坏情况下也会遍历 `n` 次，所以总体是 `n × n`。  
- **空间复杂度**：`O(1)`  
  - 只用了若干整数变量，和输入规模无关。  

---  

### 2. 最优解  

#### 思路  
从暴力解可以看到，**“不递增” 的位置把数组天然划分成了若干段**，每段内部本身就是严格递增的子数组。  
因此我们只需要一次线性遍历，**在每段递增区间内累计求和**，当遇到不递增的元素时，结束当前区间、更新答案并重新开始新的区间。  

关键点如下：  

1. **维护两个变量**  
   - `cur_sum`：当前递增区间的元素和。  
   - `max_sum`：遍历过程中出现的最大和。  
2. **遍历时的判断**  
   - 如果 `nums[i] > nums[i-1]`（比前一个大），说明仍在同一个递增区间，`cur_sum += nums[i]`。  
   - 否则，区间结束，先比较 `cur_sum` 与 `max_sum`，再把 `cur_sum` 重置为当前元素 `nums[i]`（从新区间重新开始计数）。  
3. **遍历结束后**，别忘了再比较一次 `cur_sum` 与 `max_sum`，因为最后一个区间可能是最大和所在的区间。  

这就是典型的 **一次扫描（single pass）** 思路，时间只和数组长度成正比。  

> **类比**：想象你在跑马拉松，记录每段上坡的累计海拔。只要下坡了，就把累计值记录下来并重新开始计数。  

#### 代码（Python）  

```python
def maxAscendingSum(nums):
    """
    一次线性扫描求严格递增子数组的最大和
    """
    max_sum = cur_sum = nums[0]   # 第一个元素既是当前和，也是当前最大和

    # 从第二个元素开始遍历
    for i in range(1, len(nums)):
        if nums[i] > nums[i - 1]:          # 仍然递增，累计到当前和
            cur_sum += nums[i]
        else:                              # 递增被打断，开启新子数组
            cur_sum = nums[i]              # 重新计数，从当前元素开始

        # 随时更新全局最大和
        if cur_sum > max_sum:
            max_sum = cur_sum

    return max_sum
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 解释：只遍历了一遍数组，`n` 为数组长度。相较于暴力的 `n²`，这里的“次数”大约是 `n`，如果 `n=1000`，只需要 1000 次比较，快了很多。  
- **空间复杂度**：`O(1)`  
  - 只用了常数个变量，不会随 `n` 增长。  

---  

## 心得  

- **核心技巧**：一次扫描（线性遍历）+ 维护当前区间的累计信息。  
- **适用的题型**：  
  1. “最长/最大/最小递增子数组/子序列” 类题目（如 LeetCode 674. **最长连续递增序列**）。  
  2. “区间划分” 需要在出现特定边界时重置累计值的题目（如求最大子数组和的 Kadane 算法）。  
- **解题钥匙**：**“遇到断点就重新开始”，并且在遍历过程中随时保存全局最优解**。  

## 反思  

- **第一反应**：直接想到枚举所有子数组（暴力），因为它最直观、最安全。  
- **最容易踩的坑**：  
  - 忘记在循环结束后再比较一次 `cur_sum` 与 `max_sum`（最后一个递增区间可能是答案）。  
  - 对“严格递增”的定义理解错误，导致使用 `>=` 而不是 `>`。  
- **下次类似题目第一步**：先判断“断点”在哪里（比如不递增、和为负等），思考是否可以把数组划分成若干自然的子区间，然后尝试 **一次线性扫描** 来累计并更新答案。