# #2059. 最小操作次数使数字转换 / Minimum Operations to Convert Number

> 难度：中等 · 标签：Array、Breadth-First Search · [LeetCode 链接](https://leetcode.com/problems/minimum-operations-to-convert-number/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums containing distinct numbers, an integer start, and an integer goal. There is an integer x that is initially set to start, and you want to perform operations on x such that it is converted to goal. You can perform the following operation repeatedly on the number x:
If 0 <= x <= 1000, then for any index i in the array (0 <= i < nums.length), you can set x to any of the following:
Note that you can use each nums[i] any number of times in any order. Operations that set x to be out of the range 0 <= x <= 1000 are valid, but no more operations can be done afterward.
Return the minimum number of operations needed to convert x = start into goal, and -1 if it is not possible.

**Examples**

**Example 1:**

```
Input: nums = [2,4,12], start = 2, goal = 12
Output: 2
Explanation: We can go from 2 → 14 → 12 with the following 2 operations.
- 2 + 12 = 14
- 14 - 2 = 12
```

**Example 2:**

```
Input: nums = [3,5,7], start = 0, goal = -4
Output: 2
Explanation: We can go from 0 → 3 → -4 with the following 2 operations. 
- 0 + 3 = 3
- 3 - 7 = -4
Note that the last operation sets x out of the range 0 <= x <= 1000, which is valid.
```

**Example 3:**

```
Input: nums = [2,8,16], start = 0, goal = 1
Output: -1
Explanation: There is no way to convert 0 into 1.
```

**Constraints**

- 1 <= nums.length <= 1000
- -109 <= nums[i], goal <= 109
- 0 <= start <= 1000
- start != goal
- All the integers in nums are distinct.

---

## 题目（中文翻译）

**题目描述**

给定一个下标从 0 开始的整数数组 `nums`，其中的元素互不相同；再给定两个整数 `start` 和 `goal`。现在有一个整数 `x`，初始值为 `start`，需要通过若干次操作把 `x` 转换为 `goal`。

你可以对当前的 `x` 重复执行以下操作：

- 若 `0 ≤ x ≤ 1000`，则对于数组 `nums` 中的任意下标 `i`（`0 ≤ i < nums.length`），可以将 `x` 设为以下三种结果中的任意一种：
  1. `x + nums[i]`
  2. `x - nums[i]`
  3. `x ^ nums[i]`（位异或，XOR）

> 注意：`nums[i]` 可以被使用任意次数，顺序自由。若某次操作使得 `x` 超出区间 `0 ≤ x ≤ 1000`，该操作仍然有效，但之后不能再进行任何操作。

返回将 `x = start` 转换为 `goal` 所需的最少操作次数；如果无法完成则返回 `-1`。

---

**示例**

**示例 1**

```
Input: nums = [2,4,12], start = 2, goal = 12
Output: 2
Explanation: 我们可以通过以下 2 步完成转换：
- 2 + 12 = 14
- 14 - 2 = 12
```

**示例 2**

```
Input: nums = [3,5,7], start = 0, goal = -4
Output: 2
Explanation: 我们可以通过以下 2 步完成转换：
- 0 + 3 = 3
- 3 - 7 = -4
注意，最后一步把 x 设为 -4，超出了区间 0 ≤ x ≤ 1000，这仍然是合法的。
```

**示例 3**

```
Input: nums = [2,8,16], start = 0, goal = 1
Output: -1
Explanation: 没有任何办法把 0 转换为 1。
```

---

**约束条件**

- `1 ≤ nums.length ≤ 1000`
- `-10^9 ≤ nums[i], goal ≤ 10^9`
- `0 ≤ start ≤ 1000`
- `start != goal`
- `nums` 中的所有整数互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题的本质是：**从 start 出发，每一步可以把当前数 x 与数组 `nums` 中的任意元素做三种运算**  

* `x + nums[i]`  
* `x - nums[i]`  
* `x ^ nums[i]`（按位异或）  

得到的新数如果仍在 `[0, 1000]` 区间，就可以继续往下走；一旦跑到区间外，就只能停在那儿。我们要找的，是 **最少的操作次数** 能让 `x` 变成 `goal`。

把每一个可能的数（0~1000）想象成图中的一个节点，三种运算就是从一个节点到另一些节点的无向边，且每条边的权值都是 1。于是“最少操作次数”就等价于 **从 start 节点到 goal 节点的最短路径长度**。

最直接、最“暴力”的做法是 **广度优先搜索（BFS）**：

1. 用一个队列保存“待访问的状态”，每次弹出一个 `x`，并记录已经用了几步。  
2. 对当前 `x`，遍历所有 `nums[i]`，生成 `x+nums[i]、x-nums[i]、x^nums[i]` 三个新数。  
3. 如果新数正好等于 `goal`，返回当前步数 + 1。  
4. 若新数在 `[0,1000]` 且 **未被访问过**，把它加入队列继续搜索。  
5. 当队列为空仍未找到 `goal`，说明不可达，返回 `-1`。

> **类比**：想象你在一座城市里，街道是“+、-、^”三种操作，交叉口是 0~1000 之间的整数。BFS 就像在每个交叉口同时派出多支小队向四周探索，最先到达目标的那支小队走的路程就是最少步数。

#### 代码（Python）

```python
from collections import deque
from typing import List

def minimumOperations(nums: List[int], start: int, goal: int) -> int:
    # visited[i] 表示数 i（0 <= i <= 1000）是否已经加入队列
    visited = [False] * 1001
    q = deque()
    q.append((start, 0))          # (当前数 x, 已使用的步数)
    if 0 <= start <= 1000:
        visited[start] = True

    while q:
        x, step = q.popleft()

        # 对每个 nums[i] 进行三种可能的运算
        for v in nums:
            for nxt in (x + v, x - v, x ^ v):
                # 已经到达目标，返回步数 + 1
                if nxt == goal:
                    return step + 1

                # 只把仍在合法区间且未访问过的数放进队列
                if 0 <= nxt <= 1000 and not visited[nxt]:
                    visited[nxt] = True
                    q.append((nxt, step + 1))

    # BFS 结束仍未找到 goal，说明不可达
    return -1
```

*关键注释已用中文标注，代码可直接运行。*

#### 复杂度

- **时间复杂度**：`O(1001 * len(nums))`  
  - 队列里最多会出现 0~1000 共 1001 个不同的状态（因为一旦访问过就不会再入队），每次弹出时要遍历全部 `nums[i]` 并产生 3 条边，故总体是 `1001 * len(nums)` 的量级。  
  - 用“大白话”说，就是**最多检查一千多个数字，每个数字最多检查一千次**，所以算得很快。

- **空间复杂度**：`O(1001)`  
  - `visited` 数组和队列最多同时保存 0~1000 之间的状态，约一千个布尔值/整数，空间开销非常小。

---

### 2. 最优解

#### 思路  

在本题的搜索空间里，**所有合法的状态已经被限制在 `[0,1000]`**，而 BFS 正好能够在 **无权图** 中找到最短路径。事实上，上面的“暴力解”已经是最优的时间复杂度了——没有比遍历所有可能状态更快的办法，因为我们必须保证找不到更短的路径时才返回 `-1`。

不过我们可以在实现细节上再“拔高”一点，让代码更简洁、运行更快：

1. **一次性生成三条边**：把 `+、-、^` 三种运算放进同一个循环里，减少嵌套层数。  
2. **提前判断 start 是否已经等于 goal**（虽然题目保证 `start != goal`，但写成通用模板更安全）。  
3. **使用 `set` 而非列表记录已访问的数**，在 Python 中 `set` 的 `O(1)` 查找常数更小（对 1000 规模差别不大，但写法更直观）。  

核心仍是 **BFS**，因为它天然保证“层层递进”，第一次遇到 `goal` 时一定是最少步数。

#### 代码（Python）

```python
from collections import deque
from typing import List

def minimumOperations(nums: List[int], start: int, goal: int) -> int:
    # 若起点已经是目标（题目说不会出现，但写成通用模板更稳妥）
    if start == goal:
        return 0

    visited = set()                 # 已经遍历过的合法数
    q = deque([(start, 0)])         # (当前数, 已使用的步数)

    while q:
        x, step = q.popleft()
        for v in nums:
            # 统一写成一个列表，便于一次遍历三种运算
            for nxt in (x + v, x - v, x ^ v):
                if nxt == goal:               # 第一次碰到 goal 必然是最短路径
                    return step + 1

                if 0 <= nxt <= 1000 and nxt not in visited:
                    visited.add(nxt)
                    q.append((nxt, step + 1))

    # 所有可达状态都遍历完仍未找到 goal
    return -1
```

#### 复杂度

- **时间复杂度**：`O(1001 * len(nums))`，与暴力解相同，只是实现更紧凑。  
  - 这里的 “最优” 体现在 **没有多余的重复遍历**，每个合法数只进入队列一次。

- **空间复杂度**：`O(1001)`，使用 `set` 记录已访问的数，同样最多保存 0~1000 之间的状态。

---

## 心得

- **核心技巧**：**广度优先搜索（BFS）** 用来在“状态图”中寻找最短转换步数。  
- **适用的题型**：  
  1. “最少步数把数字变成目标”类（如 LeetCode 127、1307）。  
  2. “在有限状态空间内的最短路径”类（如迷宫最短路、八数码问题的 BFS 版）。  
- **一句话总结**：**把每一次合法的数值变化看成图中的一条边，用 BFS 保证第一次到达目标的路径即为最少操作数**。

---

## 反思

- **第一反应**：看到“可以反复对 x 进行 +、-、^ 操作”，立刻想到把所有可能的数当成节点，用 BFS 逐层展开。  
- **最容易踩的坑**：  
  - 忘记 **“超出 0~1000 范围后不能再继续”**，导致无限扩散。  
  - 忽视 **负数或大于 1000 的中间结果仍可能是最终答案**（因为只要一次操作后直接等于 goal 即可）。  
  - 没有做好 **visited 去重**，会出现同一个数被反复加入队列，导致时间爆炸。  
- **下次类似题的第一步**：先确认 **状态空间的大小**（本题是 0~1000），若足够小，就直接用 BFS；若更大，再考虑双向 BFS、启发式搜索或 DP。