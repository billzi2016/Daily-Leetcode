# #3618. 按素数下标拆分数组 / Split Array by Prime Indices

> 难度：中等 · 标签：Array、Math、Number Theory · [LeetCode 链接](https://leetcode.com/problems/split-array-by-prime-indices/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums.
Split nums into two arrays A and B using the following rule:
Return the absolute difference between the sums of the two arrays: |sum(A) - sum(B)|.
Note: An empty array has a sum of 0.

**Examples**

**Example 1:**

```
Input: nums = [2,3,4]
Output: 1
Explanation:
```

**Example 2:**

```
Input: nums = [-1,5,7,0]
Output: 3
Explanation:
```

**Constraints**

- 1 <= nums.length <= 105
- -109 <= nums[i] <= 109

---

## 题目（中文翻译）

你得到一个整数数组 `nums`。  
按照如下规则将 `nums` 拆分为两个数组 **A** 和 **B**：  
返回这两个数组元素和的绝对差值：`|sum(A) - sum(B)|`。  
> 注意：空数组的和为 0。

**示例 1**  
输入：`nums = [2,3,4]`  
输出：`1`  
解释：

**示例 2**  
输入：`nums = [-1,5,7,0]`  
输出：`3`  
解释：

**约束条件**  
- `1 <= nums.length <= 10^5`  
- `-10^9 <= nums[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目要求把下标是**质数**的元素放进数组 `A`，其余下标的元素放进数组 `B`，最后返回 `|sum(A) - sum(B)|`。  
最直接的想法就是：

1. 从 `0` 到 `len(nums)-1` 逐个遍历下标 `i`。  
2. 对每个 `i` 判断它是不是质数（质数：只能被 `1` 和它本身整除的正整数，且大于 `1`）。  
3. 如果 `i` 是质数，就把 `nums[i]` 加到 `sumA`；否则加到 `sumB`。  
4. 循环结束后返回 `abs(sumA - sumB)`。

> **类比**：判断下标是否是质数，就像在字典里查单词是否存在一样——我们要逐个“翻页”，把每个下标和 `2…i-1` 的所有数都比较一次。

这个方法之所以**正确**，是因为我们严格按照题目给出的划分规则把每个元素分配到了对应的集合，最后再用绝对值算差。

#### 代码（Python）

```python
def splitArrayByPrimeIndices(nums):
    # ---------- 暴力版 ----------
    def is_prime(x: int) -> bool:
        """判断 x 是否为质数（暴力检查）"""
        if x < 2:               # 0、1 不是质数
            return False
        # 只要能被 2~x-1 整除，就不是质数
        for d in range(2, x):
            if x % d == 0:
                return False
        return True

    sumA, sumB = 0, 0
    for i, val in enumerate(nums):
        if is_prime(i):          # 如果下标 i 是质数
            sumA += val          # 加到 A 的和
        else:
            sumB += val          # 加到 B 的和
    return abs(sumA - sumB)      # 绝对差
```

#### 复杂度

- **时间复杂度**：`O(n * n)`（这里记作 `O(n²)`）  
  - 外层遍历 `n` 次，每次判断质数最坏要除到 `i-1`，平均约 `n/2`，所以整体是 `n × n`。  
  - **大白话**：如果数组有 10,000 个元素，暴力版大约要跑 100,000,000 次除法，速度会很慢。

- **空间复杂度**：`O(1)`  
  - 只用了几个整数变量，不会随输入规模增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看出 **瓶颈** 在于每次都要重新判断下标 `i` 是否为质数，这会导致 `O(n²)` 的时间。  
其实下标范围是固定的——`0 … len(nums)-1`，我们只需要 **一次性把所有质数算出来**，随后直接查表即可。

**核心技巧：埃氏筛（Sieve of Eratosthenes）**  
- 想象有一本“下标-是否是质数”的字典，一开始假设所有下标都是质数。  
- 从 `2` 开始，每遇到一个仍被标记为质数的数 `p`，就把 `p` 的所有**倍数**（`p*2, p*3, …`）标记为“不是质数”。  
- 只需要遍历到 `√n`（因为更大的因子已经被小因子筛掉），整个过程是 `O(n log log n)`，在实际中几乎是线性的。

步骤：

1. 用筛法生成一个布尔数组 `is_prime[0..n-1]`，`True` 表示对应下标是质数。  
2. 再一次遍历 `nums`，如果 `is_prime[i]` 为 `True`，把 `nums[i]` 加到 `sumA`，否则加到 `sumB`。  
3. 返回 `abs(sumA - sumB)`。

> **类比**：筛法就像把所有“不是质数的下标”先一次性贴上红贴纸，后面只要看贴纸就能立刻判断，不用每次都去除以检查。

#### 代码（Python）

```python
def splitArrayByPrimeIndices(nums):
    # ---------- 最优版 ----------
    n = len(nums)

    # 1️⃣ 生成质数表（埃氏筛）
    # is_prime[i] 为 True 表示 i 是质数
    is_prime = [False, False] + [True] * (n - 2)   # 0,1 设为非质数，其余先当质数
    p = 2
    while p * p < n:               # 只需遍历到 sqrt(n)
        if is_prime[p]:            # p 仍是质数，则把它的倍数全部标记为非质数
            for multiple in range(p * p, n, p):   # 从 p^2 开始，步长为 p
                is_prime[multiple] = False
        p += 1

    # 2️⃣ 累加两个数组的和
    sumA, sumB = 0, 0
    for i, val in enumerate(nums):
        if is_prime[i]:            # 下标 i 为质数 → 放进 A
            sumA += val
        else:                      # 其余 → 放进 B
            sumB += val

    # 3️⃣ 返回绝对差
    return abs(sumA - sumB)
```

#### 复杂度

- **时间复杂度**：`O(n log log n)`  
  - 筛法的时间大约是 `n * (1/2 + 1/3 + 1/5 + …)`，数学上等价于 `n log log n`。  
  - 对比暴力的 `O(n²)`，当 `n = 10⁵` 时，最优解只需要几万次操作，几乎是瞬间完成。

- **空间复杂度**：`O(n)`  
  - 需要一个长度为 `n` 的布尔数组来存质数信息。  
  - 相比于暴力的 `O(1)`，这里多用了 `n` 个布尔值（约 100KB，对 10⁵ 的规模来说完全可以接受）。

---

## 心得

- **核心技巧**：**埃氏筛**（Sieve of Eratosthenes）—一次性预处理所有质数，避免重复判断。  
- **适用题型**：
  1. 需要在 **固定范围** 内多次判断“是否为质数”的题目（如 “Count Primes”, “Prime Number of Set Bits”）。  
  2. 需要把数组或序列按 **质数下标** / **质数属性** 分组的题目（本题、LeetCode 2475 “Number of Unequal Triplets” 的变形）。  
- **一句话总结**：先把“质数”这张“通行证”一次性印好，后面只要看通行证就能快速分配。

---

## 反思

- **第一反应**：直接遍历每个下标，用循环除法判断是否为质数——这就是暴力解。  
- **最容易踩的坑**：
  1. **下标 0、1 不是质数**，必须在初始化时排除，否则会把它们错误地算进 `A`。  
  2. **数组长度可能只有 1**，此时 `is_prime` 列表的构造要防止负数长度（使用 `max(n,2)` 或提前判断）。  
  3. **负数元素**不影响质数判断，只影响求和，记得使用 `abs` 取绝对差。  
- **下次类似题**：第一步先思考“这类判断是否会被重复使用”。如果是，就 **预处理**（如筛质数、前缀和、哈希表）再遍历；如果不是，则直接暴力即可。