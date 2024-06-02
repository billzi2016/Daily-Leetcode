# #2718. 查询后矩阵元素之和 / Sum of Matrix After Queries

> 难度：中等 · 标签：Array、Hash Table · [LeetCode 链接](https://leetcode.com/problems/sum-of-matrix-after-queries/)

---

## 题目（英文原版）

**Description**

You are given an integer n and a 0-indexed 2D array queries where queries[i] = [typei, indexi, vali].
Initially, there is a 0-indexed n x n matrix filled with 0's. For each query, you must apply one of the following changes:
Return the sum of integers in the matrix after all queries are applied.

**Examples**

**Example 1:**

```
Input: n = 3, queries = [[0,0,1],[1,2,2],[0,2,3],[1,0,4]]
Output: 23
Explanation: The image above describes the matrix after each query. The sum of the matrix after all queries are applied is 23.
```

**Example 2:**

```
Input: n = 3, queries = [[0,0,4],[0,1,2],[1,0,1],[0,2,3],[1,2,1]]
Output: 17
Explanation: The image above describes the matrix after each query. The sum of the matrix after all queries are applied is 17.
```

**Constraints**

- 1 <= n <= 104
- 1 <= queries.length <= 5 * 104
- queries[i].length == 3
- 0 <= typei <= 1
- 0 <= indexi < n
- 0 <= vali <= 105

---

## 题目（中文翻译）

你得到一个整数 `n` 和一个 0 索引的二维数组 `queries`，其中 `queries[i] = [type_i, index_i, val_i]`。  
最初，有一个 0 索引的 `n × n` 矩阵，所有元素均为 `0`。对于每个查询，你必须执行以下两种操作之一（取决于 `type_i`）：

- `type_i = 0`：将第 `index_i` 行的所有元素设置为 `val_i`。
- `type_i = 1`：将第 `index_i` 列的所有元素设置为 `val_i`。

在全部查询执行完毕后，返回矩阵中所有整数的和。

**示例 1**  
**输入**: `n = 3, queries = [[0,0,1],[1,2,2],[0,2,3],[1,0,4]]`  
**输出**: `23`  
**解释**: 上图展示了每个查询执行后的矩阵状态。所有查询完成后矩阵中元素的和为 `23`。

**示例 2**  
**输入**: `n = 3, queries = [[0,0,4],[0,1,2],[1,0,1],[0,2,3],[1,2,1]]`  
**输出**: `17`  
**解释**: 上图展示了每个查询执行后的矩阵状态。所有查询完成后矩阵中元素的和为 `17`。

**约束条件**  
- `1 <= n <= 10^4`  
- `1 <= queries.length <= 5 * 10^4`  
- `queries[i].length == 3`  
- `0 <= type_i <= 1`  
- `0 <= index_i < n`  
- `0 <= val_i <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目给出一个 `n × n` 的全零矩阵，随后会有若干条查询：

- `type = 0` → 把第 `index` 行的所有元素全部改成 `val`  
- `type = 1` → 把第 `index` 列的所有元素全部改成 `val`

最直接的做法就是 **真的在矩阵里改**，每来一条查询，就遍历对应的整行或整列，把每个格子设成 `val`。  
这和生活中“把一排书全部换成同一本新书”差不多：我们把书架（行）上每一本书都换掉，或者把同一列的所有书都换掉。

**为什么正确**：因为每一次查询都严格按照题目要求把对应位置的数值改成 `val`，最终矩阵的每个格子都会是最近一次（即最新的）对它所在的行或列的修改结果。遍历完整个查询列表后，直接把矩阵所有元素相加即可得到答案。

#### 代码（Python）

```python
def matrix_sum_bruteforce(n: int, queries: list[list[int]]) -> int:
    # 1. 先建一个 n×n 的全 0 矩阵
    matrix = [[0] * n for _ in range(n)]

    # 2. 逐条处理查询
    for typ, idx, val in queries:
        if typ == 0:                      # 把第 idx 行全换成 val
            for col in range(n):
                matrix[idx][col] = val   # 行内每个格子都设为 val
        else:                             # 把第 idx 列全换成 val
            for row in range(n):
                matrix[row][idx] = val   # 列内每个格子都设为 val

    # 3. 把矩阵所有元素累加求和
    total = 0
    for row in matrix:
        total += sum(row)                # 一行的和直接用 sum
    return total
```

#### 复杂度

- **时间复杂度**：`O(q * n)`  
  `q` 为查询条数。每条查询都要遍历整行或整列，行/列的长度是 `n`，所以最坏情况下要做 `q × n` 次写操作。  
  用大白话说，如果 `n=1000`、`q=50000`，我们大约要写 5 0000 000 次数值。

- **空间复杂度**：`O(n²)`  
  我们真的在内存里保存了一个 `n × n` 的矩阵，矩阵里有 `n²` 个格子。  

> 暴力解的缺点在于 **矩阵太大**（`n` 可达 10⁴，`n²` 达到 10⁸，直接开数组会爆内存），而且每条查询都要遍历整行/列，导致运行时间超标。

---

### 2. 最优解

#### 思路  

从暴力解出发，**瓶颈** 在于：

1. **每次查询都遍历整行/整列**，导致 `O(n)` 的额外工作。  
2. **存整个矩阵**，占用 `O(n²)` 空间。

观察题目可以发现：**一次对同一行（或列）的后续查询会完全覆盖前面的修改**。也就是说，**只要我们知道该行（列）最后一次被修改的值，就不必关心之前的任何改动**。

这启示我们可以 **逆序** 处理查询：

- 从最后一条查询往前走，第一次遇到某行（列）时，这条查询一定是该行（列）最终的值，因为它之后的所有查询都已经在更靠前的位置（在原顺序中是更早的）了，**不会再影响**这行（列）。
- 记录已经“确定”了的行和列（用 `set`），以后再碰到同一行/列就直接跳过，因为它已经有了最终值。

逆序遍历的好处：

- 当我们处理到某条查询 `type = 0`（行）时，**只需要把这行中尚未被确定的列数目乘以 `val`**，因为这些列在以后（原顺序中）都不会再被改写。  
- 同理，`type = 1`（列）时，只需要把这列中尚未被确定的行数目乘以 `val`。

于是我们不必真的去写每个格子，只需要维护：

- `seen_rows`：已经确定了最终值的行集合  
- `seen_cols`：已经确定了最终值的列集合  
- `remaining_rows = n - len(seen_rows)`：还未确定的行数  
- `remaining_cols = n - len(seen_cols)`：还未确定的列数  

每处理一条查询，就把对应的 **贡献** 加到答案里，并把该行/列加入已见集合。

**类比**：想象有一张 `n × n` 的网格，网格里每个格子都是一盏灯，最初全是关的。我们一次把整行或整列的灯全部调到同一个亮度。逆序来看，就是从最后一次调灯开始往前追溯——当我们第一次碰到某行时，这行里那些还没有被“锁定”的灯（即对应的列还没被锁定）会被这一次的亮度决定，之后的调灯操作再也不会改动它们了。

#### 代码（Python）

```python
def matrix_sum_optimal(n: int, queries: list[list[int]]) -> int:
    """
    逆序遍历 queries，只记录每行/列的最终值，累计贡献即可。
    时间 O(q + n) ，空间 O(n)。
    """
    seen_rows = set()      # 已经确定最终值的行下标
    seen_cols = set()      # 已经确定最终值的列下标
    total = 0              # 累计矩阵的总和

    # 从最后一条查询往前遍历
    for typ, idx, val in reversed(queries):
        if typ == 0:                      # 操作行
            if idx in seen_rows:          # 这行已经确定，跳过
                continue
            # 这行还未确定，受影响的格子数 = 尚未确定的列数
            affected = n - len(seen_cols)
            total += affected * val       # 贡献 = 格子数 * 该行的值
            seen_rows.add(idx)            # 标记这行已确定
        else:                             # 操作列
            if idx in seen_cols:          # 这列已经确定，跳过
                continue
            # 这列还未确定，受影响的格子数 = 尚未确定的行数
            affected = n - len(seen_rows)
            total += affected * val       # 贡献 = 格子数 * 该列的值
            seen_cols.add(idx)            # 标记这列已确定

        # 若所有行和列都已经确定，后面的查询再也不会产生贡献，直接结束
        if len(seen_rows) == n and len(seen_cols) == n:
            break

    return total
```

#### 复杂度

- **时间复杂度**：`O(q + n)`  
  我们只遍历一次查询列表（`q` 次），每次只做集合的 `in`、`add`（均摊 O(1)）以及一次整数运算。再加上最多遍历 `n` 次集合大小检查，整体是线性的。相较于暴力的 `O(q·n)`，大幅提升。  
  用大白话说：如果 `q = 5·10⁴`、`n = 10⁴`，我们最多只做约 6 万次简单操作，几乎瞬间完成。

- **空间复杂度**：`O(n)`  
  只需要保存两套集合，最多各存 `n` 个整数（行下标或列下标），不需要整个矩阵。相比暴力的 `O(n²)`，省了大量内存。

---

## 心得

- **核心技巧**：逆序遍历 + 用集合记录“已经确定的行/列”。  
- **适用的题型**  
  1. “最后一次操作决定最终结果” 类似的问题，例如 *“Last Day Where You Can Still Cross”*（逆序二分）或 *“Maximum Row Sum After Queries”*（行列同理）。  
  2. 需要 **一次性计算整体贡献** 而不是逐格更新的矩阵/网格题，如 *“Matrix Diagonal Sum”* 的优化版。  
- **一句话总结解题钥匙**：**只关心每行/每列的最后一次修改，用集合记住已经锁定的行列，逆序累计贡献**。

---

## 反思

- **第一反应**：直接把矩阵实现出来，逐条更新——这是最自然的想法，但很快会因为 `n` 大而崩溃。  
- **最容易踩的坑**  
  - **忘记逆序**：如果正序遍历，一旦遇到同一行的多次修改，就会重复计数，需要额外的逻辑去“覆盖”。  
  - **集合更新错误**：一定要在计入贡献后再把行/列加入 `seen`，否则会把同一行的贡献算两次。  
  - **边界情况**：当所有行或所有列已经被锁定后，后面的查询不再产生贡献，提前 `break` 可以少做无意义的循环。  
- **下次遇到同类题**：第一步想到“**是否有‘最后一次决定’的特性**”，如果有，尝试 **逆序遍历** 并用 **集合/哈希表** 记录已经确定的对象，直接累加贡献而不是逐格更新。