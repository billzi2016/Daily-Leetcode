# #2049. 计数最高分的节点 / Count Nodes With the Highest Score

> 难度：中等 · 标签：Array、Tree、Depth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/count-nodes-with-the-highest-score/)

---

## 题目（英文原版）

**Description**

There is a binary tree rooted at 0 consisting of n nodes. The nodes are labeled from 0 to n - 1. You are given a 0-indexed integer array parents representing the tree, where parents[i] is the parent of node i. Since node 0 is the root, parents[0] == -1.
Each node has a score. To find the score of a node, consider if the node and the edges connected to it were removed. The tree would become one or more non-empty subtrees. The size of a subtree is the number of the nodes in it. The score of the node is the product of the sizes of all those subtrees.
Return the number of nodes that have the highest score.

**Examples**

**Example 1:**

```
Input: parents = [-1,2,0,2,0]
Output: 3
Explanation:
- The score of node 0 is: 3 * 1 = 3
- The score of node 1 is: 4 = 4
- The score of node 2 is: 1 * 1 * 2 = 2
- The score of node 3 is: 4 = 4
- The score of node 4 is: 4 = 4
The highest score is 4, and three nodes (node 1, node 3, and node 4) have the highest score.
```

**Example 2:**

```
Input: parents = [-1,2,0]
Output: 2
Explanation:
- The score of node 0 is: 2 = 2
- The score of node 1 is: 2 = 2
- The score of node 2 is: 1 * 1 = 1
The highest score is 2, and two nodes (node 0 and node 1) have the highest score.
```

**Constraints**

- n == parents.length
- 2 <= n <= 105
- parents[0] == -1
- 0 <= parents[i] <= n - 1 for i != 0
- parents represents a valid binary tree.

---

## 题目（中文翻译）

给定一棵以节点 `0` 为根的二叉树（binary tree），共有 `n` 个节点，节点编号为 `0` 到 `n - 1`。数组 `parents`（0 索引）描述了这棵树，其中 `parents[i]` 表示节点 `i` 的父节点。由于 `0` 是根节点，`parents[0] == -1`。

每个节点都有一个分数（score）。计算节点的分数时，假设将该节点及其相连的所有边全部删除，树会被拆分成一个或多个非空子树（subtree）。子树的大小（size）等于其中节点的数量。该节点的分数等于所有这些子树大小的乘积。

返回分数最高的节点数量。

**示例 1**

``` 
Input: parents = [-1,2,0,2,0]
Output: 3
Explanation:
- 节点 0 的分数是：3 * 1 = 3
- 节点 1 的分数是：4 = 4
- 节点 2 的分数是：1 * 1 * 2 = 2
- 节点 3 的分数是：4 = 4
- 节点 4 的分数是：4 = 4
最高分是 4，拥有最高分的节点有三个（节点 1、节点 3、节点 4）。
```

**示例 2**

``` 
Input: parents = [-1,2,0]
Output: 2
Explanation:
- 节点 0 的分数是：2 = 2
- 节点 1 的分数是：2 = 2
- 节点 2 的分数是：1 * 1 = 1
最高分是 2，拥有最高分的节点有两个（节点 0、节点 1）。
```

**约束条件**

- `n == parents.length`
- `2 <= n <= 10^5`
- `parents[0] == -1`
- 对于 `i != 0`，`0 <= parents[i] <= n - 1`
- `parents` 描述了一棵有效的二叉树。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

我们先把题目拆成两步来想：

1. **把树拆开**  
   对每个节点 `i`，把它和连着它的边“剪掉”。剪完后会得到若干棵**子树**（不为空）。  
   例如，根节点被剪掉后，剩下的每一棵子树就是它的左/右子树；而非根节点被剪掉后，还会多出“上面那块”——也就是除去它所在子树之外的其余所有节点。

2. **算分数**  
   每棵子树的**大小** = 这棵子树里有多少节点。把所有子树的大小相乘，就是该节点的**分数**。

最直接的做法是：**对每个节点，重新遍历整棵树，统计它的子树大小**，再算分数。  
这相当于我们把每个节点都当成一次“根”，从头到尾跑一次 DFS（深度优先搜索）来数节点数。

> **类比**：把 `hash table` 想成一本字典，`key` 是单词，`value` 是页码。这里我们把每个节点当成“查询关键字”，每次都要重新翻遍整本“字典”去找它对应的子树大小。

**为什么能得到正确答案**  
- 对每个节点我们都完整地统计了它被剪掉后形成的所有子树的大小。  
- 分数公式是“子树大小的乘积”，只要统计正确，乘积自然正确。  
- 最后把所有分数取最大值并计数，自然得到答案。

**时间/空间复杂度**  
- 对每个 `i`（共 `n` 个），我们都要遍历整棵树一次，遍历一次的时间是 `O(n)`。所以总时间是 `O(n·n) = O(n²)`。  
  - **大白话**：如果树有 10,000 个节点，暴力解相当于要做 10,000 次“全员点名”，总共 100,000,000 次操作，明显太慢。  
- 额外的空间只需要存储递归栈（深度最多 `n`），以及保存每次遍历的计数变量，整体是 `O(n)`（递归栈）或 `O(1)`（不计栈）。这里我们记为 `O(n)`。

#### 代码（Python）

```python
from typing import List

def countHighestScoreNodes_bruteforce(parents: List[int]) -> int:
    n = len(parents)

    # 把父子关系变成邻接表，方便遍历
    children = [[] for _ in range(n)]
    for node, p in enumerate(parents):
        if p != -1:               # 根节点的父亲是 -1，不加入
            children[p].append(node)

    # -------------------------------------------------
    # 辅助函数：从 start 开始 DFS，返回遍历到的节点数
    # -------------------------------------------------
    def subtree_size(start: int) -> int:
        stack = [start]
        cnt = 0
        while stack:
            cur = stack.pop()
            cnt += 1
            for ch in children[cur]:
                stack.append(ch)
        return cnt

    max_score = 0          # 当前最高分
    cnt_max   = 0          # 最高分出现的次数

    # 对每个节点都重新统计子树大小
    for i in range(n):
        # 1) 左右子树的大小（如果有子节点的话）
        left_size = subtree_size(children[i][0]) if len(children[i]) > 0 else 0
        right_size = subtree_size(children[i][1]) if len(children[i]) > 1 else 0

        # 2) “上面那块” 的大小 = 整棵树减去 i 本身和它的子树
        rest = n - (1 + left_size + right_size)

        # 3) 计算分数：把所有非零的部分相乘
        score = 1
        for part in (left_size, right_size, rest):
            if part:            # 只乘非空子树
                score *= part

        # 4) 更新最大分数及计数
        if score > max_score:
            max_score = score
            cnt_max   = 1
        elif score == max_score:
            cnt_max += 1

    return cnt_max
```

> **关键行解释**  
> - `children`：把每个节点的孩子保存下来，类似“字典”里的 `key → value`（节点 → 子节点列表）。  
> - `subtree_size`：从某个节点出发，用栈模拟递归，统计它所在子树的节点数。  
> - `rest`：把整棵树的节点数 `n` 减掉当前节点本身以及它的左右子树，得到“上面那块”的大小。  
> - `if part:`：只有子树非空时才乘进去，防止乘以 0 把分数直接变成 0。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 每个节点都要重新遍历整棵树一次，等价于 `n` 次 `O(n)` 的遍历。  
  - 对于 `n = 10⁵` 的极限数据，这几乎不可能在 1 秒内跑完。

- **空间复杂度**：`O(n)`  
  - 主要是 `children` 列表占用 `O(n)` 空间，递归栈（这里用显式栈）最坏也会有 `n` 层。

---

### 2. 最优解

#### 思路  

从暴力解我们已经知道：

- **关键**是每个节点的 **子树大小**（左子树、右子树）以及 “其余部分” 的大小。  
- 暴力解的瓶颈在于 **重复遍历**：对每个节点都重新算子树大小。

**优化的核心**：**一次遍历算出所有节点的子树大小**，随后再用这些已经算好的值直接求分数。

实现步骤：

1. **构建邻接表**（同上）来存储每个节点的孩子列表。  
2. **一次 DFS**（从根节点 `0` 开始），递归返回每个节点的 **子树节点数**。  
   - 设 `size[v]` 为以 `v` 为根的子树大小。递归公式：  
     `size[v] = 1 + sum(size[child] for child in children[v])`  
   - 这一步相当于“一次性把所有子树的大小都记下来”，以后不需要再遍历。  
3. **遍历所有节点**，利用 `size` 数组直接计算每个节点的分数：  
   - 左子树大小 `left = size[children[i][0]]`（如果有左子树），右子树同理。  
   - “上面那块” 大小 `rest = n - (1 + left + right)`。  
   - 分数 `score = left * right * rest`，其中任何为 0 的部分直接不参与乘法（因为乘 0 会把分数变 0）。  
4. **维护最大分数** `max_score` 与出现次数 `cnt_max`，遍历结束即得答案。

> **类比**：把树的子树大小看成每个人的**体重**。一次体检（DFS）把所有人的体重都记录下来，之后想算某个人的“影响力”只需要查表，而不必再让全体重新称重。

**为什么一次遍历就够**  
- 树的结构是 **无环的**，一次递归从根往下走，子树的大小只依赖于它的孩子的大小，而孩子的大小又在更深层递归里已经算好。  
- 这种“自底向上”的计算方式正好符合树的层次结构，不会产生重复工作。

#### 代码（Python）

```python
from typing import List

def countHighestScoreNodes(parents: List[int]) -> int:
    n = len(parents)

    # 1. 建立邻接表：children[i] 保存 i 的所有子节点
    children = [[] for _ in range(n)]
    for node, p in enumerate(parents):
        if p != -1:                 # 根节点的父亲是 -1
            children[p].append(node)

    # 2. 第一次 DFS：求每个节点的子树大小，存入 size[]
    size = [0] * n                  # size[v] = 子树节点数

    def dfs(v: int) -> int:
        """返回以 v 为根的子树大小，同时填充 size[v]"""
        total = 1                   # 计入自己
        for ch in children[v]:     # 遍历所有孩子
            total += dfs(ch)        # 把孩子的子树大小加进来
        size[v] = total
        return total

    dfs(0)                          # 从根节点开始

    # 3. 第二遍遍历：用已经算好的 size[] 直接求每个节点的分数
    max_score = 0
    cnt_max   = 0

    for i in range(n):
        left = right = 0

        if len(children[i]) >= 1:               # 左子树（如果存在）
            left = size[children[i][0]]
        if len(children[i]) == 2:               # 右子树（如果存在）
            right = size[children[i][1]]

        # “其余部分” 的大小 = 总节点数 - (自己 + 左子树 + 右子树)
        rest = n - (1 + left + right)

        # 计算分数：把非零的部分相乘
        score = 1
        for part in (left, right, rest):
            if part:
                score *= part

        # 更新最大分数和计数
        if score > max_score:
            max_score = score
            cnt_max   = 1
        elif score == max_score:
            cnt_max += 1

    return cnt_max
```

> **关键行解释**  
> - `children[p].append(node)`：把父节点 `p` 当成“字典的 key”，`node` 是对应的“页码”。  
> - `dfs(v)`：递归返回子树大小，同时把结果写进全局数组 `size`，实现“一次遍历全部记”。  
> - `rest = n - (1 + left + right)`：总节点数减去当前节点以及它的两个子树，就是“上面那块”。  
> - `if part:`：只乘非零的子树，避免把分数直接变成 0。

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 第一次 DFS 访问每条边一次，第二次遍历每个节点一次，整体线性。  
  - 对于 `n = 10⁵`，只需要约 `2·10⁵` 次操作，轻松跑完。

- **空间复杂度**：`O(n)`  
  - `children`、`size` 两个数组各占 `O(n)`。  
  - 递归栈深度最坏为树的高度，二叉树最坏高度为 `n`（链状），但在 Python 里可以把递归改成显式栈或调高递归深度限制，这里仍记为 `O(n)`。

---

## 心得

- **核心技巧**：一次 DFS 计算**子树大小**，随后用**乘积公式**直接求每个节点的分数。  
- **适用的题型**  
  1. 需要“子树信息”并且对所有节点都要统计的题目（如 “子树中最大值/最小值”）。  
  2. 需要**删除节点后**的连通块大小或计数的题目（如 “删除节点后的森林大小”）。  
- **解题钥匙**：**“先把所有子树信息预处理好，再遍历求答案”。** 只要把“子树大小”一次算清楚，后面的每一步都是 O(1) 的查表操作。

---

## 反思

- **第一反应**：看到“把节点和相连的边都剪掉后得到若干子树”，立刻想到**DFS**遍历子树大小。  
- **最容易踩的坑**  
  1. **根节点的“其余部分”** 为 `0`（因为根没有上面的那块），乘积时一定要把 `0` 排除，否则分数会错误变成 `0`。  
  2. **二叉树可能只有左子树或右子树**，访问 `children[i][1]` 前必须先检查长度。  
  3. **整数乘积可能很大**，但 Python 的整数是大数，语言本身不会溢出，仍需注意时间上乘法是 O(1)。  
- **下次类似题的第一步**：**先做一次 DFS，记录每个节点的子树规模（或其他需要的属性）**，再在此基础上完成后续计算。这样可以避免重复遍历，保证线性时间。