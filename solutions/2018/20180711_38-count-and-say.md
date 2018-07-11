# #38. 计数并说 / Count and Say

> 难度：中等 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/count-and-say/)

---

## 题目（英文原版）

**Description**

The count-and-say sequence is a sequence of digit strings defined by the recursive formula:
Run-length encoding (RLE) is a string compression method that works by replacing consecutive identical characters (repeated 2 or more times) with the concatenation of the character and the number marking the count of the characters (length of the run). For example, to compress the string "3322251" we replace "33" with "23", replace "222" with "32", replace "5" with "15" and replace "1" with "11". Thus the compressed string becomes "23321511".
Given a positive integer n, return the nth element of the count-and-say sequence.

**Examples**

**Example 1:**

```
countAndSay(1) = "1"
countAndSay(2) = RLE of "1" = "11"
countAndSay(3) = RLE of "11" = "21"
countAndSay(4) = RLE of "21" = "1211"
```

**Constraints**

- 1 <= n <= 30

---

## 题目（中文翻译）

计数并说序列（count-and-say sequence）是一系列由递归公式定义的数字字符串。  
游程编码（Run-length encoding，RLE）是一种字符串压缩方法，它通过将连续相同的字符（出现次数 ≥ 2）替换为“字符 + 出现次数”的形式来实现。例如，将字符串 `"3322251"` 压缩时，先把 `"33"` 替换为 `"23"`，再把 `"222"` 替换为 `"32"`，把 `"5"` 替换为 `"15"`，把 `"1"` 替换为 `"11"`，最终得到压缩后的字符串 `"23321511"`。

给定一个正整数 `n`，返回计数并说序列的第 `n` 项。

**示例 1：**  
**示例 2：**  
**约束条件：**

示例：
示例 1:
```
countAndSay(1) = "1"
countAndSay(2) = RLE of "1" = "11"
countAndSay(3) = RLE of "11" = "21"
countAndSay(4) = RLE of "21" = "1211"
```

约束条件：
- 1 <= n <= 30

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**从第 1 项 “1” 开始，依次生成第 2、3 … 第 n 项**。  
每一次生成新项时，只需要把当前字符串从左到右“顺着数”，把相同字符连续出现的次数和字符本身拼在一起，即完成一次 **Run‑Length Encoding（RLE）**。  

可以把 RLE 想象成 **查字典**：  
- **键（key）** 是“某个字符出现的次数”，  
- **值（value）** 是“这个字符本身”。  
把键和值连起来，就得到压缩后的描述。  

实现上，最朴素的办法是：

1. 用一个 `for` 循环遍历当前字符串的每个字符。  
2. 用两个变量 `cnt`（计数）和 `prev`（前一个字符）记录当前连续相同字符的个数。  
3. 当遇到不同字符或遍历结束时，把 `cnt` 与 `prev` 用字符串拼接（`str(cnt) + prev`），直接 **`+`** 到结果字符串上。  

因为 Python 的字符串是不可变的，每一次 `+` 实际上都会生成一个新的字符串并拷贝旧内容，这在循环里会产生 **大量的复制工作**，所以虽然思路正确，但效率不高。

**为什么它是对的？**  
- 每一次遍历都完整地统计了相邻相同字符的出现次数，正好对应题目要求的 “说出” 操作。  
- 只要从第 1 项一直迭代到第 n 项，就一定会得到第 n 项的答案。  

#### 代码（Python）

```python
def countAndSay_brute(n: int) -> str:
    """暴力版：每次生成新串时直接用字符串拼接 (+)"""
    cur = "1"                       # 第 1 项
    for _ in range(1, n):           # 需要生成 n-1 次
        nxt = ""                    # 用来保存下一项
        cnt = 1                     # 当前字符出现的次数，至少为 1
        for i in range(1, len(cur)):
            if cur[i] == cur[i - 1]:    # 与前一个字符相同，计数加一
                cnt += 1
            else:                       # 遇到不同字符，输出计数+字符
                nxt += str(cnt) + cur[i - 1]
                cnt = 1                 # 重新计数新字符
        # 循环结束后，还要把最后一段字符输出
        nxt += str(cnt) + cur[-1]
        cur = nxt                     # 更新为下一项
    return cur
```

> **关键行解释**  
> - `nxt += str(cnt) + cur[i - 1]`：把“出现次数 + 该字符”拼到结果中。  
> - `cur = nxt`：把生成好的字符串设为下一轮的输入。  

#### 复杂度  

- **时间复杂度**：`O(T)`，其中 `T` 是生成第 n 项过程中所有字符的总遍历次数。  
  - 第 1 项长度是 1，第 2 项长度约为 2，第 3 项约为 2·2，…… 第 n 项的长度大约是 `2^{n-1}`（实际略小），所以总体是指数级的。  
  - 用大白话说，`O(2^n)` 就是“随着 n 增大，工作量会像翻倍一样快速增长”。  
- **空间复杂度**：`O(L)`，`L` 为当前生成的字符串长度（即第 n 项的长度），因为我们只保存当前和下一项。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈在于字符串拼接**：  
- 每一次 `nxt += ...` 都会产生新的临时字符串，导致 **复制成本累计**。  

**优化的核心**是把 “逐字符拼接” 改成 “一次性收集后再合并”。  
在 Python 中，**列表（list）** 的 `append` 操作是 **O(1)** 的，最后使用 `''.join(list)` 把所有片段一次性拼成字符串，复制工作只发生一次。

优化步骤如下：

1. **仍然从第 1 项开始迭代**，每一次遍历当前字符串统计连续相同字符的次数。  
2. 把每一段的 “计数 + 字符” **放进列表** `parts` 中，而不是直接拼接到字符串。  
3. 遍历结束后，用 `''.join(parts)` 把列表一次性合并成新的字符串 `nxt`。  
4. 重复第 2、3 步直至第 n 项。  

这样做的好处：

- **减少了复制次数**：每一层只复制一次（在 `join` 时），而不是每添加一个片段就复制一次。  
- **时间上更接近理论下界**：遍历一次当前字符串的工作量仍是必须的，无法再省。  

#### 代码（Python）

```python
def countAndSay(n: int) -> str:
    """最优实现：使用列表收集片段，最后一次性 join"""
    cur = "1"                       # 第 1 项
    for _ in range(1, n):
        parts = []                  # 用列表收集 “计数+字符” 片段
        cnt = 1
        for i in range(1, len(cur)):
            if cur[i] == cur[i - 1]:
                cnt += 1
            else:
                # 把本段结果加入列表，注意转成字符串
                parts.append(str(cnt))
                parts.append(cur[i - 1])
                cnt = 1
        # 处理最后一段
        parts.append(str(cnt))
        parts.append(cur[-1])
        # 一次性把所有片段拼成新字符串
        cur = ''.join(parts)
    return cur
```

> **关键行解释**  
> - `parts.append(str(cnt))` / `parts.append(cur[i - 1])`：把计数和字符分别放进列表。  
> - `cur = ''.join(parts)`：一次性把列表里的所有小块拼成完整的字符串，复制工作只发生一次。  

#### 复杂度  

- **时间复杂度**：`O(T)`，同样是遍历所有字符的总次数 `T`，但因为每层只复制一次，实际运行时间比暴力版快约 **2~3 倍**。  
- **空间复杂度**：`O(L)`，需要额外的列表来保存片段，大小和最终字符串相当。  

与暴力解相比，**时间上的常数因子大幅下降**，而空间保持不变，因而是更实用的做法。

---

## 心得  

- **核心技巧**：**一次遍历 + 列表收集 + `join`**，这是一种常见的 “把 O(n²) 的字符串拼接降到 O(n)” 的手段。  
- **适用的题型**  
  1. **字符串压缩 / 解压**（如 LeetCode 443. 压缩字符串）  
  2. **分块处理**（如 LeetCode 424. 替换所有的问号）  
  3. **累计构造答案**（如 LeetCode 38. 报数）  
- **一句话总结**：**把“逐个拼接”改成“先收集再一次性拼接”。**  

---

## 反思  

- **第一反应**：直接写两个 `for` 循环，一个负责遍历当前字符串，一个负责把计数和字符拼接成新字符串。  
- **最容易踩的坑**  
  - **忘记处理最后一段**：循环结束后，仍需把最后一次计数的字符输出。  
  - **直接 `+` 拼接**导致超时（在 n=30 时仍能跑通，但如果 n 更大就会卡）。  
  - **计数是整数，需要 `str(cnt)`**，否则会报类型错误。  
- **下次类似题的第一步**：先 **思考“怎么一次遍历完成统计”**，再决定是 **直接拼接** 还是 **先收集后拼接**（视数据规模而定）。