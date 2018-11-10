# #166. 分数转循环小数 / Fraction to Recurring Decimal

> 难度：中等 · 标签：Hash Table、Math、String · [LeetCode 链接](https://leetcode.com/problems/fraction-to-recurring-decimal/)

---

## 题目（英文原版）

**Description**

Given two integers representing the numerator and denominator of a fraction, return the fraction in string format.
If the fractional part is repeating, enclose the repeating part in parentheses.
If multiple answers are possible, return any of them.
It is guaranteed that the length of the answer string is less than 104 for all the given inputs.

**Examples**

**Example 1:**

```
Input: numerator = 1, denominator = 2
Output: "0.5"
```

**Example 2:**

```
Input: numerator = 2, denominator = 1
Output: "2"
```

**Example 3:**

```
Input: numerator = 4, denominator = 333
Output: "0.(012)"
```

**Constraints**

- -231 <= numerator, denominator <= 231 - 1
- denominator != 0

---

## 题目（中文翻译）

给定两个整数，分别表示分子（numerator）和分母（denominator）构成的分数（fraction），返回该分数的字符串形式（string format）。  
如果小数部分（fractional part）出现循环，则在循环的部分外面加上括号（parentheses）。  
如果存在多种可能的答案，返回任意一种即可。  
保证对于所有给定的输入，答案字符串（answer string）的长度均小于 10^4。  

示例：

示例 1  
Input: numerator = 1, denominator = 2  
Output: "0.5"

示例 2  
Input: numerator = 2, denominator = 1  
Output: "2"

示例 3  
Input: numerator = 4, denominator = 333  
Output: "0.(012)"

约束条件  
- -2^31 ≤ numerator, denominator ≤ 2^31 - 1  
- denominator ≠ 0

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的办法就是 **手工模拟小学学的长除法**：

1. 先把分子 `numerator` 与分母 `denominator` 做整数除法，得到整数部分 `quotient`，余数记为 `remainder`。  
2. 只要余数不为 `0`，就把余数乘 `10` 再除以分母，得到下一位小数 `digit`，并把 `digit` 接在结果字符串后面。  
3. 为了判断小数是否出现循环，需要记住 **每一次出现的余数**。如果同一个余数再次出现，说明后面的除法过程会和上一次完全一样，从而产生循环。  

在暴力实现中，我们不使用哈希表（`dict`）而是用 **列表** 逐个保存出现过的余数。每次产生新余数时，遍历列表检查它是否已经出现过——这一步是 O(k) 的线性查找，k 是当前已经产生的余数个数。因为每一步都要遍历一次列表，整体复杂度会退化到 **O(n²)**（n 为产生的小数位数），但思路最直观，代码最容易写出来。

> **类比**：  
> 哈希表就像一本词典，直接用“单词”去找对应的“页码”；而列表的查找更像在一本厚厚的通讯录里，从头到尾翻页寻找同一个名字，速度自然慢一些。

#### 代码（Python）

```python
def fraction_to_decimal_brutal(numerator: int, denominator: int) -> str:
    # 处理符号，负数要在最前面加一个 '-'
    if (numerator < 0) ^ (denominator < 0):
        sign = '-'
    else:
        sign = ''
    num = abs(numerator)
    den = abs(denominator)

    # 1）整数部分
    integer_part = num // den
    remainder = num % den
    if remainder == 0:                     # 没有小数部分，直接返回整数
        return sign + str(integer_part)

    # 2）小数部分（暴力版：用列表保存余数并线性查找）
    res = [sign + str(integer_part), '.']  # 结果初始为 “整数部分.”
    seen_remainders = []                    # 用列表记录出现过的余数
    while remainder != 0:
        # 线性检查余数是否出现过（O(k)）
        if remainder in seen_remainders:
            # 找到第一次出现的位置，插入 '(' 与 ')'
            idx = seen_remainders.index(remainder)          # 循环开始的下标
            # 小数位从 2 开始（res[0] 为整数，res[1] 为 '.'）
            insert_pos = 2 + idx
            res.insert(insert_pos, '(')                     # 在循环开始前插 '('
            res.append(')')                                 # 在末尾加 ')'
            break

        # 记录当前余数的位置
        seen_remainders.append(remainder)

        # 继续长除法：余数 * 10 → 商 digit → 新余数
        remainder *= 10
        digit = remainder // den
        res.append(str(digit))
        remainder %= den

    return ''.join(res)
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  *n* 为产生的小数位数。因为每次产生新余数时都要在列表里线性查找是否出现过，最坏情况下要遍历已产生的全部余数，导致二次方的时间开销。可以把 “O(n²)” 想象成“把 1000 张纸一次又一次从头到尾检查，需要 1,000,000 次比较”，显然很慢。

- **空间复杂度**：`O(n)`  
  需要保存所有出现过的余数以及已经输出的字符。字符数和余数数目最多都是小数位数 *n*，所以空间随 n 线性增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈在于“余数是否出现过”的线性查找**。我们只要把 “余数 → 已经出现的位置” 这对映射保存下来，并且能 **O(1)（常数时间）** 查到，就可以把整体时间降到线性。

**哈希表（Python 的 dict）** 正好可以做到这点：把余数作为键（key），出现的位置（即小数位的下标）作为值（value）。每一次产生新余数时，先在 dict 里查询：

- 若不存在 → 说明还没有循环，把余数和当前位置记录进去，继续除法。  
- 若存在 → 循环开始于该位置，直接在结果字符串相应位置插入 '('，并在末尾加上 ')'，结束循环。

这样每一步的查找、插入都是 **O(1)**，整个过程只会遍历每个余数一次，时间复杂度降为 **O(n)**。

**核心概念：余数决定后续所有位**  
在长除法中，余数是唯一决定后面会出现什么数字的“状态”。当同一个余数再次出现时，后面的计算必然和上一次完全相同，于是产生了循环。这就是“**余数重复 ⇒ 小数循环**”的数学原理。

> **类比**：  
> 把哈希表想象成一本“快速检索的词典”，只要把余数写进去，就能立刻翻到对应的页码（位置），再也不用从头翻遍。

#### 代码（Python）

```python
def fraction_to_decimal(numerator: int, denominator: int) -> str:
    # 1. 处理符号
    if (numerator < 0) ^ (denominator < 0):
        sign = '-'
    else:
        sign = ''
    num = abs(numerator)
    den = abs(denominator)

    # 2. 整数部分
    integer_part = num // den
    remainder = num % den
    if remainder == 0:                     # 整除，直接返回整数
        return sign + str(integer_part)

    # 3. 小数部分（使用哈希表记录余数 → 位置）
    res = [sign + str(integer_part), '.']  # 初始结果
    remainder_pos = {}                     # 余数 -> 小数位在 res 中的下标

    while remainder != 0:
        # 若余数已经出现，说明开始循环
        if remainder in remainder_pos:
            idx = remainder_pos[remainder]          # 循环起始位置（相对于小数位的下标）
            insert_pos = 2 + idx                     # 2 是整数部分和 '.' 的长度
            res.insert(insert_pos, '(')              # 在循环开始前插 '('
            res.append(')')                          # 在末尾加 ')'
            break

        # 记录当前余数出现的位置（相对于小数位的下标）
        remainder_pos[remainder] = len(res) - 2      # -2 去掉整数部分和 '.'

        # 长除法一步：余数*10 → 商 digit → 新余数
        remainder *= 10
        digit = remainder // den
        res.append(str(digit))
        remainder %= den

    return ''.join(res)
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  只遍历每个余数一次，每次查找/插入哈希表都是常数时间。相比暴力的 `O(n²)`，就像把“从头翻遍通讯录”换成了“一眼看到对应条目”，快了很多。

- **空间复杂度**：`O(n)`  
  仍然需要保存出现过的余数（哈希表）以及已经生成的字符。但不再有额外的线性遍历开销。

---

## 心得

- **核心技巧**：利用余数的“状态唯一性”并用哈希表记录余数出现的位置，快速判断循环起点。  
- **适用的题型**：  
  1. **循环小数**（本题）  
  2. **判断链表是否有环**（使用哈希表或快慢指针）  
  3. **寻找数组中重复元素的第一个出现位置**（哈希表记录索引）  
- **一句话总结**：  
  “余数重复即循环，用哈希表把余数映射到位置，瞬间定位循环起点。”

---

## 反思

- **第一反应**：把分数除出来，手动做长除法，记下每一步的余数。  
- **最容易踩的坑**：  
  - **符号处理**：负数需要在最前面加 `-`，且 `-0` 要统一为 `0`。  
  - **整数部分为 0**：如 `1/2`，结果应是 `0.5`，不能漏掉前导 `0`。  
  - **余数为 0 的情况**：比如 `4/2`，没有小数点，直接返回整数。  
  - **极端整数范围**：`-2^31` 直接取绝对值会溢出，用 Python 的大整数不怕，但在其他语言要小心。  
- **下次遇到同类题**：第一步先 **判断是否会出现循环**——把“余数 → 位置”这个映射写出来，决定是用哈希表还是其他方式（比如快慢指针）。这样可以立刻把搜索空间从 “所有已生成的余数” 缩到 “常数时间查找”。