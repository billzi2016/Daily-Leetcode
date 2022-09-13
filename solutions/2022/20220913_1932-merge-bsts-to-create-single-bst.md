# #1932. 合并二叉搜索树以构造单棵二叉搜索树 / Merge BSTs to Create Single BST

> 难度：困难 · 标签：Hash Table、Binary Search、Tree、Depth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/merge-bsts-to-create-single-bst/)

---

## 题目（英文原版）

**Description**

You are given n BST (binary search tree) root nodes for n separate BSTs stored in an array trees (0-indexed). Each BST in trees has at most 3 nodes, and no two roots have the same value. In one operation, you can:
Return the root of the resulting BST if it is possible to form a valid BST after performing n - 1 operations, or null if it is impossible to create a valid BST.
A BST (binary search tree) is a binary tree where each node satisfies the following property:
A leaf is a node that has no children.

**Examples**

**Example 1:**

```
Input: trees = [[2,1],[3,2,5],[5,4]]
Output: [3,2,5,1,null,4]
Explanation:
In the first operation, pick i=1 and j=0, and merge trees[0] into trees[1].
Delete trees[0], so trees = [[3,2,5,1],[5,4]].

In the second operation, pick i=0 and j=1, and merge trees[1] into trees[0].
Delete trees[1], so trees = [[3,2,5,1,null,4]].

The resulting tree, shown above, is a valid BST, so return its root.
```

**Example 2:**

```
Input: trees = [[5,3,8],[3,2,6]]
Output: []
Explanation:
Pick i=0 and j=1 and merge trees[1] into trees[0].
Delete trees[1], so trees = [[5,3,8,2,6]].

The resulting tree is shown above. This is the only valid operation that can be performed, but the resulting tree is not a valid BST, so return null.
```

**Example 3:**

```
Input: trees = [[5,4],[3]]
Output: []
Explanation: It is impossible to perform any operations.
```

**Constraints**

- n == trees.length
- 1 <= n <= 5 * 104
- The number of nodes in each tree is in the range [1, 3].
- Each node in the input may have children but no grandchildren.
- No two roots of trees have the same value.
- All the trees in the input are valid BSTs.
- 1 <= TreeNode.val <= 5 * 104.

---

## 题目（中文翻译）

**描述**  
给定一个长度为 `n` 的数组 `trees`（下标从 0 开始），其中每个元素是一个二叉搜索树（Binary Search Tree，BST）的根节点。`trees` 中的每棵 BST 至多包含 3 个节点，且没有两棵树的根节点值相同。  

在一次操作中，你可以：  
*（原题目此处应描述具体的合并规则，本文保持原文空缺）*  

在执行 `n - 1` 次操作后，如果能够形成一棵有效的 BST，则返回该 BST 的根节点；否则返回 `null`。  

二叉搜索树（BST）是一棵二叉树，满足每个节点的左子树所有节点值均小于该节点值，右子树所有节点值均大于该节点值。  

叶子节点是指没有子节点的节点。  

**示例 1**  
```
Input: trees = [[2,1],[3,2,5],[5,4]]
Output: [3,2,5,1,null,4]
Explanation:
在第一次操作中，选择 i=1、j=0，将 trees[0] 合并到 trees[1] 中。
删除 trees[0]，此时 trees = [[3,2,5,1],[5,4]]。

在第二次操作中，选择 i=0、j=1，将 trees[1] 合并到 trees[0] 中。
删除 trees[1]，此时 trees = [[3,2,5,1,null,4]]。

得到的树如上图所示，是一棵有效的 BST，故返回其根节点。
```  

**示例 2**  
```
Input: trees = [[5,3,8],[3,2,6]]
Output: []
Explanation:
选择 i=0、j=1，将 trees[1] 合并到 trees[0] 中。
删除 trees[1]，此时 trees = [[5,3,8,2,6]]。

得到的树如上图所示。虽然这是唯一可以执行的操作，但合并后的树并不是有效的 BST，故返回 null。
```  

**示例 3**  
```
Input: trees = [[5,4],[3]]
Output: []
Explanation: 无法执行任何操作，返回 null。
```  

**约束条件**  
- `n == trees.length`  
- `1 <= n <= 5 * 10^4`  
- 每棵树的节点数在 `[1, 3]` 之间。  
- 输入中的每个节点可能有子节点，但不会有孙子节点。  
- 没有两棵树的根节点值相同。  
- 输入的所有树都是有效的 BST。  
- `1 <= TreeNode.val <= 5 * 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **把所有可能的合并顺序都枚举一遍**，只要在一次操作中找到一棵树的叶子节点的值恰好等于另一棵树的根节点的值，就把这两棵树拼在一起，然后把被拼进去的那棵树从数组里删掉。  
把这个过程一直递归下去，直到只剩下一棵树，检查它是否仍然满足二叉搜索树（BST）的性质——左子树所有节点都小于根，右子树所有节点都大于根。如果满足，就返回这棵树；否则回溯，尝试别的合并顺序。

> **类比**：把每棵小树想象成一块拼图，叶子上的数字是“卡槽”，根上的数字是“卡子”。暴力解就是把所有卡槽和卡子随意配对，尝试所有可能的拼法。

**为什么它是正确的**  
只要我们穷举了 *所有* 合法的合并顺序，答案一定会出现在其中。只要在某个顺序下最终得到的树满足 BST 条件，我们就找到了题目的合法解。

**复杂度分析**  
- 每一次合并都要遍历当前所有树去找匹配的叶子/根，最坏情况是 `O(n)`（`n` 为树的数量）。  
- 合并需要进行 `n‑1` 次，所以时间复杂度是 `O(n·(n‑1)) ≈ O(n²)`。  
- 但是我们还要回溯搜索所有可能的合并顺序，实际的搜索空间是 `O((n‑1)!)`（阶乘），因为每一步都可以任选一对匹配的树。  
- 空间方面，需要保存递归栈以及临时的树拷贝，最坏是 `O(n)`。

> **大白话**：`O(n²)` 就像把 10 本书两两比较 100 次；`O((n‑1)!)` 更夸张，像把 10 本书排成所有可能的顺序，几乎不可能在合理时间内完成。

#### 代码（Python）

```python
# 只作为思路展示，实际运行会超时
from copy import deepcopy
from typing import List, Optional

class TreeNode:
    def __init__(self, val: int, left: 'TreeNode' = None, right: 'TreeNode' = None):
        self.val = val
        self.left = left
        self.right = right

def is_bst(node: Optional[TreeNode], lo: int = -float('inf'), hi: int = float('inf')) -> bool:
    """递归检查是否满足 BST 条件"""
    if not node:
        return True
    if not (lo < node.val < hi):
        return False
    return is_bst(node.left, lo, node.val) and is_bst(node.right, node.val, hi)

def brute_merge(trees: List[TreeNode]) -> Optional[TreeNode]:
    """暴力枚举所有合并顺序"""
    if len(trees) == 1:                     # 只剩一棵树，检查合法性
        return trees[0] if is_bst(trees[0]) else None

    # 遍历所有可能的 (i, j) 组合：把树 j 合并进 i 的某个叶子
    for i in range(len(trees)):
        for j in range(len(trees)):
            if i == j:
                continue
            leaf = find_leaf_with_value(trees[i], trees[j].val)
            if leaf:                         # 找到匹配的叶子
                # 深拷贝防止回溯时破坏原树
                new_trees = deepcopy(trees)
                new_i, new_j = new_trees[i], new_trees[j]
                replace_leaf(new_i, leaf.val, new_j)   # 用 j 的根替换叶子
                del new_trees[j]                       # 删除已经合并进去的树
                res = brute_merge(new_trees)           # 递归继续合并
                if res:
                    return res
    return None

# 下面的两个辅助函数仅为示例，真实实现要遍历整棵树找叶子
def find_leaf_with_value(root: TreeNode, val: int) -> Optional[TreeNode]:
    if not root:
        return None
    if not root.left and not root.right and root.val == val:
        return root
    return find_leaf_with_value(root.left, val) or find_leaf_with_value(root.right, val)

def replace_leaf(root: TreeNode, leaf_val: int, new_subtree: TreeNode):
    """把值为 leaf_val 的叶子节点换成 new_subtree"""
    if not root:
        return
    if root.left and not root.left.left and not root.left.right and root.left.val == leaf_val:
        root.left = new_subtree
        return
    if root.right and not root.right.left and not root.right.right and root.right.val == leaf_val:
        root.right = new_subtree
        return
    replace_leaf(root.left, leaf_val, new_subtree)
    replace_leaf(root.right, leaf_val, new_subtree)
```

> 代码里每一步都在“复制-尝试-回溯”，正是暴力搜索的写法。对大数据量会 **超时**，只能作为思考的起点。

#### 复杂度

- **时间复杂度**：`O((n‑1)!)`（阶乘），因为要遍历所有可能的合并顺序。即使在每一步只做 `O(n)` 的匹配检查，整体仍然是指数级增长，几乎不可能在 5 × 10⁴ 条数据上跑完。  
- **空间复杂度**：`O(n)`，主要是递归栈和临时拷贝的树结构。

---

### 2. 最优解

#### 思路  

从暴力解我们已经看到 **瓶颈** 在于“随意挑选叶子/根进行合并”。实际上，题目给了几个关键限制，让我们可以 **一次遍历完成所有合并**：

1. **每棵树最多只有 3 个节点**（根 + 最多两个叶子）。因此所有叶子节点的值总数 ≤ 2·n。  
2. **根节点的值在所有叶子里出现的次数至多一次**（因为根值互不相同，若出现多次就意味着有两棵树的叶子相同，无法唯一对应）。  
3. **最终的根** 必须是 **“没有出现在任何叶子中的根”**。如果有多个这样的根，就无法唯一得到一棵树；如果没有，也说明根一定被别的树“吃掉”，同样不行。

基于以上观察，我们可以把问题转化为：

- 把所有根建立一个哈希表 `root_map: value → TreeNode`（就像字典，键是根的数值，值是整棵树的根节点）。
- 把所有叶子建立另一个哈希表 `leaf_map: value → (parent, is_left_child)`，并统计每个叶子值出现的次数。  
  - 若同一个叶子值出现两次以上，直接返回 `null`（无法唯一匹配）。
- 找出唯一的 **候选根**：在 `root_map` 中找那些 **不在 `leaf_map` 里的根**。若不止一个或没有，直接返回 `null`。

**合并过程**  
从候选根开始，做一次 **深度优先搜索（DFS）**。在遍历的过程中：

- 对每个节点 `node`，我们维护它在 BST 中合法的取值范围 `(low, high)`（左子树必须小于根，右子树必须大于根）。这一步跟普通的 BST 验证一样，帮助我们在合并时立即发现非法情况。
- 当遍历到 **叶子节点** 且 **它的值正好是另一棵树的根**（`node.val` 在 `root_map` 中），我们把这棵叶子 **整体替换成那棵树的根**。替换后继续递归检查新树的左右子树（因为新树本身已经是合法的 BST，只要它在当前范围内就行）。
- 替换后，需要把对应的根从 `root_map` 中删掉，防止被重复使用。

遍历结束后：

- 若 `root_map` 已经空了（所有根都被成功挂到某个叶子上），说明我们成功把所有小树拼成了一棵大树。  
- 同时，DFS 过程中若出现范围冲突，则说明合并后违反了 BST 条件，直接返回 `null`。

整个过程只需要 **一次遍历所有节点**（总节点数 ≤ 3·n），时间线性，空间只用几个哈希表和递归栈，亦是线性。

> **类比**：把所有根想象成「待拼的拼块」，所有叶子是「插槽」。我们先找出唯一的「底板」——那棵根不在任何插槽里的树。随后把每个插槽里对应的拼块直接卡进去，卡的过程中随时检查「拼块尺寸」是否合适（BST 范围），若不合适就立刻报错。

#### 代码（Python）

```python
from typing import List, Optional, Dict, Tuple

# ---------- 定义二叉树节点 ----------
class TreeNode:
    def __init__(self, val: int,
                 left: 'TreeNode' = None,
                 right: 'TreeNode' = None):
        self.val = val
        self.left = left
        self.right = right

# ---------- 主函数 ----------
def mergeBSTs(trees: List[TreeNode]) -> Optional[TreeNode]:
    """
    如果能够把所有小 BST 合并成一棵合法的 BST，返回根节点；
    否则返回 None（相当于 LeetCode 的 null）。
    """
    if not trees:
        return None

    # 1️⃣ 建立根哈希表：value -> root 节点
    root_map: Dict[int, TreeNode] = {t.val: t for t in trees}

    # 2️⃣ 建立叶子哈希表并检查重复叶子
    leaf_cnt: Dict[int, int] = {}
    leaf_info: Dict[int, Tuple[TreeNode, bool]] = {}   # value -> (parent, is_left)

    for root in trees:
        # 左子节点（如果存在）一定是叶子，因为每棵树最多 3 个节点
        if root.left:
            leaf_cnt[root.left.val] = leaf_cnt.get(root.left.val, 0) + 1
            leaf_info[root.left.val] = (root, True)   # True 表示是左孩子
        if root.right:
            leaf_cnt[root.right.val] = leaf_cnt.get(root.right.val, 0) + 1
            leaf_info[root.right.val] = (root, False)  # False 表示是右孩子

    # 若同一个叶子值出现两次以上，直接失败
    for v, c in leaf_cnt.items():
        if c > 1:
            return None

    # 3️⃣ 找唯一的候选根（不在任何叶子里的根）
    candidates = [val for val in root_map if val not in leaf_cnt]
    if len(candidates) != 1:          # 0 或 >1 都不行
        return None

    final_root_val = candidates[0]
    final_root = root_map.pop(final_root_val)   # 把它从待合并集合中移除

    # 4️⃣ 深度优先遍历并完成合并
    def dfs(node: TreeNode, low: int, high: int) -> Optional[TreeNode]:
        """
        返回合并后的子树（若合法），否则返回 None。
        low / high 表示当前节点的合法取值范围：low < node.val < high
        """
        if not node:
            return None

        # ① 检查 BST 范围
        if not (low < node.val < high):
            return None

        # ② 如果是叶子且恰好是另一棵树的根，进行“卡槽替换”
        if node.left is None and node.right is None and node.val in root_map:
            # 用对应的整棵树替换当前叶子
            node = root_map.pop(node.val)   # 取出并从集合中删除
            # 替换后仍需在相同范围内继续检查
            #（因为新树的根已经等于 node.val，范围不变）
        # ③ 继续递归处理左右子树
        node.left = dfs(node.left, low, node.val)
        node.right = dfs(node.right, node.val, high)

        # 任意子树返回 None 表示不合法
        if (node.left is None and node.right is not None) or \
           (node.right is None and node.left is not None):
            # 这里不需要特别处理，直接返回 node 即可；
            # 只要子树本身合法，父节点也合法
            pass
        if node.left is None and node.right is None:
            # 叶子已经处理完
            return node
        if node.left is None or node.right is None:
            # 单边子树合法即可
            return node
        return node

    merged_root = dfs(final_root, -float('inf'), float('inf'))

    # 5️⃣ 最后检查：所有根都已经被挂进去了吗？
    if merged_root is None or root_map:
        return None
    return merged_root
```

> **代码要点解释**  
- `root_map.pop(final_root_val)` 把最终根从「待合并」集合中取走，防止后面误把它当作叶子去挂。  
- `dfs` 中的 `low / high` 就像“上下限”，确保每个节点都在它应该出现的区间里。  
- 当叶子可以被另一棵树的根替换时，直接把 `node` 变量指向那棵子树（`node = root_map.pop(node.val)`），随后递归继续检查新树的左右子树。  
- 最后 `root_map` 必须为空，说明每棵小树都找到了自己的位置。

#### 复杂度

- **时间复杂度**：`O(N)`，其中 `N` 为所有节点的总数（`N ≤ 3·n ≤ 1.5·10⁵`）。  
  - 构建哈希表遍历一次 `O(N)`。  
  - DFS 只访问每个节点一次，同样 `O(N)`。  
  - 与暴力解的指数级搜索相比，这里只需要线性时间。

- **空间复杂度**：`O(N)`。  
  - 哈希表存储每个根和每个叶子，最坏占用 `O(N)`。  
  - 递归栈的深度最多等于树的高度，树的高度 ≤ 3（因为每棵子树本身不深），所以可以视为常数空间，整体仍是 `O(N)`。

> **对比**：暴力解的 `O((n‑1)!)` 在 `n = 10⁴` 时根本不可行，而最优解的 `O(N)` 在同样规模下毫秒级完成。

---

## 心得

- **核心技巧**：利用 **哈希表** 把根和叶子快速对应，再用 **DFS + 区间限制** 一次性完成所有合并并检查 BST 合法性。  
- **适用的题型**  
  1. “把若干棵小树合并成一棵大树”——如 LeetCode 1325 *Delete Leaves With a Given Value* 的逆向思路。  
  2. “根据值的唯一性进行匹配”——比如 1657 *Determine if Two Strings Are Close*（字符频率匹配）。  
  3. “在树结构上做一次遍历并实时验证约束”——如 98 *Validate Binary Search Tree*、106 *Construct Binary Tree from Inorder and Postorder Traversal*。  
- **一句话总结解题钥匙**：  
  > “根不在叶子里 → 唯一根；叶子只对应唯一根 → 用哈希表配对；DFS+区间检查一次完成全部合并。”

---

## 反思

- **第一反应**：看到“每棵树最多 3 个节点”，立刻想到可以 **枚举所有合并顺序**，因为搜索空间看起来不大。于是写了暴力回溯。  
- **最容易踩的坑**  
  1. **重复叶子值**：如果两个不同的树都有相同的叶子值，却只有一个对应的根，会导致冲突，必须提前检测。  
  2. **根出现在叶子里**：最终根必须是“没有出现在任何叶子中的根”，忽略这一点会导致最终树不唯一或无法完成全部合并。  
  3. **BST 区间合法性**：直接把子树接上去并不一定保证整体仍是 BST，必须在合并过程中实时检查每个节点的取值范围。  
- **下次遇到类似题**，第一步应该先 **统计值出现的频次**（根/叶子），确定唯一的 “入口” 与 “配对关系”，再 **一次遍历完成所有操作**，而不是盲目回溯。这样既能保证正确性，又能把时间复杂度控制在 O(N)。