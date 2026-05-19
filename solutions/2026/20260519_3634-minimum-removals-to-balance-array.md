# #3634. 最小删除次数使数组平衡 / Minimum Removals to Balance Array

> 难度：中等 · 标签： · [LeetCode 链接](https://leetcode.com/problems/minimum-removals-to-balance-array/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and an integer k.
An array is considered balanced if the value of its maximum element is at most k times the minimum element.
You may remove any number of elements from nums​​​​​​​ without making it empty.
Return the minimum number of elements to remove so that the remaining array is balanced.
Note: An array of size 1 is considered balanced as its maximum and minimum are equal, and the condition always holds true.

**Examples**

**Example 1:**

```
Input: nums = [2,1,5], k = 2
Output: 1
Explanation:
```

**Example 2:**

```
Input: nums = [1,6,2,9], k = 3
Output: 2
Explanation:
```

**Example 3:**

```
Input: nums = [4,6], k = 2
Output: 0
Explanation:
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 109
- 1 <= k <= 105

---

## 题目（中文翻译）

**描述**  
给定一个整数数组 `nums` 和一个整数 `k`。  
如果数组的最大元素值至多是最小元素值的 `k` 倍，则称该数组是**平衡的（balanced）**。  
你可以从 `nums` 中删除任意数量的元素，但不能使数组为空。  
返回为了使剩余数组平衡，最少需要删除的元素个数。  

> 注：长度为 `1` 的数组始终被视为平衡的，因为此时最大值和最小值相等，条件必然成立。

**示例**  

示例 1:  
```
Input: nums = [2,1,5], k = 2
Output: 1
Explanation:
```

示例 2:  
```
Input: nums = [1,6,2,9], k = 3
Output: 2
Explanation:
```

示例 3:  
```
Input: nums = [4,6], k = 2
Output: 0
Explanation:
```

**约束条件**  
- `1 <= nums.length <= 10^5`  
- `1 <= nums[i] <= 10^9`  
- `1 <= k <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的子数组**（子集），检查每个子数组是否满足“最大值 ≤ k·最小值”。  
- **数据结构**：我们可以把原数组的下标当成“钥匙”，把对应的元素值当成“字典里的解释”。遍历所有子集就像把字典的每一页都翻一遍，看看哪几页组合在一起满足条件。  
- **正确性**：只要把每一种可能的保留元素组合都检查一遍，必然能找到“最少要删多少元素”的答案，因为答案一定对应某个合法子集。  

#### 代码（Python）

```python
from itertools import combinations

def min_removals_brute(nums, k):
    n = len(nums)
    # 从保留 1 个元素开始尝试，逐渐增大保留的元素个数
    for keep in range(1, n + 1):
        # 枚举所有长度为 keep 的子集（下标组合）
        for idxs in combinations(range(n), keep):
            sub = [nums[i] for i in idxs]          # 取出子数组
            if max(sub) <= k * min(sub):           # 检查平衡条件
                # 删除的元素数 = 总数 - 保留的数目
                return n - keep
    return n - 1   # 题目保证不会返回空数组，这里是兜底
```

> **关键行解释**  
> - `combinations(range(n), keep)`: 类比查字典，`range(n)` 是所有“词”，`keep` 是一次要挑选的词数。  
> - `max(sub) <= k * min(sub)`: 直接比较子数组的最大最小值，满足题目要求即为合法。

#### 复杂度  

- **时间复杂度**：`O( C(n,1) + C(n,2) + … + C(n,n) ) = O(2^n)`  
  这相当于“把每本书的每一页都读一遍”，随着元素个数指数级增长，实际运行会非常慢。  
- **空间复杂度**：`O(n)`（存放临时子数组），相当于“打开一本书只放一页在手上”。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**重复检查相同的元素**，尤其是每次都要重新求最大最小值。  
我们可以把数组**先排个序**，这样在有序序列里，任意一个子数组的**最小值就是左端点，最大值就是右端点**。于是问题转化为：

> 在排好序的数组中，找最长的连续区间 `[i, j]` 使得 `nums[j] ≤ k * nums[i]`。

这正好可以用**双指针（滑动窗口）**一次遍历完成：

1. 设左指针 `i` 从 0 开始，右指针 `j` 也从 0 开始向右扩张。  
2. 每次尝试把 `j` 往右移，只要当前窗口仍满足 `nums[j] ≤ k * nums[i]` 就继续扩张。  
3. 当窗口不再满足时，左指针右移 `i += 1`，此时 `j` 已经在合适的位置，继续尝试扩张右指针。  
4. 记录遍历过程中出现的**最大窗口长度** `max_len`。  
5. 最终答案 = `n - max_len`（删掉其余元素）。

> **类比**：把数组想象成排好队的学生，老师要挑选一段连续的学生，使得最高的学生不超过 `k` 倍最低的学生。老师先让最矮的学生站在最左边，然后不断让右边的学生加入队列，只要最高不超过 `k` 倍最矮，就继续；一旦超过，就把最矮的学生踢出队列，让下一个更高的学生成为新的最矮。这样只需要一次遍历就能找到最长的合法队列。

#### 代码（Python）

```python
def min_removals(nums, k):
    """
    返回最少需要删除的元素个数，使得剩余数组满足
    max <= k * min 的平衡条件。
    """
    nums.sort()                     # 先排序，O(n log n)
    n = len(nums)
    max_len = 0                     # 记录最长合法窗口长度
    j = 0                           # 右指针

    for i in range(n):              # 左指针从左到右扫
        # 保证右指针不越界且窗口仍合法
        while j < n and nums[j] <= k * nums[i]:
            j += 1                  # 窗口右边界可以继续扩张

        # 此时窗口是 [i, j-1]，长度为 j-i
        cur_len = j - i
        if cur_len > max_len:
            max_len = cur_len

        # 当左指针 i 移动到 i+1 时，窗口左端会变大，
        # 右指针 j 已经在合法的最右位置，无需回退
        # （因为数组是递增的，新的最小值只会更大，条件更容易满足）

    # 删除的元素数 = 总数 - 最长合法子数组的长度
    return n - max_len
```

> **关键行解释**  
> - `nums.sort()`: 把“杂乱的书架”整理成“按字母顺序排好”，方便后面只看两端。  
> - `while j < n and nums[j] <= k * nums[i]`: 只要右端的书页号不超过左端的 `k` 倍，就继续把书加入窗口。  
> - `j - i`: 窗口长度，即当前可以保留的元素数量。  
> - `return n - max_len`: 删除的元素就是“总书数减去能一次性借走的最多书本数”。

#### 复杂度  

- **时间复杂度**：`O(n log n)`（排序）+ `O(n)`（双指针一次遍历）≈ `O(n log n)`。  
  对比暴力的 `2^n`，这里的 `n log n` 像“先把书排好顺序，然后一次性挑出最长连续的合适段”，即使 `n=10⁵` 也能在毫秒级完成。  
- **空间复杂度**：`O(1)`（不计排序的原地改动），只用了常数个指针变量，相当于“只在手上放了几本参考书”。  

---

## 心得

- **核心技巧**：先排序再使用**双指针（滑动窗口）**寻找满足比例条件的最长连续子数组。  
- **适用的题型**  
  1. “最长子数组满足 `max - min ≤ limit`”——如 LeetCode 1438. 绝对差不超过限制的最长连续子数组。  
  2. “最长子数组满足 `sum ≤ k`”——如 LeetCode 209. 长度最小的子数组之和大于等于目标值。  
  3. “子数组中所有元素满足某种比例/倍数关系”——本题的变形。  
- **一句话总结解题钥匙**：**先把数据排好序，使最小/最大只出现在窗口两端，然后用滑动窗口一次遍历找最长合法区间**。

---

## 反思

- **第一反应**：看到“最大 ≤ k·最小”，立刻想到要比较最大最小值，于是想到枚举子集检查。  
- **最容易踩的坑**  
  - **整数乘法溢出**：`k * nums[i]` 可能超过 32 位整数范围，但 Python 的整数是大数，语言层面安全；在其他语言需要使用 `long long`。  
  - **边界条件**：当所有元素都已经满足条件时，窗口会一直扩到数组末尾，需要保证右指针 `j` 不越界。  
  - **空数组**：题目规定删除后不能为空，但我们的算法天然会保留至少一个元素（因为单个元素总是平衡的）。  
- **下次类似题的第一步**：**先思考能否通过排序把“最大/最小”固定在窗口两端**，若可以，就立刻考虑**双指针/滑动窗口**来线性扫描。这样往往能把指数级搜索降到 `O(n log n)` 或 `O(n)`。