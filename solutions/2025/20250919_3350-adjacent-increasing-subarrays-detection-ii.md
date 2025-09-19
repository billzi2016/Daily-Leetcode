# #3350. 相邻递增子数组检测 II / Adjacent Increasing Subarrays Detection II

> 难度：中等 · 标签：Array、Binary Search · [LeetCode 链接](https://leetcode.com/problems/adjacent-increasing-subarrays-detection-ii/)

---

## 题目（英文原版）

**Description**

Given an array nums of n integers, your task is to find the maximum value of k for which there exist two adjacent subarrays of length k each, such that both subarrays are strictly increasing. Specifically, check if there are two subarrays of length k starting at indices a and b (a < b), where:
Return the maximum possible value of k.
A subarray is a contiguous non-empty sequence of elements within an array.

**Examples**

**Example 1:**

```
Input: nums = [2,5,7,8,9,2,3,4,3,1]
Output: 3
Explanation:
```

**Example 2:**

```
Input: nums = [1,2,3,4,4,4,4,5,6,7]
Output: 2
Explanation:
```

**Constraints**

- 2 <= nums.length <= 2 * 105
- -109 <= nums[i] <= 109

---

## 题目（中文翻译）

给定一个长度为 `n` 的整数数组 `nums`，请找出最大的整数 `k`，使得数组中存在 **两个相邻子数组（subarray）**，每个子数组的长度均为 `k`，且这两个子数组都是 **严格递增** 的。具体地，要求存在起始下标 `a` 与 `b`（`a < b`）满足：

- `b = a + k`（即两个子数组相邻）；
- 子数组 `nums[a .. a+k-1]` 与 `nums[b .. b+k-1]` 均满足 `nums[i] < nums[i+1]`（严格递增）。

返回可能的最大 `k` 值。

> **子数组（subarray）** 是数组中连续的、非空的元素序列。

### 示例

**示例 1**  
输入: `nums = [2,5,7,8,9,2,3,4,3,1]`  
输出: `3`  
解释：

**示例 2**  
输入: `nums = [1,2,3,4,4,4,4,5,6,7]`  
输出: `2`  
解释：

### 约束条件

- `2 <= nums.length <= 2 * 10^5`
- `-10^9 <= nums[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举**所有可能的子数组长度 `k`，然后检查数组中是否出现两个相邻、长度恰好为 `k` 且严格递增的子数组。  

- **枚举 `k`**：从 `1` 到 `n//2`（因为要放得下两个相邻的子数组）。  
- **枚举起始位置**：对每个 `k`，遍历所有可能的起始下标 `a`，子数组 `[a, a+k-1]` 必须严格递增；再检查紧挨着的子数组 `[a+k, a+2k-1]` 是否也严格递增。  
- **严格递增的判断**：遍历子数组内部，逐个比较相邻元素 `nums[i] < nums[i+1]`。如果全部满足，则该子数组是递增的。

> **类比**：把数组想象成一排书，找两段连续的“升序章节”。暴力做法就是把每一本书都当作章节的起点，逐本检查后面的 `k` 本是否满足“从小到大”。

**为什么正确**：只要遍历了 **所有** 可能的 `k` 和所有可能的起点，就不可能漏掉任何合法的相邻递增子数组。只要找到一个满足条件的组合，就说明该 `k` 可行。

#### 代码（Python）

```python
def max_k_bruteforce(nums):
    n = len(nums)
    # 最多只能取到 n//2，因为要放得下两个相邻的子数组
    ans = 0
    # 枚举子数组长度 k
    for k in range(1, n // 2 + 1):
        found = False          # 本轮 k 是否已经找到合法组合
        # 枚举左子数组的起始下标 a
        for a in range(0, n - 2 * k + 1):
            # 检查左子数组是否严格递增
            inc_left = True
            for i in range(a, a + k - 1):
                if nums[i] >= nums[i + 1]:
                    inc_left = False
                    break
            if not inc_left:
                continue       # 左边不递增，直接跳到下一个起点

            # 检查右子数组是否严格递增
            inc_right = True
            b = a + k           # 右子数组的起始位置
            for i in range(b, b + k - 1):
                if nums[i] >= nums[i + 1]:
                    inc_right = False
                    break
            if inc_right:
                found = True
                break           # 本次 k 已经找到，退出起点循环

        if found:
            ans = k               # 记录能够做到的最大 k
    return ans
```

> 代码里每一行都加了中文注释，帮助你快速定位思路。

#### 复杂度

- **时间复杂度**：`O(n³)`  
  - 外层枚举 `k`（最多 `n/2` 次），  
  - 中层枚举起点 `a`（最多 `n` 次），  
  - 内层遍历子数组检查递增（每次最坏 `k` 步）。  
  - 于是最坏情况约为 `n/2 * n * n/2 ≈ O(n³)`。  
  - **大白话**：如果 `n = 10⁵`，这种三层循环根本跑不完，像是让 10⁵ 个人每人排队 10⁵ 次再检查 10⁵ 件事，时间会爆炸。

- **空间复杂度**：`O(1)`  
  - 只用了常数个额外变量，不随 `n` 增长。

---

### 2. 最优解

#### 思路  

暴力解慢的根源在于**反复检查相同的子数组是否递增**。事实上，递增性是可以**预处理**的：我们只需要知道在每个位置向左/向右能够延伸多少步仍保持严格递增。这样，判断任意子数组是否递增只需要一次 **O(1)** 查询。

**步骤概览**：

1. **左侧递增长度 `inc_left[i]`**  
   - 定义为以 `i` 为**右端点**的最长严格递增子数组的长度。  
   - 递推公式  
     ```
     inc_left[0] = 1
     if nums[i-1] < nums[i]:
         inc_left[i] = inc_left[i-1] + 1
     else:
         inc_left[i] = 1
     ```
   - 直观解释：如果前一个数比当前数小，说明可以把前面的递增段“接上来”，否则只能从当前位置重新开始。

2. **右侧递增长度 `inc_right[i]`**  
   - 定义为以 `i` 为**左端点**的最长严格递增子数组的长度。  
   - 从右往左遍历，递推公式类似：
     ```
     inc_right[n-1] = 1
     if nums[i] < nums[i+1]:
         inc_right[i] = inc_right[i+1] + 1
     else:
         inc_right[i] = 1
     ```

3. **遍历所有相邻分界**  
   - 对每个可能的“边界” `i`（左子数组以 `i` 结束，右子数组从 `i+1` 开始），  
   - 左子数组最长递增长度是 `inc_left[i]`，右子数组最长递增长度是 `inc_right[i+1]`。  
   - 若想在该边界得到长度为 `k` 的相邻递增子数组，需要 `k ≤ inc_left[i]` 且 `k ≤ inc_right[i+1]`，即 `k ≤ min(inc_left[i], inc_right[i+1])`。  
   - 因此该边界能够提供的最大 `k` 为 `min(inc_left[i], inc_right[i+1])`。  
   - **答案**就是所有边界的这些最小值的最大值。

> **类比**：把数组看成一条山路。`inc_left[i]` 记录从左边爬到第 `i` 点还能保持上坡的最长距离；`inc_right[i]` 记录从右边爬到第 `i` 点还能保持上坡的最长距离。两个相邻的上坡段只要在某个拐点相遇，能共同拥有的最长相同长度，就是两侧上坡距离的较小者。

#### 代码（Python）

```python
def max_k(nums):
    """
    返回能够找到的最大 k，使得存在两个相邻、长度为 k 且严格递增的子数组。
    时间 O(n)，空间 O(n)（仅用两个长度数组）。
    """
    n = len(nums)
    if n < 2:        # 不可能出现两个相邻子数组
        return 0

    # 1️⃣ 计算以每个位置为右端点的递增长度
    inc_left = [1] * n
    for i in range(1, n):
        if nums[i - 1] < nums[i]:
            inc_left[i] = inc_left[i - 1] + 1
        # else keep 1 (从 i 开始重新计数)

    # 2️⃣ 计算以每个位置为左端点的递增长度
    inc_right = [1] * n
    for i in range(n - 2, -1, -1):
        if nums[i] < nums[i + 1]:
            inc_right[i] = inc_right[i + 1] + 1
        # else keep 1

    # 3️⃣ 遍历所有相邻分界，求最大可行的 k
    ans = 0
    for i in range(n - 1):          # 分界在 i 与 i+1 之间
        possible_k = min(inc_left[i], inc_right[i + 1])
        if possible_k > ans:
            ans = possible_k

    return ans
```

**关键行解释**：

- `inc_left[i] = inc_left[i - 1] + 1`：如果前后两数满足递增，说明可以把左边的递增段继续往右扩展。
- `inc_right[i] = inc_right[i + 1] + 1`：同理，若 `nums[i] < nums[i+1]`，右侧递增段可以向左延伸。
- `possible_k = min(inc_left[i], inc_right[i + 1])`：左、右两段各自最多能提供的递增长度，取较小的才是两个相邻子数组共同能达到的长度。

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 只遍历数组三遍（一次算 `inc_left`，一次算 `inc_right`，一次求最大 `k`），每次都是线性操作。  
  - **对比暴力**：从“每个 k 每个起点每个元素都检查”降到了“一遍预处理 + 一遍遍历”，快了几个数量级。

- **空间复杂度**：`O(n)`  
  - 需要两个长度为 `n` 的辅助数组 `inc_left`、`inc_right`。  
  - 如果想进一步压缩空间，可以把右侧长度直接在遍历时计算（只用 `O(1)`），但为了代码可读性，这里保留 `O(n)`。

---

## 心得

- **核心技巧**：利用**前缀递增长度**和**后缀递增长度**的预处理，把“子数组是否递增”的 O(k) 检查压缩到 O(1)。  
- **适用场景**：  
  1. **寻找相邻递增/递减段**的最长公共长度（如本题）。  
  2. **单调子数组的最大长度**（如“最长严格递增子数组”）。  
  3. **在数组中找满足某种单调条件的两段**（例如“两个相邻的非递减段”）。  
- **一句话总结**：把“局部递增”信息提前算好，之后只要在分界处取最小值，就能瞬间得到答案——**预处理+局部比较**是关键。

---

## 反思

- **第一反应**：直接枚举 `k` 和起点，逐个检查递增性——最自然但极慢的做法。  
- **最容易踩的坑**：  
  - 忘记 **相邻** 的要求，误把两个不相邻的递增段算进去。  
  - 边界条件：数组长度只有 2 时仍需返回 `1`（如果两个元素递增），否则返回 `0`。  
  - 递增判断要用严格的 `<`，不能用 `<=`（题目要求“严格递增”）。  
- **下次类似题目**：第一步先问自己“**我需要快速判断任意区间是否满足单调性吗**”。如果答案是“是”，就立刻想到**前缀/后缀递增长度**或**前缀和**之类的预处理技巧。这样可以把原本的 O(n²) 或 O(n³) 降到 O(n)。