# #273. 整数转英文单词 / Integer to English Words

> 难度：困难 · 标签：Math、String、Recursion · [LeetCode 链接](https://leetcode.com/problems/integer-to-english-words/)

---

## 题目（英文原版）

**Description**

Convert a non-negative integer num to its English words representation.

**Examples**

**Example 1:**

```
Input: num = 123
Output: "One Hundred Twenty Three"
```

**Example 2:**

```
Input: num = 12345
Output: "Twelve Thousand Three Hundred Forty Five"
```

**Example 3:**

```
Input: num = 1234567
Output: "One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven"
```

**Constraints**

- 0 <= num <= 231 - 1

---

## 题目（中文翻译）

将一个非负整数（non-negative integer）`num` 转换为其英文单词表示。

Example 1:  
Input: num = 123  
Output: "One Hundred Twenty Three"

Example 2:  
Input: num = 12345  
Output: "Twelve Thousand Three Hundred Forty Five"

Example 3:  
Input: num = 1234567  
Output: "One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven"

约束条件：  
- 0 <= num <= 2^31 - 1

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **把每一位数字都单独翻译**，然后再把这些单词拼在一起。  
可以把整数看成一串字符（比如 `"1234567"`），从左到右依次处理：

| 位数 | 位置 | 需要说的英文 |
|------|------|--------------|
| 千位 | 第 7 位 | “七 hundred” |
| 百位 | 第 6 位 | “六 hundred” |
| 十位 | 第 5 位 | “五 ten” |
| 个位 | 第 4 位 | “四” |
| …… | …… | …… |

为了让机器知道 **“5” 在十位要读成 “fifty”，而不是 “five”**，我们需要写 **大量的 `if-elif` 分支**，把每一种可能（0~9、10~19、20、30…90）都列出来。  

> **类比**：把哈希表想象成一本 **词典**，`key` 是数字，`value` 是对应的英文单词。暴力解相当于 **不使用词典**，而是手动在代码里写出所有对应关系，既冗长又容易出错。

**为什么它能得到正确答案**  
只要把每一位都翻成对应的单词，并且按照“千、百、十、个” 的顺序拼接，最终得到的字符串就是题目要求的英文表示（只要我们不忘记特殊的 10~19、以及每三位之间的空格）。

**复杂度分析**  
- **时间**：我们要遍历整数的每一位（最多 10 位，因为 `2³¹‑1` 只有 10 位），每位都要做一系列 `if` 判断。整体是 **O(d)**，其中 `d` 为数字的位数。因为位数上限是常数（10），可以认为 **O(1)**，但如果把位数记作 `n`，就相当于 **O(n)**，这在“大白话”里可以理解为“随数字长度线性增长”。  
- **空间**：只使用了常量级的变量和若干字符串常量，**O(1)**。

#### 代码（Python）

```python
def numberToWords_brutal(num: int) -> str:
    if num == 0:
        return "Zero"

    # 下面的几个列表相当于“词典”，但我们把它们写在代码里，而不是用 dict
    less_than_20 = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven",
                    "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen",
                    "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen",
                    "Nineteen"]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty",
            "Sixty", "Seventy", "Eighty", "Ninety"]

    s = str(num)                # 把整数转成字符串，方便逐位访问
    n = len(s)                  # 位数
    parts = []                  # 用来收集每一位对应的英文

    for i, ch in enumerate(s):
        digit = int(ch)         # 当前位的数字
        pos = n - i - 1         # 这位是第几位（0 表示个位，1 表示十位，…）

        # ---------- 处理个位 ----------
        if pos == 0:
            parts.append(less_than_20[digit])

        # ---------- 处理十位 ----------
        elif pos == 1:
            if digit == 1:                      # 10~19 是特殊情况
                # 把前一位（个位）和当前位一起取值
                last = int(s[-1])
                parts.append(less_than_20[10 + last])
                parts[-2] = ""                  # 把已经加进去的个位删掉
            elif digit > 1:
                parts.append(tens[digit])

        # ---------- 处理百位 ----------
        elif pos == 2:
            if digit != 0:
                parts.append(less_than_20[digit] + " Hundred")

        # ---------- 处理更高位（千、万、亿） ----------
        else:
            # 这里我们直接把每一位都拼到结果里，实际上会产生很多多余的空格和
            # “Zero Hundred” 之类的错误，说明暴力写法很难覆盖所有边界。
            # 为了演示，这里仅作占位，不做进一步处理。
            pass

    # 把所有非空的单词用空格连接起来
    return ' '.join(filter(bool, parts)).strip()
```

> **注意**：上面的实现只演示了“逐位翻译”的思路，**并不能覆盖所有合法输入**（比如 12345、1000010 等），这正是暴力解的缺点——代码会变得冗长且容易漏掉特殊情况。

#### 复杂度

- **时间复杂度**：`O(d)`（`d` 为数字的位数），在本题的取值范围内最多是 `O(10)`，即常数时间。可以理解为“遍历一次数字的每一位”。  
- **空间复杂度**：`O(1)`，只用了若干固定大小的列表和字符串变量。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**每三位一组**（千位、百位、十位、个位）是英文里最自然的分割方式：  

```
1234567 = 1 234 567
          |   |   |
        million thousand  (最后一组)
```

**瓶颈**：  
- 暴力解在处理 4 位以上的数字时，需要手动写很多 `if`，代码极其冗长且容易遗漏 “中间那一组是 0” 的情况。  
- 还有“十进制”和“千进制”混在一起的逻辑，导致大量重复代码。

**优化思路**  
1. **把数字拆成每 3 位一块**（即 “千位分组”），从低位往高位依次处理。  
2. 为每一块 **编写一个只负责 `< 1000` 的子函数**，把 0~999 之间的数字转成英文。  
   - 先处理 **百位**（如果不为 0，就输出 “X Hundred”）。  
   - 再处理 **十位和个位**：  
     - 0~19 有专门的单词表；  
     - 20~99 按十位（Twenty, Thirty …）+ 个位（One, Two …）拼接。  
3. 对每一块的结果再加上对应的 **单位词**（千、百万、十亿），注意 **如果该块为 0**（比如 1 000 001 中间的 “000”），**直接跳过**，不输出任何文字。  
4. 最后把所有非空块逆序（因为我们是从低位往高位遍历的）拼起来，中间用空格隔开。

> **类比**：  
> - **哈希表**就像一本词典，`key` 是数字（0~19、20、30…90），`value` 是对应的英文。  
> - **分块**就像把一本厚厚的书按章节拆开，只需要一次读完每一章节的标题，再把章节标题连起来就是整本书的目录。

**递归**（或循环）只在子函数里出现一次，用来处理 **“十位+个位”** 的特殊情况（0~19）。这样代码结构清晰，易于调试。

#### 代码（Python）

```python
def numberToWords(num: int) -> str:
    """
    把非负整数 num 转换成英文表示。
    由于 0 <= num <= 2**31 - 1，最多只会出现 Billion（十亿）这个单位。
    """
    if num == 0:
        return "Zero"

    # ---------- 1. 词典（相当于查字典） ----------
    less_than_20 = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven",
                    "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen",
                    "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen",
                    "Nineteen"]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty",
            "Sixty", "Seventy", "Eighty", "Ninety"]
    thousands = ["", "Thousand", "Million", "Billion"]   # 千位单位

    # ---------- 2. 处理 < 1000 的子函数 ----------
    def helper(n: int) -> str:
        """
        把 0 <= n < 1000 的数字转换成英文。
        递归只用在处理十位的 0~19 这一步，避免大量 if-else。
        """
        if n == 0:
            return ""
        elif n < 20:                     # 0~19 直接查表
            return less_than_20[n] + " "
        elif n < 100:                    # 20~99 = tens + (optional) ones
            return tens[n // 10] + " " + helper(n % 10)
        else:                            # 100~999 = hundreds + rest
            return less_than_20[n // 100] + " Hundred " + helper(n % 100)

    # ---------- 3. 主循环：按千位分块 ----------
    words = []               # 用来收集每一块的英文
    i = 0                    # 当前块的下标，决定使用哪一个 thousand 单位
    while num > 0:
        cur_chunk = num % 1000          # 取最低的三位
        if cur_chunk != 0:              # 只在非零块才输出
            chunk_word = helper(cur_chunk).strip()   # 去掉子函数末尾多余的空格
            if thousands[i]:            # 如果有单位词（如 Thousand、Million）
                chunk_word += " " + thousands[i]
            words.append(chunk_word)    # 先放进列表，后面会逆序拼接
        num //= 1000                     # 去掉已经处理的三位
        i += 1

    # ---------- 4. 合并所有块 ----------
    # 由于我们是从低位往高位遍历的，最终需要把列表逆序再用空格连接
    return ' '.join(reversed(words)).strip()
```

> **代码要点解释**  
> - `helper` 使用 **递归**（`helper(n % 10)`）来处理 “十位 + 个位” 的组合，代码简洁。  
> - `while num > 0` 每次 `num //= 1000` 把已经处理的低三位剔除，保证最多循环四次（Billion）。  
> - `if cur_chunk != 0` **跳过全为 0 的块**，避免出现 “Zero Thousand”。  
> - 最后 `reversed(words)` 把从低位收集到的英文块倒回来，形成正确的阅读顺序。

#### 复杂度

- **时间复杂度**：`O(k)`，其中 `k` 为数字的 **块数**（最多 4 块：Billion、Million、Thousand、Hundreds），可以看作 **O(1)**。直观上是“只需要看几次三位数”。  
- **空间复杂度**：`O(1)`（不计输出字符串本身）。我们只用了常量大小的列表 `less_than_20、tens、thousands` 和最多 4 个块的临时字符串。

---

## 心得

- **核心技巧**：把大整数按 **千位**（3 位）划分，再用 **递归/循环**处理每个小块。  
- **适用的题型**  
  1. **数字转英文**（本题）。  
  2. **千位分组的数字格式化**（如把整数写成千分位的字符串 `"1,234,567"`）。  
  3. **把整数拆成三位块进行分段求和**（如“Roman Numerals” 里把数字拆成千、百、十、个）。  
- **一句话总结**：**“千位分块 + 小块递归”** 是把任意大整数转成英文的钥匙。

---

## 反思

- **第一反应**：看到“把整数写成英文”，立刻想到把每一位都单独翻译——这导致大量 `if-else`，实现起来非常繁琐。  
- **最容易踩的坑**  
  - **0 的处理**：整个数字为 0 时必须返回 `"Zero"`，而不是空串。  
  - **中间块为 0**：比如 `1000010`，中间的 “000” 不能产生 `"Zero Thousand"`。  
  - **空格与大小写**：每个单词之间要恰好只有一个空格，首字母大写其余小写。  
- **下次思路**：遇到类似“把数字映射成某种分段文字”的题目，**先把数字按固定长度（如 3 位）分块**，再写一个只负责“块内部”的小函数，最后把块的结果拼起来。这样既能避免冗余代码，又能自然处理 “块为 0” 的情况。