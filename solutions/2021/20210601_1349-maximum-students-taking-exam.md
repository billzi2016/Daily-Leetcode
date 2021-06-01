# #1349. 最大可参加考试的学生数 / Maximum Students Taking Exam

> 难度：困难 · 标签：Array、Dynamic Programming、Bit Manipulation、Matrix、Bitmask · [LeetCode 链接](https://leetcode.com/problems/maximum-students-taking-exam/)

---

## 题目（英文原版）

**Description**

Given a m * n matrix seats  that represent seats distributions in a classroom. If a seat is broken, it is denoted by '#' character otherwise it is denoted by a '.' character.
Students can see the answers of those sitting next to the left, right, upper left and upper right, but he cannot see the answers of the student sitting directly in front or behind him. Return the maximum number of students that can take the exam together without any cheating being possible.
Students must be placed in seats in good condition.

**Examples**

**Example 1:**

```
Input: seats = [["#",".","#","#",".","#"],
                [".","#","#","#","#","."],
                ["#",".","#","#",".","#"]]
Output: 4
Explanation: Teacher can place 4 students in available seats so they don't cheat on the exam.
```

**Example 2:**

```
Input: seats = [[".","#"],
                ["#","#"],
                ["#","."],
                ["#","#"],
                [".","#"]]
Output: 3
Explanation: Place all students in available seats.
```

**Example 3:**

```
Input: seats = [["#",".",".",".","#"],
                [".","#",".","#","."],
                [".",".","#",".","."],
                [".","#",".","#","."],
                ["#",".",".",".","#"]]
Output: 10
Explanation: Place students in available seats in column 1, 3 and 5.
```

**Constraints**

- seats contains only characters '.' and'#'.
- m == seats.length
- n == seats[i].length
- 1 <= m <= 8
- 1 <= n <= 8

---

## 题目（中文翻译）

给定一个 **m × n** 矩阵（matrix）`seats`，表示教室中的座位分布。若座位损坏，用字符 `'#'` 表示；否则用字符 `'.'` 表示。

学生可以看到左侧、右侧、左上方和右上方座位上的答案，但看不到正前方或正后方座位上的答案。返回在不可能出现作弊（cheating）的前提下，能够同时参加考试的学生的最大数量。学生只能坐在完好的座位上。

**示例 1**  

**示例 2**  

**示例 3**  

**约束条件**  

- `seats` 仅包含字符 `'.'` 和 `'#'`。  
- `m == seats.length`  
- `n == seats[i].length`  
- `1 <= m <= 8`  
- `1 <= n <= 8`  

---

### 示例

**示例 1**  
```text
Input: seats = [["#",".","#","#",".","#"],
               [".","#","#","#","#","."],
               ["#",".","#","#",".","#"]]
Output: 4
Explanation: 老师可以在可用座位上安排 4 名学生，使他们之间不会产生作弊。
```

**示例 2**  
```text
Input: seats = [[".","#"],
               ["#","#"],
               ["#","."],
               ["#","#"],
               [".","#"]]
Output: 3
Explanation: 将所有学生安排在可用座位上即可。
```

**示例 3**  
```text
Input: seats = [["#",".",".",".","#"],
               [".","#",".","#","."],
               [".",".","#",".","."],
               [".","#",".","#","."],
               ["#",".",".",".","#"]]
Output: 10
Explanation: 学生可以分别安排在第 1、3、5 列的可用座位上，共计 10 人。
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每一个可以坐人的位置（`'.'`）都当作「要不要坐」的二选一，然后把所有可能的组合全部枚举一遍，挑出合法且人数最多的那种。  

- **数据结构**：我们可以把整个教室的座位看成一个 **一维数组**，每个位置对应一个二进制位（`0` 表示不坐，`1` 表示坐）。  
  - 把二维的 `seats[i][j]` 拉平成 `i * n + j`，就像把一本字典的每一页顺序编号，`key` 是位置，`value` 是这位同学是否坐在这里。  
- **合法性检查**：遍历每一位坐了学生的座位，判断它的左、右、左上、右上四个方向是否也有学生。如果出现冲突，就说明这个组合不合法。  
- **为什么正确**：因为我们把 **所有** 可能的坐法都遍历了一遍，合法的自然不会漏掉，最大人数也一定会被找到。  

> 这里的「暴力」其实是「全枚举」，时间会非常大。  
> 设教室有 `m` 行 `n` 列，最多有 `m*n ≤ 64` 个座位。每个座位两种选择，全部组合数是 `2^(m*n)`，这在最坏情况下是 `2^64`，根本不可能在计算机里跑完。

#### 代码（Python）

```python
from typing import List

def maxStudents_bruteforce(seats: List[List[str]]) -> int:
    m, n = len(seats), len(seats[0])
    total = m * n                     # 教室总座位数
    best = 0

    # 把二维坐标映射到一维下标的函数
    def idx_to_pos(idx):
        return divmod(idx, n)          # 返回 (row, col)

    # 判断当前的 bitmask 是否满足「不作弊」的约束
    def valid(mask: int) -> bool:
        for i in range(total):
            if not (mask >> i) & 1:    # 该位不坐人，直接跳过
                continue
            r, c = idx_to_pos(i)
            # 座位必须是好的（'.'）
            if seats[r][c] == '#':
                return False

            # 检查左、右
            for dc in (-1, 1):
                nc = c + dc
                if 0 <= nc < n:
                    nid = r * n + nc
                    if (mask >> nid) & 1:   # 左右有同学
                        return False

            # 检查左上、右上（只看上一行，因为只会看前面的那排）
            nr = r - 1
            if nr >= 0:
                for dc in (-1, 1):
                    nc = c + dc
                    if 0 <= nc < n:
                        nid = nr * n + nc
                        if (mask >> nid) & 1:   # 左上/右上有同学
                            return False
        return True

    # 完全枚举 0 ~ 2^total - 1
    for mask in range(1 << total):
        cnt = bin(mask).count('1')   # 这套方案里坐了多少人
        if cnt <= best:              # 已经不可能更好，直接跳过
            continue
        if valid(mask):
            best = cnt

    return best
```

> **关键行中文注释** 已写在代码里，帮助你一步步跟上思路。

#### 复杂度  

- **时间复杂度**：`O( 2^(m*n) * (m*n) )`  
  - `2^(m*n)` 是所有可能的坐法数量。  
  - 对每一种坐法我们要检查最多 `m*n` 个座位是否冲突。  
  - 用大白话说，就是「指数级」的时间，随着座位数稍微增长，计算时间就会像滚雪球一样飞快增长，几分钟都跑不完。

- **空间复杂度**：`O(1)`（不计输入）  
  - 只用了若干整数变量和一个 `mask`，不需要额外的数组。  

> 暴力解虽然思路最直白，但在本题的约束（`m,n ≤ 8`）下仍然不可接受，需要更聪明的办法。

---

### 2. 最优解

#### 思路  

**从暴力解出发**，我们已经知道「枚举」是不可行的。观察约束可以发现：

1. **每一行内部**，学生不能坐在相邻的座位（左、右会看到）。  
2. **相邻两行之间**，学生只能受到左上、右上的影响（不看正前方），也就是说第 `i` 行的坐法只需要和第 `i-1` 行的坐法「兼容」即可。

这两个条件都只涉及 **同一行** 或 **相邻两行**，恰好可以用 **动态规划 + 位掩码（bitmask）** 来把问题拆解成「逐行决定」的子问题。

##### 2.1 用位掩码表示一行的坐法  

- 把一行的 `n` 个座位用 `n` 位二进制数表示，`1` 表示该座位上坐了学生，`0` 表示空。  
- 例如 `n = 5`，掩码 `0b01001` 表示第 0、3 位坐了学生（从右往左数第 0 位是最右侧座位）。

> 类比：把每一行当成一本小字典，`key` 是座位下标，`value` 是「是否有人坐」的标记。

##### 2.2 过滤掉「行内冲突」的掩码  

- **左/右相邻**：如果掩码中出现 `11`（相邻两位都是 1），说明这两位学生会互相作弊。  
- 检查方法：`mask & (mask << 1) == 0`。如果左移一位后仍有交集，就说明有相邻的 `1`。

- **坏座位**：如果某个位对应的座位是 `'#'`，则该位在合法掩码里必须是 `0`。  
  - 先把每行的「可坐」信息也用一个掩码 `valid_mask`（`1` 表示该座位是 `'.'`）记录，合法的行掩码必须满足 `mask & ~valid_mask == 0`（即只在可坐位置上取 1）。

把所有满足以上两点的掩码列出来，记为 `valid_row_masks[i]`（第 `i` 行所有合法的坐法）。

##### 2.3 行与行之间的兼容性  

第 `i` 行的掩码 `cur` 与第 `i-1` 行的掩码 `prev` 必须满足：

- `cur` 的左上位置不坐人：`cur & (prev << 1) == 0`
- `cur` 的右上位置不坐人：`cur & (prev >> 1) == 0`

如果两者都为 `0`，说明这两行坐法不会产生左上/右上作弊。

##### 2.4 动态规划  

设 `dp[i][mask]` 为「处理到第 `i` 行（0-index），第 `i` 行使用坐法 `mask` 时，最多能坐多少学生」。递推式：

```
dp[i][cur] = max_{prev ∈ valid_row_masks[i-1] 且 compatible(prev, cur)} 
            ( dp[i-1][prev] + popcount(cur) )
```

- `popcount(cur)` 是 `cur` 二进制中 1 的个数，即第 `i` 行坐了多少学生。  
- 初始 `i = 0` 时，只需要把 `dp[0][mask] = popcount(mask)`（因为没有前一行）。

因为 `m,n ≤ 8`，每行最多只有 `2^n = 256` 种掩码，实际合法的会更少（去掉相邻 1 与坏座位），所以 DP 的状态数量是 `m * 256 * 256`，在毫秒级别即可完成。

##### 2.5 实现细节（零基础解释）

- **位运算**：`<<` 左移相当于把所有座位往右边「搬」一格，`>>` 右移相当于往左搬。用它们可以快速判断左上/右上冲突。
- **popcount**：Python 的 `bin(mask).count('1')` 或 `mask.bit_count()`（Python 3.8+）可以直接算出二进制中 1 的个数。
- **字典/列表存 DP**：因为状态不多，用普通的 `list` 或 `dict` 存放即可。

> 这样，我们把「全局指数枚举」压缩成「每行线性遍历 + 行间兼容检查」的多项式时间，真正实现了「最优」解法。

#### 代码（Python）

```python
from typing import List

def maxStudents(seats: List[List[str]]) -> int:
    m, n = len(seats), len(seats[0])

    # ---------- 1. 把每行的可坐位置转成位掩码 ----------
    # valid_row[i] 的第 j 位为 1 表示 seats[i][j] == '.'
    valid_row = []
    for i in range(m):
        mask = 0
        for j in range(n):
            if seats[i][j] == '.':
                mask |= (1 << j)      # 第 j 位设为 1
        valid_row.append(mask)

    # ---------- 2. 预计算每行所有合法的坐法（没有左/右相邻） ----------
    # valid_masks[i] = [mask1, mask2, ...] 所有满足条件的掩码
    valid_masks = []
    for i in range(m):
        cur_list = []
        # 所有可能的 0~(1<<n)-1 掩码
        for mask in range(1 << n):
            # 必须只坐在可坐的座位上
            if (mask & ~valid_row[i]) != 0:
                continue
            # 左右相邻的学生会作弊，排除出现 11 的情况
            if (mask & (mask << 1)) != 0:
                continue
            cur_list.append(mask)
        valid_masks.append(cur_list)

    # ---------- 3. 动态规划 ----------
    # dp_prev[mask] 表示上一行使用 mask 时的最大人数
    dp_prev = {0: 0}          # 第 -1 行（不存在）只有一种状态：没有学生

    for row in range(m):
        dp_cur = {}
        for cur in valid_masks[row]:
            cur_cnt = cur.bit_count()   # 本行坐了多少人
            # 枚举上一行的合法坐法，检查左上/右上冲突
            for prev, prev_val in dp_prev.items():
                if (cur & (prev << 1)) != 0:   # 左上冲突
                    continue
                if (cur & (prev >> 1)) != 0:   # 右上冲突
                    continue
                # 兼容，更新本行的 dp
                new_val = prev_val + cur_cnt
                if cur not in dp_cur or new_val > dp_cur[cur]:
                    dp_cur[cur] = new_val
        dp_prev = dp_cur                # 进入下一行

    # ---------- 4. 所有行处理完后，答案是 dp_prev 中的最大值 ----------
    return max(dp_prev.values())
```

> **代码要点注释** 已在每段前加了中文解释，帮助你把抽象的位运算映射到「左上、右上」的实际含义。

#### 复杂度  

- **时间复杂度**：`O( m * S^2 )`，其中 `S` 是单行合法掩码的数量。  
  - `S ≤ 2^n`，且 `n ≤ 8`，所以 `S ≤ 256`。  
  - 具体来说我们遍历每行的每个合法 `cur`，再遍历上一行的每个合法 `prev` 检查兼容性。  
  - 用大白话说，就是「最多 8 行 × (256 × 256) 次比较」，约十几万次操作，跑得非常快。

- **空间复杂度**：`O( S )`。我们只保留当前行和上一行的 DP 表（字典），最多存 `256` 条记录。  

> 与暴力解相比，时间从指数级（`2^(m*n)`) 降到了多项式级（`m * 2^(2n)`），在本题约束下是完全可接受的。

---

## 心得

- **核心技巧**：**按行使用位掩码 + 动态规划**，把二维约束转化为「相邻行兼容」的状态转移问题。  
- **适用的题型**（类似思路）  
  1. **Maximum Students Taking Exam**（本题）  
  2. **The Skyline Problem**（用位掩码处理行约束的变体）  
  3. **Maximum Profit in Job Scheduling**（行/时间段的兼容性 DP）  
- **一句话总结解题钥匙**：  
  > “把每一行抽象成一串 0/1 的二进制，枚举合法的 0/1 串，再用 DP 按行累加最大人数。”

---

## 反思

- **第一反应**：看到“左上、右上”这种局部视野限制，立刻想到「相邻行之间会产生冲突」——于是想到按行处理。  
- **最容易踩的坑**  
  1. **左/右相邻冲突**：忘记在每行内部排除 `11` 的情况，会导致非法解被计入。  
  2. **坏座位过滤**：如果不把 `'#'` 位强制置 0，可能会把学生安排在破座位上。  
  3. **位移越界**：左移或右移时需要注意 Python 的整数是无限长，`prev << 1` 可能产生超出 `n` 位的高位，需要在兼容性检查时只关注低 `n` 位（这里直接使用 `&` 判断即可，无需额外掩码）。  
- **下次遇到同类题**：第一步先 **把局部约束抽象成「同一行」或「相邻行」的关系**，再决定是否可以用 **位掩码 + DP** 来压缩状态空间。这样往往能把看似指数级的问题降到可接受的多项式时间。