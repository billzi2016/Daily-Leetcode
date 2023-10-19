# #2442. 反转操作后不同整数的数量 / Count Number of Distinct Integers After Reverse Operations

> 难度：中等 · 标签：Array、Hash Table、Math、Counting · [LeetCode 链接](https://leetcode.com/problems/count-number-of-distinct-integers-after-reverse-operations/)

---

## 题目（英文原版）

**Description**

You are given an array nums consisting of positive integers.
You have to take each integer in the array, reverse its digits, and add it to the end of the array. You should apply this operation to the original integers in nums.
Return the number of distinct integers in the final array.

**Examples**

**Example 1:**

```
Input: nums = [1,13,10,12,31]
Output: 6
Explanation: After including the reverse of each number, the resulting array is [1,13,10,12,31,1,31,1,21,13].
The reversed integers that were added to the end of the array are underlined. Note that for the integer 10, after reversing it, it becomes 01 which is just 1.
The number of distinct integers in this array is 6 (The numbers 1, 10, 12, 13, 21, and 31).
```

**Example 2:**

```
Input: nums = [2,2,2]
Output: 1
Explanation: After including the reverse of each number, the resulting array is [2,2,2,2,2,2].
The number of distinct integers in this array is 1 (The number 2).
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 106

---

## 题目（中文翻译）

给定一个只包含正整数的数组 `nums`。  
你需要对数组中的每个整数，**将其数字逆序**（reverse its digits），并将得到的逆序整数追加到数组的末尾。此操作只针对原始的 `nums` 中的整数进行。  
返回最终数组中 **不同整数的数量**（number of distinct integers）。

## 示例

### 示例 1
**输入**  
`nums = [1,13,10,12,31]`

**输出**  
`6`

**解释**  
在每个数后面加入其逆序数后，得到的数组为  
`[1,13,10,12,31,1,31,1,21,13]`。  
添加到数组末尾的逆序整数已用下划线标出。需要注意的是，整数 `10` 逆序后得到 `01`，即 `1`。  
该数组中不同的整数共有 6 个，分别是 `1, 10, 12, 13, 21, 31`。

### 示例 2
**输入**  
`nums = [2,2,2]`

**输出**  
`1`

**解释**  
加入每个数的逆序数后，得到的数组为  
`[2,2,2,2,2,2]`。  
数组中唯一的不同整数是 `2`，因此答案为 1。

## 约束条件

- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^6`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
题目要求把数组 `nums` 中的每个正整数 **倒置**（把十进制的各位数字反过来），并把倒置后的数再放回数组的末尾，最后统计数组里有多少 **不同** 的整数。

最直接的想法就是：

1. **遍历** `nums`，对每个数 `x`  
   - 先把 `x` 放进一个容器（用来记 “出现过的数”）。  
   - 再把 `x` 的倒置 `rev(x)` 放进同一个容器。  
2. 最后容器里元素的个数，就是答案。

> **哈希表（set）** 就像一本“查字典”。字典里每个单词（key）只会出现一次，想记住出现过的数字，我们只需要把数字当作“单词”，把它们塞进这本字典里，重复的自然会被自动去重。

**为什么正确**  
- 每个原始数字一定会出现在最终数组里。  
- 每个原始数字的倒置也一定会出现在最终数组里（题目明确要求把倒置数加到数组末尾）。  
- 把这两类数字全部放进集合，集合天然去重，集合的大小恰好等于“不同整数的个数”。  

**复杂度分析（大白话）**  
- **时间**：我们要遍历 `n` 个数，每个数倒置一次。倒置的过程相当于把数字的每一位拿出来，最多 7 位（因为 `nums[i] ≤ 10⁶`），所以时间是 `n × 7`，即 **O(n)**。  
- **空间**：集合最坏会存下所有原始数和它们的倒置，最多 `2n` 个整数，仍然是 **O(n)** 的额外空间。  

#### 代码（Python）

```python
def reverse_number(x: int) -> int:
    """
    把整数 x 的十进制位倒置，例如 120 -> 21
    思路：把 x 当作字符串，翻转后再转回整数
    """
    return int(str(x)[::-1])          # 字符串切片[::-1]实现翻转

def countDistinctIntegers(nums):
    """
    暴力思路：遍历 nums，把每个数和它的倒置都放进集合
    最后返回集合的大小
    """
    seen = set()                      # 哈希集合，自动去重
    for x in nums:
        seen.add(x)                    # 原始数
        seen.add(reverse_number(x))    # 倒置数
    return len(seen)                  # 集合元素个数 = 不同整数个数
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - `n` 为数组长度。每个数的倒置只涉及最多 7 次字符操作，常数级别。  
- **空间复杂度**：`O(n)`  
  - 需要额外的集合来保存出现过的数，最坏保存 `2n` 个元素，仍然是线性空间。

---  

### 2. 最优解  

#### 思路  
从暴力解来看，唯一的“耗时”步骤是 **倒置数字**。但倒置本身已经是最简 O(位数) 的做法，位数 ≤ 7，几乎可以忽略不计。  
因此，真正的瓶颈只可能是 **重复遍历或额外的存储**。  
- 如果我们在遍历时把倒置数直接加入集合，而不是先生成一个新列表再遍历两遍，就已经达到了最优。  
- 这正是上面的实现：一次遍历、一次集合插入，时间和空间都已经是线性最优。  

没有更快的算法能在 **不查看每个元素** 的前提下得到答案，因为每个元素（以及它的倒置）都有可能是唯一的，需要“看一眼”。  

**核心数据结构**：**集合（set）**  
- 类比查字典：把每个数当成词条，放进去后自然去重。  
- 插入、查询、统计大小的时间都是 **O(1)**（均摊意义上），所以整体保持线性。

#### 代码（Python）

```python
def countDistinctIntegers(nums):
    """
    最优实现：一次遍历 + set 去重
    """
    distinct = set()
    for x in nums:
        distinct.add(x)                       # 原数
        # 直接在这里算倒置并加入集合
        distinct.add(int(str(x)[::-1]))       # 倒置数
    return len(distinct)
```

> **小技巧**：如果你不想每次都把整数转成字符串，也可以用数学方式倒置（循环取余），但在 Python 中字符串切片已经非常高效，代码更简洁。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历一次数组，每次集合插入均摊是常数时间。  
- **空间复杂度**：`O(n)`  
  - 最多存 `2n` 个整数，仍是线性空间。  
- 与暴力解相比，**没有任何额外的遍历或中间容器**，是最紧凑的实现。

---  

## 心得  

- **核心技巧**：使用 **集合**（哈希表）实现去重。  
- **适用场景**：  
  1. “统计数组/字符串中不同元素的个数”。  
  2. “把某种变换（翻转、取反、映射等）后的结果也算进去”。  
  3. “判断两个数组是否有相同元素”——可以把一个数组放进集合，再遍历另一个数组查是否存在。  
- **解题钥匙**：**“遍历 + 哈希去重”**。

---  

## 反思  

- **第一反应**：看到“倒置后再加入”，自然想到把每个数和它的倒置都记下来，集合是最直接的工具。  
- **最容易踩的坑**：  
  - **倒置后出现前导零**：比如 `10` 倒置成 `"01"`，转回整数后会变成 `1`，这正是题目要求的行为，使用 `int(str(x)[::-1])` 能自动去掉前导零。  
  - **重复元素**：原数组本身可能有重复，需要一次遍历把原数和倒置数都加入同一个集合，别忘了把原数也计入。  
- **下次类似题的第一步**：  
  - 明确“要统计多少种不同的东西”。  
  - 想一个 **“一遍遍历 + 哈希去重”** 的方案；如果还有额外的变换（翻转、取模、映射），就在遍历中同步完成。