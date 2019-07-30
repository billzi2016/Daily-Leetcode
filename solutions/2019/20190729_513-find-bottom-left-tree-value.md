# #513. 二叉树最底层最左侧节点值 / Find Bottom Left Tree Value

> 难度：中等 · 标签：Tree、Depth-First Search、Breadth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/find-bottom-left-tree-value/)

---

## 题目（英文原版）

**Description**

Given the root of a binary tree, return the leftmost value in the last row of the tree.

**Examples**

**Example 1:**

```
Input: root = [2,1,3]
Output: 1
```

**Example 2:**

```
Input: root = [1,2,3,4,null,5,6,null,null,7]
Output: 7
```

**Constraints**

- The number of nodes in the tree is in the range [1, 104].
- -231 <= Node.val <= 231 - 1

---

## 题目（中文翻译）

给定二叉树（binary tree）的根节点（root），返回树的最后一行中最左侧的值。

**示例 1:**  

**示例 2:**  

**约束条件：**  

- 树中节点的数量在区间 `[1, 10^4]` 内。  
- `-2^31 <= 节点值（Node.val） <= 2^31 - 1`

**示例：**  

**示例 1:**  
```
Input: root = [2,1,3]
Output: 1
```

**示例 2:**  
```
Input: root = [1,2,3,4,null,5,6,null,null,7]
Output: 7
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的办法是**层序遍历**（Breadth‑First Search，BFS），也就是从上往下、从左到右一层层访问树的节点。  
可以把树的每一层想象成一排排的座位，左边的座位编号最小，右边的座位编号最大。我们只要记下每一层最左边的座位号（节点值），最后一次更新的那个值就是**最底层最左边的节点**。

实现层序遍历常用 **队列**（queue）。队列好比排队买票的队伍，先进入的先出（先入先出），正好符合“先访问上一层的左子树，再访问右子树”的顺序。

**为什么正确**  
因为 BFS 按层访问，遍历完第 `i` 层后一定已经遍历完了所有更高的层。我们每遍历完一层，就把该层最左边的节点值保存下来。遍历结束时，保存的值必然是**最后一层**（最底层）最左边的节点。

**复杂度分析**  
- 时间：每个节点恰好进队列一次、出队列一次，整体是 `O(N)`（N 为节点数）。  
- 空间：队列里最多同时保存同一层的所有节点，最坏情况是树是完全二叉树，最后一层大约有 `N/2` 个节点，所以空间是 `O(N)`。

> 大白话解释：`O(N)` 就是“和节点数成正比”，如果树有 10 万个节点，时间大概是 10 万步左右；`O(N)` 的空间意味着我们最多要在内存里同时放下 10 万个节点的引用。

#### 代码（Python）

```python
from collections import deque
from typing import Optional

# 二叉树节点的定义（LeetCode 默认）
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的数值
        self.left = left        # 左子节点
        self.right = right      # 右子节点

def findBottomLeftValue(root: Optional[TreeNode]) -> int:
    """层序遍历，记录每层最左边的节点值"""
    q = deque([root])          # 初始化队列，只放根节点
    leftmost = root.val        # 先把根节点当成答案

    while q:
        level_size = len(q)    # 当前层有多少节点
        # 遍历当前层的所有节点
        for i in range(level_size):
            node = q.popleft() # 取出队首节点（先入先出）
            # 第一次弹出的节点就是本层最左边的节点
            if i == 0:
                leftmost = node.val
            # 把左子节点、右子节点依次加入队列（左先入，保证左边先出）
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)

    return leftmost
```

#### 复杂度

- **时间复杂度**：`O(N)` — 每个节点只被访问一次，和节点数量成线性关系。  
- **空间复杂度**：`O(N)` — 最坏情况下队列里会同时存放一层的所有节点，约占总节点数的一半。

---

### 2. 最优解

#### 思路  
暴力解的时间已经是 `O(N)`，已经是最优的时间复杂度了。我们可以**优化空间**，把额外的 `O(N)` 队列去掉，改用 **深度优先搜索**（DFS）递归。

DFS 的递归调用栈天然就保存了“从根到当前节点的路径”。我们在遍历树时，记录**当前遍历到的最大深度**以及**对应深度最左边的节点值**。因为我们先递归左子树，再递归右子树，第一次遇到某一层时一定是最左边的节点。只要在遍历时发现更深的层，就更新答案。

类比：把树想象成一座多层楼的建筑，左侧的房间是“左子树”。我们派一个小机器人从根节点（入口）出发，**先往左边走到底**（左子树），再回头走右边。机器人记录下它第一次踏进每一层的房间号（节点值），当它走到最高层时，记录的就是**最底层最左边的房间**。

**关键点**  
- 用两个全局变量（或函数闭包）保存 `max_depth`（目前已知的最大深度）和 `answer`（对应的左侧节点值）。  
- 递归函数 `dfs(node, depth)`：  
  1. 若 `node` 为 `None`，直接返回。  
  2. 若 `depth > max_depth`，说明我们来到一个更深的层，更新 `max_depth` 与 `answer`。  
  3. 先递归左子树，再递归右子树，保证左侧先被访问。

**复杂度分析**  
- 时间：仍然是遍历所有节点一次，`O(N)`。  
- 空间：递归栈的深度等于树的高度。最坏情况下（树呈链状）高度为 `N`，此时空间是 `O(N)`；平均情况下（平衡二叉树）高度约为 `log N`，空间是 `O(log N)`。相较于 BFS 的 `O(N)` 队列，DFS 在大多数情况下更省内存。

#### 代码（Python）

```python
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def findBottomLeftValue(root: Optional[TreeNode]) -> int:
    """DFS 递归，记录遍历到的最深层的最左节点"""
    # 用列表包装，使其在内部函数里可以被修改（类似全局变量）
    max_depth = [-1]   # 当前已知的最大深度，初始为 -1 方便第 0 层更新
    answer = [None]    # 对应的左侧节点值

    def dfs(node: Optional[TreeNode], depth: int) -> None:
        """深度优先遍历"""
        if not node:
            return               # 空节点直接返回

        # 第一次到达某一层时 depth > max_depth，说明这是该层最左侧节点
        if depth > max_depth[0]:
            max_depth[0] = depth
            answer[0] = node.val

        # 先左后右，确保左侧先被访问
        dfs(node.left, depth + 1)
        dfs(node.right, depth + 1)

    dfs(root, 0)   # 从根节点、深度 0 开始
    return answer[0]
```

#### 复杂度

- **时间复杂度**：`O(N)` — 每个节点恰好被访问一次。  
- **空间复杂度**：`O(H)`，其中 `H` 为树的高度。  
  - 最坏情况（链状树）`H = N` → `O(N)`。  
  - 平衡二叉树时 `H ≈ log₂N` → `O(log N)`，通常比 BFS 的 `O(N)` 更省空间。

---

## 心得

- **核心技巧**：**先左后右的深度优先搜索**，配合“第一次到达更深层时更新答案”。  
- **适用场景**：  
  1. 求二叉树最左/最右/最上/最下的节点（如 “Find Largest Value in Each Tree Row”）。  
  2. 需要在遍历时记录层次信息的题目（如 “Binary Tree Right Side View”）。  
  3. 需要在递归过程中保留全局状态的题目（如 “Maximum Depth of Binary Tree”）。  
- **一句话总结**：**左子树先走，深度一增就记，最深层的第一位就是答案**。

---

## 反思

- **第一反应**：看到“最后一行最左边”，立刻想到层序遍历，因为层序天然按行排。  
- **最容易踩的坑**：  
  - BFS 时忘记在每层遍历开始时记录第一个节点，导致取到的是最右边的。  
  - DFS 时递归顺序写反（先右后左），会把最右侧的节点误当成答案。  
  - 边界情况：树只有一个节点时，答案就是根节点本身，需要确保代码能直接返回。  
- **下次遇到类似题**：第一步先**明确是“层级”还是“路径”需求**，如果是“层级”，考虑 BFS；如果要求“最左/最右的深层节点”，尝试**左/右优先的 DFS**，并在递归时记录深度。