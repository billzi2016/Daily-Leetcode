# #1793. 好子数组的最大得分 / Maximum Score of a Good Subarray

> 难度：困难 · 标签：Array、Two Pointers、Binary Search、Stack、Monotonic Stack · [LeetCode 链接](https://leetcode.com/problems/maximum-score-of-a-good-subarray/)

---

## 题目（英文原版）

**Description**

You are given an array of integers nums (0-indexed) and an integer k.
The score of a subarray (i, j) is defined as min(nums[i], nums[i+1], ..., nums[j]) * (j - i + 1). A good subarray is a subarray where i <= k <= j.
Return the maximum possible score of a good subarray.

**Examples**

**Example 1:**

```
Input: nums = [1,4,3,7,4,5], k = 3
Output: 15
Explanation: The optimal subarray is (1, 5) with a score of min(4,3,7,4,5) * (5-1+1) = 3 * 5 = 15.
```

**Example 2:**

```
Input: nums = [5,5,4,5,4,1,1,1], k = 0
Output: 20
Explanation: The optimal subarray is (0, 4) with a score of min(5,5,4,5,4) * (4-0+1) = 4 * 5 = 20.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 2 * 104
- 0 <= k < nums.length

---

## 题目（中文翻译）

给定一个整数数组 `nums`（下标从 0 开始）和一个整数 `k`。  
子数组（subarray）`(i, j)` 的得分定义为  

\[
\text{score}(i, j) = \min(nums[i], nums[i+1], \dots, nums[j]) \times (j - i + 1)
\]

如果子数组满足 `i ≤ k ≤ j`，则称其为**好子数组**（good subarray）。  
返回所有好子数组中可能的最大得分。

## 示例

### 示例 1
**输入**  
``` 
nums = [1,4,3,7,4,5], k = 3
```
**输出**  
```
15
```
**解释**  
最优的子数组是 `(1, 5)`，其得分为 `min(4,3,7,4,5) * (5-1+1) = 3 * 5 = 15`。

### 示例 2
**输入**  
``` 
nums = [5,5,4,5,4,1,1,1], k = 0
```
**输出**  
```
20
```
**解释**  
最优的子数组是 `(0, 4)`，其得分为 `min(5,5,4,5,4) * (4-0+1) = 4 * 5 = 20`。

## 约束条件
- `1 ≤ nums.length ≤ 10^5`
- `1 ≤ nums[i] ≤ 2 * 10^4`
- `0 ≤ k < nums.length`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把所有**包含下标 `k` 的子数组**枚举出来，计算它们的得分 `min * 长度`，取最大值。  
- **子数组**：在数组里挑一段连续的元素，像把一根绳子从第 `i` 根结点拉到第 `j` 根结点，`i ≤ k ≤ j` 表示这根绳子必须经过第 `k` 根。  
- **最小值**：把子数组里的所有数字想成一本字典，找出字典里最小的那个词（数值）。这一步可以直接用 Python 的 `min()` 完成。  
- **长度**：子数组的元素个数，就是 `j - i + 1`（从第 `i` 到第 `j`，两端都算）。  

因为我们把所有可能的 `(i, j)` 都检查一遍，必然能得到正确答案。  

#### 代码（Python）

```python
def maximumScore(nums, k):
    n = len(nums)
    best = 0                         # 用来记录最大得分

    # 枚举左端点 i，右端点 j，要求 i <= k <= j
    for i in range(k, -1, -1):       # i 从 k 往左走
        cur_min = nums[i]            # 当前子数组的最小值，先把左端点的值放进去
        for j in range(k, n):        # j 从 k 往右走
            cur_min = min(cur_min, nums[j])   # 把右端点加入后，更新最小值
            length = j - i + 1                # 子数组长度
            score = cur_min * length          # 计算得分
            if score > best:
                best = score                  # 维护最大值
    return best
```

> **关键行中文注释**  
> - `for i in range(k, -1, -1)`: 把左端点从 `k` 向左遍历，确保子数组一定包含 `k`。  
> - `cur_min = min(cur_min, nums[j])`: 每加入一个右端点，就把最小值更新为左、右两边的最小。  
> - `score = cur_min * length`: 按题目定义算出“分数”。  

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 外层循环最多遍历 `k+1 ≤ n` 次，内层循环最多遍历 `n-k ≤ n` 次，最坏情况下相乘得到约 `n²` 次基本操作。  
  - 用大白话说，就是如果数组有 10,000 个元素，程序大概会做 100,000,000 次比较——对大数据会很慢。  

- **空间复杂度**：`O(1)`  
  - 只用了几个常数级的变量（`best、cur_min、i、j`），不随输入规模增长。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在 **每次都重新遍历右侧**（或左侧）来找最小值，导致二次循环。  
如果我们从 `k` 开始**向两边扩张**，每一步只把新加入的元素和当前的最小值比较，就能在 **一次线性扫描** 内得到所有可能的子数组得分。  

核心思想如下：

1. 初始子数组只包含 `k` 本身，`cur_min = nums[k]`，长度 `1`。  
2. 设左指针 `l = k-1`，右指针 `r = k+1`。每次把左边或右边的一个元素“加入”子数组。  
3. 为了让得分尽可能大，我们应该先加入 **更大的元素**（因为它不太可能把当前最小值降低太多），于是比较 `nums[l]` 与 `nums[r]`，把较大的那一侧先扩展。  
4. 扩展后，`cur_min = min(cur_min, nums[new_index])`（把新加入的元素与当前最小值比较），`length = r - l - 1`（注意 `l`、`r` 分别指向子数组外侧的第一个位置）。  
5. 用 `cur_min * length` 更新答案。  
6. 重复步骤 2~5，直到左指针走到数组左端、右指针走到数组右端。

因为每个元素只会被加入一次，整个过程是 **O(n)** 的线性时间。  

> **为什么这种贪心是对的？**  
> - 每次我们都保留了子数组的 **最小值**（`cur_min`），这就是得分公式里唯一会让分数下降的因素。  
> - 若我们把一个更小的数提前加入，它会把 `cur_min` 降得更低，后面再加入更大的数也救不回已经被降低的最小值。  
> - 因此“先把较大的那一侧扩进去”可以保证在同等长度下得到更大的 `cur_min`，从而不遗漏最优解。  

下面给出完整实现，并在代码里写上详细注释。

#### 代码（Python）

```python
def maximumScore(nums, k):
    n = len(nums)

    # 初始状态：子数组只包含 k 本身
    cur_min = nums[k]          # 当前子数组的最小值
    best = cur_min * 1         # 先算长度为 1 时的得分

    # 左右指针分别指向子数组外侧的第一个位置
    left = k - 1
    right = k + 1

    # 循环直到左右都跑出数组边界
    while left >= 0 or right < n:
        # 先决定向左还是向右扩展
        #   如果右侧已经没有元素，必须左扩；左侧没有则右扩
        #   否则比较 nums[left] 与 nums[right]，把较大的那一侧加入
        if right == n or (left >= 0 and nums[left] >= nums[right]):
            # 向左扩展
            cur_min = min(cur_min, nums[left])   # 更新最小值
            left -= 1
        else:
            # 向右扩展
            cur_min = min(cur_min, nums[right])  # 更新最小值
            right += 1

        # 当前子数组的长度 = (右指针-左指针-1)
        length = right - left - 1
        best = max(best, cur_min * length)       # 维护最大得分

    return best
```

> **代码要点**  
> - `left`、`right` 初始分别指向 `k` 左右相邻位置的**外侧**，这样子数组始终是 `(left+1, right-1)`。  
> - `cur_min = min(cur_min, nums[new])` 只需要一次比较，因为 `cur_min` 已经是当前子数组的最小值。  
> - `length = right - left - 1` 用来把子数组的真实长度算出来。  

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 每个元素最多被左指针或右指针访问一次，整体只做线性次数的比较和更新。  
  - 相比暴力的 `O(n²)`，速度提升了一个量级，几乎可以在 10⁵ 长度的数组里瞬间算完。  

- **空间复杂度**：`O(1)`  
  - 只用了常数个额外变量（`cur_min、best、left、right`），不随 `n` 增长。  

---

## 心得  

- **核心技巧**：从固定位置 `k` 向左右**双指针贪心扩展**，始终维护子数组的最小值。  
- **适用的题型**  
  1. “包含指定下标的子数组” 类似题，例如 LeetCode 1793 *Maximum Score of a Good Subarray*（本题）。  
  2. “最大化最小值 × 长度” 的区间问题，如 “Maximum Subarray Min‑Product”。  
  3. “在数组中找出满足某种单调约束的最长区间”，常用双指针或单调栈。  
- **一句话总结**：**从中心向外一步步把“更大的”元素先加入，始终保留最小值，就能线性求出所有可能的得分**。  

---

## 反思  

- **第一反应**：把所有包含 `k` 的子数组枚举出来，直接算最小值乘长度——这就是暴力解。  
- **最容易踩的坑**  
  - **边界处理**：左指针走到 `-1`、右指针走到 `n` 时必须停止，否则会访问越界。  
  - **长度公式**：因为指针指向的是子数组外侧，长度要写成 `right - left - 1`，容易写成 `right - left + 1` 导致错误。  
  - **最小值更新**：一定要用 `min(cur_min, nums[new])`，而不是重新遍历整个子数组。  
- **下次类似题的第一步**：先确定“固定点”（本题是 `k`），然后**考虑从该点向两边扩张**的思路，看看是否可以用一次遍历维护必要的状态（最小值、最大值、计数等）。这样往往能把暴力的二次循环压到一次线性扫描。