# #1476. 子矩形查询 / Subrectangle Queries

> 难度：中等 · 标签：Array、Design、Matrix · [LeetCode 链接](https://leetcode.com/problems/subrectangle-queries/)

---

## 题目（英文原版）

**Description**

Implement the class SubrectangleQueries which receives a rows x cols rectangle as a matrix of integers in the constructor and supports two methods:
1. updateSubrectangle(int row1, int col1, int row2, int col2, int newValue)
2. getValue(int row, int col)

**Examples**

**Example 1:**

```
Input
["SubrectangleQueries","getValue","updateSubrectangle","getValue","getValue","updateSubrectangle","getValue","getValue"]
[[[[1,2,1],[4,3,4],[3,2,1],[1,1,1]]],[0,2],[0,0,3,2,5],[0,2],[3,1],[3,0,3,2,10],[3,1],[0,2]]
Output
[null,1,null,5,5,null,10,5]
Explanation
SubrectangleQueries subrectangleQueries = new SubrectangleQueries([[1,2,1],[4,3,4],[3,2,1],[1,1,1]]);  
// The initial rectangle (4x3) looks like:
// 1 2 1
// 4 3 4
// 3 2 1
// 1 1 1
subrectangleQueries.getValue(0, 2); // return 1
subrectangleQueries.updateSubrectangle(0, 0, 3, 2, 5);
// After this update the rectangle looks like:
// 5 5 5
// 5 5 5
// 5 5 5
// 5 5 5 
subrectangleQueries.getValue(0, 2); // return 5
subrectangleQueries.getValue(3, 1); // return 5
subrectangleQueries.updateSubrectangle(3, 0, 3, 2, 10);
// After this update the rectangle looks like:
// 5   5   5
// 5   5   5
// 5   5   5
// 10  10  10 
subrectangleQueries.getValue(3, 1); // return 10
subrectangleQueries.getValue(0, 2); // return 5
```

**Example 2:**

```
Input
["SubrectangleQueries","getValue","updateSubrectangle","getValue","getValue","updateSubrectangle","getValue"]
[[[[1,1,1],[2,2,2],[3,3,3]]],[0,0],[0,0,2,2,100],[0,0],[2,2],[1,1,2,2,20],[2,2]]
Output
[null,1,null,100,100,null,20]
Explanation
SubrectangleQueries subrectangleQueries = new SubrectangleQueries([[1,1,1],[2,2,2],[3,3,3]]);
subrectangleQueries.getValue(0, 0); // return 1
subrectangleQueries.updateSubrectangle(0, 0, 2, 2, 100);
subrectangleQueries.getValue(0, 0); // return 100
subrectangleQueries.getValue(2, 2); // return 100
subrectangleQueries.updateSubrectangle(1, 1, 2, 2, 20);
subrectangleQueries.getValue(2, 2); // return 20
```

**Constraints**

- There will be at most 500 operations considering both methods: updateSubrectangle and getValue.
- 1 <= rows, cols <= 100
- rows == rectangle.length
- cols == rectangle[i].length
- 0 <= row1 <= row2 < rows
- 0 <= col1 <= col2 < cols
- 1 <= newValue, rectangle[i][j] <= 10^9
- 0 <= row < rows
- 0 <= col < cols

---

## 题目（中文翻译）

实现一个类 `SubrectangleQueries`，在构造函数中接受一个 `rows x cols` 的整数矩阵 `rectangle`，并支持以下两种操作：

1. `updateSubrectangle(int row1, int col1, int row2, int col2, int newValue)`  
   将左上角坐标为 `(row1, col1)`、右下角坐标为 `(row2, col2)` 的子矩形（subrectangle）中的所有元素更新为 `newValue`。

2. `getValue(int row, int col)`  
   返回矩阵中坐标 `(row, col)` 处的当前值。

---

### 示例

#### 示例 1

```json
Input
["SubrectangleQueries","getValue","updateSubrectangle","getValue","getValue","updateSubrectangle","getValue","getValue"]
[[[[1,2,1],[4,3,4],[3,2,1],[1,1,1]]],[0,2],[0,0,3,2,5],[0,2],[3,1],[3,0,3,2,10],[3,1],[0,2]]
Output
[null,1,null,5,5,null,10,5]
```

**Explanation**  
```java
SubrectangleQueries subrectangleQueries = new SubrectangleQueries(
    [[1,2,1],
     [4,3,4],
     [3,2,1],
     [1,1,1]]
);
// 初始矩形为 4 行 3 列

subrectangleQueries.getValue(0, 2);            // 返回 1
subrectangleQueries.updateSubrectangle(0, 0, 3, 2, 5); // 将左上角 (0,0) 到右下角 (3,2) 的所有元素更新为 5
subrectangleQueries.getValue(0, 2);            // 返回 5
subrectangleQueries.getValue(3, 1);            // 返回 5
subrectangleQueries.updateSubrectangle(3, 0, 3, 2, 10); // 将第 3 行的所有元素更新为 10
subrectangleQueries.getValue(3, 1);            // 返回 10
subrectangleQueries.getValue(0, 2);            // 返回 5
```

#### 示例 2

```json
Input
["SubrectangleQueries","getValue","updateSubrectangle","getValue","getValue","updateSubrectangle","getValue"]
[[[[1,1,1],[2,2,2],[3,3,3]]],[0,0],[0,0,2,2,100],[0,0],[2,2],[1,1,2,2,20],[2,2]]
Output
[null,1,null,100,100,null,20]
```

**Explanation**  
```java
SubrectangleQueries subrectangleQueries = new SubrectangleQueries(
    [[1,1,1],
     [2,2,2],
     [3,3,3]]
);
subrectangleQueries.getValue(0, 0);            // 返回 1
subrectangleQueries.updateSubrectangle(0, 0, 2, 2, 100); // 将整个矩形更新为 100
subrectangleQueries.getValue(0, 0);            // 返回 100
subrectangleQueries.getValue(2, 2);            // 返回 100
subrectangleQueries.updateSubrectangle(1, 1, 2, 2, 20); // 将右下角的 2×2 区域更新为 20
subrectangleQueries.getValue(2, 2);            // 返回 20
```

---

### 约束条件

- `updateSubrectangle` 与 `getValue` 两个方法的调用总次数不超过 500 次。  
- `1 <= rows, cols <= 100`  
- `rows == rectangle.length`  
- `cols == rectangle[i].length`  
- `0 <= row1 <= row2 < rows`  
- `0 <= col1 <= col2 < cols`  
- `1 <= newValue, rectangle[i][j] <= 10^9`  
- `0 <= row < rows`  
- `0 <= col < cols`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**把矩形直接改掉**，然后在查询时直接读取矩阵里的值。

- **数据结构**：直接把输入的二维列表 `rectangle` 当作我们的矩阵。  
  - 可以把它想象成一张电子表格，行号是行，列号是列，单元格里存的是数字。  
- **为什么正确**：`updateSubrectangle` 的要求是把左上角 `(row1, col1)` 到右下角 `(row2, col2)` 的所有格子改成 `newValue`。我们只要遍历这块子矩形的每一个格子，把它们的值设为 `newValue` 即可。之后 `getValue` 只要返回矩阵对应位置的数，就一定是最新的值。  
- **复杂度分析**：  
  - `updateSubrectangle` 需要遍历子矩形的所有格子，最多遍历 `rows * cols`（整个矩阵）个格子。我们把大写的 **O** 看作 “数量级”。所以时间复杂度是 **O(m·n)**，这里 `m = rows, n = cols`。如果把它说成 “最多 10,000 次操作”，更容易理解。  
  - `getValue` 只做一次下标访问，时间是 **O(1)**（常数时间），也就是“几乎不花时间”。  
  - 额外空间只用到了原矩阵本身，没有额外的数组，空间复杂度 **O(1)**（不随输入规模增长）。

#### 代码（Python）

```python
class SubrectangleQueries:
    def __init__(self, rectangle):
        """
        初始化时直接保存原矩阵。
        rectangle 是一个二维列表，例如 [[1,2,1],[4,3,4],...]
        """
        # 直接把列表引用保存下来，后面会直接在上面修改
        self.rect = rectangle

    def updateSubrectangle(self, row1, col1, row2, col2, newValue):
        """
        把左上 (row1, col1) 到右下 (row2, col2) 的所有格子改成 newValue。
        """
        for r in range(row1, row2 + 1):          # 行号从 row1 到 row2（含）
            for c in range(col1, col2 + 1):      # 列号从 col1 到 col2（含）
                self.rect[r][c] = newValue       # 把对应位置改成 newValue

    def getValue(self, row, col):
        """
        直接返回矩阵中 (row, col) 位置的数。
        """
        return self.rect[row][col]
```

#### 复杂度

- **时间复杂度**  
  - `updateSubrectangle`：**O(m·n)**，其中 `m` 为行数、`n` 为列数。相当于“最坏情况下要遍历整张表”。  
  - `getValue`：**O(1)**，只做一次下标访问，几乎不耗时。  

- **空间复杂度**  
  - **O(1)**，只用了原矩阵，没有额外随输入规模增长的存储。

---

### 2. 最优解

#### 思路  

虽然暴力更新已经能在题目限制（最多 500 次操作，矩阵最大 100×100）下 AC，但我们仍可以把 **更新的成本降到 O(1)**，把查询的成本稍微提升一点。思路如下：

1. **观察瓶颈**：在暴力解里，`updateSubrectangle` 需要遍历子矩形的每个格子，这在子矩形很大的时候会比较慢。  
2. **把“改”推迟**：我们可以不立即改矩阵，而是把这次更新的**信息记录下来**（记录四个坐标和新的数值）。  
3. **查询时回溯**：当 `getValue(row, col)` 被调用时，检查所有历史更新（从最近的到最早的），看有没有哪一次覆盖了 `(row, col)`。如果找到了，返回对应的 `newValue`；否则返回原矩阵里的值。  
4. **核心数据结构**：一个列表 `updates`，每条记录是 `(row1, col1, row2, col2, newValue)`。列表就像一本“更新日志”。  
5. **复杂度对比**：  
   - `updateSubrectangle` 只需要把这条记录 **追加** 到列表，时间 **O(1)**。  
   - `getValue` 最多遍历所有历史更新（≤500 条），时间 **O(k)**，其中 `k` 是更新次数。因为 `k ≤ 500`，这仍然是常数级别的开销。  

> 类比：把矩阵看成一本书，暴力解是每次改动都直接在纸上涂改；最优解是把每次改动写进批注本，读时先看看批注本里有没有对应的改动。

#### 代码（Python）

```python
class SubrectangleQueries:
    def __init__(self, rectangle):
        """
        保存原矩阵和一个空的更新日志。
        """
        self.original = rectangle          # 原始矩阵，永远不变
        self.updates = []                  # 每次 update 的记录列表

    def updateSubrectangle(self, row1, col1, row2, col2, newValue):
        """
        只把这次更新的信息加入日志，实际不改矩阵。
        """
        # 追加一条记录 (左上行, 左上列, 右下行, 右下列, 新的数值)
        self.updates.append((row1, col1, row2, col2, newValue))

    def getValue(self, row, col):
        """
        从最近的更新开始倒着检查，哪条更新覆盖了 (row, col)。
        如果找到，直接返回对应的 newValue；
        否则返回原矩阵里的值。
        """
        # 倒序遍历，使得最近的更新拥有最高优先级
        for r1, c1, r2, c2, val in reversed(self.updates):
            if r1 <= row <= r2 and c1 <= col <= c2:
                return val                # 这条更新覆盖了查询位置
        # 没有任何更新覆盖，返回原始矩阵的值
        return self.original[row][col]
```

#### 复杂度

- **时间复杂度**  
  - `updateSubrectangle`：**O(1)**，只把一条记录加入列表。  
  - `getValue`：**O(k)**，`k` 为累计的更新次数（ ≤ 500 ），相当于“最多检查 500 条批注”。在最坏情况下仍然是常数级别，因为 500 是一个很小的固定上限。  

- **空间复杂度**  
  - **O(k)**，需要保存所有更新记录。最坏保存 500 条，每条只占 5 个整数，空间非常有限。

---

## 心得

- **核心技巧**：**懒更新（延迟操作）+ 记录日志**。把本应该在更新时完成的工作，推迟到查询时再处理。  
- **适用的题型**  
  1. 区间赋值后查询单点值（如本题、LeetCode 307. Range Sum Query – Mutable 的简化版）。  
  2. “画图后查询颜色”类问题（LeetCode 1470. Shuffle the Array 的思路类似）。  
- **一句话总结**：**把每次改动记下来，查询时从最新的记录往前找**，即可把更新成本降到 O(1)。

## 反思

- **第一反应**：直接遍历子矩形并改值——最直观、最容易实现的办法。  
- **最容易踩的坑**  
  - **边界**：记得 `row2`、`col2` 是 **包含**的，需要使用 `<=` 而不是 `<`。  
  - **更新顺序**：如果使用正序遍历日志，后来的更新会被前面的覆盖，导致返回错误的值。必须倒序检查或把最新的记录放在列表末尾并倒着遍历。  
  - **空间泄漏**：虽然题目限制小，但如果把每次更新都复制整个矩阵，会导致 O(m·n·k) 的空间爆炸。记录参数即可。  
- **下次遇到同类题**：第一步先思考“是否可以把改动记录下来，而不是立刻改动”。如果操作次数远大于查询次数，往往可以把查询成本稍微提升来换取更快的更新。