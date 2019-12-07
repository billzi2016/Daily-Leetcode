# #687. 最长同值路径 / Longest Univalue Path

> 难度：中等 · 标签：Tree、Depth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/longest-univalue-path/)

---

## 题目（英文原版）

**Description**

Given the root of a binary tree, return the length of the longest path, where each node in the path has the same value. This path may or may not pass through the root.
The length of the path between two nodes is represented by the number of edges between them.

**Examples**

**Example 1:**

```
Input: root = [5,4,5,1,1,null,5]
Output: 2
Explanation: The shown image shows that the longest path of the same value (i.e. 5).
```

**Example 2:**

```
Input: root = [1,4,5,4,4,null,5]
Output: 2
Explanation: The shown image shows that the longest path of the same value (i.e. 4).
```

**Constraints**

- The number of nodes in the tree is in the range [0, 104].
- -1000 <= Node.val <= 1000
- The depth of the tree will not exceed 1000.

---

## 题目（中文翻译）

给定一棵二叉树（binary tree）的根节点（root），返回其中**最长同值路径**的长度，即路径上所有节点（node）的值都相同。该路径可以经过根节点，也可以不经过根节点。  
路径的长度用路径中 **边（edge）** 的数量来表示。

**示例 1**  

**示例 2**  

**约束条件**  

- 树中节点的数量在 `[0, 10^4]` 区间内。  
- `-1000 ≤ Node.val ≤ 1000`  
- 树的深度不会超过 `1000`。

**示例**

**示例 1**  
```
Input: root = [5,4,5,1,1,null,5]
Output: 2
Explanation: 如图所示，最长的同值路径的值为 5，长度为 2（包含两条相同值的边）。
```

**示例 2**  
```
Input: root = [1,4,5,4,4,null,5]
Output: 2
Explanation: 如图所示，最长的同值路径的值为 4，长度为 2（包含两条相同值的边）。
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把树的每一个节点都当作「路径的中点」**，然后从这个节点向左、向右分别往下走，只要遇到的节点值和中点相同，就继续往下。把左边最长的同值链和右边最长的同值链相加，就得到以该节点为「拐点」的同值路径长度。  

- **用到的数据结构**：  
  - 二叉树的节点 `TreeNode`（就像一本书的章节，每个章节可能有左子章节和右子章节）。  
  - 递归（相当于让小朋友去每个子章节重复同样的查找任务）。  

- **为什么正确**：  
  对于任意一条同值路径，它必定有一个「最靠近根节点」的节点。把这条路径的这条「最靠近根」的节点记作 `center`，那么这条路径一定是 `center` 往左走若干条边，再往右走若干条边（可能左边或右边为空）。所以只要把每个节点都当成 `center` 检查一次，就能找到全局最长的同值路径。

- **时间/空间复杂度**：  
  - 对每个节点我们都要**遍历它的整棵子树**来找同值链的长度，最坏情况（所有节点值都相同）下，遍历次数是 `1 + 2 + 3 + … + N = O(N²)`，这里的 `N` 是节点数。  
  - 递归调用栈的深度最多等于树的高度，最坏是 `O(N)`（链状树），但在暴力实现里我们还会在每次遍历时产生新的递归栈，整体空间仍是 `O(N)`。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的数值
        self.left = left        # 左子树
        self.right = right      # 右子树


def longestUnivaluePath(root: TreeNode) -> int:
    """暴力解：对每个节点都做一次完整的同值深度搜索"""
    if not root:
        return 0

    # 计算以 node 为根，向下只能走同值边的最长链（返回边数）
    def dfs_same(node, target):
        if not node or node.val != target:
            return 0
        # 左右子树各走一步再继续
        left_len = dfs_same(node.left, target)
        right_len = dfs_same(node.right, target)
        # 只取较长的一条，因为这里只能走成“一条线”
        return 1 + max(left_len, right_len)

    # 以当前节点为中心的同值路径长度 = 左边最长 + 右边最长（边数）
    left = dfs_same(root.left, root.val)   # 左子树向下的同值链（边数）
    right = dfs_same(root.right, root.val) # 右子树向下的同值链（边数）
    # 这里的路径长度是边的数量，所以不需要再 +1
    cur_path = left + right

    # 递归求左、右子树的答案，取最大
    left_best = longestUnivaluePath(root.left)
    right_best = longestUnivaluePath(root.right)

    return max(cur_path, left_best, right_best)
```

#### 复杂度

- **时间复杂度**：`O(N²)`  
  想象每个节点都要把整棵子树遍历一遍，就像在一堆书里每本书都要重新读一遍，工作量会随 `N` 的平方增长。  
- **空间复杂度**：`O(N)`  
  递归栈的深度最多等于树的高度，最坏是链状树，需要 `N` 层栈帧。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每个节点都要重复遍历它的子树**，导致大量重复计算。我们可以把「向下寻找同值链」的过程**合并到一次深度优先遍历（DFS）**里去完成。  

核心想法：

1. **后序遍历**（左→右→根），先把左右子树的答案算好，再来处理当前节点。  
2. 对每个节点，**只需要知道它左子树和右子树各自向下的最长同值链长度**（以子节点为起点，且必须和当前节点值相同）。这两个长度可以直接从子节点的递归返回值得到。  
3. 当前节点能形成的「通过它的同值路径」长度 = `left_chain + right_chain`（左、右各走多少边）。这就是以当前节点为拐点的路径。  
4. 用一个全局变量 `ans` 记录遍历过程中出现的最大路径长度。递归函数返回值是**从当前节点向下继续延伸的最长同值链长度**（只能选左或右，不能同时走两边），因为向上层节点只能选一条继续。

**类比**：把树看成一条河流的分支网络，水只能沿同一种颜色的河道继续流动。我们从最小的支流往上汇聚，记录每次汇合时两边最长的同色河段之和，就是最长的同值路径。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def longestUnivaluePath(root: TreeNode) -> int:
    """最优解：一次 DFS 完成全部统计"""
    ans = 0  # 用来保存全局最长路径的边数

    def dfs(node: TreeNode) -> int:
        """返回值：从 node 向下最长的同值链（边数），只能选左或右其中一条"""
        nonlocal ans
        if not node:
            return 0

        # 递归得到左右子树各自的最长同值链
        left_len = dfs(node.left)   # 左子树向下的同值链（边数）
        right_len = dfs(node.right) # 右子树向下的同值链（边数）

        # 只有当子节点的值和当前节点相同，才可以把这条边算进同值链
        left_arrow = right_arrow = 0   # 向左/右延伸的边数，默认 0（不延伸）

        if node.left and node.left.val == node.val:
            left_arrow = left_len + 1   # +1 表示把左边这条边计入
        if node.right and node.right.val == node.val:
            right_arrow = right_len + 1 # 同理

        # 以当前节点为拐点的同值路径长度 = 左边 + 右边（边数）
        ans = max(ans, left_arrow + right_arrow)

        # 向上传递给父节点的只能是「单边」的最长链
        return max(left_arrow, right_arrow)

    dfs(root)
    return ans
```

#### 复杂度

- **时间复杂度**：`O(N)`  
  每个节点只被访问一次，所有计算都在一次递归中完成。相当于只读一遍树的所有章节，工作量随节点数线性增长。  
- **空间复杂度**：`O(H)`，`H` 为树的高度。递归栈深度等于树的最大层数，最坏情况（链状树）是 `O(N)`，平均情况（平衡树）是 `O(log N)`。

---

## 心得

- **核心技巧**：一次后序深度优先遍历（DFS）同时返回「向下的同值链」并用全局变量记录「经过节点的同值路径」的最大值。  
- **适用的题型**：  
  1. 二叉树中求「最长同值路径」或「最长递增路径」等，需要在**子树信息合并**时更新全局答案的题目。  
  2. 「二叉树直径」(`Diameter of Binary Tree`)——思路完全相同，只是判断条件换成「任意节点」而不是「相同值」。  
  3. 「二叉树中和为指定值的最长路径」等，需要把路径信息向上回传的题目。  
- **一句话总结解题钥匙**：**后序遍历 + 子树信息合并 + 只保留单向最长链**。

---

## 反思

- **第一反应**：看到「最长同值路径」就想到「遍历每条路径」或「把每个节点当作中心」的暴力想法。  
- **最容易踩的坑**：  
  - **忘记返回的是「边数」而不是「节点数」**，导致答案多加了 1。  
  - **没有区分左、右两边是否可以继续**，导致把不相同的子树也算进了同值链。  
  - **递归返回值写成「节点数」**，会在合并时出现多余的 `+1`。  
- **下次遇到同类题**：第一步先**确定「局部信息」——从子树能向上贡献多少**，然后用**后序遍历一次性合并**，避免重复遍历。这样可以把时间复杂度从 `O(N²)` 降到 `O(N)`。