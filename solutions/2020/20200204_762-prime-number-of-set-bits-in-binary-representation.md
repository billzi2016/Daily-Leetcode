# #762. 二进制表示中置位数为质数的数字 / Prime Number of Set Bits in Binary Representation

> 难度：简单 · 标签：Math、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/prime-number-of-set-bits-in-binary-representation/)

---

## 题目（英文原版）

**Description**

Given two integers left and right, return the count of numbers in the inclusive range [left, right] having a prime number of set bits in their binary representation.
Recall that the number of set bits an integer has is the number of 1's present when written in binary.

**Examples**

**Example 1:**

```
Input: left = 6, right = 10
Output: 4
Explanation:
6  -> 110 (2 set bits, 2 is prime)
7  -> 111 (3 set bits, 3 is prime)
8  -> 1000 (1 set bit, 1 is not prime)
9  -> 1001 (2 set bits, 2 is prime)
10 -> 1010 (2 set bits, 2 is prime)
4 numbers have a prime number of set bits.
```

**Example 2:**

```
Input: left = 10, right = 15
Output: 5
Explanation:
10 -> 1010 (2 set bits, 2 is prime)
11 -> 1011 (3 set bits, 3 is prime)
12 -> 1100 (2 set bits, 2 is prime)
13 -> 1101 (3 set bits, 3 is prime)
14 -> 1110 (3 set bits, 3 is prime)
15 -> 1111 (4 set bits, 4 is not prime)
5 numbers have a prime number of set bits.
```

**Constraints**

- 1 <= left <= right <= 106
- 0 <= right - left <= 104

---

## 题目（中文翻译）

给定两个整数 `left` 和 `right`，返回区间 **[left, right]**（包含左右端点）中，**二进制表示（binary representation）**中 **置位数（set bits）** 为 **质数（prime number）** 的整数个数。

> 回想一下，整数的置位数是指其二进制表示中出现的 `1` 的个数。

### 示例

#### 示例 1
```
Input: left = 6, right = 10
Output: 4
Explanation:
6  -> 110  (2 个置位，2 是质数)
7  -> 111  (3 个置位，3 是质数)
8  -> 1000 (1 个置位，1 不是质数)
9  -> 1001 (2 个置位，2 是质数)
10 -> 1010 (2 个置位，2 是质数)
共有 4 个数的置位数为质数。
```

#### 示例 2
```
Input: left = 10, right = 15
Output: 5
Explanation:
10 -> 1010 (2 个置位，2 是质数)
11 -> 1011 (3 个置位，3 是质数)
12 -> 1100 (2 个置位，2 是质数)
13 -> 1101 (3 个置位，3 是质数)
14 -> 1110 (3 个置位，3 是质数)
15 -> 1111 (4 个置位，4 不是质数)
共有 5 个数的置位数为质数。
```

### 约束条件
- `1 <= left <= right <= 10^6`
- `0 <= right - left <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法就是把区间 `[left, right]` 里的每一个整数都 **逐个检查**：

1. 把当前整数写成二进制，统计里面有多少个 `1`（这叫“二进制中 1 的个数”，或者**集合位数**）。  
   - 可以把整数想象成一串灯泡，亮着的灯泡用 `1` 表示，数一数亮着的灯泡就得到集合位数。  
   - Python 中可以用 `bin(num)` 把整数转成字符串，再用 `count('1')` 计数，或者自己写一个循环右移并计数。

2. 判断这个计数是不是**质数**（只能被 1 和自身整除的数）。  
   - 这里的质数范围很小，因为 `right ≤ 10⁶`，二进制最多只有 20 位（`2¹⁰ ≈ 1024`，`2²⁰ ≈ 10⁶`），所以只需要判断 `2,3,5,7,11,13,17,19` 这几个数。

3. 如果是质数，就把答案加一。

这样遍历完所有数后，答案就得到了。

**为什么正确？**  
我们对每个数都完整地做了题目要求的两件事：统计集合位数 → 判断是否为质数。只要这两个子步骤都正确，整体答案自然正确。

**复杂度分析（大白话）**  
- **时间复杂度**：外层遍历 `right-left+1` 个数，最多 `10⁴+1`（题目限制），每个数统计二进制位数需要查看它的每一位，最多 20 次。因此总时间大约是 `O(N * 20)`，可以写成 `O(N)`（N 为区间长度），这里的 `O(N)` 实际上就是 **线性**，但常数是 20，足够快。  
- **空间复杂度**：只用了几个整数变量，和输入规模无关，记作 `O(1)`（常数空间）。

#### 代码（Python）

```python
def countPrimeSetBits_bruteforce(left: int, right: int) -> int:
    # 质数集合（只需要到 20）
    prime_set = {2, 3, 5, 7, 11, 13, 17, 19}
    ans = 0

    for num in range(left, right + 1):
        # 统计二进制里 1 的个数
        # 方法一：使用 bin() + count()
        # ones = bin(num).count('1')

        # 方法二：手动右移计数（更贴近位运算的本质）
        ones = 0
        x = num
        while x:
            ones += x & 1          # 取最低位是否为 1
            x >>= 1                # 右移一位，丢掉已经检查过的最低位

        # 判断是否是质数
        if ones in prime_set:
            ans += 1

    return ans
```

#### 复杂度

- **时间复杂度**：`O(N)`（N 为 `right-left+1`），每个数最多检查 20 位，实际运行很快。  
- **空间复杂度**：`O(1)`，只用了常数个额外变量。

---

### 2. 最优解

#### 思路  
暴力解已经是线性的，已经满足题目限制。但我们仍可以 **进一步简化代码**、**提升常数因子**，让实现更“优雅”：

1. **利用 Python 内置的位计数**  
   Python 3.8+ 提供 `int.bit_count()`，它直接返回二进制中 `1` 的个数，底层是用硬件指令或高效的算法实现，常数更小。

2. **预先准备好质数集合**  
   因为最大位数只有 20，直接写一个集合 `prime_set`，查找时间是 `O(1)`（哈希表就像字典，查词的速度几乎是瞬间的）。

3. **一次遍历**  
   仍然遍历 `[left, right]`，但每个数只做两件事：`num.bit_count()` → `prime_set` 查找。这样代码更简洁，执行更快。

**慢在哪里？**  
在暴力解里，手动右移计数每次都要循环 20 次，虽然不多，但 Python 循环本身有一定开销。使用 `bit_count()` 可以把这一步交给底层实现，省去 Python 循环的开销。

**核心技巧**：**位计数（popcount）** 与 **哈希表快速判质**。  
- **位计数**：把整数视作灯泡，数亮着的灯泡数目。现代 CPU 有专门指令，一行代码即可完成。  
- **哈希表快速判质**：把“哪些数字是质数”事先装进字典，查询时像查字典一样瞬间得到答案。

#### 代码（Python）

```python
def countPrimeSetBits(left: int, right: int) -> int:
    # 只需要判断到 20 位的质数
    prime_set = {2, 3, 5, 7, 11, 13, 17, 19}
    ans = 0

    for num in range(left, right + 1):
        # Python 内置的位计数，等价于统计二进制中 1 的个数
        ones = num.bit_count()          # O(1) 底层实现
        if ones in prime_set:           # 哈希表查找，几乎是瞬间
            ans += 1

    return ans
```

#### 复杂度

- **时间复杂度**：`O(N)`，仍然是线性遍历，但每个数的处理只用了常数时间（`bit_count` 与哈希查找），比手动右移更快。  
- **空间复杂度**：`O(1)`，只用了一个质数集合和若干计数变量。

---

## 心得

- **核心技巧**：位计数（popcount） + 哈希表快速判断质数。  
- **适用的题型**  
  1. “统计二进制中 1 的个数并做进一步判断”——如 **Counting Bits**、**Hamming Distance**。  
  2. “集合位数落在某个小范围内的计数”——如 **Number of Integers with Even Number of Digits**（改成二进制）。  
- **一句话总结解题钥匙**：**把整数的二进制视作灯泡，用一次 `bit_count` 把亮灯数拿到手，查哈希表判断是否为质数，线性遍历即可。**

## 反思

- **第一反应**：直接遍历区间，用 `bin(num).count('1')` 统计 1 的个数，再手动写一个判断质数的函数。  
- **最容易踩的坑**  
  - 忘记只需要判断到 20 位以内的质数，写了通用的质数检测会导致不必要的循环。  
  - 边界条件：`left`、`right` 可能相等，代码必须包含 `right` 本身（使用 `range(left, right+1)`）。  
- **下次遇到同类题**：第一步先**确定最大位数**（或最大可能的统计值），把所有可能的“好”值预先放进集合或数组，再**利用语言自带的位计数**或**查表**实现 O(1) 判断，最后线性遍历即可。