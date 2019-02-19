# #306. 可加数 / Additive Number

> 难度：中等 · 标签：String、Backtracking · [LeetCode 链接](https://leetcode.com/problems/additive-number/)

---

## 题目（英文原版）

**Description**

An additive number is a string whose digits can form an additive sequence.
A valid additive sequence should contain at least three numbers. Except for the first two numbers, each subsequent number in the sequence must be the sum of the preceding two.
Given a string containing only digits, return true if it is an additive number or false otherwise.
Note: Numbers in the additive sequence cannot have leading zeros, so sequence 1, 2, 03 or 1, 02, 3 is invalid.
Follow up: How would you handle overflow for very large input integers?

**Examples**

**Example 1:**

```
Input: "112358"
Output: true
Explanation: 
The digits can form an additive sequence: 1, 1, 2, 3, 5, 8. 
1 + 1 = 2, 1 + 2 = 3, 2 + 3 = 5, 3 + 5 = 8
```

**Example 2:**

```
Input: "199100199"
Output: true
Explanation: 
The additive sequence is: 1, 99, 100, 199. 
1 + 99 = 100, 99 + 100 = 199
```

**Constraints**

- 1 <= num.length <= 35
- num consists only of digits.

---

## 题目（中文翻译）

**描述**  
可加数（additive number）是指其数字可以形成一个加法序列（additive sequence）的字符串。  
一个合法的加法序列必须至少包含三个数字。除了前两个数字外，序列中的每一个后续数字都必须等于其前两个数字之和。  
给定仅由数字组成的字符串 `num`，如果它是可加数则返回 `true`，否则返回 `false`。  

**说明**  
加法序列中的数字不能有前导零。因此序列 `1, 2, 03` 或 `1, 02, 3` 均视为无效。

**示例 1**  
```
Input: "112358"
Output: true
Explanation: 
The digits can form an additive sequence: 1, 1, 2, 3, 5, 8. 
1 + 1 = 2, 1 + 2 = 3, 2 + 3 = 5, 3 + 5 = 8
```

**示例 2**  
```
Input: "199100199"
Output: true
Explanation: 
The additive sequence is: 1, 99, 100, 199. 
1 + 99 = 100, 99 + 100 = 199
```

**约束条件**  
- `1 <= num.length <= 35`  
- `num` 仅由数字组成  

**进阶**  
如果输入的整数非常大，如何处理溢出问题？

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把字符串的前面任意切成两个数**（记为 `first`、`second`），然后按照“后面的数 = 前两个数之和”不断往后匹配，看看能否把整个字符串完整地走完。

- **数据结构**：这里我们只用到 **字符串**（`str`）和 **列表**（`list`）来保存已经得到的序列。  
  - 把字符串切片（`s[i:j]`）想象成在一串珠子中间剪开取出一段珠子。  
  - 判断是否相等相当于把两段珠子摆在一起比对。

- **为什么正确**：如果存在一个合法的加法序列，那么一定可以在某个位置把前两个数挑出来，之后每一步的和都唯一决定了下一个数。只要我们把所有可能的前两段尝试一遍，就一定会找到这条合法路径（如果有的话）。

- **时间/空间复杂度**  
  - 我们要枚举 `first` 的结束位置 `i`（最多 `n-2` 种）和 `second` 的结束位置 `j`（最多 `n-1-i` 种），所以外层是 **二重循环**，复杂度大约是 `O(n²)`（`n` 是字符串长度）。  
  - 对每一组 `(i, j)`，我们会一次遍历剩余的字符去验证，加上每次字符串相加的开销，总体时间大约是 `O(n³)`。  
  - 空间上只保存几个临时字符串和递归栈，最多 `O(n)`（递归深度不会超过 `n`）。

> 大白话解释：`O(n³)` 就是说如果字符串长度是 10，最坏情况下会做大概 10×10×10 = 1000 次基本操作；如果长度是 30，则是 27,000 次——随长度增长，耗时会“立方”增长。

#### 代码（Python）

```python
def isAdditiveNumber(num: str) -> bool:
    n = len(num)

    # 用来判断子串是否可以作为合法的数字（不能有前导零，除非本身就是 "0"）
    def valid(x: str) -> bool:
        return not (x.startswith('0') and len(x) > 1)

    # 递归尝试把剩余的字符串匹配成加法序列
    def backtrack(prev1: int, prev2: int, start: int) -> bool:
        # 已经匹配到字符串末尾，说明成功
        if start == n:
            return True
        # 计算下一个应该出现的数字
        target = prev1 + prev2
        target_str = str(target)
        # 检查从 start 开始的子串是否以 target_str 开头
        if num.startswith(target_str, start):
            # 匹配成功，继续向后递归
            return backtrack(prev2, target, start + len(target_str))
        return False

    # 枚举第一、第二个数的切分点
    for i in range(1, n):                 # first 的长度
        first = num[:i]
        if not valid(first):
            continue
        for j in range(i + 1, n):         # second 的结束位置
            second = num[i:j]
            if not valid(second):
                continue
            # 把字符串转成整数，交给递归检查后面的部分
            if backtrack(int(first), int(second), j):
                return True
    return False
```

**关键行中文注释**  
- `valid`：判断是否出现了非法的前导零。  
- `backtrack`：递归检查后面的字符是否能完整地形成加法序列。  
- `num.startswith(target_str, start)`：判断当前未匹配的部分是否正好以 **目标数字** 开头。  

#### 复杂度

- **时间复杂度**：`O(n³)`  
  - 两层循环枚举前两个数 `O(n²)`，每次递归最多遍历剩余字符 `O(n)`，所以乘起来是立方级别。  
- **空间复杂度**：`O(n)`  
  - 递归深度最多等于序列的长度（最坏情况每次只匹配一个数字），加上存放少量临时字符串的空间。

---

### 2. 最优解

#### 思路  

暴力解已经是 **全枚举**，但我们可以在枚举时加入**剪枝**，把不可能的分支提前剔除，从而把实际运行时间大幅降低。核心思路如下：

1. **限制第一、第二个数的长度**  
   - 因为后面的每一步都是前两数之和，若第一、第二个数已经太长，剩余字符根本容不下它们的和。  
   - 设 `len(first) = i`，`len(second) = j-i`，则 `i`、`j` 最多只需要遍历到 `n/2` 左右（经验上足够）。

2. **在递归时使用“前缀和”判断**  
   - 与其每次都把 `prev1 + prev2` 转成字符串再比较，不如直接在原始字符串上 **逐位相加**（手动实现大数相加），这样可以在加法过程中发现不匹配就立刻返回，避免生成完整的中间字符串。

3. **利用 Python 的大整数特性**  
   - Python 本身支持任意长度整数，直接使用 `int` 相加不会溢出。这里我们仍保留手动大数相加的思路，帮助读者理解 **“数字太大时手动相加”** 的技巧——这也是面试常考的点。

综上，最优解仍然是 **回溯（Backtracking）**，但加入了**长度剪枝**和**逐位相加的即时校验**，实际运行时间在多数测试里会接近 `O(n²)`。

> **核心算法**：回溯 + 大数相加（逐位校验）  
> **核心数据结构**：字符串切片、列表（用于保存加数的每一位）

#### 代码（Python）

```python
def isAdditiveNumber(num: str) -> bool:
    n = len(num)

    # 判断子串是否合法（不能有前导零）
    def valid(s: str) -> bool:
        return not (s.startswith('0') and len(s) > 1)

    # 手动实现大数相加，返回相加后的字符串（不依赖 Python int）
    def add_str(a: str, b: str) -> str:
        i, j = len(a) - 1, len(b) - 1
        carry = 0
        res = []
        while i >= 0 or j >= 0 or carry:
            digit = carry
            if i >= 0:
                digit += ord(a[i]) - ord('0')
                i -= 1
            if j >= 0:
                digit += ord(b[j]) - ord('0')
                j -= 1
            res.append(chr(digit % 10 + ord('0')))   # 余数转字符
            carry = digit // 10
        return ''.join(reversed(res))

    # 递归检查从 start 开始的子串是否能继续构成加法序列
    def dfs(first: str, second: str, start: int) -> bool:
        if start == n:                # 已经匹配完全部字符
            return True
        sum_str = add_str(first, second)   # 计算期望的下一个数字
        # 若剩余字符没有以 sum_str 开头，直接失败
        if not num.startswith(sum_str, start):
            return False
        # 成功匹配后，继续递归，以 (second, sum_str) 为新的前两数
        return dfs(second, sum_str, start + len(sum_str))

    # 枚举第一、第二个数的结束位置，加入长度剪枝
    # 第一段长度 i 最多不超过 n//2（否则后面根本容不下两个数的和）
    for i in range(1, n // 2 + 1):
        first = num[:i]
        if not valid(first):
            continue
        # 第二段长度 j-i 最多不超过 n//2 同理
        for j in range(i + 1, i + 1 + n // 2):
            if j >= n:
                break
            second = num[i:j]
            if not valid(second):
                continue
            if dfs(first, second, j):
                return True
    return False
```

**关键行中文注释**  
- `add_str`：手动实现大数相加，逐位相加并处理进位，返回结果字符串。  
- `dfs`：深度优先搜索，**即时**校验下一个数字是否匹配，若不匹配立刻返回 `False`，避免多余递归。  
- 循环的上限 `n // 2`：保证前两个数的长度不至于超过整体长度的一半，从而剪掉不可能的分支。

#### 复杂度

- **时间复杂度**：`O(n²)`（近似）  
  - 两层循环的枚举次数被 `n//2` 限制，最多约 `n²/4`。  
  - 每一次递归只做一次线性的大数相加和字符串比较，整体仍保持在二次级别。相较于暴力的立方级别有明显提升。  
- **空间复杂度**：`O(n)`  
  - 递归栈深度最多 `O(n)`，加上 `add_str` 生成的临时字符串同样不超过 `n`。

---

## 心得

- **核心技巧**：**回溯 + 大数相加（逐位校验）**。回溯负责枚举前两段，大数相加帮助在每一步即时判断是否匹配，从而提前剪枝。  
- **适用的题型**  
  1. “**Additive Number**” 系列（判断加法序列、返回序列本身等）。  
  2. “**Fibonacci‑like string**” 或 “**斐波那契字符串**” 类似的递推序列问题。  
  3. 需要**逐位相加**而整数可能超出语言原生范围的题目（如大数相加、乘法等）。  
- **一句话总结解题钥匙**：  
  “先把前两段固定下来，然后**每一步都立即算出下一个数并检查**，不匹配就立刻回溯。”

---

## 反思

- **第一反应**：看到“加法序列”，立刻想到“把前两个数拿出来，后面每次都算和”。于是自然想到回溯。  
- **最容易踩的坑**  
  - **前导零**：`"01"`、`"00"` 等都不合法，需要在切分时专门过滤。  
  - **长度剪枝不足**：如果不限制前两段的最大长度，枚举会爆炸。  
  - **大数溢出**：在某些语言里 `int` 会溢出，需要手动大数相加或使用语言自带的大整数类型。  
- **下次遇到同类题**：第一步先**限定前两段的可能长度**，并准备**逐位相加的检查函数**，这样可以在搜索时即时剔除不可能的分支。