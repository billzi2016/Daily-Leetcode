# #1018. 二进制前缀能被5整除 / Binary Prefix Divisible By 5

> 难度：简单 · 标签：Array、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/binary-prefix-divisible-by-5/)

---

## 题目（英文原版）

**Description**

You are given a binary array nums (0-indexed).
We define xi as the number whose binary representation is the subarray nums[0..i] (from most-significant-bit to least-significant-bit).
Return an array of booleans answer where answer[i] is true if xi is divisible by 5.

**Examples**

**Example 1:**

```
Input: nums = [0,1,1]
Output: [true,false,false]
Explanation: The input numbers in binary are 0, 01, 011; which are 0, 1, and 3 in base-10.
Only the first number is divisible by 5, so answer[0] is true.
```

**Example 2:**

```
Input: nums = [1,1,1]
Output: [false,false,false]
```

**Constraints**

- 1 <= nums.length <= 105
- nums[i] is either 0 or 1.

---

## 题目（中文翻译）

你得到一个二进制数组 (binary array) `nums`（下标从 0 开始）。  
我们定义 `xi` 为二进制表示为子数组 (subarray) `nums[0..i]` 的整数（从最高位到最低位）。  
返回一个布尔数组 `answer`，其中 `answer[i]` 为 `true` 当且仅当 `xi` 能被 5 整除。

**示例 1**  
**输入**: `nums = [0,1,1]`  
**输出**: `[true,false,false]`  
**解释**: 二进制数分别为 `0`、`01`、`011`，对应十进制为 `0、1、3`。只有第一个数能被 5 整除，因此 `answer[0]` 为 `true`。

**示例 2**  
**输入**: `nums = [1,1,1]`  
**输出**: `[false,false,false]`

**约束条件**  
- `1 <= nums.length <= 10^5`  
- `nums[i]` 只能是 `0` 或 `1`。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：**每次都把从第 0 位到第 i 位的二进制数完整地算出来，再判断它能不能被 5 整除**。  
可以把这一步想象成“从左到右读一本书的章节”，每读完一章（即一个前缀），我们就把这段文字重新转成十进制的数字，然后除以 5 看余数是否为 0。  

实现细节  
- 用 `int` 类型把二进制位拼成整数：`value = value * 2 + nums[j]`（相当于在十进制里左移一位再加上当前位）。  
- 为了得到第 i 个前缀的值，需要把 `j` 从 0 循环到 i。  
- 判断 `value % 5 == 0`，把结果放进答案数组。  

为什么会对？  
二进制数的十进制等价转换公式正是 `value = Σ (bit_k * 2^{len-1-k})`，而我们用 “左移 + 加位” 的方式一步步累加，等价于直接计算这个求和，所以得到的 `value` 与题目定义的 `xi` 完全相同。  

**时间/空间复杂度的大白话**  
- 时间复杂度记作 `O(n²)`，这里的 `n` 是数组长度。`O` 只是一种“数量级”记号，`n²` 表示**随着 `n` 增大，运行时间会像 `n` 的平方一样快速增长**。举个例子，`n=1000` 时，操作大约是 `1000*1000=1,000,000` 次。  
- 空间复杂度是 `O(1)`，因为我们只用常数个额外变量（不随 `n` 增长而增加）。  

#### 代码（Python）  

```python
def prefixesDivBy5_bruteforce(nums):
    """
    暴力解：每次都重新计算完整的前缀值
    :param nums: List[int] 只包含 0 或 1
    :return: List[bool] answer[i] 表示前缀 xi 是否能被 5 整除
    """
    n = len(nums)
    answer = [False] * n          # 用来存放结果
    for i in range(n):
        # 重新从 0 计算到 i 的二进制数对应的十进制值
        value = 0
        for j in range(i + 1):    # 包含第 i 位
            value = value * 2 + nums[j]   # 左移一位再加当前位
        # 判断是否能被 5 整除
        answer[i] = (value % 5 == 0)
    return answer
```

#### 复杂度  

- **时间复杂度**：`O(n²)` —— 外层循环 `n` 次，内层平均也要遍历约 `n/2` 次，总操作数约为 `n·n/2`，量级是 `n²`。  
- **空间复杂度**：`O(1)` —— 只用了几个整型变量 `value、i、j`，不随输入规模增长。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到**瓶颈**在于每次都要从头重新累加，导致二次方的时间。  
其实我们可以**利用数学的“模运算”性质**，把每一步的结果保留下来，直接在上一轮的余数基础上更新：

> 已知前缀 `X` 的十进制值对 5 的余数是 `r`（即 `X % 5 = r`），  
> 那么在后面再加一位二进制 `b`（0 或 1），新的十进制值是 `2*X + b`。  
> 对 5 取余后得到的新余数是 `(2*r + b) % 5`。

这条公式把 **“左移 + 加位”** 的操作搬到了 **余数层面**，只需要**常数时间**就能得到下一个前缀是否能被 5 整除。  

**核心概念解释**  
- **模运算（取余）**：把一个大数“压缩”到 0~(k-1) 的范围内，只保留对除数 `k` 的余数。就像把一堆糖果装进盒子，每盒装 `k` 颗，剩下的糖果数就是余数。  
- **前缀累加**：在遍历数组时，维护一个“当前的余数”变量 `rem`，每读进一个新位，就用上面的公式更新 `rem`。  

实现步骤  
1. 初始化 `rem = 0`（空前缀的余数）。  
2. 依次读取 `nums[i]`，用 `rem = (rem * 2 + nums[i]) % 5` 更新余数。  
3. 如果 `rem == 0`，说明当前前缀能被 5 整除，把 `True` 放进答案；否则放 `False`。  

这样只遍历一次数组，时间是线性的，额外空间只用来存答案和一个整型变量。

#### 代码（Python）  

```python
def prefixesDivBy5(nums):
    """
    最优解：利用模运算在遍历时维护余数
    :param nums: List[int] 只包含 0 或 1
    :return: List[bool] answer[i] 表示前缀 xi 是否能被 5 整除
    """
    answer = []          # 直接用列表的 append，空间随输出增长
    rem = 0               # 当前前缀对 5 的余数，初始为 0（空前缀）

    for bit in nums:
        # 先把已有的数左移一位（相当于乘以 2），再加上当前位
        # 再对 5 取余，得到新的余数
        rem = (rem * 2 + bit) % 5
        # 若余数为 0，说明当前前缀能被 5 整除
        answer.append(rem == 0)

    return answer
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 只遍历一次数组，每一步做常数次算术运算。相较于暴力的 `O(n²)`，运行时间随 `n` 线性增长，`n=10⁵` 也能毫秒级完成。  
- **空间复杂度**：`O(1)`（不计答案数组）—— 只用了一个整数 `rem` 和少量临时变量，额外占用的空间不随输入规模增长。  

---  

## 心得  

- **核心技巧**：利用 **模运算 + 前缀累加**，把“是否可被 k 整除”的判断压缩到余数的更新上。  
- **适用的题型**  
  1. “前缀和/前缀乘积能否被 K 整除”——如 LeetCode 1018（本题）或 1656 *"Design an Ordered Stream"* 中的类似思路。  
  2. “子数组和能否被 K 整除”——如 523 *"Continuous Subarray Sum"*，同样用前缀余数来判断。  
  3. “二进制/十进制数的可除性”——如 1018 变体 “Binary Prefix Divisible By 3”。  
- **一句话总结解题钥匙**：**把大数的除法问题转化为余数的递推**，只要记住 `(a*base + new_digit) % k = (a%k * base % k + new_digit%k) % k`。  

## 反思  

- **第一反应**：看到“二进制前缀”和“能否被 5 整除”，本能想到直接把二进制转成十进制再除以 5。  
- **最容易踩的坑**  
  - **整数溢出**：如果直接把二进制转成十进制，长度 10⁵ 位会远超 Python 的整数范围（虽然 Python 的 `int` 可任意大，但运算会很慢），导致时间爆炸。  
  - **忘记对每一步取余**：只在最后取余会失去线性时间的优势。  
  - **边界情况**：首位为 0 时，前缀值仍然是 0，需要返回 `True`（因为 0 能被任何正整数整除）。  
- **下次类似题的第一步**：先问自己 “能否用**模运算的递推公式**把每一步的结果压缩？” 如果能，就直接走递推路线；如果不行，再考虑暴力或其他技巧。