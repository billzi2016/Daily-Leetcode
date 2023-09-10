# #2397. 通过列覆盖的最大行数 / Maximum Rows Covered by Columns

> 难度：中等 · 标签：Array、Backtracking、Bit Manipulation、Matrix、Enumeration · [LeetCode 链接](https://leetcode.com/problems/maximum-rows-covered-by-columns/)

---

## 题目（英文原版）

**Description**

You are given an m x n binary matrix matrix and an integer numSelect.
Your goal is to select exactly numSelect distinct columns from matrix such that you cover as many rows as possible.
A row is considered covered if all the 1's in that row are also part of a column that you have selected. If a row does not have any 1s, it is also considered covered.
More formally, let us consider selected = {c1, c2, ...., cnumSelect} as the set of columns selected by you. A row i is covered by selected if:
Return the maximum number of rows that can be covered by a set of numSelect columns.

**Examples**

**Example 1:**

```
Input: matrix = [[0,0,0],[1,0,1],[0,1,1],[0,0,1]], numSelect = 2
Output: 3
Explanation:
One possible way to cover 3 rows is shown in the diagram above. We choose s = {0, 2}. - Row 0 is covered because it has no occurrences of 1. - Row 1 is covered because the columns with value 1, i.e. 0 and 2 are present in s. - Row 2 is not covered because matrix[2][1] == 1 but 1 is not present in s. - Row 3 is covered because matrix[2][2] == 1 and 2 is present in s. Thus, we can cover three rows. Note that s = {1, 2} will also cover 3 rows, but it can be shown that no more than three rows can be covered.
```

**Example 2:**

```
Input: matrix = [[1],[0]], numSelect = 1
Output: 2
Explanation:
Selecting the only column will result in both rows being covered since the entire matrix is selected.
```

**Constraints**

- m == matrix.length
- n == matrix[i].length
- 1 <= m, n <= 12
- matrix[i][j] is either 0 or 1.
- 1 <= numSelect <= n

---

## 题目（中文翻译）

给定一个 `m × n` 的二进制矩阵 `matrix` 和一个整数 `numSelect`。  
你的目标是 **恰好** 选择 `numSelect` 个互不相同的列，使得能够覆盖的行数尽可能多。  

如果一行中的所有 `1` 所在的列都被选中了，则该行被视为 **已覆盖**（covered）。  
如果一行中没有任何 `1`，也视为已覆盖。  

形式化地，设 `selected = {c₁, c₂, …, c_{numSelect}}` 为你选择的列集合。第 `i` 行在以下条件成立时被 `selected` 覆盖：

- 对所有满足 `matrix[i][j] == 1` 的列索引 `j`，都有 `j ∈ selected`；或者
- 第 `i` 行不存在 `1`（即整行全为 `0`）。

返回可以通过恰好 `numSelect` 列覆盖的 **最大行数**。

### 示例 1
``` 
Input: matrix = [[0,0,0],[1,0,1],[0,1,1],[0,0,1]], numSelect = 2
Output: 3
Explanation:
一种可以覆盖 3 行的方案如图所示。我们选择列集合 s = {0, 2}。
- 第 0 行被覆盖，因为它没有出现 `1`。
- 第 1 行被覆盖，因为其值为 `1` 的列（0 和 2）都在 s 中。
- 第 2 行未被覆盖，因为 `matrix[2][1] == 1`，但列 1 不在 s 中。
- 第 3 行被覆盖，因为唯一的 `1` 出现在列 2，列 2 在 s 中。
```

### 示例 2
``` 
Input: matrix = [[1],[0]], numSelect = 1
Output: 2
Explanation:
选择唯一的那一列后，所有行都被覆盖，因为整列已被选中。
```

### 约束条件
- `m == matrix.length`
- `n == matrix[i].length`
- `1 ≤ m, n ≤ 12`
- `matrix[i][j]` 仅为 `0` 或 `1`
- `1 ≤ numSelect ≤ n`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是「把所有可能的列组合都枚举一遍，看看每一种组合能覆盖多少行，取最大值」。  
- **枚举方式**：从 `n` 列里挑出恰好 `numSelect` 列。可以把列的下标看成「超市的货架」，我们要从这些货架里挑出 `numSelect` 个来「摆上」我们的商品。  
- **判断一行是否被覆盖**：遍历该行的每一个元素，只要出现了 `1`，对应的列必须在我们挑选的集合里。换句话说，这一行的所有「1」就像「需要的配件」，只有全部配齐（对应列都被选中），这行才算「完成」。如果一行全是 `0`，它根本不需要配件，天然算完成。  
- **为什么一定正确**：我们把 **所有** 合法的列集合都检查了一遍，最大覆盖行数必然出现在其中的某个集合里。  

> **数据结构类比**  
> - **集合**（`selected`）可以看成「字典」的关键词集合，判断一个列是否被选中就像在字典里查找某个词是否存在。  
> - **行的 1 的位置** 用一个列表或整数的二进制位来保存，后面会用到位运算来快速判断「是否全部在集合里」。

#### 代码（Python）

```python
from itertools import combinations
from typing import List

def maxRowsCovered_bruteforce(matrix: List[List[int]], numSelect: int) -> int:
    m, n = len(matrix), len(matrix[0])

    # 预处理：把每一行中出现 1 的列下标保存下来，方便后面检查
    # row_one_cols[i] = {col index where matrix[i][col] == 1}
    row_one_cols = []
    for row in matrix:
        cols = {j for j, val in enumerate(row) if val == 1}
        row_one_cols.append(cols)

    best = 0  # 当前找到的最大覆盖行数

    # 逐个枚举所有恰好选取 numSelect 列的组合
    for selected in combinations(range(n), numSelect):
        selected_set = set(selected)          # 把元组转成集合，查找更快
        covered = 0

        # 检查每一行是否被覆盖
        for cols in row_one_cols:
            # 如果该行没有 1，直接算覆盖；否则检查它的所有 1 所在列是否都在 selected_set 中
            if not cols or cols.issubset(selected_set):
                covered += 1

        best = max(best, covered)  # 更新最大值

    return best
```

**关键行中文注释**  
- `combinations(range(n), numSelect)`: 从 `0 … n-1` 中挑出恰好 `numSelect` 列的所有组合。  
- `cols.issubset(selected_set)`: 判断该行所有 `1` 所在列是否全部在我们挑选的列集合里。  

#### 复杂度  

- **时间复杂度**：`O( C(n, numSelect) * m * n )`  
  - `C(n, k)` 表示「从 n 中挑 k」的组合数，例如 `C(12,6)=924`。  
  - 对每一种列组合，我们要检查 `m` 行，每行最坏要遍历 `n` 列（找 `1` 的位置），所以乘以 `m·n`。  
  - 大白话：如果列数是 12，行数也是 12，最多要尝试几百种组合，每种组合再看 12 行 * 12 列，计算量在几千次以内，完全能接受。  
- **空间复杂度**：`O(m·n)` 用来存放 `row_one_cols`（每行的 1 的位置），其实可以更省，只需要 `O(m)` 的位掩码，后面会介绍。  

---

### 2. 最优解  

#### 思路  

虽然上面的暴力已经能在题目限制下跑完，但我们可以把「检查每行是否被覆盖」的过程压缩到 **位运算**（Bit Manipulation）里，省掉集合的创建与子集判断，进一步提升常数因子。  

**核心想法**  

1. **把列集合和行的 1 的位置都用二进制整数表示**  
   - 把第 `j` 列对应二进制的第 `j` 位（从右往左），如果该列被选中，位设为 `1`。  
   - 对每一行，同样把出现 `1` 的列对应的位设为 `1`，得到 `rowMask[i]`。  
   - 例如 `n = 5`，一行是 `[0,1,0,1,0]` → `rowMask = 0b01010`。  

2. **判断行是否被覆盖**  
   - 设 `selectedMask` 为当前选中的列的二进制表示。  
   - 行被覆盖的条件是：`rowMask[i]` 中的所有 `1` 都出现在 `selectedMask` 中。  
   - 用位运算写成：`rowMask[i] & ~selectedMask == 0`。  
   - 解释：`~selectedMask` 把未选中的列对应的位设为 `1`，与 `rowMask` 做与运算后，只要出现 `1`，说明该行还有未被选中的 `1`，不满足覆盖。  

3. **枚举所有恰好 `numSelect` 列的组合**  
   - 仍然使用组合枚举，但每次得到的是一个整数的位掩码。  
   - 由于 `n ≤ 12`，我们可以把所有 `2^n`（最多 4096）种列子集预先生成，然后只挑出位数恰好等于 `numSelect` 的那些。  

这样做的好处是：  
- **判断是否覆盖** 只需要一次位运算，时间常数极低。  
- **空间** 只需要保存 `m` 个整数（每行的掩码），即 `O(m)`。  

#### 代码（Python）

```python
from itertools import combinations
from typing import List

def maxRowsCovered_opt(matrix: List[List[int]], numSelect: int) -> int:
    m, n = len(matrix), len(matrix[0])

    # 1️⃣ 把每一行的 1 的位置压成一个二进制整数（位掩码）
    row_masks = []
    for row in matrix:
        mask = 0
        for j, val in enumerate(row):
            if val == 1:
                mask |= 1 << j      # 第 j 列对应第 j 位设为 1
        row_masks.append(mask)      # 例如 0b01010

    best = 0

    # 2️⃣ 枚举所有恰好选取 numSelect 列的组合，直接生成位掩码
    #    这里使用 itertools.combinations 生成列下标的组合，然后转成 mask
    for cols in combinations(range(n), numSelect):
        selected_mask = 0
        for c in cols:
            selected_mask |= 1 << c   # 把选中的列对应位设为 1

        # 3️⃣ 统计这套列能覆盖多少行
        covered = 0
        for rm in row_masks:
            # 行的所有 1 必须已经在 selected_mask 中
            # 等价于 (rm & ~selected_mask) == 0
            if rm & ~selected_mask == 0:
                covered += 1

        best = max(best, covered)

    return best
```

**关键行中文注释**  
- `mask |= 1 << j`：把第 `j` 列对应的位「打开」——把 1 放进二进制的第 `j` 位。  
- `selected_mask |= 1 << c`：同理，把我们挑选的列也用位掩码表示。  
- `rm & ~selected_mask == 0`：判断该行的所有 1 是否都已经被选中的列覆盖。  

#### 复杂度  

- **时间复杂度**：`O( C(n, numSelect) * m )`  
  - 与暴力解的组合数相同，但每行检查只用了常数次位运算，省去了遍历列的 `O(n)`，所以整体更快。  
  - 例如 `n=12, numSelect=6` 时，大约 924 种组合 × 12 行 ≈ 1.1 万次位运算，几乎瞬间完成。  
- **空间复杂度**：`O(m)`  
  - 只存放 `m` 个整数的行掩码，远小于之前的集合/列表存储。  

---

## 心得  

- **核心技巧**：**位掩码 + 组合枚举**。把「列是否被选」和「行中 1 的分布」都压成二进制，再用位运算快速判断「全部在选中列里”。  
- **适用的题型**  
  1. **子集覆盖**（如「选择若干列覆盖所有行的 1」）  
  2. **集合交并判等**（如「判断两个集合是否相等」）  
  3. **状态压缩 DP**（如「旅行商问题」的 `dp[mask]`）  
- **一句话总结解题钥匙**：**用位掩码把「是否被选」变成「0/1」的二进制，再用位运算一次性验证整行是否满足**。  

---

## 反思  

- **第一反应**：看到「选若干列」和「行的 1 必须全部在选中列里」立刻想到「遍历所有列组合」——这在约束很小的情况下是最自然的暴力思路。  
- **最容易踩的坑**  
  - **忘记把全 0 行算作已覆盖**：在代码里要把 `rowMask == 0` 的情况也算进来（位运算自然满足）。  
  - **位数越界**：Python 整数位数不受限制，但在其他语言（如 C++）要确保使用足够宽的整数类型（`int`/`long long`）。  
  - **组合枚举的重复**：直接使用 `itertools.combinations` 能保证不重复，手写递归时要注意剪枝。  
- **下次遇到同类题**：第一步先思考「能否把集合信息压成二进制」，如果可以，就立刻转为 **位掩码**，再用 **枚举子集** 或 **动态规划** 来求最优。这样往往能把原本的指数遍历降到可接受的常数因子。