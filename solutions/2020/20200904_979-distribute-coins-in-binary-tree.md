# #979. 二叉树中的硬币分配 / Distribute Coins in Binary Tree

> 难度：中等 · 标签：Tree、Depth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/distribute-coins-in-binary-tree/)

---

## 题目（英文原版）

**Description**

You are given the root of a binary tree with n nodes where each node in the tree has node.val coins. There are n coins in total throughout the whole tree.
In one move, we may choose two adjacent nodes and move one coin from one node to another. A move may be from parent to child, or from child to parent.
Return the minimum number of moves required to make every node have exactly one coin.

**Examples**

**Example 1:**

```
Input: root = [3,0,0]
Output: 2
Explanation: From the root of the tree, we move one coin to its left child, and one coin to its right child.
```

**Example 2:**

```
Input: root = [0,3,0]
Output: 3
Explanation: From the left child of the root, we move two coins to the root [taking two moves]. Then, we move one coin from the root of the tree to the right child.
```

**Constraints**

- The number of nodes in the tree is n.
- 1 <= n <= 100
- 0 <= Node.val <= n
- The sum of all Node.val is n.

---

## 题目（中文翻译）

给定一棵包含 `n` 个节点的二叉树 (binary tree) 的根节点 `root`，树中的每个节点拥有 `node.val` 枚硬币。整个树恰好共有 `n` 枚硬币。

在一次移动中，你可以选择两个相邻的节点，将一枚硬币从其中一个节点移到另一个节点。移动既可以是从父节点到子节点，也可以是从子节点到父节点。

**返回** 为使每个节点恰好拥有一枚硬币所需的最少移动次数。

## 示例

### 示例 1
**输入**：`root = [3,0,0]`  
**输出**：`2`  
**解释**：从根节点向左子节点移动一枚硬币，再向右子节点移动一枚硬币。

### 示例 2
**输入**：`root = [0,3,0]`  
**输出**：`3`  
**解释**：先从根的左子节点向根节点移动两枚硬币（共两次移动），随后再从根节点向右子节点移动一枚硬币。

## 约束条件

- 树中节点的数量为 `n`。  
- `1 <= n <= 100`  
- `0 <= Node.val <= n`  
- 所有 `Node.val` 的和恰好等于 `n`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每一次搬运硬币都模拟出来**，直到所有节点恰好各有一枚硬币为止。  
我们可以把树看成一张“邻接表”，每个节点都记住它的左右孩子（如果有的话）。  

1. 先遍历整棵树，找到所有**多余硬币**的节点（`node.val > 1`）和**缺少硬币**的节点（`node.val == 0`）。  
2. 对每一个缺少硬币的节点，沿着树的边向上（或向下）寻找最近的、还有多余硬币的节点，然后把一枚硬币沿着这条路径搬过去。  
3. 把搬运的每一步都记为一次移动，直到所有缺少的节点都被填满。

> **类比**：把树想象成一栋楼，每个房间里有若干硬币。我们要把多余的硬币搬到空房间，搬运过程就像搬家一样——先找最近的有多余的房间，然后把硬币一步一步搬过去。

这种方法之所以 **正确**，是因为我们每一次都把一个缺少硬币的节点补齐，而总硬币数恰好等于节点数，最终必然能把所有多余硬币全部分配完。

**为什么会慢**  
- 每次寻找最近的多余节点需要遍历树的路径，最坏情况是从根到叶子走完整棵树。  
- 如果缺少硬币的节点有 `k` 个，且每次都要遍历 `O(n)` 的路径，整体时间复杂度大约是 `O(k·n)`，而 `k` 最多接近 `n`，于是时间复杂度退化为 `O(n²)`。  

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x          # 当前节点的硬币数量
        self.left = None
        self.right = None

def collect_nodes(root):
    """把所有节点放进列表，方便后面遍历"""
    nodes = []
    def dfs(node):
        if not node:
            return
        nodes.append(node)
        dfs(node.left)
        dfs(node.right)
    dfs(root)
    return nodes

def bfs_path(start, target):
    """在树上做 BFS，返回从 start 到 target 的路径长度（边数）"""
    from collections import deque
    q = deque([(start, 0)])          # (当前节点, 已走的步数)
    visited = set([start])
    while q:
        node, dist = q.popleft()
        if node is target:
            return dist
        for nxt in (node.left, node.right):
            if nxt and nxt not in visited:
                visited.add(nxt)
                q.append((nxt, dist + 1))
        # 这里我们也可以向父节点走，但为了简化演示，假设我们已经保存了父指针
    return float('inf')   # 不可能的情况

def distribute_coins_bruteforce(root: TreeNode) -> int:
    """
    暴力模拟搬运过程，返回最少搬运次数
    """
    nodes = collect_nodes(root)               # 所有节点的列表
    moves = 0

    # 记录每个节点的父节点，方便向上走
    parent = {root: None}
    def set_parent(node):
        if not node:
            return
        if node.left:
            parent[node.left] = node
        if node.right:
            parent[node.right] = node
        set_parent(node.left)
        set_parent(node.right)
    set_parent(root)

    # 辅助函数：从一个节点向上走到根
    def path_to_root(node):
        path = []
        while node:
            path.append(node)
            node = parent[node]
        return path   # 从当前节点到根的路径（包括根）

    while True:
        # 找出所有缺少硬币的节点
        deficit_nodes = [node for node in nodes if node.val == 0]
        if not deficit_nodes:          # 全部补齐，结束
            break

        # 任选一个缺少硬币的节点，找最近的有多余硬币的节点
        target = deficit_nodes[0]
        # 广度优先搜索最近的 surplus 节点
        from collections import deque
        q = deque([(target, 0)])       # (当前节点, 距离)
        visited = set([target])
        found = None
        while q:
            cur, d = q.popleft()
            if cur.val > 1:            # 找到一个可以供出硬币的节点
                found = cur
                distance = d
                break
            # 向左右子树和父节点扩展
            for nxt in (cur.left, cur.right, parent[cur]):
                if nxt and nxt not in visited:
                    visited.add(nxt)
                    q.append((nxt, d + 1))
        # 把一枚硬币从 found 搬到 target，沿路径每走一步计一次移动
        moves += distance
        found.val -= 1
        target.val += 1

    return moves
```

> **注意**：上述代码仅作演示，实际在 LeetCode 环境中会因为缺少父指针而无法直接运行。但它完整体现了“每次都找最近的多余节点、搬一次硬币”的暴力思路。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  解释：最坏情况下，每次寻找最近的多余节点需要遍历整棵树（`O(n)`），而缺少硬币的节点可能有 `O(n)` 次，需要重复上述过程，所以总体是 `n × n`。

- **空间复杂度**：`O(n)`  
  解释：我们保存了所有节点的列表以及父指针映射，所需额外空间随节点数线性增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到**瓶颈在于重复遍历**——我们每次都在整棵树里寻找最近的多余节点。  
其实我们并不需要一次一次地搬运，而是可以一次性算出每条边需要搬运多少硬币。

**关键观察**  
- 对于任意子树，只有两件事会影响父节点：  
  1. 子树内部多余（或缺少）的硬币数量  
  2. 为了把这些多余/缺少的硬币搬到父节点，需要经过子树根与父节点之间的那条边多少次搬运  

- 设 `balance(node) = node.val + balance(left) + balance(right) - 1`  
  - `node.val` 是当前节点本身的硬币数  
  - `-1` 表示每个节点最终应该保留 **恰好一枚** 硬币  
  - `balance(left/right)` 是左右子树“净多余”或“净缺少”的硬币数（正数表示子树多余，负数表示子树缺少）

- `balance(node)` 的绝对值正好等于**这条边需要搬运的次数**。  
  - 如果左子树 `balance(left) = 3`，说明左子树整体多出 3 枚硬币，这 3 枚必须经过左子树根到 `node` 的这条边搬走，需要 3 步。  
  - 同理如果是 `-2`，则需要从 `node` 向左子树搬 2 枚硬币，同样是 2 步。

因此，只要我们**后序遍历（后左后右先根）**，在返回每个节点的 `balance` 时把 `abs(balance(left)) + abs(balance(right))` 加到全局计数器中，最后计数器的值就是最少搬运次数。

> **类比**：想象每个子树是一座小仓库，`balance` 表示仓库里多余或缺少的货物数量。把货物从仓库搬到父仓库只能走唯一的那条通道——于是搬运次数就是“货物数量”。我们把所有通道的搬运次数加起来，就是总搬运次数。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    def distributeCoins(self, root: TreeNode) -> int:
        """
        采用后序遍历（深度优先搜索），一次性算出每条边的搬运次数。
        """
        self.moves = 0          # 全局计数器，记录总搬运次数

        def dfs(node: TreeNode) -> int:
            """
            返回值：当前子树的净硬币数（多余-缺少）。
            同时把该子树内部产生的搬运次数累加到 self.moves。
            """
            if not node:
                return 0        # 空节点贡献 0

            # 递归计算左、右子树的净硬币数
            left_balance = dfs(node.left)
            right_balance = dfs(node.right)

            # 左、右子树各自需要搬运的次数，就是它们净硬币数的绝对值
            self.moves += abs(left_balance) + abs(right_balance)

            # 当前节点的净硬币数 = 本身硬币数 + 左子树净数 + 右子树净数 - 1（留给自己的一枚）
            net = node.val + left_balance + right_balance - 1
            return net          # 把这个净数交给父节点继续处理

        dfs(root)                # 从根节点启动递归
        return self.moves
```

> 代码每一行都有中文注释，直接复制即可运行。

#### 复杂度

- **时间复杂度**：`O(n)`  
  解释：我们只遍历每个节点一次，所有计算都在遍历过程中完成，没有额外的搜索。`n` 是节点数，线性时间。

- **空间复杂度**：`O(h)`（递归栈），最坏情况 `O(n)`  
  解释：递归深度等于树的高度 `h`，在完全不平衡的链状树中 `h = n`，否则在平衡树中 `h ≈ log n`。这属于额外的函数调用栈空间。

---

## 心得

- **核心技巧**：后序遍历（DFS）配合**子树净平衡**的思想。  
  把每个子树的“多余/缺少”硬币数抽象成一个整数，利用绝对值直接得到搬运次数。

- **适用的题型**  
  1. **二叉树的平衡转移**：如 “二叉树中所有节点的子树和相等” 类题。  
  2. **树上流量/资源分配**：如 “二叉树的最大路径和” 需要把子树信息向上汇总。  
  3. **后序递归求解的 DP**：如 “删除节点使二叉树成为满二叉树” 等。

- **一句话总结**：**把每棵子树的“盈亏”压缩成一个整数，沿树的边累加绝对值，即得最少搬运次数**。

---

## 反思

- **第一反应**：看到“每次搬一次硬币，要求最少次数”，本能想到 **贪心** 或 **逐步模拟**，于是写出了暴力遍历的思路。  
- **最容易踩的坑**  
  - 忘记每个节点最终必须保留 **恰好一枚**，导致 `balance` 计算时少了 `-1`。  
  - 递归返回值写错成 `node.val + left + right`，会把根节点也算进来，导致答案偏大。  
  - 边界情况：单节点树（已经满足）应返回 `0`，代码中必须处理 `None` 节点。  

- **下次遇到同类题**，第一步应该先**思考“局部盈余/缺口如何向父节点传递”**，尝试用 **后序 DFS 把信息压缩**，而不是直接模拟搬运过程。这样往往能把时间从 `O(n²)` 降到 `O(n)`。