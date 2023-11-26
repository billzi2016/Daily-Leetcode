# #2488. **计数中位数为 K 的子数组** / Count Subarrays With Median K

> 难度：困难 · 标签：Array、Hash Table、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/count-subarrays-with-median-k/)

---

## 题目（英文原版）

**Description**

You are given an array nums of size n consisting of distinct integers from 1 to n and a positive integer k.
Return the number of non-empty subarrays in nums that have a median equal to k.
Note:

**Examples**

**Example 1:**

```
Input: nums = [3,2,1,4,5], k = 4
Output: 3
Explanation: The subarrays that have a median equal to 4 are: [4], [4,5] and [1,4,5].
```

**Example 2:**

```
Input: nums = [2,3,1], k = 3
Output: 1
Explanation: [3] is the only subarray that has a median equal to 3.
```

**Constraints**

- n == nums.length
- 1 <= n <= 105
- 1 <= nums[i], k <= n
- The integers in nums are distinct.

---

## 题目（中文翻译）

给定一个长度为 `n` 的数组 `nums`，其中元素为 `1` 到 `n` 的互不相同的整数，以及一个正整数 `k`。  
返回 `nums` 中所有非空子数组（subarray）且其中位数（median）等于 `k` 的子数组的数量。

**示例 1**  
输入: `nums = [3,2,1,4,5]`, `k = 4`  
输出: `3`  
解释: 中位数等于 `4` 的子数组有 `[4]`、`[4,5]` 和 `[1,4,5]`。

**示例 2**  
输入: `nums = [2,3,1]`, `k = 3`  
输出: `1`  
解释: `[3]` 是唯一一个中位数等于 `3` 的子数组。

**约束条件**  
- `n == nums.length`  
- `1 <= n <= 10^5`  
- `1 <= nums[i], k <= n`  
- `nums` 中的整数互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的办法是枚举所有 **非空子数组**，逐个判断它们的中位数是否等于 `k`。  
具体步骤：

1. 对每个左端点 `left`（0 ≤ left < n）  
   - 对每个右端点 `right`（left ≤ right < n）  
     - 取出子数组 `nums[left : right+1]`  
     - 将子数组排序（因为原数组元素互不相同，排序后中位数的定义很直观）  
     - 计算中位数的位置 `mid = (len(sub) - 1) // 2`（奇数长度取中间，偶数长度取左侧中位数）  
     - 检查 `sorted_sub[mid] == k`，若相等计数 +1  

> **类比**：把每一次枚举子数组想象成在一排书中挑选一段连续的书，然后把这段书重新排好顺序，看看第几本正好是编号为 `k` 的书。  

这个方法一定能得到正确答案，因为我们把所有可能的子数组都检查了一遍。

#### 代码（Python）

```python
from typing import List

def countSubarrays_bruteforce(nums: List[int], k: int) -> int:
    n = len(nums)
    ans = 0
    for left in range(n):
        for right in range(left, n):
            # 取子数组并排序
            sub = sorted(nums[left:right + 1])
            # 中位数下标（左侧中位数）
            mid = (len(sub) - 1) // 2
            if sub[mid] == k:
                ans += 1
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n³)`  
  - 外层两个循环各 `O(n)`，内部的 `sorted` 需要 `O(m log m)`（`m` 为子数组长度，最坏 `O(n log n)`），整体约为 `O(n³)`。  
  - **大白话**：如果数组长度是 1000，暴力解大概要做 1000 × 1000 × log 1000 ≈ 10⁹ 次操作，明显会超时。  

- **空间复杂度**：`O(n)`（排序时临时的子数组）  

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**频繁排序**和**重复遍历子数组**。我们需要找一种方式，**一次遍历就能统计所有满足条件的子数组**。

下面一步步推导优化思路：

1. **把数组映射成只有 -1、0、1 三种值**  
   - 对于每个元素 `x`  
     - 若 `x > k`，记为 `1`（相当于“比 k 大”）  
     - 若 `x < k`，记为 `-1`（相当于“比 k 小”）  
     - 若 `x == k`，记为 `0`（就是我们要的中位数）  

   > **类比**：把每本书分成三类：比 `k` 大的标记为 “+”，比 `k` 小的标记为 “-”，正好是 `k` 的标记为 “0”。  

2. **观察子数组的性质**  
   - 对于一个子数组如果它的 **中位数是 k**，那么在上述映射后，这个子数组里 **+1 与 -1 的数量差** 必须是 `0` 或 `1`（因为中位数左侧的元素不多于右侧）。  
   - 换句话说，子数组的 **前缀和**（把映射后的数累加）在包含 `k` 的位置左侧和右侧的差值只能是 `0` 或 `1`。  

3. **使用前缀和 + 哈希表计数**  
   - 设 `pref[i]` 为前 i 个元素（映射后）的累计和，`pref[0] = 0`。  
   - 找到 `k` 在原数组中的下标 `pos`。  
   - 把 **左侧**（包括 `pos`）的前缀和统计到哈希表 `cnt` 中：遍历 `i` 从 `pos` 往左走，记录 `pref[i]` 出现的次数。  
   - 再遍历 **右侧**（从 `pos` 往右走），对于每个右端点 `j`，我们需要找左侧的前缀和 `pref[i]` 使得 `pref[j] - pref[i]` 为 `0` 或 `1`，即 `pref[i] = pref[j]` 或 `pref[i] = pref[j] - 1`。  
   - 哈希表直接给出满足条件的左端点数量，累加即为答案。  

4. **为什么只需要统计一次左侧**  
   - 前缀和是从数组左端点累加的，左侧的所有可能 `pref[i]` 已经被记录。右侧遍历时，每次只看当前的 `pref[j]`，配合哈希表即可得到所有以 `k` 为中位数且右端点为 `j` 的子数组数目。  

> **关键概念解释**  
> - **前缀和**：把数组的累计和想象成跑步的里程表，`pref[i]` 表示跑到第 i 步时总共走了多少“正负步”。  
> - **哈希表**：像一本“查字典”，键是前缀和的值，值是出现的次数。我们可以在 O(1) 时间内问：“这个里程表出现过几次？”  

#### 代码（Python）

```python
from typing import List
from collections import defaultdict

def countSubarrays(nums: List[int], k: int) -> int:
    n = len(nums)
    # 1. 找到 k 的位置
    pos = nums.index(k)

    # 2. 把原数组映射为 -1 / 0 / 1
    #    大于 k -> 1, 小于 k -> -1, 等于 k -> 0
    mapped = []
    for x in nums:
        if x > k:
            mapped.append(1)
        elif x < k:
            mapped.append(-1)
        else:
            mapped.append(0)

    # 3. 统计左侧（包括 pos）所有前缀和出现的次数
    cnt = defaultdict(int)      # 哈希表：前缀和 -> 出现次数
    pref = 0                     # 当前前缀和
    cnt[0] = 1                   # 空前缀（左端点就在 pos 左边）算一次
    for i in range(pos - 1, -1, -1):   # 向左遍历
        pref += mapped[i]               # 累加 -1 / 1（pos 本身是 0，不影响）
        cnt[pref] += 1                  # 记录出现次数

    # 4. 向右遍历，统计满足条件的子数组
    ans = 0
    pref = 0                 # 重新从 pos 开始计算右侧前缀和
    for j in range(pos, n):
        pref += mapped[j]                # 包含 pos 本身的 0
        # 需要左侧前缀和使得差值为 0 或 1
        ans += cnt.get(pref, 0)          # diff == 0
        ans += cnt.get(pref - 1, 0)      # diff == 1

    return ans
```

> **代码要点**  
> - 第 2 步的映射把问题转化为“正负步数平衡”。  
> - `cnt[0] = 1` 表示在 `pos` 左边没有取任何元素时的前缀和为 0，也是一种合法的左端点。  
> - 遍历右侧时 `pref` 包含了从 `pos` 到当前 `j` 的所有映射值（`0` 本身不改变和），于是只要在哈希表中找 `pref` 或 `pref-1` 的出现次数即可。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历数组两遍（一次左侧统计，一次右侧查询），每一步的哈希表操作都是 `O(1)`。  
  - **对比**：从原来的 `O(n³)` 降到了线性时间，几乎可以处理 10⁵ 规模的输入。  

- **空间复杂度**：`O(n)`（哈希表最多保存左侧所有不同的前缀和）  
  - 前缀和的取值范围在 `[-n, n]`，所以最坏情况下哈希表会有 `2n+1` 条记录，仍然是线性空间。  

---

## 心得

- **核心技巧**：把「中位数为 k」转化为「映射后子数组的前缀和差为 0 或 1」，进而利用前缀和 + 哈希表一次遍历计数。  
- **适用的题型**  
  1. **子数组和等于目标值**（LeetCode 560）  
  2. **子数组中正负数平衡**（如「子数组中 0 与 1 数量相同」）  
  3. **带有「中位数」或「多数元素」的统计问题**（如「子数组的中位数 ≥ k」）  

- **一句话总结**：把「中位数」的问题映射成「前缀和差」的约束，用哈希表统计前缀和出现次数，即可线性时间求解。

---

## 反思

- **第一反应**：看到「中位数」就想到「排序」和「枚举」，于是写出了暴力解。  
- **最容易踩的坑**  
  - 忘记子数组必须 **包含元素 k**，导致计数多了。  
  - 处理偶数长度时对「左侧中位数」的定义不清晰，可能产生偏差。  
  - 前缀和的起始值与哈希表的初始化（`cnt[0]=1`）容易遗漏。  

- **下次遇到同类题**：第一步先**把数值映射成符号（-1/0/1）**，思考**在映射后有什么简单的数学性质**（如前缀和差），再利用**哈希表**或**双指针**等线性结构快速计数。