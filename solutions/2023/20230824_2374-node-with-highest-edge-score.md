# #2374. 边缘分数最高的节点 / Node With Highest Edge Score

> 难度：中等 · 标签：Hash Table、Graph · [LeetCode 链接](https://leetcode.com/problems/node-with-highest-edge-score/)

---

## 题目（英文原版）

**Description**

You are given a directed graph with n nodes labeled from 0 to n - 1, where each node has exactly one outgoing edge.
The graph is represented by a given 0-indexed integer array edges of length n, where edges[i] indicates that there is a directed edge from node i to node edges[i].
The edge score of a node i is defined as the sum of the labels of all the nodes that have an edge pointing to i.
Return the node with the highest edge score. If multiple nodes have the same edge score, return the node with the smallest index.

**Examples**

**Example 1:**

```
Input: edges = [1,0,0,0,0,7,7,5]
Output: 7
Explanation:
- The nodes 1, 2, 3 and 4 have an edge pointing to node 0. The edge score of node 0 is 1 + 2 + 3 + 4 = 10.
- The node 0 has an edge pointing to node 1. The edge score of node 1 is 0.
- The node 7 has an edge pointing to node 5. The edge score of node 5 is 7.
- The nodes 5 and 6 have an edge pointing to node 7. The edge score of node 7 is 5 + 6 = 11.
Node 7 has the highest edge score so return 7.
```

**Example 2:**

```
Input: edges = [2,0,0,2]
Output: 0
Explanation:
- The nodes 1 and 2 have an edge pointing to node 0. The edge score of node 0 is 1 + 2 = 3.
- The nodes 0 and 3 have an edge pointing to node 2. The edge score of node 2 is 0 + 3 = 3.
Nodes 0 and 2 both have an edge score of 3. Since node 0 has a smaller index, we return 0.
```

**Constraints**

- n == edges.length
- 2 <= n <= 105
- 0 <= edges[i] < n
- edges[i] != i

---

## 题目（中文翻译）

给定一个 **有向图（directed graph）**，包含 `n` 个节点，节点编号为 `0` 到 `n-1`，且每个节点恰好有一条出边（outgoing edge）。  
图由长度为 `n` 的 **整数数组（integer array）** `edges` 表示，其中 `edges[i]` 表示从节点 `i` 指向节点 `edges[i]` 的有向边。

**边缘分数（edge score）** 定义为指向该节点的所有节点编号之和。  
返回边缘分数最高的节点编号。如果有多个节点的边缘分数相同，返回编号最小的节点。

---

## 示例

### 示例 1
```text
Input: edges = [1,0,0,0,0,7,7,5]
Output: 7
Explanation:
- 节点 1、2、3、4 均有一条指向节点 0 的边。节点 0 的边缘分数为 1 + 2 + 3 + 4 = 10。
- 节点 0 有一条指向节点 1 的边。节点 1 的边缘分数为 0。
- 节点 7 有一条指向节点 5 的边。节点 5 的边缘分数为 7。
- 节点 5、6 均有一条指向节点 7 的边。节点 7 的边缘分数为 5 + …
```

### 示例 2
```text
Input: edges = [2,0,0,2]
Output: 0
Explanation:
- 节点 1、2 均有一条指向节点 0 的边。节点 0 的边缘分数为 1 + 2 = 3。
- 节点 0、3 均有一条指向节点 2 的边。节点 2 的边缘分数为 0 + 3 = 3。
节点 0 与节点 2 的边缘分数均为 3。由于节点 0 的编号更小，返回 0。
```

---

## 约束条件

- `n == edges.length`
- `2 <= n <= 10^5`
- `0 <= edges[i] < n`
- `edges[i] != i`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目给出一个 **有向图**，每个节点恰好有一条指向别人的边。  
我们要算出每个节点的 **edge score**：所有指向它的节点编号之和。

最直接的想法是：

1. 对每个可能的目标节点 `i`（`0 … n-1`），遍历全部节点 `j`，检查 `edges[j]` 是否等于 `i`。  
2. 若相等，就把 `j` 加到 `i` 的分数里。  
3. 最后比较所有分数，取最大的那个（若相同取下标最小的）。

> **类比**：想象我们有一本 **电话簿**，每个人只记了自己打给谁的电话号码。要统计“谁收到的来电最多”，最笨的办法就是把每个人的记录都拿出来，逐一核对是否是同一个人收到的来电。

这个办法一定能得到正确答案，因为我们把 **所有** 边都检查了一遍，保证没有漏掉任何指向某节点的边。

#### 代码（Python）

```python
def nodeWithHighestEdgeScore_bruteforce(edges):
    n = len(edges)
    # 用一个长度为 n 的列表记录每个节点的 edge score
    scores = [0] * n

    # 对每个目标节点 i，遍历所有起点 j，统计指向 i 的节点编号之和
    for i in range(n):                     # 目标节点
        total = 0
        for j in range(n):                 # 所有可能的起点
            if edges[j] == i:               # 若 j 指向 i
                total += j                 # 把 j 加到 i 的分数里
        scores[i] = total                  # 保存 i 的 edge score

    # 找出分数最高且下标最小的节点
    max_score = -1
    answer = 0
    for i, sc in enumerate(scores):
        if sc > max_score:                  # 分数更大就更新
            max_score = sc
            answer = i
    return answer
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  解释：外层遍历 `n` 次，内层每次也要遍历 `n` 次，等价于 **“把 n × n 张纸全部翻一遍”**，所以时间随 `n` 的平方增长。

- **空间复杂度**：`O(n)`  
  只用了一个长度为 `n` 的 `scores` 数组来存每个节点的分数，除此之外几乎不占额外空间。  

> 对于 `n` 可达 `10⁵` 的情况，`n²`（≈ 10¹⁰）的操作量会严重超时，这就是暴力解的 **瓶颈**。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正需要的操作只有一次遍历**：每条边只会把它的起点编号加入一次目标节点的分数。  
因此我们可以在 **一次遍历** 中完成累计，而不必对每个目标节点再去遍历所有起点。

具体做法：

1. 准备一个长度为 `n` 的数组 `score`，`score[i]` 用来记录节点 `i` 的 edge score。  
2. 遍历数组 `edges`，下标 `i` 表示起点，`edges[i]` 表示终点。  
   - 把 `i`（起点编号）加到 `score[edges[i]]` 上。  
   - 这一步相当于 “把每个人的来电号码直接记到被叫人的账本里”。  
3. 遍历完后，`score` 中已经存好了所有节点的分数。再一次线性扫描找出 **最大分数且下标最小** 的节点即可。

> **类比**：想象有一张 **收款本**，每个人只在本子上写下自己付了多少钱（这里是自己的编号）。我们只需要把每个人的这笔记录 **直接记到收款本对应的收款人** 那一栏，最后再找出收款最多的人。

关键点：

- **哈希表/数组**：这里用数组当作哈希表，`score[x]` 就像字典中 “键 = x，值 = 当前累计的分数”。  
- **一次遍历**：每条边只处理一次，时间线性。  
- **注意整数范围**：`n` 可达 `10⁵`，每个节点编号最大 `10⁵-1`，累计可能达到 `~10¹⁰`，超过 32 位整数，需要使用 Python 的大整数（默认支持），在其它语言要用 `long long`。

#### 代码（Python）

```python
def nodeWithHighestEdgeScore(edges):
    """
    返回 edge score 最高的节点下标（若相同返回最小下标）。
    时间复杂度 O(n) ，空间复杂度 O(n)。
    """
    n = len(edges)
    # score[i] 保存节点 i 的 edge score，初始为 0
    score = [0] * n

    # 遍历每条有向边：i -> edges[i]
    for i, to in enumerate(edges):
        # 把起点 i 加到终点 to 的累计分数里
        score[to] += i          # 这里 i 是整数，Python 自动处理大数

    # 找出分数最高且下标最小的节点
    max_score = -1
    answer = 0
    for idx, sc in enumerate(score):
        # 如果当前分数更大，或者分数相同但下标更小（因为我们是从小到大遍历，直接用 > 即可）
        if sc > max_score:
            max_score = sc
            answer = idx
    return answer
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  只遍历了两遍数组（一次累计，一次找最大），**线性**增长。对 `n = 10⁵` 也能在毫秒级完成。

- **空间复杂度**：`O(n)`  
  需要一个长度为 `n` 的 `score` 数组来存每个节点的分数。若想进一步省空间，可以在遍历时直接记录当前最大值而不保存全部分数，但代码可读性会下降，这里保持 `O(n)` 更直观。

> 与暴力解相比，时间从 **“每个节点都要检查 n 次”** 降到了 **“每条边只处理一次”**，提升了 **n 倍**。

---

## 心得

- **核心技巧**：**一次遍历累计**（利用数组/哈希表把“入度贡献”直接加到对应节点）。
- **适用题型**：
  1. “统计入度/出度之和” 类问题（如 **Find the Town Judge**、**Maximum In-Degree**）。
  2. “根据每条边的权重累计到节点” 的场景（如 **Maximum Subarray Sum on Graph**）。
- **一句话总结**：**把每条边的起点直接“投票”到终点，用数组一次性收集所有投票，最后挑最高分即可。**

---

## 反思

- **第一反应**：看到“每个节点只有一条出边”，立刻想到可以 **遍历一次** 把所有信息累加进去，而不是逐个节点去找入边。
- **最容易踩的坑**：
  1. **整数溢出**：累计分数可能超过 32 位整数，需要使用大整数（Python 自动处理，C++/Java 需要 `long long` / `long`）。
  2. **平分情况**：多个节点分数相同时，要返回下标最小的，遍历时使用 `>`（而不是 `>=`）即可自然保留最先出现的下标。
  3. **边界条件**：`edges[i] != i` 保证没有自环，但代码不依赖此假设，仍然能正常工作。
- **下次思路**：看到“每条边只涉及两个节点，且只需要统计某种累计值”，第一步就考虑 **使用数组/哈希表一次遍历累计**，再在遍历结束后做一次线性扫描找答案。这样常能把原本的 `O(n²)` 降到 `O(n)`。