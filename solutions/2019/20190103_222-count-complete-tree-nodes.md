# #222. 计算完全二叉树的节点数 / Count Complete Tree Nodes

> 难度：简单 · 标签：Binary Search、Bit Manipulation、Tree、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/count-complete-tree-nodes/)

---

## 题目（英文原版）

**Description**

Given the root of a complete binary tree, return the number of the nodes in the tree.
According to Wikipedia, every level, except possibly the last, is completely filled in a complete binary tree, and all nodes in the last level are as far left as possible. It can have between 1 and 2h nodes inclusive at the last level h.
Design an algorithm that runs in less than O(n) time complexity.

**Examples**

**Example 1:**

```
Input: root = [1,2,3,4,5,6]
Output: 6
```

**Example 2:**

```
Input: root = []
Output: 0
```

**Example 3:**

```
Input: root = [1]
Output: 1
```

**Constraints**

- The number of nodes in the tree is in the range [0, 5 * 104].
- 0 <= Node.val <= 5 * 104
- The tree is guaranteed to be complete.

---

## 题目（中文翻译）

**描述**  
给定一棵完全二叉树（complete binary tree）的根节点 `root`，返回该树中的节点总数。

根据维基百科的定义，完全二叉树（complete binary tree）除最后一层外，每一层都被完全填满，且最后一层的所有节点都尽可能靠左。最后一层的节点数可以在 `1` 到 `2^h`（含）之间，其中 `h` 为最后一层的层数。

设计一个时间复杂度低于 `O(n)` 的算法。

**示例 1**  
**示例 2**  
**示例 3**  

**示例**  
- 示例 1:  
  ```text
  Input: root = [1,2,3,4,5,6]
  Output: 6
  ```

- 示例 2:  
  ```text
  Input: root = []
  Output: 0
  ```

- 示例 3:  
  ```text
  Input: root = [1]
  Output: 1
  ```

**约束条件**  
- 树中节点的数量范围为 `[0, 5 * 10^4]`。  
- `0 <= Node.val <= 5 * 10^4`。  
- 该树必定是完全二叉树（complete binary tree）。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把整棵树遍历一遍，遇到一个节点就计数，最后得到的计数就是答案。  
- **遍历方式**：可以用深度优先搜索（DFS）或广度优先搜索（BFS）。这里用递归的 DFS，递归的本质相当于“把树的每个分支都走一遍”。  
- **数据结构类比**：递归调用栈就像一本“记事本”，每进一层就往记事本里写下当前节点的地址，回到上层时再把这页擦掉。  

因为我们把每个节点都访问了一次，所以肯定能得到正确的节点总数。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点保存的数值
        self.left = left        # 左子树
        self.right = right      # 右子树

def countNodes_brute(root: TreeNode) -> int:
    """
    暴力递归遍历整棵树，统计节点数
    """
    if root is None:               # 空树直接返回 0
        return 0
    # 统计左子树的节点 + 右子树的节点 + 当前根节点
    left_cnt = countNodes_brute(root.left)   # 递归左子树
    right_cnt = countNodes_brute(root.right) # 递归右子树
    return 1 + left_cnt + right_cnt           # 1 表示当前根节点本身
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 这里的 `n` 是树中节点的个数。我们会 **一次** 访问每个节点，访问一次的代价是常数时间，所以总时间是 `n` 次常数操作。  
  - 用大白话说，就是“和节点数量成正比”，如果树有 1 万个节点，就要跑 1 万次。

- **空间复杂度**：`O(h)`（递归栈的深度）  
  - `h` 是树的高度。最坏情况下（完全二叉树）`h ≈ log₂ n`，所以额外的空间大约是 `log n`，这比 `n` 小很多。  
  - 可以把它想象成“在记事本里最多只能写这么多页”，每层递归占一页。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **“把每个节点都遍历一遍”**，这在节点很多（上限 5×10⁴）时仍然是 `O(n)`，但题目要求 **“低于 O(n)”**。  
完整二叉树的特性可以帮助我们跳过大量不必要的访问：

1. **完全二叉树的定义**  
   - 除了最后一层，每层都是满的。  
   - 最后一层的节点一定靠左排列。  

2. **利用高度快速判断子树是否满**  
   - 对于任意节点 `root`，计算左子树的左边界到底的高度 `left_depth`，以及右子树的右边界到底的高度 `right_depth`。  
   - 如果 `left_depth == right_depth`，说明左子树是一棵满二叉树（因为左子树的最左路径和最右路径一样长），节点数可以直接用公式 `2^depth - 1` 计算，**不需要递归遍历左子树**。  
   - 否则，左子树不是满的，右子树一定是满的（因为最后一层节点左对齐），这时我们递归左子树，同时右子树直接用公式计算。

3. **核心公式**  
   - 满二叉树的节点数 = `2^depth - 1`（深度从 1 开始计数）。  
   - 这里的 `2^depth` 可以用左移 `1 << depth` 实现，计算速度更快。

4. **类比**  
   - 想象一座楼，每层的房间数都是前一层的两倍。如果我们知道某层已经“整层满”，就不必逐个检查每个房间，只要算出这层的总房间数即可。

5. **算法步骤**  
   - 递归函数 `count(root)`  
     1. 若 `root` 为 `None` → 返回 0。  
     2. 计算左子树最左路径深度 `left_depth`，右子树最右路径深度 `right_depth`。  
     3. 若两者相等 → 左子树满，返回 ` (1 << left_depth) + count(root.right) `  
        - `1 << left_depth` 等价于 `2^left_depth`，即左子树节点数 + 根节点。  
     4. 否则 → 右子树满，返回 ` (1 << right_depth) + count(root.left) `  

这样我们每次都能 **把一整棵满子树的节点数一次性算出来**，只对“最后可能不满的那条路径”继续递归，递归深度最多是树的高度 `log n`，所以整体时间是 `O(log² n)`（每层都要走一次高度计算，复杂度为 `log n * log n`）。

#### 代码（Python）

```python
def countNodes(root: TreeNode) -> int:
    """
    利用完全二叉树的特性，递归地在 O(log^2 n) 时间内统计节点数
    """
    if root is None:               # 空树直接返回 0
        return 0

    # ---------- 计算左子树最左路径的深度 ----------
    def left_depth(node: TreeNode) -> int:
        d = 0
        while node:
            d += 1                # 每走到下一层，深度加 1
            node = node.left      # 一直往左走到底
        return d

    # ---------- 计算右子树最右路径的深度 ----------
    def right_depth(node: TreeNode) -> int:
        d = 0
        while node:
            d += 1
            node = node.right     # 一直往右走到底
        return d

    left_h = left_depth(root)      # 左子树的左边界深度
    right_h = right_depth(root)    # 右子树的右边界深度

    if left_h == right_h:
        # 整棵树是满的：节点数 = 2^depth - 1，根节点已经算在内
        # 这里用左移代替 2**left_h，效率更高
        return (1 << left_h) - 1
    else:
        # 左子树不满，右子树一定是满的
        # 右子树节点数 = 2^right_h - 1
        # 再递归统计左子树的实际节点数
        return (1 << right_h) - 1 + countNodes(root.left)
```

> **小技巧**：如果不想每次都写两个 `while`，可以把求深度的过程抽成一个函数 `getDepth(node, go_left)`，`go_left=True` 表示左走，`False` 表示右走，代码更简洁。

#### 复杂度  

- **时间复杂度**：`O(log² n)`  
  - 每层递归都要走一次左/右到底的路径来计算深度，这条路径长度是树的高度 `log n`。递归的层数同样是 `log n`（因为每次把高度减半），于是总体是 `log n * log n`。  
  - 用大白话说，就是“先找一次楼层高度（最多 16 步），再把高度再找一次（再最多 16 步），总共大约 256 步，即使有几万节点也几乎感受不到”。  

- **空间复杂度**：`O(log n)`（递归栈）  
  - 递归最多进行 `log n` 次，每次占用一次栈帧。相当于“记事本最多只需要写这么多页”，远小于遍历全部节点时的 `O(n)`。

---

## 心得

- **核心技巧**：利用完全二叉树的“满子树”特性，通过左/右深度比较一次性算出满子树的节点数。  
- **适用的题型**：  
  1. “计数完全二叉树节点” （本题）  
  2. “在完全二叉树中查找第 k 小/大元素” （可用相同的二分思路）  
  3. “判断完全二叉树的高度或是否满树” （同样利用左右深度）  
- **一句话总结**：**把“整层满”当成“可以直接用公式算”，只在“不满的那条路径”上递归**。

---

## 反思

- **第一反应**：直接用遍历计数——最自然但不满足 “低于 O(n)” 的要求。  
- **最容易踩的坑**：  
  - 忘记把根节点算进满树的公式中（`2^depth - 1` 已经包含根）。  
  - 在递归时把左/右子树的满树节点数写反，导致重复计数或遗漏。  
  - 计算深度时忘记 `while node:` 的循环条件，导致空指针错误。  
- **下次遇到同类题的第一步**：先问自己“这棵树是不是**完全**或**满**的？如果是，能否用**高度公式**一次算出节点数？” 再决定是否需要二分或递归细化。