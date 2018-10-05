# #124. 二叉树最大路径和 / Binary Tree Maximum Path Sum

> 难度：困难 · 标签：Dynamic Programming、Tree、Depth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/binary-tree-maximum-path-sum/)

---

## 题目（英文原版）

**Description**

A path in a binary tree is a sequence of nodes where each pair of adjacent nodes in the sequence has an edge connecting them. A node can only appear in the sequence at most once. Note that the path does not need to pass through the root.
The path sum of a path is the sum of the node's values in the path.
Given the root of a binary tree, return the maximum path sum of any non-empty path.

**Examples**

**Example 1:**

```
Input: root = [1,2,3]
Output: 6
Explanation: The optimal path is 2 -> 1 -> 3 with a path sum of 2 + 1 + 3 = 6.
```

**Example 2:**

```
Input: root = [-10,9,20,null,null,15,7]
Output: 42
Explanation: The optimal path is 15 -> 20 -> 7 with a path sum of 15 + 20 + 7 = 42.
```

**Constraints**

- The number of nodes in the tree is in the range [1, 3 * 104].
- -1000 <= Node.val <= 1000

---

## 题目（中文翻译）

路径（path）在二叉树（binary tree）中是由一系列节点组成，序列中相邻的每一对节点之间都有一条边相连。每个节点在序列中至多出现一次。需要注意的是，路径不一定要经过根节点（root）。  
路径和（path sum）指的是路径上所有节点值的总和。  
给定一棵二叉树的根节点，返回任意非空路径（non‑empty path）的最大路径和。

**示例 1**  
**示例 2**  
**约束条件**  

### 示例

#### 示例 1
**Input:** `root = [1,2,3]`  
**Output:** `6`  
**Explanation:** 最优路径为 `2 -> 1 -> 3`，其路径和为 `2 + 1 + 3 = 6`。

#### 示例 2
**Input:** `root = [-10,9,20,null,null,15,7]`  
**Output:** `42`  
**Explanation:** 最优路径为 `15 -> 20 -> 7`，其路径和为 `15 + 20 + 7 = 42`。

### 约束条件
- 树中节点的数量范围为 `[1, 3 * 10^4]`。
- `-1000 <= Node.val <= 1000`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把「所有可能的路径」都枚举一遍，然后求出每条路径的和，取最大值。  
在二叉树里，一条合法路径的特点是：

* 相邻的两个节点之间必须有边相连（左子树、右子树或父子关系）。
* 同一个节点在同一条路径里只能出现一次（不能走回头路）。
* 路径不一定要经过根节点。

**暴力做法**：

1. 对树里的每一个节点 `node`，把它当作「路径的起点」。
2. 从 `node` 出发，使用深度优先搜索（DFS）遍历所有能走到的节点，记录遍历过程中累计的和。  
   - 为了不走回头，我们在递归时把「上一次走来的节点」记下来，下一层搜索时不再回到它。
3. 把从这个起点得到的最大累计和与全局答案比较，更新全局最大。
4. 对所有节点重复步骤 1~3，最终的全局最大就是答案。

> **类比**：把树想象成一座城市的道路网络，每个交叉口是节点。暴力解相当于把每个交叉口都当作出发点，穷举所有不走回头的行走路线，记下最高的「收益」。

**为什么正确**：  
因为我们遍历了**所有**可能的起点以及从该起点出发的**所有**合法路径，必然能覆盖题目要求的「任意非空路径」，因此最大值一定被找到。

**复杂度分析**：

- 对每个节点都要做一次完整的 DFS，DFS 的遍历量与树的节点数 `N` 成正比。于是时间复杂度是 `O(N²)`（最坏情况是链状树，每次 DFS 要遍历几乎全部节点）。  
  - **大白话**：如果树有 10,000 个节点，暴力解大概要跑 10,000 × 10,000 = 1 亿次「访问」——会慢到让人等不及。
- 递归栈深度最多 `O(N)`，再加上常数级的额外变量，空间复杂度是 `O(N)`（主要是递归调用占用的栈空间）。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的数值
        self.left = left        # 左子树
        self.right = right      # 右子树


def maxPathSum_bruteforce(root: TreeNode) -> int:
    """暴力解：枚举所有起点并从起点进行全遍历"""

    # 全局最大路径和（使用列表是因为 Python 在内部函数里需要 nonlocal）
    ans = [-float('inf')]

    # --------- 第一步：遍历所有节点，作为起点 ----------
    def traverse_all(node: TreeNode):
        if not node:
            return
        # 以当前 node 为起点，计算所有不回头的路径和
        dfs_from(node, None, 0)
        # 继续把左、右子树的节点也作为起点
        traverse_all(node.left)
        traverse_all(node.right)

    # --------- 第二步：从某个起点出发的 DFS ----------
    def dfs_from(cur: TreeNode, parent: TreeNode, cur_sum: int):
        """
        cur: 当前所在的节点
        parent: 上一次来的节点（用来防止回头）
        cur_sum: 到达 cur 前累计的路径和
        """
        # 把当前节点加入路径
        cur_sum += cur.val
        # 更新全局答案
        ans[0] = max(ans[0], cur_sum)

        # 向左子树继续走（如果左子树不是我们来的方向）
        if cur.left and cur.left != parent:
            dfs_from(cur.left, cur, cur_sum)
        # 向右子树继续走
        if cur.right and cur.right != parent:
            dfs_from(cur.right, cur, cur_sum)

    # 调用入口
    traverse_all(root)
    return ans[0]
```

#### 复杂度

- **时间复杂度**：`O(N²)`  
  - 这里的 `N` 是树的节点数。因为对每个节点都要进行一次遍历，最坏情况下每次遍历会遍历到几乎所有节点。
- **空间复杂度**：`O(N)`  
  - 递归栈的最大深度等于树的高度，最坏是 `N`（链状树），其余只用了常数级的额外空间。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**大量的重复遍历**：同一条子树会被不同的起点反复搜索。  
我们需要一种方式，让每个节点只被「处理」一次，同时把它能贡献的最大路径信息「向上」传递给父节点。

**关键观察**：

1. 对于任意节点 `node`，如果我们只关心「以 `node` 为路径的 **起点**，且路径只能往下走（不能转向父节点）」的最大和，这个值只跟 `node` 的左右子树的「向下最大贡献」有关。
2. 设 `gain(node)` 为「从 `node` 往下走，能够得到的最大路径和」，但我们**可以选择不走**左/右子树（因为子树的贡献可能是负的），所以  
   `gain(node) = node.val + max(0, gain(node.left)) + max(0, gain(node.right))`  
   这里的 `max(0, ...)` 表示「如果子树贡献是负的，就不选它」。
3. 当我们在某个节点 `node` 计算 `gain(node)` 时，实际上已经得到了一条「**以 `node` 为最高点**」的完整路径的和——它可能左子树贡献 + `node.val` + 右子树贡献。这个路径不需要继续往上延伸，因为再往上会导致「拐弯」两次（左 → node → 右 → 父），违背路径只能出现一次的规则。
4. 因此，在后序遍历（左 → 右 → 根）的过程中，**每访问一个节点**，我们可以：
   - 计算左、右子树各自的 `gain`（递归返回值）。
   - 用这两个 `gain` 计算「以该节点为最高点的路径和」并更新全局最大。
   - 把 `node.val + max(0, left_gain) + max(0, right_gain)` 作为 **向父节点返回的最大向下贡献**（只能选左或右其中一条继续向上）。

这就是典型的「树形 DP」或「后序遍历 + 递归返回值」的思路，时间只需要一次遍历。

> **类比**：把每棵子树想象成一个小工厂，`gain` 就是这家工厂向外输出的最大利润。父工厂只会挑选利润为正的子工厂继续合作，负利润的子工厂直接丢掉。每次合并后，父工厂还能记录一次「全公司最高利润」的快照。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def maxPathSum(root: TreeNode) -> int:
    """最优解：后序遍历 + 树形 DP，一遍 O(N)"""

    # 用列表保存全局最大值，便于在内部函数里修改
    max_sum = [-float('inf')]

    def dfs(node: TreeNode) -> int:
        """
        返回值：从 node 往下走，能够得到的最大贡献（可以为 0，表示不选任何子树）。
        同时在函数内部更新全局 max_sum。
        """
        if not node:
            return 0  # 空节点对路径和没有贡献

        # 递归求左、右子树的最大向下贡献
        left_gain = max(dfs(node.left), 0)   # 若左子树贡献为负，则取 0（不选左子树）
        right_gain = max(dfs(node.right), 0) # 同理处理右子树

        # 以当前节点为最高点的路径和（左 + node + 右）
        price_through_node = node.val + left_gain + right_gain

        # 更新全局答案
        max_sum[0] = max(max_sum[0], price_through_node)

        # 返回给父节点的最大向下贡献：只能选左或右其中一条继续向上
        return node.val + max(left_gain, right_gain)

    dfs(root)          # 从根节点启动后序遍历
    return max_sum[0]  # 最终的全局最大即为答案
```

#### 复杂度

- **时间复杂度**：`O(N)`  
  - 每个节点只被访问一次，所有计算都是常数时间。相比暴力的 `O(N²)`，大幅提升速度。  
  - **大白话**：如果树有 10,000 个节点，最优解只需要大约 10,000 次「访问」，几乎是瞬间完成。
- **空间复杂度**：`O(H)`，其中 `H` 是树的高度。递归栈深度等于树的层数，最坏情况（链状树）是 `O(N)`，平衡树则是 `O(log N)`。额外的存储只有一个全局变量 `max_sum`，是常数级。

---

## 心得

- **核心技巧**：**树形动态规划 + 后序遍历**。在遍历的同时把「向下的最大贡献」向上返回，同时维护「经过当前节点的完整路径最大和」。
- **适用的题型**  
  1. **Maximum Path Sum**（本题）  
  2. **Binary Tree Maximum Sum of Non‑Overlapping Paths**（类似的需要在子树内部维护全局最优）  
  3. **Maximum Sum BST Subtree**（在每个子树内部计算信息并向上合并）
- **一句话总结**：**把每棵子树看成一个「只会输出正利润」的工厂，递归返回最大正向贡献，同时记录所有工厂合并后出现的最高利润**。

---

## 反思

- **第一反应**：直接想到「枚举所有路径」——这在没有经验时是最自然的想法，但会导致超时。
- **最容易踩的坑**  
  1. **负数节点**：如果直接把左、右子树的贡献相加而不做 `max(0, ...)` 处理，负值会把整体路径和拉低。  
  2. **返回值只能选一条向上**：在递归返回时只能选择左或右中较大的那条，不能把左右都带上，否则会出现「拐弯两次」的非法路径。  
  3. **全局答案的更新位置**：必须在「经过当前节点的完整路径」计算后立即更新，而不是只在返回值里更新，否则会漏掉以当前节点为最高点的情况。
- **下次遇到同类题**，第一步应该思考「**每个子结构（子树）能提供什么信息给父结构**」，并尝试用**后序遍历**一次性收集并合并这些信息，而不是暴力枚举。这样往往能把时间从 `O(N²)` 降到 `O(N)`。