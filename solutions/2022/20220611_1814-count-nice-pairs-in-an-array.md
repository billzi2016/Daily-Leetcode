# #1814. 数组中美好数对计数 / Count Nice Pairs in an Array

> 难度：中等 · 标签：Array、Hash Table、Math、Counting · [LeetCode 链接](https://leetcode.com/problems/count-nice-pairs-in-an-array/)

---

## 题目（英文原版）

**Description**

You are given an array nums that consists of non-negative integers. Let us define rev(x) as the reverse of the non-negative integer x. For example, rev(123) = 321, and rev(120) = 21. A pair of indices (i, j) is nice if it satisfies all of the following conditions:
Return the number of nice pairs of indices. Since that number can be too large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: nums = [42,11,1,97]
Output: 2
Explanation: The two pairs are:
 - (0,3) : 42 + rev(97) = 42 + 79 = 121, 97 + rev(42) = 97 + 24 = 121.
 - (1,2) : 11 + rev(1) = 11 + 1 = 12, 1 + rev(11) = 1 + 11 = 12.
```

**Example 2:**

```
Input: nums = [13,10,35,24,76]
Output: 4
```

**Constraints**

- 1 <= nums.length <= 105
- 0 <= nums[i] <= 109

---

## 题目（中文翻译）

**题目描述**

给定一个只包含非负整数的数组 `nums`。定义 `rev(x)` 为非负整数 `x` 的逆序，例如 `rev(123) = 321`，`rev(120) = 21`。若一对索引 `(i, j)` 满足以下全部条件，则称其为 **美好数对**（nice pair）：

1. `0 <= i < j < nums.length`
2. `nums[i] + rev(nums[j]) == nums[j] + rev(nums[i])`

请返回美好数对的数量。由于答案可能非常大，返回结果对 `10^9 + 7` 取模。

**示例**

示例 1  
Input: `nums = [42,11,1,97]`  
Output: `2`  
Explanation: 这两个美好数对为：
- `(0,3)`：`42 + rev(97) = 42 + 79 = 121`，`97 + rev(42) = 97 + 24 = 121`。  
- `(1,2)`：`11 + rev(1) = 11 + 1 = 12`，`1 + rev(11) = 1 + 11 = 12`。

示例 2  
Input: `nums = [13,10,35,24,76]`  
Output: `4`

**约束条件**

- `1 <= nums.length <= 10^5`
- `0 <= nums[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**枚举所有**下标对 `(i, j)`（`i < j`），检查题目给出的等式是否成立：

```
nums[i] + rev(nums[j]) == nums[j] + rev(nums[i])
```

- **用到的数据结构**：  
  - `list`（数组）直接存放 `nums`。  
  - `rev(x)` 用一个普通函数把整数的十进制位倒过来，这相当于在字典里查词：`x` 是“词”，倒过来的数是“词义”。  
- **为什么正确**：  
  只要把所有可能的 `(i, j)` 都算一遍，凡是满足等式的就一定是“好对”。没有遗漏，也不会多算。  
- **时间/空间复杂度**：  
  - 我们要检查 `C(n,2) = n·(n-1)/2` 对下标，时间随 `n` 的平方增长，用大白话说就是“如果数组长度是 10,000，循环次数大概是 50,000,000”。这就是 **O(n²)**。  
  - 只用到常数级别的额外空间（存放 `rev` 函数的临时变量），所以是 **O(1)**。

#### 代码（Python）

```python
MOD = 10 ** 9 + 7

def rev(x: int) -> int:
    """把整数 x 的十进制位倒过来，例如 rev(120) = 21"""
    return int(str(x)[::-1])          # 把数字转成字符串，翻转后再转回整数

def countNicePairs_bruteforce(nums):
    n = len(nums)
    ans = 0
    for i in range(n):
        for j in range(i + 1, n):
            # 检查题目等式
            if nums[i] + rev(nums[j]) == nums[j] + rev(nums[i]):
                ans += 1
                ans %= MOD               # 防止结果太大
    return ans
```

#### 复杂度

- **时间复杂度：O(n²)** — 随着数组长度 `n` 增大，运算次数大约是 `n` 的平方，`n = 10⁵` 时根本跑不完。  
- **空间复杂度：O(1)** — 只用了几个整数变量，额外占用的内存不随 `n` 增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于两层循环——我们每次都要重复计算 `rev(nums[i])`，而且比较的是两个数的和。  
把等式两边同减 `rev(nums[i]) + rev(nums[j])`，得到等价的**更简洁的形式**：

```
nums[i] - rev(nums[i]) == nums[j] - rev(nums[j])
```

这说明，只要把每个元素 **映射** 成一个新值  

```
key_i = nums[i] - rev(nums[i])
```

那么满足条件的好对就是 **key 相同的下标对**。  
于是问题转化为：

> 在数组 `keys` 中，有多少对下标 `(i, j)`（i<j）使得 `keys[i] == keys[j]`？

这正是“计数相同元素的组合数”。  
我们只需遍历一次数组，维护一个 **哈希表**（Python 的 `dict`），记录每个 `key` 出现的次数：

1. 对当前 `key`，如果哈希表里已经出现过 `cnt` 次，则这 `cnt` 个之前的下标都可以和当前下标组成好对，答案加 `cnt`。  
2. 再把哈希表中 `key` 的计数加一，表示自己也加入到了“已见”集合。

这样只需要 **一次线性遍历**，时间从 O(n²) 降到 **O(n)**。

- **核心数据结构**：哈希表（字典）。可以把它想象成“查字典”：单词是 `key`，对应的页码是出现次数。查找、插入都是 O(1)。  
- **为什么正确**：因为我们已经把原来的等式完整等价地转化成 `key` 相等的条件，哈希表正好帮我们统计每个 `key` 出现的次数，从而直接得到配对数目。

#### 代码（Python）

```python
MOD = 10 ** 9 + 7

def rev(x: int) -> int:
    """返回整数 x 的十进制反转，例如 rev(120) = 21"""
    return int(str(x)[::-1])

def countNicePairs(nums):
    """
    最优解：只遍历一次数组，利用哈希表统计 (num - rev(num)) 的出现次数。
    """
    freq = {}               # key -> 已出现的次数
    ans = 0

    for num in nums:
        key = num - rev(num)          # 把每个元素映射成唯一的 key
        cnt = freq.get(key, 0)        # 之前出现过多少次相同的 key
        ans = (ans + cnt) % MOD       # 这些 cnt 个下标都可以和当前下标配对
        freq[key] = cnt + 1           # 当前下标也加入统计

    return ans
```

#### 复杂度

- **时间复杂度：O(n)** — 只遍历一次数组，哈希表的查询/插入都是常数时间。对于 `n = 10⁵` 完全可以在毫秒级完成。  
- **空间复杂度：O(n)** — 最坏情况下每个 `key` 都不相同，需要存 `n` 条记录。相当于“装下所有不同单词的字典”。

---

## 心得

- **核心技巧**：把原始等式转化为“差值相等”，然后利用哈希表统计相同值的出现次数。  
- **适用的题型**：  
  1. “相等差值/和/乘积的配对”——如 *Count Good Pairs*、*Number of Pairs With Absolute Difference K*。  
  2. “把元素映射成某个特征值后计数”——如 *Longest Subarray With Equal Number of 0s and 1s*（映射 0→-1）。  
- **一句话总结**：**把等式化简成“相同特征值”，用哈希表一次遍历计数**。

---

## 反思

- **第一反应**：看到“rev”会想到要把每个数字翻转，随后想到直接枚举所有下标对。  
- **最容易踩的坑**：  
  - 忘记 **模 10⁹+7**，导致答案溢出。  
  - `rev(0)` 必须返回 `0`，否则会出现错误的差值。  
  - 负数的差值 `num - rev(num)` 可能为负，哈希表的键可以是负数，别误以为只能是正数。  
- **下次类似题的第一步**：**把题目条件写成等价的“某个函数值相等”形式**，然后思考是否能用哈希表统计出现次数来直接求答案。