# #1448. **二叉树中好节点的计数** / Count Good Nodes in Binary Tree

> 难度：中等 · 标签：Tree、Depth-First Search、Breadth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/count-good-nodes-in-binary-tree/)

---

## 题目（英文原版）

**Description**

Given a binary tree root, a node X in the tree is named good if in the path from root to X there are no nodes with a value greater than X.
Return the number of good nodes in the binary tree.

**Examples**

**Example 1:**

```
Input: root = [3,1,4,3,null,1,5]
Output: 4
Explanation: Nodes in blue are good.
Root Node (3) is always a good node.
Node 4 -> (3,4) is the maximum value in the path starting from the root.
Node 5 -> (3,4,5) is the maximum value in the path
Node 3 -> (3,1,3) is the maximum value in the path.
```

**Example 2:**

```
Input: root = [3,3,null,4,2]
Output: 3
Explanation: Node 2 -> (3, 3, 2) is not good, because "3" is higher than it.
```

**Example 3:**

```
Input: root = [1]
Output: 1
Explanation: Root is considered as good.
```

**Constraints**

- The number of nodes in the binary tree is in the range [1, 10^5].
- Each node's value is between [-10^4, 10^4].

---

## 题目（中文翻译）

给定一棵二叉树（binary tree）`root`，如果在从根节点（root）到节点 `X` 的路径（path）上不存在值大于 `X` 的节点，则称节点 `X` 为**好节点（good node）**。返回二叉树中好节点的数量。

**示例 1**

```
Input: root = [3,1,4,3,null,1,5]
Output: 4
Explanation: 蓝色标记的节点是好节点。
- 根节点 (3) 始终是好节点。
- 节点 4 → 路径 (3,4) 中 4 为该路径的最大值。
- 节点 5 → 路径 (3,4,5) 中 5 为该路径的最大值。
- 节点 3 → 路径 (3,1,3) 中 3 为该路径的最大值。
```

**示例 2**

```
Input: root = [3,3,null,4,2]
Output: 3
Explanation: 节点 2 → 路径 (3,3,2) 中存在比 2 更大的节点 3，故 2 不是好节点。
```

**示例 3**

```
Input: root = [1]
Output: 1
Explanation: 根节点被视为好节点。
```

**约束条件**

- 二叉树中的节点数在范围 **[1, 10^5]** 内。
- 每个节点的值在 **[-10^4, 10^4]** 之间。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**对每一个节点都单独走一遍从根到它的路径，找出路径上的最大值**，然后比较这个最大值是否等于该节点的值。  
- **数据结构**：我们仍然使用二叉树的节点结构 `TreeNode`，遍历时可以用递归或显式的栈。为了“查找路径上的最大值”，可以把从根到当前节点的所有节点值存进一个列表（就像把走过的路标记下来），随后用 `max()` 求最大值。  
- **正确性**：如果路径上没有比节点 X 更大的数，那么 `max(path)` 必然等于 X 的值，说明 X 是 *good*；反之则不是。逐个检查所有节点，自然能得到答案。  

**为什么会慢**：  
- 对每个节点都重新遍历一次根到该节点的路径，最坏情况下树是“一条长链”，第 i 个节点要走 i 步，所有节点累计步数是 `1 + 2 + … + N = O(N²)`。  
- 空间上我们除了递归栈外，还要保存路径列表，最坏 `O(N)`。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def countGoodNodes_brute(root: TreeNode) -> int:
    """暴力解：对每个节点都重新算一次根到它的最大值"""
    if not root:
        return 0

    # 用来存放所有节点的计数
    good_cnt = 0

    # 先把所有节点收集到一个列表里（前序遍历）
    nodes = []

    def collect(node):
        if not node:
            return
        nodes.append(node)
        collect(node.left)
        collect(node.right)

    collect(root)

    # 对每个节点，重新走一遍根到它的路径
    for node in nodes:
        # 找到 node 的路径上的所有节点值
        path_vals = []

        def dfs(cur):
            if not cur:
                return False
            path_vals.append(cur.val)          # 记录当前节点值
            if cur is node:                     # 已经到达目标
                return True
            # 继续向左/右子树搜索，若找到了就不必继续
            if dfs(cur.left) or dfs(cur.right):
                return True
            path_vals.pop()                     # 回溯时把不在路径上的值删掉
            return False

        dfs(root)                               # 从根开始搜索
        # 路径最大值
        max_on_path = max(path_vals)
        if node.val >= max_on_path:             # 如果没有更大的，就算 good
            good_cnt += 1

    return good_cnt
```

#### 复杂度

- **时间复杂度**：`O(N²)`  
  解释：对每个节点都要重新遍历一次从根到它的路径，最坏情况（链状树）相当于 `1 + 2 + … + N` 步，等价于 `N²/2`，我们用大 O 记作 `O(N²)`。  
- **空间复杂度**：`O(N)`  
  解释：`nodes` 列表保存所有节点需要 `O(N)`，递归栈最深也可能是 `O(N)`（链状树），加起来仍是线性空间。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**重复走根到某节点的路径是浪费**。如果我们在一次深度优先遍历（DFS）中，**把“当前路径的最大值”随时带下来**，每到一个节点只需要比较一次：

1. **维护一个变量 `cur_max`**，表示从根到当前节点（包括当前节点）路径上出现的最大值。  
2. 当我们来到节点 `node` 时，**如果 `node.val >= cur_max`，说明它是 good 节点**，计数加一。  
3. 递归左子树和右子树时，把 `max(cur_max, node.val)` 作为新的 `cur_max` 传下去。  

这样每个节点只访问一次，时间是 `O(N)`，空间只需要递归栈的深度（最坏 `O(N)`，平均 `O(logN)`）。

**核心概念——前缀最大**  
想象我们在爬山，`cur_max` 就是“到目前为止最高的海拔”。只要当前海拔不低于最高海拔，就算是“好点”。这种“从左到右维护前缀最大”的思想在数组里也常见（比如寻找“记录保持者”），这里把它搬到树的路径上。

#### 代码（Python）

```python
def countGoodNodes(root: TreeNode) -> int:
    """
    最优解：一次 DFS，沿途维护路径最大值。
    返回二叉树中 good 节点的数量。
    """

    def dfs(node: TreeNode, cur_max: int) -> int:
        if not node:
            return 0                     # 空节点不计数

        # 判断当前节点是否 good
        good = 1 if node.val >= cur_max else 0

        # 更新路径最大值，传给子节点
        new_max = max(cur_max, node.val)

        # 递归左、右子树，累加计数
        left_cnt = dfs(node.left, new_max)
        right_cnt = dfs(node.right, new_max)

        return good + left_cnt + right_cnt

    # 根节点本身一定在路径上，初始最大值设为根的值
    return dfs(root, root.val)
```

#### 复杂度

- **时间复杂度**：`O(N)`  
  解释：每个节点只被访问一次，做常数次比较和递归调用，线性时间。相比暴力的 `O(N²)`，提升显著。  
- **空间复杂度**：`O(H)`，其中 `H` 为树的高度。  
  解释：递归栈的深度等于树的高度。最坏情况下（链状树）`H = N`，即 `O(N)`；如果是平衡二叉树，`H ≈ log₂N`，空间更小。

---

## 心得

- **核心技巧**：在遍历过程中**携带路径状态**（这里是路径最大值），用“前缀最大”思想把全局信息局部化。  
- **适用题型**：  
  1. “记录保持者”类问题（如 LeetCode 1448 *Count Good Nodes in Binary Tree*）。  
  2. “路径上满足某种约束”的计数，如 “路径上所有节点值均不小于某值”。  
  3. “在树/图的遍历中累计信息” 如 “最大路径和” (LeetCode 124) 或 “最长递增路径”。  
- **一句话总结**：**一次 DFS，带着“到目前为止的最大值”下去，遇到更大或相等的节点就计数**。

---

## 反思

- **第一反应**：看到“根到节点的路径上没有更大的数”，自然想到**遍历每条路径**，于是联想到暴力的“对每个节点重新走一遍路径”。  
- **最容易踩的坑**：  
  - 忘记把根节点本身计入 good 节点（根的路径最大值就是它自己）。  
  - 递归时没有更新 `cur_max`，导致后面的子树仍使用旧的最大值，答案会偏小。  
  - 对空树的处理：题目保证至少有一个节点，但写通用代码时仍需防止 `None` 的访问。  
- **下次遇到同类题**：第一步先**思考能否在一次遍历中把需要的“路径信息”沿路传递**，如果可以，就立刻构造带参数的递归或显式栈实现。这样往往能把 `O(N²)` 的暴力思路压缩到 `O(N)`。