# #2101. 引爆最多炸弹 / Detonate the Maximum Bombs

> 难度：中等 · 标签：Array、Math、Depth-First Search、Breadth-First Search、Graph、Geometry · [LeetCode 链接](https://leetcode.com/problems/detonate-the-maximum-bombs/)

---

## 题目（英文原版）

**Description**

You are given a list of bombs. The range of a bomb is defined as the area where its effect can be felt. This area is in the shape of a circle with the center as the location of the bomb.
The bombs are represented by a 0-indexed 2D integer array bombs where bombs[i] = [xi, yi, ri]. xi and yi denote the X-coordinate and Y-coordinate of the location of the ith bomb, whereas ri denotes the radius of its range.
You may choose to detonate a single bomb. When a bomb is detonated, it will detonate all bombs that lie in its range. These bombs will further detonate the bombs that lie in their ranges.
Given the list of bombs, return the maximum number of bombs that can be detonated if you are allowed to detonate only one bomb.

**Examples**

**Example 1:**

```
Input: bombs = [[2,1,3],[6,1,4]]
Output: 2
Explanation:
The above figure shows the positions and ranges of the 2 bombs.
If we detonate the left bomb, the right bomb will not be affected.
But if we detonate the right bomb, both bombs will be detonated.
So the maximum bombs that can be detonated is max(1, 2) = 2.
```

**Example 2:**

```
Input: bombs = [[1,1,5],[10,10,5]]
Output: 1
Explanation:
Detonating either bomb will not detonate the other bomb, so the maximum number of bombs that can be detonated is 1.
```

**Example 3:**

```
Input: bombs = [[1,2,3],[2,3,1],[3,4,2],[4,5,3],[5,6,4]]
Output: 5
Explanation:
The best bomb to detonate is bomb 0 because:
- Bomb 0 detonates bombs 1 and 2. The red circle denotes the range of bomb 0.
- Bomb 2 detonates bomb 3. The blue circle denotes the range of bomb 2.
- Bomb 3 detonates bomb 4. The green circle denotes the range of bomb 3.
Thus all 5 bombs are detonated.
```

**Constraints**

- 1 <= bombs.length <= 100
- bombs[i].length == 3
- 1 <= xi, yi, ri <= 105

---

## 题目（中文翻译）

**题目描述**  
给定一系列炸弹。炸弹的范围定义为其效果能够感受到的区域，该区域为以炸弹所在位置为中心、半径为 `ri` 的圆形。  
炸弹用下标从 **0** 开始的二维整数数组 `bombs` 表示，其中 `bombs[i] = [xi, yi, ri]`。`xi` 和 `yi` 分别表示第 `i` 炸弹的 **X 坐标**（X-coordinate）和 **Y 坐标**（Y-coordinate），`ri` 表示其范围的半径。  

你可以选择引爆 **一个** 炸弹。引爆后，所有位于其范围内的炸弹都会被连锁引爆，这些炸弹又会继续引爆其范围内的炸弹，以此类推。  

给定炸弹列表，返回在只能引爆 **一个** 炸弹的前提下，能够引爆的最多炸弹数量。

---

## 示例

### 示例 1  
**输入**: `bombs = [[2,1,3],[6,1,4]]`  
**输出**: `2`  
**解释**:  
上图展示了两个炸弹的位置和范围。  
- 如果引爆左侧的炸弹，右侧的炸弹不会受到影响。  
- 如果引爆右侧的炸弹，则两个炸弹都会被引爆。  

因此，能够引爆的最大炸弹数为 `max(1, 2) = 2`。

### 示例 2  
**输入**: `bombs = [[1,1,5],[10,10,5]]`  
**输出**: `1`  
**解释**:  
无论引爆哪一个炸弹，都无法引爆另一枚炸弹，所以最大可引爆的炸弹数为 `1`。

### 示例 3  
**输入**: `bombs = [[1,2,3],[2,3,1],[3,4,2],[4,5,3],[5,6,4]]`  
**输出**: `5`  
**解释**:  
最佳的引爆选择是炸弹 `0`，原因如下：  
- 炸弹 `0` 能引爆炸弹 `1` 和 `2`（红色圆圈表示炸弹 `0` 的范围）。  
- 炸弹 `2` 能进一步引爆炸弹 `3`（蓝色圆圈表示炸弹 `2` 的范围）。  
- 炸弹 `3` 再引爆炸弹 `4`（绿色圆圈表示炸弹 `3` 的范围）。  

于是全部 `5` 枚炸弹被连锁引爆。

---

## 约束条件
- `1 <= bombs.length <= 100`
- `bombs[i].length == 3`
- `1 <= xi, yi, ri <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**一次只选一个炸弹**，把它点燃后**不停地遍历所有炸弹**，看哪些在已经炸开的炸弹的范围内。如果某个炸弹在范围内，就把它也点燃；随后再继续检查剩下的炸弹，直到没有新的炸弹可以被点燃为止。

- **使用的结构**  
  - **列表**（list）保存所有炸弹的信息 `[[x, y, r], …]`。  
  - **集合**（set）记录已经被点燃的炸弹下标，类似“已经点燃的炸弹清单”。  
  - **循环**（while）不断尝试把新的炸弹加入集合，类似“不断往锅里加材料”。  

- **为什么能得到正确答案**  
  只要把**所有可能的传导路径**都枚举出来，就一定会得到从起始炸弹出发能够波及的全部炸弹。我们把每一次能够被点燃的炸弹都加入集合，循环结束时集合里就是这一次点燃能到达的全部炸弹。遍历所有起始炸弹，取最大集合大小即为答案。

- **复杂度分析（大白话）**  
  - 外层我们要**尝试每一个炸弹作为起点**，所以要跑 `n` 次（`n` 是炸弹数量）。  
  - 每一次点燃过程里，我们会**把每个炸弹和已经点燃的每个炸弹比较一次**，最坏情况下要比较 `n × n` 次。  
  - 所以总的时间是 `n`（起点） × `n × n`（比较） = **O(n³)**。  
  - 只用了一个集合来保存已经点燃的炸弹，最多装 `n` 个元素，空间是 **O(n)**。

> **O(n³) 是什么意思？**  
> 如果炸弹数量是 10，程序大约要做 10³ = 1000 次基本操作；如果是 100，操作数会涨到 1,000,000 次。随着 `n` 增大，运行时间会“立方级”增长。

#### 代码（Python）

```python
from typing import List, Set

def maximumDetonation_bruteforce(bombs: List[List[int]]) -> int:
    n = len(bombs)

    # 判断炸弹 j 是否在炸弹 i 的爆炸范围内（不需要开根号，比较平方就行）
    def in_range(i: int, j: int) -> bool:
        xi, yi, ri = bombs[i]
        xj, yj, _ = bombs[j]
        return (xi - xj) ** 2 + (yi - yj) ** 2 <= ri ** 2

    best = 0  # 记录最大能炸开的炸弹数

    # 把每个炸弹当作起点尝试一次
    for start in range(n):
        exploded: Set[int] = {start}      # 已经炸开的集合，先放进起点
        changed = True                    # 标记本轮是否有新炸弹被点燃

        while changed:                    # 只要还有新炸弹，就继续循环
            changed = False
            # 遍历所有炸弹，看有没有还能被炸开的
            for i in range(n):
                if i in exploded:         # 已经炸开的就跳过
                    continue
                # 只要有一个已经炸开的炸弹能把 i 引爆，就把 i 加进去
                for j in exploded:
                    if in_range(j, i):
                        exploded.add(i)
                        changed = True
                        break            # i 已经炸开，退出内部循环

        best = max(best, len(exploded))   # 更新全局最大值

    return best
```

#### 复杂度

- **时间复杂度：O(n³)**  
  - `n` 次起点 × 每次最多 `n` 次外层循环 × 每次比较 `n` 对炸弹。  
  - 直观理解：如果炸弹是 100 个，最坏情况下要进行 1,000,000 次距离判断。

- **空间复杂度：O(n)**  
  - 只用了一个集合 `exploded` 保存最多 `n` 个炸弹的编号。  

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于每次点燃过程都要**重复遍历所有炸弹**来检查是否在范围内，这导致了三层循环。我们可以把**“谁能炸到谁”**这层关系提前算好，保存成**有向图**（directed graph），然后每次只需要在图上做一次深度/广度搜索即可。

1. **构建有向图**  
   - 把每个炸弹当成**节点**。  
   - 如果炸弹 `i` 的圆形范围能够覆盖炸弹 `j`（即 `j` 在 `i` 的范围内），就在图里加一条**有向边** `i → j`。  
   - 判断是否在范围内仍然使用**距离的平方**，避免开根号的浮点运算。  
   - 这一步需要比较所有炸弹对，时间是 **O(n²)**，空间是 **O(n²)**（邻接表也算 `O(n²)`，但对 `n ≤ 100` 完全可以接受）。

2. **从每个节点出发做 DFS/BFS**  
   - 有向图已经把“能直接炸到的炸弹”列出来了。  
   - 对于起点 `i`，只要在图上**遍历所有能到达的节点**，就等价于“从 i 爆炸能波及的所有炸弹”。  
   - 采用 **深度优先搜索（DFS）**（递归或栈）或 **广度优先搜索（BFS）**（队列）均可，这里用 DFS。  
   - 每一次搜索遍历的边数至多是图的总边数 `E`，而 `E ≤ n²`，所以一次搜索是 **O(n²)**。  
   - 再对所有 `n` 个起点做一次搜索，总时间仍是 **O(n³)**，但常数更小，而且代码更简洁；实际上因为每次搜索只遍历 **已经建好的邻接表**，整体复杂度可以认为是 **O(n²)**（每条边最多被访问一次）。

3. **取最大值**  
   - 对每个起点记录搜索得到的节点数量，取最大即为答案。

> **为什么说是最优？**  
> - 建图只需要 **一次** `O(n²)` 的遍历，之后每次搜索只沿已有的边走，**不再重复做距离判断**。  
> - 对 `n ≤ 100` 的数据，这已经是最好的时间复杂度（**O(n²)**），再进一步的优化意义不大。

#### 代码（Python）

```python
from typing import List
from collections import defaultdict, deque

def maximumDetonation(bombs: List[List[int]]) -> int:
    n = len(bombs)

    # ---------- 1. 建图 ----------
    # graph[i] 保存所有被 i 炸到的炸弹下标
    graph = defaultdict(list)

    # 判断 j 是否在 i 的爆炸范围内（用平方距离避免 sqrt）
    def in_range(i: int, j: int) -> bool:
        xi, yi, ri = bombs[i]
        xj, yj, _ = bombs[j]
        return (xi - xj) ** 2 + (yi - yj) ** 2 <= ri ** 2

    for i in range(n):
        for j in range(n):
            if i != j and in_range(i, j):
                graph[i].append(j)   # 有向边 i -> j

    # ---------- 2. DFS 统计可炸到的炸弹 ----------
    def dfs(start: int) -> int:
        stack = [start]
        visited = set([start])    # 记录已经访问过的节点
        while stack:
            cur = stack.pop()
            for nxt in graph[cur]:
                if nxt not in visited:
                    visited.add(nxt)
                    stack.append(nxt)
        return len(visited)

    # ---------- 3. 求最大 ----------
    ans = 0
    for i in range(n):
        ans = max(ans, dfs(i))

    return ans
```

#### 复杂度

- **时间复杂度：O(n²)**  
  - 建图阶段：遍历所有炸弹对 `n × n` → O(n²)。  
  - 对每个起点的 DFS：每条有向边最多被访问一次，总共仍是 O(n²)。  
  - 对 `n ≤ 100` 的规模，这已经是最好的理论复杂度。

- **空间复杂度：O(n²)**  
  - 邻接表 `graph` 最坏情况下每个炸弹都能炸到所有其他炸弹，存 `n²` 条边。  
  - 递归栈/显式栈以及 visited 集合最多保存 `n` 个节点，属于次要开销。

---

## 心得

- **核心技巧**：把几何关系抽象成**有向图**，再利用**图的遍历（DFS/BFS）**求可达节点数。  
- **适用的题型**  
  1. “传染/扩散”类问题，如 **传播病毒、灯泡点亮** 等。  
  2. **区间覆盖**、**传送门**、**跳跃游戏** 等可以用有向边描述“从 A 能直接到 B”。  
  3. 任意**二维几何**中“点在圆/矩形内”导致的**依赖关系**，比如 **“最少点覆盖圆”**、**“激光能否穿过障碍”**。  
- **一句话总结解题钥匙**：  
  *“先把‘谁能直接影响谁’写成图，再在图上跑一次可达性搜索。”*

---

## 反思

- **第一反应**：看到“炸弹会炸到其他炸弹”，马上想到**递归/传播**，于是想到**从每个炸弹出发不断检查所有炸弹**，这就是暴力思路。  
- **最容易踩的坑**  
  1. **距离比较**要用平方，避免 `sqrt` 带来的精度误差和额外的时间开销。  
  2. **有向性**：炸弹 A 能炸到 B 并不代表 B 能炸到 A，构图时一定要区分方向。  
  3. **边界条件**：只有一个炸弹时答案必然是 1；坐标、半径可能很大（≤ 10⁵），但平方后仍在 Python 整数范围内。  
- **下次类似题的第一步**：  
  *先把“直接可达”关系抽象成图（或邻接表），再在图上做一次遍历*。这样既能避免重复计算，又能把几何问题转化为熟悉的图论问题。