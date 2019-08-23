# #543. 二叉树的直径 / Diameter of Binary Tree

> 难度：简单 · 标签：Tree、Depth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/diameter-of-binary-tree/)

---

## 题目（英文原版）

**Description**

Given the root of a binary tree, return the length of the diameter of the tree.
The diameter of a binary tree is the length of the longest path between any two nodes in a tree. This path may or may not pass through the root.
The length of a path between two nodes is represented by the number of edges between them.

**Examples**

**Example 1:**

```
Input: root = [1,2,3,4,5]
Output: 3
Explanation: 3 is the length of the path [4,2,1,3] or [5,2,1,3].
```

**Example 2:**

```
Input: root = [1,2]
Output: 1
```

**Constraints**

- The number of nodes in the tree is in the range [1, 104].
- -100 <= Node.val <= 100

---

## 题目（中文翻译）

给定二叉树（binary tree）的根节点 `root`，返回该树的直径长度。  
二叉树的直径是树中任意两个节点之间最长路径的长度。该路径 **可能** 经过根节点，也可能不经过。  
两个节点之间路径的长度用它们之间的边数来表示。

**示例 1**  
Input: `root = [1,2,3,4,5]`  
Output: `3`  
Explanation: `3` 是路径 `[4,2,1,3]` 或 `[5,2,1,3]` 的长度。

**示例 2**  
Input: `root = [1,2]`  
Output: `1`

### 约束条件
- 树中节点的数量在 `[1, 10^4]` 区间内。  
- `-100 <= Node.val <= 100`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**对每一个节点**都去算一次“以它为根的子树的左、右子树的最高深度”。  
- 先把树想象成一棵**家谱树**，每个节点就是一个人，左子树和右子树分别是他的两个子女的后代。  
- “以某个节点为根的子树的最高深度”相当于**从这个人往下数最多要几代**才能到最远的后代。  

直觉解的步骤：

1. 对树中的每一个节点 `node`（可以用一次遍历把所有节点收集到列表里），  
2. 分别**递归**求它左子树的最大深度 `leftDepth`，右子树的最大深度 `rightDepth`（每次递归都是从头再算一次）。  
3. 以 `node` 为“转折点”的路径长度 = `leftDepth + rightDepth`（因为路径是从左最深的叶子上来，再经过 `node`，再到右最深的叶子）。  
4. 把所有节点得到的路径长度取最大值，即为树的直径。

> **为什么正确？**  
> 直径一定是一条从某个叶子节点走到另一个叶子节点的最长路径。任意一条最长路径必定在某个节点 `v` 处左、右子树的深度之和最大（如果路径不经过根，也一定会在它的“转折点”满足这个性质），所以遍历所有节点并取最大 `leftDepth+rightDepth` 能覆盖所有可能的最长路径。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的值（本题不关心具体数值）
        self.left = left        # 左子树
        self.right = right      # 右子树


def maxDepth(root: TreeNode) -> int:
    """返回以 root 为根的子树的最大深度（边的条数）"""
    if not root:                     # 空树深度为 0
        return 0
    # 递归求左、右子树的深度，然后取较大者 + 1（+1 代表连接到当前节点这条边）
    left = maxDepth(root.left)
    right = maxDepth(root.right)
    return max(left, right) + 1


def diameterOfBinaryTree_bruteforce(root: TreeNode) -> int:
    """暴力解：对每个节点都重新计算左右子树深度，取最大 left+right"""
    if not root:
        return 0

    # 先把所有节点收集起来，方便遍历
    nodes = []

    def preorder(node: TreeNode):
        if not node:
            return
        nodes.append(node)          # 记录当前节点
        preorder(node.left)
        preorder(node.right)

    preorder(root)

    max_diameter = 0
    for node in nodes:
        # 对每个节点重新计算左、右子树深度（这里又会遍历它的子树，导致重复计算）
        left = maxDepth(node.left)
        right = maxDepth(node.right)
        max_diameter = max(max_diameter, left + right)  # 边数 = 左深度 + 右深度

    return max_diameter
```

#### 复杂度  

- **时间复杂度：** `O(N²)`  
  - 解释：树里有 `N` 个节点。对每个节点我们都要 **完整遍历它的子树** 来求深度，最坏情况下（比如一条链）第一次遍历 `N`，第二次遍历 `N‑1`，……，总和大约是 `N + (N‑1) + … + 1 ≈ N²/2`，所以是二次方级别。  
- **空间复杂度：** `O(N)`  
  - 解释：递归栈深度最坏会是 `N`（链形树），另外我们还用了一个 `nodes` 列表存所有节点，同样是 `N` 大小。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**重复计算左、右子树深度是主要的性能瓶颈**。  
如果我们在一次深度优先遍历（DFS）中，同时得到：

1. 当前节点的**最大深度**（返回值），  
2. 以当前节点为“转折点”的路径长度 `leftDepth + rightDepth`，并实时更新全局最大直径  

就可以把 `O(N²)` 的重复遍历消除，做到 **一次遍历搞定**，即 `O(N)`。

实现细节：

- **后序遍历**（先处理左右子树，再处理当前节点）最适合，因为要先知道左右子树的深度才能算出以当前节点为中心的直径。  
- 用一个**全局变量** `ans`（或作为外层函数的非局部变量）记录遍历过程中出现的最大 `leftDepth + rightDepth`。  
- 对每个节点 `node`：  
  - `left = dfs(node.left)` 获得左子树的最大深度  
  - `right = dfs(node.right)` 获得右子树的最大深度  
  - **更新直径**：`ans = max(ans, left + right)`（因为路径长度是边的数目）  
  - **返回给父节点的深度**：`max(left, right) + 1`（+1 表示从当前节点向下走一步）  

> **类比**：把树想成一条河流网络，`dfs` 就像水流从叶子流向根部，沿途把“最长支流长度”传递上来，同时在每个交汇点记录“左右支流之和”的最大值，这就是直径。

#### 代码（Python）

```python
def diameterOfBinaryTree(root: TreeNode) -> int:
    """
    最优解：一次 DFS，边遍历边更新全局直径。
    返回值是树的直径（以边的数量计）。
    """
    ans = 0                     # 用来存放遍历过程中找到的最大直径

    def dfs(node: TreeNode) -> int:
        """返回以 node 为根的子树的最大深度，同时更新 ans"""
        nonlocal ans            # 声明我们要修改外层变量 ans
        if not node:
            return 0            # 空节点的深度是 0（不计边）

        # 递归得到左、右子树的深度
        left = dfs(node.left)
        right = dfs(node.right)

        # 以 node 为转折点的路径长度 = 左深度 + 右深度
        ans = max(ans, left + right)   # 更新全局最大直径

        # 向上返回当前节点的深度（父节点只需要最长的一条向下的边）
        return max(left, right) + 1

    dfs(root)                   # 从根节点开始遍历
    return ans                  # ans 已经是所有可能路径的最大边数
```

#### 复杂度  

- **时间复杂度：** `O(N)`  
  - 解释：每个节点只被访问一次，递归体内的操作都是 `O(1)`，所以整体是线性时间。相比暴力解的 `N²`，快了很多。  
- **空间复杂度：** `O(H)`（`H` 为树的高度）  
  - 解释：递归栈的深度等于树的高度。最坏情况下（链形树）`H = N`，此时空间是 `O(N)`；平均情况下（平衡二叉树）`H ≈ log N`，更省内存。  

---

## 心得  

- **核心技巧**：**后序深度优先遍历 + 同时返回子树深度**，在遍历过程中实时维护全局答案。  
- **适用的题型**：  
  1. “二叉树的最大路径和”（LeetCode 124）——同样需要在遍历时把左、右子树的贡献合并。  
  2. “二叉树的最长同值路径”（LeetCode 687）——在 DFS 中记录相同值的最长连线。  
  3. “二叉树的最大宽度”（LeetCode 662）——虽然使用层序遍历，但思路也是一次遍历完成统计。  
- **一句话总结**：**把“求子树信息”与“更新全局答案”合二为一，利用一次 DFS 就能把所有局部信息汇聚成全局最优。**  

---

## 反思  

- **第一反应**：看到“最长路径”，立刻想到“对每个节点算左、右子树的深度”。  
- **最容易踩的坑**：  
  - 把**节点数**和**边数**混淆。直径要求的是边的数量，返回的深度要以“边”为单位（空节点深度 `0`，而不是 `-1`）。  
  - 忘记在递归返回时加 `+1`，导致深度比实际少 1，进而直径也会少 1。  
  - 对于只有一个节点的树，直径应为 `0`（没有边），代码要能正确返回。  
- **下次遇到同类题**，第一步应该想到：**“是否可以在一次遍历中把需要的子树信息返回，同时在遍历过程中更新答案？”** 若答案是肯定的，往往就能把时间复杂度降到 `O(N)`。