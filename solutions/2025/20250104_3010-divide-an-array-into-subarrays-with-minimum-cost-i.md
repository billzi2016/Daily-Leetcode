# #3010. 将数组划分为子数组，使成本最小 I / Divide an Array Into Subarrays With Minimum Cost I

> 难度：简单 · 标签：Array、Sorting、Enumeration · [LeetCode 链接](https://leetcode.com/problems/divide-an-array-into-subarrays-with-minimum-cost-i/)

---

## 题目（英文原版）

**Description**

You are given an array of integers nums of length n.
The cost of an array is the value of its first element. For example, the cost of [1,2,3] is 1 while the cost of [3,4,1] is 3.
You need to divide nums into 3 disjoint contiguous subarrays.
Return the minimum possible sum of the cost of these subarrays.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,12]
Output: 6
Explanation: The best possible way to form 3 subarrays is: [1], [2], and [3,12] at a total cost of 1 + 2 + 3 = 6.
The other possible ways to form 3 subarrays are:
- [1], [2,3], and [12] at a total cost of 1 + 2 + 12 = 15.
- [1,2], [3], and [12] at a total cost of 1 + 3 + 12 = 16.
```

**Example 2:**

```
Input: nums = [5,4,3]
Output: 12
Explanation: The best possible way to form 3 subarrays is: [5], [4], and [3] at a total cost of 5 + 4 + 3 = 12.
It can be shown that 12 is the minimum cost achievable.
```

**Example 3:**

```
Input: nums = [10,3,1,1]
Output: 12
Explanation: The best possible way to form 3 subarrays is: [10,3], [1], and [1] at a total cost of 10 + 1 + 1 = 12.
It can be shown that 12 is the minimum cost achievable.
```

**Constraints**

- 3 <= n <= 50
- 1 <= nums[i] <= 50

---

## 题目（中文翻译）

给定一个长度为 `n` 的整数数组 `nums`。  
数组的 **成本**（cost）定义为它的第一个元素的值。例如，数组 `[1,2,3]` 的成本为 `1`，而数组 `[3,4,1]` 的成本为 `3`。  

你需要将 `nums` 划分成 **3 个互不重叠且连续的子数组**（subarrays）。  
返回这些子数组成本之和的 **最小可能值**。

## 示例

### 示例 1
**输入**  
```text
nums = [1,2,3,12]
```
**输出**  
```text
6
```
**解释**  
形成 3 个子数组的最佳方式是：`[1]`、`[2]` 和 `[3,12]`，其总成本为 `1 + 2 + 3 = 6`。  
其他可能的划分方式包括：
- `[1]、[2,3]、[12]`，总成本 `1 + 2 + 12 = 15`。  
- `[1,2]、[3]、[12]`，总成本 `1 + 3 + 12 = 16`。

### 示例 2
**输入**  
```text
nums = [5,4,3]
```
**输出**  
```text
12
```
**解释**  
形成 3 个子数组的最佳方式是：`[5]、[4]、[3]`，总成本为 `5 + 4 + 3 = 12`。  
可以证明 `12` 是可以达到的最小成本。

### 示例 3
**输入**  
```text
nums = [10,3,1,1]
```
**输出**  
```text
12
```
**解释**  
形成 3 个子数组的最佳方式是：`[10,3]、[1]、[1]`，总成本为 `10 + 1 + 1 = 12`。  
可以证明 `12` 是可以达到的最小成本。

## 约束条件
- `3 <= n <= 50`
- `1 <= nums[i] <= 50`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有可能的切分方式** 都枚举一遍，然后挑出费用最小的那一种。  
因为题目要求把数组 `nums` 分成 **3 个连续且不相交的子数组**，我们只需要确定两条切分线的位置：

```
[0 … i-1] | [i … j-1] | [j … n-1]
   第 1 部分   第 2 部分   第 3 部分
```

- `i` 必须在 `1 … n-2` 之间（第 1 段至少有一个元素，剩下的还要留出两段）  
- `j` 必须在 `i+1 … n-1` 之间（第 2 段也至少有一个元素）

子数组的 **费用** 只和它的第一个元素有关，所以一次切分的总费用是：

```
cost = nums[0] + nums[i] + nums[j]
```

只要遍历所有合法的 `(i, j)`，记录最小的 `cost` 就能得到答案。

> **类比**：把数组想成一条装满珠子的线，切分线就像是两把剪刀。我们把剪刀摆在所有可能的位置，看看每次剪下来的“三段珠子”首颗珠子的价值之和最小是多少。

**为什么一定能得到最优解**：因为我们把所有合法的切法都尝试了一遍，最小值自然就是全局最优。

**复杂度分析**：

- 外层循环 `i` 需要遍历 `n-2` 次，内层循环 `j` 最多遍历 `n-i-1` 次，总次数约为 `O(n²)`（大约是 `n*(n-1)/2`）。  
- 空间上只用了常数个变量，`O(1)`。

> **大白话**：`O(n²)` 就是“把 `n` 个人两两配对”，如果 `n` 只有 50（本题上限），最多也只有 2500 次配对，完全可以接受。

#### 代码（Python）

```python
def min_cost_bruteforce(nums):
    n = len(nums)
    # 先把答案设成一个很大的数，后面会不断取更小的
    best = float('inf')

    # i 为第二段的起点，下标从 1 开始，保证第一段非空
    for i in range(1, n - 1):
        # j 为第三段的起点，必须在 i 之后，保证第二段非空
        for j in range(i + 1, n):
            cost = nums[0] + nums[i] + nums[j]   # 三段子数组的费用
            if cost < best:
                best = cost                      # 记录更小的费用

    return best
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  → 需要检查所有 `i, j` 的组合，最坏情况下大约是 `n*(n-1)/2` 次。

- **空间复杂度**：`O(1)`  
  → 只用了几个整数变量，不随 `n` 增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正决定费用的只有三个数**：`nums[0]`（永远在），以及切分点 `i`、`j` 处的两个数 `nums[i]`、`nums[j]`。  
所以我们要做的其实是：

> 在下标 `1 … n-1` 中，选出 **两个** 元素 `a`、`b`，要求 `a` 在 `b` 前面（`i < j`），使 `a + b` 最小。

`nums[0]` 是固定的，只需要把 **后面** 两个最小、且满足前后顺序的数加进去。

**如何在 O(n) 时间找到这两个数？**  
我们可以从右往左遍历数组，维护 “当前右侧最小的元素”。具体步骤：

1. 初始化 `min_suffix = +∞`（右侧最小值），`best_pair = +∞`（最小的 `nums[i] + nums[j]`）。
2. 从 `j = n-1` 往左遍历到 `1`（因为 `i` 必须 ≥ 1）：
   - 对于当前位置 `j`，`min_suffix` 已经是 `j+1 … n-1` 区间的最小值（如果有的话）。
   - 设 `i = j-1`（即把 `j` 当作第二段的起点），此时 `nums[i]` 与 `min_suffix` 组合得到一种合法的 `(i, j')`（这里的 `j'` 实际上是 `min_suffix` 所在的下标），费用是 `nums[i] + min_suffix`。更新 `best_pair` 为更小的值。
   - 然后把 `nums[j]` 合并进右侧最小值：`min_suffix = min(min_suffix, nums[j])`。
3. 最终答案 = `nums[0] + best_pair`。

> **类比**：把数组看成一排商店，左边的店是你必须先进入的，接下来你想找两家“最便宜的”店，而且第二家必须在第一家后面。我们从最右边的店开始往左走，随时记住“目前看到的最便宜的右侧店”，这样每走到一间新店时，就立刻能算出“这家店 + 右侧最便宜的那家”的费用。

**为什么正确**：

- 对每个可能的左侧切点 `i`，我们都用了**右侧最小值**来代表所有合法 `j > i` 中费用最小的那一个。  
- 由于我们遍历了所有 `i`（实际上是 `i = j-1` 的形式），不漏掉任何合法组合。  
- 取最小的 `nums[i] + min_suffix` 就等价于在所有合法 `(i, j)` 中选出最小的两数和。

**复杂度**：

- 只遍历一次数组，时间 `O(n)`。  
- 只用了几个额外变量，空间 `O(1)`。

#### 代码（Python）

```python
def min_cost_optimal(nums):
    n = len(nums)
    # 第一个子数组的费用是固定的
    first_cost = nums[0]

    # min_suffix 记录当前遍历位置右侧（包括自己）最小的元素值
    min_suffix = float('inf')
    # best_pair 记录在所有合法 (i, j) 中，nums[i] + nums[j] 的最小值
    best_pair = float('inf')

    # 从右往左遍历，j 代表「第三段」的起点（必须 ≥ 1）
    for j in range(n - 1, 0, -1):
        # 此时 min_suffix 已经是 j+1 … n-1 区间的最小值（如果存在）
        # 把 j 当作「第二段」的起点，则左侧的 i 必须是 j-1（因为我们只需要考虑相邻的 i，j）
        # 实际上遍历所有 i，只要把 nums[i] 与右侧最小值比较即可
        if min_suffix != float('inf'):          # 右侧还有元素时才构成合法的三段划分
            best_pair = min(best_pair, nums[j] + min_suffix)

        # 更新右侧最小值：把当前位置的 nums[j] 加入考虑范围
        min_suffix = min(min_suffix, nums[j])

    # 对于 n == 3 的特殊情况，上面的循环只会比较一次，仍然得到正确答案
    return first_cost + best_pair
```

> **说明**：  
> - 循环从 `n-1` 到 `1`（不包括 `0`），因为 `0` 已经是第一段的起点，不能再当作切分点。  
> - 当 `min_suffix` 仍为 `inf` 时，说明右侧没有元素，不能形成三段，此时不更新 `best_pair`。  
> - 最终的 `best_pair` 正好是 `min_{i<j} (nums[i] + nums[j])`。

#### 复杂度

- **时间复杂度**：`O(n)`  
  → 只遍历一次数组，线性时间。相比暴力的 `O(n²)`，速度提升明显（尤其当 `n` 更大时）。

- **空间复杂度**：`O(1)`  
  → 只用了常数个额外变量。

---

## 心得

- **核心技巧**：把「子数组的费用是首元素」的限制转化为「只需要关注切分点的首元素」；随后利用**单调后缀最小值**（或称“从右到左维护最小值”）在一次遍历中求出两数之和的最小值。  
- **适用的题型**：  
  1. “在数组中选取 k（k≥2）个元素，使它们的下标保持递增且和最小/最大”。  
  2. “划分数组为若干段，每段费用只与首元素或尾元素相关”。  
  3. “在数组里找两数之和最小且满足顺序约束”。  
- **一句话总结**：**把费用只和首元素挂钩的划分问题，等价于在后缀中找最小的两个递增下标的数**。

---

## 反思

- **第一反应**：直接枚举所有切分点（暴力）——因为题目规模小，先写出来最安全。  
- **最容易踩的坑**：  
  - 忘记子数组必须 **非空**，导致切分点取值越界。  
  - 在最优解里没有正确处理 `n = 3` 的边界（右侧最小值为空时的情况）。  
  - 误以为可以随意挑选最小的两个数而不考虑顺序，导致错误答案。  
- **下次类似题的第一步**：先把“每段费用只取决于某个位置的值”这类信息抽象出来，看看是否能把问题转化为“在序列中挑选满足顺序约束的若干个元素的最小和”，再考虑单调栈/单调数组或前缀/后缀最小值等线性技巧。