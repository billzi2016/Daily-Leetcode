# #2270. 分割数组的方案数 / Number of Ways to Split Array

> 难度：中等 · 标签：Array、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/number-of-ways-to-split-array/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums of length n.
nums contains a valid split at index i if the following are true:
Return the number of valid splits in nums.

**Examples**

**Example 1:**

```
Input: nums = [10,4,-8,7]
Output: 2
Explanation: 
There are three ways of splitting nums into two non-empty parts:
- Split nums at index 0. Then, the first part is [10], and its sum is 10. The second part is [4,-8,7], and its sum is 3. Since 10 >= 3, i = 0 is a valid split.
- Split nums at index 1. Then, the first part is [10,4], and its sum is 14. The second part is [-8,7], and its sum is -1. Since 14 >= -1, i = 1 is a valid split.
- Split nums at index 2. Then, the first part is [10,4,-8], and its sum is 6. The second part is [7], and its sum is 7. Since 6 < 7, i = 2 is not a valid split.
Thus, the number of valid splits in nums is 2.
```

**Example 2:**

```
Input: nums = [2,3,1,0]
Output: 2
Explanation: 
There are two valid splits in nums:
- Split nums at index 1. Then, the first part is [2,3], and its sum is 5. The second part is [1,0], and its sum is 1. Since 5 >= 1, i = 1 is a valid split. 
- Split nums at index 2. Then, the first part is [2,3,1], and its sum is 6. The second part is [0], and its sum is 0. Since 6 >= 0, i = 2 is a valid split.
```

**Constraints**

- 2 <= nums.length <= 105
- -105 <= nums[i] <= 105

---

## 题目（中文翻译）

给定一个下标从 **0** 开始的整数数组 `nums`，长度为 `n`。  
如果在下标 `i` 处将 `nums` 分成左右两段，使得：

- 左侧子数组为 `nums[0..i]`（包含下标 `i`），右侧子数组为 `nums[i+1..n-1]`（两段均非空），且
- 左侧子数组的元素和 **大于等于** 右侧子数组的元素和，

则称 `i` 为 **有效分割点（valid split）**。  

求数组 `nums` 中所有有效分割点的数量，并返回该数量。

### 示例

#### 示例 1
```
Input: nums = [10,4,-8,7]
Output: 2
Explanation: 
存在三种将 `nums` 分成两个非空部分的方式：
- 在下标 0 处分割。左侧子数组为 `[10]`，和为 10；右侧子数组为 `[4,-8,7]`，和为 3。由于 10 ≥ 3，`i = 0` 为有效分割。
- 在下标 1 处分割。左侧子数组为 `[10,4]`，和为 14；右侧子数组为 `[-8,7]`，和为 -1。由于 14 ≥ -1，`i = 1` 为有效分割。
- 在下标 2 处分割。左侧子数组为 `[10,4,-8]`，和为 6；右侧子数组为 `[7]`，和为 7。由于 6 < 7，`i = 2` **不是** 有效分割。

因此共有 2 个有效分割点，返回 `2`。
```

#### 示例 2
```
Input: nums = [2,3,1,0]
Output: 2
Explanation: 
存在两种有效的分割方式：
- 在下标 1 处分割。左侧子数组为 `[2,3]`，和为 5；右侧子数组为 `[1,0]`，和为 1。5 ≥ 1，`i = 1` 为有效分割。
- 在下标 2 处分割。左侧子数组为 `[2,3,1]`，和为 6；右侧子数组为 `[0]`，和为 0。6 ≥ 0，`i = 2` 为有效分割。

返回 `2`。
```

### 约束条件
- `2 <= nums.length <= 10^5`
- `-10^5 <= nums[i] <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有可能的切分点都枚举一遍。  
- **切分点** `i` 表示把数组分成 `[0 … i]` 与 `[i+1 … n‑1]` 两段，要求两段都非空。  
- 对每一个 `i`，我们分别把左边和右边的元素全部加起来，得到 `left_sum` 与 `right_sum`。  
- 只要 `left_sum >= right_sum`，这个 `i` 就是“合法切分”。  

> **类比**：把数组想象成一本书的章节，切分点就像在目录里插入一本新书的章节页码。我们需要把左边章节的页数（左段和）和右边章节的页数（右段和）逐个算出来，再比较大小。

这种做法一定能得到正确答案，因为我们没有遗漏任何可能的切分点，也没有对比较条件做任何简化。

#### 代码（Python）

```python
def waysToSplit_bruteforce(nums):
    n = len(nums)
    ans = 0

    # 枚举所有合法的切分点 i，i 取值范围是 0 … n-2（右边必须至少有一个元素）
    for i in range(n - 1):
        left_sum = 0
        # 计算左段和：把下标 0 … i 的元素全部相加
        for j in range(i + 1):
            left_sum += nums[j]

        right_sum = 0
        # 计算右段和：把下标 i+1 … n-1 的元素全部相加
        for j in range(i + 1, n):
            right_sum += nums[j]

        # 判断是否合法
        if left_sum >= right_sum:
            ans += 1

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 对每个切分点（大约 `n` 次）我们都要遍历一次左段和一次右段，最坏情况下每次都要遍历 `≈ n` 个元素。  
  - 用大白话说，就是“把一本 100 页的书的每一页都重复读 100 次”，所以会慢得不可接受。  

- **空间复杂度**：`O(1)`  
  - 只用了常数个额外变量（`left_sum、right_sum、ans`），不随输入规模增长。

---

### 2. 最优解  

#### 思路  

暴力解的慢点在于**重复累计求和**。  
实际上，左段的和 `left_sum(i)` 与前一个切分点的左段和 `left_sum(i‑1)` 只差一个元素 `nums[i]`：  

```
left_sum(i) = left_sum(i‑1) + nums[i]
```

这就是**前缀和**的核心思想——一次遍历就能得到所有前缀和。  
同时，如果我们事先算出整个数组的总和 `total`，右段的和就可以用总和减去左段和得到：

```
right_sum(i) = total - left_sum(i)
```

于是我们只需要一次线性扫描：

1. 先算出 `total = sum(nums)`（一次 O(n)）。  
2. 再从左到右累计 `left_sum`，每走到一个合法的切分点 `i`（`i ≤ n‑2`），检查 `left_sum >= total - left_sum`。  
3. 满足条件就计数。

> **类比**：把数组想象成一根绳子，`total` 是绳子的总长度。我们从左边慢慢卷起绳子，每卷一次就知道已经卷了多少（`left_sum`），剩下的自然是 `total - left_sum`。只要左边卷起来的长度不小于右边剩余的长度，就算一次合法的“分割”。  

这样我们只遍历两遍数组（一次求总和，一次累计），时间降到 `O(n)`，空间保持 `O(1)`。

#### 代码（Python）

```python
def waysToSplit(nums):
    """
    返回数组 nums 中合法切分点的数量。
    思路：一次遍历得到总和 total；
          再一次遍历累计前缀和 left_sum，比较 left_sum 与 total - left_sum。
    """
    total = sum(nums)          # 整个数组的和，O(n)
    left_sum = 0               # 累计左侧的前缀和
    ans = 0

    # i 只能到 n-2，因为右边必须至少保留一个元素
    for i in range(len(nums) - 1):
        left_sum += nums[i]    # 前缀和递推：加入当前元素

        # 右侧和 = total - left_sum
        if left_sum >= total - left_sum:
            ans += 1

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只需要两次线性遍历（求总和 + 累计前缀），相当于“读一本书只读一遍”。相比暴力的 `O(n²)`，速度提升了 **n 倍**。  

- **空间复杂度**：`O(1)`  
  - 只用几个整数变量（`total、left_sum、ans`），不随数组长度增长。

---

## 心得  

- **核心技巧**：前缀和（Prefix Sum）+ 总和的减法。  
- **适用的题型**  
  1. “判断数组中是否存在满足某种前缀和条件的切分点”——如 LeetCode 1520. **Maximum Number of Non‑Overlapping Subarrays With Sum Equals Target**。  
  2. “求满足前缀和与后缀和关系的子数组数量”——如 LeetCode 974. **Subarray Sums Divisible by K**。  
- **一句话总结**：  
  *“把累计的左边和当作滚动的指针，用总和减去它即得右边和，一遍遍历即可。”*

---

## 反思  

- **第一反应**：看到“把数组分成两段，左边的和 ≥ 右边的和”，自然会想到“遍历每个切分点，分别求左、右和”。这就是暴力思路。  
- **最容易踩的坑**  
  - **边界条件**：切分点不能放在最左或最右，必须保证两段都非空；因此循环上界是 `len(nums)-2`（或在代码里遍历到 `len(nums)-1` 并在比较前已累加当前元素）。  
  - **负数情况**：数组可能出现负数，不能把“左边和越大越好”简化为只看正数，需要完整比较。  
  - **整数溢出**：在 Python 中整数不溢出，但在某些语言需要使用 64 位整数。  
- **下次遇到同类题**：第一步先问自己“是否可以一次遍历累计得到左边的值？”如果答案是“可以”，那么就考虑**前缀和 + 总和**的技巧。