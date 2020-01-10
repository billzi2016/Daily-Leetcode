# #726. 原子计数 / Number of Atoms

> 难度：困难 · 标签：Hash Table、String、Stack、Sorting · [LeetCode 链接](https://leetcode.com/problems/number-of-atoms/)

---

## 题目（英文原版）

**Description**

Given a string formula representing a chemical formula, return the count of each atom.
The atomic element always starts with an uppercase character, then zero or more lowercase letters, representing the name.
One or more digits representing that element's count may follow if the count is greater than 1. If the count is 1, no digits will follow.
Two formulas are concatenated together to produce another formula.
A formula placed in parentheses, and a count (optionally added) is also a formula.
Return the count of all elements as a string in the following form: the first name (in sorted order), followed by its count (if that count is more than 1), followed by the second name (in sorted order), followed by its count (if that count is more than 1), and so on.
The test cases are generated so that all the values in the output fit in a 32-bit integer.

**Examples**

**Example 1:**

```
Input: formula = "H2O"
Output: "H2O"
Explanation: The count of elements are {'H': 2, 'O': 1}.
```

**Example 2:**

```
Input: formula = "Mg(OH)2"
Output: "H2MgO2"
Explanation: The count of elements are {'H': 2, 'Mg': 1, 'O': 2}.
```

**Example 3:**

```
Input: formula = "K4(ON(SO3)2)2"
Output: "K4N2O14S4"
Explanation: The count of elements are {'K': 4, 'N': 2, 'O': 14, 'S': 4}.
```

**Constraints**

- 1 <= formula.length <= 1000
- formula consists of English letters, digits, '(', and ')'.
- formula is always valid.

---

## 题目（中文翻译）

给定一个字符串 `formula`，表示一个化学式（chemical formula），返回每种原子（atom）的计数。  
原子名称总是以大写字母开头，后面可以跟零个或多个小写字母，构成元素名。  
如果该元素的计数大于 1，则其后会跟随一个或多个数字表示计数；计数为 1 时则不写数字。  
两个化学式可以直接相连，形成另一个化学式。  
将一个化学式放在括号 `(`、`)` 中，并在后面可选地添加一个计数，同样视为一个化学式。  

返回所有元素的计数，格式为一个字符串：先写字母顺序排序后的第一个元素名，若计数大于 1 则紧跟其计数；再写第二个元素名，同样计数大于 1 时写出计数；依此类推。  

测试用例保证输出中的所有计数均能放入 32 位整数。

**示例 1**  
输入: `formula = "H2O"`  
输出: `"H2O"`  
解释: 元素计数为 `{'H': 2, 'O': 1}`。

**示例 2**  
输入: `formula = "Mg(OH)2"`  
输出: `"H2MgO2"`  
解释: 元素计数为 `{'H': 2, 'Mg': 1, 'O': 2}`。

**示例 3**  
输入: `formula = "K4(ON(SO3)2)2"`  
输出: `"K4N2O14S4"`  
解释: 元素计数为 `{'K': 4, 'N': 2, 'O': 14, 'S': 4}`。

**约束条件**  
- `1 <= formula.length <= 1000`  
- `formula` 仅由英文字母、数字、`(`、`)` 组成。  
- `formula` 必定是合法的化学式。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把化学式从左到右**一次遍历**，把每个原子及其数量记下来。  
- **原子名**：大写字母开头，后面可能跟若干小写字母。可以把它想象成「词典」里的词，**查字典**时先看到大写字母，再往后读小写字母，直到遇到不是小写字母为止。  
- **数量**：原子名后面可能跟一串数字，表示该原子的个数。如果没有数字，则默认数量为 1。数字的读取可以像“数数”，从左到右一直读到不是数字的字符为止。  
- **括号**：遇到 '(' 时，先把括号内部当成一个独立的子公式递归处理，得到子公式内部每种原子的计数。随后再读取括号后面的数字（如果有），把子公式的计数全部乘上这个数字。  

把所有计数放进一个 **哈希表**（在 Python 中就是 `dict`），键是原子名，值是累计的数量。哈希表就像一本**查字典的手册**，我们可以随时通过原子名（key）快速找到它的当前计数（value），不需要遍历整个列表。

**为什么这个方法一定能得到正确答案？**  
- 公式的语法是严格的：每个原子一定以大写字母开头，括号一定成对，数字一定是正整数。我们把公式拆解成「原子+数量」或「子公式+乘数」的最小单元，然后把每个单元的计数加到全局哈希表里，所有出现的原子都会被统计一次，且不会遗漏或重复计数。

**时间/空间复杂度的“大白话”**  
- **时间复杂度 O(n²)**：每次递归都要在字符串中**重新定位**对应的右括号位置（需要一次线性扫描），最坏情况下会出现 **嵌套 n/2 层** 的括号，导致总的扫描次数接近 `1 + 2 + … + n/2 = O(n²)`。可以把它想象成在一条长队里，每次都要从头重新数到指定位置，次数会很多。  
- **空间复杂度 O(n)**：递归栈最深可能达到公式长度的数量级（每遇到一个 '(' 就进栈一次），以及哈希表里最多会出现 `O(n)` 种不同的原子名。

#### 代码（Python）  
```python
def countOfAtoms(formula: str) -> str:
    """
    暴力递归版：每次遇到 '(' 都向后扫描一次寻找配对的 ')'
    """
    n = len(formula)

    # 读取从 i 开始的连续数字，返回数字以及下一个未读取的位置
    def parse_number(i: int):
        if i >= n or not formula[i].isdigit():
            return 1, i          # 没有数字，默认 1
        num = 0
        while i < n and formula[i].isdigit():
            num = num * 10 + int(formula[i])
            i += 1
        return num, i

    # 读取从 i 开始的原子名（大写字母 + 若干小写字母）
    def parse_atom(i: int):
        start = i
        i += 1                     # 第一个一定是大写字母
        while i < n and formula[i].islower():
            i += 1                 # 读取所有后续的小写字母
        return formula[start:i], i

    # 递归解析子公式，返回 (计数字典, 结束位置)
    def parse(i: int):
        counts = {}                # 当前层级的原子计数
        while i < n and formula[i] != ')':
            if formula[i] == '(':
                # 递归解析括号内部
                sub_counts, i = parse(i + 1)   # i+1 跳过 '('
                mul, i = parse_number(i)       # 读取括号后的乘数
                # 把子公式的计数乘上 mul 加到当前层
                for atom, cnt in sub_counts.items():
                    counts[atom] = counts.get(atom, 0) + cnt * mul
            else:
                atom, i = parse_atom(i)         # 读取原子名
                mul, i = parse_number(i)        # 读取数量
                counts[atom] = counts.get(atom, 0) + mul
        return counts, i + 1   # 跳过右括号 ')'

    total_counts, _ = parse(0)

    # 按字典序输出
    parts = []
    for atom in sorted(total_counts):
        cnt = total_counts[atom]
        parts.append(atom + (str(cnt) if cnt > 1 else ""))
    return "".join(parts)
```

#### 复杂度  
- **时间复杂度：O(n²)** — 每次遇到 '(' 都要向后线性扫描找配对的 ')'，最坏情况会出现二次遍历。  
- **空间复杂度：O(n)** — 递归栈深度和哈希表大小均与公式长度成正比。

---  

### 2. 最优解  

#### 思路  
从暴力解可以看到，**瓶颈在于每次都要重新扫描找配对的括号**。如果我们在一次遍历中就把括号匹配的信息保存下来，就可以避免二次扫描。  
实现思路：**用栈**一次遍历完成全部工作。  

1. **栈的作用**  
   - 想象一个装有「计数表」的盒子堆。遇到 '(' 时，说明要进入一个新的子公式，于是把当前计数表压入栈，打开一个空的计数表来统计子公式。  
   - 当遇到 ')' 时，说明子公式结束，弹出栈顶的「父公式计数表」并把子公式的计数乘上紧随 ')' 的数字（如果有），再合并回父公式计数表。  

2. **遍历过程**（一次线性扫描）  
   - **读原子名**：同暴力解，用大写字母 + 小写字母。  
   - **读数字**：同上，默认 1。  
   - **遇 '('**：把当前计数表（`defaultdict(int)`）压栈，重新创建一个空计数表。  
   - **遇 ')'**：先读取后面的数字 `mul`（默认 1），把当前计数表的每个原子计数乘以 `mul`，然后弹出栈顶的父计数表，把乘好的子计数合并进去。  

3. **为什么一次遍历就能完成？**  
   - 栈天然记录了「当前所在的层级」信息。每读完一个字符，我们都能立即决定是把计数加到哪一层，而不需要再去找匹配的括号位置。  

4. **核心数据结构解释**  
   - **哈希表（dict / defaultdict）**：存放 `atom -> count`，查找和更新都是 O(1)。  
   - **栈（list 充当栈）**：后进先出，帮助我们在进入/退出括号时保存和恢复计数表。可以把它想象成**层层叠放的盒子**，每打开一个括号就往上放一个新盒子，闭合时把盒子里的东西倒回下面的盒子。

#### 代码（Python）  
```python
from collections import defaultdict

def countOfAtoms(formula: str) -> str:
    """
    最优解：一次遍历 + 栈
    时间复杂度 O(n) ，空间复杂度 O(n)
    """
    n = len(formula)
    i = 0                       # 当前指针

    # 读取从 i 开始的连续数字，返回数字以及下一个未读取的位置
    def parse_number() -> int:
        nonlocal i
        if i >= n or not formula[i].isdigit():
            return 1            # 默认乘数为 1
        num = 0
        while i < n and formula[i].isdigit():
            num = num * 10 + int(formula[i])
            i += 1
        return num

    # 读取从 i 开始的原子名（大写 + 若干小写）
    def parse_atom() -> str:
        nonlocal i
        start = i
        i += 1                 # 第一个字符一定是大写
        while i < n and formula[i].islower():
            i += 1
        return formula[start:i]

    stack = []                 # 栈中保存父层的计数表
    cur = defaultdict(int)    # 当前层的计数表

    while i < n:
        ch = formula[i]
        if ch == '(':
            # 进入子公式：把当前计数表压栈，重新开始一个空计数表
            stack.append(cur)
            cur = defaultdict(int)
            i += 1
        elif ch == ')':
            i += 1                     # 跳过 ')'
            mul = parse_number()      # 读取括号后的乘数（默认 1）
            # 把当前层的计数乘以 mul
            for atom in cur:
                cur[atom] *= mul
            # 合并到父层
            parent = stack.pop()
            for atom, cnt in cur.items():
                parent[atom] += cnt
            cur = parent              # 恢复为父层计数表
        else:
            # 读取原子名和后面的数量
            atom = parse_atom()
            cnt = parse_number()
            cur[atom] += cnt

    # 最后 cur 即为全局计数表
    # 按字典序输出
    parts = []
    for atom in sorted(cur):
        cnt = cur[atom]
        parts.append(atom + (str(cnt) if cnt > 1 else ""))
    return "".join(parts)
```

#### 复杂度  
- **时间复杂度：O(n)** — 只遍历一次字符串，每个字符的处理都是常数时间。相当于“一次性把所有信息都装进了背包”。  
- **空间复杂度：O(n)** — 最坏情况下所有字符都是 '('，栈深度会达到 `n/2`，计数表的键数也不会超过 `n`，因此使用的额外空间与公式长度成线性关系。

---  

## 心得  

- **核心技巧**：**栈 + 哈希表**，用于处理带层级结构的字符串（如括号嵌套）。  
- **适用的题型**  
  1. **基本括号匹配**（如 LeetCode 20 Valid Parentheses）  
  2. **表达式求值**（如 LeetCode 224 Basic Calculator）  
  3. **带嵌套结构的计数**（如本题 Number of Atoms）  
- **一句话总结解题钥匙**：**“遇到 '(' 开新层，遇到 ')' 合并并乘系数，始终用栈记录层级”**。

---  

## 反思  

- **第一反应**：把公式拆成「原子」和「子公式」两类，递归处理。  
- **最容易踩的坑**  
  - **数字为空**时忘记默认乘数/计数为 1。  
  - **多位数字**的读取不完整，只读取了第一位。  
  - **括号后没有数字**的情况，需要默认乘以 1。  
  - **原子名可能有多个小写字母**（如 `Mg`、`Uuo`），不能只读取一个字符。  
- **下次类似题的第一步**：先判断「当前字符是 '('、')' 还是字母”，决定是 **打开新层**、**关闭层并合并**，还是 **读取原子名**，并统一使用 **栈** 来保存层级信息。