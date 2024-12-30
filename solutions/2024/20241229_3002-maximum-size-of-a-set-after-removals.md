# #3002. 移除元素后集合的最大大小 / Maximum Size of a Set After Removals

> 难度：中等 · 标签：Array、Hash Table、Greedy · [LeetCode 链接](https://leetcode.com/problems/maximum-size-of-a-set-after-removals/)

---

## 题目（英文原版）

**Description**

You are given two 0-indexed integer arrays nums1 and nums2 of even length n.
You must remove n / 2 elements from nums1 and n / 2 elements from nums2. After the removals, you insert the remaining elements of nums1 and nums2 into a set s.
Return the maximum possible size of the set s.

**Examples**

**Example 1:**

```
Input: nums1 = [1,2,1,2], nums2 = [1,1,1,1]
Output: 2
Explanation: We remove two occurences of 1 from nums1 and nums2. After the removals, the arrays become equal to nums1 = [2,2] and nums2 = [1,1]. Therefore, s = {1,2}.
It can be shown that 2 is the maximum possible size of the set s after the removals.
```

**Example 2:**

```
Input: nums1 = [1,2,3,4,5,6], nums2 = [2,3,2,3,2,3]
Output: 5
Explanation: We remove 2, 3, and 6 from nums1, as well as 2 and two occurrences of 3 from nums2. After the removals, the arrays become equal to nums1 = [1,4,5] and nums2 = [2,3,2]. Therefore, s = {1,2,3,4,5}.
It can be shown that 5 is the maximum possible size of the set s after the removals.
```

**Example 3:**

```
Input: nums1 = [1,1,2,2,3,3], nums2 = [4,4,5,5,6,6]
Output: 6
Explanation: We remove 1, 2, and 3 from nums1, as well as 4, 5, and 6 from nums2. After the removals, the arrays become equal to nums1 = [1,2,3] and nums2 = [4,5,6]. Therefore, s = {1,2,3,4,5,6}.
It can be shown that 6 is the maximum possible size of the set s after the removals.
```

**Constraints**

- n == nums1.length == nums2.length
- 1 <= n <= 2 * 104
- n is even.
- 1 <= nums1[i], nums2[i] <= 109

---

## 题目（中文翻译）

给定两个下标从 0 开始的整数数组 `nums1` 和 `nums2`，它们的长度均为偶数 `n`。  
你需要分别从 `nums1` 中移除 `n / 2` 个元素，并从 `nums2` 中移除 `n / 2` 个元素。移除完毕后，将剩余的 `nums1` 与 `nums2` 中的所有元素插入到一个集合 `s`（set）中。  
返回集合 `s` 的最大可能大小。

**示例 1**  
**输入**: `nums1 = [1,2,1,2]`, `nums2 = [1,1,1,1]`  
**输出**: `2`  
**解释**: 我们从 `nums1` 与 `nums2` 中各移除两个 `1`。移除后，`nums1 = [2,2]`，`nums2 = [1,1]`，因此 `s = {1,2}`。可以证明，`2` 是在所有合法移除方式下集合 `s` 的最大可能大小。

**示例 2**  
**输入**: `nums1 = [1,2,3,4,5,6]`, `nums2 = [2,3,2,3,2,3]`  
**输出**: `5`  
**解释**: 我们从 `nums1` 中移除 `2、3、6`，从 `nums2` 中移除 `2` 与两个 `3`。移除后，`nums1 = [1,4,5]`，`nums2 = [2,3,2]`，因此 `s = {1,2,3,4,5}`。可以证明，`5` 是集合 `s` 的最大可能大小。

**示例 3**  
**输入**: `nums1 = [1,1,2,2,3,3]`, `nums2 = [4,4,5,5,6,6]`  
**输出**: `6`  
**解释**: 我们从 `nums1` 中移除 `1、2、3`，从 `nums2` 中移除 `4、5、6`。移除后，`nums1 = [1,2,3]`，`nums2 = [4,5,6]`，因此 `s = {1,2,3,4,5,6}`。可以证明，`6` 是集合 `s` 的最大可能大小。

**约束条件**  
- `n == nums1.length == nums2.length`  
- `1 <= n <= 2 * 10^4`  
- `n` 为偶数  
- `1 <= nums1[i], nums2[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可能的删除方式都穷举一遍**，看哪一种能得到最大的集合大小。

- 对 `nums1`，我们需要删掉 `n/2` 个元素，也就是**保留** `n/2` 个元素。  
- 对 `nums2` 同理。  
- 把保留下来的两个子数组合并放进集合 `s`（集合天然会把相同的数字合并），统计 `s` 的大小。

> **类比**：想象你有两袋糖果，每袋恰好有 `n/2` 颗糖要留下。你可以把每一种糖果的颜色记在一本字典里（集合），相同颜色只记一次。要想让颜色种类最多，就要把所有可能的挑选方式都尝试一遍。

**为什么这一定能得到正确答案**  
因为我们枚举了**所有**合法的保留方案，最大值必然出现在其中。

**时间/空间复杂度**  
- 对每个数组，要从 `n` 个元素里选 `n/2` 个，组合数是 `C(n, n/2)`，两数组组合数是 `C(n, n/2)^2`。  
- 对每一种组合，还要把元素放进集合并统计大小，时间是 `O(n)`。  

所以整体时间是 **指数级**，在最坏情况下大约是 `O( C(n, n/2)^2 * n )`，即 **爆炸性增长**，即使 `n=20` 也会非常慢。  
空间上，只需要存放当前的两个子数组和集合，`O(n)`。

> **大白话**：`O(n²)` 代表“随 `n` 增长，耗时会像 `n` 的平方那样快”。这里的复杂度比 `n²` 还快很多，几乎是“不可接受的慢”。

#### 代码（Python）

```python
import itertools
from typing import List

def max_set_size_bruteforce(nums1: List[int], nums2: List[int]) -> int:
    n = len(nums1)
    keep = n // 2                     # 每个数组要保留的个数
    best = 0

    # 枚举 nums1 的所有保留方案
    for keep1 in itertools.combinations(range(n), keep):
        set1 = {nums1[i] for i in keep1}          # 把保留下来的元素放进集合
        # 枚举 nums2 的所有保留方案
        for keep2 in itertools.combinations(range(n), keep):
            set2 = {nums2[i] for i in keep2}
            cur = len(set1 | set2)                # 并集的大小就是集合 s 的大小
            best = max(best, cur)
    return best
```

> 这段代码只能用于 **非常小的 n**（比如 `n ≤ 12`）来验证思路，实际提交会超时。

#### 复杂度

- 时间复杂度：`O( C(n, n/2)^2 * n )` —— 组合数的指数增长，几乎不可接受。  
- 空间复杂度：`O(n)` —— 只存放当前的两个子集合和临时集合。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**枚举所有组合太慢**，我们需要利用题目结构来直接算出最大可能的集合大小，而不是去尝试每一种情况。

**关键观察 1：只要保留的元素种类越多，集合 `s` 越大**。  
所以我们应该**优先保留那些在另一数组里根本不存在的元素**——这些元素一定会为集合贡献一个新的数字。

- 在 `nums1` 中，只有 `nums1` 有而 `nums2` 没有的数字记为 **只在 1 中出现**，记作 `only1`。  
- 同理，记 `only2` 为只在 `nums2` 中出现的数字。  
- 两个数组都出现的数字记作 **公共数字**，记作 `common`。

> **类比**：把 `nums1` 看成「左边的水果篮」，`nums2` 看成「右边的水果篮」。  
> - 左篮子里独有的水果（只在左边）就像「稀有水果」，放进去一定能让水果种类增加。  
> - 右篮子里独有的水果同理。  
> - 两篮子都有的水果（公共）如果已经放进集合，第二次放进来就不再增加种类。

**关键观察 2：每个数组只能保留 `n/2` 个元素**，这相当于每边有 `n/2` 个「名额」可以填。  
我们把名额先分配给「只在本数组出现」的数字，剩下的名额再填「公共」数字。

设  

- `a = |only1|`（只在 `nums1` 中出现的不同数字个数）  
- `b = |only2|`（只在 `nums2` 中出现的不同数字个数）  
- `c = |common|`（公共不同数字的个数）  

每边最多能放进的独有数字数量是 `min(a, n/2)` 和 `min(b, n/2)`。  
放完独有数字后，左边还剩 `left1 = n/2 - min(a, n/2)` 个空位，右边剩 `left2 = n/2 - min(b, n/2)` 个空位。  
公共数字如果要增加集合大小，必须同时被左、右两边保留下来（否则只保留在一边并不会产生新种类，因为另一边已经有同样的数字）。  
因此可以再加入的公共数字数量是 `min(c, left1, left2)`。

**最终答案**  

```
answer = min(a, n/2) + min(b, n/2) + min(c, left1, left2)
```

整个过程只需要遍历两遍数组，统计出现次数或直接构造集合，时间线性，空间常数。

#### 代码（Python）

```python
from typing import List

def maximumSetSize(nums1: List[int], nums2: List[int]) -> int:
    n = len(nums1)
    half = n // 2                     # 每个数组必须保留的个数

    # 用集合直接得到不同的数字集合
    set1 = set(nums1)
    set2 = set(nums2)

    # 只在 nums1 中出现的数字
    only1 = set1 - set2
    # 只在 nums2 中出现的数字
    only2 = set2 - set1
    # 两边都有的数字
    common = set1 & set2

    a = len(only1)        # |only1|
    b = len(only2)        # |only2|
    c = len(common)      # |common|

    # 先把独有数字尽可能多地放进去
    keep_only1 = min(a, half)
    keep_only2 = min(b, half)

    # 计算每边剩余的名额
    left1 = half - keep_only1
    left2 = half - keep_only2

    # 再把公共数字放进去，受三者共同限制
    keep_common = min(c, left1, left2)

    return keep_only1 + keep_only2 + keep_common
```

> **关键行注释**  
> - `only1 = set1 - set2`：集合的差集，好比把「左篮子」的水果和「右篮子」的水果做对比，只留下左边独有的。  
> - `common = set1 & set2`：集合的交集，就是两边都有的水果。  
> - `min(a, half)`：左边独有的水果如果多过名额，只能挑 `half` 个保留下来。  
> - `min(c, left1, left2)`：公共水果要同时占用左、右两边的空位，受最小的那一边限制。

#### 复杂度

- 时间复杂度：`O(n)` —— 只遍历两遍数组，集合操作均摊为常数。  
  - **大白话**：如果数组长度是 10 000，程序大约只需要跑 10 000 次基本操作，几乎是瞬间完成。  
- 空间复杂度：`O(u)`，其中 `u` 是两数组中不同数字的总数（最多 `2n`），在最坏情况下仍是线性 `O(n)`。  
  - 实际上只用了三个集合，常数级别的额外空间。

---

## 心得

- **核心技巧**：利用集合的差集、交集，**贪心**地先保留只出现一次的元素，再在剩余名额内填公共元素。  
- **适用的题型**  
  1. “在两个集合中挑选元素，使得最终集合大小最大”——如 *Maximum Size of a Set After Removals*。  
  2. “在限制次数的删除/保留操作下，最大化不同元素数目”——如 *Maximum Number of Distinct Elements After Removal*（类似思路）。  
  3. “两组资源各有配额，尽量让最终种类最多”——如 *Maximum Diversity of Selected Items*。  
- **一句话总结解题钥匙**：**先抢独有的，再用公共填剩余名额**。

---

## 反思

- **第一反应**：想到枚举所有删除方式，直接暴力搜索。  
- **最容易踩的坑**  
  - 忘记每边都有 **固定的保留名额**（`n/2`），导致把所有独有元素都算进去而超出限制。  
  - 误以为只要把公共元素全部保留下来就能增加集合大小，实际上只有当两边都有空位时才有效。  
  - 边界情况：当 `only1` 或 `only2` 已经超过 `n/2`，需要取最小值；当公共元素数目大于剩余名额时，同样要取最小值。  
- **下次类似题的第一步**：**把每个集合的“只出现一次的元素”和“公共元素”分开统计**，再根据各自的配额进行**贪心分配**。这样可以立刻得到 O(n) 的解法，避免暴力枚举的陷阱。