# #1567. 正积子数组的最大长度 / Maximum Length of Subarray With Positive Product

> 难度：中等 · 标签：Array、Dynamic Programming、Greedy · [LeetCode 链接](https://leetcode.com/problems/maximum-length-of-subarray-with-positive-product/)

---

## 题目（英文原版）

**Description**

Given an array of integers nums, find the maximum length of a subarray where the product of all its elements is positive.
A subarray of an array is a consecutive sequence of zero or more values taken out of that array.
Return the maximum length of a subarray with positive product.

**Examples**

**Example 1:**

```
Input: nums = [1,-2,-3,4]
Output: 4
Explanation: The array nums already has a positive product of 24.
```

**Example 2:**

```
Input: nums = [0,1,-2,-3,-4]
Output: 3
Explanation: The longest subarray with positive product is [1,-2,-3] which has a product of 6.
Notice that we cannot include 0 in the subarray since that'll make the product 0 which is not positive.
```

**Example 3:**

```
Input: nums = [-1,-2,-3,0,1]
Output: 2
Explanation: The longest subarray with positive product is [-1,-2] or [-2,-3].
```

**Constraints**

- 1 <= nums.length <= 105
- -109 <= nums[i] <= 109

---

## 题目（中文翻译）

给定一个整数数组 `nums`，求出其中乘积（product）为正的子数组（subarray）的最大长度。  
子数组是指从数组中连续取出的零个或多个元素构成的序列。  
返回乘积为正的子数组的最大可能长度。

**示例 1**  
```
输入: nums = [1,-2,-3,4]
输出: 4
解释: 整个数组的乘积为 24，已经是正数，长度为 4。
```

**示例 2**  
```
输入: nums = [0,1,-2,-3,-4]
输出: 3
解释: 最长的乘积为正的子数组是 [1,-2,-3]，其乘积为 6。  
注意，子数组中不能包含 0，因为乘积会变为 0，而 0 不是正数。
```

**示例 3**  
```
输入: nums = [-1,-2,-3,0,1]
输出: 2
解释: 最长的乘积为正的子数组可以是 [-1,-2] 或 [-2,-3]。
```

**约束条件**  
- `1 <= nums.length <= 10^5`  
- `-10^9 <= nums[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有可能的连续子数组都枚举一遍，算出它们的乘积，然后看乘积是正数还是负数，记录下最长的正乘积子数组长度。

- **枚举子数组**：把数组看成一本书的每一页，子数组就是从第 `i` 页翻到第 `j` 页的连续章节。我们可以把每一对 `(i, j)`（`i ≤ j`）都尝试一次。
- **乘积**：把子数组里的每个数字乘起来，就像把每页的数字写在一起形成一个“大数”。如果最后的结果大于 0，则说明这段章节的乘积是正的。
- **记录最大长度**：每次发现正乘积时，用 `j - i + 1`（子数组的长度）去更新答案。

> 为什么这样一定能得到正确答案？因为我们把**所有**合法的子数组都检查了一遍，答案一定在其中。

**复杂度分析**  
- 外层循环遍历起始位置 `i`（`n` 次），内层循环遍历结束位置 `j`（平均约 `n/2` 次），每次都要遍历子数组里的元素去求乘积（最坏 `O(n)`），于是总时间是 `O(n³)`，但我们可以在遍历 `j` 的时候累计乘积，省去一次遍历，时间降到 `O(n²)`。
- 只用了几个整数变量，额外空间是 `O(1)`。

> **大白话**：`O(n²)` 就相当于“如果有 10,000 个数字，你大概要做 100,000,000 次乘法”。在实际面试里，这通常会超时。

#### 代码（Python）

```python
def getMaxLen_bruteforce(nums):
    """
    暴力解：枚举所有子数组，累计乘积，记录最长正乘积子数组的长度。
    时间复杂度 O(n²) ，空间复杂度 O(1)
    """
    n = len(nums)
    ans = 0

    for i in range(n):                     # 子数组左端点
        prod = 1                            # 累计乘积，从左往右扩展
        for j in range(i, n):               # 子数组右端点
            prod *= nums[j]                 # 把新加入的元素乘进去
            if prod > 0:                    # 乘积为正
                ans = max(ans, j - i + 1)   # 更新最长长度
            # 如果 prod 为 0，后面的任何扩展都会保持 0，直接退出内层循环
            if prod == 0:
                break
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 两层循环遍历所有起止位置，累计乘积的操作是 `O(1)`，所以整体是平方级别。  
- **空间复杂度**：`O(1)` —— 只用了常数个临时变量，没有额外的数组或递归栈。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**大量重复计算**：同一个元素会被乘进很多子数组里。我们需要一种方式，只遍历一次数组，就能得到答案。

关键观察：

1. **零把数组切成独立块**  
   乘积为正的子数组里 **不能出现 0**（因为 0 会把乘积变成 0，不是正数）。所以可以把原数组按照 0 分割成若干段，每段之间互不影响。后面只在每段内部求解。

2. **负数的奇偶性决定正负**  
   - 若一段（不含 0）里的负数个数是 **偶数**，整个段的乘积一定是正的，最长子数组就是整段。  
   - 若负数个数是 **奇数**，整个段的乘积是负的。要想得到正乘积，只能**去掉**段的左侧或右侧的若干元素，使负数的个数变成偶数。最好的办法是：  
     - 删除 **最左边** 的负数（即把左端点移动到第一个负数的下一个位置），或者  
     - 删除 **最右边** 的负数（即把右端点移动到最后一个负数的前一个位置）。  
   两种方案对应的子数组长度分别是  
   `len(segment) - (index_of_first_negative + 1)` 和 `len(segment) - (len(segment) - index_of_last_negative)`，取较大者即为该段的答案。

3. **一次遍历即可得到所有信息**  
   在遍历数组的同时，记录当前段的起始位置、负数出现的次数、第一次负数的下标、最后一次负数的下标。每当遇到 0 或遍历结束时，就可以利用上述公式计算该段的最大正乘积子数组长度，并更新全局答案。

> **类比**：把每段看成一根绳子，绳子上有若干个“标记”（负数）。如果标记数是偶数，整根绳子都可以用；如果是奇数，就只能把最左或最右的标记剪掉，剩下的最长部分就是我们要的。

#### 代码（Python）

```python
def getMaxLen(nums):
    """
    最优解：一次遍历，利用“零切段 + 负数奇偶性”得到最长正乘积子数组长度。
    时间复杂度 O(n) ，空间复杂度 O(1)
    """
    n = len(nums)
    ans = 0                      # 全局最大长度
    start = 0                    # 当前段（不含0）的左端点
    first_neg = -1               # 本段第一次出现负数的下标
    last_neg = -1                # 本段最近一次出现负数的下标
    neg_cnt = 0                  # 本段负数个数

    for i, v in enumerate(nums):
        if v == 0:               # 遇到0，段结束，先处理前面的段
            # 根据负数个数决定本段最大长度
            if neg_cnt % 2 == 0:                 # 负数个数为偶数
                ans = max(ans, i - start)       # 整段都可以用
            else:                                 # 负数个数为奇数
                # 去掉左侧到第一个负数的部分，或右侧到最后一个负数的部分
                left_len = i - (first_neg + 1)   # 去掉左侧
                right_len = (last_neg) - start   # 去掉右侧
                ans = max(ans, left_len, right_len)
            # 重置为新段的起点
            start = i + 1
            first_neg = -1
            last_neg = -1
            neg_cnt = 0
            continue

        # 处理非0元素
        if v < 0:
            neg_cnt += 1
            if first_neg == -1:        # 记录第一次负数的位置
                first_neg = i
            last_neg = i               # 始终更新为最新的负数位置

    # 结束后还可能剩下一个没有被0切断的段，需要再处理一次
    if start < n:                     # 确保数组非空
        if neg_cnt % 2 == 0:
            ans = max(ans, n - start)
        else:
            left_len = n - (first_neg + 1)
            right_len = (last_neg) - start
            ans = max(ans, left_len, right_len)

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历一次数组，每个元素做常数次操作。相比暴力的 `O(n²)`，速度提升了一个数量级。  
- **空间复杂度**：`O(1)` —— 只用了若干整数变量，额外空间不随 `n` 增长。

---

## 心得

- **核心技巧**：利用“零分段 + 负数奇偶性”把原问题转化为局部区间的长度比较。  
- **适用的题型**：  
  1. **子数组乘积符号**（如本题）  
  2. **最长子数组使和为正**（可用前缀和 + 单调栈）  
  3. **数组中最多的连续正数/负数**（同样可以按零切段、统计奇偶性）  
- **一句话总结**：**把数组按零切开，奇负数段只需要删掉最左或最右的负数即可得到最长正乘积子数组**。

---

## 反思

- **第一反应**：直接想到枚举所有子数组，算乘积，记录最长正乘积——这就是暴力解。  
- **最容易踩的坑**：  
  - 忘记 **0** 会把乘积变为 0，导致子数组必须跨不含 0 的连续块。  
  - 处理负数奇数个时，边界条件容易写错（比如只有一个负数的情况）。  
  - 最后一次遍历结束后，别忘了对 **尾部未被 0 截断的段** 再做一次计算。  
- **下次遇到同类题**：第一步先 **“按 0（或其他会破坏性质的元素）把数组划分成独立块”**，再在每块内部利用**奇偶性或单调性**来快速得到答案。