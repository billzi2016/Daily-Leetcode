# #476. 整数补数 / Number Complement

> 难度：简单 · 标签：Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/number-complement/)

---

## 题目（英文原版）

**Description**

The complement of an integer is the integer you get when you flip all the 0's to 1's and all the 1's to 0's in its binary representation.
Given an integer num, return its complement.
Note: This question is the same as 1009: https://leetcode.com/problems/complement-of-base-10-integer/

**Examples**

**Example 1:**

```
Input: num = 5
Output: 2
Explanation: The binary representation of 5 is 101 (no leading zero bits), and its complement is 010. So you need to output 2.
```

**Example 2:**

```
Input: num = 1
Output: 0
Explanation: The binary representation of 1 is 1 (no leading zero bits), and its complement is 0. So you need to output 0.
```

**Constraints**

- 1 <= num < 231

---

## 题目（中文翻译）

整数的补数（complement）是指在其二进制表示（binary representation）中把所有的 `0` 翻成 `1`，所有的 `1` 翻成 `0` 后得到的整数。给定整数 `num`，返回它的补数。

**示例 1**  
**示例 2**  
**约束**  
- `1 <= num < 2^31`  

**备注**：本题与 1009 题相同，参见 https://leetcode.com/problems/complement-of-base-10-integer/

### 示例

**示例 1**  
Input: `num = 5`  
Output: `2`  
Explanation: 5 的二进制表示（binary representation）为 `101`（没有前导零），其补数为 `010`，所以输出 `2`。

**示例 2**  
Input: `num = 1`  
Output: `0`  
Explanation: 1 的二进制表示（binary representation）为 `1`（没有前导零），其补数为 `0`，所以输出 `0`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把整数先转成二进制的字符串，像 `"101"` 那样，然后把每个字符 `'0'` 换成 `'1'`，`'1'` 换成 `'0'`，得到补码的二进制字符串，再把它转回十进制整数。

- **数据结构**：这里我们只用到 **字符串**。可以把二进制看成一本“只写 0 和 1 的书”，把每一页（字符）翻面就相当于把 0↔1。
- **正确性**：题目要求把二进制表示中的每一位都取反，而字符串的每个字符正好对应二进制的每一位，逐位翻转后再转成整数，就是题目要求的“补数”。
- **复杂度**：  
  - 把整数转成二进制需要遍历所有位，位数大约是 `log₂(num)`（比如 5 → 3 位）。  
  - 翻转字符串再转回整数，同样要遍历这些位。  
  - 所以 **时间复杂度** 为 `O(log num)`，在大白话里就是“和数字的二进制位数成正比”。  
  - 我们额外创建了一个二进制字符串，长度也是 `log₂(num)`，因此 **空间复杂度** 为 `O(log num)`。

#### 代码（Python）

```python
def findComplement_bruteforce(num: int) -> int:
    # 1️⃣ 把整数转成二进制字符串（去掉 Python 默认的 '0b' 前缀）
    bin_str = bin(num)[2:]                     # 例如 5 → '101'

    # 2️⃣ 逐位取反：0 变 1，1 变 0
    complement_bits = []
    for ch in bin_str:
        if ch == '0':
            complement_bits.append('1')
        else:  # ch == '1'
            complement_bits.append('0')
    complement_str = ''.join(complement_bits)  # 例如 '101' → '010'

    # 3️⃣ 把翻转后的二进制字符串再转成十进制整数返回
    return int(complement_str, 2)               # '010' → 2
```

#### 复杂度

- **时间复杂度**：`O(log num)` —— 只和二进制位数有关，位数越多花的时间越多。  
- **空间复杂度**：`O(log num)` —— 需要额外存放二进制字符串和翻转后的字符列表。

---

### 2. 最优解

#### 思路  

虽然暴力解已经能跑通，但它用了额外的字符串，空间和时间上都有“多余的搬砖”。我们可以直接在 **位运算** 层面完成取反，省去字符串的来回转换。

1. **找出最高位的掩码**  
   对于 `num = 5 (101₂)`，最高位是第 3 位。我们想要一个全 1 的掩码，长度恰好和 `num` 的二进制位数相同，即 `111₂`（十进制 7）。只要把 `num` 的最高位左移一位得到 `1000₂`，再减 1，就得到 `111₂`。这一步的核心操作是 `mask = (1 << bit_len) - 1`，其中 `bit_len` 是二进制位数。

2. **位翻转**  
   - 直接用异或 `^`：`num ^ mask` 会把 `num` 中的 0 变成 1，1 变成 0，因为 `mask` 的每一位都是 1。  
   - 或者用取反再与掩码：`(~num) & mask`。`~num` 把所有位都取反（包括高位的无限补码 1），再用掩码把多余的高位清零。

3. **如何得到 bit_len**  
   我们可以不断右移 `num`（`num >>= 1`）并计数，直到 `num` 变成 0 为止。计数的次数就是二进制位数。

> **类比**：把 `num` 想成一根尺子，上面刻着若干格子（每格对应一位）。我们先把尺子量满（构造全 1 的掩码），再把尺子和掩码对应的格子“相减”，就得到每格翻转后的结果。

#### 代码（Python）

```python
def findComplement(num: int) -> int:
    # 边界：如果 num 为 0（题目保证 >=1），补码应该是 1，但这里不需要处理。
    # 1️⃣ 计算二进制位数
    bit_len = 0
    temp = num
    while temp:
        bit_len += 1          # 记录我们已经看了多少位
        temp >>= 1            # 右移一位，等价于除以 2

    # 2️⃣ 构造全 1 的掩码，长度恰好是 bit_len 位
    mask = (1 << bit_len) - 1   # 1 左移 bit_len 位后减 1，例如 bit_len=3 → 0b111

    # 3️⃣ 用异或实现位翻转
    return num ^ mask
```

> **注**：如果你更喜欢 “取反后掩码” 的写法，只需要把最后一行改成 `return (~num) & mask`，效果完全相同。

#### 复杂度

- **时间复杂度**：`O(log num)` —— 只遍历二进制位数一次（求位数的循环）和一次常数位运算。相较于暴力解，省掉了字符串的遍历与拼接，实际运行更快。
- **空间复杂度**：`O(1)` —— 只用了几个整数变量，没有额外的随位数增长的存储。

---

## 心得

- **核心技巧**：**位掩码 + 异或**（或取反再掩码）。通过构造一个全 1 的掩码，使得每一位都能被“一键翻转”。
- **适用题型**：
  1. **求二进制取反**（本题）。
  2. **把整数的二进制反转后再转成十进制**（如 LeetCode 190：Reverse Bits）。
  3. **找出最高位的 1 并做相应操作**（如 LeetCode 342：Power of Four 判断）。
- **一句话总结**：先把目标数的二进制长度补齐为全 1，然后用异或“一次搞定”全部位的翻转。

---

## 反思

- **第一反应**：把数字转成二进制字符串，逐位取反，再转回整数——最直观但不是最省时省空间的办法。
- **最容易踩的坑**：
  - **忽略最高位**：如果直接用 `~num`，会把整数的符号位（无限的 1）也翻转，需要用掩码把高位清零。
  - **边界条件**：虽然题目保证 `num ≥ 1`，但若出现 `num = 0`，我们的位数循环会得到 `0`，此时掩码应为 `1`（因为 `0` 的二进制补码是 `1`），需要额外判断。
- **下次遇到类似题**：先思考**“我需要一个和原数位数相同、全是 1 的数字吗？”**——如果答案是肯定的，马上想到**位掩码 + 异或**的组合。