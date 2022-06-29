# #1837. 进制 K 中数字之和 / Sum of Digits in Base K

> 难度：简单 · 标签：Math · [LeetCode 链接](https://leetcode.com/problems/sum-of-digits-in-base-k/)

---

## 题目（英文原版）

**Description**

Given an integer n (in base 10) and a base k, return the sum of the digits of n after converting n from base 10 to base k.
After converting, each digit should be interpreted as a base 10 number, and the sum should be returned in base 10.

**Examples**

**Example 1:**

```
Input: n = 34, k = 6
Output: 9
Explanation: 34 (base 10) expressed in base 6 is 54. 5 + 4 = 9.
```

**Example 2:**

```
Input: n = 10, k = 10
Output: 1
Explanation: n is already in base 10. 1 + 0 = 1.
```

**Constraints**

- 1 <= n <= 100
- 2 <= k <= 10

---

## 题目（中文翻译）

给定一个十进制整数 `n` 和一个进制 `k`，返回将 `n` 从十进制 (base 10) 转换为 `k` 进制 (base k) 后，各位数字的和。  
转换后，每个数字应按十进制数值解释，求得的和也以十进制返回。

**示例 1**  
**输入**: `n = 34, k = 6`  
**输出**: `9`  
**解释**: `34`（十进制）用 `6` 进制表示为 `54`。`5 + 4 = 9`。

**示例 2**  
**输入**: `n = 10, k = 10`  
**输出**: `1`  
**解释**: `n` 已经是十进制。`1 + 0 = 1`。

**约束条件**  
- `1 <= n <= 100`  
- `2 <= k <= 10`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的办法就是把十进制整数 `n` **手动** 转成 `k` 进制，然后把每一位相加。  
- **转换过程**：不断把 `n` 除以 `k`，余数就是最低位（最右边）的数字。把余数记下来后，把 `n` 更新为商 `n // k`，继续循环，直到商为 0。  
- **类比**：这就像我们把一本书从后往前翻页，先看到最后一页的页码（余数），再翻到前一页（商），一直翻到封面。  
- **为什么正确**：除以 `k` 的余数恰好是 `k` 进制表示中对应位的数值，所有余数按逆序（从低位到高位）排列即得到完整的 `k` 进制数字。把这些余数相加，就是题目要求的“各位数字之和”。  

#### 代码（Python）  

```python
def sum_of_digits_in_base_k(n: int, k: int) -> int:
    """把十进制 n 转成 k 进制，并返回各位数字之和（仍然是十进制）"""
    total = 0               # 用来累计各位数字的和
    while n > 0:            # 当还有未处理的高位时循环
        digit = n % k       # 余数就是当前最低位的数字
        total += digit      # 累加到答案
        n //= k             # 把 n 缩小到剩余的高位部分
    return total
```

*关键行中文注释已写在代码里，直接复制运行即可。*  

#### 复杂度  

- **时间复杂度：** `O(log_k n)`  
  - 解释：每次循环把 `n` 除以 `k`，相当于把数字的位数“削掉”一位。循环次数等于 `n` 在 `k` 进制下的位数，记作 `log_k n`（对数的意思是“多少个 k 能乘到 n”。）  
- **空间复杂度：** `O(1)`  
  - 解释：只用了几个整数变量，和输入规模无关，恒定不变。  

---  

### 2. 最优解  

#### 思路  
对于本题，**暴力解已经是最优**，因为我们只能逐位读取 `k` 进制的每一位，无法跳过任何一步。  
- **瓶颈**：没有额外的循环或数据结构会导致更高的复杂度。  
- **优化思路**：唯一可以做的就是把代码写得更简洁或利用 Python 的内置函数一次性完成转换。但时间复杂度仍是 `O(log_k n)`，空间仍是 `O(1)`。  

下面给出一种利用 **Python 的 `while` 循环**（与上面相同）以及一种 **利用 `int` 的进制转换** 的写法，供读者了解不同的实现方式。  

#### 代码（Python）  

**方式 1：手动除取余（推荐，最直观）**  

```python
def sum_of_digits_in_base_k(n: int, k: int) -> int:
    total = 0
    while n:
        total += n % k      # 取当前最低位并累加
        n //= k             # 删除已经处理的最低位
    return total
```

**方式 2：利用 Python 的 `format`（仅适用于 k ≤ 10）**  

```python
def sum_of_digits_in_base_k(n: int, k: int) -> int:
    # 把 n 转成 k 进制的字符串，例如 n=34, k=6 -> "54"
    base_k_str = ''
    while n:
        base_k_str = str(n % k) + base_k_str
        n //= k
    # 把每个字符（仍是十进制的数字）转成 int 再求和
    return sum(int(ch) for ch in base_k_str)
```

> 这里的 `format` 思路其实仍是手动除余，只是把余数拼接成字符串再求和。两者在复杂度上是等价的。  

#### 复杂度  

- **时间复杂度：** `O(log_k n)`  
  - 与暴力解完全相同，因为无论怎么写，都必须遍历 `k` 进制的每一位。  
- **空间复杂度：** `O(1)`（方式 1）或 `O(log_k n)`（方式 2，存字符串）  
  - 方式 1 只用常数个变量；方式 2 需要额外的字符串来保存所有位，但位数本身就是 `log_k n`，在本题的极小约束（`n ≤ 100`）下影响可以忽略。  

---  

## 心得  

- **核心技巧**：**“逐位除余”**——把一个十进制数转成任意进制时，除以进制基数得到余数即为当前位的数值。  
- **适用的题型**：  
  1. *Convert a Number to Base K*（把数字转换成任意进制）  
  2. *Number of Steps to Reduce a Number in Binary*（二进制位操作）  
  3. *Additive Persistence*（求数字各位相加的迭代次数）  
- **解题钥匙**：**“把大问题拆成“每一次只处理最右边一位”**，循环直至没有剩余。  

## 反思  

- **第一反应**：直接想到“除以 k，余数就是一位”，于是写出循环。  
- **最容易踩的坑**：  
  - 忘记在 `while n > 0` 前处理 `n = 0` 的情况（虽然本题约束 `n ≥ 1`，但养成好习惯）。  
  - 对进制 `k` 超过 10 时，余数可能是两位数，需要额外的字符映射（本题 `k ≤ 10`，所以可以直接使用 `str(digit)`）。  
- **下次遇到同类题**：第一步先**确定“逐位处理”是否可行**，即是否可以通过除余得到每一位；如果可以，就立刻写出 `while n:` 循环框架。