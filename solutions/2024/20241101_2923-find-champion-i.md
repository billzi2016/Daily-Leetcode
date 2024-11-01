# #2923. **寻找冠军 I** / Find Champion I

> 难度：简单 · 标签：Array、Matrix · [LeetCode 链接](https://leetcode.com/problems/find-champion-i/)

---

## 题目（英文原版）

**Description**

There are n teams numbered from 0 to n - 1 in a tournament.
Given a 0-indexed 2D boolean matrix grid of size n * n. For all i, j that 0 <= i, j <= n - 1 and i != j team i is stronger than team j if grid[i][j] == 1, otherwise, team j is stronger than team i.
Team a will be the champion of the tournament if there is no team b that is stronger than team a.
Return the team that will be the champion of the tournament.

**Examples**

**Example 1:**

```
Input: grid = [[0,1],[0,0]]
Output: 0
Explanation: There are two teams in this tournament.
grid[0][1] == 1 means that team 0 is stronger than team 1. So team 0 will be the champion.
```

**Example 2:**

```
Input: grid = [[0,0,1],[1,0,1],[0,0,0]]
Output: 1
Explanation: There are three teams in this tournament.
grid[1][0] == 1 means that team 1 is stronger than team 0.
grid[1][2] == 1 means that team 1 is stronger than team 2.
So team 1 will be the champion.
```

**Constraints**

- n == grid.length
- n == grid[i].length
- 2 <= n <= 100
- grid[i][j] is either 0 or 1.
- For all i grid[i][i] is 0.
- For all i, j that i != j, grid[i][j] != grid[j][i].
- The input is generated such that if team a is stronger than team b and team b is stronger than team c, then team a is stronger than team c.

---

## 题目（中文翻译）

给定一个编号为 `0` 到 `n-1` 的 `n` 支队伍参加一场锦标赛。  
提供一个下标从 `0` 开始的 `n × n` 布尔矩阵 `grid`。对所有满足 `0 ≤ i, j ≤ n-1 且 i ≠ j` 的 `i, j`，若 `grid[i][j] == 1`，则队伍 `i` **更强**（stronger）于队伍 `j`；否则队伍 `j` 更强于队伍 `i`。  

如果不存在任何队伍 `b` 比队伍 `a` 更强，则队伍 `a` 将成为本次锦标赛的 **冠军**（champion）。  
请返回锦标赛的冠军队伍编号。

---

**示例 1**

```text
Input: grid = [[0,1],[0,0]]
Output: 0
Explanation: 本锦标赛有两支队伍。  
grid[0][1] == 1 表示队伍 0 更强于队伍 1。因此队伍 0 成为冠军。
```

**示例 2**

```text
Input: grid = [[0,0,1],[1,0,1],[0,0,0]]
Output: 1
Explanation: 本锦标赛有三支队伍。  
grid[1][0] == 1 表示队伍 1 更强于队伍 0。  
grid[1][2] == 1 表示队伍 1 更强于队伍 2。  
因此队伍 1 成为冠军。
```

---

**约束条件**

- `n == grid.length`
- `n == grid[i].length`
- `2 ≤ n ≤ 100`
- `grid[i][j]` 仅为 `0` 或 `1`
- 对所有 `i`，`grid[i][i]` 为 `0`
- 对所有 `i, j`（`i != j`），`grid[i][j] != grid[j][i]`
- 输入保证若队伍 `a` 更强于队伍 `b` 且队伍 `b` 更强于队伍 `c`，则队伍 `a` 也更强于队伍 `c`（即关系满足传递性）。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**逐个检查每支队伍**，看有没有别的队伍比它强。如果某支队伍 `i` 没有任何 `j` 满足 `grid[j][i] == 1`（即没有队伍 `j` 在 `i` 的左边为 1），那么 `i` 就是冠军。

- **用到的数据结构**：二维布尔矩阵 `grid`。可以把它想象成一张“比赛结果表”，行代表“我”，列代表“对手”。如果 `grid[i][j] = 1`，就像在字典里查到 “i > j”，对应的“解释”是 “i 比 j 强”。  
- **为什么正确**：题目保证“如果 a 强于 b 且 b 强于 c，则 a 必然强于 c”，也就是说强关系满足传递性。只要找不到比 `i` 强的队伍，`i` 必然是所有队伍中最强的（即冠军）。
- **复杂度大白话**：我们要对每支队伍检查它的所有对手，检查一次算一次操作。若有 `n` 支队伍，就要检查 `n × n` 次，记作 **O(n²)**，意思是“随队伍数的平方增长”。空间上只用到原矩阵和常数个变量，记作 **O(1)**（常数空间）。

#### 代码（Python）

```python
def findChampion(grid):
    n = len(grid)                     # 队伍总数
    for i in range(n):                # 逐个尝试每支队伍 i
        champion = True               # 假设 i 是冠军
        for j in range(n):            # 检查所有其他队伍 j
            if i == j:
                continue              # 自己和自己不比较
            if grid[j][i] == 1:       # j 比 i 强
                champion = False      # i 不是冠军
                break                 # 立刻停止对 i 的检查
        if champion:                  # 没有任何 j 强过 i
            return i                  # 找到冠军，直接返回
    return -1                         # 根据题意不会走到这里
```

#### 复杂度

- **时间复杂度**：**O(n²)** — 需要检查每支队伍和所有其他队伍的关系，随 `n` 的平方增长。  
- **空间复杂度**：**O(1)** — 只用了若干整数变量，和输入矩阵的大小无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都要遍历完整个矩阵**。观察矩阵的特性：

1. **传递性**：如果 `a > b` 且 `b > c`，则 `a > c`。  
2. **互斥性**：对于任意 `i ≠ j`，`grid[i][j]` 与 `grid[j][i]` 必然相反（一个是 1，另一个是 0）。

利用这两点，我们可以**一次遍历就淘汰不可能的冠军**：

- 先假设 `0` 为冠军候选者 `cand`。  
- 依次比较 `cand` 与 `i`（`i` 从 `1` 到 `n-1`）：
  - 若 `cand` **输给** `i`（即 `grid[cand][i] == 0`），说明 `cand` 不是冠军，直接把 `cand` 换成 `i`。
  - 若 `cand` **赢** `i`（`grid[cand][i] == 1`），则 `i` 不可能是冠军，保持 `cand` 不变。

因为每一次比较都能**淘汰一个队伍**，遍历结束后留下的 `cand` 必然是没有更强队伍的冠军。整个过程只遍历一次矩阵的上三角（或下三角），时间 **O(n)**。

> **类比**：想象有 `n` 位选手站成一排，先让第一个选手和第二个比，输的直接让位；再让留下来的选手和第三个比，依此类推，最后留下的就是最强者。每一次比拼都只需要看两个人的直接对决，省掉了大量不必要的比较。

#### 代码（Python）

```python
def findChampion(grid):
    n = len(grid)
    cand = 0                     # 先假设 0 为冠军候选
    for i in range(1, n):        # 依次与后面的队伍比较
        # 如果 cand 输给 i，则 cand 不是冠军，换成 i
        if grid[cand][i] == 0:   # 说明 i > cand
            cand = i
        # else: cand > i，i 被淘汰，cand 仍然是候选
    return cand                  # 循环结束后 cand 必是冠军
```

#### 复杂度

- **时间复杂度**：**O(n)** — 只遍历一次 `n-1` 次比较，随队伍数线性增长，比暴力的 `O(n²)` 快很多。  
- **空间复杂度**：**O(1)** — 只用一个整数 `cand` 保存候选者，额外空间不随 `n` 增长。

---

## 心得

- **核心技巧**：**一次遍历淘汰法**（也叫“候选者消除”），利用传递性和互斥性快速定位唯一的最强元素。  
- **适用的题型**：
  1. “找出所有人中最受欢迎的那个人”（如 LeetCode 1512. 好数对）  
  2. “寻找唯一的“老师”或“领袖””类问题（如找出图中唯一的“根节点”）  
  3. “找出数组中只出现一次的元素”时的“摩尔投票”思路（同样是一次遍历淘汰）  
- **一句话总结**：**把“谁比谁强”这张表想成“一场接一场的决斗”，每场只保留胜者，最后留下的就是冠军。**

---

## 反思

- **第一反应**：看到“没有比它强的队伍”，第一时间会想到“逐个检查是否有更强的”。  
- **最容易踩的坑**：
  - 忘记矩阵对角线 `grid[i][i]` 必为 `0`，但代码里仍要跳过自己避免误判。  
  - 误以为 `grid[i][j] == 1` 表示 “i 被 j 打败”，实际上是 “i 强于 j”。方向记反会导致答案相反。  
  - 没有利用题目给出的**传递性**，导致仍使用 `O(n²)` 的暴力解。  
- **下次类似题的第一步**：先检查是否有“**传递性或互斥性**”的特性，尝试用**一次遍历消除**的思路把候选者压缩到常数个，再做验证。