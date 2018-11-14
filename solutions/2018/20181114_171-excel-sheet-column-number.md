# #171. Excel 表列编号 / Excel Sheet Column Number

> 难度：简单 · 标签：Math、String · [LeetCode 链接](https://leetcode.com/problems/excel-sheet-column-number/)

---

## 题目（英文原版）

**Description**

Given a string columnTitle that represents the column title as appears in an Excel sheet, return its corresponding column number.
For example:

**Examples**

**Example 1:**

```
A -> 1
B -> 2
C -> 3
...
Z -> 26
AA -> 27
AB -> 28 
...
```

**Example 2:**

```
Input: columnTitle = "A"
Output: 1
```

**Example 3:**

```
Input: columnTitle = "AB"
Output: 28
```

**Example 4:**

```
Input: columnTitle = "ZY"
Output: 701
```

**Constraints**

- 1 <= columnTitle.length <= 7
- columnTitle consists only of uppercase English letters.
- columnTitle is in the range ["A", "FXSHRXW"].

---

## 题目（中文翻译）

给定一个字符串列标题（columnTitle），它表示 Excel 表格中出现的列标题，返回其对应的列编号（column number）。

**示例 1**  
A → 1  
B → 2  
C → 3  
…  
Z → 26  
AA → 27  
AB → 28  
…

**示例 2**  
输入: `columnTitle = "A"`  
输出: `1`

**示例 3**  
输入: `columnTitle = "AB"`  
输出: `28`

**示例 4**  
输入: `columnTitle = "ZY"`  
输出: `701`

**约束条件**

- `1 <= columnTitle.length <= 7`
- `columnTitle` 仅由大写英文字母组成。
- `columnTitle` 的取值范围在 `["A", "FXSHRXW"]` 之间。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接、最笨的办法是把 **所有可能的 Excel 列标题** 按顺序枚举出来，直到出现和输入 `columnTitle` 相同的那一个，统计它是第几次出现，就得到对应的列号。  

- **数据结构**：可以把已经生成的标题放进一个列表（list），列表就像一本“词典”，每加入一个新词（标题），它的下标（从 0 开始）+1 就是列号。  
- **为什么正确**：Excel 的列标题本身就是一种 **26 进制的递增序列**（A, B, …, Z, AA, AB, …），只要把序列完整地走一遍，必定会在正确的位置遇到 `columnTitle`，此时计数器的值就是答案。  
- **复杂度分析**：  
  - 假设标题长度为 `n`，所有长度 ≤ n 的标题总数约为 `26 + 26² + … + 26ⁿ = (26ⁿ⁺¹‑26)/25`，也就是 **指数级**，记作 **O(26ⁿ)**。  
  - 空间上我们把这些标题都存下来，需要同样数量的空间，故 **O(26ⁿ)**。  
  - 用大白话说：如果标题只有 2 位（最多 26²=676 种），我们要生成 676 个字符串；如果是 5 位，就要生成 26⁵≈1.2 千万个——明显不可接受。

#### 代码（Python）  
```python
def titleToNumber_bruteforce(columnTitle: str) -> int:
    # 用来保存已经生成的标题，类似“词典”
    generated = []          # [] 代表目前还没有任何标题

    # 递归生成所有长度为 1~len(columnTitle) 的标题
    def dfs(current: str, max_len: int):
        if len(current) == max_len:
            generated.append(current)
            return
        for ch in map(chr, range(ord('A'), ord('Z') + 1)):
            dfs(current + ch, max_len)

    # 逐层增长长度，模拟 Excel 从 A 开始的顺序
    for length in range(1, len(columnTitle) + 1):
        dfs("", length)      # 生成所有 length 位的标题

    # 遍历生成的列表，找到第一个等于 columnTitle 的位置
    for idx, title in enumerate(generated, start=1):  # start=1 把下标转成列号
        if title == columnTitle:
            return idx
    # 理论上不会走到这里，因为题目保证 columnTitle 合法
    return -1
```
> **关键行中文注释**  
> - `generated`：像字典一样保存所有已经生成的标题。  
> - `dfs`：深度优先搜索，逐字符拼接生成标题。  
> - `enumerate(..., start=1)`：从 1 开始计数，直接得到列号。

#### 复杂度  
- **时间复杂度**：`O(26ⁿ)` — 需要生成并检查指数级数量的字符串，`n` 为标题长度。  
- **空间复杂度**：`O(26ⁿ)` — 把所有生成的标题都保存在列表里，同样是指数级。  

---

### 2. 最优解  

#### 思路  
从暴力解可以看到 **枚举** 是最慢的环节。其实我们并不需要把所有标题列出来，只要直接把标题当作 **26 进制的数** 来计算即可。  

- **瓶颈**：暴力解把每个可能的标题都显式生成，时间和空间都爆炸。  
- **优化思路**：  
  1. 把每个字符当成一位“数字”。在 Excel 中，`A → 1, B → 2, …, Z → 26`（注意没有 0）。  
  2. 从左到右累加：`result = result * 26 + value_of_current_char`。这和我们平时把十进制字符串转整数的过程完全相同，只是进位基数从 10 变成了 26。  
- **核心算法**：**进制转换**（把 26 进制的“字母数”转成十进制的列号）。  
- **类比**：把 Excel 的列标题想象成一本书的章节号，例如 “AB” 就像 “第 1 章第 2 小节”。先算出第 1 章对应的基数（`1 * 26`），再加上第 2 小节的编号（`2`），得到总的章节号 `28`。  

#### 代码（Python）  
```python
def titleToNumber(columnTitle: str) -> int:
    """
    把 Excel 列标题当作 26 进制数转换为十进制列号
    """
    result = 0                       # 最终答案，先设为 0
    for ch in columnTitle:           # 从左到右遍历每个字母
        digit = ord(ch) - ord('A') + 1   # 把字母转成 1~26 的数值
        result = result * 26 + digit     # 进制位累加：旧值 * 26 + 当前位
    return result
```
> **关键行中文注释**  
> - `ord(ch) - ord('A') + 1`：把字符 `'A'~'Z'` 映射到 `1~26`。`ord` 相当于查字典得到字符的 Unicode 编码。  
> - `result = result * 26 + digit`：相当于把已有的高位左移一位（乘以 26），再放入当前位的值。

#### 复杂度  
- **时间复杂度**：`O(n)` — 只遍历一次字符串，`n` 为标题长度（最多 7），几乎瞬间完成。  
- **空间复杂度**：`O(1)` — 只用了几个整数变量，和输入长度无关。  

---

## 心得  

- **核心技巧**：把字母序列视作 **26 进制数字**，使用进制转换的思路一次遍历即可求出列号。  
- **适用题型**：  
  1. “Excel Sheet Column Title” （把列号转标题）  
  2. “Base‑7 / Base‑8 / Base‑k 转十进制” 类似的进制转换题目  
  3. “把字母映射为数字求和” 如 “Roman to Integer” 也是类似的映射+累加思路。  
- **一句话总结**：**把标题当作没有 0 的 26 进制数，左移乘 26 再加当前字符值**。  

---

## 反思  

- **第一反应**：看到 `A → 1, Z → 26, AA → 27`，立刻联想到 **进制**，于是想到把字符转成数字后累加。  
- **最容易踩的坑**：  
  - 忘记 Excel 的进制是 **1‑26**，而不是 **0‑25**，所以要在 `ord` 计算后加 `+1`。  
  - 输入可能只有一位字符，仍需按照同样的公式处理，不能单独写特殊分支。  
  - 字符串长度虽小（≤ 7），但如果把结果放进 32 位整数要注意不会溢出（实际最大值 `FXSHRXW` 对应 2 147 483 647，正好在 32 位有符号整数范围内）。  
- **下次类似题的第一步**：先判断 **是否可以把字符/符号映射为数值并按某个基数累加**，如果可以，直接用进制转换的模板写出 O(n) 解法。