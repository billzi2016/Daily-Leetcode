# #2917. 数组的 K-or / Find the K-or of an Array

> 难度：简单 · 标签：Array、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/find-the-k-or-of-an-array/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums, and an integer k. Let's introduce K-or operation by extending the standard bitwise OR. In K-or, a bit position in the result is set to 1 if at least k numbers in nums have a 1 in that position.
Return the K-or of nums.

**Examples**

**Example 1:**

```
Input: nums = [7,12,9,8,9,15], k = 4
Output: 9
Explanation:
Represent numbers in binary:
Bit 0 is set in 7, 9, 9, and 15. Bit 3 is set in 12, 9, 8, 9, and 15. Only bits 0 and 3 qualify. The result is (1001) 2 = 9 .
```

**Example 2:**

```
Input: nums = [2,12,1,11,4,5], k = 6
Output: 0
Explanation: No bit appears as 1 in all six array numbers, as required for K-or with k = 6 . Thus, the result is 0.
```

**Example 3:**

```
Input: nums = [10,8,5,9,11,6,8], k = 1
Output: 15
Explanation: Since k == 1 , the 1-or of the array is equal to the bitwise OR of all its elements. Hence, the answer is 10 OR 8 OR 5 OR 9 OR 11 OR 6 OR 8 = 15 .
```

**Constraints**

- 1 <= nums.length <= 50
- 0 <= nums[i] < 231
- 1 <= k <= nums.length

---

## 题目（中文翻译）

给定一个整数数组 `nums` 和一个整数 `k`。我们通过扩展标准的按位或（bitwise OR）来引入 **K-or 操作（K-or operation）**。在 K-or 中，如果 `nums` 中至少有 `k` 个数字在某个位位置（bit position）上为 1，则结果的该位被置为 1。返回数组 `nums` 的 K-or。

### 示例

#### 示例 1
**输入**: `nums = [7,12,9,8,9,15]`, `k = 4`  
**输出**: `9`  
**解释**:  
将数字转换为二进制:
- 位 0 在 `7, 9, 9, 15` 中为 1  
- 位 3 在 `12, 9, 8, 9, 15` 中为 1  

只有位 0 和位 3 满足至少有 4 个数为 1 的条件。结果为二进制 `(1001)_2 = 9`。

#### 示例 2
**输入**: `nums = [2,12,1,11,4,5]`, `k = 6`  
**输出**: `0`  
**解释**: 没有任何位在所有 6 个数组元素中 simultaneously 为 1，因而满足 `k = 6` 的 K-or 结果为 0。

#### 示例 3
**输入**: `nums = [10,8,5,9,11,6,8]`, `k = 1`  
**输出**: `15`  
**解释**: 当 `k == 1` 时，数组的 1-or 等价于所有元素的按位或（bitwise OR）。因此答案为 `10 OR 8 OR 5 OR 9 OR 11 OR 6 OR 8 = 15`。

### 约束条件
- `1 <= nums.length <= 50`
- `0 <= nums[i] < 2^31`
- `1 <= k <= nums.length`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**逐位检查**。  
我们把 32 位（因为题目说 `nums[i] < 2^31`）从低位到高位一个一个遍历。  
对于每一位 `bit`，再遍历整个数组 `nums`，统计有多少个数在该位上是 1。  
- **数据结构**：只需要一个整数 `cnt` 用来计数，想象成在做“点名”。  
- **类比**：把每一位看成一本词典的页码，遍历数组就是把每本书的对应页码翻出来，看看有多少本书在这页上写了“1”。  
- **为什么正确**：题目要求“如果至少 k 个数在该位是 1，结果位就设为 1”。我们正好把每一位的 1 的出现次数算出来，满足条件就把结果的该位设 1，不满足就保持 0。  

#### 代码（Python）  

```python
from typing import List

def k_or(nums: List[int], k: int) -> int:
    res = 0                      # 最终答案，二进制位全是 0
    # 只需要检查 0~30 位（31 位足够，因为 < 2^31），这里统一遍历 0~31
    for bit in range(32):
        mask = 1 << bit          # 2^bit，对应当前要检查的那一位
        cnt = 0                  # 统计有多少个数在该位上是 1
        # 暴力遍历整个数组，逐个判断该位是否为 1
        for x in nums:
            if x & mask:         # 如果 x 与 mask 的按位与不为 0，说明该位是 1
                cnt += 1
        # 如果出现次数不少于 k，就把结果的对应位设为 1
        if cnt >= k:
            res |= mask           # 把 mask 加到结果中（相当于把该位设为 1）
    return res
```

#### 复杂度  

- **时间复杂度**：`O(32 * n)`，其中 `n = len(nums)`。  
  解释一下：我们有 32 次外层循环，每次都要遍历 `n` 个数去计数。  
  这里的 “`O(32 * n)`” 可以理解为 “大约是 32 倍的 `n`”，因为 32 是常数，实际运行时间随 `n` 线性增长。  
- **空间复杂度**：`O(1)`，只用了常数个额外变量（`res、mask、cnt`），不随输入规模增长。

---  

### 2. 最优解  

#### 思路  

暴力解已经很接近最优，因为我们只能检查每一位是否满足 “出现次数 ≥ k”。  
唯一可以改进的地方是**把两层循环合并成一次遍历**：  
- 在一次遍历数组的过程中，把每个数的 **所有 1 位** 的计数直接加到对应的位计数器中。  
- 这样我们只需要 **一次遍历 `nums`**（而不是每个位都遍历一次），随后再一次遍历 0~31 位判断是否 ≥ k。  

核心技巧是 **位计数**（bit counting），它和我们在统计二进制中每一位出现次数时使用的“哈希表”类似，只是这里的 “键” 是位的位置，值是出现次数。  

实现步骤：  
1. 初始化长度为 32 的列表 `bit_cnt`，全部为 0，用来记录每一位出现了多少次 1。  
2. 遍历数组 `nums`，对当前数 `x`：  
   - 使用 `while x:` 循环，每次取出最低位的 1（`x & -x`），得到该位的索引 `bit`（`(x & -x).bit_length() - 1`），计数器 `bit_cnt[bit] += 1`。  
   - 然后把最低位的 1 去掉（`x &= x - 1`），继续。这样只会遍历 **实际为 1 的位**，若一个数只有少数几位是 1，就更快。  
3. 再遍历 0~31 位，如果 `bit_cnt[bit] >= k`，把该位设为 1，得到答案。  

这样做的好处是 **实际遍历的位数 ≤ 所有数中 1 的总个数**，在很多数值稀疏的情况下会更快。  

#### 代码（Python）  

```python
from typing import List

def k_or_opt(nums: List[int], k: int) -> int:
    # 第一步：统计每一位出现 1 的次数
    bit_cnt = [0] * 32          # 32 位计数器，初始全为 0
    for x in nums:
        y = x                    # 复制一份，防止修改原数
        while y:                 # 只遍历 y 中为 1 的位
            # 取出最低位的 1，例如 10100 -> 00100
            low_bit = y & -y
            # 计算该位的索引（0 为最低位）
            bit = low_bit.bit_length() - 1
            bit_cnt[bit] += 1    # 对应位计数加 1
            y &= y - 1           # 把最低位的 1 清掉，继续

    # 第二步：根据计数决定结果的每一位
    res = 0
    for bit in range(32):
        if bit_cnt[bit] >= k:    # 出现次数不少于 k，设为 1
            res |= (1 << bit)    # 把 2^bit 加入答案
    return res
```

#### 复杂度  

- **时间复杂度**：`O(n * b)`，其中 `b` 是每个数中 **1 的个数的平均值**。  
  - 最坏情况（所有数都是 `2^31 - 1`，即全部 31 位都是 1）时，`b = 31`，仍然是 `O(31 * n)`，与暴力解同阶。  
  - 实际上，如果数组里的数大多数位为 0，这种写法会更快，因为我们只遍历了出现的 1。  
- **空间复杂度**：`O(1)`（仅用到长度为 32 的固定列表 `bit_cnt`），不随 `n` 增长。

---

## 心得  

- **核心技巧**：**位计数**——统计每一位上 1 出现的次数，再与阈值 `k` 比较。  
- **适用的题型**：  
  1. “**K‑or**” 这类要求“至少 k 个数在该位为 1” 的题目。  
  2. “**位出现次数 ≥ 某值**” 的统计题，例如 LeetCode 1375 “Number of Times Binary String Is Prefix” 的位统计变体。  
  3. “**统计数组中每一位出现次数**” 的题，如 “Maximum AND Sum of Two Subarrays”。  
- **一句话总结**：把每一位当成独立的“投票”，统计票数 ≥ k 即可得到 K‑or。

## 反思  

- **第一反应**：直接把题目描述翻译成“遍历每一位、计数、满足条件就置位”。  
- **最容易踩的坑**：  
  - 忘记处理 **第 31 位**（因为 `nums[i]` 可能接近 `2^31`），所以循环要到 31（共 32 位）。  
  - 使用 `x & (1 << bit)` 判断位时，需要确保左移的位数不超出 Python 整数范围（Python 自动扩展，但保持在 0~31 更安全）。  
  - `k` 可能等于 `len(nums)`，这时只能在所有数都为 1 的位才会置位。  
- **下次遇到同类题**：第一步就想到“**把每一位当作独立的计数器**”，先统计再比较，而不是尝试一次性把所有数合并后再处理。这样思路清晰，代码也容易写对。