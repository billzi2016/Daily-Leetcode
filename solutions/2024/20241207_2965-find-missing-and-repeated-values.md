# #2965. 找到缺失与重复的数值 / Find Missing and Repeated Values

> 难度：简单 · 标签：Array、Hash Table、Math、Matrix · [LeetCode 链接](https://leetcode.com/problems/find-missing-and-repeated-values/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed 2D integer matrix grid of size n * n with values in the range [1, n2]. Each integer appears exactly once except a which appears twice and b which is missing. The task is to find the repeating and missing numbers a and b.
Return a 0-indexed integer array ans of size 2 where ans[0] equals to a and ans[1] equals to b.

**Examples**

**Example 1:**

```
Input: grid = [[1,3],[2,2]]
Output: [2,4]
Explanation: Number 2 is repeated and number 4 is missing so the answer is [2,4].
```

**Example 2:**

```
Input: grid = [[9,1,7],[8,9,2],[3,4,6]]
Output: [9,5]
Explanation: Number 9 is repeated and number 5 is missing so the answer is [9,5].
```

**Constraints**

- 2 <= n == grid.length == grid[i].length <= 50
- 1 <= grid[i][j] <= n * n
- For all x that 1 <= x <= n * n there is exactly one x that is not equal to any of the grid members.
- For all x that 1 <= x <= n * n there is exactly one x that is equal to exactly two of the grid members.
- For all x that 1 <= x <= n * n except two of them there is exactly one pair of i, j that 0 <= i, j <= n - 1 and grid[i][j] == x.

---

## 题目（中文翻译）

你被给定一个 **0 索引（0-indexed）** 的二维整数矩阵 `grid`，其大小为 `n × n`，矩阵中的数值均在 `[1, n²]` 范围内。除了一个数 `a` 出现两次，另一个数 `b` 完全缺失之外，其他每个整数恰好出现一次。  
请找出重复的数 `a` 与缺失的数 `b`。  

返回一个 **0 索引（0-indexed）** 的整数数组 `ans`，长度为 `2`，其中 `ans[0]` 为 `a`，`ans[1]` 为 `b`。  

## 示例

### 示例 1
```
Input: grid = [[1,3],[2,2]]
Output: [2,4]
Explanation: 数字 2 重复出现，数字 4 缺失，因此答案为 [2,4]。
```

### 示例 2
```
Input: grid = [[9,1,7],[8,9,2],[3,4,6]]
Output: [9,5]
Explanation: 数字 9 重复出现，数字 5 缺失，因此答案为 [9,5]。
```

## 约束条件
- `2 ≤ n == grid.length == grid[i].length ≤ 50`
- `1 ≤ grid[i][j] ≤ n * n`
- 对于所有 `x`，满足 `1 ≤ x ≤ n * n`，恰好有一个 `x` 不等于矩阵中的任何元素（即缺失的数）。
- 对于所有 `x`，满足 `1 ≤ x ≤ n * n`，恰好有一个 `x` 等于矩阵中恰好两个元素（即重复的数）。
- 对于除上述两个数之外的所有 `x`（`1 ≤ x ≤ n * n`），恰好存在唯一一对下标 `(i, j)`，`0 ≤ i, j ≤ n - 1` 且 `grid[i][j] == x`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把矩阵里所有的数都 **逐个检查**，看看哪个数出现了两次，哪个数根本没出现。  
我们可以把「出现次数」记在一个 **哈希表**（在 Python 中用 `dict`）里：

- 哈希表就像一本字典，**key** 是数字本身，**value** 是它出现的次数。  
- 当我们把每个格子里的数放进去时，如果发现某个 `key` 已经有 `value == 1`，说明这就是重复的数 `a`。  
- 把所有数字都放进去后，再遍历 `1 … n²`，找出 **没有出现在哈希表里的** 那个数字，就是缺失的数 `b`。

这种做法一定能得到正确答案，因为我们检查了**所有**可能的数字。

**时间复杂度**：我们要遍历矩阵 `n²` 次，然后再遍历 `1 … n²` 一次，整体是 `O(n² + n²) = O(n²)`。  
在大白话里，`O(n²)` 就是「和矩阵里格子一样多的操作」，如果矩阵是 5×5，就要做 25 次左右的事。

**空间复杂度**：需要一个大小为 `n²+1` 的哈希表（或者普通数组）来记录出现次数，空间是 `O(n²)`。  
可以把它想象成「我们为每个可能的数字准备了一个小抽屉」，抽屉的数量和数字的范围一样多。

#### 代码（Python）

```python
def findMissingAndRepeated(grid):
    n = len(grid)                     # 矩阵的边长
    max_val = n * n                   # 最大可能的数字
    freq = {}                         # 用字典记录每个数字出现的次数

    # 1️⃣ 把所有格子里的数放进字典
    for i in range(n):
        for j in range(n):
            val = grid[i][j]
            freq[val] = freq.get(val, 0) + 1   # 出现次数 +1

    repeated = -1                     # 用来保存重复的数 a
    missing = -1                      # 用来保存缺失的数 b

    # 2️⃣ 找出重复的数（出现次数为 2 的就是 a）
    for num, cnt in freq.items():
        if cnt == 2:
            repeated = num
            break

    # 3️⃣ 在 1~n² 中找没有出现的数，就是缺失的 b
    for num in range(1, max_val + 1):
        if num not in freq:           # 没有键对应到它，说明没有出现过
            missing = num
            break

    return [repeated, missing]
```

#### 复杂度

- **时间复杂度**：`O(n²)` — 需要遍历矩阵一次（`n²` 次）再遍历 `1…n²` 一次，整体和格子数量成正比。  
- **空间复杂度**：`O(n²)` — 需要额外的哈希表保存每个可能数字的出现次数，最坏情况下会存 `n²` 条记录。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于我们用了额外的 `O(n²)` 空间来记录每个数字出现的次数。  
实际上，只要知道 **两个整体的统计量**——所有数字的**和**、**平方和**——就能推导出重复数 `a` 和缺失数 `b`，而不需要额外的存储。

设  

- `S = 1 + 2 + … + n² = n²·(n²+1)/2`   （完整矩阵的理论总和）  
- `P = 1² + 2² + … + (n²)² = n²·(n²+1)·(2·n²+1)/6` （完整矩阵的理论平方和）

我们遍历一次矩阵，累计实际出现的 **和** `S_actual` 和 **平方和** `P_actual`：

- `S_actual = S - b + a`（因为缺了 `b`，多了 `a`）  
- `P_actual = P - b² + a²`

把两式相减得到：

```
S_actual - S = a - b          …… (1)
P_actual - P = a² - b² = (a - b)(a + b) …… (2)
```

用 (1) 把 `a - b` 记为 `diff`，把 (2) 除以 `diff`（diff ≠ 0，因为一定有重复和缺失），得到 `a + b`：

```
sum_ab = (P_actual - P) / diff
```

现在我们已经有：

```
a - b = diff
a + b = sum_ab
```

只要把这两个方程相加、相减，就能求出 `a` 与 `b`：

```
a = (diff + sum_ab) // 2
b = a - diff
```

整个过程只需要 **一次遍历** 矩阵，额外空间只有常数级别 `O(1)`。

#### 代码（Python）

```python
def findMissingAndRepeated(grid):
    n = len(grid)
    total_nums = n * n                     # 最大数字，也是元素总数

    # 1️⃣ 计算完整矩阵的理论和与平方和（数学公式）
    expected_sum = total_nums * (total_nums + 1) // 2
    expected_sq_sum = total_nums * (total_nums + 1) * (2 * total_nums + 1) // 6

    # 2️⃣ 实际遍历矩阵，累计出现的和与平方和
    actual_sum = 0
    actual_sq_sum = 0
    for row in grid:
        for val in row:
            actual_sum += val
            actual_sq_sum += val * val

    # 3️⃣ 根据推导的公式求出 a - b 与 a + b
    diff = actual_sum - expected_sum                 # a - b
    # 为防止除法出现浮点数，使用整数除法 //（diff 一定不为 0）
    sum_ab = (actual_sq_sum - expected_sq_sum) // diff   # a + b

    # 4️⃣ 解方程得到重复数 a 与缺失数 b
    a = (diff + sum_ab) // 2
    b = a - diff

    return [a, b]
```

#### 复杂度

- **时间复杂度**：`O(n²)` — 只遍历矩阵一次，操作次数和格子数量成正比。相比暴力解，**没有额外的遍历** 来找缺失数，常数因子更小。  
- **空间复杂度**：`O(1)` — 只用了几个整数变量（`expected_sum`、`actual_sum` …），不随 `n` 增长。

---

## 心得

- 这道题的核心技巧是 **利用整体统计量（和、平方和）把两个未知数转化为线性方程组**，从而在 **常数空间** 内完成求解。  
- 类似的技巧常用于**找重复/缺失数字**的题目，例如  
  1. LeetCode 645. **Set Mismatch**（一维数组版）  
  2. LeetCode 287. **Find the Duplicate Number**（利用快慢指针也属于数学思路）  
  3. LeetCode 1769. **Missing Number**（只缺一个数，用异或或求和）  
- **一句话总结**：把「重复」和「缺失」分别看作「多了一个」和「少了一个」，用「总和」和「平方和」把它们消掉，方程求解即可。

---

## 反思

- **第一反应**：直接用哈希表或计数数组记录每个数字出现的次数，这是最直观、最安全的办法。  
- **最容易踩的坑**  
  - 忘记把 `diff`（即 `a - b`）作为除数时可能出现除以 0 的错误（实际上这里一定不为 0，因为一定有重复和缺失）。  
  - 使用浮点除法会导致精度问题，必须使用整数除法 `//`。  
  - 边界条件：`n = 2` 时矩阵只有 4 个格子，仍然适用公式，不需要额外处理。  
- **下次遇到同类题**，第一步应该先思考：「能否用**整体统计**（和、异或、平方和）把未知数降维？」如果可以，就尝试写出相应的方程；否则再回退到计数或哈希表的暴力实现。