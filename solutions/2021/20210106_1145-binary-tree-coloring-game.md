# #1145. 二叉树染色游戏 / Binary Tree Coloring Game

> 难度：中等 · 标签：Tree、Depth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/binary-tree-coloring-game/)

---

## 题目（英文原版）

**Description**

Two players play a turn based game on a binary tree. We are given the root of this binary tree, and the number of nodes n in the tree. n is odd, and each node has a distinct value from 1 to n.
Initially, the first player names a value x with 1 <= x <= n, and the second player names a value y with 1 <= y <= n and y != x. The first player colors the node with value x red, and the second player colors the node with value y blue.
Then, the players take turns starting with the first player. In each turn, that player chooses a node of their color (red if player 1, blue if player 2) and colors an uncolored neighbor of the chosen node (either the left child, right child, or parent of the chosen node.)
If (and only if) a player cannot choose such a node in this way, they must pass their turn. If both players pass their turn, the game ends, and the winner is the player that colored more nodes.
You are the second player. If it is possible to choose such a y to ensure you win the game, return true. If it is not possible, return false.

**Examples**

**Example 1:**

```
Input: root = [1,2,3,4,5,6,7,8,9,10,11], n = 11, x = 3
Output: true
Explanation: The second player can choose the node with value 2.
```

**Example 2:**

```
Input: root = [1,2,3], n = 3, x = 1
Output: false
```

**Constraints**

- The number of nodes in the tree is n.
- 1 <= x <= n <= 100
- n is odd.
- 1 <= Node.val <= n
- All the values of the tree are unique.

---

## 题目（中文翻译）

两位玩家在一棵二叉树 (binary tree) 上进行回合制游戏。已知这棵二叉树的根节点以及树中节点的总数 *n*，且 *n* 为奇数，树中每个节点的值均为 1 到 *n* 的唯一整数。

游戏开始时，玩家 1 先选取一个值 *x*（1 ≤ *x* ≤ *n*），玩家 2 再选取一个值 *y*（1 ≤ *y* ≤ *n* 且 *y* ≠ *x*）。玩家 1 将值为 *x* 的节点染成红色，玩家 2 将值为 *y* 的节点染成蓝色。

随后玩家轮流行动，先手为玩家 1。每一回合，当前玩家必须从已经染成自己颜色的节点（玩家 1 为红色，玩家 2 为蓝色）中选择一个，并将该节点的**未染色的相邻节点**（左子节点、右子节点或父节点）染成自己的颜色。如果玩家无法完成此操作，则必须**跳过**本回合。**当两位玩家连续都跳过**时，游戏结束，染色节点数更多的玩家获胜。

你是玩家 2。若存在一种选取 *y* 的方式可以确保你必胜，则返回 `true`；否则返回 `false`。

**示例 1**  
**示例 2**  
**约束条件**  

### 示例

#### 示例 1
**输入**  
`root = [1,2,3,4,5,6,7,8,9,10,11], n = 11, x = 3`  
**输出**  
`true`  
**解释**  
玩家 2 可以选择值为 2 的节点。

#### 示例 2
**输入**  
`root = [1,2,3], n = 3, x = 1`  
**输出**  
`false`

### 约束条件
- 树中节点数为 *n*。  
- 1 ≤ *x* ≤ *n* ≤ 100。  
- *n* 为奇数。  
- 1 ≤ `Node.val` ≤ *n*。  
- 树中所有节点的值均唯一。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是「把所有可能的第二个选择 `y` 都枚举一遍，然后把游戏完整地模拟一遍，看能不能赢」。  
具体步骤如下：

1. **遍历所有候选节点** `y (y ≠ x)`。这一步相当于把树上每个节点都当成「蓝色起点」去尝试一次。  
2. **模拟游戏过程**  
   - 记录每个节点的颜色（未染色 / 红 / 蓝）。  
   - 按照题目规则轮流让两位玩家「从自己已经染色的节点出发，向相邻的未染色节点扩散」；如果当前玩家没有可扩散的节点，则**pass**。  
   - 当两位玩家连续 **pass** 两次（即都没有可走的地方）时，游戏结束，比较两位玩家染色的节点数。  
3. 如果在某一次枚举的 `y` 中，蓝色节点数严格大于红色节点数，则返回 `True`；否则全部尝试完返回 `False`。

> **类比**：把树想象成一张城市地图，玩家的颜色就是「领地」的颜色。每回合玩家只能从自己已经拥有的城市出发，扩张到相邻的未被占领的城市。暴力解就是让每个可能的起始城市都尝试一次，看看能否占领更多的城市。

**为什么暴力解一定能得到答案**  
因为我们把「所有合法的第二次选择」都穷举了，并且对每一种选择都完整地模拟了游戏的所有可能走法（题目已经规定每一步的走法唯一：只能向相邻未染色的节点扩张），所以只要有一种 `y` 能赢，枚举过程必定会发现。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def btreeGameWinningMove_bruteforce(root: TreeNode, n: int, x: int) -> bool:
    """暴力枚举所有 y 并完整模拟游戏，返回是否存在必胜的 y"""

    # ---------- 辅助函数 ----------
    # 把树的结构转成邻接表（无向图），方便后面像“城市地图”那样遍历
    from collections import defaultdict, deque

    adj = defaultdict(list)          # key: 节点值, value: 相邻节点值列表

    def build_adj(node: TreeNode, parent: TreeNode = None):
        if not node:
            return
        if parent:
            adj[node.val].append(parent.val)
            adj[parent.val].append(node.val)
        if node.left:
            build_adj(node.left, node)
        if node.right:
            build_adj(node.right, node)

    build_adj(root)

    # ---------- 主循环：枚举 y ----------
    for y in range(1, n + 1):
        if y == x:               # 不能和 x 重复
            continue

        # 颜色状态：0=未染, 1=红 (玩家1), 2=蓝 (玩家2)
        color = {i: 0 for i in range(1, n + 1)}
        color[x] = 1
        color[y] = 2

        # 记录每位玩家当前可以扩张的节点集合（从这些节点出发可以向相邻未染色的节点扩散）
        red_frontier = {x}
        blue_frontier = {y}

        # 两位玩家交替行动，直到双方都没有可行动的节点
        while red_frontier or blue_frontier:
            # -------- 玩家 1（红） ----------
            new_red = set()
            for node in red_frontier:
                for nb in adj[node]:
                    if color[nb] == 0:        # 仍是未染色
                        color[nb] = 1
                        new_red.add(nb)       # 这颗新染的红色节点以后还能继续扩散
            red_frontier = new_red            # 更新红方的 frontier

            # -------- 玩家 2（蓝） ----------
            new_blue = set()
            for node in blue_frontier:
                for nb in adj[node]:
                    if color[nb] == 0:
                        color[nb] = 2
                        new_blue.add(nb)
            blue_frontier = new_blue

        # --------- 统计染色数量 ----------
        red_cnt = sum(1 for v in color.values() if v == 1)
        blue_cnt = sum(1 for v in color.values() if v == 2)

        if blue_cnt > red_cnt:   # 找到必胜的 y
            return True

    return False
```

> **关键行中文注释** 已在代码中标明，帮助初学者快速定位每一步的作用。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 外层循环遍历所有可能的 `y`（最多 `n-1` 次）。  
  - 每一次模拟游戏时，最坏情况会遍历整棵树一次（`O(n)`），因为每个节点只会被染色一次。  
  - 所以总体是 `O((n-1) * n) ≈ O(n²)`。  
  - **大白话**：如果树有 1000 个节点，暴力解大约要做 1000 × 1000 = 100 万次基本操作，明显会慢。

- **空间复杂度**：`O(n)`  
  - 需要存储邻接表、颜色数组以及两位玩家的 frontier 集合，均与节点数成线性关系。  

---

### 2. 最优解

#### 思路  

从暴力解出发，我们可以发现 **瓶颈** 在于「枚举所有 `y` 并完整模拟游戏」这一步。实际上，游戏的结果只和 **相对位置** 有关，而不是每一步的细节。  
观察题目：

- 第一次红色玩家已经把节点 `x` 染红。  
- 第二位玩家只要在 `x` 的 **相邻** 节点（左子树根、右子树根、或 `x` 的父节点所在的那块）下手，就可以把整块相邻的子树「封锁」住，使得红色玩家无法进入该子树。  

> **类比**：把 `x` 想成一棵大树的「城堡」，它有三条通道：左侧、右侧、以及通往上层的通道。第二位玩家只要站在其中一条通道的入口（即选 `y` 为该通道的第一个节点），就可以把整条通道占为己有，阻止红色玩家进入。

因此，**只需要比较这三块区域的大小**：

1. `left_sz`  = `x` 左子树的节点数  
2. `right_sz` = `x` 右子树的节点数  
3. `parent_sz` = 整棵树的节点总数 `n` 减去 `x` 所在的子树（`left_sz + right_sz + 1`），也就是「除 `x` 与它的左右子树之外」的那块区域  

如果其中 **任意一块** 的节点数 **大于** 总节点数的一半（即 `> n/2`），第二位玩家只要把 `y` 选在这块区域的入口，就能控制超过半数的节点，从而必胜。  

> **为什么 > n/2 就能必胜**  
> - 游戏结束时，两位玩家各自占据的节点数之和恰好是 `n`（所有节点都被染色）。  
> - 若蓝色玩家一开始就掌控了超过半数的节点，那么红色玩家最多只能得到 `n - blue_cnt < blue_cnt`，自然蓝方赢。  

**核心算法**：一次深度优先搜索（DFS）计算出 `x` 的左、右子树大小即可，时间 `O(n)`，空间 `O(h)`（递归栈深度），`h` 为树高。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def btreeGameWinningMove(root: TreeNode, n: int, x: int) -> bool:
    """
    O(n) 版本：只计算 x 左、右子树的大小，再判断是否存在 > n/2 的区域。
    """

    left_sz = right_sz = 0          # 用来保存 x 左、右子树的节点数量

    # --------- DFS 返回子树节点总数 ----------
    def dfs(node: TreeNode) -> int:
        """返回以 node 为根的子树节点数，同时在遍历到值为 x 的节点时记录左右子树大小"""
        if not node:
            return 0
        l = dfs(node.left)          # 左子树节点数
        r = dfs(node.right)         # 右子树节点数
        if node.val == x:           # 找到 x，保存左右子树大小
            nonlocal left_sz, right_sz
            left_sz, right_sz = l, r
        return l + r + 1            # 当前子树总节点数

    dfs(root)                       # 触发一次完整遍历

    # 父侧（不属于 x 本身及其左右子树的那块）的节点数
    parent_sz = n - (left_sz + right_sz + 1)

    # 只要有一块区域 > n/2，蓝方就可以选其入口赢得比赛
    half = n // 2
    return max(left_sz, right_sz, parent_sz) > half
```

> **关键行中文注释** 已在代码中标明，帮助你一步步跟随思路。

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 只进行一次深度优先遍历，访问每个节点一次。  
  - **对比**：相较于暴力解的 `O(n²)`，这相当于把「遍历 1000 次」压缩成「遍历 1 次」，速度提升显著。

- **空间复杂度**：`O(h)`（递归栈），最坏情况下 `h = n`（链状树），平均情况下 `h ≈ log n`（平衡树）。  
  - 只用了常数级别的额外变量 `left_sz、right_sz、parent_sz`。

---

## 心得

- **核心技巧**：把二叉树看成「若干相邻的子区域」并利用**子树大小比较**决定胜负。  
- **适用的题型**  
  1. *Binary Tree Coloring Game*（本题）  
  2. *Count Largest Subtree*（比较子树大小来决定是否满足条件）  
  3. *Maximum Area of Island*（在网格中划分相邻区域，比较面积大小）  
- **一句话总结**：只要把 `x` 的左右子树和「其余部分」的节点数算出来，看看有没有一块超过半数，第二位玩家就能直接选这块的入口赢得游戏。

---

## 反思

- **第一反应**：先想到「枚举所有 y」然后「逐步模拟」——这是一种直观的「暴力」思路，适合快速验证想法。  
- **最容易踩的坑**  
  - 忘记把「父侧」也算进来，只比较了左右子树。  
  - 在递归中错误地覆盖了 `left_sz`、`right_sz`（需要使用 `nonlocal`）。  
  - 没考虑 `n` 为奇数的限制——其实不影响判断，只是保证不会出现平局。  
- **下次遇到类似题**：第一步先**把问题抽象成「把树划分为若干相邻块」并**统计每块的规模**，往往能直接得到 O(n) 的解法，而不必去模拟每一步的过程。