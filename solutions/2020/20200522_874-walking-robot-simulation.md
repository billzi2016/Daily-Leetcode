# #874. 行走机器人模拟 / Walking Robot Simulation

> 难度：中等 · 标签：Array、Hash Table、Simulation · [LeetCode 链接](https://leetcode.com/problems/walking-robot-simulation/)

---

## 题目（英文原版）

**Description**

A robot on an infinite XY-plane starts at point (0, 0) facing north. The robot receives an array of integers commands, which represents a sequence of moves that it needs to execute. There are only three possible types of instructions the robot can receive:
Some of the grid squares are obstacles. The ith obstacle is at grid point obstacles[i] = (xi, yi). If the robot runs into an obstacle, it will stay in its current location (on the block adjacent to the obstacle) and move onto the next command.
Return the maximum squared Euclidean distance that the robot reaches at any point in its path (i.e. if the distance is 5, return 25).
Note:

**Examples**

**Example 1:**

```
Input: commands = [4,-1,3], obstacles = []
Output: 25
Explanation:
The robot starts at (0, 0) :
The furthest point the robot ever gets from the origin is (3, 4) , which squared is 3 2 + 4 2 = 25 units away.
```

**Example 2:**

```
Input: commands = [4,-1,4,-2,4], obstacles = [[2,4]]
Output: 65
Explanation:
The robot starts at (0, 0) :
The furthest point the robot ever gets from the origin is (1, 8) , which squared is 1 2 + 8 2 = 65 units away.
```

**Example 3:**

```
Input: commands = [6,-1,-1,6], obstacles = [[0,0]]
Output: 36
Explanation:
The robot starts at (0, 0) :
The furthest point the robot ever gets from the origin is (0, 6) , which squared is 6 2 = 36 units away.
```

**Constraints**

- 1 <= commands.length <= 104
- commands[i] is either -2, -1, or an integer in the range [1, 9].
- 0 <= obstacles.length <= 104
- -3 * 104 <= xi, yi <= 3 * 104
- The answer is guaranteed to be less than 231.

---

## 题目（中文翻译）

机器人位于无限大的 XY 平面上，初始坐标为 (0, 0)，面向北方。机器人会收到一个整数数组 `commands`，该数组表示机器人需要依次执行的指令。机器人只能收到以下三种指令：

- `-2`：向左转 90°（逆时针）。
- `-1`：向右转 90°（顺时针）。
- 正整数 `k`（1 ≤ k ≤ 9）：向当前方向前进 `k` 步，每步移动一个单位长度。

平面上有若干障碍物（obstacle）。第 `i` 个障碍物位于网格点 `obstacles[i] = (xi, yi)`。如果机器人前进时碰到障碍物，它会停留在障碍物相邻的格子中，不会进入障碍物所在的格子，然后继续执行下一条指令。

返回机器人在整个运动过程中距离原点的最大 **平方欧氏距离**（squared Euclidean distance），即如果最大距离为 5，则返回 25。

**示例**  

**示例 1**  
Input: `commands = [4,-1,3]`, `obstacles = []`  
Output: `25`  
Explanation:  
机器人从 (0, 0) 开始，按照指令依次前进。它离原点最远的点是 (3, 4)，其平方距离为 3² + 4² = 25。

**示例 2**  
Input: `commands = [4,-1,4,-2,4]`, `obstacles = [[2,4]]`  
Output: `65`  
Explanation:  
机器人从 (0, 0) 开始，途中会因障碍物 (2, 4) 而改变路径。它离原点最远的点是 (1, 8)，其平方距离为 1² + 8² = 65。

**示例 3**  
Input: `commands = [6,-1,-1,6]`, `obstacles = [[0,0]]`  
Output: `36`  
Explanation:  
机器人从 (0, 0) 开始，虽然起点被障碍物占据，但它仍然可以向北前进。它离原点最远的点是 (0, 6)，其平方距离为 6² = 36。

**约束条件**  
- 1 ≤ `commands.length` ≤ 10⁴  
- `commands[i]` 只能是 -2、-1，或范围在 [1, 9] 的整数  
- 0 ≤ `obstacles.length` ≤ 10⁴  
- -3 × 10⁴ ≤ `xi`, `yi` ≤ 3 × 10⁴  
- 答案保证小于 2³¹。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

我们把机器人当成一个在无限棋盘上走的“小人”。  
- **位置** 用 `(x, y)` 两个整数表示，起点是 `(0, 0)`。  
- **朝向** 有四种可能：北、东、南、西，分别记作 `0, 1, 2, 3`（顺时针）。  
- **指令** 有三类  
  - 正整数 `k`（`1~9`）：向当前朝向前进 `k` 步。  
  - `-1`：向右转 90°（朝向 +1）。  
  - `-2`：向左转 90°（朝向 -1）。  

最直接的想法是**一步一步模拟**机器人的行动：  
1. 读取一条指令。  
2. 如果是转向指令，直接改朝向。  
3. 如果是前进指令，就循环 `k` 次，每次把 `(x, y)` 按当前朝向加一格。  
4. 移动前要检查**下一个格子**是否是障碍物。如果是障碍，**停在当前格子**，直接结束这条前进指令，继续处理后面的指令。  
5. 每走到一个新格子，就用欧氏距离的平方 `x*x + y*y` 更新“最远距离”。  

> **数据结构**：障碍物集合可以直接用 **列表** 保存。判断一个格子是否是障碍时，用 `if (nx, ny) in obstacles:` 线性遍历整个列表。  
> 类比：列表就像一本**电话簿**，要找某个人的电话号码，需要从头到尾翻阅，最坏情况下要看完整本电话簿。

**为什么正确**：我们严格按照题目给出的规则执行每一步，且每次都记录当前位置到原点的距离。遍历完所有指令后，记录的最大值就是答案。

#### 代码（Python）  

```python
from typing import List

def robotSim_bruteforce(commands: List[int], obstacles: List[List[int]]) -> int:
    # 方向向量，顺序为北、东、南、西
    # 北 → y+1，东 → x+1，南 → y-1，西 → x-1
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    dir_idx = 0                     # 初始朝向是北
    x = y = 0                       # 起点坐标
    max_dist2 = 0                   # 记录最大距离的平方

    # 暴力检查障碍：遍历整个列表
    def is_obstacle(nx: int, ny: int) -> bool:
        for ox, oy in obstacles:    # O(len(obstacles)) 的线性查找
            if ox == nx and oy == ny:
                return True
        return False

    for cmd in commands:
        if cmd == -1:               # 向右转
            dir_idx = (dir_idx + 1) % 4
        elif cmd == -2:             # 向左转
            dir_idx = (dir_idx - 1) % 4
        else:                       # 前进 cmd 步
            dx, dy = dirs[dir_idx]
            for _ in range(cmd):
                nx, ny = x + dx, y + dy
                if is_obstacle(nx, ny):   # 碰到障碍就停下来
                    break
                x, y = nx, ny
                max_dist2 = max(max_dist2, x * x + y * y)

    return max_dist2
```

#### 复杂度  

- **时间复杂度**：`O(C * S * O)`  
  - `C = len(commands)`（指令条数），  
  - `S` 为单条前进指令的最大步数（题目限定在 `1~9`，所以 `S ≤ 9`），  
  - `O = len(obstacles)`（障碍物数量）。  
  也就是说，每走一步都要在障碍列表里**顺序查找**一次，最坏情况下会遍历完整个列表。  
  用大白话说，就是“**指令数 × 每步查表的时间**”。在最坏的 10⁴ 条指令、10⁴ 个障碍时，时间会达到 10⁸ 级别，可能会超时。

- **空间复杂度**：`O(1)`（不计输入本身）。只用了常数个变量来保存位置、方向和最大距离。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈**在于判断一个格子是否是障碍时的线性搜索。  
如果我们能够**在 O(1) 时间内判断**“某个坐标是否在障碍集合里”，整体复杂度就会大幅下降。

**哈希表（集合）** 正好可以做到这一点。  
- 把每个障碍坐标 `(x, y)` 组成一个 **元组**，存入 Python 的 `set`。  
- 判断 `(nx, ny) in obstacle_set` 的时间复杂度是 **均摊 O(1)**，因为底层是哈希查找。  
- 类比：集合就像一本**字典**，每个单词都有对应的页码，直接翻到对应的页码即可，无需从头查找。

其余的模拟过程与暴力解完全相同，只是把 `is_obstacle` 换成一次哈希查询。

**完整步骤**  
1. 把 `obstacles` 转成 `set`，每个元素是 `(x, y)`。  
2. 用同样的四个方向向量 `dirs` 和一个方向索引 `dir_idx` 表示当前朝向。  
3. 依次处理指令：  
   - `-1` / `-2` 调整 `dir_idx`。  
   - 正整数 `k`，循环 `k` 步：  
     - 计算下一个坐标 `nx, ny`。  
     - 若 ` (nx, ny) ` 在 `obstacle_set` 中，则**本条指令终止**，直接进入下一条指令。  
     - 否则更新当前位置 `(x, y)`，并更新最大距离的平方。  
4. 所有指令执行完后，返回记录的最大距离平方。

**为什么最优**：  
- 每一步的障碍检查只需要一次哈希查找，时间是常数。  
- 机器人最多走 `commands.length * 9` 步（因为每条前进指令最多 9 步），所以总时间是 `O(C * 9)`，即 `O(C)`。  
- 额外使用的哈希集合占用 `O(O)` 空间，和障碍数量成正比。

#### 代码（Python）  

```python
from typing import List

def robotSim(commands: List[int], obstacles: List[List[int]]) -> int:
    # 1. 把障碍点放进集合，哈希查询 O(1)
    obstacle_set = {(ox, oy) for ox, oy in obstacles}

    # 2. 方向向量：北、东、南、西（顺时针）
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    dir_idx = 0                     # 初始朝向向北
    x = y = 0                       # 起点坐标
    max_dist2 = 0                   # 记录最大距离的平方

    for cmd in commands:
        if cmd == -1:               # 向右转 90°
            dir_idx = (dir_idx + 1) % 4
        elif cmd == -2:             # 向左转 90°
            dir_idx = (dir_idx - 1) % 4
        else:                       # 前进 cmd 步
            dx, dy = dirs[dir_idx]
            for _ in range(cmd):
                nx, ny = x + dx, y + dy
                # 直接用集合判断是否是障碍
                if (nx, ny) in obstacle_set:
                    # 碰到障碍，停止当前指令的前进
                    break
                x, y = nx, ny
                # 更新最大距离（欧氏距离的平方）
                max_dist2 = max(max_dist2, x * x + y * y)

    return max_dist2
```

#### 复杂度  

- **时间复杂度**：`O(C * 9) = O(C)`  
  - `C = len(commands)`（最多 10⁴），每步只做一次哈希查找，常数时间。  
  - 用大白话说，就是“**指令数乘以一个很小的常数**”。相比暴力解的 `O(C * O)`，快了好几倍。

- **空间复杂度**：`O(O)`  
  - 需要存储所有障碍点的哈希集合，和障碍数量成正比。  
  - 这里的 “O” 代表障碍的数量（最多 10⁴），相当于一本字典的大小。

---

## 心得  

- **核心技巧**：使用哈希集合（`set`）实现 **O(1) 坐标查询**，把原本的线性搜索转化为常数时间查找。  
- **适用场景**  
  1. “判断某个元素是否出现过” 的**快速查重**（如 LeetCode 217. Contains Duplicate）。  
  2. “二维平面上是否有障碍/点” 的**空间定位**（如 3. Longest Substring Without Repeating Characters 的字符集合）。  
  3. “坐标去重/去冲突” 的**网格游戏**（如 212. Word Search II 中的前缀树+哈希剪枝）。  
- **一句话总结**：**把障碍点装进字典（哈希表），查询障碍就像查单词——一眼就能找到**。

---

## 反思  

- **第一反应**：看到机器人、指令、障碍，立刻想到**一步一步模拟**。  
- **最容易踩的坑**  
  1. **转向的方向顺序**：要记清楚左转是 `-1`，右转是 `+1`，以及对应的模 4 运算。  
  2. **障碍判断的坐标**：必须在**尝试移动之前**检查下一个格子，而不是移动后再判断。否则会把机器人“卡在”障碍里。  
  3. **负坐标的哈希**：Python 的元组可以直接哈希，别忘了把 `(-1, -2)` 也放进集合。  
- **下次思路**：看到“判断坐标是否在集合里”时，第一步就想到**哈希集合**，把障碍预处理成 `set`，避免每步线性遍历。这样可以把时间复杂度直接降到 **线性**。