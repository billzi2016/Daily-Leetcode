# #1881. 插入后最大值 / Maximum Value after Insertion

> 难度：中等 · 标签：String、Greedy · [LeetCode 链接](https://leetcode.com/problems/maximum-value-after-insertion/)

---

## 题目（英文原版）

**Description**

You are given a very large integer n, represented as a string,​​​​​​ and an integer digit x. The digits in n and the digit x are in the inclusive range [1, 9], and n may represent a negative number.
You want to maximize n's numerical value by inserting x anywhere in the decimal representation of n​​​​​​. You cannot insert x to the left of the negative sign.
Return a string representing the maximum value of n​​​​​​ after the insertion.

**Examples**

**Example 1:**

```
Input: n = "99", x = 9
Output: "999"
Explanation: The result is the same regardless of where you insert 9.
```

**Example 2:**

```
Input: n = "-13", x = 2
Output: "-123"
Explanation: You can make n one of {-213, -123, -132}, and the largest of those three is -123.
```

**Constraints**

- 1 <= n.length <= 105
- 1 <= x <= 9
- The digits in n​​​ are in the range [1, 9].
- n is a valid representation of an integer.
- In the case of a negative n,​​​​​​ it will begin with '-'.

---

## 题目（中文翻译）

你得到一个非常大的整数 `n`，以字符串（string）形式给出，以及一个整数位 `x`。`n` 中的每个数字以及 `x` 都在闭区间 `[1, 9]` 内，`n` 可能表示负数。  
你希望通过在 `n` 的十进制表示的任意位置插入 `x` 来使 `n` 的数值最大化。**不能**把 `x` 插入到负号左侧。  
返回一个字符串，表示插入 `x` 之后 `n` 的最大值。

## 示例

### 示例 1
**输入**: `n = "99", x = 9`  
**输出**: `"999"`  
**解释**: 无论把 `9` 插入到哪里，结果都是相同的。

### 示例 2
**输入**: `n = "-13", x = 2`  
**输出**: `"-123"`  
**解释**: 你可以得到 `{-213, -123, -132}` 三种可能，最大的是 `-123`。

## 约束条件
- `1 <= n.length <= 10^5`
- `1 <= x <= 9`
- `n` 中的每个数字都在 `[1, 9]` 区间内
- `n` 是一个合法的整数表示
- 若 `n` 为负数，则以字符 `'-'` 开头

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把数字 **x** 插入到原字符串 **n** 的每一个可能位置，然后把得到的所有新字符串转成整数比较大小，选出最大的那个。

- **数据结构**：只需要 Python 的 `str`（字符串）和 `int`（整数）。  
  - 把字符串看成一本书的页码，**插入** 就像在书的任意页前面加上一页新内容。  
  - 把字符串转成整数相当于把这本书“翻开”读出它的数值。

- **正确性**：因为我们枚举了**所有**合法的插入位置（包括最左、最右），所以必然能找到最大值。

- **时间/空间复杂度**：  
  - 字符串长度记作 `n`（`1 ≤ n ≤ 10⁵`）。  
  - 插入位置有 `n+1` 种，每一次我们要生成一个新字符串（`O(n)`）并把它转成整数再比较（`O(n)`），所以总体是 `O((n+1)·n) = O(n²)`。  
  - 这里的 `O(n²)` 并不是“平方”本身的意思，而是说随着输入长度的增长，运行时间会以 **长度的平方** 增长。  
  - 只用了常数级的额外空间（存几个临时字符串），因此空间复杂度是 `O(1)`（不计输入本身）。

#### 代码（Python）

```python
def maxValue_bruteforce(n: str, x: int) -> str:
    """
    暴力枚举所有插入位置，返回数值最大的结果。
    """
    best = None          # 用来保存当前最大的字符串
    x_char = str(x)      # 把数字 x 转成字符，方便拼接

    # i 表示在原字符串的第 i 位之前插入 x，i 范围是 0~len(n)
    for i in range(len(n) + 1):
        # 负数的情况：不能把 x 插到负号左边
        if n[0] == '-' and i == 0:
            continue

        cand = n[:i] + x_char + n[i:]   # 生成候选字符串

        # 用整数比较大小（Python 能直接处理大整数）
        if best is None or int(cand) > int(best):
            best = cand

    return best
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 需要遍历 `n+1` 个位置，每次操作都要遍历一次字符串（`O(n)`）来生成和比较。
- **空间复杂度**：`O(1)` —— 只用了常数级的临时变量（不计输入 `n` 本身）。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都要完整遍历字符串**来生成候选答案。其实我们只需要一次线性扫描就能决定**最佳的插入位置**，关键在于正负号的不同处理：

1. **正数**（`n` 不以 `-` 开头）  
   - 目标是让数值**最大**。  
   - 当我们在某一位 `s[i]` 前插入 `x` 时，如果 `x` 比 `s[i]` **大**，则新数会在这一位起变得更大，后面的位数保持不变，从而整体更大。  
   - 因此，**第一次出现 `s[i] < x` 的位置**就是最佳插入点；如果全程都没有出现，则把 `x` 放在最右侧（末尾）。

2. **负数**（`n` 以 `-` 开头）  
   - 负数的数值大小和它的**绝对值**呈相反关系：绝对值越小，数值越大（比如 `-5 > -9`）。  
   - 为了让负数尽可能大，我们要让它的 **绝对值尽可能小**。这等价于在正数情况下**寻找最小**的数值。  
   - 当在某位 `s[i]` 前插入 `x` 时，如果 `x` **小于** `s[i]`，绝对值会变小，数值会变大。但在负数里我们需要的是**`s[i] > x`**（即 `x` 更小）时插入。  
   - 所以，**第一次出现 `s[i] > x` 的位置**（从左到右）就是最佳插入点；若全程没有出现，则把 `x` 放在末尾。

> **类比**：把正数看成一列递增的楼层，想让电梯尽快升到更高层，就把更大的按钮（`x`）提前按下；负数则像倒挂的楼层，想让电梯尽量不往下掉，就把更小的按钮提前按下。

#### 代码（Python）

```python
def maxValue_greedy(n: str, x: int) -> str:
    """
    贪心一次扫描决定插入位置，时间 O(n)，空间 O(1)。
    """
    x_char = str(x)

    # 处理正数
    if n[0] != '-':
        for i, ch in enumerate(n):
            # 找到第一个比当前位小的地方，直接在前面插入
            if ch < x_char:
                return n[:i] + x_char + n[i:]
        # 若全程没有更小的位，则把 x 放在末尾
        return n + x_char

    # 处理负数（首字符是 '-')
    # 从第二个字符开始检查（因为不能在负号左边插入）
    for i in range(1, len(n)):
        if n[i] > x_char:          # 这里寻找“大于 x”的位置
            return n[:i] + x_char + n[i:]
    # 若没有找到合适位置，直接在末尾插入
    return n + x_char
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历一次字符串，找出插入点后直接拼接返回。相较于暴力的 `O(n²)`，当 `n` 很大（比如 10⁵）时速度提升了 **数百倍**。
- **空间复杂度**：`O(1)` —— 只用了常数个临时变量（`x_char`、索引 `i`），不随输入规模增长。

---

## 心得

- **核心技巧**：**贪心**——在满足局部最优条件（正数找第一个比 `x` 小的位，负数找第一个比 `x` 大的位）时，即可保证全局最优。
- **适用的题型**  
  1. “在字符串/数组中插入/删除元素，使结果最大/最小” 类的题目（如 “Maximum Number after Digit Insertion”）。  
  2. “构造字典序最小（大）字符串” 的问题（如 “最小字典序子序列”）。  
  3. “单调栈/单调队列” 相关的单调性贪心题（如 “最小/最大子数组乘积”）。
- **一句话总结解题钥匙**：**正数把更大的数往左插，负数把更小的数往左插**。

---

## 反思

- **第一反应**：直接想到“把 x 放到每个位置试试看”，于是写出了暴力解。  
- **最容易踩的坑**  
  - 忘记 **负号** 的特殊限制——不能把 `x` 插到负号左边。  
  - 对负数的比较方向搞反了：在负数中要让数值更大，需要让 **绝对值更小**，所以插入条件是 `s[i] > x`（而不是 `s[i] < x`）。  
  - 边界情况：全部位都不满足条件时，需要把 `x` 放在末尾。  
- **下次类似题目第一步**：先判断**正负号**或整体的**单调方向**，明确“更大/更小”对应的局部比较规则，再用一次线性扫描找到插入点。这样可以立刻从暴力转向贪心。