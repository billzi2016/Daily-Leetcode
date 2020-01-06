# #721. 合并账户 / Accounts Merge

> 难度：中等 · 标签：Array、Hash Table、String、Depth-First Search、Breadth-First Search、Union Find、Sorting · [LeetCode 链接](https://leetcode.com/problems/accounts-merge/)

---

## 题目（英文原版）

**Description**

Given a list of accounts where each element accounts[i] is a list of strings, where the first element accounts[i][0] is a name, and the rest of the elements are emails representing emails of the account.
Now, we would like to merge these accounts. Two accounts definitely belong to the same person if there is some common email to both accounts. Note that even if two accounts have the same name, they may belong to different people as people could have the same name. A person can have any number of accounts initially, but all of their accounts definitely have the same name.
After merging the accounts, return the accounts in the following format: the first element of each account is the name, and the rest of the elements are emails in sorted order. The accounts themselves can be returned in any order.

**Examples**

**Example 1:**

```
Input: accounts = [["John","johnsmith@mail.com","john_newyork@mail.com"],["John","johnsmith@mail.com","john00@mail.com"],["Mary","mary@mail.com"],["John","johnnybravo@mail.com"]]
Output: [["John","john00@mail.com","john_newyork@mail.com","johnsmith@mail.com"],["Mary","mary@mail.com"],["John","johnnybravo@mail.com"]]
Explanation:
The first and second John's are the same person as they have the common email "johnsmith@mail.com".
The third John and Mary are different people as none of their email addresses are used by other accounts.
We could return these lists in any order, for example the answer [['Mary', 'mary@mail.com'], ['John', 'johnnybravo@mail.com'], 
['John', 'john00@mail.com', 'john_newyork@mail.com', 'johnsmith@mail.com']] would still be accepted.
```

**Example 2:**

```
Input: accounts = [["Gabe","Gabe0@m.co","Gabe3@m.co","Gabe1@m.co"],["Kevin","Kevin3@m.co","Kevin5@m.co","Kevin0@m.co"],["Ethan","Ethan5@m.co","Ethan4@m.co","Ethan0@m.co"],["Hanzo","Hanzo3@m.co","Hanzo1@m.co","Hanzo0@m.co"],["Fern","Fern5@m.co","Fern1@m.co","Fern0@m.co"]]
Output: [["Ethan","Ethan0@m.co","Ethan4@m.co","Ethan5@m.co"],["Gabe","Gabe0@m.co","Gabe1@m.co","Gabe3@m.co"],["Hanzo","Hanzo0@m.co","Hanzo1@m.co","Hanzo3@m.co"],["Kevin","Kevin0@m.co","Kevin3@m.co","Kevin5@m.co"],["Fern","Fern0@m.co","Fern1@m.co","Fern5@m.co"]]
```

**Constraints**

- 1 <= accounts.length <= 1000
- 2 <= accounts[i].length <= 10
- 1 <= accounts[i][j].length <= 30
- accounts[i][0] consists of English letters.
- accounts[i][j] (for j > 0) is a valid email.

---

## 题目（中文翻译）

给定一个账户列表，其中 `accounts[i]` 是一个字符串数组，`accounts[i][0]` 为用户名，随后所有元素均为该账户的电子邮件（email）。  
现在，请合并这些账户。如果两个账户之间存在至少一个相同的电子邮件，则它们一定属于同一个人。请注意，即使两个账户的用户名相同，也可能属于不同的人，因为不同的人可能同名。一个人最初可能拥有任意数量的账户，但这些账户的用户名必定相同。

合并完毕后，以如下格式返回结果：每个账户的第一个元素为用户名，随后按字典序排序的所有电子邮件。各账户的顺序可以任意。

## 示例 1
```text
Input: accounts = [["John","johnsmith@mail.com","john_newyork@mail.com"],
                   ["John","johnsmith@mail.com","john00@mail.com"],
                   ["Mary","mary@mail.com"],
                   ["John","johnnybravo@mail.com"]]
Output: [["John","john00@mail.com","john_newyork@mail.com","johnsmith@mail.com"],
         ["Mary","mary@mail.com"],
         ["John","johnnybravo@mail.com"]]
Explanation:
- 第一个和第二个 “John” 的账户拥有相同的电子邮件 "johnsmith@mail.com"，因此它们属于同一人，需要合并。
- 第三个 “John” 与 “Mary” 的账户之间没有任何共同的电子邮件，说明它们是不同的人。
- 结果列表的顺序可以随意，例如 `[["Mary","mary@mail.com"],["John","johnnybravo@mail.com"],["John","john00@mail.com","john_newyork@mail.com","johnsmith@mail.com"]]` 也是合法的。
```

## 示例 2
```text
Input: accounts = [["Gabe","Gabe0@m.co","Gabe3@m.co","Gabe1@m.co"],
                   ["Kevin","Kevin3@m.co","Kevin5@m.co","Kevin0@m.co"],
                   ["Ethan","Ethan5@m.co","Ethan4@m.co","Ethan0@m.co"],
                   ["Hanzo","Hanzo3@m.co","Hanzo1@m.co","Hanzo0@m.co"],
                   ["Fern","Fern5@m.co","Fern1@m.co","Fern0@m.co"]]
Output: [["Ethan","Ethan0@m.co","Ethan4@m.co","Ethan5@m.co"],
         ["Gabe","Gabe0@m.co","Gabe1@m.co","Gabe3@m.co"],
         ["Hanzo","Hanzo0@m.co","Hanzo1@m.co","Hanzo3@m.co"],
         ["Kevin","Kevin0@m.co","Kevin3@m.co","Kevin5@m.co"],
         ["Fern","Fern0@m.co","Fern1@m.co","Fern5@m.co"]]
```

## 约束条件
- `1 <= accounts.length <= 1000`
- `2 <= accounts[i].length <= 10`
- `1 <= accounts[i][j].length <= 30`
- `accounts[i][0]` 只包含英文字母。
- 对于 `j > 0`，`accounts[i][j]` 为合法的电子邮件（email）。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每个账户两两比较，看看它们的邮箱列表里有没有交集。如果有交集，就把这两个账户“合并”。合并后再次和其它账户比较，直到没有可以合并的为止。

- **使用的数据结构**  
  - `list`（列表）保存每个账户。  
  - `set`（集合）用来快速判断两个账户的邮箱是否有公共元素，集合的“求交”就像在字典里查词一样快：把一个邮箱当成“词”，如果另一份字典里也出现了这词，就说明两份字典有关联。  
  - `dict`（字典）记录每个邮箱对应的账户下标，方便后面把同一个邮箱出现的所有账户连在一起。

- **为什么正确**  
  两个账户只要有任意一个相同的邮箱，就一定属于同一个人。暴力遍历所有账户对，逐个把满足条件的账户合并，最后得到的每一组就是同一个人的全部邮箱集合。

- **时间/空间复杂度**  
  - 设 `n = len(accounts)`，`m` 为单个账户最多的邮箱数（题目 ≤ 10），总邮箱数记为 `E`。  
  - 两两比较需要 `n*(n-1)/2` 次，每次比较要把两个集合取交集，最坏要遍历 `m` 个邮箱 → **时间复杂度约为 O(n²·m)**。  
    大白话：如果有 1000 个人，每个人都有 10 封邮件，暴力算法要检查 1000×999/2≈500k 次，每次检查最多 10 条邮件，算下来会很慢。  
  - 需要额外的 `set`、`dict` 来保存邮箱 → **空间复杂度 O(E)**，即所有邮箱的总数。

#### 代码（Python）

```python
from typing import List

def accountsMerge_bruteforce(accounts: List[List[str]]) -> List[List[str]]:
    # 把每个账户的邮箱转成集合，方便后面求交
    email_sets = [set(acc[1:]) for acc in accounts]
    merged = []                # 最终的合并结果
    visited = [False] * len(accounts)   # 标记哪些账户已经被合并进某个组

    for i in range(len(accounts)):
        if visited[i]:
            continue
        # 从第 i 个账户开始做一次 BFS，找出所有和它相连的账户
        stack = [i]
        visited[i] = True
        cur_emails = set(email_sets[i])   # 当前连通块的所有邮箱

        while stack:
            cur = stack.pop()
            for j in range(len(accounts)):
                if not visited[j] and cur_emails & email_sets[j]:
                    # 有交集 → 说明两账户属于同一个人
                    visited[j] = True
                    stack.append(j)
                    cur_emails.update(email_sets[j])   # 合并邮箱

        # 把连通块整理成题目要求的格式
        name = accounts[i][0]
        merged.append([name] + sorted(cur_emails))

    return merged
```

#### 复杂度

- **时间复杂度**：`O(n²·m)`  
  解释：我们对每对账户都检查一次交集，`n` 是账户数，`m` 是每个账户的邮箱数（≤10），所以最坏情况会出现二次方的比较。
- **空间复杂度**：`O(E)`  
  解释：我们存了每个账户的邮箱集合，总共占用所有邮箱的数量 `E` 的空间。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **“两两比较”**——每次都要遍历所有账户。  
其实我们只需要把 **“同一个人所有邮箱”** 看成一个连通块（connected component），只要把属于同一块的邮箱统一到同一个集合里，后面再把同集合的邮箱归并即可。

**关键点**：  
- 同一个账户里出现的所有邮箱，都一定属于同一个人。  
- 如果两个账户有共同的邮箱，那么它们对应的所有邮箱也属于同一个人。  

这正好对应 **并查集（Union‑Find / Disjoint Set Union, DSU）** 的使用场景：

1. **遍历所有账户**  
   - 取出第一个邮箱作为 “代表” ，把该账户里出现的其余邮箱都 **union（合并）** 到这个代表上。  
   - 同时用一个 `email_to_name` 字典记录每个邮箱对应的真实姓名（后面输出时需要）。

2. **遍历完所有账户后**，每个邮箱都找到了它的根节点（representative），根节点相同的邮箱就属于同一个人。  
   - 再用 `defaultdict(list)` 把根节点 → 邮箱列表 建立映射。

3. **输出**  
   - 对每个根节点的邮箱列表进行排序，然后在前面加上对应的姓名（从 `email_to_name` 中取）。

> **并查集的原理**（零基础解释）  
> - 想象每个邮箱是一张卡片，最初每张卡片都自成一堆（自己是自己的“家”）。  
> - 当我们发现两张卡片应该放在同一堆时，就把它们的“家”合并，让其中一堆的“家”指向另一堆的“家”。  
> - 查找时，我们沿着指向一直往上找，直到找到最顶层的“家”。为了加速，这个查找过程会把沿途的卡片直接指向最顶层，这叫 **路径压缩**。  
> - 合并时，我们会把较小的堆挂到较大的堆下面，这叫 **按秩合并**（或按大小合并），可以让树的高度保持很小。

**为什么更快**  
- 每条邮箱只会被 `union` 一次（或几次），而 `find` 的时间几乎是 **常数**（α(N)，α 为 Ackermann 函数的逆，几乎不增长）。  
- 整体只遍历一次所有账户 → **线性** 时间。

#### 代码（Python）

```python
from typing import List
from collections import defaultdict

class UnionFind:
    """并查集实现，带路径压缩和按秩合并"""
    def __init__(self):
        self.parent = {}   # key: 元素，value: 父节点
        self.rank = {}     # 用来做按秩合并的辅助信息

    def find(self, x):
        """返回 x 的根节点，同时进行路径压缩"""
        if self.parent[x] != x:
            # 递归查找根节点，并把路径上的所有节点直接挂到根节点下
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        """把 x、y 两个元素所在的集合合并"""
        root_x, root_y = self.find(x), self.find(y)
        if root_x == root_y:      # 已经在同一个集合，无需合并
            return
        # 按秩合并：rank 小的挂到 rank 大的下面
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

def accountsMerge(accounts: List[List[str]]) -> List[List[str]]:
    uf = UnionFind()
    email_to_name = {}          # 邮箱 → 姓名（后面输出需要）

    # ---------- 第一步：建立并查集 ----------
    for acc in accounts:
        name = acc[0]
        first_email = acc[1]    # 选第一个邮箱做“代表”
        for email in acc[1:]:
            # 初始化并查集节点（第一次出现时）
            if email not in uf.parent:
                uf.parent[email] = email
                uf.rank[email] = 0
            # 记录邮箱对应的姓名（所有同人邮箱的姓名相同）
            email_to_name[email] = name
            # 把当前邮箱和代表邮箱合并
            uf.union(first_email, email)

    # ---------- 第二步：根据根节点把邮箱归类 ----------
    roots = defaultdict(list)   # 根节点 → 同根的所有邮箱
    for email in uf.parent:
        root = uf.find(email)    # 找到根节点
        roots[root].append(email)

    # ---------- 第三步：整理输出 ----------
    merged = []
    for root, emails in roots.items():
        emails.sort()                     # 按字典序排序
        merged.append([email_to_name[root]] + emails)

    return merged
```

#### 复杂度

- **时间复杂度**：`O(E·α(E))`，约等于 `O(E)`  
  - `E` 为所有邮箱的总数（≤ 1000 × 10 = 10⁴）。  
  - `α(E)` 是 Ackermann 逆函数的值，几乎是常数（小于 5），所以整体近似线性。  
  - 与暴力解的二次方相比，提升非常明显。

- **空间复杂度**：`O(E)`  
  - 需要存储每个邮箱的父指针、秩、以及 `email_to_name` 映射，都是和邮箱数量成正比的。

---

## 心得

- **核心技巧**：把“同一个人所有邮箱”抽象成 **连通块**，使用 **并查集（Union‑Find）** 或 **图的遍历**（DFS/BFS）快速找出这些块。  
- **适用的题型**  
  1. **Friend Circles / Number of Provinces**（判断社交网络或省份的连通块）  
  2. **Redundant Connection**（在无向图中找出多余的边）  
  3. **Satisfiability of Equality Equations**（等式不等式的合并判断）  
- **一句话总结解题钥匙**：把“有共同邮箱的账户”视为 **等价关系**，用并查集把等价的邮箱归并到同一个根节点。

---

## 反思

- **拿到题目第一反应**：先想把所有账户两两比较，找出公共邮箱后合并——这就是暴力思路。  
- **最容易踩的坑**  
  - **姓名的处理**：不同账户即使姓名相同，也不一定是同一个人，必须完全依赖邮箱来决定合并。  
  - **重复邮箱**：同一个邮箱可能出现在多行，需要确保在并查集中只创建一次节点。  
  - **输出顺序**：每组邮箱要先排序，再在最前面加上对应的姓名；否则会不符合题目要求。  
- **下次遇到同类题，第一步该想到**：**是否可以把元素之间的“相连关系”抽象为图的边**，如果是，则考虑 **并查集**（快速合并）或 **DFS/BFS**（遍历连通块）来解决。