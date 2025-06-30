# #3248. 矩阵中的蛇 / Snake in Matrix

> 难度：简单 · 标签：Array、String、Simulation · [LeetCode 链接](https://leetcode.com/problems/snake-in-matrix/)

---

## 题目（英文原版）

**Description**

There is a snake in an n x n matrix grid and can move in four possible directions. Each cell in the grid is identified by the position: grid[i][j] = (i * n) + j.
The snake starts at cell 0 and follows a sequence of commands.
You are given an integer n representing the size of the grid and an array of strings commands where each command[i] is either "UP", "RIGHT", "DOWN", and "LEFT". It's guaranteed that the snake will remain within the grid boundaries throughout its movement.
Return the position of the final cell where the snake ends up after executing commands.

**Examples**

**Example 1:**

```
Input: n = 2, commands = ["RIGHT","DOWN"]
Output: 3
Explanation:
```

**Example 2:**

```
Input: n = 3, commands = ["DOWN","RIGHT","UP"]
Output: 1
Explanation:
```

**Constraints**

- 2 <= n <= 10
- 1 <= commands.length <= 100
- commands consists only of "UP", "RIGHT", "DOWN", and "LEFT".
- The input is generated such the snake will not move outside of the boundaries.

---

## 题目（中文翻译）

**描述**  
在一个 `n x n` 的矩阵网格中有一条蛇，它可以向四个方向移动：上（UP）、右（RIGHT）、下（DOWN）和左（LEFT）。网格中的每个单元格用坐标 `grid[i][j] = (i * n) + j` 标识。  
蛇从单元格 `0` 开始，并按照给定的指令序列移动。  
给定整数 `n` 表示网格的大小，以及字符串数组 `commands`，其中 `commands[i]` 为 `"UP"`、`"RIGHT"`、`"DOWN"` 或 `"LEFT"` 中的一个。题目保证蛇在整个移动过程中始终位于网格内部。  
返回执行完所有指令后蛇所在的最终单元格的编号。

**示例**

示例 1  
```
Input: n = 2, commands = ["RIGHT","DOWN"]
Output: 3
```
解释：

示例 2  
```
Input: n = 3, commands = ["DOWN","RIGHT","UP"]
Output: 1
```
解释：

**约束条件**
- `2 <= n <= 10`
- `1 <= commands.length <= 100`
- `commands` 只包含 `"UP"`、`"RIGHT"`、`"DOWN"`、`"LEFT"` 四种字符串。
- 输入保证蛇不会移出矩阵边界。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
这道题本质上让我们把一条蛇在 `n × n` 的棋盘上“走”一遍，最后问它停在哪个格子。  
最直接的想法就是**一步步模拟**蛇的移动：

1. 用两个整数 `r, c` 分别记录蛇当前所在的行、列。起点是左上角 `(0,0)`，对应格子编号 `0`。  
2. 依次读取 `commands` 中的每条指令，按照指令的方向把 `r` 或 `c` 加 1、减 1。  
   - `"UP"`  → `r -= 1`  
   - `"DOWN"` → `r += 1`  
   - `"LEFT"` → `c -= 1`  
   - `"RIGHT"`→ `c += 1`  
3. 题目保证蛇永远不会跑出边界，所以我们不必额外检查 `r,c` 是否越界。  
4. 所有指令执行完后，把行列坐标转回格子编号：`pos = r * n + c`，即返回结果。

> **类比**：把 `r`、`c` 当作在地图上“坐标”，每条指令就像是给你一张“前进一步/后退一步”的指示牌。  
> **哈希表**在这里并不需要——我们只用两个整数就能随时查到蛇所在的格子。

#### 代码（Python）

```python
def finalPosition(n: int, commands: list[str]) -> int:
    # 初始位置在左上角 (0,0)
    r, c = 0, 0

    # 用字典把指令映射到行列的增量，方便统一处理
    delta = {
        "UP":    (-1, 0),
        "DOWN":  (1, 0),
        "LEFT":  (0, -1),
        "RIGHT": (0, 1),
    }

    # 逐条执行指令
    for cmd in commands:
        dr, dc = delta[cmd]   # 取出对应的行、列变化量
        r += dr                # 行号更新
        c += dc                # 列号更新
        # 题目保证不会越界，这里就不写检查代码了

    # 行列转成唯一的格子编号 (i * n + j)
    return r * n + c
```

#### 复杂度

- **时间复杂度**：`O(m)`，其中 `m = len(commands)`。意思是“随着指令数量线性增长”，每条指令只处理一次，跟 `n`（棋盘大小）无关。  
- **空间复杂度**：`O(1)`，只用了常数个变量（`r, c, dr, dc`），不随输入规模扩大而增加。

---

### 2. 最优解

#### 思路  
对于本题，**暴力模拟已经是最优**的做法。  
唯一可以再思考的地方是：  
- 是否需要每一步都更新坐标？答案是必须的，因为每条指令都会改变行或列。  
- 是否可以一次性算出最终位置？如果把所有 `"UP"`、`"DOWN"` 的次数相加得到总的行偏移，同理列偏移，也可以得到最终坐标。  

下面给出一种 **计数式** 的实现——把所有指令先分类计数，再一次性算出行列变化。它的时间仍是 `O(m)`，但代码思路更偏向“先统计后计算”，对理解“累计偏移”很有帮助。

#### 代码（Python）

```python
def finalPosition_opt(n: int, commands: list[str]) -> int:
    # 统计每种方向出现的次数
    up = commands.count("UP")
    down = commands.count("DOWN")
    left = commands.count("LEFT")
    right = commands.count("RIGHT")

    # 行的最终偏移 = 向下的步数 - 向上的步数
    r = down - up
    # 列的最终偏移 = 向右的步数 - 向左的步数
    c = right - left

    # 题目保证不会越界，直接返回格子编号
    return r * n + c
```

> **为什么仍然是最优**：我们仍然必须遍历一次 `commands`（无论是逐条处理还是一次性计数），所以时间下界是 `Ω(m)`。这两种写法的时间都是 `O(m)`，空间都是 `O(1)`，没有更快的可能。

#### 复杂度

- **时间复杂度**：`O(m)`，因为 `list.count` 在内部仍然遍历列表，等价于一次完整遍历。  
- **空间复杂度**：`O(1)`，只用了若干整数计数器。

---

## 心得

- **核心技巧**：**坐标模拟 + 累计偏移**。把二维格子映射为 `(row, col)`，每条指令对应行列的增减。  
- **适用题型**：  
  1. **机器人在网格中移动**（如 LeetCode 874 “Walking Robot Simulation”）  
  2. **按指令控制小车/船的路径**（如 1490 “Clone Number” 的思路）  
  3. **计算最终位置的累计和问题**（如 2248 “Intersection of Multiple Arrays” 中的坐标累加）  
- **一句话总结**：**把方向指令翻译成行列增量，累加即可得到最终格子编号**。

## 反思

- **第一反应**：看到“UP、DOWN、LEFT、RIGHT”，马上想到“坐标平移”，于是写了最直接的模拟代码。  
- **最容易踩的坑**：  
  - 忘记题目保证不越界，误写了额外的边界检查导致代码更复杂。  
  - 在返回结果时直接返回 `(r, c)` 而不是 `r * n + c`，忘记了题目要求的“一维格子编号”。  
- **下次遇到同类题**：第一步先**确定坐标系统**（行列或 x、y），再**把每条指令映射为增量**，最后**累计**得到最终坐标/编号。这样思路清晰、实现不会出错。