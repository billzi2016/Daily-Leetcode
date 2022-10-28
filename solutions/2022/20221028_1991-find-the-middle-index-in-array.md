# #1991. 寻找数组的中间索引 / Find the Middle Index in Array

> 难度：简单 · 标签：Array、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/find-the-middle-index-in-array/)

---

## 题目（英文原版）

**Description**

Given a 0-indexed integer array nums, find the leftmost middleIndex (i.e., the smallest amongst all the possible ones).
A middleIndex is an index where nums[0] + nums[1] + ... + nums[middleIndex-1] == nums[middleIndex+1] + nums[middleIndex+2] + ... + nums[nums.length-1].
If middleIndex == 0, the left side sum is considered to be 0. Similarly, if middleIndex == nums.length - 1, the right side sum is considered to be 0.
Return the leftmost middleIndex that satisfies the condition, or -1 if there is no such index.
Note: This question is the same as 724: https://leetcode.com/problems/find-pivot-index/

**Examples**

**Example 1:**

```
Input: nums = [2,3,-1,8,4]
Output: 3
Explanation: The sum of the numbers before index 3 is: 2 + 3 + -1 = 4
The sum of the numbers after index 3 is: 4 = 4
```

**Example 2:**

```
Input: nums = [1,-1,4]
Output: 2
Explanation: The sum of the numbers before index 2 is: 1 + -1 = 0
The sum of the numbers after index 2 is: 0
```

**Example 3:**

```
Input: nums = [2,5]
Output: -1
Explanation: There is no valid middleIndex.
```

**Constraints**

- 1 <= nums.length <= 100
- -1000 <= nums[i] <= 1000

---

## 题目（中文翻译）

给定一个 **0 索引** 的整数数组 `nums`，请找到最左侧的 `middleIndex`（即所有满足条件的索引中最小的那个）。  
`middleIndex` 定义为满足以下等式的下标：

```
nums[0] + nums[1] + ... + nums[middleIndex‑1] == nums[middleIndex+1] + nums[middleIndex+2] + ... + nums[nums.length‑1]
```

如果 `middleIndex == 0`，左侧的和视为 `0`；同理，若 `middleIndex == nums.length‑1`，右侧的和视为 `0`。  
返回满足条件的最左侧 `middleIndex`，若不存在则返回 `-1`。

**示例 1**  
**示例 2**  
**示例 3**  

**约束条件**  
- `1 <= nums.length <= 100`  
- `-1000 <= nums[i] <= 1000`

> **注意**：本题与 LeetCode 第 724 题相同：<https://leetcode.com/problems/find-pivot-index/>

**示例**

**示例 1**  
Input: `nums = [2,3,-1,8,4]`  
Output: `3`  
Explanation: 索引 `3` 左侧的数字之和为 `2 + 3 + -1 = 4`，右侧的数字之和为 `4 = 4`。

**示例 2**  
Input: `nums = [1,-1,4]`  
Output: `2`  
Explanation: 索引 `2` 左侧的数字之和为 `1 + -1 = 0`，右侧的数字之和为 `0`。

**示例 3**  
Input: `nums = [2,5]`  
Output: `-1`  
Explanation: 不存在满足条件的 `middleIndex`。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是**逐个检查每个下标**，看它左边的元素和是否等于右边的元素和。  
- 对于下标 `i`，左侧和 = `nums[0] + … + nums[i‑1]`，右侧和 = `nums[i+1] + … + nums[n‑1]`。  
- 如果 `i == 0`，左侧和视为 `0`；如果 `i == n‑1`，右侧和视为 `0`。  
- 只要找到第一个满足条件的 `i`，立刻返回；遍历完都没有则返回 `-1`。  

**数据结构**：这里只用到了 **列表**（存放数组本身）和 **几个整数变量**。可以把 “左侧和” 想成在厨房里把前面的所有调料都称重，右侧和则是把后面的调料称重。  

**为什么正确**：我们把每一个可能的下标都“试一遍”，只要它满足题目要求就一定是答案。因为题目要求返回最左边的下标，遍历顺序本身就保证了这一点。  

**复杂度分析**（大白话版）：  
- 对每个下标 `i`，我们都要重新遍历左边一次、右边一次，最坏情况是 `i` 在中间时左、右各遍历约 `n/2` 次。于是总的操作次数大约是 `1 + 2 + … + n ≈ n²/2`，用 **O(n²)** 表示。  
- 空间上只用了常数个变量（不随 `n` 增长），所以是 **O(1)**。  

#### 代码（Python）  

```python
def findMiddleIndex(nums):
    n = len(nums)
    # 从左到右逐个尝试每个下标
    for i in range(n):
        # 计算左侧和：把 i 前面的所有元素相加
        left_sum = 0
        for j in range(i):
            left_sum += nums[j]          # 左边累加

        # 计算右侧和：把 i 后面的所有元素相加
        right_sum = 0
        for j in range(i + 1, n):
            right_sum += nums[j]         # 右边累加

        # 如果两边相等，就找到了答案
        if left_sum == right_sum:
            return i                     # 返回最左的满足条件的下标

    # 循环结束仍未找到，说明不存在这样的下标
    return -1
```

#### 复杂度  

- **时间复杂度：O(n²)** —— 这里的 `n` 是数组长度。想象成“每检查一个位置，都要把左边和右边的所有东西重新称一遍”，所以会产生二次方的工作量。  
- **空间复杂度：O(1)** —— 只用了几个计数变量，和输入规模无关。  

---  

### 2. 最优解  

#### 思路  
从暴力解可以看到，**重复计算左、右两侧的和是低效的**。  
- **瓶颈**：每次都要遍历一遍左边和右边，导致 `O(n²)`。  
- **关键观察**：如果我们已经知道了 **整个数组的总和**，那么右侧和可以用总和减去左侧和再减去当前元素得到。  
- 具体做法：  
  1. 先算出数组所有元素的 **总和** `total`（一次遍历）。  
  2. 再从左到右遍历数组，维护一个变量 `left_sum`，表示**当前下标左侧所有元素的和**。  
  3. 对于下标 `i`，右侧和 `right_sum = total - left_sum - nums[i]`（总和减去左侧和和当前元素）。  
  4. 判断 `left_sum == right_sum`，如果相等直接返回 `i`。  
  5. 否则把 `nums[i]` 加到 `left_sum` 中，继续检查下一个下标。  

这就是 **前缀和**（prefix sum）思想的简化版：我们不必显式保存每个前缀的和，只用一个变量滚动更新即可。  

**类比**：想象你在一本账本里记录总收入 `total`，每天结束后把当天的收入记到 “左侧累计收入” `left_sum`，剩下的未记的收入自然就是 “右侧累计收入”。只要左侧和等于右侧和，就找到了平衡点。  

#### 代码（Python）  

```python
def findMiddleIndex(nums):
    total = sum(nums)          # 整个数组的总和，只算一次
    left_sum = 0               # 左侧累计和，初始为 0（因为左侧空）

    for i, val in enumerate(nums):
        # 右侧和 = 总和 - 左侧和 - 当前元素
        right_sum = total - left_sum - val

        # 如果左侧和等于右侧和，当前下标就是答案
        if left_sum == right_sum:
            return i           # 返回最左的符合条件的下标

        # 把当前元素加入左侧累计和，准备检查下一个位置
        left_sum += val

    # 循环结束仍未找到平衡点
    return -1
```

#### 复杂度  

- **时间复杂度：O(n)** —— 只遍历两遍（一次求总和，第二次寻找平衡点），所以工作量随 `n` 成线性关系。可以想象成“只需要一次全局称重，再一次顺序检查”。  
- **空间复杂度：O(1)** —— 只用了 `total`、`left_sum`、`right_sum` 三个整数，额外空间不随数组大小增长。  

---  

## 心得  

- **核心技巧**：利用**前缀和**（或滚动累计）把重复的求和操作降到一次遍历。  
- **适用的题型**：  
  1. **Pivot Index / 中心下标**（本题）  
  2. **子数组和等于目标值的分割点**（如 LeetCode 560 Subarray Sum Equals K 的前缀哈希表版）  
  3. **求数组的左侧最大和右侧最小的平衡点**（类似分割数组的题目）  
- **一句话总结解题钥匙**：**先算总和，再用滚动的左侧累计和推导右侧和，省去每次的全遍历**。  

## 反思  

- **第一反应**：看到“左边和等于右边和”，立刻想到“遍历每个位置、分别求左右和”，于是写出暴力解。  
- **最容易踩的坑**：  
  - 忘记把 **左侧为空** 或 **右侧为空** 的情况视作和为 `0`（即 `i==0` 或 `i==n-1`）。  
  - 对负数的处理没有额外注意，但前缀和方法同样适用。  
- **下次遇到同类题**：第一步先**求整体信息**（总和或前缀数组），再**在一次遍历中利用已有信息**快速判断，避免重复求和。