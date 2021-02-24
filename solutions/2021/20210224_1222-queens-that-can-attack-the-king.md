# #1222. 可以攻击国王的皇后 / Queens That Can Attack the King

> 难度：中等 · 标签：Array、Matrix、Simulation · [LeetCode 链接](https://leetcode.com/problems/queens-that-can-attack-the-king/)

---

## 题目（英文原版）

**Description**

On a 0-indexed 8 x 8 chessboard, there can be multiple black queens and one white king.
You are given a 2D integer array queens where queens[i] = [xQueeni, yQueeni] represents the position of the ith black queen on the chessboard. You are also given an integer array king of length 2 where king = [xKing, yKing] represents the position of the white king.
Return the coordinates of the black queens that can directly attack the king. You may return the answer in any order.

**Examples**

**Example 1:**

```
Input: queens = [[0,1],[1,0],[4,0],[0,4],[3,3],[2,4]], king = [0,0]
Output: [[0,1],[1,0],[3,3]]
Explanation: The diagram above shows the three queens that can directly attack the king and the three queens that cannot attack the king (i.e., marked with red dashes).
```

**Example 2:**

```
Input: queens = [[0,0],[1,1],[2,2],[3,4],[3,5],[4,4],[4,5]], king = [3,3]
Output: [[2,2],[3,4],[4,4]]
Explanation: The diagram above shows the three queens that can directly attack the king and the three queens that cannot attack the king (i.e., marked with red dashes).
```

**Constraints**

- 1 <= queens.length < 64
- queens[i].length == king.length == 2
- 0 <= xQueeni, yQueeni, xKing, yKing < 8
- All the given positions are unique.

---

## 题目（中文翻译）

**描述**  
在一个 0 起始索引的 8 × 8 国际象棋棋盘上，可能有多个黑皇后（queen）和唯一的白国王（king）。  
给定一个二维整数数组 `queens`，其中 `queens[i] = [xQueen_i, yQueen_i]` 表示第 i 个黑皇后的位置。另给定一个长度为 2 的整数数组 `king = [xKing, yKing]`，表示白国王的位置。  

返回所有能够直接攻击国王的黑皇后的位置坐标。答案的顺序不限。

**示例**  

*示例 1*  
```
Input: queens = [[0,1],[1,0],[4,0],[0,4],[3,3],[2,4]], king = [0,0]
Output: [[0,1],[1,0],[3,3]]
Explanation: 上图展示了能够直接攻击国王的三枚皇后以及无法攻击国王的三枚皇后（用红色虚线标记）。
```

*示例 2*  
```
Input: queens = [[0,0],[1,1],[2,2],[3,4],[3,5],[4,4],[4,5]], king = [3,3]
Output: [[2,2],[3,4],[4,4]]
Explanation: 上图展示了能够直接攻击国王的三枚皇后以及无法攻击国王的三枚皇后（用红色虚线标记）。
```

**约束条件**  

- `1 <= queens.length < 64`
- `queens[i].length == king.length == 2`
- `0 <= xQueen_i, yQueen_i, xKing, yKing < 8`
- 所有给定的位置互不相同。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：遍历每一只黑皇后，判断它是否和王在同一直线（横向、纵向或对角线）上，并且中间没有其他棋子阻挡。  

- **数据结构**：我们把所有皇后的位置放进一个 **集合**（`set`），类似于查字典：键（key）是坐标 `(x, y)`，值（value）可以直接忽略，只是为了 O(1) 时间判断某格子是否有皇后。  
- **判断是否能攻击**：  
  1. **同一行**：`x == king_x`。从皇后往王的方向一步步走（左或右），如果遇到另一只皇后就说明被挡住了，当前皇后不能攻击。  
  2. **同一列**：`y == king_y`，同理上下走。  
  3. **同一对角线**：`abs(x - king_x) == abs(y - king_y)`，沿着左上‑右下或右上‑左下的斜线逐格检查。  
- **正确性**：只要在同一直线上且没有其他皇后挡住，皇后就可以“一步到位”吃掉国王，符合国际象棋的走法规则。  

#### 代码（Python）  
```python
from typing import List, Set, Tuple

def queensAttacktheKing_bruteforce(queens: List[List[int]], king: List[int]) -> List[List[int]]:
    # 把所有皇后坐标放进集合，查找是否有皇后占据某格子是 O(1) 时间
    queen_set: Set[Tuple[int, int]] = {tuple(q) for q in queens}
    kx, ky = king
    ans: List[List[int]] = []

    # 8 个方向的增量向量，分别对应 上、下、左、右、左上、右上、左下、右下
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]

    # 对每个方向，沿着该方向一直走，遇到第一只皇后就停下来
    for dx, dy in directions:
        x, y = kx + dx, ky + dy
        while 0 <= x < 8 and 0 <= y < 8:          # 仍在棋盘范围内
            if (x, y) in queen_set:               # 发现皇后
                ans.append([x, y])                # 记录它
                break                             # 该方向只需要最近的皇后
            x += dx
            y += dy

    return ans
```
- **关键行解释**  
  - `queen_set = {tuple(q) for q in queens}`：把列表转成集合，查找快。  
  - `directions`：把八个可能的进攻方向写成向量，后面遍历时只要把坐标加上向量就能一步步前进。  
  - `while 0 <= x < 8 ...`：保证不跑出 8×8 棋盘。  
  - `if (x, y) in queen_set`：一旦碰到皇后，就把它加入答案并停止该方向的搜索，因为更远的皇后一定被前面的挡住。

#### 复杂度  
- **时间复杂度**：`O(8 * 8) = O(1)`  
  - 虽然外层遍历 8 条方向，内层最多走满整条线（最多 7 步），常数很小，整体是常数时间。  
  - 对于一般的 `n × n` 棋盘，这里会是 `O(8·n) = O(n)`，因为每条方向最多走 `n` 步。  
- **空间复杂度**：`O(Q)`（`Q` 为皇后数量）  
  - 只额外用了一个集合来存皇后坐标，最坏情况是棋盘上放满 63 只皇后，仍然是线性空间。

---

### 2. 最优解  

#### 思路  
从暴力解可以看到，真正的瓶颈并不是遍历所有皇后，而是**对每个方向都要一步一步检查**。由于棋盘只有 8×8，实际运行时间已经很快，但我们仍可以把思路抽象成“**一次遍历找到每个方向最近的皇后**”，这也是官方推荐的最简洁做法。

- **核心技巧**：**一次遍历所有皇后，直接判断它在八个方向中的哪一个（如果有的话），并记录该方向上距离国王最近的皇后**。  
- **为什么更好**：  
  - 只需要 **O(Q)** 次遍历（`Q` 为皇后数量），不需要再在棋盘上走格子。  
  - 只使用常数个变量保存最近皇后的位置，空间开销更小（`O(1)`）。  
- **实现细节**：  
  1. 计算皇后相对于国王的行列差 `dx = qx - kx`、`dy = qy - ky`。  
  2. 根据 `dx, dy` 判断皇后是否在同一行、同一列或同一对角线上。  
  3. 对于符合条件的皇后，计算它到国王的曼哈顿距离（行列差的绝对值），若比当前记录的更近，就更新。  
  4. 最后把八个方向上最近的皇后收集起来返回。  

> **类比**：想象你在城市的十字路口（国王所在），四周有很多餐馆（皇后）。你想知道每个方向最近的那家餐馆，最直接的办法是把所有餐馆的坐标一次性拿出来比较，而不是沿着每条街道一个街区一个街区地走。

#### 代码（Python）  
```python
from typing import List

def queensAttacktheKing_optimal(queens: List[List[int]], king: List[int]) -> List[List[int]]:
    kx, ky = king

    # 用 8 个变量分别保存 8 个方向最近皇后的坐标和距离
    # 初始化为 None 表示该方向暂时没有皇后
    dirs = {
        "up":        None,   # dx < 0, dy == 0
        "down":      None,   # dx > 0, dy == 0
        "left":      None,   # dx == 0, dy < 0
        "right":     None,   # dx == 0, dy > 0
        "up_left":   None,   # dx < 0, dy < 0, |dx| == |dy|
        "up_right":  None,   # dx < 0, dy > 0, |dx| == |dy|
        "down_left": None,   # dx > 0, dy < 0, |dx| == |dy|
        "down_right":None    # dx > 0, dy > 0, |dx| == |dy|
    }

    # 辅助函数：更新方向对应的最近皇后
    def update(dir_key: str, qx: int, qy: int, dist: int) -> None:
        cur = dirs[dir_key]
        if cur is None or dist < cur[2]:          # cur[2] 保存当前最近皇后的距离
            dirs[dir_key] = (qx, qy, dist)

    for qx, qy in queens:
        dx, dy = qx - kx, qy - ky

        # 同一列
        if dy == 0:
            if dx < 0:
                update("up", qx, qy, -dx)         # 距离用正数表示
            else:
                update("down", qx, qy, dx)

        # 同一行
        elif dx == 0:
            if dy < 0:
                update("left", qx, qy, -dy)
            else:
                update("right", qx, qy, dy)

        # 对角线：行列差绝对值相等
        elif abs(dx) == abs(dy):
            if dx < 0 and dy < 0:
                update("up_left", qx, qy, -dx)
            elif dx < 0 and dy > 0:
                update("up_right", qx, qy, -dx)
            elif dx > 0 and dy < 0:
                update("down_left", qx, qy, dx)
            else:  # dx > 0 and dy > 0
                update("down_right", qx, qy, dx)

    # 把每个方向上非空的皇后坐标提取出来
    result = []
    for info in dirs.values():
        if info is not None:
            result.append([info[0], info[1]])

    return result
```
- **关键行解释**  
  - `dx, dy = qx - kx, qy - ky`：得到皇后相对于国王的位移向量。  
  - `if dy == 0` / `elif dx == 0`：判断是否在同一直线（列/行）。  
  - `elif abs(dx) == abs(dy)`: 判断是否在同一条斜线（对角线），因为斜线的行列差的绝对值相等。  
  - `update(...)`：只保留**最近**的皇后，`dist` 使用正数，越小代表越近。  
  - 最后把 `dirs` 中非 `None` 的坐标收集成答案。

#### 复杂度  
- **时间复杂度**：`O(Q)`  
  - 只遍历一次所有皇后（最多 63），每只皇后只做常数次比较和赋值。  
  - 与暴力解相比，省掉了在棋盘上逐格前进的循环，理论上更快。  
- **空间复杂度**：`O(1)`  
  - 只用了 8 个变量（即 8 条方向的最近皇后信息），不随 `Q` 增长而增长。

---

## 心得  

- **核心技巧**：**一次遍历 + 方向分类**，找出每个方向最近的目标。  
- **适用题型**：  
  1. “在二维平面上，找离某点最近的点”——如 LeetCode 1992 *Find All Groups of Farmland*（方向遍历）  
  2. “棋子攻击范围”——如 LeetCode 1192 *Critical Connections in a Network*（其实是图），或 1066 *Campus Bikes*（最近点）  
  3. “八皇后”类的冲突检测问题（方向判断 + 最近冲突）。  
- **一句话总结**：**把所有候选对象一次性分类到 8 条方向，然后只保留每条方向上最近的一个，即可得到所有能直接攻击国王的皇后。**

---

## 反思  

- **第一反应**：看到“8×8 棋盘”和“皇后”，立刻想到在八个方向上搜索最近的皇后。  
- **最容易踩的坑**：  
  - 忘记 **同一格子上只能有一个棋子**，导致在遍历时把国王自己算进了皇后集合。  
  - 对角线的判断写成 `dx == dy`，而忘记取绝对值，导致只能识别左上‑右下方向。  
  - 更新最近皇后时忘记比较距离，导致把更远的皇后覆盖了更近的。  
- **下次遇到同类题**：第一步先 **确定“方向”或“直线”**（行、列、对角），然后 **一次遍历所有对象**，在每个方向上维护“最近的”记录。这样既省时又不易出错。