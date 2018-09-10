# #98. 验证二叉搜索树 / Validate Binary Search Tree

> 难度：中等 · 标签：Tree、Depth-First Search、Binary Search Tree、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/validate-binary-search-tree/)

---

## 题目（英文原版）

**Description**

Given the root of a binary tree, determine if it is a valid binary search tree (BST).
A valid BST is defined as follows:

**Examples**

**Example 1:**

```
Input: root = [2,1,3]
Output: true
```

**Example 2:**

```
Input: root = [5,1,4,null,null,3,6]
Output: false
Explanation: The root node's value is 5 but its right child's value is 4.
```

**Constraints**

- The number of nodes in the tree is in the range [1, 104].
- -231 <= Node.val <= 231 - 1

---

## 题目（中文翻译）

给定一棵二叉树（binary tree）的根节点（root），判断它是否是一棵有效的二叉搜索树（binary search tree，BST）。  

有效的 BST 满足以下条件：  
- 对于任意节点（node），其左子树（left subtree）中的所有节点值均小于该节点的值。  
- 对于任意节点，其右子树（right subtree）中的所有节点值均大于该节点的值。  
- 左、右子树本身也必须分别是有效的 BST。  

示例  

示例 1:  
输入: `root = [2,1,3]`  
输出: `true`  

示例 2:  
输入: `root = [5,1,4,null,null,3,6]`  
输出: `false`  
解释: 根节点的值为 5，但其右子节点的值为 4。  

约束条件  
- 树中节点的数量在 `[1, 10^4]` 范围内。  
- `-2^31 <= Node.val <= 2^31 - 1`   (即 `-231 <= Node.val <= 231 - 1`)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直观的想法是：**每个节点都要检查它左子树的所有节点是否都小于它本身，右子树的所有节点是否都大于它本身**。  
可以把这件事想象成 **“把树的每一层都翻过去检查”**，就像我们在一本书里找某个词，要把前面的所有页码都检查一遍才敢确定它的顺序是否正确。

实现时：

1. 对每个节点 `node`，  
   - 在左子树里找到最大的值 `max_left`，要求 `max_left < node.val`。  
   - 在右子树里找到最小的值 `min_right`，要求 `min_right > node.val`。  
2. 对左、右子树递归执行同样的检查。

这样做是**一定正确**的，因为只要左子树里有任何一个值不小于根节点，或者右子树里有任何一个值不大于根节点，BST 的定义就被破坏了。

> **为什么能保证正确？**  
> BST 的定义要求 **所有** 左子树节点 < 根 < **所有** 右子树节点。我们逐个节点把左/右子树的极值（最大/最小）找出来并比较，等价于把“所有”条件压缩成了两个最关键的比较。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def isValidBST(root: TreeNode) -> bool:
    """暴力版：每个节点都遍历一次它的整棵子树"""
    if not root:
        return True

    # ---------- 辅助函数：在 subtree 中找最大值 ----------
    def get_max(node: TreeNode) -> int:
        if not node:
            return float("-inf")          # 空树的最大值设为负无穷
        return max(node.val, get_max(node.left), get_max(node.right))

    # ---------- 辅助函数：在 subtree 中找最小值 ----------
    def get_min(node: TreeNode) -> int:
        if not node:
            return float("inf")           # 空树的最小值设为正无穷
        return min(node.val, get_min(node.left), get_min(node.right))

    # 1️⃣ 检查左子树的最大值是否小于当前节点值
    if root.left:
        if get_max(root.left) >= root.val:
            return False

    # 2️⃣ 检查右子树的最小值是否大于当前节点值
    if root.right:
        if get_min(root.right) <= root.val:
            return False

    # 3️⃣ 递归检查左右子树自身是否满足 BST 条件
    return isValidBST(root.left) and isValidBST(root.right)
```

> 代码里每一行的中文注释已经解释了它的作用，直接复制到 IDE 中即可运行。

#### 复杂度

- **时间复杂度：** `O(n²)`  
  - 对每个节点（共 `n` 个），我们都要遍历它的左/右子树来找最大/最小值，最坏情况下每次遍历的节点数也是 `O(n)`，于是总时间是 `n × n`。  
  - 用大白话说，就是“把树的每一片叶子都检查了很多遍”，所以会慢。

- **空间复杂度：** `O(h)`，其中 `h` 是树的高度  
  - 递归调用栈的深度最多等于树的高度。最坏情况下（链状树）高度为 `n`，所以空间最坏为 `O(n)`；平均情况下是 `O(log n)`（平衡树）。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都要重新遍历子树**，导致大量重复工作。我们可以把“左子树全部小于根、右子树全部大于根”这件事**一次性传递**下来，而不是每次都去重新找极值。

**核心想法：**  
- 对每个节点，维护它能够取值的合法区间 `(low, high)`。  
- 初始时，根节点的合法区间是 `(-∞, +∞)`。  
- 当我们向左子树递归时，右边界收紧为 `parent.val`（左子树的所有值必须 < 父节点）。  
- 当我们向右子树递归时，左边界收紧为 `parent.val`（右子树的所有值必须 > 父节点）。  
- 只要当前节点的值落在 `(low, high)` 之间，就说明它没有违背任何祖先节点的限制。

可以把这个过程类比为 **“给每个孩子发放一张通行证”，** 通行证上写着它能出现的最小/最大数字范围。只要孩子拿着通行证进去，就一定不会闯红灯。

实现时，只需要一次深度优先遍历（前序/中序均可），在递归参数里携带 `low` 与 `high` 即可。这样每个节点只被访问一次，时间是 `O(n)`。

#### 代码（Python）

```python
def isValidBST(root: TreeNode) -> bool:
    """最优解：一次遍历，用区间限制每个节点的取值范围"""

    # ---------- 辅助递归函数 ----------
    def helper(node: TreeNode, low: float, high: float) -> bool:
        if not node:                     # 空树天然合法
            return True
        # ① 当前节点必须严格位于 (low, high) 之间
        if not (low < node.val < high):
            return False

        # ② 递归检查左子树：右边界收紧为 node.val
        left_is_valid = helper(node.left, low, node.val)
        # ③ 递归检查右子树：左边界收紧为 node.val
        right_is_valid = helper(node.right, node.val, high)

        return left_is_valid and right_is_valid

    # 从根节点开始，合法区间是 (-∞, +∞)
    return helper(root, float("-inf"), float("inf"))
```

> 这段代码只用了 **一次** 深度优先遍历，且每行都有中文注释，易于理解。

#### 复杂度

- **时间复杂度：** `O(n)`  
  - 每个节点恰好被访问一次，没有重复遍历。用大白话讲，就是“只走一遍树的每条路”，所以速度快。

- **空间复杂度：** `O(h)`（递归栈深度）  
  - 同样只需要保存递归调用的栈帧，最坏情况下是 `O(n)`（链状树），平衡时是 `O(log n)`。

---

## 心得

- **核心技巧**：**使用递归传递合法取值区间**（也叫“上下界法”）。  
- **适用的题型**  
  1. 验证 BST（本题）。  
  2. “在 BST 中搜索/插入/删除” 时需要维护区间。  
  3. “二叉树的最大/最小路径和” 这类需要把信息从父传给子的问题（只不过信息是和而不是区间）。  
- **一句话总结**：**只要把“所有祖先的约束”压缩成一个上下界，就能一次遍历搞定验证**。

---

## 反思

- **拿到题目第一反应**：先检查每个节点的左右孩子是否满足 BST 条件，随后想到要遍历子树求极值——这就是暴力思路。  
- **最容易踩的坑**  
  - 只比较直接左右子节点会漏掉更深层的违规情况（如左子树的右子孙大于根节点）。  
  - 递归传递区间时要记得使用 **严格** 的不等号 `<`，因为 BST 要求左子树全部 **小于** 根，右子树全部 **大于** 根，等于的情况是不合法的。  
  - 边界值使用 `float("-inf")` / `float("inf")` 防止整数溢出。  
- **下次遇到同类题**：第一步先思考“有没有全局约束可以一次性传递下来”，如果有，就立刻用 **上下界** 的递归模板；如果没有，再考虑暴力或其他辅助信息（如中序遍历是否有序）。