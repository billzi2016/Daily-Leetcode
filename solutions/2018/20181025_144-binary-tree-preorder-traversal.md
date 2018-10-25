# #144. 二叉树的前序遍历 / Binary Tree Preorder Traversal

> 难度：简单 · 标签：Stack、Tree、Depth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/binary-tree-preorder-traversal/)

---

## 题目（英文原版）

**Description**

Given the root of a binary tree, return the preorder traversal of its nodes' values.
Follow up: Recursive solution is trivial, could you do it iteratively?

**Examples**

**Example 1:**

```
Input: root = [1,null,2,3]
Output: [1,2,3]
Explanation:
```

**Example 2:**

```
Input: root = [1,2,3,4,5,null,8,null,null,6,7,9]
Output: [1,2,4,5,6,7,3,8,9]
Explanation:
```

**Example 3:**

```
Input: root = []
Output: []
```

**Example 4:**

```
Input: root = [1]
Output: [1]
```

**Constraints**

- The number of nodes in the tree is in the range [0, 100].
- -100 <= Node.val <= 100

---

## 题目（中文翻译）

给定一棵二叉树（binary tree）的根节点 `root`，返回其节点值的先序遍历（preorder traversal）结果。

**示例 1**  
输入: `root = [1,null,2,3]`  
输出: `[1,2,3]`  
解释：

**示例 2**  
输入: `root = [1,2,3,4,5,null,8,null,null,6,7,9]`  
输出: `[1,2,4,5,6,7,3,8,9]`  
解释：

**示例 3**  
输入: `root = []`  
输出: `[]`  
解释：

**示例 4**  
输入: `root = [1]`  
输出: `[1]`  
解释：

**约束条件**  
- 树中节点的数量在 `[0, 100]` 区间内。  
- `-100 <= Node.val <= 100`

**进阶**  
递归解法很容易实现，能否使用迭代（iteratively）方式完成？

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

二叉树的**先序遍历**的顺序是：  
1）先访问根节点  
2）再遍历左子树（仍然按照先序）  
3）最后遍历右子树（仍然按照先序）  

最直接的办法就是**递归**：把“先序遍历”这件事交给函数自己去完成。  
递归的过程可以想象成**把树的每一个子树拆成更小的子树**，一直拆到空树为止，然后把访问顺序记录下来。

- **用到的数据结构**：  
  - `list`（Python 中的数组）用来保存遍历得到的节点值。  
  - 递归调用本身会隐式使用**调用栈**，就像在查字典时不断往下翻页，翻到最底层再逐层返回。

- **为什么正确**：  
  对于任意节点 `node`，递归函数先把 `node.val` 加入结果，然后递归处理 `node.left`，再递归处理 `node.right`。这正好满足先序遍历的定义，所以最终得到的序列一定是正确的。

- **时间/空间复杂度**：  
  - **时间**：每个节点恰好被访问一次，花费的时间与节点数 `n` 成正比，记作 **O(n)**。  
    用大白话说，就是如果树有 100 个节点，就要跑 100 步；如果有 1,000,000 个节点，就要跑 1,000,000 步。  
  - **空间**：递归需要保存调用栈，最坏情况下（比如一条全左的链）栈的深度等于节点数 `n`，所以空间复杂度也是 **O(n)**。如果树是平衡的，栈深度大约是 `log n`，但我们只说最坏情况。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的值
        self.left = left        # 左子树
        self.right = right      # 右子树

class Solution:
    def preorderTraversal(self, root: TreeNode) -> list[int]:
        """
        递归实现二叉树的先序遍历
        """
        result = []                     # 用来存放遍历顺序

        def dfs(node: TreeNode):
            if not node:                # 空节点直接返回
                return
            result.append(node.val)    # 1. 先访问根节点
            dfs(node.left)              # 2. 再遍历左子树
            dfs(node.right)             # 3. 最后遍历右子树

        dfs(root)                       # 从根节点开始递归
        return result
```

#### 复杂度

- **时间复杂度**：O(n) — 需要访问每个节点一次，n 越大，花的时间线性增长。  
- **空间复杂度**：O(n) — 递归栈最深可能等于节点数（极端情况是链状树），所以最坏需要 n 个栈帧。

---

### 2. 最优解

#### 思路  

递归写起来很简洁，但它隐式使用了系统调用栈。如果面试官要求**“请用迭代方式实现”**，我们需要自己维护一个栈来模拟递归的过程。

**慢的地方**：递归每次都会进入函数调用，系统要帮我们保存局部变量，这会有一定的开销；而且在一些语言里递归深度受限（Python 默认递归深度约 1000），对大树会炸掉。

**优化思路**：  
1. **显式栈**：我们手动创建一个 Python 列表 `stack`，把根节点压进去。  
2. **循环**：只要栈不空，就弹出栈顶节点 `node`，把 `node.val` 加入结果。  
3. **压入子节点**：因为栈是 **后进先出**（LIFO），我们希望左子树先被处理，所以**先把右子节点压栈，再把左子节点压栈**。这样左子节点会在下一次循环最先被弹出，顺序正好符合先序遍历。

**核心概念——栈**：可以把栈想象成**一本翻页的书**，每次只能在最上面那一页（栈顶）做操作。我们把“以后要处理的节点”暂时放在书的后面，等到前面的都处理完再往后翻。

#### 代码（Python）

```python
class Solution:
    def preorderTraversal(self, root: TreeNode) -> list[int]:
        """
        迭代实现二叉树的先序遍历
        使用显式栈来模拟递归过程
        """
        if not root:                     # 空树直接返回空列表
            return []

        stack = [root]                   # 初始化栈，先把根节点压进去
        result = []                      # 保存遍历顺序

        while stack:                     # 栈不为空就一直循环
            node = stack.pop()           # 弹出栈顶节点（最近压进去的）
            result.append(node.val)      # 先访问根节点

            # 先压右子树，再压左子树，保证左子树先被处理
            if node.right:               # 右子节点非空才压栈
                stack.append(node.right)
            if node.left:                # 左子节点非空才压栈
                stack.append(node.left)

        return result
```

#### 复杂度

- **时间复杂度**：O(n) — 每个节点恰好被压栈一次、弹栈一次，仍然是线性时间。相比递归，少了函数调用的开销。  
- **空间复杂度**：O(n) — 最坏情况下栈里会同时保存树的所有节点（比如全部左子树的情况），所以仍是线性空间。不过这里的空间是我们自己显式分配的，而不是系统调用栈。

---

## 心得

- **核心技巧**：利用**显式栈**把递归过程手动展开，掌握 **先入后出** 的顺序控制。  
- **适用的题型**：  
  1. 二叉树的中序遍历、后序遍历（同样可以用栈实现）  
  2. 图的深度优先搜索（DFS）  
  3. “括号匹配”或“单调栈”这类需要 **后进先出** 的问题  
- **一句话总结**：先序遍历 = “先根、左、右”，用栈把“右后左前”压进去，左子树自然先出来。

---

## 反思

- **第一反应**：直接写递归，因为递归和先序遍历的定义一一对应，最省事。  
- **最容易踩的坑**：  
  - 忘记先压右子树再压左子树，导致遍历顺序变成根、右、左（错误的先序）。  
  - 对空树或单节点树没有做好边界判断，直接 `pop` 会报错。  
- **下次遇到同类题**：第一步先问自己“这道遍历/搜索的顺序是什么？”然后决定是用递归还是**显式栈**来模拟，若面试官要求迭代，就立刻把递归的“先根、左、右”转化为“栈 → 先右后左”。