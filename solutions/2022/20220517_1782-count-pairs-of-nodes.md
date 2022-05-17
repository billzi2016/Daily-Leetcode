# #1782. **计数节点对** / Count Pairs Of Nodes

> 难度：困难 · 标签：Array、Hash Table、Two Pointers、Binary Search、Graph、Sorting、Counting · [LeetCode 链接](https://leetcode.com/problems/count-pairs-of-nodes/)

---

## 题目（英文原版）

**Description**

You are given an undirected graph defined by an integer n, the number of nodes, and a 2D integer array edges, the edges in the graph, where edges[i] = [ui, vi] indicates that there is an undirected edge between ui and vi. You are also given an integer array queries.
Let incident(a, b) be defined as the number of edges that are connected to either node a or b.
The answer to the jth query is the number of pairs of nodes (a, b) that satisfy both of the following conditions:
Return an array answers such that answers.length == queries.length and answers[j] is the answer of the jth query.
Note that there can be multiple edges between the same two nodes.

**Examples**

**Example 1:**

```
Input: n = 4, edges = [[1,2],[2,4],[1,3],[2,3],[2,1]], queries = [2,3]
Output: [6,5]
Explanation: The calculations for incident(a, b) are shown in the table above.
The answers for each of the queries are as follows:
- answers[0] = 6. All the pairs have an incident(a, b) value greater than 2.
- answers[1] = 5. All the pairs except (3, 4) have an incident(a, b) value greater than 3.
```

**Example 2:**

```
Input: n = 5, edges = [[1,5],[1,5],[3,4],[2,5],[1,3],[5,1],[2,3],[2,5]], queries = [1,2,3,4,5]
Output: [10,10,9,8,6]
```

**Constraints**

- 2 <= n <= 2 * 104
- 1 <= edges.length <= 105
- 1 <= ui, vi <= n
- ui != vi
- 1 <= queries.length <= 20
- 0 <= queries[j] < edges.length

---

## 题目（中文翻译）

给定一个由整数 `n` 表示节点数的无向图（undirected graph），以及一个二维整数数组 `edges` 表示图中的边，其中 `edges[i] = [ui, vi]` 表示在节点 `ui` 与节点 `vi` 之间存在一条无向边。另给定一个整数数组 `queries`。

定义 `incident(a, b)` 为与节点 `a` 或节点 `b` 任意一端相连的边的数量（即同时统计两节点的所有相邻边，重复的边会被多次计入）。

第 `j` 个查询的答案是满足以下 **全部** 条件的节点对 `(a, b)`（`a < b`）的数量：

*（题目原文中应列出具体的条件，此处保留原样）*

返回一个数组 `answers`，使得 `answers.length == queries.length`，且 `answers[j]` 为第 `j` 个查询的答案。

注意：同一对节点之间可能存在多条边（即多重边）。

---

### 示例

**示例 1**

> **输入**  
> `n = 4`  
> `edges = [[1,2],[2,4],[1,3],[2,3],[2,1]]`  
> `queries = [2,3]`  
>   
> **输出**  
> `[6,5]`  
>   
> **解释**  
> 表格中展示了每对节点的 `incident(a, b)` 计算结果。  
> - `answers[0] = 6`。所有节点对的 `incident(a, b)` 均大于 `2`。  
> - `answers[1] = 5`。除节点对 `(3, 4)` 之外，其余所有节点对的 `incident(a, b)` 均大于 `3`。

**示例 2**

> **输入**  
> `n = 5`  
> `edges = [[1,5],[1,5],[3,4],[2,5],[1,3],[5,1],[2,3],[2,5]]`  
> `queries = [1,2,3,4,5]`  
>   
> **输出**  
> `[10,10,9,8,6]`

---

### 约束

- `2 <= n <= 2 * 10^4`
- `1 <= edges.length <= 10^5`
- `1 <= ui, vi <= n`
- `ui != vi`
- `1 <= queries.length <= 20`
- `0 <= queries[j] < edges.length`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法就是把所有可能的节点对 `(a, b)`（`a < b`）都枚举一遍，逐个计算  
```
incident(a, b) = degree[a] + degree[b] - occurrences(a, b)
```  
其中  

* **degree[x]**：与节点 `x` 相连的边的总条数（如果两条相同的边都算在内）。可以把它想成“这个人有多少条朋友线”。  
* **occurrences(a, b)**：在 `edges` 中出现的 `(a, b)`（或 `(b, a)`）的次数。它相当于“这两个人之间重复的聊天记录”。  

只要 `incident(a, b) > query`，这对节点就算合法，答案就加一。

> **类比**：把 `degree` 想成字典里每个单词出现的次数，`occurrences` 就是两个单词一起出现的次数。我们要比较“各自出现次数之和减去一起出现的次数”是否大于给定阈值。

暴力遍历所有 `C(n,2) = n·(n‑1)/2` 对，逐对检查即可。

#### 代码（Python）  

```python
from collections import defaultdict
from typing import List

def brute_force(n: int, edges: List[List[int]], queries: List[int]) -> List[int]:
    # 1. 统计每个节点的度（有多少条边连到它）
    degree = [0] * (n + 1)                 # 下标从 1 开始，0 位置不用
    # 2. 统计每对节点之间出现了几条相同的边
    pair_cnt = defaultdict(int)           # (小, 大) -> 出现次数

    for u, v in edges:
        degree[u] += 1
        degree[v] += 1
        a, b = (u, v) if u < v else (v, u)
        pair_cnt[(a, b)] += 1

    ans = []
    # 3. 对每个 query 暴力枚举所有节点对
    for k in queries:
        cur = 0
        for a in range(1, n + 1):
            for b in range(a + 1, n + 1):
                # incident = degree[a] + degree[b] - occurrences(a,b)
                inc = degree[a] + degree[b] - pair_cnt.get((a, b), 0)
                if inc > k:
                    cur += 1
        ans.append(cur)
    return ans
```

#### 复杂度  

- **时间复杂度**：`O( n² + m )`  
  - `n²` 来自两层循环枚举所有节点对（`n` 最大 2·10⁴，`n²` 会是 4·10⁸，远超时间限制）。  
  - `m` 是遍历所有边的成本（`m = len(edges)`），在这里算作常数级别。  

- **空间复杂度**：`O( n + m )`  
  - `degree` 需要 `O(n)` 空间。  
  - `pair_cnt` 用哈希表记录每对节点的出现次数，最坏情况每条边都是不同的端点，空间是 `O(m)`。  

> **大白话**：时间复杂度里的 `O(n²)` 就像让 20 000 个人两两握手，次数是几亿次，显然不可能在几秒内完成。  

---

### 2. 最优解  

#### 思路  

暴力的瓶颈在于**枚举所有 `n·(n‑1)/2` 对**。我们要把这一步换成**线性或对数级别**的操作。  
关键观察如下：

1. **先不考虑 `occurrences(a, b)`**（即假设没有多条相同的边）。  
   那么条件简化为  
   ```
   degree[a] + degree[b] > k
   ```  
   只要两个节点的度之和大于阈值，就算合法。  

2. 对所有节点的度数进行排序。设 `deg` 为排序后的数组（从小到大）。  
   对每个 `i`（从左到右），我们可以用**双指针**找出最右侧的 `j` 使得 `deg[i] + deg[j] > k`。  
   由于 `deg` 已经排好序，`j` 只会向左移动，整个过程是 `O(n)`。  

3. 上面的计数**把所有满足 `degree[a] + degree[b] > k` 的对都算进来了**，但我们忘记减去 `occurrences(a, b)`。  
   对于真正的 `incident(a, b)`，如果  
   ```
   degree[a] + degree[b] > k   且   degree[a] + degree[b] - cnt(a,b) <= k
   ```  
   说明这对在第 2 步被错误计数了，需要 **减 1**。  

   只需要遍历所有出现过的边（即 `pair_cnt` 中的键），检查上述条件即可。因为 `pair_cnt` 的大小等于不同端点对的数量，最多 `m`，所以这一步是 `O(m)`。  

4. 对每个查询 `k` 重复步骤 2、3。  
   - 步骤 2 只涉及已排序的度数组，用 **双指针** 线性计数，`O(n)`。  
   - 步骤 3 只遍历 `pair_cnt`，`O(m)`。  

   `queries` 的数量 ≤ 20，整体复杂度是  
   ```
   O( n log n )   // 一次排序
   +  queries * ( O(n) + O(m) )
   ```

   在题目限制下（n ≤ 2·10⁴，m ≤ 10⁵，queries ≤ 20）完全可接受。  

#### 关键数据结构与概念  

| 数据结构 | 生活化类比 | 作用 |
| -------- | ---------- | ---- |
| `degree` 列表 | 每个人的“朋友圈人数” | 快速得到任意节点的度 |
| 哈希表 `pair_cnt[(a,b)]` | “两个人之间的重复聊天记录次数” | 记录多条相同边的出现次数 |
| 排序后的 `deg` 数组 | 把所有人的朋友圈人数从少到多排好，方便快速配对 | 双指针计数的前提 |
| 双指针 | 两个指针像两只手，从左边最小、右边最大向中间靠拢，找出满足条件的配对 | `O(n)` 计数所有 `degree[a]+degree[b] > k` 的对 |

#### 代码（Python）  

```python
from collections import defaultdict
from typing import List

def count_pairs(n: int, edges: List[List[int]], queries: List[int]) -> List[int]:
    # ---------- 1. 预处理 ----------
    degree = [0] * (n + 1)                 # 节点度，1-indexed
    pair_cnt = defaultdict(int)           # (小, 大) -> 多重边数量

    for u, v in edges:
        degree[u] += 1
        degree[v] += 1
        a, b = (u, v) if u < v else (v, u)
        pair_cnt[(a, b)] += 1

    # 把度数放到一个只含 1..n 的列表并排序（不包括下标 0）
    deg = sorted(degree[1:])               # 长度恰好是 n

    # ---------- 2. 对每个 query 计算 ----------
    res = []
    for k in queries:
        # 2.1 双指针统计 degree[a] + degree[b] > k 的对数（先不减重复边）
        cnt = 0
        left = 0
        right = n - 1                       # deg 的最后一个下标

        while left < n:
            # 移动 right，直到 deg[left] + deg[right] <= k 为止
            while right > left and deg[left] + deg[right] > k:
                right -= 1
            # 此时 right 位置不满足 >k，右侧 (right+1 ... n-1) 都满足
            cnt += n - max(right + 1, left + 1)
            left += 1
        # 2.2 修正：把因为多重边而被多算的对减掉
        for (a, b), c in pair_cnt.items():
            # 原始度数之和
            s = degree[a] + degree[b]
            # 如果原本满足 >k，但扣掉 c 之后不满足，则需要减 1
            if s > k and s - c <= k:
                cnt -= 1
        res.append(cnt)

    return res
```

**代码要点说明（中文注释）**  

1. **度数统计**：遍历所有边，分别给两端节点 `+1`，并在哈希表中记录这条边出现的次数。  
2. **排序**：把所有节点的度数取出来排序，只需要一次 `O(n log n)`。  
3. **双指针计数**：  
   * `left` 从最小度数向右遍历。  
   * `right` 从最大度数向左移动，保持 `deg[left] + deg[right] > k` 为 **不成立**（即 `<= k`）。  
   * 当 `right` 停下来后，右侧所有下标 `> right` 与 `left` 配对都满足 `> k`，于是直接把这些配对数加入答案。  
   * 这种“滑动窗口”只会让指针单向移动，总共 `O(n)`。  
4. **修正重复边**：遍历 `pair_cnt`（至多 `m` 条），检查是否因为 `occurrences` 把本应不合法的对算进来了，若是则答案减一。  

#### 复杂度  

- **时间复杂度**  
  - 排序度数：`O(n log n)`（只做一次）。  
  - 对每个 query：双指针 `O(n)` + 修正多重边 `O(m)`。  
  - 总计：`O(n log n + q·(n + m))`，其中 `q = len(queries) ≤ 20`。  
  - 与暴力的 `O(n²)` 相比，**把几亿次的遍历降到了几万次**，跑得非常快。  

- **空间复杂度**  
  - `degree`、`deg` 各 `O(n)`。  
  - `pair_cnt` 最多保存 `m` 条不同的端点对，`O(m)`。  
  - 总体 `O(n + m)`，符合题目限制。  

---

## 心得  

- **核心技巧**：先把 “度数之和 > k” 的计数用**排序 + 双指针**搞定，再**减去因多重边导致的错误计数**。  
- **适用场景**：  
  1. 需要统计满足 `value[i] + value[j] > threshold` 的所有无序对（如 “Two Sum 大于阈值”）。  
  2. 计数图中满足某种度数约束的节点对（如 “度数之和大于 X 的节点对”）。  
- **一句话总结**：**先把所有度数配对算出来，再用哈希表把重复边的“超额计数”逐一抵消**。  

---

## 反思  

- **第一反应**：看到 “incident(a, b) = degree[a] + degree[b] - occurrences(a,b)”，自然想到直接遍历所有节点对，直接套公式。  
- **最容易踩的坑**  
  1. **多重边**：同一对节点可能出现多条边，需要用哈希表统计出现次数，否则会把 `occurrences` 当成 0，导致答案偏大。  
  2. **下标错误**：度数组是 1‑based，排序后是 0‑based，双指针时一定要注意不要把同一个节点配对（`a != b`）。  
  3. **边界条件**：`k` 可能为 0，也可能等到 `edges.length-1`，双指针的 `while` 条件要写得严谨，防止越界。  
- **下次遇到同类题的第一步**：  
  1. 把 **“不考虑相互影响的部分”**（这里是 `degree[a]+degree[b]`）先单独计数（排序+双指针或二分）。  
  2. 再用 **哈希表** 把 **“相互影响的修正项”**（这里是 `occurrences`）逐一校正。