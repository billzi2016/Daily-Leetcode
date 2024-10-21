# #2909. 山峰三元组的最小和 II / Minimum Sum of Mountain Triplets II

> 难度：中等 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/minimum-sum-of-mountain-triplets-ii/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array nums of integers.
A triplet of indices (i, j, k) is a mountain if:
Return the minimum possible sum of a mountain triplet of nums. If no such triplet exists, return -1.

**Examples**

**Example 1:**

```
Input: nums = [8,6,1,5,3]
Output: 9
Explanation: Triplet (2, 3, 4) is a mountain triplet of sum 9 since: 
- 2 < 3 < 4
- nums[2] < nums[3] and nums[4] < nums[3]
And the sum of this triplet is nums[2] + nums[3] + nums[4] = 9. It can be shown that there are no mountain triplets with a sum of less than 9.
```

**Example 2:**

```
Input: nums = [5,4,8,7,10,2]
Output: 13
Explanation: Triplet (1, 3, 5) is a mountain triplet of sum 13 since: 
- 1 < 3 < 5
- nums[1] < nums[3] and nums[5] < nums[3]
And the sum of this triplet is nums[1] + nums[3] + nums[5] = 13. It can be shown that there are no mountain triplets with a sum of less than 13.
```

**Example 3:**

```
Input: nums = [6,5,4,3,4,5]
Output: -1
Explanation: It can be shown that there are no mountain triplets in nums.
```

**Constraints**

- 3 <= nums.length <= 105
- 1 <= nums[i] <= 108

---

## 题目（中文翻译）

**题目描述**  
给定一个下标从 0 开始的整数数组 `nums`。  
如果满足以下条件，则索引三元组 `(i, j, k)` 被称为**山峰三元组（mountain triplet）**：

- `i < j < k`
- `nums[i] < nums[j]` 且 `nums[k] < nums[j]`

返回 `nums` 中任意山峰三元组的 **最小可能和**。如果不存在这样的三元组，返回 `-1`。

**示例**

> 示例 1  
> 输入: `nums = [8,6,1,5,3]`  
> 输出: `9`  
> 解释: 三元组 `(2, 3, 4)` 是山峰三元组，和为 `9`，因为  
> - `2 < 3 < 4`  
> - `nums[2] < nums[3]` 且 `nums[4] < nums[3]`  
> 该三元组的和为 `nums[2] + nums[3] + nums[4] = 9`。可以证明不存在和小于 `9` 的山峰三元组。

> 示例 2  
> 输入: `nums = [5,4,8,7,10,2]`  
> 输出: `13`  
> 解释: 三元组 `(1, 3, 5)` 是山峰三元组，和为 `13`，因为  
> - `1 < 3 < 5`  
> - `nums[1] < nums[3]` 且 `nums[5] < nums[3]`  
> 该三元组的和为 `nums[1] + nums[3] + nums[5] = 13`。可以证明不存在和小于 `13` 的山峰三元组。

> 示例 3  
> 输入: `nums = [6,5,4,3,4,5]`  
> 输出: `-1`  
> 解释: 可以证明 `nums` 中不存在山峰三元组。

**约束条件**

- `3 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^8`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法就是把所有可能的三元组都枚举一遍，检查它们是否满足山形条件：  

- 下标满足 `i < j < k`；  
- `nums[i] < nums[j]` 并且 `nums[k] < nums[j]`。  

如果满足，就计算它们的和 `nums[i] + nums[j] + nums[k]`，在所有合法的山形三元组中取最小值。  

这里用到的唯一数据结构是 **普通的数组**，我们只需要用三个嵌套的 `for` 循环遍历下标。  

这种方法之所以**一定能得到正确答案**，是因为我们没有漏掉任何可能的 `(i, j, k)`，只要遍历完整个搜索空间，最小的合法和自然会被找到。  

> **时间复杂度的直观解释**  
> - 第一个循环要跑 `n` 次，第二个循环在每一次外层循环里最多跑 `n` 次，第三个循环同理。于是总共的操作次数大约是 `n × n × n = n³`，这就是 **O(n³)**。  
> - “O” 只关心数量级的增长快慢，实际的常数（比如每次循环里做了几行代码）在大 O 记号里被省略了。  

#### 代码（Python）  

```python
def minimumMountainSum_bruteforce(nums):
    n = len(nums)
    ans = float('inf')                     # 用正无穷表示“还没有找到合法三元组”
    
    # 枚举所有 i < j < k 的组合
    for i in range(n - 2):                 # i 最多到 n-3
        for j in range(i + 1, n - 1):      # j 必须在 i 右边，且留出 k 的位置
            if nums[i] >= nums[j]:        # 先排除不满足左侧升高的情况，省点时间
                continue
            for k in range(j + 1, n):     # k 必须在 j 右边
                if nums[k] < nums[j]:     # 右侧也要比 j 小
                    cur = nums[i] + nums[j] + nums[k]
                    ans = min(ans, cur)   # 更新最小和

    return -1 if ans == float('inf') else ans
```

#### 复杂度  
- **时间复杂度**：`O(n³)` —— 三层循环，每层最多遍历 `n` 次。  
- **空间复杂度**：`O(1)` —— 只用了常数个额外变量（`ans、i、j、k、cur`），不随输入规模增长。

---

### 2. 最优解  

#### 思路  
暴力解的主要瓶颈在于**大量重复的比较**。  
对于固定的中间下标 `j`，我们只需要找到：

1. **左侧**：在 `j` 左边且 `< nums[j]` 的最小元素 `left`。  
2. **右侧**：在 `j` 右边且 `< nums[j]` 的最小元素 `right`。  

如果这两个元素都存在，那么 `left + nums[j] + right` 就是以 `j` 为山峰的唯一可能的最小和。于是我们只需要在所有 `j` 中取最小的那一个即可。

**如何快速得到 left / right？**  
- **左侧最小值**：遍历数组一次，维护一个前缀最小数组 `prefix_min[i]`，表示 `nums[0..i]` 中的最小元素。  
  - 对于位置 `j`，左侧候选就是 `prefix_min[j-1]`（因为 `j-1` 已经包含了所有左边的数）。  
- **右侧最小值**：同理，遍历一次得到后缀最小数组 `suffix_min[i]`，表示 `nums[i..n-1]` 中的最小元素。  
  - 对于位置 `j`，右侧候选就是 `suffix_min[j+1]`。  

这样，**每个 j 只做 O(1) 的查询**，整体只需要两次线性遍历即可完成，时间降到 `O(n)`。

> **前缀/后缀最小的类比**  
> 想象你在阅读一本书，想随时知道“从第一页到当前页”里出现的最小页码是什么，你可以在翻页时把当前的最小页码记录下来，这就是前缀最小。后缀最小则相反，从书的最后一页往前记录最小页码。  

#### 代码（Python）  

```python
def minimumMountainSum(nums):
    n = len(nums)
    if n < 3:
        return -1

    # ---------- 1. 预处理前缀最小 ----------
    prefix_min = [0] * n
    cur_min = nums[0]
    for i in range(n):
        cur_min = min(cur_min, nums[i])
        prefix_min[i] = cur_min
    # prefix_min[i] = min(nums[0..i])

    # ---------- 2. 预处理后缀最小 ----------
    suffix_min = [0] * n
    cur_min = nums[-1]
    for i in range(n - 1, -1, -1):
        cur_min = min(cur_min, nums[i])
        suffix_min[i] = cur_min
    # suffix_min[i] = min(nums[i..n-1])

    # ---------- 3. 枚举山峰 j ----------
    ans = float('inf')
    for j in range(1, n - 1):          # j 不能是最左或最右
        left = prefix_min[j - 1]      # 左侧最小值
        right = suffix_min[j + 1]     # 右侧最小值

        # 必须同时满足 left < nums[j] 且 right < nums[j]
        if left < nums[j] and right < nums[j]:
            cur_sum = left + nums[j] + right
            ans = min(ans, cur_sum)

    return -1 if ans == float('inf') else ans
```

#### 复杂度  
- **时间复杂度**：`O(n)` —— 两次线性遍历（前缀、后缀）+一次遍历 `j`，总共是线性规模。相比暴力的 `O(n³)`，快了很多。  
- **空间复杂度**：`O(n)` —— 需要两个额外的数组 `prefix_min`、`suffix_min` 来保存每个位置的最小值。  

---

## 心得  

- **核心技巧**：前缀最小 / 后缀最小的预处理。它把“在区间里找最小值”这个查询从 **每次 O(n)** 降到了 **O(1)**。  
- **适用场景**：  
  1. “在左侧/右侧寻找满足条件的最优元素”类题目（如 “Maximum Sum of Increasing Triplet”）。  
  2. 需要对每个位置的**左/右区间信息**快速获取的题目（如 “Best Sightseeing Pair”）。  
  3. 任何可以通过一次扫描累计信息的**前缀/后缀**问题。  
- **一句话总结解题钥匙**：**把全局搜索转化为局部最优查询，利用前缀/后缀数组把查询时间压到常数**。

---

## 反思  

- **第一反应**：看到 “i < j < k 且两侧都比中间小”，立刻想到枚举三元组。  
- **最容易踩的坑**：  
  - 忘记检查 **左侧最小值必须真的小于 `nums[j]`**（前缀最小可能等于或大于 `nums[j]`，此时该 `j` 不是合法山峰）。  
  - 边界处理：`j` 不能取到最左或最右，否则左/右侧没有元素。  
  - 当数组长度只有 3 时仍需正常工作。  
- **下次类似题目第一步**：先思考 **“对于每个中心位置，我需要左边/右边的什么信息？”**，如果是“最小”“最大”“最近满足条件的值”，就考虑用 **前缀/后缀数组** 或 **单调栈/有序集合** 来预处理。