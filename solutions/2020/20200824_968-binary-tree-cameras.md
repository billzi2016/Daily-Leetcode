# #968. 二叉树摄像头 / Binary Tree Cameras

> 难度：困难 · 标签：Dynamic Programming、Tree、Depth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/binary-tree-cameras/)

---

## 题目（英文原版）

**Description**

You are given the root of a binary tree. We install cameras on the tree nodes where each camera at a node can monitor its parent, itself, and its immediate children.
Return the minimum number of cameras needed to monitor all nodes of the tree.

**Examples**

**Example 1:**

```
Input: root = [0,0,null,0,0]
Output: 1
Explanation: One camera is enough to monitor all nodes if placed as shown.
```

**Example 2:**

```
Input: root = [0,0,null,0,null,0,null,null,0]
Output: 2
Explanation: At least two cameras are needed to monitor all nodes of the tree. The above image shows one of the valid configurations of camera placement.
```

**Constraints**

- The number of nodes in the tree is in the range [1, 1000].
- Node.val == 0

---

## 题目（中文翻译）

给定一棵二叉树（binary tree）的根节点 `root`。我们可以在树的节点上安装摄像头，每个摄像头能够监视它的父节点、它自身以及它的直接子节点。  
返回监视整棵树所有节点所需的最少摄像头数量。

**示例 1**  
**示例 2**  
**约束条件**  

### 示例

#### 示例 1
```
Input: root = [0,0,null,0,0]
Output: 1
Explanation: 只需要在如图所示的位置放置一个摄像头，即可监视所有节点。
```

#### 示例 2
```
Input: root = [0,0,null,0,null,0,null,null,0]
Output: 2
Explanation: 至少需要两个摄像头才能监视整棵树。上图展示了一种合法的摄像头放置方案。
```

### 约束条件
- 树中节点的数量在 `[1, 1000]` 区间内。
- `Node.val == 0`（所有节点的值均为 0）。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **枚举每一种可能的摄像头放置方式**，然后检查这种方式能否把所有节点都监控到，最后取摄像头最少的那种。  

- **枚举方式**：把树的每个节点看成一个开关，`0` 表示不装摄像头，`1` 表示装。对 `n` 个节点就有 `2ⁿ` 种组合。  
- **检查覆盖**：遍历整棵树，判断每个节点是否被以下三者之一监控到  
  1. 它自己装了摄像头  
  2. 它的父节点装了摄像头  
  3. 它的左/右子节点装了摄像头  

> **类比**：把树想成一栋楼，每个房间（节点）里可以装摄像头，摄像头的视野覆盖自己、上下楼（父子关系）。我们把所有房间的装摄像头情况列出来，然后看哪些组合能够让每个房间都在摄像头的视野里。

这种方法一定能得到答案，因为它把**所有**可能的放置方式都遍历了一遍。只是不实际可行，尤其当节点数稍大（如 20）时，`2²⁰ ≈ 1,048,576` 种组合已经让程序跑得很慢，而题目最多 1000 个节点，根本不可能穷举。

#### 代码（Python）

```python
# -*- coding: utf-8 -*-
from typing import Optional, List
from itertools import product
import sys
sys.setrecursionlimit(2000)   # 防止递归太深

# 二叉树的定义（LeetCode 默认）
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def tree_to_list(root: Optional[TreeNode]) -> List[int]:
    """把二叉树转成层序列表，方便调试（不必在答案里使用）"""
    if not root:
        return []
    from collections import deque
    q = deque([root])
    res = []
    while q:
        node = q.popleft()
        if node:
            res.append(node.val)
            q.append(node.left)
            q.append(node.right)
        else:
            res.append(None)
    # 去掉末尾的 None
    while res and res[-1] is None:
        res.pop()
    return res

def brute_min_camera(root: Optional[TreeNode]) -> int:
    """暴力枚举所有摄像头放置方式，返回最小摄像头数"""
    # 先把所有节点收集到一个列表，方便用下标表示
    nodes = []
    def dfs(node):
        if not node:
            return
        nodes.append(node)
        dfs(node.left)
        dfs(node.right)
    dfs(root)
    n = len(nodes)

    best = float('inf')   # 记录目前找到的最少摄像头数

    # 用 product 生成 0/1 的所有组合（2^n 种）
    for mask in product([0, 1], repeat=n):
        # 统计本次组合的摄像头数量，剪枝：若已经不可能比 best 更好，就直接跳过
        cam_cnt = sum(mask)
        if cam_cnt >= best:
            continue

        # 把每个节点是否装摄像头记录在字典里，方便后面查询
        has_cam = {node: bool(mask[i]) for i, node in enumerate(nodes)}

        # 检查每个节点是否被监控到
        def covered(node):
            if not node:
                return True      # 空节点自然被“覆盖”
            if has_cam[node]:
                return True      # 自己装摄像头
            if node.left and has_cam[node.left]:
                return True      # 左子节点装摄像头
            if node.right and has_cam[node.right]:
                return True      # 右子节点装摄像头
            if node.left and has_cam.get(node.left, False):
                return True
            if node.right and has_cam.get(node.right, False):
                return True
            # 父节点的摄像头需要在遍历时额外判断，这里采用递归向上检查
            # 为了简化，直接把父节点的摄像头也算在子节点的检查里
            return False

        # 为了判断父节点是否装摄像头，我们在遍历时把父节点信息一起传下去
        ok = True
        def check(node, parent_has_cam=False):
            nonlocal ok
            if not node or not ok:
                return
            # 当前节点是否被监控到
            if (has_cam[node] or
                parent_has_cam or
                (node.left and has_cam[node.left]) or
                (node.right and has_cam[node.right])):
                pass
            else:
                ok = False
                return
            # 继续检查左右子树，传递当前节点是否装摄像头
            check(node.left, has_cam[node])
            check(node.right, has_cam[node])

        check(root)
        if ok:
            best = cam_cnt

    return best if best != float('inf') else -1   # -1 表示没有合法方案（理论上不会出现）
```

> **说明**：  
> - 代码里用了 `product([0,1], repeat=n)` 产生所有 `0/1` 组合。  
> - `check` 函数在遍历时把父节点是否装摄像头的状态传下来，完整地判断每个节点是否被监控。  
> - 由于是暴力搜索，时间会随 `n` 指数级增长，只能在极小的测试例子上跑通。

#### 复杂度  

- **时间复杂度**：`O(2ⁿ * n)`  
  - `2ⁿ` 是所有可能的摄像头放置方式；对每种方式我们要遍历整棵树（`n`）来检查覆盖。  
  - 大白话：如果树有 20 个节点，需要检查 `2²⁰ ≈ 1,000,000` 种情况，每种情况再看 20 次，总共约 20 百万次操作。节点稍多就会爆炸。  

- **空间复杂度**：`O(n)`  
  - 主要是存放节点列表和递归栈（深度最坏 `n`），以及 `has_cam` 字典。  

---

### 2. 最优解  

#### 思路  

暴力解的**瓶颈**在于它把每一种摄像头放置方式都列举了一遍，而实际上我们只关心每个子树的**状态**，而不是具体哪一个节点装摄像头。  
如果我们能把“子树到底需要几台摄像头才能让它以及上层满足监控要求”这件事，用**少量的状态信息**概括，就可以把指数级的枚举压缩到线性时间。

**核心想法**：对每个节点，分别考虑三种可能的“局部状态”  

| 状态 | 含义 |
|------|------|
| `0`（有摄像头） | 这个节点上装了摄像头。它自己、父节点、左右子节点全部被监控。 |
| `1`（已被监控） | 这个节点没有摄像头，但已经被子节点的摄像头监控到了。 |
| `2`（未被监控） | 这个节点既没有摄像头，也没有被子节点监控，需要由父节点来装摄像头。 |

> **类比**：把每个节点想成一个小房间，房间可以有三种“安全等级”。  
> - 等级 0：房间里装了摄像头，安全感最强。  
> - 等级 1：房间里没有摄像头，但邻居（子房间）装了摄像头，安全感也够。  
> - 等级 2：房间里既没有摄像头，也没有邻居装摄像头，只有上层（父房间）装摄像头才能保安全。

我们使用**后序遍历（深度优先搜索）**从叶子向根部计算每个节点在这三种状态下需要的最少摄像头数量。  

**状态转移**（设 `L0,L1,L2` 为左子树在三种状态下的最小摄像头数，`R0,R1,R2` 为右子树对应的数）：

1. **节点装摄像头（状态 0）**  
   - 左右子树可以是任意状态，因为摄像头已经覆盖了它们。  
   - `dp0 = 1 + min(L0, L1, L2) + min(R0, R1, R2)`  
   - 加 `1` 表示在当前节点放一个摄像头。

2. **节点已被监控（状态 1）**  
   - 必须保证至少有 **一个子节点装摄像头**（否则父节点装摄像头也只能覆盖当前节点，无法让当前节点“已被监控”）。  
   - 计算方式：  
     - 让左子树装摄像头，右子树随意：`L0 + min(R0, R1)`  
     - 让右子树装摄像头，左子树随意：`R0 + min(L0, L1)`  
   - 取两者最小：`dp1 = min(L0 + min(R0, R1), R0 + min(L0, L1))`

3. **节点未被监控（状态 2）**  
   - 只能依赖父节点来装摄像头，所以**子树必须已经被监控**（不能是状态 2）。  
   - `dp2 = min(L1, L0) + min(R1, R0)`  
   - 这里不加 `1`，因为当前节点本身不装摄像头。

**根节点的处理**  
- 树的根没有父节点，根必须被监控。  
- 所以答案是 `min(root_state0, root_state1)`（根装摄像头或根已被子节点监控），根不能取状态 2。

**为什么这能得到最优**  
- 每个子树的最优解只和它自己的三种状态有关，和更高层的细节无关（子树内部已经“自洽”）。  
- 通过后序遍历，我们保证在计算父节点状态时，子节点的最优结果已经准备好。  
- 只考虑三种状态，避免了指数级的组合枚举，时间线性。

#### 代码（Python）

```python
# -*- coding: utf-8 -*-
from typing import Optional
import sys
sys.setrecursionlimit(2000)   # 防止深度递归时栈溢出

# LeetCode 默认的二叉树结点定义
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def minCameraCover(self, root: Optional[TreeNode]) -> int:
        """
        返回最少摄像头数量，使得二叉树所有节点都被监控到。
        使用后序遍历 + 动态规划（每个节点三种状态）。
        """

        # dfs 返回一个长度为 3 的元组：
        #   dp[0] = 当前节点装摄像头时的最少摄像头数
        #   dp[1] = 当前节点已被监控（但自己没有摄像头）时的最少摄像头数
        #   dp[2] = 当前节点未被监控，需要父节点装摄像头时的最少摄像头数
        def dfs(node: Optional[TreeNode]):
            if not node:
                # 空节点不需要摄像头，且视作已被监控（因为它不存在），
                # 但是如果父节点想让它“未被监控”，这是不可能的，用一个很大的数表示。
                return (float('inf'), 0, 0)

            L0, L1, L2 = dfs(node.left)   # 左子树三种状态的最优值
            R0, R1, R2 = dfs(node.right)  # 右子树三种状态的最优值

            # 1. 当前节点装摄像头
            dp0 = 1 + min(L0, L1, L2) + min(R0, R1, R2)

            # 2. 当前节点已被监控（但自己不装摄像头）
            # 必须保证左、右至少有一个子节点装摄像头
            dp1 = min(
                L0 + min(R0, R1),   # 左子树装摄像头，右子树随意（已监控或装摄像头）
                R0 + min(L0, L1)    # 右子树装摄像头，左子树随意
            )

            # 3. 当前节点未被监控，需要父节点装摄像头
            # 子树必须已经被监控，不能是状态 2
            dp2 = min(L1, L0) + min(R1, R0)

            return (dp0, dp1, dp2)

        root0, root1, root2 = dfs(root)
        # 根节点没有父节点，不能取状态 2
        return min(root0, root1)
```

> **代码要点注释**  
> - `float('inf')` 用来表示“不可能的情况”。在空节点的 `dp0` 中使用它，防止在父节点需要“左子树装摄像头”时选到空节点。  
> - `dp2`（未被监控）在根节点时不使用，因为根没有父节点可以帮它监控。  
> - 递归的返回值是一个 **元组**，一次返回三种状态，避免全局变量，使函数更易理解。  

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 每个节点只访问一次，做常数次的算术比较。  
  - 与暴力解的 `O(2ⁿ)` 相比，线性时间在 1000 个节点的限制下轻松跑完。  

- **空间复杂度**：`O(h)`（递归栈）  
  - `h` 是树的高度，最坏情况下（完全不平衡的链状树）`h = n`，即 `O(n)`。  
  - 额外的 DP 表只用常数空间（每次递归返回 3 个整数），不随 `n` 增长。

---

## 心得  

- **核心技巧**：**树形动态规划 + 三状态 DP**。  
- **适用的题型**  
  1. **监控/覆盖类**：如 LeetCode 968（二叉树摄像头）、LeetCode 337（打家劫舍 III）  
  2. **选择子树结构**：如 LeetCode 124（二叉树中的最大路径和）在某些变形中也可以用状态划分。  
- **一句话总结**：把每棵子树的“是否需要父节点帮助”抽象为少数几种状态，用后序遍历自底向上求最优。

---

## 反思  

- **第一反应**：先想到枚举所有摄像头放置方式——最直观但不切实际。  
- **最容易踩的坑**  
  1. **状态定义不完整**：忘记考虑“子树已经被监控但没有摄像头”这种状态，导致递归转移出错。  
  2. **空节点的处理**：空节点的 `dp0` 必须设为无穷大，否则会错误地让父节点把摄像头“装在空位置”。  
  3. **根节点的特殊性**：根没有父节点，不能取“未被监控”状态。  
- **下次类似题目**：第一步先**划分子问题的状态**（比如“装摄像头”“已覆盖”“未覆盖”），再**写出状态转移**，最后用 **后序遍历** 把子树的答案合并到父节点。这样可以把指数级的搜索压缩到线性时间。