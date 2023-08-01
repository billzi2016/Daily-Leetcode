# #2344. **使数组可被整除的最少删除次数** / Minimum Deletions to Make Array Divisible

> 难度：困难 · 标签：Array、Math、Sorting、Heap (Priority Queue)、Number Theory · [LeetCode 链接](https://leetcode.com/problems/minimum-deletions-to-make-array-divisible/)

---

## 题目（英文原版）

**Description**

You are given two positive integer arrays nums and numsDivide. You can delete any number of elements from nums.
Return the minimum number of deletions such that the smallest element in nums divides all the elements of numsDivide. If this is not possible, return -1.
Note that an integer x divides y if y % x == 0.

**Examples**

**Example 1:**

```
Input: nums = [2,3,2,4,3], numsDivide = [9,6,9,3,15]
Output: 2
Explanation: 
The smallest element in [2,3,2,4,3] is 2, which does not divide all the elements of numsDivide.
We use 2 deletions to delete the elements in nums that are equal to 2 which makes nums = [3,4,3].
The smallest element in [3,4,3] is 3, which divides all the elements of numsDivide.
It can be shown that 2 is the minimum number of deletions needed.
```

**Example 2:**

```
Input: nums = [4,3,6], numsDivide = [8,2,6,10]
Output: -1
Explanation: 
We want the smallest element in nums to divide all the elements of numsDivide.
There is no way to delete elements from nums to allow this.
```

**Constraints**

- 1 <= nums.length, numsDivide.length <= 105
- 1 <= nums[i], numsDivide[i] <= 109

---

## 题目（中文翻译）

给定两个正整数数组 `nums` 和 `numsDivide`。你可以从 `nums` 中删除任意数量的元素。  
返回使得 `nums` 中的最小元素能够整除（divides）`numsDivide` 中所有元素所需的最少删除次数。如果无法实现，返回 `-1`。  

**注意**：整数 `x` 整除 `y` 当且仅当 `y % x == 0`。

### 示例

#### 示例 1
```
Input: nums = [2,3,2,4,3], numsDivide = [9,6,9,3,15]
Output: 2
Explanation: 
最小的元素是 `2`，但 `2` 不能整除 `numsDivide` 中的所有元素。
我们删除 `nums` 中所有等于 `2` 的元素（共 2 次），得到 `nums = [3,4,3]`。
此时最小元素为 `3`，而 `3` 能整除 `numsDivide` 的所有元素。
可以证明 2 是所需的最小删除次数。
```

#### 示例 2
```
Input: nums = [4,3,6], numsDivide = [8,2,6,10]
Output: -1
Explanation: 
我们希望 `nums` 中的最小元素能够整除 `numsDivide` 的所有元素。
无论如何删除 `nums` 中的元素，都无法满足该条件，因此返回 -1。
```

### 约束条件
- `1 <= nums.length, numsDivide.length <= 10^5`
- `1 <= nums[i], numsDivide[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把 `nums` 中的每个元素都当作“留下来的最小值”，**  
然后判断它是否能整除 `numsDivide` 中的所有数。  

- **数据结构**：我们只需要两个普通的 **列表**（数组），不需要额外的高级结构。  
  - 把 `nums` 当成“可删除或保留的候选集合”。  
  - 把 `numsDivide` 当成“必须被整除的目标集合”。  

- **为什么正确**：如果某个数 `x` 能整除 `numsDivide` 中的每个元素，那么把所有 **比 `x` 小** 的数全部删掉，`x` 就会成为 `nums` 中的最小值，题目要求也就满足了。  

- **暴力实现**：  
  1. 对 `nums` 中的每个元素 `candidate`（不去重），遍历 `numsDivide` 检查 `candidate` 是否能整除所有数。  
  2. 如果可以，统计需要删除的元素数目：所有 **严格小于 `candidate`** 的元素都必须删掉（因为它们会抢走最小值），这一步只需要一次线性计数。  
  3. 在所有可行的 `candidate` 中取最小的删除次数。  

- **时间/空间复杂度**（大白话）  
  - 时间：对每个 `candidate`（最多 `n = len(nums)`）都要遍历一遍 `numsDivide`（长度 `m`），于是 **O(n·m)**。如果 `n`、`m` 都是 10⁵，这相当于 **1 万亿次**的比较，显然会超时。  
  - 空间：只用了原数组和几个计数变量，**O(1)** 的额外空间。  

> 大多数同学在看到“遍历所有可能”时会先写出这种暴力版本，先确保思路没有错误，再去找优化点。

#### 代码（Python）

```python
from typing import List

def min_deletions_bruteforce(nums: List[int], numsDivide: List[int]) -> int:
    # 暴力：逐个尝试 nums 中的每个数作为最小值
    best = float('inf')                     # 记录最小的删除次数
    for i, cand in enumerate(nums):
        # 检查 cand 能否整除 numsDivide 中的所有数
        ok = True
        for d in numsDivide:
            if d % cand != 0:                # 只要有一个不能被整除，就不行
                ok = False
                break
        if not ok:
            continue

        # 计算需要删除的元素数目：所有比 cand 小的元素都必须删掉
        deletions = sum(1 for x in nums if x < cand)
        best = min(best, deletions)

    return -1 if best == float('inf') else best
```

#### 复杂度

- **时间复杂度**：`O(n·m)`  
  - `n` 是 `nums` 的长度，`m` 是 `numsDivide` 的长度。  
  - 用大白话说，就是“每个候选都要检查所有目标”，所以会很慢。

- **空间复杂度**：`O(1)`  
  - 只用了常数个额外变量，不随输入规模增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于每次都要遍历完整个 `numsDivide` 来判断能否整除。  
我们需要一种 **一次性** 判断“哪些整数可以整除所有 `numsDivide` 的方法”。  

**关键数学事实**：  
> 如果一个整数 `x` 能整除 `numsDivide` 中的每个数，那么 `x` 必然是 **所有数的最大公约数（GCD）** 的 **约数**。  
> 换句话说：`x` 能整除所有数  ⇔  `gcd_all % x == 0`，其中 `gcd_all` 是 `numsDivide` 的 GCD。

因此，问题可以转化为：

> 在 `nums` 中找一个最小的数 `x`，满足 `gcd_all % x == 0`，并且让我们只需要删除 **比 `x` 小的元素**。

这一步骤只需要 **一次** 计算 GCD（线性时间），随后在 `nums` 中寻找符合条件的最小数。

**实现细节**  

1. **计算 GCD**  
   - 使用欧几里得算法（`math.gcd`）两两合并，时间 `O(m)`（`m = len(numsDivide)`）。  

2. **排序 nums**  
   - 把 `nums` 按从小到大排序，这样第一次出现满足条件的数就是 **删除次数最少** 的答案。  
   - 排序耗时 `O(n log n)`，在 10⁵ 规模下完全可接受。  

3. **遍历排序后的 nums**  
   - 依次检查 `gcd_all % num == 0`。  
   - 第一次满足的下标 `i` 正好是需要删除的元素数目（因为前面 `i` 个都是更小的数，必须删掉）。  

4. **若遍历结束仍未找到**，说明没有任何数可以成为满足条件的最小值，返回 `-1`。

**类比**：  
- 把 `gcd_all` 想成一本“大字典”，里面记载了所有 `numsDivide` 的共同“根”。  
- 我们在 `nums` 里找一个“钥匙”，这把钥匙的长度必须是字典页面编号的 **约数**，才能打开所有页面。  
- 把 `nums` 排序后，从最短的钥匙开始试，第一把能开的钥匙就是我们要找的——因为更短的钥匙都打不开，删掉更短的钥匙自然是最省力的。

#### 代码（Python）

```python
import math
from typing import List

def min_deletions(nums: List[int], numsDivide: List[int]) -> int:
    """
    返回最少的删除次数，使得 nums 中的最小元素能整除 numsDivide 中的全部元素。
    若不存在则返回 -1。
    """

    # 1. 计算 numsDivide 所有数的 GCD
    g = 0
    for v in numsDivide:
        g = math.gcd(g, v)          # 逐步取两数的 GCD，最终得到整体 GCD
    # 此时任意能整除所有 numsDivide 的数，都必须是 g 的约数

    # 2. 对 nums 排序，方便一次遍历得到最小的合法候选
    nums.sort()                    # O(n log n)

    # 3. 从小到大检查是否是 g 的约数
    for i, val in enumerate(nums):
        if g % val == 0:           # val 能整除 g ⇒ val 能整除所有 numsDivide
            return i               # 前面 i 个元素（更小）全部删掉即可
    # 没有任何数满足条件
    return -1
```

#### 复杂度

- **时间复杂度**：`O(m + n log n)`  
  - `O(m)` 用于一次遍历求 GCD。  
  - `O(n log n)` 是对 `nums` 的排序。  
  - 与暴力解的 `O(n·m)` 相比，**快了几个数量级**，在 10⁵ 规模下毫秒级即可完成。

- **空间复杂度**：`O(1)`（不计排序本身的原地实现）  
  - 只用了常数个额外变量（`g`、`i`、`val`），不随输入规模增长。

---

## 心得

- **核心技巧**：利用 **最大公约数（GCD）** 将 “所有数能被同一个数整除” 的判定压缩为 “该数是 GCD 的约数”。  
- **适用题型**  
  1. “找一个数，使其能整除数组中的所有元素”——如 *Find the Smallest Divisor*。  
  2. “所有元素都满足同一个数的倍数关系”——如 *Make Array Elements Equal*（需要先求 GCD 再处理）。  
  3. “数组中选出元素，使其满足某种数论约束”——如 *Smallest Subset With GCD Greater Than One*。  
- **一句话总结解题钥匙**：**先把所有目标的共同约数算出来，再在候选里找最小的约数即可**。

---

## 反思

- **第一反应**：把每个 `nums` 的元素都当作最小值去暴力检查。  
- **最容易踩的坑**  
  - **忘记先求 GCD**，导致每次都遍历 `numsDivide`，时间爆炸。  
  - **排序后计数错误**：删除次数是 “比候选小的元素个数”，而不是 “候选出现的次数”。  
  - **整数溢出**：在某些语言中 GCD 计算要使用 64 位，但 Python 自动大整数，故不必担心。  
- **下次遇到同类题**，第一步应该思考 **“有没有一个全局的数值（如 GCD、LCM）能一次性概括所有约束？”**，再基于它进行筛选。这样往往能把指数级搜索降到线性或线性对数级。