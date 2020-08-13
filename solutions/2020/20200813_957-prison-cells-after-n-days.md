# #957. N 天后的监狱单元状态 / Prison Cells After N Days

> 难度：中等 · 标签：Array、Hash Table、Math、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/prison-cells-after-n-days/)

---

## 题目（英文原版）

**Description**

There are 8 prison cells in a row and each cell is either occupied or vacant.
Each day, whether the cell is occupied or vacant changes according to the following rules:
Note that because the prison is a row, the first and the last cells in the row can't have two adjacent neighbors.
You are given an integer array cells where cells[i] == 1 if the ith cell is occupied and cells[i] == 0 if the ith cell is vacant, and you are given an integer n.
Return the state of the prison after n days (i.e., n such changes described above).

**Examples**

**Example 1:**

```
Input: cells = [0,1,0,1,1,0,0,1], n = 7
Output: [0,0,1,1,0,0,0,0]
Explanation: The following table summarizes the state of the prison on each day:
Day 0: [0, 1, 0, 1, 1, 0, 0, 1]
Day 1: [0, 1, 1, 0, 0, 0, 0, 0]
Day 2: [0, 0, 0, 0, 1, 1, 1, 0]
Day 3: [0, 1, 1, 0, 0, 1, 0, 0]
Day 4: [0, 0, 0, 0, 0, 1, 0, 0]
Day 5: [0, 1, 1, 1, 0, 1, 0, 0]
Day 6: [0, 0, 1, 0, 1, 1, 0, 0]
Day 7: [0, 0, 1, 1, 0, 0, 0, 0]
```

**Example 2:**

```
Input: cells = [1,0,0,1,0,0,1,0], n = 1000000000
Output: [0,0,1,1,1,1,1,0]
```

**Constraints**

- cells.length == 8
- cells[i] is either 0 or 1.
- 1 <= n <= 109

---

## 题目（中文翻译）

有 8 个监狱单元（cell）排成一行，每个单元要么被占用（1），要么为空（0）。  
每天，单元的占用状态会按照以下规则更新：

- 如果一个单元的左右相邻单元状态相同（即都为 0 或都为 1），则该单元在下一天变为 0（空）。
- 否则，该单元在下一天变为 1（占用）。

> 注意：由于监狱是线性的，首位和末位单元没有两个相邻的邻居，它们的左（或右）邻居视为 0。

给定一个整数数组 `cells`，其中 `cells[i] == 1` 表示第 `i` 个单元被占用，`cells[i] == 0` 表示第 `i` 个单元为空；再给定一个整数 `n`。  
返回经过 `n` 天（即上述状态变化 `n` 次）后的监狱单元状态。

---

### 示例

**示例 1**

```
Input: cells = [0,1,0,1,1,0,0,1], n = 7
Output: [0,0,1,1,0,0,0,0]
Explanation: 下表汇总了监狱在每一天的状态：
Day 0: [0, 1, 0, 1, 1, 0, 0, 1]
Day 1: [0, 1, 1, 0, 0, 0, 0, 0]
Day 2: [0, 0, 0, 0, 1, 1, 1, 0]
Day 3: [0, 1, 1, 0, 0, 1, 0, 0]
Day 4: [0, 0, 0, 0, 0, 1, 0, 0]
Day 5: [0, 1, 1, 1, 0, 1, 0, 0]
Day 6: [0, 0, 1, 0, 1, 1, 0, 0]
Day 7: [0, 0, 1, 1, 0, 0, 0, 0]
```

**示例 2**

```
Input: cells = [1,0,0,1,0,0,1,0], n = 1000000000
Output: [0,0,1,1,1,1,1,0]
```

---

### 约束

- `cells.length == 8`
- `cells[i]` 只能是 `0` 或 `1`
- `1 <= n <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**把每一天都算一遍**，把当天的监狱状态按照题目给出的规则算出第二天的状态，然后把得到的数组再继续往后推，循环 `n` 次。

- **使用的数据结构**：  
  - `list`（Python 中的数组）保存每一天的 8 个监狱格子。  
  - 额外再开一个同样长度的 `new_cells` 用来存放“明天”的状态，算完后再把它复制回 `cells`。  
- **规则的生活化类比**：  
  想象每个格子是一个灯，左边和右边各有一盏灯。若左、右两盏灯的开关状态相同（都是亮或都是灭），那么中间的灯第二天就会 **亮**（1），否则会 **灭**（0）。第一格和最后一格因为没有左/右邻居，永远是灭（0）。  
- **为什么正确**：  
  只要严格按照题目描述对每一天的状态进行一次“翻转”，连续做 `n` 次，最后得到的就是第 `n` 天的监狱状态。  
- **时间/空间复杂度的大白话**：  
  - 时间复杂度 `O(n·8)`，因为我们要遍历 `n` 天，每天遍历 8 个格子。这里的 `8` 是常数，等价于 `O(n)`。如果 `n` 很大（比如 `10^9`），这就像每天跑 8 步，跑了十亿天，显然会慢到爆。  
  - 空间复杂度 `O(1)`，只用了固定大小的几个列表，和 `n` 没有关系。

#### 代码（Python）

```python
from typing import List

class Solution:
    def prisonAfterNDays(self, cells: List[int], n: int) -> List[int]:
        """
        暴力模拟：逐天计算监狱状态
        """
        for _ in range(n):                 # 循环 n 次
            new_cells = [0] * 8            # 新一天的状态，默认全 0（首尾永远是 0）
            for i in range(1, 7):          # 只需要关心中间 6 个格子
                # 左右相等则变成 1，否则 0
                new_cells[i] = 1 if cells[i-1] == cells[i+1] else 0
            cells = new_cells               # 更新为新一天的状态
        return cells
```

#### 复杂度

- **时间复杂度**：`O(n)`（实际是 `8·n`，因为每一天只遍历 8 次）  
  > 当 `n` 很大时，这个算法会花很久——比如 `n = 10^9`，相当于要执行十亿次循环。

- **空间复杂度**：`O(1)`（只用了常数个长度为 8 的列表）  

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于循环 `n` 次。  
观察题目可以发现：

1. **状态总数有限**：每个格子只有 0/1，两端固定为 0，实际可变的只有中间 6 位。因此所有可能的状态数是 `2^6 = 64` 种。  
2. **一定会出现循环**：如果某一天的状态再次出现，那么之后的状态序列会和之前完全一样，形成一个**环**（循环周期）。一旦找到了环，就可以把 `n` 降到环长度的余数，避免多余的重复计算。

**利用哈希表（字典）记录已经出现过的状态**，并在每一次迭代后检查：

- 若当前状态已经在字典里出现过，说明我们找到了循环的入口和长度。  
- 用 `n % cycle_len` 直接跳到剩余的天数，再进行少量模拟即可。

这一步可以类比为 **“查字典”**：键是状态（我们把 8 位数组转成一个整数），值是该状态出现的第几天。字典就像一本字典，帮我们快速判断“我以前见过这个状态吗？”

**核心技巧**：  
- **状态压缩**：把 `[0,1,0,1,1,0,0,1]` 这 8 位二进制数转换成整数 `0b01011001`（十进制 89），这样可以直接作为字典的键。  
- **循环检测**：使用 `dict` 保存 `state -> day`，一旦发现重复，就得到循环长度 `cycle_len = current_day - first_day`。  
- **余数跳跃**：`n = n % cycle_len`，把天数压缩到不超过循环长度。

#### 代码（Python）

```python
from typing import List

class Solution:
    def prisonAfterNDays(self, cells: List[int], n: int) -> List[int]:
        """
        使用哈希表检测循环，并利用余数跳过冗余的模拟。
        """
        seen = {}                     # state (int) -> 第几天出现
        day = 0

        while n > 0:
            # 把当前的 8 位列表压成一个整数，方便哈希表查找
            state_key = self._to_int(cells)

            if state_key in seen:     # 出现了环
                # 环的长度 = 已走的天数 - 上一次出现该状态时的天数
                cycle_len = day - seen[state_key]
                n %= cycle_len        # 只剩下不到一个环的天数需要模拟
                if n == 0:            # 正好整除，直接返回当前状态
                    break
            else:
                seen[state_key] = day  # 记录第一次出现的天数

            # 进行一天的状态转移
            cells = self._next_day(cells)
            n -= 1
            day += 1

        return cells

    def _next_day(self, cells: List[int]) -> List[int]:
        """按照题目规则计算第二天的监狱状态"""
        new = [0] * 8
        for i in range(1, 7):
            new[i] = 1 if cells[i-1] == cells[i+1] else 0
        return new

    def _to_int(self, cells: List[int]) -> int:
        """把 8 位 0/1 列表压成一个整数，例如 [0,1,0,1,1,0,0,1] -> 89"""
        num = 0
        for bit in cells:
            num = (num << 1) | bit   # 左移一位后加上当前位
        return num
```

> **关键行中文注释** 已经写在代码里，帮助你一步步跟踪思路。

#### 复杂度

- **时间复杂度**：`O(64)` → 实际上是 `O(1)`  
  因为最多只会遍历 `64` 种不同的状态（环的最长长度），不管 `n` 多大，循环检测后最多只需要模拟 64 天。  
  > 与暴力解相比，**从线性 `n` 降到了常数**，即使 `n = 10^9` 也只会跑几百次循环。

- **空间复杂度**：`O(64)` → `O(1)`  
  哈希表最多存 64 条记录，每条记录只保存一个整数键和一天的编号，空间仍然是常数级别。

---

## 心得

- **核心技巧**：**循环检测 + 状态压缩**（把数组转成整数，用哈希表找环）。  
- **适用的题型**：  
  1. “状态机”类题目，如 **“循环数组”**、**“灯泡开关”**（每次翻转相邻灯的状态）  
  2. **“游戏生命演化”**（Game of Life）等需要重复演化的格子问题  
  3. **“循环迭代”** 的数列或字符串转换（如“找循环长度”）  
- **一句话总结解题钥匙**：**“所有状态有限 ⇒ 必有循环 ⇒ 用哈希表快速跳过多余的循环”。**

---

## 反思

- **第一反应**：直接写一个循环模拟每一天，代码好写但会超时。  
- **最容易踩的坑**：  
  - 忘记把首尾格子固定为 0，导致结果错误。  
  - 循环检测后忘记对剩余天数 `n` 再做一次 `while n > 0` 的模拟，直接返回错误的中间状态。  
  - 状态压缩时位移顺序写反，导致相同的数组映射成不同的整数。  
- **下次遇到同类题**，第一步应该先 **思考状态空间是否有限**，如果是，就立刻考虑 **哈希表记录出现的状态**，寻找循环周期，再用 **取模** 把大 `n` 缩小到可接受的范围。