# #814. 二叉树剪枝 / Binary Tree Pruning

> 难度：中等 · 标签：Tree、Depth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/binary-tree-pruning/)

---

## 题目（英文原版）

**Description**

Given the root of a binary tree, return the same tree where every subtree (of the given tree) not containing a 1 has been removed.
A subtree of a node node is node plus every node that is a descendant of node.

**Examples**

**Example 1:**

```
Input: root = [1,null,0,0,1]
Output: [1,null,0,null,1]
Explanation: 
Only the red nodes satisfy the property "every subtree not containing a 1".
The diagram on the right represents the answer.
```

**Example 2:**

```
Input: root = [1,0,1,0,0,0,1]
Output: [1,null,1,null,1]
```

**Example 3:**

```
Input: root = [1,1,0,1,1,0,1,0]
Output: [1,1,0,1,1,null,1]
```

**Constraints**

- The number of nodes in the tree is in the range [1, 200].
- Node.val is either 0 or 1.

---

## 题目（中文翻译）

给定一棵二叉树（binary tree）的根节点 `root`，返回同一棵树，其中所有**不包含 1 的子树（subtree）**都已被删除。  
节点 `node` 的子树指的是 `node` 本身以及所有是 `node` 的后代（descendant）的节点。

### 示例 1
**输入**: `root = [1,null,0,0,1]`  
**输出**: `[1,null,0,null,1]`  
**解释**:  
只有红色的节点满足“每个子树都不包含 1”这一属性。右侧的图示即为答案。

### 示例 2
**输入**: `root = [1,0,1,0,0,0,1]`  
**输出**: `[1,null,1,null,1]`

### 示例 3
**输入**: `root = [1,1,0,1,1,0,1,0]`  
**输出**: `[1,1,0,1,1,null,1]`

### 约束条件
- 树中节点的数量在 `[1, 200]` 之间。  
- `Node.val` 仅为 `0` 或 `1`。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**对每一个节点**都检查它的整棵子树里有没有 `1`，如果没有就把这个节点整个删除。  
实现时可以：

1. **遍历整棵树**（先序/中序/后序都行），把每个节点的指针记下来。  
2. 对于遍历到的每个节点，**再跑一次 DFS** 去判断该节点所在的子树是否包含 `1`。  
   - 这一步相当于在“查字典”，我们把 **子树的所有节点** 当作字典的“词”，要找的 `1` 就是“页码”。  
3. 如果子树里没有 `1`，把该节点从父节点的左/右指针设为 `None`（相当于把这本书从书架上拿走）。  

> **为什么正确？**  
> 只要我们对每个节点都做了“子树里有没有 1”的检查，并且把不满足条件的整棵子树删掉，最后留下的树必然是“每个子树里至少有一个 1”。  

> **时间/空间分析（大白话）**  
> - 对每个节点我们都要**再遍历一次它的子树**，最坏情况下（比如所有节点都是 `0`），第一次遍历访问 `n` 个节点，第二次遍历又访问 `n-1` 个，依次类推，总共大约 `n + (n‑1) + … + 1 = n·(n+1)/2` 次访问。  
> - 用数学符号写就是 **O(n²)**，也就是“平方级”，意思是当节点数翻倍时，运行时间会增加大约四倍。  
> - 额外的空间只用来保存递归栈深度，最坏是树的高度 `O(n)`（链状树），再加上一点临时的指针变量，整体是 **O(n)**。  

#### 代码（Python）  

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def contains_one(node: TreeNode) -> bool:
    """判断以 node 为根的子树里是否至少有一个 1。
    这里用的是普通的 DFS，遍历所有后代节点。"""
    if not node:
        return False
    # 先检查当前节点的值
    if node.val == 1:
        return True
    # 再检查左子树和右子树
    return contains_one(node.left) or contains_one(node.right)


def pruneTree_bruteforce(root: TreeNode) -> TreeNode:
    """暴力版：对每个节点都重新检查一次子树是否包含 1。"""
    if not root:
        return None

    # 先递归处理左、右子树，确保子树已经被裁剪好
    root.left = pruneTree_bruteforce(root.left)
    root.right = pruneTree_bruteforce(root.right)

    # 现在检查以当前节点为根的整棵子树是否有 1
    if not contains_one(root):
        # 整个子树都没有 1，直接返回 None（等同于删除）
        return None
    # 否则保留当前节点
    return root
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 想象每个节点都要“重新打开一本字典”，字典的大小随节点数线性增长，最终的访问次数是平方级的。  
- **空间复杂度**：`O(n)`  
  - 递归调用的最深层次等于树的高度，最坏情况下树退化成链表，需要 `n` 层栈空间。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**重复检查子树是否包含 `1`** 是主要的性能瓶颈。  
我们可以在一次遍历中**把“检查”和“剪枝”这两件事合并**，这样每个节点只访问一次。

**关键点**：

1. **后序遍历（左 → 右 → 父）**：先把子树处理好，再决定父节点该不该被删除。  
   - 想象我们在修剪树枝：先把下面的枝条都剪掉（处理子树），再判断上面的枝干是否还能留下。  
2. **返回值**：对每个递归调用返回一个布尔值 `has_one`，表示该子树里是否至少有一个 `1`。  
   - 如果左子树返回 `False`，说明左子树全是 `0`，我们就把 `node.left = None`（相当于把这根左枝剪掉）。右子树同理。  
3. **剪枝后**：如果当前节点的值是 `0`，且左、右子树都已经被剪掉（即 `has_one_left`、`has_one_right` 都是 `False`），那么这棵子树里没有 `1`，返回 `False` 给父节点，让父节点把它剪掉。  

**为什么这样是最优的？**  

- 每个节点只被访问一次，**没有重复检查**。  
- 所有信息（子树里是否有 `1`）都在一次递归中向上传递，不需要额外的遍历或存储。  

**核心算法**：**后序深度优先搜索（DFS） + 递归返回信息**。  

#### 代码（Python）  

```python
def pruneTree(root: TreeNode) -> TreeNode:
    """
    最优解：一次 DFS 完成检查与剪枝。
    返回值：
        True  -> 该子树（包括当前节点）至少包含一个 1
        False -> 该子树全是 0，需要被父节点剪掉
    """
    if not root:
        # 空树显然不含 1
        return False

    # 先递归处理左、右子树，得到它们是否含 1
    left_has_one = pruneTree(root.left)   # 左子树会在内部完成剪枝
    right_has_one = pruneTree(root.right) # 右子树会在内部完成剪枝

    # 根据子树的返回值决定是否剪枝
    if not left_has_one:
        # 左子树全是 0，直接切断左指针
        root.left = None
    if not right_has_one:
        # 右子树全是 0，直接切断右指针
        root.right = None

    # 当前节点只要自身是 1，或者左/右子树中有 1，就算“含 1”
    return root.val == 1 or left_has_one or right_has_one


def pruneTree_wrapper(root: TreeNode) -> TreeNode:
    """
    对外统一的入口函数，返回剪枝后的根节点。
    如果整棵树都没有 1，pruneTree 会返回 False，此时我们返回 None。
    """
    if pruneTree(root):
        return root          # 根节点本身或其子树里有 1，保留根
    else:
        return None          # 全树都是 0，直接返回空树
```

> **代码注释要点**  
> - `if not root: return False`：空树相当于“没有 1”。  
> - `left_has_one = pruneTree(root.left)`：递归返回左子树是否含 1，递归内部已经完成了对左子树的所有剪枝。  
> - `if not left_has_one: root.left = None`：左子树全是 0，直接把左指针设为 `None`（相当于把这根枝条砍掉）。  
> - `return root.val == 1 or left_has_one or right_has_one`：只要当前节点是 1，或者任意子树里有 1，就算本子树“含 1”。  

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 每个节点只被访问一次，类似“一遍走完所有树枝”。  
- **空间复杂度**：`O(h)`，其中 `h` 是树的高度（递归栈占用的空间）。  
  - 对于平衡二叉树，`h ≈ log₂ n`，所以空间是对数级的。最坏情况下（链状树）`h = n`，仍然是线性空间。  

---  

## 心得  

- **核心技巧**：后序深度优先搜索（DFS）配合**递归返回信息**（本题返回子树是否含 1）实现“一遍遍历、同步剪枝”。  
- **适用的题型**：  
  1. “删除满足某种条件的子树”类题目（如 *Remove Subtrees With All Even Values*）。  
  2. “在遍历过程中累计信息并决定是否保留”类题目（如 *Binary Tree Maximum Path Sum* 的后序 DP）。  
  3. “需要自底向上合并子树信息” 的树形 DP 题目（如 *House Robber III*）。  
- **一句话总结解题钥匙**：**后序遍历 + 子树信息向上回传**，让剪枝在子树已经处理好的前提下安全进行。  

---  

## 反思  

- **第一反应**：看到“删除不含 1 的子树”，立刻想到“遍历每个节点，检查子树里有没有 1”。这导致了重复遍历的暴力想法。  
- **最容易踩的坑**：  
  - **忘记先处理子树**：如果先判断当前节点再剪枝，可能会误剪掉本该保留的子树。  
  - **返回值写错**：返回 `True` 表示“本子树含 1”，返回 `False` 表示“全是 0”，弄反会导致整棵树被错误剪除。  
  - **空树返回处理**：根节点整棵树全是 0 时，需要额外把最终返回值设为 `None`，否则会得到一个空根节点但仍保留引用。  
- **下次遇到同类题**：第一步就想**“是否可以在一次遍历中把需要的信息往上传递？”**，如果可以，就直接设计后序 DFS 并让递归返回必要的状态，而不是做多次遍历。