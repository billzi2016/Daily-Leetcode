# #3370. 全为 1 的最小数 / Smallest Number With All Set Bits

> 难度：简单 · 标签：Math、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/smallest-number-with-all-set-bits/)

---

## 题目（英文原版）

**Description**

You are given a positive number n.
Return the smallest number x greater than or equal to n, such that the binary representation of x contains only set bits

**Examples**

**Example 1:**

```
Input: n = 5
Output: 7
Explanation:
The binary representation of 7 is "111" .
```

**Example 2:**

```
Input: n = 10
Output: 15
Explanation:
The binary representation of 15 is "1111" .
```

**Example 3:**

```
Input: n = 3
Output: 3
Explanation:
The binary representation of 3 is "11" .
```

**Constraints**

- 1 <= n <= 1000

---

## 题目（中文翻译）

**描述**  
给定一个正整数 `n`。返回大于等于 `n` 的最小整数 `x`，使得 `x` 的二进制表示仅包含已置位（set bits）。

**示例**

*示例 1*  
```
Input: n = 5
Output: 7
Explanation:
7 的二进制表示为 "111"。
```

*示例 2*  
```
Input: n = 10
Output: 15
Explanation:
15 的二进制表示为 "1111"。
```

*示例 3*  
```
Input: n = 3
Output: 3
Explanation:
3 的二进制表示为 "11"。
```

**约束条件**  
- `1 <= n <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **从 n 开始往上找**，每检查一个数 `x`，判断它的二进制里是不是全部都是 `1`。  
- 判断“全是 1”可以用一个小技巧：如果一个数的二进制全部是 1，那么把它加 1 就会得到一个形如 `1000…0` 的数，两者做位与运算必然得到 0。即 `x & (x + 1) == 0`。  
- 这里用到的位运算就像在纸上写二进制数后直接进位一样，**哈希表**在这里并不需要，只要会用 `&`（与）和 `+`（加）即可。

这个方法之所以一定能得到答案，是因为**所有全 1 的数都是形如 `2^k - 1`**（比如 `111b = 7 = 2³-1`），而整数集合是连续的，必然能在 `n` 之后的某个位置碰到下一个 `2^k - 1`。

#### 代码（Python）

```python
def smallest_all_ones_bruteforce(n: int) -> int:
    x = n                     # 从 n 开始检查
    while True:
        # 如果 x 的二进制全是 1，则 x & (x+1) 必为 0
        if x & (x + 1) == 0:  # 位运算：判断全 1
            return x
        x += 1                # 继续往上找
```

#### 复杂度

- **时间复杂度**：`O(d)`，其中 `d` 是 `n` 到答案之间的距离。最坏情况下（比如 `n = 2^k`），我们可能要检查大约 `2^k - (2^{k-1} - 1) ≈ 2^{k-1}` 次，直观上可以理解为“要遍历的数字个数”。  
- **空间复杂度**：`O(1)`，只用了常数个变量 `x`。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **逐个检查**，当 `n` 与最近的全 1 数相差很大时会非常慢。我们可以直接算出答案，而不是一步步逼近。

观察全 1 数的形态：

```
1        -> 2^1 - 1
11       -> 2^2 - 1
111      -> 2^3 - 1
...
```

也就是说，只要知道需要多少位 `k`，答案就是 `(1 << k) - 1`（左移相当于乘 2 的幂次）。

**如何得到合适的 k？**  
- 先看 `n` 的二进制长度 `bits = n.bit_length()`，这相当于 “把 n 看成多少位”。  
- 用 `bits` 位全 1 的数 `candidate = (1 << bits) - 1`。  
  - 如果 `candidate >= n`，说明已经够大，直接返回。  
  - 否则说明 `n` 超过了当前位数能表示的最大全 1 数，需要再多加一位，即 `bits + 1`，答案是 `(1 << (bits + 1)) - 1`。

这个过程只用了 **一次位数的计算**，不需要循环遍历，时间大幅提升。

#### 代码（Python）

```python
def smallest_all_ones_optimal(n: int) -> int:
    # n 的二进制需要多少位（不包括前导零）
    bits = n.bit_length()          # 类似“数有几位”
    
    # 用 bits 位全 1 的数：111...1（bits 个 1）
    candidate = (1 << bits) - 1    # 1 左移 bits 位再减 1，相当于 2^bits - 1
    
    if candidate >= n:
        return candidate           # 已经满足条件，直接返回
    # 否则再加一位，得到更大的全 1 数
    return (1 << (bits + 1)) - 1
```

#### 复杂度

- **时间复杂度**：`O(1)`，只做了几次位运算和一次 `bit_length()`，不随 `n` 的大小增长。相比暴力的 `O(d)`，快得多。  
- **空间复杂度**：`O(1)`，同样只用了常数个变量。

---

## 心得

- **核心技巧**：利用全 1 数的数学形式 `2^k - 1`，结合二进制位数 (`bit_length`) 直接构造答案。  
- **适用场景**：  
  1. 求最小的形如 `2^k`（幂）或 `2^k - 1`（全 1）的大于等于给定数的问题。  
  2. 与 “下一个更高的 1 位数” 类似的位运算题，如 **Next Power of Two**、**Binary Prefix** 等。  
- **解题钥匙**：把“全部是 1”转化为 “`2^k - 1`”，然后只需要算出合适的 `k`。

---

## 反思

- **第一反应**：看到“全是 1 的二进制”，自然想到 `2^k - 1`，于是想直接枚举 `k`。  
- **最容易踩的坑**：  
  - 忘记 `bit_length()` 对 `0` 的返回是 `0`（本题 `n ≥ 1`，不受影响）。  
  - 只检查 `bits` 位的全 1 数，却忘记在 `candidate < n` 时需要再加一位。  
- **下次类似题的第一步**：先把“特殊二进制形态”用数学式子写出来（如 `2^k`、`2^k-1`、`(1<<k)-1`），再利用位数或对数快速定位 `k`。