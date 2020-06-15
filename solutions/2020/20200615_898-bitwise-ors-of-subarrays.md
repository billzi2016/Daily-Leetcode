# #898. 子数组的按位或 / Bitwise ORs of Subarrays

> 难度：中等 · 标签：Array、Dynamic Programming、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/bitwise-ors-of-subarrays/)

---

## 题目（英文原版）

**Description**

Given an integer array arr, return the number of distinct bitwise ORs of all the non-empty subarrays of arr.
The bitwise OR of a subarray is the bitwise OR of each integer in the subarray. The bitwise OR of a subarray of one integer is that integer.
A subarray is a contiguous non-empty sequence of elements within an array.

**Examples**

**Example 1:**

```
Input: arr = [0]
Output: 1
Explanation: There is only one possible result: 0.
```

**Example 2:**

```
Input: arr = [1,1,2]
Output: 3
Explanation: The possible subarrays are [1], [1], [2], [1, 1], [1, 2], [1, 1, 2].
These yield the results 1, 1, 2, 1, 3, 3.
There are 3 unique values, so the answer is 3.
```

**Example 3:**

```
Input: arr = [1,2,4]
Output: 6
Explanation: The possible results are 1, 2, 3, 4, 6, and 7.
```

**Constraints**

- 1 <= arr.length <= 5 * 104
- 0 <= arr[i] <= 109

---

## 题目（中文翻译）

给定一个整数数组 `arr`，返回 `arr` 所有非空子数组（subarray）的按位或（bitwise OR）结果的不同值的数量。  
子数组的按位或是指该子数组中每个整数的按位或的结果。单个整数构成的子数组的按位或即为该整数本身。  
子数组是数组中连续的、非空的元素序列。

### 示例

**示例 1**  
输入: `arr = [0]`  
输出: `1`  
解释: 只有唯一一种可能的结果：`0`。

**示例 2**  
输入: `arr = [1,1,2]`  
输出: `3`  
解释: 所有可能的子数组为 `[1]`, `[1]`, `[2]`, `[1,1]`, `[1,2]`, `[1,1,2]`。  
这些子数组的按位或分别得到 `1, 1, 2, 1, 3, 3`。  
不同的结果有 `1、2、3` 三个，所以答案为 `3`。

**示例 3**  
输入: `arr = [1,2,4]`  
输出: `6`  
解释: 所有可能的结果为 `1, 2, 3, 4, 6, 7`。

### 约束条件

- `1 <= arr.length <= 5 * 10^4`
- `0 <= arr[i] <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法就是把 **所有子数组** 都枚举一遍，求出它们的按位或（OR），最后把得到的结果放进集合（`set`）去重。  

- **子数组**：数组里连续的一段，例如 `[1,2,4]` 的子数组有 `[1]、[2]、[4]、[1,2]、[2,4]、[1,2,4]`。  
- **按位或**：把两个整数的二进制位做“或”运算，任意一位上只要有一个是 1，结果那位就是 1。可以把它想象成 **“把两个字典的词条合并，只要出现过的字母就保留下来”**。  
- **集合去重**：Python 中的 `set` 就像一本 **“不允许出现重复页码的字典”**，把所有得到的 OR 值放进去，最后集合的大小就是答案。

**为什么正确**  
暴力遍历不遗漏任何子数组，所有可能的 OR 值都会被算出来并加入集合，自然得到的就是所有**不同**的 OR 结果数。

**时间/空间复杂度**  
- **时间**：枚举子数组需要两层循环，外层遍历起点 `i`（`n` 次），内层遍历终点 `j`（最坏情况也是 `n` 次），每次把 `arr[i…j]` 的 OR 逐步累加 → **O(n²)**。  
  - 大白话：如果数组长度是 10,000，粗略估计要做 10,000 × 10,000 ≈ 1 亿 次运算，明显会超时。  
- **空间**：除了保存答案的集合外，只用了常数级别的临时变量 → **O(1)**（不计答案集合本身的大小）。

#### 代码（Python）

```python
from typing import List

def subarrayBitwiseORs_brute(arr: List[int]) -> int:
    n = len(arr)
    distinct = set()                     # 用来存放所有出现过的 OR 值

    for i in range(n):                   # 子数组的左端点
        cur = 0
        for j in range(i, n):            # 子数组的右端点，逐步扩展
            cur |= arr[j]                # 按位或累计，等价于把 arr[i..j] 全部 OR 在一起
            distinct.add(cur)            # 把得到的结果放进集合，自动去重

    return len(distinct)                 # 集合大小即为不同的 OR 值个数
```

#### 复杂度  

- **时间复杂度**：`O(n²)` —— 两层循环遍历所有子数组。  
- **空间复杂度**：`O(1)`（不计答案集合）—— 只用了常数个额外变量。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在 **“枚举所有子数组”**，这一步导致二次循环。  
观察 **按位或的性质**：

1. 对同一个子数组不断往右扩展时，OR 只能 **“添砖加瓦”**，即二进制位只能从 0 变成 1，永远不会再变回 0。  
2. 因此，**从左到右遍历数组** 时，所有以当前位置 `i` 结尾的子数组的 OR 值，只可能是  
   - 只含 `arr[i]` 本身  
   - 前面某个位置的 OR 再与 `arr[i]` 做 OR  
   换句话说，**只需要记住上一次（以 i‑1 结尾）的所有 OR 结果**，再和 `arr[i]` 合并，就能得到以 `i` 结尾的所有可能 OR。  

设 `prev` 为 **所有以 `i-1` 为右端点的子数组的 OR 集合**，则  

```
cur = { arr[i] } ∪ { x | arr[i]  for x in prev }
```

`cur` 的大小不会太大：因为每次做 OR 至少会把某些 0 位变成 1 位，最多 32（或 30）次变位后就不可能再产生新值。  
所以 **整体时间** 为 `O(n * 30)`，在本题的约束下完全可以接受。

**实现细节**  

- 用两个集合交替保存 `prev` 与 `cur`，每次遍历一个元素时更新 `cur`。  
- 同时把 `cur` 中的所有值加入全局集合 `ans`，最终答案就是 `len(ans)`。  
- 为了避免在循环中产生重复的 OR 值（同一个值可能由不同的前缀得到），使用 `set` 自动去重。

#### 代码（Python）

```python
from typing import List

def subarrayBitwiseORs(arr: List[int]) -> int:
    ans = set()          # 存放所有出现过的 OR 结果
    prev = set()         # 记录上一次（以 i-1 为结尾）的所有 OR

    for num in arr:      # 从左到右遍历数组
        cur = {num}      # 只含当前元素的子数组
        # 把所有以 i-1 为结尾的子数组的 OR 再和当前元素做 OR
        for x in prev:
            cur.add(x | num)
        ans.update(cur)  # 把本轮得到的所有 OR 放进全局集合
        prev = cur       # 为下一轮准备

    return len(ans)
```

**代码解释（逐行注释）**  

- `ans = set()`：最终答案集合，类似一本“所有出现过的页码的字典”。  
- `prev = set()`：上一轮的 OR 集合，记录“上一次能到达的所有状态”。  
- `for num in arr:`：遍历每个元素，视作当前子数组的最右端。  
- `cur = {num}`：子数组只含当前元素时的 OR，必然是它本身。  
- `for x in prev: cur.add(x | num)`：把所有以 `num` 前面位置结尾的 OR 再和 `num` 合并，得到新的子数组 OR。  
- `ans.update(cur)`：把本轮产生的所有 OR 加入答案集合。  
- `prev = cur`：把本轮结果保存，供下一次循环使用。  

#### 复杂度  

- **时间复杂度**：`O(n * B)`，其中 `B` 为整数的二进制位数（本题 `B ≤ 30`），实际约等于 `O(n)`。  
  - 大白话：每遍历一个元素，只会产生最多 30 个新 OR 值，所以即使数组长 5×10⁴，也只会做大约 1.5 百万次运算，十分轻松。  
- **空间复杂度**：`O(K)`，`K` 为所有不同 OR 值的个数，最坏也不会超过 `n * B`，在本题约为 `1.5 × 10⁶` 以下，实际更少。  
  - 这里的额外空间主要是集合 `ans` 与 `prev/cur`，都与输入规模线性相关。

---

## 心得  

- **核心技巧**：利用 **按位或的单调性**（只会把 0 变成 1）和 **动态规划的“状态压缩”**，只保留以当前位置结尾的所有可能 OR。  
- **适用题型**：  
  1. “子数组/子序列的所有可能结果” 类问题（如 *Subarray Bitwise ANDs*、*Subarray Minimums*）。  
  2. “使用位运算或其他单调操作” 的集合遍历（如 *Maximum XOR of Two Numbers in an Array*）。  
- **一句话总结**：**“把‘所有子数组’的遍历压缩到‘以当前位置结尾的状态集合’”**，就是这道题的解题钥匙。

---

## 反思  

- **第一反应**：直接暴力枚举所有子数组，代码很快写出来，但会担心会超时。  
- **最容易踩的坑**：  
  - 忘记使用集合去重，导致答案计数错误。  
  - 在优化思路中遗漏了 `num` 本身的情况（只有当前元素的子数组）。  
  - 没考虑整数的位数上限，误以为会产生指数级别的状态。  
- **下次类似题的第一步**：先问自己“这个操作（OR、AND、最大值等）在不断扩展子数组时是否单调”，如果是，就尝试 **“只记录以当前位置结尾的状态集合”**，从而把二次遍历降到线性。