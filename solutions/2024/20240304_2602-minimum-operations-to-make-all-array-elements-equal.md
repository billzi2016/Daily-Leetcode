# #2602. 使所有数组元素相等的最少操作次数 / Minimum Operations to Make All Array Elements Equal

> 难度：中等 · 标签：Array、Binary Search、Sorting、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/minimum-operations-to-make-all-array-elements-equal/)

---

## 题目（英文原版）

**Description**

You are given an array nums consisting of positive integers.
You are also given an integer array queries of size m. For the ith query, you want to make all of the elements of nums equal to queries[i]. You can perform the following operation on the array any number of times:
Return an array answer of size m where answer[i] is the minimum number of operations to make all elements of nums equal to queries[i].
Note that after each query the array is reset to its original state.

**Examples**

**Example 1:**

```
Input: nums = [3,1,6,8], queries = [1,5]
Output: [14,10]
Explanation: For the first query we can do the following operations:
- Decrease nums[0] 2 times, so that nums = [1,1,6,8].
- Decrease nums[2] 5 times, so that nums = [1,1,1,8].
- Decrease nums[3] 7 times, so that nums = [1,1,1,1].
So the total number of operations for the first query is 2 + 5 + 7 = 14.
For the second query we can do the following operations:
- Increase nums[0] 2 times, so that nums = [5,1,6,8].
- Increase nums[1] 4 times, so that nums = [5,5,6,8].
- Decrease nums[2] 1 time, so that nums = [5,5,5,8].
- Decrease nums[3] 3 times, so that nums = [5,5,5,5].
So the total number of operations for the second query is 2 + 4 + 1 + 3 = 10.
```

**Example 2:**

```
Input: nums = [2,9,6,3], queries = [10]
Output: [20]
Explanation: We can increase each value in the array to 10. The total number of operations will be 8 + 1 + 4 + 7 = 20.
```

**Constraints**

- n == nums.length
- m == queries.length
- 1 <= n, m <= 105
- 1 <= nums[i], queries[i] <= 109

---

## 题目（中文翻译）

给定一个由正整数构成的数组 `nums`。  
再给定一个长度为 `m` 的整数数组 `queries`。对于第 `i` 条查询，你需要将 `nums` 中的所有元素都变成 `queries[i]`。  
你可以对数组执行以下操作任意次数：**将任意元素加 1 或减 1**，每执行一次算作一次操作。  

返回一个长度为 `m` 的数组 `answer`，其中 `answer[i]` 为使所有元素等于 `queries[i]` 所需的最小操作次数。  
注意，每次查询结束后数组会恢复到最初的状态。

## 示例

### 示例 1  
**输入**  
```
nums = [3,1,6,8], queries = [1,5]
```
**输出**  
```
[14,10]
```
**解释**  
对第一个查询（目标值为 1）可以按如下方式操作：

- 将 `nums[0]` 减少 2 次，使数组变为 `[1,1,6,8]`。  
- 将 `nums[2]` 减少 5 次，使数组变为 `[1,1,1,8]`。  
- 将 `nums[3]` 减少 7 次，使数组变为 `[1,1,1,1]`。

总操作次数为 `2 + 5 + 7 = 14`。

对第二个查询（目标值为 5）可以得到最少操作次数 `10`（过程省略）。

### 示例 2  
**输入**  
```
nums = [2,9,6,3], queries = [10]
```
**输出**  
```
[20]
```
**解释**  
将数组中的每个元素都增加到 10，所需的操作次数为 `8 + 1 + 4 + 7 = 20`。

## 约束条件
- `n == nums.length`
- `m == queries.length`
- `1 <= n, m <= 10^5`
- `1 <= nums[i], queries[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：对每一个查询 `q`，遍历整个数组 `nums`，把每个元素 `x` 改成 `q` 所需要的操作次数就是 `|x - q|`（增大或减小的步数），把所有这些次数加起来，就是答案。  

- **使用的数据结构**：只需要一个普通的 Python 列表 `nums`，遍历它就行。可以把列表想象成一本“账本”，我们把账本里的每一笔金额 `x` 调整到目标金额 `q`，需要的操作数就是两者的差的绝对值，就像算账本里每笔钱离目标差多少。
- **为什么正确**：题目要求把所有元素都变成同一个数 `q`，每一次增/减只能让一个元素的值改变 1，最终需要的总步数必然是每个元素与 `q` 差值的绝对值之和，所有元素互不影响，所以把每个 `|x-q|` 加起来就得到最小操作数。
- **复杂度分析**：  
  - 对每个查询我们都要遍历 `n` 个元素，时间是 `O(n)`。查询有 `m` 条，所以总时间是 `O(n·m)`。  
  - 只用了原数组和几个计数变量，额外空间是 `O(1)`（不计输入本身）。

> **大白话解释**：如果你把 `O(n·m)` 看成“每次查询都要把所有的 `n` 个数字都搬一次”，当 `n`、`m` 都是 10⁵ 时，搬运次数会达到 10¹⁰ 次，根本不可能在几秒内完成。

#### 代码（Python）

```python
def minOperations_bruteforce(nums, queries):
    """
    暴力解法：对每个查询遍历整个数组，累加绝对差。
    时间复杂度 O(n * m)，空间复杂度 O(1)。
    """
    ans = []
    for q in queries:               # 对每个查询
        total = 0
        for x in nums:              # 遍历所有数组元素
            total += abs(x - q)     # 需要的操作次数 = 绝对差
        ans.append(total)
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n·m)` — 想象成“每个查询都要把 `n` 个数字全部搬一遍”，当 `n,m` 都是 10⁵ 时，操作次数会非常大（10⁵ × 10⁵ = 10¹⁰）。
- **空间复杂度**：`O(1)` — 只用了常数级的额外变量（计数器、结果列表除外）。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于每次查询都要 **完整遍历** `nums`，这导致 `n·m` 的时间。  
观察公式：

\[
\text{answer}(q) = \sum_{i=1}^{n} |\,\text{nums}[i] - q\,|
\]

如果把 `nums` 排序后记为 `a₁ ≤ a₂ ≤ … ≤ aₙ`，则可以把数组划分为两部分：

- 左侧：所有 **≤ q** 的元素  
- 右侧：所有 **> q** 的元素  

对于左侧的每个元素 `a_i`，`|a_i - q| = q - a_i`（因为 `q` 大于等于它），  
对于右侧的每个元素 `a_j`，`|a_j - q| = a_j - q`（因为 `a_j` 大于 `q`）。

于是：

\[
\text{answer}(q) = 
\underbrace{(\#\text{左侧}) \times q - \text{左侧元素和}}_{\text{左侧贡献}}
\;+\;
\underbrace{(\text{右侧元素和}) - (\#\text{右侧}) \times q}_{\text{右侧贡献}}
\]

关键是**快速得到**：

1. 左侧（或右侧）有多少个元素  
2. 左侧（或右侧）元素的**前缀和**（累加和）

这两件事可以在 **排序 + 前缀和** 之后，用 **二分查找** 在 `O(log n)` 时间内完成：

- 排序：`O(n log n)`（一次性做）
- 前缀和数组 `pre[i] = a₁ + … + a_i`，`pre[0]=0`（`O(n)`）
- 对每个查询 `q`：  
  - 用 `bisect_left` 找到第一个大于 `q` 的位置 `pos`（即左侧元素的个数 = `pos`）。  
  - 左侧和 = `pre[pos]`，右侧和 = `pre[n] - pre[pos]`。  
  - 把上面的公式代入，算出答案。

> **核心概念解释**  
> - **二分查找**：把有序的数组想象成一本电话簿，想找某个名字出现的第一行，用“每次看中间”把范围快速缩小，这就是 `O(log n)` 的查找。  
> - **前缀和**：把数组的累计和存下来，好比把每一天的收入累计到今天的总资产，之后想知道任意区间的和，只需要两次减法。

#### 代码（Python）

```python
import bisect

def minOperations_optimal(nums, queries):
    """
    最优解：排序 + 前缀和 + 二分查找
    时间复杂度 O(n log n + m log n)，空间复杂度 O(n)。
    """
    # 1. 对 nums 排序
    nums.sort()                              # O(n log n)

    # 2. 构造前缀和数组 pre，pre[i] = 前 i 个元素的和，pre[0] = 0
    pre = [0] * (len(nums) + 1)              # 长度 n+1
    for i, x in enumerate(nums, 1):          # i 从 1 开始对应 pre 的下标
        pre[i] = pre[i - 1] + x               # 累加得到前缀和

    total_sum = pre[-1]                      # 整个数组的和，方便后面使用

    ans = []
    for q in queries:
        # 3. 二分找第一个大于 q 的位置（左侧元素个数）
        pos = bisect.bisect_left(nums, q)    # O(log n)

        # 左侧元素个数 = pos，左侧和 = pre[pos]
        left_cnt = pos
        left_sum = pre[pos]

        # 右侧元素个数 = n - pos，右侧和 = total_sum - pre[pos]
        right_cnt = len(nums) - pos
        right_sum = total_sum - pre[pos]

        # 4. 代入公式：左侧贡献 + 右侧贡献
        #    左侧：left_cnt * q - left_sum
        #    右侧：right_sum - right_cnt * q
        ops = (left_cnt * q - left_sum) + (right_sum - right_cnt * q)
        ans.append(ops)

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n log n + m log n)`  
  - 排序一次 `O(n log n)`，后续每个查询只需要二分 `O(log n)`，共 `m` 次。  
  - 与暴力解的 `O(n·m)` 相比，**从“每次遍历全部”降到了“每次只找位置”**，当 `n,m` 都是 10⁵ 时，大约只需要 `10⁵·log2(10⁵) ≈ 1.7·10⁶` 次基本操作，轻松在毫秒级完成。

- **空间复杂度**：`O(n)`  
  - 需要存放排序后的数组和前缀和数组，各占 `n` 长度的空间。相比暴力解的 `O(1)`，多了线性空间，但这在题目限制（10⁵）下完全可以接受。

---

## 心得

- **核心技巧**：把「所有元素与目标的绝对差之和」转化为「左侧元素的差 + 右侧元素的差」，利用**排序 + 前缀和 + 二分查找**实现快速求和。
- **适用场景**：  
  1. **求每个查询的总绝对差**（本题）。  
  2. **求数组中每个元素与目标值的距离之和**（如 LeetCode 1848 “Minimum Distance to the Target Element”）。  
  3. **区间统计类问题**，例如「统计数组中小于/大于某值的元素个数和总和」。
- **一句话总结**：**先把数组排好序，用前缀和把“区间求和”变成 O(1) 再配合二分定位，所有查询瞬间搞定。**

---

## 反思

- **第一反应**：看到“把所有元素变成同一个数”，立刻想到“遍历求每个元素与目标的差”，于是写出了暴力解。
- **最容易踩的坑**  
  - 忘记对 `nums` 进行 **排序**，导致二分查找失效。  
  - 前缀和数组的下标容易写错（`pre[0] = 0`，`pre[i]` 对应前 `i` 个元素）。  
  - 大数相乘可能超过 32 位整数范围，但 Python 的整数是大数，仍需注意语言的整数上限（在 C++/Java 中要用 `long long`）。
- **下次思考的第一步**：遇到「每个查询都需要对整数组求某种聚合」时，先判断能否 **预处理**（排序、前缀和、位置信息），把每次查询的复杂度从 `O(n)` 降到 `O(log n)` 或 `O(1)`。这样往往能从暴力直接跳到最优方案。