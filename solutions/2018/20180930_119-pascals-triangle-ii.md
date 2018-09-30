# #119. 帕斯卡三角形 II / Pascal's Triangle II

> 难度：简单 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/pascals-triangle-ii/)

---

## 题目（英文原版）

**Description**

Given an integer rowIndex, return the rowIndexth (0-indexed) row of the Pascal's triangle.
In Pascal's triangle, each number is the sum of the two numbers directly above it as shown:
Follow up: Could you optimize your algorithm to use only O(rowIndex) extra space?

**Examples**

**Example 1:**

```
Input: rowIndex = 3
Output: [1,3,3,1]
```

**Example 2:**

```
Input: rowIndex = 0
Output: [1]
```

**Example 3:**

```
Input: rowIndex = 1
Output: [1,1]
```

**Constraints**

- 0 <= rowIndex <= 33

---

## 题目（中文翻译）

给定一个整数 `rowIndex`，返回帕斯卡三角形（Pascal's triangle）中第 `rowIndex` 行（0 基索引）的所有元素。

在帕斯卡三角形中，每个数字等于其正上方左侧和右侧两个数字之和，如下所示：

**示例 1**  
**示例 2**  
**示例 3**

**进阶**：你能否将算法优化至仅使用 O(rowIndex) 的额外空间？

---

### 示例

**示例 1**  
输入: `rowIndex = 3`  
输出: `[1,3,3,1]`

**示例 2**  
输入: `rowIndex = 0`  
输出: `[1]`

**示例 3**  
输入: `rowIndex = 1`  
输出: `[1,1]`

### 约束条件

- `0 <= rowIndex <= 33`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **把整个 Pascal 三角形先算出来**，再把第 `rowIndex` 行取出来返回。  
Pascal 三角形的生成规则很像“层层递进”的建筑：

- 第 0 行只有一个 `1`（就像第一层只有一块砖）。
- 第 i 行的第 j 个数（`0 ≤ j ≤ i`）等于上一行第 `j-1` 个数和第 `j` 个数之和。  
  > 可以把它想成在上一层的两块砖上各放一块砖，新的砖的高度是它们高度之和。

实现时我们可以使用一个二维列表 `triangle`，`triangle[i][j]` 存第 i 行第 j 个数。  
遍历每一行，按照上面的递推公式填值，最后返回 `triangle[rowIndex]` 即可。

> **为什么正确？**  
> 递推公式正是 Pascal 三角形的定义，逐行、逐列按照定义计算，必然得到正确的三角形。

#### 代码（Python）

```python
def getRow(rowIndex: int):
    # 用一个二维列表保存每一行，triangle[i] 是第 i 行
    triangle = []

    for i in range(rowIndex + 1):          # 需要算到第 rowIndex 行（包括它）
        # 第 i 行有 i+1 个数，先全部填 1，边界处都是 1
        row = [1] * (i + 1)

        # 对于内部的数（不在两端），按照 Pascal 规则更新
        # j 从 1 开始，到 i-1（不包括两端的 1）
        for j in range(1, i):
            # 上一行的第 j-1 和第 j 个数相加得到当前行的第 j 个数
            row[j] = triangle[i - 1][j - 1] + triangle[i - 1][j]

        # 把算好的这一行放进 triangle，供后面行使用
        triangle.append(row)

    # 返回第 rowIndex 行
    return triangle[rowIndex]
```

#### 复杂度

- **时间复杂度：** `O(rowIndex²)`  
  > 因为我们要算 `0 … rowIndex` 共 `rowIndex+1` 行，第 i 行需要遍历 i 次，所有遍历次数相加就是 `1 + 2 + … + rowIndex = O(rowIndex²)`。可以把 `O(rowIndex²)` 想成“如果 rowIndex 是 100，循环大约会执行 10 000 次”。

- **空间复杂度：** `O(rowIndex²)`  
  > 我们把整棵三角形都存了下来，需要的空间和行数的平方成正比。对于 `rowIndex = 33`，最多只会存 34 行，总共 595 个整数，仍然很小，但在理论上是二次空间。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于我们把所有行都保存了，实际上只需要**最后一行**。  
如果我们在计算第 i 行时，只保留当前行本身，而不再需要前面所有行的完整数据，就可以把空间降到 `O(rowIndex)`。

关键点是：**第 i 行的每个数只依赖于第 i‑1 行的两个相邻数**。  
因此我们可以使用「一维滚动数组」的技巧，从后向前更新数组，这样在更新 `row[j]` 时，`row[j-1]` 仍然是上一行的值，而 `row[j]` 还未被覆盖。

实现步骤：

1. 创建一个长度为 `rowIndex+1` 的列表 `row`，全部初始化为 `1`（每行两端都是 1）。
2. 从第 2 行开始（`i = 2`），向后遍历（`j` 从 `i-1` 到 `1`），用公式  
   `row[j] = row[j] + row[j-1]` 更新。  
   - 因为我们是从右往左更新，`row[j]` 仍是上一行的值，`row[j-1]` 也是上一行的值，两者相加得到当前行的值。
3. 循环结束后，`row` 正好是第 `rowIndex` 行。

> **类比**：想象你在一条绳子上依次写数字，每次要把新一行的数字写在旧数字的上面。为了不把旧数字抹掉，我们从右边往左边写，这样左边的旧数字还在，右边的已经是新数字了。

#### 代码（Python）

```python
def getRow(rowIndex: int):
    # 初始化，只包含最左边的 1，长度为 rowIndex+1，其他位置先填 0（后面会被覆盖）
    row = [1] * (rowIndex + 1)

    # 从第 2 行开始往下构造（第 0、1 行已经是全 1 了）
    for i in range(2, rowIndex + 1):
        # 从右往左更新，避免覆盖掉左侧还需要使用的旧值
        # j 的取值范围是 i-1 … 1（两端的 1 不需要更新）
        for j in range(i - 1, 0, -1):
            # row[j]（旧的）+ row[j-1]（旧的） => 新的 row[j]
            row[j] = row[j] + row[j - 1]

    return row
```

#### 复杂度

- **时间复杂度：** `O(rowIndex²)`  
  > 虽然空间降了，但我们仍然要遍历每一行的内部元素，累计的操作次数仍是 `1 + 2 + … + rowIndex = O(rowIndex²)`。可以把它理解为「行数多了，内部的加法次数也会多」。

- **空间复杂度：** `O(rowIndex)`  
  > 只用了一个长度为 `rowIndex+1` 的列表来保存当前行，空间随 `rowIndex` 线性增长。相当于「只需要一条绳子」而不是整棵树。

---

## 心得

- **核心技巧**：一维滚动数组（从右往左更新），在需要“只保留上一层信息”时非常有用。
- **适用的题型**  
  1. **Pascal 三角形第 k 行**（本题）  
  2. **计算组合数 C(n, k) 只用一维 DP**（LeetCode 518）  
  3. **背包问题的空间优化**（0/1 背包只保留一维 DP 数组）
- **一句话总结解题钥匙**：**“从后往前更新，避免覆盖掉还需要的旧数据”。**

---

## 反思

- **第一反应**：先把整个三角形算出来再取第 `rowIndex` 行——最直观但空间浪费。
- **最容易踩的坑**  
  - **更新顺序错误**：如果从左往右更新，`row[j-1]` 已经是新一行的值，会导致错误结果。  
  - **边界处理**：`rowIndex = 0` 或 `1` 时，直接返回 `[1]` 或 `[1,1]`，循环不应执行。  
  - **列表长度**：一定要提前创建长度为 `rowIndex+1`，否则在更新时会出现 IndexError。
- **下次类似题的第一步**：先思考「本层只依赖上一层的哪些位置」——如果只依赖相邻位置，就尝试一维滚动更新，省空间。