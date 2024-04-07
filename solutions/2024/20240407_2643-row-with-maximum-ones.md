# #2643. 拥有最多 1 的行 / Row With Maximum Ones

> 难度：简单 · 标签：Array、Matrix · [LeetCode 链接](https://leetcode.com/problems/row-with-maximum-ones/)

---

## 题目（英文原版）

**Description**

Given a m x n binary matrix mat, find the 0-indexed position of the row that contains the maximum count of ones, and the number of ones in that row.
In case there are multiple rows that have the maximum count of ones, the row with the smallest row number should be selected.
Return an array containing the index of the row, and the number of ones in it.

**Examples**

**Example 1:**

```
Input: mat = [[0,1],[1,0]]
Output: [0,1]
Explanation: Both rows have the same number of 1's. So we return the index of the smaller row, 0, and the maximum count of ones (1). So, the answer is [0,1].
```

**Example 2:**

```
Input: mat = [[0,0,0],[0,1,1]]
Output: [1,2]
Explanation: The row indexed 1 has the maximum count of ones (2). So we return its index, 1, and the count. So, the answer is [1,2].
```

**Example 3:**

```
Input: mat = [[0,0],[1,1],[0,0]]
Output: [1,2]
Explanation: The row indexed 1 has the maximum count of ones (2). So the answer is [1,2].
```

**Constraints**

- m == mat.length
- n == mat[i].length
- 1 <= m, n <= 100
- mat[i][j] is either 0 or 1.

---

## 题目（中文翻译）

给定一个 **m × n** 的二进制矩阵 `mat`，找出包含 **1** 的数量最多的那一行的 **0** 起始下标，以及该行中 **1** 的个数。  
如果有多行拥有相同的最大 **1** 的数量，则返回下标最小的那一行。  
返回一个数组，其中第一个元素是行的下标，第二个元素是该行的 **1** 的个数。

**示例 1:**  
**示例 2:**  
**示例 3:**  

### 示例

#### 示例 1
**输入:** `mat = [[0,1],[1,0]]`  
**输出:** `[0,1]`  
**解释:** 两行的 **1** 的数量相同，均为 1。因此返回下标较小的行 0，以及最大 **1** 的数量 1，答案为 `[0,1]`。

#### 示例 2
**输入:** `mat = [[0,0,0],[0,1,1]]`  
**输出:** `[1,2]`  
**解释:** 下标为 1 的行拥有最多的 **1**（共 2 个），所以返回其下标 1 和数量 2，答案为 `[1,2]`。

#### 示例 3
**输入:** `mat = [[0,0],[1,1],[0,0]]`  
**输出:** `[1,2]`  
**解释:** 下标为 1 的行拥有最多的 **1**（共 2 个），答案为 `[1,2]`。

### 约束条件
- `m == mat.length`
- `n == mat[i].length`
- `1 <= m, n <= 100`
- `mat[i][j]` 只能是 `0` 或 `1`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把矩阵每一行都拿出来，**逐个数**该行里有多少个 `1`，然后把「最多 `1` 的行」记录下来。

- **用到的数据结构**：二维列表 `mat` 本身就是我们要遍历的容器。  
  - 把每一行看成一本**字典**，行号是词条（key），行里 `1` 的数量是对应的解释（value）。我们只需要把每本字典的解释数出来，找出最大值即可。  
- **为什么正确**：因为题目要求的正是「哪一行的 `1` 最多」以及「具体有多少个 `1`」。只要把每行的 `1` 全部数一遍，就一定能得到真实的最大值和对应的行号。  
- **时间/空间复杂度**：  
  - **时间**：我们要遍历所有 `m` 行，每行遍历 `n` 列，最坏情况下要检查 `m × n` 次元素，记作 **O(m·n)**。  
    - 大白话：如果矩阵是 100×100，最坏要检查 10,000 次，这就是 O(10⁴)。  
  - **空间**：只需要几个额外的整数（记录当前最大行号、最大 `1` 的个数），不随输入规模增长，记作 **O(1)**（常数空间）。

#### 代码（Python）

```python
from typing import List

def rowAndMaximumOnes(mat: List[List[int]]) -> List[int]:
    """
    暴力遍历每一行，统计 1 的个数，记录最大值所在的行号
    """
    max_ones = -1          # 当前发现的最大 1 的数量，初始设为 -1 方便第一次更新
    max_row = -1           # 对应的行号

    for i, row in enumerate(mat):          # i 是行号，row 是该行的列表
        count = 0
        for val in row:                    # 逐个检查该行的每个元素
            if val == 1:
                count += 1                 # 统计 1 的数量
        # 如果当前行的 1 比之前的最多的多，或者相等但行号更小，就更新答案
        if count > max_ones:
            max_ones = count
            max_row = i
        # 当 count == max_ones 时不更新，因为我们要保留最小的行号

    return [max_row, max_ones]
```

#### 复杂度  

- **时间复杂度**：O(m·n) — 需要检查矩阵里每一个元素一次。  
- **空间复杂度**：O(1) — 只用了常数个额外变量。

---

### 2. 最优解

#### 思路  

对这道题目来说，**暴力解已经是最优的**。原因如下：

1. **瓶颈在哪里**  
   - 我们唯一需要的信息是每行中 `1` 的总数。无论采用什么技巧，都必须**看到**每一行的每一个元素，才能确定该行到底有多少个 `1`。  
   - 没有额外的结构（比如每行已经排好序）可以让我们跳过检查某些元素。

2. **一步步推导**  
   - 如果矩阵的每行都是“先 0 后 1”排好的（即 **单调递增**），可以从右上角用 “左移/下移” 的方式一次遍历完所有行，时间降到 O(m+n)。  
   - 但题目并未给出这种排序保证，所以我们只能逐行逐列检查。

3. **核心算法/数据结构**  
   - **一次遍历 + 计数**：只需要两层循环，外层遍历行，内层遍历列并计数。  
   - **常数空间**：用几个整数保存当前最大值和对应行号。

4. **类比**  
   - 想象我们在一个 **电影院**，每排座位上有人坐（`1`）或空（`0`），想知道哪一排坐得最多。我们只能逐排走过去数坐的人，不能跳过某排，因为每排的坐姿是随意的。

因此，这里给出的实现已经是 **时间 O(m·n)、空间 O(1)** 的最优解。

#### 代码（Python）

```python
from typing import List

def rowAndMaximumOnes_opt(mat: List[List[int]]) -> List[int]:
    """
    单次遍历即可得到答案，时间 O(m·n)，空间 O(1)。
    """
    max_row, max_ones = -1, -1          # 初始化答案

    for i, row in enumerate(mat):
        # Python 的内置 sum 可以直接统计列表中 1 的个数，等价于手动计数
        count = sum(row)                # O(n) 的一次遍历

        # 更新最大值和对应行号
        if count > max_ones:
            max_row, max_ones = i, count
        # 当 count == max_ones 时不更新，保持最小行号

    return [max_row, max_ones]
```

#### 复杂度  

- **时间复杂度**：O(m·n) — 必须检查所有元素，已无法进一步降低。  
- **空间复杂度**：O(1) — 只用了固定的几个变量。

---

## 心得

- **核心技巧**：对每行进行一次完整计数，使用 `sum` 或手动遍历即可。  
- **适用的题型**：  
  1. “矩阵中出现最多的元素行/列” 类题目（如 `Row With Maximum Sum`）。  
  2. “统计二维数组中满足某条件的行/列” （如 `Count Negative Numbers in a Grid`）。  
- **解题钥匙**：**遍历 + 计数**——只要把需要的统计信息全部算出来，再比较取最大/最小即可。

---

## 反思

- **第一反应**：直接想到“遍历每行，数 1 的个数”，这就是暴力思路。  
- **最容易踩的坑**：  
  - 忘记在出现相同最大 `1` 数时保留 **最小行号**（要在 `>` 而不是 `>=` 时更新）。  
  - 对空矩阵或行长度为 0 的情况没有做好防护（本题约束保证至少有一行一列）。  
- **下次遇到同类题**：第一步先 **明确统计目标**（是行、列还是整体），然后决定是逐行/列遍历还是利用已有的排序/单调性做优化。若没有额外信息，**一次完整遍历**往往是最稳妥的方案。