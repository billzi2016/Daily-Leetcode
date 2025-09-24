# #3356. 零数组转换 II / Zero Array Transformation II

> 难度：中等 · 标签：Array、Binary Search、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/zero-array-transformation-ii/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums of length n and a 2D array queries where queries[i] = [li, ri, vali].
Each queries[i] represents the following action on nums:
A Zero Array is an array with all its elements equal to 0.
Return the minimum possible non-negative value of k, such that after processing the first k queries in sequence, nums becomes a Zero Array. If no such k exists, return -1.

**Examples**

**Example 1:**

```
Input: nums = [2,0,2], queries = [[0,2,1],[0,2,1],[1,1,3]]
Output: 2
Explanation:
```

**Example 2:**

```
Input: nums = [4,3,2,1], queries = [[1,3,2],[0,2,1]]
Output: -1
Explanation:
```

**Constraints**

- 1 <= nums.length <= 105
- 0 <= nums[i] <= 5 * 105
- 1 <= queries.length <= 105
- queries[i].length == 3
- 0 <= li <= ri < nums.length
- 1 <= vali <= 5

---

## 题目（中文翻译）

**题目描述**  
给定一个长度为 `n` 的整数数组 `nums` 和一个二维数组 `queries`，其中 `queries[i] = [li, ri, vali]`。  
每个 `queries[i]` 表示对 `nums` 执行以下操作：

- 将下标区间 `[li, ri]`（**闭区间**）内的每个元素加上 `vali`。

**Zero Array（零数组）** 是指所有元素都等于 `0` 的数组。

返回最小的非负整数 `k`，使得按顺序处理前 `k` 条查询后，`nums` 变成 **Zero Array（零数组）**。如果不存在这样的 `k`，返回 `-1`。

---

### 示例

**示例 1**  
```text
Input: nums = [2,0,2], queries = [[0,2,1],[0,2,1],[1,1,3]]
Output: 2
Explanation:
处理前两条查询后，数组变为 [0,0,0]，已经是 Zero Array（零数组），因此答案为 2。
```

**示例 2**  
```text
Input: nums = [4,3,2,1], queries = [[1,3,2],[0,2,1]]
Output: -1
Explanation:
无论处理多少条查询，数组都不可能全部变为 0，故返回 -1。
```

---

### 约束条件
- `1 <= nums.length <= 10^5`
- `0 <= nums[i] <= 5 * 10^5`
- `1 <= queries.length <= 10^5`
- `queries[i].length == 3`
- `0 <= li <= ri < nums.length`
- `1 <= vali <= 5 * 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **按顺序把每一条 query 真正执行一遍**，看什么时候数组全部变成 0。  

- **数据结构**：我们只需要一个普通的 Python 列表 `arr` 来保存当前的数组状态。  
- **生活化类比**：把数组想象成一排水槽，每个水槽里装着一定量的水（`nums[i]`）。每条 query 就是把一段连续的水槽里的水 **往下倒** `val` 单位——倒完后水不能出现负数，就像水槽里最少只能有 0 水一样。  
- **正确性**：我们严格按照题目要求的顺序、严格按照每条 query 的范围和倒水量去修改数组，最终如果所有水槽的水都为 0，说明找到了满足条件的 `k`。  

#### 代码（Python）

```python
def brute_force(nums, queries):
    # 复制一份，防止修改原始输入
    arr = nums[:]                     # 当前数组状态
    for k, (l, r, val) in enumerate(queries, 1):   # k 从 1 开始计数
        # 对区间 [l, r] 逐个元素减去 val，负数截为 0
        for i in range(l, r + 1):
            arr[i] = max(arr[i] - val, 0)
        # 检查是否已经全部为 0
        if all(x == 0 for x in arr):
            return k                 # 最小的 k 找到了
    return -1                         # 所有 query 用完仍不全为 0
```

#### 复杂度  

- **时间复杂度**：`O(m * n)`（最坏情况下每条 query 都遍历整个数组），其中 `m = len(queries)`，`n = len(nums)`。  
  - 大白话：如果数组有 10⁵ 个格子，查询有 10⁵ 条，最糟糕的情况要做 10⁵ × 10⁵ = 10¹⁰ 次“倒水”，这在电脑里根本跑不完。  
- **空间复杂度**：`O(n)`，我们只用额外的一个同等大小的数组来保存当前状态。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈** 在于每次遍历区间 `[l, r]`，导致 `O(m·n)`。  
要想加速，需要把“对同一段区间的多次减法” **合并**，一次性算出每个位置累计被减掉了多少。  

**核心技巧**：**差分数组 + 前缀和 + 二分搜索**  

1. **单调性**  
   - 每执行一次 query，数组元素只能变小（或者保持 0），永远不会回升。  
   - 因此如果前 `k` 条查询已经把数组全部变成 0，后面再继续执行更多查询，数组仍然是全 0。  
   - 这意味着答案 `k` 在 `[0, m]` 区间上是 **单调** 的：`False … False True … True`。  
   - 单调性让我们可以 **二分搜索** 最小的满足条件的 `k`。  

2. **如何在 O(n + k) 内判断前 k 条查询是否足够？**  
   - 用 **差分数组** `diff`（长度 `n+1`）记录每条 query 对区间的影响：  
     - `diff[l] += val`  
     - `diff[r+1] -= val`（如果 `r+1` 在数组范围内）  
   - 对 `diff` 做一次前缀和，就得到 `sub[i]` —— 前 `k` 条查询累计减掉的值。  
   - 最后只要检查 `nums[i] <= sub[i]` 对所有 `i` 成立，就说明第 `i` 位置已经被“倒空”。  

3. **整体流程**  

   ```
   left = 1, right = m, answer = -1
   while left <= right:
       mid = (left + right) // 2          # 试探的 k
       if check(mid):                     # O(n + mid)
           answer = mid
           right = mid - 1                # 继续找更小的 k
       else:
           left = mid + 1                 # 需要更多 query
   return answer
   ```

   - `check(k)` 用差分数组一次性计算前 `k` 条查询的累计减量，随后遍历一次数组验证是否全部为 0。  
   - 由于二分只会调用 `check` 大约 `log₂(m)` 次（最多约 17 次），总体复杂度是 `O((n + m) log m)`，完全可以接受。  

4. **类比**  
   - 差分数组就像在一本“增减日志”里记下每次倒水的起止点，真正倒水只在最后一次性算出每个水槽到底倒了多少。  

#### 代码（Python）

```python
from typing import List

def min_queries_to_zero(nums: List[int], queries: List[List[int]]) -> int:
    """
    返回最小的 k（1-indexed），使得执行前 k 条 queries 后 nums 全部变为 0。
    若不存在则返回 -1。
    """

    n = len(nums)
    m = len(queries)

    # ---------- 判定函数 ----------
    def check(k: int) -> bool:
        """
        判断执行前 k 条查询后，数组是否全为 0。
        采用差分数组 + 前缀和，时间 O(n + k)。
        """
        diff = [0] * (n + 1)          # 差分数组，长度多一个哨兵

        # 把前 k 条查询的增减信息写进 diff
        for i in range(k):
            l, r, val = queries[i]
            diff[l] += val
            if r + 1 < n:
                diff[r + 1] -= val

        # 前缀和得到每个位置累计减掉的量
        cur = 0
        for idx in range(n):
            cur += diff[idx]          # cur = sub[idx]
            # 如果原始值仍大于累计减掉的量，则该位置还没清空
            if nums[idx] > cur:
                return False
        return True

    # ---------- 二分搜索 ----------
    left, right = 1, m
    answer = -1
    while left <= right:
        mid = (left + right) // 2
        if check(mid):
            answer = mid          # 记录一个可能的最小 k
            right = mid - 1       # 向左侧继续搜索更小的 k
        else:
            left = mid + 1        # 需要更多的查询才能清空数组

    return answer
```

#### 复杂度  

- **时间复杂度**：`O((n + m) * log m)`  
  - `log m` 次二分，每次 `check` 需要遍历前 `k` 条查询（最坏是 `m`）以及整个数组 `n`。  
  - 与暴力的 `O(n·m)` 相比，下降到了 **近线性** 级别。  
- **空间复杂度**：`O(n)`  
  - 只使用了一个长度为 `n+1` 的差分数组 `diff`，额外空间与输入规模同阶。  

---

## 心得  

- **核心技巧**：利用 **差分数组** 把区间增减合并，再配合 **二分搜索** 利用答案的单调性。  
- **适用的题型**：  
  1. “区间加/减 + 判定是否满足某种全局条件” 类的题（如 “Range Addition Queries”）  
  2. “最早满足条件的前缀长度” 需要单调性判断的题（如 “Find Minimum Operations to Make Array Empty”）  
  3. “大规模区间更新后求某种属性” 的题（如 “Maximum Subarray Sum After K Operations”）  
- **一句话总结解题钥匙**：**把所有区间操作先累加到差分数组，再用二分定位最早满足全零的前缀**。  

---

## 反思  

- **第一反应**：直接模拟每条 query，遍历区间——这在规模稍大时就会超时。  
- **最容易踩的坑**：  
  - **边界条件**：`r+1` 可能等于 `n`，此时不能写入 `diff`，否则会越界。  
  - **单调性**：必须确认“执行更多查询不会让已经为 0 的位置重新变非零”。这里因为操作是 “减到不低于 0”，单调性成立。  
  - **返回值的 1-indexed**：题目要求的 `k` 是“前 k 条”，而 Python 列表是 0‑indexed，注意二分的左右边界和返回值的对应。  
- **下次类似题的第一步**：先判断是否存在 **单调性**（答案随前缀长度单调递增/递减），如果有，就立刻考虑 **二分 + 前缀/差分** 这条思路。