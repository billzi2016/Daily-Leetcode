# #1250. 检查数组是否为好数组 / Check If It Is a Good Array

> 难度：困难 · 标签：Array、Math、Number Theory · [LeetCode 链接](https://leetcode.com/problems/check-if-it-is-a-good-array/)

---

## 题目（英文原版）

**Description**

Given an array nums of positive integers. Your task is to select some subset of nums, multiply each element by an integer and add all these numbers. The array is said to be good if you can obtain a sum of 1 from the array by any possible subset and multiplicand.
Return True if the array is good otherwise return False.

**Examples**

**Example 1:**

```
Input: nums = [12,5,7,23]
Output: true
Explanation: Pick numbers 5 and 7.
5*3 + 7*(-2) = 1
```

**Example 2:**

```
Input: nums = [29,6,10]
Output: true
Explanation: Pick numbers 29, 6 and 10.
29*1 + 6*(-3) + 10*(-1) = 1
```

**Example 3:**

```
Input: nums = [3,6]
Output: false
```

**Constraints**

- 1 <= nums.length <= 10^5
- 1 <= nums[i] <= 10^9

---

## 题目（中文翻译）

给定一个由正整数构成的数组 `nums`。你的任务是从 `nums` 中选择若干元素组成一个子集（subset），对每个选中的元素乘以一个整数（multiplicand），然后将这些乘积相加。若存在某个子集以及对应的整数，使得最终的和等于 `1`，则称该数组为**好数组**（good）。

如果数组是好数组，返回 `True`；否则返回 `False`。

## 示例

### 示例 1
**输入**: `nums = [12,5,7,23]`  
**输出**: `true`  
**解释**: 选取数字 `5` 和 `7`。  
`5 * 3 + 7 * (-2) = 1`

### 示例 2
**输入**: `nums = [29,6,10]`  
**输出**: `true`  
**解释**: 选取数字 `29、6、10`。  
`29 * 1 + 6 * (-3) + 10 * (-1) = 1`

### 示例 3
**输入**: `nums = [3,6]`  
**输出**: `false`

## 约束条件
- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把题目字面意思全部写出来**：

1. 从数组 `nums` 中任选一个子集（可以是 1 个、2 个，甚至全部），  
2. 给子集里的每个元素分别乘上一个 **任意整数**（正的、负的、甚至 0），  
3. 把这些乘积全部相加，看看能不能得到 **1**。

> **类比**：把数组想成一堆不同面值的硬币（只能正向或反向使用），  
> 你可以任意取几枚硬币，每枚硬币还能翻面（乘以 -1），  
> 目标是凑出面值为 1 的“钱”。  

如果遍历所有可能的子集并尝试所有整数乘数，肯定能判断答案——**因为把所有情况都试一遍就不会漏**。  

但是：

- `nums` 长度可达 `10^5`，子集的数量是 `2^n`（指数级），根本不可能枚举。  
- 对每个子集，乘数本身也是无限多（整数可以任意大），更是无解。

所以 **暴力方法虽然概念上可行，却在时间和空间上完全不可实现**。

#### 代码（Python）

下面的代码仅作“思路演示”，**不要在实际测试中运行**，会直接卡死。

```python
from itertools import combinations, product

def brute_is_good(nums):
    # 对所有子集长度进行遍历（从 1 到 len(nums)）
    for r in range(1, len(nums) + 1):
        for subset in combinations(nums, r):          # 取出一个子集
            # 为子集中的每个元素尝试若干整数乘数（这里仅取 -2,-1,0,1,2 作示例）
            # 实际上乘数的取值范围是无限的，演示用的范围根本不够
            for coeffs in product([-2, -1, 0, 1, 2], repeat=r):
                total = sum(a * b for a, b in zip(subset, coeffs))
                if total == 1:                         # 找到 1，说明是 good
                    return True
    return False
```

#### 复杂度  

- **时间复杂度**：`O(2^n * k^n)`（指数级），其中 `k` 是我们假设的乘数取值个数。  
  > 大白话：如果数组有 20 个数，`2^20` 已经是 **一百万** 级别；  
  > 再乘上每个数的乘数组合，根本不可能在几秒内算完。  
- **空间复杂度**：`O(n)` 用来存放子集和系数的临时变量，实际受限于递归栈深度。

> **结论**：暴力解只能帮助我们理清“题目到底在求什么”，但绝不能作为最终实现。

---

### 2. 最优解

#### 思路  

**从暴力解出发，找出瓶颈**：

- 暴力解的慢点在于**枚举所有子集和所有整数系数**。  
- 观察等式 `a·x + b·y = 1`（两数的线性组合），在数论里有**Bézout 引理**：  
  > 只有当 `gcd(a, b) = 1` 时，才存在整数 `x, y` 使得 `a·x + b·y = 1`。  

这条引理把“找系数”这件事转化为“求最大公约数”。  
如果我们把数组里 **所有数的最大公约数** 记作 `g`，则：

- 若 `g = 1`，说明 **至少存在** 一组整数系数（不一定是正数）使得线性组合得到 1。  
- 若 `g > 1`，则任何整数线性组合的结果都一定是 `g` 的倍数，根本不可能得到 1。

**关键点**：**数组是否 good，只和所有元素的 GCD 是否为 1 有关**，与子集、系数的具体取法无关。

> **类比**：想象每个数都是一根不同长度的木棍，只有当所有木棍的长度没有共同的“最小公因子”时，才能用它们拼出长度为 1 的小段。

**如何求 GCD**：

- 两个数的 GCD 可以用欧几里得算法（辗转相除）在 `O(log min(a,b))` 时间求出。  
- 多个数的 GCD 只需要把前两个的 GCD 再和第三个求 GCD，依此类推，**一次遍历即可**。

**步骤**：

1. 初始化 `g = nums[0]`。  
2. 依次遍历数组的其余元素 `num`，把 `g = gcd(g, num)` 更新。  
3. 循环结束后检查 `g == 1`，返回相应布尔值。

#### 代码（Python）

```python
import math
from typing import List

def isGoodArray(nums: List[int]) -> bool:
    """
    判断数组是否为 good
    思路：若所有数的最大公约数 (gcd) 为 1，则一定可以通过整数线性组合得到 1。
    """
    # 1. 取第一个数作为初始 gcd
    g = nums[0]                     # 初始 gcd

    # 2. 依次与后面的数取 gcd，逐步缩小
    for num in nums[1:]:
        g = math.gcd(g, num)        # math.gcd 是欧几里得算法的实现
        # 只要 g 已经降到 1，就不必继续了，后面再和别的数取 gcd 也会保持 1
        if g == 1:
            break

    # 3. g 为 1 表示可以得到 1，返回 True；否则返回 False
    return g == 1
```

#### 复杂度  

- **时间复杂度**：`O(n * log M)`，其中 `n = len(nums)`，`M` 是数组中最大数的大小。  
  - 大白话：我们只遍历一次数组（`n` 次），每次求 gcd 的代价相当于 “把两个数不停地除”，最多 `log` 级别的步骤。  
  - 在最坏情况下（比如所有数都是 `10^9`），`log M` 约为 30，基本可以视作常数。  
- **空间复杂度**：`O(1)`，只用了几个整数变量，不随输入规模增长。

> 与暴力解相比，时间从 **指数级** 降到 **线性**，空间也从 **线性** 降到 **常数**，完全可以接受。

---

## 心得

- **核心技巧**：**Bézout 引理 + 求数组 GCD**。  
- 这种“把线性组合转化为 GCD 判定”的思路在数论题里非常常见，尤其是涉及“能否表示为 1（或其他整数）”的问题。  
- **相似题型**：
  1. *LC 1979. Find Greatest Common Divisor of Array*（直接求 GCD）。  
  2. *LC 1250. Check If It Is a Good Array*（本题）。  
  3. *LC 2034. Partition Array Into Two Arrays With Equal Sum*（需要判断能否用子集和表示特定值，常用 GCD/DP）。

> **一句话总结解题钥匙**：**只要所有数的最大公约数是 1，就一定能用整数线性组合得到 1**。

---

## 反思

- **第一反应**：看到“子集 + 任意整数乘数”，本能想枚举子集并搜索系数——这正是暴力思路。  
- **最容易踩的坑**：
  - 误以为只要出现 `1` 就一定 good，忽视了负系数的作用。  
  - 忽略了 **Bézout 引理**，导致没有发现 GCD 与答案的直接联系。  
  - 没有提前考虑 **时间限制**（`10^5` 长度），导致尝试了不可行的枚举。  
- **下次类似题**：  
  1. **先停下来，问自己**：是否有数学定理可以把“组合”问题转化为“公因数”或“同余”等更易判断的形式？  
  2. **检查极端约束**（数组长度、数值范围），判断暴力是否真的不可行。  
  3. **从最小案例出发**（两个数），验证 Bézout 或其他数论结论，再推广到多数。