# #2037. 让每个人坐下的最少移动次数 / Minimum Number of Moves to Seat Everyone

> 难度：简单 · 标签：Array、Greedy、Sorting、Counting Sort · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-moves-to-seat-everyone/)

---

## 题目（英文原版）

**Description**

There are n availabe seats and n students standing in a room. You are given an array seats of length n, where seats[i] is the position of the ith seat. You are also given the array students of length n, where students[j] is the position of the jth student.
You may perform the following move any number of times:
Return the minimum number of moves required to move each student to a seat such that no two students are in the same seat.
Note that there may be multiple seats or students in the same position at the beginning.

**Examples**

**Example 1:**

```
Input: seats = [3,1,5], students = [2,7,4]
Output: 4
Explanation: The students are moved as follows:
- The first student is moved from position 2 to position 1 using 1 move.
- The second student is moved from position 7 to position 5 using 2 moves.
- The third student is moved from position 4 to position 3 using 1 move.
In total, 1 + 2 + 1 = 4 moves were used.
```

**Example 2:**

```
Input: seats = [4,1,5,9], students = [1,3,2,6]
Output: 7
Explanation: The students are moved as follows:
- The first student is not moved.
- The second student is moved from position 3 to position 4 using 1 move.
- The third student is moved from position 2 to position 5 using 3 moves.
- The fourth student is moved from position 6 to position 9 using 3 moves.
In total, 0 + 1 + 3 + 3 = 7 moves were used.
```

**Example 3:**

```
Input: seats = [2,2,6,6], students = [1,3,2,6]
Output: 4
Explanation: Note that there are two seats at position 2 and two seats at position 6.
The students are moved as follows:
- The first student is moved from position 1 to position 2 using 1 move.
- The second student is moved from position 3 to position 6 using 3 moves.
- The third student is not moved.
- The fourth student is not moved.
In total, 1 + 3 + 0 + 0 = 4 moves were used.
```

**Constraints**

- n == seats.length == students.length
- 1 <= n <= 100
- 1 <= seats[i], students[j] <= 100

---

## 题目（中文翻译）

**描述**  
有 `n` 个可用的座位（seat）和 `n` 名站在教室里的学生（student）。给定长度为 `n` 的数组 `seats`，其中 `seats[i]` 表示第 `i` 个座位的**位置 (position)**。同样，给定长度为 `n` 的数组 `students`，其中 `students[j]` 表示第 `j` 名学生的**位置 (position)**。  

你可以无限次执行以下操作：将任意一名学生向左或向右移动 1 个单位的距离（即一次**移动 (move)**）。  

返回使每位学生坐到一个座位上且没有两名学生坐在同一座位所需的**最小移动次数**。注意，初始时可能存在多个座位或多个学生位于同一位置。

**示例 1**  
```
Input: seats = [3,1,5], students = [2,7,4]
Output: 4
Explanation: 学生的移动过程如下：
- 第 1 名学生从位置 2 移动到位置 1，使用 1 次移动。
- 第 2 名学生从位置 7 移动到位置 5，使用 2 次移动。
- 第 3 名学生从位置 4 移动到位置 3，使用 1 次移动。
总计 1 + 2 + 1 = 4 次移动。
```

**示例 2**  
```
Input: seats = [4,1,5,9], students = [1,3,2,6]
Output: 7
Explanation: 学生的移动过程如下：
- 第 1 名学生保持不动。
- 第 2 名学生从位置 3 移动到位置 4，使用 1 次移动。
- 第 3 名学生从位置 2 移动到位置 5，使用 3 次移动。
- 第 4 名学生从位置 6 移动到位置 9，使用 3 次移动。
总计 0 + 1 + 3 + 3 = 7 次移动。
```

**示例 3**  
```
Input: seats = [2,2,6,6], students = [1,3,2,6]
Output: 4
Explanation: 注意有两个座位位于位置 2，两个座位位于位置 6。学生的移动过程如下：
- 第 1 名学生从位置 1 移动到位置 2，使用 1 次移动。
- 第 2 名学生从位置 3 移动到位置 6，使用 3 次移动。
- 第 3 名学生保持不动。
- 第 4 名学生保持不动。
总计 1 + 3 + 0 + 0 = 4 次移动。
```

**约束条件**  
- `n == seats.length == students.length`
- `1 <= n <= 100`
- `1 <= seats[i], students[j] <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每个学生安排到每个座位的所有可能组合都尝试一遍**，找出移动次数最少的那种安排。  

- **数据结构**：我们可以把座位位置 `seats` 看成一本“座位字典”，把学生位置 `students` 看成一本“学生字典”。  
- **暴力做法**：列出所有 `n!`（n 的阶乘）种学生到座位的对应关系（即全排列），对每一种对应关系计算总移动步数 `|seat - student|` 的和，取最小值。  
- **为什么正确**：因为我们穷举了所有合法的“一对一配对”，必然会包含最优配对，最小的总移动步数自然就是答案。  

> **注意**：`n!` 在 `n=100` 时是天文数字，根本不可算。但在学习阶段，先写出这种“完整搜索”可以帮助我们理解“配对”本身的本质。

#### 代码（Python）

```python
import itertools
from typing import List

def minMovesBruteForce(seats: List[int], students: List[int]) -> int:
    """
    暴力枚举所有学生与座位的匹配方式，返回最小移动次数。
    只适用于 n 很小的情况（比如 n <= 8），因为排列数会爆炸。
    """
    n = len(seats)
    ans = float('inf')                     # 用一个很大的数保存当前最小值

    # itertools.permutations 会生成 seats 的所有排列（即所有配对方式）
    for perm in itertools.permutations(seats):
        # 计算当前排列对应的总移动步数
        total = 0
        for i in range(n):
            total += abs(perm[i] - students[i])   # |座位位置 - 学生位置|
        ans = min(ans, total)                     # 取最小值

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n! * n)`  
  - `n!` 是所有排列的数量，`* n` 是遍历每个排列时计算距离的代价。  
  - 用大白话说，就是“先把所有可能的配对写出来（数量会非常多），再一个一个算”。  
- **空间复杂度**：`O(n)`  
  - 只用了几个长度为 `n` 的列表来存数据，额外的递归栈深度与 `n` 成正比。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**配对的顺序**直接影响总距离。我们要找一种配对方式，使每一次配对的距离都尽可能小。  

**慢在哪里**  
- 暴力解把所有可能都尝试了一遍，根本没有利用“位置”本身的大小信息。  
- 实际上，**把左边最左的学生送到左边最左的座位**，再把次左的学生送到次左的座位……，这样每一次的距离都是局部最小的，整体也会是全局最小的。  

**为什么“最左配最左”是最优的？**  
可以用**交换论证**来说明：  
- 假设我们有两个学生 `a < b`（位置更左）和两个座位 `x < y`。  
- 如果我们把 `a` 配给 `y`、`b` 配给 `x`，总距离是 `|a-y| + |b-x|`。  
- 把 `a` 配给 `x`、`b` 配给 `y`，总距离是 `|a-x| + |b-y|`。  
- 由于 `a ≤ b` 且 `x ≤ y`，可以证明 `|a-x| + |b-y| ≤ |a-y| + |b-x|`（把两边的绝对值展开后会出现非负的差值），即**不交叉配对**永远不比交叉配对好。  
- 递归地把所有学生和座位排序后，两两对应，就不会出现“交叉配对”，所以得到的总距离就是最小的。

**核心算法**：**排序 + 贪心配对**  
1. 把 `seats` 排序（从小到大）。  
2. 把 `students` 排序（从小到大）。  
3. 对每个下标 `i`，让第 `i` 位学生坐到第 `i` 位座位，累计 `abs(seats[i] - students[i])`。  

**为什么排序能在 O(n log n) 完成**  
- Python 内置的 `list.sort()` 使用的是 Timsort，时间复杂度是 `O(n log n)`，在本题的 `n ≤ 100` 完全够快。  

#### 代码（Python）

```python
from typing import List

def minMovesGreedy(seats: List[int], students: List[int]) -> int:
    """
    贪心算法：先把座位和学生的位置都排好序，然后两两对应。
    时间复杂度 O(n log n)，空间复杂度 O(1)（不计输入数组本身）。
    """
    # 1. 排序
    seats.sort()          # 小到大排列，类似把座位排成一条直线
    students.sort()       # 同理，把学生排成一条直线

    # 2. 两两配对，累计移动步数
    total_moves = 0
    for s, stu in zip(seats, students):
        total_moves += abs(s - stu)   # 计算当前学生到对应座位的距离

    return total_moves
```

#### 复杂度

- **时间复杂度**：`O(n log n)` — 主要花在对两个长度为 `n` 的数组排序上。  
  - 与暴力解的 `n!` 相比，`log n` 只是在“把东西排好序”时的轻微额外工作，几乎可以忽略不计。  
- **空间复杂度**：`O(1)` （如果不计输入数组本身）— 只用了常数个额外变量；排序在原数组上原地进行，不需要额外的辅助数组。  

---

## 心得

- **核心技巧**：**排序 + 贪心配对**（也叫“最小匹配”）。  
- **适用的题型**：  
  1. “分配任务/机器/房间”等需要“一对一匹配且代价是绝对差” 的问题（如 LeetCode 1637. 双向链表最小移动次数）。  
  2. “最小化总距离” 类的匹配问题，例如“最小化搬家距离”“配对骑士和马匹”。  
- **解题钥匙**：**把两组数排好序，再对应相配**——不交叉配对必然最优。

---

## 反思

- **第一反应**：看到“移动步数 = 位置差的绝对值”，立刻想到**距离最小化**，于是想到**排序**。  
- **最容易踩的坑**：  
  - 忽视**重复位置**（多个座位或学生在同一点），但排序后仍然可以正确配对。  
  - 忘记取绝对值 `abs`，导致负数出现错误的总和。  
  - 对于极端情况（`n=1`）也要返回正确的 `|seat - student|`。  
- **下次类似题的第一步**：先**判断代价函数是否满足“单调”或“绝对差”**，如果是，就考虑**排序后逐位配对**的贪心策略。