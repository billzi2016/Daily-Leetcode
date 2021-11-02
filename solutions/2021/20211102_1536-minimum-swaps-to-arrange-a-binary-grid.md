# #1536. 二进制网格的最少交换次数 / Minimum Swaps to Arrange a Binary Grid

> 难度：中等 · 标签：Array、Greedy、Matrix · [LeetCode 链接](https://leetcode.com/problems/minimum-swaps-to-arrange-a-binary-grid/)

---

## 题目（英文原版）

**Description**

Given an n x n binary grid, in one step you can choose two adjacent rows of the grid and swap them.
A grid is said to be valid if all the cells above the main diagonal are zeros.
Return the minimum number of steps needed to make the grid valid, or -1 if the grid cannot be valid.
The main diagonal of a grid is the diagonal that starts at cell (1, 1) and ends at cell (n, n).

**Examples**

**Example 1:**

```
Input: grid = [[0,0,1],[1,1,0],[1,0,0]]
Output: 3
```

**Example 2:**

```
Input: grid = [[0,1,1,0],[0,1,1,0],[0,1,1,0],[0,1,1,0]]
Output: -1
Explanation: All rows are similar, swaps have no effect on the grid.
```

**Example 3:**

```
Input: grid = [[1,0,0],[1,1,0],[1,1,1]]
Output: 0
```

**Constraints**

- n == grid.length == grid[i].length
- 1 <= n <= 200
- grid[i][j] is either 0 or 1

---

## 题目（中文翻译）

**题目描述**  
给定一个 `n × n` 的二进制网格（binary grid），在一次操作中你可以选择网格中相邻的两行并将它们交换位置。  
如果网格中主对角线（main diagonal）上方的所有单元格均为 `0`，则该网格被认为是有效的（valid）。  
返回使网格有效所需的最少操作次数，如果无法使网格有效则返回 `-1`。

**示例**  

示例 1  
```text
输入: grid = [[0,0,1],[1,1,0],[1,0,0]]
输出: 3
```

示例 2  
```text
输入: grid = [[0,1,1,0],[0,1,1,0],[0,1,1,0],[0,1,1,0]]
输出: -1
说明: 所有行都相同，交换操作对网格没有影响。
```

示例 3  
```text
输入: grid = [[1,0,0],[1,1,0],[1,1,1]]
输出: 0
```

**约束条件**  
- `n == grid.length == grid[i].length`
- `1 ≤ n ≤ 200`
- `grid[i][j]` 只能是 `0` 或 `1`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有行的排列方式都尝试一遍**，看哪一种能够让矩阵满足“主对角线右上方全是 0”的要求，并记录下最少的相邻交换次数。  

- **数据结构**：把每一行看成一个整体，用列表 `order` 保存当前的行顺序。  
- **类比**：这类似于把一副扑克牌全部洗牌后再排好，每一种排法都要检查一次。  
- **正确性**：只要遍历了**所有**可能的行顺序，就一定能找到最少交换次数（如果有解的话），因为题目只限制相邻行的交换，而任意两行的相对位置都可以通过若干次相邻交换实现。  

但是，这种“全枚举”会导致**指数级**的时间开销：  
- 对于 `n` 行，有 `n!`（阶乘）种排列。  
- 每检查一种排列都需要 O(n²)（遍历矩阵上三角）来判断是否合法。  

所以这只能用来**验证思路**或在 `n` 非常小（如 n≤6）时测试。

#### 代码（Python）

```python
from itertools import permutations

def is_valid(grid):
    """检查矩阵是否已经满足条件：主对角线右上全为 0"""
    n = len(grid)
    for i in range(n):
        for j in range(i + 1, n):          # 只看主对角线右上方的格子
            if grid[i][j] == 1:
                return False
    return True

def min_swaps_bruteforce(grid):
    n = len(grid)
    rows = list(range(n))                 # 行的原始下标
    best = float('inf')

    # 枚举所有行的排列
    for perm in permutations(rows):
        # 根据排列重新排列矩阵
        new_grid = [grid[i] for i in perm]

        if is_valid(new_grid):
            # 计算从原始顺序到 perm 需要的相邻交换次数
            # 这里用冒泡的思想计数：把每个元素往左“冒泡”到目标位置
            swaps = 0
            pos = list(perm)               # 当前顺序
            for i in range(n):
                # 在当前位置 i 左边找第一个等于 i 的元素
                j = pos.index(i, i)        # 第 i 行应该放在第 i 位
                swaps += j - i
                # 把它向左移动到第 i 位，模拟相邻交换
                while j > i:
                    pos[j], pos[j-1] = pos[j-1], pos[j]
                    j -= 1
            best = min(best, swaps)

    return -1 if best == float('inf') else best
```

> **提示**：上述代码仅用于演示暴力思路，`permutations` 在 `n>8` 时就会失去可行性。

#### 复杂度  

- **时间复杂度**：`O(n! * n²)`  
  - `n!` 来自所有行排列的枚举；  
  - `n²` 来自每次检查矩阵上三角是否全 0。  
  - 直观理解：当 `n=10` 时，`10! ≈ 3.6 million`，已经远远超出常规程序的承受范围。  
- **空间复杂度**：`O(n)`  
  - 只用了几个长度为 `n` 的临时列表（`rows`, `perm`, `pos`）。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到，**真正的难点在于找出每一行应该放到哪一行**，而不是去枚举所有可能的排列。  
下面一步步推导出线性（或准线性）时间的贪心算法：

1. **每行能容忍的最右侧 1 的位置**  
   对第 `i` 行来说，若要满足“主对角线右上全为 0”，则该行第 `i` 列（从 0 开始计数）右侧的所有格子必须都是 0。  
   换句话说，这一行**最右边出现的 1**（记作 `right_one[i]`）必须位于第 `i` 列或更左侧。  
   - 若该行全是 0，则 `right_one[i] = -1`（表示不存在 1）。  
   - 若 `right_one[i] = k`，则只有当 `k ≤ i` 时，这一行才能放在第 `i` 行。

2. **把每行的 `right_one` 看成一个数组**  
   ```
   right_one = [最右的1所在列, ...]
   ```
   例如 `grid = [[0,0,1],[1,1,0],[1,0,0]]`  
   `right_one = [2,1,0]`

3. **贪心选择**  
   从上到下遍历目标行 `i = 0 … n-1`：  
   - 在当前以及其下方的行中（`j >= i`），找 **第一个** 满足 `right_one[j] ≤ i` 的行 `j`。  
   - 这行 `j` 必须被搬到第 `i` 行，否则第 `i` 行的右上方必然会出现 1，导致不合法。  
   - 将行 `j` **通过相邻交换向上冒泡**到第 `i` 行，需要 `j - i` 次交换。把这个次数累计到答案中。  
   - 同时，要把 `right_one` 数组中对应的元素也一起向上移动（因为行顺序改变了）。

   这一步是**核心**：每次都取离目标位置最近的可用行，保证交换次数最小。  
   为什么最近的就够好？因为如果我们把更远的行提前搬上来，必然会多出不必要的额外交换，而后面的行仍然可以在后面继续满足各自的约束。

4. **是否有解的判定**  
   在遍历的过程中，如果在某个 `i` 找不到满足 `right_one[j] ≤ i` 的行，则说明无论怎么交换都无法让第 `i` 行符合要求，直接返回 `-1`。

5. **时间复杂度分析**  
   - 计算 `right_one`：遍历每行的每个元素，最坏 O(n²)。  
   - 主循环：外层 `i` 走 `n` 次，内层找 `j` 最坏也走 `n` 次，总共 O(n²)。  
   - 所以整体是 **O(n²)**，在 `n ≤ 200` 的限制下毫无压力。

#### 代码（Python）

```python
def min_swaps(grid):
    """
    贪心实现：返回使矩阵满足“主对角线右上全为0”所需的最少相邻行交换次数，
    若无解返回 -1。
    """
    n = len(grid)

    # 1. 计算每行最右侧 1 的下标（若全为 0 则记为 -1）
    right_one = []
    for row in grid:
        pos = -1                     # 默认全 0
        for idx, val in enumerate(row):
            if val == 1:
                pos = idx           # 记录最新的 1 的位置
        right_one.append(pos)

    swaps = 0                       # 累计交换次数

    # 2. 从上到下依次确定每一行应该放哪一行
    for i in range(n):
        # 在 i 及其以下的行中找第一个满足 right_one[j] <= i 的行
        target = -1
        for j in range(i, n):
            if right_one[j] <= i:
                target = j
                break

        # 如果找不到，说明无解
        if target == -1:
            return -1

        # 3. 将目标行 target “冒泡”到第 i 行，需要 target - i 次相邻交换
        swaps += target - i
        # 把 right_one 数组中对应的元素向上移动，模拟行的交换过程
        while target > i:
            right_one[target], right_one[target - 1] = (
                right_one[target - 1],
                right_one[target],
            )
            target -= 1

    return swaps
```

> **代码注释说明**  
> - `right_one[j] <= i` 表示第 `j` 行的最右 1 已经在第 `i` 列或更左，放到第 `i` 行后不会破坏上三角的 0。  
> - `while target > i` 这段代码相当于把行 `target` 用 **相邻交换** 一次次往上移，正好对应题目允许的操作。

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 计算 `right_one` 需要遍历全部 `n × n` 元素；  
  - 主循环每次最多向下扫描一次，最坏也只会遍历 `n` 行两次。  
  - 与暴力解相比，省掉了阶乘级别的排列枚举，只剩下二次遍历，运行速度提升数千倍。

- **空间复杂度**：`O(n)`  
  - 只用了一个长度为 `n` 的 `right_one` 列表和若干常数级别的临时变量。  
  - 没有额外的二维数组或递归栈，内存占用几乎和输入规模相同。

---

## 心得

- **核心技巧**：**把每行最右侧的 1 当作约束值，利用贪心把最近的可放行“冒泡”到目标位置**。  
- **适用场景**：  
  1. 需要把数组/矩阵的元素移动到满足某种“左边/上边必须为 0（或小于等于）”的约束时，如 “Minimum Operations to Make the Array Non-decreasing”。  
  2. 只允许相邻交换且目标是“把每个位置的元素限制在一定范围内”，典型例子还有 “Minimum Adjacent Swaps to Make a Palindrome”。  
  3. 类似的行/列移动问题，如 “Matrix Rearrangement with Row/Column Swaps”。  
- **一句话总结**：**把每行的“最右 1”视作它的“最大可容忍列”，从上到下贪心挑最近的满足行并用相邻交换把它搬上来**。

---

## 反思

- **第一反应**：看到“相邻行交换”，本能想到 BFS/全排列搜索，导致想到暴力解。  
- **最容易踩的坑**：  
  - 忘记把 **全 0 行** 的 `right_one` 设为 `-1`，导致判断 `right_one[j] <= i` 时出现错误。  
  - 在模拟交换时只累计次数，却忘记同步更新 `right_one`（行顺序已经改变），会导致后面的判断不准确。  
  - 题目要求的是“主对角线右上全为 0”，而不是“左上全为 0”，容易把比较方向写反。  
- **下次类似题的第一步**：先 **把每个元素对应的约束值提取出来**（比如最右 1、最左 1、最大值等），再判断是否存在满足这些约束的排列；若存在，尝试 **贪心/双指针** 把最近可用的元素搬到目标位置。这样往往能直接得到 O(n²) 或更优的解法。