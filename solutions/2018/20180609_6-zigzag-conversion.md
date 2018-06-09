# #6. Z字形变换 / Zigzag Conversion

> 难度：中等 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/zigzag-conversion/)

---

## 题目（英文原版）

**Description**

The string "PAYPALISHIRING" is written in a zigzag pattern on a given number of rows like this: (you may want to display this pattern in a fixed font for better legibility)
And then read line by line: "PAHNAPLSIIGYIR"
Write the code that will take a string and make this conversion given a number of rows:

**Examples**

**Example 1:**

```
P   A   H   N
A P L S I I G
Y   I   R
```

**Example 2:**

```
string convert(string s, int numRows);
```

**Example 3:**

```
Input: s = "PAYPALISHIRING", numRows = 3
Output: "PAHNAPLSIIGYIR"
```

**Example 4:**

```
Input: s = "PAYPALISHIRING", numRows = 4
Output: "PINALSIGYAHRPI"
Explanation:
P     I    N
A   L S  I G
Y A   H R
P     I
```

**Example 5:**

```
Input: s = "A", numRows = 1
Output: "A"
```

**Constraints**

- 1 <= s.length <= 1000
- s consists of English letters (lower-case and upper-case), ',' and '.'.
- 1 <= numRows <= 1000

---

## 题目（中文翻译）

**题目描述**  
字符串 `"PAYPALISHIRING"` 按照给定的行数以之字形（zigzag）模式写成如下图所示的形式（为保证可读性，可使用等宽字体显示）：

然后按行读取得到 `"PAHNAPLSIIGYIR"`。  
请编写代码，实现将任意字符串按照指定的行数进行上述之字形转换。

**函数签名**  
```cpp
string convert(string s, int numRows);
```

**示例**  

示例 1：  
```
P   A   H   N
A P L S I I G
Y   I   R
```

示例 2：  
函数签名如上所示。

示例 3：  
输入: `s = "PAYPALISHIRING", numRows = 3`  
输出: `"PAHNAPLSIIGYIR"`

示例 4：  
输入: `s = "PAYPALISHIRING", numRows = 4`  
输出: `"PINALSIGYAHRPI"`  
**解释**：  
```
P     I    N
A   L S  I G
Y A   H R
P     I
```

示例 5：  
输入: `s = "A", numRows = 1`  
输出: `"A"`

**约束条件**  
- `1 <= s.length <= 1000`  
- `s` 只包含英文大小写字母、逗号（,）和句点（.）。  
- `1 <= numRows <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **把字符真的按 Z 字形排好，再把每一行读出来**。  
我们可以把每一行想成一条“纸带”，用一个长度为 `numRows` 的列表 `rows` 来保存每条纸带的内容。  
遍历原字符串 `s` 时，先从上往下依次往每条纸带写字符（相当于把字母往“下楼梯”走），写到最底部后，再反方向往上写（相当于“爬坡”），如此循环往复，直到所有字符都写完。  
这跟我们在生活中把东西放进不同的抽屉，然后按顺序把抽屉里的东西取出来的过程是一致的——**抽屉 = 行，抽屉里的内容 = 该行的字符**。

实现细节：

1. 特判 `numRows == 1`，此时 Z 字形退化成一行，直接返回原串。  
2. 用 `rows = [''] * numRows` 初始化每行的字符串。  
3. 用两个变量控制**方向**和**当前行号**：  
   - `cur_row` 表示现在写到哪一行。  
   - `going_down` 为布尔值，`True` 表示向下走，`False` 表示向上走。  
4. 遍历 `s` 中的每个字符 `c`：  
   - 把 `c` 加到 `rows[cur_row]` 的末尾。  
   - 若到了第一行或最后一行，就把 `going_down` 取反（相当于碰到墙要掉头）。  
   - 根据 `going_down` 更新 `cur_row`（向下 `+1`，向上 `-1`）。  
5. 最后把所有行的字符串拼接起来，即得到答案。

这个方法**一定正确**，因为它完整地模拟了题目描述的排版过程，没有遗漏或多写任何字符。

#### 代码（Python）

```python
def convert(s: str, numRows: int) -> str:
    # 特例：只有一行时，直接返回原字符串
    if numRows == 1 or numRows >= len(s):
        return s

    # 用列表保存每一行的字符，初始都是空串
    rows = [''] * numRows

    cur_row = 0          # 当前写入的行号
    going_down = False   # 初始方向向下（第一次进入循环时会翻转）

    for ch in s:
        rows[cur_row] += ch          # 把字符放到对应的“抽屉”里

        # 碰到第一行或最后一行就要掉头
        if cur_row == 0 or cur_row == numRows - 1:
            going_down = not going_down

        # 根据方向决定下一行是往上还是往下
        cur_row += 1 if going_down else -1

    # 把所有行的内容合并成最终答案
    return ''.join(rows)
```

#### 复杂度

- **时间复杂度**：`O(n)`（`n` 为字符串长度）  
  只遍历了一遍字符，每个字符的处理都是 O(1) 的常数时间。  
  “O(n)” 可以想象成“走一遍所有字符，需要的步数正比于字符个数”。

- **空间复杂度**：`O(min(n, numRows))`  
  需要保存每行的字符，总共最多保存 `numRows` 条字符串，最坏情况下每行可能只放一个字符，实际占用的空间与 `numRows` 成正比；如果 `numRows` 大于 `n`，则只会用到 `n` 条行（每行一个字符），所以取两者的最小值。

---

### 2. 最优解

#### 思路  

暴力解已经是 **线性时间、线性空间** 的最优时间复杂度了（不可能比 `O(n)` 更快，因为必须看每个字符）。  
但我们可以从 **“为什么需要 `rows` 列表？”** 入手，进一步压缩空间，使得只用 **O(1) 额外空间**（不计输出字符串本身）来完成转换。

**关键观察**：

- 当我们把字符按照 Z 字形排好后，读取顺序其实是**先把所有在第 0 行的字符取出来**，再第 1 行，第 2 行……  
- 对于第 `i` 行（`0 <= i < numRows`），它的字符出现的间隔是有规律的：  
  - **第一行和最后一行**（`i = 0` 或 `i = numRows-1`）的字符之间的间隔都是 `cycle_len = 2 * (numRows - 1)`。  
  - **中间行**（`0 < i < numRows-1`）的字符出现两种间隔交替出现：  
    - `down_gap = cycle_len - 2 * i`（从当前行向下走到下一次回到该行的间隔）  
    - `up_gap   = 2 * i`（从当前行向上走到下一次回到该行的间隔）  
  - 这两个间隔交替出现，形成“下‑上‑下‑上”的节奏。

**基于上述规律**，我们可以不需要额外的 `rows` 列表，而是直接在原字符串上**按行遍历**，把对应的字符直接写进结果字符串中。

实现步骤：

1. 处理特例 `numRows == 1`（退化成一行）。  
2. 计算 `cycle_len = 2 * (numRows - 1)`，这是完整的一个 Z 字形周期的长度。  
3. 创建一个列表 `res_chars = []` 用于收集结果字符（等价于最终的字符串）。  
4. 对每一行 `i`（从 0 到 `numRows-1`）做：
   - 设 `j = i` 为该行第一个字符在原串中的下标。  
   - 当 `j < len(s)` 时：
     - 把 `s[j]` 加入结果。  
     - 对于第一行或最后一行，只需要跳 `cycle_len`（因为中间没有“上‑下”交替）。  
     - 对于中间行，需要先跳 `down_gap`，再跳 `up_gap`，交替进行。  
5. 最后把 `res_chars` 合并成字符串返回。

这样做的 **空间** 只用了一个存放结果的列表（输出本身），不再需要 `numRows` 条额外的字符串，符合 **O(1) 额外空间** 的要求。

#### 代码（Python）

```python
def convert(s: str, numRows: int) -> str:
    # 特例：只有一行时直接返回原字符串
    if numRows == 1 or numRows >= len(s):
        return s

    cycle_len = 2 * (numRows - 1)          # 一个完整 Z 字形的字符数
    res_chars = []                         # 用列表收集字符，最后一次性 join

    for i in range(numRows):               # 按行遍历
        j = i                               # 当前行第一个字符在原串中的下标
        while j < len(s):
            # 当前字符一定属于第 i 行
            res_chars.append(s[j])

            # 对第一行和最后一行，只需要一个间隔
            if i == 0 or i == numRows - 1:
                j += cycle_len
            else:
                # 中间行有两个交替的间隔
                down_gap = cycle_len - 2 * i   # 向下走的间隔
                up_gap   = 2 * i               # 向上走的间隔

                # 先向下跳（如果还有字符）
                j += down_gap
                if j >= len(s):
                    break
                res_chars.append(s[j])

                # 再向上跳
                j += up_gap

    return ''.join(res_chars)
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  每个字符被访问恰好一次（或在中间行时被访问两次，但仍是常数次数），整体仍是线性时间。  
  与暴力解相比，**没有额外的遍历**，只是把遍历顺序从“逐字符”改为“逐行”，时间上等价。

- **空间复杂度**：`O(1)`（不计输出）  
  除了返回的结果字符串外，只用了常数个整数变量（`cycle_len`, `i`, `j`, `down_gap`, `up_gap`），不随输入规模增长。  
  这比暴力解的 `O(numRows)` 额外空间更省。

---

## 心得

- **核心技巧**：利用 Z 字形的周期性规律，**按行直接跳步**。  
- **适用场景**：任何需要“按固定模式分块读取”或“周期性跳跃”的字符串/数组题目，例如  
  1. **字符串交叉合并**（把两段交叉取字符）  
  2. **交错数组遍历**（如把二维矩阵按对角线顺序输出）  
  3. **编码/解码中的周期性映射**（如凯撒密码的变形）  
- **一句话总结**：**找出字符出现的固定间隔，用数学跳步代替真实排版**。

---

## 反思

- **第一反应**：把字符真的画出来排排看，最直观。  
- **最容易踩的坑**：  
  - `numRows == 1` 或 `numRows >= len(s)` 时忘记直接返回，会导致除以 0 或产生错误的循环间隔。  
  - 中间行的两段间隔必须交替使用，写成固定间隔会漏掉字符。  
  - 循环结束条件要小心，防止越界访问。  
- **下次遇到类似题**：先**写出排版的周期**（比如 `cycle_len`），再**思考每行的跳步**，把“画图”转化为“算数”。