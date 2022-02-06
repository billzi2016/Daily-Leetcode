# #1659. 最大化网格幸福感 / Maximize Grid Happiness

> 难度：困难 · 标签：Dynamic Programming、Bit Manipulation、Memoization、Bitmask · [LeetCode 链接](https://leetcode.com/problems/maximize-grid-happiness/)

---

## 题目（英文原版）

**Description**

You are given four integers, m, n, introvertsCount, and extrovertsCount. You have an m x n grid, and there are two types of people: introverts and extroverts. There are introvertsCount introverts and extrovertsCount extroverts.
You should decide how many people you want to live in the grid and assign each of them one grid cell. Note that you do not have to have all the people living in the grid.
The happiness of each person is calculated as follows:
Neighbors live in the directly adjacent cells north, east, south, and west of a person's cell.
The grid happiness is the sum of each person's happiness. Return the maximum possible grid happiness.

**Examples**

**Example 1:**

```
Input: m = 2, n = 3, introvertsCount = 1, extrovertsCount = 2
Output: 240
Explanation: Assume the grid is 1-indexed with coordinates (row, column).
We can put the introvert in cell (1,1) and put the extroverts in cells (1,3) and (2,3).
- Introvert at (1,1) happiness: 120 (starting happiness) - (0 * 30) (0 neighbors) = 120
- Extrovert at (1,3) happiness: 40 (starting happiness) + (1 * 20) (1 neighbor) = 60
- Extrovert at (2,3) happiness: 40 (starting happiness) + (1 * 20) (1 neighbor) = 60
The grid happiness is 120 + 60 + 60 = 240.
The above figure shows the grid in this example with each person's happiness. The introvert stays in the light green cell while the extroverts live on the light purple cells.
```

**Example 2:**

```
Input: m = 3, n = 1, introvertsCount = 2, extrovertsCount = 1
Output: 260
Explanation: Place the two introverts in (1,1) and (3,1) and the extrovert at (2,1).
- Introvert at (1,1) happiness: 120 (starting happiness) - (1 * 30) (1 neighbor) = 90
- Extrovert at (2,1) happiness: 40 (starting happiness) + (2 * 20) (2 neighbors) = 80
- Introvert at (3,1) happiness: 120 (starting happiness) - (1 * 30) (1 neighbor) = 90
The grid happiness is 90 + 80 + 90 = 260.
```

**Example 3:**

```
Input: m = 2, n = 2, introvertsCount = 4, extrovertsCount = 0
Output: 240
```

**Constraints**

- 1 <= m, n <= 5
- 0 <= introvertsCount, extrovertsCount <= min(m * n, 6)

---

## 题目（中文翻译）

给定四个整数 `m、n、introvertsCount、extrovertsCount`。你有一个 `m × n` 的网格（grid），其中有两类人：内向者（introverts）和外向者（extroverts）。共有 `introvertsCount` 个内向者和 `extrovertsCount` 个外向者。  
你需要决定让多少人入住网格，并为每个人分配一个网格单元格。注意，并不一定要让所有人都入住网格。  

每个人的幸福值计算方式如下：  
- **相邻者（neighbors）** 指的是位于该单元格正北、正东、正南、正西四个方向的单元格中的人。  
- **内向者** 的初始幸福值为 120，若有相邻者，每个相邻者会使其幸福值降低 30。  
- **外向者** 的初始幸福值为 40，若有相邻者，每个相邻者会使其幸福值提升 20。  

网格幸福值（grid happiness）是所有人的幸福值之和。返回能够得到的最大网格幸福值。

---

### 示例

#### 示例 1
```
Input: m = 2, n = 3, introvertsCount = 1, extrovertsCount = 2
Output: 240
```
**解释**：假设网格使用 1‑索引，坐标形式为 (行, 列)。  
我们可以把内向者放在单元格 (1,1)，把两个外向者分别放在单元格 (1,3) 和 (2,3)。  
- 内向者在 (1,1) 的幸福值：120（初始幸福值）‑ (0 × 30)（0 个相邻者）= 120  
- 外向者在 (1,3) 的幸福值：40（初始幸福值）+ (1 × 20)（1 个相邻者）= 60  
- 外向者在 (2,3) 的幸福值：40（初始幸福值）+ (1 × 20)（1 个相邻者）= 60  
网格幸福值为 120 + 60 + 60 = 240。

#### 示例 2
```
Input: m = 3, n = 1, introvertsCount = 2, extrovertsCount = 1
Output: 260
```
**解释**：把两个内向者分别放在 (1,1) 和 (3,1)，把外向者放在 (2,1)。  
- 内向者在 (1,1) 的幸福值：120 ‑ (1 × 30)（1 个相邻者）= 90  
- 外向者在 (2,1) 的幸福值：40 + (2 × 20)（2 个相邻者）= 80  
- 内向者在 (3,1) 的幸福值：120 ‑ (1 × 30)（1 个相邻者）= 90  
网格幸福值为 90 + 80 + 90 = 260。

#### 示例 3
```
Input: m = 2, n = 2, introvertsCount = 4, extrovertsCount = 0
Output: 240
```

---

### 约束条件
- `1 ≤ m, n ≤ 5`
- `0 ≤ introvertsCount, extrovertsCount ≤ min(m × n, 6)`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每个格子都枚举三种可能：

* 空的  
* 放一个内向者（introvert）  
* 放一个外向者（extrovert）  

想象一下我们有一本**字典**（哈希表），键（key）是格子的坐标，值（value）是放进去的人或空。把所有格子都填满后，按照题目给出的规则去逐个计算每个人的幸福值，再把所有人的幸福加起来，就是一种可行的答案。

只要我们把**所有可能的放置方式**都遍历一遍，记录下最大的幸福值，就一定能得到正确答案——因为答案一定出现在这些枚举的情况里。

**为什么这种方法一定对？**  
- 每个格子只能是三种状态之一，遍历所有组合就覆盖了所有合法布局。  
- 题目允许不把所有人都放进网格，只要在枚举时把“剩余人数”控制在给定的 `introvertsCount`、`extrovertsCount` 范围内即可。  

**时间/空间分析（大白话）**  
- 网格最多有 `m·n ≤ 5·5 = 25` 个格子。每个格子 3 种选择，所以所有组合数是 `3^(m·n)`。这就像把 25 本书每本都有 3 种摆放方式，要把所有可能的排法都列出来，数量会非常巨大。  
- 对每一种组合，我们还要遍历整张网格算一次幸福值，时间是 `O(m·n)`。  
- 因此总体时间复杂度是 **O(3^(m·n) · m·n)**，这在最坏情况下已经是 **上百亿** 次操作，根本跑不完。  
- 空间上只需要保存当前递归的路径和计数，最多 `O(m·n)`（递归栈深度），可以认为是常数级别。  

> **结论**：暴力解思路清晰、实现简单，但只能用于“思考正确性”，在本题的约束下不可行。

#### 代码（Python）

```python
from functools import lru_cache

# ---------- 题目中给出的幸福增减表 ----------
# 基础幸福值
BASE = {0: 0, 1: 120, 2: 40}          # 0=空, 1=内向, 2=外向
# 相邻关系带来的变化
# (自己类型, 邻居类型) -> 增减值
DELTA = {
    (1, 1): -30, (1, 2): -10,
    (2, 1): +10, (2, 2): +20,
}


def maxGridHappiness_bruteforce(m, n, introvertsCount, extrovertsCount):
    """暴力枚举所有布局，返回最大幸福值（仅用于演示）"""

    total_cells = m * n

    @lru_cache(None)
    def dfs(pos, i_left, e_left, grid_state):
        """
        pos          : 当前处理的格子下标（0 .. total_cells-1）
        i_left, e_left: 剩余可用的内向/外向人数
        grid_state   : 已经放置好的格子，以整数 0/1/2 表示，按行主序保存为元组
        """
        if pos == total_cells:
            return 0

        r, c = divmod(pos, n)               # 当前格子的行列坐标
        # 上、左邻居的类型（若越界则视为空 0）
        up = grid_state[pos - n] if r > 0 else 0
        left = grid_state[pos - 1] if c > 0 else 0

        best = dfs(pos + 1, i_left, e_left, grid_state + (0,))   # 选空

        # -------- 放内向者 ----------
        if i_left > 0:
            cur = BASE[1]
            # 与上、左邻居的相互影响
            cur += DELTA.get((1, up), 0) + DELTA.get((up, 1), 0)
            cur += DELTA.get((1, left), 0) + DELTA.get((left, 1), 0)
            best = max(best,
                       cur + dfs(pos + 1, i_left - 1, e_left,
                                 grid_state + (1,)))

        # -------- 放外向者 ----------
        if e_left > 0:
            cur = BASE[2]
            cur += DELTA.get((2, up), 0) + DELTA.get((up, 2), 0)
            cur += DELTA.get((2, left), 0) + DELTA.get((left, 2), 0)
            best = max(best,
                       cur + dfs(pos + 1, i_left, e_left - 1,
                                 grid_state + (2,)))

        return best

    return dfs(0, introvertsCount, extrovertsCount, ())


# -------------------------------------------------
# 下面的调用仅作演示，实际运行会非常慢（指数级）
# print(maxGridHappiness_bruteforce(2, 2, 2, 1))
```

> 代码里每一行都有中文注释，帮助你快速定位关键逻辑。  
> 由于 `3^(m·n)` 的爆炸式增长，**请勿在正式提交时使用**，仅作思路验证。

#### 复杂度

- **时间复杂度**：`O(3^(m·n) · m·n)`  
  - “`3^(m·n)`” 表示所有可能的格子填充方式，等价于把每个格子都投掷一次 3 面骰子。  
  - 再乘上遍历整张网格的 `m·n`，因为每次组合都要算一次幸福值。  
- **空间复杂度**：`O(m·n)`（递归栈深度）  
  - 只保存当前路径的状态，最多等同于格子数目。  

---

### 2. 最优解

#### 思路  

从暴力解我们知道，**遍历所有组合是不可行的**，瓶颈在于“每个格子都要独立记住自己的状态”。  
如果我们能够在遍历时**共享一部分信息**，就能把状态空间大幅压缩。  

**关键观察**  

1. **相邻只影响上下左右四个方向**。  
   当我们按照行从左到右、从上到下依次填格子时，格子 **只会与已经处理过的格子产生交互**：  
   - 左边的格子（同一行、前一列）已经确定。  
   - 上边的格子（前一行、同一列）也已经确定。  
   - 右边和下边的格子还未决定，暂时不需要考虑。  

2. **只需要记住上一行的状态**。  
   对于即将处理的格子，它的上方邻居来源于“上一行”。如果我们把整行的放置情况保存下来，就能随时查询上方邻居的类型。  

3. **每个格子只可能是 0/1/2 三种**，可以用**3 进制**的**位掩码**（bitmask）来压缩一行的信息。  
   - 把每一列的状态看作一个“基-3 位”，例如 `n = 3` 时，行状态 `[0,1,2]` 可映射为整数 `0*3^0 + 1*3^1 + 2*3^2 = 0 + 3 + 18 = 21`。  
   - 这类似于把一本**字典**压缩进一个整数，查询某列的状态只需要对 `3` 取余和除法，速度很快。  

4. **动态规划 + 记忆化**。  
   - 设 `dp[pos][mask][i][e]` 为：**在处理到第 `pos`（0‑based）格子时，上一行的状态为 `mask`，还剩 `i` 个内向者和 `e` 个外向者可以使用时，能够得到的最大幸福值**。  
   - `pos` 从 `0` 到 `m·n`，遍历顺序保证左、上邻居的信息已经在 `mask` 和当前行的左邻居变量里。  
   - 对每个格子尝试三种放置方式（空、内向、外向），计算本次放置带来的幸福增量（包括与左、上邻居的相互影响），再递归到下一个格子。  
   - 使用 `@lru_cache` 进行记忆化，避免重复计算相同子问题。  

**如何计算增量**  

- 基础幸福值：`base = {0:0, 1:120, 2:40}`。  
- 与左邻居的交互：左邻居类型 `left` 已经在本行的 **前一个格子** 决定，可以直接传入递归函数。  
- 与上邻居的交互：上邻居类型 `up` 通过 `mask` 的对应列取出（`mask // 3^col % 3`）。  
- 增量公式（对每个方向都要计两次，因为相互影响是双向的）：

```
delta = base[type]
delta += effect[type][up] + effect[up][type]   # 上
delta += effect[type][left] + effect[left][type] # 左
```

其中 `effect` 对应题目给出的表格：

| 自己 \ 邻居 | 空(0) | 内向(1) | 外向(2) |
|-----------|------|--------|--------|
| 内向(1)   | 0    | -30    | -10    |
| 外向(2)   | 0    | +10    | +20    |

**状态压缩细节**  

- 当我们把当前格子放置为 `cur`（0/1/2）后，需要**更新 mask** 为“下一行的上一行”。  
  - 对于列 `col`，新的上方状态就是 `cur`（因为它将成为下一行的上邻居）。  
  - 其余列保持不变，只是整体向左移动一列（因为我们已经处理完当前列）。  
- 实际上可以把 `mask` 当成 **上一行的完整状态**，在递归进入下一格时，用 `new_mask = (mask % (3**col)) + cur * (3**col) + (mask // (3**(col+1))) * (3**(col+1))`，但更简洁的做法是把 **整行的状态随列移动**，即每处理完一格，就把 `mask` 整体除以 `3`（相当于把列向左“滑动”），并把当前格子的状态加入最高位。  

**整体时间复杂度**  

- 行状态数目：`3^n`（每列 3 种可能）。  
- `pos` 共有 `m·n ≤ 25` 步。  
- `i`、`e` 的取值范围均 ≤ 6。  
- 因此状态总数约为 `m·n·3^n·(intro+1)·(extro+1) ≤ 25·243·7·7 ≈ 300k`，每个状态只做常数次转移，**在 1 秒内轻松跑完**。  

#### 代码（Python）

```python
from functools import lru_cache

# ------------------- 常量表 -------------------
BASE = {0: 0, 1: 120, 2: 40}
# (自己, 邻居) -> 影响值
EFFECT = {
    (1, 1): -30, (1, 2): -10,
    (2, 1):  10, (2, 2):  20,
}
# 方便查询，缺省为 0（与空相邻不产生影响）
def get_effect(a, b):
    return EFFECT.get((a, b), 0)


def maxGridHappiness(m: int, n: int, introvertsCount: int, extrovertsCount: int) -> int:
    """最优 DP（状态压缩 + 记忆化）"""

    total = m * n                      # 网格总格子数

    @lru_cache(None)
    def dfs(pos: int, mask: int, i_left: int, e_left: int, left_type: int) -> int:
        """
        参数说明：
        pos        : 当前处理的格子编号（0 .. total-1），行主序
        mask       : 前一行的状态，使用 3 进制压缩，每列占一位
        i_left/e_left : 剩余可用的内向/外向人数
        left_type  : 本行左侧已放置格子的类型（0/1/2），用于计算左邻居
        返回值     : 从当前位置到网格末尾的最大幸福增量
        """
        if pos == total:                # 所有格子已处理
            return 0

        row, col = divmod(pos, n)       # 当前格子坐标

        # 取出上方邻居的类型（若越界则为 0）
        up_type = (mask // (3 ** col)) % 3

        best = dfs(pos + 1,
                   mask // 3,          # 把 mask 整体右移一列，准备进入下一格
                   i_left, e_left,
                   0)                  # 选空时，左邻居对后面的格子是 0

        # ---------- 放内向者 ----------
        if i_left > 0:
            cur = 1
            cur_happy = BASE[cur]
            # 与上、左邻居的相互影响（双向计数）
            cur_happy += get_effect(cur, up_type) + get_effect(up_type, cur)
            cur_happy += get_effect(cur, left_type) + get_effect(left_type, cur)

            # 更新 mask：当前格子会成为下一行的“上邻居”
            new_mask = (mask // 3) + cur * (3 ** (n - 1))
            best = max(best,
                       cur_happy + dfs(pos + 1,
                                       new_mask,
                                       i_left - 1, e_left,
                                       cur))

        # ---------- 放外向者 ----------
        if e_left > 0:
            cur = 2
            cur_happy = BASE[cur]
            cur_happy += get_effect(cur, up_type) + get_effect(up_type, cur)
            cur_happy += get_effect(cur, left_type) + get_effect(left_type, cur)

            new_mask = (mask // 3) + cur * (3 ** (n - 1))
            best = max(best,
                       cur_happy + dfs(pos + 1,
                                       new_mask,
                                       i_left, e_left - 1,
                                       cur))

        return best

    # 初始 mask 为全 0（上一行全空），左邻居也为 0
    return dfs(0, 0, introvertsCount, extrovertsCount, 0)


# ------------------- 示例测试 -------------------
if __name__ == "__main__":
    print(maxGridHappiness(2, 3, 1, 2))  # 240
    print(maxGridHappiness(3, 1, 2, 1))  # 260
    print(maxGridHappiness(2, 2, 4, 0))  # 240
```

> **代码要点注释**  
> - `mask // 3`：相当于把上一行的状态向左“滑动”，因为我们已经处理完当前列，下一列的上邻居其实是上一行同一列的状态。  
> - `cur * (3 ** (n - 1))`：把本格子的类型放到 **最高位**，这样它会在下一行的对应列出现。  
> - `left_type` 参数在递归时随列移动，始终保存**本行左侧最近的格子**类型，供下一个格子使用。  

#### 复杂度

- **时间复杂度**：`O(m·n·3^n·I·E)`  
  - `3^n` 是每行可能的压缩状态数（如 `n=5` 时是 243）。  
  - `I = introvertsCount + 1 ≤ 7`、`E = extrovertsCount + 1 ≤ 7` 为剩余人数的取值范围。  
  - 实际上最多约 `25·243·7·7 ≈ 3·10^5` 次状态转移，常数很小，运行在毫秒级。  
  - 与暴力解的 `3^(m·n)` 相比，指数从 `3^25` 降到了 `3^5`，降低了 **指数级**。

- **空间复杂度**：`O(m·n·3^n·I·E)`（记忆化表）  
  - 由于使用 `@lru_cache`，所有子问题的结果都会被存下来。  
  - 这大约也是 30 万 个整数，约几 MB 的内存，完全可以接受。  

---

## 心得  

- **核心技巧**：**行状态压缩 + 动态规划**（又称“按行 DP + 位掩码”）。  
- **适用场景**：  
  1. 网格类问题，且相邻关系只涉及**上、左**两侧（例如 “放置棋子、涂色、布局”）。  
  2. 状态空间受限（行宽 ≤ 5~7），可以用 **3 进制/4 进制**等小基数压缩。  
  3. 需要在每一步维护“前缀信息”，典型例子还有 “Maximum Grid Happiness”（本题），“Maximum Score of a Grid Game”等。  

- **一句话总结解题钥匙**：  
  > 把“上一行的所有格子状态”压成一个整数，用它和左邻居一起决定当前格子的收益，随后递归/DP，既避免了指数爆炸，又能完整考虑所有相邻影响。  

---

## 反思  

- **第一反应**：看到网格、相邻、两种人，立刻想到**枚举所有格子**（暴力）或**贪心**。但很快发现格子之间的相互作用是双向且累计的，贪心难以保证全局最优。  
- **最容易踩的坑**：  
  1. **左邻居的处理**：在行压缩时容易忘记把左侧已经放置的类型传递给下一个格子，导致遗漏左侧的相互影响。  
  2. **mask 更新错误**：`mask // 3` 与 `cur * 3^(n-1)` 的组合必须对应“左移 + 填最高位”，写反会把状态弄错。  
  3. **边界情况**：第一行、第一列的上/左邻居是空（0），一定要在代码里显式返回 0，防止越界。  
  4. **人数限制**：必须在递归/转移时检查 `i_left`、`e_left` 是否足够，否则会出现非法放置导致错误的最大值。  

- **下次类似题的第一步**：  
  > 先判断“相邻关系只涉及已经处理过的方向吗？”（通常是上/左），如果是，就立刻考虑**按行/按列 DP + 状态压缩**，把未处理的方向留到后面再考虑。  

祝你在算法的道路上越走越远 🚀