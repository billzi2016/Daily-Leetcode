# #238. 除自身之外数组的乘积 / Product of Array Except Self

> 难度：中等 · 标签：Array、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/product-of-array-except-self/)

---

## 题目（英文原版）

**Description**

Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i].
The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.
You must write an algorithm that runs in O(n) time and without using the division operation.
Follow up: Can you solve the problem in O(1) extra space complexity? (The output array does not count as extra space for space complexity analysis.)

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,4]
Output: [24,12,8,6]
```

**Example 2:**

```
Input: nums = [-1,1,0,-3,3]
Output: [0,0,9,0,0]
```

**Constraints**

- 2 <= nums.length <= 105
- -30 <= nums[i] <= 30
- The input is generated such that answer[i] is guaranteed to fit in a 32-bit integer.

---

## 题目（中文翻译）

给定一个整数数组 `nums`，返回一个数组 `answer`，其中 `answer[i]` 等于 `nums` 中所有元素的乘积，但 **不包括** `nums[i]` 本身。  
题目保证 `nums` 任意前缀（prefix）或后缀（suffix）的乘积都能装入 32 位整数。  

要求实现的算法时间复杂度为 **O(n)**，且**不能使用除法（division）**运算。

**示例 1**  
**示例 2**  

**约束条件**  
- 2 ≤ `nums.length` ≤ 10⁵  
- -30 ≤ `nums[i]` ≤ 30  
- 输入保证 `answer[i]` 必然能装入 32 位整数  

**进阶**：能否在 **O(1)** 额外空间复杂度下完成此题？（输出数组 `answer` 本身不计入额外空间。）

---

**示例**

**示例 1**  
```
输入: nums = [1,2,3,4]
输出: [24,12,8,6]
```

**示例 2**  
```
输入: nums = [-1,1,0,-3,3]
输出: [0,0,9,0,0]
```

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：对每一个位置 `i`，把数组里除 `i` 本身之外的所有数都乘起来，得到 `answer[i]`。  
- **数据结构**：只需要原始的列表 `nums`，以及一个同长度的结果列表 `ans`。可以把它想象成厨房里的**配料表**，我们把每一种配料（数组元素）都放进锅里，只是每次把一种配料暂时拿出来不放进去，就得到对应的“除自己之外的配料组合”。  
- **为什么正确**：因为题目要求的正是“除去自身以外的所有数的乘积”，遍历所有其它位置并相乘自然可以得到正确答案。  
- **时间/空间复杂度**：  
  - 对每个 `i`（共 `n` 个），都要遍历一次整个数组（`n` 次），所以总共做了 `n × n = n²` 次乘法，记作 **O(n²)**。这里的 **O** 表示“数量级”，也就是说当数组长度翻倍时，运算次数会变成原来的 **4 倍**。  
  - 额外空间只用了一个和输入等长的结果数组 `ans`，空间复杂度是 **O(n)**（因为我们必须把每个答案保存下来）。  

#### 代码（Python）  

```python
from typing import List

def productExceptSelf_bruteforce(nums: List[int]) -> List[int]:
    n = len(nums)
    ans = [1] * n                     # 先准备好长度相同的答案列表，默认值为 1
    for i in range(n):                # 对每个位置 i
        prod = 1                       # 用来累计除 i 之外的乘积
        for j in range(n):            # 再遍历一次整个数组
            if i == j:                 # 跳过自己
                continue
            prod *= nums[j]            # 累乘其它位置的数
        ans[i] = prod                  # 把结果写进答案列表
    return ans
```

#### 复杂度  

- **时间复杂度**：O(n²) —— 需要两层循环，外层 `n` 次，内层最多 `n` 次。  
- **空间复杂度**：O(n) —— 只额外用了存放答案的数组 `ans`（输出数组不算在 “额外空间” 里时仍是 O(n)）。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**重复计算** 是主要的性能瓶颈：对每个 `i`，我们都要遍历整个数组去乘积。实际上，很多乘积是可以**共享**的。  

**关键观察**：  
- 对于位置 `i`，答案等于 **左侧所有数的乘积** × **右侧所有数的乘积**。  
- 左侧乘积只和 `i` 左边的元素有关，右侧乘积只和 `i` 右边的元素有关。  

这就引出了 **前缀乘积（prefix product）** 和 **后缀乘积（suffix product）** 的概念。  
- 前缀乘积：`pre[i] = nums[0] * nums[1] * ... * nums[i-1]`（不包括 `i` 本身）。可以把它想象成从左到右走路时，背包里已经装好的 “左边所有配料”。  
- 后缀乘积：`post[i] = nums[i+1] * ... * nums[n-1]`（不包括 `i` 本身），相当于从右边走来时背包里装的 “右边所有配料”。  

如果我们先把所有前缀乘积算好，再把所有后缀乘积算好，那么 `answer[i] = pre[i] * post[i]` 就可以 ** O(1)** 时间得到。  

**空间优化**：  
- 题目要求 **O(1) 额外空间**（不计输出数组本身）。我们可以把前缀乘积直接写进答案数组 `ans`，随后再用一个临时变量保存后缀乘积，遍历一次数组（从右到左）把后缀乘积乘进去。这样只用了一个额外的标量变量 `suffix`。  

**步骤**  
1. **左到右**：遍历 `nums`，`ans[i]` 保存左侧所有数的乘积（即前缀乘积）。  
2. **右到左**：维护变量 `suffix` 记录当前位置右侧的乘积，遍历时把 `suffix` 乘到 `ans[i]` 上，同时更新 `suffix` 为 `suffix * nums[i]`。  

这样只用了两次线性遍历，时间 **O(n)**，额外空间 **O(1)**（不计输出数组）。

#### 代码（Python）  

```python
from typing import List

def productExceptSelf(nums: List[int]) -> List[int]:
    n = len(nums)
    ans = [1] * n                 # 第一次遍历后，ans[i] 会存左侧乘积

    # 1️⃣ 左侧前缀乘积
    prefix = 1                     # 当前左侧所有数的乘积，初始为空集，乘积为 1
    for i in range(n):
        ans[i] = prefix            # 把左侧乘积写进答案数组
        prefix *= nums[i]          # 更新左侧乘积，加入 nums[i] 为下一个位置的左侧

    # 2️⃣ 右侧后缀乘积（从右往左遍历）
    suffix = 1                     # 当前右侧所有数的乘积，初始为空集
    for i in range(n - 1, -1, -1):
        ans[i] *= suffix           # 右侧乘积乘到已有的左侧乘积上，得到最终答案
        suffix *= nums[i]          # 更新右侧乘积，加入 nums[i] 为下一个位置的右侧

    return ans
```

#### 复杂度  

- **时间复杂度**：O(n) —— 只遍历了两遍数组，每次都是线性规模。相较于暴力的 O(n²)，当 `n` 很大时快得多。  
- **空间复杂度**：O(1) —— 只用了常数个额外变量 `prefix`、`suffix`（输出数组本身不算在额外空间里）。  

---

## 心得  

- **核心技巧**：利用前缀积和后缀积的分治思想，把“除自身之外的乘积”拆成左乘积 × 右乘积。  
- **适用题型**：  
  1. **前缀和/前缀乘** 类题目（如 “求数组的子数组和”）。  
  2. **左右乘积** 需求的题目（如 “求每个位置左侧最大乘积”）。  
  3. 需要 **O(1) 额外空间** 的线性扫描题（如 “移动零”）。  
- **一句话总结**：先把左边的累计结果存下来，再用一个滚动变量把右边的累计结果乘进去，所有位置一次搞定。  

---

## 反思  

- **第一反应**：直接写双层循环遍历每个元素，计算除自身外的乘积。  
- **最容易踩的坑**：  
  - 忘记把乘积的初始值设为 `1`（空乘积的单位元），否则会导致全部结果为 `0`。  
  - 忽视 `0` 的存在：若数组里有多个 `0`，答案里对应位置全是 `0`，但我们的前缀/后缀方法自然会处理好，不需要额外判断。  
  - 把输出数组算进了“额外空间”，导致空间复杂度评估错误。  
- **下次遇到同类题**：第一步先想“能不能把整个问题拆成左侧 + 右侧两部分”，然后判断是否可以用前缀/后缀累计的方式在一次或两次遍历中完成。