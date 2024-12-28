# #3001. 捕获皇后所需的最少移动次数 / Minimum Moves to Capture The Queen

> 难度：中等 · 标签：Math、Enumeration · [LeetCode 链接](https://leetcode.com/problems/minimum-moves-to-capture-the-queen/)

---

## 题目（英文原版）

**Description**

There is a 1-indexed 8 x 8 chessboard containing 3 pieces.
You are given 6 integers a, b, c, d, e, and f where:
Given that you can only move the white pieces, return the minimum number of moves required to capture the black queen.
Note that:

**Examples**

**Example 1:**

```
Input: a = 1, b = 1, c = 8, d = 8, e = 2, f = 3
Output: 2
Explanation: We can capture the black queen in two moves by moving the white rook to (1, 3) then to (2, 3).
It is impossible to capture the black queen in less than two moves since it is not being attacked by any of the pieces at the beginning.
```

**Example 2:**

```
Input: a = 5, b = 3, c = 3, d = 4, e = 5, f = 2
Output: 1
Explanation: We can capture the black queen in a single move by doing one of the following: 
- Move the white rook to (5, 2).
- Move the white bishop to (5, 2).
```

**Constraints**

- 1 <= a, b, c, d, e, f <= 8
- No two pieces are on the same square.

---

## 题目（中文翻译）

**题目描述**  
在一个 1 索引的 8 × 8 棋盘（chessboard）上放置了 3 枚棋子。  
给定 6 个整数 `a, b, c, d, e, f`，它们分别表示棋子的坐标（坐标范围为 1 ≤ x, y ≤ 8），具体含义如下：

- 白车（white rook）位于 `(a, b)`  
- 黑皇后（black queen）位于 `(c, d)`  
- 白象（white bishop）位于 `(e, f)`

你只能移动白色棋子，返回捕获黑皇后所需的最少移动次数。

**说明**  
- 只能在每一步中移动白车或白象一次。  
- 捕获即将白车或白象移动到与黑皇后相同的格子。  
- 如果一开始白车或白象已经能够攻击黑皇后，则可以在一次移动内将其捕获。  

**示例**  

*示例 1*  
```
Input: a = 1, b = 1, c = 8, d = 8, e = 2, f = 3
Output: 2
Explanation: 我们可以通过两步捕获黑皇后：先将白车移动到 (1, 3)，再移动到 (2, 3)。  
由于起始时没有任何白棋攻击到黑皇后，少于两步是不可能的。
```

*示例 2*  
```
Input: a = 5, b = 3, c = 3, d = 4, e = 5, f = 2
Output: 1
Explanation: 只需一步即可捕获黑皇后，方法之一是：
- 将白车移动到 (5, 2)；
- 或者将白象移动到 (5, 2)。
```

**约束条件**  

- `1 <= a, b, c, d, e, f <= 8`
- 任意两枚棋子不会位于同一格子。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题只要求**最少的走子次数**，而且题目已经暗示答案只能是 **1 步或 2 步**。  
因此最直接的想法是：

1. **先判断能否一步吃掉黑后**。  
   - **白车**（rook）只能在同一行或同一列直线移动。只要黑后在同一行或同一列，且车和后之间没有别的棋子挡住，就可以一步吃掉。  
   - **白象**（bishop）只能沿对角线移动。只要黑后在同一条对角线上（行差等于列差的绝对值），且象和后之间没有别的棋子挡住，也可以一步吃掉。

2. **如果一步不行，答案一定是 2 步**。  
   题目保证在最多两步内一定能把后吃掉，所以不需要再去枚举所有可能的中间位置，只要判断“一步不可”，直接返回 2。

> **类比**：  
> - **哈希表**就像一本字典，`key` 是单词，`value` 是页码。这里我们不需要哈希表，只需要**判断两个坐标是否在同一条“路”上**，相当于在字典里查“这两个词是否在同一页”。  
> - **判断是否被挡住**就像看两座城市之间的高速是否被修路封闭，只要中间没有“封路”（即另一枚白棋子）就可以直达。

**为什么这种做法一定对？**  
- 车和象的走法都是**直线**（水平/垂直或斜线），而棋盘只有 8×8，最多只能被另一枚白子挡住一次。  
- 只要不在同一直线上，就不可能一步吃掉。  
- 题目保证 **2 步必能吃掉**，所以只要“一步不可”，答案必为 2。

**时间/空间复杂度**  
- 只检查几次坐标关系，**时间复杂度是 O(1)**（常数时间），不随输入规模增长。  
- 只用几个整数变量，**空间复杂度也是 O(1)**。

#### 代码（Python）

```python
def minMoves(a: int, b: int, c: int, d: int, e: int, f: int) -> int:
    """
    a, b : white rook   (row, col)
    c, d : white bishop (row, col)
    e, f : black queen  (row, col)
    返回最少走子次数（1 或 2）
    """

    # ---------- 辅助函数 ----------
    def between(x1, y1, x2, y2, x, y) -> bool:
        """
        判断坐标 (x, y) 是否严格位于 (x1, y1) 与 (x2, y2) 之间
        前提：三点在同一直线上（同行、同列或同对角线）
        """
        # 同行：行相同，列在两端之间
        if x1 == x2 == x:
            return min(y1, y2) < y < max(y1, y2)
        # 同列：列相同，行在两端之间
        if y1 == y2 == y:
            return min(x1, x2) < x < max(x1, x2)
        # 同对角线：行差等于列差，且坐标在两端之间
        if abs(x1 - x2) == abs(y1 - y2) and abs(x1 - x) == abs(y1 - y):
            return min(x1, x2) < x < max(x1, x2) and min(y1, y2) < y < max(y1, y2)
        return False

    # ---------- 1 步能否吃掉 ----------
    # 1) 白车攻击黑后
    rook_can = False
    if a == e:                               # 同行
        if not between(a, b, e, f, c, d):    # 象不在中间
            rook_can = True
    if b == f:                               # 同列
        if not between(a, b, e, f, c, d):
            rook_can = True

    # 2) 白象攻击黑后
    bishop_can = False
    if abs(c - e) == abs(d - f):             # 同对角线
        if not between(c, d, e, f, a, b):    # 车不在中间
            bishop_can = True

    if rook_can or bishop_can:               # 任意一种一步可吃
        return 1

    # ---------- 一步不行，答案必为 2 ----------
    return 2
```

#### 复杂度

- **时间复杂度**：`O(1)` — 只做了几次常数次的比较和算术运算。  
  > 大白话：不管输入是 1 组坐标还是 1000 组，这段代码花的时间几乎不变，就像在桌面上摆放几枚棋子，检查它们的相对位置，速度永远很快。

- **空间复杂度**：`O(1)` — 只用了几个整数变量和一个小函数，几乎不占内存。  
  > 大白话：就像你口袋里只放了一支笔和一张纸，根本不占空间。

---

### 2. 最优解

#### 思路  

其实上面的“暴力”已经是最优解，因为**整个问题只涉及常数个坐标**，没有任何需要遍历或动态规划的子结构。  
这里再从“从暴力到最优”的角度解释思考过程：

1. **发现瓶颈**  
   - 初始想法可能是枚举所有白子可以走到的格子，再判断是否能在第二步吃到后，这会产生 O(64) 的枚举，虽然仍是常数时间，但不够“最干净”。  
   - 观察到题目已经给出 **答案只能是 1 或 2**，所以我们只需要判断“是否一步可吃”。不需要真正枚举第二步的路径。

2. **一步判定的关键**  
   - **直线/对角线检查**：车只看行或列，象只看斜线。  
   - **是否被挡**：只可能被另一枚白子挡住，因为黑后是目标，不能被自己挡。  
   - 这两个检查只用几条 `if` 就能完成。

3. **核心数据结构**：这里不需要额外的数据结构，只用了 **坐标比较** 与 **一个判断“在两点之间” 的小函数**。

> **图示文字**：  
> - 想象棋盘是一条十字路口，白车像公交车只能走东西南北，白象像地铁只能沿对角线跑。黑后是站点。只要公交车或地铁的线路直接连到站点且中间没有其他车辆拦路，就能“一站到达”。否则，你只能先换乘一次（走到另一个能直达的站点），再第二次到达目的地——这正是两步的含义。

#### 代码（Python）

（与上面暴力解相同，已是最优实现）

```python
def minMoves(a: int, b: int, c: int, d: int, e: int, f: int) -> int:
    def between(x1, y1, x2, y2, x, y) -> bool:
        if x1 == x2 == x:
            return min(y1, y2) < y < max(y1, y2)
        if y1 == y2 == y:
            return min(x1, x2) < x < max(x1, x2)
        if abs(x1 - x2) == abs(y1 - y2) and abs(x1 - x) == abs(y1 - y):
            return min(x1, x2) < x < max(x1, x2) and min(y1, y2) < y < max(y1, y2)
        return False

    # 车能否一步吃
    if a == e and not between(a, b, e, f, c, d):
        return 1
    if b == f and not between(a, b, e, f, c, d):
        return 1

    # 象能否一步吃
    if abs(c - e) == abs(d - f) and not between(c, d, e, f, a, b):
        return 1

    # 否则必然两步
    return 2
```

#### 复杂度

- **时间复杂度**：`O(1)` — 只做常数次比较。  
  与暴力解相比，没有任何额外遍历，速度完全一样且代码更简洁。

- **空间复杂度**：`O(1)` — 只使用少量局部变量。

---

## 心得

- **核心技巧**：判断两点是否在同一直线上（行、列或对角线），以及是否被另一枚棋子挡住。  
- **适用的题型**  
  1. “**最少步数捕获**”系列，如 *Minimum Moves to Capture the Rook*。  
  2. “**棋子是否相互攻击**”的判断题，如 *Can the King Capture the Queen?*。  
  3. “**两步可达**”的几何格子问题，例如 *Two Moves to Reach Target*。

- **一句话总结解题钥匙**：  
  **“一步可吃 ⇔ 同一直线且中间无阻”。** 若不满足，一步必不可，答案直接是 2。

---

## 反思

- **第一反应**：看到“最少步数”，本能想把所有可能的走法枚举出来。  
- **最容易踩的坑**  
  - 忘记检查 **是否被另一枚白子挡住**，只判断同一行/列/对角线会得到错误的 1 步答案。  
  - 边界条件：坐标在棋盘边缘（1 或 8）时仍需正常判断，`between` 函数必须排除“恰好在端点”的情况。  
- **下次遇到同类题**：第一步先判断**是否已经在攻击范围内且无阻挡**，如果不行，直接返回 “2”。这一步往往就能决定答案，后面的复杂搜索可以省掉。