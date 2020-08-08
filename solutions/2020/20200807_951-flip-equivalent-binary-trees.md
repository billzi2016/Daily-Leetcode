# #951. 翻转等价二叉树 / Flip Equivalent Binary Trees

> 难度：中等 · 标签：Tree、Depth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/flip-equivalent-binary-trees/)

---

## 题目（英文原版）

**Description**

For a binary tree T, we can define a flip operation as follows: choose any node, and swap the left and right child subtrees.
A binary tree X is flip equivalent to a binary tree Y if and only if we can make X equal to Y after some number of flip operations.
Given the roots of two binary trees root1 and root2, return true if the two trees are flip equivalent or false otherwise.

**Examples**

**Example 1:**

```
Input: root1 = [1,2,3,4,5,6,null,null,null,7,8], root2 = [1,3,2,null,6,4,5,null,null,null,null,8,7]
Output: true
Explanation: We flipped at nodes with values 1, 3, and 5.
```

**Example 2:**

```
Input: root1 = [], root2 = []
Output: true
```

**Example 3:**

```
Input: root1 = [], root2 = [1]
Output: false
```

**Constraints**

- The number of nodes in each tree is in the range [0, 100].
- Each tree will have unique node values in the range [0, 99].

---

## 题目（中文翻译）

对于一棵二叉树 (binary tree) **T**，我们可以定义如下的翻转操作 (flip operation)：选择任意一个节点，并交换其左、右子树。  
如果存在若干次翻转操作，使得二叉树 **X** 可以变成二叉树 **Y**，则称 **X** 与 **Y** 为翻转等价 (flip equivalent)。  

给定两棵二叉树的根节点 `root1` 和 `root2`，如果这两棵树是翻转等价的返回 `true`，否则返回 `false`。  

---

### 示例

#### 示例 1
**输入**  
`root1 = [1,2,3,4,5,6,null,null,null,7,8]`  
`root2 = [1,3,2,null,6,4,5,null,null,null,null,8,7]`  

**输出**  
`true`  

**解释**  
我们在值为 1、3、5 的节点处分别执行了翻转操作。

#### 示例 2
**输入**  
`root1 = []`  
`root2 = []`  

**输出**  
`true`  

#### 示例 3
**输入**  
`root1 = []`  
`root2 = [1]`  

**输出**  
`false`  

---

### 约束条件

- 每棵树的节点数在区间 **[0, 100]** 内。  
- 每棵树的节点值唯一，且在区间 **[0, 99]** 内。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**把两棵树的每个节点都尝试翻转一次，然后逐层比较**。  
可以把树想象成一棵“家谱树”，每个节点有左孩子和右孩子。  
“翻转”相当于把左边的孩子和右边的孩子互换位置——就像把左手和右手的手套换一下。  

暴力做法的步骤：

1. 从根节点开始，同时遍历两棵树。  
2. 若当前两个节点的值不同，直接返回 `False`（不可能相等）。  
3. 否则，对**左子树**和**右子树**分别递归比较两棵树：  
   - **不翻转**的情况：`root1.left` 必须和 `root2.left` 相等，`root1.right` 必须和 `root2.right` 相等。  
   - **翻转**的情况：`root1.left` 必须和 `root2.right` 相等，`root1.right` 必须和 `root2.left` 相等。  
4. 只要有一种情况成立，就说明从这个节点开始可以通过若干次翻转得到相同结构。  

因为题目保证每个节点值唯一，比较节点值即可判断是否对应同一个节点。  

**为什么正确？**  
- 若两棵树在某个节点上不需要翻转，那么它们的左子树和右子树本来就对应相等，递归比较会返回 `True`。  
- 若需要翻转，只要把左、右子树互换后再递归比较，同样会返回 `True`。  
- 只要遍历到所有节点并检查这两种可能，必然覆盖所有合法的翻转组合，所以只要有一种组合使得两树相等，就会得到 `True`。  

**时间/空间复杂度（大白话）**  
- **时间**：每个节点最多会被比较两次（一次“不翻转”，一次“翻转”），所以整体是 **O(n)**，这里的 *n* 就是树的节点数。  
- **空间**：递归调用栈的深度最坏等于树的高度。最坏情况是链状树，深度为 *n*，所以空间是 **O(n)**。如果是平衡树，深度约为 `log n`，空间会更小。  

#### 代码（Python）  

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的数值
        self.left = left        # 左子树
        self.right = right      # 右子树

def flipEquiv(root1: TreeNode, root2: TreeNode) -> bool:
    """
    暴力递归：同时遍历两棵树，分别尝试“翻转”和“不翻转”两种情况。
    """
    # 1️⃣ 两棵树都为空 → 相等
    if not root1 and not root2:
        return True
    # 2️⃣ 只有一棵树为空 → 不相等
    if not root1 or not root2:
        return False
    # 3️⃣ 节点值不相同 → 不相等
    if root1.val != root2.val:
        return False

    # 4️⃣ 不翻转的情况：左左 + 右右
    no_flip = (flipEquiv(root1.left,  root2.left) and
               flipEquiv(root1.right, root2.right))

    # 5️⃣ 翻转的情况：左右互换 → 左右 + 右左
    flip = (flipEquiv(root1.left,  root2.right) and
            flipEquiv(root1.right, root2.left))

    # 只要有一种方式能匹配，就返回 True
    return no_flip or flip
```

#### 复杂度  

- **时间复杂度**：`O(n)` — 这里的 *n* 是两棵树中节点的总数。每个节点最多递归检查两次，仍然是线性级别。  
- **空间复杂度**：`O(h)` — *h* 为递归栈的深度，最坏情况下等于节点数 *n*（链状树），平衡树时约为 `log n`。  

---  

### 2. 最优解  

#### 思路  

从暴力解我们已经得到 **递归** 的框架：对每个节点，只需要判断两种对应关系（是否翻转）。  
事实上，这已经是**最优**的时间复杂度 `O(n)`，因为我们必须至少访问每个节点一次才能判断它们是否相同。  
下面的“最优解”主要是**代码层面的优化**和**思路的梳理**，帮助初学者更清晰地理解：

1. **提前剪枝**  
   - 当两个节点值不相等时，立刻返回 `False`，无需继续递归。  
   - 当两棵树的结构已经确定相同（不需要翻转）时，直接递归左、右子树，避免不必要的“翻转”递归。  

2. **使用** `or` **短路特性**  
   - Python 中 `a or b` 会先求 `a`，若 `a` 为 `True` 则直接返回 `True`，不再计算 `b`。这可以在 **不翻转** 成功时省掉 **翻转** 的递归调用。  

3. **递归改成迭代（可选）**  
   - 若担心递归栈太深（虽然本题节点数 ≤ 100，递归完全安全），可以用 **栈** 手动模拟深度优先遍历。  
   - 这里仍然保留递归写法，因为更易于阅读。  

核心概念仍然是 **深度优先搜索（DFS）**：从根往下检查每个子树，递归的本质就是 DFS。  

#### 代码（Python）  

```python
def flipEquiv(root1: TreeNode, root2: TreeNode) -> bool:
    """
    最优写法：在递归时尽量利用短路和提前返回，保持 O(n) 时间、O(h) 空间。
    """
    # 两棵树都空 → 相等
    if not root1 and not root2:
        return True
    # 只要有一棵为空 → 不相等
    if not root1 or not root2:
        return False
    # 节点值不同 → 不相等
    if root1.val != root2.val:
        return False

    # 先检查不翻转的情况；如果成功直接返回 True（利用 or 的短路）
    if (flipEquiv(root1.left, root2.left) and
        flipEquiv(root1.right, root2.right)):
        return True

    # 再检查翻转的情况
    return (flipEquiv(root1.left, root2.right) and
            flipEquiv(root1.right, root2.left))
```

#### 复杂度  

- **时间复杂度**：`O(n)` — 每个节点只会被访问一次（最坏情况下两次，但常数因子不影响大 O 表示）。  
- **空间复杂度**：`O(h)` — 递归栈深度等于树的高度，最坏 `O(n)`，平均 `O(log n)`（平衡树）。  

---

## 心得  

- **核心技巧**：**递归 + 双向匹配**（考虑翻转与否两种对应关系）。  
- **适用的题型**：  
  1. **相同树的变形**——例如 “相同的树” 题目，只需比较左左右右。  
  2. **可交换子树的判定**——如 “相等的二叉树” 需要考虑子树顺序是否可调。  
  3. **树的同构判定**——判断两棵无根树是否结构相同（常见的树同构问题）。  
- **一句话总结解题钥匙**：**“每个节点只需要比较两种对应关系：不翻转 vs 翻转”。**  

---

## 反思  

- **第一反应**：看到“翻转”二字，立刻想到“把左子树和右子树换位置”，于是想要在遍历时把树“翻个面”。  
- **最容易踩的坑**：  
  - 忽略 **空树** 的情况，导致空指针异常。  
  - 只检查 **不翻转** 的情况，忘记了子树可以在更深层次被翻转。  
  - 没有利用递归返回值的短路特性，导致不必要的额外递归。  
- **下次遇到同类题**，第一步应想到：**“对于每个节点，枚举所有合法的子树配对方式（这里是两种），递归验证”。**这样思路清晰，代码自然就会写出来。