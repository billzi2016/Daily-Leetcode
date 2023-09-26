# #2415. 反转二叉树的奇数层 / Reverse Odd Levels of Binary Tree

> 难度：中等 · 标签：Tree、Depth-First Search、Breadth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/reverse-odd-levels-of-binary-tree/)

---

## 题目（英文原版）

**Description**

Given the root of a perfect binary tree, reverse the node values at each odd level of the tree.
Return the root of the reversed tree.
A binary tree is perfect if all parent nodes have two children and all leaves are on the same level.
The level of a node is the number of edges along the path between it and the root node.

**Examples**

**Example 1:**

```
Input: root = [2,3,5,8,13,21,34]
Output: [2,5,3,8,13,21,34]
Explanation: 
The tree has only one odd level.
The nodes at level 1 are 3, 5 respectively, which are reversed and become 5, 3.
```

**Example 2:**

```
Input: root = [7,13,11]
Output: [7,11,13]
Explanation: 
The nodes at level 1 are 13, 11, which are reversed and become 11, 13.
```

**Example 3:**

```
Input: root = [0,1,2,0,0,0,0,1,1,1,1,2,2,2,2]
Output: [0,2,1,0,0,0,0,2,2,2,2,1,1,1,1]
Explanation: 
The odd levels have non-zero values.
The nodes at level 1 were 1, 2, and are 2, 1 after the reversal.
The nodes at level 3 were 1, 1, 1, 1, 2, 2, 2, 2, and are 2, 2, 2, 2, 1, 1, 1, 1 after the reversal.
```

**Constraints**

- The number of nodes in the tree is in the range [1, 214].
- 0 <= Node.val <= 105
- root is a perfect binary tree.

---

## 题目（中文翻译）

给定一棵**完全二叉树**（perfect binary tree）的根节点 `root`，请将树中每个奇数层的节点值进行反转。  
返回反转后的树的根节点 `root`。

- **完全二叉树**：所有父节点都有两个子节点，且所有叶子节点位于同一层。  
- 节点的**层级**（level）指的是从根节点到该节点路径上的边数。

---

## 示例

### 示例 1
**输入**  
`root = [2,3,5,8,13,21,34]`

**输出**  
`[2,5,3,8,13,21,34]`

**解释**  
树只有一个奇数层。  
第 1 层的节点分别是 `3`、`5`，反转后变为 `5`、`3`。

### 示例 2
**输入**  
`root = [7,13,11]`

**输出**  
`[7,11,13]`

**解释**  
第 1 层的节点是 `13`、`11`，反转后变为 `11`、`13`。

### 示例 3
**输入**  
`root = [0,1,2,0,0,0,0,1,1,1,1,2,2,2,2]`

**输出**  
`[0,2,1,0,0,0,0,2,2,2,2,1,1,1,1]`

**解释**  
奇数层的节点值均非零。  
- 第 1 层的节点原本是 `1`、`2`，反转后变为 `2`、`1`。  
- 第 3 层的节点原本是 `1, 1, 1, 1, 2, 2, 2, 2`，反转后变为 `2, 2, 2, 2, 1, 1, 1, 1`。

---

## 约束条件

- 树中节点的数量在 `[1, 214]` 的范围内。  
- `0 <= Node.val <= 10^5`  
- `root` 为一棵**完全二叉树**（perfect binary tree）。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **层序遍历**（Breadth‑First Search），一次把树按层“拍平”。  
具体步骤：

1. 用一个队列把根节点放进去，随后不断弹出队首、把子节点加入队尾，这样弹出的顺序恰好是从上到下、从左到右的层序。
2. 在遍历的过程中，用一个 `level` 计数器记录当前所在的层数（根节点为第 0 层）。
3. 把每一层的所有节点（实际只需要保存它们的引用）放进一个列表 `cur_level_nodes`。遍历完该层后，如果 `level` 是奇数（1、3、5 …），就把 `cur_level_nodes` 中节点的值 **倒序**，即把第 0 个节点的值换成最后一个节点的值，第 1 个换成倒数第 2 个，以此类推。
4. 继续遍历下一层，直到队列为空。

> **类比**：把树看成一本书的章节，层序遍历就是把章节按顺序排好；奇数层倒序就像把这些章节的页码重新排列成相反的顺序。

这种方法一定能得到正确答案，因为我们严格按照题目要求“在每个奇数层把节点值倒序”，没有遗漏也没有多余的操作。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

from collections import deque

def reverseOddLevels(root: TreeNode) -> TreeNode:
    if not root:
        return None

    q = deque([root])      # 队列，用来做层序遍历
    level = 0              # 当前层号，根节点是第 0 层

    while q:
        size = len(q)                      # 本层节点数
        cur_level_nodes = []               # 暂存本层的节点对象

        for _ in range(size):
            node = q.popleft()             # 取出队首节点
            cur_level_nodes.append(node)   # 记录下来，后面可能要改值

            # 将左右子节点加入队列，准备遍历下一层
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)

        # 如果是奇数层，进行值的倒序
        if level % 2 == 1:
            i, j = 0, len(cur_level_nodes) - 1
            while i < j:
                # 交换两个节点的值
                cur_level_nodes[i].val, cur_level_nodes[j].val = (
                    cur_level_nodes[j].val,
                    cur_level_nodes[i].val,
                )
                i += 1
                j -= 1

        level += 1   # 进入下一层

    return root
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  解释：我们遍历每个节点恰好一次（`n` 为节点总数），所以时间随节点数线性增长。  
  用大白话说，树里有多少水果，就要搬多少次箱子，搬一次的时间是固定的。

- **空间复杂度**：`O(n)`（最坏情况）  
  解释：队列里最多会同时存放一层的所有节点。对于完美二叉树，最后一层大约有 `n/2` 个节点，所以空间和 `n` 成正比。  
  用生活化的说法，就是我们要在一次搬运中装满一整层水果的箱子，箱子的容量和水果总量差不多。

---  

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于需要额外的 `O(n)` 队列和 `O(n)` 的临时列表来保存每层的节点。  
其实我们可以 **直接在递归过程中交换对应节点的值**，不必把整层节点先保存下来。

关键观察：

- 在完美二叉树中，**同一层的左侧节点和右侧节点是成对出现的**，比如第 1 层的左子树根节点和右子树根节点对应，第 3 层的最左边节点对应最右边节点，依此类推。
- 如果我们把 **左子树的一个节点** 和 **右子树的镜像节点** 传进去一起递归，当遍历到奇数层时，只需要 **交换它们的值**，随后继续向下递归它们的子节点（左的左 ↔ 右的右，左的右 ↔ 右的左）。

实现方式：

1. 写一个辅助函数 `dfs(left, right, depth)`，其中 `left`、`right` 是当前配对的两个节点，`depth` 表示它们所在的层（根的左右子节点是第 1 层）。
2. 若 `depth` 为奇数，则交换 `left.val` 与 `right.val`。
3. 递归处理下一层的四对配对节点：
   - `dfs(left.left, right.right, depth + 1)`
   - `dfs(left.right, right.left, depth + 1)`
4. 主函数只需要调用一次 `dfs(root.left, root.right, 1)`。

这样做的好处：

- **不需要额外的容器**，只用递归栈保存函数调用信息，空间降到 `O(h)`，其中 `h` 是树高（`log₂ n`），对完美二叉树来说非常小。
- **只遍历一次**，时间仍是 `O(n)`。

> **类比**：把树想成两条对称的河流（左子树、右子树），我们让两条河的对应位置的船只互换货物（节点值），只在奇数桥（层）上换，过程不需要把所有船只排成一行再换。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def reverseOddLevels(root: TreeNode) -> TreeNode:
    """
    使用深度优先搜索（递归）直接在配对节点之间交换值。
    只在奇数层进行交换，递归深度为树的高度，空间开销为 O(log n)。
    """

    def dfs(left: TreeNode, right: TreeNode, depth: int) -> None:
        if not left or not right:
            return

        # 奇数层需要交换值
        if depth % 2 == 1:
            left.val, right.val = right.val, left.val

        # 继续向下配对：左的左 ↔ 右的右，左的右 ↔ 右的左
        dfs(left.left, right.right, depth + 1)
        dfs(left.right, right.left, depth + 1)

    if root:
        dfs(root.left, root.right, 1)   # 从第 1 层开始检查
    return root
```

#### 复杂度  

- **时间复杂度**：`O(n)` — 每个节点只被访问一次，和暴力解一样快。  
  用通俗的话讲，就是我们只搬一次箱子，不需要额外的整理过程。

- **空间复杂度**：`O(log n)`（递归栈） — 树的高度 `h = log₂ n`（因为是完美二叉树），递归调用最多占用 `h` 层栈空间。  
  相比于暴力解的 `O(n)` 队列，这就像只需要一把梯子就能够到最高层，而不是把整栋楼的楼梯都搬上来。

---

## 心得

- **核心技巧**：利用二叉树的对称性，配对递归（双指针）在奇数层交换节点值。
- **适用场景**：  
  1. 需要在同层“镜像”位置进行操作的题目（如 “对称树的值交换”）。  
  2. 只在特定层做处理的层次问题（如 “奇数层翻转值”）。  
  3. 需要在树上做 “成对” 操作的题目（如 “翻转每两层的子树结构”）。
- **一句话总结**：**把左右子树当成镜像，奇数层直接交换对应节点的值**，即可在 O(n) 时间、O(log n) 空间内完成。

## 反思

- **第一反应**：看到“完美二叉树”“奇数层倒序”，立刻想到层序遍历并把每层的节点收集起来再倒序。
- **最容易踩的坑**：  
  - 忘记根节点是第 0 层，导致把第 0 层（偶数层）误判为需要翻转。  
  - 在递归实现时配对错误（左的左 ↔ 右的左等），会导致交换不对称位置的值。  
  - 递归终止条件写漏了，导致空指针异常。
- **下次类似题目第一步**：先判断“是否可以利用树的对称性”，如果可以，尝试 **配对递归**（双指针）而不是“一层层收集”。这样往往能直接得到 O(1) 额外空间的最优方案。