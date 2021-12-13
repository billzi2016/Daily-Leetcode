# #1589. 任意排列得到的最大总和 / Maximum Sum Obtained of Any Permutation

> 难度：中等 · 标签：Array、Greedy、Sorting、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/maximum-sum-obtained-of-any-permutation/)

---

## 题目（英文原版）

**Description**

We have an array of integers, nums, and an array of requests where requests[i] = [starti, endi]. The ith request asks for the sum of nums[starti] + nums[starti + 1] + ... + nums[endi - 1] + nums[endi]. Both starti and endi are 0-indexed.
Return the maximum total sum of all requests among all permutations of nums.
Since the answer may be too large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,4,5], requests = [[1,3],[0,1]]
Output: 19
Explanation: One permutation of nums is [2,1,3,4,5] with the following result: 
requests[0] -> nums[1] + nums[2] + nums[3] = 1 + 3 + 4 = 8
requests[1] -> nums[0] + nums[1] = 2 + 1 = 3
Total sum: 8 + 3 = 11.
A permutation with a higher total sum is [3,5,4,2,1] with the following result:
requests[0] -> nums[1] + nums[2] + nums[3] = 5 + 4 + 2 = 11
requests[1] -> nums[0] + nums[1] = 3 + 5  = 8
Total sum: 11 + 8 = 19, which is the best that you can do.
```

**Example 2:**

```
Input: nums = [1,2,3,4,5,6], requests = [[0,1]]
Output: 11
Explanation: A permutation with the max total sum is [6,5,4,3,2,1] with request sums [11].
```

**Example 3:**

```
Input: nums = [1,2,3,4,5,10], requests = [[0,2],[1,3],[1,1]]
Output: 47
Explanation: A permutation with the max total sum is [4,10,5,3,2,1] with request sums [19,18,10].
```

**Constraints**

- n == nums.length
- 1 <= n <= 105
- 0 <= nums[i] <= 105
- 1 <= requests.length <= 105
- requests[i].length == 2
- 0 <= starti <= endi < n

---

## 题目（中文翻译）

我们有一个整数数组 `nums`，以及一个请求数组 `requests`，其中 `requests[i] = [starti, endi]`。第 `i` 个请求要求计算  

`nums[starti] + nums[starti + 1] + ... + nums[endi - 1] + nums[endi]`  

其中 `starti`、`endi` 为 **0** 起始下标。  
返回在 **所有** `nums` 的排列（permutation）中，所有请求的总和的最大可能值。  
由于答案可能非常大，请返回 **模** `10^9 + 7` 的结果。

---

### 示例

#### 示例 1  
**输入**  
```
nums = [1,2,3,4,5], requests = [[1,3],[0,1]]
```  
**输出**  
```
19
```  
**解释**  
一种排列是 `[2,1,3,4,5]`，得到的各请求结果为：  
- `requests[0]` → `nums[1] + nums[2] + nums[3] = 1 + 3 + 4 = 8`  
- `requests[1]` → `nums[0] + nums[1] = 2 + 1 = 3`  

总和为 `8 + 3 = 11`。  
更大的总和可以通过排列 `[3,5,4,2,1]` 实现，其中  
`requests[0]` → `nums[1] + nums[2] + nums[3] = 5 + 4 + 2 = 11`，  
`requests[1]` → `nums[0] + nums[1] = 3 + 5 = 8`，  
总和 `11 + 8 = 19`。

#### 示例 2  
**输入**  
```
nums = [1,2,3,4,5,6], requests = [[0,1]]
```  
**输出**  
```
11
```  
**解释**  
最大总和对应的排列为 `[6,5,4,3,2,1]`，请求和为 `6 + 5 = 11`。

#### 示例 3  
**输入**  
```
nums = [1,2,3,4,5,10], requests = [[0,2],[1,3],[1,1]]
```  
**输出**  
```
47
```  
**解释**  
最大总和对应的排列为 `[4,10,5,3,2,1]`，各请求和分别为  
`requests[0]` → `4 + 10 + 5 = 19`，  
`requests[1]` → `10 + 5 + 3 = 18`，  
`requests[2]` → `10 = 10`，  
总和 `19 + 18 + 10 = 47`。

---

### 约束条件
- `n == nums.length`
- `1 <= n <= 10^5`
- `0 <= nums[i] <= 10^5`
- `1 <= requests.length <= 10^5`
- `requests[i].length == 2`
- `0 <= starti <= endi < n`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**把所有可能的排列都列出来，算出每个排列对应所有请求的总和，取最大值**。  

- **数据结构**：我们只需要普通的数组 `list` 来保存一个排列，和一个二维数组 `requests` 保存每个请求的 `[start, end]`。  
- **为什么能得到答案**：因为我们把所有合法的排列都尝试了一遍，必然会碰到最优的那一个，所以答案一定被找到。  

> **生活类比**：想象有一堆不同重量的石子（`nums`），要把它们摆成一排，然后让小朋友挑选区间（`requests`）来称重。暴力做法就是把石子所有可能的摆法都试一遍，记录每次称出来的总重量，最后挑出最大的。  

#### 代码（Python）  

```python
import itertools
from typing import List

MOD = 10 ** 9 + 7

def maxSumBruteForce(nums: List[int], requests: List[List[int]]) -> int:
    best = 0
    # itertools.permutations 会生成所有排列，n 超过 8 时就会爆炸
    for perm in itertools.permutations(nums):
        total = 0
        # 逐个请求累加区间和
        for l, r in requests:
            # sum(perm[l:r+1]) 直接求区间和
            total += sum(perm[l:r + 1])
        best = max(best, total)
    return best % MOD
```

> **关键行解释**  
> - `itertools.permutations(nums)`：相当于把所有石子排成每一种可能的顺序。  
> - `sum(perm[l:r + 1])`：把小朋友挑选的区间里所有石子的重量相加。  

#### 复杂度  

- **时间复杂度**：`O(n! * m * n)`  
  - `n!` 是所有排列的个数（比如 n=8 时已经是 40320），每个排列要遍历 `m`（请求数）次，每次求区间和最坏要遍历 `n` 次。  
  - **大白话**：时间会随着数组长度指数级增长，几分钟内根本算不完。  

- **空间复杂度**：`O(n)`  
  - 只保存当前排列 `perm`（长度 n）以及常数级的临时变量。  

> 结论：暴力解只能在 **n ≤ 8** 的极小数据上跑通，用来验证思路，不能满足题目给出的 `n ≤ 10⁵`。  

---  

### 2. 最优解  

#### 思路  

从暴力解我们可以看到，**真正决定总和大小的不是排列本身，而是每个位置被请求的次数**。  

1. **统计每个下标被多少次请求覆盖**  
   - 对每个请求 `[l, r]`，下标 `l…r` 都会被该请求计数一次。  
   - 直接对每个请求的每个位置加一会是 `O(n·m)`，太慢。  
   - 用**差分数组**（类似于“区间增量”）只在 `l` 位置加 `+1`，在 `r+1` 位置加 `-1`，最后前缀和一次即可得到每个下标的出现频率。  

2. **把大数放到出现频率高的位置**  
   - 如果某个下标被请求的次数很多，那么把 **最大的 nums** 放到这里能让总和最大化。  
   - 于是把 `freq`（每个位置被请求的次数）从大到小排序，同时把 `nums` 从大到小排序，两者对应相乘后求和，就是答案。  

3. **取模**  
   - 题目要求对 `10⁹+7` 取模，累加时每一步都取模即可防止溢出。  

> **类比**：把 `freq` 想成每个座位的“人气值”，`nums` 想成“明星的知名度”。要让演唱会票房最高，就把最红的明星安排在最火的座位。  

#### 代码（Python）  

```python
from typing import List

MOD = 10 ** 9 + 7

def maxSumRangeQuery(nums: List[int], requests: List[List[int]]) -> int:
    n = len(nums)

    # 1️⃣ 用差分数组统计每个下标被请求的次数
    diff = [0] * (n + 1)            # 多一个位置防止越界
    for l, r in requests:
        diff[l] += 1                # 区间左端点 +1
        diff[r + 1] -= 1            # 区间右端点的下一个位置 -1

    freq = [0] * n                  # 最终的频率数组
    cur = 0
    for i in range(n):
        cur += diff[i]               # 前缀和得到当前位置的累计次数
        freq[i] = cur

    # 2️⃣ 把频率和数值都从大到小排序
    nums.sort(reverse=True)         # 大 → 小
    freq.sort(reverse=True)         # 大 → 小

    # 3️⃣ 计算加权和，途中取模
    ans = 0
    for v, f in zip(nums, freq):
        if f == 0:                   # 频率为 0 的位置对总和没有贡献，后面全是 0
            break
        ans = (ans + v * f) % MOD    # 乘积可能很大，取模防止溢出

    return ans
```

> **关键行解释**  
> - `diff[l] += 1` / `diff[r + 1] -= 1`：把一次请求的“增量”只记录在区间两端，后面一次前缀和就能把它扩散到区间内部。  
> - `cur += diff[i]`：相当于在跑“一条河”，每经过一个位置就把之前所有请求的影响累计起来，得到该位置被请求的次数。  
> - `if f == 0: break`：频率为 0 的位置以后全是 0（因为已经排序），可以提前结束循环，稍微提速。  

#### 复杂度  

- **时间复杂度**：`O(n log n + m)`  
  - `O(m)` 用来遍历所有请求并更新差分数组。  
  - 两次排序 `nums.sort`、`freq.sort` 各是 `O(n log n)`，是主要耗时。  
  - 线性遍历求和是 `O(n)`。  
  - **大白话**：我们只需要把 10⁵ 长的数组排两次序，算一次前缀和，整体运行在几百毫秒以内。  

- **空间复杂度**：`O(n)`  
  - 额外的差分数组 `diff`、频率数组 `freq` 各占 `n` 长度的空间。  

> 与暴力解相比，时间从指数级降到 **线性 + 排序**，可以轻松处理最大输入规模。  

---  

## 心得  

- **核心技巧**：**统计每个下标被请求的频率 + 贪心把大数分配到高频位置**。  
- **适用的题型**  
  1. “数组求和请求” 类题目，如 *Range Sum Query*、*Maximum Sum of Array After Queries*。  
  2. “资源分配” 类贪心题，例如把任务分配给工人，使总收益最大（任务收益对应频率，工人工资对应数值）。  
  3. “区间覆盖计数” 题，如 *Car Pooling*、*Maximum Number of Overlapping Intervals*（都可以用差分数组统计覆盖次数）。  

- **一句话总结解题钥匙**：**把“需求热度”(频率) 排序后，和“资源大小”(数值) 同序匹配，即可得到最大总和**。  

---  

## 反思  

- **第一反应**：直接想遍历所有排列，想到“暴力”但马上发现不行。  
- **最容易踩的坑**  
  1. **差分数组越界**：对 `r+1` 做减法时要确保数组长度是 `n+1`。  
  2. **模运算顺序**：乘积可能超过 64 位整数范围，必须在累加时立即 `% MOD`。  
  3. **频率为 0 的位置**：如果忘记把频率为 0 的位置排在最后，仍然会把它们和小的 `nums` 相乘，答案仍对，但会浪费时间。  

- **下次遇到同类题**：第一步先**统计每个位置被多少次使用**（差分+前缀和），随后**把大数给高频位置**（排序贪心）。这一步几乎是所有“最大化”类区间请求题的通用套路。