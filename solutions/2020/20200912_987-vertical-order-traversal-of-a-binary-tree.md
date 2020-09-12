# #987. 二叉树的垂直遍历 / Vertical Order Traversal of a Binary Tree

> 难度：困难 · 标签：Hash Table、Tree、Depth-First Search、Breadth-First Search、Sorting、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/vertical-order-traversal-of-a-binary-tree/)

---

## 题目（英文原版）

**Description**

Given the root of a binary tree, calculate the vertical order traversal of the binary tree.
For each node at position (row, col), its left and right children will be at positions (row + 1, col - 1) and (row + 1, col + 1) respectively. The root of the tree is at (0, 0).
The vertical order traversal of a binary tree is a list of top-to-bottom orderings for each column index starting from the leftmost column and ending on the rightmost column. There may be multiple nodes in the same row and same column. In such a case, sort these nodes by their values.
Return the vertical order traversal of the binary tree.

**Examples**

**Example 1:**

```
Input: root = [3,9,20,null,null,15,7]
Output: [[9],[3,15],[20],[7]]
Explanation:
Column -1: Only node 9 is in this column.
Column 0: Nodes 3 and 15 are in this column in that order from top to bottom.
Column 1: Only node 20 is in this column.
Column 2: Only node 7 is in this column.
```

**Example 2:**

```
Input: root = [1,2,3,4,5,6,7]
Output: [[4],[2],[1,5,6],[3],[7]]
Explanation:
Column -2: Only node 4 is in this column.
Column -1: Only node 2 is in this column.
Column 0: Nodes 1, 5, and 6 are in this column.
          1 is at the top, so it comes first.
          5 and 6 are at the same position (2, 0), so we order them by their value, 5 before 6.
Column 1: Only node 3 is in this column.
Column 2: Only node 7 is in this column.
```

**Example 3:**

```
Input: root = [1,2,3,4,6,5,7]
Output: [[4],[2],[1,5,6],[3],[7]]
Explanation:
This case is the exact same as example 2, but with nodes 5 and 6 swapped.
Note that the solution remains the same since 5 and 6 are in the same location and should be ordered by their values.
```

**Constraints**

- The number of nodes in the tree is in the range [1, 1000].
- 0 <= Node.val <= 1000

---

## 题目（中文翻译）

给定一棵二叉树 (binary tree) 的根节点，计算该二叉树的垂直顺序遍历 (vertical order traversal)。  
对于每个位于位置 (row, col) 的节点，它的左子节点位于 (row + 1, col - 1) ，右子节点位于 (row + 1, col + 1) 。树的根节点位于 (0, 0)。  
二叉树的垂直顺序遍历是按照列索引从最左侧列到最右侧列的顺序，返回每一列中从上到下的节点值列表。若同一列同一行上有多个节点，需要先按行从上到下，再对这些节点按值大小升序排列。  
返回该二叉树的垂直顺序遍历结果。

**示例 1**  
**输入**: `root = [3,9,20,null,null,15,7]`  
**输出**: `[[9],[3,15],[20],[7]]`  
**解释**:  
- 列 -1: 该列只有节点 9。  
- 列 0: 该列的节点是 3 和 15，按从上到下的顺序依次出现。  
- 列 1: 该列只有节点 20。  
- 列 2: 该列只有节点 7。  

**示例 2**  
**输入**: `root = [1,2,3,4,5,6,7]`  
**输出**: `[[4],[2],[1,5,6],[3],[7]]`  
**解释**:  
- 列 -2: 该列只有节点 4。  
- 列 -1: 该列只有节点 2。  
- 列 0: 该列包含节点 1、5、6。  
  - 节点 1 位于最上方，先输出。  
  - 节点 5 和 6 位于同一位置 (2, 0)，因此按值大小排序，5 在前，6 在后。  
- 列 1: 该列只有节点 3。  
- 列 2: 该列只有节点 7。  

**示例 3**  
**输入**: `root = [1,2,3,4,6,5,7]`  
**输出**: `[[4],[2],[1,5,6],[3],[7]]`  
**解释**:  
该例与示例 2 完全相同，只是节点 5 与 6 的位置互换。由于它们处于同一坐标，仍需按值大小排序，结果与示例 2 相同。  

**约束条件**  
- 树中节点的数量在 `[1, 1000]` 区间内。  
- `0 <= Node.val <= 1000`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把 **每个节点** 的坐标 `(row, col)` 记录下来，然后把所有节点按照 **列号**、**行号**、**节点值** 的顺序排好序，最后把同一列的节点值放到一起即可。  

- **数据结构**  
  - **列表** `nodes`：存放三元组 `(col, row, val)`，相当于把树的所有节点摊开成一张“表”。  
  - **字典** `col_table`：`col → [val]`，用来把排好序的节点按列收集起来。字典可以类比为 **查字典**，键（key）是列号，值（value）是该列所有节点的值列表。  

- **为什么正确**  
  - 题目已经明确规定：左子节点的列号减 1、右子节点的列号加 1，行号都加 1。只要我们在遍历树的过程中把这些规则照搬进去，就能得到每个节点的真实坐标。  
  - 排序规则正好是：先按列号从左到右，再在同一列里按行号从上到下，行号相同再按节点值从小到大。把所有三元组按照 `(col, row, val)` 这三个键排序后，顺序必然满足题目要求。  

- **复杂度分析（大白话）**  
  - **时间**：遍历树一次是 `O(N)`（`N` 为节点数），随后对 `N` 条记录整体排序，排序的代价大约是 `N log N`，所以总时间是 `O(N log N)`。可以把 `log N` 想象成 “把 1000 条记录排好序，大约需要 10 次比较”。  
  - **空间**：我们额外用了一个长度为 `N` 的列表来存坐标，和一个字典来分列，都是 `O(N)` 的额外空间。  

#### 代码（Python）  

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

from collections import defaultdict

class Solution:
    def verticalTraversal(self, root: TreeNode):
        """
        暴力思路：DFS 收集 (col, row, val) → 全局排序 → 按列分组
        """
        nodes = []                     # 用来存放所有 (col, row, val)

        # 深度优先遍历，记录每个节点的坐标
        def dfs(node, row, col):
            if not node:
                return
            nodes.append((col, row, node.val))   # 记录当前节点
            dfs(node.left,  row + 1, col - 1)    # 左子树：列号-1，行号+1
            dfs(node.right, row + 1, col + 1)    # 右子树：列号+1，行号+1

        dfs(root, 0, 0)                # 从根节点 (0,0) 开始

        # 按 (col, row, val) 排序
        nodes.sort()                   # Python 默认元组比较就是逐元素比较

        # 把排好序的节点按列收集起来
        col_table = defaultdict(list)  # col → [val]
        for col, row, val in nodes:
            col_table[col].append(val)

        # 按列号从左到右输出结果
        return [col_table[c] for c in sorted(col_table)]
```

#### 复杂度  

- **时间复杂度**：`O(N log N)` —— 主要花在对 `N` 条记录的全局排序上。  
- **空间复杂度**：`O(N)` —— 额外存放坐标的列表和分列的字典。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**排序** 是必不可少的，因为题目要求在同一列、同一行的节点要按值升序排列。  
唯一的瓶颈是：我们把所有节点一次性收集完再排序，这会导致一次性占用 `O(N)` 的额外空间，而且排序的比较次数会稍微多一些。  

**优化思路**：  
1. **层序遍历（BFS）** 天然是 **从上到下** 访问节点的，这正好满足“行号小的先出现”的要求。  
2. 在 BFS 的过程中，**把每一层的节点按照列号从小到大放进同一个队列**，这样同一层里列号更左的节点会先被处理。  
3. 为了在同一层、同一列出现多个节点时还能按值排序，我们可以把 **每一列的节点放进一个小根堆（priority queue）**，堆会自动按照 `(row, val)` 的顺序弹出。  
4. 最后，只需要把每列的堆中元素依次弹出（行号已经是递增的），得到的顺序即是答案。  

> **核心数据结构**  
> - **队列（Queue）**：实现 BFS，像排队买票一样，先进去的先出来，保证“上层先处理”。  
> - **默认字典 + 小根堆**：`col → [(row, val)]`，堆的比较规则是先比较行号 `row`，相同再比较节点值 `val`，相当于把同一列的节点排成一条有序的“小队”。  

> **类比**：想象你在观察一座城市的高楼，每层楼的建筑从左到右依次出现。如果你把每层楼的建筑编号记录下来，然后在每条街道（列）上把同一层的建筑再按照高度（行）和编号（值）排序，最后按街道顺序输出，就是我们要的视图。

**为什么更好**  
- BFS 本身只需要 `O(N)` 的时间遍历树。  
- 每个节点只会被放进一次堆，堆的插入/弹出是 `O(log K)`（`K` 为同列节点数），整体仍是 `O(N log N)`，但常数更小。  
- 只需要 **一次遍历** 完成收集，无需额外的全局排序步骤，代码更直观。  

#### 代码（Python）  

```python
from collections import defaultdict, deque
import heapq

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    def verticalTraversal(self, root: TreeNode):
        """
        最优思路：BFS + 按列收集小根堆
        1) BFS 同时记录 (row, col)
        2) col_table[col] 是一个堆，元素为 (row, val)
        3) BFS 结束后，按列号从左到右弹堆，得到每列的有序结果
        """
        if not root:
            return []

        # col → [(row, val)]，用堆维护行号/节点值的顺序
        col_table = defaultdict(list)

        # 队列里保存 (node, row, col)
        q = deque([(root, 0, 0)])

        while q:
            node, row, col = q.popleft()
            # 把当前节点放进对应列的堆
            heapq.heappush(col_table[col], (row, node.val))

            # 左子节点：列号-1，行号+1
            if node.left:
                q.append((node.left, row + 1, col - 1))
            # 右子节点：列号+1，行号+1
            if node.right:
                q.append((node.right, row + 1, col + 1))

        # 取出所有列号，排序后依次输出每列的节点值
        result = []
        for col in sorted(col_table.keys()):
            column_vals = []
            # 按堆弹出顺序得到 (row 小 → 大, 同 row 时 val 小 → 大)
            while col_table[col]:
                row, val = heapq.heappop(col_table[col])
                column_vals.append(val)
            result.append(column_vals)

        return result
```

#### 复杂度  

- **时间复杂度**：`O(N log N)`  
  - BFS 本身是 `O(N)`。  
  - 每个节点在对应列的堆中插入一次，堆的操作是 `O(log K)`，`K ≤ N`，所以整体仍是 `O(N log N)`，但只涉及局部堆，常数更小。  
- **空间复杂度**：`O(N)`  
  - 队列最多保存一层的节点，最多 `O(width)`，在最坏情况下仍是 `O(N)`。  
  - `col_table` 保存所有节点的 `(row, val)`，也是 `O(N)`。  

---  

## 心得  

- **核心技巧**：**层序遍历（BFS） + 按列收集并使用小根堆维护行/值的顺序**。  
- **适用的题型**  
  1. “二叉树的垂直遍历” 系列（如 LeetCode 987、1039）。  
  2. “二叉树的水平/对角线遍历” 需要按照层/列的顺序分组。  
  3. “坐标系下的点排序” 类似题目（例如把二维平面上的点按 `x`、`y` 排序）。  
- **一句话总结**：**先用 BFS 把节点按层（行）顺序遍历，再用堆在每列内部完成行号/值的排序**，即可一次遍历搞定垂直顺序。  

---  

## 反思  

- **第一反应**：看到“行、列”坐标，立刻想到把每个节点的 `(row, col)` 记下来，然后全局排序。  
- **最容易踩的坑**  
  - **同一行同一列的节点顺序**：如果只用 `dict[col] → list`，会忘记在同一列内部再按 `row`、`val` 排序，导致答案错误。  
  - **列号的正负顺序**：记得在最终输出时要对列号进行排序（左负右正）。  
  - **空树**：虽然题目保证至少有一个节点，写代码时仍要防止 `root is None` 的情况。  
- **下次遇到同类题**，第一步应该：**先决定遍历方式（DFS 还是 BFS）来得到行列坐标，再思考如何在同一列内部保持行号/值的有序**，必要时使用堆或排序来完成。