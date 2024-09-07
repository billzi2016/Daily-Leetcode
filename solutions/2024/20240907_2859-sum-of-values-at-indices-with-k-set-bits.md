# #2859. 索引二进制中恰有 K 个置位的元素之和 / Sum of Values at Indices With K Set Bits

> 难度：简单 · 标签：Array、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/sum-of-values-at-indices-with-k-set-bits/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums and an integer k.
Return an integer that denotes the sum of elements in nums whose corresponding indices have exactly k set bits in their binary representation.
The set bits in an integer are the 1's present when it is written in binary.

**Examples**

**Example 1:**

```
Input: nums = [5,10,1,5,2], k = 1
Output: 13
Explanation: The binary representation of the indices are: 
0 = 0002
1 = 0012
2 = 0102
3 = 0112
4 = 1002 
Indices 1, 2, and 4 have k = 1 set bits in their binary representation.
Hence, the answer is nums[1] + nums[2] + nums[4] = 13.
```

**Example 2:**

```
Input: nums = [4,3,2,1], k = 2
Output: 1
Explanation: The binary representation of the indices are:
0 = 002
1 = 012
2 = 102
3 = 112
Only index 3 has k = 2 set bits in its binary representation.
Hence, the answer is nums[3] = 1.
```

**Constraints**

- 1 <= nums.length <= 1000
- 1 <= nums[i] <= 105
- 0 <= k <= 10

---

## 题目（中文翻译）

给定一个 **0 索引** 整数数组 `nums` 和一个整数 `k`。  
返回一个整数，表示 `nums` 中所有 **对应索引的二进制表示（binary representation）** 恰好包含 `k` 个 **置位（set bits）** 的元素之和。

**置位** 指的是整数在二进制表示中为 `1` 的位数。

---

## 示例

### 示例 1
**输入**  
```text
nums = [5,10,1,5,2], k = 1
```
**输出**  
```text
13
```
**解释**  
索引的二进制表示为：  
```
0 = 000₂
1 = 001₂
2 = 010₂
3 = 011₂
4 = 100₂
```
索引 `1、2、4` 的二进制中恰有 `k = 1` 个置位。  
因此答案为 `nums[1] + nums[2] + nums[4] = 13`。

### 示例 2
**输入**  
```text
nums = [4,3,2,1], k = 2
```
**输出**  
```text
1
```
**解释**  
索引的二进制表示为：  
```
0 = 00₂
1 = 01₂
2 = 10₂
3 = 11₂
```
只有索引 `3` 的二进制中有 `k = 2` 个置位。  
所以答案为 `nums[3] = 1`。

---

## 约束条件
- `1 <= nums.length <= 1000`
- `1 <= nums[i] <= 10^5`
- `0 <= k <= 10`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法就是把 **每一个下标** `i` 都拿出来，看看它的二进制里有几个 `1`（即“集合位”），如果恰好等于给定的 `k`，就把 `nums[i]` 累加到答案中。

- **数据结构**：只需要遍历数组本身，另外用一个整数变量 `cnt` 来记录当前下标的 `1` 的个数。  
  - 把整数的二进制想象成一本**字典**，每一位是一个单词，“1” 就是出现的词，数一数出现了多少次就行了。
- **为什么正确**：题目要求的正是“下标的二进制中恰好有 `k` 个 1”，我们逐个检查，所有满足条件的下标必然会被累加，所有不满足的下标不会被计入，答案自然正确。

#### 代码（Python）

```python
def sumIndicesWithKSetBits(nums, k):
    """
    暴力遍历所有下标，统计每个下标的 1 的个数
    """
    total = 0                         # 用来累计答案
    n = len(nums)

    for i in range(n):                # 逐个检查下标 i
        # 统计 i 的二进制中 1 的个数
        # 方法一：直接使用 Python 的内置函数 bit_count（Python 3.8+）
        # cnt = i.bit_count()
        # 方法二：手动计数（兼容所有版本）
        cnt = 0
        x = i
        while x:                      # 当 x 不为 0 时循环
            cnt += x & 1              # x & 1 取最低位，若为 1 则计数加一
            x >>= 1                   # 右移一位，继续检查下一位

        if cnt == k:                   # 正好有 k 个 1
            total += nums[i]           # 累加对应的数组元素

    return total
```

#### 复杂度  

- **时间复杂度**：`O(n * log n)`  
  - `n` 是数组长度。对每个下标 `i`，我们需要查看它的二进制位数，最多是 `log₂ i`（即整数的位数），所以总共大约是 `n` 乘以 `log n` 次操作。  
  - 用大白话说，就是如果数组有 1000 个元素，每个元素最多检查 10 位（二进制），总共大约检查 10000 次，算是“稍微有点慢”。
- **空间复杂度**：`O(1)`  
  - 只用了常数级别的额外变量 `total、cnt、x`，不随输入规模增长。

---  

### 2. 最优解

#### 思路  

从暴力解可以看出，**瓶颈** 在于每次都要重新统计下标的 `1` 的个数。其实，**相邻的下标之间的二进制只差一点**（`i` → `i+1`），我们可以利用这个关系把计数过程“递推”下来，做到 **一次遍历即可**。

**核心技巧：**  
- **位计数的递推公式**  
  - 对任意非负整数 `i`，`i` 的二进制 `1` 的个数（记作 `popcount(i)`）可以用下面的式子快速算出：  
    ```
    popcount(i) = popcount(i >> 1) + (i & 1)
    ```
    - `i >> 1` 表示把 `i` 右移一位，相当于把最低位丢掉。  
    - `(i & 1)` 取出最低位的值，要么是 0 要么是 1，正好是这位是否为 `1`。  
  - 换句话说，`i` 的 `1` 的个数 = “把 `i` 去掉最低位后剩下的 `1` 的个数” + “最低位是不是 1”。  
- **从 0 开始递推**：我们可以先把 `popcount(0)` 设为 0，然后顺序遍历 `i = 1 … n-1`，每次使用上面的公式得到 `popcount(i)`，时间只需要 `O(1)`。

**类比**：把每个下标的二进制想象成一串灯泡，右移相当于把最左边的灯泡“搬走”。我们只需要记住搬走前的灯泡数量，加上搬走的那盏灯是否亮着（1）即可得到新的灯泡数量。

#### 代码（Python）

```python
def sumIndicesWithKSetBits(nums, k):
    """
    使用递推的方式一次遍历求出所有下标的 1 的个数，
    时间 O(n)，空间 O(1)。
    """
    n = len(nums)
    total = 0                # 最终答案
    pop = [0] * n            # pop[i] 保存下标 i 的 1 的个数（可省略，只保留前一个值也行）

    for i in range(n):
        if i == 0:
            pop[i] = 0                     # 0 的二进制是 0，没有 1
        else:
            # 递推公式：pop[i] = pop[i >> 1] + (i & 1)
            pop[i] = pop[i >> 1] + (i & 1)

        # 如果当前下标的 1 的个数恰好等于 k，就把对应元素加入答案
        if pop[i] == k:
            total += nums[i]

    return total
```

> **小技巧**：如果使用 Python 3.8 以上的版本，直接写 `i.bit_count()` 就等价于上面的递推，代码更简洁，但这里演示递推是为了帮助大家理解“从前一个结果快速得到下一个结果”的思想。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历一次数组，每个下标的 `popcount` 通过常数时间的递推得到。相较于暴力解的 `O(n·log n)`，这里把“每个下标要检查多少位”这一步省掉了，真正只跟元素个数成线性关系。  
- **空间复杂度**：`O(1)`（若把 `pop` 数组改成单个变量）  
  - 只用了几个整数变量。如果不需要保存所有 `pop[i]`，可以把 `pop[i]` 用一个临时变量 `cnt` 直接覆盖，进一步压缩空间。

---

## 心得

- **核心技巧**：利用**位运算的递推**（`popcount(i) = popcount(i>>1) + (i&1)`）一次遍历完成所有下标的 1 位计数。  
- **适用题型**  
  1. “统计数组下标/数值的二进制 1 的个数”类题目（如 LeetCode 338. Counting Bits）。  
  2. 需要根据 **位计数** 分类求和或计数的题目（如 “按位计数分组求和”）。  
  3. 任何涉及“子集枚举”“状态压缩”时，需要快速得到某个状态的 1 的个数。  
- **一句话总结**：**“相邻整数的二进制只差一位，利用递推把位计数从 O(log n) 降到 O(1)”。**

---

## 反思

- **第一反应**：看到“下标的二进制里有 k 个 1”，自然想到**遍历下标、逐个计数**。这就是暴力解的雏形。  
- **最容易踩的坑**  
  1. **边界条件**：`k` 可能为 `0`，此时只有下标 `0`（二进制全是 0）会被计入，需要确保代码能够正确处理。  
  2. **位数不足**：如果直接用 `bin(i).count('1')`，在极端情况下（如 `i` 很大）仍然能工作，但要注意 `bin` 会产生字符串，效率稍低。  
  3. **空间误用**：不需要额外的数组保存所有 `popcount`，否则会把原本 `O(1)` 的空间浪费成 `O(n)`。  
- **下次遇到同类题**：第一步先问自己“相邻状态之间有什么简单的关系？”如果答案是“只差一位”，就尝试写出递推公式，把计数过程压到常数时间。这样往往能从“暴力”直接跳到“最优”。