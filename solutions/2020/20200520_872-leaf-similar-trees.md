# #872. 叶子相似的树 / Leaf-Similar Trees

> 难度：简单 · 标签：Tree、Depth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/leaf-similar-trees/)

---

## 题目（英文原版）

**Description**

Consider all the leaves of a binary tree, from left to right order, the values of those leaves form a leaf value sequence.
For example, in the given tree above, the leaf value sequence is (6, 7, 4, 9, 8).
Two binary trees are considered leaf-similar if their leaf value sequence is the same.
Return true if and only if the two given trees with head nodes root1 and root2 are leaf-similar.

**Examples**

**Example 1:**

```
Input: root1 = [3,5,1,6,2,9,8,null,null,7,4], root2 = [3,5,1,6,7,4,2,null,null,null,null,null,null,9,8]
Output: true
```

**Example 2:**

```
Input: root1 = [1,2,3], root2 = [1,3,2]
Output: false
```

**Constraints**

- The number of nodes in each tree will be in the range [1, 200].
- Both of the given trees will have values in the range [0, 200].

---

## 题目（中文翻译）

考虑一棵二叉树（binary tree）的所有叶子（leaf），按照从左到右的顺序，这些叶子的值构成一个叶子值序列（leaf value sequence）。  
例如，上图中的二叉树，其叶子值序列为 (6, 7, 4, 9, 8)。  

如果两棵二叉树的叶子值序列相同，则这两棵树被认为是叶子相似的（leaf-similar）。  
只有当给定的两棵树的根节点（head nodes）`root1` 和 `root2` 的叶子值序列完全相同，函数才返回 `true`，否则返回 `false`。

**示例 1**  
**示例 2**  
**约束条件**  

**示例：**  
**示例 1:**  
```
Input: root1 = [3,5,1,6,2,9,8,null,null,7,4], root2 = [3,5,1,6,7,4,2,null,null,null,null,null,null,9,8]
Output: true
```

**示例 2:**  
```
Input: root1 = [1,2,3], root2 = [1,3,2]
Output: false
```

**约束条件：**  
- 每棵树的节点数在区间 `[1, 200]` 内。  
- 两棵树的节点值均在区间 `[0, 200]` 内。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：把两棵树的所有叶子节点都“摘下来”，按照从左到右的顺序排成一个列表，然后把两个列表逐个比较是否相同。

- **叶子节点**：没有左子树也没有右子树的节点。可以把它想象成一棵树的“果实”，只有到达最底层才会收获。
- **遍历方式**：深度优先搜索（DFS）是最自然的方式。递归地先左子树后右子树，就能保证“左到右”的顺序。递归函数好比一个 **“查字典”**，每次进到左子树就像在字典里往前翻页，左子树遍历完再去右子树。
- **为什么正确**：DFS 按照 **左‑子‑树 → 右‑子‑树** 的顺序访问每个节点，恰好对应题目要求的叶子从左到右的顺序。把遍历到的叶子值依次放进列表，列表的顺序就等价于题目说的 “leaf value sequence”。比较两个列表是否相等，自然就能判断两棵树是否 leaf‑similar。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的数值
        self.left = left        # 左子树
        self.right = right      # 右子树

def leaf_sequence(root: TreeNode) -> list[int]:
    """
    深度优先遍历整棵树，把所有叶子节点的值按左→右顺序收集到列表中
    """
    leaves = []                     # 用来保存叶子序列的列表

    def dfs(node: TreeNode):
        if not node:                # 空节点直接返回
            return
        if not node.left and not node.right:   # 同时没有左子树和右子树 → 叶子
            leaves.append(node.val)            # 把叶子的值加入列表
            return
        dfs(node.left)   # 先遍历左子树 → 保证左边的叶子先被收集
        dfs(node.right)  # 再遍历右子树

    dfs(root)                         # 从根节点开始遍历
    return leaves

def leafSimilar(root1: TreeNode, root2: TreeNode) -> bool:
    """
    暴力解：分别得到两棵树的叶子序列，然后直接比较两个列表是否相等
    """
    seq1 = leaf_sequence(root1)   # 树 1 的叶子序列
    seq2 = leaf_sequence(root2)   # 树 2 的叶子序列
    return seq1 == seq2           # 列表相等 → 两棵树 leaf‑similar
```

#### 复杂度

- **时间复杂度**：`O(N + M)`  
  这里 `N`、`M` 分别是两棵树的节点数。我们要把每个节点都访问一次（递归遍历），所以时间随节点总数线性增长。  
  用大白话说，节点越多，花的时间就像把所有水果从树上摘下来一样，必须一个一个检查。

- **空间复杂度**：`O(H1 + H2)`（递归栈）+ `O(L1 + L2)`（叶子列表）  
  - 递归调用的最大深度等于树的高度 `H`，相当于树的“枝杈”最深的层数。  
  - 我们额外用了两个列表来保存所有叶子，叶子数量记作 `L`。最坏情况下（所有节点都是叶子），列表大小和节点数相同。  

---

### 2. 最优解

#### 思路  
在暴力解里，我们把 **所有** 叶子一次性全部保存下来再比较。实际上，只要在遍历的过程中 **同步** 比较两个树的叶子，就可以提前发现不相等的情况，省掉很多不必要的存储。

- **瓶颈所在**：  
  1. 需要额外的列表保存完整的叶子序列，空间是 `O(L)`。  
  2. 即使前面已经发现序列不同，仍然会继续遍历完整棵树（因为我们在遍历完才比较）。

- **优化思路**：  
  把遍历过程变成“**生成器**”（generator），每次只产生下一个叶子值。然后交替从两棵树的生成器中取值进行比较：

  1. 用 **DFS 生成器** `yield` 叶子值，保持左→右顺序。  
  2. 同时从 `gen1`、`gen2` 取出下一个叶子值 `v1`、`v2`。  
  3. 若两者不相等，直接返回 `False`。  
  4. 当两棵树的叶子都遍历完（生成器抛出 `StopIteration`），说明所有叶子都相等，返回 `True`。

  这样我们只在栈中保留递归的路径（高度 `H`），不需要额外的列表，空间降到 `O(H1 + H2)`。时间仍然是一次遍历 `O(N + M)`，但在发现不相等时可以**提前结束**，更快。

- **核心概念解释**  
  - **生成器（generator）**：可以把一个函数想象成“**按需供应**”的机器。调用 `next()` 时，它才会运行到下一个 `yield` 位置并把结果输出，随后“暂停”。这就像你在森林里采果子，每次只摘一颗，走到下一颗再摘，不需要一次性装满背包。  
  - **栈（递归调用本身的栈）**：递归实现 DFS 时，系统会为每一次函数调用压入一个“记号”，这就是栈。栈的深度等于树的高度 `H`，相当于我们在树的最深分支上爬到最高点时背的背包层数。

#### 代码（Python）

```python
def leaf_generator(root: TreeNode):
    """
    采用深度优先遍历的生成器，按左→右顺序依次产生叶子节点的值
    """
    stack = [root]               # 用显式栈模拟递归，避免递归深度限制
    while stack:
        node = stack.pop()       # 取出栈顶节点
        if not node:
            continue
        # 如果是叶子，直接产出（yield）它的值
        if not node.left and not node.right:
            yield node.val
        else:
            # 先右后左入栈，这样弹出时左子树会先被处理，保持左→右顺序
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)

def leafSimilar(root1: TreeNode, root2: TreeNode) -> bool:
    """
    最优解：同步遍历两棵树的叶子生成器，逐个比较
    """
    gen1 = leaf_generator(root1)   # 生成器 1
    gen2 = leaf_generator(root2)   # 生成器 2

    while True:
        try:
            v1 = next(gen1)        # 取出下一颗叶子
        except StopIteration:
            v1 = None               # 生成器已遍历完

        try:
            v2 = next(gen2)
        except StopIteration:
            v2 = None

        # 同时遍历完 → 两棵树的叶子数量相同且全部相等
        if v1 is None and v2 is None:
            return True
        # 只要有一个提前结束或两个值不相等 → 不是 leaf‑similar
        if v1 != v2:
            return False
```

#### 复杂度

- **时间复杂度**：`O(N + M)`（最坏情况）  
  每棵树的每个节点仍然只会被访问一次。若在遍历过程中提前发现不相等，实际耗时会更少——相当于“先发现问题就先停”。  
  与暴力解相比，时间大体相同，只是**更早**可以返回。

- **空间复杂度**：`O(H1 + H2)`  
  只用了显式栈保存遍历路径，栈的最大深度等于树的高度 `H`。没有额外的列表来存放所有叶子，显著降低了空间开销。  
  用生活化的比喻：我们不再一次性装满背包（列表），而是只背一把梯子（栈），随走随用。

---

## 心得

- **核心技巧**：使用 **生成器（yield） + 双指针/同步遍历**，在遍历过程中即时比较，既省空间又能提前结束。  
- **适用的题型**  
  1. **两序列相等**的判定（如判断两链表是否相同、两数组是否相同）——可以用生成器同步遍历。  
  2. **流式比较**（如比较两个有序流是否相同、合并两个有序流）——同样可以边读边比较。  
  3. **树的特殊遍历**（如比较两棵树的中序遍历是否相同、前序遍历是否相同）——把遍历写成生成器即可。
- **一句话总结**：**“把遍历变成按需产值的生成器，边走边比，省掉整列存储”。**

---

## 反思

- **第一反应**：看到“叶子序列”，立刻想到 **DFS 收集所有叶子**，再比较两个列表——这就是最直觉的暴力思路。  
- **最容易踩的坑**  
  1. **遍历顺序错误**：如果先右子树再左子树，得到的叶子序列会倒置，导致误判。  
  2. **空树或只有根节点的情况**：根节点本身可能是叶子，需要把 `if not node.left and not node.right` 放在递归/遍历的最前面。  
  3. **生成器提前结束**：比较时必须同时检测两个生成器是否都已遍历完，否则可能出现一个还有叶子而另一个已经结束的假阳性。  
- **下次遇到同类题的第一步**：先思考 **“是否可以把完整结果逐个产生而不是一次性存下来？”**，如果答案是肯定的，就尝试用生成器或迭代器实现同步比较。这样往往能把空间从 `O(N)` 降到 `O(H)`。