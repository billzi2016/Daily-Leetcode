# #3099. Harshad 数 / Harshad Number

> 难度：简单 · 标签：Math · [LeetCode 链接](https://leetcode.com/problems/harshad-number/)

---

## 题目（英文原版）

**Description**

An integer divisible by the sum of its digits is said to be a Harshad number. You are given an integer x. Return the sum of the digits of x if x is a Harshad number, otherwise, return -1.

**Examples**

**Example 1:**

```
Input: x = 18
Output: 9
Explanation:
The sum of digits of x is 9 . 18 is divisible by 9 . So 18 is a Harshad number and the answer is 9 .
```

**Example 2:**

```
Input: x = 23
Output: -1
Explanation:
The sum of digits of x is 5 . 23 is not divisible by 5 . So 23 is not a Harshad number and the answer is -1 .
```

**Constraints**

- 1 <= x <= 100

---

## 题目（中文翻译）

整数如果能够被其各位数字之和整除，则称为 **Harshad 数（Harshad number）**。给定整数 `x`，如果 `x` 是 Harshad 数，返回 `x` 的各位数字之和；否则返回 `-1`。

**示例 1**  
**示例 2**  
**约束条件**：

### 示例

#### 示例 1
``` 
Input: x = 18
Output: 9
```
**解释**：  
`x` 的各位数字之和为 9。18 能被 9 整除，所以 18 是 Harshad 数，答案为 9。

#### 示例 2
``` 
Input: x = 23
Output: -1
```
**解释**：  
`x` 的各位数字之和为 5。23 不能被 5 整除，因此 23 不是 Harshad 数，答案为 -1。

### 约束条件
- `1 <= x <= 100`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法就是：先把整数 `x` 的每一位数字加起来得到 **数字之和**，再判断 `x` 能否被这个和整除。  

- **怎么把数字一位一位取出来？**  
  想象把 `x` 当成一串珠子，每颗珠子是一个十进制位。我们可以用 “取模 10” (`x % 10`) 把最右边的珠子摘下来，用 “整除 10” (`x //= 10`) 把它从原串里去掉，循环往复直到珠子全部摘完。这个过程就像把一本书从最后一页往前翻，**取模** 就是看当前页码，**整除** 就是把书往前翻一页。  

- **判断是否是 Harshad 数**  
  计算出数字之和 `s` 后，只要 `x % s == 0`（即 `x` 能被 `s` 整除），说明 `x` 是 Harshad 数，答案返回 `s`；否则返回 `-1`。  

- **为什么这个方法一定对？**  
  我们把 **每一位** 的数值都加到了 `s`，而除法判断正是题目要求的“能否被数字之和整除”。没有遗漏，也没有多余的步骤，逻辑完整。

- **时间/空间复杂度**  
  - **时间**：我们需要遍历 `x` 的每一位。`x` 的位数大约是 `log10(x)`（十进制的位数），所以时间是 **O(log x)**。用大白话说，就是 **“和 `x` 的位数成正比”**，比如 `x=12345` 需要 5 次循环。  
  - **空间**：只用了几个整数变量，和 `x` 的大小无关，**O(1)**（常数空间）。

#### 代码（Python）

```python
def sum_of_digits(x: int) -> int:
    """
    计算整数 x 的各位数字之和
    """
    total = 0               # 用来累加每一位的数字
    while x > 0:            # 当还有未处理的位时循环
        total += x % 10     # 取最右边一位并加到 total
        x //= 10            # 把最右边一位“删掉”，相当于右移一位
    return total


def sum_of_digits_if_harshad(x: int) -> int:
    """
    如果 x 是 Harshad 数，返回它的数字之和；否则返回 -1
    """
    s = sum_of_digits(x)    # 先算出数字之和
    if s != 0 and x % s == 0:   # 判断能否被整除（s 不会为 0，因为 x≥1）
        return s
    else:
        return -1
```

#### 复杂度  

- **时间复杂度**：`O(log x)` —— 只和数字的位数有关，位数越多循环次数越多。  
- **空间复杂度**：`O(1)` —— 只用了常数个变量，不随 `x` 大小变化。

---  

### 2. 最优解  

#### 思路  

对于本题，**暴力解已经是最优**，因为我们只能遍历每一位数字一次来得到它们的和。没有办法在不查看每一位的情况下得出数字之和，也没有必要使用更高级的数据结构（如哈希表、前缀和）来加速——这些都不会降低时间复杂度，反而会增加额外开销。  

唯一可以改进的细节是 **把求和与整除判断合并在一次循环里**，这样可以省掉一次函数调用的开销（在 Python 里这几乎可以忽略不计），但时间复杂度仍是 `O(log x)`，空间仍是 `O(1)`。

#### 代码（Python）

```python
def sum_of_digits_if_harshad_opt(x: int) -> int:
    """
    在一次遍历中同时求数字之和并判断是否为 Harshad 数
    """
    original = x              # 记住原始值，后面要用来做除法判断
    digit_sum = 0

    while x > 0:
        digit_sum += x % 10   # 加上当前位
        x //= 10              # 去掉当前位

    # 循环结束后，digit_sum 已经是所有位的和
    return digit_sum if digit_sum != 0 and original % digit_sum == 0 else -1
```

#### 复杂度  

- **时间复杂度**：`O(log x)` —— 仍然是遍历每一位数字一次。  
- **空间复杂度**：`O(1)` —— 只用常数个整数变量。

---

## 心得  

- **核心技巧**：**逐位求和 + 整除判断**，也就是把十进制数拆成一位一位的“珠子”。  
- **适用的题型**  
  1. 判断一个数是否能被其各位数字之和整除（Harshad 数）。  
  2. 计算数字之和后进行某种判定（如 “数字之和是奇数/偶数”）。  
  3. 需要把整数拆成各位进行处理的题目（如 “判断回文数”）。  
- **一句话总结解题钥匙**：**“把大数拆成小数位，逐位累加，再用原数做除法”**。

## 反思  

- **第一反应**：先想“把数字拆开求和”，因为题目明确要求“数字之和”。  
- **最容易踩的坑**  
  - 忘记 **`x` 可能只有一位**，循环仍然要执行一次。  
  - 忘记 **`digit_sum` 可能为 0**（在本题不可能，因为 `x ≥ 1`），但在写通用代码时要防止除以 0。  
  - 忽略 **返回值必须是数字之和**，而不是布尔值。  
- **下次遇到同类题**：第一步先 **“逐位遍历 + 累加”**，随后根据题意决定是否继续比较、判断或返回。这样思路清晰，代码也自然简洁。