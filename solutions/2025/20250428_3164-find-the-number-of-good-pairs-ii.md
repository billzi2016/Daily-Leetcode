# #3164. 好配对数 II / Find the Number of Good Pairs II

> 难度：中等 · 标签：Array、Hash Table · [LeetCode 链接](https://leetcode.com/problems/find-the-number-of-good-pairs-ii/)

---

## 题目（英文原版）

**Description**

You are given 2 integer arrays nums1 and nums2 of lengths n and m respectively. You are also given a positive integer k.
A pair (i, j) is called good if nums1[i] is divisible by nums2[j] * k (0 <= i <= n - 1, 0 <= j <= m - 1).
Return the total number of good pairs.

**Examples**

**Example 1:**

```
Input: nums1 = [1,3,4], nums2 = [1,3,4], k = 1
Output: 5
Explanation:
```

**Example 2:**

```
Input: nums1 = [1,2,4,12], nums2 = [2,4], k = 3
Output: 2
Explanation:
The 2 good pairs are (3, 0) and (3, 1) .
```

**Constraints**

- 1 <= n, m <= 105
- 1 <= nums1[i], nums2[j] <= 106
- 1 <= k <= 103

---

## 题目（中文翻译）

给定两个整数数组（integer arrays）`nums1` 和 `nums2`，长度分别为 `n` 和 `m`。同时给定一个正整数 `k`。  
如果满足 `nums1[i]` 能被 `nums2[j] * k` 整除，则称配对（pair）`(i, j)` 为**好配对（good pair）**（`0 <= i <= n - 1, 0 <= j <= m - 1`）。  
返回所有好配对的数量。

**示例 1**  
``` 
Input: nums1 = [1,3,4], nums2 = [1,3,4], k = 1
Output: 5
Explanation: 
```

**示例 2**  
``` 
Input: nums1 = [1,2,4,12], nums2 = [2,4], k = 3
Output: 2
Explanation: 
有两个好配对，分别是 (3, 0) 和 (3, 1) 。
```

**约束条件**  
- `1 <= n, m <= 10^5`  
- `1 <= nums1[i], nums2[j] <= 10^6`  
- `1 <= k <= 10^3`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有可能的下标组合都枚举一遍：

1. 遍历 `i`（0 … n‑1），取出 `nums1[i]`。  
2. 再遍历 `j`（0 … m‑1），取出 `nums2[j]`。  
3. 检查 `nums1[i]` 是否能被 `nums2[j] * k` 整除。  
   - 整除的条件可以写成 `nums1[i] % (nums2[j] * k) == 0`。  

这就像在现实生活中把两堆苹果一个个配对，看看每对是否满足“左边的重量是右边重量的 k 倍的整数倍”。  

**为什么正确**：我们把所有可能的 `(i, j)` 都检查了一遍，只要满足条件就计数，最终得到的计数必然等于题目要求的“好对”数目。

#### 代码（Python）

```python
def number_of_good_pairs_bruteforce(nums1, nums2, k):
    """
    暴力枚举所有 (i, j) ，统计满足 nums1[i] 能被 nums2[j] * k 整除的对数
    """
    count = 0
    for i, a in enumerate(nums1):                 # 第一次遍历 nums1
        for j, b in enumerate(nums2):             # 第二次遍历 nums2
            if a % (b * k) == 0:                  # 判断是否能整除
                count += 1
    return count
```

#### 复杂度  

- **时间复杂度**：`O(n * m)`  
  - 这里的 `n` 是 `nums1` 长度，`m` 是 `nums2` 长度。  
  - 想象一下你要在两条长为 `n`、`m` 的队列中挑选每一对人，这显然会很慢。  
- **空间复杂度**：`O(1)`  
  - 只用了几个计数变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **双层循环**：每次都要遍历 `nums2`，导致 `n*m` 次检查。  
我们需要把“遍历 `nums2` 的过程”省掉，改为 **一次性查询**。

关键观察：

- 条件 `nums1[i]` 能被 `nums2[j] * k` 整除  
  ⇔ `nums1[i]` 是 `nums2[j] * k` 的 **倍数**。  
- 如果我们事先知道 **每个可能的数** 在 `nums1` 中出现了多少次（频率），
  那么对于任意一个 `target = nums2[j] * k`，只要把所有 `target` 的 **倍数** 的频率加起来，就得到与这个 `j` 对应的好对数。

于是可以把问题转化为：

1. **统计 `nums1` 中每个数的出现次数**。  
   - 由于 `nums1[i] ≤ 10⁶`，我们可以直接用长度为 `max_val+1` 的数组 `freq`（类似字典）来存，  
     就像把所有数字写进一本“电话号码簿”，数字是键，出现次数是页码。  
2. 对每个 `j`，计算 `target = nums2[j] * k`，然后遍历 `target, 2*target, 3*target, …`（即 `target` 的所有倍数）直到 `max_val`，把对应的 `freq` 加到答案里。  
   - 这一步相当于“把所有能被 `target` 整除的 `nums1` 元素一次性挑出来”。  

**为什么快**：  
- 对每个 `target` 我们只遍历它的倍数，而不是所有 `nums2`。  
- 所有 `target` 的遍历次数之和等价于 `∑_{t} max_val / t`，其中 `t` 是所有可能的 `target`。  
- 这类似“调和级数”，上界是 `max_val * (1 + 1/2 + 1/3 + …) ≈ max_val * log(max_val)`，即 **O(max_val·log max_val)**，远小于 `O(n·m)`（因为 `n,m ≤ 10⁵`，而 `max_val = 10⁶`）。

下面给出完整实现。  

#### 代码（Python）

```python
def number_of_good_pairs(nums1, nums2, k):
    """
    最优解：利用频率数组 + 倍数遍历
    时间复杂度：O(max_val * log max_val)  (max_val = max(nums1) )
    空间复杂度：O(max_val)
    """
    # 1️⃣ 统计 nums1 中每个数出现的次数
    max_val = max(nums1)                     # nums1 中的最大值，用来决定频率数组大小
    freq = [0] * (max_val + 1)               # freq[x] = x 在 nums1 中出现的次数
    for v in nums1:
        freq[v] += 1

    ans = 0
    # 2️⃣ 对每个 nums2[j]，计算 target = nums2[j] * k
    for b in nums2:
        target = b * k
        if target > max_val:                 # target 已经比 nums1 中所有数都大，后面不可能有倍数
            continue

        # 3️⃣ 遍历 target 的所有倍数，累计对应的出现次数
        #    类似于「筛法」的过程：target, 2*target, 3*target, ...
        mult = target
        while mult <= max_val:
            ans += freq[mult]                # 把所有等于 mult 的 nums1 元素计入答案
            mult += target                   # 前进到下一个倍数

    return ans
```

> **代码细节解释**  
> - `freq` 相当于一本“词典”，`key` 是数字，`value` 是它出现的次数。  
> - `while mult <= max_val:` 这条循环就像在数“第 target、2·target、3·target …”的楼层，直到最高层 `max_val` 为止。  
> - `if target > max_val: continue` 是一个小优化：如果 `target` 已经比 `nums1` 中最大的数还大，那么它的任何倍数都不可能出现在 `nums1`，直接跳过即可。

#### 复杂度  

- **时间复杂度**：`O(max_val * log max_val)`  
  - `max_val ≤ 10⁶`，`log max_val` 约等于 14，整体约在 `1.4×10⁷` 次操作以内，完全可以在一秒内跑完。  
  - 与暴力解的 `O(n·m)`（最坏可达 `10¹⁰`）相比，提升了几个数量级。  
- **空间复杂度**：`O(max_val)`  
  - 需要一个大小为 `max_val+1` 的整数数组来存频率，约占 4 MB（`10⁶` × 4 byte），在普通机器上毫无压力。  

---

## 心得

- **核心技巧**：把“能被 … 整除”转化为“是 … 的倍数”，利用**频率数组 + 倍数遍历**（类似筛法）一次性统计满足条件的元素。  
- **适用场景**：  
  1. 统计数组中满足 “`a[i]` 能被 `b[j]` 整除” 的配对数（如本题）。  
  2. “求所有数对 `(i, j)`，使得 `a[i] + a[j]` 能被 `k` 整除”。（可以用余数频率 + 组合计数）  
  3. “统计数组中每个数的约数出现次数”。（利用约数枚举或倍数遍历）  
- **一句话总结**：**把除法条件换成倍数搜索，利用频率表一次遍历所有可能的倍数**，即可把暴力的二次循环压到准线性。

---

## 反思

- **第一反应**：直接双层循环，写出最朴素的实现。  
- **最容易踩的坑**：  
  - `nums2[j] * k` 可能会超过 `int` 范围（在 Python 中不会溢出，但要注意是否超过 `max_val`，否则遍历倍数会无限循环）。  
  - 忘记对 `target > max_val` 的提前剪枝，会导致不必要的循环。  
  - `freq` 的大小必须以 `max(nums1)` 为界，若取错界限会出现 IndexError。  
- **下次类似题目**：第一步先**统计一个数组的频率**（或余数/约数等），再把条件转化为“倍数”“余数”等可以**一次性遍历**的形式，这样往往能把时间从 `O(n·m)` 降到 `O(N log N)` 甚至 `O(N)`。