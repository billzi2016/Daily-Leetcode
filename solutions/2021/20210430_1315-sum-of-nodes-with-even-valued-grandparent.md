# #1315. 偶数值祖父节点的节点和 / Sum of Nodes with Even-Valued Grandparent

> 难度：中等 · 标签：Tree、Depth-First Search、Breadth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/sum-of-nodes-with-even-valued-grandparent/)

---

## 题目（英文原版）

**Description**

Given the root of a binary tree, return the sum of values of nodes with an even-valued grandparent. If there are no nodes with an even-valued grandparent, return 0.
A grandparent of a node is the parent of its parent if it exists.

**Examples**

**Example 1:**

```
Input: root = [6,7,8,2,7,1,3,9,null,1,4,null,null,null,5]
Output: 18
Explanation: The red nodes are the nodes with even-value grandparent while the blue nodes are the even-value grandparents.
```

**Example 2:**

```
Input: root = [1]
Output: 0
```

**Constraints**

- The number of nodes in the tree is in the range [1, 104].
- 1 <= Node.val <= 100

---

## 题目（中文翻译）

给定一棵二叉树（binary tree）的根节点 `root`，返回所有满足 **祖父节点（grandparent）的值为偶数** 的节点值之和。如果不存在满足条件的节点，返回 `0`。  
节点的祖父节点是指其父节点的父节点（如果存在）。

**示例 1**  
**示例 2**  
**约束条件**  

#### 示例
**示例 1**  
输入：`root = [6,7,8,2,7,1,3,9,null,1,4,null,null,null,5]`  
输出：`18`  
解释：红色节点是拥有偶数值祖父节点的节点，蓝色节点是偶数值的祖父节点。

**示例 2**  
输入：`root = [1]`  
输出：`0`

#### 约束条件
- 树中节点的数量在范围 `[1, 10^4]` 内。  
- `1 <= Node.val <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**遍历树的每一个节点**，对每个节点再去**找它的祖父节点**（即父节点的父节点），判断祖父的值是否为偶数，若是则把当前节点的值加到答案里。

- **遍历树**：可以用递归的深度优先搜索（DFS）或层序遍历（BFS），这里用递归实现。
- **找祖父**：对当前节点 `cur`，我们可以先记录它的父节点 `parent`，然后在父节点的子树里再次遍历一次，找到 `parent` 的父节点 `grandparent`。这一步相当于在已经遍历好的树上**再走一遍**，所以整体会出现 **两层循环** 的效果。

> 类比：把树想象成一棵家谱树，暴力做法就像是“每找一个人，就去翻遍整棵家谱，看看他上上代（祖父）是谁”。显然，这样会重复很多工作。

**为什么正确**：只要我们真的找到了每个节点的祖父，并检查了它的奇偶性，就不会漏掉任何符合条件的节点，所以答案一定是对的。

**时间/空间复杂度**  
- 对每个节点，我们都要再遍历一次去找祖父，最坏情况下相当于 **O(n²)**（n 为节点数）。  
  - **O(n²)** 可以理解为：如果树有 10,000 个节点，程序大概会进行 10,000 × 10,000 = 1 亿次基本操作，显然会超时。  
- 递归调用栈的深度最多等于树的高度，最坏是 O(n)（链状树），因此**空间复杂度是 O(n)**。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的数值
        self.left = left        # 左子树
        self.right = right      # 右子树


def sumEvenGrandparent(root: TreeNode) -> int:
    """暴力版：对每个节点都重新找一次祖父"""
    if not root:
        return 0

    # 辅助函数：在整棵树中找 target 的父节点（返回 None 表示没有父节点）
    def find_parent(cur, target):
        if not cur:
            return None
        if cur.left is target or cur.right is target:
            return cur
        # 在左子树或右子树继续找
        left = find_parent(cur.left, target)
        if left:
            return left
        return find_parent(cur.right, target)

    # 主遍历：对每个节点检查祖父是否偶数
    total = 0

    def dfs(node):
        nonlocal total
        if not node:
            return
        # 先找父节点
        parent = find_parent(root, node)
        if parent:
            # 再找祖父节点
            grand = find_parent(root, parent)
            if grand and grand.val % 2 == 0:   # 祖父是偶数
                total += node.val
        # 继续遍历左右子树
        dfs(node.left)
        dfs(node.right)

    dfs(root)
    return total
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 对每个节点都要再遍历一次整棵树找祖父，等价于两层循环。  
- **空间复杂度**：`O(n)`  
  - 递归栈的最大深度是树的高度，最坏情况下等于节点数 n（链状树）。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**瓶颈在于每次都重新遍历整棵树去找祖父**。其实在一次遍历的过程中，我们已经能够知道每个节点的父亲是谁，只要把父亲的信息再往下传递，就能在同一次遍历时直接得到祖父。

**关键点**：

1. **在递归函数的参数里同时携带「父节点」和「祖父节点」**。  
   - 当我们从父节点递归到子节点时，当前的父节点就会变成子节点的「父亲」；原来的父节点再往上一层，就是子节点的「祖父」。
2. **只要祖父的值是偶数，就把当前节点的值累加**。  
   - 这里不需要再去搜索，只要在递归入口检查 `grandparent`（祖父）是否为 `None`（不存在）或是否为偶数即可。

**类比**：想象你在走一条楼梯，每走一步，你都把「上一层」的编号记下来，这样站在第 k 层时，你已经知道第 k‑1 层（父层）和第 k‑2 层（祖父层）的编号，无需再回头查找。

**实现细节**：

- 使用深度优先搜索（递归）遍历二叉树。  
- 递归函数 `dfs(node, parent, grandparent)`：
  - `node` 当前访问的节点；
  - `parent` 当前节点的父亲（可能为 `None`）；
  - `grandparent` 当前节点的祖父（可能为 `None`）。
- 在函数体内：
  - 若 `grandparent` 存在且值为偶数，则 `ans += node.val`。
  - 递归调用左子树 `dfs(node.left, node, parent)`，右子树同理。

这样只遍历一次树，时间复杂度降为 **O(n)**。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def sumEvenGrandparent(root: TreeNode) -> int:
    """最优解：一次遍历，携带父、祖父信息"""
    total = 0                     # 用来累计符合条件的节点值

    def dfs(node: TreeNode, parent: TreeNode, grandparent: TreeNode):
        """递归遍历二叉树
        node        -> 当前节点
        parent      -> 当前节点的父亲（可能为 None）
        grandparent -> 当前节点的祖父（可能为 None）"""
        nonlocal total
        if not node:
            return                # 空节点直接返回

        # 如果祖父存在且是偶数，则把当前节点的值加入答案
        if grandparent and grandparent.val % 2 == 0:
            total += node.val

        # 继续向下遍历，更新 parent 与 grandparent 的指向
        dfs(node.left, node, parent)    # 左子树：当前变父亲，父亲变祖父
        dfs(node.right, node, parent)   # 右子树同理

    dfs(root, None, None)        # 从根节点开始，根没有父亲和祖父
    return total
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 每个节点只访问一次，等价于一次线性遍历。相比暴力的 `O(n²)`，快了很多。  
- **空间复杂度**：`O(h)`（h 为树的高度）  
  - 递归栈占用的空间与树的深度成正比。最坏情况下（树呈链状）是 `O(n)`，平均情况下（平衡二叉树）约为 `O(log n)`。

---

## 心得

- **核心技巧**：在递归/遍历过程中**携带额外的状态信息**（这里是父节点、祖父节点），可以把本来需要二次遍历的查询变成一次遍历完成。  
- **适用的题型**  
  1. “某节点满足父/祖父/子/兄弟关系的条件” —— 例如 *Sum of Nodes with Even-Valued Grandparent*、*Count Nodes With Even-Valued Grandparent*。  
  2. “在路径上满足某种约束的统计” —— 如 *Binary Tree Paths*、*Path Sum III*（需要在遍历时维护前缀和）。  
  3. “需要在遍历时知道前一次或前两次的状态” —— 如 *Maximum Length of Repeated Subarray*（滑动窗口）、*Longest Consecutive Sequence in Binary Tree*（记录父节点值）。  
- **一句话总结解题钥匙**：**把“上一次/上上一次”的信息随遍历一起传递，避免重复搜索**。

---

## 反思

- **第一反应**：看到“祖父”这个关键词，我第一时间想到“每次都去找祖父”。于是想到两层遍历的暴力实现。  
- **最容易踩的坑**  
  1. **空指针**：根节点没有父亲和祖父，需要在代码里做好 `None` 判断。  
  2. **递归参数传递错误**：父亲和祖父的顺序一定要对应好，写反了会导致判断错误。  
  3. **整数溢出**：在 Python 中不存在，但在某些语言需要注意累计和的范围。  
- **下次遇到同类题**：第一步先**思考是否可以在一次遍历中把需要的“前置信息”带进去**，如果可以，就直接用递归/栈保存这些信息；如果不行，再考虑额外的数据结构（哈希表、前缀和等）来实现。