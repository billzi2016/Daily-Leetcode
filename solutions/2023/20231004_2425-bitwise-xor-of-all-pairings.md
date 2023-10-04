# #2425. 位运算异或所有配对 / Bitwise XOR of All Pairings

> 难度：中等 · 标签：Array、Bit Manipulation、Brainteaser · [LeetCode 链接](https://leetcode.com/problems/bitwise-xor-of-all-pairings/)

---

## 题目（英文原版）

**Description**

You are given two 0-indexed arrays, nums1 and nums2, consisting of non-negative integers. Let there be another array, nums3, which contains the bitwise XOR of all pairings of integers between nums1 and nums2 (every integer in nums1 is paired with every integer in nums2 exactly once).
Return the bitwise XOR of all integers in nums3.

**Examples**

**Example 1:**

```
Input: nums1 = [2,1,3], nums2 = [10,2,5,0]
Output: 13
Explanation:
A possible nums3 array is [8,0,7,2,11,3,4,1,9,1,6,3].
The bitwise XOR of all these numbers is 13, so we return 13.
```

**Example 2:**

```
Input: nums1 = [1,2], nums2 = [3,4]
Output: 0
Explanation:
All possible pairs of bitwise XORs are nums1[0] ^ nums2[0], nums1[0] ^ nums2[1], nums1[1] ^ nums2[0],
and nums1[1] ^ nums2[1].
Thus, one possible nums3 array is [2,5,1,6].
2 ^ 5 ^ 1 ^ 6 = 0, so we return 0.
```

**Constraints**

- 1 <= nums1.length, nums2.length <= 105
- 0 <= nums1[i], nums2[j] <= 109

---

## 题目（中文翻译）

给定两个 **0 索引** 的数组（array）`nums1` 和 `nums2`，其中均包含非负整数。再设一个数组 `nums3`，其元素为 `nums1` 与 `nums2` 中所有整数配对的位运算异或（bitwise XOR）结果（即 `nums1` 中的每个整数都会与 `nums2` 中的每个整数恰好配对一次）。  
返回 `nums3` 中所有整数的位运算异或（bitwise XOR）值。

## 示例

### 示例 1
**输入**  
`nums1 = [2,1,3]`, `nums2 = [10,2,5,0]`  

**输出**  
`13`  

**解释**  
一种可能的 `nums3` 为 `[8,0,7,2,11,3,4,1,9,1,6,3]`。这些数的位运算异或（bitwise XOR）结果为 `13`，因此返回 `13`。

### 示例 2
**输入**  
`nums1 = [1,2]`, `nums2 = [3,4]`  

**输出**  
`0`  

**解释**  
所有可能的配对位运算异或（bitwise XOR）为 `nums1[0] ^ nums2[0]`、`nums1[0] ^ nums2[1]`、`nums1[1] ^ nums2[0]`、`nums1[1] ^ nums2[1]`。  
于是一个可能的 `nums3` 为 `[2,5,1,6]`。  
`2 ^ 5 ^ 1 ^ 6 = 0`，所以返回 `0`。

## 约束条件
- `1 <= nums1.length, nums2.length <= 10^5`
- `0 <= nums1[i], nums2[j] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把 `nums1` 和 `nums2` 中的每一个数两两配对，算出它们的 **异或**（`^`），把所有得到的结果放进一个新数组 `nums3`，最后再把 `nums3` 中的所有元素再异或一次得到答案。

> **类比**：把 `nums1` 看成左边的水果篮，`nums2` 看成右边的水果篮。我们要把左边的每个水果和右边的每个水果都配对一次，记录下配对后的味道（这里的味道就是异或值），最后把所有味道再混合（再次异或）得到最终的味道。

这种做法一定能得到正确答案，因为我们把**所有**合法配对都算进来了，异或运算本身是**交换律**和**结合律**成立的，顺序不影响最终结果。

#### 代码（Python）

```python
def xorAllPairs_bruteforce(nums1, nums2):
    # 记录最终答案
    ans = 0
    # 对 nums1 中的每个元素
    for a in nums1:                 # 外层循环遍历左篮子
        # 对 nums2 中的每个元素
        for b in nums2:             # 内层循环遍历右篮子
            ans ^= a ^ b            # 先算 a ^ b，再把它和当前答案异或
    return ans
```

#### 复杂度

- **时间复杂度**：`O(m * n)`（`m = len(nums1)`, `n = len(nums2)`）  
  直译就是「我们要遍历左篮子里的每个水果 `m` 次，每次都要遍历右篮子里的 `n` 个水果」，所以总共要做 `m×n` 次异或运算。  
  当 `m`、`n` 都是 10⁵ 时，`m*n` 会达到 10¹⁰，远远超出计算机的接受范围，实际会超时。

- **空间复杂度**：`O(1)`  
  只用了常数个额外变量 (`ans`, `a`, `b`)，不随输入规模增长。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到：**每个 `nums1` 中的数会和 `nums2` 中的每个数配对一次**。  
如果把配对的过程展开，实际等价于：

- `nums1` 中的每个元素 **出现 `n` 次**（因为它要和 `nums2` 中的 `n` 个元素配对）。
- `nums2` 中的每个元素 **出现 `m` 次**（因为它要和 `nums1` 中的 `m` 个元素配对）。

异或的一个重要特性是：**相同的数异或两次会相互抵消，等于 0**（`x ^ x = 0`），而且 **0 再和任何数异或仍是原数**（`0 ^ x = x`）。  
因此，**出现偶数次的数最终会被抵消掉，只剩下出现奇数次的数对答案有贡献**。

所以我们只需要关心：

- `n`（`len(nums2)`）是 **奇数** 还是 **偶数**  
  - 若 `n` 为奇数，`nums1` 中的每个数出现奇数次 → 这些数全部保留下来（整体再异或一次）。
  - 若 `n` 为偶数，`nums1` 中的每个数出现偶数次 → 全部抵消，贡献为 0。

- 同理，`m`（`len(nums1)`）的奇偶性决定 `nums2` 中的数是否会留下。

于是答案可以直接写成：

```
if n is odd:   ans ^= XOR of all nums1
if m is odd:   ans ^= XOR of all nums2
```

如果 `m` 与 `n` 同时为偶数，`ans` 直接是 0。

> **类比**：想象左篮子里的水果每种都有 `n` 只，右篮子里的水果每种都有 `m` 只。我们把同种水果两两配对后再“混合”。如果某种水果的数量是偶数（2、4、6…），它们会两两抵消，最后桌面上看不见；只有数量是奇数（1、3、5…）时，才会留下一只，参与最终的味道。

#### 代码（Python）

```python
def xorAllPairs(nums1, nums2):
    """
    计算所有配对的异或结果的整体异或。
    思路：只保留出现奇数次的数。
    """
    m, n = len(nums1), len(nums2)

    # 先算出 nums1 的整体异或，和 nums2 的整体异或
    xor1 = 0
    for x in nums1:          # 遍历左篮子，累积异或
        xor1 ^= x

    xor2 = 0
    for x in nums2:          # 遍历右篮子，累积异或
        xor2 ^= x

    ans = 0
    # 当 nums2 长度为奇数时，nums1 中的每个数出现奇数次，需要保留
    if n % 2 == 1:           # n 为奇数
        ans ^= xor1          # 把所有 nums1 的异或结果加入答案

    # 当 nums1 长度为奇数时，nums2 中的每个数出现奇数次，需要保留
    if m % 2 == 1:           # m 为奇数
        ans ^= xor2          # 把所有 nums2 的异或结果加入答案

    return ans
```

#### 复杂度

- **时间复杂度**：`O(m + n)`  
  只需要遍历两遍数组，各自计算一次整体异或。  
  与暴力的 `m*n` 相比，规模从 “乘法” 降到了 “加法”，即使 `m`、`n` 都是 10⁵，最多也只有 2×10⁵ 次运算，轻松在 1 秒内完成。

- **空间复杂度**：`O(1)`  
  只用了几个整数变量 (`m, n, xor1, xor2, ans`)，不随输入规模增长。

---

## 心得

- **核心技巧**：利用异或的“奇偶抵消”特性，只保留出现奇数次的数。  
- **适用的题型**：  
  1. “所有子集/子数组/配对的异或/与/或” 这类需要统计出现次数的题目。  
  2. “数组中出现奇数次的数” （如 LeetCode 137）  
  3. “两组数的笛卡尔积异或/与/或” （本题就是典型例子）

- **一句话总结**：**只要判断每个原数组的长度奇偶性，就能瞬间得到所有配对异或的整体结果。**

---

## 反思

- **第一反应**：直接写两层循环暴力枚举，没想到异或的抵消特性可以把问题大幅简化。  
- **最容易踩的坑**：忘记考虑数组长度的奇偶性导致把所有数都直接异或，或者在代码里把 `xor1`、`xor2` 写成了 `^=`（自异或）导致错误。  
- **下次类似题的第一步**：先思考“每个元素会出现多少次”，然后利用“出现偶数次抵消，出现奇数次保留”的异或/与/或特性，看看能否把计数转化为**奇偶判断**。