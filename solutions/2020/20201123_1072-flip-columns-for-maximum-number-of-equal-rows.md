# #1072. 翻转列以获得最多相等行 / Flip Columns For Maximum Number of Equal Rows

> 难度：中等 · 标签：Array、Hash Table、Matrix · [LeetCode 链接](https://leetcode.com/problems/flip-columns-for-maximum-number-of-equal-rows/)

---

## 题目（英文原版）

**Description**

You are given an m x n binary matrix matrix.
You can choose any number of columns in the matrix and flip every cell in that column (i.e., Change the value of the cell from 0 to 1 or vice versa).
Return the maximum number of rows that have all values equal after some number of flips.

**Examples**

**Example 1:**

```
Input: matrix = [[0,1],[1,1]]
Output: 1
Explanation: After flipping no values, 1 row has all values equal.
```

**Example 2:**

```
Input: matrix = [[0,1],[1,0]]
Output: 2
Explanation: After flipping values in the first column, both rows have equal values.
```

**Example 3:**

```
Input: matrix = [[0,0,0],[0,0,1],[1,1,0]]
Output: 2
Explanation: After flipping values in the first two columns, the last two rows have equal values.
```

**Constraints**

- m == matrix.length
- n == matrix[i].length
- 1 <= m, n <= 300
- matrix[i][j] is either 0 or 1.

---

## 题目（中文翻译）

给定一个 `m × n` 的二进制矩阵（binary matrix）`matrix`。  
你可以选择矩阵中的任意若干列，并翻转（flip）该列中的每个单元格（即将单元格的值从 `0` 变为 `1`，或从 `1` 变为 `0`）。  
返回在进行任意次数的列翻转后，所有元素相等的行（row）的最大数量。

**示例 1**

```
Input: matrix = [[0,1],[1,1]]
Output: 1
Explanation: 不进行任何翻转时，有 1 行的所有值相等。
```

**示例 2**

```
Input: matrix = [[0,1],[1,0]]
Output: 2
Explanation: 翻转第一列后，两行的值全部相等。
```

**示例 3**

```
Input: matrix = [[0,0,0],[0,0,1],[1,1,0]]
Output: 2
Explanation: 翻转前两列后，最后两行的值全部相等。
```

**约束条件**

- `m == matrix.length`
- `n == matrix[i].length`
- `1 <= m, n <= 300`
- `matrix[i][j]` 仅为 `0` 或 `1`。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每一种可能的列翻转方式都穷举一遍**，然后看在该方式下有多少行全部相同（全 0 或全 1），取最大值即可。  

- **枚举列翻转方式**：一共有 `n` 列，每列可以“翻”也可以“不翻”。所以所有可能的组合数是 `2ⁿ`（类似把 `n` 把灯的开关全部打开或关闭的所有情况）。我们可以把每一种组合看成一个长度为 `n` 的二进制数组 `K`，`K[j]=1` 表示第 `j` 列要翻，`0` 表示不翻。  
- **判断一行是否统一**：对某一行 `row`，如果把 `K` 按位异或（XOR）到这行上，即 `row ^ K`，得到的新行如果全是 `0` 或全是 `1`，说明在这套翻转方案下，这行是“好行”。  
- **统计**：遍历所有行，统计好行的数量，记录最大值。

> **为什么这样一定能得到答案？**  
> 因为我们把 **所有可能的翻转方案** 都尝试了一遍，答案必然出现在这些方案之中。只要找到让最多行统一的方案，就是题目要求的最大行数。

#### 代码（Python）

```python
from itertools import product
from typing import List

def maxEqualRowsAfterFlips_bruteforce(matrix: List[List[int]]) -> int:
    m, n = len(matrix), len(matrix[0])
    best = 0                     # 记录目前找到的最大行数

    # 0/1 组合代表每列是否翻转，product 会生成 2^n 种组合
    for flips in product([0, 1], repeat=n):   # flips 是一个长度为 n 的元组
        cnt = 0                               # 统计在当前 flips 下有多少行统一
        for row in matrix:
            # 把当前翻转方案 XOR 到整行上
            transformed = [cell ^ f for cell, f in zip(row, flips)]
            # 检查 transformed 是否全是 0 或全是 1
            if all(v == 0 for v in transformed) or all(v == 1 for v in transformed):
                cnt += 1
        best = max(best, cnt)                 # 更新全局最大值
    return best
```

#### 复杂度  

- **时间复杂度**：`O(2^n * m * n)`  
  - `2^n` 是列翻转方案的数量。  
  - 对每种方案，我们要遍历 `m` 行，每行要遍历 `n` 列做异或和检查。  
  - **大白话**：如果矩阵有 10 列，`2^10 = 1024`，相当于要尝试 1024 次，每次都要检查所有格子，明显会慢。  

- **空间复杂度**：`O(1)`（不计输入矩阵本身）  
  - 只用了常数级别的额外变量 `flips`、`cnt`、`transformed`（临时列表大小为 `n`），不随 `m`、`n` 增长而增长。  

---

### 2. 最优解  

#### 思路  

暴力解的**瓶颈**在于“枚举所有列的翻转方式”，当列数 `n` 较大（题目最高 300）时，`2^n` 彻底不可接受。  
我们要寻找一种 **只遍历矩阵一次** 就能得到答案的办法。  

观察：

1. **翻转列的本质是对每一行做同样的异或操作**  
   把某个列翻一次，相当于把这列所在的所有行的该位都取反。若把若干列一起翻，就相当于把一个固定的二进制向量 `K`（长度为 `n`）和每行做 XOR。  

2. **统一的行只能是“全 0”或“全 1”**  
   假设在某个翻转方案 `K` 下，第 `i` 行变成了全 0，则原始的第 `i` 行满足 `row_i ^ K = 0…0`，即 `row_i = K`。  
   同理，如果第 `i` 行变成了全 1，则 `row_i ^ K = 1…1`，即 `row_i = ¬K`（按位取反的 K）。  

3. **结论**：  
   两行如果**要么完全相同，要么完全相反**（即每个位置的值相反），它们就可以在同一个翻转方案下同时变成全 0（或全 1）。  

   换句话说，**只要把每行“统一”到以第一列为基准的形式，就能把能一起统一的行归为同一类**。  
   - 若某行的第一列是 `0`，保持不变；  
   - 若第一列是 `1`，把整行取反（相当于假设我们已经翻了第一列）。  

   经过这样“标准化”后，所有可以在同一方案下统一的行会得到 **完全相同的模式**。  
   因此，只需要统计出现次数最多的这种模式的行数，即为答案。

4. **实现细节**  
   - 用一个哈希表（Python 的 `dict`）统计每种标准化模式出现的次数。  
   - 标准化时不必真的去翻列，只要把行的每个元素与该行的首元素异或即可：`norm[j] = row[j] ^ row[0]`。  
   - 把 `norm`（元组形式）作为哈希表的键，计数。  
   - 最终答案是哈希表中最大计数。  

> **类比**：把每行想象成一本书的章节标题。如果第一章是“正面”，我们把整本书的所有标题都统一为“正面”；如果第一章是“负面”，我们把整本书的标题全部翻转为“正面”。这样所有标题相同的书就可以一次性“统一”。  

#### 代码（Python）

```python
from collections import Counter
from typing import List

def maxEqualRowsAfterFlips(matrix: List[List[int]]) -> int:
    """
    最优解：只遍历一次矩阵，利用哈希表统计“标准化”后的行模式。
    """
    cnt = Counter()                     # 用来统计每种模式出现的次数
    for row in matrix:
        # 以该行第一个元素为基准，把整行“标准化”。如果 row[0]==0，norm 与 row 相同；
        # 如果 row[0]==1，则每个位置都取反（异或 1），相当于假设我们已经翻了第一列。
        norm = tuple(cell ^ row[0] for cell in row)   # 转成 tuple 方便哈希
        cnt[norm] += 1                                 # 计数

    # 出现次数最多的模式，就是可以在同一翻转方案下统一的最大行数
    return max(cnt.values())
```

#### 复杂度  

- **时间复杂度**：`O(m * n)`  
  - 只遍历矩阵一次，对每个元素做一次异或（常数时间），总共 `m·n` 次操作。  
  - 与暴力解的 `2^n` 相比，线性时间在 `m,n ≤ 300` 的范围内毫无压力。  

- **空间复杂度**：`O(m)`（最坏情况每行的标准化模式都不相同）  
  - 哈希表最多保存 `m` 条记录，每条记录的键长度为 `n`（但实际存的是引用），因此额外空间与行数成正比。  
  - 相比暴力解的 `O(1)`，这里用了额外的字典，但在本题规模下完全可接受。  

---

## 心得  

- **核心技巧**：把“列翻转”转化为“对每行统一做异或”，并利用**行之间的相等或相反**关系归类。  
- **适用的题型**：  
  1. “行/列翻转后使矩阵满足某种统一性质”的题目（如 *Flip Columns For Maximum Number of Equal Rows*）。  
  2. “把每行视为二进制数，找出最多相同或相反的行”类题目（如 *Maximum Equal Row after Flips*）。  
  3. “按某一基准把数组/字符串标准化后统计出现次数”类题目（如 *Group Anagrams* 的变形）。  
- **一句话总结**：**把所有行统一到同一个“基准”下，统计出现最多的基准即可**。  

---

## 反思  

- **第一反应**：直接想到枚举所有列的翻转方式（暴力），因为题目说“可以翻任意列”。  
- **最容易踩的坑**：  
  - 忘记“全 0”和“全 1”都算合法统一，需要同时考虑这两种情况。  
  - 在实现时误把行的标准化方式写成 `cell ^ row[0]` 的相反方向，导致计数错误。  
  - 对空矩阵或只有一列的特殊情况没有做好边界检查（本题约束已经保证 `m,n ≥ 1`）。  
- **下次类似题目**的第一步思考：**先找出“翻转操作对每行的影响是统一的”，再把问题转化为“行之间的相等/相反关系”。** 这一步往往能把指数级搜索压缩到线性遍历。