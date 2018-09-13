# #101. 对称二叉树 / Symmetric Tree

> 难度：简单 · 标签：Tree、Depth-First Search、Breadth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/symmetric-tree/)

---

## 题目（英文原版）

**Description**

Given the root of a binary tree, check whether it is a mirror of itself (i.e., symmetric around its center).

**Examples**

**Example 1:**

```
Input: root = [1,2,2,3,4,4,3]
Output: true
```

**Example 2:**

```
Input: root = [1,2,2,null,3,null,3]
Output: false
```

**Constraints**

- The number of nodes in the tree is in the range [1, 1000].
- -100 <= Node.val <= 100

---

## 题目（中文翻译）

给定一棵二叉树的根节点 `root`，判断该树是否是自身的镜像（即关于中心对称）。

**示例 1**  
**输入**: `root = [1,2,2,3,4,4,3]`  
**输出**: `true`

**示例 2**  
**输入**: `root = [1,2,2,null,3,null,3]`  
**输出**: `false`

**约束条件**  
- 树中节点的数量在 `[1, 1000]` 区间内。  
- `-100 <= Node.val <= 100`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直观的做法是 **把树按层级（level）展开**，把每一层的节点值放进一个列表，然后检查这个列表是否是回文（前后读都一样）。  
- **层序遍历**（Breadth‑First Search，简称 BFS）可以一次性把树的所有层都遍历出来，类似于我们在超市排队结账时，从前往后依次检查每个人的购物车。  
- **回文检查** 就像读一本书的章节标题，如果正着读和反着读完全相同，就说明这层是对称的。  
- 如果所有层都满足回文条件，整棵树就是对称的；只要有一层不满足，就可以立刻返回 `False`。

> **为什么这个方法能得到正确答案？**  
> 对称二叉树的定义要求：左子树的结构和右子树的结构是镜像的，且对应位置的节点值相等。层序遍历把同一层的节点从左到右依次列出，如果这层从左到右的顺序和从右到左的顺序完全相同（即回文），说明这层的左右两侧是镜像的。对每一层都如此检查，等价于检查整棵树的对称性。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的数值
        self.left = left        # 左子树
        self.right = right      # 右子树


def isSymmetric(root: TreeNode) -> bool:
    """暴力层序遍历 + 回文检查"""
    if not root:                     # 空树自然对称
        return True

    # 用队列实现 BFS（这里用列表当队列，pop(0) 代表出队）
    queue = [root]

    while queue:
        level_vals = []              # 当前层的节点值（包括 None 占位）
        next_queue = []              # 下一层的节点

        # 把本层所有节点全部取出来
        for node in queue:
            if node:
                level_vals.append(node.val)          # 记录真实节点的值
                # 左右子节点都要加入下一层，即使是 None 也要占位
                next_queue.append(node.left)
                next_queue.append(node.right)
            else:
                level_vals.append(None)               # 用 None 表示空位

        # 检查本层是否回文
        if level_vals != level_vals[::-1]:           # 列表反转后比较
            return False

        # 只要下一层还有真实节点，就继续循环
        # （如果全是 None，说明已经遍历完所有层）
        if any(n is not None for n in next_queue):
            queue = next_queue
        else:
            break

    return True
```

#### 复杂度

- **时间复杂度：** `O(n)`  
  这里的 `n` 是树中节点的数量。我们遍历每个节点恰好一次，并且对每层做一次回文比较（回文比较本身是线性的，但所有层加起来仍是 `O(n)`）。
- **空间复杂度：** `O(n)`  
  最坏情况下（例如完全二叉树的最后一层），队列里会同时存放约 `n/2` 个节点，属于线性空间。

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在 **“把整棵树层层展开后再检查回文”**，这一步把树的结构信息额外复制了一遍，空间上不够紧凑。  
其实，对称性本质上是 **“左子树和右子树是否互为镜像”**，我们可以 **递归地同时遍历这两棵子树**，每次只比较两个对应节点，而不需要把整层保存下来。

关键点：

1. **镜像比较**  
   - 两个节点 `a`（左子树的某个节点）和 `b`（右子树的对应节点）必须满足：  
     - `a.val == b.val`（数值相等）  
     - `a.left` 与 `b.right` 互为镜像  
     - `a.right` 与 `b.left` 互为镜像  
   - 这正好形成了递归的子问题。

2. **递归终止条件**  
   - 同时为 `None` → 两侧都是空，视为对称。  
   - 一个为 `None` 而另一个不为 `None` → 结构不匹配，直接返回 `False`。  
   - 两个都不为 `None` 但数值不同 → 直接返回 `False`。

3. **实现方式**  
   - 写一个辅助函数 `isMirror(left, right)` 完成上述递归检查。  
   - 主函数只需要调用 `isMirror(root.left, root.right)` 即可。

> **类比**：把两棵子树想象成两面镜子，左边树的左手要和右边树的右手对应，左边树的右手要和右边树的左手对应。如果每一对手都形状相同、位置相同，那么两面镜子就完美对称。

#### 代码（Python）

```python
def isSymmetric(root: TreeNode) -> bool:
    """递归版：同时遍历左、右子树，检查镜像对称"""

    def isMirror(left: TreeNode, right: TreeNode) -> bool:
        # 1️⃣ 两侧都为空 → 对称
        if not left and not right:
            return True
        # 2️⃣ 只有一侧为空 → 不对称
        if not left or not right:
            return False
        # 3️⃣ 数值不相等 → 不对称
        if left.val != right.val:
            return False

        # 4️⃣ 递归比较外侧和内侧
        #    left 的左子树 ↔ right 的右子树
        #    left 的右子树 ↔ right 的左子树
        return isMirror(left.left, right.right) and isMirror(left.right, right.left)

    # 空树直接返回 True
    if not root:
        return True

    return isMirror(root.left, root.right)
```

#### 复杂度

- **时间复杂度：** `O(n)`  
  每个节点恰好被访问一次（在递归过程中），所以整体仍是线性时间。相比暴力层序遍历，它没有额外的回文检查步骤，常数因子更小。

- **空间复杂度：** `O(h)`（其中 `h` 为树的高度）  
  递归调用会占用栈空间，最坏情况下（树呈链状）高度 `h = n`，空间退化到 `O(n)`；而在平衡二叉树中，`h ≈ log n`，空间只需 `log n`，比暴力解的 `O(n)` 更紧凑。

---

## 心得

- **核心技巧**：**镜像递归**（或迭代双指针）——同时从左、右两侧向内推进，比较对应节点的值和结构。
- **适用的题型**：  
  1. 判断两棵二叉树是否相同（LeetCode 100 – Same Tree）  
  2. 合并两棵二叉树（LeetCode 617 – Merge Two Binary Trees）  
  3. 检查二叉搜索树的前序序列是否合法（LeetCode 255 – Verify Preorder Sequence in Binary Search Tree）  
- **一句话总结**：**“把左子树的左边当右子树的右边来比较，左子树的右边当右子树的左边来比较”。**

## 反思

- **第一反应**：看到“对称”，马上想到“左↔右镜像”，于是想到层序遍历后检查回文或递归同时遍历两侧。
- **最容易踩的坑**：  
  - 忽略空节点的占位导致结构不匹配（如左子树有左孩子而右子树没有右孩子）。  
  - 只比较节点值而忘记比较子树结构。  
  - 递归结束条件写错导致无限递归或提前返回。  
- **下次第一步**：先在脑子里画出两侧的“镜像对应关系”，确认需要同时遍历的两个子树，然后决定是递归实现还是用显式栈/队列的迭代实现。