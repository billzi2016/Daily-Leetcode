# #910. 最小范围 II / Smallest Range II

> 难度：中等 · 标签：Array、Math、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/smallest-range-ii/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and an integer k.
For each index i where 0 <= i < nums.length, change nums[i] to be either nums[i] + k or nums[i] - k.
The score of nums is the difference between the maximum and minimum elements in nums.
Return the minimum score of nums after changing the values at each index.

**Examples**

**Example 1:**

```
Input: nums = [1], k = 0
Output: 0
Explanation: The score is max(nums) - min(nums) = 1 - 1 = 0.
```

**Example 2:**

```
Input: nums = [0,10], k = 2
Output: 6
Explanation: Change nums to be [2, 8]. The score is max(nums) - min(nums) = 8 - 2 = 6.
```

**Example 3:**

```
Input: nums = [1,3,6], k = 3
Output: 3
Explanation: Change nums to be [4, 6, 3]. The score is max(nums) - min(nums) = 6 - 3 = 3.
```

**Constraints**

- 1 <= nums.length <= 104
- 0 <= nums[i] <= 104
- 0 <= k <= 104

---

## 题目（中文翻译）

给定一个整数数组 `nums` 和一个整数 `k`。  
对于每个满足 `0 <= i < nums.length` 的下标 `i`，你可以将 `nums[i]` 改为 `nums[i] + k` 或 `nums[i] - k`。  
数组 `nums` 的 **得分**（score）定义为其最大元素与最小元素的差值。  
返回对每个下标都进行上述修改后，`nums` 的最小可能得分。

### 示例

#### 示例 1
**输入**  
`nums = [1]`, `k = 0`  

**输出**  
`0`  

**解释**  
得分为 `max(nums) - min(nums) = 1 - 1 = 0`。

#### 示例 2
**输入**  
`nums = [0,10]`, `k = 2`  

**输出**  
`6`  

**解释**  
将数组改为 `[2, 8]`。得分为 `max(nums) - min(nums) = 8 - 2 = 6`。

#### 示例 3
**输入**  
`nums = [1,3,6]`, `k = 3`  

**输出**  
`3`  

**解释**  
将数组改为 `[4, 6, 3]`。得分为 `max(nums) - min(nums) = 6 - 3 = 3`。

### 约束条件
- `1 <= nums.length <= 10^4`
- `0 <= nums[i] <= 10^4`
- `0 <= k <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**对每一个下标 `i`，都有两种选择**——把 `nums[i]` 加上 `k`，或者减去 `k`。  
于是可以把所有可能的组合全部枚举出来，得到一个新的数组后，计算它的 **分数**（最大值减最小值），取所有组合里最小的分数即为答案。

- **用到的数据结构**：  
  - `list`（列表）保存当前的数组。  
  - `int` 保存当前组合的分数。  
  - **类比**：把每个数看成一本书的页码，`+k` 就是把这本书往后翻 `k` 页，`-k` 就是往前翻 `k` 页。我们要把所有书都翻（每本书有两种翻法），找出翻完后最大页码与最小页码的差值最小的情况。

- **为什么正确**：  
  只要把**所有**可能的加/减方案都尝试一遍，必然能找到最优的那一种。暴力搜索不漏任何一种组合。

- **时间/空间复杂度**：  
  - 对每个元素都有两种选择，`n` 个元素就有 `2ⁿ` 种组合。遍历每种组合要 O(n) 去算最大最小值，所以 **时间复杂度是 O(n·2ⁿ)**。  
  - 只需要保存当前遍历的数组和一些临时变量，**空间复杂度是 O(n)**（存放临时数组）。

> **大白话**：  
> `2ⁿ` 就像是“翻硬币 n 次，正反两面都可能出现”，如果 `n=20`，组合数已经是 **1,048,576**，很快就会超时。

#### 代码（Python）

```python
from itertools import product
from typing import List

def smallestRangeII_bruteforce(nums: List[int], k: int) -> int:
    n = len(nums)
    best = float('inf')                     # 用来保存目前找到的最小分数

    # product 会产生所有 0/1 的组合，0 代表 -k，1 代表 +k
    for mask in product([0, 1], repeat=n):
        transformed = []                     # 存放本次组合后的数组
        for i, sign in enumerate(mask):
            if sign == 0:
                transformed.append(nums[i] - k)   # -k
            else:
                transformed.append(nums[i] + k)   # +k

        cur_score = max(transformed) - min(transformed)   # 计算分数
        best = min(best, cur_score)                       # 更新最小分数

    return best
```

#### 复杂度

- **时间复杂度**：`O(n·2ⁿ)` —— 每个元素有两种决定，所有组合数是指数级的。  
- **空间复杂度**：`O(n)` —— 只需要保存一次遍历时的临时数组。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **“枚举所有 2ⁿ 种可能”**，这在 `n` 达到 `10⁴` 时根本不可行。  
观察题目可以发现：

1. 每个数只能 **向左（-k）** 或 **向右（+k）** 移动，移动的幅度都是相同的 `k`。  
2. 如果把所有数先 **排序**，那么我们只需要决定一个“分界点” `i`，把 **左侧** 的数全部 **+k**，把 **右侧** 的数全部 **-k**（或者相反），就可以得到所有可能的最小区间。  

> **为什么只需要考虑这种“左加右减” 的方式？**  
> 把数组排好序后，若某个数在左边被 **-k**，而它右边的数却被 **+k**，则左边的数会更小，右边的数会更大，导致区间宽度不可能更小。把左边的数都往上调（+k），右边的数往下调（-k），可以让最大值和最小值更靠近，从而缩小区间。

具体做法：

1. 将 `nums` **升序** 排序，记为 `a[0] ≤ a[1] ≤ … ≤ a[n‑1]`。  
2. 初始答案设为 `a[-1] - a[0]`（全部不动或全加全减的情况）。  
3. 枚举分界点 `i`（`0 ≤ i < n-1`），把 **左侧**（`0…i`）全部 **+k**，把 **右侧**（`i+1…n-1`）全部 **-k**。此时：
   - **最小值** = `min(a[0] + k, a[i+1] - k)`  
   - **最大值** = `max(a[i] + k, a[-1] - k)`  
   计算 `max - min` 并更新答案。  
4. 最后返回最小的答案。

**核心算法/数据结构**：

- **排序**（`O(n log n)`）——把数列变成有序，便于“一刀切”地划分左右。  
- **一次遍历**（`O(n)`）——枚举分界点，计算区间宽度。  

> **类比**：想象一排小朋友站成一列，老师要把左边的孩子往前一步（+k），右边的孩子往后一步（-k），这样两端的距离会变小。老师只需要决定从哪位孩子开始转向（分界点），不必每个人单独决定。

#### 代码（Python）

```python
from typing import List

def smallestRangeII(nums: List[int], k: int) -> int:
    # 1. 先把数组排序
    nums.sort()                               # O(n log n)

    n = len(nums)
    # 2. 初始答案：不做任何 +/- 操作时的区间宽度
    ans = nums[-1] - nums[0]

    # 3. 枚举分界点 i，左侧 +k，右侧 -k
    for i in range(n - 1):
        # 左侧最大值（因为左侧已经全部 +k）
        max_left = nums[i] + k
        # 右侧最大值（右侧全部 -k，整体最大值可能是原来的最大值 -k）
        max_right = nums[-1] - k
        cur_max = max(max_left, max_right)

        # 左侧最小值（左侧全部 +k，最小值可能是原来的最小值 +k）
        min_left = nums[0] + k
        # 右侧最小值（右侧已经 -k）
        min_right = nums[i + 1] - k
        cur_min = min(min_left, min_right)

        ans = min(ans, cur_max - cur_min)    # 更新全局最小区间宽度

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 排序需要 `O(n log n)`，遍历分界点只要 `O(n)`，两者相加仍是 `O(n log n)`。  
  - 与暴力解的 `O(n·2ⁿ)` 相比，**指数级** 的搜索被压缩成 **对数级** 的排序，速度快了很多。

- **空间复杂度**：`O(1)`（不计排序的原地修改）  
  - 只使用常数个额外变量；排序可以原地完成，不需要额外的数组。

---

## 心得

- **核心技巧**：先排序，再利用 **左右划分 +k / -k** 的贪心思路把搜索空间从指数级压到线性级。  
- **适用的题型**：  
  1. “**把每个数加/减同一个值**” 类的最小区间问题（如 *Smallest Range I*）。  
  2. 需要 **分段统一操作** 的优化问题（如 *Minimize the Maximum Difference After Increasing Elements*）。  
  3. 通过 **排序 + 前缀/后缀** 思想把全局最优转化为局部枚举的题目。  
- **一句话总结**：先排序，再一次遍历决定“左加右减”的分界点，即可得到最小可能区间。

---

## 反思

- **第一反应**：直接想到枚举每个数的 `+k / -k`，写出暴力搜索。  
- **最容易踩的坑**：  
  - 忘记 **考虑分界点在最左或最右** 的情况（即全部加或全部减），这就是初始化答案时使用 `nums[-1] - nums[0]` 的原因。  
  - 边界条件 `i = n-1` 不需要处理，因为右侧已经没有元素，若硬写会导致索引越界。  
- **下次遇到同类题**：第一步先 **排序**，思考是否可以把所有元素划分为“左侧统一操作 / 右侧统一操作”，再用一次遍历枚举分界点。这样常能把指数级搜索降到 `O(n log n)`。