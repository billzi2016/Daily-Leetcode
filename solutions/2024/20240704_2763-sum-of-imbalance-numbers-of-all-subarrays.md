# #2763. 所有子数组的不平衡数之和 / Sum of Imbalance Numbers of All Subarrays

> 难度：困难 · 标签：Array、Hash Table、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/sum-of-imbalance-numbers-of-all-subarrays/)

---

## 题目（英文原版）

**Description**

The imbalance number of a 0-indexed integer array arr of length n is defined as the number of indices in sarr = sorted(arr) such that:
Here, sorted(arr) is the function that returns the sorted version of arr.
Given a 0-indexed integer array nums, return the sum of imbalance numbers of all its subarrays.
A subarray is a contiguous non-empty sequence of elements within an array.

**Examples**

**Example 1:**

```
Input: nums = [2,3,1,4]
Output: 3
Explanation: There are 3 subarrays with non-zero imbalance numbers:
- Subarray [3, 1] with an imbalance number of 1.
- Subarray [3, 1, 4] with an imbalance number of 1.
- Subarray [1, 4] with an imbalance number of 1.
The imbalance number of all other subarrays is 0. Hence, the sum of imbalance numbers of all the subarrays of nums is 3.
```

**Example 2:**

```
Input: nums = [1,3,3,3,5]
Output: 8
Explanation: There are 7 subarrays with non-zero imbalance numbers:
- Subarray [1, 3] with an imbalance number of 1.
- Subarray [1, 3, 3] with an imbalance number of 1.
- Subarray [1, 3, 3, 3] with an imbalance number of 1.
- Subarray [1, 3, 3, 3, 5] with an imbalance number of 2. 
- Subarray [3, 3, 3, 5] with an imbalance number of 1. 
- Subarray [3, 3, 5] with an imbalance number of 1.
- Subarray [3, 5] with an imbalance number of 1.
The imbalance number of all other subarrays is 0. Hence, the sum of imbalance numbers of all the subarrays of nums is 8.
```

**Constraints**

- 1 <= nums.length <= 1000
- 1 <= nums[i] <= nums.length

---

## 题目（中文翻译）

**题目描述**  
给定一个下标从 0 开始、长度为 n 的整数数组 `arr`，先将其排序得到 `sarr = sorted(arr)`（`sorted` 为返回数组升序排列后的函数）。`arr` 的 **不平衡数** 定义为满足  

```
sarr[i+1] - sarr[i] > 1
```  

的索引 `i` 的个数。  

现在给定一个下标从 0 开始的整数数组 `nums`，请返回其所有 **子数组**（连续且非空的元素序列）的不平衡数之和。  

**示例**  

*示例 1*  
输入：`nums = [2,3,1,4]`  
输出：`3`  
解释：有 3 个子数组的不平衡数不为 0：
- 子数组 `[3, 1]` 的不平衡数为 1。  
- 子数组 `[3, 1, 4]` 的不平衡数为 1。  
- 子数组 `[1, 4]` 的不平衡数为 1。  

其余子数组的不平衡数均为 0。因此所有子数组的不平衡数之和为 3。

*示例 2*  
输入：`nums = [1,3,3,3,5]`  
输出：`8`  
解释：共有 7 个子数组的不平衡数不为 0：
- 子数组 `[1, 3]` 的不平衡数为 1。  
- 子数组 `[1, 3, 3]` 的不平衡数为 1。  
- 子数组 `[1, 3, 3, 3]` 的不平衡数为 1。  
- 子数组 `[1, 3, 3, 3, 5]` 的不平衡数为 2。  
- 子数组 `[3, 3, 3, 5]` 的不平衡数为 1。  
- 子数组 `[3, 3, 5]` 的不平衡数为 1。  
- 子数组 `[3, 5]` 的不平衡数为 1。  

其余子数组的不平衡数为 0，所有子数组的不平衡数之和为 8。

**约束条件**  
- `1 <= nums.length <= 1000`  
- `1 <= nums[i] <= nums.length`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每一个子数组都枚举出来，单独求它的 “imbalance number”，最后把所有结果加起来**。  
- **子数组枚举**：双层循环 `left`、`right`，`left ≤ right`，把 `nums[left … right]` 取出来。  
- **求 imbalance**：先把子数组复制一份并排序（`sorted(sub)`），得到有序数组 `s`。  
  - `imbalance` 定义为：在 `s` 中，**相邻两个数之间的差大于 1** 的次数。  
  - 可以把它想象成 **字典**：每个不同的数字对应一本书的页码，若相邻两本书的页码相差超过 1，就算一次“不相邻”。  
- **把所有子数组的 imbalance 加总**，得到答案。

> **为什么这样一定对？**  
> 因为题目对每个子数组的定义已经给出，只要我们完整遍历、完整排序、完整计数，就一定得到准确的数值。  

#### 代码（Python）

```python
from typing import List

def sumImbalanceNumbers(nums: List[int]) -> int:
    n = len(nums)
    ans = 0

    # 枚举左端点
    for left in range(n):
        # 枚举右端点
        for right in range(left, n):
            # 取出子数组并排序
            sub = sorted(nums[left:right + 1])          # O(k log k) ，k = right-left+1

            # 统计相邻差大于 1 的次数
            imbalance = 0
            for i in range(1, len(sub)):
                if sub[i] - sub[i - 1] > 1:              # 不相邻 → 计数
                    imbalance += 1

            ans += imbalance

    return ans
```

> **关键行中文注释**  
> - `sorted(nums[left:right + 1])`：把当前子数组排好序，类似把词典里的词按照字母顺序排列。  
> - `if sub[i] - sub[i - 1] > 1`：判断相邻两页码之间是否“跳了”一个以上的页码。

#### 复杂度  

- **时间复杂度**：  
  - 子数组的数量是 `n·(n+1)/2 ≈ O(n²)`。  
  - 对每个子数组我们要 **排序**，排序的代价是 `O(k log k)`（`k` 为子数组长度），最坏情况下 `k≈n`。  
  - 所以总体是 `O(n³ log n)`，在最坏情况下相当于 **立方级** 的运算。  
  - **大白话**：如果 `n=1000`，会进行大约 `10⁹` 次比较，远远超过 1 秒的时间限制。

- **空间复杂度**：  
  - 只用了常数级别的额外变量和一个临时的子数组（最多 `O(n)`），所以是 **O(n)**。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每次都要重新排序**。我们可以 **增量维护** 已经出现的数，并在加入新数时快速更新 `imbalance`，这样就不必再对每个子数组重新排序。

> **核心观察**  
> 对一个子数组，`imbalance` 等价于 **不同数之间的“间隙数”**。  
> - 把子数组里出现的 **不同的数字** 按大小排成一列。  
> - 只要相邻两个不同数字的差大于 1，就算一次间隙。  
> - 因此，只要知道 **哪些数字出现了**，以及它们在数轴上的相对位置，就能算出 `imbalance`。

> **增量更新规则**（把新数字 `x` 加入当前子数组）  
> 设已经出现的不同数字集合为 `S`（有序），`gap` 为当前的间隙数。  
> 1. **如果 `x` 已经在 `S` 中** → `S`、`gap` 不变（重复数字不产生新间隙）。  
> 2. **否则**，找出 `x` 在有序集合中的左右邻居：`prev`（≤`x`的最大）和 `next`（≥`x`的最小）。  
>    - **情况 A**：`prev` 与 `next` 都不存在（`S` 为空） → `gap` 仍为 0。  
>    - **情况 B**：只有一个邻居存在（`x` 成为最小或最大） →  
>        - 若该邻居与 `x` 的差大于 1，则 **新增 1 条间隙**。  
>        - 否则（差等于 1），间隙不变。  
>    - **情况 C**：左右邻居都存在 →  
>        - 若 `prev` 与 `next` 之间本来是间隙（`next - prev > 1`），而 `x` 插入后把它 **拆开**，间隙数 **-1**。  
>        - 再检查 `x` 与 `prev`、`x` 与 `next` 的差：如果 `x - prev > 1` 再 **+1**，如果 `next - x > 1` 再 **+1**。  
>        - 简单来说：**插入一个新数会把原来的间隙拆成最多两个新间隙**。

> **数据结构**  
> - **有序集合**：在 Python 中可以用 `bisect` 在一个 **有序列表** 中二分查找插入位置，实现类似 “TreeSet” 的功能。  
> - **集合 `seen`**：快速判断一个数是否已经出现（`O(1)`），相当于 “字典里查词”。  

> **整体算法**  
> 1. 固定左端点 `left`，清空 `ordered = []`（有序列表）和 `seen = set()`，`gap = 0`。  
> 2. 右端点从 `left` 向右移动，逐个把 `nums[right]` 加入集合，按照上面的增量规则更新 `gap`。  
> 3. 当前子数组的 `imbalance` 就是 `gap`，累加到答案中。  
> 4. 重复 `left` 的所有可能，时间复杂度是 `O(n² log n)`（每次插入要二分定位 `log n`），空间 `O(n)`。

> **为什么比暴力快**  
> - 只做一次排序（维护有序列表），不必对每个子数组重新排序。  
> - 每次扩展子数组只做 **常数次** 的比较和一次二分插入，极大降低了时间。

#### 代码（Python）

```python
from bisect import bisect_left, insort
from typing import List

def sumImbalanceNumbers(nums: List[int]) -> int:
    n = len(nums)
    ans = 0

    # 固定左端点
    for left in range(n):
        ordered = []          # 有序的不同数字列表（类似 TreeSet）
        seen = set()          # 记录出现过的数字，避免重复插入
        gap = 0               # 当前子数组的 imbalance

        # 右端点逐步向右扩展
        for right in range(left, n):
            x = nums[right]

            # 若已经出现，gap 不变，直接累加答案
            if x in seen:
                ans += gap
                continue

            # 找到 x 在有序列表中的插入位置
            pos = bisect_left(ordered, x)   # O(log len(ordered))

            # 取左右邻居（若不存在，用 None 表示）
            prev = ordered[pos - 1] if pos > 0 else None
            nxt  = ordered[pos]     if pos < len(ordered) else None

            # ---------- 根据邻居情况增量更新 gap ----------
            if prev is None and nxt is None:
                # 第一个元素，gap 仍为 0
                pass
            elif prev is None:  # 只存在右邻居，x 成为最小值
                if nxt - x > 1:     # 与右邻居不相邻 → 新增 1 条间隙
                    gap += 1
            elif nxt is None:   # 只存在左邻居，x 成为最大值
                if x - prev > 1:     # 与左邻居不相邻 → 新增 1 条间隙
                    gap += 1
            else:
                # 左右邻居都存在，先看原来的间隙是否被拆掉
                if nxt - prev > 1:   # 原本 prev 与 nxt 之间是间隙
                    gap -= 1         # 插入 x 后把它拆掉
                # 再看 x 与左右邻居的新间隙
                if x - prev > 1:
                    gap += 1
                if nxt - x > 1:
                    gap += 1
            # ---------------------------------------------------

            # 把 x 插入有序列表，并标记已出现
            insort(ordered, x)   # O(log len(ordered))
            seen.add(x)

            # 当前子数组的 imbalance 累加到答案
            ans += gap

    return ans
```

> **关键行中文注释**  
> - `bisect_left`：在已经排好序的列表里 **二分查找** 插入位置，时间像找字典里的页码一样快（`log n`）。  
> - `insort`：把新数插入到有序列表中，保持顺序不变。  
> - `prev`、`nxt`：分别是 **左邻居**（比 `x` 小的最大数）和 **右邻居**（比 `x` 大的最小数），帮助判断“相邻”还是“间隙”。  
> - `gap` 的增减逻辑：严格按照前面的 “增量更新规则” 实现。

#### 复杂度  

- **时间复杂度**：`O(n² log n)`  
  - 外层两层循环产生 `O(n²)` 个子数组。  
  - 每次向右扩展只做一次二分定位和一次插入，都是 `O(log n)`。  
  - 与暴力的 `O(n³ log n)` 相比，**把一个 `n` 级别的循环省掉**，在 `n ≤ 1000` 时运行毫秒级。

- **空间复杂度**：`O(n)`  
  - `ordered`、`seen` 最多保存当前左端点右侧的所有不同数字，最多 `n` 个。  

---

## 心得  

- **核心技巧**：**增量维护有序集合并通过相邻关系计算间隙**（即 imbalance）。  
- **适用的题型**：  
  1. “子数组/子序列的 **gap / 不相邻** 计数”——如 *Sum of Subarray Ranges*、*Number of Subarrays with Bounded Maximum*。  
  2. “需要在滑动窗口中快速获取 **前驱/后继**” 的问题——如 *Sliding Window Median*、*Longest Subarray with Absolute Diff ≤ limit*。  
- **一句话总结解题钥匙**：**把“重新排序”换成“增量插入并维护相邻关系”，让每次扩展只用常数或对数时间**。

---

## 反思  

- **第一反应**：看到 “imbalance number = 相邻差大于 1 的次数”，马上想到 **先排序再遍历**，于是写出了暴力解。  
- **最容易踩的坑**：  
  - **重复数字**：若不先判断是否已经出现，会把同一个数字多次计入集合，导致错误的间隙增减。  
  - **左/右邻居为空**：边界情况（子数组只有一个元素或插入成为最小/最大）需要单独处理，否则会出现 `IndexError`。  
  - **间隙的增减**：在左右邻居都存在时，忘记先把原来的间隙减掉，会把间隙数算得太大。  
- **下次遇到同类题**：第一步先 **思考如何在窗口扩展/收缩时维护“有序唯一集合”**，并 **利用前驱/后继的差值** 来更新答案，而不是每次重新排序。这样往往能把指数级/立方级的暴力直接降到二次或二次对数级。