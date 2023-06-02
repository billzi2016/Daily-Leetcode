# #2267. 检查是否存在有效的括号字符串路径 /  Check if There Is a Valid Parentheses String Path

> 难度：困难 · 标签：Array、Dynamic Programming、Matrix · [LeetCode 链接](https://leetcode.com/problems/check-if-there-is-a-valid-parentheses-string-path/)

---

## 题目（英文原版）

**Description**

A parentheses string is a non-empty string consisting only of '(' and ')'. It is valid if any of the following conditions is true:
You are given an m x n matrix of parentheses grid. A valid parentheses string path in the grid is a path satisfying all of the following conditions:
Return true if there exists a valid parentheses string path in the grid. Otherwise, return false.

**Examples**

**Example 1:**

```
Input: grid = [["(","(","("],[")","(",")"],["(","(",")"],["(","(",")"]]
Output: true
Explanation: The above diagram shows two possible paths that form valid parentheses strings.
The first path shown results in the valid parentheses string "()(())".
The second path shown results in the valid parentheses string "((()))".
Note that there may be other valid parentheses string paths.
```

**Example 2:**

```
Input: grid = [[")",")"],["(","("]]
Output: false
Explanation: The two possible paths form the parentheses strings "))(" and ")((". Since neither of them are valid parentheses strings, we return false.
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 100
- grid[i][j] is either '(' or ')'.

---

## 题目（中文翻译）

**描述**  
括号字符串（parentheses string）是仅由字符 `'('` 和 `')'` 组成的非空字符串。若满足以下任意条件，则该字符串是有效的（valid）：

（题目原文未给出具体条件，此处默认指常规的括号匹配规则，即每个 `'('` 必须在后面对应一个 `')'`，且任意前缀的 `'('` 数量不小于 `')'` 的数量，整体 `'('` 与 `')'` 数量相等。）

给定一个 `m x n` 的括号网格（parentheses grid），即一个由 `'('` 和 `')'` 组成的矩阵。**有效的括号字符串路径**（valid parentheses string path）是指从左上角 `(0,0)` 出发，只能向右或向下移动，最终到达右下角 `(m‑1, n‑1)`，并且沿途经过的字符连接起来形成一个有效的括号字符串。

返回 `true` 表示在网格中存在至少一条满足上述条件的路径；否则返回 `false`。

**示例 1**  
```text
Input: grid = [["(","(","("],
               [")","(",")"],
               ["(","(",")"],
               ["(","(",")"]]
Output: true
Explanation: 上图展示了两条可以形成有效括号字符串的路径。  
第一条路径得到的字符串是 `"()(())"`；  
第二条路径得到的字符串是 `"((()))"`。  
注意，可能还存在其他有效的路径。
```

**示例 2**  
```text
Input: grid = [[" )"," )"],
               [" ("," ("]]
Output: false
Explanation: 两条可能的路径分别形成括号字符串 `"))("` 和 `")(("`，它们都不是有效的括号字符串，因此返回 `false`。
```

**约束条件**  
- `m == grid.length`  
- `n == grid[i].length`  
- `1 <= m, n <= 100`  
- `grid[i][j]` 仅为 `'('` 或 `')'`。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有可能的路径都枚举出来，逐条检查它们拼成的括号串是否合法。  

- **路径的定义**：从左上角 `(0,0)` 出发，只能向右或向下走，最终到达右下角 `(m-1,n-1)`。这和走迷宫、找最短路径的思路完全一样。  
- **遍历方式**：用深度优先搜索（DFS）递归地尝试「向右」或「向下」两条分支。每走一步就把当前格子的字符 `'('` 或 `')'` 加到一个临时字符串 `path` 里。  
- **合法性判断**：遍历完一条完整路径后，用一个小函数检查 `path` 是否是「有效括号串」：从左到右扫描，维护一个计数器 `balance`（打开的 '(' 数量减去已经匹配的 ')' 数量），  
  - 遇到 `'('` 就 `balance += 1`；  
  - 遇到 `')'` 就 `balance -= 1`。  
  - **关键**：如果在任何位置 `balance` 变成负数，说明右括号比左括号多，序列已经不合法；遍历结束后 `balance` 必须恰好为 0，才能算合法。  

> **类比**：`balance` 就像一本字典的“未匹配的左括号页码”。只要页码不小于 0，说明左括号够用；最后页码为 0 才算所有左括号都找到了对应的右括号。

因为我们把所有路径都跑一遍，所以一定能找到一条合法的（如果存在的话），答案必然正确。

#### 代码（Python）

```python
from typing import List

def is_valid(seq: str) -> bool:
    """检查 seq 是否是合法的括号串"""
    balance = 0
    for ch in seq:
        if ch == '(':
            balance += 1
        else:               # ch == ')'
            balance -= 1
        if balance < 0:    # 右括号多了，已经不合法
            return False
    return balance == 0    # 必须恰好匹配完

def hasValidPath_bruteforce(grid: List[List[str]]) -> bool:
    m, n = len(grid), len(grid[0])
    target_len = m + n - 1                # 路径上格子总数

    def dfs(i: int, j: int, path: List[str]) -> bool:
        """从 (i,j) 出发继续搜索，path 保存已走过的字符列表"""
        path.append(grid[i][j])           # 把当前格子字符加入路径

        # 已经走到终点，检查完整路径是否合法
        if i == m - 1 and j == n - 1:
            result = is_valid(''.join(path))
            path.pop()                    # 回溯：撤销当前格子
            return result

        # 向右走
        if j + 1 < n and dfs(i, j + 1, path):
            path.pop()
            return True
        # 向下走
        if i + 1 < m and dfs(i + 1, j, path):
            path.pop()
            return True

        path.pop()                        # 回溤：撤销当前格子，继续探索其他分支
        return False

    return dfs(0, 0, [])
```

#### 复杂度  

- **时间复杂度**：`O(2^{m+n})`（指数级）  
  - 每一步都有两种选择（右/下），总共走 `m+n-2` 步，所有路径数大约是 `C(m+n-2, m-1)`，在最坏情况下近似 `2^{m+n}`。  
  - 对每条路径我们还要遍历一次字符检查合法性，时间仍然是指数级。  
  - **大白话**：如果网格是 10×10，大约有 2^{18} ≈ 260 000 条路径，已经很大；100×100 时更是天文数字，根本跑不完。  

- **空间复杂度**：`O(m+n)`（递归栈 + 路径字符串）  
  - 递归深度最多 `m+n-1`，路径列表也只保存当前走过的字符，同样是线性空间。  

> 暴力解只能用来验证思路或在极小的测试数据上跑通，实际提交会超时。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到**瓶颈**在于「枚举所有路径」。我们需要一种方式，**一次遍历就把所有可能的状态合并**，不必逐条检查。  

观察合法括号串的**前缀性质**：

1. 对于任意前缀，左括号的数量 **不小于** 右括号的数量。  
2. 整个串结束时，左括号数量恰好等于右括号数量。  

用一个整数 `balance` 表示「已经走过的格子中，左括号比右括号多了多少」。  
- 初始 `balance = 1`（因为左上角一定要先放进去，它可能是 '(' 也可能是 ')'，若是 ')' 那么 `balance` 直接为负，说明根本不可能合法）。  
- 每走一步：  
  - `'('` → `balance += 1`（多了一个左括号）  
  - `')'` → `balance -= 1`（用掉一个左括号）  
- 只要 `balance` 维持 **非负**，这条路径的前缀仍然有可能成为合法串。  

于是**状态**可以抽象为 `(i, j, balance)`：在格子 `(i, j)` 处，当前的 `balance` 为多少。  
从一个状态我们只能向 **右** 或 **下** 两个方向转移，转移后更新 `balance`。如果转移后 `balance` 为负，则该分支直接剪枝（不再继续）。  

这正好是**动态规划（DP）**的典型模型：  
- **子问题**：到达某格子时，可能的 `balance` 有哪些？  
- **递推**：把上一步的可能 `balance` 通过右/下两条边转移得到当前格子的可能 `balance`。  
- **初始状态**：`(0,0, start_balance)`，其中 `start_balance = 1` 若左上角是 `'('`，否则直接返回 `False`。  
- **结束条件**：在右下角 `(m-1,n-1)`，若存在 `balance == 0` 的状态，则说明有合法路径。  

**实现细节**  

- `balance` 最大不会超过路径长度 `L = m + n - 1`（全部都是 '(' 的极端），所以我们可以把 `balance` 限制在 `[0, L]`。  
- 为了节省空间，用 `set` 保存每个格子所有可达的 `balance`，或者直接使用布尔数组 `dp[i][j][b]`。这里采用 **集合**，代码更直观：  
  ```python
  dp[i][j] = {b1, b2, ...}
  ```  
- 逐行/逐列遍历网格（或 BFS），把上面/左边的集合转移进来。  
- 复杂度上：**状态总数** 为 `m * n * L`，其中 `L ≤ 200`（因为 `m,n ≤ 100`），约为两百万，完全可以在一秒内完成。  

> **类比**：想象每个格子是一座小城，`balance` 是“手里剩余的左括号票”。从左上城出发，你每经过一条路（右或下），都要根据城里卖的票（'(' 或 ')'）增减手中的票数。只要票数不变负，你还能继续前进；到终点时恰好票数为 0，说明你刚好用完所有票——这就是合法路径。

#### 代码（Python）

```python
from typing import List

def hasValidPath(grid: List[List[str]]) -> bool:
    m, n = len(grid), len(grid[0])
    L = m + n - 1                     # 任意路径的格子数上限

    # 起点必须是 '('，否则一开始 balance 就为负，直接不可能
    if grid[0][0] == ')':
        return False

    # dp[i][j] 用集合记录在 (i,j) 处可以得到的所有合法 balance
    dp = [[set() for _ in range(n)] for _ in range(m)]
    dp[0][0].add(1)                   # 起点是 '('，balance = 1

    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                continue               # 起点已经初始化
            cur_char = grid[i][j]

            # 从上面过来
            if i > 0:
                for bal in dp[i-1][j]:
                    nb = bal + (1 if cur_char == '(' else -1)
                    if nb >= 0:        # 只保留非负的 balance
                        dp[i][j].add(nb)

            # 从左边过来
            if j > 0:
                for bal in dp[i][j-1]:
                    nb = bal + (1 if cur_char == '(' else -1)
                    if nb >= 0:
                        dp[i][j].add(nb)

    # 终点若存在 balance == 0，则说明有合法路径
    return 0 in dp[m-1][n-1]
```

#### 复杂度  

- **时间复杂度**：`O(m * n * L)`，其中 `L = m + n - 1 ≤ 200`。  
  - 对每个格子我们遍历它上方和左方的所有可能 `balance`，每个集合大小最多 `L`，所以总操作数约为 `m*n*L`。  
  - **大白话**：在最大 100×100 的网格里，最多算两百万次「加一或减一」的简单操作，跑得非常快。  

- **空间复杂度**：`O(m * n * L)`（使用布尔数组时）或 `O(m * n * avg_set_size)`（集合实现）。  
  - 同样是把每个格子的所有可能 `balance` 记下来，最坏情况下每个格子会存 `L` 个整数，整体仍然在几 MB 级别，完全可以接受。  

> 与暴力解相比，时间从指数级下降到线性级（相对于网格面积），是本题的关键突破。

---

## 心得  

- **核心技巧**：利用括号序列的「前缀平衡」特性，把「合法性」转化为一个非负整数 `balance`，并在动态规划中维护所有可能的 `balance`。  
- **适用题型**：  
  1. **路径上的括号匹配**（本题）。  
  2. **在网格/树上找满足前缀约束的路径**（如“只允许出现不超过 K 次的某字符的路径”）。  
  3. **带有“累计和不低于 0”约束的 DP**（比如“最大子矩形和不小于 0”类问题）。  
- **一句话总结解题钥匙**：**把“合法括号串”抽象为“路径上始终保持非负的平衡计数”，用 DP 把所有可能的平衡合并在一起**。

---

## 反思  

- **第一反应**：看到“有效括号串”马上想到栈或计数器，随后想到把每一步的计数当作状态来做 DP。  
- **最容易踩的坑**：  
  - 起点是 `')'` 时直接返回 `False`（因为一开始就负了）。  
  - 忽略了路径长度的上限导致 `balance` 超出数组范围，实际上 `balance` 最大只能到 `m+n-1`。  
  - 在转移时忘记检查 `nb >= 0`，导致无效的负平衡被错误保留下来。  
- **下次类似题**：第一步先写出“前缀必须满足的约束”（如非负、累计和 ≤ K），再思考**状态**是否可以用一个或几个整数来表示，并尝试用 DP 或 BFS 合并所有可能的状态。