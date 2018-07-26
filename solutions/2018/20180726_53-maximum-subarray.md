# #53. 最大子数组 / Maximum Subarray

> 难度：中等 · 标签：Array、Divide and Conquer、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/maximum-subarray/)

---

## 题目（英文原版）

**Description**

Given an integer array nums, find the subarray with the largest sum, and return its sum.
Follow up: If you have figured out the O(n) solution, try coding another solution using the divide and conquer approach, which is more subtle.

**Examples**

**Example 1:**

```
Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
Output: 6
Explanation: The subarray [4,-1,2,1] has the largest sum 6.
```

**Example 2:**

```
Input: nums = [1]
Output: 1
Explanation: The subarray [1] has the largest sum 1.
```

**Example 3:**

```
Input: nums = [5,4,-1,7,8]
Output: 23
Explanation: The subarray [5,4,-1,7,8] has the largest sum 23.
```

**Constraints**

- 1 <= nums.length <= 105
- -104 <= nums[i] <= 104

---

## 题目（中文翻译）

给定一个整数数组（integer array）`nums`，找出和最大的子数组（subarray），并返回该和。

**示例 1**  
**示例 2**  
**示例 3**  

**约束条件**  
- 1 ≤ `nums.length` ≤ 10⁵  
- -10⁴ ≤ `nums[i]` ≤ 10⁴  

**进阶**：如果你已经实现了时间复杂度为 O(n) 的解法，尝试使用分治（divide and conquer）方法再实现一次，这种方法更为微妙。

---

### 示例

**示例 1**  
**输入**：`nums = [-2,1,-3,4,-1,2,1,-5,4]`  
**输出**：`6`  
**解释**：子数组 `[4,-1,2,1]` 的和最大，为 `6`。

**示例 2**  
**输入**：`nums = [1]`  
**输出**：`1`  
**解释**：子数组 `[1]` 的和为 `1`，即为最大和。

**示例 3**  
**输入**：`nums = [5,4,-1,7,8]`  
**输出**：`23`  
**解释**：子数组 `[5,4,-1,7,8]` 的和为 `23`，即为最大和。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**枚举所有可能的连续子数组**，计算每个子数组的和，找出最大的那个。  
- **数组**本身就是我们要操作的数据结构，想象成一串数字的珠子。  
- 连续子数组就像从珠子串中挑出一段连续的珠子。  
- 为了快速得到子数组的和，我们可以在枚举时把每个子数组的所有元素相加。

这种做法一定能得到正确答案，因为我们把**所有**可能的子数组都检查了一遍，最大的和自然会被发现。

#### 代码（Python）

```python
def maxSubArray_bruteforce(nums):
    """
    暴力枚举所有连续子数组，返回最大子数组和
    """
    n = len(nums)
    max_sum = -float('inf')          # 先设一个很小的值，方便后面比较

    # i 为子数组的左端点，j 为右端点（左闭右闭）
    for i in range(n):
        cur_sum = 0                  # 从 i 开始累计子数组和
        for j in range(i, n):
            cur_sum += nums[j]       # 累加第 j 个元素
            if cur_sum > max_sum:    # 更新全局最大值
                max_sum = cur_sum
    return max_sum
```

#### 复杂度  

- **时间复杂度：**`O(n²)`  
  解释：外层循环跑 `n` 次，内层平均也跑 `n/2` 次，整体大约是 `n × n`，即 **平方级**。  
  用生活化的说法：如果有 1000 个珠子，暴力解相当于把每一段（约 500,000 条）都数一遍，耗时很长。

- **空间复杂度：**`O(1)`  
  只用了常数个额外变量（`max_sum、cur_sum`），不随输入规模增长。

---  

### 2. 最优解

#### 思路  

从暴力解可以看到，**重复累加**是耗时的根本原因。  
观察累加过程：

- 当我们从左往右遍历数组时，维护一个“**当前子数组的最大和**”。  
- 如果把当前元素 `x` 加到前面的子数组会让和更大，就继续累加；  
- 否则，说明前面的子数组已经“拖累”了，**从 `x` 重新开始**会更好。

这就是 **动态规划** 的思想：  
设 `dp[i]` 为以 `nums[i]` 结尾的最大子数组和。  
则  
```
dp[i] = max(nums[i], dp[i-1] + nums[i])
```
- `nums[i]`：单独把 `i` 当作子数组的开始（相当于“重新开始”）。  
- `dp[i-1] + nums[i]`：把 `i` 接在前面的最大子数组后面。

我们只需要记录**上一次的 dp 值**，不必保留整个数组，空间可以降到 `O(1)`。  
遍历完所有元素后，所有 `dp[i]` 中的最大值即为答案。

这就是著名的 **Kadane 算法**，时间线性 `O(n)`。

#### 代码（Python）

```python
def maxSubArray_kadane(nums):
    """
    Kadane 算法：一次遍历求最大子数组和
    """
    # 第一个元素既是当前子数组的最大和，也是全局最大和的初始值
    cur_max = global_max = nums[0]

    # 从第二个元素开始遍历
    for i in range(1, len(nums)):
        x = nums[i]

        # 如果把 x 加到之前的子数组会更小，就把子数组重新从 x 开始
        cur_max = max(x, cur_max + x)   # 动态规划转移方程

        # 更新全局最大值
        if cur_max > global_max:
            global_max = cur_max

    return global_max
```

#### 复杂度  

- **时间复杂度：**`O(n)`  
  解释：只遍历一次数组，每个元素做 **常数** 次计算。  
  生活化说法：如果有 100 万个珠子，只需要顺着珠子走一遍，就能算出答案，速度非常快。

- **空间复杂度：**`O(1)`  
  只用了几个变量 (`cur_max、global_max`) 与输入规模无关。

---

## 心得

- **核心技巧**：**动态规划 + 贪心**（Kadane），把“是否继续累加”这个决定压缩成一次比较。  
- **适用的题型**：  
  1. **最大子数组乘积**（同样用 DP 记录正负乘积）  
  2. **最长递增子序列的连续版**（如最长连续递增子数组）  
  3. **最大连续 1 的长度**（二进制数组）  
- **一句话总结解题钥匙**：**“遇到需要在连续区间上求最值时，尝试用‘当前最优 + 新元素’ 与 ‘仅新元素’ 两者比较”。**

---

## 反思

- **第一反应**：立刻想到枚举所有子数组（暴力），因为这样最直观、最保险。  
- **最容易踩的坑**：  
  - 忘记在遍历开始时把 `global_max` 初始化为 `nums[0]`（如果用 `-inf`，在全负数情况下仍然会得到正确答案，但要小心）。  
  - 没考虑 **全负数** 的情况，若直接把 `cur_max` 初始化为 `0`，会错误地返回 `0`。  
- **下次类似题的第一步**：先问自己“**是否可以把问题拆成‘以当前位置结束的最优解’**”，如果能，就立刻写出 DP 转移方程并尝试把空间压到 `O(1)`。