# #2580. 统计将重叠区间分组的方案数 / Count Ways to Group Overlapping Ranges

> 难度：中等 · 标签：Array、Sorting · [LeetCode 链接](https://leetcode.com/problems/count-ways-to-group-overlapping-ranges/)

---

## 题目（英文原版）

**Description**

You are given a 2D integer array ranges where ranges[i] = [starti, endi] denotes that all integers between starti and endi (both inclusive) are contained in the ith range.
You are to split ranges into two (possibly empty) groups such that:
Two ranges are said to be overlapping if there exists at least one integer that is present in both ranges.
Return the total number of ways to split ranges into two groups. Since the answer may be very large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: ranges = [[6,10],[5,15]]
Output: 2
Explanation: 
The two ranges are overlapping, so they must be in the same group.
Thus, there are two possible ways:
- Put both the ranges together in group 1.
- Put both the ranges together in group 2.
```

**Example 2:**

```
Input: ranges = [[1,3],[10,20],[2,5],[4,8]]
Output: 4
Explanation: 
Ranges [1,3], and [2,5] are overlapping. So, they must be in the same group.
Again, ranges [2,5] and [4,8] are also overlapping. So, they must also be in the same group. 
Thus, there are four possible ways to group them:
- All the ranges in group 1.
- All the ranges in group 2.
- Ranges [1,3], [2,5], and [4,8] in group 1 and [10,20] in group 2.
- Ranges [1,3], [2,5], and [4,8] in group 2 and [10,20] in group 1.
```

**Constraints**

- 1 <= ranges.length <= 105
- ranges[i].length == 2
- 0 <= starti <= endi <= 109

---

## 题目（中文翻译）

**题目描述**  
给定一个二维整数数组 `ranges`，其中 `ranges[i] = [start_i, end_i]` 表示第 *i* 个区间包含所有介于 `start_i` 和 `end_i`（两端均包含）的整数。  
要求把这些区间划分为两个（可能为空）组，使得：

- 若两个区间存在至少一个公共整数，则称它们是**重叠（overlapping）**的。  

返回将区间划分为两组的所有可能方式数。由于答案可能非常大，请返回答案对 `10^9 + 7` 取模后的结果。

**示例**

*示例 1*  
```
输入: ranges = [[6,10],[5,15]]
输出: 2
解释: 
这两个区间是重叠的，因此必须放在同一组。  
所以有两种可能的划分方式：
- 将两个区间都放入组 1；
- 将两个区间都放入组 2。
```

*示例 2*  
```
输入: ranges = [[1,3],[10,20],[2,5],[4,8]]
输出: 4
解释: 
区间 [1,3] 与 [2,5] 重叠，故它们必须在同一组。  
区间 [2,5] 与 [4,8] 也重叠，故这三个区间全部必须在同一组。  
因此共有四种划分方式：
- 所有区间都放入组 1；
- 所有区间都放入组 2；
- 将区间 [1,3]、[2,5]、[4,8] 放入组 1，区间 [10,20] 放入组 2；
- 将区间 [1,3]、[2,5]、[4,8] 放入组 2，区间 [10,20] 放入组 1。
```

**约束条件**  
- `1 <= ranges.length <= 10^5`  
- `ranges[i].length == 2`  
- `0 <= start_i <= end_i <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每个区间看成图中的一个点，**如果两个区间有交集就连一条边**。  
这样我们得到一个无向图，图里相互连通的点必须被放进同一个组——因为只要有一条“重叠”边，它们就不能分到不同组。  

- **数据结构类比**：  
  - **邻接表**（list of lists）就像一本《通讯录》：每个人（区间）都有一个“朋友列表”（与之重叠的区间）。  
  - **深度优先搜索（DFS）** 像在《通讯录》中从一个人出发，顺着朋友关系把所有能联系到的人全部找出来，这些人就是同一个连通分量。  

- **正确性**：  
  - 在同一个连通分量里的任意两个区间，都可以通过若干条重叠边相互到达。若把它们分到不同组，必然会出现一条跨组的重叠边，违反题意。  
  - 反之，把每个连通分量整体放进任意一个组（左组或右组）一定合法，因为同一分量内部的所有重叠关系都保持在同一组内。  

- **计数**：  
  - 设有 `k` 个连通分量，每个分量有 **两种** 放法（左组或右组），相互独立，故总方案数是 `2^k`。  

#### 代码（Python）

```python
MOD = 10**9 + 7

def overlap(a, b):
    """判断两个区间是否有交集。"""
    return not (a[1] < b[0] or b[1] < a[0])   # 如果 a 完全在 b 左侧或右侧则不重叠

def brute_count(ranges):
    n = len(ranges)
    # 1️⃣ 建图：邻接表
    graph = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if overlap(ranges[i], ranges[j]):
                graph[i].append(j)
                graph[j].append(i)

    # 2️⃣ DFS 找连通分量
    visited = [False] * n
    comp_cnt = 0

    def dfs(v):
        stack = [v]
        while stack:
            cur = stack.pop()
            if visited[cur]:
                continue
            visited[cur] = True
            for nb in graph[cur]:
                if not visited[nb]:
                    stack.append(nb)

    for i in range(n):
        if not visited[i]:
            comp_cnt += 1          # 新的连通分量
            dfs(i)

    # 3️⃣ 计算 2^k（取模）
    return pow(2, comp_cnt, MOD)
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 两层循环遍历所有区间对检查是否重叠，`n` 最多 10⁵ 时会超时。  
  - “O(n²)” 可以理解为“如果你把 10,000 个元素两两比较，需要大约 1 亿 次比较”。  
- **空间复杂度**：`O(n²)`（最坏情况下每对区间都重叠，邻接表要存 `n²` 条边）  
  - 实际上即使是 `O(n²)` 条边，也会占用巨大的内存，远超题目限制。  

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **两两比较**。我们可以利用区间的 **排序** 特性把比较次数降到线性。  

**关键观察**：  
- 按左端点 `start` 从小到大排序后，如果当前区间的左端点大于“已合并区间的最右端点”，说明它 **不与前面的任何区间重叠**，从而开启一个新的连通分量。  
- 否则，它必定与前面的某个区间（其实是与最近的已合并区间）重叠，属于同一个连通分量。  

于是我们只需要一次遍历，维护**当前连通块的最右端点** `cur_end`：

1. **排序**：`ranges.sort(key=lambda x: x[0])`（按左端点升序）  
2. **遍历**：  
   - 初始 `cur_end = -1`，`components = 0`  
   - 对每个区间 `[l, r]`：  
     - 若 `l > cur_end` → 进入 **新块**，`components += 1`，并把 `cur_end = r`。  
     - 否则（有交集） → 仍在同一块，更新 `cur_end = max(cur_end, r)`（把右端点往右延伸）。  

遍历结束后，`components` 就是连通分量的数量 `k`。答案即 `2^k (mod MOD)`。

**类比**：  
把每个区间想象成一段道路，左端点是起点，右端点是终点。把所有道路按起点排好队后，司机只要看前面道路的终点能否“挡住”自己，就知道自己是否要加入已经在行驶的车队（同一个连通块）——如果挡不住，就开辟新车队（新块）。

#### 代码（Python）

```python
MOD = 10**9 + 7

def countWays(ranges):
    """
    计算把 intervals 分成两组的方案数。
    思路：排序 + 一次线性扫描，统计不相交的合并块个数 k，答案为 2^k。
    """
    # 1️⃣ 按左端点升序排列
    ranges.sort(key=lambda x: x[0])

    components = 0          # 连通块（合并后区间）的数量
    cur_end = -1            # 当前块的最右端点

    for l, r in ranges:
        if l > cur_end:     # 与前面的块不相交 → 新块
            components += 1
            cur_end = r
        else:               # 与当前块相交 → 合并进同一块
            cur_end = max(cur_end, r)   # 把右端点往右延伸

    # 2️⃣ 2 的 components 次方（取模）
    return pow(2, components, MOD)
```

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 主要耗时在排序（`n log n`），遍历本身是线性的 `O(n)`。  
  - “O(n log n)” 可以理解为“把 100,000 本书排好顺序大约需要 100,000 × 17 次比较”，远比 `n²` 快得多。  
- **空间复杂度**：`O(1)`（不计输入数组本身）  
  - 只用了几个整型变量来记录当前右端点和块计数。  

---

## 心得  

- **核心技巧**：把「区间是否相交」转化为「左端点是否大于上一个块的右端点」，通过排序实现线性扫描。  
- **适用题型**：  
  1. 合并重叠区间（LeetCode 56）  
  2. 判断区间是否可以安排在同一资源上（会议室安排，LeetCode 252）  
  3. 统计不相交区间的最大子集（区间调度问题）  
- **一句话总结**：  
  “先排序、后扫线——相邻区间的左端点决定是否开启新组”。  

---

## 反思  

- **第一反应**：想到把区间当作图的节点，两两检查是否相交，然后做连通分量。  
- **最容易踩的坑**：  
  - **边界条件**：`l == cur_end` 时仍算重叠（因为区间是闭区间），要用 `l > cur_end` 判断新块。  
  - **取模**：答案可能非常大，记得对 `2^k` 取 `10⁹+7`。  
  - **排序后忘记更新 `cur_end` 为 `max`**，导致错误的块计数。  
- **下次第一步**：  
  “先把所有区间按左端点排序，再用一个变量记录当前块的最右端点，遍历一次即可得到块的数量”。