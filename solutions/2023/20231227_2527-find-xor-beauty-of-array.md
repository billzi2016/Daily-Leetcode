# #2527. 数组的 XOR 美感 / Find Xor-Beauty of Array

> 难度：中等 · 标签：Array、Math、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/find-xor-beauty-of-array/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums.
The effective value of three indices i, j, and k is defined as ((nums[i] | nums[j]) & nums[k]).
The xor-beauty of the array is the XORing of the effective values of all the possible triplets of indices (i, j, k) where 0 <= i, j, k < n.
Return the xor-beauty of nums.
Note that:

**Examples**

**Example 1:**

```
Input: nums = [1,4]
Output: 5
Explanation: 
The triplets and their corresponding effective values are listed below:
- (0,0,0) with effective value ((1 | 1) & 1) = 1
- (0,0,1) with effective value ((1 | 1) & 4) = 0
- (0,1,0) with effective value ((1 | 4) & 1) = 1
- (0,1,1) with effective value ((1 | 4) & 4) = 4
- (1,0,0) with effective value ((4 | 1) & 1) = 1
- (1,0,1) with effective value ((4 | 1) & 4) = 4
- (1,1,0) with effective value ((4 | 4) & 1) = 0
- (1,1,1) with effective value ((4 | 4) & 4) = 4 
Xor-beauty of array will be bitwise XOR of all beauties = 1 ^ 0 ^ 1 ^ 4 ^ 1 ^ 4 ^ 0 ^ 4 = 5.
```

**Example 2:**

```
Input: nums = [15,45,20,2,34,35,5,44,32,30]
Output: 34
Explanation: The xor-beauty of the given array is 34.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 109

---

## 题目（中文翻译）

给定一个下标从 **0** 开始的整数数组 `nums`。  
三个下标 `i`、`j`、`k` 的 **有效值 (effective value)** 定义为 `((nums[i] | nums[j]) & nums[k])`。  
数组的 **XOR 美感 (xor-beauty)** 为所有可能的下标三元组 **(i, j, k)**（其中 `0 <= i, j, k < n`）的有效值进行 **异或 (XOR)** 运算后的结果。  
返回 `nums` 的 XOR 美感。

**示例 1**  
```
Input: nums = [1,4]
Output: 5
Explanation:
列举的三元组及其对应的有效值如下：
- (0,0,0) 的有效值为 ((1 | 1) & 1) = 1
- (0,0,1) 的有效值为 ((1 | 1) & 4) = 0
- (0,1,0) 的有效值为 ((1 | 4) & 1) = 1
- (0,1,1) 的有效值为 ((1 | 4) & 4) = 4
- (1,0,0) 的有效值为 ((4 | 1) & 1) = 1
- (1,0,1) 的有效值为 ((4 | 1) & 4) = 4
- (1,1,0) 的有效值为 ((4 | 4) & 1) = 0
- (1,1,1) 的有效值为 ((4 | 4) & 4) = 4
对所有 8 种有效值进行异或得到 5。
```

**示例 2**  
```
Input: nums = [15,45,20,2,34,35,5,44,32,30]
Output: 34
Explanation: 给定数组的 XOR 美感为 34。
```

**约束条件**  
- `1 <= nums.length <= 10^5`  
- `1 <= nums[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把题目给出的“三元组”全部枚举出来，逐个计算  

```
effective = (nums[i] | nums[j]) & nums[k]
```

然后把所有得到的 `effective` 用 XOR（异或）累加。  
这里用到的两个位运算：

* **或（|）**：把两个数的二进制位“拼在一起”，只要对应位有一个是 1，结果位就是 1。可以把它想象成“两个灯泡只要有一个亮，整体就亮”。  
* **与（&）**：只有对应位都是 1，结果位才是 1。就像“两个开关必须都打开，灯才亮”。  

我们只需要把所有可能的 `(i, j, k)`（`0 ≤ i, j, k < n`）遍历一遍，计算 `(nums[i] | nums[j]) & nums[k]`，再把这些值用 `^=`（XOR）累加即可。

> **为什么暴力一定能得到正确答案？**  
> 题目要求的就是把 **所有** 三元组的有效值进行 XOR，遍历不遗漏任何组合自然就满足要求。

#### 代码（Python）

```python
def xor_beauty_bruteforce(nums):
    n = len(nums)
    ans = 0                         # 用来累计 XOR 的答案
    for i in range(n):              # 第一个下标 i
        for j in range(n):          # 第二个下标 j
            for k in range(n):      # 第三个下标 k
                # 先做 “或” 再做 “与”，得到当前三元组的有效值
                effective = (nums[i] | nums[j]) & nums[k]
                ans ^= effective    # 累计异或
    return ans
```

> 关键行的中文注释已经写在代码里，直接复制运行即可。

#### 复杂度

- **时间复杂度**：`O(n³)`  
  这里的 `n³` 表示如果数组有 1000 个元素，需要执行 1000³ = 10⁹ 次最内层的计算。用大白话说，就是**随着元素个数每增加一次，运算次数会乘以自身的大小**，很快就会不可接受。

- **空间复杂度**：`O(1)`  
  只用了几个额外的变量（`ans`、循环计数器），和输入规模无关。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，真正耗时的地方是 **三层循环**——我们在每一次循环里都在重复做同样的位运算。  
要想提速，需要找出 **哪些三元组在异或时会相互抵消**，只保留对最终答案有“奇数次”贡献的那部分。

**关键观察**（位层面）  
我们把每一位（比如第 0 位、 第 1 位 …）单独考虑。  
设第 `b` 位的掩码为 `mask = 1 << b`，记 `cnt` 为数组中 **第 `b` 位为 1 的元素个数**。  

对任意三元组 `(i, j, k)`，第 `b` 位的有效值为 1 当且仅当：

1. `nums[k]` 的第 `b` 位是 1（因为要 `& nums[k]`），**并且**  
2. `nums[i]` 或 `nums[j]` 的第 `b` 位是 1（因为要 `|`）。

所以，**只要 `k` 的第 `b` 位是 1，`i`、`j` 的取值方式并不影响第 `b` 位的最终值**——因为 `|` 只要有一个 1，结果就是 1，而所有 `i、j` 的组合中，总会出现 “至少有一个 1” 的情况。

更正式的计数：

- 选 `k` 的方式有 `cnt` 种（因为只有这些元素的第 `b` 位是 1）。
- 对于每个固定的 `k`，`i`、`j` 可以是任意元素，总共有 `n·n` 种组合。
- 所以，第 `b` 位为 1 的三元组总数 = `cnt * n * n`。

在 XOR 中，**只关心奇偶性**：如果出现的次数是偶数，最终会抵消为 0；如果是奇数，最终保留下来为 1。  
`cnt * n * n` 的奇偶性只取决于 `cnt` 的奇偶性，因为 `n * n`（即 `n²`）不管是奇是偶，都不会改变奇偶性（奇数乘奇数仍是奇数，偶数乘任意数都是偶数）。  
于是：

- 当 `cnt` 为 **奇数** 时，第 `b` 位在答案中为 1。
- 当 `cnt` 为 **偶数** 时，第 `b` 位在答案中为 0。

这正好等价于 **对所有数组元素做一次 XOR**——因为 XOR 本身的性质是：对应位的结果是 1 当且仅当该位出现奇数次 1。  

**结论**：`xor-beauty(nums) = nums[0] ^ nums[1] ^ … ^ nums[n‑1]`。

> **为什么不需要考虑 i、j 的具体值？**  
> 因为 `|` 运算只要有一个 1 就一定是 1，而在所有 `i、j` 的组合里，至少会出现一次 “i 或 j 为 1”。这一次已经把该位设为 1，后面的组合对该位不再产生影响（异或会把偶数次出现的 1 抵消掉）。

#### 代码（Python）

```python
def xor_beauty(nums):
    """
    最优解：直接把所有元素异或即可。
    时间 O(n)，空间 O(1)。
    """
    ans = 0               # 累计答案
    for x in nums:        # 遍历每个元素
        ans ^= x          # 异或累计
    return ans
```

> 代码每行都有中文解释，直接跑通即可。

#### 复杂度

- **时间复杂度**：`O(n)`  
  只需要遍历一次数组，和元素个数成线性关系。相比暴力的 `n³`，大幅降低运算量。

- **空间复杂度**：`O(1)`  
  只用了常数个额外变量（`ans`、循环变量），不随 `n` 增长。

---

## 心得

- **核心技巧**：**位独立性 + 奇偶性**。把异或的“奇数次出现保留、偶数次抵消”特性与每一位出现的次数联系起来，得出整体答案等于所有数的异或。
- **适用的题型**  
  1. “对所有子集/子序列/三元组做位运算后再异或”类问题（例如 LeetCode 1720 `Decode XORed Array` 的思路类似）。  
  2. “统计某位出现次数的奇偶性”类问题（例如 `Sum of All Subset XOR Totals`）。  
  3. 需要把复杂组合简化为 **线性** 操作的位运算题。
- **一句话总结**：**只要把每一位出现的次数取模 2，答案就是所有元素的异或**。

---

## 反思

- **第一反应**：看到“三重循环 + 位运算”，本能想到直接枚举——这在小数据上能跑通，但很快会卡在时间限制上。
- **最容易踩的坑**  
  - **忘记奇偶性**：在 XOR 中，偶数次出现会抵消，必须把注意力放在“出现次数是奇数还是偶数”。  
  - **误以为 i、j 必须一起讨论**：实际上 `|` 的特性让它们可以被整体忽略，只要 `k` 的该位为 1 即可。  
  - **边界条件**：数组长度可能是 1，仍然要返回该唯一元素的值（此时 `cnt = 1`，奇数，答案就是该元素本身）。
- **下次类似题的第一步**：**先把表达式拆到位层面，统计每一位出现的次数的奇偶性**，看能否直接映射到 “所有元素的 XOR”。这样往往能把看似指数级的组合问题降到线性时间。