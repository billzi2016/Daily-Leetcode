# #1386. 电影院座位分配 / Cinema Seat Allocation

> 难度：中等 · 标签：Array、Hash Table、Greedy、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/cinema-seat-allocation/)

---

## 题目（英文原版）

**Description**

A cinema has n rows of seats, numbered from 1 to n and there are ten seats in each row, labelled from 1 to 10 as shown in the figure above.
Given the array reservedSeats containing the numbers of seats already reserved, for example, reservedSeats[i] = [3,8] means the seat located in row 3 and labelled with 8 is already reserved.
Return the maximum number of four-person groups you can assign on the cinema seats. A four-person group occupies four adjacent seats in one single row. Seats across an aisle (such as [3,3] and [3,4]) are not considered to be adjacent, but there is an exceptional case on which an aisle split a four-person group, in that case, the aisle split a four-person group in the middle, which means to have two people on each side.

**Examples**

**Example 1:**

```
Input: n = 3, reservedSeats = [[1,2],[1,3],[1,8],[2,6],[3,1],[3,10]]
Output: 4
Explanation: The figure above shows the optimal allocation for four groups, where seats mark with blue are already reserved and contiguous seats mark with orange are for one group.
```

**Example 2:**

```
Input: n = 2, reservedSeats = [[2,1],[1,8],[2,6]]
Output: 2
```

**Example 3:**

```
Input: n = 4, reservedSeats = [[4,3],[1,4],[4,6],[1,7]]
Output: 4
```

**Constraints**

- 1 <= n <= 10^9
- 1 <= reservedSeats.length <= min(10*n, 10^4)
- reservedSeats[i].length == 2
- 1 <= reservedSeats[i][0] <= n
- 1 <= reservedSeats[i][1] <= 10
- All reservedSeats[i] are distinct.

---

## 题目（中文翻译）

描述  
一座电影院有 `n` 行（row）座位，行号从 `1` 到 `n`，每行有十个座位（seat），编号为 `1` 到 `10`，如上图所示。  
给定数组 `reservedSeats`，其中每个元素 `reservedSeats[i] = [r, c]` 表示第 `r` 行第 `c` 列的座位已被预订。例如，`[3,8]` 表示第 3 行、编号为 8 的座位已被占用。  

返回可以在电影院座位上安排的最多 **四人组**（four-person group）数量。一个四人组占用同一行中相邻的四个座位。跨过过道（aisle）的座位（例如 `[3,3]` 与 `[3,4]`）不视为相邻，但有一种例外情况：如果过道正好把四人组分成两半，即每侧各坐两人，这仍然算作一个合法的四人组。

示例  
示例 1:  
输入: `n = 3`, `reservedSeats = [[1,2],[1,3],[1,8],[2,6],[3,1],[3,10]]`  
输出: `4`  
解释: 上图展示了四个四人组的最优分配方案，蓝色标记的座位已被预订，橙色标记的连续座位用于一个四人组。

示例 2:  
输入: `n = 2`, `reservedSeats = [[2,1],[1,8],[2,6]]`  
输出: `2`  

示例 3:  
输入: `n = 4`, `reservedSeats = [[4,3],[1,4],[4,6],[1,7]]`  
输出: `4`  

约束条件  
- `1 <= n <= 10^9`  
- `1 <= reservedSeats.length <= min(10*n, 10^4)`  
- `reservedSeats[i].length == 2`  
- `1 <= reservedSeats[i][0] <= n`  
- `1 <= reservedSeats[i][1] <= 10`  
- 所有 `reservedSeats[i]` 均不相同。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每一排的座位都列出来**，然后把已经被预定的座位标记为 “不可用”。接着在该排里**枚举所有可能的 4 连座**，只要这 4 个座位都是可用的，就算作一个四人组。遍历完所有排，得到的组数即为答案。

- **使用的数据结构**  
  - **二维列表** `cinema = [[0]*11 for _ in range(n+1)]`（第 0 列不使用，只是把座位号和下标对应起来）。这里的 `cinema[row][seat] = 1` 表示该座位已被预定。可以把它想象成一本“座位手册”，每一页对应一排，页码上标记了哪些座位被占了。  
  - **列表 `reservedSeats`** 本身已经给出了哪些座位被占，用它直接在手册上打勾即可。

- **为什么这个方法一定能得到正确答案**  
  - 我们检查了**每一排的每一种合法的四连座**，只要它们全部未被占用，就一定可以安排一个四人组。没有漏掉的情况，也不会把不合法的坐法算进去（比如跨过过道的座位）。

- **时间/空间复杂度的大白话**  
  - **时间复杂度**：我们要遍历 `n` 排，每排检查最多 3 种四连座（[2‑5]、[4‑7]、[6‑9]），所以是 `O(n)`。但是题目里 `n` 可能高达 `10^9`，如果真的逐排遍历，执行时间会非常久——这就是暴力解的**瓶颈**。  
  - **空间复杂度**：我们用了一个大小为 `n × 11` 的二维数组，等价于 **`O(n)` 的额外空间**，当 `n` 很大时几乎不可能在内存里放下。

> **大概意思**：暴力解就像把电影院的每一排都画出来，逐个检查，可是电影院有可能上亿排，这样画图会花掉太多时间和内存。

#### 代码（Python）

```python
def maxNumberOfFamilies_bruteforce(n, reservedSeats):
    # 1. 建立座位手册（第 0 列不使用，方便下标对应座位号）
    cinema = [[0] * 11 for _ in range(n + 1)]

    # 2. 把已经预定的座位标记为 1
    for r, c in reservedSeats:
        cinema[r][c] = 1          # 把第 r 排第 c 座位设为已占

    ans = 0
    # 3. 按排遍历，检查三种可能的四连座
    for row in range(1, n + 1):
        left   = all(cinema[row][i] == 0 for i in range(2, 6))   # 2~5
        middle = all(cinema[row][i] == 0 for i in range(4, 8))   # 4~7
        right  = all(cinema[row][i] == 0 for i in range(6, 10))  # 6~9

        # 4. 根据检查结果累加最大可安排的家庭数
        if left and right:
            ans += 2          # 两边都可以，最多安排两组
        elif left or middle or right:
            ans += 1          # 至少有一块可以安排一组
        # else: 0 组，什么都不加

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 这里的 `O(n)` 表示我们要遍历每一排一次。如果 `n = 10^9`，即使每一步只做几次判断，也要花上 **十亿次**的循环，实际运行会超时。  
- **空间复杂度**：`O(n)`  
  - 需要 `n` 行的二维数组来记录每个座位的占用情况，随着 `n` 增大，内存需求会线性增长，根本装不下。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到，**真正影响答案的只有有预定座位的那几排**。其余没有任何预定的排，天然可以安排 **两组**（左边 `[2‑5]` 与右边 `[6‑9]`），因为它们的座位都是空的。  

**关键瓶颈**  
- 暴力解遍历所有 `n` 排，导致 `O(n)` 的时间和空间。  
- 实际上，`reservedSeats` 的长度最多只有 `10⁴`，也就是说**只有最多 `10⁴` 行会受到影响**。

**优化思路**  

1. **只处理出现过预定的行**。用 **哈希表（字典）** 把每一行的已占座位压缩成一个整数的**位掩码**（bitmask）。  
   - 把座位号 1~10 看作 10 位二进制，从右到左对应座位 1~10。  
   - 如果座位被占，用 `1` 表示；未占用，用 `0` 表示。  
   - 这样每一行只需要一个整数（最多 10 位）就能完整描述它的占用情况。  
   - 类比：哈希表就像一本**电话簿**，`key` 是行号，`value` 是该行的座位“状态码”。查找、插入都是 `O(1)`。

2. **对每一行的位掩码进行判定**，决定可以安排几组家庭。  
   - **左侧四连座** `[2,3,4,5]` 对应的位掩码是 `0b00011110`（十进制 30）。  
   - **右侧四连座** `[6,7,8,9]` 对应的位掩码是 `0b111100000`（十进制 960）。  
   - **中间四连座** `[4,5,6,7]` 对应的位掩码是 `0b00111100`（十进制 60）。  
   - 对当前行的掩码 `mask`：  
     - 如果左侧和右侧都没有被占（`mask & left == 0` 且 `mask & right == 0`），则可以安排 **2 组**。  
     - 否则，如果左侧或右侧或中间有任意一块是空的（`mask & left == 0` 或 `mask & right == 0` 或 `mask & middle == 0`），则可以安排 **1 组**。  
     - 否则，**0 组**。

3. **统计答案**  
   - 对所有出现过的行按照上面的规则累计可安排的组数。  
   - 再加上 **其余未出现的行数** `n - len(rows_with_reservation)`，每行都能安排 2 组。  

**核心算法/数据结构解释**  

- **位运算（Bit Manipulation）**：把 10 个座位压成 10 位二进制，利用 `&`（与）操作快速判断某几位是否全为 0（即这些座位全空）。  
  - 想象每个位是一个小灯泡，`1` 表示灯亮（座位被占），`0` 表示灯灭（座位空）。我们只需要检查某几个灯泡是否全灭，用 “与” 操作一次即可。  
- **哈希表（字典）**：只保存有预定的行，查询/更新都是 O(1)。这样即使 `n` 超大，也只会使用 `O(m)` 空间，其中 `m = len(reservedSeats) ≤ 10⁴`。

#### 代码（Python）

```python
def maxNumberOfFamilies(n: int, reservedSeats: list[list[int]]) -> int:
    """
    贪心 + 位掩码
    只遍历出现过预定的行，时间 O(m)，空间 O(m)，m = len(reservedSeats) <= 10^4
    """
    # 1. 用字典记录每一行的占用位掩码
    row_mask = {}                     # key: 行号, value: 10 位二进制掩码
    for r, c in reservedSeats:
        # 把座位 c 对应的那一位设为 1
        # 1 << (c-1) 把 1 移动到第 (c-1) 位（因为座位号从 1 开始）
        row_mask[r] = row_mask.get(r, 0) | (1 << (c - 1))

    # 2. 预先写好的三个关键掩码（十进制写法更直观）
    LEFT   = 0b00011110   # seats 2,3,4,5
    RIGHT  = 0b111100000  # seats 6,7,8,9
    MID    = 0b00111100   # seats 4,5,6,7

    families = 0

    # 3. 只遍历有预定的行，逐行判断可以安排几组
    for mask in row_mask.values():
        left_free  = (mask & LEFT) == 0      # 左侧四连座全空
        right_free = (mask & RIGHT) == 0     # 右侧四连座全空
        if left_free and right_free:
            families += 2                     # 左右都能坐，最多两组
        elif left_free or right_free or (mask & MID) == 0:
            families += 1                     # 至少有一块能坐一组
        # else: 0 组，不加

    # 4. 其余没有任何预定的行，每行都能坐 2 组
    families += (n - len(row_mask)) * 2
    return families
```

#### 复杂度  

- **时间复杂度**：`O(m)`，其中 `m = len(reservedSeats) ≤ 10⁴`。  
  - 只遍历了预定列表一次构建哈希表，随后遍历哈希表的键值（最多 `m` 行），每行只做几次位运算，常数时间。相比暴力的 `O(n)`（`n` 可能是十亿），速度提升 **数万倍**。  
- **空间复杂度**：`O(m)`。  
  - 哈希表只存有预定的行及其位掩码，最多 `m` 条记录，远小于 `n`。  

与暴力解相比，**时间从遍历所有排降到只遍历有预定的少数排**，**空间从 `O(n)` 降到 `O(m)`**，因此在极大规模的输入下也能轻松通过。

---

## 心得  

- **核心技巧**：**位掩码 + 哈希表的贪心判定**。  
- **适用的题型**：  
  1. “座位/房间/停车位”类的布局优化（如 LeetCode 1109 – 航班预订统计的压缩技巧）。  
  2. “子集/区间是否被占用”类的查询（如 1695 – 删除子数组的最大和）。  
- **一句话总结解题钥匙**：**只关心有冲突的行，用几位二进制快速判断四连座是否空**。

---

## 反思  

- **第一反应**：看到每排只有 10 个座位，就想把每排的座位全部展开成数组，然后逐排枚举。  
- **最容易踩的坑**：  
  - 忘记 **过道的限制**：座位 4 与 5 之间有过道，不能把跨过道的四个座位算作相邻。  
  - 只检查左侧和右侧，却遗漏了 **中间块** `[4,5,6,7]`（当左侧或右侧被占，但中间仍可坐时，只能安排一组）。  
  - 当 `n` 很大时，直接遍历所有排会导致 **超时或内存爆炸**。  
- **下次类似题的第一步**：先**统计出现冲突的行**（或区间），再**用压缩表示（位掩码/哈希表）**进行常数时间判定，避免对无冲突的部分做冗余遍历。