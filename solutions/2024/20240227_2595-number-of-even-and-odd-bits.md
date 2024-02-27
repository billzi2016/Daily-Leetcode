# #2595. 偶数位和奇数位的个数 / Number of Even and Odd Bits

> 难度：简单 · 标签：Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/number-of-even-and-odd-bits/)

---

## 题目（英文原版）

**Description**

You are given a positive integer n.
Let even denote the number of even indices in the binary representation of n with value 1.
Let odd denote the number of odd indices in the binary representation of n with value 1.
Note that bits are indexed from right to left in the binary representation of a number.
Return the array [even, odd].

**Examples**

**Example 1:**

```
Input: n = 50
Output: [1,2]
Explanation:
The binary representation of 50 is 110010 .
It contains 1 on indices 1, 4, and 5.
```

**Example 2:**

```
Input: n = 2
Output: [0,1]
Explanation:
The binary representation of 2 is 10 .
It contains 1 only on index 1.
```

**Constraints**

- 1 <= n <= 1000

---

## 题目（中文翻译）

给定一个正整数（positive integer）`n`。

记 **even** 为 `n` 的二进制表示（binary representation）中，索引为偶数且对应位为 `1` 的个数。  
记 **odd** 为 `n` 的二进制表示中，索引为奇数且对应位为 `1` 的个数。

注意，二进制位的索引从右向左、从 `0` 开始计数。

返回数组（array）`[even, odd]`。

---

**示例 1**  
**输入**: `n = 50`  
**输出**: `[1,2]`  
**解释**:  
`50` 的二进制表示为 `110010`。  
其中 `1` 出现在索引 `1、4、5` 处，偶数索引只有 `4` 一个，奇数索引有 `1、5` 两个，因此结果为 `[1,2]`。

**示例 2**  
**输入**: `n = 2`  
**输出**: `[0,1]`  
**解释**:  
`2` 的二进制表示为 `10`。  
`1` 只出现在索引 `1`（奇数）处，所以结果为 `[0,1]`。

---

**约束条件**  
- `1 <= n <= 1000`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把整数 `n` 转成二进制字符串，然后逐个字符检查它是不是 `'1'`。  
- **数据结构**：二进制字符串就像一串珠子，左边是高位，右边是低位。我们把每一颗珠子的位置（下标）记下来，判断它是偶数位还是奇数位。  
- **为什么正确**：题目只要统计“二进制里为 1 的偶数位”和“二进制里为 1 的奇数位”，遍历整条珠子链，遇到 `'1'` 就把对应的计数器加一，最后得到的 `[even, odd]` 正是答案。  
- **时间/空间复杂度**：  
  - 需要把整数转换成字符串，长度是 `log₂ n`（二进制位数），遍历一次即可。  
  - 时间复杂度记作 **O(log n)**，这里的 `log n` 可以理解为“二进制位数”，比如 `n=50` 时有 6 位，就只需要检查 6 次。  
  - 额外空间只用了两个计数器和一个字符串，空间复杂度是 **O(log n)**（存放二进制字符串需要的空间）。  

#### 代码（Python）  

```python
def even_odd_bits_brute(n: int) -> list[int]:
    # 把 n 转成二进制字符串，去掉前面的 '0b'
    b = bin(n)[2:]                 # 例如 50 -> '110010'
    even, odd = 0, 0               # 偶数位计数、奇数位计数

    # 逆序遍历，右边（最低位）对应下标 0，左边依次递增
    for idx, ch in enumerate(reversed(b)):
        if ch == '1':              # 只统计位为 1 的情况
            if idx % 2 == 0:       # idx 为偶数 → 偶数位
                even += 1
            else:                  # idx 为奇数 → 奇数位
                odd += 1
    return [even, odd]
```

#### 复杂度  

- **时间复杂度**：`O(log n)` – 只遍历二进制位的个数。  
- **空间复杂度**：`O(log n)` – 用了一个长度为二进制位数的字符串。  

---

### 2. 最优解  

#### 思路  
暴力解已经是 **O(log n)**，已经很快了。但我们可以省掉把整数转成字符串的那一步，直接用位运算（`&`、`>>`）一次遍历整数的每一位。  

- **慢在哪里**：`bin()` 会在内部创建一个新字符串，虽然时间仍是 `O(log n)`，但额外的字符串拷贝会带来一点点不必要的开销。  
- **优化思路**：  
  1. 用变量 `idx` 记录当前位的下标（从 0 开始）。  
  2. `n & 1` 可以直接判断最低位是否为 1（就像检查珠子最右边的颜色）。  
  3. 判断完后，把 `n` 右移一位（`n >>= 1`），相当于把珠子链整体往右滑动一格，下一次循环继续检查新的最低位。  
  4. 当 `n` 变成 0 时，所有位都已检查完，退出循环。  

- **核心数据结构**：位运算。把二进制位看作“一排灯泡”，`& 1` 就是“只看最右边那盏灯是否亮”。  

- **类比**：想象你手里有一根尺子，上面标了刻度（位下标），每次只看最右边的刻度，记下是否有标记（位为 1），然后把尺子整体左移一格，继续检查。这样就不需要先把尺子展开成文字（字符串）了。  

#### 代码（Python）  

```python
def even_odd_bits_optimal(n: int) -> list[int]:
    even, odd = 0, 0          # 计数器
    idx = 0                   # 当前位的下标（从 0 开始）

    while n:                  # 当 n 仍然大于 0 时继续
        if n & 1:             # 检查最低位是否为 1（相当于看最右边的灯是否亮）
            if idx % 2 == 0:  # 偶数下标 → 偶数位
                even += 1
            else:             # 奇数下标 → 奇数位
                odd += 1
        n >>= 1                # 右移一位，准备检查下一位
        idx += 1               # 下标加一
    return [even, odd]
```

#### 复杂度  

- **时间复杂度**：`O(log n)` – 仍然只遍历二进制位的个数。和暴力解的时间相同，但省掉了字符串创建的常数时间。  
- **空间复杂度**：`O(1)` – 只用了几个整数变量，没有额外随位数增长的空间。  

---

## 心得  

- **核心技巧**：位运算（`&`、`>>`）配合下标计数。  
- **适用的题型**：  
  1. “Number of 1 Bits”（统计二进制中 1 的个数）  
  2. “Reverse Bits”（把二进制位倒序）  
  3. “Binary Subarray Sum”（利用前缀异或求二进制子数组）  
- **解题钥匙**：**把整数看成一串灯泡，用位运算一盏盏检查**。  

## 反思  

- **第一反应**：把 `n` 直接 `bin()` 成字符串，然后逐字符计数。  
- **最容易踩的坑**：  
  - **下标方向**：题目要求“从右往左”编号，左边是高位，右边是低位；容易写成从左往右导致计数错误。  
  - **边界情况**：`n = 1`（只有第 0 位），需要确保偶数位计数为 1，奇数位为 0。  
- **下次思路**：看到“二进制位的奇偶统计”或“按位操作”时，第一步就想到 **位运算 + 循环右移**，而不是先转成字符串。这样既省时又省空间。