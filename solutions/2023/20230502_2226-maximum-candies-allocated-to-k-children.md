# #2226. **分配给 K 个孩子的最大糖果数** / Maximum Candies Allocated to K Children

> 难度：中等 · 标签：Array、Binary Search · [LeetCode 链接](https://leetcode.com/problems/maximum-candies-allocated-to-k-children/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array candies. Each element in the array denotes a pile of candies of size candies[i]. You can divide each pile into any number of sub piles, but you cannot merge two piles together.
You are also given an integer k. You should allocate piles of candies to k children such that each child gets the same number of candies. Each child can be allocated candies from only one pile of candies and some piles of candies may go unused.
Return the maximum number of candies each child can get.

**Examples**

**Example 1:**

```
Input: candies = [5,8,6], k = 3
Output: 5
Explanation: We can divide candies[1] into 2 piles of size 5 and 3, and candies[2] into 2 piles of size 5 and 1. We now have five piles of candies of sizes 5, 5, 3, 5, and 1. We can allocate the 3 piles of size 5 to 3 children. It can be proven that each child cannot receive more than 5 candies.
```

**Example 2:**

```
Input: candies = [2,5], k = 11
Output: 0
Explanation: There are 11 children but only 7 candies in total, so it is impossible to ensure each child receives at least one candy. Thus, each child gets no candy and the answer is 0.
```

**Constraints**

- 1 <= candies.length <= 105
- 1 <= candies[i] <= 107
- 1 <= k <= 1012

---

## 题目（中文翻译）

给定一个下标从 0 开始的整数数组 `candies`。数组中的每个元素表示一堆糖果，大小为 `candies[i]`。你可以将每堆糖果拆分成任意数量的子堆（sub piles），但不能将两堆糖果合并在一起。

同时给定一个整数 `k`，要求把糖果堆分配给 `k` 个孩子，使得每个孩子得到的糖果数量相同。每个孩子只能从 **一堆** 糖果中获得糖果，且部分糖果堆可以不被使用。

返回每个孩子能够得到的最大糖果数量。

---

### 示例

#### 示例 1
**输入**  
`candies = [5,8,6]`, `k = 3`

**输出**  
`5`

**解释**  
我们可以把 `candies[1]` 拆成大小为 5 和 3 的两堆，把 `candies[2]` 拆成大小为 5 和 1 的两堆。此时得到的糖果堆大小为 5、5、3、5、1。可以把三堆大小为 5 的糖果分别分配给 3 个孩子。可以证明，任何分配方案中每个孩子得到的糖果数都不可能超过 5。

#### 示例 2
**输入**  
`candies = [2,5]`, `k = 11`

**输出**  
`0`

**解释**  
共有 11 个孩子，但糖果总数只有 7 颗，无法保证每个孩子至少得到一颗糖果。因此每个孩子都得不到糖果，答案为 0。

---

### 约束条件

- `1 <= candies.length <= 10^5`
- `1 <= candies[i] <= 10^7`
- `1 <= k <= 10^12`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把可能的每一种糖果数量都枚举一遍**，看看能不能满足 `k` 个小朋友。  
具体步骤：

1. 先找到所有糖果堆里最大的那堆 `max_candy`，因为每个小朋友不可能得到超过它的糖果数。  
2. 从 `1` 到 `max_candy`（甚至可以从 `0` 开始）逐个尝试每个候选值 `c`（每个孩子要拿的糖果数）。  
3. 对于某个固定的 `c`，遍历所有堆，计算这堆能切出多少个大小为 `c` 的小堆：`candies[i] // c`（整数除法）。把所有堆得到的小堆数相加，记为 `total`。  
4. 如果 `total >= k`，说明 **至少** 能给 `k` 个孩子每人 `c` 颗糖；否则 `c` 太大，不能满足需求。  
5. 把所有满足条件的 `c` 记录下来，最后取最大的那个，就是答案。

> **类比**：把每堆糖果想象成一本厚厚的词典，`c` 相当于“每页要容纳的单词数”。我们想知道在给定的页数（`c`）下，所有词典一共能装出多少页（`total`），看能不能满足读者（`k`）的需求。

**为什么正确**  
因为我们枚举了 **所有** 可能的每人糖果数，只要有一种切法能让 `k` 个孩子得到 `c` 颗糖，就会被记录。取最大值自然就是答案。

#### 代码（Python）

```python
def maximumCandies_bruteforce(candies, k):
    """
    暴力枚举每一种可能的每个孩子得到的糖果数
    :param candies: List[int] 每堆糖果的数量
    :param k: int 需要分配的孩子数量
    :return: int 最大的每个孩子可以得到的糖果数
    """
    if not candies:
        return 0

    max_candy = max(candies)                # 最大堆的大小，答案不可能超过它
    best = 0                                 # 当前找到的最大可行答案

    # 从 1 到 max_candy 逐个尝试（0 直接返回 0）
    for c in range(1, max_candy + 1):
        total = 0
        for pile in candies:
            total += pile // c               # 这堆能切出多少个大小为 c 的小堆
        if total >= k:                       # 能满足 k 个孩子吗？
            best = c                         # 记录下来，继续尝试更大的 c
    return best
```

#### 复杂度

- **时间复杂度**：`O(max_candy * n)`  
  - `max_candy` 最坏可达 `10⁷`，`n`（数组长度）最高 `10⁵`，所以在极端情况下会出现 `10¹²` 次循环，远远超出可接受范围。  
  - 用大白话说，就是“把每一颗可能的糖果数都试一遍”，太慢了。

- **空间复杂度**：`O(1)`  
  - 只用了常数级别的额外变量，不随输入规模增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**枚举所有可能的 `c` 是瓶颈**——我们其实只需要找出满足条件的 **最大** `c`，不必一个一个检查。  
观察到：

- 当 `c` **变大** 时，每堆能切出的子堆数 `pile // c` **只会变少**，因此 `total`（所有子堆的总数）是 **单调递减** 的函数。  
- 单调递减的函数非常适合 **二分搜索**（binary search），我们可以在 `[0, max_candy]` 这条数轴上快速定位最大的满足 `total >= k` 的 `c`。

二分搜索的核心步骤：

1. **左边界** `lo = 0`（每个孩子拿 0 颗糖永远可以满足），**右边界** `hi = max(candies)`（不可能超过最大堆的大小）。  
2. 取中点 `mid = (lo + hi + 1) // 2`（上取整是为了防止死循环）。  
3. 用 `mid` 作为每个孩子的目标糖果数，遍历所有堆，计算 `total = sum(pile // mid)`。  
4. 如果 `total >= k`，说明 `mid` 可行，尝试更大的值：`lo = mid`。  
5. 否则 `mid` 太大，缩小范围：`hi = mid - 1`。  
6. 当 `lo == hi` 时，循环结束，`lo`（或 `hi`）就是答案。

> **类比**：把可能的每人糖果数看成一根长度为 `max_candy` 的尺子，我们想在尺子上找最靠右、还能让 `k` 个人站得下的位置。二分搜索就是不断把尺子折半，快速逼近目标。

#### 代码（Python）

```python
def maximumCandies(candies, k):
    """
    二分搜索求解每个孩子可以得到的最大糖果数
    :param candies: List[int] 每堆糖果的数量
    :param k: int 需要分配的孩子数量
    :return: int 最大的每个孩子可以得到的糖果数
    """
    if not candies:
        return 0

    lo, hi = 0, max(candies)          # 搜索区间 [lo, hi]
    
    # 二分搜索：寻找最大的满足条件的 c
    while lo < hi:
        mid = (lo + hi + 1) // 2      # 取上中点，防止死循环
        total = 0
        for pile in candies:
            total += pile // mid      # 这堆能切出多少个大小为 mid 的小堆
        if total >= k:                # mid 可行，尝试更大
            lo = mid
        else:                         # mid 不可行，缩小区间
            hi = mid - 1
    return lo
```

#### 复杂度

- **时间复杂度**：`O(n log M)`  
  - `n` 是数组长度（最多 `10⁵`），`M = max(candies)` 是最大堆的大小（最多 `10⁷`）。  
  - 二分搜索的迭代次数约为 `log₂ M`（大约 24 次），每次遍历全部堆求和，所以总操作数约为 `24 * 10⁵`，在一秒内轻松完成。  
  - 与暴力解相比，从“每个可能的 c 都试一次”降到了“只试 log 次”，快了几个数量级。

- **空间复杂度**：`O(1)`  
  - 只用了常数级的变量 `lo、hi、mid、total`，不随输入规模增长。

---

## 心得

- **核心技巧**：利用单调性 + 二分搜索把“在所有可能答案中找最大可行值”的问题转化为对数时间的搜索。  
- **适用的题型**：  
  1. **分配类**：比如“最大化每个学生的分数”“最大化每台机器的负载”。  
  2. **容量类**：比如“在给定总容量下，最大化每个盒子的装载量”。  
  3. **阈值类**：比如“最小化满足条件的时间”“最大化可接受的速度”。  
- **一句话总结解题钥匙**：**把“能否”转化为单调判定函数，再用二分搜索快速定位极限**。

---

## 反思

- **第一反应**：看到“每个孩子只能从同一堆取糖，且可以把堆拆分”，自然会想到 **“每堆能切出多少份”**，于是想到枚举每个可能的糖果数。  
- **最容易踩的坑**：  
  1. **边界条件**：`k` 可能远大于总糖果数，答案应是 `0`，二分搜索的左边界要设为 `0`。  
  2. **整数除法**：`pile // mid` 必须使用整数除，否则会出现浮点误差。  
  3. **上取中点**：若使用 `(lo+hi)//2` 可能导致在 `lo+1==hi` 时无限循环，记得加 `+1` 或者改写循环条件。  
- **下次遇到同类题**，第一步应该思考：**“把待求的答案当作阈值，能否检查‘是否可行’？”**如果答案的可行性随阈值单调变化，就立刻想到二分搜索。