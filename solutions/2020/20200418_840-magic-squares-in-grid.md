# #840. 网格中的魔方阵（Magic Squares In Grid） / Magic Squares In Grid

> 难度：中等 · 标签：Array、Hash Table、Math、Matrix · [LeetCode 链接](https://leetcode.com/problems/magic-squares-in-grid/)

---

## 题目（英文原版）

**Description**

A 3 x 3 magic square is a 3 x 3 grid filled with distinct numbers from 1 to 9 such that each row, column, and both diagonals all have the same sum.
Given a row x col grid of integers, how many 3 x 3 magic square subgrids are there?
Note: while a magic square can only contain numbers from 1 to 9, grid may contain numbers up to 15.

**Examples**

**Example 1:**

```
Input: grid = [[4,3,8,4],[9,5,1,9],[2,7,6,2]]
Output: 1
Explanation: 
The following subgrid is a 3 x 3 magic square:

while this one is not:

In total, there is only one magic square inside the given grid.
```

**Example 2:**

```
Input: grid = [[8]]
Output: 0
```

**Constraints**

- row == grid.length
- col == grid[i].length
- 1 <= row, col <= 10
- 0 <= grid[i][j] <= 15

---

## 题目（中文翻译）

一个 **3 × 3 魔方阵（magic square）** 是指一个 3 × 3 的网格，其中填入的数字必须是 1 到 9 的 **不同** 整数，并且每一行、每一列以及两条对角线的数字和都相等。  

给定一个 `row × col` 的整数网格 `grid`，请统计其中 **3 × 3 魔方阵子网格（subgrid）** 的个数。

> 注意：虽然魔方阵只能包含 1~9 的数字，但原始网格中的数字范围可能到 15。

### 示例

#### 示例 1
**输入**
```text
grid = [[4,3,8,4],
        [9,5,1,9],
        [2,7,6,2]]
```
**输出**
```text
1
```
**解释**  
下面这块子网格是一个 3 × 3 的魔方阵：

```
4 3 8
9 5 1
2 7 6
```

而下面这块则不是：

```
3 8 4
5 1 9
7 6 2
```

整个网格中仅存在一个符合条件的魔方阵子网格。

#### 示例 2
**输入**
```text
grid = [[8]]
```
**输出**
```text
0
```

### 约束条件
- `row == grid.length`
- `col == grid[i].length`
- `1 ≤ row, col ≤ 10`
- `0 ≤ grid[i][j] ≤ 15`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**把所有可能的 3×3 小方阵都枚举出来，逐个检查它们是不是“魔方阵”。**  

- **枚举**：如果原矩阵有 `row` 行、`col` 列，只要左上角坐标 `(i, j)` 满足 `0 ≤ i ≤ row-3`、`0 ≤ j ≤ col-3`，就可以截取出一个 3×3 子矩阵。  
- **检查**：把这 9 个数拿出来，先判断它们是否全部是 **1~9 的互不相同的整数**（相当于在字典里查单词是否出现过——哈希表的“查字典”过程），再判断 **每一行、每一列、两条对角线的和是否相等**。如果都满足，则计数 +1。

> **为什么这个方法一定对？**  
> 因为题目要求的“魔方阵”定义就是“这 9 个数满足上述所有条件”。只要把所有子矩阵都遍历一遍，必然不会漏掉任何合法的情况。

> **复杂度怎么理解？**  
> - **时间**：我们要遍历 `(row-2)*(col-2)` 个左上角位置，每个位置检查 9 个数并做几次加法、比较，算是常数时间 `O(1)`。所以整体是 `O(row * col)`。在最坏情况下 `row, col ≤ 10`，最多 100 次检查，几乎瞬间完成。  
> - **空间**：只用了几个临时变量（比如存 9 个数的列表、哈希集合），与输入规模无关，属于 `O(1)` 常数空间。

#### 代码（Python）

```python
from typing import List

def numMagicSquaresInside(grid: List[List[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    ans = 0

    # 遍历所有可能的左上角 (i, j)
    for i in range(rows - 2):
        for j in range(cols - 2):
            if is_magic(grid, i, j):
                ans += 1
    return ans


def is_magic(grid: List[List[int]], r: int, c: int) -> bool:
    """判断以 (r, c) 为左上角的 3×3 子矩阵是否是魔方阵"""

    nums = []               # 用来收集 9 个数
    seen = set()            # 哈希集合：判断是否出现重复

    # 逐行读取 3×3 区域
    for i in range(r, r + 3):
        for j in range(c, c + 3):
            val = grid[i][j]
            # 必须是 1~9 的整数
            if not (1 <= val <= 9):
                return False
            # 不能出现重复数字
            if val in seen:
                return False
            seen.add(val)
            nums.append(val)

    # 计算每行、每列、两条对角线的和
    # 行和
    for i in range(3):
        if sum(grid[r + i][c:c + 3]) != 15:
            return False
    # 列和
    for j in range(3):
        if sum(grid[r + k][c + j] for k in range(3)) != 15:
            return False
    # 对角线和
    if (grid[r][c] + grid[r + 1][c + 1] + grid[r + 2][c + 2] != 15 or
        grid[r][c + 2] + grid[r + 1][c + 1] + grid[r + 2][c] != 15):
        return False

    return True
```

> **代码要点**  
> - 第 7~13 行是**双层循环**，把所有左上角坐标枚举出来。  
> - `is_magic` 函数里先用 **哈希集合**（`set`）检查 1~9 是否全部出现且不重复，这一步类似“查字典”。  
> - 接下来分别检查 **行、列、两条对角线**的和是否等于 15（3×3 魔方阵的唯一可能和）。  

#### 复杂度

- **时间复杂度**：`O(row * col)`  
  > 这里的 `O` 记号可以理解为“随矩阵大小线性增长”。比如 10×10 的矩阵要检查 64 个子矩阵，20×20（虽然超出题目限制）就会检查 324 个，基本是正比例关系。

- **空间复杂度**：`O(1)`  
  > 只用了常数个变量（`set`、`list`），不随输入大小增大而增多。

---

### 2. 最优解

#### 思路  

虽然上面的暴力解已经够快（因为矩阵本身很小），但如果把行列上限放大到几千甚至上万，**逐个检查 9 个数的完整过程就会成为瓶颈**。我们可以利用 **3×3 魔方阵的数学特性**，在检查时提前剔除大多数不可能的子矩阵，从而把每个子矩阵的验证时间从 `O(9)` 降到 `O(1)`。

**关键特性**（可以把它们想象成“魔方阵的 DNA”）：

1. **中心一定是 5**  
   - 证明：在 1~9 中，只有 5 能使行、列、对角线的和都等于 15。  
2. **四个角必须是偶数（2、4、6、8）**，**四条边必须是奇数（1、3、7、9）**  
   - 这来源于奇偶性分析：行/列和为 15（奇数），若中心 5 为奇数，则每行（或列）里另外两个数必须一奇一偶。  
3. **所有数字必须互不相同且在 1~9 之间**（已经在暴力解里检查过）。

利用这三个条件，我们可以把检查过程压缩为：

- 先看中心是否为 5，若不是直接返回 `False`（一步就能淘汰 9/10 的子矩阵）。
- 再检查四个角是否全部是 **偶数**，若有奇数直接淘汰。
- 再检查四条边（不包括中心）是否全部是 **奇数**，若有偶数直接淘汰。
- 最后只需要验证 **行、列、对角线的和是否为 15**（因为前面的奇偶性已经保证了每行必有一奇一偶，且中心为 5，只有 1 种可能的和）。

这样每个子矩阵只需要常数次的判断（几条 `if`），不需要遍历全部 9 个格子。

#### 代码（Python）

```python
from typing import List

def numMagicSquaresInside(grid: List[List[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    count = 0

    for i in range(rows - 2):
        for j in range(cols - 2):
            if is_magic_opt(grid, i, j):
                count += 1
    return count


def is_magic_opt(grid: List[List[int]], r: int, c: int) -> bool:
    """基于魔方阵特性进行 O(1) 检查"""

    # 1️⃣ 中心必须是 5
    if grid[r + 1][c + 1] != 5:
        return False

    # 2️⃣ 角必须是偶数，且在 1~9 范围内
    corners = [
        grid[r][c],         # 左上
        grid[r][c + 2],     # 右上
        grid[r + 2][c],     # 左下
        grid[r + 2][c + 2]  # 右下
    ]
    for v in corners:
        if v % 2 != 0 or not (1 <= v <= 9):
            return False

    # 3️⃣ 边（不包括中心）必须是奇数，且在 1~9 范围内
    edges = [
        grid[r][c + 1],         # 上中
        grid[r + 1][c],         # 左中
        grid[r + 1][c + 2],     # 右中
        grid[r + 2][c + 1]      # 下中
    ]
    for v in edges:
        if v % 2 == 0 or not (1 <= v <= 9):
            return False

    # 4️⃣ 检查是否所有数字互不相同
    nums = [
        grid[r][c], grid[r][c + 1], grid[r][c + 2],
        grid[r + 1][c], grid[r + 1][c + 1], grid[r + 1][c + 2],
        grid[r + 2][c], grid[r + 2][c + 1], grid[r + 2][c + 2]
    ]
    if len(set(nums)) != 9:      # 集合长度不等于 9，说明有重复
        return False

    # 5️⃣ 最后验证行、列、对角线的和是否为 15
    # 行和
    for i in range(3):
        if sum(grid[r + i][c:c + 3]) != 15:
            return False
    # 列和
    for j in range(3):
        if sum(grid[r + k][c + j] for k in range(3)) != 15:
            return False
    # 对角线
    if (grid[r][c] + grid[r + 1][c + 1] + grid[r + 2][c + 2] != 15 or
        grid[r][c + 2] + grid[r + 1][c + 1] + grid[r + 2][c] != 15):
        return False

    return True
```

> **代码要点**  
> - 第 9 行直接判断中心是否为 5，这一步能把 **90%+** 的候选子矩阵淘汰掉。  
> - 第 12~20 行检查四个角的奇偶性；第 23~30 行检查四条边的奇偶性，利用“偶数在角、奇数在边”的特性。  
> - 第 33~38 行仍然需要确保 **9 个数不重复**（因为即使奇偶性满足，也可能出现重复数字）。  
> - 最后仍保留一次完整的行/列/对角线求和检查，以防出现罕见的 “奇偶性+中心为5+不重复” 仍不满足魔方阵的情况（理论上已经不可能，但加上保险）。  

#### 复杂度

- **时间复杂度**：`O(row * col)`（同样是遍历所有左上角）  
  > 与暴力解的时间复杂度形式相同，但**常数因子更小**——每个子矩阵只做几次 `if` 判断和少量加法，而不是遍历 9 个格子。对于大矩阵（比如 1000×1000）可以把运行时间从几秒降到毫秒级。

- **空间复杂度**：`O(1)`  
  > 只使用了固定数量的临时变量和一个长度为 9 的列表，和输入规模无关。

---

## 心得

- **核心技巧**：利用 **数学性质（中心为5、奇偶分布）** 进行提前剪枝，结合 **哈希集合** 检查“数字是否唯一”。  
- **适用的题型**：  
  1. **固定大小子矩阵的特殊结构检测**（如 “判断 2×2 是否为全 1”）。  
  2. **利用数值特性快速过滤**（如 “判断 4×4 是否为拉丁方”）。  
  3. **需要判断“全局唯一性+局部约束”的问题**（如 “判断数独中的 3×3 子格是否合法”）。  
- **一句话总结解题钥匙**：**先用最容易判断的属性把大多数不合格的候选剔除，再用完整检查确认**。

---

## 反思

- **第一反应**：看到“3×3 魔方阵”，立刻想到把每个子矩阵全部枚举、逐个验证——这是最自然的暴力思路。  
- **最容易踩的坑**：  
  - 忽略 **数字必须在 1~9 范围内**（题目只保证 grid 中数字 ≤15），导致出现 10、12 之类的数仍被误判。  
  - 忘记检查 **数字是否互不相同**，只检查和相等会把如 `[5,5,5]` 的行误认为合法。  
  - 边界条件：当 `row < 3` 或 `col < 3` 时直接返回 0，防止负索引错误。  
- **下次遇到同类题**：第一步先**寻找题目给出的数学/结构性约束**（如中心固定、奇偶分布、和的固定值），把这些“硬约束”写成快速过滤条件，再决定是否需要完整遍历检查。这样可以把时间复杂度的常数降到最低。