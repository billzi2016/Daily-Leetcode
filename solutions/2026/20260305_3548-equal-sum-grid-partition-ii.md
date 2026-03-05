# #3548. 等和网格划分 II / Equal Sum Grid Partition II

> 难度：困难 · 标签：Array、Hash Table、Matrix、Enumeration、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/equal-sum-grid-partition-ii/)

---

## 题目（英文原版）

**Description**

You are given an m x n matrix grid of positive integers. Your task is to determine if it is possible to make either one horizontal or one vertical cut on the grid such that:
Return true if such a partition exists; otherwise, return false.
Note: A section is connected if every cell in it can be reached from any other cell by moving up, down, left, or right through other cells in the section.

**Examples**

**Example 1:**

```
Input: grid = [[1,4],[2,3]]
Output: true
Explanation:
```

**Example 2:**

```
Input: grid = [[1,2],[3,4]]
Output: true
Explanation:
```

**Example 3:**

```
Input: grid = [[1,2,4],[2,3,5]]
Output: false
Explanation:
```

**Example 4:**

```
Input: grid = [[4,1,8],[3,2,6]]
Output: false
Explanation:
No valid cut exists, so the answer is false .
```

**Constraints**

- 1 <= m == grid.length <= 105
- 1 <= n == grid[i].length <= 105
- 2 <= m * n <= 105
- 1 <= grid[i][j] <= 105

---

## 题目（中文翻译）

**描述**  
给定一个 `m × n` 的正整数矩阵 `grid`。请判断是否可以在矩阵上仅做一次水平切割或一次垂直切割，使得切割后得到的两个部分的元素之和相等。  
返回 `true` 表示存在这样的划分；否则返回 `false`。  

> **提示**：如果一个区域中的任意两个单元格可以通过上下、左右相邻的单元格在该区域内相连，则该区域是连通的（connected）。

**示例 1**  
Input: `grid = [[1,4],[2,3]]`  
Output: `true`  
Explanation:  

**示例 2**  
Input: `grid = [[1,2],[3,4]]`  
Output: `true`  
Explanation:  

**示例 3**  
Input: `grid = [[1,2,4],[2,3,5]]`  
Output: `false`  
Explanation:  

**示例 4**  
Input: `grid = [[4,1,8],[3,2,6]]`  
Output: `false`  
Explanation:  
不存在满足条件的切割，故答案为 `false`。

**约束条件**  
- `1 ≤ m == grid.length ≤ 10^5`  
- `1 ≤ n == grid[i].length ≤ 10^5`  
- `2 ≤ m × n ≤ 10^5`  
- `1 ≤ grid[i][j] ≤ 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的切割位置**，然后分别计算切割后两块的元素和，看看是否相等（或通过删掉一格让它们相等）。  

- **切割方式**  
  - 水平切割：在第 `k` 行和第 `k+1` 行之间切，得到上半部分和下半部分。  
  - 垂直切割：在第 `k` 列和第 `k+1` 列之间切，得到左半部分和右半部分。  

- **怎么算和**  
  对于每一种切割，都要遍历整张表，把对应的格子加到两个子区域的和里。  
  如果两边的和相等，直接返回 `True`。  
  若不相等，则看差值 `diff = |sum1 - sum2|` 是否恰好等于某个子区域里出现过的格子值（因为只能删掉 **一格**），如果存在同样返回 `True`。

- **为什么正确**  
  只要把所有合法的切割全部尝试一遍，就一定能找到答案（若有的话），这是一种“穷举”思路，保证不遗漏任何可能性。

- **复杂度分析（大白话）**  
  - **时间**：  
    - 对每一条水平切割（最多 `m-1` 条）我们要遍历整个 `m × n` 的矩阵求和 → `O(m·(m·n)) = O(m²·n)`。  
    - 对每一条垂直切割（最多 `n-1` 条）同理 → `O(n²·m)`。  
    - 综合下来大约是 `O(m²·n + n²·m)`，在最坏情况下相当于 **每个格子被重复加了上千次**，对 10⁵ 个格子的限制来说会超时。  
  - **空间**：只用了常数级的临时变量（比如两个累计和），所以是 `O(1)`。

#### 代码（Python）

```python
def equalSumGridPartition_bruteforce(grid):
    m, n = len(grid), len(grid[0])
    # ---------- 水平切割 ----------
    for cut in range(1, m):                     # cut 在第 cut 行上方
        top_sum, bottom_sum = 0, 0
        top_vals, bottom_vals = set(), set()   # 用集合记录出现过的格子值

        for i in range(m):
            for j in range(n):
                if i < cut:
                    top_sum += grid[i][j]
                    top_vals.add(grid[i][j])
                else:
                    bottom_sum += grid[i][j]
                    bottom_vals.add(grid[i][j])

        if top_sum == bottom_sum:
            return True
        diff = abs(top_sum - bottom_sum)
        # 看能否删掉一格
        if top_sum > bottom_sum and diff in top_vals:
            return True
        if bottom_sum > top_sum and diff in bottom_vals:
            return True

    # ---------- 垂直切割 ----------
    for cut in range(1, n):
        left_sum, right_sum = 0, 0
        left_vals, right_vals = set(), set()

        for i in range(m):
            for j in range(n):
                if j < cut:
                    left_sum += grid[i][j]
                    left_vals.add(grid[i][j])
                else:
                    right_sum += grid[i][j]
                    right_vals.add(grid[i][j])

        if left_sum == right_sum:
            return True
        diff = abs(left_sum - right_sum)
        if left_sum > right_sum and diff in left_vals:
            return True
        if right_sum > left_sum and diff in right_vals:
            return True

    return False
```

> 代码里每个 `for` 循环都在遍历整张表，**所以会非常慢**。  
> 只把思路写出来，后面我们会一步步把它改快。

#### 复杂度

- **时间复杂度**：`O(m²·n + n²·m)`  
  - “O” 代表“量级”，比如 `O(m²·n)` 就相当于“矩阵的行数平方乘以列数”。当 `m`、`n` 都是几千时，这个量级已经是上千万次操作，远远超过 10⁵ 规模的上限。  
- **空间复杂度**：`O(1)`  
  - 只用了几个整数和集合（集合大小最多 `m·n`，但在最坏情况下我们可以把它们换成哈希表计数，仍然是常数级别的额外空间）。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次切割都重新遍历整张表**。我们需要把“遍历一次”与“检查所有切割”结合起来，使每个格子只被统计 **一次**。

核心思路：

1. **前缀和 + 滚动统计**  
   - 先算出整张表的总和 `total`（一次遍历）。  
   - 逐行（或逐列）累加，**实时维护上方（左方）子区域的和** `sum_up`，下方（右方）子区域的和自然是 `total - sum_up`。这样每移动一次切割，只需要把当前行（列）的贡献加进去，**不需要重新遍历已统计的部分**。

2. **出现值的哈希表**  
   - 为了判断“删掉一格能否让两边相等”，我们需要快速查询某个差值 `diff` 是否在对应子区域出现过。  
   - 使用 **字典 `cnt_up` 记录上方（左方）子区域中每个数出现的次数**，`cnt_down` 记录下方（右方）子区域中每个数出现的次数。  
   - 当切割向下（右）移动一行（列）时：  
     - 把当前行（列）的所有格子加入 `cnt_up`（同时从 `cnt_down` 中减去）。  
     - 这样 `cnt_up` / `cnt_down` 始终保持**最新**的子区域统计。

3. **判断条件**  
   - 设 `sum_up` 为上方（左方）子区域的和，`sum_down = total - sum_up`。  
   - **如果两边已经相等** → `True`。  
   - **否则**，设 `diff = abs(sum_up - sum_down)`，我们只能删掉 **一格**，于是：  
     - 如果 `sum_up > sum_down`，需要从上方删掉一个值恰好等于 `diff` → 检查 `cnt_up[diff] > 0`。  
     - 如果 `sum_down > sum_up`，需要从下方删掉一个值恰好等于 `diff` → 检查 `cnt_down[diff] > 0`。  
   - 任意一种满足即返回 `True`。

4. **单行 / 单列的特殊处理**  
   - 当矩阵只有一行时只能做垂直切割；只有一列时只能做水平切割。  
   - 其余情况两种切割方式都要尝试一次（分别跑一次上面的过程）。

5. **时间/空间分析**  
   - 每个格子只被 **加入一次、删除一次**，所以整体是 `O(m·n)`。  
   - 哈希表最多存储所有格子的值，空间同样是 `O(m·n)`（在最坏情况下每个格子数值都不相同）。

> **关键点**：把“遍历求和”与“检查每条切割”合并，用 **前缀和**（滚动累计）和 **哈希计数** 两把钥匙，彻底摆脱二次遍历的灾难。

#### 代码（Python）

```python
from collections import Counter
from typing import List

def equalSumGridPartition(grid: List[List[int]]) -> bool:
    """
    最优解：一次遍历 + 哈希表计数
    """
    m, n = len(grid), len(grid[0])
    total = sum(sum(row) for row in grid)          # 整张表的总和，只算一次

    # ---------- 只可能水平切割的情况（单列或普通情况） ----------
    # cnt_down 初始保存整张表所有格子的出现次数
    cnt_down = Counter()
    for row in grid:
        cnt_down.update(row)

    cnt_up = Counter()          # 上方（左方）子区域的计数，初始为空
    sum_up = 0                  # 上方子区域的和

    # 逐行尝试把切割放在当前行的上方（即 cut 在 row 与 row+1 之间）
    for r in range(m - 1):      # 最后一行后面不能再切
        # 把第 r 行的所有元素加入上方区域，同时从下方区域中减去
        for val in grid[r]:
            sum_up += val
            cnt_up[val] += 1
            cnt_down[val] -= 1
            if cnt_down[val] == 0:
                del cnt_down[val]   # 删除键，保持字典小

        sum_down = total - sum_up
        if sum_up == sum_down:
            return True

        diff = abs(sum_up - sum_down)
        if sum_up > sum_down:
            # 需要在上方删掉一个 diff
            if cnt_up.get(diff, 0) > 0:
                return True
        else:
            # 需要在下方删掉一个 diff
            if cnt_down.get(diff, 0) > 0:
                return True

    # ---------- 只可能垂直切割的情况（单行或普通情况） ----------
    # 下面的逻辑与水平切割完全对称，只是把“行”换成“列”
    cnt_down = Counter()
    for row in grid:
        cnt_down.update(row)

    cnt_up = Counter()
    sum_up = 0

    # 逐列尝试切割
    for c in range(n - 1):
        for r in range(m):
            val = grid[r][c]
            sum_up += val
            cnt_up[val] += 1
            cnt_down[val] -= 1
            if cnt_down[val] == 0:
                del cnt_down[val]

        sum_down = total - sum_up
        if sum_up == sum_down:
            return True

        diff = abs(sum_up - sum_down)
        if sum_up > sum_down:
            if cnt_up.get(diff, 0) > 0:
                return True
        else:
            if cnt_down.get(diff, 0) > 0:
                return True

    return False
```

**代码要点解释（中文注释已经写在代码里）**  

- `Counter` 相当于 **哈希表**，键是格子里的数，值是出现次数。它的查询、增加、删除都是 `O(1)`（均摊）。  
- `sum_up` 是**滚动前缀和**，每加入一行（列）就把该行（列）的所有数加进去。  
- `sum_down = total - sum_up` 直接算出另一侧的和，**不需要再次遍历**。  
- `diff` 是两侧和的差值，只要在“较大那侧”出现过这个差值，就能通过删掉这一个格子让两边相等。

#### 复杂度

- **时间复杂度**：`O(m·n)`  
  - 每个格子只被访问两次（一次加入上/左区域，一次从下/右区域删），相当于一次线性扫描。相比暴力解的 `O(m²·n + n²·m)`，快了几个数量级。  
  - 在最坏的 10⁵ 格子规模下，这样的复杂度完全可以在毫秒级跑完。

- **空间复杂度**：`O(m·n)`（哈希表存储所有不同的数值）  
  - 如果所有格子数值都不相同，字典会有 `m·n` 条记录。  
  - 这仍然在题目给出的 10⁵ 上限内可接受（约几 MB 的内存）。

---

## 心得

- **核心技巧**：  
  1. **前缀和（滚动累计）**：把“切割后两块的和”转化为一次遍历得到的累计值。  
  2. **哈希表计数**：快速判断某个差值是否在当前子区域出现过，支持“一格删掉”这种“可选删除”需求。  

- **适用的题型**（类似思路可复用）  
  1. *Equal Sum Grid Partition*（第一版，只要求两块和相等，不允许删除）  
  2. *Split Array With Same Average*（数组划分成两段，使平均值相等）  
  3. *Maximum Subarray Sum with One Deletion*（子数组最大和，允许删除一个元素）  

- **一句话总结解题钥匙**  
  > “把所有切割的**和**用一次前缀累计算出来，再用哈希表瞬间查‘能否删掉一个等差值’”。  

---

## 反思

- **拿到题目第一反应**  
  - “先遍历所有切割点，分别算两边的和”。这自然会想到暴力实现。  

- **最容易踩的坑**  
  1. **单行 / 单列的边界**：如果直接把水平和垂直两种切割都跑一次，会在 `m-1` 或 `n-1` 为 0 时出现空循环，需要提前判断。  
  2. **删除元素的方向**：差值必须在**较大那侧**出现，忽略方向会导致错误的正例。  
  3. **哈希表的同步更新**：从 `cnt_down` 删除计数时一定要在计数归零后 `del` 键，否则后面 `get` 会误以为还有该值。  

- **下次遇到同类题，第一步该想到什么**  
  - “是否可以把**多次重复的子问题**（如每条切割的求和）**合并为一次滚动累计**？”  
  - “是否需要**快速判断某个值是否出现**？”——如果是，就准备好哈希表或计数数组。  

这样一步步把暴力思路“精炼”成线性时间的最优解，就能在面试或比赛中稳稳拿下这类“分割+可删”题目。祝学习愉快！