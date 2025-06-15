# #3226. 使两个整数相等的位改变次数 / Number of Bit Changes to Make Two Integers Equal

> 难度：简单 · 标签：Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/number-of-bit-changes-to-make-two-integers-equal/)

---

## 题目（英文原版）

**Description**

You are given two positive integers n and k.
You can choose any bit in the binary representation of n that is equal to 1 and change it to 0.
Return the number of changes needed to make n equal to k. If it is impossible, return -1.

**Examples**

**Example 1:**

```
Input: n = 13, k = 4
Output: 2
Explanation: Initially, the binary representations of n and k are n = (1101) 2 and k = (0100) 2 . We can change the first and fourth bits of n . The resulting integer is n = ( 0 10 0 ) 2 = k .
```

**Example 2:**

```
Input: n = 21, k = 21
Output: 0
Explanation: n and k are already equal, so no changes are needed.
```

**Example 3:**

```
Input: n = 14, k = 13
Output: -1
Explanation: It is not possible to make n equal to k .
```

**Constraints**

- 1 <= n, k <= 106

---

## 题目（中文翻译）

**题目描述**  
给定两个正整数 `n` 和 `k`。  
你可以选择 `n` 的二进制表示（binary representation）中任意值为 `1` 的位（bit），并将其改为 `0`。  
返回使 `n` 等于 `k` 所需的最少改变次数。如果无法做到，返回 `-1`。

**示例**  

**示例 1**  
输入: `n = 13, k = 4`  
输出: `2`  
解释: 最初，`n` 与 `k` 的二进制表示分别为 `n = (1101)_2` 和 `k = (0100)_2`。我们可以将 `n` 的第一位和第四位（从左到右）改为 `0`，得到 `n = (0100)_2 = k`。

**示例 2**  
输入: `n = 21, k = 21`  
输出: `0`  
解释: `n` 与 `k` 已经相等，无需任何改变。

**示例 3**  
输入: `n = 14, k = 13`  
输出: `-1`  
解释: 无法通过只将 `1` 改为 `0` 的操作使 `n` 等于 `k`。

**约束条件**  
- `1 <= n, k <= 10^6`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

题目要求把整数 **n** 通过“只能把 1 变成 0” 的操作，变成整数 **k**。  
最直接的想法就是把 **n** 和 **k** 的二进制位一位一位对比：

1. 把 **n**、**k** 都写成二进制（想象成一串灯泡，亮=1，灭=0）。  
2. 从最低位到最高位逐个检查：  
   - 如果 **n** 的这位是 **1**，而 **k** 的这位是 **0**，说明需要把这盏灯关掉，计数加 1。  
   - 如果 **n** 的这位是 **0**，而 **k** 的这位是 **1**，这时我们 **只能把 1 变 0，不能把 0 变 1**，所以根本不可能完成。直接返回 `-1`。  
3. 检查完所有位后，计数就是需要的最少操作数。

> **类比**：把二进制看成一本字典，**位** 就是词条，**1** 表示这本书里有这页，**0** 表示没有。我们只能把已有的页码撕掉，不能添加新页。

这个方法一定能得到正确答案，因为我们逐位判断了所有可能的冲突，并且只在必须的位上进行“关灯”操作。

#### 代码（Python）

```python
def minBitChanges_bruteforce(n: int, k: int) -> int:
    changes = 0                 # 记录需要关闭的灯的数量
    i = 0                       # 当前检查的位数（从 0 开始）

    # 当 n 或 k 还有未检查的高位时，继续循环
    while n > 0 or k > 0:
        n_bit = n & 1           # 取 n 的最低位 (0 或 1)
        k_bit = k & 1           # 取 k 的最低位

        if n_bit == 0 and k_bit == 1:
            # 只能把 1 变 0，遇到 0 → 1 的情况直接返回 -1
            return -1

        if n_bit == 1 and k_bit == 0:
            # 需要把这位的 1 关掉
            changes += 1

        # 右移一位，继续检查下一位
        n >>= 1
        k >>= 1
        i += 1

    return changes
```

#### 复杂度  

- **时间复杂度**：`O(log max(n, k))`  
  大白话：我们只检查二进制位的个数，最多是数字的位数。比如 `n = 13 (1101)` 只需要检查 4 位，所以时间跟位数成正比。  
- **空间复杂度**：`O(1)`  
  只用了常数个变量，和输入大小无关。

---

### 2. 最优解  

#### 思路  

暴力解已经是线性的位数检查，已经很快。但我们可以把“逐位检查”这件事交给 **位运算** 一口气完成，代码会更简洁，常数更小。

1. **先判断能否完成**  
   - 只能把 1 变 0，意味着 **k** 中出现的每一个 1，都必须在 **n** 中对应位置也是 1。  
   - 用位运算写成 `k & ~n == 0`（`~n` 是 n 的位取反，`k & ~n` 取出所有在 k 为 1、而 n 为 0 的位）。如果不为 0，说明出现了 “0 → 1” 的冲突，直接返回 `-1`。

2. **统计需要关掉的位**  
   - 只要 **n** 为 1、**k** 为 0 的位置需要关灯。可以用 `n & ~k` 把这些位挑出来。  
   - 再求出这个数的 **二进制中 1 的个数**（即**集合中有多少盏灯要关**），这就是答案。求 1 的个数常用的技巧叫 **popcount**，在 Python 可以用 `bin(x).count('1')`，也可以用 `int.bit_count()`（Python 3.8+）。

> **类比**：把 `n` 看成一本已经装好页码的书，`k` 看成我们想要的目标书。`~k` 把目标书里不需要的页码翻成 1，`n & ~k` 就是“原书里有而目标里没有的页码”，我们只需要把这些页码撕掉。

这样我们只用了两次位运算和一次计数，整个过程一次性完成。

#### 代码（Python）

```python
def minBitChanges_optimal(n: int, k: int) -> int:
    # 1) 判断是否出现 0 -> 1 的非法情况
    #    k 中的 1 必须全部在 n 中也为 1
    if k & ~n:                # 如果结果非零，说明存在 k 为 1 而 n 为 0 的位
        return -1

    # 2) 需要关掉的位 = n 中为 1 且 k 中为 0 的位
    need_to_turn_off = n & ~k

    # 3) 统计这些位中 1 的个数，即需要的操作次数
    #    Python 3.8+ 可以直接使用 int.bit_count()
    return need_to_turn_off.bit_count()
```

#### 复杂度  

- **时间复杂度**：`O(1)`（常数时间）  
  所有操作都是一次位运算和一次计数，和数字的大小无关。相较于暴力的 `O(log max)`，这里把遍历位的过程“压缩”成了常数时间。  
- **空间复杂度**：`O(1)`  
  只用了几个整数变量。

---

## 心得  

- **核心技巧**：**位运算 + popcount**  
  - 判断能否完成：`k & ~n == 0`（没有“0→1”冲突）。  
  - 统计需要关闭的位：`popcount(n & ~k)`。  

- **适用的题型**（类似思路）：  
  1. “将两个二进制数相等，只能翻转 1 为 0” 类似题。  
  2. “判断一个数是否是另一个数的子集”（子集关系 = `a & b == a`）。  
  3. “求两个数的不同位数”（`popcount(a ^ b)`）。

- **一句话总结解题钥匙**：  
  *先用位运算判断合法性，再用 `n & ~k` 把“多余的 1”挑出来，用 popcount 计数即得最少操作数。*

---

## 反思  

- **第一反应**：把两个数写成二进制，逐位比较，记下需要关闭的灯。  
- **最容易踩的坑**：忘记先判断 “0 → 1” 的非法情况，直接计数会得到错误的正数而不是 `-1`。  
- **下次类似题的第一步**：先把 “只能做哪种位变换” 用位运算写成一个**可判定**的条件（如 `k & ~n == 0`），再根据条件决定后续计数或返回。