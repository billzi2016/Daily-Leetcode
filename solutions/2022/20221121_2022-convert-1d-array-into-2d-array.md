# #2022. 转换一维数组为二维数组 / Convert 1D Array Into 2D Array

> 难度：简单 · 标签：Array、Matrix、Simulation · [LeetCode 链接](https://leetcode.com/problems/convert-1d-array-into-2d-array/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed 1-dimensional (1D) integer array original, and two integers, m and n. You are tasked with creating a 2-dimensional (2D) array with  m rows and n columns using all the elements from original.
The elements from indices 0 to n - 1 (inclusive) of original should form the first row of the constructed 2D array, the elements from indices n to 2 * n - 1 (inclusive) should form the second row of the constructed 2D array, and so on.
Return an m x n 2D array constructed according to the above procedure, or an empty 2D array if it is impossible.

**Examples**

**Example 1:**

```
Input: original = [1,2,3,4], m = 2, n = 2
Output: [[1,2],[3,4]]
Explanation: The constructed 2D array should contain 2 rows and 2 columns.
The first group of n=2 elements in original, [1,2], becomes the first row in the constructed 2D array.
The second group of n=2 elements in original, [3,4], becomes the second row in the constructed 2D array.
```

**Example 2:**

```
Input: original = [1,2,3], m = 1, n = 3
Output: [[1,2,3]]
Explanation: The constructed 2D array should contain 1 row and 3 columns.
Put all three elements in original into the first row of the constructed 2D array.
```

**Example 3:**

```
Input: original = [1,2], m = 1, n = 1
Output: []
Explanation: There are 2 elements in original.
It is impossible to fit 2 elements in a 1x1 2D array, so return an empty 2D array.
```

**Constraints**

- 1 <= original.length <= 5 * 104
- 1 <= original[i] <= 105
- 1 <= m, n <= 4 * 104

---

## 题目（中文翻译）

**题目描述**  
给定一个下标从 **0** 开始的一维 (1D) 整数数组 `original`，以及两个整数 `m` 和 `n`。请使用 `original` 中的所有元素构造一个具有 `m` 行 `n` 列的二维 (2D) 数组。

- `original` 中下标 `[0, n‑1]`（含） 的元素构成构造后二维数组的第一行；
- `original` 中下标 `[n, 2·n‑1]`（含） 的元素构成第二行；
- 依此类推。

返回按照上述规则构造的 `m × n` 二维数组；如果无法完成构造（即 `original` 的元素数量不等于 `m·n`），则返回一个空的二维数组。

**示例 1**  
```text
Input: original = [1,2,3,4], m = 2, n = 2
Output: [[1,2],[3,4]]
Explanation: 构造的二维数组应有 2 行 2 列。  
原数组前 2 个元素 [1,2] 成为第一行，接下来的 2 个元素 [3,4] 成为第二行。
```

**示例 2**  
```text
Input: original = [1,2,3], m = 1, n = 3
Output: [[1,2,3]]
Explanation: 构造的二维数组应有 1 行 3 列。  
将原数组的全部 3 个元素放入第一行即可。
```

**示例 3**  
```text
Input: original = [1,2], m = 1, n = 1
Output: []
Explanation: 原数组有 2 个元素，但 1×1 的二维数组只能容纳 1 个元素，无法完成构造，故返回空二维数组。
```

**约束条件**  
- `1 <= original.length <= 5 * 10^4`  
- `1 <= original[i] <= 10^5`  
- `1 <= m, n <= 4 * 10^4`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：先检查能否把 `original` 塞进 `m × n` 的矩阵。  
- **能否塞进去** 就看总格子数 `m * n` 是否等于数组长度 `len(original)`。  
  - 如果不相等，说明元素太多或太少，根本不可能填满矩阵，直接返回空的二维数组 `[]`。  
- 检查通过后，我们把 `original` 按照每 `n` 个元素一组切成 `m` 行。  
  - 这里可以把 `original` 看成一本书，`n` 就是每页的行数，顺序翻页把每页的内容取出来放进二维数组。  
- 用 **列表切片**（`original[start:end]`）来取出每一行。切片相当于在字典里查词：键是下标范围，值是对应的子数组。  

这样做一定能得到符合题目要求的二维数组，因为我们严格按照题目说明的顺序取元素。

#### 代码（Python）

```python
def construct2DArray(original, m, n):
    # 1️⃣ 先判断能否填满矩阵
    if m * n != len(original):
        return []                     # 长度不匹配，返回空二维数组

    res = []                          # 用来存放最终的二维数组
    # 2️⃣ 按每 n 个元素取出一行，共 m 行
    for row in range(m):
        start = row * n               # 本行在 original 中的起始下标
        end   = start + n             # 本行的结束下标（不含）
        res.append(original[start:end])   # 切片得到本行，加入结果
        # 切片相当于把原数组的第 start~end-1 个元素复制到一个新列表

    return res
```

#### 复杂度  

- **时间复杂度：** `O(m * n)`  
  - 实际上我们遍历了 `original` 中的每一个元素一次（`m * n` 次），所以时间随元素个数线性增长。  
  - 用大白话说，假如有 1000 个数字，就要花 1000 步把它们搬进去。

- **空间复杂度：** `O(m * n)`（输出空间）+ `O(1)`（额外工作空间）  
  - 除了返回的二维数组本身（题目要求必须返回），我们只用了常数级的临时变量 (`start`, `end`, `row`)。  

---

### 2. 最优解  

#### 思路  
从暴力解可以看到，**瓶颈**并不在遍历或切片本身，而在于我们必须把所有元素都搬进去——这一步是不可避免的。  
因此“最优”并不是把时间复杂度进一步压缩，而是**写得更简洁、一次性完成**：

1. **一次性检查**：`m * n == len(original)`。如果不等直接返回 `[]`。  
2. **一次性构造**：利用 Python 的 **列表推导式**（list comprehension）在一行代码里把所有切片收集起来。  
   - 列表推导式可以看成是“一次性搬家工人”，把每一行的 `n` 个元素一次性搬进结果列表，省去显式的 `for` 循环写法。  
   - 这仍然是线性时间 `O(m*n)`，但代码更紧凑，易读性更好。  

核心数据结构仍然是 **列表**（list），没有额外的哈希表、栈等复杂结构。

#### 代码（Python）

```python
def construct2DArray(original, m, n):
    # 检查能否完整填满矩阵
    if m * n != len(original):
        return []

    # 列表推导式：一次性生成每一行的切片
    return [original[i * n : (i + 1) * n] for i in range(m)]
    # 解释：
    # i 取值 0 ~ m-1，对应第 i 行
    # i * n   是本行的起始下标
    # (i+1)*n 是本行的结束下标（不含）
    # 切片得到本行，所有行组成外层列表即为最终的二维数组
```

#### 复杂度  

- **时间复杂度：** `O(m * n)`  
  - 与暴力解相同，因为必须访问每个元素一次。相对来说，省掉了显式的 `for` 循环的循环体开销，常数因子更小。  

- **空间复杂度：** `O(m * n)`（输出）+ `O(1)`（额外）  
  - 只用了常数级的临时变量 `i`，其余全部是返回的二维数组。  

---

## 心得  

- **核心技巧**：先判断可行性（`m * n == len(original)`），再使用 **切片** 把一维数组按固定长度分块。  
- **适用的题型**：  
  1. 将一维数组拆分成固定大小的子数组（如 “Split Array into Consecutive Subarrays”）。  
  2. 按行列填充矩阵的题目（如 “Reshape the Matrix”）。  
- **解题钥匙**：**“先判断能否填满，再按块切片”**。

---

## 反思  

- **第一反应**：看到 `m` 行 `n` 列，第一时间想到检查总格子数是否匹配，然后逐行取元素。  
- **最容易踩的坑**：  
  - 忘记返回空二维数组 `[]`（而不是 `None`）当长度不匹配。  
  - 切片的结束下标写成 `i * n + n - 1`（会少取一个元素），正确写法是 `i * n : (i + 1) * n`（结束下标是开区间）。  
- **下次类似题的第一步**：先写出 **“是否可行”** 的判断式 `if m * n != len(arr): return []`，把不可能的情况提前剔除，再专注于构造过程。