# #1818. 最小绝对和差 / Minimum Absolute Sum Difference

> 难度：中等 · 标签：Array、Binary Search、Sorting、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/minimum-absolute-sum-difference/)

---

## 题目（英文原版）

**Description**

You are given two positive integer arrays nums1 and nums2, both of length n.
The absolute sum difference of arrays nums1 and nums2 is defined as the sum of |nums1[i] - nums2[i]| for each 0 <= i < n (0-indexed).
You can replace at most one element of nums1 with any other element in nums1 to minimize the absolute sum difference.
Return the minimum absolute sum difference after replacing at most one element in the array nums1. Since the answer may be large, return it modulo 109 + 7.
|x| is defined as:

**Examples**

**Example 1:**

```
Input: nums1 = [1,7,5], nums2 = [2,3,5]
Output: 3
Explanation: There are two possible optimal solutions:
- Replace the second element with the first: [1,7,5] => [1,1,5], or
- Replace the second element with the third: [1,7,5] => [1,5,5].
Both will yield an absolute sum difference of |1-2| + (|1-3| or |5-3|) + |5-5| = 3.
```

**Example 2:**

```
Input: nums1 = [2,4,6,8,10], nums2 = [2,4,6,8,10]
Output: 0
Explanation: nums1 is equal to nums2 so no replacement is needed. This will result in an 
absolute sum difference of 0.
```

**Example 3:**

```
Input: nums1 = [1,10,4,4,2,7], nums2 = [9,3,5,1,7,4]
Output: 20
Explanation: Replace the first element with the second: [1,10,4,4,2,7] => [10,10,4,4,2,7].
This yields an absolute sum difference of |10-9| + |10-3| + |4-5| + |4-1| + |2-7| + |7-4| = 20
```

**Constraints**

- n == nums1.length
- n == nums2.length
- 1 <= n <= 105
- 1 <= nums1[i], nums2[i] <= 105

---

## 题目（中文翻译）

给定两个正整数数组（positive integer arrays）`nums1` 和 `nums2`，两者长度均为 `n`。  
数组 `nums1` 与 `nums2` 的 **绝对和差**（absolute sum difference）定义为所有下标 `0 <= i < n`（0‑索引）处 `|nums1[i] - nums2[i]|` 的总和。  

你可以将 `nums1` 中至多一个元素替换为 `nums1` 中的任意其他元素，以期使绝对和差最小化。  
返回替换至多一次后的最小绝对和差。由于答案可能很大，请返回其对 `10^9 + 7` 取模后的结果。  

`|x|` 的定义为：

**示例 1**  
```
Input: nums1 = [1,7,5], nums2 = [2,3,5]
Output: 3
Explanation: 有两种可能的最优方案：
- 将第二个元素换成第一个元素： [1,7,5] => [1,1,5]；
- 将第二个元素换成第三个元素： [1,7,5] => [1,5,5]。
两者都会得到绝对和差 |1-2| + (|1-3| 或 |5-3|) + |5-5| = 3。
```

**示例 2**  
```
Input: nums1 = [2,4,6,8,10], nums2 = [2,4,6,8,10]
Output: 0
Explanation: nums1 与 nums2 完全相等，无需替换，绝对和差为 0。
```

**示例 3**  
```
Input: nums1 = [1,10,4,4,2,7], nums2 = [9,3,5,1,7,4]
Output: 20
Explanation: 将第一个元素换成第二个元素： [1,10,4,4,2,7] => [10,10,4,4,2,7]。
此时的绝对和差为 |10-9| + |10-3| + |4-5| + |4-1| + |2-7| + |7-4| = 20。
```

**约束条件**  
- `n == nums1.length`  
- `n == nums2.length`  
- `1 <= n <= 10^5`  
- `1 <= nums1[i], nums2[i] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**遍历每一个可能的替换**，看看把 `nums1` 的哪一个元素换成哪一个（可以是 `nums1` 中的任意元素）后，整体的绝对差和最小是多少。

- **数据结构**：我们只需要两个普通的 Python 列表 `nums1`、`nums2`。  
  - 把列表想象成一排排的格子，格子里装的是数字。  
  - “把 `nums1` 的某个格子换成另一个格子里的数” 就像把一本书的章节重新排版。

- **为什么正确**：因为我们枚举了**所有**合法的一次替换（包括“不替换”的情况），所以必然能找到最优解。

- **时间/空间复杂度**：  
  - 对每个位置 `i`（共 `n` 个），我们尝试把 `nums1[i]` 换成 `nums1` 中的每一个元素（也是 `n` 种可能），并重新计算整个数组的差值和。  
  - 这相当于两层循环，时间是 `O(n × n) = O(n²)`。  
  - `O(n²)` 可以想象成：如果 `n = 10⁴`，则需要 1 亿次计算，显然太慢。  
  - 只用了原数组和几个临时变量，空间是 `O(1)`（常数级别）。

#### 代码（Python）

```python
from typing import List

MOD = 10 ** 9 + 7

def minAbsoluteSumDiff_brute(nums1: List[int], nums2: List[int]) -> int:
    n = len(nums1)
    # 计算原始的绝对差和
    base = sum(abs(nums1[i] - nums2[i]) for i in range(n))
    ans = base                         # 最小答案先设为不做任何替换的情况

    # 枚举要替换的下标 i
    for i in range(n):
        # 枚举替换成的候选值 v（可以是 nums1 中的任意一个元素）
        for v in nums1:
            # 计算替换后新的差值和
            cur = base \
                  - abs(nums1[i] - nums2[i])   # 去掉原来 i 位置的贡献
            cur += abs(v - nums2[i])          # 加上用 v 替换后的贡献
            # 其余位置保持不变，直接累加
            cur += sum(abs(nums1[j] - nums2[j]) for j in range(n) if j != i)
            ans = min(ans, cur)

    return ans % MOD
```

> **注意**：上述代码仅作概念演示，实际运行会超时。

#### 复杂度

- **时间复杂度**：`O(n²)` —— 两层循环遍历 `n`² 次，每次都要做常数级的加减运算。  
  - “O(n²)” 可以理解为“时间随 `n` 的平方增长”，`n` 翻倍，时间会变成原来的 4 倍。
- **空间复杂度**：`O(1)` —— 只用了常数个额外变量，不随 `n` 增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于每次都要遍历整个 `nums1` 来找最佳替换值。  
我们需要一种**快速定位**“最接近 `nums2[i]` 的 `nums1` 中的数”的方法。

**关键观察**：

- 对于固定的 `i`，我们只关心 `|v - nums2[i]|` 最小的 `v`（`v` 必须是 `nums1` 中的某个元素）。  
- 如果把 `nums1` 事先排好序，那么在有序数组里查找最接近目标值的元素，只需要 **二分查找**，时间是 `O(log n)`。

**步骤**：

1. **计算原始差值和** `base = Σ|nums1[i] - nums2[i]|`。  
   这一步是必不可少的，因为我们最终的答案是 `base - 最大可能的改进`。

2. **把 `nums1` 复制一份并排序**，记作 `sorted_nums1`。  
   排序相当于把书籍按照章节号从小到大排好，后面查找时就可以快速定位。

3. 对每个位置 `i`：
   - 设目标值 `t = nums2[i]`。  
   - 在 `sorted_nums1` 中 **二分查找** 第一个不小于 `t` 的数（下标 `pos`），以及 `pos-1`（如果存在），这两个数是最接近 `t` 的候选。  
   - 计算如果把 `nums1[i]` 换成这两个候选之一后，**可以减少的差值**：  
     `improvement = |nums1[i] - t| - min(|candidate - t|)`。  
   - 记录所有 `improvement` 中的最大值 `max_gain`。

4. **答案** = `(base - max_gain) % MOD`。  
   如果 `max_gain = 0`，说明不替换也已经是最优。

**为什么对每个 `i` 只需要检查两个候选**：

- 在有序数组里，离目标值最近的元素必然在 **左侧最近的** 或 **右侧最近的** 两个位置。  
- 这就像在数轴上找最近的站点，只可能是左边最近的站或右边最近的站。

**二分查找的原理**（从零解释）：

- 把有序数组分成两半，比较中间元素和目标值的大小，决定继续在左半边还是右半边搜索。  
- 每次排除掉一半元素，最多需要 `log₂ n` 次比较就能定位到目标位置。  
- Python 的 `bisect` 模块已经实现了这种搜索，我们直接使用 `bisect_left`。

#### 代码（Python）

```python
from bisect import bisect_left
from typing import List

MOD = 10 ** 9 + 7

def minAbsoluteSumDiff(nums1: List[int], nums2: List[int]) -> int:
    n = len(nums1)

    # 1. 计算原始的绝对差和
    base = 0
    for a, b in zip(nums1, nums2):
        base += abs(a - b)

    # 2. 排序后的 nums1，供二分查找使用
    sorted_nums1 = sorted(nums1)

    max_gain = 0   # 能够得到的最大改进（即差值的最大减少）

    # 3. 对每一对 (nums1[i], nums2[i])，尝试找最接近 nums2[i] 的替换值
    for i in range(n):
        a, b = nums1[i], nums2[i]
        original = abs(a - b)          # 当前位置原来的贡献

        # 在有序数组里找第一个 >= b 的位置
        pos = bisect_left(sorted_nums1, b)

        # 检查 pos 处（如果存在）和 pos-1 处（如果存在）的两种可能
        # 这两者就是离 b 最近的数
        best = original                # 默认不做替换，改进为 0
        if pos < n:
            # candidate >= b
            cand = sorted_nums1[pos]
            best = min(best, abs(cand - b))
        if pos > 0:
            # candidate < b
            cand = sorted_nums1[pos - 1]
            best = min(best, abs(cand - b))

        # 这一步得到如果把 nums1[i] 换成最优候选后，能够减少的差值
        gain = original - best
        if gain > max_gain:
            max_gain = gain

    # 4. 用最大改进来更新答案，并取模
    ans = (base - max_gain) % MOD
    return ans
```

> **关键行解释**  
> - `sorted_nums1 = sorted(nums1)`：把书籍按编号排好序，后面查找更快。  
> - `pos = bisect_left(sorted_nums1, b)`：二分找第一个不小于 `b` 的位置。  
> - `gain = original - best`：原来的差值减去换成最接近的数后的差值，就是这一次替换能省下的“钱”。  

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 排序 `sorted(nums1)` 需要 `O(n log n)`。  
  - 对每个 `i` 做一次二分查找，`O(log n)`，共 `n` 次，仍是 `O(n log n)`。  
  - 与暴力解的 `O(n²)` 相比，`log n` 只在几千左右（`n ≤ 10⁵` 时 `log₂ n ≈ 17`），速度提升数百倍。

- **空间复杂度**：`O(n)`  
  - 需要额外存放排好序的数组 `sorted_nums1`，占用 `n` 个整数的空间。  
  - 除此之外只用常数级变量。

---

## 心得

- **核心技巧**：**二分查找 + 排序** 用来在数组中快速定位最接近的元素，从而把“遍历所有候选”降到对数时间。  
- **适用的题型**  
  1. **最小化绝对差** 类题目（如 *Minimize Absolute Difference*、*Min Cost to Connect Sticks* 的变形）。  
  2. **一次替换或一次操作** 的优化问题（如 *Maximum Subarray Sum After One Operation*）。  
  3. **需要在已有集合中找最近值** 的场景（如 *Closest Number*、*Find the Smallest Missing Positive* 的变体）。  
- **一句话总结解题钥匙**：  
  > 把“遍历所有可能”换成“在排好序的集合里二分找最近”，一次替换的最佳收益立刻可得。

---

## 反思

- **第一反应**：看到“可以把 `nums1` 中的一个数换成任意另一个数”，自然想到**枚举所有替换**，但很快意识到 `n` 可达 `10⁵`，暴力不可行。  
- **最容易踩的坑**  
  - **遗漏“不替换”的情况**：如果所有替换都让差值变大，答案应为原始差值。  
  - **二分边界**：`pos` 可能等于 `0` 或 `n`，要分别检查 `pos-1` 与 `pos` 是否在合法范围内。  
  - **取模负数**：`base - max_gain` 可能为负数，使用 Python 的 `% MOD` 可自动得到正的模值。  
- **下次遇到同类题**，第一步应该想到：  
  > “我需要在一个已有集合里找最接近某个目标的元素”，于是**先排序再二分**，把线性搜索降到对数时间。