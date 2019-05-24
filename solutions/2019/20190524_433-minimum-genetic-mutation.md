# #433. 最小基因突变 / Minimum Genetic Mutation

> 难度：中等 · 标签：Hash Table、String、Breadth-First Search · [LeetCode 链接](https://leetcode.com/problems/minimum-genetic-mutation/)

---

## 题目（英文原版）

**Description**

A gene string can be represented by an 8-character long string, with choices from 'A', 'C', 'G', and 'T'.
Suppose we need to investigate a mutation from a gene string startGene to a gene string endGene where one mutation is defined as one single character changed in the gene string.
There is also a gene bank bank that records all the valid gene mutations. A gene must be in bank to make it a valid gene string.
Given the two gene strings startGene and endGene and the gene bank bank, return the minimum number of mutations needed to mutate from startGene to endGene. If there is no such a mutation, return -1.
Note that the starting point is assumed to be valid, so it might not be included in the bank.

**Examples**

**Example 1:**

```
Input: startGene = "AACCGGTT", endGene = "AACCGGTA", bank = ["AACCGGTA"]
Output: 1
```

**Example 2:**

```
Input: startGene = "AACCGGTT", endGene = "AAACGGTA", bank = ["AACCGGTA","AACCGCTA","AAACGGTA"]
Output: 2
```

**Constraints**

- 0 <= bank.length <= 10
- startGene.length == endGene.length == bank[i].length == 8
- startGene, endGene, and bank[i] consist of only the characters ['A', 'C', 'G', 'T'].

---

## 题目（中文翻译）

**描述**  
基因字符串（gene string）可以用长度为 8 的字符序列表示，字符只能是 `'A'`, `'C'`, `'G'`, 和 `'T'`。  
假设我们需要研究从基因字符串 `startGene` 到基因字符串 `endGene` 的突变过程，其中一次突变（mutation）定义为基因字符串中恰好改变一个字符。  
还有一个基因库（gene bank） `bank`，记录了所有合法的基因突变。一个基因只有出现在基因库中才算是合法基因字符串（valid gene string）。  
给定起始基因 `startGene`、目标基因 `endGene` 以及基因库 `bank`，返回将 `startGene` 突变为 `endGene` 所需的最少突变次数。如果不存在这样的突变路径，返回 `-1`。  
注意，起始基因默认是合法的，所以它可能不在基因库中。

**示例**  

*示例 1*  
```
Input: startGene = "AACCGGTT", endGene = "AACCGGTA", bank = ["AACCGGTA"]
Output: 1
```

*示例 2*  
```
Input: startGene = "AACCGGTT", endGene = "AAACGGTA", bank = ["AACCGGTA","AACCGCTA","AAACGGTA"]
Output: 2
```

**约束条件**  
- `0 <= bank.length <= 10`  
- `startGene.length == endGene.length == bank[i].length == 8`  
- `startGene`, `endGene` 和 `bank[i]` 仅由字符 `'A'`, `'C'`, `'G'`, `'T'` 组成

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的基因序列都枚举出来**，然后检查从 `startGene` 到 `endGene` 的每一种可能路径是否只经过银行 `bank` 中出现的基因。  
具体可以这样做：

1. **把 bank 当成集合**（就像查字典一样，键是基因序列，值是“这条基因是合法的”。）  
2. 用 **深度优先搜索（DFS）** 从 `startGene` 逐个尝试把每一个字符换成 `'A','C','G','T'`（共 4 种可能），形成新的基因。  
3. 如果新基因在 bank 中且没有访问过，就继续往下搜索，直到找到 `endGene` 为止。  
4. 在搜索的过程中记录已经走过的步数，遍历完所有路径后取最小的步数。  

为什么这能得到答案？

- 每一步我们只允许把一个字符改成另外三个合法字符（因为改成自己不算是“突变”），所以搜索的每条路径恰好对应一次合法的基因突变序列。  
- 只要路径中的每个基因都在 bank 里，题目就说它们是“有效的”。因此遍历所有合法路径即可找到最短的那条。

> **注意**：这里的暴力解会尝试 **所有可能的基因组合**（最多 `4^8 = 65536` 种），并且在每条路径上进行深度遍历，时间会很慢。

#### 代码（Python）

```python
from typing import List

def minMutation_brute(start: str, end: str, bank: List[str]) -> int:
    # 把 bank 放进集合，查找 O(1)（像查字典一样）
    valid = set(bank)
    if end not in valid:          # 终点不在合法集合里，直接返回 -1
        return -1

    min_steps = float('inf')      # 用来记录找到的最小步数
    visited = set()               # 防止在同一条路径上循环

    # 辅助函数：DFS 搜索
    def dfs(cur: str, steps: int):
        nonlocal min_steps
        # 剪枝：已经比当前最小步数更大，直接返回
        if steps >= min_steps:
            return
        if cur == end:            # 找到终点，更新最小步数
            min_steps = steps
            return

        # 尝试把每一个位置的字符换成 A/C/G/T
        for i in range(len(cur)):
            for ch in "ACGT":
                if ch == cur[i]:
                    continue      # 换成自己不算突变
                nxt = cur[:i] + ch + cur[i+1:]  # 生成新基因
                if nxt in valid and nxt not in visited:
                    visited.add(nxt)            # 标记为已访问
                    dfs(nxt, steps + 1)         # 继续向下搜索
                    visited.remove(nxt)         # 回溯，撤销访问标记

    visited.add(start)
    dfs(start, 0)

    return -1 if min_steps == float('inf') else min_steps
```

#### 复杂度

- **时间复杂度**：`O(4^L * L)`（`L = 8` 为基因长度）  
  - 解释：每个字符有 4 种可能，总共有 `4^8` 种基因组合。对每个基因我们都要遍历 `L` 位字符来生成新基因，所以乘以 `L`。在最坏情况下（所有组合都是合法的），搜索会遍历全部组合，故时间会呈指数级增长。

- **空间复杂度**：`O(4^L)`  
  - 解释：递归栈深度最坏可以达到所有基因的数量（即所有组合），再加上 `visited` 集合保存已经访问的基因，空间随搜索的分支数线性增长。

> 对于本题的约束（`bank` 最多只有 10 条），暴力解在实际运行时还能接受，但如果约束放宽就会超时。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **“遍历所有可能的基因组合”**，而我们只关心 **银行里出现的基因**。  
因此我们可以把 **每一次合法突变看成图中的一条边**，把所有合法基因（`startGene`、`endGene`、以及 `bank` 中的基因）看成 **图的节点**。  

- 两个基因之间**相邻**（可以直接突变），当且仅当它们的字符串只相差 **恰好一个字符**。  
- 求最少突变次数，就等价于在这张无向图中求 **最短路径**，起点是 `startGene`，终点是 `endGene`。

**最短路径**的经典算法是 **广度优先搜索（BFS）**，它一次层层展开，第一次碰到终点时的层数就是最短路径长度。  

实现步骤：

1. 把 `bank` 放进集合 `valid`（字典查找 O(1)）。如果 `endGene` 不在集合里，直接返回 `-1`（因为终点本身不合法）。
2. 初始化 BFS 队列 `queue`，放入 `(startGene, 0)`，其中 `0` 表示已经走了 0 步。
3. 当队列不为空时，弹出当前基因 `cur` 与已走步数 `step`。
4. **枚举所有可能的下一步基因**：遍历 8 个位置，分别尝试把字符换成 `'A','C','G','T'`（除去原字符），得到新基因 `next_gene`。
5. 如果 `next_gene` 在 `valid` 中且未访问过：
   - 若 `next_gene == endGene`，返回 `step + 1`（因为这一步已经完成突变）。
   - 否则把 `next_gene` 加入队列并标记已访问，继续搜索。
6. 如果 BFS 结束仍未找到终点，返回 `-1`。

> **为什么 BFS 能保证最短？**  
> BFS 按层展开：第一次遍历完所有“0 步能到达的基因”，再遍历所有“1 步能到达的基因”，以此类推。于是第一次遇到终点的那层，就是最少突变次数。

#### 代码（Python）

```python
from collections import deque
from typing import List

def minMutation(start: str, end: str, bank: List[str]) -> int:
    # 1. 把 bank 放进集合，查询快（像查字典）
    valid = set(bank)
    if end not in valid:                 # 终点不合法，直接返回 -1
        return -1

    # 2. BFS 初始化
    queue = deque()
    queue.append((start, 0))             # (当前基因, 已走步数)
    visited = set([start])               # 已访问的基因

    # 3. BFS 主循环
    while queue:
        cur, step = queue.popleft()
        # 4. 枚举所有可能的下一个基因
        for i in range(len(cur)):        # 基因长度固定为 8
            for ch in "ACGT":
                if ch == cur[i]:
                    continue            # 换成自己不算突变
                nxt = cur[:i] + ch + cur[i+1:]  # 生成新基因

                # 5. 只关心合法且未访问过的基因
                if nxt in valid and nxt not in visited:
                    if nxt == end:        # 找到终点，返回步数+1
                        return step + 1
                    visited.add(nxt)     # 标记访问
                    queue.append((nxt, step + 1))

    # 6. BFS 结束仍未找到，说明无解
    return -1
```

#### 复杂度

- **时间复杂度**：`O(M * L * 4)`，其中 `M = len(bank)`（最多 10），`L = 8` 为基因长度。  
  - 解释：每次从队列里弹出一个基因，我们会遍历它的每个位置（`L`）并尝试 4 种字符，生成最多 `L*3`（因为去掉原字符）个新基因。每个新基因只会被检查一次（因为用 `visited` 防重），所以总体是 `O(M * L * 4)`，在本题约等于常数级别。

- **空间复杂度**：`O(M)`  
  - 解释：`valid` 集合、`visited` 集合以及 BFS 队列最多存放所有合法基因，数量不超过 `M + 2`（包括 `start` 与 `end`），因此空间随 `bank` 大小线性增长。

> 与暴力解相比，最优解只在 **合法基因集合** 上做搜索，避免了遍历所有 `4^8` 种组合，速度提升几个数量级。

---

## 心得

- **核心技巧**：把“每一次合法突变”抽象为图的**邻接关系**，使用**广度优先搜索（BFS）**求最短路径。  
- **适用场景**：  
  1. **单词接龙**（Word Ladder）——把每次只改一个字母的单词视为图的边。  
  2. **最少转换次数**（如把一个数字变成另一个数字，每次只能加减固定值且必须在合法集合中）。  
  3. **棋盘最短路径**（仅允许合法格子移动），同样可以用 BFS。  
- **一句话总结**：把合法基因看成图的节点，BFS 把“层数”直接映射为最少突变次数，即是解题钥匙。

---

## 反思

- **第一反应**：看到“每次只能改一个字符”，自然想到**枚举所有可能的变换**，于是想到 DFS 暴力搜索。  
- **最容易踩的坑**：  
  - **终点不在 bank** 时直接返回 `-1`，否则会在 BFS 中永远找不到。  
  - **重复访问**：没有 `visited` 集合会导致无限循环或大量冗余搜索。  
  - **字符换成自身**：在枚举时一定要跳过 `ch == cur[i]`，否则会把同一个基因当成一次突变，导致步数错误。  
- **下次遇到同类题**：第一步先思考**“有没有可以抽象成图的结构？”**，如果可以，用 **BFS**（或 DFS）在合法节点集合上搜索最短路径。这样可以迅速定位最优解的方向。