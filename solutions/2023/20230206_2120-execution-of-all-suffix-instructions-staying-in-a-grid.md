# #2120. 在网格中执行所有后缀指令且保持在网格内 / Execution of All Suffix Instructions Staying in a Grid

> 难度：中等 · 标签：String、Simulation · [LeetCode 链接](https://leetcode.com/problems/execution-of-all-suffix-instructions-staying-in-a-grid/)

---

## 题目（英文原版）

**Description**

There is an n x n grid, with the top-left cell at (0, 0) and the bottom-right cell at (n - 1, n - 1). You are given the integer n and an integer array startPos where startPos = [startrow, startcol] indicates that a robot is initially at cell (startrow, startcol).
You are also given a 0-indexed string s of length m where s[i] is the ith instruction for the robot: 'L' (move left), 'R' (move right), 'U' (move up), and 'D' (move down).
The robot can begin executing from any ith instruction in s. It executes the instructions one by one towards the end of s but it stops if either of these conditions is met:
Return an array answer of length m where answer[i] is the number of instructions the robot can execute if the robot begins executing from the ith instruction in s.

**Examples**

**Example 1:**

```
Input: n = 3, startPos = [0,1], s = "RRDDLU"
Output: [1,5,4,3,1,0]
Explanation: Starting from startPos and beginning execution from the ith instruction:
- 0th: "RRDDLU". Only one instruction "R" can be executed before it moves off the grid.
- 1st:  "RDDLU". All five instructions can be executed while it stays in the grid and ends at (1, 1).
- 2nd:   "DDLU". All four instructions can be executed while it stays in the grid and ends at (1, 0).
- 3rd:    "DLU". All three instructions can be executed while it stays in the grid and ends at (0, 0).
- 4th:     "LU". Only one instruction "L" can be executed before it moves off the grid.
- 5th:      "U". If moving up, it would move off the grid.
```

**Example 2:**

```
Input: n = 2, startPos = [1,1], s = "LURD"
Output: [4,1,0,0]
Explanation:
- 0th: "LURD".
- 1st:  "URD".
- 2nd:   "RD".
- 3rd:    "D".
```

**Example 3:**

```
Input: n = 1, startPos = [0,0], s = "LRUD"
Output: [0,0,0,0]
Explanation: No matter which instruction the robot begins execution from, it would move off the grid.
```

**Constraints**

- m == s.length
- 1 <= n, m <= 500
- startPos.length == 2
- 0 <= startrow, startcol < n
- s consists of 'L', 'R', 'U', and 'D'.

---

## 题目（中文翻译）

**题目描述**  
给定一个 `n x n` 的网格，左上角坐标为 `(0, 0)`，右下角坐标为 `(n - 1, n - 1)`。  
你会得到整数 `n` 和一个整数数组 `startPos = [startrow, startcol]`，表示机器人最初位于单元格 `(startrow, startcol)`。  

同时给定一个下标从 `0` 开始的字符串 `s`（长度为 `m`），其中 `s[i]` 表示机器人的第 `i` 条指令，取值为  
- `'L'`（向左移动）  
- `'R'`（向右移动）  
- `'U'`（向上移动）  
- `'D'`（向下移动）  

机器人可以从 `s` 的任意第 `i` 条指令开始执行，随后按顺序执行后续指令，直到满足以下任意条件时停止执行：  
- 移动后超出网格范围。  

返回一个长度为 `m` 的数组 `answer`，其中 `answer[i]` 表示若机器人从第 `i` 条指令开始执行，最多能够成功执行的指令数量。

**示例**  

**示例 1**  
```
Input: n = 3, startPos = [0,1], s = "RRDDLU"
Output: [1,5,4,3,1,0]
Explanation:
从起始位置 `startPos` 开始，并从第 i 条指令起执行：
- 第 0 条："RRDDLU"。只能执行第一条指令 "R"，随后会移出网格。
- 第 1 条："RDDLU"。全部 5 条指令都可以执行，且始终保持在网格内，最终停在 (1, 1)。
- 第 2 条："DDLU"。全部 4 条指令都可以执行。
- 第 3 条："DLU"。只能执行 3 条指令。
- 第 4 条："LU"。只能执行 1 条指令。
- 第 5 条："U"。无法执行任何指令，直接会移出网格。
```

**示例 2**  
```
Input: n = 2, startPos = [1,1], s = "LURD"
Output: [4,1,0,0]
Explanation:
- 第 0 条："LURD"：全部 4 条指令均可执行。
- 第 1 条："URD"：只能执行第一条指令 "U"，随后会移出网格。
- 第 2 条："RD"：无法执行任何指令。
- 第 3 条："D"：无法执行任何指令。
```

**示例 3**  
```
Input: n = 1, startPos = [0,0], s = "LRUD"
Output: [0,0,0,0]
Explanation: 无论从哪条指令开始执行，机器人都会立即移出网格，故均为 0。
```

**约束条件**  
- `m == s.length`  
- `1 <= n, m <= 500`  
- `startPos.length == 2`  
- `0 <= startrow, startcol < n`  
- `s` 仅由字符 `'L'`, `'R'`, `'U'`, `'D'` 组成

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**从每一个下标 i 开始，逐条执行指令，看到什么时候会走出棋盘，就停下来**。  
这和我们平时玩游戏时“从第 i 步开始走，看到第一步把人送出地图就算输了”一模一样。  

需要的工具只有两个：

| 数据结构 | 生活化类比 | 用途 |
|----------|-----------|------|
| 两个整数 `row, col` | 机器人在地图上的坐标，就像在城市里用 GPS 定位 | 记录当前所在的格子 |
| 方向映射表 `{'L':(0,-1), 'R':(0,1), 'U':(-1,0), 'D':(1,0)}` | 把指令字符翻译成“往哪走”，就像字典里查单词的解释 | 把字符转换成坐标的增量 |

算法流程：

1. 依次把 `i = 0 … m-1` 当作起始下标。  
2. 把机器人位置重置为 `startPos`（题目给的起始格子）。  
3. 从 `j = i` 向后遍历指令：  
   * 用映射表把 `s[j]` 转成 `(dr, dc)`，更新 `row += dr, col += dc`。  
   * 检查 `row`、`col` 是否仍在 `[0, n-1]` 范围内。  
   * 若仍在棋盘，计数 `cnt += 1`，继续；否则立刻停止。  
4. 把计数 `cnt` 写入答案数组的第 `i` 位。  

为什么一定正确？  
- 我们严格按照题目要求，从第 `i` 条指令开始、一步一步执行，**只要出现越界就立刻结束**，这正是题目定义的“机器人停止的条件”。  
- 所有可能的起始下标都遍历了一遍，所以每个 `answer[i]` 都是对应的最大可执行指令数。

#### 代码（Python）

```python
def executeInstructions(n: int, startPos: list[int], s: str) -> list[int]:
    m = len(s)
    ans = [0] * m                     # 最终答案

    # 把字符映射成坐标增量，想象成“查字典”得到每条指令的方向
    move = {
        'L': (0, -1),   # 向左：行不变，列 -1
        'R': (0, 1),    # 向右：列 +1
        'U': (-1, 0),   # 向上：行 -1
        'D': (1, 0)     # 向下：行 +1
    }

    # ------------------- 暴力遍历每个起始下标 -------------------
    for i in range(m):                # i 是本次模拟的起始指令下标
        row, col = startPos           # 机器人回到起点
        cnt = 0                       # 能成功执行的指令数

        for j in range(i, m):         # 从 i 开始往后执行指令
            dr, dc = move[s[j]]       # 把字符翻译成“往哪走”
            row += dr
            col += dc

            # 检查是否仍在棋盘内部
            if 0 <= row < n and 0 <= col < n:
                cnt += 1              # 这一步合法，计数+1
            else:                     # 一旦出界，立刻停止本次模拟
                break

        ans[i] = cnt                  # 把本次模拟的结果写入答案

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(m²)`  
  - 外层循环 `m` 次，内层最坏也要遍历 `m` 次（比如机器人一直在棋盘内部），所以总体是 `m × m`。  
  - 把 `O(m²)` 想象成“如果 `m = 500`，最多要算 500 × 500 = 250 000 步”，在现代电脑上毫秒级完成，完全可以接受。  

- **空间复杂度**：`O(1)`（不计答案数组）  
  - 只用了几个整数变量来记录当前位置和计数，和输入规模无关。  

---  

### 2. 最优解  

#### 思路  

虽然上面的暴力解已经能在题目给出的约束下跑完，但我们仍可以 **把每一次“从 i 开始模拟”里重复的工作去掉**，让整体时间更接近线性。  

关键观察：

1. **每一步指令只会让坐标增加或减少 1**。  
2. 对于任意起始下标 `i`，机器人在执行 `s[i … j]`（`i ≤ j`）期间的相对位移，只取决于这段子串里 `'L','R','U','D'` 各出现了多少次，而与 `i` 之前的指令毫无关系。  

因此我们可以先 **预处理出前缀累计位移**（前缀和）：

- `pref_r[k]` = 从 `s[0]` 到 `s[k-1]`（左闭右开）累计的行位移（向上为 -1，向下为 +1）。  
- `pref_c[k]` = 同理的列位移（向左为 -1，向右为 +1）。  

有了前缀累计位移后，任意子串 `s[i … j]` 的净位移可以用 **差分**求出：

```
delta_r = pref_r[j+1] - pref_r[i]
delta_c = pref_c[j+1] - pref_c[i]
```

接下来要判断子串 `s[i … j]` 是否会让机器人出界，只要检查 **在这段子串的每一步**，机器人所在的实际坐标是否仍在 `[0, n-1]`。  
这等价于检查 **在 i … j 之间的所有前缀位移的最小值和最大值** 是否都满足：

```
0 ≤ startRow + (pref_r[t] - pref_r[i]) < n   对所有 i ≤ t ≤ j
0 ≤ startCol + (pref_c[t] - pref_c[i]) < n   对所有 i ≤ t ≤ j
```

于是问题转化为：

> 对每个起始下标 `i`，在数组 `pref_r`、`pref_c` 中找到最远的 `j`，使得在区间 `[i, j]` 内的 **最小前缀位移** 与 **最大前缀位移** 同时保持在合法范围内。

这正是**区间最值查询**（Range Minimum Query / Range Maximum Query）的问题。我们可以用 **稀疏表（Sparse Table）** 在 `O(1)` 时间内得到任意区间的最小值和最大值，预处理耗时 `O(m log m)`。随后对每个 `i` 用 **二分搜索** 找到最大的合法 `j`，总时间 `O(m log m)`。

> 对于初学者来说，稀疏表的实现稍微有点儿技术含量，但概念很简单：把数组分层存，每层保存长度为 `2^k` 的区间最值，查询时只取两段重叠的区间即可得到答案。

下面给出完整实现，代码中会详细解释每一步的意义。

#### 代码（Python）

```python
import math
from typing import List

def executeInstructions(n: int, startPos: List[int], s: str) -> List[int]:
    m = len(s)

    # ---------- 1. 前缀累计位移 ----------
    # pref_r[k] / pref_c[k] 表示执行前 k 条指令后（0 <= k <= m）的行/列位移
    pref_r = [0] * (m + 1)
    pref_c = [0] * (m + 1)

    # 把字符映射成位移，和暴力解里的一样
    move = {'L': (0, -1), 'R': (0, 1), 'U': (-1, 0), 'D': (1, 0)}

    for i, ch in enumerate(s, 1):          # i 从 1 开始，方便构造前缀和
        dr, dc = move[ch]
        pref_r[i] = pref_r[i - 1] + dr
        pref_c[i] = pref_c[i - 1] + dc

    # ---------- 2. 稀疏表预处理 ----------
    # 用来在 O(1) 时间内得到任意区间的最小/最大前缀位移
    LOG = math.floor(math.log2(m)) + 1     # 最高的 2^k 不会超过 m

    # st_min_r[k][i] = 区间 [i, i+2^k) 的最小行位移
    # 同理还有 max、以及列方向的 min/max
    st_min_r = [[0] * (m + 1) for _ in range(LOG)]
    st_max_r = [[0] * (m + 1) for _ in range(LOG)]
    st_min_c = [[0] * (m + 1) for _ in range(LOG)]
    st_max_c = [[0] * (m + 1) for _ in range(LOG)]

    # 第 0 层（长度为 1）的最值就是数组本身
    for i in range(m + 1):
        st_min_r[0][i] = st_max_r[0][i] = pref_r[i]
        st_min_c[0][i] = st_max_c[0][i] = pref_c[i]

    # 构造更高层
    for k in range(1, LOG):
        span = 1 << (k - 1)                # 2^{k-1}
        for i in range(m + 1 - (1 << k) + 1):
            st_min_r[k][i] = min(st_min_r[k-1][i], st_min_r[k-1][i + span])
            st_max_r[k][i] = max(st_max_r[k-1][i], st_max_r[k-1][i + span])
            st_min_c[k][i] = min(st_min_c[k-1][i], st_min_c[k-1][i + span])
            st_max_c[k][i] = max(st_max_c[k-1][i], st_max_c[k-1][i + span])

    # ---------- 3. 区间最值查询函数 ----------
    def query_min_max(arr_min, arr_max, l, r):
        """
        在前缀数组里查询闭区间 [l, r]（两端都包含）的最小值和最大值。
        这里用的是「离线 RMQ」的经典技巧：把区间拆成两段长度为 2^k 的子区间。
        """
        length = r - l + 1
        k = length.bit_length() - 1        # 2^k <= length
        min_val = min(arr_min[k][l], arr_min[k][r - (1 << k) + 1])
        max_val = max(arr_max[k][l], arr_max[k][r - (1 << k) + 1])
        return min_val, max_val

    # ---------- 4. 对每个起始下标二分寻找最远可执行位置 ----------
    ans = [0] * m
    start_r, start_c = startPos

    for i in range(m):
        # 二分搜索合法的最右端 j（闭区间）
        lo, hi = i, m - 1
        best = i - 1                         # 若 i 本身非法，保持 -1
        while lo <= hi:
            mid = (lo + hi) // 2
            # 取区间 [i, mid] 的行/列位移最值
            min_r, max_r = query_min_max(st_min_r, st_max_r, i, mid)
            min_c, max_c = query_min_max(st_min_c, st_max_c, i, mid)

            # 把相对位移转换成绝对坐标范围
            # 机器人在执行过程中最上面会到 start_r + (min_r - pref_r[i])
            # 最下面会到 start_r + (max_r - pref_r[i])，同理列方向
            top    = start_r + (min_r - pref_r[i])
            bottom = start_r + (max_r - pref_r[i])
            left   = start_c + (min_c - pref_c[i])
            right  = start_c + (max_c - pref_c[i])

            # 判断这段子串是否全部保持在棋盘内部
            if 0 <= top and bottom < n and 0 <= left and right < n:
                best = mid                # 这段合法，尝试更长
                lo = mid + 1
            else:
                hi = mid - 1               # 超出边界，必须缩短

        ans[i] = best - i + 1               # 能执行的指令数 = 区间长度

    return ans
```

> **代码要点说明**  
> 1. **前缀累计位移**：把整个指令串抽象成“一条数轴”，`pref_r[i]` 表示执行前 `i` 条指令后，机器人相对于起点在行方向上移动了多少格。  
> 2. **稀疏表**：把前缀数组的最小值/最大值提前算好，查询时只需要取两段重叠的区间（长度都是 `2^k`），时间就是 `O(1)`。  
> 3. **二分搜索**：对每个起始下标 `i`，我们在 `[i, m-1]` 区间里找最长的合法子串。因为合法性随子串长度单调（越长越容易超界），可以用二分把搜索过程从线性降到对数。  
> 4. **合法性判定**：只要子串里**最极端的**行/列位移（最小/最大）仍在棋盘范围内，就说明整个子串都安全**。这正是利用了“最坏情况决定整体”的思想。

#### 复杂度  

- **时间复杂度**：`O(m log m)`  
  - 前缀累计位移 `O(m)`。  
  - 稀疏表构造 `O(m log m)`（每层遍历一次数组）。  
  - 对每个起始下标二分搜索，查询最值 `O(1)`，二分深度 `log m`，所以整体 `O(m log m)`。  
  - 与暴力解的 `O(m²)` 相比，**在 `m` 较大时（比如 10⁵）会快很多**，虽然本题的约束只有 500，二者都能通过，但这套思路在更大规模的同类问题里是“最优”的。

- **空间复杂度**：`O(m log m)`  
  - 稀疏表需要存 `4 * LOG * (m+1)` 个整数（行/列的最小/最大），`LOG ≈ log₂ m`。  
  - 这在 `m ≤ 500` 时几乎可以忽略不计，在更大数据下仍然是线性对数级别的合理开销。

---

## 心得  

- **核心技巧**：**前缀累计 + 区间最值查询**（稀疏表 / RMQ）  
  把“每一步都要检查”转化为“只检查区间的最极端值”。  

- **适用题型**  
  1. “在字符串/数组的子区间里，某个累计值是否会超出阈值” —— 如 LeetCode 1861 *检查是否有合法子数组*。  
  2. “在二维平面上，路径的最远/最近位置是否在安全区” —— 如机器人路径、棋盘游戏的合法移动判断。  
  3. “查询子数组的最大/最小前缀和” —— 如前缀和+单调栈的组合题。

- **一句话总结**：  
  *把连续指令的累计位移抽象成前缀和，利用区间最值快速判断“最坏一步是否出界”，就能一次性算出所有后缀的可执行长度。*

---

## 反思  

- **第一反应**：看到“每个后缀都要模拟”，立刻想到最直白的双层循环——暴力模拟。  

- **最容易踩的坑**  
  1. **越界判断写反**：记得在更新坐标后立刻检查，而不是检查之前的坐标。  
  2. **起始位置忘记恢复**：每次模拟都必须把机器人重新放回 `startPos`，否则会把上一次的位移累加进去。  
  3. **字符映射错误**：`U` 是行减 1，`D` 是行加 1，容易写成相反导致答案全是 0。  

- **下次遇到同类题**：  
  首先判断“是否可以把每一步的影响累加成前缀和”。如果可以，就尝试 **用区间最值（RMQ）或单调栈** 把“逐步检查”压缩成“只检查极值”。这一步往往能把二次暴力降到 `O(m log m)` 或 `O(m)`。