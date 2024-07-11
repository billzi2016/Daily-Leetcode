# #2771. 两个数组构成的最长非递减子数组 / Longest Non-decreasing Subarray From Two Arrays

> 难度：中等 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/longest-non-decreasing-subarray-from-two-arrays/)

---

## 题目（英文原版）

**Description**

You are given two 0-indexed integer arrays nums1 and nums2 of length n.
Let's define another 0-indexed integer array, nums3, of length n. For each index i in the range [0, n - 1], you can assign either nums1[i] or nums2[i] to nums3[i].
Your task is to maximize the length of the longest non-decreasing subarray in nums3 by choosing its values optimally.
Return an integer representing the length of the longest non-decreasing subarray in nums3.
Note: A subarray is a contiguous non-empty sequence of elements within an array.

**Examples**

**Example 1:**

```
Input: nums1 = [2,3,1], nums2 = [1,2,1]
Output: 2
Explanation: One way to construct nums3 is: 
nums3 = [nums1[0], nums2[1], nums2[2]] => [2,2,1]. 
The subarray starting from index 0 and ending at index 1, [2,2], forms a non-decreasing subarray of length 2. 
We can show that 2 is the maximum achievable length.
```

**Example 2:**

```
Input: nums1 = [1,3,2,1], nums2 = [2,2,3,4]
Output: 4
Explanation: One way to construct nums3 is: 
nums3 = [nums1[0], nums2[1], nums2[2], nums2[3]] => [1,2,3,4]. 
The entire array forms a non-decreasing subarray of length 4, making it the maximum achievable length.
```

**Example 3:**

```
Input: nums1 = [1,1], nums2 = [2,2]
Output: 2
Explanation: One way to construct nums3 is: 
nums3 = [nums1[0], nums1[1]] => [1,1]. 
The entire array forms a non-decreasing subarray of length 2, making it the maximum achievable length.
```

**Constraints**

- 1 <= nums1.length == nums2.length == n <= 105
- 1 <= nums1[i], nums2[i] <= 109

---

## 题目（中文翻译）

给定两个下标从 **0** 开始的整数数组 `nums1` 和 `nums2`，长度均为 `n`。  
定义另一个下标从 **0** 开始的整数数组 `nums3`，长度为 `n`。对于每个索引 `i`（`0 ≤ i ≤ n‑1`），你可以将 `nums1[i]` 或 `nums2[i]` 中的任意一个赋值给 `nums3[i]`。  

你的任务是通过合理选择每个位置的取值，使得 `nums3` 中**最长非递减子数组**（non-decreasing subarray）的长度最大化。返回该最长长度的整数值。

> **注意**：子数组（subarray）是数组中连续且非空的元素序列。

## 示例

### 示例 1
**输入**  
`nums1 = [2,3,1]`, `nums2 = [1,2,1]`  

**输出**  
`2`  

**解释**  
一种构造 `nums3` 的方式为：  
`nums3 = [nums1[0], nums2[1], nums2[2]] => [2,2,1]`。  
下标 `0` 到 `1` 的子数组 `[2,2]` 构成长度为 `2` 的非递减子数组。可以证明 `2` 是能够达到的最大长度。

### 示例 2
**输入**  
`nums1 = [1,3,2,1]`, `nums2 = [2,2,3,4]`  

**输出**  
`4`  

**解释**  
一种构造 `nums3` 的方式为：  
`nums3 = [nums1[0], nums2[1], nums2[2], nums2[3]] => [1,2,3,4]`。  
整个数组本身就是长度为 `4` 的非递减子数组，已达到最大可能长度。

### 示例 3
**输入**  
`nums1 = [1,1]`, `nums2 = [2,2]`  

**输出**  
`2`  

**解释**  
一种构造 `nums3` 的方式为：  
`nums3 = [nums1[0], nums1[1]] => [1,1]`。  
整个数组形成长度为 `2` 的非递减子数组，同样是最大可达长度。

## 约束条件

- `1 ≤ nums1.length == nums2.length == n ≤ 10^5`
- `1 ≤ nums1[i], nums2[i] ≤ 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的 `nums3` 都枚举出来**，再在每个完整的数组里找最长的非递减（non‑decreasing）子数组。  
- **枚举**：对每个下标 `i`，我们可以任选 `nums1[i]` 或 `nums2[i]`，相当于在每个位置上有两张“卡片”。把所有卡片排成一行，一共有 `2ⁿ` 种排法（因为每个位置有两种选择）。  
- **检查**：得到一条完整的 `nums3` 后，用一次线性扫描计算它的最长非递减子数组长度。  
- **取最大**：把所有情况的答案取最大即为最终答案。

> **类比**：把 `nums1`、`nums2` 看成两本词典，`i` 位置的词可以从任意一本挑选。暴力解相当于把每一本词典的每一页都翻一遍，看看能拼出多长的“递增”句子。

**为什么正确**：因为我们枚举了**所有**合法的 `nums3`，所以答案一定会出现在枚举的集合里。

#### 代码（Python）

```python
from itertools import product

def longest_non_decreasing_bruteforce(nums1, nums2):
    """
    仅用于演示，实际 n 超过 20 时会爆炸。
    """
    n = len(nums1)
    best = 0

    # product([0,1], repeat=n) 生成所有 0/1 的组合，0 表示选 nums1，1 表示选 nums2
    for mask in product([0, 1], repeat=n):
        # 生成对应的 nums3
        nums3 = [nums1[i] if bit == 0 else nums2[i] for i, bit in enumerate(mask)]

        # 线性扫描求最长非递减子数组
        cur_len = 1
        max_len = 1
        for i in range(1, n):
            if nums3[i] >= nums3[i - 1]:
                cur_len += 1
            else:
                cur_len = 1
            max_len = max(max_len, cur_len)

        best = max(best, max_len)

    return best
```

#### 复杂度

- **时间复杂度**：`O(2ⁿ * n)`  
  - `2ⁿ` 表示所有可能的选择（指数级），每种选择要再遍历一次数组（`n`）。  
  - **大白话**：如果 `n = 20`，大约有 `1,048,576` 种组合，跑完可能需要几秒；`n = 30` 时就已经是十亿级别，根本跑不完。

- **空间复杂度**：`O(n)`  
  - 主要是保存临时的 `nums3`（长度 `n`）和递归生成的掩码。

> **结论**：暴力解只能用来验证思路或跑极小的样例，不能用于正式提交。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**我们不需要真的枚举所有组合**，只要在每个位置记录“以某个选择结尾的最长非递减子数组长度”，就可以递推得到答案。  

**关键观察**  
- 对于位置 `i`，我们只关心两种可能的结尾值：`nums1[i]` 或 `nums2[i]`。  
- 如果我们已经知道了位置 `i-1` 以 `nums1[i-1]`（记为状态 0）或 `nums2[i-1]`（记为状态 1）结尾的最长非递减子数组长度，那么：
  - 若 `nums1[i] >= nums1[i-1]`，则可以把 `nums1[i]` 接在状态 0 的序列后面，长度加一。  
  - 若 `nums1[i] >= nums2[i-1]`，则也可以把 `nums1[i]` 接在状态 1 的序列后面，长度加一。  
  - 同理处理 `nums2[i]`。

这就是**动态规划**（Dynamic Programming）的典型做法：  
- `dp0[i]` = 以 `nums1[i]` 为结尾的最长非递减子数组长度。  
- `dp1[i]` = 以 `nums2[i]` 为结尾的最长非递减子数组长度。

**转移方程**（把下标从 0 开始）：

```
dp0[i] = 1
if nums1[i] >= nums1[i-1]: dp0[i] = max(dp0[i], dp0[i-1] + 1)
if nums1[i] >= nums2[i-1]: dp0[i] = max(dp0[i], dp1[i-1] + 1)

dp1[i] = 1
if nums2[i] >= nums1[i-1]: dp1[i] = max(dp1[i], dp0[i-1] + 1)
if nums2[i] >= nums2[i-1]: dp1[i] = max(dp1[i], dp1[i-1] + 1)
```

- 初始时 `dp0[0] = dp1[0] = 1`（单个元素本身就是长度为 1 的非递减子数组）。
- 在遍历的过程中，维护一个全局最大值 `ans = max(ans, dp0[i], dp1[i])`。

**空间优化**  
我们只会在转移时用到 `i-1` 的状态，因此可以只保留前一个位置的两个值，而不是整个数组。这样把空间从 `O(n)` 降到 `O(1)`。

> **类比**：把每个位置想象成一座小城，`dp0`、`dp1` 是两条通往这座城的道路长度。我们只需要记住前一座城的两条道路长度，就能算出到达当前城的最长道路。

#### 代码（Python）

```python
def longest_non_decreasing(nums1, nums2):
    """
    动态规划 O(n) 时间，O(1) 额外空间。
    """
    n = len(nums1)
    # 第 0 位的状态都是 1（单独一个元素）
    prev0, prev1 = 1, 1
    ans = 1

    for i in range(1, n):
        cur0 = 1  # 以 nums1[i] 结尾的最长长度
        cur1 = 1  # 以 nums2[i] 结尾的最长长度

        # 计算 cur0
        if nums1[i] >= nums1[i - 1]:
            cur0 = max(cur0, prev0 + 1)          # 前一位选 nums1
        if nums1[i] >= nums2[i - 1]:
            cur0 = max(cur0, prev1 + 1)          # 前一位选 nums2

        # 计算 cur1
        if nums2[i] >= nums1[i - 1]:
            cur1 = max(cur1, prev0 + 1)          # 前一位选 nums1
        if nums2[i] >= nums2[i - 1]:
            cur1 = max(cur1, prev1 + 1)          # 前一位选 nums2

        # 更新答案和上一轮的状态
        ans = max(ans, cur0, cur1)
        prev0, prev1 = cur0, cur1

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 只遍历一次数组，且每一步的计算都是常数次比较和取最大。  
  - 与暴力解的 `O(2ⁿ·n)` 相比，线性时间可以轻松处理 `n = 10⁵` 的规模。

- **空间复杂度**：`O(1)`（常数）  
  - 只用了几条变量来保存前一个位置的状态，不随 `n` 增长。

---

## 心得

- **核心技巧**：**状态压缩的动态规划**——在每个位置只关心两种“结尾值”的最长非递减长度，然后用前一位置的状态递推出当前状态。  
- **适用的题型**  
  1. 两条平行序列，每个下标可以任选其一构造新序列（如本题）。  
  2. “在每一步有多种选择，且选择之间有顺序约束” 的 DP（例如 “两个数组交叉拼接的最长递增子序列”）。  
  3. “在每个位置有两种颜色/状态，需要统计满足某种相邻关系的最长连续段” （如 “颜色翻转后最长相同子数组”）。

- **一句话总结**：**把“每个位置的两种可能”抽象成两个 DP 状态，利用前一位置的状态直接转移，既避免枚举，又能一次遍历得到答案。**

---

## 反思

- **第一反应**：看到“可以任选 `nums1[i]` 或 `nums2[i]`”，立刻想到“枚举所有组合”，这在脑中是最自然的暴力思路。  
- **最容易踩的坑**  
  - **边界条件**：第 0 位没有前驱，需要单独初始化 `dp0 = dp1 = 1`。  
  - **比较方向**：题目要求**非递减**（`>=`），而不是严格递增（`>`），细节容易写错。  
  - **溢出**：在 Python 中整数不会溢出，但如果用其他语言要注意 `int` 范围。  
- **下次第一步**：先**确定状态**（这里是“以哪个数组的元素结尾”），再**写出转移**，检查是否只依赖前一位置，若是则可以直接做**空间压缩**。这样就能从一开始就走向最优解，而不是先陷入指数级暴力。