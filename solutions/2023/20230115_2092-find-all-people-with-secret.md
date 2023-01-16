# #2092. 寻找所有知道秘密的人 / Find All People With Secret

> 难度：困难 · 标签：Depth-First Search、Breadth-First Search、Union Find、Graph、Sorting · [LeetCode 链接](https://leetcode.com/problems/find-all-people-with-secret/)

---

## 题目（英文原版）

**Description**

You are given an integer n indicating there are n people numbered from 0 to n - 1. You are also given a 0-indexed 2D integer array meetings where meetings[i] = [xi, yi, timei] indicates that person xi and person yi have a meeting at timei. A person may attend multiple meetings at the same time. Finally, you are given an integer firstPerson.
Person 0 has a secret and initially shares the secret with a person firstPerson at time 0. This secret is then shared every time a meeting takes place with a person that has the secret. More formally, for every meeting, if a person xi has the secret at timei, then they will share the secret with person yi, and vice versa.
The secrets are shared instantaneously. That is, a person may receive the secret and share it with people in other meetings within the same time frame.
Return a list of all the people that have the secret after all the meetings have taken place. You may return the answer in any order.

**Examples**

**Example 1:**

```
Input: n = 6, meetings = [[1,2,5],[2,3,8],[1,5,10]], firstPerson = 1
Output: [0,1,2,3,5]
Explanation:
At time 0, person 0 shares the secret with person 1.
At time 5, person 1 shares the secret with person 2.
At time 8, person 2 shares the secret with person 3.
At time 10, person 1 shares the secret with person 5.​​​​
Thus, people 0, 1, 2, 3, and 5 know the secret after all the meetings.
```

**Example 2:**

```
Input: n = 4, meetings = [[3,1,3],[1,2,2],[0,3,3]], firstPerson = 3
Output: [0,1,3]
Explanation:
At time 0, person 0 shares the secret with person 3.
At time 2, neither person 1 nor person 2 know the secret.
At time 3, person 3 shares the secret with person 0 and person 1.
Thus, people 0, 1, and 3 know the secret after all the meetings.
```

**Example 3:**

```
Input: n = 5, meetings = [[3,4,2],[1,2,1],[2,3,1]], firstPerson = 1
Output: [0,1,2,3,4]
Explanation:
At time 0, person 0 shares the secret with person 1.
At time 1, person 1 shares the secret with person 2, and person 2 shares the secret with person 3.
Note that person 2 can share the secret at the same time as receiving it.
At time 2, person 3 shares the secret with person 4.
Thus, people 0, 1, 2, 3, and 4 know the secret after all the meetings.
```

**Constraints**

- 2 <= n <= 105
- 1 <= meetings.length <= 105
- meetings[i].length == 3
- 0 <= xi, yi <= n - 1
- xi != yi
- 1 <= timei <= 105
- 1 <= firstPerson <= n - 1

---

## 题目（中文翻译）

**题目描述**  
给定一个整数 `n`，表示有 `n` 个人，编号为 `0` 到 `n - 1`。还给定一个下标从 `0` 开始的二维整数数组 `meetings`，其中 `meetings[i] = [xi, yi, timei]` 表示编号为 `xi` 的人和编号为 `yi` 的人在 `timei` 时刻进行了一次会面。一个人可以在同一时刻参加多场会面。最后，给定一个整数 `firstPerson`。

人 `0` 拥有一个秘密，并在时间 `0` 时立即将该秘密分享给 `firstPerson`。此后，每当有会面发生，若会面中的任意一方已经拥有该秘密，则会立刻把秘密分享给另一方。形式化地，对于每场会面，如果人在 `timei` 时刻拥有秘密，则他们会把秘密分享给会面的另一人，反之亦然。

秘密的分享是瞬时完成的，即一个人在同一时间点接收到秘密后，可以立即在该时间点的其他会面中再次分享。

返回所有在所有会面结束后拥有该秘密的人的编号列表，答案可以按任意顺序返回。

---

**示例 1**  
```text
Input: n = 6, meetings = [[1,2,5],[2,3,8],[1,5,10]], firstPerson = 1
Output: [0,1,2,3,5]
Explanation:
At time 0, person 0 shares the secret with person 1.
At time 5, person 1 shares the secret with person 2.
At time 8, person 2 shares the secret with person 3.
At time 10, person 1 shares the secret with person 5.
Thus, people 0, 1, 2, 3, and 5 know the secret after all the meetings.
```

**示例 2**  
```text
Input: n = 4, meetings = [[3,1,3],[1,2,2],[0,3,3]], firstPerson = 3
Output: [0,1,3]
Explanation:
At time 0, person 0 shares the secret with person 3.
At time 2, neither person 1 nor person 2 know the secret.
At time 3, person 3 shares the secret with person 0 and person 1.
Thus, people 0, 1, and 3 know the secret after all the meetings.
```

**示例 3**  
```text
Input: n = 5, meetings = [[3,4,2],[1,2,1],[2,3,1]], firstPerson = 1
Output: [0,1,2,3,4]
Explanation:
At time 0, person 0 shares the secret with person 1.
At time 1, person 1 shares the secret with person 2, and person 2 shares the secret with person 3.
Note that person 2 can share the secret at the same time as receiving it.
At time 2, person 3 shares the secret with person 4.
Thus, people 0, 1, 2, 3, 4 know the secret after all the meetings.
```

---

**约束条件**  
- `2 <= n <= 10^5`
- `1 <= meetings.length <= 10^5`
- `meetings[i].length == 3`
- `0 <= xi, yi <= n - 1`
- `xi != yi`
- `1 <= timei <= 10^5`
- `1 <= firstPerson <= n - 1`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有会议按时间顺序排好**，然后从时间 0 开始，一场一场地模拟信息的传播。  
- 维护一个 `has_secret[i]` 布尔数组，`True` 表示第 `i` 个人已经知道秘密。  
- 初始时 `has_secret[0] = has_secret[firstPerson] = True`（0 点把秘密直接告诉 `firstPerson`）。  
- 按时间遍历每个会议 `[x, y, t]`：  
  - 如果 `has_secret[x]` 或 `has_secret[y]` 为 `True`，说明这场会议里有人已经知道秘密，立刻把它传给对方（把两个位置都设为 `True`）。  
- 为了满足 “同一时间内收到秘密的人可以立刻再传给同时间的其他会议” 的要求，**在处理完同一时间的所有会议后**，我们需要再遍历一次这些会议，直到本时间段内再也没有人可以被新增为 `True` 为止。  

这就是“暴力”做法：每个时间段都要 **反复扫描** 该时间段的所有会议，直到没有新的传播发生。  

> **类比**：把每个人想象成字典里的词，`has_secret` 就是词典里是否已经标记了“已知”。每次会议像是把两个词的页码互相抄写，一旦某个词被标记，所有和它同页的词都要重新检查一遍。

**为什么正确**  
只要遍历顺序是时间递增，并且在同一时间内把所有可能的传播都穷举完，就不会遗漏任何一次“即时”传递。因为所有会议都是离散的、时间是整数，最多只需要在同一时间段内做若干次“传播闭合”。

**时间/空间复杂度**  
- 假设有 `m = len(meetings)` 场会议。最坏情况下，同一时间会出现 `O(m)` 场会议，每次都要遍历全部 `m` 场才能收敛，导致 **时间复杂度 O(m²)**。  
- 只用了一个长度为 `n` 的布尔数组，**空间复杂度 O(n)**。

> **大白话解释**：`O(m²)` 就像你有 10 000 场会议，程序要跑 10 000 × 10 000 = 1 亿 次检查，显然太慢了。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def findAllPeople_bruteforce(n: int, meetings: List[List[int]], firstPerson: int) -> List[int]:
    # 1. 按时间排序，方便分组
    meetings.sort(key=lambda x: x[2])

    # 2. secret[i] == True 表示 i 已经知道秘密
    secret = [False] * n
    secret[0] = secret[firstPerson] = True   # 时间 0 的分享

    i = 0
    while i < len(meetings):
        # 取出时间相同的一批会议
        cur_time = meetings[i][2]
        same_time = []
        while i < len(meetings) and meetings[i][2] == cur_time:
            same_time.append(meetings[i])
            i += 1

        # 3. 在这段时间里不断传播，直到不再有新增
        changed = True
        while changed:
            changed = False
            for x, y, _ in same_time:
                if secret[x] or secret[y]:
                    # 如果任意一方已经知道，就把另一方也标记为 True
                    if not secret[x]:
                        secret[x] = True
                        changed = True
                    if not secret[y]:
                        secret[y] = True
                        changed = True

    # 4. 把所有 True 的下标收集返回
    return [i for i, know in enumerate(secret) if know]
```

#### 复杂度

- **时间复杂度**：`O(m²)` —— 同一时间段内可能需要多次遍历所有会议，最坏情况每次都遍历 `m` 场。
- **空间复杂度**：`O(n)` —— 只用了一个长度为 `n` 的布尔数组。

---

### 2. 最优解

#### 思路  

**瓶颈**  
暴力解的慢点在于同一时间段需要**多次全遍历**，导致二次方复杂度。我们需要一种方式，一遍遍历就能把同一时间段里所有可以相互传播的人员**一次性**连起来。

**关键观察**  
在同一时间 `t`，所有参加 `t` 时会议的人构成了若干**连通分量**（可以看成一个小图），只要分量里有任何一个已经知道秘密的人，整个分量的成员都会在时间 `t` 结束时同时得到秘密。  
> **类比**：把同一时间的会议看成一张社交网络图，图中每条边是一次会议。只要图里有“已经知道秘密的节点”，整个连通块都能立刻被点亮。

**如何快速找连通块**  
**并查集（Union‑Find）** 正好可以在 **近线性** 时间内把两个人合并到同一个集合，并且可以快速查询两个人是否在同一个集合里。  
步骤如下：

1. **按时间排序** 所有会议（`O(m log m)`）。
2. **逐时间段处理**  
   - 把本时间段所有会议的两端 `union`（合并到同一个集合）。此时同一个集合代表同一连通块。  
   - 再遍历本时间段的所有出现过的人员，检查它们的根节点 `find(x)` 是否等于根节点 `find(0)`（因为 0 或 `firstPerson` 已经是秘密的传播源）。如果等于，则说明这个集合里有人已经知道秘密，**把本集合的所有成员全部标记为已知**。  
   - 为了不让本时间段的合并影响后面的时间段，需要**在处理完本时间段后把参与者的并查集恢复到初始状态**（即只重置本段出现的节点的父指针）。这可以通过记录本段出现的节点列表，在结束时把它们的 `parent` 重新指向自己即可。

3. 最后把所有 `secret[i] == True` 的下标返回。

**为什么正确**  
- 按时间递增保证了信息只能向未来传播。  
- 在同一时间段，所有相互连通的人员在一次 `union` 操作后已经在同一个集合里，若集合里有秘密持有者，信息会瞬时传遍整个集合，符合“即时传播”。  
- 恢复并查集的做法确保每个时间段的连通性只在该段内部有效，不会错误地把不同时间段的会议混在一起。

**核心数据结构**  
- **并查集（Union‑Find）**：`parent[x]` 表示 `x` 的父节点，`find(x)` 带路径压缩返回根，`union(a,b)` 把两棵树合并（按秩或大小合并），几乎是 `O(α(n))`，其中 `α` 是极慢增长的逆阿克曼函数，几乎可以看作常数。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n          # 用于按秩合并

    def find(self, x: int) -> int:
        # 路径压缩：递归寻找根的同时把路径上的节点直接挂到根上
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        # 按秩合并，使树的高度尽量小
        if self.rank[ra] < self.rank[rb]:
            self.parent[ra] = rb
        elif self.rank[ra] > self.rank[rb]:
            self.parent[rb] = ra
        else:
            self.parent[rb] = ra
            self.rank[ra] += 1


def findAllPeople(n: int, meetings: List[List[int]], firstPerson: int) -> List[int]:
    # 1️⃣ 按时间排序
    meetings.sort(key=lambda x: x[2])

    uf = UnionFind(n)
    secret = [False] * n
    secret[0] = secret[firstPerson] = True   # 时间 0 的分享

    i = 0
    while i < len(meetings):
        cur_time = meetings[i][2]
        # 收集本时间段出现的所有人员，方便后面恢复并查集
        participants = set()
        # 2️⃣ 把本时间段的所有会议合并进并查集
        j = i
        while j < len(meetings) and meetings[j][2] == cur_time:
            x, y, _ = meetings[j]
            uf.union(x, y)
            participants.add(x)
            participants.add(y)
            j += 1

        # 3️⃣ 检查哪些连通块里已有秘密持有者
        # 先找出根为 secret 持有者的根集合
        secret_roots = {uf.find(p) for p in range(n) if secret[p]}
        # 把本时间段所有出现的人员，如果它们所在的根在 secret_roots 中，则全体标记为 True
        for p in participants:
            if uf.find(p) in secret_roots:
                secret[p] = True

        # 4️⃣ 恢复并查集：只把本时间段出现的节点的父指针恢复成自己，rank 仍保留（不影响后续）
        for p in participants:
            uf.parent[p] = p
            uf.rank[p] = 0   # 重置秩，防止后面出现不必要的高树

        i = j   # 继续处理下一个时间段

    return [idx for idx, know in enumerate(secret) if know]
```

#### 复杂度

- **时间复杂度**  
  - 排序：`O(m log m)`  
  - 每场会议最多一次 `union`、一次 `find`（在检查阶段），`union`/`find` 的均摊复杂度是 `O(α(n))`，可以视作常数。  
  - 因此总体是 `O(m log m + m·α(n))`，在实际数据下基本等价于 `O(m log m)`。  
  - 与暴力解的 `O(m²)` 相比，提升非常显著。

- **空间复杂度**  
  - 并查集需要 `O(n)` 的 `parent`、`rank` 数组。  
  - 额外的 `secret` 布尔数组、以及每次时间段的 `participants` 集合，最多存 `O(n)`（极端情况下所有人同时间参加），所以总体 **`O(n)`**。

---

## 心得

- **核心技巧**：把同一时间的会议抽象成一张无向图，用 **并查集（Union‑Find）** 找连通块，再根据是否包含已有秘密的节点一次性传播。  
- **该技巧适用的题型**  
  1. “在同一时间/同一批次内的关系可以一次性合并” 类的图论题（如 LeetCode 1971 *Find if Path Exists in Graph* 的离线版）。  
  2. “动态连通性 + 时间顺序” 的问题（如 1722 *Minimize Hamming Distance After Swap Operations*）。  
- **一句话总结解题钥匙**：**同一时间段的所有会议构成一个连通块，使用并查集一次合并即可完成即时传播**。

---

## 反思

- **拿到题目第一反应**：先把会议按时间排序，然后模拟每一场会议的传播，感觉实现起来很直接。  
- **最容易踩的坑**  
  - **同一时间多次传播**：忘记在同一时间段内部进行“闭环”传播，会导致像示例 3 那样的“收到后立刻再传”情况出错。  
  - **并查集的恢复**：如果不把本时间段的并查集合并后恢复，会把不该跨时间段连通的节点错误地连在一起，导致后面的时间段产生错误的传播。  
  - **忘记把 `firstPerson` 在时间 0 时标记为已知**，会少算 0 点的直接传播。  
- **下次遇到同类题，第一步该想到**：**把“同一时间/同一批次的关系”抽象为图的连通块**，考虑使用 **并查集** 或 **BFS/DFS** 一次性处理，而不是逐条循环。这样往往能把二次方的暴力降到近线性。