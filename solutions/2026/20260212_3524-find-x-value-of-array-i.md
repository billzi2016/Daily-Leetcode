# #3524. 数组的 X 值 I / Find X Value of Array I

> 难度：中等 · 标签：Array、Math、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/find-x-value-of-array-i/)

---

## 题目（英文原版）

**Description**

You are given an array of positive integers nums, and a positive integer k.
You are allowed to perform an operation once on nums, where in each operation you can remove any non-overlapping prefix and suffix from nums such that nums remains non-empty.
You need to find the x-value of nums, which is the number of ways to perform this operation so that the product of the remaining elements leaves a remainder of x when divided by k.
Return an array result of size k where result[x] is the x-value of nums for 0 <= x <= k - 1.
A prefix of an array is a subarray that starts from the beginning of the array and extends to any point within it.
A suffix of an array is a subarray that starts at any point within the array and extends to the end of the array.
Note that the prefix and suffix to be chosen for the operation can be empty.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,4,5], k = 3
Output: [9,2,4]
Explanation:
```

**Example 2:**

```
Input: nums = [1,2,4,8,16,32], k = 4
Output: [18,1,2,0]
Explanation:
```

**Example 3:**

```
Input: nums = [1,1,2,1,1], k = 2
Output: [9,6]
```

**Constraints**

- 1 <= nums[i] <= 109
- 1 <= nums.length <= 105
- 1 <= k <= 5

---

## 题目（中文翻译）

给定一个由正整数构成的数组 `nums`，以及一个正整数 `k`。  
你可以对 `nums` **进行一次操作**：在一次操作中，你可以删除 `nums` 的任意 **不相交的前缀（prefix）和后缀（suffix）**，要求删除后数组仍然非空。  
前缀是指从数组开头开始直到任意位置的子数组（subarray），后缀是指从任意位置开始一直到数组结尾的子数组（subarray）。  
需要计算 `nums` 的 **x‑value**，即在满足上述操作后，**剩余元素的乘积（product）除以 `k` 的余数为 `x` 的不同操作方式的数量**。  
返回一个大小为 `k` 的数组 `result`，其中 `result[x]` 表示 `0 ≤ x ≤ k‑1` 时的 x‑value。

**注意**  
- 可以选择的前缀和后缀均可以为空。  
- 删除前缀和后缀后，数组必须至少保留一个元素。

### 示例

**示例 1**  
```text
Input: nums = [1,2,3,4,5], k = 3
Output: [9,2,4]
Explanation: 
我们枚举所有合法的前缀/后缀删除方式，共有 15 种。计算剩余元素乘积对 3 的余数后，余数为 0 的方式有 9 种，余数为 1 的方式有 2 种，余数为 2 的方式有 4 种。因此 result = [9,2,4]。
```

**示例 2**  
```text
Input: nums = [1,2,4,8,16,32], k = 4
Output: [18,1,2,0]
Explanation: 
通过遍历所有合法的删除方案，统计乘积模 4 的结果可得：余数 0 出现 18 次，余数 1 出现 1 次，余数 2 出现 2 次，余数 3 未出现。因此 result = [18,1,2,0]。
```

**示例 3**  
```text
Input: nums = [1,1,2,1,1], k = 2
Output: [9,6]
Explanation: 
所有合法操作共计 15 种，其中乘积为偶数（余数 0）有 9 种，乘积为奇数（余数 1）有 6 种，故 result = [9,6]。
```

### 约束条件
- `1 ≤ nums[i] ≤ 10^9`
- `1 ≤ nums.length ≤ 10^5`
- `1 ≤ k ≤ 5`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
题目说「把数组的一个前缀和一个后缀删掉，剩下的子数组乘积模 k 等于 x」，其实这等价于 **统计所有非空连续子数组**（即任意 `i … j`）的乘积对 `k` 的余数。  

最直接的想法就是把每一对起始下标 `i` 和结束下标 `j` 都枚举一遍，逐个累乘并取模，记下余数出现的次数。  

- **数据结构**：只需要几个整数计数，最外层用一个长度为 `k` 的列表 `ans` 来存每个余数出现的次数。  
- **生活化类比**：把数组看成一排商品，暴力解就像让你把每一种可能的“买几件从第 i 件到第 j 件”的组合都尝一遍，记下每次付款后找零（余数）是多少。  

为什么这种办法一定能得到正确答案？因为我们把 **所有** 合法子数组都遍历了一遍，漏掉的情况为零，所以计数自然完整。

#### 代码（Python）  

```python
def x_value_bruteforce(nums, k):
    """
    暴力枚举所有子数组，统计乘积 % k 的出现次数
    时间复杂度 O(n^2) ，空间复杂度 O(k)
    """
    n = len(nums)
    ans = [0] * k                     # ans[r] = 子数组乘积 % k == r 的个数

    for i in range(n):                # 子数组左端点
        prod = 1                       # 累乘从 i 开始的子数组
        for j in range(i, n):          # 子数组右端点
            prod = (prod * nums[j]) % k   # 每乘一个数就取模，防止溢出
            ans[prod] += 1                # 记录当前余数
    return ans
```

> **关键行解释**  
> - `prod = (prod * nums[j]) % k`：相当于“每买进一件商品，就立刻算一次找零”，这样乘积永远不会爆掉（`nums[i] ≤ 10^9`，直接相乘会超出 Python 整数的常规范围）。  
> - `ans[prod] += 1`：把这一次的找零记录下来。

#### 复杂度  

- **时间复杂度**：`O(n²)`。  
  - `n` 是数组长度。外层遍历 `n` 次，内层最坏也要遍历 `n` 次，等价于把 `n*(n+1)/2`（约 `n²/2`）个子数组都算一遍。  
  - 大白话：如果数组有 10 000 个元素，暴力解大概要算 5 0 0 0 0 0 0 0 0（5 亿）次，明显太慢。

- **空间复杂度**：`O(k)`。  
  - 只用了长度为 `k` 的结果数组，`k ≤ 5`，几乎可以忽略不计。

---

### 2. 最优解  

#### 思路  

从暴力解看出 **瓶颈** 在于每次都要从左端点重新累乘，导致 `O(n²)`。  
我们注意到 **乘积的模运算只跟前缀的模值有关**，于是可以用 **动态规划** 把“从左端点开始的所有子数组”压缩成 `k` 个状态。

> **核心概念——状态**  
> - `dp[r]` 表示「以**当前元素的左侧**为结尾的子数组（即已经遍历到当前位置之前的子数组）中，乘积模 `k` 等于 `r` 的个数」。
> - `k ≤ 5`，所以状态只有 `0 … k‑1`，可以直接放进一个长度为 `k` 的列表里。

遍历数组时，对每个新出现的元素 `a = nums[i]`：

1. **把所有已有的子数组延长**：  
   之前以 `i‑1` 为右端点、模值为 `r` 的子数组乘积是 `r`。  
   把 `a` 再乘进去后，新模值 = `(r * a) % k`。  
   所以 `new_dp[(r * a) % k] += dp[r]`。

2. **新建只包含 `a` 的子数组**：  
   余数是 `a % k`，计数加 `1`。

把这两步得到的 `new_dp` 累加到答案 `ans`（因为所有以 `i` 为右端点的子数组都是合法的），随后把 `dp ← new_dp` 继续向后走。

整个过程只遍历一次数组，每个元素只和 `k` 个状态做乘法，时间 `O(n·k)`，空间 `O(k)`。

> **类比**：把数组想成一条流水线，`dp` 记录了「截至目前」每种颜色（余数）的小零件有多少；新来的零件 `a` 进来后，会把旧零件染色（乘模）成新的颜色，同时自己也会产生一个新零件。我们只关心每种颜色的数量，不必记住每个零件的具体位置。

#### 代码（Python）  

```python
def x_value(nums, k):
    """
    动态规划 O(n * k) 求所有子数组乘积 % k 的出现次数
    n = len(nums) , k <= 5
    """
    ans = [0] * k          # 最终结果，ans[r] = 余数 r 的出现次数
    dp = [0] * k           # dp[r] = 以当前元素左侧为结尾的子数组余数为 r 的个数

    for a in nums:         # 依次处理每个元素
        ndp = [0] * k      # 用来保存“以当前元素为右端点”的子数组计数

        # 1) 让已有子数组延长一位
        for r in range(k):
            if dp[r]:                     # 只对出现过的状态进行转移
                new_r = (r * a) % k
                ndp[new_r] += dp[r]

        # 2) 只包含当前元素的子数组
        ndp[a % k] += 1

        # 3) 把以 i 为右端点的所有子数组计数累加到答案中
        for r in range(k):
            ans[r] += ndp[r]

        # 4) 为下一轮准备 dp
        dp = ndp

    return ans
```

> **关键行解释**  
> - `new_r = (r * a) % k`：把旧子数组的余数 `r` 再乘上新元素 `a`，然后取模得到新余数。  
> - `ndp[a % k] += 1`：单独的子数组 `[a]` 也要算进去。  
> - `ans[r] += ndp[r]`：所有以当前元素结尾的子数组都是合法的，把它们的计数直接加到全局答案里。

#### 复杂度  

- **时间复杂度**：`O(n * k)`。  
  - `n ≤ 10⁵`，`k ≤ 5`，最多约 `5 × 10⁵` 次简单的乘法和加法，几乎是线性时间。  
  - 与暴力的 `O(n²)`（对 10⁵ 的数组相当于 10¹⁰ 次运算）相比，快了 **几个数量级**。

- **空间复杂度**：`O(k)`。  
  - 只用了 `dp`、`ndp`、`ans` 三个长度为 `k` 的列表，常数级别的额外空间。

---

## 心得  

- **核心技巧**：用「以当前位置为右端点的子数组」的 **动态规划**（状态压缩）来统计所有子数组的某种属性（这里是乘积模 `k`）。  
- **适用题型**：  
  1. 统计子数组和/乘积的模值（如 “子数组和为 k 的倍数”）。  
  2. 计数满足某种前缀/后缀关系的子数组（如 “前缀和相同的子数组”）。  
  3. 类似的 “子序列/子数组的乘积/和的离散化计数” 场景。  
- **一句话总结**：**把所有子数组压缩到 `k` 种余数的计数上，边遍历边更新，时间线性，空间常数。**

---

## 反思  

- **第一反应**：看到“删除前缀和后缀”，立刻把它转化成“统计所有连续子数组”。这一步是关键的抽象。  
- **最容易踩的坑**：  
  - **乘积溢出**：直接相乘会爆掉，必须在每一步都取模。  
  - **空前缀/后缀**：允许空前缀或空后缀，等价于所有非空子数组都合法，别忘了把单元素子数组计入。  
  - **状态更新顺序**：在同一轮里必须使用上一次的 `dp`（旧状态）来生成 `ndp`，否则会出现“同一元素被多次使用”的错误。  
- **下次遇到同类题**：第一步先 **把题目转化为“统计所有子数组/子序列的某个函数值”**，然后思考 **是否可以用前缀/后缀的累计信息（前缀和、前缀乘积）做状态压缩**，尤其是当模数或目标值范围很小的时候。