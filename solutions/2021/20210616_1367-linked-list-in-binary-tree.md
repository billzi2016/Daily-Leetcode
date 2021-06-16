# #1367. 二叉树中的链表 / Linked List in Binary Tree

> 难度：中等 · 标签：Linked List、Tree、Depth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/linked-list-in-binary-tree/)

---

## 题目（英文原版）

**Description**

Given a binary tree root and a linked list with head as the first node.
Return True if all the elements in the linked list starting from the head correspond to some downward path connected in the binary tree otherwise return False.
In this context downward path means a path that starts at some node and goes downwards.

**Examples**

**Example 1:**

```
Input: head = [4,2,8], root = [1,4,4,null,2,2,null,1,null,6,8,null,null,null,null,1,3]
Output: true
Explanation: Nodes in blue form a subpath in the binary Tree.
```

**Example 2:**

```
Input: head = [1,4,2,6], root = [1,4,4,null,2,2,null,1,null,6,8,null,null,null,null,1,3]
Output: true
```

**Example 3:**

```
Input: head = [1,4,2,6,8], root = [1,4,4,null,2,2,null,1,null,6,8,null,null,null,null,1,3]
Output: false
Explanation: There is no path in the binary tree that contains all the elements of the linked list from head.
```

**Constraints**

- The number of nodes in the tree will be in the range [1, 2500].
- The number of nodes in the list will be in the range [1, 100].
- 1 <= Node.val <= 100 for each node in the linked list and binary tree.

---

## 题目（中文翻译）

**描述**  
给定一棵二叉树（binary tree）`root` 和一个链表（linked list），其头节点为 `head`。如果链表中从头节点开始的所有元素对应于二叉树中某条**向下路径（downward path）**上的节点序列，则返回 `True`，否则返回 `False`。这里的向下路径指的是从某个节点出发、一直向子节点方向延伸的路径。

**示例**

示例 1  
Input: head = [4,2,8], root = [1,4,4,null,2,2,null,1,null,6,8,null,null,null,null,1,3]  
Output: true  
Explanation: 蓝色节点构成二叉树中的一个子路径，使其对应链表的顺序。

示例 2  
Input: head = [1,4,2,6], root = [1,4,4,null,2,2,null,1,null,6,8,null,null,null,null,1,3]  
Output: true  
Explanation: 链表的节点在二叉树中也能找到对应的向下路径。

示例 3  
Input: head = [1,4,2,6,8], root = [1,4,4,null,2,2,null,1,null,6,8,null,null,null,null,1,3]  
Output: false  
Explanation: 二叉树中不存在一条向下路径能够包含链表从头到尾的所有元素。

**约束条件**  
- 树中节点数在 `[1, 2500]` 区间内。  
- 链表中节点数在 `[1, 100]` 区间内。  
- 对于链表和二叉树中的每个节点，`1 <= Node.val <= 100`。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把二叉树的每一个节点都当作可能的起点**，从这个节点往下走，逐个比对链表的节点值。  
如果从某个起点开始，能够完整匹配链表的所有节点，就返回 `True`；遍历完所有起点仍未匹配成功，则返回 `False`。

- **数据结构**  
  - **链表**：顺序的、只能向后走的结构。这里我们把它看成“顺序的单词”，每个节点的 `val` 就像单词里的字母。  
  - **二叉树**：每个节点有左、右两个子节点，向下走的路径相当于“从树根向叶子走”。  

  类比：链表就像一本字典里要查的单词，二叉树的每条向下路径就像字典里的一行文字。我们要找的是“字典里是否出现了这整个单词”。  

- **为什么正确**  
  - 任意一条向下路径都是从某个节点开始、只向子节点前进的序列。遍历所有节点作为起点，就覆盖了所有可能的路径。  
  - 对每条路径逐个比较，只有全部相等时才算匹配成功，符合题目“对应某条向下路径”的要求。

- **时间/空间复杂度**  
  - **时间**：设二叉树有 `N` 个节点，链表长度为 `M`。我们要对每个树节点尝试一次匹配，匹配过程最多遍历 `M` 个链表节点（因为匹配失败后会立刻停止）。最坏情况是每次都要走完 `M` 步，所以总共是 `N × M` 次比较，记作 **O(N·M)**。  
    - 大白话：如果树有 2500 个节点，链表长 100，最多会检查 2500×100=250 000 次，仍在可接受范围。  
  - **空间**：递归调用的深度最多是链表长度 `M`（因为匹配时只能沿着树向下走，深度受链表限制），再加上递归遍历树本身的深度 `O(H)`（`H` ≤ `N`）。在最坏情况下（链表很长且树呈链状），空间是 **O(M)**，因为我们在匹配时的递归深度受链表控制。其余使用的变量都是常数级。

#### 代码（Python）

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    # 主入口
    def isSubPath(self, head: ListNode, root: TreeNode) -> bool:
        # 1）遍历二叉树的每一个节点，尝试把它当作匹配的起点
        return self.dfs_tree(root, head)

    # 2）在二叉树中遍历所有节点
    def dfs_tree(self, node: TreeNode, head: ListNode) -> bool:
        if not node:                     # 树到头了，说明该分支不可能匹配
            return False
        # 只要有一次匹配成功，就返回 True
        return (self.dfs_match(node, head)          # 以当前节点为起点尝试匹配
                or self.dfs_tree(node.left, head)   # 左子树继续尝试
                or self.dfs_tree(node.right, head)) # 右子树继续尝试

    # 3）从某个树节点开始，逐个比较链表节点
    def dfs_match(self, node: TreeNode, head: ListNode) -> bool:
        if not head:                     # 链表已经全部匹配完，成功
            return True
        if not node:                     # 树已经走到叶子，链表还没完，失败
            return False
        if node.val != head.val:         # 当前值不相等，匹配失败
            return False
        # 当前值相等，继续向左或向右子节点尝试匹配下一个链表节点
        return (self.dfs_match(node.left, head.next) or
                self.dfs_match(node.right, head.next))
```

#### 复杂度  

- **时间复杂度**：**O(N·M)**  
  - `N` 为二叉树节点数，`M` 为链表长度。遍历每个树节点（`N` 次），每次最多比较 `M` 次链表节点。  
- **空间复杂度**：**O(M)**  
  - 递归栈深度受链表长度限制，最坏情况下是 `M`（链表全匹配时递归沿着树一路向下）。  

---

### 2. 最优解  

#### 思路  

在上面的暴力解里，我们已经把时间复杂度压到了 **O(N·M)**，这已经是题目给出的约束（`N ≤ 2500, M ≤ 100`）下的最优量级。  
仍然可以从“**哪里慢**”的角度说明优化思路，让读者更清楚为什么不需要再继续“更快”。  

**慢点**  
- 暴力解的两层递归（遍历树 + 匹配链表）看起来像是两层循环。  
- 但是每一次匹配的深度被链表长度 `M` 限制，无法再“剪枝”。  

**进一步思考**  
- 如果把链表视作一个模式串，二叉树的每条向下路径视作一段文本，经典的字符串匹配算法（如 KMP）可以在 **O(N+M)** 时间完成匹配。  
- 但二叉树不是线性结构，路径会分叉，直接套用 KMP 需要把所有路径展开成大量字符串，反而会导致 **O(N·H)**（`H` 为树高） 的额外开销，且实现复杂度大幅提升。  

**结论**  
- 对于本题的规模，**遍历每个节点并从该节点尝试匹配** 已经是最简洁、最易实现且时间足够的方案。  
- 因此我们把上面的实现直接称为“最优解”。  

> **核心技巧**：*在树上做 DFS，同时在链表上做递归匹配*。这是一种“**同步递归**”的思路：每走一步树，就走一步链表。

#### 代码（Python）

（与上面暴力解相同，只是把函数名和注释稍作整理，强调这是最优实现）

```python
class Solution:
    def isSubPath(self, head: ListNode, root: TreeNode) -> bool:
        """
        判断链表 head 是否是二叉树 root 中某条向下路径的子序列。
        """
        # 对每个树节点尝试匹配
        return self.search(root, head)

    def search(self, node: TreeNode, head: ListNode) -> bool:
        if not node:
            return False
        # 只要任意一种情况成功就返回 True
        return (self.match(node, head)          # 以当前节点为起点匹配
                or self.search(node.left, head) # 左子树继续尝试
                or self.search(node.right, head))

    def match(self, node: TreeNode, head: ListNode) -> bool:
        """
        从 tree 节点 node 开始，尝试把链表 head 完全匹配下来。
        """
        if not head:               # 链表已匹配完
            return True
        if not node:               # 树已经走到尽头
            return False
        if node.val != head.val:   # 当前值不同，匹配失败
            return False
        # 当前值相同，继续向左或向右匹配下一个链表节点
        return (self.match(node.left, head.next) or
                self.match(node.right, head.next))
```

#### 复杂度  

- **时间复杂度**：**O(N·M)**  
  - 与暴力解相同，但已经是最优的理论下界。  
  - 与最初的“暴力”对比：我们没有额外的重复计算，每一次递归都是必要的。  

- **空间复杂度**：**O(M)**  
  - 递归栈深度受链表长度限制。  

---

## 心得  

- **核心技巧**：在树上同步递归匹配链表（同步 DFS），即“在遍历树的同时逐步消耗链表”。  
- **适用的题型**  
  1. *链表是否是树/图中某条路径的子序列*（如本题）。  
  2. *在二叉树中寻找满足特定序列的路径*（例如“路径和等于给定值”可以用相似的同步递归思路）。  
  3. *在网格或图中匹配字符串*（LeetCode 79 Word Search 采用相同的 DFS+回溯框架）。  
- **一句话总结**：**把链表当作“指针”，在二叉树的每条向下路径上同步前进，匹配成功即为答案**。

## 反思  

- **第一反应**：看到“链表 + 向下路径”，马上想到“遍历每个树节点，然后尝试从这里开始匹配”。  
- **最容易踩的坑**  
  - 忘记在匹配过程中 **同时**检查左子树和右子树，导致只走单一路径而漏掉答案。  
  - 边界条件：链表为空时应直接返回 `True`（因为空序列总是子序列），实现时要在递归入口先判断 `if not head`.  
  - 树节点为 `None` 时仍继续递归会导致 `AttributeError`，一定要先 `if not node:` 返回 `False`。  
- **下次遇到同类题**：第一步先 **把链表（或字符串）视为模式串，树的每个节点视为可能的起点**，然后写出“**从起点同步匹配**”的递归函数。这样思路清晰，代码也容易写对。