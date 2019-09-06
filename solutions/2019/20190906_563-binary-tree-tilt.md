# #563. 二叉树倾斜度 / Binary Tree Tilt

> 难度：简单 · 标签：Tree、Depth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/binary-tree-tilt/)

---

## 题目（英文原版）

**Description**

Given the root of a binary tree, return the sum of every tree node's tilt.
The tilt of a tree node is the absolute difference between the sum of all left subtree node values and all right subtree node values. If a node does not have a left child, then the sum of the left subtree node values is treated as 0. The rule is similar if the node does not have a right child.

**Examples**

**Example 1:**

```
Input: root = [1,2,3]
Output: 1
Explanation: 
Tilt of node 2 : |0-0| = 0 (no children)
Tilt of node 3 : |0-0| = 0 (no children)
Tilt of node 1 : |2-3| = 1 (left subtree is just left child, so sum is 2; right subtree is just right child, so sum is 3)
Sum of every tilt : 0 + 0 + 1 = 1
```

**Example 2:**

```
Input: root = [4,2,9,3,5,null,7]
Output: 15
Explanation: 
Tilt of node 3 : |0-0| = 0 (no children)
Tilt of node 5 : |0-0| = 0 (no children)
Tilt of node 7 : |0-0| = 0 (no children)
Tilt of node 2 : |3-5| = 2 (left subtree is just left child, so sum is 3; right subtree is just right child, so sum is 5)
Tilt of node 9 : |0-7| = 7 (no left child, so sum is 0; right subtree is just right child, so sum is 7)
Tilt of node 4 : |(3+5+2)-(9+7)| = |10-16| = 6 (left subtree values are 3, 5, and 2, which sums to 10; right subtree values are 9 and 7, which sums to 16)
Sum of every tilt : 0 + 0 + 0 + 2 + 7 + 6 = 15
```

**Example 3:**

```
Input: root = [21,7,14,1,1,2,2,3,3]
Output: 9
```

**Constraints**

- The number of nodes in the tree is in the range [0, 104].
- -1000 <= Node.val <= 1000

---

## 题目（中文翻译）

给定一棵二叉树的根节点 `root`，返回所有树节点倾斜度的总和。  
节点的倾斜度是其左子树（left subtree）节点值之和与右子树（right subtree）节点值之和的绝对差。如果节点没有左子节点，则左子树的节点值之和视为 `0`；没有右子节点时右子树同理。

**示例 1:**  
**示例 2:**  
**示例 3:**  

**约束条件**  
- 树中节点的数量在 `[0, 10^4]` 范围内。  
- `-1000 <= Node.val <= 1000`

---

### 示例

#### 示例 1
**输入:** `root = [1,2,3]`  
**输出:** `1`  
**解释:**  
- 节点 `2` 的倾斜度: `|0-0| = 0`（无子节点）  
- 节点 `3` 的倾斜度: `|0-0| = 0`（无子节点）  
- 节点 `1` 的倾斜度: `|2-3| = 1`（左子树只有左子节点，和为 `2`；右子树只有右子节点，和为 `3`）  
- 所有倾斜度之和: `0 + 0 + 1 = 1`

#### 示例 2
**输入:** `root = [4,2,9,3,5,null,7]`  
**输出:** `15`  
**解释:**  
- 节点 `3` 的倾斜度: `|0-0| = 0`（无子节点）  
- 节点 `5` 的倾斜度: `|0-0| = 0`（无子节点）  
- 节点 `7` 的倾斜度: `|0-0| = 0`（无子节点）  
- 节点 `2` 的倾斜度: `|3-5| = 2`（左子树只有左子节点，和为 `3`；右子树只有右子节点，和为 `5`）  
- 节点 `9` 的倾斜度: `|0-7| = 7`（无左子节点，左子树和为 `0`；右子树只有右子节点，和为 `7`）  
- 节点 `4` 的倾斜度: `|(3+5+2)-(9+7)| = |10-16| = 6`（左子树节点值为 `3, 5, 2`，和为 `10`；右子树节点值为 `9, 7`，和为 `16`）  
- 所有倾斜度之和: `0 + 0 + 0 + 2 + 7 + 6 = 15`

#### 示例 3
**输入:** `root = [21,7,14,1,1,2,2,3,3]`  
**输出:** `9`  
**解释:**（略）

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**对树中的每一个节点，都求出它左子树的所有节点值之和、右子树的所有节点值之和，然后算绝对差**，把所有节点的差累加起来就是答案。

- **用到的数据结构**  
  - 二叉树的 `TreeNode`（每个节点保存 `val、left、right`）。可以把它想象成家谱树，`left`、`right` 分别是“左孩子”“右孩子”。  
  - “子树的和值”需要遍历整棵子树，这类似于在字典里查找一个词的所有解释，需要把所有解释（节点值）逐一累加。  

- **为什么正确**  
  题目要求的倾斜度（tilt）正是左子树和值与右子树和值的绝对差。只要我们把每个节点的左、右子树分别遍历一遍并把值相加，就能得到准确的倾斜度，最后把所有倾斜度相加即可。

- **时间/空间复杂度**  
  - 对每个节点我们都要**再遍历一次它的左子树和右子树**，这相当于在树上做了两层循环（外层遍历所有节点，内层遍历子树）。最坏情况下（树是链状）时间复杂度是 **O(n²)**，即“平方级”。如果把 n=10000，时间大约是 10000×10000=1 亿次操作，显得有点慢。  
  - 递归栈的深度最多等于树的高度，最坏是 O(n)。除此之外我们只用到常数级的额外空间，所以空间复杂度是 **O(n)**（递归栈）。


#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的数值
        self.left = left        # 左子树
        self.right = right      # 右子树

def subtree_sum(node: TreeNode) -> int:
    """
    递归求整棵子树的节点值之和。
    如果 node 为 None，返回 0（相当于空子树的和值）。
    """
    if not node:
        return 0
    # 左子树和 + 右子树和 + 当前节点值
    return subtree_sum(node.left) + subtree_sum(node.right) + node.val

def findTilt(root: TreeNode) -> int:
    """
    暴力版：对每个节点分别计算左右子树的和值，再求倾斜度并累计。
    """
    if not root:
        return 0

    # 计算当前节点的倾斜度
    left = subtree_sum(root.left)    # 左子树的和值
    right = subtree_sum(root.right)  # 右子树的和值
    tilt = abs(left - right)          # 当前节点的倾斜度

    # 递归处理左、右子树，累加它们的倾斜度
    return tilt + findTilt(root.left) + findTilt(root.right)
```

#### 复杂度

- **时间复杂度：O(n²)**  
  对每个节点都要遍历一次它的子树，等价于“对每对节点都可能会被访问一次”。  
- **空间复杂度：O(n)**  
  递归调用栈的最大深度等于树的高度，最坏情况下是 n（链状树）。除此之外只用了常数级变量。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于我们对同一棵子树的和值做了重复计算**。例如，计算根节点左子树的和值时，实际上已经遍历了一遍左子树；随后在递归到左子树的根节点时，又要再次遍历它的子树，造成大量冗余。

**关键优化思路**：**一次遍历同时返回两个信息**  
1. 这棵子树的所有节点值之和（供父节点使用）。  
2. 这棵子树内部所有节点的倾斜度之和（累计到全局答案）。

这正好符合 **后序遍历（post‑order）** 的特点：先处理左子树、再处理右子树，最后处理当前节点。这样在回到当前节点时，左、右子树的和值已经算好，直接用它们求倾斜度即可，无需再次遍历。

**核心算法/数据结构**  
- **深度优先搜索（DFS）**：递归实现后序遍历。递归函数返回子树的和值，同时把倾斜度累加到外部变量 `total_tilt`。  
- **全局/非局部变量**：用一个整数 `total_tilt` 保存所有节点的倾斜度之和，递归结束后直接返回。

**类比**：把树看成一棵“账本”。每个节点是一本账，左子树、右子树是它的两个子账本。我们一次性把子账本的总额算出来，交给父账本使用；同时把每本账的“差额”（倾斜度）记下来，最后把所有差额加起来就是答案。

#### 代码（Python）

```python
# Definition for a binary tree node (同上)
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def findTilt(root: TreeNode) -> int:
    """
    最优解：一次后序遍历同时求子树和值和累计倾斜度。
    """
    total_tilt = 0                     # 用来累计所有节点的倾斜度

    def postorder(node: TreeNode) -> int:
        """
        返回值：以 node 为根的子树所有节点值之和。
        副作用：把该子树内部所有节点的倾斜度累加到 total_tilt。
        """
        nonlocal total_tilt           # 让内部函数可以修改外层的 total_tilt
        if not node:
            return 0                  # 空子树的和值为 0

        # 递归得到左、右子树的和值
        left_sum = postorder(node.left)
        right_sum = postorder(node.right)

        # 当前节点的倾斜度 = |左子树和值 - 右子树和值|
        node_tilt = abs(left_sum - right_sum)
        total_tilt += node_tilt       # 累计到全局答案

        # 返回以当前节点为根的子树的总和值（供父节点使用）
        return left_sum + right_sum + node.val

    postorder(root)                   # 从根节点开始遍历
    return total_tilt
```

#### 复杂度

- **时间复杂度：O(n)**  
  每个节点只被访问一次（一次后序遍历），所以时间随节点数线性增长。相当于“把 n=10000 的树只遍历一次，就能得到答案”。  
- **空间复杂度：O(h)**  
  递归栈的深度等于树的高度 `h`。在最坏情况下（链状树）`h = n`，所以最坏是 O(n)；在平衡树中 `h ≈ log n`，空间更少。这里的空间指的是函数调用栈，而不是额外的数组或字典。

---

## 心得

- **核心技巧**：后序遍历 + 递归返回子树累计值。  
- **适用的题型**  
  1. **子树求和类**（如 LeetCode 1025 “Divisor Game” 中需要子树信息的变形）。  
  2. **需要父节点依赖子节点信息的题目**（如 337 “House Robber III”、563 “Binary Tree Tilt”）。  
  3. **求子树最大/最小/路径和**（如 124 “Binary Tree Maximum Path Sum”）。  
- **一句话总结**：**一次后序遍历即可同时得到子树和值和累计倾斜度，避免重复计算**。

---

## 反思

- **第一反应**：看到“左子树和值”和“右子树和值”，马上想到要遍历两遍——先算子树和值，再算倾斜度。  
- **最容易踩的坑**  
  - **空子树的处理**：没有左/右孩子时要记得返回 0，否则会出现 `None` 报错或错误的差值。  
  - **全局累计**：如果在递归里每次都返回倾斜度的和，容易混淆子树的和值与倾斜度的累计，需要明确区分返回值的意义。  
  - **递归深度**：极端不平衡树会导致递归层数很深，Python 递归深度默认 1000，若节点数超过 10⁴ 可能会触发 `RecursionError`。在实际面试中可以把递归改写为显式栈的迭代版，或在代码开头加 `sys.setrecursionlimit(20000)`（仅在受限环境下使用）。  
- **下次遇到同类题**：**先想后序遍历能否一次完成所有需要的子树信息**，如果可以，就直接写递归返回“子树状态 + 累计答案”。这往往是最简洁且最优的思路。