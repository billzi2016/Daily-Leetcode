# #1743. 从相邻数对恢复数组 / Restore the Array From Adjacent Pairs

> 难度：中等 · 标签：Array、Hash Table、Depth-First Search · [LeetCode 链接](https://leetcode.com/problems/restore-the-array-from-adjacent-pairs/)

---

## 题目（英文原版）

**Description**

There is an integer array nums that consists of n unique elements, but you have forgotten it. However, you do remember every pair of adjacent elements in nums.
You are given a 2D integer array adjacentPairs of size n - 1 where each adjacentPairs[i] = [ui, vi] indicates that the elements ui and vi are adjacent in nums.
It is guaranteed that every adjacent pair of elements nums[i] and nums[i+1] will exist in adjacentPairs, either as [nums[i], nums[i+1]] or [nums[i+1], nums[i]]. The pairs can appear in any order.
Return the original array nums. If there are multiple solutions, return any of them.

**Examples**

**Example 1:**

```
Input: adjacentPairs = [[2,1],[3,4],[3,2]]
Output: [1,2,3,4]
Explanation: This array has all its adjacent pairs in adjacentPairs.
Notice that adjacentPairs[i] may not be in left-to-right order.
```

**Example 2:**

```
Input: adjacentPairs = [[4,-2],[1,4],[-3,1]]
Output: [-2,4,1,-3]
Explanation: There can be negative numbers.
Another solution is [-3,1,4,-2], which would also be accepted.
```

**Example 3:**

```
Input: adjacentPairs = [[100000,-100000]]
Output: [100000,-100000]
```

**Constraints**

- nums.length == n
- adjacentPairs.length == n - 1
- adjacentPairs[i].length == 2
- 2 <= n <= 105
- -105 <= nums[i], ui, vi <= 105
- There exists some nums that has adjacentPairs as its pairs.

---

## 题目（中文翻译）

有一个整数数组（integer array）`nums`，其中包含 `n` 个唯一元素（unique elements），但你已经忘记了它的具体内容。幸运的是，你记得 `nums` 中所有相邻元素的配对信息。

给定一个大小为 `n - 1` 的二维整数数组（2D integer array）`adjacentPairs`，其中 `adjacentPairs[i] = [ui, vi]` 表示元素 `ui` 与 `vi` 在 `nums` 中是相邻的。已知 `nums` 中每一对相邻元素 `nums[i]` 与 `nums[i+1]` 必然出现在 `adjacentPairs` 中，形式可以是 `[nums[i], nums[i+1]]` 或 `[nums[i+1], nums[i]]`。这些配对的出现顺序任意。

返回原始数组 `nums`。如果存在多种可能的答案，返回任意一种即可。

### 示例

#### 示例 1
**输入:** `adjacentPairs = [[2,1],[3,4],[3,2]]`  
**输出:** `[1,2,3,4]`  
**解释:** 该数组的所有相邻数对都出现在 `adjacentPairs` 中。需要注意的是，`adjacentPairs[i]` 未必按左到右的顺序给出。

#### 示例 2
**输入:** `adjacentPairs = [[4,-2],[1,4],[-3,1]]`  
**输出:** `[-2,4,1,-3]`  
**解释:** 数组中可以出现负数。另一种可接受的答案是 `[-3,1,4,-2]`。

#### 示例 3
**输入:** `adjacentPairs = [[100000,-100000]]`  
**输出:** `[100000,-100000]`

### 约束条件
- `nums.length == n`
- `adjacentPairs.length == n - 1`
- `adjacentPairs[i].length == 2`
- `2 <= n <= 10^5`
- `-10^5 <= nums[i], ui, vi <= 10^5`
- 必定存在至少一个满足条件的 `nums`，其相邻数对即为 `adjacentPairs`。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把所有可能的排列都枚举出来，然后检查每一种排列的相邻元素是否都出现在 `adjacentPairs` 中。  

- **枚举排列**：把长度为 `n` 的未知数组 `nums` 看成 `n` 个不同的数字的全排列。  
- **检查合法性**：遍历每一种排列，对每个相邻位置 `i,i+1`，查看 `[nums[i], nums[i+1]]`（顺序可以换成 `[nums[i+1], nums[i]]`）是否在给出的 `adjacentPairs` 里。  

这里用到的唯一数据结构是 **哈希表**（Python 的 `set`），它就像一本查字典：  
- `key` 是一对相邻数字的**有序**或**无序**形式（我们统一存成 `frozenset`），  
- `value` 只需要知道这对数字是否出现过，所以用 `set` 的“存在性查询”即可。  

因为只要找到一种满足所有相邻对的排列就可以返回，**只要遍历完所有排列**（最坏情况）就一定能找到答案（题目保证答案一定存在）。  

#### 代码（Python）  

```python
from itertools import permutations
from typing import List

def restoreArray_bruteforce(adjacentPairs: List[List[int]]) -> List[int]:
    # 把每一对无序化后放进集合，后面检查时只要看这对是否在集合里即可
    pair_set = {frozenset(p) for p in adjacentPairs}   # 哈希表：存在性查询

    n = len(adjacentPairs) + 1           # 原数组长度
    # 先把所有出现过的数字收集起来，后面只在这些数字上枚举排列
    nums_candidates = {x for pair in adjacentPairs for x in pair}

    # 用 itertools.permutations 产生所有可能的排列（暴力枚举）
    for perm in permutations(nums_candidates, n):
        ok = True
        # 检查相邻两个数是否都在 pair_set 里
        for i in range(n - 1):
            if frozenset((perm[i], perm[i + 1])) not in pair_set:
                ok = False
                break
        if ok:                # 找到合法的排列，直接返回
            return list(perm)

    # 题目保证一定有解，这里不会被执行
    return []
```

> **关键行注释**  
> - `pair_set = {frozenset(p) for p in adjacentPairs}`：把每一对变成无序集合，放进哈希表，查询 O(1)。  
> - `for perm in permutations(nums_candidates, n):`：暴力遍历所有 `n!` 种排列。  
> - `if frozenset((perm[i], perm[i + 1])) not in pair_set:`：检查相邻是否匹配。  

#### 复杂度  

- **时间复杂度**：`O(n! * n)`  
  - `n!` 是所有排列的数量，`n` 是每次检查相邻对的时间。  
  - 用大白话说，就是“先把所有可能的顺序列出来（这一步已经非常慢），再逐个验证”。  
- **空间复杂度**：`O(n)`  
  - 只用了存放所有出现过的数字的集合和 `pair_set`（大小都是 `O(n)`），以及递归产生的排列（Python 的 `permutations` 是惰性生成的）。  

> 由于 `n` 最多可达 `10⁵`，这套暴力方法根本不可行，只是帮助大家理解最“笨”的思路。  

---  

### 2. 最优解  

#### 思路  

从暴力解我们可以看到，**枚举所有排列是最耗时的**，真正的难点在于 **怎么快速找到正确的顺序**。  
观察题目可以得到以下关键信息：

1. **每个数只会出现在两条相邻对里**（因为数组是线性的），**端点**（数组第一个和最后一个）只会出现在 **一条** 相邻对里。  
2. 把每条相邻对看成 **无向边**，所有数字看成 **节点**，则整个结构恰好是一条 **链**（一条没有分叉的路径）。  
3. 找到链的任意一个端点后，只要沿着 “相邻” 的方向一步步走，就能恢复完整的数组。  

基于上述观察，优化思路如下：

- **步骤 1：建立哈希表（邻接表）**  
  用 `defaultdict(list)` 把每个数字映射到它的相邻数字列表。  
  类比：这就像一本“谁和谁是好邻居”的小册子，`key` 是某个人，`value` 是他的邻居们。  

- **步骤 2：找到端点**  
  扫描哈希表，出现一次的数字即为链的端点（度为 1 的节点）。  

- **步骤 3：顺序重建**  
  从端点开始，按如下规则往后走：  
  - 当前数字的邻居有 **两个**（普通节点）或 **一个**（端点）。  
  - 已经放进答案的数字不再回头（使用前一个数字来判断下一个）。  
  - 把下一个未访问的邻居加入答案，继续前进。  

整个过程只遍历一次 `adjacentPairs`，时间线性。  

#### 代码（Python）  

```python
from collections import defaultdict
from typing import List

def restoreArray(adjacentPairs: List[List[int]]) -> List[int]:
    # 1. 建立邻接表：每个数对应它的相邻数列表
    graph = defaultdict(list)          # 哈希表：key 是数字，value 是邻居列表
    for u, v in adjacentPairs:
        graph[u].append(v)              # u 的邻居加 v
        graph[v].append(u)              # v 的邻居加 u（无向图）

    # 2. 找到度为 1 的端点（数组的第一个元素）
    start = None
    for node, neigh in graph.items():
        if len(neigh) == 1:             # 只出现一次的数字就是端点
            start = node
            break

    n = len(adjacentPairs) + 1          # 原数组长度
    ans = [0] * n                       # 预分配答案数组，提升速度
    ans[0] = start

    # 3. 按顺序遍历链条
    # prev 用来记录上一个已经放进答案的数字，防止回头
    prev = None
    cur = start
    for i in range(1, n):
        # 当前数字的邻居们
        neighbors = graph[cur]
        # 在邻居里挑出那个不是上一个的，就是下一个
        nxt = neighbors[0] if neighbors[0] != prev else neighbors[1] if len(neighbors) > 1 else None
        ans[i] = nxt
        # 更新 prev、cur，继续前进
        prev, cur = cur, nxt

    return ans
```

> **关键行注释**  
> - `graph = defaultdict(list)`：哈希表的“邻接表”，把每条边存两次，类似“谁和谁是好邻居”。  
> - `if len(neigh) == 1:`：度为 1 的节点就是链的端点。  
> - `nxt = neighbors[0] if neighbors[0] != prev else neighbors[1]`：从当前节点的邻居中挑出“不是刚才来的那个”，这一步相当于“往前走”。  

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 建图遍历 `adjacentPairs` 一次 `O(n)`，  
  - 找端点、顺序重建各自也是一次线性遍历 `O(n)`。  
  - 用大白话说，就是“只走了一遍所有相邻对”，比暴力的 “尝遍所有排列” 快了天文倍数。  

- **空间复杂度**：`O(n)`  
  - `graph` 存储每个数字的邻居，总共 `2·(n‑1)` 条记录，规模正比于 `n`。  
  - 额外的答案数组也占 `O(n)` 空间。  

---  

## 心得  

- **核心技巧**：把相邻对视作无向图的边，利用「度为 1 的节点是链的端点」的性质，从端点沿着唯一的路径重建数组。  
- **适用题型**：  
  1. “恢复链表/数组” 类问题（如 LeetCode 1734. 解码异或数组）  
  2. “从边信息恢复节点顺序” 的图题（如 1657. 确定二叉树的根节点）  
  3. “找出路径的两端点” 的题目（如 1436. 旅行终点站）  
- **一句话总结**：**把相邻对当作链的边，先找端点再顺着唯一路径走完，就是答案。**  

## 反思  

- **第一反应**：看到「相邻」这两个字就想到「图」——把每对数字看成连在一起的边。  
- **最容易踩的坑**  
  - 忘记把相邻对存成 **无向** 的邻接表，只记了单向会导致找不到另一端点。  
  - 在遍历链时没有记录上一个节点，导致在度为 2 的普通节点处来回跳，形成死循环。  
  - 边界条件：`n = 2` 时，只有一条边，代码里 `neighbors[1]` 会越界，需要额外判断。  
- **下次类似题的第一步**：**先检查度数**（每个节点出现几次），找出度为 1 的端点，再利用唯一路径的特性顺序恢复。