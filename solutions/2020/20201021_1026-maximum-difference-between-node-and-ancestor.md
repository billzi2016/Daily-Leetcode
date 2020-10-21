# #1026. 节点与祖先之间的最大差值 / Maximum Difference Between Node and Ancestor

> 难度：中等 · 标签：Tree、Depth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/maximum-difference-between-node-and-ancestor/)

---

## 题目（英文原版）

**Description**

Given the root of a binary tree, find the maximum value v for which there exist different nodes a and b where v = |a.val - b.val| and a is an ancestor of b.
A node a is an ancestor of b if either: any child of a is equal to b or any child of a is an ancestor of b.

**Examples**

**Example 1:**

```
Input: root = [8,3,10,1,6,null,14,null,null,4,7,13]
Output: 7
Explanation: We have various ancestor-node differences, some of which are given below :
|8 - 3| = 5
|3 - 7| = 4
|8 - 1| = 7
|10 - 13| = 3
Among all possible differences, the maximum value of 7 is obtained by |8 - 1| = 7.
```

**Example 2:**

```
Input: root = [1,null,2,null,0,3]
Output: 3
```

**Constraints**

- The number of nodes in the tree is in the range [2, 5000].
- 0 <= Node.val <= 105

---

## 题目（中文翻译）

给定一棵二叉树（binary tree）的根节点 `root`，求最大值 `v`，满足存在不同的节点 `a` 和 `b`，使得  

```
v = |a.val - b.val|
```  

且 `a` 是 `b` 的祖先（ancestor）。

节点 `a` 是节点 `b` 的祖先，当且仅当满足以下任意一种情况：

- `a` 的任意子节点（child）等于 `b`；
- `a` 的任意子节点本身是 `b` 的祖先。

---

## 示例

### 示例 1

**输入**  
```
root = [8,3,10,1,6,null,14,null,null,4,7,13]
```

**输出**  
```
7
```

**解释**  
我们可以得到多种祖先‑节点之间的差值，部分如下：

- |8 - 3| = 5  
- |3 - 7| = 4  
- |8 - 1| = 7  
- |10 - 13| = 3  

在所有可能的差值中，最大值为 7，来源于 |8 - 1| = 7。

### 示例 2

**输入**  
```
root = [1,null,2,null,0,3]
```

**输出**  
```
3
```

---

## 约束条件

- 树中节点的数量在 `[2, 5000]` 区间内。  
- `0 <= Node.val <= 10^5`   (节点值范围)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是「对每一个节点 a，都把它所有的子孙节点 b 列举出来，算一次 |a.val‑b.val|，把最大的记下来」。  
这相当于把树展开成「父子关系网」，然后把每一条「祖先 → 后代」的路径都遍历一遍。

- **用到的数据结构**  
  - **二叉树**：每个节点有 `left`、`right` 两个指针。可以把它想象成「左手边的孩子」和「右手边的孩子」。
  - **递归/栈**：我们用深度优先搜索（DFS）把树的每个节点都访问到。递归本质上就是系统帮我们维护的「栈」，类似我们在超市排队时把所有要买的东西一个个放进购物车。

- **为什么正确**  
  对每个节点我们都穷举它所有的后代，算出所有可能的 |祖先值‑后代值|。因为「最大」一定出现在这全部可能的组合里，所以取最大值一定是答案。

- **时间/空间复杂度**  
  - 对每个节点 `a`，我们都要遍历它的全部子树。若树有 `n` 个节点，最坏情况下（比如链状树）第一次遍历要看 `n` 个节点，第二次看 `n‑1`，…，最后一次只看 1 个，总共大约是 `n + (n‑1) + … + 1 = n·(n+1)/2`，即 **O(n²)**。  
    大白话：如果树有 1000 个节点，暴力解大约要算 500 000 次差值，随节点数增大，次数会呈「平方」增长，速度很快就跟不上了。
  - 递归调用栈最多保存树的高度 `h`（最坏 `h = n`），所以 **O(h)**，即 **O(n)** 的空间。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的数值
        self.left = left        # 左子树
        self.right = right      # 右子树

def maxDiffAncestor_bruteforce(root: TreeNode) -> int:
    """暴力解：对每个节点遍历它的所有后代，求最大差值"""
    # 辅助函数：收集 node 的所有后代节点的值
    def collect_descendants(node):
        if not node:
            return []
        vals = []
        # 递归收集左子树和右子树的后代
        vals += collect_descendants(node.left)
        vals += collect_descendants(node.right)
        # 把子节点本身也加入（因为子节点是自己的后代）
        if node.left:
            vals.append(node.left.val)
        if node.right:
            vals.append(node.right.val)
        return vals

    # 主函数：遍历每个节点，计算差值
    max_diff = 0

    def dfs(node):
        nonlocal max_diff
        if not node:
            return
        # 取出当前节点的所有后代的值
        descendants = collect_descendants(node)
        for d in descendants:
            diff = abs(node.val - d)
            if diff > max_diff:
                max_diff = diff
        # 继续向下遍历
        dfs(node.left)
        dfs(node.right)

    dfs(root)
    return max_diff
```

#### 复杂度

- **时间复杂度：O(n²)**  
  解释：每个节点都要遍历它的子树，子树大小随节点位置不同而不同，最坏情况下会出现「平方级」的遍历次数。
- **空间复杂度：O(n)**  
  解释：递归栈深度最坏等于树的高度，链状树时高度等于节点数 `n`，因此需要 `n` 层栈帧。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于「每次都要把整棵子树遍历一遍」——重复工作太多。  
其实我们只需要 **沿着从根到当前节点的路径** 记住「已经出现过的最小值」和「已经出现过的最大值」。因为：

- 对于任意祖先 `a` 与当前节点 `b`，`|a.val - b.val|` 的最大值一定是  
  `max( |b.val - min_on_path| , |b.val - max_on_path| )`。  
  这里的 `min_on_path` / `max_on_path` 分别是从根到 `b`（包括 `b` 本身）之间的最小、最大节点值。

于是我们在一次深度优先遍历（DFS）中，**随时维护这两个极值**：

1. 进入节点 `node` 时，已知从根到它父节点的 `cur_min`、`cur_max`。  
2. 用 `node.val` 与这两个极值算差值，更新全局答案。  
3. 把 `node.val` 加入路径极值：`new_min = min(cur_min, node.val)`、`new_max = max(cur_max, node.val)`。  
4. 递归处理左子树、右子树，传入 `new_min`、`new_max`。

这只需要一次遍历，时间 **O(n)**，空间只剩下递归栈的高度 **O(h)**（平均 `O(log n)`，最坏 `O(n)`）。

> **核心概念——路径上的最值**  
> 想象你在爬山，沿途的最高点和最低点已经记在心里。到达某个新地点时，只要比较「当前海拔」与「最高/最低海拔」的差，就能立刻得到「这段路上最大的落差」。

#### 代码（Python）

```python
def maxDiffAncestor(root: TreeNode) -> int:
    """最优解：一次 DFS，沿路径维护最小值和最大值"""
    # 用一个非局部变量记录全局最大差值
    max_diff = 0

    def dfs(node, cur_min, cur_max):
        """
        node      : 当前访问的节点
        cur_min   : 从根到父节点路径上出现的最小值
        cur_max   : 从根到父节点路径上出现的最大值
        """
        nonlocal max_diff
        if not node:
            return

        # 计算当前节点与路径极值的差值，更新全局答案
        diff1 = abs(node.val - cur_min)
        diff2 = abs(node.val - cur_max)
        max_diff = max(max_diff, diff1, diff2)

        # 更新路径上的最小值和最大值，准备传给子节点
        new_min = min(cur_min, node.val)
        new_max = max(cur_max, node.val)

        # 继续向左、右子树递归
        dfs(node.left, new_min, new_max)
        dfs(node.right, new_min, new_max)

    # 初始时根节点本身就是最小也是最大
    dfs(root, root.val, root.val)
    return max_diff
```

#### 复杂度

- **时间复杂度：O(n)** — 只遍历每个节点一次。与暴力解相比，从「平方级」降到了「线性级」，即使 5000 个节点也能在毫秒级完成。
- **空间复杂度：O(h)** — 递归栈的深度等于树的高度。对于平衡二叉树 `h ≈ log₂ n`，最坏（链状树）时 `h = n`，但仍在可接受范围。

---

## 心得

- **核心技巧**：**在遍历的过程中维护路径上的最小值 / 最大值**，把「全局」信息压缩到「局部」状态。
- **适用的题型**  
  1. “Maximum Difference Between Node and Ancestor”（本题）  
  2. “Binary Tree Maximum Path Sum” – 需要沿路径累计最大/最小信息  
  3. “Validate Binary Search Tree” – 用上下界限制递归，类似维护极值
- **一句话总结**：**只要在 DFS 时把“沿路的最小/最大”带进去，所有祖先‑后代的差值都能在 O(1) 时间算出**。

---

## 反思

- **第一反应**：看到「祖先‑后代」的关系，马上想到「对每个节点遍历它的子树」——也就是暴力思路。
- **最容易踩的坑**  
  - **忘记把根节点本身计入最小/最大**，导致首层差值被错算为 0。  
  - **递归返回值写错**：最优解不需要返回子树的最值，只需要把它们作为参数传下去。  
  - **边界条件**：树可能只有左子树或右子树，递归要对 `None` 做保护。
- **下次类似题的第一步**：**先思考“在从根到当前节点的路径上，有哪些全局信息是一次遍历就能累计的？”**，通常是最值、和、计数等，这会直接指向 O(n) 的解法。