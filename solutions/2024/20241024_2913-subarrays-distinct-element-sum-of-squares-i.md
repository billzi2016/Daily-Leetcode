# #2913. 子数组不同元素计数平方和 I / Subarrays Distinct Element Sum of Squares I

> 难度：简单 · 标签：Array、Hash Table · [LeetCode 链接](https://leetcode.com/problems/subarrays-distinct-element-sum-of-squares-i/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums.
The distinct count of a subarray of nums is defined as:
Return the sum of the squares of distinct counts of all subarrays of nums.
A subarray is a contiguous non-empty sequence of elements within an array.

**Examples**

**Example 1:**

```
Input: nums = [1,2,1]
Output: 15
Explanation: Six possible subarrays are:
[1]: 1 distinct value
[2]: 1 distinct value
[1]: 1 distinct value
[1,2]: 2 distinct values
[2,1]: 2 distinct values
[1,2,1]: 2 distinct values
The sum of the squares of the distinct counts in all subarrays is equal to 12 + 12 + 12 + 22 + 22 + 22 = 15.
```

**Example 2:**

```
Input: nums = [1,1]
Output: 3
Explanation: Three possible subarrays are:
[1]: 1 distinct value
[1]: 1 distinct value
[1,1]: 1 distinct value
The sum of the squares of the distinct counts in all subarrays is equal to 12 + 12 + 12 = 3.
```

**Constraints**

- 1 <= nums.length <= 100
- 1 <= nums[i] <= 100

---

## 题目（中文翻译）

给定一个下标从 **0** 开始的整数数组 `nums`。  
子数组（subarray）的 **不同元素计数** 定义为该子数组中不相同的数值个数。  

返回 `nums` 的所有子数组的 **不同元素计数的平方** 的和。

> 子数组是数组中连续且非空的元素序列。

### 示例

**示例 1**  
输入：`nums = [1,2,1]`  
输出：`15`  
解释：所有可能的子数组如下：

- `[1]`：1 个不同的数值  
- `[2]`：1 个不同的数值  
- `[1]`：1 个不同的数值  
- `[1,2]`：2 个不同的数值  
- `[2,1]`：2 个不同的数值  
- `[1,2,1]`：2 个不同的数值  

不同元素计数的平方之和为 `1² + 1² + 1² + 2² + 2² + 2² = 15`。

**示例 2**  
输入：`nums = [1,1]`  
输出：`3`  
解释：所有可能的子数组如下：

- `[1]`：1 个不同的数值  
- `[1]`：1 个不同的数值  
- `[1,1]`：1 个不同的数值  

不同元素计数的平方之和为 `1² + 1² + 1² = 3`。

### 约束

- `1 <= nums.length <= 100`
- `1 <= nums[i] <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**把所有子数组都枚举出来**，然后逐个统计子数组里不同元素的个数，最后把这些个数的平方求和。

- **枚举子数组**：把左端点 `l` 从 `0` 到 `n‑1`，右端点 `r` 从 `l` 到 `n‑1`，每一对 `(l, r)` 就对应一个连续子数组 `nums[l…r]`。  
- **统计不同元素个数**：对每个子数组，用一个集合（`set`）把出现的元素收集起来。集合的大小 `len(set)` 就是该子数组的**distinct count**。  
- **求平方并累计**：把 `len(set) ** 2` 加到答案中。

> **类比**：集合就像一本字典，往里面写单词时，如果单词已经在字典里，页码不变；如果是新单词，就会多出一页。字典的页数（即集合大小）正好等于不同单词的数量。

**为什么正确**：我们把题目要求的「所有子数组」一一列举，并且对每个子数组准确地计算了它的不同元素个数，随后按照题目要求对这个数做平方并相加，显然得到的就是答案。

**时间/空间复杂度**：

- 枚举子数组的两层循环是 `O(n²)`，而对每个子数组再次遍历其内部元素去建集合需要 `O(k)`（`k` 为子数组长度），最坏情况下 `k≈n`，于是整体是 `O(n³)`。  
- 额外空间只用到了一个临时集合，大小不超过子数组长度 `≤ n`，所以是 `O(n)`（在最坏情况下）。

> **大白话**：`O(n³)` 可以想象成「先挑左端点，再挑右端点，最后把子数组里每个数都读一遍」——三层循环，随 `n` 的增大会很快变慢。

#### 代码（Python）

```python
def subarrayDistinctCountSumSq_bruteforce(nums):
    n = len(nums)
    ans = 0

    # 枚举左端点
    for l in range(n):
        # 枚举右端点
        for r in range(l, n):
            # 用集合统计 nums[l..r] 中出现的不同元素
            distinct = set()
            for i in range(l, r + 1):
                distinct.add(nums[i])      # 往集合里“写字典”
            cnt = len(distinct)            # 不同元素的个数
            ans += cnt * cnt                # 求平方并累计
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n³)` —— 三层循环，`n` 越大会很快超时。  
- **空间复杂度**：`O(n)` —— 最坏情况下集合里会装满整个数组的元素。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次子数组结束后都要重新遍历一次子数组来统计不同元素**。我们可以把这一步“搬到”外层循环里，让它随着右端点的移动而 **增量更新**，这样就只需要 `O(1)` 的额外工作来得到当前子数组的 distinct count。

具体做法：

1. 固定左端点 `l`，让右端点 `r` 从 `l` 向右扩展。  
2. 用一个哈希表（`defaultdict(int)`）记录当前窗口 `[l, r]` 中每个数出现的次数。  
   - 当把 `nums[r]` 加入窗口时，若它之前的计数是 `0`（即第一次出现），distinct count **加 1**。  
   - 否则计数增加，但 distinct count 不变。  
3. 这样在每次右端点右移时，我们**只需 O(1)** 就能得到新的 distinct count。把它的平方加入答案即可。  
4. 当左端点左移到下一个位置时，重新清空哈希表，重新从该左端点开始统计。

因为 `n ≤ 100`，即使是 `O(n²)` 也足够快，而相较于 `O(n³)`，这已经是本题的最优（在不使用更高级的数学技巧的情况下）。

> **类比**：哈希表就像一本「实时更新的字典」，每次你往里写一个新单词，字典会立刻告诉你「这是不是新单词」——如果是新单词，就要把页码加一。

#### 代码（Python）

```python
from collections import defaultdict

def subarrayDistinctCountSumSq_opt(nums):
    n = len(nums)
    ans = 0

    # 固定左端点 l
    for l in range(n):
        freq = defaultdict(int)   # 记录窗口内每个数出现的次数
        distinct = 0               # 当前窗口的不同元素个数

        # 右端点 r 从 l 向右扩展
        for r in range(l, n):
            x = nums[r]
            if freq[x] == 0:       # 第一次看到 x
                distinct += 1
            freq[x] += 1           # 更新出现次数

            ans += distinct * distinct   # 把 distinct 的平方加入答案
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 两层循环遍历所有子数组，每次右移只做 `O(1)` 的哈希表更新。  
  - 与暴力 `O(n³)` 相比，省掉了每个子数组内部再遍历一次的开销，速度提升约 `n` 倍。  
- **空间复杂度**：`O(m)`，其中 `m` 是不同元素的种类数（`≤ 100`），相当于 `O(1)` 常数空间。  
  - 哈希表最多存放当前窗口的所有不同元素，最多不超过数组长度。

---

## 心得

- **核心技巧**：**滑动窗口 + 哈希表增量统计**。  
  通过让右端点一步步向右移动，利用哈希表记录出现次数，能够在 `O(1)` 时间内得到窗口的 distinct count，从而把整体复杂度降到 `O(n²)`。  

- **适用的题型**  
  1. **子数组/子串的不同元素统计**（如 “Count Distinct Elements in Subarrays”）。  
  2. **子数组满足某种计数条件**（如 “Longest Substring with At Most K Distinct Characters”）。  
  3. **需要对每个子数组的某个属性做累加**（如 “Sum of Subarray Minimums”）。

- **一句话总结**：**把“每次重新统计”改成“边走边统计”，哈希表帮你记住已经出现的元素**。

---

## 反思

- **第一反应**：直接把所有子数组列出来，然后逐个用集合计数——最自然但最慢的做法。  
- **最容易踩的坑**  
  - 忘记在左端点改变时清空哈希表，导致计数残留。  
  - 对同一个元素多次出现时误把 distinct count 加多次，实际上只在第一次出现时才加。  
  - 处理空数组或单元素数组的边界条件（本题 `nums.length ≥ 1`，但写通用代码时要小心）。  

- **下次类似题的第一步**：**先想能否在遍历的过程中“增量更新”需要的统计信息**，如果能，就把暴力的 `O(n³)` 降到 `O(n²)`（或更低）。这样往往是突破的关键。