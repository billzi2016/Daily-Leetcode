# #2584. 分割数组以使乘积互质 / Split the Array to Make Coprime Products

> 难度：困难 · 标签：Array、Hash Table、Math、Number Theory · [LeetCode 链接](https://leetcode.com/problems/split-the-array-to-make-coprime-products/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums of length n.
A split at an index i where 0 <= i <= n - 2 is called valid if the product of the first i + 1 elements and the product of the remaining elements are coprime.
Return the smallest index i at which the array can be split validly or -1 if there is no such split.
Two values val1 and val2 are coprime if gcd(val1, val2) == 1 where gcd(val1, val2) is the greatest common divisor of val1 and val2.

**Examples**

**Example 1:**

```
Input: nums = [4,7,8,15,3,5]
Output: 2
Explanation: The table above shows the values of the product of the first i + 1 elements, the remaining elements, and their gcd at each index i.
The only valid split is at index 2.
```

**Example 2:**

```
Input: nums = [4,7,15,8,3,5]
Output: -1
Explanation: The table above shows the values of the product of the first i + 1 elements, the remaining elements, and their gcd at each index i.
There is no valid split.
```

**Constraints**

- n == nums.length
- 1 <= n <= 104
- 1 <= nums[i] <= 106

---

## 题目（中文翻译）

给定一个下标从 **0** 开始的整数数组 `nums`，长度为 `n`。  
若在下标 `i`（`0 <= i <= n - 2`）处进行分割（**split**），使得前 `i + 1` 个元素的乘积 **product** 与剩余元素的乘积 **product** 互质（**coprime**），则该分割称为 **有效**（**valid**）。  

返回能够进行有效分割的最小下标 `i`，如果不存在这样的分割，返回 `-1`。  

两个数 `val1` 与 `val2` 若满足 `gcd(val1, val2) == 1`，则称它们互质，其中 `gcd(val1, val2)` 为 **最大公约数**（**greatest common divisor**）。

---

### 示例

**示例 1**  
```
Input: nums = [4,7,8,15,3,5]
Output: 2
Explanation: 上表展示了每个下标 `i` 处，前 `i + 1` 个元素的乘积、剩余元素的乘积以及它们的 gcd。唯一的有效分割出现在下标 2。
```

**示例 2**  
```
Input: nums = [4,7,15,8,3,5]
Output: -1
Explanation: 上表展示了每个下标 `i` 处，前 `i + 1` 个元素的乘积、剩余元素的乘积以及它们的 gcd。不存在有效分割。
```

---

### 约束条件

- `n == nums.length`
- `1 <= n <= 10^4`
- `1 <= nums[i] <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每个可能的切分点都算一遍**：

1. 从左到右枚举切分位置 `i`（`0 ≤ i ≤ n‑2`）。  
2. 计算左半段 `nums[0..i]` 的所有元素的乘积 `left_prod`，以及右半段 `nums[i+1..n‑1]` 的乘积 `right_prod`。  
3. 用欧几里得算法求 `gcd(left_prod, right_prod)`，如果等于 `1`，说明两段的乘积互质，返回当前 `i`。  

> **类比**：把数组想象成一串珠子，左边的珠子全拴在一起形成一个“大球”，右边的珠子拴成另一个“大球”。我们把两球的“重量”（乘积）拿去比较，看看它们有没有共同的“因子”（质因子）。如果没有共同因子，它们就是互质的。

**为什么能得到正确答案**：  
因为我们穷举了所有合法的切分点，只要有一个切分点满足条件，必然会在遍历过程中被发现；如果没有，则遍历结束后返回 `-1`。

**时间/空间分析（大白话）**：

- 对每个切分点都要重新算左边和右边的乘积。  
  - 第 1 次算 1 个数，  
  - 第 2 次算 2 个数， …，  
  - 第 `n‑1` 次算 `n‑1` 个数。  
  - 这相当于把 `1 + 2 + … + (n‑1)` 这些数都加了一遍，等于 `n·(n‑1)/2`，也就是 **O(n²)** 的时间。  
- 只用到几个临时变量存乘积和 `gcd`，不需要额外的数组，**O(1)** 的空间。

#### 代码（Python）

```python
from math import gcd
from typing import List

def splitArray(nums: List[int]) -> int:
    n = len(nums)
    # 枚举所有可能的切分点 i
    for i in range(n - 1):
        # 计算左半段乘积
        left_prod = 1
        for j in range(i + 1):
            left_prod *= nums[j]

        # 计算右半段乘积
        right_prod = 1
        for j in range(i + 1, n):
            right_prod *= nums[j]

        # 判断是否互质
        if gcd(left_prod, right_prod) == 1:
            return i          # 找到最左边的合法切分点
    return -1                 # 没有合法切分点
```

> **注意**：Python 的整数是「大整数」(`bigint`)，理论上可以存放任意大的乘积，但实际运行时乘法和 `gcd` 的代价会随数字位数指数增长，导致这段代码在 `n≈10⁴、nums[i]≈10⁶` 时几乎会超时。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  > 想象一下，学生排队买饭，每个人都要从头数到自己前面的人数，总共要数 `1+2+…+n` 次，和 `n²/2` 同阶。
- **空间复杂度**：`O(1)`  
  > 只用了几个临时变量，和数组大小无关。

---

### 2. 最优解

#### 思路  

暴力解慢的根源在于**每次都要重新算乘积**。  
观察乘积的本质：  

- 两个数的乘积互质 ⇔ 它们**没有共同的质因子**。  
- 因此我们不必真的去算乘积，只要知道每一段里出现了哪些**质因子**，以及它们是否同时出现在左、右两段，就能判断是否互质。

**关键点**：  
如果某个质因子在左段出现了，它**不能再出现在右段**；否则左、右乘积会共享这个质因子，`gcd` > 1。

**步骤概览**  

1. **预处理**：遍历整个数组，对每个元素进行**质因数分解**（把它写成若干个质数的乘积）。  
   - 对每个出现的质数 `p`，记录它在数组中**最右侧出现的下标** `last[p]`。  
   - 这里的「最右侧」是指该质数在数组里出现的最靠后的位置。  

2. **扫描左段**：再次从左到右遍历数组，维护一个变量 `max_last`，表示**已经看到的所有质数的最右出现位置的最大值**。  
   - 当遍历到下标 `i` 时，`max_last` 就是「左侧所有质数在数组中最右出现位置」的最大值。  

3. **判断切分**：如果当前下标 `i` **已经不小于** `max_last`（即 `i >= max_last`），说明左侧出现的每个质数在右侧都已经「走完」了——右侧不再出现这些质数，左、右乘积必然互质。  
   - 第一个满足 `i >= max_last` 的 `i` 就是答案。  

4. 如果遍历完都没有找到合法切分，返回 `-1`。

> **类比**：把每个质因子想象成一种颜色的贴纸，`last[p]` 记录了这种颜色贴纸最后一次贴在第几块砖上。我们从左往右搬砖，当搬到第 `i` 块时，如果已经搬过的所有颜色的最后一块贴纸都已经在左边（`i` 已经到了或超过了它们的最右位置），那么左边的砖块和右边的砖块就没有共同颜色，能够「安全分开」。

**质因数分解的实现**（对 `num ≤ 10⁶`）  
- 直接遍历从 `2` 到 `√num` 的整数尝试除尽，复杂度约 `O(√num)`。  
- 由于 `num ≤ 10⁶`，`√num ≤ 1000`，在本题约束下完全可接受。

#### 代码（Python）

```python
from typing import List
import math

def splitArray(nums: List[int]) -> int:
    n = len(nums)

    # 1. 记录每个质因子最后出现的下标
    last = {}                     # key: 质因子，value: 最右下标

    for idx, val in enumerate(nums):
        x = val
        d = 2
        while d * d <= x:         # 试除到 sqrt(x)
            if x % d == 0:
                # d 是一个质因子
                last[d] = idx      # 记录最新出现位置
                while x % d == 0:  # 去掉所有相同的 d
                    x //= d
            d += 1 if d == 2 else 2   # 2 之后只检查奇数
        if x > 1:                  # 剩下的 x 本身是质数
            last[x] = idx

    # 2. 从左到右扫描，维护已经出现质因子的最右下标的最大值
    max_last = -1                  # 初始没有质因子
    for i, val in enumerate(nums):
        x = val
        d = 2
        while d * d <= x:
            if x % d == 0:
                max_last = max(max_last, last[d])   # 更新最大右端
                while x % d == 0:
                    x //= d
            d += 1 if d == 2 else 2
        if x > 1:
            max_last = max(max_last, last[x])

        # 只检查到 n-2，最后一块不需要再划分
        if i < n - 1 and i >= max_last:
            return i               # 找到最左边合法切分点

    return -1                      # 没有合法切分
```

**代码要点解释**  

- `last`：类似字典（哈希表），把「质因子 → 最右出现位置」存进去，查找和写入都是 `O(1)`。  
- `while d * d <= x`：只需要试除到平方根，因为若 `x` 有因子大于 `√x`，另一个因子必然小于 `√x`。  
- `d += 1 if d == 2 else 2`：先检查 `2`，之后只检查奇数，省去偶数的无用尝试。  
- `max_last = max(max_last, last[p])`：把左侧已经看到的所有质因子的最右出现位置取最大，确保左侧的每个质因子在右侧都不再出现。  

#### 复杂度

- **时间复杂度**：`O(n * √M)`，其中 `M = max(nums[i]) ≤ 10⁶`。  
  - 对每个元素进行一次质因数分解，最多尝试到 `√M ≈ 1000` 次。  
  - 对比暴力的 `O(n²)`，这相当于把「数千次乘法」换成「千次除法」，在 `n ≤ 10⁴` 时非常快。  

- **空间复杂度**：`O(K)`，`K` 为所有不同质因子的数量。  
  - 最坏情况下 `K` 不会超过 `π(10⁶) ≈ 78 498`（所有小于等于 10⁶ 的质数），在本题的约束下仍然是可接受的。  
  - 实际上因为每个数最多只有 ~7 个不同质因子，`K` 通常远小于 `n`。

---

## 心得

- **核心技巧**：**把“乘积互质”转化为“质因子不重叠”**，利用哈希表记录每个质因子的最右出现位置，再用一次线性扫描找分界点。  
- **适用的题型**  
  1. 判断两个子数组的乘积是否互质（本题的变体）。  
  2. 把数组划分成若干段，使得每段的元素集合互不共享质因子（如 LeetCode 2407 “Longest Subarray With Fixed Sum” 的质因子版）。  
  3. 需要快速判断区间内是否存在公共质因子的查询题（如 “Range GCD Queries” 的质因子版）。  

- **一句话总结**：  
  “只要把质因子当成‘颜色’，确保左侧颜色不再出现在右侧，就能把乘积互质的问题简化为一次线性扫描。”

---

## 反思

- **第一反应**：直接计算左、右乘积再求 `gcd`，因为乘积是最直观的“数值”。  
- **最容易踩的坑**  
  - **整数溢出/超大乘积**：在语言不支持大整数时会直接溢出。  
  - **质因子重复**：同一个质因子在同一个数里出现多次，只需要记录一次即可，否则会误把 `max_last` 拉得更远。  
  - **边界条件**：只能在 `0 ≤ i ≤ n‑2` 处切分，记得在循环里排除最后一个位置。  
- **下次遇到同类题**：第一步先思考“**是否可以用质因子（或其他离散特征）代替大数运算**”，再决定是否需要预处理（哈希表、前缀信息）来实现 **O(n)** 或 **O(n log n)** 的解法。