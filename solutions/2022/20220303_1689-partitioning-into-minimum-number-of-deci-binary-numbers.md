# #1689. 划分为最少数量的十进制二进制数 / Partitioning Into Minimum Number Of Deci-Binary Numbers

> 难度：中等 · 标签：String、Greedy · [LeetCode 链接](https://leetcode.com/problems/partitioning-into-minimum-number-of-deci-binary-numbers/)

---

## 题目（英文原版）

**Description**

A decimal number is called deci-binary if each of its digits is either 0 or 1 without any leading zeros. For example, 101 and 1100 are deci-binary, while 112 and 3001 are not.
Given a string n that represents a positive decimal integer, return the minimum number of positive deci-binary numbers needed so that they sum up to n.

**Examples**

**Example 1:**

```
Input: n = "32"
Output: 3
Explanation: 10 + 11 + 11 = 32
```

**Example 2:**

```
Input: n = "82734"
Output: 8
```

**Example 3:**

```
Input: n = "27346209830709182346"
Output: 9
```

**Constraints**

- 1 <= n.length <= 105
- n consists of only digits.
- n does not contain any leading zeros and represents a positive integer.

---

## 题目（中文翻译）

**题目描述**  
十进制二进制数（deci-binary）是指每一位数字仅为 0 或 1，且没有前导零的十进制整数。例如，101 和 1100 是十进制二进制数，而 112 和 3001 则不是。  
给定一个字符串 `n`，它表示一个正的十进制整数，返回将若干个正的十进制二进制数相加得到 `n` 所需的最少个数。

**示例**

**示例 1**  
Input: `n = "32"`  
Output: `3`  
Explanation: `10 + 11 + 11 = 32`

**示例 2**  
Input: `n = "82734"`  
Output: `8`  

**示例 3**  
Input: `n = "27346209830709182346"`  
Output: `9`  

**约束条件**  
- `1 <= n.length <= 10^5`  
- `n` 仅由数字字符组成。  
- `n` 不含前导零且表示一个正整数。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把原数字一次一次地减去一个合法的 deci‑binary 数**，直到剩下 0 为止。  
- 先把字符串 `n` 转成一个整数数组 `digits`，每个元素是对应的十进制位（`'3' → 3`）。  
- 构造一个 deci‑binary 数的方法很简单：只要当前位大于 0，就在该位放 `1`，否则放 `0`。举个例子，`digits = [3,2]`（对应 “32”）  
  - 第一次构造得到 `11`（因为两位都大于 0），  
  - 再把 `11` 从 `32` 中减去，得到 `21` → 再构造 `11`，  
  - 再减去得到 `10` → 再构造 `10`，  
  - 最后减到 `00`，共用了 3 次。  

这相当于“把每一位的数字拆成若干个 1”，每一次我们都尽可能多地把 `1` 放进去，类似把一块巧克力一次切成最多的小块。  

**为什么一定能得到正确答案？**  
每一次减去的都是合法的 deci‑binary（只含 0/1），而且我们每次都把所有还能减的位都减了 `1`，所以整个过程等价于把每个十进制位的数值 **拆成若干个 1**，最后的次数就是所有位上最大需要拆多少次，也就是答案。

**时间/空间复杂度**  
- 每一次减法需要遍历全部 `len(n)` 位，最多减 `max_digit` 次（`max_digit` 是字符串中最大的数字，最多是 9）。所以时间复杂度是 `O(max_digit * len(n))`。  
  - 大白话：如果数字长度是 1000，最大位是 8，那么最多要做 8 × 1000 = 8000 次遍历，仍然可以接受。  
- 只用了一个长度为 `len(n)` 的数组来存放每位数字，空间复杂度是 `O(len(n))`。

#### 代码（Python）

```python
def min_partitions_brute(n: str) -> int:
    # 把字符串每个字符转成整数，方便后面直接做减法
    digits = [int(ch) for ch in n]          # 例如 "32" → [3, 2]
    cnt = 0                                 # 记录用了多少个 deci‑binary

    while any(d > 0 for d in digits):       # 只要还有非零位，就继续
        cnt += 1
        # 本轮要构造的 deci‑binary：每个还能减的位放 1，不能减的位放 0
        for i in range(len(digits)):
            if digits[i] > 0:               # 该位大于 0，减去 1
                digits[i] -= 1

    return cnt
```

#### 复杂度

- **时间复杂度**：`O(max_digit * len(n))`  
  - `max_digit` ≤ 9，意味着最坏情况只会遍历至多 9 × n 次。  
- **空间复杂度**：`O(len(n))`  
  - 只用了一个与输入等长的整数数组来保存每位数字。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**每一次我们都把所有还能减的位都减了 1**。  
于是可以思考：  
- 对于某一位 `d`（0 ≤ d ≤ 9），它至少需要被减 `d` 次，才能变成 0。  
- 由于不同位可以在同一次操作里一起减 1（因为 deci‑binary 只要对应位是 1 即可），**所有位的减法次数的上限就是最大位的数值**。  

换句话说，答案只和最高位的数字有关：  

```
答案 = max( n[i] )   (i 为所有字符下标)
```

这就是一道**贪心**（greedy）题：每一步都尽可能多地使用 1，最终的次数自然等于最大的需求。

**为什么这个贪心是最优的？**  
- 任意一种合法的分解方式，都必须让最大位的 `max_digit` 次 `1` 出现在对应的 deci‑binary 数中（否则它永远减不掉）。  
- 同时我们可以把每一次 `1` 同时放到所有还有剩余的位上，正好用 `max_digit` 次就把所有位都凑到 0。  
- 所以不存在比 `max_digit` 更少的次数，`max_digit` 必然是最小可能值。

**核心概念：**  
- **贪心**：每一步都选局部最优（这里是“把每位都减 1”），全局最优即为最大位数。  
- **最大值**：在一堆数字里挑最大的，那就是答案。

#### 代码（Python）

```python
def min_partitions(n: str) -> int:
    """
    返回将正整数 n 拆分成最少个 deci‑binary 数的数量。
    思路：答案就是字符串中出现的最大数字。
    """
    # 直接遍历字符，取最大值。字符 '0'~'9' 的 ASCII 码可以直接比较。
    max_digit = 0
    for ch in n:
        # 将字符转成对应的整数值
        digit = ord(ch) - ord('0')
        if digit > max_digit:
            max_digit = digit
    return max_digit
```

#### 复杂度

- **时间复杂度**：`O(len(n))`  
  - 只需要一次遍历，读完每个字符就知道最大值。相比暴力的 `max_digit * len(n)`，省了最多 9 倍的循环次数。  
- **空间复杂度**：`O(1)`  
  - 只用了几个整型变量，和输入长度无关。

---

## 心得

- **核心技巧**：**找最大值 = 贪心**。这道题的关键在于认识到每一位的需求是独立的，整体的最少次数就是所有需求中的最大值。  
- **适用的题型**：  
  1. “把数字拆成若干满足某种局部约束的子数字”，如 *Minimum Number of Flips to Convert Binary Matrix to Zero*（求最大行/列翻转次数）。  
  2. “每一步都可以对所有满足条件的元素做同样的操作”，如 *Maximum Number of Coins You Can Get*（贪心取最大）。  
- **一句话总结**：**答案就是输入字符串里的最大数字**——把每位的需求都一次性并行完成。

---

## 反思

- **第一反应**：看到“每位都是 0/1 的数”，本能想到把原数拆成若干个只含 0/1 的数，进而想到“每次把所有还能减的位都减 1”。  
- **最容易踩的坑**：  
  - 忽略了 **“正整数”** 的前提，误把 `0` 当作可能的输入。  
  - 在暴力实现时忘记判断所有位是否已经全为 0，导致死循环。  
  - 在最优解中直接使用 `max(map(int, n))` 虽然简洁，但对初学者解释时要拆开来说明每一步的意义。  
- **下次遇到同类题**，第一步应该问自己：**每一位的需求是否可以独立统计？** 如果可以，答案往往是 **“最大需求”** 或者 **“所有需求之和的某种变形”**，再据此选择贪心或 DP。