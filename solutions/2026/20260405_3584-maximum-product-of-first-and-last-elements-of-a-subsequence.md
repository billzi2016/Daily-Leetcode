# #3584. 子序列首尾元素的最大乘积 / Maximum Product of First and Last Elements of a Subsequence

> 难度：中等 · 标签：Array、Two Pointers · [LeetCode 链接](https://leetcode.com/problems/maximum-product-of-first-and-last-elements-of-a-subsequence/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and an integer m.
Return the maximum product of the first and last elements of any subsequence of nums of size m.

**Examples**

**Example 1:**

```
Input: nums = [-1,-9,2,3,-2,-3,1], m = 1
Output: 81
Explanation:
The subsequence [-9] has the largest product of the first and last elements: -9 * -9 = 81 . Therefore, the answer is 81.
```

**Example 2:**

```
Input: nums = [1,3,-5,5,6,-4], m = 3
Output: 20
Explanation:
The subsequence [-5, 6, -4] has the largest product of the first and last elements.
```

**Example 3:**

```
Input: nums = [2,-1,2,-6,5,2,-5,7], m = 2
Output: 35
Explanation:
The subsequence [5, 7] has the largest product of the first and last elements.
```

**Constraints**

- 1 <= nums.length <= 105
- -105 <= nums[i] <= 105
- 1 <= m <= nums.length

---

## 题目（中文翻译）

给定一个整数数组（array）`nums` 和一个整数 `m`。  
返回 `nums` 中任意长度为 `m` 的子序列（subsequence）其首元素与末元素乘积的最大值。

## 示例

### 示例 1
**输入**: `nums = [-1,-9,2,3,-2,-3,1]`, `m = 1`  
**输出**: `81`  
**解释**:  
子序列 `[-9]` 的首尾元素乘积最大：`-9 * -9 = 81`，因此答案为 `81`。

### 示例 2
**输入**: `nums = [1,3,-5,5,6,-4]`, `m = 3`  
**输出**: `20`  
**解释**:  
子序列 `[-5, 6, -4]` 的首尾元素乘积最大。

### 示例 3
**输入**: `nums = [2,-1,2,-6,5,2,-5,7]`, `m = 2`  
**输出**: `35`  
**解释**:  
子序列 `[5, 7]` 的首尾元素乘积最大。

## 约束条件

- `1 <= nums.length <= 10^5`
- `-10^5 <= nums[i] <= 10^5`
- `1 <= m <= nums.length`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把所有合法的子序列都列举出来，算出它们的「首元素 × 末元素」的乘积，然后取最大值。  

- **合法子序列**：长度恰好为 `m`，并且保持原数组的相对顺序。  
- 对于一个子序列，只有首元素 `nums[i]` 和末元素 `nums[j]` 会影响乘积，中间的 `m‑2` 个元素可以随便挑。  
- 因此只要保证 `j - i >= m-1`（两者之间至少留出 `m-2` 个位置），`(i, j)` 就对应一种合法的子序列。  

我们可以遍历所有满足 `j - i >= m-1` 的 `(i, j)` 对，计算 `nums[i] * nums[j]`，保存最大值。  

> **类比**：把数组想成一本书的章节，`i` 是选的第一章，`j` 是选的最后一章，只要两章之间还有足够的章节（≥ `m‑2`），就能凑齐 `m` 章节的阅读计划。  

**为什么正确**：因为乘积只依赖首尾，两者的所有可能组合都被遍历到了，最大值自然不会漏掉。

**时间/空间复杂度**：  
- 外层循环遍历 `i`（最多 `n` 次），内层循环遍历所有满足条件的 `j`（平均约 `n/2` 次），总共大约 `n²/2` 次乘法运算 → **时间复杂度 O(n²)**。  
- 只用常数个额外变量 → **空间复杂度 O(1)**。  

> **大白话解释**：`O(n²)` 就像让每个人和所有其他人握手，人数多时手都要握太多次，效率很低。

#### 代码（Python）

```python
from typing import List

def maxProduct_bruteforce(nums: List[int], m: int) -> int:
    n = len(nums)
    ans = float('-inf')                     # 记录最大的乘积
    # i 为首元素下标
    for i in range(n):
        # j 必须足够靠后，才能在 i 与 j 之间放下其余 m-2 个元素
        for j in range(i + m - 1, n):
            prod = nums[i] * nums[j]        # 只关心首尾的乘积
            if prod > ans:
                ans = prod
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)` —— 每对合法的首尾都要算一次乘积。  
- **空间复杂度**：`O(1)` —— 只用了几个整数变量。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，真正耗时的地方是 **对所有合法的 `(i, j)` 对做两层循环**。  
我们需要把内部的遍历去掉，只在一次遍历中完成所有乘积的比较。  

**关键观察**  

- 当我们把 `j` 当作「末元素」时，首元素只能取 **下标 ≤ j‑(m‑1)** 的位置。  
- 在这些候选首元素中，**最大值** 与 **最小值**（即最负的数）最有可能产生最大乘积：  
  - 正数 × 正数 → 用最大正数。  
  - 负数 × 负数 → 用最小（最负）数，因为负负得正，且绝对值越大越好。  
- 因此，对于每个 `j`，只需要知道 **截至下标 `j‑(m‑1)` 的最大值和最小值**，就可以在 **O(1)** 时间内算出以 `j` 为末元素的最佳乘积。  

**如何维护这两个极值**  

- 随着 `j` 从左到右移动，允许的首元素下标集合只会 **不断扩展**（从不收缩），因为 `j‑(m‑1)` 只会增大。  
- 所以我们可以在一次遍历中维护两个变量 `max_first`、`min_first`，每次把新加入的下标对应的 `nums` 与它们比较并更新。  

**完整步骤**  

1. 初始化 `max_first = min_first = nums[0]`（第一个元素一定在候选范围内）。  
2. 从 `j = m-1` 开始遍历（最小的合法末元素下标）。  
3. 在每次循环开始前，**把新加入的下标 `j-(m-1)` 对应的值** 与 `max_first`、`min_first` 比较并更新。  
4. 计算两种可能的乘积：  
   - `max_first * nums[j]`（最大正数 × 末元素）  
   - `min_first * nums[j]`（最负数 × 末元素）  
   取这两者的最大值，与全局答案 `ans` 比较并更新。  
5. 循环结束后，`ans` 即为所求的最大乘积。  

**为什么正确**  

- 对于固定的 `j`，所有合法的 `i` 已经全部包含在 `max_first`、`min_first` 维护的范围内。  
- 任意合法乘积 `nums[i] * nums[j]` 必然 ≤ `max(max_first * nums[j], min_first * nums[j])`，因为 `max_first` 是所有候选 `nums[i]` 中的最大，`min_first` 是最小。  
- 因此在每个 `j` 取到的最大乘积一定是所有以 `j` 为末元素的子序列中最优的，遍历完所有 `j` 就覆盖了全部合法子序列。  

> **类比**：想象你在跑步，前面有一条绳子把已经跑过的最高点和最低点记录下来，每到一个新地点（`j`），只需要看这两个极值与当前地点的乘积，就能知道“最好的配对”了，而不必回头检查每一步。

#### 代码（Python）

```python
from typing import List

def maxProduct(nums: List[int], m: int) -> int:
    """
    O(n) 时间、O(1) 额外空间的最优解
    """
    n = len(nums)
    # 初始时只有下标 0 可以作为首元素
    max_first = min_first = nums[0]
    ans = float('-inf')

    # j 为末元素的下标，最小合法 j 为 m-1
    for j in range(m - 1, n):
        # 新加入的首元素下标是 j - (m - 1)
        new_idx = j - (m - 1)
        # 更新极值（因为集合只会扩大，直接比较即可）
        if nums[new_idx] > max_first:
            max_first = nums[new_idx]
        if nums[new_idx] < min_first:
            min_first = nums[new_idx]

        # 以当前 j 为末元素时，可能的最大乘积
        cand1 = max_first * nums[j]   # 最大正数 × 末元素
        cand2 = min_first * nums[j]   # 最小（最负）数 × 末元素
        best_here = cand1 if cand1 > cand2 else cand2

        if best_here > ans:
            ans = best_here

    return ans
```

**代码要点注释**  

- `new_idx = j - (m - 1)`：这是在把 `j` 作为末元素时，**刚好可以加入**的最左侧首元素位置。  
- `max_first / min_first`：分别记录截至 `new_idx` 为止的最大值和最小值。  
- `cand1 / cand2`：考虑正×正和负×负两种可能，取大的那一个。  

#### 复杂度  

- **时间复杂度**：`O(n)` —— 只遍历一次数组，每个元素做常数次操作。相比暴力的 `O(n²)` 快了好几倍。  
- **空间复杂度**：`O(1)` —— 只用了几个整数变量，和输入规模无关。

---

## 心得  

- **核心技巧**：**滑动窗口 + 维护前缀极值（最大/最小）**。  
- **适用的题型**：  
  1. “在满足距离/长度约束的前提下，求两数乘积/和的最大值”。  
  2. “给定窗口大小，求窗口内最大/最小元素”。  
  3. “子序列首尾乘积最大” 这类只关心首尾的子序列问题。  
- **一句话总结**：只要把「首元素」的候选范围压缩为「当前已见的最大/最小值」，就能在一次遍历里把所有合法配对的最优乘积找出来。

---

## 反思  

- **第一反应**：直接枚举所有合法的首尾下标，写两层循环。  
- **最容易踩的坑**：  
  - 忘记 **负数** 也可能得到更大的正乘积，需要同时维护最小值。  
  - `m = 1` 的特殊情况：首尾是同一个元素，答案是元素的平方。上述算法自然兼容，但如果手动写特判，容易漏掉。  
  - 边界下标 `j - (m-1)` 必须在数组范围内，循环起点要设为 `m-1`。  
- **下次遇到同类题**：第一步想到“**固定末元素**，其左侧可以选的首元素形成一个前缀区间”，于是就去 **维护该区间的最大/最小**，把二次循环降到一次遍历。