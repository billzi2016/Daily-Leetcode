# #1394. 在数组中寻找幸运整数 / Find Lucky Integer in an Array

> 难度：简单 · 标签：Array、Hash Table、Counting · [LeetCode 链接](https://leetcode.com/problems/find-lucky-integer-in-an-array/)

---

## 题目（英文原版）

**Description**

Given an array of integers arr, a lucky integer is an integer that has a frequency in the array equal to its value.
Return the largest lucky integer in the array. If there is no lucky integer return -1.

**Examples**

**Example 1:**

```
Input: arr = [2,2,3,4]
Output: 2
Explanation: The only lucky number in the array is 2 because frequency[2] == 2.
```

**Example 2:**

```
Input: arr = [1,2,2,3,3,3]
Output: 3
Explanation: 1, 2 and 3 are all lucky numbers, return the largest of them.
```

**Example 3:**

```
Input: arr = [2,2,2,3,3]
Output: -1
Explanation: There are no lucky numbers in the array.
```

**Constraints**

- 1 <= arr.length <= 500
- 1 <= arr[i] <= 500

---

## 题目（中文翻译）

给定一个整数数组 `arr`，若某个整数在数组中的出现次数（frequency）等于它的数值，则称该整数为 **幸运整数**（lucky integer）。  
返回数组中最大的幸运整数。如果数组中不存在幸运整数，返回 `-1`。

**示例 1**  
**示例 2**  
**示例 3**  

**约束条件**

- `1 <= arr.length <= 500`
- `1 <= arr[i] <= 500`

### 示例

#### 示例 1
**输入:** `arr = [2,2,3,4]`  
**输出:** `2`  
**解释:** 唯一的幸运整数是 `2`，因为 `frequency[2] == 2`。

#### 示例 2
**输入:** `arr = [1,2,2,3,3,3]`  
**输出:** `3`  
**解释:** `1、2、3` 都是幸运整数，返回其中最大的 `3`。

#### 示例 3
**输入:** `arr = [2,2,2,3,3]`  
**输出:** `-1`  
**解释:** 数组中不存在幸运整数。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**对每个不同的数，遍历整个数组去统计它出现了多少次**，然后检查“出现次数 == 数的本身”。  
这相当于把数组看成一本书，**每查一次某个词的出现次数，就像从头到尾把整本书重新读一遍**。  
- **数据结构**：只需要数组本身，不需要额外的结构。  
- **正确性**：因为我们对每个可能的幸运整数都完整统计了它的出现频率，若频率恰好等于它的值，就满足题意。  

#### 代码（Python）

```python
def findLucky_brute(arr):
    # 记录所有出现过的不同数字
    candidates = set(arr)          # set 像是把所有不同的词收集起来

    lucky = -1                     # 默认没有幸运整数

    for num in candidates:         # 对每个不同的数字，逐个检查
        cnt = 0
        # 暴力统计 num 在数组中出现的次数
        for x in arr:              # 把整本书重新读一遍
            if x == num:
                cnt += 1

        # 如果出现次数正好等于数字本身，就可能是幸运整数
        if cnt == num:
            lucky = max(lucky, num)   # 取最大的那个

    return lucky
```

#### 复杂度  

- **时间复杂度**：`O(n * m)`，其中 `n = len(arr)`，`m = number of distinct values`。最坏情况下 `m ≈ n`，于是时间是 `O(n²)`，也就是“把整本书读 `n` 次”。  
- **空间复杂度**：`O(m)` 用来存放 `set`，最坏 `O(n)`，相当于只多出一张记录不同词的纸。

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在于**每次都要遍历整个数组来统计频率**。我们可以把统计工作一次性完成，然后直接查询。  
- **第一步**：一次遍历数组，记录每个数字出现了多少次。这里可以使用 **哈希表**（在 Python 中是 `dict`），它就像是一本“词典”，`key` 是数字，`value` 是出现次数。  
- **第二步**：遍历哈希表的键，找出满足 `frequency == number` 的数字，取最大值。  

由于题目给出的数值范围 `1 ≤ arr[i] ≤ 500`，我们甚至可以用长度为 501 的列表直接当作计数器，这比哈希表更省空间且更快（下标就是数字本身）。  

**核心技巧**：**计数（Counting）**——一次遍历把所有频率都算好，后面再直接比较。

#### 代码（Python）

```python
def findLucky(arr):
    # 计数数组，下标 i 表示数字 i 出现的次数
    # 因为题目限制数字最大是 500，所以长度取 501（0 位不使用）
    freq = [0] * 501

    # 第一步：一次遍历统计频率
    for num in arr:               # 把整本书只读一遍，就把每个词的出现次数记下来
        freq[num] += 1            # freq[num] 像是词典里记录的页码

    lucky = -1                     # 默认没有幸运整数

    # 第二步：遍历所有可能的数字，找出符合条件的最大值
    for num in range(1, 501):      # 只需要检查 1~500
        if freq[num] == num:       # 出现次数恰好等于数字本身
            lucky = max(lucky, num)   # 取最大的那个

    return lucky
```

#### 复杂度  

- **时间复杂度**：`O(n + M)`，其中 `n = len(arr)`，`M = 500`（常数）。我们只遍历一次数组（`O(n)`），再遍历一次固定长度的计数表（`O(500)`），整体几乎是线性 `O(n)`。相比暴力的 `O(n²)`，快了很多。  
- **空间复杂度**：`O(M)`，这里是 `501` 的整数列表，固定大小，不随输入规模增长。相当于只准备了一张长度为 501 的“记事本”。

---

## 心得

- **核心技巧**：**计数（Counting）**——一次遍历把每个元素出现的次数记录下来，然后利用这些信息直接求解。  
- **适用的题型**：  
  1. “出现次数等于自身”类（如本题）。  
  2. “出现次数超过 K 次”或“出现次数恰好为 K 次”的统计题。  
  3. “找出出现频率最高的元素”或“众数”问题。  
- **一句话总结**：**把所有频率一次算完，再一次查表，就能把暴力的“遍历‑遍历”压缩成“遍历‑查表”。**

---

## 反思

- **第一反应**：看到“频率”和“数值相等”，自然想到统计每个数出现多少次。  
- **最容易踩的坑**：  
  - 忘记 **只统计出现过的数字**，而是遍历整个 `freq`（虽然这里是常数范围，但在更大范围时会浪费时间）。  
  - 没有处理 **没有幸运整数** 的情况，直接返回了 `0` 而不是 `-1`。  
  - 对于 `arr[i]` 超出 500 的情况，计数数组会越界，需要使用哈希表做通用解。  
- **下次遇到同类题**，第一步应该想到 **“先计数，再筛选”**，把频率信息一次性准备好，后面的判断就可以 O(1) 完成。