# #2194. Excel 表格中单元格范围 / Cells in a Range on an Excel Sheet

> 难度：简单 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/cells-in-a-range-on-an-excel-sheet/)

---

## 题目（英文原版）

**Description**

A cell (r, c) of an excel sheet is represented as a string "<col><row>" where:
You are given a string s in the format "<col1><row1>:<col2><row2>", where <col1> represents the column c1, <row1> represents the row r1, <col2> represents the column c2, and <row2> represents the row r2, such that r1 <= r2 and c1 <= c2.
Return the list of cells (x, y) such that r1 <= x <= r2 and c1 <= y <= c2. The cells should be represented as strings in the format mentioned above and be sorted in non-decreasing order first by columns and then by rows.

**Examples**

**Example 1:**

```
Input: s = "K1:L2"
Output: ["K1","K2","L1","L2"]
Explanation:
The above diagram shows the cells which should be present in the list.
The red arrows denote the order in which the cells should be presented.
```

**Example 2:**

```
Input: s = "A1:F1"
Output: ["A1","B1","C1","D1","E1","F1"]
Explanation:
The above diagram shows the cells which should be present in the list.
The red arrow denotes the order in which the cells should be presented.
```

**Constraints**

- s.length == 5
- 'A' <= s[0] <= s[3] <= 'Z'
- '1' <= s[1] <= s[4] <= '9'
- s consists of uppercase English letters, digits and ':'.

---

## 题目（中文翻译）

**描述**  
Excel 表格中的一个单元格 (r, c) 用字符串 "`<col><row>`" 表示，其中 `<col>` 为列标，`<row>` 为行号。  
给定一个字符串 `s`，其格式为 "`<col1><row1>:<col2><row2>`"，其中 `<col1>` 表示列 `c1`，`<row1>` 表示行 `r1`，`<col2>` 表示列 `c2`，`<row2>` 表示行 `r2`，并满足 `r1 ≤ r2` 且 `c1 ≤ c2`。  
返回所有满足 `r1 ≤ x ≤ r2` 且 `c1 ≤ y ≤ c2` 的单元格 `(x, y)`。单元格需以上述字符串形式返回，并按**先列后行**的非递减顺序排序。

**示例 1**  
输入: `s = "K1:L2"`  
输出: `["K1","K2","L1","L2"]`  
**解释:**  
上图展示了应当出现在列表中的单元格。红色箭头表示单元格的出现顺序。

**示例 2**  
输入: `s = "A1:F1"`  
输出: `["A1","B1","C1","D1","E1","F1"]`  
**解释:**  
上图展示了应当出现在列表中的单元格。红色箭头表示单元格的出现顺序。

**约束条件**  
- `s.length == 5`  
- `'A' ≤ s[0] ≤ s[3] ≤ 'Z'`  
- `'1' ≤ s[1] ≤ s[4] ≤ '9'`  
- `s` 只包含大写英文字母、数字和字符 `':'`。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
把题目提供的范围 `"<col1><row1>:<col2><row2>"` 拆开，得到左上角的单元格和右下角的单元格。  
- **列** 用大写字母表示，`'A'`、`'B'`…`'Z'`，可以把它们想象成 **字典的键**，`ord('A')` 是 65，`ord('B')` 是 66…… 用 `ord` 减去 `ord('A')` 就得到 0、1、2…的序号，类似“查字典”得到页码。  
- **行** 是数字字符 `'1'`~`'9'`，直接转成整数即可。  

有了左上角 `(c1, r1)` 和右下角 `(c2, r2)`，最直接的办法就是 **双层循环**：  
1. 外层遍历列号 `c` 从 `c1` 到 `c2`（升序），  
2. 内层遍历行号 `r` 从 `r1` 到 `r2`（升序），  
3. 把每个 `(c, r)` 再转回字母+数字的形式加入结果列表。  

因为题目要求返回的顺序是“先列后行”，正好对应上述循环的顺序。  

**为什么正确**：  
- 题目保证 `c1 ≤ c2`、`r1 ≤ r2`，所以遍历的每一对 `(c, r)` 都在合法矩形内部。  
- 循环的遍历顺序恰好是“列升序 → 行升序”，与题目要求的排序一致。  

**复杂度大白话**：  
- 如果列跨度是 `Δc = c2 - c1 + 1`，行跨度是 `Δr = r2 - r1 + 1`，我们会访问 `Δc × Δr` 次，每一次都做常数时间的字符拼接和列表追加。  
- 用大 O 记号写就是 `O(Δc·Δr)`，这其实就是**输出的单元格数**，没有多余的计算。  

#### 代码（Python）  

```python
def cellsInRange(s: str) -> list[str]:
    """
    暴力枚举所有满足条件的单元格
    参数 s 形如 "K1:L2"
    返回 按列、行升序 排好的字符串列表
    """
    # 1. 把字符串用 ':' 分成左右两部分
    start, end = s.split(':')
    # 2. 解析列（字母）和行（数字）
    c1, r1 = start[0], int(start[1])          # 例如 'K', 1
    c2, r2 = end[0], int(end[1])              # 例如 'L', 2

    res = []                                   # 用来收集答案

    # 3. 外层遍历列，从 c1 到 c2（升序）
    for col_code in range(ord(c1), ord(c2) + 1):
        col_char = chr(col_code)               # 把 ASCII 码转回字母，如 75 -> 'K'
        # 4. 内层遍历行，从 r1 到 r2（升序）
        for row in range(r1, r2 + 1):
            cell = f"{col_char}{row}"          # 拼接成 "K1"、"K2"…
            res.append(cell)                   # 加入结果列表

    return res
```

#### 复杂度  

- **时间复杂度**：`O(Δc·Δr)` —— 实际上等于输出的单元格数。  
  *大白话*：如果要输出 10×5=50 个格子，就会花大约 50 步。  
- **空间复杂度**：`O(Δc·Δr)` —— 需要把所有格子存进列表返回。  
  *大白话*：返回的列表本身就占用了这么多空间。  

---  

### 2. 最优解  

#### 思路  
对于这道题，**暴力枚举已经是最优的**。因为答案本身就要把所有符合条件的单元格逐一列出来，任何算法都必须产生这些输出，时间下界就是 `Ω(输出个数)`。  
所以“优化”只能体现在**代码简洁度**和**常数因子**上：  

1. 直接把列、行的遍历写成 **列表推导式**（list comprehension），省去显式的 `append` 循环。  
2. 用 `chr` / `ord` 把字母和数字相互转换，一次性完成，不需要额外的数据结构（比如哈希表）。  

核心思路仍然是“**双指针**”：一个指针在列上前进，一个指针在行上前进。  

#### 代码（Python）  

```python
def cellsInRange(s: str) -> list[str]:
    """
    最简洁的实现：利用列表推导式一次性生成所有单元格
    """
    start, end = s.split(':')
    c1, r1 = start[0], int(start[1])
    c2, r2 = end[0], int(end[1])

    # 列的字母从 c1 到 c2，行的数字从 r1 到 r2
    return [
        f"{chr(col)}{row}"
        for col in range(ord(c1), ord(c2) + 1)   # 列循环
        for row in range(r1, r2 + 1)            # 行循环
    ]
```

#### 复杂度  

- **时间复杂度**：`O(Δc·Δr)` —— 与暴力解相同，因为必须生成同样数量的字符串。  
  与暴力解的区别在于常数更小（省去了 `append` 的函数调用），实际运行更快。  
- **空间复杂度**：`O(Δc·Δr)` —— 仍然是存放所有结果的列表。  

---  

## 心得  

- **核心技巧**：把字符（列）和数字（行）相互转换，然后使用双层循环（或列表推导式）按列、行的顺序枚举。  
- **适用的题型**  
  1. “矩形区域遍历”类题目，例如 LeetCode 59 `Spiral Matrix II`（螺旋遍历矩阵）  
  2. “坐标范围展开”类题目，例如 “All Cells in a Range on an Excel Sheet” 的变形  
  3. “字母数字组合生成”类，如生成所有可能的车牌号等。  
- **一句话总结**：**先把列字母映射成整数，再用两层循环/列表推导生成“列+行”组合，即是答案。**  

## 反思  

- **第一反应**：把输入字符串拆成起点和终点，分别取出列字母和行数字，然后逐个枚举。  
- **最容易踩的坑**  
  - **忘记把行字符转成整数**，导致循环比较时把 `'9'` 当成字符比较，顺序会出错。  
  - **列的范围不包括右端点**：`range(ord(c1), ord(c2))` 会少算最后一列，需要 `+1`。  
  - **返回顺序**：必须是先列后行，不能把行放在外层循环。  
- **下次遇到同类题**：第一步先 **把所有维度（列/行）映射成可比较的整数**，再 **按照题目要求的顺序用嵌套循环遍历**，最后把整数再映射回原始的字符形式。