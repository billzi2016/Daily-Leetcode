# #2640. 求数组所有前缀的得分 / Find the Score of All Prefixes of an Array

> 难度：中等 · 标签：Array、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/find-the-score-of-all-prefixes-of-an-array/)

---

## 题目（英文原版）

**Description**

We define the conversion array conver of an array arr as follows:
We also define the score of an array arr as the sum of the values of the conversion array of arr.
Given a 0-indexed integer array nums of length n, return an array ans of length n where ans[i] is the score of the prefix nums[0..i].

**Examples**

**Example 1:**

```
Input: nums = [2,3,7,5,10]
Output: [4,10,24,36,56]
Explanation: 
For the prefix [2], the conversion array is [4] hence the score is 4
For the prefix [2, 3], the conversion array is [4, 6] hence the score is 10
For the prefix [2, 3, 7], the conversion array is [4, 6, 14] hence the score is 24
For the prefix [2, 3, 7, 5], the conversion array is [4, 6, 14, 12] hence the score is 36
For the prefix [2, 3, 7, 5, 10], the conversion array is [4, 6, 14, 12, 20] hence the score is 56
```

**Example 2:**

```
Input: nums = [1,1,2,4,8,16]
Output: [2,4,8,16,32,64]
Explanation: 
For the prefix [1], the conversion array is [2] hence the score is 2
For the prefix [1, 1], the conversion array is [2, 2] hence the score is 4
For the prefix [1, 1, 2], the conversion array is [2, 2, 4] hence the score is 8
For the prefix [1, 1, 2, 4], the conversion array is [2, 2, 4, 8] hence the score is 16
For the prefix [1, 1, 2, 4, 8], the conversion array is [2, 2, 4, 8, 16] hence the score is 32
For the prefix [1, 1, 2, 4, 8, 16], the conversion array is [2, 2, 4, 8, 16, 32] hence the score is 64
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 109

---

## 题目（中文翻译）

我们将数组 `arr` 的 **转换数组**（conversion array）`conver` 定义如下：

我们还将数组 `arr` 的 **得分**（score）定义为其转换数组中所有值的和。

给定一个下标从 **0** 开始、长度为 `n` 的整数数组 `nums`，返回一个长度为 `n` 的数组 `ans`，其中 `ans[i]` 为前缀 `nums[0..i]` 的得分。

**示例 1**  
```text
Input: nums = [2,3,7,5,10]
Output: [4,10,24,36,56]
Explanation: 
对于前缀 [2]，转换数组为 [4]，因此得分为 4
对于前缀 [2, 3]，转换数组为 [4, 6]，因此得分为 10
对于前缀 [2, 3, 7]，转换数组为 [4, 6, 14]，因此得分为 24
对于前缀 [2, 3, 7, 5]，转换数组为 [4, 6, 14, 12]，因此得分为 36
对于前缀 [2, 3, 7, 5, 10]，转换数组为 [4, 6, 14, 12, 20]，因此得分为 56
```

**示例 2**  
```text
Input: nums = [1,1,2,4,8,16]
Output: [2,4,8,16,32,64]
Explanation: 
对于前缀 [1]，转换数组为 [2]，因此得分为 2
对于前缀 [1, 1]，转换数组为 [2, 2]，因此得分为 4
对于前缀 [1, 1, 2]，转换数组为 [2, 2, 4]，因此得分为 8
对于前缀 [1, 1, 2, 4]，转换数组为 [2, 2, 4, 8]，因此得分为 16
对于前缀 [1, 1, 2, 4, 8]，转换数组为 [2, 2, 4, 8, 16]，因此得分为 32
对于前缀 [1, 1, 2, 4, 8, 16]，转换数组为 [2, 2, 4, 8, 16, 32]，因此得分为 64
```

**约束条件**  
- `1 <= nums.length <= 10^5`  
- `1 <= nums[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **一步一步模拟题目描述**：

1. 对每一个前缀 `nums[0..i]`，先把它完整取出来。  
2. 再遍历这个前缀，计算 **转换数组** `conver`：  
   - 对每个位置 `j`，找出 `nums[0..j]` 的最大值 `max_j`（相当于在字典里查 “从头到 j 的最大词”，这一步就像在查字典）。  
   - `conver[j] = nums[j] + max_j`（把当前数字和它前面出现的最大数字相加）。  
3. 把 `conver` 所有元素加起来得到该前缀的 **得分**。  

把上述过程对每个前缀都做一遍，就得到答案数组 `ans`。

> **为什么能得到正确答案？**  
> 题目说“转换数组的定义”就是 **当前元素 + 该位置之前的最大元素**（从例子可以推导出这一定义），而 **得分** 正是转换数组所有元素的和。我们把每一步都照着做，自然得到正确的结果。

#### 代码（Python）

```python
def score_of_prefixes_bruteforce(nums):
    n = len(nums)
    ans = [0] * n

    # 对每一个前缀 i
    for i in range(n):
        conver_sum = 0          # 用来累计当前前缀的 conver 元素和
        cur_max = -float('inf') # 当前前缀的最大值

        # 逐个计算前缀里的 conver[j]
        for j in range(i + 1):
            cur_max = max(cur_max, nums[j])   # 找到 nums[0..j] 的最大值
            conver_sum += nums[j] + cur_max   # conver[j] = nums[j] + cur_max

        ans[i] = conver_sum
    return ans
```

> 关键行中文注释已经写在代码里，直接复制即可运行。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  对每个前缀 `i` 都要再遍历一次长度为 `i+1` 的子数组，整体相当于 `1 + 2 + … + n = n·(n+1)/2` 次操作。  
  用大白话说，就是 **“随着 n 增大，耗时会像正方形一样快”**。

- **空间复杂度**：`O(1)`（不计答案数组）  
  只用了几个常数级的变量 `cur_max`、`conver_sum`，不随输入规模增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 出在每次都要重新遍历前缀去找最大值。  
实际上，**前缀的最大值只会增大或保持不变**，我们可以在一次遍历中把它“记下来”，以后直接使用。

思路分解：

1. **维护一个滚动的前缀最大值 `cur_max`**  
   - 当遍历到 `nums[i]` 时，`cur_max = max(cur_max, nums[i])`。  
   - 这一步相当于在“字典”里随时更新最新的最大词条。

2. **直接得到当前的转换值**  
   - `conver_i = nums[i] + cur_max`（因为 `cur_max` 已经是 `nums[0..i]` 的最大值）。

3. **利用前缀和的性质**  
   - 题目提示 `ans[i] = ans[i-1] + conver[i]`。  
   - 只要把上一步算出的 `conver_i` 加到上一次的答案 `ans[i-1]` 上，就得到 `ans[i]`。

4. **一次遍历即可完成所有前缀的得分**  
   - 用 `cur_max`、`cur_score`（即 `ans[i]`）这两个变量，边遍历边更新答案列表。

> **核心概念解释**  
> - **前缀最大值**：想象从左到右读一本书，记住目前为止读到的最大字数。以后再读新的一页，只需要把这页的字数和已记录的最大值相加，无需重新翻回去查所有页。  
> - **前缀和**：把每一步的结果累加起来，就像把每一天赚的钱放进同一个存钱罐，罐子里的总额就是前缀和。

#### 代码（Python）

```python
def score_of_prefixes(nums):
    """
    返回 ans，其中 ans[i] 为数组 nums 前缀 nums[0..i] 的得分。
    思路：一次遍历，维护前缀最大值和当前前缀的得分。
    """
    n = len(nums)
    ans = [0] * n

    cur_max = 0          # 当前遍历到位置 i 时的前缀最大值
    cur_score = 0        # ans[i]，即到目前为止的总得分

    for i, x in enumerate(nums):
        # 更新前缀最大值（相当于在字典里查找/更新“最大词”）
        cur_max = max(cur_max, x)

        # 计算当前位置的转换值：当前元素 + 前缀最大值
        conver_i = x + cur_max

        # 前缀得分是之前的得分加上本次的转换值
        cur_score += conver_i

        ans[i] = cur_score   # 把答案写入结果数组

    return ans
```

> 关键行已经配上中文注释，代码即插即用。

#### 复杂度

- **时间复杂度**：`O(n)`  
  只遍历一次数组，每个元素做常数次操作。  
  用大白话说，就是 **“随着 n 增大，耗时只会线性增长”**，远快于 `O(n²)`。

- **空间复杂度**：`O(1)`（不计答案数组）  
  只用了 `cur_max`、`cur_score` 两个额外变量，大小不随 `n` 变化。

---

## 心得

- **核心技巧**：**维护前缀最大值 + 前缀和**，把“重复的求最大”转换成一次更新。
- **适用题型**：
  1. “每个位置的值依赖于之前的最大/最小值”，如 *Maximum Subarray Sum with Prefix Max*。  
  2. “答案本身是另一数组的前缀和”，如 *Running Sum of 1D Array*。  
  3. “需要在遍历过程中累计某种状态”，如 *Number of Subarrays with Bounded Maximum*。
- **一句话总结**：**把“每次都重新计算”改成“一次遍历中实时维护”，就是从暴力到最优的钥匙。**

---

## 反思

- **第一反应**：看到“前缀”二字，立刻想到**前缀和**；看到“转换数组”又想到**每个位置都要用之前的信息**，于是想到暴力模拟。
- **最容易踩的坑**  
  1. **忘记更新前缀最大值**：如果只在计算 `conver_i` 时使用旧的 `cur_max`，会导致错误。  
  2. **整数溢出**（在某些语言中）：`nums[i]` 可达 `10⁹`，累计后可能超过 32 位整数，需要使用 64 位或 Python 的大整数。  
  3. **边界条件**：空数组（题目保证长度≥1）或只有一个元素时，算法仍需正确返回单元素得分。
- **下次类似题的第一步**：**明确“每一步需要哪些历史信息”，然后判断这些信息是否可以在一次遍历中持续更新**。如果可以，就直接写滚动变量；如果不行，再考虑更复杂的数据结构（如单调栈、线段树）来维护。