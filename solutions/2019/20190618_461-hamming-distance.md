# #461. 汉明距离 / Hamming Distance

> 难度：简单 · 标签：Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/hamming-distance/)

---

## 题目（英文原版）

**Description**

The Hamming distance between two integers is the number of positions at which the corresponding bits are different.
Given two integers x and y, return the Hamming distance between them.
Note: This question is the same as  2220: Minimum Bit Flips to Convert Number.

**Examples**

**Example 1:**

```
Input: x = 1, y = 4
Output: 2
Explanation:
1   (0 0 0 1)
4   (0 1 0 0)
       ↑   ↑
The above arrows point to positions where the corresponding bits are different.
```

**Example 2:**

```
Input: x = 3, y = 1
Output: 1
```

**Constraints**

- 0 <= x, y <= 231 - 1

---

## 题目（中文翻译）

两个整数之间的汉明距离（Hamming distance）指的是对应的二进制位（bit）中不同的位数。  
给定整数 `x` 和 `y`，返回它们之间的汉明距离。

**示例 1**  

**示例 2**  

**约束条件**  
- 0 ≤ x, y ≤ 2³¹ - 1  

> **注意**：本题与 2220: Minimum Bit Flips to Convert Number 完全相同。

---

### 示例

**示例 1**  
```
Input: x = 1, y = 4
Output: 2
Explanation:
1   (0 0 0 1)
4   (0 1 0 0)
       ↑   ↑
上图中的箭头指向二进制位不同的位置。
```

**示例 2**  
```
Input: x = 3, y = 1
Output: 1
```

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：把两个整数都展开成二进制的“串”，然后从右往左（或从左往右）一位一位比较，看它们在第几位上不相同，统计这样的位数即可。  

- **数据结构**：这里我们只需要把整数当成“二进制数组”。可以把整数不断除以 2（右移），每次取余数（`% 2`）得到最低位，然后把这个位存进列表里。列表就像一本字典，索引（下标）对应位的位置，值（0 或 1）对应该位的实际数字。  
- **为什么正确**：二进制的每一位都只能是 0 或 1，比较对应位是否相等恰好就是题目所说的“对应位不同”。把所有不同的位数加起来，就是 Hamming 距离。  

**时间复杂度**：我们要把两个数都转换成二进制，最多要遍历它们的最高位。因为题目限制 `x, y ≤ 2^31‑1`，最高位不超过 31 位，所以遍历次数最多是 31 次。我们把这个次数记作 `n`，则总体时间是 `O(n)`，在这里 `n` 只会是常数（31），所以可以说是 **O(1)**，但为了说明概念，仍然写成 `O(n)`。  
**空间复杂度**：我们用了两个列表分别存放二进制位，列表长度也是 `n`，所以是 `O(n)`（同理，这里也是常数空间）。

#### 代码（Python）  
```python
def hammingDistance_brute(x: int, y: int) -> int:
    # 把整数转换成二进制位列表（低位在前）
    def to_bits(num: int) -> list[int]:
        bits = []
        while num:                     # 当 num 不为 0 时循环
            bits.append(num % 2)       # 取最低位
            num //= 2                  # 右移一位
        return bits                    # 例如 5 -> [1,0,1]

    bits_x = to_bits(x)
    bits_y = to_bits(y)

    # 为了对齐长度，短的那边补 0
    max_len = max(len(bits_x), len(bits_y))
    bits_x += [0] * (max_len - len(bits_x))
    bits_y += [0] * (max_len - len(bits_y))

    # 逐位比较，统计不同的位数
    diff = 0
    for i in range(max_len):
        if bits_x[i] != bits_y[i]:    # 不同则计数
            diff += 1
    return diff
```

#### 复杂度  
- **时间复杂度**：`O(n)`（`n` 为整数的二进制位数，最多 31）——遍历每一位一次。  
- **空间复杂度**：`O(n)`——存放两个二进制位列表。  

---

### 2. 最优解  

#### 思路  
暴力解的瓶颈在于**显式地把每个数拆成列表**，这一步其实可以省掉。我们只需要知道对应位是否相同，而 **异或（XOR）** 正好能一次性告诉我们：  

- 对于同一位，如果两个比特相同（00 或 11），异或结果是 0；  
- 如果不同（01 或 10），异或结果是 1。  

所以 `x ^ y` 的二进制表示里，所有为 1 的位正好对应着“不同的位”。接下来我们只要统计这个数有多少个 1 即可，这个过程叫**计数二进制中 1 的个数**（也称“population count”或“位计数”）。

**计数 1 的常用技巧**：  
- **循环右移**：每次检查最低位 (`num & 1`) 然后右移 (`num >>= 1`)。这需要遍历所有位，时间是 O(n)。  
- **Brian Kernighan 算法**：每次 `num &= num - 1` 可以把最低的 1 删掉，循环的次数等于 1 的个数，通常更快。这里我们用更直观的右移方法，代码更易懂。  

**为什么最优**：我们只用了常数级别的位运算，没有额外的列表，空间降到 `O(1)`，时间仍是遍历位数（最多 31），在实际运行中快很多。

#### 代码（Python）  
```python
def hammingDistance(x: int, y: int) -> int:
    xor = x ^ y               # 1. 异或，得到不同位的掩码
    count = 0
    while xor:                # 只要还有 1，就继续计数
        count += xor & 1      # 取最低位是否为 1，若是则计数 +1
        xor >>= 1             # 右移一位，准备检查下一位
    return count
```

> **关键点注释**  
> - `x ^ y`：把两个数的二进制对应位做“不同即为 1”的操作。  
> - `xor & 1`：检查当前最低位是否为 1。  
> - `xor >>= 1`：把二进制整体右移一位，相当于除以 2，准备检查下一位。  

#### 复杂度  
- **时间复杂度**：`O(n)`（`n` 为二进制位数，最多 31），每次循环检查一位。相较于暴力解，省掉了构造列表的开销。  
- **空间复杂度**：`O(1)`——只用了若干个整数变量，没有额外的数组。  

---

## 心得  

- **核心技巧**：利用异或（XOR）一次性找出“不同位”，再用位计数求出 1 的个数。  
- **适用的题型**：  
  1. “两个数的二进制不同位数”类（如本题、LeetCode 2220 Minimum Bit Flips）。  
  2. “判断两个数的奇偶性是否相同”或“统计二进制中 1 的个数”类（如 191. Number of 1 Bits）。  
  3. “两数相加不进位的结果”类（异或直接相加）。  
- **一句话总结解题钥匙**：**异或找不同，位计数求答案**。  

---

## 反思  

- **第一反应**：把数字写成二进制字符串，逐位比较。  
- **最容易踩的坑**：  
  - 忘记对位数不相同的情况进行补齐（如 1 与 4 的二进制位数不同）。  
  - 在计数 1 时使用了错误的位运算，导致无限循环或漏计。  
- **下次类似题的第一步**：先思考是否可以用**位运算（尤其是 XOR）**一次性把“不同”抽取出来，再决定用何种方式统计 1 的个数。