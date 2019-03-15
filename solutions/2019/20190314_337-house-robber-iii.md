# #337. 打家劫舍 III / House Robber III

> 难度：中等 · 标签：Dynamic Programming、Tree、Depth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/house-robber-iii/)

---

## 题目（英文原版）

**Description**

The thief has found himself a new place for his thievery again. There is only one entrance to this area, called root.
Besides the root, each house has one and only one parent house. After a tour, the smart thief realized that all houses in this place form a binary tree. It will automatically contact the police if two directly-linked houses were broken into on the same night.
Given the root of the binary tree, return the maximum amount of money the thief can rob without alerting the police.

**Examples**

**Example 1:**

```
Input: root = [3,2,3,null,3,null,1]
Output: 7
Explanation: Maximum amount of money the thief can rob = 3 + 3 + 1 = 7.
```

**Example 2:**

```
Input: root = [3,4,5,1,3,null,1]
Output: 9
Explanation: Maximum amount of money the thief can rob = 4 + 5 = 9.
```

**Constraints**

- The number of nodes in the tree is in the range [1, 104].
- 0 <= Node.val <= 104

---

## 题目（中文翻译）

小偷又找到了一处新的作案地点。该区域只有唯一的入口，称为根节点（root）。  
除了根节点外，每栋房子都有且仅有一个父节点（parent house）。经过观察，聪明的小偷发现该地区的所有房子构成了一棵二叉树（binary tree）。如果在同一夜晚盗窃了两栋直接相连的房子，警报会自动触发并联系警察。  

给定二叉树的根节点，返回小偷在不触发警报的前提下能够抢劫的最大金额。

**示例 1**  
**示例 2**  
**约束条件**  

示例  
**示例 1**  
``` 
Input: root = [3,2,3,null,3,null,1]
Output: 7
Explanation: 最大可抢劫的金额为 3 + 3 + 1 = 7.
```  

**示例 2**  
``` 
Input: root = [3,4,5,1,3,null,1]
Output: 9
Explanation: 最大可抢劫的金额为 4 + 5 = 9.
```  

约束条件：
- 树中节点的数量范围为 \[1, 10^4\]。
- 0 ≤ Node.val ≤ 10^4。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**对每一棵子树，都尝试两种选择**——  
1. 抢当前节点的金币，那么它的左右子节点就**不能**再被抢。  
2. 不抢当前节点，那么左右子节点可以自行决定抢不抢。

于是我们可以用递归遍历整棵树，对每个节点枚举这两种情况，取最大值返回。  

- **用到的数据结构**：二叉树的节点（`TreeNode`）。递归本质上是**调用栈**，相当于我们在“走路”时把已经走过的路径放进背包，等回头时再取出来。  
- **为什么正确**：因为我们枚举了所有合法的抢劫方案（没有出现相邻父子同时被抢的情况），最终的最大值自然就是答案。  

> 这里的“暴力”其实就是**穷举**所有可能的组合，和把所有钥匙都尝试一遍的过程类似。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def rob(root: TreeNode) -> int:
    """暴力递归：对每个节点尝试抢或不抢，返回能得到的最大金额"""
    if not root:
        return 0

    # 方案1：抢当前节点，则左右孩子不能抢，只能继续抢孙子辈
    val_with_root = root.val
    if root.left:
        # 左子树的左右孩子可以抢
        val_with_root += rob(root.left.left) + rob(root.left.right)
    if root.right:
        # 右子树的左右孩子可以抢
        val_with_root += rob(root.right.left) + rob(root.right.right)

    # 方案2：不抢当前节点，则直接递归左右子树，子树内部自行决定抢不抢
    val_without_root = rob(root.left) + rob(root.right)

    # 取两种方案的最大值
    return max(val_with_root, val_without_root)
```

#### 复杂度  

- **时间复杂度**：`O(2^n)` —— 对每个节点都有“抢”或“不抢”两种选择，最坏情况下会遍历所有可能的子集，类似二进制数从 `0` 到 `2^n‑1` 的枚举。  
- **空间复杂度**：`O(h)` —— 递归调用栈的深度等于树的高度 `h`（最坏 `h = n`，即链表形状），因此额外空间随树高线性增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**重复计算**是主要的性能瓶颈。比如在上面的代码里，同一个子树的 `rob` 会被多次调用（左子树的孙子、右子树的孙子等都会重复遍历）。  
我们需要**记住**每个子树已经算好的结果，这正是**动态规划**的思想：把大问题拆成子问题，子问题只算一次，后面直接查表。

**关键观察**：对于每个节点，有两种“状态”：

1. **抢了这个节点** → 只能拿它的左右子树的“未抢”结果。  
2. **没抢这个节点** → 可以自由选择左右子树的“抢”或“未抢”中更大的那个。

于是我们在 **后序遍历**（先算左右子树，再算当前节点）时，返回一个二元组：

```
(dp0, dp1) = (不抢当前节点的最大金额, 抢当前节点的最大金额)
```

- `dp0 = max(left.dp0, left.dp1) + max(right.dp0, right.dp1)`
- `dp1 = node.val + left.dp0 + right.dp0`

这样每个子树只计算一次，整个过程是 **一次遍历**。

> 类比：把每棵子树看成一本“小字典”，键是“是否抢”，值是对应的最大收益。我们只需要查一次字典，就能得到答案。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def rob(root: TreeNode) -> int:
    """后序DFS + 动态规划，返回根节点能够得到的最大金额"""

    def dfs(node: TreeNode):
        """
        返回 (不抢 node, 抢 node) 两种情况下的最大金额
        - 不抢 node：左右子树可以自由选择抢或不抢，取最大值
        - 抢 node：左右子树必须不抢
        """
        if not node:
            # 空节点，无论抢不抢，收益都是 0
            return (0, 0)

        # 先递归左右子树，得到它们的 dp 值
        left_not, left_yes = dfs(node.left)
        right_not, right_yes = dfs(node.right)

        # 当前节点不抢：左右子树各自取最大值
        not_rob = max(left_not, left_yes) + max(right_not, right_yes)

        # 当前节点抢：只能加上左右子树在“不抢”状态下的收益
        rob_it = node.val + left_not + right_not

        return (not_rob, rob_it)

    # 最终答案是根节点“抢”或“不抢”两种情况的最大值
    return max(dfs(root))
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 每个节点只访问一次，做常数次算术运算。相比暴力的指数级，快了很多。  
- **空间复杂度**：`O(h)` —— 递归栈深度仍然是树的高度 `h`（最坏 `O(n)`），但不再有额外的记忆化表，只是每层返回一个长度为 2 的元组。

---

## 心得

- **核心技巧**：在树形结构上使用「**状态压缩的动态规划**」——对每个节点保存「抢」与「不抢」两种状态的最优值。  
- **适用的题型**  
  1. **House Robber III**（二叉树抢劫）  
  2. **Maximum Independent Set on Tree**（树的最大独立集）  
  3. **Binary Tree Cameras**（二叉树摄像头）——同样需要为每个节点维护多种状态。  
- **一句话总结**：把「抢」或「不抢」当成节点的两种“身份”，用后序遍历一次性算出每种身份的最优收益。

## 反思

- **第一反应**：看到「不能抢相邻的父子」就想到「相邻不能同时选」的约束，联想到「打家劫舍」的线性 DP，于是尝试把树「摊平」成链表。  
- **最容易踩的坑**  
  1. **重复计算**：没有记忆化导致指数级时间。  
  2. **忘记处理空节点**：递归返回的默认值必须是 `(0,0)`，否则会出现 `None` 加法错误。  
  3. **返回值顺序**：一定要保持「不抢、抢」的顺序一致，否则合并左右子树时会出错。  
- **下次遇到同类题**：第一步先**划分状态**（当前节点是否被选），再**后序遍历**把子树的状态合并。这样可以立刻把问题从「暴力搜索」转化为「线性 DP」。