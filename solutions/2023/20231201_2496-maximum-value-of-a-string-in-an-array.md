# #2496. 数组中字符串的最大值 / Maximum Value of a String in an Array

> 难度：简单 · 标签：Array、String · [LeetCode 链接](https://leetcode.com/problems/maximum-value-of-a-string-in-an-array/)

---

## 题目（英文原版）

**Description**

The value of an alphanumeric string can be defined as:
Given an array strs of alphanumeric strings, return the maximum value of any string in strs.

**Examples**

**Example 1:**

```
Input: strs = ["alic3","bob","3","4","00000"]
Output: 5
Explanation: 
- "alic3" consists of both letters and digits, so its value is its length, i.e. 5.
- "bob" consists only of letters, so its value is also its length, i.e. 3.
- "3" consists only of digits, so its value is its numeric equivalent, i.e. 3.
- "4" also consists only of digits, so its value is 4.
- "00000" consists only of digits, so its value is 0.
Hence, the maximum value is 5, of "alic3".
```

**Example 2:**

```
Input: strs = ["1","01","001","0001"]
Output: 1
Explanation: 
Each string in the array has value 1. Hence, we return 1.
```

**Constraints**

- 1 <= strs.length <= 100
- 1 <= strs[i].length <= 9
- strs[i] consists of only lowercase English letters and digits.

---

## 题目（中文翻译）

字母数字字符串（alphanumeric string）的价值定义如下：  
- 若字符串仅由数字组成，则其价值为该字符串对应的数值（忽略前导零）。  
- 否则，价值为字符串的长度。

给定一个由字母数字字符串组成的数组 `strs`，返回 `strs` 中任意字符串的最大价值。

## 示例

### 示例 1
**输入**: `strs = ["alic3","bob","3","4","00000"]`  
**输出**: `5`  
**解释**:  
- `"alic3"` 同时包含字母和数字，其价值为长度，即 `5`。  
- `"bob"` 只包含字母，其价值也为长度，即 `3`。  
- `"3"` 只包含数字，其价值为数值 `3`。  
- `"4"` 只包含数字，其价值为数值 `4`。  
- `"00000"` 只包含数字，数值为 `0`（忽略前导零），其价值为 `0`。  
因此最大价值为 `5`。

### 示例 2
**输入**: `strs = ["1","01","001","0001"]`  
**输出**: `1`  
**解释**:  
数组中的每个字符串均只含数字，且数值均为 `1`（去掉前导零后）。因此返回 `1`。

## 约束条件
- `1 <= strs.length <= 100`
- `1 <= strs[i].length <= 9`
- `strs[i]` 只由小写英文字母和数字组成。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把数组里的每个字符串都“逐个检查”一遍：

1. **判断字符串只包含数字还是包含字母**  
   - 可以把每个字符都和 `'0'~'9'` 比对，或者直接使用 Python 的 `str.isdigit()` 方法。  
   - 这里把 `isdigit` 想象成一本**查字典**：把整个单词（字符串）交给字典，如果每个字母都是“数字”，字典就会说“是”，否则说“不是”。  

2. **计算该字符串的“价值”**  
   - **全是数字** → 把它当成十进制整数读出来（`int(s)`），这相当于把“00123”变成数字 `123`。  
   - **包含字母** → 直接把字符串的长度当作价值。  

3. **在遍历的过程中维护最大价值**，最后返回即可。

**为什么这个方法一定对？**  
- 价值的定义在题目里已经完整给出：要么是“整数值”，要么是“长度”。只要我们把每个字符串对应的价值算出来，取最大值就是答案。  

**复杂度分析（大白话）**  
- **时间**：我们要看每个字符串的每个字符一次，判断它是不是数字。设数组长度为 `n`，每个字符串最长 `L`（题目说最多 9），总共检查 `n × L` 次。用大写的 **O(n·L)** 表示，意思就是“随数组大小和每个字符串长度线性增长”。  
- **空间**：只用几个整数保存当前价值和最大价值，和输入规模无关，用 **O(1)** 表示“常数级”空间。  

#### 代码（Python）  

```python
def maximumValue(strs):
    """
    返回数组中任意字符串的最大价值
    """
    max_val = 0                     # 用来保存遍历过程中出现的最大价值

    for s in strs:                  # 逐个取出字符串
        # 1. 判断是否全部由数字组成
        if s.isdigit():            # s.isdigit() 相当于“查字典”：全是数字返回 True
            cur = int(s)           # 全数字 → 把字符串直接转成整数
        else:
            cur = len(s)           # 含字母 → 用字符串长度当价值

        # 2. 更新最大价值
        if cur > max_val:
            max_val = cur

    return max_val
```

#### 复杂度  

- **时间复杂度：O(n·L)**  
  - `n` 是数组长度，`L` 是单个字符串的最长长度（这里 ≤ 9），所以整体随 `n` 与 `L` 成正比。  
- **空间复杂度：O(1)**  
  - 只用了固定的几个变量，和输入大小无关。  

---  

### 2. 最优解  

#### 思路  

对于这道 **Easy** 题，暴力解已经是 **最优** 的了，因为我们必须**至少看一遍**每个字符才能判断它是全数字还是包含字母。没有办法在不检查字符的情况下得到正确的价值。

唯一可以做的优化是**把代码写得更简洁、更“Pythonic”**，从而让实现更易读、常数因子更小：

- 用 `max()` 搭配 **列表推导式** 一行算出所有价值，再取最大值。  
- 判断全数字仍然使用 `str.isdigit()`，转整数用 `int()`，长度用 `len()`，这都是 O(1) 的内置操作。  

这样仍然是一次遍历，时间复杂度不变，但代码更短。  

#### 代码（Python）  

```python
def maximumValue(strs):
    """
    一行代码搞定：先把每个字符串映射为它的价值，然后取最大值
    """
    # 列表推导式把每个 s 转成对应的价值：
    #   - 全数字 → int(s)
    #   - 否则    → len(s)
    values = [int(s) if s.isdigit() else len(s) for s in strs]

    # max() 直接返回最大的价值
    return max(values)
```

> **小技巧**：如果你担心 `max()` 在空列表上会报错（这里不会，因为题目保证 `strs` 至少有一个元素），可以写成 `max(values, default=0)`，给出默认值。  

#### 复杂度  

- **时间复杂度：O(n·L)**  
  - 仍然需要检查每个字符一次，和暴力解的时间复杂度完全相同。  
- **空间复杂度：O(n)**  
  - 这里额外创建了一个长度为 `n` 的列表 `values` 来保存每个字符串的价值。  
  - 如果想把空间降回 **O(1)**，可以在遍历时直接维护最大值（即第一种实现），两者在本题规模下都完全可接受。  

---  

## 心得  

- **核心技巧**：**字符分类 + 条件取值**。先判断字符串是否全为数字，再决定使用整数值还是长度。  
- **适用的题型**  
  1. “字符串价值”类：如 LeetCode 1795 *Maximum Number of Groups Entering a Competition*（需要判断全数字或字母）。  
  2. “根据内容决定数值”类：如 LeetCode 1368 *Minimum Cost to Make at Least One Valid Path in a Grid*（根据格子属性取不同权值）。  
- **解题钥匙**：**“先分类，再统一处理”**——把所有可能的情况拆开判断，然后用统一的方式（取最大/最小/求和）收敛答案。  

---  

## 反思  

- **第一反应**：看到“全数字 → 数值，其余 → 长度”，马上想到遍历每个字符串并用 `isdigit` 判断。  
- **最容易踩的坑**  
  - **前导零**：`int("00000")` 会得到 `0`，这正是题目要求的“数值”。  
  - **空字符串**：题目保证每个字符串长度 ≥ 1，故不必额外处理。  
  - **混合字符**：只要出现一个字母，就直接取长度，不需要把数字部分转成整数。  
- **下次类似题的第一步**：先**明确每种输入类型对应的价值/代价**，再**决定用哪种数据结构或语言特性（如 `isdigit`、`int`、`len`）快速得到该价值**。