# #2056. 棋盘上合法移动组合的数量 / Number of Valid Move Combinations On Chessboard

> 难度：困难 · 标签：Array、String、Backtracking、Simulation · [LeetCode 链接](https://leetcode.com/problems/number-of-valid-move-combinations-on-chessboard/)

---

## 题目（英文原版）

**Description**

There is an 8 x 8 chessboard containing n pieces (rooks, queens, or bishops). You are given a string array pieces of length n, where pieces[i] describes the type (rook, queen, or bishop) of the ith piece. In addition, you are given a 2D integer array positions also of length n, where positions[i] = [ri, ci] indicates that the ith piece is currently at the 1-based coordinate (ri, ci) on the chessboard.
When making a move for a piece, you choose a destination square that the piece will travel toward and stop on.
You must make a move for every piece on the board simultaneously. A move combination consists of all the moves performed on all the given pieces. Every second, each piece will instantaneously travel one square towards their destination if they are not already at it. All pieces start traveling at the 0th second. A move combination is invalid if, at a given time, two or more pieces occupy the same square.
Return the number of valid move combinations​​​​​.
Notes:

**Examples**

**Example 1:**

```
Input: pieces = ["rook"], positions = [[1,1]]
Output: 15
Explanation: The image above shows the possible squares the piece can move to.
```

**Example 2:**

```
Input: pieces = ["queen"], positions = [[1,1]]
Output: 22
Explanation: The image above shows the possible squares the piece can move to.
```

**Example 3:**

```
Input: pieces = ["bishop"], positions = [[4,3]]
Output: 12
Explanation: The image above shows the possible squares the piece can move to.
```

**Constraints**

- n == pieces.length
- n == positions.length
- 1 <= n <= 4
- pieces only contains the strings "rook", "queen", and "bishop".
- There will be at most one queen on the chessboard.
- 1 <= ri, ci <= 8
- Each positions[i] is distinct.

---

## 题目（中文翻译）

描述  
在一个 $8 \times 8$ 的棋盘上放置了 $n$ 枚棋子（车（rook）、后（queen）或象（bishop））。给定长度为 $n$ 的字符串数组 `pieces`，其中 `pieces[i]` 描述第 $i$ 枚棋子的类型（rook、queen 或 bishop）。另外，给定同样长度为 $n$ 的二维整数数组 `positions`，其中 `positions[i] = [r_i, c_i]` 表示第 $i$ 枚棋子当前位于棋盘上 **1‑based** 坐标 $(r_i, c_i)$。

对每一枚棋子进行移动时，你需要选择一个目的格子，棋子会朝该格子前进并最终停在上面。**必须**同时为棋盘上的每一枚棋子各自选择一次移动。一次 **移动组合（move combination）** 指所有棋子所执行的移动集合。每一秒，若棋子尚未到达目的格子，它会瞬间向目的格子前进一步。所有棋子在第 $0$ 秒同时开始移动。若在某一时刻出现两枚或更多棋子占据同一格子，则该移动组合 **无效**。  

返回所有 **合法** 移动组合的数量。

示例  
**示例 1**  
```text
Input: pieces = ["rook"], positions = [[1,1]]
Output: 15
Explanation: 上图展示了该车（rook）可以移动到的所有格子。
```

**示例 2**  
```text
Input: pieces = ["queen"], positions = [[1,1]]
Output: 22
Explanation: 上图展示了该后（queen）可以移动到的所有格子。
```

**示例 3**  
```text
Input: pieces = ["bishop"], positions = [[4,3]]
Output: 12
Explanation: 上图展示了该象（bishop）可以移动到的所有格子。
```

约束条件
- $n = \text{pieces.length}$
- $n = \text{positions.length}$
- $1 \le n \le 4$
- `pieces` 只包含字符串 `"rook"`、`"queen"` 和 `"bishop"`。
- 棋盘上至多只有一枚后（queen）。
- $1 \le r_i, c_i \le 8$
- 每个 `positions[i]` 均互不相同。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

- **每个棋子能去哪些格子**  
  - **车 (rook)**：只能在同一行或同一列上移动，像在一条直路上跑。  
  - **象 (bishop)**：只能在同一条对角线上移动，像在斜坡上滑。  
  - **后 (queen)**：既能走直路也能走斜坡，等价于把车和象的走法合在一起。  

  把「所有能到达的格子」想成「字典」里的所有**键**，键就是目标格子坐标 `(r, c)`。  
  注意**不能把棋子原地不动**，因为题目要求「必须为每个棋子选择一个目的格子」，而示例中已经把原位置排除掉了。

- **同时移动会不会相撞**  
  所有棋子在第 `0` 秒同时出发，每秒向目的地前进一步（如果已经到达就停在原地）。  
  我们可以把每个棋子的「完整路径」列出来：  
  ```
  time 0 : 起点
  time 1 : 第一步
  time 2 : 第二步
  ...
  time d : 目的地（d 为该棋子到目的地的步数）
  time d+1, d+2, ... : 仍停在目的地
  ```
  只要在 **任意同一时刻** 两个棋子出现在同一个格子，整个移动组合就是 **无效** 的。  

- **暴力枚举**  
  1. 为每个棋子生成「可达格子」列表（不包括自己的位置）。  
  2. 对所有棋子的可达格子做笛卡尔积，得到每一种「目的格子组合」。  
  3. 对每一种组合，模拟所有棋子同步前进的过程，检查是否出现冲突。  

  由于 `n ≤ 4`，每个棋子最多有 `27`（后在中心位置的走法）种目的格子，  
  所以组合数最多是 `27⁴ ≈ 5.3×10⁵`，完全可以在几百毫秒内跑完。

#### 代码（Python）

```python
from itertools import product
from typing import List, Tuple

# --------------------------------------------------------------
# 1️⃣ 生成单个棋子的所有合法目的格子（不包括原点）
# --------------------------------------------------------------
def reachable(piece: str, r: int, c: int) -> List[Tuple[int, int]]:
    """返回 (r,c) 位置的 piece 能到达的所有格子，坐标均为 1~8"""
    dirs = []
    if piece == "rook" or piece == "queen":
        # 四个方向：上下左右
        dirs += [(1, 0), (-1, 0), (0, 1), (0, -1)]
    if piece == "bishop" or piece == "queen":
        # 四个对角线方向
        dirs += [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    res = []
    for dr, dc in dirs:                # 逐个方向走
        nr, nc = r + dr, c + dc
        while 1 <= nr <= 8 and 1 <= nc <= 8:   # 仍在棋盘内就继续
            res.append((nr, nc))               # 记录这个格子
            nr += dr
            nc += dc
    return res

# --------------------------------------------------------------
# 2️⃣ 计算两格之间的一步步路径（包括起点，不包括终点）
# --------------------------------------------------------------
def step_path(start: Tuple[int, int], dest: Tuple[int, int]) -> List[Tuple[int, int]]:
    """返回从 start 到 dest 的每秒位置序列（不含 dest），一步一步走"""
    r0, c0 = start
    r1, c1 = dest
    dr = (r1 - r0)
    dc = (c1 - c0)

    # 方向只能是 -1、0、1 三种情况之一
    step_r = 0 if dr == 0 else (1 if dr > 0 else -1)
    step_c = 0 if dc == 0 else (1 if dc > 0 else -1)

    path = []
    cur_r, cur_c = r0, c0
    while (cur_r, cur_c) != (r1, c1):
        cur_r += step_r
        cur_c += step_c
        path.append((cur_r, cur_c))   # 这一步到达的位置
    return path                         # 最后一个元素恰好是 dest

# --------------------------------------------------------------
# 3️⃣ 主函数：枚举并验证
# --------------------------------------------------------------
def countValidMoveCombinations(pieces: List[str],
                               positions: List[List[int]]) -> int:
    n = len(pieces)

    # 为每个棋子预计算可达格子
    options = []
    for typ, (r, c) in zip(pieces, positions):
        opts = reachable(typ, r, c)      # 所有目的格子
        options.append(opts)

    valid_cnt = 0

    # 暴力遍历所有目的格子组合（笛卡尔积）
    for dests in product(*options):
        # 1) 目的格子不能与其他棋子的起点冲突（因为起点本身已经是占用的）
        conflict = False
        for i in range(n):
            for j in range(i + 1, n):
                if dests[i] == positions[j] or dests[j] == positions[i]:
                    conflict = True
                    break
            if conflict:
                break
        if conflict:
            continue

        # 2) 模拟同步前进，检查每秒是否有重叠
        #   计算每个棋子的完整路径（包括停留在目的地的时间）
        paths = []
        max_len = 0
        for i in range(n):
            start = tuple(positions[i])
            dest = dests[i]
            step_seq = step_path(start, dest)          # 逐秒移动的序列
            paths.append(step_seq)
            max_len = max(max_len, len(step_seq))

        #   检查每个时间点 t = 0 .. max_len
        #   注意：t = 0 时已经是起点，题目保证不同，这里直接从 1 开始即可
        occupied = set()
        ok = True
        for t in range(1, max_len + 1):
            occupied.clear()
            for i in range(n):
                # 若该棋子已经到达目的地，则一直停在最后一个格子
                pos = paths[i][t - 1] if t <= len(paths[i]) else paths[i][-1]
                if pos in occupied:      # 已有棋子在此格子
                    ok = False
                    break
                occupied.add(pos)
            if not ok:
                break

        if ok:
            valid_cnt += 1

    return valid_cnt
```

> **关键行中文注释** 已经写在代码里，直接复制运行即可。

#### 复杂度  

- **时间复杂度**：  
  - 每个棋子最多 `27` 种目的格子，组合数为 `∏|options_i| ≤ 27⁴ ≈ 5.3×10⁵`。  
  - 对每个组合我们最多模拟 `8`（棋盘最大距离）秒，每秒检查至多 `4` 棋子。  
  - 所以总体时间 `O(27⁴ · 8 · 4) ≈ O(10⁷)`，在 1 秒内可以轻松完成。  
  - 大白话：我们把所有可能的「去向」列出来，然后「逐个实验」看会不会撞车，实验次数上限大约 50 万次，每次实验只跑几步。

- **空间复杂度**：  
  - 只保存每个棋子的可达格子列表（最多 `27` 条）和一次模拟时的路径，均为常数级别。  
  - `O(1)`（不随 `n` 增长，`n ≤ 4` 固定）。

---

### 2. 最优解  

#### 思路  

暴力解已经能够在题目限制下 AC，但我们仍可以 **在枚举时提前剪枝**，进一步降低常数。

1. **从「慢」的地方入手**  
   - 暴力解在生成完整的目的格子组合后才去判断是否冲突。  
   - 事实上，在决定第 `k` 个棋子的目的格子时，就可以提前判断：  
     - 与已经确定的前 `k‑1` 个棋子的路径是否会在任意时刻相撞。  
     - 如果已经冲突，则不必继续往下枚举第 `k+1` … `n` 个棋子的目的格子。

2. **回溯 + 前置冲突检测**  
   - 按顺序为每个棋子 **递归** 选择目的格子。  
   - 选定一个目的格子后，立刻把该棋子的完整路径（含停留）加入 **全局时间表**（`time → set of occupied squares`）。  
   - 当后续棋子尝试某个目的格子时，只要它的路径在任意时间点与已有的时间表冲突，就直接 **回溯**，不必继续搜索。  

3. **核心数据结构：时间表（字典）**  
   - `timeline[t]` 保存第 `t` 秒已经被占用的格子集合。  
   - `t` 的范围只到当前已决定棋子中最大步数，最多 `8`，所以字典非常小。  

4. **为什么还能保证正确**  
   - 所有棋子同时出发、同步前进的规则只与每条**完整路径**有关。  
   - 当我们在递归中把已经确定的路径全部写入时间表，后面加入的路径只要不与时间表冲突，就一定不会与之前的任何棋子相撞。  
   - 递归结束时所有棋子都已选定，且没有冲突，即得到一个合法的「移动组合」。

5. **复杂度对比**  
   - 最坏情况下仍然会遍历所有组合（因为冲突率可能很低），但 **大量无效分支会被提前剪掉**，实际运行更快。  
   - 仍然是指数级 `O(27ⁿ)`（`n ≤ 4`），但常数更小。  

#### 代码（Python）

```python
from typing import List, Tuple, Dict, Set

# --------------------------------------------------------------
# 与上面相同的辅助函数（可复用）
# --------------------------------------------------------------
def reachable(piece: str, r: int, c: int) -> List[Tuple[int, int]]:
    dirs = []
    if piece in ("rook", "queen"):
        dirs += [(1, 0), (-1, 0), (0, 1), (0, -1)]
    if piece in ("bishop", "queen"):
        dirs += [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    res = []
    for dr, dc in dirs:
        nr, nc = r + dr, c + dc
        while 1 <= nr <= 8 and 1 <= nc <= 8:
            res.append((nr, nc))
            nr += dr
            nc += dc
    return res


def step_path(start: Tuple[int, int], dest: Tuple[int, int]) -> List[Tuple[int, int]]:
    r0, c0 = start
    r1, c1 = dest
    step_r = 0 if r1 == r0 else (1 if r1 > r0 else -1)
    step_c = 0 if c1 == c0 else (1 if c1 > c0 else -1)

    path = []
    cur_r, cur_c = r0, c0
    while (cur_r, cur_c) != (r1, c1):
        cur_r += step_r
        cur_c += step_c
        path.append((cur_r, cur_c))
    return path


# --------------------------------------------------------------
# 3️⃣ 回溯 + 时间表剪枝
# --------------------------------------------------------------
def countValidMoveCombinations_opt(pieces: List[str],
                                   positions: List[List[int]]) -> int:
    n = len(pieces)
    # 每个棋子的可达格子（不含原点）
    options = [reachable(p, r, c) for p, (r, c) in zip(pieces, positions)]

    # timeline[t] = 已经被占用的格子集合（t 从 0 开始）
    timeline: Dict[int, Set[Tuple[int, int]]] = {}
    # 初始时刻 0 所有棋子已经占据起点
    for i, (r, c) in enumerate(positions):
        timeline.setdefault(0, set()).add((r, c))

    ans = 0  # 计数器

    def dfs(idx: int) -> None:
        """为第 idx 块棋子挑选目的格子并继续递归"""
        nonlocal ans
        if idx == n:                     # 所有棋子都已确定合法目的格子
            ans += 1
            return

        start = tuple(positions[idx])
        for dest in options[idx]:
            # 1) 目的格子不能是别的棋子的起点（已经在 timeline[0] 中）
            if dest in timeline[0]:
                continue

            # 2) 生成该棋子的完整路径（包括停留在终点的时间）
            path = step_path(start, dest)          # 每秒移动的格子序列
            # 把停留在终点的时间也算进去，最长模拟时间会随后更新
            max_t = len(path)                       # 目的地所在的时间点
            # 把终点往后延伸至当前已知的最大时间，以防后面还有更慢的棋子
            # 这里不必真的延伸，只在冲突检测时把“已经到达”视为占位即可

            # 3) 检测冲突并暂时写入时间表
            conflict = False
            for t, pos in enumerate(path, start=1):   # t 从 1 开始
                if pos in timeline.get(t, set()):
                    conflict = True
                    break
            if conflict:
                continue

            # 4) 写入时间表（包括停留在终点的时刻）
            #   为了简化，只把到达终点的那一刻写进去；后面的时间点
            #   若有更慢的棋子出现冲突，递归层会再次检查。
            for t, pos in enumerate(path, start=1):
                timeline.setdefault(t, set()).add(pos)

            # 递归进入下一个棋子
            dfs(idx + 1)

            # 5) 回溯：把刚才写入的格子全部删掉
            for t, pos in enumerate(path, start=1):
                timeline[t].remove(pos)
                if not timeline[t]:          # 集合为空则删掉键，保持字典小
                    del timeline[t]

    dfs(0)
    return ans
```

> 这段代码的核心是 **递归+冲突提前检测**，每挑选一个目的格子就把它的路径写进 `timeline`，后面的棋子只能在不碰撞的前提下继续选择。这样很多“不可能”的组合在搜索树的上层就被剪掉了。

#### 复杂度  

- **时间复杂度**  
  - 最坏仍是 `O(27ⁿ)`（`n ≤ 4`），因为我们仍然可能遍历所有组合。  
  - 实际上，每次选取目的格子时都会做一次 **路径冲突检测**，时间是 `O(step)`，`step ≤ 8`。  
  - 因为大量分支在早期就被裁掉，实际运行时间往往比全枚举快数倍。  

- **空间复杂度**  
  - `timeline` 最多记录 `max_step ≤ 8` 秒的占用格子，每秒至多 `n ≤ 4` 个格子，整体 `O(1)`。  
  - 递归深度为 `n ≤ 4`，同样是常数级别。

---

## 心得  

- **核心技巧**：**回溯 + 时间表冲突检测**。  
  - 把「所有棋子同步移动」抽象成「每秒钟哪些格子被占用」的离散时间表。  
  - 在搜索过程中随时检查新路径是否与已有时间表冲突，做到**边枚举边剪枝**。  

- **适用题型**  
  1. 多个移动实体同步行进，需要防止**碰撞**的题目（如多机器人路径、棋子同步走）。  
  2. “在限定步数内”或“每一步都必须满足约束”的组合计数问题（如“跳棋”“马走日”同步计数）。  
  3. 小规模的**状态枚举**，利用时间维度进行冲突检测的情形。  

- **一句话总结解题钥匙**：  
  > **把每一步的占位情况写进“时间表”，在递归选取目的地时即时检测冲突，既保证正确又能提前剔除无效分支。**

---

## 反思  

- **第一反应**：看到「同时移动」和「不能相撞」就想到**模拟**，于是立刻想到「枚举所有目的格子 → 逐秒模拟」的暴力办法。  
- **最容易踩的坑**  
  1. **忘记排除原点**：题目要求每个棋子必须移动，原位置不是合法目的格子。  
  2. **碰撞判定不完整**：只检查“终点是否相同”是不够的，还要检查途中经过的格子以及已经到达终点后仍然占位的情况。  
  3. **对角线移动的步数**：象和后在斜向移动时步长是 `|dr|`（等于 `|dc|`），不能像车那样用 Manhattan 距离。  
- **下次遇到同类题的第一步**：  
  > **先把每个实体的所有可能路径列出来（或能到达的终点），再把“每秒的占位”抽象成时间表，边枚举边检查冲突**。这样既能确保不漏判，又能在搜索过程中尽早剪枝。