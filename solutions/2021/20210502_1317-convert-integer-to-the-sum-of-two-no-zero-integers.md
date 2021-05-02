# #1317. 将整数拆分为两个无零整数的和 / Convert Integer to the Sum of Two No-Zero Integers

> 难度：简单 · 标签：Math · [LeetCode 链接](https://leetcode.com/problems/convert-integer-to-the-sum-of-two-no-zero-integers/)

---

## 题目（英文原版）

**Description**

No-Zero integer is a positive integer that does not contain any 0 in its decimal representation.
Given an integer n, return a list of two integers [a, b] where:
The test cases are generated so that there is at least one valid solution. If there are many valid solutions, you can return any of them.

**Examples**

**Example 1:**

```
Input: n = 2
Output: [1,1]
Explanation: Let a = 1 and b = 1.
Both a and b are no-zero integers, and a + b = 2 = n.
```

**Example 2:**

```
Input: n = 11
Output: [2,9]
Explanation: Let a = 2 and b = 9.
Both a and b are no-zero integers, and a + b = 11 = n.
Note that there are other valid answers as [8, 3] that can be accepted.
```

**Constraints**

- 2 <= n <= 104

---

## 题目（中文翻译）

**描述**  
无零整数（No-Zero integer）是指十进制表示中不包含数字 0 的正整数。  
给定一个整数 `n`，返回一个包含两个整数 `[a, b]` 的列表，使得：

- `a` 和 `b` 均为无零整数；
- `a + b = n`。

题目保证至少存在一个满足条件的解。若存在多个合法解，返回任意一个即可。

**示例 1**  
**输入**: `n = 2`  
**输出**: `[1,1]`  
**解释**: 设 `a = 1`，`b = 1`。  
`a` 与 `b` 均为无零整数，且 `a + b = 2 = n`。

**示例 2**  
**输入**: `n = 11`  
**输出**: `[2,9]`  
**解释**: 设 `a = 2`，`b = 9`。  
`a` 与 `b` 均为无零整数，且 `a + b = 11 = n`。  
注意，`[8,3]` 等其他合法答案也会被接受。

**约束条件**  
- `2 <= n <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：  
从 **1** 开始枚举所有可能的 `a`，把剩下的 `b` 设为 `n - a`。  
只要 `a` 与 `b` 都不含数字 **0**，就找到了答案。  

- **数据结构**：这里只需要两个整数 `a`、`b`，以及一个判断“是否含 0”的小函数。  
  判断是否含 0 可以把整数转换成字符串，再逐字符检查。  
  这有点像我们平时查字典：把数字变成“单词”，看里面有没有“0”这页码。  

- **为什么一定能找到**：题目已经保证至少有一个合法答案，所以只要遍历完整个 `[1, n‑1]` 的区间，就一定会碰到满足条件的 `(a, b)`。

- **时间/空间复杂度**：  
  - 最坏情况下我们要检查所有 `i = 1 … n‑1`，每次检查要把整数转成字符串（长度至多 5，因为 `n ≤ 10⁴`），所以时间是 **O(n·d)**，这里的 `d` 是数字位数，最多是 5，故可以简化为 **O(n)**。  
  - 只用了常数级别的额外空间（存放 `a、b` 和临时字符串），所以空间是 **O(1)**。  
  - 大白话：如果 `n = 10000`，我们最多循环一万次，每次只做几次字符比较，算得上“快”。  

#### 代码（Python）

```python
def no_zero(x: int) -> bool:
    """
    判断整数 x 的十进制表示中是否不包含数字 0
    把整数转成字符串后逐字符检查
    """
    return '0' not in str(x)   # 若字符串里没有 '0'，返回 True

def get_no_zero_sum_brute(n: int) -> list[int]:
    """
    暴力枚举 a，从 1 到 n-1，找出满足条件的 (a, b)
    """
    for a in range(1, n):                # a 可能的取值
        b = n - a                         # b 必须等于 n - a
        if no_zero(a) and no_zero(b):    # 同时检查 a、b 是否都是 No‑Zero
            return [a, b]                # 找到后直接返回
    # 题目保证一定有解，这行理论上不会执行
    return []
```

#### 复杂度

- **时间复杂度**：**O(n)**  
  解释：我们最多遍历 `n‑1` 次，每次只做一次字符串检查（常数时间），所以整体随 `n` 线性增长。  
- **空间复杂度**：**O(1)**  
  解释：只用了几个整数变量和一条临时字符串，不会随 `n` 增大而增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **线性遍历**：即使 `n` 很大（这里最高 10⁴），我们仍然要尝试很多次。  
其实我们可以直接 **构造** 出满足条件的 `(a, b)`，不需要遍历。

构造思路来源于**逐位拆分**：

1. 把 `n` 看成十进制的每一位，例如 `n = 5083` → `[5,0,8,3]`（从高位到低位）。  
2. 对每一位 `d`，我们希望把它拆成 `a_digit + b_digit = d`，并且 `a_digit`、`b_digit` 都在 **1~9**（不能为 0）。  
3. 当 `d != 0` 时，最简单的拆法是 `a_digit = 1`，`b_digit = d-1`。两者都不是 0。  
4. 当 `d == 0` 时，直接拆不到非零数，需要向更高一位 **借 1**（相当于十进制减法的“借位”），把当前位视作 `10`：  
   - 设 `a_digit = 1`，`b_digit = 9`（因为 `1 + 9 = 10`），并把前一位的值减 1。  
   - 这样做会把原本的 `0` 位变成 `10`，再拆成 `1` 与 `9`，满足不含 0。  

按照上述规则从高位到低位依次处理，最终得到两个只含 1~9 的整数 `a`、`b`。  
因为每一位只做常数次操作，时间只跟 **位数** 成正比（`len(str(n))`），在本题最多 5 位，几乎是 O(1) 的表现。

#### 代码（Python）

```python
def get_no_zero_sum_optimal(n: int) -> list[int]:
    """
    逐位构造 a、b，使得 a + b = n 且两数均不含 0。
    思路：从高位到低位拆分，每位保证 a_digit、b_digit ∈ [1,9]。
    """
    digits = list(map(int, str(n)))   # 将 n 的每一位拆成列表，例如 5083 → [5,0,8,3]
    a_digits = []                     # 用来保存 a 的每一位
    b_digits = []                     # 用来保存 b 的每一位

    # 从左（高位）到右（低位）遍历
    for i, d in enumerate(digits):
        if d != 0:                     # 当前位不是 0，直接拆成 1 与 d-1
            a_digits.append(1)
            b_digits.append(d - 1)
        else:                          # 当前位是 0，需要向左边借位
            # 向前一位借 1（十进制的借位相当于把当前位视作 10）
            # 因为左边一定有位（题目保证有解），我们直接在 digits 中减 1
            j = i - 1
            while j >= 0 and digits[j] == 0:   # 找到第一个非零的高位
                j -= 1
            digits[j] -= 1                     # 借位：高位减 1
            # 当前位视为 10，拆成 1 与 9
            a_digits.append(1)
            b_digits.append(9)

    # 把每位数字合成整数
    a = int(''.join(map(str, a_digits)))
    b = int(''.join(map(str, b_digits)))
    return [a, b]
```

> **代码要点说明**  
> - `digits` 保存原始的十进制位，后面可能会被修改（借位时把左侧位减 1）。  
> - 当遇到 `0` 时，我们向左寻找最近的非零位进行借位，这一步类似手算减法的“向左借”。  
> - 最后把 `a_digits`、`b_digits` 通过 `join` 合成字符串，再转成整数即可。

#### 复杂度

- **时间复杂度**：**O(k)**，其中 `k` 是 `n` 的十进制位数（`k ≤ 5`）。  
  解释：我们只遍历每一位一次，借位最多也只会再向左走几步，整体随位数线性增长。相对于暴力的 `O(n)`，这里几乎是常数时间。  
- **空间复杂度**：**O(k)** 用于存放 `a_digits`、`b_digits`，同样是位数级别的额外空间。  
  解释：不随 `n` 的大小指数增长，最多几位。

---

## 心得

- **核心技巧**：**逐位拆分 + 借位**——把整数按十进制位拆开，确保每位的拆分结果都不为 0。  
- **适用的题型**：  
  1. “把数字拆成满足某种位约束的两数”——如 *Split a Number Into Two Non‑Zero Parts*。  
  2. “不含特定数字的构造”——如 *No‑Zero Integer*、*No‑Zero Product*。  
  3. “位运算或进位/借位的模拟”——如 *Additive Persistence*、*Digit DP* 的入门题。  
- **一句话总结**：**只要把每一位都拆成 1 与 (digit‑1)（或 1 与 9 并借位），就能一次性得到合法答案**。

---

## 反思

- **第一反应**：看到“把 n 拆成两数，且两数都不能有 0”，立刻想到 **枚举**，因为最直接的办法就是遍历。  
- **最容易踩的坑**：  
  - 忽略 **0** 位的特殊处理，直接把 `0` 拆成 `1` 与 `-1` 会出错。  
  - 边界情况：`n` 本身可能只有一位（如 `n=2`），此时不需要借位。  
  - 当借位时，左侧位可能已经是 `0`，需要继续向更左找非零位。  
- **下次遇到同类题**，第一步应该先 **思考能否逐位构造**，而不是直接暴力枚举；如果位数不大，优先尝试 **位拆分 + 借位** 的思路。