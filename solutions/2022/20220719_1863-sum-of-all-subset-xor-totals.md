# #1863. 所有子集异或总和的和 / Sum of All Subset XOR Totals

> 难度：简单 · 标签：Array、Math、Backtracking、Bit Manipulation、Combinatorics、Enumeration · [LeetCode 链接](https://leetcode.com/problems/sum-of-all-subset-xor-totals/)

---

## 题目（英文原版）

**Description**

The XOR total of an array is defined as the bitwise XOR of all its elements, or 0 if the array is empty.
Given an array nums, return the sum of all XOR totals for every subset of nums.
Note: Subsets with the same elements should be counted multiple times.
An array a is a subset of an array b if a can be obtained from b by deleting some (possibly zero) elements of b.

**Examples**

**Example 1:**

```
Input: nums = [1,3]
Output: 6
Explanation: The 4 subsets of [1,3] are:
- The empty subset has an XOR total of 0.
- [1] has an XOR total of 1.
- [3] has an XOR total of 3.
- [1,3] has an XOR total of 1 XOR 3 = 2.
0 + 1 + 3 + 2 = 6
```

**Example 2:**

```
Input: nums = [5,1,6]
Output: 28
Explanation: The 8 subsets of [5,1,6] are:
- The empty subset has an XOR total of 0.
- [5] has an XOR total of 5.
- [1] has an XOR total of 1.
- [6] has an XOR total of 6.
- [5,1] has an XOR total of 5 XOR 1 = 4.
- [5,6] has an XOR total of 5 XOR 6 = 3.
- [1,6] has an XOR total of 1 XOR 6 = 7.
- [5,1,6] has an XOR total of 5 XOR 1 XOR 6 = 2.
0 + 5 + 1 + 6 + 4 + 3 + 7 + 2 = 28
```

**Example 3:**

```
Input: nums = [3,4,5,6,7,8]
Output: 480
Explanation: The sum of all XOR totals for every subset is 480.
```

**Constraints**

- 1 <= nums.length <= 12
- 1 <= nums[i] <= 20

---

## 题目（中文翻译）

XOR 总和（XOR total）定义为数组中所有元素的按位异或（bitwise XOR），若数组为空则为 0。  
给定数组 `nums`，返回 `nums` 的每一个子集的 XOR 总和的累加和。  
注意：具有相同元素的子集应当被多次计数。  
数组 `a` 是数组 `b` 的子集（subset），当且仅当可以通过删除 `b` 中的若干（可能为零）元素得到 `a`。

### 示例

#### 示例 1
**输入**: `nums = [1,3]`  
**输出**: `6`  
**解释**: `[1,3]` 的 4 个子集为：  
- 空子集的 XOR 总和为 0。  
- `[1]` 的 XOR 总和为 1。  
- `[3]` 的 XOR 总和为 3。  
- `[1,3]` 的 XOR 总和为 `1 XOR 3 = 2`。  
`0 + 1 + 3 + 2 = 6`

#### 示例 2
**输入**: `nums = [5,1,6]`  
**输出**: `28`  
**解释**: `[5,1,6]` 的 8 个子集为：  
- 空子集的 XOR 总和为 0。  
- `[5]` 的 XOR 总和为 5。  
- `[1]` 的 XOR 总和为 1。  
- `[6]` 的 XOR 总和为 6。  
- `[5,1]` 的 XOR 总和为 `5 XOR 1 = 4`。  
- `[5,6]` 的 XOR 总和为 `5 XOR 6 = 3`。  
- `[1,6]` 的 XOR 总和为 `1 XOR 6 = 7`。  
- `[5,1,6]` 的 XOR 总和为 `5 XOR 1 XOR 6 = 2`。  
`0 + 5 + 1 + 6 + 4 + 3 + 7 + 2 = 28`

#### 示例 3
**输入**: `nums = [3,4,5,6,7,8]`  
**输出**: `480`  
**解释**: 所有子集的 XOR 总和之和为 480。

### 约束条件
- `1 <= nums.length <= 12`
- `1 <= nums[i] <= 20`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是**把所有子集枚举出来**，对每个子集计算它的 XOR 总和，再把这些 XOR 总和累加。  

- **子集**可以看成从原数组里“挑”或“不挑”每个元素。比如把 `nums = [a, b, c]` 想象成三个开关，每个开关可以打开（选进子集）或关闭（不选），于是会产生 `2³ = 8` 种不同的组合。  
- **XOR** 操作就像“奇偶”计数器：相同的位出现两次会相互抵消（0），出现一次则保留（1）。把子集里所有数按位 XOR，得到的就是该子集的 XOR 总和。  

暴力法之所以**一定正确**，是因为我们真的遍历了题目要求的**所有**子集，没漏掉也没多算。

**复杂度分析（大白话）**  
- 对长度为 `n` 的数组，有 `2ⁿ` 个子集。我们要对每个子集遍历其中的元素来算 XOR，最坏情况下每个子集会遍历 `n` 次。于是总的时间是 `2ⁿ × n`，写成 **O(n·2ⁿ)**。  
- 只用了几个整数来保存临时的 XOR 值和累计答案，空间是 **O(1)**（不算递归栈），因为我们不需要额外的数组来存所有子集。

#### 代码（Python）

```python
from itertools import combinations
from typing import List

def subsetXORSum_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    total = 0                      # 累计所有子集的 XOR 总和

    # 0~n 表示子集的大小，分别枚举每一种大小的组合
    for k in range(n + 1):
        for comb in combinations(nums, k):   # 取出大小为 k 的子集
            xor_val = 0
            for x in comb:                   # 计算该子集的 XOR
                xor_val ^= x
            total += xor_val                  # 加入答案

    return total
```

> **关键行中文注释**  
> - `combinations(nums, k)`：相当于从 `nums` 中挑出 `k` 个元素，所有可能的挑法都列出来。  
> - `xor_val ^= x`：把当前元素的二进制和已有的 `xor_val` 做“奇偶”合并，等价于 `xor_val = xor_val ^ x`。

#### 复杂度

- **时间复杂度**：`O(n·2ⁿ)` —— 想象成把所有可能的开关组合都试一遍，每次还要把选中的数逐个 “翻转”。
- **空间复杂度**：`O(1)` —— 只用了常数个临时变量。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到 **瓶颈** 在于 **枚举 2ⁿ 个子集**。实际上我们并不需要真的列出每个子集，只要知道每一位（每个二进制位）在所有子集的 XOR 结果中出现了多少次，就可以直接算出答案。

**关键观察**  
- 对于某一位 `b`（比如第 2 位对应的值是 `4`），子集的 XOR 在这位上是 **1** 当且仅当子集中包含了奇数个“该位为 1 的数”。  
- 假设数组里至少有一个数的第 `b` 位是 `1`。我们把所有子集分成两类：  
  1. **不选** 这第一个出现 `1` 的数 → 该位的奇偶性由其余元素决定。  
  2. **选** 这第一个出现 `1` 的数 → 会把奇偶性翻转一次。  

  对于每一种其余元素的选法，上面两类各对应一种子集，恰好互为翻转。因此 **恰好有一半子集** 在该位上得到 `1`，另一半得到 `0`。  
- 如果整个数组在第 `b` 位上都没有 `1`（即所有数的该位都是 `0`），那么无论怎么选，XOR 那位永远是 `0`，贡献为 `0`。

**结论**  
- 只要该位在 **任意一个数** 中出现过，它在所有子集的 XOR 结果里出现 `1` 的次数就是 `2^{n-1}`（所有子集的一半）。  
- 因此，这一位对答案的贡献是 `2^{n-1} * (1 << b)`。  
- 把所有出现过的位加起来，就是 `2^{n-1} * (OR of all numbers)`，因为 `OR` 正好把“出现过的位”全打开。

**类比**：想象每一位是灯泡，只要有一盏灯能被点亮（数组里有数的该位为 1），那么在所有可能的开关组合里，一半的组合会让灯泡亮，一半会让灯泡灭。最终我们只需要统计哪些灯泡能被点亮，然后乘以组合数的一半。

**算法步骤**  
1. 计算数组所有元素的 **按位或**（`or_all = nums[0] | nums[1] | ...`）。  
2. 计算 `2^{n-1}`（可以用左移 `1 << (n-1)`）。  
3. 返回 `or_all * (1 << (n-1))`。

#### 代码（Python）

```python
from typing import List

def subsetXORSum(nums: List[int]) -> int:
    """
    最优解：答案 = (所有数的按位或) * 2^{n-1}
    """
    n = len(nums)
    # 1. 计算所有数的 OR
    or_all = 0
    for x in nums:
        or_all |= x          # 把每个数的二进制位“打开”，相当于查字典的合并

    # 2. 2^{n-1} 用左移实现，左移 k 位等价于乘以 2^k
    subsets_half = 1 << (n - 1)   # 当 n=1 时，2^{0}=1，仍然成立

    # 3. 直接返回乘积
    return or_all * subsets_half
```

> **关键行中文注释**  
> - `or_all |= x`：把 `x` 的每一位与 `or_all` 做“或”操作，像把多本字典的页码合在一起，只要有一本出现该页码，就保留下来。  
> - `1 << (n - 1)`：左移相当于 “把 1 乘以 2 的 (n‑1) 次方”，得到所有子集的一半数量。

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历一次数组，做常数次的位运算。比暴力的 `O(n·2ⁿ)` 快很多。  
- **空间复杂度**：`O(1)` —— 只用了几个整数变量。

---

## 心得

- **核心技巧**：**按位或 + 子集数量的一半**。  
  通过观察每一位的奇偶性分布，发现只要该位出现过，它在所有子集的 XOR 里出现 `1` 的次数恰好是子集总数的一半。于是把复杂的枚举转化为一次线性遍历。  

- **适用题型**（类似思路）  
  1. “所有子集的 AND/OR 总和”——可以用类似的位统计方法。  
  2. “求所有子集的位wise 异或之和”——本题的变形。  
  3. “统计所有子集的位和（求每一位出现多少次）”——常见的组合计数技巧。

- **一句话总结**：**只要位出现过，它在子集 XOR 中出现一半次数 → 用 OR 乘 2^{n-1} 即可。**

---

## 反思

- **第一反应**：直接想把所有子集枚举出来，写递归或 `itertools.combinations`，因为题目说“每个子集”。这是一种直觉的“穷举”思路。  
- **最容易踩的坑**  
  - 忘记 **空子集** 的 XOR 为 `0`，但在公式里已经自然包含。  
  - 当 `n = 1` 时，`2^{n-1}` 为 `1`，要确保左移不出现负数位移（`1 << 0 = 1`）。  
  - 对位运算不熟悉时，可能会误把 “出现过的位” 当成 “每个数的位数之和”，导致错误。  

- **下次类似题目**：**先思考“每一位的贡献如何计数”，再看是否可以把计数结果直接用乘法合并**。这一步往往能把指数级的枚举压缩到线性时间。