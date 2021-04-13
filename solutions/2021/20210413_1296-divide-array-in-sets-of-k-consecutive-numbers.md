# #1296. **将数组划分为 K 个连续数字的集合** / Divide Array in Sets of K Consecutive Numbers

> 难度：中等 · 标签：Array、Hash Table、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/divide-array-in-sets-of-k-consecutive-numbers/)

---

## 题目（英文原版）

**Description**

Given an array of integers nums and a positive integer k, check whether it is possible to divide this array into sets of k consecutive numbers.
Return true if it is possible. Otherwise, return false.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,3,4,4,5,6], k = 4
Output: true
Explanation: Array can be divided into [1,2,3,4] and [3,4,5,6].
```

**Example 2:**

```
Input: nums = [3,2,1,2,3,4,3,4,5,9,10,11], k = 3
Output: true
Explanation: Array can be divided into [1,2,3] , [2,3,4] , [3,4,5] and [9,10,11].
```

**Example 3:**

```
Input: nums = [1,2,3,4], k = 3
Output: false
Explanation: Each array should be divided in subarrays of size 3.
```

**Constraints**

- 1 <= k <= nums.length <= 105
- 1 <= nums[i] <= 109

---

## 题目（中文翻译）

给定一个整数数组（array）`nums` 和一个正整数 `k`，判断是否可以将该数组划分为若干个大小为 `k` 的连续数字（consecutive numbers）集合。  
如果可以，返回 `true`；否则返回 `false`。

**示例 1**  
**示例 2**  
**示例 3**  

**示例**

**示例 1**  
输入: `nums = [1,2,3,3,4,4,5,6]`, `k = 4`  
输出: `true`  
解释: 数组可以划分为 `[1,2,3,4]` 和 `[3,4,5,6]`。

**示例 2**  
输入: `nums = [3,2,1,2,3,4,3,4,5,9,10,11]`, `k = 3`  
输出: `true`  
解释: 数组可以划分为 `[1,2,3]`, `[2,3,4]`, `[3,4,5]` 和 `[9,10,11]`。

**示例 3**  
输入: `nums = [1,2,3,4]`, `k = 3`  
输出: `false`  
解释: 每个子数组（subarray）的大小都必须为 3。

**约束条件**

- `1 <= k <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **“把所有可能的划分全部枚举一遍”**，只要找到一种划分使得每组恰好包含 `k` 个连续整数，就返回 `True`，否则返回 `False`。  
实现上可以采用 **回溯（Backtracking）**：

1. 先把数组 `nums` 排序，方便后面判断“连续”。  
2. 用一个布尔数组 `used` 标记哪些位置的元素已经被放进了某个子集。  
3. 从左到右遍历，找到第一个未被使用的最小元素 `v`，尝试把 `v, v+1, … , v+k-1` 这 `k` 个数全部取出来（如果有缺失就回溯）。  
4. 重复步骤 3，直到所有元素都被使用（成功）或所有尝试都失败（不可能）。

> **类比**：把每个数字想象成书架上的一本书，`used` 就是“这本书已经被借走了吗”。我们一次尝试挑走 `k` 本连续编号的书，若找不到完整的一套，就把已经挑走的书放回去再尝试别的组合——这就是回溯的过程。

**为什么这个方法正确**  
回溯会尝试 *所有* 可能的分组方式，只要存在一种合法划分，就一定会在搜索树的某个分支上找到并返回 `True`。因此它的正确性由“穷举所有可能”保证。

**时间/空间复杂度**  
- 最坏情况下，`nums` 长度为 `n`，我们需要在每一步尝试把 `k` 个数挑出来，回溯树的分支数大约是 `(n/k)!`（每一次都要决定下一组的起始位置），所以 **时间复杂度是指数级**，记作 `O( (n/k)! )`。  
- 额外使用的 `used` 数组占 `O(n)` 空间，递归栈深度最多 `n/k`，同样是 `O(n)`。

> **大白话**：指数级就像“每增加一个元素，可能的组合数就像翻倍一样快速增长”，即使 `n` 只有 20，执行时间也可能已经不可接受。

#### 代码（Python）

```python
from collections import Counter
from typing import List

def canDivide_bruteforce(nums: List[int], k: int) -> bool:
    # 1. 长度必须能被 k 整除，否则一定不行
    if len(nums) % k != 0:
        return False

    # 2. 排序后更容易判断连续性
    nums.sort()
    n = len(nums)
    used = [False] * n          # 标记是否已经被放进某个子集

    def backtrack(start: int, groups_left: int) -> bool:
        """尝试从位置 start 开始，完成剩余 groups_left 组的划分"""
        if groups_left == 0:    # 所有组都已经成功划分
            return True

        # 找到下一个未使用的最小元素的下标
        i = start
        while i < n and used[i]:
            i += 1
        if i == n:              # 已经遍历完仍有组未完成，说明失败
            return False

        # 以 nums[i] 为起点尝试构造一组连续的 k 个数
        v = nums[i]
        temp = []               # 暂存本次挑选的下标，方便回溯时恢复
        for offset in range(k):
            target = v + offset
            # 在剩余未使用的元素中寻找 target
            j = i
            while j < n:
                if not used[j] and nums[j] == target:
                    used[j] = True
                    temp.append(j)
                    break
                j += 1
            else:                # 没找到 target，回溯
                for idx in temp:
                    used[idx] = False
                return False

        # 成功挑出一组，递归处理剩余的组
        if backtrack(i + 1, groups_left - 1):
            return True

        # 递归失败，恢复本次挑选的状态，继续尝试其它可能（这里其实已经穷举完了）
        for idx in temp:
            used[idx] = False
        return False

    total_groups = len(nums) // k
    return backtrack(0, total_groups)
```

#### 复杂度

- **时间复杂度**：`O( (n/k)! )`（指数级），因为需要遍历所有可能的分组方式。  
- **空间复杂度**：`O(n)`，主要是 `used` 数组和递归栈的开销。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **大量的重复搜索**：每次我们都要从头遍历未使用的元素来找连续的 `k` 个数。实际上，**只要从最小的数开始，按照升序一次性把它们“配对”**，就能一次完成全部划分，根本不需要回溯。

关键观察（题目提示）：

- 若数组能够成功划分，那么 **最小的数** 必须是某一组的起点。于是它的后面必须恰好出现 `V+1, V+2, …, V+k-1`，每个数的出现次数必须足够支撑所有以 `V` 为起点的组数。
- 这意味着我们可以 **从小到大遍历**，把每个数的出现次数记下来（哈希表），然后对每个出现的最小数 `v`，**一次性创建 `cnt[v]` 组**，并把 `v+1 … v+k-1` 的计数都减去 `cnt[v]`。如果在此过程中出现负数，说明缺少必要的连续元素，直接返回 `False`。

实现细节：

1. **计数**：使用 `collections.Counter`（相当于“查字典”，key 是数字，value 是出现次数）。  
2. **排序**：把所有出现的不同数字取出来并排序，这样可以保证我们总是先处理最小的数。  
3. **贪心配对**：遍历排序后的数字 `v`，若 `cnt[v] > 0`，说明还有 `cnt[v]` 组需要以 `v` 为起点。于是对 `i = 0 … k-1`，把 `cnt[v+i]` 减去 `cnt[v]`。如果 `v+i` 在字典中不存在或减到负数，说明无法形成完整的连续组，返回 `False`。  
4. 所有数字遍历完毕且没有出现负数，说明每个数都被恰好分配到了某个组，返回 `True`。

> **类比**：把每个数字想象成“仓库里的一种零件”，`cnt` 记录每种零件的库存。我们要把零件按照顺序组装成若干套机器，每套机器恰好需要 `k` 种连续编号的零件。我们从最少库存的最小编号零件开始，决定要生产多少套机器（`cnt[v]`），然后一次性扣除后面 `k-1` 种零件的库存。只要库存永不为负，就能完成全部装配。

#### 代码（Python）

```python
from collections import Counter
from typing import List

def canDivide(nums: List[int], k: int) -> bool:
    """
    贪心 + 哈希表
    1. 统计每个数字出现的次数（相当于查字典）
    2. 按数字从小到大遍历
    3. 对每个仍有剩余次数的数字 v，创建 cnt[v] 组，以 v 为起点的连续 k 个数
       并把它们的计数都减去 cnt[v]
    4. 只要在此过程中出现负数，就说明缺少必要的连续数字，返回 False
    """
    n = len(nums)
    if n % k != 0:          # 长度必须能被 k 整除
        return False

    cnt = Counter(nums)    # 统计出现次数，类似“查字典”
    # 取出所有出现过的不同数字并排序，保证从最小的数开始处理
    sorted_keys = sorted(cnt.keys())

    for v in sorted_keys:
        if cnt[v] == 0:     # 该数字已经全部配完，直接跳过
            continue
        need = cnt[v]       # 需要以 v 为起点的组数
        # 检查 v, v+1, ..., v+k-1 是否都有足够的数量
        for i in range(k):
            cur = v + i
            if cnt[cur] < need:   # 不足，无法完成连续组
                return False
            cnt[cur] -= need      # 扣除已使用的数量
    return True
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 统计次数是 `O(n)`。  
  - 对不同数字进行排序需要 `O(m log m)`，其中 `m` 是不同数字的数量，`m ≤ n`，所以整体是 `O(n log n)`。  
  - 主循环里每个数字最多遍历一次内部的 `k` 步，累计也是 `O(n)`（因为每次扣除的元素总数等于数组长度）。  
  - 与暴力的指数级搜索相比，这已经是线性或线性对数级的高效算法。

- **空间复杂度**：`O(m)`（即 `O(n)`）  
  - `Counter` 保存每个不同数字的计数，需要额外的哈希表空间。  
  - 其余变量都是常数级别。

> 与暴力解对比：时间从“指数级”降到“几乎线性”，空间仍保持在 `O(n)`，但常数更小，实际可以轻松处理 `10⁵` 规模的输入。

---

## 心得

- **核心技巧**：**贪心 + 哈希计数**。从最小的数开始，确定它必须是某些连续组的起点，随后一次性扣除后面 `k‑1` 个数的计数。  
- **适用的题型**  
  1. “把数组分成若干连续子集”——如 *Divide Array in Sets of K Consecutive Numbers*（本题）。  
  2. “判断能否把手牌组成顺子”——如 *Hand of Straights*（LeetCode 846）。  
  3. “把数列拆分成等差子序列”——如 *Split Array into Consecutive Subarrays*（变形）。  
- **一句话总结解题钥匙**：**“总是先处理最小的未完成数字，它决定了后面的配对方式”。**

---

## 反思

- **第一反应**：看到“连续”“k 个一组”，立刻想到要 **先排序**，再 **从最小元素开始配对**。  
- **最容易踩的坑**  
  - 忘记先检查 `len(nums) % k == 0`，导致不必要的计算。  
  - 只检查 `v, v+1, …, v+k-1` 是否在数组里，而没有考虑它们的出现次数（比如出现次数不够会导致负数）。  
  - 在实现时对 `cnt[cur]` 直接 `+=` 或 `-=` 时忘记先判断键是否存在，导致 `KeyError`。  
- **下次遇到同类题的第一步**：**统计每个数字出现次数并排序**，然后以最小未配完的数字为起点，尝试一次性“扣除”一整组的计数——这一步往往就能判断题目是否可解。