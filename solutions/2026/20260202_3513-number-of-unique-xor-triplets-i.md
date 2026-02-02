# #3513. 唯一异或三元组计数 I / Number of Unique XOR Triplets I

> 难度：中等 · 标签：Array、Math、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/number-of-unique-xor-triplets-i/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums of length n, where nums is a permutation of the numbers in the range [1, n].
A XOR triplet is defined as the XOR of three elements nums[i] XOR nums[j] XOR nums[k] where i <= j <= k.
Return the number of unique XOR triplet values from all possible triplets (i, j, k).

**Examples**

**Example 1:**

```
Input: nums = [1,2]
Output: 2
Explanation:
The possible XOR triplet values are:
The unique XOR values are {1, 2} , so the output is 2.
```

**Example 2:**

```
Input: nums = [3,1,2]
Output: 4
Explanation:
The possible XOR triplet values include:
The unique XOR values are {0, 1, 2, 3} , so the output is 4.
```

**Constraints**

- 1 <= n == nums.length <= 105
- 1 <= nums[i] <= n
- nums is a permutation of integers from 1 to n.

---

## 题目（中文翻译）

给定一个长度为 `n` 的整数数组 `nums`，其中 `nums` 是区间 `[1, n]` 内所有数字的一个排列。  
定义 **异或三元组（XOR triplet）** 为三个元素的异或运算 `nums[i] XOR nums[j] XOR nums[k]`，其中 `i ≤ j ≤ k`。  
返回所有可能的三元组 `(i, j, k)` 所得到的 **唯一异或值** 的个数。

#### 示例 1  
输入：`nums = [1,2]`  
输出：`2`  
解释：  
可能的异或三元组值为：`1 XOR 1 XOR 1 = 1`、`1 XOR 1 XOR 2 = 2`、`1 XOR 2 XOR 2 = 1`、`2 XOR 2 XOR 2 = 2`。  
唯一的异或值为 `{1, 2}`，因此答案是 `2`。

#### 示例 2  
输入：`nums = [3,1,2]`  
输出：`4`  
解释：  
可能的异或三元组值包括：`3 XOR 3 XOR 3 = 3`、`3 XOR 3 XOR 1 = 1`、`3 XOR 1 XOR 2 = 0`、`1 XOR 1 XOR 1 = 1`、`2 XOR 2 XOR 2 = 2` 等。  
唯一的异或值为 `{0, 1, 2, 3}`，所以答案是 `4`。

#### 约束条件
- `1 ≤ n == nums.length ≤ 10^5`
- `1 ≤ nums[i] ≤ n`
- `nums` 是从 `1` 到 `n` 的一个排列。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有合法的三元组全部枚举出来，算出它们的 XOR 值，然后放进一个集合（`set`）去重，最后返回集合的大小。

- **使用的数据结构**  
  - **三层循环**：依次遍历 `i、j、k`（满足 `i ≤ j ≤ k`）。这就像我们在超市里挑选三件商品，先挑第一个，再挑第二个（不能比第一个挑得更早），最后挑第三个（同理）。  
  - **集合（set）**：相当于一本“字典”，里面只记录出现过的词（这里是 XOR 值），相同的词只会出现一次。就像查字典时，看到同一个单词只记一遍。

- **为什么正确**  
  我们把「所有可能的三元组」都列出来了，随后把每个三元组对应的 XOR 结果收集进集合。集合天然去重，所以最后集合的大小就是「不同 XOR 值的个数」。

- **复杂度分析（大白话）**  
  - **时间**：三层循环，每层最多跑 `n` 次，整体大约是 `n × n × n = n³` 次操作。把 `n³` 用大 O 表示就是 **O(n³)**，意思是「时间会随 `n` 的立方增长」，当 `n` 达到几万时根本跑不完。  
  - **空间**：我们只需要保存一个集合，最坏情况下它会装下所有不同的 XOR 值。因为 XOR 的取值范围不超过 `2⁽ⁱ⁾-1`（这里的 `i` 不超过 30），所以集合的大小是常数级的，记作 **O(1)**（相对于 `n` 来说可以忽略）。

#### 代码（Python）

```python
from typing import List

def brute_unique_xor_triplets(nums: List[int]) -> int:
    n = len(nums)
    uniq = set()                     # 用来去重的集合
    # 三层循环枚举 i ≤ j ≤ k
    for i in range(n):
        for j in range(i, n):
            for k in range(j, n):
                xor_val = nums[i] ^ nums[j] ^ nums[k]   # ^ 是异或运算
                uniq.add(xor_val)       # 自动去重
    return len(uniq)                 # 集合的大小就是答案
```

#### 复杂度

- **时间复杂度**：O(n³) — 随着数组长度的立方增长，实际运行会非常慢。  
- **空间复杂度**：O(1) — 只用了一个集合，最多存几百个整数（与 `n` 无关）。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到，**枚举所有三元组是最大的瓶颈**。我们要思考：  
1. **XOR 的取值范围到底有多大？**  
2. **有没有办法直接算出「可以得到多少种不同的 XOR」而不去枚举？**

**关键观察**  

- 数组 `nums` 是 `1 … n` 的一个排列，意味着它恰好包含了 **所有** 小于等于 `n` 的正整数。  
- 对于任意整数 `x`，我们只关心它的二进制位。设 `msb(n)` 为 `n` 的最高位（最左边的 `1`）所在的下标（从 0 开始计数）。例如 `n = 13 (1101₂)`，`msb = 3`。  
- 当 `n ≥ 3` 时，**可以得到 `[0, 2^{msb(n)+1} - 1]` 区间内的所有数**。换句话说，所有长度为 `msb+1` 位的二进制数（从全 0 到全 1）都能通过某个三元组的 XOR 获得。  

**为什么会这样？**  

把每个数字看成一个二进制向量（每一位是 0/1），XOR 就是向量的 **按位加法（模 2）**。  
- `1 … n` 包含了 **完整的基**：从 `1` 到 `2^{msb}`，我们已经拥有了所有可能的最高位组合。  
- 只要我们选出两个数 `a`、`b`，我们可以把第三个数设成 `c = a ^ b ^ target`，这样 `a ^ b ^ c = target`。因为 `target` 的每一位都不超过最高位 `msb`，`c` 也一定在 `[1, n]` 范围内（`n` 已经覆盖了所有这些数）。  
- 由于题目允许 **重复选取**（`i ≤ j ≤ k`），即使 `c` 与 `a`、`b` 相同也合法。于是 **任意目标值** 都能被构造出来。

**特殊情况**  

- 当 `n = 1` 时，只能取唯一的三元组 `(1,1,1)`，XOR = `1` → 1 种。  
- 当 `n = 2` 时，可能的 XOR 值是 `{1,2}` → 2 种。  
- 这两个小于 3 的情况需要单独返回 `n`。

**最终公式**  

```
if n <= 2:   answer = n
else:        answer = 2 ** (msb(n) + 1)
```

其中 `msb(n) = floor(log2 n)`，在 Python 中可以用 `n.bit_length() - 1` 获得。

#### 代码（Python）

```python
from typing import List

def unique_xor_triplets(nums: List[int]) -> int:
    """
    返回所有满足 i ≤ j ≤ k 的三元组的 XOR 结果中不同值的个数。
    只依赖数组长度 n，实际元素内容不影响答案，因为 nums 是 1..n 的排列。
    """
    n = len(nums)
    if n <= 2:                     # 小规模直接返回 n
        return n

    # msb = 最高位下标 = (二进制位数 - 1)
    msb = n.bit_length() - 1       # 例如 n=13(1101) -> bit_length=4 -> msb=3
    return 1 << (msb + 1)           # 2^{msb+1}，左移等价于幂运算
```

#### 复杂度

- **时间复杂度**：O(1) — 只做常数次整数运算，和 `n` 的大小无关。  
- **空间复杂度**：O(1) — 只用了几个整数变量。

---

## 心得

- **核心技巧**：利用 **位运算的线性空间特性**，把「所有可能的 XOR」转化为「能否在给定的整数集合中构造任意目标向量」的判断。  
- **适用的题型**  
  1. 只要给定的集合是 **完整的连续整数区间**（或能生成完整的二进制基），询问「XOR/AND/OR 能产生多少种不同值」的题目。  
  2. 需要 **快速求取全部可能结果数量**，而不是逐一枚举的 combinatorial 题目。  
  3. 类似的「三数异或」或「两数异或」覆盖区间的题目（如 LeetCode 1738、1915 等）。  

- **一句话总结解题钥匙**：**当数组是 1~n 的全排列且 n≥3 时，三数异或可以覆盖所有 ≤最高位的二进制数，答案就是 2^{msb+1}**。

---

## 反思

- **第一反应**：直接写三层循环枚举，想把所有情况都算出来。  
- **最容易踩的坑**  
  - 忘记 **允许重复下标**（i ≤ j ≤ k），导致遗漏像 `(a,a,a)` 这种情况。  
  - 对 **边界 n=1、2** 没有单独处理，直接套公式会得到 `4`（错误）。  
  - 对 **msb 的定义** 不清晰，导致写错 `bit_length` 的使用方式。  

- **下次类似题目第一步**：先思考「给定的数集合能否在二进制位上生成完整的基」——如果可以，往往能直接得到“覆盖全区间”的结论，从而避免枚举。