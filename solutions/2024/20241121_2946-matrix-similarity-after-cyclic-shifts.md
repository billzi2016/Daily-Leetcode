# #2946. 循环移位后的矩阵相似性 / Matrix Similarity After Cyclic Shifts

> 难度：简单 · 标签：Array、Math、Matrix、Simulation · [LeetCode 链接](https://leetcode.com/problems/matrix-similarity-after-cyclic-shifts/)

---

## 题目（英文原版）

**Description**

You are given an m x n integer matrix mat and an integer k. The matrix rows are 0-indexed.
The following proccess happens k times:
Return true if the final modified matrix after k steps is identical to the original matrix, and false otherwise.

**Examples**

**Example 1:**

```
Input: mat = [[1,2,3],[4,5,6],[7,8,9]], k = 4
Output: false
Explanation:
In each step left shift is applied to rows 0 and 2 (even indices), and right shift to row 1 (odd index).
```

**Example 2:**

```
Input: mat = [[1,2,1,2],[5,5,5,5],[6,3,6,3]], k = 2
Output: true
Explanation:
```

**Example 3:**

```
Input: mat = [[2,2],[2,2]], k = 3
Output: true
Explanation:
As all the values are equal in the matrix, even after performing cyclic shifts the matrix will remain the same.
```

**Constraints**

- 1 <= mat.length <= 25
- 1 <= mat[i].length <= 25
- 1 <= mat[i][j] <= 25
- 1 <= k <= 50

---

## 题目（中文翻译）

给定一个 `m × n` 整数矩阵 `mat` 和一个整数 `k`。矩阵的行采用 **0 索引**。  
接下来将进行 `k` 次如下过程：

- 对每一行，如果行索引为偶数，则对该行执行一次左循环移位（left shift），即把最左边的元素移到最右边；
- 如果行索引为奇数，则对该行执行一次右循环移位（right shift），即把最右边的元素移到最左边。

在完成 `k` 步后，若得到的矩阵与最初的矩阵 **完全相同**，返回 `true`；否则返回 `false`。

---

### 示例

#### 示例 1
```
Input: mat = [[1,2,3],[4,5,6],[7,8,9]], k = 4
Output: false
Explanation:
在每一步中，对索引为偶数的行（0 行和 2 行）执行左循环移位，对索引为奇数的行（1 行）执行右循环移位。
```

#### 示例 2
```
Input: mat = [[1,2,1,2],[5,5,5,5],[6,3,6,3]], k = 2
Output: true
Explanation:
经过两次循环移位后，矩阵恢复到原来的形状。
```

#### 示例 3
```
Input: mat = [[2,2],[2,2]], k = 3
Output: true
Explanation:
矩阵中所有元素相同，无论进行多少次循环移位，矩阵都保持不变。
```

---

### 约束条件

- `1 ≤ mat.length ≤ 25`
- `1 ≤ mat[i].length ≤ 25`
- `1 ≤ mat[i][j] ≤ 25`
- `1 ≤ k ≤ 50`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**一步步模拟**题目描述的过程：

1. 读取矩阵 `mat`，记住原始矩阵 `orig`（因为最后要和它比较）。  
2. 重复 `k` 次：
   - 对下标为 **偶数** 的行做一次 **左循环移位**（把第一个元素搬到行尾）。
   - 对下标为 **奇数** 的行做一次 **右循环移位**（把最后一个元素搬到行首）。
3. 循环结束后，把得到的矩阵 `mat` 和 `orig` 挨个元素比较，全部相同则返回 `True`，否则返回 `False`。

> **类比**：把每一行想成一本书的书页，左移相当于把第一页翻到书的最后一页，右移则是把最后一页翻到最前面。我们一次只翻一页，重复 `k` 次，最后看所有书是否仍然保持原来的顺序。

**为什么正确**  
因为我们严格按照题目规定的「每一步」去变换矩阵，所有的行移动都没有遗漏，也没有额外的操作。经过 `k` 步的真实变换后，矩阵的状态一定就是我们模拟得到的状态，所以直接比较即可得到答案。

**复杂度分析（大白话版）**  

- **时间复杂度**：每一步我们都要遍历所有 `m × n` 个元素进行移位，重复 `k` 次，时间是 `O(k · m · n)`。如果把 `k` 想成「跑了多少圈」，每跑一圈就要检查整张表一次，所以总工作量随圈数线性增长。
- **空间复杂度**：我们额外保存一份原始矩阵 `orig`（大小也是 `m × n`），所以是 `O(m·n)`。如果把原矩阵视为「原始资料」，我们只多占用了同等大小的纸张。

#### 代码（Python）

```python
def are_similar_bruteforce(mat, k):
    """
    暴力模拟 k 步循环移位后，矩阵是否和原矩阵相同
    """
    m, n = len(mat), len(mat[0])
    # 复制一份原始矩阵，用于最后比较
    orig = [row[:] for row in mat]

    # 逐步执行 k 次移位
    for step in range(k):
        for i in range(m):
            if i % 2 == 0:               # 偶数行 → 左移 1 位
                first = mat[i][0]
                for j in range(n - 1):
                    mat[i][j] = mat[i][j + 1]
                mat[i][n - 1] = first
            else:                         # 奇数行 → 右移 1 位
                last = mat[i][n - 1]
                for j in range(n - 1, 0, -1):
                    mat[i][j] = mat[i][j - 1]
                mat[i][0] = last

    # 与原矩阵逐元素比较
    for i in range(m):
        for j in range(n):
            if mat[i][j] != orig[i][j]:
                return False
    return True
```

#### 复杂度

- **时间复杂度**：`O(k·m·n)` — 例如 `k=50, m=n=25` 时最多会做 `50·25·25 = 31250` 次基本操作，仍在可接受范围。
- **空间复杂度**：`O(m·n)` — 需要保存原始矩阵的副本。

---

### 2. 最优解

#### 思路  

从暴力解出发，我们发现 **瓶颈** 在于每一步都遍历整张矩阵进行移位。其实我们并不需要真的把矩阵一次次“翻页”，只要 **知道每行最终会被左/右移动多少位**，就能直接判断它们是否会恢复原样。

关键观察：

1. **循环移位的周期**是列数 `n`。左/右移动 `n` 次后，行会回到原来的顺序。  
   → 把 `k` 取模 `n`，只需要考虑 `k' = k % n` 次实际移动即可。  
2. 偶数行左移 `k'` 位、奇数行右移 `k'` 位。左移 `k'` 位等价于把行切成两段 `A|B`（`A` 为前 `k'` 个元素），再拼成 `B+A`；右移则是 `A|B`（`A` 为前 `n‑k'` 个元素）拼成 `B+A`。  
3. 对每一行，只要把它 **按照对应方向**旋转 `k'` 位后，和原行完全相同，就说明这行在 `k` 步后会恢复。所有行都满足则整体相同。

> **类比**：想象每行是一条环形跑道，左移 `k'` 步相当于顺时针跑 `k'` 步，右移则逆时针跑 `k'` 步。跑完 `k'` 步后，如果你恰好回到起点（即跑道上的标记和起点重合），说明这行没有变化。

实现细节：

- 先把 `k` 化简为 `k' = k % n`，因为多余的整圈不会影响结果。  
- 对每行 `i`：
  - 若 `i` 为偶数，用切片 `row[k':] + row[:k']` 产生左移后的新行；
  - 若 `i` 为奇数，用切片 `row[-k':] + row[:-k']`（或 `row[n-k':] + row[:n-k']`）产生右移后的新行；
  - 比较新行与原行是否相同。  
- 若所有行都相同，返回 `True`，否则 `False`。

这样我们只遍历 **一次** 矩阵，每行只做常数次切片操作，时间从 `O(k·m·n)` 降到 `O(m·n)`，空间只用常数额外空间。

#### 代码（Python）

```python
def are_similar(mat, k):
    """
    最优解：只需一次遍历，利用循环移位的周期性直接判断。
    """
    m, n = len(mat), len(mat[0])
    # 只保留 k 在 [0, n-1] 之间的有效位移
    shift = k % n
    if shift == 0:                 # 完全不需要移动，直接相等
        return True

    for i in range(m):
        row = mat[i]
        if i % 2 == 0:             # 偶数行 → 左移 shift 位
            shifted = row[shift:] + row[:shift]
        else:                       # 奇数行 → 右移 shift 位
            shifted = row[-shift:] + row[:-shift]
        # 与原行逐元素比较
        if shifted != row:
            return False
    return True
```

#### 复杂度

- **时间复杂度**：`O(m·n)` — 只遍历矩阵一次。即使 `k` 很大（如 10⁹），我们先取模后只做 `n` 次比较，速度始终与矩阵大小成正比。
- **空间复杂度**：`O(1)` — 只使用常数级别的额外变量（`shift`、`shifted`），不随输入规模增长。

---

## 心得

- **核心技巧**：**利用循环移位的周期性**（`k % n`），把多次模拟压缩为一次直接比较。  
- **适用场景**：  
  1. 任意**循环移位**问题（如数组/字符串旋转后是否相等）。  
  2. **行/列交替方向**的矩阵变换（如奇偶行分别左/右移）。  
  3. **周期性操作**的判等（如每次加 1 mod `M` 的数列是否回到起点）。  
- **一句话总结**：把“做多少次”换算成“最终会怎样”，不必真的去做每一次。

---

## 反思

- **第一反应**：直接写循环模拟，感觉最安全。  
- **最容易踩的坑**：  
  - 忘记对 `k` 取模 `n`，导致不必要的循环，尤其 `k` 可能很大。  
  - 右移的切片写法容易写错（`row[-shift:] + row[:-shift]` 与 `row[n-shift:] + row[:n-shift]` 要对应）。  
  - 当 `shift == 0` 时直接返回 `True`，否则切片会产生空列表导致错误比较。  
- **下次遇到同类题**：第一步先思考“这类操作的周期是多少”，把大步数压缩成**等价的最小步数**，再决定是直接比较还是再做进一步优化。