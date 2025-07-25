# #3280. 将日期转换为二进制 / Convert Date to Binary

> 难度：简单 · 标签：Math、String · [LeetCode 链接](https://leetcode.com/problems/convert-date-to-binary/)

---

## 题目（英文原版）

**Description**

You are given a string date representing a Gregorian calendar date in the yyyy-mm-dd format.
date can be written in its binary representation obtained by converting year, month, and day to their binary representations without any leading zeroes and writing them down in year-month-day format.
Return the binary representation of date.

**Examples**

**Example 1:**

```
Input: date = "2080-02-29"
Output: "100000100000-10-11101"
Explanation:
100000100000, 10, and 11101 are the binary representations of 2080, 02, and 29 respectively.
```

**Example 2:**

```
Input: date = "1900-01-01"
Output: "11101101100-1-1"
Explanation:
11101101100, 1, and 1 are the binary representations of 1900, 1, and 1 respectively.
```

**Constraints**

- date.length == 10
- date[4] == date[7] == '-', and all other date[i]'s are digits.
- The input is generated such that date represents a valid Gregorian calendar date between Jan 1st, 1900 and Dec 31st, 2100 (both inclusive).

---

## 题目（中文翻译）

你得到一个字符串 `date`，表示 Gregorian calendar（公历）日期，格式为 `yyyy-mm-dd`。  
可以将 `date` 转换为二进制表示：将年份、月份和日期分别转换为它们的二进制（binary）形式，**不保留前导零**，然后按 `year-month-day` 的顺序用 `-` 连接起来。  
返回该二进制表示的字符串。

**示例 1**  
**输入**  
```text
date = "2080-02-29"
```  
**输出**  
```text
"100000100000-10-11101"
```  
**解释**  
`100000100000`、`10` 和 `11101` 分别是 2080、02、29 的二进制表示。

**示例 2**  
**输入**  
```text
date = "1900-01-01"
```  
**输出**  
```text
"11101101100-1-1"
```  
**解释**  
`11101101100`、`1` 和 `1` 分别是 1900、1、1 的二进制表示。

**约束条件**

- `date.length == 10`
- `date[4] == date[7] == '-'`，其余位置均为数字字符。
- 输入保证 `date` 是合法的 Gregorian calendar（公历）日期，范围在 1900 年 1 月 1 日至 2100 年 12 月 31 日（含）。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法就是把 `"yyyy-mm-dd"` 按照 `-` 分成三段：年、月、日。  
随后把每一段的十进制数字转换成二进制字符串。  

- **把字符串切成三块**：就像把一本书按照章节标题分开阅读，`split('-')` 能一次性帮我们完成。  
- **十进制 → 二进制**：Python 自带的 `bin()` 函数相当于一个「进制转换机器」，把整数 `x` 变成形如 `"0b1010"` 的字符串。我们只要去掉开头的 `"0b"`，剩下的就是纯二进制。  
- **重新拼接**：把三个二进制块用 `-` 再连起来，就是答案。

这个办法一定能得到正确答案，因为题目只要求把每个数单独转成二进制，不涉及进位或进制之间的混合运算。

#### 代码（Python）  

```python
def convertDateToBinary(date: str) -> str:
    # 1. 按照 '-' 把原字符串分成 ['yyyy', 'mm', 'dd']
    year_str, month_str, day_str = date.split('-')

    # 2. 把每一段转成整数，再用 bin() 得到二进制，去掉前缀 '0b'
    #    int('08') 这种写法会自动忽略前导零，和十进制数一样处理
    year_bin = bin(int(year_str))[2:]   # 例如 2080 -> '100000100000'
    month_bin = bin(int(month_str))[2:] # 例如 02   -> '10'
    day_bin = bin(int(day_str))[2:]     # 例如 29   -> '11101'

    # 3. 用 '-' 把三个二进制块拼起来
    return f"{year_bin}-{month_bin}-{day_bin}"
```

#### 复杂度  

- **时间复杂度：O(1)**  
  这里的 `O(1)` 并不是说没有任何计算，而是说所有操作的规模都是常数级的：只处理固定长度（10 个字符）的字符串，转换三次整数，时间几乎不随输入大小变化。  
- **空间复杂度：O(1)**  
  只用了几个临时变量存放年、月、日的二进制字符串，所占空间不随输入长度增长。

---

### 2. 最优解  

#### 思路  

在本题里，暴力解已经是最优的了，因为  
1. 输入长度固定（10），没有可以进一步“削减” 的循环。  
2. 每一步的工作量（拆分、整数转换、二进制表示）都是不可或缺的基本操作。  

因此最优解与暴力解在实现上完全相同，只是把「暴力」的称呼换成「线性/常数时间」的描述。下面仍然给出同样的实现，并在注释中解释每一步背后的概念，帮助你把这种「直接转化」的思路迁移到其他类似题目上（例如把时间、IP 地址等拆分后分别转码）。

#### 代码（Python）  

```python
def convertDateToBinary(date: str) -> str:
    # 1️⃣ 拆分：把日期字符串切成年、月、日三块
    y, m, d = date.split('-')

    # 2️⃣ 转十进制 → 二进制：int() 把字符串变成整数，bin() 把整数变成二进制
    #    切片 [2:] 去掉前缀 '0b'，相当于只保留真正的二进制位
    y_bin = bin(int(y))[2:]
    m_bin = bin(int(m))[2:]
    d_bin = bin(int(d))[2:]

    # 3️⃣ 组装：用 '-' 再把三段二进制连接起来
    return f"{y_bin}-{m_bin}-{d_bin}"
```

#### 复杂度  

- **时间复杂度：O(1)**  
  与暴力解相同，所有操作都是对常数长度的字符串进行的。  
- **空间复杂度：O(1)**  
  只需要存放三个结果字符串，空间使用不随输入增长。

---

## 心得  

- **核心技巧**：字符串分割 + 十进制到二进制的直接转换。  
- **适用场景**：  
  1. 把时间戳、IP 地址等按固定分隔符拆分后分别进行进制转换。  
  2. 将身份证号、手机号等固定格式的数字串按段处理。  
- **解题钥匙**：**把“大问题”拆成“若干个小的、可以直接用语言特性解决的子问题**。  

## 反思  

- **第一反应**：看到 `"yyyy-mm-dd"`，立刻想到 `split('-')`，因为这就是最自然的切分方式。  
- **最容易踩的坑**：  
  - 忘记去掉 `bin()` 返回值的 `'0b'` 前缀，导致结果多出两个字符。  
  - 对月、日的前导零产生误解：`int('02')` 会自动把 `'02'` 当作十进制的 2 处理，转换后不需要额外处理。  
- **下次思考的第一步**：确认输入是否可以用固定分隔符直接拆分，若可以，先把它们拆开，再针对每块使用最直接的语言工具（如 `int()`、`bin()`、`hex()`）完成转换。