# #1318. 使 a OR b 等于 c 的最小翻转次数 / Minimum Flips to Make a OR b Equal to c

> 难度：中等 · 标签：Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/minimum-flips-to-make-a-or-b-equal-to-c/)

---

## 题目（英文原版）

**Description**

Given 3 positives numbers a, b and c. Return the minimum flips required in some bits of a and b to make ( a OR b == c ). (bitwise OR operation).
Flip operation consists of change any single bit 1 to 0 or change the bit 0 to 1 in their binary representation.

**Examples**

**Example 1:**

```
Input: a = 2, b = 6, c = 5
Output: 3
Explanation: After flips a = 1 , b = 4 , c = 5 such that (a OR b == c)
```

**Example 2:**

```
Input: a = 4, b = 2, c = 7
Output: 1
```

**Example 3:**

```
Input: a = 1, b = 2, c = 3
Output: 0
```

**Constraints**

- 1 <= a <= 10^9
- 1 <= b <= 10^9
- 1 <= c <= 10^9

---

## 题目（中文翻译）

**描述**  
给定三个正整数 `a`、`b` 和 `c`。返回将 `a` 和 `b` 的若干位翻转后，使得 `(a OR b == c)`（按位或（bitwise OR）运算）成立所需的最小翻转次数。  
翻转操作指将二进制表示中的任意单个位 `1` 改为 `0`，或将 `0` 改为 `1`。

**示例 1**  
```
Input: a = 2, b = 6, c = 5
Output: 3
Explanation: 翻转后得到 a = 1, b = 4, c = 5，使得 (a OR b == c)
```

**示例 2**  
```
Input: a = 4, b = 2, c = 7
Output: 1
```

**示例 3**  
```
Input: a = 1, b = 2, c = 3
Output: 0
```

**约束条件**  
- `1 <= a <= 10^9`  
- `1 <= b <= 10^9`  
- `1 <= c <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把 **a、b、c** 都转成二进制字符串，逐位（从低位到高位）比较它们的字符。  
- **位** 就像一本书的每一页的“0/1”，我们只要看同一页（同一位）上三个数写的是什么，就能决定要不要改动。  
- 对于每一位，按照下面的规则计数翻转次数：  

| c 的位 | a 的位 | b 的位 | 需要的翻转数 | 说明 |
|-------|-------|-------|------------|------|
| 0 | 0 | 0 | 0 | 已经满足 a|b = 0 |
| 0 | 1 | 0 | 1 | 必须把 a 的 1 翻成 0 |
| 0 | 0 | 1 | 1 | 必须把 b 的 1 翻成 0 |
| 0 | 1 | 1 | 2 | a、b 都要各翻一次 |
| 1 | 0 | 0 | 1 | 必须把 a 或 b 中的 0 翻成 1（任选其一） |
| 1 | 1 | 0 | 0 | 已经满足 a|b = 1 |
| 1 | 0 | 1 | 0 | 已经满足 a|b = 1 |
| 1 | 1 | 1 | 0 | 已经满足 a|b = 1 |

把所有位的翻转数加起来，就是答案。  
这个方法之所以**正确**，是因为位之间互不影响——每一位的 OR 结果只和该位的 a、b 有关，和其它位完全独立。只要每一位都满足条件，整体的 a OR b 就一定等于 c。

#### 代码（Python）  
```python
def minFlips_brute(a: int, b: int, c: int) -> int:
    # 将三个数转成二进制字符串，去掉前面的 '0b'
    bin_a = bin(a)[2:][::-1]   # 逆序，方便从低位开始遍历
    bin_b = bin(b)[2:][::-1]
    bin_c = bin(c)[2:][::-1]

    # 取最长的长度，确保所有位都被遍历到
    max_len = max(len(bin_a), len(bin_b), len(bin_c))
    flips = 0

    for i in range(max_len):
        # 取第 i 位的字符，若该数不足该位则视为 '0'
        ai = bin_a[i] if i < len(bin_a) else '0'
        bi = bin_b[i] if i < len(bin_b) else '0'
        ci = bin_c[i] if i < len(bin_c) else '0'

        if ci == '0':
            # c 为 0，a 与 b 必须都是 0，出现 1 就要翻
            flips += (ai == '1') + (bi == '1')
        else:  # ci == '1'
            # c 为 1，a 与 b 至少有一个为 1
            if ai == '0' and bi == '0':
                flips += 1          # 把 a 或 b 的 0 翻成 1，任选其一
    return flips
```

#### 复杂度  
- **时间复杂度：O(k)** —— 这里的 *k* 是 a、b、c 中二进制位数的最大值（最多 30 左右，因为 10⁹ < 2³⁰）。我们只遍历一次所有位，所以说“线性遍历”就行了。  
- **空间复杂度：O(k)** —— 需要存放三个二进制字符串（每个最多 30 个字符），属于额外的线性空间。  

---  

### 2. 最优解  

#### 思路  
暴力解已经是 **线性** 的，但我们可以省去把数字转成字符串的步骤，直接用位运算（`&`, `>>`, `|`）在整数上逐位检查。  
- **瓶颈**：字符串的切片、逆序等操作会产生额外的开销。  
- **优化**：用右移 `>>` 把当前位移到最右边，再用 `& 1` 取出该位的值。这样每一次循环只涉及几条机器指令，速度更快，空间也只用常数。  

核心概念——**位运算**，可以把它想象成“超高速的字典”。  
- `x & 1` 就像在字典里查 “第 0 位”，返回 0 或 1。  
- `x >> 1` 相当于把整本书往左翻一页，让下一位成为新的第 0 位。

**逐位决策规则** 与上表完全相同，只是用整数操作实现：

```text
if c_bit == 0:
    flips += a_bit + b_bit          # 只要是 1 都要翻
else:  # c_bit == 1
    if a_bit == 0 and b_bit == 0:
        flips += 1                  # 两个都是 0，需要翻一个
```

遍历结束后 `flips` 就是最少翻转次数。  

#### 代码（Python）  
```python
def minFlips(a: int, b: int, c: int) -> int:
    flips = 0
    # 当任意一个数还有未处理的位时继续循环
    while a or b or c:
        # 取当前最低位
        a_bit = a & 1
        b_bit = b & 1
        c_bit = c & 1

        if c_bit == 0:
            # 目标位是 0，a、b 中的每个 1 都需要翻成 0
            flips += a_bit + b_bit
        else:  # c_bit == 1
            # 目标位是 1，只要 a、b 同时为 0 才需要翻 1 次
            if a_bit == 0 and b_bit == 0:
                flips += 1

        # 右移一位，准备检查下一位
        a >>= 1
        b >>= 1
        c >>= 1
    return flips
```

#### 复杂度  
- **时间复杂度：O(k)** —— 仍然是遍历每一位，但每位只做几条整数操作，常数因子更小。这里的 *k* 同样是最高位数（≤30）。  
- **空间复杂度：O(1)** —— 只用了几个整型变量，不会随输入大小增长。相比暴力解省掉了字符串的额外空间。

---

## 心得  

- **核心技巧**：逐位检查并利用位运算（`>>`、`&`）完成“贪心”计数。  
- **适用的题型**  
  1. *Number of Steps to Reduce a Number to Zero*（逐位计数）  
  2. *Sum of Two Integers without '+'*（位运算实现加法）  
  3. *Maximum XOR of Two Numbers in an Array*（利用 Trie + 位）  
- **一句话总结**：**把每一位当成独立的小任务，只要把每位的最优决定加起来，整体就是最少翻转次数。**  

---

## 反思  

- **第一反应**：把三个数都写成二进制，逐位对照，记下来每位要改几次。  
- **最容易踩的坑**  
  - 忘记处理最高位后仍然有 `1` 的情况（需要继续循环直到所有数都为 0）。  
  - 当 `c` 的位为 `1` 时，只要 `a`、`b` 同时为 `0` 才需要翻 1 次，其他组合不需要翻。容易把“只要有一个是 1 就不动”写错成“只要两个都是 1 才不动”。  
- **下次类似题**：第一步先**思考位是否独立**，如果是，就用**逐位位运算**把每一位的最优决策累加即可。