# #8. 字符串转整数 (atoi) / String to Integer (atoi)

> 难度：中等 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/string-to-integer-atoi/)

---

## 题目（英文原版）

**Description**

Implement the myAtoi(string s) function, which converts a string to a 32-bit signed integer.
The algorithm for myAtoi(string s) is as follows:
Return the integer as the final result.

**Examples**

**Example 1:**

```
The underlined characters are what is read in and the caret is the current reader position.
Step 1: "42" (no characters read because there is no leading whitespace)
         ^
Step 2: "42" (no characters read because there is neither a '-' nor '+')
         ^
Step 3: "42" ("42" is read in)
           ^
```

**Example 2:**

```
Step 1: "   -042" (leading whitespace is read and ignored)
            ^
Step 2: "   -042" ('-' is read, so the result should be negative)
             ^
Step 3: "   -042" ("042" is read in, leading zeros ignored in the result)
               ^
```

**Example 3:**

```
Step 1: "1337c0d3" (no characters read because there is no leading whitespace)
         ^
Step 2: "1337c0d3" (no characters read because there is neither a '-' nor '+')
         ^
Step 3: "1337c0d3" ("1337" is read in; reading stops because the next character is a non-digit)
             ^
```

**Example 4:**

```
Step 1: "0-1" (no characters read because there is no leading whitespace)
         ^
Step 2: "0-1" (no characters read because there is neither a '-' nor '+')
         ^
Step 3: "0-1" ("0" is read in; reading stops because the next character is a non-digit)
          ^
```

**Constraints**

- 0 <= s.length <= 200
- s consists of English letters (lower-case and upper-case), digits (0-9), ' ', '+', '-', and '.'.

---

## 题目（中文翻译）

实现 `myAtoi(string s)` 函数，将字符串转换为 **32 位带符号整数**（32-bit signed integer）。  
转换过程遵循以下步骤：

1. **去除前导空格**（whitespace）。  
2. 读取可选的正负号（'+' 或 '-'），确定结果的符号。  
3. 读取连续的数字字符，将其转换为整数；读取过程遇到非数字字符即停止。  
4. 若得到的整数超出 **32 位有符号整数** 的取值范围 \[−2³¹, 2³¹ − 1\]，则返回边界值 `INT_MIN = -2³¹` 或 `INT_MAX = 2³¹ − 1`。  
5. 返回最终得到的整数。

**返回值** 为转换后的整数。

## 示例

### 示例 1
**输入:** `"42"`  
**输出:** `42`  
**解释:**  
- 第一步: `"42"`（没有读取任何字符，因为没有前导空格）  
  `^`  
- 第二步: `"42"`（没有读取任何字符，因为既没有 '-' 也没有 '+'）  
  `^`  
- 第三步: `"42"`（读取了 `"42"`）  
  `^`

### 示例 2
**输入:** `"   -042"`  
**输出:** `-42`  
**解释:**  
- 第一步: `"   -042"`（读取并忽略前导空格）  
  `^`  
- 第二步: `"   -042"`（读取到 '-'，因此结果应为负数）  
  `^`  
- 第三步: `"   -042"`（读取 `"042"`，结果中忽略前导零）  
  `^`

### 示例 3
**输入:** `"1337c0d3"`  
**输出:** `1337`  
**解释:**  
- 第一步: `"1337c0d3"`（没有读取任何字符，因为没有前导空格）  
  `^`  
- 第二步: `"1337c0d3"`（没有读取任何字符，因为既没有 '-' 也没有 '+'）  
  `^`  
- 第三步: `"1337c0d3"`（读取了 `"1337"`，随后遇到非数字字符停止读取）  
  `^`

### 示例 4
**输入:** `"0-1"`  
**输出:** `0`  
**解释:**  
- 第一步: `"0-1"`（没有读取任何字符，因为没有前导空格）  
  `^`  
- 第二步: `"0-1"`（没有读取任何字符，因为既没有 '-' 也没有 '+'）  
  `^`  
- 第三步: `"0-1"`（读取了 `"0"`，随后遇到非数字字符停止读取）  
  `^`

### 示例 5
**输入:** `"-91283472332"`  
**输出:** `-2147483648`  
**解释:** 读取的数字超过了 32 位有符号整数的下界，返回 `INT_MIN = -2³¹`。

## 约束条件
- `0 <= s.length <= 200`
- `s` 仅由英文字母（大小写）、数字（0-9）、空格 `' '`、符号 `'+'`、`'-'` 和点 `'.'` 组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把字符串 **完整地** 交给 Python 的 `int()` 函数，让它帮我们完成所有的工作。  
实现步骤可以概括为：

1. **去掉前导空格**：`str.strip()` 把左边的空格删掉，和我们在纸上“跳过空格”是同一个动作。  
2. **截取合法的子串**：从第一个出现的 `+`、`-` 或数字开始，一直往后读，直到遇到第一个非数字字符为止。  
3. **交给 `int()`**：把这段只包含符号和数字的子串直接转成整数。  
4. **判断 32 位有符号整数范围**：如果结果小于 `-2**31`，返回 `-2**31`；如果大于 `2**31-1`，返回 `2**31-1`。

这里使用的 **数据结构** 只有最基本的 **字符串**，不需要额外的容器。  
把 `int()` 想象成一本 **查字典** 的工具，键（key）是我们截取的数字字符串，返回值（value）就是对应的整数。

> **为什么这个方法正确？**  
> - 题目规定只要把合法的数字子串转成整数，超出范围就截断到上下限。`int()` 正好完成了“合法子串 → 整数”的映射。  
> - 只要我们正确截取子串，后面的处理就是数学上的比较，必然得到符合题意的答案。

> **时间/空间复杂度**  
> - **时间**：我们要遍历一次字符串来找出合法子串，最坏情况是整个字符串都要看一遍，记作 **O(n)**（n 为字符串长度）。这里的 `O(n)` 就是“线性增长”，比如长度是 10 时需要 10 步，长度是 100 时需要 100 步。  
> - **空间**：只额外保存了几个指针和一个子串（子串本身是原字符串的一段视图，Python 不会额外拷贝），所以是 **O(1)**（常数级别的空间）。

#### 代码（Python）

```python
def myAtoi(s: str) -> int:
    # 1. 去掉左侧空格
    s = s.lstrip()                     # lstrip() 只删左边的空格

    if not s:                          # 空字符串直接返回 0
        return 0

    # 2. 记录符号位，默认正数
    sign = 1
    idx = 0
    if s[0] == '+':                    # 正号直接跳过
        idx = 1
    elif s[0] == '-':                  # 负号记住并跳过
        sign = -1
        idx = 1

    # 3. 读取连续的数字字符，遇到非数字就停
    num_str = []
    while idx < len(s) and s[idx].isdigit():
        num_str.append(s[idx])
        idx += 1

    if not num_str:                    # 没有数字直接返回 0
        return 0

    # 4. 把数字字符列表转成字符串，再交给 int()
    num = int(''.join(num_str)) * sign

    # 5. 处理 32 位有符号整数的上下界
    INT_MIN, INT_MAX = -2**31, 2**31 - 1
    if num < INT_MIN:
        return INT_MIN
    if num > INT_MAX:
        return INT_MAX
    return num
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历了一遍字符串，长度翻倍就多走两步。  
- **空间复杂度**：`O(1)` — 只用了常数个变量（`sign、idx、num_str` 的列表最多也只会存放 `n` 个字符，但在最坏情况下它相当于原字符串的一个视图，整体算作常数额外空间）。

---

### 2. 最优解

#### 思路  

暴力解已经是 **线性时间**，已经是最快的时间复杂度了。不过它仍然有几个可以改进的地方：

| 暴力解的“慢点” | 为什么需要改进 |
|----------------|----------------|
| 使用 `int()` 进行一次性转换 | `int()` 会把完整的数字一次性转成大整数，若数字非常长（比如 100 位），Python 仍会生成一个巨大的整数再去比较上下限，这会带来 **额外的时间和空间开销**。|
| 先把所有数字收集到列表再 `''.join()` | 产生了临时的列表对象，稍微占用一点内存。|

**最优思路**：在遍历字符的同时 **逐位** 构造整数，并在每一步 **提前检查是否会溢出**。这样可以：

1. **不产生中间的大整数**：每读进一位，就把当前结果 `res = res * 10 + digit`。如果 `res` 已经接近上限，再乘 10 会导致溢出，我们可以提前判断。  
2. **省去额外容器**：直接用整数变量 `res` 累加，不需要列表或字符串拼接。

**核心技巧**——**“在循环中检测溢出”**。  
设 `INT_MAX = 2**31 - 1`，`INT_MIN = -2**31`。在读取下一个数字 `d` 前，若 `res > INT_MAX // 10`，则 `res * 10` 已经超过上限；若 `res == INT_MAX // 10` 且 `d > INT_MAX % 10`，则 `res * 10 + d` 仍会超过上限。此时直接返回上限（或下限）即可。

下面把整个过程用 **状态机**（有限自动机）来描述，帮助大家把思路系统化：

1. **状态 S0（起始）**：跳过所有空格。  
2. **状态 S1（符号）**：读取可选的 `+` 或 `-`，记录符号。  
3. **状态 S2（数字）**：只要后面是数字，就进入此状态，逐位累加结果并检测溢出。  
4. **状态 S3（结束）**：一旦遇到非数字字符或遍历完字符串，返回结果（并加上符号）。

> **类比**：想象我们在超市结账，每买一个商品（读进一位数字），都把它的价钱加到购物车里（`res = res*10 + d`），如果购物车的总价已经快到信用卡额度（`INT_MAX`）了，我们会提前提示“超额”，而不是等到全部商品都放进去后才发现。

#### 代码（Python）

```python
def myAtoi(s: str) -> int:
    INT_MAX, INT_MIN = 2**31 - 1, -2**31

    i, n = 0, len(s)

    # S0: 跳过前导空格
    while i < n and s[i] == ' ':
        i += 1

    # 如果全是空格直接返回 0
    if i == n:
        return 0

    # S1: 读取符号
    sign = 1
    if s[i] == '+':
        i += 1
    elif s[i] == '-':
        sign = -1
        i += 1

    # S2: 读取数字并实时检测溢出
    res = 0
    while i < n and s[i].isdigit():
        digit = int(s[i])

        # 检查是否会在下一个步骤溢出
        if res > INT_MAX // 10 or (res == INT_MAX // 10 and digit > INT_MAX % 10):
            # 根据符号返回对应的上下界
            return INT_MAX if sign == 1 else INT_MIN

        # 没有溢出，安全累加
        res = res * 10 + digit
        i += 1

    return sign * res
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历一次字符串，且每一步都是常数时间操作。相比暴力解省去 `int()` 产生大整数的额外成本。  
- **空间复杂度**：`O(1)` — 只用了几个整数变量（`i、sign、res、digit`），不依赖额外的容器。

---

## 心得

- **核心技巧**：在遍历字符串时**逐位构造整数并即时检测溢出**。  
- **适用的题型**：  
  1. **字符串转数值**（如 `atoi`、`strtod`）。  
  2. **手写大数乘法/加法**（需要逐位运算并检测进位）。  
  3. **解析表达式的数值部分**（如中缀表达式求值的数字读取）。
- **一句话总结解题钥匙**：**“边读边算，提前把越界拦在门口”。**

---

## 反思

- **拿到题目第一反应**：先把字符串清理干净，直接交给 Python 的 `int()`，因为我知道它可以把合法的数字串变成整数。  
- **最容易踩的坑**：  
  - 忽略了 **前导空格**、**符号**、以及 **非数字字符的提前终止**。  
  - 没有考虑 **整数溢出**，直接返回大整数会导致答案错误。  
  - 对空字符串或只包含符号的情况返回了错误值。  
- **下次遇到同类题**，第一步应该想到：**“先把合法的数字子串逐位提取出来，同时在提取过程中就判断是否会越界”。**这样既能一次遍历完成，又能避免额外的大整数计算。