# #1362. 最近的因子 / Closest Divisors

> 难度：中等 · 标签：Math · [LeetCode 链接](https://leetcode.com/problems/closest-divisors/)

---

## 题目（英文原版）

**Description**

Given an integer num, find the closest two integers in absolute difference whose product equals num + 1 or num + 2.
Return the two integers in any order.

**Examples**

**Example 1:**

```
Input: num = 8
Output: [3,3]
Explanation: For num + 1 = 9, the closest divisors are 3 & 3, for num + 2 = 10, the closest divisors are 2 & 5, hence 3 & 3 is chosen.
```

**Example 2:**

```
Input: num = 123
Output: [5,25]
```

**Example 3:**

```
Input: num = 999
Output: [40,25]
```

**Constraints**

- 1 <= num <= 10^9

---

## 题目（中文翻译）

给定一个整数 `num`，找到绝对差最小的两个整数，使它们的乘积等于 `num + 1` 或 `num + 2`。返回这两个整数，顺序不限。

**示例 1**  
**输入**: `num = 8`  
**输出**: `[3,3]`  
**解释**: 对于 `num + 1 = 9`，最接近的因子（divisors）是 `3` 与 `3`；对于 `num + 2 = 10`，最接近的因子是 `2` 与 `5`，因此选择 `3` 与 `3`。

**示例 2**  
**输入**: `num = 123`  
**输出**: `[5,25]`

**示例 3**  
**输入**: `num = 999`  
**输出**: `[40,25]`

**约束条件**  
- `1 <= num <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：  
1. 先把 `num+1` 和 `num+2` 两个数都列出来。  
2. 对每个数，从 **1** 开始枚举所有可能的因子 `a`，把 `b = target // a`（如果 `a` 能整除 `target`）作为另一因子。  
3. 记录下每一对因子 `(a, b)` 的绝对差 `|a-b|`，找出差值最小的那一对即可。

> **生活化类比**：把 “因子” 想成 **拼图块**，我们要把一块数字 `target` 拆成两块 `a` 与 `b`，要求这两块大小尽可能接近。  
> 暴力解相当于把 **每一块都尝试一次**，就像把所有拼图块都搬到桌面上逐个比对，最慢但最可靠。

**为什么正确**：  
只要遍历了 **所有** 能整除 `target` 的 `a`，我们就不会漏掉任何合法的因子对。于是最小差值一定会在遍历过程中被发现。

**时间/空间分析**（大白话）  
- 暴力解会从 `1` 检查到 `target` 本身（`target = num+2` 最大），也就是 **检查 `target` 次**。如果 `target` 是 10⁹，检查 10⁹ 次显然太慢。  
- 时间复杂度记作 **O(target)**，这里的 `O` 只是一种 “数量级” 的标记，意思是“随 `target` 增大，运行时间几乎线性增长”。  
- 只用了常数级的变量 (`a, b, best_diff, answer`)，所以空间复杂度是 **O(1)**（不随输入大小增长）。

#### 代码（Python）

```python
import math
from typing import List

def closestDivisors_bruteforce(num: int) -> List[int]:
    # 目标是 num+1 或 num+2
    candidates = [num + 1, num + 2]
    best_pair = [1, candidates[0]]   # 先随便放一对，差值很大
    best_diff = abs(best_pair[0] - best_pair[1])

    for target in candidates:                # 两个数都要检查
        for a in range(1, target + 1):       # 暴力枚举 1~target
            if target % a == 0:              # a 能整除 target，才是合法因子
                b = target // a
                diff = abs(a - b)
                if diff < best_diff:         # 找到更接近的因子对
                    best_diff = diff
                    best_pair = [a, b]
    return best_pair
```

#### 复杂度

- **时间复杂度**：`O(num)`（因为 `target ≤ num+2`，最坏情况下要遍历到 `num+2` 次）  
  → 大白话：如果 `num` 是 1000，程序大概会跑 1000 次循环；如果是 10⁹，就会跑 10⁹ 次，几乎不可接受。  
- **空间复杂度**：`O(1)`，只用了几个变量，和输入规模无关。

---

### 2. 最优解

#### 思路  
从暴力解可以看到 **瓶颈** 在于我们遍历了太多不可能的 `a`（从 1 到 `target`）。  
实际上，**如果 `a` 是因子，必然有 `a ≤ sqrt(target)`**，因为一旦 `a` 超过平方根，另一因子 `b = target / a` 就会小于平方根，已经在前面遍历过了。  

**关键点**：只需要检查到 `√target`，就能把所有因子对都找齐。  

步骤如下：

1. 同样准备 `target1 = num+1`、`target2 = num+2`。  
2. 对每个 `target`，从 `int(sqrt(target))` 向下递减（**从大到小**），因为我们想要两个因子尽可能接近，最先找到的那对（`i` 与 `target//i`）往往差值最小。  
3. 第一次出现 `target % i == 0` 时，`i` 与 `target//i` 就是**最接近的因子对**，立刻返回。  
4. 对两个 `target` 分别得到最接近的因子对，比较它们的差值，挑选差值更小的那一对返回。

> **类比**：想象你在找两块大小最相近的拼图块。先把大块的尺寸（平方根）算出来，然后从这个尺寸往下找，第一次能拼合成功的两块，就是最接近的组合，后面再往下找只会让差距更大。

**为什么只检查到 sqrt**：  
设 `a ≤ b`，且 `a * b = target`。如果 `a > sqrt(target)`，则 `b = target / a < sqrt(target)`，这意味着我们已经在检查 `b` 时发现了这对因子。因此只检查到 sqrt 已经覆盖了所有可能的配对。

#### 代码（Python）

```python
import math
from typing import List

def closestDivisors(num: int) -> List[int]:
    """
    返回 num+1 或 num+2 的因子对，使得两数差值最小。
    思路：只遍历到 sqrt(target)，从 sqrt 往下找，第一次整除即是最接近的因子对。
    """
    def nearest_pair(target: int) -> List[int]:
        # 从 sqrt(target) 开始往下找
        i = int(math.isqrt(target))          # math.isqrt 返回整数平方根，避免浮点误差
        while i >= 1:
            if target % i == 0:              # 找到合法因子
                return [i, target // i]      # 这就是差值最小的一对
            i -= 1
        # 理论上永远不会走到这里，因为 1 总是因子
        return [1, target]

    # 分别求 num+1 和 num+2 的最近因子对
    pair1 = nearest_pair(num + 1)
    pair2 = nearest_pair(num + 2)

    # 计算两对的差值，返回差值更小的那一对
    diff1 = abs(pair1[0] - pair1[1])
    diff2 = abs(pair2[0] - pair2[1])
    return pair1 if diff1 <= diff2 else pair2
```

#### 复杂度

- **时间复杂度**：`O(√num)`  
  - 解释：我们最多只遍历到 `sqrt(num+2)`，即约 `31623` 次（当 `num = 10⁹` 时）。这比暴力的 `10⁹` 次少了 **四位数级别的量级**，几乎是瞬间完成。  
  - 与暴力解对比：从“每次都要跑到 `num` 次”降到“每次只跑到 `√num` 次”，提升巨大。

- **空间复杂度**：`O(1)`  
  - 只用了常数个局部变量，和输入大小无关。

---

## 心得

- **核心技巧**：利用**平方根剪枝**（只枚举到 `√target`）并**从大到小搜索**，即可在 O(√n) 时间内找到最接近的因子对。  
- **适用场景**  
  1. **寻找整数的因子**（如 LeetCode 1979. Find Greatest Common Divisor of Array）  
  2. **最小化差值的配对问题**（如 1492. The kth Factor of n）  
  3. **需要判断是否存在某种乘积关系的题目**（如 2520. Count the Number of Pairs With Absolute Difference K）  

- **一句话总结解题钥匙**：**“只检查到平方根，先找最大的可能因子，就能直接得到差值最小的配对”。**

---

## 反思

- **第一反应**：直接把 `num+1`、`num+2` 的所有因子枚举出来，找差值最小的那一对。  
- **最容易踩的坑**  
  - **遍历范围过大**：忘记 `√target` 的剪枝，导致超时。  
  - **整数平方根的精度**：使用 `math.sqrt` 得到浮点数再转 `int` 可能出现 1.999999 → 1 的错误，推荐 `math.isqrt`（整数平方根）安全可靠。  
  - **返回顺序**：题目要求“任意顺序”，但要保证返回的是两个整数而不是列表的引用错误。  
- **下次遇到同类题**：第一步立刻想到“**只需要检查到 sqrt**”，并且**从 sqrt 往下找**，因为这一步几乎可以把所有 “因子配对、最小差值” 的问题一次性解决。