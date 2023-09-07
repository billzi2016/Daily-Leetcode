# #2392. 构造满足条件的矩阵 / Build a Matrix With Conditions

> 难度：困难 · 标签：Array、Graph、Topological Sort、Matrix · [LeetCode 链接](https://leetcode.com/problems/build-a-matrix-with-conditions/)

---

## 题目（英文原版）

**Description**

You are given a positive integer k. You are also given:
The two arrays contain integers from 1 to k.
You have to build a k x k matrix that contains each of the numbers from 1 to k exactly once. The remaining cells should have the value 0.
The matrix should also satisfy the following conditions:
Return any matrix that satisfies the conditions. If no answer exists, return an empty matrix.

**Examples**

**Example 1:**

```
Input: k = 3, rowConditions = [[1,2],[3,2]], colConditions = [[2,1],[3,2]]
Output: [[3,0,0],[0,0,1],[0,2,0]]
Explanation: The diagram above shows a valid example of a matrix that satisfies all the conditions.
The row conditions are the following:
- Number 1 is in row 1, and number 2 is in row 2, so 1 is above 2 in the matrix.
- Number 3 is in row 0, and number 2 is in row 2, so 3 is above 2 in the matrix.
The column conditions are the following:
- Number 2 is in column 1, and number 1 is in column 2, so 2 is left of 1 in the matrix.
- Number 3 is in column 0, and number 2 is in column 1, so 3 is left of 2 in the matrix.
Note that there may be multiple correct answers.
```

**Example 2:**

```
Input: k = 3, rowConditions = [[1,2],[2,3],[3,1],[2,3]], colConditions = [[2,1]]
Output: []
Explanation: From the first two conditions, 3 has to be below 1 but the third conditions needs 3 to be above 1 to be satisfied.
No matrix can satisfy all the conditions, so we return the empty matrix.
```

**Constraints**

- 2 <= k <= 400
- 1 <= rowConditions.length, colConditions.length <= 104
- rowConditions[i].length == colConditions[i].length == 2
- 1 <= abovei, belowi, lefti, righti <= k
- abovei != belowi
- lefti != righti

---

## 题目（中文翻译）

给定一个正整数 `k`，以及两个二维数组 `rowConditions` 和 `colConditions`。数组中的每个元素都是长度为 2 的整数对，取值范围为 `[1, k]`。

你的任务是构造一个 `k × k` 的矩阵，使得：

- 矩阵中恰好出现一次 `1` 到 `k` 的每个数字，其余单元格的值为 `0`。
- 对于每个 `rowConditions[i] = [above, below]`，要求数字 `above` 所在的行号 **小于**（即在上方）数字 `below` 的行号。
- 对于每个 `colConditions[i] = [left, right]`，要求数字 `left` 所在的列号 **小于**（即在左侧）数字 `right` 的列号。

返回任意满足上述所有条件的矩阵。如果不存在符合要求的矩阵，返回空矩阵 `[]`。

---

### 示例

**示例 1**

```text
Input: k = 3, rowConditions = [[1,2],[3,2]], colConditions = [[2,1],[3,2]]
Output: [[3,0,0],[0,0,1],[0,2,0]]
Explanation: 上图展示了一个满足所有条件的有效矩阵。
行条件解释如下：
- `[1,2]` 表示数字 1 所在的行在数字 2 之上。
- `[3,2]` 表示数字 3 所在的行在数字 2 之上。
列条件解释如下：
- `[2,1]` 表示数字 2 所在的列在数字 1 之左。
- `[3,2]` 表示数字 3 所在的列在数字 2 之左。
```

**示例 2**

```text
Input: k = 3, rowConditions = [[1,2],[2,3],[3,1],[2,3]], colConditions = [[2,1]]
Output: []
Explanation: 前两个行条件要求 3 在 1 的下方，而第三个行条件要求 3 在 1 的上方，导致冲突。没有矩阵能够同时满足所有条件，故返回空矩阵。
```

---

### 约束

- `2 ≤ k ≤ 400`
- `1 ≤ rowConditions.length, colConditions.length ≤ 10^4`
- `rowConditions[i].length == colConditions[i].length == 2`
- `1 ≤ above_i, below_i, left_i, right_i ≤ k`
- `above_i != below_i`
- `left_i != right_i`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把 **每一个数** 的行位置和列位置都枚举出来，然后检查是否满足所有约束。  
可以把「行约束」`[a, b]` 看成「`a` 必须在 `b` 的上面」；「列约束」`[c, d]` 看成「`c` 必须在 `d` 的左边」。  
如果我们把 `1…k` 的所有排列都列出来（`k!` 种），把其中一种排列当作行顺序、另一种当作列顺序，随后把每个数放到对应的交叉格子里，就能得到一张矩阵。  
只要这张矩阵满足所有约束，就返回它；否则继续尝试下一对排列。

> **类比**：把 `k` 本不同的书排成一排（行顺序）和再排成一排（列顺序），每本书在行排和列排的交叉点上放一本编号相同的书。如果两本书之间有「必须在前面」的关系，就检查排好的顺序是否满足。

**为什么正确**  
因为我们把 **所有可能的行顺序和列顺序** 都穷举了，只要存在合法解，就一定会在某一次枚举中被找到。

**时间/空间复杂度**  
- 枚举所有行排列需要 `k!` 次，列排列同理，组合起来是 `k! × k!`，这在 `k ≤ 400` 时几乎不可能完成。  
- 检查约束只需要遍历 `rowConditions`、`colConditions`，时间是 `O(m)`（`m` 为约束数量）。  
- 空间主要是保存两套排列，`O(k)`。

> **大白话**：`O(k!)` 就像把 `k` 张扑克牌全洗完再排好序，随着 `k` 增大，可能的排列会像天文数字一样爆炸，根本算不完。

#### 代码（Python）

```python
import itertools
from typing import List

def buildMatrix_bruteforce(k: int,
                           rowConditions: List[List[int]],
                           colConditions: List[List[int]]) -> List[List[int]]:
    # 所有可能的行顺序
    for rows in itertools.permutations(range(1, k + 1)):
        # 把行顺序映射为「数 → 行号」
        row_pos = {num: i for i, num in enumerate(rows)}
        # 检查所有行约束是否满足
        ok = True
        for a, b in rowConditions:          # a 必须在 b 的上面
            if row_pos[a] >= row_pos[b]:    # 行号越大表示越往下
                ok = False
                break
        if not ok:
            continue

        # 所有可能的列顺序（外层循环放在这里可以提前剪枝）
        for cols in itertools.permutations(range(1, k + 1)):
            col_pos = {num: i for i, num in enumerate(cols)}
            # 检查列约束
            ok = True
            for a, b in colConditions:      # a 必须在 b 的左边
                if col_pos[a] >= col_pos[b]:
                    ok = False
                    break
            if not ok:
                continue

            # 两套顺序都满足，构造矩阵
            matrix = [[0] * k for _ in range(k)]
            for num in range(1, k + 1):
                r, c = row_pos[num], col_pos[num]
                matrix[r][c] = num
            return matrix

    # 没有任何合法排列
    return []
```

> 代码里每一行都加了中文注释，帮助你对照思路。

#### 复杂度

- **时间复杂度**：`O(k! × k! × (|row| + |col|))` —— 随着 `k` 增大，时间呈阶乘级增长，几乎不可用。
- **空间复杂度**：`O(k)` —— 只保存两套位置映射和结果矩阵（`k²` 只在找到答案时才分配）。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **枚举所有排列**，这一步把时间推到了不可接受的阶乘级。  
观察约束可以发现：

- 行约束只涉及“哪一个数在另一数的上面”，这其实是 **有向图的前后关系**。  
- 列约束同理，只是对应“左‑右”关系。

如果我们把 `1…k` 当作图的节点，`[a, b]`（a 在 b 上面）当作一条从 `a` 指向 `b` 的有向边，那么 **所有行约束** 合起来就是一个 **有向无环图（DAG）**（前提是约束不冲突）。  
对这个 DAG 进行 **拓扑排序**（Topological Sort）即可得到一种合法的行顺序；同理，对列约束进行拓扑排序得到列顺序。

> **类比**：把每个数字想象成一张卡片，卡片之间有“必须在前面/后面”的箭头。把所有箭头排成一个顺序（没有环）就是把卡片排成一列，这正是拓扑排序要做的事。

**关键步骤**：

1. **构建两张有向图**：`row_graph`、`col_graph`。  
2. **拓扑排序**（Kahn 算法）  
   - 统计每个节点的入度（有多少前置条件）。  
   - 把入度为 0 的节点放入队列，逐个弹出并加入结果序列，同时把它指向的节点的入度减 1。  
   - 如果最终得到的序列长度不是 `k`，说明图里有环，约束冲突，直接返回空矩阵。  
3. **根据得到的行顺序和列顺序**，把每个数放到 `matrix[row][col]` 中。  

**为什么正确**  
- 拓扑排序的定义正是 “把所有前置关系全部满足的线性序列”。因此得到的行序列必然满足所有 `rowConditions`，列序列必然满足所有 `colConditions`。  
- 若任意约束冲突，必然在对应的图中形成环，拓扑排序会失败（无法得到完整序列），我们就返回空矩阵，正好符合题意。

**复杂度分析**  
- 构图和计算入度遍历所有约束，时间 `O(|row| + |col|)`。  
- 拓扑排序遍历每个节点一次、每条边一次，仍是 `O(k + |row| + |col|)`。  
- 最终填矩阵是 `O(k)`。  
整体 **时间** 为 `O(k + m)`（`m` 为约束总数），**空间** 为 `O(k + m)`（存图和入度数组）。

> 对比暴力：从阶乘级 `O(k!)` 降到线性级 `O(k + m)`，在 `k ≤ 400`、`m ≤ 10⁴` 的限制下轻松跑完。

#### 代码（Python）

```python
from collections import deque, defaultdict
from typing import List

def topological_sort(k: int, edges: List[List[int]]) -> List[int]:
    """
    Kahn 算法实现的拓扑排序。
    返回一个包含 1..k 的顺序列表；如果出现环则返回空列表。
    """
    graph = defaultdict(list)   # 邻接表：u -> [v1, v2, ...]
    indeg = [0] * (k + 1)        # 入度统计，0 位置不用

    # 建图 + 计算入度
    for u, v in edges:
        graph[u].append(v)
        indeg[v] += 1

    # 所有入度为 0 的节点进入队列
    q = deque([i for i in range(1, k + 1) if indeg[i] == 0])
    order = []                   # 拓扑序列

    while q:
        node = q.popleft()
        order.append(node)
        for nxt in graph[node]:
            indeg[nxt] -= 1      # 删除这条边
            if indeg[nxt] == 0:
                q.append(nxt)

    # 若没有遍历到所有节点，说明有环
    return order if len(order) == k else []

def buildMatrix(k: int,
                rowConditions: List[List[int]],
                colConditions: List[List[int]]) -> List[List[int]]:
    # 1. 拓扑排序得到行顺序、列顺序
    row_order = topological_sort(k, rowConditions)
    col_order = topological_sort(k, colConditions)

    if not row_order or not col_order:      # 任意一个出现环
        return []                           # 空矩阵

    # 2. 把顺序映射为「数 → 行/列索引」
    row_index = {num: i for i, num in enumerate(row_order)}
    col_index = {num: i for i, num in enumerate(col_order)}

    # 3. 按行列索引填充矩阵
    matrix = [[0] * k for _ in range(k)]
    for num in range(1, k + 1):
        r = row_index[num]
        c = col_index[num]
        matrix[r][c] = num

    return matrix
```

**代码要点注释**（已在函数内部添加中文解释）：

- `defaultdict(list)` 把每个节点的所有出边放在一个列表里，类似「每个人的朋友列表」。
- `indeg` 类似「每个人有多少前置任务」；任务为 0 时才能先做（入度为 0 的节点先入队）。
- `deque` 实现的队列保证 **先入先出**，对应 Kahn 算法的 “把可以立刻完成的任务排进去”。

#### 复杂度

- **时间复杂度**：`O(k + |rowConditions| + |colConditions|)`  
  - 解释：我们只遍历每个数字一次（`k`），以及每条约束一次（`|row| + |col|`），没有指数级的枚举。  
  - 与暴力解相比，时间从 `O(k!)` 降到了线性级，几乎可以在毫秒内完成。

- **空间复杂度**：`O(k + |rowConditions| + |colConditions|)`  
  - 用来存储邻接表、入度数组以及行/列映射。`k ≤ 400`，即使约束达到 `10⁴`，也只占几百 KB 的内存。

---

## 心得

- **核心技巧**：把“在上/左”约束抽象为 **有向图**，使用 **拓扑排序** 获得合法的行、列顺序。  
- **适用题型**  
  1. **任务调度**（LeetCode 207）——根据前置任务返回执行顺序。  
  2. **课程表**（LeetCode 210）——判断能否完成所有课程并返回学习顺序。  
  3. **矩阵布局类**（本题）——行列分别需要满足独立的前后约束。  
- **一句话总结解题钥匙**：  
  > “把所有相对位置约束看成有向图，用拓扑排序一次性求出行序和列序，若出现环则无解。”

---

## 反思

- **第一反应**：直接想把所有排列枚举出来检查——这在概念上可行，却忽视了规模的爆炸。  
- **最容易踩的坑**  
  - **环检测**：忘记在拓扑排序后检查是否得到完整的 `k` 长序列，导致错误地返回不完整的矩阵。  
  - **下标混淆**：行/列索引是从 `0` 开始，节点编号从 `1` 开始，映射时一定要注意 `-1` 或 `+1` 的偏移。  
  - **重复约束**：同一对 `(a, b)` 可能出现多次，建图时不需要去重，算法仍能正常工作。  
- **下次类似题目**的第一步应是：  
  > “把‘必须在…之前/左边/上面’的关系画成有向图，先判断是否有环，再用拓扑排序得到线性顺序。”