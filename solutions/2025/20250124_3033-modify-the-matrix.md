# #3033. 修改矩阵 / Modify the Matrix

> 难度：简单 · 标签：Array、Matrix · [LeetCode 链接](https://leetcode.com/problems/modify-the-matrix/)

---

## 题目（英文原版）

**Description**

Given a 0-indexed m x n integer matrix matrix, create a new 0-indexed matrix called answer. Make answer equal to matrix, then replace each element with the value -1 with the maximum element in its respective column.
Return the matrix answer.

**Examples**

**Example 1:**

```
Input: matrix = [[1,2,-1],[4,-1,6],[7,8,9]]
Output: [[1,2,9],[4,8,6],[7,8,9]]
Explanation: The diagram above shows the elements that are changed (in blue).
- We replace the value in the cell [1][1] with the maximum value in the column 1, that is 8.
- We replace the value in the cell [0][2] with the maximum value in the column 2, that is 9.
```

**Example 2:**

```
Input: matrix = [[3,-1],[5,2]]
Output: [[3,2],[5,2]]
Explanation: The diagram above shows the elements that are changed (in blue).
```

**Constraints**

- m == matrix.length
- n == matrix[i].length
- 2 <= m, n <= 50
- -1 <= matrix[i][j] <= 100
- The input is generated such that each column contains at least one non-negative integer.

---

## 题目（中文翻译）

给定一个 **0 索引** 的 `m x n` 整数矩阵 `matrix`，创建一个同样 **0 索引** 的新矩阵 `answer`。先令 `answer` 与 `matrix` 相同，然后将 `answer` 中每个值为 `-1` 的元素替换为其所在列的最大元素。返回矩阵 `answer`。

**示例 1**  
**示例 2**  
**约束条件**：

- `m == matrix.length`
- `n == matrix[i].length`
- `2 <= m, n <= 50`
- `-1 <= matrix[i][j] <= 100`
- 输入保证每一列至少包含一个非负整数。

---

### 示例

#### 示例 1
**输入**  
```json
matrix = [[1,2,-1],[4,-1,6],[7,8,9]]
```
**输出**  
```json
[[1,2,9],[4,8,6],[7,8,9]]
```
**解释**：上图中用蓝色标记的元素被修改。  
- 将单元格 `[1][1]` 的值替换为第 1 列的最大值 `8`。  
- 将单元格 `[0][2]` 的值替换为第 2 列的最大值 `9`。

#### 示例 2
**输入**  
```json
matrix = [[3,-1],[5,2]]
```
**输出**  
```json
[[3,2],[5,2]]
```
**解释**：上图中用蓝色标记的元素被修改。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每一个值为 -1 的格子单独处理**：

1. 找到矩阵中所有等于 -1 的位置 `(i, j)`。  
2. 对于每个这样的位置，**遍历它所在的整列 `j`**，找出该列的最大元素（因为题目保证每列至少有一个非负数，最大值一定是非负的）。  
3. 把 `(i, j)` 处的 -1 替换成刚才找到的最大值。

> 类比：把矩阵想成一本《通讯录》，每一列就是一本“姓氏簿”。我们要把标记为 “未知” (‑1) 的人的电话号码改成该姓氏簿里出现的 **最大** 电话号码。暴力做法就是每次遇到 “未知” 时，翻遍整本簿子找最大号码。

**为什么正确**  
- 题目要求把每个 -1 替换成**同一列的最大元素**，只要我们把对应列的所有元素都看一遍，找到最大值，再替换即可。  
- 每一次替换都不影响其它列的最大值（因为我们只读取原矩阵的值），所以逐个处理不会出错。

#### 代码（Python）

```python
from typing import List

def modifyMatrix_bruteforce(matrix: List[List[int]]) -> List[List[int]]:
    m, n = len(matrix), len(matrix[0])          # 行数、列数
    answer = [row[:] for row in matrix]        # 深拷贝，防止修改原矩阵

    for i in range(m):
        for j in range(n):
            if answer[i][j] == -1:             # 找到需要替换的格子
                # 暴力遍历整列 j，找最大值
                col_max = answer[0][j]         # 先假设第一行是最大值
                for k in range(1, m):
                    if answer[k][j] > col_max:
                        col_max = answer[k][j]
                answer[i][j] = col_max          # 用最大值替换 -1
    return answer
```

#### 复杂度  

- **时间复杂度**：`O(m * n * m)`，即 `O(m²·n)`。  
  - 外层两层循环遍历所有格子是 `O(m·n)`。  
  - 每遇到一个 -1，还要再遍历一遍所在列（最多 `m` 次），最坏情况每个格子都是 -1，导致整体 `O(m·n·m)`。  
  - 用大白话说，就是**“矩阵的每一行每一列都要被重复检查好几遍”**，所以会慢。

- **空间复杂度**：`O(m·n)` 用于存放 `answer` 的拷贝（题目要求返回一个新矩阵），其它变量都是常数级别。  

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**重复遍历同一列是浪费**。如果我们提前把每一列的最大值算好，后面再遇到 -1 时直接查表替换，就不需要再遍历列了。

优化步骤：

1. **一次性遍历矩阵**，记录每一列的最大值。  
   - 用一个长度为 `n` 的列表 `col_max`，`col_max[j]` 保存第 `j` 列的最大元素。  
   - 因为题目保证每列至少有一个非负数，直接用 `max` 比较即可。  
2. 再次遍历矩阵，对每个 -1 直接用 `col_max[j]` 替换。  
   - 只需要 **两次完整的遍历**（一次找最大值，一次替换），不再有嵌套的列遍历。

> 类比：把每列的最大值先记在一本“小抄”里（`col_max`），以后要把 “未知” 改成最大值时，只要翻开小抄看一眼就行了，不必再去翻整本簿子。

#### 代码（Python）

```python
from typing import List

def modifyMatrix(matrix: List[List[int]]) -> List[List[int]]:
    m, n = len(matrix), len(matrix[0])

    # 第一步：计算每一列的最大值
    col_max = [float('-inf')] * n               # 初始化为负无穷
    for i in range(m):
        for j in range(n):
            if matrix[i][j] > col_max[j]:       # 更新第 j 列的最大值
                col_max[j] = matrix[i][j]

    # 第二步：生成答案矩阵并进行替换
    answer = [row[:] for row in matrix]         # 深拷贝
    for i in range(m):
        for j in range(n):
            if answer[i][j] == -1:              # 只处理 -1 的位置
                answer[i][j] = col_max[j]       # 直接使用预先算好的最大值
    return answer
```

#### 复杂度  

- **时间复杂度**：`O(m·n)`。  
  - 两次完整遍历矩阵，每次都是 `m·n` 步，常数因子 2 在大 O 记号里省略。  
  - 用大白话说，就是**“只走两趟矩阵的每一格”**，比暴力解省了大量重复的列扫描。

- **空间复杂度**：`O(n + m·n)`。  
  - `col_max` 只需要 `n` 个额外空间（存每列最大值）。  
  - 题目要求返回一个新矩阵，需要 `m·n` 的拷贝空间，这部分是必须的。  
  - 相比暴力解，额外的辅助空间只有 `O(n)`，非常小。

---

## 心得

- **核心技巧**：先预处理（一次遍历）得到列（或行）的聚合信息（这里是最大值），再在第二遍直接使用。  
- **适用场景**：  
  1. “把矩阵中满足某条件的元素替换成所在行/列的统计值”——例如 `行最大值、列最小值、行和、列和`。  
  2. “二维数组的每一行/列需要统一的映射”——如 LeetCode 1732 “找出所有子数组的最大值”。  
  3. “需要多次查询同一维度的聚合信息”——比如图像处理中的列归一化。  
- **一句话总结解题钥匙**：**“先把每列的‘答案’算好，后面只需要‘查表’即可”。**

---

## 反思

- **第一反应**：看到 “把 -1 换成所在列的最大值”，立刻想到对每个 -1 单独遍历列，这就是暴力解。  
- **最容易踩的坑**：  
  - **忘记对原矩阵做拷贝**，直接在原矩阵上修改会影响后面列最大值的计算（因为后面的 -1 可能已经被改成了最大值，导致错误）。  
  - **边界条件**：如果某列全是 -1（但题目保证不出现），需要额外判断；实际题目已经排除这种情况。  
- **下次思路**：遇到“对同一行/列的多个位置做相同的聚合替换”时，第一步就考虑**先一次遍历把聚合值统计出来**，再一次遍历完成替换，避免重复扫描。