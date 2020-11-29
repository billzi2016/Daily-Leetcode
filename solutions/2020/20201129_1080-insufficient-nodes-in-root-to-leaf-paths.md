# #1080. 根到叶子路径的不足节点 / Insufficient Nodes in Root to Leaf Paths

> 难度：中等 · 标签：Tree、Depth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/insufficient-nodes-in-root-to-leaf-paths/)

---

## 题目（英文原版）

**Description**

Given the root of a binary tree and an integer limit, delete all insufficient nodes in the tree simultaneously, and return the root of the resulting binary tree.
A node is insufficient if every root to leaf path intersecting this node has a sum strictly less than limit.
A leaf is a node with no children.

**Examples**

**Example 1:**

```
Input: root = [1,2,3,4,-99,-99,7,8,9,-99,-99,12,13,-99,14], limit = 1
Output: [1,2,3,4,null,null,7,8,9,null,14]
```

**Example 2:**

```
Input: root = [5,4,8,11,null,17,4,7,1,null,null,5,3], limit = 22
Output: [5,4,8,11,null,17,4,7,null,null,null,5]
```

**Example 3:**

```
Input: root = [1,2,-3,-5,null,4,null], limit = -1
Output: [1,null,-3,4]
```

**Constraints**

- The number of nodes in the tree is in the range [1, 5000].
- -105 <= Node.val <= 105
- -109 <= limit <= 109

---

## 题目（中文翻译）

给定一棵二叉树（binary tree）的根节点 `root` 和一个整数 `limit`，同时删除树中所有不足的节点（insufficient nodes），并返回删除后二叉树的根节点。

如果 **每条经过该节点的根到叶子路径（root to leaf path）的路径和** 都严格小于 `limit`，则该节点被视为不足的。  
叶子（leaf）指的是没有子节点的节点。

**示例 1：**  
Input: `root = [1,2,3,4,-99,-99,7,8,9,-99,-99,12,13,-99,14], limit = 1`  
Output: `[1,2,3,4,null,null,7,8,9,null,14]`

**示例 2：**  
Input: `root = [5,4,8,11,null,17,4,7,1,null,null,5,3], limit = 22`  
Output: `[5,4,8,11,null,17,4,7,null,null,null,5]`

**示例 3：**  
Input: `root = [1,2,-3,-5,null,4,null], limit = -1`  
Output: `[1,null,-3,4]`

**约束条件：**
- 树中节点的数量在区间 `[1, 5000]` 内。
- `-10^5 <= Node.val <= 10^5`
- `-10^9 <= limit <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**对每一条根到叶子的路径**都计算一次路径和，然后把所有 **和 < limit** 的路径上的节点全部删掉。  
可以把树看成一张“道路网络”，每条从根出发一直走到没有分叉的终点（叶子）的路就是一条“路径”。  
我们把每条路径的“总收入”累加起来，如果这条路的收入小于公司要求的 `limit`，那么这条路上所有的“站点”（节点）都要被裁掉。

实现上可以：

1. 用一次 **深度优先搜索（DFS）** 把所有根到叶子的路径收集到一个列表 `paths`，每条路径用节点指针的列表表示。  
2. 对每条路径求和，判断是否满足 `limit`。  
3. 把不满足的路径对应的节点标记为 “需要删除”。  
4. 再遍历一次树，把标记好的节点真的从父节点的左/右指针上去掉。

> **为什么正确**  
> 如果一条根到叶子的路径的总和 < limit，则这条路径上 **每一个** 节点在 **所有** 经过它的路径中（这里唯一的一条）都不满足要求，按照题意它们都是 *insufficient*，必须被删除。相反，只要节点所在的 **任意** 一条路径满足 `sum >= limit`，它就不是 *insufficient*，不应被删掉。暴力方法正是逐条检查所有路径，保证了这一点。

> **复杂度分析（大白话）**  
> - 假设树有 `n` 个节点。最坏情况下树是一条长链，根到叶子只有一条路径，收集路径本身是 O(n)。  
> - 但如果树是完全二叉树，根到叶子有约 `n/2` 条路径，每条路径长度约 `log₂ n`。我们要把每条路径都遍历一遍求和，时间大约是 `路径数 × 路径长 ≈ (n/2) * log₂ n`，仍然在 **O(n log n)**。  
> - 由于我们还要把每条路径上的节点标记并再次遍历整棵树，最坏会出现 **每个节点被访问多次**，在最不平衡的情况下会退化到 **O(n²)**（每个节点都在很多不同的路径上出现）。  
> - 空间上，需要存储所有路径，最坏情况是每条路径都占用 O(log n) 空间，总共 O(n log n) 的额外空间。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def insufficientNodes_bruteforce(root: TreeNode, limit: int) -> TreeNode:
    # 1. 收集所有根到叶子的路径（用节点指针列表表示）
    all_paths = []          # [[node1, node2, ...], ...]

    def dfs_collect(node, path):
        if not node:
            return
        path.append(node)               # 把当前节点加入当前路径
        if not node.left and not node.right:   # 叶子节点
            all_paths.append(list(path))        # 保存一条完整路径的拷贝
        else:
            dfs_collect(node.left, path)
            dfs_collect(node.right, path)
        path.pop()                     # 回溯，撤销当前节点

    dfs_collect(root, [])

    # 2. 标记所有需要删除的节点
    to_delete = set()      # 用集合存放需要删除的节点对象（方便 O(1) 查）

    for path in all_paths:
        path_sum = sum(node.val for node in path)
        if path_sum < limit:                # 这条路径不够“钱”
            to_delete.update(path)          # 路径上的所有节点都要删

    # 3. 再遍历一次树，把标记的节点真正从父节点切断
    def prune(node, parent, is_left):
        if not node:
            return
        # 先递归处理子树，防止子树被提前删除后找不到父节点
        prune(node.left, node, True)
        prune(node.right, node, False)

        if node in to_delete:                # 当前节点需要删除
            if parent:                        # 有父节点时，把对应的指针设为 None
                if is_left:
                    parent.left = None
                else:
                    parent.right = None

    prune(root, None, False)

    # 如果根本身被删掉，返回 None
    return None if root in to_delete else root
```

#### 复杂度

- **时间复杂度**：`O(n²)`（最坏情况下每个节点会出现在很多路径里，被重复遍历）
  - 大白话：想象一棵非常不平衡的树，根到每个叶子都要走一次全树，导致工作量像 “数数” 一样成平方增长。
- **空间复杂度**：`O(n log n)`（存所有路径的额外空间）
  - 大白话：我们把每条路径都记下来，路径越长占的空间越多，最坏大约是 `n` 条路径 * 每条 `log n` 长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **把所有路径都保存下来**，导致大量重复遍历。  
其实我们只需要 **自底向上**（后序）一次遍历，就能判断每个节点是否“够格”。思路如下：

1. **从叶子往上返回**：对每个节点，计算 **从该节点到任意叶子的最大路径和**（记为 `maxDown`）。  
   - 叶子节点的 `maxDown = node.val`（只能自己）。
   - 非叶子节点的 `maxDown = node.val + max(leftMax, rightMax)`（挑选左/右子树中更大的那条路继续走下去）。
2. **判断是否删除**：如果 `maxDown < limit`，说明 ******从该节点出发的所有根到叶子路径的和** 都小于 `limit`，因为 `maxDown` 已经是最大的可能和，仍然不够。于是把这整棵子树 **剪掉**（返回 `None`）。
3. **递归返回**：如果 `maxDown >= limit`，说明还有至少一条满足要求的路径，保留当前节点，同时把已经可能被剪掉的左/右子树（返回值可能是 `None`）挂回去。

这就是一次 **深度优先搜索**（DFS）完成的 **后序遍历**（先处理子树再处理自己），不需要额外存储所有路径。

> **核心数据结构解释**  
> - **递归栈**：每一次函数调用会在电脑的“记事本”里留下一个小纸条，记录当前节点和已经累计的路径和。递归结束后纸条会被撕掉，回到上一个节点。  
> - **返回值（子树根）**：我们让递归函数返回 **可能被剪掉的子树根**（`None` 表示这棵子树已经被全部删除），父节点只需要把它接回来即可。

> **类比**  
> 想象你在爬山，山顶是叶子，山根是根节点。每一步都有一个“海拔高度”（路径和）。我们从山顶往下看，记录每条路的最高海拔（`maxDown`），如果最高海拔连山根都达不到公司规定的最低海拔 `limit`，这整座小山就不值得保留，直接推倒。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def insufficientNodes(root: TreeNode, limit: int) -> TreeNode:
    """
    后序 DFS：返回剪枝后的子树根（可能为 None）
    """
    def dfs(node: TreeNode) -> TreeNode:
        if not node:                         # 空节点直接返回 None
            return None

        # 递归处理左、右子树，得到剪枝后的子树根
        node.left = dfs(node.left)
        node.right = dfs(node.right)

        # 计算从当前节点向下的最大路径和
        # 如果左右子树都被剪掉了，max_child 为 0（相当于只剩自己）
        left_max = node.left.val if node.left else None
        right_max = node.right.val if node.right else None

        # 下面的 max_child 实际上是「从子节点到叶子的最大和」加上子节点本身的值
        # 为了不额外记录，我们直接用子树根的值（因为子树根已经是「最大和」的节点）
        max_child = max(
            (node.left.val if node.left else float('-inf')),
            (node.right.val if node.right else float('-inf'))
        )
        # 如果左右子树都不存在，max_child 为 -inf，后面会只保留 node.val

        # 当前节点的最大向下路径和
        max_down = node.val if max_child == float('-inf') else node.val + max_child

        # 若最大向下和仍然小于 limit，则整棵子树都要删除
        if max_down < limit:
            return None                      # 剪掉，返回 None 让父节点断开链接

        return node                          # 保留，返回自身（可能已经把子树剪掉）

    return dfs(root)
```

> **代码细节说明**  
> 1. `dfs` 返回 **剪枝后的根**，父节点负责把返回值接回去。  
> 2. `max_child` 用 `float('-inf')` 表示 “不存在的子树”，这样在只有单侧子树或叶子时计算 `max_down` 能保持正确。  
> 3. 当 `max_down < limit` 时直接返回 `None`，相当于把整棵子树从树中摘除。  

#### 复杂度

- **时间复杂度**：`O(n)`，只遍历每个节点一次。  
  - 大白话：像是只走了一遍树的每个房间，没重复走回头路，所以工作量跟节点数成正比。
- **空间复杂度**：`O(h)`，其中 `h` 是树的高度，用来保存递归调用栈。  
  - 对于平衡二叉树 `h ≈ log₂ n`，最坏（完全倾斜）时 `h = n`，仍然比暴力解的 `O(n log n)` 要好。

---

## 心得

- **核心技巧**：后序深度优先遍历 + “从子树返回的最大路径和” 判断剪枝。  
- **适用的题型**  
  1. “删除不满足条件的子树” 类题目（如 LeetCode 1110、1080 等）。  
  2. “在树上求满足某种约束的路径/子树” 类题目（如求最长递增路径、最大路径和等）。  
- **解题钥匙**：**自底向上**思考——先弄清楚子树的“最佳表现”，再决定父节点是否还能留下。

---

## 反思

- **第一反应**：看到“所有根到叶子路径的和 < limit 就删”，立刻想到枚举所有路径，写个 `DFS` 把路径保存下来。  
- **最容易踩的坑**  
  1. **边界条件**：叶子节点本身可能已经不满足 `limit`，需要把它直接剪掉。  
  2. **负数 limit**：路径和可能是负数，不能把 `max_child` 当成 0 来处理，否则会误判。  
  3. **递归返回值**：忘记把剪枝后的子树根接回父节点，会导致父节点仍然指向已经删除的节点。  
- **下次第一步**：先问自己“如果只看这棵子树内部，是否已经可以判断是否需要删除？”——这会自然引导到 **后序 DFS** 的思路。