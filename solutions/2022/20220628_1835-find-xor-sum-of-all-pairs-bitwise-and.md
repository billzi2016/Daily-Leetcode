# #1835. 求所有配对按位与的 XOR 和 / Find XOR Sum of All Pairs Bitwise AND

> 难度：困难 · 标签：Array、Math、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/find-xor-sum-of-all-pairs-bitwise-and/)

---

## 题目（英文原版）

**Description**

The XOR sum of a list is the bitwise XOR of all its elements. If the list only contains one element, then its XOR sum will be equal to this element.
You are given two 0-indexed arrays arr1 and arr2 that consist only of non-negative integers.
Consider the list containing the result of arr1[i] AND arr2[j] (bitwise AND) for every (i, j) pair where 0 <= i < arr1.length and 0 <= j < arr2.length.
Return the XOR sum of the aforementioned list.

**Examples**

**Example 1:**

```
Input: arr1 = [1,2,3], arr2 = [6,5]
Output: 0
Explanation: The list = [1 AND 6, 1 AND 5, 2 AND 6, 2 AND 5, 3 AND 6, 3 AND 5] = [0,1,2,0,2,1].
The XOR sum = 0 XOR 1 XOR 2 XOR 0 XOR 2 XOR 1 = 0.
```

**Example 2:**

```
Input: arr1 = [12], arr2 = [4]
Output: 4
Explanation: The list = [12 AND 4] = [4]. The XOR sum = 4.
```

**Constraints**

- 1 <= arr1.length, arr2.length <= 105
- 0 <= arr1[i], arr2[j] <= 109

---

## 题目（中文翻译）

**题目描述**

列表的 **XOR sum**（异或和）是其所有元素进行按位异或（bitwise XOR）的结果。如果列表仅包含一个元素，则其 **XOR sum** 等于该元素本身。

给定两个下标从 0 开始的数组 `arr1` 和 `arr2`，两者仅包含非负整数。  
考虑所有满足 `0 <= i < arr1.length` 且 `0 <= j < arr2.length` 的 `(i, j)` 配对，对每个配对计算 `arr1[i] AND arr2[j]`（按位与，bitwise AND），并将结果形成一个列表。

返回上述列表的 **XOR sum**。

**示例**

*示例 1*  
输入: `arr1 = [1,2,3]`, `arr2 = [6,5]`  
输出: `0`  
解释: 列表为 `[1 AND 6, 1 AND 5, 2 AND 6, 2 AND 5, 3 AND 6, 3 AND 5] = [0,1,2,0,2,1]`。  
**XOR sum** = `0 XOR 1 XOR 2 XOR 0 XOR 2 XOR 1 = 0`。

*示例 2*  
输入: `arr1 = [12]`, `arr2 = [4]`  
输出: `4`  
解释: 列表为 `[12 AND 4] = [4]`。**XOR sum** = `4`。

**约束条件**

- `1 <= arr1.length, arr2.length <= 10^5`
- `0 <= arr1[i], arr2[j] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把 **所有** 可能的 `(i, j)` 配对都枚举出来，先算出 `arr1[i] AND arr2[j]`（按位与），再把这些结果逐个做异或（XOR）。  

- **使用的数据结构**：两个普通的 Python 列表 `arr1`、`arr2`，以及一个变量 `ans` 用来累计 XOR 结果。  
- **生活化类比**：把 `arr1` 看成一排小盒子，每个盒子里放着一个数字；把 `arr2` 再看成另一排小盒子。我们把每个 `arr1` 盒子里的数字分别和 **每个** `arr2` 盒子里的数字“握手”，握手的方式是 “按位与”。所有握手的结果再放进一个大桶里，最后把桶里所有数字“捏在一起”进行 XOR（相当于把所有数字的每一位做奇偶计数）。  

**为什么正确**  
因为题目要求的就是**所有** `(i, j)` 对的 `AND` 结果再 XOR，遍历完整个笛卡尔积（全组合）自然能得到完整列表，随后的 XOR 也正是题目要的答案。

#### 代码（Python）

```python
from typing import List

def xorAllPairs_bruteforce(arr1: List[int], arr2: List[int]) -> int:
    ans = 0                     # 用来累计 XOR 结果
    for a in arr1:              # 遍历 arr1 中的每个元素 a
        for b in arr2:          # 与 arr2 中的每个元素 b 配对
            ans ^= (a & b)      # 先按位与，再异或到 ans
    return ans
```

> **关键行中文注释**  
> - `ans ^= (a & b)`: `a & b` 是当前配对的 **按位与**，`^=` 表示把它和已有的 `ans` 做 **异或并写回**。

#### 复杂度

- **时间复杂度**：`O(m * n)`，其中 `m = len(arr1)`，`n = len(arr2)`。  
  大白话：如果 `arr1` 有 10 000 个数，`arr2` 也有 10 000 个数，我们就要做 **一亿次** 按位与和异或——明显太慢。

- **空间复杂度**：`O(1)`（不计输入数组本身），只用了一个额外的整数 `ans`。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于双层循环：我们对每一对都重复计算了“按位与”。  
观察下面的代数性质（**位运算的分配律**）：

```
(a & b) ^ (a & c) = a & (b ^ c)
```

也就是说，如果 `a` 固定不变，把它分别和 `b、c` 做 AND 再 XOR，等价于先把 `b、c` 做 XOR，再和 `a` 做一次 AND。  

把这个思路推广到整组数组：

```
(arr1[i] & arr2[0]) ^ (arr1[i] & arr2[1]) ^ ... ^ (arr1[i] & arr2[n-1])
= arr1[i] & (arr2[0] ^ arr2[1] ^ ... ^ arr2[n-1])
```

左边正是“**固定一个 arr1[i]，遍历所有 arr2**”得到的 XOR；右边只需要先算出 **arr2 的整体 XOR**，记作 `xor2`，再与 `arr1[i]` 做一次 AND。

同理，对所有 `arr1[i]` 再做一次相同的变形：

```
xor2 & arr1[0] ^ xor2 & arr1[1] ^ ... ^ xor2 & arr1[m-1]
= xor2 & (arr1[0] ^ arr1[1] ^ ... ^ arr1[m-1])
```

把 `arr1` 的整体 XOR 记作 `xor1`，最后答案就是：

```
answer = xor1 & xor2
```

**核心概念**  
- **XOR 的结合律 & 交换律**：`a ^ b ^ c` 可以随意重新组合。  
- **按位与的分配律**：`a & (b ^ c) = (a & b) ^ (a & c)`。  
- **整体思路**：把二维循环压缩成 **两次线性遍历**，分别求出两个数组的 XOR，然后再一次 AND。

#### 代码（Python）

```python
from typing import List
from functools import reduce
import operator

def xorAllPairs_optimal(arr1: List[int], arr2: List[int]) -> int:
    """
    只遍历两遍数组，时间 O(m + n)，空间 O(1)。
    """
    # 1. 计算 arr1 所有元素的 XOR
    xor1 = 0
    for x in arr1:
        xor1 ^= x               # 累计 XOR

    # 2. 计算 arr2 所有元素的 XOR
    xor2 = 0
    for x in arr2:
        xor2 ^= x               # 累计 XOR

    # 3. 最终答案是两者的 AND
    return xor1 & xor2
```

> **关键行中文注释**  
> - `xor1 ^= x`：把当前元素 `x` 加入到 `arr1` 的整体 XOR 中。  
> - `xor2 ^= x`：同理，求 `arr2` 的整体 XOR。  
> - `return xor1 & xor2`：根据上面的数学推导，这一步直接得到所有配对的 XOR‑AND 结果。

#### 复杂度

- **时间复杂度**：`O(m + n)`。我们只遍历两遍数组，各自做一次 XOR，随后一次 AND，整体是线性的。相比暴力的 `O(m·n)`，快了 **指数级**（即从“一亿次”降到 “二十万次”）。

- **空间复杂度**：`O(1)`。只用了几个整数变量（`xor1`, `xor2`, `x`），不随输入规模增长。

---

## 心得

- **核心技巧**：利用位运算的分配律把二维组合的 AND‑XOR 过程“拆解”为两个一维的 XOR 再一次 AND。  
- **适用的题型**  
  1. “**XOR of all pairwise AND**” 类似题目（比如 LeetCode 2413 – *Maximum Sum of Array After K Subtractions* 中的位运算技巧）。  
  2. “**XOR of all pairwise OR**” 或 “**XOR of all pairwise SUM**” 等，只要能找到类似的分配律或结合律。  
  3. “**求所有子集的 XOR/AND/OR**” 这类需要压缩指数级组合的题。  

> **一句话总结解题钥匙**：**先把一维数组的 XOR 预先算好，再一次 AND 完事**。

---

## 反思

- **第一反应**：看到“所有配对的 AND 再 XOR”，第一时间会想到两层循环暴力枚举，因为这最直观。  
- **最容易踩的坑**  
  - 忽视 **位运算的分配律**，导致错失从 `O(m·n)` 到 `O(m+n)` 的优化。  
  - 忘记 **空数组**（虽然约束不允许），如果出现，需要提前返回 `0`。  
  - 对 **大数范围**（`0 ≤ value ≤ 10^9`）不必担心溢出，因为 Python 整数是无限精度，但在有些语言需要注意位宽。  

- **下次遇到同类题**，第一步应该：**思考能否把“对每个元素的全部配对”用一次全局的运算（如 XOR、AND、OR）替代**，寻找分配律或结合律的切入口。这样往往能把指数级的组合问题压缩到线性时间。