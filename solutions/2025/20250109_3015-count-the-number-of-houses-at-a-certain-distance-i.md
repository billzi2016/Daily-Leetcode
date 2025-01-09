# #3015. **统计一定距离的房屋对数 I** / Count the Number of Houses at a Certain Distance I

> 难度：中等 · 标签：Breadth-First Search、Graph、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/count-the-number-of-houses-at-a-certain-distance-i/)

---

## 题目（英文原版）

**Description**

You are given three positive integers n, x, and y.
In a city, there exist houses numbered 1 to n connected by n streets. There is a street connecting the house numbered i with the house numbered i + 1 for all 1 <= i <= n - 1 . An additional street connects the house numbered x with the house numbered y.
For each k, such that 1 <= k <= n, you need to find the number of pairs of houses (house1, house2) such that the minimum number of streets that need to be traveled to reach house2 from house1 is k.
Return a 1-indexed array result of length n where result[k] represents the total number of pairs of houses such that the minimum streets required to reach one house from the other is k.
Note that x and y can be equal.

**Examples**

**Example 1:**

```
Input: n = 3, x = 1, y = 3
Output: [6,0,0]
Explanation: Let's look at each pair of houses:
- For the pair (1, 2), we can go from house 1 to house 2 directly.
- For the pair (2, 1), we can go from house 2 to house 1 directly.
- For the pair (1, 3), we can go from house 1 to house 3 directly.
- For the pair (3, 1), we can go from house 3 to house 1 directly.
- For the pair (2, 3), we can go from house 2 to house 3 directly.
- For the pair (3, 2), we can go from house 3 to house 2 directly.
```

**Example 2:**

```
Input: n = 5, x = 2, y = 4
Output: [10,8,2,0,0]
Explanation: For each distance k the pairs are:
- For k == 1, the pairs are (1, 2), (2, 1), (2, 3), (3, 2), (2, 4), (4, 2), (3, 4), (4, 3), (4, 5), and (5, 4).
- For k == 2, the pairs are (1, 3), (3, 1), (1, 4), (4, 1), (2, 5), (5, 2), (3, 5), and (5, 3).
- For k == 3, the pairs are (1, 5), and (5, 1).
- For k == 4 and k == 5, there are no pairs.
```

**Example 3:**

```
Input: n = 4, x = 1, y = 1
Output: [6,4,2,0]
Explanation: For each distance k the pairs are:
- For k == 1, the pairs are (1, 2), (2, 1), (2, 3), (3, 2), (3, 4), and (4, 3).
- For k == 2, the pairs are (1, 3), (3, 1), (2, 4), and (4, 2).
- For k == 3, the pairs are (1, 4), and (4, 1).
- For k == 4, there are no pairs.
```

**Constraints**

- 2 <= n <= 100
- 1 <= x, y <= n

---

## 题目（中文翻译）

给定三个正整数 `n`、`x` 和 `y`。  
在一座城市中，有编号为 `1` 到 `n` 的房屋，且它们之间通过 `n` 条街道相连。对于所有 `1 ≤ i ≤ n‑1`，都有一条街道把编号为 `i` 的房屋与编号为 `i+1` 的房屋相连。除此之外，还有一条额外的街道把编号为 `x` 的房屋与编号为 `y` 的房屋相连（`x` 和 `y` 可能相等）。

对于每个满足 `1 ≤ k ≤ n` 的整数 `k`，求满足以下条件的房屋对 `(house1, house2)` 的数量：从 `house1` 到 `house2` 所需经过的最少街道数恰好为 `k`。  

返回一个 **1 索引**（1-indexed）的数组 `result`，其长度为 `n`，其中 `result[k]` 表示最少需要走 `k` 条街道即可从一栋房屋到达另一栋房屋的所有有序房屋对的总数。

> 注意：`x` 与 `y` 可以相等。

---

### 示例

**示例 1**

```
Input: n = 3, x = 1, y = 3
Output: [6,0,0]
```

**Explanation（解释）**：逐个枚举所有房屋对：

- 对于 `(1, 2)`，可以直接走一条街道到达。
- 对于 `(2, 1)`，同上。
- 对于 `(1, 3)`，可以直接走额外的那条街道到达。
- 对于 `(3, 1)`，同上。
- 对于 `(2, 3)`，可以直接走一条街道到达。
- 对于 `(3, 2)`，同上。

其余距离均不存在对应的房屋对，因此结果为 `[6,0,0]`。

---

**示例 2**

```
Input: n = 5, x = 2, y = 4
Output: [10,8,2,0,0]
```

**Explanation（解释）**：

- `k == 1` 时的房屋对有  
  `(1,2)`, `(2,1)`, `(2,3)`, `(3,2)`, `(2,4)`, `(4,2)`, `(3,4)`, `(4,3)`, `(4,5)`, `(5,4)`，共 10 对。
- `k == 2` 时的房屋对有  
  `(1,3)`, `(3,1)`, `(1,4)`, `(4,1)`, `(2,5)`, `(5,2)`, `(3,5)`, `(5,3)`，共 8 对。
- `k == 3` 时的房屋对有  
  `(1,5)`, `(5,1)`，共 2 对。
- `k == 4` 与 `k == 5` 时没有符合条件的房屋对。

---

**示例 3**

```
Input: n = 4, x = 1, y = 1
Output: [6,4,2,0]
```

**Explanation（解释）**：

- `k == 1` 的房屋对有  
  `(1,2)`, `(2,1)`, `(2,3)`, `(3,2)`, `(3,4)`, `(4,3)`，共 6 对。
- `k == 2` 的房屋对有  
  `(1,3)`, `(3,1)`, `(2,4)`, `(4,2)`，共 4 对。
- `k == 3` 的房屋对有  
  `(1,4)`, `(4,1)`，共 2 对。
- `k == 4` 时没有符合条件的房屋对。

---

### 约束条件

- `2 ≤ n ≤ 100`
- `1 ≤ x, y ≤ n`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

这座城市的道路可以抽象成 **无向图**：  
- **节点** 是房子 `1 … n`。  
- **普通道路** 把相邻的房子 `i` 与 `i+1` 连在一起，形成一条**直线**。  
- **特殊道路** 把房子 `x` 与 `y` 再多连一条边（如果 `x==y`，这条边其实是自环，等价于没有额外影响）。

我们要统计 **有序对** `(house1, house2)` 的最短路径长度（走的最少街道数）等于 `k` 的个数，`k` 从 `1` 到 `n`。

最直接的办法就是 **对每个起点**，用 **BFS（广度优先搜索）** 求出它到所有其他房子的最短距离，然后把得到的距离放进统计表。  
- BFS 的核心思想类似“在地图上找最短路径”，它会一次层层向外扩散，保证第一次到达某个节点时的步数就是最短距离。  
- 这里的 **队列** 好比我们排队叫号，每一次出队相当于“走一步”。  

因为 `n ≤ 100`，最多只会有 `100` 个起点，每次 BFS 访问 `n` 条边，时间开销完全可以接受。

**为什么正确**  
BFS 在 **无权图**（每条边代价相同）里恰好返回**最短路径长度**。我们的图每条街道都算作走一步，所以 BFS 正好符合题意。

**时间/空间复杂度**  
- **时间**：对每个起点做一次 BFS，`n` 次 BFS，每次遍历 `O(n)` 条边 → `O(n²)`。  
  用大白话说，就是如果 `n=100`，最多要算 10 000 次“走几步”。  
- **空间**：需要保存一个 `n` 长的距离数组和一个队列，都是 `O(n)`。  

#### 代码（Python）

```python
from collections import deque
from typing import List

def countPairs_bruteforce(n: int, x: int, y: int) -> List[int]:
    # 结果数组，result[k] 统计距离恰好等于 k+1 的有序对数（1-indexed）
    result = [0] * n          # Python 用 0-index，最后直接返回

    # 把特殊道路加入邻接表（无向图）
    # adj[i] 保存所有和 i 相连的房子编号（1-indexed）
    adj = [[] for _ in range(n + 1)]
    for i in range(1, n):          # 直线道路
        adj[i].append(i + 1)
        adj[i + 1].append(i)
    # 额外道路（如果 x==y，下面两行会把同一个节点加两次，后面 BFS 仍然是正确的）
    adj[x].append(y)
    adj[y].append(x)

    # 对每个起点做 BFS
    for start in range(1, n + 1):
        dist = [-1] * (n + 1)      # -1 表示未访问
        q = deque()
        q.append(start)
        dist[start] = 0           # 起点到自己的距离是 0

        while q:
            cur = q.popleft()
            for nxt in adj[cur]:
                if dist[nxt] == -1:          # 只访问一次，保证是最短距离
                    dist[nxt] = dist[cur] + 1
                    q.append(nxt)

        # 统计从 start 出发到所有 other 的距离
        for other in range(1, n + 1):
            if other == start:
                continue            # 题目要求的是两个不同的房子
            d = dist[other]         # d 必然在 1..n-1 之间
            result[d - 1] += 1      # 结果数组是 0-index，故减 1

    return result
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 直观解释：我们把每栋房子都当作“出发点”，对每个出发点遍历所有街道一次，等价于在一个 `n×n` 的格子里填数。  
- **空间复杂度**：`O(n)`  
  - 只用了 `adj`（邻接表）和 `dist` 两个长度为 `n` 的数组，随 `n` 线性增长。

---

### 2. 最优解  

#### 思路  

暴力解的 **瓶颈** 在于我们对每个起点都重复做 BFS，虽然 `n` 很小，但我们可以利用 **图的特殊结构**（一条直线 + 一条额外的跨线边）直接算出两点之间的最短距离，进而在 **`O(n²)` → `O(n)`**（或 `O(n log n)`）的时间内完成计数。

**关键观察**  

任意两栋房子 `i` 与 `j`（`i < j`）的最短距离只有三种可能：

1. **沿直线走**：`|i - j|`  
2. **先走到 `x`，跨过特殊道路到 `y`，再走到 `j`**：`|i - x| + 1 + |y - j|`  
3. **先走到 `y`，跨过特殊道路到 `x`，再走到 `j`**：`|i - y| + 1 + |x - j|`

因为所有道路的权重都是 `1`，所以最短距离就是这三者的 **最小值**：

```
dist(i, j) = min( |i-j|,
                  |i-x| + 1 + |y-j|,
                  |i-y| + 1 + |x-j| )
```

> **类比**：想象城里有一条“快递专线”只能在 `x ↔ y` 两点之间使用，平时只能走普通街道。两点之间的最快路线，就是在三条候选路线里挑最短的那条。

于是我们只要遍历所有 **无序对** `(i, j)`（`i < j`），算出上述最小值，然后把它记到结果数组中（因为题目要求有序对，所以最后乘以 `2`）。

**如何把遍历降到 `O(n)`？**  

注意到 `|i-j|` 是 **线性递增** 的函数，而另外两条式子在 `i` 固定、`j` 增大时也是单调的。我们可以利用 **前缀计数**（或双指针）一次性统计每个距离出现的次数：

1. 先统计仅使用 **直线** 的配对数量。对每个距离 `d`（`1 ≤ d ≤ n-1`），有 `n-d` 对 `(i, i+d)`，所以直线贡献是 `2*(n-d)`（乘以 2 因为有序对）。
2. 再考虑 **经过特殊道路** 的配对。  
   - 设 `a = min(x, y)`，`b = max(x, y)`。  
   - 当 `i ≤ a` 且 `j ≥ b` 时，走 `i → a → b → j` 这条跨线路径会比直线更短。具体距离是 `(a-i) + 1 + (j-b) = (j-i) - (b-a) + 1`。  
   - 类似地，当 `i ≥ a` 且 `j ≤ b` 时，走 `i → b → a → j` 会更短。  
   - 这两种情况对应的 **区间** 可以用 **双指针** 或 **前缀和** 快速统计。

下面给出一种更直观的 **枚举** 方法：遍历 `i`，把 `j` 分成三段（左侧、右侧、跨过 `x,y`），每段的距离公式是线性的，直接累计到对应的 `result` 索引。因为每次只遍历一次 `j`，整体是 `O(n²)` 的常数更小版；但在 `n ≤ 100` 时已经足够快。这里我们把 **实现简化为 O(n²) 但只算一次距离**（不做 BFS），这样时间从 `O(n³)` 降到 `O(n²)`，对大多数语言仍然是“最优”。  

> **说明**：LeetCode 官方的最优解也是 `O(n²)`，因为要统计所有 `n·(n-1)` 对，时间下界就是 `Θ(n²)`。我们这里的优化是 **去掉 BFS 的额外 `O(n)` 因子**，直接用公式算距离。

#### 代码（Python）

```python
from typing import List

def countPairs_optimal(n: int, x: int, y: int) -> List[int]:
    """
    直接用公式计算两点之间的最短距离，时间 O(n^2)，空间 O(n)。
    结果 result[k] 表示距离恰好等于 k+1 的有序对数（1-indexed）。
    """
    result = [0] * n          # 0 .. n-1  对应距离 1 .. n

    # 预先把 x, y 排序，方便后面统一讨论
    a, b = min(x, y), max(x, y)

    # 遍历所有无序对 (i, j) ，i < j
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            # 直线距离
            d1 = j - i

            # 经过 (x, y) 的两种可能
            d2 = abs(i - x) + 1 + abs(y - j)
            d3 = abs(i - y) + 1 + abs(x - j)

            # 取最小值
            dist = min(d1, d2, d3)

            # 把有序对计数加 2（i->j 和 j->i）
            result[dist - 1] += 2

    return result
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 直观解释：我们只遍历所有房子对一次（`n·(n-1)/2` 次），每次用常数时间算三个表达式并取最小值。  
  - 与暴力 BFS 的 `O(n²)` 同阶，但省掉了每次 BFS 中的队列操作，实际跑得更快。  
- **空间复杂度**：`O(n)`  
  - 只用了结果数组 `result`（长度 `n`）以及几个临时整数。

---

## 心得  

- **核心技巧**：利用图的结构把最短路径转化为**三条显式公式**的最小值，从而避免 BFS。  
- **适用场景**：  
  1. **线性图 + 少量额外边**（如“树上加一条额外边”）。  
  2. **一维坐标系中的最短路径**（如“环形道路 + 短路”）。  
  3. **需要统计所有点对距离的题目**（如 LeetCode 1722 “Minimize Hamming Distance After Swap Operations” 中的距离计数思路）。  
- **一句话总结**：**把图的最短路“手写”成公式，直接算距离，省去遍历搜索**。

---

## 反思  

- **第一反应**：看到“最短街道数”，立刻想到 BFS，毕竟 BFS 是无权图的最短路万能解。  
- **最容易踩的坑**：  
  - **自环**（`x == y`）会导致额外边其实不产生任何新路径，公式仍然适用，但要确保不把 `+1` 误写成 `+0`。  
  - **有序对** vs **无序对**：统计完后一定要乘以 `2`（除去 `(i,i)`），否则答案会只有一半。  
  - **下标偏移**：结果数组是 **1-indexed**，但 Python 使用 **0-index**，记得在写入时 `dist-1`。  
- **下次类似**：遇到“线性结构 + 少量跨线边”的最短路计数时，第一步就尝试**写出所有可能的路径长度公式**，再取最小值，而不是直接跑 BFS。这样既能理清思路，又能写出更高效的代码。