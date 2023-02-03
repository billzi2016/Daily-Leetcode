# #2116. 检查括号字符串是否可以有效 / Check if a Parentheses String Can Be Valid

> 难度：中等 · 标签：String、Stack、Greedy · [LeetCode 链接](https://leetcode.com/problems/check-if-a-parentheses-string-can-be-valid/)

---

## 题目（英文原版）

**Description**

A parentheses string is a non-empty string consisting only of '(' and ')'. It is valid if any of the following conditions is true:
You are given a parentheses string s and a string locked, both of length n. locked is a binary string consisting only of '0's and '1's. For each index i of locked,
Return true if you can make s a valid parentheses string. Otherwise, return false.

**Examples**

**Example 1:**

```
Input: s = "))()))", locked = "010100"
Output: true
Explanation: locked[1] == '1' and locked[3] == '1', so we cannot change s[1] or s[3].
We change s[0] and s[4] to '(' while leaving s[2] and s[5] unchanged to make s valid.
```

**Example 2:**

```
Input: s = "()()", locked = "0000"
Output: true
Explanation: We do not need to make any changes because s is already valid.
```

**Example 3:**

```
Input: s = ")", locked = "0"
Output: false
Explanation: locked permits us to change s[0]. 
Changing s[0] to either '(' or ')' will not make s valid.
```

**Example 4:**

```
Input: s = "(((())(((())", locked = "111111010111"
Output: true
Explanation: locked permits us to change s[6] and s[8]. 
We change s[6] and s[8] to ')' to make s valid.
```

**Constraints**

- n == s.length == locked.length
- 1 <= n <= 105
- s[i] is either '(' or ')'.
- locked[i] is either '0' or '1'.

---

## 题目（中文翻译）

一个括号字符串（parentheses string）是只包含字符 '(' 和 ')' 的非空字符串。如果满足以下任意条件，则该字符串是有效的：

给定一个长度为 `n` 的括号字符串 `s` 与同样长度的字符串 `locked`。`locked` 是只包含 `'0'` 和 `'1'` 的二进制字符串。对于每个索引 `i`：

- 当 `locked[i] == '1'` 时，位置 `i` 上的字符 **不能** 被修改；
- 当 `locked[i] == '0'` 时，位置 `i` 上的字符 **可以** 任意改为 '(' 或 ')'。

返回 `true` 当且仅当可以通过修改所有可修改的位置，使得 `s` 成为一个有效的括号字符串；否则返回 `false`。

## 示例

### 示例 1
**输入**  
` s = "))()))", locked = "010100" `  

**输出**  
` true `  

**解释**  
`locked[1] == '1'` 且 `locked[3] == '1'`，因此无法修改 `s[1]` 和 `s[3]`。  
我们把 `s[0]` 和 `s[4]` 改为 '('，保持 `s[2]` 和 `s[5]` 不变，得到的字符串是有效的。

### 示例 2
**输入**  
` s = "()()", locked = "0000" `  

**输出**  
` true `  

**解释**  
无需做任何修改，因为 `s` 本身已经是有效的括号字符串。

### 示例 3
**输入**  
` s = ")", locked = "0" `  

**输出**  
` false `  

**解释**  
`locked` 允许我们修改 `s[0]`。  
无论把 `s[0]` 改成 '(' 还是 ')'，都无法得到有效的括号字符串。

### 示例 4
**输入**  
` s = "(((())(((())", locked = "111111010111" `  

**输出**  
` true `  

**解释**  
`locked` 允许我们修改 `s[6]` 和 `s[8]`。  
我们把 `s[6]`、`s[8]` 改为 ')'，即可使字符串有效。

## 约束条件

- `n == s.length == locked.length`
- `1 <= n <= 10^5`
- `s[i]` 只能是 `'('` 或 `')'`
- `locked[i]` 只能是 `'0'` 或 `'1'`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有 **可以改动** 的字符（`locked[i] == '0'`）枚举出来，尝试每一种改成 `'('` 或 `')'` 的可能性，检查改完以后整串是否满足“有效括号串”的定义。  

- **数据结构**：  
  - 用一个列表 `idx` 保存所有可改动位置的下标，就像在字典里查找“哪些词可以随意改”。  
  - 递归（或循环）遍历 `idx`，每访问一个下标，就把它当成 `'('` 或 `')'` 两种情况分别继续搜索。  

- **为什么正确**：  
  - 只要遍历了所有可能的改动方式，就一定会碰到一种恰好能让字符串合法的改法（如果存在的话），因此只要找到一种合法的，就返回 `True`。  

- **复杂度**：  
  - 设可改动的字符数为 `k`，每个位置有两种选择，所以总共要检查 `2^k` 种情况。  
  - `O(2^k)` 在实际中是 **指数级** 的增长，哪怕 `k = 20`（约一百万种）也会让程序在几秒钟内超时。  
  - 空间方面，需要保存递归栈深度 `k`，即 `O(k)`。  

> **大白话**：  
> 把每个可以动的字符想成一把可以随意开关的灯，全部灯一起开关完所有组合再看灯光是否能拼成一幅合法的图形——这显然太费力了。

#### 代码（Python）

```python
def checkValidString_bruteforce(s: str, locked: str) -> bool:
    n = len(s)
    # 收集所有可以改动的位置
    free_idx = [i for i, c in enumerate(locked) if c == '0']

    def is_valid(t: str) -> bool:
        """判断字符串 t 是否是合法的括号串（普通的线性扫描）"""
        bal = 0          # 当前左括号的数量
        for ch in t:
            if ch == '(':
                bal += 1
            else:        # ')'
                bal -= 1
            if bal < 0:  # 右括号多于左括号，必不合法
                return False
        return bal == 0

    # 深度优先遍历所有可能的改动方式
    def dfs(pos: int, cur: list) -> bool:
        if pos == len(free_idx):            # 所有可改位置都已经决定
            return is_valid(''.join(cur))
        i = free_idx[pos]                   # 当前要决定的下标
        # 方案1：把它改成 '('
        cur[i] = '('
        if dfs(pos + 1, cur):
            return True
        # 方案2：改成 ')'
        cur[i] = ')'
        if dfs(pos + 1, cur):
            return True
        # 恢复原样（对后面的递归没有影响，但写的更直观）
        cur[i] = s[i]
        return False

    # 用原始字符串做起点，随后在递归里就地修改
    return dfs(0, list(s))
```

> 这段代码可以直接跑通小规模测试，但在 `n` 达到上限 `10^5` 时会因为 `2^k` 的爆炸式增长而超时。

#### 复杂度  

- **时间复杂度**：`O(2^k * n)`，其中 `k` 为可改动字符数。指数级增长，实际不可接受。  
- **空间复杂度**：`O(k + n)`，递归栈深度 `k` 加上保存字符数组的 `n`。  

---

### 2. 最优解  

#### 思路  

**从暴力解出发**，我们发现瓶颈在于“每次都要枚举所有可能”。  
其实我们并不需要真的去枚举，而是可以 **利用可改动位置的灵活性**，在遍历字符串时“尽量把它们当成有利的括号”。  

关键观察：

1. **奇数长度不可能合法**  
   有效括号串的左括号数必等于右括号数，所以字符总数必须是偶数。  

2. **从左到右的检查**  
   - 当遇到 **锁定的 `')'`** 时，它必须被左边的某个 `'('`（锁定或可改）抵消。  
   - 为了让抵消的机会最大，我们可以把所有 **可改的字符** 暂时当成 `'('`（因为 `'('` 能帮助平衡右括号）。  
   - 维护一个 **balance**（左括号的“余额”），`'('` → `+1`，`')'` → `-1`。  
   - 如果在遍历过程中 `balance` 变成负数，说明左侧根本没有足够的左括号来平衡当前的右括号，**无论怎么改动后面的字符都救不回来**，直接返回 `False`。  

3. **从右到左的检查**（对称）  
   - 同理，遍历时把所有 **可改的字符** 当成 `')'`（因为从右往左看，右括号相当于“左括号”）。  
   - 用另一个 `balance`（这次 `'')'` → `+1`，`'('` → `-1`）。  
   - 若 `balance` 变负，说明右侧没有足够的右括号来抵消左括号，同样返回 `False`。  

4. **两遍都通过，则一定可以构造合法串**  
   - 左→右保证**没有左侧缺少左括号**的情况。  
   - 右→左保证**没有右侧缺少右括号**的情况。  
   - 这两条同时成立，说明我们可以把所有可改字符恰当地分配为 `'('` 或 `')'`，从而得到合法串。  

**类比**：  
把锁定字符想成 **固定的砖块**，只能按原样摆放；把可改字符想成 **可随意旋转的积木**，我们在左→右遍历时把它们全部当成 “向左撑起的支柱”（`'('`），在右→左遍历时把它们全部当成 “向右撑起的支柱”（`')'`）。只要两次检查都不出现“支柱不足”的情况，就一定能把积木摆成稳固的桥。

#### 代码（Python）

```python
def checkValidString(s: str, locked: str) -> bool:
    n = len(s)
    # 1️⃣ 奇数长度必不合法
    if n % 2 == 1:
        return False

    # 2️⃣ 左→右遍历，尽量把 unlocked 当 '('
    balance = 0          # 左括号的“剩余量”
    for i in range(n):
        if locked[i] == '1':          # 锁定的字符只能按原样计数
            if s[i] == '(':
                balance += 1
            else:                     # ')'
                balance -= 1
        else:                         # unlocked，假设它是 '('
            balance += 1
        # 只要左侧的 '(' 不够抵消出现的 ')'
        if balance < 0:
            return False

    # 3️⃣ 右→左遍历，尽量把 unlocked 当 ')'
    balance = 0          # 这次的 “右括号余量”
    for i in range(n - 1, -1, -1):
        if locked[i] == '1':
            if s[i] == ')':
                balance += 1
            else:                     # '('
                balance -= 1
        else:                         # unlocked，假设它是 ')'
            balance += 1
        if balance < 0:               # 右侧缺少足够的 ')' 来匹配 '('
            return False

    # 两遍都没有出现负 balance，说明可以配成合法串
    return True
```

> 代码每行都配有中文注释，直接复制到编辑器即可运行。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历字符串两遍，线性时间。与暴力的 `2^k` 相比，快得多。  
- **空间复杂度**：`O(1)`  
  - 只使用了若干整数变量，不随 `n` 增长而增加。  

---

## 心得  

- **核心技巧**：**双向贪心 + 把可改字符当成最有利的那一类**。  
- **适用的题型**（类似思路）：  
  1. **LeetCode 2116** – *Check if a Parentheses String Can Be Valid*（本题）。  
  2. **LeetCode 1812** – *Maximum Score of a Good Subarray*（需要从两端维护可调节的窗口）。  
  3. **LeetCode 1650** – *Lowest Common Ancestor of a Binary Tree III*（在遍历时利用“灵活”节点的特性）。  
- **一句话总结解题钥匙**：  
  > 把“可以随意改动的字符”视作**最有帮助的括号**，分别从左到右、从右到左检查是否出现“左侧缺左括号”或“右侧缺右括号”的情况。

---

## 反思  

- **第一反应**：立刻想到枚举所有可能（暴力搜索），因为最直观的做法就是“把每个 0 位改成 '(' 或 ')'”。  
- **最容易踩的坑**：  
  - 忽略 **奇数长度** 必然不合法的前置条件，导致在奇数输入上仍继续检查而出错。  
  - 在左→右遍历时把 unlocked 当成 `')'`（或右→左时相反），会导致判断过于保守，错误地返回 `False`。  
  - 忽视 **两遍都要检查** 的必要性，只做左→右或只做右→左会漏掉某些非法情况。  
- **下次类似题目**，第一步应该：  
  1. 检查长度的奇偶性。  
  2. 确定“固定”与“可变”字符的角色。  
  3. 用 **从左到右**（或 **从右到左**）的 **贪心** 思路，尽量让可变字符帮助平衡当前不匹配的括号，检查是否出现“余额不足”的情况。  

这样即可在 O(n) 时间内快速判断答案。