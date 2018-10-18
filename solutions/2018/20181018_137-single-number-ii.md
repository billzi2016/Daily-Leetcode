# #137. 只出现一次的数字 II / Single Number II

> 难度：中等 · 标签：Array、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/single-number-ii/)

---

## 题目（英文原版）

**Description**

Given an integer array nums where every element appears three times except for one, which appears exactly once. Find the single element and return it.
You must implement a solution with a linear runtime complexity and use only constant extra space.

**Examples**

**Example 1:**

```
Input: nums = [2,2,3,2]
Output: 3
```

**Example 2:**

```
Input: nums = [0,1,0,1,0,1,99]
Output: 99
```

**Constraints**

- 1 <= nums.length <= 3 * 104
- -231 <= nums[i] <= 231 - 1
- Each element in nums appears exactly three times except for one element which appears once.

---

## 题目（中文翻译）

给定一个整数数组（integer array）`nums`，其中除一个只出现一次的元素外，所有元素均出现三次。找出这个只出现一次的元素并返回。

要求实现的算法 **时间复杂度为线性（linear runtime complexity）**，且只能使用 **常数额外空间（constant extra space）**。

**示例 1**  
输入: `nums = [2,2,3,2]`  
输出: `3`

**示例 2**  
输入: `nums = [0,1,0,1,0,1,99]`  
输出: `99`

**约束条件**  

- `1 <= nums.length <= 3 * 10^4`
- `-2^31 <= nums[i] <= 2^31 - 1`
- `nums` 中每个元素恰好出现三次，唯一例外的是有且仅有一个元素只出现一次。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把数组里每个数字出现的次数都记下来，然后找出只出现一次的那个。  
- **数据结构**：使用 Python 的 `dict`（字典），它就像一本**查字典**：单词是 `key`，对应的页码是 `value`。这里 `key` 是数组里的数字，`value` 是出现的次数。  
- **为什么正确**：只要我们把所有出现次数统计完整，遍历一遍字典即可找到 `value == 1` 的 `key`，这就是唯一只出现一次的数。  

#### 代码（Python）  

```python
def singleNumber(nums):
    # 1. 用字典统计出现次数
    count = {}                      # key: 数字，value: 出现次数
    for x in nums:                  # 遍历数组，每个数都计数
        count[x] = count.get(x, 0) + 1   # 若不存在则默认 0，再加 1

    # 2. 再遍历一次字典，找到只出现一次的数
    for num, freq in count.items():
        if freq == 1:               # 只出现一次的就是答案
            return num
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 解释：我们遍历数组一次（`n` 次）再遍历字典一次，整体仍然和 `n` 成正比。  
- **空间复杂度**：`O(n)`  
  - 解释：最坏情况下数组里每个数都不相同，需要在字典里保存 `n` 条记录，所占空间随 `n` 增长。  

> 这种解法满足 **线性时间** 要求，但没有满足「**常数额外空间**」的限制。下面我们来优化空间。

---  

### 2. 最优解  

#### 思路  

从暴力解出发，瓶颈在于**额外空间**——我们用了一个大小随输入增长的哈希表。  
要把空间降到 `O(1)`，只能使用**固定个数的变量**来完成统计。  
本题的关键是**位运算**（Bit Manipulation），因为整数在计算机里是二进制位的组合。  

**核心观察**  
- 每一位（第 0 位、 第 1 位 …）上，出现三次的数会让该位的“1”出现 3 的倍数次。  
- 唯一只出现一次的数的每一位，要么是 `0`（如果该位在所有数里都是 0），要么是 `1`（如果该位的“1”出现的次数除以 3 余 1）。  

**两种实现思路**  

1. **逐位求和取模**  
   - 对每一位 `i`（0~31），统计所有数在第 `i` 位上出现 `1` 的次数 `sum_i`。  
   - `sum_i % 3` 的结果就是答案在第 `i` 位上的值。  
   - 最后把所有位拼起来得到答案。  
   - 这种做法需要遍历 32 次，每次遍历整个数组，时间仍是 `O(32·n) = O(n)`，空间 `O(1)`。  

2. **状态机（两位计数）**  
   - 用两个整数 `ones`、`twos` 来分别记录「出现一次」和「出现两次」的位的状态。  
   - 当遍历到新数 `x` 时，先把 `twos` 更新为已经出现两次的位：`twos |= ones & x`。  
   - 然后把 `ones` 更新为出现一次的位：`ones ^= x`（异或相当于「出现奇数次」）。  
   - 最后把已经出现三次的位从 `ones`、`twos` 中清除：`common_mask = ~(ones & twos)`，`ones &= common_mask`，`twos &= common_mask`。  
   - 经过所有数后，`ones` 正好保存了只出现一次的数。  

下面给出 **状态机** 的实现，因为它只需要一次遍历，代码更简洁，且易于记忆。  

#### 代码（Python）  

```python
def singleNumber(nums):
    """
    使用位运算的状态机方法，只用两个变量就能找出只出现一次的数。
    ones：记录出现 1 次的位
    twos：记录出现 2 次的位
    当同一位出现 3 次时，both ones 与 twos 都会把它抹掉，实现“模 3”。
    """
    ones, twos = 0, 0          # 初始都为 0，表示没有任何位被计数

    for x in nums:
        # 第一步：把已经出现两次的位记录到 twos 中
        #   - (ones & x) 找到那些在 ones 中已经出现一次且这次又出现的位
        twos = twos | (ones & x)

        # 第二步：更新一次出现的位（异或相当于“出现奇数次”）
        #   - 如果 x 的某位之前没有出现过，则会在 ones 中被置为 1
        #   - 如果该位已经在 ones 中为 1，再次出现会被翻转为 0（相当于出现了第二次）
        ones = ones ^ x

        # 第三步：把出现三次的位全部清零
        #   - (ones & twos) 表示那些已经出现了 3 次的位（因为它们同时在 ones 和 twos 中）
        #   - ~(... ) 取反得到掩码，之后与 ones、twos 与运算把这些位抹掉
        common_mask = ~(ones & twos)
        ones &= common_mask
        twos &= common_mask

    # 循环结束后，ones 中保存的就是只出现一次的数
    return ones
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 解释：只遍历一次数组，对每个元素做固定次数的位运算（都是常数时间），所以整体随 `n` 成正比。  
- **空间复杂度**：`O(1)`  
  - 解释：只使用了 `ones、twos、common_mask` 三个整数，大小不随输入规模变化，属于常数空间。  

与暴力解相比，**时间相同**（都是线性），但**空间从 O(n) 降到了 O(1)**，满足题目「常数额外空间」的要求。

---  

## 心得  

- **核心技巧**：**位运算 + 计数状态机**（把「出现次数模 3」用位的方式实现）。  
- **适用的题型**  
  1. *Single Number*（所有数出现两次，唯一一次出现）——使用异或即可。  
  2. *Single Number II*（出现三次）——本题的状态机或逐位求和取模。  
  3. *Single Number III*（出现两次，两个数只出现一次）——使用异或+分组。  
- **一句话总结**：**把「出现次数」映射到二进制位的「状态」上，用固定的几位变量模拟计数并取模**。  

---  

## 反思  

- **第一反应**：直接想到哈希表计数，写出能跑通的代码。  
- **最容易踩的坑**  
  - **负数的处理**：在 Python 中整数是无限长的，位运算对负数也有效，但要注意最终结果的符号位。状态机实现本身已经兼容负数，无需额外处理。  
  - **位数范围**：如果使用「逐位求和」的思路，需要遍历到 32 位（或 64 位）才能覆盖所有可能的整数范围。  
- **下次遇到同类题**：第一步先判断「出现次数」的模数（2、3、4…），再思考是否可以用 **位运算** 把「计数」压缩到常数个变量上。若模数是 2，直接异或；若是 3，则使用本题的两位状态机；若是更大，可以推广到 `k` 位计数器（使用 `log₂k` 个整数）。