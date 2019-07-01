# #477. 总汉明距离 / Total Hamming Distance

> 难度：中等 · 标签：Array、Math、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/total-hamming-distance/)

---

## 题目（英文原版）

**Description**

The Hamming distance between two integers is the number of positions at which the corresponding bits are different.
Given an integer array nums, return the sum of Hamming distances between all the pairs of the integers in nums.

**Examples**

**Example 1:**

```
Input: nums = [4,14,2]
Output: 6
Explanation: In binary representation, the 4 is 0100, 14 is 1110, and 2 is 0010 (just
showing the four bits relevant in this case).
The answer will be:
HammingDistance(4, 14) + HammingDistance(4, 2) + HammingDistance(14, 2) = 2 + 2 + 2 = 6.
```

**Example 2:**

```
Input: nums = [4,14,4]
Output: 4
```

**Constraints**

- 1 <= nums.length <= 104
- 0 <= nums[i] <= 109
- The answer for the given input will fit in a 32-bit integer.

---

## 题目（中文翻译）

两个整数之间的汉明距离（Hamming distance）是指对应的二进制位中不同的位数。
给定一个整数数组 `nums`，返回 `nums` 中所有整数对之间的汉明距离之和。

**示例 1**  
**示例 2**  
**约束条件**  

### 示例

#### 示例 1
**输入:** `nums = [4,14,2]`  
**输出:** `6`  
**解释:**  
二进制表示中，`4` 为 `0100`，`14` 为 `1110`，`2` 为 `0010`（这里只展示了相关的四位）。  
答案为：  
`HammingDistance(4, 14) + HammingDistance(4, 2) + HammingDistance(14, 2) = 2 + 2 + 2 = 6`。

#### 示例 2
**输入:** `nums = [4,14,4]`  
**输出:** `4`

### 约束条件
- `1 <= nums.length <= 10^4`
- `0 <= nums[i] <= 10^9`
- 给定输入的答案能够放入 32 位整数中。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的办法是把数组里所有两两组合的元素挑出来，分别计算它们的 **汉明距离**（即二进制表示中不同的位数），然后把所有距离累加。

- **数据结构**：我们只需要普通的 Python 列表 `nums`。  
- **汉明距离的计算**：可以把两个整数 `a`、`b` 做异或 `a ^ b`，异或后得到的二进制数中，`1` 出现的次数正好等于不同位的数量。于是再把这个结果的 `1` 统计出来（常用的做法是 `while x: cnt += x & 1; x >>= 1`），即可得到 `a` 与 `b` 的汉明距离。

> 类比：把 `a`、`b` 看成两本同样页数的书，`1` 表示该页上有图画，`0` 表示空白。异或相当于把两本书对应页的图画进行“对比”，只要有一页上图画不同，就在结果里留下一个记号（`1`），最后数记号的数量就是不同的页数。

- **正确性**：每一对 `(i, j)`（`i < j`）都会被遍历一次，且我们用数学上等价的异或+计数方式得到了它们的汉明距离，累加所有距离即为题目要求的答案。

#### 代码（Python）

```python
from typing import List

class Solution:
    def totalHammingDistance(self, nums: List[int]) -> int:
        n = len(nums)
        total = 0                      # 累计所有对的汉明距离

        # 暴力遍历所有两两组合
        for i in range(n):
            for j in range(i + 1, n):
                x = nums[i] ^ nums[j]   # 异或得到不同位的掩码
                # 统计 x 中 1 的个数，即汉明距离
                while x:
                    total += x & 1      # x 的最低位是 1 就加 1
                    x >>= 1             # 右移一位，继续检查下一位
        return total
```

#### 复杂度

- **时间复杂度**：`O(n² * w)`，其中 `n` 是数组长度，`w` 是整数的二进制位数（本题最多 30 位，因为 `nums[i] ≤ 10⁹`）。  
  大白话：如果数组有 10⁴ 个元素，暴力会比较约 5×10⁷ 对，每对又要检查 30 位，运算次数会非常大，容易超时。

- **空间复杂度**：`O(1)`，只用了常数级的额外变量。  
  大白话：不管数组有多长，程序占用的额外内存几乎不变。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 出在两层循环：我们对每一对元素都要重复检查相同的位。实际上，**每一位的贡献是可以独立计算的**：

- 对于二进制的第 `k` 位（从 0 开始计数），如果有 `c` 个数在这位上是 `1`，其余 `n‑c` 个数是 `0`。  
- 这 `c` 个 `1` 与 `n‑c` 个 `0` 组合成的不同位对数是 `c * (n - c)`（每个 `1` 可以和每个 `0` 形成一对）。  
- 由于每对不同位在该位上贡献 **1**，所以第 `k` 位对答案的贡献就是 `c * (n - c)`。  

把所有位（0~30）都算一遍，最后把每位的贡献相加，就是所有两两汉明距离的总和。

> 类比：把每一位想成一道“颜色题”。有 `c` 只红色球（1）和 `n‑c` 只蓝色球（0），每次把一只红球和一只蓝球配对，就得到一次“颜色不同”。配对的总次数正是 `c * (n - c)`。

**实现细节**：

1. 先遍历数组一次，统计每一位上 `1` 的个数 `cnt[k]`（用一个长度为 31 的列表存储，31 因为 `10⁹ < 2³⁰`，再多一位安全）。  
2. 再遍历这 31 位，对每位使用公式 `cnt[k] * (n - cnt[k])` 累加到答案。  
3. 时间上是 `O(n * w)`，空间上是 `O(w)`（只存 31 个计数），远快于暴力。

#### 代码（Python）

```python
from typing import List

class Solution:
    def totalHammingDistance(self, nums: List[int]) -> int:
        n = len(nums)
        # cnt[k] 记录第 k 位上 1 出现的次数，k 从 0 到 30（共 31 位）
        cnt = [0] * 31

        # 统计每一位的 1 的个数
        for num in nums:
            for k in range(31):
                # (num >> k) & 1 取出第 k 位，若为 1 则计数加一
                cnt[k] += (num >> k) & 1

        total = 0
        # 对每一位计算贡献：c * (n - c)
        for k in range(31):
            c = cnt[k]                # 第 k 位上 1 的数量
            total += c * (n - c)      # 与 0 配对的次数，即该位的汉明距离总和
        return total
```

#### 复杂度

- **时间复杂度**：`O(n * w)`，这里 `w = 31` 是常数，所以实际是线性 `O(n)`。  
  与暴力 `O(n²)` 相比，数量级从平方级降到了线性级，10000 个元素也能在毫秒级完成。

- **空间复杂度**：`O(w)`，即只用了 31 个整数的额外空间。  
  这在实际中几乎可以忽略不计。

---

## 心得

- **核心技巧**：**按位计数**（Bitwise counting），把全局的两两比较拆解为每一位的独立统计。  
- **适用题型**：  
  1. “所有数对的异或和” 类似题目（如 LeetCode 477 Total Hamming Distance）。  
  2. “求数组中每一位出现 1 的次数” 的变体（如求所有子集的按位或总和）。  
  3. “统计数组中每位 1 的数量再求组合” 的问题（如 1310 Xor Queries of a Subarray）。  
- **一句话总结解题钥匙**：**把两两比较的重复工作拆到每一位上，用组合数 `c·(n‑c)` 把它一次算完**。

---

## 反思

- **第一反应**：看到“所有两两的汉明距离”，自然想到双层循环暴力求解。  
- **最容易踩的坑**：  
  - 忘记考虑整数的最高位，导致统计位数不够（`10⁹` 需要到第 30 位）。  
  - 在统计每位 `1` 的次数时，直接使用 `bin(num).count('1')` 会把所有位混在一起，失去位置信息。  
  - 组合公式要记得是 `c * (n - c)`，而不是 `c * c` 或者 `c * (c-1)`。  
- **下次遇到同类题**：第一步先思考“是否可以把问题拆成每一位独立处理”，如果可以，就立刻转向 **按位计数** 的思路。