# #2288. 对价格进行折扣 / Apply Discount to Prices

> 难度：中等 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/apply-discount-to-prices/)

---

## 题目（英文原版）

**Description**

A sentence is a string of single-space separated words where each word can contain digits, lowercase letters, and the dollar sign '$'. A word represents a price if it is a sequence of digits preceded by a dollar sign.
You are given a string sentence representing a sentence and an integer discount. For each word representing a price, apply a discount of discount% on the price and update the word in the sentence. All updated prices should be represented with exactly two decimal places.
Return a string representing the modified sentence.
Note that all prices will contain at most 10 digits.

**Examples**

**Example 1:**

```
Input: sentence = "there are $1 $2 and 5$ candies in the shop", discount = 50
Output: "there are $0.50 $1.00 and 5$ candies in the shop"
Explanation: 
The words which represent prices are "$1" and "$2". 
- A 50% discount on "$1" yields "$0.50", so "$1" is replaced by "$0.50".
- A 50% discount on "$2" yields "$1". Since we need to have exactly 2 decimal places after a price, we replace "$2" with "$1.00".
```

**Example 2:**

```
Input: sentence = "1 2 $3 4 $5 $6 7 8$ $9 $10$", discount = 100
Output: "1 2 $0.00 4 $0.00 $0.00 7 8$ $0.00 $10$"
Explanation: 
Applying a 100% discount on any price will result in 0.
The words representing prices are "$3", "$5", "$6", and "$9".
Each of them is replaced by "$0.00".
```

**Constraints**

- 1 <= sentence.length <= 105
- sentence consists of lowercase English letters, digits, ' ', and '$'.
- sentence does not have leading or trailing spaces.
- All words in sentence are separated by a single space.
- All prices will be positive numbers without leading zeros.
- All prices will have at most 10 digits.
- 0 <= discount <= 100

---

## 题目（中文翻译）

**描述**  
一句话（sentence）是由单个空格分隔的若干单词组成的字符串，每个单词可能包含数字、小写字母以及美元符号 `'$'`。如果一个单词是以美元符号开头、后面紧跟数字序列，则该单词表示一个价格（price）。

给定字符串 `sentence` 表示一句话，以及整数 `discount`（折扣百分比）。对句子中每个表示价格的单词，按照 `discount%` 的折扣计算新的价格，并用该新价格替换原单词。所有更新后的价格必须保留 **恰好两位小数**（即使小数部分为 0 也要显示），并仍以 `'$'` 开头。

返回修改后的句子字符串。

> **注意**  
> - 所有价格的数字部分长度不超过 10 位。

**示例 1**  
```text
输入: sentence = "there are $1 $2 and 5$ candies in the shop", discount = 50
输出: "there are $0.50 $1.00 and 5$ candies in the shop"
解释:
表示价格的单词是 "$1" 和 "$2"。
- 对 "$1" 打 50% 折扣得到 "$0.50"，所以用 "$0.50" 替换 "$1"。
- 对 "$2" 打 50% 折扣得到 "$1"。由于价格必须保留两位小数，最终写成 "$1.00"。
其余单词保持不变。
```

**示例 2**  
```text
输入: sentence = "1 2 $3 4 $5 $6 7 8$ $9 $10$", discount = 100
输出: "1 2 $0.00 4 $0.00 $0.00 7 8$ $0.00 $10$"
解释:
折扣为 100% 时，所有价格均变为 0。
句子中表示价格的单词有 "$3"、"$5"、"$6" 和 "$9"，它们全部被替换为 "$0.00"。
其余单词保持不变。
```

**约束条件**
- `1 <= sentence.length <= 10^5`
- `sentence` 只包含小写英文字母、数字、空格 `' '` 和字符 `'$'`
- `sentence` **不**含首尾空格，且单词之间仅有单个空格分隔
- 所有价格都是正数，且不含前导零
- 每个价格的数字部分最多 10 位
- `0 <= discount <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

1. **把句子切成单词**  
   句子里单词之间只有一个空格，使用 `sentence.split(' ')` 就能得到一个列表。可以把每个单词想象成一句话里的“拼图块”。  

2. **判断一个单词是不是价格**  
   - 必须以字符 `$` 开头。  
   - `$` 后面只能是数字（`0-9`），且至少有一位。  
   这相当于在查字典：**key** 是 `$`，**value** 必须全部是数字。我们可以直接遍历 `$` 后面的字符，检查它们是否都是数字。如果全部是数字，则该单词是价格。  

3. **对价格进行折扣计算**  
   - 把 `$` 后面的数字转成 `int` → 原价 `price`。  
   - 折扣后的实际金额 = `price * (100 - discount) / 100`。  
   - 结果要保留 **恰好两位小数**，可以用 Python 的格式化 `"{:.2f}"`。  

4. **把折扣后的价格重新拼回原句**  
   把每个单词（有可能已经被改成 `$0.50` 之类）重新用空格 `' '` 连接起来，得到最终的句子。  

> **为什么这个方法一定正确？**  
> - 只要单词满足 “`$` + 全数字” 这两个条件，它必然是题目定义的价格。  
> - 折扣公式是题目直接给出的数学表达式，使用浮点数除法再保留两位小数即可得到题目要求的格式。  

#### 代码（Python）

```python
def discountPrices(sentence: str, discount: int) -> str:
    # 把句子拆成单词，单词之间只有一个空格
    words = sentence.split(' ')
    res = []                       # 用来保存处理后的单词

    for w in words:
        # ---------- 判断是否为价格 ----------
        if w.startswith('$') and len(w) > 1:   # 必须以 $ 开头且后面还有字符
            number_part = w[1:]                # 去掉开头的 $
            # 检查剩余部分是否全是数字
            if number_part.isdigit():          # str.isdigit() 相当于“全是数字”
                price = int(number_part)       # 原价（整数）
                # ---------- 计算折后价 ----------
                discounted = price * (100 - discount) / 100
                # 保留两位小数，并加上 $ 符号
                new_word = f"${discounted:.2f}"
                res.append(new_word)
                continue          # 已处理完当前单词，直接进入下一个
        # ---------- 不是价格，保持原样 ----------
        res.append(w)

    # 用空格把所有单词拼回一句话
    return ' '.join(res)
```

#### 复杂度

- **时间复杂度：O(n)**  
  `n` 为句子中字符的总数。我们只遍历了一遍句子（`split`、遍历单词、检查每个字符是否是数字），每个字符最多被访问常数次。  
  *大白话*：如果句子长 1000 个字符，算法大约需要 1000 次左右的基本操作。

- **空间复杂度：O(n)**  
  需要额外的列表 `words` 和 `res` 来存放拆分后的单词以及结果，最坏情况下占用与输入相同量级的空间。  

---

### 2. 最优解

#### 思路  

对于这道题，**暴力解已经是最优的**，因为：

- 句子本身必须被一次遍历才能检查每个单词是否是价格，无法做到更少的遍历次数。  
- 价格的判断只需要检查 `$` 后面的字符是否全是数字，这一步已经是 **O(单词长度)** 的最小可能复杂度。  
- 折扣计算和格式化也是常数时间操作。

因此，真正的“优化”在于 **代码实现的简洁性和常数因子**：

1. **使用字符串的内置方法** `isdigit()` 替代手动遍历字符。  
2. **一次性完成所有处理**：在遍历单词时直接决定是否替换并写入结果列表，避免二次遍历。  
3. **避免不必要的类型转换**：只在确认是价格后才把数字转成 `int`，其余单词保持原字符串。

上述技巧让代码更加**线性且常数因子更小**，在大数据量（句子长度 10⁵）时表现更好。

#### 代码（Python）

```python
def discountPrices(sentence: str, discount: int) -> str:
    # 直接在遍历时完成拆分、判别、计算、拼接
    words = sentence.split()
    factor = (100 - discount) / 100          # 预先算好的折扣系数

    for i, w in enumerate(words):
        # 必须以 $ 开头且后面全是数字，才能算作价格
        if w.startswith('$') and w[1:].isdigit():
            price = int(w[1:])                # 把数字部分转成整数
            discounted = price * factor       # 计算折后价（浮点数）
            # 使用 f-string 保留两位小数，并加上 $
            words[i] = f"${discounted:.2f}"
        # 不是价格的单词保持不变

    return ' '.join(words)
```

#### 复杂度

- **时间复杂度：O(n)**  
  与暴力解相同，只是常数因子更小。遍历一次句子，每个字符最多被 `split`、`isdigit`、`int`、`format` 其中一次。

- **空间复杂度：O(n)**  
  需要存放拆分后的单词列表，和最终返回的字符串。  

---

## 心得

- **核心技巧**：字符串的分割、前缀判断、数字校验 (`isdigit`) 与浮点数格式化。  
- **适用的题型**  
  1. “把句子中符合某种模式的单词替换成新值”——如把所有邮箱地址脱敏。  
  2. “根据特定前缀/后缀识别并处理数值”——如把所有以 `#` 开头的标签转成整数。  
- **一句话总结**：**先把句子拆开，利用 `startswith`+`isdigit` 快速定位价格，再用公式乘折扣系数、`{:.2f}` 保留两位小数即可。**

## 反思

- **第一反应**：把句子按空格切开，逐个检查是否是 `$` 开头的数字，然后直接算折扣。  
- **最容易踩的坑**  
  - 忽略了 `$` 后面可能是空字符串（如单独的 `$`），需要确保至少有一位数字。  
  - 折扣为 100% 时要输出 `$0.00`，不能出现 `-0.00`（浮点数负零）。  
  - 保留两位小数时一定要使用格式化，否则 `1` 会变成 `$1` 而不是 `$1.00`。  
- **下次遇到同类题**：第一步先**确定“识别模式”（前缀/全数字）**，再**一次遍历完成替换**，避免多余的遍历或临时结构。