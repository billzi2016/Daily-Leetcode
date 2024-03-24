# #2624. **蜗牛遍历** / Snail Traversal

> 难度：中等 · 标签： · [LeetCode 链接](https://leetcode.com/problems/snail-traversal/)

---

## 题目（英文原版）

**Description**

Write code that enhances all arrays such that you can call the snail(rowsCount, colsCount) method that transforms the 1D array into a 2D array organised in the pattern known as snail traversal order. Invalid input values should output an empty array. If rowsCount * colsCount !== nums.length, the input is considered invalid.
Snail traversal order starts at the top left cell with the first value of the current array. It then moves through the entire first column from top to bottom, followed by moving to the next column on the right and traversing it from bottom to top. This pattern continues, alternating the direction of traversal with each column, until the entire current array is covered. For example, when given the input array [19, 10, 3, 7, 9, 8, 5, 2, 1, 17, 16, 14, 12, 18, 6, 13, 11, 20, 4, 15] with rowsCount = 5 and colsCount = 4, the desired output matrix is shown below. Note that iterating the matrix following the arrows corresponds to the order of numbers in the original array.

**Examples**

**Example 1:**

```
Input: 
nums = [19, 10, 3, 7, 9, 8, 5, 2, 1, 17, 16, 14, 12, 18, 6, 13, 11, 20, 4, 15]
rowsCount = 5
colsCount = 4
Output: 
[
 [19,17,16,15],
 [10,1,14,4],
 [3,2,12,20],
 [7,5,18,11],
 [9,8,6,13]
]
```

**Example 2:**

```
Input: 
nums = [1,2,3,4]
rowsCount = 1
colsCount = 4
Output: [[1, 2, 3, 4]]
```

**Example 3:**

```
Input: 
nums = [1,3]
rowsCount = 2
colsCount = 2
Output: []
Explanation: 2 multiplied by 2 is 4, and the original array [1,3] has a length of 2; therefore, the input is invalid.
```

**Constraints**

- 0 <= nums.length <= 250
- 1 <= nums[i] <= 1000
- 1 <= rowsCount <= 250
- 1 <= colsCount <= 250

---

## 题目（中文翻译）

编写代码为所有数组添加功能，使其可以调用 `snail(rowsCount, colsCount)` 方法，将一维数组（1D array）转换为按照**蜗牛遍历顺序**（snail traversal order）组织的二维数组（2D array）。若输入值无效，则返回空数组。若 `rowsCount * colsCount !== nums.length`，则视为输入无效。

**蜗牛遍历顺序** 从当前数组的第一个元素对应的左上角单元格开始。随后沿第一列从上到下遍历完整列，再移动到右侧的下一列并从下往上遍历。该模式在每一列交替方向进行，直至覆盖整个数组。例如，给定数组  

`[19, 10, 3, 7, 9, 8, 5, 2, 1, 17, 16, 14, 12, 18, 6, 13, 11, 20, 4, 15]`  

以及 `rowsCount = 5`, `colsCount = 4`，得到的矩阵如下所示。注意，沿矩阵中的箭头方向遍历得到的顺序即为原数组的顺序。

### 示例

**示例 1**

```text
Input: 
nums = [19, 10, 3, 7, 9, 8, 5, 2, 1, 17, 16, 14, 12, 18, 6, 13, 11, 20, 4, 15]
rowsCount = 5
colsCount = 4
Output: 
[
 [19,17,16,15],
 [10,1,14,4],
 [3,2,12,20],
 [7,5,18,11],
 [9,8,6,13]
]
```

**示例 2**

```text
Input: 
nums = [1,2,3,4]
rowsCount = 1
colsCount = 4
Output: [[1, 2, 3, 4]]
```

**示例 3**

```text
Input: 
nums = [1,3]
rowsCount = 2
colsCount = 2
Output: []
Explanation: 2 乘以 2 等于 4，而原数组 `[1,3]` 长度为 2；因此输入无效。
```

### 约束条件

- `0 <= nums.length <= 250`
- `1 <= nums[i] <= 1000`
- `1 <= rowsCount <= 250`
- `1 <= colsCount <= 250`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**把原始一维数组的元素依次放进一个二维矩阵**，按照题目描述的“蜗牛列遍历”顺序填充：

1. 先准备一个 `rowsCount × colsCount` 的空矩阵（可以用 `[[0]*colsCount for _ in range(rowsCount)]`，相当于一张空白的表格）。  
2. 用一个指针 `idx` 从 `0` 开始遍历原始数组 `nums`。  
3. 按列从左到右遍历，每一列的遍历方向取决于列号的奇偶性  
   * **偶数列**（0、2、4…） → 从上往下填  
   * **奇数列**（1、3、5…） → 从下往上填  
4. 把 `nums[idx]` 放进对应的格子后，`idx += 1`，继续填下一个格子。  
5. 当所有元素都放完，矩阵即为答案。  

> **类比**：把矩阵想成一本竖排的书，每一列是一行文字。偶数列我们从第一页往后翻，奇数列则把书倒过来，从最后一页往前翻，这样就形成了“上下交替”的阅读顺序。

如果 `rowsCount * colsCount != len(nums)`，说明数组元素不足或多余，直接返回空列表 `[]` 表示输入非法。

> **为什么正确**：我们严格按照题目给出的遍历顺序把每个数组元素放到对应位置，且每个位置只放一次，遍历完所有元素后恰好填满整个矩阵，必然得到符合要求的结果。

#### 代码（Python）

```python
def snail(nums, rowsCount, colsCount):
    # ---------- 参数合法性检查 ----------
    if rowsCount * colsCount != len(nums):
        return []                     # 长度不匹配，直接返回空列表

    # ---------- 创建空矩阵 ----------
    # rowsCount 行，每行 colsCount 列，初始全为 0
    matrix = [[0] * colsCount for _ in range(rowsCount)]

    idx = 0  # nums 的指针，指向当前要写入的元素

    # ---------- 按列遍历 ----------
    for col in range(colsCount):
        if col % 2 == 0:                     # 偶数列：从上往下
            for row in range(rowsCount):
                matrix[row][col] = nums[idx]
                idx += 1
        else:                                # 奇数列：从下往上
            for row in range(rowsCount - 1, -1, -1):
                matrix[row][col] = nums[idx]
                idx += 1

    return matrix
```

#### 复杂度

- **时间复杂度**：`O(n)`（其中 `n = rowsCount * colsCount`），因为我们恰好遍历一次原数组的每个元素，没有额外的循环嵌套。  
  > 大白话：不管矩阵多大，只要元素个数是 `n`，我们就只做 `n` 次“放进格子”的操作，速度和元素个数成正比。

- **空间复杂度**：`O(n)` 用于存放结果矩阵（题目要求必须返回一个二维数组），额外的临时变量只占 `O(1)`。

---

### 2. 最优解

#### 思路  

从暴力解来看，唯一的“瓶颈”其实是**每列都要判断一次是向上还是向下**，这一步虽然是 `O(1)`，但我们可以进一步**用数学公式直接算出每个格子的行号**，省去 `if … else` 的分支判断，使代码更简洁，也更容易推广到更高维度的类似问题。

关键观察：

- 对于第 `c` 列（`c` 从 `0` 开始），遍历方向只和 `c` 的奇偶性有关。  
- 当 `c` 为偶数时，行号随元素顺序递增：`0, 1, 2, …, rowsCount-1`。  
- 当 `c` 为奇数时，行号随元素顺序递减：`rowsCount-1, rowsCount-2, …, 0`。  

于是我们可以把 **行号** 用下面的公式表达：

```
row = i                 if c 是偶数
row = rowsCount - 1 - i if c 是奇数
```

其中 `i` 是当前列已经放入的元素个数（0 ≤ i < rowsCount）。

这样只需要一次循环遍历 `colsCount` 列，在每列内部再用 `range(rowsCount)` 产生 `i`，直接算出对应的 `row` 并写入即可。

> **类比**：想象每一列是一根电梯的轨道。偶数列的电梯从第一层向上跑，奇数列的电梯从顶层往下跑。我们不需要实际“开关电梯”，只要知道当前是第几层（`i`），再根据轨道是向上还是向下，直接算出应该站在哪层（`row`）。

#### 代码（Python）

```python
def snail(nums, rowsCount, colsCount):
    # ---------- 参数合法性 ----------
    if rowsCount * colsCount != len(nums):
        return []

    # ---------- 初始化结果矩阵 ----------
    matrix = [[0] * colsCount for _ in range(rowsCount)]

    idx = 0  # nums 的读取指针

    # ---------- 直接用数学公式计算行号 ----------
    for col in range(colsCount):
        # 对当前列的每一个位置 i（0~rowsCount-1）计算真实行号
        for i in range(rowsCount):
            # 偶数列：正序；奇数列：倒序
            row = i if col % 2 == 0 else rowsCount - 1 - i
            matrix[row][col] = nums[idx]
            idx += 1

    return matrix
```

#### 复杂度

- **时间复杂度**：`O(n)`，与暴力解相同，因为仍然只遍历 `n` 次元素。  
  > 与暴力解对比：我们把分支判断搬到了公式里，实际执行的基本指令更少，常数因子更小，运行会稍快。

- **空间复杂度**：`O(n)`，同样是返回的二维矩阵占用的空间。

---

## 心得

- **核心技巧**：**按列遍历、利用奇偶性决定方向**，以及**用数学公式直接映射行号**。  
- **适用的题型**  
  1. “蛇形填充/之字形填充”类（例如 LeetCode 59 `Spiral Matrix II` 的变形）。  
  2. “按行/列交替方向遍历”类（如“Z字形遍历二叉树”）。  
  3. 需要把一维序列映射到二维结构且遍历顺序固定的题目。  
- **一句话总结解题钥匙**：**把“方向交替”抽象成列号的奇偶性，用公式一次算出行坐标**。

## 反思

- **第一反应**：检查输入是否合法，然后想象矩阵的填充顺序——先列后行，方向交替。  
- **最容易踩的坑**  
  - 忘记先判断 `rowsCount * colsCount` 是否等于 `len(nums)`，导致 IndexError。  
  - 在奇数列时写成 `row = i`（正序）而忘记倒序，导致矩阵行列顺序颠倒。  
  - 边界条件：`rowsCount` 或 `colsCount` 为 `1` 时仍需正常工作（代码已覆盖）。  
- **下次类似题的第一步**：**明确“遍历顺序”是否可以用列/行的奇偶性或其他规律表达**，如果可以，就先写出对应的坐标公式，再进行填充。