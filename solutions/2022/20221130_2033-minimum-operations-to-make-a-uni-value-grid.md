# #2033. 使网格统一值的最少操作次数 / Minimum Operations to Make a Uni-Value Grid

> 难度：中等 · 标签：Array、Math、Sorting、Matrix · [LeetCode 链接](https://leetcode.com/problems/minimum-operations-to-make-a-uni-value-grid/)

---

## 题目（英文原版）

**Description**

You are given a 2D integer grid of size m x n and an integer x. In one operation, you can add x to or subtract x from any element in the grid.
A uni-value grid is a grid where all the elements of it are equal.
Return the minimum number of operations to make the grid uni-value. If it is not possible, return -1.

**Examples**

**Example 1:**

```
Input: grid = [[2,4],[6,8]], x = 2
Output: 4
Explanation: We can make every element equal to 4 by doing the following: 
- Add x to 2 once.
- Subtract x from 6 once.
- Subtract x from 8 twice.
A total of 4 operations were used.
```

**Example 2:**

```
Input: grid = [[1,5],[2,3]], x = 1
Output: 5
Explanation: We can make every element equal to 3.
```

**Example 3:**

```
Input: grid = [[1,2],[3,4]], x = 2
Output: -1
Explanation: It is impossible to make every element equal.
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 105
- 1 <= m * n <= 105
- 1 <= x, grid[i][j] <= 104

---

## 题目（中文翻译）

给定一个大小为 `m x n` 的二维整数网格（grid）`grid` 和一个整数 `x`。在一次操作中，你可以对网格中的任意元素加上 `x` 或减去 `x`。  
如果网格中所有元素都相等，则称其为统一值网格（uni-value grid）。  
返回使网格成为统一值网格所需的最小操作次数。如果无法实现，返回 `-1`。

示例 1:
``` 
Input: grid = [[2,4],[6,8]], x = 2
Output: 4
Explanation: 我们可以通过以下操作使所有元素等于 4：
- 对 2 加一次 x。
- 对 6 减一次 x。
- 对 8 减两次 x。
共计使用 4 次操作。
```

示例 2:
``` 
Input: grid = [[1,5],[2,3]], x = 1
Output: 5
Explanation: 我们可以使所有元素等于 3。
```

示例 3:
``` 
Input: grid = [[1,2],[3,4]], x = 2
Output: -1
Explanation: 无法使所有元素相等。
```

约束条件：
- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 10^5`
- `1 <= m * n <= 10^5`
- `1 <= x, grid[i][j] <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举**所有可能的目标值 `t`，把每个格子都改成 `t`，统计需要的操作次数，取最小的那一个。  
- **数据结构**：我们只需要把二维矩阵 `grid` 展平成一个一维列表 `vals`，这样遍历和统计会更直观。把矩阵想象成一本书的章节，展开后就是一本长长的目录（列表），每个章节（格子）都有自己的页码（数值）。  
- **为什么正确**：只要把每个格子都改成同一个数 `t`，不管 `t` 是多少，最终一定会得到一个**统一值的网格**（uni‑value grid），所以遍历所有 `t` 能保证找到最优解。  

但是，这种做法有两个致命的缺点：

1. **目标值的取值范围太大**。`grid[i][j]` 最大到 `10⁴`，`x` 也可能是 `1`，那么可能的 `t` 值多达几万甚至上万，枚举每一个会导致时间爆炸。  
2. **每次遍历都要计算所有格子的操作数**，如果网格有 `m·n`（最多 `10⁵`）个格子，枚举 `k` 个目标值的时间复杂度就是 `O(k·m·n)`，在最坏情况下是 `O(10⁹)`，远远超出时间限制。

#### 代码（Python）

```python
def min_operations_bruteforce(grid, x):
    # 把二维矩阵拉平成一维，方便遍历
    vals = [v for row in grid for v in row]

    # 可能的目标值集合：从最小值到最大值，步长为 x
    lo, hi = min(vals), max(vals)
    candidates = range(lo, hi + 1, x)          # 每次加 x，模拟所有合法的 t

    best = float('inf')
    for t in candidates:
        ops = 0
        for v in vals:
            diff = abs(v - t)
            # 如果 diff 不是 x 的整数倍，就无法通过加/减 x 到达 t
            if diff % x != 0:
                return -1                     # 直接返回不可能
            ops += diff // x                  # 需要的操作次数
        best = min(best, ops)

    return best if best != float('inf') else -1
```

> **注意**：代码里已经加入了“如果出现不可达的情况直接返回 -1”，因为只要有一个格子无法通过 `±x` 达到目标，就不可能完成。

#### 复杂度

- **时间复杂度**：`O(k·m·n)`，其中 `k = (max‑min)/x + 1` 是可能目标值的数量。  
  - 大白话：如果 `x = 1`，`k` 可能是几千甚至几万，乘上格子数 `10⁵`，就会出现几百亿次的循环，明显太慢。  
- **空间复杂度**：`O(m·n)` 用来存放拉平后的列表 `vals`。  

> 结论：暴力解虽然思路简单，却因为枚举太多目标值而不可行，需要进一步优化。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**两个关键点**决定是否可行以及代价大小：

1. **可行性**：两个数 `a`、`b` 能否通过若干次 `±x` 变成相同的数？答案是：只有当 `a % x == b % x` 时才可能。把 `%` 想成“余数”，就像把所有格子按 `x` 划分成若干个“同余类”。如果格子落在不同的类里，就永远无法相遇，直接返回 `-1`。  
2. **最小操作数**：在所有可行的目标值中，哪个目标能让总操作次数最少？把每个格子的数值除以 `x`（因为每次操作相当于把数值“向左/右”移动一步），得到一组整数 `a_i = (grid[i][j] - base) / x`（这里 `base` 是任意一个格子的值，只要余数相同就行）。我们要最小化  
   \[
   \sum |a_i - t|
   \]
   其中 `t` 是目标整数（对应真实目标值 `base + t·x`）。  
   这正是**求绝对值差之和最小**的问题，而**中位数**（median）恰好是该问题的最优解。把 `a_i` 排序后，取中间的那个数（如果个数是偶数，任意取中间两个中的一个即可），把所有数搬到这个位置，需要的步数最少。

**完整步骤**：

1. 把所有格子拉平成一维列表 `vals`。  
2. 检查所有数的余数 `val % x` 是否相同，若不同返回 `-1`。  
3. 把每个数都除以 `x`（整除），得到新列表 `norm`。这里的除法相当于把“每一次加/减 x”抽象成“一步”。  
4. 将 `norm` 排序，取中位数 `median`。  
5. 计算总操作次数 `sum(|v - median|)`，这已经是 **步数**，不需要再乘 `x`（因为我们已经把 `x` 抽出来了）。  
6. 返回该总和。

**类比**：想象有一排小朋友站在数轴上，每次只能走一步（步长 1），我们想让他们全部聚到同一个位置，最省力的办法就是让他们聚到中间的那个人所在的位置——这就是“中位数”理念的直观解释。

#### 代码（Python）

```python
def minOperations(grid, x):
    """
    返回将 grid 变成所有元素相等所需的最少操作次数，若不可能返回 -1。
    思路：
    1. 余数必须相同，否则 impossible。
    2. 把每个数除以 x，转化为“步数”列表。
    3. 取中位数作为目标，求绝对差之和即为答案。
    """
    # 1️⃣ 拉平
    vals = [v for row in grid for v in row]

    # 2️⃣ 检查同余性
    remainder = vals[0] % x
    for v in vals:
        if v % x != remainder:          # 余数不相同，无法统一
            return -1

    # 3️⃣ 归一化：每次操作相当于“走一步”，所以除以 x
    norm = [(v - remainder) // x for v in vals]   # 这里减去相同的 remainder 再除 x，确保是整数

    # 4️⃣ 找中位数
    norm.sort()
    median = norm[len(norm) // 2]      # 中间的那个数（偶数时取右侧中位数，任意即可）

    # 5️⃣ 计算总操作次数（已是步数）
    ops = sum(abs(v - median) for v in norm)

    return ops
```

> **代码解释**  
> - 第 2 步利用余数相同的性质快速判断可行性，类似于“查字典”，键是余数，若出现不同的键就直接返回 `-1`。  
> - 第 3 步的 `(v - remainder) // x` 把原始值映射到“步数坐标”，这样每一次加/减 `x` 就对应坐标轴上走一步。  
> - 第 4 步的 `median` 是最优聚集点，取中位数的原因在于**绝对值差之和的最小化**（数学证明略，可视为“把大家都搬到中间最省力”）。  
> - 第 5 步直接把所有步数相加，就是最终的操作次数。

#### 复杂度

- **时间复杂度**：`O(m·n log(m·n))`  
  - 拉平、检查余数是线性 `O(m·n)`，排序占 `O(m·n log(m·n))`，这是整个过程的瓶颈。  
  - 大白话：如果有 `10⁵` 个格子，排序大约需要 `10⁵ × log₂10⁵ ≈ 10⁵ × 17 ≈ 1.7·10⁶` 次比较，完全可以在一秒内完成。  
- **空间复杂度**：`O(m·n)` 用来存放拉平后的列表和归一化后的列表（可以复用同一列表以节省一点空间，但对初学者保持直观更好）。  

> 与暴力解相比，时间从可能的 **亿级** 降到了 **百万级**，是一次质的飞跃。

---

## 心得

- **核心技巧**：  
  1. **同余判定**（余数相同才能相等）  
  2. **归一化 + 中位数**（把“每次加/减 x”抽象成一步，使用中位数最小化绝对差之和）  

- **适用的题型**（可迁移的思路）：  
  - *“使数组所有元素相等的最少操作数”*（如 LeetCode 462. Minimum Moves to Equal Array Elements II）  
  - *“按固定步长平移数组元素”*（如 2035. Partition Array Into Two Arrays With Minimum Difference）  
  - *“同余类判断”*（如 1705. Maximum Number of Eaten Apples, 2045. Minimum Number of Operations to Make Array Continuous）  

- **一句话总结解题钥匙**：  
  > “先把问题化成‘走步数’的形式，余数相同是能否到达的前提，步数的中位数是最省力的聚集点。”

---

## 反思

- **拿到题目第一反应**：先检查能否通过 `±x` 把所有数调到同一个值（余数是否相同），然后想办法在可能的范围里找最省操作的目标。  
- **最容易踩的坑**  
  1. **忘记余数检查**，直接尝试计算会得到错误的非负答案。  
  2. **在归一化时直接除 `x` 而不处理余数**，导致出现非整数导致的精度问题。  
  3. **中位数的选择**：若元素个数为偶数，随便取左中位数或右中位数都可以，但一定要取列表中的一个实际元素，不能取平均值（那不是整数步数）。  
- **下次遇到同类题，第一步该想到**：  
  > “先把所有数映射到同余类（余数）上，看是否在同一个类；如果在同一个类，就把问题转化为‘最小化绝对差之和’，中位数自然浮现。”