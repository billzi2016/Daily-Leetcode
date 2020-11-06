# #1041. 机器人在圆内受限 / Robot Bounded In Circle

> 难度：中等 · 标签：Math、String、Simulation · [LeetCode 链接](https://leetcode.com/problems/robot-bounded-in-circle/)

---

## 题目（英文原版）

**Description**

On an infinite plane, a robot initially stands at (0, 0) and faces north. Note that:
The robot can receive one of three instructions:
The robot performs the instructions given in order, and repeats them forever.
Return true if and only if there exists a circle in the plane such that the robot never leaves the circle.

**Examples**

**Example 1:**

```
Input: instructions = "GGLLGG"
Output: true
Explanation: The robot is initially at (0, 0) facing the north direction.
"G": move one step. Position: (0, 1). Direction: North.
"G": move one step. Position: (0, 2). Direction: North.
"L": turn 90 degrees anti-clockwise. Position: (0, 2). Direction: West.
"L": turn 90 degrees anti-clockwise. Position: (0, 2). Direction: South.
"G": move one step. Position: (0, 1). Direction: South.
"G": move one step. Position: (0, 0). Direction: South.
Repeating the instructions, the robot goes into the cycle: (0, 0) --> (0, 1) --> (0, 2) --> (0, 1) --> (0, 0).
Based on that, we return true.
```

**Example 2:**

```
Input: instructions = "GG"
Output: false
Explanation: The robot is initially at (0, 0) facing the north direction.
"G": move one step. Position: (0, 1). Direction: North.
"G": move one step. Position: (0, 2). Direction: North.
Repeating the instructions, keeps advancing in the north direction and does not go into cycles.
Based on that, we return false.
```

**Example 3:**

```
Input: instructions = "GL"
Output: true
Explanation: The robot is initially at (0, 0) facing the north direction.
"G": move one step. Position: (0, 1). Direction: North.
"L": turn 90 degrees anti-clockwise. Position: (0, 1). Direction: West.
"G": move one step. Position: (-1, 1). Direction: West.
"L": turn 90 degrees anti-clockwise. Position: (-1, 1). Direction: South.
"G": move one step. Position: (-1, 0). Direction: South.
"L": turn 90 degrees anti-clockwise. Position: (-1, 0). Direction: East.
"G": move one step. Position: (0, 0). Direction: East.
"L": turn 90 degrees anti-clockwise. Position: (0, 0). Direction: North.
Repeating the instructions, the robot goes into the cycle: (0, 0) --> (0, 1) --> (-1, 1) --> (-1, 0) --> (0, 0).
Based on that, we return true.
```

**Constraints**

- 1 <= instructions.length <= 100
- instructions[i] is 'G', 'L' or, 'R'.

---

## 题目（中文翻译）

**描述**  
在一个无限平面（infinite plane）上，机器人最初位于坐标 (0, 0)，面向北方。注意：

- 机器人可以收到三种指令之一：  
  - **G**：向当前方向前进一单位。  
  - **L**：逆时针（anti‑clockwise）旋转 90 度。  
  - **R**：顺时针（clockwise）旋转 90 度。  

机器人按指令顺序执行，并无限次重复执行这些指令。  
如果存在一个平面上的圆（circle），使得机器人永远不会离开该圆，则返回 `true`；否则返回 `false`。

**示例 1**  
**输入**: `instructions = "GGLLGG"`  
**输出**: `true`  
**解释**:  
机器人最初位于 (0, 0)，面向北方。  
- **G**: 前进一步。位置: (0, 1)。方向: 北。  
- **G**: 前进一步。位置: (0, 2)。方向: 北。  
- **L**: 逆时针旋转 90 度。位置: (0, 2)。方向: 西。  
- **L**: 逆时针旋转 90 度。位置: (0, 2)。方向: 南。  
- **G**: 前进一步。位置: (0, 1)。方向: 南。  
- **G**: 前进一步。位置: (0, 0)。方向: 南。  

重复指令后，机器人进入循环路径: (0, 0) → (0, 1) → (0, 2) → (0, 1) → (0, 0)。  
因此返回 `true`。

**示例 2**  
**输入**: `instructions = "GG"`  
**输出**: `false`  
**解释**:  
机器人最初位于 (0, 0)，面向北方。  
- **G**: 前进一步。位置: (0, 1)。方向: 北。  
- **G**: 前进一步。位置: (0, 2)。方向: 北。  

重复指令后，机器人一直向北前进，不会形成循环。  
因此返回 `false`。

**示例 3**  
**输入**: `instructions = "GL"`  
**输出**: `true`  
**解释**:  
机器人最初位于 (0, 0)，面向北方。  
- **G**: 前进一步。位置: (0, 1)。方向: 北。  
- **L**: 逆时针旋转 90 度。位置: (0, 1)。方向: 西。  
- **G**: 前进一步。位置: (-1, 1)。方向: 西。  
- **L**: 逆时针旋转 90 度。位置: (-1, 1)。方向: 南。  
- **G**: 前进一步。位置: (-1, 0)。方向: 南。  
- **L**: 逆时针旋转 90 度。位置: (-1, 0)。方向: 东。  
- **G**: 前进一步。位置: (0, 0)。方向: 东。  
- **L**: 逆时针旋转 90 度。位置: (0, 0)。方向: 北。  

重复指令后，机器人进入循环路径: (0, 0) → (0, 1) → (-1, 1) → (-1, 0) → (0, 0)。  
因此返回 `true`。

**约束条件**  
- $1 \leq \text{instructions.length} \leq 100$  
- $\text{instructions}[i]$ 为 `'G'`、`'L'` 或 `'R'`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把指令一次又一次地“放进机器人”，看它会不会跑出一个无限大的平面。  
我们可以：

1. **模拟**机器人执行指令的过程。  
2. 把同一段指令循环若干次（比如 4 次），因为机器人每走完一遍指令后，方向只可能是 **北、东、南、西** 四个方向中的一个，最多 4 次就会回到原来的朝向。  
3. 每次循环结束后检查机器人是否回到了原点 `(0,0)`。如果在这几次循环中出现了原点，就说明它以后会在一个有限的区域里循环；否则它会一直往外跑。

> **类比**：把机器人想成一只在方格纸上走的“小蚂蚁”。我们让它跑四遍指令，就像让蚂蚁围着一个正方形走四圈，观察它是否会回到起点。

> **为什么正确**：  
> - 机器人每走完一次指令后，方向只能是四个方向之一。  
> - 如果方向仍是北，并且位置没有回到原点，那么下一遍指令会让它继续向北走，永远离开原点。  
> - 只要在四遍之内出现一次回到原点（不管方向怎样），以后每四遍的轨迹都会重复，从而被一个圆圈“套住”。

#### 代码（Python）

```python
def isRobotBounded(instructions: str) -> bool:
    # 方向向量，顺序为 北、东、南、西
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    x = y = 0          # 机器人当前位置
    d = 0              # 方向下标，0 表示北

    # 重复执行指令四次
    for _ in range(4):
        for ch in instructions:
            if ch == 'G':                     # 前进一步
                dx, dy = dirs[d]
                x += dx
                y += dy
            elif ch == 'L':                   # 左转 90°
                d = (d - 1) % 4               # (d-1) 防止负数，用模 4 保证在 0~3
            else:  # ch == 'R'                # 右转 90°
                d = (d + 1) % 4

        # 如果回到原点，直接返回 True
        if x == 0 and y == 0:
            return True

    # 四遍都没回到原点，说明永远向北直走
    return False
```

#### 复杂度

- **时间复杂度**：`O(4 * n) = O(n)`，`n` 是指令长度。  
  大白话：我们最多遍历指令四遍，每遍看一次指令，指令有多少看多少次，整体就是线性时间。
- **空间复杂度**：`O(1)`，只用了几个整数变量，和指令长度无关。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**“方向是否改变”** 是判断的关键。  
我们把一次指令执行完后的**状态**抽象为：

- **位置向量** `(dx, dy)` —— 相当于“走了多远”。  
- **朝向** `d` —— 相当于“指向哪儿”。  

观察可以得到下面的数学结论：

> **结论**：机器人在平面上是有界的（能被一个圆圈套住），当且仅当以下两种情况之一成立  
> 1. 执行完一遍指令后，它回到了原点 `(0,0)`（不管方向如何）。  
> 2. 执行完一遍指令后，它的方向 **不再是北**（即 `d != 0`），即使位置没回到原点，随后再执行几遍指令它也一定会回到原点。

**为什么**：

- 若第一次结束后已经在原点，显然以后每次循环都会从原点出发，轨迹必定在一个有限范围内。  
- 若方向改变（不再是北），那么最多 **四遍**（因为四个方向循环）就会回到原点。  
  - 设第一次结束时方向是 `d != 0`，再执行一次相同的指令，机器人会在新的方向上继续移动。四次循环后，方向会回到北，同时位置的累计向量恰好是四次旋转后的和，恰好为 `(0,0)`（可以通过向量旋转的线性代数证明）。  
- 唯一的例外是 **方向仍是北且位置不在原点**，这时机器人每遍指令都会向同一方向平移，轨迹会无限扩散，无法被任何圆圈套住。

于是我们只需要一次遍历指令，记录最终位置和方向，即可判断。

> **类比**：把机器人当成一只“走迷宫的老鼠”。只要它走完一次指令后要么回到起点，要么转了头（不再往北走），它以后每走四次就会回到起点，像在原地打转；否则它会一直往前走，像在直线跑步。

#### 代码（Python）

```python
def isRobotBounded(instructions: str) -> bool:
    # 方向顺序：北、东、南、西
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    x = y = 0          # 当前位置
    d = 0              # 当前朝向下标，0 表示北

    for ch in instructions:
        if ch == 'G':                     # 前进一步
            dx, dy = dirs[d]
            x += dx
            y += dy
        elif ch == 'L':                   # 左转
            d = (d - 1) % 4
        else:  # ch == 'R'                # 右转
            d = (d + 1) % 4

    # 只要回到原点或方向不是北，就一定会被圈住
    return (x == 0 and y == 0) or (d != 0)
```

#### 复杂度

- **时间复杂度**：`O(n)`，只遍历一次指令。  
  与暴力解相比，我们省去了 4 次循环的常数因子，真正做到“一遍到底”。  
- **空间复杂度**：`O(1)`，只用常数个变量。

---

## 心得

- **核心技巧**：**状态压缩 + 方向判断**。只需要关心“最终位置”和“最终方向”，不必模拟无限次循环。  
- **适用的题型**  
  1. 机器人/小车在平面上运动，判断是否会回到起点（如 LeetCode 1041、874）。  
  2. 方向/向量循环类问题（如判断旋转指令是否会让物体回到原位）。  
- **一句话总结**：只要一次执行后位置是原点或方向不再向北，机器人必然被一个圆圈套住。

---

## 反思

- **第一反应**：看到“无限重复”就想“一直模拟”，于是想到“跑几遍看看”。这虽然能得到答案，但不够高效。  
- **最容易踩的坑**  
  - 忽略方向的影响，只检查是否回到原点，导致对像 `"GL"` 这种最终不在原点但方向改变的情况判断错误。  
  - 边界条件：指令全是 `'L'` 或 `'R'`，此时机器人根本不移动，但方向会改变，仍然是有界的。  
- **下次思路**：看到“无限重复 + 方向/位置”时，先思考“一次执行后的状态”，判断是否存在 **不变**（如方向仍是北且位置不变） 的不动点；若不存在，则一定会在有限范围内循环。这样可以快速定位最优解的思路。