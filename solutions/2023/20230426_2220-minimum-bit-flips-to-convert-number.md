# #2220. 最少位翻转次数使数字相等 / Minimum Bit Flips to Convert Number

> 难度：简单 · 标签：Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/minimum-bit-flips-to-convert-number/)

---

## 题目（英文原版）

**Description**

A bit flip of a number x is choosing a bit in the binary representation of x and flipping it from either 0 to 1 or 1 to 0.
Given two integers start and goal, return the minimum number of bit flips to convert start to goal.
Note: This question is the same as 461: Hamming Distance.

**Examples**

**Example 1:**

```
Input: start = 10, goal = 7
Output: 3
Explanation: The binary representation of 10 and 7 are 1010 and 0111 respectively. We can convert 10 to 7 in 3 steps:
- Flip the first bit from the right: 1010 -> 1011.
- Flip the third bit from the right: 1011 -> 1111.
- Flip the fourth bit from the right: 1111 -> 0111.
It can be shown we cannot convert 10 to 7 in less than 3 steps. Hence, we return 3.
```

**Example 2:**

```
Input: start = 3, goal = 4
Output: 3
Explanation: The binary representation of 3 and 4 are 011 and 100 respectively. We can convert 3 to 4 in 3 steps:
- Flip the first bit from the right: 011 -> 010.
- Flip the second bit from the right: 010 -> 000.
- Flip the third bit from the right: 000 -> 100.
It can be shown we cannot convert 3 to 4 in less than 3 steps. Hence, we return 3.
```

**Constraints**

- 0 <= start, goal <= 109

---

## 题目（中文翻译）

**题目描述**  
对一个整数 `x` 的位翻转（bit flip）指的是在 `x` 的二进制表示中选取任意一位，并将其从 `0` 变为 `1`，或从 `1` 变为 `0`。  
给定两个整数 `start` 和 `goal`，返回将 `start` 转换为 `goal` 所需的最少位翻转次数。

**示例 1**  
**输入**: `start = 10, goal = 7`  
**输出**: `3`  
**解释**: `10` 与 `7` 的二进制分别为 `1010` 和 `0111`。我们可以在 3 步内完成转换：  
- 将最右侧的第一位翻转: `1010 → 1011`。  
- 将倒数第三位翻转: `1011 → 1111`。  
- 将倒数第四位翻转: `1111 → 0111`。  
可以证明，少于 3 步无法完成转换。因此返回 `3`。

**示例 2**  
**输入**: `start = 3, goal = 4`  
**输出**: `3`  
**解释**: `3` 与 `4` 的二进制分别为 `011` 和 `100`。我们可以在 3 步内完成转换：  
- 将最右侧的第一位翻转: `011 → 010`。  
- 将倒数第二位翻转: `010 → 000`。  
- 将倒数第三位翻转: `000 → 100`。  
可以证明，少于 3 步无法完成转换。因此返回 `3`。

**约束条件**  
- `0 <= start, goal <= 10^9`  

> **提示**：本题等价于 LeetCode 第 461 题 “Hamming Distance”。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把两个数的二进制位一个一个对比：  
- 把 `start` 和 `goal` 都写成二进制字符串（不足的位前面补 0），比如 `10 → 1010`、`7 → 0111`。  
- 从最右边的第一位开始往左遍历，每看到一对不同的位（一个是 0，另一个是 1），就记一次“翻转”。  
- 最后统计所有不同位的个数，就是把 `start` 变成 `goal` 所需的最少翻转次数。

**类比**：把每一位看成一本词典里的词条，`start` 的词条是“0”还是“1”。要把 `start` 改成 `goal`，就像在词典里把错误的词条改成正确的词条，一处错误就要改一次。

这个方法之所以正确，是因为**每一位的翻转互不影响**——翻第 3 位不会改变第 1 位的值，所以只要把所有不同的位都翻一次，就一定能得到目标数，且不可能更少。

#### 代码（Python）

```python
def min_bit_flips_bruteforce(start: int, goal: int) -> int:
    # 1. 把两个数转成二进制字符串，去掉前面的 '0b' 前缀
    bin_start = bin(start)[2:]
    bin_goal = bin(goal)[2:]

    # 2. 为了逐位对应，补齐长度（左侧补 0）
    max_len = max(len(bin_start), len(bin_goal))
    bin_start = bin_start.zfill(max_len)   # zfill 在左边补 0
    bin_goal = bin_goal.zfill(max_len)

    # 3. 逐位比较，统计不同的位数
    flips = 0
    for i in range(max_len):
        if bin_start[i] != bin_goal[i]:   # 只要两个字符不同，就需要翻转
            flips += 1
    return flips
```

#### 复杂度  

- **时间复杂度**：`O(k)`，这里的 `k` 是 `start`、`goal` 二进制表示的位数。因为我们要遍历每一位一次。  
  大白话：如果数字最大到 `10⁹`，二进制最多只有 30 位，所以最多只循环 30 次，几乎可以忽略不计。  
- **空间复杂度**：`O(k)`，存放两个二进制字符串以及补齐后的结果，同样最多 30‑40 个字符。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**把数字先转成字符串再遍历**，这一步虽然已经是线性时间，但我们可以直接在整数层面完成同样的比较，省去字符串的创建和遍历。  

关键观察：  
- 当两位相同时，`0 XOR 0 = 0`，`1 XOR 1 = 0`。  
- 当两位不同时，`0 XOR 1 = 1`，`1 XOR 0 = 1`。  

所以，把 `start` 与 `goal` 做一次 **异或（XOR）** 运算，得到的二进制数中恰好 1 的位置就是需要翻转的位。于是**计数二进制中 1 的个数**（也叫**汉明重量**）即为答案。

**类比**：XOR 就像是一把“比较尺”，把两本词典对应位置的词条放在一起，如果相同则尺子显示 0（不需要改），不同则显示 1（需要改）。随后我们只需要数一数尺子上有多少个 1。

实现计数 1 的方法有两种常见技巧：  
1. **循环右移**：每次检查最低位是否为 1，计数后右移一位，直到数变成 0。  
2. **Brian Kernighan 算法**：每次把 `x & (x - 1)`，可以一次消掉最低的 1，循环次数等于 1 的个数，效率更高。

这里用更简洁的 Python 内置函数 `bit_count()`（Python 3.8+ 可用 `bin(x).count('1')`），它内部已经用了高效的实现。

#### 代码（Python）

```python
def min_bit_flips(start: int, goal: int) -> int:
    """
    计算把 start 变成 goal 所需的最少位翻转次数
    思路：先异或得到不同位的掩码，然后统计其中 1 的个数
    """
    # 1. XOR 得到不同位的二进制掩码
    diff = start ^ goal          # 不同的位会变成 1

    # 2. 统计 diff 中 1 的个数
    # Python 3.10+ 可以直接使用 int.bit_count()
    flips = diff.bit_count()     # 等价于 bin(diff).count('1')

    return flips
```

> **注**：如果使用的 Python 版本不支持 `int.bit_count()`，可以改成  
> `flips = bin(diff).count('1')`（仍然是 O(k)）或手动实现 Brian Kernighan：

```python
def popcount(x: int) -> int:
    cnt = 0
    while x:
        x &= x - 1   # 把最低的 1 消掉
        cnt += 1
    return cnt
```

#### 复杂度  

- **时间复杂度**：`O(k)`，仍然是遍历二进制位的数量，但不需要额外的字符串转换。实际运行更快。  
- **空间复杂度**：`O(1)`，只用了常数级别的额外变量（`diff`、计数器），不随输入规模增长。

---

## 心得  

- **核心技巧**：使用 **异或 (XOR) 找不同位 + 计数二进制 1 的个数**（汉明距离）。  
- **适用题型**：  
  1. “Hamming Distance” 系列（LeetCode 461）。  
  2. “Number of Different Bits Between Two Integers”。  
  3. “Maximum XOR of Two Numbers in an Array”（需要先求异或，再利用位操作）。  
- **解题钥匙**：`start ^ goal` 把所有需要翻转的位一次性标记出来，只要数一数 1 的个数即可。

---

## 反思  

- **第一反应**：看到“翻转位”，立刻想到把两个数的二进制写出来对比。  
- **最容易踩的坑**：  
  - 忽视了高位的不同（直接用 `bin` 可能导致前导 0 被省掉，需要补齐）。  
  - 对大数不必手动补齐，因为 XOR 已经把所有位都考虑进去了。  
- **下次思考路径**：遇到“位翻转”“位差”这类描述，第一步想到 **异或**，随后根据需求决定是计数 1 还是寻找最高位等。这样可以快速从暴力想法跳到最优实现。