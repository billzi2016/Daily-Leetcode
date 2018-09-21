# #110. **平衡二叉树** / Balanced Binary Tree

> 难度：简单 · 标签：Tree、Depth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/balanced-binary-tree/)

---

## 题目（英文原版）

**Description**

Given a binary tree, determine if it is height-balanced.

**Examples**

**Example 1:**

```
Input: root = [3,9,20,null,null,15,7]
Output: true
```

**Example 2:**

```
Input: root = [1,2,2,3,3,null,null,4,4]
Output: false
```

**Example 3:**

```
Input: root = []
Output: true
```

**Constraints**

- The number of nodes in the tree is in the range [0, 5000].
- -104 <= Node.val <= 104

---

## 题目（中文翻译）

给定一棵二叉树（binary tree），请判断该树是否是高度平衡（height‑balanced）的。

> **高度平衡的定义**：对于树中的每个节点，其左、右子树的高度差的绝对值不超过 1。

---

### 示例

**示例 1**  
**输入**：`root = [3,9,20,null,null,15,7]`  
**输出**：`true`

**示例 2**  
**输入**：`root = [1,2,2,3,3,null,null,4,4]`  
**输出**：`false`

**示例 3**  
**输入**：`root = []`  
**输出**：`true`

---

### 约束条件

- 树中节点的数量在 `[0, 5000]` 范围内。  
- 每个节点的取值满足 `-10^4 <= Node.val <= 10^4`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**对每个节点都去检查它的左右子树高度差是否 ≤ 1**。  
实现上可以把「求树的高度」写成一个递归函数 `height(node)`，它返回以 `node` 为根的子树的最大深度（根节点算 1 层，空树算 0 层）。  
然后对整棵树的每个节点：

1. 调用 `height(node.left)` 得到左子树的高度  
2. 调用 `height(node.right)` 得到右子树的高度  
3. 判断 `abs(left - right) <= 1`，如果不满足直接返回 `False`  
4. 递归检查左子树和右子树是否也都是平衡的  

> **类比**：求树的高度就像在楼房里数层数，从根层往下往每个子树递归数，空的地方算 0 层。

为什么能对？因为平衡二叉树的定义正是「每个节点的左右子树高度差不超过 1」且「左右子树本身也要平衡」。只要对每个节点都做一次检查，就能确保整棵树满足要求。

**时间/空间分析**  
- 对每个节点我们都要调用两次 `height`，而 `height` 本身会遍历整棵子树。于是根节点会遍历全部 `N` 个节点，左子树会再次遍历约 `N/2` 个节点，右子树同理……这导致**时间复杂度是 O(N²)**。  
- 递归调用栈的深度最多等于树的高度，最坏情况下（链状树）高度是 `N`，所以**空间复杂度是 O(N)**（递归栈占用）。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的数值
        self.left = left        # 左子树
        self.right = right      # 右子树

def height(node: TreeNode) -> int:
    """返回以 node 为根的子树的高度（空树高度为 0）"""
    if not node:
        return 0
    # 递归求左、右子树的高度，然后取较大值加一
    left_h = height(node.left)
    right_h = height(node.right)
    return max(left_h, right_h) + 1

def isBalanced(root: TreeNode) -> bool:
    """暴力检查整棵树是否平衡"""
    if not root:
        return True                     # 空树自然平衡

    left_h = height(root.left)          # 左子树高度
    right_h = height(root.right)        # 右子树高度

    # 当前节点高度差大于 1 则不平衡
    if abs(left_h - right_h) > 1:
        return False

    # 递归检查左右子树是否也平衡
    return isBalanced(root.left) and isBalanced(root.right)
```

#### 复杂度

- **时间复杂度：O(N²)**  
  “N²” 可以理解为「对每个节点（N 个）都要重新遍历一次它下面的所有节点（平均约 N/2），于是总工作量大约是 N × N/2 ≈ N²」。
- **空间复杂度：O(N)**  
  递归栈最深可能等于树的高度；在最坏的链状树里高度就是节点数 N。

---

### 2. 最优解

#### 思路  
从暴力解可以看到**瓶颈在于每次都要重新遍历子树求高度**，这导致大量重复计算。  
优化的关键是**一次遍历同时返回两件事**：

1. 这棵子树的高度  
2. 这棵子树是否已经是平衡的  

如果我们在后序遍历（左 → 右 → 根）的过程中，先得到左子树的高度和是否平衡，再得到右子树的同样信息，最后在根节点处只需要一次比较 `abs(left_h - right_h) ≤ 1` 并且检查左右子树本身是否平衡，就可以直接得出根节点子树的结果。这样每个节点只被访问一次，**时间降到 O(N)**。

**核心概念：后序遍历 + “信息合并”**  
- **后序遍历**：先处理子树，再处理当前节点，正好符合我们需要先知道子树高度的需求。  
- **信息合并**：返回一个二元组 `(is_balanced, height)`，相当于在每一步“把子树的两个属性打包带回去”。  

> **类比**：想象你在爬山，每到一个山口（节点）都要先把左边和右边的山路走完（左、右子树），再把两边的最高海拔和是否平稳的报告带回山口，最后决定整个山口的情况。

#### 代码（Python）

```python
def isBalanced(root: TreeNode) -> bool:
    """
    采用自底向上的后序遍历，只遍历一次即可判断是否平衡。
    返回值是一个布尔值，表示整棵树是否平衡。
    """
    def check(node: TreeNode):
        """
        辅助函数，返回 (is_balanced, height)。
        - is_balanced: 以 node 为根的子树是否平衡
        - height:      该子树的高度（空树高度为 0）
        """
        if not node:
            return True, 0          # 空树平衡，且高度为 0

        # 递归检查左子树
        left_balanced, left_h = check(node.left)
        # 递归检查右子树
        right_balanced, right_h = check(node.right)

        # 当前节点是否平衡取决于三件事：
        # 1. 左子树平衡
        # 2. 右子树平衡
        # 3. 左右子树高度差不超过 1
        balanced = (
            left_balanced and
            right_balanced and
            abs(left_h - right_h) <= 1
        )

        # 当前子树的高度 = 左右子树最高高度 + 1（加上当前节点）
        height = max(left_h, right_h) + 1

        return balanced, height

    # 只需要关心根节点返回的 is_balanced 部分
    result, _ = check(root)
    return result
```

#### 复杂度

- **时间复杂度：O(N)**  
  “O(N)” 可以理解为「每个节点只被访问一次」——我们只做一次后序遍历，所有信息在一次递归中完成合并。相比暴力解的「每个节点要再遍历它下面的所有节点」大幅提升。

- **空间复杂度：O(H)**（其中 H 为树的高度）  
  递归栈的深度等于树的高度。最坏情况下（链状树）高度为 N，空间为 O(N)；在平衡树里高度约为 `log₂N`，空间约为 O(log N)。这已经是最优的额外空间使用。

---

## 心得

- **核心技巧**：后序遍历时“一次返回多信息”，即 **自底向上** 的动态规划思想。  
- **适用的题型**  
  1. 判断二叉树是否满足某种全局性质（如 `是否为 BST`、`是否为完全二叉树`）  
  2. 需要在遍历过程中累计子树信息的题目（如 `求二叉树最大路径和`、`求二叉树直径`）  
- **解题钥匙**：**把“子树的状态 + 子树的结果”一次性返回，避免重复遍历**。

---

## 反思

- **第一反应**：直接写两个递归，一个算高度，一个检查平衡，结果是 O(N²)。  
- **最容易踩的坑**  
  - 忘记在空树（`None`）的情况下返回正确的高度 0，导致高度计算错误。  
  - 只检查根节点的高度差，而忽略了左右子树本身是否已经不平衡。  
- **下次遇到同类题**：第一步想到「能否在一次遍历中把需要的所有信息一次性收集回来？」如果可以，就尝试写一个返回多值的递归函数，实现自底向上的动态规划。