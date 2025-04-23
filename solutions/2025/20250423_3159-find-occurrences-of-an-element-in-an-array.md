# #3159. 在数组中查找元素的第 k 次出现位置 / Find Occurrences of an Element in an Array

> 难度：中等 · 标签：Array、Hash Table · [LeetCode 链接](https://leetcode.com/problems/find-occurrences-of-an-element-in-an-array/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums, an integer array queries, and an integer x.
For each queries[i], you need to find the index of the queries[i]th occurrence of x in the nums array. If there are fewer than queries[i] occurrences of x, the answer should be -1 for that query.
Return an integer array answer containing the answers to all queries.

**Examples**

**Example 1:**

```
Input: nums = [1,3,1,7], queries = [1,3,2,4], x = 1
Output: [0,-1,2,-1]
Explanation:
```

**Example 2:**

```
Input: nums = [1,2,3], queries = [10], x = 5
Output: [-1]
Explanation:
```

**Constraints**

- 1 <= nums.length, queries.length <= 105
- 1 <= queries[i] <= 105
- 1 <= nums[i], x <= 104

---

## 题目（中文翻译）

You are given an integer array（integer array）`nums`, an integer array（integer array）`queries`, and an integer `x`.  
For each `queries[i]`, you need to find the index of the `queries[i]`‑th occurrence of `x` in the `nums` array. If there are fewer than `queries[i]` occurrences of `x`, the answer should be `-1` for that query.  
Return an integer array（integer array）`answer` containing the answers to all queries.

**示例 1**  
Input: `nums = [1,3,1,7]`, `queries = [1,3,2,4]`, `x = 1`  
Output: `[0,-1,2,-1]`  
Explanation:  

**示例 2**  
Input: `nums = [1,2,3]`, `queries = [10]`, `x = 5`  
Output: `[-1]`  
Explanation:  

**约束条件**  

- `1 <= nums.length, queries.length <= 10^5`  
- `1 <= queries[i] <= 10^5`  
- `1 <= nums[i], x <= 10^4`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：**对每一个查询 `queries[i]`，从头遍历数组 `nums`，数一数出现了多少次 `x`，当计数等于 `queries[i]` 时，就把当前下标记下来**。如果遍历结束仍没有达到要求的次数，就返回 `-1`。  

- **使用的数据结构**：只需要遍历 `nums`，不需要额外的容器。可以把遍历过程想象成在一本书里找第几次出现的某个词，逐页翻阅，遇到一次就记个数，数到第 `k` 次就停下来。  
- **为什么正确**：因为我们严格按照题目要求的“第 `k` 次出现”顺序检查，每次都从数组最左边开始，所以一定能得到正确的下标（如果存在的话）。  

#### 代码（Python）  
```python
def find_occurrences_bruteforce(nums, queries, x):
    """
    暴力实现：对每个查询都重新遍历 nums。
    返回一个列表 ans，ans[i] 为第 queries[i] 次出现 x 的下标，若不存在则为 -1。
    """
    ans = []
    for k in queries:                     # 对每个查询 k（第 k 次出现）
        cnt = 0                            # 已经找到了多少次 x
        idx = -1                           # 默认答案是 -1
        for i, val in enumerate(nums):    # 从左到右遍历 nums
            if val == x:                  # 只关心等于 x 的位置
                cnt += 1                  # 计数加一
                if cnt == k:              # 找到第 k 次出现
                    idx = i                # 记录下标
                    break                  # 可以提前结束本次遍历
        ans.append(idx)                    # 把答案放进结果列表
    return ans
```

#### 复杂度  
- **时间复杂度**：`O(n * m)`（`n = len(nums)`，`m = len(queries)`）。  
  直观解释：想象你要找 `m` 次“第 k 次出现”，每次都要把整本书（长度 `n`）从头翻一遍，所以总共要翻 `m` 本书，最坏情况下每本都要翻完整本。  
- **空间复杂度**：`O(1)`（不使用额外的随问题规模增长的容器，只用了常数级别的计数器和结果列表）。  

---

### 2. 最优解  

#### 思路  
从暴力解可以看到，**最大的瓶颈在于每次查询都要重新遍历整个 `nums`**。如果我们把 `nums` 中所有 `x` 出现的位置一次性记下来，下次查询就可以直接定位，而不需要再遍历。  

具体步骤如下：

1. **预处理**：遍历 `nums` 一遍，收集所有等于 `x` 的下标，存入一个列表 `pos`。这一步类似于在字典里查“词条 x 的所有页码”。  
2. **回答查询**：对于每个 `k = queries[i]`，只要检查 `pos` 的长度是否 ≥ `k`。  
   - 如果足够，答案就是 `pos[k‑1]`（因为列表是 0 基的，第 `k` 次出现对应下标 `k-1`）。  
   - 否则返回 `-1`。  

这样，**每个查询的时间只剩下 O(1)**，总体时间就是一次遍历 `nums` 加上一次遍历 `queries`，即 `O(n + m)`。

> **核心数据结构——哈希表（字典）**  
> 这里我们其实只需要一个列表 `pos`，但如果题目要求查询多个不同的元素，就可以把每个元素的出现位置列表放进哈希表：`hash[element] = [所有下标]`。哈希表就像是“查字典”，`key` 是元素的值，`value` 是它出现的所有位置。

#### 代码（Python）  
```python
def find_occurrences_optimal(nums, queries, x):
    """
    最优实现：先把所有 x 出现的下标收集起来，随后每个查询 O(1) 直接定位。
    """
    # 1. 预处理：收集 x 的所有出现位置
    pos = []                     # 用来存放下标的列表
    for i, val in enumerate(nums):
        if val == x:             # 只关心等于 x 的元素
            pos.append(i)        # 把它的下标加入列表

    # 2. 回答每个查询
    ans = []
    for k in queries:            # k 表示第 k 次出现
        if k <= len(pos):        # 检查是否有足够多的出现次数
            ans.append(pos[k-1]) # 第 k 次出现对应列表中的第 k-1 项
        else:
            ans.append(-1)       # 不足 k 次，返回 -1
    return ans
```

#### 复杂度  
- **时间复杂度**：`O(n + m)`。  
  - `n` 步遍历一次 `nums` 收集位置；  
  - `m` 步遍历 `queries`，每步只做常数次比较和索引。  
  与暴力解相比，省掉了每次查询都遍历 `nums` 的巨大开销。  
- **空间复杂度**：`O(c)`，其中 `c` 是 `x` 在 `nums` 中出现的次数。  
  - 我们需要把所有出现位置存下来，相当于把这部分信息“搬进了记事本”。如果 `x` 出现很多，空间就会相应增大；但在最坏情况下 `c ≤ n`，仍然是线性的。  

---

## 心得  

- **核心技巧**：**预处理 + 索引直接访问**（即把“出现位置”提前记录下来）。  
- **适用的题型**  
  1. “查询某个元素第 k 次出现的下标”——本题。  
  2. “给定数组，快速回答区间内某个值出现次数”——可以先把每个值的前缀计数列表存起来。  
  3. “多次查询同一数组中某个数的最近位置”——同样先保存所有位置，用二分查找或直接索引。  
- **一句话总结**：**把“要反复查的东西”一次性记下来，查询时直接定位，省时又省力。**  

---

## 反思  

- **第一反应**：看到“第 k 次出现”，本能想要“一次遍历一次计数”。这就是暴力思路。  
- **最容易踩的坑**  
  - **下标从 0 开始**：`k` 是第几次出现（从 1 开始计数），对应列表索引要减一。  
  - **查询值可能不存在**：如果 `x` 完全不在 `nums`，`pos` 为空，直接返回 `-1`。  
  - **大数据量**：`nums`、`queries` 均可达 `10⁵`，若仍使用暴力会超时。  
- **下次遇到同类题**：第一步先**思考能否一次遍历把所有需要的“信息”收集好**（比如出现位置、前缀和、最大最小值等），再利用这些信息在 O(1) 或 O(log n) 内回答每个查询。这样就能把时间从 “每次查询都遍历” 降到 “一次遍历 + 快速查询”。