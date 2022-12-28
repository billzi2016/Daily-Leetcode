# #2069. **行走机器人模拟 II** / Walking Robot Simulation II

> 难度：中等 · 标签：Design、Simulation · [LeetCode 链接](https://leetcode.com/problems/walking-robot-simulation-ii/)

---

## 题目（英文原版）

**Description**

A width x height grid is on an XY-plane with the bottom-left cell at (0, 0) and the top-right cell at (width - 1, height - 1). The grid is aligned with the four cardinal directions ("North", "East", "South", and "West"). A robot is initially at cell (0, 0) facing direction "East".
The robot can be instructed to move for a specific number of steps. For each step, it does the following.
After the robot finishes moving the number of steps required, it stops and awaits the next instruction.
Implement the Robot class:

**Examples**

**Example 1:**

```
Input
["Robot", "step", "step", "getPos", "getDir", "step", "step", "step", "getPos", "getDir"]
[[6, 3], [2], [2], [], [], [2], [1], [4], [], []]
Output
[null, null, null, [4, 0], "East", null, null, null, [1, 2], "West"]

Explanation
Robot robot = new Robot(6, 3); // Initialize the grid and the robot at (0, 0) facing East.
robot.step(2);  // It moves two steps East to (2, 0), and faces East.
robot.step(2);  // It moves two steps East to (4, 0), and faces East.
robot.getPos(); // return [4, 0]
robot.getDir(); // return "East"
robot.step(2);  // It moves one step East to (5, 0), and faces East.
                // Moving the next step East would be out of bounds, so it turns and faces North.
                // Then, it moves one step North to (5, 1), and faces North.
robot.step(1);  // It moves one step North to (5, 2), and faces North (not West).
robot.step(4);  // Moving the next step North would be out of bounds, so it turns and faces West.
                // Then, it moves four steps West to (1, 2), and faces West.
robot.getPos(); // return [1, 2]
robot.getDir(); // return "West"
```

**Constraints**

- 2 <= width, height <= 100
- 1 <= num <= 105
- At most 104 calls in total will be made to step, getPos, and getDir.

---

## 题目（中文翻译）

一个宽度为 `width`、高度为 `height` 的网格位于 XY 平面上，左下角的单元格坐标为 `(0, 0)`，右上角的单元格坐标为 `(width - 1, height - 1)`。网格的四个方向分别对应四个基准方向（“North”、 “East”、 “South”、 “West”）。机器人最初位于单元格 `(0, 0)`，面向方向 “East”。  

机器人可以接受指令，让它移动指定的步数。每一步的执行过程如下：

1. 若机器人向当前面朝方向前进一步仍然在网格内部，则完成该步并保持原方向。  
2. 若前进一步会超出网格边界，则机器人顺时针旋转 90 度（即 “East” → “South” → “West” → “North” → “East”），并尝试在新的方向上前进一步。若仍然越界，则继续顺时针旋转，直至找到一个合法的方向后再前进。  
3. 完成一步后，机器人保持此时的方向，继续执行剩余的步数。

当机器人完成指令要求的全部步数后，它会停止并等待下一条指令。

请实现 `Robot` 类，支持以下方法：

* `Robot(int width, int height)`  
  初始化网格尺寸以及机器人位置（`(0, 0)`）和方向（`"East"`）。

* `void step(int num)`  
  让机器人按照上述规则前进 `num` 步。

* `int[] getPos()`  
  返回机器人当前所在单元格的坐标 `[x, y]`。

* `String getDir()`  
  返回机器人当前面朝的方向，可能的取值为 `"North"`、`"East"`、`"South"`、`"West"`。

---

### 示例

**示例 1：**

```text
Input
["Robot", "step", "step", "getPos", "getDir", "step", "step", "step", "getPos", "getDir"]
[[6, 3], [2], [2], [], [], [2], [1], [4], [], []]

Output
[null, null, null, [4, 0], "East", null, null, null, [1, 2], "West"]
```

**解释**
```java
Robot robot = new Robot(6, 3); // 初始化网格，机器人位于 (0, 0)，面向 East。
robot.step(2);  // 向东移动两步，来到 (2, 0)，仍面向 East。
robot.step(2);  // 再向东移动两步，来到 (4, 0)，仍面向 East。
robot.getPos(); // 返回 [4, 0]。
robot.getDir(); // 返回 "East"。
robot.step(2);  // 第一步到达 (5, 0)；第二步若继续向东会越界，机器人顺时针转向 South 并移动到 (5, 1)。
robot.step(1);  // 向 South 再移动一步，来到 (5, 2)，仍面向 South。
robot.step(4);  // 第一步若继续向 South 会越界，机器人顺时针转向 West 并移动到 (4, 2)；随后向 West 连续移动三步，最终位于 (1, 2)，面向 West。
robot.getPos(); // 返回 [1, 2]。
robot.getDir(); // 返回 "West"。
```

---

### 约束条件

* `2 <= width, height <= 100`
* `1 <= num <= 10^5`
* 对 `step`、`getPos`、`getDir` 的调用总次数不超过 `10^4`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把机器人每走一步都写进代码里：

1. **记录当前位置** `(x, y)` 与**朝向** `dir`（East、South、West、North）。  
2. `step(num)` 时，循环 `num` 次：
   - 先算出往前一步的坐标 `(nx, ny)`（比如向 East 就是 `(x+1, y)`）。  
   - 检查 `(nx, ny)` 是否还在 `0 ≤ nx < width`、`0 ≤ ny < height` 的矩形里。  
   - **如果在**，直接把 `(x, y) ← (nx, ny)`。  
   - **如果不在**，说明机器人要“撞墙”，按照题意**向右转 90°**（顺时针），然后再按照新方向走一步（这一步一定在格子里，因为机器人只会在四条边上转弯）。

这个思路和我们日常生活中“走迷宫”时的做法一模一样：一步一步检查前方是否可走，不行就右转再继续。

> **类比**：  
> - **哈希表**好比一本“词典”，`key`是单词，`value`是页码。  
> - **这里的坐标** `(x, y)` 就是机器人在“地图”上的位置，`dir` 就是它手里的一把“指南针”。每走一步都要拿指南针指的方向去查询下一格是否在地图范围内。

**正确性**：  
- 每一次循环都严格遵守题目描述的“先尝试前进，若出界则右转再前进”。  
- 循环 `num` 次恰好模拟了机器人走 `num` 步的全部过程，因而最终位置与方向必然与题目要求一致。

#### 代码（Python）

```python
class Robot:
    # 四个方向顺时针排列，方便右转时取下一个
    DIRS = ["East", "South", "West", "North"]
    # 对应的坐标增量 (dx, dy)
    VEC = {"East": (1, 0), "South": (0, -1), "West": (-1, 0), "North": (0, 1)}

    def __init__(self, width: int, height: int):
        self.w, self.h = width, height          # 网格大小
        self.x, self.y = 0, 0                    # 起点 (0,0)
        self.dir_idx = 0                         # 0 对应 East

    def step(self, num: int) -> None:
        """一次走 num 步，逐步模拟"""
        for _ in range(num):
            # 先尝试往当前方向前进一步
            dx, dy = self.VEC[self.DIRS[self.dir_idx]]
            nx, ny = self.x + dx, self.y + dy
            # 若超出边界，则右转（顺时针）再重新计算前进方向
            if not (0 <= nx < self.w and 0 <= ny < self.h):
                self.dir_idx = (self.dir_idx + 1) % 4   # 右转 90°
                dx, dy = self.VEC[self.DIRS[self.dir_idx]]
                nx, ny = self.x + dx, self.y + dy
            # 更新位置
            self.x, self.y = nx, ny

    def getPos(self) -> list[int]:
        """返回当前坐标"""
        return [self.x, self.y]

    def getDir(self) -> str:
        """返回当前朝向文字描述"""
        return self.DIRS[self.dir_idx]
```

> 关键行中文注释已经写在代码里，直接复制运行即可。

#### 复杂度

- **时间复杂度**：`O(num)`。每走一步都要循环一次。如果一次指令要求走 `10⁵` 步，循环 `10⁵` 次就能完成。  
  > 大白话：如果把“一步”看成“一块砖”，那么时间就是“搬多少块砖”。搬得越多，时间越长。

- **空间复杂度**：`O(1)`。只用了几个整数记录位置、方向和网格大小，和输入规模无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **逐步循环**——当 `num` 很大（最高 `10⁵`）且调用次数多（最多 `10⁴`）时，整体运行时间会达到 `10⁹` 步，远远超出 1 秒的限制。

观察题目可以发现：

1. **机器人永远在矩形的四条边上运动**，从左下角顺时针跑一圈后又回到起点。  
2. 这条“边缘路径”是一个**闭环**，长度为  

   \[
   L = 2 \times (width + height) - 4
   \]

   （四条边的格子数相加，四个角只算一次）。  

3. 把每个边缘格子按照顺时针顺序编号 `0 … L‑1`，则机器人每走一步相当于**编号 +1（模 L）**。  
4. **方向只和格子编号有关**：  
   - 编号在 `0 … width‑2` → 在底边，面向 East  
   - 编号在 `width‑1 … width+height‑3` → 右边，面向 North  
   - 编号在 `width+height‑2 … 2*width+height‑4` → 顶边，面向 West  
   - 其余 → 左边，面向 South  

   换句话说，只要知道当前的编号，就能 **直接算出坐标和朝向**，不需要一步步模拟。

**优化步骤**：

- **预处理**：在构造函数里计算 `L`，并把“编号 → (x, y, dir)” 的映射保存到三个列表 `pos_x`, `pos_y`, `pos_dir` 中。因为 `width, height ≤ 100`，`L ≤ 2*(100+100)-4 = 396`，空间几乎可以忽略不计。  
- **一步到位**：`step(num)` 时，只需要把当前编号 `idx` 加上 `num` 再对 `L` 取模，得到新的 `idx`。随后直接从预处理好的数组里取出对应的坐标和方向。  

这样每一次 `step` 的时间都降到了 **O(1)**，不随 `num` 大小变化。

> **类比**：  
> 想象一条跑道（周长 L）上有若干个标记点，机器人每跑一步就从一个标记跳到下一个。我们不需要记录每一步的脚印，只要记住它现在站在哪个标记上，下一次跑 `k` 步后，它会直接跳到 “当前标记 + k（取模）” 处。

#### 代码（Python）

```python
class Robot:
    # 四个方向顺时针顺序
    DIRS = ["East", "South", "West", "North"]

    def __init__(self, width: int, height: int):
        self.w, self.h = width, height
        # 周长（仅在边缘的格子数）
        self.L = 2 * (width + height) - 4

        # 预计算：编号 → 坐标、方向
        self.pos_x = [0] * self.L
        self.pos_y = [0] * self.L
        self.pos_dir = [0] * self.L          # 用方向下标表示

        idx = 0
        # ---------- 底边，朝 East ----------
        for x in range(width - 1):           # (0,0) … (width-2,0)
            self.pos_x[idx] = x
            self.pos_y[idx] = 0
            self.pos_dir[idx] = 0            # East
            idx += 1

        # ---------- 右边，朝 North ----------
        for y in range(height - 1):          # (width-1,0) … (width-1,height-2)
            self.pos_x[idx] = width - 1
            self.pos_y[idx] = y
            self.pos_dir[idx] = 1            # North
            idx += 1

        # ---------- 顶边，朝 West ----------
        for x in range(width - 1, 0, -1):    # (width-1,height-1) … (1,height-1)
            self.pos_x[idx] = x
            self.pos_y[idx] = height - 1
            self.pos_dir[idx] = 2            # West
            idx += 1

        # ---------- 左边，朝 South ----------
        for y in range(height - 1, 0, -1):   # (0,height-1) … (0,1)
            self.pos_x[idx] = 0
            self.pos_y[idx] = y
            self.pos_dir[idx] = 3            # South
            idx += 1

        # 初始位置对应的编号是 0
        self.idx = 0

    def step(self, num: int) -> None:
        """一次性跳 num 步，只需要 O(1) 时间"""
        self.idx = (self.idx + num) % self.L   # 环形前进
        # 位置和方向已经在预处理表里，无需额外计算

    def getPos(self) -> list[int]:
        """直接返回预处理好的坐标"""
        return [self.pos_x[self.idx], self.pos_y[self.idx]]

    def getDir(self) -> str:
        """根据编号取方向下标，再映射成文字"""
        return self.DIRS[self.pos_dir[self.idx]]
```

**代码要点解释**：

- `self.L` 为**周长**，相当于跑道的总格子数。  
- 四段 `for` 循环分别遍历 **底、右、顶、左** 四条边，按照顺时针顺序填充 `pos_x / pos_y / pos_dir`。  
- `self.idx` 保存机器人当前在跑道上的**编号**，`step` 只做一次模运算。  
- `getPos / getDir` 直接从数组取值，时间为常数。

#### 复杂度

- **时间复杂度**：`O(1)`（常数）  
  - `step` 只做一次加法和一次取模。  
  - `getPos`、`getDir` 只做数组索引。  
  > 与暴力解相比，**不再随 `num` 的大小增长**，即使 `num = 10⁵` 也只花常数时间。

- **空间复杂度**：`O(L) = O(width + height)`  
  - 需要保存周长上每个格子的坐标和方向。  
  - 由于 `width, height ≤ 100`，最多只有约 400 条记录，几乎可以忽略不计。  

---

## 心得

- **核心技巧**：把机器人在矩形边缘的运动抽象为 **环形（循环）编号**，利用**模运算**一次性跳过大量步骤。  
- **适用的题型**  
  1. “在环形路径上移动”类题目，如 **Walking Robot Simulation I**、**Design Circular Queue**。  
  2. “在圆形或周期性序列上跳跃”类题目，如 **Elimination Game**、**Find the Winner of the Circular Game**。  
- **一句话总结**：把“一步一步走”转化为“在编号环上直接跳”，用模运算一次算到终点。

## 反思

- **第一反应**：直接写循环模拟每一步，感觉最直观。  
- **最容易踩的坑**  
  - **忘记去掉四个角的重复计数**，导致周长 `L` 计算错误（会多算 4 格）。  
  - **方向映射错误**：左边应该是 South，右边是 North，容易把顺时针顺序写成逆时针。  
  - **取模时使用负数**：如果 `num` 可能为负（本题不会），需要先把 `num % L` 调整到正数区间。  
- **下次类似题的第一步**：先检查**运动是否在一个固定的环/周期**上，尝试把位置映射到**编号**，看能否用**模运算**一次性完成移动。这样往往能把线性时间降到常数时间。