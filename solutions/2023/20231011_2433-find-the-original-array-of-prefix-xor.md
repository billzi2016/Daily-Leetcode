# #2433. 找到前缀异或的原始数组 / Find The Original Array of Prefix Xor

> 难度：中等 · 标签：Array、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/find-the-original-array-of-prefix-xor/)

---

## 题目（英文原版）

**Description**

You are given an integer array pref of size n. Find and return the array arr of size n that satisfies:
Note that ^ denotes the bitwise-xor operation.
It can be proven that the answer is unique.

**Examples**

**Example 1:**

```
Input: pref = [5,2,0,3,1]
Output: [5,7,2,3,2]
Explanation: From the array [5,7,2,3,2] we have the following:
- pref[0] = 5.
- pref[1] = 5 ^ 7 = 2.
- pref[2] = 5 ^ 7 ^ 2 = 0.
- pref[3] = 5 ^ 7 ^ 2 ^ 3 = 3.
- pref[4] = 5 ^ 7 ^ 2 ^ 3 ^ 2 = 1.
```

**Example 2:**

```
Input: pref = [13]
Output: [13]
Explanation: We have pref[0] = arr[0] = 13.
```

**Constraints**

- 1 <= pref.length <= 105
- 0 <= pref[i] <= 106

---

## 题目（中文翻译）

给定一个整数数组 `pref`，长度为 `n`。请找出并返回一个长度同样为 `n` 的数组 `arr`，使得：

- `pref[i] = arr[0] ^ arr[1] ^ ... ^ arr[i]`（`^` 表示按位异或（bitwise‑xor）运算）

可以证明答案唯一。

## 示例

### 示例 1
**输入**：`pref = [5,2,0,3,1]`  
**输出**：`[5,7,2,3,2]`  
**解释**：从数组 `[5,7,2,3,2]` 可以得到：

- `pref[0] = 5`
- `pref[1] = 5 ^ 7 = 2`
- `pref[2] = 5 ^ 7 ^ 2 = 0`
- `pref[3] = 5 ^ 7 ^ 2 ^ 3 = 3`
- `pref[4] = 5 ^ 7 ^ 2 ^ 3 ^ 2 = 1`

### 示例 2
**输入**：`pref = [13]`  
**输出**：`[13]`  
**解释**：`pref[0] = arr[0] = 13`

## 约束条件
- `1 <= pref.length <= 10^5`
- `0 <= pref[i] <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目给了我们 **前缀异或** 数组 `pref`，要求恢复出原始数组 `arr`，满足  

```
pref[i] = arr[0] ^ arr[1] ^ ... ^ arr[i]   （^ 为按位异或）
```

最直接的想法是**逐个验证**：  
- 已知 `arr[0] = pref[0]`（因为前缀只有一个数）。  
- 对于第 `i` 个位置（`i>0`），我们可以把已经求出的 `arr[0..i-1]` 再全部异或一次，得到 `cur = arr[0] ^ ... ^ arr[i-1]`。  
- 然后把 `cur` 与 `pref[i]` 再异或，得到 `arr[i]`：  

```
arr[i] = cur ^ pref[i]        （因为 cur ^ arr[i] = pref[i]）
```

这一步其实就是把「已知的前缀」和「目标前缀」进行比较，求出缺失的那个数。

> **类比**：把 `pref[i]` 看成一本厚厚的字典，`cur` 是我们已经翻到的页码。要找第 `i` 页的词（即 `arr[i]`），只需要把已经翻过的页码和目标页码做一次“差异”运算（异或），就能得到那一页的内容。

**为什么正确**  
异或满足 **自反性**（`a ^ a = 0`）和 **结合律**（`a ^ (b ^ c) = (a ^ b) ^ c`），所以  

```
(cur) ^ arr[i] = pref[i]
=> arr[i] = cur ^ pref[i]
```

只要 `cur` 正确地等于 `arr[0] ^ ... ^ arr[i-1]`，上述等式必然成立。

**时间/空间复杂度**  
- 对每个 `i`，我们都要遍历 `0..i-1` 来计算 `cur`，所以总共要做 `1 + 2 + … + (n-1) = O(n²)` 次异或运算。  
- 只使用了常数级别的额外空间 `O(1)`（除了返回的结果数组）。

> **大白话**：`O(n²)` 就像在一个有 `n` 行的表格里，每行都要把前面所有行的数字加起来，工作量会随 `n` 的增长而呈平方增长，`n=10⁵` 时根本不可接受。

#### 代码（Python）

```python
from typing import List

def findArray_bruteforce(pref: List[int]) -> List[int]:
    n = len(pref)
    arr = [0] * n                 # 用来保存答案
    for i in range(n):
        if i == 0:
            # 第一个元素直接等于 pref[0]
            arr[i] = pref[i]
        else:
            cur = 0                # cur 用来存 arr[0] ^ ... ^ arr[i-1]
            for j in range(i):    # 暴力累加前缀异或
                cur ^= arr[j]     # ^ 是按位异或
            # 根据 cur ^ arr[i] = pref[i] 求出 arr[i]
            arr[i] = cur ^ pref[i]
    return arr
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  意味着当数组长度 `n` 很大（比如 10⁵）时，程序会非常慢，因为需要做近 `n²/2` 次异或运算。

- **空间复杂度**：`O(1)`（不计答案数组）  
  只用了几个临时变量，额外占用的内存几乎不随 `n` 增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于每次都重新遍历前面的元素去求 `cur`。  
其实我们不必每次都重新计算，**前一次的前缀异或已经帮我们保存了信息**。

记住：

```
pref[i] = arr[0] ^ arr[1] ^ ... ^ arr[i]
pref[i-1] = arr[0] ^ arr[1] ^ ... ^ arr[i-1]
```

把这两式做一次异或：

```
pref[i] ^ pref[i-1] = (arr[0] ^ ... ^ arr[i]) ^ (arr[0] ^ ... ^ arr[i-1])
                     = arr[i]               （因为相同的部分会相互抵消，a ^ a = 0）
```

于是我们直接得到：

```
arr[i] = pref[i] ^ pref[i-1]    （i > 0）
arr[0] = pref[0]                （单独处理）
```

这就是**一次遍历**即可完成的公式。我们只需要保存前一个 `pref` 的值（其实数组本身已经保存），不必再做额外的累加。

> **类比**：把 `pref` 看成两本相邻的账本，上一页的总额 `pref[i-1]` 与本页的总额 `pref[i]` 做一次“差额”运算（异或），差额正好是本页的收入 `arr[i]`。账本之间的差额直接告诉我们本页的数字，省去重新算账的麻烦。

#### 代码（Python）

```python
from typing import List

def findArray(pref: List[int]) -> List[int]:
    """
    根据前缀异或数组 pref，恢复原数组 arr。
    时间 O(n)，空间 O(1)（不计返回值）。
    """
    n = len(pref)
    arr = [0] * n
    for i in range(n):
        if i == 0:
            # 第一个元素没有前缀可以参考，直接等于 pref[0]
            arr[i] = pref[i]
        else:
            # arr[i] = pref[i] ^ pref[i-1]   （异或抵消前面的部分）
            arr[i] = pref[i] ^ pref[i - 1]
    return arr
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  只遍历一次数组，每个位置做一次常数时间的异或运算。相较于暴力的 `O(n²)`，速度提升了 **n 倍**，即使 `n = 10⁵` 也能在毫秒级完成。

- **空间复杂度**：`O(1)`（不计返回的 `arr`）  
  只用了几个临时变量 (`i`, `n`) 和常量大小的结果数组，不随输入规模增长。

---

## 心得

- **核心技巧**：利用异或的 **自反性** 与 **结合律**，把两个相邻的前缀异或相减（异或），直接得到当前元素。  
- **适用题型**  
  1. 前缀和/前缀异或逆推问题（如“恢复原数组”系列）。  
  2. “求数组中唯一出现一次的数”类问题（利用 `a ^ a = 0` 把成对出现的数抵消）。  
  3. “数组的子数组异或为 K”计数问题（前缀异或 + 哈希表）。
- **一句话总结**：**“相邻前缀异或的差即为原数组元素”。**

---

## 反思

- **第一反应**：看到“前缀”二字，我立刻想到“累加”或“累异或”，于是想用循环把已经算好的前缀再一次累加，导致了 `O(n²)` 的暴力思路。  
- **最容易踩的坑**  
  - 忘记 `arr[0]` 直接等于 `pref[0]`，把它也套入 `pref[i] ^ pref[i-1]` 会导致索引错误。  
  - 对异或的性质不熟悉，可能误以为 `a ^ b = a + b`，从而写出错误的公式。  
- **下次遇到同类题**：先检查是否可以把“前缀”与“后缀”或相邻前缀进行**一次异或/一次相减**得到想要的局部信息，避免重复累加。  

祝你在算法的道路上越走越顺！ 🚀