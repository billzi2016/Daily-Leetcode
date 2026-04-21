# #3602. 十六进制和三十六进制转换 / Hexadecimal and Hexatrigesimal Conversion

> 难度：简单 · 标签：Math、String · [LeetCode 链接](https://leetcode.com/problems/hexadecimal-and-hexatrigesimal-conversion/)

---

## 题目（英文原版）

**Description**

You are given an integer n.
Return the concatenation of the hexadecimal representation of n2 and the hexatrigesimal representation of n3.
A hexadecimal number is defined as a base-16 numeral system that uses the digits 0 – 9 and the uppercase letters A - F to represent values from 0 to 15.
A hexatrigesimal number is defined as a base-36 numeral system that uses the digits 0 – 9 and the uppercase letters A - Z to represent values from 0 to 35.

**Examples**

**Example 1:**

```
Input: n = 13
Output: "A91P1"
Explanation:
```

**Example 2:**

```
Input: n = 36
Output: "5101000"
Explanation:
```

**Constraints**

- 1 <= n <= 1000

---

## 题目（中文翻译）

**题目描述**  
给定一个整数 `n`。返回 `n²` 的十六进制（hexadecimal）表示 与 `n³` 的三十六进制（hexatrigesimal）表示 的拼接结果。

- 十六进制是一种基数为 16 的进制系统，使用字符 `0‑9` 和大写字母 `A‑F` 表示 `0` 到 `15` 的数值。  
- 三十六进制是一种基数为 36 的进制系统，使用字符 `0‑9` 和大写字母 `A‑Z` 表示 `0` 到 `35` 的数值。

**示例**  

```
示例 1:
Input: n = 13
Output: "A91P1"
Explanation:
```

```
示例 2:
Input: n = 36
Output: "5101000"
Explanation:
```

**约束条件**  
- `1 <= n <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是：

1. 先算出 `n²` 和 `n³`（这一步非常简单，直接 `**` 运算）。
2. 把 `n²` 转成十六进制（base‑16），把 `n³` 转成三十六进制（base‑36）。
3. 把两个字符串直接拼起来返回。

这里用到的“数据结构”只有 **字符串**。  
- **十六进制**：像我们平时写的 0‑9 加上 A‑F（A 代表 10，F 代表 15）。  
- **三十六进制**：在十六进制的基础上继续往后加上字母 G‑Z（G 代表 16，Z 代表 35）。  
可以把 **进制转换** 想象成“把数字写进不同语言的字典”。字典里每个 “词” 就是对应的字符，键是 0‑35。

Python 标准库里已经帮我们实现了十六进制的转换（`hex()`），但没有直接的三十六进制函数。**暴力解**可以直接利用 Python 的 `int` → `str` 的内置函数 `format`（`format(x, 'x')`）得到十六进制，再手写一个很短的循环把三十六进制算出来。

为什么这个方法一定能得到正确答案？

- 先算 `n²`、`n³`：数学上这两个数是唯一的，没有歧义。  
- 再把它们分别按照进制规则写出来：每一步都严格遵守“除以基数取余数”的规则，余数对应的字符一定是唯一的。  
- 最后把两段字符连在一起：题目要求的就是这两个字符串的直接拼接。

**复杂度分析（大白话）**  
- 计算 `n²`、`n³` 是 O(1)（因为 `n ≤ 1000`，算数运算时间几乎可以忽略）。  
- 十六进制转换的循环次数大约是 `log₁₆(n²)`，即 **数字位数**，最多 5~6 次。  
- 三十六进制转换的循环次数大约是 `log₃₆(n³)`，同理也很少。  
整体时间复杂度是 **O(log n)**，空间只用来存放结果字符串，大小也是 **O(log n)**。

#### 代码（Python）

```python
def to_base(num: int, base: int) -> str:
    """
    把正整数 num 转成指定进制 base（2 <= base <= 36）的字符串。
    采用“除基取余”法：不断除以 base，余数对应字符，倒序拼接。
    """
    if num == 0:
        return "0"
    digits = []                     # 用列表收集每一位字符，最后再逆序合并
    while num > 0:
        rem = num % base             # 余数 0~35
        # 把余数映射成字符：0-9 -> '0'-'9'，10-35 -> 'A'-'Z'
        if rem < 10:
            ch = chr(ord('0') + rem)
        else:
            ch = chr(ord('A') + rem - 10)
        digits.append(ch)            # 低位先放进列表
        num //= base                 # 去掉已经转换的低位
    # 逆序得到正确的高位到低位顺序
    return ''.join(reversed(digits))

def concatenated_representation(n: int) -> str:
    # 1. 计算 n²、n³
    square = n * n
    cube = n * n * n

    # 2. 十六进制（base=16） + 三十六进制（base=36）
    hex_part = to_base(square, 16)   # 这里得到的字符已经是大写
    base36_part = to_base(cube, 36)

    # 3. 直接拼接返回
    return hex_part + base36_part

# ----------------- 测试 -----------------
print(concatenated_representation(13))   # -> "A91P1"
print(concatenated_representation(36))   # -> "5101000"
```

#### 复杂度

- **时间复杂度**：`O(log₁₆(n²) + log₃₆(n³))`，即 **O(log n)**。  
  这里的 `log` 代表“位数”，比如十进制的 1000 只有 4 位，十六进制和三十六进制更少位，所以运行非常快。  
- **空间复杂度**：`O(log n)`，因为我们用列表保存每一位字符，最多也只会存几位。

---

### 2. 最优解

#### 思路  

暴力解已经非常高效（只用了几次循环），在本题的约束下已经是 **最优** 的时间表现。  
这里的 “最优解” 其实是 **把进制转换抽象成通用函数**，使代码结构更清晰、可复用，并且彻底避免使用任何语言自带的进制函数（有的语言没有直接的 36 进制），从而在所有编程语言里都能保持同样的复杂度。

从暴力解出发的优化点：

1. **统一的进制转换函数**  
   - 只写一次 `to_base`，既能处理十六进制也能处理三十六进制。这样代码重复率降到最低，阅读时更容易抓住核心逻辑。  
2. **避免不必要的字符串拼接**  
   - 使用列表收集字符后一次性 `join`，而不是每次都 `+`，可以省去 Python 中的临时字符串创建（虽然这里规模小，影响不大，但是良好习惯）。  

核心算法仍然是 **“除基取余”**，下面把它从零解释一下：

- 把一个十进制整数 `x` 看成 **若干个基 `b` 的位**。  
- 先把 `x` 除以 `b`，余数就是最低位（类似我们写十进制数时最右边的那一位）。  
- 再把商继续除以 `b`，得到次低位，以此类推，直到商为 0。  
- 余数的顺序是 **从低位到高位**，所以最后要把收集到的字符逆序（`reversed`）才能得到正确的读法。

可以把这个过程类比为 **把大块的糖果分装进不同容量的盒子**：先装最小的盒子（余数），剩下的再装更大的盒子（商），最后把装好的盒子从大到小排好顺序。

#### 代码（Python）

```python
def to_base(num: int, base: int) -> str:
    """通用进制转换（2~36），返回大写字符的表示。"""
    if num == 0:
        return "0"
    # 预先准备好 0-9 + A-Z 的映射表，直接索引即可
    symbols = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    res = []                     # 用列表收集字符
    while num:
        num, rem = divmod(num, base)   # 同时得到商和余数，语义更清晰
        res.append(symbols[rem])       # 余数对应的字符直接取
    return ''.join(reversed(res))

def concatenated_representation(n: int) -> str:
    """返回 n² 的十六进制 + n³ 的三十六进制（均为大写）。"""
    return to_base(n * n, 16) + to_base(n * n * n, 36)

# ----------------- 示例 -----------------
print(concatenated_representation(13))   # "A91P1"
print(concatenated_representation(36))   # "5101000"
```

#### 复杂度

- **时间复杂度**：`O(log₁₆(n²) + log₃₆(n³)) = O(log n)`。  
  与暴力解完全相同，只是常数因子更小（一次 `divmod` 替代两次取模/整除），在极端大数时会稍微快一点。  
- **空间复杂度**：`O(log n)`，因为只保存每一位字符的列表。

---

## 心得

- **核心技巧**：**除基取余的进制转换**（把任意十进制整数写成任意 2~36 进制的字符串）。  
- **适用场景**：  
  1. 把十进制整数转换成二进制、八进制、十六进制等常见进制（如 “整数转二进制”）。  
  2. “把数字表示成字母序列” 的题目，如把 0‑35 映射到 `0-9A-Z`（常见的 URL 短链编码）。  
  3. 需要自定义进制的场景，例如 “把十进制时间转成自定义基数的计时器”。  
- **一句话总结解题钥匙**：**“除基取余 + 逆序拼接”** 就能把任何正整数转成任意 2~36 进制的字符串。

---

## 反思

- **第一反应**：直接想到先算 `n²`、`n³`，然后用已有的进制转换函数（或手写）分别得到十六进制和三十六进制，最后拼接。  
- **最容易踩的坑**：  
  - 忘记把三十六进制的字母映射到 **大写**（题目要求大写）。  
  - `num == 0` 时直接返回空字符串，会导致结果缺少 “0”。  
  - 在手动拼接时使用 `+` 逐字符相加，会产生额外的时间开销（虽然本题规模不大，但养成好习惯很重要）。  
- **下次类似题的第一步**：先把 “把整数写成某进制” 这一步抽象成函数 `to_base(x, b)`，确认它在所有需要的进制上都能正常工作，再去处理题目要求的拼接或其他后处理。