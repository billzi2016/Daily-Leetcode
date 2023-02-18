# #2133. 检查每行每列是否包含所有数字 / Check if Every Row and Column Contains All Numbers

> 难度：简单 · 标签：Array、Hash Table、Matrix · [LeetCode 链接](https://leetcode.com/problems/check-if-every-row-and-column-contains-all-numbers/)

---

## 题目（英文原版）

**Description**

An n x n matrix is valid if every row and every column contains all the integers from 1 to n (inclusive).
Given an n x n integer matrix matrix, return true if the matrix is valid. Otherwise, return false.

**Examples**

**Example 1:**

```
Input: matrix = [[1,2,3],[3,1,2],[2,3,1]]
Output: true
Explanation: In this case, n = 3, and every row and column contains the numbers 1, 2, and 3.
Hence, we return true.
```

**Example 2:**

```
Input: matrix = [[1,1,1],[1,2,3],[1,2,3]]
Output: false
Explanation: In this case, n = 3, but the first row and the first column do not contain the numbers 2 or 3.
Hence, we return false.
```

**Constraints**

- n == matrix.length == matrix[i].length
- 1 <= n <= 100
- 1 <= matrix[i][j] <= n

---

## 题目（中文翻译）

**描述**  
一个 n × n 的矩阵如果每一行和每一列都恰好包含从 1 到 n（inclusive）的所有整数，则称该矩阵为有效矩阵。给定一个 n × n 的整数矩阵 `matrix`，如果矩阵有效返回 `true`，否则返回 `false`。

**示例 1:**  
**示例 2:**  
**约束条件:**  

**示例**

**示例 1:**  
Input: matrix = [[1,2,3],[3,1,2],[2,3,1]]  
Output: true  
Explanation: 在此例中，n = 3，且每一行和每一列都包含数字 1、2、3。因此返回 `true`。

**示例 2:**  
Input: matrix = [[1,1,1],[1,2,3],[1,2,3]]  
Output: false  
Explanation: 在此例中，n = 3，但第一行和第一列缺少数字 2 或 3。因此返回 `false`。

**约束条件**  
- n == matrix.length == matrix[i].length  
- 1 ≤ n ≤ 100  
- 1 ≤ matrix[i][j] ≤ n

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**逐行、逐列检查**，看每一行和每一列里出现的数字集合是否正好是 `{1,2,…,n}`。  

- **用到的数据结构**：  
  - **集合（set）**：像查字典一样，往里面放数字，重复的数字会自动被“合并”。集合的大小 `len(set)` 就能告诉我们有多少种不同的数字。  
- **为什么正确**：  
  - 题目要求每行、每列都恰好出现 `1~n`，只要我们把该行（或列）所有元素放进集合，若集合大小恰好等于 `n`，说明这 `n` 个位置里没有缺漏也没有多余的数字。  
- **复杂度分析**（大白话解释）：  
  - 我们要遍历 **每一行**（`n` 行），每行里要遍历 **每个元素**（`n` 个），所以总共要看 `n × n` 次元素——这叫 **O(n²)**，即“随矩阵规模的平方而增长”。  
  - 集合本身最多装 `n` 个数字，空间上额外需要 `O(n)` 的空间（每检查一行或一列时只保留一个集合），整体空间是 **O(n)**。

#### 代码（Python）

```python
def checkValid(matrix):
    """
    暴力检查：逐行、逐列使用 set
    """
    n = len(matrix)                     # 矩阵的规模

    # 检查每一行
    for i in range(n):
        row_set = set()                 # 像字典一样收集本行出现的数字
        for j in range(n):
            row_set.add(matrix[i][j])   # 把第 i 行第 j 列的数字放进集合
        if len(row_set) != n:           # 集合大小不等于 n → 缺数字或有重复
            return False

    # 检查每一列
    for j in range(n):
        col_set = set()                 # 收集本列出现的数字
        for i in range(n):
            col_set.add(matrix[i][j])
        if len(col_set) != n:
            return False

    return True                         # 所有行列都满足条件
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 解释：我们遍历了 `n` 行 + `n` 列，每行/列内部又遍历了 `n` 个元素，总共大约 `2·n·n` 次操作，数量随 `n` 的平方增长。
- **空间复杂度**：`O(n)`  
  - 解释：一次只用到一个集合，最多装 `n` 个不同的数字，空间随 `n` 线性增长。

---

### 2. 最优解

#### 思路  
从暴力解可以看到，**遍历次数已经是最低的 `n²`**（因为必须看到每个元素一次），所以真正的“瓶颈”在于**集合的创建和哈希开销**。我们可以把集合换成**长度为 n 的布尔数组**（或 Python 中的列表）来记录数字是否出现过，这样：

- 插入/查询都是 **O(1)** 的数组下标操作，常数更小；
- 不需要哈希函数，省去一点额外的时间；
- 仍然只需要额外的 `O(n)` 空间。

实现步骤：

1. 对每一行，创建一个长度为 `n+1` 的布尔列表 `seen`（下标 `k` 表示数字 `k` 是否出现）。遍历该行的每个数字 `x`，把 `seen[x]` 设为 `True`。遍历结束后检查 `seen[1:]` 是否全部为 `True`。
2. 同理，对每一列做同样的检查。

> **为什么用 `n+1` 长度**：因为数字范围是 `1~n`，下标 `0` 我们直接不使用，保持代码直观。

#### 代码（Python）

```python
def checkValid(matrix):
    """
    使用布尔数组代替集合，减少常数时间开销
    """
    n = len(matrix)

    # 检查每一行
    for i in range(n):
        seen = [False] * (n + 1)        # seen[k] 表示数字 k 是否出现过
        for j in range(n):
            val = matrix[i][j]
            if seen[val]:               # 已经出现过 → 重复，直接返回 False
                return False
            seen[val] = True
        # 此时若有未出现的数字，seen 中会有 False，直接检查
        if not all(seen[1:]):           # all() 用来判断列表里所有元素是否都为 True
            return False

    # 检查每一列
    for j in range(n):
        seen = [False] * (n + 1)
        for i in range(n):
            val = matrix[i][j]
            if seen[val]:
                return False
            seen[val] = True
        if not all(seen[1:]):
            return False

    return True
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 与暴力解相同，因为每个元素仍然只能看一次。不过这里的每一步都是纯数组下标操作，实际运行更快。
- **空间复杂度**：`O(n)`  
  - 每次检查行或列时只用一个长度为 `n+1` 的布尔数组，空间仍然随 `n` 线性增长。

---

## 心得

- **核心技巧**：**使用集合或布尔数组检查出现的数字是否完整**。这是一种“全出现检查”常见模式。
- **适用题型**：
  1. 判断数独（Sudoku）中每行/列/子宫格是否合法。  
  2. 判断排列（Permutation）数组是否包含 `1~n`。  
  3. 检查一个字符串中是否出现所有英文字母（pangram）。
- **一句话总结解题钥匙**：**把“是否出现”抽象成“集合/布尔数组”，一次遍历即可完整验证**。

---

## 反思

- **第一反应**：看到“每行每列都要包含 1~n”，立刻想到“逐行、逐列收集元素”，于是使用集合实现最直接的检查。
- **最容易踩的坑**：
  - **忘记检查重复**：仅看集合大小可能漏掉同一个数字出现多次但缺少其他数字的情况（不过集合本身会去重，这里不是问题，但在布尔数组实现时需要显式判断 `seen[val]` 是否已为 `True`）。  
  - **边界条件**：`n = 1` 时仍需正确返回 `True`；矩阵中数值可能恰好等于 `n`，所以布尔数组要长度 `n+1`，否则会出现索引越界。  
- **下次遇到同类题**：第一步先 **“确定检查范围（行/列/子结构）”，再决定使用 **集合** 还是 **布尔数组** 来记录出现情况**，这样可以快速得到 O(n²) 的正确解法。