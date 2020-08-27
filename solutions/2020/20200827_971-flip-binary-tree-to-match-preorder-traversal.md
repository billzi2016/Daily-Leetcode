# #971. 翻转二叉树以匹配先序遍历 / Flip Binary Tree To Match Preorder Traversal

> 难度：中等 · 标签：Tree、Depth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/flip-binary-tree-to-match-preorder-traversal/)

---

## 题目（英文原版）

**Description**

You are given the root of a binary tree with n nodes, where each node is uniquely assigned a value from 1 to n. You are also given a sequence of n values voyage, which is the desired pre-order traversal of the binary tree.
Any node in the binary tree can be flipped by swapping its left and right subtrees. For example, flipping node 1 will have the following effect:
Flip the smallest number of nodes so that the pre-order traversal of the tree matches voyage.
Return a list of the values of all flipped nodes. You may return the answer in any order. If it is impossible to flip the nodes in the tree to make the pre-order traversal match voyage, return the list [-1].

**Examples**

**Example 1:**

```
Input: root = [1,2], voyage = [2,1]
Output: [-1]
Explanation: It is impossible to flip the nodes such that the pre-order traversal matches voyage.
```

**Example 2:**

```
Input: root = [1,2,3], voyage = [1,3,2]
Output: [1]
Explanation: Flipping node 1 swaps nodes 2 and 3, so the pre-order traversal matches voyage.
```

**Example 3:**

```
Input: root = [1,2,3], voyage = [1,2,3]
Output: []
Explanation: The tree's pre-order traversal already matches voyage, so no nodes need to be flipped.
```

**Constraints**

- The number of nodes in the tree is n.
- n == voyage.length
- 1 <= n <= 100
- 1 <= Node.val, voyage[i] <= n
- All the values in the tree are unique.
- All the values in voyage are unique.

---

## 题目（中文翻译）

给定一棵包含 `n` 个节点的二叉树（binary tree）根节点 `root`，其中每个节点的值唯一且取值范围为 `1` 到 `n`。同时给定一个长度为 `n` 的序列 `voyage`，它表示期望的先序遍历（pre-order traversal）顺序。

可以对二叉树中的任意节点进行翻转（flip），即交换该节点的左子树（left subtree）和右子树（right subtree）。例如，翻转节点 `1` 会产生如下效果：

> **目标**：以最少的翻转次数，使得树的先序遍历与 `voyage` 完全一致。  
> **返回值**：返回所有被翻转节点的值构成的列表，顺序任意。如果无法通过翻转使先序遍历匹配 `voyage`，则返回 `[-1]`。

---

### 示例

#### 示例 1
**输入**  
```
root = [1,2], voyage = [2,1]
```
**输出**  
```
[-1]
```
**解释**：无法通过翻转节点使得先序遍历匹配 `voyage`。

#### 示例 2
**输入**  
```
root = [1,2,3], voyage = [1,3,2]
```
**输出**  
```
[1]
```
**解释**：翻转节点 `1` 会交换节点 `2` 和 `3`，从而使先序遍历与 `voyage` 匹配。

#### 示例 3
**输入**  
```
root = [1,2,3], voyage = [1,2,3]
```
**输出**  
```
[]
```
**解释**：树的先序遍历已经与 `voyage` 相同，无需翻转任何节点。

---

### 约束条件

- 树中节点的数量为 `n`。  
- `n == voyage.length`  
- `1 <= n <= 100`  
- `1 <= Node.val, voyage[i] <= n`  
- 树中所有节点的值互不相同。  
- `voyage` 中的所有值互不相同。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每一种可能的翻转组合都尝试一遍**，看哪一种能够让树的先序遍历恰好等于 `voyage`，最少翻转的那种就是答案。  

- **遍历所有翻转方式**：每个节点都有两种状态——不翻转、翻转。于是整棵树的翻转方式数量是 `2ⁿ`（`n` 为节点数），相当于把每个节点当成一个“开关”。  
- **模拟先序遍历**：对每一种翻转方式，我们先把树按照该方式“翻转”（即把左、右子树指针互换），随后用递归或栈完成一次普通的先序遍历，得到一个序列 `order`。  
- **比较**：把 `order` 与给定的 `voyage` 逐个比较，若完全相同则记录下这一次用了多少个翻转；所有合法的情况中取最小的翻转集合即可。  

> **类比**：把翻转看成一本词典的“页码”。如果我们把每本词典的章节顺序随意调换（翻转），就会得到不同的阅读顺序。我们要找的是恰好对应目标阅读顺序的那几本词典的调换方式。  

这个方法一定能得到正确答案，因为我们穷举了**所有**可能的翻转组合。只要有一种组合能够匹配 `voyage`，我们必定会在枚举过程中发现它。

#### 代码（Python）

```python
# 暴力解：枚举所有翻转方式
# 由于 n ≤ 100，2^n 在最坏情况下会爆炸，这里仅作思路演示

from itertools import product
from typing import List, Optional

# 二叉树定义（LeetCode 常用）
class TreeNode:
    def __init__(self, val: int, left: 'TreeNode' = None, right: 'TreeNode' = None):
        self.val = val
        self.left = left
        self.right = right

def preorder(root: Optional[TreeNode], res: List[int]) -> None:
    """普通先序遍历（根-左-右），把访问顺序放进 res"""
    if not root:
        return
    res.append(root.val)          # 先访问根
    preorder(root.left, res)      # 再遍历左子树
    preorder(root.right, res)     # 最后遍历右子树

def clone_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """深拷贝一棵树，后面会在拷贝上随意翻转，原树不受影响"""
    if not root:
        return None
    new_root = TreeNode(root.val)
    new_root.left = clone_tree(root.left)
    new_root.right = clone_tree(root.right)
    return new_root

def flip(node: Optional[TreeNode]) -> None:
    """翻转单个节点的左右子树"""
    if node:
        node.left, node.right = node.right, node.left

def brute_force_flip(root: TreeNode, voyage: List[int]) -> List[int]:
    # 先把所有节点收集到列表，方便后面枚举翻转状态
    nodes = []
    def collect(node):
        if not node: return
        nodes.append(node)
        collect(node.left)
        collect(node.right)
    collect(root)

    best = None   # 记录最少翻转的节点集合
    # product 会生成 0/1 的笛卡尔积，长度等于节点数
    for bits in product([0, 1], repeat=len(nodes)):
        # 在原树的拷贝上执行翻转
        cur_root = clone_tree(root)
        # 把 bits 对应的节点映射到拷贝上的同位置节点
        cur_nodes = []
        def map_nodes(orig, copy):
            if not orig: return
            cur_nodes.append(copy)
            map_nodes(orig.left, copy.left)
            map_nodes(orig.right, copy.right)
        map_nodes(root, cur_root)

        flipped = []   # 本次翻转的节点值
        for flag, node in zip(bits, cur_nodes):
            if flag:          # 需要翻转
                flip(node)
                flipped.append(node.val)

        # 计算翻转后树的先序序列
        order = []
        preorder(cur_root, order)

        if order == voyage:   # 匹配成功
            if best is None or len(flipped) < len(best):
                best = flipped

    return best if best is not None else [-1]
```

> **注意**：上述代码仅用于说明「暴力」思路，实际运行会因为 `2ⁿ` 的指数爆炸而超时。  

#### 复杂度  

- **时间复杂度**：`O(2^n * n)`  
  - `2^n` 是所有翻转组合的数量。  
  - 对每一种组合，我们需要一次先序遍历（`O(n)`）以及若干常数级操作。  
  - 用大白话说，就是**随着节点数的增加，耗时会呈指数级增长**，几乎不可能在 1 秒内跑完 100 个节点的情况。  

- **空间复杂度**：`O(n)`  
  - 需要保存树的拷贝以及递归栈，最多 `n` 个节点的空间。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**真正的瓶颈在于我们尝试了所有不必要的翻转**。实际上，在一次先序遍历的过程中，我们已经能够判断是否需要翻转，以及是否有解。关键在于：

1. **先序遍历的顺序是唯一的**：先访问根，再左子树，最后右子树。  
2. **`voyage` 给出了我们期望的访问顺序**，我们只要在遍历时“对齐”它，就不必尝试别的组合。  

##### 具体步骤  

- 用一个全局指针 `i` 指向 `voyage` 当前应该匹配的元素（初始 `i = 0`）。  
- 递归遍历树：

  1. **检查根节点**：如果当前根的值 `node.val` 与 `voyage[i]` 不相等，说明已经偏离目标序列，**无论怎么翻转都无法恢复**，直接返回失败。  
  2. **匹配成功后**，`i += 1`，准备匹配左子树的第一个节点。  
  3. **决定是否翻转**：  
     - 正常情况下，左子树的根应该是 `voyage[i]`（因为先序遍历先走左子树）。  
     - 如果左子树不存在，或者左子树的根正好等于 `voyage[i]`，**不需要翻转**，直接递归左、右子树。  
     - 否则（左子树根不等于 `voyage[i]`），**说明期望的下一个节点其实在右子树**，这时我们必须把当前节点的左右子树互换一次（记录该节点的值），然后再按**“先左后右”**的顺序递归（此时原来的右子树已经变成左子树）。  

- 如果在递归的任何一步发现不匹配，立刻返回失败。遍历结束后如果没有失败，则记录的所有翻转节点即为答案。  

##### 为什么这样一定最优？  

- **只在必须翻转的地方翻转**：如果左子树根不等于 `voyage[i]`，唯一的办法是把右子树提前访问，而翻转正好实现了这一点。没有别的更少翻转的办法。  
- **一次遍历即可决定**：我们只用一次深度优先搜索（DFS），每个节点最多检查一次，时间线性。  

> **类比**：想象你在阅读一本书的章节目录（`voyage`），但手头的章节顺序（树的先序）和目录不完全一致。每当你发现下一个要读的章节在后面的“右边”，只能把当前章节的左、右顺序调换一次，才能继续顺着目录往下读。调换的次数恰好就是我们要记录的节点。  

#### 代码（Python）

```python
# 最优解：一次 DFS，按需翻转
from typing import List, Optional

class TreeNode:
    def __init__(self, val: int, left: 'TreeNode' = None, right: 'TreeNode' = None):
        self.val = val
        self.left = left
        self.right = right

def flipMatchVoyage(root: Optional[TreeNode], voyage: List[int]) -> List[int]:
    """
    返回需要翻转的节点值列表；若不可能，则返回 [-1]。
    思路：一次先序遍历，对齐 voyage；只有左子树根不符合时才翻转。
    """
    res = []            # 记录翻转的节点值
    i = 0               # 全局指针，指向 voyage 当前要匹配的位置

    def dfs(node: Optional[TreeNode]) -> bool:
        """返回 True 表示子树可以匹配，否则 False"""
        nonlocal i
        if not node:                 # 空节点天然匹配
            return True
        # 1）根必须与当前 voyage[i] 相等，否则直接失败
        if node.val != voyage[i]:
            return False
        i += 1                       # 匹配成功，指针前进

        # 2）检查左子树根是否符合下一个期待值
        #   如果左子树存在且左子树根 != voyage[i]，说明需要翻转
        if node.left and i < len(voyage) and node.left.val != voyage[i]:
            # 记录翻转
            res.append(node.val)
            # 先遍历原来的右子树（现在变成左子树），再遍历原来的左子树
            if not dfs(node.right):   # 右子树先
                return False
            if not dfs(node.left):    # 左子树后
                return False
        else:
            # 正常顺序：先左后右
            if not dfs(node.left):
                return False
            if not dfs(node.right):
                return False
        return True

    if dfs(root):
        return res          # 成功匹配，返回所有翻转节点
    else:
        return [-1]         # 无法匹配，返回 [-1]
```

> **代码要点注释**  
- `i` 是全局指针，始终指向 **下一个** 应该匹配的 `voyage` 元素。  
- `if node.left and node.left.val != voyage[i]` 判断左子树根是否**不符合**期望；此时唯一可行的操作是**翻转**。  
- `res.append(node.val)` 记录被翻转节点的值，题目要求返回的顺序可以是任意，只要包含所有翻转节点即可。  

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 每个节点只被访问一次（递归调用一次），所有比较、指针移动都是 `O(1)`。  
  - 用大白话说，就是“节点数量多少，耗时就多少”，线性增长，100 个节点轻松跑完。  

- **空间复杂度**：`O(h)`（递归栈），`h` 为树的高度。  
  - 最坏情况下树退化成链表，`h = n`，此时栈空间是 `O(n)`。  
  - 对于平衡树，`h ≈ log n`，空间更小。  

---

## 心得  

- **核心技巧**：在先序遍历过程中**实时对齐**目标序列，只有在左子树根不符合期待时才翻转。  
- **适用的题型**：  
  1. “翻转二叉树使先序/中序/后序匹配” 类的题目（如本题）。  
  2. “根据给定遍历序列重建二叉树” 时，需要判断唯一性或可行性。  
  3. “在遍历过程中动态决定操作” 的贪心/模拟题（如 LeetCode 965. Univalued Binary Tree 的类似思路）。  
- **一句话总结解题钥匙**：**只在必须让下一个期望节点提前出现时才翻转**，一次 DFS 即可完成全部判断。  

---

## 反思  

- **第一反应**：看到“翻转子树”和“先序遍历”，马上想到“遍历过程中比对序列”，于是想到了递归+指针。  
- **最容易踩的坑**：  
  - 忘记在根节点不匹配时立刻返回 `False`，导致后续仍然继续遍历产生错误结果。  
  - 当左子树为空而右子树恰好是下一个期待值时，**不需要翻转**；若误判为需要翻转，会多余记录错误节点。  
  - 边界条件：`voyage` 长度恰好等于节点数，指针 `i` 不能越界。  

- **下次遇到同类题**：**先把目标遍历序列当成指针**，在递归遍历时逐步对齐，只有在“下一个应访问的节点在右侧”时才进行翻转或其他必要操作。这样可以把“枚举所有可能”转化为“一次贪心模拟”。