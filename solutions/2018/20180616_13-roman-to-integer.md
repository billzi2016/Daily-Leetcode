# #13. 罗马数字转整数 / Roman to Integer

> 难度：简单 · 标签：Hash Table、Math、String · [LeetCode 链接](https://leetcode.com/problems/roman-to-integer/)

---

## 题目（英文原版）

**Description**

Roman numerals are represented by seven different symbols: I, V, X, L, C, D and M.
For example, 2 is written as II in Roman numeral, just two ones added together. 12 is written as XII, which is simply X + II. The number 27 is written as XXVII, which is XX + V + II.
Roman numerals are usually written largest to smallest from left to right. However, the numeral for four is not IIII. Instead, the number four is written as IV. Because the one is before the five we subtract it making four. The same principle applies to the number nine, which is written as IX. There are six instances where subtraction is used:
Given a roman numeral, convert it to an integer.

**Examples**

**Example 1:**

```
Symbol       Value
I             1
V             5
X             10
L             50
C             100
D             500
M             1000
```

**Example 2:**

```
Input: s = "III"
Output: 3
Explanation: III = 3.
```

**Example 3:**

```
Input: s = "LVIII"
Output: 58
Explanation: L = 50, V= 5, III = 3.
```

**Example 4:**

```
Input: s = "MCMXCIV"
Output: 1994
Explanation: M = 1000, CM = 900, XC = 90 and IV = 4.
```

**Constraints**

- 1 <= s.length <= 15
- s contains only the characters ('I', 'V', 'X', 'L', 'C', 'D', 'M').
- It is guaranteed that s is a valid roman numeral in the range [1, 3999].

---

## 题目（中文翻译）

罗马数字（Roman numerals）由七个不同的符号表示：`I`、`V`、`X`、`L`、`C`、`D` 和 `M`。  
例如，数字 **2** 写作 `II`，即两个 `I` 相加。数字 **12** 写作 `XII`，即 `X + II`。数字 **27** 写作 `XXVII`，即 `XX + V + II`。  

罗马数字通常从左到右按从大到小的顺序书写。但数字 **4** 并不是 `IIII`，而是写作 `IV`——因为 `I` 位于 `V` 前面，需要减去 `I`，得到 4。相同的原则也适用于数字 **9**，写作 `IX`。在罗马数字中，有 **六种** 使用减法的情况：

- `IV` = 4  
- `IX` = 9  
- `XL` = 40  
- `XC` = 90  
- `CD` = 400  
- `CM` = 900  

**任务**：给定一个罗马数字字符串，将其转换为整数。

### 示例

**示例 1**  

| Symbol | Value |
|--------|-------|
| I      | 1     |
| V      | 5     |
| X      | 10    |
| L      | 50    |
| C      | 100   |
| D      | 500   |
| M      | 1000  |

**示例 2**  
Input: `s = "III"`  
Output: `3`  
**解释**：`III` = 3。

**示例 3**  
Input: `s = "LVIII"`  
Output: `58`  
**解释**：`L` = 50, `V` = 5, `III` = 3。

**示例 4**  
Input: `s = "MCMXCIV"`  
Output: `1994`  
**解释**：`M` = 1000, `CM` = 900, `XC` = 90, `IV` = 4。

### 约束条件

- `1 <= s.length <= 15`
- `s` 只包含字符 `'I'`, `'V'`, `'X'`, `'L'`, `'C'`, `'D'`, `'M'`。
- 保证 `s` 是一个有效的罗马数字，且对应的整数在 `[1, 3999]` 范围内。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：把罗马数字的每个字符都看成对应的阿拉伯数字，然后**把相邻的两个字符**拿出来比较。  
- 如果左边的字符对应的值 **小于** 右边的字符对应的值，则这两个字符表示的是“减法”（例如 `IV` → 5‑1），我们把 **左字符的值取负**，再把右字符的值正常相加。  
- 否则就是普通的加法（例如 `VI` → 5+1），直接相加即可。  

这里需要用到 **哈希表**（在 Python 中叫 `dict`），它的作用就像一本查字典：  
- **key**（钥匙）是罗马字符 `'I','V','X','L','C','D','M'`，  
- **value**（对应的页码）是它们对应的整数 `1,5,10,50,100,500,1000`。  

只要把每个字符的值查出来，按照上面的规则累加，就能得到最终的整数。  
为什么它一定对？因为罗马数字的定义正是这样：**从左到右**，如果出现“左小右大”的情况，就要把左边的数减去；否则就加。只要严格按照这个规则遍历一次，答案必然正确。  

**时间/空间复杂度**  
- 我们只遍历一次字符串，字符个数记作 `n`，所以时间复杂度是 **O(n)**。  
  - “O(n)” 的意思是：如果字符串长度翻倍，程序跑的时间也大概会翻倍，呈线性增长。  
- 额外使用的哈希表只保存 7 条映射，空间是 **O(1)**（常数级），不随 `n` 增长。  

#### 代码（Python）  

```python
def romanToInt(s: str) -> int:
    # 1. 建立字符到数值的映射表（相当于查字典）
    value = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000,
    }

    total = 0                      # 最终答案
    n = len(s)

    for i in range(n):
        cur = value[s[i]]          # 当前字符对应的整数

        # 2. 看看右边有没有字符，且右边字符的数值更大
        if i + 1 < n and cur < value[s[i + 1]]:
            total -= cur           # 需要减去
        else:
            total += cur           # 正常相加

    return total
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 随着输入长度线性增长。  
- **空间复杂度**：`O(1)` —— 只用了一个固定大小的字典。  



---  

### 2. 最优解  

#### 思路  

虽然上面的暴力解已经是 `O(n)`，但我们可以把**比较的方向**改成从右往左，这样只需要记住**已经遍历过的最大值**，不必每次都去查找右边的字符。  

**瓶颈**  
- 暴力解在每一步都要看“右边的字符”，这会产生 `i+1` 的边界检查，思路上稍显繁琐。  
- 若把遍历方向改为 **从后往前**，我们只需要比较**当前字符的值**和**已经看到的最大值**（即右侧最大值）。  
  - 如果当前值 **小于** 最大值，说明它是“左小右大” 的减法情形，需要 **减去**。  
  - 否则，它应该 **加上**，并且更新最大值为当前值（因为向左继续遍历时，当前值是新的右侧最大值）。  

这样只用 **一个额外变量** `max_right` 保存右侧最大值，代码更简洁，逻辑也更直观。  

**核心数据结构**  
- 同样使用 **哈希表** 把字符映射到整数。  
- 额外的一个整数 `max_right` 用来记录“当前已经看到的最大的罗马数值”。  

**类比**  
想象你在看一条向左延伸的山坡，`max_right` 就像是你已经爬到的最高海拔。往左走时，如果前面的山峰比最高海拔低，你就往下走（减去），否则你就往上走（加上），并把最高海拔更新为这座山峰的高度。  

#### 代码（Python）  

```python
def romanToInt(s: str) -> int:
    # 1. 同样的查字典表
    value = {
        'I': 1, 'V': 5, 'X': 10,
        'L': 50, 'C': 100, 'D': 500, 'M': 1000,
    }

    total = 0          # 最终结果
    max_right = 0      # 右侧已经出现的最大值，初始为 0

    # 2. 从右往左遍历字符
    for ch in reversed(s):               # reversed() 让我们一次得到倒序的字符
        cur = value[ch]                   # 当前字符对应的整数

        if cur < max_right:               # 小于右侧最大值 → 减法
            total -= cur
        else:                             # 大于等于 → 加法，并更新 max_right
            total += cur
            max_right = cur               # 更新右侧最大值

    return total
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 仍然只遍历一次，只是把方向改了，实际运行速度稍快。  
- **空间复杂度**：`O(1)` —— 只用了常数级的字典和两个整数变量。  

相比暴力解，**逻辑更清晰**，省去了每一步的边界检查，代码更易于阅读和维护。  



## 心得  

- 这道题的核心技巧是**把“左小右大”视为减法**，并利用**哈希表**快速把字符转成数值。  
- 适用该技巧的相似题目  
  1. **整数转罗马**（把阿拉伯数字转成罗马字符）  
  2. **Excel 表格列序号**（把类似 “AB” 的字符串转成数字）  
  3. **自定义进制数转换**（比如把 “1011” 按 2 进制转十进制）  
- 解题钥匙：**从右往左遍历，保持右侧最大值**，小于它就减，大于等于就加。  



## 反思  

- **第一反应**：看到罗马数字，我立刻想到“左小右大要减”，于是把每个字符的值查出来，按照相邻两字符的大小关系决定加还是减。  
- **最容易踩的坑**  
  - 忽略了最后一个字符的处理（因为它右边没有字符，需要单独加上）。  
  - 对于只出现一次的字符（如 `"V"`）没有正确判断加法。  
  - 边界条件：字符串长度为 1 时仍然要返回对应的数值。  
- **下次遇到同类题**：第一步先**明确符号之间的大小关系规则**，决定是**正向遍历**还是**逆向遍历**更方便，然后用**哈希表**把字符映射为数值，最后按照规则累加或累减。