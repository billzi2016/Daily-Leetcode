# #2420. 找到所有好下标 / Find All Good Indices

> 难度：中等 · 标签：Array、Dynamic Programming、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/find-all-good-indices/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums of size n and a positive integer k.
We call an index i in the range k <= i < n - k good if the following conditions are satisfied:
Return an array of all good indices sorted in increasing order.

**Examples**

**Example 1:**

```
Input: nums = [2,1,1,1,3,4,1], k = 2
Output: [2,3]
Explanation: There are two good indices in the array:
- Index 2. The subarray [2,1] is in non-increasing order, and the subarray [1,3] is in non-decreasing order.
- Index 3. The subarray [1,1] is in non-increasing order, and the subarray [3,4] is in non-decreasing order.
Note that the index 4 is not good because [4,1] is not non-decreasing.
```

**Example 2:**

```
Input: nums = [2,1,1,2], k = 2
Output: []
Explanation: There are no good indices in this array.
```

**Constraints**

- n == nums.length
- 3 <= n <= 105
- 1 <= nums[i] <= 106
- 1 <= k <= n / 2

---

## 题目（中文翻译）

给定一个下标从 **0** 开始的整数数组 `nums`，长度为 `n`，以及一个正整数 `k`。  
我们称满足下列条件的下标 `i`（其中 `k ≤ i < n - k`）为 **好下标**：

- 下标 `i` 前的 `k` 个元素构成的子数组（subarray）是 **非递增** 的，即 `nums[i - k] ≥ nums[i - k + 1] ≥ ... ≥ nums[i - 1]`；
- 下标 `i` 后的 `k` 个元素构成的子数组（subarray）是 **非递减** 的，即 `nums[i + 1] ≤ nums[i + 2] ≤ ... ≤ nums[i + k]`。

返回所有好下标组成的数组，要求按递增顺序排序。

## 示例

### 示例 1

```text
Input: nums = [2,1,1,1,3,4,1], k = 2
Output: [2,3]
Explanation: 数组中存在两个好下标：
- 下标 2。子数组 [2,1] 为非递增，子数组 [1,3] 为非递减。
- 下标 3。子数组 [1,1] 为非递增，子数组 [3,4] 为非递减。
注意下标 4 不是好下标，因为子数组 [4,1] 不是非递减的。
```

### 示例 2

```text
Input: nums = [2,1,1,2], k = 2
Output: []
Explanation: 该数组不存在好下标。
```

## 约束条件

- `n == nums.length`
- `3 ≤ n ≤ 10^5`
- `1 ≤ nums[i] ≤ 10^6`
- `1 ≤ k ≤ n / 2`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把每一个可能的「好下标」`i`（满足 `k ≤ i < n‑k`）都枚举一遍，然后分别检查：

1. **左侧**：下标 `i‑k … i‑1` 的 `k` 个数是否是**非递增**的  
   （即 `nums[j] ≥ nums[j+1]` 对所有 `j` 成立）。
2. **右侧**：下标 `i+1 … i+k` 的 `k` 个数是否是**非递减**的  
   （即 `nums[j] ≤ nums[j+1]` 对所有 `j` 成立）。

如果两个子数组都满足条件，就把 `i` 加进答案。

> **类比**：把数组想成一排排书。左侧的检查相当于把这 `k` 本书从左到右“压平”，要求每本都不比右边的薄；右侧的检查则是把书从左到右“撑起”，要求每本都不比左边的薄。只要左边压得好、右边撑得好，这个位置就是“好下标”。

**为什么正确**：题目本身的定义就是要检查这两个子数组的单调性，暴力遍历逐个验证自然符合定义。

#### 代码（Python）

```python
from typing import List

def goodIndices_bruteforce(nums: List[int], k: int) -> List[int]:
    n = len(nums)
    ans = []

    # 只枚举可能的 i，省掉两端的无效位置
    for i in range(k, n - k):
        # 检查左侧 k 个数是否非递增
        left_ok = True
        for j in range(i - k, i - 1):          # j 从 i‑k 到 i‑2
            if nums[j] < nums[j + 1]:          # 只要出现递增就不行
                left_ok = False
                break

        # 检查右侧 k 个数是否非递减
        right_ok = True
        for j in range(i + 1, i + k):          # j 从 i+1 到 i+k‑1
            if nums[j] > nums[j + 1]:          # 只要出现递减就不行
                right_ok = False
                break

        if left_ok and right_ok:
            ans.append(i)

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n * k)`  
  - 对每个可能的 `i`（最多 `n` 个）都要检查 `k` 次左侧和 `k` 次右侧。  
  - 当 `k` 接近 `n/2` 时，最坏会变成 `O(n²)`，即“平方级”，相当于把一张 10 000 × 10 000 的表格全部填满再读一遍，计算量很大。

- **空间复杂度**：`O(1)`（不计答案数组）  
  - 只用了常数级的额外变量。

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于每次都要**重复遍历**左侧和右侧的 `k` 个元素。  
我们可以把「连续的非递增」和「连续的非递减」信息**提前算好**，以后只需要**查表**，就能在 `O(1)` 时间判断某个位置左/右侧是否满足要求。

**关键技巧**：**前缀/后缀计数**（也叫「单调段长度」），它是一种**动态规划**的思路：

1. **左侧计数 `left[i]`**  
   - 含义：从 `i` 往左数，连续满足 `nums[t] ≥ nums[t+1]`（非递增）的元素个数（包括 `i` 本身）。  
   - 递推公式（从左到右遍历）  
     ```
     if nums[i] <= nums[i-1]:   # 前一个不比当前大，说明还能继续向左保持非递增
         left[i] = left[i-1] + 1
     else:
         left[i] = 1            # 只能自己一个，向左就断了
     ```
   - 这样 `left[i]` 实际上记录了「以 i 为右端点的最长非递增段长度」。

2. **右侧计数 `right[i]`**  
   - 含义：从 `i` 往右数，连续满足 `nums[t] ≤ nums[t+1]`（非递减）的元素个数（包括 `i` 本身）。  
   - 递推公式（从右到左遍历）  
     ```
     if nums[i] <= nums[i+1]:   # 当前不比右边大，说明还能继续向右保持非递减
         right[i] = right[i+1] + 1
     else:
         right[i] = 1
     ```

3. **判断好下标**  
   - 对于下标 `i`，左侧需要 `k` 个元素全都满足非递增，即 **左端点是 `i-1`**，要求 `left[i-1] >= k`。  
   - 右侧需要 `k` 个元素全都满足非递减，即 **右端点是 `i+1`**，要求 `right[i+1] >= k`。  
   - 同时 `i` 必须落在合法区间 `k ≤ i < n‑k`。

> **类比**：把 `left` 看成「从左边往右数的递减梯子长度」，`right` 看成「从右边往左数的递增梯子长度」。只要左边的梯子够长（≥k）且右边的梯子也够长（≥k），站在中间的台阶 `i` 就是「好台阶」。

#### 代码（Python）

```python
from typing import List

def goodIndices(nums: List[int], k: int) -> List[int]:
    n = len(nums)
    # left[i]：以 i 为右端点的最长非递增段长度（包括 i 本身）
    left = [1] * n
    for i in range(1, n):
        if nums[i] <= nums[i - 1]:          # 前一个不小于当前 → 仍然是非递增
            left[i] = left[i - 1] + 1
        # else left[i] 仍为 1

    # right[i]：以 i 为左端点的最长非递减段长度（包括 i 本身）
    right = [1] * n
    for i in range(n - 2, -1, -1):
        if nums[i] <= nums[i + 1]:          # 当前不大于后一个 → 仍然是非递减
            right[i] = right[i + 1] + 1
        # else right[i] 仍为 1

    ans = []
    # 只遍历可能的 i
    for i in range(k, n - k):
        # 左侧需要以 i-1 为右端点的非递增段长度 >= k
        # 右侧需要以 i+1 为左端点的非递减段长度 >= k
        if left[i - 1] >= k and right[i + 1] >= k:
            ans.append(i)

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历了三遍数组（一次算 `left`，一次算 `right`，一次收集答案），每次都是线性操作。  
  - 与暴力解的 `O(n·k)` 相比，尤其在 `k` 很大时（比如 `k≈n/2`），速度提升可达 **数十倍**。

- **空间复杂度**：`O(n)`  
  - 需要两个额外的同长度数组 `left`、`right` 来保存中间信息。  
  - 若在意空间，还可以把 `right` 直接在原数组上复用或用滚动变量把空间降到 `O(1)`，但 `O(n)` 已经完全可以接受（`n ≤ 10⁵`）。

---

## 心得

- **核心技巧**：用**前缀/后缀计数**（或称“单调段长度”）把局部单调性预处理成 O(1) 查询。  
- **适用题型**  
  1. **连续子数组满足单调/相等条件**（如 LeetCode 2289 *Steps to Make Array Non-decreasing*）。  
  2. **需要在每个位置快速判断左/右侧满足某种“连续”约束**（如 2289、2420 *Find All Good Indices* 的变形）。  
  3. **滑动窗口里要判断窗口内是否全为递增或递减**（可以用同样的计数技巧代替每次遍历）。

- **一句话总结**：**把“每次都走路检查”改成“先铺好路标，走到哪儿直接看路标”。**

---

## 反思

- **第一反应**：直接遍历每个候选下标并逐个检查左右 `k` 个数——这就是暴力解。  
- **最容易踩的坑**  
  - **边界**：`i` 必须满足 `k ≤ i < n‑k`，否则左/右侧的 `k` 个数根本不存在。  
  - **计数起始值**：`left[i]`、`right[i]` 都要包括自身，初始化为 `1`（而不是 `0`），否则会把实际长度少算 1。  
  - **相等情况**：题目要求「非递增」和「非递减」，所以等号是允许的，条件里要用 `<=` 而不是 `<`（或 `>=` 而不是 `>`）。

- **下次遇到同类题**：第一步想到 **“能否把局部的单调性提前预处理？”**，如果可以，就立刻写出两遍 DP（左→右、右→左）来得到 O(1) 判断，从而把时间复杂度从 `O(n·k)` 降到 `O(n)`。