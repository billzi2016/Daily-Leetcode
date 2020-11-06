# #1042. 不相邻的花卉种植 / Flower Planting With No Adjacent

> 难度：中等 · 标签：Depth-First Search、Breadth-First Search、Graph · [LeetCode 链接](https://leetcode.com/problems/flower-planting-with-no-adjacent/)

---

## 题目（英文原版）

**Description**

You have n gardens, labeled from 1 to n, and an array paths where paths[i] = [xi, yi] describes a bidirectional path between garden xi to garden yi. In each garden, you want to plant one of 4 types of flowers.
All gardens have at most 3 paths coming into or leaving it.
Your task is to choose a flower type for each garden such that, for any two gardens connected by a path, they have different types of flowers.
Return any such a choice as an array answer, where answer[i] is the type of flower planted in the (i+1)th garden. The flower types are denoted 1, 2, 3, or 4. It is guaranteed an answer exists.

**Examples**

**Example 1:**

```
Input: n = 3, paths = [[1,2],[2,3],[3,1]]
Output: [1,2,3]
Explanation:
Gardens 1 and 2 have different types.
Gardens 2 and 3 have different types.
Gardens 3 and 1 have different types.
Hence, [1,2,3] is a valid answer. Other valid answers include [1,2,4], [1,4,2], and [3,2,1].
```

**Example 2:**

```
Input: n = 4, paths = [[1,2],[3,4]]
Output: [1,2,1,2]
```

**Example 3:**

```
Input: n = 4, paths = [[1,2],[2,3],[3,4],[4,1],[1,3],[2,4]]
Output: [1,2,3,4]
```

**Constraints**

- 1 <= n <= 104
- 0 <= paths.length <= 2 * 104
- paths[i].length == 2
- 1 <= xi, yi <= n
- xi != yi
- Every garden has at most 3 paths coming into or leaving it.

---

## 题目（中文翻译）

你有 `n` 株花园，编号从 `1` 到 `n`，以及一个数组 `paths`，其中 `paths[i] = [x_i, y_i]` 表示花园 `x_i` 与花园 `y_i` 之间的一条双向路径。每个花园需要种植一种花，共有 4 种花可选。  
**限制条件**：每个花园至多有 3 条路径相连（即最多 3 条入度或出度）。  

你的任务是为每个花园选择一种花的类型，使得任意两座通过路径相连的花园种植的花类型不同。返回任意一种满足条件的选择方案 `answer`，其中 `answer[i]` 表示第 `i+1` 株花园种植的花的类型。花的类型用整数 `1、2、3、4` 表示。题目保证一定存在可行解。

**示例 1**  
**输入**  
```text
n = 3, paths = [[1,2],[2,3],[3,1]]
```  
**输出**  
```text
[1,2,3]
```  
**解释**：  
- 花园 1 与花园 2 种植的花类型不同。  
- 花园 2 与花园 3 种植的花类型不同。  
- 花园 3 与花园 1 种植的花类型不同。  

因此 `[1,2,3]` 是一个合法答案。其他合法答案还包括 `[1,2,4]`、`[1,4,2]`、`[3,2,1]` 等。

**示例 2**  
**输入**  
```text
n = 4, paths = [[1,2],[3,4]]
```  
**输出**  
```text
[1,2,1,2]
```  

**示例 3**  
**输入**  
```text
n = 4, paths = [[1,2],[2,3],[3,4],[4,1],[1,3],[2,4]]
```  
**输出**  
```text
[1,2,3,4]
```  

**约束条件**  

- `1 <= n <= 10^4`  
- `0 <= paths.length <= 2 * 10^4`  
- `paths[i].length == 2`  
- `1 <= x_i, y_i <= n`  
- `x_i != y_i`  
- 每个花园的相连路径数至多为 3。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每个花园看成图中的一个点，把路径看成无向边。  
我们需要给每个点涂上 1~4 四种颜色中的一种，使相邻的点颜色不同。  

一种“暴力”做法是 **回溯（DFS + 试探）**：

1. 按顺序遍历第 `1`、`2` …… `n` 个花园。  
2. 对当前花园，尝试把 1、2、3、4 四种颜色依次放进去。  
3. 放颜色前检查所有已经涂好的相邻花园的颜色是否冲突（相同即冲突）。  
4. 如果没有冲突，就递归处理下一个花园；如果后面的递归全部失败，就把当前颜色撤回（回溯），尝试下一个颜色。  

> **类比**：把它想成在一排座位上安排学生，每个学生只能坐在不和左边/右边已经坐好的同学颜色相同的座位上。如果坐不下，就换另一种颜色再试。

因为题目保证每个花园最多只有 3 条边，而颜色有 4 种，所以一定能找到合法的颜色，只是暴力搜索会尝试很多不必要的组合。

#### 代码（Python）

```python
from typing import List

def gardenNoAdj_bruteforce(n: int, paths: List[List[int]]) -> List[int]:
    # 建立邻接表，类似“谁和谁是好邻居”
    graph = [[] for _ in range(n)]
    for u, v in paths:
        u -= 1                     # 0‑based 方便下标
        v -= 1
        graph[u].append(v)
        graph[v].append(u)

    answer = [0] * n               # 0 表示还未染色

    def dfs(idx: int) -> bool:
        """尝试给第 idx（0‑based）个花园染色，成功返回 True"""
        if idx == n:               # 所有花园都已经染好
            return True

        # 试 1~4 四种颜色
        for color in range(1, 5):
            # 检查相邻花园的颜色是否冲突
            conflict = False
            for nb in graph[idx]:
                if answer[nb] == color:
                    conflict = True
                    break
            if conflict:
                continue            # 颜色冲突，换下一个颜色

            # 没冲突，暂时把颜色写进去
            answer[idx] = color
            # 递归处理下一个花园
            if dfs(idx + 1):
                return True        # 找到合法方案，直接返回
            # 回溯：撤销当前颜色，尝试别的颜色
            answer[idx] = 0
        # 四个颜色都不行，说明前面的选择有问题
        return False

    dfs(0)                         # 从第 0 个花园开始搜索
    return answer
```

#### 复杂度

- **时间复杂度**：最坏情况是每个花园都尝试 4 种颜色，且每次检查相邻的 ≤3 条边。于是时间上界是 `O(4^n * 3)`，即指数级的 `O(4^n)`。这里的 `4^n` 可以想象成“每个花园有 4 种可能”，所有组合都遍历一遍。  
- **空间复杂度**：除了存图的邻接表 `O(n + m)`（`m = len(paths)`），递归栈深度为 `n`，所以总共是 `O(n + m)`。在本题 `m ≤ 2·10^4`，`n ≤ 10^4`，仍然是线性空间。

> 暴力搜索虽然能得到答案，但对 `n=10^4` 的规模根本不可行。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**冲突只发生在相邻的花园之间**。  
关键观察：

- 每个花园最多只有 **3 条相邻路径**，而可选颜色有 **4 种**。  
- 这意味着**只要我们在给当前花园染色时，检查它已经染好的邻居，用剩下的颜色就一定能选到**。  

于是我们可以**一次遍历**（不需要回溯）就完成染色：

1. 先把所有路径转成邻接表，便于快速得到每个花园的邻居。  
2. 按顺序遍历花园 `1 … n`（顺序任意都行），对第 `i` 个花园：
   - 用一个长度为 `5` 的布尔数组 `used[5]`（下标 1~4）记录它的已染色邻居占用了哪些颜色。  
   - 只需要遍历至多 3 个邻居，标记 `used[neighbor_color] = True`。  
   - 再从颜色 `1,2,3,4` 中挑出第一个 `used[color] == False` 的颜色，即为合法颜色。  
3. 把挑选的颜色写入答案数组，继续下一个花园。

> **类比**：想象每个花园是一个孩子，每个孩子最多有 3 位朋友。我们给孩子发衣服颜色时，只要看朋友们已经穿了什么颜色，剩下的颜色随便挑一个就行。因为颜色有 4 种，而朋友最多只占走 3 种。

这就是 **贪心染色**（Greedy Coloring）在**度 ≤ 3**的特殊图上的直接实现。由于保证答案一定存在，这种一次遍历的方式必能成功。

#### 代码（Python）

```python
from typing import List

def gardenNoAdj(n: int, paths: List[List[int]]) -> List[int]:
    # 1️⃣ 建图：邻接表，graph[i] 保存第 i+1 个花园的所有相邻花园（0‑based）
    graph = [[] for _ in range(n)]
    for u, v in paths:
        u -= 1
        v -= 1
        graph[u].append(v)
        graph[v].append(u)

    answer = [0] * n               # 最终颜色答案，0 表示未染

    # 2️⃣ 按顺序为每个花园挑颜色
    for i in range(n):
        used = [False] * 5         # 索引 1~4 对应四种颜色是否被邻居占用
        # 标记已经染好的相邻花园的颜色
        for nb in graph[i]:
            if answer[nb] != 0:    # 只看已经染色的邻居
                used[answer[nb]] = True

        # 选第一个没有被占用的颜色
        for color in range(1, 5):
            if not used[color]:
                answer[i] = color
                break               # 找到后直接结束内层循环

    return answer
```

#### 复杂度

- **时间复杂度**：  
  - 建图遍历所有路径一次，`O(m)`（`m = len(paths)`）。  
  - 主循环遍历 `n` 个花园，每个花园检查至多 3 个邻居，常数级操作 `O(1)`。  
  - 因此总时间是 **`O(n + m)`**，线性级别。对比暴力的指数级，快得多。  
  - 用生活化的说法：我们只需要一次“走访所有花园”，每次只看它的几个邻居，就能决定颜色，根本不需要“反复尝试”。

- **空间复杂度**：  
  - 邻接表占 `O(n + m)`，答案数组占 `O(n)`，其余临时变量都是常数。  
  - 整体仍是 **`O(n + m)`** 的线性空间。

---

## 心得

- 这道题的核心技巧是 **基于最大度数的贪心染色**：因为每个节点的度 ≤ 3，而颜色数是 4，必然存在未被占用的颜色。  
- 类似的技巧可以用在：
  1. **图的染色问题**（如 “分配课程表” 中的冲突检测，只要颜色数 ≥ 最大度数 + 1 就能贪心完成）。  
  2. **调度问题**，如 “给任务分配机器”，每台机器最多同时处理 `k` 个相互冲突的任务，只要机器数 ≥ `k+1`，可以直接贪心分配。  
  3. **地图着色**（四色定理的简化版），当每块区域的相邻块数 ≤ 3 时，同样可以用 4 种颜色一次遍历完成。  

> **解题钥匙**：**“度 ≤ 颜色数-1 ⇒ 贪心一次遍历必能成功”。**

---

## 反思

- **第一反应**：看到“每个花园最多 3 条路，颜色有 4 种”，立刻想到“一定可以给每个花园挑一个不冲突的颜色”。于是从贪心的角度出发，而不是马上写回溯。  
- **最容易踩的坑**  
  1. **下标混淆**：题目使用 1‑based 编号，代码里要统一转成 0‑based，否则数组越界。  
  2. **忘记只看已染色的邻居**：在遍历时如果把所有邻居的颜色都标记，会把未染色的 0 也算进去，导致误判颜色被占用。  
  3. **没有考虑路径为空的情况**：`paths` 可能为 `[]`，此时每个花园都可以随意取颜色，代码仍需正常返回长度为 `n` 的数组。  

- **下次类似题的第一步**：先检查**图的最大度数**与**可用颜色（或资源）数量**的关系，如果 “可用资源 ≥ 最大度数 + 1”，就尝试 **一次贪心遍历**；否则再考虑回溯或更复杂的算法。