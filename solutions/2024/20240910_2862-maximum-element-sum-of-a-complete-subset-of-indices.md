# #2862. 完整索引子集的最大元素和 / Maximum Element-Sum of a Complete Subset of Indices

> 难度：困难 · 标签：Array、Math、Number Theory · [LeetCode 链接](https://leetcode.com/problems/maximum-element-sum-of-a-complete-subset-of-indices/)

---

## 题目（英文原版）

**Description**

You are given a 1-indexed array nums. Your task is to select a complete subset from nums where every pair of selected indices multiplied is a perfect square,. i. e. if you select ai and aj, i * j must be a perfect square.
Return the sum of the complete subset with the maximum sum.

**Examples**

**Example 1:**

```
Input: nums = [8,7,3,5,7,2,4,9]
Output: 16
Explanation:
We select elements at indices 2 and 8 and 2 * 8 is a perfect square.
```

**Example 2:**

```
Input: nums = [8,10,3,8,1,13,7,9,4]
Output: 20
Explanation:
We select elements at indices 1, 4, and 9. 1 * 4 , 1 * 9 , 4 * 9 are perfect squares.
```

**Constraints**

- 1 <= n == nums.length <= 104
- 1 <= nums[i] <= 109

---

## 题目（中文翻译）

你得到一个 **1-indexed**（从 1 开始索引）的数组 `nums`。请从中挑选一个 **完整子集（complete subset）**，满足任意两个被选中的下标相乘都是 **完全平方数（perfect square）**——即若选择了下标 `i` 和 `j`，则 `i * j` 必须是完全平方数。返回所有满足条件的完整子集中，元素和最大的那个的和。

**示例 1**

```text
Input: nums = [8,7,3,5,7,2,4,9]
Output: 16
Explanation:
我们选择下标为 2 和 8 的元素，2 * 8 = 16 是完全平方数。
```

**示例 2**

```text
Input: nums = [8,10,3,8,1,13,7,9,4]
Output: 20
Explanation:
我们选择下标为 1、4、9 的元素。1 * 4、1 * 9、4 * 9 都是完全平方数。
```

**约束条件**

- `1 <= n == nums.length <= 10^4`
- `1 <= nums[i] <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**把所有可能的下标子集都枚举一遍**，然后检查子集里任意两两下标的乘积是否是完全平方数。  
如果满足条件，就把对应的 `nums` 元素相加，记录下最大的和。  

- **数据结构**：我们只需要一个数组 `nums`，以及若干个 `list`（或 `set`）来存放当前正在尝试的下标集合。  
- **生活化类比**：把每个下标想成一张卡片，暴力解就是把所有卡片随意组合成小堆，逐个检查每堆里两张卡片的“乘积是否是完美正方形”。  
- **正确性**：因为我们遍历了**所有**可能的子集，只要有一个子集满足题目要求，必定会被检测到并计算其和，所以最终的最大和一定是正确的。  

#### 代码（Python）

```python
from itertools import combinations
import math

def is_perfect_square(x: int) -> bool:
    """判断 x 是否为完全平方数（根号取整后再平方等于 x）"""
    r = int(math.isqrt(x))
    return r * r == x

def max_sum_bruteforce(nums):
    n = len(nums)                     # nums 是 0-index 的，题目说 1-index，下面会把下标 +1
    best = 0

    # 枚举子集的大小，从 1 到 n
    for size in range(1, n + 1):
        # 组合出所有 size 大小的下标集合（下标从 0 开始）
        for idx_tuple in combinations(range(n), size):
            ok = True
            # 检查任意两两下标乘积是否是完全平方数
            for i in range(size):
                for j in range(i + 1, size):
                    idx_i = idx_tuple[i] + 1   # 题目下标从 1 开始
                    idx_j = idx_tuple[j] + 1
                    if not is_perfect_square(idx_i * idx_j):
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                cur_sum = sum(nums[k] for k in idx_tuple)
                best = max(best, cur_sum)
    return best
```

> 关键行中文注释已写在代码里。  

#### 复杂度  

- **时间复杂度**：  
  枚举所有子集的复杂度是 `O(2^n)`（因为每个元素可以选或不选），  
  对每个子集还要检查 `size^2` 次两两乘积，最坏情况下是 `O(n^2)`。  
  所以整体是 **指数级**，在 `n=10^4` 时根本不可行。  
  用大白话说，这相当于让你在 1 天里尝遍所有 10,000 位数的所有可能排列，显然不可能完成。  

- **空间复杂度**：  
  只用了常数级的额外空间 `O(1)`（递归栈、临时变量），但因为要存下所有子集的组合，实际会占用大量内存，最坏也是 `O(2^n)`。  

> 暴力解的目的仅在于帮助我们**发现问题的本质**——下标之间的约束可以用数学方式简化，从而得到更快的算法。  

---  

### 2. 最优解  

#### 思路  

**从暴力解出发**，我们注意到：  
- 判断两个下标 `i` 与 `j` 是否可以同在一个子集，只需要检查 `i * j` 是否是完全平方数。  
- 直接计算 `i * j` 的平方根会很慢，而且我们要对所有配对检查，这仍然是 `O(n^2)`。

**关键观察**：  
把整数的质因数分解写成  
```
x = p1^a1 * p2^a2 * ... * pk^ak
```
如果把所有指数为 **奇数** 的质因子乘起来，得到的数记作 `P(x)`，称为 **x 的平方自由核**（square‑free kernel）。  

- **性质**：`i * j` 是完全平方数 ⇔ `P(i) == P(j)`。  
  - 解释：`i * j` 的质因数指数是 `ai + aj`。要让每个指数都是偶数，必须保证在 `i` 与 `j` 中出现奇数次的质因子是完全相同的，也就是它们的奇指数集合相同，等价于 `P(i) = P(j)`。  

因此，**所有满足题目要求的下标必须拥有相同的 `P(i)`**。这把原本的“任意两两配对检查”问题，转化为：

> **把下标按照 `P(i)` 分组**，同一组内的下标两两乘积必然是完全平方数。  
> **在每一组里**，把对应的 `nums` 值相加，取最大和即可。

所以算法步骤如下：

1. **预处理**：用线性筛或最小质因数（SPF）数组在 `O(n log log n)` 时间内得到每个 `i (1 … n)` 的 `P(i)`。  
2. **分组求和**：遍历 `i = 1 … n`，把 `nums[i‑1]` 加到 `group_sum[P(i)]` 中。  
3. **答案**：返回 `group_sum` 中的最大值。

#### 关键工具：最小质因数（SPF）  

- SPF[i] = i 的最小质因数。  
- 通过 SPF 可以在 `O(log i)` 时间内快速分解 `i`，只需要遍历它的因子并计数奇偶性。  

#### 代码（Python）

```python
import math
from collections import defaultdict

def smallest_prime_factors(limit: int):
    """线性筛，返回 0..limit 的最小质因数数组（spf[0]=spf[1]=1）"""
    spf = [0] * (limit + 1)
    spf[0] = spf[1] = 1
    primes = []
    for i in range(2, limit + 1):
        if spf[i] == 0:               # i 是质数
            spf[i] = i
            primes.append(i)
        # 用已知的质数更新后续数的最小质因数
        for p in primes:
            if p > spf[i] or i * p > limit:
                break
            spf[i * p] = p
    return spf

def square_free_kernel(x: int, spf):
    """
    计算 P(x)：把所有出现奇数次的质因子乘起来。
    通过 spf（最小质因数表）快速分解。
    """
    res = 1
    while x > 1:
        p = spf[x]          # 当前最小质因数
        cnt = 0
        while x % p == 0:
            x //= p
            cnt += 1
        if cnt % 2 == 1:    # 出现奇数次，就保留这个质因子
            res *= p
    return res

def max_sum_complete_subset(nums):
    """
    主函数：返回满足 “任意两下标乘积为完全平方数” 的完整子集的最大元素和。
    """
    n = len(nums)                     # nums 长度即下标最大值（1-index）
    spf = smallest_prime_factors(n)   # 预处理最小质因数

    group_sum = defaultdict(int)      # key = P(i)，value = 该组的 nums 和

    for i in range(1, n + 1):         # 下标从 1 开始遍历
        p = square_free_kernel(i, spf)   # 计算 P(i)
        group_sum[p] += nums[i - 1]       # 把对应的 nums 加入该组

    # 取最大组和即为答案
    return max(group_sum.values())
```

**代码说明（关键行中文注释）**  

- `smallest_prime_factors`：利用线性筛一次遍历得到每个整数的最小质因数，后面分解时只需要不停除以最小质因数即可。  
- `square_free_kernel`：循环除去相同的质因数，记录出现的次数 `cnt`，如果 `cnt` 为奇数，则把该质因子乘进结果 `res`。  
- 主循环 `for i in range(1, n + 1)`：对每个下标计算它的 `P(i)`，然后把对应的 `nums[i-1]` 加到同一 `P` 的组里。  
- `max(group_sum.values())`：所有合法组的和里取最大的，就是题目要求的最大和。  

#### 复杂度  

- **时间复杂度**：  
  1. 线性筛构造 SPF：`O(n)`（常数因子稍大但仍线性）。  
  2. 对每个 `i` 计算 `P(i)`：每次除以最小质因数，最多 `O(log i)` 步，累计 `O(n log n)`，在 `n ≤ 10^4` 下几乎可以视为 `O(n)`。  
  3. 分组求和和取最大：`O(n)`。  
  综合下来 **总体是 `O(n log n)`，在本题规模下约等于线性 `O(n)`**。  

  与暴力解的指数级 `O(2^n)` 相比，快了天壤之别——相当于把原来要用几天甚至几年的“穷举”，压缩到几毫秒完成。  

- **空间复杂度**：  
  - SPF 数组占 `O(n)` 空间。  
  - `group_sum` 最多保存 `n` 个不同的 `P(i)`（实际上远少于 `n`），也是 `O(n)`。  
  整体 **`O(n)`**，即与输入规模线性相关。  

---

## 心得  

- **核心技巧**：把 “乘积为完全平方数” 转化为 **下标的平方自由核相等**（`P(i) = P(j)`），从而把两两约束化为 **同一组** 的约束。  
- **该技巧适用的题型**：  
  1. “下标乘积为完全平方数” 或 “下标乘积为完全立方数”等，需要判断乘积的奇偶指数的题目。  
  2. “把元素按某种等价关系分组，求每组的最大/最小/和”等聚合类问题（如 LeetCode 1513 “Number of Substrings With Only 1s” 中的连续段分组）。  
  3. “利用数的平方自由核进行去重” 的数论题目，例如 “最小删除使数组中所有数两两乘积为完全平方”。  

- **一句话总结解题钥匙**：  
  **“把乘积是否为完全平方的判断，转化为下标的平方自由核是否相等，从而只需做一次哈希分组”。**  

---

## 反思  

- **拿到题目第一反应**：想到要检查所有下标对的乘积是否是完全平方，第一时间想到**枚举**或**两层循环**。  
- **最容易踩的坑**：  
  1. **忽视 1‑index 与 0‑index 的差异**：在代码实现时容易把下标当成 0‑based，导致 `P(i)` 计算错误。  
  2. **平方自由核的定义不清晰**：如果只记下“奇数次出现的质因子”，而忘记把它们相乘得到唯一的整数 `P(i)`，会导致哈希冲突。  
  3. **大数溢出**：`i` 的平方自由核本身不会超过 `i`（因为只乘奇数次的质因子），但如果直接用 `i*j` 检查是否为完全平方，会产生 `i*j` 超过 64 位整数的风险。  

- **下次遇到同类题的第一步**：  
  **先把约束转化为等价的“等价关系”**（如 `P(i) = P(j)`），再把问题归结为“在同一等价类中取最大和”。这样可以立刻从指数级搜索跳到线性/对数级聚合。