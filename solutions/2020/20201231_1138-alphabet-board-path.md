# #1138. **字母棋盘路径** / Alphabet Board Path

> 难度：中等 · 标签：Hash Table、String · [LeetCode 链接](https://leetcode.com/problems/alphabet-board-path/)

---

## 题目（英文原版）

**Description**

On an alphabet board, we start at position (0, 0), corresponding to character board[0][0].
Here, board = ["abcde", "fghij", "klmno", "pqrst", "uvwxy", "z"], as shown in the diagram below.
We may make the following moves:
(Here, the only positions that exist on the board are positions with letters on them.)
Return a sequence of moves that makes our answer equal to target in the minimum number of moves.  You may return any path that does so.

**Examples**

**Example 1:**

```
Input: target = "leet"
Output: "DDR!UURRR!!DDD!"
```

**Example 2:**

```
Input: target = "code"
Output: "RR!DDRR!UUL!R!"
```

**Constraints**

- 1 <= target.length <= 100
- target consists only of English lowercase letters.

---

## 题目（中文翻译）

在字母棋盘上，我们从位置 `(0, 0)` 开始，对应字符 `board[0][0]`。  
棋盘定义为  

```
board = ["abcde",
         "fghij",
         "klmno",
         "pqrst",
         "uvwxy",
         "z"]
```

如上图所示，棋盘仅包含上述字母所在的格子。我们可以进行以下移动：

- `U`：向上移动一格（Up）
- `D`：向下移动一格（Down）
- `L`：向左移动一格（Left）
- `R`：向右移动一格（Right）
- `!`：选择当前格子的字符并将其加入答案

要求返回一串移动指令，使得依次选中的字符拼成目标字符串 `target`，且移动次数最少。满足条件的任意一条路径均可返回。

**示例 1**

> **输入** `target = "leet"`  
> **输出** `"DDR!UURRR!!DDD!"`

**示例 2**

> **输入** `target = "code"`  
> **输出** `"RR!DDRR!UUL!R!"`

**约束条件**

- `1 <= target.length <= 100`
- `target` 只包含英文小写字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每一次从当前位置走到下一个目标字符的最短路径单独算出来**，然后把所有小路径拼接起来。  
这一步可以用 **广度优先搜索（BFS）** 完成：

1. 先把字母板上每个字符对应的坐标存进哈希表（`dict`），相当于“查字典”，键是字符，值是 `(row, col)`。  
2. 从当前坐标 `(r, c)` 出发，使用 BFS 按层遍历所有可能的移动（`U,D,L,R`），直到碰到目标字符所在的坐标。  
3. BFS 保证第一次碰到目标坐标的路径就是**最短路径**（因为每一步的代价都是 1），于是我们得到一串移动指令，再加上选字符的 `!`。  
4. 把这段指令接到答案后，更新当前位置为目标字符的坐标，继续处理下一个字符。

> **为什么 BFS 能得到最短路径？**  
> 想象在棋盘上走迷宫，每走一步都花同样的时间（1），BFS 就像波纹一样向四周扩散，最先到达终点的波纹对应的路径就是最少步数的路径。

#### 代码（Python）

```python
from collections import deque

def alphabet_board_path_bruteforce(target: str) -> str:
    # 1️⃣ 建立字符 → 坐标 的映射，像查字典一样
    board = ["abcde", "fghij", "klmno", "pqrst", "uvwxy", "z"]
    pos = {}
    for i, row in enumerate(board):
        for j, ch in enumerate(row):
            pos[ch] = (i, j)

    # 四个方向对应的移动字符
    dirs = [('U', -1, 0), ('D', 1, 0), ('L', 0, -1), ('R', 0, 1)]

    # 判断坐标是否在合法范围内（只能落在有字母的格子上）
    def inside(r, c):
        if 0 <= r < 6 and 0 <= c < 5:          # 前 5 行宽度都是 5
            if r == 5:                         # 第 6 行只有 'z' 在 (5,0)
                return c == 0
            return True
        return False

    # 2️⃣ BFS：从 (sr, sc) 走到 (tr, tc) 的最短路径
    def bfs(sr, sc, tr, tc):
        q = deque()
        q.append((sr, sc, ""))          # 当前坐标 + 已走的指令
        visited = {(sr, sc)}
        while q:
            r, c, path = q.popleft()
            if (r, c) == (tr, tc):
                return path            # 第一次到达目标，就是最短路径
            for move, dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if inside(nr, nc) and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    q.append((nr, nc, path + move))

    # 3️⃣ 依次把每个字符连起来
    cur_r, cur_c = 0, 0          # 起点是 'a' 的坐标 (0,0)
    ans = []
    for ch in target:
        tr, tc = pos[ch]          # 目标字符的坐标
        ans.append(bfs(cur_r, cur_c, tr, tc))  # 最短移动序列
        ans.append('!')           # 选取该字符
        cur_r, cur_c = tr, tc     # 更新当前位置
    return "".join(ans)
```

> **关键行注释**  
> - `inside` 用来判断新坐标是否仍在字母板上，特别处理第 6 行只有 `'z'` 的情况。  
> - `bfs` 返回从起点到终点的最短指令序列（不含 `!`），因为 BFS 按层遍历，第一次碰到目标坐标就一定是最少步数。  

#### 复杂度

- **时间复杂度**：`O(|target| * 25)`  
  - 对每个字符我们都要在最多 25（5×5）个格子里 BFS，实际搜索空间非常小，常数因素不大。  
  - 用大白话说，就是**每个字母最多跑 25 步**，所以整体是 `target 长度 × 25`。
- **空间复杂度**：`O(25)`  
  - BFS 队列和 visited 集合最多保存 25 个坐标，和 `target` 长度无关，属于常数级空间。

---

### 2. 最优解

#### 思路  

暴力解虽然可以 AC，但每次都要跑一次 BFS，有点“画蛇添足”。  
观察字母板的形状我们可以发现：

| 行号 | 内容                |
|------|---------------------|
| 0‑4  | 每行恰好 5 个字母   |
| 5    | 只有 `'z'`，在最左侧 (5,0) |

因此，**从任意位置走到另一位置，只要知道行、列的差值，就能直接写出最短指令**。  
唯一需要注意的是 `'z'` 所在的行只有第 0 列，**不能先向右/下走到非法格子**。  
解决办法：**先把上（U）和左（L）方向走完，再走下（D）和右（R）**。这样如果目标在 `'z'` 行，或者当前在 `'z'` 行，都不会踩到不存在的格子。

具体步骤：

1. **预处理**：用哈希表把每个字母映射到坐标 `(row, col)`（一次性完成）。
2. **遍历目标字符串**，维护当前坐标 `(cr, cc)`（初始是 `'a'` 的 (0,0)）。  
   对于下一个字符 `ch`，取出它的坐标 `(tr, tc)`。
3. 计算行差 `dr = tr - cr`，列差 `dc = tc - cc`。  
   - 如果 `dr < 0`（需要向上），先输出 `'U'` * `|dr|`。  
   - 如果 `dc < 0`（需要向左），先输出 `'L'` * `|dc|`。  
   - 再如果 `dr > 0`（向下），输出 `'D'` * `dr`。  
   - 最后如果 `dc > 0`（向右），输出 `'R'` * `dc`。  
   这种顺序保证不会进入非法格子，尤其是 `'z'` 行的左侧限制。
4. 在走完所有移动后，加上 `'!'` 表示选取该字符。  
5. 把当前位置更新为 `(tr, tc)`，继续处理下一个字符。

> **为什么这种顺序一定是最短？**  
> - 每一步的移动都是 **水平或垂直的最短差距**（因为我们直接用了坐标差），没有多余的绕路。  
> - 只要不违反板子边界，这就是唯一的最短路径。  
> - 只在需要时把 “先上/左后下/右” 的顺序作为“安全措施”，并不会增加额外步数，因为如果不需要避开 `'z'`，这两组指令本来就是可以随意调换的。

#### 代码（Python）

```python
def alphabet_board_path(target: str) -> str:
    # 1️⃣ 预处理：字符 → (row, col) 的映射
    board = ["abcde", "fghij", "klmno", "pqrst", "uvwxy", "z"]
    pos = {}
    for i, row in enumerate(board):
        for j, ch in enumerate(row):
            pos[ch] = (i, j)

    cur_r, cur_c = 0, 0               # 起点是 'a'
    ans = []

    for ch in target:
        tr, tc = pos[ch]              # 目标字符坐标
        dr, dc = tr - cur_r, tc - cur_c

        # 先上/左再下/右，防止走到非法格子（尤其是 'z' 那一行）
        if dr < 0:                    # 向上
            ans.append('U' * (-dr))
        if dc < 0:                    # 向左
            ans.append('L' * (-dc))
        if dr > 0:                    # 向下
            ans.append('D' * dr)
        if dc > 0:                    # 向右
            ans.append('R' * dc)

        ans.append('!')               # 选取字符
        cur_r, cur_c = tr, tc         # 更新当前位置

    return "".join(ans)
```

> **代码要点说明**  
> - `pos` 的构建只做一次，时间开销可以忽略。  
> - `ans.append('U' * (-dr))` 利用字符串乘法一次性生成多次同方向的指令，既简洁又高效。  
> - 移动顺序 **U→L→D→R** 正是“先上/左后下/右”，确保不会在走到 `'z'` 时走出边界。

#### 复杂度

- **时间复杂度**：`O(|target|)`  
  - 对每个字符只做常数次算术和字符串拼接，整体随目标长度线性增长。  
  - 与暴力解的 `O(|target| * 25)` 相比，省掉了每次 BFS 的搜索，快了约 25 倍（常数因子更小）。

- **空间复杂度**：`O(1)`（不计输出字符串）  
  - 只用了固定大小的哈希表（26 条记录）和几个整数变量，和 `target` 长度无关。

---

## 心得

- **核心技巧**：把二维坐标差直接转化为移动指令，并注意特殊格子（`z`）的行列限制。  
- **适用的题型**  
  1. 在固定网格上从一点走到另一点，要求最短路径且每步代价相同（如 “Robot Move” 系列）。  
  2. 需要把字符映射到坐标并按顺序访问的字符串题（如 “Keyboard Row Path”。）  
  3. 任何出现“字母键盘”或“棋盘”且移动规则为上下左右的题目。  

> **一句话总结解题钥匙**：**坐标差 + “先上/左后下/右” 的安全顺序 = 最短路径**。

---

## 反思

- **第一反应**：先想到 BFS 逐段搜索最短路径，因为 BFS 是“找最短路”的常用套路。  
- **最容易踩的坑**  
  1. **`z` 的行只有一列**：如果直接把 `D` 放在 `R` 前面，可能会尝试走到 `(5,1)` 这种不存在的格子。  
  2. **字符坐标映射错误**：忘记把 `'z'` 放在第 5 行第 0 列，导致坐标错位。  
  3. **忘记在每次移动后加 `!`**：导致输出字符串缺少选字符指令。  

- **下次遇到同类题**，第一步应该先 **把每个目标点的坐标写出来**，再 **比较坐标差**，思考是否有“特殊格子”需要先处理方向顺序。这样可以直接写出 O(N) 的最优解，而不必跑 BFS。